#!/usr/bin/env python3
"""Phase T discovery report checks. Standard library only; run with a report JSON path."""
from __future__ import annotations
import hashlib, json, re, sys, unittest
from pathlib import Path

if len(sys.argv) != 2:
    print("USAGE: test_d_renderer_phase_t_authority_evidence_discovery_20261029.py <report.json>")
    raise SystemExit(2)
REPORT_PATH = Path(sys.argv[1]).resolve()
try:
    REPORT = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
except Exception as exc:
    print(f"PHASE_T_REPORT_LOAD_FAILED={type(exc).__name__}:{exc}")
    raise SystemExit(2)
sys.argv = [sys.argv[0]]
HEX64 = re.compile(r"^[0-9a-f]{64}$")

class PhaseTDiscoveryReportTests(unittest.TestCase):
    def test_01_schema_version(self): self.assertEqual(REPORT.get("schema_version"), "1.0.0")
    def test_02_phase(self): self.assertEqual(REPORT.get("phase"), "T")
    def test_03_status_allowed(self): self.assertIn(REPORT.get("status"), {"CANDIDATE_INVENTORY_READY_FOR_HUMAN_REVIEW", "INCOMPLETE_SCAN_REQUIRES_REMEDIATION"})
    def test_04_created_utc(self): self.assertRegex(REPORT.get("created_utc", ""), r"Z$")
    def test_05_scan_root_absolute(self): self.assertTrue(Path(REPORT.get("scan_root", "")).is_absolute())
    def test_06_scope_object(self): self.assertIsInstance(REPORT.get("scope"), dict)
    def test_07_worktree_only(self): self.assertIs(REPORT["scope"].get("working_tree_only"), True)
    def test_08_git_history_not_searched(self): self.assertIs(REPORT["scope"].get("git_history_searched"), False)
    def test_09_external_files_not_searched(self): self.assertIs(REPORT["scope"].get("external_files_searched"), False)
    def test_10_text_extensions_nonempty(self): self.assertGreater(len(REPORT["scope"].get("text_extensions", [])), 0)
    def test_11_exclusions_declared(self): self.assertGreater(len(REPORT["scope"].get("excluded_directory_names", [])), 0)
    def test_12_self_exclusions_declared(self): self.assertGreater(len(REPORT["scope"].get("self_excluded_prefixes", [])), 0)
    def test_13_text_size_cap(self): self.assertEqual(REPORT["scope"].get("maximum_text_file_bytes"), 4194304)
    def test_14_binary_content_limit(self): self.assertIs(REPORT["scope"].get("binary_contents_searched"), False)
    def test_15_archive_content_limit(self): self.assertIs(REPORT["scope"].get("archive_contents_searched"), False)
    def test_16_counts_object(self): self.assertIsInstance(REPORT.get("counts"), dict)
    def test_17_scan_counts_nonnegative(self): self.assertTrue(all(isinstance(v, int) and v >= 0 for v in REPORT["counts"].values()))
    def test_18_scanned_not_greater_seen(self): self.assertLessEqual(REPORT["counts"]["text_files_scanned"], REPORT["counts"]["files_seen"])
    def test_19_candidate_count_matches(self): self.assertEqual(REPORT["counts"]["candidate_files"], len(REPORT.get("candidates", [])))
    def test_20_unsearched_count_matches(self): self.assertEqual(REPORT["counts"]["unsearched_documents"], len(REPORT.get("unsearched_documents", [])))
    def test_21_scan_error_count_matches(self): self.assertEqual(REPORT["counts"]["scan_errors"], len(REPORT.get("scan_errors", [])))
    def test_22_scan_index_hash(self): self.assertRegex(REPORT.get("scan_index_sha256", ""), HEX64)
    def test_23_candidate_paths_unique(self):
        paths=[c.get("path") for c in REPORT.get("candidates", [])]; self.assertEqual(len(paths), len(set(paths)))
    def test_24_candidate_path_safe(self): self.assertTrue(all(isinstance(c.get("path"), str) and not c["path"].startswith("/") and ".." not in Path(c["path"]).parts for c in REPORT.get("candidates", [])))
    def test_25_candidate_hashes_valid(self): self.assertTrue(all(HEX64.fullmatch(c.get("sha256", "")) for c in REPORT.get("candidates", [])))
    def test_26_candidate_bytes_nonnegative(self): self.assertTrue(all(isinstance(c.get("bytes"), int) and c["bytes"] >= 0 for c in REPORT.get("candidates", [])))
    def test_27_candidates_not_authority(self): self.assertTrue(all(c.get("classification") == "UNREVIEWED_CANDIDATE_NOT_AUTHORITY" for c in REPORT.get("candidates", [])))
    def test_28_matches_are_lists(self): self.assertTrue(all(isinstance(c.get("matches"), list) for c in REPORT.get("candidates", [])))
    def test_29_match_line_numbers(self): self.assertTrue(all(isinstance(m.get("line"), int) and m["line"] >= 0 for c in REPORT.get("candidates", []) for m in c.get("matches", [])))
    def test_30_match_snippets_bounded(self): self.assertTrue(all(len(m.get("snippet", "")) <= 260 for c in REPORT.get("candidates", []) for m in c.get("matches", [])))
    def test_31_unsearched_paths_unique(self):
        paths=[d.get("path") for d in REPORT.get("unsearched_documents", [])]; self.assertEqual(len(paths), len(set(paths)))
    def test_32_unsearched_reasons_declared(self): self.assertTrue(all(d.get("reason") for d in REPORT.get("unsearched_documents", [])))
    def test_33_skipped_large_list(self): self.assertIsInstance(REPORT.get("skipped_large_files"), list)
    def test_34_errors_list(self): self.assertIsInstance(REPORT.get("scan_errors"), list)
    def test_35_clean_scan_status_consistent(self):
        if REPORT["scan_errors"]: self.assertEqual(REPORT["status"], "INCOMPLETE_SCAN_REQUIRES_REMEDIATION")
        else: self.assertEqual(REPORT["status"], "CANDIDATE_INVENTORY_READY_FOR_HUMAN_REVIEW")
    def test_36_source_pins_pass(self): self.assertEqual(len(REPORT.get("source_pins_verified", [])), 11); self.assertTrue(all(p.get("status") == "PASS" and HEX64.fullmatch(p.get("sha256", "")) for p in REPORT["source_pins_verified"]))
    def test_37_governance_renderer_off(self): self.assertEqual(REPORT["governance"].get("renderer"), "OFF")
    def test_38_governance_bindings_zero(self): self.assertEqual((REPORT["governance"].get("approved_bindings"), REPORT["governance"].get("approved_custom_data_bindings"), REPORT["governance"].get("approved_renderer_projection_bindings")), (0,0,0))
    def test_39_release_authority_none(self): self.assertEqual(REPORT["governance"].get("release_authority"), "NONE")
    def test_40_timing_and_scope_locks(self):
        conflicts=REPORT.get("timing_conflicts", []); self.assertEqual({x.get("challenge") for x in conflicts}, {"CHALLENGE_008","CHALLENGE_009"}); self.assertTrue(all(x.get("declared_total_duration_seconds")==11 and x.get("phase_duration_sum_seconds")==12 and x.get("status")=="BLOCKER_NO_CORRECTION_INFERRED" for x in conflicts)); self.assertIs(REPORT.get("no_global_absence_claim"), True)

if __name__ == "__main__":
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(PhaseTDiscoveryReportTests)
    result=unittest.TextTestRunner(stream=sys.stderr, verbosity=2).run(suite)
    if result.wasSuccessful():
        print("PHASE_T_AUTHORITY_DISCOVERY_TESTS=40/40")
        raise SystemExit(0)
    print(f"PHASE_T_AUTHORITY_DISCOVERY_TESTS={result.testsRun-result.failures.__len__()-result.errors.__len__()}/40")
    raise SystemExit(1)
