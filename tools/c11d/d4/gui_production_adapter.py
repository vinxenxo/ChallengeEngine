#!/usr/bin/env python3
"""Toolkit-independent data adapter for the canonical C11-D planning pipeline."""

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TOOLS = ROOT / "tools" / "c11d" / "d4"
SCHEMA_PATH = ROOT / "definitions" / "c11d" / "production" / "C11D_PRODUCTION_REQUEST_SCHEMA_V1.json"
PERSONALIZATION_REGISTRY_PATH = ROOT / "definitions" / "c11d" / "personalization" / "C11D_PERSONALIZATION_PROFILE_REGISTRY_V1.json"
RECEIPTS = {
    "D4.2": ROOT / "artifacts" / "tests" / "c11d_d4" / "d4_2" / "d4_2_validation_receipt.json",
    "D4.3": ROOT / "artifacts" / "tests" / "c11d_d4" / "d4_3" / "d4_3_validation_receipt.json",
    "D4.4": ROOT / "artifacts" / "tests" / "c11d_d4" / "d4_4" / "d4_4_validation_receipt.json",
}
FIXTURE_DIR = ROOT / "artifacts" / "tests" / "c11d_d4" / "d4_6" / "fixtures"


def import_shared_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load canonical module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Use the actual canonical components. This adapter contains no business rules.
NORMALIZER = import_shared_module(
    "c11d_d4_2_normalizer", TOOLS / "production_request_normalizer.py"
)
PERSONALIZATION = import_shared_module(
    "c11d_d4_3_personalization", TOOLS / "personalization_resolver.py"
)
ORCHESTRATOR = import_shared_module(
    "c11d_d4_4_orchestrator", TOOLS / "canonical_production_orchestrator.py"
)


def load_json(path):
    with open(path, "r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def load_pipeline_inputs():
    return (
        NORMALIZER.load_json(str(SCHEMA_PATH)),
        PERSONALIZATION.load_json(str(PERSONALIZATION_REGISTRY_PATH)),
    )


def build_gui_request(gui_payload):
    """Map GUI data to the shared request shape and stamp interface provenance."""
    if not isinstance(gui_payload, dict):
        return gui_payload
    request = copy.deepcopy(gui_payload)
    provenance = request.get("provenance")
    if isinstance(provenance, dict):
        provenance["request_origin"] = "GUI"
    return request


def normalize_request(raw_request, schema):
    """Call the D4.2 normalizer directly; validation remains owned by D4.2."""
    return NORMALIZER.normalize_request(raw_request, schema)


def resolve_personalization(canonical_request, registry):
    """Call the D4.3 registry validator and resolver directly."""
    validated_registry = PERSONALIZATION.validate_registry(registry)
    return PERSONALIZATION.normalize_personalization(
        canonical_request, validated_registry
    )


def generate_plan(gui_payload):
    """Return the canonical D4.4 plan and hashes without executing production."""
    schema, registry = load_pipeline_inputs()
    gui_request = build_gui_request(gui_payload)
    canonical_request = normalize_request(gui_request, schema)
    request_hash = NORMALIZER.request_hash(canonical_request)
    resolved_personalization = resolve_personalization(canonical_request, registry)
    orchestrator_request = copy.deepcopy(canonical_request)
    orchestrator_request["personalization"] = resolved_personalization
    plan, plan_hash = ORCHESTRATOR.build_plan(
        orchestrator_request, schema, registry
    )
    return {
        "status": "PLANNED",
        "request_hash": request_hash,
        "plan_hash": plan_hash,
        "execution": False,
        "renderer": False,
        "plan": plan,
        "canonical_request": canonical_request,
        "resolved_personalization": resolved_personalization,
    }


def self_test(evidence_path=None, plan_path=None, parity_path=None, receipt_path=None):
    for checkpoint, path in RECEIPTS.items():
        receipt = load_json(path)
        if receipt.get("result") != "PASS" or receipt.get("status") != "CLOSED":
            raise AssertionError(f"{checkpoint} receipt is not PASS/CLOSED")

    schema, registry = load_pipeline_inputs()
    review_path = FIXTURE_DIR / "request_gui_review.json"
    production_path = FIXTURE_DIR / "request_gui_production.json"
    gui_review_raw = load_json(review_path)
    gui_production_raw = load_json(production_path)

    gui_review = generate_plan(gui_review_raw)
    gui_production = generate_plan(gui_production_raw)
    if gui_review["plan"]["mode"] != "REVIEW":
        raise AssertionError("GUI REVIEW plan mode mismatch")
    if gui_production["plan"]["mode"] != "PRODUCTION":
        raise AssertionError("GUI PRODUCTION plan mode mismatch")
    if gui_review["status"] != "PLANNED" or gui_production["status"] != "PLANNED":
        raise AssertionError("GUI API status must remain PLANNED")

    # Match the GUI request in every semantic field and vary only interface origin.
    cli_equivalent_raw = copy.deepcopy(gui_production_raw)
    cli_equivalent_raw["provenance"]["request_origin"] = "CLI"
    gui_canonical = gui_production["canonical_request"]
    cli_canonical = normalize_request(cli_equivalent_raw, schema)
    gui_canonical_equal = NORMALIZER.canonical_json(gui_canonical) == NORMALIZER.canonical_json(cli_canonical)
    if not gui_canonical_equal:
        raise AssertionError("GUI and CLI canonical Production Requests differ")

    cli_resolved_personalization = resolve_personalization(cli_canonical, registry)
    cli_canonical["personalization"] = cli_resolved_personalization
    cli_plan, cli_plan_hash = ORCHESTRATOR.build_plan(cli_canonical, schema, registry)
    gui_plan_equal = gui_production["plan"] == cli_plan
    gui_cli_hash_equal = gui_production["plan_hash"] == cli_plan_hash
    if not gui_plan_equal or not gui_cli_hash_equal:
        raise AssertionError("GUI and CLI plans or plan hashes differ")

    # Verify the real D4.5 CLI adapter against the same request identity.
    with tempfile.TemporaryDirectory(prefix="c11d_d46_") as temp_dir:
        cli_request_path = Path(temp_dir) / "request_cli.json"
        cli_request_path.write_text(
            json.dumps(cli_equivalent_raw, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        cli_run = subprocess.run(
            [
                sys.executable,
                str(TOOLS / "production_cli.py"),
                "--request",
                str(cli_request_path),
                "--print-json",
            ],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if cli_run.returncode != 0:
            raise AssertionError("D4.5 CLI parity invocation failed: " + cli_run.stderr)
        actual_cli_plan = json.loads(cli_run.stdout)
    if actual_cli_plan != gui_production["plan"]:
        raise AssertionError("GUI API plan differs from actual D4.5 CLI output")

    gui_a_raw = copy.deepcopy(gui_production_raw)
    gui_b_raw = copy.deepcopy(gui_production_raw)
    gui_a_raw["personalization"]["values"]["player_name"] = "ANA"
    gui_b_raw["personalization"]["values"]["player_name"] = "LUIS"
    gui_a = generate_plan(gui_a_raw)
    gui_b = generate_plan(gui_b_raw)
    personalization_a = gui_a["resolved_personalization"]
    personalization_b = gui_b["resolved_personalization"]
    personalization_hash_a = PERSONALIZATION.digest(personalization_a)
    personalization_hash_b = PERSONALIZATION.digest(personalization_b)
    personalization_isolation = (
        gui_a["plan"]["seed"] == gui_b["plan"]["seed"]
        and gui_a["plan"]["music_seed"] == gui_b["plan"]["music_seed"]
        and personalization_hash_a != personalization_hash_b
        and gui_a["plan_hash"] != gui_b["plan_hash"]
    )
    if not personalization_isolation:
        raise AssertionError("Personalization changed seeds or failed to change plan identity")

    invalid_request = copy.deepcopy(gui_review_raw)
    invalid_request.pop("music_seed", None)
    try:
        generate_plan(invalid_request)
        invalid_request_rejected = False
    except ValueError:
        invalid_request_rejected = True

    invalid_personalization = copy.deepcopy(gui_review_raw)
    invalid_personalization["personalization"]["values"]["seed"] = 999
    try:
        generate_plan(invalid_personalization)
        invalid_personalization_rejected = False
    except ValueError:
        invalid_personalization_rejected = True

    forbidden_control = copy.deepcopy(gui_review_raw)
    forbidden_control["winning_frame"] = 500
    try:
        generate_plan(forbidden_control)
        forbidden_control_rejected = False
    except ValueError:
        forbidden_control_rejected = True

    if not all((invalid_request_rejected, invalid_personalization_rejected, forbidden_control_rejected)):
        raise AssertionError("A canonical negative validation case was accepted")

    checks = {
        "d42_d43_d44_predecessors_pass_closed": True,
        "review_pass": True,
        "production_pass": True,
        "gui_cli_canonical_request_equal": gui_canonical_equal,
        "gui_cli_plan_equal": gui_plan_equal and actual_cli_plan == gui_production["plan"],
        "gui_cli_sha256_equal": gui_cli_hash_equal,
        "personalization_isolation": personalization_isolation,
        "invalid_request_rejected_by_d42": invalid_request_rejected,
        "invalid_personalization_rejected_by_d43": invalid_personalization_rejected,
        "forbidden_simulation_control_rejected": forbidden_control_rejected,
        "renderer_activation_false": gui_production["renderer"] is False,
        "production_execution_false": gui_production["execution"] is False,
        "gui_activation_false": gui_production["plan"]["gui_activation"] is False,
        "plan_hash_owned_by_d44": gui_production["plan_hash"] == ORCHESTRATOR.sha256(gui_production["plan"]),
        "api_adds_no_plan_fields": set(gui_production["plan"]) == set(
            ORCHESTRATOR.build_plan(
                dict(gui_canonical, personalization=gui_production["resolved_personalization"]),
                schema,
                registry,
            )[0]
        ),
    }
    if not all(checks.values()):
        failures = [name for name, passed in checks.items() if not passed]
        raise AssertionError("D4.6 self-test failed: " + ", ".join(failures))

    parity = {
        "gui_cli_canonical_request_equal": gui_canonical_equal,
        "gui_cli_plan_equal": gui_plan_equal and actual_cli_plan == gui_production["plan"],
        "gui_cli_sha256_equal": gui_cli_hash_equal,
        "canonical_request_sha256": gui_production["request_hash"],
        "production_plan_sha256": gui_production["plan_hash"],
    }
    evidence = {
        "checkpoint": "C11-D D4.6",
        "result": "PASS",
        "status": "CLOSED",
        "gui_adapter": True,
        "canonical_normalizer_reused": True,
        "personalization_resolver_reused": True,
        "orchestrator_reused": True,
        "review_pass": True,
        "production_pass": True,
        "gui_cli_canonical_request_equal": gui_canonical_equal,
        "gui_cli_plan_equal": checks["gui_cli_plan_equal"],
        "gui_cli_sha256_equal": gui_cli_hash_equal,
        "personalization_isolation": personalization_isolation,
        "personalization_hash_ana": personalization_hash_a,
        "personalization_hash_luis": personalization_hash_b,
        "invalid_request_rejected": invalid_request_rejected,
        "invalid_personalization_rejected": invalid_personalization_rejected,
        "forbidden_simulation_control_rejected": forbidden_control_rejected,
        "renderer_activation": False,
        "production_execution": False,
        "gui_activation": False,
        "runtime_authority": "NONE",
        "checks": checks,
        "next": "D4.7 - GUI/CLI Parity",
    }
    receipt = dict(evidence)
    receipt["plan_sha256"] = gui_production["plan_hash"]
    receipt["request_sha256"] = gui_production["request_hash"]

    outputs = (
        (evidence_path, evidence),
        (plan_path, gui_production["plan"]),
        (parity_path, parity),
        (receipt_path, receipt),
    )
    for output_path, value in outputs:
        if output_path:
            path = Path(output_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return receipt


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--evidence")
    parser.add_argument("--plan")
    parser.add_argument("--parity")
    parser.add_argument("--receipt")
    args = parser.parse_args()
    if not args.self_test:
        parser.error("D4.6 adapter API is consumed by its host GUI; use --self-test for validation")
    try:
        self_test(args.evidence, args.plan, args.parity, args.receipt)
    except Exception as exc:
        print(f"D4.6 GUI ADAPTER ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
