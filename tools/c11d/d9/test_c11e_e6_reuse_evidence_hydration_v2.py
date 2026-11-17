import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path
import sys
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import c11e_e6_reuse_evidence_hydration_v2 as mod

class HydrationV2Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "project"
        self.root.mkdir()

    def tearDown(self): self.tmp.cleanup()

    def write(self, rel, data=b"abc", base=None):
        p = (base or self.root) / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
        return p

    def test_safe_relative_path(self):
        self.assertEqual(mod.safe_path(self.root, "a/b.txt"), self.root / "a/b.txt")

    def test_rejects_parent_traversal(self):
        with self.assertRaises(ValueError): mod.safe_path(self.root, "../outside")

    def test_rejects_absolute_posix_outside(self):
        with self.assertRaises(ValueError): mod.safe_path(self.root, "/tmp/outside")

    def test_rejects_windows_drive_relative(self):
        with self.assertRaises(ValueError): mod.safe_path(self.root, "C:\\temp\\x")

    def test_windows_absolute_path_inside_root_normalizes(self):
        rel = mod.windows_absolute_to_relative(r"C:\Users\x\Project", r"C:\Users\x\Project\artifacts\a.json")
        self.assertEqual(rel, "artifacts/a.json")

    def test_windows_absolute_path_case_insensitive_normalizes(self):
        rel = mod.windows_absolute_to_relative(r"C:\Users\x\Project", r"c:\users\X\project\ARTIFACTS\a.json")
        self.assertEqual(rel.lower(), "artifacts/a.json")

    def test_windows_absolute_path_outside_root_rejected(self):
        with self.assertRaises(ValueError): mod.windows_absolute_to_relative(r"C:\Project", r"C:\Other\a.json")

    def test_windows_absolute_path_different_drive_rejected(self):
        with self.assertRaises(ValueError): mod.windows_absolute_to_relative(r"C:\Project", r"D:\Project\a.json")

    def test_windows_absolute_parent_traversal_rejected(self):
        with self.assertRaises(ValueError): mod.windows_absolute_to_relative(r"C:\Project", r"C:\Project\sub\..\a.json")

    def test_posix_absolute_inside_root_resolves(self):
        p = self.write("artifacts/a.json")
        self.assertEqual(mod.resolve_artifact_path(self.root, str(p)), p)

    def test_posix_absolute_outside_root_rejected(self):
        p = Path(self.tmp.name) / "outside.bin"
        p.write_bytes(b"x")
        with self.assertRaises(ValueError): mod.resolve_artifact_path(self.root, str(p))

    def test_file_hash_pass(self):
        p = self.write("a.bin")
        d = hashlib.sha256(b"abc").hexdigest()
        self.assertEqual(mod.check_file(self.root, "a.bin", d)["status"], "PASS")

    def test_file_hash_mismatch(self):
        self.write("a.bin")
        self.assertEqual(mod.check_file(self.root, "a.bin", "0"*64)["status"], "SHA256_MISMATCH")

    def test_missing_file(self):
        self.assertEqual(mod.check_file(self.root, "missing.bin", "0"*64)["status"], "MISSING")

    def test_receipt_relative_fallback_stays_inside_root(self):
        base = self.root / "artifacts" / "run"
        p = self.write("out/a.dat", b"x", base)
        d = hashlib.sha256(b"x").hexdigest()
        result = mod.check_file(self.root, "out/a.dat", d, base)
        self.assertEqual(result["status"], "PASS")

    def test_receipt_relative_parent_traversal_rejected(self):
        base = self.root / "artifacts" / "run"
        base.mkdir(parents=True)
        result = mod.check_file(self.root, "../../escape", "0"*64, base)
        self.assertEqual(result["status"], "INVALID_REFERENCE")

    def test_external_runtime_tool_file_hash_pass(self):
        ext = Path(self.tmp.name) / "ffmpeg.exe"
        ext.write_bytes(b"tool-binary")
        d = hashlib.sha256(b"tool-binary").hexdigest()
        result = mod.check_file(self.root, str(ext), d, allow_external_runtime=True, runtime_key="ffmpeg")
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["scope"], "EXTERNAL_RUNTIME_TOOL")

    def test_external_runtime_tool_name_mismatch_rejected(self):
        ext = Path(self.tmp.name) / "evil.exe"
        ext.write_bytes(b"tool-binary")
        d = hashlib.sha256(b"tool-binary").hexdigest()
        result = mod.check_file(self.root, str(ext), d, allow_external_runtime=True, runtime_key="ffmpeg")
        self.assertEqual(result["status"], "INVALID_REFERENCE")

    def test_external_artifact_not_allowed(self):
        ext = Path(self.tmp.name) / "anything.bin"
        ext.write_bytes(b"x")
        d = hashlib.sha256(b"x").hexdigest()
        result = mod.check_file(self.root, str(ext), d)
        self.assertEqual(result["status"], "INVALID_REFERENCE")

    def test_runtime_pointer_recognition_exact(self):
        self.assertTrue(mod.is_runtime_executable_pointer("$.runtime_tools.ffmpeg.path"))
        self.assertTrue(mod.is_runtime_executable_pointer("$.runtime_executables.python.path"))
        self.assertFalse(mod.is_runtime_executable_pointer("$.some_file.path"))

    def test_verify_nested_allows_project_root_absolute_artifact(self):
        p = self.write("assets/nested.bin", b"nested")
        digest = hashlib.sha256(b"nested").hexdigest()
        audit = mod.Audit(self.root)
        count = audit.verify_nested("FIXTURE", {"artifact": {"path": str(p), "sha256": digest}}, self.root)
        self.assertEqual(count, 1)
        self.assertEqual(audit.checks[0]["status"], "PASS")

    def test_verify_nested_allowlisted_external_runtime_hashes_actual_file(self):
        p = Path(self.tmp.name) / "ffprobe.exe"
        p.write_bytes(b"ffprobe")
        digest = hashlib.sha256(b"ffprobe").hexdigest()
        audit = mod.Audit(self.root)
        audit.verify_nested("FIXTURE", {"runtime_tools": {"ffprobe": {"path": str(p), "sha256": digest}}}, self.root)
        self.assertEqual(audit.checks[0]["status"], "PASS")
        self.assertEqual(audit.checks[0]["scope"], "EXTERNAL_RUNTIME_TOOL")

    def test_nested_path_hash_pair(self):
        refs = mod.paired_path_hash_refs({"outputs":[{"mp4_path":"a.mp4","mp4_sha256":"a"*64}]})
        self.assertEqual(len(refs), 1)
        self.assertEqual(refs[0][1], "a.mp4")

    def test_generic_path_sha_pair(self):
        refs = mod.paired_path_hash_refs({"artifact":{"path":"x.dat","sha256":"b"*64}})
        self.assertEqual(len(refs), 1)

    def test_ignores_unpaired_path(self):
        self.assertEqual(mod.paired_path_hash_refs({"path":"x.dat"}), [])

    def test_nested_list_pairs(self):
        refs = mod.paired_path_hash_refs([{"path":"a","sha256":"a"*64},{"path":"b","sha256":"b"*64}])
        self.assertEqual(len(refs), 2)

    def test_find_json_by_exact_hash(self):
        p = self.write("artifacts/tests/c11e/x.json", b'{"x":1}')
        d = hashlib.sha256(p.read_bytes()).hexdigest()
        self.assertEqual(mod.find_json_by_sha(self.root, d, self.root/"artifacts/tests/c11e"), [p])

    def test_find_json_rejects_no_match(self):
        self.assertEqual(mod.find_json_by_sha(self.root, "f"*64, self.root), [])

    def test_small_file_search_finds_report(self):
        p = self.write("artifacts/tests/c11e/report.md", b"report")
        d = hashlib.sha256(p.read_bytes()).hexdigest()
        self.assertEqual(mod.find_small_file_by_sha(d, self.root/"artifacts/tests/c11e"), [p])

    def test_report_hash_sidecar_format_is_sha256(self):
        self.assertRegex(mod.D9_RECEIPT_SHA, r"^[0-9a-f]{64}$")

    def test_expected_drill_matrix_is_six_rows(self):
        self.assertEqual(len(mod.DRILL_ROWS), 6)
        self.assertEqual(len({x[0] for x in mod.DRILL_ROWS}), 6)

    def test_ch004_historical_source_drift_is_not_auto_passed(self):
        self.assertIn("HISTORICAL_SOURCE_PIN_DIVERGENCE", (Path(mod.__file__).read_text(encoding="utf-8")))
        # Classification remains a failure status; no ignore/waiver branch exists.
        self.assertNotIn('status="PASS" if r.get("status") == "HISTORICAL_SOURCE_PIN_DIVERGENCE"', Path(mod.__file__).read_text(encoding="utf-8"))

    def test_empty_checkout_returns_blocked_report_without_mutation(self):
        report = mod.Audit(self.root).run()
        self.assertEqual(report["status"], "BLOCKED_E6_REUSE_EVIDENCE_INCOMPLETE")
        self.assertGreater(report["failed_checks"], 0)
        self.assertFalse(report["governance"]["source_checkout_mutated"])

    def test_no_git_or_media_process_imports(self):
        source = Path(mod.__file__).read_text(encoding="utf-8").lower()
        for forbidden in ("import subprocess", "subprocess.run", "os.system", "git status", "git rev-parse"):
            self.assertNotIn(forbidden, source)

if __name__ == "__main__": unittest.main(verbosity=2)
