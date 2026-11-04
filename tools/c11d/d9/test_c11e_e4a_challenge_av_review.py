from __future__ import annotations
import ast
import hashlib
import importlib.util
import inspect
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("c11e_e4a_challenge_av_review.py")
SPEC = importlib.util.spec_from_file_location("e4a4_runner_under_test", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)
SOURCE = SCRIPT.read_text(encoding="utf-8")
TREE = ast.parse(SOURCE)

class E4A4RunnerContractTests(unittest.TestCase):
    def test_01_runner_compiles_as_valid_python_ast(self):
        self.assertIsInstance(TREE, ast.Module)

    def test_02_frozen_manifest_pin_is_immutable_expected_value(self):
        self.assertEqual(MODULE.REPO_MANIFEST_SHA, "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953")

    def test_03_e4a2_receipt_pin_is_exact(self):
        self.assertEqual(MODULE.E4A2_RECEIPT_SHA, "b23a5f0c1557b52b724c99ac90a671e0a8d8457dcd5e605f8d097c517f366308")

    def test_04_e4a2_report_pin_is_exact(self):
        self.assertEqual(MODULE.E4A2_REPORT_SHA, "e940f0a150d7dcea8ab34003b2f053d4be614f602ee6ea3ff04cd8bfa2b71159")

    def test_05_normalized_video_sha_is_exact(self):
        self.assertEqual(MODULE.BASE_MP4_SHA, "edbd446d67142d20e138e55563f16cbae8d9a4c39469fd2bebcb3c9d5723fb9e")

    def test_06_e4a3_receipt_pin_is_exact(self):
        self.assertEqual(MODULE.E4A3_RECEIPT_SHA, "3670428feae3b34766677b4cdba3985babecbda9ee781eebe4cc57c318cd9f1c")

    def test_07_e4a3_report_pin_is_exact(self):
        self.assertEqual(MODULE.E4A3_REPORT_SHA, "ee1be803f4d0433347778793aab12228301aea5108f426011836c27dc268dc08")

    def test_08_e3_pipeline_is_reused_at_exact_pin(self):
        self.assertEqual(MODULE.E3_PIPELINE_SHA, "46b087683a3dcb460601c925373b84e390999d44d73141328285e6c8a633ba5d")

    def test_09_e1_service_is_read_only_pinned(self):
        self.assertEqual(MODULE.E1_SERVICE_SHA, "f0655d8d93df3b766b157d80a76a5bfc7b514d740815646f54c88ca788f602c0")

    def test_10_d3_v5_engine_pin_is_exact(self):
        self.assertEqual(MODULE.D3_ENGINE_SHA, "03ae7e2997796e0c67ca15c8886b1e5b290791a142b6631a572d1cba6eba4eb1")

    def test_11_d3_contract_pin_is_exact(self):
        self.assertEqual(MODULE.D3_CONTRACT_SHA, "12c59ce2a2135a49ce0d5968a29905a1e5890743507db1ee0039da1374efcfe8")

    def test_12_policy_approval_pin_is_exact(self):
        self.assertEqual(MODULE.APPROVED_POLICY_SHA, "764629384896a255cf992da89fa427c19f60f9b2e623b81ad17d909674b466b5")

    def test_13_gameplay_seed_is_preserved_from_real_challenge_source(self):
        self.assertEqual(MODULE.GAMEPLAY_SEED, 314159)

    def test_14_music_a_b_seed_is_the_historical_pilot_seed(self):
        self.assertEqual(MODULE.MUSIC_SEED_A, 840001)

    def test_15_music_control_seed_is_distinct(self):
        self.assertNotEqual(MODULE.MUSIC_SEED_A, MODULE.MUSIC_SEED_C)

    def test_16_tempo_is_marked_as_historical_fixture_only(self):
        self.assertEqual(MODULE.TEMPO_BPM_FIXTURE, 104)
        self.assertIn("not a product default", MODULE.__doc__.lower() + SOURCE.lower())

    def test_17_video_duration_is_derived_from_ffprobe(self):
        self.assertIn('duration = float(source["video_probe"]["duration_seconds"])', SOURCE)
        self.assertIn('frames = int(source["video_probe"]["frames"])', SOURCE)

    def test_18_input_video_must_be_720x1280_30fps_450_frames_15s(self):
        for token in ('("h264", 720, 1280, "yuv420p")', 'frames != 450', 'abs(fps - 30.0)', 'abs(duration - 15.0)'):
            self.assertIn(token, SOURCE)

    def test_19_audio_source_is_required_to_be_silent_of_audio_streams(self):
        self.assertIn('if len(videos) != 1 or audios:', SOURCE)

    def test_20_three_e1_intents_are_prepared_through_shared_service(self):
        self.assertIn('service.prepare_c11e_production_intent', SOURCE)
        self.assertIn('service.validate_c11e_production_intent', SOURCE)
        self.assertIn('request_origin="TEST"', SOURCE)

    def test_21_e1_preparation_never_claims_dispatch(self):
        self.assertIn('intent.get("status") != "PREPARED_E1_NOT_DISPATCHED"', SOURCE)
        self.assertIn('execution_boundary", {}).get("dispatch_authorized") is not False', SOURCE)

    def test_22_raw_request_enables_audio_for_test_intents_only(self):
        self.assertIn('"audio_enabled": True', SOURCE)
        self.assertIn('"request_origin": "TEST"', SOURCE)

    def test_23_d3_v5_invocation_uses_e1_music_seed_and_ffprobe_duration(self):
        self.assertIn('record = engine.render(engine_request, spec, profile, raw_path)', SOURCE)
        self.assertIn('"duration_seconds": duration', SOURCE)
        self.assertIn('"music_seed": seed', SOURCE)

    def test_24_mastering_uses_accepted_d3_3_loudnorm_parameters(self):
        self.assertIn('loudnorm=I=-14:TP=-1:LRA=7:print_format=summary', SOURCE)
        self.assertIn('"-t", "30"', SOURCE)

    def test_25_delivery_master_is_trimmed_to_source_duration(self):
        self.assertIn('atrim=duration={duration:.6f}', SOURCE)

    def test_26_mux_stream_copies_the_original_video(self):
        self.assertIn('"-c:v", "copy"', SOURCE)
        self.assertIn('"-c:a", "aac"', SOURCE)

    def test_27_ffprobe_requires_expected_video_frame_count_and_fps(self):
        self.assertIn('expected_video_frames=frames', SOURCE)
        self.assertIn('expected_video_fps=30.0', SOURCE)

    def test_28_video_stream_must_remain_identical(self):
        self.assertIn('all(v == source_video_hash for v in mux_video_hashes.values())', SOURCE)

    def test_29_decoded_audio_ab_must_repeat(self):
        self.assertIn('decoded_hashes["A"] == decoded_hashes["B_REPEAT"]', SOURCE)

    def test_30_changed_music_seed_must_change_decoded_audio(self):
        self.assertIn('decoded_hashes["A"] != decoded_hashes["C_CHANGED_MUSIC_SEED"]', SOURCE)

    def test_31_layout_is_explicitly_not_approved(self):
        self.assertIn('"layout_approval": "NOT_GRANTED"', SOURCE)
        self.assertIn('"visual_placement_approved": False', SOURCE)

    def test_32_d_overlay_is_explicitly_not_embedded_in_video(self):
        self.assertIn('"fullframe_d_compositor_embedded_in_mp4": False', SOURCE)
        self.assertIn('"D_layer_not_embedded": True', SOURCE)

    def test_33_no_c11c_renderer_or_production_dispatch_symbol(self):
        for forbidden in ('run_c11c_challenge_production', 'run_c11c_challenge_bulk', 'd_render_adapter.dispatch', 'renderer_dispatch('):
            self.assertNotIn(forbidden, SOURCE)

    def test_34_no_protected_c11c_mechanics_or_core_audio_edit(self):
        for forbidden in ('SimulationResult', 'WinningFrameDetector', 'RenderedFrameStream', 'FrameSnapshot.custom_data', 'core/audio'):
            self.assertNotIn(forbidden, SOURCE)

    def test_35_governance_stays_test_only(self):
        for token in ('"production_dispatch": False', '"production_renderer": False', '"production_media_created": False', '"release_authority": "NONE"'):
            self.assertIn(token, SOURCE)

    def test_36_each_run_uses_a_fresh_non_overwriting_evidence_directory(self):
        self.assertIn('run_root.mkdir(parents=False, exist_ok=False)', SOURCE)

    def test_37_command_logs_are_reused_from_pinned_e3_pipeline(self):
        self.assertIn('e3._run(', SOURCE)
        self.assertIn('e3._audio_metrics(', SOURCE)

    def test_38_failure_emits_blocked_receipt_not_pass(self):
        self.assertIn('receipt["status"] = "BLOCKED"', SOURCE)
        self.assertIn('receipt["result"] = "FAIL"', SOURCE)

    def test_39_evidence_archive_is_created_from_run_root(self):
        self.assertIn('zipfile.ZipFile(zip_path', SOURCE)
        self.assertIn('E4A4_ZIP_SHA256=', SOURCE)

    def test_40_path_hash_helper_is_sha256(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "x.txt"
            p.write_text("E4A4", encoding="utf-8")
            self.assertEqual(MODULE.sha256_file(p), hashlib.sha256(b"E4A4").hexdigest())

    def test_41_pin_check_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "source.py"
            p.write_text("changed", encoding="utf-8")
            with self.assertRaises(MODULE.E4A4Error):
                MODULE.assert_pin(Path(td), "source.py", "0" * 64)

    def test_42_json_writer_creates_valid_readable_receipt(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "sub" / "receipt.json"
            MODULE.write_json(p, {"status": "PASS", "release_authority": "NONE"})
            self.assertEqual(json.loads(p.read_text(encoding="utf-8"))["status"], "PASS")

if __name__ == "__main__":
    unittest.main(verbosity=2)
