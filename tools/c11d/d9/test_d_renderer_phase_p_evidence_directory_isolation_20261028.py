#!/usr/bin/env python3
"""Read-only static regression for Phase P evidence-directory isolation."""
from __future__ import annotations
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUNNER = ROOT / "tools" / "c11d" / "d9" / "run_d_renderer_phase_p_source_value_frame_value_provenance_20261028.ps1"

class PhasePEvidenceDirectoryIsolationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not RUNNER.is_file():
            raise AssertionError(f"Required runner not found: {RUNNER}")
        cls.source = RUNNER.read_text(encoding="utf-8-sig")

    def test_audit_directory_declared_once_under_parent(self) -> None:
        self.assertEqual(len(re.findall(r"(?im)^\s*\$auditDir\s*=\s*Join-Path\s+\$evidenceDir\s+'audit'\s*$", self.source)), 1)

    def test_report_path_is_under_audit_directory(self) -> None:
        self.assertEqual(len(re.findall(r"(?im)^\s*\$reportPath\s*=\s*Join-Path\s+\$auditDir\s+'phase_p_provenance_report\.json'\s*$", self.source)), 1)
        self.assertEqual(re.findall(r"(?im)^.*\$reportPath\s*=\s*Join-Path\s+\$evidenceDir\b.*$", self.source), [])

    def test_actual_cli_argument_uses_audit_directory(self) -> None:
        self.assertEqual(len(re.findall(r"(?im)^\$args\s*=\s*@\([^\r\n]*--evidence-dir[^\r\n]*\$auditDir[^\r\n]*\)$", self.source)), 1)
        self.assertEqual(re.findall(r"(?im)^\$args\s*=\s*@\([^\r\n]*--evidence-dir[^\r\n]*\$evidenceDir[^\r\n]*\)$", self.source), [])
        self.assertNotIn("--output-dir", self.source)

    def test_runner_logs_stay_in_parent_directory(self) -> None:
        self.assertEqual(len(re.findall(r"(?im)^\$runnerOut\s*=\s*Join-Path\s+\$evidenceDir\s+'runner\.stdout\.txt'\s*$", self.source)), 1)
        self.assertEqual(len(re.findall(r"(?im)^\$runnerErr\s*=\s*Join-Path\s+\$evidenceDir\s+'runner\.stderr\.txt'\s*$", self.source)), 1)

    def test_audit_subdirectory_is_not_precreated(self) -> None:
        self.assertEqual(re.findall(r"(?im)^\s*New-Item\s+-ItemType\s+Directory\s+-Path\s+\$auditDir\b.*$", self.source), [])

    def test_audit_receipt_is_checked_after_process_and_report_path_is_dynamic(self) -> None:
        arg = self.source.index("'--evidence-dir'")
        process = self.source.index('$runProc = Start-Process')
        report = self.source.index('$reportPath = Join-Path $auditDir')
        self.assertLess(arg, process)
        self.assertLess(process, report)
        self.assertIn("'phase_p_provenance_report.json'", self.source)

if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(PhasePEvidenceDirectoryIsolationTests))
    passed = result.testsRun - len(result.failures) - len(result.errors)
    print(f"PHASE_P_EVIDENCE_DIRECTORY_ISOLATION_REGRESSION={passed}/{result.testsRun}")
    raise SystemExit(0 if result.wasSuccessful() else 1)
