from __future__ import annotations

import copy
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import wave
from pathlib import Path
from unittest import mock

import c11e_e3_audio_pipeline as pipeline
from c11e_e3_audio_pipeline import (
    C11EE3AudioPilotError,
    _audio_metrics,
    _validate_mux_probe,
    _verify_r4_source,
    _verify_source_pins,
    run_e3_audio_pilot,
)
from c11e_production_service import (
    C11EProductionServiceError,
    prepare_c11e_production_intent,
    sha256 as intent_sha256,
    validate_c11e_production_intent,
)
from test_c11e_e3_audio_pipeline import make_request

ROOT = Path(__file__).resolve().parents[2]
FIXTURE_ROOT = ROOT / "tools" / "c11e" / "e3" / "fixtures"
VIDEO = FIXTURE_ROOT / "CHALLENGE_001_R4_A_REVIEW_720.mp4"
R4_RECEIPT = FIXTURE_ROOT / "C11E_E2_R4_RENDER_RECEIPT.json"
R4_SHA = FIXTURE_ROOT / "C11E_E2_R4_RENDER_RECEIPT.json.sha256"


def valid_probe() -> dict:
    return {
        "streams": [
            {
                "codec_type": "video", "codec_name": "h264", "profile": "High",
                "width": 720, "height": 1280, "avg_frame_rate": "30/1",
                "nb_read_frames": "270", "start_time": "0.000000", "duration": "9.000000",
            },
            {
                "codec_type": "audio", "codec_name": "aac", "sample_rate": "48000",
                "channels": 2, "channel_layout": "stereo", "start_time": "0.000000",
                "duration": "9.000000",
            },
        ],
        "format": {"duration": "9.000000"},
    }


def reseal_intent(intent: dict) -> dict:
    result = copy.deepcopy(intent)
    result.pop("intent_sha256", None)
    result["intent_sha256"] = intent_sha256(result)
    return result


class C11EE3NegativeControlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
            raise RuntimeError("FFmpeg and FFprobe are required for E3 negative controls")
        if not R4_RECEIPT.is_file() or not R4_SHA.is_file():
            raise RuntimeError("Pinned R4 E2 receipt fixtures are required")

    def test_valid_final_mux_probe_passes_with_stream_and_timing_receipt(self):
        result = _validate_mux_probe(valid_probe(), label="A", expected_video_duration=9.0)
        self.assertEqual(result["video_stream_count"], 1)
        self.assertEqual(result["audio_stream_count"], 1)
        self.assertAlmostEqual(result["av_end_drift_seconds"], 0.0)
        self.assertEqual(result["audio"]["channel_layout"], "stereo")

    def test_missing_audio_stream_is_rejected(self):
        probe = valid_probe()
        probe["streams"] = probe["streams"][:1]
        with self.assertRaisesRegex(C11EE3AudioPilotError, "exactly one video and one audio"):
            _validate_mux_probe(probe, label="missing-audio", expected_video_duration=9.0)
        probe = valid_probe()
        probe["streams"] = probe["streams"][1:]
        with self.assertRaisesRegex(C11EE3AudioPilotError, "exactly one video and one audio"):
            _validate_mux_probe(probe, label="missing-video", expected_video_duration=9.0)

    def test_multiple_audio_streams_are_rejected(self):
        probe = valid_probe()
        probe["streams"].append(copy.deepcopy(probe["streams"][1]))
        with self.assertRaisesRegex(C11EE3AudioPilotError, "exactly one video and one audio"):
            _validate_mux_probe(probe, label="multiple-audio", expected_video_duration=9.0)

    def test_multiple_video_streams_are_rejected(self):
        probe = valid_probe()
        probe["streams"].append(copy.deepcopy(probe["streams"][0]))
        with self.assertRaisesRegex(C11EE3AudioPilotError, "exactly one video and one audio"):
            _validate_mux_probe(probe, label="multiple-video", expected_video_duration=9.0)

    def test_corrupt_or_zero_or_negative_durations_are_rejected(self):
        for value in ("0", "-1"):
            with self.subTest(duration=value):
                probe = valid_probe()
                probe["streams"][1]["duration"] = value
                with self.assertRaisesRegex(C11EE3AudioPilotError, "zero/negative media duration"):
                    _validate_mux_probe(probe, label="duration", expected_video_duration=9.0)
        probe = valid_probe()
        probe["streams"][0]["duration"] = "not-a-duration"
        with self.assertRaisesRegex(C11EE3AudioPilotError, "missing/invalid stream timing"):
            _validate_mux_probe(probe, label="bad-duration", expected_video_duration=9.0)

    def test_wrong_video_or_audio_codec_is_rejected(self):
        probe = valid_probe()
        probe["streams"][0]["codec_name"] = "hevc"
        with self.assertRaisesRegex(C11EE3AudioPilotError, "video codec/frame-count"):
            _validate_mux_probe(probe, label="wrong-video-codec", expected_video_duration=9.0)
        probe = valid_probe()
        probe["streams"][0]["nb_read_frames"] = "269"
        with self.assertRaisesRegex(C11EE3AudioPilotError, "video codec/frame-count"):
            _validate_mux_probe(probe, label="wrong-video-frame-count", expected_video_duration=9.0)
        probe = valid_probe()
        probe["streams"][0]["width"] = 540
        with self.assertRaisesRegex(C11EE3AudioPilotError, "video dimensions changed"):
            _validate_mux_probe(probe, label="wrong-video-dimensions", expected_video_duration=9.0)
        probe = valid_probe()
        probe["streams"][0]["avg_frame_rate"] = "25/1"
        with self.assertRaisesRegex(C11EE3AudioPilotError, "video frame rate changed"):
            _validate_mux_probe(probe, label="wrong-video-fps", expected_video_duration=9.0)
        probe = valid_probe()
        probe["streams"][1]["codec_name"] = "mp3"
        with self.assertRaisesRegex(C11EE3AudioPilotError, "audio codec is not AAC"):
            _validate_mux_probe(probe, label="wrong-audio-codec", expected_video_duration=9.0)

    def test_wrong_audio_sample_rate_or_channel_layout_is_rejected(self):
        probe = valid_probe()
        probe["streams"][1]["sample_rate"] = "44100"
        with self.assertRaisesRegex(C11EE3AudioPilotError, "sample rate is not 48000"):
            _validate_mux_probe(probe, label="wrong-rate", expected_video_duration=9.0)
        probe = valid_probe()
        probe["streams"][1]["channels"] = 1
        probe["streams"][1]["channel_layout"] = "mono"
        with self.assertRaisesRegex(C11EE3AudioPilotError, "channel layout is not stereo"):
            _validate_mux_probe(probe, label="wrong-layout", expected_video_duration=9.0)

    def test_truncated_audio_is_rejected(self):
        probe = valid_probe()
        probe["streams"][1]["duration"] = "8.500000"
        with self.assertRaisesRegex(C11EE3AudioPilotError, "end-time drift .* exceeds 0.15s"):
            _validate_mux_probe(probe, label="truncated", expected_video_duration=9.0)
        probe = valid_probe()
        probe["streams"][0]["duration"] = "8.700000"
        probe["streams"][1]["duration"] = "8.700000"
        with self.assertRaisesRegex(C11EE3AudioPilotError, "video duration does not match the pinned source duration"):
            _validate_mux_probe(probe, label="truncated-video", expected_video_duration=9.0)

    def test_excessive_start_time_drift_is_rejected(self):
        probe = valid_probe()
        probe["streams"][1]["start_time"] = "0.200000"
        with self.assertRaisesRegex(C11EE3AudioPilotError, "start-time drift .* exceeds 0.15s"):
            _validate_mux_probe(probe, label="start-drift", expected_video_duration=9.0)

    def test_excessive_end_time_drift_is_rejected(self):
        probe = valid_probe()
        probe["streams"][1]["duration"] = "8.700000"
        with self.assertRaisesRegex(C11EE3AudioPilotError, "end-time drift .* exceeds 0.15s"):
            _validate_mux_probe(probe, label="end-drift", expected_video_duration=9.0)

    def test_invalid_gameplay_and_music_seeds_are_rejected_by_e1(self):
        prepared = prepare_c11e_production_intent(make_request(), ROOT, request_origin="TEST")["intent"]
        for domain in ("gameplay", "music"):
            with self.subTest(domain=domain):
                invalid = copy.deepcopy(prepared)
                invalid["seed_domains"][domain]["value"] = 0
                invalid = reseal_intent(invalid)
                with self.assertRaisesRegex(C11EProductionServiceError, f"Invalid {domain} seed value"):
                    validate_c11e_production_intent(invalid, ROOT)

    def test_missing_music_source_profile_is_rejected_without_mutating_repo(self):
        with tempfile.TemporaryDirectory(prefix="c11e-e3-missing-profile-") as temp:
            temp_root = Path(temp)
            contract_rel = Path("pins/contract.json")
            engine_rel = Path("pins/engine.py")
            spec_rel = Path("pins/spec.json")
            profile_rel = Path("pins/profile.json")
            (temp_root / contract_rel).parent.mkdir(parents=True, exist_ok=True)
            (temp_root / engine_rel).write_bytes(b"engine")
            (temp_root / spec_rel).write_bytes(b"spec")
            contract = {
                "schema": "C11E-E3.2-D3-V5-E1-MUSIC-CONTRACT",
                "schema_version": "1.0",
                "engine": {"sha256": hashlib.sha256(b"engine").hexdigest(), "spec_sha256": hashlib.sha256(b"spec").hexdigest()},
                "style_profile": {"sha256": hashlib.sha256(b"profile").hexdigest()},
            }
            (temp_root / contract_rel).write_text(json.dumps(contract), encoding="utf-8")
            with (
                mock.patch.object(pipeline, "CONTRACT_REL", contract_rel),
                mock.patch.object(pipeline, "ENGINE_REL", engine_rel),
                mock.patch.object(pipeline, "SPEC_REL", spec_rel),
                mock.patch.object(pipeline, "PROFILE_REL", profile_rel),
            ):
                with self.assertRaisesRegex(C11EE3AudioPilotError, "Pinned source missing: pins/profile.json"):
                    _verify_source_pins(temp_root)

    def test_invalid_challenge_style_profile_is_rejected_by_d3_v5(self):
        engine = pipeline._load_engine(ROOT / pipeline.ENGINE_REL)
        spec = json.loads((ROOT / pipeline.SPEC_REL).read_text(encoding="utf-8"))
        profile = json.loads((ROOT / pipeline.PROFILE_REL).read_text(encoding="utf-8"))
        profile["profile_id"] = "not_a_challenge_profile"
        request = {
            "music_seed": 840001,
            "style_profile_id": "not_a_challenge_profile",
            "style_profile_version": "1.0",
            "tempo_bpm": 104,
            "duration_seconds": 1.0,
            "variation_index": 0,
        }
        with tempfile.TemporaryDirectory(prefix="c11e-e3-invalid-profile-") as temp:
            with self.assertRaisesRegex(ValueError, "targets challenge_8bit_v1 only"):
                engine.render(request, spec, profile, Path(temp) / "must-not-exist.wav")
            self.assertFalse((Path(temp) / "must-not-exist.wav").exists())

    def test_missing_or_invalid_r4_source_is_rejected(self):
        with tempfile.TemporaryDirectory(prefix="c11e-e3-missing-source-") as temp:
            missing = Path(temp) / "missing.mp4"
            with self.assertRaisesRegex(C11EE3AudioPilotError, "Required R4 fixture is missing"):
                _verify_r4_source(missing, R4_RECEIPT, R4_SHA, "ffprobe", Path(temp) / "evidence")

    def test_silent_audio_is_rejected_by_real_ffmpeg_volume_analysis(self):
        with tempfile.TemporaryDirectory(prefix="c11e-e3-silent-audio-") as temp:
            root = Path(temp)
            silent = root / "silent.wav"
            with wave.open(str(silent), "wb") as writer:
                writer.setnchannels(2)
                writer.setsampwidth(2)
                writer.setframerate(48000)
                writer.writeframes(b"\x00\x00\x00\x00" * 48000)
            with self.assertRaisesRegex(C11EE3AudioPilotError, "silent or FFmpeg volume metrics are unavailable"):
                _audio_metrics(silent, shutil.which("ffmpeg") or "ffmpeg", shutil.which("ffprobe") or "ffprobe", root, "silent")

    def test_corrupt_mp4_is_rejected_by_ffprobe(self):
        with tempfile.TemporaryDirectory(prefix="c11e-e3-corrupt-mp4-") as temp:
            root = Path(temp)
            corrupt = root / "corrupt.mp4"
            corrupt.write_bytes(b"not-an-mp4-container")
            with self.assertRaises(C11EE3AudioPilotError):
                _audio_metrics(corrupt, shutil.which("ffmpeg") or "ffmpeg", shutil.which("ffprobe") or "ffprobe", root, "corrupt")

    def test_ffprobe_process_failure_is_recorded_and_fails_closed(self):
        with tempfile.TemporaryDirectory(prefix="c11e-e3-ffprobe-failure-") as temp:
            root = Path(temp)
            failed = subprocess.CompletedProcess(args=["ffprobe"], returncode=1, stdout="", stderr="simulated ffprobe failure")
            with mock.patch.object(pipeline.subprocess, "run", return_value=failed):
                with self.assertRaisesRegex(C11EE3AudioPilotError, "failed with exit code 1"):
                    pipeline._run(["ffprobe", "bad.mp4"], stage="negative_ffprobe", evidence_root=root)
            self.assertEqual((root / "negative_ffprobe.exitcode.txt").read_text(encoding="ascii").strip(), "1")
            self.assertIn("simulated ffprobe failure", (root / "negative_ffprobe.stderr.log").read_text(encoding="utf-8"))

    @unittest.skipUnless(
        VIDEO.is_file(),
        "R4 source MP4 is omitted from the read-only context snapshot; the Windows checkout must contain the V1.3 fixture",
    )
    def test_e3_worker_runs_as_standalone_cli_separate_process(self):
        request = make_request()
        request["request_id"] = "C11E-E3-V15-CLI-SUBPROCESS"
        intent = prepare_c11e_production_intent(request, ROOT, request_origin="CLI")["intent"]
        with tempfile.TemporaryDirectory(prefix="c11e-e3-cli-worker-") as temp:
            temp_root = Path(temp)
            intent_path = temp_root / "cli-intent.json"
            intent_path.write_text(json.dumps(intent, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            output_root = temp_root / "cli-output"
            worker = Path(__file__).resolve().parent / "c11e_e3_audio_pilot.py"
            run = subprocess.run(
                [
                    sys.executable, str(worker),
                    "--root", str(ROOT),
                    "--intent", str(intent_path),
                    "--source-video", str(VIDEO),
                    "--source-receipt", str(R4_RECEIPT),
                    "--source-receipt-sha256", str(R4_SHA),
                    "--output-root", str(output_root),
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )
            self.assertEqual(run.returncode, 0, msg=f"stdout={run.stdout}\nstderr={run.stderr}")
            self.assertIn("C11E_E3_AUDIO_PILOT=PASS", run.stdout)
            receipt_path = output_root / "C11E_E3_AUDIO_PILOT_RECEIPT.json"
            self.assertTrue(receipt_path.is_file())
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertEqual(receipt["status"], "PASS_E3_CHALLENGE_AUDIO_PILOT_TEST_ONLY")
            self.assertFalse(receipt["operator_gui_invoked"])
            self.assertEqual(receipt["execution_origin"], "AUTOMATED_TEST_RUNNER")
            self.assertFalse(receipt["gameplay_renderer_invoked"])
            self.assertFalse(receipt["gameplay_rerendered"])

    def test_existing_output_root_is_never_overwritten(self):
        with tempfile.TemporaryDirectory(prefix="c11e-e3-output-collision-") as temp:
            output = Path(temp) / "already-used"
            output.mkdir()
            sentinel = output / "keep.txt"
            sentinel.write_text("immutable evidence", encoding="utf-8")
            with self.assertRaisesRegex(C11EE3AudioPilotError, "overwrite is forbidden"):
                run_e3_audio_pilot(
                    project_root=ROOT,
                    e1_intent_path=Path(temp) / "not-needed-intent.json",
                    source_video_path=VIDEO,
                    source_receipt_path=R4_RECEIPT,
                    source_receipt_sha_path=R4_SHA,
                    output_root=output,
                )
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "immutable evidence")


if __name__ == "__main__":
    unittest.main(verbosity=2)
