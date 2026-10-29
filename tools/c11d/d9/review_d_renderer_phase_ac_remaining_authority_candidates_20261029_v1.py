#!/usr/bin/env python3
"""Build a byte-preserving review bundle for the 55 medium + 2 low Phase U candidates.
This is read-only with respect to repository source files; outputs are caller-supplied.
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys, zipfile
from pathlib import Path, PurePosixPath

EXPECTED_TRIAGE_SHA256 = '4db4ab20040b68872c4501dc39dda61b7ca2d8716303a536dbdd4121929ec418'
EXPECTED_COUNTS = {'all':107, 'high':50, 'medium':55, 'low':2, 'selected':57}
ALLOWED = {'MEDIUM_REVIEW_PRIORITY','LOW_REVIEW_PRIORITY'}

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()
def safe_relpath(value: str) -> bool:
    if not isinstance(value,str) or not value.strip() or value.startswith(('/', '\\')) or re.match(r'^[A-Za-z]:',value):
        return False
    p=PurePosixPath(value.replace('\\','/'))
    return all(part not in ('','.','..') for part in p.parts)
def select_remaining(triage: dict) -> list[dict]:
    if triage.get('phase') != 'U' or triage.get('status') != 'CANDIDATE_TRIAGE_READY_FOR_HUMAN_REVIEW':
        raise ValueError('PHASE_U_TRIAGE_STATUS_INVALID')
    if triage.get('no_global_absence_claim') is not True:
        raise ValueError('PHASE_U_GLOBAL_ABSENCE_SCOPE_INVALID')
    counts=triage.get('counts')
    if not isinstance(counts,dict): raise ValueError('PHASE_U_COUNTS_MISSING')
    expected={'candidates':107,'high_priority':50,'medium_priority':55,'low_priority':2,'unsearched_documents':7,'scan_errors':0}
    for key,value in expected.items():
        if counts.get(key) != value: raise ValueError('PHASE_U_COUNT_MISMATCH_'+key)
    governance=triage.get('governance',{})
    if governance.get('renderer')!='OFF' or governance.get('approved_bindings')!=0 or governance.get('approved_custom_data_bindings')!=0 or governance.get('approved_renderer_projection_bindings')!=0 or governance.get('release_authority')!='NONE':
        raise ValueError('PHASE_U_GOVERNANCE_LOCK_MISMATCH')
    candidates=triage.get('candidates')
    if not isinstance(candidates,list) or len(candidates)!=107: raise ValueError('PHASE_U_CANDIDATES_INVALID')
    seen=set(); picked=[]; buckets={'HIGH_REVIEW_PRIORITY':0,'MEDIUM_REVIEW_PRIORITY':0,'LOW_REVIEW_PRIORITY':0}
    for row in candidates:
        if not isinstance(row,dict): raise ValueError('PHASE_U_CANDIDATE_NOT_OBJECT')
        path=row.get('path'); digest=row.get('sha256'); size=row.get('bytes'); priority=row.get('priority')
        if not safe_relpath(path): raise ValueError('CANDIDATE_PATH_UNSAFE')
        norm=path.replace('\\','/')
        if norm in seen: raise ValueError('CANDIDATE_PATH_DUPLICATE')
        seen.add(norm)
        if not isinstance(digest,str) or not re.fullmatch(r'[0-9a-f]{64}',digest): raise ValueError('CANDIDATE_SHA256_INVALID')
        if not isinstance(size,int) or isinstance(size,bool) or size<0: raise ValueError('CANDIDATE_BYTES_INVALID')
        if priority not in {'HIGH_REVIEW_PRIORITY','MEDIUM_REVIEW_PRIORITY','LOW_REVIEW_PRIORITY'}: raise ValueError('CANDIDATE_PRIORITY_INVALID')
        buckets[priority]+=1
        if priority in ALLOWED:
            picked.append({**row,'path':norm,'priority':priority})
    if buckets != {'HIGH_REVIEW_PRIORITY':50,'MEDIUM_REVIEW_PRIORITY':55,'LOW_REVIEW_PRIORITY':2}:
        raise ValueError('PHASE_U_PRIORITY_DISTRIBUTION_MISMATCH')
    if len(picked)!=57: raise ValueError('PHASE_U_REMAINING_COUNT_MISMATCH')
    picked.sort(key=lambda r:(r['priority'],r['path'].casefold()))
    return picked

def build_bundle(root: Path, triage: dict, triage_sha256: str, output_json: Path, output_md: Path, content_zip: Path) -> dict:
    if triage_sha256 != EXPECTED_TRIAGE_SHA256: raise ValueError('PHASE_U_TRIAGE_SHA256_MISMATCH')
    picked=select_remaining(triage)
    root=root.resolve()
    prepared=[]
    for row in picked:
        src=(root / Path(*PurePosixPath(row['path']).parts)).resolve()
        if not src.is_relative_to(root): raise ValueError('CANDIDATE_ESCAPES_CHECKOUT')
        if not src.is_file(): raise ValueError('CANDIDATE_SOURCE_MISSING='+row['path'])
        data=src.read_bytes()
        if len(data)!=row['bytes']: raise ValueError('CANDIDATE_SOURCE_SIZE_MISMATCH='+row['path'])
        digest=sha256_bytes(data)
        if digest!=row['sha256']: raise ValueError('CANDIDATE_SOURCE_SHA256_MISMATCH='+row['path']+'='+digest)
        member='sources/'+row['path']
        prepared.append({'path':row['path'],'priority':row['priority'],'priority_score':row.get('priority_score'),
                         'priority_signals':row.get('priority_signals',[]),'bytes':len(data),'sha256':digest,
                         'archive_member':member,'data':data})
    for out in (output_json,output_md,content_zip):
        if out.exists(): raise ValueError('OUTPUT_DESTINATION_EXISTS='+str(out))
    output_json.parent.mkdir(parents=True,exist_ok=True); output_md.parent.mkdir(parents=True,exist_ok=True); content_zip.parent.mkdir(parents=True,exist_ok=True)
    manifest={'schema_version':1,'phase':'AC','source_triage_sha256':triage_sha256,
              'counts':{'medium_priority':55,'low_priority':2,'bundled_sources':57,'source_hash_matches':57,'source_hash_mismatches':0,'source_files_missing':0},
              'sources':[{k:v for k,v in r.items() if k!='data'} for r in prepared],
              'governance':{'renderer':'OFF','approved_bindings':0,'approved_custom_data_bindings':0,'approved_renderer_projection_bindings':0,'release_authority':'NONE'},
              'authority_adjudication':'NOT_PERFORMED','policy_adoption':'NONE'}
    with zipfile.ZipFile(content_zip,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        z.writestr('source_manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
        for r in prepared: z.writestr(r['archive_member'],r['data'])
    with zipfile.ZipFile(content_zip,'r') as z:
        bad=z.testzip()
        if bad is not None: raise ValueError('BUNDLE_CRC_FAILED='+bad)
        names=set(z.namelist())
        expected={'source_manifest.json'}|{r['archive_member'] for r in prepared}
        if names!=expected: raise ValueError('BUNDLE_MEMBER_SET_MISMATCH')
    zip_sha=sha256_file(content_zip); zip_bytes=content_zip.stat().st_size
    sources=[{k:v for k,v in r.items() if k!='data'} for r in prepared]
    result={'schema_version':1,'phase':'AC','title':'Remaining Authority Candidate Content Review Bundle',
            'status':'CONTENT_BUNDLE_READY_FOR_REMAINING_CANDIDATE_REVIEW','source_triage_path':'docs/current/d/C11D_PHASE_U_AUTHORITY_CANDIDATE_HUMAN_TRIAGE_RESULT_20261029_V1.json',
            'source_triage_sha256':triage_sha256,
            'counts':{'all_candidates':107,'high_priority_previously_reviewed':50,'previously_unsearched_documents_reviewed_in_phase_y':7,
                      'medium_priority':55,'low_priority':2,'bundled_sources':57,'source_hash_matches':57,'source_hash_mismatches':0,'source_files_missing':0},
            'sources':sources,'bundle':{'path':str(content_zip.resolve()),'sha256':zip_sha,'bytes':zip_bytes,'members':58,'source_members':57,
                                        'manifest_member':'source_manifest.json','crc':'PASS'},
            'prior_coverage':{'phase_y_high_priority_candidates':50,'phase_y_previously_unsearched_documents':7,
                              'medium_low_full_content_review':'PENDING_CURRENT_BUNDLE_REVIEW'},
            'authority_adjudication':'NOT_PERFORMED','policy_adoption':'NONE','no_global_absence_claim':True,
            'hard_locks':{'renderer':'OFF','media_created':False,'payload_materialized':False,'candidate_input_admissible':False,
                          'seed_domains_complete_for_candidate_input':False,'automatic_seed_generation':False,'master_seed':'NOT_ADOPTED',
                          'approved_bindings':0,'approved_custom_data_bindings':0,'approved_renderer_projection_bindings':0,
                          'D4.8':'BLOCKED','D9.10':'PREPARE_ONLY','D9.14':'BLOCKED','D9.16':'BLOCKED','D9.17':'BLOCKED_NO_GO',
                          'D10':'BLOCKED_FOR_PROMOTION','baseline_approval':'MISSING','freeze_eligible':False,'release_authority':'NONE'},
            'next_gate':'PHASE_AC_FULL_CONTENT_REVIEW_AND_CANDIDATE_FINDINGS'}
    result['bundle']['sha256']=zip_sha
    output_json.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    lines=['# C11-D Phase AC — Remaining Authority Candidate Content Bundle','',
           '- Status: `CONTENT_BUNDLE_READY_FOR_REMAINING_CANDIDATE_REVIEW`',
           f'- Phase U triage SHA-256: `{triage_sha256}`',
           f'- Bundle ZIP SHA-256: `{zip_sha}`',f'- Bundle bytes: {zip_bytes}',
           '- Scope: only the 55 medium-priority and 2 low-priority candidates; priority is not an authority finding.',
           '- All current source bytes matched recorded Phase U SHA-256 and byte length before bundling.',
           '- ZIP CRC and member set verified; all original bytes are stored under `sources/` and manifest pins each member.',
           '- No source file was written or changed; no runtime/Godot/renderer was invoked.',
           '- Authority adjudication: `NOT_PERFORMED`; policy adoption: `NONE`; no global absence claim.','',
           '## Sources (57)','']
    for r in sources:
        lines.append(f"- `{r['priority']}` `{r['path']}` — {r['bytes']} bytes; SHA-256 `{r['sha256']}`; signals: {', '.join(r['priority_signals']) or 'none'}")
    lines += ['', '## Required review', '',
              'Read each complete source. Distinguish effective authority decisions from historical narrow decisions, drafts, proposals, tests, logs, stale records and unrelated keyword matches. For any claimed authority, verify issuer/role, delegation, exact decision scope/options, effective dates, signature/provenance, source pins and acceptance-test obligations.',
              'CHALLENGE_008/009 remain at declared 11 seconds versus a 12-second phase sum. No timing correction is inferred.',
              '', '## Hard locks', '', '`renderer=OFF`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `automatic_seed_generation=false`; `master_seed=NOT_ADOPTED`; approved binding counts remain zero; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `release_authority=NONE`. C11-C remains immutable production authority.','']
    output_md.write_text('\n'.join(lines),encoding='utf-8',newline='\n')
    return result

def main(argv=None):
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',required=True,type=Path)
    ap.add_argument('--triage-json',required=True,type=Path)
    ap.add_argument('--output-json',required=True,type=Path)
    ap.add_argument('--output-md',required=True,type=Path)
    ap.add_argument('--content-zip',required=True,type=Path)
    a=ap.parse_args(argv)
    try:
        raw=a.triage_json.read_bytes(); digest=sha256_bytes(raw)
        if digest!=EXPECTED_TRIAGE_SHA256: raise ValueError('PHASE_U_TRIAGE_SHA256_MISMATCH='+digest)
        triage=json.loads(raw.decode('utf-8-sig'))
        result=build_bundle(a.root,triage,digest,a.output_json,a.output_md,a.content_zip)
    except Exception as e:
        print('PHASE_AC_PREP_ERROR='+str(e),file=sys.stderr); return 2
    print('PHASE_AC_REMAINING_CANDIDATE_BUNDLE=PASS_READ_ONLY_BUNDLE_READY')
    print('PHASE_AC_ALL_CANDIDATES=107')
    print('PHASE_AC_PREVIOUSLY_REVIEWED_HIGH_PRIORITY=50')
    print('PHASE_AC_MEDIUM_PRIORITY=55')
    print('PHASE_AC_LOW_PRIORITY=2')
    print('PHASE_AC_BUNDLED_SOURCES=57')
    print('PHASE_AC_SOURCE_HASH_MATCHES=57; SOURCE_HASH_MISMATCHES=0; SOURCE_FILES_MISSING=0')
    print('PHASE_AC_CONTENT_REVIEW_BUNDLE='+str(a.content_zip.resolve()))
    print('PHASE_AC_CONTENT_BUNDLE_SHA256='+result['bundle']['sha256'])
    print('PHASE_AC_CONTENT_BUNDLE_BYTES='+str(result['bundle']['bytes']))
    print('AUTHORITY_ADJUDICATION=NOT_PERFORMED; POLICY_ADOPTION=NONE')
    print('RUNTIME_REEXECUTED=false; GODOT_INVOKED=false; RENDERER=OFF; RELEASE_AUTHORITY=NONE')
    return 0
if __name__=='__main__': raise SystemExit(main())
