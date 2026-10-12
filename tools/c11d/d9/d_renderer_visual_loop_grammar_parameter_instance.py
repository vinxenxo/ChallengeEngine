"""D9 grammar-specific parameter instance: canonical request-bound, in-memory only."""
from __future__ import annotations
import argparse, base64, copy, hashlib, json, math, os, re, subprocess, sys
from pathlib import Path
from typing import Any, Callable, Mapping
try:
    from jsonschema import Draft202012Validator
except ImportError as exc:
    raise RuntimeError("jsonschema is required for the D9 grammar parameter instance contract") from exc
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path: sys.path.insert(0, str(HERE))
import d_renderer_dynamic_request_payload_binding as dynamic
import d_renderer_visual_loop_grammar_binding_audit as grammar_audit
CONTRACT_REL=Path("definitions/c11d/production/D_RENDERER_VISUAL_LOOP_GRAMMAR_PARAMETER_INSTANCE_V1.json")
RUNNER_REL=Path("tools/c11d/d9/d_renderer_visual_loop_grammar_parameter_instance.py")
CONTRACT_SCHEMA_REL=Path("definitions/c11d/production/D_RENDERER_VISUAL_LOOP_GRAMMAR_PARAMETER_CONTRACT_SCHEMA_V1.json")
INPUT_SCHEMA_REL=Path("definitions/c11d/production/D_RENDERER_VISUAL_LOOP_GRAMMAR_PARAMETER_INPUT_SCHEMA_V1.json")
OUTPUT_SCHEMA_REL=Path("definitions/c11d/production/D_RENDERER_VISUAL_LOOP_GRAMMAR_PARAMETER_INSTANCE_SCHEMA_V1.json")

MANIFEST_REL=Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")
HARNESS_REL=Path("tools/c11d/d9/materialize_visual_loop_grammar_parameter_instance_in_memory.gd")
EXPECTED_MANIFEST_SHA256="e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
EXPECTED_GODOT_VERSION="4.7.1.stable.mono.official.a13da4feb"
PROBE_PREFIX="C11D_GRAMMAR_PARAMETER_INSTANCE_PROBE="
RECEIPT_PREFIX="C11D_GRAMMAR_PARAMETER_INSTANCE_RECEIPT="
SELECTED={"content_type":"visual_loops","family_id":"c11c_geometric_waves_v1","subtype_id":"harmonic_membrane","variant_id":None}
EXPECTED_CASE_IDS=("BASE","GAMEPLAY_SEED_ONLY","MUSIC_SEED_ONLY","VARIATION_INDEX_ONLY","DELIVERY_PROFILE_ONLY","EDITORIAL_ONLY")
MANIFEST_REL=Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")
PROTECTED_C11C_PATHS={"tools/prototypes/c11c_common/C11CVariationProfile.gd","tools/prototypes/c11c_geometric_waves_v1/GeometricWavesPrototype.gd","tools/prototypes/c11c_geometric_waves_v1/GeometricWavesRenderer.gd","tools/prototypes/c11c_geometric_waves_v1/GeometricWaves.gdshader","tools/prototypes/c11c_geometric_waves_v1/definition.json"}
STYLE_KEYS=("grammar_mode","palette_mode","morph","wave_frequency","line_width","glow_strength","polygon_sides","wave_ratio","shape_rotation","layer_spread","radial_wave_amplitude","liss_x_frequency","liss_y_frequency","interference_scale","hero_scale","perspective_strength","depth_strength","secondary_phase","color_phase","stroke_scale")
BOUNDARY={"mode":"GODOT_HEADLESS_IN_MEMORY_GRAMMAR_PARAMETER_REVIEW_ONLY","request_input_persisted":False,"parameter_payload_files_written":False,"receipt_files_written":False,"renderer_instance_created":False,"renderer_native_input_emitted":False,"renderer_dispatch_invoked":False,"shader_executed":False,"media_created":False,"c11c_source_mutation":False,"candidate_input_admissible":False,"renderer":"OFF","d4_8":"BLOCKED","release_authority":"NONE","d9_14":"BLOCKED_AS_REQUIRED","d9_16":"BLOCKED_AS_REQUIRED","d9_17":"BLOCKED_NO_GO","d10":"BLOCKED"}
class GrammarParameterInstanceError(ValueError): pass
def _root(value=None): return Path(value).resolve() if value else Path(__file__).resolve().parents[3]
def _canonical(value): return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)
def _sha_json(value): return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()
def _sha_file(path):
    try: return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as exc: raise GrammarParameterInstanceError(f"Cannot hash required source {path}: {exc}") from exc
def _read_json(path):
    try: return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc: raise GrammarParameterInstanceError(f"Cannot read JSON {path}: {exc}") from exc
def _is_sha(value): return isinstance(value,str) and re.fullmatch(r"[0-9a-f]{64}",value) is not None
def _require(condition,message):
    if not condition: raise GrammarParameterInstanceError(message)
def load_contract(root):
    contract=_read_json(root/CONTRACT_REL); c_schema=_read_json(root/CONTRACT_SCHEMA_REL); i_schema=_read_json(root/INPUT_SCHEMA_REL); o_schema=_read_json(root/OUTPUT_SCHEMA_REL)
    for schema in (c_schema,i_schema,o_schema):
        _require(schema.get("$schema")=="https://json-schema.org/draft/2020-12/schema","All schemas must use JSON Schema Draft 2020-12")
        Draft202012Validator.check_schema(schema)
    try: Draft202012Validator(c_schema).validate(contract)
    except Exception as exc: raise GrammarParameterInstanceError(f"Grammar parameter contract schema rejected: {getattr(exc,'message',str(exc))}") from exc
    _require(contract.get("schema")=="C11-D-D9-VISUAL-LOOP-GRAMMAR-PARAMETER-INSTANCE-CONTRACT-V1" and contract.get("schema_version")=="1.0","Grammar parameter contract identity mismatch")
    _require(contract.get("status")=="PREPARATION_ONLY_EXACT_GRAMMAR_PARAMETER_INSTANCE_IN_MEMORY_NOT_RENDERER_INPUT","Contract cannot self-promote")
    _require(contract.get("source_of_truth",{}).get("frozen_c11c_manifest_sha256")==EXPECTED_MANIFEST_SHA256 and _sha_file(root/MANIFEST_REL)==EXPECTED_MANIFEST_SHA256,"Frozen C11-C manifest mismatch")
    _require(contract.get("scope",{}).get("selected_grammar_id")=="harmonic_membrane" and contract.get("scope",{}).get("selected_grammar_index")==0,"Only pinned harmonic_membrane@0 is admitted")
    _require(contract.get("execution_boundary")==BOUNDARY,"Execution or governance boundary changed")
    approvals={"dynamic_request_contract_approved":False,"grammar_parameter_instance_approved":False,"visual_loop_grammar_instance_approved":False,"editorial_visual_consumption_approved":False,"presentation_geometry_approved":False,"temporal_alignment_approved":False,"renderer_baseline_approved":False,"renderer_baseline_frozen":False,"d4_8_authorized":False,"release_authority":"NONE"}
    _require(contract.get("approval_state")==approvals,"Contract approval state cannot promote production readiness")
    lineage=contract.get("source_lineage")
    _require(isinstance(lineage,list) and len(lineage)==18,"Expected 18 exact source pins")
    seen=set()
    for index,row in enumerate(lineage):
        _require(isinstance(row,dict) and set(row)=={"path","sha256"},"Malformed source pin")
        rel=row["path"]; path=Path(rel)
        _require(isinstance(rel,str) and not path.is_absolute() and ".." not in path.parts and "\\" not in rel and rel not in seen,"Unsafe or duplicate source pin")
        _require(_is_sha(row["sha256"]),f"Malformed SHA-256 source pin: {rel}")
        _require(_sha_file(root/path)==row["sha256"],f"Pinned source drift: {rel}")
        if index==0: _require(rel==MANIFEST_REL.as_posix() and row["sha256"]==EXPECTED_MANIFEST_SHA256,"Frozen C11-C manifest must be the first pin")
        seen.add(rel)
    # Validate both existing contracts and their own full upstream lineage before using their private canonical-chain functions.
    dynamic._load_contract(root)
    grammar_audit.load_and_validate_contract(root)
    _require(dynamic.EXPECTED_SCOPE["visual_loops"]==("VISUAL_LOOP_FAMILY_ENVELOPE_GRAMMAR_INSTANCE_UNRESOLVED",False),"Upstream visual-loop payload must remain truthfully family-level")
    return contract,c_schema,i_schema,o_schema,lineage

def _raw_cases():
    raw=dynamic._base_request(SELECTED,"D-GRAMMAR-PARAM-VISUAL-LOOP-BASE")
    cases=[]
    cases.append(("BASE",copy.deepcopy(raw)))
    v=copy.deepcopy(raw); v["request_id"]="D-GRAMMAR-PARAM-VISUAL-LOOP-GAMEPLAY-SEED-ONLY"; v["seed"]=54321; cases.append(("GAMEPLAY_SEED_ONLY",v))
    v=copy.deepcopy(raw); v["request_id"]="D-GRAMMAR-PARAM-VISUAL-LOOP-MUSIC-SEED-ONLY"; v["music_seed"]=840002; cases.append(("MUSIC_SEED_ONLY",v))
    v=copy.deepcopy(raw); v["request_id"]="D-GRAMMAR-PARAM-VISUAL-LOOP-VARIATION-ONLY"; v["variation_index"]=17; cases.append(("VARIATION_INDEX_ONLY",v))
    v=copy.deepcopy(raw); v["request_id"]="D-GRAMMAR-PARAM-VISUAL-LOOP-DELIVERY-ONLY"; v["delivery_profile_id"]="MASTER_1080"; cases.append(("DELIVERY_PROFILE_ONLY",v))
    v=copy.deepcopy(raw); v["request_id"]="D-GRAMMAR-PARAM-VISUAL-LOOP-EDITORIAL-ONLY"; v["production_override"]["title"]="Título editorial alternativo"; cases.append(("EDITORIAL_ONLY",v))
    return cases

def _build_probe_input(chain,root,contract):
    request=dynamic._godot_input(chain)
    result=chain["result"]; bridge=chain["bridge"]; envelope=chain["envelope"]
    value={"schema":"C11-D-D9-VISUAL-LOOP-GRAMMAR-PARAMETER-INPUT-V1","schema_version":"1.0","contract_sha256":_sha_file(root/CONTRACT_REL),"frozen_c11c_manifest_sha256":EXPECTED_MANIFEST_SHA256,"request":request,"canonical_chain":{"plan_hash":result["plan_hash"],"editorial_hash":result["editorial_hash"],"bridge_record_hash":bridge["record_hash"],"adapter_envelope_hash":envelope["envelope_hash"],"source_binding_sha256":chain["source_binding"]["binding_sha256"]}}
    try: Draft202012Validator(_read_json(root/INPUT_SCHEMA_REL)).validate(value)
    except Exception as exc: raise GrammarParameterInstanceError(f"Probe input rejected by strict schema: {getattr(exc,'message',str(exc))}") from exc
    return value

def _validate_probe(report,probe_input,root=None):
    request=probe_input["request"]; chain=probe_input["canonical_chain"]; selected_root=_root(root)
    expected={"schema":"C11-D-D9-VISUAL-LOOP-GRAMMAR-PARAMETER-PROBE-V1","schema_version":"1.0","status":"PREPARATION_ONLY_EXACT_GRAMMAR_PARAMETER_INSTANCE_IN_MEMORY_NOT_RENDERER_INPUT","contract_sha256":probe_input["contract_sha256"],"request_id":request["request_id"],"request_hash":request["request_hash"],"selection":SELECTED,"gameplay_seed":request["seed"],"music_seed":request["music_seed"],"variation_index":request["variation_index"],"presentation_profile_id":request["presentation_profile_id"],"delivery_profile_id":request["delivery_profile_id"],"canonical_chain":chain,"repeat_deterministic":True,"source_checks_passed":True,"renderer_native_input_emitted":False,"renderer_instance_created":False,"renderer_dispatch_invoked":False,"shader_executed":False,"media_created":False,"disk_writes":False,"c11c_source_mutation":False,"candidate_input_admissible":False,"renderer":"OFF","d4_8":"BLOCKED","release_authority":"NONE","d9_17":"BLOCKED_NO_GO","d10":"BLOCKED"}
    for k,v in expected.items():
        if report.get(k)!=v: raise GrammarParameterInstanceError(f"Godot probe summary mismatch at {k}: expected {v!r}, got {report.get(k)!r}")
    if set(report)!=(set(expected)|{"parameter_instance"}): raise GrammarParameterInstanceError("Godot probe summary has unknown or missing fields")
    instance=report.get("parameter_instance")
    if not isinstance(instance,dict): raise GrammarParameterInstanceError("parameter_instance must be an object")
    try: Draft202012Validator(_read_json(selected_root/OUTPUT_SCHEMA_REL)["$defs"]["parameter_instance"]).validate(instance)
    except Exception as exc:
        # A nested schema is strictly revalidated by final receipt validation; this message keeps the first error useful.
        if hasattr(exc,"message"): raise GrammarParameterInstanceError(f"Parameter instance rejected: {exc.message}") from exc
        raise
    if instance.get("selection")!=SELECTED or instance.get("grammar_id")!="harmonic_membrane" or instance.get("grammar_index")!=0 or instance.get("shader_branch")!="field_harmonic_membrane" or instance.get("shader_uniform")!="grammar_mode":
        raise GrammarParameterInstanceError("Parameter instance does not match exact selector-to-shader mapping")
    style=instance.get("style_parameters")
    if not isinstance(style,dict) or set(style)!=set(STYLE_KEYS) or len(style)!=20:
        raise GrammarParameterInstanceError("Projected style parameter shape is not exactly 20 parameters")
    if style.get("grammar_mode")!=0: raise GrammarParameterInstanceError("Selected grammar index was not pinned at 0")
    for key,val in style.items():
        if isinstance(val,bool) or not isinstance(val,(int,float)) or not math.isfinite(float(val)):
            raise GrammarParameterInstanceError(f"Style parameter is not a finite numeric value: {key}")
    for key in ("style_parameters_sha256","parameter_instance_sha256"):
        if not _is_sha(instance.get(key)): raise GrammarParameterInstanceError(f"Malformed {key}")
    if instance["style_parameters_sha256"] != _sha_json(style):
        raise GrammarParameterInstanceError("Style parameter SHA-256 does not match the projected values")
    instance_core={k:v for k,v in instance.items() if k not in ("style_parameters_sha256","parameter_instance_sha256")}
    if instance["parameter_instance_sha256"] != _sha_json(instance_core):
        raise GrammarParameterInstanceError("Parameter-instance SHA-256 does not match the complete instance")
    return dict(report)

def _invoke_probe(root,chain,contract,iodata,godot,timeout,process_runner):
    data=_build_probe_input(chain,root,contract)
    encoded=base64.b64encode(_canonical(data).encode("utf-8")).decode("ascii")
    command=[godot,"--headless","--path",str(root),"--script","res://"+HARNESS_REL.as_posix(),"--",encoded]
    try: completed=process_runner(command,cwd=str(root),text=True,capture_output=True,timeout=timeout,check=False)
    except Exception as exc: raise GrammarParameterInstanceError(f"Godot grammar-parameter probe invocation failed: {exc}") from exc
    out=str(getattr(completed,"stdout","") or ""); err=str(getattr(completed,"stderr","") or ""); combined=out+"\n"+err; code=int(getattr(completed,"returncode",-1))
    if code!=0 or "SCRIPT ERROR:" in combined or "ERROR:" in combined or "GRAMMAR PARAMETER INSTANCE PROBE FAIL" in combined:
        raise GrammarParameterInstanceError(f"Godot grammar-parameter probe failed (exit={code}): {combined[-4500:]}")
    rows=[line[len(PROBE_PREFIX):] for line in combined.splitlines() if line.startswith(PROBE_PREFIX)]
    if len(rows)!=1: raise GrammarParameterInstanceError(f"Expected exactly one grammar-parameter probe receipt; got {len(rows)}")
    try: report=json.loads(rows[0])
    except json.JSONDecodeError as exc: raise GrammarParameterInstanceError("Godot probe output is not valid JSON") from exc
    if not isinstance(report,dict): raise GrammarParameterInstanceError("Godot probe output root must be an object")
    return _validate_probe(report,data,root)

def _case_receipt(case_id,chain,report):
    result,bridge,envelope=chain["result"],chain["bridge"],chain["envelope"]; req=result["canonical_request"]
    identity={"request_id":req["request_id"],"request_hash":result["request_hash"],"selection":SELECTED,"gameplay_seed":req["seed"],"music_seed":req["music_seed"],"variation_index":req["variation_index"],"presentation_profile_id":req["presentation_profile_id"],"delivery_profile_id":req["delivery_profile_id"]}
    canonical={"plan_hash":result["plan_hash"],"editorial_hash":result["editorial_hash"],"bridge_record_hash":bridge["record_hash"],"adapter_envelope_hash":envelope["envelope_hash"],"source_binding_sha256":chain["source_binding"]["binding_sha256"]}
    instance=report["parameter_instance"]
    bind_core={"case_id":case_id,"request_identity":identity,"canonical_chain":canonical,"parameter_instance_sha256":instance["parameter_instance_sha256"],"frozen_c11c_manifest_sha256":EXPECTED_MANIFEST_SHA256}
    return {"case_id":case_id,"request_identity":identity,"canonical_chain":canonical,"parameter_instance":instance,"request_parameter_binding_sha256":_sha_json(bind_core),"evidence":{"canonical_request_chain_verified":True,"source_pins_verified":True,"same_seed_repeat_deterministic":True,"exact_grammar_parameter_instance_materialized":True,"exact_selector_visual_payload_materialized":False,"family_authoring_envelope_gap":"REMAINS_OPEN"}}

def build_receipt(cases,root,contract,lineage,output_schema):
    by_id={r["case_id"]:r for r in cases}
    if len(cases)!=len(EXPECTED_CASE_IDS) or len(by_id)!=len(EXPECTED_CASE_IDS) or set(by_id)!=set(EXPECTED_CASE_IDS): raise GrammarParameterInstanceError("Case matrix identity mismatch")
    base=by_id["BASE"]["parameter_instance"]
    for case_id in ("MUSIC_SEED_ONLY","VARIATION_INDEX_ONLY","DELIVERY_PROFILE_ONLY","EDITORIAL_ONLY"):
        if by_id[case_id]["parameter_instance"]["style_parameters_sha256"]!=base["style_parameters_sha256"]:
            raise GrammarParameterInstanceError(f"Metadata-only change contaminated style values: {case_id}")
        if by_id[case_id]["parameter_instance"]["parameter_instance_sha256"]!=base["parameter_instance_sha256"]:
            raise GrammarParameterInstanceError(f"Metadata-only change contaminated grammar parameter instance: {case_id}")
    changed=by_id["GAMEPLAY_SEED_ONLY"]["parameter_instance"]
    if changed["style_parameters_sha256"]==base["style_parameters_sha256"] or changed["parameter_instance_sha256"]==base["parameter_instance_sha256"]:
        raise GrammarParameterInstanceError("Changing gameplay seed did not change the actual grammar parameter instance")
    for case_id,case in by_id.items():
        if case["parameter_instance"]["grammar_id"]!="harmonic_membrane" or case["parameter_instance"]["grammar_index"]!=0: raise GrammarParameterInstanceError(f"Grammar selector drifted with request metadata: {case_id}")
    lineage_digest=_sha_json(lineage)
    receipt={"schema":"C11-D-D9-VISUAL-LOOP-GRAMMAR-PARAMETER-INSTANCE-RECEIPT-V1","schema_version":"1.0","status":"PREPARATION_ONLY_EXACT_GRAMMAR_PARAMETER_INSTANCE_IN_MEMORY_NOT_RENDERER_INPUT","frozen_c11c_manifest_sha256":EXPECTED_MANIFEST_SHA256,
     "source_identity":{"contract_sha256":_sha_file(root/CONTRACT_REL),"input_schema_sha256":_sha_file(root/INPUT_SCHEMA_REL),"output_schema_sha256":_sha_file(root/OUTPUT_SCHEMA_REL),"harness_sha256":_sha_file(root/HARNESS_REL),"implementation_sha256":_sha_file(Path(__file__).resolve()),"source_lineage_sha256":lineage_digest,"dynamic_binding_implementation_sha256":_sha_file(root/Path("tools/c11d/d9/d_renderer_dynamic_request_payload_binding.py")),"grammar_audit_implementation_sha256":_sha_file(root/Path("tools/c11d/d9/d_renderer_visual_loop_grammar_binding_audit.py"))},
     "cases":cases,
     "findings":{"canonical_request_chain_passed":True,"grammar_parameter_instances_materialized":True,"case_count":6,"distinct_seed_style_change":True,"metadata_orthogonality_passed":True,"music_seed_isolated":True,"variation_index_isolated":True,"delivery_and_editorial_metadata_isolated":True,"family_authoring_envelope_gap":"REMAINS_OPEN","exact_selector_visual_payload_materialized":False,"candidate_input_admissible":False,"video_render_ready":False},
     "execution_boundary":copy.deepcopy(BOUNDARY)}
    receipt["receipt_sha256"]=_sha_json(receipt)
    try: Draft202012Validator(output_schema).validate(receipt)
    except Exception as exc: raise GrammarParameterInstanceError(f"Final receipt schema rejected: {getattr(exc,'message',str(exc))}") from exc
    _validate_receipt(receipt,root,output_schema)
    return receipt

def _validate_receipt(receipt,root,output_schema):
    if receipt.get("receipt_sha256")!=_sha_json({k:v for k,v in receipt.items() if k!="receipt_sha256"}): raise GrammarParameterInstanceError("Final receipt SHA-256 mismatch")
    if receipt.get("execution_boundary")!=BOUNDARY: raise GrammarParameterInstanceError("Receipt attempted to alter execution/governance boundary")
    if receipt.get("findings",{}).get("exact_selector_visual_payload_materialized") is not False: raise GrammarParameterInstanceError("Receipt may not claim a renderer-ready exact visual payload")
    if receipt.get("findings",{}).get("family_authoring_envelope_gap")!="REMAINS_OPEN": raise GrammarParameterInstanceError("Family-level authoring envelope gap must remain open")
    seen=set()
    for row in receipt.get("cases",[]):
        cid=row.get("case_id")
        if cid not in EXPECTED_CASE_IDS or cid in seen: raise GrammarParameterInstanceError("Duplicate or unknown matrix case ID")
        seen.add(cid)
        inst=row["parameter_instance"]
        core={k:v for k,v in inst.items() if k not in ("style_parameters_sha256","parameter_instance_sha256")}
        if not _is_sha(inst.get("style_parameters_sha256")) or not _is_sha(inst.get("parameter_instance_sha256")): raise GrammarParameterInstanceError("Malformed instance digest")
        if inst.get("style_parameter_count")!=20 or set(inst.get("style_parameters",{}))!=set(STYLE_KEYS): raise GrammarParameterInstanceError("Parameter instance lacks exact 20 style keys")
        if inst["style_parameters_sha256"] != _sha_json(inst["style_parameters"]): raise GrammarParameterInstanceError("Style parameter digest does not bind the style values")
        if inst["parameter_instance_sha256"] != _sha_json(core): raise GrammarParameterInstanceError("Parameter instance digest does not bind the complete instance")
        bind_core={"case_id":cid,"request_identity":row["request_identity"],"canonical_chain":row["canonical_chain"],"parameter_instance_sha256":inst["parameter_instance_sha256"],"frozen_c11c_manifest_sha256":EXPECTED_MANIFEST_SHA256}
        if row.get("request_parameter_binding_sha256")!=_sha_json(bind_core): raise GrammarParameterInstanceError("Request-to-parameter-instance digest mismatch")
    if seen!=set(EXPECTED_CASE_IDS): raise GrammarParameterInstanceError("Receipt matrix is incomplete")
    by_id={row["case_id"]:row for row in receipt["cases"]}
    base_case=by_id["BASE"]
    base_instance=base_case["parameter_instance"]
    base_identity=base_case["request_identity"]
    request_ids=[row["request_identity"]["request_id"] for row in receipt["cases"]]
    request_hashes=[row["request_identity"]["request_hash"] for row in receipt["cases"]]
    if len(set(request_ids))!=len(EXPECTED_CASE_IDS) or len(set(request_hashes))!=len(EXPECTED_CASE_IDS):
        raise GrammarParameterInstanceError("Matrix requests must have distinct IDs and canonical request hashes")
    for case_id in ("MUSIC_SEED_ONLY","VARIATION_INDEX_ONLY","DELIVERY_PROFILE_ONLY","EDITORIAL_ONLY"):
        row=by_id[case_id]
        if row["parameter_instance"]["style_parameters_sha256"]!=base_instance["style_parameters_sha256"]:
            raise GrammarParameterInstanceError(f"Metadata-only change contaminated style values: {case_id}")
        if row["parameter_instance"]["parameter_instance_sha256"]!=base_instance["parameter_instance_sha256"]:
            raise GrammarParameterInstanceError(f"Metadata-only change contaminated grammar parameter instance: {case_id}")
        if row["request_parameter_binding_sha256"]==base_case["request_parameter_binding_sha256"]:
            raise GrammarParameterInstanceError(f"Request-binding digest did not change for altered request: {case_id}")
        if row["request_identity"]["request_hash"]==base_identity["request_hash"]:
            raise GrammarParameterInstanceError(f"Canonical request hash did not change for altered request: {case_id}")
    gameplay=by_id["GAMEPLAY_SEED_ONLY"]["parameter_instance"]
    if gameplay["style_parameters_sha256"]==base_instance["style_parameters_sha256"] or gameplay["parameter_instance_sha256"]==base_instance["parameter_instance_sha256"]:
        raise GrammarParameterInstanceError("Gameplay-seed change did not alter style and grammar parameter-instance digests")
    for row in receipt["cases"]:
        inst=row["parameter_instance"]
        if inst.get("grammar_id")!="harmonic_membrane" or inst.get("grammar_index")!=0 or inst.get("shader_branch")!="field_harmonic_membrane" or inst.get("shader_uniform")!="grammar_mode":
            raise GrammarParameterInstanceError("Exact selector-to-shader grammar binding drifted")
        evidence=row.get("evidence",{})
        if evidence.get("exact_grammar_parameter_instance_materialized") is not True or evidence.get("exact_selector_visual_payload_materialized") is not False or evidence.get("family_authoring_envelope_gap")!="REMAINS_OPEN":
            raise GrammarParameterInstanceError("Case evidence overstated exact payload readiness or closed an unresolved gap")
    try: Draft202012Validator(output_schema).validate(dict(receipt))
    except Exception as exc: raise GrammarParameterInstanceError(f"Receipt schema validation failed: {getattr(exc,'message',str(exc))}") from exc
    return True

def run_matrix(godot,timeout=120,project_root=None,process_runner=subprocess.run):
    root=_root(project_root); contract,_,input_schema,output_schema,lineage=load_contract(root)
    cases=[]
    for case_id,raw in _raw_cases():
        chain=dynamic._build_canonical_chain(raw,root)
        selection=dynamic._canonical_selection(chain["result"]["plan"]["selection"])
        if selection!=SELECTED: raise GrammarParameterInstanceError(f"Canonical chain produced unexpected selection for {case_id}")
        data=_build_probe_input(chain,root,contract)
        report=_invoke_probe(root,chain,contract,data,godot,timeout,process_runner)
        cases.append(_case_receipt(case_id,chain,report))
    receipt=build_receipt(cases,root,contract,lineage,output_schema)
    return receipt

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--godot",default=os.environ.get("C11D_GODOT_EXECUTABLE",""),help="Godot 4.7.1 console executable")
    parser.add_argument("--timeout",type=int,default=120,help="Per-probe timeout in seconds")
    parser.add_argument("--root",default=str(_root()),help="Repository root")
    args=parser.parse_args(argv); root=Path(args.root).resolve()
    if not args.godot or not Path(args.godot).is_file():
        print("C11-D VISUAL LOOP GRAMMAR PARAMETER INSTANCE FAIL | Godot console executable missing | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE"); return 2
    if args.timeout<1 or args.timeout>600:
        print("C11-D VISUAL LOOP GRAMMAR PARAMETER INSTANCE FAIL | timeout must be in 1..600 | renderer=OFF | media_created=false"); return 2
    try:
        version=subprocess.run([args.godot,"--version"],cwd=str(root),text=True,capture_output=True,timeout=min(args.timeout,30),check=False)
        version_text=(str(version.stdout or "")+str(version.stderr or "")).strip()
        if version.returncode!=0 or version_text!=EXPECTED_GODOT_VERSION: raise GrammarParameterInstanceError(f"Expected Godot {EXPECTED_GODOT_VERSION}, got {version_text!r}")
        receipt=run_matrix(args.godot,args.timeout,root,subprocess.run)
        print(RECEIPT_PREFIX+json.dumps(receipt,ensure_ascii=False,sort_keys=True,separators=(",",":")))
        for c in receipt["cases"]:
            i=c["request_identity"]; p=c["parameter_instance"]
            print("C11-D GRAMMAR PARAMETER CASE | id=%s | seed=%s | music_seed=%s | variation_index=%s | grammar=%s@%s | style_sha256=%s | instance_sha256=%s | request_binding=%s"%(c["case_id"],i["gameplay_seed"],i["music_seed"],i["variation_index"],p["grammar_id"],p["grammar_index"],p["style_parameters_sha256"],p["parameter_instance_sha256"],c["request_parameter_binding_sha256"]))
        print("C11-D VISUAL LOOP GRAMMAR PARAMETER INSTANCE PASS | cases=6/6 | canonical_request_chain=6/6 | exact_grammar_parameter_instance=6/6 | style_parameters=20/20 | gameplay_seed_changes_visual_instance=PASS | metadata_orthogonality=4/4 | exact_selector_visual_payload_materialized=false | family_envelope_gap=OPEN | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
        return 0
    except Exception as exc:
        print("C11-D VISUAL LOOP GRAMMAR PARAMETER INSTANCE FAIL | %s | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE"%str(exc)); return 1
if __name__=="__main__": raise SystemExit(main())
