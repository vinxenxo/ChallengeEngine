from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_CANDIDATE_IDENTITY_INVENTORY_V1.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_CANDIDATE_IDENTITY_INVENTORY_SCHEMA_V1.json")
RUNNER_REL = Path("tools/c11d/d9/d_renderer_candidate_identity_inventory.py")
TEST_REL = Path("tools/c11d/d9/test_d_renderer_candidate_identity_inventory.py")
SCHEMA_ID = "C11-D-RENDERER-CANDIDATE-IDENTITY-INVENTORY-V1"
CONTRACT_ID = "C11-D-RENDERER-CANDIDATE-IDENTITY-INVENTORY-CONTRACT-V1"
EXPECTED_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
EXPECTED_CONTRACT_SHA256 = "87be19bbf54e9524a6e23a4c46b92e2d2a7e141f68948a5018ecec8f73136eec"
EXPECTED_SCHEMA_SHA256 = "ad36c8f2b78fcc4f86a574b733f58cba5a4335156f6fe3882ef41dc4a4020205"
EXPECTED_CONTEXT_PATHS = [
    "docs/current/d/D_RENDERER_BASELINE_PREPARATION_PLAN_V1.md",
    "docs/current/d/D_RENDERER_UNIFIED_CONTENT_REVIEW_CHECKPOINT_V1.md",
    "docs/current/d/D_RENDERER_EDITORIAL_FIELD_CONSUMPTION_AUDIT_CHECKPOINT_V1.md",
    "docs/current/d/D_RENDERER_EDITORIAL_FIELD_ROUTING_VISIBILITY_RECONCILIATION_CHECKPOINT_V1.md",
    "docs/current/d/D_RENDERER_EDITORIAL_VISUAL_CONSUMPTION_PHASE_CHECKPOINT_V1.md",
    "docs/current/d/D_RENDERER_CANDIDATE_IO_GAP_AUDIT_CHECKPOINT_V1.md",
    "docs/current/d/D_RENDERER_DYNAMIC_REQUEST_PAYLOAD_BINDING_CHECKPOINT_V1.md",
    "docs/current/d/D_RENDERER_POLICY_APPROVAL_DECISION_PACKET_V1.md",
    "docs/current/d/D_RENDERER_REQUEST_PAYLOAD_MANIFEST_CHECKPOINT_V1.md",
    "docs/current/d/C11D_CONTEXT_CHECKPOINT_D10_20261011.md",
    "docs/current/d/MASTER_HANDOVER_C11D_CURRENT.md",
    "docs/current/d/START_PROMPT_C11D_CURRENT.md",
    "docs/current/d/C11-D_ROADMAP_V1.0_STATELESS.md",
    "docs/current/d/D_RENDERER_VISUAL_DRILL_SEED_DOMAIN_AUDIT_CHECKPOINT_V1.md",
    "docs/current/d/D_RENDERER_CANDIDATE_SEED_DOMAIN_AUDIT_CHECKPOINT_V1.md",
    "docs/current/d/D_RENDERER_SEED_DOMAIN_COLLISION_AUDIT_CHECKPOINT_V1.md",
]
EXPECTED_PACKET_COMPONENTS = [
    {"path": "definitions/c11d/production/D_RENDERER_CANDIDATE_IDENTITY_INVENTORY_V1.json", "role": "IDENTITY_INVENTORY_CONTRACT"},
    {"path": "definitions/c11d/production/D_RENDERER_CANDIDATE_IDENTITY_INVENTORY_SCHEMA_V1.json", "role": "IDENTITY_REPORT_SCHEMA"},
    {"path": "tools/c11d/d9/d_renderer_candidate_identity_inventory.py", "role": "READ_ONLY_INVENTORY_RUNNER"},
    {"path": "tools/c11d/d9/test_d_renderer_candidate_identity_inventory.py", "role": "INVENTORY_TESTS"},
]
EXPECTED_BLOCKERS = [
    "D9_14_REAL_MEDIA_CERTIFICATION_BLOCKED",
    "D9_16_FULL_ACCEPTANCE_NOT_CLOSED",
    "D9_17_CLOSURE_NO_GO",
    "D_RENDERER_BASELINE_APPROVAL_NOT_RECORDED",
    "D_BASELINE_APPROVAL_NOT_RECORDED",
]


class CandidateInventoryError(ValueError):
    """The identity inventory cannot be trusted or violates its read-only scope."""


def _root(project_root: Path | str | None = None) -> Path:
    return Path(project_root).resolve() if project_root is not None else Path(__file__).resolve().parents[3]


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CandidateInventoryError(f"Cannot read required inventory JSON: {path}") from exc
    if not isinstance(value, dict):
        raise CandidateInventoryError(f"JSON root must be an object: {path}")
    return value


def _relative_path(value: Any) -> str:
    if not isinstance(value, str) or not value or "\\" in value or value.startswith("/"):
        raise CandidateInventoryError(f"Inventory path is not normalized repository-relative POSIX syntax: {value!r}")
    parts = value.split("/")
    if any(part in ("", ".", "..") for part in parts) or ":" in parts[0]:
        raise CandidateInventoryError(f"Inventory path escapes or aliases repository root: {value!r}")
    return value


def _probe_godot(project_root: Path, enabled: bool) -> tuple[str, str | None, list[str]]:
    project = (project_root / "project.godot").read_text(encoding="utf-8-sig")
    match = re.search(r'config/features\s*=\s*PackedStringArray\(([^)]*)\)', project)
    features = re.findall(r'"([^"]+)"', match.group(1)) if match else []
    if not enabled:
        return "NOT_PROBED", None, features
    executable = shutil.which("godot") or shutil.which("godot4")
    if not executable:
        return "NOT_FOUND_ON_PATH", None, features
    try:
        result = subprocess.run([executable, "--version"], check=False, capture_output=True, text=True, timeout=5, shell=False)
    except (OSError, subprocess.SubprocessError):
        return "PROBE_FAILED", None, features
    version = (result.stdout or result.stderr).strip().splitlines()
    if result.returncode != 0 or not version:
        return "PROBE_FAILED", None, features
    return "VERSION_PROBED", version[0].strip(), features


def _validate_contract(contract: dict[str, Any]) -> None:
    if contract.get("schema") != CONTRACT_ID or contract.get("schema_version") != "1.0":
        raise CandidateInventoryError("Inventory contract identity/version mismatch")
    if contract.get("status") != "READ_ONLY_CANDIDATE_IDENTITY_ONLY_NOT_APPROVAL_OR_FREEZE":
        raise CandidateInventoryError("Identity inventory contract cannot claim approval or freeze")
    if contract.get("fingerprint_scope") != "DECLARED_RENDERER_CANDIDATE_REVIEW_SURFACE_ONLY_NOT_FULL_REPOSITORY_TREE":
        raise CandidateInventoryError("Fingerprint scope cannot be widened silently")
    if contract.get("required_candidate_blockers") != EXPECTED_BLOCKERS:
        raise CandidateInventoryError("Required candidate blockers changed")
    expected_locks = {
        "renderer_implementation": "NOT_IMPLEMENTED",
        "renderer_build_artifact": "NONE",
        "renderer_input_emitted": False,
        "renderer_dispatch_invoked": False,
        "renderer_activation": "OFF",
        "media_created": False,
        "d4_8": "BLOCKED",
        "release_authority": "NONE",
        "renderer_baseline_approved": False,
        "renderer_baseline_frozen": False,
        "baseline_approval": "MISSING",
        "freeze_eligible": False,
    }
    if contract.get("governance_locks") != expected_locks:
        raise CandidateInventoryError("Inventory cannot self-promote renderer/baseline governance")
    entries = contract.get("source_inventory")
    if not isinstance(entries, list) or len(entries) < 100:
        raise CandidateInventoryError("Candidate identity inventory must cover at least 100 declared artifacts")
    paths: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {"path", "role", "sha256"}:
            raise CandidateInventoryError("Malformed source inventory entry")
        path = _relative_path(entry.get("path"))
        if not isinstance(entry.get("role"), str) or not entry["role"]:
            raise CandidateInventoryError(f"Missing source role: {path}")
        digest = entry.get("sha256")
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise CandidateInventoryError(f"Invalid SHA-256 declaration: {path}")
        paths.append(path)
    if paths != sorted(paths) or len(paths) != len(set(paths)):
        raise CandidateInventoryError("Source inventory must be sorted and contain unique paths")
    protected = contract.get("protected_reference")
    if protected != {"path": "release/C11C_FREEZE_PACKAGE_MANIFEST.json", "sha256": EXPECTED_MANIFEST_SHA256}:
        raise CandidateInventoryError("Protected C11-C manifest reference changed")
    if contract.get("source_inventory_minimum") != 100:
        raise CandidateInventoryError("Source inventory minimum must remain 100")
    if contract.get("report_context_paths") != EXPECTED_CONTEXT_PATHS:
        raise CandidateInventoryError("Review context path allowlist changed")
    if contract.get("review_packet_components") != EXPECTED_PACKET_COMPONENTS:
        raise CandidateInventoryError("Review packet component allowlist changed")


def build_inventory(project_root: Path | str | None = None, *, probe_godot: bool = True) -> dict[str, Any]:
    root = _root(project_root)
    contract_path = root / CONTRACT_REL
    schema_path = root / SCHEMA_REL
    contract = _read_json(contract_path)
    schema = _read_json(schema_path)
    if _sha(contract_path) != EXPECTED_CONTRACT_SHA256:
        raise CandidateInventoryError("Identity inventory contract SHA-256 mismatch; review pins before updating runner")
    if _sha(schema_path) != EXPECTED_SCHEMA_SHA256:
        raise CandidateInventoryError("Identity inventory schema SHA-256 mismatch; review pins before updating runner")
    _validate_contract(contract)
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or schema.get("$id") != "urn:c11d:renderer-candidate-identity-inventory:v1" or schema.get("additionalProperties") is not False:
        raise CandidateInventoryError("Identity report schema identity/strictness mismatch")

    rows: list[dict[str, Any]] = []
    for pin in contract["source_inventory"]:
        rel = pin["path"]
        path = root / rel
        if not path.is_file():
            raise CandidateInventoryError(f"Pinned candidate source is missing: {rel}")
        actual = _sha(path)
        if actual != pin["sha256"]:
            raise CandidateInventoryError(f"Pinned candidate source SHA-256 mismatch: {rel}")
        rows.append({"path": rel, "role": pin["role"], "sha256": actual, "size_bytes": path.stat().st_size})

    protected = contract["protected_reference"]
    manifest = root / protected["path"]
    if not manifest.is_file() or _sha(manifest) != EXPECTED_MANIFEST_SHA256:
        raise CandidateInventoryError("Frozen C11-C manifest does not match its authoritative SHA-256")

    packet_components: list[dict[str, Any]] = []
    for item in contract["review_packet_components"]:
        rel = _relative_path(item.get("path"))
        path = root / rel
        if not path.is_file():
            raise CandidateInventoryError(f"Review packet component missing: {rel}")
        packet_components.append({"path": rel, "role": item["role"], "sha256": _sha(path), "size_bytes": path.stat().st_size})

    review_context: list[dict[str, Any]] = []
    for rel_value in contract["report_context_paths"]:
        rel = _relative_path(rel_value)
        path = root / rel
        if not path.is_file():
            raise CandidateInventoryError(f"Required review context document missing: {rel}")
        review_context.append({"path": rel, "sha256": _sha(path), "size_bytes": path.stat().st_size})

    rows.sort(key=lambda x: x["path"])
    fingerprint = sha256_json(rows)
    godot_status, godot_version, features = _probe_godot(root, probe_godot)
    report: dict[str, Any] = {
        "schema": SCHEMA_ID,
        "schema_version": "1.0",
        "status": "IDENTITY_ONLY_REVIEW_PACKET_NOT_BASELINE_READY",
        "candidate_id": contract["candidate_id"],
        "fingerprint_scope": contract["fingerprint_scope"],
        "source_count": len(rows),
        "source_inventory": rows,
        "source_fingerprint": fingerprint,
        "protected_reference": {"path": protected["path"], "sha256": EXPECTED_MANIFEST_SHA256, "matches_expected": True},
        "review_packet_components": packet_components,
        "review_context": review_context,
        "toolchain": {
            "python_version": platform.python_version(),
            "python_implementation": sys.implementation.name,
            "host_platform": platform.system(),
            "project_engine_features": features,
            "godot_probe_status": godot_status,
            "godot_version": godot_version,
        },
        "governance": dict(contract["governance_locks"]),
        "required_candidate_blockers": list(EXPECTED_BLOCKERS),
    }
    report["report_sha256"] = sha256_json(report)
    _validate_report(report, schema)
    return report


def _validate_report(report: dict[str, Any], schema: dict[str, Any]) -> None:
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        # Minimal structural check keeps inventory usable without optional dependency.
        required = schema.get("required", [])
        if set(required) - set(report) or report.get("schema") != SCHEMA_ID or report.get("status") != "IDENTITY_ONLY_REVIEW_PACKET_NOT_BASELINE_READY":
            raise CandidateInventoryError("Report failed structural schema fallback")
    else:
        errors = sorted(Draft202012Validator(schema).iter_errors(report), key=lambda err: list(err.path))
        if errors:
            raise CandidateInventoryError("Identity report schema validation failed: " + "; ".join(e.message for e in errors[:5]))
    unsigned = {key: value for key, value in report.items() if key != "report_sha256"}
    if report.get("report_sha256") != sha256_json(unsigned):
        raise CandidateInventoryError("Identity report SHA-256 mismatch")
    if report.get("source_count") != len(report.get("source_inventory", [])):
        raise CandidateInventoryError("Source count does not match inventory")
    if report.get("governance", {}).get("renderer_activation") != "OFF" or report.get("governance", {}).get("release_authority") != "NONE":
        raise CandidateInventoryError("Inventory cannot activate renderer or grant release authority")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only D renderer candidate identity inventory; never renders or persists a report.")
    parser.add_argument("--no-godot-version-probe", action="store_true", help="do not run the harmless Godot --version query")
    parser.add_argument("--full-report", action="store_true", help="emit the full declared-source JSON report; default output is a concise summary")
    args = parser.parse_args(argv)
    try:
        report = build_inventory(probe_godot=not args.no_godot_version_probe)
    except CandidateInventoryError as exc:
        print(f"C11-D RENDERER CANDIDATE IDENTITY INVENTORY FAIL: {exc}", file=sys.stderr)
        return 2
    if args.full_report:
        print("C11-D RENDERER CANDIDATE IDENTITY INVENTORY=" + json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    print(
        "C11-D RENDERER CANDIDATE IDENTITY PASS"
        f" | source_files={report['source_count']}"
        f" | fingerprint={report['source_fingerprint']}"
        f" | report_sha256={report['report_sha256']}"
        f" | python={report['toolchain']['python_version']}"
        f" | godot_probe={report['toolchain']['godot_probe_status']}"
        f" | C11-C=IMMUTABLE_REFERENCE_MATCH"
        f" | renderer=OFF | renderer_build=NONE | media_created=false"
        f" | D4.8=BLOCKED | release_authority=NONE | baseline_approval=MISSING | freeze_eligible=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
