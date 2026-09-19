#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import subprocess
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
FIELDS = {
    "initial_seed", "final_seed", "seed_used", "attempts", "rng_version",
    "winning_frame_game", "winning_frame", "total_frames", "hook_frames",
    "game_frames", "reveal_frames", "cta_frames", "minimum_distance",
    "score", "close_calls", "winning_frame_in_valid_window",
}
FLOATS = {"minimum_distance", "score"}
# Godot may surface a Windows native access violation as either signed or unsigned.
NATIVE_CRASH_CODES = {3221225477, -1073741819}  # 0xC0000005


def telemetry(stdout: str) -> dict[str, Any]:
    lines = [x for x in stdout.splitlines() if x.startswith("[TELEMETRY_JSON]")]
    if not lines:
        raise RuntimeError("[TELEMETRY_JSON] marker missing")
    obj = json.loads(lines[-1][len("[TELEMETRY_JSON]"):])
    if not isinstance(obj, dict):
        raise RuntimeError("telemetry payload is not object")
    return obj


def same(a: dict[str, Any], b: dict[str, Any]) -> bool:
    for field in FIELDS:
        if field not in a or field not in b:
            return False
        if field in FLOATS:
            if not math.isclose(float(a[field]), float(b[field]), rel_tol=1e-10, abs_tol=1e-9):
                return False
        elif a[field] != b[field]:
            return False
    return True


def run_once(config: Path) -> dict[str, Any]:
    proc = subprocess.run(
        [
            "godot", "--headless", "--path", str(ROOT), "--",
            f"--config={config.as_posix()}", "--validate-only",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    rec: dict[str, Any] = {"exit_code": proc.returncode}
    if proc.returncode == 0:
        try:
            rec["telemetry"] = telemetry(proc.stdout)
        except Exception as exc:
            rec["error"] = str(exc)
    else:
        rec["error"] = f"godot exit {proc.returncode}"
        if proc.returncode in NATIVE_CRASH_CODES:
            rec["native_crash"] = True
    return rec


def run_with_retries(config: Path, repeat: int, retries: int, retry_delay: float) -> list[dict[str, Any]]:
    executions: list[dict[str, Any]] = []
    for logical_repeat in range(1, repeat + 1):
        attempt = 0
        while True:
            attempt += 1
            rec = run_once(config)
            rec["repeat"] = logical_repeat
            rec["attempt"] = attempt
            executions.append(rec)

            if rec.get("exit_code") == 0 and "telemetry" in rec:
                break

            # Retry only process-level/runtime failures or a missing telemetry marker.
            # A deterministic telemetry mismatch is checked later and is never hidden.
            if attempt >= retries + 1:
                break
            time.sleep(retry_delay)
    return executions


def main() -> int:
    ap = argparse.ArgumentParser(description="Fixed-seed deterministic stress gate")
    ap.add_argument("--challenge-dir", default="challenges")
    ap.add_argument("--seed-file", default="tests/fixtures/seeds/stress_v1.json")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--repeat", type=int, default=2)
    ap.add_argument("--retries", type=int, default=3, help="extra attempts after process/runtime failure")
    ap.add_argument("--retry-delay", type=float, default=0.75)
    args = ap.parse_args()

    if args.repeat < 1:
        raise SystemExit("repeat must be >= 1")
    if args.retries < 0:
        raise SystemExit("retries must be >= 0")

    corpus = json.loads((ROOT / args.seed_file).read_text(encoding="utf-8"))
    seeds = list(corpus["stress_seeds"])
    if args.limit > 0:
        seeds = seeds[:args.limit]

    base_out = ROOT / "artifacts/qa/seed_stress"
    cfg_dir = base_out / "configs"
    cfg_dir.mkdir(parents=True, exist_ok=True)
    base_out.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, Any]] = []
    cases = 0

    for challenge_path in sorted((ROOT / args.challenge_dir).glob("CHALLENGE_*.json")):
        base = json.loads(challenge_path.read_text(encoding="utf-8"))
        challenge_id = str(base.get("challenge_id", challenge_path.stem))

        for seed in seeds:
            cases += 1
            definition = json.loads(json.dumps(base))
            definition.setdefault("generation", {})["seed"] = int(seed)
            config = cfg_dir / f"{challenge_id}_seed_{seed}.json"
            config.write_text(
                json.dumps(definition, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

            executions = run_with_retries(config, args.repeat, args.retries, args.retry_delay)
            successful = [x for x in executions if x.get("exit_code") == 0 and "telemetry" in x]

            ok = len(successful) >= args.repeat
            if ok:
                # Use the first successful execution for each logical repeat.
                by_repeat: dict[int, dict[str, Any]] = {}
                for rec in successful:
                    by_repeat.setdefault(int(rec["repeat"]), rec)
                ok = len(by_repeat) == args.repeat
                if ok:
                    reference = by_repeat[1]["telemetry"]
                    ok = all(same(reference, by_repeat[n]["telemetry"]) for n in range(2, args.repeat + 1))

            row = {
                "challenge_id": challenge_id,
                "seed": int(seed),
                "repeat": args.repeat,
                "retries": args.retries,
                "pass": ok,
                "executions": executions,
            }
            rows.append(row)

            if not ok:
                report = {
                    "schema_version": "1.1",
                    "status": "FAIL",
                    "corpus_id": corpus.get("corpus_id"),
                    "seed_corpus_sha256": corpus.get("sha256"),
                    "seeds": len(seeds),
                    "challenges": 9,
                    "repeat": args.repeat,
                    "retries": args.retries,
                    "cases": len(rows),
                    "expected_cases": 9 * len(seeds),
                    "rows": rows,
                }
                (base_out / "STRESS_REPORT.json").write_text(
                    json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8",
                )
                print(f"[C11FREEZE][STRESS] FAIL {challenge_id}/seed_{seed}")
                return 1

    report = {
        "schema_version": "1.1",
        "corpus_id": corpus.get("corpus_id"),
        "seed_corpus_sha256": corpus.get("sha256"),
        "seeds": len(seeds),
        "challenges": 9,
        "repeat": args.repeat,
        "retries": args.retries,
        "cases": cases,
        "executions": sum(len(x["executions"]) for x in rows),
        "logical_executions": cases * args.repeat,
        "status": "PASS",
        "rows": rows,
    }
    (base_out / "STRESS_REPORT.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        f"[C11FREEZE][STRESS] PASS cases={cases} logical_executions={cases * args.repeat} "
        f"process_executions={report['executions']} repeat={args.repeat} retries={args.retries}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
