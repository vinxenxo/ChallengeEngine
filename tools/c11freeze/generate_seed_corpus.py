#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import random

MAX_SEED = 2_147_483_646
CANONICAL = ["12345_A", "12345_B", "314159", "54321", "7770001", "998877"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=32)
    ap.add_argument("--corpus-seed", type=int, default=0xC11F2026)
    ap.add_argument("--output", default="qa/seed_corpus/stress_v1.json")
    args = ap.parse_args()
    if args.count <= 0:
        raise SystemExit("count must be > 0")

    rng = random.Random(args.corpus_seed)
    values: list[int] = []
    seen: set[int] = set()
    while len(values) < args.count:
        value = rng.randint(1, MAX_SEED)
        if value not in seen:
            seen.add(value)
            values.append(value)

    payload = {
        "schema_version": "1.0",
        "corpus_id": "c11_freeze_stress_v1",
        "generator_seed": args.corpus_seed,
        "count": len(values),
        "domain": [1, MAX_SEED],
        "canonical_c11a1": CANONICAL,
        "stress_seeds": values,
    }
    raw = json.dumps(payload, indent=2, ensure_ascii=False).encode("utf-8")
    payload["sha256"] = hashlib.sha256(raw).hexdigest()

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[C11FREEZE] seed corpus: {out}")
    print(f"[C11FREEZE] count={len(values)} generator_seed={args.corpus_seed} sha256={payload['sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
