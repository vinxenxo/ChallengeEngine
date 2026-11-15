from __future__ import annotations
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "tools" / "c11d" / "d9" / "RUN_C11E_E4C_TRACKING_TIERS_2_TO_5_V1.ps1"
DRIVER = ROOT / "tools" / "c11d" / "d9" / "c11e_e4c_tracking_tier_batch.py"
COORDINATOR = DRIVER.read_text(encoding="utf-8")
RUNNER_TEXT = RUNNER.read_text(encoding="utf-8")

class TrackingRunnerContractTests(unittest.TestCase):
    def test_wrapper_pins_exact_installed_coordinator_sha(self):
        expected = hashlib.sha256(DRIVER.read_bytes()).hexdigest()
        match = re.search(r"\$driverSha -ne '([0-9a-f]{64})'", RUNNER_TEXT)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), expected)

    def test_wrapper_uses_only_installed_v23_and_v27_guides(self):
        self.assertIn("STYLE_GUIDE_20261114_V23.md", RUNNER_TEXT)
        self.assertIn("STYLE_GUIDE_20261115_V27.md", RUNNER_TEXT)
        for stale in ("STYLE_GUIDE_20261115_V24.md", "STYLE_GUIDE_20261115_V25.md", "STYLE_GUIDE_20261115_V26.md"):
            self.assertNotIn(stale, RUNNER_TEXT)

    def test_wrapper_requires_v27_switch(self):
        self.assertIn("--require-v27-guide", RUNNER_TEXT)
        self.assertNotIn("--require-v26-guide", RUNNER_TEXT)

    def test_default_path_is_prepare_only(self):
        self.assertIn("if ($Execute) { $argsList += '--execute' }", RUNNER_TEXT)
        self.assertIn("BATCH_EXECUTION=NOT_STARTED_PREPARE_ONLY", RUNNER_TEXT)

    def test_module_requires_installed_v27_guide(self):
        self.assertIn("STYLE_GUIDE_V27_PATH", COORDINATOR)
        self.assertIn("93b83ec7c5a640235edc3d70e877088896babe9d6d3b1fc3ed224fe0b6b07f43", COORDINATOR)
        self.assertIn("--require-v27-guide", COORDINATOR)
        self.assertIn("if args.require_v27_guide:", COORDINATOR)
        self.assertNotIn("args.require_v26_guide", COORDINATOR)

    def test_no_git_or_production_dispatch_commands(self):
        for token in ("git status", "git rev-parse", "git branch", "git commit"):
            self.assertNotIn(token, RUNNER_TEXT.lower())
        self.assertIn("PRODUCTION_DISPATCH=FALSE", RUNNER_TEXT)
        self.assertIn("RELEASE_AUTHORITY=NONE", RUNNER_TEXT)

if __name__ == "__main__":
    unittest.main(verbosity=2)
