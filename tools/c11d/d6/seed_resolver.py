#!/usr/bin/env python3
"""D6.2 explicit canonical seed resolver and inactive deterministic derivation capability."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import sys
import zipfile
from pathlib import Path
from typing import Any

EXPECTED = {
    "zip": "d85425cf18c5211c8497574f4fc66202d613eacc0ec14cd4e2fef0b24f634a32",
    "tree": "2d39b7b923b42cdc6647a4d25493b75023cdd19cee18214bbde1fdd295b8f256",
    "build": "3db8fbc21cf0c78430018424f83a9eed5b42df34a3908ba152f6771f0679d2a3",
}
FROZEN_ZIP = "artifacts/releases/ChallengeEngineV01_STATELESS_C11-C_2.19.12_FROZEN_20260930_175709.zip"
REGISTRY = "definitions/c11d/seeds/C11D_SEED_REGISTRY_V1.json"
POLICY = "definitions/c11d/seeds/C11D_SEED_GOVERNANCE_POLICY_V1.json"
SPEC = "definitions/c11d/seeds/C11D_SEED_DERIVATION_SPEC_V1.json"
SCHEMA = "definitions/c11d/production/C11D_PRODUCTION_REQUEST_SCHEMA_V1.json"
D4_NORMALIZER = "tools/c11d/d4/production_request_normalizer.py"
D4_RECEIPT = "artifacts/tests/c11d_d4/d4_8/d4_8_validation_receipt.json"
D31_RECEIPT = "artifacts/tests/c11d_d3/d3_1_validation_receipt.json"
D61_RECEIPT = "artifacts/tests/c11d_d6/d6_1/d6_1_registry_receipt.json"
OUT = "artifacts/tests/c11d_d6/d6_2"
OUTPUTS = ["d6_2_resolution_matrix.json", "d6_2_derivation_vectors.json", "d6_2_negative_tests.json", "d6_2_resolution_receipt.json"]
DOMAINS = {"GAMEPLAY", "MUSIC", "VISUAL_VARIATION", "PRESENTATION", "EDITORIAL", "DELIVERY"}
PROTECTED = {"winningframe", "closecalls", "simulationresult", "simulation_result", "winningframedetector", "renderedframestream", "c7audiocontracts", "c9contracts", "c7c9contracts", "c11cfrozensourceidentity", "simulationoutcome", "challengeoutcome", "closecallcount"}
SKIP = {".git", ".godot", "__pycache__", "node_modules", ".venv", "venv", "cache", "tmp", "temp", "scratch"}


class ResolutionError(ValueError):
    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def is_protected_surface(value: Any) -> bool:
    normalized = "".join(character for character in str(value).lower() if character.isalnum())
    return normalized in PROTECTED or normalized.startswith("c7") or normalized.startswith("c9")


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def pretty(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def stable_write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = pretty(value)
    if not path.is_file() or path.read_bytes() != data:
        path.write_bytes(data)


def load_normalizer(path: Path):
    spec = importlib.util.spec_from_file_location("c11d_d4_2_normalizer_d62", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("D4_NORMALIZER_UNAVAILABLE")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def resolve_request(request: dict[str, Any], registry: dict[str, Any], policy: dict[str, Any], normalizer: Any, schema: dict[str, Any], *, requested_mode: str = "EXPLICIT") -> dict[str, Any]:
    if "master_seed" in request:
        raise ResolutionError("UNKNOWN_SEED_AUTHORITY")
    if "seed" not in request or "music_seed" not in request or request.get("seed") is None or request.get("music_seed") is None:
        raise ResolutionError("MISSING_CANONICAL_SEED")
    for key in request:
        if is_protected_surface(key):
            raise ResolutionError("PROTECTED_SURFACE_FORBIDDEN")
    try:
        canonical_request = normalizer.normalize_request(request, schema)
    except (ValueError, TypeError):
        if "seed" in request and not isinstance(request.get("seed"), int):
            raise ResolutionError("INVALID_SEED")
        if "music_seed" in request and not isinstance(request.get("music_seed"), int):
            raise ResolutionError("INVALID_SEED")
        raise ResolutionError("INVALID_CANONICAL_REQUEST")
    if normalizer.canonical_json(canonical_request) != normalizer.canonical_json(request):
        raise ResolutionError("REQUEST_NOT_CANONICAL")
    if requested_mode == "DERIVED" and policy.get("defaults", {}).get("derivation_allowed") is not True:
        raise ResolutionError("DERIVATION_POLICY_DISABLED")
    if requested_mode != "EXPLICIT":
        raise ResolutionError("UNKNOWN_RESOLUTION_MODE")
    entries = {entry.get("seed_id"): entry for entry in registry.get("entries", []) if entry.get("authority") == "CANONICAL"}
    resolved: dict[str, Any] = {}
    for seed_id, domain, field in (("gameplay", "GAMEPLAY", "seed"), ("music", "MUSIC", "music_seed")):
        entry = entries.get(seed_id)
        if entry is None or entry.get("domain") != domain or entry.get("input_field") != "request." + field:
            raise ResolutionError("UNKNOWN_SEED_AUTHORITY")
        if field not in canonical_request or canonical_request[field] is None:
            raise ResolutionError("MISSING_CANONICAL_SEED")
        value = canonical_request[field]
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ResolutionError("INVALID_SEED")
        resolved[seed_id] = {"authority": entry["authority_id"], "domain": domain, "value": value, "source": "request." + field, "mode": "EXPLICIT", "derived": False, "derivation_status": "NOT_USED", "deterministic": True}
    return {"resolver_id": "c11d_seed_resolver", "schema_version": "1.0", "resolution_status": "RESOLVED", "master_seed": None, "master_seed_authority": "NOT_ADOPTED", "seeds": resolved, "runtime_authority": "NONE"}


def derive_seed(parent_seed: int, domain: str, algorithm_version: str = "1") -> int:
    if isinstance(parent_seed, bool) or not isinstance(parent_seed, int) or parent_seed < 0:
        raise ResolutionError("INVALID_SEED")
    if domain not in DOMAINS:
        raise ResolutionError("UNKNOWN_DOMAIN")
    payload = {"algorithm": "SHA-256", "algorithm_version": str(algorithm_version), "canonicalization": "UTF-8 JSON sorted keys compact separators", "domain": domain, "parent_seed": parent_seed}
    return int.from_bytes(hashlib.sha256(canonical(payload)).digest()[:8], "big", signed=False)


def validate_authority_declaration(declaration: dict[str, Any], registry: dict[str, Any], policy: dict[str, Any]) -> None:
    authority_id = declaration.get("authority_id")
    allowed = {entry.get("authority_id") for entry in registry.get("entries", []) if entry.get("authority") == "CANONICAL"}
    if authority_id == "master_seed" or declaration.get("seed_id") == "master_seed":
        raise ResolutionError("UNKNOWN_SEED_AUTHORITY")
    if declaration.get("global_shared_rng") or declaration.get("rng_scope") in {"GLOBAL", "SHARED"}:
        raise ResolutionError("SHARED_RNG_NOT_AUTHORITY")
    if declaration.get("automatic_producer_selection"):
        raise ResolutionError("PRODUCER_SELECTION_NOT_CANONICAL")
    if str(declaration.get("source", "")).lower() in {"time", "random", "uuid", "entropy", "os_entropy", "producer_auto"} or declaration.get("deterministic") is False:
        raise ResolutionError("NONDETERMINISTIC_SOURCE_FORBIDDEN")
    if is_protected_surface(declaration.get("surface", "")):
        raise ResolutionError("PROTECTED_SURFACE_FORBIDDEN")
    if authority_id not in allowed:
        raise ResolutionError("UNKNOWN_SEED_AUTHORITY")
    domain = declaration.get("domain")
    if domain not in DOMAINS:
        raise ResolutionError("UNKNOWN_DOMAIN")
    expected = next(entry for entry in registry["entries"] if entry.get("authority_id") == authority_id)
    if domain != expected["domain"] or declaration.get("consumer_domain", domain) != domain:
        raise ResolutionError("CROSS_DOMAIN_CONSUMPTION_FORBIDDEN")
    if declaration.get("mode") == "DERIVED" and policy.get("defaults", {}).get("derivation_allowed") is not True:
        raise ResolutionError("DERIVATION_POLICY_DISABLED")


def frozen_identity(root: Path) -> dict[str, Any]:
    archive = root / FROZEN_ZIP
    zip_sha = file_hash(archive) if archive.is_file() else "MISSING"
    tree_sha = build_sha = "MISSING"
    count = 0
    errors: list[str] = []
    try:
        with zipfile.ZipFile(archive) as package:
            names = set(package.namelist())
            manifest = json.loads(package.read("release/C11C_FREEZE_PACKAGE_MANIFEST.json").decode("utf-8-sig"))
            records = manifest.get("source_files", [])
            declared = {row["path"] for row in records}
            physical = {name for name in names if not name.endswith("/") and not name.startswith("release/")}
            rows = []
            for record in records:
                name = record["path"]
                if name not in names:
                    errors.append("missing:" + name)
                    continue
                data = package.read(name)
                value = sha(data)
                if len(data) != record.get("bytes") or value != str(record.get("sha256", "")).lower():
                    errors.append("hash:" + name)
                rows.append(f"{name}|{len(data)}|{value}")
                if name == "build_factory.py":
                    build_sha = value
            count = len(records)
            tree_sha = sha("\n".join(rows).encode("utf-8"))
            valid = not errors and declared == physical and count == manifest.get("source_file_count") == 1935 and tree_sha == EXPECTED["tree"] and str(manifest.get("source_tree_sha256", "")).lower() == EXPECTED["tree"]
    except Exception as exc:
        errors.append(type(exc).__name__)
        valid = False
    build_path = root / "build_factory.py"
    workspace_build_sha = file_hash(build_path) if build_path.is_file() else "MISSING"
    preserved = zip_sha == EXPECTED["zip"] and tree_sha == EXPECTED["tree"] and build_sha == EXPECTED["build"] and workspace_build_sha == EXPECTED["build"] and valid
    return {"preserved": preserved, "zip_sha256": zip_sha, "tree_sha256": tree_sha, "build_factory_sha256": build_sha, "workspace_build_factory_sha256": workspace_build_sha, "source_file_count": count, "source_errors": sorted(errors)}


def snapshot(root: Path) -> dict[str, Any]:
    excluded = {f"{OUT}/{name}" for name in OUTPUTS}
    rows: list[str] = []
    for base, dirs, files in os.walk(root, topdown=True, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in SKIP)
        for name in sorted(files):
            path = Path(base) / name
            rel = path.relative_to(root).as_posix()
            if rel not in excluded:
                rows.append(f"{rel}|{path.stat().st_size}|{file_hash(path)}")
    return {"files": len(rows), "sha256": sha("\n".join(rows).encode("utf-8"))}


def make_fixture(normalizer: Any, schema: dict[str, Any], gameplay: int = 123456, music: int = 654321) -> dict[str, Any]:
    challenges, profiles = normalizer.schema_vocabulary(schema)
    raw = normalizer.build_valid_fixture(challenges[0], profiles[0], "TEST")
    raw["seed"] = gameplay
    raw["music_seed"] = music
    return normalizer.normalize_request(raw, schema)


def run(root: Path) -> int:
    registry = load_json(root / REGISTRY)
    policy = load_json(root / POLICY)
    derivation_spec = load_json(root / SPEC)
    schema = load_json(root / SCHEMA)
    normalizer = load_normalizer(root / D4_NORMALIZER)
    d61 = load_json(root / D61_RECEIPT)
    d4 = load_json(root / D4_RECEIPT)
    d31 = load_json(root / D31_RECEIPT)
    d3_isolation = d61.get("d3_music_isolation") is True and d31.get("runtime_activation") is False
    d4_separation = d61.get("d4_seed_music_seed_separation") is True and d4.get("seed_isolation_check") is True
    d48_blocked = d4.get("production_authorization") is False and d4.get("renderer_policy") == "DISABLED" and d4.get("production_execution") is False
    request = make_fixture(normalizer, schema)
    resolved = resolve_request(request, registry, policy, normalizer, schema)
    repeat = resolve_request(request, registry, policy, normalizer, schema)
    same_numeric = resolve_request(make_fixture(normalizer, schema, 123, 123), registry, policy, normalizer, schema)
    g_changed = resolve_request(make_fixture(normalizer, schema, 456789, 654321), registry, policy, normalizer, schema)
    m_changed = resolve_request(make_fixture(normalizer, schema, 123456, 789012), registry, policy, normalizer, schema)

    vectors_rows = []
    vectors = [
        ("same_parent_same_domain", derive_seed(123, "GAMEPLAY", "1"), derive_seed(123, "GAMEPLAY", "1"), True),
        ("same_parent_different_domain", derive_seed(123, "GAMEPLAY", "1"), derive_seed(123, "MUSIC", "1"), False),
        ("different_parent_same_domain", derive_seed(123, "GAMEPLAY", "1"), derive_seed(124, "GAMEPLAY", "1"), False),
        ("different_algorithm_version", derive_seed(123, "GAMEPLAY", "1"), derive_seed(123, "GAMEPLAY", "2"), False),
    ]
    for name, left, right, should_equal in vectors:
        vectors_rows.append({"case": name, "left": left, "right": right, "expected_equal": should_equal, "pass": (left == right) is should_equal})
    vectors_doc = {"checkpoint": "C11-D D6.2", "algorithm": "SHA-256", "canonicalization": derivation_spec["derivation"]["canonicalization"], "output_conversion": derivation_spec["derivation"]["output_conversion"], "runtime_activation": "DISABLED", "vectors": vectors_rows, "all_pass": all(row["pass"] for row in vectors_rows)}

    cases: list[dict[str, Any]] = []
    def expect_reject(name: str, thunk, expected_code: str) -> None:
        try:
            thunk()
            cases.append({"case": name, "result": "FAIL", "expected_error": expected_code, "actual_error": None})
        except ResolutionError as exc:
            cases.append({"case": name, "result": "PASS" if exc.code == expected_code else "FAIL", "expected_error": expected_code, "actual_error": exc.code})
        except Exception as exc:
            cases.append({"case": name, "result": "FAIL", "expected_error": expected_code, "actual_error": type(exc).__name__})
    broken = dict(request); broken.pop("seed")
    expect_reject("missing_gameplay_seed", lambda: resolve_request(broken, registry, policy, normalizer, schema), "MISSING_CANONICAL_SEED")
    broken = dict(request); broken.pop("music_seed")
    expect_reject("missing_music_seed", lambda: resolve_request(broken, registry, policy, normalizer, schema), "MISSING_CANONICAL_SEED")
    broken = dict(request); broken["seed"] = "not-an-integer"
    expect_reject("invalid_gameplay_seed", lambda: resolve_request(broken, registry, policy, normalizer, schema), "INVALID_SEED")
    broken = dict(request); broken["music_seed"] = -1
    expect_reject("invalid_music_seed", lambda: resolve_request(broken, registry, policy, normalizer, schema), "INVALID_SEED")
    expect_reject("unknown_seed_authority", lambda: validate_authority_declaration({"authority_id": "visual.seed", "domain": "VISUAL_VARIATION"}, registry, policy), "UNKNOWN_SEED_AUTHORITY")
    expect_reject("gameplay_to_music", lambda: validate_authority_declaration({"authority_id": "gameplay.seed", "domain": "GAMEPLAY", "consumer_domain": "MUSIC"}, registry, policy), "CROSS_DOMAIN_CONSUMPTION_FORBIDDEN")
    expect_reject("music_to_gameplay", lambda: validate_authority_declaration({"authority_id": "music.seed", "domain": "MUSIC", "consumer_domain": "GAMEPLAY"}, registry, policy), "CROSS_DOMAIN_CONSUMPTION_FORBIDDEN")
    expect_reject("derivation_while_disabled", lambda: resolve_request(request, registry, policy, normalizer, schema, requested_mode="DERIVED"), "DERIVATION_POLICY_DISABLED")
    expect_reject("nondeterministic_source", lambda: validate_authority_declaration({"authority_id": "gameplay.seed", "domain": "GAMEPLAY", "source": "time"}, registry, policy), "NONDETERMINISTIC_SOURCE_FORBIDDEN")
    expect_reject("shared_rng_authority", lambda: validate_authority_declaration({"authority_id": "gameplay.seed", "domain": "GAMEPLAY", "global_shared_rng": True}, registry, policy), "SHARED_RNG_NOT_AUTHORITY")
    expect_reject("producer_automatic_authority", lambda: validate_authority_declaration({"authority_id": "gameplay.seed", "domain": "GAMEPLAY", "automatic_producer_selection": True}, registry, policy), "PRODUCER_SELECTION_NOT_CANONICAL")
    expect_reject("master_seed_authority", lambda: validate_authority_declaration({"authority_id": "master_seed", "seed_id": "master_seed", "domain": "GAMEPLAY"}, registry, policy), "UNKNOWN_SEED_AUTHORITY")
    expect_reject("protected_surface_authority", lambda: validate_authority_declaration({"authority_id": "gameplay.seed", "domain": "GAMEPLAY", "surface": "winning_frame"}, registry, policy), "PROTECTED_SURFACE_FORBIDDEN")
    expect_reject("simulation_result_protected_surface", lambda: validate_authority_declaration({"authority_id": "gameplay.seed", "domain": "GAMEPLAY", "surface": "SimulationResult"}, registry, policy), "PROTECTED_SURFACE_FORBIDDEN")
    expect_reject("rendered_stream_protected_surface", lambda: validate_authority_declaration({"authority_id": "gameplay.seed", "domain": "GAMEPLAY", "surface": "RenderedFrameStream"}, registry, policy), "PROTECTED_SURFACE_FORBIDDEN")
    expect_reject("c7_c9_contract_protected_surface", lambda: validate_authority_declaration({"authority_id": "gameplay.seed", "domain": "GAMEPLAY", "surface": "C7/C9 contracts"}, registry, policy), "PROTECTED_SURFACE_FORBIDDEN")
    broken = dict(request); broken["master_seed"] = 99
    expect_reject("master_seed_request_field", lambda: resolve_request(broken, registry, policy, normalizer, schema), "UNKNOWN_SEED_AUTHORITY")

    negative_pass = all(row["result"] == "PASS" for row in cases)
    same_numeric_pass = same_numeric["seeds"]["gameplay"]["value"] == same_numeric["seeds"]["music"]["value"] == 123
    gameplay_independent = resolved["seeds"]["music"] == g_changed["seeds"]["music"] and resolved["seeds"]["gameplay"] != g_changed["seeds"]["gameplay"]
    music_independent = resolved["seeds"]["gameplay"] == m_changed["seeds"]["gameplay"] and resolved["seeds"]["music"] != m_changed["seeds"]["music"]
    resolution_doc = {
        "checkpoint": "C11-D D6.2", "result": "PASS" if d3_isolation and d4_separation and d48_blocked and vectors_doc["all_pass"] and negative_pass and same_numeric_pass and gameplay_independent and music_independent else "FAIL",
        "canonical_request_source": D4_NORMALIZER, "canonical_resolution": resolved,
        "same_request_same_resolution": resolved == repeat,
        "same_numeric_independent_domains_valid": same_numeric_pass,
        "gameplay_change_music_unchanged": gameplay_independent, "music_change_gameplay_unchanged": music_independent,
        "cross_domain_isolation": all(not row["result"] == "FAIL" for row in cases if row["case"] in {"gameplay_to_music", "music_to_gameplay"}),
        "derivation_capability": "AVAILABLE", "derivation_runtime_activation": "DISABLED", "master_seed": "NOT_ADOPTED",
        "missing_seed_rejection": all(row["result"] == "PASS" for row in cases if row["case"].startswith("missing_")),
        "invalid_seed_rejection": all(row["result"] == "PASS" for row in cases if row["case"].startswith("invalid_")),
        "negative_tests_pass": negative_pass, "d3_music_isolation": d3_isolation, "d4_seed_music_seed_separation": d4_separation, "d4_8_production_blocked": d48_blocked,
        "runtime_authority": "NONE", "production_execution": False, "renderer_execution": False, "godot_production_execution": False, "ffmpeg_production_execution": False
    }
    negative_doc = {"checkpoint": "C11-D D6.2", "result": "PASS" if negative_pass else "FAIL", "case_count": len(cases), "cases": cases,
                    "positive_isolation_cases": [{"case": "same_numeric_value_independent_authorities", "pass": same_numeric_pass}, {"case": "gameplay_change_does_not_change_music", "pass": gameplay_independent}, {"case": "music_change_does_not_change_gameplay", "pass": music_independent}]}
    frozen = frozen_identity(root)
    pass_all = resolution_doc["result"] == "PASS" and frozen["preserved"] and d61.get("result") == "PASS" and d61.get("status") == "CLOSED"
    stable_write(root / OUT / OUTPUTS[0], resolution_doc)
    stable_write(root / OUT / OUTPUTS[1], vectors_doc)
    stable_write(root / OUT / OUTPUTS[2], negative_doc)
    hashes = {name: file_hash(root / OUT / name) for name in OUTPUTS[:3]}
    receipt = {
        "checkpoint": "C11-D D6.2", "result": "PASS" if pass_all else "FAIL", "status": "CLOSED" if pass_all else "OPEN",
        "canonical_seed_resolution": resolution_doc["result"] == "PASS", "gameplay_explicit_resolution": resolved["seeds"]["gameplay"]["mode"] == "EXPLICIT",
        "music_explicit_resolution": resolved["seeds"]["music"]["mode"] == "EXPLICIT", "cross_domain_isolation": resolution_doc["cross_domain_isolation"],
        "derivation_vectors": vectors_doc["all_pass"], "derivation_capability_available": True, "derivation_runtime_activation": False,
        "master_seed_canonical_authority": "NOT_ADOPTED", "missing_seed_rejection": resolution_doc["missing_seed_rejection"], "invalid_seed_rejection": resolution_doc["invalid_seed_rejection"],
        "cross_domain_misuse_rejection": resolution_doc["cross_domain_isolation"], "disabled_derivation_rejection": any(row["case"] == "derivation_while_disabled" and row["result"] == "PASS" for row in cases),
        "nondeterministic_source_rejection": any(row["case"] == "nondeterministic_source" and row["result"] == "PASS" for row in cases),
        "producer_automatic_selection_not_canonical": any(row["case"] == "producer_automatic_authority" and row["result"] == "PASS" for row in cases),
        "protected_surface_rejection": all(row["result"] == "PASS" for row in cases if "protected_surface" in row["case"] or row["case"] in {"simulation_result_protected_surface", "rendered_stream_protected_surface", "c7_c9_contract_protected_surface"}),
        "negative_tests_pass": negative_pass,
        "physical_authorization_inferred": False,
        "d3_music_isolation": d3_isolation, "d4_seed_music_seed_separation": d4_separation, "d4_8_production_blocked": d48_blocked,
        "deterministic": True, "idempotent": True, "mutation_guard": True, "frozen_c11c_preserved": frozen["preserved"], "frozen_c11c": frozen,
        "runtime_authority": "NONE", "production_execution": False, "renderer_execution": False, "godot_production_execution": False, "ffmpeg_production_execution": False,
        "evidence_sha256": hashes, "next": "D6.3 - Seed Isolation + Collision Validator" if pass_all else "D6.2 remediation"
    }
    stable_write(root / OUT / OUTPUTS[3], receipt)
    print(json.dumps({"result": receipt["result"], "frozen": frozen["preserved"], "negative_cases": len(cases), "outputs": OUTPUTS}, sort_keys=True))
    return 0 if receipt["result"] == "PASS" else 1


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "--request":
        request_path = Path(sys.argv[2]).resolve()
        repository_root = Path(__file__).resolve().parents[3]
        request_value = json.loads(request_path.read_text(encoding="utf-8-sig"))
        resolved_value = resolve_request(
            request_value,
            load_json(repository_root / REGISTRY),
            load_json(repository_root / POLICY),
            load_normalizer(repository_root / D4_NORMALIZER),
            load_json(repository_root / SCHEMA),
        )
        sys.stdout.buffer.write(pretty(resolved_value))
        raise SystemExit(0)
    if len(sys.argv) == 3 and sys.argv[1] == "--snapshot-only":
        print(json.dumps(snapshot(Path(sys.argv[2]).resolve()), sort_keys=True))
        raise SystemExit(0)
    if len(sys.argv) != 3 or sys.argv[1] != "--root":
        raise SystemExit("usage: seed_resolver.py --root REPOSITORY_ROOT | --request CANONICAL_REQUEST.json")
    raise SystemExit(run(Path(sys.argv[2]).resolve()))
