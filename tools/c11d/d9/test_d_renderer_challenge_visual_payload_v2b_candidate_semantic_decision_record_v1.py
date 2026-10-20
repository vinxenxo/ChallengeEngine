#!/usr/bin/env python3
"""Static regression tests for C11-D V2-B candidate semantic decision record. No Godot, rendering or writes."""
from __future__ import annotations
import hashlib, json, sys
from datetime import datetime
from pathlib import Path

C11C='e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953'
DESIGN='e4f02e37fd4b9b2c89cbaa7597162f87b180da43182dc576d664263c1b937cfc'
MATRIX='d69c3fb2aca78a26c3afbfda0084f7f7aef458ee404b37f65261c6d22e43121a'
V2C='6d3c59214edbdd917cf63fe9ca4859edb6968d503368ec84e867bdd56a8df74c'
RUNTIME_CONTRACT='f89235640f40c81be6100f01f1007ed4e787990a1bbf7927fcd8d676ef2cb9a3'
RUNTIME_REPORT='f7a1522695cbd6d3f3681d3f266b625e3062d5141c32cddbb4532bcb466e0446'
AUDIT='8c4503c128355fa21e670be0aaea25b093a73c325253a2afcec2a066a92e5f00'
IMPL_RECEIPT='e64cfd259914c471d03e8578b955140ad487b04694c5f682834517d823fcbfc4'
AUDIT_TEST_RECEIPT='1a57d59a41c87696a07128fd397db0f031f74d87ac42fb1877a084a1c2c5631d'
RECEIPT_FIX_TEST='6b8b166c36a1341ceec23cde38c4999d7aa6aacb26a5153459ce05879fec1043'
REVIEW_REQUEST='b576612dd0913ce8f706a5272a5b9ca5ceb6c7a1f39d832323d9db98578b5d01'
REVIEW_REQUEST_TEST='8de93859cd82e391d541d190f21d95a98a5508a7d5ee5952fe65eff256d1d53d'
SOURCE_REVIEW='374472b2d7ab0a70d94ed1f650302869b829252dcf06a7afe29c7c2e18e345dc'
REQUEST_SCHEMA='66e75d5fc136c0e3ffeeb2861abae8ac73d2e43eded257e54aadbd2736f2c68c'
DECISION_SCHEMA='ab09a617e9efc0aacb2111d9f6b02fc5764850f667cfdb33005451c5d4b073b9'
RECORD_SHA='cc3550cd4d13f228ec9b3d51eeaa199505c5975b42882fb06ba3e83c4a000e90'
ACCEPT='ACCEPT_SEMANTIC_DEFINITION_FOR_FUTURE_BINDING_SPECIFICATION'
BLOCKED='BLOCKED_NEEDS_SOURCE_OR_POLICY_DECISION'
EXPECTED=[
 ('CHALLENGE_003','target_x','float',ACCEPT),
 ('CHALLENGE_005','target_position','Vector2',ACCEPT),
 ('CHALLENGE_006','target_position','Vector2',ACCEPT),
 ('CHALLENGE_007','target_position','Vector2',ACCEPT),
 ('CHALLENGE_008','active_selection','int',BLOCKED),
 ('CHALLENGE_009','displayed_count','int',BLOCKED),
]

def sha(path:Path)->str: return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path:Path): return json.loads(path.read_text(encoding='utf-8'))

def main()->int:
    root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd().resolve()
    n=0
    def ck(label, condition):
        nonlocal n
        if not condition:
            print('FAIL '+label,file=sys.stderr)
            raise AssertionError(label)
        n+=1

    recp=root/'definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_SEMANTIC_DECISION_RECORD_V1.json'
    schp=root/'definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_SEMANTIC_DECISION_RECORD_SCHEMA_V1.json'
    reqp=root/'definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_SEMANTIC_REVIEW_REQUEST_V1.json'
    reqschp=root/'definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_SEMANTIC_REVIEW_REQUEST_SCHEMA_V1.json'
    srcp=root/'definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_SOURCE_SEMANTIC_REVIEW_V1.json'
    designp=root/'definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SAFE_VISUAL_PROJECTION_DESIGN_V1.json'
    matrixp=root/'definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SEED_TEST_MATRIX_V1.json'
    v2cp=root/'definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2C_SOURCE_FRAME_RUNTIME_RECEIPT_V1.json'
    runtimecp=root/'definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SAFE_PROJECTION_RUNTIME_CONTRACT_V1.json'
    frozenp=root/'release/C11C_FREEZE_PACKAGE_MANIFEST.json'
    docs=[recp,schp,reqp,reqschp,srcp,designp,matrixp,v2cp,runtimecp,frozenp]
    for p in docs: ck('required file: '+p.name,p.is_file())

    rec=read(recp); sch=read(schp); req=read(reqp); reqsch=read(reqschp); src=read(srcp); design=read(designp); matrix=read(matrixp); v2c=read(v2cp); runtimec=read(runtimecp); frozen=read(frozenp)

    for label,path,expected in [
      ('record SHA',recp,RECORD_SHA),('decision schema SHA',schp,DECISION_SCHEMA),('review request SHA',reqp,REVIEW_REQUEST),
      ('review request schema SHA',reqschp,REQUEST_SCHEMA),('source review SHA',srcp,SOURCE_REVIEW),
      ('design SHA',designp,DESIGN),('seed matrix SHA',matrixp,MATRIX),('V2-C source frame SHA',v2cp,V2C),
      ('runtime contract SHA',runtimecp,RUNTIME_CONTRACT),('frozen manifest SHA',frozenp,C11C)]:
        ck(label,sha(path)==expected)

    ck('record schema id',rec.get('schema')=='C11D-V2B-CANDIDATE-SEMANTIC-DECISION-RECORD-V1')
    ck('record schema version',rec.get('schema_version')=='1.0')
    ck('record final status',rec.get('status')=='SEMANTIC_DECISIONS_RECORDED_BINDINGS_NOT_APPROVED')
    ck('schema strict root',sch.get('additionalProperties') is False)
    ck('schema ID matches record',sch.get('properties',{}).get('schema',{}).get('const')==rec.get('schema'))
    ck('schema root required complete',set(rec.keys())==set(sch.get('required',[])))
    ck('record keys known to schema',set(rec.keys()).issubset(set(sch.get('properties',{}).keys())))
    ck('nested decisions strict schema',sch.get('properties',{}).get('decisions',{}).get('items',{}).get('additionalProperties') is False)
    ck('allowed decision enum complete',set(sch.get('properties',{}).get('decisions',{}).get('items',{}).get('properties',{}).get('semantic_decision',{}).get('enum',[]))=={ACCEPT,'REJECT_CANDIDATE_SEMANTIC_DEFINITION',BLOCKED})
    ck('binding authorization forbidden by schema',sch.get('properties',{}).get('binding_authorization',{}).get('const')=='NOT_GRANTED_BY_SEMANTIC_REVIEW')
    ck('renderer authorization forbidden by schema',sch.get('properties',{}).get('renderer_projection_authorization',{}).get('const')=='NOT_GRANTED_BY_SEMANTIC_REVIEW')
    ck('request schema strict root',reqsch.get('additionalProperties') is False)
    ck('request schema id',req.get('schema')=='C11D-V2B-CANDIDATE-SEMANTIC-REVIEW-REQUEST-V1')
    ck('request schema version',req.get('schema_version')=='1.0')
    ck('review request remains pending',req.get('status')=='PENDING_EXPLICIT_SEMANTIC_DECISIONS')
    ck('review request candidate count',req.get('candidate_count')==6 and len(req.get('candidates',[]))==6)
    ck('review request next gate preserved',req.get('next_gate')=='OPERATOR_SEMANTIC_DECISION_RECORD_REQUIRED; NO_BINDING_APPROVAL; NO_PAYLOAD_CONSUMER')
    ck('request SHA bound into decision record',rec.get('request_sha256')==sha(reqp)==REVIEW_REQUEST)
    ck('candidate audit SHA bound into record',rec.get('candidate_evidence_audit_sha256')==req.get('evidence_pins',{}).get('candidate_evidence_audit_json_sha256')==AUDIT)
    ck('runtime report hash is pinned',req.get('evidence_pins',{}).get('runtime_report_sha256')==RUNTIME_REPORT)
    ck('implementation receipt hash pinned',req.get('evidence_pins',{}).get('implementation_test_receipt_sha256')==IMPL_RECEIPT)
    ck('audit-test receipt hash pinned',req.get('evidence_pins',{}).get('candidate_audit_static_test_receipt_sha256')==AUDIT_TEST_RECEIPT)
    ck('receipt-fix test hash pinned',req.get('evidence_pins',{}).get('receipt_schema_fix_test_receipt_sha256')==RECEIPT_FIX_TEST)
    ck('request evidence pin keys exact',set(req.get('evidence_pins',{}))=={'candidate_audit_static_test_receipt_sha256','candidate_evidence_audit_json_sha256','frozen_c11c_manifest_sha256','implementation_test_receipt_sha256','receipt_schema_fix_test_receipt_sha256','runtime_report_sha256','source_semantic_review_sha256','v2b_design_contract_sha256','v2b_runtime_contract_sha256','v2b_seed_matrix_sha256','v2c_source_frame_contract_sha256'})
    ck('source semantic review hash pinned',req.get('evidence_pins',{}).get('source_semantic_review_sha256')==SOURCE_REVIEW)
    ck('runtime contract hash pinned',req.get('evidence_pins',{}).get('v2b_runtime_contract_sha256')==RUNTIME_CONTRACT)
    ck('seed matrix hash pinned',req.get('evidence_pins',{}).get('v2b_seed_matrix_sha256')==MATRIX)
    ck('V2-C source contract hash pinned',req.get('evidence_pins',{}).get('v2c_source_frame_contract_sha256')==V2C)
    ck('C11-C manifest hash pinned',req.get('evidence_pins',{}).get('frozen_c11c_manifest_sha256')==C11C)
    ck('runtime gate retained',req.get('runtime_acceptance_scope',{}).get('status')=='PASS_SAFE_PROJECTION_SEED_SENSITIVITY')
    ck('runtime source-frame scope retained',req.get('runtime_acceptance_scope',{}).get('scope')=='IN_MEMORY_SOURCE_FRAME_SAFE_PROJECTION_AND_HASH_ONLY_CANDIDATE_OBSERVATIONS')
    ck('source review approval count remains zero',src.get('review_summary',{}).get('approved_bindings')==0)
    ck('source review custom binding count remains zero',src.get('review_summary',{}).get('approved_custom_data_bindings')==0)
    ck('source review has six candidates',len(src.get('custom_data_candidate_reviews',[]))==6)
    ck('design has 81 source pins',len(design.get('source_pins',[]))==81)
    ck('design has 9 authority pins',len(design.get('authority_input_pins',[]))==9)
    ck('matrix selector count remains nine',matrix.get('whole_increment_invocations',{}).get('selector_count')==9)
    ck('runtime contract renderer lock preserved',runtimec.get('renderer')=='OFF' and runtimec.get('media_created') is False and runtimec.get('payload_materialized') is False)
    ck('C11-C manifest hash remains frozen',sha(frozenp)==C11C)

    ck('candidate decisions exactly six',len(rec.get('decisions',[]))==6)
    ck('decision IDs and fields exact',[(d.get('challenge_id'),d.get('field')) for d in rec['decisions']]==[(x[0],x[1]) for x in EXPECTED])
    ck('decision semantic types exactly map to request',[(c.get('challenge_id'),c.get('field'),c.get('semantic_type')) for c in req['candidates']]==[(x[0],x[1],x[2]) for x in EXPECTED])
    ck('all record candidates map to request',[(d.get('challenge_id'),d.get('field')) for d in rec['decisions']]==[(c.get('challenge_id'),c.get('field')) for c in req['candidates']])
    ck('four semantic acceptances',sum(d.get('semantic_decision')==ACCEPT for d in rec['decisions'])==4)
    ck('two policy blocks',sum(d.get('semantic_decision')==BLOCKED for d in rec['decisions'])==2)
    ck('no candidate rejected',all(d.get('semantic_decision')!='REJECT_CANDIDATE_SEMANTIC_DEFINITION' for d in rec['decisions']))
    ck('reviewer role operator',rec.get('reviewer_role')=='operator')
    try:
        parsed=datetime.fromisoformat(str(rec.get('reviewed_at','')).replace('Z','+00:00'))
        timestamp_valid=parsed.tzinfo is not None
    except ValueError: timestamp_valid=False
    ck('review timestamp ISO timezone-aware',timestamp_valid)
    ck('no binding authorization granted',rec.get('binding_authorization')=='NOT_GRANTED_BY_SEMANTIC_REVIEW')
    ck('no renderer projection authorization granted',rec.get('renderer_projection_authorization')=='NOT_GRANTED_BY_SEMANTIC_REVIEW')
    ck('notes contain future-spec-only boundary','futura especificación' in rec.get('notes','').lower())
    ck('notes explicitly deny bindings','no aprueba bindings' in rec.get('notes','').lower())
    ck('notes keep 008/009 blocked','CHALLENGE_008' in rec.get('notes','') and 'CHALLENGE_009' in rec.get('notes',''))
    ck('decision record has no raw value keys',not any(k in rec for k in ('raw_candidate_values','candidate_values','custom_data','observations')))

    for d, expected in zip(rec['decisions'],EXPECTED):
        cid,field,semantic_type,wanted=expected
        item_schema=sch.get('properties',{}).get('decisions',{}).get('items',{})
        ck(cid+' schema item strict',set(d.keys())==set(item_schema.get('required',[])))
        ck(cid+' identity and field',d.get('challenge_id')==cid and d.get('field')==field)
        ck(cid+' explicit decision',d.get('semantic_decision')==wanted)
        ck(cid+' meaningful rationale',isinstance(d.get('rationale'),str) and len(d['rationale'])>=20)
        ck(cid+' source semantics acknowledged',d.get('source_semantics_acknowledged') is True)
        ck(cid+' runtime evidence checked',d.get('runtime_evidence_checked') is True)
        ck(cid+' temporal policy acknowledged',d.get('temporal_policy_acknowledged') is True)
        ck(cid+' decision enum schema accepts value',d.get('semantic_decision') in item_schema.get('properties',{}).get('semantic_decision',{}).get('enum',[]))

    ck('CHALLENGE_003 rationale retains scalar coordinate','escalar X' in rec['decisions'][0]['rationale'] and 'PILOT_0X100' in rec['decisions'][0]['rationale'])
    ck('CHALLENGE_003 not independent seed oracle','no es un oráculo independiente' in rec['decisions'][0]['rationale'])
    ck('CHALLENGE_005 rationale retains per-run constant','por intento' in rec['decisions'][1]['rationale'])
    ck('CHALLENGE_005 not trajectory','No debe interpretarse como trayectoria' in rec['decisions'][1]['rationale'])
    ck('CHALLENGE_006 separated from catcher','catcher' in rec['decisions'][2]['rationale'])
    ck('CHALLENGE_006 fail closed semantics retained','fallo cerrado' in rec['decisions'][2]['rationale'])
    ck('CHALLENGE_007 distinct scanner','scanner' in rec['decisions'][3]['rationale'])
    ck('CHALLENGE_007 excludes distractor/scoring','distractores' in rec['decisions'][3]['rationale'] and 'scoring' in rec['decisions'][3]['rationale'])
    ck('CHALLENGE_008 still blocked by 11s/12s','11s' in rec['decisions'][4]['rationale'] and '12s' in rec['decisions'][4]['rationale'])
    ck('CHALLENGE_009 still blocked by 11s/12s','11s/12s' in rec['decisions'][5]['rationale'])
    ck('CHALLENGE_009 not target_count','displayed_count no es target_count' in rec['decisions'][5]['rationale'])

    ck('request candidates keep binding flags false',all(c.get('binding_authorized') is False and c.get('renderer_projection_approved') is False for c in req['candidates']))
    ck('request raw values false',req.get('raw_candidate_values_included') is False)
    ck('governance renderer OFF',req.get('governance_locks',{}).get('renderer')=='OFF')
    ck('governance media false',req.get('governance_locks',{}).get('media_created') is False)
    ck('governance payload false',req.get('governance_locks',{}).get('payload_materialized') is False)
    ck('governance candidate input inadmissible',req.get('governance_locks',{}).get('candidate_input_admissible') is False)
    ck('governance approved bindings zero',req.get('governance_locks',{}).get('approved_bindings')==0)
    ck('governance custom-data bindings zero',req.get('governance_locks',{}).get('approved_custom_data_bindings')==0)
    ck('governance release authority none',req.get('governance_locks',{}).get('release_authority')=='NONE')
    ck('CHALLENGE_008 temporal conflict remains',req['candidates'][4].get('temporal_review_status')=='BLOCKED_TIMEBASE_CONFLICT_SOURCE_FRAME_ONLY')
    ck('CHALLENGE_009 temporal conflict remains',req['candidates'][5].get('temporal_review_status')=='BLOCKED_TIMEBASE_CONFLICT_SOURCE_FRAME_ONLY')
    ck('global schema states no explicit approval',req.get('decision_record_policy',{}).get('explicit_binding_approval')=='NOT_GRANTED_BY_THIS_REVIEW')
    ck('accepted definitions only go to future binding spec','future binding-specification' in ' '.join(d['rationale'] for d in rec['decisions'][:4]).lower() or all(d['semantic_decision']==ACCEPT for d in rec['decisions'][:4]))

    print(f'C11D_V2B_CANDIDATE_SEMANTIC_DECISION_RECORD_TESTS={n}/{n}')
    print('C11D_V2B_CANDIDATE_SEMANTIC_DECISIONS=4_ACCEPTED_2_BLOCKED')
    print('C11D_V2B_BINDING_AUTHORIZATION=NOT_GRANTED')
    print('C11D_V2B_RENDERER_PROJECTION_AUTHORIZATION=NOT_GRANTED')
    return 0

if __name__=='__main__':
    try: raise SystemExit(main())
    except Exception as exc:
        print('ERROR: '+str(exc),file=sys.stderr)
        raise
