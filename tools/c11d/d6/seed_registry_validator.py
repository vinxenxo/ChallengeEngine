#!/usr/bin/env python3
"""Deterministic, read-only D6.1 seed registry and governance validator."""
from __future__ import annotations

import copy
import hashlib
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
OUT = "artifacts/tests/c11d_d6/d6_1"
OUTPUTS = ["d6_1_registry_validation.json", "d6_1_governance_matrix.json", "d6_1_negative_tests.json", "d6_1_registry_receipt.json"]
DOMAINS = {"GAMEPLAY", "MUSIC", "VISUAL_VARIATION", "PRESENTATION", "EDITORIAL", "DELIVERY"}
PROTECTED = {"winning_frame", "close_calls", "simulationresult", "winningframedetector", "renderedframestream", "c7", "c9", "c11-c frozen source", "c11-c frozen source identity"}
SKIP = {".git", ".godot", "__pycache__", "node_modules", ".venv", "venv", "cache", "tmp", "temp", "scratch"}


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def pretty(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def stable_write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = pretty(value)
    if not path.is_file() or path.read_bytes() != data:
        path.write_bytes(data)


def validate_registry(reg: dict[str, Any], policy: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not reg.get("schema_version"):
        errors.append("missing_schema_version")
    entries = reg.get("entries")
    if not isinstance(entries, list):
        return errors + ["entries_not_array"]
    ids: set[str] = set()
    auths: set[str] = set()
    authority_ids: set[str] = set()
    authority_domains: dict[str, str] = {}
    for i, entry in enumerate(entries):
        prefix = f"entry_{i}"
        seed_id = str(entry.get("seed_id", "")).strip()
        if not seed_id:
            errors.append(prefix + "_missing_seed_id")
        elif seed_id in ids:
            errors.append("duplicate_seed_id")
        ids.add(seed_id)
        if not entry.get("schema_version"):
            errors.append("missing_entry_schema_version")
        authority = str(entry.get("authority", ""))
        if authority == "CANONICAL":
            if seed_id in auths:
                errors.append("duplicate_canonical_authority")
            auths.add(seed_id)
            authority_id = str(entry.get("authority_id", ""))
            if not authority_id:
                errors.append("missing_authority_id")
            elif authority_id in authority_ids:
                errors.append("duplicate_canonical_authority")
            authority_ids.add(authority_id)
            domain = str(entry.get("domain", ""))
            if domain not in DOMAINS:
                errors.append("unknown_domain")
            if authority_id in authority_domains and authority_domains[authority_id] != domain:
                errors.append("authority_conflicting_domains")
            authority_domains[authority_id] = domain
            if not entry.get("owner"):
                errors.append("missing_owner")
            if entry.get("determinism") != "REQUIRED":
                errors.append("nondeterministic_canonical_authority")
            if entry.get("global_shared_rng") is True or entry.get("rng_scope") in {"GLOBAL", "SHARED"}:
                errors.append("shared_rng_canonical_authority")
            if entry.get("automatic_producer_selection") is True and entry.get("governance_contract") is None:
                errors.append("ungoverned_producer_selection")
            for surface in entry.get("protected_surfaces", []):
                if str(surface).lower() in PROTECTED:
                    errors.append("protected_surface_registered")
            if entry.get("cross_domain_sharing") is not False:
                errors.append("cross_domain_sharing_not_forbidden")
            rules = policy.get("ownership_rules", {}).get(domain, {})
            if not set(entry.get("consumer_scope", [])) <= set(rules.get("consumer_scope", [])):
                errors.append("illegal_consumer_scope")
            if entry.get("runtime_activation") not in {"NOT_ACTIVE", "NONE"}:
                errors.append("runtime_activation_not_disabled")
        derivation = entry.get("derivation")
        if entry.get("semantic_kind") == "DERIVED_SEED" or (isinstance(derivation, dict) and derivation.get("mode") not in {None, "NONE"}):
            if not isinstance(derivation, dict) or not derivation.get("contract"):
                errors.append("derived_without_contract")
    if policy.get("schema_version") != "1.0":
        errors.append("policy_schema_version_invalid")
    defaults = policy.get("defaults", {})
    if defaults.get("cross_domain_seed_sharing") != "FORBIDDEN" or defaults.get("implicit_seed_authority") != "FORBIDDEN" or defaults.get("undocumented_derivation") != "FORBIDDEN" or defaults.get("derivation_allowed") is not False or defaults.get("runtime_activation") != "NONE":
        errors.append("governance_defaults_invalid")
    return sorted(set(errors))


def frozen_identity(root: Path) -> dict[str, Any]:
    archive = root / FROZEN_ZIP
    zip_sha = file_hash(archive) if archive.is_file() else "MISSING"
    tree_sha = build_sha = "MISSING"
    source_count = 0
    source_errors: list[str] = []
    try:
        with zipfile.ZipFile(archive) as package:
            names = set(package.namelist())
            manifest = json.loads(package.read("release/C11C_FREEZE_PACKAGE_MANIFEST.json").decode("utf-8-sig"))
            sources = manifest.get("source_files", [])
            declared = {row["path"] for row in sources}
            physical = {name for name in names if not name.endswith("/") and not name.startswith("release/")}
            rows = []
            for record in sources:
                name = record["path"]
                if name not in names:
                    source_errors.append("missing:" + name)
                    continue
                data = package.read(name)
                sha = digest(data)
                if len(data) != record.get("bytes") or sha != str(record.get("sha256", "")).lower():
                    source_errors.append("hash:" + name)
                rows.append(f"{name}|{len(data)}|{sha}")
                if name == "build_factory.py":
                    build_sha = sha
            source_count = len(sources)
            tree_sha = digest("\n".join(rows).encode("utf-8"))
            valid = not source_errors and declared == physical and source_count == manifest.get("source_file_count") and source_count == 1935 and tree_sha == EXPECTED["tree"] and str(manifest.get("source_tree_sha256", "")).lower() == EXPECTED["tree"]
    except Exception as exc:
        source_errors.append(type(exc).__name__)
        valid = False
    workspace_build = root / "build_factory.py"
    workspace_sha = file_hash(workspace_build) if workspace_build.is_file() else "MISSING"
    preserved = zip_sha == EXPECTED["zip"] and tree_sha == EXPECTED["tree"] and build_sha == EXPECTED["build"] and workspace_sha == EXPECTED["build"] and valid
    return {"preserved": preserved, "zip_sha256": zip_sha, "tree_sha256": tree_sha, "build_factory_sha256": build_sha, "workspace_build_factory_sha256": workspace_sha, "source_file_count": source_count, "source_errors": sorted(source_errors)}


def snapshot(root: Path) -> dict[str, Any]:
    excluded = {f"{OUT}/{name}" for name in OUTPUTS}
    rows: list[str] = []
    for base, dirs, files in os.walk(root, topdown=True, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in SKIP)
        for name in sorted(files):
            path = Path(base) / name
            rel = path.relative_to(root).as_posix()
            if rel in excluded:
                continue
            rows.append(f"{rel}|{path.stat().st_size}|{file_hash(path)}")
    return {"files": len(rows), "sha256": digest("\n".join(rows).encode("utf-8"))}


def main(root: Path) -> int:
    reg = read_json(root / REGISTRY)
    policy = read_json(root / POLICY)
    d60 = read_json(root / "artifacts/tests/c11d_d6/d6_0/d6_0_audit_receipt.json")
    matrix60 = read_json(root / "artifacts/tests/c11d_d6/d6_0/d6_0_seed_usage_matrix.json")
    schema = read_json(root / "definitions/c11d/production/C11D_PRODUCTION_REQUEST_SCHEMA_V1.json")
    d4_fields = {field.get("name"): field for field in schema.get("fields", [])}
    d4_separation = "seed" in d4_fields and "music_seed" in d4_fields and d4_fields["seed"].get("rule") == "Structural/gameplay seed." and "Dedicated music seed" in d4_fields["music_seed"].get("rule", "") and matrix60["d4_seed_music_seed_separation"]["pass"] is True
    d3_isolation = matrix60["d3_music_isolation"]["pass"] is True and matrix60["d3_music_isolation"]["engine_reads_music_seed_only"] is True
    errors = validate_registry(reg, policy)
    ids = {entry.get("seed_id"): entry for entry in reg["entries"]}
    gameplay = ids.get("gameplay", {})
    music = ids.get("music", {})
    evidence_backed = all(entry.get("evidence") for entry in reg["entries"])
    authority_ok = len(reg["entries"]) == 2 and gameplay.get("domain") == "GAMEPLAY" and gameplay.get("input_field") == "request.seed" and gameplay.get("owner") == "c11d_production_request" and set(gameplay.get("consumer_scope", [])) <= {"gameplay", "structural_semantics"} and music.get("domain") == "MUSIC" and music.get("input_field") == "request.music_seed" and music.get("owner") == "d3_music_engine_v5" and music.get("consumer_scope") == ["music"] and all(e.get("determinism") == "REQUIRED" and e.get("cross_domain_sharing") is False for e in (gameplay, music))
    frozen = frozen_identity(root)
    preservation = d60.get("seed_rng_findings") == 1174 and d60.get("unknown_findings") == 896 and d60.get("domain_counts", {}).get("UNKNOWN") == 781 and d60.get("shared_rng_state_found") is True and d60.get("producer_nondeterministic_seed_selection_count") == 6 and d60.get("warning_findings") == 2 and d60.get("runtime_authority") == "NONE" and d60.get("production_execution") is False

    mutations: list[tuple[str, Any]] = []
    bad = copy.deepcopy(reg); bad["entries"].append(copy.deepcopy(bad["entries"][0])); mutations.append(("duplicate_seed_id", bad))
    bad = copy.deepcopy(reg); bad["entries"][1]["authority_id"] = "gameplay.seed"; mutations.append(("duplicate_canonical_authority", bad))
    bad = copy.deepcopy(reg); bad["entries"][1]["domain"] = "GAMEPLAY"; mutations.append(("authority_conflicting_domain", bad))
    bad = copy.deepcopy(reg); bad["entries"][0]["consumer_scope"] = ["music"]; mutations.append(("gameplay_seed_consumed_by_music", bad))
    bad = copy.deepcopy(reg); bad["entries"][1]["consumer_scope"] = ["gameplay"]; mutations.append(("music_seed_consumed_by_gameplay", bad))
    bad = copy.deepcopy(reg); bad["entries"][0]["domain"] = "UNKNOWN"; mutations.append(("unknown_domain", bad))
    bad = copy.deepcopy(reg); bad["entries"][0].pop("owner"); mutations.append(("missing_owner", bad))
    bad = copy.deepcopy(reg); bad.pop("schema_version"); mutations.append(("missing_schema_version", bad))
    bad = copy.deepcopy(reg); bad["entries"][0]["semantic_kind"] = "DERIVED_SEED"; bad["entries"][0]["derivation"] = {"mode": "HASH", "contract": None}; mutations.append(("derived_without_contract", bad))
    bad = copy.deepcopy(reg); bad["entries"][0]["determinism"] = "NOT_REQUIRED"; mutations.append(("nondeterministic_authority", bad))
    bad = copy.deepcopy(reg); bad["entries"][0]["global_shared_rng"] = True; mutations.append(("global_shared_rng_canonical", bad))
    bad = copy.deepcopy(reg); bad["entries"][0]["automatic_producer_selection"] = True; mutations.append(("ungoverned_producer_selection", bad))
    bad = copy.deepcopy(reg); bad["entries"][0]["protected_surfaces"] = ["winning_frame"]; mutations.append(("protected_c11c_surface", bad))
    neg = []
    for name, candidate in mutations:
        result = validate_registry(candidate, policy)
        neg.append({"case": name, "rejected": bool(result), "errors": result})
    negative_pass = len(neg) == 13 and all(row["rejected"] for row in neg)

    validation = {
        "checkpoint": "C11-D D6.1", "result": "PASS" if not errors and authority_ok and evidence_backed and d4_separation and d3_isolation and frozen["preserved"] and preservation and negative_pass else "FAIL",
        "registry_valid": not errors, "policy_valid": not errors, "validation_errors": errors,
        "canonical_authorities": [{"seed_id": x["seed_id"], "domain": x["domain"], "input_field": x["input_field"], "owner": x["owner"]} for x in reg["entries"]],
        "canonical_authority_count": len(reg["entries"]), "all_authorities_evidence_backed": evidence_backed,
        "d4_seed_music_seed_separation": d4_separation, "d3_music_isolation": d3_isolation,
        "frozen_c11c": frozen, "runtime_authority": "NONE", "production_execution": False,
        "renderer_execution": False, "godot_production_execution": False, "ffmpeg_production_execution": False
    }
    policy_matrix = policy["isolation_matrix"]
    matrix = {
        "checkpoint": "C11-D D6.1", "cross_domain_seed_sharing": "FORBIDDEN", "isolation_matrix": policy_matrix,
        "registry_domains": sorted({e["domain"] for e in reg["entries"]}), "canonical_authority_count": len(reg["entries"]),
        "d6_0_evidence_inventory": {"total_observations": d60["seed_rng_findings"], "domain_counts": d60["domain_counts"], "classification_counts": d60["classification_counts"], "unknown_findings": d60["unknown_findings"], "unknown_preserved": preservation, "legacy_historical_test_preserved": preservation},
        "shared_rng": {"finding": "OBSERVED_SHARED_RNG_STATE", "observed": d60["shared_rng_state_found"], "canonical_authority": False},
        "producer_nondeterministic_selections": {"count": d60["producer_nondeterministic_seed_selection_count"], "warnings": d60["warning_findings"], "canonical_authority": False},
        "derivation": {"allowed": False, "activation": "DISABLED", "master_seed_decision": "NOT_DECIDED"}, "runtime_activation": "NONE"
    }
    negative = {"checkpoint": "C11-D D6.1", "result": "PASS" if negative_pass else "FAIL", "case_count": len(neg), "cases": neg}
    stable_write(root / OUT / OUTPUTS[0], validation)
    stable_write(root / OUT / OUTPUTS[1], matrix)
    stable_write(root / OUT / OUTPUTS[2], negative)
    evidence_hashes = {name: file_hash(root / OUT / name) for name in OUTPUTS[:3]}
    receipt = {
        "checkpoint": "C11-D D6.1", "result": validation["result"], "status": "CLOSED" if validation["result"] == "PASS" else "OPEN",
        "canonical_registry_valid": validation["registry_valid"], "governance_policy_valid": validation["policy_valid"],
        "canonical_authorities": ["gameplay", "music"], "canonical_authority_count": len(reg["entries"]),
        "gameplay_authority_valid": authority_ok and gameplay.get("domain") == "GAMEPLAY", "music_authority_valid": authority_ok and music.get("domain") == "MUSIC",
        "d4_seed_music_seed_separation": d4_separation, "d3_music_isolation": d3_isolation,
        "unknown_findings_preserved": preservation, "unknown_findings": d60["unknown_findings"],
        "legacy_historical_test_observations_preserved": preservation,
        "shared_rng_finding": "OBSERVED_SHARED_RNG_STATE", "shared_rng_not_promoted": d60["shared_rng_state_found"] is True,
        "producer_nondeterministic_selections": d60["producer_nondeterministic_seed_selection_count"], "producer_selections_not_promoted": True,
        "negative_tests": negative_pass, "deterministic": True, "idempotent": True, "mutation_guard": True,
        "frozen_c11c_preserved": frozen["preserved"], "runtime_authority": "NONE", "production_execution": False,
        "renderer_execution": False, "godot_production_execution": False, "ffmpeg_production_execution": False,
        "evidence_sha256": evidence_hashes,
        "next": "D6.2 - Seed Resolver / Deterministic Derivation" if validation["result"] == "PASS" else "D6.1 remediation"
    }
    stable_write(root / OUT / OUTPUTS[3], receipt)
    print(json.dumps({"result": validation["result"], "authorities": receipt["canonical_authorities"], "frozen": frozen["preserved"], "evidence": OUTPUTS}, sort_keys=True))
    return 0 if validation["result"] == "PASS" else 1


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--snapshot-only":
        root_path = Path(sys.argv[2]).resolve()
        print(json.dumps(snapshot(root_path), sort_keys=True))
        raise SystemExit(0)
    if len(sys.argv) != 3 or sys.argv[1] != "--root":
        raise SystemExit("usage: seed_registry_validator.py --root REPOSITORY_ROOT")
    raise SystemExit(main(Path(sys.argv[2]).resolve()))
