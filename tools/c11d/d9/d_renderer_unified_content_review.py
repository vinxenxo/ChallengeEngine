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
from d_renderer_challenge_coordinate_sample_composition import (
    CompositionContractError,
    validate_contract as validate_coordinate_sample_composition_contract,
)
from d_renderer_loop_drill_editorial_field_windows import (
    FieldWindowProposalError,
    validate_contract as validate_loop_drill_editorial_field_window_contract,
)
from d_renderer_challenge_temporal_alignment_policy import (
    ChallengeTemporalAlignmentError,
    build_preview as build_temporal_alignment_preview,
    validate_preview as validate_temporal_alignment_preview,
)
from d_renderer_unified_delivery_timebase_policy import (
    EXPECTED_MATRIX as EXPECTED_UNIFIED_DELIVERY_MATRIX,
    EXPECTED_TARGET_PROFILE as EXPECTED_UNIFIED_DELIVERY_PROFILE,
    POLICY_ID as UNIFIED_DELIVERY_POLICY_ID,
    UnifiedDeliveryPolicyError,
    build_preview as build_unified_delivery_policy_preview,
    validate_preview as validate_unified_delivery_policy_preview,
)
from d_renderer_unified_audio_music_delivery_policy import (
    EXPECTED_MATRIX as EXPECTED_AUDIO_DELIVERY_MATRIX,
    EXPECTED_PROFILE as EXPECTED_AUDIO_DELIVERY_PROFILE,
    POLICY_ID as UNIFIED_AUDIO_MUSIC_POLICY_ID,
    UnifiedAudioMusicDeliveryPolicyError,
    build_preview as build_unified_audio_music_policy_preview,
    validate_preview as validate_unified_audio_music_policy_preview,
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
    ("definitions/c11d/production/D_RENDERER_CHALLENGE_COORDINATE_SAMPLE_COMPOSITION_PROPOSAL_V1.json", "72aa659dfc464ce8f2205cc483c18cdff96b82e55f3651102310f9f83ce897b4"),
    ("definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json", "25fe4aaaaa94a80dbabcbf92533ff9c19a9d61cc0b3173cb0cd986a62701fd57"),
    ("definitions/c11d/production/D_RENDERER_CHALLENGE_TEMPORAL_ALIGNMENT_POLICY_PROPOSAL_V1.json", "bf8084f4d6e1257ac3aa594cd5a5625a6814d9022643774f152392558a224dd4"),
    ("definitions/c11d/production/D_RENDERER_UNIFIED_DELIVERY_TIMEBASE_POLICY_PROPOSAL_V1.json", "1e190d5bc1541d04f93052ccc27afd8a3ed289d9c2271d364ebbae6548412921"),
    ("definitions/c11d/production/D_RENDERER_UNIFIED_AUDIO_MUSIC_DELIVERY_POLICY_PROPOSAL_V1.json", "12d9000b73f09318a005e8f1d76e2efb2777469715dfeb7d686760600ba11238"),
]
EXPECTED_UNRESOLVED_GATES = [
    "VISUAL_LOOP_EDITORIAL_FIELD_MAPPING_NOT_APPROVED",
    "VISUAL_DRILL_EDITORIAL_FIELD_MAPPING_NOT_APPROVED",
    "CHALLENGE_SIMULATION_SAMPLE_SELECTION_AND_INTERPOLATION_UNRESOLVED",
    "CHALLENGE_COORDINATE_PROJECTION_POLICY_NOT_APPROVED",
    "DELIVERY_TIMEBASE_PROJECTION_POLICY_NOT_APPROVED",
    "AUDIO_MUSIC_DELIVERY_AND_EDITORIAL_POLICY_NOT_APPROVED",
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
    if policy.get("challenge_coordinate_sample_composition") != "PROPOSED_NOT_APPROVED_INCLUDED_IN_UNIFIED_REVIEW_NOT_APPLIED":
        raise UnifiedContentReviewError("Coordinate/sample composition must remain proposal-only and must not be applied here")
    if policy.get("visual_loop_editorial_mapping") != "PROPOSED_NOT_APPROVED_INCLUDED_IN_UNIFIED_REVIEW_NOT_APPLIED" or policy.get("visual_drill_editorial_mapping") != "PROPOSED_NOT_APPROVED_INCLUDED_IN_UNIFIED_REVIEW_NOT_APPLIED":
        raise UnifiedContentReviewError("Loop/Drill editorial field-window mappings must be present for review only and remain unapproved")
    if policy.get("loop_drill_editorial_field_windows") != "PROPOSED_NOT_APPROVED_INCLUDED_IN_UNIFIED_REVIEW_NOT_APPLIED":
        raise UnifiedContentReviewError("Loop/Drill editorial field-window proposal must remain review-only and unapplied")
    if policy.get("challenge_temporal_alignment") != "PROPOSED_NOT_APPROVED_INCLUDED_IN_UNIFIED_REVIEW_NOT_APPLIED":
        raise UnifiedContentReviewError("Challenge temporal alignment must remain proposal-only and unapplied")
    if policy.get("unified_delivery_timebase_policy") != "PROPOSED_NOT_APPROVED_INCLUDED_IN_UNIFIED_REVIEW_NOT_APPLIED":
        raise UnifiedContentReviewError("Unified delivery timebase policy must remain proposal-only and unapplied")
    if policy.get("unified_audio_music_delivery_policy") != "PROPOSED_NOT_APPROVED_INCLUDED_IN_UNIFIED_REVIEW_NOT_APPLIED":
        raise UnifiedContentReviewError("Unified audio/music delivery policy must remain proposal-only and unapplied")
    approval_state = contract.get("approval_state", {})
    if (
        approval_state.get("simulation_sample_selection_policy_approved") is not False
        or approval_state.get("interpolation_policy_approved") is not False
        or approval_state.get("coordinate_sample_composition_policy_approved") is not False
        or approval_state.get("loop_editorial_field_mapping_approved") is not False
        or approval_state.get("drill_editorial_field_mapping_approved") is not False
        or approval_state.get("loop_drill_editorial_field_window_policy_approved") is not False
        or approval_state.get("challenge_temporal_alignment_policy_approved") is not False
        or approval_state.get("unified_delivery_timebase_policy_approved") is not False
        or approval_state.get("audio_delivery_profile_policy_approved") is not False
        or approval_state.get("music_selection_policy_approved") is not False
        or approval_state.get("mixing_policy_approved") is not False
        or approval_state.get("loudness_policy_approved") is not False
        or approval_state.get("audio_timeline_policy_approved") is not False
    ):
        raise UnifiedContentReviewError("Unified review cannot approve sample/composition, editorial, delivery-timebase or audio/music policies")
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
    root = _root(project_root)

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

    # Join the Loop/Drill editorial-window proposal as metadata only. The Godot
    # payload harness deliberately omits raw editorial text, so this stage records
    # the mapping rules and exact payload timing without fabricating per-field windows.
    try:
        loop_drill_editorial = validate_loop_drill_editorial_field_window_contract(root)
    except FieldWindowProposalError as exc:
        raise UnifiedContentReviewError(f"Loop/Drill editorial field-window proposal invalid: {exc}") from exc
    editorial_contract = loop_drill_editorial["contract"]
    editorial_policy = editorial_contract.get("mapping_policy", {})
    editorial_fixtures = loop_drill_editorial["fixtures"]
    if editorial_contract.get("status") != "PROPOSAL_ONLY_NOT_RENDERER_INPUT" or editorial_policy.get("state") != "PROPOSED_NOT_APPROVED":
        raise UnifiedContentReviewError("Loop/Drill editorial field-window policy must remain proposal-only")
    expected_visible_rules = [
        {"field_id": "title", "target_region": "HEADER", "condition": "NONEMPTY_STRING", "window_rule": "FULL_CONTINUOUS_PAYLOAD_SPAN"},
        {"field_id": "subtitle", "target_region": "HEADER", "condition": "NONEMPTY_STRING", "window_rule": "FULL_CONTINUOUS_PAYLOAD_SPAN"},
        {"field_id": "call_to_action", "target_region": "FOOTER", "condition": "NONEMPTY_STRING", "window_rule": "FULL_CONTINUOUS_PAYLOAD_SPAN"},
    ]
    if editorial_policy.get("visible_fields") != expected_visible_rules:
        raise UnifiedContentReviewError("Loop/Drill editorial field mapping rules drift")
    if editorial_policy.get("metadata_only_fields") != [{"field_id": "language", "rule": "METADATA_ONLY_NO_VISIBILITY_WINDOW"}]:
        raise UnifiedContentReviewError("Loop/Drill language must remain metadata-only")
    if editorial_policy.get("empty_value_rule") != "SUPPRESS_FIELD_AND_ASSIGN_NO_WINDOW" or editorial_policy.get("interval_rule") != "START_FRAME_INCLUSIVE_END_FRAME_EXCLUSIVE":
        raise UnifiedContentReviewError("Loop/Drill editorial empty-value or interval convention drift")
    if (editorial_policy.get("window_formula"), editorial_policy.get("payload_frame_count_authority")) != (
        "NONEMPTY_VISUAL_FIELD_WINDOW_EQUALS_[0,GENERATED_PAYLOAD_FRAME_COUNT)",
        "REQUEST_SCOPED_IN_MEMORY_MATERIALIZED_PAYLOAD_INSTANCE",
    ):
        raise UnifiedContentReviewError("Loop/Drill editorial window formula or timing authority drift")
    for row, content_type in ((loop, "visual_loops"), (drill, "visual_drills")):
        fixture = editorial_fixtures[content_type]
        for key in ("instance_id", "payload_instance_sha256", "fps", "frame_count", "duration_seconds"):
            if row.get(key) != fixture.get(key):
                raise UnifiedContentReviewError(f"Loop/Drill editorial proposal payload identity/timing mismatch: {content_type}.{key}")
        if fixture.get("delivery_profile_id") != "REVIEW_720":
            raise UnifiedContentReviewError(f"Loop/Drill editorial proposal fixture delivery profile mismatch: {content_type}")
        if row.get("selection") != fixture.get("selection"):
            raise UnifiedContentReviewError(f"Loop/Drill editorial proposal selection mismatch: {content_type}")
    if editorial_contract.get("approval_state", {}).get("loop_editorial_field_mapping_approved") is not False or editorial_contract.get("approval_state", {}).get("drill_editorial_field_mapping_approved") is not False or editorial_contract.get("approval_state", {}).get("field_window_policy_approved") is not False:
        raise UnifiedContentReviewError("Loop/Drill editorial approval locks must remain false")
    editorial_contract_sha256 = sha256_bytes((root / "definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json").read_bytes())
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

    # Join the spatial and temporal proposals without materializing a composed
    # snapshot payload. This checks policy/contract parity only; the renderer and
    # canonical simulation remain untouched.
    try:
        coordinate_sample_composition = validate_coordinate_sample_composition_contract(root)
    except CompositionContractError as exc:
        raise UnifiedContentReviewError(f"Challenge coordinate/sample composition proposal invalid: {exc}") from exc
    composition_contract = coordinate_sample_composition["contract"]
    composition_case = composition_contract.get("case", {})
    composition_spatial = composition_contract.get("spatial_projection", {})
    composition_ops = composition_contract.get("composition", {})
    composition_facts = composition_contract.get("expected_review_facts", {})
    if composition_contract.get("status") != "PROPOSED_NOT_APPROVED_NOT_FROZEN":
        raise UnifiedContentReviewError("Coordinate/sample composition must remain unapproved and unfrozen")
    expected_composition_case = {
        "challenge_id": "CHALLENGE_004", "mechanic": "parking_v2",
        "source_fps": 60, "delivery_fps": 30,
        "source_total_frames": 900, "delivery_total_frames": 450,
        "game_source_start_frame": source_game.get("start_frame"),
        "game_source_end_frame_exclusive": source_game.get("end_frame"),
        "game_delivery_start_frame": delivery_game.get("start_frame"),
        "game_delivery_end_frame_exclusive": delivery_game.get("end_frame"),
        "source_game_snapshot_count": coord_frames.get("source_records"),
        "delivery_game_snapshot_count": assessment.get("delivery_snapshot_count"),
        "source_to_delivery_stride": assessment.get("stride"),
        "sampling_origin": sample_policy.get("sampling_origin"),
        "first_selected_source_local_index": assessment.get("first_source_snapshot_index"),
        "last_selected_source_local_index": assessment.get("last_source_snapshot_index"),
        "winning_frame_local_game_index": anchor.get("winning_frame_local_game_index"),
        "winning_frame_absolute_source_index": anchor.get("winning_frame_absolute_source_index"),
        "winning_frame_delivery_local_game_index": anchor.get("winning_delivery_game_frame_index"),
        "winning_frame_absolute_delivery_index": anchor.get("winning_absolute_delivery_frame_index"),
        "close_calls": anchor.get("close_calls_count"),
    }
    for key, expected_value in expected_composition_case.items():
        if composition_case.get(key) != expected_value:
            raise UnifiedContentReviewError(f"Coordinate/sample composition case parity mismatch: {key}")
    if composition_ops.get("operation_order") != ["PROJECT_ALL_GAME_COORDINATES_IN_ORIGINAL_ORDER", "SELECT_EVEN_ZERO_BASED_GAME_LOCAL_INDICES"]:
        raise UnifiedContentReviewError("Coordinate/sample composition operation order drift")
    if (composition_ops.get("spatial_projection_record_count"), composition_ops.get("composed_delivery_record_count"), composition_ops.get("sampling_stride"), composition_ops.get("interpolation"), composition_ops.get("resampling")) != (420, 210, 2, "NONE", "NONE_BEYOND_EXPLICIT_EVERY_SECOND_SOURCE_SNAPSHOT_SELECTION"):
        raise UnifiedContentReviewError("Coordinate/sample composition cadence or no-interpolation boundary drift")
    if composition_ops.get("selection_uses_winning_frame_as_input") is not False or composition_ops.get("selection_uses_close_calls_as_timing") is not False:
        raise UnifiedContentReviewError("Coordinate/sample composition must not derive sample selection from winning_frame or close_calls")
    if composition_spatial.get("combined_scale") != [2.0 / 3.0, 2.0 / 3.0] or composition_spatial.get("combined_offset") != [0.0, 0.0]:
        raise UnifiedContentReviewError("Coordinate/sample composition spatial transform drift")
    if coordinate_sample_composition["selected_indexes"] != [row.get("source_game_snapshot_index") for row in samples]:
        raise UnifiedContentReviewError("Coordinate/sample composition selected indices differ from the sample-selection proposal")
    target_delivery = coord_projection.get("target_position", {}).get("delivery", [])
    expected_target_delivery = coordinate_sample_composition.get("projected_target_position", ())
    if len(target_delivery) != 2 or len(expected_target_delivery) != 2 or any(not isinstance(a, (int, float)) or not math.isclose(float(a), float(e), rel_tol=1e-5, abs_tol=1e-4) for a, e in zip(target_delivery, expected_target_delivery)):
        raise UnifiedContentReviewError("Coordinate/sample composition target position differs from the runtime coordinate projection")
    if composition_facts.get("projected_source_snapshot_count") != 420 or composition_facts.get("composed_delivery_snapshot_count") != 210 or composition_facts.get("winning_anchor_is_exact_selected_sample") is not True:
        raise UnifiedContentReviewError("Coordinate/sample composition expected review facts mismatch")
    if composition_contract.get("governance_locks", {}).get("policy_approved") is not False or composition_contract.get("governance_locks", {}).get("coordinate_projection_policy_approved") is not False or composition_contract.get("governance_locks", {}).get("sample_selection_policy_approved") is not False:
        raise UnifiedContentReviewError("Coordinate/sample composition policy approval locks must remain false")

    # Join Challenge source/delivery phase boundaries to a separately versioned
    # temporal-alignment proposal. This is a consistency check only: it neither
    # resamples snapshots nor infers editorial visibility or renderer readiness.
    try:
        temporal_alignment_preview = build_temporal_alignment_preview(root, verify_source_lineage=False)
        validate_temporal_alignment_preview(temporal_alignment_preview, root, verify_source_lineage=False)
    except ChallengeTemporalAlignmentError as exc:
        raise UnifiedContentReviewError(f"Challenge temporal-alignment proposal invalid: {exc}") from exc
    temporal_source = temporal_alignment_preview.get("source_timeline", {})
    temporal_delivery = temporal_alignment_preview.get("delivery_timeline", {})
    source_boundaries = [source_segments[0].get("start_frame")] + [segment.get("end_frame") for segment in source_segments]
    delivery_boundaries = [delivery_segments[0].get("start_frame")] + [segment.get("end_frame") for segment in delivery_segments]
    source_phase_counts = [segment.get("frame_count") for segment in source_segments]
    delivery_phase_counts = [segment.get("frame_count") for segment in delivery_segments]
    expected_phase_order = ["HOOK", "GAME", "REVEAL", "CTA"]
    temporal_phase_alignment = temporal_alignment_preview.get("phase_alignment", [])
    if temporal_source.get("boundaries") != source_boundaries or temporal_source.get("phase_frames") != source_phase_counts or temporal_source.get("fps") != source_timeline.get("fps") or temporal_source.get("total_frames") != source_timeline.get("total_frames"):
        raise UnifiedContentReviewError("Challenge temporal-alignment source timeline parity mismatch")
    if temporal_delivery.get("boundaries") != delivery_boundaries or temporal_delivery.get("phase_frames") != delivery_counts or temporal_delivery.get("fps") != delivery_fps or temporal_delivery.get("total_frames") != delivery_total_frames:
        raise UnifiedContentReviewError("Challenge temporal-alignment delivery timeline parity mismatch")
    if [phase.get("phase") for phase in temporal_phase_alignment] != expected_phase_order:
        raise UnifiedContentReviewError("Challenge temporal-alignment phase order mismatch")
    for index, phase in enumerate(temporal_phase_alignment):
        expected_source_range = [source_segments[index].get("start_frame"), source_segments[index].get("end_frame")]
        expected_delivery_range = [delivery_segments[index].get("start_frame"), delivery_segments[index].get("end_frame")]
        if phase.get("source_range") != expected_source_range or phase.get("delivery_range") != expected_delivery_range or phase.get("boundary_exact") is not True:
            raise UnifiedContentReviewError(f"Challenge temporal-alignment phase range mismatch: {phase.get('phase')}")
    temporal_windows = temporal_alignment_preview.get("editorial_windows", {})
    actual_field_ranges = {
        row.get("field_id"): None if row.get("visibility_range") is None else [row["visibility_range"].get("start_frame"), row["visibility_range"].get("end_frame")]
        for row in window_rows
    }
    if temporal_windows.get("state") != "PROPOSED_NOT_APPROVED" or temporal_windows.get("expected_field_ranges") != actual_field_ranges:
        raise UnifiedContentReviewError("Challenge temporal-alignment editorial window parity mismatch")
    temporal_sample = temporal_alignment_preview.get("sample_selection", {})
    if temporal_sample.get("state") != proposal.get("proposal_state") or (temporal_sample.get("source_game_snapshots"), temporal_sample.get("delivery_game_snapshots"), temporal_sample.get("stride"), temporal_sample.get("interpolation")) != (assessment.get("source_snapshot_count"), assessment.get("delivery_snapshot_count"), assessment.get("stride"), sample_policy.get("interpolation")):
        raise UnifiedContentReviewError("Challenge temporal-alignment sample-selection parity mismatch")
    temporal_anchor = temporal_alignment_preview.get("winning_anchor", {})
    if (temporal_anchor.get("source_absolute_frame_index"), temporal_anchor.get("source_game_local_index"), temporal_anchor.get("delivery_game_local_index"), temporal_anchor.get("delivery_absolute_frame_index")) != (anchor.get("winning_frame_absolute_source_index"), anchor.get("winning_frame_local_game_index"), anchor.get("winning_delivery_game_frame_index"), anchor.get("winning_absolute_delivery_frame_index")):
        raise UnifiedContentReviewError("Challenge temporal-alignment winning-anchor parity mismatch")
    temporal_alignment_contract_sha256 = sha256_bytes((root / "definitions/c11d/production/D_RENDERER_CHALLENGE_TEMPORAL_ALIGNMENT_POLICY_PROPOSAL_V1.json").read_bytes())
    if temporal_alignment_preview.get("policy_state") != "PROPOSED_NOT_APPROVED" or temporal_alignment_preview.get("summary_facts") != {"phase_boundaries_exact": True, "phase_count": 4, "duration_preserved": True, "delivery_candidate_materialized": False, "text_visibility_inferred_from_phase_names": False}:
        raise UnifiedContentReviewError("Challenge temporal-alignment proposal status/evidence mismatch")
    if temporal_alignment_preview.get("approval_state", {}).get("challenge_temporal_alignment_policy_approved") is not False or temporal_alignment_preview.get("execution_boundary", {}).get("renderer_native_input_emitted") is not False or temporal_alignment_preview.get("execution_boundary", {}).get("d4_8") != "BLOCKED" or temporal_alignment_preview.get("execution_boundary", {}).get("release_authority") != "NONE":
        raise UnifiedContentReviewError("Challenge temporal-alignment governance lock changed")

    # Unify timebase metadata across all three content types without making media.
    # Loop/Drill preserve their already-30-FPS timelines; Challenge references the
    # separate boundary and sample-selection proposals. Audio/music remains out of scope.
    try:
        unified_delivery_policy_preview = build_unified_delivery_policy_preview(root, verify_sources=False)
        validate_unified_delivery_policy_preview(unified_delivery_policy_preview, root, verify_sources=False)
    except UnifiedDeliveryPolicyError as exc:
        raise UnifiedContentReviewError(f"Unified delivery timebase proposal invalid: {exc}") from exc
    target_profile = unified_delivery_policy_preview.get("target_delivery_profile", {})
    delivery_profile_facts = identity.get("identity_facts", {})
    if (delivery_profile_facts.get("delivery_profile_id"), delivery_profile_facts.get("delivery_profile_fps"), delivery_profile_facts.get("delivery_width"), delivery_profile_facts.get("delivery_height")) != (target_profile.get("profile_id"), target_profile.get("fps"), target_profile.get("width"), target_profile.get("height")):
        raise UnifiedContentReviewError("Unified delivery target profile does not match profile-identity runtime evidence")
    matrix = {row["content_type"]: row for row in unified_delivery_policy_preview.get("content_matrix", [])}
    for row, content_type in ((loop, "visual_loops"), (drill, "visual_drills")):
        rule = matrix[content_type]
        if (row.get("fps"), row.get("frame_count"), row.get("duration_seconds")) != (rule["delivery_fps"], rule["delivery_frame_count"], rule["duration_seconds"]):
            raise UnifiedContentReviewError(f"Unified delivery timebase does not preserve {content_type} request-scoped payload timing")
        if rule["source_fps"] != rule["delivery_fps"] or rule["timebase_mode"] != "IDENTITY_NO_RESAMPLING":
            raise UnifiedContentReviewError(f"Unified delivery policy unexpectedly resamples {content_type}")
    if (source_timeline.get("fps"), source_timeline.get("total_frames"), delivery_fps, delivery_total_frames, delivery_counts) != (matrix["challenges"]["source_fps"], matrix["challenges"]["source_frame_count"], matrix["challenges"]["delivery_fps"], matrix["challenges"]["delivery_frame_count"], matrix["challenges"]["delivery_phase_frame_counts"]):
        raise UnifiedContentReviewError("Unified delivery timebase Challenge matrix differs from runtime/timeline evidence")
    if unified_delivery_policy_preview.get("policy_approved") is not False or unified_delivery_policy_preview.get("delivery_candidate_materialized") is not False or unified_delivery_policy_preview.get("renderer_native_input_emitted") is not False or unified_delivery_policy_preview.get("audio_music_policy") != "OUT_OF_SCOPE_NOT_DEFINED_NOT_EMITTED":
        raise UnifiedContentReviewError("Unified delivery policy crossed an approval, execution, or audio/music scope boundary")

    # Review the independent technical audio delivery envelope. This only checks
    # pinned output metadata and exact pre-encode timeline arithmetic; it never
    # chooses music, creates silence, or materializes audio samples.
    try:
        unified_audio_music_policy_preview = build_unified_audio_music_policy_preview(root, verify_sources=True)
        validate_unified_audio_music_policy_preview(unified_audio_music_policy_preview, root, verify_sources=True)
    except UnifiedAudioMusicDeliveryPolicyError as exc:
        raise UnifiedContentReviewError(f"Unified audio/music delivery proposal invalid: {exc}") from exc
    audio_profile = unified_audio_music_policy_preview.get("target_audio_profile", {})
    if audio_profile != EXPECTED_AUDIO_DELIVERY_PROFILE:
        raise UnifiedContentReviewError("Unified audio delivery fields drift from the pinned REVIEW_720 profile")
    audio_matrix = {row["content_type"]: row for row in unified_audio_music_policy_preview.get("content_matrix", [])}
    timebase_matrix = {row["content_type"]: row for row in unified_delivery_policy_preview.get("content_matrix", [])}
    for content_type in ("visual_loops", "visual_drills", "challenges"):
        audio_row = audio_matrix[content_type]
        video_row = timebase_matrix[content_type]
        if (audio_row["duration_seconds"], audio_row["delivery_fps"], audio_row["delivery_frame_count"]) != (video_row["duration_seconds"], video_row["delivery_fps"], video_row["delivery_frame_count"]):
            raise UnifiedContentReviewError(f"Audio pre-encode timeline does not match video delivery timeline: {content_type}")
        if audio_row["target_pcm_sample_count"] != int(audio_row["duration_seconds"] * audio_row["audio_sample_rate_hz"]):
            raise UnifiedContentReviewError(f"Audio pre-encode sample count is not an exact integer: {content_type}")
        if audio_row["source_audio_selected"] is not False or audio_row["music_asset_selected"] is not False or audio_row["audio_samples_emitted"] is not False or audio_row["audio_delivery_materialized"] is not False:
            raise UnifiedContentReviewError(f"Audio policy may not select or emit audio: {content_type}")
    if unified_audio_music_policy_preview.get("policy_approved") is not False or unified_audio_music_policy_preview.get("audio_samples_emitted") is not False or unified_audio_music_policy_preview.get("audio_payload_materialized") is not False or unified_audio_music_policy_preview.get("music_asset_selected") is not False:
        raise UnifiedContentReviewError("Audio/music delivery policy crossed an approval or materialization boundary")

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
        "coordinate_sample_composition": coordinate_sample_composition,
        "coordinate_sample_composition_contract_sha256": sha256_bytes((root / "definitions/c11d/production/D_RENDERER_CHALLENGE_COORDINATE_SAMPLE_COMPOSITION_PROPOSAL_V1.json").read_bytes()),
        "loop_drill_editorial_field_window_contract": editorial_contract,
        "loop_drill_editorial_field_window_contract_sha256": editorial_contract_sha256,
        "loop_drill_editorial_field_window_fixtures": editorial_fixtures,
        "temporal_alignment_preview": temporal_alignment_preview,
        "temporal_alignment_contract_sha256": temporal_alignment_contract_sha256,
        "unified_delivery_policy_preview": unified_delivery_policy_preview,
        "unified_audio_music_policy_preview": unified_audio_music_policy_preview,
        "challenge_visual_payload_sha256": challenge_visual["payload_sha256"],
        "d_render_model_sha256": render_model_sha,
    }


def _loop_drill_editorial_review(joined: Mapping[str, Any], content_type: str, frame_count: int) -> dict[str, Any]:
    contract = joined["loop_drill_editorial_field_window_contract"]
    policy = contract["mapping_policy"]
    # Raw editorial text is intentionally not echoed from this preview harness.
    # Report proposal rules separately from evaluated runtime visibility windows.
    return {
        "field_window_mapping": "PROPOSED_NOT_APPROVED_FULL_SPAN_NONEMPTY_VISUAL_FIELDS",
        "policy_id": policy["policy_id"],
        "policy_state": policy["state"],
        "proposal_contract_sha256": joined["loop_drill_editorial_field_window_contract_sha256"],
        "visible_field_rules": copy.deepcopy(policy["visible_fields"]),
        "metadata_only_fields": copy.deepcopy(policy["metadata_only_fields"]),
        "empty_value_rule": policy["empty_value_rule"],
        "interval_rule": policy["interval_rule"],
        "window_formula": policy["window_formula"],
        "payload_frame_count_authority": policy["payload_frame_count_authority"],
        "payload_frame_count": frame_count,
        "visibility_windows": None,
        "visibility_window_evaluation": "RAW_EDITORIAL_VALUES_NOT_EXPOSED_IN_RUNTIME_SUMMARY",
        "renderer_native_input_emitted": False,
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
            "editorial_review": _loop_drill_editorial_review(joined, "visual_loops", loop["frame_count"]),
            "materialization": "IN_MEMORY_ONLY_VISUAL_PAYLOAD_MATERIALIZED",
        },
        {
            "content_type": "visual_drills",
            "selection": drill.get("selection", {}),
            "identity": {"instance_id": drill["instance_id"], "seed": drill["seed"], "variation_index": drill["variation_index"], "payload_instance_sha256": drill["payload_instance_sha256"], "authoring_envelope_sha256": drill["authoring_envelope_sha256"]},
            "timing": {"fps": drill["fps"], "duration_seconds": drill["duration_seconds"], "frame_count": drill["frame_count"], "delivery_profile_id": "REVIEW_720"},
            "editorial_review": _loop_drill_editorial_review(joined, "visual_drills", drill["frame_count"]),
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
            "coordinate_sample_composition": {"state": joined["coordinate_sample_composition"]["contract"]["status"], "proposal_contract_sha256": joined["coordinate_sample_composition_contract_sha256"], "coordinate_projection_policy_id": joined["coordinate_projection"]["projection"]["policy_id"], "sample_selection_policy_id": joined["sample_selection_preview"]["proposal_id"], "operation_order": joined["coordinate_sample_composition"]["contract"]["composition"]["operation_order"], "projected_source_snapshot_count": joined["coordinate_sample_composition"]["contract"]["composition"]["spatial_projection_record_count"], "delivery_candidate_snapshot_count": joined["coordinate_sample_composition"]["contract"]["composition"]["composed_delivery_record_count"], "selection_stride": joined["coordinate_sample_composition"]["contract"]["composition"]["sampling_stride"], "interpolation": joined["coordinate_sample_composition"]["contract"]["composition"]["interpolation"], "equivalence_claim": "DECLARED_FOR_AFFINE_UNIFORM_TRANSFORM_ONLY", "projected_then_selected_indices_match_sampling_proposal": True, "delivery_candidate_materialized": False, "policy_approved": False, "renderer_native_input_emitted": False},
            "temporal_alignment": {
                "policy_id": joined["temporal_alignment_preview"]["policy_id"],
                "policy_state": joined["temporal_alignment_preview"]["policy_state"],
                "proposal_contract_sha256": joined["temporal_alignment_contract_sha256"],
                "preview_sha256": sha256_json(joined["temporal_alignment_preview"]),
                "source_fps": joined["temporal_alignment_preview"]["source_timeline"]["fps"],
                "source_total_frames": joined["temporal_alignment_preview"]["source_timeline"]["total_frames"],
                "source_boundaries": joined["temporal_alignment_preview"]["source_timeline"]["boundaries"],
                "source_phase_frame_counts": joined["temporal_alignment_preview"]["source_timeline"]["phase_frames"],
                "delivery_fps": joined["temporal_alignment_preview"]["delivery_timeline"]["fps"],
                "delivery_total_frames": joined["temporal_alignment_preview"]["delivery_timeline"]["total_frames"],
                "delivery_boundaries": joined["temporal_alignment_preview"]["delivery_timeline"]["boundaries"],
                "delivery_phase_frame_counts": joined["temporal_alignment_preview"]["delivery_timeline"]["phase_frames"],
                "phase_order": [phase["phase"] for phase in joined["temporal_alignment_preview"]["phase_alignment"]],
                "duration_seconds": joined["temporal_alignment_preview"]["delivery_timeline"]["duration_seconds"],
                "phase_boundaries_exact": joined["temporal_alignment_preview"]["summary_facts"]["phase_boundaries_exact"],
                "winning_anchor_source_absolute_frame_index": joined["temporal_alignment_preview"]["winning_anchor"]["source_absolute_frame_index"],
                "winning_anchor_delivery_absolute_frame_index": joined["temporal_alignment_preview"]["winning_anchor"]["delivery_absolute_frame_index"],
                "editorial_windows_policy_state": joined["temporal_alignment_preview"]["editorial_windows"]["state"],
                "sample_selection_policy_state": joined["temporal_alignment_preview"]["sample_selection"]["state"],
                "interpolation": joined["temporal_alignment_preview"]["sample_selection"]["interpolation"],
                "delivery_candidate_materialized": joined["temporal_alignment_preview"]["summary_facts"]["delivery_candidate_materialized"],
                "policy_approved": False,
                "renderer_native_input_emitted": joined["temporal_alignment_preview"]["execution_boundary"]["renderer_native_input_emitted"],
            },
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
        "unified_delivery_policy": {**copy.deepcopy(joined["unified_delivery_policy_preview"]), "preview_sha256": sha256_json(joined["unified_delivery_policy_preview"])},
        "unified_audio_music_policy": {**copy.deepcopy(joined["unified_audio_music_policy_preview"]), "preview_sha256": sha256_json(joined["unified_audio_music_policy_preview"])},
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
            "challenge_coordinate_sample_composition_proposal_parity": True,
            "loop_drill_editorial_field_window_proposal_parity": True,
            "challenge_temporal_alignment_policy_parity": True,
            "unified_delivery_policy_parity": True,
            "unified_audio_music_policy_parity": True,
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
    if report.get("cross_artifact_checks") != {key: True for key in ("c11c_manifest_identity", "challenge_source_identity", "payload_repeat_determinism", "profile_identity_parity", "delivery_timeline_parity", "field_window_parity", "simulation_invariance", "governance_boundary", "challenge_visual_payload_identity", "coordinate_projection_parity", "challenge_sample_selection_proposal_parity", "challenge_coordinate_sample_composition_proposal_parity", "loop_drill_editorial_field_window_proposal_parity", "challenge_temporal_alignment_policy_parity", "unified_delivery_policy_parity", "unified_audio_music_policy_parity")}:
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
    expected_editorial_review_keys = ("policy_id", "policy_state", "proposal_contract_sha256", "visible_field_rules", "metadata_only_fields", "empty_value_rule", "interval_rule", "window_formula", "payload_frame_count_authority", "payload_frame_count", "visibility_windows", "visibility_window_evaluation", "renderer_native_input_emitted")
    for content, expected_frames in ((loop, 600), (drill, 630)):
        editorial_review = content.get("editorial_review", {})
        if editorial_review.get("field_window_mapping") != "PROPOSED_NOT_APPROVED_FULL_SPAN_NONEMPTY_VISUAL_FIELDS":
            raise UnifiedContentReviewError("Visual Loop/Drill field-window mapping must remain proposal-only")
        if any(key not in editorial_review for key in expected_editorial_review_keys):
            raise UnifiedContentReviewError("Visual Loop/Drill editorial review is missing proposal metadata")
        if (editorial_review.get("policy_id"), editorial_review.get("policy_state"), editorial_review.get("proposal_contract_sha256")) != ("C11D_LOOP_DRILL_NONEMPTY_VISUAL_FIELDS_FULL_CONTINUOUS_SPAN_V1", "PROPOSED_NOT_APPROVED", "25fe4aaaaa94a80dbabcbf92533ff9c19a9d61cc0b3173cb0cd986a62701fd57"):
            raise UnifiedContentReviewError("Visual Loop/Drill editorial policy identity/state mismatch")
        if editorial_review.get("payload_frame_count") != expected_frames or editorial_review.get("visibility_windows") is not None or editorial_review.get("visibility_window_evaluation") != "RAW_EDITORIAL_VALUES_NOT_EXPOSED_IN_RUNTIME_SUMMARY":
            raise UnifiedContentReviewError("Visual Loop/Drill review must not fabricate evaluated windows without raw editorial values")
        if editorial_review.get("renderer_native_input_emitted") is not False:
            raise UnifiedContentReviewError("Visual Loop/Drill field-window proposal cannot emit renderer input")
        if editorial_review.get("visible_field_rules") != [
            {"field_id": "title", "target_region": "HEADER", "condition": "NONEMPTY_STRING", "window_rule": "FULL_CONTINUOUS_PAYLOAD_SPAN"},
            {"field_id": "subtitle", "target_region": "HEADER", "condition": "NONEMPTY_STRING", "window_rule": "FULL_CONTINUOUS_PAYLOAD_SPAN"},
            {"field_id": "call_to_action", "target_region": "FOOTER", "condition": "NONEMPTY_STRING", "window_rule": "FULL_CONTINUOUS_PAYLOAD_SPAN"},
        ] or editorial_review.get("metadata_only_fields") != [{"field_id": "language", "rule": "METADATA_ONLY_NO_VISIBILITY_WINDOW"}]:
            raise UnifiedContentReviewError("Visual Loop/Drill field mapping rules drifted")
        if editorial_review.get("empty_value_rule") != "SUPPRESS_FIELD_AND_ASSIGN_NO_WINDOW" or editorial_review.get("interval_rule") != "START_FRAME_INCLUSIVE_END_FRAME_EXCLUSIVE" or editorial_review.get("window_formula") != "NONEMPTY_VISUAL_FIELD_WINDOW_EQUALS_[0,GENERATED_PAYLOAD_FRAME_COUNT)" or editorial_review.get("payload_frame_count_authority") != "REQUEST_SCOPED_IN_MEMORY_MATERIALIZED_PAYLOAD_INSTANCE":
            raise UnifiedContentReviewError("Visual Loop/Drill editorial window semantics drifted")
    if report.get("approval_state", {}).get("loop_editorial_field_mapping_approved") is not False or report.get("approval_state", {}).get("drill_editorial_field_mapping_approved") is not False or report.get("approval_state", {}).get("loop_drill_editorial_field_window_policy_approved") is not False:
        raise UnifiedContentReviewError("Unified review cannot approve Loop/Drill editorial field-window policies")
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
    composition = challenge.get("coordinate_sample_composition", {})
    expected_composition = {
        "state": "PROPOSED_NOT_APPROVED_NOT_FROZEN",
        "proposal_contract_sha256": "72aa659dfc464ce8f2205cc483c18cdff96b82e55f3651102310f9f83ce897b4",
        "coordinate_projection_policy_id": "C11D_CHALLENGE_COORDINATE_PROJECTION_1080_TO_540_TO_REVIEW720_V1",
        "sample_selection_policy_id": "C11D_CHALLENGE_SAMPLE_EVERY_SECOND_SOURCE_SNAPSHOT_NO_INTERPOLATION_V1",
        "operation_order": ["PROJECT_ALL_GAME_COORDINATES_IN_ORIGINAL_ORDER", "SELECT_EVEN_ZERO_BASED_GAME_LOCAL_INDICES"],
        "projected_source_snapshot_count": 420, "delivery_candidate_snapshot_count": 210, "selection_stride": 2,
        "interpolation": "NONE", "equivalence_claim": "DECLARED_FOR_AFFINE_UNIFORM_TRANSFORM_ONLY",
        "projected_then_selected_indices_match_sampling_proposal": True, "delivery_candidate_materialized": False,
        "policy_approved": False, "renderer_native_input_emitted": False,
    }
    if composition != expected_composition:
        raise UnifiedContentReviewError("Challenge coordinate/sample composition summary mismatch or approval drift")
    if report.get("approval_state", {}).get("simulation_sample_selection_policy_approved") is not False or report.get("approval_state", {}).get("interpolation_policy_approved") is not False or report.get("approval_state", {}).get("coordinate_sample_composition_policy_approved") is not False:
        raise UnifiedContentReviewError("Unified review cannot approve simulation sample selection, interpolation or coordinate/sample composition")
    temporal = challenge.get("temporal_alignment", {})
    expected_temporal = {
        "policy_id": "C11D_CHALLENGE_TEMPORAL_ALIGNMENT_60_TO_30_HALF_OPEN_BOUNDARIES_V1",
        "policy_state": "PROPOSED_NOT_APPROVED",
        "proposal_contract_sha256": "bf8084f4d6e1257ac3aa594cd5a5625a6814d9022643774f152392558a224dd4",
        "source_fps": 60, "source_total_frames": 900, "source_boundaries": [0, 180, 600, 780, 900],
        "source_phase_frame_counts": [180, 420, 180, 120],
        "delivery_fps": 30, "delivery_total_frames": 450, "delivery_boundaries": [0, 90, 300, 390, 450],
        "delivery_phase_frame_counts": [90, 210, 90, 60], "phase_order": ["HOOK", "GAME", "REVEAL", "CTA"],
        "duration_seconds": 15, "phase_boundaries_exact": True,
        "winning_anchor_source_absolute_frame_index": 574,
        "winning_anchor_delivery_absolute_frame_index": 287,
        "editorial_windows_policy_state": "PROPOSED_NOT_APPROVED",
        "sample_selection_policy_state": "PROPOSED_NOT_APPROVED",
        "interpolation": "NONE", "delivery_candidate_materialized": False,
        "policy_approved": False, "renderer_native_input_emitted": False,
    }
    if temporal != {**expected_temporal, "preview_sha256": temporal.get("preview_sha256")} or not _is_sha256(temporal.get("preview_sha256")):
        raise UnifiedContentReviewError("Challenge temporal-alignment summary mismatch or approval drift")
    if report.get("approval_state", {}).get("challenge_temporal_alignment_policy_approved") is not False:
        raise UnifiedContentReviewError("Unified review cannot approve Challenge temporal alignment")
    delivery_policy = report.get("unified_delivery_policy", {})
    delivery_policy_unsigned = {k: copy.deepcopy(v) for k, v in delivery_policy.items() if k != "preview_sha256"}
    if delivery_policy.get("schema") != "C11-D-D9-UNIFIED-DELIVERY-TIMEBASE-POLICY-PREVIEW-V1" or delivery_policy.get("policy_id") != UNIFIED_DELIVERY_POLICY_ID or delivery_policy.get("policy_state") != "PROPOSED_NOT_APPROVED":
        raise UnifiedContentReviewError("Unified delivery policy identity/state mismatch")
    if delivery_policy.get("proposal_contract_sha256") != "1e190d5bc1541d04f93052ccc27afd8a3ed289d9c2271d364ebbae6548412921":
        raise UnifiedContentReviewError("Unified delivery policy contract identity pin mismatch")
    if delivery_policy.get("target_delivery_profile") != EXPECTED_UNIFIED_DELIVERY_PROFILE or delivery_policy.get("content_matrix") != EXPECTED_UNIFIED_DELIVERY_MATRIX:
        raise UnifiedContentReviewError("Unified delivery policy target-profile or cross-content matrix mismatch")
    if delivery_policy.get("shared_invariants") != ["DELIVERY_PROFILE_IS_EXPLICIT_AND_RESOLVED_ONCE", "PRESERVE_ELAPSED_DURATION", "PRESERVE_PHASE_ORDER_AND_HALF_OPEN_BOUNDARY_CONTINUITY", "DO_NOT_MUTATE_SOURCE_SIMULATION_OR_CANONICAL_CONTENT", "NO_INTERPOLATED_SIMULATION_STATE", "WINNING_FRAME_IS_READ_ONLY_AND_NOT_A_SAMPLE_SELECTION_INPUT", "CLOSE_CALLS_IS_COUNT_ONLY_AND_NOT_TIMING"]:
        raise UnifiedContentReviewError("Unified delivery policy shared invariants drift")
    if delivery_policy.get("audio_music_policy") != "OUT_OF_SCOPE_NOT_DEFINED_NOT_EMITTED" or delivery_policy.get("delivery_candidate_materialized") is not False or delivery_policy.get("policy_approved") is not False or delivery_policy.get("renderer_native_input_emitted") is not False or delivery_policy.get("media_created") is not False:
        raise UnifiedContentReviewError("Unified delivery policy approval, audio/music or execution boundary drift")
    if delivery_policy.get("approval_state", {}).get("unified_delivery_timebase_policy_approved") is not False or delivery_policy.get("execution_boundary", {}).get("d4_8") != "BLOCKED" or delivery_policy.get("execution_boundary", {}).get("release_authority") != "NONE":
        raise UnifiedContentReviewError("Unified delivery policy cannot approve itself, D4.8 or release authority")
    if not _is_sha256(delivery_policy.get("preview_sha256")) or sha256_json(delivery_policy_unsigned) != delivery_policy.get("preview_sha256"):
        raise UnifiedContentReviewError("Unified delivery policy preview digest mismatch")
    if report.get("approval_state", {}).get("unified_delivery_timebase_policy_approved") is not False:
        raise UnifiedContentReviewError("Unified review cannot approve the unified delivery policy")
    audio_policy = report.get("unified_audio_music_policy", {})
    audio_unsigned = {k: copy.deepcopy(v) for k, v in audio_policy.items() if k != "preview_sha256"}
    if audio_policy.get("schema") != "C11-D-D9-UNIFIED-AUDIO-MUSIC-DELIVERY-POLICY-PREVIEW-V1" or audio_policy.get("policy_id") != UNIFIED_AUDIO_MUSIC_POLICY_ID or audio_policy.get("policy_state") != "PROPOSED_NOT_APPROVED":
        raise UnifiedContentReviewError("Unified audio/music delivery policy identity/state mismatch")
    if audio_policy.get("proposal_contract_sha256") != "12d9000b73f09318a005e8f1d76e2efb2777469715dfeb7d686760600ba11238":
        raise UnifiedContentReviewError("Unified audio/music delivery proposal contract identity pin mismatch")
    if audio_policy.get("target_audio_profile") != EXPECTED_AUDIO_DELIVERY_PROFILE or audio_policy.get("content_matrix") != EXPECTED_AUDIO_DELIVERY_MATRIX:
        raise UnifiedContentReviewError("Unified audio/music target profile or pre-encode timeline matrix mismatch")
    if audio_policy.get("shared_invariants") != ["USE_EXPLICIT_REVIEW_720_AUDIO_FIELDS_FROM_PINNED_DELIVERY_REGISTRY", "PRE_ENCODE_PCM_TIMELINE_DURATION_EQUALS_VIDEO_DELIVERY_DURATION", "PCM_SAMPLE_COUNT_EQUALS_DURATION_SECONDS_TIMES_48000_EXACTLY", "DO_NOT_SELECT_OR_SYNTHESIZE_MUSIC_OR_SOUND_EFFECTS", "DO_NOT_INFER_SILENCE_AS_DEFAULT_WHEN_AUDIO_ASSET_IS_ABSENT", "DO_NOT_MIX_DUCK_FADE_LOOP_OR_CROSSFADE_AUDIO", "DO_NOT_APPLY_GAIN_OR_LOUDNESS_NORMALIZATION", "CODEC_PRIMING_AND_POST_ENCODE_DURATION_TOLERANCE_REMAIN_UNDEFINED", "NO_AUDIO_PAYLOAD_OR_MEDIA_IS_EMITTED_BY_THIS_REVIEW"]:
        raise UnifiedContentReviewError("Unified audio/music delivery policy invariants drift")
    if audio_policy.get("audio_payload_materialized") is not False or audio_policy.get("audio_samples_emitted") is not False or audio_policy.get("music_asset_selected") is not False or audio_policy.get("policy_approved") is not False:
        raise UnifiedContentReviewError("Unified audio/music delivery review cannot select, emit or approve audio")
    if audio_policy.get("approval_state", {}).get("audio_delivery_profile_policy_approved") is not False or audio_policy.get("approval_state", {}).get("music_selection_policy_approved") is not False or audio_policy.get("approval_state", {}).get("mixing_policy_approved") is not False or audio_policy.get("approval_state", {}).get("loudness_policy_approved") is not False or audio_policy.get("approval_state", {}).get("audio_timeline_policy_approved") is not False:
        raise UnifiedContentReviewError("Unified audio/music delivery policy approvals must remain false")
    audio_exec = audio_policy.get("execution_boundary", {})
    if audio_exec.get("audio_samples_emitted") is not False or audio_exec.get("audio_payload_materialized") is not False or audio_exec.get("music_asset_selected") is not False or audio_exec.get("renderer_native_input_emitted") is not False or audio_exec.get("renderer_activation") is not False or audio_exec.get("media_created") is not False or audio_exec.get("d4_8") != "BLOCKED" or audio_exec.get("release_authority") != "NONE":
        raise UnifiedContentReviewError("Unified audio/music delivery execution/governance boundary drift")
    if not _is_sha256(audio_policy.get("preview_sha256")) or sha256_json(audio_unsigned) != audio_policy.get("preview_sha256"):
        raise UnifiedContentReviewError("Unified audio/music delivery preview digest mismatch")
    for content_type, expected_duration, expected_frames in (("visual_loops", 20.0, 600), ("visual_drills", 21.0, 630), ("challenges", 15.0, 450)):
        row = next((x for x in EXPECTED_AUDIO_DELIVERY_MATRIX if x["content_type"] == content_type), None)
        item_row = loop if content_type == "visual_loops" else drill if content_type == "visual_drills" else challenge
        if row is None or row["duration_seconds"] != expected_duration or row["target_pcm_sample_count"] != int(expected_duration * 48000):
            raise UnifiedContentReviewError(f"Audio duration/sample-count invariant failed: {content_type}")
        actual_duration = item_row.get("timing", {}).get("duration_seconds")
        if actual_duration != expected_duration:
            raise UnifiedContentReviewError(f"Audio duration does not match unified video timing: {content_type}")
    if report.get("approval_state", {}).get("audio_delivery_profile_policy_approved") is not False or report.get("approval_state", {}).get("music_selection_policy_approved") is not False or report.get("approval_state", {}).get("mixing_policy_approved") is not False or report.get("approval_state", {}).get("loudness_policy_approved") is not False or report.get("approval_state", {}).get("audio_timeline_policy_approved") is not False:
        raise UnifiedContentReviewError("Unified review cannot approve audio delivery, music selection, mixing, loudness or timeline policy")
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
