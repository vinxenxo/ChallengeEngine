import hashlib
import json
import tempfile
import unittest
from pathlib import Path
import sys
HERE = Path(__file__).resolve().parent
for candidate in (HERE, HERE.parent / 'tools'):
    if (candidate / 'c11e_e6_reuse_evidence_hydration_v1.py').is_file():
        sys.path.insert(0, str(candidate))
        break
import c11e_e6_reuse_evidence_hydration_v1 as mod

class HydrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self): self.tmp.cleanup()

    def write(self, rel, data=b'abc'):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
        return p

    def test_safe_relative_path(self):
        self.assertEqual(mod.safe_path(self.root, 'a/b.txt'), self.root / 'a/b.txt')

    def test_rejects_parent_traversal(self):
        with self.assertRaises(ValueError): mod.safe_path(self.root, '../outside')

    def test_rejects_absolute_path(self):
        with self.assertRaises(ValueError): mod.safe_path(self.root, '/tmp/outside')

    def test_rejects_windows_drive_path(self):
        with self.assertRaises(ValueError): mod.safe_path(self.root, 'C:\\temp\\x')

    def test_file_hash_pass(self):
        p = self.write('a.bin')
        digest = hashlib.sha256(b'abc').hexdigest()
        self.assertEqual(mod.check_file(self.root, 'a.bin', digest)['status'], 'PASS')

    def test_file_hash_mismatch(self):
        self.write('a.bin')
        self.assertEqual(mod.check_file(self.root, 'a.bin', '0'*64)['status'], 'SHA256_MISMATCH')

    def test_missing_file(self):
        self.assertEqual(mod.check_file(self.root, 'missing.bin', '0'*64)['status'], 'MISSING')

    def test_nested_path_hash_pair(self):
        refs = mod.paired_path_hash_refs({'outputs':[{'mp4_path':'a.mp4','mp4_sha256':'a'*64}]})
        self.assertEqual(len(refs), 1)
        self.assertEqual(refs[0][1], 'a.mp4')

    def test_generic_path_sha_pair(self):
        refs = mod.paired_path_hash_refs({'artifact':{'path':'x.dat','sha256':'b'*64}})
        self.assertEqual(len(refs), 1)

    def test_ignores_unpaired_path(self):
        self.assertEqual(mod.paired_path_hash_refs({'path':'x.dat'}), [])

    def test_nested_list_pairs(self):
        refs = mod.paired_path_hash_refs([{'path':'a','sha256':'a'*64},{'path':'b','sha256':'b'*64}])
        self.assertEqual(len(refs), 2)

    def test_find_json_by_exact_hash(self):
        p = self.write('artifacts/tests/c11e/x.json', b'{"x":1}')
        digest = hashlib.sha256(p.read_bytes()).hexdigest()
        self.assertEqual(mod.find_json_by_sha(self.root, digest, self.root/'artifacts/tests/c11e'), [p])

    def test_find_json_rejects_no_match(self):
        self.assertEqual(mod.find_json_by_sha(self.root, 'f'*64, self.root), [])

    def test_small_file_search_finds_report(self):
        p = self.write('artifacts/tests/c11e/report.md', b'report')
        digest = hashlib.sha256(p.read_bytes()).hexdigest()
        self.assertEqual(mod.find_small_file_by_sha(digest, self.root/'artifacts/tests/c11e'), [p])

    def test_report_hash_sidecar_format_is_sha256(self):
        self.assertRegex(mod.D9_RECEIPT_SHA, r'^[0-9a-f]{64}$')

    def test_expected_drill_matrix_is_six_rows(self):
        self.assertEqual(len(mod.DRILL_ROWS), 6)
        self.assertEqual(len({x[0] for x in mod.DRILL_ROWS}), 6)

    def test_empty_checkout_returns_blocked_report_without_mutation(self):
        report = mod.Audit(self.root).run()
        self.assertEqual(report['status'], 'BLOCKED_E6_REUSE_EVIDENCE_INCOMPLETE')
        self.assertGreater(report['failed_checks'], 0)
        self.assertFalse(report['governance']['source_checkout_mutated'])

    def test_no_git_or_media_process_imports(self):
        src = Path(mod.__file__).read_text(encoding='utf-8')
        for forbidden in ('import subprocess', 'subprocess.run', 'os.system', 'git status', 'git rev-parse'):
            self.assertNotIn(forbidden, src.lower())

if __name__ == '__main__': unittest.main(verbosity=2)
