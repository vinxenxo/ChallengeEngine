import re
import unittest
from pathlib import Path


class CliSmokeRunnerContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]
        cls.runner = cls.root / "tools" / "c11d" / "d9" / "RUN_C11E_E4C_DRILL_CLI_SMOKE_V1.ps1"
        cls.installer = cls.root / "_installer" / "INSTALL_C11E_E4C_CLI_SMOKE_ACCEPTANCE_V1_6.ps1"
        cls.text = cls.runner.read_text(encoding="ascii")
        cls.installer_text = cls.installer.read_text(encoding="ascii")

    def test_01_explicit_cli_av_opt_in(self):
        self.assertIn("'--origin','CLI','--execute-drill-av'", self.text)

    def test_02_existing_cli_facade_and_single_shared_executor(self):
        self.assertIn("c11c-suite\\c11c-producer\\c11e_production_cli.py", self.text)
        self.assertIn("c11e_e4c_drill_execution.py", self.text)

    def test_03_fresh_request_id_and_no_output_reuse(self):
        self.assertIn("E4C-CLI-SMOKE-", self.text)
        self.assertIn("OUTPUT_COLLISION", self.text)
        self.assertIn("EVIDENCE_COLLISION", self.text)

    def test_04_pre_and_post_source_pins(self):
        self.assertIn("SOURCE_PINS_PRE=PASS", self.text)
        self.assertIn("SOURCE_PINS_POST=PASS", self.text)
        self.assertIn("Assert-SourcePins $root", self.text)
        pin_lines = re.findall(r"^\s*@\('([^']+)'", self.text, re.MULTILINE)
        self.assertEqual(len(pin_lines), 19)
        self.assertEqual(len(set(pin_lines)), 19)

    def test_05_e1_and_release_boundaries(self):
        for token in ("PASS_E1_PREPARATION_ONLY", "NOT_CONNECTED_E1", "production_dispatch", "release_authority"):
            self.assertIn(token, self.text)

    def test_06_process_capture_and_exit_code(self):
        for token in ("System.Diagnostics.ProcessStartInfo", "ReadToEndAsync()", "$process.ExitCode", "CLI_STDERR.log"):
            self.assertIn(token, self.text)

    def test_07_no_git_or_dependency_mutation(self):
        lower = self.text.lower()
        self.assertNotIn("git status", lower)
        self.assertNotIn("git rev-parse", lower)
        self.assertNotIn("pip install", lower)

    def test_08_no_cli_plan_only_false_pass(self):
        self.assertIn("--execute-drill-av", self.text)
        self.assertIn("PASS_E4C_DRILL_SINGLE_SELECTOR_A_V_QUALIFICATION", self.text)
        self.assertIn("$receiptPath = [string]$summary.receipt", self.text)

    def test_09_receipt_checks_governance_and_media_invariants(self):
        for token in ("source_pin_count -ne 91", "video_stream_identical", "audio_stream_changed",
                      "same_seed_ab_identical", "changed_seed_c_distinct", "c11c_frozen_manifest_unchanged",
                      "production_dispatch", "release_authority"):
            self.assertIn(token, self.text)

    def test_10_baseline_gui_request_and_receipt_are_sha_pinned(self):
        for token in ("BASE_GUI_REQUEST_SHA_FAIL", "BASE_GUI_RECEIPT_SHA_FAIL", "BASE_GUI_ACCEPTED_RECEIPT_MISMATCH",
                      "711749f3a7c4bb20340b5256da6100971e2be4f12a57c7b9c7267703ddb96a7e",
                      "d8aad7176ed99d8bc0c067cece58272c5ac44045d55d746c768ea72324d459db"):
            self.assertIn(token, self.text)

    def test_11_python_arguments_use_non_reserved_named_parameter(self):
        function_start = self.installer_text.index('function Invoke-Python')
        function_end = self.installer_text.index('function Assert-NoReparseAncestors', function_start)
        function_text = self.installer_text[function_start:function_end]
        self.assertIn('$PythonArguments', function_text)
        self.assertNotRegex(function_text, r'(?i)\$Args\b')
        self.assertIn('-PythonArguments ([string[]]@(', self.installer_text)
        self.assertIn('PYTHON_ARGUMENT_LIST_EMPTY', function_text)

    def test_12_python_stdin_is_closed_and_command_is_logged(self):
        function_start = self.installer_text.index('function Invoke-Python')
        function_end = self.installer_text.index('function Assert-NoReparseAncestors', function_start)
        function_text = self.installer_text[function_start:function_end]
        self.assertIn('$psi.RedirectStandardInput = $true', function_text)
        self.assertIn('$p.StandardInput.Close()', function_text)
        self.assertIn('$script:PythonCommandLine', function_text)
        self.assertIn('PYTHON_TIMEOUT: timeout_seconds=', function_text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
