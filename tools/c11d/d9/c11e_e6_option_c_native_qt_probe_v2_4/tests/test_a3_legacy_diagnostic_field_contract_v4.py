from __future__ import annotations
import copy, json, os, shutil, tempfile, unittest
from pathlib import Path
import importlib.util

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = PACKAGE_ROOT / "support/a3_lineage_adjudicator_v4.py"
SPEC = importlib.util.spec_from_file_location("_c11e_a3_test_adjudicator_v4", str(MODULE_PATH))
if SPEC is None or SPEC.loader is None: raise RuntimeError("A3_TEST_MODULE_SPEC_UNAVAILABLE")
MOD = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(MOD)
adjudicate_loop_a3, A3AdjudicationError = MOD.adjudicate_loop_a3, MOD.A3AdjudicationError
BRIDGE_REL, HIST_REL, CURR_REL, MODEL_REL = MOD.BRIDGE_REL, MOD.HIST_REL, MOD.CURR_REL, MOD.MODEL_REL
PROPOSAL_REL, DECISION_REL = MOD.PROPOSAL_REL, MOD.DECISION_REL
BRIDGE_SHA, HIST_SHA, CURR_SHA, MODEL_SHA = MOD.BRIDGE_SHA, MOD.HIST_SHA, MOD.CURR_SHA, MOD.MODEL_SHA
PROPOSAL_SHA, DECISION_SHA = MOD.PROPOSAL_SHA, MOD.DECISION_SHA
POINTER = MOD.POINTER

class A3LegacyDiagnosticFieldContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        configured = os.environ.get("C11E_PROJECT_ROOT")
        cls.source_root = Path(configured).resolve() if configured else Path("/mnt/data/C11E_E6_A3_V3_LOCAL_FIXTURE_PROJECT")
        cls.temp = Path(tempfile.mkdtemp(prefix="C11E_A3_V4_FIELDS_"))
        cls.root = cls.temp / "isolated_project_copy"; cls.root.mkdir()
        cls.rels = [BRIDGE_REL,HIST_REL,CURR_REL,MODEL_REL,PROPOSAL_REL,DECISION_REL]
        cls.originals = {}
        for rel in cls.rels:
            src=cls.source_root.joinpath(*rel.split("/")); data=src.read_bytes(); cls.originals[rel]=data
            dst=cls.root.joinpath(*rel.split("/")); dst.parent.mkdir(parents=True,exist_ok=True); dst.write_bytes(data)
        cls.bridge=json.loads((cls.root/BRIDGE_REL).read_text(encoding="utf-8"))
        cls.lineage=cls.bridge["review_manifest_lineage"]
        old_value,new_value=cls.lineage["old_pointer_value"],cls.lineage["new_pointer_value"]
        cls.active={
            "status":"PASS", "actual_manifest_differences":[POINTER],
            "transition":cls.lineage["installed_transition"],
            "identities":[
              {"path":BRIDGE_REL,"sha256":BRIDGE_SHA}, {"path":HIST_REL,"sha256":HIST_SHA},
              {"path":CURR_REL,"sha256":CURR_SHA}, {"path":MODEL_REL,"sha256":MODEL_SHA},
              {"path":PROPOSAL_REL,"sha256":PROPOSAL_SHA}, {"path":DECISION_REL,"sha256":DECISION_SHA}],
            # These assignments are byte-pinned to the original diagnostic producer.
            "old_pointer_expected":HIST_SHA,
            "old_pointer_actual":old_value,
            "bridge_old_pointer_value":old_value,
            "new_pointer_expected":MODEL_SHA,
            "new_pointer_actual":new_value,
            "bridge_new_pointer_value":new_value,
            "pointer_target_path":MODEL_REL,
        }
        cls.diag={"active_a3_lineage":cls.active,"issues":[
            "UNCLASSIFIED_CHECK_STATUS:PASS_SINGLE_POINTER_LINEAGE_RECONCILIATION",
            "RECEIPT_TOP_LEVEL_STATUS_CONTRADICTS_CHECKS",
            "A3_CHECK_NOT_PASS:PASS_SINGLE_POINTER_LINEAGE_RECONCILIATION"],
            "source_receipt_sha256":"5afc42ca84480ba1d025d288f2653d009e85af053fff5b62133e067a17dfb4be"}
        cls.loop={"checks":([{"id":f"check_{i}","status":"PASS"} for i in range(17)]+[
            {"id":"a3_lineage_single_pointer_reconciliation","status":"PASS_SINGLE_POINTER_LINEAGE_RECONCILIATION"}]),
            "check_count":18,"passed_checks":17,"failed_checks":0,
            "status":"PASS_LOOP_POLICY_DECISIONS_RECONCILED_NOT_COMPOSITOR_ACCEPTANCE"}
    @classmethod
    def tearDownClass(cls): shutil.rmtree(cls.temp,ignore_errors=True)
    def setUp(self):
        for rel,data in self.originals.items():
            p=self.root.joinpath(*rel.split("/"));p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
        self.diag=copy.deepcopy(type(self).diag);self.loop=copy.deepcopy(type(self).loop)
    def run_a3(self): return adjudicate_loop_a3(self.root,self.loop,self.diag)

    def test_01_actual_source_generated_field_shape_passes(self):
        r=self.run_a3()
        self.assertEqual(r["status"],"PASS_SPECIALIZED_A3_PASS_CLASSIFIED")
        self.assertEqual(r["structural_reconstruction"],"PASS_EXACTLY_ONE_POINTER_CHANGED")
        self.assertNotEqual(self.diag["active_a3_lineage"]["old_pointer_expected"],self.diag["active_a3_lineage"]["old_pointer_actual"])
        self.assertEqual(r["diagnostic_generator_sha256"],MOD.DIAGNOSTIC_GENERATOR_SHA)

    def test_02_old_expected_must_be_historical_whole_manifest_sha(self):
        self.diag["active_a3_lineage"]["old_pointer_expected"]=self.lineage["old_pointer_value"]
        with self.assertRaisesRegex(A3AdjudicationError,"A3_DIAGNOSTIC_FIELD_CONTRACT_MISMATCH:old_pointer_expected"): self.run_a3()

    def test_03_old_actual_must_be_historical_pointer_content(self):
        self.diag["active_a3_lineage"]["old_pointer_actual"]=HIST_SHA
        with self.assertRaisesRegex(A3AdjudicationError,"A3_DIAGNOSTIC_FIELD_CONTRACT_MISMATCH:old_pointer_actual"): self.run_a3()

    def test_04_new_expected_must_be_d98_model_file_sha(self):
        self.diag["active_a3_lineage"]["new_pointer_expected"]=CURR_SHA
        with self.assertRaisesRegex(A3AdjudicationError,"A3_DIAGNOSTIC_FIELD_CONTRACT_MISMATCH:new_pointer_expected"): self.run_a3()

    def test_05_new_actual_must_be_current_pointer_content(self):
        self.diag["active_a3_lineage"]["new_pointer_actual"]=CURR_SHA
        with self.assertRaisesRegex(A3AdjudicationError,"A3_DIAGNOSTIC_FIELD_CONTRACT_MISMATCH:new_pointer_actual"): self.run_a3()

    def test_06_old_bridge_value_must_equal_historical_pointer(self):
        self.diag["active_a3_lineage"]["bridge_old_pointer_value"]="0"*64
        with self.assertRaisesRegex(A3AdjudicationError,"A3_DIAGNOSTIC_FIELD_CONTRACT_MISMATCH:bridge_old_pointer_value"): self.run_a3()

    def test_07_new_bridge_value_must_equal_current_pointer(self):
        self.diag["active_a3_lineage"]["bridge_new_pointer_value"]="0"*64
        with self.assertRaisesRegex(A3AdjudicationError,"A3_DIAGNOSTIC_FIELD_CONTRACT_MISMATCH:bridge_new_pointer_value"): self.run_a3()

    def test_08_pointer_target_path_is_exact(self):
        self.diag["active_a3_lineage"]["pointer_target_path"]=CURR_REL
        with self.assertRaisesRegex(A3AdjudicationError,"A3_DIAGNOSTIC_FIELD_CONTRACT_MISMATCH:pointer_target_path"): self.run_a3()

    def test_09_duplicate_identity_path_is_rejected(self):
        self.diag["active_a3_lineage"]["identities"].append(copy.deepcopy(self.diag["active_a3_lineage"]["identities"][0]))
        with self.assertRaisesRegex(A3AdjudicationError,"A3_IDENTITY_ROW_COUNT_MISMATCH"): self.run_a3()

    def test_10_unapproved_manifest_change_is_rejected(self):
        p=self.root/CURR_REL;v=json.loads(p.read_text(encoding="utf-8"));v["unapproved_extra"]=True
        p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        with self.assertRaisesRegex(A3AdjudicationError,"A3_LIVE_IDENTITY_FILE_PIN_MISMATCH|A3_POSTIMAGE_DIFFERS_BEYOND_SINGLE_POINTER"):
            self.run_a3()

    def test_11_loop_receipt_counts_remain_exact(self):
        self.loop["failed_checks"]=1
        with self.assertRaisesRegex(A3AdjudicationError,"LOOP_V2_COUNT_CONTRACT_MISMATCH"): self.run_a3()

    def test_12_history_archive_bytes_are_immutable(self):
        p=self.root/HIST_REL;v=json.loads(p.read_text(encoding="utf-8"));v["source_lineage"][6]["sha256"]="0"*64
        p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        with self.assertRaises(A3AdjudicationError): self.run_a3()

    def test_13_generator_reference_pin_is_exact(self):
        self.assertEqual(MOD.verify_generator_provenance(),"90375a6c21550d67e6aa1f374d5e5c8dcd7c06b630c51b34ad83313fbb7b2fc2")

if __name__ == "__main__": unittest.main(verbosity=2)
