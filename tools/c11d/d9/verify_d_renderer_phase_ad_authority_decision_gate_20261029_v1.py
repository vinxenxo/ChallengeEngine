#!/usr/bin/env python3
"""Structural verifier for Phase AC closeout and Phase AD decision gate."""
from __future__ import annotations
import argparse, json, hashlib, sys
from pathlib import Path

def digest(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--phase-ac-result-json',required=True)
    ap.add_argument('--phase-ac-matrix-json',required=True)
    ap.add_argument('--phase-ad-packet-json',required=True)
    args=ap.parse_args()
    ac=json.loads(Path(args.phase_ac_result_json).read_text(encoding='utf-8'))
    mx=json.loads(Path(args.phase_ac_matrix_json).read_text(encoding='utf-8'))
    ad=json.loads(Path(args.phase_ad_packet_json).read_text(encoding='utf-8'))
    errors=[]
    if ac.get('phase')!='AC' or ac.get('status')!='PASS_CONTENT_REVIEW_COMPLETE_NO_APPLICABLE_D_RENDER_AUTHORITY_FOUND': errors.append('AC_STATUS')
    if ac.get('input',{}).get('source_bundle_sha256')!='5ee6ec0f5a6b3a0884c22bbecfc98691269bd431adc896c088e7eb7f9d0b7f08': errors.append('AC_BUNDLE_PIN')
    counts=ac.get('counts',{})
    for k,v in {'remaining_candidates_reviewed_in_phase_ac':57,'medium_priority':55,'low_priority':2,'source_hash_matches':57,'source_hash_mismatches':0,'source_files_missing':0,'authority_records_applicable_to_first_d_baseline_render':0,'policy_adoptions':0,'authority_adjudications_from_operator_evidence':0}.items():
        if counts.get(k)!=v: errors.append('AC_COUNT_'+k)
    if len(mx.get('source_dispositions',[]))!=57: errors.append('MATRIX_ROWS')
    if digest(args.phase_ac_result_json)!=(ad.get('evidence_review_basis',{}).get('phase_ac_result_json_sha256')): errors.append('AC_REPORT_HASH')
    if digest(args.phase_ac_matrix_json)!=(ad.get('evidence_review_basis',{}).get('phase_ac_disposition_matrix_sha256')): errors.append('AC_MATRIX_HASH')
    rows=ad.get('decisions',[])
    expected=['R-01-TIMEBASE-SAMPLING','R-02-SPATIAL-MAPPING','R-03-PILOT-SCALAR-X-AND-PRESENTATION-Y','R-04-VISIBILITY-AND-REGION-OWNERSHIP','R-05-ASSET-GEOMETRY-ANCHOR-CROP-ROUNDING','R-06-INVALID-DATA-AND-TRACK-INTEGRITY','R-07-SEMANTIC-VISUAL-OWNERSHIP','R-08-CHALLENGE-008','R-09-CHALLENGE-009']
    if [r.get('decision_id') for r in rows]!=expected: errors.append('DECISION_IDS')
    if any(r.get('operator_decision_gate_status')!='PENDING_OPERATOR_ACTION' or r.get('selected_option') is not None for r in rows): errors.append('ROWS_NOT_PENDING')
    if ad.get('authority_records_submitted')!=0 or ad.get('operator_decisions_adjudicated')!=0: errors.append('EVIDENCE_COUNTS')
    gov=ad.get('governance',{})
    locks={'renderer':'OFF','media_created':False,'payload_materialized':False,'candidate_input_admissible':False,'seed_domains_complete_for_candidate_input':False,'automatic_seed_generation':False,'master_seed':'NOT_ADOPTED','approved_bindings':0,'approved_custom_data_bindings':0,'approved_renderer_projection_bindings':0,'D4.8':'BLOCKED','D9.10':'PREPARE_ONLY','D9.14':'BLOCKED','D9.16':'BLOCKED','D9.17':'BLOCKED_NO_GO','D10':'BLOCKED_FOR_PROMOTION','baseline_approval':'MISSING','freeze_eligible':False,'release_authority':'NONE'}
    for k,v in locks.items():
        if gov.get(k)!=v: errors.append('LOCK_'+k)
    if ad.get('status')!='PENDING_OPERATOR_CHOICE_NO_APPLICABLE_AUTHORITY_SUBMITTED': errors.append('AD_STATUS')
    if ad.get('operator_decision',{}).get('chosen_global_option') is not None: errors.append('GLOBAL_OPTION_INVENTED')
    if ad.get('first_render_readiness')!='BLOCKED': errors.append('RENDER_READINESS')
    if errors:
        print('PHASE_AD_VERIFICATION=FAIL')
        print('ERRORS='+','.join(errors))
        return 2
    print('PHASE_AD_VERIFICATION=PASS_DECISION_PACKET_AND_GOVERNANCE_LOCKS')
    print('PHASE_AD_VERIFIED_DECISIONS=9')
    print('PHASE_AD_OPERATOR_DECISION=PENDING_EVIDENCE_OR_KEEP_BLOCKED')
    print('PHASE_AD_RENDER_READINESS=BLOCKED')
    print('NEXT_ACTION=OPERATOR_SUBMIT_REAL_AUTHORITY_OR_EXPLICIT_KEEP_BLOCKED')
    return 0
if __name__=='__main__': sys.exit(main())
