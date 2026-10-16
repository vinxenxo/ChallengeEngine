"""Focused regressions for the preparation-only geometric request-binding matrix V2."""
from __future__ import annotations
import ast, copy, json, sys, unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
if str(HERE) not in sys.path: sys.path.insert(0,str(HERE))
import d_renderer_visual_loop_request_scoped_binding_matrix_v2 as mod

class VisualLoopRequestBindingMatrixV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=mod.build_report(ROOT)

    def test_contract_and_all_direct_pins_match(self):
        c,cs,rs,pins=mod._load_contract(ROOT)
        self.assertEqual(len(pins),30)
        self.assertEqual(pins[0]["path"],"release/C11C_FREEZE_PACKAGE_MANIFEST.json")
        self.assertEqual(pins[0]["sha256"],mod.EXPECTED_MANIFEST)

    def test_all_five_geometric_grammars_have_source_bound_records(self):
        ids=[b["source_binding"]["resolved_identity"]["selected_grammar_id"] for b in self.report["bindings"]]
        self.assertEqual(ids,mod.EXPECTED_GRAMMARS)
        self.assertEqual(self.report["summary"]["v2_preparation_source_binding"],"5/5")

    def test_v1_fixed_scope_remains_unmodified_and_reported(self):
        self.assertEqual(self.report["summary"]["v1_canonical_binding"],"1/5")
        c=mod.read_json(ROOT,mod.CONTRACT_REL)
        self.assertFalse(c["authority"]["canonical_v1_mutated"])
        self.assertFalse(c["v1_core_reuse"]["v1_source_contract_modified"])

    def test_request_plan_hashes_are_unique_and_bound_to_parent_carrier(self):
        rows=self.report["bindings"]
        self.assertEqual(len({x["source_identity"]["request_hash"] for x in rows}),5)
        self.assertEqual(len({x["source_identity"]["plan_hash"] for x in rows}),5)
        self.assertEqual(self.report["summary"]["request_reference_joins"],"5/5")

    def test_all_45_policy_reference_pairs_are_metadata_only(self):
        rows=self.report["bindings"]
        self.assertEqual(sum(x["timing_review_reference"]["policy_reference_count"] for x in rows),45)
        self.assertEqual(len({x["timing_review_reference"]["selector_envelope_sha256"] for x in rows}),5)
        self.assertEqual(len({x["timing_review_reference"]["shared_policy_reference_set_sha256"] for x in rows}),1)
        for x in rows:
            self.assertFalse(x["timing_review_reference"]["policy_values_consumed"])
            self.assertFalse(x["timing_review_reference"]["policy_instructions_emitted"])
            self.assertFalse(x["timing_review_reference"]["timing_review_inheritance_approved"])

    def test_no_grammar_specific_payload_instance_is_claimed(self):
        for x in self.report["bindings"]:
            self.assertEqual(x["source_binding"]["source_class"],"FAMILY_CANONICAL_VISUAL_LOOP_DEFINITION_NOT_GRAMMAR_INSTANCE")
            self.assertFalse(x["source_binding"]["selected_grammar_materialized"])
            self.assertFalse(x["source_binding"]["exact_request_payload_instance_materialized"])
            self.assertIsNone(x["source_binding"]["payload_instance_id"])
            self.assertIsNone(x["source_binding"]["payload_instance_sha256"])
            self.assertFalse(x["readiness"]["request_scoped_visual_payload_instance_bound"])
            self.assertFalse(x["readiness"]["video_render_ready"])

    def test_every_binding_has_valid_self_hash(self):
        for x in self.report["bindings"]:
            self.assertEqual(x["binding_sha256"],mod.digest({k:v for k,v in x.items() if k!="binding_sha256"}))

    def test_report_hash_and_rebuild_validation(self):
        self.assertEqual(self.report["report_sha256"],mod.digest({k:v for k,v in self.report.items() if k!="report_sha256"}))
        self.assertTrue(mod.validate_report(self.report,ROOT))

    def test_report_is_deterministic(self):
        self.assertEqual(self.report,mod._build(ROOT))

    def test_governance_remains_closed_and_all_19_approvals_pending(self):
        g=self.report["governance"]
        self.assertEqual(g["approval_assertions_checked"],19)
        self.assertEqual(g["approvals_granted"],0)
        self.assertEqual(g["pending_approval_assertions"],19)
        for key in ("visual_loop_binding_matrix_v2_approved","canonical_request_selector_matrix_approved","exact_selector_payload_approved","timing_review_inheritance_approved","all_nine_shared_policy_sources_approved","candidate_io_contract_complete","d4_8_authorized","candidate_input_admissible","request_persisted","payload_materialized","renderer_native_input_emitted","renderer_dispatch_invoked","media_created","c11c_source_mutation"):
            self.assertFalse(g[key])
        self.assertEqual(g["renderer"],"OFF");self.assertEqual(g["D4.8"],"BLOCKED");self.assertEqual(g["release_authority"],"NONE")

    def test_summary_cannot_promote_candidate_or_materialization(self):
        s=self.report["summary"]
        self.assertEqual(s["selected_grammar_payload_instances_bound"],"0/5")
        self.assertEqual(s["payloads_materialized"],0)
        self.assertFalse(s["candidate_input_admissible"])

    def test_report_schema_is_strict(self):
        schema=mod.read_json(ROOT,mod.REPORT_SCHEMA_REL)
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(set(schema["required"]),set(schema["properties"]))
        try:
            from jsonschema import Draft202012Validator
            Draft202012Validator.check_schema(schema)
            Draft202012Validator(schema).validate(self.report)
        except ImportError:
            self.assertEqual(set(self.report),set(schema["required"]))

    def test_unknown_top_level_report_field_rejected(self):
        changed=copy.deepcopy(self.report);changed["payload_materialized"]=True
        self.assertNotEqual(changed,self.report)
        schema=mod.read_json(ROOT,mod.REPORT_SCHEMA_REL)
        try:
            from jsonschema import Draft202012Validator
            self.assertTrue(list(Draft202012Validator(schema).iter_errors(changed)))
        except ImportError:
            self.assertNotEqual(set(changed),set(schema["required"]))

    def test_forged_request_identity_is_rejected_by_canonical_rebuild(self):
        changed=copy.deepcopy(self.report);changed["bindings"][2]["source_identity"]["request_hash"]="0"*64
        changed["bindings"][2]["binding_sha256"]=mod.digest({k:v for k,v in changed["bindings"][2].items() if k!="binding_sha256"})
        changed["report_sha256"]=mod.digest({k:v for k,v in changed.items() if k!="report_sha256"})
        with self.assertRaises(mod.MatrixAuditError):mod.validate_report(changed,ROOT)

    def test_forged_selector_reference_digest_is_rejected(self):
        changed=copy.deepcopy(self.report);changed["bindings"][3]["timing_review_reference"]["selector_envelope_sha256"]="0"*64
        changed["bindings"][3]["binding_sha256"]=mod.digest({k:v for k,v in changed["bindings"][3].items() if k!="binding_sha256"})
        changed["report_sha256"]=mod.digest({k:v for k,v in changed.items() if k!="report_sha256"})
        with self.assertRaises(mod.MatrixAuditError):mod.validate_report(changed,ROOT)

    def test_readiness_escalation_is_rejected(self):
        changed=copy.deepcopy(self.report);changed["bindings"][0]["readiness"]["video_render_ready"]=True
        changed["bindings"][0]["binding_sha256"]=mod.digest({k:v for k,v in changed["bindings"][0].items() if k!="binding_sha256"})
        changed["report_sha256"]=mod.digest({k:v for k,v in changed.items() if k!="report_sha256"})
        with self.assertRaises(mod.MatrixAuditError):mod.validate_report(changed,ROOT)

    def test_binding_sha_mutation_rejected(self):
        changed=copy.deepcopy(self.report);changed["bindings"][1]["binding_sha256"]="0"*64
        changed["report_sha256"]=mod.digest({k:v for k,v in changed.items() if k!="report_sha256"})
        with self.assertRaises(mod.MatrixAuditError):mod.validate_report(changed,ROOT)

    def test_report_hash_mutation_rejected(self):
        changed=copy.deepcopy(self.report);changed["report_sha256"]="0"*64
        with self.assertRaises(mod.MatrixAuditError):mod.validate_report(changed,ROOT)

    def test_contract_schema_is_strict(self):
        schema=mod.read_json(ROOT,mod.CONTRACT_SCHEMA_REL)
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(set(schema["required"]),set(schema["properties"]))

    def test_source_binding_uses_current_v1_core_implementation(self):
        contract=mod.read_json(ROOT,mod.CONTRACT_REL)
        path=ROOT/contract["v1_core_reuse"]["implementation_path"]
        pin={x["path"]:x["sha256"] for x in contract["source_lineage"]}[contract["v1_core_reuse"]["implementation_path"]]
        self.assertEqual(mod.file_sha(path),pin)

    def test_no_process_or_render_dispatch_capability(self):
        src=(HERE/"d_renderer_visual_loop_request_scoped_binding_matrix_v2.py").read_text(encoding="utf-8")
        tree=ast.parse(src);forbidden_modules={"subprocess","socket","multiprocessing","ffmpeg","godot"};forbidden_calls={"write_text","write_bytes","Popen","system","startfile","check_call","check_output","dispatch","render_video"}
        for n in ast.walk(tree):
            if isinstance(n,ast.Import):self.assertFalse(any(a.name.split('.')[0] in forbidden_modules for a in n.names))
            elif isinstance(n,ast.ImportFrom):self.assertNotIn((n.module or '').split('.')[0],forbidden_modules)
            elif isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute):self.assertNotIn(n.func.attr,forbidden_calls)

    def test_no_input_or_output_artifact_paths_are_created(self):
        for x in self.report["bindings"]:
            self.assertIsNone(x["source_binding"]["payload_output_path"])
            self.assertIsNone(x["execution_boundary"]["output_artifact_path"])
            self.assertFalse(x["execution_boundary"]["media_output_created"])
        self.assertFalse(self.report["governance"]["request_persisted"])

if __name__=="__main__":
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(VisualLoopRequestBindingMatrixV2Tests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
