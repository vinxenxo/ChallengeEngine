"""D9.9 dynamic request -> bounded in-memory payload binding; no renderer dispatch."""
from __future__ import annotations

import argparse
import ast
import base64
import copy
import hashlib
import json
import os
import re
import subprocess
import sys
from collections.abc import Mapping, Callable
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from universal_producer import REQUEST_SCHEMA_ID, evaluate_universal_request
from editorial_render_bridge import build_bridge_planning_record
from d_render_adapter import prepare_d_only_adapter_envelope
from d_renderer_request_scoped_payload_binding import (
    build_request_scoped_payload_binding,
    validate_request_scoped_payload_binding,
)

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_DYNAMIC_REQUEST_PAYLOAD_BINDING_V1.json")
INPUT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_DYNAMIC_REQUEST_PAYLOAD_INPUT_SCHEMA_V1.json")
OUTPUT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_DYNAMIC_REQUEST_PAYLOAD_BINDING_SCHEMA_V1.json")
DRILL_V2_CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_DYNAMIC_REQUEST_PAYLOAD_BINDING_V2.json")
DRILL_V2_INPUT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_DYNAMIC_REQUEST_PAYLOAD_INPUT_SCHEMA_V2.json")
DRILL_V2_OUTPUT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_DYNAMIC_REQUEST_PAYLOAD_BINDING_SCHEMA_V2.json")
MANIFEST_REL = Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")
CONTRACT_ID = "C11-D-RENDERER-DYNAMIC-REQUEST-PAYLOAD-BINDING-CONTRACT-V1"
INPUT_SCHEMA_ID = "C11-D-D9-DYNAMIC-REQUEST-PAYLOAD-INPUT-V1"
OUTPUT_SCHEMA_ID = "C11-D-D9-DYNAMIC-REQUEST-PAYLOAD-BINDING-V1"
PAYLOAD_MANIFEST_SCHEMA_ID = "C11-D-D9-REQUEST-PAYLOAD-MANIFEST-V1"
PAYLOAD_MANIFEST_STATUS = "PREPARATION_ONLY_REQUEST_BOUND_PAYLOAD_MANIFEST_NOT_RENDERER_INPUT"
GODOT_SUMMARY_SCHEMA_ID = "C11-D-D9-DYNAMIC-REQUEST-PAYLOAD-MATERIALIZATION-V1"
DRILL_V2_CONTRACT_ID = "C11-D-RENDERER-DYNAMIC-REQUEST-PAYLOAD-BINDING-CONTRACT-V2"
DRILL_V2_INPUT_SCHEMA_ID = "C11-D-D9-DYNAMIC-REQUEST-PAYLOAD-INPUT-V2"
DRILL_V2_OUTPUT_SCHEMA_ID = "C11-D-D9-VISUAL-DRILL-DYNAMIC-REQUEST-PAYLOAD-BINDING-V2"
DRILL_V2_PAYLOAD_MANIFEST_SCHEMA_ID = "C11-D-D9-VISUAL-DRILL-REQUEST-PAYLOAD-MANIFEST-V2"
DRILL_V2_PAYLOAD_MANIFEST_STATUS = "PREPARATION_ONLY_VISUAL_DRILL_REQUEST_BOUND_PAYLOAD_MANIFEST_NOT_RENDERER_INPUT"
DRILL_V2_GODOT_SUMMARY_SCHEMA_ID = "C11-D-D9-VISUAL-DRILL-REQUEST-PAYLOAD-MATERIALIZATION-V2"
DRILL_V2_STATUS = "PREPARATION_ONLY_VISUAL_DRILL_DYNAMIC_REQUEST_BOUND_PAYLOAD_REVIEW_NOT_RENDERER_INPUT"
DRILL_V2_PAYLOAD_SCOPE = "VISUAL_DRILL_REQUEST_SELECTOR_TIER_PAYLOAD_V2"
DRILL_V2_FAMILIES = ("peripheral_scan", "pursuit", "saccade", "tracking")
DRILL_V2_TIERS = ("tier-1", "tier-2", "tier-3", "tier-4", "tier-5")
DRILL_V2_COMMON_AUTHORING_PATHS = (
    "core/authoring/VisualAuthoringAssemblyContext.gd",
    "core/authoring/VisualAuthoringGenerator.gd",
    "core/authoring/VisualAuthoringPolicyRegistry.gd",
    "core/authoring/VisualAuthoringRegistry.gd",
    "core/authoring/VisualAuthoringRequest.gd",
    "core/authoring/VisualAuthoringRequestValidator.gd",
    "core/authoring/VisualDifficultyResolver.gd",
    "core/authoring/VisualDrillSeedVariation.gd",
    "core/authoring/adapters/VisualDrillAuthoringAdapter.gd",
)
DRILL_V2_STATIC_SOURCE_PATHS = (
    "definitions/c11d/production/D_RENDERER_VISUAL_DRILL_SELECTOR_AUTHORING_COVERAGE_V1.json",
    "definitions/c11d/production/D_RENDERER_VISUAL_DRILL_SELECTOR_AUTHORING_COVERAGE_SCHEMA_V1.json",
)
DRILL_V2_RECEIPT_PREFIX = "C11-D DYNAMIC REQUEST PAYLOAD RECEIPT VERIFIED="
STATUS = "PREPARATION_ONLY_DYNAMIC_REQUEST_BOUND_PAYLOAD_REVIEW_NOT_RENDERER_INPUT"
EXPECTED_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
GODOT_HARNESS_REL = Path("tools/c11d/d9/materialize_dynamic_request_payload_in_memory.gd")
GODOT_SUMMARY_PREFIX = "C11-D DYNAMIC REQUEST PAYLOAD MATERIALIZATION SUMMARY="
ERROR_MARKERS = ("SCRIPT ERROR:", "ERROR:", "DYNAMIC REQUEST PAYLOAD MATERIALIZATION FAIL")
SUPPORTED_TYPES = ("challenges", "visual_loops", "visual_drills")
ALLOWED_DELIVERY_PROFILES = ("REVIEW_720", "MIN_540", "MASTER_1080", "META_REELS_FINAL_V1")
EXPECTED_SELECTIONS: dict[str, dict[str, Any]] = {
    "challenges": {"content_type": "challenges", "family_id": "parking_v2", "subtype_id": None, "variant_id": "CHALLENGE_004"},
    "visual_loops": {"content_type": "visual_loops", "family_id": "c11c_geometric_waves_v1", "subtype_id": "harmonic_membrane", "variant_id": None},
    "visual_drills": {"content_type": "visual_drills", "family_id": "tracking", "subtype_id": None, "variant_id": "tier-2"},
}
EXPECTED_SCOPE: dict[str, tuple[str, bool]] = {
    "challenges": ("CHALLENGE_RUNTIME_VISUAL_PAYLOAD_SOURCE_TIMEBASE", True),
    "visual_loops": ("VISUAL_LOOP_SELECTOR_PAYLOAD_HARMONIC_MEMBRANE_V1", True),
    "visual_drills": ("VISUAL_DRILL_TIER_SEED_PAYLOAD", True),
}
EXPECTED_GRAMMAR_COMPOSITION = {
    "status": "PREPARATION_ONLY_COMPOSITE_PAYLOAD_MATERIALIZED_IN_MEMORY",
    "selection": {"content_type": "visual_loops", "family_id": "c11c_geometric_waves_v1", "subtype_id": "harmonic_membrane", "variant_id": None},
    "payload_member_path": "grammar_parameter_instance",
    "grammar_id": "harmonic_membrane",
    "grammar_index": 0,
    "shader_branch": "field_harmonic_membrane",
    "shader_uniform": "grammar_mode",
    "style_parameter_count": 20,
    "profile_input_aliases": {"glow": "glow_strength"},
    "family_authoring_envelope_subtype": "geometric",
    "family_authoring_adapter_itself_grammar_aware": False,
    "only_pinned_selector_admitted": True,
    "other_visual_loop_grammars": "REJECTED_BY_CANONICAL_REQUEST_SELECTOR_MATRIX",
    "renderer_native_input_emitted": False,
    "renderer_created": False,
    "shader_executed": False,
    "media_created": False,
}
EXPECTED_BOUNDARY = {
    "mode": "GODOT_HEADLESS_IN_MEMORY_DYNAMIC_REQUEST_REVIEW_ONLY",
    "request_input_persisted": False,
    "payload_files_written": False,
    "receipt_files_written": False,
    "renderer_native_input_emitted": False,
    "renderer_dispatch_invoked": False,
    "renderer_activation": False,
    "production_execution": False,
    "media_output_created": False,
    "output_artifact_path": None,
    "c11c_source_mutation": False,
    "d4_8": "BLOCKED",
    "release_authority": "NONE",
    "d9_14": "BLOCKED_AS_REQUIRED",
    "d9_16": "BLOCKED_AS_REQUIRED",
    "d9_17": "BLOCKED_NO_GO",
    "d10": "BLOCKED",
}
EXPECTED_SEMANTIC_LIMITS = {
    "music_seed_in_visual_payload": False,
    "variation_index_semantics": "METADATA_ONLY_NOT_A_VISUAL_VARIANT_SELECTOR",
    "delivery_profile_semantics": "IDENTITY_ONLY_PROJECTION_NOT_APPLIED",
    "presentation_geometry": "UNRESOLVED_NOT_APPLIED",
    "editorial_visual_consumption": "NOT_APPLIED",
    "simulation_telemetry_included": False,
    "winning_frame_used_as_timing": False,
    "close_calls_used_as_timing": False,
}


class DynamicRequestPayloadBindingError(ValueError):
    """Raised on source drift, invalid selector identity, false materialization or policy promotion."""


def _root(project_root: Path | str | None = None) -> Path:
    return Path(project_root).resolve() if project_root is not None else Path(__file__).resolve().parents[3]


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _sha_json(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha_file(path: Path) -> str:
    try:
        return _sha_bytes(path.read_bytes())
    except OSError as exc:
        raise DynamicRequestPayloadBindingError(f"Cannot hash required source {path}: {exc}") from exc


def _read_json(root: Path, rel: str | Path) -> dict[str, Any]:
    try:
        value = json.loads((root / rel).read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise DynamicRequestPayloadBindingError(f"Cannot read required JSON {rel}: {exc}") from exc
    if not isinstance(value, dict):
        raise DynamicRequestPayloadBindingError(f"Expected JSON object at {rel}")
    return value


def _is_sha(value: Any) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def _load_contract(root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[dict[str, str]]]:
    contract = _read_json(root, CONTRACT_REL)
    input_schema = _read_json(root, INPUT_SCHEMA_REL)
    output_schema = _read_json(root, OUTPUT_SCHEMA_REL)
    if contract.get("schema") != CONTRACT_ID or contract.get("schema_version") != "1.0":
        raise DynamicRequestPayloadBindingError("Dynamic request contract identity/version mismatch")
    if contract.get("status") != "PREPARATION_ONLY_DYNAMIC_REQUEST_BOUND_IN_MEMORY_PAYLOAD_REVIEW_NOT_RENDERER_INPUT":
        raise DynamicRequestPayloadBindingError("Dynamic request contract cannot self-promote")
    if contract.get("candidate_input_admissible") is not False:
        raise DynamicRequestPayloadBindingError("Candidate input must remain inadmissible")
    if contract.get("source_of_truth", {}).get("frozen_c11c_manifest_sha256") != EXPECTED_MANIFEST_SHA256 or _sha_file(root / MANIFEST_REL) != EXPECTED_MANIFEST_SHA256:
        raise DynamicRequestPayloadBindingError("Frozen C11-C manifest mismatch")
    if input_schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or input_schema.get("$id") != "urn:c11d:renderer-dynamic-request-payload-input:v1" or input_schema.get("additionalProperties") is not False:
        raise DynamicRequestPayloadBindingError("Dynamic request input schema identity/strictness mismatch")
    if output_schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or output_schema.get("$id") != "urn:c11d:renderer-dynamic-request-payload-binding:v1" or output_schema.get("additionalProperties") is not False:
        raise DynamicRequestPayloadBindingError("Dynamic payload binding output schema identity/strictness mismatch")
    if set(output_schema.get("required", [])) != set(output_schema.get("properties", {})):
        raise DynamicRequestPayloadBindingError("Output schema top-level required/properties mismatch")
    if contract.get("supported_content_types") != list(SUPPORTED_TYPES):
        raise DynamicRequestPayloadBindingError("Supported content-type scope changed")
    expected_matrix = {
        key: {"selection": EXPECTED_SELECTIONS[key], "payload_scope": EXPECTED_SCOPE[key][0], "exact_selector_payload_materialized": EXPECTED_SCOPE[key][1]}
        for key in SUPPORTED_TYPES
    }
    if contract.get("supported_selector_matrix") != expected_matrix:
        raise DynamicRequestPayloadBindingError("Pinned selector matrix or per-content materialization status drifted")
    if contract.get("visual_loop_grammar_composition") != EXPECTED_GRAMMAR_COMPOSITION:
        raise DynamicRequestPayloadBindingError("Pinned Visual Loop composite grammar contract drifted")
    if contract.get("execution_boundary") != EXPECTED_BOUNDARY:
        raise DynamicRequestPayloadBindingError("Execution/governance boundary drifted")
    expected_approval = {
        "dynamic_request_contract_approved": False,
        "payload_instances_approved": False,
        "visual_loop_grammar_instance_approved": False,
        "editorial_visual_consumption_approved": False,
        "presentation_geometry_approved": False,
        "temporal_alignment_approved": False,
        "renderer_baseline_approved": False,
        "renderer_baseline_frozen": False,
        "d4_8_authorized": False,
        "d9_14_full_acceptance": "BLOCKED_AS_REQUIRED",
        "d9_16_full_acceptance": "BLOCKED_AS_REQUIRED",
        "d9_17_closure": "BLOCKED_NO_GO",
        "d10": "BLOCKED",
        "release_authority": "NONE",
    }
    if contract.get("approval_state") != expected_approval:
        raise DynamicRequestPayloadBindingError("Contract may not approve payloads, policy, baseline or release")
    harness_info = contract.get("harness", {})
    if harness_info.get("path") != GODOT_HARNESS_REL.as_posix() or not _is_sha(harness_info.get("sha256")):
        raise DynamicRequestPayloadBindingError("Dynamic Godot harness identity malformed")
    if _sha_file(root / GODOT_HARNESS_REL) != harness_info["sha256"]:
        raise DynamicRequestPayloadBindingError("Dynamic Godot harness hash mismatch")
    raw_lineage = contract.get("source_lineage")
    if not isinstance(raw_lineage, list) or len(raw_lineage) < 30:
        raise DynamicRequestPayloadBindingError("Source lineage is incomplete")
    lineage: list[dict[str, str]] = []
    seen: set[str] = set()
    for row in raw_lineage:
        if not isinstance(row, Mapping) or set(row) != {"path", "sha256"}:
            raise DynamicRequestPayloadBindingError("Malformed source-lineage row")
        rel, expected_hash = str(row["path"]), str(row["sha256"])
        path = Path(rel)
        if path.is_absolute() or ".." in path.parts or rel in seen or not _is_sha(expected_hash):
            raise DynamicRequestPayloadBindingError(f"Unsafe/duplicate source pin: {rel}")
        actual = _sha_file(root / path)
        if actual != expected_hash:
            raise DynamicRequestPayloadBindingError(f"Pinned source drift: {rel}")
        seen.add(rel)
        lineage.append({"path": path.as_posix(), "sha256": actual})
    if not lineage or lineage[0] != {"path": MANIFEST_REL.as_posix(), "sha256": EXPECTED_MANIFEST_SHA256}:
        raise DynamicRequestPayloadBindingError("Frozen C11-C manifest must be first source pin")
    return contract, input_schema, output_schema, lineage


def _load_visual_drill_v2_contract(root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[dict[str, str]]]:
    """Load the additive Visual Drill selector/tier contract; source drift fails closed."""
    # Validate the original contract first. V2 is an extension, never a replacement for V1.
    base_contract, _, _, base_lineage = _load_contract(root)
    contract = _read_json(root, DRILL_V2_CONTRACT_REL)
    input_schema = _read_json(root, DRILL_V2_INPUT_SCHEMA_REL)
    output_schema = _read_json(root, DRILL_V2_OUTPUT_SCHEMA_REL)
    if contract.get("schema") != DRILL_V2_CONTRACT_ID or contract.get("schema_version") != "2.0":
        raise DynamicRequestPayloadBindingError("Visual Drill V2 contract identity/version mismatch")
    if contract.get("status") != DRILL_V2_STATUS or contract.get("candidate_input_admissible") is not False:
        raise DynamicRequestPayloadBindingError("Visual Drill V2 contract attempted policy/candidate promotion")
    if contract.get("extension_of") != {
        "contract_path": CONTRACT_REL.as_posix(),
        "schema": CONTRACT_ID,
        "compatibility": "V1 Challenge and harmonic_membrane Loop matrix remains unchanged; same Python binder and canonical request chain.",
    }:
        raise DynamicRequestPayloadBindingError("Visual Drill V2 is not bound to the exact V1 dynamic binder contract")
    if contract.get("source_of_truth", {}).get("frozen_c11c_manifest_sha256") != EXPECTED_MANIFEST_SHA256 or _sha_file(root / MANIFEST_REL) != EXPECTED_MANIFEST_SHA256:
        raise DynamicRequestPayloadBindingError("Visual Drill V2 frozen C11-C manifest mismatch")
    expected_matrix = {
        "content_type": "visual_drills",
        "family_ids": list(DRILL_V2_FAMILIES),
        "tiers": [1, 2, 3, 4, 5],
        "expected_selector_count": 20,
        "authoring_domain_family": "visual_drill",
        "payload_scope": DRILL_V2_PAYLOAD_SCOPE,
        "exact_selector_payload_materialized": True,
    }
    if contract.get("supported_content_types") != ["visual_drills"] or contract.get("supported_selector_matrix") != expected_matrix:
        raise DynamicRequestPayloadBindingError("Visual Drill V2 canonical selector matrix drifted")
    if contract.get("execution_boundary") != EXPECTED_BOUNDARY or contract.get("approval_state") != base_contract.get("approval_state"):
        raise DynamicRequestPayloadBindingError("Visual Drill V2 contract attempted to relax existing governance locks")
    schemas = contract.get("schemas")
    expected_schema_meta = {
        "input": {"path": DRILL_V2_INPUT_SCHEMA_REL.as_posix(), "id": "urn:c11d:renderer-dynamic-request-payload-input:v2"},
        "output": {"path": DRILL_V2_OUTPUT_SCHEMA_REL.as_posix(), "id": "urn:c11d:renderer-dynamic-request-payload-binding:v2"},
    }
    if not isinstance(schemas, Mapping):
        raise DynamicRequestPayloadBindingError("Visual Drill V2 schema pins are missing")
    for key, expected_meta in expected_schema_meta.items():
        entry = schemas.get(key)
        if not isinstance(entry, Mapping) or entry.get("path") != expected_meta["path"] or entry.get("id") != expected_meta["id"] or not _is_sha(entry.get("sha256")):
            raise DynamicRequestPayloadBindingError(f"Malformed Visual Drill V2 {key} schema pin")
        schema_path = root / str(entry["path"])
        if _sha_file(schema_path) != entry["sha256"]:
            raise DynamicRequestPayloadBindingError(f"Visual Drill V2 {key} schema hash mismatch")
    if input_schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or input_schema.get("$id") != expected_schema_meta["input"]["id"] or input_schema.get("additionalProperties") is not False:
        raise DynamicRequestPayloadBindingError("Visual Drill V2 input schema identity/strictness mismatch")
    if output_schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or output_schema.get("$id") != expected_schema_meta["output"]["id"] or output_schema.get("additionalProperties") is not False:
        raise DynamicRequestPayloadBindingError("Visual Drill V2 output schema identity/strictness mismatch")
    if set(output_schema.get("required", [])) != set(output_schema.get("properties", {})):
        raise DynamicRequestPayloadBindingError("Visual Drill V2 output schema top-level required/properties mismatch")
    try:
        import jsonschema  # type: ignore
        jsonschema.Draft202012Validator.check_schema(input_schema)
        jsonschema.Draft202012Validator.check_schema(output_schema)
    except ImportError:
        pass
    except Exception as exc:
        raise DynamicRequestPayloadBindingError(f"Visual Drill V2 schema is invalid: {exc}") from exc
    harness = contract.get("harness", {})
    harness_rel = Path("tools/c11d/d9/materialize_visual_drill_dynamic_request_payload_in_memory_v2.gd")
    if harness.get("path") != harness_rel.as_posix() or not _is_sha(harness.get("sha256")) or _sha_file(root / harness_rel) != harness.get("sha256"):
        raise DynamicRequestPayloadBindingError("Visual Drill V2 Godot harness identity/hash mismatch")
    rows = contract.get("source_lineage")
    if not isinstance(rows, list) or len(rows) < 60:
        raise DynamicRequestPayloadBindingError("Visual Drill V2 source lineage is incomplete")
    seen: set[str] = set()
    lineage: list[dict[str, str]] = []
    for index, row in enumerate(rows):
        if not isinstance(row, Mapping) or set(row) != {"path", "sha256"}:
            raise DynamicRequestPayloadBindingError("Malformed Visual Drill V2 source-lineage row")
        rel, expected_hash = str(row["path"]), str(row["sha256"])
        path = Path(rel)
        if path.is_absolute() or ".." in path.parts or rel in seen or not _is_sha(expected_hash):
            raise DynamicRequestPayloadBindingError(f"Unsafe/duplicate Visual Drill V2 source pin: {rel}")
        actual = _sha_file(root / path)
        if actual != expected_hash:
            raise DynamicRequestPayloadBindingError(f"Visual Drill V2 pinned source drift: {rel}")
        if index == 0 and (rel != MANIFEST_REL.as_posix() or expected_hash != EXPECTED_MANIFEST_SHA256):
            raise DynamicRequestPayloadBindingError("Frozen C11-C manifest must be first V2 source pin")
        if index > 1 and rel <= lineage[-1]["path"]:
            raise DynamicRequestPayloadBindingError("Visual Drill V2 source pins must be lexicographically sorted after frozen manifest")
        seen.add(rel)
        lineage.append({"path": path.as_posix(), "sha256": actual})
    coverage_contract = _read_json(root, "definitions/c11d/production/D_RENDERER_VISUAL_DRILL_SELECTOR_AUTHORING_COVERAGE_V1.json")
    expected_paths = {row["path"] for row in base_contract["source_lineage"]}
    expected_paths.update(row["path"] for row in coverage_contract["source_lineage"])
    expected_paths.update({
        "definitions/c11d/production/D_RENDERER_VISUAL_DRILL_SELECTOR_AUTHORING_COVERAGE_V1.json",
        DRILL_V2_CONTRACT_REL.as_posix(),
        DRILL_V2_INPUT_SCHEMA_REL.as_posix(),
        DRILL_V2_OUTPUT_SCHEMA_REL.as_posix(),
        harness_rel.as_posix(),
    })
    # The V2 harness consumes this full common authoring dependency set. Ensure
    # every selected source is also explicitly hash-bound in the V2 contract.
    expected_paths.update(DRILL_V2_COMMON_AUTHORING_PATHS)
    # The contract itself cannot pin its own bytes; remove it from the expected source set.
    expected_paths.discard(DRILL_V2_CONTRACT_REL.as_posix())
    if seen != expected_paths:
        raise DynamicRequestPayloadBindingError(f"Visual Drill V2 source-lineage closure mismatch; missing={sorted(expected_paths-seen)}; extra={sorted(seen-expected_paths)}")
    authoring_evidence = contract.get("source_of_truth", {})
    coverage_rel = Path("definitions/c11d/production/D_RENDERER_VISUAL_DRILL_SELECTOR_AUTHORING_COVERAGE_V1.json")
    if authoring_evidence.get("authoring_coverage_contract_path") != coverage_rel.as_posix() or authoring_evidence.get("authoring_coverage_contract_sha256") != _sha_file(root / coverage_rel) or authoring_evidence.get("authoring_adapter_audit_does_not_imply_request_manifest_acceptance") is not True:
        raise DynamicRequestPayloadBindingError("Visual Drill V2 authoring evidence linkage is invalid")
    manifest_info = contract.get("request_payload_manifest", {})
    if manifest_info != {
        "schema": DRILL_V2_PAYLOAD_MANIFEST_SCHEMA_ID,
        "schema_version": "2.0",
        "status": DRILL_V2_PAYLOAD_MANIFEST_STATUS,
        "includes_selected_canonical_definition_and_difficulty_policy": True,
        "includes_full_dynamic_binder_lineage": True,
        "includes_selected_authoring_dependency_lineage": True,
        "includes_independent_runtime_repeat_evidence": True,
    }:
        raise DynamicRequestPayloadBindingError("Visual Drill V2 request manifest contract drifted")
    return contract, input_schema, output_schema, lineage


def _load_contract_for_mode(root: Path, mode: str = "v1") -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[dict[str, str]]]:
    if mode == "visual_drill_v2":
        return _load_visual_drill_v2_contract(root)
    if mode != "v1":
        raise DynamicRequestPayloadBindingError(f"Unsupported binder mode: {mode}")
    return _load_contract(root)


def _is_visual_drill_v2_contract(contract: Mapping[str, Any]) -> bool:
    return contract.get("schema") == DRILL_V2_CONTRACT_ID and contract.get("schema_version") == "2.0"


def _base_request(selection: Mapping[str, Any], request_id: str) -> dict[str, Any]:
    override: dict[str, str] = {
        "title": "Prueba editorial · título",
        "subtitle": "Subtítulo de revisión",
        "call_to_action": "Continuar",
        "language": "es",
    }
    if selection.get("content_type") == "challenges":
        override.update({"player_name": "ANA", "challenge_label": "RETO"})
    return {
        "schema": REQUEST_SCHEMA_ID,
        "schema_version": "1.0",
        "request_id": request_id,
        "mode": "REVIEW",
        "selection": copy.deepcopy(dict(selection)),
        "seed": 12345,
        "music_seed": 840001,
        "delivery_profile_id": "REVIEW_720",
        "presentation_profile_id": "social_default_v1",
        "variation_index": 0,
        "audio_enabled": True,
        "personalization_enabled": True,
        "editorial_profile": {},
        "production_override": override,
        "provenance": {"source_revision": "C11D-D9.9-DYNAMIC-REQUEST-V1", "request_origin": "TEST"},
    }


def _matrix_raw_requests() -> list[dict[str, Any]]:
    requests: list[dict[str, Any]] = []
    bases: dict[str, dict[str, Any]] = {}
    for content_type in SUPPORTED_TYPES:
        raw = _base_request(EXPECTED_SELECTIONS[content_type], f"D-DYNAMIC-{content_type.upper()}-BASE")
        bases[content_type] = raw
        requests.append(copy.deepcopy(raw))
        changed_seed = copy.deepcopy(raw)
        changed_seed["request_id"] = f"D-DYNAMIC-{content_type.upper()}-SEED-CHANGE"
        changed_seed["seed"] = 54321
        requests.append(changed_seed)
    loop_base = bases["visual_loops"]
    music_only = copy.deepcopy(loop_base)
    music_only["request_id"] = "D-DYNAMIC-VISUAL_LOOPS-MUSIC-ONLY"
    music_only["music_seed"] = 840002
    requests.append(music_only)
    variation_only = copy.deepcopy(loop_base)
    variation_only["request_id"] = "D-DYNAMIC-VISUAL_LOOPS-VARIATION-ONLY"
    variation_only["variation_index"] = 17
    requests.append(variation_only)
    delivery_only = copy.deepcopy(loop_base)
    delivery_only["request_id"] = "D-DYNAMIC-VISUAL_LOOPS-DELIVERY-ONLY"
    delivery_only["delivery_profile_id"] = "MASTER_1080"
    requests.append(delivery_only)
    editorial_only = copy.deepcopy(loop_base)
    editorial_only["request_id"] = "D-DYNAMIC-VISUAL_LOOPS-EDITORIAL-ONLY"
    editorial_only["production_override"]["title"] = "Título editorial alternativo"
    requests.append(editorial_only)
    return requests


def _canonical_selection(plan_selection: Mapping[str, Any]) -> dict[str, Any]:
    return {key: plan_selection.get(key) for key in ("content_type", "family_id", "subtype_id", "variant_id")}


def _is_allowed_visual_drill_selection(selection: Mapping[str, Any]) -> bool:
    return (
        selection.get("content_type") == "visual_drills"
        and selection.get("family_id") in DRILL_V2_FAMILIES
        and selection.get("subtype_id") is None
        and selection.get("variant_id") in DRILL_V2_TIERS
    )


def _visual_drill_matrix_raw_requests() -> list[dict[str, Any]]:
    requests: list[dict[str, Any]] = []
    for family in DRILL_V2_FAMILIES:
        for tier in DRILL_V2_TIERS:
            selection = {"content_type": "visual_drills", "family_id": family, "subtype_id": None, "variant_id": tier}
            request_id = f"D-DYNAMIC-VISUAL-DRILLS-{family.upper()}-{tier.upper()}"
            requests.append(_base_request(selection, request_id))
    return requests


def _build_canonical_chain(raw: Mapping[str, Any], root: Path, allow_visual_drill_matrix: bool = False) -> dict[str, Any]:
    # Validate the caller's selector before D9.9 normalization. Without this
    # preflight, aliases/defaulting in the canonical request planner could turn
    # an unknown family or tier into a valid-looking selection downstream.
    if allow_visual_drill_matrix:
        raw_selection = raw.get("selection")
        if not isinstance(raw_selection, Mapping):
            raise DynamicRequestPayloadBindingError("Visual Drill V2 request requires an explicit selection object")
        required_selection_fields = {"content_type", "family_id", "subtype_id", "variant_id"}
        if set(raw_selection.keys()) != required_selection_fields:
            raise DynamicRequestPayloadBindingError("Visual Drill V2 selection fields must exactly match the pinned schema")
        if not _is_allowed_visual_drill_selection(raw_selection):
            raise DynamicRequestPayloadBindingError("Visual Drill V2 selector/tier must be an exact member of the pinned 20-pair matrix")
    try:
        result = evaluate_universal_request(dict(raw), root)
        bridge = build_bridge_planning_record(result, root)
        envelope = prepare_d_only_adapter_envelope(result, bridge, root)
        source_binding = build_request_scoped_payload_binding(result, bridge, envelope, root, allow_visual_drill_matrix=allow_visual_drill_matrix)
        validate_request_scoped_payload_binding(source_binding, result, bridge, envelope, root, allow_visual_drill_matrix=allow_visual_drill_matrix)
    except Exception as exc:
        raise DynamicRequestPayloadBindingError(f"Canonical D9.9/D9.10/source-binding chain rejected request: {exc}") from exc
    if result.get("status") != "PLANNED":
        raise DynamicRequestPayloadBindingError("Canonical universal request did not produce PLANNED status")
    content_type = str(result.get("plan", {}).get("selection", {}).get("content_type", ""))
    canonical_selection = _canonical_selection(result["plan"]["selection"])
    if content_type == "visual_drills" and allow_visual_drill_matrix:
        if not _is_allowed_visual_drill_selection(canonical_selection):
            raise DynamicRequestPayloadBindingError("Visual Drill selector/tier is outside the exact V2 family × tier matrix")
    elif content_type not in EXPECTED_SELECTIONS or canonical_selection != EXPECTED_SELECTIONS[content_type]:
        raise DynamicRequestPayloadBindingError("Selector is outside the pinned request-to-payload matrix")
    request = result.get("canonical_request", {})
    if request.get("presentation_profile_id") != "social_default_v1":
        raise DynamicRequestPayloadBindingError("V1 admits only social_default_v1 presentation identity")
    if request.get("delivery_profile_id") not in ALLOWED_DELIVERY_PROFILES:
        raise DynamicRequestPayloadBindingError("V1 rejects Longform or non-admitted delivery profile identity")
    if request.get("seed") != int(raw.get("seed", -1)) or request.get("music_seed") != int(raw.get("music_seed", -1)):
        raise DynamicRequestPayloadBindingError("Canonical request changed a declared seed domain")
    return {"raw": dict(raw), "result": result, "bridge": bridge, "envelope": envelope, "source_binding": source_binding}


def _godot_input(chain: Mapping[str, Any], contract: Mapping[str, Any] | None = None) -> dict[str, Any]:
    result = chain["result"]
    request = result["canonical_request"]
    v2 = bool(contract and _is_visual_drill_v2_contract(contract))
    data = {
        "schema": DRILL_V2_INPUT_SCHEMA_ID if v2 else INPUT_SCHEMA_ID,
        "schema_version": "2.0" if v2 else "1.0",
        "request_id": request["request_id"],
        "request_hash": result["request_hash"],
        "selection": _canonical_selection(result["plan"]["selection"]),
        "seed": request["seed"],
        "music_seed": request["music_seed"],
        "variation_index": request["variation_index"],
        "presentation_profile_id": request["presentation_profile_id"],
        "delivery_profile_id": request["delivery_profile_id"],
    }
    return data


def _visual_drill_selected_lineage(selection: Mapping[str, Any], lineage: list[dict[str, str]]) -> list[dict[str, str]]:
    family = str(selection.get("family_id", ""))
    if family not in DRILL_V2_FAMILIES or selection.get("variant_id") not in DRILL_V2_TIERS or selection.get("subtype_id") is not None:
        raise DynamicRequestPayloadBindingError("Cannot form authoring lineage for unknown Visual Drill selector/tier")
    required_paths = {
        f"definitions/visual_drill_{family}_canonical.json",
        f"profiles/difficulty/visual_drill_{family}.json",
        *DRILL_V2_COMMON_AUTHORING_PATHS,
    }
    by_path = {row["path"]: row for row in lineage}
    missing = required_paths - set(by_path)
    if missing:
        raise DynamicRequestPayloadBindingError(f"Selected Visual Drill authoring lineage is incomplete: {sorted(missing)}")
    return [copy.deepcopy(by_path[path]) for path in sorted(required_paths)]


def _expected_visual_drill_authoring_evidence(
    selection: Mapping[str, Any], seed: int, root: Path, lineage: list[dict[str, str]], actual: Mapping[str, Any]
) -> dict[str, Any]:
    family = str(selection.get("family_id", ""))
    variant = str(selection.get("variant_id", ""))
    if not _is_allowed_visual_drill_selection(selection):
        raise DynamicRequestPayloadBindingError("Visual Drill authoring evidence selection is outside the exact 20-pair matrix")
    tier = int(variant.removeprefix("tier-"))
    canonical_path = f"definitions/visual_drill_{family}_canonical.json"
    policy_path = f"profiles/difficulty/visual_drill_{family}.json"
    by_path = {row["path"]: row["sha256"] for row in lineage}
    for rel in (canonical_path, policy_path, *DRILL_V2_COMMON_AUTHORING_PATHS):
        if rel not in by_path or _sha_file(root / rel) != by_path[rel]:
            raise DynamicRequestPayloadBindingError(f"Selected Visual Drill source is not hash-bound: {rel}")
    canonical = _read_json(root, canonical_path)
    policy = _read_json(root, policy_path)
    canonical_payload = canonical.get("payload", {})
    duration = canonical_payload.get("duration")
    fps = canonical_payload.get("fps")
    frame_count = canonical_payload.get("frame_count")
    if canonical.get("subtype") != family or policy.get("domain_family") != "visual_drill" or policy.get("subtype") != family:
        raise DynamicRequestPayloadBindingError("Pinned Visual Drill definition/policy identity mismatch")
    if not isinstance(duration, (int, float)) or isinstance(duration, bool) or duration <= 0 or fps != 30 or frame_count != round(duration * fps):
        raise DynamicRequestPayloadBindingError("Pinned Visual Drill canonical timing tuple is invalid")
    policy_tiers = policy.get("tiers")
    if not isinstance(policy_tiers, Mapping) or set(policy_tiers) != {"1", "2", "3", "4", "5"}:
        raise DynamicRequestPayloadBindingError("Pinned Visual Drill policy must contain exact tiers 1..5")
    if not isinstance(policy_tiers.get(str(tier)), Mapping):
        raise DynamicRequestPayloadBindingError("Selected tier is missing from the pinned difficulty policy")
    selected_lineage = _visual_drill_selected_lineage(selection, lineage)
    expected = {
        "content_type": "visual_drills",
        "family_id": family,
        "variant_id": variant,
        "authoring_domain_family": "visual_drill",
        "authoring_subtype": family,
        "difficulty_tier": tier,
        "canonical_source_path": canonical_path,
        "canonical_source_sha256": by_path[canonical_path],
        "difficulty_policy_path": policy_path,
        "difficulty_policy_sha256": by_path[policy_path],
        "policy_registry_path": "core/authoring/VisualAuthoringPolicyRegistry.gd",
        "policy_registry_sha256": by_path["core/authoring/VisualAuthoringPolicyRegistry.gd"],
        "difficulty_resolver_path": "core/authoring/VisualDifficultyResolver.gd",
        "difficulty_resolver_sha256": by_path["core/authoring/VisualDifficultyResolver.gd"],
        "authoring_registry_path": "core/authoring/VisualAuthoringRegistry.gd",
        "authoring_registry_sha256": by_path["core/authoring/VisualAuthoringRegistry.gd"],
        "authoring_generator_path": "core/authoring/VisualAuthoringGenerator.gd",
        "authoring_generator_sha256": by_path["core/authoring/VisualAuthoringGenerator.gd"],
        "request_validator_path": "core/authoring/VisualAuthoringRequestValidator.gd",
        "request_validator_sha256": by_path["core/authoring/VisualAuthoringRequestValidator.gd"],
        "visual_drill_adapter_path": "core/authoring/adapters/VisualDrillAuthoringAdapter.gd",
        "visual_drill_adapter_sha256": by_path["core/authoring/adapters/VisualDrillAuthoringAdapter.gd"],
        "seed_variation_path": "core/authoring/VisualDrillSeedVariation.gd",
        "seed_variation_sha256": by_path["core/authoring/VisualDrillSeedVariation.gd"],
        "request_model_path": "core/authoring/VisualAuthoringRequest.gd",
        "request_model_sha256": by_path["core/authoring/VisualAuthoringRequest.gd"],
        "assembly_context_path": "core/authoring/VisualAuthoringAssemblyContext.gd",
        "assembly_context_sha256": by_path["core/authoring/VisualAuthoringAssemblyContext.gd"],
        "materialized_difficulty_tier": tier,
        "materialized_generator": family,
        "materialized_task_type": family,
        "seed_motion_seed": seed,
        "canonical_duration_seconds": float(duration),
        "canonical_fps": 30,
        "canonical_frame_count": int(frame_count),
        "materialized_duration_seconds": float(duration),
        "materialized_fps": 30,
        "materialized_frame_count": int(frame_count),
    }
    parameter_digest = actual.get("resolved_effective_parameters_sha256")
    if not _is_sha(parameter_digest):
        raise DynamicRequestPayloadBindingError("Resolved effective authoring-parameter digest is malformed")
    expected["resolved_effective_parameters_sha256"] = parameter_digest
    if set(actual) != set(expected):
        raise DynamicRequestPayloadBindingError("Visual Drill authoring evidence has missing or unknown fields")
    for field, expected_value in expected.items():
        if actual.get(field) != expected_value:
            raise DynamicRequestPayloadBindingError(f"Visual Drill authoring evidence mismatch at {field}")
    return expected


def _validate_godot_summary(
    summary: Mapping[str, Any],
    chain: Mapping[str, Any],
    contract_data: tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[dict[str, str]]] | None = None,
    project_root: Path | None = None,
) -> None:
    result = chain["result"]
    req = result["canonical_request"]
    selection = _canonical_selection(result["plan"]["selection"])
    content_type = str(selection["content_type"])
    v2 = contract_data is not None and _is_visual_drill_v2_contract(contract_data[0])
    lineage = contract_data[3] if contract_data is not None else []
    if v2:
        if content_type != "visual_drills" or not _is_allowed_visual_drill_selection(selection):
            raise DynamicRequestPayloadBindingError("V2 harness may materialize only exact Visual Drill selector/tier pairs")
        expected_scope, exact = DRILL_V2_PAYLOAD_SCOPE, True
    else:
        expected_scope, exact = EXPECTED_SCOPE[content_type]
    grammar_evidence = summary.get("grammar_parameter_evidence")
    if content_type == "visual_loops":
        expected_evidence_literals = {
            "composition_role": "D_OWNED_COMPOSITE_REVIEW_PAYLOAD",
            "payload_member_path": "grammar_parameter_instance",
            "payload_contains_instance": True,
            "grammar_id": "harmonic_membrane",
            "grammar_index": 0,
            "shader_branch": "field_harmonic_membrane",
            "shader_uniform": "grammar_mode",
            "style_parameter_count": 20,
            "family_authoring_envelope_subtype": "geometric",
            "family_authoring_adapter_itself_grammar_aware": False,
        }
        if not isinstance(grammar_evidence, Mapping):
            raise DynamicRequestPayloadBindingError("Visual Loop composite payload is missing grammar-parameter evidence")
        if set(grammar_evidence) != set(expected_evidence_literals) | {"style_parameters_sha256", "parameter_instance_sha256"}:
            raise DynamicRequestPayloadBindingError("Visual Loop grammar evidence contains missing/unknown properties")
        for field, value in expected_evidence_literals.items():
            if grammar_evidence.get(field) != value:
                raise DynamicRequestPayloadBindingError(f"Visual Loop grammar evidence mismatch at {field}")
        for field in ("style_parameters_sha256", "parameter_instance_sha256"):
            if not _is_sha(grammar_evidence.get(field)):
                raise DynamicRequestPayloadBindingError(f"Visual Loop grammar evidence has malformed {field}")
    elif grammar_evidence is not None:
        raise DynamicRequestPayloadBindingError("Non-Loop selector must not carry Visual Loop grammar evidence")
    expected = {
        "schema": DRILL_V2_GODOT_SUMMARY_SCHEMA_ID if v2 else GODOT_SUMMARY_SCHEMA_ID,
        "schema_version": "2.0" if v2 else "1.0",
        "status": "PREPARATION_ONLY_DYNAMIC_REQUEST_BOUND_IN_MEMORY_INSTANCE_NOT_RENDERER_INPUT",
        "request_id": req["request_id"],
        "request_hash": result["request_hash"],
        "content_type": content_type,
        "selection": selection,
        "gameplay_seed": req["seed"],
        "music_seed": req["music_seed"],
        "variation_index": req["variation_index"],
        "presentation_profile_id": req["presentation_profile_id"],
        "delivery_profile_id": req["delivery_profile_id"],
        "payload_scope": expected_scope,
        "exact_selector_payload_materialized": exact,
        "payload_deterministic_repeat": True,
        "payload_materialization": "IN_MEMORY_ONLY",
        "semantic_limits": EXPECTED_SEMANTIC_LIMITS,
        "execution_boundary": EXPECTED_BOUNDARY,
    }
    if v2:
        actual_authoring = summary.get("visual_drill_authoring_evidence")
        if not isinstance(actual_authoring, Mapping):
            raise DynamicRequestPayloadBindingError("V2 Godot summary is missing Visual Drill authoring-source evidence")
        expected["visual_drill_authoring_evidence"] = _expected_visual_drill_authoring_evidence(
            selection, int(req["seed"]), project_root if project_root is not None else _root(), lineage, actual_authoring
        )
    for key, expected_value in expected.items():
        if summary.get(key) != expected_value:
            raise DynamicRequestPayloadBindingError(f"Godot summary mismatch at {key}: expected {expected_value!r}, got {summary.get(key)!r}")
    if not _is_sha(summary.get("payload_sha256")):
        raise DynamicRequestPayloadBindingError("Godot payload hash is malformed")
    if not _is_sha(summary.get("visual_state_sha256")):
        raise DynamicRequestPayloadBindingError("Godot visual-state hash is malformed")
    allowed = set(expected) | {"payload_sha256", "visual_state_sha256", "grammar_parameter_evidence"}
    if set(summary) != allowed:
        raise DynamicRequestPayloadBindingError("Godot summary shape contains missing or unknown properties")


def _invoke_godot(
    chain: Mapping[str, Any], godot: str, timeout: int, root: Path,
    process_runner: Callable[..., Any],
    contract_data: tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[dict[str, str]]] | None = None,
) -> dict[str, Any]:
    contract = contract_data[0] if contract_data is not None else None
    data = _godot_input(chain, contract)
    encoded = base64.b64encode(_canonical(data).encode("utf-8")).decode("ascii")
    harness_rel = Path(str(contract.get("harness", {}).get("path", GODOT_HARNESS_REL.as_posix()))) if contract else GODOT_HARNESS_REL
    command = [godot, "--headless", "--path", str(root), "--script", "res://" + harness_rel.as_posix(), "--", encoded]
    try:
        completed = process_runner(command, cwd=str(root), text=True, capture_output=True, timeout=timeout, check=False)
    except Exception as exc:
        raise DynamicRequestPayloadBindingError(f"Godot dynamic payload harness invocation failed: {exc}") from exc
    stdout = str(getattr(completed, "stdout", "") or "")
    stderr = str(getattr(completed, "stderr", "") or "")
    combined = stdout + "\n" + stderr
    exit_code = int(getattr(completed, "returncode", -1))
    if exit_code != 0:
        raise DynamicRequestPayloadBindingError(f"Godot harness returned exit={exit_code}: {combined[-4000:]}")
    if any(marker in combined for marker in ERROR_MARKERS):
        raise DynamicRequestPayloadBindingError(f"Godot harness emitted an error marker: {combined[-4000:]}")
    rows = [line[len(GODOT_SUMMARY_PREFIX):] for line in combined.splitlines() if line.startswith(GODOT_SUMMARY_PREFIX)]
    if len(rows) != 1:
        raise DynamicRequestPayloadBindingError(f"Expected one Godot dynamic payload summary, received {len(rows)}")
    try:
        summary = json.loads(rows[0])
    except json.JSONDecodeError as exc:
        raise DynamicRequestPayloadBindingError("Godot dynamic payload summary is not valid JSON") from exc
    if not isinstance(summary, Mapping):
        raise DynamicRequestPayloadBindingError("Godot summary root must be an object")
    _validate_godot_summary(summary, chain, contract_data, root)
    return dict(summary)


def _build_receipt(
    chain: Mapping[str, Any], summary: Mapping[str, Any], root: Path,
    contract: Mapping[str, Any], lineage: list[dict[str, str]],
    contract_data: tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[dict[str, str]]] | None = None,
    repeat_summary: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    v2 = _is_visual_drill_v2_contract(contract)
    result, bridge, envelope = chain["result"], chain["bridge"], chain["envelope"]
    request = result["canonical_request"]
    content_type = str(result["plan"]["selection"]["content_type"])
    expected_scope, exact = (DRILL_V2_PAYLOAD_SCOPE, True) if v2 else EXPECTED_SCOPE[content_type]
    if v2 and (content_type != "visual_drills" or repeat_summary is None):
        raise DynamicRequestPayloadBindingError("Visual Drill V2 receipt requires a Drill request and independent repeated runtime evidence")
    request_identity = {
        "request_id": request["request_id"],
        "content_type": content_type,
        "selection": _canonical_selection(result["plan"]["selection"]),
        "gameplay_seed": request["seed"],
        "music_seed": request["music_seed"],
        "variation_index": request["variation_index"],
        "presentation_profile_id": request["presentation_profile_id"],
        "delivery_profile_id": request["delivery_profile_id"],
    }
    binding = chain["source_binding"]
    binding_identity = binding["source_identity"]
    grammar_evidence = copy.deepcopy(summary.get("grammar_parameter_evidence"))
    grammar_instance_sha = grammar_evidence.get("parameter_instance_sha256") if isinstance(grammar_evidence, Mapping) else None

    runtime_repeat_evidence: dict[str, Any] | None = None
    visual_drill_authoring: dict[str, Any] | None = None
    if v2:
        first_authoring = summary.get("visual_drill_authoring_evidence")
        repeat_authoring = repeat_summary.get("visual_drill_authoring_evidence") if repeat_summary is not None else None
        if not isinstance(first_authoring, Mapping) or not isinstance(repeat_authoring, Mapping):
            raise DynamicRequestPayloadBindingError("Independent Visual Drill run lacks authoring identity evidence")
        if summary.get("payload_sha256") != repeat_summary.get("payload_sha256") or summary.get("visual_state_sha256") != repeat_summary.get("visual_state_sha256"):
            raise DynamicRequestPayloadBindingError("Independent Visual Drill runtime executions produced different payload/visual-state digests")
        if dict(first_authoring) != dict(repeat_authoring):
            raise DynamicRequestPayloadBindingError("Independent Visual Drill runtime executions produced different authoring/lineage evidence")
        runtime_repeat_evidence = {
            "status": "VERIFIED",
            "independent_runtime_executions": 2,
            "first_payload_sha256": summary["payload_sha256"],
            "repeat_payload_sha256": repeat_summary["payload_sha256"],
            "first_visual_state_sha256": summary["visual_state_sha256"],
            "repeat_visual_state_sha256": repeat_summary["visual_state_sha256"],
            "first_authoring_evidence_sha256": _sha_json(first_authoring),
            "repeat_authoring_evidence_sha256": _sha_json(repeat_authoring),
        }
        selection = request_identity["selection"]
        authoring_lineage = _visual_drill_selected_lineage(selection, lineage)
        visual_drill_authoring = {
            "selection": copy.deepcopy(selection),
            "evidence": copy.deepcopy(dict(first_authoring)),
            "source_lineage": authoring_lineage,
            "source_lineage_sha256": _sha_json(authoring_lineage),
        }

    payload_manifest: dict[str, Any] = {
        "schema": DRILL_V2_PAYLOAD_MANIFEST_SCHEMA_ID if v2 else PAYLOAD_MANIFEST_SCHEMA_ID,
        "schema_version": "2.0" if v2 else "1.0",
        "status": DRILL_V2_PAYLOAD_MANIFEST_STATUS if v2 else PAYLOAD_MANIFEST_STATUS,
        "frozen_c11c_manifest_sha256": EXPECTED_MANIFEST_SHA256,
        "request_identity": {
            "request_id": request["request_id"],
            "content_type": content_type,
            "selection": _canonical_selection(result["plan"]["selection"]),
            "canonical_request_sha256": result["request_hash"],
            "plan_sha256": result["plan_hash"],
            "editorial_sha256": result["editorial_hash"],
            "gameplay_seed": request["seed"],
            "music_seed": request["music_seed"],
            "variation_index": request["variation_index"],
            "presentation_profile_id": request["presentation_profile_id"],
            "delivery_profile_id": request["delivery_profile_id"],
        },
        "source_lineage": {
            "bridge_record_sha256": bridge["record_hash"],
            "adapter_envelope_sha256": envelope["envelope_hash"],
            "request_scoped_binding_sha256": binding["binding_sha256"],
            "binding_preview_sha256": binding_identity["binding_preview_sha256"],
            "logical_composition_sha256": binding_identity["logical_composition_sha256"],
            "frame_program_sha256": binding_identity["frame_program_sha256"],
            "temporal_preview_sha256": binding_identity["temporal_preview_sha256"],
            "delivery_projection_sha256": binding_identity["delivery_projection_sha256"],
            "editorial_review_manifest_sha256": binding_identity["editorial_review_manifest_sha256"],
            "definition_source_sha256": binding_identity["definition_source_sha256"],
            "registry_sha256": binding_identity["registry_sha256"],
            "request_scoped_binding_lineage_sha256": binding_identity["source_lineage_sha256"],
            "dynamic_binding_lineage_sha256": _sha_json(lineage),
        },
        "payload_identity": {
            "payload_sha256": summary["payload_sha256"],
            "visual_state_sha256": summary["visual_state_sha256"],
            "payload_scope": expected_scope,
            "exact_selector_payload_materialized": exact,
            "materialization": "IN_MEMORY_ONLY",
            "grammar_parameter_instance_sha256": grammar_instance_sha,
        },
        "governance": {
            "candidate_input_admissible": False,
            "video_render_ready": False,
            "renderer_native_input_emitted": False,
            "renderer_dispatch_invoked": False,
            "media_created": False,
            "d4_8": "BLOCKED",
            "release_authority": "NONE",
        },
    }
    if v2:
        payload_manifest["visual_drill_authoring"] = visual_drill_authoring
        payload_manifest["runtime_repeat_evidence"] = runtime_repeat_evidence
    payload_manifest["manifest_sha256"] = _sha_json(payload_manifest)
    payload_manifest_sha256 = payload_manifest["manifest_sha256"]

    identity_core = {
        **request_identity,
        "request_hash": result["request_hash"],
        "plan_hash": result["plan_hash"],
        "editorial_hash": result["editorial_hash"],
        "bridge_record_hash": bridge["record_hash"],
        "adapter_envelope_hash": envelope["envelope_hash"],
        "source_binding_sha256": chain["source_binding"]["binding_sha256"],
        "payload_sha256": summary["payload_sha256"],
        "visual_state_sha256": summary["visual_state_sha256"],
        "request_payload_manifest_sha256": payload_manifest_sha256,
        "frozen_c11c_manifest_sha256": EXPECTED_MANIFEST_SHA256,
    }
    request_binding_sha256 = _sha_json(identity_core)
    request_identity["request_binding_sha256"] = request_binding_sha256
    payload_evidence: dict[str, Any] = {
        "payload_sha256": summary["payload_sha256"],
        "visual_state_sha256": summary["visual_state_sha256"],
        "payload_scope": expected_scope,
        "exact_selector_payload_materialized": exact,
        "deterministic_repeat_pass": True,
        "materialization": "IN_MEMORY_ONLY",
        "grammar_parameter_evidence": grammar_evidence,
        "request_payload_manifest_sha256": payload_manifest_sha256,
    }
    if v2:
        payload_evidence["visual_drill_authoring_evidence"] = copy.deepcopy(dict(summary["visual_drill_authoring_evidence"]))
        payload_evidence["runtime_repeat_evidence"] = copy.deepcopy(runtime_repeat_evidence)
    receipt: dict[str, Any] = {
        "schema": DRILL_V2_OUTPUT_SCHEMA_ID if v2 else OUTPUT_SCHEMA_ID,
        "schema_version": "2.0" if v2 else "1.0",
        "status": DRILL_V2_STATUS if v2 else STATUS,
        "frozen_c11c_manifest_sha256": EXPECTED_MANIFEST_SHA256,
        "source_identity": {
            "request_hash": result["request_hash"],
            "plan_hash": result["plan_hash"],
            "editorial_hash": result["editorial_hash"],
            "bridge_record_hash": bridge["record_hash"],
            "adapter_envelope_hash": envelope["envelope_hash"],
            "source_binding_sha256": chain["source_binding"]["binding_sha256"],
            "source_lineage_sha256": _sha_json(lineage),
            "binding_preview_sha256": binding_identity["binding_preview_sha256"],
            "logical_composition_sha256": binding_identity["logical_composition_sha256"],
            "frame_program_sha256": binding_identity["frame_program_sha256"],
            "temporal_preview_sha256": binding_identity["temporal_preview_sha256"],
            "delivery_projection_sha256": binding_identity["delivery_projection_sha256"],
            "editorial_review_manifest_sha256": binding_identity["editorial_review_manifest_sha256"],
            "definition_source_sha256": binding_identity["definition_source_sha256"],
            "registry_sha256": binding_identity["registry_sha256"],
            "request_scoped_binding_sha256": binding["binding_sha256"],
            "binding_source_lineage_sha256": binding_identity["source_lineage_sha256"],
            "request_payload_manifest_sha256": payload_manifest_sha256,
            "harness_sha256": contract["harness"]["sha256"],
            "implementation_sha256": _sha_file(Path(__file__).resolve()),
        },
        "request_identity": request_identity,
        "payload_evidence": payload_evidence,
        "payload_manifest": payload_manifest,
        "semantic_limits": copy.deepcopy(EXPECTED_SEMANTIC_LIMITS),
        "readiness": {
            "canonical_request_chain_passed": True,
            "canonical_source_bound": True,
            "request_payload_hash_bound": True,
            "exact_selected_payload_instance_materialized": exact,
            "candidate_input_admissible": False,
            "video_render_ready": False,
        },
        "execution_boundary": copy.deepcopy(EXPECTED_BOUNDARY),
    }
    if v2:
        receipt["runtime_verification_status"] = "VERIFIED"
        receipt["runtime_repeat_evidence"] = copy.deepcopy(runtime_repeat_evidence)
    receipt["receipt_sha256"] = _sha_json(receipt)
    effective_contract_data = contract_data if contract_data is not None else _load_contract(root)
    _validate_receipt(receipt, root, effective_contract_data)
    return receipt


def _validate_receipt(
    receipt: Mapping[str, Any], root: Path,
    contract_data: tuple[dict[str, Any], dict[str, Any], dict[str, str], list[dict[str, str]]] | None = None,
) -> bool:
    loaded = contract_data if contract_data is not None else _load_contract(root)
    contract, _, schema, lineage = loaded
    v2 = _is_visual_drill_v2_contract(contract)
    if set(receipt) != set(schema.get("required", [])):
        raise DynamicRequestPayloadBindingError("Receipt does not match strict output schema shape")
    if receipt.get("receipt_sha256") != _sha_json({key: value for key, value in receipt.items() if key != "receipt_sha256"}):
        raise DynamicRequestPayloadBindingError("Receipt SHA-256 mismatch")
    expected_receipt_identity = (
        (DRILL_V2_OUTPUT_SCHEMA_ID, "2.0", DRILL_V2_STATUS)
        if v2 else (OUTPUT_SCHEMA_ID, "1.0", STATUS)
    )
    if (receipt.get("schema"), receipt.get("schema_version"), receipt.get("status")) != expected_receipt_identity:
        raise DynamicRequestPayloadBindingError("Receipt identity/status cannot be promoted")
    if v2 and receipt.get("runtime_verification_status") != "VERIFIED":
        raise DynamicRequestPayloadBindingError("Visual Drill V2 receipt is not runtime-verified")
    if receipt.get("frozen_c11c_manifest_sha256") != EXPECTED_MANIFEST_SHA256:
        raise DynamicRequestPayloadBindingError("Receipt immutable C11-C manifest pin mismatch")

    source = receipt.get("source_identity")
    identity = receipt.get("request_identity")
    evidence = receipt.get("payload_evidence")
    readiness = receipt.get("readiness")
    if not all(isinstance(item, Mapping) for item in (source, identity, evidence, readiness)):
        raise DynamicRequestPayloadBindingError("Receipt identity/evidence/readiness sections must be objects")
    content_type = str(identity.get("content_type", ""))
    selection_value = identity.get("selection", {})
    if v2:
        if content_type != "visual_drills" or not isinstance(selection_value, Mapping) or not _is_allowed_visual_drill_selection(selection_value):
            raise DynamicRequestPayloadBindingError("Receipt Visual Drill selector identity is outside the exact 20-pair matrix")
        expected_scope, expected_exact = DRILL_V2_PAYLOAD_SCOPE, True
    else:
        if content_type not in EXPECTED_SELECTIONS:
            raise DynamicRequestPayloadBindingError("Receipt content type is outside the pinned selector matrix")
        if selection_value != EXPECTED_SELECTIONS[content_type] or selection_value.get("content_type") != content_type:
            raise DynamicRequestPayloadBindingError("Receipt selector identity is outside the pinned matrix")
        expected_scope, expected_exact = EXPECTED_SCOPE[content_type]
    if evidence.get("payload_scope") != expected_scope or evidence.get("exact_selector_payload_materialized") is not expected_exact:
        raise DynamicRequestPayloadBindingError("Receipt payload scope/materialization claim contradicts the pinned selector matrix")
    if evidence.get("deterministic_repeat_pass") is not True or evidence.get("materialization") != "IN_MEMORY_ONLY":
        raise DynamicRequestPayloadBindingError("Receipt payload evidence is not an in-memory deterministic repeat")
    if not _is_sha(evidence.get("payload_sha256")) or not _is_sha(evidence.get("visual_state_sha256")):
        raise DynamicRequestPayloadBindingError("Receipt payload or visual-state digest is malformed")
    grammar_evidence = evidence.get("grammar_parameter_evidence")
    if content_type == "visual_loops":
        expected_grammar_literals = {
            "composition_role": "D_OWNED_COMPOSITE_REVIEW_PAYLOAD",
            "payload_member_path": "grammar_parameter_instance",
            "payload_contains_instance": True,
            "grammar_id": "harmonic_membrane",
            "grammar_index": 0,
            "shader_branch": "field_harmonic_membrane",
            "shader_uniform": "grammar_mode",
            "style_parameter_count": 20,
            "family_authoring_envelope_subtype": "geometric",
            "family_authoring_adapter_itself_grammar_aware": False,
        }
        if not isinstance(grammar_evidence, Mapping):
            raise DynamicRequestPayloadBindingError("Visual Loop receipt is missing composite grammar evidence")
        if set(grammar_evidence) != set(expected_grammar_literals) | {"style_parameters_sha256", "parameter_instance_sha256"}:
            raise DynamicRequestPayloadBindingError("Visual Loop receipt grammar evidence shape mismatch")
        for field, expected_value in expected_grammar_literals.items():
            if grammar_evidence.get(field) != expected_value:
                raise DynamicRequestPayloadBindingError(f"Visual Loop receipt grammar evidence mismatch at {field}")
        for field in ("style_parameters_sha256", "parameter_instance_sha256"):
            if not _is_sha(grammar_evidence.get(field)):
                raise DynamicRequestPayloadBindingError(f"Visual Loop receipt grammar digest malformed: {field}")
    elif grammar_evidence is not None:
        raise DynamicRequestPayloadBindingError("Non-Loop receipt contains inadmissible grammar evidence")
    if readiness != {
        "canonical_request_chain_passed": True,
        "canonical_source_bound": True,
        "request_payload_hash_bound": True,
        "exact_selected_payload_instance_materialized": expected_exact,
        "candidate_input_admissible": False,
        "video_render_ready": False,
    }:
        raise DynamicRequestPayloadBindingError("Receipt readiness attempted to promote renderer or candidate readiness")
    if receipt.get("semantic_limits") != EXPECTED_SEMANTIC_LIMITS or receipt.get("execution_boundary") != EXPECTED_BOUNDARY:
        raise DynamicRequestPayloadBindingError("Receipt attempted to alter semantic or execution-governance limits")
    expected_source_identity = {
        "harness_sha256": contract["harness"]["sha256"],
        "source_lineage_sha256": _sha_json(lineage),
        "implementation_sha256": _sha_file(Path(__file__).resolve()),
    }
    for field, value in expected_source_identity.items():
        if source.get(field) != value:
            raise DynamicRequestPayloadBindingError(f"Receipt source identity mismatch at {field}")
    if not _is_sha(source.get("request_hash")) or not _is_sha(source.get("plan_hash")) or not _is_sha(source.get("editorial_hash")):
        raise DynamicRequestPayloadBindingError("Receipt canonical request/plan/editorial hashes are malformed")

    manifest = receipt.get("payload_manifest")
    if not isinstance(manifest, Mapping):
        raise DynamicRequestPayloadBindingError("Receipt is missing its request-scoped payload manifest")
    manifest_unsigned = {str(k): copy.deepcopy(v) for k, v in manifest.items() if k != "manifest_sha256"}
    manifest_sha = manifest.get("manifest_sha256")
    if not _is_sha(manifest_sha) or manifest_sha != _sha_json(manifest_unsigned):
        raise DynamicRequestPayloadBindingError("Request-scoped payload manifest digest mismatch")
    expected_manifest_identity = (
        (DRILL_V2_PAYLOAD_MANIFEST_SCHEMA_ID, "2.0", DRILL_V2_PAYLOAD_MANIFEST_STATUS)
        if v2 else (PAYLOAD_MANIFEST_SCHEMA_ID, "1.0", PAYLOAD_MANIFEST_STATUS)
    )
    if (manifest.get("schema"), manifest.get("schema_version"), manifest.get("status")) != expected_manifest_identity:
        raise DynamicRequestPayloadBindingError("Request-scoped payload manifest identity/status mismatch")
    if manifest.get("frozen_c11c_manifest_sha256") != EXPECTED_MANIFEST_SHA256:
        raise DynamicRequestPayloadBindingError("Payload manifest immutable C11-C pin mismatch")
    manifest_request = manifest.get("request_identity")
    manifest_lineage = manifest.get("source_lineage")
    manifest_payload = manifest.get("payload_identity")
    manifest_governance = manifest.get("governance")
    if not all(isinstance(item, Mapping) for item in (manifest_request, manifest_lineage, manifest_payload, manifest_governance)):
        raise DynamicRequestPayloadBindingError("Payload manifest sections must be objects")
    expected_manifest_governance = {
        "candidate_input_admissible": False, "video_render_ready": False,
        "renderer_native_input_emitted": False, "renderer_dispatch_invoked": False,
        "media_created": False, "d4_8": "BLOCKED", "release_authority": "NONE",
    }
    if dict(manifest_governance) != expected_manifest_governance:
        raise DynamicRequestPayloadBindingError("Payload manifest attempted to promote candidate/renderer governance")
    for field, expected_value in {
        "request_id": identity.get("request_id"), "content_type": identity.get("content_type"),
        "selection": identity.get("selection"), "gameplay_seed": identity.get("gameplay_seed"),
        "music_seed": identity.get("music_seed"), "variation_index": identity.get("variation_index"),
        "presentation_profile_id": identity.get("presentation_profile_id"), "delivery_profile_id": identity.get("delivery_profile_id"),
        "canonical_request_sha256": source.get("request_hash"), "plan_sha256": source.get("plan_hash"),
        "editorial_sha256": source.get("editorial_hash"),
    }.items():
        if manifest_request.get(field) != expected_value:
            raise DynamicRequestPayloadBindingError(f"Payload manifest request identity mismatch at {field}")
    expected_lineage = {
        "bridge_record_sha256": source.get("bridge_record_hash"),
        "adapter_envelope_sha256": source.get("adapter_envelope_hash"),
        "request_scoped_binding_sha256": source.get("request_scoped_binding_sha256"),
        "binding_preview_sha256": source.get("binding_preview_sha256"),
        "logical_composition_sha256": source.get("logical_composition_sha256"),
        "frame_program_sha256": source.get("frame_program_sha256"),
        "temporal_preview_sha256": source.get("temporal_preview_sha256"),
        "delivery_projection_sha256": source.get("delivery_projection_sha256"),
        "editorial_review_manifest_sha256": source.get("editorial_review_manifest_sha256"),
        "definition_source_sha256": source.get("definition_source_sha256"),
        "registry_sha256": source.get("registry_sha256"),
        "request_scoped_binding_lineage_sha256": source.get("binding_source_lineage_sha256"),
        "dynamic_binding_lineage_sha256": source.get("source_lineage_sha256"),
    }
    if dict(manifest_lineage) != expected_lineage:
        raise DynamicRequestPayloadBindingError("Payload manifest source lineage does not match the request chain")
    grammar_instance_sha = grammar_evidence.get("parameter_instance_sha256") if isinstance(grammar_evidence, Mapping) else None
    expected_payload_identity = {
        "payload_sha256": evidence.get("payload_sha256"), "visual_state_sha256": evidence.get("visual_state_sha256"),
        "payload_scope": evidence.get("payload_scope"),
        "exact_selector_payload_materialized": evidence.get("exact_selector_payload_materialized"),
        "materialization": evidence.get("materialization"),
        "grammar_parameter_instance_sha256": grammar_instance_sha,
    }
    if dict(manifest_payload) != expected_payload_identity:
        raise DynamicRequestPayloadBindingError("Payload manifest digest target differs from the materialized payload evidence")
    if source.get("request_payload_manifest_sha256") != manifest_sha or evidence.get("request_payload_manifest_sha256") != manifest_sha:
        raise DynamicRequestPayloadBindingError("Request payload manifest hash is not propagated into receipt identity/evidence")

    if v2:
        repeat = receipt.get("runtime_repeat_evidence")
        evidence_repeat = evidence.get("runtime_repeat_evidence")
        manifest_repeat = manifest.get("runtime_repeat_evidence")
        if not all(isinstance(item, Mapping) for item in (repeat, evidence_repeat, manifest_repeat)):
            raise DynamicRequestPayloadBindingError("Visual Drill V2 independent runtime-repeat evidence is missing")
        if dict(repeat) != dict(evidence_repeat) or dict(repeat) != dict(manifest_repeat):
            raise DynamicRequestPayloadBindingError("Runtime-repeat evidence differs between receipt and request manifest")
        expected_repeat = {
            "status": "VERIFIED",
            "independent_runtime_executions": 2,
            "first_payload_sha256": evidence.get("payload_sha256"),
            "repeat_payload_sha256": evidence.get("payload_sha256"),
            "first_visual_state_sha256": evidence.get("visual_state_sha256"),
            "repeat_visual_state_sha256": evidence.get("visual_state_sha256"),
            "first_authoring_evidence_sha256": _sha_json(evidence.get("visual_drill_authoring_evidence", {})),
            "repeat_authoring_evidence_sha256": _sha_json(evidence.get("visual_drill_authoring_evidence", {})),
        }
        if dict(repeat) != expected_repeat:
            raise DynamicRequestPayloadBindingError("Independent runtime runs are not byte-equivalent for payload, state and authoring evidence")
        authoring = evidence.get("visual_drill_authoring_evidence")
        manifest_authoring = manifest.get("visual_drill_authoring")
        if not isinstance(authoring, Mapping) or not isinstance(manifest_authoring, Mapping):
            raise DynamicRequestPayloadBindingError("Visual Drill V2 selector/policy lineage is missing")
        _expected_visual_drill_authoring_evidence(
            selection_value, int(identity.get("gameplay_seed", -1)), root, lineage, authoring
        )
        selected_lineage = _visual_drill_selected_lineage(selection_value, lineage)
        expected_authoring = {
            "selection": dict(selection_value),
            "evidence": dict(authoring),
            "source_lineage": selected_lineage,
            "source_lineage_sha256": _sha_json(selected_lineage),
        }
        if dict(manifest_authoring) != expected_authoring:
            raise DynamicRequestPayloadBindingError("Visual Drill manifest authoring lineage is not closed over the selected family/tier")

    identity_core = {
        "request_id": identity.get("request_id"),
        "content_type": identity.get("content_type"),
        "selection": identity.get("selection"),
        "gameplay_seed": identity.get("gameplay_seed"),
        "music_seed": identity.get("music_seed"),
        "variation_index": identity.get("variation_index"),
        "presentation_profile_id": identity.get("presentation_profile_id"),
        "delivery_profile_id": identity.get("delivery_profile_id"),
        "request_hash": source.get("request_hash"),
        "plan_hash": source.get("plan_hash"),
        "editorial_hash": source.get("editorial_hash"),
        "bridge_record_hash": source.get("bridge_record_hash"),
        "adapter_envelope_hash": source.get("adapter_envelope_hash"),
        "source_binding_sha256": source.get("source_binding_sha256"),
        "payload_sha256": evidence.get("payload_sha256"),
        "visual_state_sha256": evidence.get("visual_state_sha256"),
        "request_payload_manifest_sha256": manifest_sha,
        "frozen_c11c_manifest_sha256": EXPECTED_MANIFEST_SHA256,
    }
    if identity.get("request_binding_sha256") != _sha_json(identity_core):
        raise DynamicRequestPayloadBindingError("Receipt request/payload binding digest does not match its identity fields")

    try:
        import jsonschema  # type: ignore
    except ImportError:
        jsonschema = None
    if jsonschema is not None:
        try:
            jsonschema.Draft202012Validator(schema).validate(dict(receipt))
        except Exception as exc:
            raise DynamicRequestPayloadBindingError(f"Receipt schema validation failed closed: {exc.message if hasattr(exc, 'message') else exc}") from exc
    return True


def _run_one(
    raw: Mapping[str, Any], godot: str, timeout: int, root: Path,
    contract_data: tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[dict[str, str]]],
    process_runner: Callable[..., Any], independent_repeat: bool = False,
) -> tuple[dict[str, Any], dict[str, Any]]:
    contract, input_schema, output_schema, lineage = contract_data
    v2 = _is_visual_drill_v2_contract(contract)
    chain = _build_canonical_chain(raw, root, allow_visual_drill_matrix=v2)
    godot_input = _godot_input(chain, contract)
    try:
        import jsonschema  # type: ignore
    except ImportError:
        jsonschema = None
    if jsonschema is not None:
        try:
            jsonschema.Draft202012Validator(input_schema).validate(godot_input)
        except Exception as exc:
            raise DynamicRequestPayloadBindingError(f"Godot input schema validation failed closed: {exc.message if hasattr(exc, 'message') else exc}") from exc
    summary = _invoke_godot(chain, godot, timeout, root, process_runner, contract_data)
    repeated_summary: dict[str, Any] | None = None
    if independent_repeat:
        if not v2:
            raise DynamicRequestPayloadBindingError("Independent full runtime repeats are reserved for the Visual Drill V2 gate")
        repeated_chain = _build_canonical_chain(raw, root, allow_visual_drill_matrix=True)
        for key in ("request_hash", "plan_hash", "editorial_hash"):
            if chain["result"].get(key) != repeated_chain["result"].get(key):
                raise DynamicRequestPayloadBindingError(f"Repeated canonical request-chain resolution changed {key}")
        if chain["bridge"].get("record_hash") != repeated_chain["bridge"].get("record_hash"):
            raise DynamicRequestPayloadBindingError("Repeated canonical bridge record changed")
        if chain["envelope"].get("envelope_hash") != repeated_chain["envelope"].get("envelope_hash"):
            raise DynamicRequestPayloadBindingError("Repeated canonical adapter envelope changed")
        if chain["source_binding"].get("binding_sha256") != repeated_chain["source_binding"].get("binding_sha256"):
            raise DynamicRequestPayloadBindingError("Repeated canonical request-scoped binding changed")
        repeated_summary = _invoke_godot(repeated_chain, godot, timeout, root, process_runner, contract_data)
    receipt = _build_receipt(chain, summary, root, contract, lineage, contract_data, repeated_summary)
    return receipt, summary


def _assert_visual_drill_matrix(receipts: list[Mapping[str, Any]]) -> dict[str, int]:
    if len(receipts) != 20:
        raise DynamicRequestPayloadBindingError(f"Visual Drill V2 gate requires exactly 20 receipts, got {len(receipts)}")
    expected = {
        (family, tier)
        for family in DRILL_V2_FAMILIES
        for tier in DRILL_V2_TIERS
    }
    seen: set[tuple[str, str]] = set()
    for receipt in receipts:
        identity = receipt.get("request_identity", {})
        evidence = receipt.get("payload_evidence", {})
        manifest = receipt.get("payload_manifest", {})
        selection = identity.get("selection", {}) if isinstance(identity, Mapping) else {}
        key = (str(selection.get("family_id", "")), str(selection.get("variant_id", "")))
        if key not in expected or key in seen:
            raise DynamicRequestPayloadBindingError(f"Visual Drill V2 matrix has unknown or duplicate selector/tier: {key}")
        seen.add(key)
        if receipt.get("runtime_verification_status") != "VERIFIED":
            raise DynamicRequestPayloadBindingError(f"Visual Drill V2 receipt is not VERIFIED: {key}")
        if evidence.get("exact_selector_payload_materialized") is not True or evidence.get("payload_scope") != DRILL_V2_PAYLOAD_SCOPE:
            raise DynamicRequestPayloadBindingError(f"Visual Drill V2 exact selector payload not accepted: {key}")
        if manifest.get("manifest_sha256") != evidence.get("request_payload_manifest_sha256"):
            raise DynamicRequestPayloadBindingError(f"Visual Drill V2 manifest digest is not propagated: {key}")
        repeat = receipt.get("runtime_repeat_evidence", {})
        if not isinstance(repeat, Mapping) or repeat.get("status") != "VERIFIED" or repeat.get("independent_runtime_executions") != 2:
            raise DynamicRequestPayloadBindingError(f"Visual Drill V2 independent-repeat proof missing: {key}")
    if seen != expected:
        raise DynamicRequestPayloadBindingError(f"Visual Drill V2 matrix incomplete; missing={sorted(expected-seen)}")
    return {"cases": 20, "families": 4, "tiers": 5, "independent_repeat": 20, "manifests": 20, "lineage_closure": 20}


def run_dynamic_request_matrix(
    godot: str,
    timeout: int = 120,
    project_root: Path | str | None = None,
    process_runner: Callable[..., Any] = subprocess.run,
    raw_requests: list[dict[str, Any]] | None = None,
    mode: str = "v1",
    independent_repeat: bool = False,
) -> dict[str, Any]:
    root = _root(project_root)
    contract_data = _load_contract_for_mode(root, mode)
    v2 = _is_visual_drill_v2_contract(contract_data[0])
    raw_list = raw_requests if raw_requests is not None else (_visual_drill_matrix_raw_requests() if v2 else _matrix_raw_requests())
    if v2 and not independent_repeat:
        raise DynamicRequestPayloadBindingError("Visual Drill V2 matrix must require independent repeated runtime executions")
    if not v2 and independent_repeat:
        raise DynamicRequestPayloadBindingError("V1 cannot enable V2-only independent-repeat semantics")
    receipts: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []
    for raw in raw_list:
        receipt, summary = _run_one(raw, godot, timeout, root, contract_data, process_runner, independent_repeat)
        receipts.append(receipt)
        summaries.append(summary)
    stats = _assert_visual_drill_matrix(receipts) if v2 else _assert_matrix_relationships(receipts)
    return {"receipts": receipts, "summaries": summaries, "contract_data": contract_data, "stats": stats}


def _assert_matrix_relationships(receipts: list[Mapping[str, Any]]) -> dict[str, int]:
    by_id = {str(item["request_identity"]["request_id"]): item for item in receipts}
    required_ids = {
        f"D-DYNAMIC-{ct.upper()}-BASE" for ct in SUPPORTED_TYPES
    } | {
        f"D-DYNAMIC-{ct.upper()}-SEED-CHANGE" for ct in SUPPORTED_TYPES
    } | {
        "D-DYNAMIC-VISUAL_LOOPS-MUSIC-ONLY",
        "D-DYNAMIC-VISUAL_LOOPS-VARIATION-ONLY",
        "D-DYNAMIC-VISUAL_LOOPS-DELIVERY-ONLY",
        "D-DYNAMIC-VISUAL_LOOPS-EDITORIAL-ONLY",
    }
    # A single custom request is allowed by the API; the default full matrix is audited below.
    if set(by_id) != required_ids:
        for record in receipts:
            if record["readiness"]["candidate_input_admissible"] is not False:
                raise DynamicRequestPayloadBindingError("Single-request receipt unexpectedly admits candidate input")
        return {"cases": len(receipts), "seed_isolation": 0, "orthogonality": 0}
    seed_checks = 0
    for content_type in SUPPORTED_TYPES:
        base = by_id[f"D-DYNAMIC-{content_type.upper()}-BASE"]
        varied = by_id[f"D-DYNAMIC-{content_type.upper()}-SEED-CHANGE"]
        if base["payload_evidence"]["visual_state_sha256"] == varied["payload_evidence"]["visual_state_sha256"]:
            raise DynamicRequestPayloadBindingError(f"Gameplay seed did not change {content_type} visual-state evidence")
        if base["request_identity"]["music_seed"] != varied["request_identity"]["music_seed"]:
            raise DynamicRequestPayloadBindingError("Gameplay-seed mutation unexpectedly changed music seed")
        seed_checks += 1
    loop_base = by_id["D-DYNAMIC-VISUAL_LOOPS-BASE"]
    loop_base_grammar = loop_base["payload_evidence"].get("grammar_parameter_evidence")
    if not isinstance(loop_base_grammar, Mapping):
        raise DynamicRequestPayloadBindingError("Base Visual Loop receipt lacks grammar-parameter evidence")
    seed_changed_loop = by_id["D-DYNAMIC-VISUAL_LOOPS-SEED-CHANGE"]
    seed_changed_grammar = seed_changed_loop["payload_evidence"].get("grammar_parameter_evidence")
    if not isinstance(seed_changed_grammar, Mapping) or seed_changed_grammar.get("parameter_instance_sha256") == loop_base_grammar.get("parameter_instance_sha256"):
        raise DynamicRequestPayloadBindingError("Gameplay seed did not change the pinned Loop grammar parameter instance")
    for suffix in ("MUSIC-ONLY", "VARIATION-ONLY", "DELIVERY-ONLY", "EDITORIAL-ONLY"):
        changed = by_id[f"D-DYNAMIC-VISUAL_LOOPS-{suffix}"]
        if loop_base["payload_evidence"]["visual_state_sha256"] != changed["payload_evidence"]["visual_state_sha256"]:
            raise DynamicRequestPayloadBindingError(f"{suffix.lower()} change leaked into visual-state evidence")
        if loop_base["payload_evidence"]["payload_sha256"] != changed["payload_evidence"]["payload_sha256"]:
            raise DynamicRequestPayloadBindingError(f"{suffix.lower()} change leaked into the current visual payload")
        if changed["payload_evidence"].get("grammar_parameter_evidence") != loop_base_grammar:
            raise DynamicRequestPayloadBindingError(f"{suffix.lower()} change leaked into grammar-parameter evidence")
        if loop_base["request_identity"]["request_binding_sha256"] == changed["request_identity"]["request_binding_sha256"]:
            raise DynamicRequestPayloadBindingError(f"{suffix.lower()} change was not retained by request binding identity")
    return {"cases": len(receipts), "seed_isolation": seed_checks, "orthogonality": 4}


def _load_raw_request(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise DynamicRequestPayloadBindingError(f"Cannot read canonical D9.9 request file: {exc}") from exc
    if not isinstance(value, dict):
        raise DynamicRequestPayloadBindingError("Canonical request-file root must be a JSON object")
    return value


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--godot", default=os.environ.get("C11D_GODOT_EXECUTABLE", ""), help="Godot 4.7.1 console executable")
    parser.add_argument("--timeout", type=int, default=120, help="Per-Godot-run timeout in seconds")
    parser.add_argument("--root", default=str(_root()), help="Repository root (defaults to this checkout)")
    parser.add_argument("--request-file", default="", help="Optional canonical D9.9 JSON request; otherwise run the 10-case V1 dynamic acceptance matrix")
    parser.add_argument("--visual-drill-matrix", action="store_true", help="Run the additive V2 20-pair Visual Drill selector/tier matrix through the existing binder; performs two independent real-Godot executions per pair")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    if not args.godot or not Path(args.godot).is_file():
        print("C11-D DYNAMIC REQUEST PAYLOAD BINDING FAIL | Godot console executable not found/configured | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
        return 2
    if args.timeout < 1 or args.timeout > 600:
        print("C11-D DYNAMIC REQUEST PAYLOAD BINDING FAIL | timeout must be in 1..600 seconds")
        return 2
    try:
        if args.visual_drill_matrix and args.request_file:
            raise DynamicRequestPayloadBindingError("--visual-drill-matrix cannot be combined with --request-file")
        mode = "visual_drill_v2" if args.visual_drill_matrix else "v1"
        data = _load_contract_for_mode(root, mode)
        raw_requests = [_load_raw_request(Path(args.request_file).resolve())] if args.request_file else None
        result = run_dynamic_request_matrix(
            args.godot, args.timeout, root, subprocess.run, raw_requests,
            mode=mode, independent_repeat=args.visual_drill_matrix,
        )
        receipts = result["receipts"]
        if args.visual_drill_matrix:
            stats = result["stats"]
            # Emit no receipt until the complete 20-pair matrix and all repeat checks passed.
            for receipt in receipts:
                print(DRILL_V2_RECEIPT_PREFIX + json.dumps(receipt, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
            print(
                "C11-D VISUAL DRILL DYNAMIC REQUEST PAYLOAD BINDING V2 PASS"
                + " | cases=20 | families=4/4 | selectors=20/20 | independent_runtime_repeat=20/20"
                + " | request_payload_manifest=20/20 | lineage_closure=20/20"
                + f" | source_pins={len(data[3])}/{len(data[3])} | fail_closed=ENFORCED"
                + " | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE"
            )
        elif raw_requests is not None:
            print("C11-D DYNAMIC REQUEST PAYLOAD BINDING RECEIPT=" + json.dumps(receipts[0], ensure_ascii=False, sort_keys=True, separators=(",", ":")))
            print("C11-D DYNAMIC REQUEST PAYLOAD BINDING PASS | cases=1 | selector_scope=PINNED_MATRIX_ONLY | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
        else:
            stats = result["stats"]
            for receipt in receipts:
                r = receipt["request_identity"]
                p = receipt["payload_evidence"]
                print("C11-D DYNAMIC REQUEST PAYLOAD RECEIPT=" + json.dumps({"request_id":r["request_id"],"content_type":r["content_type"],"gameplay_seed":r["gameplay_seed"],"music_seed":r["music_seed"],"variation_index":r["variation_index"],"delivery_profile_id":r["delivery_profile_id"],"payload_sha256":p["payload_sha256"],"visual_state_sha256":p["visual_state_sha256"],"payload_scope":p["payload_scope"],"exact_selector_payload_materialized":p["exact_selector_payload_materialized"],"grammar_parameter_evidence":p["grammar_parameter_evidence"],"request_binding_sha256":r["request_binding_sha256"],"request_payload_manifest_sha256":receipt["source_identity"]["request_payload_manifest_sha256"]},ensure_ascii=False,sort_keys=True,separators=(",", ":")))
            print("C11-D DYNAMIC REQUEST PAYLOAD BINDING PASS | cases=%d | selector_types=3/3 | gameplay_seed_binding=%d/3 | orthogonality=%d/4 | source_pins=%d/%d | request_payload_manifest=10/10 | lineage_closure=10/10 | longform=REJECTED | loop_grammar_instance=HARMONIC_MEMBRANE_COMPOSITE_MATERIALIZED | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE" % (stats["cases"], stats["seed_isolation"], stats["orthogonality"], len(data[3]), len(data[3])))
        return 0
    except Exception as exc:
        print("C11-D DYNAMIC REQUEST PAYLOAD BINDING FAIL | %s | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE" % str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
