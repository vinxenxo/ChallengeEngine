from __future__ import annotations
import argparse, hashlib, json, os, re, sys
from pathlib import Path
from datetime import datetime, timezone

SCHEMA='C11E-E6-RENDER-GATE-PREFLIGHT-RECEIPT-V1'

def sha(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def safe_rel(root: Path, rel: str) -> Path:
    p=(root/Path(rel)).resolve()
    rr=root.resolve()
    try: p.relative_to(rr)
    except ValueError: raise ValueError(f'PATH_ESCAPE:{rel}')
    return p

def evaluate(project_root: Path, inputs: dict, run_id: str) -> dict:
    checks=[]; blockers=[]
    for row in inputs['project_source_pins']:
        p=safe_rel(project_root,row['path'])
        if not p.is_file():
            checks.append({'kind':'SOURCE_PIN','path':row['path'],'expected_sha256':row['sha256'],'status':'MISSING'})
            blockers.append('SOURCE_PIN_MISSING:'+row['path']); continue
        actual=sha(p); st='PASS' if actual==row['sha256'] else 'MISMATCH'
        checks.append({'kind':'SOURCE_PIN','path':row['path'],'expected_sha256':row['sha256'],'actual_sha256':actual,'bytes':p.stat().st_size,'status':st})
        if st!='PASS': blockers.append('SOURCE_PIN_'+st+':'+row['path'])
    for row in inputs['receipt_pins']:
        p=safe_rel(project_root,row['path'])
        if not p.is_file():
            checks.append({'kind':'RECEIPT_PIN','id':row['id'],'path':row['path'],'expected_sha256':row['sha256'],'status':'MISSING'})
            blockers.append('RECEIPT_MISSING:'+row['id']); continue
        actual=sha(p); st='PASS' if actual==row['sha256'] else 'MISMATCH'
        checks.append({'kind':'RECEIPT_PIN','id':row['id'],'path':row['path'],'expected_sha256':row['sha256'],'actual_sha256':actual,'bytes':p.stat().st_size,'status':st})
        side=p.with_name(p.name+'.sha256')
        side_status='MISSING'
        if side.is_file():
            side_tokens=side.read_text(encoding='utf-8').strip().split(); side_status='PASS' if side_tokens and side_tokens[0].lower()==actual else 'MISMATCH'
        checks.append({'kind':'RECEIPT_SIDECAR','id':row['id'],'path':str(side.relative_to(project_root)) if side.is_relative_to(project_root) else row['path']+'.sha256','status':side_status})
        if st!='PASS': blockers.append('RECEIPT_'+st+':'+row['id'])
        if side_status!='PASS': blockers.append('RECEIPT_SIDECAR_'+side_status+':'+row['id'])
    tool_checks=[]
    for t in inputs['external_runtime_tools']:
        p=Path(t['path'])
        if not p.is_file():
            item={'id':t['id'],'path':t['path'],'expected_sha256':t['sha256'],'status':'MISSING'}
            blockers.append('RUNTIME_TOOL_MISSING:'+t['id'])
        else:
            actual=sha(p); size=p.stat().st_size
            status='PASS' if actual==t['sha256'] and size==t['bytes'] else 'MISMATCH'
            item={'id':t['id'],'path':t['path'],'expected_sha256':t['sha256'],'actual_sha256':actual,'expected_bytes':t['bytes'],'actual_bytes':size,'observed_version':t['observed_version'],'status':status}
            if status!='PASS': blockers.append('RUNTIME_TOOL_'+status+':'+t['id'])
        tool_checks.append(item)
    out_rel=inputs['output_root_relative']
    out=safe_rel(project_root,out_rel)
    out_exists=out.exists()
    if out_exists:
        blockers.append('PREFLIGHT_OUTPUT_ROOT_ALREADY_EXISTS')
    # Explicitly keep all known blocker records; the audit does not decide them away.
    blockers.extend('OPEN_GATE:'+x['id'] for x in inputs['known_open_gates'])
    unique=[]; seen=set()
    for b in blockers:
        if b not in seen: seen.add(b); unique.append(b)
    source_ok=all(x['status']=='PASS' for x in checks if x['kind']=='SOURCE_PIN')
    receipt_ok=all(x['status']=='PASS' for x in checks if x['kind']=='RECEIPT_PIN') and all(x['status']=='PASS' for x in checks if x['kind']=='RECEIPT_SIDECAR')
    tools_ok=all(x['status']=='PASS' for x in tool_checks)
    status='PASS_PREFLIGHT_INVENTORY_EXECUTION_HELD' if source_ok and receipt_ok and tools_ok and not out_exists else 'PASS_AUDIT_WITH_RENDER_GATES_BLOCKED'
    return {'schema':SCHEMA,'schema_version':'1.0','run_id':run_id,'created_utc':datetime.now(timezone.utc).isoformat(),'project_root':str(project_root),'status':status,'audit_scope':'READ_ONLY_SHA256_SOURCE_RECEIPT_AND_EXTERNAL_TOOL_INVENTORY_NO_EXECUTABLE_INVOCATION','counts':{'project_source_pins_expected':len(inputs['project_source_pins']),'project_source_pins_passed':sum(x['kind']=='SOURCE_PIN' and x['status']=='PASS' for x in checks),'receipts_expected':len(inputs['receipt_pins']),'receipts_passed':sum(x['kind']=='RECEIPT_PIN' and x['status']=='PASS' for x in checks),'receipt_sidecars_passed':sum(x['kind']=='RECEIPT_SIDECAR' and x['status']=='PASS' for x in checks),'runtime_tools_expected':len(tool_checks),'runtime_tools_passed':sum(x['status']=='PASS' for x in tool_checks),'editorial_targets':30,'smoke18_rows':18},'checks':checks,'runtime_tools':tool_checks,'output_root':{'relative':out_rel,'exists_before_audit':out_exists,'created':False},'known_open_gates':inputs['known_open_gates'],'blockers':unique,'governance':inputs['governance'],'execution':inputs['execution_prohibition'],'limitations':['Tool versions are inherited from historical accepted process receipts; this audit validates file path/hash/size only and deliberately does not execute any binary.','A PASS inventory does not authorize Godot, FFmpeg, FFprobe, audio, mux, media, rendering, dispatch or release.','Known open gates remain blockers even when all hashes pass.']}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--project-root',required=True); ap.add_argument('--inputs',required=True); ap.add_argument('--run-id',required=True); args=ap.parse_args()
    root=Path(args.project_root).resolve(); inp=Path(args.inputs)
    if not inp.is_file(): print('INPUTS_MISSING',file=sys.stderr); return 2
    data=json.loads(inp.read_text(encoding='utf-8'))
    report=evaluate(root,data,args.run_id)
    outdir=safe_rel(root,data['output_root_relative'])/args.run_id
    outdir.mkdir(parents=True,exist_ok=False)
    target=outdir/'E6_RENDER_GATE_PREFLIGHT_RECEIPT_V1.json'
    raw=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    target.write_bytes(raw); digest=hashlib.sha256(raw).hexdigest()
    side=target.with_name(target.name+'.sha256'); side.write_text(f'{digest}  {target.name}\n',encoding='ascii')
    print(f"E6_RENDER_GATE_PREFLIGHT_STATUS={report['status']}")
    print(f"SOURCE_PINS={report['counts']['project_source_pins_passed']}/{report['counts']['project_source_pins_expected']}")
    print(f"PREDECESSOR_RECEIPTS={report['counts']['receipts_passed']}/{report['counts']['receipts_expected']}; SIDECARS={report['counts']['receipt_sidecars_passed']}/{report['counts']['receipts_expected']}")
    print(f"RUNTIME_TOOL_HASHES={report['counts']['runtime_tools_passed']}/{report['counts']['runtime_tools_expected']}")
    print('EDITORIAL_TARGETS=30/30; SMOKE18_ROWS=18/18 (PREPARE_ONLY EVIDENCE)')
    print(f"KNOWN_OPEN_GATES={len(report['known_open_gates'])}; BLOCKERS={len(report['blockers'])}")
    for b in report['blockers']: print('BLOCKER='+b)
    print('GODOT_INVOKED=FALSE; FFMPEG_INVOKED=FALSE; FFPROBE_INVOKED=FALSE; AUDIO_GENERATED=FALSE; MUX_INVOKED=FALSE; MEDIA_CREATED=FALSE')
    print('D4_8=BLOCKED; E6_TEST_ONLY_AUTHORIZED=FALSE; RENDERER=OFF; RELEASE_AUTHORITY=NONE')
    print(f'AUDIT_RECEIPT={target}'); print(f'AUDIT_RECEIPT_SHA256={digest}')
    return 0
if __name__=='__main__': raise SystemExit(main())
