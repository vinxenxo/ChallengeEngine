"""C11-D D9 request-to-payload instance integration V2; in-memory only, no renderer dispatch."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import os
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import d_renderer_dynamic_request_payload_binding as dynamic
import d_renderer_request_scoped_payload_materialization_binding as materialization_v1
import d_renderer_request_scoped_editorial_value_carrier as editorial_carrier_v1

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_REQUEST_SCOPED_PAYLOAD_MATERIALIZATION_BINDING_V2.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_REQUEST_SCOPED_PAYLOAD_MATERIALIZATION_BINDING_SCHEMA_V2.json")
PROPOSAL_REL = Path("definitions/c11d/production/D_RENDERER_CANDIDATE_REQUEST_PAYLOAD_INSTANCE_INTEGRATION_PROPOSAL_V1.json")
DECISION_REL = Path("definitions/c11d/production/D_RENDERER_REQUEST_PAYLOAD_INSTANCE_INTEGRATION_DECISION_V1.json")
MANIFEST_REL = Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")
MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
CONTRACT_ID = "C11-D-RENDERER-REQUEST-SCOPED-PAYLOAD-MATERIALIZATION-BINDING-CONTRACT-V2"
OUTPUT_SCHEMA = "C11-D-D9-RENDERER-REQUEST-SCOPED-PAYLOAD-MATERIALIZATION-BINDING-V2"
STATUS = "PREPARATION_ONLY_DYNAMIC_REQUEST_TO_PAYLOAD_INSTANCE_INTEGRATION_REVIEW_NOT_RENDERER_INPUT"
PROPOSAL_SHA256 = "3e65d03532417502ff9a957bc9a6efca01a974641aeaa1b9b00a11b1bdad4e81"
DECISION_SHA256 = "68d1e6e992f5d426c9553cbc0ae4da360e94a0cad3363b9b7c89a43e77c34711"

class PayloadInstanceIntegrationError(ValueError):
    """Fail-closed error for request/payload lineage or governance mismatches."""

def _root(project_root: Path | str | None = None) -> Path:
    return Path(project_root).resolve() if project_root is not None else HERE.parents[2]

def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

def _sha_json(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()

def _sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def _read_json(root: Path, rel: str | Path) -> dict[str, Any]:
    p = root / rel
    try:
        value = json.loads(p.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise PayloadInstanceIntegrationError(f"Cannot read JSON source {rel}: {exc}") from exc
    if not isinstance(value, dict):
        raise PayloadInstanceIntegrationError(f"JSON source root is not an object: {rel}")
    return value

def _is_sha(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(ch in "0123456789abcdef" for ch in value)

def _load_contract(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    contract = _read_json(root, CONTRACT_REL)
    schema = _read_json(root, SCHEMA_REL)
    proposal = _read_json(root, PROPOSAL_REL)
    decision = _read_json(root, DECISION_REL)
    manifest = root / MANIFEST_REL
    if not manifest.is_file() or manifest.stat().st_size != 796318 or _sha_file(manifest) != MANIFEST_SHA256:
        raise PayloadInstanceIntegrationError("Frozen C11-C manifest identity/byte count mismatch")
    if _sha_file(root / PROPOSAL_REL) != PROPOSAL_SHA256:
        raise PayloadInstanceIntegrationError("Accepted proposal source drift")
    if _sha_file(root / DECISION_REL) != DECISION_SHA256:
        raise PayloadInstanceIntegrationError("Decision record source drift")
    if decision.get("status") != "ACCEPTED_FOR_BOUNDED_NONPRODUCTION_INTEGRATION_IMPLEMENTATION_AND_RUNTIME_REVIEW_ONLY":
        raise PayloadInstanceIntegrationError("Bounded integration decision is not accepted")
    if proposal.get("status") != "PROPOSAL_ONLY_NON_PRODUCTION_INTEGRATION_NOT_IMPLEMENTED_NOT_APPROVED":
        raise PayloadInstanceIntegrationError("Proposal status drift")
    if contract.get("schema") != CONTRACT_ID or contract.get("schema_version") != "2.0" or contract.get("candidate_input_admissible") is not False:
        raise PayloadInstanceIntegrationError("V2 contract identity/status/admission boundary mismatch")
    if contract.get("source_pins", [None])[0].get("path") != MANIFEST_REL.as_posix():
        raise PayloadInstanceIntegrationError("C11-C manifest must be first in the source pin list")
    pins = contract.get("source_pins")
    if not isinstance(pins, list) or len(pins) != 60:
        raise PayloadInstanceIntegrationError("V2 requires exactly the 54 proposal pins plus six proposal/decision pins")
    seen: set[str] = set()
    for row in pins:
        if not isinstance(row, Mapping) or set(row) != {"path", "role", "sha256"}:
            raise PayloadInstanceIntegrationError("Malformed V2 source pin")
        rel = Path(str(row["path"]))
        if rel.is_absolute() or ".." in rel.parts or rel.as_posix() in seen:
            raise PayloadInstanceIntegrationError("Unsafe or duplicate source pin path")
        seen.add(rel.as_posix())
        path = root / rel
        if not path.is_file() or not _is_sha(row["sha256"]):
            raise PayloadInstanceIntegrationError(f"Pinned source missing or digest malformed: {rel.as_posix()}")
        actual = _sha_file(path)
        if actual != row["sha256"]:
            raise PayloadInstanceIntegrationError(f"Source pin mismatch: {rel.as_posix()} expected={row['sha256']} actual={actual}")
    try:
        import jsonschema  # type: ignore
    except ImportError as exc:
        raise PayloadInstanceIntegrationError("jsonschema is required for strict Draft 2020-12 validation") from exc
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise PayloadInstanceIntegrationError("Output schema is not Draft 2020-12")
    jsonschema.Draft202012Validator.check_schema(schema)
    return contract, schema

def _verify_self_hash(obj: Mapping[str, Any], field: str, label: str) -> None:
    digest = obj.get(field)
    if not _is_sha(digest) or _sha_json({k: v for k, v in obj.items() if k != field}) != digest:
        raise PayloadInstanceIntegrationError(f"{label} self-hash mismatch")

def _normalized_selection(value: Mapping[str, Any]) -> dict[str, Any]:
    return {key: value.get(key) for key in ("content_type", "family_id", "subtype_id", "variant_id")}

def _join_one(
    binder: Mapping[str, Any], material: Mapping[str, Any], carrier: Mapping[str, Any], fixture: Mapping[str, Any]
) -> dict[str, Any]:
    # The dynamic binder has already run and validated its current V1 output schema.
    # Re-check digest closure and all keys at this interface boundary.
    _verify_self_hash(binder, "receipt_sha256", "dynamic binder receipt")
    manifest = binder.get("payload_manifest")
    if not isinstance(manifest, Mapping):
        raise PayloadInstanceIntegrationError("Dynamic binder request payload manifest missing")
    _verify_self_hash(manifest, "manifest_sha256", "dynamic request payload manifest")
    readiness = binder.get("readiness")
    if (
        binder.get("schema") != dynamic.OUTPUT_SCHEMA_ID
        or binder.get("status") != dynamic.STATUS
        or not isinstance(readiness, Mapping)
        or readiness.get("candidate_input_admissible") is not False
    ):
        raise PayloadInstanceIntegrationError(
            "Dynamic binder receipt schema/status/admission mismatch "
            "(candidate_input_admissible is defined under readiness by the V1 receipt schema)"
        )
    if binder.get("execution_boundary") != dynamic.EXPECTED_BOUNDARY:
        raise PayloadInstanceIntegrationError("Dynamic binder execution boundary is not fully locked")
    if readiness.get("video_render_ready") is not False:
        raise PayloadInstanceIntegrationError("Dynamic binder receipt must remain not render-ready")

    identity = binder.get("request_identity")
    source = binder.get("source_identity")
    evidence = binder.get("payload_evidence")
    midentity = manifest.get("request_identity")
    msource = manifest.get("source_lineage")
    mpayload = manifest.get("payload_identity")
    if not all(isinstance(x, Mapping) for x in (identity, source, evidence, midentity, msource, mpayload)):
        raise PayloadInstanceIntegrationError("Dynamic binder receipt has incomplete identity/manifest sections")

    content_type = str(fixture["content_type"])
    expected_selection = _normalized_selection(fixture["selection"])
    actual_selection = _normalized_selection(identity.get("selection", {}))
    manifest_selection = _normalized_selection(midentity.get("selection", {}))
    if actual_selection != expected_selection or manifest_selection != expected_selection:
        raise PayloadInstanceIntegrationError(f"Dynamic request selector mismatch: {content_type}")
    for key, expected in (("request_id", fixture["request_id"]), ("content_type", content_type),
                          ("gameplay_seed", fixture["gameplay_seed"]), ("music_seed", fixture["music_seed"]),
                          ("variation_index", fixture["variation_index"]),
                          ("presentation_profile_id", fixture["presentation_profile_id"]),
                          ("delivery_profile_id", fixture["delivery_profile_id"])):
        if identity.get(key) != expected or midentity.get(key) != expected:
            raise PayloadInstanceIntegrationError(f"Dynamic request identity mismatch {content_type}.{key}")
    if identity.get("gameplay_seed") == identity.get("music_seed"):
        raise PayloadInstanceIntegrationError("Gameplay and music seed domains must remain separate")

    request_hash = source.get("request_hash")
    if not _is_sha(request_hash) or midentity.get("canonical_request_sha256") != request_hash:
        raise PayloadInstanceIntegrationError("Canonical request hash does not close across binder and payload manifest")
    if midentity.get("plan_sha256") != source.get("plan_hash") or midentity.get("editorial_sha256") != source.get("editorial_hash"):
        raise PayloadInstanceIntegrationError("Canonical plan/editorial hashes differ across binder and manifest")
    if source.get("request_payload_manifest_sha256") != manifest.get("manifest_sha256") or evidence.get("request_payload_manifest_sha256") != manifest.get("manifest_sha256"):
        raise PayloadInstanceIntegrationError("Request payload manifest digest differs across receipt surfaces")
    for field, evidence_key in (("payload_sha256", "payload_sha256"), ("visual_state_sha256", "visual_state_sha256"), ("payload_scope", "payload_scope")):
        if evidence.get(evidence_key) != mpayload.get(field):
            raise PayloadInstanceIntegrationError(f"Manifest/payload evidence mismatch: {content_type}.{field}")
    lineage_hash = source.get("source_lineage_sha256")
    if not _is_sha(lineage_hash) or msource.get("dynamic_binding_lineage_sha256") != lineage_hash:
        raise PayloadInstanceIntegrationError("Dynamic request source lineage digest does not close")
    if msource.get("bridge_record_sha256") != source.get("bridge_record_hash") or msource.get("adapter_envelope_sha256") != source.get("adapter_envelope_hash") or msource.get("request_scoped_binding_sha256") != source.get("request_scoped_binding_sha256"):
        raise PayloadInstanceIntegrationError("Bridge/adapter/request-binding lineage differs across manifest surfaces")

    # V1 fixture payload hash is a different declared serialization from the dynamic binder's payload hash.
    # Preserve both digest namespaces; compare the request and provenance joins, never infer byte equality.
    _verify_self_hash(material, "binding_sha256", "fixed materialization binding")
    _verify_self_hash(carrier, "carrier_binding_sha256", "editorial carrier binding")
    if material.get("content_type") != content_type or carrier.get("content_type") != content_type:
        raise PayloadInstanceIntegrationError(f"Materialization/carrier content-type mismatch: {content_type}")
    if material.get("request_id") != fixture["request_id"] or carrier.get("request_id") != fixture["request_id"]:
        raise PayloadInstanceIntegrationError(f"Materialization/carrier request id mismatch: {content_type}")
    if material.get("canonical_request_sha256") != request_hash or carrier.get("canonical_request_sha256") != request_hash or carrier.get("base_materialization_request_sha256") != request_hash or carrier.get("request_hash_matches_base_materialization_request") is not True:
        raise PayloadInstanceIntegrationError(f"Canonical request hash does not join to both fixed materialization and editorial carrier: {content_type}")
    if material.get("producer_plan_sha256") != source.get("plan_hash") or material.get("bridge_record_sha256") != source.get("bridge_record_hash") or material.get("adapter_envelope_sha256") != source.get("adapter_envelope_hash") or material.get("request_source_binding_sha256") != source.get("source_binding_sha256"):
        raise PayloadInstanceIntegrationError(f"Request/plan/bridge/adapter/source-binding lineage mismatch: {content_type}")
    if material.get("selection") != {k:v for k,v in expected_selection.items() if k in material.get("selection", {})}:
        raise PayloadInstanceIntegrationError(f"Fixed materialization selector mismatch: {content_type}")
    if material.get("gameplay_seed") != fixture["gameplay_seed"] or material.get("source_seed_matches_request") is not True or material.get("materialization") != "IN_MEMORY_ONLY" or material.get("video_render_ready") is not False:
        raise PayloadInstanceIntegrationError(f"Fixed materialization seed/governance mismatch: {content_type}")
    if material.get("payload_instance_sha256") != carrier.get("payload_instance_sha256") or material.get("payload_instance_id") != carrier.get("payload_instance_id"):
        raise PayloadInstanceIntegrationError(f"Editorial carrier is not bound to the exact fixed materialization instance: {content_type}")
    if carrier.get("payload_mutated") is not False or carrier.get("editorial_values_injected_into_visual_payload") is not False or carrier.get("visual_payload_consumed_editorial_text") is not False:
        raise PayloadInstanceIntegrationError(f"Editorial sidecar falsely claims payload mutation/consumption: {content_type}")
    editorial_sha = source.get("editorial_hash")
    if not _is_sha(editorial_sha) or carrier.get("editorial_values_sha256") != editorial_sha:
        raise PayloadInstanceIntegrationError(f"Canonical editorial hash does not join to the sidecar: {content_type}")
    if material.get("gameplay_seed") != identity.get("gameplay_seed") or material.get("music_seed") != identity.get("music_seed") or material.get("variation_index") != identity.get("variation_index") or material.get("presentation_profile_id") != identity.get("presentation_profile_id") or material.get("delivery_profile_id") != identity.get("delivery_profile_id"):
        raise PayloadInstanceIntegrationError(f"Materialization request scope mismatch: {content_type}")

    row: dict[str, Any] = {
        "content_type": content_type,
        "request_id": str(identity["request_id"]),
        "selection": actual_selection,
        "gameplay_seed": int(identity["gameplay_seed"]),
        "music_seed": int(identity["music_seed"]),
        "variation_index": int(identity["variation_index"]),
        "presentation_profile_id": str(identity["presentation_profile_id"]),
        "delivery_profile_id": str(identity["delivery_profile_id"]),
        "canonical_request_sha256": str(request_hash),
        "producer_plan_sha256": str(source["plan_hash"]),
        "bridge_record_sha256": str(source["bridge_record_hash"]),
        "adapter_envelope_sha256": str(source["adapter_envelope_hash"]),
        "request_source_binding_sha256": str(source["source_binding_sha256"]),
        "dynamic_binder_receipt_sha256": str(binder["receipt_sha256"]),
        "request_payload_manifest_sha256": str(manifest["manifest_sha256"]),
        "dynamic_payload_sha256": str(mpayload["payload_sha256"]),
        "dynamic_visual_state_sha256": str(mpayload["visual_state_sha256"]),
        "dynamic_payload_scope": str(mpayload["payload_scope"]),
        "dynamic_source_lineage_sha256": str(lineage_hash),
        "legacy_payload_instance_id": str(material["payload_instance_id"]),
        "legacy_payload_instance_sha256": str(material["payload_instance_sha256"]),
        "legacy_materialization_binding_sha256": str(material["binding_sha256"]),
        "editorial_values_sha256": str(carrier["editorial_values_sha256"]),
        "editorial_carrier_binding_sha256": str(carrier["carrier_binding_sha256"]),
        "request_identity_join": "EXACT_CANONICAL_REQUEST_HASH_AND_SELECTOR_JOIN_PASS",
        "payload_digest_relation": "SEPARATE_CONTRACTS_NO_EQUIVALENCE_CLAIM",
        "editorial_sidecar_join": "CANONICAL_REQUEST_AND_EDITORIAL_VALUE_HASH_JOIN_PASS",
        "editorial_payload_consumed": False,
    }
    row["binding_sha256"] = _sha_json(row)
    return row

def _validate_receipt(receipt: Mapping[str, Any], schema: Mapping[str, Any]) -> None:
    if set(receipt) != set(schema.get("required", [])) or set(receipt) != set(schema.get("properties", {})):
        raise PayloadInstanceIntegrationError("V2 receipt top-level shape differs from strict schema")
    _verify_self_hash(receipt, "receipt_sha256", "integration receipt")
    for row in receipt.get("content_bindings", []):
        if set(row) != set(schema["properties"]["content_bindings"]["items"]["required"]):
            raise PayloadInstanceIntegrationError("V2 content binding shape differs from schema")
        _verify_self_hash(row, "binding_sha256", "V2 content binding")
    try:
        import jsonschema  # type: ignore
    except ImportError as exc:
        raise PayloadInstanceIntegrationError("jsonschema is required for strict Draft 2020-12 validation") from exc
    jsonschema.Draft202012Validator(schema).validate(dict(receipt))

def build_integration_receipt(
    root: Path | str,
    dynamic_receipts: list[Mapping[str, Any]],
    materialization_receipt: Mapping[str, Any],
    carrier_receipt: Mapping[str, Any],
) -> dict[str, Any]:
    project_root = _root(root)
    contract, schema = _load_contract(project_root)
    material_bindings = materialization_receipt.get("content_bindings")
    carrier_bindings = carrier_receipt.get("content_bindings")
    fixtures = contract.get("fixed_request_fixtures")
    if not isinstance(material_bindings, list) or not isinstance(carrier_bindings, list) or not isinstance(fixtures, list):
        raise PayloadInstanceIntegrationError("Existing materialization/carrier/fixture matrix is malformed")
    if len(dynamic_receipts) != 3 or len(material_bindings) != 3 or len(carrier_bindings) != 3 or len(fixtures) != 3:
        raise PayloadInstanceIntegrationError("V2 accepts exactly three fixed fixture receipts")
    if materialization_receipt.get("candidate_input_admissible") is not False or carrier_receipt.get("candidate_input_admissible") is not False:
        raise PayloadInstanceIntegrationError("Upstream materialization/carrier must remain inadmissible")
    _verify_self_hash(materialization_receipt, "receipt_sha256", "fixed materialization receipt")
    _verify_self_hash(carrier_receipt, "carrier_sha256", "editorial carrier receipt")
    rows = []
    for index, fixture in enumerate(fixtures):
        if fixture.get("content_type") != material_bindings[index].get("content_type") or fixture.get("content_type") != carrier_bindings[index].get("content_type"):
            raise PayloadInstanceIntegrationError("Canonical content binding order mismatch")
        rows.append(_join_one(dynamic_receipts[index], material_bindings[index], carrier_bindings[index], fixture))
    if [row["content_type"] for row in rows] != ["challenges", "visual_loops", "visual_drills"]:
        raise PayloadInstanceIntegrationError("V2 receipt content type/order is not canonical")

    runtime_identity = {
        "contract_path": CONTRACT_REL.as_posix(), "contract_sha256": _sha_file(project_root / CONTRACT_REL),
        "schema_path": SCHEMA_REL.as_posix(), "schema_sha256": _sha_file(project_root / SCHEMA_REL),
        "implementation_path": Path(__file__).resolve().relative_to(project_root).as_posix(), "implementation_sha256": _sha_file(Path(__file__).resolve()),
        "test_path": "tools/c11d/d9/test_d_renderer_request_scoped_payload_materialization_binding_v2.py",
        "test_sha256": _sha_file(project_root / "tools/c11d/d9/test_d_renderer_request_scoped_payload_materialization_binding_v2.py"),
        "proposal_contract_sha256": PROPOSAL_SHA256, "decision_record_sha256": DECISION_SHA256
    }
    receipt: dict[str, Any] = {
        "schema": OUTPUT_SCHEMA,
        "schema_version": "2.0",
        "status": STATUS,
        "frozen_c11c_manifest_sha256": MANIFEST_SHA256,
        "candidate_input_admissible": False,
        "source_pin_count": len(contract["source_pins"]),
        "runtime_identity": runtime_identity,
        "content_bindings": rows,
        "summary": {
            "content_types": 3,
            "request_identity_joins": 3,
            "payload_manifest_digests_verified": 3,
            "editorial_sidecar_joins": 3,
            "sidecar_field_values": 14,
            "visual_text_sidecar_values": 11,
            "metadata_only_values": 3,
            "visual_payload_text_consumed": 0,
            "payload_digest_equivalence_proven": False,
            "video_render_ready": False
        },
        "execution_boundary": {
            "mode":"IN_MEMORY_REVIEW_ONLY_REQUEST_PAYLOAD_JOIN_V2",
            "request_input_persisted":False,"payload_files_written":False,"receipt_files_written":False,
            "renderer_native_input_emitted":False,"renderer_dispatch_invoked":False,"renderer_activation":False,
            "production_execution":False,"media_output_created":False,"output_artifact_path":None,
            "editorial_values_injected_into_visual_payload":False,"c11c_source_mutation":False,
            "d4_8":"BLOCKED","release_authority":"NONE","d9_14":"BLOCKED_AS_REQUIRED",
            "d9_16":"BLOCKED_AS_REQUIRED","d9_17":"BLOCKED_NO_GO","d10":"BLOCKED"
        }
    }
    receipt["receipt_sha256"] = _sha_json(receipt)
    _validate_receipt(receipt, schema)
    return receipt

def run_review(godot: str, timeout: int = 120, root: Path | str | None = None) -> dict[str, Any]:
    project_root = _root(root)
    _load_contract(project_root)
    if not godot or (os.path.sep in godot and not Path(godot).is_file()):
        raise PayloadInstanceIntegrationError("A valid Godot 4.7.1 executable is required")
    if timeout < 1 or timeout > 600:
        raise PayloadInstanceIntegrationError("Timeout must be in 1..600 seconds")
    # Existing fixed payload and editorial sidecar remain their authoritative V1 interfaces.
    materialization_receipt = materialization_v1.run_review(project_root, executable=godot, timeout_seconds=timeout)
    carrier_receipt = editorial_carrier_v1.build_carrier(materialization_receipt, root=project_root)
    fixtures_by_type = materialization_v1._fixture_requests(project_root)
    raw_requests = [materialization_v1._raw_request(fixtures_by_type[key]) for key in ("challenges", "visual_loops", "visual_drills")]
    dynamic_result = dynamic.run_dynamic_request_matrix(
        godot, timeout, project_root, subprocess.run, raw_requests=raw_requests, mode="v1", independent_repeat=False
    )
    return build_integration_receipt(project_root, dynamic_result["receipts"], materialization_receipt, carrier_receipt)

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build a source-pinned in-memory V2 join of canonical requests, existing dynamic payload manifests and editorial sidecars; never renderer input.")
    parser.add_argument("--godot", default=os.environ.get("C11D_GODOT_EXECUTABLE", ""), help="Godot 4.7.1 Mono executable")
    parser.add_argument("--timeout", type=int, default=180, help="Per Godot harness timeout (1..600 seconds)")
    parser.add_argument("--root", default=str(_root()), help="Active checkout root")
    args = parser.parse_args(argv)
    try:
        receipt = run_review(args.godot, args.timeout, args.root)
    except Exception as exc:
        print(f"C11-D REQUEST-PAYLOAD INSTANCE INTEGRATION V2 FAIL | {exc} | renderer=OFF | media_created=false | candidate_input_admissible=false | D4.8=BLOCKED | release_authority=NONE", file=sys.stderr)
        return 1
    print("C11-D REQUEST-PAYLOAD INSTANCE INTEGRATION V2 PASS | fixtures=3/3 | canonical_request_joins=3/3 | payload_manifest_digests=3/3 | editorial_sidecar_joins=3/3 | sidecar_fields=14/14 | visual_payload_consumed=0/14 | payload_digest_equivalence=NOT_CLAIMED | source_pins=%d/%d | renderer=OFF | media_created=false | candidate_input_admissible=false | D4.8=BLOCKED | release_authority=NONE" % (receipt["source_pin_count"], receipt["source_pin_count"]))
    print("C11-D REQUEST-PAYLOAD INSTANCE INTEGRATION V2 RECEIPT=" + _canonical(receipt))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
