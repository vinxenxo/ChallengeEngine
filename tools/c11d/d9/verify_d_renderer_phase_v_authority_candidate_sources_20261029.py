#!/usr/bin/env python3
"""Verifies Phase V source-review output against exact Phase U triage evidence."""
import argparse, hashlib, json, re, sys
from pathlib import Path

def safe(p):
    return isinstance(p,str) and bool(p) and not p.startswith(('/','\\')) and not re.match(r'^[A-Za-z]:',p) and all(x not in ('','.','..') for x in p.replace('\\','/').split('/'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main(argv=None):
    ap=argparse.ArgumentParser();ap.add_argument('--triage-json',required=True,type=Path);ap.add_argument('--review-json',required=True,type=Path);ap.add_argument('--review-md',required=True,type=Path);a=ap.parse_args(argv)
    for p in (a.triage_json,a.review_json,a.review_md):
        if not p.is_file(): raise ValueError('REQUIRED_FILE_MISSING='+str(p))
    tri_raw=a.triage_json.read_bytes();tri=json.loads(tri_raw.decode('utf-8-sig'));r=json.loads(a.review_json.read_text(encoding='utf-8-sig'))
    if r.get('phase')!='V' or r.get('source_triage_sha256')!=hashlib.sha256(tri_raw).hexdigest(): raise ValueError('TRIAGE_SOURCE_PIN_MISMATCH')
    if r.get('no_global_absence_claim') is not True or r.get('authority_adjudication')!='NOT_PERFORMED' or r.get('policy_adoption')!='NONE': raise ValueError('AUTHORITY_STATE_INVALID')
    if r.get('scope',{}).get('automated_adjudication') is not False or r.get('scope',{}).get('full_sources_modified') is not False: raise ValueError('SCOPE_LOCK_MISMATCH')
    originals={x['path']:x for x in tri['candidates']};results={x['path']:x for x in r['candidates']}
    if len(originals)!=len(tri['candidates']) or set(originals)!=set(results): raise ValueError('CANDIDATE_PATH_SET_CHANGED')
    if r['counts']['candidates']!=107 or len(results)!=107: raise ValueError('CANDIDATE_COUNT_MISMATCH')
    if (r['counts']['high_priority'],r['counts']['medium_priority'],r['counts']['low_priority'])!=(50,55,2): raise ValueError('PRIORITY_COUNTS_CHANGED')
    source_mismatches=r['counts'].get('source_hash_mismatches',-1); source_missing=r['counts'].get('source_files_missing',-1); source_matches=r['counts'].get('source_hash_matches',-1)
    if source_matches + source_mismatches + source_missing != 107: raise ValueError('SOURCE_INTEGRITY_TOTAL_MISMATCH')
    expected_status='SOURCE_PIN_DRIFT_REQUIRES_RECONCILIATION' if source_mismatches or source_missing else 'SOURCE_EVIDENCE_INVENTORY_READY_FOR_HUMAN_REVIEW'
    if r.get('status')!=expected_status: raise ValueError('SOURCE_INTEGRITY_STATUS_MISMATCH')
    for p,x in results.items():
        o=originals[p]
        if not safe(p) or x.get('expected_sha256')!=o.get('sha256') or x.get('expected_bytes')!=o.get('bytes') or x.get('priority')!=o.get('priority'): raise ValueError('SOURCE_METADATA_CHANGED='+p)
        if x.get('review_status')!='NOT_REVIEWED' or x.get('authority_finding')!='UNDETERMINED': raise ValueError('REVIEW_STATE_CHANGED='+p)
        if x.get('source_integrity')=='MATCH' and x.get('actual_sha256')!=x.get('expected_sha256'): raise ValueError('FALSE_SOURCE_MATCH='+p)
        if x.get('source_integrity')=='MATCH' and x.get('actual_bytes')!=x.get('expected_bytes'): raise ValueError('FALSE_SIZE_MATCH='+p)
        for ex in x.get('excerpts',[]):
            if len(ex.get('text',''))>1800 or ex.get('start_line',0)<1 or ex.get('end_line',0)<ex.get('start_line',0): raise ValueError('EXCERPT_BOUND_INVALID='+p)
    u0={x['path']:x for x in tri['unsearched_documents']};u1={x['path']:x for x in r['unsearched_documents']}
    if len(u0)!=7 or set(u0)!=set(u1): raise ValueError('UNSEARCHED_PATH_SET_CHANGED')
    for p,x in u1.items():
        if x.get('review_status')!='NOT_INSPECTED' or x.get('authority_finding')!='UNDETERMINED' or x.get('content_read') is not False: raise ValueError('UNSEARCHED_CONTENT_STATE_INVALID='+p)
    md=a.review_md.read_text(encoding='utf-8-sig')
    if 'Human review checklist' not in md or 'content not inspected' not in md.lower(): raise ValueError('MARKDOWN_LIMITATIONS_MISSING')
    if any(t.get('declared_total_duration_seconds')!=11 or t.get('phase_duration_sum_seconds')!=12 for t in r.get('timing_conflicts',[])): raise ValueError('TIMING_CONFLICT_CHANGED')
    print('PHASE_V_SOURCE_REVIEW_VERIFICATION=PASS_INVENTORY_PRESERVED')
    print('PHASE_V_VERIFIED_CANDIDATES=107');print('PHASE_V_VERIFIED_UNSEARCHED_DOCUMENTS=7')
    print('PHASE_V_SOURCE_HASH_MATCHES='+str(r['counts']['source_hash_matches']))
    print('PHASE_V_SOURCE_HASH_MISMATCHES='+str(r['counts']['source_hash_mismatches']))
    print('PHASE_V_SOURCE_INTEGRITY=' + ('PASS_ALL_107_CURRENT_SOURCE_PINS' if expected_status=='SOURCE_EVIDENCE_INVENTORY_READY_FOR_HUMAN_REVIEW' else 'BLOCKED_SOURCE_PIN_DRIFT_REQUIRES_RECONCILIATION'))
    print('PHASE_V_AUTHORITY_ADJUDICATION=NOT_PERFORMED; POLICY_ADOPTION=NONE')
    print('RUNTIME_REEXECUTED=false; GODOT_INVOKED=false; RENDERER=OFF; APPROVED_BINDINGS=0; RELEASE_AUTHORITY=NONE');return 0
if __name__=='__main__':
    try:raise SystemExit(main())
    except (OSError,ValueError,json.JSONDecodeError) as e:print('PHASE_V_SOURCE_REVIEW_VERIFY_ERROR='+str(e),file=sys.stderr);raise SystemExit(2)
