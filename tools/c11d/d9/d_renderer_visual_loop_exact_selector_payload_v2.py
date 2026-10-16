"""Preparation-only, in-memory exact-selector Visual Loop payload audit; never renders media."""
from __future__ import annotations
import argparse
import base64
import copy
import hashlib
import importlib.util
import json
import math
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable, Mapping
try:
    from jsonschema import Draft202012Validator
except ImportError as exc:
    raise RuntimeError("jsonschema is required for exact-selector visual payload V2") from exc

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_VISUAL_LOOP_EXACT_SELECTOR_PAYLOAD_V2.json")
CONTRACT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_VISUAL_LOOP_EXACT_SELECTOR_PAYLOAD_SCHEMA_V2.json")
INPUT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_VISUAL_LOOP_EXACT_SELECTOR_PAYLOAD_INPUT_SCHEMA_V2.json")
REPORT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_VISUAL_LOOP_EXACT_SELECTOR_PAYLOAD_REPORT_SCHEMA_V2.json")
HARNESS_REL = Path("tools/c11d/d9/materialize_visual_loop_exact_selector_payload_v2_in_memory.gd")
PARAMETER_BINDING_REL = Path("tools/c11d/d9/d_renderer_visual_loop_request_scoped_grammar_parameter_binding_v2.py")
PARAMETER_BINDING_CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_VISUAL_LOOP_REQUEST_SCOPED_GRAMMAR_PARAMETER_BINDING_V2.json")
PARAMETER_BINDING_MANIFEST_REL = Path("C11D_VISUAL_LOOP_REQUEST_SCOPED_GRAMMAR_PARAMETER_BINDING_V2_OVERLAY_MANIFEST_20261016.json")
MANIFEST_REL = Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")
EXPECTED_MANIFEST = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
EXPECTED_GODOT_VERSION = "4.7.1.stable.mono.official.a13da4feb"
INPUT_SCHEMA = "C11-D-D9-VISUAL-LOOP-EXACT-SELECTOR-PAYLOAD-INPUT-V2"
PROBE_PREFIX = "C11D_VISUAL_LOOP_EXACT_SELECTOR_PAYLOAD_V2_PROBE="
REPORT_PREFIX = "C11D_VISUAL_LOOP_EXACT_SELECTOR_PAYLOAD_V2_REPORT="
STATUS = "PREPARATION_ONLY_IN_MEMORY_EXACT_SELECTOR_VISUAL_PAYLOADS_NOT_RENDERER_INPUT_NOT_APPROVED"
GRAMMARS = (
    ("harmonic_membrane", 0, "field_harmonic_membrane"),
    ("interference_plane", 1, "field_interference_plane"),
    ("parametric_ribbon", 2, "field_parametric_ribbon"),
    ("lattice_wave", 3, "field_lattice_wave"),
    ("orbital_wave", 4, "field_orbital_wave"),
)
STYLE_KEYS = ("grammar_mode", "palette_mode", "morph", "wave_frequency", "line_width", "glow_strength", "polygon_sides", "wave_ratio", "shape_rotation", "layer_spread", "radial_wave_amplitude", "liss_x_frequency", "liss_y_frequency", "interference_scale", "hero_scale", "perspective_strength", "depth_strength", "secondary_phase", "color_phase", "stroke_scale")
BOUNDARY = {
    "payload_materialized_in_memory": True,
    "payload_file_written": False,
    "receipt_file_written": False,
    "renderer_instance_created": False,
    "shader_material_created": False,
    "shader_executed": False,
    "renderer_native_input_emitted": False,
    "renderer_dispatch_invoked": False,
    "renderer_activation": False,
    "media_created": False,
    "c11c_source_mutation": False,
    "candidate_input_admissible": False,
    "renderer": "OFF",
    "D4.8": "BLOCKED",
    "D9.10": "PREPARE_ONLY",
    "D9.17": "BLOCKED_NO_GO",
    "D10": "BLOCKED",
    "release_authority": "NONE",
}

class ExactSelectorPayloadError(ValueError):
    """Raised when the payload descriptor, source lineage, or governance boundary drifts."""

def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)

def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()

def file_sha(path: Path) -> str:
    if not path.is_file():
        raise ExactSelectorPayloadError(f"Pinned source is missing: {path}")
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def read_json(root: Path, rel: str | Path) -> dict[str, Any]:
    try:
        value = json.loads((root / rel).read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise ExactSelectorPayloadError(f"Cannot read JSON source {rel}: {exc}") from exc
    if not isinstance(value, dict):
        raise ExactSelectorPayloadError(f"Expected JSON object at {rel}")
    return value

def _root(value: str | Path | None = None) -> Path:
    return Path(value).resolve() if value is not None else Path(__file__).resolve().parents[3]

def _load_module(path: Path, name: str):
    if not path.is_file():
        raise ExactSelectorPayloadError(f"Required parent runner is missing: {path}")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ExactSelectorPayloadError(f"Cannot load parent runner: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    sibling = str(path.parent)
    if sibling in sys.path:
        sys.path.remove(sibling)
    sys.path.insert(0, sibling)
    spec.loader.exec_module(module)
    return module

def _is_sha(value: Any) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[a-f0-9]{64}", value) is not None

def _load_contract(root: Path):
    contract = read_json(root, CONTRACT_REL)
    schema = read_json(root, CONTRACT_SCHEMA_REL)
    input_schema = read_json(root, INPUT_SCHEMA_REL)
    report_schema = read_json(root, REPORT_SCHEMA_REL)
    for candidate in (schema, input_schema, report_schema):
        if candidate.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or candidate.get("additionalProperties") is not False:
            raise ExactSelectorPayloadError("All V2 schemas must be strict JSON Schema Draft 2020-12")
        Draft202012Validator.check_schema(candidate)
    try:
        Draft202012Validator(schema).validate(contract)
    except Exception as exc:
        raise ExactSelectorPayloadError(f"Contract schema rejected the contract: {getattr(exc, 'message', str(exc))}") from exc
    if contract.get("schema") != "C11-D-D9-VISUAL-LOOP-EXACT-SELECTOR-PAYLOAD-CONTRACT-V2" or contract.get("schema_version") != "2.0":
        raise ExactSelectorPayloadError("Exact-selector payload contract identity/version mismatch")
    if contract.get("status") != STATUS:
        raise ExactSelectorPayloadError("Contract attempted to self-promote")
    if file_sha(root / MANIFEST_REL) != EXPECTED_MANIFEST or contract.get("authority", {}).get("frozen_c11c_manifest_sha256") != EXPECTED_MANIFEST:
        raise ExactSelectorPayloadError("Frozen C11-C manifest mismatch")
    parent_manifest_sha = file_sha(root / PARAMETER_BINDING_MANIFEST_REL)
    if contract.get("authority", {}).get("parent_parameter_binding_overlay_manifest_sha256") != parent_manifest_sha:
        raise ExactSelectorPayloadError("Parent parameter-binding overlay manifest hash mismatch")
    authority = contract.get("authority", {})
    for path_key, sha_key in (("parent_parameter_binding_contract_path", "parent_parameter_binding_contract_sha256"), ("parent_parameter_binding_runner_path", "parent_parameter_binding_runner_sha256")):
        path_text = authority.get(path_key)
        if not isinstance(path_text, str) or authority.get(sha_key) != file_sha(root / path_text):
            raise ExactSelectorPayloadError(f"Pinned parent binding dependency mismatch: {path_key}")
    observed = [(row.get("grammar_id"), row.get("grammar_index"), row.get("shader_branch")) for row in contract.get("scope", {}).get("grammar_matrix", [])]
    if tuple(observed) != GRAMMARS:
        raise ExactSelectorPayloadError("The five grammar IDs/indexes/branches are not exact")
    if contract.get("scope", {}).get("exact_selector_visual_payload_materialized_in_memory") is not True or contract.get("scope", {}).get("renderer_native_input_emitted") is not False:
        raise ExactSelectorPayloadError("Exact selector materialization or renderer-input boundary changed")
    if contract.get("reference_boundary", {}).get("policy_values_consumed") is not False or contract.get("reference_boundary", {}).get("policy_reference_count_per_selector") != 9:
        raise ExactSelectorPayloadError("Timing/review references crossed the metadata-only boundary")
    if contract.get("approval_state", {}).get("approval_assertions_checked") != 19 or contract.get("approval_state", {}).get("approvals_granted") != 0:
        raise ExactSelectorPayloadError("Approval count is no longer locked at 0/19")
    for key, value in contract.get("approval_state", {}).items():
        if key.endswith(("_approved", "_authorized", "_frozen")) and value is not False:
            raise ExactSelectorPayloadError(f"Approval gate unexpectedly promoted: {key}")
    if contract.get("approval_state", {}).get("release_authority") != "NONE":
        raise ExactSelectorPayloadError("Release authority must remain NONE")
    if contract.get("execution_boundary") != BOUNDARY:
        raise ExactSelectorPayloadError("Execution/governance boundary mismatch")
    harness_record = contract.get("harness", {})
    if harness_record.get("path") != HARNESS_REL.as_posix() or harness_record.get("sha256") != file_sha(root / HARNESS_REL):
        raise ExactSelectorPayloadError("Pinned Godot harness hash mismatch")
    pins = contract.get("source_lineage")
    if not isinstance(pins, list) or len(pins) < 60 or pins[0].get("path") != MANIFEST_REL.as_posix() or pins[0].get("sha256") != EXPECTED_MANIFEST:
        raise ExactSelectorPayloadError("Source lineage is incomplete; frozen C11-C manifest must be first")
    checked = []
    seen = set()
    for row in pins:
        if not isinstance(row, Mapping) or set(row) != {"path", "sha256"}:
            raise ExactSelectorPayloadError("Malformed direct source-lineage row")
        rel, expected = row["path"], row["sha256"]
        p = Path(rel)
        if not isinstance(rel, str) or p.is_absolute() or ".." in p.parts or "\\" in rel or rel in seen:
            raise ExactSelectorPayloadError(f"Unsafe or duplicate source pin: {rel!r}")
        if not _is_sha(expected):
            raise ExactSelectorPayloadError(f"Malformed source pin digest: {rel}")
        actual = file_sha(root / rel)
        if actual != expected:
            raise ExactSelectorPayloadError(f"Pinned source drift: {rel}")
        checked.append({"path": rel, "sha256": actual})
        seen.add(rel)
    try:
        Draft202012Validator(input_schema).validate(_sample_input(contract))
    except Exception as exc:
        # The sample uses syntactically complete placeholders, so failure here indicates a schema defect.
        raise ExactSelectorPayloadError(f"Input schema rejects its own valid-shaped sample: {getattr(exc, 'message', str(exc))}") from exc
    return contract, schema, input_schema, report_schema, checked

def _sample_input(contract: Mapping[str, Any]) -> dict[str, Any]:
    req_hash = "1" * 64
    selection = {"content_type": "visual_loops", "family_id": "c11c_geometric_waves_v1", "subtype_id": "harmonic_membrane", "variant_id": None}
    style = {key: 1.0 for key in STYLE_KEYS}
    style["grammar_mode"] = 0
    parameter = {
        "schema": "C11-D-D9-VISUAL-LOOP-GRAMMAR-PARAMETER-INSTANCE-V2", "schema_version": "2.0", "selection": selection,
        "grammar_id": "harmonic_membrane", "grammar_index": 0, "shader_branch": "field_harmonic_membrane", "shader_uniform": "grammar_mode",
        "style_parameter_count": 20, "style_parameters": style, "gameplay_seed": 1, "request_hash": req_hash,
        "style_parameters_sha256": "2" * 64, "parameter_instance_sha256": "3" * 64,
    }
    request = {"request_id": "sample", "request_hash": req_hash, "selection": selection, "gameplay_seed": 1, "music_seed": 2, "variation_index": 0, "presentation_profile_id": "social_default_v1", "delivery_profile_id": "REVIEW_720"}
    chain = {key: "4" * 64 for key in ("plan_hash", "editorial_hash", "bridge_record_hash", "adapter_envelope_hash", "source_binding_sha256")}
    chain["editorial_hash"] = "5" * 64
    reference = {"carrier_report_sha256": "6" * 64, "selector_envelope_sha256": "7" * 64, "shared_policy_reference_set_sha256": "8" * 64, "policy_reference_count": 9, "policy_values_consumed": False}
    return {
        "schema": INPUT_SCHEMA, "schema_version": "2.0", "contract_sha256": "9" * 64,
        "frozen_c11c_manifest_sha256": EXPECTED_MANIFEST, "parent_binding_report_sha256": "a" * 64,
        "request_identity": request, "canonical_chain": chain, "timing_review_reference": reference,
        "request_parameter_binding_sha256": "b" * 64, "parameter_instance": parameter,
    }

def _validate_probe(report: Mapping[str, Any], probe_input: Mapping[str, Any], contract: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(report, Mapping):
        raise ExactSelectorPayloadError("Godot probe receipt must be an object")
    request = probe_input["request_identity"]
    parameter = probe_input["parameter_instance"]
    selection = request["selection"]
    grammar = selection["subtype_id"]
    grammar_row = next((item for item in contract["scope"]["grammar_matrix"] if item["grammar_id"] == grammar), None)
    if grammar_row is None:
        raise ExactSelectorPayloadError("Selector is outside the fixed five-grammar set")
    expected = {
        "schema": "C11-D-D9-VISUAL-LOOP-EXACT-SELECTOR-PAYLOAD-PROBE-V2",
        "schema_version": "2.0",
        "status": "IN_MEMORY_REVIEW_ONLY_EXACT_SELECTOR_VISUAL_PAYLOAD_NOT_RENDERER_INPUT",
        "contract_sha256": probe_input["contract_sha256"],
        "parent_binding_report_sha256": probe_input["parent_binding_report_sha256"],
        "request_identity": dict(request),
        "canonical_chain": dict(probe_input["canonical_chain"]),
        "timing_review_reference": dict(probe_input["timing_review_reference"]),
        "parent_request_parameter_binding_sha256": probe_input["request_parameter_binding_sha256"],
        "parameter_instance_sha256": parameter["parameter_instance_sha256"],
        "selection": dict(selection),
        "grammar_id": grammar,
        "grammar_index": grammar_row["grammar_index"],
        "shader_branch_review_only": grammar_row["shader_branch"],
        "payload_sections": ["request_identity", "selection", "authoring_envelope", "family_variation_recipe", "resolved_palette", "visual_spec", "timing"],
        "payload_materialized_in_memory": True,
        "deterministic_repeat_pass": True,
        "exact_selector_visual_payload_materialized": True,
        "renderer_shader_mapping_is_review_metadata_only": True,
        "policy_values_consumed": False,
        "non_geometric_family_authoring_gaps_remain_open": True,
        "family_authoring_envelope_gap": "REMAINS_OPEN_OUTSIDE_THIS_GEOMETRIC_SELECTOR_SCOPE",
        "source_checks_passed": True,
        "execution_boundary": BOUNDARY,
    }
    if set(report) != set(expected) | {"authoring_envelope_sha256", "family_variation_recipe_sha256", "resolved_palette_sha256", "visual_spec_sha256", "payload_instance_sha256"}:
        raise ExactSelectorPayloadError("Probe receipt has unknown/missing fields")
    for key, value in expected.items():
        if report.get(key) != value:
            raise ExactSelectorPayloadError(f"Godot receipt mismatch for {key}")
    for key in ("authoring_envelope_sha256", "family_variation_recipe_sha256", "resolved_palette_sha256", "visual_spec_sha256", "payload_instance_sha256"):
        if not _is_sha(report.get(key)):
            raise ExactSelectorPayloadError(f"Malformed in-memory payload digest: {key}")
    if parameter.get("selection") != selection or parameter.get("grammar_id") != grammar or parameter.get("grammar_index") != grammar_row["grammar_index"]:
        raise ExactSelectorPayloadError("Request identity and parameter instance are detached")
    if parameter.get("request_hash") != request.get("request_hash") or parameter.get("gameplay_seed") != request.get("gameplay_seed"):
        raise ExactSelectorPayloadError("Payload parameter instance does not match request hash/seed")
    refs = report["timing_review_reference"]
    if refs.get("policy_reference_count") != 9 or refs.get("policy_values_consumed") is not False:
        raise ExactSelectorPayloadError("Timing/review reference boundary changed")
    return dict(report)

def _run_probe(root: Path, godot: str, timeout: float, contract: Mapping[str, Any], input_schema: Mapping[str, Any], probe_input: Mapping[str, Any], process_runner: Callable[..., Any]) -> dict[str, Any]:
    try:
        Draft202012Validator(input_schema).validate(probe_input)
    except Exception as exc:
        raise ExactSelectorPayloadError(f"Strict payload input schema rejected the case: {getattr(exc, 'message', str(exc))}") from exc
    encoded = base64.b64encode(canonical(probe_input).encode("utf-8")).decode("ascii")
    command = [godot, "--headless", "--path", str(root), "--script", "res://" + HARNESS_REL.as_posix(), "--", encoded]
    try:
        completed = process_runner(command, cwd=str(root), text=True, capture_output=True, timeout=timeout, check=False)
    except Exception as exc:
        raise ExactSelectorPayloadError(f"Godot exact-selector payload probe invocation failed: {exc}") from exc
    stdout = str(getattr(completed, "stdout", "") or "")
    stderr = str(getattr(completed, "stderr", "") or "")
    combined = stdout + "\n" + stderr
    exit_code = int(getattr(completed, "returncode", -1))
    if exit_code != 0 or "SCRIPT ERROR:" in combined or "ERROR:" in combined or "EXACT SELECTOR PAYLOAD V2 PROBE FAIL" in combined:
        raise ExactSelectorPayloadError(f"Godot payload materialization probe failed (exit={exit_code}): {combined[-5000:]}")
    rows = [line[len(PROBE_PREFIX):] for line in combined.splitlines() if line.startswith(PROBE_PREFIX)]
    if len(rows) != 1:
        raise ExactSelectorPayloadError(f"Expected exactly one probe receipt; got {len(rows)}")
    try:
        report = json.loads(rows[0])
    except json.JSONDecodeError as exc:
        raise ExactSelectorPayloadError("Godot payload probe receipt is invalid JSON") from exc
    return _validate_probe(report, probe_input, contract)

def build_report(project_root: str | Path | None = None, godot: str | None = None, timeout: float = 120, process_runner: Callable[..., Any] = subprocess.run) -> dict[str, Any]:
    root = _root(project_root)
    if not godot or not Path(godot).is_file():
        raise ExactSelectorPayloadError("An explicit Godot 4.7.1 console executable is required")
    contract, _schema, input_schema, report_schema, pins = _load_contract(root)
    contract["_validation_root"] = str(root)
    try:
        version = process_runner([godot, "--version"], cwd=str(root), text=True, capture_output=True, timeout=min(timeout, 30), check=False)
    except Exception as exc:
        raise ExactSelectorPayloadError(f"Cannot invoke pinned Godot console executable: {exc}") from exc
    version_text = (str(getattr(version, "stdout", "") or "") + "\n" + str(getattr(version, "stderr", "") or "")).strip()
    if int(getattr(version, "returncode", -1)) != 0 or EXPECTED_GODOT_VERSION not in version_text:
        raise ExactSelectorPayloadError(f"Expected Godot {EXPECTED_GODOT_VERSION}, got {version_text!r}")

    parent_binding = _load_module(root / PARAMETER_BINDING_REL, "_c11d_exact_selector_payload_parent_binding_v2")
    parent_report = parent_binding.build_report(root, godot, timeout, process_runner)
    parent_summary = parent_report.get("summary", {})
    if (
        parent_summary.get("request_plans") != "5/5" or
        parent_summary.get("request_parameter_bindings") != "5/5" or
        parent_summary.get("selected_grammar_parameter_instances_bound") != "5/5" or
        parent_summary.get("selected_grammar_payload_instances_bound") != "0/5" or
        parent_summary.get("approvals_granted") != 0 or
        parent_summary.get("candidate_input_admissible") is not False
    ):
        raise ExactSelectorPayloadError("Parent V2 parameter matrix did not pass in its fixed preparation-only scope")

    cases = []
    seen_payload_hashes: set[str] = set()
    for row in parent_report["cases"]:
        probe_input = {
            "schema": INPUT_SCHEMA,
            "schema_version": "2.0",
            "contract_sha256": file_sha(root / CONTRACT_REL),
            "frozen_c11c_manifest_sha256": EXPECTED_MANIFEST,
            "parent_binding_report_sha256": parent_report["report_sha256"],
            "request_identity": copy.deepcopy(row["request_identity"]),
            "canonical_chain": copy.deepcopy(row["canonical_chain"]),
            "timing_review_reference": copy.deepcopy(row["timing_review_reference"]),
            "request_parameter_binding_sha256": row["request_parameter_binding_sha256"],
            "parameter_instance": copy.deepcopy(row["parameter_instance"]),
        }
        probe = _run_probe(root, godot, timeout, contract, input_schema, probe_input, process_runner)
        if probe["payload_instance_sha256"] in seen_payload_hashes:
            raise ExactSelectorPayloadError("Distinct canonical selectors produced duplicate payload-instance hashes")
        seen_payload_hashes.add(probe["payload_instance_sha256"])
        cases.append({
            "request_identity": probe["request_identity"],
            "canonical_chain": probe["canonical_chain"],
            "timing_review_reference": probe["timing_review_reference"],
            "request_parameter_binding_sha256": probe["parent_request_parameter_binding_sha256"],
            "parameter_instance_sha256": probe["parameter_instance_sha256"],
            "grammar_id": probe["grammar_id"],
            "grammar_index": probe["grammar_index"],
            "shader_branch_review_only": probe["shader_branch_review_only"],
            "authoring_envelope_sha256": probe["authoring_envelope_sha256"],
            "family_variation_recipe_sha256": probe["family_variation_recipe_sha256"],
            "resolved_palette_sha256": probe["resolved_palette_sha256"],
            "visual_spec_sha256": probe["visual_spec_sha256"],
            "payload_instance_sha256": probe["payload_instance_sha256"],
            "payload_materialized_in_memory": True,
            "deterministic_repeat_pass": True,
            "exact_selector_visual_payload_materialized": True,
            "renderer_input_emitted": False,
            "policy_values_consumed": False,
        })
    if len(cases) != 5 or tuple((x["grammar_id"], x["grammar_index"], x["shader_branch_review_only"]) for x in cases) != GRAMMARS:
        raise ExactSelectorPayloadError("Five exact selectors are not materialized in canonical order")
    if len({x["request_identity"]["request_hash"] for x in cases}) != 5 or len({x["canonical_chain"]["plan_hash"] for x in cases}) != 5:
        raise ExactSelectorPayloadError("Request and plan identities must remain unique across selectors")
    if len({x["payload_instance_sha256"] for x in cases}) != 5 or len({x["parameter_instance_sha256"] for x in cases}) != 5:
        raise ExactSelectorPayloadError("Payload and parameter instance identities must be unique across selectors")
    if len({x["timing_review_reference"]["shared_policy_reference_set_sha256"] for x in cases}) != 1 or len({x["timing_review_reference"]["selector_envelope_sha256"] for x in cases}) != 5:
        raise ExactSelectorPayloadError("Shared policy-set/selector envelope digest cardinality changed")
    if sum(x["timing_review_reference"]["policy_reference_count"] for x in cases) != 45 or any(x["policy_values_consumed"] for x in cases):
        raise ExactSelectorPayloadError("Expected 45 metadata-only policy references and zero policy-body consumption")

    report = {
        "schema": "C11-D-D9-VISUAL-LOOP-EXACT-SELECTOR-PAYLOAD-REPORT-V2",
        "schema_version": "2.0",
        "status": STATUS,
        "contract_sha256": file_sha(root / CONTRACT_REL),
        "input_schema_sha256": file_sha(root / INPUT_SCHEMA_REL),
        "report_schema_sha256": file_sha(root / REPORT_SCHEMA_REL),
        "source_lineage": pins,
        "source_lineage_sha256": digest(pins),
        "parent_parameter_binding_report_sha256": parent_report["report_sha256"],
        "parent_parameter_binding_contract_sha256": file_sha(root / PARAMETER_BINDING_CONTRACT_REL),
        "cases": cases,
        "summary": {
            "direct_source_pins": f"{len(pins)}/{len(pins)}",
            "request_plans": "5/5",
            "parameter_instances_bound": "5/5",
            "exact_selector_visual_payload_instances_materialized": "5/5",
            "distinct_payload_instance_hashes": "5/5",
            "deterministic_repeats": "5/5",
            "authoring_envelopes": "5/5",
            "shader_branch_selector_reviews": "5/5",
            "policy_reference_pairs": "45/45",
            "policy_values_consumed": False,
            "renderer_inputs_emitted": "0/5",
            "payload_files_written": False,
            "approval_assertions_checked": 19,
            "approvals_granted": 0,
            "candidate_input_admissible": False,
            "non_geometric_family_authoring_gaps_remain_open": True,
        },
        "governance": {
            "approval_assertions_checked": 19,
            "approvals_granted": 0,
            "pending_approval_assertions": 19,
            "exact_selector_payload_v2_approved": False,
            "grammar_parameter_binding_v2_approved": False,
            "visual_loop_binding_matrix_v2_approved": False,
            "canonical_request_selector_matrix_approved": False,
            "timing_review_inheritance_approved": False,
            "all_nine_shared_policy_sources_approved": False,
            "candidate_io_contract_complete": False,
            "renderer_baseline_approved": False,
            "renderer_baseline_frozen": False,
            "d4_8_authorized": False,
            "request_input_persisted": False,
            "payload_file_written": False,
            "receipt_file_written": False,
            "renderer_native_input_emitted": False,
            "renderer_dispatch_invoked": False,
            "shader_executed": False,
            "media_created": False,
            "c11c_source_mutation": False,
            "candidate_input_admissible": False,
            "renderer": "OFF",
            "D4.8": "BLOCKED",
            "D9.10": "PREPARE_ONLY",
            "D9.17": "BLOCKED_NO_GO",
            "D10": "BLOCKED",
            "release_authority": "NONE",
        },
        "execution_boundary": BOUNDARY,
    }
    report["report_sha256"] = digest(report)
    try:
        Draft202012Validator(report_schema).validate(report)
    except Exception as exc:
        raise ExactSelectorPayloadError(f"Report schema rejected the final report: {getattr(exc, 'message', str(exc))}") from exc
    if digest({key: value for key, value in report.items() if key != "report_sha256"}) != report["report_sha256"]:
        raise ExactSelectorPayloadError("Audit report self-hash mismatch")
    return report

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True)
    parser.add_argument("--godot", required=True)
    parser.add_argument("--timeout", type=float, default=120)
    parser.add_argument("--full-report", action="store_true")
    args = parser.parse_args(argv)
    try:
        report = build_report(args.root, args.godot, args.timeout)
        s = report["summary"]
        print("C11-D VISUAL LOOP EXACT SELECTOR PAYLOAD V2 AUDIT PASS | direct_source_pins=" + s["direct_source_pins"] + " | request_plans=" + s["request_plans"] + " | parameter_instances_bound=" + s["parameter_instances_bound"] + " | exact_selector_visual_payload_instances_materialized=" + s["exact_selector_visual_payload_instances_materialized"] + " | distinct_payload_instance_hashes=" + s["distinct_payload_instance_hashes"] + " | deterministic_repeats=" + s["deterministic_repeats"] + " | authoring_envelopes=" + s["authoring_envelopes"] + " | shader_branch_selector_reviews=" + s["shader_branch_selector_reviews"] + " | policy_reference_pairs=" + s["policy_reference_pairs"] + " | policy_values_consumed=false | renderer_inputs_emitted=" + s["renderer_inputs_emitted"] + " | payload_files_written=false | approval_assertions_checked=19 | approvals_granted=0 | candidate_input_admissible=false | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
        print(REPORT_PREFIX + canonical(report))
        if args.full_report:
            print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except Exception as exc:
        print("C11-D VISUAL LOOP EXACT SELECTOR PAYLOAD V2 AUDIT FAIL | " + str(exc) + " | payload_materialized_in_memory=not_confirmed | candidate_input_admissible=false | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
