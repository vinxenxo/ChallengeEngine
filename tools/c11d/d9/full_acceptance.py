"""D9.16 full acceptance preflight: verify wiring, never claim blocked evidence.

No test subprocesses are executed here (the aggregate Suite runner does that),
no renderer or media is invoked, and no evidence is written.
"""
from __future__ import annotations
import copy, hashlib, json
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[3]
CONTRACT_REL = Path("definitions/c11d/d9/D9_16_FULL_ACCEPTANCE_V1.json")
FREEZE_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
SCHEMA = "C11-D-D9.16-FULL-ACCEPTANCE-PREFLIGHT-V1"
SURFACES = ("c11c-config", "c11c-producer", "c11c-test", "c11c-catalog", "c11c-maintenance")

class FullAcceptanceError(ValueError): pass

def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)

def sha256(value: Any) -> str: return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()
def sha256_file(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()
def _seal(record: Mapping[str, Any]) -> dict[str, Any]:
    result=copy.deepcopy(dict(record)); result.pop("preflight_sha256",None); result["preflight_sha256"]=sha256(result); return result
def _readj(path: Path) -> dict[str, Any]:
    try: value=json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc: raise FullAcceptanceError(f"cannot read JSON {path}: {exc}") from exc
    if not isinstance(value,dict): raise FullAcceptanceError(f"expected JSON object: {path}")
    return value
def _root(project_root: Path | str | None = None) -> Path: return Path(project_root).resolve() if project_root is not None else ROOT.resolve()

def build_full_acceptance_preflight(project_root: Path | str | None = None) -> dict[str, Any]:
    root=_root(project_root); errors=[]; checks=[]
    contract_path=(root/CONTRACT_REL).resolve()
    manifest_path=(root/"release/C11C_FREEZE_PACKAGE_MANIFEST.json").resolve()
    for candidate in (contract_path,manifest_path):
        try: candidate.relative_to(root)
        except ValueError as exc: raise FullAcceptanceError("D9.16 governed path escapes repository root") from exc
        if not candidate.is_file() or candidate.is_symlink(): errors.append(f"required governed file missing/unsafe: {candidate.relative_to(root)}")
    if errors: raise FullAcceptanceError("; ".join(errors))
    contract=_readj(contract_path); manifest_hash=sha256_file(manifest_path)
    if contract.get("schema")!="C11-D-D9.16-FULL-ACCEPTANCE-V1" or contract.get("checkpoint")!="D9.16": errors.append("canonical D9.16 contract identity mismatch")
    if manifest_hash != FREEZE_MANIFEST_SHA256 or manifest_hash != contract.get("immutable_reference",{}).get("sha256"): errors.append("immutable C11-C freeze manifest hash mismatch")

    # Verify exact five-surface topology through the shell's literal APP registry.
    shell_path=root/"c11c-suite/main.py"; shell_source=shell_path.read_text(encoding="utf-8-sig")
    import ast
    tree=ast.parse(shell_source); apps=None
    for node in ast.walk(tree):
        if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="APPS" for t in node.targets):
            try: apps=ast.literal_eval(node.value)
            except Exception: apps=None
            break
    surface_paths={row[1] for row in apps} if isinstance(apps,list) and all(isinstance(row,(list,tuple)) and len(row)>1 for row in apps) else set()
    expected_paths={f"{name}/main.py" for name in SURFACES}
    topology_ok=len(surface_paths)==5 and surface_paths==expected_paths
    checks.append({"check_id":"canonical_five_surface_topology","status":"PASS" if topology_ok else "BLOCKED","expected_surface_count":5,"actual_surface_count":len(surface_paths)})
    if not topology_ok: errors.append("canonical Suite surface topology drifted; exactly five surfaces required")

    # Confirm the accepted history checkpoints are represented as runnable test files.
    evidence_rows=[]
    for item in contract.get("acceptance_scope",[]):
        rel=item.get("evidence") if isinstance(item,dict) else None
        path=(root/str(rel)).resolve() if rel else root/"__missing__"
        try: path.relative_to(root)
        except ValueError: exists=False; errors.append(f"evidence path escapes repository: {rel}")
        else: exists=path.is_file() and not path.is_symlink()
        evidence_rows.append({"checkpoint":item.get("checkpoint"),"evidence":rel,"expected":item.get("expected"),"registered":exists})
        if not exists: errors.append(f"required checkpoint test missing/unsafe: {rel}")
    expect_checkpoints=[f"D9.{x}" for x in range(8,17)]
    checkpoint_order=[x.get("checkpoint") for x in evidence_rows]
    if checkpoint_order != expect_checkpoints: errors.append("D9.8–D9.16 evidence rows/order mismatch")
    checks.append({"check_id":"d9_8_to_d9_16_evidence_wiring","status":"PASS" if evidence_rows and all(x["registered"] for x in evidence_rows) and checkpoint_order==expect_checkpoints else "BLOCKED","registered_count":sum(bool(x["registered"]) for x in evidence_rows),"expected_count":len(expect_checkpoints)})

    test_manifest=_readj(root/"c11c-suite/c11c-test/BUILD_MANIFEST.json")
    config_manifest=_readj(root/"c11c-suite/c11c-config/BUILD_MANIFEST.json")
    producer_manifest=_readj(root/"c11c-suite/c11c-producer/BUILD_MANIFEST.json")
    catalog_manifest=_readj(root/"c11c-suite/c11c-catalog/BUILD_MANIFEST.json")
    maintenance_manifest=_readj(root/"c11c-suite/c11c-maintenance/BUILD_MANIFEST.json")
    test_route=any(isinstance(r,dict) and r.get("name")=="D9.16 FULL D9 ACCEPTANCE PREFLIGHT (NO MEDIA)" and r.get("entry")=="tools/c11d/d9/test_full_acceptance.py" for r in test_manifest.get("gui_routes",[]))
    test_declares= "tools/c11d/d9/test_full_acceptance.py" in test_manifest.get("tests",[])
    config_ro=(config_manifest.get("d9_16_full_acceptance_contract") == CONTRACT_REL.as_posix() and config_manifest.get("d9_16_full_acceptance_contract_access")=="READ_ONLY_CANONICAL")
    gates_safe=(test_manifest.get("renderer_activation") is False and test_manifest.get("media_creation") is False and test_manifest.get("release_authority")=="NONE" and config_manifest.get("release_authority")=="NONE" and producer_manifest.get("d9_14_renderer_activation") is False and catalog_manifest.get("release_authority")=="NONE" and maintenance_manifest.get("release_authority")=="NONE")
    checks.append({"check_id":"existing_surface_route_and_read_only_registration","status":"PASS" if test_route and test_declares and config_ro and gates_safe else "BLOCKED","test_route":test_route,"test_manifest_entry":test_declares,"config_read_only_registration":config_ro,"governance_flags_safe":gates_safe})
    if not test_route or not test_declares or not config_ro or not gates_safe: errors.append("D9.16 route/config/governance registration mismatch")

    # Independently verify D9.14 remains blocked and D9.15 is a static preflight only.
    import sys
    sys.path.insert(0,str(root/"tools/c11d/d9"))
    try:
        import gui_real_media_certification as d914
        gate=d914.build_certification_gate(root); d914.validate_certification_gate(gate,root)
        d914_safe=(gate.get("status")=="BLOCKED" and gate.get("governance",{}).get("d4_8")=="BLOCKED" and gate.get("governance",{}).get("renderer_activation") is False and gate.get("governance",{}).get("media_output_created") is False and gate.get("governance",{}).get("release_authority")=="NONE")
    except Exception as exc: d914_safe=False; errors.append(f"D9.14 gate validation failed: {exc}")
    try:
        import gui_operational_acceptance as d915
        op=d915.build_operational_preflight(root); d915.validate_operational_preflight(op,root)
        d915_safe=(op.get("status")=="PREFLIGHT_PASS_OPERATOR_CONFIRMATION_REQUIRED" and op.get("operational_acceptance_closed") is False and op.get("operator_acceptance",{}).get("confirmed") is False and op.get("surface_count")==5)
    except Exception as exc: d915_safe=False; errors.append(f"D9.15 preflight validation failed: {exc}")
    checks.append({"check_id":"d9_14_blocked_gate_preserved","status":"PASS" if d914_safe else "BLOCKED"})
    checks.append({"check_id":"d9_15_operator_evidence_not_inferred","status":"PASS" if d915_safe else "BLOCKED"})
    if not d914_safe: errors.append("D9.14 must remain blocked until separately authorized baseline and D4.8")
    if not d915_safe: errors.append("D9.15 cannot infer five-surface operator evidence from static preflight")

    blockers=list(contract.get("full_acceptance_blockers",[]))
    static_pass=not errors and len(checks)==5 and all(x["status"]=="PASS" for x in checks) and len(evidence_rows)==9 and all(x["registered"] for x in evidence_rows)
    # This preflight explicitly is not a full acceptance and cannot be closed by local flags.
    record={
      "schema": "C11-D-D9.16-FULL-ACCEPTANCE-PREFLIGHT-V1",
      "schema_version":"1.0","checkpoint":"D9.16",
      "status":"PREFLIGHT_PASS_FULL_ACCEPTANCE_BLOCKED_AS_REQUIRED" if static_pass else "BLOCKED_PREFLIGHT",
      "static_preflight_pass":bool(static_pass),"full_acceptance_status":"BLOCKED_AS_REQUIRED",
      "full_acceptance_closed":False,"operator_confirmation_required":True,
      "case_count":len(evidence_rows),"cases":evidence_rows,"checks":checks,"check_count":len(checks),
      "blockers":blockers,"errors":errors,
      "operator_evidence":{"status":"REQUIRED","five_surface_evidence_recorded":False,"evidence_ref":None},
      "governance":copy.deepcopy(contract.get("governance",{})),
      "side_effects":{"files_written":False,"renderer_activated":False,"production_executed":False,"media_created":False,"release_created":False},
      "references":{"contract_sha256":sha256_file(contract_path),"historical_c11c_manifest_sha256":manifest_hash},
      "d9_14_gate_status":"BLOCKED","d9_15_operator_status":"REQUIRED",
    }
    return _seal(record)

def validate_full_acceptance_preflight(record: Mapping[str,Any], project_root: Path | str | None = None) -> dict[str,Any]:
    root=_root(project_root)
    if not isinstance(record,Mapping): raise FullAcceptanceError("D9.16 record must be an object")
    candidate=copy.deepcopy(dict(record)); given=candidate.pop("preflight_sha256",None)
    if not isinstance(given,str) or len(given)!=64 or given!=sha256(candidate): raise FullAcceptanceError("D9.16 preflight SHA-256 mismatch")
    if candidate.get("schema")!=SCHEMA or candidate.get("checkpoint")!="D9.16": raise FullAcceptanceError("D9.16 schema/checkpoint mismatch")
    if candidate.get("status")!="PREFLIGHT_PASS_FULL_ACCEPTANCE_BLOCKED_AS_REQUIRED" or candidate.get("static_preflight_pass") is not True: raise FullAcceptanceError("D9.16 static preflight is not passing")
    if candidate.get("full_acceptance_status")!="BLOCKED_AS_REQUIRED" or candidate.get("full_acceptance_closed") is not False: raise FullAcceptanceError("D9.16 cannot claim full acceptance while mandatory evidence is blocked")
    expected_gov={"master_seed":"NOT_ADOPTED","gameplay_seed_source":"request.seed","music_seed_source":"request.music_seed","cross_domain_seed_sharing":"FORBIDDEN","automatic_seed_generation":False,"runtime_seed_derivation":False,"renderer_activation":False,"renderer_input_emitted":False,"production_execution":False,"media_created":False,"d4_8":"BLOCKED","runtime_authority":"NONE","release_authority":"NONE","longform":"DISABLED_UNTIL_CANONICAL_D_REQUEST_SUPPORTS_LONGFORM","c11c_frozen_reference_mutation":"FORBIDDEN"}
    if candidate.get("governance")!=expected_gov: raise FullAcceptanceError("D9.16 governance invariants drifted")
    if candidate.get("side_effects")!={"files_written":False,"renderer_activated":False,"production_executed":False,"media_created":False,"release_created":False}: raise FullAcceptanceError("D9.16 preflight must be side-effect-free")
    required=set(_readj(root/CONTRACT_REL).get("full_acceptance_blockers",[]))
    if not required.issubset(set(candidate.get("blockers",[]))): raise FullAcceptanceError("D9.16 blocker inventory incomplete")
    if candidate.get("operator_evidence")!={"status":"REQUIRED","five_surface_evidence_recorded":False,"evidence_ref":None}: raise FullAcceptanceError("D9.16 cannot invent operator evidence")
    if candidate.get("d9_14_gate_status")!="BLOCKED" or candidate.get("d9_15_operator_status")!="REQUIRED": raise FullAcceptanceError("D9.14/D9.15 blocker state drifted")
    if len(candidate.get("cases",[]))!=9 or candidate.get("case_count")!=9: raise FullAcceptanceError("D9.16 acceptance scope must contain nine checkpoints D9.8–D9.16")
    if candidate.get("errors")!=[]: raise FullAcceptanceError("passing static preflight cannot contain errors")
    current=build_full_acceptance_preflight(root)
    if current.get("status")!="PREFLIGHT_PASS_FULL_ACCEPTANCE_BLOCKED_AS_REQUIRED": raise FullAcceptanceError("current D9.16 preflight no longer passes")
    if current.get("preflight_sha256")!=given: raise FullAcceptanceError("stale D9.16 preflight record")
    return {"valid":True,"status":"PREFLIGHT_PASS_FULL_ACCEPTANCE_BLOCKED_AS_REQUIRED","full_acceptance_closed":False}
