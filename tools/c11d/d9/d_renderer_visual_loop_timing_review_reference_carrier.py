#!/usr/bin/env python3
"""Prepare and audit selector-scoped timing/review reference envelopes; never bind/render them."""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, sys
from pathlib import Path
from typing import Any
try:
    from jsonschema import Draft202012Validator
except ImportError as exc:
    raise RuntimeError("jsonschema is required by the C11-D contract audits") from exc

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_VISUAL_LOOP_TIMING_REVIEW_REFERENCE_CARRIER_CANDIDATE_V1.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_VISUAL_LOOP_TIMING_REVIEW_REFERENCE_CARRIER_CANDIDATE_SCHEMA_V1.json")
REPORT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_VISUAL_LOOP_TIMING_REVIEW_REFERENCE_CARRIER_REPORT_SCHEMA_V1.json")
EXPECTED_C11C = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
EXPECTED_GRAMMARS = ["harmonic_membrane", "interference_plane", "parametric_ribbon", "lattice_wave", "orbital_wave"]
EXPECTED_POLICY_IDS = [
 "LOOP_DRILL_EDITORIAL_FIELD_WINDOW_V1", "UNIFIED_DELIVERY_TIMEBASE_V1", "UNIFIED_PRESENTATION_REGION_V1",
 "UNIFIED_AUDIO_MUSIC_DELIVERY_V1", "SOURCE_BOUND_TEMPORAL_PREVIEW_V1", "EDITORIAL_REVIEW_MANIFEST_V1",
 "UNIFIED_CONTENT_REVIEW_V1", "NEUTRAL_FRAME_PROGRAM_V1", "CANDIDATE_LOGICAL_COMPOSITION_V1"]

class ReferenceCarrierError(RuntimeError): pass
def require(condition: bool, message: str) -> None:
    if not condition: raise ReferenceCarrierError(message)
def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()
def file_sha(path: Path) -> str:
    try: return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as exc: raise ReferenceCarrierError(f"Cannot read pinned source: {path}") from exc
def read_json(path: Path) -> Any:
    try: return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc: raise ReferenceCarrierError(f"Invalid JSON {path}: {exc}") from exc

def load_module(path: Path, name: str):
    spec=importlib.util.spec_from_file_location(name,path)
    require(spec is not None and spec.loader is not None, f"Cannot load parent audit module: {path}")
    module=importlib.util.module_from_spec(spec); sys.modules[name]=module; spec.loader.exec_module(module)
    return module

def verify_direct_pins(root: Path, contract: dict[str, Any]) -> int:
    lineage=contract.get("source_lineage")
    require(isinstance(lineage,list) and len(lineage)==16, "Exactly 16 direct source pins are required")
    seen=set()
    for i,row in enumerate(lineage):
        require(isinstance(row,dict) and set(row)=={"path","sha256"}, "Malformed source lineage row")
        rel=row["path"]
        require(isinstance(rel,str) and rel and not Path(rel).is_absolute() and ".." not in Path(rel).parts and "\\" not in rel, f"Unsafe source path: {rel!r}")
        require(rel not in seen, f"Duplicate source pin: {rel}"); seen.add(rel)
        actual=file_sha(root/rel)
        require(actual==row["sha256"], f"Pinned source drift: {rel}; expected={row['sha256']}; actual={actual}")
        if i==0: require(rel=="release/C11C_FREEZE_PACKAGE_MANIFEST.json" and actual==EXPECTED_C11C, "Frozen C11-C manifest must be first pin")
    return len(lineage)

def _policy_descriptor(ref: dict[str, Any]) -> dict[str, Any]:
    assertions=ref.get("approval_assertions",{})
    require(isinstance(assertions,dict) and len(assertions)>0, f"Missing approval assertions: {ref.get('id')}")
    require(all(value is False for value in assertions.values()), f"Unapproved policy has changed approval state: {ref.get('id')}")
    # Metadata only: deliberately omit the policy's actual content, instructions, values and review bodies.
    return {"id":ref["id"],"path":ref["path"],"sha256":ref["sha256"],"expected_status":ref["expected_status"],
            "scope":ref["scope"],"approval_assertion_count":len(assertions),"all_approval_assertions_false":True,
            "reference_role":"PROVENANCE_ONLY_NOT_INSTRUCTIONS"}

def build_envelope(selector: dict[str, Any], policy_refs: list[dict[str, Any]]) -> dict[str, Any]:
    require(selector.get("grammar_id") in EXPECTED_GRAMMARS, "Unsupported geometric grammar")
    idx=EXPECTED_GRAMMARS.index(selector["grammar_id"])
    require(selector.get("grammar_index")==idx, "Grammar identity/index mismatch")
    require(selector.get("content_type")=="visual_loops" and selector.get("family_id")=="c11c_geometric_waves_v1", "Selector scope mismatch")
    require(len(policy_refs)==9 and [p.get("id") for p in policy_refs]==EXPECTED_POLICY_IDS, "Policy reference identity/order mismatch")
    descriptors=[_policy_descriptor(p) for p in policy_refs]
    shared_digest=digest(descriptors)
    selection={k:selector[k] for k in ("content_type","family_id","grammar_id","grammar_index","shader_branch")}
    identity_material={"schema":"C11-D-VISUAL-LOOP-TIMING-REVIEW-REFERENCE-ENVELOPE-V1","schema_version":"1.0",
      "mode":"SELECTOR_SCOPED_REFERENCE_METADATA_ONLY","selection":selection,"policy_references":descriptors,
      "shared_reference_set_sha256":shared_digest,"policy_source_bodies_copied":False,"policy_values_copied":False,
      "renderer_instructions_emitted":False,"canonical_request_modified":False,"canonical_payload_modified":False}
    selector_digest=digest(identity_material)
    return {**identity_material,"selector_envelope_sha256":selector_digest,"request_bound":False,"payload_materialized":False,
      "renderer_native_input_emitted":False,"canonical_binding_admitted":False,"policy_approval_state":"UNAPPROVED_PROPOSALS_REFERENCE_ONLY"}

def verify_contract_schema(contract: dict[str, Any], schema: dict[str, Any], report_schema: dict[str, Any]) -> None:
    for item in (schema,report_schema):
        require(item.get("$schema")=="https://json-schema.org/draft/2020-12/schema", "JSON Schema must use Draft 2020-12")
        Draft202012Validator.check_schema(item)
    errors=sorted(Draft202012Validator(schema).iter_errors(contract),key=lambda e:list(e.absolute_path))
    if errors:
        e=errors[0]; raise ReferenceCarrierError(f"Contract schema rejected {'/'.join(map(str,e.absolute_path)) or '<root>'}: {e.message}")

def audit(root_path: Path | str) -> dict[str, Any]:
    root=Path(root_path).resolve()
    contract=read_json(root/CONTRACT_REL); schema=read_json(root/SCHEMA_REL); report_schema=read_json(root/REPORT_SCHEMA_REL)
    verify_contract_schema(contract,schema,report_schema)
    require(contract.get("schema")=="C11-D-D10-VISUAL-LOOP-TIMING-REVIEW-REFERENCE-CARRIER-CANDIDATE-V1", "Contract identity mismatch")
    require(contract.get("status")=="PREPARATION_ONLY_REFERENCE_CARRIER_NOT_CANONICAL_BINDING_NOT_POLICY_APPROVAL", "Contract status self-promotion")
    require(contract.get("authority",{}).get("frozen_c11c_manifest_sha256")==EXPECTED_C11C, "Frozen C11-C pin changed")
    require(contract.get("authority",{}).get("canonical_binder_v1_mutated") is False and contract.get("authority",{}).get("canonical_binding_v2_activated") is False, "Canonical binder boundary changed")
    require(contract.get("authority",{}).get("policy_approval_granted") is False and contract.get("authority",{}).get("renderer_admission_granted") is False, "Governance authority changed")
    pin_count=verify_direct_pins(root,contract)
    parent_contract=read_json(root/"definitions/c11d/production/D_RENDERER_VISUAL_LOOP_TIMING_REVIEW_INHERITANCE_V1.json")
    require(file_sha(root/"definitions/c11d/production/D_RENDERER_VISUAL_LOOP_TIMING_REVIEW_INHERITANCE_V1.json")==contract["parents"]["timing_review_inheritance_contract_sha256"], "Parent timing/review contract pin mismatch")
    # Run the two canonical parent audits. The first validates 17 source pins + 19 false approval assertions.
    timing_module=load_module(root/"tools/c11d/d9/d_renderer_visual_loop_timing_review_inheritance_audit.py","_c11d_parent_timing_review_audit")
    timing_summary=timing_module.audit(root)
    gap_module=load_module(root/"tools/c11d/d9/d_renderer_visual_loop_geometric_request_chain_gap_audit.py","_c11d_parent_request_chain_gap_audit")
    gap_report=gap_module.run_audit(root)
    require(gap_report.get("summary",{}).get("canonical_plans")=="5/5", "Parent chain audit canonical plans not 5/5")
    require(gap_report.get("summary",{}).get("source_binding_review_passes")=="1/5", "Parent chain audit binding scope unexpectedly changed")
    require(gap_report.get("summary",{}).get("blocked_by_fixed_v1_scope")=="4/4", "Parent chain audit blocked scope unexpectedly changed")
    require(gap_report.get("summary",{}).get("candidate_input_admissible") is False, "Parent chain audit unexpectedly admitted candidate input")
    require(timing_summary.get("approval_assertions_checked")==19 and timing_summary.get("approvals_granted")==0, "Parent policy approvals are not all false")
    
    scope=contract["scope"]; timing_scope=parent_contract["scope"]
    require(scope.get("selector_ids")==EXPECTED_GRAMMARS, "Candidate selector list changed")
    require([r.get("grammar_id") for r in scope.get("selector_rows",[]) ]==EXPECTED_GRAMMARS, "Candidate selector rows/order changed")
    require(timing_scope.get("selector_rows") and [r["grammar_id"] for r in timing_scope["selector_rows"]]==EXPECTED_GRAMMARS, "Parent timing selector rows differ")
    prefs=parent_contract.get("shared_policy_refs",[])
    require(len(prefs)==9 and [p.get("id") for p in prefs]==EXPECTED_POLICY_IDS, "Parent policy reference set differs")
    require(scope.get("family_exceptions")==[], "Undocumented family exception added")
    require(scope.get("inheritance_mode")=="PROPOSED_SHARED_POLICY_DEFAULT", "Inheritance must remain proposal-only")
    
    gap_by_id={c["grammar_id"]:c for c in gap_report["cases"]}
    envelopes=[]
    for row in scope["selector_rows"]:
        case=gap_by_id.get(row["grammar_id"])
        require(case is not None, f"Missing parent chain case: {row['grammar_id']}")
        require(case.get("grammar_index")==row["grammar_index"] and case.get("shader_branch")==row["shader_branch"], f"Selector matrix drift: {row['grammar_id']}")
        require(case.get("request_scoped_source_binding_status")==row["current_canonical_binding_status"], f"Current binding status drift: {row['grammar_id']}")
        require(row.get("reference_carrier_state")=="PREPARED_METADATA_ONLY_NOT_CANONICAL_BINDING" and row.get("canonical_binding_admitted") is False, "Reference envelope self-promoted")
        envelopes.append(build_envelope(row,prefs))
    require(len(envelopes)==5, "Exactly five selector-scoped envelopes required")
    require(len({e["shared_reference_set_sha256"] for e in envelopes})==1, "Shared policy ref bundle digest is not consistent")
    require(len({e["selector_envelope_sha256"] for e in envelopes})==5, "Selector identity is not bound into unique envelope digests")
    require(sum(e["request_bound"] is True for e in envelopes)==0, "Reference-only carrier must not claim request binding")
    require(sum(e["canonical_binding_admitted"] is True for e in envelopes)==0, "Reference-only carrier must not admit canonical binding")
    
    report={"schema":"C11-D-VISUAL-LOOP-TIMING-REVIEW-REFERENCE-CARRIER-REPORT-V1","schema_version":"1.0",
      "status":"PASS_PREPARATION_ONLY_REFERENCE_ENVELOPES_VERIFIED_NOT_BINDING_NOT_APPROVED",
      "contract_sha256":file_sha(root/CONTRACT_REL),"source_lineage":[dict(x) for x in contract["source_lineage"]],"envelopes":envelopes,
      "summary":{"direct_source_pins":"16/16","selectors":5,"policy_refs_per_selector":9,"reference_descriptors":45,"prepared_envelopes":"5/5",
        "shared_reference_set_digest_unique_count":1,"selector_envelope_digest_unique_count":"5/5","canonical_binding_review":"1/5",
        "blocked_by_fixed_v1_scope":"4/4","approval_assertions_checked":19,"approvals_granted":0,"candidate_input_admissible":False},
      "governance":{"timing_review_inheritance_approved":False,"canonical_request_selector_matrix_approved":False,
        "exact_selector_payload_approved":False,"shared_policy_approved":False,"renderer_baseline_approved":False,"renderer_baseline_frozen":False,
        "godot_invoked":False,"request_persisted":False,"payload_materialized":False,"renderer_native_input_emitted":False,
        "renderer_dispatch_invoked":False,"media_created":False,"c11c_source_mutation":False,"renderer":"OFF","D4.8":"BLOCKED",
        "release_authority":"NONE","D9.10":"PREPARE_ONLY","D9.17":"BLOCKED_NO_GO"}}
    report["report_sha256"]=digest(report)
    errors=sorted(Draft202012Validator(report_schema).iter_errors(report),key=lambda e:list(e.absolute_path))
    if errors:
        e=errors[0]; raise ReferenceCarrierError(f"Report schema rejected {'/'.join(map(str,e.absolute_path)) or '<root>'}: {e.message}")
    require(report["report_sha256"]==digest({k:v for k,v in report.items() if k!="report_sha256"}), "Report self-hash mismatch")
    return report

def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument("--root",required=True); ap.add_argument("--full-report",action="store_true")
    args=ap.parse_args(argv)
    try:
        r=audit(args.root); s=r["summary"]
        print("C11-D VISUAL LOOP TIMING/REVIEW REFERENCE CARRIER AUDIT PASS | direct_source_pins=16/16 | selectors=5/5 | policy_refs=9/9 | reference_descriptors=45/45 | prepared_envelopes=5/5 | shared_reference_digest=1 | selector_envelope_digests=5/5 | canonical_binding=1/5 | blocked_by_fixed_v1_scope=4/4 | approval_assertions_checked=19 | approvals_granted=0 | candidate_input_admissible=false | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
        print("C11D_TIMING_REVIEW_REFERENCE_CARRIER_REPORT="+canonical(r))
        if args.full_report: print(json.dumps(r,ensure_ascii=False,indent=2,sort_keys=True))
        return 0
    except Exception as exc:
        print(f"C11-D VISUAL LOOP TIMING/REVIEW REFERENCE CARRIER AUDIT FAIL | {exc} | candidate_input_admissible=false | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
        return 1
if __name__=="__main__": raise SystemExit(main())
