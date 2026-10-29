#!/usr/bin/env python3
"""Read-only structural verifier for Phase AA closeout and Phase AB evidence intake."""
import argparse,json,sys
from pathlib import Path
IDS=['R-01-TIMEBASE-SAMPLING','R-02-SPATIAL-MAPPING','R-03-PILOT-SCALAR-X-AND-PRESENTATION-Y','R-04-VISIBILITY-AND-REGION-OWNERSHIP','R-05-ASSET-GEOMETRY-ANCHOR-CROP-ROUNDING','R-06-INVALID-DATA-AND-TRACK-INTEGRITY','R-07-SEMANTIC-VISUAL-OWNERSHIP','R-08-CHALLENGE-008','R-09-CHALLENGE-009']
LOCKS={'renderer':'OFF','media_created':False,'payload_materialized':False,'candidate_input_admissible':False,'seed_domains_complete_for_candidate_input':False,'automatic_seed_generation':False,'master_seed':'NOT_ADOPTED','approved_bindings':0,'approved_custom_data_bindings':0,'approved_renderer_projection_bindings':0,'D4.8':'BLOCKED','D9.10':'PREPARE_ONLY','D9.14':'BLOCKED','D9.16':'BLOCKED','D9.17':'BLOCKED_NO_GO','D10':'BLOCKED_FOR_PROMOTION','baseline_approval':'MISSING','freeze_eligible':False,'release_authority':'NONE'}
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def verify(aa_result,aa_packet,ab_result,ab_packet):
 aa=load(aa_result); aap=load(aa_packet); ab=load(ab_result); abp=load(ab_packet)
 assert aa['phase']=='AA' and aa['status']=='PASS_PRE_RENDER_AUDIT_COMPLETE_RENDER_READINESS_BLOCKED'
 assert aa['checks']['phase_z_static_tests']=='PASS_30_OF_30'
 assert aa['checks']['decision_evidence_completed'] is False and aa['checks']['pre_render_readiness']=='BLOCKED'
 assert aa['hard_locks']==LOCKS
 assert ab['phase']=='AB' and ab['status']=='INTAKE_PACKET_PREPARED_PENDING_OPERATOR_EVIDENCE'
 assert ab['decision_count']==9 and ab['decision_ids']==IDS
 assert ab['evidence_records_submitted']==0 and ab['authority_adjudications_completed']==0
 assert ab['operator_decisions_fabricated']==0 and ab['policy_adoption']=='NONE'
 assert ab['authority_adjudication']=='PENDING_OPERATOR_EVIDENCE' and ab['hard_locks']==LOCKS
 assert abp['phase']=='AB' and abp['status']=='PREPARED_PENDING_OPERATOR_EVIDENCE_AND_AUTHORITY_ADJUDICATION'
 assert [x['decision_id'] for x in abp['decisions']]==IDS
 assert abp['required_fields']==['decision_id','requested_disposition','exact_policy_text_and_selected_option','named_approving_authority_and_role','authority_scope_and_delegation_basis','decision_date_and_effective_date','rationale','source_paths_and_sha256_pins','acceptance_test_obligations','verifiable_approval_provenance_or_signature','immutable_record_location']
 assert abp['hard_locks']==LOCKS and abp['global_governance_acknowledgements']['policy_adoption']=='NONE'
 for row in abp['decisions']:
  assert row['intake_status']=='PENDING_OPERATOR_SUBMISSION' and row['operator_disposition']=='PENDING'
  assert row['selected_option'] is None and row['exact_policy_text'] is None
  assert row['named_approving_authority'] is None and row['approving_role'] is None
  assert row['source_records']==[] and row['authority_review']['decision']=='PENDING_NOT_ADJUDICATED'
  assert row['status']=='BLOCKED_REQUIRED_AUTHORITY_EVIDENCE_MISSING'
 assert all(abp['decisions'][i]['current_disposition']=='NOT_ADOPTED_KEEP_BLOCKED' for i in range(7))
 assert abp['decisions'][7]['current_disposition']=='BLOCKED_EXPLICIT_AUTHORITY_REQUIRED'
 assert abp['decisions'][8]['current_disposition']=='BLOCKED_EXPLICIT_AUTHORITY_REQUIRED'
 assert ab['next_gate']=='PHASE_AB_OPERATOR_DECISION_EVIDENCE_SUBMISSION_AND_AUTHORITY_ADJUDICATION'
 return True
def main():
 p=argparse.ArgumentParser(); p.add_argument('--phase-aa-result-json',required=True); p.add_argument('--phase-aa-packet-json',required=True); p.add_argument('--phase-ab-result-json',required=True); p.add_argument('--phase-ab-packet-json',required=True); a=p.parse_args()
 try: verify(a.phase_aa_result_json,a.phase_aa_packet_json,a.phase_ab_result_json,a.phase_ab_packet_json)
 except Exception as e: print('PHASE_AB_VERIFY_ERROR='+str(e),file=sys.stderr); return 2
 print('PHASE_AB_VERIFICATION=PASS_INTAKE_STRUCTURE_AND_GOVERNANCE_LOCKS')
 print('PHASE_AB_VERIFIED_DECISIONS=9')
 print('PHASE_AB_EVIDENCE_RECORDS_SUBMITTED=0')
 print('PHASE_AB_AUTHORITY_ADJUDICATION=PENDING_OPERATOR_EVIDENCE')
 print('PHASE_AB_RENDER_READINESS=BLOCKED')
 print('AUTHORITY_ADJUDICATION=PENDING; POLICY_ADOPTION=NONE; RENDERER=OFF; APPROVED_BINDINGS=0; RELEASE_AUTHORITY=NONE')
 print('NEXT_ACTION=SUBMIT_REAL_IMMUTABLE_AUTHORITY_EVIDENCE_OR_RECORD_KEEP_BLOCKED')
 return 0
if __name__=='__main__': raise SystemExit(main())
