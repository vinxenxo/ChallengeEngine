#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, sys, zipfile
from pathlib import Path
from review_d_renderer_phase_ac_remaining_authority_candidates_20261029_v1 import EXPECTED_TRIAGE_SHA256, select_remaining, sha256_bytes, sha256_file

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--triage-json',required=True,type=Path); ap.add_argument('--review-json',required=True,type=Path); ap.add_argument('--review-md',required=True,type=Path); ap.add_argument('--content-zip',required=True,type=Path); a=ap.parse_args()
 try:
  triage_raw=a.triage_json.read_bytes(); triage_sha=sha256_bytes(triage_raw)
  if triage_sha!=EXPECTED_TRIAGE_SHA256: raise ValueError('TRIAGE_PIN_MISMATCH='+triage_sha)
  triage=json.loads(triage_raw.decode('utf-8-sig'))
  review=json.loads(a.review_json.read_text(encoding='utf-8-sig'))
  if review.get('phase')!='AC' or review.get('status')!='CONTENT_BUNDLE_READY_FOR_REMAINING_CANDIDATE_REVIEW': raise ValueError('REVIEW_STATUS_INVALID')
  selected=select_remaining(triage)
  if review.get('source_triage_sha256')!=triage_sha: raise ValueError('REVIEW_TRIAGE_PIN_MISMATCH')
  expected_by_path={row['path'].replace('\\','/'):row for row in selected}
  review_sources=review.get('sources',[])
  review_by_path={row.get('path'):row for row in review_sources if isinstance(row,dict)}
  if set(review_by_path)!=set(expected_by_path) or len(review_sources)!=57: raise ValueError('REVIEW_SOURCE_PATH_SET_MISMATCH')
  for path, source_row in review_by_path.items():
   expected_row=expected_by_path[path]
   if source_row.get('sha256')!=expected_row.get('sha256') or source_row.get('bytes')!=expected_row.get('bytes') or source_row.get('priority')!=expected_row.get('priority'):
    raise ValueError('REVIEW_SOURCE_RECORD_MISMATCH='+path)
  counts=review.get('counts',{})
  expected={'all_candidates':107,'high_priority_previously_reviewed':50,'previously_unsearched_documents_reviewed_in_phase_y':7,'medium_priority':55,'low_priority':2,'bundled_sources':57,'source_hash_matches':57,'source_hash_mismatches':0,'source_files_missing':0}
  for k,v in expected.items():
   if counts.get(k)!=v: raise ValueError('REVIEW_COUNT_MISMATCH_'+k)
  if review.get('authority_adjudication')!='NOT_PERFORMED' or review.get('policy_adoption')!='NONE' or review.get('hard_locks',{}).get('renderer')!='OFF' or review.get('hard_locks',{}).get('release_authority')!='NONE': raise ValueError('REVIEW_GOVERNANCE_LOCK_MISMATCH')
  if len(review.get('sources',[]))!=57: raise ValueError('REVIEW_SOURCE_RECORD_COUNT_MISMATCH')
  with zipfile.ZipFile(a.content_zip,'r') as z:
   bad=z.testzip()
   if bad is not None: raise ValueError('BUNDLE_CRC_FAILED='+bad)
   manifest=json.loads(z.read('source_manifest.json').decode('utf-8-sig'))
   entries=set(z.namelist())
   expected_entries={'source_manifest.json'}|{x['archive_member'] for x in review['sources']}
   if entries!=expected_entries or len(entries)!=58: raise ValueError('BUNDLE_MEMBER_SET_MISMATCH')
   if manifest.get('source_triage_sha256')!=triage_sha or len(manifest.get('sources',[]))!=57: raise ValueError('BUNDLE_MANIFEST_INVALID')
   if manifest.get('sources')!=review.get('sources'): raise ValueError('BUNDLE_MANIFEST_SOURCE_RECORDS_MISMATCH')
   for row in review['sources']:
    member=row['archive_member']; raw=z.read(member)
    if len(raw)!=row['bytes']: raise ValueError('BUNDLE_SOURCE_SIZE_MISMATCH='+row['path'])
    if sha256_bytes(raw)!=row['sha256']: raise ValueError('BUNDLE_SOURCE_SHA256_MISMATCH='+row['path'])
   if manifest.get('counts',{}).get('bundled_sources')!=57: raise ValueError('BUNDLE_MANIFEST_COUNT_INVALID')
  bundle_sha=sha256_file(a.content_zip)
  if review.get('bundle',{}).get('sha256')!=bundle_sha: raise ValueError('REVIEW_BUNDLE_SHA256_MISMATCH')
  if '57' not in a.review_md.read_text(encoding='utf-8-sig'): raise ValueError('REVIEW_MARKDOWN_COUNT_MISSING')
 except Exception as e:
  print('PHASE_AC_VERIFY_ERROR='+str(e),file=sys.stderr); return 2
 print('PHASE_AC_VERIFICATION=PASS_REMAINING_SOURCE_BYTES_PRESERVED')
 print('PHASE_AC_VERIFIED_REMAINING_CANDIDATES=57')
 print('PHASE_AC_VERIFIED_MEDIUM=55')
 print('PHASE_AC_VERIFIED_LOW=2')
 print('PHASE_AC_VERIFIED_BUNDLE_MEMBERS=58')
 print('PHASE_AC_AUTHORITY_ADJUDICATION=NOT_PERFORMED')
 print('PHASE_AC_RENDER_READINESS=BLOCKED')
 print('AUTHORITY_ADJUDICATION=PENDING; POLICY_ADOPTION=NONE; RENDERER=OFF; APPROVED_BINDINGS=0; RELEASE_AUTHORITY=NONE')
 return 0
if __name__=='__main__': raise SystemExit(main())
