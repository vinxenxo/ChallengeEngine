#!/usr/bin/env python3
"""Read-only CH004 E4A.7 semantic non-interference review V2.

Verifies the two E4A.7 source preimages, the transitive D9.8 JSON preimage,
E4B recovery lineage, JSON scope, six-selector Challenge resolver parity, and
old/current E1 Challenge preparation parity. It does not alter source/evidence,
restore backups, execute media, reserve BatchId, or change governance.
"""
from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import importlib.util
import json
import os
import shutil
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any, Mapping

SCHEMA = "C11E-E6-CH004-SEMANTIC-NONINTERFERENCE-REVIEW-V2"
OUTPUT_REL = Path("artifacts/tests/c11e/e6_ch004_semantic_noninterference")

FROZEN_MANIFEST_REL = "release/C11C_FREEZE_PACKAGE_MANIFEST.json"
FROZEN_MANIFEST_SHA = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
D4_8_REL = "definitions/c11d/production/C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V2.json"
D4_8_SHA = "0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07"

RECON_REL = (
    "artifacts/tests/c11e/e6_d9_dependency_pin_reconciliation/"
    "E6D9PINREC_20261118T094345Z_2B9358D1/E6D9PINREC_20261118T094345Z_2B9358D1_REPORT_V1.json"
)
RECON_SHA = "0e2c977f1122d9cfc69da255d8fa539720a23f00cdc2f4c030d48bd01019a59a"
V1_ADJ_REPORT_REL = (
    "artifacts/tests/c11e/e6_ch004_source_pin_adjudication/"
    "E6CH004ADJ_20261118T101236Z_6C62AE7F/E6CH004ADJ_20261118T101236Z_6C62AE7F_REPORT_V1.json"
)
V1_ADJ_REPORT_SHA = "d99cec7ac6b0edb71665eadfd25314bd4eebece0bca9e17f05fa9cf943fa6ebd"
V1_ADJ_RUN_ID = "E6CH004ADJ_20261118T101236Z_6C62AE7F"
E4A7_RECEIPT_REL = (
    "artifacts/tests/c11e/e4a_d_composited_av_review/"
    "RUN_20261106T070808Z-62F31F9C/C11E_E4A7_D_COMPOSITED_CHALLENGE_AV_RECEIPT.json"
)
E4A7_RECEIPT_SHA = "102cf07a0b8920318c3ba211a3bd4374c3e080018486363d701f81e65613aaa0"
E5_AV_CLOSEOUT_REL = "docs/current/e/C11E_E5_CROSS_FAMILY_AV_CLOSEOUT_20261116_V1.md"
E5_AV_CLOSEOUT_SHA = "520515803ceb44bde830f99c6fa9b413015d0fecd4c36c60c845128054cbb760"
E4A6_ENVELOPE_REL = (
    "artifacts/tests/c11e/e4a6_reserved_bands_black/BLACK_BANDS_V2/e4a6_challenge_004_envelope.json"
)
E4A6_ENVELOPE_SHA = "2a62637072d34f2b68e11f92ddb1d7d981d870507e696c800396a8e15f8a527e"

E4B_V2_PINS_REL = "tools/c11d/d9/C11E_E4B_SHARED_SERVICE_INTEGRATION_V2_SOURCE_PINS.json"
E4B_V2_PINS_SHA = "c57c20abab5f58f32174d0b0cbef51d72b5c2ef473812d6d309a962c116df7be"
E4B_V3_PINS_REL = "tools/c11d/d9/C11E_E4B_SHARED_SERVICE_INTEGRATION_V3_SOURCE_PINS.json"
E4B_V3_PINS_SHA = "dc97cf4a3361414e46bf5996b1cbdb6adda384853da702104cd6876134e43328"
E4B_V3_RECOVERY_REL = (
    "artifacts/tests/c11e/e4b_shared_service_integration_recovery_v3/"
    "20261107T010101Z-A05C1878/C11E_E4B_SHARED_SERVICE_INTEGRATION_V3_RECOVERY_RECEIPT.json"
)
E4B_V3_RECOVERY_SHA = "09f78d97c8797885056882b343e1ee54e3fc2bb75cf2320338c037f6ea893048"
E4B_V3_RUN_REL = (
    "artifacts/tests/c11e/e4b_shared_service_integration_v3/"
    "20261107T010113Z-CCE37AD9/C11E_E4B_SHARED_SERVICE_INTEGRATION_RUN_RECEIPT_V3.json"
)
E4B_V3_RUN_SHA = "622ecf63186b17f50dfce23ab699385190d605a48222e5120d647af50a73ceaf"
E4B_SERVICE_INTERMEDIATE_SHA = "08ab5a278de8ebb55795a57391c83a27207ce01920704c419b8e28be25ddcf65"

BACKUP_ROOT = Path(
    "artifacts/tests/c11e/e4b_shared_service_integration_overlay/"
    "20261107T005116Z-B9D97544/b"
)
SOURCES = {
    "tools/c11d/d9/universal_editorial_model.py": {
        "pre_sha": "5c575be1942ba0613d66579d14db5cf9d7786e7062dfb001bd7be8a2e9c18ae5",
        "pre_bytes": 26574,
        "current_sha": "dac95fb698b52f96432a517d8ec3196a397e5e6bd3c025300350dd55ddce3afd",
        "current_bytes": 27585,
        "backup": BACKUP_ROOT / "05.bak",
        "slot": "05.bak",
    },
    "c11c-suite/c11c-producer/c11e_production_service.py": {
        "pre_sha": "348997e575d985fe153a4f433f089c5f205be5d4d8f3853baf07be917a134951",
        "pre_bytes": 32885,
        "current_sha": "e5dbf9baa72d4c066ff8ba24006df954700d72a5b0f11f9f88aec653e84dce87",
        "current_bytes": 86687,
        "backup": BACKUP_ROOT / "01.bak",
        "slot": "01.bak",
    },
    "definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json": {
        "pre_sha": "50655c82521a353f1db6920f4d099cad92452ae369251f9fbde45cbaee4e8c53",
        "pre_bytes": 12692,
        "current_sha": "dabb458fc2215156ddb5ebea7e8ebec811098886ce2858733ba9fb13f6075ccb",
        "current_bytes": 12932,
        "backup": BACKUP_ROOT / "04.bak",
        "slot": "04.bak",
    },
}

E4B_V3_BACKUP_PATHS = {
    "tools/c11d/d9/universal_editorial_model.py": "05.bak",
    "c11c-suite/c11c-producer/c11e_production_service.py": "01.bak",
    "definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json": "04.bak",
}

ALLOWED_MODEL_ADDITIONS = {
    ("content_types", "visual_loops", "d9_9_plan_compatible"): True,
    ("content_types", "visual_loops", "d4_executable_compatible"): False,
    ("content_types", "visual_drills", "d9_9_plan_compatible"): True,
    ("content_types", "visual_drills", "d4_executable_compatible"): False,
}
CHALLENGE_IDS = [
    "CHALLENGE_001", "CHALLENGE_002", "CHALLENGE_004",
    "CHALLENGE_005", "CHALLENGE_006", "CHALLENGE_007",
]

class ReviewError(RuntimeError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_path(root: Path, relative: str | Path) -> Path:
    raw = str(relative).replace("\\", "/")
    p = PurePosixPath(raw)
    if not raw or p.is_absolute() or ".." in p.parts or (len(raw) >= 2 and raw[1] == ":"):
        raise ReviewError(f"UNSAFE_PROJECT_PATH:{relative}")
    base = root.resolve()
    candidate = base.joinpath(*p.parts)
    current = base
    for part in p.parts:
        current = current / part
        if current.is_symlink() or _is_reparse(current):
            raise ReviewError(f"REPARSE_POINT_IN_PROJECT_PATH:{relative}")
    resolved = candidate.resolve(strict=False)
    if resolved != base and base not in resolved.parents:
        raise ReviewError(f"PATH_ESCAPES_PROJECT_ROOT:{relative}")
    return resolved


def _is_reparse(path: Path) -> bool:
    try:
        return bool(getattr(path.stat(follow_symlinks=False), "st_file_attributes", 0) & 0x400)
    except (OSError, AttributeError):
        return False


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise ReviewError(f"INVALID_JSON:{path}:{exc}") from exc
    if not isinstance(value, dict):
        raise ReviewError(f"EXPECTED_JSON_OBJECT:{path}")
    return value


def verify_file(root: Path, rel: str, expected: str, label: str, expected_bytes: int | None = None) -> dict[str, Any]:
    path = safe_path(root, rel)
    if not path.is_file():
        raise ReviewError(f"{label}_MISSING:{rel}")
    actual = sha256_file(path)
    size = path.stat().st_size
    if actual != expected:
        raise ReviewError(f"{label}_SHA256_MISMATCH:{rel}:{actual}")
    if expected_bytes is not None and size != expected_bytes:
        raise ReviewError(f"{label}_BYTE_COUNT_MISMATCH:{rel}:{size}")
    return {"path": rel, "bytes": size, "sha256": actual, "status": "PASS"}


def _sidecar_for(path: Path, expected_sha: str) -> dict[str, Any]:
    sidecar = Path(str(path) + ".sha256")
    if not sidecar.is_file():
        raise ReviewError(f"SIDECAR_MISSING:{sidecar}")
    value = sidecar.read_text(encoding="ascii", errors="strict").strip().split()
    if not value or value[0].lower() != expected_sha.lower():
        raise ReviewError(f"SIDECAR_SHA_MISMATCH:{sidecar}")
    return {"path": str(sidecar), "sha256": value[0].lower(), "status": "PASS"}


def verify_v1_adjudication(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    proof = verify_file(root, V1_ADJ_REPORT_REL, V1_ADJ_REPORT_SHA, "V1_ADJUDICATION_REPORT")
    path = safe_path(root, V1_ADJ_REPORT_REL)
    side = _sidecar_for(path, V1_ADJ_REPORT_SHA)
    report = load_json(path)
    if report.get("run_id") != V1_ADJ_RUN_ID:
        raise ReviewError("V1_ADJUDICATION_RUN_ID_MISMATCH")
    if report.get("status") != "PASS_HISTORICAL_PREIMAGES_RECOVERED_REVIEW_REQUIRED":
        raise ReviewError("V1_ADJUDICATION_STATUS_MISMATCH")
    if report.get("historical_preimage_count") != "2/2" or report.get("automatic_reuse_acceptance") is not False:
        raise ReviewError("V1_ADJUDICATION_PREIMAGE_OR_ACCEPTANCE_FLAGS_MISMATCH")

    # Bind the report's two historical source rows to the exact receipt preimages and
    # the independently observed current postimages. Do not trust a status label alone.
    adjudication_rows = {
        str(row.get("source_path", "")).replace("\\", "/"): row
        for row in report.get("source_pin_adjudication", []) if isinstance(row, Mapping)
    }
    for rel, spec in SOURCES.items():
        if rel.endswith("C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json"):
            continue
        row = adjudication_rows.get(rel)
        if not row:
            raise ReviewError(f"V1_ADJUDICATION_SOURCE_ROW_MISSING:{rel}")
        if row.get("historical_e4a7_sha256") != spec["pre_sha"] or row.get("historical_e4a7_bytes") != spec["pre_bytes"]:
            raise ReviewError(f"V1_ADJUDICATION_PREIMAGE_BINDING_MISMATCH:{rel}")
        if row.get("expected_current_sha256") != spec["current_sha"] or row.get("current_actual_sha256") != spec["current_sha"]:
            raise ReviewError(f"V1_ADJUDICATION_CURRENT_SOURCE_BINDING_MISMATCH:{rel}")
        if row.get("historical_preimage_status") != "EXACT_SHA256_AND_BYTES_MATCH":
            raise ReviewError(f"V1_ADJUDICATION_PREIMAGE_STATUS_MISMATCH:{rel}")

    diff_record = report.get("diff_artifact")
    if not isinstance(diff_record, Mapping) or not diff_record.get("path"):
        raise ReviewError("V1_DIFF_ARTIFACT_RECORD_MISSING")
    diff_path = safe_path(root, str(diff_record["path"]))
    if not diff_path.is_file():
        raise ReviewError("V1_DIFF_ARTIFACT_MISSING")
    diff_sha = sha256_file(diff_path)
    if diff_sha != diff_record.get("sha256"):
        raise ReviewError("V1_DIFF_ARTIFACT_HASH_MISMATCH")
    diff_side = _sidecar_for(diff_path, diff_sha)
    diff_text = diff_path.read_text(encoding="utf-8-sig", errors="replace")
    for required in ("universal_editorial_model.py", "c11e_production_service.py", "request_plan_state", "visual_loops", "visual_drills"):
        if required not in diff_text:
            raise ReviewError(f"V1_DIFF_REQUIRED_REVIEW_TERM_MISSING:{required}")
    return {"report": proof, "report_sidecar": side, "diff": {"path": str(diff_record["path"]), "sha256": diff_sha, "bytes": diff_path.stat().st_size, "sidecar": diff_side}}, {
        "status": report.get("status"), "historical_preimage_count": report.get("historical_preimage_count"),
        "source_pin_adjudication": report.get("source_pin_adjudication"),
        "e4b_lineage": report.get("e4b_post_qualification_change_lineage"),
    }


def verify_reconciliation(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    proof = verify_file(root, RECON_REL, RECON_SHA, "V2_RECONCILIATION_REPORT")
    report = load_json(safe_path(root, RECON_REL))
    counts = report.get("counts", {})
    expected_counts = {
        "accepted_source_pins": "33/33", "additional_route_dependencies": "9/9",
        "ch004_observed_current_hashes": "2/2", "fixed_evidence_pins": "13/13",
    }
    if counts != expected_counts:
        raise ReviewError(f"RECONCILIATION_COUNTS_MISMATCH:{counts}")
    hydration = report.get("hydration_v2_reconciliation", {})
    if hydration.get("check_count") != 1803 or hydration.get("passed_checks") != 1801 or hydration.get("failed_checks") != 2:
        raise ReviewError("HYDRATION_RECONCILIATION_TOTALS_MISMATCH")
    if hydration.get("failure_categories") != {"historical_source_pin_divergence": 2, "other_failures": 0}:
        raise ReviewError("HYDRATION_RECONCILIATION_FAILURE_CATEGORY_MISMATCH")
    divergences = {str(x.get("path", "")): x for x in hydration.get("historical_divergences", []) if isinstance(x, Mapping)}
    expected_divergences = {
        "tools/c11d/d9/universal_editorial_model.py": (SOURCES["tools/c11d/d9/universal_editorial_model.py"]["pre_sha"], SOURCES["tools/c11d/d9/universal_editorial_model.py"]["current_sha"]),
        "c11c-suite/c11c-producer/c11e_production_service.py": (SOURCES["c11c-suite/c11c-producer/c11e_production_service.py"]["pre_sha"], SOURCES["c11c-suite/c11c-producer/c11e_production_service.py"]["current_sha"]),
    }
    if set(divergences) != set(expected_divergences):
        raise ReviewError("HYDRATION_HISTORICAL_DIVERGENCE_PATH_SET_MISMATCH")
    for rel, (old_sha, current_sha) in expected_divergences.items():
        row = divergences[rel]
        if row.get("expected_sha256") != old_sha or row.get("actual_sha256") != current_sha:
            raise ReviewError(f"HYDRATION_HISTORICAL_DIVERGENCE_HASH_MISMATCH:{rel}")
    if report.get("blockers") not in ([], None):
        raise ReviewError("RECONCILIATION_HAS_BLOCKERS")
    return proof, {"counts": counts, "hydration": hydration, "status": report.get("status")}


def verify_governance_and_e4b(root: Path) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    rows = [
        verify_file(root, FROZEN_MANIFEST_REL, FROZEN_MANIFEST_SHA, "FROZEN_MANIFEST", 796318),
        verify_file(root, D4_8_REL, D4_8_SHA, "D4_8_POLICY"),
        verify_file(root, E4A7_RECEIPT_REL, E4A7_RECEIPT_SHA, "E4A7_RECEIPT"),
        verify_file(root, E5_AV_CLOSEOUT_REL, E5_AV_CLOSEOUT_SHA, "E5_OPERATOR_AV_CLOSEOUT"),
        verify_file(root, E4A6_ENVELOPE_REL, E4A6_ENVELOPE_SHA, "E4A6_ENVELOPE"),
        verify_file(root, E4B_V2_PINS_REL, E4B_V2_PINS_SHA, "E4B_V2_PINS"),
        verify_file(root, E4B_V3_PINS_REL, E4B_V3_PINS_SHA, "E4B_V3_PINS"),
        verify_file(root, E4B_V3_RECOVERY_REL, E4B_V3_RECOVERY_SHA, "E4B_V3_RECOVERY_RECEIPT"),
        verify_file(root, E4B_V3_RUN_REL, E4B_V3_RUN_SHA, "E4B_V3_RUN_RECEIPT"),
    ]
    e4a7 = load_json(safe_path(root, E4A7_RECEIPT_REL))
    if e4a7.get("run_id") != "20261106T070808Z-62F31F9C" or e4a7.get("status") != "PASS_ISOLATED_E4A7_D_COMPOSITED_CHALLENGE_AV_TEST_ONLY":
        raise ReviewError("E4A7_RECEIPT_IDENTITY_MISMATCH")
    e4a7_pins = e4a7.get("source_pins", {})
    for pin_key, rel in (("d9_editorial", "tools/c11d/d9/universal_editorial_model.py"), ("e1_service", "c11c-suite/c11c-producer/c11e_production_service.py")):
        row = e4a7_pins.get(pin_key, {})
        spec = SOURCES[rel]
        if row.get("path") != rel or row.get("sha256") != spec["pre_sha"] or row.get("bytes") != spec["pre_bytes"]:
            raise ReviewError(f"E4A7_HISTORICAL_SOURCE_PIN_MISMATCH:{pin_key}")
    e4a7_invariants = e4a7.get("invariants", {})
    for key in ("C11C_generators_unchanged", "D_layer_embedded_in_source_video", "gameplay_video_not_rerendered", "source_video_h264_stream_identical_in_all_muxes"):
        if e4a7_invariants.get(key) is not True:
            raise ReviewError(f"E4A7_A_V_INVARIANT_NOT_CONFIRMED:{key}")
    e5_closeout = safe_path(root, E5_AV_CLOSEOUT_REL).read_text(encoding="utf-8-sig", errors="replace")
    if "PASS_TEST_ONLY_OPERATOR_A_V_ACCEPTED" not in e5_closeout or "Challenge | `parking_v2 / CHALLENGE_004`" not in e5_closeout or "PASS — video, audio, editorial, music, layout" not in e5_closeout:
        raise ReviewError("E5_CHALLENGE_OPERATOR_AV_ACCEPTANCE_NOT_PINNED")
    e1 = load_json(safe_path(root, E4A6_ENVELOPE_REL)).get("e1_intent")
    if not isinstance(e1, Mapping) or e1.get("request", {}).get("selection", {}).get("variant_id") != "CHALLENGE_004":
        raise ReviewError("E4A6_E1_INTENT_CHALLENGE004_MISSING")
    if e1.get("service_version") != "0.2.0-E3.2" or len(e1.get("source_identity", {}).get("source_pins", [])) != 12:
        raise ReviewError("E4A6_HISTORICAL_E1_SOURCE_IDENTITY_MISMATCH")

    v2_pins = load_json(safe_path(root, E4B_V2_PINS_REL))
    v3_pins = load_json(safe_path(root, E4B_V3_PINS_REL))
    recovery = load_json(safe_path(root, E4B_V3_RECOVERY_REL))
    run = load_json(safe_path(root, E4B_V3_RUN_REL))
    if recovery.get("status") != "PASS_V2_INSTALL_EFFECTS_CONFIRMED_AND_V3_ADD_ONLY_INSTALLED":
        raise ReviewError("E4B_V3_RECOVERY_STATUS_MISMATCH")
    if run.get("status") != "PASS_TEST_ONLY_SHARED_LOOP_BOUNDARY_PREPARATION_V3" or run.get("service_tests") != "25/25_PASS":
        raise ReviewError("E4B_V3_RUN_RECEIPT_STATUS_OR_TESTS_MISMATCH")
    gov = run.get("governance", {})
    if gov.get("renderer") != "OFF" or gov.get("d4_8") != "BLOCKED" or gov.get("d9_10") != "PREPARE_ONLY" or gov.get("release_authority") != "NONE" or any(gov.get(k) is not False for k in ("launcher_invoked", "dispatch", "audio", "media", "c11c_baseline_modified")):
        raise ReviewError("E4B_V3_GOVERNANCE_BOUNDARY_MISMATCH")
    for label, pin_manifest in (("V2", v2_pins), ("V3", v3_pins)):
        if pin_manifest.get("frozen_c11c_manifest_sha256") != FROZEN_MANIFEST_SHA:
            raise ReviewError(f"E4B_{label}_FROZEN_MANIFEST_BINDING_MISMATCH")

    patch_rows_v2 = {str(x.get("path", "")).replace("\\", "/"): x for x in v2_pins.get("source_patches", []) if isinstance(x, Mapping)}
    patch_rows_v3 = {str(x.get("path", "")).replace("\\", "/"): x for x in v3_pins.get("source_patches", []) if isinstance(x, Mapping)}
    backup_rows = {str(x.get("source_path", "")).replace("\\", "/"): x for x in recovery.get("v2_source_backups", []) if isinstance(x, Mapping)}
    if len(patch_rows_v2) != 6 or len(patch_rows_v3) != 6:
        raise ReviewError("E4B_SOURCE_PATCH_MANIFEST_CARDINALITY_MISMATCH")
    backup_proof = []
    expected_e4b_post = {
        "tools/c11d/d9/universal_editorial_model.py": SOURCES["tools/c11d/d9/universal_editorial_model.py"]["current_sha"],
        "c11c-suite/c11c-producer/c11e_production_service.py": E4B_SERVICE_INTERMEDIATE_SHA,
        "definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json": SOURCES["definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json"]["current_sha"],
    }
    backup_root = PureWindowsPath(str(recovery.get("v2_backup_run_root", "")))
    expected_backup_parent = backup_root / "b"
    for rel, spec in SOURCES.items():
        patch_v2 = patch_rows_v2.get(rel)
        patch_v3 = patch_rows_v3.get(rel)
        backup = backup_rows.get(rel)
        if not patch_v2 or not patch_v3 or not backup:
            raise ReviewError(f"E4B_LINEAGE_ROW_MISSING:{rel}")
        expected_post = expected_e4b_post[rel]
        for label, patch_row in (("V2", patch_v2), ("V3", patch_v3)):
            if patch_row.get("preimage_sha256") != spec["pre_sha"] or patch_row.get("postimage_sha256") != expected_post:
                raise ReviewError(f"E4B_{label}_PATCH_LINEAGE_MISMATCH:{rel}")
        receipt_backup_path = PureWindowsPath(str(backup.get("backup_path", "")))
        expected_backup_path = expected_backup_parent / spec["slot"]
        if backup.get("sha256") != spec["pre_sha"] or receipt_backup_path != expected_backup_path:
            raise ReviewError(f"E4B_BACKUP_RECEIPT_BINDING_MISMATCH:{rel}")
        backup_proof.append({"source_path": rel, "backup_slot": spec["slot"], "backup_sha256": backup.get("sha256"), "e4b_postimage_sha256": expected_post, "status": "PASS_RECEIPT_BOUND"})

    backup_root_text = str(recovery.get("v2_backup_run_root", "")).replace("/", "\\").rstrip("\\")
    expected_root = str((root / BACKUP_ROOT.parent).resolve()).replace("/", "\\").rstrip("\\")
    if backup_root_text.casefold() != expected_root.casefold():
        raise ReviewError("E4B_BACKUP_ROOT_BINDING_MISMATCH")
    return rows, {"e4a7_receipt_status": e4a7.get("status"), "e4a7_run_id": e4a7.get("run_id"), "e5_operator_av_closeout": "PASS_TEST_ONLY_OPERATOR_A_V_ACCEPTED", "e1_intent": dict(e1), "e4b_v3_run_status": run.get("status"), "e4b_v3_service_tests": run.get("service_tests")}, {"backup_receipt_bindings": backup_proof, "backup_run_root": backup_root_text}


def verify_three_preimages(root: Path) -> tuple[list[dict[str, Any]], dict[str, bytes]]:
    proofs = []
    data: dict[str, bytes] = {}
    recovery = load_json(safe_path(root, E4B_V3_RECOVERY_REL))
    backup_rows = {str(x.get("source_path", "")).replace("\\", "/"): x for x in recovery.get("v2_source_backups", []) if isinstance(x, Mapping)}
    expected_backup_parent = PureWindowsPath(str(recovery.get("v2_backup_run_root", ""))) / "b"
    for rel, spec in SOURCES.items():
        backup = safe_path(root, spec["backup"])
        current = safe_path(root, rel)
        if not backup.is_file() or not current.is_file():
            raise ReviewError(f"PREIMAGE_OR_CURRENT_SOURCE_MISSING:{rel}")
        backup_data = backup.read_bytes()
        current_data = current.read_bytes()
        old_sha, new_sha = sha256_bytes(backup_data), sha256_bytes(current_data)
        if old_sha != spec["pre_sha"]:
            raise ReviewError(f"HISTORICAL_PREIMAGE_SHA_MISMATCH:{rel}:{old_sha}")
        if spec["pre_bytes"] is not None and len(backup_data) != spec["pre_bytes"]:
            raise ReviewError(f"HISTORICAL_PREIMAGE_BYTE_COUNT_MISMATCH:{rel}:{len(backup_data)}")
        if new_sha != spec["current_sha"] or len(current_data) != spec["current_bytes"]:
            raise ReviewError(f"CURRENT_SOURCE_PIN_MISMATCH:{rel}:{new_sha}")
        receipt_row = backup_rows.get(rel)
        if not receipt_row or receipt_row.get("sha256") != old_sha:
            raise ReviewError(f"HISTORICAL_PREIMAGE_NOT_BOUND_TO_RECOVERY_RECEIPT:{rel}")
        receipt_backup_path = PureWindowsPath(str(receipt_row.get("backup_path", "")))
        if receipt_backup_path != expected_backup_parent / spec["slot"]:
            raise ReviewError(f"HISTORICAL_PREIMAGE_BACKUP_SLOT_MISMATCH:{rel}")
        data[rel] = backup_data
        proofs.append({"path": rel, "backup_path": str(spec["backup"]).replace("\\", "/"), "preimage_sha256": old_sha, "preimage_bytes": len(backup_data), "current_sha256": new_sha, "current_bytes": len(current_data), "status": "PASS_EXACT_PREIMAGE_AND_CURRENT_PIN"})
    return proofs, data


def _get_path(obj: Mapping[str, Any], path: tuple[str, ...]) -> Any:
    current: Any = obj
    for key in path:
        if not isinstance(current, Mapping) or key not in current:
            return None
        current = current[key]
    return current


def _has_path(obj: Mapping[str, Any], path: tuple[str, ...]) -> bool:
    current: Any = obj
    for key in path:
        if not isinstance(current, Mapping) or key not in current:
            return False
        current = current[key]
    return True


def strip_loop_drill_flags(model: Mapping[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(dict(model))
    for content_type in ("visual_loops", "visual_drills"):
        declaration = result.get("content_types", {}).get(content_type)
        if isinstance(declaration, dict):
            declaration.pop("d9_9_plan_compatible", None)
            declaration.pop("d4_executable_compatible", None)
    return result


def verify_model_semantic_delta(old_data: bytes, current_data: bytes) -> dict[str, Any]:
    old = json.loads(old_data.decode("utf-8-sig"))
    new = json.loads(current_data.decode("utf-8-sig"))
    if not isinstance(old, dict) or not isinstance(new, dict):
        raise ReviewError("D98_MODEL_JSON_ROOT_NOT_OBJECT")
    for path, expected in ALLOWED_MODEL_ADDITIONS.items():
        if _has_path(old, path):
            raise ReviewError(f"D98_MODEL_HISTORICAL_PREIMAGE_ALREADY_HAS_NEW_FLAG:{'.'.join(path)}")
        if _get_path(new, path) is not expected:
            raise ReviewError(f"D98_MODEL_CURRENT_FLAG_VALUE_MISMATCH:{'.'.join(path)}")
    old_projected = strip_loop_drill_flags(old)
    new_projected = strip_loop_drill_flags(new)
    if old_projected != new_projected:
        raise ReviewError("D98_MODEL_CHANGED_OUTSIDE_FOUR_LOOP_DRILL_COMPATIBILITY_FLAGS")
    if old.get("content_types", {}).get("challenges") != new.get("content_types", {}).get("challenges"):
        raise ReviewError("CHALLENGE_MODEL_DECLARATION_CHANGED")
    return {"status": "PASS_ONLY_FOUR_LOOP_DRILL_COMPATIBILITY_FLAGS_ADDED", "allowed_differences": ["content_types.visual_loops.d9_9_plan_compatible", "content_types.visual_loops.d4_executable_compatible", "content_types.visual_drills.d9_9_plan_compatible", "content_types.visual_drills.d4_executable_compatible"], "challenge_declaration_identical": True}


def strip_compatibility_fields(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: strip_compatibility_fields(v) for k, v in value.items() if k not in {"d9_9_plan_compatible", "d4_executable_compatible"}}
    if isinstance(value, list):
        return [strip_compatibility_fields(x) for x in value]
    return value


def challenge_selector_parity(old_module: Any, new_module: Any, old_root: Path, new_root: Path) -> list[dict[str, Any]]:
    rows = []
    for challenge_id in CHALLENGE_IDS:
        selection = {"content_type": "challenges", "variant_id": challenge_id}
        old_node = old_module.resolve_selection(selection, old_root)
        new_node = new_module.resolve_selection(selection, new_root)
        if strip_compatibility_fields(old_node) != strip_compatibility_fields(new_node):
            raise ReviewError(f"D98_CHALLENGE_RESOLVE_SELECTION_DRIFT:{challenge_id}")
        if new_node.get("request_plan_compatible") is not True:
            raise ReviewError(f"D98_CHALLENGE_D4_REQUEST_COMPATIBILITY_NOT_TRUE:{challenge_id}")
        if new_node.get("d9_9_plan_compatible") is not True or new_node.get("d4_executable_compatible") is not True:
            raise ReviewError(f"D98_CHALLENGE_DEFAULT_COMPATIBILITY_FLAGS_NOT_TRUE:{challenge_id}")
        profile = {
            "global": {"title": "C11E semantic audit", "subtitle": "Challenge parity", "call_to_action": "FOLLOW", "language": "ES"},
            "family": {new_node["scope_keys"]["family"]: {"player_name": "Operator", "challenge_label": challenge_id}},
            "variant": {new_node["scope_keys"]["variant"]: {"title": f"{challenge_id} title"}},
        }
        old_res = old_module.resolve_editorial_values(selection, profile=profile, production_override={"call_to_action": "FOLLOW AGAIN"}, project_root=old_root)
        new_res = new_module.resolve_editorial_values(selection, profile=profile, production_override={"call_to_action": "FOLLOW AGAIN"}, project_root=new_root)
        if strip_compatibility_fields(old_res) != strip_compatibility_fields(new_res):
            raise ReviewError(f"D98_CHALLENGE_EDITORIAL_VALUE_DRIFT:{challenge_id}")
        if new_res.get("request_plan_compatible") is not True or new_res.get("request_plan_state") != "CURRENT_D4_CHALLENGE_PATH":
            raise ReviewError(f"D98_CHALLENGE_REQUEST_PLAN_STATE_CHANGED:{challenge_id}")
        rows.append({"challenge_id": challenge_id, "selection": "PASS", "editorial_values": "PASS", "current_d4_path": new_res.get("request_plan_state"), "status": "PASS"})
    return rows


def _copy_file(source_root: Path, target_root: Path, relative: str, expected_sha: str | None = None) -> None:
    src = safe_path(source_root, relative)
    if not src.is_file():
        raise ReviewError(f"FIXTURE_SOURCE_MISSING:{relative}")
    data = src.read_bytes()
    if expected_sha is not None and sha256_bytes(data) != expected_sha:
        raise ReviewError(f"FIXTURE_SOURCE_PIN_MISMATCH:{relative}")
    dst = target_root.joinpath(*PurePosixPath(relative).parts)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(data)


def _copy_tree(source_root: Path, target_root: Path, relative: str) -> None:
    src = safe_path(source_root, relative)
    if not src.is_dir():
        raise ReviewError(f"FIXTURE_DIRECTORY_MISSING:{relative}")
    for item in sorted(src.rglob("*")):
        if item.is_symlink() or _is_reparse(item):
            raise ReviewError(f"REPARSE_POINT_IN_RUNTIME_FIXTURE:{relative}:{item}")
        if not item.is_file():
            continue
        rel = item.relative_to(source_root).as_posix()
        dst = target_root.joinpath(*PurePosixPath(rel).parts)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(item, dst)


def _clear_runtime_imports() -> None:
    for name in list(sys.modules):
        if name in {"c11e_d9_universal_producer_shared", "universal_editorial_model", "c11d_d4_2_normalizer", "c11d_d4_3_personalization", "c11d_d4_4_orchestrator", "c11e_ch004_semantic_service"} or name.startswith("_c11d_d99_"):
            sys.modules.pop(name, None)
    sys.path[:] = [x for x in sys.path if "CH004_SEMANTIC_" not in x]


def build_runtime_fixture(source_root: Path, target_root: Path, e1_intent: Mapping[str, Any], old_data: Mapping[str, bytes] | None) -> None:
    # Canonical E1 pin rows provide the exact source set used by the accepted E4A.6 Challenge intent.
    source_pin_rows = e1_intent.get("source_identity", {}).get("source_pins", [])
    if not isinstance(source_pin_rows, list) or len(source_pin_rows) != 12:
        raise ReviewError("E4A6_E1_SOURCE_PIN_CARDINALITY_MISMATCH")
    historical_override = {
        "tools/c11d/d9/universal_editorial_model.py": "tools/c11d/d9/universal_editorial_model.py",
        "definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json": "definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json",
    }
    for row in source_pin_rows:
        rel = str(row.get("path", ""))
        expected = str(row.get("sha256", ""))
        if not rel or len(expected) != 64:
            raise ReviewError("E4A6_E1_SOURCE_PIN_ROW_INVALID")
        if old_data is not None and rel in historical_override:
            data = old_data[rel]
            if sha256_bytes(data) != expected:
                raise ReviewError(f"E4A6_PREIMAGE_SOURCE_PIN_MISMATCH:{rel}")
            dst = target_root.joinpath(*PurePosixPath(rel).parts)
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(data)
        else:
            _copy_file(source_root, target_root, rel, expected if old_data is not None else None)
    # The two modules under adjudication are the only non-E1-pinned service/resolver replacements.
    service_rel = "c11c-suite/c11c-producer/c11e_production_service.py"
    if old_data is not None:
        for rel in (service_rel,):
            dst = target_root.joinpath(*PurePosixPath(rel).parts)
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(old_data[rel])
    else:
        _copy_file(source_root, target_root, service_rel, SOURCES[service_rel]["current_sha"])

    # D4 GUI adapter imports its closed D4 tools and reads the declarative registry/receipts.
    for rel in ("tools/c11d/d4", "definitions/c11d/production", "definitions/c11d/personalization", "artifacts/tests/c11d_d4"):
        _copy_tree(source_root, target_root, rel)
    # Override the D9.8 model JSON/resolver after the shared directory copy.
    for rel, target in (("tools/c11d/d9/universal_editorial_model.py", "tools/c11d/d9/universal_editorial_model.py"), ("definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json", "definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json")):
        data = old_data[rel] if old_data is not None else safe_path(source_root, rel).read_bytes()
        if sha256_bytes(data) != (SOURCES[rel]["pre_sha"] if old_data is not None else SOURCES[rel]["current_sha"]):
            raise ReviewError(f"RUNTIME_FIXTURE_D98_SOURCE_HASH_MISMATCH:{rel}")
        dst = target_root.joinpath(*PurePosixPath(target).parts)
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(data)

    for rel in (FROZEN_MANIFEST_REL, D4_8_REL):
        _copy_file(source_root, target_root, rel)


def _load_service_module(root: Path, label: str):
    _clear_runtime_imports()
    d9_dir = root / "tools" / "c11d" / "d9"
    sys.path.insert(0, str(d9_dir))
    service_path = root / "c11c-suite" / "c11c-producer" / "c11e_production_service.py"
    name = f"c11e_ch004_semantic_service_{label}"
    spec = importlib.util.spec_from_file_location(name, service_path)
    if spec is None or spec.loader is None:
        raise ReviewError("RUNTIME_SERVICE_IMPORT_FAILED")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _load_editorial_resolver(root: Path, label: str):
    _clear_runtime_imports()
    resolver_path = root / "tools" / "c11d" / "d9" / "universal_editorial_model.py"
    name = f"c11e_ch004_semantic_editorial_{label}"
    spec = importlib.util.spec_from_file_location(name, resolver_path)
    if spec is None or spec.loader is None:
        raise ReviewError("RUNTIME_EDITORIAL_RESOLVER_IMPORT_FAILED")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _historical_raw_request(e1_intent: Mapping[str, Any]) -> dict[str, Any]:
    request = e1_intent["request"]
    seeds = e1_intent["seed_domains"]
    delivery = e1_intent["delivery"]
    return {
        "schema": "C11-D-D9.9-UNIVERSAL-PRODUCER-REQUEST-V1",
        "schema_version": "1.0",
        "request_id": request["request_id"],
        "mode": request["mode"],
        "selection": {"content_type": "challenges", "family_id": "parking_v2", "variant_id": "CHALLENGE_004"},
        "seed": seeds["gameplay"]["value"],
        "music_seed": seeds["music"]["value"],
        "delivery_profile_id": delivery["requested_profile_id"],
        "presentation_profile_id": delivery["presentation_profile_id"],
        "variation_index": request["variation_index"],
        "audio_enabled": delivery["audio_enabled"],
        "personalization_enabled": True,
        "editorial_profile": {},
        "production_override": dict(e1_intent["editorial"]),
        "presentation_options": dict(request["presentation_options"]),
        "provenance": {"source_revision": "C11E-E4A6-LIVE-CONSUMER-TEST-V1", "request_origin": "TEST"},
    }


def _intent_projection(intent: Mapping[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(dict(intent))
    result.pop("service_version", None)
    result.pop("source_identity", None)
    result.pop("intent_sha256", None)
    identity = result.get("identity")
    if isinstance(identity, dict):
        identity.pop("intent_hash", None)
    return result


def compare_source_identity(old_intent: Mapping[str, Any], new_intent: Mapping[str, Any]) -> dict[str, Any]:
    old_rows = old_intent.get("source_identity", {}).get("source_pins", [])
    new_rows = new_intent.get("source_identity", {}).get("source_pins", [])
    old_paths = [row.get("path") for row in old_rows]
    new_paths = [row.get("path") for row in new_rows]
    if old_paths != new_paths:
        raise ReviewError("CHALLENGE_SOURCE_PIN_PATH_SET_OR_ORDER_CHANGED")
    changed = {}
    normalized_new_identity = copy.deepcopy(dict(old_intent.get("source_identity", {})))
    observed_new_identity = copy.deepcopy(dict(new_intent.get("source_identity", {})))
    allowed = {
        "tools/c11d/d9/universal_editorial_model.py": (
            SOURCES["tools/c11d/d9/universal_editorial_model.py"]["pre_sha"],
            SOURCES["tools/c11d/d9/universal_editorial_model.py"]["current_sha"],
            SOURCES["tools/c11d/d9/universal_editorial_model.py"]["pre_bytes"],
            SOURCES["tools/c11d/d9/universal_editorial_model.py"]["current_bytes"],
        ),
        "definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json": (
            SOURCES["definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json"]["pre_sha"],
            SOURCES["definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json"]["current_sha"],
            SOURCES["definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json"]["pre_bytes"],
            SOURCES["definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json"]["current_bytes"],
        ),
    }
    for index, (a, b) in enumerate(zip(old_rows, new_rows)):
        path = str(a.get("path"))
        if path == str(b.get("path")) and (a.get("bytes"), a.get("sha256")) == (b.get("bytes"), b.get("sha256")):
            continue
        expected = allowed.get(path)
        observed = (a.get("sha256"), b.get("sha256"), a.get("bytes"), b.get("bytes"))
        if expected is None or str(b.get("path")) != path or observed != expected:
            raise ReviewError(f"CHALLENGE_SOURCE_IDENTITY_UNEXPECTED_DELTA:{path}")
        changed[path] = {
            "historical_sha256": a.get("sha256"), "historical_bytes": a.get("bytes"),
            "current_sha256": b.get("sha256"), "current_bytes": b.get("bytes"),
            "status": "KNOWN_POST_E4A7_SOURCE_EVOLUTION",
        }
        # Normalize only the two allowed pin values back to their historical values.
        observed_new_identity["source_pins"][index]["sha256"] = a.get("sha256")
        observed_new_identity["source_pins"][index]["bytes"] = a.get("bytes")
    if set(changed) != set(allowed):
        raise ReviewError("CHALLENGE_SOURCE_IDENTITY_CHANGED_PATH_COUNT_MISMATCH")
    if observed_new_identity != normalized_new_identity:
        raise ReviewError("CHALLENGE_SOURCE_IDENTITY_METADATA_CHANGED_OUTSIDE_ALLOWED_PINS")
    return {"source_pin_paths_identical": True, "only_expected_historical_paths_changed": changed, "other_source_identity_metadata_identical": True}


def verify_service_challenge_parity(root: Path, e1_intent: Mapping[str, Any], old_data: Mapping[str, bytes]) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="CH004_SEMANTIC_NONINTERFERENCE_") as tmp:
        base = Path(tmp)
        old_root, new_root = base / "historical", base / "current"
        old_root.mkdir(); new_root.mkdir()
        build_runtime_fixture(root, old_root, e1_intent, old_data)
        build_runtime_fixture(root, new_root, e1_intent, None)
        raw = _historical_raw_request(e1_intent)

        old_service = _load_service_module(old_root, "historical")
        old_prepared = old_service.prepare_c11e_production_intent(raw, old_root, request_origin="TEST")
        old_valid = old_service.validate_c11e_production_intent(old_prepared["intent"], old_root)
        if old_valid.get("status") != "PASS_E1_PREPARATION_ONLY":
            raise ReviewError("HISTORICAL_E1_INTENT_VALIDATION_FAILED")
        historical_intent = e1_intent
        # This exact comparison ties the reconstructed preimage execution to the accepted E4A.6 intent.
        if _intent_projection(old_prepared["intent"]) != _intent_projection(historical_intent):
            raise ReviewError("HISTORICAL_E1_PREIMAGE_REPRODUCTION_MISMATCH")
        if old_prepared["intent"].get("service_version") != "0.2.0-E3.2":
            raise ReviewError("HISTORICAL_E1_SERVICE_VERSION_MISMATCH")

        new_service = _load_service_module(new_root, "current")
        new_prepared = new_service.prepare_c11e_production_intent(raw, new_root, request_origin="TEST")
        new_valid = new_service.validate_c11e_production_intent(new_prepared["intent"], new_root)
        if new_valid.get("status") != "PASS_E1_PREPARATION_ONLY":
            raise ReviewError("CURRENT_E1_CHALLENGE_INTENT_VALIDATION_FAILED")
        if _intent_projection(old_prepared["intent"]) != _intent_projection(new_prepared["intent"]):
            raise ReviewError("E1_CHALLENGE_SEMANTIC_INTENT_CHANGED")
        if new_prepared["intent"].get("service_version") != "0.4.0-E4C":
            raise ReviewError("CURRENT_E1_SERVICE_VERSION_UNEXPECTED")
        source_identity = compare_source_identity(old_prepared["intent"], new_prepared["intent"])
        identity_fields = ("request_hash", "editorial_hash", "plan_hash")
        if any(old_prepared["intent"]["identity"].get(k) != new_prepared["intent"]["identity"].get(k) for k in identity_fields):
            raise ReviewError("E1_CHALLENGE_CANONICAL_IDENTITY_CHANGED")
        return {
            "status": "PASS_E1_CHALLENGE_PREPARATION_PARITY",
            "historical_e1_intent_reproduced": True,
            "historical_validation": old_valid,
            "current_validation": new_valid,
            "same_semantic_intent_projection": True,
            "canonical_identity_fields_equal": list(identity_fields),
            "service_version_transition": [old_prepared["intent"].get("service_version"), new_prepared["intent"].get("service_version")],
            "source_identity_reconciliation": source_identity,
            "renderer_input_emitted": False,
            "dispatch_authorized": False,
            "media_created": False,
        }


def run_audit(root: Path) -> dict[str, Any]:
    root = root.resolve()
    run_id = "E6CH004SEM_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "_" + uuid.uuid4().hex[:8].upper()
    out_dir = safe_path(root, OUTPUT_REL / run_id)
    out_dir.mkdir(parents=True, exist_ok=False)
    evidence: dict[str, Any] = {}
    blockers: list[str] = []
    checks = []
    old_data: dict[str, bytes] = {}
    try:
        v1_proof, v1_summary = verify_v1_adjudication(root)
        checks.append("V1_ADJUDICATION_AND_DIFF=PASS")
        evidence["v1_adjudication"] = {"proof": v1_proof, "summary": v1_summary}
        recon_proof, recon_summary = verify_reconciliation(root)
        checks.append("ACTIVE_RECONCILIATION=PASS")
        evidence["v2_reconciliation"] = {"proof": recon_proof, "summary": recon_summary}
        governance, e4b_summary, backup_summary = verify_governance_and_e4b(root)
        checks.append("E4A7_E4A6_E4B_LINEAGE_AND_GOVERNANCE=PASS")
        evidence["governance_and_e4b"] = {"proofs": governance, "summary": e4b_summary, "backup_receipt_bindings": backup_summary}
        preimage_proofs, old_data = verify_three_preimages(root)
        checks.append("THREE_HISTORICAL_PREIMAGES_AND_CURRENT_FILES=3/3_PASS")
        evidence["three_preimages"] = preimage_proofs
        json_proof = verify_model_semantic_delta(old_data["definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json"], safe_path(root, "definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json").read_bytes())
        checks.append("D98_MODEL_JSON_SCOPE=PASS")
        evidence["model_json_semantic_delta"] = json_proof
        old_model = json.loads(old_data["definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json"].decode("utf-8-sig"))
        current_model = load_json(safe_path(root, "definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json"))
        if strip_loop_drill_flags(old_model) != strip_loop_drill_flags(current_model):
            raise ReviewError("D98_MODEL_GLOBAL_OR_CHALLENGE_CONTRACT_CHANGED")
        e1_intent = e4b_summary["e1_intent"] if "e1_intent" in e4b_summary else load_json(safe_path(root, E4A6_ENVELOPE_REL))["e1_intent"]
        # Build isolated copies for runtime tests; no source writes or runner invocations occur in the checkout.
        with tempfile.TemporaryDirectory(prefix="CH004_RESOLVER_PARITY_ROOTS_") as tmp:
            root_old = Path(tmp) / "old"
            root_new = Path(tmp) / "new"
            root_old.mkdir(); root_new.mkdir()
            # Resolver parity only needs the exact preimage/current resolver + model JSON and unchanged Producer schema.
            for target_root, old_side in ((root_old, True), (root_new, False)):
                for rel in ("c11c-suite/c11c-producer/producer_schema.json",):
                    _copy_file(root, target_root, rel, "564f11fb4fee9221910dc373550650172eda4f106d6dc25532cc43cb8e6314a0")
                for rel in ("tools/c11d/d9/universal_editorial_model.py", "definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json"):
                    data = old_data[rel] if old_side else safe_path(root, rel).read_bytes()
                    dst = target_root.joinpath(*PurePosixPath(rel).parts); dst.parent.mkdir(parents=True, exist_ok=True); dst.write_bytes(data)
            old_mod = _load_editorial_resolver(root_old, "old")
            new_mod = _load_editorial_resolver(root_new, "new")
            selector_rows = challenge_selector_parity(old_mod, new_mod, root_old, root_new)
            if len(selector_rows) != len(CHALLENGE_IDS):
                raise ReviewError("CHALLENGE_SELECTOR_PARITY_CARDINALITY_MISMATCH")
            evidence["challenge_resolver_parity"] = {"status": "PASS", "rows": selector_rows, "count": f"{len(selector_rows)}/{len(CHALLENGE_IDS)}"}
            checks.append("D98_CHALLENGE_RESOLVER_AND_EDITORIAL_PARITY=6/6_PASS")
        service_parity = verify_service_challenge_parity(root, e1_intent, old_data)
        evidence["e1_service_challenge_parity"] = service_parity
        checks.append("E1_CHALLENGE_PREIMAGE_REPRODUCTION_AND_CURRENT_PARITY=PASS")
    except Exception as exc:
        blockers.append(f"{type(exc).__name__}:{exc}")

    passed = not blockers
    report = {
        "schema": SCHEMA,
        "schema_version": "2.0",
        "run_id": run_id,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "project_root": str(root),
        "status": "PASS_CH004_SEMANTIC_NONINTERFERENCE_CONFIRMED_REQUIRES_E6_LEDGER_REQUALIFICATION" if passed else "BLOCKED_CH004_SEMANTIC_REVIEW",
        "ch004_reuse_disposition": "ELIGIBLE_FOR_E6_LEDGER_REQUALIFICATION_NOT_ACCEPTED" if passed else "NOT_ELIGIBLE_PENDING_SEMANTIC_REVIEW",
        "checks": checks,
        "blockers": blockers,
        "evidence": evidence,
        "automatic_e6_acceptance": False,
        "e6_ledger_requalification_required": True,
        "ch004_a_v_evidence_recreated": False,
        "historical_preimages_restored": False,
        "source_files_modified": False,
        "d4_8_overridden": False,
        "renderer": "OFF",
        "dispatch": False,
        "media_invoked": False,
        "godot_invoked": False,
        "ffmpeg_invoked": False,
        "ffprobe_invoked": False,
        "audio_generated": False,
        "mux_invoked": False,
        "media_created": False,
        "batch_id_consumed": False,
        "release_authority": "NONE",
        "git_checks": "SKIPPED",
        "commits": "OPERATOR_MANAGED",
        "source_file_pins": "ENFORCED",
    }
    report_path = out_dir / f"{run_id}_REPORT_V2.json"
    raw = (json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    report_path.write_bytes(raw)
    digest = sha256_bytes(raw)
    (Path(str(report_path) + ".sha256")).write_text(f"{digest}  {report_path.name}\n", encoding="ascii")
    report["report_path"] = str(report_path.relative_to(root)).replace("\\", "/")
    report["report_sha256"] = digest
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[3])
    args = parser.parse_args(argv)
    root = args.project_root.resolve()
    if not root.is_dir():
        print(f"PROJECT_ROOT_MISSING={root}", file=sys.stderr)
        return 2
    report = run_audit(root)
    print(f"E6_CH004_SEMANTIC_REVIEW_STATUS={report['status']}")
    print(f"E6_CH004_REUSE_DISPOSITION={report['ch004_reuse_disposition']}")
    print(f"E6_CH004_SEMANTIC_CHECKS={len(report['checks'])}; BLOCKERS={len(report['blockers'])}")
    print(f"E6_CH004_SEMANTIC_REPORT={report['report_path']}")
    print(f"E6_CH004_SEMANTIC_REPORT_SHA256={report['report_sha256']}")
    print("SOURCE_FILES_MODIFIED=FALSE; HISTORICAL_PREIMAGES_RESTORED=FALSE")
    print("MEDIA_INVOKED=FALSE; GODOT_INVOKED=FALSE; FFMPEG_INVOKED=FALSE; FFPROBE_INVOKED=FALSE")
    print("AUDIO_GENERATED=FALSE; MUX_INVOKED=FALSE; BATCH_ID_CONSUMED=FALSE; RELEASE_AUTHORITY=NONE")
    print("GIT_CHECKS=SKIPPED; COMMITS=OPERATOR_MANAGED; SOURCE_FILE_PINS=ENFORCED")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
