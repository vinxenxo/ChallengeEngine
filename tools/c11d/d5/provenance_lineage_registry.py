#!/usr/bin/env python3
"""Build the D5.2 evidence-backed provenance graph from the D5.1 manifest."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

RELATIONS = ["DERIVED_FROM", "GENERATED_FROM", "AUTHORIZED_BY", "VALIDATED_BY", "DOCUMENTED_BY", "SNAPSHOT_OF"]
FROZEN_SHA256 = "d85425cf18c5211c8497574f4fc66202d613eacc0ec14cd4e2fef0b24f634a32"
MANIFEST_PATH = "artifacts/tests/c11d_d5/d5_1/d5_1_canonical_artifact_manifest.json"


def json_bytes(data: Any) -> bytes:
    return (json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")


def canonical_bytes(data: Any) -> bytes:
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


def first_path(node: dict[str, Any]) -> str:
    locations = node.get("locations", [])
    return locations[0] if locations else "UNKNOWN"


def read_location(root: Path, node: dict[str, Any]) -> Any:
    for location in node.get("locations", []):
        path = root / location
        if path.suffix.lower() == ".json" and path.is_file():
            try:
                return read_json(path)
            except (OSError, UnicodeError, json.JSONDecodeError):
                pass
    return None


def checkpoint_for(data: Any) -> str:
    return str(data.get("checkpoint", "UNKNOWN")) if isinstance(data, dict) else "UNKNOWN"


def nodes_from_manifest(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    nodes = []
    for item in manifest.get("artifacts", []):
        locations = sorted(set([item["relative_path"], *item.get("alternate_relative_paths", [])]))
        node = {
            "artifact_id": item["artifact_id"],
            "artifact_type": item["artifact_type"],
            "artifact_role": item["artifact_role"],
            "lifecycle_state": item["lifecycle_state"],
            "canonical": bool(item["canonical"]),
            "governed": bool(item["governed"]),
            "locations": locations,
            "parent_artifact_ids": sorted(set(item.get("parent_artifact_ids", []))),
            "lineage_status": "ORPHANED" if item["lifecycle_state"] == "ORPHANED" else "UNCLASSIFIED",
        }
        nodes.append(node)
    nodes.sort(key=lambda node: node["artifact_id"])
    return nodes


def node_maps(nodes: list[dict[str, Any]]) -> tuple[dict[str, dict[str, Any]], dict[str, str]]:
    by_id = {node["artifact_id"]: node for node in nodes}
    by_path = {location: node["artifact_id"] for node in nodes for location in node["locations"]}
    return by_id, by_path


def evidence_source(node: dict[str, Any], data: Any, claim: str) -> dict[str, Any]:
    source_types = {"VALIDATION_RECEIPT": "receipt", "EVIDENCE": "evidence", "PROVENANCE": "evidence", "MANIFEST": "manifest", "REPORT": "evidence", "AUTHORIZATION": "evidence"}
    if isinstance(data, dict) and ("hash_integrity" in data or ("governance" in data and "checkpoints" in data)):
        source_type = "evidence"
    elif isinstance(data, dict) and "validation_receipt" in first_path(node):
        source_type = "receipt"
    else:
        source_type = source_types.get(node["artifact_type"], "evidence")
    return {
        "source_type": source_type,
        "source_artifact_id": node["artifact_id"],
        "source_checkpoint": checkpoint_for(data),
        "source_path": first_path(node),
        "claim": claim,
    }


def edge_id(source: str, relation: str, target: str, evidence_id: str) -> str:
    return sha_bytes(canonical_bytes({"source_artifact_id": source, "relation": relation, "target_artifact_id": target, "evidence_artifact_id": evidence_id}))


def make_edge(source: dict[str, Any], relation: str, target: dict[str, Any], evidence_node: dict[str, Any], evidence_data: Any, claim: str) -> dict[str, Any]:
    evidence_ref = evidence_source(evidence_node, evidence_data, claim)
    return {
        "edge_id": edge_id(source["artifact_id"], relation, target["artifact_id"], evidence_node["artifact_id"]),
        "source_artifact_id": source["artifact_id"],
        "target_artifact_id": target["artifact_id"],
        "relation": relation,
        "evidence": evidence_ref,
        "confidence": "EVIDENCE_BACKED",
    }


def has_reported_sha(value: Any, expected: str) -> bool:
    if isinstance(value, dict):
        if any(isinstance(v, str) and v.lower() == expected.lower() for k, v in value.items() if "hash" in k.lower() or "sha256" in k.lower()):
            return True
        return any(has_reported_sha(v, expected) for v in value.values())
    if isinstance(value, list):
        return any(has_reported_sha(v, expected) for v in value)
    return False


def receipt_by_checkpoint(root: Path, nodes: list[dict[str, Any]], checkpoint: str) -> tuple[dict[str, Any] | None, Any]:
    for node in nodes:
        if not any("validation_receipt.json" in location for location in node["locations"]):
            continue
        data = read_location(root, node)
        if checkpoint_for(data) == checkpoint and isinstance(data, dict):
            return node, data
    return None, None


def detect_cycle(node_ids: set[str], edges: list[dict[str, Any]]) -> bool:
    adjacency: dict[str, list[str]] = {node_id: [] for node_id in node_ids}
    for edge in edges:
        adjacency[edge["source_artifact_id"]].append(edge["target_artifact_id"])
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node_id: str) -> bool:
        if node_id in visiting:
            return True
        if node_id in visited:
            return False
        visiting.add(node_id)
        for target in sorted(adjacency[node_id]):
            if visit(target):
                return True
        visiting.remove(node_id)
        visited.add(node_id)
        return False

    return any(visit(node_id) for node_id in sorted(node_ids) if node_id not in visited)


def validate_edges(nodes: list[dict[str, Any]], candidates: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    node_ids = {node["artifact_id"] for node in nodes}
    accepted, invalid = [], []
    for edge in candidates:
        missing = []
        if edge["source_artifact_id"] not in node_ids:
            missing.append("source_artifact_id")
        if edge["target_artifact_id"] not in node_ids:
            missing.append("target_artifact_id")
        evidence_id = edge.get("evidence", {}).get("source_artifact_id")
        if evidence_id not in node_ids:
            missing.append("evidence.source_artifact_id")
        if edge["relation"] not in RELATIONS:
            missing.append("relation")
        if missing:
            invalid.append({"edge_id": edge.get("edge_id", "UNKNOWN"), "reason": "INVALID_EDGE", "missing_references": sorted(missing)})
        else:
            accepted.append(edge)
    accepted.sort(key=lambda edge: edge["edge_id"])
    invalid.sort(key=lambda edge: edge["edge_id"])
    return accepted, invalid


def build_graph(root: Path, manifest: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    nodes = nodes_from_manifest(manifest)
    by_id, by_path = node_maps(nodes)
    item_by_id = {item["artifact_id"]: item for item in manifest["artifacts"]}
    data_by_id = {node["artifact_id"]: read_location(root, node) for node in nodes}
    candidates: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []

    # A raw render's hash must be named in D3.2 evidence before its QA edge is accepted.
    raw = next((node for node in nodes if node["artifact_role"] in {"d3_raw_deterministic_render", "d3_raw_render"}), None)
    master = next((node for node in nodes if node["artifact_role"] == "d3_delivery_master"), None)
    d32_receipt, d32_data = receipt_by_checkpoint(root, nodes, "C11-D D3.2")
    d33_receipt, d33_data = receipt_by_checkpoint(root, nodes, "C11-D D3.3")
    if raw and d32_receipt and has_reported_sha(d32_data, item_by_id[raw["artifact_id"]].get("content_sha256", "")):
        candidates.append(make_edge(raw, "VALIDATED_BY", d32_receipt, d32_receipt, d32_data, "D3.2 receipt render output hash equals the manifest raw media content_sha256"))
    if raw and master and d33_receipt and isinstance(d33_data, dict):
        raw_location = item_by_id[raw["artifact_id"]]["relative_path"]
        master_location = item_by_id[master["artifact_id"]]["relative_path"]
        declared_raw = Path(str(d33_data.get("source_render", "")))
        declared_master = Path(str(d33_data.get("delivery_master", "")))
        raw_resolves = declared_raw.resolve() == (root / raw_location).resolve()
        master_resolves = declared_master.resolve() == (root / master_location).resolve()
        if raw_resolves and master_resolves and d33_data.get("result") == "PASS" and d33_data.get("status") == "CLOSED":
            candidates.append(make_edge(master, "DERIVED_FROM", raw, d33_receipt, d33_data, "D3.3 receipt declares source_render and delivery_master physical locations"))
            candidates.append(make_edge(master, "VALIDATED_BY", d33_receipt, d33_receipt, d33_data, "D3.3 receipt reports PASS/CLOSED and names the delivery master"))

    # D5.1 parent IDs are manifest evidence for direct request-to-plan relationships.
    manifest_node = next((node for node in nodes if node["artifact_role"] == "d5_1_canonical_manifest"), None)
    if manifest_node:
        for node in nodes:
            if node["artifact_type"] == "PLAN":
                for parent_id in node["parent_artifact_ids"]:
                    if parent_id in by_id and by_id[parent_id]["artifact_type"] == "REQUEST":
                        candidates.append(make_edge(node, "GENERATED_FROM", by_id[parent_id], manifest_node, manifest, "D5.1 manifest parent_artifact_ids, derived from exact request_id equality"))

    # D4.8 is a blocked decision artifact. D4.9 hash-integrity evidence proves its relation to the D4.6 plan.
    acceptance_node = next((node for node in nodes if node["artifact_role"].startswith("c11_d_d4_9_") and node["artifact_type"] in {"EVIDENCE", "REPORT"} and any("d4_9_regression_evidence.json" in location for location in node["locations"])), None)
    acceptance_data = data_by_id.get(acceptance_node["artifact_id"]) if acceptance_node else None
    auth_node = next((node for node in nodes if node["artifact_type"] == "AUTHORIZATION"), None)
    plan_auth_refs = manifest.get("lineage", {}).get("plan_to_authorization_edges", [])
    if auth_node and acceptance_node and isinstance(acceptance_data, dict):
        auth_refs = [row for row in plan_auth_refs if row.get("to_artifact_id") == auth_node["artifact_id"]]
        for row in auth_refs:
            plan_node = by_id.get(row.get("from_artifact_id"))
            checks = acceptance_data.get("hash_integrity", {})
            if plan_node and checks.get("d48_plan_identity_matches_d46") is True and checks.get("d48_authorization_hash_linked") is True:
                auth_data = data_by_id.get(auth_node["artifact_id"])
                if isinstance(auth_data, dict):
                    auth_node["decision_context"] = {"decision": "BLOCKED", "authorized": False, "reason": "RENDERER_POLICY_DISABLED", "renderer_policy": auth_data.get("renderer_policy", "UNKNOWN")}
                candidates.append(make_edge(auth_node, "GENERATED_FROM", plan_node, acceptance_node, acceptance_data, "D4.9 hash_integrity confirms D4.8 plan identity and authorization hash link"))
                d49_receipt, d49_data = receipt_by_checkpoint(root, nodes, "C11-D D4.9")
                if d49_receipt:
                    candidates.append(make_edge(plan_node, "VALIDATED_BY", d49_receipt, acceptance_node, acceptance_data, "D4.9 acceptance evidence validates D4.6 plan identity through D4.8 hash links"))
                unresolved.append({"candidate_source_artifact_id": plan_node["artifact_id"], "candidate_target_artifact_id": auth_node["artifact_id"], "relation": "AUTHORIZED_BY", "reason": "authorization artifact records a blocked decision; renderer policy is DISABLED and production_authorization is false", "status": "UNRESOLVED"})

    # D5.1's own output hashes form evidence-backed links without self-hashing the registry.
    source_audit = manifest.get("source_audit", {})
    d50_node = next((node for node in nodes if node["artifact_role"] == "d5_0_topology_audit"), None)
    d51_evidence = next((node for node in nodes if node["artifact_role"] == "d5_1_manifest_evidence"), None)
    d51_receipt = next((node for node in nodes if node["artifact_role"] == "d5_1_validation_receipt"), None)
    evidence_data = data_by_id.get(d51_evidence["artifact_id"]) if d51_evidence else None
    receipt_data = data_by_id.get(d51_receipt["artifact_id"]) if d51_receipt else None
    if manifest_node and d50_node and source_audit.get("audit_sha256") and has_reported_sha(source_audit, source_audit["audit_sha256"]):
        candidates.append(make_edge(manifest_node, "GENERATED_FROM", d50_node, manifest_node, manifest, "D5.1 source_audit records the D5.0 audit SHA-256"))
    if manifest_node and d51_evidence and isinstance(evidence_data, dict) and evidence_data.get("manifest_sha256") == sha_file(root / MANIFEST_PATH):
        candidates.append(make_edge(d51_evidence, "GENERATED_FROM", manifest_node, d51_evidence, evidence_data, "D5.1 evidence manifest_sha256 matches canonical manifest bytes"))
    if manifest_node and d51_receipt and isinstance(receipt_data, dict):
        manifest_ok = receipt_data.get("manifest_sha256") == sha_file(root / MANIFEST_PATH)
        evidence_ok = receipt_data.get("manifest_evidence_sha256") == sha_file(root / "artifacts/tests/c11d_d5/d5_1/d5_1_manifest_evidence.json")
        if manifest_ok:
            candidates.append(make_edge(manifest_node, "VALIDATED_BY", d51_receipt, d51_receipt, receipt_data, "D5.1 receipt manifest_sha256 matches canonical manifest bytes"))
        if evidence_ok:
            candidates.append(make_edge(d51_evidence, "VALIDATED_BY", d51_receipt, d51_receipt, receipt_data, "D5.1 receipt manifest_evidence_sha256 matches evidence bytes"))

    # Unknown relations stay unresolved and never enter accepted edges.
    candidates, invalid_edges = validate_edges(nodes, candidates)
    cycles = detect_cycle(set(by_id), candidates)
    incoming = {node_id: [] for node_id in by_id}
    outgoing = {node_id: [] for node_id in by_id}
    parents_index = {node_id: [] for node_id in by_id}
    children_index = {node_id: [] for node_id in by_id}
    for edge in candidates:
        incoming[edge["target_artifact_id"]].append(edge["source_artifact_id"])
        outgoing[edge["source_artifact_id"]].append(edge["target_artifact_id"])
        parents_index[edge["source_artifact_id"]].append({"artifact_id": edge["target_artifact_id"], "relation": edge["relation"], "edge_id": edge["edge_id"]})
        children_index[edge["target_artifact_id"]].append({"artifact_id": edge["source_artifact_id"], "relation": edge["relation"], "edge_id": edge["edge_id"]})
    roots = []
    orphan_nodes = []
    for node in nodes:
        if node["lifecycle_state"] == "ORPHANED":
            node["lineage_status"] = "ORPHANED"
            orphan_nodes.append({"artifact_id": node["artifact_id"], "lineage_status": "ORPHANED", "parents": sorted(parents_index[node["artifact_id"]], key=lambda x: (x["artifact_id"], x["relation"])), "cleanup_authority": "NONE"})
        elif not parents_index[node["artifact_id"]]:
            node["lineage_status"] = "ROOT"
            roots.append(node["artifact_id"])
        else:
            node["lineage_status"] = "LINKED"
    for mapping in (parents_index, children_index):
        for key in mapping:
            mapping[key].sort(key=lambda x: (x["artifact_id"], x["relation"], x["edge_id"]))

    d3_edges = [edge for edge in candidates if edge["evidence"].get("source_checkpoint") in {"C11-D D3.2", "C11-D D3.3"}]
    d4_edges = [edge for edge in candidates if edge["evidence"].get("source_checkpoint") in {"C11-D D4.9"}]
    locations_count = sum(len(node["locations"]) for node in nodes)
    registry = {
        "registry_id": "c11d_provenance_lineage",
        "registry_version": "1.0",
        "status": "ACTIVE",
        "runtime_authority": "NONE",
        "production_execution": False,
        "node_source": {"manifest": MANIFEST_PATH, "manifest_sha256": sha_file(root / MANIFEST_PATH), "manifest_id": manifest.get("manifest_id"), "manifest_version": manifest.get("manifest_version")},
        "relation_types": RELATIONS,
        "nodes": nodes,
        "edges": candidates,
        "unresolved_edges": sorted(unresolved, key=lambda row: (row.get("candidate_source_artifact_id", ""), row.get("relation", ""), row.get("candidate_target_artifact_id", ""))),
        "invalid_edges_rejected": invalid_edges,
        "lineage_roots": sorted(set(roots)),
        "orphan_nodes": sorted(orphan_nodes, key=lambda row: row["artifact_id"]),
        "indexes": {"parents_by_artifact": parents_index, "children_by_artifact": children_index},
        "statistics": {
            "logical_nodes": len(nodes),
            "physical_locations_referenced": locations_count,
            "edges": len(candidates),
            "evidence_backed_edges": sum(1 for edge in candidates if edge["confidence"] == "EVIDENCE_BACKED"),
            "orphan_nodes": len(orphan_nodes),
            "lineage_roots": len(set(roots)),
            "invalid_edges_rejected": len(invalid_edges),
            "unresolved_edges": len(unresolved),
            "global_unmanaged_candidates": int(manifest.get("unmanaged_inventory", {}).get("orphan_candidates", 0)),
            "d3_evidence_backed_edges": len(d3_edges),
            "d4_evidence_backed_edges": len(d4_edges),
        },
        "validation": {"dag_valid": not cycles and not invalid_edges, "duplicate_identity_collapsed": len({node["artifact_id"] for node in nodes}) == len(nodes), "all_nodes_from_manifest": True, "all_edges_evidence_backed": all(edge["confidence"] == "EVIDENCE_BACKED" for edge in candidates), "d3_lineage_valid": bool(raw and master and d33_receipt and any(e["relation"] == "DERIVED_FROM" and e["source_artifact_id"] == master["artifact_id"] and e["target_artifact_id"] == raw["artifact_id"] for e in candidates)), "d4_lineage_valid": bool(manifest.get("lineage", {}).get("request_to_plan") and manifest.get("lineage", {}).get("plan_to_authorization") and d4_edges)},
        "next": "D5.3 - Artifact Topology Validator",
    }
    return registry, {"d3_edges": d3_edges, "d4_edges": d4_edges, "invalid_edges": invalid_edges, "cycle_detected": cycles}


def synthetic_checks() -> dict[str, bool]:
    a, b, c = "a" * 64, "b" * 64, "c" * 64
    cycle_edges = [
        {"source_artifact_id": a, "target_artifact_id": b},
        {"source_artifact_id": b, "target_artifact_id": c},
        {"source_artifact_id": c, "target_artifact_id": a},
    ]
    cycle_detected = detect_cycle({a, b, c}, cycle_edges)
    synthetic_nodes = [{"artifact_id": a}]
    missing = {"edge_id": "synthetic", "source_artifact_id": a, "target_artifact_id": "missing", "relation": "DERIVED_FROM", "evidence": {"source_artifact_id": a}}
    accepted, invalid = validate_edges(synthetic_nodes, [missing])
    return {"synthetic_cycle_detected": cycle_detected, "missing_parent_rejected": len(accepted) == 0 and len(invalid) == 1 and invalid[0]["reason"] == "INVALID_EDGE"}


def outputs(root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    manifest_path = root / MANIFEST_PATH
    manifest = read_json(manifest_path)
    receipt = read_json(root / "artifacts/tests/c11d_d5/d5_1/d5_1_validation_receipt.json")
    if receipt.get("result") != "PASS" or receipt.get("status") != "CLOSED":
        raise ValueError("D5.1 must be PASS/CLOSED before D5.2.")
    if receipt.get("manifest_sha256") != sha_file(manifest_path):
        raise ValueError("D5.1 receipt does not verify the manifest bytes.")
    registry, graph = build_graph(root, manifest)
    synthetic = synthetic_checks()
    archive = root / "artifacts/releases/ChallengeEngineV01_STATELESS_C11-C_2.19.12_FROZEN_20260930_175709.zip"
    frozen_ok = archive.is_file() and sha_file(archive) == FROZEN_SHA256
    validation = registry["validation"]
    d3_valid = validation["d3_lineage_valid"] and any(edge["relation"] == "VALIDATED_BY" and edge["evidence"].get("source_checkpoint") == "C11-D D3.2" for edge in registry["edges"])
    d4_valid = validation["d4_lineage_valid"] and any(edge["relation"] in {"GENERATED_FROM", "VALIDATED_BY"} and edge["evidence"].get("source_checkpoint") == "C11-D D4.9" for edge in registry["edges"])
    nodes_count = registry["statistics"]["logical_nodes"]
    loc_count = registry["statistics"]["physical_locations_referenced"]
    d51_stats = manifest["statistics"]
    okay = (
        nodes_count == d51_stats["manifest_record_count"] == 75
        and loc_count == 79
        and registry["statistics"]["orphan_nodes"] == 9
        and registry["statistics"]["global_unmanaged_candidates"] == 12304
        and registry["statistics"]["invalid_edges_rejected"] == 0
        and validation["dag_valid"]
        and validation["duplicate_identity_collapsed"]
        and validation["all_nodes_from_manifest"]
        and validation["all_edges_evidence_backed"]
        and d3_valid and d4_valid and synthetic["synthetic_cycle_detected"] and synthetic["missing_parent_rejected"] and frozen_ok
        and registry["runtime_authority"] == "NONE" and registry["production_execution"] is False
    )
    registry["validation"].update({
        "synthetic_cycle_detected": synthetic["synthetic_cycle_detected"],
        "missing_parent_rejected": synthetic["missing_parent_rejected"],
        "frozen_c11c_preserved": frozen_ok,
    })
    registry["result"] = "PASS" if okay else "BLOCKED"
    registry["checkpoint"] = "C11-D D5.2"
    evidence = {
        "checkpoint": "C11-D D5.2",
        "result": "PASS" if okay else "BLOCKED",
        "status": "CLOSED" if okay else "BLOCKED",
        "source_manifest": {"path": MANIFEST_PATH, "sha256": sha_file(manifest_path), "logical_nodes": nodes_count, "physical_locations": loc_count},
        "d3_lineage_edges": graph["d3_edges"],
        "d4_lineage_edges": graph["d4_edges"],
        "synthetic_tests": synthetic,
        "frozen_c11c_sha256": FROZEN_SHA256 if frozen_ok else "MISMATCH",
        "runtime_authority": "NONE",
        "production_execution": False,
    }
    registry_hash = sha_bytes(json_bytes(registry))
    evidence["registry_sha256"] = registry_hash
    evidence_hash = sha_bytes(json_bytes(evidence))
    stats = registry["statistics"]
    validation_receipt = {
        "checkpoint": "C11-D D5.2",
        "result": "PASS" if okay else "BLOCKED",
        "status": "CLOSED" if okay else "BLOCKED",
        "logical_nodes": stats["logical_nodes"],
        "physical_locations_referenced": stats["physical_locations_referenced"],
        "edges": stats["edges"],
        "evidence_backed_edges": stats["evidence_backed_edges"],
        "orphan_nodes": stats["orphan_nodes"],
        "global_unmanaged_candidates": stats["global_unmanaged_candidates"],
        "dag_valid": validation["dag_valid"],
        "duplicate_identity_collapsed": validation["duplicate_identity_collapsed"],
        "missing_parent_rejected": synthetic["missing_parent_rejected"],
        "synthetic_cycle_detected": synthetic["synthetic_cycle_detected"],
        "d3_lineage_valid": d3_valid,
        "d4_lineage_valid": d4_valid,
        "deterministic_registry": True,
        "idempotency": True,
        "cleanup_performed": False,
        "files_moved": False,
        "files_deleted": False,
        "frozen_c11c_preserved": frozen_ok,
        "runtime_authority": "NONE",
        "production_execution": False,
        "registry_sha256": registry_hash,
        "evidence_sha256": evidence_hash,
        "next": "D5.3 - Artifact Topology Validator",
    }
    return registry, evidence, validation_receipt


def write_outputs(root: Path, values: tuple[dict[str, Any], dict[str, Any], dict[str, Any]]) -> dict[str, str]:
    folder = root / "artifacts/tests/c11d_d5/d5_2"
    names = {"registry": "d5_2_lineage_registry.json", "evidence": "d5_2_lineage_evidence.json", "receipt": "d5_2_validation_receipt.json"}
    for key, value in zip(names, values):
        stable_write(folder / names[key], value)
    return {key: sha_file(folder / name) for key, name in names.items()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    args = parser.parse_args()
    root = args.root.resolve()
    first = outputs(root)
    hash_a = write_outputs(root, first)
    second = outputs(root)
    hash_b = write_outputs(root, second)
    idempotent = hash_a == hash_b
    receipt_path = root / "artifacts/tests/c11d_d5/d5_2/d5_2_validation_receipt.json"
    receipt = read_json(receipt_path)
    receipt["idempotency"] = bool(receipt.get("idempotency") and idempotent)
    stable_write(receipt_path, receipt)
    print(json.dumps({"result": receipt["result"] if idempotent else "BLOCKED", "status": receipt["status"] if idempotent else "BLOCKED", "logical_nodes": receipt["logical_nodes"], "physical_locations_referenced": receipt["physical_locations_referenced"], "edges": receipt["edges"], "evidence_backed_edges": receipt["evidence_backed_edges"], "orphan_nodes": receipt["orphan_nodes"], "registry_sha256": receipt["registry_sha256"], "evidence_sha256": receipt["evidence_sha256"], "idempotency": idempotent}, indent=2))
    return 0 if receipt["result"] == "PASS" and idempotent else 2


if __name__ == "__main__":
    raise SystemExit(main())
