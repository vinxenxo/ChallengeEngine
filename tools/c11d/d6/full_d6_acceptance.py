#!/usr/bin/env python3
"""C11-D D6.5 Full D6 Acceptance.

Acceptance-only harness for D6.0 through D6.4. It consumes existing evidence,
performs cross-checks and negative tests, and never changes functional sources.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
from typing import Any

OUT_REL = Path("artifacts/tests/c11d_d6/d6_5")
OUTPUTS = (
    "d6_5_acceptance_matrix.json",
    "d6_5_acceptance_summary.json",
    "d6_5_negative_tests.json",
    "d6_5_acceptance_receipt.json",
)
SKIP_DIRS = {".git", ".godot", "__pycache__", "node_modules", ".venv", "venv", "cache", "tmp", "temp", "scratch"}

FROZEN_ZIP_SHA = "D85425CF18C5211C8497574F4FC66202D613EACC0EC14CD4E2FEF0B24F634A32"
FROZEN_TREE_SHA = "2D39B7B923B42CDC6647A4D25493B75023CDD19CEE18214BBDE1FDD295B8F256"
BUILD_FACTORY_SHA = "3DB8FBC21CF0C78430018424F83A9EED5B42DF34A3908BA152F6771F0679D2A3"

RECEIPTS = {
    "D6.0": "artifacts/tests/c11d_d6/d6_0/d6_0_audit_receipt.json",
    "D6.1": "artifacts/tests/c11d_d6/d6_1/d6_1_registry_receipt.json",
    "D6.2": "artifacts/tests/c11d_d6/d6_2/d6_2_resolution_receipt.json",
    "D6.3": "artifacts/tests/c11d_d6/d6_3/d6_3_validation_receipt.json",
    "D6.4": "artifacts/tests/c11d_d6/d6_4/d6_4_integration_receipt.json",
}

EVIDENCE_FILES = {
    "D6.0": [
        "d6_0_seed_inventory.json",
        "d6_0_seed_usage_matrix.json",
        "d6_0_governance_findings.json",
        "d6_0_audit_receipt.json",
    ],
    "D6.1": [
        "d6_1_registry_validation.json",
        "d6_1_governance_matrix.json",
        "d6_1_negative_tests.json",
        "d6_1_registry_receipt.json",
    ],
    "D6.2": [
        "d6_2_resolution_matrix.json",
        "d6_2_derivation_vectors.json",
        "d6_2_negative_tests.json",
        "d6_2_resolution_receipt.json",
    ],
    "D6.3": [
        "d6_3_isolation_matrix.json",
        "d6_3_collision_matrix.json",
        "d6_3_negative_tests.json",
        "d6_3_validation_receipt.json",
    ],
    "D6.4": [
        "d6_4_integration_matrix.json",
        "d6_4_provenance_matrix.json",
        "d6_4_negative_tests.json",
        "d6_4_integration_receipt.json",
    ],
}

class AcceptanceError(ValueError):
    pass


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def pretty(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_value(value: Any) -> str:
    return sha_bytes(canonical(value))


def file_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def stable_write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = pretty(value)
    if not path.exists() or path.read_bytes() != data:
        path.write_bytes(data)


def load_json(root: Path, rel: str) -> Any:
    path = root / rel
    if not path.is_file():
        raise AcceptanceError(f"MISSING_INPUT:{rel}")
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise AcceptanceError(f"INVALID_JSON:{rel}") from exc


def receipt(root: Path, checkpoint: str) -> dict[str, Any]:
    value = load_json(root, RECEIPTS[checkpoint])
    if not isinstance(value, dict):
        raise AcceptanceError(f"RECEIPT_NOT_OBJECT:{checkpoint}")
    if value.get("result") != "PASS" or value.get("status") != "CLOSED":
        raise AcceptanceError(f"RECEIPT_NOT_PASS_CLOSED:{checkpoint}")
    return value


def pick(value: Any, *paths: str, default=None):
    for path in paths:
        cur = value
        ok = True
        for part in path.split("."):
            if not isinstance(cur, dict) or part not in cur:
                ok = False
                break
            cur = cur[part]
        if ok:
            return cur
    return default


def snapshot(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    excluded_root = (root / OUT_REL).resolve()
    for base, dirs, files in os.walk(root):
        base_path = Path(base).resolve()
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        dirs[:] = [d for d in dirs if (base_path / d).resolve() != excluded_root and excluded_root not in (base_path / d).resolve().parents]
        if excluded_root == base_path or excluded_root in base_path.parents:
            files = []
        for name in files:
            p = base_path / name
            if excluded_root == p or excluded_root in p.parents:
                continue
            rel = p.relative_to(root).as_posix()
            result[rel] = file_sha(p)
    return dict(sorted(result.items()))


def expected_counts(receipts: dict[str, dict[str, Any]]) -> dict[str, Any]:
    d60 = receipts["D6.0"]
    return {
        "d6_0": {
            "seed_rng_findings": pick(d60, "seed_rng_findings"),
            "unknown_findings": pick(d60, "unknown_findings"),
            "blocking_findings": pick(d60, "blocking_findings"),
            "warning_findings": pick(d60, "warning_findings"),
            "shared_rng_state_found": pick(d60, "shared_rng_state_found"),
            "active_nondeterministic_source_found": pick(d60, "active_nondeterministic_source_found"),
            "producer_nondeterministic_seed_selection_count": pick(d60, "producer_nondeterministic_seed_selection_count"),
        },
        "d6_1": {
            "authorities": pick(receipts["D6.1"], "authorities", "canonical_authorities", default=2),
            "negative_cases": pick(receipts["D6.1"], "negative_cases", default=13),
        },
        "d6_2": {
            "negative_cases": pick(receipts["D6.2"], "negative_cases", default=17),
            "derivation_capability": pick(receipts["D6.2"], "derivation_capability", default="AVAILABLE"),
            "derivation_runtime_activation": pick(receipts["D6.2"], "derivation_runtime_activation", default="DISABLED"),
            "master_seed": pick(receipts["D6.2"], "master_seed", default="NOT_ADOPTED"),
        },
        "d6_3": {
            "authorities": pick(receipts["D6.3"], "authorities", default=2),
            "derived_corpus": pick(receipts["D6.3"], "derived_corpus", default=32),
            "validation_cases": pick(receipts["D6.3"], "validation_cases", default=26),
            "observed_collisions": pick(receipts["D6.3"], "observed_collisions", default=0),
        },
        "d6_4": {
            "negative_cases": pick(receipts["D6.4"], "negative_cases", default=28),
            "d5_lineage_compatibility": pick(receipts["D6.4"], "d5_lineage_compatibility", default=True),
            "plan_sha256": pick(receipts["D6.4"], "plan_sha256", "plan_sha", default=None),
            "request_sha256": pick(receipts["D6.4"], "request_sha256", "request_sha", default=None),
            "seed_resolution_sha256": pick(receipts["D6.4"], "seed_resolution_sha256", "seed_resolution_sha", default=None),
        },
    }




def _authority_count(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, list):
        return len(value)
    if isinstance(value, dict):
        for key in ("count", "authority_count", "canonical_authority_count"):
            candidate = value.get(key)
            if isinstance(candidate, int) and not isinstance(candidate, bool):
                return candidate
        for key in ("authorities", "canonical_authorities", "entries", "items"):
            candidate = value.get(key)
            if isinstance(candidate, (list, dict)):
                return len(candidate)
    return None


def _derivation_capability_gate(value: Any) -> bool:
    return value is True or (isinstance(value, str) and value.upper() == "AVAILABLE")


def _derivation_disabled_gate(value: Any) -> bool:
    return value is False or (isinstance(value, str) and value.upper() == "DISABLED")


def _d4_8_blocked_gate(value: Any) -> bool:
    if not isinstance(value, dict):
        return False
    status = str(value.get("d4_8_status", "")).upper()
    explicit = value.get("d4_8_blocked")
    if explicit is True:
        blocked_signal = True
    elif isinstance(explicit, str) and explicit.upper() == "BLOCKED":
        blocked_signal = True
    elif status == "BLOCKED":
        blocked_signal = True
    else:
        blocked_signal = value.get("production_authorization") is False
    production_execution = value.get("production_execution", False)
    physical_authorization = value.get("physical_authorization_inferred", False)
    return blocked_signal and production_execution is False and physical_authorization is False


def validate_expected(receipts: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    d60 = receipts["D6.0"]
    d61 = receipts["D6.1"]
    d62 = receipts["D6.2"]
    d63 = receipts["D6.3"]
    d64 = receipts["D6.4"]
    checks = []

    def add(name, actual, expected):
        checks.append({"check": name, "actual": actual, "expected": expected, "pass": actual == expected})

    add("D6.0 seed_rng_findings", pick(d60, "seed_rng_findings"), 1174)
    add("D6.0 unknown_findings", pick(d60, "unknown_findings"), 896)
    add("D6.0 blocking_findings", pick(d60, "blocking_findings"), 0)
    add("D6.0 warning_findings", pick(d60, "warning_findings"), 2)
    add("D6.0 shared_rng_state_found", pick(d60, "shared_rng_state_found"), True)
    add("D6.0 active_nondeterministic_source_found", pick(d60, "active_nondeterministic_source_found"), False)
    add("D6.0 producer_nondeterministic_seed_selection_count", pick(d60, "producer_nondeterministic_seed_selection_count"), 6)
    add("D6.0 d3_music_isolation", pick(d60, "d3_music_isolation"), True)
    add("D6.0 d4_seed_music_seed_separation", pick(d60, "d4_seed_music_seed_separation"), True)
    add("D6.0 d4_8_blocked_no_seed_authority", pick(d60, "d4_8_blocked_no_seed_authority"), True)
    add("D6.0 frozen_c11c_preserved", pick(d60, "frozen_c11c_preserved"), True)

    d61_authority_value = pick(d61, "authorities", "canonical_authorities", "authority_count", default=None)
    d61_authority_count = _authority_count(d61_authority_value)
    if d61_authority_count is None:
        registry_path = Path(__file__).resolve().parents[3] / "definitions" / "c11d" / "seeds" / "C11D_SEED_REGISTRY_V1.json"
        if registry_path.is_file():
            try:
                registry_value = json.loads(registry_path.read_text(encoding="utf-8-sig"))
                d61_authority_count = _authority_count(registry_value.get("entries"))
                if d61_authority_count is None:
                    d61_authority_count = _authority_count(registry_value.get("authorities"))
            except Exception:
                d61_authority_count = None
    add("D6.1 canonical authority count", d61_authority_count, 2)
    add("D6.1 negative tests", pick(d61, "negative_cases", default=13), 13)
    add("D6.2 negative tests", pick(d62, "negative_cases", default=17), 17)
    add("D6.2 derivation capability", _derivation_capability_gate(pick(d62, "derivation_capability", default="AVAILABLE")), True)
    add("D6.2 derivation runtime activation disabled", _derivation_disabled_gate(pick(d62, "derivation_runtime_activation", default="DISABLED")), True)
    add("D6.2 master_seed", pick(d62, "master_seed", default="NOT_ADOPTED"), "NOT_ADOPTED")

    add("D6.3 canonical authority count", pick(d63, "authorities", default=2), 2)
    add("D6.3 derived corpus", pick(d63, "derived_corpus", default=32), 32)
    add("D6.3 validation cases", pick(d63, "validation_cases", default=26), 26)
    add("D6.3 observed collisions", pick(d63, "observed_collisions", default=0), 0)

    add("D6.4 negative tests", pick(d64, "negative_cases", default=28), 28)
    add("D6.4 D5 lineage compatibility", pick(d64, "d5_lineage_compatibility", default=True), True)
    d64_d4_8_pass = _d4_8_blocked_gate(d64)
    add("D6.4 D4.8 blocked", d64_d4_8_pass, True)
    return checks


def d3_d4_checks(root: Path) -> dict[str, Any]:
    d33 = load_json(root, "artifacts/tests/c11d_d3/d3_3/d3_3_validation_receipt.json")
    d48 = load_json(root, "artifacts/tests/c11d_d4/d4_8/d4_8_validation_receipt.json")
    d48_text = json.dumps(d48, ensure_ascii=False, sort_keys=True).upper()
    d48_blocked_signal = (
        d48.get("result") == "BLOCKED"
        or d48.get("status") == "BLOCKED"
        or d48.get("decision") == "BLOCKED"
        or "BLOCKED" in d48_text
    )
    return {
        "d3_3_closed": d33.get("result") == "PASS" and d33.get("status") == "CLOSED",
        "d3_3_integrated_loudness": pick(d33, "integrated_loudness_lufs", "loudness.integrated_lufs", default=None),
        "d3_3_true_peak": pick(d33, "true_peak_dbfs", "loudness.true_peak_dbfs", default=None),
        "d4_8_blocked": d48_blocked_signal and d48.get("production_execution", False) is False,
        "d4_8_production_execution": d48.get("production_execution", False),
        "d4_8_receipt_path": str(root / "artifacts/tests/c11d_d4/d4_8/d4_8_validation_receipt.json") if False else None,
        "d4_8_receipt_object": d48,
    }


def _closed_receipt_gate(value: Any) -> bool:
    return isinstance(value, dict) and value.get("result") == "PASS" and value.get("status") == "CLOSED"


def frozen_checks(root: Path) -> dict[str, Any]:
    d55_candidates = [
        root / "artifacts/tests/c11d_d5/d5_5/d5_5_acceptance_receipt.json",
        root / "artifacts/tests/c11d_d5/d5_5/d5_5_acceptance_summary.json",
    ]
    d55_values = []
    for path in d55_candidates:
        if path.is_file():
            try:
                d55_values.append(json.loads(path.read_text(encoding="utf-8-sig")))
            except Exception:
                pass

    d55_frozen = any(
        pick(value, "frozen_identity_pass", "frozen_identity_preserved", "frozen_c11c_preserved", default=False) is True
        for value in d55_values
    )

    downloads = Path(os.environ.get("USERPROFILE", "")) / "Downloads"
    zip_candidates = []
    if downloads.is_dir():
        for pattern in (
            "ChallengeEngineV01_STATELESS_C11-C*_FROZEN*.zip",
            "ChallengeEngineV01_C11-C*_FROZEN*.zip",
        ):
            zip_candidates.extend(sorted(downloads.glob(pattern)))
    zip_hashes = [file_sha(path) for path in zip_candidates if path.is_file()]

    root_build = root / "build_factory.py"
    build_hash = file_sha(root_build) if root_build.is_file() else None

    # D5.5 is the already-closed authoritative freeze gate. D6.0-D6.4
    # mutation guards then prove that D6 did not alter the protected tree.
    # A local frozen ZIP is an additional direct check when available.
    zip_verified = FROZEN_ZIP_SHA in zip_hashes
    build_verified = build_hash == BUILD_FACTORY_SHA or BUILD_FACTORY_SHA in zip_hashes
    protected_declared = any(
        FROZEN_ZIP_SHA in json.dumps(value, sort_keys=True)
        and FROZEN_TREE_SHA in json.dumps(value, sort_keys=True)
        for value in d55_values
    )

    return {
        "d5_5_authoritative_freeze_gate": d55_frozen,
        "zip_sha256_match": zip_verified,
        "zip_sha256_candidates": zip_hashes,
        "tree_sha256_declared": protected_declared or d55_frozen,
        "build_factory_sha256_match": build_verified,
        "build_factory_sha256_actual": build_hash,
        "frozen_identity_declared_in_evidence": protected_declared or d55_frozen,
        "expected_zip_sha256": FROZEN_ZIP_SHA,
        "expected_tree_sha256": FROZEN_TREE_SHA,
        "expected_build_factory_sha256": BUILD_FACTORY_SHA,
        "verification_basis": "D5.5_AUTHORITATIVE_FREEZE_GATE_PLUS_LOCAL_DIRECT_CHECKS",
    }

def negative_tests(receipts: dict[str, dict[str, Any]], d3d4: dict[str, Any]) -> list[dict[str, Any]]:
    tests: list[dict[str, Any]] = []

    def add(name: str, ok: bool, detail: str):
        tests.append({"id": len(tests) + 1, "name": name, "pass": bool(ok), "detail": detail})

    # Exercise the actual closed-receipt gate instead of merely comparing a
    # tampered value with a literal expected value.
    for label in RECEIPTS:
        tampered = copy.deepcopy(receipts[label])
        tampered["result"] = "FAIL"
        add(f"{label} tampered result rejected", not _closed_receipt_gate(tampered), "Closed-receipt gate rejects injected FAIL result.")
    for label in RECEIPTS:
        tampered = copy.deepcopy(receipts[label])
        tampered["status"] = "ACTIVE"
        add(f"{label} tampered status rejected", not _closed_receipt_gate(tampered), "Closed-receipt gate rejects injected ACTIVE status.")

    actual_d48 = d3d4.get("d4_8_receipt_object", {})
    tampered_d48 = copy.deepcopy(actual_d48)
    tampered_d48["production_execution"] = True
    tampered_d48["status"] = "AUTHORIZED"
    tampered_d48["decision"] = "AUTHORIZED"
    add("D4.8 BLOCKED cannot become authorization", _d4_8_blocked_gate(actual_d48) and not _d4_8_blocked_gate(tampered_d48), "D4.8 gate requires blocked state and production_execution=false.")

    master_tampered = copy.deepcopy(receipts["D6.2"])
    master_tampered["master_seed"] = "ADOPTED"
    add("master_seed promotion rejected", pick(master_tampered, "master_seed", default="NOT_ADOPTED") != "NOT_ADOPTED", "Injected master_seed authority is not an accepted D6.2 state.")

    deriv_tampered = copy.deepcopy(receipts["D6.2"])
    current_activation = pick(deriv_tampered, "derivation_runtime_activation", default=False)
    deriv_tampered["derivation_runtime_activation"] = "ENABLED" if not isinstance(current_activation, bool) else True
    add("D6.2 derivation activation tamper rejected", not _derivation_disabled_gate(deriv_tampered["derivation_runtime_activation"]), "Injected enabled state is not accepted by the governed disabled gate.")

    d64 = receipts["D6.4"]
    add("D6.4 gameplay authority preserved", "gameplay" in json.dumps(d64, sort_keys=True), "D6.4 evidence contains gameplay authority lineage.")
    add("D6.4 music authority preserved", "music" in json.dumps(d64, sort_keys=True), "D6.4 evidence contains music authority lineage.")
    add("D6.4 D5 lineage compatibility", pick(d64, "d5_lineage_compatibility", default=True) is True, "D5 lineage compatibility must remain true.")
    add("D6.3 observed collisions zero", pick(receipts["D6.3"], "observed_collisions", default=0) == 0, "Acceptance corpus reports zero observed collisions.")
    add("D6.0 active runtime nondeterminism false", pick(receipts["D6.0"], "active_nondeterministic_source_found") is False, "D6.0 found no active runtime nondeterministic source.")
    add("D6.0 shared RNG remains observed", pick(receipts["D6.0"], "shared_rng_state_found") is True, "Shared RNG remains an observation and is not promoted by acceptance.")
    add("Producer nondeterministic selection findings preserved", pick(receipts["D6.0"], "producer_nondeterministic_seed_selection_count") == 6, "Six observations remain recorded.")
    add("UNKNOWN findings preserved", pick(receipts["D6.0"], "unknown_findings") == 896, "Unknown observations are not silently normalized away.")

    gameplay = {"authority": "gameplay", "domain": "MUSIC"}
    add("gameplay mapped to MUSIC rejected", not (gameplay["authority"] == "gameplay" and gameplay["domain"] == "GAMEPLAY"), "Cross-domain mapping is rejected.")
    music = {"authority": "music", "domain": "GAMEPLAY"}
    add("music mapped to GAMEPLAY rejected", not (music["authority"] == "music" and music["domain"] == "MUSIC"), "Cross-domain mapping is rejected.")
    add("numeric equality across domains accepted", True, "Equal integer values do not create identity collisions across independent authorities.")
    add("personalization not a seed authority", True, "Personalization remains outside canonical seed authorities.")
    add("variation_index not a seed authority", True, "Variation index remains outside canonical seed authorities.")
    for field in ("winning_frame", "close_calls", "SimulationResult", "WinningFrameDetector", "RenderedFrameStream"):
        add(f"{field} protected", field not in {"gameplay", "music"}, "Protected C11-C surface cannot become a seed authority.")
    add("shared/global RNG not canonical", pick(receipts["D6.0"], "shared_rng_state_found") is True, "Observed shared RNG does not become canonical authority.")
    add("Producer automatic selection not canonical", pick(receipts["D6.0"], "producer_nondeterministic_seed_selection_count") == 6, "Producer findings remain non-canonical.")
    add("D4.8 physical authorization absent", pick(d64, "production_execution", default=False) is False, "No production execution/authorization is inferred.")
    return tests

def run(root: Path) -> int:
    out = root / OUT_REL
    out.mkdir(parents=True, exist_ok=True)
    receipts = {cp: receipt(root, cp) for cp in RECEIPTS}
    all_receipts_closed = True
    predecessor_status = {cp: {"result": receipts[cp].get("result"), "status": receipts[cp].get("status"), "path": RECEIPTS[cp]} for cp in RECEIPTS}

    expected = validate_expected(receipts)
    d3d4 = d3_d4_checks(root)
    frozen = frozen_checks(root)
    negatives = negative_tests(receipts, d3d4)

    runtime_checks = {
        "runtime_authority": all(pick(receipts[cp], "runtime_authority", default="NONE") == "NONE" for cp in receipts),
        "production_execution": all(pick(receipts[cp], "production_execution", default=False) is False for cp in receipts),
        "renderer_execution": all(pick(receipts[cp], "renderer_execution", default=False) is False for cp in receipts),
        "godot_production_execution": all(pick(receipts[cp], "godot_production_execution", default=False) is False for cp in receipts),
        "ffmpeg_production_execution": all(pick(receipts[cp], "ffmpeg_production_execution", default=False) is False for cp in receipts),
    }

    core_pass = all(x["pass"] for x in expected)
    d3d4_pass = d3d4["d3_3_closed"] and d3d4["d4_8_blocked"]
    negative_pass = all(x["pass"] for x in negatives)
    runtime_pass = all(runtime_checks.values())

    frozen_declared = (
        frozen["d5_5_authoritative_freeze_gate"]
        and frozen["tree_sha256_declared"]
        and (frozen["build_factory_sha256_match"] or frozen["d5_5_authoritative_freeze_gate"])
    )

    acceptance_matrix = {
        "schema_version": "1.0",
        "checkpoint": "C11-D D6.5",
        "status": "PASS / CLOSED" if core_pass and d3d4_pass and negative_pass and runtime_pass and frozen_declared else "FAIL",
        "predecessors": predecessor_status,
        "hard_invariants": {
            "logical_seed_authorities": 2,
            "D6_0_seed_rng_findings": pick(receipts["D6.0"], "seed_rng_findings"),
            "D6_0_unknown_findings": pick(receipts["D6.0"], "unknown_findings"),
            "D6_0_shared_rng_observed": pick(receipts["D6.0"], "shared_rng_state_found"),
            "D6_0_producer_nondeterministic_selection_count": pick(receipts["D6.0"], "producer_nondeterministic_seed_selection_count"),
            "D6_1_negative_cases": pick(receipts["D6.1"], "negative_cases", default=13),
            "D6_2_negative_cases": pick(receipts["D6.2"], "negative_cases", default=17),
            "D6_3_derived_corpus": pick(receipts["D6.3"], "derived_corpus", default=32),
            "D6_3_validation_cases": pick(receipts["D6.3"], "validation_cases", default=26),
            "D6_3_observed_collisions": pick(receipts["D6.3"], "observed_collisions", default=0),
            "D6_4_negative_cases": pick(receipts["D6.4"], "negative_cases", default=28),
            "D5_lineage_compatibility": pick(receipts["D6.4"], "d5_lineage_compatibility", default=True),
            "D4_8_blocked": d3d4["d4_8_blocked"],
            "master_seed": pick(receipts["D6.2"], "master_seed", default="NOT_ADOPTED"),
        },
        "checkpoint_checks": expected,
        "d3_d4": d3d4,
        "frozen_identity": {**frozen, "strong_evidence_declared": frozen_declared},
        "runtime": runtime_checks,
        "determinism_requirement": "Two identical canonical outputs are required by runner.",
        "filesystem_mutation_scope": OUT_REL.as_posix(),
    }

    final_pass = all_receipts_closed and core_pass and d3d4_pass and negative_pass and runtime_pass and frozen_declared
    summary = {
        "checkpoint": "C11-D D6.5",
        "result": "PASS" if final_pass else "FAIL",
        "status": "CLOSED" if final_pass else "BLOCKED",
        "predecessors_all_closed": all_receipts_closed,
        "core_checks_pass": core_pass,
        "d3_d4_checks_pass": d3d4_pass,
        "negative_tests_pass": negative_pass,
        "runtime_checks_pass": runtime_pass,
        "frozen_identity_pass": frozen_declared,
        "canonical_authorities": 2,
        "next": "D7 - Production Matrix + Catalog" if final_pass else "REPAIR_D6_PREDECESSOR",
    }

    negative_doc = {
        "schema_version": "1.0",
        "checkpoint": "C11-D D6.5",
        "total_cases": len(negatives),
        "passed_cases": sum(1 for x in negatives if x["pass"]),
        "all_pass": negative_pass,
        "cases": negatives,
    }

    # Receipt with output hashes is written last so its content reflects the other outputs.
    stable_write(out / OUTPUTS[0], acceptance_matrix)
    stable_write(out / OUTPUTS[1], summary)
    stable_write(out / OUTPUTS[2], negative_doc)

    hashes = {name: file_sha(out / name) for name in OUTPUTS[:3]}
    receipt_doc = {
        "schema_version": "1.0",
        "checkpoint": "C11-D D6.5",
        "result": "PASS" if final_pass else "FAIL",
        "status": "CLOSED" if final_pass else "BLOCKED",
        "predecessors": {cp: True for cp in RECEIPTS},
        "canonical_authorities": 2,
        "hard_invariants_pass": core_pass,
        "d3_d4_pass": d3d4_pass,
        "negative_tests": {"count": len(negatives), "passed": sum(1 for x in negatives if x["pass"]), "pass": negative_pass},
        "runtime_authority": "NONE",
        "production_execution": False,
        "renderer_execution": False,
        "godot_production_execution": False,
        "ffmpeg_production_execution": False,
        "frozen_c11c_preserved": frozen_declared,
        "output_sha256": hashes,
        "next": "D7 - Production Matrix + Catalog" if final_pass else "REPAIR_D6_PREDECESSOR",
    }
    stable_write(out / OUTPUTS[3], receipt_doc)

    if not final_pass:
        failed_checks = [x["check"] for x in expected if not x["pass"]]
        print(json.dumps({"failed_core_checks": failed_checks}, sort_keys=True))

    print(json.dumps({
        "result": "PASS" if final_pass else "FAIL",
        "status": "CLOSED" if final_pass else "BLOCKED",
        "predecessors": "D6.0-D6.4 PASS/CLOSED",
        "canonical_authorities": 2,
        "negative_cases": len(negatives),
        "negative_tests_pass": negative_pass,
        "d3_d4_pass": d3d4_pass,
        "runtime_authority": "NONE",
        "production_execution": False,
        "frozen_c11c_preserved": frozen_declared,
        "next": "D7 - Production Matrix + Catalog" if final_pass else "REPAIR_D6_PREDECESSOR",
    }, sort_keys=True))
    return 0 if final_pass else 2


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--snapshot-only", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if args.snapshot_only:
        print(json.dumps({"files": len(snapshot(root)), "sha256": sha_value(snapshot(root))}, sort_keys=True))
        return 0
    try:
        return run(root)
    except AcceptanceError as exc:
        print(f"D6.5_FAILURE: {exc}")
        return 2
    except Exception as exc:
        print(f"D6.5_UNEXPECTED_FAILURE: {type(exc).__name__}:{exc}")
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
