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
MANIFEST_REL = Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")
CONTRACT_ID = "C11-D-RENDERER-DYNAMIC-REQUEST-PAYLOAD-BINDING-CONTRACT-V1"
INPUT_SCHEMA_ID = "C11-D-D9-DYNAMIC-REQUEST-PAYLOAD-INPUT-V1"
OUTPUT_SCHEMA_ID = "C11-D-D9-DYNAMIC-REQUEST-PAYLOAD-BINDING-V1"
PAYLOAD_MANIFEST_SCHEMA_ID = "C11-D-D9-REQUEST-PAYLOAD-MANIFEST-V1"
PAYLOAD_MANIFEST_STATUS = "PREPARATION_ONLY_REQUEST_BOUND_PAYLOAD_MANIFEST_NOT_RENDERER_INPUT"
GODOT_SUMMARY_SCHEMA_ID = "C11-D-D9-DYNAMIC-REQUEST-PAYLOAD-MATERIALIZATION-V1"
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


def _build_canonical_chain(raw: Mapping[str, Any], root: Path) -> dict[str, Any]:
    try:
        result = evaluate_universal_request(dict(raw), root)
        bridge = build_bridge_planning_record(result, root)
        envelope = prepare_d_only_adapter_envelope(result, bridge, root)
        source_binding = build_request_scoped_payload_binding(result, bridge, envelope, root)
        validate_request_scoped_payload_binding(source_binding, result, bridge, envelope, root)
    except Exception as exc:
        raise DynamicRequestPayloadBindingError(f"Canonical D9.9/D9.10/source-binding chain rejected request: {exc}") from exc
    if result.get("status") != "PLANNED":
        raise DynamicRequestPayloadBindingError("Canonical universal request did not produce PLANNED status")
    content_type = str(result.get("plan", {}).get("selection", {}).get("content_type", ""))
    if content_type not in EXPECTED_SELECTIONS or _canonical_selection(result["plan"]["selection"]) != EXPECTED_SELECTIONS[content_type]:
        raise DynamicRequestPayloadBindingError("Selector is outside the pinned request-to-payload matrix")
    request = result.get("canonical_request", {})
    if request.get("presentation_profile_id") != "social_default_v1":
        raise DynamicRequestPayloadBindingError("V1 admits only social_default_v1 presentation identity")
    if request.get("delivery_profile_id") not in ALLOWED_DELIVERY_PROFILES:
        raise DynamicRequestPayloadBindingError("V1 rejects Longform or non-admitted delivery profile identity")
    if request.get("seed") != int(raw.get("seed", -1)) or request.get("music_seed") != int(raw.get("music_seed", -1)):
        raise DynamicRequestPayloadBindingError("Canonical request changed a declared seed domain")
    return {"raw": dict(raw), "result": result, "bridge": bridge, "envelope": envelope, "source_binding": source_binding}


def _godot_input(chain: Mapping[str, Any]) -> dict[str, Any]:
    result = chain["result"]
    request = result["canonical_request"]
    data = {
        "schema": INPUT_SCHEMA_ID,
        "schema_version": "1.0",
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


def _validate_godot_summary(summary: Mapping[str, Any], chain: Mapping[str, Any]) -> None:
    result = chain["result"]
    req = result["canonical_request"]
    selection = _canonical_selection(result["plan"]["selection"])
    content_type = str(selection["content_type"])
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
        "schema": GODOT_SUMMARY_SCHEMA_ID,
        "schema_version": "1.0",
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
    for key, expected_value in expected.items():
        if summary.get(key) != expected_value:
            raise DynamicRequestPayloadBindingError(f"Godot summary mismatch at {key}: expected {expected_value!r}, got {summary.get(key)!r}")
    if not _is_sha(summary.get("payload_sha256")):
        raise DynamicRequestPayloadBindingError("Godot payload hash is malformed")
    if not _is_sha(summary.get("visual_state_sha256")):
        raise DynamicRequestPayloadBindingError("Godot visual-state hash is malformed")
    if set(summary) != set(expected) | {"payload_sha256", "visual_state_sha256", "grammar_parameter_evidence"}:
        raise DynamicRequestPayloadBindingError("Godot summary shape contains missing or unknown properties")


def _invoke_godot(chain: Mapping[str, Any], godot: str, timeout: int, root: Path, process_runner: Callable[..., Any]) -> dict[str, Any]:
    data = _godot_input(chain)
    encoded = base64.b64encode(_canonical(data).encode("utf-8")).decode("ascii")
    command = [godot, "--headless", "--path", str(root), "--script", "res://" + GODOT_HARNESS_REL.as_posix(), "--", encoded]
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
    _validate_godot_summary(summary, chain)
    return dict(summary)


def _build_receipt(chain: Mapping[str, Any], summary: Mapping[str, Any], root: Path, contract: Mapping[str, Any], lineage: list[dict[str, str]]) -> dict[str, Any]:
    result, bridge, envelope = chain["result"], chain["bridge"], chain["envelope"]
    request = result["canonical_request"]
    content_type = str(result["plan"]["selection"]["content_type"])
    expected_scope, exact = EXPECTED_SCOPE[content_type]
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
    payload_manifest: dict[str, Any] = {
        "schema": PAYLOAD_MANIFEST_SCHEMA_ID,
        "schema_version": "1.0",
        "status": PAYLOAD_MANIFEST_STATUS,
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
    receipt: dict[str, Any] = {
        "schema": OUTPUT_SCHEMA_ID,
        "schema_version": "1.0",
        "status": STATUS,
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
        "payload_evidence": {
            "payload_sha256": summary["payload_sha256"],
            "visual_state_sha256": summary["visual_state_sha256"],
            "payload_scope": expected_scope,
            "exact_selector_payload_materialized": exact,
            "deterministic_repeat_pass": True,
            "materialization": "IN_MEMORY_ONLY",
            "grammar_parameter_evidence": grammar_evidence,
            "request_payload_manifest_sha256": payload_manifest_sha256,
        },
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
    receipt["receipt_sha256"] = _sha_json(receipt)
    _validate_receipt(receipt, root)
    return receipt


def _validate_receipt(receipt: Mapping[str, Any], root: Path) -> bool:
    contract, _, schema, lineage = _load_contract(root)
    if set(receipt) != set(schema.get("required", [])):
        raise DynamicRequestPayloadBindingError("Receipt does not match strict output schema shape")
    if receipt.get("receipt_sha256") != _sha_json({key: value for key, value in receipt.items() if key != "receipt_sha256"}):
        raise DynamicRequestPayloadBindingError("Receipt SHA-256 mismatch")
    if receipt.get("schema") != OUTPUT_SCHEMA_ID or receipt.get("schema_version") != "1.0" or receipt.get("status") != STATUS:
        raise DynamicRequestPayloadBindingError("Receipt identity/status cannot be promoted")
    if receipt.get("frozen_c11c_manifest_sha256") != EXPECTED_MANIFEST_SHA256:
        raise DynamicRequestPayloadBindingError("Receipt immutable C11-C manifest pin mismatch")

    source = receipt.get("source_identity")
    identity = receipt.get("request_identity")
    evidence = receipt.get("payload_evidence")
    readiness = receipt.get("readiness")
    if not all(isinstance(item, Mapping) for item in (source, identity, evidence, readiness)):
        raise DynamicRequestPayloadBindingError("Receipt identity/evidence/readiness sections must be objects")
    content_type = str(identity.get("content_type", ""))
    if content_type not in EXPECTED_SELECTIONS:
        raise DynamicRequestPayloadBindingError("Receipt content type is outside the pinned selector matrix")
    if identity.get("selection") != EXPECTED_SELECTIONS[content_type] or identity.get("selection", {}).get("content_type") != content_type:
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
    if manifest.get("schema") != PAYLOAD_MANIFEST_SCHEMA_ID or manifest.get("schema_version") != "1.0" or manifest.get("status") != PAYLOAD_MANIFEST_STATUS:
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


def _run_one(raw: Mapping[str, Any], godot: str, timeout: int, root: Path, contract_data: tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[dict[str, str]]], process_runner: Callable[..., Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    contract, input_schema, output_schema, lineage = contract_data
    chain = _build_canonical_chain(raw, root)
    godot_input = _godot_input(chain)
    try:
        import jsonschema  # type: ignore
    except ImportError:
        jsonschema = None
    if jsonschema is not None:
        try:
            jsonschema.Draft202012Validator(input_schema).validate(godot_input)
        except Exception as exc:
            raise DynamicRequestPayloadBindingError(f"Godot input schema validation failed closed: {exc.message if hasattr(exc, 'message') else exc}") from exc
    summary = _invoke_godot(chain, godot, timeout, root, process_runner)
    receipt = _build_receipt(chain, summary, root, contract, lineage)
    return receipt, summary


def run_dynamic_request_matrix(
    godot: str,
    timeout: int = 120,
    project_root: Path | str | None = None,
    process_runner: Callable[..., Any] = subprocess.run,
    raw_requests: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    root = _root(project_root)
    contract_data = _load_contract(root)
    raw_list = raw_requests if raw_requests is not None else _matrix_raw_requests()
    receipts: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []
    for raw in raw_list:
        receipt, summary = _run_one(raw, godot, timeout, root, contract_data, process_runner)
        receipts.append(receipt)
        summaries.append(summary)
    _assert_matrix_relationships(receipts)
    return {"receipts": receipts, "summaries": summaries, "contract_data": contract_data}


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
    parser.add_argument("--request-file", default="", help="Optional canonical D9.9 JSON request; otherwise run the 10-case dynamic acceptance matrix")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    if not args.godot or not Path(args.godot).is_file():
        print("C11-D DYNAMIC REQUEST PAYLOAD BINDING FAIL | Godot console executable not found/configured | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
        return 2
    if args.timeout < 1 or args.timeout > 600:
        print("C11-D DYNAMIC REQUEST PAYLOAD BINDING FAIL | timeout must be in 1..600 seconds")
        return 2
    try:
        data = _load_contract(root)
        raw_requests = [_load_raw_request(Path(args.request_file).resolve())] if args.request_file else None
        result = run_dynamic_request_matrix(args.godot, args.timeout, root, subprocess.run, raw_requests)
        receipts = result["receipts"]
        if raw_requests is not None:
            print("C11-D DYNAMIC REQUEST PAYLOAD BINDING RECEIPT=" + json.dumps(receipts[0], ensure_ascii=False, sort_keys=True, separators=(",", ":")))
            print("C11-D DYNAMIC REQUEST PAYLOAD BINDING PASS | cases=1 | selector_scope=PINNED_MATRIX_ONLY | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
        else:
            stats = _assert_matrix_relationships(receipts)
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
