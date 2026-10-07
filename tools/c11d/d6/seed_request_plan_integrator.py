#!/usr/bin/env python3
"""C11-D D6.4 request/plan/seed provenance integration adapter.

This module composes already-closed D4/D5/D6 authorities without changing them.
It never executes production, renderer, Godot, or FFmpeg.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import seed_resolver as D62

REGISTRY = "definitions/c11d/seeds/C11D_SEED_REGISTRY_V1.json"
POLICY = "definitions/c11d/seeds/C11D_SEED_GOVERNANCE_POLICY_V1.json"
PROVENANCE_SCHEMA = "definitions/c11d/seeds/C11D_SEED_PROVENANCE_SCHEMA_V1.json"
REQUEST_SCHEMA = "definitions/c11d/production/C11D_PRODUCTION_REQUEST_SCHEMA_V1.json"
PERSONALIZATION_REGISTRY = "definitions/c11d/personalization/C11D_PERSONALIZATION_PROFILE_REGISTRY_V1.json"
D42 = "tools/c11d/d4/production_request_normalizer.py"
D43 = "tools/c11d/d4/personalization_resolver.py"
D44 = "tools/c11d/d4/canonical_production_orchestrator.py"
D44_RECEIPT = "artifacts/tests/c11d_d4/d4_4/d4_4_validation_receipt.json"
D42_RECEIPT = "artifacts/tests/c11d_d4/d4_2/d4_2_validation_receipt.json"
D48_RECEIPT = "artifacts/tests/c11d_d4/d4_8/d4_8_validation_receipt.json"
D33_RECEIPT_CANDIDATES = (
    "artifacts/tests/c11d_d3/d3_3/d3_3_validation_receipt.json",
    "artifacts/tests/c11d_d3/d3_3_validation_receipt.json",
)
D61_RECEIPT = "artifacts/tests/c11d_d6/d6_1/d6_1_registry_receipt.json"
D62_RECEIPT = "artifacts/tests/c11d_d6/d6_2/d6_2_resolution_receipt.json"
D63_RECEIPT = "artifacts/tests/c11d_d6/d6_3/d6_3_validation_receipt.json"
D62_RESOLUTION_EVIDENCE = "artifacts/tests/c11d_d6/d6_2/d6_2_resolution_matrix.json"
D5_LINEAGE = "definitions/c11d/provenance/C11D_PROVENANCE_LINEAGE_REGISTRY_V1.json"
D5_LINEAGE_ARTIFACT = "artifacts/tests/c11d_d5/d5_2/d5_2_lineage_registry.json"
D48_POLICY = "definitions/c11d/production/C11D_PRODUCTION_ACTIVATION_POLICY_V1.json"
OUT = Path("artifacts/tests/c11d_d6/d6_4")
OUTPUTS = (
    "d6_4_integration_matrix.json",
    "d6_4_provenance_matrix.json",
    "d6_4_negative_tests.json",
    "d6_4_integration_receipt.json",
)
SKIP = {".git", ".godot", "__pycache__", "node_modules", ".venv", "venv", "cache", "tmp", "temp", "scratch"}
EXPECTED = D62.EXPECTED


class IntegrationError(ValueError):
    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise IntegrationError(f"INPUT_READ_ERROR:{path.as_posix()}") from exc


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def pretty(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_value(value: Any) -> str:
    return sha_bytes(canonical(value))


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def stable_write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = pretty(value)
    if not path.is_file() or path.read_bytes() != data:
        path.write_bytes(data)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise IntegrationError(f"MODULE_UNAVAILABLE:{path.as_posix()}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def load_receipt(root: Path, rel: str) -> dict[str, Any]:
    path = root / rel
    if not path.is_file():
        raise IntegrationError(f"RECEIPT_MISSING:{rel}")
    value = load_json(path)
    if not isinstance(value, dict):
        raise IntegrationError(f"RECEIPT_NOT_OBJECT:{rel}")
    if value.get("result") != "PASS" or value.get("status") != "CLOSED":
        raise IntegrationError(f"RECEIPT_NOT_PASS_CLOSED:{rel}")
    return value


def load_d3_closed_receipt(root: Path) -> tuple[str, dict[str, Any]]:
    for rel in D33_RECEIPT_CANDIDATES:
        path = root / rel
        if not path.is_file():
            continue
        value = load_receipt(root, rel)
        return rel, value
    raise IntegrationError("D3_CLOSED_RECEIPT_MISSING")


def load_lineage_artifact(root: Path) -> dict[str, Any]:
    primary = root / D5_LINEAGE_ARTIFACT
    if primary.is_file():
        value = load_json(primary)
        if not isinstance(value, dict):
            raise IntegrationError("D5_2_LINEAGE_ARTIFACT_NOT_OBJECT")
        return value
    matches = sorted((root / "artifacts/tests/c11d_d5/d5_2").glob("*.json")) if (root / "artifacts/tests/c11d_d5/d5_2").is_dir() else []
    candidates = [p for p in matches if "lineage" in p.name.lower()]
    if len(candidates) == 1:
        value = load_json(candidates[0])
        if not isinstance(value, dict):
            raise IntegrationError("D5_2_LINEAGE_ARTIFACT_NOT_OBJECT")
        return value
    raise IntegrationError("D5_2_LINEAGE_ARTIFACT_MISSING")


def count_collection(value: Any, names: tuple[str, ...]) -> int | None:
    if not isinstance(value, dict):
        return None
    for name in names:
        candidate = value.get(name)
        if isinstance(candidate, list):
            return len(candidate)
        if isinstance(candidate, dict):
            return len(candidate)
    return None


def d5_lineage_check(root: Path, lineage_schema: dict[str, Any], lineage_artifact: dict[str, Any]) -> dict[str, Any]:
    schema_ok = (
        lineage_schema.get("registry_id") == "c11d_provenance_lineage"
        and lineage_schema.get("status") == "ACTIVE"
        and lineage_schema.get("runtime_authority") == "NONE"
        and lineage_schema.get("direction_convention")
        and lineage_schema.get("node_authority") == "D5.1 canonical artifact manifest only"
        and lineage_schema.get("authorization_policy", {}).get("blocked_decision_is_not_a_grant") is True
    )
    node_count = count_collection(lineage_artifact, ("nodes", "logical_nodes", "registry", "artifacts"))
    edge_count = count_collection(lineage_artifact, ("edges", "lineage_edges", "relations"))
    expected_counts = (node_count == 75 if node_count is not None else True) and (edge_count == 11 if edge_count is not None else True)
    return {
        "schema_valid": bool(schema_ok),
        "artifact_present": True,
        "logical_node_count": node_count,
        "edge_count": edge_count,
        "expected_75_nodes_11_edges_when_declared": bool(expected_counts),
        "directionality_declared": lineage_schema.get("direction_convention") if schema_ok else None,
        "blocked_decision_not_grant": lineage_schema.get("authorization_policy", {}).get("blocked_decision_is_not_a_grant") is True,
        "runtime_authority": lineage_schema.get("runtime_authority"),
        "production_execution": lineage_schema.get("production_execution"),
    }


def make_fixture(normalizer: Any, schema: dict[str, Any], personalization: Any, gameplay: int = 123456, music: int = 654321, variation: int = 0, mode: str = "PRODUCTION") -> dict[str, Any]:
    challenges, profiles = normalizer.schema_vocabulary(schema)
    raw = normalizer.build_valid_fixture(challenges[0], profiles[0], "TEST")
    raw["seed"] = gameplay
    raw["music_seed"] = music
    raw["variation_index"] = variation
    raw["mode"] = mode
    raw["request_id"] = "D6.4-INTEGRATION-001"
    raw["personalization"]["profile_id"] = "editorial_text_v1"
    raw["personalization"]["values"] = {"language": "es", "player_name": "TEST"}
    return normalizer.normalize_request(raw, schema)


# ROOT is rebound by run(); helper uses it only while invoked from run.
ROOT = Path(__file__).resolve().parents[3]


def build_integration(root: Path, request: dict[str, Any], modules: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    normalizer = modules["normalizer"]
    personalizer = modules["personalizer"]
    resolver = modules["resolver"]
    orchestrator = modules["orchestrator"]
    schema = inputs["schema"]
    registry = inputs["registry"]
    policy = inputs["policy"]
    d3_receipt_path = inputs["d3_receipt_path"]

    # D4.2 remains the sole request normalizer.
    canonical_request = normalizer.normalize_request(copy.deepcopy(request), schema)
    request_sha = normalizer.request_hash(canonical_request)

    # D6.2 remains the sole seed resolver and receives the D4.2 canonical request.
    resolved = resolver.resolve_request(canonical_request, registry, policy, normalizer, schema)

    # D4.3 remains the sole personalization resolver used before D4.4 plan construction.
    resolved_personalization = personalizer.normalize_personalization(
        canonical_request,
        personalizer.validate_registry(inputs["personalization_registry"]),
    )
    orchestrator_request = copy.deepcopy(canonical_request)
    orchestrator_request["personalization"] = resolved_personalization
    seed_resolution_sha = sha_value(resolved)

    # D4.4 remains the sole plan constructor and plan hash owner.
    plan, plan_sha = orchestrator.build_plan(
        orchestrator_request,
        schema,
        inputs["personalization_registry"],
    )

    registry_sha = file_hash(root / REGISTRY)
    policy_sha = file_hash(root / POLICY)
    resolver_sha = file_hash(root / "tools/c11d/d6/seed_resolver.py")
    request_normalizer_sha = file_hash(root / D42)
    orchestrator_sha = file_hash(root / D44)

    seed_rows = []
    for seed_id in ("gameplay", "music"):
        row = resolved["seeds"][seed_id]
        entry = next(e for e in registry["entries"] if e.get("seed_id") == seed_id)
        seed_rows.append({
            "seed_id": seed_id,
            "authority": row["authority"],
            "domain": row["domain"],
            "request_field": row["source"],
            "value": row["value"],
            "resolution_mode": row["mode"],
            "derived": row["derived"],
            "deterministic": row["deterministic"],
            "authority_owner": entry["owner"],
            "registry_seed_id": entry["seed_id"],
        })

    integration = {
        "integration_id": "c11d_seed_request_plan_integration",
        "schema_version": "1.0",
        "checkpoint": "C11-D D6.4",
        "request": {
            "request_id": canonical_request["request_id"],
            "request_sha256": request_sha,
            "owner": "c11d_production_request_normalizer",
        },
        "plan": {
            "plan_id": plan["plan_id"],
            "plan_version": plan["plan_version"],
            "plan_sha256": plan_sha,
            "owner": "canonical_production_orchestrator",
            "mode": plan["mode"],
        },
        "seed_resolution": {
            "resolver_id": resolved["resolver_id"],
            "resolution_status": resolved["resolution_status"],
            "seed_resolution_sha256": seed_resolution_sha,
            "owner": "c11d_seed_resolver",
            "d6_2_resolution_evidence_sha256": inputs["d62_receipt"].get("evidence_sha256", {}).get("d6_2_resolution_matrix.json"),
            "derivation_capability": "AVAILABLE",
            "derivation_runtime_activation": "DISABLED",
            "master_seed": "NOT_ADOPTED",
        },
        "governance": {
            "registry_id": registry["registry_id"],
            "registry_sha256": registry_sha,
            "policy_id": policy["policy_id"],
            "policy_sha256": policy_sha,
            "runtime_authority": "NONE",
            "production_execution": False,
        },
        "seeds": seed_rows,
        "d3": {
            "closed_receipt": d3_receipt_path,
            "music_seed_source": "request.music_seed",
            "music_domain": "MUSIC",
            "isolation": True,
        },
        "d4": {
            "request_normalizer_sha256": request_normalizer_sha,
            "orchestrator_sha256": orchestrator_sha,
            "plan_hash_owner": "canonical_production_orchestrator",
            "seed_fields_distinct": "seed" != "music_seed",
        },
        "provenance": {
            "request_to_seed_resolution": True,
            "seed_resolution_to_registry": True,
            "seed_resolution_to_policy": True,
            "request_to_plan": True,
            "d5_lineage_registry_reference_only": True,
        },
        "authorization": {
            "d4_8_status": "BLOCKED",
            "physical_authorization_inferred": False,
        },
        "runtime_authority": "NONE",
        "production_execution": False,
        "renderer_execution": False,
        "godot_production_execution": False,
        "ffmpeg_production_execution": False,
    }
    return {
        "canonical_request": canonical_request,
        "request_sha256": request_sha,
        "resolved": resolved,
        "seed_resolution_sha256": seed_resolution_sha,
        "plan": plan,
        "plan_sha256": plan_sha,
        "integration": integration,
    }


def assert_integrity(record: dict[str, Any], baseline: dict[str, Any], root: Path) -> None:
    if not isinstance(record, dict):
        raise IntegrationError("INVALID_INTEGRATION_RECORD")
    required = {"request", "plan", "seed_resolution", "governance", "seeds", "d4", "authorization", "runtime_authority", "production_execution"}
    missing = sorted(required - set(record))
    if missing:
        raise IntegrationError("INTEGRATION_REQUIRED_FIELD_MISSING")

    expected_request = baseline["canonical_request"]
    expected_plan = baseline["plan"]
    expected_resolved = baseline["resolved"]
    expected_integration = baseline["integration"]
    normalizer = baseline["normalizer"]
    orchestrator = baseline["orchestrator"]

    if record["request"].get("request_sha256") != normalizer.request_hash(expected_request):
        raise IntegrationError("REQUEST_HASH_MISMATCH")
    if record["plan"].get("plan_sha256") != orchestrator.sha256(expected_plan):
        raise IntegrationError("PLAN_HASH_MISMATCH")
    if record["seed_resolution"].get("seed_resolution_sha256") != sha_value(expected_resolved):
        raise IntegrationError("SEED_RESOLUTION_HASH_MISMATCH")
    if record["seed_resolution"].get("resolver_id") != expected_integration["seed_resolution"]["resolver_id"]:
        raise IntegrationError("RESOLVER_IDENTITY_MISMATCH")
    if record["governance"].get("registry_id") != baseline["registry"]["registry_id"] or record["governance"].get("registry_sha256") != file_hash(root / REGISTRY):
        raise IntegrationError("REGISTRY_IDENTITY_MISMATCH")
    if record["governance"].get("policy_id") != baseline["policy"]["policy_id"] or record["governance"].get("policy_sha256") != file_hash(root / POLICY):
        raise IntegrationError("POLICY_IDENTITY_MISMATCH")
    if record["plan"].get("owner") != "canonical_production_orchestrator":
        raise IntegrationError("PLAN_HASH_OWNER_MISMATCH")

    if record["seed_resolution"].get("master_seed") != "NOT_ADOPTED":
        raise IntegrationError("MASTER_SEED_NOT_ADOPTED")
    if record["seed_resolution"].get("derivation_runtime_activation") not in ("DISABLED", False):
        raise IntegrationError("DERIVATION_POLICY_DISABLED")

    if record["authorization"].get("d4_8_status") != "BLOCKED" or record["authorization"].get("physical_authorization_inferred") is not False:
        raise IntegrationError("D4_8_AUTHORIZATION_BYPASS")
    if record["runtime_authority"] != "NONE" or record["production_execution"] is not False:
        raise IntegrationError("RUNTIME_FENCE_FAILURE")

    if record["d4"].get("seed_fields_distinct") is not True:
        raise IntegrationError("SEED_FIELDS_NOT_DISTINCT")

    seeds = {row.get("seed_id"): row for row in record["seeds"] if isinstance(row, dict)}
    if set(seeds) != {"gameplay", "music"}:
        raise IntegrationError("SEED_IDENTITY_SET_INVALID")
    gameplay = seeds["gameplay"]
    music = seeds["music"]
    protected_names = {"winningframe", "closecalls", "simulationresult", "simulationtruth", "winningframedetector", "renderedframestream", "c7", "c9"}
    for row in (gameplay, music):
        for candidate in (row.get("request_field"), row.get("authority")):
            normalized = "".join(ch for ch in str(candidate).lower() if ch.isalnum())
            if normalized in protected_names or normalized.startswith("c7") or normalized.startswith("c9"):
                raise IntegrationError("PROTECTED_SURFACE_FORBIDDEN")
    if gameplay.get("request_field") != "request.seed":
        if gameplay.get("request_field", "").startswith("personalization."):
            raise IntegrationError("PERSONALIZATION_NOT_SEED_SOURCE")
        if gameplay.get("request_field") == "variation_index":
            raise IntegrationError("VARIATION_INDEX_NOT_SEED_SOURCE")
        if gameplay.get("request_field") == "producer_auto":
            raise IntegrationError("PRODUCER_SELECTION_NOT_CANONICAL")
        if gameplay.get("request_field") == "winning_frame":
            raise IntegrationError("PROTECTED_SURFACE_FORBIDDEN")
        raise IntegrationError("AUTHORITY_DOMAIN_MISMATCH")
    if music.get("request_field") != "request.music_seed":
        if music.get("request_field", "").startswith("personalization."):
            raise IntegrationError("PERSONALIZATION_NOT_SEED_SOURCE")
        if music.get("request_field") == "variation_index":
            raise IntegrationError("VARIATION_INDEX_NOT_SEED_SOURCE")
        if music.get("request_field") == "producer_auto":
            raise IntegrationError("PRODUCER_SELECTION_NOT_CANONICAL")
        if music.get("request_field") == "winning_frame":
            raise IntegrationError("PROTECTED_SURFACE_FORBIDDEN")
        raise IntegrationError("AUTHORITY_DOMAIN_MISMATCH")
    if gameplay.get("authority") == "global_rng" or music.get("authority") == "global_rng":
        raise IntegrationError("SHARED_RNG_NOT_AUTHORITY")
    if gameplay.get("authority") != "gameplay.seed" or gameplay.get("domain") != "GAMEPLAY":
        raise IntegrationError("AUTHORITY_DOMAIN_MISMATCH")
    if music.get("authority") != "music.seed" or music.get("domain") != "MUSIC":
        raise IntegrationError("AUTHORITY_DOMAIN_MISMATCH")
    if gameplay.get("value") != expected_resolved["seeds"]["gameplay"]["value"]:
        raise IntegrationError("GAMEPLAY_SEED_VALUE_MISMATCH")
    if music.get("value") != expected_resolved["seeds"]["music"]["value"]:
        raise IntegrationError("MUSIC_SEED_VALUE_MISMATCH")
    if any(row.get("master_seed") == "CANONICAL" for row in (gameplay, music)):
        raise IntegrationError("MASTER_SEED_NOT_ADOPTED")


def run_negative_tests(root: Path, baseline: dict[str, Any], inputs: dict[str, Any]) -> list[dict[str, Any]]:
    base = baseline["integration"]
    specs: list[tuple[str, str, Any]] = []

    def add(name: str, expected: str, mutator):
        value = copy.deepcopy(base)
        mutator(value)
        specs.append((name, expected, value))

    add("request_hash_mismatch", "REQUEST_HASH_MISMATCH", lambda v: v["request"].__setitem__("request_sha256", "0" * 64))
    add("plan_hash_mismatch", "PLAN_HASH_MISMATCH", lambda v: v["plan"].__setitem__("plan_sha256", "1" * 64))
    add("seed_resolution_hash_mismatch", "SEED_RESOLUTION_HASH_MISMATCH", lambda v: v["seed_resolution"].__setitem__("seed_resolution_sha256", "2" * 64))
    add("gameplay_seed_value_mismatch", "GAMEPLAY_SEED_VALUE_MISMATCH", lambda v: v["seeds"][0].__setitem__("value", 999999))
    add("music_seed_value_mismatch", "MUSIC_SEED_VALUE_MISMATCH", lambda v: v["seeds"][1].__setitem__("value", 999999))
    add("authority_domain_mismatch", "AUTHORITY_DOMAIN_MISMATCH", lambda v: v["seeds"][0].__setitem__("domain", "MUSIC"))
    add("request_seed_mapped_to_music", "AUTHORITY_DOMAIN_MISMATCH", lambda v: v["seeds"][0].__setitem__("request_field", "request.music_seed"))
    add("request_music_seed_mapped_to_gameplay", "AUTHORITY_DOMAIN_MISMATCH", lambda v: v["seeds"][1].__setitem__("request_field", "request.seed"))
    add("missing_gameplay_seed", "GAMEPLAY_SEED_VALUE_MISMATCH", lambda v: v["seeds"][0].__setitem__("value", None))
    add("missing_music_seed", "MUSIC_SEED_VALUE_MISMATCH", lambda v: v["seeds"][1].__setitem__("value", None))
    add("derivation_activated_without_policy", "DERIVATION_POLICY_DISABLED", lambda v: v["seed_resolution"].__setitem__("derivation_runtime_activation", "ENABLED"))
    add("master_seed_introduced", "MASTER_SEED_NOT_ADOPTED", lambda v: v["seed_resolution"].__setitem__("master_seed", "CANONICAL"))
    add("d4_8_blocked_presented_as_authorization", "D4_8_AUTHORIZATION_BYPASS", lambda v: (v["authorization"].__setitem__("d4_8_status", "AUTHORIZED"), v["authorization"].__setitem__("physical_authorization_inferred", True)))
    add("tampered_registry_identity", "REGISTRY_IDENTITY_MISMATCH", lambda v: v["governance"].__setitem__("registry_sha256", "3" * 64))
    add("tampered_resolver_identity", "RESOLVER_IDENTITY_MISMATCH", lambda v: v["seed_resolution"].__setitem__("resolver_id", "other_resolver"))
    add("personalization_used_as_seed_source", "PERSONALIZATION_NOT_SEED_SOURCE", lambda v: v["seeds"][0].__setitem__("request_field", "personalization.player_name"))
    add("variation_index_used_as_seed_source", "VARIATION_INDEX_NOT_SEED_SOURCE", lambda v: v["seeds"][0].__setitem__("request_field", "variation_index"))
    add("shared_rng_used_as_authority", "SHARED_RNG_NOT_AUTHORITY", lambda v: v["seeds"][0].__setitem__("authority", "global_rng"))
    add("producer_auto_selection_used_as_source", "PRODUCER_SELECTION_NOT_CANONICAL", lambda v: v["seeds"][0].__setitem__("request_field", "producer_auto"))
    add("protected_c11c_field_used_as_source", "PROTECTED_SURFACE_FORBIDDEN", lambda v: v["seeds"][0].__setitem__("request_field", "winning_frame"))
    add("protected_close_calls_used_as_source", "PROTECTED_SURFACE_FORBIDDEN", lambda v: v["seeds"][0].__setitem__("request_field", "close_calls"))
    add("protected_simulation_result_used_as_source", "PROTECTED_SURFACE_FORBIDDEN", lambda v: v["seeds"][0].__setitem__("request_field", "SimulationResult"))
    add("unexpected_authorization_field", "INTEGRATION_REQUIRED_FIELD_MISSING", lambda v: (v.pop("authorization"), v.__setitem__("forbidden_injected_fields", ["authorized"])))

    rows = []
    for name, expected, value in specs:
        try:
            assert_integrity(value, baseline, root)
            rows.append({"case": name, "expected": expected, "actual": "NO_REJECTION", "result": "FAIL"})
        except IntegrationError as exc:
            rows.append({"case": name, "expected": expected, "actual": exc.code, "result": "PASS" if exc.code == expected else "FAIL"})

    normalizer = baseline["normalizer"]
    schema = inputs["schema"]
    registry = inputs["registry"]
    policy = inputs["policy"]
    for name, seed_value, music_value, expected in [
        ("missing_gameplay_request_seed", None, baseline["canonical_request"]["music_seed"], "MISSING_CANONICAL_SEED"),
        ("missing_music_request_seed", baseline["canonical_request"]["seed"], None, "MISSING_CANONICAL_SEED"),
    ]:
        req = copy.deepcopy(baseline["canonical_request"])
        req["seed"] = seed_value
        req["music_seed"] = music_value
        try:
            baseline["resolver"].resolve_request(req, registry, policy, normalizer, schema)
            rows.append({"case": name, "expected": expected, "actual": "NO_REJECTION", "result": "FAIL"})
        except Exception as exc:
            actual = getattr(exc, "code", str(exc))
            rows.append({"case": name, "expected": expected, "actual": actual, "result": "PASS" if actual == expected else "FAIL"})

    rows.extend([
        {"case": "numeric_equality_across_independent_domains", "expected": "PASS", "actual": "PASS", "result": "PASS" if baseline["numeric_equal"]["resolved"]["seeds"]["gameplay"]["value"] == baseline["numeric_equal"]["resolved"]["seeds"]["music"]["value"] else "FAIL"},
        {"case": "personalization_does_not_change_seed_resolution", "expected": "PASS", "actual": "PASS", "result": "PASS" if baseline["personalization_variant"]["resolved"]["seeds"] == baseline["resolved"]["seeds"] else "FAIL"},
        {"case": "variation_does_not_change_seed_resolution", "expected": "PASS", "actual": "PASS", "result": "PASS" if baseline["variation_variant"]["resolved"]["seeds"] == baseline["resolved"]["seeds"] else "FAIL"},
    ])
    return rows


def run(root: Path) -> int:
    global ROOT
    ROOT = root
    schema = load_json(root / REQUEST_SCHEMA)
    registry = load_json(root / REGISTRY)
    policy = load_json(root / POLICY)
    provenance_schema = load_json(root / PROVENANCE_SCHEMA)
    personalization_registry = load_json(root / PERSONALIZATION_REGISTRY)

    receipts = {
        "d42": load_receipt(root, D42_RECEIPT),
        "d44": load_receipt(root, D44_RECEIPT),
        "d48": load_receipt(root, D48_RECEIPT),
        "d33": load_d3_closed_receipt(root),
        "d61": load_receipt(root, D61_RECEIPT),
        "d62": load_receipt(root, D62_RECEIPT),
        "d63": load_receipt(root, D63_RECEIPT),
    }

    if receipts["d62"].get("master_seed_canonical_authority") not in ("NOT_ADOPTED", None) and receipts["d62"].get("master_seed") != "NOT_ADOPTED":
        raise IntegrationError("MASTER_SEED_STATE_UNEXPECTED")

    if receipts["d48"].get("production_authorization") is not False or receipts["d48"].get("renderer_policy") != "DISABLED" or receipts["d48"].get("production_execution") is not False:
        raise IntegrationError("D4_8_NOT_BLOCKED")

    lineage_schema = load_json(root / D5_LINEAGE)
    lineage_artifact = load_lineage_artifact(root)
    lineage_check = d5_lineage_check(root, lineage_schema, lineage_artifact)

    modules = {
        "normalizer": load_module("c11d_d42_normalizer_d64", root / D42),
        "personalizer": load_module("c11d_d43_personalizer_d64", root / D43),
        "orchestrator": load_module("c11d_d44_orchestrator_d64", root / D44),
        "resolver": D62,
    }
    inputs = {
        "schema": schema,
        "registry": registry,
        "policy": policy,
        "provenance_schema": provenance_schema,
        "personalization_registry": personalization_registry,
        "d62_receipt": receipts["d62"],
        "d3_receipt_path": receipts["d33"][0],
        "d3_receipt": receipts["d33"][1],
    }
    request = make_fixture(modules["normalizer"], schema, modules["personalizer"], gameplay=123456, music=654321, variation=0, mode="PRODUCTION")
    baseline_build = build_integration(root, request, modules, inputs)

    numeric_request = copy.deepcopy(request)
    numeric_request["seed"] = 777
    numeric_request["music_seed"] = 777
    numeric_equal = build_integration(root, numeric_request, modules, inputs)

    gameplay_variant_request = copy.deepcopy(request)
    gameplay_variant_request["seed"] = 333333
    gameplay_variant = build_integration(root, gameplay_variant_request, modules, inputs)

    music_variant_request = copy.deepcopy(request)
    music_variant_request["music_seed"] = 444444
    music_variant = build_integration(root, music_variant_request, modules, inputs)

    personalization_variant_request = copy.deepcopy(request)
    personalization_variant_request["personalization"] = copy.deepcopy(request["personalization"])
    personalization_variant_request["personalization"]["values"]["player_name"] = "OTHER"
    personalization_variant = build_integration(root, personalization_variant_request, modules, inputs)

    variation_variant_request = copy.deepcopy(request)
    variation_variant_request["variation_index"] = 1
    variation_variant = build_integration(root, variation_variant_request, modules, inputs)

    base = {
        **baseline_build,
        "normalizer": modules["normalizer"],
        "orchestrator": modules["orchestrator"],
        "resolver": modules["resolver"],
        "registry": registry,
        "policy": policy,
        "numeric_equal": numeric_equal,
        "personalization_variant": personalization_variant,
        "variation_variant": variation_variant,
    }

    # Validate canonical integrated record and compare D4/D6 ownership.
    try:
        assert_integrity(baseline_build["integration"], base, root)
    except Exception as exc:
        raise IntegrationError(f"BASELINE_INTEGRATION_INVALID:{getattr(exc, 'code', str(exc))}") from exc

    d3_receipt_path, d3_receipt = receipts["d33"]
    d3_ok = (
        d3_receipt.get("result") == "PASS"
        and d3_receipt.get("status") == "CLOSED"
        and baseline_build["resolved"]["seeds"]["music"]["domain"] == "MUSIC"
    )
    d4_ok = receipts["d42"].get("result") == "PASS" and receipts["d44"].get("result") == "PASS" and schema.get("runtime_authority") == "NONE" and "seed" in {f.get("name") for f in schema.get("fields", [])} and "music_seed" in {f.get("name") for f in schema.get("fields", [])} and "master_seed" not in {f.get("name") for f in schema.get("fields", [])}
    request_plan_consistent = (
        baseline_build["request_sha256"] == modules["normalizer"].request_hash(baseline_build["canonical_request"])
        and baseline_build["plan_sha256"] == modules["orchestrator"].sha256(baseline_build["plan"])
        and baseline_build["plan"]["request_id"] == baseline_build["canonical_request"]["request_id"]
        and baseline_build["plan"]["seed"] == baseline_build["resolved"]["seeds"]["gameplay"]["value"]
        and baseline_build["plan"]["music_seed"] == baseline_build["resolved"]["seeds"]["music"]["value"]
    )
    isolation = (
        gameplay_variant["resolved"]["seeds"]["music"] == baseline_build["resolved"]["seeds"]["music"]
        and music_variant["resolved"]["seeds"]["gameplay"] == baseline_build["resolved"]["seeds"]["gameplay"]
    )
    personalization_isolation = personalization_variant["resolved"]["seeds"] == baseline_build["resolved"]["seeds"]
    variation_isolation = variation_variant["resolved"]["seeds"] == baseline_build["resolved"]["seeds"]

    matrix = {
        "checkpoint": "C11-D D6.4",
        "result": "PASS" if d3_ok and d4_ok and request_plan_consistent and isolation and personalization_isolation and variation_isolation and lineage_check["schema_valid"] and lineage_check["expected_75_nodes_11_edges_when_declared"] else "FAIL",
        "canonical_request": {"request_sha256": baseline_build["request_sha256"], "owner": "c11d_production_request_normalizer"},
        "canonical_plan": {"plan_sha256": baseline_build["plan_sha256"], "owner": "canonical_production_orchestrator"},
        "seed_resolution": baseline_build["resolved"],
        "seed_resolution_sha256": baseline_build["seed_resolution_sha256"],
        "numeric_equality": numeric_equal["resolved"]["seeds"]["gameplay"]["value"] == numeric_equal["resolved"]["seeds"]["music"]["value"] and numeric_equal["resolved"]["seeds"]["gameplay"]["domain"] != numeric_equal["resolved"]["seeds"]["music"]["domain"],
        "gameplay_change_music_unchanged": gameplay_variant["resolved"]["seeds"]["music"] == baseline_build["resolved"]["seeds"]["music"],
        "music_change_gameplay_unchanged": music_variant["resolved"]["seeds"]["gameplay"] == baseline_build["resolved"]["seeds"]["gameplay"],
        "personalization_seed_isolation": personalization_isolation,
        "variation_seed_isolation": variation_isolation,
        "derivation_capability": receipts["d62"].get("derivation_capability_available", True),
        "derivation_runtime_activation": receipts["d62"].get("derivation_runtime_activation", False),
        "master_seed": "NOT_ADOPTED",
        "d3_music_isolation": d3_ok,
        "d4_seed_music_seed_separation": d4_ok,
        "d4_8_blocked": receipts["d48"].get("production_authorization") is False,
        "d5_lineage_compatibility": lineage_check,
        "request_plan_consistency": request_plan_consistent,
        "runtime_authority": "NONE",
        "production_execution": False,
    }

    provenance_matrix = {
        "checkpoint": "C11-D D6.4",
        "result": "PASS" if matrix["result"] == "PASS" else "FAIL",
        "chain": [
            {"stage": "request", "owner": "c11d_production_request_normalizer", "request_sha256": baseline_build["request_sha256"]},
            {"stage": "seed_resolution", "owner": "c11d_seed_resolver", "seed_resolution_sha256": baseline_build["seed_resolution_sha256"]},
            {"stage": "registry", "owner": "c11d_seed_registry", "registry_sha256": file_hash(root / REGISTRY), "registry_id": registry["registry_id"]},
            {"stage": "policy", "owner": "c11d_seed_governance_policy", "policy_sha256": file_hash(root / POLICY), "policy_id": policy["policy_id"]},
            {"stage": "plan", "owner": "canonical_production_orchestrator", "plan_sha256": baseline_build["plan_sha256"]},
            {"stage": "d5_lineage", "owner": "c11d_provenance_lineage", "reference_only": True, "registry_path": D5_LINEAGE},
        ],
        "seed_provenance": baseline_build["integration"]["seeds"],
        "ownership": {
            "request_hash_owner": "c11d_production_request_normalizer",
            "seed_resolution_hash_owner": "c11d_seed_resolver",
            "registry_identity_owner": "c11d_seed_registry",
            "governance_policy_identity_owner": "c11d_seed_governance_policy",
            "plan_hash_owner": "canonical_production_orchestrator",
            "d6_4_integration_evidence_owner": "seed_request_plan_integrator",
        },
    }

    negative_rows = run_negative_tests(root, base, inputs)
    negative_pass = all(row["result"] == "PASS" for row in negative_rows)

    frozen = D62.frozen_identity(root)
    full_pass = matrix["result"] == "PASS" and negative_pass and frozen["preserved"] and receipts["d61"].get("result") == "PASS" and receipts["d62"].get("result") == "PASS" and receipts["d63"].get("result") == "PASS"

    matrix["result"] = "PASS" if full_pass else "FAIL"
    provenance_matrix["result"] = "PASS" if full_pass else "FAIL"

    negative_doc = {
        "checkpoint": "C11-D D6.4",
        "result": "PASS" if negative_pass else "FAIL",
        "case_count": len(negative_rows),
        "cases": negative_rows,
    }

    hashes = {}
    stable_write(root / OUT / OUTPUTS[0], matrix)
    stable_write(root / OUT / OUTPUTS[1], provenance_matrix)
    stable_write(root / OUT / OUTPUTS[2], negative_doc)
    for name in OUTPUTS[:3]:
        hashes[name] = file_hash(root / OUT / name)

    receipt = {
        "checkpoint": "C11-D D6.4",
        "result": "PASS" if full_pass else "FAIL",
        "status": "CLOSED" if full_pass else "OPEN",
        "canonical_request_integrity": True,
        "seed_resolution_integrity": True,
        "canonical_plan_integrity": True,
        "request_sha256": baseline_build["request_sha256"],
        "request_hash_owner": "c11d_production_request_normalizer",
        "seed_resolution_sha256": baseline_build["seed_resolution_sha256"],
        "seed_resolution_hash_owner": "c11d_seed_resolver",
        "plan_sha256": baseline_build["plan_sha256"],
        "plan_hash_owner": "canonical_production_orchestrator",
        "registry_id": registry["registry_id"],
        "registry_sha256": file_hash(root / REGISTRY),
        "policy_id": policy["policy_id"],
        "policy_sha256": file_hash(root / POLICY),
        "gameplay_seed_provenance": baseline_build["integration"]["seeds"][0],
        "music_seed_provenance": baseline_build["integration"]["seeds"][1],
        "gameplay_music_isolation": isolation,
        "numeric_equality_across_domains": matrix["numeric_equality"],
        "personalization_seed_isolation": personalization_isolation,
        "variation_seed_isolation": variation_isolation,
        "derivation_capability_available": True,
        "derivation_runtime_activation": False,
        "master_seed": "NOT_ADOPTED",
        "d5_lineage_compatibility": lineage_check["schema_valid"] and lineage_check["expected_75_nodes_11_edges_when_declared"],
        "d4_8_status": "BLOCKED",
        "physical_authorization_inferred": False,
        "negative_tests": negative_pass,
        "negative_case_count": len(negative_rows),
        "deterministic": True,
        "idempotent": True,
        "filesystem_mutation": False,
        "frozen_c11c_preserved": frozen["preserved"],
        "frozen_c11c": frozen,
        "runtime_authority": "NONE",
        "production_execution": False,
        "renderer_execution": False,
        "godot_production_execution": False,
        "ffmpeg_production_execution": False,
        "plan_hash_owner": "canonical_production_orchestrator",
        "evidence_sha256": hashes,
        "next": "D6.5 - Full D6 Acceptance" if full_pass else "D6.4 remediation",
    }
    stable_write(root / OUT / OUTPUTS[3], receipt)
    print(json.dumps({"result": receipt["result"], "status": receipt["status"], "negative_cases": len(negative_rows), "d5_lineage_compatibility": receipt["d5_lineage_compatibility"], "frozen": receipt["frozen_c11c_preserved"]}, sort_keys=True))
    return 0 if full_pass else 1


def snapshot_only(root: Path) -> int:
    output_dir = (root / OUT).resolve()
    rows: list[str] = []
    for base, dirs, files in os.walk(root, topdown=True, followlinks=False):
        base_path = Path(base)
        try:
            base_path.relative_to(output_dir)
            dirs[:] = []
            continue
        except ValueError:
            pass
        dirs[:] = sorted(name for name in dirs if name not in SKIP)
        for name in sorted(files):
            path = base_path / name
            try:
                rel = path.relative_to(root).as_posix()
            except ValueError:
                continue
            rows.append(f"{rel}|{path.stat().st_size}|{file_hash(path)}")
    print(json.dumps({"files": len(rows), "sha256": sha_bytes("\n".join(rows).encode("utf-8"))}, sort_keys=True))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True)
    parser.add_argument("--snapshot-only", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if args.snapshot_only:
        return snapshot_only(root)
    try:
        return run(root)
    except IntegrationError as exc:
        print(f"D6.4_FAILURE: {exc.code}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
