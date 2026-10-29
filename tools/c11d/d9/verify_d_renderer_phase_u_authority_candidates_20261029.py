#!/usr/bin/env python3
"""Verifies a Phase U triage output against its exact Phase T input report."""
import argparse, hashlib, json, re, sys
from pathlib import Path

def safe(path):
    if not isinstance(path,str) or not path or path.startswith(('/', '\\')) or re.match(r'^[A-Za-z]:',path): return False
    return all(p not in ('','.','..') for p in path.replace('\\','/').split('/'))
def main(argv=None):
    ap=argparse.ArgumentParser()
    ap.add_argument('--input-json',required=True,type=Path)
    ap.add_argument('--triage-json',required=True,type=Path)
    ap.add_argument('--triage-md',required=True,type=Path)
    a=ap.parse_args(argv)
    for p in (a.input_json,a.triage_json,a.triage_md):
        if not p.is_file(): raise ValueError('REQUIRED_FILE_MISSING='+str(p))
    raw=a.input_json.read_bytes(); src=json.loads(raw.decode('utf-8-sig')); tri=json.loads(a.triage_json.read_text(encoding='utf-8-sig'))
    expected_sha=hashlib.sha256(raw).hexdigest()
    if tri.get('phase')!='U' or tri.get('status')!='CANDIDATE_TRIAGE_READY_FOR_HUMAN_REVIEW': raise ValueError('TRIAGE_STATUS_INVALID')
    if tri.get('source_report_sha256')!=expected_sha: raise ValueError('SOURCE_REPORT_HASH_MISMATCH')
    if tri.get('source_scan_index_sha256')!=src.get('scan_index_sha256'): raise ValueError('SCAN_INDEX_HASH_MISMATCH')
    if tri.get('no_global_absence_claim') is not True: raise ValueError('GLOBAL_ABSENCE_CLAIM_INVALID')
    if tri.get('authority_adjudication')!='NOT_PERFORMED' or tri.get('policy_adoption')!='NONE': raise ValueError('ADJUDICATION_OR_POLICY_STATE_INVALID')
    sg=src.get('governance',{}); tg=tri.get('governance',{})
    for k,locked in [('renderer','OFF'),('approved_bindings',0),('approved_custom_data_bindings',0),('approved_renderer_projection_bindings',0),('release_authority','NONE')]:
        if sg.get(k)!=locked or tg.get(k)!=locked: raise ValueError('GOVERNANCE_LOCK_MISMATCH='+k)
    original=src.get('candidates',[]); results=tri.get('candidates',[])
    if len(original)!=len(results) or tri.get('counts',{}).get('candidates')!=len(original): raise ValueError('CANDIDATE_COUNT_MISMATCH')
    orig={x.get('path'):x for x in original}
    if len(orig)!=len(original): raise ValueError('SOURCE_CANDIDATE_PATH_DUPLICATE')
    found={}
    for x in results:
        p=x.get('path')
        if not safe(p): raise ValueError('TRIAGE_CANDIDATE_PATH_UNSAFE')
        if p in found: raise ValueError('TRIAGE_CANDIDATE_PATH_DUPLICATE')
        found[p]=x
        if p not in orig or x.get('sha256')!=orig[p].get('sha256') or x.get('bytes')!=orig[p].get('bytes') or x.get('matches')!=orig[p].get('matches'):
            raise ValueError('CANDIDATE_SOURCE_EVIDENCE_CHANGED='+str(p))
        if x.get('review_status')!='NOT_REVIEWED' or x.get('authority_finding')!='UNDETERMINED': raise ValueError('CANDIDATE_REVIEW_STATE_INVALID='+str(p))
        if x.get('priority') not in ('HIGH_REVIEW_PRIORITY','MEDIUM_REVIEW_PRIORITY','LOW_REVIEW_PRIORITY'): raise ValueError('CANDIDATE_PRIORITY_INVALID='+str(p))
    u0=src.get('unsearched_documents',[]); u1=tri.get('unsearched_documents',[])
    if len(u0)!=len(u1) or tri.get('counts',{}).get('unsearched_documents')!=len(u0): raise ValueError('UNSEARCHED_COUNT_MISMATCH')
    u0map={x.get('path'):x for x in u0}; u1map={x.get('path'):x for x in u1}
    if set(u0map)!=set(u1map): raise ValueError('UNSEARCHED_PATH_SET_CHANGED')
    for p,x in u1map.items():
        if not safe(p) or x.get('review_status')!='NOT_INSPECTED' or x.get('authority_finding')!='UNDETERMINED': raise ValueError('UNSEARCHED_REVIEW_STATE_INVALID='+str(p))
        for key,value in u0map[p].items():
            if x.get(key)!=value: raise ValueError('UNSEARCHED_SOURCE_EVIDENCE_CHANGED='+str(p))
    timings=src.get('timing_conflicts',[])
    if tri.get('timing_conflicts')!=timings or len(timings)!=2: raise ValueError('TIMING_CONFLICTS_CHANGED')
    if tri.get('counts',{}).get('scan_errors')!=len(src.get('scan_errors',[])): raise ValueError('SCAN_ERROR_COUNT_CHANGED')
    md=a.triage_md.read_text(encoding='utf-8-sig').lower()
    if 'not authority evidence' not in md or 'unsearched documents' not in md: raise ValueError('MARKDOWN_SCOPE_DISCLAIMER_MISSING')
    print('PHASE_U_TRIAGE_REPORT_VERIFICATION=PASS_EVIDENCE_PRESERVED')
    print('PHASE_U_VERIFIED_CANDIDATES='+str(len(results)))
    print('PHASE_U_VERIFIED_UNSEARCHED_DOCUMENTS='+str(len(u1)))
    print('PHASE_U_AUTHORITY_ADJUDICATION=NOT_PERFORMED; POLICY_ADOPTION=NONE')
    print('RUNTIME_REEXECUTED=false; GODOT_INVOKED=false; RENDERER=OFF; APPROVED_BINDINGS=0; RELEASE_AUTHORITY=NONE')
    return 0
if __name__=='__main__':
    try: raise SystemExit(main())
    except (OSError,ValueError,json.JSONDecodeError) as e:
        print('PHASE_U_TRIAGE_VERIFY_ERROR='+str(e),file=sys.stderr); raise SystemExit(2)
