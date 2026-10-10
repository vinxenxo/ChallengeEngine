from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

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
]
EXPECTED_UNRESOLVED_GATES = [
    "VISUAL_LOOP_EDITORIAL_FIELD_MAPPING_UNDECLARED",
    "VISUAL_DRILL_EDITORIAL_FIELD_MAPPING_UNDECLARED",
    "CHALLENGE_VISUAL_PAYLOAD_NOT_MATERIALIZED",
    "CHALLENGE_SIMULATION_SAMPLE_SELECTION_AND_INTERPOLATION_UNRESOLVED",
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


def validate_harness_summaries(summaries: Mapping[str, dict[str, Any]]) -> dict[str, Any]:
    expected_names = [item["name"] for item in EXPECTED_HARNESSES]
    if list(summaries.keys()) != expected_names:
        raise UnifiedContentReviewError("All five runtime summaries must be provided in canonical order")
    visual = summaries["visual_payloads"]
    challenge = summaries["challenge_runtime"]
    identity = summaries["profile_identity"]
    timeline = summaries["delivery_timeline"]
    windows = summaries["editorial_windows"]

    frozen = FROZEN_MANIFEST_SHA256
    if any(x.get("frozen_c11c_manifest_sha256") != frozen for x in (visual, challenge, identity, timeline, windows)):
        raise UnifiedContentReviewError("The five harnesses do not agree on the frozen C11-C manifest")
    if any(x.get("challenge_source_sha256") != CHALLENGE_SHA256 for x in (challenge, identity, timeline, windows)):
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
        raise UnifiedContentReviewError("Visual payload harness must continue to leave Challenge payload unmaterialized")
    if challenge.get("challenge_runtime_output_materialized") is not True or challenge.get("challenge_visual_payload_materialized") is not False or challenge.get("deterministic_repeat_pass") is not True:
        raise UnifiedContentReviewError("Challenge runtime result must be deterministic, but its visual payload must remain unmaterialized")
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

    return {
        "loop": loop,
        "drill": drill,
        "challenge": challenge_instance,
        "identity": identity,
        "timeline": timeline,
        "windows": windows,
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
            "identity": {"seed_requested": challenge["seed_requested"], "seed_used": challenge["seed_used"], "runtime_output_sha256": challenge["runtime_output_sha256"], "simulation_frame_signature_sha256": challenge["frame_signature_sha256"], "d_presentation_render_model_sha256": joined["d_render_model_sha256"], "legacy_runtime_profile_id": "test_master_11s", "d_presentation_profile_id": "social_default_v1"},
            "timing": {"source_fps": 60, "source_total_frames": 900, "game_frame_count": 420, "delivery_profile_id": "REVIEW_720", "delivery_fps": 30, "delivery_total_frames": 450, "delivery_segments": timeline["delivery_segments"], "field_windows_proposal_sha256": windows["proposal_sha256"]},
            "editorial_review": {"field_window_mapping": "CHALLENGE_PROPOSAL_2_VISIBLE_FIELDS_1_EMPTY_SUPPRESSED", "fields": windows["fields"], "policy_state": "PROPOSED_NOT_APPROVED"},
            "materialization": "IN_MEMORY_ONLY_RUNTIME_RESULT_VISUAL_PAYLOAD_NOT_MATERIALIZED",
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
    if report.get("cross_artifact_checks") != {key: True for key in ("c11c_manifest_identity", "challenge_source_identity", "payload_repeat_determinism", "profile_identity_parity", "delivery_timeline_parity", "field_window_parity", "simulation_invariance", "governance_boundary")}:
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
    if challenge.get("materialization") != "IN_MEMORY_ONLY_RUNTIME_RESULT_VISUAL_PAYLOAD_NOT_MATERIALIZED" or challenge.get("editorial_review", {}).get("policy_state") != "PROPOSED_NOT_APPROVED":
        raise UnifiedContentReviewError("Challenge review must not claim a visual payload or approved editorial policy")
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
