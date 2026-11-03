from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from c11e_e3_audio_pipeline import (
    C11EE3AudioPilotError,
    PILOT_GAMEPLAY_SEED,
    PILOT_MUSIC_SEED,
    R4_EXPECTED_RECEIPT_SHA256,
    R4_EXPECTED_VIDEO_SHA256,
    _verify_r4_source,
    _verify_source_pins,
    run_e3_audio_pilot,
)
from c11e_production_service import prepare_c11e_production_intent

ROOT = Path(__file__).resolve().parents[2]
PRODUCER_ROOT = Path(__file__).resolve().parent
FIXTURE_ROOT = ROOT / "tools" / "c11e" / "e3" / "fixtures"
VIDEO = FIXTURE_ROOT / "CHALLENGE_001_R4_A_REVIEW_720.mp4"
R4_RECEIPT = FIXTURE_ROOT / "C11E_E2_R4_RENDER_RECEIPT.json"
R4_SHA = FIXTURE_ROOT / "C11E_E2_R4_RENDER_RECEIPT.json.sha256"


def make_request(*, audio_enabled: bool = True, seed: int = PILOT_GAMEPLAY_SEED, music_seed: int = PILOT_MUSIC_SEED) -> dict:
    return {
        "schema": "C11-D-D9.9-UNIVERSAL-PRODUCER-REQUEST-V1",
        "schema_version": "1.0",
        "request_id": "C11E-E3-AUDIO-UNIT-TEST-001",
        "mode": "REVIEW",
        "selection": {
            "content_type": "challenges",
            "family_id": "key",
            "variant_id": "CHALLENGE_001",
        },
        "seed": seed,
        "music_seed": music_seed,
        "delivery_profile_id": "REVIEW_720",
        "presentation_profile_id": "social_default_v1",
        "variation_index": 0,
        "audio_enabled": audio_enabled,
        "personalization_enabled": True,
        "editorial_profile": {},
        "production_override": {"title": "C11-E E3 audio integration test"},
        "provenance": {"source_revision": "C11E-E3-AUDIO-TEST", "request_origin": "TEST"},
    }


def prepare_intent(*, audio_enabled: bool = True, seed: int = PILOT_GAMEPLAY_SEED, music_seed: int = PILOT_MUSIC_SEED) -> dict:
    return prepare_c11e_production_intent(make_request(audio_enabled=audio_enabled, seed=seed, music_seed=music_seed), ROOT, request_origin="TEST")["intent"]


class C11EE3AudioPipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not shutil.which("ffmpeg") and not shutil.which("ffmpeg.exe"):
            raise RuntimeError("FFmpeg is required for the C11-E E3 audiovisual test suite")
        if not shutil.which("ffprobe") and not shutil.which("ffprobe.exe"):
            raise RuntimeError("FFprobe is required for the C11-E E3 audiovisual test suite")

    def test_e3_2_engine_spec_and_profile_pins_are_current(self):
        report = _verify_source_pins(ROOT)
        self.assertEqual(report["contract"]["engine"]["engine_id"], "c11d_music_engine_v5")
        self.assertEqual(report["contract"]["style_profile"]["canonical_id"], "challenge_8bit_v1")
        self.assertEqual(report["sources"]["tools/c11d/d3/c11d_music_engine_v5.py"]["sha256"], report["contract"]["engine"]["sha256"])

    def test_r4_video_fixture_receipt_hash_and_duration_are_verified(self):
        import tempfile
        from c11e_e3_audio_pipeline import _resolve_tool

        with tempfile.TemporaryDirectory(prefix="c11e-e3-source-probe-") as temp:
            evidence = Path(temp)
            source = _verify_r4_source(VIDEO, R4_RECEIPT, R4_SHA, _resolve_tool("ffprobe"), evidence)
        self.assertEqual(source["sha256"], R4_EXPECTED_VIDEO_SHA256)
        self.assertEqual(source["receipt_sha256"], R4_EXPECTED_RECEIPT_SHA256)
        self.assertAlmostEqual(source["derived_duration_seconds"], 9.0, places=6)
        self.assertEqual(source["source_frames"], 270)
        self.assertEqual(source["audio_stream_count"], 0)

    def test_audio_disabled_intent_is_rejected_before_engine_load_or_mux(self):
        intent = prepare_intent(audio_enabled=False)
        with tempfile.TemporaryDirectory(prefix="c11e-e3-disabled-") as temp:
            output = Path(temp) / "must-not-run"
            with mock.patch("c11e_e3_audio_pipeline._load_engine", side_effect=AssertionError("engine must not load")):
                with self.assertRaisesRegex(C11EE3AudioPilotError, "audio disabled"):
                    run_e3_audio_pilot(
                        project_root=ROOT,
                        e1_intent_path=self._write_intent(temp, intent),
                        source_video_path=VIDEO,
                        source_receipt_path=R4_RECEIPT,
                        source_receipt_sha_path=R4_SHA,
                        output_root=output,
                    )
            self.assertTrue((output / "C11E_E3_AUDIO_PILOT_RECEIPT.json").is_file())
            failure = json.loads((output / "C11E_E3_AUDIO_PILOT_RECEIPT.json").read_text(encoding="utf-8"))
            self.assertEqual(failure["status"], "FAIL_E3_AUDIO_PILOT_TEST_ONLY")
            self.assertFalse(failure["ffmpeg_mux_invoked"])
            self.assertFalse(failure["gameplay_renderer_invoked"])

    @staticmethod
    def _write_intent(directory: str, intent: dict) -> Path:
        path = Path(directory) / "intent.json"
        path.write_text(json.dumps(intent, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return path

    def test_gameplay_seed_must_match_r4_source_identity(self):
        intent = prepare_intent(seed=PILOT_GAMEPLAY_SEED + 1)
        with tempfile.TemporaryDirectory(prefix="c11e-e3-seed-mismatch-") as temp:
            with self.assertRaisesRegex(C11EE3AudioPilotError, "R4 video provenance"):
                run_e3_audio_pilot(
                    project_root=ROOT,
                    e1_intent_path=self._write_intent(temp, intent),
                    source_video_path=VIDEO,
                    source_receipt_path=R4_RECEIPT,
                    source_receipt_sha_path=R4_SHA,
                    output_root=Path(temp) / "run",
                )

    def test_full_challenge_audio_mux_repeatability_and_seed_isolation(self):
        intent = prepare_intent()
        with tempfile.TemporaryDirectory(prefix="c11e-e3-full-pilot-") as temp:
            intent_path = self._write_intent(temp, intent)
            output = Path(temp) / "e3-output"
            receipt = run_e3_audio_pilot(
                project_root=ROOT,
                e1_intent_path=intent_path,
                source_video_path=VIDEO,
                source_receipt_path=R4_RECEIPT,
                source_receipt_sha_path=R4_SHA,
                output_root=output,
            )
            self.assertEqual(receipt["status"], "PASS_E3_CHALLENGE_AUDIO_PILOT_TEST_ONLY")
            self.assertTrue(receipt["music"]["repeat_raw_wav_identical"])
            self.assertTrue(receipt["music"]["changed_music_seed_changes_raw_wav"])
            self.assertTrue(receipt["music"]["repeat_final_master_identical"])
            self.assertTrue(receipt["music"]["changed_music_seed_changes_final_master"])
            self.assertTrue(receipt["mux"]["repeat_decoded_audio_identical"])
            self.assertTrue(receipt["mux"]["changed_music_seed_changes_decoded_audio"])
            self.assertTrue(receipt["mux"]["video_bitstream_unchanged_for_all_music_seeds"])
            self.assertEqual(receipt["source_video"]["sha256"], R4_EXPECTED_VIDEO_SHA256)
            self.assertEqual(receipt["e1_intent"]["gameplay_seed"], PILOT_GAMEPLAY_SEED)
            self.assertEqual(receipt["e1_intent"]["music_seed"], PILOT_MUSIC_SEED)
            self.assertEqual(receipt["release_authority"], "NONE")
            self.assertFalse(receipt["gameplay_renderer_invoked"])
            self.assertTrue((output / "C11E_E3_AUDIO_PILOT_RECEIPT.json").is_file())
            self.assertTrue((output / "CHALLENGE_001_R4_AUDIO_A.mp4").is_file())
            self.assertTrue((output / "CHALLENGE_001_R4_AUDIO_C_CHANGED_MUSIC_SEED.mp4").is_file())


if __name__ == "__main__":
    unittest.main(verbosity=2)
