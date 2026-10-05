#!/usr/bin/env python3
"""Thin command-line adapter for the canonical C11-D production planning pipeline."""

import argparse
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
D42_RECEIPT_PATH = ROOT / "artifacts" / "tests" / "c11d_d4" / "d4_2" / "d4_2_validation_receipt.json"
D43_RECEIPT_PATH = ROOT / "artifacts" / "tests" / "c11d_d4" / "d4_3" / "d4_3_validation_receipt.json"
FIXTURE_DIR = ROOT / "artifacts" / "tests" / "c11d_d4" / "d4_5" / "fixtures"


class AdapterFailure(Exception):
    def __init__(self, code, stage, message):
        super().__init__(message)
        self.code = code
        self.stage = stage


def import_shared_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load shared module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Import the actual D4.2, D4.3, and D4.4 implementations. This adapter contains
# no copies of their request, personalization, profile, or plan rules.
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
    try:
        with open(path, "r", encoding="utf-8-sig") as handle:
            return json.load(handle)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise AdapterFailure(1, "request", f"Could not load request JSON: {exc}") from exc


def load_shared_inputs():
    try:
        schema = NORMALIZER.load_json(str(SCHEMA_PATH))
        registry = PERSONALIZATION.load_json(str(PERSONALIZATION_REGISTRY_PATH))
        return schema, registry
    except Exception as exc:
        raise AdapterFailure(5, "internal", f"Could not load canonical pipeline inputs: {exc}") from exc


def verify_predecessors():
    for path, checkpoint in ((D42_RECEIPT_PATH, "D4.2"), (D43_RECEIPT_PATH, "D4.3")):
        try:
            receipt = load_json(path)
        except AdapterFailure as exc:
            raise AdapterFailure(5, "governance", f"{checkpoint} receipt unavailable: {exc}") from exc
        if receipt.get("result") != "PASS" or receipt.get("status") != "CLOSED":
            raise AdapterFailure(5, "governance", f"{checkpoint} is not PASS/CLOSED")


def process_request(raw_request, schema, registry):
    try:
        canonical_request = NORMALIZER.normalize_request(raw_request, schema)
    except ValueError as exc:
        # D4.2 is the authority for malformed or invalid Production Requests.
        raise AdapterFailure(1, "normalization", str(exc)) from exc
    except Exception as exc:
        raise AdapterFailure(2, "normalization", str(exc)) from exc

    try:
        validated_registry = PERSONALIZATION.validate_registry(registry)
        normalized_personalization = PERSONALIZATION.normalize_personalization(
            canonical_request, validated_registry
        )
        canonical_request["personalization"] = normalized_personalization
    except ValueError as exc:
        # D4.3 is the authority for personalization validation and normalization.
        raise AdapterFailure(3, "personalization", str(exc)) from exc
    except Exception as exc:
        raise AdapterFailure(3, "personalization", str(exc)) from exc

    try:
        plan, plan_sha256 = ORCHESTRATOR.build_plan(
            canonical_request, schema, registry
        )
        return canonical_request, plan, plan_sha256
    except Exception as exc:
        # D4.4 alone constructs the Production Plan and its identity.
        raise AdapterFailure(4, "orchestration", str(exc)) from exc


def write_plan(path, plan):
    try:
        ORCHESTRATOR.save_json(str(path), plan)
    except Exception as exc:
        raise AdapterFailure(5, "output", f"Could not write Production Plan: {exc}") from exc


def print_status(request, plan_sha256):
    mode = request["mode"]
    status = "VALIDATED" if mode == "REVIEW" else "PLANNED"
    print("C11-D CLI")
    print(f"REQUEST: {request['request_id']}")
    print(f"MODE: {mode}")
    print(f"STATUS: {status}")
    print(f"PLAN SHA-256: {plan_sha256}")
    print("EXECUTION: FALSE")
    print("RENDERER: FALSE")
    print("NEXT: D4.6")


def run_self_test(evidence_path, plan_path, receipt_path):
    verify_predecessors()
    schema, registry = load_shared_inputs()
    review_path = FIXTURE_DIR / "request_cli_review.json"
    production_path = FIXTURE_DIR / "request_cli_production.json"
    review_raw = load_json(review_path)
    production_raw = load_json(production_path)

    review_request, review_plan, review_hash = process_request(review_raw, schema, registry)
    production_request, production_plan, production_hash = process_request(
        production_raw, schema, registry
    )

    if review_plan.get("mode") != "REVIEW" or production_plan.get("mode") != "PRODUCTION":
        raise AssertionError("REVIEW / PRODUCTION plan mode mismatch")
    if review_plan.get("renderer_activation") is not False:
        raise AssertionError("REVIEW plan enables the renderer")
    if production_plan.get("renderer_activation") is not False:
        raise AssertionError("PRODUCTION plan enables the renderer")
    if review_plan.get("orchestrator_execution") is not False or production_plan.get("orchestrator_execution") is not False:
        raise AssertionError("A plan enables production execution")

    with tempfile.TemporaryDirectory(prefix="c11d_d45_") as temp_dir:
        temp = Path(temp_dir)
        # Exercise the installed CLI entry point itself for both modes.
        review_run = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), "--request", str(review_path), "--print-json"],
            cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8"
        )
        if review_run.returncode != 0:
            raise AssertionError("CLI REVIEW invocation failed: " + review_run.stderr)
        review_cli_plan = json.loads(review_run.stdout)

        cli_plan_path = temp / "cli_production_plan.json"
        production_run = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), "--request", str(production_path), "--output", str(cli_plan_path)],
            cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8"
        )
        if production_run.returncode != 0 or not cli_plan_path.exists():
            raise AssertionError("CLI PRODUCTION planning invocation failed: " + production_run.stderr)
        production_cli_plan = load_json(cli_plan_path)

        invalid_request = dict(review_raw)
        invalid_request.pop("music_seed", None)
        invalid_path = temp / "invalid_request.json"
        invalid_path.write_text(json.dumps(invalid_request), encoding="utf-8")
        invalid_run = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), "--request", str(invalid_path), "--print-json"],
            cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8"
        )

        invalid_personalization = json.loads(json.dumps(review_raw))
        invalid_personalization["personalization"]["values"]["seed"] = 999
        invalid_personalization_path = temp / "invalid_personalization.json"
        invalid_personalization_path.write_text(json.dumps(invalid_personalization), encoding="utf-8")
        invalid_personalization_run = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), "--request", str(invalid_personalization_path), "--print-json"],
            cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8"
        )

        forbidden_request = json.loads(json.dumps(review_raw))
        forbidden_request["winning_frame"] = 500
        forbidden_path = temp / "forbidden_request.json"
        forbidden_path.write_text(json.dumps(forbidden_request), encoding="utf-8")
        forbidden_run = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), "--request", str(forbidden_path), "--print-json"],
            cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8"
        )

        repeat_run = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), "--request", str(production_path), "--print-json"],
            cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8"
        )
        if repeat_run.returncode != 0:
            raise AssertionError("Deterministic repeat CLI invocation failed")
        repeated_plan = json.loads(repeat_run.stdout)

    checks = {
        "review_request_pass": review_plan["mode"] == "REVIEW",
        "production_request_pass": production_plan["mode"] == "PRODUCTION",
        "review_renderer_not_called": review_plan["renderer_activation"] is False,
        "production_execution_false": production_plan["orchestrator_execution"] is False,
        "invalid_request_rejected_by_d42": invalid_run.returncode == 1 and "normalization" in invalid_run.stderr.lower(),
        "invalid_personalization_rejected_by_d43": invalid_personalization_run.returncode == 3 and "personalization" in invalid_personalization_run.stderr.lower(),
        "forbidden_simulation_control_rejected": forbidden_run.returncode == 1 and "winning_frame" in forbidden_run.stderr,
        "deterministic_repeat_plan_equal": production_cli_plan == repeated_plan,
        "deterministic_repeat_sha256_equal": production_hash == ORCHESTRATOR.sha256(repeated_plan),
        "cli_plan_equals_orchestrator_plan": production_cli_plan == production_plan,
        "plan_hash_from_orchestrator": production_hash == ORCHESTRATOR.sha256(production_plan),
        "adapter_adds_no_plan_fields": set(production_cli_plan) == set(production_plan),
    }
    if not all(checks.values()):
        failures = [key for key, passed in checks.items() if not passed]
        raise AssertionError("D4.5 self-test failed: " + ", ".join(failures))

    write_plan(plan_path, production_cli_plan)
    result = {
        "checkpoint": "C11-D D4.5",
        "result": "PASS",
        "status": "CLOSED",
        "cli_adapter": True,
        "canonical_normalizer_reused": True,
        "personalization_resolver_reused": True,
        "orchestrator_reused": True,
        "review_request_pass": True,
        "production_request_pass": True,
        "deterministic_repeat_pass": True,
        "invalid_request_rejected": True,
        "invalid_request_exit_code": invalid_run.returncode,
        "invalid_personalization_rejected": True,
        "invalid_personalization_exit_code": invalid_personalization_run.returncode,
        "forbidden_simulation_controls_rejected": True,
        "forbidden_control_exit_code": forbidden_run.returncode,
        "plan_identity_owned_by": "D4.4 canonical_production_orchestrator.sha256",
        "adapter_adds_plan_fields": False,
        "review_plan_sha256": review_hash,
        "production_plan_sha256": production_hash,
        "review_plan_renderer_activation": False,
        "production_plan_renderer_activation": False,
        "production_execution": False,
        "renderer_activation": False,
        "runtime_authority": "NONE",
        "checks": checks,
        "next": "D4.6 - GUI Adapter",
    }
    for path in (evidence_path, receipt_path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


class AdapterArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise AdapterFailure(5, "arguments", message)


def main(argv=None):
    parser = AdapterArgumentParser(description=__doc__)
    parser.add_argument("--request")
    parser.add_argument("--output")
    parser.add_argument("--print-json", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--evidence")
    parser.add_argument("--plan")
    parser.add_argument("--receipt")
    args = parser.parse_args(argv)

    try:
        if args.self_test:
            if not args.evidence or not args.plan or not args.receipt:
                raise AdapterFailure(5, "arguments", "--self-test requires --evidence, --plan, and --receipt")
            run_self_test(args.evidence, args.plan, args.receipt)
            return 0

        if not args.request:
            raise AdapterFailure(5, "arguments", "--request is required")
        verify_predecessors()
        schema, registry = load_shared_inputs()
        raw_request = load_json(args.request)
        canonical_request, plan, plan_sha256 = process_request(raw_request, schema, registry)
        if args.output:
            write_plan(args.output, plan)
        if args.print_json:
            print(ORCHESTRATOR.canonical_json(plan))
        else:
            print_status(canonical_request, plan_sha256)
        return 0
    except AdapterFailure as exc:
        print(f"C11-D CLI ERROR [{exc.stage}]: {exc}", file=sys.stderr)
        return exc.code
    except Exception as exc:
        print(f"C11-D CLI ERROR [internal]: {exc}", file=sys.stderr)
        return 5


if __name__ == "__main__":
    sys.exit(main())
