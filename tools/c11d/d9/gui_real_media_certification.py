"""D9.14 fail-closed gate for future real-media GUI certification.

This module reports readiness only. It never calls a renderer, creates media,
starts production, writes certification evidence, or grants authority.
"""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[3]
CONTRACT_REL = Path("definitions/c11d/d9/D9_14_GUI_REAL_MEDIA_CERTIFICATION_GATE_V1.json")
BRIDGE_REL = Path("definitions/c11d/production/C11D_EDITORIAL_RENDER_BRIDGE_D9_10_V1.json")
ACTIVATION_REL = Path("definitions/c11d/production/C11D_PRODUCTION_ACTIVATION_POLICY_V1.json")
FREEZE_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
SCHEMA = "C11-D-D9.14-GUI-REAL-MEDIA-CERTIFICATION-PREFLIGHT-V1"

class CertificationGateError(ValueError):
    """Raised when D9.14 gate evidence is malformed or attempts to unlock execution."""

def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)

def sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()

def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def _read_json(path: Path) -> dict[str, Any]:
    try:
        value=json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise CertificationGateError(f"Cannot read governed JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise CertificationGateError(f"Governed JSON must be an object: {path}")
    return value

def _root(project_root: Path | str | None = None) -> Path:
    return Path(project_root).resolve() if project_root is not None else ROOT.resolve()

def _seal(record: Mapping[str, Any]) -> dict[str, Any]:
    result=copy.deepcopy(dict(record))
    result.pop("gate_sha256", None)
    result["gate_sha256"] = sha256(result)
    return result

def build_certification_gate(project_root: Path | str | None = None) -> dict[str, Any]:
    root=_root(project_root)
    contract_path=(root/CONTRACT_REL).resolve()
    bridge_path=(root/BRIDGE_REL).resolve()
    activation_path=(root/ACTIVATION_REL).resolve()
    manifest_path=(root/"release/C11C_FREEZE_PACKAGE_MANIFEST.json").resolve()
    for candidate in (contract_path, bridge_path, activation_path, manifest_path):
        try:
            candidate.relative_to(root)
        except ValueError as exc:
            raise CertificationGateError("D9.14 governed path escapes the project root") from exc
        if not candidate.is_file() or candidate.is_symlink():
            raise CertificationGateError(f"D9.14 required governed evidence missing or unsafe: {candidate.relative_to(root)}")
    contract=_read_json(contract_path)
    bridge=_read_json(bridge_path)
    activation=_read_json(activation_path)
    if contract.get("schema") != "C11-D-D9.14-GUI-REAL-MEDIA-CERTIFICATION-GATE-V1" or contract.get("checkpoint") != "D9.14":
        raise CertificationGateError("D9.14 canonical gate contract identity mismatch")
    manifest_hash=sha256_file(manifest_path)
    if manifest_hash != FREEZE_MANIFEST_SHA256 or manifest_hash != contract.get("immutable_reference",{}).get("sha256"):
        raise CertificationGateError("Historical C11-C freeze manifest hash mismatch; refusing certification preflight")
    if bridge.get("governance",{}).get("d4_8") != "BLOCKED" or bridge.get("governance",{}).get("renderer_activation") is not False or bridge.get("governance",{}).get("production_execution") is not False:
        raise CertificationGateError("D9.10 bridge policy drifted; D9.14 cannot infer authorization")
    execution=activation.get("execution",{})
    if activation.get("runtime_authority") != "NONE" or activation.get("renderer_activation_policy",{}).get("state") != "DISABLED" or execution.get("renderer_called") is not False or execution.get("production_execution") is not False:
        raise CertificationGateError("D4.8 activation policy drifted; D9.14 preflight fails closed")

    blockers=[
        "FUTURE_D_FROZEN_BASELINE_ABSENT_OR_NOT_AUTHORIZED",
        "D4_8_EXPLICIT_GOVERNANCE_AUTHORIZATION_ABSENT",
        "RENDERER_ACTIVATION_DISABLED",
        "PRODUCTION_EXECUTION_DISABLED",
        "REAL_MEDIA_PROVENANCE_AND_QA_NOT_AVAILABLE_FOR_UNIVERSAL_EDITORIAL_BINDER",
        "WINDOWS_GUI_REAL_MEDIA_OPERATOR_EVIDENCE_NOT_YET_ACCEPTED"
    ]
    cases=[]
    for item in contract.get("case_matrix",[]):
        if not isinstance(item,dict) or not isinstance(item.get("case_id"),str) or not isinstance(item.get("expected"),str):
            raise CertificationGateError("D9.14 case matrix is malformed")
        cases.append({"case_id":item["case_id"],"status":item["expected"],"executed":False,"media_created":False})
    record={
        "schema":SCHEMA,
        "schema_version":"1.0",
        "checkpoint":"D9.14",
        "status":"BLOCKED",
        "gate_result":"BLOCKED_REQUIRED_AUTHORIZED_D_RENDERER_BASELINE_AND_D4_8_GATE",
        "readiness_only":True,
        "operator_execution_authorized":False,
        "supported_content_types":list(contract["certification_scope"]["supported_content_types_when_authorized"]),
        "unsupported_content_types":copy.deepcopy(contract["certification_scope"]["unsupported_content_types"]),
        "case_count":len(cases),
        "cases":cases,
        "blockers":blockers,
        "references":{
            "contract_sha256":sha256_file(contract_path),
            "bridge_contract_sha256":sha256_file(bridge_path),
            "activation_policy_sha256":sha256_file(activation_path),
            "historical_c11c_manifest_sha256":manifest_hash
        },
        "governance":{
            "master_seed":"NOT_ADOPTED",
            "gameplay_seed_source":"request.seed",
            "music_seed_source":"request.music_seed",
            "cross_domain_seed_sharing":"FORBIDDEN",
            "automatic_seed_generation":False,
            "runtime_seed_derivation":False,
            "renderer_activation":False,
            "renderer_adapter_invoked":False,
            "renderer_input_emitted":False,
            "production_execution":False,
            "media_output_created":False,
            "output_artifact_path":None,
            "d4_8":"BLOCKED",
            "runtime_authority":"NONE",
            "release_authority":"NONE",
            "c11c_frozen_reference_mutation":"FORBIDDEN"
        }
    }
    return _seal(record)

def validate_certification_gate(record: Mapping[str, Any], project_root: Path | str | None = None) -> dict[str, Any]:
    root=_root(project_root)
    if not isinstance(record,Mapping):
        raise CertificationGateError("D9.14 gate record must be an object")
    candidate=dict(record)
    expected_hash=candidate.get("gate_sha256")
    unsigned=copy.deepcopy(candidate); unsigned.pop("gate_sha256",None)
    if not isinstance(expected_hash,str) or len(expected_hash)!=64 or expected_hash != sha256(unsigned):
        raise CertificationGateError("D9.14 gate SHA-256 seal mismatch")
    contract=_read_json(root/CONTRACT_REL)
    if candidate.get("schema") != SCHEMA or candidate.get("checkpoint") != "D9.14":
        raise CertificationGateError("D9.14 gate schema/checkpoint mismatch")
    if candidate.get("status") != "BLOCKED" or candidate.get("gate_result") != "BLOCKED_REQUIRED_AUTHORIZED_D_RENDERER_BASELINE_AND_D4_8_GATE":
        raise CertificationGateError("D9.14 cannot report production readiness while the future D baseline is absent")
    if candidate.get("readiness_only") is not True or candidate.get("operator_execution_authorized") is not False:
        raise CertificationGateError("D9.14 gate must remain preflight-only and unauthorized")
    scope=contract.get("certification_scope",{})
    if candidate.get("supported_content_types") != scope.get("supported_content_types_when_authorized"):
        raise CertificationGateError("D9.14 supported content type inventory mismatch")
    if candidate.get("unsupported_content_types") != scope.get("unsupported_content_types"):
        raise CertificationGateError("D9.14 unsupported content type policy mismatch")
    governance=candidate.get("governance",{})
    fixed={"renderer_activation":False,"renderer_adapter_invoked":False,"renderer_input_emitted":False,"production_execution":False,"media_output_created":False,"output_artifact_path":None,"d4_8":"BLOCKED","runtime_authority":"NONE","release_authority":"NONE","c11c_frozen_reference_mutation":"FORBIDDEN","master_seed":"NOT_ADOPTED","gameplay_seed_source":"request.seed","music_seed_source":"request.music_seed","cross_domain_seed_sharing":"FORBIDDEN","automatic_seed_generation":False,"runtime_seed_derivation":False}
    for key,value in fixed.items():
        actual=governance.get(key, object())
        if actual != value:
            raise CertificationGateError(f"D9.14 governance invariant violated: {key}")
    required_blockers={"FUTURE_D_FROZEN_BASELINE_ABSENT_OR_NOT_AUTHORIZED","D4_8_EXPLICIT_GOVERNANCE_AUTHORIZATION_ABSENT","RENDERER_ACTIVATION_DISABLED","PRODUCTION_EXECUTION_DISABLED"}
    if not required_blockers.issubset(set(candidate.get("blockers",[]))):
        raise CertificationGateError("D9.14 blocker list incomplete")
    cases=candidate.get("cases")
    expected_cases=contract.get("case_matrix",[])
    if not isinstance(cases,list) or len(cases)!=len(expected_cases) or candidate.get("case_count")!=len(expected_cases):
        raise CertificationGateError("D9.14 case count/matrix mismatch")
    expected_ids=[x.get("case_id") for x in expected_cases]
    if [x.get("case_id") if isinstance(x,dict) else None for x in cases] != expected_ids:
        raise CertificationGateError("D9.14 case order/identity mismatch")
    for row,source in zip(cases,expected_cases):
        if row.get("status") != source["expected"] or row.get("executed") is not False or row.get("media_created") is not False:
            raise CertificationGateError(f"D9.14 case must remain not-run/no-media: {row.get('case_id')}")
    refs=candidate.get("references",{})
    manifest=root/"release/C11C_FREEZE_PACKAGE_MANIFEST.json"
    if refs.get("historical_c11c_manifest_sha256") != FREEZE_MANIFEST_SHA256 or not manifest.is_file() or sha256_file(manifest)!=FREEZE_MANIFEST_SHA256:
        raise CertificationGateError("D9.14 historical C11-C manifest reference invalid")
    return {"status":"PASS_GATE_BLOCKED_AS_REQUIRED","case_count":len(cases),"blocker_count":len(candidate["blockers"]),"gate_sha256":expected_hash}

def run_preflight(project_root: Path | str | None = None) -> dict[str, Any]:
    gate=build_certification_gate(project_root)
    validate_certification_gate(gate,project_root)
    return gate

if __name__ == "__main__":
    try:
        gate=run_preflight()
    except CertificationGateError as exc:
        print(json.dumps({"status":"FAIL_CLOSED","error":str(exc)},ensure_ascii=False))
        raise SystemExit(2)
    print(json.dumps(gate,ensure_ascii=False,indent=2))
    print(f"C11-D D9.14 REAL-MEDIA CERTIFICATION GATE PASS | gate=BLOCKED | cases={gate['case_count']}/10 | blockers={len(gate['blockers'])} | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
