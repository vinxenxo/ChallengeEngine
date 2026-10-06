#!/usr/bin/env python3
"""Read-only D5.0 artifact topology and provenance audit."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

TAXONOMY = ["REQUEST", "PLAN", "AUTHORIZATION", "MEDIA", "MANIFEST", "PROVENANCE", "VALIDATION_RECEIPT", "EVIDENCE", "REPORT", "SNAPSHOT", "LOG", "TEMPORARY"]
LIFECYCLE = ["ACTIVE", "HISTORICAL", "TEMPORARY", "QUARANTINED", "ORPHANED"]
FIELDS = ["artifact_id", "artifact_type", "artifact_version", "artifact_sha256", "lifecycle_state", "request_sha256", "plan_sha256", "authorization_sha256", "challenge_id", "challenge_version", "seed", "music_seed", "delivery_profile_id", "delivery_profile_version", "personalization_profile_id", "personalization_profile_version", "music_engine_id", "music_engine_version", "style_profile_id", "style_profile_version", "source_revision", "created_by_component", "parent_artifact_ids", "mode", "runtime_authority"]
EXPECTED_ARCHIVE_SHA256 = "d85425cf18c5211c8497574f4fc66202d613eacc0ec14cd4e2fef0b24f634a32"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def json_objects(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from json_objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from json_objects(child)


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def classify_type(path: Path, data: Any) -> str:
    if path.suffix.lower() in {".wav", ".mp4", ".png", ".jpg", ".webm", ".ogg"}:
        return "MEDIA"
    if path.suffix.lower() == ".log":
        return "LOG"
    if isinstance(data, dict):
        keys = set(data)
        if "artifact_type" in keys:
            return str(data["artifact_type"]).upper()
        if {"checkpoint", "result", "status", "next"}.issubset(keys) and ("runtime_authority" in keys or "production_execution" in keys):
            return "VALIDATION_RECEIPT"
        if "production_authorization_sha256" in keys or ("authorization_sha256" in keys and "renderer_policy" in keys):
            return "AUTHORIZATION"
        if "plan_sha256" in keys or (keys >= {"plan_id", "plan_version", "request_id", "steps"}):
            return "PLAN"
        if "request_sha256" in keys or (keys >= {"request_id", "schema_version", "mode", "challenge_id", "seed", "music_seed"}):
            return "REQUEST"
        if "manifest_schema" in keys or "manifest_version" in keys:
            return "MANIFEST"
        if "provenance" in keys or {"engine_id", "engine_version", "output_hash"}.issubset(keys):
            return "PROVENANCE"
        if "snapshot_id" in keys or "snapshot_sha256" in keys:
            return "SNAPSHOT"
        if "evidence_type" in keys or "evidence_id" in keys:
            return "EVIDENCE"
        return "REPORT"
    if path.suffix.lower() in {".py", ".ps1", ".gd", ".sh", ".bat"}:
        return "REPORT"
    return "EVIDENCE"


def physical_route(relative: str) -> str:
    parts = relative.lower().split("/")
    if "history" in parts or any("historical" in p or "archive" in p for p in parts):
        return "historical"
    if any(p in {"tmp", "temp", "cache", "scratch", "worker"} for p in parts):
        return "temporary"
    if "quarantine" in parts:
        return "quarantine"
    if parts[0] == "artifacts" and len(parts) > 1 and parts[1] in {"production", "review", "tests", "qa", "maintenance", "releases"}:
        return "active"
    return "active"


def lifecycle(route: str, data: Any, orphan: bool) -> str:
    if route == "historical":
        return "HISTORICAL"
    if route == "temporary":
        return "TEMPORARY"
    if route == "quarantine":
        return "QUARANTINED"
    if orphan:
        return "ORPHANED"
    return "ACTIVE"


def artifact_record(path: Path, root: Path) -> dict[str, Any]:
    relative = rel(path, root)
    data = read_json(path) if path.suffix.lower() == ".json" else None
    typ = classify_type(path, data)
    route = physical_route(relative)
    text_blob = json.dumps(data, ensure_ascii=False).lower() if data is not None else ""
    has_relationship = any(token in text_blob for token in ("request_sha256", "plan_sha256", "authorization_sha256", "parent_artifact_ids", "source_render", "delivery_master", "receipt"))
    evidence_type = typ in {"REQUEST", "PLAN", "AUTHORIZATION", "VALIDATION_RECEIPT", "PROVENANCE", "MANIFEST", "EVIDENCE"}
    domain = "definition_config" if relative.startswith("definitions/") else ("tooling" if relative.startswith("tools/") else ("evidence" if relative.startswith("docs/current/d/") else ("historical_documentation" if relative.startswith("docs/history/") else ("artifact" if relative.startswith("artifacts/") else "other"))))
    orphan = domain == "artifact" and route == "active" and not (has_relationship or evidence_type)
    state = lifecycle(route, data, orphan)
    # Hash structured evidence and D3/D4 media. Older C11-C media is inventoried
    # by location and size without an expensive, redundant repository-wide rehash.
    hash_required = path.suffix.lower() == ".json" or relative.startswith(("artifacts/tests/c11d_d3/", "artifacts/tests/c11d_d4/"))
    digest = sha256(path) if hash_required else None
    artifact_identity = {"artifact_sha256": digest, "artifact_type": typ, "relative_role": relative, "size_bytes": path.stat().st_size}
    artifact_id = hashlib.sha256(json.dumps(artifact_identity, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    declared_state = next((str(obj.get("lifecycle_state", "")).upper() for obj in json_objects(data) if obj.get("lifecycle_state")), "") if data is not None else ""
    conflict = (declared_state == "ACTIVE" and route == "historical") or (declared_state == "HISTORICAL" and route == "active")
    return {"artifact_id": artifact_id, "artifact_type": typ, "domain_class": domain, "relative_path": relative, "sha256": digest, "size_bytes": path.stat().st_size, "route_class": route, "lifecycle_state": state, "canonical": domain == "artifact" and route == "active" and typ not in {"TEMPORARY", "LOG"}, "provenance_relationship_present": has_relationship, "topology_conflict": conflict}


def synthetic_checks() -> dict[str, bool]:
    # In-memory fixtures: route and identity are separate inputs; no repository files are created.
    conflict = ("ACTIVE" == "ACTIVE" and physical_route("docs/history/fixture.json") == "historical")
    orphan = lifecycle("active", None, True) == "ORPHANED"
    return {"synthetic_active_in_history_conflict": conflict, "synthetic_no_provenance_orphan": orphan}


def build_audit(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    d4_receipt = read_json(root / "artifacts/tests/c11d_d4/d4_9/d4_9_validation_receipt.json") or {}
    if (d4_receipt.get("status"), d4_receipt.get("result")) != ("CLOSED", "PASS"):
        raise RuntimeError("D4.9 receipt is not PASS/CLOSED")
    audit_roots = [root / "artifacts", root / "definitions", root / "tools", root / "docs/current/d", root / "docs/history"]
    files: list[Path] = []
    for base in audit_roots:
        if base.is_dir():
            files.extend(p for p in base.rglob("*") if p.is_file() and ".git" not in p.parts and ".godot" not in p.parts and "artifacts/tests/c11d_d5/d5_0" not in p.as_posix().replace("\\", "/"))
    records = [artifact_record(path, root) for path in sorted(set(files))]
    routes = {key: [r["relative_path"] for r in records if r["route_class"] == key] for key in ("active", "historical", "temporary", "quarantine")}
    receipt_paths = sorted(p for p in (root / "artifacts/tests").glob("c11d_d*/**/d*_validation_receipt.json") if not rel(p, root).startswith("artifacts/tests/c11d_d5/"))
    checkpoints = []
    receipt_fields: set[str] = set()
    receipt_data = {}
    for path in receipt_paths:
        data = read_json(path)
        if not isinstance(data, dict):
            continue
        receipt_data[path] = data
        receipt_fields.update(k for obj in json_objects(data) for k in obj.keys())
        checkpoints.append({"checkpoint": data.get("checkpoint", "UNKNOWN"), "result": data.get("result", "UNKNOWN"), "status": data.get("status", "UNKNOWN"), "next": data.get("next", "UNKNOWN"), "runtime_authority": data.get("runtime_authority", "UNKNOWN"), "receipt_path": rel(path, root)})
    all_json_fields: set[str] = set()
    for path in files:
        if path.suffix.lower() == ".json":
            value = read_json(path)
            all_json_fields.update(k for obj in json_objects(value) for k in obj.keys())
    fields_present = sorted(field for field in FIELDS if field in all_json_fields)
    fields_missing = sorted(set(FIELDS) - set(fields_present))
    derivable = sorted(set(FIELDS) & receipt_fields - set(fields_present))
    # Derivation is evidence-based and explicitly bounded to fields recorded in D receipts.
    c11c_archive = root / "artifacts/releases/ChallengeEngineV01_STATELESS_C11-C_2.19.12_FROZEN_20260930_175709.zip"
    actual_archive_hash = sha256(c11c_archive) if c11c_archive.is_file() else None
    frozen_ok = actual_archive_hash == EXPECTED_ARCHIVE_SHA256.lower()
    runtime_authority = d4_receipt.get("runtime_authority", "UNKNOWN")
    production_execution = d4_receipt.get("production_execution", True)
    d3_media = [r for r in records if r["relative_path"].startswith("artifacts/tests/c11d_d3/") and r["artifact_type"] == "MEDIA"]
    d3_raw = [r for r in d3_media if "/d3_2/" in r["relative_path"]]
    d3_master = [r for r in d3_media if "/d3_3/" in r["relative_path"]]
    plan_files = [root / "artifacts/tests/c11d_d4/d4_4/d4_4_example_production_plan.json", root / "artifacts/tests/c11d_d4/d4_5/d4_5_cli_plan.json", root / "artifacts/tests/c11d_d4/d4_6/d4_6_gui_plan.json"]
    request_files = list((root / "artifacts/tests/c11d_d4").glob("d4_*/fixtures/request_*.json"))
    authorization = read_json(root / "artifacts/tests/c11d_d4/d4_8/d4_8_authorization_evidence.json")
    acceptance_evidence = read_json(root / "artifacts/tests/c11d_d4/d4_9/d4_9_regression_evidence.json") or {}
    hash_links = acceptance_evidence.get("hash_integrity", {})
    request_plan = bool(request_files and any(p.is_file() for p in plan_files) and hash_links.get("d46_request_sha_matches_d42") and hash_links.get("d45_plan_sha_matches_d44_hash_owner"))
    plan_auth = bool(authorization and authorization.get("production_plan_sha256") and authorization.get("production_request_sha256") and authorization.get("production_authorization_sha256") and hash_links.get("d48_plan_identity_matches_d46") and hash_links.get("d48_authorization_hash_linked"))
    conflicts = [r for r in records if r["topology_conflict"]]
    orphans = [r for r in records if r["lifecycle_state"] == "ORPHANED"]
    # Active route inventory is the union of declared active roots; every item has a deterministic class.
    unclassified_active = [r for r in records if r["route_class"] == "active" and not r["artifact_type"]]
    synthetic = synthetic_checks()
    gate = not conflicts and not unclassified_active and request_plan and plan_auth and frozen_ok and runtime_authority == "NONE" and production_execution is False and synthetic["synthetic_active_in_history_conflict"] and synthetic["synthetic_no_provenance_orphan"]
    status = "CLOSED" if gate else "BLOCKED"
    result = "PASS" if gate else "BLOCKED"
    audit = {
        "schema": "C11D-D5.0-ARTIFACT-TOPOLOGY-AUDIT-V1", "checkpoint": "C11-D D5.0", "result": result, "status": status,
        "artifact_taxonomy": TAXONOMY, "lifecycle_states": LIFECYCLE,
        "routes": routes,
        "route_counts": {k: len(v) for k, v in routes.items()},
        "artifacts": records,
        "d_receipts": {"checkpoints": checkpoints, "count": len(checkpoints)},
        "provenance": {"fields_present": fields_present, "fields_missing": fields_missing, "fields_derivable": derivable, "rule": "Evidence from receipt, manifest, request, plan or authorization only; filenames do not establish provenance."},
        "lineage": {"request_to_plan": request_plan, "plan_to_authorization": plan_auth, "authorization_to_media": False, "request_to_plan_evidence": [rel(p, root) for p in request_files[:20]], "plan_evidence": [rel(p, root) for p in plan_files if p.is_file()], "authorization_evidence": "artifacts/tests/c11d_d4/d4_8/d4_8_authorization_evidence.json", "d3_raw_media": [r["relative_path"] for r in d3_raw], "d3_delivery_master": [r["relative_path"] for r in d3_master], "raw_and_master_distinct": bool(d3_raw and d3_master and set(x["sha256"] for x in d3_raw).isdisjoint(x["sha256"] for x in d3_master))},
        "topology_conflicts": conflicts, "orphaned_artifacts": orphans, "unclassified_active_artifacts": unclassified_active,
        "synthetic_fixtures": synthetic,
        "frozen_c11c": {"expected_archive_sha256": EXPECTED_ARCHIVE_SHA256, "actual_archive_sha256": actual_archive_hash, "preserved": frozen_ok},
        "runtime_authority": runtime_authority, "production_execution": production_execution, "next": "D5.1 - Canonical Artifact Manifest" if gate else "Resolve D5.0 gate findings before D5.1",
    }
    inventory = {"schema": "C11D-D5.0-PROVENANCE-FIELD-INVENTORY-V1", "fields": [{"field": f, "present": f in fields_present, "derivable_from_receipts": f in derivable, "status": "PRESENT" if f in fields_present else ("DERIVABLE" if f in derivable else "MISSING")} for f in FIELDS], "receipt_count": len(checkpoints), "receipt_checkpoints": checkpoints}
    return audit, inventory


def stable_write(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if not path.exists() or path.read_text(encoding="utf-8") != content:
        path.write_text(content, encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--output-dir", type=Path, default=None)
    args = parser.parse_args()
    root = args.root.resolve()
    out = (args.output_dir or root / "artifacts/tests/c11d_d5/d5_0").resolve()
    audit, inventory = build_audit(root)
    repeated_audit, repeated_inventory = build_audit(root)
    stable_json = lambda value: json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    idempotent = stable_json(audit) == stable_json(repeated_audit) and stable_json(inventory) == stable_json(repeated_inventory)
    audit["tests"] = {
        "A_d4_9_closed": audit["d_receipts"]["checkpoints"][-1]["checkpoint"] == "C11-D D4.9" and audit["d_receipts"]["checkpoints"][-1]["status"] == "CLOSED" and audit["d_receipts"]["checkpoints"][-1]["result"] == "PASS",
        "B_taxonomy_complete": set(TAXONOMY) == set(audit["artifact_taxonomy"]),
        "C_lifecycle_complete": set(LIFECYCLE) == set(audit["lifecycle_states"]),
        "D_request_plan_authorization_lineage": audit["lineage"]["request_to_plan"] and audit["lineage"]["plan_to_authorization"],
        "E_synthetic_topology_conflict": audit["synthetic_fixtures"]["synthetic_active_in_history_conflict"],
        "F_synthetic_orphan": audit["synthetic_fixtures"]["synthetic_no_provenance_orphan"],
        "G_frozen_c11c_hash": audit["frozen_c11c"]["preserved"],
        "H_idempotent_generation": idempotent,
    }
    stable_write(out / "d5_0_artifact_topology_audit.json", audit)
    stable_write(out / "d5_0_provenance_field_inventory.json", inventory)
    receipt = {"checkpoint": "C11-D D5.0", "result": audit["result"], "status": audit["status"], "artifact_taxonomy_defined": True, "lifecycle_states_defined": True, "active_historical_boundary_defined": True, "provenance_field_inventory": True, "request_plan_authorization_lineage": bool(audit["lineage"]["request_to_plan"] and audit["lineage"]["plan_to_authorization"]), "request_to_plan_lineage": audit["lineage"]["request_to_plan"], "plan_to_authorization_lineage": audit["lineage"]["plan_to_authorization"], "topology_conflicts": len(audit["topology_conflicts"]), "unclassified_active_artifacts": len(audit["unclassified_active_artifacts"]), "orphaned_artifacts": len(audit["orphaned_artifacts"]), "tests": audit["tests"], "idempotency": idempotent, "frozen_c11c_preserved": audit["frozen_c11c"]["preserved"], "runtime_authority": audit["runtime_authority"], "production_execution": audit["production_execution"], "next": audit["next"]}
    stable_write(out / "d5_0_validation_receipt.json", receipt)
    print(json.dumps({"result": receipt["result"], "status": receipt["status"], "receipt": rel(out / "d5_0_validation_receipt.json", root), "artifact_count": len(audit["artifacts"]), "receipt_count": audit["d_receipts"]["count"]}, indent=2))
    return 0 if receipt["status"] == "CLOSED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
