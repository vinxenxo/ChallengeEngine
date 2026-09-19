#!/usr/bin/env python3
from __future__ import annotations
import argparse, copy, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument('--source',default='challenges'); ap.add_argument('--output',default='artifacts/qa/video_matrix/configs'); ap.add_argument('--seed-file',default='qa/seed_corpus/stress_v1.json'); ap.add_argument('--include-canonical',action='store_true'); ap.add_argument('--limit',type=int,default=3); args=ap.parse_args()
    corpus=json.loads((ROOT/args.seed_file).read_text(encoding='utf-8')); seeds=(corpus['canonical_c11a1'] if args.include_canonical else [])+corpus['stress_seeds'][:args.limit]
    out=ROOT/args.output; out.mkdir(parents=True,exist_ok=True); count=0
    for path in sorted((ROOT/args.source).glob('CHALLENGE_*.json')):
        base=json.loads(path.read_text(encoding='utf-8')); cid=str(base.get('challenge_id',path.stem)); gen=base.get('generation',{}); video=base.get('video',{}); rng=str(gen.get('rng_version','?')); fps=video.get('fps','?'); game=video.get('game_duration','?')
        for seed in seeds:
            d=copy.deepcopy(base); d.setdefault('generation',{})['seed']=seed; c=d.setdefault('content',{}); c['hook']=f'QA · {cid} · SEED {seed}'; c['cta']=f'TEST · RNG {rng} · {fps} FPS · GAME {game}s'; d.setdefault('presentation',{})['qa_mode']=True
            (out/f'{cid}_seed_{seed}.json').write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8'); count+=1
    print(f'[C11FREEZE] QA video matrix configs generated: {count}'); return 0
if __name__=='__main__': raise SystemExit(main())
