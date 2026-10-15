from __future__ import annotations

"""Read-only explicit-seed and numeric-collision rejection audit."""
from copy import deepcopy
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[3]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import d_renderer_dynamic_request_payload_binding as binder  # noqa: E402
import d_renderer_candidate_seed_domain_audit as cross_audit  # noqa: E402

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_SEED_DOMAIN_COLLISION_AUDIT_V1.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_SEED_DOMAIN_COLLISION_AUDIT_SCHEMA_V1.json")
EXPECTED_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
EXPECTED_CONTRACT_SHA256 = "d68c9e342c6c6937f05737d5299dda0310b6b72157d009eb6706c527232e49c8"
EXPECTED_SCHEMA_SHA256 = "83fa12afb4809d5a1b8c7f1a97c637bd9f81a0f05643bc5daf5c805e1f4ddae4"
CONTRACT_ID = "C11-D-RENDERER-SEED-DOMAIN-COLLISION-AUDIT-V1"
SCHEMA_ID = "urn:c11d:renderer-seed-domain-collision-audit:v1"
STATUS = "PREPARATION_ONLY_EXPLICIT_SEED_AND_NUMERIC_COLLISION_AUDIT_NOT_INPUT_ADMISSION"
COLLISION_VALUES = (12345, 840001)
NEGATIVE_CASES = (
    "missing_gameplay_seed", "null_gameplay_seed", "string_gameplay_seed",
    "boolean_gameplay_seed", "zero_gameplay_seed", "out_of_range_gameplay_seed",
    "missing_music_seed", "null_music_seed", "automatic_seed_mode", "master_seed_alias",
)
PIN_ROLES = dict(cross_audit.PIN_ROLES)
PIN_ROLES.update({
    "definitions/c11d/production/D_RENDERER_CANDIDATE_SEED_DOMAIN_AUDIT_V1.json": "ACCEPTED_CROSS_TYPE_SEED_AUDIT_CONTRACT",
    "definitions/c11d/production/D_RENDERER_CANDIDATE_SEED_DOMAIN_AUDIT_SCHEMA_V1.json": "ACCEPTED_CROSS_TYPE_SEED_AUDIT_SCHEMA",
    "tools/c11d/d9/d_renderer_candidate_seed_domain_audit.py": "ACCEPTED_CROSS_TYPE_SEED_AUDIT_RUNNER",
    "tools/c11d/d9/test_d_renderer_candidate_seed_domain_audit.py": "ACCEPTED_CROSS_TYPE_SEED_AUDIT_TEST",
    "tools/c11d/d9/d_render_adapter.py": "CANONICAL_D9_10_SEED_DOMAIN_ISOLATION_GUARD",
})
PINNED_PATHS = tuple(sorted(PIN_ROLES))
GOVERNANCE_BOUNDARY = {
    "runtime": "PYTHON_PREFLIGHT_REJECTION_ONLY_NO_GODOT_INVOCATION",
    "request_input_persisted": False,
    "payload_files_written": False,
    "receipt_files_written": False,
    "renderer_input_emitted": False,
    "renderer_dispatch_invoked": False,
    "renderer_activation": False,
    "production_execution": False,
    "media_created": False,
    "output_artifact_path": None,
    "c11c_source_mutation": False,
    "d4_8": "BLOCKED",
    "release_authority": "NONE",
}


class SeedCollisionAuditError(RuntimeError):
    """An implicit seed/collision was accepted or pinned evidence drifted."""


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sha_json(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SeedCollisionAuditError(f"Cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SeedCollisionAuditError(f"Expected JSON object at {path}")
    return value


def _root(project_root: Path | str | None = None) -> Path:
    return Path(project_root).resolve() if project_root is not None else ROOT


def _validate_seed_policy(policy: Mapping[str, Any]) -> None:
    if policy.get("required_fields") != ["seed", "music_seed"] or policy.get("runtime_seed_derivation_enabled") is not False or policy.get("automatic_seed_generation") is not False or policy.get("master_seed_adopted") is not False or policy.get("equal_numeric_values_across_domains") != "REJECTED_FAIL_CLOSED":
        raise SeedCollisionAuditError("Seed-domain policy was weakened or changed")


def _load_and_validate_contract(root: Path) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, str]]]:
    contract_path, schema_path = root / CONTRACT_REL, root / SCHEMA_REL
    if not contract_path.is_file() or _sha_file(contract_path) != EXPECTED_CONTRACT_SHA256:
        raise SeedCollisionAuditError("Seed collision audit contract missing or SHA-256 mismatch")
    if not schema_path.is_file() or _sha_file(schema_path) != EXPECTED_SCHEMA_SHA256:
        raise SeedCollisionAuditError("Seed collision report schema missing or SHA-256 mismatch")
    contract, schema = _read_json(contract_path), _read_json(schema_path)
    if contract.get("schema") != CONTRACT_ID or contract.get("schema_version") != "1.0":
        raise SeedCollisionAuditError("Seed collision contract identity/version mismatch")
    if contract.get("status") != "READ_ONLY_EXPLICIT_SEED_AND_COLLISION_REJECTION_AUDIT_NOT_INPUT_ADMISSION":
        raise SeedCollisionAuditError("Seed collision contract is not read-only")
    if contract.get("source_of_truth", {}).get("frozen_c11c_manifest_sha256") != EXPECTED_MANIFEST_SHA256:
        raise SeedCollisionAuditError("Frozen C11-C reference mismatch")
    expected_experiment = {
        "content_types": list(cross_audit.CONTENT_TYPES),
        "selectors": cross_audit.EXPECTED_SELECTOR_SCOPE,
        "collision_values_tested": list(COLLISION_VALUES),
        "explicit_seed_fields_required": ["seed", "music_seed"],
        "runtime_seed_derivation_enabled": False,
        "master_seed_adopted": False,
        "automatic_seed_generation": False,
        "expected_implicit_negative_cases": len(cross_audit.CONTENT_TYPES) * len(NEGATIVE_CASES),
        "expected_collision_rejections": len(cross_audit.CONTENT_TYPES) * len(COLLISION_VALUES),
        "rejection_boundary": "CANONICAL_D9_9_D9_10_REQUEST_PLANNING_BEFORE_GODOT",
        "godot_invocations": 0,
    }
    if contract.get("experiment") != expected_experiment:
        raise SeedCollisionAuditError("Seed collision experiment contract drifted")
    _validate_seed_policy(contract.get("seed_policy", {}))
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or schema.get("$id") != SCHEMA_ID or schema.get("additionalProperties") is not False:
        raise SeedCollisionAuditError("Seed collision report schema identity/strictness mismatch")
    pins = contract.get("source_pins")
    if not isinstance(pins, list) or len(pins) != contract.get("source_pin_count") or len(pins) != len(PINNED_PATHS):
        raise SeedCollisionAuditError(f"Expected {len(PINNED_PATHS)} exact source pins")
    verified: list[dict[str, str]] = []
    seen: list[str] = []
    for row in pins:
        if not isinstance(row, dict) or set(row) != {"path", "sha256", "role"}:
            raise SeedCollisionAuditError("Malformed source pin row")
        rel, expected = row.get("path"), row.get("sha256")
        if not isinstance(rel, str) or rel not in PIN_ROLES or row.get("role") != PIN_ROLES[rel]:
            raise SeedCollisionAuditError(f"Unapproved source path or role: {rel!r}")
        if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
            raise SeedCollisionAuditError(f"Malformed source digest: {rel}")
        source = root / rel
        if not source.is_file() or _sha_file(source) != expected:
            raise SeedCollisionAuditError(f"Source pin mismatch: {rel}")
        verified.append({"path": rel, "sha256": expected, "role": row["role"]})
        seen.append(rel)
    if seen != list(PINNED_PATHS):
        raise SeedCollisionAuditError("Source pins must be unique, sorted and complete")
    if _sha_file(root / "release/C11C_FREEZE_PACKAGE_MANIFEST.json") != EXPECTED_MANIFEST_SHA256:
        raise SeedCollisionAuditError("Immutable C11-C manifest SHA-256 mismatch")
    cross_audit._load_and_validate_contract(root)
    return contract, schema, verified


def _rejected_implicit_seed_cases(root: Path) -> list[dict[str, str]]:
    outcomes: list[dict[str, str]] = []
    for content_type in cross_audit.CONTENT_TYPES:
        selection = cross_audit.EXPECTED_SELECTOR_SCOPE[content_type]["selection"]
        base = binder._base_request(selection, f"C11D-SEED-NEGATIVE-{content_type.upper()}")
        for case in NEGATIVE_CASES:
            request = deepcopy(base)
            if case == "missing_gameplay_seed": request.pop("seed")
            elif case == "null_gameplay_seed": request["seed"] = None
            elif case == "string_gameplay_seed": request["seed"] = "12345"
            elif case == "boolean_gameplay_seed": request["seed"] = True
            elif case == "zero_gameplay_seed": request["seed"] = 0
            elif case == "out_of_range_gameplay_seed": request["seed"] = 2147483647
            elif case == "missing_music_seed": request.pop("music_seed")
            elif case == "null_music_seed": request["music_seed"] = None
            elif case == "automatic_seed_mode": request["seed_mode"] = "auto"
            elif case == "master_seed_alias": request["master_seed"] = 12345
            else: raise SeedCollisionAuditError(f"Unknown negative case: {case}")
            try:
                binder._build_canonical_chain(request, root)
            except binder.DynamicRequestPayloadBindingError:
                outcomes.append({"content_type": content_type, "case": case, "result": "REJECTED_AS_REQUIRED"})
            else:
                raise SeedCollisionAuditError(f"Implicit/invalid seed request was accepted: {content_type}/{case}")
    return outcomes


def _rejected_numeric_seed_collisions(root: Path) -> list[dict[str, Any]]:
    outcomes: list[dict[str, Any]] = []
    for content_type in cross_audit.CONTENT_TYPES:
        selection = cross_audit.EXPECTED_SELECTOR_SCOPE[content_type]["selection"]
        for value in COLLISION_VALUES:
            request = binder._base_request(selection, f"C11D-SEED-COLLISION-{content_type.upper()}-{value}")
            request["seed"] = value
            request["music_seed"] = value
            try:
                binder._build_canonical_chain(request, root)
            except binder.DynamicRequestPayloadBindingError as exc:
                if "seed values must remain isolated" not in str(exc).lower():
                    raise SeedCollisionAuditError(f"Collision rejected for an unexpected reason: {content_type}/{value}: {exc}") from exc
                outcomes.append({"content_type": content_type, "case": f"equal_seed_collision_{value}", "collision_value": value, "result": "REJECTED_BEFORE_GODOT_AS_REQUIRED"})
            else:
                raise SeedCollisionAuditError(f"Equal gameplay/music seed values were accepted: {content_type}/{value}")
    return outcomes


def evaluate_seed_domain_rejections(
    root: Path | str | None = None,
) -> dict[str, Any]:
    project_root = _root(root)
    negatives = _rejected_implicit_seed_cases(project_root)
    collisions = _rejected_numeric_seed_collisions(project_root)
    report: dict[str, Any] = {
        "schema": SCHEMA_ID,
        "schema_version": "1.0",
        "status": STATUS,
        "scope": "EXPLICIT_SEED_NEGATIVE_MATRIX_AND_EQUAL_VALUE_COLLISION_REJECTION_FOR_TWO_PINNED_SELECTORS_ONLY",
        "selectors": len(cross_audit.CONTENT_TYPES),
        "explicit_seed_negative_cases": {"passed": len(negatives), "total": len(negatives)},
        "negative_case_count_per_selector": len(NEGATIVE_CASES),
        "numeric_seed_collision_rejections": {"passed": len(collisions), "total": len(collisions)},
        "collision_values_tested": list(COLLISION_VALUES),
        "all_rejections_precede_godot": True,
        "source_pin_count": len(PINNED_PATHS),
        "runtime_invocations": 0,
        "godot_version": None,
        "frozen_c11c_manifest_sha256": EXPECTED_MANIFEST_SHA256,
        "cross_type_seed_audit_contract_sha256": _sha_file(project_root / cross_audit.CONTRACT_REL),
        "runtime_seed_derivation_enabled": False,
        "automatic_seed_generation": False,
        "master_seed_adopted": False,
        "seed_domains_complete_for_candidate_input": False,
        "rejection_outcomes": negatives + collisions,
        "unclosed_requirements": [
            "Additional Challenge selectors and Visual Loop grammars remain unverified.",
            "Visual Drill seed sensitivity remains governed by its separate accepted 20-selector audit.",
            "The accepted cross-type runtime audit remains limited to one Challenge and one Visual Loop selector.",
            "This request-planning rejection audit does not prove catalog-wide seed-domain behavior or candidate input completeness.",
            "No renderer input admission, renderer activation, production execution or media creation is established.",
        ],
        "execution_boundary": deepcopy(GOVERNANCE_BOUNDARY),
    }
    return report


def _validate_report_schema(report: dict[str, Any], schema: dict[str, Any]) -> None:
    try:
        from jsonschema import Draft202012Validator
    except ImportError as exc:
        raise SeedCollisionAuditError("jsonschema is required for strict report validation") from exc
    errors = sorted(Draft202012Validator(schema).iter_errors(report), key=lambda err: list(err.path))
    if errors:
        raise SeedCollisionAuditError("Report schema validation failed: " + "; ".join(err.message for err in errors[:5]))
    unsigned = {key: value for key, value in report.items() if key != "audit_sha256"}
    if report.get("audit_sha256") != _sha_json(unsigned):
        raise SeedCollisionAuditError("Report audit_sha256 mismatch")


def run_seed_domain_rejection_audit(project_root: Path | str | None = None) -> dict[str, Any]:
    root = _root(project_root)
    contract, schema, pins = _load_and_validate_contract(root)
    report = evaluate_seed_domain_rejections(root)
    report["source_pin_count"] = len(pins)
    report["audit_sha256"] = _sha_json(report)
    _validate_report_schema(report, schema)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only explicit-seed and numeric-collision fail-closed audit; no Godot invocation")
    parser.add_argument("--root", default=str(ROOT), help="Repository root")
    parser.add_argument("--full-report", action="store_true", help="Print full audit JSON to stdout")
    args = parser.parse_args(argv)
    try:
        report = run_seed_domain_rejection_audit(args.root)
        print(
            "C11-D SEED DOMAIN REJECTION AUDIT PASS"
            f" | selectors={report['selectors']}"
            f" | explicit_seed_negative_cases={report['explicit_seed_negative_cases']['passed']}/{report['explicit_seed_negative_cases']['total']}"
            f" | numeric_seed_collision_rejections={report['numeric_seed_collision_rejections']['passed']}/{report['numeric_seed_collision_rejections']['total']}"
            " | all_rejections_precede_godot=true | runtime_invocations=0"
            f" | source_pins={report['source_pin_count']}/{report['source_pin_count']}"
            " | runtime_seed_derivation_enabled=false | automatic_seed_generation=false | master_seed_adopted=false"
            " | seed_domains_complete_for_candidate_input=false | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE"
        )
        if args.full_report:
            print(json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        return 0
    except (SeedCollisionAuditError, binder.DynamicRequestPayloadBindingError, OSError, ValueError, TypeError, KeyError) as exc:
        print(f"C11-D SEED DOMAIN REJECTION AUDIT FAIL | {exc} | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
