#!/usr/bin/env python3
"""Deterministic human-review prioritization for a Phase T discovery report.
This tool never decides authority and never modifies the input report.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, re, sys
from datetime import datetime, timezone
from pathlib import Path

HIGH_TERMS = (
    "authority", "authorized", "authorised", "approved by", "approval", "sign-off", "signoff",
    "signature", "signed by", "issuer", "release_authority", "baseline_approval", "policy_adoption",
    "adopted option", "decision_id", "decision id", "effective date", "approved_bindings",
)
MEDIUM_TERMS = (
    "governance", "binding", "renderer", "policy", "baseline", "freeze", "acceptance", "release",
    "adjudication", "validation gate", "promotion", "master_seed", "semantic", "decision",
)

def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

def safe_relative(path: str) -> bool:
    if not isinstance(path,str) or not path or path.startswith(('/', '\\')) or re.match(r'^[A-Za-z]:',path): return False
    parts=path.replace('\\','/').split('/')
    return all(p not in ('','.','..') for p in parts)

def classify_priority(candidate: dict) -> tuple[str,int,list[str]]:
    hay = (str(candidate.get('path',''))+' '+ ' '.join(str(m.get('snippet','')) for m in candidate.get('matches',[]) if isinstance(m,dict))).lower()
    high=sorted({t for t in HIGH_TERMS if t in hay})
    med=sorted({t for t in MEDIUM_TERMS if t in hay})
    if high: return 'HIGH_REVIEW_PRIORITY',100+len(high),high+med
    if med: return 'MEDIUM_REVIEW_PRIORITY',50+len(med),med
    return 'LOW_REVIEW_PRIORITY',0,[]

def triage_report(report: dict, report_sha256: str) -> dict:
    if report.get('phase')!='T': raise ValueError('INPUT_REPORT_PHASE_NOT_T')
    if report.get('status')!='CANDIDATE_INVENTORY_READY_FOR_HUMAN_REVIEW': raise ValueError('INPUT_REPORT_STATUS_INVALID')
    if report.get('no_global_absence_claim') is not True: raise ValueError('INPUT_GLOBAL_ABSENCE_SCOPE_INVALID')
    counts=report.get('counts')
    if not isinstance(counts,dict): raise ValueError('INPUT_COUNTS_MISSING')
    candidates=report.get('candidates')
    if not isinstance(candidates,list) or len(candidates)!=counts.get('candidate_files'): raise ValueError('INPUT_CANDIDATE_COUNT_MISMATCH')
    unsearched=report.get('unsearched_documents')
    if not isinstance(unsearched,list) or len(unsearched)!=counts.get('unsearched_documents'): raise ValueError('INPUT_UNSEARCHED_COUNT_MISMATCH')
    errors=report.get('scan_errors')
    if not isinstance(errors,list) or len(errors)!=counts.get('scan_errors'): raise ValueError('INPUT_SCAN_ERROR_COUNT_MISMATCH')
    g=report.get('governance',{})
    if g.get('renderer')!='OFF' or g.get('approved_bindings')!=0 or g.get('approved_custom_data_bindings')!=0 or g.get('approved_renderer_projection_bindings')!=0 or g.get('release_authority')!='NONE': raise ValueError('INPUT_GOVERNANCE_LOCK_MISMATCH')
    out=[]; seen=set()
    for c in candidates:
        if not isinstance(c,dict): raise ValueError('CANDIDATE_NOT_OBJECT')
        p=c.get('path'); h=c.get('sha256'); b=c.get('bytes'); matches=c.get('matches',[])
        if not safe_relative(p): raise ValueError('CANDIDATE_PATH_UNSAFE')
        if p in seen: raise ValueError('CANDIDATE_PATH_DUPLICATE')
        seen.add(p)
        if not isinstance(h,str) or not re.fullmatch(r'[0-9a-f]{64}',h): raise ValueError('CANDIDATE_SHA256_INVALID')
        if not isinstance(b,int) or isinstance(b,bool) or b<0: raise ValueError('CANDIDATE_BYTES_INVALID')
        if c.get('classification')!='UNREVIEWED_CANDIDATE_NOT_AUTHORITY': raise ValueError('CANDIDATE_CLASSIFICATION_INVALID')
        if not isinstance(matches,list): raise ValueError('CANDIDATE_MATCHES_INVALID')
        for m in matches:
            if not isinstance(m,dict) or not isinstance(m.get('line'),int) or m['line']<0 or not isinstance(m.get('snippet'),str): raise ValueError('CANDIDATE_MATCH_INVALID')
            if len(m['snippet'])>260: raise ValueError('CANDIDATE_SNIPPET_TOO_LONG')
        priority,score,signals=classify_priority(c)
        out.append({'path':p,'sha256':h,'bytes':b,'filename_match':bool(c.get('filename_match',False)),'matches':matches,'priority':priority,'priority_score':score,'priority_signals':signals,'review_status':'NOT_REVIEWED','authority_finding':'UNDETERMINED','human_review_checks':['inspect actual file bytes','confirm source SHA-256','issuer and role authority','exact decision IDs and scope','unambiguous adopted option/value','effective version/date','signature or immutable decision-record identity','source hashes, conditions and required gates']})
    out.sort(key=lambda x:(-x['priority_score'],x['path'].casefold()))
    u=[]; useen=set()
    for item in unsearched:
        if not isinstance(item,dict): raise ValueError('UNSEARCHED_ITEM_NOT_OBJECT')
        p=item.get('path')
        if not safe_relative(p): raise ValueError('UNSEARCHED_PATH_UNSAFE')
        if p in useen: raise ValueError('UNSEARCHED_PATH_DUPLICATE')
        useen.add(p)
        u.append({**item,'review_status':'NOT_INSPECTED','authority_finding':'UNDETERMINED'})
    u.sort(key=lambda x:x['path'].casefold())
    timings=report.get('timing_conflicts',[])
    if len(timings)!=2: raise ValueError('TIMING_CONFLICT_COUNT_MISMATCH')
    for t in timings:
        if t.get('declared_total_duration_seconds')!=11 or t.get('phase_duration_sum_seconds')!=12 or t.get('status')!='BLOCKER_NO_CORRECTION_INFERRED': raise ValueError('TIMING_CONFLICT_CHANGED')
    hc=sum(x['priority']=='HIGH_REVIEW_PRIORITY' for x in out); mc=sum(x['priority']=='MEDIUM_REVIEW_PRIORITY' for x in out); lc=sum(x['priority']=='LOW_REVIEW_PRIORITY' for x in out)
    return {'schema_version':'1.0.0','phase':'U','status':'CANDIDATE_TRIAGE_READY_FOR_HUMAN_REVIEW','created_utc':datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),'source_report_sha256':report_sha256,'source_scan_index_sha256':report.get('scan_index_sha256'),'scope':{'input_phase_t_report_only':True,'working_tree_rescanned':False,'git_history_searched':False,'external_files_searched':False,'binary_document_contents_searched':False,'priority_is_authority':False},'counts':{'candidates':len(out),'high_priority':hc,'medium_priority':mc,'low_priority':lc,'unsearched_documents':len(u),'scan_errors':len(errors)},'candidates':out,'unsearched_documents':u,'skipped_large_files':report.get('skipped_large_files',[]),'scan_errors':errors,'governance':{k:g.get(k) for k in ['renderer','approved_bindings','approved_custom_data_bindings','approved_renderer_projection_bindings','release_authority']},'timing_conflicts':timings,'no_global_absence_claim':True,'authority_adjudication':'NOT_PERFORMED','policy_adoption':'NONE','next_action':'HUMAN_REVIEW_CANDIDATES_AND_UNSEARCHED_DOCUMENTS'}

def render_markdown(result: dict) -> str:
    c=result['counts']; lines=['# C11-D Phase U — Human Candidate Triage','',f"- Status: `{result['status']}`",f"- Source report SHA-256: `{result['source_report_sha256']}`",f"- Source scan index SHA-256: `{result['source_scan_index_sha256']}`",'- Scope: triage of the recorded Phase T report only; no rescan, Git history or binary contents.','- Priority scores are heuristic ordering only. Keyword matches are not authority evidence.','', '## Counts','',f"- Candidates: {c['candidates']} (high {c['high_priority']}, medium {c['medium_priority']}, low {c['low_priority']})",f"- Unsearched documents: {c['unsearched_documents']}",f"- Scan errors inherited from Phase T: {c['scan_errors']}",'', '## High review priority','']
    for bucket in ('HIGH_REVIEW_PRIORITY','MEDIUM_REVIEW_PRIORITY','LOW_REVIEW_PRIORITY'):
        title={'HIGH_REVIEW_PRIORITY':'High review priority','MEDIUM_REVIEW_PRIORITY':'Medium review priority','LOW_REVIEW_PRIORITY':'Low review priority'}[bucket]
        if bucket!='HIGH_REVIEW_PRIORITY': lines += ['',f'## {title}','']
        items=[x for x in result['candidates'] if x['priority']==bucket]
        if not items: lines.append('- None.')
        for x in items:
            snippets='; '.join(f"line {m.get('line')}: {m.get('snippet','')}" for m in x['matches']) or 'No saved snippet.'
            lines.append(f"- `{x['path']}` — sha256 `{x['sha256']}`; score {x['priority_score']}; status `NOT_REVIEWED`; finding `UNDETERMINED`; signals `{', '.join(x['priority_signals']) or 'none'}`; matches: {snippets}")
    lines += ['', '## Unsearched documents — coverage gap','']
    if not result['unsearched_documents']: lines.append('- None listed in Phase T report.')
    for x in result['unsearched_documents']:
        lines.append(f"- `{x['path']}` — `NOT_INSPECTED`; reason: {x.get('reason',x.get('classification','not provided'))}")
    lines += ['', '## Governance locks','', '`renderer=OFF`; approved binding counters remain zero; `release_authority=NONE`. CHALLENGE_008/009 remain blocked at 11 seconds declared versus 12 seconds phase sum. No policy adoption. No global absence claim.', '']
    return '\n'.join(lines)

def main(argv=None) -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--input-json',required=True,type=Path)
    ap.add_argument('--output-json',required=True,type=Path)
    ap.add_argument('--output-md',required=True,type=Path)
    args=ap.parse_args(argv)
    raw=args.input_json.read_bytes(); report=json.loads(raw.decode('utf-8-sig'))
    source_sha=hashlib.sha256(raw).hexdigest(); result=triage_report(report,source_sha)
    args.output_json.parent.mkdir(parents=True,exist_ok=True); args.output_md.parent.mkdir(parents=True,exist_ok=True)
    args.output_json.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    args.output_md.write_text(render_markdown(result),encoding='utf-8')
    print('PHASE_U_AUTHORITY_CANDIDATE_TRIAGE=PASS_READ_ONLY_QUEUE_READY')
    print(f"PHASE_U_SOURCE_REPORT_SHA256={source_sha}")
    print(f"PHASE_U_TRIAGE_JSON={args.output_json.resolve()}")
    print(f"PHASE_U_TRIAGE_MD={args.output_md.resolve()}")
    print(f"PHASE_U_CANDIDATES={result['counts']['candidates']}")
    print(f"PHASE_U_PRIORITY_HIGH={result['counts']['high_priority']}")
    print(f"PHASE_U_PRIORITY_MEDIUM={result['counts']['medium_priority']}")
    print(f"PHASE_U_PRIORITY_LOW={result['counts']['low_priority']}")
    print(f"PHASE_U_UNSEARCHED_DOCUMENTS={result['counts']['unsearched_documents']}")
    print('AUTHORITY_ADJUDICATION=NOT_PERFORMED; POLICY_ADOPTION=NONE')
    print('RUNTIME_REEXECUTED=false; GODOT_INVOKED=false; RENDERER=OFF; RELEASE_AUTHORITY=NONE')
    return 0
if __name__=='__main__':
    try: raise SystemExit(main())
    except (OSError,ValueError,json.JSONDecodeError) as exc:
        print(f'PHASE_U_TRIAGE_ERROR={exc}',file=sys.stderr); raise SystemExit(2)
