from __future__ import annotations
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).with_name("RECOVER_C11E_E4C_V2_EXISTING_OUTPUT_REVIEW_V1.py")
SPEC = importlib.util.spec_from_file_location("recovery", SCRIPT)
recovery = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(recovery)

class ExistingOutputRecoveryTests(unittest.TestCase):
    def test_recovery_is_bound_to_one_existing_run(self):
        self.assertEqual(recovery.RUN_ID, "E4C-CLI-COMPOSITION-V2-20261114T003422Z-a4d913f9")

    def test_expected_final_inventory_is_exactly_three_outputs(self):
        self.assertEqual(set(recovery.EXPECTED_FINALS), {"A", "B", "C"})
        self.assertEqual(recovery.EXPECTED_FINALS["A"][1], recovery.EXPECTED_FINALS["B"][1])
        self.assertNotEqual(recovery.EXPECTED_FINALS["A"][1], recovery.EXPECTED_FINALS["C"][1])

    def test_expected_composition_timebase(self):
        self.assertEqual(recovery.TOTAL_FRAMES, 810)
        self.assertEqual([i for i, _ in recovery.SAMPLES], [0, 89, 90, 405, 719, 720, 809])

    def test_expected_aac_hashes_match_ab_and_change_c(self):
        self.assertEqual(recovery.EXPECTED_AAC_STREAM_SHA256["A"], recovery.EXPECTED_AAC_STREAM_SHA256["B"])
        self.assertNotEqual(recovery.EXPECTED_AAC_STREAM_SHA256["A"], recovery.EXPECTED_AAC_STREAM_SHA256["C"])

    def test_main_requalifier_is_patched_to_fps_mode(self):
        runner = Path(__file__).with_name("REQUALIFY.py")
        source = runner.read_text(encoding="utf-8-sig")
        self.assertIn('"-fps_mode", "passthrough"', source)
        self.assertNotIn('"-vsync"', source)

    def test_extract_command_uses_modern_fps_mode_not_removed_vsync(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); review = root / "review"; qual = root / "qualification"
            review.mkdir(); qual.mkdir()
            commands = []
            def fake_run(command, **kwargs):
                commands.append(command)
                Path(command[-1]).write_bytes(b"png")
                return type("R", (), {"returncode": 0, "stderr": "", "stdout": ""})()
            with patch.object(recovery.subprocess, "run", side_effect=fake_run):
                rows = recovery.extract_review_frames(Path("ffmpeg.exe"), Path("final.mp4"), review, qual)
            self.assertEqual(len(rows), 7)
            self.assertTrue(all("-fps_mode" in c and "passthrough" in c for c in commands))
            self.assertTrue(all("-vsync" not in c for c in commands))

    def test_extract_frame_logs_exact_command_and_result(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); review = root / "review"; qual = root / "qualification"
            review.mkdir(); qual.mkdir()
            def fake_run(command, **kwargs):
                Path(command[-1]).write_bytes(b"png-data")
                return type("R", (), {"returncode": 0, "stderr": "", "stdout": ""})()
            with patch.object(recovery.subprocess, "run", side_effect=fake_run):
                rows = recovery.extract_review_frames(Path("ffmpeg.exe"), Path("final.mp4"), review, qual)
            log = json.loads((qual / "review_frame_000_PRE_ROLL_FIRST_ffmpeg.json").read_text())
            self.assertEqual(log["returncode"], 0)
            self.assertEqual(log["fps_mode"], "passthrough")
            self.assertTrue(rows[0]["sha256"])

    def test_extract_failure_is_fail_closed_and_logged(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); review = root / "review"; qual = root / "qualification"
            review.mkdir(); qual.mkdir()
            result = type("R", (), {"returncode": 1, "stderr": "unsupported", "stdout": ""})()
            with patch.object(recovery.subprocess, "run", return_value=result):
                with self.assertRaisesRegex(RuntimeError, "review frame extraction failed for 0"):
                    recovery.extract_review_frames(Path("ffmpeg.exe"), Path("final.mp4"), review, qual)
            log = json.loads((qual / "review_frame_000_PRE_ROLL_FIRST_ffmpeg.json").read_text())
            self.assertEqual(log["stderr"], "unsupported")

    def test_existing_review_frame_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); review = root / "review"; qual = root / "qualification"
            review.mkdir(); qual.mkdir()
            existing = review / "frame_000_PRE_ROLL_FIRST.png"
            existing.write_bytes(b"keep")
            with self.assertRaises(FileExistsError):
                recovery.extract_review_frames(Path("ffmpeg.exe"), Path("final.mp4"), review, qual)
            self.assertEqual(existing.read_bytes(), b"keep")

    def test_video_contract_rejects_wrong_codec_or_count(self):
        good = {"codec_name":"h264","width":720,"height":1280,"avg_frame_rate":"30/1",
                "pix_fmt":"yuv420p","profile":"High","color_range":"tv","nb_read_frames":"810"}
        recovery.validate_video_stream(good, "good")
        bad = dict(good, nb_read_frames="809")
        with self.assertRaises(RuntimeError): recovery.validate_video_stream(bad, "bad")

    def test_final_probe_requires_aac_lc_and_sync(self):
        video = {"codec_type":"video","codec_name":"h264","width":720,"height":1280,"avg_frame_rate":"30/1",
                 "pix_fmt":"yuv420p","profile":"High","color_range":"tv","nb_read_frames":"810","start_time":"0.0"}
        audio = {"codec_type":"audio","codec_name":"aac","profile":"LC","sample_rate":"48000","channels":2,"start_time":"0.0"}
        probe = {"streams":[video,audio],"format":{"duration":"27.0"}}
        self.assertEqual(recovery.validate_final_probe(probe, "valid")["av_start_delta_seconds"], 0.0)
        bad = {"streams":[video,dict(audio,start_time="0.1")],"format":{"duration":"27.0"}}
        with self.assertRaisesRegex(RuntimeError, "A/V start offset"):
            recovery.validate_final_probe(bad, "bad")

    def test_run_rejects_any_other_run_id_before_touching_project(self):
        args = type("Args", (), {"output_id":"E4C-CLI-COMPOSITION-V2-NOT-THIS-RUN", "project_root":"missing",
                                 "evidence_root":"missing", "ffmpeg":None,"ffprobe":None})()
        with self.assertRaisesRegex(ValueError, "bound to the existing R3 output id"):
            recovery.run(args)

    def test_canonical_intent_hash_excludes_self_hash_field(self):
        intent = {"b": 2, "a": "á", "intent_sha256": "placeholder"}
        expected = __import__("hashlib").sha256(
            json.dumps({"a": "á", "b": 2}, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        ).hexdigest()
        self.assertEqual(recovery.canonical_intent_sha256(intent), expected)

    def test_raw_file_sha_is_not_confused_with_canonical_intent_sha(self):
        intent = {"identity": {"request_id": "R"}, "intent_sha256": "placeholder"}
        canonical = recovery.canonical_intent_sha256(intent)
        raw = json.dumps(intent, indent=2).encode("utf-8")
        self.assertNotEqual(__import__("hashlib").sha256(raw).hexdigest(), canonical)

    def test_intent_integrity_requires_all_three_bindings(self):
        intent = {"identity": {"request_id": "R"}, "intent_sha256": "placeholder"}
        canonical = recovery.canonical_intent_sha256(intent)
        intent["intent_sha256"] = canonical
        receipt = {"e1_validation": {"intent_sha256": canonical}}
        with patch.object(recovery, "EXPECTED_INTENT_SHA256", canonical), patch.object(recovery, "EXPECTED_INTENT_FILE_SHA256", "raw-pin"):
            result = recovery.validate_intent_integrity(intent, "raw-pin", receipt)
        self.assertEqual(result, {"intent_file_sha256": "raw-pin", "intent_canonical_sha256": canonical})

    def test_intent_integrity_rejects_wrong_raw_file_hash(self):
        intent = {"x": 1, "intent_sha256": recovery.EXPECTED_INTENT_SHA256}
        receipt = {"e1_validation": {"intent_sha256": recovery.EXPECTED_INTENT_SHA256}}
        with self.assertRaisesRegex(ValueError, "intent file SHA-256 mismatch"):
            recovery.validate_intent_integrity(intent, "wrong-raw-sha", receipt)

    def test_original_evidence_uses_distinct_canonical_and_raw_hashes(self):
        self.assertEqual(recovery.EXPECTED_INTENT_SHA256, "9dfe5c1c4568ed7fbc4bb4260d47da4e518b1a163811fb88f2a9f1bff55c304e")
        self.assertEqual(recovery.EXPECTED_INTENT_FILE_SHA256, "dfc861764302d7a6dec71de4532828dfe146708ed33dd2483b9c611bdd2f9a94")
        self.assertNotEqual(recovery.EXPECTED_INTENT_SHA256, recovery.EXPECTED_INTENT_FILE_SHA256)

if __name__ == "__main__":
    unittest.main(verbosity=2)
