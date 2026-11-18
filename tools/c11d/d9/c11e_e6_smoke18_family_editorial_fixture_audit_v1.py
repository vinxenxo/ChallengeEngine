#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

FIXTURE_REL = 'definitions/c11e/test_only/C11E_E6_SMOKE18_FAMILY_EDITORIAL_FIXTURE_V1.json'
V2_RECEIPT_REL = 'artifacts/tests/c11e/e6_composition_readiness_v2/E6COMPREADINESSV2_20261118T214318Z_D41DD6C6/receipt/E6_COMPOSITION_READINESS_AUDIT_RECEIPT_V2.json'
V2_RECEIPT_SHA = '5470ee637b559977f266f1ed8131dbb1729bc9ef2225cddd58414efe3187035f'
CHALLENGE_BASE = 'artifacts/tests/c11e/e6_challenge_prepare_only_orchestrator/E6CHPREP_20261118T202841Z_37C6AE0E'
CHALLENGE_RECEIPT_REL = CHALLENGE_BASE + '/E6_CHALLENGE_PREPARE_ONLY_ORCHESTRATOR_RECEIPT_V1.json'
CHALLENGE_RECEIPT_SHA = 'b54a884f1574d22fa65ea198d279d9ba84bb3967adc87885213f7659a1b1c944'
CHALLENGE_INPUT_REL = 'definitions/c11d/production/C11E_E6_CHALLENGE_PREPARE_ONLY_INPUT_MANIFEST_V1.json'
CHALLENGE_INPUT_SHA = '4607831a94ecbb64b2f1cfb6ef3a7480e3f7315e8aee588a3ef9a93f97ce8878'
REQUAL_REL = 'artifacts/tests/c11e/e6_smoke18_reuse_requalification/E6SMK18REQUAL_20261118T141200Z_BA5AC046/E6_SMOKE18_REUSE_REQUALIFICATION_RECEIPT_V1.json'
REQUAL_SHA = '4d63b8caec7a975cc0362ee9d7a5924f5ab8371e8e8e1457e1d60956bf65ce33'
C11C_REL = 'release/C11C_FREEZE_PACKAGE_MANIFEST.json'
C11C_SHA = 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953'
D48_REL = 'definitions/c11d/production/C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V2.json'
D48_SHA = '0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07'

class AuditError(RuntimeError): pass

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8-sig'))

def require_file(root: Path, rel: str, expected: str) -> dict[str, Any]:
    p=root/Path(rel)
    if not p.is_file(): raise AuditError(f'REQUIRED_FILE_MISSING:{rel}')
    actual=sha256(p)
    if actual != expected: raise AuditError(f'SOURCE_PIN_MISMATCH:{rel}:{actual}')
    return {'path':rel,'sha256':actual,'bytes':p.stat().st_size,'status':'PASS'}

def build_plan(fixture: dict[str,Any], provenance: dict[str,Any]) -> dict[str,Any]:
    rows=fixture['rows']; family_map=fixture['family_fixtures']
    plan_rows=[]; target_count=0
    for row in rows:
        family=row['family']; ff=family_map[family]
        targets=[]
        for variant in row['probe_targets']:
            targets.append({'target_id':f"{row['scenario_id']}::{variant}",'variant':variant,
                            'fixture_id':ff['fixture_id'],'editorial':{
                              'title':ff['title'],'subtitle':ff['subtitle'],'call_to_action':ff['call_to_action']},
                            'target_status':'PREPARE_ONLY_BINDING_RECORD_NOT_RUNTIME_CONSUMPTION_PROOF'})
        target_count += len(targets)
        plan_rows.append({**row,'fixture_id':ff['fixture_id'],'consumer_route':ff['consumer_route'],
                          'consumer_status':ff['consumer_status'],'editorial':{
                            'title':ff['title'],'subtitle':ff['subtitle'],'call_to_action':ff['call_to_action']},
                          'targets':targets})
    return {
      'schema':'C11E-E6-SMOKE18-FAMILY-EDITORIAL-FIXTURE-PLAN-V1','schema_version':'1.0',
      'status':'PASS_PREPARE_ONLY_18_ROWS_30_TARGETS_RUNTIME_CONSUMPTION_NOT_PROVEN',
      'created_utc':datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),
      'fixture_id':fixture['fixture_id'],'fixture_sha256':provenance['fixture']['sha256'],
      'top_level_rows_expected':18,'top_level_rows_actual':len(plan_rows),
      'editorial_targets_expected':30,'editorial_targets_actual':target_count,
      'family_counts':{f:sum(1 for x in plan_rows if x['family']==f) for f in ('challenge','visual_loop','visual_drill')},
      'family_target_counts':{f:sum(len(x['targets']) for x in plan_rows if x['family']==f) for f in ('challenge','visual_loop','visual_drill')},
      'rows':plan_rows,'provenance':provenance,
      'default_distinctness':'E6-marked synthetic copy is deliberately authored as test copy; runtime comparison against each family default is still required.',
      'runtime_consumption':{
        'challenge':'NOT_PROVEN; must read the text through the pinned Challenge consumer and verify final composed pixels / exact text readback.',
        'visual_loop':'BLOCKED; no admitted D pixel consumer / postcompositor at V2 audit.',
        'visual_drill':'NOT_PROVEN; E4C consumer exists, but this plan has not invoked it or validated E6 fixture readback.'
      },
      'execution_boundary':fixture['execution_boundary']
    }

def write_json_pair(path: Path, obj: dict[str,Any]) -> tuple[str,str]:
    path.parent.mkdir(parents=True,exist_ok=True)
    data=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    path.write_bytes(data); digest=hashlib.sha256(data).hexdigest()
    side=path.with_name(path.name+'.sha256'); side.write_text(f'{digest}  {path.name}\n',encoding='ascii')
    return digest,str(side)

def run(root:Path,out:Path) -> dict[str,Any]:
    fixture_path=root/FIXTURE_REL
    fixture_sha=sha256(fixture_path) if fixture_path.is_file() else None
    if fixture_sha is None: raise AuditError('FIXTURE_MISSING')
    fixture=read_json(fixture_path)
    if fixture.get('schema')!='C11E-E6-SMOKE18-FAMILY-EDITORIAL-FIXTURE-V1': raise AuditError('FIXTURE_SCHEMA_MISMATCH')
    provenance={
      'fixture':{'path':FIXTURE_REL,'sha256':fixture_sha,'bytes':fixture_path.stat().st_size,'status':'PASS'},
      'composition_readiness_v2':require_file(root,V2_RECEIPT_REL,V2_RECEIPT_SHA),
      'challenge_prepare_only_receipt':require_file(root,CHALLENGE_RECEIPT_REL,CHALLENGE_RECEIPT_SHA),
      'challenge_input_manifest':require_file(root,CHALLENGE_INPUT_REL,CHALLENGE_INPUT_SHA),
      'reuse_requalification_receipt':require_file(root,REQUAL_REL,REQUAL_SHA),
      'c11c_manifest':require_file(root,C11C_REL,C11C_SHA),
      'd4_8_policy':require_file(root,D48_REL,D48_SHA)
    }
    v2=read_json(root/V2_RECEIPT_REL)
    ps=v2.get('source_pin_summary',{})
    if not (v2.get('status')=='PASS_AUDIT_ONLY_GAPS_IDENTIFIED_EXECUTION_HELD' and ps.get('expected')==17 and ps.get('passed')==17 and ps.get('failed')==0):
        raise AuditError('V2_PREDECESSOR_AUDIT_NOT_PASS_17_OF_17')
    ch=read_json(root/CHALLENGE_RECEIPT_REL)
    counts=ch.get('counts',{})
    if not (ch.get('status')=='PASS_PREPARE_ONLY_18_E1_INTENTS_18_D_ENVELOPES_EXECUTION_HELD' and counts.get('challenge_scenario_groups')==6 and counts.get('challenge_probe_subruns')==18 and counts.get('e1_intents')==18 and counts.get('d_envelopes')==18):
        raise AuditError('CHALLENGE_PREPARE_ONLY_PREDECESSOR_COUNTS_INVALID')
    # Verify the original plan remains intentionally unmodified and is not the fixture carrier.
    input_manifest=read_json(root/CHALLENGE_INPUT_REL)
    req=input_manifest.get('request_template',{})
    if req.get('personalization_enabled') is not False or req.get('editorial_profile') != {} or req.get('production_override') != {}:
        raise AuditError('CHALLENGE_INPUT_MANIFEST_UNEXPECTED_OVERRIDE_OR_PERSONALIZATION')
    exec_obj=ch.get('execution',{})
    forbidden=('godot_invoked','ffmpeg_invoked','ffprobe_invoked','audio_generated','mux_invoked','media_created','renderer_invoked','production_dispatch','batch_id_consumed')
    if any(exec_obj.get(k) is not False for k in forbidden): raise AuditError('PREDECESSOR_EXECUTION_BOUNDARY_VIOLATION')
    if fixture.get('execution_boundary',{}).get('e6_test_only_authorized') is not False: raise AuditError('FIXTURE_MUST_REMAIN_UNAUTHORIZED')
    if fixture.get('execution_boundary',{}).get('d4_8')!='BLOCKED': raise AuditError('D4_8_MUST_REMAIN_BLOCKED')
    plan=build_plan(fixture,provenance)
    if plan['top_level_rows_actual']!=18 or plan['editorial_targets_actual']!=30: raise AuditError('PLAN_ROW_OR_TARGET_COUNT_MISMATCH')
    if plan['family_counts']!={'challenge':6,'visual_loop':6,'visual_drill':6}: raise AuditError('FAMILY_ROW_COUNTS_MISMATCH')
    if plan['family_target_counts']!={'challenge':18,'visual_loop':6,'visual_drill':6}: raise AuditError('FAMILY_TARGET_COUNTS_MISMATCH')
    out.mkdir(parents=True,exist_ok=True)
    plan_path=out/'E6_SMOKE18_FAMILY_EDITORIAL_FIXTURE_PLAN_V1.json'
    plan_sha,plan_side=write_json_pair(plan_path,plan)
    receipt={
      'schema':'C11E-E6-SMOKE18-FAMILY-EDITORIAL-FIXTURE-AUDIT-RECEIPT-V1','schema_version':'1.0',
      'status':'PASS_PREPARE_ONLY_18_ROWS_30_TARGETS_RUNTIME_CONSUMPTION_NOT_PROVEN',
      'audit_scope':'READ_ONLY_SOURCE_RECONCILIATION_AND_TEST_ONLY_FIXTURE_PLAN_GENERATION',
      'created_utc':datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),
      'fixture_id':fixture['fixture_id'],'fixture_sha256':fixture_sha,
      'top_level_rows':18,'challenge_rows':6,'visual_loop_rows':6,'visual_drill_rows':6,
      'editorial_targets':30,'challenge_targets':18,'visual_loop_targets':6,'visual_drill_targets':6,
      'family_copy':fixture['family_fixtures'],
      'plan':{'path':plan_path.name,'sha256':plan_sha,'sidecar':Path(plan_side).name},
      'provenance':provenance,
      'runtime_consumption':plan['runtime_consumption'],
      'execution':{'godot_invoked':False,'ffmpeg_invoked':False,'ffprobe_invoked':False,'audio_generated':False,'mux_invoked':False,'media_created':False,'renderer_invoked':False,'dispatch_invoked':False,'batch_id_consumed':False},
      'governance':{'e6_accepted_scenarios':0,'matrix_frozen':False,'d4_8':'BLOCKED','e6_test_only_authorized':False,'renderer':'OFF','production_dispatch':False,'release_authority':'NONE','git_checks':'SKIPPED','commits':'OPERATOR_MANAGED','source_file_pins':'ENFORCED'},
      'limitations':['This is a fixture mapping/coverage plan, not a visual render or consumer readback.','Loop remains blocked pending implementation/admission of the D-owned pixel consumer.','The E6 marker makes copy visibly synthetic; compare against active family defaults during actual consumer readback.']
    }
    receipt_path=out/'E6_SMOKE18_FAMILY_EDITORIAL_FIXTURE_AUDIT_RECEIPT_V1.json'
    receipt_sha,receipt_side=write_json_pair(receipt_path,receipt)
    print('FAMILY_EDITORIAL_FIXTURE=PASS/3_FAMILIES')
    print('SMOKE18_TOP_LEVEL_ROWS=18/18')
    print('EDITORIAL_TARGETS=30/30')
    print('CHALLENGE_TARGETS=18/18; LOOP_TARGETS=6/6; DRILL_TARGETS=6/6')
    print('V2_SOURCE_PINS=17/17; PREDECESSOR_RECEIPTS=PASS')
    print('RUNTIME_EDITORIAL_CONSUMPTION=NOT_PROVEN')
    print('LOOP_D_COMPOSITOR=BLOCKED_NOT_ADMITTED')
    print('E6_ACCEPTED=0; MATRIX_FROZEN=FALSE; D4_8=BLOCKED; RENDERER=OFF; RELEASE_AUTHORITY=NONE')
    print(f'PLAN_SHA256={plan_sha}')
    print(f'AUDIT_RECEIPT={receipt_path}')
    print(f'AUDIT_RECEIPT_SHA256={receipt_sha}')
    return receipt

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--project-root',required=True)
    ap.add_argument('--output-root',required=True)
    a=ap.parse_args()
    try: run(Path(a.project_root).resolve(),Path(a.output_root).resolve())
    except Exception as e:
        print(f'FAMILY_EDITORIAL_AUDIT_BLOCKED={type(e).__name__}:{e}',file=sys.stderr); return 2
    return 0
if __name__=='__main__': raise SystemExit(main())
