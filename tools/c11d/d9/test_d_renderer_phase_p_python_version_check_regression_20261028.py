"""Focused regression tests for the Phase P Python 3.13 version guard; static only."""
from __future__ import annotations
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUNNER = ROOT / "tools" / "c11d" / "d9" / "run_d_renderer_phase_p_source_value_frame_value_provenance_20261028.ps1"


def phase_p_normalize_version(raw: str) -> str:
    # Mirrors the two prefix-normalization operations used by the PowerShell runner.
    value = re.sub(r"^Python\s+", "", raw.strip())
    value = re.sub(r"^[^\d]*", "", value).strip()
    return value


class PhasePPythonVersionCheckRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not RUNNER.is_file():
            raise AssertionError(f"Phase P runner missing: {RUNNER}")
        cls.source = RUNNER.read_text(encoding="utf-8-sig")

    def test_version_probe_uses_native_version_switch(self) -> None:
        self.assertIn("-3.13 --version 2>&1", self.source)

    def test_normalization_removes_python_prefix_before_validation(self) -> None:
        self.assertRegex(self.source, r"(?m)^\s*\$pythonVersionOutput\s*=.*-replace\s+'\^Python\\s\+',\s*''\s*\)\s*$")
        self.assertRegex(self.source, r"(?m)^\s*\$pythonVersionText\s*=.*-replace\s+'\^\[\^\\d\]\*',\s*''\s*$")

    def test_validation_matches_normalized_version_not_removed_prefix(self) -> None:
        self.assertRegex(self.source, r"(?m)^\s*if\s*\(\$pythonVersionExitCode\s*-ne\s*0\s*-or\s*\$pythonVersionText\s*-notmatch\s+'\^3\\\.13\(\?:\\\.|\$\)'\)")
        self.assertNotRegex(self.source, r"(?m)\$pythonVersionText\s*-notmatch\s+'\^Python\\s\+3\\\.13")

    def test_python_313_patch_version_passes(self) -> None:
        normalized = phase_p_normalize_version("Python 3.13.14\r\n")
        self.assertEqual(normalized, "3.13.14")
        self.assertRegex(normalized, r"^3\.13(?:\.|$)")

    def test_python_313_without_patch_passes(self) -> None:
        normalized = phase_p_normalize_version("Python 3.13")
        self.assertRegex(normalized, r"^3\.13(?:\.|$)")

    def test_wrong_python_versions_fail_closed(self) -> None:
        for raw in ("Python 3.12.8", "Python 3.130.0", "Python 2.7.18", "not a Python version"):
            normalized = phase_p_normalize_version(raw)
            self.assertNotRegex(normalized, r"^3\.13(?:\.|$)", msg=raw)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(PhasePPythonVersionCheckRegression)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    passed = result.testsRun - len(result.failures) - len(result.errors)
    print(f"PHASE_P_PYTHON_VERSION_CHECK_REGRESSION={passed}/{result.testsRun}")
    raise SystemExit(0 if result.wasSuccessful() else 1)
