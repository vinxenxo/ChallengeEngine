from __future__ import annotations
import hashlib
from pathlib import Path
import re
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DRIVER = PROJECT_ROOT / "tools" / "c11d" / "d9" / "c11e_e4c_saccade_tier_batch.py"
RUNNER = PROJECT_ROOT / "tools" / "c11d" / "d9" / "RUN_C11E_E4C_SACCADE_TIERS_1_TO_5_V1.ps1"


class SaccadeRunnerContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver_text = DRIVER.read_text(encoding="utf-8")
        cls.runner_text = RUNNER.read_text(encoding="ascii")

    def test_driver_sha_pin_is_exact_and_64_hex(self):
        match = re.search(r"\$driverSha -ne '([a-f0-9]{64})'", self.runner_text)
        self.assertIsNotNone(match)
        self.assertEqual(hashlib.sha256(DRIVER.read_bytes()).hexdigest(), match.group(1))

    def test_runner_is_ascii_without_bom(self):
        raw = RUNNER.read_bytes()
        self.assertFalse(raw.startswith(b"\xef\xbb\xbf"))
        self.assertTrue(all(b < 128 for b in raw))

    def test_runner_self_parses_and_requires_windows_powershell_51(self):
        self.assertIn("Parser]::ParseFile($PSCommandPath", self.runner_text)
        self.assertIn("WINDOWS_POWERSHELL_5_1_REQUIRED", self.runner_text)

    def test_runner_waits_for_child_and_captures_both_streams(self):
        self.assertIn("Start-Process", self.runner_text)
        self.assertIn("-Wait -PassThru", self.runner_text)
        self.assertIn("-RedirectStandardOutput", self.runner_text)
        self.assertIn("-RedirectStandardError", self.runner_text)
        self.assertIn("$process.ExitCode", self.runner_text)

    def test_prepare_only_is_default_and_execute_is_explicit(self):
        self.assertIn("[switch]$Execute", self.runner_text)
        self.assertIn("if ($Execute) { $argsList += '--execute' }", self.runner_text)
        self.assertIn("NOT_STARTED_PREPARE_ONLY", self.runner_text)

    def test_runner_pins_style_guides_v29_v30_v31_v33_v34(self):
        for label in ("V29", "V30", "V31", "V33", "V34"):
            self.assertIn("Label='" + label + "'", self.runner_text)
        self.assertNotIn("__STYLE_GUIDE_V34_SHA256__", self.runner_text)

    def test_runner_style_guide_v34_sha_matches_exact_packaged_bytes(self):
        digest = hashlib.sha256((PROJECT_ROOT / "docs" / "current" / "e" / "C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261116_V34.md").read_bytes()).hexdigest()
        match = re.search(r"Relative='docs\\current\\e\\C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261116_V34\.md'; Sha='([a-f0-9]{64})'; Label='V34'", self.runner_text)
        self.assertIsNotNone(match)
        self.assertEqual(digest, match.group(1))

    def test_driver_declares_exact_37_source_pins(self):
        self.assertIn("if len(SOURCE_PINS) != 37", self.driver_text)
        self.assertIn("test_exact_37_runtime_source_pins_are_declared", (PROJECT_ROOT / "tests" / "test_c11e_e4c_saccade_tier_batch.py").read_text(encoding="utf-8"))

    def test_both_pursuit_and_saccade_canonicals_are_pinned(self):
        self.assertIn("PURSUIT_CANONICAL_REL: PURSUIT_CANONICAL_SHA256", self.driver_text)
        self.assertIn("SACCADE_CANONICAL_REL: SACCADE_CANONICAL_SHA256", self.driver_text)

    def test_frozen_manifest_identity_is_pinned(self):
        self.assertIn("e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953", self.driver_text)

    def test_no_git_bookkeeping_is_in_runner_or_driver(self):
        for content in (self.driver_text, self.runner_text):
            self.assertNotRegex(content, r"(?im)\bgit\s+(status|branch|rev-parse|log|commit)\b")

    def test_all_five_saccade_tiers_are_one_shot(self):
        self.assertIn("TIERS = (1, 2, 3, 4, 5)", self.driver_text)
        self.assertIn("AUTHORIZED_ONCE_FOR_TIERS_1_TO_5", self.driver_text)
        self.assertIn("BATCH_EVIDENCE_COLLISION", self.driver_text)

    def test_no_pursuit_t1_recovery_is_used_for_saccade(self):
        self.assertNotIn("REUSED_EXISTING_T1", self.driver_text)
        self.assertIn("All five Saccade tiers are independent", self.driver_text)
        self.assertIn("base_cli_smoke", self.driver_text)
        self.assertIn("REQUEST_TEMPLATE_ONLY_NO_RERUN", self.driver_text)

    def test_saccade_profile_is_circuit_pulse(self):
        self.assertIn('EXPECTED_PROFILE = "CIRCUIT_PULSE"', self.driver_text)
        self.assertIn('"family_music_profile": EXPECTED_PROFILE', self.driver_text)

    def test_timeline_uses_native_510_frames_plus_90_90(self):
        self.assertIn("PRE_ROLL_SECONDS = 3.0", self.driver_text)
        self.assertIn("END_CTA_SECONDS = 3.0", self.driver_text)
        self.assertIn('"PRE_ROLL": pre_roll, "GAME": gameplay_frames, "END_CTA": end_cta', self.driver_text)

    def test_91_physical_pins_are_verified_before_and_after_child(self):
        self.assertIn("def verify_91_pin_snapshots", self.driver_text)
        self.assertIn("source_pins_immediately_pre_renderer", self.driver_text)
        self.assertIn("source_pins_post_execution", self.driver_text)

    def test_failures_stop_batch_and_preserve_one_shot_evidence(self):
        self.assertIn("STOPPED_FAIL_CLOSED", self.driver_text)
        self.assertIn("Any failed child or post-child audit consumes this BatchId permanently", self.driver_text)
        self.assertIn("do not retry it", self.driver_text)

    def test_output_collisions_fail_before_attempt_authorization(self):
        exec_start = self.driver_text.index("def execute_batch(")
        lock_start = self.driver_text.index('"status": "ATTEMPT_RESERVED"', exec_start)
        collision_start = self.driver_text.index("OUTPUT_COLLISION", exec_start)
        self.assertLess(collision_start, lock_start)

    def test_request_uses_selector_specific_saccade_family(self):
        self.assertIn('"family_id": "saccade"', self.driver_text)
        self.assertIn('f"saccade/tier-{tier}"', self.driver_text)

    def test_no_renderer_or_dispatch_during_prepare_only(self):
        self.assertIn('"renderer_invoked": False', self.driver_text)
        self.assertIn('"production_dispatch": False', self.driver_text)
        self.assertIn('"release_authority": "NONE"', self.driver_text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
