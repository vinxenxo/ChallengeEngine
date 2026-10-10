from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_DELIVERY_TIMELINE_REVIEW_V1.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_DELIVERY_TIMELINE_REVIEW_SCHEMA_V1.json")
CONTRACT_ID = "C11-D-D9-RENDERER-CHALLENGE-DELIVERY-TIMELINE-REVIEW-V1"
FROZEN_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
EXPECTED_LINEAGE = [
    ("release/C11C_FREEZE_PACKAGE_MANIFEST.json", "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"),
    ("challenges/CHALLENGE_004.json", "6a674c02c2d8831a872691954f1cc40e2492193f9b136f60656730a7be686b71"),
    ("profiles/video/test_master_11s.json", "6ac5ddd620d5300f1e365dd4dd8ca6c04e0f97c2ceb95ec48438d52059bff93b"),
    ("profiles/video/parking_v2_social_15s.json", "12b49f14e0ee755d290f7dd36471723da6337ab3244461fc0088a3e3b77c5a82"),
    ("profiles/delivery/c11c_video_delivery_profiles.json", "967831513eb225e6eafd56496ce0d0a0b0f0e158d205b5985e7bba11b0534ae3"),
    ("core/execution/ChallengeRuntimeBridge.gd", "c53f04df064b3697f8dd02cd779f8ef002a4e3e2d40fa0e01aa7d9b1a80a8191"),
    ("core/execution/ChallengeTimelineBuilder.gd", "35a47ad126a2e11577933a03b251f47732e580693e5c08e45d3b6af047c8c9af"),
    ("core/authoring/ChallengeMigrationAdapter.gd", "79099cbb5fea9d9c5c519370b1c56d72c8394db14e9adf5b0bb744410e507c13"),
    ("core/authoring/TemporalCore.gd", "f076e9090c3d13be63b7ccda91a5861576a4d32eb673380a95272b3b3fa27966"),
    ("core/presentation/ChallengePresentationBinder.gd", "755ecfc9cc6e1ee51738938583217ab8a470c1a1f290bb107e91e19990d74b47"),
    ("definitions/c11d/production/D_RENDERER_PROFILE_IDENTITY_SEPARATION_V1.json", "e217d0d94a580747e754be68aba18bcadc4cf954c09d60f97a07e2b9c35fbb77"),
    ("definitions/c11d/production/D_RENDERER_DELIVERY_TIMEBASE_PROJECTION_V1.json", "602c938cbf8378e8f71aefc6fb46d61496e78f9ab84d595f9efab982a2820a38"),
    ("definitions/c11d/production/D_RENDERER_CHALLENGE_RUNTIME_OUTPUT_PREVIEW_V1.json", "ed56660d77de32e288eb3f4106499e94e390785d6d6503c5c028fc3399dd20c5"),
    ("definitions/c11d/production/D_RENDERER_TEMPORAL_BOUND_PREVIEW_V1.json", "ff203026f6a4dee4ae2ccb47992b3dde7c7d9644320427eabd17eddc0a4ac646"),
    ("definitions/c11d/production/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1.json", "660f20bf39f6c797e5b3f06615e19efe490353c35637effcacd2e7d4acc447fd"),
]
PHASES = ("HOOK", "GAME", "REVEAL", "CTA")
DURATION_KEYS = ("hook_duration", "game_duration", "reveal_duration", "cta_duration")


class ChallengeDeliveryTimelineReviewError(ValueError):
    pass


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ChallengeDeliveryTimelineReviewError(f"Cannot read JSON: {path}") from exc
    if not isinstance(value, dict):
        raise ChallengeDeliveryTimelineReviewError(f"JSON root must be an object: {path}")
    return value


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_contract(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    contract = _load_json(root / CONTRACT_REL)
    schema = _load_json(root / SCHEMA_REL)
    if contract.get("schema") != CONTRACT_ID or contract.get("schema_version") != "1.0":
        raise ChallengeDeliveryTimelineReviewError("Contract identity/version drift.")
    if contract.get("status") != "IN_MEMORY_REVIEW_ONLY_NOT_RENDERER_INPUT":
        raise ChallengeDeliveryTimelineReviewError("Contract cannot authorize renderer use.")
    lineage = contract.get("source_lineage")
    expected = [{"path": p, "sha256": h} for p, h in EXPECTED_LINEAGE]
    if lineage != expected:
        raise ChallengeDeliveryTimelineReviewError("Pinned source-lineage declaration drifted.")
    for rel, expected_sha in EXPECTED_LINEAGE:
        path = root / rel
        if not path.is_file() or _sha(path) != expected_sha:
            raise ChallengeDeliveryTimelineReviewError(f"Pinned source missing or hash mismatch: {rel}")
    manifest = root / "release/C11C_FREEZE_PACKAGE_MANIFEST.json"
    if _sha(manifest) != FROZEN_MANIFEST_SHA256:
        raise ChallengeDeliveryTimelineReviewError("Frozen C11-C manifest hash mismatch.")
    projection = _load_json(root / "definitions/c11d/production/D_RENDERER_DELIVERY_TIMEBASE_PROJECTION_V1.json")
    if projection.get("normalization_policy", {}).get("state") != "PROPOSED_NOT_APPROVED":
        raise ChallengeDeliveryTimelineReviewError("Delivery projection policy was silently approved.")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise ChallengeDeliveryTimelineReviewError("Expected Draft 2020-12 schema.")
    return contract, schema


def project_boundary(source_boundary: int, source_fps: int, delivery_fps: int) -> int:
    """Integer nearest-tick projection with half-up tie breaking for non-negative boundaries."""
    if isinstance(source_boundary, bool) or not isinstance(source_boundary, int) or source_boundary < 0:
        raise ChallengeDeliveryTimelineReviewError("Source boundary must be a non-negative integer.")
    if isinstance(source_fps, bool) or not isinstance(source_fps, int) or source_fps <= 0:
        raise ChallengeDeliveryTimelineReviewError("Source FPS must be a positive integer.")
    if isinstance(delivery_fps, bool) or not isinstance(delivery_fps, int) or delivery_fps <= 0:
        raise ChallengeDeliveryTimelineReviewError("Delivery FPS must be a positive integer.")
    return (2 * source_boundary * delivery_fps + source_fps) // (2 * source_fps)


def _duration_to_frames(duration: Any, fps: int, name: str) -> int:
    if isinstance(duration, bool) or not isinstance(duration, (int, float)) or duration < 0:
        raise ChallengeDeliveryTimelineReviewError(f"Invalid duration: {name}")
    frames = Fraction(str(duration)) * fps
    if frames.denominator != 1:
        raise ChallengeDeliveryTimelineReviewError(f"Duration does not map to an integral source frame count: {name}")
    return frames.numerator


def _phase_records(counts: list[int], fps: int, target_fps: int | None = None) -> tuple[list[dict[str, Any]], list[int]]:
    start = 0
    boundaries = [0]
    records: list[dict[str, Any]] = []
    for name, count in zip(PHASES, counts, strict=True):
        end = start + count
        if target_fps is None:
            out_start, out_end = start, end
        else:
            out_start = project_boundary(start, fps, target_fps)
            out_end = project_boundary(end, fps, target_fps)
        records.append({"phase": name, "start_frame": out_start, "end_frame": out_end, "frame_count": out_end - out_start})
        start = end
        boundaries.append(end)
    return records, boundaries


def build_preview(root: Path) -> dict[str, Any]:
    contract, _ = validate_contract(root)
    challenge_path = root / "challenges/CHALLENGE_004.json"
    challenge = _load_json(challenge_path)
    video = challenge.get("video")
    presentation = challenge.get("presentation")
    if not isinstance(video, dict) or not isinstance(presentation, dict):
        raise ChallengeDeliveryTimelineReviewError("Challenge source lacks inline video/presentation objects.")
    if challenge.get("challenge_id") != "CHALLENGE_004" or challenge.get("video_profile") != "test_master_11s":
        raise ChallengeDeliveryTimelineReviewError("Challenge identity or legacy profile alias drifted.")
    if presentation.get("profile") != "social_default_v1":
        raise ChallengeDeliveryTimelineReviewError("Explicit source presentation profile drifted.")
    source_fps = video.get("fps")
    if isinstance(source_fps, bool) or not isinstance(source_fps, int) or source_fps != 60:
        raise ChallengeDeliveryTimelineReviewError("Challenge inline FPS changed from the pinned source contract.")
    counts = [_duration_to_frames(video.get(key), source_fps, key) for key in DURATION_KEYS]
    if counts != [180, 420, 180, 120]:
        raise ChallengeDeliveryTimelineReviewError("Canonical phase frame counts do not match the pinned timeline.")
    source_records, source_boundaries = _phase_records(counts, source_fps)
    delivery_registry = _load_json(root / "profiles/delivery/c11c_video_delivery_profiles.json")
    profile = delivery_registry.get("profiles", {}).get("REVIEW_720", {})
    if not isinstance(profile, dict) or (profile.get("fps"), profile.get("width"), profile.get("height")) != (30, 720, 1280):
        raise ChallengeDeliveryTimelineReviewError("REVIEW_720 delivery profile facts drifted.")
    projected_records, _ = _phase_records(counts, source_fps, int(profile["fps"]))
    source_total = sum(counts)
    projected_total = project_boundary(source_total, source_fps, int(profile["fps"]))
    source_seconds = Fraction(source_total, source_fps)
    projected_seconds = Fraction(projected_total, int(profile["fps"]))
    if source_seconds != projected_seconds or source_boundaries != [0, 180, 600, 780, 900]:
        raise ChallengeDeliveryTimelineReviewError("Source timeline boundaries/duration mismatch.")
    projected_boundaries = [project_boundary(boundary, source_fps, int(profile["fps"])) for boundary in source_boundaries]
    if projected_boundaries != [0, 90, 300, 390, 450]:
        raise ChallengeDeliveryTimelineReviewError("Projected delivery boundaries mismatch.")
    return {
        "schema": CONTRACT_ID,
        "schema_version": "1.0",
        "status": "IN_MEMORY_REVIEW_ONLY_NOT_RENDERER_INPUT",
        "frozen_c11c_manifest_sha256": FROZEN_MANIFEST_SHA256,
        "challenge_source_sha256": _sha(challenge_path),
        "profile_identity": {
            "challenge_id": "CHALLENGE_004",
            "legacy_video_profile_id": str(challenge["video_profile"]),
            "source_presentation_profile_id": str(presentation["profile"]),
            "d_presentation_profile_id": str(presentation["profile"]),
            "delivery_profile_id": "REVIEW_720"
        },
        "source_timeline": {
            "fps": source_fps,
            "total_frames": source_total,
            "duration_seconds": int(source_seconds),
            "phase_order": list(PHASES),
            "boundary_frames": source_boundaries
        },
        "delivery_profile": {"profile_id": "REVIEW_720", "fps": int(profile["fps"]), "width": int(profile["width"]), "height": int(profile["height"])},
        "source_segments": source_records,
        "delivery_segments": projected_records,
        "field_visibility": {"state": "UNRESOLVED_NO_PER_FIELD_FRAME_WINDOWS", "frame_ranges": None},
        "runtime_evidence": {
            "mode": "NOT_RUN_BY_PYTHON_CONTRACT_TEST",
            "runtime_success": None,
            "repeat_deterministic": None,
            "simulation_frame_signature_unchanged": None,
            "winning_frame_unchanged": None,
            "metrics_unchanged": None,
            "game_frame_count": None
        },
        "policy_state": "PROPOSED_NOT_APPROVED",
        "source_lineage": contract["source_lineage"],
        "execution_boundary": {
            "report_file_written": False,
            "renderer_native_input_emitted": False,
            "renderer_dispatch_invoked": False,
            "renderer_activation": False,
            "media_created": False,
            "c11c_source_mutation": False,
            "output_artifact_path": None,
            "d4_8": "BLOCKED",
            "release_authority": "NONE",
            "video_render_ready": False
        }
    }


def validate_preview(record: dict[str, Any], root: Path) -> bool:
    _, schema = validate_contract(root)
    try:
        import jsonschema
    except ImportError:
        jsonschema = None
    if jsonschema is not None:
        try:
            jsonschema.Draft202012Validator(schema).validate(record)
        except jsonschema.ValidationError as exc:
            raise ChallengeDeliveryTimelineReviewError("Review record failed Draft 2020-12 validation.") from exc
    expected = build_preview(root)
    if record != expected:
        raise ChallengeDeliveryTimelineReviewError("Preview differs from pinned source facts or deterministic phase projection.")
    return True
