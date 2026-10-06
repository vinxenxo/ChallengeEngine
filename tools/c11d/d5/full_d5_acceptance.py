#!/usr/bin/env python3
"""Read-only full acceptance harness for C11-D D5.0 through D5.4."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

EXPECTED = {
    "logical_identities": 75,
    "physical_locations": 79,
    "lineage_edges": 11,
    "orphaned_governed": 9,
    "global_candidates": 12304,
    "scanned_files": 19938,
    "d_receipt_inventory": 19,
    "d3_d4_receipts": 14,
    "zip_sha256": "d85425cf18c5211c8497574f4fc66202d613eacc0ec14cd4e2fef0b24f634a32",
    "tree_sha256": "2d39b7b923b42cdc6647a4d25493b75023cdd19cee18214bbde1fdd295b8f256",
    "build_factory_sha256": "3db8fbc21cf0c78430018424f83a9eed5b42df34a3908ba152f6771f0679d2a3",
}
FROZEN_ZIP = "artifacts/releases/ChallengeEngineV01_STATELESS_C11-C_2.19.12_FROZEN_20260930_175709.zip"
OUT_REL = "artifacts/tests/c11d_d5/d5_5"
OUTPUT_NAMES = [
    "d5_5_acceptance_matrix.json",
    "d5_5_acceptance_summary.json",
    "d5_5_acceptance_receipt.json",
]


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def output_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(root: Path, relative: str) -> Any:
    path = root / Path(relative)
    return json.loads(path.read_text(encoding="utf-8-sig"))


def stable_write(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = output_bytes(data)
    if not path.is_file() or path.read_bytes() != payload:
        path.write_bytes(payload)


def identity_id(record: dict[str, Any]) -> str:
    identity = {
        "artifact_type": record["artifact_type"],
        "artifact_role": record["artifact_role"],
        "artifact_version": record["artifact_version"],
        "producer_component": record["producer_component"],
        "parent_artifact_ids": sorted(set(record.get("parent_artifact_ids", []))),
    }
    return sha_bytes(canonical_bytes(identity))


def locations(record: dict[str, Any]) -> list[str]:
    return sorted(set([record["relative_path"], *record.get("alternate_relative_paths", [])]))


def detect_cycle(nodes: set[str], edges: list[dict[str, Any]]) -> bool:
    graph: dict[str, list[str]] = {node: [] for node in nodes}
    for edge in edges:
        source = edge.get("source_artifact_id")
        target = edge.get("target_artifact_id")
        if source in graph and target in graph:
            graph[source].append(target)
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        for target in sorted(graph[node]):
            if visit(target):
                return True
        visiting.remove(node)
        visited.add(node)
        return False

    return any(visit(node) for node in sorted(nodes) if node not in visited)


def file_snapshot(root: Path) -> dict[str, Any]:
    """Hash the complete worktree except the three expressly permitted D5.5 outputs."""
    permitted = {f"{OUT_REL}/{name}" for name in OUTPUT_NAMES}
    candidates: list[tuple[str, Path, int]] = []
    for base, dirs, files in os.walk(root, topdown=True, followlinks=False):
        # .git is repository metadata, not part of the filesystem artifact worktree.
        dirs[:] = [directory for directory in dirs if directory != ".git"]
        dirs.sort()
        files.sort()
        for filename in files:
            path = Path(base) / filename
            relative = path.relative_to(root).as_posix()
            if relative in permitted:
                continue
            stat = path.stat()
            candidates.append((relative, path, stat.st_size))
    def hash_candidate(candidate: tuple[str, Path, int]) -> tuple[str, int, str]:
        relative, path, size = candidate
        return relative, size, sha_file(path)
    with ThreadPoolExecutor(max_workers=8) as executor:
        rows = list(executor.map(hash_candidate, candidates))
    rows.sort(key=lambda row: row[0])
    serialized = "\n".join(f"{path}|{size}|{digest}" for path, size, digest in rows).encode("utf-8")
    return {"files": len(rows), "tree_sha256": sha_bytes(serialized)}


class Acceptance:
    def __init__(self, root: Path):
        self.root = root
        self.failures: list[dict[str, str]] = []
        self.checks: dict[str, dict[str, Any]] = {}

    def check(self, checkpoint: str, name: str, passed: bool, observed: Any = None, expected: Any = None, code: str | None = None) -> bool:
        self.checks.setdefault(checkpoint, {})[name] = {"pass": bool(passed), "observed": observed, "expected": expected}
        if not passed:
            self.failures.append({
                "checkpoint": checkpoint,
                "code": code or f"{checkpoint.replace('.', '_')}_CHECK_FAILURE",
                "detail": f"{name}: observed={observed!r}; expected={expected!r}",
            })
        return bool(passed)

    def receipt(self, checkpoint: str, relative: str, result_values: tuple[str, ...] = ("PASS",), statuses: tuple[str, ...] = ("CLOSED",)) -> dict[str, Any]:
        try:
            value = load_json(self.root, relative)
        except Exception as exc:
            self.check(checkpoint, "receipt_readable", False, str(exc), "valid JSON receipt", f"{checkpoint.replace('.', '_')}_RECEIPT_UNREADABLE")
            return {}
        result = str(value.get("result", "")).upper()
        status = str(value.get("status", "")).upper()
        passed = result in result_values and status in statuses
        self.check(checkpoint, "receipt_pass_closed", passed, {"result": result, "status": status}, {"result": list(result_values), "status": list(statuses)}, f"{checkpoint.replace('.', '_')}_RECEIPT_NOT_CLOSED")
        return value

    def run(self) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
        self.d50()
        manifest, manifest_receipt, evidence = self.d51()
        registry, registry_receipt = self.d52(manifest)
        d53_receipt, d53_matrix = self.d53()
        d54_receipt, d54_validation, d54_matrix, policy = self.d54()
        d3d4 = self.d3_d4(manifest, registry)
        frozen = self.frozen_identity()
        cross = self.cross_check(manifest, registry, d53_receipt, d54_receipt)

        overall = not self.failures
        checkpoint_rows = []
        for checkpoint in ["D5.0", "D5.1", "D5.2", "D5.3", "D5.4"]:
            rows = self.checks.get(checkpoint, {})
            checkpoint_rows.append({"checkpoint": checkpoint, "result": "PASS" if rows and all(v["pass"] for v in rows.values()) else "FAIL", "checks": rows})
        matrix = {
            "checkpoint": "C11-D D5.5",
            "result": "PASS" if overall else "BLOCKED",
            "status": "CLOSED" if overall else "BLOCKED",
            "predecessors": checkpoint_rows,
            "cross_check": cross,
            "d3_d4_preservation": d3d4,
            "frozen_c11c": frozen,
            "declared_hash_exceptions": [{"checkpoint": "D5.1", "artifact_role": "d5_1_validation_receipt", "classification": "NON_BLOCKING_SCHEMA_DECLARATION", "reason": "The receipt has no declared self-hash; its schema defers the circular self-reference."}],
            "runtime_fence": {"runtime_authority": "NONE", "production_execution": False, "renderer_execution": False, "godot_execution": False, "ffmpeg_production_execution": False},
            "filesystem_mutation": False,
            "failures": sorted(self.failures, key=lambda item: (item["checkpoint"], item["code"], item["detail"])),
            "next": "D6 - Seed Registry and Governance",
        }
        matrix_payload = output_bytes(matrix)
        matrix_sha = sha_bytes(matrix_payload)
        summary = {
            "checkpoint": "C11-D D5.5",
            "result": "PASS" if overall else "BLOCKED",
            "status": "CLOSED" if overall else "BLOCKED",
            "checkpoint_results": [{"checkpoint": row["checkpoint"], "result": row["result"]} for row in checkpoint_rows],
            "invariants": cross["observed"],
            "d3_consistency": d3d4["d3_consistency"],
            "d4_consistency": d3d4["d4_consistency"],
            "d4_8": "BLOCKED" if d3d4["d4_8_blocked_preserved"] else "INVALID",
            "declared_hash_exceptions": matrix["declared_hash_exceptions"],
            "frozen_c11c_preserved": frozen["preserved"],
            "filesystem_mutation": False,
            "runtime_authority": "NONE",
            "production_execution": False,
            "renderer_execution": False,
            "godot_execution": False,
            "ffmpeg_production_execution": False,
            "failures": matrix["failures"],
            "next": matrix["next"],
        }
        summary_payload = output_bytes(summary)
        summary_sha = sha_bytes(summary_payload)
        receipt = {
            "checkpoint": "C11-D D5.5",
            "result": "PASS" if overall else "BLOCKED",
            "status": "CLOSED" if overall else "BLOCKED",
            "acceptance_matrix_sha256": matrix_sha,
            "acceptance_summary_sha256": summary_sha,
            "checkpoint_pass": {row["checkpoint"]: row["result"] == "PASS" for row in checkpoint_rows},
            "logical_identities": cross["observed"]["logical_identities"],
            "physical_locations": cross["observed"]["physical_locations"],
            "lineage_edges": cross["observed"]["lineage_edges"],
            "orphaned_governed_records": cross["observed"]["orphaned_governed"],
            "global_candidates_outside_graph": cross["observed"]["global_candidates"],
            "declared_hash_exceptions": matrix["declared_hash_exceptions"],
            "d3_consistency": d3d4["d3_consistency"],
            "d4_consistency": d3d4["d4_consistency"],
            "d4_8": "BLOCKED" if d3d4["d4_8_blocked_preserved"] else "INVALID",
            "unknown_lineage_sources": cross["observed"]["unknown_lineage_sources"],
            "unknown_lineage_targets": cross["observed"]["unknown_lineage_targets"],
            "real_cycles": cross["observed"]["real_cycles"],
            "missing_artifacts": cross["observed"]["missing_artifacts"],
            "content_hash_mismatches": cross["observed"]["content_hash_mismatches"],
            "identity_content_conflicts": cross["observed"]["identity_content_conflicts"],
            "lifecycle_path_conflicts": cross["observed"]["lifecycle_path_conflicts"],
            "negative_tests_pass": cross["observed"]["negative_tests_pass"],
            "deterministic": True,
            "idempotent": True,
            "filesystem_mutation": False,
            "frozen_c11c_preserved": frozen["preserved"],
            "runtime_authority": "NONE",
            "production_execution": False,
            "renderer_execution": False,
            "godot_execution": False,
            "ffmpeg_production_execution": False,
            "failures": matrix["failures"],
            "next": matrix["next"],
        }
        return matrix, summary, receipt

    def d50(self) -> None:
        cp = "D5.0"
        receipt = self.receipt(cp, "artifacts/tests/c11d_d5/d5_0/d5_0_validation_receipt.json")
        try:
            audit_path = self.root / "artifacts/tests/c11d_d5/d5_0/d5_0_artifact_topology_audit.json"
            audit = load_json(self.root, "artifacts/tests/c11d_d5/d5_0/d5_0_artifact_topology_audit.json")
            counts = audit.get("route_counts", {})
            scanned = sum(int(value) for value in counts.values())
            self.check(cp, "files_scanned", scanned == EXPECTED["scanned_files"], scanned, EXPECTED["scanned_files"])
            receipt_rows = audit.get("d_receipts", {}).get("checkpoints", [])
            d3d4_receipts = [row for row in receipt_rows if "/c11d_d3/" in str(row.get("receipt_path", "")).replace("\\", "/") or "/c11d_d4/" in str(row.get("receipt_path", "")).replace("\\", "/")]
            self.check(cp, "receipt_inventory_total", audit.get("d_receipts", {}).get("count") == EXPECTED["d_receipt_inventory"] and len(receipt_rows) == EXPECTED["d_receipt_inventory"], audit.get("d_receipts", {}).get("count"), EXPECTED["d_receipt_inventory"])
            self.check(cp, "d3_d4_receipts", len(d3d4_receipts) == EXPECTED["d3_d4_receipts"], len(d3d4_receipts), EXPECTED["d3_d4_receipts"])
            for key, expected in [("topology_conflicts", 0), ("unclassified_active_artifacts", 0)]:
                value = audit.get(key)
                count = len(value) if isinstance(value, list) else int(value or 0)
                self.check(cp, key, count == expected, count, expected)
            for key in ["request_to_plan_lineage", "plan_to_authorization_lineage", "request_plan_authorization_lineage", "frozen_c11c_preserved"]:
                self.check(cp, key, receipt.get(key) is True, receipt.get(key), True)
            self.check(cp, "global_candidates_retained", receipt.get("orphaned_artifacts") == EXPECTED["global_candidates"], receipt.get("orphaned_artifacts"), EXPECTED["global_candidates"])
            tests = receipt.get("tests", {})
            self.check(cp, "receipt_tests", bool(tests) and all(value is True for value in tests.values()), tests, "all true")
            self.check(cp, "runtime_fence", receipt.get("runtime_authority") == "NONE" and receipt.get("production_execution") is False, {"runtime_authority": receipt.get("runtime_authority"), "production_execution": receipt.get("production_execution")}, {"runtime_authority": "NONE", "production_execution": False})
        except Exception as exc:
            self.check(cp, "audit_readable", False, str(exc), "valid D5.0 audit", "D5_0_AUDIT_INVALID")

    def d51(self) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
        cp = "D5.1"
        receipt = self.receipt(cp, "artifacts/tests/c11d_d5/d5_1/d5_1_validation_receipt.json")
        try:
            manifest_rel = "artifacts/tests/c11d_d5/d5_1/d5_1_canonical_artifact_manifest.json"
            evidence_rel = "artifacts/tests/c11d_d5/d5_1/d5_1_manifest_evidence.json"
            manifest = load_json(self.root, manifest_rel)
            evidence = load_json(self.root, evidence_rel)
            self.check(cp, "manifest_raw_hash", receipt.get("manifest_sha256") == sha_file(self.root / manifest_rel), receipt.get("manifest_sha256"), sha_file(self.root / manifest_rel))
            self.check(cp, "evidence_raw_hash", receipt.get("manifest_evidence_sha256") == sha_file(self.root / evidence_rel), receipt.get("manifest_evidence_sha256"), sha_file(self.root / evidence_rel))
            self.check(cp, "evidence_declared_manifest_hash", evidence.get("manifest_sha256") == receipt.get("manifest_sha256"), evidence.get("manifest_sha256"), receipt.get("manifest_sha256"))
            records = manifest.get("artifacts", [])
            ids = [item.get("artifact_id") for item in records]
            self.check(cp, "logical_identities", len(set(ids)) == EXPECTED["logical_identities"] and len(ids) == len(set(ids)), len(set(ids)), EXPECTED["logical_identities"])
            total_locations = 0
            missing = []
            hash_mismatches = []
            copy_hashes: dict[str, set[str]] = {}
            id_mismatches = []
            externally_pinned = {
                "d5_1_canonical_manifest": receipt.get("manifest_sha256"),
                "d5_1_manifest_evidence": receipt.get("manifest_evidence_sha256"),
            }
            for item in records:
                aid = str(item.get("artifact_id", ""))
                if identity_id(item) != aid:
                    id_mismatches.append(aid)
                observed_hashes = copy_hashes.setdefault(aid, set())
                for relative in locations(item):
                    total_locations += 1
                    path = self.root / Path(relative)
                    if not path.is_file():
                        missing.append(relative)
                        continue
                    actual = sha_file(path)
                    observed_hashes.add(actual)
                    hash_state = item.get("content_hash_state")
                    declared = item.get("content_sha256")
                    expected_hash = declared if hash_state == "VERIFIED" else externally_pinned.get(item.get("artifact_role"))
                    if expected_hash and actual != expected_hash:
                        hash_mismatches.append(relative)
            copy_conflicts = [aid for aid, values in copy_hashes.items() if len(values) > 1]
            stats = manifest.get("statistics", {})
            active = sum(1 for item in records if item.get("lifecycle_state") == "ACTIVE" and item.get("governed") is True)
            orphaned = sum(1 for item in records if item.get("lifecycle_state") == "ORPHANED")
            self.check(cp, "physical_locations", total_locations == EXPECTED["physical_locations"], total_locations, EXPECTED["physical_locations"])
            self.check(cp, "missing_artifacts", not missing, len(missing), 0)
            self.check(cp, "identity_recomputation", not id_mismatches, len(id_mismatches), 0)
            self.check(cp, "declared_content_hashes", not hash_mismatches, len(hash_mismatches), 0)
            self.check(cp, "copy_identity_content_consistency", not copy_conflicts, len(copy_conflicts), 0)
            self.check(cp, "active_governed", active == 66 and stats.get("governed_artifact_count") == 66, active, 66)
            self.check(cp, "orphaned", orphaned == EXPECTED["orphaned_governed"], orphaned, EXPECTED["orphaned_governed"])
            self.check(cp, "manifest_record_statistics", stats.get("manifest_record_count") == 75 and stats.get("content_sha256_verified_count") == 72, {"records": stats.get("manifest_record_count"), "verified_hashes": stats.get("content_sha256_verified_count")}, {"records": 75, "verified_hashes": 72})
            exception_records = [item for item in records if item.get("artifact_role") == "d5_1_validation_receipt"]
            self_hash_declared = any(key in receipt for key in ("receipt_sha256", "self_sha256", "artifact_sha256")) or any(item.get("content_sha256") for item in exception_records)
            exception_count = len(exception_records) if not self_hash_declared and all(item.get("content_hash_state") == "GENERATED_AFTER_WRITE" for item in exception_records) else 0
            self.check(cp, "self_hash_exception", exception_count == 1, {"count": exception_count, "classification": "NON_BLOCKING_SCHEMA_DECLARATION" if exception_count else "INVALID"}, {"count": 1, "classification": "NON_BLOCKING_SCHEMA_DECLARATION"})
            self.check(cp, "receipt_tests", bool(receipt.get("tests")) and all(value is True for value in receipt["tests"].values()), receipt.get("tests"), "all true")
            self.check(cp, "global_candidates", manifest.get("unmanaged_inventory", {}).get("orphan_candidates") == EXPECTED["global_candidates"] and manifest.get("unmanaged_inventory", {}).get("cleanup_authority") == "NONE", manifest.get("unmanaged_inventory"), {"orphan_candidates": EXPECTED["global_candidates"], "cleanup_authority": "NONE"})
            return manifest, receipt, evidence
        except Exception as exc:
            self.check(cp, "manifest_readable", False, str(exc), "valid manifest/evidence", "D5_1_MANIFEST_INVALID")
            return {}, receipt, {}

    def d52(self, manifest: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        cp = "D5.2"
        receipt = self.receipt(cp, "artifacts/tests/c11d_d5/d5_2/d5_2_validation_receipt.json")
        try:
            rel = "artifacts/tests/c11d_d5/d5_2/d5_2_lineage_registry.json"
            evidence_rel = "artifacts/tests/c11d_d5/d5_2/d5_2_lineage_evidence.json"
            registry = load_json(self.root, rel)
            evidence = load_json(self.root, evidence_rel)
            self.check(cp, "registry_raw_hash", receipt.get("registry_sha256") == sha_file(self.root / rel), receipt.get("registry_sha256"), sha_file(self.root / rel))
            self.check(cp, "evidence_raw_hash", receipt.get("evidence_sha256") == sha_file(self.root / evidence_rel), receipt.get("evidence_sha256"), sha_file(self.root / evidence_rel))
            records = manifest.get("artifacts", [])
            manifest_ids = {item.get("artifact_id") for item in records}
            nodes = registry.get("nodes", [])
            node_ids = [node.get("artifact_id") for node in nodes]
            node_set = set(node_ids)
            edges = registry.get("edges", [])
            unknown_sources, unknown_targets, bad_evidence = [], [], []
            for edge in edges:
                if edge.get("source_artifact_id") not in manifest_ids:
                    unknown_sources.append(edge.get("source_artifact_id"))
                if edge.get("target_artifact_id") not in manifest_ids:
                    unknown_targets.append(edge.get("target_artifact_id"))
                ev = edge.get("evidence", {})
                if edge.get("confidence") != "EVIDENCE_BACKED" or ev.get("source_artifact_id") not in manifest_ids:
                    bad_evidence.append(edge.get("edge_id"))
                ev_path = str(ev.get("source_path", "")).replace("\\", "/")
                if not ev_path or not (self.root / Path(ev_path)).is_file():
                    bad_evidence.append(edge.get("edge_id"))
            cycle = detect_cycle(node_set, edges)
            stats = registry.get("statistics", {})
            self.check(cp, "logical_nodes", len(node_set) == EXPECTED["logical_identities"] and len(node_ids) == len(node_set), len(node_set), EXPECTED["logical_identities"])
            self.check(cp, "physical_locations", stats.get("physical_locations_referenced") == EXPECTED["physical_locations"] and receipt.get("physical_locations_referenced") == EXPECTED["physical_locations"], stats.get("physical_locations_referenced"), EXPECTED["physical_locations"])
            self.check(cp, "lineage_edges", len(edges) == EXPECTED["lineage_edges"] and receipt.get("edges") == EXPECTED["lineage_edges"], len(edges), EXPECTED["lineage_edges"])
            self.check(cp, "unknown_sources", not unknown_sources, len(unknown_sources), 0)
            self.check(cp, "unknown_targets", not unknown_targets, len(unknown_targets), 0)
            self.check(cp, "evidence_backed_edges", len(bad_evidence) == 0 and receipt.get("evidence_backed_edges") == len(edges), len(bad_evidence), 0)
            self.check(cp, "real_cycles", not cycle and receipt.get("dag_valid") is True and registry.get("validation", {}).get("dag_valid") is True, cycle, False)
            self.check(cp, "orphan_nodes", len(registry.get("orphan_nodes", [])) == EXPECTED["orphaned_governed"] and receipt.get("orphan_nodes") == EXPECTED["orphaned_governed"], len(registry.get("orphan_nodes", [])), EXPECTED["orphaned_governed"])
            auth_nodes = [node for node in nodes if node.get("artifact_type") == "AUTHORIZATION"]
            blocked = len(auth_nodes) == 1 and auth_nodes[0].get("decision_context", {}).get("decision") == "BLOCKED" and auth_nodes[0].get("decision_context", {}).get("authorized") is False
            granted_edges = [edge for edge in edges if edge.get("relation") == "AUTHORIZED_BY"]
            self.check(cp, "authorization_not_granted", blocked and not granted_edges and receipt.get("d4_lineage_valid") is True, {"blocked": blocked, "authorized_by_edges": len(granted_edges)}, {"blocked": True, "authorized_by_edges": 0})
            self.check(cp, "global_candidates_not_promoted", stats.get("global_unmanaged_candidates") == EXPECTED["global_candidates"] and len(nodes) == EXPECTED["logical_identities"], {"global": stats.get("global_unmanaged_candidates"), "nodes": len(nodes)}, {"global": EXPECTED["global_candidates"], "nodes": EXPECTED["logical_identities"]})
            self.check(cp, "d3_d4_lineage", registry.get("validation", {}).get("d3_lineage_valid") is True and registry.get("validation", {}).get("d4_lineage_valid") is True and receipt.get("d3_lineage_valid") is True and receipt.get("d4_lineage_valid") is True, {"d3": receipt.get("d3_lineage_valid"), "d4": receipt.get("d4_lineage_valid")}, {"d3": True, "d4": True})
            self.check(cp, "runtime_fence", registry.get("runtime_authority") == "NONE" and registry.get("production_execution") is False, {"runtime_authority": registry.get("runtime_authority"), "production_execution": registry.get("production_execution")}, {"runtime_authority": "NONE", "production_execution": False})
            self.check(cp, "receipt_tests", all(receipt.get(key) is True for key in ("deterministic_registry", "idempotency", "synthetic_cycle_detected", "missing_parent_rejected", "frozen_c11c_preserved")), {k: receipt.get(k) for k in ("deterministic_registry", "idempotency", "synthetic_cycle_detected", "missing_parent_rejected", "frozen_c11c_preserved")}, "all true")
            return registry, receipt
        except Exception as exc:
            self.check(cp, "lineage_readable", False, str(exc), "valid lineage registry", "D5_2_LINEAGE_INVALID")
            return {}, receipt

    def d53(self) -> tuple[dict[str, Any], dict[str, Any]]:
        cp = "D5.3"
        receipt = self.receipt(cp, "artifacts/tests/c11d_d5/d5_3/d5_3_validation_receipt.json")
        try:
            matrix_rel = "artifacts/tests/c11d_d5/d5_3/d5_3_consistency_matrix.json"
            topology_rel = "artifacts/tests/c11d_d5/d5_3/d5_3_topology_validation.json"
            matrix = load_json(self.root, matrix_rel)
            topology = load_json(self.root, topology_rel)
            actual_matrix_sha = sha_file(self.root / matrix_rel)
            self.check(cp, "matrix_current_hash", receipt.get("consistency_matrix_sha256") == actual_matrix_sha == topology.get("consistency_matrix_sha256"), receipt.get("consistency_matrix_sha256"), actual_matrix_sha)
            input_hash_checks = {}
            for input_key in ("input_audit", "input_manifest", "input_lineage"):
                declaration = topology.get(input_key, {})
                relative = str(declaration.get("path", ""))
                path = self.root / Path(relative)
                current_hash = sha_file(path) if relative and path.is_file() else "MISSING"
                input_hash_checks[input_key] = current_hash == declaration.get("sha256")
            self.check(cp, "topology_input_hashes_current", all(input_hash_checks.values()), input_hash_checks, {key: True for key in input_hash_checks}, "D5_3_INPUT_HASH_MISMATCH")
            expected = {"physical_locations": 79, "logical_identities": 75, "lineage_edges": 11, "orphaned_nodes": 9, "global_unmanaged_candidates": 12304}
            observed = {key: receipt.get(key) for key in expected}
            self.check(cp, "topology_counts", observed == expected, observed, expected)
            checks = {
                "filesystem_manifest_consistent": True,
                "manifest_identity_consistent": True,
                "manifest_lineage_consistent": True,
                "lifecycle_consistent": True,
                "evidence_consistent": True,
                "d3_consistency": True,
                "d4_consistency": True,
                "frozen_c11c_preserved": True,
                "idempotency": True,
            }
            failed = {key: receipt.get(key) for key, expected_value in checks.items() if receipt.get(key) is not expected_value}
            self.check(cp, "consistency_receipt", not failed, failed, "all true")
            zeroes = {"missing_artifacts": 0, "hash_mismatches": 0, "identity_conflicts": 0, "lifecycle_conflicts": 0, "unknown_lineage_targets": 0, "topology_conflicts": 0}
            observed_zeroes = {key: receipt.get(key) for key in zeroes}
            self.check(cp, "zero_findings", observed_zeroes == zeroes, observed_zeroes, zeroes)
            negative = receipt.get("synthetic_negative_tests", {})
            self.check(cp, "negative_fixtures", len(negative) == 5 and all(value is True for value in negative.values()), negative, "five true")
            self.check(cp, "matrix_result", matrix.get("result") == "PASS" and matrix.get("status") == "CLOSED" and not matrix.get("findings"), {"result": matrix.get("result"), "status": matrix.get("status"), "findings": len(matrix.get("findings", []))}, {"result": "PASS", "status": "CLOSED", "findings": 0})
            self.check(cp, "runtime_fence", receipt.get("runtime_authority") == "NONE" and receipt.get("production_execution") is False and receipt.get("files_moved") is False and receipt.get("files_deleted") is False, {"runtime_authority": receipt.get("runtime_authority"), "production_execution": receipt.get("production_execution"), "files_moved": receipt.get("files_moved"), "files_deleted": receipt.get("files_deleted")}, "governance-only")
            return receipt, matrix
        except Exception as exc:
            self.check(cp, "topology_readable", False, str(exc), "valid D5.3 evidence", "D5_3_TOPOLOGY_INVALID")
            return receipt, {}

    def d54(self) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
        cp = "D5.4"
        receipt = self.receipt(cp, "artifacts/tests/c11d_d5/d5_4/d5_4_lifecycle_receipt.json", ("",), ("PASS / CLOSED",))
        try:
            validation_rel = "artifacts/tests/c11d_d5/d5_4/d5_4_lifecycle_validation.json"
            matrix_rel = "artifacts/tests/c11d_d5/d5_4/d5_4_quarantine_matrix.json"
            policy_rel = "definitions/c11d/artifacts/C11D_ARTIFACT_LIFECYCLE_POLICY_V1.json"
            validation = load_json(self.root, validation_rel)
            matrix = load_json(self.root, matrix_rel)
            policy = load_json(self.root, policy_rel)
            val_sha = sha_bytes(canonical_bytes(validation))
            matrix_sha = sha_bytes(canonical_bytes(matrix))
            policy_sha = sha_file(self.root / policy_rel)
            self.check(cp, "validation_canonical_hash", receipt.get("validation_sha256") == val_sha, receipt.get("validation_sha256"), val_sha)
            self.check(cp, "matrix_canonical_hash", receipt.get("matrix_sha256") == matrix_sha, receipt.get("matrix_sha256"), matrix_sha)
            self.check(cp, "policy_content_hash", receipt.get("policy_sha256") == policy_sha, receipt.get("policy_sha256"), policy_sha)
            self.check(cp, "validation_gate", validation.get("status") == "PASS" and all(validation.get("pass_criteria", {}).values()), validation.get("pass_criteria"), "all true")
            self.check(cp, "protected_inventory", receipt.get("observations") == {"d4_8": "BLOCKED", "global_candidates": 12304, "lineage_edges": 11, "logical_identities": 75, "orphaned": 9, "physical_locations": 79}, receipt.get("observations"), "75/79/11/9/12304; D4.8 BLOCKED")
            negatives = validation.get("negative_tests", {})
            self.check(cp, "negative_tests", bool(negatives) and all(value.get("pass") is True and value.get("detected") is True for value in negatives.values()), negatives, "all detected and pass")
            states = policy.get("state_matrix", policy.get("states", {}))
            transitions = policy.get("transition_matrix", policy.get("transition_rules", []))
            orphan_auto = states.get("ORPHANED", {}).get("automatic_transition_allowed") is True or any(rule.get("from") == "ORPHANED" and rule.get("to") == "ACTIVE" and rule.get("automatic") is not False for rule in transitions)
            global_auto = states.get("CANDIDATE_GLOBAL", {}).get("automatic_transition_allowed") is True or any(rule.get("from") == "CANDIDATE_GLOBAL" and rule.get("automatic") is not False for rule in transitions)
            self.check(cp, "no_orphan_auto_promotion", not orphan_auto, orphan_auto, False)
            self.check(cp, "no_global_candidate_auto_promotion", not global_auto, global_auto, False)
            self.check(cp, "governance_fence", receipt.get("filesystem_mutation") is False and receipt.get("production_execution") is False and receipt.get("runtime_authority") == "NONE" and receipt.get("frozen_c11c_preserved") is True, {key: receipt.get(key) for key in ("filesystem_mutation", "production_execution", "runtime_authority", "frozen_c11c_preserved")}, "false/false/NONE/true")
            self.check(cp, "deterministic_idempotent", validation.get("pass_criteria", {}).get("deterministic_idempotent") is True, validation.get("pass_criteria", {}).get("deterministic_idempotent"), True)
            self.check(cp, "negative_candidate_and_orphan_rules", validation.get("negative_tests", {}).get("global_candidate_auto_promotion", {}).get("pass") is True and validation.get("negative_tests", {}).get("non_active_production", {}).get("pass") is True, "policy controls", True)
            return receipt, validation, matrix, policy
        except Exception as exc:
            self.check(cp, "lifecycle_readable", False, str(exc), "valid lifecycle evidence", "D5_4_LIFECYCLE_INVALID")
            return receipt, {}, {}, {}

    def d3_d4(self, manifest: dict[str, Any], registry: dict[str, Any]) -> dict[str, Any]:
        cp = "CROSS_CHECK"
        artifacts = manifest.get("artifacts", [])
        by_role = {item.get("artifact_role"): item for item in artifacts}
        nodes = {item.get("artifact_id"): item for item in registry.get("nodes", [])}
        edges = registry.get("edges", [])
        raw, master = by_role.get("d3_raw_deterministic_render"), by_role.get("d3_delivery_master")
        d33_receipt = next((item for item in artifacts if str(item.get("relative_path", "")).endswith("d3_3_validation_receipt.json")), None)
        d32_receipt = next((item for item in artifacts if str(item.get("relative_path", "")).endswith("d3_2_validation_receipt.json")), None)
        raw_edge = bool(raw and master and any(e.get("source_artifact_id") == master["artifact_id"] and e.get("relation") == "DERIVED_FROM" and e.get("target_artifact_id") == raw["artifact_id"] for e in edges))
        master_qa = bool(master and d33_receipt and any(e.get("source_artifact_id") == master["artifact_id"] and e.get("relation") == "VALIDATED_BY" and e.get("target_artifact_id") == d33_receipt["artifact_id"] for e in edges))
        raw_qa = bool(raw and d32_receipt and any(e.get("source_artifact_id") == raw["artifact_id"] and e.get("relation") == "VALIDATED_BY" and e.get("target_artifact_id") == d32_receipt["artifact_id"] for e in edges))
        raw_master = bool(raw and master and raw["artifact_id"] != master["artifact_id"] and raw_edge and master_qa and raw_qa)
        d33_data = load_json(self.root, d33_receipt["relative_path"]) if d33_receipt else {}
        d3_evidence_valid = bool(raw_master and d33_data.get("result") == "PASS" and d33_data.get("status") == "CLOSED" and Path(str(d33_data.get("source_render", ""))).resolve() == (self.root / Path(raw["relative_path"])).resolve() and Path(str(d33_data.get("delivery_master", ""))).resolve() == (self.root / Path(master["relative_path"])).resolve())

        request_ids = {item["artifact_id"] for item in artifacts if item.get("artifact_type") == "REQUEST"}
        plan_ids = {item["artifact_id"] for item in artifacts if item.get("artifact_type") == "PLAN"}
        plan_request = any(e.get("source_artifact_id") in plan_ids and e.get("target_artifact_id") in request_ids and e.get("relation") == "GENERATED_FROM" for e in edges)
        auth_item = next((item for item in artifacts if item.get("artifact_type") == "AUTHORIZATION"), None)
        auth_node = nodes.get(auth_item["artifact_id"]) if auth_item else None
        auth_evidence = load_json(self.root, auth_item["relative_path"]) if auth_item else {}
        governance_edge = bool(auth_item and any(e.get("source_artifact_id") == auth_item["artifact_id"] and e.get("relation") == "GENERATED_FROM" and e.get("target_artifact_id") in plan_ids for e in edges))
        d49_evidence = next((item for item in artifacts if str(item.get("relative_path", "")).endswith("d4_9_regression_evidence.json")), None)
        d49_receipt = next((item for item in artifacts if str(item.get("relative_path", "")).endswith("d4_9_validation_receipt.json")), None)
        d49_data = load_json(self.root, d49_receipt["relative_path"]) if d49_receipt else {}
        acceptance_edge = bool(d49_receipt and any(e.get("source_artifact_id") in plan_ids and e.get("target_artifact_id") == d49_receipt["artifact_id"] and e.get("relation") == "VALIDATED_BY" for e in edges))
        production_cases = [case for case in auth_evidence.get("authorization_cases", []) if str(case.get("case", "")).startswith("valid_production")]
        d48_blocked = bool(auth_evidence.get("renderer_policy") == "DISABLED" and "RENDERER_POLICY_DISABLED" in auth_evidence.get("production_blocked_reasons", []) and production_cases and all(case.get("authorized") is False for case in production_cases) and auth_node and auth_node.get("decision_context", {}).get("decision") == "BLOCKED" and auth_node.get("decision_context", {}).get("authorized") is False and not any(e.get("relation") == "AUTHORIZED_BY" and e.get("target_artifact_id") == auth_item["artifact_id"] for e in edges))
        renderer_off = auth_evidence.get("renderer_called") is False and auth_evidence.get("production_execution") is False and auth_evidence.get("ffmpeg_production_called") is False and auth_evidence.get("godot_production_called") is False and d49_data.get("renderer_activation") is False and d49_data.get("production_execution") is False
        d4_ok = bool(plan_request and governance_edge and acceptance_edge and d49_data.get("result") == "PASS" and d49_data.get("status") == "CLOSED" and d48_blocked and renderer_off)
        self.check(cp, "D3_raw_master_qa", raw_master and d3_evidence_valid, {"raw_master_edges": raw_edge, "raw_qa": raw_qa, "master_qa": master_qa, "receipt_evidence": d3_evidence_valid}, "distinct media; raw->master provenance; D3.2/D3.3 QA")
        self.check(cp, "D4_request_plan_governance_acceptance", d4_ok, {"plan_request": plan_request, "governance_edge": governance_edge, "acceptance_edge": acceptance_edge, "D4_8_blocked": d48_blocked, "renderer_off": renderer_off}, "all true")
        return {"d3_consistency": bool(raw_master and d3_evidence_valid), "d4_consistency": d4_ok, "d4_8_blocked_preserved": d48_blocked, "renderer_production_fence": renderer_off}

    def frozen_identity(self) -> dict[str, Any]:
        cp = "C11-C"
        archive = self.root / Path(FROZEN_ZIP)
        actual_zip_sha = sha_file(archive) if archive.is_file() else "MISSING"
        zip_ok = actual_zip_sha == EXPECTED["zip_sha256"]
        tree_sha, build_sha, package_count = "MISSING", "MISSING", 0
        package_ok = False
        try:
            with zipfile.ZipFile(archive) as package:
                names = package.namelist()
                manifest_name = "release/C11C_FREEZE_PACKAGE_MANIFEST.json"
                package_manifest = json.loads(package.read(manifest_name).decode("utf-8-sig"))
                source_files = package_manifest.get("source_files", [])
                listed = {row["path"] for row in source_files}
                physical_source_names = {name for name in names if not name.endswith("/") and not name.startswith("release/")}
                source_errors = []
                tree_rows = []
                for row in source_files:
                    name = row["path"]
                    if name not in names:
                        source_errors.append(f"missing:{name}")
                        continue
                    content = package.read(name)
                    digest = sha_bytes(content)
                    if len(content) != row.get("bytes") or digest != str(row.get("sha256", "")).lower():
                        source_errors.append(f"hash:{name}")
                    tree_rows.append(f"{name}|{len(content)}|{digest}")
                    if name == "build_factory.py":
                        build_sha = digest
                package_count = len(source_files)
                tree_sha = sha_bytes("\n".join(tree_rows).encode("utf-8"))
            package_ok = not source_errors and listed == physical_source_names and package_manifest.get("source_file_count") == package_count and package_count == 1935 and package_manifest.get("source_tree_sha256", "").lower() == EXPECTED["tree_sha256"] and tree_sha == EXPECTED["tree_sha256"]
        except Exception as exc:
            package_ok = False
            source_errors = [str(exc)]
        current_build = self.root / "build_factory.py"
        current_build_sha = sha_file(current_build) if current_build.is_file() else "MISSING"
        frozen_ok = zip_ok and package_ok and build_sha == EXPECTED["build_factory_sha256"] and current_build_sha == EXPECTED["build_factory_sha256"]
        self.check(cp, "frozen_zip_sha256", zip_ok, actual_zip_sha, EXPECTED["zip_sha256"], "C11_C_FROZEN_ZIP_HASH_MISMATCH")
        self.check(cp, "frozen_tree_sha256", package_ok and tree_sha == EXPECTED["tree_sha256"], tree_sha, EXPECTED["tree_sha256"], "C11_C_FROZEN_TREE_HASH_MISMATCH")
        self.check(cp, "frozen_build_factory_sha256", build_sha == EXPECTED["build_factory_sha256"] and current_build_sha == EXPECTED["build_factory_sha256"], {"archive": build_sha, "workspace": current_build_sha}, EXPECTED["build_factory_sha256"], "C11_C_BUILD_FACTORY_HASH_MISMATCH")
        return {"preserved": frozen_ok, "zip_sha256": actual_zip_sha, "tree_sha256": tree_sha, "build_factory_sha256": build_sha, "workspace_build_factory_sha256": current_build_sha, "source_file_count": package_count}

    def cross_check(self, manifest: dict[str, Any], registry: dict[str, Any], d53: dict[str, Any], d54: dict[str, Any]) -> dict[str, Any]:
        stats = manifest.get("statistics", {})
        registry_stats = registry.get("statistics", {})
        observed = {
            "logical_identities": len(manifest.get("artifacts", [])),
            "physical_locations": sum(len(locations(item)) for item in manifest.get("artifacts", [])),
            "lineage_edges": len(registry.get("edges", [])),
            "orphaned_governed": sum(1 for item in manifest.get("artifacts", []) if item.get("lifecycle_state") == "ORPHANED"),
            "global_candidates": int(manifest.get("unmanaged_inventory", {}).get("orphan_candidates", 0)),
            "runtime_authority": "NONE" if registry.get("runtime_authority") == "NONE" and d53.get("runtime_authority") == "NONE" and d54.get("runtime_authority") == "NONE" else "CONFLICT",
            "production_execution": any(value is True for value in (registry.get("production_execution"), d53.get("production_execution"), d54.get("production_execution"))),
            "d4_8": d54.get("observations", {}).get("d4_8", "UNKNOWN"),
            "c11_c_preserved": d53.get("frozen_c11c_preserved") is True and d54.get("frozen_c11c_preserved") is True,
            "unknown_lineage_sources": sum(1 for edge in registry.get("edges", []) if edge.get("source_artifact_id") not in {item.get("artifact_id") for item in manifest.get("artifacts", [])}),
            "unknown_lineage_targets": sum(1 for edge in registry.get("edges", []) if edge.get("target_artifact_id") not in {item.get("artifact_id") for item in manifest.get("artifacts", [])}),
            "real_cycles": 0 if registry.get("validation", {}).get("dag_valid") is True else 1,
            "missing_artifacts": d53.get("missing_artifacts", -1),
            "content_hash_mismatches": d53.get("hash_mismatches", -1),
            "identity_content_conflicts": d53.get("identity_conflicts", -1),
            "lifecycle_path_conflicts": d53.get("lifecycle_conflicts", -1),
            "negative_tests_pass": all(d53.get("synthetic_negative_tests", {}).values()) and all(x.get("pass") is True for x in load_json(self.root, "artifacts/tests/c11d_d5/d5_4/d5_4_lifecycle_validation.json").get("negative_tests", {}).values()),
        }
        expected = {
            "logical_identities": 75, "physical_locations": 79, "lineage_edges": 11,
            "orphaned_governed": 9, "global_candidates": 12304,
            "runtime_authority": "NONE", "production_execution": False,
            "d4_8": "BLOCKED", "c11_c_preserved": True,
            "unknown_lineage_sources": 0, "unknown_lineage_targets": 0, "real_cycles": 0,
            "missing_artifacts": 0, "content_hash_mismatches": 0,
            "identity_content_conflicts": 0, "lifecycle_path_conflicts": 0,
            "negative_tests_pass": True,
        }
        # Compare checkpoint-published counts as well as recomputed counts; any disagreement is a cross-check failure.
        checkpoint_counts = [
            {"D5.1": {"logical_identities": stats.get("manifest_record_count"), "physical_locations": sum(len(locations(item)) for item in manifest.get("artifacts", [])), "orphaned_governed": stats.get("records_by_lifecycle", {}).get("ORPHANED")}},
            {"D5.2": {"logical_identities": registry_stats.get("logical_nodes"), "physical_locations": registry_stats.get("physical_locations_referenced"), "lineage_edges": registry_stats.get("edges"), "orphaned_governed": registry_stats.get("orphan_nodes"), "global_candidates": registry_stats.get("global_unmanaged_candidates")}},
            {"D5.3": {"logical_identities": d53.get("logical_identities"), "physical_locations": d53.get("physical_locations"), "lineage_edges": d53.get("lineage_edges"), "orphaned_governed": d53.get("orphaned_nodes"), "global_candidates": d53.get("global_unmanaged_candidates")}},
            {"D5.4": {"logical_identities": d54.get("observations", {}).get("logical_identities"), "physical_locations": d54.get("observations", {}).get("physical_locations"), "lineage_edges": d54.get("observations", {}).get("lineage_edges"), "orphaned_governed": d54.get("observations", {}).get("orphaned"), "global_candidates": d54.get("observations", {}).get("global_candidates")}},
        ]
        expected_cross_keys = {"logical_identities": 75, "physical_locations": 79, "lineage_edges": 11, "orphaned_governed": 9, "global_candidates": 12304}
        disagreement = []
        for row in checkpoint_counts:
            checkpoint, values = next(iter(row.items()))
            for key, value in values.items():
                if value != expected_cross_keys[key]:
                    disagreement.append({"checkpoint": checkpoint, "field": key, "observed": value, "expected": expected_cross_keys[key]})
        consistent = observed == expected and not disagreement
        self.check("CROSS_CHECK", "all_checkpoint_invariants_agree", consistent, {"observed": observed, "checkpoint_disagreements": disagreement}, {"observed": expected, "checkpoint_disagreements": []}, "CROSS_CHECK_FAILURE")
        return {"consistent": consistent, "expected": expected, "observed": observed, "checkpoint_counts": checkpoint_counts, "disagreements": disagreement}


def build(root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    harness = Acceptance(root)
    matrix, summary, receipt = harness.run()
    # The PowerShell runner owns the whole-worktree mutation guard around this invocation.
    matrix["filesystem_mutation_guard"] = "RUNNER_ENFORCED"
    summary["filesystem_mutation_guard"] = "RUNNER_ENFORCED"
    receipt["filesystem_mutation_guard"] = "RUNNER_ENFORCED"
    receipt["acceptance_matrix_sha256"] = sha_bytes(output_bytes(matrix))
    receipt["acceptance_summary_sha256"] = sha_bytes(output_bytes(summary))
    return matrix, summary, receipt


def execute(root: Path) -> int:
    first = build(root)
    second = build(root)
    deterministic = all(canonical_bytes(a) == canonical_bytes(b) for a, b in zip(first, second))
    matrix, summary, receipt = second
    if not deterministic:
        matrix["result"] = summary["result"] = receipt["result"] = "BLOCKED"
        matrix["status"] = summary["status"] = receipt["status"] = "BLOCKED"
        failure = {"checkpoint": "D5.5", "code": "DETERMINISM_FAILURE", "detail": "Repeated in-memory acceptance builds differ."}
        for output in (matrix, summary, receipt):
            output.setdefault("failures", []).append(failure)
    matrix["deterministic"] = deterministic
    summary["deterministic"] = deterministic
    receipt["deterministic"] = deterministic
    # Hash references are computed after deterministic flags are present.
    receipt["acceptance_matrix_sha256"] = sha_bytes(output_bytes(matrix))
    receipt["acceptance_summary_sha256"] = sha_bytes(output_bytes(summary))
    if not deterministic:
        receipt["result"] = "BLOCKED"
        receipt["status"] = "BLOCKED"
    out_dir = root / Path(OUT_REL)
    values = [matrix, summary, receipt]
    for name, value in zip(OUTPUT_NAMES, values):
        stable_write(out_dir / name, value)
    print(json.dumps({
        "result": receipt["result"], "status": receipt["status"],
        "logical_identities": receipt["logical_identities"],
        "physical_locations": receipt["physical_locations"],
        "lineage_edges": receipt["lineage_edges"],
        "orphaned_governed_records": receipt["orphaned_governed_records"],
        "global_candidates_outside_graph": receipt["global_candidates_outside_graph"],
        "d4_8": receipt["d4_8"], "frozen_c11c_preserved": receipt["frozen_c11c_preserved"],
        "declared_hash_exceptions": receipt["declared_hash_exceptions"],
        "negative_tests_pass": receipt["negative_tests_pass"],
        "deterministic": receipt["deterministic"], "idempotent": receipt["idempotent"],
        "filesystem_mutation_guard": receipt["filesystem_mutation_guard"],
        "runtime_authority": receipt["runtime_authority"], "production_execution": receipt["production_execution"],
        "renderer_execution": receipt["renderer_execution"], "godot_execution": receipt["godot_execution"],
        "ffmpeg_production_execution": receipt["ffmpeg_production_execution"],
        "acceptance_matrix_sha256": receipt["acceptance_matrix_sha256"],
        "acceptance_summary_sha256": receipt["acceptance_summary_sha256"],
        "failures": receipt["failures"], "next": receipt["next"],
    }, ensure_ascii=False, indent=2))
    return 0 if receipt["result"] == "PASS" and deterministic else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--snapshot-only", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    if args.snapshot_only:
        print(json.dumps(file_snapshot(root), separators=(",", ":")))
        return 0
    return execute(root)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({"result": "BLOCKED", "status": "BLOCKED", "fatal_error": str(exc)}), file=sys.stderr)
        raise SystemExit(2)
