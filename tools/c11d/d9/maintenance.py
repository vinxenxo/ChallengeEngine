from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
POLICY_REL = Path("definitions/c11d/d9/D9_11_MAINTENANCE_POLICY_V1.json")
MATRIX_REL = Path("definitions/c11d/d9/D9_SUITE_VERSION_MATRIX_V1.json")
ROADMAP_REL = Path("docs/current/d/C11-D_ROADMAP_V1.0_STATELESS.md")
FREEZE_MANIFEST_REL = Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")
LEDGER_REL = Path("artifacts/maintenance/d9_11/D9_11_MAINTENANCE_LEDGER.json")
QUARANTINE_SOURCE = "c11c-suite/c11d-control"
EXPECTED_APPS = {
    "c11c-test/main.py",
    "c11c-producer/main.py",
    "c11c-catalog/main.py",
    "c11c-config/main.py",
    "c11c-maintenance/main.py",
}
EXPECTED_C11C_ZIP_SHA256 = "D85425CF18C5211C8497574F4FC66202D613EACC0EC14CD4E2FEF0B24F634A32"
EXPECTED_C11C_TREE_SHA256 = "2D39B7B923B42CDC6647A4D25493B75023CDD19CEE18214BBDE1FDD295B8F256"
CONFIRM_QUARANTINE = "QUARANTINE_C11D_CONTROL"
CONFIRM_RESTORE = "RESTORE_C11D_CONTROL"
CONFIRM_CLEANUP = "CLEAN_TRANSIENTS_ONLY"
CONFIRM_RESTORE_CLEANUP = "RESTORE_CLEANUP_ARCHIVE"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def emit(value: Any) -> None:
    payload = json_bytes(value)
    out = getattr(sys.stdout, "buffer", None)
    if out is not None:
        out.write(payload)
        out.flush()
    else:
        sys.stdout.write(payload.decode("utf-8"))
        sys.stdout.flush()


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def stamp_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def relative_path(root: Path, rel: str) -> Path:
    """Resolve an authored relative path without allowing traversal or symlink escapes."""
    if not isinstance(rel, str) or not rel or "\x00" in rel:
        raise ValueError("path must be a non-empty relative string")
    posix = PurePosixPath(rel.replace("\\", "/"))
    if posix.is_absolute() or any(part in {"..", "."} for part in posix.parts) or ":" in rel:
        raise ValueError("absolute paths, dot segments and drive-qualified paths are forbidden")
    base = root.resolve()
    candidate = base.joinpath(*posix.parts)
    try:
        candidate.absolute().relative_to(base)
        candidate.resolve(strict=False).relative_to(base)
    except (ValueError, OSError) as exc:
        raise ValueError("path escapes project root") from exc
    cursor = base
    for part in posix.parts:
        cursor = cursor / part
        if cursor.is_symlink() or bool(getattr(cursor, "is_junction", lambda: False)()):
            raise ValueError(f"symlink/junction path is forbidden: {rel}")
    return candidate


def _canonical_ledger() -> dict[str, Any]:
    return {"schema": "C11-D-D9.11-MAINTENANCE-LEDGER-V1", "schema_version": "1.0", "events": []}


def load_ledger(root: Path) -> dict[str, Any]:
    path = relative_path(root, LEDGER_REL.as_posix())
    if not path.exists():
        return _canonical_ledger()
    if not path.is_file():
        raise ValueError("maintenance ledger path is not a regular file")
    value = read_json(path)
    if not isinstance(value, dict) or value.get("schema") != "C11-D-D9.11-MAINTENANCE-LEDGER-V1" or not isinstance(value.get("events"), list):
        raise ValueError("maintenance ledger schema is invalid; refusing to overwrite or repair it implicitly")
    return value


def write_ledger_atomic(root: Path, ledger: dict[str, Any]) -> None:
    path = relative_path(root, LEDGER_REL.as_posix())
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.parent.is_symlink() or bool(getattr(path.parent, "is_junction", lambda: False)()):
        raise ValueError("maintenance ledger directory cannot be a symlink/junction")
    payload = json_bytes(ledger)
    fd, name = tempfile.mkstemp(prefix=".d9_11_ledger_", suffix=".tmp", dir=str(path.parent))
    temp = Path(name)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, path)
    except Exception:
        try:
            temp.unlink(missing_ok=True)
        except Exception:
            pass
        raise


def append_event(root: Path, event: dict[str, Any]) -> None:
    ledger = load_ledger(root)
    ledger["events"].append(event)
    write_ledger_atomic(root, ledger)


def latest_lifecycle_event(ledger: dict[str, Any], resource: str = QUARANTINE_SOURCE) -> dict[str, Any] | None:
    events = [e for e in ledger.get("events", []) if isinstance(e, dict) and e.get("resource") == resource and e.get("event_type") in {"QUARANTINED", "RESTORED"}]
    return events[-1] if events else None


def inventory_tree(path: Path) -> dict[str, Any]:
    if not path.exists() or not path.is_dir() or path.is_symlink() or bool(getattr(path, "is_junction", lambda: False)()):
        raise ValueError(f"inventory root must be a real existing directory: {path}")
    files: list[dict[str, Any]] = []
    dirs: list[str] = []
    for current, dirnames, filenames in os.walk(path, topdown=True, followlinks=False):
        current_path = Path(current)
        keep_dirs = []
        for name in sorted(dirnames):
            child = current_path / name
            if child.is_symlink() or bool(getattr(child, "is_junction", lambda: False)()):
                raise ValueError(f"symlink/junction inside governed tree: {child.relative_to(path).as_posix()}")
            keep_dirs.append(name)
            dirs.append(child.relative_to(path).as_posix())
        dirnames[:] = keep_dirs
        for name in sorted(filenames):
            child = current_path / name
            if child.is_symlink() or bool(getattr(child, "is_junction", lambda: False)()):
                raise ValueError(f"symlink/junction inside governed tree: {child.relative_to(path).as_posix()}")
            if not child.is_file():
                raise ValueError(f"non-regular filesystem entry inside governed tree: {child.relative_to(path).as_posix()}")
            files.append({"path": child.relative_to(path).as_posix(), "bytes": child.stat().st_size, "sha256": sha256_file(child)})
    dirs.sort()
    files.sort(key=lambda row: row["path"])
    identity = {"directories": dirs, "files": files}
    return {
        "tree_sha256": sha256_bytes(json_bytes(identity)),
        "directory_count": len(dirs),
        "file_count": len(files),
        "bytes": sum(row["bytes"] for row in files),
        "directories": dirs,
        "files": files,
    }


def _manifest_info(root: Path) -> dict[str, Any]:
    path = relative_path(root, FREEZE_MANIFEST_REL.as_posix())
    if not path.is_file():
        return {"status": "MISSING", "path": FREEZE_MANIFEST_REL.as_posix(), "sha256": None, "legacy_control_references": []}
    raw_hash = sha256_file(path)
    data = read_json(path)
    rows = data.get("source_files") if isinstance(data, dict) else None
    if not isinstance(rows, list):
        raise ValueError("C11-C freeze manifest has no source_files list")
    refs = []
    prefix = QUARANTINE_SOURCE + "/"
    for row in rows:
        if isinstance(row, dict) and isinstance(row.get("path"), str):
            rel = row["path"].replace("\\", "/")
            if rel.startswith(prefix):
                refs.append({"path": rel, "bytes": row.get("bytes"), "sha256": row.get("sha256")})
    return {
        "status": "READ_ONLY_HISTORICAL_EVIDENCE",
        "path": FREEZE_MANIFEST_REL.as_posix(),
        "sha256": raw_hash,
        "release": data.get("release"),
        "source_tree_sha256": data.get("source_tree_sha256"),
        "source_file_count": data.get("source_file_count"),
        "legacy_control_references": refs,
        "rewritten": False,
    }


def _registered_apps(root: Path) -> list[dict[str, Any]]:
    path = relative_path(root, "c11c-suite/main.py")
    tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
    value = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "APPS" for t in node.targets):
            value = ast.literal_eval(node.value)
            break
    if not isinstance(value, (list, tuple)):
        raise ValueError("canonical Suite APPS registry not found or is not a literal list")
    rows = []
    for row in value:
        if isinstance(row, (list, tuple)) and len(row) >= 2:
            rows.append({"label": str(row[0]), "entrypoint": str(row[1])})
    return rows


def is_protected_path(relative: str, policy: dict[str, Any]) -> bool:
    """Return true when a repository path falls under a canonical protected root."""
    normalized = relative.replace("\\", "/").strip("/").lower()
    for raw in policy.get("protected_paths", []):
        token = str(raw).replace("\\", "/").lower()
        if token.endswith("/"):
            if normalized.startswith(token.rstrip("/")):
                return True
        elif normalized == token:
            return True
    return False


def is_allowed_quarantine_source(relative: str, policy: dict[str, Any]) -> bool:
    """Only the named legacy surface can be quarantined; no general path mutation API exists."""
    normalized = relative.replace("\\", "/").strip("/")
    return normalized == policy.get("quarantine_policy", {}).get("only_allowed_source") and not is_protected_path(normalized, policy)


def _validate_policy(root: Path) -> dict[str, Any]:
    policy = read_json(relative_path(root, POLICY_REL.as_posix()))
    if not isinstance(policy, dict) or policy.get("schema") != "C11-D-D9.11-MAINTENANCE-POLICY-V1":
        raise ValueError("canonical D9.11 maintenance policy schema mismatch")
    if policy.get("version") != "0.2.0" or policy.get("checkpoint") != "D9.11":
        raise ValueError("maintenance policy version/checkpoint mismatch")
    authority = policy.get("authority", {})
    for name, expected in (("runtime_authority", "NONE"), ("renderer_activation", False), ("production_execution", False), ("release_authority", "NONE"), ("c11c_frozen_reference_mutation", "FORBIDDEN"), ("d4_8", "BLOCKED")):
        if authority.get(name) != expected:
            raise ValueError(f"maintenance authority invariant violated: {name}")
    if policy.get("active_suite_topology") != ["c11c-test", "c11c-producer", "c11c-catalog", "c11c-config", "c11c-maintenance"]:
        raise ValueError("maintenance policy must preserve exactly five canonical Suite surfaces")
    if QUARANTINE_SOURCE != policy.get("quarantine_policy", {}).get("only_allowed_source"):
        raise ValueError("quarantine allowlist mismatch")
    return policy


def _candidate_files(root: Path, policy: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    items: list[dict[str, Any]] = []
    errors: list[str] = []
    for rel in policy.get("safe_transient_roots", []):
        try:
            base = relative_path(root, rel)
        except Exception as exc:
            errors.append(f"cleanup allowlist path blocked ({rel}): {exc}")
            continue
        if not base.exists():
            continue
        if not base.is_dir():
            errors.append(f"cleanup root is not a directory: {rel}")
            continue
        for current, dirnames, filenames in os.walk(base, topdown=True, followlinks=False):
            cp = Path(current)
            safe_dirs = []
            for name in sorted(dirnames):
                child = cp / name
                if child.is_symlink() or bool(getattr(child, "is_junction", lambda: False)()):
                    errors.append(f"symlink/junction blocked under cleanup allowlist: {child.relative_to(root).as_posix()}")
                else:
                    safe_dirs.append(name)
            dirnames[:] = safe_dirs
            for name in sorted(filenames):
                child = cp / name
                if child.is_symlink() or bool(getattr(child, "is_junction", lambda: False)()):
                    errors.append(f"symlink/junction blocked under cleanup allowlist: {child.relative_to(root).as_posix()}")
                    continue
                if not child.is_file():
                    errors.append(f"non-regular file blocked under cleanup allowlist: {child.relative_to(root).as_posix()}")
                    continue
                items.append({"path": child.relative_to(root).as_posix(), "bytes": child.stat().st_size, "sha256": sha256_file(child)})
    items.sort(key=lambda row: row["path"])
    return items, errors


def _latest_cleanup_event(ledger: dict[str, Any]) -> dict[str, Any] | None:
    events = [e for e in ledger.get("events", []) if isinstance(e, dict) and e.get("resource") == "SAFE_TRANSIENT_ALLOWLIST" and e.get("event_type") in {"CLEANUP_ARCHIVED", "CLEANUP_RESTORED"}]
    return events[-1] if events else None


def build_plan(root: Path = ROOT) -> dict[str, Any]:
    root = root.resolve()
    errors: list[str] = []
    warnings: list[str] = []
    policy: dict[str, Any] = {}
    matrix: dict[str, Any] = {}
    manifest: dict[str, Any] = {}
    apps: list[dict[str, Any]] = []
    ledger = _canonical_ledger()
    source = root / QUARANTINE_SOURCE
    source_inventory = None
    try:
        policy = _validate_policy(root)
    except Exception as exc:
        errors.append(f"policy: {exc}")
    try:
        matrix = read_json(relative_path(root, MATRIX_REL.as_posix()))
        if matrix.get("active_suite_topology") != ["c11c-test", "c11c-producer", "c11c-catalog", "c11c-config", "c11c-maintenance"]:
            errors.append("D9 suite version matrix does not list exactly five canonical surfaces")
        governance = matrix.get("governance", {})
        if governance.get("d4_8") != "BLOCKED" or governance.get("release_authority") != "NONE" or governance.get("frozen_c11c_mutation") != "FORBIDDEN":
            errors.append("D9 governance matrix no longer protects D4.8/C11-C/release authority")
    except Exception as exc:
        errors.append(f"version matrix: {exc}")
    try:
        roadmap = relative_path(root, ROADMAP_REL.as_posix()).read_text(encoding="utf-8-sig")
        if EXPECTED_C11C_ZIP_SHA256 not in roadmap or EXPECTED_C11C_TREE_SHA256 not in roadmap:
            errors.append("roadmap no longer records both immutable C11-C 2.19.12 reference hashes")
    except Exception as exc:
        errors.append(f"roadmap: {exc}")
    try:
        apps = _registered_apps(root)
        app_paths = {row["entrypoint"] for row in apps}
        if app_paths != EXPECTED_APPS or len(apps) != 5:
            errors.append(f"shared Suite registry mismatch: {sorted(app_paths)}")
        if any("c11d-control" in row["entrypoint"].lower() for row in apps):
            errors.append("legacy c11d-control is incorrectly registered as an operational surface")
    except Exception as exc:
        errors.append(f"shared Suite registry: {exc}")
    try:
        manifest = _manifest_info(root)
        if manifest.get("status") == "MISSING":
            errors.append("read-only C11-C freeze manifest is missing")
        if not manifest.get("legacy_control_references"):
            warnings.append("historical C11-C manifest contains no c11d-control file references")
        source_tree = manifest.get("source_tree_sha256")
        if source_tree and source_tree.upper() != EXPECTED_C11C_TREE_SHA256:
            warnings.append("working C11-C freeze manifest tree hash differs from immutable 2.19.12 reference; preserve as historical evidence and do not rewrite")
    except Exception as exc:
        errors.append(f"historical freeze manifest: {exc}")
    try:
        ledger = load_ledger(root)
    except Exception as exc:
        errors.append(f"maintenance ledger: {exc}")
    last = latest_lifecycle_event(ledger)
    if source.exists():
        try:
            source_inventory = inventory_tree(source)
        except Exception as exc:
            errors.append(f"legacy surface inventory: {exc}")
        if last and last.get("event_type") == "QUARANTINED":
            warnings.append("source folder is present while ledger says QUARANTINED; manual reconciliation required")
            quarantine_state = "SOURCE_LEDGER_CONFLICT"
        elif last and last.get("event_type") == "RESTORED":
            quarantine_state = "RESTORED_PRESENT_UNREGISTERED"
        else:
            quarantine_state = "READY_TO_QUARANTINE"
    else:
        if last and last.get("event_type") == "QUARANTINED":
            qpath = last.get("destination_path")
            try:
                actual = inventory_tree(relative_path(root, str(qpath)))
                if actual.get("tree_sha256") != last.get("tree_sha256"):
                    errors.append("quarantined legacy surface tree hash differs from ledger")
                    quarantine_state = "QUARANTINE_HASH_CONFLICT"
                else:
                    quarantine_state = "QUARANTINED_LEDGER_RECONCILED"
                current_manifest_hash = manifest.get("sha256")
                if current_manifest_hash != last.get("historical_manifest_sha256"):
                    warnings.append("C11-C manifest changed after quarantine; reconciliation requires manual review")
                    quarantine_state = "QUARANTINE_MANIFEST_CONFLICT"
            except Exception as exc:
                errors.append(f"quarantine destination verification: {exc}")
                quarantine_state = "QUARANTINE_DESTINATION_MISSING"
        else:
            errors.append("legacy c11d-control source is missing without a matching quarantine ledger event")
            quarantine_state = "UNTRACKED_MISSING"
    try:
        cleanup_items, cleanup_errors = _candidate_files(root, policy)
        errors.extend(cleanup_errors)
    except Exception as exc:
        cleanup_items = []
        errors.append(f"cleanup allowlist inspection: {exc}")
    required_docs = [
        "docs/current/d/C11-D_ROADMAP_V1.0_STATELESS.md",
        "docs/current/d/C11-D_MILESTONES_APPROVED.md",
        "docs/current/suite/C11C_SUITE_CURRENT_RULES.md",
        "docs/current/suite/C11C_SUITE_TOOLING_MATRIX.md",
        "docs/current/d/D9_UNIVERSAL_EDITORIAL_MODEL_V1.md",
        "docs/current/d/D9.8_UNIVERSAL_EDITORIAL_MODEL_CHECKPOINT.md",
        "docs/current/d/D9.9_PRODUCER_UNIVERSAL_COVERAGE_CHECKPOINT.md",
        "docs/current/d/D9.10_EDITORIAL_TO_RENDER_BRIDGE_PLANNING_CHECKPOINT.md",
        "docs/current/d/D9.11_MAINTENANCE_0.2.0_CHECKPOINT.md",
    ]
    missing_docs = []
    for rel in required_docs:
        try:
            if not relative_path(root, rel).is_file():
                missing_docs.append(rel)
        except Exception:
            missing_docs.append(rel)
    if missing_docs:
        errors.append("required current governance docs missing: " + ", ".join(missing_docs))
    freeze_ready = False
    freeze_reasons = [
        "D9.11 performs D-branch freeze preflight only; it does not create a release archive",
        "release_authority=NONE and D4.8=BLOCKED",
        "future D renderer/frozen baseline is still a separate roadmap gate",
    ]
    latest_cleanup = _latest_cleanup_event(ledger)
    return {
        "schema": "C11-D-D9.11-MAINTENANCE-PLAN-V1",
        "checkpoint": "D9.11",
        "maintenance_version": "0.2.0",
        "status": "PASS" if not errors else "BLOCKED",
        "mode": "DRY_RUN_ONLY",
        "project_root": ".",
        "active_suite_topology": sorted(row["entrypoint"] for row in apps),
        "registered_surface_count": len(apps),
        "governance": {
            "d4_8": matrix.get("governance", {}).get("d4_8", "UNKNOWN"),
            "release_authority": matrix.get("governance", {}).get("release_authority", "UNKNOWN"),
            "frozen_c11c_mutation": matrix.get("governance", {}).get("frozen_c11c_mutation", "UNKNOWN"),
            "renderer_activation": False,
            "production_execution": False,
            "automatic_seed_generation": False,
            "runtime_seed_derivation": False,
        },
        "legacy_surface": {
            "path": QUARANTINE_SOURCE,
            "registered": False,
            "state": quarantine_state,
            "tree_sha256": source_inventory.get("tree_sha256") if source_inventory else (last.get("tree_sha256") if last else None),
            "file_count": source_inventory.get("file_count") if source_inventory else (last.get("file_count") if last else 0),
            "quarantine_destination": last.get("destination_path") if last and last.get("event_type") == "QUARANTINED" else None,
        },
        "cleanup": {
            "allowlist": policy.get("safe_transient_roots", []),
            "candidate_files": len(cleanup_items),
            "candidate_bytes": sum(row["bytes"] for row in cleanup_items),
            "deletion_policy": "NONE; explicit apply archives to reversible quarantine and records hashes",
            "last_event": latest_cleanup.get("event_type") if latest_cleanup else None,
        },
        "historical_manifest": {
            "path": manifest.get("path"),
            "sha256": manifest.get("sha256"),
            "legacy_control_reference_count": len(manifest.get("legacy_control_references", [])),
            "rewritten": False,
            "reconciliation": "append-only ledger; historical manifest bytes are preserved",
        },
        "documentation": {"status": "REQUIRED_DOCS_PRESENT" if not missing_docs else "BLOCKED_MISSING_DOCS", "missing": missing_docs, "consolidation": "DRY_RUN_ONLY"},
        "freeze_preparation": {"status": "PREPARATION_ONLY_NOT_AUTHORIZED", "freeze_ready": freeze_ready, "reasons": freeze_reasons},
        "warnings": warnings,
        "errors": errors,
        "side_effects": {"files_moved": False, "files_deleted": False, "manifest_rewritten": False, "archive_created": False},
    }


def _choose_destination(root: Path, prefix: str) -> Path:
    base = relative_path(root, "docs/history/root_conflicts")
    if base.exists() and (base.is_symlink() or not base.is_dir() or bool(getattr(base, "is_junction", lambda: False)())):
        raise ValueError("quarantine destination root is not a real directory")
    base.mkdir(parents=True, exist_ok=True)
    stamp = stamp_utc()
    for suffix in range(0, 1000):
        suffix_text = "" if suffix == 0 else f"_{suffix:02d}"
        candidate_rel = f"{prefix}{stamp}{suffix_text}"
        candidate = relative_path(root, candidate_rel)
        if not candidate.exists():
            return candidate
    raise FileExistsError("could not allocate a unique quarantine destination; no files were moved")


def quarantine_legacy_control(root: Path = ROOT, *, apply: bool = False, confirmation: str | None = None) -> dict[str, Any]:
    root = root.resolve()
    plan = build_plan(root)
    if plan["status"] != "PASS":
        return {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "BLOCKED", "operation": "QUARANTINE_LEGACY_CONTROL", "errors": plan["errors"], "side_effects": {"files_moved": False}}
    if not is_allowed_quarantine_source(QUARANTINE_SOURCE, _validate_policy(root)):
        return {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "BLOCKED_PROTECTED_PATH", "operation": "QUARANTINE_LEGACY_CONTROL", "errors": ["quarantine source is not the exact approved unregistered path"], "side_effects": {"files_moved": False}}
    source = relative_path(root, QUARANTINE_SOURCE)
    ledger = load_ledger(root)
    last = latest_lifecycle_event(ledger)
    if not source.exists():
        if last and last.get("event_type") == "QUARANTINED":
            return {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "ALREADY_QUARANTINED", "operation": "QUARANTINE_LEGACY_CONTROL", "destination_path": last.get("destination_path"), "tree_sha256": last.get("tree_sha256"), "side_effects": {"files_moved": False}}
        return {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "BLOCKED", "operation": "QUARANTINE_LEGACY_CONTROL", "errors": ["legacy source missing without matching ledger event"], "side_effects": {"files_moved": False}}
    inventory = inventory_tree(source)
    manifest = _manifest_info(root)
    if not manifest.get("legacy_control_references"):
        return {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "BLOCKED", "operation": "QUARANTINE_LEGACY_CONTROL", "errors": ["historical C11-C freeze manifest does not contain the legacy directory references expected by the reconciliation contract"], "side_effects": {"files_moved": False}}
    if not apply:
        return {
            "schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "WOULD_QUARANTINE", "operation": "QUARANTINE_LEGACY_CONTROL",
            "source_path": QUARANTINE_SOURCE, "proposed_destination_prefix": "docs/history/root_conflicts/c11d-control_quarantine_",
            "tree_sha256": inventory["tree_sha256"], "file_count": inventory["file_count"], "directory_count": inventory["directory_count"],
            "historical_manifest_sha256": manifest["sha256"], "manifest_reference_count": len(manifest["legacy_control_references"]),
            "manifest_rewrite": False, "confirmation_required": CONFIRM_QUARANTINE, "side_effects": {"files_moved": False, "files_deleted": False},
        }
    if confirmation != CONFIRM_QUARANTINE:
        return {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "BLOCKED", "operation": "QUARANTINE_LEGACY_CONTROL", "errors": ["explicit quarantine confirmation token is required"], "side_effects": {"files_moved": False}}
    destination = _choose_destination(root, "docs/history/root_conflicts/c11d-control_quarantine_")
    event = {
        "event_id": f"QUARANTINED-{stamp_utc()}-{inventory['tree_sha256'][:12]}", "occurred_at_utc": now_utc(), "event_type": "QUARANTINED",
        "resource": QUARANTINE_SOURCE, "source_path": QUARANTINE_SOURCE,
        "destination_path": destination.relative_to(root).as_posix(), "tree_sha256": inventory["tree_sha256"],
        "file_count": inventory["file_count"], "directory_count": inventory["directory_count"], "files": inventory["files"],
        "historical_manifest_path": FREEZE_MANIFEST_REL.as_posix(), "historical_manifest_sha256": manifest["sha256"],
        "historical_manifest_references": manifest["legacy_control_references"],
        "manifest_treatment": "PRESERVED_UNMODIFIED_HISTORICAL_EVIDENCE; RECONCILED_BY_APPEND_ONLY_LEDGER",
        "suite_registration": "UNREGISTERED_BEFORE_AND_AFTER_QUARANTINE", "release_authority": "NONE", "d4_8": "BLOCKED",
    }
    source.rename(destination)
    try:
        moved = inventory_tree(destination)
        if moved["tree_sha256"] != inventory["tree_sha256"]:
            raise RuntimeError("post-move tree identity mismatch")
        if sha256_file(relative_path(root, FREEZE_MANIFEST_REL.as_posix())) != manifest["sha256"]:
            raise RuntimeError("historical C11-C manifest changed during quarantine transaction")
        append_event(root, event)
    except Exception as exc:
        try:
            if not source.exists() and destination.exists():
                destination.rename(source)
        except Exception as rollback_exc:
            return {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "RECOVERY_REQUIRED", "operation": "QUARANTINE_LEGACY_CONTROL", "errors": [str(exc), f"rollback failed: {rollback_exc}"], "destination_path": destination.relative_to(root).as_posix(), "side_effects": {"files_moved": True, "ledger_committed": False}}
        return {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "ROLLED_BACK", "operation": "QUARANTINE_LEGACY_CONTROL", "errors": [str(exc)], "side_effects": {"files_moved": False, "ledger_committed": False}}
    return {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "QUARANTINED", "operation": "QUARANTINE_LEGACY_CONTROL", "destination_path": destination.relative_to(root).as_posix(), "tree_sha256": inventory["tree_sha256"], "manifest_reference_count": len(manifest["legacy_control_references"]), "manifest_rewritten": False, "side_effects": {"files_moved": True, "files_deleted": False, "ledger_committed": True}}


def restore_legacy_control(root: Path = ROOT, *, apply: bool = False, confirmation: str | None = None) -> dict[str, Any]:
    root = root.resolve()
    plan = build_plan(root)
    if plan["status"] != "PASS":
        return {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "BLOCKED", "operation": "RESTORE_LEGACY_CONTROL", "errors": plan["errors"], "side_effects": {"files_moved": False}}
    if not is_allowed_quarantine_source(QUARANTINE_SOURCE, _validate_policy(root)):
        return {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "BLOCKED_PROTECTED_PATH", "operation": "RESTORE_LEGACY_CONTROL", "errors": ["restore target is not the exact approved legacy path"], "side_effects": {"files_moved": False}}
    ledger = load_ledger(root)
    last = latest_lifecycle_event(ledger)
    if not last or last.get("event_type") != "QUARANTINED":
        return {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "BLOCKED", "operation": "RESTORE_LEGACY_CONTROL", "errors": ["there is no latest active quarantine to restore"], "side_effects": {"files_moved": False}}
    source = relative_path(root, QUARANTINE_SOURCE)
    destination = relative_path(root, str(last.get("destination_path", "")))
    if source.exists():
        return {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "BLOCKED_SOURCE_CONFLICT", "operation": "RESTORE_LEGACY_CONTROL", "errors": ["source already exists; restore will not overwrite or merge it"], "side_effects": {"files_moved": False}}
    if not destination.exists():
        return {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "BLOCKED_DESTINATION_MISSING", "operation": "RESTORE_LEGACY_CONTROL", "errors": ["quarantined destination is missing"], "side_effects": {"files_moved": False}}
    actual = inventory_tree(destination)
    if actual.get("tree_sha256") != last.get("tree_sha256"):
        return {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "BLOCKED_TREE_HASH_MISMATCH", "operation": "RESTORE_LEGACY_CONTROL", "errors": ["quarantined tree no longer matches ledger identity"], "side_effects": {"files_moved": False}}
    manifest = _manifest_info(root)
    if manifest.get("sha256") != last.get("historical_manifest_sha256"):
        return {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "BLOCKED_MANIFEST_CHANGED", "operation": "RESTORE_LEGACY_CONTROL", "errors": ["historical manifest differs from quarantine record; manual reconciliation required"], "side_effects": {"files_moved": False}}
    if not apply:
        return {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "WOULD_RESTORE", "operation": "RESTORE_LEGACY_CONTROL", "source_path": QUARANTINE_SOURCE, "destination_path": last["destination_path"], "tree_sha256": actual["tree_sha256"], "confirmation_required": CONFIRM_RESTORE, "side_effects": {"files_moved": False}}
    if confirmation != CONFIRM_RESTORE:
        return {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "BLOCKED", "operation": "RESTORE_LEGACY_CONTROL", "errors": ["explicit restore confirmation token is required"], "side_effects": {"files_moved": False}}
    source.parent.mkdir(parents=True, exist_ok=True)
    destination.rename(source)
    event = {
        "event_id": f"RESTORED-{stamp_utc()}-{actual['tree_sha256'][:12]}", "occurred_at_utc": now_utc(), "event_type": "RESTORED",
        "resource": QUARANTINE_SOURCE, "source_path": last["destination_path"], "destination_path": QUARANTINE_SOURCE,
        "tree_sha256": actual["tree_sha256"], "file_count": actual["file_count"], "directory_count": actual["directory_count"],
        "historical_manifest_path": FREEZE_MANIFEST_REL.as_posix(), "historical_manifest_sha256": manifest["sha256"],
        "manifest_treatment": "PRESERVED_UNMODIFIED_HISTORICAL_EVIDENCE", "suite_registration": "REMAINS_UNREGISTERED", "release_authority": "NONE", "d4_8": "BLOCKED",
    }
    try:
        append_event(root, event)
    except Exception as exc:
        try:
            if source.exists() and not destination.exists():
                source.rename(destination)
        except Exception as rollback_exc:
            return {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "RECOVERY_REQUIRED", "operation": "RESTORE_LEGACY_CONTROL", "errors": [str(exc), f"rollback failed: {rollback_exc}"], "side_effects": {"files_moved": True, "ledger_committed": False}}
        return {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "ROLLED_BACK", "operation": "RESTORE_LEGACY_CONTROL", "errors": [str(exc)], "side_effects": {"files_moved": False, "ledger_committed": False}}
    return {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "RESTORED", "operation": "RESTORE_LEGACY_CONTROL", "source_path": QUARANTINE_SOURCE, "tree_sha256": actual["tree_sha256"], "manifest_rewritten": False, "side_effects": {"files_moved": True, "ledger_committed": True}}


def cleanup_allowlisted(root: Path = ROOT, *, apply: bool = False, confirmation: str | None = None) -> dict[str, Any]:
    root = root.resolve()
    plan = build_plan(root)
    if plan["status"] != "PASS":
        return {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "BLOCKED", "operation": "CLEANUP_ALLOWLISTED", "errors": plan["errors"], "side_effects": {"files_moved": False, "files_deleted": False}}
    policy = _validate_policy(root)
    if any(is_protected_path(rel, policy) for rel in policy.get("safe_transient_roots", [])):
        return {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "BLOCKED_PROTECTED_PATH", "operation": "CLEANUP_ALLOWLISTED", "errors": ["cleanup allowlist overlaps a protected root"], "side_effects": {"files_moved": False, "files_deleted": False}}
    items, errors = _candidate_files(root, policy)
    if errors:
        return {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "BLOCKED", "operation": "CLEANUP_ALLOWLISTED", "errors": errors, "side_effects": {"files_moved": False, "files_deleted": False}}
    if not apply:
        return {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "WOULD_ARCHIVE_ALLOWLISTED_TRANSIENTS", "operation": "CLEANUP_ALLOWLISTED", "allowlist": policy["safe_transient_roots"], "files": items, "file_count": len(items), "bytes": sum(x["bytes"] for x in items), "confirmation_required": CONFIRM_CLEANUP, "permanent_deletion": False, "side_effects": {"files_moved": False, "files_deleted": False}}
    if confirmation != CONFIRM_CLEANUP:
        return {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "BLOCKED", "operation": "CLEANUP_ALLOWLISTED", "errors": ["explicit transient cleanup confirmation token is required"], "side_effects": {"files_moved": False, "files_deleted": False}}
    ledger = load_ledger(root)
    run_stamp = stamp_utc()
    archive_rel = f"artifacts/maintenance/d9_11/cleanup_quarantine/{run_stamp}"
    archive = relative_path(root, archive_rel)
    if archive.exists():
        suffix = 1
        while True:
            alt_rel = f"artifacts/maintenance/d9_11/cleanup_quarantine/{run_stamp}_{suffix:02d}"
            archive = relative_path(root, alt_rel)
            if not archive.exists():
                archive_rel = alt_rel
                break
            suffix += 1
    moved: list[tuple[Path, Path]] = []
    archive.mkdir(parents=True, exist_ok=False)
    try:
        for item in items:
            source = relative_path(root, item["path"])
            destination = archive / item["path"]
            destination.parent.mkdir(parents=True, exist_ok=True)
            if destination.exists():
                raise FileExistsError(f"archive destination conflict: {destination.relative_to(root).as_posix()}")
            if not source.is_file() or sha256_file(source) != item["sha256"]:
                raise RuntimeError(f"candidate changed after preview: {item['path']}")
            source.rename(destination)
            moved.append((source, destination))
        # Remove only empty nested directories beneath allowlisted roots; preserve the roots.
        for rel in policy["safe_transient_roots"]:
            base = relative_path(root, rel)
            if not base.exists():
                continue
            for folder in sorted((p for p in base.rglob("*") if p.is_dir()), key=lambda p: len(p.parts), reverse=True):
                if folder.is_symlink() or bool(getattr(folder, "is_junction", lambda: False)()):
                    raise RuntimeError(f"symlink/junction appeared during cleanup: {folder.relative_to(root).as_posix()}")
                try:
                    folder.rmdir()
                except OSError:
                    pass
        event = {
            "event_id": f"CLEANUP_ARCHIVED-{run_stamp}", "occurred_at_utc": now_utc(), "event_type": "CLEANUP_ARCHIVED",
            "resource": "SAFE_TRANSIENT_ALLOWLIST", "archive_path": archive_rel, "allowlist": policy["safe_transient_roots"],
            "files": items, "file_count": len(items), "bytes": sum(x["bytes"] for x in items),
            "permanent_deletion": False, "reversible": True,
        }
        ledger["events"].append(event)
        write_ledger_atomic(root, ledger)
    except Exception as exc:
        rollback_errors = []
        for source, destination in reversed(moved):
            try:
                source.parent.mkdir(parents=True, exist_ok=True)
                if source.exists():
                    raise FileExistsError(f"rollback source conflict: {source.relative_to(root).as_posix()}")
                destination.rename(source)
            except Exception as rollback_exc:
                rollback_errors.append(str(rollback_exc))
        if not rollback_errors:
            try:
                shutil.rmtree(archive, ignore_errors=True)
            except Exception:
                pass
            return {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "ROLLED_BACK", "operation": "CLEANUP_ALLOWLISTED", "errors": [str(exc)], "side_effects": {"files_moved": False, "files_deleted": False}}
        return {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "RECOVERY_REQUIRED", "operation": "CLEANUP_ALLOWLISTED", "errors": [str(exc), *rollback_errors], "archive_path": archive_rel, "side_effects": {"files_moved": bool(moved), "files_deleted": False}}
    return {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "ARCHIVED_ALLOWLISTED_TRANSIENTS", "operation": "CLEANUP_ALLOWLISTED", "archive_path": archive_rel, "file_count": len(items), "bytes": sum(x["bytes"] for x in items), "permanent_deletion": False, "side_effects": {"files_moved": bool(items), "files_deleted": False, "ledger_committed": True}}


def restore_cleanup_archive(root: Path = ROOT, *, apply: bool = False, confirmation: str | None = None) -> dict[str, Any]:
    root = root.resolve()
    ledger = load_ledger(root)
    last = _latest_cleanup_event(ledger)
    if not last or last.get("event_type") != "CLEANUP_ARCHIVED":
        return {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "BLOCKED", "operation": "RESTORE_CLEANUP_ARCHIVE", "errors": ["there is no latest active cleanup archive to restore"], "side_effects": {"files_moved": False}}
    archive = relative_path(root, str(last.get("archive_path", "")))
    items = last.get("files", [])
    if not archive.is_dir():
        return {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "BLOCKED_ARCHIVE_MISSING", "operation": "RESTORE_CLEANUP_ARCHIVE", "errors": ["cleanup archive is missing"], "side_effects": {"files_moved": False}}
    for item in items:
        source = relative_path(root, item["path"])
        archived = archive / item["path"]
        if source.exists():
            return {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "BLOCKED_SOURCE_CONFLICT", "operation": "RESTORE_CLEANUP_ARCHIVE", "errors": [f"restore will not overwrite existing path: {item['path']}"], "side_effects": {"files_moved": False}}
        if not archived.is_file() or sha256_file(archived) != item.get("sha256"):
            return {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "BLOCKED_ARCHIVE_HASH_MISMATCH", "operation": "RESTORE_CLEANUP_ARCHIVE", "errors": [f"archived file missing or hash mismatch: {item['path']}"], "side_effects": {"files_moved": False}}
    if not apply:
        return {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "WOULD_RESTORE_CLEANUP_ARCHIVE", "operation": "RESTORE_CLEANUP_ARCHIVE", "archive_path": last["archive_path"], "file_count": len(items), "confirmation_required": CONFIRM_RESTORE_CLEANUP, "side_effects": {"files_moved": False}}
    if confirmation != CONFIRM_RESTORE_CLEANUP:
        return {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "BLOCKED", "operation": "RESTORE_CLEANUP_ARCHIVE", "errors": ["explicit cleanup restore confirmation token is required"], "side_effects": {"files_moved": False}}
    moved: list[tuple[Path, Path]] = []
    try:
        for item in items:
            source = relative_path(root, item["path"])
            archived = archive / item["path"]
            source.parent.mkdir(parents=True, exist_ok=True)
            archived.rename(source)
            moved.append((source, archived))
        ledger["events"].append({"event_id": f"CLEANUP_RESTORED-{stamp_utc()}", "occurred_at_utc": now_utc(), "event_type": "CLEANUP_RESTORED", "resource": "SAFE_TRANSIENT_ALLOWLIST", "archive_path": last["archive_path"], "files": items, "file_count": len(items), "reversible": True})
        write_ledger_atomic(root, ledger)
    except Exception as exc:
        rollback_errors = []
        for source, archived in reversed(moved):
            try:
                archived.parent.mkdir(parents=True, exist_ok=True)
                source.rename(archived)
            except Exception as rollback_exc:
                rollback_errors.append(str(rollback_exc))
        return {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "RECOVERY_REQUIRED" if rollback_errors else "ROLLED_BACK", "operation": "RESTORE_CLEANUP_ARCHIVE", "errors": [str(exc), *rollback_errors], "side_effects": {"files_moved": bool(moved)}}
    return {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "RESTORED_CLEANUP_ARCHIVE", "operation": "RESTORE_CLEANUP_ARCHIVE", "file_count": len(items), "side_effects": {"files_moved": bool(items), "ledger_committed": True}}


def docs_audit(root: Path = ROOT) -> dict[str, Any]:
    plan = build_plan(root)
    if plan["status"] != "PASS":
        return {"schema": "C11-D-D9.11-DOC-AUDIT-V1", "status": "BLOCKED", "errors": plan["errors"], "side_effects": {"files_moved": False, "files_written": False}}
    return {
        "schema": "C11-D-D9.11-DOC-AUDIT-V1", "status": "PASS", "mode": "DRY_RUN_ONLY",
        "required_current_documents": [
            "docs/current/d/C11-D_ROADMAP_V1.0_STATELESS.md", "docs/current/d/C11-D_MILESTONES_APPROVED.md",
            "docs/current/suite/C11C_SUITE_CURRENT_RULES.md", "docs/current/suite/C11C_SUITE_TOOLING_MATRIX.md",
            "docs/current/d/D9.11_MAINTENANCE_0.2.0_CHECKPOINT.md",
        ],
        "historical_policy": "Keep dated/older duplicates under docs/history; do not overwrite conflicting evidence.",
        "c11c_consolidator_invoked": False,
        "files_written": False,
        "side_effects": {"files_moved": False, "files_written": False},
    }


def freeze_preflight(root: Path = ROOT) -> dict[str, Any]:
    plan = build_plan(root)
    return {
        "schema": "C11-D-D9.11-FREEZE-PREFLIGHT-V1", "status": "PASS" if plan["status"] == "PASS" else "BLOCKED",
        "mode": "PREFLIGHT_ONLY_NOT_AUTHORIZED", "maintenance_plan_status": plan["status"],
        "immutable_c11c_reference": {"zip_sha256": EXPECTED_C11C_ZIP_SHA256, "tree_sha256": EXPECTED_C11C_TREE_SHA256, "mutation": "FORBIDDEN"},
        "current_c11c_manifest": plan.get("historical_manifest", {}),
        "governance": {"d4_8": "BLOCKED", "release_authority": "NONE", "renderer_activation": False, "production_execution": False},
        "freeze_ready": False,
        "blocking_reasons": [
            "D9.11 is maintenance preflight, not an authorized release/freeze checkpoint",
            "future D frozen baseline is required before physical editorial-to-render materialization",
            "C11-C frozen reference and historical manifest must remain unchanged",
        ],
        "errors": plan["errors"],
        "side_effects": {"archive_created": False, "manifest_rewritten": False, "files_moved": False, "files_deleted": False},
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="C11-D D9.11 safe maintenance (dry-run by default)")
    subs = parser.add_subparsers(dest="command", required=True)
    subs.add_parser("plan", help="inspect D9.11 maintenance plan without filesystem mutation")
    subs.add_parser("docs-audit", help="read-only current governance documentation audit")
    subs.add_parser("freeze-preflight", help="read-only D-branch freeze preparation check")
    subs.add_parser("cleanup-preview", help="inspect allowlisted transient files")
    cleanup = subs.add_parser("cleanup-allowlisted", help="reversibly archive allowlisted transient files")
    cleanup.add_argument("--apply", action="store_true")
    cleanup.add_argument("--confirm", default=None)
    qc = subs.add_parser("quarantine-legacy-control", help="preview or quarantine the one legacy unregistered directory")
    qc.add_argument("--apply", action="store_true")
    qc.add_argument("--confirm", default=None)
    rs = subs.add_parser("restore-legacy-control", help="preview or restore a verified quarantine")
    rs.add_argument("--apply", action="store_true")
    rs.add_argument("--confirm", default=None)
    rc = subs.add_parser("restore-cleanup-archive", help="preview or restore the latest reversible transient archive")
    rc.add_argument("--apply", action="store_true")
    rc.add_argument("--confirm", default=None)
    args = parser.parse_args(argv)
    try:
        if args.command == "plan":
            result = build_plan(ROOT)
        elif args.command == "docs-audit":
            result = docs_audit(ROOT)
        elif args.command == "freeze-preflight":
            result = freeze_preflight(ROOT)
        elif args.command == "cleanup-preview":
            result = cleanup_allowlisted(ROOT, apply=False)
        elif args.command == "cleanup-allowlisted":
            result = cleanup_allowlisted(ROOT, apply=args.apply, confirmation=args.confirm)
        elif args.command == "quarantine-legacy-control":
            result = quarantine_legacy_control(ROOT, apply=args.apply, confirmation=args.confirm)
        elif args.command == "restore-legacy-control":
            result = restore_legacy_control(ROOT, apply=args.apply, confirmation=args.confirm)
        elif args.command == "restore-cleanup-archive":
            result = restore_cleanup_archive(ROOT, apply=args.apply, confirmation=args.confirm)
        else:
            raise ValueError(f"unsupported command: {args.command}")
    except Exception as exc:
        result = {"schema": "C11-D-D9.11-OPERATION-RESULT-V1", "status": "BLOCKED", "operation": args.command, "errors": [f"{type(exc).__name__}: {exc}"], "side_effects": {"files_moved": False, "files_deleted": False, "manifest_rewritten": False}}
    emit(result)
    return 0 if result.get("status") in {"PASS", "WOULD_QUARANTINE", "QUARANTINED", "ALREADY_QUARANTINED", "WOULD_RESTORE", "RESTORED", "WOULD_ARCHIVE_ALLOWLISTED_TRANSIENTS", "ARCHIVED_ALLOWLISTED_TRANSIENTS", "WOULD_RESTORE_CLEANUP_ARCHIVE", "RESTORED_CLEANUP_ARCHIVE", "PASS_WITH_REVIEW"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
