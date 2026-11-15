from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "c11d" / "d9" / "c11e_e4c_tracking_tier_batch.py"
spec = importlib.util.spec_from_file_location("c11e_e4c_tracking_tier_batch", MODULE_PATH)
assert spec and spec.loader
batch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(batch)


class TrackingTierBatchTests(unittest.TestCase):
    def setUp(self) -> None:
        self.base = {
            "schema": "C11-D-D9.9-UNIVERSAL-PRODUCER-REQUEST-V1",
            "schema_version": "1.0",
            "request_id": "ACCEPTED-TIER-1",
            "mode": "PRODUCTION",
            "selection": {"content_type": "visual_drills", "family_id": "tracking", "variant_id": "tier-1"},
            "seed": 12345,
            "music_seed": 840001,
            "variation_index": 0,
            "audio_enabled": True,
            "personalization_enabled": True,
            "delivery_profile_id": "REVIEW_720",
            "presentation_profile_id": "social_default_v1",
            "production_override": {
                "title": "SEGUIMIENTO VISUAL · NIVEL 1",
                "subtitle": "Sigue el objetivo con precisión",
                "call_to_action": "Mantén la mirada en el objetivo",
                "language": "es",
            },
            "provenance": {"request_origin": "CLI", "source_revision": "C11D-D9.10-PRODUCER-0.11.1"},
        }

    def test_plan_is_exactly_four_tracking_rows(self):
        rows = batch.batch_plan("E4C-TRACKING-T2-5-20261115T012400Z-a1b2c3d4")
        self.assertEqual([r["selector"] for r in rows], [
            "tracking/tier-2", "tracking/tier-3", "tracking/tier-4", "tracking/tier-5"
        ])
        self.assertEqual(len({r["request_id"] for r in rows}), 4)
        self.assertTrue(all(r["family_music_profile"] == "FLOWING_VECTOR" for r in rows))

    def test_plan_rejects_unscoped_or_malformed_batch_id(self):
        for batch_id in ("E4C-TRACKING-T1-5-x12345678", "bad-id", "E4C-TRACKING-T2-5-short"):
            with self.subTest(batch_id=batch_id), self.assertRaises(batch.BatchError):
                batch.batch_plan(batch_id)

    def test_request_is_selector_specific_and_seed_domains_are_preserved(self):
        request = batch.create_request(self.base, 4, "E4C-TRK-T4-a1b2c3d4")
        self.assertEqual(request["selection"], {
            "content_type": "visual_drills", "family_id": "tracking", "variant_id": "tier-4"
        })
        self.assertEqual(request["request_id"], "E4C-TRK-T4-a1b2c3d4")
        self.assertEqual(request["seed"], 12345)
        self.assertEqual(request["music_seed"], 840001)
        self.assertNotEqual(request["seed"], request["music_seed"])
        self.assertEqual(request["production_override"]["title"], "SEGUIMIENTO VISUAL · NIVEL 4")
        self.assertTrue(request["audio_enabled"])
        self.assertTrue(request["personalization_enabled"])
        self.assertEqual(request["provenance"]["request_origin"], "CLI")

    def test_request_does_not_mutate_base_template(self):
        before = self.base["selection"]["variant_id"]
        batch.create_request(self.base, 5, "E4C-TRK-T5-a1b2c3d4")
        self.assertEqual(self.base["selection"]["variant_id"], before)
        self.assertEqual(self.base["production_override"]["title"], "SEGUIMIENTO VISUAL · NIVEL 1")

    def test_expected_post_r63a_consumer_and_test_are_pinned(self):
        self.assertEqual(batch.SOURCE_PINS[batch.CONSUMER_REL], "d5cd8e24c0cfdd83ec035b006c76468ed637d6babf5f0a9fcca8a93817ba1aa8")
        self.assertEqual(batch.SOURCE_PINS[batch.CONSUMER_TEST_REL], "5da9ec59d0f6d716861e9a4cbcfc36db5e61f992c966a2294bb23ef2c344bafb")
        self.assertEqual(batch.SOURCE_PINS[batch.EXECUTOR_REL], "b7cbf7bd97f76f4c2e339840fc694d3f5b0e50186ba2456e45ff00e585751abe")
        self.assertEqual(batch.SOURCE_PINS["release/C11C_FREEZE_PACKAGE_MANIFEST.json"], batch.FROZEN_MANIFEST_SHA256)
        self.assertEqual(batch.SOURCE_PINS[batch.STYLE_GUIDE_PATH], batch.STYLE_GUIDE_SHA256)
        self.assertEqual(batch.STYLE_GUIDE_V27_PATH, "docs/current/e/C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261115_V27.md")
        self.assertEqual(len(batch.STYLE_GUIDE_V27_SHA256), 64)

    def _final_fixture(self):
        streams = [
            {"codec_type": "video", "codec_name": "h264", "profile": "High", "width": 720,
             "height": 1280, "pix_fmt": "yuv420p", "color_range": "tv", "avg_frame_rate": "30/1",
             "nb_read_frames": "810"},
            {"codec_type": "audio", "codec_name": "aac", "profile": "LC", "sample_rate": "48000",
             "channels": 2, "channel_layout": "stereo"},
        ]
        return {"duration_seconds": 27.0, "av_start_delta_seconds": 0.0,
                "ffprobe": {"streams": streams}}

    def test_ffprobe_contract_accepts_expected_720p_aac_profile(self):
        batch.verify_ffprobe_contract(self._final_fixture(), "TRACKING_TIER_2_A")

    def test_ffprobe_contract_rejects_wrong_pixel_format(self):
        final = self._final_fixture()
        final["ffprobe"]["streams"][0]["pix_fmt"] = "yuvj420p"
        with self.assertRaises(batch.BatchError):
            batch.verify_ffprobe_contract(final, "TRACKING_TIER_2_A")

    def test_ffprobe_contract_rejects_av_drift(self):
        final = self._final_fixture()
        final["av_start_delta_seconds"] = 0.01
        with self.assertRaises(batch.BatchError):
            batch.verify_ffprobe_contract(final, "TRACKING_TIER_2_A")

    def test_full_qualification_receipt_contract_is_bound_to_its_selector(self):
        import hashlib
        import json
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            request_id = "E4C-TRK-T2-a1b2c3d4"
            output_root = root / "artifacts" / "production" / "c11e" / request_id
            output_root.mkdir(parents=True)
            evidence_root = root / "artifacts" / "tests" / "c11e" / "batch"
            evidence_root.mkdir(parents=True)
            def put(name: str, body: bytes) -> tuple[str, str]:
                path = output_root / name
                path.write_bytes(body)
                return str(path), hashlib.sha256(body).hexdigest()
            wav_a, wav_a_sha = put("music_A.wav", b"wav-a")
            wav_b, wav_b_sha = put("music_B.wav", b"wav-a")
            wav_c, wav_c_sha = put("music_C.wav", b"wav-c")
            mp4_a, mp4_a_sha = put("final_A.mp4", b"video-a")
            mp4_c, mp4_c_sha = put("final_C.mp4", b"video-c")
            final = self._final_fixture()
            receipt = {
                "status": "PASS_E4C_DRILL_SINGLE_SELECTOR_A_V_QUALIFICATION",
                "request_id": request_id, "request_origin": "CLI", "family": "tracking", "tier": 2,
                "gameplay_seed": 12345, "music_seed_a": 840001, "music_seed_b": 840001,
                "family_music_profile": "FLOWING_VECTOR", "family_adapter_preparation_status": "NOT_CONNECTED_E1",
                "release_authority": "NONE", "production_dispatch": False, "production_release": False,
                "c11c_frozen_manifest_unchanged": True,
                "c11c_manifest_sha256": batch.FROZEN_MANIFEST_SHA256, "c11c_source_mutation": False,
                "renderer_invoked": True, "d_postcomposition": True, "ffmpeg_decode_encode_mux": True,
                "audio_generated": True, "source_pins_pre_post_equal": True, "source_pin_count": 91,
                "family_adapter_execution": {"shared_entrypoint": "c11e_e4c_drill_execution.py"},
                "e1_gui_cli_parity": {"status": "PASS_E1_SHARED_GUI_CLI_INTENT_PARITY", "semantic_identity_equal": True},
                "e1_validation": {"status": "PASS_E1_PREPARATION_ONLY"},
                "native_timeline": {"fps": 30, "total_frames": 810, "duration_seconds": 27.0},
                "d_composition": {"frames_composed": 810, "frames_expected": 810,
                                  "phase_counts": {"PRE_ROLL": 90, "GAME": 630, "END_CTA": 90}},
                "d_editorial_visible_fields": ["title", "subtitle", "call_to_action"],
                "family_music": {"route": "C11_C_FAMILY_MUSIC_V4", "profile_id": "FLOWING_VECTOR",
                                 "same_seed_ab_identical": True, "changed_seed_c_distinct": True,
                                 "A": {"path": wav_a, "sha256": wav_a_sha},
                                 "B": {"path": wav_b, "sha256": wav_b_sha},
                                 "C": {"path": wav_c, "sha256": wav_c_sha}},
                "bitstream_isolation": {"video_stream_identical": True, "audio_stream_changed": True,
                                         "video_stream_sha256_A": "a"*64, "video_stream_sha256_C": "a"*64,
                                         "audio_stream_sha256_A": "b"*64, "audio_stream_sha256_C": "c"*64},
                "final_A": {"path": mp4_a, "sha256": mp4_a_sha, **final},
                "final_C_changed_music": {"path": mp4_c, "sha256": mp4_c_sha, **final},
            }
            receipt_path = output_root / "E4C_DRILL_AV_QUALIFICATION_RECEIPT.json"
            receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
            summary_path = evidence_root / "summary.json"
            summary_path.write_text(json.dumps({"status": receipt["status"], "request_id": request_id,
                "selector": "tracking/tier-2", "family_music_profile": "FLOWING_VECTOR",
                "receipt": str(receipt_path)}), encoding="utf-8")
            request = {"request_id": request_id}
            result = batch.validate_qualification(root, request, summary_path, 2)
            self.assertEqual(result["selector"], "tracking/tier-2")
            self.assertEqual(result["review_status"], "PENDING_OPERATOR_VISUAL_AUDIO_REVIEW")

    def test_missing_source_pin_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(batch.BatchError):
                batch.verify_pins(Path(directory))


if __name__ == "__main__":
    unittest.main(verbosity=2)
