"""Audit the boundary between canonical D9.9 editorial values and current payloads.

The tool is read-only. It builds the three pinned review chains in memory,
revalidates exact editorial text/hash parity in the renderer-neutral review
manifest, and confirms that current fixed Godot payload harness sources do not
expose those fields as payload members. It never emits renderer input or media.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from d_renderer_editorial_review_manifest import build_editorial_review_manifest
from d_renderer_request_scoped_payload_materialization_binding import (
    _build_request_chains,
    _load_contract as _load_materialization_contract,
)

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_EDITORIAL_FIELD_CONSUMPTION_AUDIT_V1.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_EDITORIAL_FIELD_CONSUMPTION_AUDIT_SCHEMA_V1.json")
MANIFEST_REL = Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")
MODEL_REL = Path("definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json")
EXPECTED_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
CONTRACT_SCHEMA = "C11-D-RENDERER-EDITORIAL-FIELD-CONSUMPTION-AUDIT-CONTRACT-V1"
OUTPUT_SCHEMA = "C11-D-D9-RENDERER-EDITORIAL-FIELD-CONSUMPTION-AUDIT-V1"
STATUS = "PREPARATION_ONLY_FIELD_CONSUMPTION_GAP_AUDIT_REVIEW_CHAIN_ONLY"
SUPPORTED_TYPES = ("challenges", "visual_loops", "visual_drills")
PAYLOAD_HARNESS_BY_TYPE = {
    "challenges": "tools/c11d/d9/materialize_challenge_visual_payload_in_memory.gd",
    "visual_loops": "tools/c11d/d9/materialize_visual_payloads_in_memory.gd",
    "visual_drills": "tools/c11d/d9/materialize_visual_payloads_in_memory.gd",
}


class EditorialFieldConsumptionAuditError(ValueError):
    """Raised for source drift, incomplete field parity, or a false readiness claim."""


def _root(project_root: Path | str | None = None) -> Path:
    return Path(project_root).resolve() if project_root is not None else Path(__file__).resolve().parents[3]


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _sha(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _read_json(root: Path, rel: str | Path) -> dict[str, Any]:
    try:
        value = json.loads((root / rel).read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise EditorialFieldConsumptionAuditError(f"Cannot read JSON source {rel}: {exc}") from exc
    if not isinstance(value, dict):
        raise EditorialFieldConsumptionAuditError(f"Expected JSON object at {rel}")
    return value


def _sha_file(path: Path) -> str:
    try:
        return _sha_bytes(path.read_bytes())
    except Exception as exc:
        raise EditorialFieldConsumptionAuditError(f"Cannot hash required source {path}: {exc}") from exc


def _load_contract(root: Path) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, str]]]:
    contract = _read_json(root, CONTRACT_REL)
    schema = _read_json(root, SCHEMA_REL)
    if contract.get("schema") != CONTRACT_SCHEMA or contract.get("schema_version") != "1.0":
        raise EditorialFieldConsumptionAuditError("Editorial field-consumption audit contract identity/version mismatch")
    if contract.get("status") != "PREPARATION_ONLY_FIELD_CONSUMPTION_GAP_AUDIT_NOT_RENDERER_INPUT":
        raise EditorialFieldConsumptionAuditError("Audit contract cannot self-promote")
    if contract.get("scope", {}).get("content_types") != list(SUPPORTED_TYPES):
        raise EditorialFieldConsumptionAuditError("Supported content-type scope drift")
    if contract.get("scope", {}).get("dynamic_request_transport") != "NOT_IMPLEMENTED":
        raise EditorialFieldConsumptionAuditError("Audit cannot claim dynamic request transport")
    if contract.get("scope", {}).get("renderer_native_input") != "NOT_EMITTED":
        raise EditorialFieldConsumptionAuditError("Audit cannot emit renderer-native input")
    if _sha_file(root / MANIFEST_REL) != EXPECTED_MANIFEST_SHA256:
        raise EditorialFieldConsumptionAuditError("Frozen C11-C manifest SHA-256 mismatch")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or schema.get("$id") != "urn:c11d:renderer-editorial-field-consumption-audit:v1":
        raise EditorialFieldConsumptionAuditError("Audit receipt schema identity mismatch")
    if schema.get("additionalProperties") is not False or set(schema.get("required", [])) != set(schema.get("properties", {})):
        raise EditorialFieldConsumptionAuditError("Audit receipt schema must be strict and exact at top-level")

    boundary = {
        "mode": "IN_MEMORY_AUDIT_ONLY", "payload_files_written": False, "receipt_files_written": False,
        "renderer_native_input_emitted": False, "renderer_dispatch_invoked": False, "renderer_activation": False,
        "production_execution": False, "media_output_created": False, "output_artifact_path": None,
        "c11c_source_mutation": False, "d4_8": "BLOCKED", "release_authority": "NONE",
    }
    approval = {
        "audit_contract_approved": False, "editorial_values_visually_consumed": False,
        "editorial_layout_approved": False, "editorial_visibility_windows_approved": False,
        "renderer_baseline_approved": False, "renderer_baseline_frozen": False, "d4_8_authorized": False,
        "d9_14": "BLOCKED_AS_REQUIRED", "d9_16": "BLOCKED_AS_REQUIRED", "d9_17": "BLOCKED_NO_GO",
        "d10": "BLOCKED", "release_authority": "NONE",
    }
    if contract.get("execution_boundary") != boundary or contract.get("approval_state") != approval:
        raise EditorialFieldConsumptionAuditError("Audit governance locks drifted or were promoted")

    raw = contract.get("source_lineage")
    if not isinstance(raw, list) or len(raw) < 18:
        raise EditorialFieldConsumptionAuditError("Audit source lineage is incomplete")
    lineage: list[dict[str, str]] = []
    seen: set[str] = set()
    for row in raw:
        if not isinstance(row, Mapping) or set(row) != {"path", "sha256"}:
            raise EditorialFieldConsumptionAuditError("Malformed source-lineage row")
        rel = str(row["path"])
        if rel in seen:
            raise EditorialFieldConsumptionAuditError(f"Duplicate source-lineage path: {rel}")
        actual = _sha_file(root / rel)
        if actual != str(row["sha256"]):
            raise EditorialFieldConsumptionAuditError(f"Pinned audit source drift: {rel}")
        lineage.append({"path": rel, "sha256": actual})
        seen.add(rel)
    if not lineage or lineage[0]["path"] != str(MANIFEST_REL).replace("\\", "/"):
        raise EditorialFieldConsumptionAuditError("Frozen C11-C manifest must be the first lineage pin")

    model = _read_json(root, MODEL_REL)
    expected_enabled = []
    expected_disabled = []
    for field, spec in model.get("editorial_fields", {}).items():
        if spec.get("enabled") is True:
            expected_enabled.append({
                "field": field,
                "content_types": spec.get("content_types", []),
                "current_visual_payload_consumption": "NOT_CONSUMED_BY_CURRENT_IN_MEMORY_VISUAL_PAYLOAD_HARNESS",
                "review_chain_state": "LANGUAGE_METADATA_ONLY" if field == "language" else "EXACT_VALUE_AND_SHA256_PARITY_IN_REVIEW_MANIFEST",
                "layout_state": "UNRESOLVED_NO_COORDINATES",
                "temporal_state": "NOT_SCHEDULED_NO_FRAME_RANGE",
            })
        elif spec.get("enabled") is False:
            expected_disabled.append({"field": field, "status": spec.get("status", "DISABLED"), "content_types": spec.get("content_types", [])})
    if contract.get("field_classification", {}).get("enabled_fields") != expected_enabled:
        raise EditorialFieldConsumptionAuditError("Enabled-field matrix differs from the canonical universal editorial model")
    if contract.get("field_classification", {}).get("disabled_reserved_fields") != expected_disabled:
        raise EditorialFieldConsumptionAuditError("Reserved-field matrix differs from the canonical universal editorial model")
    if contract.get("field_classification", {}).get("expected_payload_consumption") != "NOT_CONSUMED_BY_CURRENT_IN_MEMORY_VISUAL_PAYLOAD_HARNESS":
        raise EditorialFieldConsumptionAuditError("Audit cannot claim current visual-payload consumption")
    return contract, schema, lineage


def _payload_field_scan(root: Path, content_type: str, enabled_fields: list[str], contract: Mapping[str, Any]) -> dict[str, Any]:
    rel = PAYLOAD_HARNESS_BY_TYPE[content_type]
    text = (root / rel).read_text(encoding="utf-8-sig")
    scanned_keys = list(contract["field_classification"]["payload_field_scan_keys"])
    editorial_keys: list[str] = []
    # The scan concerns literal payload-object members, not arbitrary prose or local variable names.
    for field in scanned_keys:
        if re.search(rf'(?m)^\s*"{re.escape(field)}"\s*:', text):
            editorial_keys.append(field)
    # Any literal key match means the previously audited consumer boundary has changed;
    # fail closed and require a reviewed update to this audit contract.
    if editorial_keys:
        raise EditorialFieldConsumptionAuditError(
            f"Payload harness now declares editorial field key(s) requiring re-audit for {content_type}: {', '.join(editorial_keys)}"
        )
    return {"scanned_keys": scanned_keys, "editorial_keys_found": [], "no_editorial_value_keys_found": True}


def _build_report(project_root: Path | str | None = None) -> dict[str, Any]:
    root = _root(project_root)
    contract, schema, lineage = _load_contract(root)
    materialization_contract, _, _ = _load_materialization_contract(root)
    chains = _build_request_chains(root, materialization_contract)
    model = _read_json(root, MODEL_REL)
    results: list[dict[str, Any]] = []
    total_fields = 0
    total_review_values = 0
    for content_type in SUPPORTED_TYPES:
        chain = chains[content_type]
        result = chain["result"]
        plan = result.get("plan", {})
        editorial = plan.get("editorial", {})
        if not isinstance(editorial, Mapping):
            raise EditorialFieldConsumptionAuditError(f"Canonical D9.9 editorial values missing for {content_type}")
        model_fields = model.get("content_types", {}).get(content_type, {}).get("editable_fields", [])
        if not isinstance(model_fields, list) or set(editorial) != set(model_fields):
            raise EditorialFieldConsumptionAuditError(f"Canonical request/editorial model field coverage mismatch for {content_type}")
        review_manifest = build_editorial_review_manifest(result, chain["bridge"], chain["envelope"], root)
        instructions = review_manifest.get("editorial_fields", [])
        instruction_by_field = {str(row.get("source_field")): row for row in instructions}
        expected_instruction_fields = set(editorial) - {"language"}
        if len(instruction_by_field) != len(instructions) or set(instruction_by_field) != expected_instruction_fields:
            raise EditorialFieldConsumptionAuditError(f"Frame-program instruction field coverage mismatch for {content_type}")
        for row in instructions:
            field = str(row["source_field"])
            if row.get("text_value") != editorial.get(field) or row.get("text_sha256") != _sha(editorial.get(field)):
                raise EditorialFieldConsumptionAuditError(f"Review frame-program text/hash differs from canonical plan: {content_type}.{field}")
            if row.get("target_mapping_state") != "PROPOSED_NOT_APPROVED" or row.get("layout_binding_state") != "UNRESOLVED_NO_COORDINATES" or row.get("temporal_binding_state") != "NOT_SCHEDULED_NO_FRAME_RANGE" or row.get("visibility_frame_range") is not None:
                raise EditorialFieldConsumptionAuditError(f"Editorial layout/timing state was promoted for {content_type}.{field}")
        if any(row.get("language") != editorial.get("language") for row in instructions):
            raise EditorialFieldConsumptionAuditError(f"Canonical language metadata mismatch in review instructions for {content_type}")

        enabled_fields: list[str] = list(model_fields)
        field_records: list[dict[str, Any]] = []
        for field in enabled_fields:
            value = editorial.get(field)
            if not isinstance(value, str):
                raise EditorialFieldConsumptionAuditError(f"Canonical editable value is not a string: {content_type}.{field}")
            if field == "language":
                review_state = "LANGUAGE_METADATA_ONLY"
            else:
                reviewed = instruction_by_field.get(field)
                if not isinstance(reviewed, Mapping):
                    raise EditorialFieldConsumptionAuditError(f"Canonical editorial field absent from review manifest: {content_type}.{field}")
                review_state = "EXACT_VALUE_AND_SHA256_PARITY_IN_REVIEW_MANIFEST"
            field_records.append({
                "field": field,
                "value_sha256": _sha(value),
                "canonical_request_state": "EXACT_VALUE_PRESENT_IN_CANONICAL_D9_9_PLAN",
                "review_chain_state": review_state,
                "visual_payload_consumption_state": "NOT_CONSUMED_BY_CURRENT_IN_MEMORY_VISUAL_PAYLOAD_HARNESS",
                "layout_state": "UNRESOLVED_NO_COORDINATES",
                "temporal_state": "NOT_SCHEDULED_NO_FRAME_RANGE",
                "visibility_frame_range": None,
            })
        scan = _payload_field_scan(root, content_type, enabled_fields, contract)
        results.append({
            "content_type": content_type,
            "request_id": str(result["canonical_request"]["request_id"]),
            "canonical_request_sha256": str(result["request_hash"]),
            "plan_sha256": str(result["plan_hash"]),
            "review_manifest_sha256": str(review_manifest["review_manifest_sha256"]),
            "payload_harness_path": PAYLOAD_HARNESS_BY_TYPE[content_type],
            "payload_field_scan": scan,
            "canonical_editorial_field_count": len(enabled_fields),
            "review_instruction_field_count": len(instructions),
            "editorial_fields": field_records,
            "canonical_review_parity": "PASS",
            "visual_payload_consumption_complete": False,
            "video_render_ready": False,
        })
        total_fields += len(field_records)
        total_review_values += len(field_records)

    if [row["content_type"] for row in results] != list(SUPPORTED_TYPES):
        raise EditorialFieldConsumptionAuditError("Content-type result coverage/order is not canonical")
    boundary = copy.deepcopy(contract["execution_boundary"])
    approval = copy.deepcopy(contract["approval_state"])
    report: dict[str, Any] = {
        "schema": OUTPUT_SCHEMA,
        "schema_version": "1.0",
        "status": STATUS,
        "frozen_c11c_manifest_sha256": EXPECTED_MANIFEST_SHA256,
        "audit_contract_sha256": _sha_file(root / CONTRACT_REL),
        "implementation_sha256": _sha_file(Path(__file__).resolve()),
        "source_lineage": lineage,
        "content_results": results,
        "summary": {
            "supported_content_types": 3,
            "content_types_reviewed": len(results),
            "enabled_field_instances": total_fields,
            "exact_review_chain_field_instances": total_review_values,
            "visual_payload_consumed_field_instances": 0,
            "all_canonical_review_values_match": True,
            "visual_payload_consumption_complete": False,
            "candidate_input_admissible": False,
        },
        "unresolved_gaps": [
            "DYNAMIC_REQUEST_TRANSPORT_NOT_IMPLEMENTED_FIXED_REVIEW_FIXTURES_ONLY",
            "EDITORIAL_VALUES_ARE_CARRIED_IN_D9_9_PLAN_AND_REVIEW_MANIFEST_BUT_NOT_CONSUMED_BY_CURRENT_VISUAL_PAYLOAD_HARNESSES",
            "SEMANTIC_REGION_COORDINATES_REMAIN_UNRESOLVED_AND_UNAPPROVED",
            "PER_FIELD_VISIBILITY_FRAME_WINDOWS_REMAIN_UNRESOLVED_AND_UNAPPROVED",
            "CHALLENGE_RUNTIME_PAYLOAD_IDENTITY_IS_NOT_A_NATIVE_REQUEST_SCOPED_INSTANCE_ID",
            "RENDERER_IMPLEMENTATION_BASELINE_APPROVAL_AND_D4_8_AUTHORIZATION_REMAIN_BLOCKED",
        ],
        "execution_boundary": boundary,
        "approval_state": approval,
    }
    report["audit_sha256"] = _sha(report)
    return report


def _validate_schema(report: Mapping[str, Any], schema: Mapping[str, Any]) -> None:
    if set(report) != set(schema.get("required", [])) or set(report) != set(schema.get("properties", {})):
        raise EditorialFieldConsumptionAuditError("Audit receipt top-level shape differs from strict schema")
    if report.get("schema") != OUTPUT_SCHEMA or report.get("schema_version") != "1.0" or report.get("status") != STATUS:
        raise EditorialFieldConsumptionAuditError("Audit receipt identity/status mismatch")
    digest = report.get("audit_sha256")
    if digest != _sha({k: v for k, v in report.items() if k != "audit_sha256"}):
        raise EditorialFieldConsumptionAuditError("Audit receipt SHA-256 mismatch")
    if report.get("frozen_c11c_manifest_sha256") != EXPECTED_MANIFEST_SHA256:
        raise EditorialFieldConsumptionAuditError("Audit receipt frozen manifest mismatch")
    summary = report.get("summary", {})
    if summary != {
        "supported_content_types": 3, "content_types_reviewed": 3,
        "enabled_field_instances": 14, "exact_review_chain_field_instances": 14,
        "visual_payload_consumed_field_instances": 0, "all_canonical_review_values_match": True,
        "visual_payload_consumption_complete": False, "candidate_input_admissible": False,
    }:
        raise EditorialFieldConsumptionAuditError("Audit summary falsely claims field consumption or readiness")
    if len(report.get("content_results", [])) != 3:
        raise EditorialFieldConsumptionAuditError("Audit must cover exactly the three supported content types")
    for result in report["content_results"]:
        if result.get("visual_payload_consumption_complete") is not False or result.get("video_render_ready") is not False:
            raise EditorialFieldConsumptionAuditError("Audit result falsely promotes visual consumption or readiness")
        fields = result.get("editorial_fields", [])
        if len(fields) != result.get("canonical_editorial_field_count"):
            raise EditorialFieldConsumptionAuditError("Editorial field count mismatch")
        for row in fields:
            if row.get("visual_payload_consumption_state") != "NOT_CONSUMED_BY_CURRENT_IN_MEMORY_VISUAL_PAYLOAD_HARNESS":
                raise EditorialFieldConsumptionAuditError("An editorial field was falsely marked as visually consumed")
            if row.get("visibility_frame_range") is not None or row.get("layout_state") != "UNRESOLVED_NO_COORDINATES" or row.get("temporal_state") != "NOT_SCHEDULED_NO_FRAME_RANGE":
                raise EditorialFieldConsumptionAuditError("An unresolved editorial layout/timing field was promoted")
    try:
        import jsonschema  # type: ignore
    except ImportError:
        jsonschema = None
    if jsonschema is not None:
        jsonschema.Draft202012Validator(schema).validate(dict(report))


def build_audit(project_root: Path | str | None = None) -> dict[str, Any]:
    root = _root(project_root)
    report = _build_report(root)
    _, schema, _ = _load_contract(root)
    _validate_schema(report, schema)
    return report


def validate_audit(candidate: Mapping[str, Any], project_root: Path | str | None = None) -> bool:
    root = _root(project_root)
    _, schema, _ = _load_contract(root)
    _validate_schema(candidate, schema)
    expected = _build_report(root)
    if dict(candidate) != expected:
        raise EditorialFieldConsumptionAuditError("Audit receipt differs from canonical request/review/harness gap evidence")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit D9.9 editorial values versus review-manifest parity and current visual payload consumption; read-only.")
    parser.add_argument("--root", default=None, help="Project root; defaults to this checkout")
    args = parser.parse_args()
    try:
        report = build_audit(args.root)
    except (EditorialFieldConsumptionAuditError, ValueError, TypeError, KeyError, OSError) as exc:
        print(f"C11-D EDITORIAL FIELD CONSUMPTION AUDIT FAIL | {exc}", file=sys.stderr)
        return 1
    print(
        "C11-D EDITORIAL FIELD CONSUMPTION GAP AUDIT PASS"
        f" | content_types={report['summary']['content_types_reviewed']}/3"
        f" | editorial_field_instances={report['summary']['enabled_field_instances']}"
        f" | review_chain_parity={report['summary']['exact_review_chain_field_instances']}/14"
        " | visual_payload_consumed=0/14 | video_render_ready=false"
        " | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE"
    )
    print("C11-D EDITORIAL FIELD CONSUMPTION AUDIT RECEIPT=" + _canonical(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
