from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
REQUIREMENTS_REL = Path('definitions/c11d/baseline/D_BASELINE_OPERATOR_EVIDENCE_REQUIREMENTS_V1.json')
D915_CONTRACT_REL = Path('definitions/c11d/d9/D9_15_GUI_OPERATIONAL_ACCEPTANCE_V1.json')
MANIFEST_REL = Path('release/C11C_FREEZE_PACKAGE_MANIFEST.json')
LEDGER_REL = Path('artifacts/evidence/d9_15_operator/D9_15_OPERATOR_EVIDENCE_LEDGER.json')
CHECKPOINT_REL = Path('docs/current/d/D9_15_OPERATOR_ACCEPTANCE_CHECKPOINT.json')
EXPECTED_MANIFEST_SHA256 = 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953'
ZERO_HASH = '0' * 64
ATTESTATION = 'I_CONFIRM_GUI_OBSERVED_AND_EVIDENCE_VERIFIED_NO_MEDIA'
SUPPORTED_SUFFIXES = {'.png', '.jpg', '.jpeg', '.txt', '.log', '.json'}
HASH_RE = re.compile(r'^[0-9a-f]{64}$')

class EvidenceError(RuntimeError):
    pass

def _canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')

def _seal(value: dict[str, Any], field: str) -> dict[str, Any]:
    result = dict(value); result.pop(field, None); result[field] = hashlib.sha256(_canonical(result)).hexdigest(); return result

def _sha_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def _load_json(path: Path) -> dict[str, Any]:
    try: data=json.loads(path.read_text(encoding='utf-8-sig'))
    except Exception as exc: raise EvidenceError(f'cannot read JSON {path}: {exc}') from exc
    if not isinstance(data,dict): raise EvidenceError(f'expected JSON object: {path}')
    return data

def _root(value: Path | str | None=None) -> Path:
    root=Path(value).resolve() if value is not None else ROOT
    if not root.is_dir(): raise EvidenceError(f'project root missing: {root}')
    return root

def _requirements(root: Path) -> dict[str, Any]:
    req=_load_json(root/REQUIREMENTS_REL)
    if req.get('schema')!='C11-D-BASELINE-OPERATOR-EVIDENCE-REQUIREMENTS-V1' or req.get('checkpoint')!='D9.15':
        raise EvidenceError('D9.15 evidence requirements identity mismatch')
    actual=dict(req); claimed=actual.pop('requirements_sha256',None)
    if claimed!=hashlib.sha256(_canonical(actual)).hexdigest(): raise EvidenceError('requirements contract seal mismatch')
    return req

def _required_keys(req: dict[str, Any]) -> set[tuple[str,str]]:
    rows=req.get('required_evidence_pairings')
    if not isinstance(rows,list) or not rows: raise EvidenceError('required pairing matrix is empty')
    keys={(str(row.get('surface_id')),str(row.get('capability_id'))) for row in rows if isinstance(row,dict)}
    if len(keys)!=len(rows): raise EvidenceError('required pairing matrix has duplicates or malformed rows')
    return keys

def _manifest_hash(root: Path) -> str:
    manifest=root/MANIFEST_REL
    if not manifest.is_file(): raise EvidenceError('immutable historical C11-C manifest is missing')
    digest=_sha_file(manifest)
    if digest!=EXPECTED_MANIFEST_SHA256: raise EvidenceError('immutable C11-C manifest SHA-256 mismatch')
    return digest

def _ledger_path(root: Path) -> Path: return root/LEDGER_REL

def _write_atomic(path: Path, data: dict[str,Any]) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    payload=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
    fd,tmp=tempfile.mkstemp(prefix=path.name+'.',suffix='.tmp',dir=str(path.parent))
    try:
        with os.fdopen(fd,'w',encoding='utf-8',newline='\n') as f:
            f.write(payload); f.flush(); os.fsync(f.fileno())
        os.replace(tmp,path)
    except Exception:
        try: os.unlink(tmp)
        except OSError: pass
        raise

def init_ledger(project_root: Path | str | None=None) -> dict[str,Any]:
    root=_root(project_root); req=_requirements(root); manifest_hash=_manifest_hash(root); path=_ledger_path(root)
    if path.exists(): raise EvidenceError(f'ledger already exists; append evidence rather than reinitialize: {LEDGER_REL.as_posix()}')
    entries=[]
    for row in req['required_evidence_pairings']:
        entries.append({**row,'status':'PENDING','latest_event_sequence':None,'evidence_sha256':None})
    ledger={
      'schema':'C11-D-D9.15-OPERATOR-EVIDENCE-LEDGER-V1','schema_version':'1.0','checkpoint':'D9.15',
      'candidate_id':'C11-D-BASELINE-CANDIDATE-0.1','created_at_utc':datetime.now(timezone.utc).isoformat(),
      'requirements_sha256':req['requirements_sha256'],'historical_c11c_manifest_sha256':manifest_hash,
      'evidence_root':req['evidence_root'],'required_pairing_count':len(entries),'pairings':entries,'events':[],
      'governance':{'renderer_activation':False,'production_execution':False,'media_created':False,'d4_8':'BLOCKED','release_authority':'NONE'},
    }
    ledger['ledger_sha256']=hashlib.sha256(_canonical(ledger)).hexdigest(); _write_atomic(path,ledger)
    return {'status':'INITIALIZED_PENDING','required_pairings':len(entries),'recorded_pass_pairings':0,'ledger_path':LEDGER_REL.as_posix(),'ledger_sha256':ledger['ledger_sha256'],'media_created':False,'release_authority':'NONE'}

def _resolve_evidence(root: Path, req: dict[str,Any], rel_value: str) -> tuple[Path,str,int]:
    if not isinstance(rel_value,str) or not rel_value.strip(): raise EvidenceError('evidence file path is required')
    raw=Path(rel_value)
    if raw.is_absolute() or '..' in raw.parts: raise EvidenceError('evidence path must be relative and cannot traverse')
    evidence_root=(root/str(req['evidence_root'])).resolve()
    path=(root/raw).resolve()
    try: path.relative_to(evidence_root)
    except ValueError as exc: raise EvidenceError('evidence file must be beneath the approved D9.15 evidence root') from exc
    if path.is_symlink() or not path.is_file(): raise EvidenceError(f'evidence file is missing or unsafe: {rel_value}')
    if path.suffix.lower() not in SUPPORTED_SUFFIXES: raise EvidenceError('unsupported evidence type; use PNG/JPG screenshot or TXT/LOG/JSON excerpt')
    size=path.stat().st_size
    if size<24: raise EvidenceError('evidence file is empty or implausibly short (<24 bytes)')
    return path,_sha_file(path),size

def _verify_ledger(root: Path, req: dict[str,Any], ledger: dict[str,Any]) -> dict[str,Any]:
    if ledger.get('schema')!='C11-D-D9.15-OPERATOR-EVIDENCE-LEDGER-V1' or ledger.get('checkpoint')!='D9.15': raise EvidenceError('operator evidence ledger identity mismatch')
    if ledger.get('requirements_sha256')!=req.get('requirements_sha256'): raise EvidenceError('ledger is bound to a different requirements contract')
    if ledger.get('historical_c11c_manifest_sha256')!=_manifest_hash(root): raise EvidenceError('ledger historical manifest binding mismatch')
    gov=ledger.get('governance',{})
    if gov!={'renderer_activation':False,'production_execution':False,'media_created':False,'d4_8':'BLOCKED','release_authority':'NONE'}: raise EvidenceError('ledger attempts to change protected governance')
    claimed=ledger.get('ledger_sha256'); temp=dict(ledger); temp.pop('ledger_sha256',None)
    if not isinstance(claimed,str) or claimed!=hashlib.sha256(_canonical(temp)).hexdigest(): raise EvidenceError('ledger seal mismatch')
    required=_required_keys(req); pairings=ledger.get('pairings'); events=ledger.get('events')
    if not isinstance(pairings,list) or {(str(x.get('surface_id')),str(x.get('capability_id'))) for x in pairings if isinstance(x,dict)}!=required: raise EvidenceError('ledger pairing matrix differs from canonical requirements')
    if not isinstance(events,list): raise EvidenceError('ledger events must be a list')
    prev=ZERO_HASH; latest={}; valid_events=0
    for idx,event in enumerate(events,1):
        if not isinstance(event,dict) or event.get('sequence')!=idx: raise EvidenceError(f'event sequence mismatch at {idx}')
        if event.get('previous_event_sha256')!=prev: raise EvidenceError(f'event hash-chain predecessor mismatch at {idx}')
        check=dict(event); claimed_event=check.pop('event_sha256',None)
        if not isinstance(claimed_event,str) or claimed_event!=hashlib.sha256(_canonical(check)).hexdigest(): raise EvidenceError(f'event seal mismatch at {idx}')
        key=(str(event.get('surface_id')),str(event.get('capability_id')))
        if key not in required: raise EvidenceError(f'event references non-required pairing: {key}')
        if event.get('observed_status') not in ('PASS','BLOCKED'): raise EvidenceError(f'invalid observed status at event {idx}')
        if event.get('operator_attestation')!=ATTESTATION: raise EvidenceError(f'operator attestation missing at event {idx}')
        if event.get('renderer_activation') is not False or event.get('production_execution') is not False or event.get('media_created') is not False or event.get('d4_8')!='BLOCKED' or event.get('release_authority')!='NONE': raise EvidenceError(f'governance violation in event {idx}')
        path,digest,size=_resolve_evidence(root,req,str(event.get('evidence_path','')))
        if digest!=event.get('evidence_sha256') or size!=event.get('evidence_bytes'): raise EvidenceError(f'evidence content changed after recording: {event.get("evidence_path")}')
        if not isinstance(event.get('action'),str) or len(event['action'].strip())<6: raise EvidenceError(f'event action missing at {idx}')
        recorded=event.get('recorded_at_utc')
        if not isinstance(recorded,str) or not recorded.endswith('+00:00'): raise EvidenceError(f'event timestamp must be UTC at {idx}')
        for hash_field in ('request_sha256','plan_sha256','lifecycle_sha256'):
            value=event.get(hash_field)
            if value is not None and (not isinstance(value,str) or not HASH_RE.fullmatch(value)): raise EvidenceError(f'invalid {hash_field} at event {idx}')
        prev=claimed_event; latest[key]=event; valid_events+=1
    for row in pairings:
        key=(str(row.get('surface_id')),str(row.get('capability_id'))); event=latest.get(key)
        row['status']=event['observed_status'] if event else 'PENDING'
        row['latest_event_sequence']=event['sequence'] if event else None
        row['evidence_sha256']=event['evidence_sha256'] if event else None
    passed=sum(1 for key in required if key in latest and latest[key]['observed_status']=='PASS')
    blocked=sum(1 for key in required if key in latest and latest[key]['observed_status']=='BLOCKED')
    pending=len(required)-passed-blocked
    return {'required':len(required),'passed':passed,'blocked':blocked,'pending':pending,'events':valid_events,'complete':passed==len(required) and blocked==0 and pending==0,'latest_events':latest}

def inspect_ledger(project_root: Path | str | None=None) -> dict[str,Any]:
    root=_root(project_root); req=_requirements(root); path=_ledger_path(root)
    if not path.is_file():
        return {'status':'D9.15_OPERATOR_EVIDENCE_REQUIRED','required_pairings':len(_required_keys(req)),'recorded_pass_pairings':0,'blocked_pairings':0,'pending_pairings':len(_required_keys(req)),'ledger_exists':False,'acceptance_checkpoint':'MISSING','freeze_eligible':False,'renderer_activation':False,'media_created':False,'d4_8':'BLOCKED','release_authority':'NONE'}
    ledger=_load_json(path); stats=_verify_ledger(root,req,ledger)
    checkpoint_status='MISSING'; checkpoint_path=root/CHECKPOINT_REL
    if checkpoint_path.is_file():
        ok,_reason=validate_acceptance_checkpoint(root, raise_on_error=False)
        checkpoint_status='PASS_CLOSED' if ok else 'INVALID_OR_STALE'
    status='D9.15_OPERATOR_EVIDENCE_PASS_CLOSED' if stats['complete'] and checkpoint_status=='PASS_CLOSED' else ('D9.15_OPERATOR_EVIDENCE_COMPLETE_CHECKPOINT_REQUIRED' if stats['complete'] else 'D9.15_OPERATOR_EVIDENCE_REQUIRED')
    return {'status':status,'required_pairings':stats['required'],'recorded_pass_pairings':stats['passed'],'blocked_pairings':stats['blocked'],'pending_pairings':stats['pending'],'events':stats['events'],'ledger_exists':True,'ledger_sha256':ledger['ledger_sha256'],'acceptance_checkpoint':checkpoint_status,'complete':stats['complete'],'freeze_eligible':False,'renderer_activation':False,'media_created':False,'d4_8':'BLOCKED','release_authority':'NONE'}

def record_event(project_root: Path | str | None, *, surface: str, capability: str, action: str, evidence_file: str, observed_status: str, operator: str, operator_attestation: str, request_sha256: str | None=None, plan_sha256: str | None=None, lifecycle_sha256: str | None=None) -> dict[str,Any]:
    root=_root(project_root); req=_requirements(root); manifest_hash=_manifest_hash(root); ledger_path=_ledger_path(root)
    if operator_attestation!=ATTESTATION: raise EvidenceError(f'explicit attestation required: {ATTESTATION}')
    if observed_status not in ('PASS','BLOCKED'): raise EvidenceError('observed status must be PASS or BLOCKED')
    if not isinstance(operator,str) or len(operator.strip())<2: raise EvidenceError('operator role/identifier required')
    if not isinstance(action,str) or len(action.strip())<6: raise EvidenceError('exact observed GUI action/route is required')
    key=(surface,capability); required=_required_keys(req)
    if key not in required: raise EvidenceError(f'unsupported surface/capability pairing: {surface}/{capability}')
    if not ledger_path.is_file(): init_ledger(root)
    ledger=_load_json(ledger_path); _verify_ledger(root,req,ledger)
    evidence_path,digest,size=_resolve_evidence(root,req,evidence_file)
    for name,value in (('request_sha256',request_sha256),('plan_sha256',plan_sha256),('lifecycle_sha256',lifecycle_sha256)):
        if value is not None and not HASH_RE.fullmatch(value): raise EvidenceError(f'{name} must be a 64-character SHA-256 hex digest')
    events=ledger['events']; previous=events[-1]['event_sha256'] if events else ZERO_HASH
    event={
      'sequence':len(events)+1,'surface_id':surface,'capability_id':capability,'action':action.strip(),
      'observed_status':observed_status,'recorded_at_utc':datetime.now(timezone.utc).isoformat(),
      'operator':operator.strip(),'operator_attestation':ATTESTATION,
      'evidence_path':Path(evidence_file).as_posix(),'evidence_sha256':digest,'evidence_bytes':size,
      'request_sha256':request_sha256,'plan_sha256':plan_sha256,'lifecycle_sha256':lifecycle_sha256,
      'previous_event_sha256':previous,'renderer_activation':False,'production_execution':False,
      'media_created':False,'d4_8':'BLOCKED','release_authority':'NONE',
    }
    event['event_sha256']=hashlib.sha256(_canonical(event)).hexdigest(); events.append(event)
    ledger['updated_at_utc']=datetime.now(timezone.utc).isoformat(); ledger.pop('ledger_sha256',None); ledger['ledger_sha256']=hashlib.sha256(_canonical(ledger)).hexdigest()
    _write_atomic(ledger_path,ledger)
    stats=_verify_ledger(root,req,ledger)
    return {'status':'RECORDED','sequence':event['sequence'],'surface':surface,'capability':capability,'observed_status':observed_status,'evidence_sha256':digest,'ledger_sha256':ledger['ledger_sha256'],'recorded_pass_pairings':stats['passed'],'required_pairings':stats['required'],'complete':stats['complete'],'media_created':False,'release_authority':'NONE'}

def finalize_acceptance(project_root: Path | str | None=None, *, operator_attestation: str) -> dict[str,Any]:
    root=_root(project_root); req=_requirements(root); ledger_path=_ledger_path(root)
    if operator_attestation!='I_CONFIRM_ALL_D915_PAIRINGS_REVIEWED_NO_MEDIA': raise EvidenceError('finalization requires explicit operator confirmation: I_CONFIRM_ALL_D915_PAIRINGS_REVIEWED_NO_MEDIA')
    if not ledger_path.is_file(): raise EvidenceError('operator evidence ledger missing')
    ledger=_load_json(ledger_path); stats=_verify_ledger(root,req,ledger)
    if not stats['complete']: raise EvidenceError(f'D9.15 cannot close; pass={stats["passed"]}/{stats["required"]}, blocked={stats["blocked"]}, pending={stats["pending"]}')
    cp_path=root/CHECKPOINT_REL
    if cp_path.exists(): raise EvidenceError('D9.15 acceptance checkpoint already exists; do not overwrite; adjudicate separately')
    manifest_hash=_manifest_hash(root)
    checkpoint={
      'schema':'C11-D-D9.15-OPERATOR-ACCEPTANCE-CHECKPOINT-V1','schema_version':'1.0','checkpoint':'D9.15',
      'status':'PASS_CLOSED','decision':'OPERATIONAL_GUI_ACCEPTANCE_ONLY',
      'candidate_id':'C11-D-BASELINE-CANDIDATE-0.1','accepted_at_utc':datetime.now(timezone.utc).isoformat(),
      'accepted_by':operator_attestation,'requirements_sha256':req['requirements_sha256'],
      'ledger_path':LEDGER_REL.as_posix(),'ledger_sha256':ledger['ledger_sha256'],
      'required_pairings':stats['required'],'passed_pairings':stats['passed'],'blocked_pairings':stats['blocked'],'pending_pairings':stats['pending'],
      'historical_c11c_manifest_sha256':manifest_hash,
      'd9_14_real_media_status':'BLOCKED_AS_REQUIRED','renderer_activation':False,'production_execution':False,'media_created':False,
      'd4_8':'BLOCKED','release_authority':'NONE','full_acceptance_authorized':False,'baseline_freeze_authorized':False,
      'limitations':['This checkpoint closes only D9.15 operator GUI operational acceptance.','It does not authorize renderer activation, media generation, D4.8, D9.14 real-media acceptance, D9.16 full acceptance, D9.17 closure, baseline freeze or release authority.'],
    }
    checkpoint['checkpoint_sha256']=hashlib.sha256(_canonical(checkpoint)).hexdigest()
    _write_atomic(cp_path,checkpoint)
    return {'status':'D9.15_OPERATOR_EVIDENCE_PASS_CLOSED','checkpoint_path':CHECKPOINT_REL.as_posix(),'checkpoint_sha256':checkpoint['checkpoint_sha256'],'ledger_sha256':ledger['ledger_sha256'],'pairings':'13/13','d9_14':'BLOCKED_AS_REQUIRED','media_created':False,'release_authority':'NONE'}

def validate_acceptance_checkpoint(project_root: Path | str | None=None, *, raise_on_error: bool=True) -> tuple[bool,str]:
    try:
        root=_root(project_root); req=_requirements(root); path=root/CHECKPOINT_REL; ledger_path=_ledger_path(root)
        if not path.is_file(): raise EvidenceError('D9.15 operator acceptance checkpoint missing')
        if not ledger_path.is_file(): raise EvidenceError('D9.15 ledger missing')
        cp=_load_json(path); ledger=_load_json(ledger_path); stats=_verify_ledger(root,req,ledger)
        claimed=cp.get('checkpoint_sha256'); body=dict(cp); body.pop('checkpoint_sha256',None)
        if claimed!=hashlib.sha256(_canonical(body)).hexdigest(): raise EvidenceError('D9.15 acceptance checkpoint seal mismatch')
        if cp.get('schema')!='C11-D-D9.15-OPERATOR-ACCEPTANCE-CHECKPOINT-V1' or cp.get('status')!='PASS_CLOSED' or cp.get('decision')!='OPERATIONAL_GUI_ACCEPTANCE_ONLY': raise EvidenceError('D9.15 checkpoint identity/status mismatch')
        if not stats['complete'] or cp.get('ledger_sha256')!=ledger.get('ledger_sha256') or cp.get('requirements_sha256')!=req.get('requirements_sha256'): raise EvidenceError('D9.15 checkpoint is stale or ledger incomplete')
        if cp.get('required_pairings')!=stats['required'] or cp.get('passed_pairings')!=stats['passed'] or cp.get('blocked_pairings')!=0 or cp.get('pending_pairings')!=0: raise EvidenceError('D9.15 checkpoint coverage is invalid')
        if cp.get('historical_c11c_manifest_sha256')!=_manifest_hash(root): raise EvidenceError('D9.15 checkpoint historical manifest binding mismatch')
        protected={'d9_14_real_media_status':'BLOCKED_AS_REQUIRED','renderer_activation':False,'production_execution':False,'media_created':False,'d4_8':'BLOCKED','release_authority':'NONE','full_acceptance_authorized':False,'baseline_freeze_authorized':False}
        if any(cp.get(k)!=v for k,v in protected.items()): raise EvidenceError('D9.15 checkpoint attempts to overstep its authority')
        return True,'D9.15_OPERATOR_EVIDENCE_PASS_CLOSED'
    except Exception as exc:
        if raise_on_error: raise
        return False,str(exc)

def main(argv: list[str] | None=None) -> int:
    p=argparse.ArgumentParser(description='Append-only D9.15 Windows GUI evidence ledger. No media, renderer or release authority.')
    p.add_argument('command',choices=['init','status','record','finalize'])
    p.add_argument('--root',default=str(ROOT))
    p.add_argument('--surface'); p.add_argument('--capability'); p.add_argument('--action'); p.add_argument('--evidence-file')
    p.add_argument('--observed-status',choices=['PASS','BLOCKED']); p.add_argument('--operator')
    p.add_argument('--operator-attestation'); p.add_argument('--request-sha256'); p.add_argument('--plan-sha256'); p.add_argument('--lifecycle-sha256')
    args=p.parse_args(argv)
    try:
        if args.command=='init': result=init_ledger(args.root)
        elif args.command=='status': result=inspect_ledger(args.root)
        elif args.command=='record':
            missing=[name for name in ('surface','capability','action','evidence_file','observed_status','operator','operator_attestation') if not getattr(args,name)]
            if missing: raise EvidenceError('missing required option(s): '+', '.join('--'+x.replace('_','-') for x in missing))
            result=record_event(args.root,surface=args.surface,capability=args.capability,action=args.action,evidence_file=args.evidence_file,observed_status=args.observed_status,operator=args.operator,operator_attestation=args.operator_attestation,request_sha256=args.request_sha256,plan_sha256=args.plan_sha256,lifecycle_sha256=args.lifecycle_sha256)
        else:
            if not args.operator_attestation: raise EvidenceError('finalize requires --operator-attestation')
            result=finalize_acceptance(args.root,operator_attestation=args.operator_attestation)
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 0
    except EvidenceError as exc:
        print(json.dumps({'status':'BLOCKED','error':str(exc),'renderer_activation':False,'media_created':False,'d4_8':'BLOCKED','release_authority':'NONE'},ensure_ascii=False,indent=2),file=sys.stderr)
        return 2

if __name__=='__main__': raise SystemExit(main())
