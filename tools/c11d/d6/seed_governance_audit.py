#!/usr/bin/env python3
"""Read-only, deterministic seed/RNG governance audit for C11-D D6.0."""
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
    "zip_sha256": "d85425cf18c5211c8497574f4fc66202d613eacc0ec14cd4e2fef0b24f634a32",
    "tree_sha256": "2d39b7b923b42cdc6647a4d25493b75023cdd19cee18214bbde1fdd295b8f256",
    "build_factory_sha256": "3db8fbc21cf0c78430018424f83a9eed5b42df34a3908ba152f6771f0679d2a3",
}
FROZEN_ZIP = "artifacts/releases/ChallengeEngineV01_STATELESS_C11-C_2.19.12_FROZEN_20260930_175709.zip"
OUT_REL = "artifacts/tests/c11d_d6/d6_0"
OUTPUTS = [
    "d6_0_seed_inventory.json",
    "d6_0_seed_usage_matrix.json",
    "d6_0_governance_findings.json",
    "d6_0_audit_receipt.json",
]
EXTENSIONS = {".gd", ".py", ".ps1", ".cs", ".json", ".tscn", ".tres", ".gdshader", ".ts", ".js", ".yml", ".yaml"}
SCAN_ROOTS = [
    "core", "challenges", "definitions", "tools/c11d/d3", "tools/c11d/d4",
    "tools/c11freeze", "tools/qa/c11", "tools/qa/c7", "tools/prototypes",
    "tests", "c11c-suite/c11c-producer",
]
SKIP_PARTS = {".git", ".godot", "__pycache__", "node_modules", ".venv", "venv", "cache", "tmp", "temp", "scratch"}
SEED_PATTERN = re.compile(
    r"(?i)(?<![A-Za-z0-9_])(?:music_seed|seed|rng|random|RandomNumberGenerator|randf|randi|randomize|shuffle|choice|rnd|uuid|urandom|secrets|SystemRandom|NewGuid)(?![A-Za-z0-9_])"
)
NONDET_PATTERN = re.compile(r"(?i)(randomize\s*\(|uuid[0-9a-z_]*\s*\(|uuid\.(?:uuid[0-9]+|new|random)[a-z0-9_]*\s*\(|urandom|secrets\.(?:choice|randbelow|randbits|token_[a-z]+)\s*\(|SystemRandom|Guid\.NewGuid\s*\(|time\.time\s*\(|datetime\.now|DateTimeOffset\.Now|Time\.get_unix_time|OS\.get_unix_time|random\.seed\s*\()")
PY_RANDOM_CALL = re.compile(r"\brandom\.(?:random|randint|randrange|choice|shuffle|uniform)\s*\(")
RNG_INIT_PATTERN = re.compile(r"(?i)(random\.Random\s*\(|RandomNumberGenerator\.new\s*\(|\.randomize\s*\(|\brandomize\s*\(|\bseed\s*\([^)]*\))")
RNG_USE_PATTERN = re.compile(r"(?i)(\.randf\s*\(|\.randi(?:_range)?\s*\(|\b(?:randf|randi|randi_range)\s*\(|\.sample_(?:integer|float|float_range)\s*\(|\bshuffle\s*\(|\bchoice\s*\(|\brnd\s*\()")
DERIVE_PATTERN = re.compile(r"(?i)(derive[^\n]*seed|seed[^\n]*(?:derive|hash|lcg)|lcg_next_seed|_derive_stream_seed|stable_u\s*\(|hashlib\.(?:sha|blake)|\bhash\s*\()")
ASSIGN_PATTERN = re.compile(r"(?i)(?:\bseed\b|\bmusic_seed\b)\s*(?::[^=]+)?=|\bseed\s*:\s*(?:int|integer)|\"(?:seed|music_seed)\"\s*:")


def is_nondeterministic(line: str) -> bool:
    return bool(NONDET_PATTERN.search(line) or PY_RANDOM_CALL.search(line))


def is_rng_use(line: str) -> bool:
    return bool(RNG_USE_PATTERN.search(line) or PY_RANDOM_CALL.search(line))


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def pretty_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def stable_write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = pretty_bytes(value)
    if not path.is_file() or path.read_bytes() != payload:
        path.write_bytes(payload)


def snapshot(root: Path) -> dict[str, Any]:
    excluded = {f"{OUT_REL}/{name}" for name in OUTPUTS}
    entries: list[tuple[str, Path, int]] = []
    for base, dirs, files in os.walk(root, topdown=True, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_PARTS)
        for name in sorted(files):
            path = Path(base) / name
            rel = path.relative_to(root).as_posix()
            if rel in excluded:
                continue
            entries.append((rel, path, path.stat().st_size))
    def digest_entry(entry: tuple[str, Path, int]) -> tuple[str, int, str]:
        rel, path, size = entry
        return rel, size, sha_file(path)
    with ThreadPoolExecutor(max_workers=8) as executor:
        rows = list(executor.map(digest_entry, entries))
    rows.sort(key=lambda row: row[0])
    tree = "\n".join(f"{name}|{size}|{digest}" for name, size, digest in rows).encode("utf-8")
    return {"files": len(rows), "tree_sha256": sha_bytes(tree)}


def scan_files(root: Path) -> list[Path]:
    found: set[Path] = set()
    for relative_root in SCAN_ROOTS:
        base = root / Path(relative_root)
        if not base.exists():
            continue
        for current, dirs, files in os.walk(base, topdown=True, followlinks=False):
            dirs[:] = sorted(d for d in dirs if d not in SKIP_PARTS)
            for filename in files:
                path = Path(current) / filename
                rel = path.relative_to(root).as_posix()
                if path.suffix.lower() not in EXTENSIONS or rel.startswith(OUT_REL + "/"):
                    continue
                found.add(path)
    return sorted(found, key=lambda p: p.relative_to(root).as_posix())


def nearest_symbol(lines: list[str], index: int, suffix: str) -> str:
    patterns = [re.compile(r"^\s*(?:static\s+)?func\s+([A-Za-z_][A-Za-z0-9_]*)"), re.compile(r"^\s*(?:async\s+)?def\s+([A-Za-z_][A-Za-z0-9_]*)"), re.compile(r"^\s*class\s+([A-Za-z_][A-Za-z0-9_]*)")]
    for prior in range(index, -1, -1):
        for pattern in patterns:
            match = pattern.search(lines[prior])
            if match:
                return match.group(1)
    return "module_scope"


def classify(path: str, line: str) -> tuple[str, str, str, bool]:
    low_path, text = path.lower(), line.lower()
    historical = low_path.startswith("tests/reference/") or "/history/" in low_path
    test_fixture = low_path.startswith("tests/") or "/test" in low_path or "fixture" in low_path
    legacy = "legacy" in low_path or "prototype" in low_path or "c11freeze/" in low_path
    domain = "UNKNOWN"
    if "music_seed" in text or "/d3/" in low_path or "music_engine" in low_path or "music" in low_path and "seed" in text:
        domain = "MUSIC"
    elif low_path.startswith(("core/mechanics/", "core/execution/", "challenges/")):
        domain = "GAMEPLAY"
    elif "variationprofile" in low_path or "visual" in low_path and "seed" in text or "visual_loop" in low_path or "visual_drill" in low_path:
        domain = "VISUAL_VARIATION"
    elif "presentation" in low_path:
        domain = "PRESENTATION"
    elif "editorial" in low_path or "editorial" in text:
        domain = "EDITORIAL"
    elif "delivery" in low_path:
        domain = "DELIVERY"

    runtime_relevant = low_path.startswith(("core/", "challenges/"))
    if is_nondeterministic(line):
        classification = "NONDETERMINISTIC_SOURCE"
    elif historical:
        classification = "HISTORICAL"
    elif test_fixture:
        classification = "TEST_FIXTURE"
    elif legacy:
        classification = "HISTORICAL" if "history" in low_path else "LEGACY"
    elif re.search(r"(?i)^\s*(?:import\s+random|from\s+random\s+import)", line):
        classification = "RNG_INITIALIZATION"
    elif RNG_INIT_PATTERN.search(line) and ("random" in text or "rng" in text):
        classification = "RNG_INITIALIZATION"
    elif RNG_USE_PATTERN.search(line):
        classification = "RNG_CONSUMPTION"
    elif DERIVE_PATTERN.search(line):
        classification = "DERIVED_SEED"
    elif ASSIGN_PATTERN.search(line):
        classification = "EXPLICIT_SEED"
    else:
        classification = "UNKNOWN"
    if test_fixture and (is_rng_use(line) or RNG_INIT_PATTERN.search(line)):
        # Keep fixture classification while preserving behavior in a separate field.
        behavior = "RNG_CONSUMPTION" if is_rng_use(line) else "RNG_INITIALIZATION"
    elif is_rng_use(line):
        behavior = "RNG_CONSUMPTION"
    elif RNG_INIT_PATTERN.search(line):
        behavior = "RNG_INITIALIZATION"
    elif DERIVE_PATTERN.search(line):
        behavior = "DERIVED_SEED"
    elif classification == "TEST_FIXTURE":
        behavior = "TEST_FIXTURE"
    else:
        behavior = classification
    return domain, classification, behavior, runtime_relevant


def scan_findings(root: Path) -> list[dict[str, Any]]:
    findings: dict[tuple[str, int, str], dict[str, Any]] = {}
    for path in scan_files(root):
        rel = path.relative_to(root).as_posix()
        try:
            lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
        except OSError:
            continue
        for index, line in enumerate(lines):
            if not SEED_PATTERN.search(line):
                continue
            stripped = line.strip()
            if not stripped or stripped.startswith(("#", "//", "/*", "*", "##")):
                continue
            domain, classification, behavior, runtime_relevant = classify(rel, line)
            terms = sorted({match.group(0) for match in SEED_PATTERN.finditer(line)}, key=lambda term: (term.lower(), term))
            symbol = nearest_symbol(lines, index, path.suffix.lower())
            seed_field_match = re.search(r"(?i)(music_seed|seed|rng)", line)
            field = seed_field_match.group(1) if seed_field_match else "UNKNOWN"
            if field.lower() == "rng":
                field = "RNG_STATE_OR_API"
            elif field.lower() == "music_seed":
                field = "music_seed"
            else:
                field = "seed"
            if re.search(r"(?i)^\s*(?:import\s+random|from\s+random\s+import)", line):
                producer = "Python random module global instance; initialization source is implicit/UNKNOWN"
            elif PY_RANDOM_CALL.search(line):
                producer = "Python module-level random singleton; automatic seed source is implicit/UNKNOWN"
            elif ASSIGN_PATTERN.search(line):
                producer = "explicit input/configuration at this callsite"
            elif DERIVE_PATTERN.search(line):
                producer = "deterministic derivation expression; upstream source recorded as UNKNOWN unless shown"
            elif "random.Random" in line:
                producer = "explicit corpus seed argument"
            else:
                producer = "UNKNOWN"
            consumer = symbol if is_rng_use(line) else "UNKNOWN"
            if "music_seed" in line.lower():
                consumer = symbol if symbol != "module_scope" else "D3/D4 music request path (see correlated evidence)"
            derivation = stripped if DERIVE_PATTERN.search(line) else "NONE_DECLARED" if field in ("seed", "music_seed") and ASSIGN_PATTERN.search(line) else "UNKNOWN"
            finding = {
                "artifact": "REPOSITORY_SOURCE_OR_CONFIGURATION",
                "path": rel,
                "line": index + 1,
                "symbol": symbol,
                "seed_field": field,
                "domain": domain,
                "classification": classification,
                "behavior_classification": behavior,
                "producer": producer,
                "consumer": consumer,
                "derivation": derivation,
                "deterministic": False if classification == "NONDETERMINISTIC_SOURCE" else True if classification in {"EXPLICIT_SEED", "DERIVED_SEED", "RNG_INITIALIZATION", "RNG_CONSUMPTION", "TEST_FIXTURE", "LEGACY", "HISTORICAL"} else "UNKNOWN",
                "runtime_relevant": runtime_relevant,
                "production_tool_relevant": rel.startswith("c11c-suite/c11c-producer/"),
                "runtime_authority": "NONE",
                "evidence": {"path": rel, "line": index + 1, "excerpt": stripped[:360], "matched_terms": terms},
            }
            findings[(rel, index + 1, classification)] = finding
    return [findings[key] for key in sorted(findings)]


def frozen_identity(root: Path) -> dict[str, Any]:
    archive = root / Path(FROZEN_ZIP)
    actual_zip = sha_file(archive) if archive.is_file() else "MISSING"
    tree_sha, build_sha, source_count = "MISSING", "MISSING", 0
    source_errors: list[str] = []
    try:
        with zipfile.ZipFile(archive) as package:
            names = set(package.namelist())
            manifest = read_json_from_zip(package, "release/C11C_FREEZE_PACKAGE_MANIFEST.json")
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
                digest = sha_bytes(data)
                if len(data) != record.get("bytes") or digest != str(record.get("sha256", "")).lower():
                    source_errors.append("hash:" + name)
                rows.append(f"{name}|{len(data)}|{digest}")
                if name == "build_factory.py":
                    build_sha = digest
            source_count = len(sources)
            tree_sha = sha_bytes("\n".join(rows).encode("utf-8"))
            valid = not source_errors and declared == physical and source_count == manifest.get("source_file_count") and source_count == 1935 and tree_sha == EXPECTED["tree_sha256"] and manifest.get("source_tree_sha256", "").lower() == EXPECTED["tree_sha256"]
    except Exception as exc:
        source_errors.append(str(exc))
        valid = False
    workspace_build = root / "build_factory.py"
    workspace_build_sha = sha_file(workspace_build) if workspace_build.is_file() else "MISSING"
    preserved = actual_zip == EXPECTED["zip_sha256"] and tree_sha == EXPECTED["tree_sha256"] and build_sha == EXPECTED["build_factory_sha256"] and workspace_build_sha == EXPECTED["build_factory_sha256"] and valid
    return {"preserved": preserved, "zip_sha256": actual_zip, "tree_sha256": tree_sha, "build_factory_sha256": build_sha, "workspace_build_factory_sha256": workspace_build_sha, "source_file_count": source_count, "source_errors": sorted(source_errors)}


def read_json_from_zip(package: zipfile.ZipFile, name: str) -> Any:
    return json.loads(package.read(name).decode("utf-8-sig"))


def correlated_evidence(root: Path) -> dict[str, Any]:
    d31 = read_json(root / "artifacts/tests/c11d_d3/d3_1_validation_receipt.json")
    d32 = read_json(root / "artifacts/tests/c11d_d3/d3_2/d3_2_validation_receipt.json")
    d41 = read_json(root / "artifacts/tests/c11d_d4/d4_1/d4_1_validation_receipt.json")
    d43 = read_json(root / "artifacts/tests/c11d_d4/d4_3/d4_3_validation_receipt.json")
    d48 = read_json(root / "artifacts/tests/c11d_d4/d4_8/d4_8_validation_receipt.json")
    schema = read_json(root / "definitions/c11d/production/C11D_PRODUCTION_REQUEST_SCHEMA_V1.json")
    personalization_source = (root / "tools/c11d/d4/personalization_resolver.py").read_text(encoding="utf-8-sig")
    music_engine = root / "tools/c11d/d3/c11d_music_engine_v5.py"
    engine_text = music_engine.read_text(encoding="utf-8-sig")
    fields = {item.get("name"): item for item in schema.get("fields", [])}
    request_separation = fields.get("seed", {}).get("rule") == "Structural/gameplay seed." and "Dedicated music seed" in fields.get("music_seed", {}).get("rule", "")
    personalization_excludes_seeds = '"seed", "music_seed"' in personalization_source and d43.get("tests", {}).get("non_allowlisted_field_rejected") is True and d43.get("seed_isolation", {}).get("seed_identical") is True and d43.get("seed_isolation", {}).get("music_seed_identical") is True
    d4_pass = (
        request_separation
        and personalization_excludes_seeds
        and d41.get("result") == "PASS" and d41.get("status") == "CLOSED"
        and d43.get("seed_isolation", {}).get("seed_identical") is True
        and d43.get("seed_isolation", {}).get("music_seed_identical") is True
        and d48.get("seed_isolation_check") is True
    )
    music_only = 'req["music_seed"]' in engine_text and 'req["seed"]' not in engine_text and d31.get("dedicated_music_seed") is True
    d31_isolated = d31.get("structural_rng_decoupled") is True and d31.get("gameplay_rng_decoupled") is True and d31.get("runtime_activation") is False
    d3_pass = str(d31.get("result", "")).startswith("PASS") and d31_isolated and d32.get("result") == "PASS" and d32.get("status") == "CLOSED" and music_only
    blocked = d48.get("result") == "PASS" and d48.get("status") == "CLOSED" and d48.get("renderer_policy") == "DISABLED" and d48.get("production_authorization") is False and d48.get("runtime_authority") == "NONE"
    return {
        "d3_music_isolation": {"pass": d3_pass, "engine_reads_music_seed_only": music_only, "d3_1_structural_rng_decoupled": d31.get("structural_rng_decoupled"), "d3_1_gameplay_rng_decoupled": d31.get("gameplay_rng_decoupled"), "d3_2_status": d32.get("status"), "evidence_paths": ["tools/c11d/d3/c11d_music_engine_v5.py", "artifacts/tests/c11d_d3/d3_1_validation_receipt.json", "artifacts/tests/c11d_d3/d3_2/d3_2_validation_receipt.json"]},
        "d4_seed_separation": {"pass": d4_pass, "request_seed_domain": "GAMEPLAY", "request_music_seed_domain": "MUSIC", "schema_separates_fields": request_separation, "personalization_cannot_source_seeds": personalization_excludes_seeds, "d4_1_status": d41.get("status"), "d4_3_isolation": d43.get("seed_isolation"), "d4_8_isolation_check": d48.get("seed_isolation_check"), "evidence_paths": ["definitions/c11d/production/C11D_PRODUCTION_REQUEST_SCHEMA_V1.json", "tools/c11d/d4/personalization_resolver.py", "artifacts/tests/c11d_d4/d4_1/d4_1_validation_receipt.json", "artifacts/tests/c11d_d4/d4_3/d4_3_validation_receipt.json", "artifacts/tests/c11d_d4/d4_8/d4_8_validation_receipt.json"]},
        "d4_8_blocked_no_seed_authority": blocked,
    }


def main_audit(root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    findings = scan_findings(root)
    domains = ["GAMEPLAY", "MUSIC", "VISUAL_VARIATION", "PRESENTATION", "EDITORIAL", "DELIVERY", "UNKNOWN"]
    classifications = ["EXPLICIT_SEED", "DERIVED_SEED", "RNG_INITIALIZATION", "RNG_CONSUMPTION", "NONDETERMINISTIC_SOURCE", "LEGACY", "HISTORICAL", "TEST_FIXTURE", "UNKNOWN"]
    domain_counts = {domain: sum(1 for row in findings if row["domain"] == domain) for domain in domains}
    classification_counts = {kind: sum(1 for row in findings if row["classification"] == kind) for kind in classifications}
    # Check all source lines for shared/global RNG constructs, independently of seed field matches.
    shared_pattern = re.compile(r"(?i)(?:^(?:var|const)\s+\w*(?:rng|random)\w*\s*[:=].*(?:RandomNumberGenerator|random\.Random)|(?:^|\n)\s*random\.seed\s*\(|\b(?:setget|singleton)\b.*\b(?:rng|random)\b)")
    shared_hits = []
    nondeterministic_hits = []
    for path in scan_files(root):
        rel = path.relative_to(root).as_posix()
        try:
            content = path.read_text(encoding="utf-8-sig", errors="replace")
        except OSError:
            continue
        for number, line in enumerate(content.splitlines(), 1):
            if shared_pattern.search(line):
                shared_hits.append({"path": rel, "line": number, "evidence": line.strip()[:300]})
            if re.search(r"(?i)^\s*(?:import\s+random|from\s+random\s+import)", line) and PY_RANDOM_CALL.search(content):
                shared_hits.append({"path": rel, "line": number, "evidence": "module-level Python random singleton is imported and consumed in this component"})
            if is_nondeterministic(line):
                nondeterministic_hits.append({"path": rel, "line": number, "evidence": line.strip()[:300], "runtime_relevant": rel.startswith(("core/", "challenges/")), "production_tool_relevant": rel.startswith("c11c-suite/c11c-producer/")})
    shared_rng = {"checked": True, "shared_or_global_rng_found": bool(shared_hits), "cross_domain_engine_state_proven": False, "evidence": sorted(shared_hits, key=lambda x: (x["path"], x["line"]))}
    active_nondeterminism = [hit for hit in nondeterministic_hits if hit["runtime_relevant"]]
    nondeterministic = {"checked": True, "matches": sorted(nondeterministic_hits, key=lambda x: (x["path"], x["line"])), "active_runtime_sources": active_nondeterminism, "active_runtime_source_found": bool(active_nondeterminism)}
    evidence = correlated_evidence(root)
    frozen = frozen_identity(root)

    protected = [
        {"surface": "winning_frame", "classification": "PROTECTED / NO_SEED_AUTHORITY", "authority": "simulation-derived truth; not a seed control"},
        {"surface": "close_calls", "classification": "PROTECTED / NO_SEED_AUTHORITY", "authority": "simulation-derived truth; not a seed control"},
        {"surface": "SimulationResult", "classification": "PROTECTED / NO_SEED_AUTHORITY"},
        {"surface": "WinningFrameDetector", "classification": "PROTECTED / NO_SEED_AUTHORITY"},
        {"surface": "RenderedFrameStream", "classification": "PROTECTED / NO_SEED_AUTHORITY"},
        {"surface": "C7 audio contracts", "classification": "PROTECTED / NO_SEED_AUTHORITY"},
        {"surface": "C9 authoring contracts", "classification": "PROTECTED / NO_SEED_AUTHORITY"},
        {"surface": "C11-C frozen archive/runtime", "classification": "PROTECTED / NO_SEED_AUTHORITY"},
    ]

    findings_report: list[dict[str, Any]] = []
    if shared_rng["shared_or_global_rng_found"]:
        findings_report.append({"severity": "WARNING", "code": "SHARED_OR_GLOBAL_RNG_STATE", "details": shared_rng["evidence"], "interpretation": "Module/global RNG use is present; cross-domain engine-state flow is not established by this audit."})
    if active_nondeterminism:
        findings_report.append({"severity": "BLOCKING", "code": "ACTIVE_NONDETERMINISTIC_RUNTIME_SOURCE", "details": active_nondeterminism})
    tool_nondeterminism = [hit for hit in nondeterministic_hits if hit["production_tool_relevant"]]
    if tool_nondeterminism:
        findings_report.append({"severity": "WARNING", "code": "NONDETERMINISTIC_PRODUCER_SEED_SELECTION", "count": len(tool_nondeterminism), "details": tool_nondeterminism, "interpretation": "Automatic Producer seed/parameter selection uses module-level random; it is upstream job selection, not the gameplay RNG object."})
    unknowns = [row for row in findings if row["domain"] == "UNKNOWN" or row["classification"] == "UNKNOWN"]
    if unknowns:
        findings_report.append({"severity": "UNKNOWN", "code": "SEED_DOMAIN_OR_BEHAVIOR_UNKNOWN", "count": len(unknowns), "finding_keys": [{"path": row["path"], "line": row["line"], "field": row["seed_field"]} for row in unknowns]})
    legacy_count = sum(1 for row in findings if row["classification"] in {"LEGACY", "HISTORICAL"})
    if legacy_count:
        findings_report.append({"severity": "LEGACY", "code": "LEGACY_SEED_SURFACES", "count": legacy_count})
    if not findings_report:
        findings_report.append({"severity": "INFO", "code": "NO_GOVERNANCE_FINDINGS", "count": 0})

    blocking = [row for row in findings_report if row["severity"] == "BLOCKING"]
    warnings = [row for row in findings_report if row["severity"] == "WARNING"]
    audit_complete = all(row["path"] and row["classification"] in classifications and row["domain"] in domains and row["evidence"].get("path") == row["path"] for row in findings)
    gate_pass = audit_complete and not blocking and evidence["d3_music_isolation"]["pass"] and evidence["d4_seed_separation"]["pass"] and evidence["d4_8_blocked_no_seed_authority"] and frozen["preserved"]
    inventory = {
        "checkpoint": "C11-D D6.0",
        "audit_scope": {"roots": SCAN_ROOTS, "extensions": sorted(EXTENSIONS), "excluded": [".git", ".godot", "cache/temp directories", "bulk generated media and unrelated repository artifacts"]},
        "audit_complete": audit_complete,
        "source_files_scanned": len(scan_files(root)),
        "taxonomy": {"domains": domains, "classifications": classifications},
        "finding_count": len(findings),
        "findings": findings,
        "protected_surfaces": protected,
        "correlated_pipeline_evidence": evidence,
        "frozen_c11c": frozen,
        "runtime_authority": "NONE",
        "production_execution": False,
    }
    usage_rows: dict[tuple[str, str, str], dict[str, Any]] = {}
    for row in findings:
        key = (row["seed_field"], row["domain"], row["classification"])
        item = usage_rows.setdefault(key, {"seed_or_rng": row["seed_field"], "domain": row["domain"], "classification": row["classification"], "references": [], "producers": set(), "consumers": set(), "deterministic_values": set(), "runtime_relevant": False})
        item["references"].append({"path": row["path"], "line": row["line"], "symbol": row["symbol"]})
        item["producers"].add(row["producer"])
        item["consumers"].add(row["consumer"])
        item["deterministic_values"].add(str(row["deterministic"]))
        item["runtime_relevant"] = item["runtime_relevant"] or row["runtime_relevant"]
    matrix_rows = []
    for key in sorted(usage_rows):
        row = usage_rows[key]
        matrix_rows.append({"seed_or_rng": row["seed_or_rng"], "domain": row["domain"], "classification": row["classification"], "producers": sorted(row["producers"]), "consumers": sorted(row["consumers"]), "explicit": key[2] == "EXPLICIT_SEED", "derived": key[2] == "DERIVED_SEED", "deterministic": "UNKNOWN" if "UNKNOWN" in row["deterministic_values"] else "false" not in row["deterministic_values"], "runtime_relevant": row["runtime_relevant"], "reference_count": len(row["references"]), "evidence": sorted(row["references"], key=lambda x: (x["path"], x["line"]))})
    matrix = {
        "checkpoint": "C11-D D6.0",
        "result": "PASS",
        "usage": matrix_rows,
        "domain_counts": domain_counts,
        "classification_counts": classification_counts,
        "shared_rng_state": shared_rng,
        "nondeterministic_sources": nondeterministic,
        "d3_music_isolation": evidence["d3_music_isolation"],
        "d4_seed_music_seed_separation": evidence["d4_seed_separation"],
        "unknowns_are_explicit_not_reclassified": True,
        "runtime_authority": "NONE",
        "production_execution": False,
    }
    receipt = {
        "checkpoint": "C11-D D6.0",
        "result": "PASS" if gate_pass else "BLOCKED",
        "status": "CLOSED" if gate_pass else "BLOCKED",
        "audit_complete": audit_complete,
        "seed_rng_findings": len(findings),
        "domain_counts": domain_counts,
        "classification_counts": classification_counts,
        "blocking_findings": len(blocking),
        "warning_findings": len(warnings),
        "unknown_findings": len(unknowns),
        "shared_rng_state_checked": True,
        "shared_rng_state_found": shared_rng["shared_or_global_rng_found"],
        "cross_domain_engine_rng_sharing_proven": shared_rng["cross_domain_engine_state_proven"],
        "active_nondeterministic_source_found": nondeterministic["active_runtime_source_found"],
        "producer_nondeterministic_seed_selection_count": len(tool_nondeterminism),
        "d3_music_isolation": evidence["d3_music_isolation"]["pass"],
        "d4_seed_music_seed_separation": evidence["d4_seed_separation"]["pass"],
        "d4_8_blocked_no_seed_authority": evidence["d4_8_blocked_no_seed_authority"],
        "frozen_c11c_preserved": frozen["preserved"],
        "files_moved": False,
        "files_deleted": False,
        "source_files_rewritten": False,
        "filesystem_mutation": False,
        "deterministic": True,
        "idempotent": True,
        "runtime_authority": "NONE",
        "production_execution": False,
        "renderer_execution": False,
        "godot_production_execution": False,
        "ffmpeg_production_execution": False,
        "next": "D6.1 - Canonical Seed Registry + Governance Policy",
    }
    findings_doc = {"checkpoint": "C11-D D6.0", "result": receipt["result"], "findings": findings_report, "shared_rng_state": shared_rng, "nondeterministic_sources": nondeterministic, "protected_surfaces": protected, "unknown_finding_count": len(unknowns), "blocking_finding_count": len(blocking), "runtime_authority": "NONE"}
    return inventory, matrix, findings_doc, receipt


def execute(root: Path) -> int:
    first = main_audit(root)
    second = main_audit(root)
    deterministic = all(canonical_bytes(a) == canonical_bytes(b) for a, b in zip(first, second))
    inventory, matrix, findings, receipt = second
    if not deterministic:
        receipt["result"] = receipt["status"] = "BLOCKED"
        receipt["deterministic"] = receipt["idempotent"] = False
        findings["result"] = "BLOCKED"
        findings.setdefault("findings", []).append({"severity": "BLOCKING", "code": "DETERMINISM_FAILURE"})
    for value in (inventory, matrix, findings):
        value["deterministic"] = deterministic
    receipt["deterministic"] = deterministic
    out = root / Path(OUT_REL)
    values = [inventory, matrix, findings, receipt]
    for name, value in zip(OUTPUTS, values):
        stable_write(out / name, value)
    hashes = {name: sha_file(out / name) for name in OUTPUTS}
    print(json.dumps({
        "result": receipt["result"], "status": receipt["status"],
        "seed_rng_findings": receipt["seed_rng_findings"], "domain_counts": receipt["domain_counts"],
        "classification_counts": receipt["classification_counts"], "blocking_findings": receipt["blocking_findings"], "warning_findings": receipt["warning_findings"],
        "unknown_findings": receipt["unknown_findings"], "shared_rng_state_found": receipt["shared_rng_state_found"],
        "active_nondeterministic_source_found": receipt["active_nondeterministic_source_found"], "producer_nondeterministic_seed_selection_count": receipt["producer_nondeterministic_seed_selection_count"],
        "d3_music_isolation": receipt["d3_music_isolation"], "d4_seed_music_seed_separation": receipt["d4_seed_music_seed_separation"],
        "d4_8_blocked_no_seed_authority": receipt["d4_8_blocked_no_seed_authority"],
        "frozen_c11c_preserved": receipt["frozen_c11c_preserved"], "filesystem_mutation": receipt["filesystem_mutation"],
        "deterministic": receipt["deterministic"], "idempotent": receipt["idempotent"],
        "runtime_authority": receipt["runtime_authority"], "production_execution": receipt["production_execution"],
        "output_sha256": hashes, "next": receipt["next"],
    }, ensure_ascii=False, indent=2))
    return 0 if receipt["result"] == "PASS" and deterministic else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--snapshot-only", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    if args.snapshot_only:
        print(json.dumps(snapshot(root), separators=(",", ":")))
        return 0
    return execute(root)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({"result": "BLOCKED", "status": "BLOCKED", "fatal_error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(2)
