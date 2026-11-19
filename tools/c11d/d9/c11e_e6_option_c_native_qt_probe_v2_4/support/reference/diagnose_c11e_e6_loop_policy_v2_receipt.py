#!/usr/bin/env python3
"""Read-only diagnostic for the 2026-11-19 Loop Policy V2 receipt and A.3 lineage.

It does not rerun the old audit/tests and never writes to project source. It writes
only a new diagnostic JSON and SHA-256 sidecar at the requested output path.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path, PurePosixPath
from typing import Any

EXPECTED_RECEIPT_SHA256 = "5afc42ca84480ba1d025d288f2653d009e85af053fff5b62133e067a17dfb4be"
EXPECTED_RECEIPT_SCHEMA = "C11E-E6-LOOP-POLICY-PIN-RECONCILIATION-RECEIPT-V2"
A3_BRIDGE_REL = "docs/current/e/C11E_E4C_A3_REVIEW_MANIFEST_LINEAGE_RECONCILIATION_20261110_V2.json"
A3_BRIDGE_SHA = "aec0e387f167f4b821b7d94f06a67f78f498be939fe3cda857d20ce550819cac"
A3_ARCHIVE_REL = "docs/history/c11e/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1_PRE_D98_LINEAGE_REFRESH_20261106.json"
A3_ARCHIVE_SHA = "2075da9c33c689861a68d3bd8fb19b7ed593c6e76010ab200880746aa6d1a470"
A3_CURRENT_REL = "definitions/c11d/production/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1.json"
A3_CURRENT_SHA = "5702092bc1c88e4b333dd30cc150f0d383cd2006121037b0198905c75a3af795"
A3_MODEL_REL = "definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json"
A3_MODEL_SHA = "dabb458fc2215156ddb5ebea7e8ebec811098886ce2858733ba9fb13f6075ccb"
A3_PROPOSAL_REL = "definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json"
A3_PROPOSAL_SHA = "609a4d183aac07c2cbe1abaf41444160fdd137217faffbead3aef618320d57dc"
DECISION_REL = "docs/current/e/C11E_E4B_OPERATOR_POLICY_DECISION_RECORD_20261106_V1.json"
DECISION_SHA = "49efd5494f351f09d7597c4699e9c12e361b36884b6bfadacd822e6ff1480e04"
EXPECTED_POINTER = "/source_lineage/6/sha256"


class DiagnosticError(Exception):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def safe_project_path(root: Path, relative: str) -> Path:
    posix = PurePosixPath(relative.replace("\\", "/"))
    if posix.is_absolute() or not posix.parts or any(part in ("", ".", "..") for part in posix.parts):
        raise DiagnosticError(f"UNSAFE_PROJECT_RELATIVE_PATH:{relative}")
    path = root.joinpath(*posix.parts).resolve(strict=True)
    resolved_root = root.resolve(strict=True)
    if path != resolved_root and resolved_root not in path.parents:
        raise DiagnosticError(f"PROJECT_PATH_ESCAPES_ROOT:{relative}")
    if not path.is_file():
        raise DiagnosticError(f"PROJECT_PATH_NOT_FILE:{relative}")
    return path


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise DiagnosticError(f"JSON_READ_FAILED:{path}:{type(exc).__name__}:{exc}") from exc


def file_identity(root: Path, relative: str, expected_sha: str) -> dict[str, Any]:
    path = safe_project_path(root, relative)
    actual = sha256_file(path)
    size = path.stat().st_size
    return {
        "path": relative,
        "bytes": size,
        "sha256": actual,
        "expected_sha256": expected_sha,
        "status": "PASS" if actual == expected_sha else "FAIL",
    }


def collect_leaf_differences(left: Any, right: Any, prefix: str = "") -> list[str]:
    """Return differing JSON pointer paths between two parsed JSON values."""
    diffs: list[str] = []
    if isinstance(left, dict) and isinstance(right, dict):
        keys = sorted(set(left) | set(right))
        for key in keys:
            child = f"{prefix}/{str(key).replace('~', '~0').replace('/', '~1')}"
            if key not in left or key not in right:
                diffs.append(child)
            else:
                diffs.extend(collect_leaf_differences(left[key], right[key], child))
    elif isinstance(left, list) and isinstance(right, list):
        if len(left) != len(right):
            diffs.append(prefix or "/")
        else:
            for index, (a, b) in enumerate(zip(left, right)):
                diffs.extend(collect_leaf_differences(a, b, f"{prefix}/{index}"))
    elif left != right:
        diffs.append(prefix or "/")
    return diffs


def inspect_report_contract(report: dict[str, Any]) -> dict[str, Any]:
    issues: list[str] = []
    checks = report.get("checks")
    if not isinstance(checks, list):
        checks = []
        issues.append("RECEIPT_CHECKS_NOT_ARRAY")
    statuses = [str(row.get("status")) for row in checks if isinstance(row, dict)]
    pass_count = sum(status == "PASS" for status in statuses)
    fail_count = sum(status == "FAIL" for status in statuses)
    other_statuses = [status for status in statuses if status not in ("PASS", "FAIL")]
    declared_count = report.get("check_count")
    declared_pass = report.get("passed_checks")
    declared_fail = report.get("failed_checks")
    if declared_count != len(checks):
        issues.append("RECEIPT_CHECK_COUNT_MISMATCH")
    if declared_pass != pass_count:
        issues.append("RECEIPT_PASSED_COUNT_MISMATCH")
    if declared_fail != fail_count:
        issues.append("RECEIPT_FAILED_COUNT_MISMATCH")
    if other_statuses:
        issues.append("UNCLASSIFIED_CHECK_STATUS:" + ",".join(sorted(set(other_statuses))))
    failures = report.get("failures")
    if not isinstance(failures, list):
        issues.append("RECEIPT_FAILURES_NOT_ARRAY")
        failures = []
    declared_status = report.get("status")
    expected_status = (
        "PASS_LOOP_POLICY_DECISIONS_RECONCILED_NOT_COMPOSITOR_ACCEPTANCE"
        if pass_count == len(checks) and fail_count == 0 and not other_statuses and not failures
        else "BLOCKED_LOOP_POLICY_RECONCILIATION"
    )
    if declared_status != expected_status:
        issues.append("RECEIPT_TOP_LEVEL_STATUS_CONTRADICTS_CHECKS")
    a3_rows = [row for row in checks if isinstance(row, dict) and row.get("id") == "a3_lineage_single_pointer_reconciliation"]
    if len(a3_rows) != 1:
        issues.append("A3_CHECK_ROW_MISSING_OR_DUPLICATE")
        a3_status = "MISSING_OR_DUPLICATE"
        a3_error = None
    else:
        a3_status = str(a3_rows[0].get("status"))
        a3_error = a3_rows[0].get("error")
        if a3_status != "PASS":
            issues.append("A3_CHECK_NOT_PASS:" + a3_status)
    return {
        "declared_status": declared_status,
        "expected_status_from_check_rows": expected_status,
        "declared_check_count": declared_count,
        "actual_check_count": len(checks),
        "declared_passed_checks": declared_pass,
        "actual_passed_checks": pass_count,
        "declared_failed_checks": declared_fail,
        "actual_failed_checks": fail_count,
        "unclassified_statuses": other_statuses,
        "failures": failures,
        "a3_row_status": a3_status,
        "a3_row_error": a3_error,
        "issues": issues,
        "status": "PASS" if not issues else "FAIL",
    }


def validate_a3_objects(bridge: dict[str, Any], historical: dict[str, Any], current: dict[str, Any]) -> dict[str, Any]:
    issues: list[str] = []
    if bridge.get("schema") != "C11E-E4C-A3-REVIEW-MANIFEST-LINEAGE-RECONCILIATION-V2":
        issues.append("A3_BRIDGE_SCHEMA_MISMATCH")
    if bridge.get("status") != "ATTESTED_SINGLE_SOURCE_LINEAGE_POINTER_REFRESH_NO_POLICY_CHANGE":
        issues.append("A3_BRIDGE_STATUS_MISMATCH")
    lineage = bridge.get("review_manifest_lineage")
    if not isinstance(lineage, dict):
        raise DiagnosticError("A3_REVIEW_MANIFEST_LINEAGE_MISSING")
    if lineage.get("path") != A3_CURRENT_REL or lineage.get("historical_archive_path") != A3_ARCHIVE_REL:
        issues.append("A3_REVIEW_MANIFEST_PATH_MISMATCH")
    if lineage.get("historical_sha256") != A3_ARCHIVE_SHA or lineage.get("current_sha256") != A3_CURRENT_SHA:
        issues.append("A3_REVIEW_MANIFEST_HASH_MISMATCH")
    if lineage.get("allowed_json_pointer_difference") != [EXPECTED_POINTER]:
        issues.append("A3_ALLOWED_POINTER_DIFFERENCE_MISMATCH")
    if lineage.get("new_pointer_value") != A3_MODEL_SHA:
        issues.append("A3_NEW_POINTER_VALUE_MISMATCH")
    if lineage.get("pointer_target_path") != A3_MODEL_REL:
        issues.append("A3_POINTER_TARGET_PATH_MISMATCH")
    transition = lineage.get("installed_transition")
    expected_transition = {
        "operation": "PINNED_REPLACE",
        "preimage_sha256": A3_ARCHIVE_SHA,
        "postimage_sha256": A3_CURRENT_SHA,
        "preimage_bytes": 8591,
        "postimage_bytes": 8591,
        "only_changed_json_pointer": EXPECTED_POINTER,
        "historical_bytes_preserved_as_add_only_archive": True,
    }
    if not isinstance(transition, dict):
        issues.append("A3_INSTALLED_TRANSITION_MISSING")
    else:
        for key, value in expected_transition.items():
            if transition.get(key) != value:
                issues.append("A3_TRANSITION_FIELD_MISMATCH:" + key)
    if lineage.get("historical_bytes") != 8591 or lineage.get("current_bytes") != 8591:
        issues.append("A3_LINEAGE_BYTE_COUNTS_MISMATCH")
    try:
        historical_pointer = historical["source_lineage"][6]["sha256"]
        current_pointer = current["source_lineage"][6]["sha256"]
    except Exception as exc:
        raise DiagnosticError(f"A3_POINTER_LOCATION_INVALID:{type(exc).__name__}:{exc}") from exc
    old_pointer = lineage.get("old_pointer_value")
    new_pointer = lineage.get("new_pointer_value")
    if historical_pointer != old_pointer:
        issues.append("A3_HISTORICAL_POINTER_VALUE_MISMATCH")
    if current_pointer != new_pointer:
        issues.append("A3_CURRENT_POINTER_VALUE_MISMATCH")
    expected_current = copy.deepcopy(historical)
    expected_current["source_lineage"][6]["sha256"] = new_pointer
    pointer_differences = collect_leaf_differences(historical, current)
    if pointer_differences != [EXPECTED_POINTER]:
        issues.append("A3_MANIFEST_DIFF_NOT_SINGLE_POINTER:" + json.dumps(pointer_differences))
    if current != expected_current:
        issues.append("A3_CURRENT_MANIFEST_NOT_EXACT_ATTESTED_POSTIMAGE")
    return {
        "status": "PASS" if not issues else "BLOCKED",
        "old_pointer_expected": A3_ARCHIVE_SHA,
        "old_pointer_actual": historical_pointer,
        "bridge_old_pointer_value": old_pointer,
        "new_pointer_expected": A3_MODEL_SHA,
        "new_pointer_actual": current_pointer,
        "bridge_new_pointer_value": new_pointer,
        "pointer_target_path": lineage.get("pointer_target_path"),
        "transition": transition,
        "actual_manifest_differences": pointer_differences,
        "issues": issues,
    }


def inspect_a3_active_checkout(root: Path) -> dict[str, Any]:
    identities = [
        file_identity(root, A3_BRIDGE_REL, A3_BRIDGE_SHA),
        file_identity(root, A3_ARCHIVE_REL, A3_ARCHIVE_SHA),
        file_identity(root, A3_CURRENT_REL, A3_CURRENT_SHA),
        file_identity(root, A3_MODEL_REL, A3_MODEL_SHA),
        file_identity(root, A3_PROPOSAL_REL, A3_PROPOSAL_SHA),
        file_identity(root, DECISION_REL, DECISION_SHA),
    ]
    identity_issues = [f"ACTIVE_PIN_MISMATCH:{row['path']}:{row['sha256']}" for row in identities if row["status"] != "PASS"]
    bridge = read_json(safe_project_path(root, A3_BRIDGE_REL))
    historical = read_json(safe_project_path(root, A3_ARCHIVE_REL))
    current = read_json(safe_project_path(root, A3_CURRENT_REL))
    values = validate_a3_objects(bridge, historical, current)
    issues = identity_issues + values["issues"]
    return {
        **values,
        "status": "PASS" if not issues else "BLOCKED",
        "identities": identities,
        "bridge_schema": bridge.get("schema"),
        "bridge_status": bridge.get("status"),
        "issues": issues,
    }


def diagnose(project_root: Path, receipt_path: Path, expected_receipt_sha: str) -> dict[str, Any]:
    root = project_root.resolve(strict=True)
    receipt = receipt_path.resolve(strict=True)
    report_sha = sha256_file(receipt)
    receipt_issues: list[str] = []
    if report_sha != expected_receipt_sha:
        receipt_issues.append("LOOP_V2_RECEIPT_SHA256_MISMATCH:" + report_sha)
    report = read_json(receipt)
    if report.get("schema") != EXPECTED_RECEIPT_SCHEMA:
        receipt_issues.append("LOOP_V2_RECEIPT_SCHEMA_MISMATCH")
    report_contract = inspect_report_contract(report)
    receipt_issues.extend(report_contract["issues"])
    a3 = inspect_a3_active_checkout(root)
    all_issues = receipt_issues + a3["issues"]
    return {
        "schema": "C11E-E6-SMOKE18-CONTINUATION-A3-RECEIPT-DIAGNOSTIC-V1",
        "status": "PASS_A3_LINEAGE_AND_RECEIPT_CONTRACT_RECONCILED" if not all_issues else "BLOCKED_A3_LINEAGE_OR_RECEIPT_CONTRACT",
        "source_receipt": str(receipt),
        "source_receipt_sha256": report_sha,
        "expected_source_receipt_sha256": expected_receipt_sha,
        "receipt_contract": report_contract,
        "active_a3_lineage": a3,
        "issues": all_issues,
        "governance": {
            "project_source_files_modified": False,
            "old_v2_receipt_modified": False,
            "old_v2_audit_tests_rerun": False,
            "godot_invoked": False,
            "ffmpeg_invoked": False,
            "ffprobe_invoked": False,
            "audio_generated": False,
            "mux_invoked": False,
            "renderer": "OFF",
            "d4_8": "BLOCKED",
            "e6_accepted": 0,
            "git_checks": "SKIPPED",
            "commits": "OPERATOR_MANAGED",
            "source_file_pins": "ENFORCED",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--expected-receipt-sha256", default=EXPECTED_RECEIPT_SHA256)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        result = diagnose(Path(args.project_root), Path(args.receipt), args.expected_receipt_sha256.lower())
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        payload = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        output.write_bytes(payload)
        sidecar = output.with_name(output.name + ".sha256")
        sidecar.write_text(sha256_bytes(payload) + "  " + output.name + "\n", encoding="ascii")
        print("LOOP_V2_RECEIPT_CONTRACT=" + result["receipt_contract"]["status"])
        print("A3_ACTIVE_LINEAGE=" + result["active_a3_lineage"]["status"])
        print("A3_ACTUAL_POINTER_DIFFS=" + json.dumps(result["active_a3_lineage"]["actual_manifest_differences"]))
        if result["issues"]:
            for issue in result["issues"]:
                print("DIAGNOSTIC_ISSUE=" + issue)
        print("CONTINUATION_DIAGNOSTIC_STATUS=" + result["status"])
        print("PROJECT_SOURCE_FILES_MODIFIED=FALSE; PRIOR_V2_RECEIPT_MODIFIED=FALSE; OLD_V2_TESTS_RERUN=FALSE")
        print("GODOT_INVOKED=FALSE; FFMPEG_INVOKED=FALSE; FFPROBE_INVOKED=FALSE; AUDIO_GENERATED=FALSE; MUX_INVOKED=FALSE")
        print("REPORT=" + str(output))
        print("REPORT_SHA256=" + sha256_file(output))
        return 0 if not result["issues"] else 2
    except Exception as exc:
        print(f"CONTINUATION_DIAGNOSTIC_FATAL={type(exc).__name__}:{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
