"""Source-pinned, renderer-neutral temporal topology proposal. Never creates a schedule instance or media."""
from __future__ import annotations
import copy, hashlib, json
from pathlib import Path
from typing import Any, Mapping

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_TEMPORAL_SCHEDULE_PROPOSAL_V1.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_TEMPORAL_SCHEDULE_PROPOSAL_SCHEMA_V1.json")
HIERARCHY_REL = Path("definitions/c11d/production/D_RENDERER_REGION_HIERARCHY_RECONCILIATION_V1.json")
MANIFEST_REL = Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")
CONTRACT_ID = "C11-D-RENDERER-TEMPORAL-SCHEDULE-PROPOSAL-CONTRACT-V1"
OUTPUT_SCHEMA = "C11-D-D9-RENDERER-TEMPORAL-TOPOLOGY-PROPOSAL-V1"
OUTPUT_STATUS = "PREPARATION_ONLY_TEMPORAL_TOPOLOGY_NOT_RENDERER_INPUT"
EXPECTED_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
SUPPORTED_CONTENT = ("challenges", "visual_loops", "visual_drills")

class DRendererTemporalScheduleError(ValueError):
    """Invalid timing source, proposal contract or attempted authority escalation."""

def _root(project_root: Path | str | None = None) -> Path:
    return Path(project_root).resolve() if project_root is not None else Path(__file__).resolve().parents[3]

def _read_json(root: Path, rel: Path) -> dict[str, Any]:
    try:
        value = json.loads((root / rel).read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise DRendererTemporalScheduleError(f"Cannot read JSON source {rel}: {exc}") from exc
    if not isinstance(value, dict):
        raise DRendererTemporalScheduleError(f"Expected object at {rel}")
    return value

def _sha(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except Exception as exc:
        raise DRendererTemporalScheduleError(f"Cannot hash required source {path}: {exc}") from exc

def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)

def _sha_json(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()

def _validate_inputs(root: Path) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, str]]]:
    contract = _read_json(root, CONTRACT_REL)
    schema = _read_json(root, SCHEMA_REL)
    if contract.get("schema") != CONTRACT_ID or contract.get("schema_version") != "1.0":
        raise DRendererTemporalScheduleError("Temporal proposal contract identity/version mismatch")
    if contract.get("status") != "PREPARATION_ONLY_TEMPORAL_TOPOLOGY_NOT_APPROVED_NOT_FROZEN":
        raise DRendererTemporalScheduleError("Temporal topology cannot self-approve or freeze")
    if contract.get("supported_content_types") != list(SUPPORTED_CONTENT):
        raise DRendererTemporalScheduleError("Temporal proposal scope changed")
    locks = contract.get("required_locks", {})
    expected_locks = {
        "source_adapter_mode": "PREPARE_ONLY", "temporal_topology_approved": False,
        "concrete_schedule_instantiated": False, "duration_values_emitted": False,
        "frame_indices_emitted": False, "frame_ranges_emitted": False,
        "pixel_coordinates_emitted": False, "renderer_native_input_emitted": False,
        "renderer_dispatch_invoked": False, "renderer_activation": False,
        "production_execution": False, "media_output_created": False,
        "output_artifact_path": None, "d4_8": "BLOCKED", "release_authority": "NONE",
        "c11c_source_mutation": False,
    }
    if locks != expected_locks:
        raise DRendererTemporalScheduleError("Temporal proposal governance locks mismatch")
    approval = contract.get("approval_state", {})
    expected_approval = {
        "temporal_topology_approved": False, "renderer_baseline_approved": False,
        "renderer_baseline_frozen": False, "d4_8_authorized": False,
        "d9_14_full_acceptance": "BLOCKED_AS_REQUIRED", "d9_16_full_acceptance": "BLOCKED_AS_REQUIRED",
        "d9_17_closure": "BLOCKED_NO_GO", "d10": "BLOCKED", "release_authority": "NONE",
    }
    if approval != expected_approval:
        raise DRendererTemporalScheduleError("Temporal proposal approval boundary mismatch")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or schema.get("$id") != "urn:c11d:renderer-temporal-schedule-proposal:v1" or schema.get("additionalProperties") is not False:
        raise DRendererTemporalScheduleError("Temporal output schema identity/strictness mismatch")
    if _sha(root / MANIFEST_REL) != EXPECTED_MANIFEST_SHA256 or contract.get("source_of_truth", {}).get("frozen_c11c_manifest_sha256") != EXPECTED_MANIFEST_SHA256:
        raise DRendererTemporalScheduleError("Frozen C11-C manifest pin mismatch")

    hierarchy = _read_json(root, HIERARCHY_REL)
    if hierarchy.get("schema") != "C11-D-RENDERER-REGION-HIERARCHY-RECONCILIATION-CONTRACT-V1" or hierarchy.get("status") != "PREPARATION_ONLY_RECONCILIATION_NOT_RENDERER_INPUT":
        raise DRendererTemporalScheduleError("Existing D1.5 region hierarchy reconciliation is missing or promoted")
    prior = hierarchy.get("previous_normalized_region_proposal", {})
    if prior.get("numeric_bounds_are_canonical") is not False or prior.get("may_drive_temporal_schedule") is not False:
        raise DRendererTemporalScheduleError("Unapproved normalized region proposal cannot drive temporal topology")
    spatial = contract.get("spatial_integration", {})
    if spatial.get("hierarchy_source") != str(HIERARCHY_REL).replace("\\", "/") or spatial.get("prior_normalized_permille_proposal_is_canonical") is not False or spatial.get("spatial_bounds_used_by_schedule") is not False:
        raise DRendererTemporalScheduleError("Spatial source hierarchy mismatch")

    source_entries = contract.get("source_of_truth", {}).get("timing_sources")
    if not isinstance(source_entries, list) or len(source_entries) != 11:
        raise DRendererTemporalScheduleError("Temporal source pin list must contain exactly 11 entries")
    lineage: list[dict[str, str]] = []
    seen: set[str] = set()
    for item in source_entries:
        if not isinstance(item, Mapping) or set(item) != {"path", "sha256"}:
            raise DRendererTemporalScheduleError("Malformed temporal source lineage entry")
        rel = str(item["path"])
        expected = str(item["sha256"])
        if rel in seen or len(expected) != 64:
            raise DRendererTemporalScheduleError("Duplicate or malformed temporal source pin")
        seen.add(rel)
        actual = _sha(root / rel)
        if actual != expected:
            raise DRendererTemporalScheduleError(f"Pinned temporal source changed: {rel}")
        lineage.append({"path": rel, "sha256": actual})

    # Source-level audit. Exact hashes above prevent silent temporal implementation drift.
    source_text = {
        rel: (root / rel).read_text(encoding="utf-8-sig")
        for rel in seen if rel.endswith((".gd", ".md"))
    }
    challenge = source_text["core/authoring/ChallengeTimeLiine.gd"]
    challenge_builder = source_text["core/execution/ChallengeTimelineBuilder.gd"]
    canonical = source_text["core/authoring/CanonicalV2Assembler.gd"]
    loop = source_text["core/authoring/VisualLoopTimeline.gd"]
    drill = source_text["core/authoring/VisualDrillTimeline.gd"]
    temporal = source_text["core/authoring/TemporalCore.gd"]
    loop_runtime = source_text["core/runtime/VisualLoopRuntime.gd"]
    drill_runtime = source_text["core/runtime/VisualDrillRuntime.gd"]
    marker_sets = [
        (challenge, ["class_name ChallengeTimeline", "hook_frames", "game_frames", "reveal_frames", "cta_frames", 'return "HOOK"', 'return "GAME"', 'return "REVEAL"', 'return "CTA"']),
        (challenge_builder, ['video_profile.get("fps")', 'phases.get("game_duration")', 'phases.get("hook_duration", 0.0)', 'phases.get("reveal_duration", 0.0)', 'phases.get("cta_duration", 0.0)']),
        (canonical, ['for key in ["hook_duration", "game_duration", "reveal_duration", "cta_duration"]', '"fps": int(video_profile.get("fps"))']),
        (loop, ["class_name VisualLoopTimeline", "total_frames = duration_to_frames(duration)", "return _current_frame % total_frames"]),
        (drill, ["class_name VisualDrillTimeline", "Phase semantics pending explicit JSON schema definition.", "total_frames = duration_to_frames(duration)"]),
        (temporal, ["func duration_to_frames(duration_seconds: float) -> int:", "int(round(duration_seconds * float(fps)))"]),
        (loop_runtime, ['not payload.has("duration") or not payload.has("fps") or not payload.has("frame_count")', "expected_frames != int(payload[\"frame_count\"])", "timeline = VisualLoopTimeline.new(duration, fps)"]),
        (drill_runtime, ['for required in ["duration", "fps", "frame_count", "exercise_parameters"', "expected_frames != int(payload[\"frame_count\"])", "timeline = VisualDrillTimeline.new(duration, fps)"]),
    ]
    for src, markers in marker_sets:
        for marker in markers:
            if marker not in src:
                raise DRendererTemporalScheduleError(f"Temporal implementation marker missing or drifted: {marker}")
    return contract, schema, lineage

def _expected_topology(content_type: str, contract: Mapping[str, Any]) -> dict[str, Any]:
    if content_type not in SUPPORTED_CONTENT:
        raise DRendererTemporalScheduleError("Unsupported content type; Longform and unknown values fail closed")
    model = contract.get("temporal_models", {}).get(content_type)
    if not isinstance(model, Mapping):
        raise DRendererTemporalScheduleError("No explicit temporal topology for content type")
    expected_keys = {"model", "timeline_class", "timeline_source", "phase_sequence", "sequence_authority", "duration_authority", "fps_authority", "frame_count_rule", "zero_length_policy", "subphase_policy"}
    if set(model) != expected_keys:
        raise DRendererTemporalScheduleError("Temporal model schema/field set mismatch")
    if content_type == "challenges":
        if model.get("phase_sequence") != ["HOOK", "GAME", "REVEAL", "CTA"] or model.get("timeline_class") != "ChallengeTimeline":
            raise DRendererTemporalScheduleError("Challenge phase topology does not match existing ChallengeTimeline")
        if model.get("duration_authority") != "RESOLVED_VIDEO_PROFILE_PHASE_DURATIONS" or model.get("fps_authority") != "RESOLVED_VIDEO_PROFILE_FPS":
            raise DRendererTemporalScheduleError("Challenge timeline values must stay bound to resolved video profile")
    else:
        if model.get("phase_sequence") != [] or model.get("timeline_class") not in ("VisualLoopTimeline", "VisualDrillTimeline"):
            raise DRendererTemporalScheduleError("Visual Loop/Drill cannot acquire invented engine subphases")
        if model.get("duration_authority") != "BOUND_PAYLOAD_DURATION_WITH_RUNTIME_FRAME_COUNT_CHECK" or model.get("fps_authority") != "BOUND_PAYLOAD_FPS":
            raise DRendererTemporalScheduleError("Visual Loop/Drill timing must stay bound to the validated payload")
    expected_model = {
        "model": model["model"], "timeline_class": model["timeline_class"], "timeline_source": model["timeline_source"],
        "phase_sequence": copy.deepcopy(model["phase_sequence"]), "sequence_authority": model["sequence_authority"],
        "duration_authority": model["duration_authority"], "fps_authority": model["fps_authority"],
        "frame_count_rule": model["frame_count_rule"], "zero_length_policy": model["zero_length_policy"],
        "subphase_policy": model["subphase_policy"], "schedule_state": "TOPOLOGY_ONLY_NO_INSTANCE",
    }
    if content_type == "visual_loops" and "loop" not in expected_model["model"].lower():
        raise DRendererTemporalScheduleError("Visual Loop model identity mismatch")
    if content_type == "visual_drills" and "drill" not in expected_model["model"].lower():
        raise DRendererTemporalScheduleError("Visual Drill model identity mismatch")
    return expected_model

def _without_hash(value: Mapping[str, Any]) -> dict[str, Any]:
    return {str(k): copy.deepcopy(v) for k, v in value.items() if k != "proposal_sha256"}

def _build_expected(content_type: str, root: Path, contract: Mapping[str, Any], schema: Mapping[str, Any], lineage: list[dict[str, str]]) -> dict[str, Any]:
    topology = _expected_topology(content_type, contract)
    spatial = {
        "hierarchy_source": str(HIERARCHY_REL).replace("\\", "/"),
        "D1_5_shared_frame_is_unchanged": True,
        "prior_normalized_permille_proposal_is_canonical": False,
        "spatial_bounds_used_by_schedule": False,
        "pixel_coordinates_emitted": False,
    }
    instantiation = {
        "concrete_schedule_instantiated": False,
        "duration_values_emitted": False,
        "frame_indices_emitted": False,
        "frame_ranges_emitted": False,
        "timeline_instantiated": False,
        "duration_state": "UNBOUND_PROPOSAL_NOT_APPROVED",
    }
    execution = {
        "source_adapter_mode": "PREPARE_ONLY", "renderer_native_input_emitted": False,
        "renderer_dispatch_invoked": False, "renderer_activation": False,
        "production_execution": False, "media_output_created": False,
        "output_artifact_path": None, "d4_8": "BLOCKED", "release_authority": "NONE",
        "c11c_source_mutation": False,
    }
    result: dict[str, Any] = {
        "schema": OUTPUT_SCHEMA, "schema_version": "1.0", "status": OUTPUT_STATUS,
        "content_type": content_type, "manifest_sha256": EXPECTED_MANIFEST_SHA256,
        "source_lineage": copy.deepcopy(lineage), "temporal_topology": topology,
        "spatial_integration": spatial, "instantiation": instantiation,
        "execution_boundary": execution,
    }
    result["proposal_sha256"] = _sha_json(result)
    return result

def build_temporal_schedule_proposal(content_type: str, project_root: Path | str | None = None) -> dict[str, Any]:
    root = _root(project_root)
    contract, schema, lineage = _validate_inputs(root)
    result = _build_expected(content_type, root, contract, schema, lineage)
    validate_temporal_schedule_proposal(result, project_root=root)
    return result

def validate_temporal_schedule_proposal(candidate: Mapping[str, Any], project_root: Path | str | None = None) -> None:
    if not isinstance(candidate, Mapping):
        raise DRendererTemporalScheduleError("Temporal proposal candidate must be a mapping")
    root = _root(project_root)
    contract, schema, lineage = _validate_inputs(root)
    expected = _build_expected(str(candidate.get("content_type")), root, contract, schema, lineage)
    if dict(candidate) != expected:
        raise DRendererTemporalScheduleError("Temporal proposal mismatch, source drift, invented timing, or authority escalation")
    required = schema.get("required", [])
    if set(candidate.keys()) != set(required):
        raise DRendererTemporalScheduleError("Temporal proposal output shape does not match strict schema")
    if _sha_json(_without_hash(candidate)) != candidate.get("proposal_sha256"):
        raise DRendererTemporalScheduleError("Temporal proposal SHA-256 mismatch")
    if candidate.get("manifest_sha256") != EXPECTED_MANIFEST_SHA256:
        raise DRendererTemporalScheduleError("Immutable C11-C manifest pin mismatch")
