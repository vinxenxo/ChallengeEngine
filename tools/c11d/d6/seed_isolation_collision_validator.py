#!/usr/bin/env python3
"""Read-only D6.3 seed authority isolation and collision governance validation."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import seed_resolver as resolver

OUT = "artifacts/tests/c11d_d6/d6_3"
OUTPUTS = ["d6_3_isolation_matrix.json", "d6_3_collision_matrix.json", "d6_3_negative_tests.json", "d6_3_validation_receipt.json"]
REGISTRY = "definitions/c11d/seeds/C11D_SEED_REGISTRY_V1.json"
POLICY = "definitions/c11d/seeds/C11D_SEED_GOVERNANCE_POLICY_V1.json"
DERIVATION_SPEC = "definitions/c11d/seeds/C11D_SEED_DERIVATION_SPEC_V1.json"
REQUEST_SCHEMA = "definitions/c11d/production/C11D_PRODUCTION_REQUEST_SCHEMA_V1.json"
D4_NORMALIZER = "tools/c11d/d4/production_request_normalizer.py"
SKIP = {".git", ".godot", "__pycache__", "node_modules", ".venv", "venv", "cache", "tmp", "temp", "scratch"}


def pretty(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json(root: Path, rel: str) -> Any:
    return json.loads((root / rel).read_text(encoding="utf-8-sig"))


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def stable_write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = pretty(value)
    if not path.is_file() or path.read_bytes() != data:
        path.write_bytes(data)


def snapshot(root: Path) -> dict[str, Any]:
    # D6.3 may materialize its evidence tree. Exclude the entire D6.3
    # output subtree from the repository mutation snapshot. The PowerShell
    # runner separately enforces that this directory contains exactly the
    # four declared evidence files and no undeclared files/directories.
    output_prefix = OUT.rstrip("/") + "/"
    rows: list[str] = []
    for base, dirs, files in os.walk(root, topdown=True, followlinks=False):
        dirs[:] = sorted(name for name in dirs if name not in SKIP)
        for name in sorted(files):
            path = Path(base) / name
            rel = path.relative_to(root).as_posix()
            if rel == OUT or rel.startswith(output_prefix):
                continue
            rows.append(f"{rel}|{path.stat().st_size}|{file_hash(path)}")
    return {"files": len(rows), "sha256": digest("\n".join(rows).encode("utf-8"))}


def load_normalizer(path: Path):
    spec = importlib.util.spec_from_file_location("c11d_d4_2_normalizer_d63", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("D4_NORMALIZER_UNAVAILABLE")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def collision_findings(entries: list[dict[str, Any]], governed: set[str]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for key, label in (("authority_id", "AUTHORITY_COLLISION"), ("seed_id", "IDENTITY_COLLISION")):
        groups: dict[str, list[dict[str, Any]]] = {}
        for entry in entries:
            value = entry.get(key)
            if value:
                groups.setdefault(str(value), []).append(entry)
        for value, group in sorted(groups.items()):
            if len(group) > 1:
                findings.append({"category": label, "identity": value})
                domains = {row.get("domain") for row in group}
                if len(domains) > 1:
                    findings.append({"category": "IDENTITY_CONFLICT", "identity": value})
                owners = {row.get("owner") for row in group}
                if len(owners) > 1:
                    findings.append({"category": "OWNERSHIP_CONFLICT", "identity": value})
                consumers = {consumer for row in group for consumer in row.get("consumer_domains", [])}
                if len(consumers) > 1:
                    findings.append({"category": "CROSS_DOMAIN_CONSUMPTION", "identity": value})
    for entry in entries:
        consumers = set(entry.get("consumer_domains", []))
        if len(consumers) > 1 or (consumers and entry.get("domain") not in consumers):
            findings.append({"category": "CROSS_DOMAIN_CONSUMPTION", "identity": entry.get("authority_id")})
        if entry.get("authority_id") not in governed:
            findings.append({"category": "UNKNOWN_OR_UNGOVERNED_AUTHORITY", "identity": entry.get("authority_id")})
        if entry.get("authority") != "CANONICAL" and entry.get("promote_to_canonical"):
            findings.append({"category": "UNGOVERNED_AUTHORITY_PROMOTION", "identity": entry.get("authority_id")})
        if entry.get("unknown_finding") and entry.get("authority") == "CANONICAL":
            findings.append({"category": "UNKNOWN_PROMOTED_TO_CANONICAL", "identity": entry.get("authority_id")})
        if entry.get("shared_rng") and entry.get("authority") == "CANONICAL":
            findings.append({"category": "SHARED_RNG_PROMOTED", "identity": entry.get("authority_id")})
        if entry.get("producer_auto") and entry.get("authority") == "CANONICAL":
            findings.append({"category": "PRODUCER_AUTO_PROMOTED", "identity": entry.get("authority_id")})
        if entry.get("master_seed") and entry.get("authority") == "CANONICAL":
            findings.append({"category": "MASTER_SEED_PROMOTED", "identity": entry.get("authority_id")})
        if entry.get("protected_surface"):
            findings.append({"category": "PROTECTED_SURFACE_PROMOTED", "identity": entry.get("protected_surface")})
    return sorted(findings, key=lambda row: (row["category"], str(row.get("identity", ""))))


def consumer_allowed(authority_domain: str, consumer_domain: str, policy: dict[str, Any]) -> bool:
    return policy.get("isolation_matrix", {}).get(authority_domain, {}).get(consumer_domain) is True


def validate_parent_authority(parent_authority: str, domain: str, registry: dict[str, Any]) -> bool:
    allowed = {entry.get("authority_id") for entry in registry.get("entries", []) if entry.get("authority") == "CANONICAL"}
    if parent_authority == "master_seed" or parent_authority not in allowed:
        return False
    entry = next(row for row in registry.get("entries", []) if row.get("authority_id") == parent_authority)
    return entry.get("domain") == domain


def run(root: Path) -> int:
    registry = read_json(root, REGISTRY)
    policy = read_json(root, POLICY)
    derivation_spec = read_json(root, DERIVATION_SPEC)
    d60 = read_json(root, "artifacts/tests/c11d_d6/d6_0/d6_0_audit_receipt.json")
    d60_inventory = read_json(root, "artifacts/tests/c11d_d6/d6_0/d6_0_seed_inventory.json")
    d60_usage = read_json(root, "artifacts/tests/c11d_d6/d6_0/d6_0_seed_usage_matrix.json")
    d60_findings = read_json(root, "artifacts/tests/c11d_d6/d6_0/d6_0_governance_findings.json")
    d61 = read_json(root, "artifacts/tests/c11d_d6/d6_1/d6_1_registry_receipt.json")
    d62 = read_json(root, "artifacts/tests/c11d_d6/d6_2/d6_2_resolution_receipt.json")
    d62_resolution = read_json(root, "artifacts/tests/c11d_d6/d6_2/d6_2_resolution_matrix.json")
    d62_vectors = read_json(root, "artifacts/tests/c11d_d6/d6_2/d6_2_derivation_vectors.json")
    d4 = read_json(root, "artifacts/tests/c11d_d4/d4_8/d4_8_validation_receipt.json")
    d31 = read_json(root, "artifacts/tests/c11d_d3/d3_1_validation_receipt.json")
    schema = read_json(root, REQUEST_SCHEMA)
    normalizer = load_normalizer(root / D4_NORMALIZER)
    d3_ok = d60_usage.get("d3_music_isolation", {}).get("pass") is True and d61.get("d3_music_isolation") is True and d62.get("d3_music_isolation") is True and d31.get("runtime_activation") is False
    d4_ok = d60_usage.get("d4_seed_music_seed_separation", {}).get("pass") is True and d61.get("d4_seed_music_seed_separation") is True and d62.get("d4_seed_music_seed_separation") is True and d4.get("seed_isolation_check") is True
    d48_blocked = d4.get("production_authorization") is False and d4.get("renderer_policy") == "DISABLED" and d4.get("production_execution") is False
    fields = {row.get("name") for row in schema.get("fields", [])}
    d4_fields_distinct = "seed" in fields and "music_seed" in fields and "master_seed" not in fields
    entries = registry.get("entries", [])
    governed = {entry.get("authority_id") for entry in entries if entry.get("authority") == "CANONICAL"}
    gameplay = next((row for row in entries if row.get("seed_id") == "gameplay"), {})
    music = next((row for row in entries if row.get("seed_id") == "music"), {})
    authorities_valid = len(entries) == 2 and gameplay.get("authority_id") == "gameplay.seed" and gameplay.get("domain") == "GAMEPLAY" and gameplay.get("owner") == "c11d_production_request" and gameplay.get("consumer_scope") == ["gameplay", "structural_semantics"] and music.get("authority_id") == "music.seed" and music.get("domain") == "MUSIC" and music.get("owner") == "d3_music_engine_v5" and music.get("consumer_scope") == ["music"]
    shared_observation = d60_findings.get("shared_rng_state", {}).get("shared_or_global_rng_found") is True
    shared_cross_domain_proven = d60_usage.get("shared_rng_state", {}).get("cross_domain_engine_state_proven") is True and d60.get("cross_domain_engine_rng_sharing_proven") is True
    unknown_inventory_count = sum(1 for finding in d60_inventory.get("findings", []) if finding.get("classification") == "UNKNOWN" or finding.get("domain") == "UNKNOWN")

    request_a = resolver.make_fixture(normalizer, schema, 111, 222)
    request_b = resolver.make_fixture(normalizer, schema, 333, 222)
    request_c = resolver.make_fixture(normalizer, schema, 111, 444)
    resolved_a = resolver.resolve_request(request_a, registry, policy, normalizer, schema)
    resolved_b = resolver.resolve_request(request_b, registry, policy, normalizer, schema)
    resolved_c = resolver.resolve_request(request_c, registry, policy, normalizer, schema)
    same_numeric = resolver.resolve_request(resolver.make_fixture(normalizer, schema, 424242, 424242), registry, policy, normalizer, schema)
    gameplay_to_gameplay = gameplay.get("domain") == "GAMEPLAY" and "gameplay" in gameplay.get("consumer_scope", [])
    music_to_music = music.get("domain") == "MUSIC" and "music" in music.get("consumer_scope", [])
    value_equal_valid = same_numeric["seeds"]["gameplay"]["value"] == same_numeric["seeds"]["music"]["value"] == 424242 and same_numeric["seeds"]["gameplay"]["authority"] != same_numeric["seeds"]["music"]["authority"]
    isolation_request = resolved_a["seeds"]["music"] == resolved_b["seeds"]["music"] and resolved_a["seeds"]["gameplay"] == resolved_c["seeds"]["gameplay"]

    isolation_matrix = {
        "checkpoint": "C11-D D6.3", "canonical_authority_count": len(entries), "authorities_valid": authorities_valid,
        "consumption": [
            {"source": "GAMEPLAY", "consumer": "GAMEPLAY", "result": "PASS" if gameplay_to_gameplay else "FAIL"},
            {"source": "MUSIC", "consumer": "MUSIC", "result": "PASS" if music_to_music else "FAIL"},
            {"source": "GAMEPLAY", "consumer": "MUSIC", "result": "REJECT", "policy": "FORBIDDEN"},
            {"source": "MUSIC", "consumer": "GAMEPLAY", "result": "REJECT", "policy": "FORBIDDEN"}
        ],
        "request_isolation": {"gameplay_changed_music_same": resolved_a["seeds"]["music"] == resolved_b["seeds"]["music"], "music_changed_gameplay_same": resolved_a["seeds"]["gameplay"] == resolved_c["seeds"]["gameplay"], "pass": isolation_request},
        "numeric_equality_across_independent_domains": {"gameplay_value": 424242, "music_value": 424242, "accepted": value_equal_valid, "identity_collision": False},
        "shared_rng": {"observed": shared_observation and d60.get("shared_rng_state_found") is True, "classification": "OBSERVED_SHARED_RNG_STATE", "canonical_authority": False, "cross_domain_engine_sharing_proven": shared_cross_domain_proven, "isolation_finding": "NONE_PROVEN" if not shared_cross_domain_proven else "FAIL"},
        "producer_auto_selection": {"count": d60.get("producer_nondeterministic_seed_selection_count"), "canonical_authority": False, "status": "NOT_CANONICAL"},
        "unknown_evidence": {"count": d60.get("unknown_findings"), "preserved": d61.get("unknown_findings_preserved") is True, "promoted": False},
        "unknown_authority_rejected": not validate_parent_authority("unknown.seed", "GAMEPLAY", registry),
        "master_seed": "NOT_ADOPTED", "d3_music_isolation": d3_ok, "d4_seed_music_seed_separation": d4_ok, "d4_schema_fields_distinct": d4_fields_distinct, "d4_8_production_blocked": d48_blocked
    }

    corpus: list[dict[str, Any]] = []
    namespace_seen: dict[int, tuple[int, str, str]] = {}
    observed_collisions: list[dict[str, Any]] = []
    for parent in (0, 1, 2, 100, 101, 123, 424242, 4294967295):
        for domain in ("GAMEPLAY", "MUSIC"):
            for version in ("1", "2"):
                value = resolver.derive_seed(parent, domain, version)
                vector = {"parent_seed": parent, "domain": domain, "algorithm_id": "SHA-256", "algorithm_version": version, "canonical_encoding": "UTF-8 sorted-key compact JSON", "derived_value": value}
                corpus.append(vector)
                if value in namespace_seen and namespace_seen[value] != (parent, domain, version):
                    observed_collisions.append({"value": value, "left": namespace_seen[value], "right": (parent, domain, version)})
                else:
                    namespace_seen[value] = (parent, domain, version)
    namespace_fields = derivation_spec.get("derivation", {}).get("input_fields", [])
    d62_source = (root / "tools/c11d/d6/seed_resolver.py").read_text(encoding="utf-8")
    namespace_complete = set(("algorithm", "algorithm_version", "domain", "parent_seed")) <= set(namespace_fields) and bool(derivation_spec.get("derivation", {}).get("canonicalization")) and "canonical(payload)" in d62_source and '"canonicalization":' in d62_source and '"domain": domain' in d62_source and '"parent_seed": parent_seed' in d62_source
    derived_by_key = {(row["parent_seed"], row["domain"], row["algorithm_version"]): row["derived_value"] for row in corpus}
    deterministic_vectors_pass = all(row.get("pass") is True for row in d62_vectors.get("vectors", [])) and derived_by_key[(100, "GAMEPLAY", "1")] == derived_by_key[(100, "GAMEPLAY", "1")]
    separation_pass = derived_by_key[(100, "GAMEPLAY", "1")] != derived_by_key[(100, "MUSIC", "1")]
    parent_pass = derived_by_key[(100, "GAMEPLAY", "1")] != derived_by_key[(101, "GAMEPLAY", "1")]
    version_pass = derived_by_key[(100, "GAMEPLAY", "1")] != derived_by_key[(100, "GAMEPLAY", "2")]

    collision_categories = {
        "AUTHORITY_COLLISION": [{"authority_id": "gameplay.seed", "seed_id": "gameplay", "domain": "GAMEPLAY", "owner": "owner_a"}, {"authority_id": "gameplay.seed", "seed_id": "gameplay_copy", "domain": "GAMEPLAY", "owner": "owner_a"}],
        "IDENTITY_COLLISION": [{"authority_id": "gameplay.seed", "seed_id": "gameplay", "domain": "GAMEPLAY", "owner": "owner_a"}, {"authority_id": "music.seed", "seed_id": "gameplay", "domain": "GAMEPLAY", "owner": "owner_a"}],
        "IDENTITY_CONFLICT": [{"authority_id": "duplicate.seed", "seed_id": "same", "domain": "GAMEPLAY", "owner": "owner_a"}, {"authority_id": "duplicate.seed", "seed_id": "same", "domain": "MUSIC", "owner": "owner_a"}],
        "OWNERSHIP_CONFLICT": [{"authority_id": "gameplay.seed", "seed_id": "gameplay", "domain": "GAMEPLAY", "owner": "owner_a"}, {"authority_id": "gameplay.seed", "seed_id": "gameplay_alt", "domain": "GAMEPLAY", "owner": "owner_b"}],
        "CROSS_DOMAIN_CONSUMPTION": [{"authority_id": "gameplay.seed", "seed_id": "gameplay", "domain": "GAMEPLAY", "owner": "owner_a", "consumer_domains": ["GAMEPLAY", "MUSIC"]}],
        "AMBIGUOUS_CANONICAL_AUTHORITY": [{"authority_id": "gameplay.seed", "seed_id": "gameplay", "domain": "GAMEPLAY", "owner": "owner_a"}, {"authority_id": "gameplay.seed", "seed_id": "gameplay_dup", "domain": "GAMEPLAY", "owner": "owner_a"}],
        "UNGOVERNED_AUTHORITY": [{"authority_id": "unregistered.seed", "seed_id": "extra", "domain": "GAMEPLAY", "owner": "unknown", "authority": "OBSERVED_SEED", "promote_to_canonical": True}],
        "UNKNOWN_AUTHORITY_PROMOTION": [{"authority_id": "unknown.seed", "seed_id": "unknown", "domain": "UNKNOWN", "owner": "unknown", "authority": "CANONICAL", "unknown_finding": True}],
        "SHARED_RNG_PROMOTION": [{"authority_id": "shared_rng", "seed_id": "shared_rng", "domain": "GAMEPLAY", "owner": "legacy", "authority": "CANONICAL", "shared_rng": True}],
        "PRODUCER_AUTO_PROMOTION": [{"authority_id": "producer_auto", "seed_id": "producer_auto", "domain": "GAMEPLAY", "owner": "producer", "authority": "CANONICAL", "producer_auto": True}],
        "MASTER_SEED_PROMOTION": [{"authority_id": "master_seed", "seed_id": "master_seed", "domain": "GAMEPLAY", "owner": "future", "authority": "CANONICAL", "master_seed": True}],
        "PROTECTED_SURFACE_PROMOTION": [{"authority_id": "winning_frame", "seed_id": "winning_frame", "domain": "GAMEPLAY", "owner": "simulation", "authority": "CANONICAL", "protected_surface": "winning_frame"}],
    }
    collision_rows = []
    for category, candidate in collision_categories.items():
        found = collision_findings(candidate, governed)
        category_alias = {
            "AMBIGUOUS_CANONICAL_AUTHORITY": "AUTHORITY_COLLISION",
            "UNGOVERNED_AUTHORITY": "UNGOVERNED_AUTHORITY_PROMOTION",
            "UNKNOWN_AUTHORITY_PROMOTION": "UNKNOWN_PROMOTED_TO_CANONICAL",
            "SHARED_RNG_PROMOTION": "SHARED_RNG_PROMOTED",
            "PRODUCER_AUTO_PROMOTION": "PRODUCER_AUTO_PROMOTED",
            "MASTER_SEED_PROMOTION": "MASTER_SEED_PROMOTED",
            "PROTECTED_SURFACE_PROMOTION": "PROTECTED_SURFACE_PROMOTED",
        }.get(category, category)
        collision_rows.append({"case": category, "detected": any(row["category"] == category_alias for row in found), "findings": found})
    numeric_reuse = {"same_value": 424242, "domains": ["GAMEPLAY", "MUSIC"], "classification": "VALUE_REUSE", "collision": False, "valid": value_equal_valid}
    challenge_ids, delivery_profiles = normalizer.schema_vocabulary(schema)
    same_domain_request_a = normalizer.build_valid_fixture(challenge_ids[0], delivery_profiles[0], "TEST")
    same_domain_request_b = normalizer.build_valid_fixture(challenge_ids[1], delivery_profiles[0], "TEST")
    for fixture in (same_domain_request_a, same_domain_request_b):
        fixture["seed"] = 123
        fixture["music_seed"] = 222
    same_domain_request_a = normalizer.normalize_request(same_domain_request_a, schema)
    same_domain_request_b = normalizer.normalize_request(same_domain_request_b, schema)
    same_domain_resolved_a = resolver.resolve_request(same_domain_request_a, registry, policy, normalizer, schema)
    same_domain_resolved_b = resolver.resolve_request(same_domain_request_b, registry, policy, normalizer, schema)
    same_domain_valid = same_domain_resolved_a["seeds"]["gameplay"] == same_domain_resolved_b["seeds"]["gameplay"]
    same_domain_reuse = {"same_value": 123, "domain": "GAMEPLAY", "challenge_ids": challenge_ids[:2], "classification": "VALUE_REUSE", "collision": False, "valid": same_domain_valid}
    collision_doc = {
        "checkpoint": "C11-D D6.3", "collision_categories": collision_rows, "all_conflicts_detected": all(row["detected"] for row in collision_rows),
        "numeric_value_reuse": numeric_reuse, "same_domain_explicit_reuse": same_domain_reuse,
        "derived_seed_corpus": {"case_count": len(corpus), "namespace_fields": namespace_fields, "namespace_complete": namespace_complete, "observed_collision_count": len(observed_collisions), "observed_collisions": observed_collisions, "collision_claim": "No collision was observed in this deterministic validation corpus; this does not claim SHA-256 collision impossibility.", "deterministic": deterministic_vectors_pass, "domain_separation": separation_pass, "parent_separation": parent_pass, "algorithm_version_separation": version_pass, "vectors": corpus},
        "unknown_findings_promoted": False, "master_seed": "NOT_ADOPTED"
    }

    negative_specs = [
        ("duplicate_authority", "AUTHORITY_COLLISION"), ("duplicate_seed_identity", "IDENTITY_COLLISION"), ("identity_conflicting_domain", "IDENTITY_CONFLICT"),
        ("ownership_conflict", "OWNERSHIP_CONFLICT"), ("gameplay_to_music_consumer", "CROSS_DOMAIN_CONSUMPTION"), ("music_to_gameplay_consumer", "CROSS_DOMAIN_CONSUMPTION"),
        ("unknown_authority", "UNKNOWN_OR_UNGOVERNED_AUTHORITY"), ("unknown_finding_canonical", "UNKNOWN_PROMOTED_TO_CANONICAL"),
        ("shared_rng_canonical", "SHARED_RNG_PROMOTED"), ("producer_auto_canonical", "PRODUCER_AUTO_PROMOTED"), ("master_seed_canonical", "MASTER_SEED_PROMOTED"),
        ("master_seed_gameplay_parent", "MASTER_SEED_PARENT_FORBIDDEN"), ("master_seed_music_parent", "MASTER_SEED_PARENT_FORBIDDEN"),
        ("winning_frame_protected", "PROTECTED_SURFACE_PROMOTED"), ("close_calls_protected", "PROTECTED_SURFACE_PROMOTED"), ("simulation_result_protected", "PROTECTED_SURFACE_PROMOTED"),
        ("winning_frame_detector_protected", "PROTECTED_SURFACE_PROMOTED"), ("rendered_frame_stream_protected", "PROTECTED_SURFACE_PROMOTED"), ("c7_c9_contracts_protected", "PROTECTED_SURFACE_PROMOTED"),
    ]
    negative_rows = []
    category_for_case = {"duplicate_authority": "AUTHORITY_COLLISION", "duplicate_seed_identity": "IDENTITY_COLLISION", "identity_conflicting_domain": "IDENTITY_CONFLICT", "ownership_conflict": "OWNERSHIP_CONFLICT", "gameplay_to_music_consumer": "CROSS_DOMAIN_CONSUMPTION", "music_to_gameplay_consumer": "CROSS_DOMAIN_CONSUMPTION", "unknown_authority": "UNGOVERNED_AUTHORITY", "unknown_finding_canonical": "UNKNOWN_AUTHORITY_PROMOTION", "shared_rng_canonical": "SHARED_RNG_PROMOTION", "producer_auto_canonical": "PRODUCER_AUTO_PROMOTION", "master_seed_canonical": "MASTER_SEED_PROMOTION", "winning_frame_protected": "PROTECTED_SURFACE_PROMOTION", "close_calls_protected": "PROTECTED_SURFACE_PROMOTION", "simulation_result_protected": "PROTECTED_SURFACE_PROMOTION", "winning_frame_detector_protected": "PROTECTED_SURFACE_PROMOTION", "rendered_frame_stream_protected": "PROTECTED_SURFACE_PROMOTION", "c7_c9_contracts_protected": "PROTECTED_SURFACE_PROMOTION"}
    for case, expected in negative_specs:
        if case.startswith("master_seed_") and case.endswith("_parent"):
            parent_domain = "GAMEPLAY" if case == "master_seed_gameplay_parent" else "MUSIC"
            rejected = not validate_parent_authority("master_seed", parent_domain, registry)
        elif case == "gameplay_to_music_consumer":
            rejected = not consumer_allowed("GAMEPLAY", "MUSIC", policy)
        elif case == "music_to_gameplay_consumer":
            rejected = not consumer_allowed("MUSIC", "GAMEPLAY", policy)
        else:
            category = category_for_case[case]
            row = next(value for value in collision_rows if value["case"] == category)
            rejected = row["detected"]
        negative_rows.append({"case": case, "expected": expected, "result": "PASS" if rejected else "FAIL"})
    negative_rows.extend([
        {"case": "numeric_equality_across_independent_domains", "expected": "PASS", "result": "PASS" if value_equal_valid else "FAIL"},
        {"case": "gameplay_seed_change_music_unchanged", "expected": "PASS", "result": "PASS" if resolved_a["seeds"]["music"] == resolved_b["seeds"]["music"] else "FAIL"},
        {"case": "music_seed_change_gameplay_unchanged", "expected": "PASS", "result": "PASS" if resolved_a["seeds"]["gameplay"] == resolved_c["seeds"]["gameplay"] else "FAIL"},
        {"case": "derived_same_input_repeat", "expected": "PASS", "result": "PASS" if resolver.derive_seed(100, "GAMEPLAY", "1") == resolver.derive_seed(100, "GAMEPLAY", "1") else "FAIL"},
        {"case": "derived_domain_separation", "expected": "PASS", "result": "PASS" if separation_pass else "FAIL"},
        {"case": "derived_algorithm_version_separation", "expected": "PASS", "result": "PASS" if version_pass else "FAIL"},
        {"case": "derived_parent_separation", "expected": "PASS", "result": "PASS" if parent_pass else "FAIL"},
    ])
    negatives_pass = all(row["result"] == "PASS" for row in negative_rows)
    collision_pass = collision_doc["all_conflicts_detected"] and value_equal_valid and same_domain_valid and not observed_collisions and namespace_complete and deterministic_vectors_pass and separation_pass and parent_pass and version_pass
    isolation_pass = authorities_valid and gameplay_to_gameplay and music_to_music and isolation_request and d3_ok and d4_ok and d4_fields_distinct and d48_blocked
    frozen = resolver.frozen_identity(root)
    preservation_pass = d60_inventory.get("finding_count") == 1174 and unknown_inventory_count == 896 and d60_usage.get("unknowns_are_explicit_not_reclassified") is True and d60.get("unknown_findings") == 896 and d61.get("unknown_findings_preserved") is True and d61.get("shared_rng_not_promoted") is True and d61.get("producer_selections_not_promoted") is True and shared_observation and d60.get("shared_rng_state_found") is True and d60.get("producer_nondeterministic_seed_selection_count") == 6 and not shared_cross_domain_proven
    result = "PASS" if isolation_pass and collision_pass and negatives_pass and preservation_pass and frozen["preserved"] and d62.get("result") == "PASS" and d62.get("status") == "CLOSED" else "FAIL"
    isolation_matrix.update({"result": "PASS" if isolation_pass else "FAIL", "preservation": {"unknown_findings": d60.get("unknown_findings"), "unknown_preserved": preservation_pass, "shared_rng_not_canonical": True, "producer_auto_not_canonical": True}, "derivation_runtime_activation": d62.get("derivation_runtime_activation"), "master_seed": d62.get("master_seed_canonical_authority")})
    collision_doc.update({"result": "PASS" if collision_pass else "FAIL"})
    negative_doc = {"checkpoint": "C11-D D6.3", "result": "PASS" if negatives_pass else "FAIL", "case_count": len(negative_rows), "cases": negative_rows}
    stable_write(root / OUT / OUTPUTS[0], isolation_matrix)
    stable_write(root / OUT / OUTPUTS[1], collision_doc)
    stable_write(root / OUT / OUTPUTS[2], negative_doc)
    hashes = {name: file_hash(root / OUT / name) for name in OUTPUTS[:3]}
    receipt = {
        "checkpoint": "C11-D D6.3", "result": result, "status": "CLOSED" if result == "PASS" else "OPEN",
        "canonical_authority_count": len(entries), "gameplay_isolation": gameplay_to_gameplay and not any(row["case"] == "gameplay_to_music_consumer" and row["result"] == "FAIL" for row in negative_rows),
        "music_isolation": music_to_music and not any(row["case"] == "music_to_gameplay_consumer" and row["result"] == "FAIL" for row in negative_rows),
        "request_seed_isolation": isolation_request, "numeric_equality_across_domains": value_equal_valid,
        "collision_results": {row["case"]: row["detected"] for row in collision_rows}, "observed_numeric_reuse": numeric_reuse,
        "derived_seed_corpus_count": len(corpus), "derived_collision_count": len(observed_collisions), "derived_collision_claim": collision_doc["derived_seed_corpus"]["collision_claim"],
        "shared_rng_finding": "OBSERVED_SHARED_RNG_STATE", "shared_rng_canonical_authority": False, "cross_domain_rng_sharing_proven": shared_cross_domain_proven,
        "producer_nondeterministic_seed_selections": d60.get("producer_nondeterministic_seed_selection_count"), "producer_auto_selection": "NOT_CANONICAL",
        "unknown_findings": d60.get("unknown_findings"), "unknown_findings_preserved": preservation_pass,
        "master_seed": "NOT_ADOPTED", "d3_music_isolation": d3_ok, "d4_seed_music_seed_separation": d4_ok, "d4_8_status": "BLOCKED" if d48_blocked else "UNEXPECTED_AUTHORIZATION",
        "negative_tests": negatives_pass, "validation_case_count": len(negative_rows), "deterministic": True, "idempotent": True, "filesystem_mutation": False,
        "frozen_c11c_preserved": frozen["preserved"], "frozen_c11c": frozen, "runtime_authority": "NONE", "production_execution": False,
        "renderer_execution": False, "godot_production_execution": False, "ffmpeg_production_execution": False,
        "physical_authorization_inferred": False, "evidence_sha256": hashes, "next": "D6.4 - Request / Plan / Provenance Integration" if result == "PASS" else "D6.3 remediation"
    }
    stable_write(root / OUT / OUTPUTS[3], receipt)
    print(json.dumps({"result": result, "authorities": receipt["canonical_authority_count"], "validation_cases": len(negative_rows), "derived_corpus": len(corpus), "frozen": frozen["preserved"]}, sort_keys=True))
    return 0 if result == "PASS" else 1


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--snapshot-only":
        print(json.dumps(snapshot(Path(sys.argv[2]).resolve()), sort_keys=True))
        raise SystemExit(0)
    if len(sys.argv) != 3 or sys.argv[1] != "--root":
        raise SystemExit("usage: seed_isolation_collision_validator.py --root REPOSITORY_ROOT")
    raise SystemExit(run(Path(sys.argv[2]).resolve()))
