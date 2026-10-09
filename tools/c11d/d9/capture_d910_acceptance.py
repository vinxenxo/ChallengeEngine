"""Automate D9.10 adapter acceptance evidence without screenshots or media.

Runs focused D9.10 backend/CLI/static-GUI contracts, Config integration and candidate preflight. Optional flags exercise the existing test/operator Qt GUI offscreen and/or include the aggregate Suite. No mode launches a renderer or media production.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

EXPECTED_C11C_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def clean_run_id(value: str) -> str:
    value = value.strip()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{2,79}", value):
        raise ValueError("run-id must be 3-80 simple filename characters")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default="D910_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    parser.add_argument("--output-root", default="artifacts/tests/c11d_d9/d910_adapter_acceptance")
    parser.add_argument("--include-aggregate", action="store_true", help="also run the full c11c-suite/self_test.py aggregate and bind its result into this report")
    parser.add_argument("--include-qt-gui-runtime", action="store_true", help="instantiate the existing Producer test GUI offscreen and exercise the D9.10 callback for Challenge, Loop and Drill; no screenshots or media")
    args = parser.parse_args()
    run_id = clean_run_id(args.run_id)
    root = Path(__file__).resolve().parents[3]
    output_base = (root / args.output_root).resolve()
    try:
        output_base.relative_to(root)
    except ValueError:
        parser.error("output-root must remain inside the repository")
    run_root = output_base / run_id
    if run_root.exists():
        parser.error(f"run output already exists; choose a new --run-id: {run_root}")
    run_root.mkdir(parents=True, exist_ok=False)

    manifest_path = root / "release" / "C11C_FREEZE_PACKAGE_MANIFEST.json"
    manifest_hash = sha256_bytes(manifest_path.read_bytes()) if manifest_path.is_file() else None
    commands = [
        ("d910_bridge_and_adapter", [sys.executable, "tools/c11d/d9/test_editorial_render_bridge.py"], 180),
        ("producer_gui_contract", [sys.executable, "c11c-suite/c11c-producer/test_producer_gui_contract.py"], 60),
        ("config_contract", [sys.executable, "c11c-suite/c11c-config/test_config_gui_contract.py"], 60),
        ("config_self_test", [sys.executable, "c11c-suite/c11c-config/self_test.py"], 90),
        ("candidate_preflight", [sys.executable, "tools/c11d/baseline_candidate/test_d_baseline_candidate.py"], 120),
    ]
    if args.include_qt_gui_runtime:
        commands.append(("qt_gui_runtime", [sys.executable, "tools/c11d/d9/test_d910_gui_runtime_acceptance.py", "--run-id", run_id], 240))
    if args.include_aggregate:
        commands.append(("aggregate_suite", [sys.executable, "-u", "c11c-suite/self_test.py"], 600))
    results: list[dict[str, Any]] = []
    started = datetime.now(timezone.utc).isoformat()
    for name, command, timeout in commands:
        t0 = time.monotonic()
        try:
            proc = subprocess.run(
                command,
                cwd=root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
                check=False,
            )
            stdout = proc.stdout
            stderr = proc.stderr
            rc = proc.returncode
            error = None
        except subprocess.TimeoutExpired as exc:
            stdout = exc.stdout.decode("utf-8", errors="replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
            stderr = exc.stderr.decode("utf-8", errors="replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
            rc = 124
            error = f"timeout after {timeout}s"
        duration = round(time.monotonic() - t0, 3)
        stdout_bytes = stdout.encode("utf-8")
        stderr_bytes = stderr.encode("utf-8")
        (run_root / f"{name}.stdout.log").write_bytes(stdout_bytes)
        (run_root / f"{name}.stderr.log").write_bytes(stderr_bytes)
        results.append({
            "name": name,
            "command": command,
            "exit_code": rc,
            "status": "PASS" if rc == 0 else "FAIL",
            "duration_seconds": duration,
            "stdout_sha256": sha256_bytes(stdout_bytes),
            "stderr_sha256": sha256_bytes(stderr_bytes),
            "stdout_log": f"{name}.stdout.log",
            "stderr_log": f"{name}.stderr.log",
            "error": error,
        })

    all_pass = all(item["exit_code"] == 0 for item in results)
    report: dict[str, Any] = {
        "schema": "C11-D-D9.10-AUTOMATED-ACCEPTANCE-REPORT-V1",
        "schema_version": "1.0",
        "run_id": run_id,
        "started_at_utc": started,
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if all_pass and manifest_hash == EXPECTED_C11C_MANIFEST_SHA256 else "FAIL",
        "scope": "Five focused backend/CLI/static-GUI/Config/candidate checks; optional offscreen Qt runtime exercise via --include-qt-gui-runtime and aggregate Suite via --include-aggregate; no screenshots or media",
        "operator_gui_runtime_observed": False,
        "qt_gui_runtime_exercised": any(item["name"] == "qt_gui_runtime" and item["exit_code"] == 0 for item in results),
        "operator_screenshots_required_for_this_report": False,
        "gui_runtime_limit": "The optional Qt mode instantiates the existing Producer test GUI offscreen and clicks its D9.10 plan action. It does not claim a human visually observed the window and does not test the definitive GUI.",
        "checks": results,
        "governance": {
            "c11c_frozen_manifest_sha256": manifest_hash,
            "c11c_frozen_manifest_expected_sha256": EXPECTED_C11C_MANIFEST_SHA256,
            "c11c_frozen_manifest_match": manifest_hash == EXPECTED_C11C_MANIFEST_SHA256,
            "d_only_adapter_prepare_enabled": True,
            "aggregate_suite_included": args.include_aggregate,
            "qt_gui_runtime_included": args.include_qt_gui_runtime,
            "qt_gui_runtime_exercised": any(item["name"] == "qt_gui_runtime" and item["exit_code"] == 0 for item in results),
            "focused_check_count": sum(1 for item in results if item["name"] != "aggregate_suite"),
            "screenshot_collection_required": False,
            "renderer_dispatch_invoked": False,
            "renderer_input_emitted": False,
            "renderer_activation": False,
            "production_execution": False,
            "media_output_created": False,
            "d4_8": "BLOCKED",
            "release_authority": "NONE",
        },
        "outputs": {
            "relative_run_root": run_root.relative_to(root).as_posix(),
            "report_file": "D9_10_AUTOMATED_ACCEPTANCE_REPORT.json",
            "media_created": False,
        },
    }
    report["report_hash"] = hashlib.sha256(canonical_json(report).encode("utf-8")).hexdigest()
    (run_root / "D9_10_AUTOMATED_ACCEPTANCE_REPORT.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        "C11-D D9.10 AUTOMATED ACCEPTANCE " + report["status"]
        + f" | checks={sum(x['exit_code'] == 0 for x in results)}/{len(results)}"
        + f" | C11-C_manifest_match={str(report['governance']['c11c_frozen_manifest_match']).lower()}"
        + f" | GUI_runtime_observed=false | qt_gui_runtime={'PASS' if any(item['name'] == 'qt_gui_runtime' and item['exit_code'] == 0 for item in results) else ('NOT_REQUESTED' if not args.include_qt_gui_runtime else 'FAIL')} | renderer=OFF | media_created=false | release_authority=NONE"
        + f" | report={run_root.relative_to(root).as_posix()}/D9_10_AUTOMATED_ACCEPTANCE_REPORT.json"
    )
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
