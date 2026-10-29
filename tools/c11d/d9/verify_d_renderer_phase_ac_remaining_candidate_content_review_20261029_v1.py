#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re, sys, zipfile
from pathlib import Path
EXPECTED_BUNDLE_SHA='5ee6ec0f5a6b3a0884c22bbecfc98691269bd431adc896c088e7eb7f9d0b7f08'
EXPECTED_MANIFEST_SHA='bc8405ccba850a540ab00d50691462ef496f1ccda9586dda7f775ff09e5c7ac1'

def sha(b): return hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser()
 ap.add_argument('--review-json',required=True); ap.add_argument('--matrix-json',required=True); ap.add_argument('--source-bundle',required=True)
 a=ap.parse_args()
 r=json.loads(Path(a.review_json).read_text(encoding='utf-8')); m=json.loads(Path(a.matrix_json).read_text(encoding='utf-8'))
 bp=Path(a.source_bundle)
 data=bp.read_bytes()
 if sha(data)!=EXPECTED_BUNDLE_SHA or len(data)!=180653: raise ValueError('source bundle SHA/size mismatch')
 with zipfile.ZipFile(bp) as z:
  if z.testzip() is not None or len(z.infolist())!=58: raise ValueError('source bundle CRC/entry count mismatch')
  manifest_bytes=z.read('source_manifest.json')
  if sha(manifest_bytes)!=EXPECTED_MANIFEST_SHA: raise ValueError('source manifest SHA mismatch')
  sm=json.loads(manifest_bytes.decode('utf-8-sig'))
  if len(sm.get('sources',[]))!=57: raise ValueError('source manifest candidate count mismatch')
  by_path={x['path']:x for x in sm['sources']}
  if len(by_path)!=57: raise ValueError('duplicate source path')
  rows=r['source_dispositions']
  if len(rows)!=57 or len(m['source_dispositions'])!=57: raise ValueError('disposition row count mismatch')
  for x in rows:
   orig=by_path.get(x['path'])
   if orig is None: raise ValueError('source not in manifest: '+x['path'])
   raw=z.read(orig['archive_member'])
   if len(raw)!=x['bytes'] or sha(raw)!=x['sha256'] or x['sha256']!=orig['sha256']:
    raise ValueError('source byte/hash mismatch: '+x['path'])
  if set(by_path)!=set(x['path'] for x in rows): raise ValueError('source disposition coverage mismatch')
  pri={}
  for x in rows: pri[x['priority']]=pri.get(x['priority'],0)+1
  if pri!={'MEDIUM_REVIEW_PRIORITY':55,'LOW_REVIEW_PRIORITY':2}: raise ValueError('priority counts mismatch')
 if r['status']!='PASS_CONTENT_REVIEW_COMPLETE_NO_APPLICABLE_D_RENDER_AUTHORITY_FOUND': raise ValueError('review status mismatch')
 if r['governance']['renderer']!='OFF' or r['governance']['approved_bindings']!=0 or r['governance']['release_authority']!='NONE': raise ValueError('governance lock mismatch')
 if r['authority_conclusion']['applicable_authority_for_first_d_baseline_render']!='NONE_FOUND_IN_THE_57_PHASE_AC_REMAINING_CANDIDATES': raise ValueError('authority conclusion mismatch')
 print('PHASE_AC_CONTENT_REVIEW_VERIFICATION=PASS_ALL_57_SOURCE_BYTES_AND_DISPOSITIONS')
 print('PHASE_AC_VERIFIED_CANDIDATES=57; MEDIUM=55; LOW=2')
 print('PHASE_AC_AUTHORITY_FOR_D_RENDER=NONE_FOUND_IN_REMAINING_CANDIDATES')
 print('PHASE_AC_D914=LIMITED_C11C_QUALIFICATION_ONLY')
 print('PHASE_AC_RENDER_READINESS=BLOCKED; RENDERER=OFF; APPROVED_BINDINGS=0; RELEASE_AUTHORITY=NONE')
 print('NEXT_GATE=PHASE_AD_OPERATOR_AUTHORITY_EVIDENCE_OR_EXPLICIT_KEEP_BLOCKED_DECISION')
 return 0
if __name__=='__main__':
 try: raise SystemExit(main())
 except Exception as e:
  print('PHASE_AC_CONTENT_REVIEW_VERIFY_ERROR='+str(e),file=sys.stderr); raise SystemExit(2)
