#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _safe_seed(seed: object) -> str:
    return re.sub(r"[^A-Za-z0-9_-]+", "_", str(seed))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="challenges")
    ap.add_argument("--output", default="artifacts/qa/video_matrix/configs")
    ap.add_argument("--seed-file", default="qa/seed_corpus/stress_v1.json")
    ap.add_argument("--include-canonical", action="store_true")
    ap.add_argument("--limit", type=int, default=3)
    args = ap.parse_args()

    corpus = json.loads((ROOT / args.seed_file).read_text(encoding="utf-8"))
    if args.include_canonical:
        seeds = list(corpus["canonical_c11a1"])
    else:
        stress = list(corpus["stress_seeds"])
        limit = len(stress) if args.limit <= 0 else min(args.limit, len(stress))
        seeds = stress[:limit]

    source_dir = ROOT / args.source
    out = ROOT / args.output
    out.mkdir(parents=True, exist_ok=True)

    for stale in out.glob("CHALLENGE_*_seed_*.json"):
        stale.unlink()

    count = 0
    for path in sorted(source_dir.glob("CHALLENGE_*.json")):
        base = json.loads(path.read_text(encoding="utf-8"))
        base_id = str(base.get("challenge_id", path.stem))
        generation = base.get("generation") if isinstance(base.get("generation"), dict) else {}
        video = base.get("video") if isinstance(base.get("video"), dict) else {}
        rng = str(generation.get("rng_version", "?"))
        fps = video.get("fps", "?")
        game = video.get("game_duration", "?")

        for seed in seeds:
            seed_label = _safe_seed(seed)
            d = copy.deepcopy(base)
            # build_factory requires unique IDs per batch config. This is test-only provenance;
            # the underlying mechanic/version/RNG and simulation math remain unchanged.
            d["challenge_id"] = f"{base_id}_QA_{seed_label}"
            d.setdefault("generation", {})["seed"] = seed

            content = d.setdefault("content", {})
            if not isinstance(content, dict):
                content = {}
                d["content"] = content
            content["hook"] = f"QA - {base_id} - SEED {seed}"
            content["cta"] = f"TEST - RNG {rng} - {fps} FPS - GAME {game}s"

            presentation = d.setdefault("presentation", {})
            if not isinstance(presentation, dict):
                presentation = {}
                d["presentation"] = presentation
            presentation["qa_mode"] = True

            (out / f"{base_id}_seed_{seed_label}.json").write_text(
                json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
            )
            count += 1

    print(f"[C11FREEZE] QA video matrix configs generated: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
