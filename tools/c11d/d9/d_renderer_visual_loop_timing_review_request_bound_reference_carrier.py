#!/usr/bin/env python3
"""Join canonical D9.9 request identity to timing/review reference metadata only; never bind payloads or render."""
from __future__ import annotations
import argparse, copy, hashlib, importlib.util, json, sys
from pathlib import Path
from typing import Any, Mapping
try:
    from jsonschema import Draft202012Validator
except ImportError as exc:
    raise RuntimeError("jsonschema is required for C11-D preparation audit") from exc
HERE=Path(__file__).resolve().parent
if str(HERE) not in sys.path: sys.path.insert(0,str(HERE))
CONTRACT_REL=Path("definitions/c11d/production/D_RENDERER_VISUAL_LOOP_TIMING_REVIEW_REQUEST_BOUND_REFERENCE_CARRIER_V1.json")
SCHEMA_REL=Path("definitions/c11d/production/D_RENDERER_VISUAL_LOOP_TIMING_REVIEW_REQUEST_BOUND_REFERENCE_CARRIER_SCHEMA_V1.json")
REPORT_SCHEMA_REL=Path("definitions/c11d/production/D_RENDERER_VISUAL_LOOP_TIMING_REVIEW_REQUEST_BOUND_REFERENCE_CARRIER_REPORT_SCHEMA_V1.json")
EXPECTED_C11C="e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
GRAMMARS=["harmonic_membrane","interference_plane","parametric_ribbon","lattice_wave","orbital_wave"]
class RequestBoundReferenceCarrierError(RuntimeError): pass
def require(cond: bool,msg: str):
    if not cond: raise RequestBoundReferenceCarrierError(msg)
def canonical(value: Any) -> str: return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)
def digest(value: Any) -> str: return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()
def file_sha(path: Path) -> str:
    try:return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as exc:raise RequestBoundReferenceCarrierError(f"Cannot read pinned source: {path}") from exc
def read_json(path: Path) -> Any:
    try:return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:raise RequestBoundReferenceCarrierError(f"Invalid JSON {path}: {exc}") from exc
def load_module(path: Path,name: str):
    spec=importlib.util.spec_from_file_location(name,path)
    require(spec is not None and spec.loader is not None,f"Cannot load parent audit: {path}")
    mod=importlib.util.module_from_spec(spec);sys.modules[name]=mod;spec.loader.exec_module(mod);return mod
def _root(root=None):return Path(root).resolve() if root is not None else Path(__file__).resolve().parents[3]
def _load(root: Path):
    c=read_json(root/CONTRACT_REL);s=read_json(root/SCHEMA_REL);rs=read_json(root/REPORT_SCHEMA_REL)
    for schema in (s,rs):
        require(schema.get("$schema")=="https://json-schema.org/draft/2020-12/schema","Wrong JSON Schema draft");Draft202012Validator.check_schema(schema)
    errors=sorted(Draft202012Validator(s).iter_errors(c),key=lambda e:list(e.absolute_path))
    if errors:
        e=errors[0];raise RequestBoundReferenceCarrierError(f"Contract schema rejected {'/'.join(map(str,e.absolute_path)) or '<root>'}: {e.message}")
    require(c.get("schema")=="C11-D-D10-VISUAL-LOOP-TIMING-REVIEW-REQUEST-BOUND-REFERENCE-CARRIER-V1","Contract identity mismatch")
    require(c.get("status")=="PREPARATION_ONLY_REQUEST_IDENTITY_JOINED_TO_POLICY_REFERENCE_METADATA_NOT_BINDING_NOT_APPROVED","Contract status cannot self-promote")
    require(c.get("authority",{}).get("frozen_c11c_manifest_sha256")==EXPECTED_C11C,"Frozen C11-C pin mismatch")
    require(c.get("authority",{}).get("canonical_binder_v1_mutated") is False and c.get("authority",{}).get("canonical_binding_v2_activated") is False,"Canonical binder boundary changed")
    require(c.get("authority",{}).get("policy_approval_granted") is False and c.get("authority",{}).get("candidate_input_admissible") is False,"Approval/admission cannot self-promote")
    pins=c.get("source_lineage");require(isinstance(pins,list) and len(pins)==22,"Expected exactly 22 direct source pins")
    seen=set()
    for i,row in enumerate(pins):
        require(isinstance(row,dict) and set(row)=={"path","sha256"},"Malformed source lineage row")
        rel=row["path"];require(isinstance(rel,str) and rel and not Path(rel).is_absolute() and ".." not in Path(rel).parts and "\\" not in rel,f"Unsafe source path: {rel!r}")
        require(rel not in seen,f"Duplicate pin: {rel}");seen.add(rel)
        actual=file_sha(root/rel);require(actual==row["sha256"],f"Pinned source drift: {rel}; expected={row['sha256']}; actual={actual}")
        if i==0:require(rel=="release/C11C_FREEZE_PACKAGE_MANIFEST.json" and actual==EXPECTED_C11C,"Frozen manifest must be first pin")
    for flag in ["timing_review_inheritance_approved","canonical_request_selector_matrix_approved","exact_selector_payload_approved","all_nine_shared_policy_sources_approved","candidate_io_contract_complete","d4_8_authorized","binding_v2_implementation_authorized"]:
        require(c.get("approval_gate",{}).get(flag) is False,f"Approval gate must remain closed: {flag}")
    return c,s,rs,len(pins)
def _build(root: Path):
    c,s,rs,pin_count=_load(root)
    # Parent audits re-verify their own sources, exact selectors, and all approval assertions.
    carrier_mod=load_module(root/"tools/c11d/d9/d_renderer_visual_loop_timing_review_reference_carrier.py","_c11d_timing_review_reference_carrier_parent")
    carrier=carrier_mod.audit(root)
    gap_mod=load_module(root/"tools/c11d/d9/d_renderer_visual_loop_geometric_request_chain_gap_audit.py","_c11d_geometric_request_chain_parent")
    gap=gap_mod.run_audit(root)
    require(gap["summary"].get("canonical_plans")=="5/5" and gap["summary"].get("source_binding_review_passes")=="1/5" and gap["summary"].get("blocked_by_fixed_v1_scope")=="4/4","Parent canonical source-binding scope changed unexpectedly")
    timing_mod=load_module(root/"tools/c11d/d9/d_renderer_visual_loop_timing_review_inheritance_audit.py","_c11d_timing_review_inheritance_parent")
    timing=timing_mod.audit(root)
    require(timing.get("approval_assertions_checked")==19 and timing.get("approvals_granted")==0,"Shared policy approvals unexpectedly changed")
    envelopes={e["selection"]["grammar_id"]:e for e in carrier["envelopes"]}
    gap_cases={r["grammar_id"]:r for r in gap["cases"]}
    from universal_producer import evaluate_universal_request, REQUEST_SCHEMA_ID
    relations=[]
    for idx,grammar in enumerate(GRAMMARS):
        env=envelopes.get(grammar);case=gap_cases.get(grammar)
        require(isinstance(env,Mapping) and isinstance(case,Mapping),f"Missing parent relation for {grammar}")
        request_id="D-GRAMMAR-CHAIN-GAP-"+grammar.upper()
        raw={"schema":REQUEST_SCHEMA_ID,"schema_version":"1.0","request_id":request_id,"mode":"REVIEW",
             "selection":{"content_type":"visual_loops","family_id":"c11c_geometric_waves_v1","subtype_id":grammar,"variant_id":None},
             "seed":12345,"music_seed":840001,"delivery_profile_id":"REVIEW_720","presentation_profile_id":"social_default_v1","variation_index":0,
             "audio_enabled":True,"personalization_enabled":True,"editorial_profile":{},
             "production_override":{"title":"Prueba editorial · título","subtitle":"Subtítulo de revisión","call_to_action":"Continuar","language":"es"},
             "provenance":{"source_revision":"C11D-D9.9-DYNAMIC-REQUEST-V1","request_origin":"TEST"}}
        result=evaluate_universal_request(raw,root)
        require(result.get("status")=="PLANNED",f"Canonical D9.9 request not planned: {grammar}")
        plan=result.get("plan",{});sel=plan.get("selection",{});can=result.get("canonical_request",{})
        require(can.get("request_id")==request_id,f"Canonical request ID drift: {grammar}")
        require(result.get("request_hash")==case.get("canonical_request_hash"),f"Request hash differs from parent gap audit: {grammar}")
        require(sel.get("content_type")=="visual_loops" and sel.get("family_id")=="c11c_geometric_waves_v1" and sel.get("subtype_id")==grammar and sel.get("variant_id") is None,f"Canonical selector mismatch: {grammar}")
        envsel=env.get("selection",{})
        selector={"content_type":"visual_loops","family_id":"c11c_geometric_waves_v1","grammar_id":grammar,"grammar_index":idx,"shader_branch":"field_"+grammar}
        require(envsel==selector,f"Reference envelope selector mismatch: {grammar}")
        require(env.get("request_bound") is False and env.get("canonical_binding_admitted") is False,f"Parent carrier self-promoted: {grammar}")
        require(env.get("canonical_request_modified") is False and env.get("canonical_payload_modified") is False and env.get("policy_values_copied") is False,f"Reference envelope ceased to be metadata-only: {grammar}")
        relation={"selector":selector,
          "request_identity":{"request_id":request_id,"request_hash":result["request_hash"],"plan_hash":result["plan_hash"],"canonical_status":"PLANNED"},
          "reference_identity":{"selector_envelope_sha256":env["selector_envelope_sha256"],"shared_reference_set_sha256":env["shared_reference_set_sha256"],"reference_count":len(env["policy_references"]),"source_envelope_request_bound":False},
          "join_checks":{"request_hash_matches_parent_chain":True,"plan_status_is_planned":True,"selector_matches_canonical_request":True,"selector_matches_reference_envelope":True,"shared_policy_digest_matches":True,"metadata_only_join":True},
          "locks":{"canonical_request_mutated":False,"canonical_plan_mutated":False,"source_envelope_mutated":False,"policy_values_consumed":False,"renderer_instructions_emitted":False,"payload_instance_bound":False,"candidate_input_admissible":False}}
        relations.append(relation)
    require(len({r["request_identity"]["request_hash"] for r in relations})==5,"Request hashes are not unique")
    require(len({r["request_identity"]["plan_hash"] for r in relations})==5,"Plan hashes are not unique")
    require(len({r["reference_identity"]["shared_reference_set_sha256"] for r in relations})==1,"Shared policy digest differs per selector")
    require(len({r["reference_identity"]["selector_envelope_sha256"] for r in relations})==5,"Selector envelope digests are not unique")
    require(sum(r["reference_identity"]["reference_count"] for r in relations)==45,"Policy reference pair count changed")
    report={"schema":"C11-D-VISUAL-LOOP-TIMING-REVIEW-REQUEST-BOUND-REFERENCE-CARRIER-REPORT-V1","schema_version":"1.0",
      "status":"PASS_PREPARATION_ONLY_REQUEST_IDENTITY_JOIN_VERIFIED_NOT_BINDING_NOT_APPROVED","contract_sha256":file_sha(root/CONTRACT_REL),
      "source_lineage":[dict(p) for p in c["source_lineage"]],"relations":relations,
      "summary":{"direct_source_pins":f"{pin_count}/{pin_count}","request_plans":"5/5","reference_envelopes":"5/5","request_identity_joins":"5/5","policy_reference_pairs":"45/45",
        "unique_request_hashes":"5/5","unique_plan_hashes":"5/5","shared_policy_digest_unique_count":1,"selector_envelope_digest_unique_count":"5/5",
        "canonical_binding":"1/5","blocked_by_fixed_v1_scope":"4/4","approval_assertions_checked":19,"approvals_granted":0,"candidate_input_admissible":False},
      "governance":{"timing_review_inheritance_approved":False,"canonical_request_selector_matrix_approved":False,"exact_selector_payload_approved":False,
        "all_shared_policy_sources_approved":False,"candidate_io_contract_complete":False,"d4_8_authorized":False,"request_persisted":False,
        "payload_materialized":False,"renderer_native_input_emitted":False,"renderer_dispatch_invoked":False,"media_created":False,"c11c_source_mutation":False,
        "renderer":"OFF","D4.8":"BLOCKED","release_authority":"NONE","D9.10":"PREPARE_ONLY","D9.17":"BLOCKED_NO_GO"}}
    report["report_sha256"]=digest(report)
    errors=sorted(Draft202012Validator(rs).iter_errors(report),key=lambda e:list(e.absolute_path))
    if errors:
        e=errors[0];raise RequestBoundReferenceCarrierError(f"Report schema rejected {'/'.join(map(str,e.absolute_path)) or '<root>'}: {e.message}")
    require(report["report_sha256"]==digest({k:v for k,v in report.items() if k!="report_sha256"}),"Report self-hash mismatch")
    return report
def build_report(project_root=None): return _build(_root(project_root))
def validate_report(candidate: Mapping[str,Any],project_root=None):
    require(isinstance(candidate,Mapping),"Report must be an object")
    expected=build_report(project_root)
    require(dict(candidate)==expected,"Report differs from canonical request/reference join or governance locks")
    require(digest({k:v for k,v in candidate.items() if k!="report_sha256"})==candidate.get("report_sha256"),"Report SHA-256 mismatch")
    return True
def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--root",required=True);p.add_argument("--full-report",action="store_true");a=p.parse_args(argv)
    try:
        r=build_report(a.root);s=r["summary"]
        print("C11-D VISUAL LOOP TIMING/REVIEW REQUEST-BOUND REFERENCE CARRIER AUDIT PASS | direct_source_pins="+s["direct_source_pins"]+" | request_plans=5/5 | reference_envelopes=5/5 | request_identity_joins=5/5 | policy_reference_pairs=45/45 | unique_request_hashes=5/5 | unique_plan_hashes=5/5 | shared_policy_digest=1 | selector_envelope_digests=5/5 | canonical_binding=1/5 | blocked_by_fixed_v1_scope=4/4 | approval_assertions_checked=19 | approvals_granted=0 | candidate_input_admissible=false | request_persisted=false | payload_materialized=false | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
        print("C11D_TIMING_REVIEW_REQUEST_BOUND_REFERENCE_CARRIER_REPORT="+canonical(r))
        if a.full_report: print(json.dumps(r,ensure_ascii=False,indent=2,sort_keys=True))
        return 0
    except Exception as exc:
        print(f"C11-D VISUAL LOOP TIMING/REVIEW REQUEST-BOUND REFERENCE CARRIER AUDIT FAIL | {exc} | candidate_input_admissible=false | request_persisted=false | payload_materialized=false | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
        return 1
if __name__=="__main__": raise SystemExit(main())
