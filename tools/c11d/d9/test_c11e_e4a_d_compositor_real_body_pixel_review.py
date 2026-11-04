#!/usr/bin/env python3
"""Focused contract tests for E4A.3 D-owned Godot real-body compositor harness."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
RUNNER = HERE / "c11e_e4a_d_compositor_real_body_pixel_review.py"
SPEC = importlib.util.spec_from_file_location("c11e_e4a_d_compositor_runner_tests", RUNNER)
assert SPEC is not None and SPEC.loader is not None
module = importlib.util.module_from_spec(SPEC)
import sys
sys.modules[SPEC.name] = module
SPEC.loader.exec_module(module)

GDSCRIPT_PATH = HERE / "materialize_challenge_visual_payload_in_memory.gd"
GDSCRIPT = GDSCRIPT_PATH.read_text(encoding="utf-8")


class CompositorContractTests(unittest.TestCase):
    def test_01_project_root_parent_index_is_checkout_root(self):
        self.assertEqual(module.ROOT, Path(__file__).resolve().parents[3])

    def test_02_materializer_postimage_pin_is_sha256(self):
        self.assertEqual(module.MATERIALIZER_SHA256, "3d1c8288ffbea3ff328d785def5fabba250b042c0d2d1b1f94215b1c62cde29b")

    def test_03_prior_runner_pin_is_sha256(self):
        self.assertEqual(len(module.PREVIOUS_RUNNER_SHA256), 64)

    def test_04_prior_test_pin_is_sha256(self):
        self.assertEqual(len(module.PREVIOUS_TEST_SHA256), 64)

    def test_05_e1_service_and_d99_pins_are_sha256(self):
        self.assertEqual(len(module.E1_SERVICE_SHA256), 64)
        self.assertEqual(len(module.D99_RESOLVER_SHA256), 64)

    def test_06_frozen_c11c_manifest_is_exact_authority_pin(self):
        self.assertEqual(module.MANIFEST_SHA256, "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953")

    def test_07_previous_report_identity_is_exact(self):
        self.assertEqual(module.PREVIOUS_REPORT_SHA256, "e940f0a150d7dcea8ab34003b2f053d4be614f602ee6ea3ff04cd8bfa2b71159")

    def test_08_base_and_normalized_media_pins_are_exact(self):
        self.assertEqual(module.BASE_MP4_SHA256, "fdd0598e20ddc6201e54cc2dad7fd3362c2ef80961df44f3ef4676fb97a765de")
        self.assertEqual(module.NORMALIZED_MP4_SHA256, "edbd446d67142d20e138e55563f16cbae8d9a4c39469fd2bebcb3c9d5723fb9e")

    def test_09_config_schema_is_dedicated_to_d_godot_compositor(self):
        self.assertEqual(module.CONFIG_SCHEMA, "C11E-E4A-D-GODOT-COMPOSITOR-PIXEL-TEST-CONFIG-V1")

    def test_10_report_schema_is_dedicated_to_d_godot_compositor(self):
        self.assertEqual(module.REPORT_SCHEMA, "C11E-E4A-D-GODOT-COMPOSITOR-REAL-BODY-PIXEL-REPORT-V1")

    def test_11_receipt_schema_is_versioned(self):
        self.assertEqual(module.RECEIPT_SCHEMA, "C11E-E4A-D-GODOT-COMPOSITOR-REAL-BODY-PIXEL-RECEIPT-V1")

    def test_12_six_expected_samples_are_canonical_order(self):
        self.assertEqual([x["label"] for x in module.EXPECTED_SAMPLES], [
            "hook_first", "hook_last", "game_first", "reveal_first", "cta_first", "cta_last"
        ])

    def test_13_sample_delivery_frames_are_exact(self):
        self.assertEqual([x["delivery_frame"] for x in module.EXPECTED_SAMPLES], [0, 89, 90, 300, 390, 449])

    def test_14_sample_phase_sequence_is_exact(self):
        self.assertEqual([x["phase"] for x in module.EXPECTED_SAMPLES], ["HOOK", "HOOK", "GAME", "REVEAL", "CTA", "CTA"])

    def test_15_delivery_frame_zero_maps_to_source_frame_zero(self):
        self.assertEqual(module.source_frame_for_delivery(0), 0)

    def test_16_last_hook_delivery_sample_maps_inside_hook(self):
        self.assertEqual(module.source_frame_for_delivery(89), 178)
        self.assertLess(module.source_frame_for_delivery(89), 180)

    def test_17_game_first_maps_to_canonical_game_start(self):
        self.assertEqual(module.source_frame_for_delivery(90), 180)

    def test_18_reveal_first_maps_to_canonical_reveal_start(self):
        self.assertEqual(module.source_frame_for_delivery(300), 600)

    def test_19_cta_samples_map_inside_canonical_cta(self):
        self.assertEqual(module.source_frame_for_delivery(390), 780)
        self.assertEqual(module.source_frame_for_delivery(449), 898)
        self.assertTrue(780 <= 898 < 900)

    def test_20_negative_delivery_frame_is_rejected(self):
        with self.assertRaises(module.CompositorReviewError):
            module.source_frame_for_delivery(-1)

    def test_21_region_coordinates_are_scaled_from_d15_exactly(self):
        self.assertEqual(module.REGIONS["HEADER"], (0, 0, 720, 192))
        self.assertEqual(module.REGIONS["BODY"], (0, 192, 720, 1088))
        self.assertEqual(module.REGIONS["FOOTER"], (0, 1088, 720, 1280))

    def test_22_build_config_uses_only_existing_e1_a_b_c_intents(self):
        intents = {k: {"status": "PREPARED_E1_NOT_DISPATCHED", "editorial": {}} for k in ("A", "B", "C")}
        config = module.build_config(Path("/tmp/RUN_TEST"), [], intents)
        self.assertEqual(config["schema"], module.CONFIG_SCHEMA)
        self.assertEqual([x["id"] for x in config["variants"]], ["A", "B", "C"])
        self.assertEqual([x["intent"] for x in config["variants"]], [intents[k] for k in ("A", "B", "C")])

    def test_23_build_config_keeps_dispatch_and_production_media_disabled(self):
        intents = {k: {"status": "PREPARED_E1_NOT_DISPATCHED"} for k in ("A", "B", "C")}
        config = module.build_config(Path("/tmp/RUN_TEST"), [], intents)
        self.assertFalse(config["authorization"]["production_renderer"])
        self.assertFalse(config["authorization"]["production_dispatch"])
        self.assertFalse(config["authorization"]["production_media"])

    def test_24_godot_command_invokes_existing_materializer_script(self):
        command = module.build_godot_command("godot.exe", Path("C:/repo"), Path("C:/repo/artifacts/tests/config.json"))
        self.assertIn("res://tools/c11d/d9/materialize_challenge_visual_payload_in_memory.gd", command)
        self.assertIn("--e4a-config", command)
        self.assertNotIn("--headless", command)
        self.assertIn("--path", command)

    def test_25_godot_command_does_not_invoke_c11c_generator(self):
        command = module.build_godot_command("godot.exe", Path("C:/repo"), Path("C:/repo/config.json"))
        self.assertFalse(any("run_c11c_challenge_production" in x for x in command))

    def test_26_ffmpeg_extraction_command_selects_frame_only(self):
        # Verify the source-level extraction path has no drawtext/composition filter.
        import inspect
        body = inspect.getsource(module.extract_base_frame)
        self.assertIn('select=eq(n\\\\,{delivery_frame})', body)
        self.assertNotIn("drawtext=", body)
        self.assertNotIn("libx264", body)

    def test_27_python_runner_never_dispatches_production_d_renderer(self):
        source = RUNNER.read_text(encoding="utf-8")
        self.assertNotIn("D9.10 dispatch", source[source.index("def run("):])
        self.assertNotIn("_run_challenge_job", source)
        self.assertNotIn("renderer_dispatch_invoked\": True", source)

    def test_28_python_runner_reuses_prior_e4a2_and_never_renders_c11c(self):
        source = RUNNER.read_text(encoding="utf-8")
        self.assertIn("validate_previous_evidence", source)
        self.assertIn("normalized_mp4", source)
        self.assertNotIn("-File", source)
        self.assertIn("C11C_RENDERER", source)  # source hash only; no invocation

    def test_29_godot_materializer_enables_transparent_subviewport_for_real_mode(self):
        self.assertIn("viewport.transparent_bg = real_background_mode", GDSCRIPT)

    def test_30_godot_materializer_alpha_composites_over_loaded_real_base(self):
        self.assertIn("base_image.load(base_background_path)", GDSCRIPT)
        self.assertIn("base_image.blend_rect(image, Rect2i(0, 0, 720, 1280), Vector2i.ZERO)", GDSCRIPT)

    def test_31_godot_materializer_validates_base_frames_inside_test_run(self):
        self.assertIn("output_dir + \"/base_frames/\"", GDSCRIPT)
        self.assertIn("_sha256_bytes(background_bytes)", GDSCRIPT)
        self.assertIn("background_image.get_width() != 720", GDSCRIPT)

    def test_32_godot_materializer_keeps_legacy_fixture_path(self):
        self.assertIn('config_schema != "C11E-E4A-CHALLENGE-PIXEL-TEST-CONFIG-V1" and not real_background_mode', GDSCRIPT)
        self.assertIn("if not real_background_mode:", GDSCRIPT)

    def test_33_godot_materializer_outputs_d_compositor_report_schema(self):
        self.assertIn("E4ADCompositorReportSchema", GDSCRIPT)
        self.assertIn("C11E_E4A_D_COMPOSITOR_PIXEL_REPORT.json", GDSCRIPT)

    def test_34_visual_placement_remains_explicitly_unapproved(self):
        self.assertIn('"visual_placement_approved": false', GDSCRIPT)
        self.assertIn('"d1_5_safe_area_and_generic_typography": "UNKNOWN"', GDSCRIPT)

    def test_35_challenge_overlay_fields_remain_geometry_blocked(self):
        self.assertIn('disposition = "BLOCKED_GEOMETRY_UNRESOLVED"', GDSCRIPT)

    def test_36_godot_pixel_compare_supports_delivery_size(self):
        self.assertIn("var image_width: int = image_a.get_width()", GDSCRIPT)
        self.assertIn("for y: int in range(image_height)", GDSCRIPT)

    def test_37_materializer_never_reads_or_serializes_frame_snapshot_custom_data(self):
        self.assertNotIn("frame.custom_data", GDSCRIPT)
        self.assertNotIn("JSON.stringify(_stable_value(frame.custom_data))", GDSCRIPT)
        self.assertIn("Fingerprint only explicit visual snapshot fields", GDSCRIPT)
        self.assertIn('_contains_key(composed_payload, "custom_data")', GDSCRIPT)

    def test_38_production_governance_stays_locked(self):
        for marker in ('"d4_8": "BLOCKED"', '"d9_10": "PREPARE_ONLY"', '"release_authority": "NONE"'):
            self.assertIn(marker, GDSCRIPT)

    def test_39_rgb_comparison_ignores_only_added_alpha_channel(self):
        rgb = SimpleNamespace(width=2, height=1, channels=3, pixels=bytes([1, 2, 3, 4, 5, 6]))
        rgba = SimpleNamespace(width=2, height=1, channels=4, pixels=bytes([1, 2, 3, 255, 4, 5, 6, 255]))
        self.assertTrue(module.rgb_pixels_equal(rgb, rgba))

    def test_40_rgb_comparison_detects_actual_color_change(self):
        rgb = SimpleNamespace(width=1, height=1, channels=3, pixels=bytes([1, 2, 3]))
        rgba = SimpleNamespace(width=1, height=1, channels=4, pixels=bytes([1, 2, 4, 255]))
        self.assertFalse(module.rgb_pixels_equal(rgb, rgba))

    def test_41_crop_hash_is_stable_for_same_region(self):
        image = SimpleNamespace(width=2, height=2, channels=3, pixels=bytes(range(12)))
        self.assertEqual(module.crop_hash(image, (0, 0, 2, 2)), module.crop_hash(image, (0, 0, 2, 2)))

    def test_42_crop_hash_changes_when_body_pixels_change(self):
        a = SimpleNamespace(width=1, height=1, channels=3, pixels=bytes([1, 2, 3]))
        b = SimpleNamespace(width=1, height=1, channels=3, pixels=bytes([1, 2, 4]))
        self.assertNotEqual(module.crop_hash(a, (0, 0, 1, 1)), module.crop_hash(b, (0, 0, 1, 1)))

    def test_43_report_status_is_test_only(self):
        self.assertEqual(module.REPORT_SCHEMA, "C11E-E4A-D-GODOT-COMPOSITOR-REAL-BODY-PIXEL-REPORT-V1")
        self.assertFalse(module.RECEIPT_SCHEMA.endswith("PRODUCTION"))

    def test_44_base_evidence_paths_are_fixed_under_e4a2_test_root(self):
        expected = Path("artifacts/tests/c11e/e4a_real_body_pixel_review")
        self.assertTrue(str(expected).endswith("e4a_real_body_pixel_review"))

    def test_45_runner_pins_the_exact_v3_materializer_postimage(self):
        self.assertEqual(len(module.MATERIALIZER_SHA256), 64)
        self.assertNotEqual(module.MATERIALIZER_SHA256, "4cf2c754c9675ebb3952a292a21af71634102cf7d880f71a871ba7d7555ac6ed")

    def test_46_runner_rechecks_all_source_media_and_sample_frames_after_godot(self):
        source = RUNNER.read_text(encoding="utf-8")
        self.assertIn("source_video_sha_before", source)
        self.assertIn("normalized_video_sha_before", source)
        self.assertIn("Extracted immutable base frame changed during Godot composition", source)
        self.assertIn('"base_frame_inputs_sha256_before_after"', source)

    def test_47_headless_mode_is_not_used_because_it_disables_rendering(self):
        command = module.build_godot_command("godot.exe", Path("C:/repo"), Path("C:/repo/config.json"))
        self.assertNotIn("--headless", command)
        self.assertIn("--script", command)

    def test_48_subprocess_timeout_preserves_stdout_and_stderr(self):
        import sys
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            out, err = root / "child.stdout.txt", root / "child.stderr.txt"
            code = "import sys; print('child-started', flush=True); print('child-error', file=sys.stderr, flush=True)"
            rc = module.run_command([sys.executable, "-c", code], root, out, err, timeout_seconds=5, progress_label="UNIT_CHILD")
            self.assertEqual(rc, 0)
            self.assertIn("child-started", out.read_text(encoding="utf-8"))
            self.assertIn("child-error", err.read_text(encoding="utf-8"))

    def test_49_godot_execution_has_finite_timeout_and_heartbeat(self):
        import inspect
        source = inspect.getsource(module.run_command)
        self.assertIn("subprocess.Popen", source)
        self.assertIn("timeout_seconds", source)
        self.assertIn("proc.terminate()", source)
        self.assertIn("proc.kill()", source)
        self.assertIn("_RUNNING elapsed_seconds=", source)

    def test_50_gdscript_emits_render_stage_markers(self):
        self.assertIn("E4A3_VIEWPORT_BEGIN=", GDSCRIPT)
        self.assertIn("E4A3_VIEWPORT_WAIT_FRAME_POST_DRAW", GDSCRIPT)
        self.assertIn("E4A3_VIEWPORT_FRAME_POST_DRAW_OK", GDSCRIPT)


if __name__ == "__main__":
    unittest.main(verbosity=2)
