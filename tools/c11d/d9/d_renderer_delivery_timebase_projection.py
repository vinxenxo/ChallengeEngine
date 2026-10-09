"""In-memory, source-pinned projection from canonical source FPS to delivery-profile FPS.

This is a proposal only. It does not choose simulation samples, interpolate frames, emit renderer input, or create media.
"""
from __future__ import annotations
import copy, hashlib, json, math
from collections.abc import Mapping
from fractions import Fraction
from pathlib import Path
from typing import Any

from d_renderer_temporal_bound_preview import build_temporal_bound_preview, validate_temporal_bound_preview, DRendererTemporalBoundPreviewError

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_DELIVERY_TIMEBASE_PROJECTION_V1.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_DELIVERY_TIMEBASE_PROJECTION_SCHEMA_V1.json")
PROFILE_REL = Path("profiles/delivery/c11c_video_delivery_profiles.json")
MANIFEST_REL = Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")
CONTRACT_SCHEMA = "C11-D-RENDERER-DELIVERY-TIMEBASE-PROJECTION-CONTRACT-V1"
OUTPUT_SCHEMA = "C11-D-D9-RENDERER-DELIVERY-TIMEBASE-PROJECTION-V1"
STATUS = "PREPARATION_ONLY_IN_MEMORY_DELIVERY_TIMEBASE_PROJECTION"
EXPECTED_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
SUPPORTED_TYPES = ("challenges", "visual_loops", "visual_drills")
EXPECTED_SOURCE_LINEAGE = [{'path': 'release/C11C_FREEZE_PACKAGE_MANIFEST.json', 'sha256': 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953'}, {'path': 'profiles/delivery/c11c_video_delivery_profiles.json', 'sha256': '967831513eb225e6eafd56496ce0d0a0b0f0e158d205b5985e7bba11b0534ae3'}, {'path': 'challenges/CHALLENGE_004.json', 'sha256': '6a674c02c2d8831a872691954f1cc40e2492193f9b136f60656730a7be686b71'}, {'path': 'definitions/visual_loop_geometric_canonical.json', 'sha256': '648eb36225dd4c090457b4da3c9e8eca218c26c8f995cf02a39914cf3f860dcc'}, {'path': 'definitions/visual_drill_tracking_canonical.json', 'sha256': '54d432c80f190f4ac5dcb8ef5b135e16f18c378da120f35723fd5be944719ec3'}, {'path': 'definitions/c11d/production/D_RENDERER_TEMPORAL_SCHEDULE_PROPOSAL_V1.json', 'sha256': '96ee3cffe8223e24673e7eb90c93308d45bb3a350961b2afc5eacbe66b54fbf8'}, {'path': 'definitions/c11d/production/D_RENDERER_TEMPORAL_SCHEDULE_PROPOSAL_SCHEMA_V1.json', 'sha256': '1744e2f748c1ce196e8655c85299bef16f475c4a71b45d5db5b6838418fa4b37'}, {'path': 'definitions/c11d/production/D_RENDERER_TEMPORAL_BOUND_PREVIEW_V1.json', 'sha256': 'ff203026f6a4dee4ae2ccb47992b3dde7c7d9644320427eabd17eddc0a4ac646'}, {'path': 'definitions/c11d/production/D_RENDERER_TEMPORAL_BOUND_PREVIEW_SCHEMA_V1.json', 'sha256': '7f53069af2be484d70b3a1b4c6172baeed9ca87a2f6bc36b8b7ff5961daa35c8'}, {'path': 'tools/c11d/d9/d_renderer_temporal_schedule.py', 'sha256': '04b85a077f06d6ef9ffc7569d3fda0a92471b9ee5e1d6e57d3b50dbf6a6247cd'}, {'path': 'tools/c11d/d9/d_renderer_temporal_bound_preview.py', 'sha256': 'b92be3e598fd59b5f788602aa798445e1a095e47290a4c591481329fe619e164'}, {'path': 'core/authoring/TemporalCore.gd', 'sha256': 'f076e9090c3d13be63b7ccda91a5861576a4d32eb673380a95272b3b3fa27966'}]
EXPECTED_POLICY = {'name': 'CUMULATIVE_SOURCE_BOUNDARY_NEAREST_DELIVERY_TICK', 'state': 'PROPOSED_NOT_APPROVED', 'source_timebase': 'CANONICAL_ZERO_BASED_HALF_OPEN_SOURCE_FRAME_BOUNDARIES', 'mapping_formula': 'delivery_boundary = floor(source_boundary * delivery_fps / source_fps + 0.5)', 'integer_implementation': 'floor((2 * source_boundary * delivery_fps + source_fps) / (2 * source_fps))', 'quantization': 'PROJECT_CUMULATIVE_BOUNDARIES; SEGMENT_COUNTS_ARE_DIFFERENCES_OF_PROJECTED_BOUNDARIES', 'phase_order': 'PRESERVE_SOURCE_TIMELINE_ORDER', 'zero_length_output_span': 'PRESERVE_ZERO_LENGTH; NEVER_FORCE_A_FRAME', 'source_timeline_mutation': False, 'simulation_frame_sampling': 'UNRESOLVED_NOT_DEFINED_NOT_EMITTED', 'simulation_anchor_mapping': 'UNRESOLVED_NOT_DEFINED_NOT_EMITTED', 'interpolation_policy': 'UNRESOLVED_NOT_DEFINED_NOT_EMITTED', 'audio_resampling_policy': 'OUT_OF_SCOPE_NOT_DEFINED_NOT_EMITTED', 'per_field_visibility_windows': 'UNRESOLVED_NOT_DEFINED_NOT_EMITTED', 'renderer_input_emission': False, 'media_creation': False}
EXPECTED_LOCKS = {'projection_mode': 'IN_MEMORY_REVIEW_ONLY', 'renderer_native_input_emitted': False, 'renderer_dispatch_invoked': False, 'renderer_activation': False, 'production_execution': False, 'media_output_created': False, 'output_artifact_path': None, 'c11c_source_mutation': False, 'd4_8': 'BLOCKED', 'release_authority': 'NONE', 'video_render_ready': False}
EXPECTED_APPROVAL = {'timebase_projection_policy_approved': False, 'temporal_topology_approved': False, 'semantic_region_mapping_approved': False, 'renderer_baseline_approved': False, 'renderer_baseline_frozen': False, 'd4_8_authorized': False, 'd9_14_full_acceptance': 'BLOCKED_AS_REQUIRED', 'd9_16_full_acceptance': 'BLOCKED_AS_REQUIRED', 'd9_17_closure': 'BLOCKED_NO_GO', 'd10': 'BLOCKED', 'release_authority': 'NONE'}
EXPECTED_SOURCE_TRUTH = {'frozen_c11c_manifest_sha256': 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953', 'source_timeline': 'D_RENDERER_TEMPORAL_BOUND_PREVIEW_V1_FROM_PINNED_C11C_TIMING_PAYLOADS', 'delivery_fps': 'EXPLICIT_REQUESTED_DELIVERY_PROFILE_RESOLVED_AGAINST_PINNED_PROFILE_REGISTRY', 'challenge_60_to_30_case': 'CHALLENGE_004_SOURCE_60FPS_AND_REVIEW_720_DELIVERY_30FPS', 'boundary_policy': 'PROPOSED_CUMULATIVE_BOUNDARY_NEAREST_DELIVERY_TICK; NOT_APPROVED', 'simulation_truth': 'NOT_READ; WINNING_FRAME/CLOSE_CALLS/TELEMETRY_NOT_MAPPED'}

class DRendererDeliveryTimebaseProjectionError(ValueError):
    """Invalid source identity, FPS profile, projected boundary, hash or governance escalation."""

def _root(project_root: Path | str | None = None) -> Path:
    return Path(project_root).resolve() if project_root is not None else Path(__file__).resolve().parents[3]

def _read_json(root: Path, rel: str | Path) -> dict[str, Any]:
    try: value = json.loads((root / rel).read_text(encoding="utf-8-sig"))
    except Exception as exc: raise DRendererDeliveryTimebaseProjectionError(f"Cannot read required JSON {rel}: {exc}") from exc
    if not isinstance(value, dict): raise DRendererDeliveryTimebaseProjectionError(f"Expected JSON object at {rel}")
    return value

def _sha_file(path: Path) -> str:
    try: return hashlib.sha256(path.read_bytes()).hexdigest()
    except Exception as exc: raise DRendererDeliveryTimebaseProjectionError(f"Cannot hash source {path}: {exc}") from exc

def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)

def _sha_json(value: Any) -> str: return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()
def _without_hash(value: Mapping[str, Any]) -> dict[str, Any]: return {str(k): copy.deepcopy(v) for k,v in value.items() if k != "projection_sha256"}

def _assert_no_truth(value: Any, location: str = "timebase_projection") -> None:
    forbidden = {"simulationresult","simulation_result","simulationtruth","simulation_truth","winning_frame","winningframe","close_calls","closecalls","derived_telemetry","derivedtelemetry","gameplay_rng","structural_rng"}
    if isinstance(value, Mapping):
        for key, child in value.items():
            if str(key).replace("-", "_").lower() in forbidden: raise DRendererDeliveryTimebaseProjectionError(f"Forbidden simulation/telemetry field in {location}: {key}")
            _assert_no_truth(child, f"{location}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value): _assert_no_truth(child, f"{location}[{index}]")

def _load_contract(root: Path) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, str]]]:
    contract = _read_json(root, CONTRACT_REL); schema = _read_json(root, SCHEMA_REL)
    if contract.get("schema") != CONTRACT_SCHEMA or contract.get("schema_version") != "1.0": raise DRendererDeliveryTimebaseProjectionError("Timebase projection contract identity/version mismatch")
    if contract.get("status") != "PREPARATION_ONLY_DELIVERY_TIMEBASE_PROJECTION_NOT_RENDERER_INPUT": raise DRendererDeliveryTimebaseProjectionError("Timebase projection cannot self-promote status")
    if contract.get("supported_content_types") != list(SUPPORTED_TYPES): raise DRendererDeliveryTimebaseProjectionError("Supported content type matrix drift")
    if contract.get("normalization_policy") != EXPECTED_POLICY: raise DRendererDeliveryTimebaseProjectionError("Normalization policy was changed or promoted without implementation review")
    if contract.get("required_locks") != EXPECTED_LOCKS: raise DRendererDeliveryTimebaseProjectionError("Execution boundary lock mismatch")
    if contract.get("approval_state") != EXPECTED_APPROVAL: raise DRendererDeliveryTimebaseProjectionError("Projection cannot grant production/baseline approval")
    if contract.get("source_of_truth") != EXPECTED_SOURCE_TRUTH: raise DRendererDeliveryTimebaseProjectionError("Source-of-truth declaration drift")
    if _sha_file(root / MANIFEST_REL) != EXPECTED_MANIFEST_SHA256: raise DRendererDeliveryTimebaseProjectionError("Frozen C11-C manifest pin mismatch")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or schema.get("$id") != "urn:c11d:renderer-delivery-timebase-projection:v1" or schema.get("additionalProperties") is not False: raise DRendererDeliveryTimebaseProjectionError("Output schema identity/strictness mismatch")
    if set(schema.get("required", [])) != set(schema.get("properties", {})): raise DRendererDeliveryTimebaseProjectionError("Output schema must require exactly its top-level properties")
    entries = contract.get("source_lineage")
    if not isinstance(entries, list) or entries != EXPECTED_SOURCE_LINEAGE: raise DRendererDeliveryTimebaseProjectionError("Pinned source-lineage declaration drift")
    observed: list[dict[str, str]] = []
    seen: set[str] = set()
    for entry in entries:
        if not isinstance(entry, Mapping) or set(entry) != {"path", "sha256"}: raise DRendererDeliveryTimebaseProjectionError("Malformed source-lineage entry")
        rel, expected = str(entry["path"]), str(entry["sha256"])
        if rel in seen or len(expected) != 64 or any(c not in "0123456789abcdef" for c in expected): raise DRendererDeliveryTimebaseProjectionError("Duplicate or malformed source pin")
        actual = _sha_file(root / rel)
        if actual != expected: raise DRendererDeliveryTimebaseProjectionError(f"Pinned source drift: {rel}")
        seen.add(rel); observed.append({"path": rel, "sha256": actual})
    if entries[0]["path"] != str(MANIFEST_REL).replace("\\", "/"): raise DRendererDeliveryTimebaseProjectionError("Frozen C11-C manifest must lead source lineage")
    return contract, schema, observed

def _profile(root: Path, profile_id: str) -> tuple[dict[str, Any], str, str]:
    if not isinstance(profile_id, str) or not profile_id.strip(): raise DRendererDeliveryTimebaseProjectionError("A non-empty explicit delivery_profile_id is required")
    registry = _read_json(root, PROFILE_REL)
    profiles = registry.get("profiles")
    if not isinstance(profiles, Mapping) or profile_id not in profiles: raise DRendererDeliveryTimebaseProjectionError(f"Unknown delivery profile: {profile_id}")
    requested = profiles[profile_id]
    if not isinstance(requested, Mapping): raise DRendererDeliveryTimebaseProjectionError("Delivery profile declaration must be an object")
    resolved_id = str(requested.get("alias_of", profile_id))
    resolved = profiles.get(resolved_id)
    if not isinstance(resolved, Mapping): raise DRendererDeliveryTimebaseProjectionError("Delivery profile alias has no canonical target")
    fps = resolved.get("fps"); width = resolved.get("width"); height = resolved.get("height")
    if isinstance(fps, bool) or not isinstance(fps, int) or fps <= 0: raise DRendererDeliveryTimebaseProjectionError("Resolved delivery profile FPS must be a positive integer")
    if isinstance(width, bool) or not isinstance(width, int) or width <= 0 or isinstance(height, bool) or not isinstance(height, int) or height <= 0: raise DRendererDeliveryTimebaseProjectionError("Resolved profile dimensions must be positive integers")
    return {"requested_profile_id": profile_id, "resolved_profile_id": resolved_id, "width": width, "height": height, "fps": fps, "registry_sha256": _sha_file(root / PROFILE_REL), "metadata_only": True}, resolved_id, _sha_file(root / PROFILE_REL)

def _round_ratio_half_up(numerator: int, denominator: int) -> int:
    if isinstance(numerator, bool) or not isinstance(numerator, int) or numerator < 0: raise DRendererDeliveryTimebaseProjectionError("Boundary numerator must be a nonnegative integer")
    if isinstance(denominator, bool) or not isinstance(denominator, int) or denominator <= 0: raise DRendererDeliveryTimebaseProjectionError("Boundary denominator must be a positive integer")
    return (2 * numerator + denominator) // (2 * denominator)

def _lineage_sha(lineage: list[dict[str, str]]) -> str: return _sha_json(lineage)

def _build(content_type: str, delivery_profile_id: str, root: Path, contract: Mapping[str, Any], schema: Mapping[str, Any], lineage: list[dict[str, str]]) -> dict[str, Any]:
    if content_type not in SUPPORTED_TYPES: raise DRendererDeliveryTimebaseProjectionError("Unsupported content type; Longform and unknown types fail closed")
    try:
        preview = build_temporal_bound_preview(content_type, root)
        validate_temporal_bound_preview(preview, project_root=root)
    except (DRendererTemporalBoundPreviewError, ValueError, TypeError, KeyError) as exc:
        raise DRendererDeliveryTimebaseProjectionError(f"Canonical temporal source refused projection: {exc}") from exc
    target, _, registry_sha = _profile(root, delivery_profile_id)
    source_schedule = preview.get("temporal_schedule", {})
    source_fps = source_schedule.get("fps"); source_total = source_schedule.get("total_frames"); source_segments = source_schedule.get("segments")
    target_fps = target["fps"]
    if isinstance(source_fps, bool) or not isinstance(source_fps, int) or source_fps <= 0: raise DRendererDeliveryTimebaseProjectionError("Source FPS must be a positive integer")
    if isinstance(source_total, bool) or not isinstance(source_total, int) or source_total <= 0: raise DRendererDeliveryTimebaseProjectionError("Source total frame count must be positive")
    if not isinstance(source_segments, list) or not source_segments: raise DRendererDeliveryTimebaseProjectionError("Canonical temporal source must contain segments")
    projected = []
    source_cursor = 0; delivery_cursor = 0
    for index, seg in enumerate(source_segments):
        if not isinstance(seg, Mapping): raise DRendererDeliveryTimebaseProjectionError("Source segment must be an object")
        sid = seg.get("segment_id"); start = seg.get("start_frame"); end = seg.get("end_frame_exclusive"); count = seg.get("frame_count")
        if not isinstance(sid, str) or not sid or any(isinstance(v, bool) or not isinstance(v, int) for v in (start, end, count)): raise DRendererDeliveryTimebaseProjectionError("Malformed canonical source segment")
        if start != source_cursor or end < start or count != end - start: raise DRendererDeliveryTimebaseProjectionError("Canonical source segment sequence is not contiguous and internally consistent")
        delivery_start = _round_ratio_half_up(start * target_fps, source_fps)
        delivery_end = _round_ratio_half_up(end * target_fps, source_fps)
        if delivery_start != delivery_cursor or delivery_end < delivery_start: raise DRendererDeliveryTimebaseProjectionError("Projected segment sequence is not contiguous and monotonic")
        delivery_count = delivery_end - delivery_start
        projected.append({
            "segment_id": sid,
            "source_start_frame": start,
            "source_end_frame_exclusive": end,
            "source_frame_count": count,
            "delivery_start_frame": delivery_start,
            "delivery_end_frame_exclusive": delivery_end,
            "delivery_frame_count": delivery_count,
            "enabled": delivery_count > 0,
        })
        source_cursor = end; delivery_cursor = delivery_end
    if source_cursor != source_total or projected[0]["source_start_frame"] != 0: raise DRendererDeliveryTimebaseProjectionError("Source segments do not cover the canonical complete timeline")
    expected_delivery_total = _round_ratio_half_up(source_total * target_fps, source_fps)
    if delivery_cursor != expected_delivery_total: raise DRendererDeliveryTimebaseProjectionError("Projected terminal boundary does not match the canonical source duration")
    error = Fraction(delivery_cursor, target_fps) - Fraction(source_total, source_fps)
    relation = "MATCH_SOURCE_AND_DELIVERY_FPS" if source_fps == target_fps else "SOURCE_FPS_DIFFERS_FROM_DELIVERY_FPS"
    out: dict[str, Any] = {
        "schema": OUTPUT_SCHEMA,
        "schema_version": "1.0",
        "status": STATUS,
        "frozen_c11c_manifest_sha256": EXPECTED_MANIFEST_SHA256,
        "content_type": content_type,
        "source_identity": {
            "temporal_preview_sha256": preview["preview_sha256"],
            "source_path": preview["source_identity"]["source_path"],
            "source_id": preview["source_identity"]["source_id"],
            "source_sha256": preview["source_identity"]["source_sha256"],
            "source_lineage_sha256": _lineage_sha(lineage),
            "source_fps": source_fps,
            "source_total_frames": source_total,
        },
        "delivery_profile": target,
        "normalization_policy": {
            "name": EXPECTED_POLICY["name"],
            "state": EXPECTED_POLICY["state"],
            "source_fps": source_fps,
            "delivery_fps": target_fps,
            "formula": EXPECTED_POLICY["mapping_formula"],
            "integer_arithmetic": EXPECTED_POLICY["integer_implementation"],
            "simulation_sampling": "UNRESOLVED_NOT_EMITTED",
            "simulation_anchor_mapping": "UNRESOLVED_NOT_EMITTED",
            "interpolation": "UNRESOLVED_NOT_EMITTED",
            "audio_resampling": "OUT_OF_SCOPE_NOT_EMITTED",
            "approved": False,
        },
        "source_timebase": {
            "fps": source_fps, "total_frames": source_total,
            "duration_numerator": source_total, "duration_denominator": source_fps,
            "frame_index_convention": "ZERO_BASED_HALF_OPEN",
        },
        "delivery_timebase": {
            "fps": target_fps, "total_frames": delivery_cursor,
            "duration_numerator": delivery_cursor, "duration_denominator": target_fps,
            "frame_index_convention": "ZERO_BASED_HALF_OPEN",
        },
        "segments": projected,
        "projection_assessment": {
            "source_segments_contiguous": True,
            "delivery_segments_contiguous": True,
            "source_order_preserved": True,
            "source_timeline_mutated": False,
            "duration_delta_seconds": {"numerator": error.numerator, "denominator": error.denominator},
            "fps_relation": relation,
            "field_visibility_windows": "UNRESOLVED_NOT_EMITTED",
            "selected_visual_payload_instance_bound": False,
            "video_render_ready": False,
        },
        "execution_boundary": copy.deepcopy(EXPECTED_LOCKS),
    }
    out["projection_sha256"] = _sha_json(out)
    _assert_no_truth(out)
    return out

def build_delivery_timebase_projection(content_type: str, delivery_profile_id: str = "REVIEW_720", project_root: Path | str | None = None) -> dict[str, Any]:
    root = _root(project_root)
    contract, schema, lineage = _load_contract(root)
    result = _build(content_type, delivery_profile_id, root, contract, schema, lineage)
    validate_delivery_timebase_projection(result, content_type, delivery_profile_id, project_root=root)
    return result

def validate_delivery_timebase_projection(candidate: Mapping[str, Any], content_type: str, delivery_profile_id: str = "REVIEW_720", project_root: Path | str | None = None) -> bool:
    if not isinstance(candidate, Mapping): raise DRendererDeliveryTimebaseProjectionError("Projection candidate must be a mapping")
    root = _root(project_root)
    contract, schema, lineage = _load_contract(root)
    expected = _build(content_type, delivery_profile_id, root, contract, schema, lineage)
    if dict(candidate) != expected: raise DRendererDeliveryTimebaseProjectionError("Projection differs from pinned source/profile, policy, frame boundaries or governance locks")
    if set(candidate) != set(schema.get("required", [])): raise DRendererDeliveryTimebaseProjectionError("Projection output shape differs from strict schema")
    if _sha_json(_without_hash(candidate)) != candidate.get("projection_sha256"): raise DRendererDeliveryTimebaseProjectionError("Projection SHA-256 mismatch")
    _assert_no_truth(candidate)
    if candidate.get("frozen_c11c_manifest_sha256") != EXPECTED_MANIFEST_SHA256: raise DRendererDeliveryTimebaseProjectionError("Frozen C11-C manifest mismatch")
    return True
