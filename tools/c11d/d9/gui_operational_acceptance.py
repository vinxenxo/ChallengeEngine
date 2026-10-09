"""D9.15 GUI operational acceptance preflight (no execution or evidence writes)."""
from __future__ import annotations
import copy, hashlib, json, ast
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[3]
CONTRACT_REL = Path("definitions/c11d/d9/D9_15_GUI_OPERATIONAL_ACCEPTANCE_V1.json")
FREEZE_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
SCHEMA = "C11-D-D9.15-GUI-OPERATIONAL-ACCEPTANCE-PREFLIGHT-V1"
SURFACES = ("c11c-config", "c11c-producer", "c11c-test", "c11c-catalog", "c11c-maintenance")

class OperationalAcceptanceError(ValueError):
    """Raised on missing/unsafe operational controls or attempts to claim acceptance early."""

def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)

def sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()

def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda:stream.read(1024*1024), b""): h.update(chunk)
    return h.hexdigest()

def _root(value: Path | str | None) -> Path:
    return Path(value).resolve() if value is not None else ROOT.resolve()

def _read_json(path: Path) -> dict[str, Any]:
    try: value=json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc: raise OperationalAcceptanceError(f"Cannot read JSON {path}: {exc}") from exc
    if not isinstance(value,dict): raise OperationalAcceptanceError(f"Expected JSON object: {path}")
    return value

def _seal(record: Mapping[str, Any]) -> dict[str, Any]:
    result=copy.deepcopy(dict(record)); result.pop("preflight_sha256",None); result["preflight_sha256"]=sha256(result); return result

def _safe_file(root: Path, rel: str) -> Path:
    candidate=(root/rel).resolve()
    try: candidate.relative_to(root)
    except ValueError as exc: raise OperationalAcceptanceError(f"D9.15 path escapes repository root: {rel}") from exc
    if candidate.is_symlink() or not candidate.is_file(): raise OperationalAcceptanceError(f"D9.15 required file missing/unsafe: {rel}")
    return candidate

def _surface_topology(root: Path) -> tuple[bool, list[str]]:
    shell=(root/"c11c-suite/main.py").read_text(encoding="utf-8-sig")
    tree=ast.parse(shell); apps=None
    for node in ast.walk(tree):
        if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="APPS" for t in node.targets):
            apps=ast.literal_eval(node.value); break
    if not isinstance(apps,list): return False,["canonical Suite APPS registry unavailable"]
    ids=[]
    for row in apps:
        if isinstance(row,(list,tuple)) and len(row)>1: ids.append(str(row[1]).replace("\\","/"))
    expected={f"{name}/main.py" for name in SURFACES}
    actual=set(ids)
    if len(ids)!=5 or actual!=expected:
        return False,[f"canonical Suite topology mismatch: count={len(ids)} paths={sorted(actual)}"]
    return True,[]

def build_operational_preflight(project_root: Path | str | None = None) -> dict[str, Any]:
    root=_root(project_root); contract_path=_safe_file(root,str(CONTRACT_REL)); contract=_read_json(contract_path)
    if contract.get("schema")!="C11-D-D9.15-GUI-OPERATIONAL-ACCEPTANCE-V1" or contract.get("checkpoint")!="D9.15":
        raise OperationalAcceptanceError("D9.15 canonical contract identity mismatch")
    errors=[]; surfaces=contract.get("surfaces",[])
    ids=[x.get("surface_id") for x in surfaces if isinstance(x,dict)]
    if tuple(ids)!=SURFACES: errors.append("D9.15 must use exactly the five canonical surfaces in approved order")
    surface_results=[]
    for item in surfaces:
        if not isinstance(item,dict): errors.append("Malformed D9.15 surface declaration"); continue
        checks=[]
        for key in ("main","launcher","manifest"):
            try: _safe_file(root,str(item.get(key,""))); checks.append({"item":key,"status":"PASS"})
            except OperationalAcceptanceError as exc: checks.append({"item":key,"status":"BLOCKED","reason":str(exc)}); errors.append(str(exc))
        try:
            manifest=_read_json(root/str(item["manifest"]))
            manifest_id=manifest.get("suite_id") or {"C11-C Producer":"c11c-producer","C11-C Catalog":"c11c-catalog"}.get(manifest.get("app"))
            if manifest_id!=item["surface_id"] or str(manifest.get("version"))!=item["version"]:
                raise OperationalAcceptanceError(f"Surface identity/version mismatch: {item['surface_id']}")
        except Exception as exc: checks.append({"item":"manifest_identity","status":"BLOCKED","reason":str(exc)}); errors.append(str(exc))
        else: checks.append({"item":"manifest_identity","status":"PASS"})
        surface_results.append({"surface_id":item["surface_id"],"checks":checks,"status":"PASS" if all(x["status"]=="PASS" for x in checks) else "BLOCKED"})
    topology_ok,topology_errors=_surface_topology(root); errors.extend(topology_errors)
    capability_results=[]
    caps=contract.get("capabilities",[])
    if not isinstance(caps,list) or not caps: raise OperationalAcceptanceError("D9.15 capability matrix missing")
    for cap in caps:
        if not isinstance(cap,dict): errors.append("Malformed capability declaration"); continue
        controls=[]
        for control in cap.get("required_controls",[]):
            try:
                path=_safe_file(root,str(control.get("path",""))); source=path.read_text(encoding="utf-8-sig")
                found=str(control.get("token","")) in source
                controls.append({"path":control["path"],"token":control["token"],"status":"PASS" if found else "BLOCKED"})
                if not found: errors.append(f"Missing GUI operational control {control.get('token')} in {control.get('path')}")
            except Exception as exc: controls.append({"path":control.get("path",""),"token":control.get("token",""),"status":"BLOCKED"}); errors.append(str(exc))
        capability_results.append({"capability_id":cap.get("capability_id"),"surface_ids":copy.deepcopy(cap.get("surface_ids",[])),"checks":controls,"status":"PASS" if controls and all(x["status"]=="PASS" for x in controls) else "BLOCKED","operator_confirmation_required":True,"operator_confirmed":False,"evidence_ref":None})
    try:
        manifest_path=_safe_file(root,"release/C11C_FREEZE_PACKAGE_MANIFEST.json"); manifest_hash=sha256_file(manifest_path)
        if manifest_hash!=FREEZE_MANIFEST_SHA256 or manifest_hash!=contract.get("immutable_reference",{}).get("sha256"):
            errors.append("Historical C11-C freeze manifest SHA-256 mismatch")
    except Exception as exc: manifest_hash=""; errors.append(str(exc))
    try:
        from gui_real_media_certification import build_certification_gate, validate_certification_gate
        gate=build_certification_gate(root); validate_certification_gate(gate,root)
        if gate.get("status")!="BLOCKED" or gate.get("governance",{}).get("renderer_activation") is not False or gate.get("governance",{}).get("media_output_created") is not False:
            errors.append("D9.14 must remain fail-closed while D4.8 is blocked")
    except Exception as exc: errors.append(f"D9.14 gate cannot be validated: {exc}")
    if len(capability_results)!=8: errors.append(f"D9.15 capability coverage must be exactly 8; got {len(capability_results)}")
    all_static=not errors and topology_ok and all(s["status"]=="PASS" for s in surface_results) and all(c["status"]=="PASS" for c in capability_results)
    record={
      "schema":SCHEMA,"schema_version":"1.0","checkpoint":"D9.15",
      "status":"PREFLIGHT_PASS_OPERATOR_CONFIRMATION_REQUIRED" if all_static else "BLOCKED",
      "preflight_pass":bool(all_static),"operational_acceptance_closed":False,
      "capability_count":len(capability_results),"capabilities":capability_results,
      "surface_count":len(surface_results),"surfaces":surface_results,
      "canonical_surface_topology":"PASS" if topology_ok else "BLOCKED",
      "operator_acceptance":{"status":"REQUIRED","confirmed":False,"evidence_ref":None,"reason":"Static preflight cannot substitute for interactive operator evidence from Windows GUI."},
      "errors":errors,
      "references":{"contract_sha256":sha256_file(contract_path),"historical_c11c_manifest_sha256":manifest_hash},
      "governance":copy.deepcopy(contract["governance"]),
      "side_effects":{"files_written":False,"renderer_activated":False,"production_executed":False,"media_created":False,"release_created":False}
    }
    return _seal(record)

def validate_operational_preflight(record: Mapping[str,Any], project_root: Path | str | None = None) -> dict[str,Any]:
    root=_root(project_root)
    if not isinstance(record,Mapping): raise OperationalAcceptanceError("D9.15 preflight must be an object")
    candidate=copy.deepcopy(dict(record)); given=candidate.pop("preflight_sha256",None)
    if not isinstance(given,str) or len(given)!=64 or given!=sha256(candidate): raise OperationalAcceptanceError("D9.15 preflight seal mismatch")
    contract=_read_json(_safe_file(root,str(CONTRACT_REL)))
    if candidate.get("schema")!=SCHEMA or candidate.get("checkpoint")!="D9.15": raise OperationalAcceptanceError("D9.15 preflight identity mismatch")
    if candidate.get("status")!="PREFLIGHT_PASS_OPERATOR_CONFIRMATION_REQUIRED" or candidate.get("preflight_pass") is not True: raise OperationalAcceptanceError("D9.15 may not claim acceptance when preflight is blocked")
    if candidate.get("operational_acceptance_closed") is not False: raise OperationalAcceptanceError("D9.15 cannot close acceptance inside static preflight")
    if candidate.get("surface_count")!=5 or [x.get("surface_id") for x in candidate.get("surfaces",[])]!=list(SURFACES): raise OperationalAcceptanceError("D9.15 must preserve five ordered canonical surfaces")
    if candidate.get("capability_count")!=8 or [x.get("capability_id") for x in candidate.get("capabilities",[])]!=[x.get("capability_id") for x in contract.get("capabilities",[])]: raise OperationalAcceptanceError("D9.15 operational capability matrix mismatch")
    if any(x.get("status")!="PASS" or x.get("operator_confirmation_required") is not True or x.get("operator_confirmed") is not False or x.get("evidence_ref") is not None for x in candidate.get("capabilities",[])): raise OperationalAcceptanceError("D9.15 cannot infer GUI operator confirmation from static checks")
    op=candidate.get("operator_acceptance",{})
    if op!={"status":"REQUIRED","confirmed":False,"evidence_ref":None,"reason":"Static preflight cannot substitute for interactive operator evidence from Windows GUI."}: raise OperationalAcceptanceError("D9.15 operator evidence state must remain pending")
    expected_gov=contract.get("governance",{})
    if candidate.get("governance")!=expected_gov: raise OperationalAcceptanceError("D9.15 governance mismatch")
    fixed_side={"files_written":False,"renderer_activated":False,"production_executed":False,"media_created":False,"release_created":False}
    if candidate.get("side_effects")!=fixed_side: raise OperationalAcceptanceError("D9.15 preflight must remain side-effect-free")
    freeze=candidate.get("references",{}).get("historical_c11c_manifest_sha256")
    if freeze!=FREEZE_MANIFEST_SHA256: raise OperationalAcceptanceError("D9.15 historical C11-C manifest reference mismatch")
    if candidate.get("errors")!=[]: raise OperationalAcceptanceError("D9.15 passing preflight cannot contain errors")
    # Verify current governed evidence, not only the receipt's sealed values.
    current=build_operational_preflight(root)
    if current.get("status")!="PREFLIGHT_PASS_OPERATOR_CONFIRMATION_REQUIRED": raise OperationalAcceptanceError("Current D9.15 preflight now blocks; stale record rejected")
    if candidate.get("references")!=current.get("references"): raise OperationalAcceptanceError("D9.15 current contract/manifest hashes differ from preflight receipt")
    return {"valid":True,"status":candidate["status"],"operator_confirmation_required":True}
