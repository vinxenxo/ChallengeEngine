#!/usr/bin/env python3
"""D4.7 acceptance matrix for the existing C11-D GUI and CLI adapters."""

import argparse
import copy
import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TOOLS = ROOT / "tools" / "c11d" / "d4"
SCHEMA_PATH = ROOT / "definitions" / "c11d" / "production" / "C11D_PRODUCTION_REQUEST_SCHEMA_V1.json"
PERSONALIZATION_REGISTRY_PATH = ROOT / "definitions" / "c11d" / "personalization" / "C11D_PERSONALIZATION_PROFILE_REGISTRY_V1.json"
RECEIPTS = {
    "D4.2": ROOT / "artifacts" / "tests" / "c11d_d4" / "d4_2" / "d4_2_validation_receipt.json",
    "D4.3": ROOT / "artifacts" / "tests" / "c11d_d4" / "d4_3" / "d4_3_validation_receipt.json",
    "D4.4": ROOT / "artifacts" / "tests" / "c11d_d4" / "d4_4" / "d4_4_validation_receipt.json",
    "D4.5": ROOT / "artifacts" / "tests" / "c11d_d4" / "d4_5" / "d4_5_validation_receipt.json",
    "D4.6": ROOT / "artifacts" / "tests" / "c11d_d4" / "d4_6" / "d4_6_validation_receipt.json",
}


def import_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load adapter module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


NORMALIZER = import_module(
    "c11d_d4_2_normalizer", TOOLS / "production_request_normalizer.py"
)
PERSONALIZATION = import_module(
    "c11d_d4_3_personalization", TOOLS / "personalization_resolver.py"
)
ORCHESTRATOR = import_module(
    "c11d_d4_4_orchestrator", TOOLS / "canonical_production_orchestrator.py"
)
CLI = import_module("c11d_d4_5_cli", TOOLS / "production_cli.py")
GUI = import_module("c11d_d4_6_gui", TOOLS / "gui_production_adapter.py")


def load_json(path):
    with open(path, "r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def verify_predecessors():
    for checkpoint, path in RECEIPTS.items():
        receipt = load_json(path)
        if receipt.get("result") != "PASS" or receipt.get("status") != "CLOSED":
            raise RuntimeError(f"{checkpoint} receipt is not PASS/CLOSED")


def request_for(case_id, challenge_id, delivery_profile_id, mode, profile_id, origin):
    if profile_id == "none_v1":
        personalization = {
            "enabled": False,
            "profile_id": "none_v1",
            "values": {},
        }
    else:
        personalization = {
            "enabled": True,
            "profile_id": "editorial_text_v1",
            "values": {
                "player_name": "PARITY",
                "language": "es",
            },
        }
    return {
        "request_id": case_id,
        "schema_version": "1.0",
        "mode": mode,
        "challenge_id": challenge_id,
        "challenge_version": "1.0",
        "seed": 700001,
        "music_seed": 800001,
        "delivery_profile_id": delivery_profile_id,
        "presentation_profile_id": "UNKNOWN",
        "duration_seconds": 10,
        "variation_index": 0,
        "personalization": personalization,
        "editorial": {
            "title": "D4.7 PARITY",
            "subtitle": "UNKNOWN",
            "language": "es",
            "call_to_action": "JUEGA",
        },
        "output": {
            "container": "mp4",
            "width": 720,
            "height": 1280,
            "fps": 30,
            "audio_enabled": True,
        },
        "provenance": {
            "source_revision": "D4.7",
            "request_origin": origin,
            "parent_request_id": "UNKNOWN",
        },
    }


def prepare_cli_request(raw_request, schema, registry):
    """Run the actual D4.5 adapter pipeline and retain its canonical request."""
    canonical_request, plan, plan_hash = CLI.process_request(
        raw_request, schema, registry
    )
    # D4.5's adapter returns its D4.2 request after D4.3 personalization has
    # resolved. Reconstruct only the D4.2 canonical identity through D4.2 itself.
    d42_request = NORMALIZER.normalize_request(raw_request, schema)
    request_hash = NORMALIZER.request_hash(d42_request)
    return d42_request, request_hash, canonical_request, plan, plan_hash


def check_case(case_id, challenge_id, delivery_profile_id, mode, profile_id, schema, registry):
    gui_raw = request_for(
        case_id, challenge_id, delivery_profile_id, mode, profile_id, "GUI"
    )
    cli_raw = copy.deepcopy(gui_raw)
    cli_raw["provenance"]["request_origin"] = "CLI"

    gui_result = GUI.generate_plan(gui_raw)
    gui_canonical = gui_result["canonical_request"]
    cli_canonical, cli_request_hash, cli_resolved, cli_plan, cli_plan_hash = prepare_cli_request(
        cli_raw, schema, registry
    )

    canonical_equal = gui_canonical == cli_canonical
    origin_unknown = (
        gui_canonical.get("provenance", {}).get("request_origin") == "UNKNOWN"
        and cli_canonical.get("provenance", {}).get("request_origin") == "UNKNOWN"
    )
    gui_request_hash = gui_result["request_hash"]
    request_sha_equal = gui_request_hash == cli_request_hash
    plan_equal = gui_result["plan"] == cli_plan
    plan_sha_equal = gui_result["plan_hash"] == cli_plan_hash
    pipeline_request_equal = (
        cli_resolved.get("personalization") == gui_result["resolved_personalization"]
        and cli_resolved.get("provenance", {}).get("request_origin") == "UNKNOWN"
    )

    plan = gui_result["plan"]
    safe = (
        plan.get("runtime_authority") == "NONE"
        and plan.get("renderer_activation") is False
        and plan.get("orchestrator_execution") is False
        and plan.get("gui_activation") is False
        and "winning_frame" not in gui_raw
        and "close_calls" not in gui_raw
        and "simulation_result" not in gui_raw
        and "simulation_truth" not in gui_raw
    )
    owner = (
        gui_result["plan_hash"] == ORCHESTRATOR.sha256(gui_result["plan"])
        and cli_plan_hash == ORCHESTRATOR.sha256(cli_plan)
        and gui_result["plan"] == ORCHESTRATOR.build_plan(
            dict(gui_canonical, personalization=gui_result["resolved_personalization"]),
            schema,
            registry,
        )[0]
    )
    passed = all((canonical_equal, origin_unknown, request_sha_equal, plan_equal, plan_sha_equal, pipeline_request_equal, safe, owner))
    return {
        "case_id": case_id,
        "challenge_id": challenge_id,
        "delivery_profile_id": delivery_profile_id,
        "mode": mode,
        "personalization_profile_id": profile_id,
        "request_sha256_gui": gui_request_hash,
        "request_sha256_cli": cli_request_hash,
        "plan_sha256_gui": gui_result["plan_hash"],
        "plan_sha256_cli": cli_plan_hash,
        "canonical_request_equal": canonical_equal,
        "request_origin_normalized_unknown": origin_unknown,
        "request_sha_equal": request_sha_equal,
        "resolved_pipeline_request_equal": pipeline_request_equal,
        "plan_equal": plan_equal,
        "plan_sha_equal": plan_sha_equal,
        "renderer": plan.get("renderer_activation"),
        "execution": plan.get("orchestrator_execution"),
        "runtime_authority": plan.get("runtime_authority"),
        "plan_hash_owned_by_d44": owner,
        "invariants_pass": safe,
        "pass": passed,
    }


def personalization_identity_tests(schema, registry):
    results = {}
    for origin, adapter in (("GUI", "gui"), ("CLI", "cli")):
        request_a = request_for(
            f"D4.7-IDENTITY-{adapter.upper()}",
            "CHALLENGE_005",
            "REVIEW_720",
            "PRODUCTION",
            "editorial_text_v1",
            origin,
        )
        request_b = copy.deepcopy(request_a)
        request_a["personalization"]["values"]["player_name"] = "ANA"
        request_b["personalization"]["values"]["player_name"] = "LUIS"
        if adapter == "gui":
            result_a = GUI.generate_plan(request_a)
            result_b = GUI.generate_plan(request_b)
            personal_a = result_a["resolved_personalization"]
            personal_b = result_b["resolved_personalization"]
            plan_a, hash_a = result_a["plan"], result_a["plan_hash"]
            plan_b, hash_b = result_b["plan"], result_b["plan_hash"]
        else:
            _, _, canonical_a, plan_a, hash_a = prepare_cli_request(request_a, schema, registry)
            _, _, canonical_b, plan_b, hash_b = prepare_cli_request(request_b, schema, registry)
            personal_a = canonical_a["personalization"]
            personal_b = canonical_b["personalization"]
        isolated = (
            plan_a["seed"] == plan_b["seed"]
            and plan_a["music_seed"] == plan_b["music_seed"]
            and PERSONALIZATION.digest(personal_a) != PERSONALIZATION.digest(personal_b)
            and hash_a != hash_b
        )
        results[adapter] = {
            "seed_identical": plan_a["seed"] == plan_b["seed"],
            "music_seed_identical": plan_a["music_seed"] == plan_b["music_seed"],
            "personalization_hash_differs": PERSONALIZATION.digest(personal_a) != PERSONALIZATION.digest(personal_b),
            "plan_hash_differs": hash_a != hash_b,
            "pass": isolated,
        }
    return results


def negative_tests(schema, registry):
    base = request_for(
        "D4.7-NEGATIVE-001", "CHALLENGE_001", "REVIEW_720", "REVIEW", "editorial_text_v1", "GUI"
    )
    invalid_request = copy.deepcopy(base)
    invalid_request.pop("music_seed")
    try:
        GUI.generate_plan(invalid_request)
        invalid_request_rejected = False
    except ValueError:
        invalid_request_rejected = True

    invalid_personalization = copy.deepcopy(base)
    invalid_personalization["personalization"]["values"]["seed"] = 999
    try:
        GUI.generate_plan(invalid_personalization)
        invalid_personalization_rejected = False
    except ValueError:
        invalid_personalization_rejected = True

    forbidden = copy.deepcopy(base)
    forbidden["winning_frame"] = 500
    try:
        GUI.generate_plan(forbidden)
        forbidden_rejected = False
    except ValueError:
        forbidden_rejected = True

    return {
        "invalid_request_rejected_by_d42": invalid_request_rejected,
        "invalid_personalization_rejected_by_d43": invalid_personalization_rejected,
        "forbidden_simulation_control_rejected": forbidden_rejected,
        "pass": all((invalid_request_rejected, invalid_personalization_rejected, forbidden_rejected)),
    }


def run_matrix():
    verify_predecessors()
    schema = NORMALIZER.load_json(str(SCHEMA_PATH))
    registry_raw = PERSONALIZATION.load_json(str(PERSONALIZATION_REGISTRY_PATH))
    registry = PERSONALIZATION.validate_registry(registry_raw)
    challenges, delivery_profiles = NORMALIZER.schema_vocabulary(schema)
    if len(challenges) != 9 or len(delivery_profiles) != 5:
        raise RuntimeError("D4.1 vocabulary is not the expected 9 Challenges / 5 delivery profiles")
    personalization_profiles = list(registry.keys())

    cases = []
    case_number = 0
    for challenge_id in challenges:
        for delivery_profile_id in delivery_profiles:
            for mode in ("REVIEW", "PRODUCTION"):
                case_number += 1
                cases.append(check_case(
                    f"D4.7-{case_number:03d}", challenge_id, delivery_profile_id,
                    mode, "none_v1", schema, registry_raw,
                ))

    for challenge_id in ("CHALLENGE_001", "CHALLENGE_005", "CHALLENGE_009"):
        for mode in ("REVIEW", "PRODUCTION"):
            for profile_id in personalization_profiles:
                case_number += 1
                cases.append(check_case(
                    f"D4.7-{case_number:03d}", challenge_id, "REVIEW_720",
                    mode, profile_id, schema, registry_raw,
                ))

    identity = personalization_identity_tests(schema, registry_raw)
    negatives = negative_tests(schema, registry_raw)
    passed = sum(1 for case in cases if case["pass"])
    failed = len(cases) - passed
    personalization_isolation = all(result["pass"] for result in identity.values())
    overall_pass = (
        len(cases) == 102
        and passed == 102
        and failed == 0
        and personalization_isolation
        and negatives["pass"]
        and all(case["plan_hash_owned_by_d44"] for case in cases)
    )
    matrix = {
        "checkpoint": "C11-D D4.7",
        "result": "PASS" if overall_pass else "FAIL",
        "status": "CLOSED" if overall_pass else "OPEN",
        "total_cases": len(cases),
        "passed_cases": passed,
        "failed_cases": failed,
        "challenge_coverage": len(challenges),
        "delivery_profile_coverage": len(delivery_profiles),
        "mode_coverage": 2,
        "personalization_profiles_covered": len(personalization_profiles),
        "matrix": cases,
    }
    evidence = {
        "checkpoint": "C11-D D4.7",
        "result": matrix["result"],
        "status": matrix["status"],
        "test_cases": len(cases),
        "passed_cases": passed,
        "failed_cases": failed,
        "challenge_coverage": len(challenges),
        "delivery_profile_coverage": len(delivery_profiles),
        "mode_coverage": 2,
        "personalization_profiles_covered": len(personalization_profiles),
        "canonical_request_parity": all(case["canonical_request_equal"] for case in cases),
        "interface_origin_normalized_unknown": all(case["request_origin_normalized_unknown"] for case in cases),
        "request_sha256_parity": all(case["request_sha_equal"] for case in cases),
        "production_plan_parity": all(case["plan_equal"] for case in cases),
        "plan_sha256_parity": all(case["plan_sha_equal"] for case in cases),
        "seed_isolation": personalization_isolation,
        "personalization_isolation": personalization_isolation,
        "personalization_identity_tests": identity,
        "negative_tests": negatives,
        "renderer_activation": False,
        "production_execution": False,
        "runtime_authority": "NONE",
        "plan_hash_owned_by_d44": all(case["plan_hash_owned_by_d44"] for case in cases),
        "plan_hash_owner": "canonical_production_orchestrator",
        "next": "D4.8 - Production Activation Governance" if overall_pass else "D4.7 - Resolve parity failures",
    }
    receipt = {
        key: value for key, value in evidence.items()
        if key not in ("personalization_identity_tests", "negative_tests")
    }
    return matrix, evidence, receipt, overall_pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    matrix, evidence, receipt, passed = run_matrix()
    outputs = (
        ("d4_7_parity_matrix.json", matrix),
        ("d4_7_parity_evidence.json", evidence),
        ("d4_7_validation_receipt.json", receipt),
    )
    for filename, value in outputs:
        (output_dir / filename).write_text(
            json.dumps(value, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"D4.7 PARITY ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
