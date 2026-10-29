#!/usr/bin/env python3
import argparse,hashlib,json,re,os,sys
from pathlib import Path
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def safe(v): return isinstance(v,str) and bool(v) and not v.startswith(('/','\\')) and not re.match(r'^[A-Za-z]:',v) and all(x not in ('','.','..') for x in v.replace('\\','/').split('/'))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--triage-json',required=True);ap.add_argument('--review-json',required=True);ap.add_argument('--queue-json',required=True);ap.add_argument('--queue-md',required=True);a=ap.parse_args()
 try:
  u=json.loads(Path(a.triage_json).read_text(encoding='utf-8-sig'));v=json.loads(Path(a.review_json).read_text(encoding='utf-8-sig'));q=json.loads(Path(a.queue_json).read_text(encoding='utf-8-sig'));md=Path(a.queue_md).read_text(encoding='utf-8-sig')
  if sha(a.triage_json)!=q['source_triage_sha256'] or sha(a.review_json)!=q['source_review_sha256']: raise ValueError('INPUT_REPORT_HASH_MISMATCH')
  if q.get('phase')!='W' or q.get('status')!='SOURCE_QUEUE_READY_FOR_HUMAN_REVIEW': raise ValueError('QUEUE_STATUS_INVALID')
  if len(q.get('candidates',[]))!=107 or len(u.get('candidates',[]))!=107 or len(v.get('candidates',[]))!=107: raise ValueError('CANDIDATE_COUNT_INVALID')
  if len(q.get('unsearched_documents',[]))!=7: raise ValueError('UNSEARCHED_COUNT_INVALID')
  um={x['path']:x for x in u['candidates']};vm={x['path']:x for x in v['candidates']};qm={x['path']:x for x in q['candidates']}
  if set(um)!=set(vm) or set(um)!=set(qm): raise ValueError('CANDIDATE_PATH_SET_CHANGED')
  for p,x in qm.items():
   if not safe(p) or x['source_integrity']!='MATCH' or x['review_status']!='NOT_REVIEWED' or x['authority_finding']!='UNDETERMINED' or x['full_document_inspected'] is not False: raise ValueError('CANDIDATE_STATE_INVALID='+p)
   if x['expected_sha256']!=um[p]['sha256'] or x['expected_bytes']!=um[p]['bytes'] or x['actual_sha256']!=vm[p]['actual_sha256'] or x['actual_bytes']!=vm[p]['actual_bytes']: raise ValueError('CANDIDATE_PROVENANCE_CHANGED='+p)
  if any(x.get('content_read') is not False or x.get('review_status')!='NOT_INSPECTED' or x.get('authority_finding')!='UNDETERMINED' for x in q['unsearched_documents']): raise ValueError('UNSEARCHED_STATE_INVALID')
  if q['governance'].get('renderer')!='OFF' or q['governance'].get('release_authority')!='NONE' or any(q['governance'].get(k)!=0 for k in ('approved_bindings','approved_custom_data_bindings','approved_renderer_projection_bindings')): raise ValueError('GOVERNANCE_LOCK_BROKEN')
  if q.get('authority_adjudication')!='NOT_PERFORMED' or q.get('policy_adoption')!='NONE' or q.get('no_global_absence_claim') is not True: raise ValueError('AUTHORITY_SCOPE_INVALID')
  if 'Seven mandatory content inspections' not in md or 'Authority threshold' not in md: raise ValueError('MARKDOWN_REVIEW_SECTIONS_MISSING')
  print('PHASE_W_QUEUE_VERIFICATION=PASS_EVIDENCE_AND_GOVERNANCE_PRESERVED');print('PHASE_W_VERIFIED_CANDIDATES=107');print('PHASE_W_VERIFIED_UNSEARCHED_DOCUMENTS=7');print('PHASE_W_SOURCE_HASH_MATCHES=107');print('PHASE_W_SOURCE_HASH_MISMATCHES=0');print('PHASE_W_AUTHORITY_ADJUDICATION=NOT_PERFORMED; POLICY_ADOPTION=NONE');print('RUNTIME_REEXECUTED=false; GODOT_INVOKED=false; RENDERER=OFF; APPROVED_BINDINGS=0; RELEASE_AUTHORITY=NONE');return 0
 except Exception as e: print('PHASE_W_VERIFY_ERROR='+str(e),file=sys.stderr);return 2
if __name__=='__main__': raise SystemExit(main())
