from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from d_renderer_unified_content_review import (
    EXPECTED_HARNESSES,
    UnifiedContentReviewError,
    _root,
    build_review_manifest,
    canonical_json,
    sha256_bytes,
    sha256_json,
    validate_contract,
    validate_review_manifest,
)

ERROR_MARKERS = ("SCRIPT ERROR:", "ERROR:", "RENDERER VISUAL PAYLOAD MATERIALIZATION PREVIEW FAIL", "CHALLENGE RUNTIME OUTPUT PREVIEW FAIL", "PROFILE IDENTITY SEPARATION FAIL", "CHALLENGE DELIVERY TIMELINE REVIEW FAIL", "EDITORIAL FIELD WINDOW PROPOSAL FAIL")
SUMMARY_PREFIXES = {item["name"]: item["summary_prefix"] for item in EXPECTED_HARNESSES}


def _parse_summary(output: str, prefix: str, name: str) -> dict[str, Any]:
    found = [line[len(prefix):] for line in output.splitlines() if line.startswith(prefix)]
    if len(found) != 1:
        raise UnifiedContentReviewError(f"{name}: expected exactly one summary line {prefix!r}; found {len(found)}")
    try:
        value = json.loads(found[0])
    except json.JSONDecodeError as exc:
        raise UnifiedContentReviewError(f"{name}: summary line is not valid JSON") from exc
    if not isinstance(value, dict):
        raise UnifiedContentReviewError(f"{name}: summary JSON root is not an object")
    return value


def _run_harness(executable: str, root: Path, item: dict[str, str], timeout_seconds: int) -> tuple[dict[str, Any], dict[str, Any]]:
    script_rel = item["script"]
    script_path = root / script_rel
    if not script_path.is_file():
        raise UnifiedContentReviewError(f"Harness script missing: {script_rel}")
    command = [executable, "--headless", "--path", str(root), "--script", "res://" + script_rel.replace("\\", "/")]
    try:
        completed = subprocess.run(
            command,
            cwd=str(root),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_seconds,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise UnifiedContentReviewError(f"Could not execute {item['name']} harness: {exc}") from exc

    output = completed.stdout or ""
    print(f"\n--- C11-D unified review child: {item['name']} ---", flush=True)
    if output:
        print(output, end="" if output.endswith("\n") else "\n", flush=True)

    if completed.returncode != 0:
        raise UnifiedContentReviewError(f"{item['name']}: Godot exited with code {completed.returncode}")
    if item["pass_marker"] not in output:
        raise UnifiedContentReviewError(f"{item['name']}: PASS marker missing")
    bad_lines = [line for line in output.splitlines() if any(marker in line for marker in ERROR_MARKERS)]
    if bad_lines:
        raise UnifiedContentReviewError(f"{item['name']}: runtime error log present despite the PASS marker: {' | '.join(bad_lines[:3])}")
    summary = _parse_summary(output, item["summary_prefix"], item["name"])
    evidence = {
        "name": item["name"],
        "script": script_rel.replace("\\", "/"),
        "script_sha256": sha256_bytes(script_path.read_bytes()),
        "exit_code": int(completed.returncode),
        "summary_sha256": sha256_json(summary),
        "pass_marker_seen": True,
        "runtime_error_log_seen": False,
    }
    return summary, evidence


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the existing five C11-D in-memory content review harnesses and emit a console-only joined manifest.")
    parser.add_argument("--godot", default=os.environ.get("C11D_GODOT_EXECUTABLE") or shutil.which("godot") or "godot", help="Godot 4.7.1 console executable or command on PATH")
    parser.add_argument("--timeout", type=int, default=120, help="Per-harness timeout in seconds (default: 120)")
    args = parser.parse_args()
    if args.timeout < 1 or args.timeout > 900:
        print("C11-D RENDERER UNIFIED CONTENT REVIEW FAIL | timeout must be in 1..900 seconds", file=sys.stderr)
        return 2

    root = _root()
    contract_path = root / "definitions/c11d/production/D_RENDERER_UNIFIED_CONTENT_REVIEW_V1.json"
    try:
        contract, schema = validate_contract(root, verify_sources=True)
        summaries: dict[str, dict[str, Any]] = {}
        evidence: list[dict[str, Any]] = []
        for item in EXPECTED_HARNESSES:
            summary, record = _run_harness(args.godot, root, item, args.timeout)
            summaries[item["name"]] = summary
            evidence.append(record)
        report = build_review_manifest(summaries, evidence, contract, contract_path)
        validate_review_manifest(report, schema)
    except UnifiedContentReviewError as exc:
        print(f"\nC11-D RENDERER UNIFIED CONTENT REVIEW FAIL | {exc}", file=sys.stderr)
        return 1

    loops = next(x for x in report["content_items"] if x["content_type"] == "visual_loops")
    drills = next(x for x in report["content_items"] if x["content_type"] == "visual_drills")
    challenge = next(x for x in report["content_items"] if x["content_type"] == "challenges")
    print(
        "\nC11-D RENDERER UNIFIED CONTENT REVIEW PASS"
        f" | content_types={len(report['content_items'])}/3"
        f" | harnesses={len(report['harness_evidence'])}/5"
        " | cross_artifact=8/8"
        f" | loop={loops['timing']['frame_count']}@{loops['timing']['fps']}FPS"
        f" | drill={drills['timing']['frame_count']}@{drills['timing']['fps']}FPS"
        f" | challenge={challenge['timing']['source_total_frames']}@{challenge['timing']['source_fps']}_TO_{challenge['timing']['delivery_total_frames']}@{challenge['timing']['delivery_fps']}FPS"
        " | editorial_fields=2_VISIBLE_1_EMPTY_SUPPRESSED"
        f" | unresolved_gates={len(report['unresolved_gates'])}"
        " | review=CONSISTENT_NOT_VIDEO_READY"
        " | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE"
    )
    print("C11-D UNIFIED CONTENT REVIEW SUMMARY=" + json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
