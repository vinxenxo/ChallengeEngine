"""Request-scoped visual source binding audit; never materializes or renders payloads."""
from __future__ import annotations
import ast, copy, hashlib, json, re, sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from universal_producer import evaluate_universal_request
from editorial_render_bridge import build_bridge_planning_record, sha256 as bridge_sha256
from d_render_adapter import prepare_d_only_adapter_envelope, validate_d_only_adapter_envelope
from d_renderer_candidate import build_renderer_binding_preview, validate_renderer_binding_preview, sha256_json
from d_renderer_logical_composition import build_logical_composition_plan, validate_logical_composition_plan
from d_renderer_frame_program import build_renderer_neutral_frame_program, validate_renderer_neutral_frame_program
from d_renderer_temporal_bound_preview import build_temporal_bound_preview, validate_temporal_bound_preview
from d_renderer_delivery_timebase_projection import build_delivery_timebase_projection, validate_delivery_timebase_projection
from d_renderer_editorial_review_manifest import build_editorial_review_manifest, validate_editorial_review_manifest

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_REQUEST_SCOPED_PAYLOAD_BINDING_V1.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_REQUEST_SCOPED_PAYLOAD_BINDING_SCHEMA_V1.json")
MANIFEST_REL = Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")
CONTRACT_SCHEMA = "C11-D-RENDERER-REQUEST-SCOPED-PAYLOAD-BINDING-CONTRACT-V1"
OUTPUT_SCHEMA = "C11-D-D9-RENDERER-REQUEST-SCOPED-PAYLOAD-BINDING-V1"
STATUS = "PREPARATION_ONLY_REQUEST_SCOPED_PAYLOAD_BINDING_REVIEW_NOT_RENDERER_INPUT"
EXPECTED_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
SUPPORTED_TYPES = ("challenges", "visual_loops", "visual_drills")

class DRendererRequestScopedPayloadBindingError(ValueError):
    """Raised for selector/source drift, false instance claims, or governance escalation."""

def _root(project_root: Path | str | None = None) -> Path:
    return Path(project_root).resolve() if project_root is not None else Path(__file__).resolve().parents[3]

def _read_json(root: Path, rel: str | Path) -> dict[str, Any]:
    try:
        value = json.loads((root / rel).read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise DRendererRequestScopedPayloadBindingError(f"Cannot read JSON source {rel}: {exc}") from exc
    if not isinstance(value, dict):
        raise DRendererRequestScopedPayloadBindingError(f"Expected JSON object at {rel}")
    return value

def _sha_file(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except Exception as exc:
        raise DRendererRequestScopedPayloadBindingError(f"Cannot hash required source {path}: {exc}") from exc

def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)

def _sha(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()

def _without_hash(value: Mapping[str, Any]) -> dict[str, Any]:
    return {str(k): copy.deepcopy(v) for k, v in value.items() if k != "binding_sha256"}

def _assert_no_truth(value: Any, location: str = "request_scoped_payload_binding") -> None:
    forbidden = {"simulationresult", "simulation_result", "simulationtruth", "simulation_truth", "winning_frame", "winningframe", "close_calls", "closecalls", "derived_telemetry", "derivedtelemetry", "gameplay_rng", "structural_rng"}
    if isinstance(value, Mapping):
        for key, child in value.items():
            normalized = str(key).replace("-", "_").lower()
            if normalized in forbidden:
                raise DRendererRequestScopedPayloadBindingError(f"Forbidden truth/telemetry field in {location}: {key}")
            _assert_no_truth(child, f"{location}.{key}")
    elif isinstance(value, list):
        for i, child in enumerate(value):
            _assert_no_truth(child, f"{location}[{i}]")


def _load_contract(root: Path) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, str]]]:
    contract = _read_json(root, CONTRACT_REL)
    schema = _read_json(root, SCHEMA_REL)
    if contract.get("schema") != CONTRACT_SCHEMA or contract.get("schema_version") != "1.0":
        raise DRendererRequestScopedPayloadBindingError("Request-scoped payload-binding contract identity/version mismatch")
    if contract.get("status") != "PREPARATION_ONLY_SOURCE_RESOLUTION_NOT_PAYLOAD_MATERIALIZATION_NOT_RENDERER_INPUT":
        raise DRendererRequestScopedPayloadBindingError("Payload binding contract cannot self-promote")
    if contract.get("supported_content_types") != list(SUPPORTED_TYPES):
        raise DRendererRequestScopedPayloadBindingError("Supported content type contract drift")
    if contract.get("source_of_truth", {}).get("frozen_c11c_manifest_sha256") != EXPECTED_MANIFEST_SHA256 or _sha_file(root / MANIFEST_REL) != EXPECTED_MANIFEST_SHA256:
        raise DRendererRequestScopedPayloadBindingError("Frozen C11-C manifest mismatch")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or schema.get("$id") != "urn:c11d:renderer-request-scoped-payload-binding:v1" or schema.get("additionalProperties") is not False:
        raise DRendererRequestScopedPayloadBindingError("Output schema identity/strictness mismatch")
    expected_locks = {
        "in_memory_only": True, "payload_instance_materialized": False,
        "renderer_native_input_emitted": False, "renderer_dispatch_invoked": False,
        "renderer_activation": False, "production_execution": False,
        "media_output_created": False, "output_artifact_path": None,
        "d4_8": "BLOCKED", "release_authority": "NONE", "c11c_source_mutation": False,
    }
    if contract.get("required_locks") != expected_locks:
        raise DRendererRequestScopedPayloadBindingError("Payload binding governance locks mismatch")
    expected_approval = {
        "payload_binding_contract_approved": False, "selected_payload_instance_approved": False,
        "renderer_baseline_approved": False, "renderer_baseline_frozen": False,
        "d4_8_authorized": False, "d9_14_full_acceptance": "BLOCKED_AS_REQUIRED",
        "d9_16_full_acceptance": "BLOCKED_AS_REQUIRED", "d9_17_closure": "BLOCKED_NO_GO",
        "d10": "BLOCKED", "release_authority": "NONE",
    }
    if contract.get("approval_state") != expected_approval:
        raise DRendererRequestScopedPayloadBindingError("Payload binding cannot grant approval/freeze/authority")
    raw = contract.get("source_lineage")
    if not isinstance(raw, list) or len(raw) < 20:
        raise DRendererRequestScopedPayloadBindingError("Pinned source lineage is incomplete")
    lineage: list[dict[str, str]] = []
    seen: set[str] = set()
    for row in raw:
        if not isinstance(row, Mapping) or set(row) != {"path", "sha256"}:
            raise DRendererRequestScopedPayloadBindingError("Malformed source lineage row")
        rel = str(row["path"]); expected = str(row["sha256"])
        if rel in seen or len(expected) != 64:
            raise DRendererRequestScopedPayloadBindingError("Duplicate or malformed source lineage row")
        actual = _sha_file(root / rel)
        if actual != expected:
            raise DRendererRequestScopedPayloadBindingError(f"Pinned source drift: {rel}")
        seen.add(rel); lineage.append({"path": rel, "sha256": actual})
    if not lineage or lineage[0]["path"] != str(MANIFEST_REL).replace("\\", "/"):
        raise DRendererRequestScopedPayloadBindingError("Frozen C11-C manifest must be the first lineage entry")
    return contract, schema, lineage


LOOP_DEFINITION_BY_INTERNAL = {
    "geometric": "definitions/visual_loop_geometric_canonical.json",
    "fractal": "definitions/visual_loop_fractal_canonical.json",
    "sacred_symmetry": "definitions/visual_loop_kaleidoscope_canonical.json",
    "living_particles": "definitions/visual_loop_particle_flow_canonical.json",
    "invisible_forces": "definitions/visual_loop_vector_field_canonical.json",
}


def _resolve_selected_source(root: Path, result: Mapping[str, Any], registry: Mapping[str, Any], source_matrix: Mapping[str, Any]) -> dict[str, Any]:
    plan = result.get("plan"); request = result.get("canonical_request")
    if not isinstance(plan, Mapping) or not isinstance(request, Mapping):
        raise DRendererRequestScopedPayloadBindingError("Canonical request/plan pair is required")
    selection = plan.get("selection")
    if not isinstance(selection, Mapping) or request.get("selection") != dict(selection):
        raise DRendererRequestScopedPayloadBindingError("Canonical request selection and plan selection diverge")
    content_type = selection.get("content_type")
    if content_type not in SUPPORTED_TYPES:
        raise DRendererRequestScopedPayloadBindingError("Unknown/unsupported content type; Longform fails closed")
    # V1 only chains the three content examples for which existing temporal and review contracts have exact sources.
    expected_case = source_matrix.get(content_type)
    if not isinstance(expected_case, Mapping):
        raise DRendererRequestScopedPayloadBindingError("No approved-in-code V1 source-resolution case exists for this content type")
    for field, expected in expected_case.get("required_selection", {}).items():
        if selection.get(field) != expected:
            raise DRendererRequestScopedPayloadBindingError(f"V1 end-to-end timing/review reference does not cover selection.{field}={selection.get(field)!r}")
    registry_rel = Path("c11c-suite/c11c-producer/producer_schema.json")
    registry_sha = _sha_file(root / registry_rel)
    payload_rel = Path(str(expected_case["payload_source_path"]))
    payload = _read_json(root, payload_rel)
    payload_sha = _sha_file(root / payload_rel)
    common = {
        "registry_reference": {"path": registry_rel.as_posix(), "sha256": registry_sha},
        "definition_reference": {"path": payload_rel.as_posix(), "sha256": payload_sha},
        "request_seed": request.get("seed"),
        "request_variation_index": request.get("variation_index"),
        "definition_seed": payload.get("seed"),
        "definition_seed_matches_request": payload.get("seed") == request.get("seed"),
        "exact_request_payload_instance_materialized": False,
        "payload_instance_id": None,
        "payload_instance_sha256": None,
        "payload_output_path": None,
    }
    if content_type == "challenges":
        challenge_id = str(selection.get("variant_id"))
        if payload.get("challenge_id") != challenge_id or str(payload.get("mechanic")) != str(selection.get("family_id")):
            raise DRendererRequestScopedPayloadBindingError("Exact Challenge variant/mechanic does not match pinned source document")
        common.update({
            "source_class": "EXACT_CHALLENGE_DEFINITION",
            "resolved_identity": {"challenge_id": challenge_id, "mechanic": payload.get("mechanic"), "asset_family": payload.get("asset_family"), "video_profile": payload.get("video_profile")},
            "selection_resolution_state": "EXACT_CHALLENGE_SOURCE_RESOLVED_RUNTIME_MEDIA_PAYLOAD_NOT_MATERIALIZED",
            "definition_matches_selection": True,
            "selected_grammar_materialized": False,
            "selected_tier_materialized": False,
            "d4_subplan_status": result.get("d4_evidence", {}).get("status") if isinstance(result.get("d4_evidence"), Mapping) else None,
            "definition_payload_summary": {"source_fps": payload.get("video", {}).get("fps") if isinstance(payload.get("video"), Mapping) else None, "source_timeline_fields": ["hook_duration", "game_duration", "reveal_duration", "cta_duration"]},
        })
    elif content_type == "visual_loops":
        family_id = str(selection.get("family_id")); grammar_id = str(selection.get("subtype_id"))
        declaration = registry.get("families", {}).get(family_id)
        if not isinstance(declaration, Mapping): raise DRendererRequestScopedPayloadBindingError("Selected Visual Loop family is absent from canonical producer registry")
        internal = str(declaration.get("internal", ""))
        grammars = declaration.get("grammars")
        if not isinstance(grammars, list) or not any(isinstance(row, list) and len(row) >= 2 and row[0] == grammar_id for row in grammars):
            raise DRendererRequestScopedPayloadBindingError("Selected Visual Loop grammar is absent from the canonical producer registry")
        if grammar_id == "auto": raise DRendererRequestScopedPayloadBindingError("AUTO is not a concrete grammar identity for an exact-instance review")
        parameters = payload.get("payload", {}).get("visual_parameters", {}) if isinstance(payload.get("payload"), Mapping) else {}
        generator = parameters.get("generator") if isinstance(parameters, Mapping) else None
        if payload.get("kind") != "visual_loop" or generator != internal or LOOP_DEFINITION_BY_INTERNAL.get(internal) != payload_rel.as_posix():
            raise DRendererRequestScopedPayloadBindingError("Visual Loop canonical family reference does not match the selected backend family")
        common.update({
            "source_class": "FAMILY_CANONICAL_VISUAL_LOOP_DEFINITION_NOT_GRAMMAR_INSTANCE",
            "resolved_identity": {"family_id": family_id, "family_internal_id": internal, "selected_grammar_id": grammar_id, "definition_subtype": payload.get("subtype"), "generator_id": generator},
            "selection_resolution_state": "FAMILY_SOURCE_RESOLVED_EXACT_GRAMMAR_PAYLOAD_INSTANCE_REQUIRED",
            "definition_matches_selection": True,
            "selected_grammar_materialized": False,
            "selected_tier_materialized": False,
            "d4_subplan_status": None,
            "definition_payload_summary": {"source_fps": payload.get("payload", {}).get("fps"), "duration_seconds": payload.get("payload", {}).get("duration"), "frame_count": payload.get("payload", {}).get("frame_count"), "canonical_loop_seamless": payload.get("payload", {}).get("loop", {}).get("seamless") if isinstance(payload.get("payload", {}).get("loop"), Mapping) else None},
        })
    else:
        family_id = str(selection.get("family_id")); variant_id = str(selection.get("variant_id")); tier_match = re.fullmatch(r"tier-([1-9][0-9]*)", variant_id)
        if not tier_match: raise DRendererRequestScopedPayloadBindingError("Visual Drill requires an explicit tier-N selection")
        requested_tier = int(tier_match.group(1))
        declaration = registry.get("drills", {}).get(family_id)
        if not isinstance(declaration, Mapping): raise DRendererRequestScopedPayloadBindingError("Selected Visual Drill type is absent from the canonical producer registry")
        tiers = declaration.get("difficulty_values")
        if not isinstance(tiers, list) or requested_tier not in tiers: raise DRendererRequestScopedPayloadBindingError("Selected Visual Drill tier is absent from canonical producer registry")
        exercise = payload.get("payload", {}).get("exercise_parameters", {}) if isinstance(payload.get("payload"), Mapping) else {}
        generator = exercise.get("generator") if isinstance(exercise, Mapping) else None
        definition_tier = exercise.get("difficulty_tier") if isinstance(exercise, Mapping) else None
        if payload.get("kind") != "visual_drill" or generator != str(declaration.get("internal", family_id)):
            raise DRendererRequestScopedPayloadBindingError("Visual Drill canonical source does not match selected drill type")
        common.update({
            "source_class": "DRILL_TYPE_CANONICAL_DEFINITION_NOT_REQUEST_INSTANCE",
            "resolved_identity": {"drill_type_id": family_id, "selected_tier": requested_tier, "definition_tier": definition_tier, "generator_id": generator},
            "selection_resolution_state": "DRILL_TYPE_SOURCE_RESOLVED_REQUEST_TIER_SEED_PAYLOAD_INSTANCE_REQUIRED",
            "definition_matches_selection": True,
            "selected_grammar_materialized": False,
            "selected_tier_materialized": definition_tier == requested_tier,
            "d4_subplan_status": None,
            "definition_payload_summary": {"source_fps": payload.get("payload", {}).get("fps"), "duration_seconds": payload.get("payload", {}).get("duration"), "frame_count": payload.get("payload", {}).get("frame_count"), "definition_seed_matches_request": payload.get("seed") == request.get("seed")},
        })
    return common


def _build_core(result: Mapping[str, Any], bridge_record: Mapping[str, Any], adapter_envelope: Mapping[str, Any], root: Path, contract: Mapping[str, Any], schema: Mapping[str, Any], lineage: list[dict[str, str]]) -> dict[str, Any]:
    if not isinstance(result, Mapping) or result.get("status") != "PLANNED": raise DRendererRequestScopedPayloadBindingError("Requires successful canonical D9.9 PLANNED result")
    # Rebuild and compare each handoff; a detached/forged bridge or adapter is never accepted.
    expected_bridge = build_bridge_planning_record(result, root)
    if dict(bridge_record) != expected_bridge: raise DRendererRequestScopedPayloadBindingError("D9.10 bridge does not exactly match canonical D9.9 result")
    expected_envelope = prepare_d_only_adapter_envelope(result, bridge_record, root)
    if dict(adapter_envelope) != expected_envelope: raise DRendererRequestScopedPayloadBindingError("PREPARE_ONLY adapter envelope does not match canonical request/bridge")
    validate_d_only_adapter_envelope(adapter_envelope, root)

    content_type = result.get("plan", {}).get("selection", {}).get("content_type")
    if content_type not in SUPPORTED_TYPES: raise DRendererRequestScopedPayloadBindingError("Unknown/unsupported content type; Longform fails closed")
    binding_preview = build_renderer_binding_preview(adapter_envelope, root)
    validate_renderer_binding_preview(binding_preview, adapter_envelope, root)
    composition = build_logical_composition_plan(binding_preview, adapter_envelope, root)
    validate_logical_composition_plan(composition, binding_preview, adapter_envelope, root)
    frame_program = build_renderer_neutral_frame_program(composition, binding_preview, adapter_envelope, root)
    validate_renderer_neutral_frame_program(frame_program, composition, binding_preview, adapter_envelope, root)
    temporal = build_temporal_bound_preview(str(content_type), root)
    validate_temporal_bound_preview(temporal, root)
    delivery_id = str(result.get("canonical_request", {}).get("delivery_profile_id"))
    projection = build_delivery_timebase_projection(str(content_type), delivery_id, root)
    validate_delivery_timebase_projection(projection, str(content_type), delivery_id, root)
    review = build_editorial_review_manifest(result, bridge_record, adapter_envelope, root)
    validate_editorial_review_manifest(review, result, bridge_record, adapter_envelope, root)

    registry_rel = Path("c11c-suite/c11c-producer/producer_schema.json")
    registry = _read_json(root, registry_rel)
    source_matrix = contract.get("representative_source_matrix", {})
    resolved = _resolve_selected_source(root, result, registry, source_matrix)
    selection = dict(result["plan"]["selection"])
    request = result["canonical_request"]
    identity = {
        "request_id": request.get("request_id"),
        "request_hash": result.get("request_hash"),
        "plan_hash": result.get("plan_hash"),
        "editorial_hash": result.get("editorial_hash"),
        "bridge_record_hash": bridge_record.get("record_hash"),
        "adapter_envelope_hash": adapter_envelope.get("envelope_hash"),
        "binding_preview_sha256": binding_preview.get("preview_sha256"),
        "logical_composition_sha256": composition.get("composition_sha256"),
        "frame_program_sha256": frame_program.get("program_sha256"),
        "temporal_preview_sha256": temporal.get("preview_sha256"),
        "delivery_projection_sha256": projection.get("projection_sha256"),
        "editorial_review_manifest_sha256": review.get("review_manifest_sha256"),
        "definition_source_sha256": resolved.get("definition_reference", {}).get("sha256"),
        "registry_sha256": resolved.get("registry_reference", {}).get("sha256"),
        "contract_sha256": _sha_file(root / CONTRACT_REL),
        "schema_sha256": _sha_file(root / SCHEMA_REL),
        "implementation_sha256": _sha_file(Path(__file__).resolve()),
        "source_lineage_sha256": _sha(lineage),
        "frozen_c11c_manifest_sha256": EXPECTED_MANIFEST_SHA256,
    }
    unresolved = [
        "REQUEST_SCOPED_VISUAL_PAYLOAD_INSTANCE_ID_AND_SHA256_NOT_MATERIALIZED",
        "VISUAL_PARAMETER_GENERATION_AND_SOURCE_INSTANCE_BINDING_NOT_EXECUTED",
        "SIMULATION_FRAME_SAMPLING_AND_INTERPOLATION_UNRESOLVED_NOT_EMITTED",
        "PER_FIELD_EDITORIAL_VISIBILITY_FRAME_WINDOWS_UNRESOLVED_NOT_EMITTED",
        "SEMANTIC_REGION_AND_TEMPORAL_TOPOLOGY_APPROVAL_NOT_GRANTED",
    ]
    if content_type == "visual_loops": unresolved.insert(0, "EXACT_SELECTED_GRAMMAR_INSTANCE_NOT_MATERIALIZED_BY_D9_9_PLAN_ONLY_ROUTE")
    elif content_type == "visual_drills": unresolved.insert(0, "REQUEST_SPECIFIC_DRILL_PAYLOAD_AND_PARAMETER_INSTANCE_NOT_MATERIALIZED")
    else: unresolved.insert(0, "CHALLENGE_SIMULATION_RUNTIME_PAYLOAD_NOT_MATERIALIZED_BY_REVIEW_CHAIN")
    out: dict[str, Any] = {
        "schema": OUTPUT_SCHEMA,
        "schema_version": "1.0",
        "status": STATUS,
        "frozen_c11c_manifest_sha256": EXPECTED_MANIFEST_SHA256,
        "content_type": content_type,
        "source_identity": identity,
        "content_selection": {
            "selection": copy.deepcopy(selection),
            "gameplay_seed": request.get("seed"),
            "music_seed": request.get("music_seed"),
            "variation_index": request.get("variation_index"),
            "presentation_profile_id": request.get("presentation_profile_id"),
            "delivery_profile_id": delivery_id,
        },
        "source_binding": resolved,
        "unresolved_requirements": unresolved,
        "readiness": {
            "canonical_selection_resolved": True,
            "source_definition_hash_bound": True,
            "selected_family_or_variant_reference_resolved": True,
            "request_scoped_visual_payload_instance_bound": False,
            "payload_instance_materialized": False,
            "editorial_review_chain_passed": True,
            "video_render_ready": False,
        },
        "execution_boundary": {
            "mode": "IN_MEMORY_SOURCE_BINDING_REVIEW_ONLY",
            "source_adapter_mode": "PREPARE_ONLY",
            "renderer_native_input_emitted": False,
            "renderer_dispatch_invoked": False,
            "renderer_activation": False,
            "production_execution": False,
            "media_output_created": False,
            "output_artifact_path": None,
            "d4_8": "BLOCKED",
            "release_authority": "NONE",
            "c11c_source_mutation": False,
        },
    }
    out["binding_sha256"] = _sha(out)
    _assert_no_truth(out)
    return out


def build_request_scoped_payload_binding(result: Mapping[str, Any], bridge_record: Mapping[str, Any], adapter_envelope: Mapping[str, Any], project_root: Path | str | None = None) -> dict[str, Any]:
    root = _root(project_root)
    contract, schema, lineage = _load_contract(root)
    out = _build_core(result, bridge_record, adapter_envelope, root, contract, schema, lineage)
    validate_request_scoped_payload_binding(out, result, bridge_record, adapter_envelope, root)
    return out


def validate_request_scoped_payload_binding(candidate: Mapping[str, Any], result: Mapping[str, Any], bridge_record: Mapping[str, Any], adapter_envelope: Mapping[str, Any], project_root: Path | str | None = None) -> bool:
    if not isinstance(candidate, Mapping): raise DRendererRequestScopedPayloadBindingError("Payload binding candidate must be a mapping")
    root = _root(project_root)
    contract, schema, lineage = _load_contract(root)
    expected = _build_core(result, bridge_record, adapter_envelope, root, contract, schema, lineage)
    if dict(candidate) != expected: raise DRendererRequestScopedPayloadBindingError("Payload binding differs from canonical request/source chain or governance locks")
    if set(candidate) != set(schema.get("required", [])): raise DRendererRequestScopedPayloadBindingError("Payload binding output shape does not match strict schema")
    if _sha(_without_hash(candidate)) != candidate.get("binding_sha256"): raise DRendererRequestScopedPayloadBindingError("Request-scoped binding SHA-256 mismatch")
    if candidate.get("frozen_c11c_manifest_sha256") != EXPECTED_MANIFEST_SHA256: raise DRendererRequestScopedPayloadBindingError("Frozen C11-C manifest pin mismatch")
    if candidate.get("readiness", {}).get("request_scoped_visual_payload_instance_bound") is not False or candidate.get("readiness", {}).get("video_render_ready") is not False: raise DRendererRequestScopedPayloadBindingError("Review binding may not claim concrete payload/render readiness")
    _assert_no_truth(candidate)
    return True
