#!/usr/bin/env python3
"""Regression tests for Phase AA audit status and preservation of governance locks."""
import argparse, json, unittest
from pathlib import Path
from verify_d_renderer_phase_aa_pre_render_readiness_20261029_v1 import verify, EXPECTED_DECISIONS, REQUIRED_LOCKS, REQUIRED_FIELDS

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
class PhaseAATests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=cls.args
        cls.z=load(p.phase_z_json); cls.pz=load(p.phase_z_packet_json); cls.r=load(p.phase_aa_result_json); cls.m=load(p.phase_aa_matrix_json); cls.pa=load(p.phase_aa_packet_json)
    def test_01_phase_z_is_prior_source(self): self.assertEqual(self.z['phase'],'Z')
    def test_02_phase_z_has_nine_decisions(self): self.assertEqual(self.z['decision_count'],9)
    def test_03_exact_decision_order(self): self.assertEqual([x['decision_id'] for x in self.z['decisions']],EXPECTED_DECISIONS)
    def test_04_packet_order_preserved(self): self.assertEqual([x['decision_id'] for x in self.pa['decisions']],EXPECTED_DECISIONS)
    def test_05_r01_to_r07_not_adopted(self): self.assertTrue(all(x['status']=='NOT_ADOPTED_KEEP_BLOCKED' for x in self.z['decisions'][:7]))
    def test_06_r08_blocked(self): self.assertEqual(self.z['decisions'][7]['status'],'BLOCKED_EXPLICIT_AUTHORITY_REQUIRED')
    def test_07_r09_blocked(self): self.assertEqual(self.z['decisions'][8]['status'],'BLOCKED_EXPLICIT_AUTHORITY_REQUIRED')
    def test_08_timing_conflict_stays_explicit(self): self.assertIn('11',self.z['decisions'][7]['evidence_assessment']); self.assertIn('12',self.z['decisions'][7]['evidence_assessment'])
    def test_09_phase_aa_status_is_audit_pass_only(self): self.assertEqual(self.r['status'],'PASS_PRE_RENDER_AUDIT_COMPLETE_RENDER_READINESS_BLOCKED')
    def test_10_operator_evidence_not_complete(self): self.assertFalse(self.r['checks']['decision_evidence_completed'])
    def test_11_required_fields_not_present(self): self.assertFalse(self.r['checks']['all_required_authority_fields_present'])
    def test_12_authority_adjudication_pending(self): self.assertEqual(self.r['checks']['authority_adjudication'],'PENDING')
    def test_13_render_readiness_blocked(self): self.assertEqual(self.r['checks']['pre_render_readiness'],'BLOCKED')
    def test_14_render_execution_not_authorized(self): self.assertFalse(self.r['checks']['render_execution_authorized'])
    def test_15_renderer_activation_not_authorized(self): self.assertFalse(self.r['checks']['renderer_activation_authorized'])
    def test_16_godot_not_invoked(self): self.assertFalse(self.r['checks']['godot_invoked'])
    def test_17_runtime_not_reexecuted(self): self.assertFalse(self.r['checks']['runtime_reexecuted'])
    def test_18_worksheet_unsigned_pending(self): self.assertEqual(self.pa['status'],'BLOCKED_REQUIRED_AUTHORITY_EVIDENCE_PENDING')
    def test_19_required_field_contract_matches_phase_z(self): self.assertEqual(self.pa['required_fields'],self.pz['required_fields'])
    def test_20_all_rows_mark_required_fields_missing(self): self.assertTrue(all(x['required_fields_missing']==REQUIRED_FIELDS for x in self.pa['decisions']))
    def test_21_no_selected_options_invented(self): self.assertTrue(all(x['selected_option'] is None for x in self.pa['decisions']))
    def test_22_no_policy_text_invented(self): self.assertTrue(all(x['exact_policy_text'] is None for x in self.pa['decisions']))
    def test_23_no_approver_invented(self): self.assertTrue(all(x['named_approving_authority'] is None and x['approving_role'] is None for x in self.pa['decisions']))
    def test_24_no_provenance_invented(self): self.assertTrue(all(x['approval_provenance_or_signature_ref'] is None for x in self.pa['decisions']))
    def test_25_incomplete_means_blocked(self): self.assertTrue(all(x['result_if_incomplete']=='KEEP_BLOCKED_NO_POLICY_ADOPTION' for x in self.pa['decisions']))
    def test_26_full_hard_lock_contract(self): self.assertEqual(self.r['hard_locks'],REQUIRED_LOCKS)
    def test_27_matrix_hard_locks_match(self): self.assertEqual(self.m['hard_locks'],REQUIRED_LOCKS)
    def test_28_candidate_input_not_admissible(self): self.assertFalse(REQUIRED_LOCKS['candidate_input_admissible'])
    def test_29_seed_domains_incomplete(self): self.assertFalse(REQUIRED_LOCKS['seed_domains_complete_for_candidate_input'])
    def test_30_master_seed_not_adopted(self): self.assertEqual(REQUIRED_LOCKS['master_seed'],'NOT_ADOPTED')
    def test_31_binding_counts_zero(self): self.assertEqual([REQUIRED_LOCKS[x] for x in ['approved_bindings','approved_custom_data_bindings','approved_renderer_projection_bindings']],[0,0,0])
    def test_32_d917_no_go(self): self.assertEqual(REQUIRED_LOCKS['D9.17'],'BLOCKED_NO_GO')
    def test_33_d10_blocked(self): self.assertEqual(REQUIRED_LOCKS['D10'],'BLOCKED_FOR_PROMOTION')
    def test_34_baseline_authority_not_granted(self): self.assertEqual(REQUIRED_LOCKS['release_authority'],'NONE'); self.assertEqual(REQUIRED_LOCKS['baseline_approval'],'MISSING')
    def test_35_renderer_off(self): self.assertEqual(REQUIRED_LOCKS['renderer'],'OFF')
    def test_36_media_payload_not_created(self): self.assertFalse(REQUIRED_LOCKS['media_created']); self.assertFalse(REQUIRED_LOCKS['payload_materialized'])
    def test_37_matrix_all_expected_gates(self): self.assertEqual(len(self.m['gates']),10)
    def test_38_render_acceptance_prepare_only(self): self.assertEqual(next(g for g in self.m['gates'] if g['gate_id']=='AA-08-ISOLATED-RENDER-ACCEPTANCE')['status'],'PREPARE_ONLY')
    def test_39_c11c_immutability_preserved(self): self.assertEqual(next(g for g in self.m['gates'] if g['gate_id']=='AA-10-C11-C-IMMUTABILITY')['status'],'PASS_PRESERVE_IMMUTABLE_BASELINE')
    def test_40_next_gate_is_phase_ab(self): self.assertEqual(self.r['next_gate'],'PHASE_AB_OPERATOR_DECISION_EVIDENCE_SUBMISSION_AND_AUTHORITY_ADJUDICATION')
    def test_41_verifier_accepts_all_contracts(self): self.assertTrue(verify(self.args.phase_z_json,self.args.phase_z_packet_json,self.args.phase_aa_result_json,self.args.phase_aa_matrix_json,self.args.phase_aa_packet_json))
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--phase-z-json',required=True); ap.add_argument('--phase-z-packet-json',required=True); ap.add_argument('--phase-aa-result-json',required=True); ap.add_argument('--phase-aa-matrix-json',required=True); ap.add_argument('--phase-aa-packet-json',required=True)
    PhaseAATests.args=ap.parse_args(); suite=unittest.defaultTestLoader.loadTestsFromTestCase(PhaseAATests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    print('PHASE_AA_PRE_RENDER_READINESS_TESTS=%d/%d' % (result.testsRun,result.testsRun))
    return 0 if result.wasSuccessful() and result.testsRun==41 else 1
if __name__=='__main__': raise SystemExit(main())
