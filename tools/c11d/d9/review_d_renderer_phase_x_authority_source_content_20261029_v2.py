#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os, re, sys, zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

U_SHA='4db4ab20040b68872c4501dc39dda61b7ca2d8716303a536dbdd4121929ec418'
V_SHA='1c36ee0afc5bcb4a9ea5b9060487d172c9f251fe366205a8cdaaea2bfc31de67'
W_SHA='ee46f59a85b6b006115b239d5b628ad07f64c9f15b858e739b81c2d2285a239f'
W_MD_SHA='b3259f7389d1c3196a11a3bbf17976d058dfccf92534d9a8b0b360778fef020b'
W_RECEIPT_SHA='98aeaa27d4f403b27b7c664dbbe422beea4d11462d773244413a018725c57871'
GOV={'renderer':'OFF','media_created':False,'payload_materialized':False,'candidate_input_admissible':False,'seed_domains_complete_for_candidate_input':False,'automatic_seed_generation':False,'master_seed':'NOT_ADOPTED','approved_bindings':0,'approved_custom_data_bindings':0,'approved_renderer_projection_bindings':0,'release_authority':'NONE'}
TIMING=[{'challenge':'CHALLENGE_008','declared_total_duration_seconds':11,'phase_duration_sum_seconds':12,'status':'BLOCKER_NO_CORRECTION_INFERRED'},{'challenge':'CHALLENGE_009','declared_total_duration_seconds':11,'phase_duration_sum_seconds':12,'status':'BLOCKER_NO_CORRECTION_INFERRED'}]
MAX_FILE=10*1024*1024
MAX_TOTAL=100*1024*1024
SENSITIVE_RE=re.compile(r'(^|[/\\])\.env($|\.)|secret|credential|password|private[_-]?key|\.pfx$|\.p12$|\.pem$|\.key$', re.I)

def sha_bytes(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def sha_file(p:Path)->str:
 h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()
def safe_rel(s:str)->bool:
 if not isinstance(s,str) or not s or '\x00' in s or '\\' in s or ':' in s or s.startswith('~'):return False
 p=PurePosixPath(s)
 return not p.is_absolute() and all(x not in ('','..','.') for x in p.parts)
def contained(root:Path,rel:str)->Path:
 if not safe_rel(rel):raise ValueError('UNSAFE_RELATIVE_PATH='+str(rel))
 rr=root.resolve(strict=True); p=(rr/Path(*PurePosixPath(rel).parts)).resolve(strict=True)
 if p!=rr and rr not in p.parents:raise ValueError('PATH_ESCAPES_ROOT='+rel)
 return p
def load_json(p:Path):return json.loads(p.read_text(encoding='utf-8-sig'))
def check_sha(p:Path,expected:str,label:str):
 actual=sha_file(p)
 if actual!=expected:raise ValueError(label+'_SHA256_MISMATCH='+actual)
 return actual
def bundle_name(kind:str,idx:int,path:str)->str:
 base=PurePosixPath(path).name
 base=re.sub(r'[^A-Za-z0-9._-]+','_',base)[:100] or 'source.bin'
 token=hashlib.sha256(path.encode('utf-8')).hexdigest()[:12]
 return f'{kind}/{idx:03d}_{token}_{base}'
def md_report(r:dict)->str:
 c=r['counts']; out=['# C11-D Phase X — Source Content Review Bundle','',f"- Status: `{r['status']}`",f"- Phase U triage SHA-256: `{r['source_pins']['phase_u_triage_sha256']}`",f"- Phase V review SHA-256: `{r['source_pins']['phase_v_review_sha256']}`",f"- Phase W queue SHA-256: `{r['source_pins']['phase_w_queue_sha256']}`",'','## Counts','',f"- Candidates recorded: {c['candidates']}; high-priority source files selected: {c['high_priority_candidates']}",f"- Unsearched documents selected: {c['unsearched_documents']}",f"- Bundled sources: {c['bundled_sources']}; SHA/size matches: {c['source_hash_matches']}; mismatches: {c['source_hash_mismatches']}; missing: {c['source_files_missing']}; excluded/not bundled: {c['excluded_or_not_bundled']}",f"- Content bundle SHA-256: `{r['bundle']['sha256']}` ({r['bundle']['bytes']} bytes)",'','## High-priority candidate originals','', '| # | Priority | Source path | Integrity | SHA-256 | Bytes | Bundle member | Review |','|---:|---|---|---|---|---:|---|---|']
 for i,x in enumerate(r['candidates'],1):
  if x['priority']!='HIGH_REVIEW_PRIORITY':continue
  out.append(f"| {i} | {x['priority']} | `{x['path']}` | `{x['integrity']}` | `{x['current_sha256']}` | {x['current_bytes']} | `{x['bundle_member']}` | `NOT_REVIEWED` |")
 out += ['','## Previously unsearched documents','', '| Source path | Reason | Integrity | SHA-256 | Bytes | Bundle member | Content adjudication |','|---|---|---|---|---:|---|---|']
 for x in r['unsearched_documents']:
  out.append(f"| `{x['path']}` | {x['reason']} | `{x['integrity']}` | `{x['current_sha256']}` | {x['current_bytes']} | `{x['bundle_member']}` | `NOT_REVIEWED` |")
 out += ['','## Governance source-field coverage','',f"- Phase U serialized lock fields: {', '.join(r['source_governance_contracts']['phase_u_fields'])}",f"- Phase V serialized lock fields: {', '.join(r['source_governance_contracts']['phase_v_fields'])}",f"- Phase W serialized lock fields: {', '.join(r['source_governance_contracts']['phase_w_fields'])}",'- Optional lock fields omitted by an upstream report are recorded as omitted, never inferred as an alternate value. The Phase X output carries the canonical full lock set.','','## Review rules','', 'The content ZIP stores original source bytes; each member is linked to a path/hash/size record in `content_manifest.json`. Do not execute files from the bundle. Inspect them as data. Source pin drift, size cap, or sensitive-name exclusions remain explicit and block a full bundle PASS. Priority and textual matches are not evidence of authority.','', 'Authority review remains `NOT_PERFORMED`; policy adoption `NONE`. Seven documents were not read during W preparation; Phase X now bundles original bytes, but full human inspection is still required.','', '## Governance locks','', '`renderer=OFF`; approved binding counters zero; release authority `NONE`; candidate input inadmissible; seed domains incomplete; master seed not adopted. CHALLENGE_008/009 remains declared 11 seconds versus phase sum 12 seconds. C11-C remains authoritative and immutable.']
 return '\n'.join(out)+'\n'
CORE_GOV={'renderer':'OFF','approved_bindings':0,'approved_custom_data_bindings':0,'approved_renderer_projection_bindings':0,'release_authority':'NONE'}
def validate_report_governance(obj:dict,name:str,require_core:bool=True):
 gov=obj.get('governance',{})
 if not isinstance(gov,dict):raise ValueError(name+'_GOVERNANCE_OBJECT_INVALID')
 # Compare every lock field that the upstream report actually serializes.
 # An omitted optional field is not interpreted as true, false, or permission.
 for key,val in GOV.items():
  if key in gov and gov[key]!=val:raise ValueError('GOVERNANCE_LOCK_MISMATCH='+name+':'+key)
 # The upstream V/W schemas are required to carry these operational lock fields.
 if require_core:
  for key,val in CORE_GOV.items():
   if gov.get(key)!=val:raise ValueError('GOVERNANCE_REQUIRED_LOCK_MISMATCH='+name+':'+key)
def validate_inputs(root:Path,u:dict,v:dict,w:dict):
 for name,obj in [('U',u),('V',v),('W',w)]:
  if obj.get('authority_adjudication')!='NOT_PERFORMED' or obj.get('policy_adoption')!='NONE':raise ValueError(name+'_AUTHORITY_STATE_INVALID')
  if obj.get('no_global_absence_claim') is not True:raise ValueError(name+'_GLOBAL_ABSENCE_SCOPE_INVALID')
  if len(obj.get('timing_conflicts',[]))!=2:raise ValueError(name+'_TIMING_CONFLICT_COUNT_INVALID')
  for t in obj['timing_conflicts']:
   if t.get('declared_total_duration_seconds')!=11 or t.get('phase_duration_sum_seconds')!=12 or t.get('status')!='BLOCKER_NO_CORRECTION_INFERRED':raise ValueError(name+'_TIMING_CONFLICT_CHANGED')
 validate_report_governance(u,'U',require_core=False)
 validate_report_governance(v,'V',require_core=True)
 validate_report_governance(w,'W',require_core=True)
 if len(u.get('candidates',[]))!=107 or len(v.get('candidates',[]))!=107 or len(w.get('candidates',[]))!=107:raise ValueError('CANDIDATE_COUNT_INVALID')
 if len(u.get('unsearched_documents',[]))!=7 or len(w.get('unsearched_documents',[]))!=7:raise ValueError('UNSEARCHED_COUNT_INVALID')
 if w.get('status')!='SOURCE_QUEUE_READY_FOR_HUMAN_REVIEW':raise ValueError('PHASE_W_QUEUE_STATUS_INVALID')
 wc=w['counts']
 if wc.get('source_hash_matches')!=107 or wc.get('source_hash_mismatches')!=0 or wc.get('source_files_missing')!=0 or wc.get('unsearched_existing')!=7 or wc.get('unsearched_missing')!=0:raise ValueError('PHASE_W_COUNTS_INVALID')
 if sum(x.get('priority')=='HIGH_REVIEW_PRIORITY' for x in w['candidates'])!=50:raise ValueError('PHASE_W_HIGH_COUNT_INVALID')
def build(root:Path,u:dict,v:dict,w:dict, pin:dict, content_zip:Path)->dict:
 validate_inputs(root,u,v,w)
 v_by={x['path']:x for x in v['candidates']}; w_by={x['path']:x for x in w['candidates']}
 if len(w_by)!=107:raise ValueError('PHASE_W_DUPLICATE_PATHS')
 bundle_entries=[]; candidates=[]; unsearched=[]; seen=set(); matches=mismatches=missing=excluded=total=0
 with zipfile.ZipFile(content_zip,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for i,c in enumerate(w['candidates'],1):
   rel=c.get('path')
   if not safe_rel(rel) or rel in seen:raise ValueError('CANDIDATE_PATH_INVALID_OR_DUPLICATE='+str(rel))
   seen.add(rel); actual_sha=None; actual_bytes=None; integrity='NOT_SELECTED'; member=None
   if c.get('priority')=='HIGH_REVIEW_PRIORITY':
    try:
     p=contained(root,rel)
     actual_bytes=p.stat().st_size; actual_sha=sha_file(p)
     if actual_sha!=c.get('actual_sha256') or actual_bytes!=c.get('actual_bytes') or actual_sha!=c.get('expected_sha256') or actual_bytes!=c.get('expected_bytes') or actual_sha!=v_by[rel].get('actual_sha256') or actual_bytes!=v_by[rel].get('actual_bytes'):
      integrity='HASH_MISMATCH';mismatches+=1
     else:
      integrity='MATCH';matches+=1
      if SENSITIVE_RE.search(rel): integrity='SENSITIVE_NAME_EXCLUDED';excluded+=1
      elif actual_bytes>MAX_FILE or total+actual_bytes>MAX_TOTAL: integrity='SIZE_CAP_EXCEEDED';excluded+=1
      else:
       member=bundle_name('high_priority_candidates',i,rel)
       z.write(p,member); total+=actual_bytes
       bundle_entries.append({'member':member,'source_path':rel,'sha256':actual_sha,'bytes':actual_bytes,'priority':c.get('priority'),'kind':'HIGH_PRIORITY_CANDIDATE'})
    except (OSError,ValueError) as e:
     integrity='MISSING_OR_UNSAFE';missing+=1
   candidates.append({'path':rel,'priority':c.get('priority'),'expected_sha256':c.get('expected_sha256'),'current_sha256':actual_sha,'expected_bytes':c.get('expected_bytes'),'current_bytes':actual_bytes,'integrity':integrity,'review_status':'NOT_REVIEWED','authority_finding':'UNDETERMINED','bundle_member':member})
  for i,x in enumerate(w['unsearched_documents'],1):
   rel=x.get('path')
   if not safe_rel(rel):raise ValueError('UNSEARCHED_PATH_INVALID='+str(rel))
   actual_sha=None; actual_bytes=None; integrity='MISSING'; member=None
   try:
    p=contained(root,rel);actual_bytes=p.stat().st_size;actual_sha=sha_file(p)
    if x.get('current_sha256')!=actual_sha or x.get('current_bytes')!=actual_bytes or x.get('current_file_state')!='EXISTS_CONTENT_NOT_READ':
     integrity='HASH_MISMATCH';mismatches+=1
    else:
     integrity='MATCH';matches+=1
     if SENSITIVE_RE.search(rel):integrity='SENSITIVE_NAME_EXCLUDED';excluded+=1
     elif actual_bytes>MAX_FILE or total+actual_bytes>MAX_TOTAL:integrity='SIZE_CAP_EXCEEDED';excluded+=1
     else:
      member=bundle_name('previously_unsearched_documents',i,rel)
      z.write(p,member);total+=actual_bytes
      bundle_entries.append({'member':member,'source_path':rel,'sha256':actual_sha,'bytes':actual_bytes,'priority':None,'kind':'PREVIOUSLY_UNSEARCHED_DOCUMENT','reason':x.get('reason','not supplied')})
   except (OSError,ValueError):integrity='MISSING_OR_UNSAFE';missing+=1
   unsearched.append({'path':rel,'reason':x.get('reason','not supplied'),'current_sha256':actual_sha,'current_bytes':actual_bytes,'integrity':integrity,'content_bytes_captured':bool(member),'human_content_reviewed':False,'bundle_member':member,'review_status':'NOT_REVIEWED','authority_finding':'UNDETERMINED'})
  manifest={'schema_version':'1.0.0','phase':'X','entries':bundle_entries,'source_pins':pin,'content_was_modified':False,'files_executed':False,'authority_adjudication':'NOT_PERFORMED','policy_adoption':'NONE'}
  manifest_bytes=(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n').encode('utf-8')
  z.writestr('content_manifest.json',manifest_bytes)

 bundled=len(bundle_entries)
 status='SOURCE_CONTENT_BUNDLE_READY_FOR_HUMAN_REVIEW' if matches==57 and mismatches==0 and missing==0 and excluded==0 and bundled==57 else 'SOURCE_CONTENT_BUNDLE_INCOMPLETE_RECONCILIATION_REQUIRED'
 summary={'candidates':len(candidates),'high_priority_candidates':sum(x.get('priority')=='HIGH_REVIEW_PRIORITY' for x in w['candidates']),'unsearched_documents':len(unsearched),'bundled_sources':bundled,'source_hash_matches':matches,'source_hash_mismatches':mismatches,'source_files_missing':missing,'excluded_or_not_bundled':excluded}
 bundle_sha=sha_file(content_zip); bundle_bytes=content_zip.stat().st_size
 report={'schema_version':'1.0.0','phase':'X','status':status,'created_utc':datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),'source_pins':pin,'counts':summary,'candidates':candidates,'unsearched_documents':unsearched,'bundle':{'path':str(content_zip),'sha256':bundle_sha,'bytes':bundle_bytes,'manifest_sha256':sha_bytes(manifest_bytes),'complete':status=='SOURCE_CONTENT_BUNDLE_READY_FOR_HUMAN_REVIEW'},'scope':{'root_only':True,'selected_full_sources':True,'candidate_source_files_modified':False,'automated_authority_adjudication':False,'no_global_absence_claim':True},'governance':GOV,'source_governance_contracts':{'phase_u_fields':sorted(u.get('governance',{}).keys()),'phase_v_fields':sorted(v.get('governance',{}).keys()),'phase_w_fields':sorted(w.get('governance',{}).keys()),'optional_lock_fields_not_serialized':{'phase_u':sorted(k for k in GOV if k not in u.get('governance',{})),'phase_v':sorted(k for k in GOV if k not in v.get('governance',{})),'phase_w':sorted(k for k in GOV if k not in w.get('governance',{}))}},'timing_conflicts':TIMING,'authority_adjudication':'NOT_PERFORMED','policy_adoption':'NONE','no_global_absence_claim':True}
 return report
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',required=True);ap.add_argument('--triage-json',required=True);ap.add_argument('--source-review-json',required=True);ap.add_argument('--queue-json',required=True);ap.add_argument('--queue-md',required=True);ap.add_argument('--queue-receipt',required=True);ap.add_argument('--output-json',required=True);ap.add_argument('--output-md',required=True);ap.add_argument('--content-zip',required=True);a=ap.parse_args()
 try:
  root=Path(a.root).resolve(strict=True);u_path=Path(a.triage_json);v_path=Path(a.source_review_json);w_path=Path(a.queue_json);wm_path=Path(a.queue_md);wr_path=Path(a.queue_receipt)
  pins={'phase_u_triage_sha256':check_sha(u_path,U_SHA,'PHASE_U'),'phase_v_review_sha256':check_sha(v_path,V_SHA,'PHASE_V'),'phase_w_queue_sha256':check_sha(w_path,W_SHA,'PHASE_W_QUEUE'),'phase_w_markdown_sha256':check_sha(wm_path,W_MD_SHA,'PHASE_W_MARKDOWN'),'phase_w_receipt_sha256':check_sha(wr_path,W_RECEIPT_SHA,'PHASE_W_RECEIPT')}
  u=load_json(u_path);v=load_json(v_path);w=load_json(w_path)
  out=Path(a.output_json);md=Path(a.output_md);bundle=Path(a.content_zip)
  out.parent.mkdir(parents=True,exist_ok=True);md.parent.mkdir(parents=True,exist_ok=True);bundle.parent.mkdir(parents=True,exist_ok=True)
  r=build(root,u,v,w,pins,bundle)
  out.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');md.write_text(md_report(r),encoding='utf-8')
  print('PHASE_X_AUTHORITY_SOURCE_CONTENT_BUNDLE_V2='+('PASS_READ_ONLY_BUNDLE_READY' if r['status']=='SOURCE_CONTENT_BUNDLE_READY_FOR_HUMAN_REVIEW' else 'SOURCE_CONTENT_BUNDLE_INCOMPLETE_RECONCILIATION_REQUIRED'))
  for k in ['candidates','high_priority_candidates','unsearched_documents','bundled_sources','source_hash_matches','source_hash_mismatches','source_files_missing','excluded_or_not_bundled']:print('PHASE_X_'+k.upper()+'='+str(r['counts'][k]))
  print('PHASE_X_REVIEW_JSON='+str(out));print('PHASE_X_REVIEW_MARKDOWN='+str(md));print('PHASE_X_CONTENT_BUNDLE='+str(bundle));print('PHASE_X_CONTENT_BUNDLE_SHA256='+r['bundle']['sha256']);print('PHASE_X_CONTENT_BUNDLE_BYTES='+str(r['bundle']['bytes']))
  print('AUTHORITY_ADJUDICATION=NOT_PERFORMED; POLICY_ADOPTION=NONE');print('RUNTIME_REEXECUTED=false; GODOT_INVOKED=false; RENDERER=OFF; RELEASE_AUTHORITY=NONE')
  return 0 if r['status']=='SOURCE_CONTENT_BUNDLE_READY_FOR_HUMAN_REVIEW' else 3
 except Exception as e:print('PHASE_X_ERROR='+str(e),file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
