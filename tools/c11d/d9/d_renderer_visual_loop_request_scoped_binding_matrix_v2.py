"""Read-only V2 preparation matrix for five Geometric Waves request/source identities."""
from __future__ import annotations
import argparse, copy, hashlib, importlib.util, json, re, sys
from pathlib import Path
from typing import Any, Mapping

CONTRACT_REL = "definitions/c11d/production/D_RENDERER_VISUAL_LOOP_REQUEST_SCOPED_BINDING_MATRIX_V2.json"
CONTRACT_SCHEMA_REL = "definitions/c11d/production/D_RENDERER_VISUAL_LOOP_REQUEST_SCOPED_BINDING_MATRIX_SCHEMA_V2.json"
REPORT_SCHEMA_REL = "definitions/c11d/production/D_RENDERER_VISUAL_LOOP_REQUEST_SCOPED_BINDING_MATRIX_REPORT_SCHEMA_V2.json"
MANIFEST_REL = "release/C11C_FREEZE_PACKAGE_MANIFEST.json"
EXPECTED_MANIFEST = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
EXPECTED_GRAMMARS = ["harmonic_membrane", "interference_plane", "parametric_ribbon", "lattice_wave", "orbital_wave"]
STATUS = "PASS_PREPARATION_ONLY_GEOMETRIC_LOOP_REQUEST_SOURCE_BINDING_MATRIX_VERIFIED_NOT_PAYLOAD_BOUND_NOT_APPROVED"

class MatrixAuditError(ValueError): pass

def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()
def file_sha(path: Path) -> str:
    if not path.is_file(): raise MatrixAuditError(f"Missing pinned source: {path}")
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024), b""): h.update(chunk)
    return h.hexdigest()
def read_json(root: Path, rel: str) -> dict[str,Any]:
    try: out=json.loads((root/rel).read_text(encoding="utf-8-sig"))
    except Exception as exc: raise MatrixAuditError(f"Cannot read JSON source {rel}: {exc}") from exc
    if not isinstance(out,dict): raise MatrixAuditError(f"Expected JSON object at {rel}")
    return out
def _root(project_root=None) -> Path:
    return Path(project_root).resolve() if project_root is not None else Path(__file__).resolve().parents[3]
def _load_module(path: Path, name: str):
    if not path.is_file(): raise MatrixAuditError(f"Missing parent implementation: {path}")
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None: raise MatrixAuditError(f"Cannot load module: {path}")
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module
    # Canonical D9 modules import sibling modules by their existing stable names.
    d9_dir=str(path.parent)
    if d9_dir in sys.path: sys.path.remove(d9_dir)
    sys.path.insert(0,d9_dir)
    spec.loader.exec_module(module)
    return module

def _load_contract(root: Path):
    c=read_json(root,CONTRACT_REL);cs=read_json(root,CONTRACT_SCHEMA_REL);rs=read_json(root,REPORT_SCHEMA_REL)
    if c.get("schema")!="C11-D-D9-VISUAL-LOOP-REQUEST-SCOPED-BINDING-MATRIX-CONTRACT-V2" or c.get("schema_version")!="2.0":
        raise MatrixAuditError("V2 matrix contract identity/version mismatch")
    if c.get("status")!="PREPARATION_ONLY_GEOMETRIC_LOOP_REQUEST_SCOPED_SOURCE_BINDING_MATRIX_NOT_CANONICAL_INPUT_NOT_APPROVED":
        raise MatrixAuditError("V2 matrix contract attempted self-promotion")
    if cs.get("$schema")!="https://json-schema.org/draft/2020-12/schema" or cs.get("additionalProperties") is not False:
        raise MatrixAuditError("V2 contract schema draft/strictness mismatch")
    if rs.get("$schema")!="https://json-schema.org/draft/2020-12/schema" or rs.get("additionalProperties") is not False:
        raise MatrixAuditError("V2 report schema draft/strictness mismatch")
    try:
        from jsonschema import Draft202012Validator
        Draft202012Validator(cs).validate(c)
    except ImportError:
        pass
    except Exception as exc:
        raise MatrixAuditError(f"V2 contract schema rejected contract: {exc}") from exc
    auth=c.get("authority",{});scope=c.get("scope",{});reuse=c.get("v1_core_reuse",{});ref=c.get("reference_boundary",{})
    if auth.get("frozen_c11c_manifest_sha256")!=EXPECTED_MANIFEST or file_sha(root/MANIFEST_REL)!=EXPECTED_MANIFEST:
        raise MatrixAuditError("Frozen C11-C manifest mismatch")
    if auth.get("canonical_v1_mutated") is not False or auth.get("canonical_v1_contract_mutated") is not False or auth.get("canonical_v1_binding_scope_changed") is not False:
        raise MatrixAuditError("Canonical V1 mutation/scope widening must remain false")
    if scope.get("content_type")!="visual_loops" or scope.get("family_id")!="c11c_geometric_waves_v1":
        raise MatrixAuditError("V2 scope unexpectedly broadened beyond Geometric Waves")
    rows=scope.get("grammar_matrix")
    if not isinstance(rows,list) or [r.get("grammar_id") for r in rows]!=EXPECTED_GRAMMARS or [r.get("grammar_index") for r in rows]!=list(range(5)):
        raise MatrixAuditError("V2 grammar matrix identity/order mismatch")
    if reuse.get("mode")!="REUSE_EXISTING_V1_CORE_IN_MEMORY_WITH_V2_GEOMETRIC_FAMILY_MATRIX" or reuse.get("duplicate_binding_engine_added") is not False:
        raise MatrixAuditError("V2 must reuse existing binding core, not introduce a duplicate engine")
    if ref.get("policy_reference_count_per_selector")!=9 or ref.get("expected_selector_policy_pairs")!=45 or ref.get("policy_values_consumed") is not False:
        raise MatrixAuditError("Metadata-only shared policy reference boundary changed")
    approval=c.get("approval_state",{})
    for key in ("visual_loop_binding_matrix_v2_approved","canonical_request_selector_matrix_approved","exact_selector_payload_approved","timing_review_inheritance_approved","all_nine_shared_policy_sources_approved","candidate_io_contract_complete","renderer_baseline_approved","renderer_baseline_frozen","d4_8_authorized"):
        if approval.get(key) is not False: raise MatrixAuditError(f"Approval gate changed: {key}")
    if approval.get("d9_14_full_acceptance")!="BLOCKED_AS_REQUIRED" or approval.get("d9_16_full_acceptance")!="BLOCKED_AS_REQUIRED" or approval.get("d9_17_closure")!="BLOCKED_NO_GO" or approval.get("d10")!="BLOCKED" or approval.get("release_authority")!="NONE":
        raise MatrixAuditError("Full acceptance, D10 or release lock changed")
    pins=c.get("source_lineage")
    if not isinstance(pins,list) or len(pins)!=30 or pins[0].get("path")!=MANIFEST_REL or pins[0].get("sha256")!=EXPECTED_MANIFEST:
        raise MatrixAuditError("Expected 30 direct source pins with frozen C11-C manifest first")
    seen=set()
    for i,row in enumerate(pins):
        rel=row.get("path");expected=row.get("sha256")
        if not isinstance(rel,str) or not rel or Path(rel).is_absolute() or ".." in Path(rel).parts or "\\" in rel or rel in seen:
            raise MatrixAuditError(f"Unsafe or duplicate source path: {rel!r}")
        if not isinstance(expected,str) or not re.fullmatch(r"[0-9a-f]{64}",expected): raise MatrixAuditError(f"Malformed source hash: {rel}")
        actual=file_sha(root/rel)
        if actual!=expected: raise MatrixAuditError(f"Pinned source drift: {rel}; expected={expected}; actual={actual}")
        seen.add(rel)
    return c,cs,rs,pins

def _request_for_grammar(root: Path, grammar: str):
    d9=root/"tools/c11d/d9"
    if str(d9) in sys.path: sys.path.remove(str(d9))
    sys.path.insert(0,str(d9))
    from universal_producer import evaluate_universal_request, REQUEST_SCHEMA_ID
    from editorial_render_bridge import build_bridge_planning_record
    from d_render_adapter import prepare_d_only_adapter_envelope
    raw={"schema":REQUEST_SCHEMA_ID,"schema_version":"1.0","request_id":"D-GRAMMAR-CHAIN-GAP-"+grammar.upper(),"mode":"REVIEW",
      "selection":{"content_type":"visual_loops","family_id":"c11c_geometric_waves_v1","subtype_id":grammar,"variant_id":None},
      "seed":12345,"music_seed":840001,"delivery_profile_id":"REVIEW_720","presentation_profile_id":"social_default_v1","variation_index":0,
      "audio_enabled":True,"personalization_enabled":True,"editorial_profile":{},
      "production_override":{"title":"Prueba editorial · título","subtitle":"Subtítulo de revisión","call_to_action":"Continuar","language":"es"},
      "provenance":{"source_revision":"C11D-D9.9-DYNAMIC-REQUEST-V1","request_origin":"TEST"}}
    result=evaluate_universal_request(raw,root)
    if result.get("status")!="PLANNED": raise MatrixAuditError(f"Canonical D9.9 request not planned: {grammar}")
    selection=result.get("plan",{}).get("selection",{})
    if selection.get("content_type")!="visual_loops" or selection.get("family_id")!="c11c_geometric_waves_v1" or selection.get("subtype_id")!=grammar or selection.get("variant_id") is not None:
        raise MatrixAuditError(f"Canonical request/plan selector mismatch: {grammar}")
    bridge=build_bridge_planning_record(result,root)
    envelope=prepare_d_only_adapter_envelope(result,bridge,root)
    return result,bridge,envelope

def _build_binding(root: Path, contract: dict[str,Any], pins: list[dict[str,str]], carrier_report: dict[str,Any], binder, v1_contract, v1_schema, v1_lineage, grammar: str):
    grammar_rows={row["grammar_id"]:row for row in contract["scope"]["grammar_matrix"]}
    if grammar not in grammar_rows: raise MatrixAuditError(f"Grammar is outside V2's exact five-selector matrix: {grammar}")
    rel_by_grammar={row.get("selector",{}).get("grammar_id"):row for row in carrier_report.get("relations",[])}
    relation=rel_by_grammar.get(grammar)
    if not isinstance(relation,Mapping): raise MatrixAuditError(f"No parent request/reference relation for {grammar}")
    result,bridge,envelope=_request_for_grammar(root,grammar)
    request=result.get("canonical_request",{});plan=result.get("plan",{})
    req_identity=relation.get("request_identity",{});ref_identity=relation.get("reference_identity",{});sel=relation.get("selector",{})
    if request.get("request_id")!=req_identity.get("request_id") or result.get("request_hash")!=req_identity.get("request_hash") or result.get("plan_hash")!=req_identity.get("plan_hash"):
        raise MatrixAuditError(f"Canonical request identity does not match parent carrier relation: {grammar}")
    if sel.get("grammar_id")!=grammar or sel.get("grammar_index")!=grammar_rows[grammar]["grammar_index"] or sel.get("shader_branch")!=grammar_rows[grammar]["shader_branch"]:
        raise MatrixAuditError(f"V2 grammar identity diverges from parent carrier: {grammar}")
    if ref_identity.get("reference_count")!=9 or ref_identity.get("source_envelope_request_bound") is not False:
        raise MatrixAuditError(f"Parent reference boundary changed: {grammar}")
    if relation.get("locks",{}).get("candidate_input_admissible") is not False or relation.get("locks",{}).get("payload_instance_bound") is not False:
        raise MatrixAuditError(f"Parent carrier governance lock changed: {grammar}")
    # Do not fork policy/source resolution logic: reuse the existing canonical V1 core with a narrowly pinned in-memory matrix.
    extended=copy.deepcopy(v1_contract)
    extended["representative_source_matrix"]["visual_loops"]={
      "required_selection":{"content_type":"visual_loops","family_id":"c11c_geometric_waves_v1"},
      "payload_source_path":"definitions/visual_loop_geometric_canonical.json"}
    core=binder._build_core(result,bridge,envelope,root,extended,v1_schema,v1_lineage,False)
    found=core.get("source_binding",{}).get("resolved_identity",{}).get("selected_grammar_id")
    if found!=grammar: raise MatrixAuditError(f"Reused V1 core resolved the wrong grammar: requested={grammar}; found={found}")
    if core.get("source_binding",{}).get("source_class")!="FAMILY_CANONICAL_VISUAL_LOOP_DEFINITION_NOT_GRAMMAR_INSTANCE":
        raise MatrixAuditError(f"Family definition was misrepresented as grammar instance: {grammar}")
    if core.get("readiness",{}).get("request_scoped_visual_payload_instance_bound") is not False or core.get("readiness",{}).get("video_render_ready") is not False:
        raise MatrixAuditError(f"V1 core readiness escalated: {grammar}")
    report_hash=carrier_report.get("report_sha256")
    selector_hash=ref_identity.get("selector_envelope_sha256")
    shared_hash=ref_identity.get("shared_reference_set_sha256")
    identity=core["source_identity"]
    identity.update({
      "contract_sha256":file_sha(root/CONTRACT_REL),
      "schema_sha256":file_sha(root/REPORT_SCHEMA_REL),
      "implementation_sha256":file_sha(Path(__file__).resolve()),
      "source_lineage_sha256":digest(pins),
      "reference_carrier_report_sha256":report_hash,
      "shared_policy_reference_set_sha256":shared_hash,
      "selector_envelope_sha256":selector_hash,
    })
    core["schema"]="C11-D-D9-VISUAL-LOOP-REQUEST-SCOPED-PAYLOAD-BINDING-V2"
    core["schema_version"]="2.0"
    core["status"]="PREPARATION_ONLY_GEOMETRIC_LOOP_REQUEST_BINDING_V2_SOURCE_RESOLVED_NOT_PAYLOAD_BOUND_NOT_APPROVED"
    core["timing_review_reference"]={
      "status":"METADATA_REFERENCE_ONLY_NOT_APPROVED_NOT_CONSUMED",
      "request_id_match":True,"request_hash_match":True,"plan_hash_match":True,"selector_matches_canonical_request":True,
      "selector_envelope_sha256":selector_hash,"shared_policy_reference_set_sha256":shared_hash,"policy_reference_count":9,
      "policy_values_consumed":False,"policy_instructions_emitted":False,"timing_review_inheritance_approved":False,
      "source_envelope_request_bound":False,"request_persisted":False,
    }
    unresolved=list(core.get("unresolved_requirements",[]))
    if "SHARED_POLICY_REFERENCE_METADATA_IS_NOT_POLICY_APPROVAL_OR_RENDERER_INSTRUCTION" not in unresolved:
      unresolved.append("SHARED_POLICY_REFERENCE_METADATA_IS_NOT_POLICY_APPROVAL_OR_RENDERER_INSTRUCTION")
    core["unresolved_requirements"]=unresolved
    eb=core["execution_boundary"]
    eb.update({"mode":"IN_MEMORY_GEOMETRIC_LOOP_REQUEST_BINDING_V2_REVIEW_ONLY","source_adapter_mode":"PREPARE_ONLY",
      "policy_values_consumed":False,"timing_review_reference_only":True})
    core.pop("binding_sha256",None)
    core["binding_sha256"]=digest(core)
    _assert_no_truth(core,binder)
    return core

def _assert_no_truth(value: Any, binder) -> None:
    binder._assert_no_truth(value)
    # Additional anti-escalation checks are explicit here even though V1 core enforces the basic locks.
    if not isinstance(value,Mapping): raise MatrixAuditError("Binding record must be an object")
    if value.get("readiness",{}).get("request_scoped_visual_payload_instance_bound") is not False or value.get("readiness",{}).get("payload_instance_materialized") is not False or value.get("readiness",{}).get("video_render_ready") is not False:
        raise MatrixAuditError("Binding V2 may not claim payload/render readiness")
    if value.get("execution_boundary",{}).get("renderer_native_input_emitted") is not False or value.get("execution_boundary",{}).get("renderer_dispatch_invoked") is not False or value.get("execution_boundary",{}).get("d4_8")!="BLOCKED":
        raise MatrixAuditError("Binding V2 governance boundary weakened")
    if value.get("timing_review_reference",{}).get("policy_values_consumed") is not False or value.get("timing_review_reference",{}).get("timing_review_inheritance_approved") is not False:
        raise MatrixAuditError("Timing/review policy metadata was consumed or self-approved")

def _build(root: Path):
    contract,contract_schema,report_schema,pins=_load_contract(root)
    # Cross-check the accepted parents rather than trusting a cached or transcribed report.
    inheritance=_load_module(root/"tools/c11d/d9/d_renderer_visual_loop_timing_review_inheritance_audit.py","_c11d_matrix_v2_inheritance_parent")
    inheritance_summary=inheritance.audit(root)
    if inheritance_summary.get("approval_assertions_checked")!=19 or inheritance_summary.get("approvals_granted")!=0 or inheritance_summary.get("canonical_bound")!=1 or inheritance_summary.get("blocked_by_fixed_v1_scope")!=4:
        raise MatrixAuditError("Timing/review inheritance parent audit changed scope or approval state")
    gapmod=_load_module(root/"tools/c11d/d9/d_renderer_visual_loop_geometric_request_chain_gap_audit.py","_c11d_matrix_v2_gap_parent")
    gap=gapmod.run_audit(root)
    if gap.get("summary",{}).get("canonical_plans")!="5/5" or gap.get("summary",{}).get("source_binding_review_passes")!="1/5" or gap.get("summary",{}).get("blocked_by_fixed_v1_scope")!="4/4":
        raise MatrixAuditError("Canonical V1 request-chain gap report changed from the expected baseline")
    carrier_mod=_load_module(root/"tools/c11d/d9/d_renderer_visual_loop_timing_review_request_bound_reference_carrier.py","_c11d_matrix_v2_reference_parent")
    carrier_report=carrier_mod.build_report(root)
    cs=carrier_report.get("summary",{})
    if cs.get("request_identity_joins")!="5/5" or cs.get("policy_reference_pairs")!="45/45" or cs.get("approval_assertions_checked")!=19 or cs.get("approvals_granted")!=0:
        raise MatrixAuditError("Request-bound reference carrier parent report changed")
    carrier_report_sha=carrier_report.get("report_sha256")
    if not isinstance(carrier_report_sha,str) or digest({k:v for k,v in carrier_report.items() if k!="report_sha256"})!=carrier_report_sha:
        raise MatrixAuditError("Parent request-bound reference carrier report hash mismatch")
    binder=_load_module(root/"tools/c11d/d9/d_renderer_request_scoped_payload_binding.py","_c11d_matrix_v2_existing_binding_core")
    v1_contract,v1_schema,v1_lineage=binder._load_contract(root)
    if v1_contract.get("schema")!="C11-D-RENDERER-REQUEST-SCOPED-PAYLOAD-BINDING-CONTRACT-V1":
        raise MatrixAuditError("Canonical V1 source contract changed unexpectedly")
    bindings=[]
    for row in contract["scope"]["grammar_matrix"]:
        binding=_build_binding(root,contract,pins,carrier_report,binder,v1_contract,v1_schema,v1_lineage,row["grammar_id"])
        if binding.get("binding_sha256")!=digest({k:v for k,v in binding.items() if k!="binding_sha256"}):
            raise MatrixAuditError(f"Binding hash mismatch: {row['grammar_id']}")
        bindings.append(binding)
    request_hashes={x["source_identity"]["request_hash"] for x in bindings};plan_hashes={x["source_identity"]["plan_hash"] for x in bindings}
    shared_hashes={x["timing_review_reference"]["shared_policy_reference_set_sha256"] for x in bindings}
    selector_hashes={x["timing_review_reference"]["selector_envelope_sha256"] for x in bindings}
    policy_pairs=sum(x["timing_review_reference"]["policy_reference_count"] for x in bindings)
    if len(request_hashes)!=5 or len(plan_hashes)!=5 or len(shared_hashes)!=1 or len(selector_hashes)!=5 or policy_pairs!=45:
        raise MatrixAuditError("Request/plan/reference identity cardinality mismatch")
    report={"schema":"C11-D-D9-VISUAL-LOOP-REQUEST-SCOPED-BINDING-MATRIX-REPORT-V2","schema_version":"2.0","status":STATUS,
      "contract_sha256":file_sha(root/CONTRACT_REL),"report_schema_sha256":file_sha(root/REPORT_SCHEMA_REL),
      "source_lineage":pins,"source_lineage_sha256":digest(pins),"parent_request_bound_reference_carrier_report_sha256":carrier_report_sha,
      "bindings":bindings,
      "summary":{"direct_source_pins":"30/30","request_plans":"5/5","reference_envelopes":"5/5","request_reference_joins":"5/5","policy_reference_pairs":"45/45",
        "unique_request_hashes":"5/5","unique_plan_hashes":"5/5","exact_grammar_identity":"5/5","shared_policy_digest_unique_count":1,"selector_envelope_digests":"5/5",
        "v1_canonical_binding":"1/5","v2_preparation_source_binding":"5/5","selected_grammar_payload_instances_bound":"0/5","payloads_materialized":0,
        "approval_assertions_checked":19,"approvals_granted":0,"candidate_input_admissible":False},
      "governance":{"approval_assertions_checked":19,"approvals_granted":0,"pending_approval_assertions":19,
        "visual_loop_binding_matrix_v2_approved":False,"canonical_request_selector_matrix_approved":False,"exact_selector_payload_approved":False,
        "timing_review_inheritance_approved":False,"all_nine_shared_policy_sources_approved":False,"candidate_io_contract_complete":False,"d4_8_authorized":False,
        "request_persisted":False,"payload_materialized":False,"renderer_native_input_emitted":False,"renderer_dispatch_invoked":False,"media_created":False,
        "c11c_source_mutation":False,"candidate_input_admissible":False,"renderer":"OFF","D4.8":"BLOCKED","release_authority":"NONE","D9.10":"PREPARE_ONLY","D9.17":"BLOCKED_NO_GO"}}
    report["report_sha256"]=digest(report)
    try:
        from jsonschema import Draft202012Validator
        Draft202012Validator(report_schema).validate(report)
    except ImportError: pass
    except Exception as exc: raise MatrixAuditError(f"V2 report JSON Schema rejected report: {exc}") from exc
    if digest({k:v for k,v in report.items() if k!="report_sha256"})!=report["report_sha256"]: raise MatrixAuditError("V2 report self-hash mismatch")
    return report

_BUILD_CACHE = {}
def build_report(project_root=None) -> dict[str,Any]:
    root = _root(project_root)
    # Verify direct source pins on every invocation before consulting the process-local cache.
    _contract, _contract_schema, _report_schema, pins = _load_contract(root)
    signature = digest({
        "source_lineage": pins,
        "contract_sha256": file_sha(root/CONTRACT_REL),
        "contract_schema_sha256": file_sha(root/CONTRACT_SCHEMA_REL),
        "report_schema_sha256": file_sha(root/REPORT_SCHEMA_REL),
    })
    key = str(root)
    cached = _BUILD_CACHE.get(key)
    if cached is not None and cached["signature"] == signature:
        return copy.deepcopy(cached["report"])
    report = _build(root)
    _BUILD_CACHE[key] = {"signature": signature, "report": copy.deepcopy(report)}
    return report
def validate_report(candidate: Mapping[str,Any], project_root=None) -> bool:
    if not isinstance(candidate,Mapping): raise MatrixAuditError("Report must be an object")
    root=_root(project_root);actual=dict(candidate)
    if actual.get("report_sha256")!=digest({k:v for k,v in actual.items() if k!="report_sha256"}): raise MatrixAuditError("V2 report self-hash mismatch")
    expected=build_report(root)
    if actual!=expected: raise MatrixAuditError("V2 report diverges from canonical requests, source binding core, metadata references or governance locks")
    return True

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--root",required=True);p.add_argument("--full-report",action="store_true");a=p.parse_args(argv)
    try:
        r=build_report(a.root);s=r["summary"]
        print("C11-D VISUAL LOOP REQUEST-SCOPED BINDING MATRIX V2 AUDIT PASS | direct_source_pins="+s["direct_source_pins"]+" | request_plans="+s["request_plans"]+" | reference_envelopes="+s["reference_envelopes"]+" | request_reference_joins="+s["request_reference_joins"]+" | policy_reference_pairs="+s["policy_reference_pairs"]+" | exact_grammar_identity="+s["exact_grammar_identity"]+" | unique_request_hashes="+s["unique_request_hashes"]+" | unique_plan_hashes="+s["unique_plan_hashes"]+" | v1_canonical_binding="+s["v1_canonical_binding"]+" | v2_preparation_source_binding="+s["v2_preparation_source_binding"]+" | selected_grammar_payload_instances_bound="+s["selected_grammar_payload_instances_bound"]+" | payloads_materialized=0 | approval_assertions_checked=19 | approvals_granted=0 | candidate_input_admissible=false | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
        print("C11D_VISUAL_LOOP_REQUEST_SCOPED_BINDING_MATRIX_V2_REPORT="+canonical(r))
        if a.full_report: print(json.dumps(r,ensure_ascii=False,indent=2,sort_keys=True))
        return 0
    except Exception as exc:
        print(f"C11-D VISUAL LOOP REQUEST-SCOPED BINDING MATRIX V2 AUDIT FAIL | {exc} | candidate_input_admissible=false | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
        return 1
if __name__=="__main__": raise SystemExit(main())
