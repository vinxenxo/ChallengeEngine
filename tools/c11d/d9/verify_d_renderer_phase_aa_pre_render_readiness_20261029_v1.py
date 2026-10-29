#!/usr/bin/env python3
"""Read-only verifier for Phase AA readiness audit and governance locks."""
import argparse, json, hashlib, sys
from pathlib import Path
EXPECTED_DECISIONS = [
'R-01-TIMEBASE-SAMPLING','R-02-SPATIAL-MAPPING','R-03-PILOT-SCALAR-X-AND-PRESENTATION-Y',
'R-04-VISIBILITY-AND-REGION-OWNERSHIP','R-05-ASSET-GEOMETRY-ANCHOR-CROP-ROUNDING',
'R-06-INVALID-DATA-AND-TRACK-INTEGRITY','R-07-SEMANTIC-VISUAL-OWNERSHIP','R-08-CHALLENGE-008','R-09-CHALLENGE-009']
REQUIRED_LOCKS = {'renderer':'OFF','media_created':False,'payload_materialized':False,'candidate_input_admissible':False,'seed_domains_complete_for_candidate_input':False,'automatic_seed_generation':False,'master_seed':'NOT_ADOPTED','approved_bindings':0,'approved_custom_data_bindings':0,'approved_renderer_projection_bindings':0,'D4.8':'BLOCKED','D9.10':'PREPARE_ONLY','D9.14':'BLOCKED','D9.16':'BLOCKED','D9.17':'BLOCKED_NO_GO','D10':'BLOCKED_FOR_PROMOTION','baseline_approval':'MISSING','freeze_eligible':False,'release_authority':'NONE'}
REQUIRED_FIELDS = ['decision_id','exact_policy_text_and_selected_option','named_approving_authority_and_role','authority_scope_and_delegation_basis','decision_date_and_effective_date','rationale','source_paths_and_sha256_pins','acceptance_test_obligations','verifiable_approval_provenance_or_signature','immutable_record_location']
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def verify(phase_z_path, packet_z_path, result_path, matrix_path, packet_aa_path):
    z=load(phase_z_path); pz=load(packet_z_path); r=load(result_path); m=load(matrix_path); pa=load(packet_aa_path)
    assert z.get('phase') == 'Z' and z.get('decision_count') == 9
    assert [x['decision_id'] for x in z['decisions']] == EXPECTED_DECISIONS
    assert [x['decision_id'] for x in pz['decisions']] == EXPECTED_DECISIONS
    assert [x['decision_id'] for x in pa['decisions']] == EXPECTED_DECISIONS
    assert r.get('phase') == 'AA' and r.get('status') == 'PASS_PRE_RENDER_AUDIT_COMPLETE_RENDER_READINESS_BLOCKED'
    assert r['checks']['phase_z_static_tests'] == 'PASS_30_OF_30'
    assert r['checks']['decision_evidence_completed'] is False
    assert r['checks']['all_required_authority_fields_present'] is False
    assert r['checks']['authority_adjudication'] == 'PENDING'
    assert r['checks']['pre_render_readiness'] == 'BLOCKED'
    assert r['checks']['render_execution_authorized'] is False
    assert r['checks']['renderer_activation_authorized'] is False
    assert r['checks']['godot_invoked'] is False and r['checks']['runtime_reexecuted'] is False
    assert m['status'] == 'AUDIT_COMPLETE_RENDER_READINESS_BLOCKED'
    for key in ['render_execution_authorized','renderer_activation_authorized','godot_invocation_authorized','media_creation_authorized','payload_materialization_authorized','candidate_input_admissibility_authorized','seed_generation_authorized','binding_activation_authorized']:
        assert m[key] is False, key
    assert m['hard_locks'] == REQUIRED_LOCKS
    assert r['hard_locks'] == REQUIRED_LOCKS
    assert pa['status'] == 'BLOCKED_REQUIRED_AUTHORITY_EVIDENCE_PENDING'
    assert pa['required_fields'] == pz['required_fields'] == REQUIRED_FIELDS
    assert len(pa['decisions']) == 9
    for d in pa['decisions']:
        assert d['requested_operator_disposition'] == 'PENDING'
        assert d['status'] == 'BLOCKED_REQUIRED_AUTHORITY_EVIDENCE_MISSING'
        assert d['result_if_incomplete'] == 'KEEP_BLOCKED_NO_POLICY_ADOPTION'
        assert d['selected_option'] is None and d['exact_policy_text'] is None
        assert d['named_approving_authority'] is None and d['approving_role'] is None
        assert d['delegation_basis_and_scope'] is None and d['decision_date'] is None and d['effective_date'] is None
        assert d['rationale'] is None and d['source_pins'] == []
        assert d['acceptance_test_obligations'] is None and d['approval_provenance_or_signature_ref'] is None
        assert d['immutable_record_location'] is None
        assert d['required_fields_missing'] == REQUIRED_FIELDS
    statuses={g['gate_id']:g['status'] for g in m['gates']}
    assert len(statuses) == 10
    assert statuses['AA-01-AUTHORITY-DECISION-EVIDENCE']=='BLOCKED'
    assert statuses['AA-02-R08-R09-TIMING-RECONCILIATION']=='BLOCKED'
    assert statuses['AA-03-CANDIDATE-INPUT-ADMISSIBILITY']=='BLOCKED'
    assert statuses['AA-04-SEED-DOMAIN-COMPLETENESS']=='BLOCKED'
    assert statuses['AA-05-SEMANTIC-AND-CUSTOM-DATA-BINDINGS']=='BLOCKED'
    assert statuses['AA-06-RENDERER-PROJECTION']=='BLOCKED'
    assert statuses['AA-07-D9-17-RENDER-NO-GO']=='BLOCKED_NO_GO'
    assert statuses['AA-08-ISOLATED-RENDER-ACCEPTANCE']=='PREPARE_ONLY'
    assert statuses['AA-09-D10-BASELINE-PROMOTION']=='BLOCKED_FOR_PROMOTION'
    assert statuses['AA-10-C11-C-IMMUTABILITY']=='PASS_PRESERVE_IMMUTABLE_BASELINE'
    byid={x['decision_id']:x for x in z['decisions']}
    assert all(byid[x]['status']=='NOT_ADOPTED_KEEP_BLOCKED' for x in EXPECTED_DECISIONS[:7])
    assert byid[EXPECTED_DECISIONS[7]]['status']=='BLOCKED_EXPLICIT_AUTHORITY_REQUIRED'
    assert byid[EXPECTED_DECISIONS[8]]['status']=='BLOCKED_EXPLICIT_AUTHORITY_REQUIRED'
    assert m['next_gate'] == r['next_gate'] == 'PHASE_AB_OPERATOR_DECISION_EVIDENCE_SUBMISSION_AND_AUTHORITY_ADJUDICATION'
    return True
def main():
    a=argparse.ArgumentParser()
    a.add_argument('--phase-z-json',required=True); a.add_argument('--phase-z-packet-json',required=True)
    a.add_argument('--phase-aa-result-json',required=True); a.add_argument('--phase-aa-matrix-json',required=True); a.add_argument('--phase-aa-packet-json',required=True)
    x=a.parse_args()
    try:
        verify(x.phase_z_json,x.phase_z_packet_json,x.phase_aa_result_json,x.phase_aa_matrix_json,x.phase_aa_packet_json)
    except Exception as e:
        print('PHASE_AA_VERIFY_ERROR='+str(e),file=sys.stderr); return 2
    print('PHASE_AA_VERIFICATION=PASS_AUDIT_AND_LOCKS')
    print('PHASE_AA_VERIFIED_DECISIONS=9')
    print('PHASE_AA_OPERATOR_EVIDENCE=BLOCKED_REQUIRED_AUTHORITY_EVIDENCE_MISSING')
    print('PHASE_AA_RENDER_READINESS=BLOCKED')
    print('AUTHORITY_ADJUDICATION=PENDING; POLICY_ADOPTION=NONE; RENDERER=OFF; APPROVED_BINDINGS=0; RELEASE_AUTHORITY=NONE')
    print('NEXT_GATE=PHASE_AB_OPERATOR_DECISION_EVIDENCE_SUBMISSION_AND_AUTHORITY_ADJUDICATION')
    return 0
if __name__=='__main__': raise SystemExit(main())
