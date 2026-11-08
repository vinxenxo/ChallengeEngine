#!/usr/bin/env python3
"""Combined R1V base 32-test regression plus integrated family-audio A/V tests."""
from __future__ import annotations
import argparse
import importlib.util
import json
import math
import struct
import sys
import tempfile
import unittest
from datetime import datetime
import wave
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT_ROOT: Path | None = None
R1P_ARCHIVE: Path | None = None
PAYLOAD_ROOT: Path | None = None


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {name} from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


av = _load_module("c11e_r1v_av", HERE / "c11e_r1v_av_family_qualification_v1.py")
base_tests = None


class R1VAVContractTests(unittest.TestCase):
    def setUp(self):
        if PROJECT_ROOT is None or R1P_ARCHIVE is None:
            self.skipTest("project-root and R1P archive arguments are mandatory")
        self.root = PROJECT_ROOT
        self.r1p = R1P_ARCHIVE
        self.policy = self.root / "definitions/c11d/production/C11E_D4_8_R1V_FAMILY_AUDIO_SCOPE_AMENDMENT_V1.json"
        self.approval = self.root / "definitions/c11d/production/C11E_D4_8_R1V_FAMILY_AUDIO_APPROVAL_AMENDMENT_20261108_V1.json"
        self.base = av.load_base_module(self.root)
        self.registry_path = self.root / "profiles/presentation/c11c_visual_music_profiles.json"
        self.registry = json.loads(self.registry_path.read_text(encoding="utf-8-sig"))
        self.selectors = av.load_r1p_audio_selector_data(self.root, self.r1p, self.base, self.registry_path)

    def test_01_audio_scope_amendment_matches_explicit_operator_approval(self):
        result = av.verify_audio_scope_amendment(self.root, self.policy, self.approval)
        self.assertEqual(result["selector_count"], 5)
        self.assertEqual(result["repeat_count"], 2)
        self.assertEqual(result["av_outputs"], 10)
        self.assertEqual(result["new_launcher_invocations"], 9)

    def test_02_audio_policy_rejects_tampered_copy(self):
        import shutil
        with tempfile.TemporaryDirectory() as td:
            altered = Path(td) / self.policy.name
            shutil.copy2(self.policy, altered)
            altered.write_bytes(altered.read_bytes() + b" ")
            with self.assertRaises(av.AVQualificationError):
                av.verify_audio_scope_amendment(self.root, altered, self.approval)

    def test_03_three_native_c11c_music_source_pins_match(self):
        result = av.verify_audio_source_pins(self.root)
        self.assertEqual(result["pin_count"], 3)

    def test_04_exactly_five_r1p_audio_selectors_are_projected(self):
        self.assertEqual(len(self.selectors), 5)
        self.assertEqual({x["grammar_id"] for x in self.selectors},
                         {"radial_bloom", "harmonic_membrane", "dipole_field", "swarm", "astrolabe"})
        # Windows path budget regression: run IDs are compact while retaining an
        # six-hex collision-resistant suffix; every planned artifact is <=259.
        run_id = av.build_run_id(datetime(2026, 11, 8, 1, 35, 50), "ABCDEF")
        self.assertEqual(run_id, "Q5_013550_ABCDEF")
        budget = av.windows_path_budget(
            r"C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS",
            run_id, self.selectors,
            "R1V_Q5_20261107_235828_6DE382A1_FRACTAL_BLOOM_A")
        self.assertLessEqual(budget["max_path_chars"], 259, budget["longest_path"])
        # FFmpeg 9 removed the legacy global -vsync option. The in-memory pixel
        # decoder must use the per-output-stream passthrough mode so every source
        # frame is retained without duplication/drop and no frames are spooled.
        decode_args = av.build_pixel_decode_args(Path("source.mp4"))
        self.assertEqual(decode_args[decode_args.index("-fps_mode") + 1], "passthrough")
        self.assertNotIn("-vsync", decode_args)
        self.assertEqual(decode_args[-5:], ["-pix_fmt", "yuv420p", "-f", "rawvideo", "pipe:1"])

    def test_05_gameplay_and_music_seed_domains_remain_distinct(self):
        for selector in self.selectors:
            self.assertNotEqual(selector["gameplay_seed"], selector["music_seed"])
            self.assertFalse(selector["r1p_music_seed_domain"]["music_seed_consumed_by_visual_parameters"])

    def test_06_family_music_profile_mapping_matches_c11c_registry(self):
        expected = {
            "fractal": "ORGANIC_BLOOM", "geometric": "CIRCUIT_PULSE",
            "invisible_forces": "FLOWING_VECTOR", "living_particles": "ORGANIC_BLOOM",
            "sacred_symmetry": "ORBITAL_RITUAL",
        }
        for selector in self.selectors:
            self.assertEqual(selector["music_profile_id"], expected[selector["internal_family_id"]])

    def test_07_music_command_uses_r1p_music_seed_not_gameplay_seed(self):
        selector = self.selectors[0]
        command = av.build_music_command("python.exe", self.root / "tools/prototypes/c11c_common/C11CSafeAmbient.py",
                                         Path("music.wav"), selector)
        self.assertEqual(command[3], str(selector["music_seed"]))
        self.assertNotEqual(command[3], str(selector["gameplay_seed"]))

    def test_08_music_command_binds_family_loop_grammar_and_cycle_count(self):
        selector = self.selectors[1]
        command = av.build_music_command("python.exe", Path("helper.py"), Path("music.wav"), selector)
        self.assertEqual(command[-3:], [selector["internal_family_id"], "loop", selector["grammar_id"]])
        self.assertEqual(command[4], str(selector["loop_cycles"]))

    def test_09_native_mux_uses_copy_video_and_fixed_aac_delivery(self):
        command = av.build_mux_command("ffmpeg", Path("source.mp4"), Path("music.wav"), Path("final.mp4"))
        self.assertEqual(command[command.index("-c:v") + 1], "copy")
        self.assertEqual(command[command.index("-c:a") + 1], "aac")
        self.assertEqual(command[command.index("-b:a") + 1], "192k")
        self.assertEqual(command[command.index("-ar") + 1], "44100")
        self.assertEqual(command[command.index("-ac") + 1], "2")
        self.assertNotIn("-vf", command)
        self.assertNotIn("-filter_complex", command)

    def test_10_godot_utf16_log_accepts_unicode_multiply_sign_and_spaces(self):
        text = "Movie Maker mode enabled, recording movie in 720×1280 @ 30 FPS...\r\n660 frames at 30 FPS (movie length: 00:00:22:00)\r\n"
        parsed = av.parse_godot_capture_log(text.encode("utf-16"), 720, 1280, 30, 660)
        self.assertEqual(parsed["completed_frames"], 660)
        self.assertEqual(parsed["completed_fps"], 30)

    def test_11_godot_log_rejects_wrong_geometry_or_rate(self):
        text = "recording movie in 540×960 @ 30 FPS\n660 frames at 30 FPS\n"
        with self.assertRaises(av.AVQualificationError):
            av.parse_godot_capture_log(text.encode("utf-8"), 720, 1280, 30, 660)

    def test_12_source_pixel_format_accepts_observed_legacy_full_range_pair(self):
        self.assertEqual(av.validate_source_pixel_format({"pix_fmt": "yuvj420p", "color_range": "pc"}), "yuvj420p")

    def test_13_source_pixel_format_accepts_tv_pair_only_as_explicit_alternative(self):
        self.assertEqual(av.validate_source_pixel_format({"pix_fmt": "yuv420p", "color_range": "tv"}), "yuv420p")

    def test_14_source_pixel_format_rejects_mismatched_or_other_pair(self):
        for stream in ({"pix_fmt": "yuvj420p", "color_range": "tv"},
                       {"pix_fmt": "yuv420p", "color_range": "pc"},
                       {"pix_fmt": "yuv444p", "color_range": "tv"}):
            with self.subTest(stream=stream), self.assertRaises(av.AVQualificationError):
                av.validate_source_pixel_format(stream)

    def test_15_audio_wav_metrics_accept_exact_pcm_contract_and_limits(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "fixture.wav"
            frames = 44100
            # A 440 Hz stereo tone at -18 dBFS; deterministic little-endian PCM16.
            samples = []
            for n in range(frames):
                value = int(32767 * 0.126 * math.sin(2 * math.pi * 440 * n / 44100))
                samples.extend((value, value))
            raw = struct.pack("<" + "h" * len(samples), *samples)
            with wave.open(str(path), "wb") as wf:
                wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(44100); wf.writeframes(raw)
            metrics = av.decode_audio_metrics(path, 1.0, self.registry["design_rules"])
            self.assertEqual(metrics["sample_rate"], 44100)
            self.assertEqual(metrics["channels"], 2)
            self.assertEqual(metrics["sample_frames"], 44100)
            self.assertGreaterEqual(metrics["rms"], 0.08)
            self.assertLessEqual(metrics["rms"], 0.16)

    def test_16_audio_wav_metrics_reject_wrong_sample_rate(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "wrong.wav"
            with wave.open(str(path), "wb") as wf:
                wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(48000)
                wf.writeframes(b"\x10\x00\x10\x00" * 48000)
            with self.assertRaises(av.AVQualificationError):
                av.decode_audio_metrics(path, 1.0, self.registry["design_rules"])

    def test_17_final_av_probe_accepts_two_stream_h264_aac_contract(self):
        source_stream = {"pix_fmt": "yuvj420p", "color_range": "pc"}
        probe = {"format": {"duration": "22.000"}, "streams": [
            {"codec_type": "video", "codec_name": "h264", "width": 720, "height": 1280,
             "r_frame_rate": "30/1", "nb_frames": "660", "pix_fmt": "yuvj420p", "color_range": "pc",
             "duration": "22.0", "start_time": "0.0"},
            {"codec_type": "audio", "codec_name": "aac", "sample_rate": "44100", "channels": 2,
             "channel_layout": "stereo", "duration": "22.0", "start_time": "0.0"},
        ]}
        selector = {"frame_count_consistency_only": 660, "duration_seconds": 22.0}
        result = av.validate_final_av_probe(probe, selector, source_stream)
        self.assertTrue(result["two_stream_contract"])

    def test_18_final_av_probe_rejects_audio_layout_or_video_stream_mutation(self):
        source_stream = {"pix_fmt": "yuvj420p", "color_range": "pc"}
        probe = {"format": {"duration": "22.0"}, "streams": [
            {"codec_type": "video", "codec_name": "h264", "width": 720, "height": 1280,
             "r_frame_rate": "30/1", "nb_frames": "660", "pix_fmt": "yuvj420p", "color_range": "pc",
             "duration": "22.0", "start_time": "0.0"},
            {"codec_type": "audio", "codec_name": "aac", "sample_rate": "48000", "channels": 1,
             "channel_layout": "mono", "duration": "22.0", "start_time": "0.0"},
        ]}
        with self.assertRaises(av.AVQualificationError):
            av.validate_final_av_probe(probe, {"frame_count_consistency_only": 660, "duration_seconds": 22.0}, source_stream)

    def test_19_repeat_comparison_requires_identical_video_pixels_wav_and_aac(self):
        rows = []
        for selector in self.selectors:
            for repeat in ("A", "B"):
                inv = {"frame_count": selector["frame_count_consistency_only"],
                       "pts": list(range(selector["frame_count_consistency_only"])),
                       "pixel_frame_hashes": ["1" * 64, "2" * 64],
                       "global_pixel_stream_sha256": "3" * 64,
                       "source_video_sha256": "4" * 64}
                audio = {"wav_sha256": "5" * 64, "aac_stream_sha256": "6" * 64}
                rows.append({"family_id": selector["family_id"], "repeat": repeat,
                             "source_inventory": inv, "audio": audio,
                             "music_seed": selector["music_seed"], "gameplay_seed": selector["gameplay_seed"]})
        result = av.compare_av_repeats(rows)
        self.assertEqual(result["pairs_passed"], 5)
        rows[-1]["audio"]["aac_stream_sha256"] = "f" * 64
        with self.assertRaises(av.AVQualificationError):
            av.compare_av_repeats(rows)


class R1VPriorCaptureIntegrationTests(unittest.TestCase):
    def test_20_prior_fractal_bloom_a_capture_is_reusable_and_pinned(self):
        if sys.platform != "win32":
            self.skipTest("The original run's receipt paths are absolute Windows paths")
        if PROJECT_ROOT is None:
            self.skipTest("project-root was not supplied")
        result = av.verify_prior_fractal_a(PROJECT_ROOT)
        self.assertTrue(result["reused_without_relaunch"])
        self.assertEqual(result["source_video_sha256"], av.PRIOR_FRACTAL_A_MP4_SHA256)
        self.assertEqual(result["launcher_exit_code"], 0)


def main() -> int:
    global PROJECT_ROOT, R1P_ARCHIVE, PAYLOAD_ROOT
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--r1p-recovered-zip", type=Path, required=True)
    args = parser.parse_args()
    PROJECT_ROOT = args.project_root.resolve()
    PAYLOAD_ROOT = PROJECT_ROOT
    R1P_ARCHIVE = args.r1p_recovered_zip.resolve()
    global base_tests
    base_tests = _load_module("c11e_r1v_base_tests", PROJECT_ROOT / "tools/c11d/d9/test_c11e_r1v_five_family_qualification_v3.py")
    base_tests.PAYLOAD_ROOT = PAYLOAD_ROOT
    base_tests.PROJECT_ROOT = PROJECT_ROOT
    base_tests.R1P_ARCHIVE = R1P_ARCHIVE
    old_suite = unittest.defaultTestLoader.loadTestsFromModule(base_tests)
    new_suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    suite = unittest.TestSuite([old_suite, new_suite])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(json.dumps({
        "status": "PASS_R1V_AV_ACTIVE_CHECKOUT_TESTS" if result.wasSuccessful() else "FAIL_R1V_AV_TESTS",
        "tests_run": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
        "skipped": len(result.skipped),
        "active_checkout": str(PROJECT_ROOT), "music_route": "C11C_FAMILY_MUSIC_V4",
        "av_outputs_authorized": 10,
    }, ensure_ascii=False, sort_keys=True))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
