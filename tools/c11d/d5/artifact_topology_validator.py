#!/usr/bin/env python3
"""Validate filesystem, D5.1 identity, and D5.2 lineage consistency."""
from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from collections import defaultdict
from pathlib import Path
from typing import Any

FROZEN_SHA256 = "d85425cf18c5211c8497574f4fc66202d613eacc0ec14cd4e2fef0b24f634a32"
MANIFEST = "artifacts/tests/c11d_d5/d5_1/d5_1_canonical_artifact_manifest.json"
REGISTRY = "artifacts/tests/c11d_d5/d5_2/d5_2_lineage_registry.json"
OUTPUTS = Path("artifacts/tests/c11d_d5/d5_3")
TYPES = ["REQUEST", "PLAN", "AUTHORIZATION", "MEDIA", "MANIFEST", "PROVENANCE", "VALIDATION_RECEIPT", "EVIDENCE", "REPORT", "SNAPSHOT", "LOG", "TEMPORARY"]
LIFECYCLES = ["ACTIVE", "HISTORICAL", "TEMPORARY", "QUARANTINED", "ORPHANED"]
EVIDENCE_TYPES = {"manifest", "receipt", "contract", "audit", "evidence"}


def json_bytes(data: Any) -> bytes:
    return (json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")


def canonical_json(data: Any) -> bytes:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def stable_write(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json_bytes(data)
    if not path.exists() or path.read_bytes() != payload:
        path.write_bytes(payload)


def artifact_identity_id(item: dict[str, Any]) -> str:
    identity = {
        "artifact_type": item["artifact_type"],
        "artifact_role": item["artifact_role"],
        "artifact_version": item["artifact_version"],
        "producer_component": item["producer_component"],
        "parent_artifact_ids": sorted(set(item.get("parent_artifact_ids", []))),
    }
    return sha_bytes(canonical_json(identity))


def all_locations(item: dict[str, Any]) -> list[str]:
    return sorted(set([item["relative_path"], *item.get("alternate_relative_paths", [])]))


def physical_path_issue(path: Path, expected_sha256: str | None = None) -> tuple[str | None, str | None]:
    if not path.is_file():
        return None, "MISSING_PHYSICAL_ARTIFACT"
    actual = sha_file(path)
    if expected_sha256 and actual != expected_sha256:
        return actual, "CONTENT_HASH_MISMATCH"
    return actual, None


def copy_hash_conflict(artifact_id: str, hashes: set[str]) -> dict[str, Any] | None:
    if len(hashes) > 1:
        return {"artifact_id": artifact_id, "content_sha256_values": sorted(hashes), "code": "IDENTITY_CONTENT_CONFLICT"}
    return None


def invalid_edge_target(edge: dict[str, Any], known_ids: set[str]) -> bool:
    return edge.get("target_artifact_id") not in known_ids


def lifecycle_conflict_code(state: str, route: str, item: dict[str, Any]) -> str | None:
    route = route.lower()
    if route == "unknown":
        return "TOPOLOGY_LIFECYCLE_CONFLICT"
    if state == "ACTIVE" and route in {"historical", "temporary", "quarantine", "quarantined"}:
        return "TOPOLOGY_LIFECYCLE_CONFLICT"
    if state == "HISTORICAL" and route == "active":
        return "TOPOLOGY_LIFECYCLE_CONFLICT"
    if state == "TEMPORARY" and route not in {"temporary", "temp", "unknown"}:
        return "TOPOLOGY_LIFECYCLE_CONFLICT"
    if state == "QUARANTINED" and route == "active":
        return "TOPOLOGY_LIFECYCLE_CONFLICT"
    if state == "ORPHANED" and (item.get("governed") is True or item.get("canonical") is True):
        return "TOPOLOGY_LIFECYCLE_CONFLICT"
    return None


def d50_route_class(relative_path: str, audit_routes: dict[str, str]) -> str:
    """Use D5.0's explicit path rules for records added after its audit snapshot."""
    if relative_path in audit_routes:
        return str(audit_routes[relative_path]).lower()
    parts = [part.lower() for part in Path(relative_path).parts]
    if parts and (parts[0] == "docs" and len(parts) > 1 and parts[1] == "history" or any(token in part for part in parts for token in ("historical", "archive"))):
        return "historical"
    if any(part in {"tmp", "temp", "cache", "scratch", "worker"} for part in parts):
        return "temporary"
    if "quarantine" in parts or "quarantined" in parts:
        return "quarantine"
    if parts and ((parts[0] in {"artifacts", "definitions", "tools"}) or parts[:3] == ["docs", "current", "d"]):
        return "active"
    return "unknown"


def normalize_evidence_path(value: str) -> str:
    return value.replace("\\", "/").lstrip("./")


def filesystem_manifest_check(root: Path, manifest: dict[str, Any], d51_receipt: dict[str, Any]) -> tuple[dict[str, Any], dict[str, dict[str, str]], list[dict[str, Any]]]:
    missing: list[dict[str, Any]] = []
    mismatches: list[dict[str, Any]] = []
    details: dict[str, dict[str, str]] = {}
    deferred: list[str] = []
    checked = 0
    manifest_records = {item["artifact_role"]: item for item in manifest["artifacts"]}
    externally_pinned = {
        "d5_1_canonical_manifest": d51_receipt.get("manifest_sha256"),
        "d5_1_manifest_evidence": d51_receipt.get("manifest_evidence_sha256"),
    }
    for item in manifest["artifacts"]:
        for relative in all_locations(item):
            checked += 1
            path = root / Path(relative)
            actual, issue = physical_path_issue(path)
            if issue == "MISSING_PHYSICAL_ARTIFACT":
                missing.append({"artifact_id": item["artifact_id"], "relative_path": relative, "code": "MISSING_PHYSICAL_ARTIFACT"})
                continue
            assert actual is not None
            details.setdefault(item["artifact_id"], {})[relative] = actual
            expected = item.get("content_sha256")
            state = item.get("content_hash_state")
            if state == "VERIFIED" and expected:
                _, issue = physical_path_issue(path, expected)
                if issue == "CONTENT_HASH_MISMATCH":
                    mismatches.append({"artifact_id": item["artifact_id"], "relative_path": relative, "expected_sha256": expected, "actual_sha256": actual, "code": "CONTENT_HASH_MISMATCH"})
            elif state == "GENERATED_AFTER_WRITE":
                pinned = externally_pinned.get(item["artifact_role"])
                if pinned:
                    if actual != pinned:
                        mismatches.append({"artifact_id": item["artifact_id"], "relative_path": relative, "expected_sha256": pinned, "actual_sha256": actual, "code": "CONTENT_HASH_MISMATCH"})
                else:
                    deferred.append(relative)
            else:
                deferred.append(relative)
    # Confirm D5.1's receipt independently pins its two non-circular output hashes.
    manifest_actual = sha_file(root / MANIFEST)
    evidence_path = root / "artifacts/tests/c11d_d5/d5_1/d5_1_manifest_evidence.json"
    if d51_receipt.get("manifest_sha256") != manifest_actual:
        mismatches.append({"artifact_id": manifest_records.get("d5_1_canonical_manifest", {}).get("artifact_id", "UNKNOWN"), "relative_path": MANIFEST, "expected_sha256": d51_receipt.get("manifest_sha256"), "actual_sha256": manifest_actual, "code": "CONTENT_HASH_MISMATCH"})
    if evidence_path.is_file() and d51_receipt.get("manifest_evidence_sha256") != sha_file(evidence_path):
        mismatches.append({"artifact_id": manifest_records.get("d5_1_manifest_evidence", {}).get("artifact_id", "UNKNOWN"), "relative_path": "artifacts/tests/c11d_d5/d5_1/d5_1_manifest_evidence.json", "expected_sha256": d51_receipt.get("manifest_evidence_sha256"), "actual_sha256": sha_file(evidence_path), "code": "CONTENT_HASH_MISMATCH"})
    return {
        "checked": checked,
        "missing": len(missing),
        "hash_mismatches": len(mismatches),
        "hashes_not_declared": len(deferred),
        "deferred_hash_paths": sorted(set(deferred)),
    }, details, missing + mismatches


def identity_check(manifest: dict[str, Any], actual_hashes: dict[str, dict[str, str]]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    mismatches = []
    copy_conflicts = []
    groups: dict[str, set[str]] = defaultdict(set)
    for item in manifest["artifacts"]:
        recomputed = artifact_identity_id(item)
        if recomputed != item["artifact_id"]:
            mismatches.append({"artifact_id": item["artifact_id"], "recomputed_artifact_id": recomputed, "artifact_role": item["artifact_role"], "code": "ARTIFACT_IDENTITY_MISMATCH"})
        groups[item["artifact_id"]].update(actual_hashes.get(item["artifact_id"], {}).values())
    for artifact_id, hashes in sorted(groups.items()):
        conflict = copy_hash_conflict(artifact_id, hashes)
        if conflict:
            copy_conflicts.append(conflict)
    return {"logical_ids": len(groups), "identity_mismatches": len(mismatches), "copy_conflicts": len(copy_conflicts)}, mismatches + copy_conflicts


def lifecycle_check(manifest: dict[str, Any], route_by_path: dict[str, str]) -> tuple[dict[str, int], list[dict[str, Any]]]:
    findings: list[dict[str, Any]] = []
    conflicts = {"active_conflicts": 0, "historical_conflicts": 0, "temporary_conflicts": 0, "quarantined_conflicts": 0, "orphan_state_conflicts": 0}
    for item in manifest["artifacts"]:
        state = item["lifecycle_state"]
        for relative in all_locations(item):
            route = route_by_path.get(relative, "UNKNOWN").lower()
            issue = lifecycle_conflict_code(state, route, item)
            if issue:
                reason = {"ACTIVE": "active_conflicts", "HISTORICAL": "historical_conflicts", "TEMPORARY": "temporary_conflicts", "QUARANTINED": "quarantined_conflicts", "ORPHANED": "orphan_state_conflicts"}[state]
                conflicts[reason] += 1
                findings.append({"artifact_id": item["artifact_id"], "relative_path": relative, "lifecycle_state": state, "route_class": route, "code": issue})
    return conflicts, findings


def lineage_check(manifest: dict[str, Any], registry: dict[str, Any], root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    manifest_ids = {item["artifact_id"] for item in manifest["artifacts"]}
    node_ids = [node["artifact_id"] for node in registry.get("nodes", [])]
    node_set = set(node_ids)
    findings: list[dict[str, Any]] = []
    unknown_nodes = sorted(node_set - manifest_ids)
    missing_nodes = sorted(manifest_ids - node_set)
    for artifact_id in unknown_nodes:
        findings.append({"artifact_id": artifact_id, "code": "UNKNOWN_LINEAGE_NODE"})
    for artifact_id in missing_nodes:
        findings.append({"artifact_id": artifact_id, "code": "MANIFEST_NODE_MISSING_FROM_LINEAGE"})
    unknown_sources = 0
    unknown_targets = 0
    missing_evidence = 0
    for edge in registry.get("edges", []):
        if edge.get("source_artifact_id") not in manifest_ids:
            unknown_sources += 1
            findings.append({"edge_id": edge.get("edge_id"), "source_artifact_id": edge.get("source_artifact_id"), "code": "UNKNOWN_LINEAGE_SOURCE"})
        if invalid_edge_target(edge, manifest_ids):
            unknown_targets += 1
            findings.append({"edge_id": edge.get("edge_id"), "target_artifact_id": edge.get("target_artifact_id"), "code": "UNKNOWN_LINEAGE_TARGET"})
        evidence = edge.get("evidence") or {}
        evidence_id = evidence.get("source_artifact_id")
        evidence_node = next((n for n in registry.get("nodes", []) if n.get("artifact_id") == evidence_id), None)
        ev_path = normalize_evidence_path(str(evidence.get("source_path", "")))
        known_locations = {normalize_evidence_path(loc) for item in manifest["artifacts"] if item["artifact_id"] == evidence_id for loc in all_locations(item)}
        if evidence_id not in manifest_ids or ev_path not in known_locations or not ev_path or not (root / Path(ev_path)).is_file():
            missing_evidence += 1
            findings.append({"edge_id": edge.get("edge_id"), "evidence_artifact_id": evidence_id, "source_path": ev_path, "code": "EDGE_EVIDENCE_MISSING"})
        if evidence_node is None or evidence.get("source_type") not in EVIDENCE_TYPES:
            missing_evidence += 1
            findings.append({"edge_id": edge.get("edge_id"), "evidence_artifact_id": evidence_id, "code": "EDGE_EVIDENCE_INVALID"})
    result = {
        "nodes_checked": len(registry.get("nodes", [])),
        "edges_checked": len(registry.get("edges", [])),
        "unknown_sources": unknown_sources,
        "unknown_targets": unknown_targets,
        "missing_manifest_nodes": len(missing_nodes),
        "unknown_lineage_nodes": len(unknown_nodes),
        "missing_evidence": missing_evidence,
        "dag_valid": registry.get("validation", {}).get("dag_valid") is True,
    }
    return result, findings


def has_edge(edges: list[dict[str, Any]], source: str, relation: str, target: str, checkpoint: str | None = None) -> bool:
    return any(e.get("source_artifact_id") == source and e.get("relation") == relation and e.get("target_artifact_id") == target and (checkpoint is None or (e.get("evidence") or {}).get("source_checkpoint") == checkpoint) for e in edges)


def phase_checks(root: Path, manifest: dict[str, Any], registry: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    by_role = {item["artifact_role"]: item for item in manifest["artifacts"]}
    nodes = {node["artifact_id"]: node for node in registry.get("nodes", [])}
    edges = registry.get("edges", [])
    findings: list[dict[str, Any]] = []

    raw = by_role.get("d3_raw_deterministic_render")
    master = by_role.get("d3_delivery_master")
    d33_receipt = next((item for item in manifest["artifacts"] if item["relative_path"].endswith("d3_3_validation_receipt.json")), None)
    d32_receipt = next((item for item in manifest["artifacts"] if item["relative_path"].endswith("d3_2_validation_receipt.json")), None)
    d3_raw_master = bool(raw and master and raw["artifact_id"] != master["artifact_id"])
    d3_derivation = bool(raw and master and has_edge(edges, master["artifact_id"], "DERIVED_FROM", raw["artifact_id"], "C11-D D3.3"))
    d3_master_qa = bool(master and d33_receipt and has_edge(edges, master["artifact_id"], "VALIDATED_BY", d33_receipt["artifact_id"], "C11-D D3.3"))
    d3_raw_qa = bool(raw and d32_receipt and has_edge(edges, raw["artifact_id"], "VALIDATED_BY", d32_receipt["artifact_id"], "C11-D D3.2"))
    d3_consistent = d3_raw_master and d3_derivation and d3_master_qa and d3_raw_qa
    if not d3_consistent:
        findings.append({"code": "D3_LINEAGE_INCONSISTENT", "raw": d3_raw_master, "master_from_raw": d3_derivation, "master_validated_by_d33": d3_master_qa, "raw_validated_by_d32": d3_raw_qa})

    plans = [item for item in manifest["artifacts"] if item["artifact_type"] == "PLAN"]
    requests = [item for item in manifest["artifacts"] if item["artifact_type"] == "REQUEST"]
    request_plan_edges = [e for e in edges if e.get("relation") == "GENERATED_FROM" and e.get("source_artifact_id") in {p["artifact_id"] for p in plans} and e.get("target_artifact_id") in {r["artifact_id"] for r in requests}]
    manifest_request_plan = manifest.get("lineage", {}).get("request_to_plan_edges", [])
    request_plan_consistent = bool(manifest.get("lineage", {}).get("request_to_plan") and manifest_request_plan and len(request_plan_edges) >= len(manifest_request_plan))
    authorization = next((item for item in manifest["artifacts"] if item["artifact_type"] == "AUTHORIZATION"), None)
    auth_node = nodes.get(authorization["artifact_id"]) if authorization else None
    governance_edge = bool(authorization and any(e.get("source_artifact_id") == authorization["artifact_id"] and e.get("relation") == "GENERATED_FROM" and e.get("target_artifact_id") in {p["artifact_id"] for p in plans} and (e.get("evidence") or {}).get("source_checkpoint") == "C11-D D4.9" for e in edges))
    auth_data = read_json(root / Path(authorization["relative_path"])) if authorization and (root / Path(authorization["relative_path"])).is_file() else {}
    blocked_auth_preserved = bool(
        all(case.get("authorized") is False for case in auth_data.get("authorization_cases", []) if case.get("case", "").startswith("valid_production"))
        and auth_data.get("renderer_policy") == "DISABLED"
        and "RENDERER_POLICY_DISABLED" in auth_data.get("production_blocked_reasons", [])
        and auth_node
        and auth_node.get("decision_context", {}).get("decision") == "BLOCKED"
        and auth_node.get("decision_context", {}).get("authorized") is False
        and auth_node.get("decision_context", {}).get("reason") == "RENDERER_POLICY_DISABLED"
        and not any(e.get("relation") == "AUTHORIZED_BY" and e.get("target_artifact_id") == authorization["artifact_id"] for e in edges)
    )
    d49_receipt = next((item for item in manifest["artifacts"] if item["relative_path"].endswith("d4_9_validation_receipt.json")), None)
    d49_data = read_json(root / Path(d49_receipt["relative_path"])) if d49_receipt and (root / Path(d49_receipt["relative_path"])).is_file() else {}
    acceptance_edge = bool(d49_receipt and any(e.get("relation") == "VALIDATED_BY" and e.get("target_artifact_id") == d49_receipt["artifact_id"] and e.get("source_artifact_id") in {p["artifact_id"] for p in plans} for e in edges))
    acceptance_consistent = bool(d49_data.get("checkpoint") == "C11-D D4.9" and d49_data.get("result") == "PASS" and d49_data.get("status") == "CLOSED" and acceptance_edge)
    d4_consistent = request_plan_consistent and governance_edge and blocked_auth_preserved and acceptance_consistent
    if not request_plan_consistent:
        findings.append({"code": "D4_REQUEST_PLAN_INCONSISTENT"})
    if not governance_edge:
        findings.append({"code": "D4_GOVERNANCE_LINEAGE_INCONSISTENT"})
    if not blocked_auth_preserved:
        findings.append({"code": "D4_BLOCKED_AUTHORIZATION_NOT_PRESERVED"})
    if not acceptance_consistent:
        findings.append({"code": "D4_ACCEPTANCE_LINEAGE_INCONSISTENT"})

    orphan_items = [item for item in manifest["artifacts"] if item["lifecycle_state"] == "ORPHANED"]
    orphan_index = {row.get("artifact_id"): row for row in registry.get("orphan_nodes", [])}
    orphan_consistent = len(orphan_items) == 9 and all(
        not item.get("governed") and not item.get("canonical")
        and item["artifact_id"] in orphan_index
        and orphan_index[item["artifact_id"]].get("lineage_status") == "ORPHANED"
        and not orphan_index[item["artifact_id"]].get("parents")
        and orphan_index[item["artifact_id"]].get("cleanup_authority") == "NONE"
        for item in orphan_items
    )
    unmanaged_count = int(manifest.get("unmanaged_inventory", {}).get("orphan_candidates", 0))
    global_not_promoted = unmanaged_count == 12304 and registry.get("statistics", {}).get("global_unmanaged_candidates") == unmanaged_count and registry.get("statistics", {}).get("logical_nodes") == len(manifest["artifacts"])
    if not orphan_consistent:
        findings.append({"code": "ORPHAN_GOVERNANCE_INCONSISTENT"})
    if not global_not_promoted:
        findings.append({"code": "GLOBAL_UNMANAGED_CANDIDATES_PROMOTED_OR_CHANGED"})
    return {
        "d3": {"raw_master_consistency": d3_consistent, "raw_exists_in_manifest": bool(raw), "master_exists_in_manifest": bool(master), "raw_and_master_distinct": d3_raw_master, "master_provenance_to_raw": d3_derivation, "master_validated_by_d33": d3_master_qa, "raw_validated_by_d32": d3_raw_qa},
        "d4": {"request_plan_consistency": request_plan_consistent, "request_plan_edges_checked": len(request_plan_edges), "governance_consistency": governance_edge, "blocked_authorization_preserved": blocked_auth_preserved, "acceptance_consistency": acceptance_consistent},
        "governance": {"governed_active": sum(1 for item in manifest["artifacts"] if item["governed"] and item["lifecycle_state"] == "ACTIVE"), "orphaned_nodes": len(orphan_items), "orphan_nodes_valid": orphan_consistent, "global_unmanaged_candidates": unmanaged_count, "global_candidates_not_promoted": global_not_promoted, "cleanup_performed": False},
    }, findings


def negative_tests() -> dict[str, bool]:
    # Temporary fixtures live outside repository artifact routes and are removed by the context manager.
    with tempfile.TemporaryDirectory(prefix="c11d_d5_3_topology_") as temp_dir:
        temp = Path(temp_dir)
        absent_path = temp / "does_not_exist.json"
        _, missing_code = physical_path_issue(absent_path)
        missing_detected = missing_code == "MISSING_PHYSICAL_ARTIFACT"

        hash_fixture = temp / "hash_fixture.bin"
        hash_fixture.write_bytes(b"fixture-content-B")
        expected_a = sha_bytes(b"fixture-content-A")
        _, hash_code = physical_path_issue(hash_fixture, expected_a)
        hash_mismatch_detected = hash_code == "CONTENT_HASH_MISMATCH"

        copy_a = sha_bytes(b"copy-A")
        copy_b = sha_bytes(b"copy-B")
        identity_content_conflict_detected = copy_hash_conflict("artifact-X", {copy_a, copy_b}) is not None

        known_ids = {"artifact-X"}
        invalid_target = "DOES_NOT_EXIST"
        unknown_target_detected = invalid_edge_target({"target_artifact_id": invalid_target}, known_ids)

        synthetic_route = "historical"
        synthetic_state = "ACTIVE"
        lifecycle_conflict_detected = lifecycle_conflict_code(synthetic_state, synthetic_route, {"governed": True, "canonical": True}) == "TOPOLOGY_LIFECYCLE_CONFLICT"
    return {
        "missing_physical_artifact_detected": missing_detected,
        "content_hash_mismatch_detected": hash_mismatch_detected,
        "identity_content_conflict_detected": identity_content_conflict_detected,
        "unknown_lineage_target_detected": unknown_target_detected,
        "lifecycle_conflict_detected": lifecycle_conflict_detected,
    }


def validate_inputs(root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    audit_path = root / "artifacts/tests/c11d_d5/d5_0/d5_0_artifact_topology_audit.json"
    manifest_path = root / MANIFEST
    registry_path = root / REGISTRY
    d50_receipt = read_json(root / "artifacts/tests/c11d_d5/d5_0/d5_0_validation_receipt.json")
    d51_receipt = read_json(root / "artifacts/tests/c11d_d5/d5_1/d5_1_validation_receipt.json")
    d52_receipt = read_json(root / "artifacts/tests/c11d_d5/d5_2/d5_2_validation_receipt.json")
    audit = read_json(audit_path)
    manifest = read_json(manifest_path)
    registry = read_json(registry_path)
    if (d50_receipt.get("result"), d50_receipt.get("status")) != ("PASS", "CLOSED"):
        raise ValueError("D5.0 audit receipt must be PASS/CLOSED.")
    if (d51_receipt.get("result"), d51_receipt.get("status")) != ("PASS", "CLOSED") or d51_receipt.get("manifest_sha256") != sha_file(manifest_path):
        raise ValueError("D5.1 manifest receipt is not PASS/CLOSED or its manifest hash does not match.")
    if (d52_receipt.get("result"), d52_receipt.get("status")) != ("PASS", "CLOSED") or d52_receipt.get("registry_sha256") != sha_file(registry_path):
        raise ValueError("D5.2 lineage receipt is not PASS/CLOSED or its registry hash does not match.")
    if manifest.get("source_audit", {}).get("audit_sha256") != sha_file(audit_path):
        raise ValueError("D5.1 manifest does not identify the current D5.0 audit bytes.")
    if registry.get("node_source", {}).get("manifest_sha256") != sha_file(manifest_path):
        raise ValueError("D5.2 registry does not identify the current D5.1 manifest bytes.")
    return audit, manifest, registry, d51_receipt, d52_receipt


def build_outputs(root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    audit, manifest, registry, d51_receipt, d52_receipt = validate_inputs(root)
    topology, actual_hashes, physical_findings = filesystem_manifest_check(root, manifest, d51_receipt)
    identity, identity_findings = identity_check(manifest, actual_hashes)
    audit_route_raw = {item.get("relative_path", ""): item.get("route_class", "UNKNOWN") for item in audit.get("artifacts", [])}
    audit_route = {relative: d50_route_class(relative, audit_route_raw) for item in manifest["artifacts"] for relative in all_locations(item)}
    route_check, route_findings = lifecycle_check(manifest, audit_route)
    lineage, lineage_findings = lineage_check(manifest, registry, root)
    phase, phase_findings = phase_checks(root, manifest, registry)
    synthetic = negative_tests()
    frozen = root / "artifacts/releases/ChallengeEngineV01_STATELESS_C11-C_2.19.12_FROZEN_20260930_175709.zip"
    frozen_ok = frozen.is_file() and sha_file(frozen) == FROZEN_SHA256

    topology_conflicts = [*physical_findings, *identity_findings, *route_findings, *lineage_findings, *phase_findings]
    known_inputs_ok = audit.get("result") == "PASS" and audit.get("status") == "CLOSED" and audit.get("topology_conflicts") == [] and audit.get("unclassified_active_artifacts") == []
    pass_gate = (
        known_inputs_ok and topology["checked"] == 79 and topology["missing"] == 0 and topology["hash_mismatches"] == 0
        and identity["logical_ids"] == 75 and identity["identity_mismatches"] == 0 and identity["copy_conflicts"] == 0
        and sum(route_check.values()) == 0 and lineage["nodes_checked"] == 75 and lineage["edges_checked"] == 11
        and lineage["unknown_sources"] == 0 and lineage["unknown_targets"] == 0 and lineage["missing_manifest_nodes"] == 0
        and lineage["unknown_lineage_nodes"] == 0 and lineage["missing_evidence"] == 0 and lineage["dag_valid"]
        and phase["d3"]["raw_master_consistency"] and phase["d4"]["request_plan_consistency"]
        and phase["d4"]["governance_consistency"] and phase["d4"]["blocked_authorization_preserved"]
        and phase["d4"]["acceptance_consistency"] and phase["governance"]["governed_active"] == 66
        and phase["governance"]["orphaned_nodes"] == 9 and phase["governance"]["orphan_nodes_valid"]
        and phase["governance"]["global_candidates_not_promoted"] and all(synthetic.values()) and frozen_ok
        and registry.get("runtime_authority") == "NONE" and registry.get("production_execution") is False
        and d52_receipt.get("files_moved") is False and d52_receipt.get("files_deleted") is False and d52_receipt.get("cleanup_performed") is False
    )
    findings = sorted(topology_conflicts, key=lambda row: (row.get("code", ""), row.get("artifact_id", ""), row.get("relative_path", ""), row.get("edge_id", "")))
    result = "PASS" if pass_gate else "BLOCKED"
    matrix = {
        "checkpoint": "C11-D D5.3",
        "result": result,
        "status": "CLOSED" if pass_gate else "BLOCKED",
        "filesystem_manifest": topology,
        "identity": identity,
        "lifecycle": route_check,
        "lineage": lineage,
        "d3": phase["d3"],
        "d4": phase["d4"],
        "governance": phase["governance"],
        "findings": findings,
        "runtime_authority": "NONE",
        "production_execution": False,
    }
    matrix_hash = sha_bytes(json_bytes(matrix))
    validation = {
        "checkpoint": "C11-D D5.3",
        "result": result,
        "status": "CLOSED" if pass_gate else "BLOCKED",
        "input_audit": {"path": "artifacts/tests/c11d_d5/d5_0/d5_0_artifact_topology_audit.json", "sha256": sha_file(root / "artifacts/tests/c11d_d5/d5_0/d5_0_artifact_topology_audit.json")},
        "input_manifest": {"path": MANIFEST, "sha256": sha_file(root / MANIFEST)},
        "input_lineage": {"path": REGISTRY, "sha256": sha_file(root / REGISTRY)},
        "filesystem_manifest": topology,
        "identity": identity,
        "lifecycle": route_check,
        "lineage": lineage,
        "phase_gates": phase,
        "synthetic_negative_tests": synthetic,
        "frozen_c11c_sha256": FROZEN_SHA256 if frozen_ok else "MISMATCH",
        "files_moved": False,
        "files_deleted": False,
        "cleanup_performed": False,
        "runtime_authority": "NONE",
        "production_execution": False,
        "next": "D5.4 - Artifact Lifecycle / Quarantine Rules",
    }
    validation["consistency_matrix_sha256"] = matrix_hash
    validation["topology_conflicts"] = len(findings)
    topology_output = {
        **validation,
        "consistency_matrix": "artifacts/tests/c11d_d5/d5_3/d5_3_consistency_matrix.json",
    }
    receipt = {
        "checkpoint": "C11-D D5.3",
        "result": result,
        "status": "CLOSED" if pass_gate else "BLOCKED",
        "filesystem_manifest_consistent": topology["missing"] == 0 and topology["hash_mismatches"] == 0,
        "manifest_identity_consistent": identity["identity_mismatches"] == 0 and identity["copy_conflicts"] == 0,
        "manifest_lineage_consistent": lineage["unknown_sources"] == 0 and lineage["unknown_targets"] == 0 and lineage["missing_manifest_nodes"] == 0 and lineage["unknown_lineage_nodes"] == 0 and lineage["dag_valid"],
        "lifecycle_consistent": sum(route_check.values()) == 0,
        "evidence_consistent": lineage["missing_evidence"] == 0,
        "logical_identities": identity["logical_ids"],
        "physical_locations": topology["checked"],
        "lineage_edges": lineage["edges_checked"],
        "orphaned_nodes": phase["governance"]["orphaned_nodes"],
        "governed_active": phase["governance"]["governed_active"],
        "global_unmanaged_candidates": phase["governance"]["global_unmanaged_candidates"],
        "d3_consistency": phase["d3"]["raw_master_consistency"],
        "d4_consistency": phase["d4"]["request_plan_consistency"] and phase["d4"]["governance_consistency"] and phase["d4"]["acceptance_consistency"] and phase["d4"]["blocked_authorization_preserved"],
        "synthetic_negative_tests": synthetic,
        "idempotency": True,
        "topology_conflicts": len(findings),
        "missing_artifacts": topology["missing"],
        "hash_mismatches": topology["hash_mismatches"],
        "hashes_not_declared": topology["hashes_not_declared"],
        "identity_conflicts": identity["identity_mismatches"] + identity["copy_conflicts"],
        "lifecycle_conflicts": sum(route_check.values()),
        "unknown_lineage_targets": lineage["unknown_targets"],
        "consistency_matrix_sha256": matrix_hash,
        "files_moved": False,
        "files_deleted": False,
        "cleanup_performed": False,
        "frozen_c11c_preserved": frozen_ok,
        "runtime_authority": "NONE",
        "production_execution": False,
        "next": "D5.4 - Artifact Lifecycle / Quarantine Rules",
    }
    return topology_output, matrix, receipt


def write_outputs(root: Path, values: tuple[dict[str, Any], dict[str, Any], dict[str, Any]]) -> dict[str, str]:
    names = ["d5_3_topology_validation.json", "d5_3_consistency_matrix.json", "d5_3_validation_receipt.json"]
    hashes = {}
    for name, value in zip(names, values):
        path = root / OUTPUTS / name
        stable_write(path, value)
        hashes[name] = sha_file(path)
    return hashes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    args = parser.parse_args()
    root = args.root.resolve()
    first = build_outputs(root)
    hashes_a = write_outputs(root, first)
    second = build_outputs(root)
    hashes_b = write_outputs(root, second)
    idempotent = hashes_a == hashes_b
    receipt_path = root / OUTPUTS / "d5_3_validation_receipt.json"
    receipt = read_json(receipt_path)
    receipt["idempotency"] = idempotent
    stable_write(receipt_path, receipt)
    print(json.dumps({"result": receipt["result"] if idempotent else "BLOCKED", "status": receipt["status"] if idempotent else "BLOCKED", "logical_identities": receipt["logical_identities"], "physical_locations": receipt["physical_locations"], "lineage_edges": receipt["lineage_edges"], "missing_artifacts": receipt["missing_artifacts"], "hash_mismatches": receipt["hash_mismatches"], "topology_conflicts": receipt["topology_conflicts"], "idempotency": idempotent}, indent=2))
    return 0 if receipt["result"] == "PASS" and idempotent else 2


if __name__ == "__main__":
    raise SystemExit(main())
