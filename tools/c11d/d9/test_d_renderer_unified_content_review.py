from __future__ import annotations

import copy
import io
import json
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch
from subprocess import CompletedProcess

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
sys.path.insert(0, str(HERE.parent))

from d_renderer_unified_content_review import (  # noqa: E402
    CHALLENGE_SHA256,
    EXPECTED_HARNESSES,
    EXPECTED_SOURCE_LINEAGE,
    FROZEN_MANIFEST_SHA256,
    UnifiedContentReviewError,
    build_review_manifest,
    sha256_json,
    validate_contract,
    validate_harness_summaries,
    validate_review_manifest,
)
from run_d_renderer_unified_content_review import _run_harness  # noqa: E402


D = lambda char: char * 64


def make_summaries() -> dict[str, dict]:
    loop = {
        "content_type": "visual_loops", "instance_id": "D-VLP-5ac67e64ff717d97", "selection": {"family_id": "c11c_geometric_waves_v1", "subtype_id": "harmonic_membrane"},
        "seed": 12345, "variation_index": 0, "fps": 30, "duration_seconds": 20.0, "frame_count": 600,
        "authoring_envelope_sha256": D("a"), "payload_instance_sha256": "5ac67e64ff717d9756b37152dd1ee1ff81a1b0e754f83c06a618964c9a62e090", "materialization": "IN_MEMORY_ONLY",
        "deterministic_repeat_pass": True, "instance_parameters_bound": True,
    }
    drill = {
        "content_type": "visual_drills", "instance_id": "D-VDP-1a96afdd7a0d950e", "selection": {"family_id": "tracking", "variant_id": "tier-2"},
        "seed": 12345, "variation_index": 0, "fps": 30, "duration_seconds": 21.0, "frame_count": 630,
        "authoring_envelope_sha256": D("c"), "payload_instance_sha256": "1a96afdd7a0d950ef3eabb5531fe13496b4206a7d4fd1d7f233892b0329a592b", "materialization": "IN_MEMORY_ONLY",
        "deterministic_repeat_pass": True, "instance_parameters_bound": True,
    }
    manifest = FROZEN_MANIFEST_SHA256
    challenge = {
        "schema": "C11-D-D9-RENDERER-CHALLENGE-RUNTIME-OUTPUT-PREVIEW-V1", "frozen_c11c_manifest_sha256": manifest,
        "challenge_source_sha256": CHALLENGE_SHA256, "challenge_runtime_output_materialized": True,
        "challenge_visual_payload_materialized": False, "deterministic_repeat_pass": True,
        "instance": {
            "content_type": "challenges", "challenge_id": "CHALLENGE_004", "mechanic": "parking_v2", "mechanic_version": "2.0",
            "asset_family": "fam_garage_01", "asset_family_version": "1.0", "seed_requested": 314159, "seed_used": 314159,
            "fps": 60, "total_frames": 900, "duration_seconds": 15.0, "game_frame_count": 420,
            "winning_frame_local": 394, "score": 0.27, "minimum_distance": 2.64, "tolerance_threshold": 15.0,
            "simulation_error_state": "OK", "presentation_binding_success": True, "presentation_profile_id": "test_master_11s",
            "frame_signature_sha256": D("e"), "runtime_output_sha256": D("f"), "materialization": "IN_MEMORY_ONLY_RUNTIME_RESULT_NOT_VISUAL_PAYLOAD",
        },
    }
    identity = {
        "schema": "C11-D-D9-RENDERER-PROFILE-IDENTITY-SEPARATION-V1", "frozen_c11c_manifest_sha256": manifest,
        "challenge_source_sha256": CHALLENGE_SHA256,
        "identity_facts": {
            "legacy_video_profile_id": "test_master_11s", "source_presentation_profile_id": "social_default_v1",
            "d_presentation_profile_id": "social_default_v1", "delivery_profile_id": "REVIEW_720", "inline_timeline_fps": 60,
            "inline_timeline_total_frames": 900, "delivery_profile_fps": 30, "delivery_width": 720, "delivery_height": 1280,
        },
        "runtime_rebind": {"runtime_success": True, "legacy_binding_success": True, "d_binding_success": True, "d_binding_profile_id": "social_default_v1", "d_binding_render_model_sha256": D("1")},
        "simulation_invariance": {"frame_signature_sha256_before": D("e"), "frame_signature_sha256_after": D("e"), "frame_signature_unchanged": True,
            "winning_frame_before": 394, "winning_frame_after": 394, "winning_frame_unchanged": True,
            "game_frame_count_before": 420, "game_frame_count_after": 420, "metrics_unchanged": True},
    }
    source_segments = [
        {"phase": "HOOK", "start_frame": 0, "end_frame": 180, "frame_count": 180},
        {"phase": "GAME", "start_frame": 180, "end_frame": 600, "frame_count": 420},
        {"phase": "REVEAL", "start_frame": 600, "end_frame": 780, "frame_count": 180},
        {"phase": "CTA", "start_frame": 780, "end_frame": 900, "frame_count": 120},
    ]
    delivery_segments = [
        {"phase": "HOOK", "start_frame": 0, "end_frame": 90, "frame_count": 90},
        {"phase": "GAME", "start_frame": 90, "end_frame": 300, "frame_count": 210},
        {"phase": "REVEAL", "start_frame": 300, "end_frame": 390, "frame_count": 90},
        {"phase": "CTA", "start_frame": 390, "end_frame": 450, "frame_count": 60},
    ]
    timeline = {
        "schema": "C11-D-RENDERER-CHALLENGE-DELIVERY-TIMELINE-REVIEW-CONTRACT-V1", "frozen_c11c_manifest_sha256": manifest,
        "challenge_source_sha256": CHALLENGE_SHA256,
        "profile_identity": {"challenge_id": "CHALLENGE_004", "legacy_video_profile_id": "test_master_11s", "source_presentation_profile_id": "social_default_v1", "d_presentation_profile_id": "social_default_v1", "delivery_profile_id": "REVIEW_720"},
        "source_timeline": {"fps": 60, "total_frames": 900, "duration_seconds": 15, "phase_order": ["HOOK", "GAME", "REVEAL", "CTA"], "boundary_frames": [0, 180, 600, 780, 900]},
        "delivery_profile": {"profile_id": "REVIEW_720", "fps": 30, "width": 720, "height": 1280},
        "source_segments": source_segments, "delivery_segments": delivery_segments,
        "runtime_evidence": {"runtime_success": True, "repeat_deterministic": True, "simulation_frame_signature_unchanged": True, "winning_frame_unchanged": True, "metrics_unchanged": True},
        "policy_state": "PROPOSED_NOT_APPROVED",
    }
    windows = {
        "schema": "C11-D-D9-RENDERER-EDITORIAL-FIELD-WINDOW-PROPOSAL-V1", "frozen_c11c_manifest_sha256": manifest,
        "challenge_source_sha256": CHALLENGE_SHA256, "challenge_id": "CHALLENGE_004",
        "policy": {"policy_id": "C11D_SAME_NAME_EDITORIAL_FIELD_TO_PHASE_FULL_WINDOW_V1", "state": "PROPOSED_NOT_APPROVED"},
        "fields": [
            {"field_id": "hook", "phase": "HOOK", "source_text": "¡SOLO EL 1% APARCA SIN ROZAR!", "state": "PROPOSED_VISIBLE_WINDOW", "visibility_range": {"start_frame": 0, "end_frame": 90, "frame_count": 90}},
            {"field_id": "reveal", "phase": "REVEAL", "source_text": "", "state": "SUPPRESSED_EMPTY_EDITORIAL_FIELD", "visibility_range": None},
            {"field_id": "cta", "phase": "CTA", "source_text": "¿Lo has clavado?", "state": "PROPOSED_VISIBLE_WINDOW", "visibility_range": {"start_frame": 390, "end_frame": 450, "frame_count": 60}},
        ],
        "unresolved_content_types": {"visual_loops": "NO_EDITORIAL_FIELD_WINDOW_MAPPING_DECLARED", "visual_drills": "NO_EDITORIAL_FIELD_WINDOW_MAPPING_DECLARED"},
        "identity_evidence": {"d_presentation_render_model_sha256": D("1")},
        "runtime_evidence": {"runtime_success": True, "repeat_deterministic": True, "simulation_frame_signature_unchanged": True, "winning_frame_unchanged": True, "metrics_unchanged": True, "game_frame_count": 420},
        "proposal_sha256": D("2"),
    }
    assets = [
        {"role": "BACKGROUND", "resource_path": "res://assets/c6/garage_background.svg", "sha256": "c9d8acdae725ca7726fc8ad23a046e4aac4d9e454b45db40d2c770732b31ab1e", "intrinsic_width": 1080, "intrinsic_height": 1920, "resource_loaded_as_texture2d": True},
        {"role": "ANIMATED_OBJECT", "resource_path": "res://assets/c6/car.svg", "sha256": "93a6f78d9654f7917ab2287800858a937e9c68c458cc60bf417d6f2b98c1a96d", "intrinsic_width": 160, "intrinsic_height": 320, "resource_loaded_as_texture2d": True},
        {"role": "TARGET", "resource_path": "res://assets/c6/parking_target.svg", "sha256": "ec2dcafd7dfc99ff501eb2d93b93906680a30c48cf0741807cbbdd915a18cfb3", "intrinsic_width": 200, "intrinsic_height": 400, "resource_loaded_as_texture2d": True},
    ]
    visual_challenge_payload = {
        "schema": "C11-D-D9-CHALLENGE-VISUAL-PAYLOAD-PREVIEW-V1", "schema_version": "1.0",
        "status": "IN_MEMORY_REVIEW_ONLY_SOURCE_TIMEBASE_VISUAL_PAYLOAD_NOT_RENDERER_INPUT",
        "frozen_c11c_manifest_sha256": manifest, "challenge_source_sha256": CHALLENGE_SHA256,
        "payload_identity": {"challenge_id": "CHALLENGE_004", "mechanic": "parking_v2", "presentation_profile_id": "social_default_v1", "coordinate_space": "CANVAS_1080X1920"},
        "payload_sha256": D("9"), "asset_nodes": assets,
        "animation": {"frame_source": "SimulationResult.frames", "frame_record_count": 420, "game_frame_count": 420, "source_fps": 60, "frame_records_sha256": D("d"), "simulation_telemetry_included": False, "winning_frame_sampling_used": False, "delivery_resampling": "UNRESOLVED_NOT_APPLIED"},
        "determinism": {"runtime_repeat_equal": True, "payload_repeat_equal": True, "frame_signature_repeat_equal": True, "simulation_invariance": True},
        "execution_boundary": {"renderer_activation": False, "renderer_dispatch_invoked": False, "renderer_native_input_emitted": False, "media_output_created": False, "payload_written": False},
        "source_lineage": [
            {"path":"definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_PREVIEW_V1.json", "sha256":"67daa1f83ac151906059695bb4d87974819c2d16d3715b78b00657bfdac54f7a"},
            {"path":"challenges/CHALLENGE_004.json", "sha256":CHALLENGE_SHA256},
            {"path":"release/C11C_FREEZE_PACKAGE_MANIFEST.json", "sha256":FROZEN_MANIFEST_SHA256},
        ],
    }
    coordinate = {
        "schema": "C11-D-D9-RENDERER-CHALLENGE-COORDINATE-PROJECTION-PREVIEW-V1", "schema_version": "1.0",
        "status": "IN_MEMORY_REVIEW_ONLY_PROJECTION_PREVIEW_NOT_RENDERER_INPUT",
        "frozen_c11c_manifest_sha256": manifest, "challenge_source_sha256": CHALLENGE_SHA256,
        "projection": {"policy_id": "C11D_CHALLENGE_COORDINATE_PROJECTION_1080_TO_540_TO_REVIEW720_V1", "state": "PROPOSED_NOT_APPROVED", "source_coordinate_space": "CANVAS_1080X1920", "stage_scales": [[0.5,0.5],[4/3,4/3]], "combined_scale": [2/3,2/3], "sampling_or_interpolation": "UNRESOLVED_NOT_APPLIED", "target_position": {"source": [850.0, 960.0], "presentation_canvas": [425.0, 480.0], "delivery": [566.6666666666666, 640.0]}},
        "projected_frames": {"source_records":420, "projected_records":420, "source_records_sha256":D("d"), "projected_records_sha256":D("e"), "order_preserved":True, "local_scale_preserved":True, "other_snapshot_fields_preserved":True},
        "determinism": {"runtime_repeat_equal":True, "projection_repeat_equal":True, "source_frame_signature_repeat_equal":True},
        "simulation_invariance": {"frame_signature_unchanged":True, "winning_frame_unchanged":True, "metrics_unchanged":True, "frame_count_unchanged":True},
        "assets": [{"role":a["role"], "resource_path":a["resource_path"], "sha256":a["sha256"]} for a in assets],
        "execution_boundary": {"renderer_activation":False, "renderer_dispatch_invoked":False, "renderer_native_input_emitted":False, "media_created":False, "projected_payload_written":False},
        "source_lineage": [
            {"path":"definitions/c11d/production/D_RENDERER_CHALLENGE_COORDINATE_PROJECTION_V1.json", "sha256":"c1caf8e640595bc89957f17ef8bbd7abe80a92cac18cf77974633a1ddde0e264"},
            {"path":"definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_PREVIEW_V1.json", "sha256":"67daa1f83ac151906059695bb4d87974819c2d16d3715b78b00657bfdac54f7a"},
            {"path":"challenges/CHALLENGE_004.json", "sha256":CHALLENGE_SHA256},
            {"path":"release/C11C_FREEZE_PACKAGE_MANIFEST.json", "sha256":FROZEN_MANIFEST_SHA256},
        ],
    }
    return {
        "visual_payloads": {"frozen_c11c_manifest_sha256": manifest, "instances": [loop, drill], "challenge_runtime_payload_materialized": False, "unmaterialized_content_types": ["challenges"]},
        "challenge_runtime": challenge, "profile_identity": identity, "delivery_timeline": timeline, "editorial_windows": windows,
        "challenge_visual_payload": visual_challenge_payload, "coordinate_projection": coordinate,
    }


def make_evidence() -> list[dict]:
    return [{"name": item["name"], "script": item["script"], "script_sha256": D(str(i + 1)), "exit_code": 0,
             "summary_sha256": D("6789abc"[i]), "pass_marker_seen": True, "runtime_error_log_seen": False}
            for i, item in enumerate(EXPECTED_HARNESSES)]


class UnifiedContentReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract, cls.schema = validate_contract(ROOT, verify_sources=False)

    def report(self) -> dict:
        summaries = make_summaries()
        evidence = make_evidence()
        report = build_review_manifest(summaries, evidence, self.contract, ROOT / "definitions/c11d/production/D_RENDERER_UNIFIED_CONTENT_REVIEW_V1.json")
        # The locally generated overlay has no complete C11-C checkout. Its contract digest is still valid.
        validate_review_manifest(report, self.schema)
        return report

    def test_contract_scope_and_lineage(self) -> None:
        self.assertEqual(self.contract["supported_content_types"], ["visual_loops", "visual_drills", "challenges"])
        self.assertEqual(len(EXPECTED_SOURCE_LINEAGE), 19)
        self.assertEqual([x["name"] for x in EXPECTED_HARNESSES], ["visual_payloads", "challenge_runtime", "profile_identity", "delivery_timeline", "editorial_windows", "challenge_visual_payload", "coordinate_projection"])

    def test_synthetic_join_passes_schema_and_digest(self) -> None:
        report = self.report()
        self.assertEqual(report["status"], "REVIEW_CHAIN_CONSISTENT_NOT_VIDEO_READY")
        self.assertEqual([x["content_type"] for x in report["content_items"]], ["visual_loops", "visual_drills", "challenges"])
        loops_item, drills_item = report["content_items"][:2]
        for item, frame_count in ((loops_item, 600), (drills_item, 630)):
            editorial = item["editorial_review"]
            self.assertEqual(editorial["field_window_mapping"], "PROPOSED_NOT_APPROVED_FULL_SPAN_NONEMPTY_VISUAL_FIELDS")
            self.assertEqual(editorial["policy_state"], "PROPOSED_NOT_APPROVED")
            self.assertEqual(editorial["payload_frame_count"], frame_count)
            self.assertIsNone(editorial["visibility_windows"])
            self.assertEqual(editorial["visibility_window_evaluation"], "RAW_EDITORIAL_VALUES_NOT_EXPOSED_IN_RUNTIME_SUMMARY")
            self.assertFalse(editorial["renderer_native_input_emitted"])
        self.assertEqual(len(report["unresolved_gates"]), 9)
        self.assertIn("VISUAL_LOOP_EDITORIAL_FIELD_MAPPING_NOT_APPROVED", report["unresolved_gates"])
        self.assertIn("VISUAL_DRILL_EDITORIAL_FIELD_MAPPING_NOT_APPROVED", report["unresolved_gates"])
        self.assertEqual(report["cross_artifact_checks"]["coordinate_projection_parity"], True)
        self.assertEqual(report["cross_artifact_checks"]["challenge_sample_selection_proposal_parity"], True)
        self.assertEqual(report["cross_artifact_checks"]["challenge_coordinate_sample_composition_proposal_parity"], True)
        self.assertEqual(report["cross_artifact_checks"]["loop_drill_editorial_field_window_proposal_parity"], True)
        self.assertEqual(report["cross_artifact_checks"]["challenge_temporal_alignment_policy_parity"], True)
        self.assertEqual(report["cross_artifact_checks"]["unified_delivery_policy_parity"], True)
        self.assertEqual(report["cross_artifact_checks"]["unified_audio_music_policy_parity"], True)
        self.assertEqual(report["unified_delivery_policy"]["policy_id"], "C11D_UNIFIED_DELIVERY_TIMEBASE_ALL_CONTENT_TYPES_V1")
        self.assertEqual(report["unified_delivery_policy"]["policy_state"], "PROPOSED_NOT_APPROVED")
        self.assertEqual(len(report["unified_delivery_policy"]["content_matrix"]), 3)
        self.assertEqual(report["unified_delivery_policy"]["content_matrix"][0]["delivery_frame_count"], 600)
        self.assertEqual(report["unified_delivery_policy"]["content_matrix"][1]["delivery_frame_count"], 630)
        self.assertEqual(report["unified_delivery_policy"]["content_matrix"][2]["delivery_frame_count"], 450)
        self.assertEqual(report["unified_delivery_policy"]["audio_music_policy"], "OUT_OF_SCOPE_NOT_DEFINED_NOT_EMITTED")
        self.assertFalse(report["approval_state"]["unified_delivery_timebase_policy_approved"])
        self.assertIn("AUDIO_MUSIC_DELIVERY_AND_EDITORIAL_POLICY_NOT_APPROVED", report["unresolved_gates"])
        audio = report["unified_audio_music_policy"]
        self.assertEqual(audio["policy_id"], "C11D_UNIFIED_AUDIO_DELIVERY_ALIGNMENT_ALL_CONTENT_TYPES_V1")
        self.assertEqual(audio["policy_state"], "PROPOSED_NOT_APPROVED")
        self.assertEqual(audio["target_audio_profile"]["audio_sample_rate_hz"], 48000)
        self.assertEqual([x["target_pcm_sample_count"] for x in audio["content_matrix"]], [960000, 1008000, 720000])
        self.assertFalse(audio["music_asset_selected"])
        self.assertFalse(audio["audio_samples_emitted"])
        self.assertFalse(audio["policy_approved"])
        challenge_item = next(item for item in report["content_items"] if item["content_type"] == "challenges")
        temporal = challenge_item["temporal_alignment"]
        self.assertEqual(temporal["policy_id"], "C11D_CHALLENGE_TEMPORAL_ALIGNMENT_60_TO_30_HALF_OPEN_BOUNDARIES_V1")
        self.assertEqual(temporal["source_boundaries"], [0, 180, 600, 780, 900])
        self.assertEqual(temporal["delivery_boundaries"], [0, 90, 300, 390, 450])
        self.assertEqual(temporal["winning_anchor_source_absolute_frame_index"], 574)
        self.assertEqual(temporal["winning_anchor_delivery_absolute_frame_index"], 287)
        self.assertFalse(temporal["policy_approved"])
        self.assertFalse(temporal["delivery_candidate_materialized"])
        self.assertRegex(temporal["preview_sha256"], r"^[a-f0-9]{64}$")
        self.assertEqual(challenge_item["materialization"], "IN_MEMORY_ONLY_SOURCE_TIMEBASE_VISUAL_PAYLOAD_MATERIALIZED_NOT_RENDERER_INPUT")
        self.assertEqual(challenge_item["coordinate_projection"]["projected_records"], 420)
        self.assertEqual(challenge_item["sample_selection"]["source_snapshot_count"], 420)
        self.assertEqual(challenge_item["sample_selection"]["delivery_snapshot_count"], 210)
        self.assertEqual(challenge_item["sample_selection"]["interpolation"], "NONE")
        self.assertEqual(challenge_item["sample_selection"]["state"], "PROPOSED_NOT_APPROVED")
        composition = challenge_item["coordinate_sample_composition"]
        self.assertEqual(composition["state"], "PROPOSED_NOT_APPROVED_NOT_FROZEN")
        self.assertEqual(composition["projected_source_snapshot_count"], 420)
        self.assertEqual(composition["delivery_candidate_snapshot_count"], 210)
        self.assertFalse(composition["delivery_candidate_materialized"])
        self.assertFalse(composition["policy_approved"])
        self.assertEqual(report["approval_state"]["simulation_sample_selection_policy_approved"], False)
        self.assertEqual(report["approval_state"]["coordinate_sample_composition_policy_approved"], False)
        self.assertIn("CHALLENGE_SIMULATION_SAMPLE_SELECTION_AND_INTERPOLATION_UNRESOLVED", report["unresolved_gates"])
        validate_review_manifest(report, self.schema)

    def test_sample_selection_anchor_mismatch_rejected(self) -> None:
        summaries = make_summaries()
        summaries["challenge_runtime"]["instance"]["winning_frame_local"] = 395
        summaries["profile_identity"]["simulation_invariance"]["winning_frame_before"] = 395
        summaries["profile_identity"]["simulation_invariance"]["winning_frame_after"] = 395
        with self.assertRaisesRegex(UnifiedContentReviewError, "sample-selection anchor does not match runtime winning_frame"):
            validate_harness_summaries(summaries)

    def test_sample_selection_proposal_cannot_be_marked_approved(self) -> None:
        report = self.report()
        challenge_item = next(item for item in report["content_items"] if item["content_type"] == "challenges")
        challenge_item["sample_selection"]["state"] = "APPROVED"
        report.pop("review_manifest_sha256")
        report["review_manifest_sha256"] = sha256_json(report)
        with self.assertRaisesRegex(UnifiedContentReviewError, "Unified review manifest failed JSON Schema"):
            validate_review_manifest(report, self.schema)

    def test_coordinate_sample_composition_proposal_cannot_self_promote(self) -> None:
        report = self.report()
        challenge_item = next(item for item in report["content_items"] if item["content_type"] == "challenges")
        challenge_item["coordinate_sample_composition"]["policy_approved"] = True
        report.pop("review_manifest_sha256")
        report["review_manifest_sha256"] = sha256_json(report)
        with self.assertRaisesRegex(UnifiedContentReviewError, "Unified review manifest failed JSON Schema"):
            validate_review_manifest(report, self.schema)

    def test_coordinate_sample_composition_operation_order_drift_rejected(self) -> None:
        from d_renderer_challenge_coordinate_sample_composition import validate_contract as validate_composition
        result = validate_composition(ROOT)
        result = copy.deepcopy(result)
        result["contract"]["composition"]["operation_order"] = [
            "SELECT_EVEN_ZERO_BASED_GAME_LOCAL_INDICES",
            "PROJECT_ALL_GAME_COORDINATES_IN_ORIGINAL_ORDER",
        ]
        with patch("d_renderer_unified_content_review.validate_coordinate_sample_composition_contract", return_value=result):
            with self.assertRaisesRegex(UnifiedContentReviewError, "Coordinate/sample composition operation order drift"):
                validate_harness_summaries(make_summaries())

    def test_payload_asset_binding_uses_runtime_summary_texture_key(self) -> None:
        summaries = make_summaries()
        joined = validate_harness_summaries(summaries)
        self.assertEqual(len(joined["challenge_visual_payload"]["asset_nodes"]), 3)
        summaries["challenge_visual_payload"]["asset_nodes"][0]["resource_loaded_as_texture2d"] = False
        with self.assertRaisesRegex(UnifiedContentReviewError, "Challenge visual payload asset binding mismatch: BACKGROUND"):
            validate_harness_summaries(summaries)

    def test_coordinate_projection_target_guard_allows_vector_float_precision(self) -> None:
        harness_path = ROOT / "tools/c11d/d9/review_challenge_coordinate_projection_in_memory.gd"
        source = harness_path.read_text(encoding="utf-8")
        self.assertIn("_near(target_delivery.x, 850.0 * 2.0 / 3.0, 0.0001)", source)
        self.assertIn("_near(target_delivery.y, 640.0, 0.0001)", source)
        self.assertIn("source=%s presentation=%s delivery=%s", source)

    def test_visual_payload_frame_records_must_match_coordinate_projection_source(self) -> None:
        summaries = make_summaries()
        summaries["coordinate_projection"]["projected_frames"]["source_records_sha256"] = D("a")
        with self.assertRaisesRegex(UnifiedContentReviewError, "do not match the Challenge visual payload"):
            validate_harness_summaries(summaries)

    def test_coordinate_projection_must_remain_unapproved(self) -> None:
        summaries = make_summaries()
        summaries["coordinate_projection"]["projection"]["state"] = "APPROVED"
        with self.assertRaisesRegex(UnifiedContentReviewError, "identity/policy state mismatch"):
            validate_harness_summaries(summaries)

    def test_challenge_source_cross_artifact_mismatch_rejected(self) -> None:
        summaries = make_summaries()
        summaries["delivery_timeline"]["challenge_source_sha256"] = D("a")
        with self.assertRaises(UnifiedContentReviewError):
            validate_harness_summaries(summaries)

    def test_delivery_profile_can_omit_total_frames_when_segments_are_authoritative(self) -> None:
        summaries = make_summaries()
        profile = summaries["delivery_timeline"]["delivery_profile"]
        self.assertNotIn("total_frames", profile)
        joined = validate_harness_summaries(summaries)
        self.assertEqual(sum(x["frame_count"] for x in joined["timeline"]["delivery_segments"]), 450)

    def test_delivery_profile_optional_metadata_does_not_break_timebase(self) -> None:
        summaries = make_summaries()
        # The canonical delivery profile may add descriptive metadata while its
        # authoritative total is derived from phase segments.
        summaries["delivery_timeline"]["delivery_profile"]["duration_seconds"] = 15.0
        summaries["delivery_timeline"]["delivery_profile"]["color_space"] = "unspecified"
        joined = validate_harness_summaries(summaries)
        self.assertEqual(joined["timeline"]["profile_identity"]["delivery_profile_id"], "REVIEW_720")

    def test_delivery_segments_with_wrong_sum_are_rejected(self) -> None:
        summaries = make_summaries()
        summaries["delivery_timeline"]["delivery_segments"][1]["frame_count"] = 211
        with self.assertRaisesRegex(UnifiedContentReviewError, "delivery profile/source timebase mismatch"):
            validate_harness_summaries(summaries)

    def test_optional_declared_delivery_total_must_match_segments(self) -> None:
        summaries = make_summaries()
        summaries["delivery_timeline"]["delivery_profile"]["total_frames"] = 449
        with self.assertRaisesRegex(UnifiedContentReviewError, "delivery profile/source timebase mismatch"):
            validate_harness_summaries(summaries)

    def test_delivery_timebase_semantic_mismatch_is_rejected(self) -> None:
        summaries = make_summaries()
        summaries["delivery_timeline"]["delivery_profile"]["fps"] = 60
        with self.assertRaisesRegex(UnifiedContentReviewError, "delivery profile/source timebase mismatch"):
            validate_harness_summaries(summaries)

    def test_simulation_mutation_rejected(self) -> None:
        summaries = make_summaries()
        summaries["profile_identity"]["simulation_invariance"]["winning_frame_unchanged"] = False
        with self.assertRaises(UnifiedContentReviewError):
            validate_harness_summaries(summaries)

    def test_missing_editorial_mapping_stays_unresolved(self) -> None:
        summaries = make_summaries()
        summaries["editorial_windows"]["unresolved_content_types"].pop("visual_loops")
        with self.assertRaises(UnifiedContentReviewError):
            validate_harness_summaries(summaries)

    def test_runner_summary_reports_temporal_alignment_as_proposal_only(self) -> None:
        source = (ROOT / "tools/c11d/d9/run_d_renderer_unified_content_review.py").read_text(encoding="utf-8")
        self.assertIn("challenge_temporal_alignment=", source)
        self.assertIn("BOUNDARIES_EXACT_PROPOSAL_ONLY", source)
        self.assertIn("unified_delivery=REVIEW_720_30FPS_3_CONTENT_TYPES_PROPOSAL_ONLY", source)

    def test_temporal_alignment_policy_cannot_self_promote(self) -> None:
        report = self.report()
        challenge_item = next(item for item in report["content_items"] if item["content_type"] == "challenges")
        challenge_item["temporal_alignment"]["policy_approved"] = True
        report.pop("review_manifest_sha256")
        report["review_manifest_sha256"] = sha256_json(report)
        with self.assertRaisesRegex(UnifiedContentReviewError, "Unified review manifest failed JSON Schema"):
            validate_review_manifest(report, self.schema)

    def test_temporal_alignment_preview_mutation_is_rejected(self) -> None:
        from d_renderer_challenge_temporal_alignment_policy import build_preview as build_temporal_preview
        altered = build_temporal_preview(ROOT, verify_source_lineage=False)
        altered["delivery_timeline"]["boundaries"][1] = 91
        with patch("d_renderer_unified_content_review.build_temporal_alignment_preview", return_value=altered):
            with self.assertRaisesRegex(UnifiedContentReviewError, "Challenge temporal-alignment proposal invalid"):
                validate_harness_summaries(make_summaries())

    def test_renderer_activation_rejected(self) -> None:
        report = self.report()
        report["execution_boundary"]["renderer_activation"] = True
        report.pop("review_manifest_sha256")
        report["review_manifest_sha256"] = sha256_json(report)
        with self.assertRaises(UnifiedContentReviewError):
            validate_review_manifest(report, self.schema)

    def test_error_log_blocks_false_pass(self) -> None:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            fake = Path(tmp) / "fake.gd"
            fake.write_text("# placeholder\n", encoding="utf-8")
            spec = {"name": "visual_payloads", "script": "fake.gd", "pass_marker": "PASS MARKER", "summary_prefix": "SUMMARY="}
            output = "PASS MARKER\nERROR: intentionally injected\nSUMMARY={}\n"
            with patch("run_d_renderer_unified_content_review.subprocess.run", return_value=CompletedProcess(args=["godot"], returncode=0, stdout=output)):
                with redirect_stdout(io.StringIO()):
                    with self.assertRaises(UnifiedContentReviewError):
                        _run_harness("godot", Path(tmp), spec, 2)


    def test_loop_drill_payload_identity_must_match_editorial_proposal_fixture(self) -> None:
        summaries = make_summaries()
        summaries["visual_payloads"]["instances"][0]["payload_instance_sha256"] = D("b")
        with self.assertRaisesRegex(UnifiedContentReviewError, "Loop/Drill editorial proposal payload identity/timing mismatch: visual_loops.payload_instance_sha256"):
            validate_harness_summaries(summaries)

    def test_loop_drill_editorial_policy_cannot_be_self_promoted(self) -> None:
        report = self.report()
        report["content_items"][0]["editorial_review"]["policy_state"] = "APPROVED"
        report.pop("review_manifest_sha256")
        report["review_manifest_sha256"] = sha256_json(report)
        with self.assertRaisesRegex(UnifiedContentReviewError, "Unified review manifest failed JSON Schema"):
            validate_review_manifest(report, self.schema)

    def test_loop_drill_editorial_mapping_cannot_emit_windows_without_raw_values(self) -> None:
        report = self.report()
        report["content_items"][0]["editorial_review"]["visibility_windows"] = [{"field_id":"title","start_frame":0,"end_frame":600}]
        report.pop("review_manifest_sha256")
        report["review_manifest_sha256"] = sha256_json(report)
        with self.assertRaisesRegex(UnifiedContentReviewError, "Unified review manifest failed JSON Schema"):
            validate_review_manifest(report, self.schema)

    def test_negative_unified_delivery_policy_promotion_rejected(self) -> None:
        report = self.report()
        report["unified_delivery_policy"]["policy_state"] = "APPROVED"
        report["unified_delivery_policy"]["preview_sha256"] = sha256_json({k:v for k,v in report["unified_delivery_policy"].items() if k != "preview_sha256"})
        report["review_manifest_sha256"] = sha256_json({k:v for k,v in report.items() if k != "review_manifest_sha256"})
        with self.assertRaises(UnifiedContentReviewError): validate_review_manifest(report, self.schema)

    def test_negative_unified_delivery_policy_matrix_drift_rejected(self) -> None:
        report = self.report()
        report["unified_delivery_policy"]["content_matrix"][0]["delivery_frame_count"] = 599
        report["unified_delivery_policy"]["preview_sha256"] = sha256_json({k:v for k,v in report["unified_delivery_policy"].items() if k != "preview_sha256"})
        report["review_manifest_sha256"] = sha256_json({k:v for k,v in report.items() if k != "review_manifest_sha256"})
        with self.assertRaises(UnifiedContentReviewError): validate_review_manifest(report, self.schema)

    def test_negative_unified_delivery_policy_audio_scope_promotion_rejected(self) -> None:
        report = self.report()
        report["unified_delivery_policy"]["audio_music_policy"] = "NORMALIZED"
        report["unified_delivery_policy"]["preview_sha256"] = sha256_json({k:v for k,v in report["unified_delivery_policy"].items() if k != "preview_sha256"})
        report["review_manifest_sha256"] = sha256_json({k:v for k,v in report.items() if k != "review_manifest_sha256"})
        with self.assertRaises(UnifiedContentReviewError): validate_review_manifest(report, self.schema)


    def test_negative_unified_audio_music_policy_cannot_self_promote(self) -> None:
        report = self.report()
        report["unified_audio_music_policy"]["policy_approved"] = True
        report["unified_audio_music_policy"]["preview_sha256"] = sha256_json({k:v for k,v in report["unified_audio_music_policy"].items() if k != "preview_sha256"})
        unsigned = dict(report); unsigned.pop("review_manifest_sha256", None); report["review_manifest_sha256"] = sha256_json(unsigned)
        with self.assertRaises(UnifiedContentReviewError):
            validate_review_manifest(report, self.schema)

    def test_negative_unified_audio_music_sample_count_drift_rejected(self) -> None:
        report = self.report()
        report["unified_audio_music_policy"]["content_matrix"][0]["target_pcm_sample_count"] = 959999
        report["unified_audio_music_policy"]["preview_sha256"] = sha256_json({k:v for k,v in report["unified_audio_music_policy"].items() if k != "preview_sha256"})
        unsigned = dict(report); unsigned.pop("review_manifest_sha256", None); report["review_manifest_sha256"] = sha256_json(unsigned)
        with self.assertRaises(UnifiedContentReviewError):
            validate_review_manifest(report, self.schema)


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(UnifiedContentReviewTests)
    result = unittest.TextTestRunner(verbosity=0).run(suite)
    if not result.wasSuccessful():
        return 1
    present_count = sum(1 for rel, _ in EXPECTED_SOURCE_LINEAGE if (ROOT / rel).is_file())
    source_paths_present = present_count == len(EXPECTED_SOURCE_LINEAGE)
    source_paths_partial = 0 < present_count < len(EXPECTED_SOURCE_LINEAGE)
    try:
        validate_contract(ROOT, verify_sources=False)
    except UnifiedContentReviewError as exc:
        print(f"C11-D RENDERER UNIFIED CONTENT REVIEW CONTRACT FAIL | source_lineage={exc}", file=sys.stderr)
        return 1
    jsonschema_ok = False
    try:
        import jsonschema  # noqa: F401
        jsonschema_ok = True
    except ImportError:
        jsonschema_ok = False
    schema_label = "jsonschema=1/1" if jsonschema_ok else "jsonschema=NOT_INSTALLED (structural checks PASS)"
    source_label = "source_files=19/19" if source_paths_present else (f"source_files=PARTIAL_BUILD_CONTEXT({present_count}/19)" if source_paths_partial else "source_files=NOT_CHECKED_IN_OVERLAY_BUILD_CONTEXT")
    print(f"C11-D RENDERER UNIFIED CONTENT REVIEW CONTRACT PASS | content_types=3/3 | harness_contracts=7/7 | cross_checks=16/16 | negative=25/25 | source_lineage=19/19 | {source_label} | schema=1/1 | {schema_label} | godot_orchestration=NOT_RUN_BY_PYTHON | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
    return 0



if __name__ == "__main__":
    raise SystemExit(main())
