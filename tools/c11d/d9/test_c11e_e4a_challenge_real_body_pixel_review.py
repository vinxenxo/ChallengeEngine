#!/usr/bin/env python3
"""Unit tests for the E4A.2 real-gameplay-body test-only pixel consumer."""
from __future__ import annotations

import struct
import sys
import tempfile
import unittest
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
import c11e_e4a_challenge_real_body_pixel_review as real  # noqa: E402


def chunk(kind: bytes, payload: bytes) -> bytes:
    crc = zlib.crc32(kind + payload) & 0xFFFFFFFF
    return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", crc)


def png_bytes(width: int, height: int, channels: int = 3, pixels: bytes | None = None, filter_type: int = 0) -> bytes:
    if pixels is None:
        pixels = bytes(width * height * channels)
    stride = width * channels
    rows = []
    for y in range(height):
        rows.append(bytes([filter_type]) + pixels[y * stride:(y + 1) * stride])
    color_type = 2 if channels == 3 else 6
    ihdr = struct.pack(">IIBBBBB", width, height, 8, color_type, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(b"".join(rows))) + chunk(b"IEND", b""))


class RealBodyPixelReviewTests(unittest.TestCase):
    def test_01_authority_pins_are_frozen(self):
        self.assertEqual(real.MANIFEST_SHA256, "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953")
        self.assertEqual(real.CHALLENGE_SHA256, "6a674c02c2d8831a872691954f1cc40e2492193f9b136f60656730a7be686b71")
        self.assertEqual(real.APPROVAL_SHA256, "764629384896a255cf992da89fa427c19f60f9b2e623b81ad17d909674b466b5")
        self.assertEqual(real.LAYOUT_SHA256, "3a8e7bfc13a369acaf9d5abe9583f3e93e0990a3b1262b8a839e81ee873c6461")

    def test_02_c11c_source_and_normalized_review_timebases_are_distinct(self):
        self.assertEqual((real.C11C_SOURCE_FPS, real.C11C_SOURCE_FRAMES), (60, 900))
        self.assertEqual((real.DELIVERY_WIDTH, real.DELIVERY_HEIGHT, real.DELIVERY_FPS), (720, 1280, 30))
        self.assertEqual(real.EXPECTED_DELIVERY_FRAMES, 450)
        self.assertIn('os.environ.get("C11E_FFMPEG_EXECUTABLE")', (HERE / "c11e_e4a_challenge_real_body_pixel_review.py").read_text(encoding="utf-8"))

    def test_03_regions_are_exactly_scaled_from_d15(self):
        self.assertEqual(real.REGIONS["HEADER"], (0, 0, 720, 192))
        self.assertEqual(real.REGIONS["BODY"], (0, 192, 720, 1088))
        self.assertEqual(real.REGIONS["FOOTER"], (0, 1088, 720, 1280))

    def test_04_challenge_timeline_is_derived_from_source(self):
        timeline, fps, duration = real.source_timeline({"video": {
            "fps": 60, "hook_duration": 3, "game_duration": 7,
            "reveal_duration": 3, "cta_duration": 2,
        }})
        self.assertEqual(fps, 60)
        self.assertEqual(duration, 15.0)
        self.assertEqual([(x["phase"], x["start_source_frame"], x["end_source_frame_exclusive"]) for x in timeline],
                         [("HOOK", 0, 180), ("GAME", 180, 600), ("REVEAL", 600, 780), ("CTA", 780, 900)])

    def test_05_timeline_rejects_missing_phase(self):
        with self.assertRaises(real.RealBodyReviewError):
            real.source_timeline({"video": {"fps": 60, "hook_duration": 3, "game_duration": 7, "reveal_duration": 3}})

    def test_06_timeline_rejects_boolean_duration(self):
        with self.assertRaises(real.RealBodyReviewError):
            real.source_timeline({"video": {"fps": 60, "hook_duration": True, "game_duration": 7, "reveal_duration": 3, "cta_duration": 2}})

    def test_07_delivery_sample_boundaries_are_half_open(self):
        timeline, _, _ = real.source_timeline({"video": {
            "fps": 60, "hook_duration": 3, "game_duration": 7,
            "reveal_duration": 3, "cta_duration": 2,
        }})
        samples = real.sample_frames(timeline, 30)
        self.assertEqual([(x["sample"], x["delivery_frame"]) for x in samples], [
            ("hook_first", 0), ("hook_last", 89), ("game_first", 90),
            ("reveal_first", 300), ("cta_first", 390), ("cta_last", 449),
        ])

    def test_08_title_subtitle_are_drawn_only_during_hook(self):
        policy = {"fields": [
            {"field": "title", "region": "HEADER", "source_phase_windows": ["HOOK"]},
            {"field": "subtitle", "region": "HEADER", "source_phase_windows": ["HOOK"]},
        ]}
        editorial = {"title": "TITLE", "subtitle": "SUBTITLE"}
        self.assertEqual([x["field"] for x in real.approved_draw_fields(policy, editorial, "HOOK")], ["title", "subtitle"])
        self.assertEqual(real.approved_draw_fields(policy, editorial, "GAME"), [])

    def test_09_cta_is_drawn_only_during_cta(self):
        policy = {"fields": [{"field": "call_to_action", "region": "FOOTER", "source_phase_windows": ["CTA"]}]}
        editorial = {"call_to_action": "CTA"}
        self.assertEqual(real.approved_draw_fields(policy, editorial, "CTA"), [
            {"field": "call_to_action", "value": "CTA", "region": "FOOTER"}])
        self.assertEqual(real.approved_draw_fields(policy, editorial, "REVEAL"), [])

    def test_10_challenge_overlay_fields_are_never_drawn(self):
        policy = {"fields": [
            {"field": "player_name", "region": "CHALLENGE_OVERLAY", "source_phase_windows": ["HOOK", "GAME"]},
            {"field": "challenge_label", "region": "CHALLENGE_OVERLAY", "source_phase_windows": ["HOOK", "GAME"]},
        ]}
        editorial = {"player_name": "PLAYER", "challenge_label": "CHALLENGE"}
        self.assertEqual(real.approved_draw_fields(policy, editorial, "HOOK"), [])
        self.assertEqual(real.approved_draw_fields(policy, editorial, "GAME"), [])

    def test_11_empty_values_are_omitted(self):
        policy = {"fields": [{"field": "title", "region": "HEADER", "source_phase_windows": ["HOOK"]}]}
        self.assertEqual(real.approved_draw_fields(policy, {"title": "  "}, "HOOK"), [])

    def test_12_filter_contains_exact_delivery_frame_selector(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output = real.build_drawtext_filter(89, [{"field": "title", "region": "HEADER"}],
                {"title": root / "title.txt"}, Path("C:/Windows/Fonts/arial.ttf"))
        self.assertIn(r"select=eq(n\,89)", output)
        self.assertIn("drawtext=", output)
        self.assertIn("y=28", output)

    def test_13_filter_rejects_unapproved_region(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(real.RealBodyReviewError):
                real.build_drawtext_filter(0, [{"field": "player_name", "region": "CHALLENGE_OVERLAY"}],
                    {"player_name": Path(tmp) / "player.txt"}, Path("C:/Windows/Fonts/arial.ttf"))

    def test_14_filter_path_escapes_windows_drive_colon(self):
        escaped = real._filter_path(Path("C:/Temp/e4a/title.txt"))
        self.assertIn(r"C\:/Temp/e4a/title.txt", escaped)

    def test_15_png_decoder_reads_rgb_image(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "a.png"
            path.write_bytes(png_bytes(3, 2, 3, bytes(range(18))))
            result = real.decode_png(path)
        self.assertEqual((result.width, result.height, result.channels), (3, 2, 3))
        self.assertEqual(result.pixels, bytes(range(18)))

    def test_16_png_decoder_reads_rgba_image(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "a.png"
            pixels = bytes(range(24))
            path.write_bytes(png_bytes(3, 2, 4, pixels))
            result = real.decode_png(path)
        self.assertEqual(result.channels, 4)
        self.assertEqual(result.pixels, pixels)

    def test_17_png_decoder_rejects_non_png(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.png"
            path.write_bytes(b"not png")
            with self.assertRaises(real.RealBodyReviewError):
                real.decode_png(path)

    def test_18_png_decoder_rejects_interlace(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "interlaced.png"
            ihdr = struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 1)
            path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(b"\0\0\0\0")) + chunk(b"IEND", b""))
            with self.assertRaises(real.RealBodyReviewError):
                real.decode_png(path)

    def test_19_pixel_compare_accepts_change_inside_header_only(self):
        width, height, channels = 720, 1280, 3
        a = bytearray(width * height * channels)
        b = bytearray(a)
        pos = (50 * width + 50) * channels
        b[pos:pos + 3] = b"\xff\xff\xff"
        result = real.pixel_compare(real.Png(width, height, channels, bytes(a)),
                                    real.Png(width, height, channels, bytes(b)), real.REGIONS["HEADER"])
        self.assertEqual(result, {"changed_pixels": 1, "changed_inside_allowed_region": 1,
                                  "changed_outside_allowed_region": 0, "changed_body_pixels": 0})

    def test_20_pixel_compare_detects_body_pixel_change(self):
        width, height, channels = 720, 1280, 3
        a = bytearray(width * height * channels)
        b = bytearray(a)
        pos = (200 * width + 50) * channels
        b[pos:pos + 3] = b"\xff\xff\xff"
        result = real.pixel_compare(real.Png(width, height, channels, bytes(a)),
                                    real.Png(width, height, channels, bytes(b)), real.REGIONS["HEADER"])
        self.assertEqual(result["changed_body_pixels"], 1)
        self.assertEqual(result["changed_outside_allowed_region"], 1)

    def test_21_e1_intent_map_requires_a_b_c(self):
        with self.assertRaises(real.RealBodyReviewError):
            real.e1_intent_map([{"id": "A", "intent": {}}, {"id": "B", "intent": {}}])

    def test_22_runner_uses_existing_c11c_generator_outside_production_root(self):
        source = (HERE / "c11e_e4a_challenge_real_body_pixel_review.py").read_text(encoding="utf-8")
        self.assertIn('"artifacts" / "tests" / "c11e" / "e4a_real_body_pixel_review"', source)
        self.assertIn('"-OutputRoot", str(base_dir), "-NoSound"', source)
        self.assertIn('"-ChallengeId", "CHALLENGE_004", "-Seed", "314159"', source)

    def test_23_runner_never_invokes_d9_10_dispatch_or_production_d_renderer(self):
        source = (HERE / "c11e_e4a_challenge_real_body_pixel_review.py").read_text(encoding="utf-8")
        self.assertNotIn("ProductionDispatch.dispatch(", source)
        self.assertIn('"d9_10_dispatch_invoked": False', source)
        self.assertIn('"d_production_renderer_activated": False', source)

    def test_24_runner_records_current_c11c_source_hashes(self):
        source = (HERE / "c11e_e4a_challenge_real_body_pixel_review.py").read_text(encoding="utf-8")
        self.assertIn('"source_script_sha256": c11c_script_sha_before', source)
        self.assertIn('"producer_main_sha256": main_source_sha_before', source)
        self.assertIn('MAIN_SOURCE_SHA256 = "f0adc54de884d6d812396707cd6ced49038df0f52e4a9bc516a9ca5e6a0ddcd3"', source)
        self.assertIn('E1_SERVICE_SHA256 = "f0655d8d93df3b766b157d80a76a5bfc7b514d740815646f54c88ca788f602c0"', source)
        self.assertIn('D99_RESOLVER_SHA256 = "9ad2adbf54946f2225ae2ed36b88abfc5717387f2ff03bbed684aa8bd32d87d1"', source)
        self.assertIn('PREVIOUS_RUNNER_SHA256 = "939a12f369df9eaa0dbaf5b06b0635a0d4dc906e14fd7d5bdf9c12b3ec2b97a0"', source)

    def test_25_report_is_explicitly_test_only_and_retains_governance_locks(self):
        source = (HERE / "c11e_e4a_challenge_real_body_pixel_review.py").read_text(encoding="utf-8")
        self.assertIn('"status": "PASS_ISOLATED_REAL_C11C_BODY_PIXEL_PROOF_TEST_ONLY"', source)
        self.assertIn('"release_authority": "NONE"', source)
        self.assertIn('"d4_8": "BLOCKED"', source)


    def test_26_full_range_c11c_source_is_normalized_to_limited_yuv420p(self):
        command = real.build_normalize_command("ffmpeg", Path("source.mp4"), Path("review.mp4"),
            {"pix_fmt": "yuvj420p", "color_range": "pc"})
        vf = command[command.index("-vf") + 1]
        self.assertIn("fps=30", vf)
        self.assertIn("scale=in_range=full:out_range=tv", vf)
        self.assertIn("format=yuv420p", vf)
        self.assertIn("-an", command)
        self.assertIn("-color_range", command)
        self.assertEqual(command[command.index("-color_range") + 1], "tv")

    def test_27_limited_range_source_is_not_expanded_as_full_range(self):
        command = real.build_normalize_command("ffmpeg", Path("source.mp4"), Path("review.mp4"),
            {"pix_fmt": "yuv420p", "color_range": "tv"})
        vf = command[command.index("-vf") + 1]
        self.assertEqual(vf, "fps=30,format=yuv420p")
        self.assertNotIn("in_range=full", vf)

    def test_28_unknown_source_range_fails_closed(self):
        with self.assertRaises(real.RealBodyReviewError):
            real.build_normalize_command("ffmpeg", Path("source.mp4"), Path("review.mp4"),
                {"pix_fmt": "yuvj420p", "color_range": "tv"})

    def test_29_runner_normalizes_test_only_copy_and_preserves_c11c_source(self):
        source = (HERE / "c11e_e4a_challenge_real_body_pixel_review.py").read_text(encoding="utf-8")
        self.assertIn("normalize_c11c_source_video(ffmpeg, video_path, normalized_video_path", source)
        self.assertIn("ORIGINAL_C11C_MP4_PRESERVED", source)
        self.assertIn("probe_c11c_source_video(ffprobe, video_path", source)
        self.assertIn("c11c_source_video", source)
        self.assertIn('"frozen_manifest_sha256_after": frozen_manifest_after', source)



    def test_30_runner_supports_reusing_the_prior_test_run(self):
        source = (HERE / "c11e_e4a_challenge_real_body_pixel_review.py").read_text(encoding="utf-8")
        self.assertIn("--reuse-c11c-base-run", source)
        self.assertIn("REUSE_EXISTING_TEST_RENDER", source)
        self.assertIn("REUSED_EXISTING_C11C_TEST_RENDER_NO_GODOT_RERUN", source)
        self.assertIn("source_run.parent != approved_test_parent", source)

    def test_31_reused_mp4_manifest_identity_and_audio_off_are_required(self):
        source = (HERE / "c11e_e4a_challenge_real_body_pixel_review.py").read_text(encoding="utf-8")
        self.assertIn('c_manifest.get("challenge_id") != "CHALLENGE_004"', source)
        self.assertIn('c_manifest.get("seed") != 314159', source)
        self.assertIn('c_manifest.get("audio_present") is not False', source)
        self.assertIn("reused_source_mp4_sha256", source)


    def test_32_runner_separates_region_proof_from_visual_placement_acceptance(self):
        source = (HERE / "c11e_e4a_challenge_real_body_pixel_review.py").read_text(encoding="utf-8")
        self.assertIn('"visual_placement_approved": False', source)
        self.assertIn('"d1_5_safe_area_and_generic_typography": "UNKNOWN"', source)
        self.assertIn("existing_c11c_hook_content_overlap_observed_in_fixture_montage", source)
        self.assertIn("TEST_PIXEL_DRAW_REGION_ONLY_PLACEMENT_UNAPPROVED", source)

    def test_33_runner_records_manifest_vs_encoded_pixel_format_mismatch(self):
        source = (HERE / "c11e_e4a_challenge_real_body_pixel_review.py").read_text(encoding="utf-8")
        self.assertIn('"pixel_format_mismatch": c_manifest.get("pixel_format") != source_video.get("pix_fmt")', source)
        self.assertIn('"ffprobe_color_range": source_video.get("color_range")', source)

if __name__ == "__main__":
    unittest.main(verbosity=2)
