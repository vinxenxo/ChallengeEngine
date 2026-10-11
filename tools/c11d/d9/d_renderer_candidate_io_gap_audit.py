"""Read-only, source-pinned gap audit for the prospective C11-D renderer I/O interface.

This tool never builds a candidate input, output manifest, renderer-native input, or media.
"""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path
from typing import Any, Mapping

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_CANDIDATE_IO_GAP_AUDIT_V1.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_CANDIDATE_IO_GAP_AUDIT_SCHEMA_V1.json")
IO_CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_CANDIDATE_IO_CONTRACT_V1.json")
INPUT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_CANDIDATE_INPUT_SCHEMA_V1.json")
OUTPUT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_CANDIDATE_OUTPUT_MANIFEST_SCHEMA_V1.json")
EXPECTED_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
CONTRACT_ID = "C11-D-RENDERER-CANDIDATE-IO-CONFORMANCE-GAP-AUDIT-V1"
REPORT_ID = "C11-D-D9-RENDERER-CANDIDATE-IO-GAP-AUDIT-REPORT-V1"
REPORT_STATUS = "READ_ONLY_SOURCE_PINNED_GAP_AUDIT_PASS_NOT_READINESS_PASS"
GROUPS = ("content_identity", "source_lineage", "payload_instance", "seed_domains", "editorial", "presentation", "timeline", "audio", "delivery", "authorization")

class IOGapAuditError(ValueError):
    """Raised when source evidence, contract state, or a report violates fail-closed expectations."""

def _root(root: Path | str | None = None) -> Path:
    if root is not None:
        return Path(root).resolve()
    return HERE.parents[2]

def _json(root: Path, rel: Path) -> dict[str, Any]:
    try:
        value = json.loads((root / rel).read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise IOGapAuditError(f"Cannot read source JSON {rel}: {exc}") from exc
    if not isinstance(value, dict):
        raise IOGapAuditError(f"Expected object at {rel}")
    return value

def _sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def _sha_json(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

def _safe_rel(raw: Any) -> Path:
    if not isinstance(raw, str) or not raw:
        raise IOGapAuditError("Source pin path must be a non-empty string")
    p = Path(raw)
    if p.is_absolute() or ".." in p.parts or "\\" in raw:
        raise IOGapAuditError(f"Unsafe source pin path: {raw}")
    return p

def _load(root: Path):
    contract = _json(root, CONTRACT_REL)
    schema = _json(root, SCHEMA_REL)
    if contract.get("schema") != CONTRACT_ID or contract.get("schema_version") != "1.0":
        raise IOGapAuditError("Gap-audit contract identity/version mismatch")
    if contract.get("status") != "READ_ONLY_INTERFACE_CONFORMANCE_AUDIT_NOT_ADMISSION_NOT_APPROVAL":
        raise IOGapAuditError("Gap-audit contract may not be promoted or repurposed")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or schema.get("$id") != "urn:c11d:renderer-candidate-io-gap-audit:v1" or schema.get("additionalProperties") is not False:
        raise IOGapAuditError("Gap-audit report schema identity/strictness mismatch")
    if schema.get("properties", {}).get("candidate_input_admissible", {}).get("const") is not False:
        raise IOGapAuditError("Report schema must keep candidate input inadmissible")
    rules = contract.get("audit_rules", {})
    if rules.get("expected_io_contract_status") != "PREPARATION_ONLY_INTERFACE_PROPOSAL_NOT_IMPLEMENTED_NOT_APPROVED":
        raise IOGapAuditError("Prospective I/O contract must remain a non-approved proposal")
    governance = contract.get("governance", {})
    expected_governance = {
        "candidate_input_admissible": False, "renderer_input_instance_emitted": False,
        "renderer_output_manifest_created": False, "renderer_implementation_added": False,
        "renderer_dispatch_invoked": False, "renderer_activation": False, "production_execution": False,
        "media_created": False, "d4_8": "BLOCKED", "release_authority": "NONE",
        "d9_14": "BLOCKED_AS_REQUIRED", "d9_16": "BLOCKED_AS_REQUIRED",
        "d9_17": "BLOCKED_NO_GO", "d10": "BLOCKED", "c11c_source_mutation": False,
    }
    if governance != expected_governance:
        raise IOGapAuditError("Audit contract crossed a renderer/production/governance boundary")
    raw_pins = contract.get("source_pins")
    if not isinstance(raw_pins, list) or len(raw_pins) < 32:
        raise IOGapAuditError("I/O gap audit needs its full source-pinned evidence set")
    seen: set[str] = set()
    verified: list[dict[str, str]] = []
    for row in raw_pins:
        if not isinstance(row, Mapping) or set(row) != {"path", "role", "sha256"}:
            raise IOGapAuditError("Malformed source pin row")
        rel = _safe_rel(row["path"])
        if rel.as_posix() in seen:
            raise IOGapAuditError(f"Duplicate source pin: {rel}")
        seen.add(rel.as_posix())
        exp = row["sha256"]
        if not isinstance(exp, str) or len(exp) != 64 or any(c not in "0123456789abcdef" for c in exp):
            raise IOGapAuditError(f"Malformed source hash: {rel}")
        path = root / rel
        if not path.is_file():
            raise IOGapAuditError(f"Pinned source missing: {rel}")
        actual = _sha_file(path)
        if actual != exp:
            raise IOGapAuditError(f"Pinned source drift: {rel}")
        verified.append({"path": rel.as_posix(), "role": str(row["role"]), "sha256": actual})
    if verified[0]["path"] != "release/C11C_FREEZE_PACKAGE_MANIFEST.json" or verified[0]["sha256"] != EXPECTED_MANIFEST_SHA256:
        raise IOGapAuditError("Immutable C11-C manifest must be the first exact source pin")
    if contract.get("source_of_truth", {}).get("frozen_c11c_manifest_sha256") != EXPECTED_MANIFEST_SHA256:
        raise IOGapAuditError("Frozen manifest authority mismatch")
    io_contract = _json(root, IO_CONTRACT_REL)
    input_schema = _json(root, INPUT_SCHEMA_REL)
    output_schema = _json(root, OUTPUT_SCHEMA_REL)
    if io_contract.get("status") != rules["expected_io_contract_status"]:
        raise IOGapAuditError("Prospective I/O contract status drift")
    if io_contract.get("boundary_state", {}).get("renderer_input_instance_emitted") is not False or io_contract.get("boundary_state", {}).get("renderer_output_manifest_created") is not False or io_contract.get("boundary_state", {}).get("renderer_implementation_added") is not False or io_contract.get("boundary_state", {}).get("renderer_dispatch_invoked") is not False:
        raise IOGapAuditError("Prospective I/O contract boundary has been promoted")
    if io_contract.get("current_admission_state", {}).get("candidate_input_admissible") is not False:
        raise IOGapAuditError("Candidate input must remain inadmissible")
    if input_schema.get("$id") != rules["expected_input_schema_id"] or output_schema.get("$id") != rules["expected_output_schema_id"]:
        raise IOGapAuditError("I/O schema IDs differ from the reviewed interface")
    schema_groups = [key for key in input_schema.get("properties", {}) if key not in {"schema", "schema_version"}]
    if schema_groups != list(GROUPS) or set(input_schema.get("required", [])) != {"schema", "schema_version", *GROUPS}:
        raise IOGapAuditError("The prospective input schema must retain exactly the ten reviewed required groups")
    assessments = contract.get("input_group_assessments")
    if not isinstance(assessments, list) or [row.get("group") for row in assessments] != list(GROUPS):
        raise IOGapAuditError("Input-group audit must cover the schema's ten required groups in canonical order")
    for row in assessments:
        expected_fields = list(input_schema["properties"][row["group"]].get("required", []))
        if row.get("schema_fields") != expected_fields or row.get("complete_for_input_emission") is not False:
            raise IOGapAuditError(f"Audit assessment does not match prospective required fields: {row.get('group')}")
    fixed_materialization = _json(root, Path("definitions/c11d/production/D_RENDERER_REQUEST_SCOPED_PAYLOAD_MATERIALIZATION_BINDING_V1.json"))
    carrier = _json(root, Path("definitions/c11d/production/D_RENDERER_REQUEST_SCOPED_EDITORIAL_VALUE_CARRIER_V1.json"))
    if fixed_materialization.get("status") != rules["require_fixed_payload_status"] or fixed_materialization.get("candidate_input_admissible") is not False:
        raise IOGapAuditError("Payload evidence no longer reflects fixed-fixture prepare-only status")
    if carrier.get("status") != rules["require_editorial_sidecar_status"] or carrier.get("candidate_input_admissible") is not False:
        raise IOGapAuditError("Editorial carrier is no longer a non-admissible sidecar")
    approval_state = carrier.get("approval_state", {})
    if approval_state.get("editorial_values_visually_consumed") is not False or approval_state.get("editorial_visibility_windows_approved") is not False:
        raise IOGapAuditError("Editorial sidecar may not imply visual consumption or approved windows")
    routing = _json(root, Path("definitions/c11d/production/D_RENDERER_EDITORIAL_FIELD_ROUTING_VISIBILITY_RECONCILIATION_V1.json"))
    if routing.get("approval_state", {}).get("editorial_values_visually_consumed") is not False:
        raise IOGapAuditError("Editorial routing must continue to report zero visual consumption")
    return contract, schema, io_contract, input_schema, output_schema, verified

def _build_report(root: Path) -> dict[str, Any]:
    contract, schema, io_contract, input_schema, output_schema, verified = _load(root)
    groups = [dict(row) for row in contract["input_group_assessments"]]
    partial = sum(1 for row in groups if str(row["state"]).startswith("PARTIAL_"))
    blocked = sum(1 for row in groups if str(row["state"]).startswith("BLOCKED_"))
    if (len(groups), partial, blocked) != (10, 6, 4):
        raise IOGapAuditError("Audit group status accounting drift")
    report: dict[str, Any] = {
        "schema": REPORT_ID,
        "schema_version": "1.0",
        "status": REPORT_STATUS,
        "candidate_io_contract_status": io_contract["status"],
        "candidate_input_admissible": False,
        "input_groups": groups,
        "summary": {
            "schema_groups": 10,
            "complete_groups": 0,
            "partial_groups": partial,
            "blocked_groups": blocked,
            "source_pins_verified": len(verified),
            "input_instance_emitted": False,
            "output_manifest_created": False,
            "renderer_implementation_added": False,
            "renderer_dispatch_invoked": False,
            "media_created": False,
            "next_safe_increment": contract["next_safe_increment"],
        },
        "source_pins": verified,
        "governance": {
            "d4_8": "BLOCKED", "release_authority": "NONE", "d9_14": "BLOCKED_AS_REQUIRED",
            "d9_16": "BLOCKED_AS_REQUIRED", "d9_17": "BLOCKED_NO_GO", "d10": "BLOCKED",
            "c11c_source_mutation": False,
        },
    }
    report["audit_sha256"] = _sha_json(report)
    try:
        import jsonschema  # type: ignore
    except ImportError:
        jsonschema = None
    if jsonschema is not None:
        jsonschema.Draft202012Validator(schema).validate(report)
    return report

def build_audit(root: Path | str | None = None) -> dict[str, Any]:
    return _build_report(_root(root))

def validate_audit(candidate: Mapping[str, Any], root: Path | str | None = None) -> bool:
    if not isinstance(candidate, Mapping):
        raise IOGapAuditError("Audit report must be an object")
    expected = build_audit(root)
    if dict(candidate) != expected:
        raise IOGapAuditError("Audit report is not the exact current source-pinned gap analysis")
    return True

def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only source-pinned audit of the prospective D renderer I/O contract")
    parser.add_argument("--full-report", action="store_true", help="Print the full JSON report to stdout; never persist a report file")
    args = parser.parse_args()
    try:
        report = build_audit()
    except (IOGapAuditError, OSError, ValueError, TypeError, KeyError) as exc:
        print(f"C11-D CANDIDATE I/O GAP AUDIT FAIL | {exc}", file=sys.stderr)
        return 1
    if args.full_report:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        s = report["summary"]
        print("C11-D CANDIDATE I/O CONFORMANCE GAP AUDIT PASS"
              f" | groups={s['schema_groups']}/10 | complete={s['complete_groups']}/10"
              f" | partial={s['partial_groups']} | blocked={s['blocked_groups']}"
              f" | source_pins={s['source_pins_verified']}/{s['source_pins_verified']}"
              " | input_instance_emitted=false | output_manifest_created=false"
              " | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
