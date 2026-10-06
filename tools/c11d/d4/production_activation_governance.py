#!/usr/bin/env python3
"""Plan authorization policy evaluation for C11-D D4.8; never executes production."""

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TOOLS = ROOT / "tools" / "c11d" / "d4"
SCHEMA_PATH = ROOT / "definitions" / "c11d" / "production" / "C11D_PRODUCTION_REQUEST_SCHEMA_V1.json"
POLICY_PATH = ROOT / "definitions" / "c11d" / "production" / "C11D_PRODUCTION_ACTIVATION_POLICY_V1.json"
PERSONALIZATION_REGISTRY_PATH = ROOT / "definitions" / "c11d" / "personalization" / "C11D_PERSONALIZATION_PROFILE_REGISTRY_V1.json"
PREDECESSOR_PATHS = {
    "D4.2": ROOT / "artifacts" / "tests" / "c11d_d4" / "d4_2" / "d4_2_validation_receipt.json",
    "D4.3": ROOT / "artifacts" / "tests" / "c11d_d4" / "d4_3" / "d4_3_validation_receipt.json",
    "D4.4": ROOT / "artifacts" / "tests" / "c11d_d4" / "d4_4" / "d4_4_validation_receipt.json",
    "D4.5": ROOT / "artifacts" / "tests" / "c11d_d4" / "d4_5" / "d4_5_validation_receipt.json",
    "D4.6": ROOT / "artifacts" / "tests" / "c11d_d4" / "d4_6" / "d4_6_validation_receipt.json",
    "D4.7": ROOT / "artifacts" / "tests" / "c11d_d4" / "d4_7" / "d4_7_validation_receipt.json",
}
STATE_NAMES = {
    "DRAFT", "NORMALIZED", "PLANNED", "VALIDATED", "AUTHORIZED",
    "EXECUTING", "COMPLETED", "FAILED", "BLOCKED"
}
RESERVED_STATES = {"EXECUTING", "COMPLETED", "FAILED"}


def import_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load canonical component: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


NORMALIZER = import_module("c11d_d4_2_normalizer", TOOLS / "production_request_normalizer.py")
PERSONALIZATION = import_module("c11d_d4_3_personalization", TOOLS / "personalization_resolver.py")
ORCHESTRATOR = import_module("c11d_d4_4_orchestrator", TOOLS / "canonical_production_orchestrator.py")


def load_json(path):
    with open(path, "r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def canonical_sha256(value):
    encoded = json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def plan_steps(plan):
    return {step.get("step_id"): step for step in plan.get("steps", []) if isinstance(step, dict)}


def authorize_production(
    plan,
    policy,
    canonical_request,
    request_sha256,
    plan_sha256,
    predecessor_receipts,
    schema,
    personalization_registry,
):
    """Evaluate authorization gates and emit a deterministic decision only."""
    reasons = []
    checks = {}

    def fail(code):
        if code not in reasons:
            reasons.append(code)

    policy_version = str(policy.get("version", "UNKNOWN"))
    renderer_state = policy.get("renderer_activation_policy", {}).get("state", "DISABLED")

    predecessor_results = {}
    for checkpoint in policy.get("required_predecessors", []):
        receipt = predecessor_receipts.get(checkpoint, {})
        closed = receipt.get("result") == "PASS" and receipt.get("status") == "CLOSED"
        predecessor_results[checkpoint] = closed
        if not closed:
            fail("PREDECESSOR_NOT_CLOSED")
    checks["predecessors_closed"] = all(predecessor_results.values()) and bool(predecessor_results)

    actual_plan_sha256 = ORCHESTRATOR.sha256(plan)
    checks["plan_hash_matches_d44"] = actual_plan_sha256 == plan_sha256
    if not checks["plan_hash_matches_d44"]:
        fail("PLAN_HASH_MISMATCH")

    actual_request_sha256 = NORMALIZER.request_hash(canonical_request)
    checks["request_hash_matches_d42"] = actual_request_sha256 == request_sha256
    if not checks["request_hash_matches_d42"]:
        fail("REQUEST_HASH_MISMATCH")

    try:
        recanonical = NORMALIZER.normalize_request(canonical_request, schema)
        checks["request_is_canonical"] = recanonical == canonical_request
    except Exception:
        checks["request_is_canonical"] = False
    if not checks["request_is_canonical"]:
        fail("REQUEST_NOT_CANONICAL")

    seed = plan.get("seed")
    music_seed = plan.get("music_seed")
    checks["seed_present"] = isinstance(seed, int) and not isinstance(seed, bool)
    checks["music_seed_present"] = isinstance(music_seed, int) and not isinstance(music_seed, bool)
    if not checks["seed_present"]:
        fail("SEED_MISSING")
    if not checks["music_seed_present"]:
        fail("MUSIC_SEED_MISSING")
    checks["seeds_distinct"] = checks["seed_present"] and checks["music_seed_present"] and seed != music_seed
    if checks["seed_present"] and checks["music_seed_present"] and seed == music_seed:
        fail("SEED_COLLISION")

    steps = plan_steps(plan)
    music_step = steps.get("music_request", {})
    checks["music_seed_isolated"] = (
        plan.get("gameplay_rng_consumption") is False
        and plan.get("structural_rng_consumption") is False
        and music_step.get("gameplay_rng_consumption") is False
        and music_step.get("music_seed") == music_seed
    )
    if not checks["music_seed_isolated"]:
        fail("MUSIC_SEED_NOT_ISOLATED")

    profile_map = PERSONALIZATION.validate_registry(personalization_registry)
    plan_personalization = plan.get("personalization", {})
    profile_id = plan_personalization.get("profile_id") if isinstance(plan_personalization, dict) else None
    profile = profile_map.get(profile_id)
    checks["personalization_profile_registered"] = profile is not None and profile.get("status") == "ACTIVE"
    checks["personalization_profile_version_matches"] = (
        profile is not None
        and plan_personalization.get("profile_version") == profile.get("profile_version")
    )
    if not checks["personalization_profile_registered"]:
        fail("PERSONALIZATION_PROFILE_UNREGISTERED")
    if not checks["personalization_profile_version_matches"]:
        fail("PERSONALIZATION_PROFILE_VERSION_MISMATCH")
    try:
        resolved_personalization = PERSONALIZATION.normalize_personalization(
            canonical_request, profile_map
        )
        checks["personalization_from_d43"] = resolved_personalization == plan_personalization
    except Exception:
        checks["personalization_from_d43"] = False
    if not checks["personalization_from_d43"]:
        fail("PERSONALIZATION_PROVENANCE_MISMATCH")

    challenge_ids, delivery_profile_ids = NORMALIZER.schema_vocabulary(schema)
    checks["challenge_registered"] = plan.get("challenge_id") in challenge_ids
    if not checks["challenge_registered"]:
        fail("CHALLENGE_UNKNOWN")
    delivery_profile_id = plan.get("delivery_profile_id")
    mode = plan.get("mode")
    delivery_unknown_allowed = (
        policy.get("review", {}).get("unknown_delivery_profile_allowed", True)
        if mode == "REVIEW"
        else policy.get("production", {}).get("unknown_delivery_profile_allowed", False)
    )
    checks["delivery_profile_registered"] = (
        delivery_profile_id in delivery_profile_ids
        or (delivery_profile_id == "UNKNOWN" and delivery_unknown_allowed)
    )
    if not checks["delivery_profile_registered"]:
        fail("DELIVERY_PROFILE_UNKNOWN")

    source_revision = canonical_request.get("provenance", {}).get("source_revision")
    plan_rebuild_matches = False
    try:
        resolved_request = dict(canonical_request)
        resolved_request["personalization"] = resolved_personalization
        rebuilt_plan, rebuilt_hash = ORCHESTRATOR.build_plan(
            resolved_request, schema, personalization_registry
        )
        plan_rebuild_matches = rebuilt_plan == plan and rebuilt_hash == plan_sha256
    except Exception:
        plan_rebuild_matches = False
    checks["request_plan_binding"] = plan_rebuild_matches
    if not plan_rebuild_matches:
        fail("REQUEST_PLAN_BINDING_MISMATCH")

    checks["provenance_complete"] = (
        isinstance(source_revision, str)
        and bool(source_revision.strip())
        and source_revision != "UNKNOWN"
        and bool(request_sha256)
        and bool(plan_sha256)
        and plan.get("request_id") == canonical_request.get("request_id")
        and plan.get("schema_version") == canonical_request.get("schema_version")
        and bool(plan_personalization.get("profile_version"))
        and bool(music_step.get("authority"))
    )
    if not checks["provenance_complete"]:
        fail("PROVENANCE_INCOMPLETE")

    checks["runtime_boundary_intact"] = (
        plan.get("runtime_authority") == "NONE"
        and plan.get("renderer_activation") is False
        and plan.get("orchestrator_execution") is False
        and plan.get("simulation_truth_mutation") is False
        and plan.get("winning_frame_mutation") is False
        and plan.get("close_calls_mutation") is False
    )
    if not checks["runtime_boundary_intact"]:
        fail("RUNTIME_BOUNDARY_VIOLATION")

    validated = not reasons
    mode_reasons = []
    authorized = False
    decision = "BLOCKED"
    state = "BLOCKED"
    if validated:
        state = "VALIDATED"
        if mode == "REVIEW":
            mode_reasons.append("REVIEW_MODE")
        elif mode != "PRODUCTION":
            mode_reasons.append("MODE_NOT_AUTHORIZABLE")
        elif renderer_state != "APPROVED":
            mode_reasons.append("RENDERER_POLICY_DISABLED" if renderer_state == "DISABLED" else "RENDERER_NOT_APPROVED")
        elif not checks["predecessors_closed"]:
            mode_reasons.append("PREDECESSOR_NOT_CLOSED")
        else:
            authorized = True
            decision = "AUTHORIZED"
            state = "AUTHORIZED"
    for reason in mode_reasons:
        fail(reason)
    if not authorized:
        decision = "BLOCKED"
        state = "BLOCKED" if not validated else "VALIDATED"

    steps = plan_steps(plan)
    provenance = {
        "source_revision": source_revision if isinstance(source_revision, str) else "UNKNOWN",
        "request_sha256": actual_request_sha256,
        "plan_sha256": actual_plan_sha256,
        "schema_version": plan.get("schema_version", "UNKNOWN"),
        "personalization_profile_id": profile_id or "UNKNOWN",
        "personalization_profile_version": plan_personalization.get("profile_version", "UNKNOWN"),
        "engine_authority": steps.get("music_request", {}).get("authority", "UNKNOWN"),
    }
    result = {
        "authorized": authorized,
        "decision": decision,
        "state": state,
        "validated": validated,
        "reasons": reasons,
        "policy_version": policy_version,
        "checks": checks,
        "predecessors": predecessor_results,
        "provenance": provenance,
        "renderer_policy": renderer_state,
        "renderer_called": False,
        "production_execution": False,
        "ffmpeg_production_called": False,
        "godot_production_called": False,
        "runtime_authority": "NONE",
        "plan_hash_owner": "canonical_production_orchestrator",
    }
    result["authorization_sha256"] = canonical_sha256(result)
    return result


def default_inputs():
    schema = NORMALIZER.load_json(str(SCHEMA_PATH))
    policy = load_json(POLICY_PATH)
    registry = PERSONALIZATION.load_json(str(PERSONALIZATION_REGISTRY_PATH))
    receipts = {key: load_json(path) for key, path in PREDECESSOR_PATHS.items()}
    return schema, policy, registry, receipts


def build_valid_candidate(mode="PRODUCTION"):
    gui_result = import_module("c11d_d4_6_gui", TOOLS / "gui_production_adapter.py")
    payload = load_json(ROOT / "artifacts" / "tests" / "c11d_d4" / "d4_6" / "fixtures" / ("request_gui_review.json" if mode == "REVIEW" else "request_gui_production.json"))
    output = gui_result.generate_plan(payload)
    canonical_request = output["canonical_request"]
    resolved_request = dict(canonical_request, personalization=output["resolved_personalization"])
    return canonical_request, resolved_request, output["plan"], output["request_hash"], output["plan_hash"]


def self_test():
    schema, policy, registry, predecessors = default_inputs()
    if policy.get("policy_id") != "c11d_production_activation" or policy.get("version") != "1.0":
        raise AssertionError("Activation policy identity/version invalid")
    states = policy.get("states", {})
    if set(states.get("defined", [])) != STATE_NAMES:
        raise AssertionError("Formal state set is incomplete")
    if not RESERVED_STATES.issubset(set(states.get("reserved_for_later_phases", []))):
        raise AssertionError("Execution states are not reserved")
    if policy.get("renderer_activation_policy", {}).get("state") != "DISABLED":
        raise AssertionError("D4.8 renderer policy must remain DISABLED")

    canonical_request, resolved_request, valid_plan, request_hash, plan_hash = build_valid_candidate("PRODUCTION")
    production = authorize_production(valid_plan, policy, canonical_request, request_hash, plan_hash, predecessors, schema, registry)
    review_request, review_resolved, review_plan, review_request_hash, review_plan_hash = build_valid_candidate("REVIEW")
    review = authorize_production(review_plan, policy, review_request, review_request_hash, review_plan_hash, predecessors, schema, registry)

    open_predecessors = dict(predecessors)
    open_predecessors["D4.7"] = {"result": "OPEN", "status": "OPEN"}
    predecessor_block = authorize_production(valid_plan, policy, canonical_request, request_hash, plan_hash, open_predecessors, schema, registry)

    tampered_plan = dict(valid_plan)
    tampered_plan["duration_seconds"] = float(tampered_plan["duration_seconds"]) + 1.0
    plan_tamper = authorize_production(tampered_plan, policy, canonical_request, request_hash, plan_hash, predecessors, schema, registry)

    tampered_seed_plan = dict(valid_plan)
    tampered_seed_plan["music_seed"] = int(tampered_seed_plan["music_seed"]) + 1
    seed_tamper = authorize_production(tampered_seed_plan, policy, canonical_request, request_hash, plan_hash, predecessors, schema, registry)

    tampered_personalization_plan = json.loads(json.dumps(valid_plan))
    tampered_personalization_plan["personalization"]["values"]["player_name"] = "ALTERED"
    personalization_tamper = authorize_production(tampered_personalization_plan, policy, canonical_request, request_hash, plan_hash, predecessors, schema, registry)

    collision_request = json.loads(json.dumps(canonical_request))
    collision_request["seed"] = collision_request["music_seed"]
    collision_resolved = dict(collision_request, personalization=PERSONALIZATION.normalize_personalization(collision_request, PERSONALIZATION.validate_registry(registry)))
    collision_plan, collision_plan_hash = ORCHESTRATOR.build_plan(collision_resolved, schema, registry)
    collision_request_hash = NORMALIZER.request_hash(collision_request)
    collision = authorize_production(collision_plan, policy, collision_request, collision_request_hash, collision_plan_hash, predecessors, schema, registry)

    tampered_request = json.loads(json.dumps(canonical_request))
    tampered_request["duration_seconds"] = float(tampered_request["duration_seconds"]) + 2.0
    request_tamper = authorize_production(valid_plan, policy, tampered_request, request_hash, plan_hash, predecessors, schema, registry)

    production_repeat = authorize_production(valid_plan, policy, canonical_request, request_hash, plan_hash, predecessors, schema, registry)
    idempotency = production == production_repeat and production["authorization_sha256"] == production_repeat["authorization_sha256"]

    cases = [
        {"case_id": "D4.8-001", "case": "valid_production_renderer_disabled", "validated": production["validated"], "authorized": production["authorized"], "expected_reason": "RENDERER_POLICY_DISABLED", "pass": production["validated"] and not production["authorized"] and "RENDERER_POLICY_DISABLED" in production["reasons"]},
        {"case_id": "D4.8-002", "case": "valid_review_never_authorized", "validated": review["validated"], "authorized": review["authorized"], "expected_reason": "REVIEW_MODE", "pass": review["validated"] and not review["authorized"] and "REVIEW_MODE" in review["reasons"]},
        {"case_id": "D4.8-003", "case": "predecessor_open", "validated": predecessor_block["validated"], "authorized": predecessor_block["authorized"], "expected_reason": "PREDECESSOR_NOT_CLOSED", "pass": not predecessor_block["authorized"] and "PREDECESSOR_NOT_CLOSED" in predecessor_block["reasons"]},
        {"case_id": "D4.8-004", "case": "tampered_duration", "validated": plan_tamper["validated"], "authorized": plan_tamper["authorized"], "expected_reason": "PLAN_HASH_MISMATCH", "pass": not plan_tamper["authorized"] and "PLAN_HASH_MISMATCH" in plan_tamper["reasons"]},
        {"case_id": "D4.8-005", "case": "tampered_music_seed", "validated": seed_tamper["validated"], "authorized": seed_tamper["authorized"], "expected_reason": "PLAN_HASH_MISMATCH", "pass": not seed_tamper["authorized"] and "PLAN_HASH_MISMATCH" in seed_tamper["reasons"]},
        {"case_id": "D4.8-006", "case": "seed_collision", "validated": collision["validated"], "authorized": collision["authorized"], "expected_reason": "SEED_COLLISION", "pass": "SEED_COLLISION" in collision["reasons"] and not collision["authorized"]},
        {"case_id": "D4.8-007", "case": "tampered_personalization", "validated": personalization_tamper["validated"], "authorized": personalization_tamper["authorized"], "expected_reason": "PLAN_HASH_MISMATCH", "pass": not personalization_tamper["authorized"] and "PLAN_HASH_MISMATCH" in personalization_tamper["reasons"] and "PERSONALIZATION_PROVENANCE_MISMATCH" in personalization_tamper["reasons"]},
        {"case_id": "D4.8-008", "case": "tampered_request_hash", "validated": request_tamper["validated"], "authorized": request_tamper["authorized"], "expected_reason": "REQUEST_HASH_MISMATCH", "pass": not request_tamper["authorized"] and "REQUEST_HASH_MISMATCH" in request_tamper["reasons"]},
    ]
    if not all(case["pass"] for case in cases):
        raise AssertionError("D4.8 governance case failed: " + ", ".join(case["case_id"] for case in cases if not case["pass"]))
    if not idempotency:
        raise AssertionError("D4.8 authorization decision is not idempotent")

    checks = {
        "predecessors_closed": production["checks"]["predecessors_closed"],
        "review_policy_test": cases[1]["pass"],
        "production_policy_test": cases[0]["pass"],
        "plan_integrity_check": production["checks"]["plan_hash_matches_d44"],
        "request_integrity_check": production["checks"]["request_hash_matches_d42"] and production["checks"]["request_plan_binding"],
        "seed_isolation_check": production["checks"]["music_seed_isolated"] and cases[5]["pass"],
        "personalization_integrity_check": production["checks"]["personalization_from_d43"] and cases[6]["pass"],
        "delivery_profile_check": production["checks"]["delivery_profile_registered"],
        "provenance_check": production["checks"]["provenance_complete"],
        "tampered_plan_rejected": cases[3]["pass"],
        "tampered_seed_rejected": cases[4]["pass"] and cases[5]["pass"],
        "tampered_personalization_rejected": cases[6]["pass"],
        "idempotency": idempotency,
    }
    if not all(checks.values()):
        raise AssertionError("D4.8 check failed: " + ", ".join(key for key, value in checks.items() if not value))

    evidence = {
        "checkpoint": "C11-D D4.8",
        "result": "PASS",
        "status": "CLOSED",
        "policy_id": "c11d_production_activation",
        "policy_version": policy["version"],
        "renderer_policy": policy["renderer_activation_policy"]["state"],
        "authorization_cases": cases,
        "checks": checks,
        "production_blocked_reasons": production["reasons"],
        "review_blocked_reasons": review["reasons"],
        "production_authorization_sha256": production["authorization_sha256"],
        "production_plan_sha256": production["provenance"]["plan_sha256"],
        "production_request_sha256": production["provenance"]["request_sha256"],
        "provenance": production["provenance"],
        "renderer_called": False,
        "production_execution": False,
        "ffmpeg_production_called": False,
        "godot_production_called": False,
        "runtime_authority": "NONE",
        "plan_hash_owner": "canonical_production_orchestrator",
        "next": "D4.9 - Full D4 Acceptance",
    }
    receipt = {
        "checkpoint": evidence["checkpoint"],
        "result": evidence["result"],
        "status": evidence["status"],
        "predecessors_closed": checks["predecessors_closed"],
        "review_policy_test": checks["review_policy_test"],
        "production_policy_test": checks["production_policy_test"],
        "renderer_policy": evidence["renderer_policy"],
        "production_authorization": False,
        "plan_integrity_check": checks["plan_integrity_check"],
        "request_integrity_check": checks["request_integrity_check"],
        "seed_isolation_check": checks["seed_isolation_check"],
        "personalization_integrity_check": checks["personalization_integrity_check"],
        "delivery_profile_check": checks["delivery_profile_check"],
        "provenance_check": checks["provenance_check"],
        "tampered_plan_rejected": checks["tampered_plan_rejected"],
        "tampered_seed_rejected": checks["tampered_seed_rejected"],
        "tampered_personalization_rejected": checks["tampered_personalization_rejected"],
        "idempotency": checks["idempotency"],
        "production_blocked_reason": "RENDERER_POLICY_DISABLED",
        "review_blocked_reason": "REVIEW_MODE",
        "authorization_sha256": production["authorization_sha256"],
        "renderer_called": False,
        "production_execution": False,
        "ffmpeg_production_called": False,
        "godot_production_called": False,
        "runtime_authority": "NONE",
        "plan_hash_owned_by_d44": True,
        "next": "D4.9 - Full D4 Acceptance",
    }
    return {"evidence": evidence, "receipt": receipt, "matrix": {"checkpoint": "C11-D D4.8", "result": "PASS", "status": "CLOSED", "total_cases": len(cases), "passed_cases": len(cases), "failed_cases": 0, "cases": cases}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    result = self_test()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    for filename, key in (
        ("d4_8_governance_matrix.json", "matrix"),
        ("d4_8_authorization_evidence.json", "evidence"),
        ("d4_8_validation_receipt.json", "receipt"),
    ):
        (output_dir / filename).write_text(
            json.dumps(result[key], ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(result["receipt"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"D4.8 GOVERNANCE ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
