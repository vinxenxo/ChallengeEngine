"""Build a D-owned, hash-bound editorial sidecar for fixed in-memory review payloads.

The carrier preserves canonical D9.9 editorial values without injecting them into the
visual payload, choosing geometry/visibility windows, emitting renderer input, or
activating production. Only editable values may vary; source selector/seed/profile
identities remain the already reviewed fixed fixtures.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from d_renderer_editorial_field_routing_visibility_reconciliation import (
    EXPECTED_FIELDS,
    VISUAL_FIELDS,
    build_reconciliation,
)
from d_renderer_request_scoped_payload_materialization_binding import (
    EXPECTED_MANIFEST_SHA256,
    CONTRACT_REL as MATERIALIZATION_CONTRACT_REL,
    SCHEMA_REL as MATERIALIZATION_SCHEMA_REL,
    STATUS as MATERIALIZATION_STATUS,
    RequestScopedMaterializationBindingError,
    _build_request_chains,
    _canonical,
    _fixture_requests,
    _load_contract as _load_materialization_contract,
    _raw_request,
    _read_json,
    _request,
    _root,
    _sha_file,
    _sha_json,
    run_review as run_materialization_review,
)

AUDIT_CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_EDITORIAL_FIELD_CONSUMPTION_AUDIT_V1.json")
CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_REQUEST_SCOPED_EDITORIAL_VALUE_CARRIER_V1.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_REQUEST_SCOPED_EDITORIAL_VALUE_CARRIER_SCHEMA_V1.json")
INPUT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_REQUEST_SCOPED_EDITORIAL_VALUE_INPUT_SCHEMA_V1.json")
CONTRACT_ID = "C11-D-RENDERER-REQUEST-SCOPED-EDITORIAL-VALUE-CARRIER-CONTRACT-V1"
OUTPUT_SCHEMA = "C11-D-D9-REQUEST-SCOPED-EDITORIAL-VALUE-CARRIER-V1"
OUTPUT_STATUS = "PREPARATION_ONLY_HASH_BOUND_EDITORIAL_SIDECAR_NOT_VISUAL_CONSUMPTION"
INPUT_SCHEMA_ID = "C11-D-D9-REQUEST-SCOPED-EDITORIAL-VALUE-OVERRIDES-V1"
CONTENT_TYPES = ("challenges", "visual_loops", "visual_drills")
FIELD_CLASS = {field: ("METADATA_ONLY" if field == "language" else "VISUAL_TEXT") for fields in EXPECTED_FIELDS.values() for field in fields}

class EditorialValueCarrierError(ValueError):
    """Raised when a source pin, override input, sidecar or governance lock drifts."""


def _sha_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _is_sha256(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(c in "0123456789abcdef" for c in value)


def _load_contract(root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[dict[str, str]]]:
    contract = _read_json(root, CONTRACT_REL)
    schema = _read_json(root, SCHEMA_REL)
    input_schema = _read_json(root, INPUT_SCHEMA_REL)
    if contract.get("schema") != CONTRACT_ID or contract.get("schema_version") != "1.0":
        raise EditorialValueCarrierError("Editorial value-carrier contract identity/version mismatch")
    if contract.get("status") != OUTPUT_STATUS or contract.get("candidate_input_admissible") is not False:
        raise EditorialValueCarrierError("Editorial value-carrier contract cannot promote candidate readiness")
    if contract.get("source_of_truth", {}).get("frozen_c11c_manifest_sha256") != EXPECTED_MANIFEST_SHA256:
        raise EditorialValueCarrierError("Frozen C11-C manifest pin differs from the established freeze")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or schema.get("$id") != "urn:c11d:renderer-request-scoped-editorial-value-carrier:v1" or schema.get("additionalProperties") is not False:
        raise EditorialValueCarrierError("Carrier output schema identity/strictness mismatch")
    if set(schema.get("required", [])) != set(schema.get("properties", {})):
        raise EditorialValueCarrierError("Carrier output schema top-level required/properties mismatch")
    if input_schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or input_schema.get("$id") != "urn:c11d:renderer-request-scoped-editorial-value-input:v1" or input_schema.get("additionalProperties") is not False:
        raise EditorialValueCarrierError("Editorial override-input schema identity/strictness mismatch")
    expected_boundary = {
        "mode": "IN_MEMORY_REVIEW_ONLY_SIDECAR",
        "payload_files_written": False,
        "receipt_files_written": False,
        "renderer_native_input_emitted": False,
        "renderer_dispatch_invoked": False,
        "renderer_activation": False,
        "production_execution": False,
        "media_output_created": False,
        "output_artifact_path": None,
        "payload_mutated": False,
        "editorial_values_injected_into_visual_payload": False,
        "c11c_source_mutation": False,
        "d4_8": "BLOCKED",
        "release_authority": "NONE",
        "d9_14": "BLOCKED_AS_REQUIRED",
        "d9_16": "BLOCKED_AS_REQUIRED",
        "d9_17": "BLOCKED_NO_GO",
        "d10": "BLOCKED",
    }
    if contract.get("execution_boundary") != expected_boundary:
        raise EditorialValueCarrierError("Editorial carrier execution/governance boundary drift")
    expected_approval = {
        "editorial_value_carrier_approved": False,
        "editorial_values_visually_consumed": False,
        "editorial_layout_approved": False,
        "editorial_visibility_windows_approved": False,
        "renderer_baseline_approved": False,
        "renderer_baseline_frozen": False,
        "d4_8_authorized": False,
        "d9_14": "BLOCKED_AS_REQUIRED",
        "d9_16": "BLOCKED_AS_REQUIRED",
        "d9_17": "BLOCKED_NO_GO",
        "d10": "BLOCKED",
        "release_authority": "NONE",
    }
    if contract.get("approval_state") != expected_approval:
        raise EditorialValueCarrierError("Editorial carrier may not approve layout, consumption or release")
    raw_lineage = contract.get("source_lineage")
    if not isinstance(raw_lineage, list) or len(raw_lineage) < 18:
        raise EditorialValueCarrierError("Carrier source lineage is incomplete")
    lineage: list[dict[str, str]] = []
    seen: set[str] = set()
    for row in raw_lineage:
        if not isinstance(row, Mapping) or set(row) != {"path", "sha256"}:
            raise EditorialValueCarrierError("Malformed carrier source-lineage row")
        rel, expected_hash = str(row["path"]), str(row["sha256"])
        path = Path(rel)
        if path.is_absolute() or ".." in path.parts or rel in seen or not _is_sha256(expected_hash):
            raise EditorialValueCarrierError(f"Unsafe, duplicate or malformed carrier source pin: {rel}")
        actual = _sha_file(root / path)
        if actual != expected_hash:
            raise EditorialValueCarrierError(f"Carrier source hash mismatch: {rel}")
        seen.add(rel)
        lineage.append({"path": path.as_posix(), "sha256": actual})
    if not lineage or lineage[0] != {"path": "release/C11C_FREEZE_PACKAGE_MANIFEST.json", "sha256": EXPECTED_MANIFEST_SHA256}:
        raise EditorialValueCarrierError("The immutable C11-C manifest must be the first source pin")
    if contract.get("supported_fields_by_content_type") != {key: list(value) for key, value in EXPECTED_FIELDS.items()}:
        raise EditorialValueCarrierError("Editorial field allowlist differs from canonical D9.9 routing declarations")
    return contract, schema, input_schema, lineage


def _validate_override_input(raw: Mapping[str, Any] | None, schema: Mapping[str, Any]) -> dict[str, dict[str, str]]:
    if raw is None:
        return {}
    if not isinstance(raw, Mapping):
        raise EditorialValueCarrierError("Editorial override input root must be an object")
    if raw.get("schema") != INPUT_SCHEMA_ID or raw.get("schema_version") != "1.0":
        raise EditorialValueCarrierError("Editorial override input identity/version mismatch")
    if set(raw) != {"schema", "schema_version", "values_by_content_type"}:
        raise EditorialValueCarrierError("Editorial override input has unknown/missing top-level properties")
    values = raw.get("values_by_content_type")
    if not isinstance(values, Mapping) or not values:
        raise EditorialValueCarrierError("values_by_content_type must contain at least one supported content type")
    if set(values) - set(CONTENT_TYPES):
        raise EditorialValueCarrierError("Only Challenges, Visual Loops and Visual Drills accept editorial overrides")
    clean: dict[str, dict[str, str]] = {}
    for content_type, field_map in values.items():
        if not isinstance(field_map, Mapping) or not field_map:
            raise EditorialValueCarrierError(f"Editorial override map must be a non-empty object: {content_type}")
        allowed = set(EXPECTED_FIELDS[str(content_type)])
        unknown = set(field_map) - allowed
        if unknown:
            raise EditorialValueCarrierError(f"Disabled/unknown editorial field(s) for {content_type}: {', '.join(sorted(map(str, unknown)))}")
        clean_map: dict[str, str] = {}
        for field, value in field_map.items():
            if not isinstance(field, str) or not isinstance(value, str):
                raise EditorialValueCarrierError(f"Editorial overrides must be string values: {content_type}.{field}")
            if len(value) > 160:
                raise EditorialValueCarrierError(f"Editorial override exceeds D9.9 max length: {content_type}.{field}")
            clean_map[field] = value
        clean[str(content_type)] = clean_map
    try:
        import jsonschema  # type: ignore
    except ImportError:
        jsonschema = None
    if jsonschema is not None:
        jsonschema.Draft202012Validator(schema).validate(dict(raw))
    return clean


def load_override_file(path: Path | str, root: Path | str | None = None) -> tuple[dict[str, dict[str, str]], str]:
    project_root = _root(root)
    _, _, input_schema, _ = _load_contract(project_root)
    try:
        raw = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EditorialValueCarrierError(f"Cannot read editorial override input JSON: {exc}") from exc
    clean = _validate_override_input(raw, input_schema)
    return clean, _sha_json({"schema": INPUT_SCHEMA_ID, "schema_version": "1.0", "values_by_content_type": clean})


def _chains_with_overrides(
    root: Path,
    materialization_contract: Mapping[str, Any],
    base_chains: Mapping[str, Mapping[str, Any]],
    overrides: Mapping[str, Mapping[str, str]],
) -> dict[str, dict[str, Any]]:
    fixtures = _fixture_requests(root)
    chains: dict[str, dict[str, Any]] = {}
    for content_type in CONTENT_TYPES:
        if content_type not in fixtures or content_type not in base_chains:
            raise EditorialValueCarrierError(f"Fixed base request fixture missing: {content_type}")
        raw = copy.deepcopy(dict(base_chains[content_type]["raw_request"]))
        raw["production_override"].update(dict(overrides.get(content_type, {})))
        try:
            result, bridge, envelope, source_binding = _request(raw, root)
        except (RequestScopedMaterializationBindingError, ValueError, TypeError, KeyError) as exc:
            raise EditorialValueCarrierError(f"Canonical D9.9 request chain rejected for {content_type}: {exc}") from exc
        fixture = fixtures[content_type]
        request = result.get("canonical_request", {})
        selection = request.get("selection", {}) if isinstance(request, Mapping) else {}
        if request.get("request_id") != fixture["request_id"]:
            raise EditorialValueCarrierError(f"Request ID changed outside the fixed fixture: {content_type}")
        if {key: selection.get(key) for key in fixture["selection"]} != fixture["selection"]:
            raise EditorialValueCarrierError(f"Editorial-only transport changed fixed content selection: {content_type}")
        if request.get("seed") != fixture["seed"] or request.get("music_seed") != 840001 or request.get("variation_index") != 0:
            raise EditorialValueCarrierError(f"Editorial-only transport changed seed/variation identity: {content_type}")
        if request.get("presentation_profile_id") != "social_default_v1" or request.get("delivery_profile_id") != "REVIEW_720":
            raise EditorialValueCarrierError(f"Editorial-only transport changed the fixed review profile: {content_type}")
        base_request = base_chains[content_type]["result"]["canonical_request"]
        base_non_editorial = copy.deepcopy(dict(base_request))
        current_non_editorial = copy.deepcopy(dict(request))
        base_non_editorial.pop("editorial", None)
        current_non_editorial.pop("editorial", None)
        if _canonical(base_non_editorial) != _canonical(current_non_editorial):
            raise EditorialValueCarrierError(f"Request differs from base fixture outside the editorial map: {content_type}")
        if not isinstance(request.get("editorial"), Mapping):
            raise EditorialValueCarrierError(f"Canonical D9.9 editorial map missing: {content_type}")
        if set(request["editorial"]) != set(EXPECTED_FIELDS[content_type]):
            raise EditorialValueCarrierError(f"Canonical D9.9 enabled field set changed: {content_type}")
        for field, value in request["editorial"].items():
            if not isinstance(value, str):
                raise EditorialValueCarrierError(f"Canonical D9.9 value is not a string: {content_type}.{field}")
        chains[content_type] = {
            "fixture": fixture,
            "raw_request": raw,
            "result": result,
            "bridge": bridge,
            "envelope": envelope,
            "source_binding": source_binding,
        }
    return chains


def _prevalidate_materialization_receipt_envelope(receipt: Mapping[str, Any]) -> None:
    """Reject forged/promoted receipts before the more expensive canonical chain rebuild."""
    if receipt.get("schema") != "C11-D-D9-RENDERER-REQUEST-SCOPED-PAYLOAD-MATERIALIZATION-BINDING-V1" or receipt.get("schema_version") != "1.0":
        raise EditorialValueCarrierError("Upstream materialization receipt identity/version mismatch")
    if receipt.get("status") != MATERIALIZATION_STATUS or receipt.get("frozen_c11c_manifest_sha256") != EXPECTED_MANIFEST_SHA256:
        raise EditorialValueCarrierError("Upstream receipt status or frozen C11-C pin mismatch")
    if receipt.get("candidate_input_admissible") is not False:
        raise EditorialValueCarrierError("Upstream materialization receipt falsely admits candidate input")
    if receipt.get("receipt_sha256") != _sha_json({key: value for key, value in receipt.items() if key != "receipt_sha256"}):
        raise EditorialValueCarrierError("Upstream materialization receipt digest mismatch")
    if receipt.get("readiness") != {
        "request_scoped_payload_instances_materialized": True,
        "bound_content_types": 3,
        "total_content_types": 3,
        "all_three_bound": True,
        "video_render_ready": False,
    }:
        raise EditorialValueCarrierError("Upstream receipt readiness boundary drift")
    boundary = receipt.get("execution_boundary", {})
    expected_boundary = {
        "payload_files_written": False,
        "renderer_native_input_emitted": False,
        "renderer_dispatch_invoked": False,
        "renderer_activation": False,
        "production_execution": False,
        "media_output_created": False,
        "output_artifact_path": None,
        "c11c_source_mutation": False,
        "d4_8": "BLOCKED",
        "release_authority": "NONE",
        "d9_14": "BLOCKED_AS_REQUIRED",
        "d9_16": "BLOCKED_AS_REQUIRED",
        "d9_17": "BLOCKED_NO_GO",
        "d10": "BLOCKED",
    }
    for key, expected in expected_boundary.items():
        if boundary.get(key) != expected:
            raise EditorialValueCarrierError(f"Upstream receipt execution boundary changed: {key}")


def _validate_materialization_receipt(
    receipt: Mapping[str, Any],
    base_chains: Mapping[str, Mapping[str, Any]],
) -> dict[str, dict[str, Any]]:
    if receipt.get("schema") != "C11-D-D9-RENDERER-REQUEST-SCOPED-PAYLOAD-MATERIALIZATION-BINDING-V1" or receipt.get("schema_version") != "1.0":
        raise EditorialValueCarrierError("Upstream materialization receipt identity/version mismatch")
    if receipt.get("status") != MATERIALIZATION_STATUS or receipt.get("frozen_c11c_manifest_sha256") != EXPECTED_MANIFEST_SHA256:
        raise EditorialValueCarrierError("Upstream receipt status or frozen C11-C pin mismatch")
    if receipt.get("candidate_input_admissible") is not False:
        raise EditorialValueCarrierError("Upstream materialization receipt falsely admits candidate input")
    if receipt.get("receipt_sha256") != _sha_json({key: value for key, value in receipt.items() if key != "receipt_sha256"}):
        raise EditorialValueCarrierError("Upstream materialization receipt digest mismatch")
    readiness = receipt.get("readiness")
    if readiness != {
        "request_scoped_payload_instances_materialized": True,
        "bound_content_types": 3,
        "total_content_types": 3,
        "all_three_bound": True,
        "video_render_ready": False,
    }:
        raise EditorialValueCarrierError("Upstream receipt readiness boundary drift")
    boundary = receipt.get("execution_boundary", {})
    for key, expected in {
        "payload_files_written": False,
        "renderer_native_input_emitted": False,
        "renderer_dispatch_invoked": False,
        "renderer_activation": False,
        "production_execution": False,
        "media_output_created": False,
        "output_artifact_path": None,
        "c11c_source_mutation": False,
        "d4_8": "BLOCKED",
        "release_authority": "NONE",
        "d9_14": "BLOCKED_AS_REQUIRED",
        "d9_16": "BLOCKED_AS_REQUIRED",
        "d9_17": "BLOCKED_NO_GO",
        "d10": "BLOCKED",
    }.items():
        if boundary.get(key) != expected:
            raise EditorialValueCarrierError(f"Upstream receipt execution boundary changed: {key}")
    rows = receipt.get("content_bindings")
    if not isinstance(rows, list) or len(rows) != 3:
        raise EditorialValueCarrierError("Upstream receipt must contain exactly three base payload bindings")
    expected_types = ["challenges", "visual_loops", "visual_drills"]
    if [row.get("content_type") for row in rows if isinstance(row, Mapping)] != expected_types:
        raise EditorialValueCarrierError("Upstream payload-binding order/coverage drift")
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        content_type = str(row["content_type"])
        if content_type not in base_chains or content_type in result:
            raise EditorialValueCarrierError(f"Unknown/duplicate upstream payload binding: {content_type}")
        expected_request_hash = base_chains[content_type]["result"]["request_hash"]
        if row.get("canonical_request_sha256") != expected_request_hash:
            raise EditorialValueCarrierError(f"Base fixture request hash mismatch in upstream payload receipt: {content_type}")
        if row.get("source_seed_matches_request") is not True or row.get("materialization") != "IN_MEMORY_ONLY" or row.get("deterministic_repeat_pass") is not True or row.get("video_render_ready") is not False:
            raise EditorialValueCarrierError(f"Upstream base payload readiness mismatch: {content_type}")
        if not _is_sha256(row.get("payload_instance_sha256")):
            raise EditorialValueCarrierError(f"Upstream payload digest malformed: {content_type}")
        if row.get("binding_sha256") != _sha_json({key: value for key, value in row.items() if key != "binding_sha256"}):
            raise EditorialValueCarrierError(f"Upstream payload-binding digest mismatch: {content_type}")
        base_fixture = base_chains[content_type]["fixture"]
        expected_identity = {
            "request_id": base_fixture["request_id"],
            "selection": base_fixture["selection"],
            "gameplay_seed": int(base_fixture["gameplay_seed"]),
            "music_seed": int(base_fixture["music_seed"]),
            "variation_index": int(base_fixture["variation_index"]),
            "presentation_profile_id": base_fixture["presentation_profile_id"],
            "delivery_profile_id": base_fixture["delivery_profile_id"],
        }
        for key, expected in expected_identity.items():
            if row.get(key) != expected:
                raise EditorialValueCarrierError(f"Upstream base payload identity differs from the fixed fixture ({key}): {content_type}")
        result[content_type] = dict(row)
    return result


def _load_and_validate_upstream_reviews(root: Path) -> tuple[str, dict[str, Any]]:
    # build_reconciliation internally runs and validates the existing field-consumption audit.
    # Capture the audit contract identity separately without redundantly rebuilding that report.
    try:
        routing = build_reconciliation(root)
    except (ValueError, TypeError, KeyError, OSError) as exc:
        raise EditorialValueCarrierError(f"Canonical editorial audit/routing review failed: {exc}") from exc
    summary = routing.get("summary", {})
    if (summary.get("field_instances_reviewed") != 14
            or summary.get("canonical_review_chain_parity") != "PASS_14_OF_14"
            or summary.get("current_visual_payload_consumption") != "ZERO_OF_14"):
        raise EditorialValueCarrierError("Upstream routing matrix no longer reports 14/14 parity and 0/14 visual consumption")
    if routing.get("approval_state", {}).get("editorial_field_window_policy_approved") is not False:
        raise EditorialValueCarrierError("Upstream editorial visibility policy was promoted")
    return _sha_file(root / AUDIT_CONTRACT_REL), routing


def build_carrier(
    materialization_receipt: Mapping[str, Any],
    *,
    root: Path | str | None = None,
    overrides: Mapping[str, Mapping[str, str]] | None = None,
    override_input_sha256: str | None = None,
) -> dict[str, Any]:
    project_root = _root(root)
    contract, schema, input_schema, lineage = _load_contract(project_root)
    materialization_contract, _, _ = _load_materialization_contract(project_root)
    clean_overrides = _validate_override_input(
        None if overrides is None or not overrides else {
            "schema": INPUT_SCHEMA_ID,
            "schema_version": "1.0",
            "values_by_content_type": {key: dict(value) for key, value in overrides.items()},
        },
        input_schema,
    )
    if override_input_sha256 is None:
        override_input_sha256 = _sha_json({"schema": INPUT_SCHEMA_ID, "schema_version": "1.0", "values_by_content_type": clean_overrides}) if clean_overrides else None
    elif not _is_sha256(override_input_sha256):
        raise EditorialValueCarrierError("Canonical override-input digest is malformed")
    expected_override_digest = _sha_json({"schema": INPUT_SCHEMA_ID, "schema_version": "1.0", "values_by_content_type": clean_overrides}) if clean_overrides else None
    if override_input_sha256 != expected_override_digest:
        raise EditorialValueCarrierError("Override-input digest does not match the canonical field values")

    _prevalidate_materialization_receipt_envelope(materialization_receipt)
    base_chains = _build_request_chains(project_root, materialization_contract)
    base_bindings = _validate_materialization_receipt(materialization_receipt, base_chains)
    audit_contract_sha256, routing = _load_and_validate_upstream_reviews(project_root)
    chains = base_chains if not clean_overrides else _chains_with_overrides(project_root, materialization_contract, base_chains, clean_overrides)

    content_bindings: list[dict[str, Any]] = []
    override_field_count = 0
    for content_type in CONTENT_TYPES:
        chain = chains[content_type]
        base_binding = base_bindings[content_type]
        canonical_request = chain["result"]["canonical_request"]
        base_request_hash = str(base_binding["canonical_request_sha256"])
        request_hash = str(chain["result"]["request_hash"])
        base_values = dict(base_chains[content_type]["result"]["canonical_request"]["editorial"])
        editorial_values = dict(canonical_request["editorial"])
        if set(editorial_values) != set(EXPECTED_FIELDS[content_type]):
            raise EditorialValueCarrierError(f"Enabled editorial field count/order changed: {content_type}")
        fields: list[dict[str, Any]] = []
        for field_name in EXPECTED_FIELDS[content_type]:
            value = editorial_values[field_name]
            if not isinstance(value, str):
                raise EditorialValueCarrierError(f"Canonical field value is not a string: {content_type}.{field_name}")
            field_override = field_name in clean_overrides.get(content_type, {})
            if field_override:
                override_field_count += 1
            fields.append({
                "field_name": field_name,
                "field_kind": FIELD_CLASS[field_name],
                "value": value,
                "value_sha256": _sha_text(value),
                "value_origin": "CANONICAL_D9_9_RESOLVED_EDITORIAL_MAP",
                "operator_override_supplied": field_override,
                "presentation_applied": False,
                "semantic_region_id": None,
                "layout_geometry": None,
                "visibility_window": None,
                "visual_payload_consumption_state": "NOT_CONSUMED",
            })
        base_request_non_editorial = copy.deepcopy(dict(base_chains[content_type]["result"]["canonical_request"]))
        request_non_editorial = copy.deepcopy(dict(canonical_request))
        base_request_non_editorial.pop("editorial", None)
        request_non_editorial.pop("editorial", None)
        editorial_only_delta = _canonical(base_request_non_editorial) == _canonical(request_non_editorial)
        if not editorial_only_delta:
            raise EditorialValueCarrierError(f"Override changed non-editorial request semantics: {content_type}")
        binding = {
            "content_type": content_type,
            "request_id": str(canonical_request["request_id"]),
            "canonical_request_sha256": request_hash,
            "base_materialization_request_sha256": base_request_hash,
            "request_hash_matches_base_materialization_request": request_hash == base_request_hash,
            "editorial_only_delta_from_base_request": True,
            "selection_seed_profile_match": True,
            "payload_instance_id": str(base_binding["payload_instance_id"]),
            "payload_instance_sha256": str(base_binding["payload_instance_sha256"]),
            "payload_linkage_basis": "BASE_REVIEW_PAYLOAD_HASH_AND_FIXED_SELECTOR_SEED_PROFILE",
            "payload_mutated": False,
            "editorial_values_injected_into_visual_payload": False,
            "visual_payload_consumed_editorial_text": False,
            "editorial_values_sha256": _sha_json(editorial_values),
            "fields": fields,
        }
        binding["carrier_binding_sha256"] = _sha_json(binding)
        content_bindings.append(binding)

    total_fields = sum(len(row["fields"]) for row in content_bindings)
    visual_fields = sum(1 for row in content_bindings for item in row["fields"] if item["field_kind"] == "VISUAL_TEXT")
    metadata_fields = total_fields - visual_fields
    runtime_identity = {
        "contract_path": CONTRACT_REL.as_posix(),
        "contract_sha256": _sha_file(project_root / CONTRACT_REL),
        "schema_path": SCHEMA_REL.as_posix(),
        "schema_sha256": _sha_file(project_root / SCHEMA_REL),
        "input_schema_path": INPUT_SCHEMA_REL.as_posix(),
        "input_schema_sha256": _sha_file(project_root / INPUT_SCHEMA_REL),
        "implementation_path": Path(__file__).resolve().relative_to(project_root).as_posix(),
        "implementation_sha256": _sha_file(Path(__file__).resolve()),
        "test_path": "tools/c11d/d9/test_d_renderer_request_scoped_editorial_value_carrier.py",
        "test_sha256": _sha_file(project_root / "tools/c11d/d9/test_d_renderer_request_scoped_editorial_value_carrier.py"),
    }
    receipt: dict[str, Any] = {
        "schema": OUTPUT_SCHEMA,
        "schema_version": "1.0",
        "status": OUTPUT_STATUS,
        "frozen_c11c_manifest_sha256": EXPECTED_MANIFEST_SHA256,
        "candidate_input_admissible": False,
        "runtime_identity": runtime_identity,
        "input": {
            "override_values_supplied": bool(clean_overrides),
            "override_input_sha256": override_input_sha256,
            "override_field_count": override_field_count,
            "canonical_d9_9_normalization_applied": True,
        },
        "upstream_review_identity": {
            "materialization_receipt_sha256": str(materialization_receipt["receipt_sha256"]),
            "editorial_audit_contract_sha256": audit_contract_sha256,
            "routing_reconciliation_sha256": str(routing["reconciliation_sha256"]),
        },
        "content_bindings": content_bindings,
        "summary": {
            "content_types": len(content_bindings),
            "enabled_editorial_field_instances": total_fields,
            "hash_bound_sidecar_field_values": total_fields,
            "visual_text_values_in_sidecar": visual_fields,
            "metadata_only_values_in_sidecar": metadata_fields,
            "visual_payload_text_consumed": 0,
            "payload_member_injection": False,
            "all_changes_editorial_only": True,
            "video_render_ready": False,
        },
        "unresolved_policy_gates": list(contract["unresolved_policy_gates"]),
        "source_lineage": lineage,
        "execution_boundary": dict(contract["execution_boundary"]),
        "approval_state": dict(contract["approval_state"]),
    }
    receipt["carrier_sha256"] = _sha_json(receipt)
    _validate_carrier(receipt, schema)
    return receipt


def _validate_carrier(receipt: Mapping[str, Any], schema: Mapping[str, Any]) -> None:
    if set(receipt) != set(schema.get("required", [])) or set(receipt) != set(schema.get("properties", {})):
        raise EditorialValueCarrierError("Carrier receipt top-level shape differs from strict schema")
    if receipt.get("schema") != OUTPUT_SCHEMA or receipt.get("schema_version") != "1.0" or receipt.get("status") != OUTPUT_STATUS:
        raise EditorialValueCarrierError("Carrier receipt identity/status mismatch")
    if receipt.get("frozen_c11c_manifest_sha256") != EXPECTED_MANIFEST_SHA256 or receipt.get("candidate_input_admissible") is not False:
        raise EditorialValueCarrierError("Carrier receipt frozen manifest/admission boundary mismatch")
    if receipt.get("carrier_sha256") != _sha_json({key: value for key, value in receipt.items() if key != "carrier_sha256"}):
        raise EditorialValueCarrierError("Carrier receipt digest mismatch")
    if receipt.get("execution_boundary") != {
        "mode": "IN_MEMORY_REVIEW_ONLY_SIDECAR",
        "payload_files_written": False,
        "receipt_files_written": False,
        "renderer_native_input_emitted": False,
        "renderer_dispatch_invoked": False,
        "renderer_activation": False,
        "production_execution": False,
        "media_output_created": False,
        "output_artifact_path": None,
        "payload_mutated": False,
        "editorial_values_injected_into_visual_payload": False,
        "c11c_source_mutation": False,
        "d4_8": "BLOCKED",
        "release_authority": "NONE",
        "d9_14": "BLOCKED_AS_REQUIRED",
        "d9_16": "BLOCKED_AS_REQUIRED",
        "d9_17": "BLOCKED_NO_GO",
        "d10": "BLOCKED",
    }:
        raise EditorialValueCarrierError("Carrier execution/governance boundary drift")
    expected_approval = {
        "editorial_value_carrier_approved": False,
        "editorial_values_visually_consumed": False,
        "editorial_layout_approved": False,
        "editorial_visibility_windows_approved": False,
        "renderer_baseline_approved": False,
        "renderer_baseline_frozen": False,
        "d4_8_authorized": False,
        "d9_14": "BLOCKED_AS_REQUIRED",
        "d9_16": "BLOCKED_AS_REQUIRED",
        "d9_17": "BLOCKED_NO_GO",
        "d10": "BLOCKED",
        "release_authority": "NONE",
    }
    if receipt.get("approval_state") != expected_approval:
        raise EditorialValueCarrierError("Carrier receipt falsely approves layout/visual consumption/release")
    bindings = receipt.get("content_bindings")
    if not isinstance(bindings, list) or [row.get("content_type") for row in bindings if isinstance(row, Mapping)] != list(CONTENT_TYPES):
        raise EditorialValueCarrierError("Carrier must contain exactly three ordered supported content bindings")
    seen_total = seen_visual = seen_metadata = 0
    for binding in bindings:
        if set(binding) != set(schema["$defs"]["content_binding"]["required"]):
            raise EditorialValueCarrierError("Carrier content binding shape mismatch")
        if binding.get("carrier_binding_sha256") != _sha_json({key: value for key, value in binding.items() if key != "carrier_binding_sha256"}):
            raise EditorialValueCarrierError("Carrier content-binding digest mismatch")
        if binding.get("editorial_only_delta_from_base_request") is not True or binding.get("selection_seed_profile_match") is not True:
            raise EditorialValueCarrierError("Carrier must keep non-editorial request identity exact")
        if binding.get("payload_mutated") is not False or binding.get("editorial_values_injected_into_visual_payload") is not False or binding.get("visual_payload_consumed_editorial_text") is not False:
            raise EditorialValueCarrierError("Carrier may not claim visual payload mutation or consumption")
        if not _is_sha256(binding.get("canonical_request_sha256")) or not _is_sha256(binding.get("base_materialization_request_sha256")) or not _is_sha256(binding.get("payload_instance_sha256")) or not _is_sha256(binding.get("editorial_values_sha256")):
            raise EditorialValueCarrierError("Carrier request/payload/editorial digest malformed")
        fields = binding.get("fields")
        content_type = str(binding["content_type"])
        if not isinstance(fields, list) or [field.get("field_name") for field in fields if isinstance(field, Mapping)] != list(EXPECTED_FIELDS[content_type]):
            raise EditorialValueCarrierError(f"Carrier field allowlist/order mismatch: {content_type}")
        values: dict[str, str] = {}
        for field in fields:
            expected_keys = set(schema["$defs"]["field_binding"]["required"])
            if set(field) != expected_keys:
                raise EditorialValueCarrierError("Carrier field binding shape mismatch")
            name = str(field["field_name"])
            value = field.get("value")
            expected_class = FIELD_CLASS.get(name)
            if not isinstance(value, str) or field.get("value_sha256") != _sha_text(value):
                raise EditorialValueCarrierError(f"Carrier value hash mismatch: {content_type}.{name}")
            if field.get("field_kind") != expected_class:
                raise EditorialValueCarrierError(f"Carrier field classification mismatch: {content_type}.{name}")
            if field.get("value_origin") != "CANONICAL_D9_9_RESOLVED_EDITORIAL_MAP" or field.get("presentation_applied") is not False or field.get("semantic_region_id") is not None or field.get("layout_geometry") is not None or field.get("visibility_window") is not None or field.get("visual_payload_consumption_state") != "NOT_CONSUMED":
                raise EditorialValueCarrierError(f"Carrier unexpectedly applies unresolved visual semantics: {content_type}.{name}")
            values[name] = value
            seen_total += 1
            if expected_class == "VISUAL_TEXT":
                seen_visual += 1
            else:
                seen_metadata += 1
                if name != "language":
                    raise EditorialValueCarrierError("Only language may be classified as metadata-only in this contract")
        if binding.get("editorial_values_sha256") != _sha_json(values):
            raise EditorialValueCarrierError("Aggregate editorial-values digest mismatch")
    if receipt.get("summary") != {
        "content_types": 3,
        "enabled_editorial_field_instances": 14,
        "hash_bound_sidecar_field_values": seen_total,
        "visual_text_values_in_sidecar": seen_visual,
        "metadata_only_values_in_sidecar": seen_metadata,
        "visual_payload_text_consumed": 0,
        "payload_member_injection": False,
        "all_changes_editorial_only": True,
        "video_render_ready": False,
    } or (seen_total, seen_visual, seen_metadata) != (14, 11, 3):
        raise EditorialValueCarrierError("Carrier summary misstates field counts or visual consumption")
    try:
        import jsonschema  # type: ignore
    except ImportError:
        jsonschema = None
    if jsonschema is not None:
        jsonschema.Draft202012Validator(schema).validate(dict(receipt))


def validate_carrier(
    candidate: Mapping[str, Any],
    materialization_receipt: Mapping[str, Any],
    *,
    root: Path | str | None = None,
    overrides: Mapping[str, Mapping[str, str]] | None = None,
    override_input_sha256: str | None = None,
) -> bool:
    project_root = _root(root)
    _, schema, _, _ = _load_contract(project_root)
    _validate_carrier(candidate, schema)
    expected = build_carrier(
        materialization_receipt,
        root=project_root,
        overrides=overrides,
        override_input_sha256=override_input_sha256,
    )
    if dict(candidate) != expected:
        raise EditorialValueCarrierError("Carrier receipt differs from canonical D9.9 values and the bound base payload review")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Bind canonical D9.9 editorial values to fixed, in-memory payload references as a D-owned sidecar; no visual rendering or renderer input.")
    parser.add_argument("--godot", default=None, help="Godot 4.7.1 console executable or command on PATH")
    parser.add_argument("--timeout", type=int, default=120, help="Per-harness timeout seconds (1..900)")
    parser.add_argument("--editorial-values-file", default=None, help="Optional strict JSON file with enabled field overrides only; does not alter payload bytes")
    parser.add_argument("--root", default=None, help="Project root; defaults to this checkout")
    args = parser.parse_args()
    project_root = _root(args.root)
    try:
        overrides: dict[str, dict[str, str]] = {}
        override_digest: str | None = None
        if args.editorial_values_file:
            overrides, override_digest = load_override_file(args.editorial_values_file, project_root)
        materialization_receipt = run_materialization_review(project_root, executable=args.godot, timeout_seconds=args.timeout)
        carrier = build_carrier(
            materialization_receipt,
            root=project_root,
            overrides=overrides,
            override_input_sha256=override_digest,
        )
    except (EditorialValueCarrierError, RequestScopedMaterializationBindingError, ValueError, TypeError, KeyError, OSError) as exc:
        print(f"C11-D REQUEST-SCOPED EDITORIAL VALUE CARRIER FAIL | {exc}", file=sys.stderr)
        return 1
    print(
        "C11-D REQUEST-SCOPED EDITORIAL VALUE CARRIER PASS"
        f" | content_types={carrier['summary']['content_types']}/3"
        f" | sidecar_fields={carrier['summary']['hash_bound_sidecar_field_values']}/14"
        f" | visual_text_sidecar={carrier['summary']['visual_text_values_in_sidecar']}/11"
        f" | visual_payload_consumed={carrier['summary']['visual_payload_text_consumed']}/14"
        f" | payload_member_injection=false | renderer_input=NOT_EMITTED | renderer=OFF"
        " | media_created=false | D4.8=BLOCKED | release_authority=NONE"
    )
    print("C11-D REQUEST-SCOPED EDITORIAL VALUE CARRIER RECEIPT=" + _canonical(carrier))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
