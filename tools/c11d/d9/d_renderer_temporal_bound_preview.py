"""Source-pinned renderer-neutral temporal preview. No engine, renderer or media side effects."""
from __future__ import annotations
import copy, hashlib, json, math
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from d_renderer_temporal_schedule import build_temporal_schedule_proposal, DRendererTemporalScheduleError

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_TEMPORAL_BOUND_PREVIEW_V1.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_TEMPORAL_BOUND_PREVIEW_SCHEMA_V1.json")
MANIFEST_REL = Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")
CONTRACT_ID = "C11-D-RENDERER-TEMPORAL-BOUND-PREVIEW-CONTRACT-V1"
OUTPUT_SCHEMA = "C11-D-D9-RENDERER-TEMPORAL-BOUND-PREVIEW-V1"
OUTPUT_STATUS = "PREPARATION_ONLY_TEMPORAL_REVIEW_PREVIEW_NOT_RENDERER_INPUT"
EXPECTED_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
SUPPORTED_TYPES = ("challenges", "visual_loops", "visual_drills")

class DRendererTemporalBoundPreviewError(ValueError):
    """Invalid timing source, stale lineage, schema drift or governance escalation."""

def _root(project_root: Path | str | None = None) -> Path:
    return Path(project_root).resolve() if project_root is not None else Path(__file__).resolve().parents[3]

def _read_json(root: Path, rel: str | Path) -> dict[str, Any]:
    try:
        value = json.loads((root / rel).read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise DRendererTemporalBoundPreviewError(f"Cannot read JSON source {rel}: {exc}") from exc
    if not isinstance(value, dict):
        raise DRendererTemporalBoundPreviewError(f"Expected JSON object at {rel}")
    return value

def _sha_file(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except Exception as exc:
        raise DRendererTemporalBoundPreviewError(f"Cannot hash required source {path}: {exc}") from exc

def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)

def _sha_json(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()

def _without_hash(value: Mapping[str, Any]) -> dict[str, Any]:
    return {str(key): copy.deepcopy(item) for key, item in value.items() if key != "preview_sha256"}

def _godot_duration_to_frames(duration_seconds: float, fps: int) -> int:
    """Match TemporalCore's nonnegative round-to-nearest frame conversion, not Python bankers-rounding."""
    if isinstance(duration_seconds, bool) or not isinstance(duration_seconds, (int, float)) or not math.isfinite(float(duration_seconds)) or duration_seconds < 0:
        raise DRendererTemporalBoundPreviewError("Duration must be finite and nonnegative")
    if isinstance(fps, bool) or not isinstance(fps, int) or fps <= 0:
        raise DRendererTemporalBoundPreviewError("FPS must be a positive integer")
    return max(0, int(math.floor(float(duration_seconds) * fps + 0.5)))

def _load_contract(root: Path) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, str]]]:
    contract = _read_json(root, CONTRACT_REL)
    schema = _read_json(root, SCHEMA_REL)
    if contract.get("schema") != CONTRACT_ID or contract.get("schema_version") != "1.0":
        raise DRendererTemporalBoundPreviewError("Temporal bound-preview contract identity/version mismatch")
    if contract.get("status") != "PREPARATION_ONLY_SOURCE_BOUND_TEMPORAL_PREVIEW_NOT_APPROVED_NOT_FROZEN":
        raise DRendererTemporalBoundPreviewError("Temporal bound preview may not approve or freeze itself")
    if _sha_file(root / MANIFEST_REL) != EXPECTED_MANIFEST_SHA256 or contract.get("source_of_truth", {}).get("frozen_c11c_manifest_sha256") != EXPECTED_MANIFEST_SHA256:
        raise DRendererTemporalBoundPreviewError("Frozen C11-C manifest pin mismatch")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or schema.get("$id") != "urn:c11d:renderer-temporal-bound-preview:v1" or schema.get("additionalProperties") is not False:
        raise DRendererTemporalBoundPreviewError("Temporal preview output schema identity/strictness mismatch")
    expected_locks = {
        "source_adapter_mode":"PREPARE_ONLY", "review_preview_only":True,
        "renderer_native_input_emitted":False, "renderer_dispatch_invoked":False,
        "renderer_activation":False, "production_execution":False, "media_output_created":False,
        "output_artifact_path":None, "d4_8":"BLOCKED", "release_authority":"NONE", "c11c_source_mutation":False,
    }
    if contract.get("required_locks") != expected_locks:
        raise DRendererTemporalBoundPreviewError("Temporal preview governance locks mismatch")
    expected_approval = {
        "temporal_topology_approved":False, "temporal_preview_approved":False,
        "renderer_baseline_approved":False, "renderer_baseline_frozen":False, "d4_8_authorized":False,
        "d9_14_full_acceptance":"BLOCKED_AS_REQUIRED", "d9_16_full_acceptance":"BLOCKED_AS_REQUIRED",
        "d9_17_closure":"BLOCKED_NO_GO", "d10":"BLOCKED", "release_authority":"NONE",
    }
    if contract.get("approval_state") != expected_approval:
        raise DRendererTemporalBoundPreviewError("Temporal preview approval boundary mismatch")
    entries = contract.get("source_of_truth", {}).get("source_lineage")
    if not isinstance(entries, list) or len(entries) != 15:
        raise DRendererTemporalBoundPreviewError("Source lineage must contain exactly 15 pins")
    lineage: list[dict[str, str]] = []
    seen: set[str] = set()
    for entry in entries:
        if not isinstance(entry, Mapping) or set(entry) != {"path", "sha256"}:
            raise DRendererTemporalBoundPreviewError("Malformed source lineage entry")
        rel, expected = str(entry["path"]), str(entry["sha256"])
        if rel in seen or len(expected) != 64:
            raise DRendererTemporalBoundPreviewError("Duplicate or malformed source lineage entry")
        actual = _sha_file(root / rel)
        if actual != expected:
            raise DRendererTemporalBoundPreviewError(f"Pinned source drift: {rel}")
        seen.add(rel)
        lineage.append({"path":rel,"sha256":actual})
    if entries[0].get("path") != str(MANIFEST_REL).replace("\\", "/"):
        raise DRendererTemporalBoundPreviewError("Manifest must be the first source-lineage entry")
    registered = contract.get("registered_review_sources", {})
    expected_sources = {
        "challenges":"challenges/CHALLENGE_004.json",
        "visual_loops":"definitions/visual_loop_geometric_canonical.json",
        "visual_drills":"definitions/visual_drill_tracking_canonical.json",
    }
    if set(registered) != set(SUPPORTED_TYPES) or {k:v.get("path") for k,v in registered.items() if isinstance(v, Mapping)} != expected_sources:
        raise DRendererTemporalBoundPreviewError("Registered review-source matrix changed without implementation review")
    rules = contract.get("preview_rules", {})
    expected_rules = {
        "in_memory_only":True, "frame_index_convention":"ZERO_BASED_HALF_OPEN",
        "segment_order":"SOURCE_TIMELINE_ORDER", "segment_start":"PREVIOUS_SEGMENT_END_FRAME_EXCLUSIVE",
        "segment_end":"START_FRAME_PLUS_FRAME_COUNT",
        "duration_to_frames":"MAX_ZERO_INT_ROUND_NONNEGATIVE_SECONDS_TIMES_FPS_MATCHING_GODOT_TEMPORALCORE",
        "visual_payload_frame_count":"MUST_EQUAL_DURATION_TO_FRAMES_RESULT; NO_REPAIR_OR_MUTATION",
        "challenge_phase_duration":"EACH_SOURCE_PHASE_ROUNDED_SEPARATELY_BEFORE_SUMMING; DO_NOT_ROUND_ONLY_TOTAL_DURATION",
        "declared_total_duration":"NOT_A_TIMELINE_AUTHORITY; ONLY_EXPLICIT_PHASE_DURATIONS_DEFINE_CHALLENGE_SPAN",
        "spatial_geometry":"D1.5_AND_REGION_HIERARCHY_REMAIN_SPATIAL_AUTHORITY; NO_COORDINATES_IN_PREVIEW",
        "topology_approval":"NOT_GRANTED", "renderer_native_input":False, "renderer_dispatch":False, "media_creation":False,
    }
    if rules != expected_rules:
        raise DRendererTemporalBoundPreviewError("Temporal preview rule set changed without implementation review")
    return contract, schema, lineage

def _finite_seconds(value: Any, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(float(value)) or value < 0:
        raise DRendererTemporalBoundPreviewError(f"{name} must be a finite nonnegative number")
    return float(value)

def _positive_fps(value: Any) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise DRendererTemporalBoundPreviewError("Source FPS must be a positive integer")
    return value

def _segment(segment_id: str, duration: float, start: int, count: int) -> dict[str, Any]:
    return {
        "segment_id": segment_id,
        "source_duration_seconds": duration,
        "start_frame": start,
        "end_frame_exclusive": start + count,
        "frame_count": count,
        "enabled": count > 0,
    }

def _build_preview(content_type: str, root: Path, contract: Mapping[str, Any], schema: Mapping[str, Any], lineage: list[dict[str, str]]) -> dict[str, Any]:
    if content_type not in SUPPORTED_TYPES:
        raise DRendererTemporalBoundPreviewError("Unsupported content type; Longform and unknown types fail closed")
    spec = contract["registered_review_sources"][content_type]
    rel = str(spec["path"])
    source = _read_json(root, rel)
    source_hash = _sha_file(root / rel)
    topology = build_temporal_schedule_proposal(content_type, root)
    topology_info = topology.get("temporal_topology", {})
    expected_model = str(spec["model"])
    if topology_info.get("model") != expected_model or topology.get("status") != "PREPARATION_ONLY_TEMPORAL_TOPOLOGY_NOT_RENDERER_INPUT":
        raise DRendererTemporalBoundPreviewError("Upstream topology proposal disagrees with the bound timing source")

    segments: list[dict[str, Any]] = []
    source_id: str
    subtype: str | None = None
    declared_frame_count: int | None = None
    duration_authority = str(spec["duration_authority"])
    cursor = 0
    if content_type == "challenges":
        source_id = str(source.get("challenge_id", ""))
        if source_id != spec.get("expected_source_id"):
            raise DRendererTemporalBoundPreviewError("Challenge timing fixture identity mismatch")
        video = source.get("video")
        if not isinstance(video, Mapping):
            raise DRendererTemporalBoundPreviewError("Challenge fixture requires its existing inline video timing object")
        fps = _positive_fps(video.get("fps"))
        durations: list[tuple[str, float]] = []
        fields = spec.get("duration_fields")
        segment_ids = spec.get("segment_ids")
        if not isinstance(fields, list) or not isinstance(segment_ids, list) or len(fields) != 4 or len(segment_ids) != 4:
            raise DRendererTemporalBoundPreviewError("Challenge phase field/segment contract mismatch")
        for field, segment_id in zip(fields, segment_ids):
            if field not in video:
                raise DRendererTemporalBoundPreviewError(f"Challenge source phase duration is absent: {field}")
            duration = _finite_seconds(video[field], field)
            count = _godot_duration_to_frames(duration, fps)
            segments.append(_segment(str(segment_id), duration, cursor, count))
            cursor += count
            durations.append((str(field), duration))
        duration_sum = sum(value for _, value in durations)
        if duration_sum <= 0 or cursor <= 0:
            raise DRendererTemporalBoundPreviewError("Challenge timeline must contain a positive-duration span")
    else:
        expected_kind = spec.get("expected_kind")
        if source.get("kind") != expected_kind:
            raise DRendererTemporalBoundPreviewError("Canonical visual payload kind does not match registered content type")
        payload = source.get("payload")
        if not isinstance(payload, Mapping):
            raise DRendererTemporalBoundPreviewError("Canonical visual payload timing object is missing")
        subtype = source.get("subtype") if isinstance(source.get("subtype"), str) else None
        source_id = Path(rel).stem
        fps = _positive_fps(payload.get("fps"))
        duration = _finite_seconds(payload.get("duration"), "payload.duration")
        if duration <= 0:
            raise DRendererTemporalBoundPreviewError("Visual payload duration must be positive")
        raw_count = payload.get(spec.get("frame_count_field"))
        if isinstance(raw_count, bool) or not isinstance(raw_count, int) or raw_count <= 0:
            raise DRendererTemporalBoundPreviewError("Visual payload frame_count must be a positive integer")
        expected_count = _godot_duration_to_frames(duration, fps)
        if raw_count != expected_count:
            raise DRendererTemporalBoundPreviewError(f"Canonical payload frame_count mismatch: declared={raw_count}, expected={expected_count}")
        declared_frame_count = raw_count
        count = expected_count
        segments.append(_segment(str(spec["segment_id"]), duration, 0, count))
        cursor = count
        duration_sum = duration

    if not segments or cursor <= 0:
        raise DRendererTemporalBoundPreviewError("Bound preview has no positive temporal span")
    if segments[0]["start_frame"] != 0:
        raise DRendererTemporalBoundPreviewError("First frame segment must start at frame zero")
    for i, item in enumerate(segments):
        if item["frame_count"] != item["end_frame_exclusive"] - item["start_frame"]:
            raise DRendererTemporalBoundPreviewError("Segment frame count/end-bound mismatch")
        if i and item["start_frame"] != segments[i - 1]["end_frame_exclusive"]:
            raise DRendererTemporalBoundPreviewError("Segment ranges must be contiguous and non-overlapping")
    if segments[-1]["end_frame_exclusive"] != cursor:
        raise DRendererTemporalBoundPreviewError("Segment list does not cover the complete temporal span")

    implementation_path = Path(__file__).resolve()
    out: dict[str, Any] = {
        "schema": OUTPUT_SCHEMA,
        "schema_version": "1.0",
        "status": OUTPUT_STATUS,
        "content_type": content_type,
        "manifest_sha256": EXPECTED_MANIFEST_SHA256,
        "topology_proposal_sha256": topology["proposal_sha256"],
        "source_lineage": copy.deepcopy(lineage),
        "source_identity": {
            "source_path": rel,
            "source_id": source_id,
            "subtype": subtype,
            "source_sha256": source_hash,
        },
        "temporal_schedule": {
            "model": expected_model,
            "fps": fps,
            "frame_index_convention": "ZERO_BASED_HALF_OPEN",
            "total_frames": cursor,
            "source_duration_sum_seconds": duration_sum,
            "frame_span_duration_seconds": cursor / fps,
            "source_declared_frame_count": declared_frame_count,
            "segments": segments,
        },
        "schedule_validation": {
            "frame_count_rule_validated": True,
            "segment_ranges_contiguous": True,
            "segments_cover_total_span": True,
            "phase_order_source_grounded": True,
            "topology_approved": False,
            "subphases_inferred": False,
            "simulation_truth_used": False,
            "winning_frame_used": False,
            "close_calls_used": False,
            "duration_authority": duration_authority,
        },
        "execution_boundary": {
            "source_adapter_mode": "PREPARE_ONLY",
            "review_preview_only": True,
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
    out["preview_sha256"] = _sha_json(out)
    _assert_no_truth_fields(out)
    return out

def _assert_no_truth_fields(value: Any, location: str = "temporal_preview") -> None:
    forbidden = {"simulationresult","simulation_result","simulationtruth","simulation_truth","winning_frame","winningframe","close_calls","closecalls","derived_telemetry","derivedtelemetry","gameplay_rng","structural_rng"}
    if isinstance(value, Mapping):
        for key, child in value.items():
            normalized = str(key).replace("-", "_").lower()
            if normalized in forbidden:
                raise DRendererTemporalBoundPreviewError(f"Forbidden simulation/telemetry field at {location}: {key}")
            _assert_no_truth_fields(child, f"{location}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _assert_no_truth_fields(child, f"{location}[{index}]")

def build_temporal_bound_preview(content_type: str, project_root: Path | str | None = None) -> dict[str, Any]:
    root = _root(project_root)
    contract, schema, lineage = _load_contract(root)
    result = _build_preview(content_type, root, contract, schema, lineage)
    validate_temporal_bound_preview(result, project_root=root)
    return result

def validate_temporal_bound_preview(candidate: Mapping[str, Any], project_root: Path | str | None = None) -> None:
    if not isinstance(candidate, Mapping):
        raise DRendererTemporalBoundPreviewError("Temporal preview must be a mapping")
    root = _root(project_root)
    contract, schema, lineage = _load_contract(root)
    content_type = str(candidate.get("content_type"))
    expected = _build_preview(content_type, root, contract, schema, lineage)
    if dict(candidate) != expected:
        raise DRendererTemporalBoundPreviewError("Temporal preview mismatch, source drift, invented timing, or governance escalation")
    if set(candidate) != set(schema.get("required", [])):
        raise DRendererTemporalBoundPreviewError("Temporal preview output shape does not match strict schema")
    if _sha_json(_without_hash(candidate)) != candidate.get("preview_sha256"):
        raise DRendererTemporalBoundPreviewError("Temporal preview SHA-256 mismatch")
    _assert_no_truth_fields(candidate)
    if candidate.get("manifest_sha256") != EXPECTED_MANIFEST_SHA256:
        raise DRendererTemporalBoundPreviewError("Immutable C11-C manifest pin mismatch")
