from __future__ import annotations
import argparse
import re
import sys
import unittest
from pathlib import Path

class RequalifierWaitTimeoutContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        parser = argparse.ArgumentParser()
        parser.add_argument("--wrapper", required=True)
        parser.add_argument("--runner", required=True)
        args, _ = parser.parse_known_args()
        cls.wrapper = Path(args.wrapper).read_text(encoding="utf-8-sig")
        cls.runner = Path(args.runner).read_text(encoding="utf-8-sig")

    def test_timeout_seconds_are_explicitly_1800(self):
        self.assertRegex(self.wrapper, r"\$timeoutSeconds\s*=\s*1800\b")

    def test_seconds_are_converted_to_milliseconds(self):
        self.assertRegex(self.wrapper, r"\$timeoutMilliseconds\s*=\s*\[int\]\(\$timeoutSeconds\s*\*\s*1000\s*\)")

    def test_wait_for_exit_poll_uses_bounded_millisecond_value(self):
        self.assertIn("$waitMilliseconds=[int][Math]::Min(3000,$remaining)", self.wrapper)
        self.assertIn("$proc.WaitForExit($waitMilliseconds)", self.wrapper)
        self.assertNotIn("$proc.WaitForExit(1800)", self.wrapper)

    def test_timeout_kills_descendant_process_tree(self):
        self.assertIn("taskkill.exe", self.wrapper)
        self.assertRegex(self.wrapper, r"/PID\s+\$proc\.Id\s+/T\s+/F")

    def test_timeout_failure_records_seconds_and_milliseconds(self):
        self.assertIn("timeout_seconds=$timeoutSeconds", self.wrapper)
        self.assertIn("timeout_milliseconds=$timeoutMilliseconds", self.wrapper)

    def test_wrapper_polls_progress_file(self):
        self.assertIn("V2_REQUALIFICATION_PROGRESS.json", self.wrapper)
        self.assertIn("REQUALIFIER_PROGRESS_STAGE=", self.wrapper)

    def test_runner_has_atomic_progress_writer(self):
        self.assertIn("def write_progress(", self.runner)
        self.assertIn("os.replace(temp, path)", self.runner)

    def test_runner_checkpoints_frame_composition_every_30_frames(self):
        self.assertIn("(frame_index + 1) % 30 == 0", self.runner)
        self.assertIn('"FRAME_COMPOSITION"', self.runner)

    def test_runner_publishes_required_stages(self):
        for stage in ("HISTORICAL_EVIDENCE_VERIFIED", "V2_COMPOSITION_PLAN_READY", "FFMPEG_TOOLCHAIN_READY", "NATIVE_INPUT_PROBED", "FRAME_COMPOSITION_COMPLETE", "SILENT_OUTPUT_PROBED", "REVIEW_FRAMES_READY", "COMPLETE"):
            self.assertIn(f'"{stage}"', self.runner)

    def test_runner_captures_failure_in_progress_checkpoint(self):
        self.assertIn('write_progress(Path(progress_path), "FAILED"', self.runner)

if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]], verbosity=2)
