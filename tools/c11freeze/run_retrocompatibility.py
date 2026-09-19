#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
REF_DEFAULTS = [
    ROOT / "qa/c11a1_challenge_qa/C11A1_CHALLENGE_BULK_MANIFEST.json",
    ROOT / "artifacts/qa/c11a1_challenge_qa/C11A1_CHALLENGE_BULK_MANIFEST.json",
]
INT_FIELDS = {
    "initial_seed", "final_seed", "seed_used", "attempts", "winning_frame_game",
    "winning_frame", "total_frames", "hook_frames", "game_frames", "reveal_frames",
    "cta_frames", "close_calls",
}
FLOAT_FIELDS = {"minimum_distance", "score"}
BOOL_FIELDS = {"winning_frame_in_valid_window"}
STR_FIELDS = {"rng_version"}


def parse_telemetry(stdout: str) -> dict[str, Any]:
    lines = [line for line in stdout.splitlines() if line.startswith("[TELEMETRY_JSON]")]
    if not lines:
        raise RuntimeError("[TELEMETRY_JSON] marker missing")
    value = json.loads(lines[-1][len("[TELEMETRY_JSON]"):])
    if not isinstance(value, dict):
        raise RuntimeError("telemetry payload is not a JSON object")
    return value


def equal(field: str, ref: Any, cur: Any) -> bool:
    if field in INT_FIELDS:
        return int(ref) == int(cur)
    if field in FLOAT_FIELDS:
        return math.isclose(float(ref), float(cur), rel_tol=1e-10, abs_tol=1e-9)
    if field in BOOL_FIELDS:
        return bool(ref) == bool(cur)
    if field in STR_FIELDS:
        return str(ref) == str(cur)
    return ref == cur


def resolve_reference(cli: str) -> Path:
    if cli:
        path = Path(cli)
        if not path.is_absolute():
            path = ROOT / path
        return path
    for path in REF_DEFAULTS:
        if path.is_file():
            return path
    raise RuntimeError("C11-A.1 frozen reference manifest not found")


def resolve_run_dir(run_id: str) -> Path:
    for root in (ROOT / "qa/c11a1_challenge_qa/runs", ROOT / "artifacts/qa/c11a1_challenge_qa/runs"):
        path = root / run_id
        if path.is_dir():
            return path
    raise RuntimeError(f"C11-A.1 run directory not found: {run_id}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reference", default="")
    ap.add_argument("--output", default="artifacts/regression/runs/c11_freeze/RETROCOMPATIBILITY_REPORT.json")
    args = ap.parse_args()

    reference_path = resolve_reference(args.reference)
    reference = json.loads(reference_path.read_text(encoding="utf-8"))
    executions = reference.get("executions")
    if not isinstance(executions, list) or len(executions) != 54:
        raise RuntimeError("Frozen C11-A.1 reference must contain exactly 54 executions")

    rows: list[dict[str, Any]] = []
    for index, item in enumerate(executions, 1):
        run_id = str(item["run_id"])
        config = resolve_run_dir(run_id) / "challenge_definition.json"
        print(f"[C11FREEZE][RETRO {index}/54] {run_id}")
        proc = subprocess.run(
            ["godot", "--headless", "--path", str(ROOT), "--", f"--config={config.as_posix()}", "--validate-only"],
            cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
        )
        row: dict[str, Any] = {
            "run_id": run_id,
            "challenge_id": str(item["challenge_id"]),
            "config": str(config.relative_to(ROOT)).replace("\\", "/"),
            "exit_code": proc.returncode,
            "mismatches": [],
        }
        try:
            cur = parse_telemetry(proc.stdout)
            row["current_telemetry"] = cur
            for field in sorted(INT_FIELDS | FLOAT_FIELDS | BOOL_FIELDS | STR_FIELDS):
                if field not in item:
                    row["mismatches"].append({"field": field, "error": "reference field missing"})
                elif field not in cur:
                    row["mismatches"].append({"field": field, "error": "current field missing"})
                elif not equal(field, item[field], cur[field]):
                    row["mismatches"].append({"field": field, "reference": item[field], "current": cur[field]})
        except Exception as exc:
            row["mismatches"].append({"error": str(exc)})
        row["pass"] = proc.returncode == 0 and not row["mismatches"]
        rows.append(row)

    ab_results = []
    for cid in sorted({str(x["challenge_id"]) for x in executions}):
        pair = {str(ref["seed_label"]): row for ref, row in zip(executions, rows) if str(ref["challenge_id"]) == cid}
        a, b = pair.get("12345_A"), pair.get("12345_B")
        same = bool(a and b and a.get("current_telemetry") == b.get("current_telemetry"))
        ab_results.append({"challenge_id": cid, "pass": same})

    failures = [row for row in rows if not row["pass"]] + [x for x in ab_results if not x["pass"]]
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "schema_version": "1.0",
        "gate": "C11_FREEZE_RETROCOMPATIBILITY",
        "reference_manifest": str(reference_path.relative_to(ROOT)).replace("\\", "/"),
        "executions": len(rows),
        "passed": sum(1 for row in rows if row["pass"]),
        "failed": len(failures),
        "presentation_hashes_compared": False,
        "reason_presentation_hashes_ignored": "C11-B.0/B.0.2/B.1 intentionally changed presentation topology/framing",
        "ab_rerun": ab_results,
        "rows": rows,
        "status": "PASS" if not failures else "FAIL",
    }
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if failures:
        print(f"[C11FREEZE][RETRO] FAIL — report={output}")
        return 1
    print("[C11FREEZE][RETRO] PASS — 54/54 telemetry comparisons and A/B rerun checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
