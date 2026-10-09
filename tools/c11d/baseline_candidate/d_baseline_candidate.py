from __future__ import annotations

import ast
import fnmatch
import hashlib
import importlib.util
import json
import os
from pathlib import Path
from typing import Any

POLICY_REL = "definitions/c11d/baseline/D_BASELINE_CANDIDATE_POLICY_V1.json"
C_MANIFEST_REL = "release/C11C_FREEZE_PACKAGE_MANIFEST.json"
D_RENDERER_BASELINE_APPROVAL_REL = "docs/current/d/D_RENDERER_BASELINE_APPROVAL_CHECKPOINT.md"
D_BASELINE_APPROVAL_REL = "docs/current/d/D_BASELINE_APPROVAL_CHECKPOINT.json"
D9_15_OPERATOR_EVIDENCE_WAIVER_REL = "docs/current/d/D9.15_OPERATOR_EVIDENCE_WAIVER_CHECKPOINT.json"
LEGACY_CONTROL_PREFIX = "c11c-suite/c11d-control/"
LEGACY_CONTROL_DIR = "c11c-suite/c11d-control"
MAINTENANCE_LEDGER_REL = "artifacts/maintenance/d9_11/D9_11_MAINTENANCE_LEDGER.json"
QUARANTINE_DESTINATION_PREFIX = "docs/history/root_conflicts/c11d-control_quarantine_"
EXPECTED_C_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
PROTECTED_PREFIXES = ("core/", "assets/", "challenges/", "schemas/", "tests/")
PROTECTED_EXACT = ("build_factory.py", "release_gate.py", "GeneradorMaestro.gd", "Main.tscn", "project.godot")
ALLOWED_D_CHANGE_ROOTS = ("c11c-suite/", "definitions/c11d/", "docs/current/d/", "docs/current/suite/", "tools/c11d/")
EXPECTED_SURFACES = {
    "c11c-test/main.py", "c11c-producer/main.py", "c11c-catalog/main.py",
    "c11c-config/main.py", "c11c-maintenance/main.py",
}
TRANSIENT_DIRS = {
    ".git", ".godot", ".mono", ".import", ".vscode", ".idea", "__pycache__",
    ".pytest_cache", ".mypy_cache", ".ruff_cache", ".venv", "venv", "env", "artifacts",
    "c11c-studio", "c11c-maintenace"
}
EXCLUDED_PREFIXES = ("docs/history/root_conflicts/",)
EXCLUDED_PATTERNS = {
    "*.pyc", "*.pyo", "*.pyd", "*.uid", "*.import", "*.tmp", "*.temp", "*.bak",
    "*.old", "*.orig", "*.swp", "*.swo", "*~", "*.zip", "*.7z", "*.rar", ".DS_Store",
    "Thumbs.db", "Desktop.ini", "*.coverage", "*.dmp", "*.stackdump"
}

class CandidateAuditError(RuntimeError):
    pass


def _sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _seal(record: dict[str, Any]) -> dict[str, Any]:
    result = dict(record)
    result.pop("seal_sha256", None)
    result["seal_sha256"] = _sha_bytes(_canonical_json(result))
    return result


def _hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise CandidateAuditError(f"Cannot read JSON {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise CandidateAuditError(f"Expected JSON object at {path}")
    return data


def _inspect_operator_evidence_waiver(root: Path, manifest_sha256: str) -> dict[str, Any]:
    """Validate the narrow D9.15 capture waiver without marking operational acceptance closed."""
    path = root / D9_15_OPERATOR_EVIDENCE_WAIVER_REL
    result: dict[str, Any] = {"valid": False, "status": "MISSING", "path": D9_15_OPERATOR_EVIDENCE_WAIVER_REL, "sha256": None, "error": None}
    if not path.is_file():
        return result
    try:
        waiver = _load_json(path)
        unsigned = dict(waiver)
        supplied_seal = unsigned.pop("waiver_sha256", None)
        if not isinstance(supplied_seal, str) or _sha_bytes(_canonical_json(unsigned)) != supplied_seal:
            raise CandidateAuditError("D9.15 operator waiver seal mismatch")
        expected = {
            "schema": "C11-D-D9.15-OPERATOR-EVIDENCE-WAIVER-CHECKPOINT-V1",
            "schema_version": "1.0",
            "checkpoint_id": "D9.15_OPERATOR_EVIDENCE_WAIVER_20261009",
            "decision": "WAIVED_FOR_CANDIDATE_EVALUATION_ONLY",
            "decision_date": "2026-10-09",
            "decision_source": "Explicit operator instruction in this work session",
            "operator_assertion": "The operator states that the five GUIs work and directs proceeding without collecting the 13 screenshot/log evidence pairings.",
            "candidate_id": "C11-D-BASELINE-CANDIDATE-0.1",
            "historical_c11c_manifest_sha256": manifest_sha256,
            "required_pairings": 13,
            "captured_pairings": 0,
            "evidence_capture_status": "NOT_CAPTURED_BY_OPERATOR_DECISION",
            "d9_15_acceptance_status": "NOT_CLOSED_BY_THIS_WAIVER",
            "d9_15_pass_claimed": False,
            "candidate_blocker_waived": "D9_15_OPERATOR_EVIDENCE_MATRIX_REQUIRED",
            "waiver_scope": "Remove only the D9.15 operator-evidence-capture blocker from C11-D baseline-candidate readiness evaluation. This waiver does not attest that screenshots/logs were captured and does not mark D9.15 PASS/CLOSED.",
            "does_not_authorize": ["D4.8", "renderer_activation", "production_execution", "D9.14 real-media acceptance", "D9.16 full acceptance", "D9.17 closure", "D baseline freeze", "release authority"],
            "governance": {"renderer_activation": False, "production_execution": False, "media_created": False, "d4_8": "BLOCKED", "release_authority": "NONE", "candidate_freeze_eligible": False},
        }
        for key, value in expected.items():
            if waiver.get(key) != value:
                raise CandidateAuditError(f"D9.15 operator waiver field mismatch: {key}")
        result.update({"valid": True, "status": "VALID_WAIVER", "sha256": _hash_file(path)})
        return result
    except Exception as exc:
        result.update({"status": "INVALID", "error": str(exc)})
        return result


def _parse_assignment(path: Path, name: str) -> Any:
    tree = ast.parse(path.read_text(encoding="utf-8-sig"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return ast.literal_eval(node.value)
    raise CandidateAuditError(f"Cannot resolve {name} from {path}")


def _iter_candidate_files(root: Path):
    for current, dirs, files in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        rel_dir = current_path.relative_to(root).as_posix()
        dirs[:] = sorted(d for d in dirs if d not in TRANSIENT_DIRS and not (rel_dir == "." and d.startswith(".candidate-tmp")))
        for name in sorted(files):
            rel = (current_path / name).relative_to(root).as_posix()
            if any(rel.startswith(prefix) for prefix in EXCLUDED_PREFIXES):
                continue
            if any(fnmatch.fnmatchcase(name, pattern) for pattern in EXCLUDED_PATTERNS):
                continue
            path = current_path / name
            if path.is_file() and not path.is_symlink():
                yield rel, path


def _candidate_tree_fingerprint(root: Path, *, exclude_paths: set[str] | None = None) -> tuple[int, str]:
    """Fingerprint candidate files; a governance approval record may exclude itself from its binding."""
    excluded = {p.replace("\\", "/") for p in (exclude_paths or set())}
    rows: list[str] = []
    for rel, path in _iter_candidate_files(root):
        if rel in excluded:
            continue
        data_hash = _hash_file(path)
        rows.append(f"{rel}\0{path.stat().st_size}\0{data_hash}\n")
    payload = "".join(sorted(rows)).encode("utf-8")
    return len(rows), _sha_bytes(payload)


def _protected_path(rel: str) -> bool:
    return rel in PROTECTED_EXACT or any(rel.startswith(prefix) for prefix in PROTECTED_PREFIXES)


def _within_allowed_d_roots(rel: str) -> bool:
    return any(rel.startswith(prefix) for prefix in ALLOWED_D_CHANGE_ROOTS)


def _collect_c_manifest_audit(root: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    entries = manifest.get("source_files")
    if not isinstance(entries, list) or len(entries) != 2545 or manifest.get("source_file_count") != 2545:
        raise CandidateAuditError("C11-C historical source manifest count/shape differs from frozen reference")
    missing: list[str] = []
    changed: list[str] = []
    protected_total = 0
    protected_changed: list[str] = []
    unapproved_drift: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            raise CandidateAuditError("Malformed C11-C source manifest entry")
        rel = entry["path"]
        path = root / rel
        if not path.is_file():
            missing.append(rel)
            continue
        stat = path.stat()
        digest = _hash_file(path)
        matches = stat.st_size == entry.get("bytes") and digest == entry.get("sha256")
        protected = _protected_path(rel)
        if protected:
            protected_total += 1
            if not matches:
                protected_changed.append(rel)
        if not matches:
            changed.append(rel)
            if not _within_allowed_d_roots(rel):
                unapproved_drift.append(rel)
    missing_legacy = [rel for rel in missing if rel.startswith(LEGACY_CONTROL_PREFIX)]
    missing_nonlegacy = [rel for rel in missing if not rel.startswith(LEGACY_CONTROL_PREFIX)]
    return {
        "c_manifest_entries": len(entries),
        "c_manifest_missing_entries": missing,
        "c_manifest_missing_legacy_entries": missing_legacy,
        "c_manifest_missing_nonlegacy_entries": missing_nonlegacy,
        "c_manifest_source_present_entries": len(entries) - len(missing),
        "c_manifest_exact_matches": len(entries) - len(changed) - len(missing),
        "c_manifest_changed_entries": changed,
        "c_manifest_changed_entries_confined_to_d_roots": len(unapproved_drift) == 0,
        "c_manifest_unapproved_drift": unapproved_drift,
        "protected_c_entries": protected_total,
        "protected_c_changed_entries": protected_changed,
    }


def _load_maintenance_module(root: Path):
    module_path = root / "tools/c11d/d9/maintenance.py"
    if not module_path.is_file():
        raise CandidateAuditError("Canonical D9.11 maintenance backend missing; quarantine cannot be reconciled")
    spec = importlib.util.spec_from_file_location("c11d_candidate_maintenance_backend", module_path)
    if spec is None or spec.loader is None:
        raise CandidateAuditError("Cannot load canonical D9.11 maintenance backend")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _legacy_control_disposition(root: Path, manifest: dict[str, Any], manifest_sha256: str) -> dict[str, Any]:
    """Read-only reconciliation of legacy paths with D9.11 ledger and exact file hashes."""
    legacy_entries = [
        row for row in manifest.get("source_files", [])
        if isinstance(row, dict) and isinstance(row.get("path"), str)
        and row["path"].replace("\\", "/").startswith(LEGACY_CONTROL_PREFIX)
    ]
    source = root / LEGACY_CONTROL_DIR
    expected_by_suffix = {
        row["path"].replace("\\", "/")[len(LEGACY_CONTROL_PREFIX):]: row
        for row in legacy_entries
    }
    result: dict[str, Any] = {
        "source_path": LEGACY_CONTROL_DIR,
        "source_present": source.is_dir(),
        "manifest_reference_count": len(legacy_entries),
        "missing_source_reference_count": sum(not (root / row["path"].replace("\\", "/")).is_file() for row in legacy_entries),
        "ledger_path": MAINTENANCE_LEDGER_REL,
        "ledger_event": None,
        "destination_path": None,
        "tree_hash_verified": False,
        "manifest_hash_verified": False,
        "entry_hashes_reconciled": False,
        "reconciled": False,
        "status": "SOURCE_PRESENT_REVIEW_REQUIRED" if source.is_dir() else "SOURCE_MISSING_UNTRACKED",
        "entry_reconciliation": [
            {
                "manifest_path": f"{LEGACY_CONTROL_PREFIX}{suffix}",
                "expected_bytes": expected.get("bytes"),
                "expected_sha256": expected.get("sha256"),
                "ledger_bytes": None,
                "ledger_sha256": None,
                "archive_bytes": None,
                "archive_sha256": None,
                "matches": False,
                "reasons": ["SOURCE_OR_LEDGER_RECONCILIATION_NOT_YET_ESTABLISHED"],
            }
            for suffix, expected in sorted(expected_by_suffix.items())
        ],
    }
    if source.exists():
        result["entry_reconciliation_status"] = "SOURCE_PRESENT_REVIEW_REQUIRED"
        return result
    ledger_path = root / MAINTENANCE_LEDGER_REL
    if not ledger_path.is_file():
        result["entry_reconciliation_status"] = "LEDGER_MISSING"
        return result
    try:
        maintenance = _load_maintenance_module(root)
        ledger = maintenance.load_ledger(root)
        event = maintenance.latest_lifecycle_event(ledger)
    except Exception as exc:
        result["status"] = "LEDGER_INVALID_REVIEW_REQUIRED"
        result["ledger_error"] = str(exc)
        result["entry_reconciliation_status"] = "LEDGER_INVALID"
        return result
    if not isinstance(event, dict):
        result["entry_reconciliation_status"] = "NO_LIFECYCLE_EVENT"
        return result
    result["ledger_event"] = event.get("event_type")
    result["destination_path"] = event.get("destination_path")
    if event.get("event_type") != "QUARANTINED":
        result["status"] = "NOT_QUARANTINED_LATEST_EVENT"
        result["entry_reconciliation_status"] = "LATEST_EVENT_NOT_QUARANTINED"
        return result
    destination_rel = event.get("destination_path")
    if not isinstance(destination_rel, str) or not destination_rel.startswith(QUARANTINE_DESTINATION_PREFIX):
        result["status"] = "QUARANTINE_DESTINATION_NOT_ALLOWLISTED"
        result["entry_reconciliation_status"] = "DESTINATION_NOT_ALLOWLISTED"
        return result
    if event.get("historical_manifest_sha256") != manifest_sha256:
        result["status"] = "QUARANTINE_MANIFEST_HASH_MISMATCH"
        result["entry_reconciliation_status"] = "MANIFEST_HASH_MISMATCH"
        return result
    result["manifest_hash_verified"] = True
    try:
        destination = maintenance.relative_path(root, destination_rel)
        actual = maintenance.inventory_tree(destination)
    except Exception as exc:
        result["status"] = "QUARANTINE_DESTINATION_UNVERIFIABLE"
        result["verification_error"] = str(exc)
        result["entry_reconciliation_status"] = "DESTINATION_UNVERIFIABLE"
        return result
    if actual.get("tree_sha256") != event.get("tree_sha256"):
        result["status"] = "QUARANTINE_TREE_HASH_MISMATCH"
        result["entry_reconciliation_status"] = "TREE_HASH_MISMATCH"
        return result
    result["tree_hash_verified"] = True
    event_files = event.get("files")
    actual_files = actual.get("files")
    if not isinstance(event_files, list) or not isinstance(actual_files, list):
        result["status"] = "QUARANTINE_FILE_INVENTORY_MISSING"
        result["entry_reconciliation_status"] = "FILE_INVENTORY_MISSING"
        return result
    event_by_suffix = {row.get("path"): row for row in event_files if isinstance(row, dict)}
    actual_by_suffix = {row.get("path"): row for row in actual_files if isinstance(row, dict)}
    diagnostics: list[dict[str, Any]] = []
    all_match = True
    for suffix, expected in sorted(expected_by_suffix.items()):
        ledger_row = event_by_suffix.get(suffix)
        archive_row = actual_by_suffix.get(suffix)
        reasons: list[str] = []
        if not isinstance(ledger_row, dict):
            reasons.append("LEDGER_ENTRY_MISSING")
        else:
            if ledger_row.get("bytes") != expected.get("bytes"):
                reasons.append("LEDGER_SIZE_DIFFERS_FROM_HISTORICAL_MANIFEST")
            if ledger_row.get("sha256") != expected.get("sha256"):
                reasons.append("LEDGER_HASH_DIFFERS_FROM_HISTORICAL_MANIFEST")
        if not isinstance(archive_row, dict):
            reasons.append("ARCHIVE_ENTRY_MISSING")
        else:
            if archive_row.get("bytes") != expected.get("bytes"):
                reasons.append("ARCHIVE_SIZE_DIFFERS_FROM_HISTORICAL_MANIFEST")
            if archive_row.get("sha256") != expected.get("sha256"):
                reasons.append("ARCHIVE_HASH_DIFFERS_FROM_HISTORICAL_MANIFEST")
        matches = not reasons
        all_match = all_match and matches
        diagnostics.append({
            "manifest_path": f"{LEGACY_CONTROL_PREFIX}{suffix}",
            "expected_bytes": expected.get("bytes"),
            "expected_sha256": expected.get("sha256"),
            "ledger_bytes": ledger_row.get("bytes") if isinstance(ledger_row, dict) else None,
            "ledger_sha256": ledger_row.get("sha256") if isinstance(ledger_row, dict) else None,
            "archive_bytes": archive_row.get("bytes") if isinstance(archive_row, dict) else None,
            "archive_sha256": archive_row.get("sha256") if isinstance(archive_row, dict) else None,
            "matches": matches,
            "reasons": reasons,
        })
    exact_cardinality = len(event_by_suffix) == len(expected_by_suffix) == len(actual_by_suffix)
    result["entry_reconciliation"] = diagnostics
    result["entry_hashes_reconciled"] = all_match and exact_cardinality
    result["entry_reconciliation_status"] = "MATCHED" if result["entry_hashes_reconciled"] else "MISMATCH"
    if result["entry_hashes_reconciled"]:
        result["reconciled"] = True
        result["status"] = "QUARANTINED_LEDGER_RECONCILED"
    else:
        result["status"] = "QUARANTINED_MANIFEST_ENTRY_MISMATCH"
    return result


def _governance_and_closure(root: Path, legacy_disposition: dict[str, Any], *, candidate_source_sha256: str, manifest_sha256: str) -> tuple[list[str], dict[str, Any]]:
    blockers: list[str] = []
    d14 = _load_json(root / "definitions/c11d/d9/D9_14_GUI_REAL_MEDIA_CERTIFICATION_GATE_V1.json")
    d15 = _load_json(root / "definitions/c11d/d9/D9_15_GUI_OPERATIONAL_ACCEPTANCE_V1.json")
    d16 = _load_json(root / "definitions/c11d/d9/D9_16_FULL_ACCEPTANCE_V1.json")
    activation = _load_json(root / "definitions/c11d/production/C11D_PRODUCTION_ACTIVATION_POLICY_V1.json")
    d17_path = root / "docs/current/d/D9.17_D9_CLOSURE_ADJUDICATION_CHECKPOINT.md"
    if not d17_path.is_file():
        raise CandidateAuditError("D9.17 closure adjudication checkpoint is missing")
    d17_text = d17_path.read_text(encoding="utf-8-sig")

    d14gov = d14.get("governance", {})
    d15gov = d15.get("governance", {})
    d16gov = d16.get("governance", {})
    if "BLOCKED" in str(d14.get("status", "")) or d14gov.get("d4_8") == "BLOCKED":
        blockers.append("D9_14_REAL_MEDIA_CERTIFICATION_BLOCKED")
    waiver = _inspect_operator_evidence_waiver(root, manifest_sha256)
    waiver_valid = bool(waiver.get("valid"))
    if d15.get("status") != "PASS_CLOSED" and d15gov.get("media_created") is False and not waiver_valid:
        blockers.append("D9_15_OPERATOR_EVIDENCE_MATRIX_REQUIRED")
    d9_15_candidate_evidence_status = (
        "D9.15_OPERATOR_EVIDENCE_PASS_CLOSED" if d15.get("status") == "PASS_CLOSED"
        else "WAIVED_NOT_EVIDENCED_FOR_CANDIDATE_ONLY" if waiver_valid
        else "OPERATOR_EVIDENCE_REQUIRED"
    )
    if d16.get("full_acceptance_blockers") or "BLOCKED" in str(d16.get("status", "")):
        blockers.append("D9_16_FULL_ACCEPTANCE_NOT_CLOSED")
    if "Decision: BLOCKED / NO-GO" in d17_text and "D9 remains OPEN" in d17_text:
        blockers.append("D9_17_CLOSURE_NO_GO")
    renderer_checkpoint_path = root / D_RENDERER_BASELINE_APPROVAL_REL
    renderer_checkpoint_sha256 = None
    renderer_checkpoint_status = "MISSING"
    if not renderer_checkpoint_path.is_file():
        blockers.append("D_RENDERER_BASELINE_APPROVAL_NOT_RECORDED")
    else:
        renderer_text = renderer_checkpoint_path.read_text(encoding="utf-8-sig")
        if "Decision: APPROVED" not in renderer_text or "D4.8=AUTHORIZED" not in renderer_text:
            blockers.append("D_RENDERER_BASELINE_APPROVAL_NOT_APPROVED")
            renderer_checkpoint_status = "PRESENT_NOT_APPROVED"
        else:
            renderer_checkpoint_sha256 = _hash_file(renderer_checkpoint_path)
            renderer_checkpoint_status = "APPROVED_CHECKPOINT_PRESENT"
    baseline_approval_path = root / D_BASELINE_APPROVAL_REL
    baseline_approval_status = "MISSING"
    baseline_approval_valid = False
    if not baseline_approval_path.is_file():
        blockers.append("D_BASELINE_APPROVAL_NOT_RECORDED")
    else:
        try:
            approval = _load_json(baseline_approval_path)
            approval_matches = (
                approval.get("schema") == "C11-D-BASELINE-APPROVAL-CHECKPOINT-V1"
                and approval.get("schema_version") == "1.0"
                and approval.get("candidate_id") == "C11-D-BASELINE-CANDIDATE-0.1"
                and approval.get("decision") == "APPROVED"
                and approval.get("candidate_source_sha256") == candidate_source_sha256
                and approval.get("historical_c11c_manifest_sha256") == manifest_sha256
                and approval.get("renderer_baseline_checkpoint_sha256") == renderer_checkpoint_sha256
                and bool(str(approval.get("approved_by", "")).strip())
                and bool(str(approval.get("approved_at_utc", "")).strip())
                and renderer_checkpoint_status == "APPROVED_CHECKPOINT_PRESENT"
            )
            if approval_matches:
                baseline_approval_valid = True
                baseline_approval_status = "APPROVED_CHECKPOINT_MATCHES_CURRENT_CANDIDATE"
            else:
                baseline_approval_status = "PRESENT_INVALID_OR_STALE"
                blockers.append("D_BASELINE_APPROVAL_NOT_RECORDED")
        except Exception as exc:
            baseline_approval_status = "PRESENT_INVALID_OR_STALE"
            blockers.append("D_BASELINE_APPROVAL_NOT_RECORDED")
    if not legacy_disposition.get("reconciled"):
        blockers.append("LEGACY_C11D_CONTROL_QUARANTINE_REVIEW_REQUIRED")
    if not legacy_disposition.get("reconciled") and legacy_disposition.get("missing_source_reference_count", 0) > 0:
        blockers.append("C11C_MANIFEST_LEGACY_ENTRIES_PENDING_DISPOSITION")
    # Deliberately do not treat a local file as authority. The canonical activation policy remains the only source here.
    governance_safe = (
        d14gov.get("d4_8") == "BLOCKED"
        and d14gov.get("renderer_activation") is False
        and d14gov.get("production_execution") is False
        and d14gov.get("release_authority") == "NONE"
        and d15gov.get("renderer_activation") is False
        and d15gov.get("media_created") is False
        and d15gov.get("release_authority") == "NONE"
        and d16gov.get("renderer_activation") is False
        and d16gov.get("media_created") is False
        and d16gov.get("d4_8") == "BLOCKED"
        and d16gov.get("release_authority") == "NONE"
        and activation.get("runtime_authority") == "NONE"
        and activation.get("renderer_activation_policy", {}).get("state") == "DISABLED"
        and activation.get("execution", {}).get("production_execution") is False
        and activation.get("execution", {}).get("runtime_authority") == "NONE"
    )
    if not governance_safe:
        raise CandidateAuditError("D governance invariant drift detected; candidate preflight refuses to continue")
    return blockers, {
        "d9_14_status": d14.get("status"),
        "d9_15_status": d15.get("status"),
        "d9_15_candidate_evidence_gate_status": d9_15_candidate_evidence_status,
        "d9_15_operator_evidence_pass_closed": d15.get("status") == "PASS_CLOSED",
        "d9_15_operator_evidence_waiver_valid": waiver_valid,
        "d9_15_operator_evidence_waiver_status": waiver.get("status", "MISSING"),
        "d9_15_operator_evidence_waiver_sha256": waiver.get("sha256"),
        "d9_15_operator_evidence_waiver_error": waiver.get("error"),
        "d9_16_status": d16.get("status"),
        "d9_16_full_acceptance_blocker_count": len(d16.get("full_acceptance_blockers", [])),
        "d9_17_closure_status": "BLOCKED_NO_GO" if "D9_17_CLOSURE_NO_GO" in blockers else "REVIEW_REQUIRED",
        "d4_8": "BLOCKED",
        "renderer_activation": False,
        "production_execution": False,
        "media_created": False,
        "release_authority": "NONE",
        "renderer_baseline_checkpoint_status": renderer_checkpoint_status,
        "renderer_baseline_checkpoint_sha256": renderer_checkpoint_sha256,
        "baseline_approval_checkpoint_status": baseline_approval_status,
        "baseline_approval_checkpoint_valid": baseline_approval_valid,
        "candidate_source_sha256_excluding_approval_checkpoint": candidate_source_sha256,
        "legacy_c11d_control_disposition": legacy_disposition,
    }


def build_candidate_preflight(project_root: Path) -> dict[str, Any]:
    root = project_root.resolve()
    if not (root / POLICY_REL).is_file():
        raise CandidateAuditError(f"Candidate policy missing: {POLICY_REL}")
    policy = _load_json(root / POLICY_REL)
    manifest_path = root / C_MANIFEST_REL
    if not manifest_path.is_file():
        raise CandidateAuditError("Immutable C11-C freeze manifest is missing")
    manifest_bytes = manifest_path.read_bytes()
    actual_manifest_sha = _sha_bytes(manifest_bytes)
    if actual_manifest_sha != EXPECTED_C_MANIFEST_SHA256:
        raise CandidateAuditError("Historical C11-C manifest hash changed; candidate audit stopped")
    manifest = json.loads(manifest_bytes.decode("utf-8-sig"))
    inventory = _collect_c_manifest_audit(root, manifest)
    if inventory["c_manifest_missing_nonlegacy_entries"]:
        raise CandidateAuditError(f"C11-C historical source paths missing outside the explicit legacy c11d-control disposition path: {inventory['c_manifest_missing_nonlegacy_entries'][:10]}")
    legacy_disposition = _legacy_control_disposition(root, manifest, actual_manifest_sha)
    inventory["legacy_c11d_control_disposition"] = legacy_disposition
    inventory["c_manifest_reconciled_legacy_entries"] = (
        len(inventory["c_manifest_missing_legacy_entries"]) if legacy_disposition.get("reconciled") else 0
    )
    inventory["c_manifest_unreconciled_legacy_entries"] = (
        0 if legacy_disposition.get("reconciled") else len(inventory["c_manifest_missing_legacy_entries"])
    )
    if inventory["protected_c_changed_entries"]:
        raise CandidateAuditError(f"Protected C11-C source drift detected: {inventory['protected_c_changed_entries'][:10]}")
    if not inventory["c_manifest_changed_entries_confined_to_d_roots"]:
        raise CandidateAuditError(f"C11-C source changes outside D extension roots: {inventory['c_manifest_unapproved_drift'][:10]}")

    shell_apps = _parse_assignment(root / "c11c-suite/main.py", "APPS")
    surfaces = [row[1] for row in shell_apps]
    if len(surfaces) != 5 or set(surfaces) != EXPECTED_SURFACES:
        raise CandidateAuditError(f"Canonical operational topology drift: count={len(surfaces)}, rows={surfaces}")
    _, candidate_source_sha256 = _candidate_tree_fingerprint(root, exclude_paths={D_BASELINE_APPROVAL_REL})
    blockers, governance = _governance_and_closure(
        root, legacy_disposition,
        candidate_source_sha256=candidate_source_sha256,
        manifest_sha256=actual_manifest_sha,
    )
    source_file_count, tree_sha256 = _candidate_tree_fingerprint(root)

    checks = [
        {"id": "C11C_MANIFEST_IDENTITY", "passed": True, "detail": f"sha256={actual_manifest_sha}"},
        {"id": "C11C_SOURCE_INVENTORY_BOUNDARY_VALID", "passed": not inventory["c_manifest_missing_nonlegacy_entries"], "detail": f"manifest_entries={inventory['c_manifest_entries']}; source_present={inventory['c_manifest_source_present_entries']}; legacy_reconciled={inventory['c_manifest_reconciled_legacy_entries']}; legacy_unresolved={inventory['c_manifest_unreconciled_legacy_entries']}; nonlegacy_missing={len(inventory['c_manifest_missing_nonlegacy_entries'])}"},
        {"id": "C11C_PROTECTED_SOURCE_IMMUTABLE", "passed": True, "detail": f"{inventory['protected_c_entries']}/{inventory['protected_c_entries']} protected entries match historical hashes"},
        {"id": "D_EXTENSIONS_CONFINED", "passed": True, "detail": f"{len(inventory['c_manifest_changed_entries'])} manifest-listed paths changed only inside approved D extension roots"},
        {"id": "FIVE_SURFACES_CANONICAL", "passed": True, "detail": "exactly five active GUI surfaces"},
        {"id": "GOVERNANCE_FAIL_CLOSED", "passed": True, "detail": "D4.8 blocked, renderer/media off, release authority NONE"},
        {"id": "D_BASELINE_APPROVAL_SEPARATE_CHECKPOINT", "passed": True, "detail": governance["baseline_approval_checkpoint_status"]},
        {"id": "CANDIDATE_ADJUDICATION_CONSISTENT", "passed": True, "detail": "the preflight cannot close D9 or authorize production"},
    ]
    record = {
        "schema": "C11-D-BASELINE-CANDIDATE-PREFLIGHT-V1",
        "schema_version": "1.0",
        "candidate_id": policy["candidate_id"],
        "decision": "PREFLIGHT_PASS_CANDIDATE_FREEZE_BLOCKED_AS_REQUIRED",
        "candidate_freeze_eligible": False,
        "candidate_release_authority": "NONE",
        "immutable_reference": {
            "release": "C11-C 2.19.12",
            "manifest_path": C_MANIFEST_REL,
            "manifest_sha256": actual_manifest_sha,
            "disposition": "IMMUTABLE_REFERENCE_ONLY",
        },
        "inventory": inventory,
        "tree_identity": {"included_files": source_file_count, "sha256": tree_sha256},
        "canonical_surfaces": {"count": len(surfaces), "paths": sorted(surfaces)},
        "governance": governance,
        "checks": checks,
        "check_count": len(checks),
        "blockers": sorted(set(blockers)),
        "side_effects": {"repository_files_written": False, "freeze_archive_created": False, "media_created": False, "renderer_activation": False, "manifest_modified": False, "release_authority_granted": False},
    }
    return _seal(record)


def _validate_candidate_record_invariants(record: dict[str, Any]) -> None:
    """Reject internally inconsistent records before the expensive authoritative tree re-audit."""
    if record.get("schema") != "C11-D-BASELINE-CANDIDATE-PREFLIGHT-V1" or record.get("schema_version") != "1.0":
        raise CandidateAuditError("Candidate preflight schema mismatch")
    if record.get("candidate_id") != "C11-D-BASELINE-CANDIDATE-0.1":
        raise CandidateAuditError("Unknown D baseline candidate identity")
    if record.get("decision") != "PREFLIGHT_PASS_CANDIDATE_FREEZE_BLOCKED_AS_REQUIRED":
        raise CandidateAuditError("Candidate decision promotion is forbidden")
    if record.get("candidate_freeze_eligible") is not False or record.get("candidate_release_authority") != "NONE":
        raise CandidateAuditError("Candidate promotion/authority is forbidden by this preflight")
    reference = record.get("immutable_reference", {})
    if reference.get("release") != "C11-C 2.19.12" or reference.get("manifest_sha256") != EXPECTED_C_MANIFEST_SHA256:
        raise CandidateAuditError("Immutable C11-C historical reference identity mismatch")
    inv = record.get("inventory", {})
    if inv.get("c_manifest_entries") != 2545:
        raise CandidateAuditError("C11-C source manifest entry count changed")
    missing = inv.get("c_manifest_missing_entries", [])
    missing_legacy = inv.get("c_manifest_missing_legacy_entries", [])
    missing_nonlegacy = inv.get("c_manifest_missing_nonlegacy_entries", [])
    if not isinstance(missing, list) or not isinstance(missing_legacy, list) or not isinstance(missing_nonlegacy, list):
        raise CandidateAuditError("C11-C missing-entry inventory is malformed")
    if set(missing) != set(missing_legacy) | set(missing_nonlegacy) or set(missing_legacy) != {p for p in missing if isinstance(p, str) and p.startswith(LEGACY_CONTROL_PREFIX)}:
        raise CandidateAuditError("Missing-entry classification does not match the legacy allowlist")
    if missing_nonlegacy:
        raise CandidateAuditError("A non-legacy C11-C manifest path is missing")
    if inv.get("c_manifest_source_present_entries") != 2545 - len(missing):
        raise CandidateAuditError("C11-C source-presence count is inconsistent")
    if inv.get("c_manifest_exact_matches") != 2545 - len(inv.get("c_manifest_changed_entries", [])) - len(missing):
        raise CandidateAuditError("C11-C exact-match count is inconsistent")
    if inv.get("protected_c_entries", 0) < 800 or inv.get("protected_c_changed_entries"):
        raise CandidateAuditError("Protected C11-C entries are missing or changed")
    if inv.get("c_manifest_changed_entries_confined_to_d_roots") is not True or inv.get("c_manifest_unapproved_drift"):
        raise CandidateAuditError("C-manifest drift is not confined to approved D extension roots")
    disp = inv.get("legacy_c11d_control_disposition", {})
    reconciled = disp.get("reconciled") is True
    if reconciled:
        if disp.get("status") != "QUARANTINED_LEDGER_RECONCILED" or not (disp.get("tree_hash_verified") and disp.get("manifest_hash_verified") and disp.get("entry_hashes_reconciled")):
            raise CandidateAuditError("Legacy quarantine claims reconciliation without complete hash evidence")
        if inv.get("c_manifest_reconciled_legacy_entries") != len(missing_legacy) or inv.get("c_manifest_unreconciled_legacy_entries") != 0:
            raise CandidateAuditError("Legacy reconciliation counts are inconsistent")
    else:
        if "LEGACY_C11D_CONTROL_QUARANTINE_REVIEW_REQUIRED" not in record.get("blockers", []):
            raise CandidateAuditError("Unreconciled legacy c11d-control must remain an explicit blocker")
        if inv.get("c_manifest_unreconciled_legacy_entries") != len(missing_legacy):
            raise CandidateAuditError("Unreconciled legacy entry count is inconsistent")
        if disp.get("missing_source_reference_count", 0) > 0 and "C11C_MANIFEST_LEGACY_ENTRIES_PENDING_DISPOSITION" not in record.get("blockers", []):
            raise CandidateAuditError("Missing legacy manifest references without ledger must remain an explicit blocker")
    surfaces = record.get("canonical_surfaces", {})
    if surfaces.get("count") != 5 or set(surfaces.get("paths", [])) != EXPECTED_SURFACES:
        raise CandidateAuditError("Canonical operational topology is not exactly five surfaces")
    governance = record.get("governance", {})
    if governance.get("d4_8") != "BLOCKED" or governance.get("renderer_activation") is not False or governance.get("production_execution") is not False or governance.get("media_created") is not False or governance.get("release_authority") != "NONE":
        raise CandidateAuditError("Governance fail-closed invariants changed")
    required = {
        "D9_14_REAL_MEDIA_CERTIFICATION_BLOCKED",
        "D9_16_FULL_ACCEPTANCE_NOT_CLOSED",
        "D9_17_CLOSURE_NO_GO",
        "D_RENDERER_BASELINE_APPROVAL_NOT_RECORDED",
        "D_BASELINE_APPROVAL_NOT_RECORDED",
    }
    blockers = set(record.get("blockers", []))
    if not required.issubset(blockers):
        raise CandidateAuditError("Candidate lost one or more mandatory freeze blockers")
    governance = record.get("governance", {})
    d915_blocker = "D9_15_OPERATOR_EVIDENCE_MATRIX_REQUIRED" in blockers
    waiver_valid = governance.get("d9_15_operator_evidence_waiver_valid") is True
    if waiver_valid:
        if d915_blocker or governance.get("d9_15_operator_evidence_waiver_status") != "VALID_WAIVER":
            raise CandidateAuditError("Validated D9.15 waiver must remove only the candidate evidence-capture blocker")
        if governance.get("d9_15_candidate_evidence_gate_status") != "WAIVED_NOT_EVIDENCED_FOR_CANDIDATE_ONLY" or governance.get("d9_15_operator_evidence_pass_closed") is not False:
            raise CandidateAuditError("D9.15 candidate waiver cannot claim operational PASS/CLOSED")
    elif not d915_blocker:
        raise CandidateAuditError("D9.15 evidence blocker is absent without an accepted checkpoint or valid waiver")
    effects = record.get("side_effects", {})
    if effects != {"repository_files_written": False, "freeze_archive_created": False, "media_created": False, "renderer_activation": False, "manifest_modified": False, "release_authority_granted": False}:
        raise CandidateAuditError("Candidate preflight declared a forbidden side effect")
    tree = record.get("tree_identity", {})
    if not isinstance(tree.get("sha256"), str) or len(tree["sha256"]) != 64 or any(c not in "0123456789abcdef" for c in tree["sha256"]):
        raise CandidateAuditError("Candidate tree identity fingerprint is malformed")
    checks = record.get("checks", [])
    expected_ids = {"C11C_MANIFEST_IDENTITY", "C11C_SOURCE_INVENTORY_BOUNDARY_VALID", "C11C_PROTECTED_SOURCE_IMMUTABLE", "D_EXTENSIONS_CONFINED", "FIVE_SURFACES_CANONICAL", "GOVERNANCE_FAIL_CLOSED", "D_BASELINE_APPROVAL_SEPARATE_CHECKPOINT", "CANDIDATE_ADJUDICATION_CONSISTENT"}
    if record.get("check_count") != 8 or {c.get("id") for c in checks if isinstance(c, dict)} != expected_ids or any(c.get("passed") is not True for c in checks if isinstance(c, dict)):
        raise CandidateAuditError("Candidate preflight check ledger is malformed or contains failed checks")


def validate_candidate_preflight(record: dict[str, Any], project_root: Path) -> dict[str, Any]:
    supplied_seal = record.get("seal_sha256")
    unsigned = dict(record)
    unsigned.pop("seal_sha256", None)
    if not isinstance(supplied_seal, str) or _sha_bytes(_canonical_json(unsigned)) != supplied_seal:
        raise CandidateAuditError("Candidate preflight seal mismatch")
    _validate_candidate_record_invariants(record)
    actual = build_candidate_preflight(project_root)
    if record != actual:
        raise CandidateAuditError("Candidate preflight differs from the authoritative current-tree evaluation")
    if not record.get("blockers"):
        raise CandidateAuditError("Candidate cannot be freeze-eligible while required blockers remain unresolved")
    return {"valid": True, "freeze_eligible": False, "blockers": len(record["blockers"])}
