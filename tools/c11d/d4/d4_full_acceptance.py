#!/usr/bin/env python3
"""Full D4 acceptance and focused regression across the existing D4 components."""

import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TOOLS = ROOT / "tools" / "c11d" / "d4"
ARTIFACTS = ROOT / "artifacts" / "tests" / "c11d_d4"
OUTPUT_DIR = ARTIFACTS / "d4_9"
EXPECTED_C11C_ARCHIVE_SHA256 = "d85425cf18c5211c8497574f4fc66202d613eacc0ec14cd4e2fef0b24f634a32"
SCHEMA_PATH = ROOT / "definitions" / "c11d" / "production" / "C11D_PRODUCTION_REQUEST_SCHEMA_V1.json"
PERSONALIZATION_REGISTRY_PATH = ROOT / "definitions" / "c11d" / "personalization" / "C11D_PERSONALIZATION_PROFILE_REGISTRY_V1.json"
RECEIPT_PATHS = {
    "D4.0": ARTIFACTS / "d4_0_validation_receipt.json",
    "D4.1": ARTIFACTS / "d4_1" / "d4_1_validation_receipt.json",
    "D4.2": ARTIFACTS / "d4_2" / "d4_2_validation_receipt.json",
    "D4.3": ARTIFACTS / "d4_3" / "d4_3_validation_receipt.json",
    "D4.4": ARTIFACTS / "d4_4" / "d4_4_validation_receipt.json",
    "D4.5": ARTIFACTS / "d4_5" / "d4_5_validation_receipt.json",
    "D4.6": ARTIFACTS / "d4_6" / "d4_6_validation_receipt.json",
    "D4.7": ARTIFACTS / "d4_7" / "d4_7_validation_receipt.json",
    "D4.8": ARTIFACTS / "d4_8" / "d4_8_validation_receipt.json",
}


def import_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load canonical D4 module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


NORMALIZER = import_module("c11d_d4_2_normalizer", TOOLS / "production_request_normalizer.py")
ORCHESTRATOR = import_module("c11d_d4_4_orchestrator", TOOLS / "canonical_production_orchestrator.py")


def load_json(path):
    with open(path, "r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def stable_sha256(value):
    raw = json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def run_regressions():
    """Call each component's own self-test; do not reproduce its assertions here."""
    commands = [
        ("D4.2", [
            sys.executable, str(TOOLS / "production_request_normalizer.py"),
            "--schema", str(SCHEMA_PATH), "--self-test",
            "--receipt", str(RECEIPT_PATHS["D4.2"]),
            "--evidence", str(ARTIFACTS / "d4_2" / "d4_2_normalization_evidence.json"),
            "--parity", str(ARTIFACTS / "d4_2" / "d4_2_gui_cli_parity.json"),
        ]),
        ("D4.3", [
            sys.executable, str(TOOLS / "personalization_resolver.py"),
            "--registry", str(PERSONALIZATION_REGISTRY_PATH), "--self-test",
            "--receipt", str(RECEIPT_PATHS["D4.3"]),
            "--evidence", str(ARTIFACTS / "d4_3" / "d4_3_personalization_evidence.json"),
        ]),
        ("D4.4", [
            sys.executable, str(TOOLS / "canonical_production_orchestrator.py"),
            "--schema", str(SCHEMA_PATH),
            "--personalization-registry", str(PERSONALIZATION_REGISTRY_PATH), "--self-test",
            "--evidence", str(ARTIFACTS / "d4_4" / "d4_4_orchestration_evidence.json"),
            "--parity", str(ARTIFACTS / "d4_4" / "d4_4_gui_cli_plan_parity.json"),
            "--plan", str(ARTIFACTS / "d4_4" / "d4_4_example_production_plan.json"),
            "--receipt", str(RECEIPT_PATHS["D4.4"]),
        ]),
        ("D4.5", [
            sys.executable, str(TOOLS / "production_cli.py"), "--self-test",
            "--evidence", str(ARTIFACTS / "d4_5" / "d4_5_cli_adapter_evidence.json"),
            "--plan", str(ARTIFACTS / "d4_5" / "d4_5_cli_plan.json"),
            "--receipt", str(RECEIPT_PATHS["D4.5"]),
        ]),
        ("D4.6", [
            sys.executable, str(TOOLS / "gui_production_adapter.py"), "--self-test",
            "--evidence", str(ARTIFACTS / "d4_6" / "d4_6_gui_adapter_evidence.json"),
            "--plan", str(ARTIFACTS / "d4_6" / "d4_6_gui_plan.json"),
            "--parity", str(ARTIFACTS / "d4_6" / "d4_6_gui_cli_parity.json"),
            "--receipt", str(RECEIPT_PATHS["D4.6"]),
        ]),
        ("D4.7", [
            sys.executable, str(TOOLS / "gui_cli_parity.py"),
            "--output-dir", str(ARTIFACTS / "d4_7"),
        ]),
        ("D4.8", [
            sys.executable, str(TOOLS / "production_activation_governance.py"),
            "--output-dir", str(ARTIFACTS / "d4_8"),
        ]),
    ]
    result = {}
    for checkpoint, command in commands:
        try:
            completed = subprocess.run(
                command,
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            result[checkpoint] = {
                "exit_code": completed.returncode,
                "pass": completed.returncode == 0,
                "error_tail": completed.stderr[-1200:] if completed.returncode else "",
            }
        except Exception as exc:
            result[checkpoint] = {"exit_code": -1, "pass": False, "error_tail": str(exc)}
    return result


def read_checkpoint_receipts():
    receipts = {}
    results = {}
    for checkpoint, path in RECEIPT_PATHS.items():
        try:
            receipt = load_json(path)
            receipts[checkpoint] = receipt
            results[checkpoint] = (
                receipt.get("result") == "PASS"
                and receipt.get("status") == "CLOSED"
                and receipt.get("checkpoint") == f"C11-D {checkpoint}"
            )
        except Exception as exc:
            receipts[checkpoint] = {}
            results[checkpoint] = False
    return receipts, results


def architecture_gate():
    module_names = (
        "production_request_normalizer.py",
        "personalization_resolver.py",
        "canonical_production_orchestrator.py",
    )
    module_counts = {
        name: sum(1 for path in (ROOT / "tools" / "c11d" / "d4").rglob(name))
        for name in module_names
    }
    cli_text = (TOOLS / "production_cli.py").read_text(encoding="utf-8")
    gui_text = (TOOLS / "gui_production_adapter.py").read_text(encoding="utf-8")
    personalization_registry = load_json(ROOT / "definitions" / "c11d" / "personalization" / "C11D_PERSONALIZATION_PROFILE_REGISTRY_V1.json")
    active_profile_ids = [
        item.get("profile_id")
        for item in personalization_registry.get("profiles", [])
        if item.get("status") == "ACTIVE"
    ]
    gates = {
        "canonical_request": ("normalize_request" in cli_text and "normalize_request" in gui_text),
        "single_normalizer": module_counts[module_names[0]] == 1,
        "single_personalization_resolver": module_counts[module_names[1]] == 1,
        "single_orchestrator": module_counts[module_names[2]] == 1,
        "gui_cli_same_pipeline": all(
            term in cli_text and term in gui_text
            for term in ("production_request_normalizer.py", "personalization_resolver.py", "canonical_production_orchestrator.py")
        ),
        "gui_to_d42_d43_d44": all(term in gui_text for term in ("NORMALIZER.normalize_request", "PERSONALIZATION.normalize_personalization", "ORCHESTRATOR.build_plan")),
        "cli_to_d42_d43_d44": all(term in cli_text for term in ("NORMALIZER.normalize_request", "PERSONALIZATION.normalize_personalization", "ORCHESTRATOR.build_plan")),
        "active_personalization_registry_entries_unique": len(active_profile_ids) == len(set(active_profile_ids)) and len(active_profile_ids) == 2,
    }
    return gates, {**module_counts, "active_personalization_profiles": len(active_profile_ids)}


def runtime_scan():
    names = (
        "production_cli.py",
        "gui_production_adapter.py",
        "canonical_production_orchestrator.py",
        "production_activation_governance.py",
        "production_request_normalizer.py",
        "personalization_resolver.py",
    )
    command_patterns = (
        re.compile(r"\bffmpeg(?:\.exe)?\b", re.IGNORECASE),
        re.compile(r"\bgodot(?:\.exe)?\b", re.IGNORECASE),
        re.compile(r"\brenderer\s*\.\s*(?:execute|run|render)\s*\(|\bexecute_renderer\s*\(", re.IGNORECASE),
        re.compile(r"\b(?:publish|upload)\s*\(", re.IGNORECASE),
    )
    hits = {}
    for name in names:
        text = (TOOLS / name).read_text(encoding="utf-8")
        hits[name] = [pattern.pattern for pattern in command_patterns if pattern.search(text)]
    return hits, all(not values for values in hits.values())


def evaluate(receipts, checkpoint_pass, regression, regression_pass):
    audit_path = ARTIFACTS / "d4_0_production_flow_audit.json"
    freeze_receipt = receipts.get("D4.0", {})
    d41_receipt = receipts.get("D4.1", {})
    try:
        audit = load_json(audit_path)
    except Exception:
        audit = {}
    stored_archive_hash = str(freeze_receipt.get("c11c_baseline_archive_sha256", "")).lower()
    audit_archive_hash = str(audit.get("baseline", {}).get("archive_sha256", "")).lower()
    frozen_hash_valid = (
        stored_archive_hash == EXPECTED_C11C_ARCHIVE_SHA256
        and audit_archive_hash == EXPECTED_C11C_ARCHIVE_SHA256
        and d41_receipt.get("frozen_c11c_changes") is False
        and audit.get("scope", {}).get("c11c_engine_modified") is False
    )

    architecture, module_counts = architecture_gate()
    architecture_pass = all(architecture.values())

    d47 = receipts.get("D4.7", {})
    matrix_path = ARTIFACTS / "d4_7" / "d4_7_parity_matrix.json"
    try:
        parity_matrix = load_json(matrix_path)
    except Exception:
        parity_matrix = {}
    matrix_cases = parity_matrix.get("matrix", [])
    matrix_case_gates = all(
        case.get("pass") is True
        and case.get("canonical_request_equal") is True
        and case.get("request_sha_equal") is True
        and case.get("plan_equal") is True
        and case.get("plan_sha_equal") is True
        and case.get("renderer") is False
        and case.get("execution") is False
        for case in matrix_cases
    )
    parity = {
        "cases": d47.get("test_cases", 0),
        "passed": d47.get("passed_cases", 0),
        "failed": d47.get("failed_cases", -1),
        "challenge_coverage": d47.get("challenge_coverage", 0),
        "delivery_profile_coverage": d47.get("delivery_profile_coverage", 0),
        "mode_coverage": d47.get("mode_coverage", 0),
        "personalization_profiles_covered": d47.get("personalization_profiles_covered", 0),
        "request_sha_parity": d47.get("request_sha256_parity") is True,
        "plan_sha_parity": d47.get("plan_sha256_parity") is True,
        "canonical_request_parity": d47.get("canonical_request_parity") is True,
        "production_plan_parity": d47.get("production_plan_parity") is True,
        "plan_hash_owner": d47.get("plan_hash_owner"),
    }
    parity_pass = (
        parity["cases"] == 102 and parity["passed"] == 102 and parity["failed"] == 0
        and parity["challenge_coverage"] == 9 and parity["delivery_profile_coverage"] == 5
        and parity["mode_coverage"] == 2 and parity["personalization_profiles_covered"] == 2
        and parity["request_sha_parity"] and parity["plan_sha_parity"]
        and parity["canonical_request_parity"] and parity["production_plan_parity"]
        and parity["plan_hash_owner"] == "canonical_production_orchestrator"
        and len(matrix_cases) == 102 and matrix_case_gates
    )

    d48 = receipts.get("D4.8", {})
    governance_evidence_path = ARTIFACTS / "d4_8" / "d4_8_authorization_evidence.json"
    governance_matrix_path = ARTIFACTS / "d4_8" / "d4_8_governance_matrix.json"
    try:
        governance_evidence = load_json(governance_evidence_path)
        governance_matrix = load_json(governance_matrix_path)
    except Exception:
        governance_evidence, governance_matrix = {}, {}
    policy = load_json(ROOT / "definitions" / "c11d" / "production" / "C11D_PRODUCTION_ACTIVATION_POLICY_V1.json")
    governance = {
        "cases": governance_matrix.get("total_cases", 0),
        "passed": governance_matrix.get("passed_cases", 0),
        "failed": governance_matrix.get("failed_cases", -1),
        "renderer_policy": d48.get("renderer_policy"),
        "production_authorization": d48.get("production_authorization"),
        "renderer_called": d48.get("renderer_called"),
        "ffmpeg_production_called": d48.get("ffmpeg_production_called"),
        "godot_production_called": d48.get("godot_production_called"),
    }
    governance_pass = (
        governance["cases"] == 8 and governance["passed"] == 8 and governance["failed"] == 0
        and governance["renderer_policy"] == "DISABLED"
        and governance["production_authorization"] is False
        and governance["renderer_called"] is False
        and governance["ffmpeg_production_called"] is False
        and governance["godot_production_called"] is False
        and d48.get("runtime_authority") == "NONE"
        and policy.get("renderer_activation_policy", {}).get("state") == "DISABLED"
    )

    d42_parity = load_json(ARTIFACTS / "d4_2" / "d4_2_gui_cli_parity.json")
    d44_parity = load_json(ARTIFACTS / "d4_4" / "d4_4_gui_cli_plan_parity.json")
    d44_plan = load_json(ARTIFACTS / "d4_4" / "d4_4_example_production_plan.json")
    d45_evidence = load_json(ARTIFACTS / "d4_5" / "d4_5_cli_adapter_evidence.json")
    d45_plan = load_json(ARTIFACTS / "d4_5" / "d4_5_cli_plan.json")
    d46_plan = load_json(ARTIFACTS / "d4_6" / "d4_6_gui_plan.json")
    d46_receipt = receipts.get("D4.6", {})
    d48_provenance = governance_evidence.get("provenance", {})
    d46_payload = load_json(ARTIFACTS / "d4_6" / "fixtures" / "request_gui_production.json")
    schema = NORMALIZER.load_json(str(SCHEMA_PATH))
    canonical_d46_request = NORMALIZER.normalize_request(d46_payload, schema)
    computed_d46_request_sha = NORMALIZER.request_hash(canonical_d46_request)

    hash_checks = {
        "d42_request_sha_present_and_equal": bool(d42_parity.get("sha256_equal")) and len(d42_parity.get("sha256", "")) == 64,
        "d44_plan_sha_matches_d44": d44_parity.get("sha256_equal") is True and d44_parity.get("sha256") == ORCHESTRATOR.sha256(d44_plan),
        "d45_plan_sha_matches_d44_hash_owner": d45_plan.get("plan_id") == "c11d_production_plan" and d45_plan.get("runtime_authority") == "NONE" and d45_evidence.get("production_plan_sha256") == ORCHESTRATOR.sha256(d45_plan),
        "d46_request_sha_matches_d42": d46_receipt.get("request_sha256") == computed_d46_request_sha,
        "d46_plan_sha_matches_d44": d46_receipt.get("plan_sha256") == ORCHESTRATOR.sha256(d46_plan),
        "d47_gui_cli_request_and_plan_hash_parity": parity_pass,
        "d48_request_identity_matches_d46": d48_provenance.get("request_sha256") == d46_receipt.get("request_sha256"),
        "d48_plan_identity_matches_d46": d48_provenance.get("plan_sha256") == d46_receipt.get("plan_sha256"),
        "d48_authorization_hash_linked": governance_evidence.get("production_authorization_sha256") == d48.get("authorization_sha256"),
    }
    hash_chain_pass = all(hash_checks.values())

    runtime_hits, static_runtime_clean = runtime_scan()
    runtime_clean = (
        static_runtime_clean
        and d47.get("renderer_activation") is False
        and d47.get("production_execution") is False
        and d48.get("renderer_called") is False
        and d48.get("production_execution") is False
        and d48.get("runtime_authority") == "NONE"
    )

    checkpoints_gate = all(checkpoint_pass.values())
    regression_gate = all(item.get("pass") is True for item in regression.values())
    gates = {
        "all_checkpoints_closed": checkpoints_gate,
        "architecture_coherent": architecture_pass,
        "gui_cli_parity_102_of_102": parity_pass,
        "production_governance_8_of_8": governance_pass,
        "hash_chain_valid": hash_chain_pass,
        "frozen_c11c_preserved": frozen_hash_valid,
        "runtime_boundary_clean": runtime_clean,
        "idempotency_and_regression": regression_gate,
    }
    return {
        "checkpoints": checkpoint_pass,
        "architecture": architecture,
        "architecture_module_counts": module_counts,
        "parity": parity,
        "governance": governance,
        "hash_integrity": hash_checks,
        "frozen_c11c": {
            "expected_archive_sha256": EXPECTED_C11C_ARCHIVE_SHA256,
            "receipt_archive_sha256": stored_archive_hash,
            "audit_archive_sha256": audit_archive_hash,
            "frozen_c11c_modified": not frozen_hash_valid,
            "preserved": frozen_hash_valid,
        },
        "runtime": {
            "static_execution_patterns": runtime_hits,
            "renderer_activation": False,
            "production_execution": False,
            "runtime_authority": "NONE",
            "clean": runtime_clean,
        },
        "regression": regression,
        "all_predecessor_runners_pass": regression_gate,
        "gates": gates,
    }


def acceptance_payload(evaluation):
    gates = evaluation["gates"]
    passed = all(gates.values())
    return {
        "checkpoint": "C11-D D4.9",
        "result": "PASS" if passed else "BLOCKED",
        "status": "CLOSED" if passed else "BLOCKED",
        "d4_complete": passed,
        "checkpoints": {
            key.lower().replace(".", "_"): "PASS/CLOSED" if value else "NOT_CLOSED"
            for key, value in evaluation["checkpoints"].items()
        },
        "gates": gates,
        "all_predecessor_runners_pass": evaluation["all_predecessor_runners_pass"],
        "gui_cli_parity": gates["gui_cli_parity_102_of_102"],
        "production_governance": gates["production_governance_8_of_8"],
        "hash_integrity": gates["hash_chain_valid"],
        "frozen_c11c_preserved": gates["frozen_c11c_preserved"],
        "runtime_boundary_clean": gates["runtime_boundary_clean"],
        "idempotency": gates["idempotency_and_regression"],
        "parity_cases": evaluation["parity"],
        "governance_cases": evaluation["governance"],
        "frozen_c11c": evaluation["frozen_c11c"],
        "hash_integrity_checks": evaluation["hash_integrity"],
        "runtime": evaluation["runtime"],
        "renderer_activation": False,
        "production_execution": False,
        "runtime_authority": "NONE",
        "next": "D5 - Artifact Topology + Provenance" if passed else "D4.9 - Resolve blocked acceptance gates",
    }


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    regression = run_regressions()
    receipts, checkpoint_pass = read_checkpoint_receipts()
    evaluation_a = evaluate(receipts, checkpoint_pass, regression, all(item["pass"] for item in regression.values()))
    evaluation_b = evaluate(receipts, checkpoint_pass, regression, all(item["pass"] for item in regression.values()))
    idempotency_pass = stable_sha256(acceptance_payload(evaluation_a)) == stable_sha256(acceptance_payload(evaluation_b))
    evaluation_a["gates"]["idempotency_and_regression"] = evaluation_a["gates"]["idempotency_and_regression"] and idempotency_pass
    evaluation_a["idempotency_hash_equal"] = idempotency_pass

    matrix = acceptance_payload(evaluation_a)
    matrix["acceptance_sha256"] = stable_sha256(matrix)
    evidence = {
        "checkpoint": "C11-D D4.9",
        "result": matrix["result"],
        "status": matrix["status"],
        "acceptance_sha256": matrix["acceptance_sha256"],
        **evaluation_a,
        "idempotency_hash_equal": idempotency_pass,
    }
    receipt = {
        "checkpoint": "C11-D D4.9",
        "result": matrix["result"],
        "status": matrix["status"],
        "d4_complete": matrix["d4_complete"],
        **matrix["checkpoints"],
        "all_predecessor_runners_pass": matrix["all_predecessor_runners_pass"],
        "gui_cli_parity": matrix["gui_cli_parity"],
        "production_governance": matrix["production_governance"],
        "hash_integrity": matrix["hash_integrity"],
        "frozen_c11c_preserved": matrix["frozen_c11c_preserved"],
        "runtime_boundary_clean": matrix["runtime_boundary_clean"],
        "idempotency": matrix["idempotency"],
        "parity_cases": matrix["parity_cases"]["cases"],
        "parity_passed": matrix["parity_cases"]["passed"],
        "parity_failed": matrix["parity_cases"]["failed"],
        "governance_cases": matrix["governance_cases"]["cases"],
        "governance_passed": matrix["governance_cases"]["passed"],
        "governance_failed": matrix["governance_cases"]["failed"],
        "frozen_c11c_archive_sha256": matrix["frozen_c11c"]["receipt_archive_sha256"],
        "frozen_c11c_modified": matrix["frozen_c11c"]["frozen_c11c_modified"],
        "renderer_activation": False,
        "production_execution": False,
        "runtime_authority": "NONE",
        "acceptance_sha256": matrix["acceptance_sha256"],
        "next": matrix["next"],
    }
    for filename, value in (
        ("d4_9_acceptance_matrix.json", matrix),
        ("d4_9_regression_evidence.json", evidence),
        ("d4_9_validation_receipt.json", receipt),
    ):
        (OUTPUT_DIR / filename).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return 0 if matrix["result"] == "PASS" else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"D4.9 ACCEPTANCE ERROR: {exc}", file=sys.stderr)
        sys.exit(2)
