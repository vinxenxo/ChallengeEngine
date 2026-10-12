#!/usr/bin/env python3
"""Read-only C11-D shared editorial/presentation inheritance conformance audit."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

CONTRACT_PATH = "definitions/c11d/production/D_RENDERER_SHARED_EDITORIAL_PRESENTATION_INHERITANCE_V1.json"
SCHEMA_PATH = "definitions/c11d/production/D_RENDERER_SHARED_EDITORIAL_PRESENTATION_INHERITANCE_SCHEMA_V1.json"
EXPECTED_SCHEMA = "C11-D-D9-SHARED-EDITORIAL-PRESENTATION-INHERITANCE-CONTRACT-V1"
EXPECTED_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
SUPPORTED_TYPES = ["challenges", "visual_loops", "visual_drills"]
EXPECTED_COMMON_FIELDS = ["title", "subtitle", "call_to_action", "language"]
EXPECTED_DISPLAY_FIELDS = ["title", "subtitle", "call_to_action"]
EXPECTED_CHALLENGE_FIELDS = ["player_name", "challenge_label"]
EXPECTED_RESERVED_DISABLED = [
    "hook", "preparation_text", "final_text", "header_line_1", "header_line_2",
    "footer_line_1", "footer_line_2", "show_title", "show_subtitle",
    "show_call_to_action", "show_header", "show_footer",
]
EXPECTED_INHERITANCE = ["global", "content_type", "family", "subtype", "variant", "production_override"]
EXPECTED_SELECTOR_DIMENSIONS = ["content_type", "family_id", "subtype_id", "variant_id"]


class AuditError(RuntimeError):
    pass


def _read_json(root: Path, relative: str) -> dict[str, Any]:
    path = (root / relative).resolve()
    root_resolved = root.resolve()
    if path != root_resolved and root_resolved not in path.parents:
        raise AuditError(f"unsafe source path: {relative}")
    if not path.is_file():
        raise AuditError(f"required source missing: {relative}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AuditError(f"invalid JSON source {relative}: {exc}") from exc
    if not isinstance(data, dict):
        raise AuditError(f"source must be a JSON object: {relative}")
    return data


def _sha256(root: Path, relative: str) -> str:
    path = (root / relative).resolve()
    root_resolved = root.resolve()
    if path != root_resolved and root_resolved not in path.parents:
        raise AuditError(f"unsafe source path: {relative}")
    if not path.is_file():
        raise AuditError(f"pinned source missing: {relative}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def audit(root: Path, contract_override: dict[str, Any] | None = None) -> dict[str, Any]:
    root = root.resolve()
    contract = contract_override if contract_override is not None else _read_json(root, CONTRACT_PATH)
    schema = _read_json(root, SCHEMA_PATH)
    errors: list[str] = []

    try:
        import jsonschema
        jsonschema.Draft202012Validator.check_schema(schema)
        jsonschema.Draft202012Validator(schema).validate(contract)
    except ImportError as exc:
        raise AuditError("jsonschema package is required for draft 2020-12 contract validation") from exc
    except Exception as exc:
        errors.append(f"contract schema validation failed: {exc}")

    _require(contract.get("schema") == EXPECTED_SCHEMA, "unexpected contract schema identity", errors)
    _require(contract.get("schema_version") == "1.0", "unexpected contract version", errors)
    _require(contract.get("status") == "ARCHITECTURE_CONTRACT_PROPOSAL_NOT_RENDERER_INPUT", "contract status overstates runtime authority", errors)

    pins = contract.get("source_lineage", [])
    pin_paths = [p.get("path") for p in pins if isinstance(p, dict)]
    _require(len(pins) == 8, f"expected 8 pinned source records, found {len(pins)}", errors)
    _require(len(pin_paths) == len(set(pin_paths)), "source pin paths are duplicated", errors)
    _require(pins[0].get("path") == "release/C11C_FREEZE_PACKAGE_MANIFEST.json" if pins and isinstance(pins[0], dict) else False,
             "frozen C11-C manifest must be the first exact source pin", errors)
    _require(pins[0].get("sha256") == EXPECTED_MANIFEST_SHA256 if pins and isinstance(pins[0], dict) else False,
             "frozen C11-C manifest pin differs from the authoritative hash", errors)

    pin_success = 0
    for pin in pins:
        if not isinstance(pin, dict):
            errors.append("source_lineage entry is not an object")
            continue
        relative = pin.get("path", "")
        digest = pin.get("sha256", "")
        if not isinstance(relative, str) or not relative or not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            errors.append("source_lineage contains an invalid path or SHA-256")
            continue
        try:
            actual = _sha256(root, relative)
        except AuditError as exc:
            errors.append(str(exc))
            continue
        if actual != digest:
            errors.append(f"source pin mismatch: {relative} expected={digest} actual={actual}")
        else:
            pin_success += 1

    try:
        editorial = _read_json(root, "definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json")
        request = _read_json(root, "definitions/c11d/production/C11D_UNIVERSAL_PRODUCER_REQUEST_D9_9_V1.json")
        bridge = _read_json(root, "definitions/c11d/production/C11D_EDITORIAL_RENDER_BRIDGE_D9_10_V1.json")
        grammar_instance = _read_json(root, "definitions/c11d/production/D_RENDERER_VISUAL_LOOP_GRAMMAR_PARAMETER_INSTANCE_V1.json")
        presentation_policy = _read_json(root, "definitions/c11d/production/D_RENDERER_UNIFIED_PRESENTATION_REGION_POLICY_PROPOSAL_V1.json")
    except AuditError as exc:
        errors.append(str(exc))
        editorial = request = bridge = grammar_instance = presentation_policy = {}

    fields = editorial.get("editorial_fields", {})
    types = request.get("supported_content_types", [])
    _require(types == SUPPORTED_TYPES, f"canonical D9.9 supported content types drifted: {types}", errors)
    _require(contract.get("current_coverage_snapshot", {}).get("supported_content_types") == types,
             "contract supported content types differ from the canonical D9.9 request", errors)
    _require(request.get("selection_fields") == EXPECTED_SELECTOR_DIMENSIONS,
             "canonical D9.9 selector dimensions changed", errors)
    _require(contract.get("future_gui_selection_contract", {}).get("selector_dimensions") == EXPECTED_SELECTOR_DIMENSIONS,
             "future GUI selector dimensions do not match D9.9", errors)
    _require(contract.get("future_gui_selection_contract", {}).get("editorial_inheritance_order") == editorial.get("inheritance_order"),
             "editorial inheritance order does not match the canonical model", errors)
    _require(editorial.get("inheritance_order") == EXPECTED_INHERITANCE, "canonical editorial inheritance order changed", errors)

    actual_common = [
        name for name, spec in fields.items()
        if spec.get("enabled") is True and all(t in spec.get("content_types", []) for t in SUPPORTED_TYPES)
    ]
    _require(actual_common == EXPECTED_COMMON_FIELDS,
             f"canonical shared enabled editorial fields differ: {actual_common}", errors)
    _require(contract.get("shared_editorial_layer", {}).get("shared_enabled_fields") == actual_common,
             "shared enabled fields disagree with the canonical editorial model", errors)
    actual_display = [x for x in actual_common if x != "language"]
    _require(actual_display == EXPECTED_DISPLAY_FIELDS, "display-text field classification changed", errors)
    _require(contract.get("shared_editorial_layer", {}).get("shared_display_text_fields") == actual_display,
             "shared display-text classification differs from canonical fields", errors)
    actual_metadata = [x for x in actual_common if x == "language"]
    _require(contract.get("shared_editorial_layer", {}).get("shared_metadata_fields") == actual_metadata,
             "shared metadata classification differs from canonical fields", errors)
    actual_challenge_only = [
        name for name, spec in fields.items()
        if spec.get("enabled") is True and spec.get("content_types") == ["challenges"]
    ]
    _require(actual_challenge_only == EXPECTED_CHALLENGE_FIELDS,
             f"challenge-only enabled editorial fields differ: {actual_challenge_only}", errors)
    _require(contract.get("shared_editorial_layer", {}).get("challenge_only_enabled_fields") == actual_challenge_only,
             "challenge-only editorial fields differ from canonical model", errors)
    actual_reserved = [
        name for name, spec in fields.items()
        if spec.get("enabled") is False and str(spec.get("status", "")).startswith("RESERVED_NOT_ENABLED")
    ]
    _require(actual_reserved == EXPECTED_RESERVED_DISABLED,
             f"reserved disabled fields differ from expected canonical set: {actual_reserved}", errors)
    _require(contract.get("shared_editorial_layer", {}).get("reserved_disabled_fields") == actual_reserved,
             "contract no longer preserves all reserved disabled editorial fields", errors)

    map_editorial = bridge.get("mapping_contract", {}).get("editorial", {})
    map_presentation = bridge.get("mapping_contract", {}).get("presentation_profile", {})
    _require(map_editorial.get("source") == "plan.editorial", "D9.10 bridge editorial source changed", errors)
    _require(map_editorial.get("allowlist_source") == "definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json",
             "D9.10 bridge no longer uses the canonical editorial allowlist", errors)
    _require(map_presentation.get("source") == "plan.presentation_profile_id" and map_presentation.get("classification") == "REGISTERED_PROFILE_REFERENCE_ONLY",
             "D9.10 presentation profile must remain a canonical reference only", errors)

    loop = contract.get("current_coverage_snapshot", {}).get("visual_loops", {})
    instance_scope = grammar_instance.get("scope", {})
    instance_semantics = grammar_instance.get("materialization_semantics", {})
    _require(loop.get("known_selector", {}).get("family_id") == instance_scope.get("family_id") and
             loop.get("known_selector", {}).get("subtype_id") == instance_scope.get("subtype_id"),
             "known Visual Loop selector differs from pinned grammar parameter instance", errors)
    _require(instance_semantics.get("exact_grammar_parameter_instance_materialized") is True,
             "current grammar parameter instance evidence is not marked materialized", errors)
    _require(instance_semantics.get("exact_selector_visual_payload_materialized") is False,
             "contract overstates exact selector visual payload materialization", errors)
    _require(instance_semantics.get("family_authoring_envelope_grammar_gap") == "REMAINS_OPEN",
             "family authoring envelope gap was incorrectly closed", errors)

    policy_approval = presentation_policy.get("approval_state", {})
    _require(policy_approval.get("semantic_region_mapping_approved") is False and
             policy_approval.get("shared_presentation_region_policy_approved") is False and
             policy_approval.get("frame_program_approved") is False,
             "presentation policy proposal must remain unapproved", errors)
    _require(contract.get("shared_presentation_layer", {}).get("geometry_state") == "UNRESOLVED_POLICY_PROPOSAL_NOT_APPROVED",
             "presentation geometry status is overstated", errors)

    new_family = contract.get("new_family_registration", {})
    exception_policy = contract.get("family_exception_policy", {})
    _require(new_family.get("registered_family_default") == "INHERIT_SHARED_EDITORIAL_AND_PRESENTATION_CONTRACT" and
             new_family.get("shared_editorial_inheritance_default") is True and
             new_family.get("shared_presentation_inheritance_default") is True and
             new_family.get("unknown_family_before_registration") == "REJECT",
             "new-family inheritance defaults or unknown-selector rejection changed", errors)
    _require(new_family.get("silent_exception_allowed") is False and
             exception_policy.get("active_exception_count") == 0 and
             exception_policy.get("exception_source_must_be_hash_bound") is True and
             exception_policy.get("exception_must_be_explicitly_approved_before_activation") is True,
             "family exception policy is not fail-closed", errors)
    _require(set(exception_policy.get("exception_must_declare", [])) >= {
             "exception_id", "family_id", "reason", "changed_fields", "schema_version", "source_path", "source_sha256", "approval_state"},
             "family exception declaration fields are incomplete", errors)

    boundary = contract.get("execution_boundary", {})
    _require(boundary.get("audit_mode") == "STATIC_READ_ONLY_SOURCE_CONFORMANCE" and
             boundary.get("renderer") == "OFF" and boundary.get("media_created") is False and
             boundary.get("renderer_native_input_emitted") is False and boundary.get("renderer_dispatch_invoked") is False and
             boundary.get("d4_8") == "BLOCKED" and boundary.get("release_authority") == "NONE" and
             boundary.get("d9_17") == "BLOCKED_NO_GO" and boundary.get("d10") == "BLOCKED",
             "execution/governance boundary was weakened", errors)

    checks = [
        "strict_contract_schema", "frozen_manifest_first_pin", "all_source_pins_match", "selector_contract_matches_d9_9",
        "editorial_inheritance_matches_d9_8", "shared_editorial_fields_match_canonical_model", "reserved_fields_remain_disabled",
        "bridge_uses_canonical_editorial_and_profile_refs", "known_loop_selector_matches_instance_contract",
        "family_authoring_envelope_gap_remains_open", "presentation_policy_remains_unapproved",
        "new_family_default_inherits_shared_layers", "family_exceptions_are_explicit_and_fail_closed",
        "runtime_and_release_authority_remain_disabled"
    ]
    if errors:
        raise AuditError("; ".join(errors))
    return {
        "schema": "C11-D-D9-SHARED-EDITORIAL-PRESENTATION-INHERITANCE-AUDIT-REPORT-V1",
        "status": "PASS",
        "checks_passed": len(checks),
        "checks_total": len(checks),
        "source_pins_passed": pin_success,
        "source_pins_total": len(pins),
        "shared_fields": len(actual_common),
        "challenge_only_fields": len(actual_challenge_only),
        "reserved_disabled_fields": len(actual_reserved),
        "supported_content_types": len(types),
        "selector_dimensions": len(EXPECTED_SELECTOR_DIMENSIONS),
        "inheritance_layers": len(EXPECTED_INHERITANCE),
        "active_family_exceptions": exception_policy.get("active_exception_count"),
        "new_family_default": "INHERIT_SHARED_EDITORIAL_AND_PRESENTATION_CONTRACT",
        "exact_loop_grammar_parameter_instance": "PROVEN_FOR_PINNED_SELECTOR",
        "exact_selector_visual_payload": "NOT_MATERIALIZED",
        "presentation_geometry": "UNAPPROVED",
        "renderer": "OFF",
        "media_created": False,
        "d4_8": "BLOCKED",
        "release_authority": "NONE",
        "d9_17": "BLOCKED_NO_GO",
        "d10": "BLOCKED",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[3]), help="Repository root")
    args = parser.parse_args(argv)
    try:
        report = audit(Path(args.root))
    except AuditError as exc:
        print(f"C11-D SHARED EDITORIAL/PRESENTATION INHERITANCE AUDIT FAIL | {exc}")
        return 1
    except Exception as exc:  # fail closed for unexpected audit/schema errors
        print(f"C11-D SHARED EDITORIAL/PRESENTATION INHERITANCE AUDIT FAIL | unexpected error: {exc}")
        return 1
    print(
        "C11-D SHARED EDITORIAL/PRESENTATION INHERITANCE AUDIT PASS | "
        f"checks={report['checks_passed']}/{report['checks_total']} | "
        f"source_pins={report['source_pins_passed']}/{report['source_pins_total']} | "
        f"shared_fields={report['shared_fields']}/4 | "
        f"challenge_only={report['challenge_only_fields']}/2 | "
        f"reserved_disabled={report['reserved_disabled_fields']}/12 | "
        f"content_types={report['supported_content_types']}/3 | "
        f"selector_dimensions={report['selector_dimensions']}/4 | "
        f"inheritance_layers={report['inheritance_layers']}/6 | "
        f"family_exceptions={report['active_family_exceptions']} | "
        f"new_family_default=INHERIT | exact_loop_payload={report['exact_selector_visual_payload']} | "
        f"presentation_geometry={report['presentation_geometry']} | renderer={report['renderer']} | "
        f"media_created={str(report['media_created']).lower()} | D4.8={report['d4_8']} | "
        f"release_authority={report['release_authority']} | D9.17={report['d9_17']} | D10={report['d10']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
