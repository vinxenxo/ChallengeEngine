from __future__ import annotations

import copy
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Mapping

from d_renderer_challenge_simulation_sample_selection import (
    ChallengeSampleSelectionError,
    build_sample_selection_preview,
    validate_sample_selection_preview,
)

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_UNIFIED_CONTENT_REVIEW_V1.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_UNIFIED_CONTENT_REVIEW_SCHEMA_V1.json")
CONTRACT_ID = "C11-D-RENDERER-UNIFIED-CONTENT-REVIEW-CONTRACT-V1"
OUTPUT_SCHEMA = "C11-D-D9-RENDERER-UNIFIED-CONTENT-REVIEW-V1"
FROZEN_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
CHALLENGE_SHA256 = "6a674c02c2d8831a872691954f1cc40e2492193f9b136f60656730a7be686b71"
EXPECTED_TYPES = ["visual_loops", "visual_drills", "challenges"]
EXPECTED_SOURCE_LINEAGE = [
    ("release/C11C_FREEZE_PACKAGE_MANIFEST.json", FROZEN_MANIFEST_SHA256),
    ("challenges/CHALLENGE_004.json", CHALLENGE_SHA256),
    ("profiles/delivery/c11c_video_delivery_profiles.json", "967831513eb225e6eafd56496ce0d0a0b0f0e158d205b5985e7bba11b0534ae3"),
    ("definitions/c11d/production/D_RENDERER_VISUAL_PAYLOAD_MATERIALIZATION_PREVIEW_V1.json", "937f34bdcb243a64b65c1e354828c2d8f81b5c0a5c3ac68619aab427c1f44c26"),
    ("definitions/c11d/production/D_RENDERER_CHALLENGE_RUNTIME_OUTPUT_PREVIEW_V1.json", "ed56660d77de32e288eb3f4106499e94e390785d6d6503c5c028fc3399dd20c5"),
    ("definitions/c11d/production/D_RENDERER_PROFILE_IDENTITY_SEPARATION_V1.json", "e217d0d94a580747e754be68aba18bcadc4cf954c09d60f97a07e2b9c35fbb77"),
    ("definitions/c11d/production/D_RENDERER_DELIVERY_TIMEBASE_PROJECTION_V1.json", "602c938cbf8378e8f71aefc6fb46d61496e78f9ab84d595f9efab982a2820a38"),
    ("definitions/c11d/production/D_RENDERER_TEMPORAL_BOUND_PREVIEW_V1.json", "ff203026f6a4dee4ae2ccb47992b3dde7c7d9644320427eabd17eddc0a4ac646"),
    ("definitions/c11d/production/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1.json", "660f20bf39f6c797e5b3f06615e19efe490353c35637effcacd2e7d4acc447fd"),
    ("definitions/c11d/production/D_RENDERER_CHALLENGE_DELIVERY_TIMELINE_REVIEW_V1.json", "30381dba04a07d6e0ea1d82b186f46b78ab7193ecaa82efe3e484dd5bcd64e22"),
    ("definitions/c11d/production/D_RENDERER_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json", "23c33f99f0bef1c76edc6526bcdfa6bf98dc27d7d22b38f48a424008f8f59c5f"),
    ("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_PREVIEW_V1.json", "67daa1f83ac151906059695bb4d87974819c2d16d3715b78b00657bfdac54f7a"),
    ("definitions/c11d/production/D_RENDERER_CHALLENGE_COORDINATE_PROJECTION_V1.json", "c1caf8e640595bc89957f17ef8bbd7abe80a92cac18cf77974633a1ddde0e264"),
    ("definitions/c11d/production/D_RENDERER_CHALLENGE_SIMULATION_SAMPLE_SELECTION_PROPOSAL_V1.json", "3e278481afe9d66458f05f29c15275819af49f9b68120b6a0b39dda2e9715cf3"),
]
EXPECTED_UNRESOLVED_GATES = [
    "VISUAL_LOOP_EDITORIAL_FIELD_MAPPING_UNDECLARED",
    "VISUAL_DRILL_EDITORIAL_FIELD_MAPPING_UNDECLARED",
    "CHALLENGE_SIMULATION_SAMPLE_SELECTION_AND_INTERPOLATION_UNRESOLVED",
    "CHALLENGE_COORDINATE_PROJECTION_POLICY_NOT_APPROVED",
    "DELIVERY_TIMEBASE_PROJECTION_POLICY_NOT_APPROVED",
    "EDITORIAL_FIELD_WINDOW_POLICY_NOT_APPROVED",
    "D_RENDERER_BASELINE_APPROVAL_EXTERNAL_GATE_NOT_ASSERTED_HERE",
    "D4_8_REMAINS_BLOCKED",
]
EXPECTED_HARNESSES = [
    {"name": "visual_payloads", "script": "tools/c11d/d9/materialize_visual_payloads_in_memory.gd", "pass_marker": "C11-D RENDERER VISUAL PAYLOAD MATERIALIZATION PREVIEW PASS", "summary_prefix": "C11-D VISUAL PAYLOAD PREVIEW SUMMARY="},
    {"name": "challenge_runtime", "script": "tools/c11d/d9/materialize_challenge_runtime_output_in_memory.gd", "pass_marker": "C11-D RENDERER CHALLENGE RUNTIME OUTPUT PREVIEW PASS", "summary_prefix": "C11-D CHALLENGE RUNTIME OUTPUT PREVIEW SUMMARY="},
    {"name": "profile_identity", "script": "tools/c11d/d9/rebind_challenge_presentation_profile_in_memory.gd", "pass_marker": "C11-D RENDERER PROFILE IDENTITY SEPARATION PASS", "summary_prefix": "C11-D PROFILE IDENTITY SEPARATION SUMMARY="},
    {"name": "delivery_timeline", "script": "tools/c11d/d9/review_challenge_delivery_timeline_in_memory.gd", "pass_marker": "C11-D RENDERER CHALLENGE DELIVERY TIMELINE REVIEW PASS", "summary_prefix": "C11-D CHALLENGE DELIVERY TIMELINE REVIEW SUMMARY="},
    {"name": "editorial_windows", "script": "tools/c11d/d9/review_editorial_field_windows_in_memory.gd", "pass_marker": "C11-D RENDERER EDITORIAL FIELD WINDOW PROPOSAL PASS", "summary_prefix": "C11-D EDITORIAL FIELD WINDOW PROPOSAL SUMMARY="},
    {"name": "challenge_visual_payload", "script": "tools/c11d/d9/materialize_challenge_visual_payload_in_memory.gd", "pass_marker": "C11-D RENDERER CHALLENGE VISUAL PAYLOAD PREVIEW PASS", "summary_prefix": "C11-D CHALLENGE VISUAL PAYLOAD PREVIEW SUMMARY="},
    {"name": "coordinate_projection", "script": "tools/c11d/d9/review_challenge_coordinate_projection_in_memory.gd", "pass_marker": "C11-D RENDERER CHALLENGE COORDINATE PROJECTION PREVIEW PASS", "summary_prefix": "C11-D CHALLENGE COORDINATE PROJECTION SUMMARY="},
]


class UnifiedContentReviewError(ValueError):
    pass


def _root(project_root: Path | str | None = None) -> Path:
    return Path(project_root).resolve() if project_root is not None else Path(__file__).resolve().parents[3]


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise UnifiedContentReviewError(f"Cannot read JSON: {path}") from exc
    if not isinstance(value, dict):
        raise UnifiedContentReviewError(f"JSON root must be an object: {path}")
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_json(value: Any) -> str:
    return sha256_bytes(canonical_json(value).encode("utf-8"))


def _is_sha256(value: Any) -> bool:
    if not isinstance(value, str) or len(value) != 64:
        return False
    return all(c in "0123456789abcdef" for c in value)


def validate_contract(project_root: Path | str | None = None, *, verify_sources: bool = False) -> tuple[dict[str, Any], dict[str, Any]]:
    root = _root(project_root)
    contract = _read_json(root / CONTRACT_REL)
    schema = _read_json(root / SCHEMA_REL)
    if contract.get("schema") != CONTRACT_ID or contract.get("schema_version") != "1.0":
        raise UnifiedContentReviewError("Contract identity/version drift")
    if contract.get("status") != "IN_MEMORY_REVIEW_ONLY_NOT_RENDERER_INPUT":
        raise UnifiedContentReviewError("Unified review must remain in-memory and non-rendering")
    if contract.get("supported_content_types") != EXPECTED_TYPES:
        raise UnifiedContentReviewError("Supported content type order/scope drift")
    lineage = contract.get("source_lineage")
    expected_lineage = [{"path": p, "sha256": h} for p, h in EXPECTED_SOURCE_LINEAGE]
    if lineage != expected_lineage:
        raise UnifiedContentReviewError("Pinned source lineage declaration drift")
    if len({row[0] for row in EXPECTED_SOURCE_LINEAGE}) != len(EXPECTED_SOURCE_LINEAGE):
        raise UnifiedContentReviewError("Duplicate pinned lineage path")
    if contract.get("runtime_harnesses") != EXPECTED_HARNESSES:
        raise UnifiedContentReviewError("Runtime harness order, path or parser markers drifted")
    policy = contract.get("review_policy", {})
    if policy.get("review_status") != "REVIEW_CHAIN_CONSISTENT_NOT_VIDEO_READY":
        raise UnifiedContentReviewError("Review readiness must not be promoted to video ready")
    if policy.get("report_persistence") != "NONE_CONSOLE_ONLY" or policy.get("reject_runtime_error_logs_even_if_pass_marker_is_present") is not True:
        raise UnifiedContentReviewError("Console-only/error-log gate drift")
    if policy.get("challenge_sample_selection_interpolation") != "PROPOSED_NOT_APPROVED_INCLUDED_IN_UNIFIED_REVIEW_NOT_APPLIED":
        raise UnifiedContentReviewError("Sample-selection proposal must be included for review only, never applied or approved here")
    approval_state = contract.get("approval_state", {})
    if approval_state.get("simulation_sample_selection_policy_approved") is not False or approval_state.get("interpolation_policy_approved") is not False:
        raise UnifiedContentReviewError("Unified review cannot approve simulation sample selection or interpolation")
    boundary = contract.get("execution_boundary", {})
    required_boundary = {
        "mode": "SEQUENTIAL_HEADLESS_IN_MEMORY_REVIEW_ONLY",
        "persistent_report_written": False,
        "payload_files_written": False,
        "renderer_native_input_emitted": False,
        "renderer_dispatch_invoked": False,
        "renderer_activation": False,
        "production_execution": False,
        "media_created": False,
        "c11c_source_mutation": False,
        "video_render_ready": False,
        "d4_8": "BLOCKED",
        "release_authority": "NONE",
    }
    if boundary != required_boundary:
        raise UnifiedContentReviewError("Execution boundary/governance lock drift")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise UnifiedContentReviewError("Unified review schema must be Draft 2020-12")
    if verify_sources:
        for rel, expected_sha in EXPECTED_SOURCE_LINEAGE:
            path = root / rel
            if not path.is_file():
                raise UnifiedContentReviewError(f"Pinned source missing: {rel}")
            actual = sha256_bytes(path.read_bytes())
            if actual != expected_sha:
                raise UnifiedContentReviewError(f"Pinned source SHA-256 mismatch: {rel}")
        for item in EXPECTED_HARNESSES:
            if not (root / item["script"]).is_file():
                raise UnifiedContentReviewError(f"Runtime harness missing: {item['script']}")
    return contract, schema


def validate_harness_summaries(summaries: Mapping[str, dict[str, Any]], project_root: Path | str | None = None) -> dict[str, Any]:
    expected_names = [item["name"] for item in EXPECTED_HARNESSES]
    if list(summaries.keys()) != expected_names:
        raise UnifiedContentReviewError("All seven runtime summaries must be provided in canonical order")
    visual = summaries["visual_payloads"]
    challenge = summaries["challenge_runtime"]
    identity = summaries["profile_identity"]
    timeline = summaries["delivery_timeline"]
    windows = summaries["editorial_windows"]
    challenge_visual = summaries["challenge_visual_payload"]
    coordinate = summaries["coordinate_projection"]

    frozen = FROZEN_MANIFEST_SHA256
    if any(x.get("frozen_c11c_manifest_sha256") != frozen for x in (visual, challenge, identity, timeline, windows, challenge_visual, coordinate)):
        raise UnifiedContentReviewError("The seven harnesses do not agree on the frozen C11-C manifest")
    if any(x.get("challenge_source_sha256") != CHALLENGE_SHA256 for x in (challenge, identity, timeline, windows, challenge_visual, coordinate)):
        raise UnifiedContentReviewError("Challenge source SHA-256 identity mismatch across runtime reviews")

    instances = visual.get("instances")
    if not isinstance(instances, list) or len(instances) != 2:
        raise UnifiedContentReviewError("Expected exactly one in-memory Visual Loop and one Visual Drill")
    by_type = {str(item.get("content_type", "")): item for item in instances if isinstance(item, dict)}
    if set(by_type) != {"visual_loops", "visual_drills"}:
        raise UnifiedContentReviewError("Visual payload preview type coverage mismatch")
    loop = by_type["visual_loops"]
    drill = by_type["visual_drills"]
    for row, expected_type, expected_frames, expected_duration in ((loop, "visual_loops", 600, 20.0), (drill, "visual_drills", 630, 21.0)):
        if row.get("content_type") != expected_type or row.get("materialization") != "IN_MEMORY_ONLY":
            raise UnifiedContentReviewError(f"Unexpected visual payload materialization: {expected_type}")
        if row.get("deterministic_repeat_pass") is not True or row.get("instance_parameters_bound") is not True:
            raise UnifiedContentReviewError(f"Visual payload determinism/binding failed: {expected_type}")
        if int(row.get("fps", -1)) != 30 or int(row.get("frame_count", -1)) != expected_frames or float(row.get("duration_seconds", -1)) != expected_duration:
            raise UnifiedContentReviewError(f"Visual payload timing mismatch: {expected_type}")
        for key in ("payload_instance_sha256", "authoring_envelope_sha256"):
            if not _is_sha256(row.get(key)):
                raise UnifiedContentReviewError(f"Malformed {key}: {expected_type}")

    if visual.get("challenge_runtime_payload_materialized") is not False or visual.get("unmaterialized_content_types") != ["challenges"]:
        raise UnifiedContentReviewError("Base Loop/Drill payload harness must leave Challenge materialization to the dedicated Challenge harness")
    if challenge.get("challenge_runtime_output_materialized") is not True or challenge.get("challenge_visual_payload_materialized") is not False or challenge.get("deterministic_repeat_pass") is not True:
        raise UnifiedContentReviewError("Challenge runtime summary must remain a simulation result; visual payload is verified by its dedicated harness")
    challenge_instance = challenge.get("instance", {})
    if not isinstance(challenge_instance, dict) or challenge_instance.get("challenge_id") != "CHALLENGE_004":
        raise UnifiedContentReviewError("Unexpected challenge runtime identity")
    if challenge_instance.get("simulation_error_state") != "OK" or challenge_instance.get("presentation_binding_success") is not True:
        raise UnifiedContentReviewError("Challenge runtime/presentation binding did not pass")
    if int(challenge_instance.get("fps", -1)) != 60 or int(challenge_instance.get("total_frames", -1)) != 900 or int(challenge_instance.get("game_frame_count", -1)) != 420:
        raise UnifiedContentReviewError("Challenge runtime timeline is not the pinned source timeline")
    if not _is_sha256(challenge_instance.get("runtime_output_sha256")) or not _is_sha256(challenge_instance.get("frame_signature_sha256")):
        raise UnifiedContentReviewError("Challenge runtime output/frame signature digest invalid")

    facts = identity.get("identity_facts", {})
    rebound = identity.get("runtime_rebind", {})
    invariance = identity.get("simulation_invariance", {})
    expected_facts = {
        "legacy_video_profile_id": "test_master_11s",
        "source_presentation_profile_id": "social_default_v1",
        "d_presentation_profile_id": "social_default_v1",
        "delivery_profile_id": "REVIEW_720",
        "inline_timeline_fps": 60,
        "inline_timeline_total_frames": 900,
        "delivery_profile_fps": 30,
        "delivery_width": 720,
        "delivery_height": 1280,
    }
    for key, value in expected_facts.items():
        if facts.get(key) != value:
            raise UnifiedContentReviewError(f"Profile identity fact mismatch: {key}")
    if rebound.get("runtime_success") is not True or rebound.get("legacy_binding_success") is not True or rebound.get("d_binding_success") is not True or rebound.get("d_binding_profile_id") != "social_default_v1":
        raise UnifiedContentReviewError("D presentation profile rebind did not pass")
    render_model_sha = rebound.get("d_binding_render_model_sha256")
    if not _is_sha256(render_model_sha):
        raise UnifiedContentReviewError("D presentation render-model SHA-256 invalid")
    if not all(invariance.get(k) is True for k in ("frame_signature_unchanged", "winning_frame_unchanged", "metrics_unchanged")):
        raise UnifiedContentReviewError("Profile identity separation altered simulation outputs")
    if invariance.get("frame_signature_sha256_before") != invariance.get("frame_signature_sha256_after") or invariance.get("frame_signature_sha256_before") != challenge_instance.get("frame_signature_sha256"):
        raise UnifiedContentReviewError("Simulation frame signature differs between independent runtime harnesses")
    if int(invariance.get("winning_frame_before", -1)) != int(invariance.get("winning_frame_after", -2)) or int(invariance.get("winning_frame_before", -1)) != int(challenge_instance.get("winning_frame_local", -2)):
        raise UnifiedContentReviewError("winning_frame differs between independent runtime harnesses")
    if int(invariance.get("game_frame_count_before", -1)) != 420 or int(invariance.get("game_frame_count_after", -1)) != 420:
        raise UnifiedContentReviewError("Game frame count changed during profile identity separation")

    timeline_identity = timeline.get("profile_identity", {})
    if timeline_identity.get("d_presentation_profile_id") != "social_default_v1" or timeline_identity.get("delivery_profile_id") != "REVIEW_720":
        raise UnifiedContentReviewError("Timeline review profile identity mismatch")
    source_timeline = timeline.get("source_timeline", {})
    delivery_profile = timeline.get("delivery_profile", {})
    source_segments = timeline.get("source_segments", [])
    delivery_segments = timeline.get("delivery_segments", [])
    if source_timeline.get("boundary_frames") != [0, 180, 600, 780, 900] or source_timeline.get("phase_order") != ["HOOK", "GAME", "REVEAL", "CTA"]:
        raise UnifiedContentReviewError("Challenge source phase boundaries/order mismatch")
    # Validate the semantic timebase facts individually. The delivery profile may
    # legitimately carry extra metadata (for example a duration or codec hint), so
    # comparing the entire object to a five-key literal is unnecessarily brittle.
    source_fps = source_timeline.get("fps")
    source_total_frames = source_timeline.get("total_frames")
    expected_delivery_facts = {
        "profile_id": "REVIEW_720",
        "fps": 30,
        "width": 720,
        "height": 1280,
    }
    delivery_fact_mismatches = {
        key: {"expected": expected, "actual": delivery_profile.get(key)}
        for key, expected in expected_delivery_facts.items()
        if delivery_profile.get(key) != expected
    }
    source_fact_mismatches = {}
    if source_fps != 60:
        source_fact_mismatches["fps"] = {"expected": 60, "actual": source_fps}
    if source_total_frames != 900:
        source_fact_mismatches["total_frames"] = {"expected": 900, "actual": source_total_frames}

    # The real Godot delivery-timeline summary exposes delivery_profile identity,
    # FPS and dimensions, but intentionally does not duplicate total_frames there.
    # The authoritative delivery frame count is derived from its contiguous phase
    # segments (90 + 210 + 90 + 60 = 450). If a future producer additionally emits
    # delivery_profile.total_frames, treat it as a cross-check, not the source of truth.
    delivery_fps = delivery_profile.get("fps")
    delivery_counts: list[int] = []
    delivery_segments_well_formed = isinstance(delivery_segments, list) and len(delivery_segments) == 4
    if delivery_segments_well_formed:
        for segment in delivery_segments:
            count = segment.get("frame_count") if isinstance(segment, dict) else None
            if not isinstance(count, int) or isinstance(count, bool) or count < 0:
                delivery_segments_well_formed = False
                break
            delivery_counts.append(count)
    delivery_total_frames = sum(delivery_counts) if delivery_segments_well_formed else None
    if delivery_total_frames != 450:
        delivery_fact_mismatches["projected_total_frames"] = {"expected": 450, "actual": delivery_total_frames}
    declared_delivery_total = delivery_profile.get("total_frames")
    if declared_delivery_total is not None and declared_delivery_total != delivery_total_frames:
        delivery_fact_mismatches["declared_total_frames"] = {"expected": delivery_total_frames, "actual": declared_delivery_total}

    same_duration = (
        isinstance(source_fps, (int, float)) and not isinstance(source_fps, bool)
        and isinstance(source_total_frames, (int, float)) and not isinstance(source_total_frames, bool)
        and isinstance(delivery_fps, (int, float)) and not isinstance(delivery_fps, bool)
        and isinstance(delivery_total_frames, int) and not isinstance(delivery_total_frames, bool)
        and source_total_frames * delivery_fps == delivery_total_frames * source_fps
    )
    if source_fact_mismatches or delivery_fact_mismatches or not same_duration:
        raise UnifiedContentReviewError(
            "Challenge delivery profile/source timebase mismatch: "
            f"source={source_fact_mismatches or {'fps': source_fps, 'total_frames': source_total_frames}}, "
            f"delivery={delivery_fact_mismatches or {'fps': delivery_fps, 'segment_total_frames': delivery_total_frames}}, "
            f"same_duration={same_duration}"
        )
    if [int(x.get("frame_count", -1)) for x in source_segments] != [180, 420, 180, 120] or [int(x.get("frame_count", -1)) for x in delivery_segments] != [90, 210, 90, 60]:
        raise UnifiedContentReviewError("Timeline phase counts differ between source and delivery")
    if [int(x.get("start_frame", -1)) for x in delivery_segments] != [0, 90, 300, 390] or [int(x.get("end_frame", -1)) for x in delivery_segments] != [90, 300, 390, 450]:
        raise UnifiedContentReviewError("Delivery phase boundaries are not contiguous/pinned")
    timeline_ev = timeline.get("runtime_evidence", {})
    if not all(timeline_ev.get(k) is True for k in ("runtime_success", "repeat_deterministic", "simulation_frame_signature_unchanged", "winning_frame_unchanged", "metrics_unchanged")):
        raise UnifiedContentReviewError("Timeline review runtime evidence failed")
    if timeline.get("policy_state") != "PROPOSED_NOT_APPROVED":
        raise UnifiedContentReviewError("Delivery timebase proposal was silently approved")

    field_policy = windows.get("policy", {})
    window_rows = windows.get("fields", [])
    if windows.get("challenge_id") != "CHALLENGE_004" or len(window_rows) != 3 or field_policy.get("state") != "PROPOSED_NOT_APPROVED":
        raise UnifiedContentReviewError("Editorial field-window proposal identity/state mismatch")
    expected_fields = [
        ("hook", "PROPOSED_VISIBLE_WINDOW", {"start_frame": 0, "end_frame": 90, "frame_count": 90}),
        ("reveal", "SUPPRESSED_EMPTY_EDITORIAL_FIELD", None),
        ("cta", "PROPOSED_VISIBLE_WINDOW", {"start_frame": 390, "end_frame": 450, "frame_count": 60}),
    ]
    for row, (field_id, state, visibility) in zip(window_rows, expected_fields, strict=True):
        if row.get("field_id") != field_id or row.get("state") != state or row.get("visibility_range") != visibility:
            raise UnifiedContentReviewError(f"Editorial field window mismatch: {field_id}")
    if windows.get("unresolved_content_types") != {"visual_loops": "NO_EDITORIAL_FIELD_WINDOW_MAPPING_DECLARED", "visual_drills": "NO_EDITORIAL_FIELD_WINDOW_MAPPING_DECLARED"}:
        raise UnifiedContentReviewError("Non-Challenge editorial mappings must remain explicitly unresolved")
    if windows.get("identity_evidence", {}).get("d_presentation_render_model_sha256") != render_model_sha:
        raise UnifiedContentReviewError("Field-window and profile identity review use different D render-model hashes")
    win_ev = windows.get("runtime_evidence", {})
    if not all(win_ev.get(k) is True for k in ("runtime_success", "repeat_deterministic", "simulation_frame_signature_unchanged", "winning_frame_unchanged", "metrics_unchanged")):
        raise UnifiedContentReviewError("Field-window review runtime evidence failed")
    if win_ev.get("game_frame_count") != 420:
        raise UnifiedContentReviewError("Field-window review game frame count mismatch")

    # Dedicated Challenge visual-payload harness: source-timebase logical payload only.
    payload_identity = challenge_visual.get("payload_identity", {})
    payload_animation = challenge_visual.get("animation", {})
    payload_boundary = challenge_visual.get("execution_boundary", {})
    if challenge_visual.get("schema") != "C11-D-D9-CHALLENGE-VISUAL-PAYLOAD-PREVIEW-V1" or challenge_visual.get("status") != "IN_MEMORY_REVIEW_ONLY_SOURCE_TIMEBASE_VISUAL_PAYLOAD_NOT_RENDERER_INPUT":
        raise UnifiedContentReviewError("Challenge visual payload harness schema/status mismatch")
    if payload_identity.get("challenge_id") != "CHALLENGE_004" or payload_identity.get("mechanic") != "parking_v2" or payload_identity.get("presentation_profile_id") != "social_default_v1" or payload_identity.get("coordinate_space") != "CANVAS_1080X1920":
        raise UnifiedContentReviewError("Challenge visual payload identity/coordinate space mismatch")
    if not _is_sha256(challenge_visual.get("payload_sha256")):
        raise UnifiedContentReviewError("Challenge visual payload digest is malformed")
    if payload_animation.get("frame_source") != "SimulationResult.frames" or payload_animation.get("frame_record_count") != 420 or payload_animation.get("game_frame_count") != 420 or payload_animation.get("source_fps") != 60:
        raise UnifiedContentReviewError("Challenge visual payload does not preserve the 420 source-timebase GAME records")
    if payload_animation.get("simulation_telemetry_included") is not False or payload_animation.get("winning_frame_sampling_used") is not False or payload_animation.get("delivery_resampling") != "UNRESOLVED_NOT_APPLIED":
        raise UnifiedContentReviewError("Challenge visual payload unexpectedly includes telemetry or applies delivery sampling")
    frame_records_sha = payload_animation.get("frame_records_sha256")
    if not _is_sha256(frame_records_sha):
        raise UnifiedContentReviewError("Challenge visual payload frame-record digest is malformed")
    if not all(challenge_visual.get("determinism", {}).get(k) is True for k in ("runtime_repeat_equal", "payload_repeat_equal", "frame_signature_repeat_equal", "simulation_invariance")):
        raise UnifiedContentReviewError("Challenge visual payload determinism/invariance evidence failed")
    expected_payload_assets = {
        "BACKGROUND": ("res://assets/c6/garage_background.svg", "c9d8acdae725ca7726fc8ad23a046e4aac4d9e454b45db40d2c770732b31ab1e"),
        "ANIMATED_OBJECT": ("res://assets/c6/car.svg", "93a6f78d9654f7917ab2287800858a937e9c68c458cc60bf417d6f2b98c1a96d"),
        "TARGET": ("res://assets/c6/parking_target.svg", "ec2dcafd7dfc99ff501eb2d93b93906680a30c48cf0741807cbbdd915a18cfb3"),
    }
    payload_nodes = challenge_visual.get("asset_nodes")
    if not isinstance(payload_nodes, list) or len(payload_nodes) != 3:
        raise UnifiedContentReviewError("Challenge visual payload must contain exactly three canonical asset nodes")
    payload_assets = {str(row.get("role")): row for row in payload_nodes if isinstance(row, dict)}
    if set(payload_assets) != set(expected_payload_assets):
        raise UnifiedContentReviewError("Challenge visual payload asset roles mismatch")
    for role, (path_expected, hash_expected) in expected_payload_assets.items():
        row = payload_assets[role]
        if row.get("resource_path") != path_expected or row.get("sha256") != hash_expected or row.get("resource_loaded_as_texture2d") is not True:
            raise UnifiedContentReviewError(f"Challenge visual payload asset binding mismatch: {role}")
    if payload_boundary.get("renderer_activation") is not False or payload_boundary.get("renderer_dispatch_invoked") is not False or payload_boundary.get("renderer_native_input_emitted") is not False or payload_boundary.get("media_output_created") is not False or payload_boundary.get("payload_written") is not False:
        raise UnifiedContentReviewError("Challenge visual payload exceeded the in-memory review boundary")

    # Coordinate projection must consume precisely the same 420 source records.
    coord_projection = coordinate.get("projection", {})
    coord_frames = coordinate.get("projected_frames", {})
    coord_boundary = coordinate.get("execution_boundary", {})
    if coordinate.get("schema") != "C11-D-D9-RENDERER-CHALLENGE-COORDINATE-PROJECTION-PREVIEW-V1" or coordinate.get("status") != "IN_MEMORY_REVIEW_ONLY_PROJECTION_PREVIEW_NOT_RENDERER_INPUT":
        raise UnifiedContentReviewError("Coordinate projection harness schema/status mismatch")
    if coordinate.get("challenge_source_sha256") != CHALLENGE_SHA256 or coord_projection.get("state") != "PROPOSED_NOT_APPROVED" or coord_projection.get("policy_id") != "C11D_CHALLENGE_COORDINATE_PROJECTION_1080_TO_540_TO_REVIEW720_V1":
        raise UnifiedContentReviewError("Coordinate projection identity/policy state mismatch")
    for key, expected_value in (("source_coordinate_space", "CANVAS_1080X1920"),):
        if coord_projection.get(key) != expected_value:
            raise UnifiedContentReviewError(f"Coordinate projection {key} mismatch")
    for key, expected_value in (("source_records", 420), ("projected_records", 420), ("order_preserved", True), ("local_scale_preserved", True), ("other_snapshot_fields_preserved", True)):
        if coord_frames.get(key) != expected_value:
            raise UnifiedContentReviewError(f"Coordinate projection frame invariant mismatch: {key}")
    if coord_frames.get("source_records_sha256") != frame_records_sha or not _is_sha256(coord_frames.get("projected_records_sha256")):
        raise UnifiedContentReviewError("Coordinate projection source records do not match the Challenge visual payload")
    actual_stages = coord_projection.get("stage_scales")
    expected_stages = [[0.5, 0.5], [4 / 3, 4 / 3]]
    if not isinstance(actual_stages, list) or len(actual_stages) != len(expected_stages):
        raise UnifiedContentReviewError("Coordinate projection stage_scales shape mismatch")
    for actual_row, expected_row in zip(actual_stages, expected_stages):
        if not isinstance(actual_row, list) or len(actual_row) != 2 or any(not isinstance(a, (int, float)) or isinstance(a, bool) or not math.isclose(float(a), float(e), rel_tol=1e-5, abs_tol=1e-5) for a, e in zip(actual_row, expected_row)):
            raise UnifiedContentReviewError("Coordinate projection stage_scales values mismatch")
    actual_combined = coord_projection.get("combined_scale")
    if not isinstance(actual_combined, list) or len(actual_combined) != 2 or any(not isinstance(a, (int, float)) or isinstance(a, bool) or not math.isclose(float(a), 2 / 3, rel_tol=1e-5, abs_tol=1e-5) for a in actual_combined):
        raise UnifiedContentReviewError("Coordinate projection combined_scale values mismatch")
    if coord_projection.get("sampling_or_interpolation") != "UNRESOLVED_NOT_APPLIED":
        raise UnifiedContentReviewError("Coordinate projection must not apply delivery sampling/interpolation")
    if not all(coordinate.get("determinism", {}).get(k) is True for k in ("runtime_repeat_equal", "projection_repeat_equal", "source_frame_signature_repeat_equal")):
        raise UnifiedContentReviewError("Coordinate projection determinism evidence failed")
    if not all(coordinate.get("simulation_invariance", {}).get(k) is True for k in ("frame_signature_unchanged", "winning_frame_unchanged", "metrics_unchanged", "frame_count_unchanged")):
        raise UnifiedContentReviewError("Coordinate projection altered source simulation state")
    if coord_boundary.get("renderer_activation") is not False or coord_boundary.get("renderer_dispatch_invoked") is not False or coord_boundary.get("renderer_native_input_emitted") is not False or coord_boundary.get("media_created") is not False or coord_boundary.get("projected_payload_written") is not False:
        raise UnifiedContentReviewError("Coordinate projection exceeded the in-memory review boundary")
    coordinate_assets = coordinate.get("assets")
    if not isinstance(coordinate_assets, list) or len(coordinate_assets) != 3:
        raise UnifiedContentReviewError("Coordinate projection must preserve exactly three asset nodes")
    asset_signatures = {(row.get("resource_path"), row.get("sha256"), row.get("role")) for row in coordinate_assets if isinstance(row, dict)}
    expected_asset_signatures = {(path, digest, role) for role, (path, digest) in expected_payload_assets.items()}
    if asset_signatures != expected_asset_signatures:
        raise UnifiedContentReviewError("Coordinate projection asset identities differ from the Challenge visual payload")
    if not _is_sha256(coordinate.get("source_lineage") and sha256_json(coordinate["source_lineage"])):
        raise UnifiedContentReviewError("Coordinate projection source lineage summary is malformed")
    challenge_payload_lineage = {row.get("path"): row.get("sha256") for row in challenge_visual.get("source_lineage", []) if isinstance(row, dict)}
    coordinate_lineage = {row.get("path"): row.get("sha256") for row in coordinate.get("source_lineage", []) if isinstance(row, dict)}
    for path, expected_sha in (("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_PREVIEW_V1.json", "67daa1f83ac151906059695bb4d87974819c2d16d3715b78b00657bfdac54f7a"), ("challenges/CHALLENGE_004.json", CHALLENGE_SHA256), ("release/C11C_FREEZE_PACKAGE_MANIFEST.json", FROZEN_MANIFEST_SHA256)):
        if challenge_payload_lineage.get(path) != expected_sha:
            raise UnifiedContentReviewError(f"Challenge visual payload source lineage mismatch: {path}")
    for path, expected_sha in (("definitions/c11d/production/D_RENDERER_CHALLENGE_COORDINATE_PROJECTION_V1.json", "c1caf8e640595bc89957f17ef8bbd7abe80a92cac18cf77974633a1ddde0e264"), ("challenges/CHALLENGE_004.json", CHALLENGE_SHA256), ("release/C11C_FREEZE_PACKAGE_MANIFEST.json", FROZEN_MANIFEST_SHA256)):
        if coordinate_lineage.get(path) != expected_sha:
            raise UnifiedContentReviewError(f"Coordinate projection source lineage mismatch: {path}")

    # Review the proposal as a deterministic mapping preview only. Nothing here
    # applies resampling to the Challenge visual payload or emits renderer input.
    root = _root(project_root)
    try:
        sample_selection_preview = build_sample_selection_preview(root)
        validate_sample_selection_preview(sample_selection_preview, root)
    except ChallengeSampleSelectionError as exc:
        raise UnifiedContentReviewError(f"Challenge sample-selection proposal preview invalid: {exc}") from exc
    proposal_sha = "3e278481afe9d66458f05f29c15275819af49f9b68120b6a0b39dda2e9715cf3"
    proposal = sample_selection_preview
    sample_time = proposal.get("source_timebase", {})
    delivery_time = proposal.get("delivery_timebase", {})
    game = proposal.get("game_segment", {})
    anchor = proposal.get("anchor_mapping", {})
    assessment = proposal.get("sample_assessment", {})
    sample_policy = proposal.get("sampling_policy", {})
    source_game = next((item for item in source_segments if isinstance(item, dict) and item.get("phase") == "GAME"), {})
    delivery_game = next((item for item in delivery_segments if isinstance(item, dict) and item.get("phase") == "GAME"), {})
    if proposal.get("proposal_state") != "PROPOSED_NOT_APPROVED" or proposal.get("proposal_contract_sha256") != proposal_sha:
        raise UnifiedContentReviewError("Challenge sample-selection proposal identity/state mismatch")
    if (sample_time.get("fps"), sample_time.get("total_frames"), delivery_time.get("fps"), delivery_time.get("total_frames")) != (60, 900, 30, 450):
        raise UnifiedContentReviewError("Challenge sample-selection proposal timebase mismatch")
    if (game.get("source_start_frame"), game.get("source_end_frame_exclusive"), game.get("source_snapshot_count"), game.get("delivery_start_frame"), game.get("delivery_end_frame_exclusive"), game.get("delivery_snapshot_count")) != (source_game.get("start_frame"), source_game.get("end_frame"), source_game.get("frame_count"), delivery_game.get("start_frame"), delivery_game.get("end_frame"), delivery_game.get("frame_count")):
        raise UnifiedContentReviewError("Challenge sample-selection GAME window does not match delivery timeline")
    winning_local = challenge_instance.get("winning_frame_local")
    if anchor.get("winning_frame_local_game_index") != winning_local:
        raise UnifiedContentReviewError("Challenge sample-selection anchor does not match runtime winning_frame")
    if anchor.get("winning_frame_absolute_source_index") != source_game.get("start_frame", -1) + int(winning_local):
        raise UnifiedContentReviewError("Challenge sample-selection absolute source anchor mismatch")
    winning_delivery_local = anchor.get("winning_delivery_game_frame_index")
    samples = proposal.get("samples", [])
    if not isinstance(winning_delivery_local, int) or isinstance(winning_delivery_local, bool) or not (0 <= winning_delivery_local < len(samples)):
        raise UnifiedContentReviewError("Challenge sample-selection delivery anchor is out of range")
    selected_anchor = samples[winning_delivery_local]
    if selected_anchor.get("source_game_snapshot_index") != winning_local or selected_anchor.get("source_absolute_frame_index") != anchor.get("winning_frame_absolute_source_index"):
        raise UnifiedContentReviewError("Challenge winning_frame is not represented by the proposed selected-sample cadence")
    if anchor.get("anchor_mapping_status") != "EXACT_SELECTED_SAMPLE_AND_DELIVERY_TICK" or anchor.get("winning_source_snapshot_selected") is not True:
        raise UnifiedContentReviewError("Challenge winning_frame does not land on the proposed delivery tick")
    if (assessment.get("source_snapshot_count"), assessment.get("delivery_snapshot_count"), assessment.get("stride"), assessment.get("first_source_snapshot_index"), assessment.get("last_source_snapshot_index"), assessment.get("source_indices_follow_stride"), assessment.get("interpolation_used")) != (420, 210, 2, 0, 418, True, False):
        raise UnifiedContentReviewError("Challenge sample-selection cadence assessment mismatch")
    if sample_policy.get("interpolation") != "NONE" or sample_policy.get("synthetic_or_interpolated_simulation_states") is not False or sample_policy.get("simulation_result_mutation") is not False or sample_policy.get("canonical_payload_mutation") is not False:
        raise UnifiedContentReviewError("Challenge sample-selection proposal exceeds the non-mutating no-interpolation boundary")
    if anchor.get("close_calls_used_for_timing") is not False or anchor.get("close_calls_count") != 1:
        raise UnifiedContentReviewError("Challenge sample-selection proposal incorrectly uses close_calls as timing")

    return {
        "loop": loop,
        "drill": drill,
        "challenge": challenge_instance,
        "identity": identity,
        "timeline": timeline,
        "windows": windows,
        "challenge_visual_payload": challenge_visual,
        "coordinate_projection": coordinate,
        "coordinate_projected_frames_sha256": coord_frames["projected_records_sha256"],
        "sample_selection_preview": sample_selection_preview,
        "challenge_visual_payload_sha256": challenge_visual["payload_sha256"],
        "d_render_model_sha256": render_model_sha,
    }


def build_review_manifest(summaries: Mapping[str, dict[str, Any]], harness_evidence: list[dict[str, Any]], contract: dict[str, Any], contract_path: Path) -> dict[str, Any]:
    joined = validate_harness_summaries(summaries)
    loop, drill, challenge = joined["loop"], joined["drill"], joined["challenge"]
    timeline, windows = joined["timeline"], joined["windows"]
    items = [
        {
            "content_type": "visual_loops",
            "selection": loop.get("selection", {}),
            "identity": {"instance_id": loop["instance_id"], "seed": loop["seed"], "variation_index": loop["variation_index"], "payload_instance_sha256": loop["payload_instance_sha256"], "authoring_envelope_sha256": loop["authoring_envelope_sha256"]},
            "timing": {"fps": loop["fps"], "duration_seconds": loop["duration_seconds"], "frame_count": loop["frame_count"], "delivery_profile_id": "REVIEW_720"},
            "editorial_review": {"field_window_mapping": "UNRESOLVED_NO_MAPPING_DECLARED", "visibility_windows": None},
            "materialization": "IN_MEMORY_ONLY_VISUAL_PAYLOAD_MATERIALIZED",
        },
        {
            "content_type": "visual_drills",
            "selection": drill.get("selection", {}),
            "identity": {"instance_id": drill["instance_id"], "seed": drill["seed"], "variation_index": drill["variation_index"], "payload_instance_sha256": drill["payload_instance_sha256"], "authoring_envelope_sha256": drill["authoring_envelope_sha256"]},
            "timing": {"fps": drill["fps"], "duration_seconds": drill["duration_seconds"], "frame_count": drill["frame_count"], "delivery_profile_id": "REVIEW_720"},
            "editorial_review": {"field_window_mapping": "UNRESOLVED_NO_MAPPING_DECLARED", "visibility_windows": None},
            "materialization": "IN_MEMORY_ONLY_VISUAL_PAYLOAD_MATERIALIZED",
        },
        {
            "content_type": "challenges",
            "selection": {"challenge_id": challenge["challenge_id"], "mechanic": challenge["mechanic"], "mechanic_version": challenge["mechanic_version"], "asset_family": challenge["asset_family"], "asset_family_version": challenge["asset_family_version"]},
            "identity": {"seed_requested": challenge["seed_requested"], "seed_used": challenge["seed_used"], "runtime_output_sha256": challenge["runtime_output_sha256"], "simulation_frame_signature_sha256": challenge["frame_signature_sha256"], "d_presentation_render_model_sha256": joined["d_render_model_sha256"], "challenge_visual_payload_sha256": joined["challenge_visual_payload_sha256"], "source_frame_records_sha256": joined["challenge_visual_payload"]["animation"]["frame_records_sha256"], "projected_frame_records_sha256": joined["coordinate_projected_frames_sha256"], "legacy_runtime_profile_id": "test_master_11s", "d_presentation_profile_id": "social_default_v1"},
            "timing": {"source_fps": 60, "source_total_frames": 900, "game_frame_count": 420, "delivery_profile_id": "REVIEW_720", "delivery_fps": 30, "delivery_total_frames": 450, "delivery_segments": timeline["delivery_segments"], "field_windows_proposal_sha256": windows["proposal_sha256"]},
            "editorial_review": {"field_window_mapping": "CHALLENGE_PROPOSAL_2_VISIBLE_FIELDS_1_EMPTY_SUPPRESSED", "fields": windows["fields"], "policy_state": "PROPOSED_NOT_APPROVED"},
            "materialization": "IN_MEMORY_ONLY_SOURCE_TIMEBASE_VISUAL_PAYLOAD_MATERIALIZED_NOT_RENDERER_INPUT",
            "coordinate_projection": {"policy_id": joined["coordinate_projection"]["projection"]["policy_id"], "state": "PROPOSED_NOT_APPROVED", "projected_records": 420, "projected_records_sha256": joined["coordinate_projected_frames_sha256"], "combined_scale": joined["coordinate_projection"]["projection"]["combined_scale"]},
            "sample_selection": {"policy_id": joined["sample_selection_preview"]["proposal_id"], "state": joined["sample_selection_preview"]["proposal_state"], "proposal_contract_sha256": joined["sample_selection_preview"]["proposal_contract_sha256"], "preview_sha256": joined["sample_selection_preview"]["preview_sha256"], "source_snapshot_count": joined["sample_selection_preview"]["sample_assessment"]["source_snapshot_count"], "delivery_snapshot_count": joined["sample_selection_preview"]["sample_assessment"]["delivery_snapshot_count"], "stride": joined["sample_selection_preview"]["sample_assessment"]["stride"], "sampling_origin": joined["sample_selection_preview"]["sampling_policy"]["sampling_origin"], "first_source_snapshot_index": joined["sample_selection_preview"]["sample_assessment"]["first_source_snapshot_index"], "last_source_snapshot_index": joined["sample_selection_preview"]["sample_assessment"]["last_source_snapshot_index"], "interpolation": joined["sample_selection_preview"]["sampling_policy"]["interpolation"], "winning_frame_local_game_index": joined["sample_selection_preview"]["anchor_mapping"]["winning_frame_local_game_index"], "winning_frame_absolute_source_index": joined["sample_selection_preview"]["anchor_mapping"]["winning_frame_absolute_source_index"], "winning_delivery_game_frame_index": joined["sample_selection_preview"]["anchor_mapping"]["winning_delivery_game_frame_index"], "winning_absolute_delivery_frame_index": joined["sample_selection_preview"]["anchor_mapping"]["winning_absolute_delivery_frame_index"], "anchor_mapping_status": joined["sample_selection_preview"]["anchor_mapping"]["anchor_mapping_status"], "close_calls_count": joined["sample_selection_preview"]["anchor_mapping"]["close_calls_count"], "close_calls_used_for_timing": joined["sample_selection_preview"]["anchor_mapping"]["close_calls_used_for_timing"], "renderer_native_input_emitted": False},
        },
    ]
    unresolved = list(EXPECTED_UNRESOLVED_GATES)
    report: dict[str, Any] = {
        "schema": OUTPUT_SCHEMA,
        "schema_version": "1.0",
        "status": "REVIEW_CHAIN_CONSISTENT_NOT_VIDEO_READY",
        "frozen_c11c_manifest_sha256": FROZEN_MANIFEST_SHA256,
        "contract_sha256": sha256_bytes(contract_path.read_bytes()),
        "source_lineage": copy.deepcopy(contract["source_lineage"]),
        "content_items": items,
        "harness_evidence": harness_evidence,
        "cross_artifact_checks": {
            "c11c_manifest_identity": True,
            "challenge_source_identity": True,
            "payload_repeat_determinism": True,
            "profile_identity_parity": True,
            "delivery_timeline_parity": True,
            "field_window_parity": True,
            "simulation_invariance": True,
            "governance_boundary": True,
            "challenge_visual_payload_identity": True,
            "coordinate_projection_parity": True,
            "challenge_sample_selection_proposal_parity": True,
        },
        "unresolved_gates": unresolved,
        "approval_state": copy.deepcopy(contract["approval_state"]),
        "execution_boundary": copy.deepcopy(contract["execution_boundary"]),
    }
    report["review_manifest_sha256"] = sha256_json(report)
    return report


def validate_review_manifest(report: dict[str, Any], schema: dict[str, Any]) -> None:
    try:
        import jsonschema  # type: ignore
    except ImportError:
        jsonschema = None
    if jsonschema is not None:
        try:
            jsonschema.Draft202012Validator(schema).validate(report)
        except jsonschema.ValidationError as exc:
            raise UnifiedContentReviewError(f"Unified review manifest failed JSON Schema: {exc.message}") from exc
    if report.get("schema") != OUTPUT_SCHEMA or report.get("schema_version") != "1.0":
        raise UnifiedContentReviewError("Output manifest identity/version mismatch")
    if report.get("status") != "REVIEW_CHAIN_CONSISTENT_NOT_VIDEO_READY":
        raise UnifiedContentReviewError("Review status must never be promoted to video-ready")
    if report.get("frozen_c11c_manifest_sha256") != FROZEN_MANIFEST_SHA256:
        raise UnifiedContentReviewError("Frozen C11-C manifest identity mismatch")
    if not _is_sha256(report.get("contract_sha256")):
        raise UnifiedContentReviewError("Unified review contract digest is malformed")
    if report.get("source_lineage") != [{"path": path, "sha256": digest} for path, digest in EXPECTED_SOURCE_LINEAGE]:
        raise UnifiedContentReviewError("Unified review source lineage differs from the pinned contract")
    items = report.get("content_items", [])
    if [x.get("content_type") for x in items] != EXPECTED_TYPES:
        raise UnifiedContentReviewError("The unified manifest must contain the three content types in canonical order")
    if report.get("cross_artifact_checks") != {key: True for key in ("c11c_manifest_identity", "challenge_source_identity", "payload_repeat_determinism", "profile_identity_parity", "delivery_timeline_parity", "field_window_parity", "simulation_invariance", "governance_boundary", "challenge_visual_payload_identity", "coordinate_projection_parity", "challenge_sample_selection_proposal_parity")}:
        raise UnifiedContentReviewError("Cross-artifact consistency checks must all pass before the review manifest is emitted")
    gates = report.get("unresolved_gates", [])
    if gates != EXPECTED_UNRESOLVED_GATES:
        raise UnifiedContentReviewError("The canonical unresolved pre-video gates must remain explicit and in fixed order")
    evidence = report.get("harness_evidence", [])
    if [x.get("name") for x in evidence] != [x["name"] for x in EXPECTED_HARNESSES]:
        raise UnifiedContentReviewError("Harness evidence identity/order mismatch")
    for item in evidence:
        if not _is_sha256(item.get("script_sha256")) or not _is_sha256(item.get("summary_sha256")) or item.get("exit_code") != 0 or item.get("pass_marker_seen") is not True or item.get("runtime_error_log_seen") is not False:
            raise UnifiedContentReviewError("Harness evidence record is incomplete or not clean")
    items_by_type = {x.get("content_type"): x for x in items}
    loop = items_by_type["visual_loops"]
    drill = items_by_type["visual_drills"]
    challenge = items_by_type["challenges"]
    if loop.get("timing") != {"fps": 30, "duration_seconds": 20.0, "frame_count": 600, "delivery_profile_id": "REVIEW_720"}:
        raise UnifiedContentReviewError("Unified Visual Loop timing mismatch")
    if drill.get("timing") != {"fps": 30, "duration_seconds": 21.0, "frame_count": 630, "delivery_profile_id": "REVIEW_720"}:
        raise UnifiedContentReviewError("Unified Visual Drill timing mismatch")
    challenge_timing = challenge.get("timing", {})
    if (challenge_timing.get("source_fps"), challenge_timing.get("source_total_frames"), challenge_timing.get("game_frame_count"), challenge_timing.get("delivery_profile_id"), challenge_timing.get("delivery_fps"), challenge_timing.get("delivery_total_frames")) != (60, 900, 420, "REVIEW_720", 30, 450):
        raise UnifiedContentReviewError("Unified Challenge source/delivery timing mismatch")
    if loop.get("editorial_review", {}).get("field_window_mapping") != "UNRESOLVED_NO_MAPPING_DECLARED" or drill.get("editorial_review", {}).get("field_window_mapping") != "UNRESOLVED_NO_MAPPING_DECLARED":
        raise UnifiedContentReviewError("Visual Loop/Drill field mappings must remain unresolved until explicitly defined")
    if challenge.get("materialization") != "IN_MEMORY_ONLY_SOURCE_TIMEBASE_VISUAL_PAYLOAD_MATERIALIZED_NOT_RENDERER_INPUT" or challenge.get("editorial_review", {}).get("policy_state") != "PROPOSED_NOT_APPROVED":
        raise UnifiedContentReviewError("Challenge review must record the in-memory payload while keeping the editorial policy unapproved")
    coord = challenge.get("coordinate_projection", {})
    if coord.get("state") != "PROPOSED_NOT_APPROVED" or coord.get("projected_records") != 420 or not _is_sha256(coord.get("projected_records_sha256")):
        raise UnifiedContentReviewError("Challenge coordinate projection evidence is missing or incorrectly approved")
    sample = challenge.get("sample_selection", {})
    expected_sample = {
        "policy_id": "C11D_CHALLENGE_SAMPLE_EVERY_SECOND_SOURCE_SNAPSHOT_NO_INTERPOLATION_V1",
        "state": "PROPOSED_NOT_APPROVED",
        "proposal_contract_sha256": "3e278481afe9d66458f05f29c15275819af49f9b68120b6a0b39dda2e9715cf3",
        "source_snapshot_count": 420, "delivery_snapshot_count": 210, "stride": 2,
        "sampling_origin": "ZERO_BASED_GAME_SEGMENT_LOCAL_INDEX",
        "first_source_snapshot_index": 0, "last_source_snapshot_index": 418,
        "interpolation": "NONE", "winning_frame_local_game_index": 394,
        "winning_frame_absolute_source_index": 574, "winning_delivery_game_frame_index": 197,
        "winning_absolute_delivery_frame_index": 287,
        "anchor_mapping_status": "EXACT_SELECTED_SAMPLE_AND_DELIVERY_TICK",
        "close_calls_count": 1, "close_calls_used_for_timing": False, "renderer_native_input_emitted": False,
    }
    if sample.get("preview_sha256") is None or not _is_sha256(sample.get("preview_sha256")):
        raise UnifiedContentReviewError("Challenge sample-selection preview digest is malformed")
    if sample != {**expected_sample, "preview_sha256": sample.get("preview_sha256")}:
        raise UnifiedContentReviewError("Challenge sample-selection proposal summary mismatch or approval drift")
    if report.get("approval_state", {}).get("simulation_sample_selection_policy_approved") is not False or report.get("approval_state", {}).get("interpolation_policy_approved") is not False:
        raise UnifiedContentReviewError("Unified review cannot approve simulation sample selection or interpolation")
    challenge_identity = challenge.get("identity", {})
    if not _is_sha256(challenge_identity.get("challenge_visual_payload_sha256")) or not _is_sha256(challenge_identity.get("source_frame_records_sha256")) or not _is_sha256(challenge_identity.get("projected_frame_records_sha256")):
        raise UnifiedContentReviewError("Challenge visual payload or projected-record identities are malformed")
    if report.get("execution_boundary") != {
        "mode": "SEQUENTIAL_HEADLESS_IN_MEMORY_REVIEW_ONLY",
        "persistent_report_written": False,
        "payload_files_written": False,
        "renderer_native_input_emitted": False,
        "renderer_dispatch_invoked": False,
        "renderer_activation": False,
        "production_execution": False,
        "media_created": False,
        "c11c_source_mutation": False,
        "video_render_ready": False,
        "d4_8": "BLOCKED",
        "release_authority": "NONE",
    }:
        raise UnifiedContentReviewError("Execution/governance boundary changed")
    supplied = report.get("review_manifest_sha256", "")
    if not _is_sha256(supplied):
        raise UnifiedContentReviewError("Review manifest digest is malformed")
    unsigned = dict(report)
    unsigned.pop("review_manifest_sha256", None)
    if sha256_json(unsigned) != supplied:
        raise UnifiedContentReviewError("Review manifest digest mismatch")
