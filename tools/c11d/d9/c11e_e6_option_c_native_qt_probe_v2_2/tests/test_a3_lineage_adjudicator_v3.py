from __future__ import annotations
import copy, json, os, shutil, sys, tempfile, unittest
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))
from support.a3_lineage_adjudicator_v3 import (
    adjudicate_loop_a3, A3AdjudicationError, BRIDGE_REL, HIST_REL, CURR_REL,
    MODEL_REL, BRIDGE_SHA, HIST_SHA, CURR_SHA, MODEL_SHA, POINTER,
)

class A3DomainSeparationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        configured_root = os.environ.get("C11E_PROJECT_ROOT")
        cls.source_root = Path(configured_root).resolve() if configured_root else PACKAGE_ROOT.parents[3]
        cls.temp = Path(tempfile.mkdtemp(prefix="C11E_A3_V3_TEST_"))
        cls.root = cls.temp / "isolated_project_copy"
        cls.root.mkdir()
        cls.rels = [
            BRIDGE_REL, HIST_REL, CURR_REL, MODEL_REL,
            "definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json",
            "docs/current/e/C11E_E4B_OPERATOR_POLICY_DECISION_RECORD_20261106_V1.json",
        ]
        cls.originals = {}
        for rel in cls.rels:
            source = cls.source_root.joinpath(*rel.split("/"))
            if not source.is_file():
                raise RuntimeError("A3_TEST_SOURCE_MISSING:" + rel)
            data = source.read_bytes()
            cls.originals[rel] = data
            target = cls.root.joinpath(*rel.split("/"))
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        cls.bridge = json.loads((cls.root/BRIDGE_REL).read_text(encoding="utf-8"))
        cls.lineage = cls.bridge["review_manifest_lineage"]
        old_value = cls.lineage["old_pointer_value"]
        new_value = cls.lineage["new_pointer_value"]
        cls.identity_rows = [
            {"path": BRIDGE_REL, "sha256": BRIDGE_SHA},
            {"path": HIST_REL, "sha256": HIST_SHA},
            {"path": CURR_REL, "sha256": CURR_SHA},
            {"path": MODEL_REL, "sha256": MODEL_SHA},
        ]
        cls.active = {
            "status": "PASS",
            "actual_manifest_differences": [POINTER],
            "transition": cls.lineage["installed_transition"],
            "identities": cls.identity_rows,
            "old_pointer_expected": HIST_SHA,
            "old_pointer_actual": HIST_SHA,
            "new_pointer_expected": CURR_SHA,
            "new_pointer_actual": CURR_SHA,
            "bridge_old_pointer_value": old_value,
            "bridge_new_pointer_value": new_value,
        }
        cls.diag = {
            "active_a3_lineage": cls.active,
            "issues": [
                "UNCLASSIFIED_CHECK_STATUS:PASS_SINGLE_POINTER_LINEAGE_RECONCILIATION",
                "RECEIPT_TOP_LEVEL_STATUS_CONTRADICTS_CHECKS",
                "A3_CHECK_NOT_PASS:PASS_SINGLE_POINTER_LINEAGE_RECONCILIATION",
            ],
            "source_receipt_sha256": "5afc42ca84480ba1d025d288f2653d009e85af053fff5b62133e067a17dfb4be",
        }
        cls.loop = {
            "checks": ([{"id": f"check_{i}", "status": "PASS"} for i in range(17)] + [
                {"id": "a3_lineage_single_pointer_reconciliation", "status": "PASS_SINGLE_POINTER_LINEAGE_RECONCILIATION"}
            ]),
            "check_count": 18, "passed_checks": 17, "failed_checks": 0,
            "status": "PASS_LOOP_POLICY_DECISIONS_RECONCILED_NOT_COMPOSITOR_ACCEPTANCE",
        }

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.temp, ignore_errors=True)

    def setUp(self):
        # Each test begins from verified immutable bytes in a scratch copy; never writes to ProjectRoot.
        for rel, data in self.originals.items():
            p = self.root.joinpath(*rel.split("/")); p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(data)
        self.diag = copy.deepcopy(type(self).diag)
        self.loop_case = copy.deepcopy(type(self).loop)

    def run_adjudicator(self):
        return adjudicate_loop_a3(self.root, self.loop_case, self.diag)

    def test_01_manifest_sha_domain_passes_and_is_reported(self):
        result = self.run_adjudicator()
        self.assertEqual(result["normalized_pass_checks"], 18)
        self.assertEqual(result["legacy_diagnostic_hash_domains"], {
            "old_expected_actual": "WHOLE_MANIFEST_SHA256",
            "new_expected_actual": "WHOLE_MANIFEST_SHA256",
        })
        self.assertEqual(result["structural_reconstruction"], "PASS_EXACTLY_ONE_POINTER_CHANGED")

    def test_02_pointer_sha_domain_also_passes_when_pair_agrees(self):
        a = self.diag["active_a3_lineage"]
        a["old_pointer_expected"] = a["old_pointer_actual"] = self.lineage["old_pointer_value"]
        a["new_pointer_expected"] = a["new_pointer_actual"] = self.lineage["new_pointer_value"]
        result = self.run_adjudicator()
        self.assertEqual(result["legacy_diagnostic_hash_domains"], {
            "old_expected_actual": "JSON_POINTER_VALUE_SHA256",
            "new_expected_actual": "JSON_POINTER_VALUE_SHA256",
        })

    def test_03_expected_actual_disagreement_is_blocked(self):
        self.diag["active_a3_lineage"]["old_pointer_actual"] = self.lineage["old_pointer_value"]
        with self.assertRaisesRegex(A3AdjudicationError, "A3_LEGACY_DIAGNOSTIC_EXPECTED_ACTUAL_MISMATCH:old"):
            self.run_adjudicator()

    def test_04_hash_outside_both_pinned_domains_is_blocked(self):
        self.diag["active_a3_lineage"]["new_pointer_expected"] = self.diag["active_a3_lineage"]["new_pointer_actual"] = "0" * 64
        with self.assertRaisesRegex(A3AdjudicationError, "A3_LEGACY_DIAGNOSTIC_HASH_OUTSIDE_PINNED_DOMAINS:new"):
            self.run_adjudicator()

    def test_05_explicit_old_bridge_pointer_must_match(self):
        self.diag["active_a3_lineage"]["bridge_old_pointer_value"] = "0" * 64
        with self.assertRaisesRegex(A3AdjudicationError, "A3_POINTER_DOMAIN_VALUE_MISMATCH:bridge_old_pointer_value"):
            self.run_adjudicator()

    def test_06_absent_optional_bridge_echo_fields_do_not_replace_source_checks(self):
        a = self.diag["active_a3_lineage"]
        a.pop("bridge_old_pointer_value")
        a.pop("bridge_new_pointer_value")
        result = self.run_adjudicator()
        self.assertEqual(result["structural_reconstruction"], "PASS_EXACTLY_ONE_POINTER_CHANGED")

    def test_07_extra_manifest_change_is_blocked(self):
        current_path = self.root/CURR_REL
        current = json.loads(current_path.read_text(encoding="utf-8")); current["extra_unapproved_test_field"] = True
        current_path.write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        with self.assertRaises(A3AdjudicationError):
            self.run_adjudicator()

    def test_08_specialized_status_requires_exact_counts(self):
        self.loop_case["failed_checks"] = 1
        with self.assertRaisesRegex(A3AdjudicationError, "LOOP_V2_COUNT_CONTRACT_MISMATCH"):
            self.run_adjudicator()

    def test_09_historical_pointer_must_match_bridge_value(self):
        hist_path = self.root/HIST_REL
        hist = json.loads(hist_path.read_text(encoding="utf-8")); hist["source_lineage"][6]["sha256"] = "0" * 64
        hist_path.write_text(json.dumps(hist, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        with self.assertRaises(A3AdjudicationError):
            self.run_adjudicator()

if __name__ == "__main__":
    unittest.main(verbosity=2)
