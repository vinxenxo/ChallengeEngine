from __future__ import annotations
import hashlib
from pathlib import Path
import re
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DRIVER = PROJECT_ROOT / "tools" / "c11d" / "d9" / "c11e_e4c_peripheral_scan_tier_batch.py"
RUNNER = PROJECT_ROOT / "tools" / "c11d" / "d9" / "RUN_C11E_E4C_PERIPHERAL_SCAN_TIERS_1_TO_5_V1.ps1"


class PeripheralScanRunnerContractTests(unittest.TestCase):
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

    def test_runner_pins_style_guides_v29_v30_v31_v33_v34_v35_v36(self):
        for label in ("V29", "V30", "V31", "V33", "V34", "V35", "V36"):
            self.assertIn("Label='" + label + "'", self.runner_text)
        self.assertNotIn("__STYLE_GUIDE_V34_SHA256__", self.runner_text)

    def test_runner_style_guide_v36_sha_matches_exact_packaged_bytes(self):
        digest = hashlib.sha256((PROJECT_ROOT / "docs" / "current" / "e" / "C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261116_V36.md").read_bytes()).hexdigest()
        match = re.search(r"Relative='docs\\current\\e\\C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261116_V36\.md'; Sha='([a-f0-9]{64})'; Label='V36'", self.runner_text)
        self.assertIsNotNone(match)
        self.assertEqual(digest, match.group(1))
        guide_v35 = PROJECT_ROOT / "docs" / "current" / "e" / "C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261116_V35.md"
        self.assertEqual(hashlib.sha256(guide_v35.read_bytes()).hexdigest(), "6680fabaabc8428cc33d0c0d38af6df443b6f0e2be8470362c1a144c5047ff8a")
        installer = (PROJECT_ROOT / "INSTALL_C11E_E4C_PERIPHERAL_SCAN_COMBINED_OVERLAY_V2.ps1").read_text(encoding="utf-8")
        self.assertIn("docs/current/e/C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261116_V35.md", installer)
        self.assertIn("$v35TestGuide = Join-Path $stageRoot 'payload\\docs\\current\\e\\C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261116_V35.md'", installer)

    def test_driver_declares_exact_38_source_pins(self):
        self.assertIn("if len(SOURCE_PINS) != 38", self.driver_text)
        self.assertIn("test_exact_38_runtime_source_pins_are_declared", (PROJECT_ROOT / "tests" / "test_c11e_e4c_peripheral_scan_tier_batch.py").read_text(encoding="utf-8"))

    def test_all_three_completed_and_active_family_canonicals_are_pinned(self):
        self.assertIn("PURSUIT_CANONICAL_REL: PURSUIT_CANONICAL_SHA256", self.driver_text)
        self.assertIn("SACCADE_CANONICAL_REL: SACCADE_CANONICAL_SHA256", self.driver_text)
        self.assertIn("PERIPHERAL_SCAN_CANONICAL_REL: PERIPHERAL_SCAN_CANONICAL_SHA256", self.driver_text)

    def test_frozen_manifest_identity_is_pinned(self):
        self.assertIn("e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953", self.driver_text)

    def test_no_git_bookkeeping_is_in_runner_or_driver(self):
        for content in (self.driver_text, self.runner_text):
            self.assertNotRegex(content, r"(?im)\bgit\s+(status|branch|rev-parse|log|commit)\b")

    def test_all_five_peripheral_scan_tiers_are_one_shot(self):
        self.assertIn("TIERS = (1, 2, 3, 4, 5)", self.driver_text)
        self.assertIn("AUTHORIZED_ONCE_FOR_TIERS_1_TO_5", self.driver_text)
        self.assertIn("BATCH_EVIDENCE_COLLISION", self.driver_text)

    def test_no_pursuit_t1_recovery_is_used_for_peripheral_scan(self):
        self.assertNotIn("REUSED_EXISTING_T1", self.driver_text)
        self.assertIn("All five Peripheral Scan tiers are independent", self.driver_text)
        self.assertIn("base_cli_smoke", self.driver_text)
        self.assertIn("REQUEST_TEMPLATE_ONLY_NO_RERUN", self.driver_text)

    def test_peripheral_scan_profile_is_orbital_ritual(self):
        self.assertIn('EXPECTED_PROFILE = "ORBITAL_RITUAL"', self.driver_text)
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

    def test_request_uses_selector_specific_peripheral_scan_family(self):
        self.assertIn('"family_id": "peripheral_scan"', self.driver_text)
        self.assertIn('f"peripheral_scan/tier-{tier}"', self.driver_text)

    def test_no_renderer_or_dispatch_during_prepare_only(self):
        self.assertIn('"renderer_invoked": False', self.driver_text)
        self.assertIn('"production_dispatch": False', self.driver_text)
        self.assertIn('"release_authority": "NONE"', self.driver_text)

    def test_combined_installer_supports_explicit_execute_batch_and_receipt(self):
        installer = (PROJECT_ROOT / "INSTALL_C11E_E4C_PERIPHERAL_SCAN_COMBINED_OVERLAY_V2.ps1").read_text(encoding="utf-8")
        self.assertIn("[switch]$ExecuteBatch", installer)
        self.assertIn("if ($ExecuteBatch)", installer)
        self.assertIn("BATCH_LAUNCH_RECEIPT.json", installer)
        self.assertIn("COMBINED_EXECUTION_RECEIPT.json", installer)
        self.assertIn("$env:PYTHONPATH = $stageDriverProject", installer)
        self.assertIn("finally {", installer)
        self.assertIn("Remove-Item Env:PYTHONPATH", installer)

    def test_runner_writes_create_new_batch_launch_receipt(self):
        self.assertIn("[string]$ResultReceiptPath", self.runner_text)
        self.assertIn("[IO.FileMode]::CreateNew", self.runner_text)
        self.assertIn("BATCH_RESULT.json", self.runner_text)
        self.assertIn("batch_result_sha256", self.runner_text)

    def test_combined_batch_failure_does_not_rollback_committed_add_only_install(self):
        installer = (PROJECT_ROOT / "INSTALL_C11E_E4C_PERIPHERAL_SCAN_COMBINED_OVERLAY_V2.ps1").read_text(encoding="utf-8")
        marker = installer.index("$installCommitted = $true")
        launch = installer.index("if ($ExecuteBatch)", marker)
        catch_start = installer.index("\ncatch {", marker)
        rollback = installer.index("if ($transactionStarted)", catch_start)
        self.assertLess(marker, launch)
        self.assertIn("$transactionStarted = $false", installer[marker:launch])
        self.assertIn("install_committed", installer)
        self.assertGreater(rollback, catch_start)

    def test_installer_executes_runner_only_after_install_receipt_and_commit(self):
        installer = (PROJECT_ROOT / "INSTALL_C11E_E4C_PERIPHERAL_SCAN_COMBINED_OVERLAY_V2.ps1").read_text(encoding="utf-8")
        receipt = installer.index("Write-JsonAtomic $receiptPath $receipt")
        launch = installer.index("if ($ExecuteBatch)", receipt)
        self.assertLess(receipt, launch)
        self.assertIn("-Execute", installer[launch:])

    def test_no_batch_id_is_supplied_by_combined_installer(self):
        installer = (PROJECT_ROOT / "INSTALL_C11E_E4C_PERIPHERAL_SCAN_COMBINED_OVERLAY_V2.ps1").read_text(encoding="utf-8")
        self.assertNotRegex(installer, r"(?im)-BatchId\s+\$")

    def test_execution_receipt_path_collision_is_preflighted_before_child_start(self):
        preflight = self.runner_text.index("EXECUTION_RECEIPT_PREFLIGHT=PASS")
        start_child = self.runner_text.index("$process = Start-Process")
        self.assertLess(preflight, start_child)
        self.assertIn("PERIPHERAL_SCAN_EXECUTION_RECEIPT_PATH_REQUIRED_BEFORE_CHILD", self.runner_text)
        self.assertIn("PERIPHERAL_SCAN_RESULT_RECEIPT_COLLISION_BEFORE_CHILD", self.runner_text)
        self.assertIn("[IO.FileMode]::CreateNew", self.runner_text)

    def test_driver_persists_reserved_batch_id_to_stderr_for_failure_recovery(self):
        marker = 'print(f"BATCH_RESERVED_ID={batch_id}", file=sys.stderr, flush=True)'
        self.assertIn(marker, self.driver_text)
        self.assertLess(self.driver_text.index('write_json_exclusive(progress_path, progress)'), self.driver_text.index(marker))

    def test_combined_execution_receipt_is_acyclic_and_keeps_install_receipt_immutable(self):
        installer = (PROJECT_ROOT / "INSTALL_C11E_E4C_PERIPHERAL_SCAN_COMBINED_OVERLAY_V2.ps1").read_text(encoding="utf-8")
        combined = installer.index("Write-JsonAtomic $combinedReceiptPath $combined")
        self.assertEqual(installer.count("Write-JsonAtomic $receiptPath $receipt"), 1)
        catch_start = installer.index("\ncatch {", combined)
        self.assertNotIn("Write-JsonAtomic $journalPath $journal", installer[combined:catch_start])
        self.assertIn("install_receipt_sha256=(Get-Sha256 $receiptPath)", installer)
        self.assertIn("batch_result_sha256=(Get-Sha256 $batchResultPath)", installer)
        self.assertIn("batch_launch_receipt_sha256=(Get-Sha256 $batchLaunchReceiptPath)", installer)


if __name__ == "__main__":
    unittest.main(verbosity=2)
