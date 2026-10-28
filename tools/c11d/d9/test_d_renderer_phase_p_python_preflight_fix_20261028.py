"""Phase P Python preflight regression. Static only: no Python/Godot child processes."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUNNER = ROOT / "tools" / "c11d" / "d9" / "run_d_renderer_phase_p_source_value_frame_value_provenance_20261028.ps1"


def is_python_313_version_output(value: str) -> bool:
    return re.match(r"^Python\s+3\.13(?:\.|$)", value.strip()) is not None


class PhasePPythonPreflightTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not RUNNER.is_file():
            raise AssertionError(f"Required runner not found: {RUNNER}")
        cls.source = RUNNER.read_text(encoding="utf-8-sig")

    def test_native_version_switch_is_used(self) -> None:
        self.assertIn("$pythonVersionOutput = & $pythonLauncher.Source -3.13 --version 2>&1", self.source)

    def test_version_probe_exit_code_is_captured_immediately(self) -> None:
        self.assertRegex(self.source, r"\$pythonVersionOutput\s*=.*--version\s+2>&1\s*\r?\n\s*\$pythonVersionExitCode\s*=\s*\$LASTEXITCODE")

    def test_version_output_must_be_python_313(self) -> None:
        self.assertRegex(self.source, r"\$pythonVersionText\s*-notmatch\s*'\^Python\\s\+3\\\.13\(\?:\\\.|\$\)'" )
        self.assertIn("if ($pythonVersionExitCode -ne 0", self.source)

    def test_executable_probe_is_separate(self) -> None:
        self.assertIn("$pythonExecutableOutput = & $pythonLauncher.Source -3.13 -c 'import sys; print(sys.executable)' 2>&1", self.source)

    def test_executable_probe_has_no_embedded_double_quotes(self) -> None:
        m = re.search(r"(?m)^\s*\$pythonExecutableOutput\s*=\s*&\s*\$pythonLauncher\.Source\s+-3\.13\s+-c\s+'([^'\r\n]+)'", self.source)
        self.assertIsNotNone(m)
        assert m is not None
        self.assertNotIn('"', m.group(1))
        self.assertEqual(m.group(1), "import sys; print(sys.executable)")

    def test_executable_probe_exit_code_is_captured_immediately(self) -> None:
        self.assertRegex(self.source, r"\$pythonExecutableOutput\s*=.*-c\s+'import sys; print\(sys\.executable\)'\s+2>&1\s*\r?\n\s*\$pythonExecutableExitCode\s*=\s*\$LASTEXITCODE")

    def test_executable_output_must_be_nonempty_single_line(self) -> None:
        self.assertIn("[string]::IsNullOrWhiteSpace($pythonExecutableText)", self.source)
        self.assertIn("@($pythonExecutableOutput).Count -ne 1", self.source)

    def test_executable_output_must_resolve_to_existing_file(self) -> None:
        self.assertIn("Test-Path -LiteralPath $pythonExecutableText -PathType Leaf", self.source)

    def test_python_exe_comes_from_executable_probe(self) -> None:
        self.assertIn("$pythonExe = $pythonExecutableText", self.source)
        self.assertNotIn("$pythonExe = $pythonVersionOutput[1].Trim()", self.source)

    def test_old_combined_quoted_version_probe_is_absent(self) -> None:
        self.assertNotRegex(self.source, r"(?m)\$pythonVersionOutput\s*=.*-3\.13\s+-c\s+'import sys; print\(\"%d")

    def test_version_output_is_not_indexed_as_two_lines(self) -> None:
        self.assertNotIn("$pythonVersionOutput.Count -lt 2", self.source)
        self.assertNotIn("$pythonVersionOutput[0].StartsWith('3.13.')", self.source)

    def test_preflight_order_precedes_static_suite_and_runtime_audit(self) -> None:
        version = self.source.index("$pythonVersionOutput = & $pythonLauncher.Source -3.13 --version 2>&1")
        executable = self.source.index("$pythonExecutableOutput = & $pythonLauncher.Source -3.13 -c 'import sys; print(sys.executable)' 2>&1")
        python_exe = self.source.index("$pythonExe = $pythonExecutableText")
        static_tests = self.source.index("$testPath = Join-Path")
        runtime_audit = self.source.index("$runScript = Join-Path")
        self.assertLess(version, executable)
        self.assertLess(executable, python_exe)
        self.assertLess(python_exe, static_tests)
        self.assertLess(static_tests, runtime_audit)

    def test_version_match_accepts_only_python_313(self) -> None:
        self.assertTrue(is_python_313_version_output("Python 3.13.14\r\n"))
        self.assertTrue(is_python_313_version_output("Python 3.13"))
        self.assertFalse(is_python_313_version_output("Python 3.12.8"))
        self.assertFalse(is_python_313_version_output("python 3.13.14"))
        self.assertFalse(is_python_313_version_output("Python 3.130.0"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
