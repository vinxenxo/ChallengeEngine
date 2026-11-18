#!/usr/bin/env python3
"""Read-only reconciliation of the E6 D9 route dependency pin ledger.

This tool verifies already accepted evidence and current source files. It does not
modify source files, execute media tools, reserve BatchId, or grant authorization.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

SCHEMA = "C11E-E6-D9-DEPENDENCY-PIN-RECONCILIATION-REPORT-V1"
EXPECTED = {
    "frozen_manifest": ("release/C11C_FREEZE_PACKAGE_MANIFEST.json", "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"),
    "d4_8_policy": ("definitions/c11d/production/C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V2.json", "0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07"),
    "dependency_pin_receipt": ("artifacts/tests/c11e/e6_runtime_dependency_pin_acceptance/E6DEPPINACCEPT_20261117T141326Z_C980FF81/E6_RUNTIME_DEPENDENCY_PIN_ACCEPTANCE_RECEIPT_V1.json", "41c62276465803dfb289a91b8a7f74c9b57c213dbad64c1323d6f626e3b2edd0"),
    "route_audit_receipt": ("artifacts/tests/c11e/e6_challenge_capture_route_audit/E6ROUTEAUDIT_20261117T125614Z_54A34DBA/E6_CHALLENGE_CAPTURE_ROUTE_AUDIT_RECEIPT_V1.json", "8deb1c23022ecde3f0b66e7ff07778172adecbd6e6a7f6ec045f6698657b4190"),
    "d9_plan_manifest": ("artifacts/tests/c11e/e6_d9_capture_orchestration_prepare_only/E6CAPPLAN_20261118T082416Z_68342FCD/E6_D9_CAPTURE_ORCHESTRATION_PREPARE_ONLY_MANIFEST_V1.json", "144470d16a222a1f01f0b7a9edec699af18d18bac614f7db938021e1acc0db2d"),
    "d9_plan_receipt": ("artifacts/tests/c11e/e6_d9_capture_orchestration_prepare_only/E6CAPPLAN_20261118T082416Z_68342FCD/E6_D9_CAPTURE_ORCHESTRATION_PREPARE_ONLY_RECEIPT_V1.json", "2233fcda43861d7c2bf1d933f1270b84976d315b6f2439bb46d1d2e237653b74"),
    "e6_smoke18_audit_receipt": ("artifacts/tests/c11e/e6_smoke18_audit/E6AUDITV2_20261116T235057Z_B7FA0492/E6_SMOKE18_READONLY_AUDIT_RECEIPT_V2.json", "054ed52aefe45cc4d986c4621adbbdb6ca7cf36dc1c4a12cbd76238de86e21fd"),
    "hydration_v2_report": ("artifacts/tests/c11e/e6_reuse_evidence_hydration_v2/E6HYDRATE_20261118T073344Z_1A9D7C52/E6HYDRATE_20261118T073344Z_1A9D7C52_REPORT_V2.json", "11f0eeba941f4740759132b3ba984eecf80c68a69aad27fe605a81a4ff8f5a77"),
}


SIDECARS = [
    ("artifacts/tests/c11e/e6_runtime_dependency_pin_acceptance/E6DEPPINACCEPT_20261117T141326Z_C980FF81/E6_RUNTIME_DEPENDENCY_PIN_ACCEPTANCE_RECEIPT_V1.json.sha256", "41c62276465803dfb289a91b8a7f74c9b57c213dbad64c1323d6f626e3b2edd0  E6_RUNTIME_DEPENDENCY_PIN_ACCEPTANCE_RECEIPT_V1.json"),
    ("artifacts/tests/c11e/e6_challenge_capture_route_audit/E6ROUTEAUDIT_20261117T125614Z_54A34DBA/E6_CHALLENGE_CAPTURE_ROUTE_AUDIT_RECEIPT_V1.json.sha256", "8deb1c23022ecde3f0b66e7ff07778172adecbd6e6a7f6ec045f6698657b4190  E6_CHALLENGE_CAPTURE_ROUTE_AUDIT_RECEIPT_V1.json"),
    ("artifacts/tests/c11e/e6_d9_capture_orchestration_prepare_only/E6CAPPLAN_20261118T082416Z_68342FCD/E6_D9_CAPTURE_ORCHESTRATION_PREPARE_ONLY_MANIFEST_V1.json.sha256", "144470d16a222a1f01f0b7a9edec699af18d18bac614f7db938021e1acc0db2d  E6_D9_CAPTURE_ORCHESTRATION_PREPARE_ONLY_MANIFEST_V1.json"),
    ("artifacts/tests/c11e/e6_d9_capture_orchestration_prepare_only/E6CAPPLAN_20261118T082416Z_68342FCD/E6_D9_CAPTURE_ORCHESTRATION_PREPARE_ONLY_RECEIPT_V1.json.sha256", "2233fcda43861d7c2bf1d933f1270b84976d315b6f2439bb46d1d2e237653b74  E6_D9_CAPTURE_ORCHESTRATION_PREPARE_ONLY_RECEIPT_V1.json"),
    ("artifacts/tests/c11e/e6_reuse_evidence_hydration_v2/E6HYDRATE_20261118T073344Z_1A9D7C52/E6HYDRATE_20261118T073344Z_1A9D7C52_REPORT_V2.json.sha256", "11f0eeba941f4740759132b3ba984eecf80c68a69aad27fe605a81a4ff8f5a77  E6HYDRATE_20261118T073344Z_1A9D7C52_REPORT_V2.json"),
]

CH004_HISTORICAL_DIVERGENCES = {
    "tools/c11d/d9/universal_editorial_model.py": {
        "historical_expected_sha256": "5c575be1942ba0613d66579d14db5cf9d7786e7062dfb001bd7be8a2e9c18ae5",
        "hydration_observed_sha256": "dac95fb698b52f96432a517d8ec3196a397e5e6bd3c025300350dd55ddce3afd",
        "disposition": "UNRESOLVED_HISTORICAL_E4A7_PIN_DIVERGENCE_NO_AUTO_WAIVER",
    },
    "c11c-suite/c11c-producer/c11e_production_service.py": {
        "historical_expected_sha256": "348997e575d985fe153a4f433f089c5f205be5d4d8f3853baf07be917a134951",
        "hydration_observed_sha256": "e5dbf9baa72d4c066ff8ba24006df954700d72a5b0f11f9f88aec653e84dce87",
        "disposition": "HISTORICAL_E4A7_PIN_SUPERSEDED_BY_LATER_ACCEPTED_33_PIN_BASELINE_BUT_REUSE_NOT_AUTO_ACCEPTED",
    },
}

CH004_OBSERVED_CURRENT_SHA256 = {
    "tools/c11d/d9/universal_editorial_model.py": "dac95fb698b52f96432a517d8ec3196a397e5e6bd3c025300350dd55ddce3afd",
    "c11c-suite/c11c-producer/c11e_production_service.py": "e5dbf9baa72d4c066ff8ba24006df954700d72a5b0f11f9f88aec653e84dce87",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_project_file(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative.strip():
        raise ValueError("EMPTY_RELATIVE_PATH")
    normalized = relative.replace("\\", "/")
    pure = PurePosixPath(normalized)
    if pure.is_absolute() or re.match(r"^[A-Za-z]:", normalized) or ".." in pure.parts:
        raise ValueError("UNSAFE_RELATIVE_PATH:" + relative)
    candidate = root.joinpath(*pure.parts)
    resolved_root = root.resolve()
    resolved = candidate.resolve(strict=False)
    try:
        resolved.relative_to(resolved_root)
    except ValueError as exc:
        raise ValueError("PATH_ESCAPES_PROJECT_ROOT:" + relative) from exc
    return candidate


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as f:
        value = json.load(f)
    if not isinstance(value, dict):
        raise ValueError("JSON_ROOT_NOT_OBJECT:" + str(path))
    return value


def validate_pin_rows(rows: Any) -> dict[str, str]:
    if not isinstance(rows, list) or len(rows) != 33:
        raise ValueError("EXPECTED_EXACTLY_33_SOURCE_PINS")
    pins: dict[str, str] = {}
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("SOURCE_PIN_ROW_NOT_OBJECT")
        rel = row.get("path")
        digest = row.get("sha256")
        if not isinstance(rel, str) or not isinstance(digest, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", digest):
            raise ValueError("INVALID_SOURCE_PIN_ROW")
        key = rel.replace("\\", "/")
        if key in pins:
            raise ValueError("DUPLICATE_SOURCE_PIN:" + key)
        PurePosixPath(key)
        pins[key] = digest.lower()
    return pins


def reconcile_route_dependencies(route_receipt: dict[str, Any], accepted_pins: dict[str, str]) -> dict[str, Any]:
    findings = route_receipt.get("findings")
    if not isinstance(findings, list):
        raise ValueError("ROUTE_AUDIT_FINDINGS_MISSING")
    finding = next((x for x in findings if isinstance(x, dict) and x.get("id") == "ADDITIONAL_RUNTIME_ROUTE_DEPENDENCY_FINGERPRINTS"), None)
    if finding is None:
        raise ValueError("ADDITIONAL_ROUTE_DEPENDENCY_FINDING_MISSING")
    rows = finding.get("rows")
    if not isinstance(rows, list) or len(rows) != 9:
        raise ValueError("EXPECTED_EXACTLY_9_ADDITIONAL_ROUTE_DEPENDENCIES")
    results = []
    for row in rows:
        rel = row.get("path")
        observed = str(row.get("observed_sha256", "")).lower()
        if not rel or not re.fullmatch(r"[0-9a-f]{64}", observed):
            raise ValueError("INVALID_ADDITIONAL_ROUTE_DEPENDENCY_ROW")
        accepted = accepted_pins.get(rel)
        results.append({"path": rel, "observed_sha256": observed, "accepted_pin_sha256": accepted,
                        "status": "ACCEPTED_MATCH" if accepted == observed else "NOT_COVERED_OR_HASH_MISMATCH"})
    matched = sum(1 for x in results if x["status"] == "ACCEPTED_MATCH")
    return {"expected": 9, "matched": matched, "status": "PASS_9_OF_9_ALREADY_ACCEPTED" if matched == 9 else "BLOCKED_ROUTE_DEPENDENCY_PIN_GAP", "rows": results}


def verify_fixed_file(root: Path, key: str) -> dict[str, Any]:
    rel, expected = EXPECTED[key]
    path = safe_project_file(root, rel)
    if not path.is_file():
        return {"id": key, "path": rel, "status": "MISSING", "expected_sha256": expected}
    actual = sha256_file(path)
    return {"id": key, "path": rel, "status": "PASS" if actual == expected else "HASH_MISMATCH",
            "expected_sha256": expected, "actual_sha256": actual, "bytes": path.stat().st_size}


def run_audit(project_root: Path) -> dict[str, Any]:
    root = project_root.resolve()
    if not root.is_dir():
        raise ValueError("PROJECT_ROOT_NOT_FOUND")
    fixed = [verify_fixed_file(root, key) for key in EXPECTED]
    for sidecar_rel, expected_text in SIDECARS:
        sidecar_path = safe_project_file(root, sidecar_rel)
        actual_text = sidecar_path.read_text(encoding="ascii").strip() if sidecar_path.is_file() else None
        fixed.append({"id": "sidecar", "path": sidecar_rel,
                      "status": "PASS" if actual_text == expected_text else ("MISSING" if actual_text is None else "SIDECAR_CONTENT_MISMATCH"),
                      "expected_content": expected_text, "actual_content": actual_text})
    fixed_pass = all(x["status"] == "PASS" for x in fixed)
    blockers: list[str] = []
    pin_rows: dict[str, str] = {}
    pin_checks: list[dict[str, Any]] = []
    route_reconciliation: dict[str, Any] = {"status": "NOT_RUN"}
    d9_checks: dict[str, Any] = {}
    hydration: dict[str, Any] = {}

    try:
        pin_receipt = load_json(safe_project_file(root, EXPECTED["dependency_pin_receipt"][0]))
        if pin_receipt.get("status") != "PASS_E6_STATIC_ROUTE_DEPENDENCY_PIN_BASELINE_ACCEPTED":
            raise ValueError("DEPENDENCY_PIN_RECEIPT_STATUS_NOT_ACCEPTED")
        pin_rows = validate_pin_rows(pin_receipt.get("source_pin_verification"))
        for rel, expected in pin_rows.items():
            path = safe_project_file(root, rel)
            if not path.is_file():
                pin_checks.append({"path": rel, "status": "MISSING", "expected_sha256": expected})
                continue
            actual = sha256_file(path)
            pin_checks.append({"path": rel, "status": "PASS" if actual == expected else "HASH_MISMATCH",
                               "expected_sha256": expected, "actual_sha256": actual})
        if len(pin_checks) != 33 or any(x["status"] != "PASS" for x in pin_checks):
            blockers.append("ACCEPTED_33_SOURCE_PINS_NOT_ALL_CURRENT")
    except Exception as exc:
        blockers.append("DEPENDENCY_PIN_RECEIPT_INVALID:" + str(exc))

    try:
        route = load_json(safe_project_file(root, EXPECTED["route_audit_receipt"][0]))
        if route.get("status") != "PASS_STATIC_ROUTE_AUDIT_EXECUTION_HELD":
            raise ValueError("ROUTE_AUDIT_STATUS_NOT_PASS")
        route_reconciliation = reconcile_route_dependencies(route, pin_rows)
        if route_reconciliation["matched"] != 9:
            blockers.append("NINE_ROUTE_DEPENDENCIES_NOT_FULLY_COVERED_BY_ACCEPTED_33_PIN_RECEIPT")
    except Exception as exc:
        blockers.append("ROUTE_DEPENDENCY_RECONCILIATION_FAILED:" + str(exc))

    try:
        d9_manifest = load_json(safe_project_file(root, EXPECTED["d9_plan_manifest"][0]))
        d9_receipt = load_json(safe_project_file(root, EXPECTED["d9_plan_receipt"][0]))
        if d9_receipt.get("status") != "PASS_D9_MULTISELECTOR_CAPTURE_GROUP_PLAN_READY_EXECUTION_HELD":
            raise ValueError("D9_PLAN_RECEIPT_STATUS_NOT_PASS")
        if d9_receipt.get("manifest_sha256") != EXPECTED["d9_plan_manifest"][1]:
            raise ValueError("D9_PLAN_MANIFEST_LINK_MISMATCH")
        if d9_receipt.get("selected_challenge_groups") != 6 or d9_receipt.get("linked_e1_intents") != 18 or d9_receipt.get("linked_d_envelopes") != 18:
            raise ValueError("D9_PLAN_CARDINALITY_MISMATCH")
        execution = d9_receipt.get("execution", {})
        forbidden = [k for k in ("processes_started", "godot_invoked", "ffmpeg_invoked", "ffprobe_invoked", "audio_generated", "mux_invoked", "media_created", "batch_id_consumed", "production_dispatch") if execution.get(k) is not False]
        if forbidden or execution.get("release_authority") != "NONE":
            raise ValueError("D9_PLAN_EXECUTION_BOUNDARY_VIOLATION:" + ",".join(forbidden))
        d9_blockers = d9_manifest.get("blockers", [])
        d9_checks = {
            "receipt_status": d9_receipt.get("status"),
            "selected_challenge_groups": d9_receipt.get("selected_challenge_groups"),
            "linked_e1_intents": d9_receipt.get("linked_e1_intents"),
            "linked_d_envelopes": d9_receipt.get("linked_d_envelopes"),
            "stale_nine_dependency_blocker_present": "NINE_ADDITIONAL_ROUTE_DEPENDENCIES_OBSERVED_BUT_NOT_ACCEPTED_SOURCE_PINS" in d9_blockers,
            "historical_ch004_blocker_present": "CH004_HISTORICAL_SOURCE_PIN_DIVERGENCE_REQUIRES_EXPLICIT_ADJUDICATION_OR_FRESH_CAPTURE" in d9_blockers,
        }
    except Exception as exc:
        blockers.append("D9_PLAN_EVIDENCE_INVALID:" + str(exc))

    try:
        hydration = load_json(safe_project_file(root, EXPECTED["hydration_v2_report"][0]))
        if hydration.get("status") != "BLOCKED_E6_REUSE_EVIDENCE_INCOMPLETE" or hydration.get("check_count") != 1803:
            raise ValueError("HYDRATION_V2_REPORT_STATUS_OR_COUNT_MISMATCH")
        if hydration.get("failure_categories") != {"historical_source_pin_divergence": 2, "other_failures": 0}:
            raise ValueError("HYDRATION_V2_FAILURE_CATEGORIES_CHANGED")
        failures = [x for x in hydration.get("checks", []) if x.get("status") == "HISTORICAL_SOURCE_PIN_DIVERGENCE"]
        if len(failures) != 2:
            raise ValueError("EXPECTED_TWO_CH004_HISTORICAL_DIVERGENCES")
        for item in failures:
            rel = item.get("path")
            if rel not in CH004_HISTORICAL_DIVERGENCES:
                raise ValueError("UNEXPECTED_CH004_HISTORICAL_DIVERGENCE_PATH:" + str(rel))
        hydration = {
            "run_id": hydration.get("run_id"), "status": hydration.get("status"),
            "check_count": hydration.get("check_count"), "passed_checks": hydration.get("passed_checks"),
            "failed_checks": hydration.get("failed_checks"), "failure_categories": hydration.get("failure_categories"),
            "historical_divergences": [{"path": x.get("path"), "expected_sha256": x.get("expected_sha256"),
                                         "actual_sha256": x.get("actual_sha256"), "json_pointer": x.get("json_pointer"),
                                         "disposition": x.get("disposition")} for x in failures],
        }
    except Exception as exc:
        blockers.append("HYDRATION_V2_EVIDENCE_INVALID:" + str(exc))

    historical_observation_checks = []
    for rel, expected_current in CH004_OBSERVED_CURRENT_SHA256.items():
        path = safe_project_file(root, rel)
        actual = sha256_file(path) if path.is_file() else None
        historical_observation_checks.append({"path": rel, "expected_observed_current_sha256": expected_current,
                                              "actual_sha256": actual,
                                              "status": "PASS" if actual == expected_current else "OBSERVED_CURRENT_SOURCE_CHANGED"})
    if any(x["status"] != "PASS" for x in historical_observation_checks):
        blockers.append("CH004_HISTORICAL_DIVERGENCE_SOURCE_CHANGED_SINCE_HYDRATION")

    if not fixed_pass:
        blockers.append("FIXED_EVIDENCE_OR_GOVERNANCE_HASH_MISMATCH")
    if len(pin_checks) == 33 and any(x["status"] != "PASS" for x in pin_checks):
        blockers.append("LIVE_SOURCE_PIN_DRIFT")

    return {
        "schema": SCHEMA, "schema_version": "1.0", "created_utc": datetime.now(timezone.utc).isoformat(),
        "project_root": str(root),
        "status": "PASS_DEPENDENCY_PIN_RECONCILIATION_EXECUTION_HELD" if not blockers else "BLOCKED_DEPENDENCY_PIN_RECONCILIATION",
        "counts": {"fixed_evidence_pins": f"{sum(x['status']=='PASS' for x in fixed)}/{len(fixed)}",
                   "accepted_source_pins": f"{sum(x['status']=='PASS' for x in pin_checks)}/{len(pin_checks)}",
                   "additional_route_dependencies": f"{route_reconciliation.get('matched',0)}/9",
                   "ch004_observed_current_hashes": f"{sum(x['status']=='PASS' for x in historical_observation_checks)}/{len(historical_observation_checks)}"},
        "fixed_evidence_checks": fixed,
        "accepted_33_source_pin_checks": pin_checks,
        "route_dependency_reconciliation": route_reconciliation,
        "d9_plan_reconciliation": d9_checks,
        "hydration_v2_reconciliation": hydration,
        "ch004_historical_divergence_observation_checks": historical_observation_checks,
        "ch004_historical_source_pin_disposition": CH004_HISTORICAL_DIVERGENCES,
        "governance": {"frozen_c11c_manifest_sha256": EXPECTED["frozen_manifest"][1],
                       "d4_8_policy_sha256": EXPECTED["d4_8_policy"][1],
                       "d4_8_overridden": False, "e6_test_only_authorization": "NOT_GRANTED_BY_THIS_AUDIT_GOVERNANCE_REVIEW_REQUIRED",
                       "renderer_enabled": False, "production_dispatch": False, "media_created": False,
                       "godot_invoked": False, "ffmpeg_invoked": False, "ffprobe_invoked": False,
                       "audio_generated": False, "mux_invoked": False, "batch_id_consumed": False,
                       "release_authority": "NONE"},
        "blockers": blockers,
        "disposition": "The nine route dependencies are superseded by the later accepted 33-pin receipt only when all 33 live hashes pass. This does not waive the two CH004 historical nested source-pin divergences, does not accept CH004 reuse, and does not authorize E6 media execution.",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--output-root", default="artifacts/tests/c11e/e6_d9_dependency_pin_reconciliation")
    args = parser.parse_args(argv)
    root = Path(args.project_root).resolve()
    try:
        report = run_audit(root)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        import uuid
        run_id = "E6D9PINREC_" + stamp + "_" + uuid.uuid4().hex[:8].upper()
        report["run_id"] = run_id
        output_root = safe_project_file(root, args.output_root)
        output_dir = output_root / run_id
        output_dir.mkdir(parents=True, exist_ok=False)
        report_path = output_dir / (run_id + "_REPORT_V1.json")
        data = (json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
        report_path.write_bytes(data)
        digest = hashlib.sha256(data).hexdigest()
        sidecar = report_path.with_suffix(report_path.suffix + ".sha256")
        sidecar.write_text(digest + "  " + report_path.name + "\n", encoding="ascii")
        print("E6_D9_PIN_RECONCILIATION_STATUS=" + report["status"])
        print("E6_D9_PIN_RECONCILIATION_FIXED_PINS=" + report["counts"]["fixed_evidence_pins"])
        print("E6_D9_PIN_RECONCILIATION_SOURCE_PINS=" + report["counts"]["accepted_source_pins"])
        print("E6_D9_PIN_RECONCILIATION_ROUTE_DEPENDENCIES=" + report["counts"]["additional_route_dependencies"])
        print("E6_D9_PIN_RECONCILIATION_CH004_OBSERVED_HASHES=" + report["counts"]["ch004_observed_current_hashes"])
        print("E6_D9_PIN_RECONCILIATION_FAILURES=" + str(len(report["blockers"])))
        print("E6_D9_PIN_RECONCILIATION_REPORT=" + str(report_path))
        print("E6_D9_PIN_RECONCILIATION_REPORT_SHA256=" + digest)
        print("SOURCE_FILES_MODIFIED=FALSE")
        print("MEDIA_INVOKED=FALSE; GODOT_INVOKED=FALSE; FFMPEG_INVOKED=FALSE; FFPROBE_INVOKED=FALSE")
        print("AUDIO_GENERATED=FALSE; MUX_INVOKED=FALSE; BATCH_ID_CONSUMED=FALSE; RELEASE_AUTHORITY=NONE")
        print("GIT_CHECKS=SKIPPED; COMMITS=OPERATOR_MANAGED; SOURCE_FILE_PINS=ENFORCED")
        return 0 if report["status"] == "PASS_DEPENDENCY_PIN_RECONCILIATION_EXECUTION_HELD" else 2
    except Exception as exc:
        print("E6_D9_PIN_RECONCILIATION_FATAL=" + type(exc).__name__ + ":" + str(exc), file=sys.stderr)
        return 3

if __name__ == "__main__":
    raise SystemExit(main())
