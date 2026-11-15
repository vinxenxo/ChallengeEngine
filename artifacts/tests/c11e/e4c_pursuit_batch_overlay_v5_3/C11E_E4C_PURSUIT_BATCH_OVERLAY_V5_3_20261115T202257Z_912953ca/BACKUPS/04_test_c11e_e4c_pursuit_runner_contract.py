from __future__ import annotations

from pathlib import Path
import hashlib
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "tools" / "c11d" / "d9" / "RUN_C11E_E4C_PURSUIT_TIERS_1_TO_5_V1.ps1"
DRIVER = ROOT / "tools" / "c11d" / "d9" / "c11e_e4c_pursuit_tier_batch.py"
INSTALLER = ROOT.parent / "INSTALL_C11E_E4C_PURSUIT_BATCH_OVERLAY_V4_RECOVERY.ps1"


class PursuitRunnerContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.raw = RUNNER.read_bytes()
        self.text = self.raw.decode("ascii")

    def test_runner_is_ascii_and_has_no_bom(self):
        self.assertFalse(self.raw.startswith(b"\xef\xbb\xbf"))
        self.assertTrue(all(byte < 128 for byte in self.raw))

    def test_runner_self_parses_with_powershell_51_ast(self):
        self.assertIn("[System.Management.Automation.Language.Parser]::ParseFile($PSCommandPath", self.text)
        self.assertIn("WINDOWS_POWERSHELL_5_1_REQUIRED", self.text)

    def test_prepare_only_is_default_and_execute_is_explicit(self):
        self.assertIn("[switch]$Execute", self.text)
        self.assertIn("if ($Execute) { $argsList += '--execute' }", self.text)
        self.assertNotIn("$argsList += '--execute'\n", self.text.replace("if ($Execute) { $argsList += '--execute' }", ""))

    def test_child_process_waits_before_reading_logs_and_captures_exit(self):
        start = self.text.index("Start-Process -FilePath $python")
        exit_pos = self.text.index("$exitCode = [int]$process.ExitCode", start)
        stdout_pos = self.text.index("Get-Content -LiteralPath $stdoutPath", start)
        stderr_pos = self.text.index("Get-Content -LiteralPath $stderrPath", start)
        self.assertLess(start, exit_pos)
        self.assertLess(exit_pos, stdout_pos)
        self.assertLess(exit_pos, stderr_pos)
        self.assertIn("-Wait -PassThru -RedirectStandardOutput", self.text)

    def test_exact_pursuit_driver_pin_matches_staged_driver_bytes(self):
        self.assertIn("c11e_e4c_pursuit_tier_batch.py", self.text)
        actual = hashlib.sha256(DRIVER.read_bytes()).hexdigest()
        match = re.search(r"if \(\$driverSha -ne '([0-9a-f]{64})'\)", self.text)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), actual)
        self.assertEqual(actual, "7164a83c882116081cda720b37c47107e9145ad2b918b759470b06c5eb3d5522")
        self.assertNotIn("dcb2c035ff5aee83a673e30347617aed67c8b382bf85af68441153611964566b", self.text)

    def test_exact_style_guides_v23_through_v30_remain_pinned(self):
        for value in (
            "C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261114_V23.md",
            "1900b8a06f52156ff18790adb44ef82268c386e2633d2b31237ebc705208c3a5",
            "C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261115_V27.md",
            "93b83ec7c5a640235edc3d70e877088896babe9d6d3b1fc3ed224fe0b6b07f43",
            "C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261115_V28.md",
            "24d9e24ac09a7a8a58445838525a306fc3f3fb8bb31f9dfa5ac7265ed3b71239",
            "C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261115_V29.md",
            "76d9187f7d8c9b44ed940f18fd242f2205e6caf357c8b7dc19756fa1cf8a0c0a",
            "C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261115_V30.md",
            "57d653890535849c7a1d55733c29b1f7fe574010a8cdb18b8d2fd86565b50c83",
        ):
            self.assertIn(value, self.text)

    def test_wrapper_stops_on_child_failure_and_leaves_dispatch_disabled(self):
        self.assertIn("if ($exitCode -ne 0) { throw", self.text)
        self.assertIn("PRODUCTION_DISPATCH=FALSE", self.text)
        self.assertIn("RELEASE_AUTHORITY=NONE", self.text)

    def test_installer_uses_start_process_for_python_test_streams(self):
        installer = INSTALLER.read_text(encoding="ascii")
        self.assertIn("Start-Process -FilePath $FilePath", installer)
        self.assertIn("-RedirectStandardOutput $StdoutPath", installer)
        self.assertIn("-RedirectStandardError $StderrPath", installer)
        self.assertIn("$exitCode = [int]$process.ExitCode", installer)
        self.assertNotIn("& $python $stageTest1 2>&1", installer)
        self.assertNotIn("& $python $stageTest2 2>&1", installer)

    def test_installer_audits_exact_prior_v2_transaction_before_mutation(self):
        installer = INSTALLER.read_text(encoding="ascii")
        for value in (
            "C11E_E4C_PURSUIT_BATCH_OVERLAY_V2_20261115T130255Z_b5f15417",
            "INSTALL_TRANSACTION_JOURNAL.json",
            "committed_count",
            "ADD_COMMITTED",
            "PREINSTALL_PREFLIGHT.json",
            "V2_PRIOR_TRANSACTION_AUDIT",
        ):
            self.assertIn(value, installer)
        self.assertLess(installer.index("V2_PRIOR_TRANSACTION_AUDIT"), installer.index("$transactionStarted = $true"))

    def test_installer_uses_single_captured_frozen_manifest_post_pin(self):
        installer = INSTALLER.read_text(encoding="ascii")
        self.assertIn("$postPinByPath['release/C11C_FREEZE_PACKAGE_MANIFEST.json']", installer)
        self.assertIn("FROZEN_C11C_MANIFEST_POST_PIN_MISMATCH", installer)
        self.assertNotIn(r"Get-Sha256 (Join-Path $root 'release\C11C_FREEZE_PACKAGE_MANIFEST.json')", installer)

    def test_installer_defaults_to_prepare_only_without_execute_switch(self):
        installer = INSTALLER.read_text(encoding="ascii")
        self.assertIn("$runnerArgs = @('-NoProfile','-ExecutionPolicy','Bypass','-File',$v4RunnerPath", installer)
        self.assertNotIn("$runnerArgs += '-Execute'", installer)
        self.assertIn("PURSUIT_BATCH_EXECUTION=NOT_STARTED_PREPARE_ONLY", installer)
        for flag in ("renderer_invoked", "godot_invoked", "ffmpeg_invoked", "production_media_created", "production_dispatch"):
            self.assertIn("if ($preview.$flag -ne $false)", installer)
        self.assertIn("$preview.source_pin_count -ne 34", installer)

    def test_replacement_preimages_are_pinned_and_backups_are_verified(self):
        import json
        installer = INSTALLER.read_text(encoding="ascii")
        manifest = json.loads((INSTALLER.parent / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
        replacements = {op["destination"]: op for op in manifest["operations"] if op["operation"] == "REPLACE"}
        runner_rel = "tools/c11d/d9/RUN_C11E_E4C_PURSUIT_TIERS_1_TO_5_V1.ps1"
        test_rel = "tests/test_c11e_e4c_pursuit_runner_contract.py"
        self.assertEqual(replacements[runner_rel]["preimage_sha256"], "e31cd6d503426e9d6188363d35cdf426d3836fb91f120b16d835e5fe6045e009")
        self.assertEqual(replacements[test_rel]["preimage_sha256"], "f7948339a64c9ce0d27b5fbc33a4fe519ad1480b541c844ba302daa27e3e4f56")
        self.assertIn("BACKUP_PREIMAGE_SHA_FAIL", installer)
        self.assertIn("Invoke-C11EAtomicReplace", installer)


if __name__ == "__main__":
    unittest.main(verbosity=2)
