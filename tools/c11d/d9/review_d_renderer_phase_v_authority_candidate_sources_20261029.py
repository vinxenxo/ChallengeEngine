#!/usr/bin/env python3
"""Read-only Phase V current-source evidence inventory. Never adjudicates authority."""
from __future__ import annotations
import argparse, hashlib, json, os, re, sys
from datetime import datetime, timezone
from pathlib import Path

TEXT_EXTS={'.md','.json','.txt','.py','.ps1','.yaml','.yml','.toml','.csv','.xml','.ini','.cfg','.rst','.jsonc'}
MAX_TEXT_BYTES=524288
MAX_MATCHES=3
CONTEXT=3
MAX_EXCERPT_CHARS=1800

def sha256_bytes(data: bytes)->str:
    return hashlib.sha256(data).hexdigest()
def sha256_file(path: Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
    return h.hexdigest()
def safe_relative(value: str)->bool:
    if not isinstance(value,str) or not value or value.startswith(('/', '\\')) or re.match(r'^[A-Za-z]:',value): return False
    parts=value.replace('\\','/').split('/')
    return all(p not in ('','.','..') for p in parts)
def contained_path(root: Path, rel: str)->Path:
    if not safe_relative(rel): raise ValueError('UNSAFE_SOURCE_PATH='+str(rel))
    base=root.resolve(strict=True); target=(root/Path(rel.replace('\\','/'))).resolve(strict=False)
    if os.path.commonpath([str(base),str(target)]) != str(base): raise ValueError('SOURCE_PATH_ESCAPES_ROOT='+rel)
    return target
def bounded_excerpts(text: str, matches: list[dict])->list[dict]:
    lines=text.splitlines(); out=[]; seen=set()
    for m in matches[:MAX_MATCHES]:
        try: line=int(m.get('line',0))
        except (TypeError,ValueError): continue
        if line<1 or not lines: continue
        # T scanner match line numbers are one-based.
        start=max(1,line-CONTEXT); end=min(len(lines),line+CONTEXT)
        if (start,end) in seen: continue
        seen.add((start,end))
        body='\n'.join(f'{i}: {lines[i-1]}' for i in range(start,end+1))
        if len(body)>MAX_EXCERPT_CHARS: body=body[:MAX_EXCERPT_CHARS]+'\n[EXCERPT_TRUNCATED]'
        out.append({'match_line':line,'start_line':start,'end_line':end,'text':body})
    return out
def validate_triage(tri: dict)->None:
    if tri.get('phase')!='U' or tri.get('status')!='CANDIDATE_TRIAGE_READY_FOR_HUMAN_REVIEW': raise ValueError('PHASE_U_TRIAGE_STATUS_INVALID')
    if tri.get('no_global_absence_claim') is not True: raise ValueError('GLOBAL_ABSENCE_SCOPE_INVALID')
    if tri.get('authority_adjudication')!='NOT_PERFORMED' or tri.get('policy_adoption')!='NONE': raise ValueError('POLICY_STATE_INVALID')
    counts=tri.get('counts',{}); candidates=tri.get('candidates'); unsearched=tri.get('unsearched_documents')
    if not isinstance(candidates,list) or len(candidates)!=counts.get('candidates'): raise ValueError('CANDIDATE_COUNT_INVALID')
    if not isinstance(unsearched,list) or len(unsearched)!=counts.get('unsearched_documents'): raise ValueError('UNSEARCHED_COUNT_INVALID')
    gov=tri.get('governance',{})
    for k,v in {'renderer':'OFF','approved_bindings':0,'approved_custom_data_bindings':0,'approved_renderer_projection_bindings':0,'release_authority':'NONE'}.items():
        if gov.get(k)!=v: raise ValueError('GOVERNANCE_LOCK_MISMATCH='+k)
    if len(tri.get('timing_conflicts',[]))!=2: raise ValueError('TIMING_CONFLICT_COUNT_INVALID')
    for t in tri['timing_conflicts']:
        if t.get('declared_total_duration_seconds')!=11 or t.get('phase_duration_sum_seconds')!=12 or t.get('status')!='BLOCKER_NO_CORRECTION_INFERRED': raise ValueError('TIMING_CONFLICT_CHANGED')

def build_report(root: Path, triage: dict, triage_sha: str)->dict:
    validate_triage(triage)
    cand_out=[]; seen=set(); hash_match=0; hash_mismatch=0; missing=0; excerpt_count=0
    for c in triage['candidates']:
        rel=c.get('path')
        if not safe_relative(rel): raise ValueError('CANDIDATE_PATH_UNSAFE='+str(rel))
        if rel in seen: raise ValueError('CANDIDATE_PATH_DUPLICATE='+rel)
        seen.add(rel)
        entry={'path':rel,'expected_sha256':c.get('sha256'),'expected_bytes':c.get('bytes'),'actual_sha256':None,'actual_bytes':None,'source_integrity':'MISSING','priority':c.get('priority'),'priority_score':c.get('priority_score',0),'review_status':'NOT_REVIEWED','authority_finding':'UNDETERMINED','excerpt_status':'NOT_REQUESTED_FOR_THIS_BATCH','excerpts':[]}
        try:
            p=contained_path(root,rel)
            if not p.is_file():
                entry['source_integrity']='MISSING'; missing+=1; entry['excerpt_status']='SOURCE_MISSING'
            else:
                st=p.stat(); entry['actual_bytes']=st.st_size; entry['actual_sha256']=sha256_file(p)
                if st.st_size!=c.get('bytes') or entry['actual_sha256']!=c.get('sha256'):
                    entry['source_integrity']='HASH_MISMATCH'; hash_mismatch+=1; entry['excerpt_status']='SOURCE_PIN_MISMATCH_NO_EXCERPT'
                else:
                    entry['source_integrity']='MATCH'; hash_match+=1
                    if c.get('priority')=='HIGH_REVIEW_PRIORITY':
                        if p.suffix.lower() not in TEXT_EXTS:
                            entry['excerpt_status']='MATCH_BUT_EXTENSION_NOT_ALLOWLISTED'
                        elif st.st_size>MAX_TEXT_BYTES:
                            entry['excerpt_status']='MATCH_BUT_OVER_TEXT_CAP'
                        else:
                            raw=p.read_bytes()
                            if b'\x00' in raw:
                                entry['excerpt_status']='MATCH_BUT_BINARY_CONTENT'
                            else:
                                try: text=raw.decode('utf-8-sig')
                                except UnicodeDecodeError:
                                    try: text=raw.decode('cp1252')
                                    except UnicodeDecodeError:
                                        text=''; entry['excerpt_status']='MATCH_BUT_TEXT_DECODE_FAILED'
                                if text:
                                    entry['excerpts']=bounded_excerpts(text,c.get('matches',[]))
                                    entry['excerpt_status']='CURRENT_SOURCE_CONTEXT_EXTRACTED' if entry['excerpts'] else 'MATCH_NO_VALID_MATCH_LINE'
                                    if entry['excerpts']: excerpt_count+=1
                    else:
                        entry['excerpt_status']='SOURCE_HASH_VERIFIED_DEFERRED_TO_LATER_BATCH'
        except (OSError,ValueError) as exc:
            entry['source_integrity']='PATH_UNSAFE' if 'UNSAFE' in str(exc) or 'ESCAPES' in str(exc) else 'READ_ERROR'
            entry['excerpt_status']='SOURCE_NOT_EXTRACTED'
            hash_mismatch+=1
        cand_out.append(entry)
    un_out=[]; useen=set(); un_existing=0; un_missing=0
    for u in triage['unsearched_documents']:
        rel=u.get('path')
        if not safe_relative(rel): raise ValueError('UNSEARCHED_PATH_UNSAFE='+str(rel))
        if rel in useen: raise ValueError('UNSEARCHED_PATH_DUPLICATE='+rel)
        useen.add(rel)
        o={'path':rel,'reason':u.get('reason',u.get('classification','not provided')),'review_status':'NOT_INSPECTED','authority_finding':'UNDETERMINED','current_file_state':'MISSING','current_sha256':None,'current_bytes':None,'content_read':False}
        try:
            p=contained_path(root,rel)
            if p.is_file():
                o['current_file_state']='EXISTS_CONTENT_NOT_READ';o['current_sha256']=sha256_file(p);o['current_bytes']=p.stat().st_size;un_existing+=1
            else: un_missing+=1
        except (OSError,ValueError):
            o['current_file_state']='PATH_UNSAFE';un_missing+=1
        un_out.append(o)
    counts=triage['counts']
    status='SOURCE_EVIDENCE_INVENTORY_READY_FOR_HUMAN_REVIEW' if hash_match==len(cand_out) and hash_mismatch==0 and missing==0 else 'SOURCE_PIN_DRIFT_REQUIRES_RECONCILIATION'
    return {'schema_version':'1.0.0','phase':'V','status':status,'created_utc':datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),'source_triage_sha256':triage_sha,'source_scan_index_sha256':triage.get('source_scan_index_sha256'),'counts':{'candidates':len(cand_out),'high_priority':sum(x['priority']=='HIGH_REVIEW_PRIORITY' for x in cand_out),'medium_priority':sum(x['priority']=='MEDIUM_REVIEW_PRIORITY' for x in cand_out),'low_priority':sum(x['priority']=='LOW_REVIEW_PRIORITY' for x in cand_out),'source_hash_matches':hash_match,'source_hash_mismatches':hash_mismatch,'source_files_missing':missing,'high_priority_excerpts':excerpt_count,'unsearched_documents':len(un_out),'unsearched_existing':un_existing,'unsearched_missing':un_missing},'scope':{'working_tree_only':True,'git_history_searched':False,'external_files_searched':False,'full_sources_modified':False,'priority_is_authority':False,'automated_adjudication':False},'candidates':cand_out,'unsearched_documents':un_out,'timing_conflicts':triage['timing_conflicts'],'governance':triage['governance'],'no_global_absence_claim':True,'authority_adjudication':'NOT_PERFORMED','policy_adoption':'NONE','next_action':'HUMAN_REVIEW_VERIFIED_SOURCE_EXCERPTS_AND_UNSEARCHED_DOCUMENTS'}

def render_markdown(r: dict)->str:
    c=r['counts']; lines=['# C11-D Phase V — Authority Candidate Source Review','',f"- Status: `{r['status']}`",f"- Source triage SHA-256: `{r['source_triage_sha256']}`",f"- Source scan index SHA-256: `{r.get('source_scan_index_sha256')}`",'- Read-only current working-tree evidence; no source file is modified.','- Excerpts are bounded navigation aids, not authority decisions.','', '## Counts','',f"- Candidates: {c['candidates']} (high {c['high_priority']}, medium {c['medium_priority']}, low {c['low_priority']})",f"- Current source SHA and size matches: {c['source_hash_matches']}",f"- Hash mismatches: {c['source_hash_mismatches']}; missing candidate sources: {c['source_files_missing']}",f"- High-priority files with extracted current-source excerpts: {c['high_priority_excerpts']}",f"- Unsearched documents: {c['unsearched_documents']} (existing {c['unsearched_existing']}, missing {c['unsearched_missing']})",'', '## High-priority source context','']
    for x in r['candidates']:
        if x['priority']!='HIGH_REVIEW_PRIORITY': continue
        lines += [f"### `{x['path']}`",f"- expected SHA-256 `{x['expected_sha256']}`; actual `{x['actual_sha256']}`; integrity `{x['source_integrity']}`",f"- bytes expected/actual: `{x['expected_bytes']}` / `{x['actual_bytes']}`; excerpt status `{x['excerpt_status']}`; review `NOT_REVIEWED`; finding `UNDETERMINED`"]
        if not x['excerpts']: lines.append('- No current-source excerpt was emitted; inspect the complete source manually.')
        for e in x['excerpts']:
            lines += ['',f"Match line {e['match_line']} (lines {e['start_line']}-{e['end_line']}):",'```text',e['text'],'```']
        lines.append('')
    lines += ['## Medium and low-priority candidates','', '| Priority | Path | Source integrity | Review state |', '|---|---|---|---|']
    for x in r['candidates']:
        if x['priority']=='HIGH_REVIEW_PRIORITY': continue
        lines.append(f"| {x['priority']} | `{x['path']}` | `{x['source_integrity']}` | `NOT_REVIEWED / UNDETERMINED` |")
    lines += ['', '## Unsearched documents: content not inspected','', '| Path | Previous reason | Current state | Current SHA-256 | Bytes |', '|---|---|---|---|---:|']
    for x in r['unsearched_documents']:
        lines.append(f"| `{x['path']}` | {x['reason']} | `{x['current_file_state']}` | `{x['current_sha256']}` | {x['current_bytes']} |")
    lines += ['', '## Governance and timing locks','', '`renderer=OFF`; binding counts remain zero; `release_authority=NONE`; `authority_adjudication=NOT_PERFORMED`; `policy_adoption=NONE`.', 'CHALLENGE_008 and CHALLENGE_009 remain blocked: declared 11 seconds vs phase sum 12 seconds. This report makes no global absence claim.', '', '## Human review checklist', '', 'For each candidate, inspect the full file and establish issuer/role, exact decision IDs and scope, unambiguous adopted option/value, effective date/version, signature or immutable record identity, source pins and required gates. Distinguish an approval from a proposal, test fixture, example, rejection, stale note or unapproved suggestion. Review all seven unsearched document contents separately.', '']
    return '\n'.join(lines)

def main(argv=None)->int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',required=True,type=Path);ap.add_argument('--triage-json',required=True,type=Path);ap.add_argument('--output-json',required=True,type=Path);ap.add_argument('--output-md',required=True,type=Path)
    a=ap.parse_args(argv); raw=a.triage_json.read_bytes();tri=json.loads(raw.decode('utf-8-sig'));result=build_report(a.root,tri,sha256_bytes(raw))
    a.output_json.parent.mkdir(parents=True,exist_ok=True);a.output_md.parent.mkdir(parents=True,exist_ok=True)
    a.output_json.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');a.output_md.write_text(render_markdown(result),encoding='utf-8')
    print('PHASE_V_AUTHORITY_SOURCE_REVIEW=PASS_READ_ONLY_INVENTORY_READY' if result['status']=='SOURCE_EVIDENCE_INVENTORY_READY_FOR_HUMAN_REVIEW' else 'PHASE_V_AUTHORITY_SOURCE_REVIEW=SOURCE_PIN_DRIFT_REQUIRES_RECONCILIATION')
    print(f"PHASE_V_SOURCE_TRIAGE_SHA256={result['source_triage_sha256']}")
    print(f"PHASE_V_REVIEW_JSON={a.output_json.resolve()}");print(f"PHASE_V_REVIEW_MD={a.output_md.resolve()}")
    for k,v in result['counts'].items(): print(f'PHASE_V_{k.upper()}={v}')
    print('AUTHORITY_ADJUDICATION=NOT_PERFORMED; POLICY_ADOPTION=NONE')
    print('RUNTIME_REEXECUTED=false; GODOT_INVOKED=false; RENDERER=OFF; APPROVED_BINDINGS=0; RELEASE_AUTHORITY=NONE')
    return 0
if __name__=='__main__':
    try: raise SystemExit(main())
    except (OSError,ValueError,json.JSONDecodeError) as e:
        print('PHASE_V_SOURCE_REVIEW_ERROR='+str(e),file=sys.stderr);raise SystemExit(2)
