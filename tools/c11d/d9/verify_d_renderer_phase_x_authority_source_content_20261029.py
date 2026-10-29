#!/usr/bin/env python3
import argparse, hashlib, json, sys, zipfile
from pathlib import Path

def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--triage-json',required=True);ap.add_argument('--source-review-json',required=True);ap.add_argument('--queue-json',required=True);ap.add_argument('--review-json',required=True);ap.add_argument('--review-md',required=True);ap.add_argument('--content-zip',required=True);a=ap.parse_args()
 try:
  expected_inputs={a.triage_json:'4db4ab20040b68872c4501dc39dda61b7ca2d8716303a536dbdd4121929ec418',a.source_review_json:'1c36ee0afc5bcb4a9ea5b9060487d172c9f251fe366205a8cdaaea2bfc31de67',a.queue_json:'ee46f59a85b6b006115b239d5b628ad07f64c9f15b858e739b81c2d2285a239f'}
  for path,expected in expected_inputs.items():
   if sha(path)!=expected:raise ValueError('PINNED_INPUT_HASH_MISMATCH='+path)
  u=json.loads(Path(a.triage_json).read_text(encoding='utf-8-sig'));v=json.loads(Path(a.source_review_json).read_text(encoding='utf-8-sig'));w=json.loads(Path(a.queue_json).read_text(encoding='utf-8-sig'));r=json.loads(Path(a.review_json).read_text(encoding='utf-8-sig'))
  if r.get('status')!='SOURCE_CONTENT_BUNDLE_READY_FOR_HUMAN_REVIEW' or r.get('bundle',{}).get('complete') is not True:raise ValueError('CONTENT_BUNDLE_NOT_COMPLETE')
  if r.get('source_pins',{}).get('phase_u_triage_sha256')!='4db4ab20040b68872c4501dc39dda61b7ca2d8716303a536dbdd4121929ec418' or r.get('source_pins',{}).get('phase_v_review_sha256')!='1c36ee0afc5bcb4a9ea5b9060487d172c9f251fe366205a8cdaaea2bfc31de67' or r.get('source_pins',{}).get('phase_w_queue_sha256')!='ee46f59a85b6b006115b239d5b628ad07f64c9f15b858e739b81c2d2285a239f':raise ValueError('REVIEW_SOURCE_PINS_INVALID')
  if len(r.get('candidates',[]))!=107 or len(r.get('unsearched_documents',[]))!=7:raise ValueError('REVIEW_COUNTS_INVALID')
  if sum(c.get('priority')=='HIGH_REVIEW_PRIORITY' and c.get('bundle_member') for c in r['candidates'])!=50:raise ValueError('HIGH_PRIORITY_BUNDLE_COUNT_INVALID')
  if sum(bool(x.get('bundle_member')) for x in r['unsearched_documents'])!=7:raise ValueError('UNSEARCHED_BUNDLE_COUNT_INVALID')
  if r.get('counts',{}).get('source_hash_matches')!=57 or r['counts'].get('source_hash_mismatches')!=0 or r['counts'].get('source_files_missing')!=0 or r['counts'].get('excluded_or_not_bundled')!=0:raise ValueError('SOURCE_PRESERVATION_COUNTS_INVALID')
  if r.get('authority_adjudication')!='NOT_PERFORMED' or r.get('policy_adoption')!='NONE' or r.get('no_global_absence_claim') is not True:raise ValueError('AUTHORITY_SCOPE_INVALID')
  if r.get('governance',{}).get('renderer')!='OFF' or r['governance'].get('release_authority')!='NONE':raise ValueError('GOVERNANCE_LOCK_INVALID')
  if sha(a.content_zip)!=r['bundle'].get('sha256'):raise ValueError('CONTENT_BUNDLE_SHA_MISMATCH')
  with zipfile.ZipFile(a.content_zip) as z:
   bad=z.testzip()
   if bad:raise ValueError('CONTENT_BUNDLE_CRC_FAILURE='+bad)
   manifest=json.loads(z.read('content_manifest.json').decode('utf-8'))
   if len(manifest.get('entries',[]))!=57:raise ValueError('CONTENT_MANIFEST_ENTRY_COUNT_INVALID')
   if hashlib.sha256(z.read('content_manifest.json')).hexdigest()!=r['bundle'].get('manifest_sha256'):raise ValueError('CONTENT_MANIFEST_SHA_MISMATCH')
   for e in manifest['entries']:
    data=z.read(e['member'])
    if len(data)!=e['bytes'] or hashlib.sha256(data).hexdigest()!=e['sha256']:raise ValueError('BUNDLED_SOURCE_HASH_MISMATCH='+e['source_path'])
  print('PHASE_X_SOURCE_CONTENT_VERIFICATION=PASS_ALL_SOURCE_BYTES_PRESERVED')
  print('PHASE_X_VERIFIED_CANDIDATES=107')
  print('PHASE_X_VERIFIED_HIGH_PRIORITY_BUNDLE=50')
  print('PHASE_X_VERIFIED_UNSEARCHED_DOCUMENTS=7')
  print('PHASE_X_VERIFIED_BUNDLE_MEMBERS=57')
  print('AUTHORITY_ADJUDICATION=NOT_PERFORMED; POLICY_ADOPTION=NONE')
  print('RUNTIME_REEXECUTED=false; GODOT_INVOKED=false; RENDERER=OFF; APPROVED_BINDINGS=0; RELEASE_AUTHORITY=NONE')
  return 0
 except Exception as e:print('PHASE_X_VERIFY_ERROR='+str(e),file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
