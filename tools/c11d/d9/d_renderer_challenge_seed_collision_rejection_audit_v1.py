from __future__ import annotations
"""Read-only seed explicitness/collision-rejection audit across all 9 canonical Challenge selectors."""
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
import d_renderer_challenge_seed_domain_preflight_v2 as challenge_preflight  # noqa: E402
import d_renderer_seed_domain_collision_audit as previous_collision_audit  # noqa: E402

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_SEED_COLLISION_REJECTION_AUDIT_V1.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_SEED_COLLISION_REJECTION_AUDIT_SCHEMA_V1.json")
EXPECTED_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
EXPECTED_CONTRACT_SHA256 = "c92376f5ec04d0dd73ef9e0775f7c57a78eb1c34678489576aaa7eee2085f780"
EXPECTED_SCHEMA_SHA256 = "67bc94300d16016317a111cbd0bf0b4390e1f0da12668177c50cf60b84155700"
EXPECTED_CHALLENGE_PREFLIGHT_CONTRACT_SHA256 = "fc09a92e1f16afd4409a6a161385d1c3bca7925bb7e9d43249944fcc6d195799"
EXPECTED_TWO_SELECTOR_COLLISION_CONTRACT_SHA256 = "d68c9e342c6c6937f05737d5299dda0310b6b72157d009eb6706c527232e49c8"
SCHEMA_ID = "urn:c11d:challenge-seed-collision-rejection-audit:v1"
STATUS = "PREPARATION_ONLY_CHALLENGE_SEED_COLLISION_REJECTION_NOT_INPUT_ADMISSION"
CHALLENGE_IDS = tuple(f"CHALLENGE_{i:03d}" for i in range(1, 10))
COLLISION_VALUES = (12345, 840001)
NEGATIVE_CASES = (
    "missing_gameplay_seed", "null_gameplay_seed", "string_gameplay_seed",
    "boolean_gameplay_seed", "zero_gameplay_seed", "out_of_range_gameplay_seed",
    "missing_music_seed", "null_music_seed", "automatic_seed_mode", "master_seed_alias",
)
EXPECTED_EXPERIMENT = {
    "content_type": "challenges",
    "challenge_ids": list(CHALLENGE_IDS),
    "expected_selector_count": 9,
    "explicit_seed_negative_cases": list(NEGATIVE_CASES),
    "expected_explicit_seed_negative_rejections": 90,
    "collision_values_tested": list(COLLISION_VALUES),
    "expected_numeric_seed_collision_rejections": 18,
    "rejection_boundary": "CANONICAL_D9_9_D9_10_REQUEST_PLANNING_BEFORE_GODOT_OR_PAYLOAD",
    "godot_invocations": 0,
    "request_input_persisted": False,
    "payload_materialized": False,
    "receipt_files_written": False,
}
PIN_ROLES = {
    "release/C11C_FREEZE_PACKAGE_MANIFEST.json": "IMMUTABLE_C11C_MANIFEST",
    "definitions/c11d/production/D_RENDERER_SEED_DOMAIN_COLLISION_AUDIT_V1.json": "ACCEPTED_TWO_SELECTOR_COLLISION_AUDIT_CONTRACT_V1",
    "definitions/c11d/production/D_RENDERER_SEED_DOMAIN_COLLISION_AUDIT_SCHEMA_V1.json": "ACCEPTED_TWO_SELECTOR_COLLISION_AUDIT_SCHEMA_V1",
    "tools/c11d/d9/d_renderer_seed_domain_collision_audit.py": "ACCEPTED_TWO_SELECTOR_COLLISION_AUDIT_RUNNER_V1",
    "definitions/c11d/production/D_RENDERER_CANDIDATE_SEED_DOMAIN_AUDIT_V1.json": "ACCEPTED_CROSS_TYPE_SEED_AUDIT_CONTRACT_V1",
    "definitions/c11d/production/D_RENDERER_CANDIDATE_SEED_DOMAIN_AUDIT_SCHEMA_V1.json": "ACCEPTED_CROSS_TYPE_SEED_AUDIT_SCHEMA_V1",
    "tools/c11d/d9/d_renderer_candidate_seed_domain_audit.py": "ACCEPTED_CROSS_TYPE_SEED_AUDIT_RUNNER_V1",
    "definitions/c11d/production/D_RENDERER_CHALLENGE_SEED_DOMAIN_PREFLIGHT_V2.json": "ACCEPTED_NINE_CHALLENGE_SEED_PREFLIGHT_CONTRACT_V2",
    "definitions/c11d/production/D_RENDERER_CHALLENGE_SEED_DOMAIN_PREFLIGHT_V2_SCHEMA.json": "ACCEPTED_NINE_CHALLENGE_SEED_PREFLIGHT_SCHEMA_V2",
    "definitions/c11d/production/D_RENDERER_CHALLENGE_SEED_DOMAIN_PREFLIGHT_V2_REPORT_SCHEMA.json": "ACCEPTED_NINE_CHALLENGE_SEED_PREFLIGHT_REPORT_SCHEMA_V2",
    "tools/c11d/d9/d_renderer_challenge_seed_domain_preflight_v2.py": "ACCEPTED_NINE_CHALLENGE_SEED_PREFLIGHT_RUNNER_V2",
    "tools/c11d/d9/universal_producer.py": "CANONICAL_D9_9_UNIVERSAL_PLANNER",
    "tools/c11d/d9/universal_editorial_model.py": "CANONICAL_EDITORIAL_SELECTOR_RESOLVER",
    "tools/c11d/d9/d_renderer_dynamic_request_payload_binding.py": "CANONICAL_D9_10_PLANNING_AND_SEED_REJECTION_CHAIN",
    "tools/c11d/d9/d_render_adapter.py": "CANONICAL_D9_10_SEED_DOMAIN_ISOLATION_GUARD",
    "definitions/c11d/production/C11D_UNIVERSAL_PRODUCER_REQUEST_D9_9_V1.json": "CANONICAL_D9_9_REQUEST_SCHEMA",
    "profiles/delivery/c11c_video_delivery_profiles.json": "CANONICAL_DELIVERY_PROFILE_REGISTRY",
    "c11c-suite/c11c-producer/c11d_gui_request.py": "CANONICAL_D4_GUI_CLI_PARITY_ADAPTER",
}
for _cid in CHALLENGE_IDS:
    PIN_ROLES[f"challenges/{_cid}.json"] = "CANONICAL_CHALLENGE_DEFINITION_" + _cid
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
    "D4.8": "BLOCKED",
    "release_authority": "NONE",
}

class ChallengeSeedCollisionAuditError(RuntimeError):
    """Pinned source drift or a required seed/collision rejection did not occur."""

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
        raise ChallengeSeedCollisionAuditError(f"Cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ChallengeSeedCollisionAuditError(f"Expected JSON object: {path}")
    return value

def _load_and_validate_contract(root: Path):
    contract_path, schema_path = root / CONTRACT_REL, root / SCHEMA_REL
    if not contract_path.is_file() or _sha_file(contract_path) != EXPECTED_CONTRACT_SHA256:
        raise ChallengeSeedCollisionAuditError("Challenge seed collision audit contract missing or SHA-256 mismatch")
    if not schema_path.is_file() or _sha_file(schema_path) != EXPECTED_SCHEMA_SHA256:
        raise ChallengeSeedCollisionAuditError("Challenge seed collision report schema missing or SHA-256 mismatch")
    if _sha_file(root / "release/C11C_FREEZE_PACKAGE_MANIFEST.json") != EXPECTED_MANIFEST_SHA256:
        raise ChallengeSeedCollisionAuditError("Frozen C11-C manifest SHA-256 mismatch")
    contract, schema = _read_json(contract_path), _read_json(schema_path)
    if contract.get("schema") != "C11-D-D9-CHALLENGE-SEED-COLLISION-REJECTION-AUDIT-CONTRACT-V1" or contract.get("schema_version") != "1.0":
        raise ChallengeSeedCollisionAuditError("Challenge seed collision contract identity/version mismatch")
    if contract.get("status") != "READ_ONLY_CANONICAL_CHALLENGE_SELECTOR_COLLISION_REJECTION_AUDIT_NOT_INPUT_ADMISSION":
        raise ChallengeSeedCollisionAuditError("Challenge collision contract is not read-only")
    if contract.get("source_of_truth", {}).get("frozen_c11c_manifest_sha256") != EXPECTED_MANIFEST_SHA256:
        raise ChallengeSeedCollisionAuditError("Frozen C11-C contract reference mismatch")
    if contract.get("source_of_truth", {}).get("accepted_challenge_preflight_contract_sha256") != EXPECTED_CHALLENGE_PREFLIGHT_CONTRACT_SHA256:
        raise ChallengeSeedCollisionAuditError("Nine-Challenge preflight contract pin mismatch")
    if contract.get("source_of_truth", {}).get("accepted_two_selector_collision_audit_contract_sha256") != EXPECTED_TWO_SELECTOR_COLLISION_CONTRACT_SHA256:
        raise ChallengeSeedCollisionAuditError("Two-selector collision audit linkage mismatch")
    if contract.get("experiment") != EXPECTED_EXPERIMENT:
        raise ChallengeSeedCollisionAuditError("Challenge seed collision experiment contract drifted")
    expected_seed_policy = {
        "required_fields": ["seed", "music_seed"],
        "runtime_seed_derivation_enabled": False,
        "automatic_seed_generation": False,
        "master_seed_adopted": False,
        "equal_numeric_values_across_domains": "REJECTED_FAIL_CLOSED",
        "collision_guard_message_contains": "Gameplay and music seed values must remain isolated",
    }
    if contract.get("seed_policy") != expected_seed_policy:
        raise ChallengeSeedCollisionAuditError("Challenge seed policy weakened or changed")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or schema.get("$id") != SCHEMA_ID or schema.get("additionalProperties") is not False:
        raise ChallengeSeedCollisionAuditError("Challenge seed collision report schema identity/strictness mismatch")
    try:
        import jsonschema
        jsonschema.Draft202012Validator.check_schema(schema)
    except ImportError as exc:
        raise ChallengeSeedCollisionAuditError("jsonschema is required for strict report validation") from exc
    except Exception as exc:
        raise ChallengeSeedCollisionAuditError(f"Report schema invalid: {exc}") from exc
    pins = contract.get("source_pins")
    if not isinstance(pins, list) or len(pins) != contract.get("source_pin_count") or len(pins) != len(PINNED_PATHS):
        raise ChallengeSeedCollisionAuditError(f"Expected {len(PINNED_PATHS)} exact source pins")
    verified, seen = [], []
    for row in pins:
        if not isinstance(row, dict) or set(row) != {"path", "sha256", "role"}:
            raise ChallengeSeedCollisionAuditError("Malformed source pin row")
        rel, expected = row.get("path"), row.get("sha256")
        if not isinstance(rel, str) or rel not in PIN_ROLES or row.get("role") != PIN_ROLES[rel]:
            raise ChallengeSeedCollisionAuditError(f"Unapproved source path/role: {rel!r}")
        if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
            raise ChallengeSeedCollisionAuditError(f"Malformed source digest: {rel}")
        path = root / rel
        if not path.is_file() or _sha_file(path) != expected:
            raise ChallengeSeedCollisionAuditError(f"Source pin mismatch: {rel}")
        verified.append({"path": rel, "sha256": expected, "role": row["role"]})
        seen.append(rel)
    if seen != list(PINNED_PATHS):
        raise ChallengeSeedCollisionAuditError("Source pins must be sorted, unique and complete")
    # Revalidate the accepted base audits and the canonical 9-selector planning matrix.
    previous_collision_audit._load_and_validate_contract(root)
    _, _, _, _, selector_rows = challenge_preflight._load_and_validate_contract(root)
    if [row["challenge_id"] for row in selector_rows] != list(CHALLENGE_IDS):
        raise ChallengeSeedCollisionAuditError("Challenge selector matrix no longer matches CHALLENGE_001..009")
    return contract, schema, verified, selector_rows

def _mutate_seed_case(request: dict[str, Any], case: str) -> None:
    if case == "missing_gameplay_seed": request.pop("seed", None)
    elif case == "null_gameplay_seed": request["seed"] = None
    elif case == "string_gameplay_seed": request["seed"] = "12345"
    elif case == "boolean_gameplay_seed": request["seed"] = True
    elif case == "zero_gameplay_seed": request["seed"] = 0
    elif case == "out_of_range_gameplay_seed": request["seed"] = 2147483647
    elif case == "missing_music_seed": request.pop("music_seed", None)
    elif case == "null_music_seed": request["music_seed"] = None
    elif case == "automatic_seed_mode": request["seed_mode"] = "auto"
    elif case == "master_seed_alias": request["master_seed"] = 12345
    else: raise ChallengeSeedCollisionAuditError(f"Unknown negative case: {case}")

def _expected_error_fragment(case: str) -> str:
    if case in ("missing_gameplay_seed", "null_gameplay_seed", "string_gameplay_seed", "boolean_gameplay_seed"):
        return "seed must be an integer"
    if case in ("zero_gameplay_seed", "out_of_range_gameplay_seed"):
        return "seed must be in the range 1..2147483646"
    if case in ("missing_music_seed", "null_music_seed"):
        return "music_seed must be an integer"
    if case == "automatic_seed_mode": return "unknown universal request field(s): seed_mode"
    if case == "master_seed_alias": return "unknown universal request field(s): master_seed"
    raise ChallengeSeedCollisionAuditError(f"Unknown negative case: {case}")

def _canonical_selection(selection: dict[str, Any]) -> dict[str, Any]:
    return {key: selection.get(key) for key in ("content_type", "family_id", "subtype_id", "variant_id")}

def evaluate_challenge_seed_collisions(root: Path, selector_rows: list[dict[str, Any]]) -> dict[str, Any]:
    negative_outcomes: list[dict[str, Any]] = []
    collision_outcomes: list[dict[str, Any]] = []
    report_selectors: list[dict[str, Any]] = []
    for row in selector_rows:
        challenge_id = row["challenge_id"]
        selection = challenge_preflight._selection_for(root, challenge_id, row["family_id"])
        if selection != {"content_type":"challenges", "family_id":row["family_id"], "subtype_id":None, "variant_id":challenge_id}:
            raise ChallengeSeedCollisionAuditError(f"Canonical selection drift: {challenge_id}")
        base = binder._base_request(selection, f"C11D-CHALLENGE-COLLISION-NEGATIVE-{challenge_id}")
        for case in NEGATIVE_CASES:
            request = deepcopy(base)
            _mutate_seed_case(request, case)
            try:
                binder._build_canonical_chain(request, root)
            except binder.DynamicRequestPayloadBindingError as exc:
                expected = _expected_error_fragment(case)
                if expected not in str(exc).lower():
                    raise ChallengeSeedCollisionAuditError(f"Wrong rejection boundary for {challenge_id}/{case}: {exc}") from exc
                negative_outcomes.append({"content_type":"challenges", "challenge_id":challenge_id, "case":case, "result":"REJECTED_AS_REQUIRED"})
            else:
                raise ChallengeSeedCollisionAuditError(f"Invalid explicit seed was accepted: {challenge_id}/{case}")
        report_selectors.append({
            "challenge_id":challenge_id,
            "family_id":row["family_id"],
            "mechanic":row["mechanic"],
            "source_path":row["source_path"],
            "source_sha256":row["source_sha256"],
            "canonical_selection":_canonical_selection(selection),
        })
        for value in COLLISION_VALUES:
            request = binder._base_request(selection, f"C11D-CHALLENGE-SEED-COLLISION-{challenge_id}-{value}")
            request["seed"] = value
            request["music_seed"] = value
            try:
                binder._build_canonical_chain(request, root)
            except binder.DynamicRequestPayloadBindingError as exc:
                if "gameplay and music seed values must remain isolated" not in str(exc).lower():
                    raise ChallengeSeedCollisionAuditError(f"Wrong collision rejection boundary for {challenge_id}/{value}: {exc}") from exc
                collision_outcomes.append({"content_type":"challenges", "challenge_id":challenge_id, "case":f"equal_seed_collision_{value}", "collision_value":value, "result":"REJECTED_BEFORE_GODOT_AS_REQUIRED"})
            else:
                raise ChallengeSeedCollisionAuditError(f"Equal gameplay/music seed was accepted: {challenge_id}/{value}")
    if len(negative_outcomes) != 90 or len(collision_outcomes) != 18 or len(report_selectors) != 9:
        raise ChallengeSeedCollisionAuditError("Challenge seed collision matrix cardinality mismatch")
    return {
        "selectors": report_selectors,
        "negative_outcomes": negative_outcomes,
        "collision_outcomes": collision_outcomes,
    }

def _validate_report(report: dict[str, Any], schema: dict[str, Any]) -> None:
    import jsonschema
    errors = sorted(jsonschema.Draft202012Validator(schema).iter_errors(report), key=lambda err: list(err.path))
    if errors:
        raise ChallengeSeedCollisionAuditError("Strict report schema failed: " + "; ".join(err.message for err in errors[:6]))
    unsigned = {key:value for key,value in report.items() if key != "audit_sha256"}
    if report.get("audit_sha256") != _sha_json(unsigned):
        raise ChallengeSeedCollisionAuditError("Audit report self-hash mismatch")

def run_audit(project_root: Path | str | None = None) -> dict[str, Any]:
    root = Path(project_root).resolve() if project_root is not None else ROOT
    contract, schema, pins, selector_rows = _load_and_validate_contract(root)
    evaluated = evaluate_challenge_seed_collisions(root, selector_rows)
    report = {
        "schema": SCHEMA_ID,
        "schema_version": "1.0",
        "status": STATUS,
        "scope": "NINE_CANONICAL_CHALLENGE_SELECTORS_X_TEN_EXPLICIT_SEED_NEGATIVES_PLUS_TWO_NUMERIC_COLLISIONS",
        "selectors": len(evaluated["selectors"]),
        "selector_matrix": evaluated["selectors"],
        "explicit_seed_negative_cases": {"passed":len(evaluated["negative_outcomes"]), "total":90},
        "negative_case_count_per_selector":len(NEGATIVE_CASES),
        "numeric_seed_collision_rejections":{"passed":len(evaluated["collision_outcomes"]), "total":18},
        "collision_values_tested":list(COLLISION_VALUES),
        "all_rejections_precede_godot":True,
        "source_pin_count":len(pins),
        "runtime_invocations":0,
        "godot_version":None,
        "frozen_c11c_manifest_sha256":EXPECTED_MANIFEST_SHA256,
        "challenge_seed_domain_preflight_contract_sha256":_sha_file(root / challenge_preflight.CONTRACT_REL),
        "two_selector_collision_audit_contract_sha256":EXPECTED_TWO_SELECTOR_COLLISION_CONTRACT_SHA256,
        "runtime_seed_derivation_enabled":False,
        "automatic_seed_generation":False,
        "master_seed_adopted":False,
        "seed_domains_complete_for_candidate_input":False,
        "rejection_outcomes":evaluated["negative_outcomes"] + evaluated["collision_outcomes"],
        "unclosed_requirements":[
            "The nine-selector audit proves planning-time rejection behavior only; it does not materialize visual payloads or prove Challenge gameplay-seed visual sensitivity.",
            "Visual Loop grammars beyond harmonic_membrane remain outside the accepted cross-type runtime matrix.",
            "Visual Drill seed coverage remains governed by its separate 20-selector audit; this Challenge audit does not replace it.",
            "Challenge selectors CHALLENGE_008 and CHALLENGE_009 retain the declared 11-second versus 12-second phase-duration conflict.",
            "Automatic/default seed behavior, master_seed adoption, arbitrary input domains, I/O completeness and prospective renderer-input admission remain unapproved.",
            "No renderer input admission, renderer activation, production execution or media creation is established.",
        ],
        "execution_boundary":deepcopy(GOVERNANCE_BOUNDARY),
    }
    report["audit_sha256"] = _sha_json(report)
    _validate_report(report, schema)
    return report

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only Challenge seed collision rejection audit; no Godot or payload materialization")
    parser.add_argument("--root", default=str(ROOT), help="Repository root")
    parser.add_argument("--full-report", action="store_true", help="Print report JSON as the final stdout line")
    args = parser.parse_args(argv)
    try:
        report = run_audit(args.root)
        print(
            "C11-D CHALLENGE SEED COLLISION REJECTION AUDIT V1 PASS"
            f" | selectors={report['selectors']}"
            f" | explicit_seed_negative_cases={report['explicit_seed_negative_cases']['passed']}/{report['explicit_seed_negative_cases']['total']}"
            f" | numeric_seed_collision_rejections={report['numeric_seed_collision_rejections']['passed']}/{report['numeric_seed_collision_rejections']['total']}"
            " | collision_values=12345,840001 | all_rejections_precede_godot=true | runtime_invocations=0"
            f" | source_pins={report['source_pin_count']}/{report['source_pin_count']}"
            " | seed_domains_complete_for_candidate_input=false | renderer=OFF | media_created=false | candidate_input_admissible=false | D4.8=BLOCKED | release_authority=NONE"
        )
        if args.full_report:
            print(json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        return 0
    except (ChallengeSeedCollisionAuditError, binder.DynamicRequestPayloadBindingError, OSError, ValueError, TypeError, KeyError) as exc:
        print("C11-D CHALLENGE SEED COLLISION REJECTION AUDIT V1 FAIL | " + str(exc) + " | renderer=OFF | media_created=false | candidate_input_admissible=false | D4.8=BLOCKED | release_authority=NONE")
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
