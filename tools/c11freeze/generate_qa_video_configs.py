#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="challenges")
    ap.add_argument("--output", default="artifacts/qa/video_matrix/configs")
    ap.add_argument("--challenge", action="append")
    ap.add_argument("--seed-label", default="QA")
    args = ap.parse_args()

    source = Path(args.source)
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    selected = set(args.challenge or [])

    count = 0
    for path in sorted(source.glob("CHALLENGE_*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        cid = str(data.get("challenge_id", path.stem))
        if selected and cid not in selected:
            continue
        seed = data.get("generation", {}).get("seed", "?")
        rng = data.get("generation", {}).get("rng_version", "?")
        fps = data.get("video", {}).get("fps", "?")
        game = data.get("video", {}).get("game_duration", "?")
        content = data.setdefault("content", {})
        content["hook"] = f"QA · {cid} · SEED {seed}"
        content["cta"] = f"{args.seed_label} · RNG {rng} · {fps} FPS · GAME {game}s"
        pres = data.setdefault("presentation", {})
        pres["qa_mode"] = True
        out = output / path.name
        out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        count += 1

    print(f"[C11FREEZE] QA configs generated: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
