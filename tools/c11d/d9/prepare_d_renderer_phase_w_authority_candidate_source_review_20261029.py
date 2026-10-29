#!/usr/bin/env python3
"""Phase W read-only authority-candidate human-review queue builder."""
from __future__ import annotations
import argparse, hashlib, json, os, re, sys
from datetime import datetime, timezone
from pathlib import Path

EXPECTED_U_SHA='4db4ab20040b68872c4501dc39dda61b7ca2d8716303a536dbdd4121929ec418'
EXPECTED_V_SHA='1c36ee0afc5bcb4a9ea5b9060487d172c9f251fe366205a8cdaaea2bfc31de67'
PRIORITIES=('HIGH_REVIEW_PRIORITY','MEDIUM_REVIEW_PRIORITY','LOW_REVIEW_PRIORITY')
TIMING=[{'challenge':'CHALLENGE_008','declared_total_duration_seconds':11,'phase_duration_sum_seconds':12,'status':'BLOCKER_NO_CORRECTION_INFERRED'},{'challenge':'CHALLENGE_009','declared_total_duration_seconds':11,'phase_duration_sum_seconds':12,'status':'BLOCKER_NO_CORRECTION_INFERRED'}]
GOV={'renderer':'OFF','approved_bindings':0,'approved_custom_data_bindings':0,'approved_renderer_projection_bindings':0,'release_authority':'NONE'}
def sha256_file(p:Path)->str:
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()
def safe_relative(v:str)->bool:
 if not isinstance(v,str) or not v or v.startswith(('/','\\')) or re.match(r'^[A-Za-z]:',v): return False
 parts=v.replace('\\','/').split('/')
 return all(x not in ('','.','..') for x in parts)
def contained(root:Path,rel:str)->Path:
 if not safe_relative(rel): raise ValueError('UNSAFE_RELATIVE_PATH='+str(rel))
 base=root.resolve(strict=True); target=(root/Path(rel.replace('\\','/'))).resolve(strict=False)
 if os.path.commonpath([str(base),str(target)])!=str(base): raise ValueError('PATH_ESCAPES_ROOT='+rel)
 return target
def validate_inputs(u:dict,v:dict,u_sha:str,v_sha:str)->None:
 if u_sha!=EXPECTED_U_SHA or v_sha!=EXPECTED_V_SHA: raise ValueError('INPUT_REPORT_PIN_MISMATCH')
 if u.get('phase')!='U' or u.get('status')!='CANDIDATE_TRIAGE_READY_FOR_HUMAN_REVIEW': raise ValueError('PHASE_U_STATUS_INVALID')
 if v.get('phase')!='V' or v.get('status')!='SOURCE_EVIDENCE_INVENTORY_READY_FOR_HUMAN_REVIEW': raise ValueError('PHASE_V_STATUS_INVALID')
 if u.get('no_global_absence_claim') is not True or v.get('no_global_absence_claim') is not True: raise ValueError('GLOBAL_ABSENCE_SCOPE_INVALID')
 if u.get('authority_adjudication')!='NOT_PERFORMED' or u.get('policy_adoption')!='NONE' or v.get('authority_adjudication')!='NOT_PERFORMED' or v.get('policy_adoption')!='NONE': raise ValueError('AUTHORITY_STATE_INVALID')
 for obj in (u,v):
  gov=obj.get('governance',{})
  for k,val in GOV.items():
   if gov.get(k)!=val: raise ValueError('GOVERNANCE_LOCK_MISMATCH='+k)
  if len(obj.get('timing_conflicts',[]))!=2: raise ValueError('TIMING_CONFLICT_COUNT_INVALID')
  for t in obj['timing_conflicts']:
   if t.get('declared_total_duration_seconds')!=11 or t.get('phase_duration_sum_seconds')!=12 or t.get('status')!='BLOCKER_NO_CORRECTION_INFERRED': raise ValueError('TIMING_CONFLICT_CHANGED')
 if len(u.get('candidates',[]))!=107 or len(v.get('candidates',[]))!=107: raise ValueError('EXPECTED_CANDIDATE_COUNT_107')
 if len(u.get('unsearched_documents',[]))!=7 or len(v.get('unsearched_documents',[]))!=7: raise ValueError('EXPECTED_UNSEARCHED_COUNT_7')
def make_candidate(c:dict,v:dict,actual_sha:str|None,actual_bytes:int|None,integrity:str)->dict:
 ve=v.get('candidate_by_path',{}).get(c.get('path'),{})
 return {'path':c.get('path'),'expected_sha256':c.get('sha256'),'expected_bytes':c.get('bytes'),'phase_v_actual_sha256':ve.get('actual_sha256'),'phase_v_actual_bytes':ve.get('actual_bytes'),'actual_sha256':actual_sha,'actual_bytes':actual_bytes,'source_integrity':integrity,'priority':c.get('priority'),'priority_score':c.get('priority_score',0),'matches':c.get('matches',[]),'excerpts':ve.get('excerpts',[]),'excerpt_status':ve.get('excerpt_status','NOT_IN_PHASE_V_RECORD'),'review_status':'NOT_REVIEWED','authority_finding':'UNDETERMINED','full_document_inspected':False,'authority_record_id':None,'issuer':None,'authority_basis':None,'decision_scope':None,'decision_option':None,'effective_date':None,'immutable_record_identity':None,'reviewer_notes':None}
def render_markdown(r:dict)->str:
 c=r['counts']; out=['# C11-D Phase W — Authority Candidate Human Review Queue','',f"- Status: `{r['status']}`",f"- Phase U input SHA-256: `{r['source_triage_sha256']}`",f"- Phase V input SHA-256: `{r['source_review_sha256']}`",'- Read-only review preparation; no candidate source is modified.','- Priority orders review only; it is not authority.','', '## Counts','',f"- Candidates: {c['candidates']} (high {c['high_priority']}, medium {c['medium_priority']}, low {c['low_priority']})",f"- Current source SHA/size matches: {c['source_hash_matches']}; mismatches {c['source_hash_mismatches']}; missing {c['source_files_missing']}",f"- Existing documents not inspected: {c['unsearched_existing']} of {c['unsearched_documents']}",'', '## High-priority excerpts (navigation only)','']
 for x in r['candidates']:
  if x['priority']!='HIGH_REVIEW_PRIORITY': continue
  out += [f"### `{x['path']}`",f"- current integrity `{x['source_integrity']}`; SHA-256 `{x['actual_sha256']}`; bytes `{x['actual_bytes']}`",f"- excerpt status `{x['excerpt_status']}`; review `NOT_REVIEWED`; finding `UNDETERMINED`; full document inspected `false`"]
  if not x['excerpts']: out.append('- No excerpt; inspect the complete file manually.')
  for e in x['excerpts']:
   out += ['',f"Lines {e.get('start_line')}–{e.get('end_line')} (match {e.get('match_line')}):",'```text',e.get('text',''),'```']
  out.append('')
 out += ['## Remaining candidate queue','', '| Priority | Path | Current integrity | Review | Finding |','|---|---|---|---|---|']
 for x in r['candidates']:
  if x['priority']=='HIGH_REVIEW_PRIORITY': continue
  out.append(f"| {x['priority']} | `{x['path']}` | `{x['source_integrity']}` | `NOT_REVIEWED` | `UNDETERMINED` |")
 out += ['', '## Seven mandatory content inspections','', '| Path | Reason | Current state | SHA-256 | Bytes | Content read by automation |','|---|---|---|---|---:|---|']
 for x in r['unsearched_documents']:
  out.append(f"| `{x['path']}` | {x['reason']} | `{x['current_file_state']}` | `{x['current_sha256']}` | {x['current_bytes']} | `false` |")
 out += ['', '## Authority threshold','', 'A candidate is not authority because of its filename, keyword matches, priority, test result, or appearance in an old report. Human review must inspect the full source and record issuer/delegation, exact decision scope and option, effective date/version, immutable identity/signature, and required downstream tests. Until then every finding remains `UNDETERMINED`.','', '## Governance locks','', '`renderer=OFF`; approved binding counts zero; release authority `NONE`; policy adoption `NONE`. CHALLENGE_008/009 remain blocked at 11 seconds declared versus 12 seconds phase sum. No global absence claim is made. C11-C remains authoritative.']
 return '\n'.join(out)+'\n'
def build(root:Path,u:dict,v:dict,u_sha:str,v_sha:str)->dict:
 validate_inputs(u,v,u_sha,v_sha)
 vby={x['path']:x for x in v['candidates']}
 if len(vby)!=len(v['candidates']): raise ValueError('PHASE_V_DUPLICATE_CANDIDATE_PATH')
 rows=[]; seen=set(); match=mismatch=missing=0
 for c in u['candidates']:
  rel=c.get('path')
  if not safe_relative(rel) or rel in seen: raise ValueError('PHASE_U_UNSAFE_OR_DUPLICATE_PATH='+str(rel))
  seen.add(rel)
  if rel not in vby: raise ValueError('PHASE_V_CANDIDATE_NOT_FOUND='+rel)
  ve=vby[rel]
  try:
   p=contained(root,rel)
   if not p.is_file(): integrity='MISSING'; missing+=1; ah=None; ab=None
   else:
    ab=p.stat().st_size; ah=sha256_file(p)
    if ab!=c.get('bytes') or ah!=c.get('sha256') or ab!=ve.get('actual_bytes') or ah!=ve.get('actual_sha256'): integrity='HASH_MISMATCH'; mismatch+=1
    else: integrity='MATCH'; match+=1
  except (OSError,ValueError): integrity='PATH_UNSAFE'; ah=None; ab=None; mismatch+=1
  rows.append(make_candidate(c, v, ah, ab, integrity))
 unrows=[]; un_seen=set(); un_existing=un_missing=0
 for x in u['unsearched_documents']:
  rel=x.get('path')
  if not safe_relative(rel) or rel in un_seen: raise ValueError('PHASE_U_UNSEARCHED_UNSAFE_OR_DUPLICATE='+str(rel))
  un_seen.add(rel)
  # The file contents are not read; only metadata and hash bytes are streamed.
  item={'path':rel,'reason':x.get('reason',x.get('classification','not provided')),'review_status':'NOT_INSPECTED','authority_finding':'UNDETERMINED','current_file_state':'MISSING','current_sha256':None,'current_bytes':None,'content_read':False}
  try:
   p=contained(root,rel)
   if p.is_file(): item.update(current_file_state='EXISTS_CONTENT_NOT_READ',current_sha256=sha256_file(p),current_bytes=p.stat().st_size);un_existing+=1
   else: un_missing+=1
  except (OSError,ValueError): item['current_file_state']='PATH_UNSAFE';un_missing+=1
  unrows.append(item)
 counts={'candidates':len(rows),'high_priority':sum(x['priority']=='HIGH_REVIEW_PRIORITY' for x in rows),'medium_priority':sum(x['priority']=='MEDIUM_REVIEW_PRIORITY' for x in rows),'low_priority':sum(x['priority']=='LOW_REVIEW_PRIORITY' for x in rows),'source_hash_matches':match,'source_hash_mismatches':mismatch,'source_files_missing':missing,'high_priority_excerpts':sum(bool(x['excerpts']) and x['priority']=='HIGH_REVIEW_PRIORITY' for x in rows),'unsearched_documents':len(unrows),'unsearched_existing':un_existing,'unsearched_missing':un_missing}
 status='SOURCE_QUEUE_READY_FOR_HUMAN_REVIEW' if match==107 and mismatch==0 and missing==0 and un_existing==7 and un_missing==0 else 'SOURCE_PIN_DRIFT_REQUIRES_RECONCILIATION'
 return {'schema_version':'1.0.0','phase':'W','status':status,'created_utc':datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),'source_triage_sha256':u_sha,'source_review_sha256':v_sha,'counts':counts,'scope':{'working_tree_only':True,'full_source_read_for_adjudication':False,'automated_adjudication':False,'priority_is_authority':False},'candidates':rows,'unsearched_documents':unrows,'governance':GOV,'timing_conflicts':TIMING,'no_global_absence_claim':True,'authority_adjudication':'NOT_PERFORMED','policy_adoption':'NONE','next_action':'HUMAN_REVIEW_COMPLETE_SOURCE_AND_UNSEARCHED_DOCUMENTS'}
def main()->int:
 ap=argparse.ArgumentParser(); ap.add_argument('--root',required=True);ap.add_argument('--triage-json',required=True);ap.add_argument('--review-json',required=True);ap.add_argument('--output-json',required=True);ap.add_argument('--output-md',required=True);args=ap.parse_args()
 try:
  u_path=Path(args.triage_json);v_path=Path(args.review_json); u_sha=sha256_file(u_path);v_sha=sha256_file(v_path)
  u=json.loads(u_path.read_text(encoding='utf-8-sig'));v=json.loads(v_path.read_text(encoding='utf-8-sig'))
  if u_sha!=EXPECTED_U_SHA: raise ValueError('PHASE_U_TRIAGE_SHA256_MISMATCH='+u_sha)
  if v_sha!=EXPECTED_V_SHA: raise ValueError('PHASE_V_REVIEW_SHA256_MISMATCH='+v_sha)
  v['candidate_by_path']={x['path']:x for x in v['candidates']}
  r=build(Path(args.root),u,v,u_sha,v_sha)
  Path(args.output_json).write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
  Path(args.output_md).write_text(render_markdown(r),encoding='utf-8')
  print('PHASE_W_AUTHORITY_CANDIDATE_REVIEW='+('PASS_READ_ONLY_QUEUE_READY' if r['status']=='SOURCE_QUEUE_READY_FOR_HUMAN_REVIEW' else 'SOURCE_PIN_DRIFT_REQUIRES_RECONCILIATION'))
  print('PHASE_W_CANDIDATES='+str(r['counts']['candidates']))
  print('PHASE_W_SOURCE_HASH_MATCHES='+str(r['counts']['source_hash_matches']))
  print('PHASE_W_SOURCE_HASH_MISMATCHES='+str(r['counts']['source_hash_mismatches']))
  print('PHASE_W_SOURCE_FILES_MISSING='+str(r['counts']['source_files_missing']))
  print('PHASE_W_UNSEARCHED_DOCUMENTS='+str(r['counts']['unsearched_documents']))
  print('PHASE_W_UNSEARCHED_CONTENT_READ=0')
  print('AUTHORITY_ADJUDICATION=NOT_PERFORMED; POLICY_ADOPTION=NONE')
  print('RUNTIME_REEXECUTED=false; GODOT_INVOKED=false; RENDERER=OFF; RELEASE_AUTHORITY=NONE')
  return 0 if r['status']=='SOURCE_QUEUE_READY_FOR_HUMAN_REVIEW' else 3
 except Exception as e:
  print('PHASE_W_ERROR='+str(e),file=sys.stderr);return 2
if __name__=='__main__': raise SystemExit(main())
