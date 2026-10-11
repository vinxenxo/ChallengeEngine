"""Static verification for the proposed D renderer I/O boundary.

This test validates only the contract document and prospective schemas. It
never builds a renderer input, creates an output manifest, dispatches a renderer,
launches Godot/FFmpeg, or writes media. jsonschema is optional, matching the
existing repository tests' optional Draft 2020-12 library behavior.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any, Mapping

try:
    if os.environ.get("C11D_FORCE_NO_JSONSCHEMA") == "1":
        raise ImportError("forced fallback validation")
    import jsonschema
except ImportError:  # Windows operator environment may not have jsonschema installed.
    jsonschema = None

ROOT = Path(__file__).resolve().parents[3]
PRODUCTION = Path("definitions/c11d/production")
CONTRACT_REL = PRODUCTION / "D_RENDERER_CANDIDATE_IO_CONTRACT_V1.json"
CONTRACT_SCHEMA_REL = PRODUCTION / "D_RENDERER_CANDIDATE_IO_CONTRACT_SCHEMA_V1.json"
INPUT_SCHEMA_REL = PRODUCTION / "D_RENDERER_CANDIDATE_INPUT_SCHEMA_V1.json"
OUTPUT_SCHEMA_REL = PRODUCTION / "D_RENDERER_CANDIDATE_OUTPUT_MANIFEST_SCHEMA_V1.json"
FROZEN_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SAFE_RELATIVE_PATH_RE = re.compile(r"^(?!/)(?![A-Za-z]:)(?!.*\.\.)(?:[A-Za-z0-9_.-]+/)*[A-Za-z0-9_.-]+$")


class ContractError(ValueError):
    """Raised when the proposed interface contract fails closed."""


def read_json(root: Path, rel: Path) -> dict[str, Any]:
    try:
        value = json.loads((root / rel).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractError(f"Cannot read JSON contract {rel}: {exc}") from exc
    if not isinstance(value, dict):
        raise ContractError(f"JSON contract root must be an object: {rel}")
    return value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def assert_schema_shape(schema: Mapping[str, Any], label: str) -> None:
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise ContractError(f"{label} must declare Draft 2020-12")
    if schema.get("type") != "object" or schema.get("additionalProperties") is not False:
        raise ContractError(f"{label} must be a strict object schema")
    props = schema.get("properties")
    required = schema.get("required")
    if not isinstance(props, Mapping) or not isinstance(required, list):
        raise ContractError(f"{label} must define properties and required arrays")
    missing = sorted(set(required) - set(props))
    if missing:
        raise ContractError(f"{label} required fields are not defined: {missing}")
    defs = schema.get("$defs")
    if not isinstance(defs, Mapping) or "sha256" not in defs:
        raise ContractError(f"{label} must define its SHA-256 schema")


def verify_pins(root: Path, contract: Mapping[str, Any]) -> int:
    pins = contract.get("source_pins")
    if not isinstance(pins, list) or len(pins) < 25:
        raise ContractError("Source pin list is missing or unexpectedly small")
    seen: set[str] = set()
    for pin in pins:
        if not isinstance(pin, Mapping):
            raise ContractError("Each source pin must be an object")
        rel_text = pin.get("path")
        expected = pin.get("sha256")
        if not isinstance(rel_text, str) or not SAFE_RELATIVE_PATH_RE.fullmatch(rel_text) or rel_text in seen:
            raise ContractError(f"Invalid, escaping or duplicate source pin path: {rel_text!r}")
        seen.add(rel_text)
        if not isinstance(expected, str) or not SHA256_RE.fullmatch(expected):
            raise ContractError(f"Invalid SHA-256 syntax for source pin: {rel_text}")
        path = root / rel_text
        if not path.is_file():
            raise ContractError(f"Pinned source file is missing: {rel_text}")
        actual = sha256_file(path)
        if actual != expected:
            raise ContractError(f"Pinned source SHA-256 mismatch: {rel_text}")
    return len(pins)



def build_schema_example(schema: Mapping[str, Any], root_schema: Mapping[str, Any], field_name: str = "") -> Any:
    """Create synthetic in-memory schema fixtures only; never persist or dispatch them."""
    if "$ref" in schema:
        ref = schema["$ref"]
        if not isinstance(ref, str) or not ref.startswith("#/"):
            raise ContractError(f"Fixture builder only supports local schema references: {ref!r}")
        resolved: Any = root_schema
        for token in ref[2:].split("/"):
            resolved = resolved[token.replace("~1", "/").replace("~0", "~")]
        return build_schema_example(resolved, root_schema, field_name)
    if "const" in schema:
        return copy.deepcopy(schema["const"])
    if isinstance(schema.get("enum"), list) and schema["enum"]:
        return copy.deepcopy(schema["enum"][0])
    for branch_key in ("oneOf", "anyOf"):
        if isinstance(schema.get(branch_key), list) and schema[branch_key]:
            return build_schema_example(schema[branch_key][0], root_schema, field_name)
    if isinstance(schema.get("allOf"), list) and schema["allOf"]:
        result: dict[str, Any] = {}
        for branch in schema["allOf"]:
            part = build_schema_example(branch, root_schema, field_name)
            if isinstance(part, dict):
                result.update(part)
        return result

    kind = schema.get("type")
    if isinstance(kind, list):
        kind = next((candidate for candidate in kind if candidate != "null"), "null")
    if kind == "object":
        properties = schema.get("properties", {})
        required = schema.get("required", list(properties))
        return {name: build_schema_example(properties[name], root_schema, name) for name in required}
    if kind == "array":
        minimum = schema.get("minItems", 1)
        return [build_schema_example(schema["items"], root_schema, field_name) for _ in range(minimum)] if "items" in schema else []
    if kind == "string":
        pattern = schema.get("pattern", "")
        if "[0-9a-f]{64}" in pattern:
            return "a" * 64
        if field_name == "relative_path":
            return "artifacts/review/example.json"
        return "x" * max(1, int(schema.get("minLength", 1)))
    if kind == "integer":
        return max(0, int(schema.get("minimum", 0)))
    if kind == "number":
        if isinstance(schema.get("exclusiveMinimum"), (int, float)):
            return schema["exclusiveMinimum"] + 1
        return max(1, schema.get("minimum", 0))
    if kind == "boolean":
        return False
    if kind == "null":
        return None
    raise ContractError(f"Fixture builder cannot make an example for schema field {field_name!r}")


def expect_schema_rejection(validator: Any, instance: Mapping[str, Any], label: str) -> None:
    if validator.is_valid(instance):
        raise ContractError(f"Schema instance negative was accepted: {label}")

def assert_current_locks(spec: Mapping[str, Any]) -> None:
    if spec.get("schema") != "C11-D-RENDERER-CANDIDATE-IO-CONTRACT-V1":
        raise ContractError("Unexpected I/O contract identity")
    if spec.get("status") != "PREPARATION_ONLY_INTERFACE_PROPOSAL_NOT_IMPLEMENTED_NOT_APPROVED":
        raise ContractError("I/O contract cannot be marked implemented or approved in this increment")
    boundary = spec.get("boundary_state", {})
    false_locks = (
        "binding_preview_is_renderer_input", "logical_composition_is_renderer_input",
        "frame_program_is_renderer_input", "renderer_input_instance_emitted",
        "renderer_output_manifest_created", "renderer_implementation_added",
        "renderer_dispatch_invoked", "renderer_activation", "production_execution",
        "media_created", "c11c_source_mutation",
    )
    for lock in false_locks:
        if boundary.get(lock) is not False:
            raise ContractError(f"Required false lock was altered: boundary_state.{lock}")
    if boundary.get("output_artifact_path") is not None:
        raise ContractError("Output artifact path must remain null")
    if boundary.get("d4_8") != "BLOCKED" or boundary.get("release_authority") != "NONE":
        raise ContractError("Governance lock was altered")
    admission = spec.get("current_admission_state", {})
    if admission.get("candidate_input_admissible") is not False:
        raise ContractError("Candidate input must remain inadmissible")
    approvals = admission.get("approval_state", {})
    for key in ("interface_design_approved", "renderer_baseline_approved", "renderer_baseline_frozen", "d4_8_authorized"):
        if approvals.get(key) is not False:
            raise ContractError(f"Unexpected approval promotion: {key}")
    if approvals.get("release_authority") != "NONE" or approvals.get("d9_17") != "BLOCKED_NO_GO":
        raise ContractError("D9.17/release status must remain closed to production")


def validate_contract(root: Path, contract: Mapping[str, Any] | None = None) -> tuple[int, int, str, int, int]:
    spec = dict(contract) if contract is not None else read_json(root, CONTRACT_REL)
    contract_schema = read_json(root, CONTRACT_SCHEMA_REL)
    input_schema = read_json(root, INPUT_SCHEMA_REL)
    output_schema = read_json(root, OUTPUT_SCHEMA_REL)
    for schema, label in (
        (contract_schema, "I/O contract schema"),
        (input_schema, "future renderer input schema"),
        (output_schema, "future renderer output manifest schema"),
    ):
        assert_schema_shape(schema, label)
    assert_current_locks(spec)

    schema_mode = "DRAFT202012_VALIDATED"
    schema_fixtures = 0
    schema_instance_negatives = 0
    if jsonschema is not None:
        for schema in (contract_schema, input_schema, output_schema):
            jsonschema.Draft202012Validator.check_schema(schema)
        errors = sorted(jsonschema.Draft202012Validator(contract_schema).iter_errors(spec), key=lambda error: list(error.path))
        if errors:
            first = errors[0]
            location = ".".join(str(part) for part in first.path) or "$"
            raise ContractError(f"Contract schema violation at {location}: {first.message}")

        # These are synthetic, in-memory examples used only to exercise the schemas.
        # They are never written as renderer inputs/output manifests or dispatched.
        input_validator = jsonschema.Draft202012Validator(input_schema)
        output_validator = jsonschema.Draft202012Validator(output_schema)
        input_example = build_schema_example(input_schema, input_schema)
        output_example = build_schema_example(output_schema, output_schema)
        input_validator.validate(input_example)
        output_validator.validate(output_example)
        schema_fixtures = 2

        invalid_input_cases = []
        bad = copy.deepcopy(input_example); bad["authorization"]["renderer_baseline_state"] = "PROPOSED"; invalid_input_cases.append((bad, "renderer baseline not approved/frozen"))
        bad = copy.deepcopy(input_example); bad["seed_domains"]["cross_domain_seed_reuse"] = True; invalid_input_cases.append((bad, "gameplay/music seed reuse"))
        bad = copy.deepcopy(input_example); bad["content_identity"]["content_type"] = "longform"; invalid_input_cases.append((bad, "unsupported content type"))
        bad = copy.deepcopy(input_example); bad["unrecognized_field"] = True; invalid_input_cases.append((bad, "unknown input property"))
        for bad, label in invalid_input_cases:
            expect_schema_rejection(input_validator, bad, label); schema_instance_negatives += 1

        invalid_output_cases = []
        bad = copy.deepcopy(output_example); bad["artifacts"]["video"]["relative_path"] = "artifacts/../release/video.mp4"; invalid_output_cases.append((bad, "output path traversal"))
        bad = copy.deepcopy(output_example); bad["governance"]["release_authority"] = "AUTHORIZED"; invalid_output_cases.append((bad, "release authority promotion"))
        bad = copy.deepcopy(output_example); bad["artifacts"].pop("audio"); invalid_output_cases.append((bad, "missing explicit audio disposition"))
        bad = copy.deepcopy(output_example); bad["qa"]["video_decode"]["status"] = "PENDING"; invalid_output_cases.append((bad, "non-passing video decode QA"))
        for bad, label in invalid_output_cases:
            expect_schema_rejection(output_validator, bad, label); schema_instance_negatives += 1
    else:
        schema_mode = "STRUCTURAL_ONLY_JSONSCHEMA_NOT_INSTALLED"
        # Strict minimal consistency checks used by existing tests when jsonschema is unavailable.
        if contract_schema.get("properties", {}).get("status", {}).get("const") != spec.get("status"):
            raise ContractError("Contract status does not match its contract schema")
        if spec.get("scope", {}).get("content_types") != ["challenges", "visual_loops", "visual_drills"]:
            raise ContractError("Supported content type list drifted")
        if len(spec.get("interface_design", {}).get("source_mapping", [])) < 6:
            raise ContractError("Source mapping is incomplete")

    if spec["interface_design"]["input_schema"]["schema_id"] != input_schema.get("$id"):
        raise ContractError("Input schema $id does not match the contract")
    if spec["interface_design"]["output_manifest_schema"]["schema_id"] != output_schema.get("$id"):
        raise ContractError("Output manifest schema $id does not match the contract")

    pins_count = verify_pins(root, spec)
    frozen = root / "release/C11C_FREEZE_PACKAGE_MANIFEST.json"
    if sha256_file(frozen) != FROZEN_MANIFEST_SHA256:
        raise ContractError("Frozen C11-C manifest mismatch")

    expected_policy_states = {
        "D_RENDERER_UNIFIED_PRESENTATION_REGION_POLICY_PROPOSAL_V1.json": "PROPOSAL_ONLY_NOT_RENDERER_INPUT",
        "D_RENDERER_UNIFIED_DELIVERY_TIMEBASE_POLICY_PROPOSAL_V1.json": "PROPOSAL_ONLY_NOT_RENDERER_INPUT",
        "D_RENDERER_UNIFIED_AUDIO_MUSIC_DELIVERY_POLICY_PROPOSAL_V1.json": "PROPOSAL_ONLY_NOT_RENDERER_INPUT",
        "D_RENDERER_CHALLENGE_TEMPORAL_ALIGNMENT_POLICY_PROPOSAL_V1.json": "PROPOSAL_ONLY_NOT_RENDERER_INPUT",
        "D_RENDERER_CHALLENGE_SIMULATION_SAMPLE_SELECTION_PROPOSAL_V1.json": "PROPOSAL_ONLY_NOT_RENDERER_INPUT",
        "D_RENDERER_CHALLENGE_COORDINATE_SAMPLE_COMPOSITION_PROPOSAL_V1.json": "PROPOSED_NOT_APPROVED_NOT_FROZEN",
        "D_RENDERER_CHALLENGE_COORDINATE_PROJECTION_V1.json": "PROPOSED_NOT_APPROVED_NOT_FROZEN",
        "D_RENDERER_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json": "PROPOSAL_ONLY_NOT_RENDERER_INPUT",
        "D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json": "PROPOSAL_ONLY_NOT_RENDERER_INPUT",
    }
    for filename, expected_state in expected_policy_states.items():
        policy = read_json(root, PRODUCTION / filename)
        if policy.get("status") != expected_state:
            raise ContractError(f"Policy state changed without an explicit contract/version review: {filename}")
        approval_state = policy.get("approval_state", {})
        if isinstance(approval_state, Mapping):
            for key, value in approval_state.items():
                if (key.endswith("_approved") or key in ("renderer_baseline_approved", "renderer_baseline_frozen", "d4_8_authorized")) and value is not False:
                    raise ContractError(f"Policy approval was promoted: {filename}:{key}")

    input_required = set(input_schema.get("required", []))
    must_require = {"source_lineage", "payload_instance", "seed_domains", "presentation", "timeline", "audio", "authorization"}
    if not must_require.issubset(input_required):
        raise ContractError("Future input schema omits a required governed input group")
    input_props = input_schema.get("properties", {})
    authorization_schema = input_props.get("authorization", {}).get("properties", {})
    if authorization_schema.get("renderer_baseline_state", {}).get("const") != "APPROVED_AND_FROZEN":
        raise ContractError("Future input schema must require a separately approved/frozen D renderer baseline")
    if authorization_schema.get("d4_8_state", {}).get("const") != "AUTHORIZED":
        raise ContractError("Future input schema must require explicit D4.8 authorization")
    seed_props = input_props.get("seed_domains", {}).get("properties", {})
    if seed_props.get("automatic_seed_generation", {}).get("const") is not False:
        raise ContractError("Future input schema must forbid automatic seed generation")
    if seed_props.get("cross_domain_seed_reuse", {}).get("const") is not False:
        raise ContractError("Future input schema must forbid gameplay/music seed reuse")
    if input_props.get("content_identity", {}).get("properties", {}).get("content_type", {}).get("enum") != ["challenges", "visual_loops", "visual_drills"]:
        raise ContractError("Future input schema must fail closed for unsupported content types")

    output_required = set(output_schema.get("required", []))
    if not {"source_lineage", "renderer_identity", "delivery", "policy_lineage", "artifacts", "qa", "determinism", "catalog", "governance"}.issubset(output_required):
        raise ContractError("Future output schema omits a required provenance/QA group")
    output_props = output_schema.get("properties", {})
    artifact_fields = set(output_props.get("artifacts", {}).get("required", []))
    if artifact_fields != {"video", "audio", "final_mux"}:
        raise ContractError("Output must separately identify video, audio and final mux artifacts")
    qa_fields = set(output_props.get("qa", {}).get("required", []))
    if not {"video_decode", "audio_policy_conformance", "visual_review", "deterministic_replay", "provenance_and_catalog"}.issubset(qa_fields):
        raise ContractError("Output schema lacks a mandatory QA category")
    release_props = output_props.get("governance", {}).get("properties", {})
    if release_props.get("release_authority", {}).get("const") != "NONE" or release_props.get("release_performed", {}).get("const") is not False:
        raise ContractError("Output manifest must not grant release authority")

    # Negative 1: schema/lock validation rejects a promotion of renderer activation.
    bad_lock = copy.deepcopy(spec)
    bad_lock["boundary_state"]["renderer_activation"] = True
    if jsonschema is not None:
        errors = list(jsonschema.Draft202012Validator(contract_schema).iter_errors(bad_lock))
        if not errors:
            raise ContractError("Contract schema accepted renderer_activation=true")
    else:
        try:
            assert_current_locks(bad_lock)
        except ContractError:
            pass
        else:
            raise ContractError("Structural lock check accepted renderer_activation=true")

    # Negative 2: source hash pins reject tampering.
    bad_pin = copy.deepcopy(spec)
    bad_pin["source_pins"][0]["sha256"] = "0" * 64
    try:
        verify_pins(root, bad_pin)
    except ContractError:
        pass
    else:
        raise ContractError("Source-pin negative did not reject a tampered digest")

    # Negative 3: a source pin cannot escape the repository root.
    bad_pin_path = copy.deepcopy(spec)
    bad_pin_path["source_pins"][0]["path"] = "../../outside.json"
    try:
        verify_pins(root, bad_pin_path)
    except ContractError:
        pass
    else:
        raise ContractError("Source-pin path negative did not reject repository escape")

    # Negative 4: output paths must be relative and confined (path traversal is forbidden).
    for unsafe_path in ("/tmp/output.mp4", "C:/output.mp4", "artifacts/../release/output.mp4"):
        if SAFE_RELATIVE_PATH_RE.fullmatch(unsafe_path):
            raise ContractError(f"Unsafe artifact path was accepted by the path guard: {unsafe_path}")
    if not SAFE_RELATIVE_PATH_RE.fullmatch("artifacts/review/video.mp4"):
        raise ContractError("Safe relative artifact-path fixture was unexpectedly rejected")

    # Negative 5: longform and invented content types must not pass the future input allowlist.
    allowed_types = input_props["content_identity"]["properties"]["content_type"]["enum"]
    if "longform" in allowed_types or "anything_else" in allowed_types:
        raise ContractError("Future input schema widened the supported content type allowlist")

    return pins_count, 5 + schema_instance_negatives, schema_mode, schema_fixtures, schema_instance_negatives


def main() -> int:
    try:
        pin_count, negative_count, schema_mode, schema_fixtures, schema_instance_negatives = validate_contract(ROOT)
    except ContractError as exc:
        print(f"C11-D RENDERER CANDIDATE I/O CONTRACT FAIL | {exc}")
        return 1
    fixture_label = f"schema_fixtures={schema_fixtures}/2" if schema_fixtures else "schema_fixtures=NOT_RUN_NO_JSONSCHEMA"
    print(
        "C11-D RENDERER CANDIDATE I/O CONTRACT PASS | "
        f"source_pins={pin_count}/{pin_count} | schemas=3/3 | schema_validation={schema_mode} | {fixture_label}"
    )
    print(
        f"fail_closed_negatives={negative_count}/{negative_count} | schema_instance_negatives={schema_instance_negatives}/{schema_instance_negatives} | "
        "candidate_input_admissible=false | renderer_input_emitted=false | "
        "renderer_dispatch_invoked=false | media_created=false | "
        "D4.8=BLOCKED | release_authority=NONE"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
