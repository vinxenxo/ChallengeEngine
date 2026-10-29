#!/usr/bin/env python3
"""Structural regressions for Phase AB authority evidence intake; no authority is inferred."""
import argparse, json, sys, unittest
from pathlib import Path
EXPECTED_IDS = [
'R-01-TIMEBASE-SAMPLING','R-02-SPATIAL-MAPPING','R-03-PILOT-SCALAR-X-AND-PRESENTATION-Y',
'R-04-VISIBILITY-AND-REGION-OWNERSHIP','R-05-ASSET-GEOMETRY-ANCHOR-CROP-ROUNDING',
'R-06-INVALID-DATA-AND-TRACK-INTEGRITY','R-07-SEMANTIC-VISUAL-OWNERSHIP','R-08-CHALLENGE-008','R-09-CHALLENGE-009']
LOCKS = {'renderer':'OFF','media_created':False,'payload_materialized':False,'candidate_input_admissible':False,'seed_domains_complete_for_candidate_input':False,'automatic_seed_generation':False,'master_seed':'NOT_ADOPTED','approved_bindings':0,'approved_custom_data_bindings':0,'approved_renderer_projection_bindings':0,'D4.8':'BLOCKED','D9.10':'PREPARE_ONLY','D9.14':'BLOCKED','D9.16':'BLOCKED','D9.17':'BLOCKED_NO_GO','D10':'BLOCKED_FOR_PROMOTION','baseline_approval':'MISSING','freeze_eligible':False,'release_authority':'NONE'}
EXPECTED_FIELDS = ['decision_id','requested_disposition','exact_policy_text_and_selected_option','named_approving_authority_and_role','authority_scope_and_delegation_basis','decision_date_and_effective_date','rationale','source_paths_and_sha256_pins','acceptance_test_obligations','verifiable_approval_provenance_or_signature','immutable_record_location']
DATA={}
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
class PhaseABTests(unittest.TestCase):
 def test_01_phaseaa_status(self): self.assertEqual(DATA['aa']['status'],'PASS_PRE_RENDER_AUDIT_COMPLETE_RENDER_READINESS_BLOCKED')
 def test_02_phaseaa_tests_41(self): self.assertEqual(DATA['result']['phase_aa_closeout']['tests'],'PASS_41_OF_41')
 def test_03_test_stdout_pin(self): self.assertEqual(DATA['result']['phase_aa_closeout']['test_stdout_sha256'],'8cf39d6dfb66a3ca351b622774e254e6e51e8bec1cf2eb2e70fa0a1677b96d2a')
 def test_04_test_stderr_pin(self): self.assertEqual(DATA['result']['phase_aa_closeout']['test_stderr_sha256'],'3b72918a4695d2085da90fa89af4e6c2cdd7b9929db7b346daa38c3a9a1cca40')
 def test_05_verify_stdout_pin(self): self.assertEqual(DATA['result']['phase_aa_closeout']['verify_stdout_sha256'],'675bd74134827a41e87bac05048c5488b1717234c0115e7f8ecd0fc87e7d0ffc')
 def test_06_verify_stderr_empty_sha(self): self.assertEqual(DATA['result']['phase_aa_closeout']['verify_stderr_sha256'],'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')
 def test_07_phaseaa_decisions_nine(self): self.assertEqual(DATA['aa']['checks']['phase_z_decisions_verified'],9)
 def test_08_phaseaa_readiness_blocked(self): self.assertEqual(DATA['aa']['checks']['pre_render_readiness'],'BLOCKED')
 def test_09_phaseab_phase(self): self.assertEqual(DATA['packet']['phase'],'AB')
 def test_10_phaseab_packet_status_pending(self): self.assertEqual(DATA['packet']['status'],'PREPARED_PENDING_OPERATOR_EVIDENCE_AND_AUTHORITY_ADJUDICATION')
 def test_11_result_status_pending(self): self.assertEqual(DATA['result']['status'],'INTAKE_PACKET_PREPARED_PENDING_OPERATOR_EVIDENCE')
 def test_12_ids_exact_order(self): self.assertEqual([x['decision_id'] for x in DATA['packet']['decisions']],EXPECTED_IDS)
 def test_13_result_ids_exact_order(self): self.assertEqual(DATA['result']['decision_ids'],EXPECTED_IDS)
 def test_14_nine_rows(self): self.assertEqual(len(DATA['packet']['decisions']),9)
 def test_15_all_intake_pending(self): self.assertTrue(all(x['intake_status']=='PENDING_OPERATOR_SUBMISSION' for x in DATA['packet']['decisions']))
 def test_16_all_dispositions_pending(self): self.assertTrue(all(x['operator_disposition']=='PENDING' for x in DATA['packet']['decisions']))
 def test_17_no_selected_option(self): self.assertTrue(all(x['selected_option'] is None for x in DATA['packet']['decisions']))
 def test_18_no_policy_text(self): self.assertTrue(all(x['exact_policy_text'] is None for x in DATA['packet']['decisions']))
 def test_19_no_approver_invented(self): self.assertTrue(all(x['named_approving_authority'] is None and x['approving_role'] is None for x in DATA['packet']['decisions']))
 def test_20_no_delegation_invented(self): self.assertTrue(all(x['delegation_basis_and_scope'] is None for x in DATA['packet']['decisions']))
 def test_21_no_dates_invented(self): self.assertTrue(all(x['decision_date'] is None and x['effective_date'] is None for x in DATA['packet']['decisions']))
 def test_22_no_rationale_invented(self): self.assertTrue(all(x['rationale'] is None for x in DATA['packet']['decisions']))
 def test_23_no_source_records_fabricated(self): self.assertTrue(all(x['source_records']==[] for x in DATA['packet']['decisions']))
 def test_24_no_signature_invented(self): self.assertTrue(all(x['approval_provenance_or_signature_ref'] is None for x in DATA['packet']['decisions']))
 def test_25_no_immutable_location_invented(self): self.assertTrue(all(x['immutable_record_location'] is None for x in DATA['packet']['decisions']))
 def test_26_review_pending(self): self.assertTrue(all(x['authority_review']['decision']=='PENDING_NOT_ADJUDICATED' for x in DATA['packet']['decisions']))
 def test_27_status_blocked_all_rows(self): self.assertTrue(all(x['status']=='BLOCKED_REQUIRED_AUTHORITY_EVIDENCE_MISSING' for x in DATA['packet']['decisions']))
 def test_28_r01_r07_unadopted(self): self.assertTrue(all(DATA['packet']['decisions'][i]['current_disposition']=='NOT_ADOPTED_KEEP_BLOCKED' for i in range(7)))
 def test_29_r08_blocked(self): self.assertEqual(DATA['packet']['decisions'][7]['current_disposition'],'BLOCKED_EXPLICIT_AUTHORITY_REQUIRED')
 def test_30_r09_blocked(self): self.assertEqual(DATA['packet']['decisions'][8]['current_disposition'],'BLOCKED_EXPLICIT_AUTHORITY_REQUIRED')
 def test_31_required_fields_exact(self): self.assertEqual(DATA['packet']['required_fields'],EXPECTED_FIELDS)
 def test_32_permitted_defer(self): self.assertIn('DEFER_KEEP_BLOCKED',DATA['packet']['permitted_intake_dispositions'])
 def test_33_permitted_no_record(self): self.assertIn('NO_VALID_AUTHORITY_RECORD_FOUND_KEEP_BLOCKED',DATA['packet']['permitted_intake_dispositions'])
 def test_34_intake_does_not_adopt(self): self.assertIs(DATA['packet']['intake_dispositions_do_not_adopt_policy'],True)
 def test_35_evidence_records_zero(self): self.assertEqual(DATA['result']['evidence_records_submitted'],0)
 def test_36_adjudications_zero(self): self.assertEqual(DATA['result']['authority_adjudications_completed'],0)
 def test_37_fabricated_decisions_zero(self): self.assertEqual(DATA['result']['operator_decisions_fabricated'],0)
 def test_38_policy_adoption_none(self): self.assertEqual(DATA['result']['policy_adoption'],'NONE')
 def test_39_global_renderer_off(self): self.assertEqual(DATA['result']['hard_locks']['renderer'],'OFF')
 def test_40_media_payload_false(self): self.assertIs(DATA['result']['hard_locks']['media_created'],False); self.assertIs(DATA['result']['hard_locks']['payload_materialized'],False)
 def test_41_candidate_input_blocked(self): self.assertIs(DATA['result']['hard_locks']['candidate_input_admissible'],False)
 def test_42_seed_domains_incomplete(self): self.assertIs(DATA['result']['hard_locks']['seed_domains_complete_for_candidate_input'],False)
 def test_43_master_seed_not_adopted(self): self.assertEqual(DATA['result']['hard_locks']['master_seed'],'NOT_ADOPTED')
 def test_44_binding_counts_zero(self): self.assertEqual([DATA['result']['hard_locks'][x] for x in ['approved_bindings','approved_custom_data_bindings','approved_renderer_projection_bindings']],[0,0,0])
 def test_45_d917_no_go(self): self.assertEqual(DATA['result']['hard_locks']['D9.17'],'BLOCKED_NO_GO')
 def test_46_d10_blocked(self): self.assertEqual(DATA['result']['hard_locks']['D10'],'BLOCKED_FOR_PROMOTION')
 def test_47_release_none(self): self.assertEqual(DATA['result']['hard_locks']['release_authority'],'NONE')
 def test_48_aa_result_input_pin(self): self.assertEqual(DATA['result']['source_pins']['docs/current/d/C11D_PHASE_AA_PRE_RENDER_READINESS_RESULT_20261029_V1.json'],'254de0a6540f02014d6530062274d72a8e552a7a06399de7e173b71e9683f40e')
 def test_49_z_packet_input_pin(self): self.assertEqual(DATA['packet']['source_phase_z_packet']['sha256'],'454e1e8fcc14634a97c124483e1272dcda040715e3febd5fbcec6cd115b68f2c')
 def test_50_next_gate(self): self.assertEqual(DATA['result']['next_gate'],'PHASE_AB_OPERATOR_DECISION_EVIDENCE_SUBMISSION_AND_AUTHORITY_ADJUDICATION')
def main():
 p=argparse.ArgumentParser()
 p.add_argument('--phase-aa-result-json',required=True); p.add_argument('--phase-aa-packet-json',required=True)
 p.add_argument('--phase-ab-result-json',required=True); p.add_argument('--phase-ab-packet-json',required=True)
 a=p.parse_args()
 try:
  DATA['aa']=load(a.phase_aa_result_json); DATA['aa_packet']=load(a.phase_aa_packet_json); DATA['result']=load(a.phase_ab_result_json); DATA['packet']=load(a.phase_ab_packet_json)
 except Exception as e:
  print('PHASE_AB_TEST_INPUT_ERROR='+str(e),file=sys.stderr); return 2
 suite=unittest.defaultTestLoader.loadTestsFromTestCase(PhaseABTests)
 result=unittest.TextTestRunner(stream=sys.stderr,verbosity=2).run(suite)
 if result.wasSuccessful():
  print('PHASE_AB_AUTHORITY_EVIDENCE_INTAKE_TESTS=50/50')
  return 0
 print('PHASE_AB_AUTHORITY_EVIDENCE_INTAKE_TESTS=FAIL')
 return 1
if __name__=='__main__': raise SystemExit(main())
