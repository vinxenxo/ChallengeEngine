from __future__ import annotations
import copy, hashlib, json, unittest
from pathlib import Path
import jsonschema
import d_renderer_visual_loop_timing_review_request_bound_reference_carrier as audit
ROOT=Path(__file__).resolve().parents[3]
class RequestBoundReferenceCarrierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract=json.loads((ROOT/audit.CONTRACT_REL).read_text(encoding="utf-8"))
        cls.schema=json.loads((ROOT/audit.SCHEMA_REL).read_text(encoding="utf-8"))
        cls.report_schema=json.loads((ROOT/audit.REPORT_SCHEMA_REL).read_text(encoding="utf-8"))
        cls.report=audit.build_report(ROOT)
    def test_contract_schema_is_strict_draft_2020_12(self):
        self.assertEqual(self.schema["$schema"],"https://json-schema.org/draft/2020-12/schema")
        self.assertFalse(self.schema["additionalProperties"])
        jsonschema.Draft202012Validator(self.schema).validate(self.contract)
    def test_report_schema_is_strict_and_validates(self):
        self.assertFalse(self.report_schema["additionalProperties"])
        jsonschema.Draft202012Validator(self.report_schema).validate(self.report)
    def test_frozen_c11c_manifest_is_first_exact_pin(self):
        self.assertEqual(self.contract["source_lineage"][0]["path"],"release/C11C_FREEZE_PACKAGE_MANIFEST.json")
        self.assertEqual(hashlib.sha256((ROOT/"release/C11C_FREEZE_PACKAGE_MANIFEST.json").read_bytes()).hexdigest(),self.contract["source_lineage"][0]["sha256"])
    def test_source_pins_are_unique_and_current(self):
        rows=self.contract["source_lineage"]
        self.assertEqual(len(rows),22)
        self.assertEqual(len({r["path"] for r in rows}),22)
        for row in rows:self.assertEqual(hashlib.sha256((ROOT/row["path"]).read_bytes()).hexdigest(),row["sha256"],row["path"])
    def test_all_five_request_plans_join(self):
        self.assertEqual(self.report["summary"]["request_plans"],"5/5")
        self.assertEqual(self.report["summary"]["request_identity_joins"],"5/5")
    def test_five_request_hashes_are_distinct(self):
        vals=[r["request_identity"]["request_hash"] for r in self.report["relations"]]
        self.assertEqual(len(set(vals)),5)
    def test_five_plan_hashes_are_distinct(self):
        vals=[r["request_identity"]["plan_hash"] for r in self.report["relations"]]
        self.assertEqual(len(set(vals)),5)
    def test_all_five_selectors_are_in_canonical_order(self):
        self.assertEqual([r["selector"]["grammar_id"] for r in self.report["relations"]],["harmonic_membrane","interference_plane","parametric_ribbon","lattice_wave","orbital_wave"])
    def test_canonical_request_identity_matches_reference_selector(self):
        for r in self.report["relations"]:
            self.assertTrue(r["join_checks"]["selector_matches_canonical_request"])
            self.assertTrue(r["join_checks"]["selector_matches_reference_envelope"])
    def test_all_forty_five_policy_reference_pairs_are_metadata_only(self):
        self.assertEqual(self.report["summary"]["policy_reference_pairs"],"45/45")
        for r in self.report["relations"]:
            self.assertEqual(r["reference_identity"]["reference_count"],9)
            self.assertFalse(r["reference_identity"]["source_envelope_request_bound"])
            self.assertTrue(r["join_checks"]["metadata_only_join"])
    def test_shared_reference_digest_is_common(self):
        self.assertEqual(self.report["summary"]["shared_policy_digest_unique_count"],1)
    def test_selector_envelope_digests_are_unique(self):
        vals=[r["reference_identity"]["selector_envelope_sha256"] for r in self.report["relations"]]
        self.assertEqual(len(set(vals)),5)
    def test_existing_canonical_binding_scope_is_unchanged(self):
        self.assertEqual(self.report["summary"]["canonical_binding"],"1/5")
        self.assertEqual(self.report["summary"]["blocked_by_fixed_v1_scope"],"4/4")
    def test_no_policy_approval_is_granted(self):
        self.assertEqual(self.report["summary"]["approval_assertions_checked"],19)
        self.assertEqual(self.report["summary"]["approvals_granted"],0)
        self.assertFalse(self.report["governance"]["timing_review_inheritance_approved"])
    def test_request_and_plan_remain_unmodified(self):
        for r in self.report["relations"]:
            self.assertFalse(r["locks"]["canonical_request_mutated"])
            self.assertFalse(r["locks"]["canonical_plan_mutated"])
            self.assertFalse(r["locks"]["source_envelope_mutated"])
    def test_no_policy_values_or_renderer_instructions_are_consumed(self):
        for r in self.report["relations"]:
            self.assertFalse(r["locks"]["policy_values_consumed"])
            self.assertFalse(r["locks"]["renderer_instructions_emitted"])
            self.assertFalse(r["locks"]["payload_instance_bound"])
    def test_candidate_input_never_becomes_admissible(self):
        self.assertFalse(self.report["summary"]["candidate_input_admissible"])
        for r in self.report["relations"]:self.assertFalse(r["locks"]["candidate_input_admissible"])
    def test_renderer_and_release_authority_stay_locked(self):
        g=self.report["governance"]
        self.assertEqual(g["renderer"],"OFF");self.assertEqual(g["D4.8"],"BLOCKED");self.assertEqual(g["release_authority"],"NONE")
        self.assertFalse(g["media_created"]);self.assertEqual(g["D9.10"],"PREPARE_ONLY");self.assertEqual(g["D9.17"],"BLOCKED_NO_GO")
    def test_report_self_hash_is_exact(self):
        body={k:v for k,v in self.report.items() if k!="report_sha256"}
        raw=json.dumps(body,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False).encode()
        self.assertEqual(hashlib.sha256(raw).hexdigest(),self.report["report_sha256"])
    def test_tampered_request_hash_rejected(self):
        altered=copy.deepcopy(self.report);altered["relations"][0]["request_identity"]["request_hash"]="0"*64
        with self.assertRaises(audit.RequestBoundReferenceCarrierError):audit.validate_report(altered,ROOT)
    def test_tampered_approval_state_rejected(self):
        altered=copy.deepcopy(self.report);altered["governance"]["timing_review_inheritance_approved"]=True
        with self.assertRaises(audit.RequestBoundReferenceCarrierError):audit.validate_report(altered,ROOT)
    def test_tampered_shared_reference_digest_rejected(self):
        altered=copy.deepcopy(self.report);altered["relations"][1]["reference_identity"]["shared_reference_set_sha256"]="f"*64
        with self.assertRaises(audit.RequestBoundReferenceCarrierError):audit.validate_report(altered,ROOT)
    def test_tampered_scope_admission_rejected(self):
        altered=copy.deepcopy(self.report);altered["summary"]["candidate_input_admissible"]=True
        with self.assertRaises(audit.RequestBoundReferenceCarrierError):audit.validate_report(altered,ROOT)
    def test_contract_cannot_self_approve_or_activate_v2(self):
        self.assertFalse(self.contract["authority"]["canonical_binding_v2_activated"])
        self.assertFalse(self.contract["authority"]["policy_approval_granted"])
        for v in self.contract["approval_gate"].values():
            if isinstance(v,bool):self.assertFalse(v)
    def test_source_envelope_request_bound_field_remains_false(self):
        for r in self.report["relations"]:self.assertFalse(r["reference_identity"]["source_envelope_request_bound"])
    def test_governance_locks_are_exact(self):
        self.assertEqual(self.report["governance"],{
          "timing_review_inheritance_approved":False,"canonical_request_selector_matrix_approved":False,"exact_selector_payload_approved":False,
          "all_shared_policy_sources_approved":False,"candidate_io_contract_complete":False,"d4_8_authorized":False,
          "request_persisted":False,"payload_materialized":False,"renderer_native_input_emitted":False,"renderer_dispatch_invoked":False,
          "media_created":False,"c11c_source_mutation":False,"renderer":"OFF","D4.8":"BLOCKED","release_authority":"NONE",
          "D9.10":"PREPARE_ONLY","D9.17":"BLOCKED_NO_GO"})
if __name__=='__main__':unittest.main(verbosity=2)
