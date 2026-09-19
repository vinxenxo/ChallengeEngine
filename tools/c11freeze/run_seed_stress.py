#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, math, subprocess
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[2]
FIELDS={"initial_seed","final_seed","seed_used","attempts","rng_version","winning_frame_game","winning_frame","total_frames","hook_frames","game_frames","reveal_frames","cta_frames","minimum_distance","score","close_calls","winning_frame_in_valid_window"}
FLOATS={"minimum_distance","score"}

def telemetry(stdout:str)->dict[str,Any]:
    lines=[x for x in stdout.splitlines() if x.startswith('[TELEMETRY_JSON]')]
    if not lines: raise RuntimeError('[TELEMETRY_JSON] marker missing')
    obj=json.loads(lines[-1][len('[TELEMETRY_JSON]'):])
    if not isinstance(obj,dict): raise RuntimeError('telemetry payload is not object')
    return obj

def same(a,b):
    for f in FIELDS:
        if f not in a or f not in b: return False
        if f in FLOATS:
            if not math.isclose(float(a[f]),float(b[f]),rel_tol=1e-10,abs_tol=1e-9): return False
        elif a[f] != b[f]: return False
    return True

def main()->int:
    ap=argparse.ArgumentParser(description='Fixed-seed deterministic stress gate')
    ap.add_argument('--challenge-dir',default='challenges')
    ap.add_argument('--seed-file',default='qa/seed_corpus/stress_v1.json')
    ap.add_argument('--limit',type=int,default=0)
    ap.add_argument('--repeat',type=int,default=2)
    args=ap.parse_args()
    if args.repeat<1: raise SystemExit('repeat must be >= 1')
    corpus=json.loads((ROOT/args.seed_file).read_text(encoding='utf-8'))
    seeds=list(corpus['stress_seeds'])
    if args.limit>0: seeds=seeds[:args.limit]
    base_out=ROOT/'artifacts/qa/seed_stress'; cfg_dir=base_out/'configs'; run_dir=base_out/'runs'
    cfg_dir.mkdir(parents=True,exist_ok=True); run_dir.mkdir(parents=True,exist_ok=True)
    rows=[]; cases=0
    for ch in sorted((ROOT/args.challenge_dir).glob('CHALLENGE_*.json')):
        base=json.loads(ch.read_text(encoding='utf-8')); cid=str(base.get('challenge_id',ch.stem))
        for seed in seeds:
            cases+=1; d=json.loads(json.dumps(base)); d.setdefault('generation',{})['seed']=int(seed)
            cfg=cfg_dir/f'{cid}_seed_{seed}.json'; cfg.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
            reps=[]
            for n in range(args.repeat):
                p=subprocess.run(['godot','--headless','--path',str(ROOT),'--',f'--config={cfg.as_posix()}','--validate-only'],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
                rec={'repeat':n+1,'exit_code':p.returncode}
                if p.returncode==0:
                    try: rec['telemetry']=telemetry(p.stdout)
                    except Exception as exc: rec['error']=str(exc)
                else: rec['error']=f'godot exit {p.returncode}'
                reps.append(rec)
            ok=all(r.get('exit_code')==0 and 'telemetry' in r for r in reps)
            if ok: ok=all(same(reps[0]['telemetry'],r['telemetry']) for r in reps[1:])
            row={'challenge_id':cid,'seed':int(seed),'repeat':args.repeat,'pass':ok,'repeats':reps}
            rows.append(row)
            if not ok:
                (base_out/'STRESS_REPORT.json').write_text(json.dumps({'status':'FAIL','cases':len(rows),'expected_cases':9*len(seeds),'rows':rows},indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
                print(f'[C11FREEZE][STRESS] FAIL {cid}/seed_{seed}'); return 1
    report={'schema_version':'1.0','corpus_id':corpus.get('corpus_id'),'seed_corpus_sha256':corpus.get('sha256'),'seeds':len(seeds),'challenges':9,'repeat':args.repeat,'cases':cases,'executions':cases*args.repeat,'status':'PASS','rows':rows}
    (base_out/'STRESS_REPORT.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(f'[C11FREEZE][STRESS] PASS cases={cases} executions={cases*args.repeat} repeat={args.repeat}')
    return 0
if __name__=='__main__': raise SystemExit(main())
