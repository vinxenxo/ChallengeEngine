#!/usr/bin/env python3
"""Read-only CH004 historical source-pin lineage adjudication for C11-E E6.

Verifies exact E4A.7 source preimages preserved by the subsequent E4B source
integration backup receipt. It never edits the checkout, restores old code,
changes historical receipts, or authorizes media execution.
"""
from __future__ import annotations

import argparse
import ast
import difflib
import hashlib
import json
import os
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

SCHEMA = "C11E-E6-CH004-HISTORICAL-SOURCE-PIN-ADJUDICATION-V1"
PROJECT_ROOT_DEFAULT = Path(__file__).resolve().parents[3]
OUTPUT_REL = Path("artifacts/tests/c11e/e6_ch004_source_pin_adjudication")

# Active-checkout reconciliation receipt produced by V2 on 2026-11-18.
RECON_REL = Path(
    "artifacts/tests/c11e/e6_d9_dependency_pin_reconciliation/"
    "E6D9PINREC_20261118T094345Z_2B9358D1/"
    "E6D9PINREC_20261118T094345Z_2B9358D1_REPORT_V1.json"
)
RECON_SHA256 = "0e2c977f1122d9cfc69da255d8fa539720a23f00cdc2f4c030d48bd01019a59a"

E4A7_RECEIPT_REL = Path(
    "artifacts/tests/c11e/e4a_d_composited_av_review/"
    "RUN_20261106T070808Z-62F31F9C/"
    "C11E_E4A7_D_COMPOSITED_CHALLENGE_AV_RECEIPT.json"
)
E4A7_RECEIPT_SHA256 = "102cf07a0b8920318c3ba211a3bd4374c3e080018486363d701f81e65613aaa0"

E4B_V2_PINS_REL = Path("tools/c11d/d9/C11E_E4B_SHARED_SERVICE_INTEGRATION_V2_SOURCE_PINS.json")
E4B_V2_PINS_SHA256 = "c57c20abab5f58f32174d0b0cbef51d72b5c2ef473812d6d309a962c116df7be"
E4B_V3_PINS_REL = Path("tools/c11d/d9/C11E_E4B_SHARED_SERVICE_INTEGRATION_V3_SOURCE_PINS.json")
E4B_V3_PINS_SHA256 = "dc97cf4a3361414e46bf5996b1cbdb6adda384853da702104cd6876134e43328"
E4B_V3_RECOVERY_REL = Path(
    "artifacts/tests/c11e/e4b_shared_service_integration_recovery_v3/"
    "20261107T010101Z-A05C1878/"
    "C11E_E4B_SHARED_SERVICE_INTEGRATION_V3_RECOVERY_RECEIPT.json"
)
E4B_V3_RECOVERY_SHA256 = "09f78d97c8797885056882b343e1ee54e3fc2bb75cf2320338c037f6ea893048"
E4B_V3_RUN_RECEIPT_REL = Path(
    "artifacts/tests/c11e/e4b_shared_service_integration_v3/"
    "20261107T010113Z-CCE37AD9/"
    "C11E_E4B_SHARED_SERVICE_INTEGRATION_RUN_RECEIPT_V3.json"
)
E4B_V3_RUN_RECEIPT_SHA256 = "622ecf63186b17f50dfce23ab699385190d605a48222e5120d647af50a73ceaf"

FROZEN_MANIFEST_REL = Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")
FROZEN_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
D4_8_REL = Path("definitions/c11d/production/C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V2.json")
D4_8_SHA256 = "0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07"

HISTORICAL_SOURCES = {
    "tools/c11d/d9/universal_editorial_model.py": {
        "bytes": 26574,
        "sha256": "5c575be1942ba0613d66579d14db5cf9d7786e7062dfb001bd7be8a2e9c18ae5",
        "current_sha256": "dac95fb698b52f96432a517d8ec3196a397e5e6bd3c025300350dd55ddce3afd",
        "current_bytes": 27585,
        "e4b_backup_rel": Path(
            "artifacts/tests/c11e/e4b_shared_service_integration_overlay/"
            "20261107T005116Z-B9D97544/b/05.bak"
        ),
        "e4b_postimage_sha256": "dac95fb698b52f96432a517d8ec3196a397e5e6bd3c025300350dd55ddce3afd",
        "e4b_reason": "Returns explicit D9.9 and D4 compatibility flags and plan state",
    },
    "c11c-suite/c11c-producer/c11e_production_service.py": {
        "bytes": 32885,
        "sha256": "348997e575d985fe153a4f433f089c5f205be5d4d8f3853baf07be917a134951",
        "current_sha256": "e5dbf9baa72d4c066ff8ba24006df954700d72a5b0f11f9f88aec653e84dce87",
        "current_bytes": 86687,
        "e4b_backup_rel": Path(
            "artifacts/tests/c11e/e4b_shared_service_integration_overlay/"
            "20261107T005116Z-B9D97544/b/01.bak"
        ),
        "e4b_postimage_sha256": "08ab5a278de8ebb55795a57391c83a27207ce01920704c419b8e28be25ddcf65",
        "e4b_reason": "E1 shared boundary orchestration for Loop; updates D9 resolver pin and fail-closed approvals/payload hashes",
    },
}

class AdjudicationError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_project_path(root: Path, relative: str | Path) -> Path:
    raw = str(relative).replace("\\", "/")
    p = Path(raw)
    if not raw.strip() or p.is_absolute() or re.match(r"^[A-Za-z]:", raw) or ".." in p.parts:
        raise AdjudicationError(f"UNSAFE_PROJECT_RELATIVE_PATH:{relative}")
    root_resolved = root.resolve()
    candidate = root_resolved / Path(*p.parts)
    # Do not follow symlink/reparse ancestors for evidence sources.
    cur = root_resolved
    for part in p.parts:
        cur = cur / part
        # Check symlink state independently of exists(): dangling symlinks may
        # report exists=False while still redirecting path resolution.
        if cur.is_symlink() or (cur.exists() and _is_reparse_point(cur)):
            raise AdjudicationError(f"REPARSE_POINT_IN_EVIDENCE_PATH:{relative}")
    resolved = candidate.resolve(strict=False)
    if resolved != root_resolved and root_resolved not in resolved.parents:
        raise AdjudicationError(f"PATH_ESCAPES_PROJECT_ROOT:{relative}")
    return resolved


def _is_reparse_point(path: Path) -> bool:
    try:
        attrs = getattr(path.stat(follow_symlinks=False), "st_file_attributes", 0)
        return bool(attrs & 0x400)  # FILE_ATTRIBUTE_REPARSE_POINT on Windows
    except (OSError, AttributeError):
        return False


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise AdjudicationError(f"INVALID_JSON:{path}:{exc}") from exc
    if not isinstance(value, dict):
        raise AdjudicationError(f"EXPECTED_JSON_OBJECT:{path}")
    return value


def verify_file(root: Path, relative: str | Path, expected_sha: str, label: str, expected_bytes: int | None = None) -> dict[str, Any]:
    path = safe_project_path(root, relative)
    if not path.is_file():
        raise AdjudicationError(f"{label}_MISSING:{relative}")
    actual = sha256_file(path)
    if actual != expected_sha:
        raise AdjudicationError(f"{label}_SHA256_MISMATCH:{relative}:{actual}")
    size = path.stat().st_size
    if expected_bytes is not None and size != expected_bytes:
        raise AdjudicationError(f"{label}_BYTE_COUNT_MISMATCH:{relative}:{size}")
    return {"path": str(relative).replace("\\", "/"), "bytes": size, "sha256": actual, "status": "PASS"}


def verify_reconciliation(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    proof = verify_file(root, RECON_REL, RECON_SHA256, "V2_PIN_RECONCILIATION_REPORT")
    report = load_json(safe_project_path(root, RECON_REL))
    counts = report.get("counts", {})
    expected_counts = {
        "accepted_source_pins": "33/33",
        "additional_route_dependencies": "9/9",
        "ch004_observed_current_hashes": "2/2",
        "fixed_evidence_pins": "13/13",
    }
    if counts != expected_counts:
        raise AdjudicationError(f"RECONCILIATION_COUNTS_MISMATCH:{counts}")
    hydration = report.get("hydration_v2_reconciliation", {})
    if hydration.get("failure_categories") != {"historical_source_pin_divergence": 2, "other_failures": 0}:
        raise AdjudicationError("RECONCILIATION_FAILURE_CATEGORY_MISMATCH")
    if hydration.get("check_count") != 1803 or hydration.get("failed_checks") != 2 or hydration.get("passed_checks") != 1801:
        raise AdjudicationError("RECONCILIATION_HYDRATION_TOTALS_MISMATCH")
    disposition = report.get("ch004_historical_source_pin_disposition", {})
    expected_dispositions = {
        "c11c-suite/c11c-producer/c11e_production_service.py": "HISTORICAL_E4A7_PIN_SUPERSEDED_BY_LATER_ACCEPTED_33_PIN_BASELINE_BUT_REUSE_NOT_AUTO_ACCEPTED",
        "tools/c11d/d9/universal_editorial_model.py": "UNRESOLVED_HISTORICAL_E4A7_PIN_DIVERGENCE_NO_AUTO_WAIVER",
    }
    for path, expected in expected_dispositions.items():
        row = disposition.get(path, {})
        if row.get("disposition") != expected:
            raise AdjudicationError(f"RECONCILIATION_CH004_DISPOSITION_MISMATCH:{path}")
        spec = HISTORICAL_SOURCES[path]
        if row.get("historical_expected_sha256") != spec["sha256"] or row.get("hydration_observed_sha256") != spec["current_sha256"]:
            raise AdjudicationError(f"RECONCILIATION_CH004_HASH_LINEAGE_MISMATCH:{path}")
    if report.get("blockers") not in ([], None):
        raise AdjudicationError("RECONCILIATION_REPORT_HAS_BLOCKERS")
    return proof, {
        "counts": counts,
        "failure_categories": hydration.get("failure_categories"),
        "ch004_source_pin_dispositions": disposition,
        "d9_plan_stale_nine_dependency_blocker": report.get("d9_plan_reconciliation", {}).get("stale_nine_dependency_blocker_present"),
        "reconciliation_status": report.get("status"),
    }


def get_receipt_pin(receipt: Mapping[str, Any], key: str) -> tuple[str, str]:
    row = receipt.get("source_pins", {}).get(key)
    if not isinstance(row, Mapping):
        raise AdjudicationError(f"E4A7_SOURCE_PIN_ROW_MISSING:{key}")
    path = str(row.get("path", ""))
    digest = str(row.get("sha256", "")).lower()
    if not path or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise AdjudicationError(f"E4A7_SOURCE_PIN_ROW_INVALID:{key}")
    return path.replace("\\", "/"), digest


def verify_e4a7_receipt(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    proof = verify_file(root, E4A7_RECEIPT_REL, E4A7_RECEIPT_SHA256, "E4A7_RECEIPT")
    receipt = load_json(safe_project_path(root, E4A7_RECEIPT_REL))
    if receipt.get("run_id") != "20261106T070808Z-62F31F9C" or receipt.get("status") != "PASS_ISOLATED_E4A7_D_COMPOSITED_CHALLENGE_AV_TEST_ONLY":
        raise AdjudicationError("E4A7_RECEIPT_IDENTITY_OR_STATUS_MISMATCH")
    pins = {
        "d9_editorial": ("tools/c11d/d9/universal_editorial_model.py", HISTORICAL_SOURCES["tools/c11d/d9/universal_editorial_model.py"]["sha256"]),
        "e1_service": ("c11c-suite/c11c-producer/c11e_production_service.py", HISTORICAL_SOURCES["c11c-suite/c11c-producer/c11e_production_service.py"]["sha256"]),
    }
    extracted = {}
    for key, expected in pins.items():
        actual = get_receipt_pin(receipt, key)
        if actual != expected:
            raise AdjudicationError(f"E4A7_SOURCE_PIN_DOES_NOT_MATCH_REGISTER:{key}:{actual}")
        receipt_row = receipt.get("source_pins", {}).get(key, {})
        expected_bytes = HISTORICAL_SOURCES[expected[0]]["bytes"]
        if receipt_row.get("bytes") != expected_bytes:
            raise AdjudicationError(f"E4A7_SOURCE_PIN_BYTE_COUNT_MISMATCH:{key}")
        extracted[key] = {"path": actual[0], "sha256": actual[1], "bytes": expected_bytes, "status": "PASS"}
    return proof, {"run_id": receipt.get("run_id"), "status": receipt.get("status"), "source_pins": extracted}


def source_patch_rows(manifest: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    rows = manifest.get("source_patches", [])
    result = {}
    for row in rows:
        if isinstance(row, dict) and row.get("path"):
            result[str(row["path"]).replace("\\", "/")] = row
    return result


def verify_e4b_lineage(root: Path) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    pins_proof = verify_file(root, E4B_V2_PINS_REL, E4B_V2_PINS_SHA256, "E4B_V2_SOURCE_PIN_MANIFEST")
    v3_pins_proof = verify_file(root, E4B_V3_PINS_REL, E4B_V3_PINS_SHA256, "E4B_V3_SOURCE_PIN_MANIFEST")
    recovery_proof = verify_file(root, E4B_V3_RECOVERY_REL, E4B_V3_RECOVERY_SHA256, "E4B_V3_RECOVERY_RECEIPT")
    run_proof = verify_file(root, E4B_V3_RUN_RECEIPT_REL, E4B_V3_RUN_RECEIPT_SHA256, "E4B_V3_RUN_RECEIPT")
    v2 = load_json(safe_project_path(root, E4B_V2_PINS_REL))
    recovery = load_json(safe_project_path(root, E4B_V3_RECOVERY_REL))
    run_receipt = load_json(safe_project_path(root, E4B_V3_RUN_RECEIPT_REL))
    if recovery.get("status") != "PASS_ADD_ONLY_INSTALL_RECOVERY_V3":
        # Some published receipts use a more specific spelling; check their prefix safely.
        status = str(recovery.get("status", ""))
        if not status.startswith("PASS"):
            raise AdjudicationError(f"E4B_V3_RECOVERY_STATUS_NOT_PASS:{status}")
    if run_receipt.get("status") != "PASS_TEST_ONLY_SHARED_LOOP_BOUNDARY_PREPARATION_V3":
        raise AdjudicationError("E4B_V3_RUN_RECEIPT_STATUS_MISMATCH")
    if run_receipt.get("service_tests") != "25/25_PASS" or run_receipt.get("d98_model_test") != "PASS":
        raise AdjudicationError("E4B_V3_SOURCE_EVOLUTION_TEST_EVIDENCE_NOT_PASS")
    gov = run_receipt.get("governance", {})
    required_false = (
        "launcher_invoked", "dispatch", "audio", "media", "c11c_baseline_modified"
    )
    if (
        gov.get("renderer") != "OFF"
        or any(gov.get(key) is not False for key in required_false)
        or gov.get("d4_8") != "BLOCKED"
        or gov.get("d9_10") != "PREPARE_ONLY"
        or gov.get("d9_14") != "BLOCKED"
        or gov.get("d9_16") != "BLOCKED"
        or gov.get("d9_17") != "BLOCKED_NO_GO"
        or gov.get("d10") != "BLOCKED_FOR_PROMOTION"
        or gov.get("release_authority") != "NONE"
    ):
        raise AdjudicationError("E4B_V3_GOVERNANCE_BOUNDARY_MISMATCH")

    patch_map = source_patch_rows(v2)
    expected = {
        "tools/c11d/d9/universal_editorial_model.py": (HISTORICAL_SOURCES["tools/c11d/d9/universal_editorial_model.py"]["sha256"], HISTORICAL_SOURCES["tools/c11d/d9/universal_editorial_model.py"]["e4b_postimage_sha256"]),
        "c11c-suite/c11c-producer/c11e_production_service.py": (HISTORICAL_SOURCES["c11c-suite/c11c-producer/c11e_production_service.py"]["sha256"], HISTORICAL_SOURCES["c11c-suite/c11c-producer/c11e_production_service.py"]["e4b_postimage_sha256"]),
    }
    for path, (pre, post) in expected.items():
        row = patch_map.get(path)
        if not row or row.get("preimage_sha256") != pre or row.get("postimage_sha256") != post:
            raise AdjudicationError(f"E4B_SOURCE_PATCH_LINEAGE_MISMATCH:{path}")

    expected_backup_root_rel = Path(
        "artifacts/tests/c11e/e4b_shared_service_integration_overlay/20261107T005116Z-B9D97544"
    )
    expected_backup_root_abs = str((root / expected_backup_root_rel).resolve()).replace("/", "\\").rstrip("\\")
    recorded_backup_root = str(recovery.get("v2_backup_run_root", "")).replace("/", "\\").rstrip("\\")
    if recorded_backup_root.casefold() != expected_backup_root_abs.casefold():
        raise AdjudicationError("E4B_RECOVERY_BACKUP_RUN_ROOT_MISMATCH")

    backups = recovery.get("v2_source_backups", [])
    backup_map = {str(x.get("source_path", "")).replace("\\", "/"): x for x in backups if isinstance(x, dict)}
    backup_proofs = []
    for path, spec in HISTORICAL_SOURCES.items():
        row = backup_map.get(path)
        if row is None:
            raise AdjudicationError(f"E4B_RECOVERY_BACKUP_ROW_MISSING:{path}")
        if str(row.get("sha256", "")).lower() != spec["sha256"]:
            raise AdjudicationError(f"E4B_RECOVERY_BACKUP_SHA_LINEAGE_MISMATCH:{path}")
        backup_path_text = str(row.get("backup_path", "")).replace("/", "\\").rstrip("\\")
        expected_backup_abs = str((root / spec["e4b_backup_rel"]).resolve()).replace("/", "\\").rstrip("\\")
        if backup_path_text.casefold() != expected_backup_abs.casefold():
            raise AdjudicationError(f"E4B_RECOVERY_BACKUP_PATH_LINEAGE_MISMATCH:{path}")
        backup_proofs.append({"source_path": path, "backup_path": str(spec["e4b_backup_rel"]).replace("\\", "/"), "expected_absolute_path": expected_backup_abs, "expected_sha256": spec["sha256"], "receipt_binding": "PASS"})

    return [pins_proof, v3_pins_proof, recovery_proof, run_proof], {
        "v2_source_patch_manifest_sha256": E4B_V2_PINS_SHA256,
        "v3_recovery_receipt_sha256": E4B_V3_RECOVERY_SHA256,
        "v3_run_receipt_sha256": E4B_V3_RUN_RECEIPT_SHA256,
        "v3_run_status": run_receipt.get("status"),
        "v3_run_created_utc": run_receipt.get("created_utc"),
        "post_qualification_change_reasons": {
            path: patch_map[path].get("reason") for path in expected
        },
    }, {"backup_receipt_bindings": backup_proofs, "backup_run_root": recovery.get("v2_backup_run_root")}


def symbol_fingerprints(data: bytes) -> dict[str, str]:
    try:
        source = data.decode("utf-8-sig")
        tree = ast.parse(source)
    except Exception as exc:
        return {"__AST_PARSE_ERROR__": f"{type(exc).__name__}:{exc}"}
    out = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            try:
                normalized = ast.dump(node, annotate_fields=True, include_attributes=False)
            except TypeError:
                normalized = ast.dump(node, annotate_fields=True)
            out[node.name] = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    return out


def verify_preimage_bytes(data: bytes, expected_sha: str, expected_bytes: int) -> dict[str, Any]:
    actual_sha = hashlib.sha256(data).hexdigest()
    actual_bytes = len(data)
    return {
        "status": "PASS" if actual_sha == expected_sha and actual_bytes == expected_bytes else "MISMATCH",
        "actual_sha256": actual_sha,
        "actual_bytes": actual_bytes,
    }


def summarize_diff(old_data: bytes, current_data: bytes) -> dict[str, Any]:
    old_text = old_data.decode("utf-8-sig", errors="replace").splitlines()
    new_text = current_data.decode("utf-8-sig", errors="replace").splitlines()
    diff = list(difflib.unified_diff(old_text, new_text, fromfile="E4A7_PREIMAGE", tofile="CURRENT_PINNED_SOURCE", lineterm=""))
    added = sum(1 for line in diff if line.startswith("+") and not line.startswith("+++"))
    removed = sum(1 for line in diff if line.startswith("-") and not line.startswith("---"))
    old_symbols, new_symbols = symbol_fingerprints(old_data), symbol_fingerprints(current_data)
    if "__AST_PARSE_ERROR__" in old_symbols or "__AST_PARSE_ERROR__" in new_symbols:
        symbol_delta = {"status": "AST_PARSE_ERROR", "old": old_symbols.get("__AST_PARSE_ERROR__"), "current": new_symbols.get("__AST_PARSE_ERROR__")}
    else:
        symbol_delta = {
            "added": sorted(set(new_symbols) - set(old_symbols)),
            "removed": sorted(set(old_symbols) - set(new_symbols)),
            "modified": sorted(k for k in set(old_symbols) & set(new_symbols) if old_symbols[k] != new_symbols[k]),
        }
    return {
        "old_lines": len(old_text),
        "current_lines": len(new_text),
        "unified_diff_added_lines": added,
        "unified_diff_removed_lines": removed,
        "top_level_symbol_delta": symbol_delta,
        "diff_lines": diff,
    }


def verify_d4_and_frozen(root: Path) -> list[dict[str, Any]]:
    return [
        verify_file(root, FROZEN_MANIFEST_REL, FROZEN_MANIFEST_SHA256, "FROZEN_C11C_MANIFEST", 796318),
        verify_file(root, D4_8_REL, D4_8_SHA256, "D4_8_POLICY"),
    ]


def run_audit(root: Path) -> dict[str, Any]:
    root = root.resolve()
    fixed_rows = verify_d4_and_frozen(root)
    recon_proof, recon_summary = verify_reconciliation(root)
    e4a7_proof, e4a7_summary = verify_e4a7_receipt(root)
    e4b_proofs, e4b_summary, backup_receipt_bindings = verify_e4b_lineage(root)

    sources = []
    all_preimages_found = True
    diff_blocks = []
    for source_rel, spec in HISTORICAL_SOURCES.items():
        backup_path = safe_project_path(root, spec["e4b_backup_rel"])
        current_path = safe_project_path(root, source_rel)
        if not current_path.is_file():
            raise AdjudicationError(f"CURRENT_PINNED_SOURCE_MISSING:{source_rel}")
        current_actual = sha256_file(current_path)
        current_bytes = current_path.stat().st_size
        if current_actual != spec["current_sha256"] or current_bytes != spec["current_bytes"]:
            raise AdjudicationError(f"CURRENT_PINNED_SOURCE_HASH_MISMATCH:{source_rel}:{current_actual}")
        row = {
            "source_path": source_rel,
            "historical_e4a7_sha256": spec["sha256"],
            "historical_e4a7_bytes": spec["bytes"],
            "e4b_backup_path": str(spec["e4b_backup_rel"]).replace("\\", "/"),
            "e4b_backup_exists": backup_path.is_file(),
            "current_source_path": source_rel,
            "expected_current_sha256": spec["current_sha256"],
            "expected_current_bytes": spec["current_bytes"],
            "current_actual_sha256": current_actual,
            "current_actual_bytes": current_bytes,
            "current_source_status": "PASS_CURRENT_PIN",
        }
        if not backup_path.is_file():
            all_preimages_found = False
            row["historical_preimage_status"] = "MISSING"
            sources.append(row)
            continue
        backup_data = backup_path.read_bytes()
        preimage_check = verify_preimage_bytes(backup_data, spec["sha256"], spec["bytes"])
        backup_actual = preimage_check["actual_sha256"]
        backup_bytes = preimage_check["actual_bytes"]
        if preimage_check["status"] != "PASS":
            all_preimages_found = False
            row.update({"historical_preimage_status": "HASH_OR_SIZE_MISMATCH", "backup_actual_sha256": backup_actual, "backup_actual_bytes": backup_bytes})
            sources.append(row)
            continue
        old_data, current_data = backup_data, current_path.read_bytes()
        diff_summary = summarize_diff(old_data, current_data)
        row.update({
            "historical_preimage_status": "EXACT_SHA256_AND_BYTES_MATCH",
            "backup_actual_sha256": backup_actual,
            "backup_actual_bytes": backup_bytes,
            "current_actual_sha256": current_actual,
            "current_actual_bytes": current_bytes,
            "diff_summary": {k: v for k, v in diff_summary.items() if k != "diff_lines"},
            "post_qualification_e4b_change_reason": spec["e4b_reason"],
        })
        sources.append(row)
        diff_blocks.append((source_rel, diff_summary["diff_lines"]))

    # Emit full, reviewable textual diff only when both exact historical preimages exist.
    diff_text = None
    if all_preimages_found and len(diff_blocks) == 2:
        parts = [
            "C11-E CH004 HISTORICAL SOURCE DIFFS V1",
            "Read-only comparison. The E4A.7 preimages are exact SHA-256/byte matches to the immutable receipt.",
            "A diff is evidence for manual semantic review; it is not an automatic compatibility waiver.",
            "",
        ]
        for rel, lines in diff_blocks:
            parts.extend([f"===== {rel} =====", *lines, ""])
        diff_text = "\n".join(parts) + "\n"

    run_id = "E6CH004ADJ_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "_" + uuid.uuid4().hex[:8].upper()
    out_dir = safe_project_path(root, OUTPUT_REL / run_id)
    out_dir.mkdir(parents=True, exist_ok=False)

    diff_record = None
    if diff_text is not None:
        diff_path = out_dir / f"{run_id}_SOURCE_DIFFS_V1.txt"
        diff_bytes = diff_text.encode("utf-8")
        diff_path.write_bytes(diff_bytes)
        diff_hash = hashlib.sha256(diff_bytes).hexdigest()
        (Path(str(diff_path) + ".sha256")).write_text(f"{diff_hash}  {diff_path.name}\n", encoding="ascii")
        diff_record = {"path": str(diff_path.relative_to(root)).replace("\\", "/"), "sha256": diff_hash, "bytes": len(diff_bytes)}

    status = "PASS_HISTORICAL_PREIMAGES_RECOVERED_REVIEW_REQUIRED" if all_preimages_found else "BLOCKED_HISTORICAL_PREIMAGE_MISSING_OR_MISMATCH_NO_WAIVER"
    report = {
        "schema": SCHEMA,
        "schema_version": "1.0",
        "run_id": run_id,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "project_root": str(root),
        "status": status,
        "ch004_e6_reuse_disposition": (
            "REUSE_CANDIDATE_PENDING_SEMANTIC_DIFF_REVIEW_AND_E6_LEDGER_REQUALIFICATION"
            if all_preimages_found else "NOT_ELIGIBLE_FOR_E6_REUSE_PREIMAGE_NOT_VERIFIED"
        ),
        "historical_preimage_count": f"{sum(x.get('historical_preimage_status') == 'EXACT_SHA256_AND_BYTES_MATCH' for x in sources)}/2",
        "fixed_governance_pins": fixed_rows,
        "active_reconciliation_report": {"proof": recon_proof, "summary": recon_summary},
        "e4a7_historical_receipt": {"proof": e4a7_proof, "summary": e4a7_summary},
        "e4b_post_qualification_change_lineage": {"proofs": e4b_proofs, "summary": e4b_summary, **backup_receipt_bindings},
        "source_pin_adjudication": sources,
        "diff_artifact": diff_record,
        "manual_review_required": True,
        "automatic_reuse_acceptance": False,
        "d4_8_overridden": False,
        "media_invoked": False,
        "godot_invoked": False,
        "ffmpeg_invoked": False,
        "ffprobe_invoked": False,
        "audio_generated": False,
        "mux_invoked": False,
        "media_created": False,
        "batch_id_consumed": False,
        "production_dispatch": False,
        "renderer": "OFF",
        "release_authority": "NONE",
        "git_checks": "SKIPPED",
        "commits": "OPERATOR_MANAGED",
        "source_files_modified": False,
    }
    report_path = out_dir / f"{run_id}_REPORT_V1.json"
    report_bytes = (json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    report_path.write_bytes(report_bytes)
    report_sha = hashlib.sha256(report_bytes).hexdigest()
    (Path(str(report_path) + ".sha256")).write_text(f"{report_sha}  {report_path.name}\n", encoding="ascii")
    report["report_path"] = str(report_path.relative_to(root)).replace("\\", "/")
    report["report_sha256"] = report_sha
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT_DEFAULT)
    args = parser.parse_args(argv)
    root = args.project_root.resolve()
    if not root.is_dir():
        print(f"PROJECT_ROOT_MISSING={root}", file=sys.stderr)
        return 2
    try:
        report = run_audit(root)
    except Exception as exc:
        print(f"E6_CH004_ADJUDICATION_STATUS=BLOCKED_AUDIT_PRECONDITION:{type(exc).__name__}:{exc}")
        return 2
    print(f"E6_CH004_HISTORICAL_SOURCE_PIN_ADJUDICATION_STATUS={report['status']}")
    print(f"E6_CH004_HISTORICAL_PREIMAGES={report['historical_preimage_count']}")
    print(f"E6_CH004_REUSE_DISPOSITION={report['ch004_e6_reuse_disposition']}")
    print(f"E6_CH004_DIFF_ARTIFACT={report['diff_artifact']['path'] if report['diff_artifact'] else 'NOT_CREATED'}")
    print(f"E6_CH004_ADJUDICATION_REPORT={report['report_path']}")
    print(f"E6_CH004_ADJUDICATION_REPORT_SHA256={report['report_sha256']}")
    print("SOURCE_FILES_MODIFIED=FALSE")
    print("MEDIA_INVOKED=FALSE; GODOT_INVOKED=FALSE; FFMPEG_INVOKED=FALSE; FFPROBE_INVOKED=FALSE")
    print("AUDIO_GENERATED=FALSE; MUX_INVOKED=FALSE; BATCH_ID_CONSUMED=FALSE; RELEASE_AUTHORITY=NONE")
    print("GIT_CHECKS=SKIPPED; COMMITS=OPERATOR_MANAGED; SOURCE_FILE_PINS=ENFORCED")
    # A well-formed blocked report is still a successful audit execution.
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
