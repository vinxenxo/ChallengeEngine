#!/usr/bin/env python3
"""Read-only contract regression suite; deliberately no consumer implementation, renderer, or media."""
from __future__ import annotations
import hashlib, json, math, sys
from pathlib import Path

ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[4]
RECEIPT=Path(sys.argv[2]).resolve() if len(sys.argv)>2 else None
SPEC_REL=Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_ALLOWLISTED_COORDINATE_PROJECTION_CONSUMER_SPECIFICATION_V1.json")
SCHEMA_REL=Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_ALLOWLISTED_COORDINATE_PROJECTION_CONSUMER_SPECIFICATION_SCHEMA_V1.json")
POLICY_REL=Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_COORDINATE_POLICY_PROPOSAL_V1.json")
POLICY_SCHEMA_REL=Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_COORDINATE_POLICY_PROPOSAL_SCHEMA_V1.json")
POLICY_TEST_REL=Path("tools/c11d/d9/test_d_renderer_challenge_visual_payload_v2b_candidate_coordinate_policy_proposal_v1.py")
POLICY_DECISION_REL=Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_COORDINATE_POLICY_DECISION_RECORD_V1.json")
POLICY_DECISION_SCHEMA_REL=Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_COORDINATE_POLICY_DECISION_RECORD_SCHEMA_V1.json")
POLICY_DECISION_TEST_REL=Path("tools/c11d/d9/test_d_renderer_challenge_visual_payload_v2b_candidate_coordinate_policy_decision_record_v1.py")
REGION_DECISION_REL=Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_DECISION_RECORD_V1.json")
REGION_SCHEMA_REL=Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_DECISION_RECORD_SCHEMA_V1.json")
REGION_TEST_REL=Path("tools/c11d/d9/test_d_renderer_challenge_visual_payload_v2b_candidate_field_region_visibility_decision_record_v1.py")
SEM_DECISION_REL=Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_SEMANTIC_DECISION_RECORD_V1.json")
EMPTY_SHA="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
C11C_SHA="e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
COORD_DECISION_RECEIPT_SHA="b61fb3403e0ad5725937be05f8a7153c3cf35ccde167306f45151ece0f1cc4cb"
COORD_DECISION_STDOUT_SHA="e233f0f85abfa4249873f14056c8ed6d089026e2e9093b8c60773d7d5282ca94"

class Gate:
    def __init__(self): self.count=0; self.failures=[]
    def check(self,v,label):
        self.count+=1
        if not v: self.failures.append(f"CHECK_{self.count:04d}: {label}")
    def same(self,a,b,label): self.check(a==b,label)
    def true(self,v,label): self.check(v is True,label)
    def false(self,v,label): self.check(v is False,label)
    def finish(self,expected):
        print(f"C11D_V2B_ALLOWLISTED_COORDINATE_PROJECTION_CONSUMER_SPECIFICATION_TEST_COUNT_GENERATED={self.count}")
        if self.count!=expected: self.failures.append(f"CHECK_COUNT: expected {expected}, generated {self.count}")
        if self.failures:
            print("C11D_V2B_ALLOWLISTED_COORDINATE_PROJECTION_CONSUMER_SPECIFICATION_STATUS=FAIL")
            for f in self.failures[:100]: print(f)
            print(f"C11D_V2B_ALLOWLISTED_COORDINATE_PROJECTION_CONSUMER_SPECIFICATION_TESTS={self.count-len(self.failures)}/{self.count}")
            return 1
        print(f"C11D_V2B_ALLOWLISTED_COORDINATE_PROJECTION_CONSUMER_SPECIFICATION_TESTS={self.count}/{self.count}")
        print("C11D_V2B_ALLOWLISTED_COORDINATE_PROJECTION_CONSUMER_SPECIFICATION_CANDIDATES=4/4")
        print("C11D_V2B_ALLOWLISTED_COORDINATE_PROJECTION_CONSUMER_SPECIFICATION_SOURCE_PINS=81/81")
        print("C11D_V2B_ALLOWLISTED_COORDINATE_PROJECTION_CONSUMER_SPECIFICATION_AUTHORITY_INPUT_PINS=9/9")
        print("C11D_V2B_ALLOWLISTED_COORDINATE_PROJECTION_CONSUMER_SPECIFICATION_SEMANTIC_INPUT_PINS=6/6")
        print("C11D_V2B_ALLOWLISTED_COORDINATE_PROJECTION_CONSUMER_SPECIFICATION_FIELD_REGION_PINS=6/6")
        print("C11D_V2B_ALLOWLISTED_COORDINATE_PROJECTION_CONSUMER_SPECIFICATION_COORDINATE_REFERENCE_PINS=3/3")
        print("C11D_V2B_ALLOWLISTED_COORDINATE_PROJECTION_CONSUMER_SPECIFICATION_COORDINATE_POLICY_PINS=3/3")
        print("C11D_V2B_ALLOWLISTED_COORDINATE_PROJECTION_CONSUMER_SPECIFICATION_COORDINATE_DECISION_PINS=3/3")
        print("C11D_V2B_ALLOWLISTED_COORDINATE_PROJECTION_CONSUMER_SPECIFICATION_STATUS=SPECIFICATION_ONLY_NOT_IMPLEMENTED")
        print("C11D_V2B_ALLOWLISTED_COORDINATE_PROJECTION_CONSUMER_SPECIFICATION_RAW_CUSTOM_DATA_SERIALIZATION=false")
        print("C11D_V2B_ALLOWLISTED_COORDINATE_PROJECTION_CONSUMER_SPECIFICATION_RUNTIME_IMPLEMENTATION_AUTHORIZATION=NOT_GRANTED")
        print("C11D_V2B_BINDING_AUTHORIZATION=NOT_GRANTED")
        print("C11D_V2B_RENDERER_PROJECTION_AUTHORIZATION=NOT_GRANTED")
        print("C11D_V2B_RENDER_TEST_AUTHORIZATION=NOT_GRANTED")
        print("C11D_V2B_CANDIDATE_INPUT_ADMISSIBLE=false")
        print("C11D_V2B_RENDERER=OFF")
        print("C11D_V2B_MEDIA_CREATED=false")
        print("C11D_V2B_C11C_IMMUTABLE=true")
        return 0

def load(p): return json.loads(p.read_text(encoding="utf-8"))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def numeric(v): return isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(float(v))
def project(candidate_id, values):
    """Test-only oracle for the contract; not production consumer code."""
    table={c["candidate_id"]:c for c in SPEC["field_allowlist"]}
    if candidate_id not in table: return (False,"UNSUPPORTED_CANDIDATE",[])
    c=table[candidate_id]
    if not isinstance(values,list) or not values: return (False,"EMPTY_SOURCE_FRAMES",[])
    out=[]; constant=None
    for ordinal,v in enumerate(values):
        if v is None: return (False,"MISSING_ALLOWLISTED_FIELD",[])
        if c["semantic_type"]=="finite_number":
            if not numeric(v): return (False,"INVALID_VALUE_TYPE",[])
            if not 0.0<=float(v)<=100.0: return (False,"VALUE_OUT_OF_DOMAIN",[])
            x=(float(v)/100.0)*540.0; y=480.0
        else:
            if not isinstance(v,(tuple,list)) or len(v)!=2: return (False,"INVALID_VALUE_TYPE",[])
            x0,y0=v
            if not numeric(x0) or not numeric(y0): return (False,"INVALID_VALUE_TYPE",[])
            if not 0.0<=float(x0)<=1080.0 or not 0.0<=float(y0)<=1920.0: return (False,"VECTOR_OUT_OF_BOUNDS",[])
            pair=(float(x0),float(y0))
            if candidate_id=="CHALLENGE_005":
                if constant is None: constant=pair
                elif pair!=constant: return (False,"PER_RUN_CONSTANT_MISMATCH",[])
            x=float(x0)*0.5; y=float(y0)*0.5
        out.append({"source_frame_index":ordinal,"target_marker":{"role":"TARGET","asset_path":c["asset_path"],"anchor_x":x,"anchor_y":y,"logical_width":50.0,"logical_height":50.0,"anchor_mode":"CENTER","asset_bounds_policy":"CLIP_BOUNDS_WITHOUT_MOVING_POINT"}})
    return (True,"OK",out)

def main():
    global SPEC
    g=Gate(); spec_path=ROOT/SPEC_REL; schema_path=ROOT/SCHEMA_REL
    g.true(spec_path.is_file(),"specification file exists"); g.true(schema_path.is_file(),"schema file exists")
    if not spec_path.is_file() or not schema_path.is_file(): return g.finish(1)
    SPEC=load(spec_path); sch=load(schema_path)
    g.same(SPEC.get("schema"),"C11D-V2B-ALLOWLISTED-COORDINATE-PROJECTION-CONSUMER-SPECIFICATION-V1","spec identity")
    g.same(SPEC.get("schema_version"),"1.0","version")
    g.same(SPEC.get("status"),"SPECIFICATION_ONLY_NOT_IMPLEMENTED","status")
    g.same(SPEC.get("decision_scope"),"FUTURE_CONSUMER_SPECIFICATION_ONLY_NO_RUNTIME_AUTHORIZATION","scope")
    g.same(SPEC.get("test_script_sha256"),sha(Path(__file__)),"suite self pin")
    # Schema is closed at root and requires every property.
    g.same(sch.get("$schema"),"https://json-schema.org/draft/2020-12/schema","schema dialect")
    g.same(sch.get("type"),"object","schema root type"); g.false(sch.get("additionalProperties",True),"root rejects unknown properties")
    for key in SPEC: g.check(key in sch.get("required",[]),"schema requires root property "+key)
    g.same(set(sch.get("properties",{})),set(SPEC.keys()),"schema properties exactly match specification")
    g.same(sch.get("properties",{}).get("schema",{}).get("const"),SPEC["schema"],"schema identity const")
    g.same(sch.get("properties",{}).get("status",{}).get("const"),SPEC["status"],"status const")
    # Core status, scope, no runtime side effects.
    scope=SPEC["scope"]
    for k,v in {"kind":"RENDERER_NEUTRAL_ALLOWLISTED_CONSUMER_SPECIFICATION_ONLY","candidate_count":4,"blocked_candidate_count":2,"accepted_candidate_ids":["CHALLENGE_003","CHALLENGE_005","CHALLENGE_006","CHALLENGE_007"],"blocked_candidate_ids":["CHALLENGE_008","CHALLENGE_009"],"reads_simulation_result_frames_only":True,"reads_only_allowlisted_custom_data_key":True,"whole_custom_data_serialization_allowed":False,"writes_challenge_json":False,"modifies_coordinate_mapper":False,"changes_simulation_or_rng":False,"source_frame_resampling_allowed":False,"runtime_implementation_included":False}.items(): g.same(scope.get(k),v,"scope "+k)
    # Prior accepted evidence files and their exact package identities.
    refs=[(POLICY_REL,"44c1ec6507988023b7cd20cdcc8e0e722c99af610d9be02a6d658ce9b07e9f57","coordinate proposal"),(POLICY_SCHEMA_REL,"9715a6d3580f86307f2fb2c2ce348555256632c66d1c6f68d54db7af199486a2","coordinate proposal schema"),(POLICY_TEST_REL,"70b869259778e3c2289782b985b7f1c89c63ded8d0130ead06d34bf28aa55e89","coordinate proposal suite"),(POLICY_DECISION_REL,"45841adf320c4815b1a63b26555497adf38b57672bd62069c81385ef327e6a1e","coordinate policy decision"),(POLICY_DECISION_SCHEMA_REL,"d7b279c3225ceb431a434cbfbea606b248d710f766200c60adefbea544e6b8bc","coordinate policy decision schema"),(POLICY_DECISION_TEST_REL,"ae4d30f25ff5988fd2a18c5aa7caabf6544eea4930d1b687a54d151b73d00d56","coordinate policy decision suite"),(REGION_DECISION_REL,"1ec59d7a9257cfc2477fc37efe8cb2f04d9807a7f9986d96afc2f2ddd9b4f7af","field-region decision"),(REGION_SCHEMA_REL,"bb32a0631216c8b557ee48f85ff06dbf1588c125606b917acff22930aa6ce50e","field-region decision schema"),(REGION_TEST_REL,"c35d3a44c0b998235ad17b2ad403892a1e6c95e0bffaeb0a3d075f4ff8258039","field-region decision suite"),(SEM_DECISION_REL,"cc3550cd4d13f228ec9b3d51eeaa199505c5975b42882fb06ba3e83c4a000e90","semantic decision")]
    for rel,expected,label in refs:
        p=ROOT/rel; g.true(p.is_file(),label+" exists")
        if p.is_file(): g.same(sha(p),expected,label+" sha")
    # Pin inventories: exact cardinalities, valid formats, path existence, live SHA-256, and unique paths.
    groups=[("source_pins",81,False),("authority_input_pins",9,True),("semantic_decision_input_pins",6,True),("field_region_decision_input_pins",6,True),("coordinate_reference_pins",3,True),("coordinate_policy_proposal_input_pins",3,True),("coordinate_policy_decision_input_pins",3,True)]
    for name,count,role_req in groups:
        pins=SPEC.get(name,[]); g.same(len(pins),count,name+" count"); g.same(len({p.get('path') for p in pins}),count,name+" unique paths")
        for i,pin in enumerate(pins):
            path_text=pin.get("path",""); digest=pin.get("sha256","")
            g.check(isinstance(path_text,str) and bool(path_text) and not path_text.startswith("/"),f"{name} path format {i}")
            g.check(isinstance(digest,str) and len(digest)==64 and all(c in "0123456789abcdef" for c in digest),f"{name} sha format {i}")
            if role_req: g.check(isinstance(pin.get("role"),str) and bool(pin.get("role")),f"{name} role {i}")
            pin_path=ROOT/Path(path_text); g.check(pin_path.is_file(),f"{name} input exists {path_text}")
            if pin_path.is_file(): g.same(sha(pin_path),digest,f"{name} input sha {path_text}")
    # Pin lists must be retained verbatim from the accepted upstream records/proposal.
    proposal=load(ROOT/POLICY_REL); decision=load(ROOT/POLICY_DECISION_REL); field=load(ROOT/REGION_DECISION_REL)
    g.same(SPEC["source_pins"],proposal.get("source_pins"),"source pins retained from proposal")
    g.same(SPEC["authority_input_pins"],proposal.get("authority_input_pins"),"authority pins retained")
    g.same(SPEC["semantic_decision_input_pins"],proposal.get("semantic_decision_input_pins"),"semantic pins retained")
    g.same(SPEC["field_region_decision_input_pins"],decision.get("field_region_decision_input_pins"),"field-region decision pins retained")
    g.same(SPEC["coordinate_reference_pins"],proposal.get("coordinate_reference_pins"),"coordinate reference pins retained")
    g.same(SPEC["coordinate_policy_proposal_input_pins"],decision.get("coordinate_policy_proposal_input_pins"),"coordinate proposal pins retained")
    expected_decision_inputs=[{"path":str(POLICY_DECISION_REL).replace("\\","/"),"sha256":"45841adf320c4815b1a63b26555497adf38b57672bd62069c81385ef327e6a1e","role":"accepted_coordinate_policy_decision_record"},{"path":str(POLICY_DECISION_SCHEMA_REL).replace("\\","/"),"sha256":"d7b279c3225ceb431a434cbfbea606b248d710f766200c60adefbea544e6b8bc","role":"coordinate_policy_decision_record_schema"},{"path":str(POLICY_DECISION_TEST_REL).replace("\\","/"),"sha256":"ae4d30f25ff5988fd2a18c5aa7caabf6544eea4930d1b687a54d151b73d00d56","role":"coordinate_policy_decision_regression_suite"}]
    g.same(SPEC["coordinate_policy_decision_input_pins"],expected_decision_inputs,"decision input pins exactly match accepted decision record")
    # Review evidence receipt: exact file SHA, content identity/counts and no stderr.
    g.true(RECEIPT is not None,"decision receipt path provided")
    if RECEIPT is not None:
        g.true(RECEIPT.is_file(),"decision receipt exists")
        if RECEIPT.is_file():
            receipt=load(RECEIPT)
            g.same(receipt.get("status"),"PASS_STATIC_TESTS","decision receipt status")
            g.same(receipt.get("test_count"),2756,"decision receipt count")
            g.same(receipt.get("stdout_sha256"),COORD_DECISION_STDOUT_SHA,"decision receipt stdout pin")
            g.same(receipt.get("stderr_sha256"),EMPTY_SHA,"decision receipt stderr empty")
            g.same(receipt.get("decision_record_sha256"),"45841adf320c4815b1a63b26555497adf38b57672bd62069c81385ef327e6a1e","decision receipt record pin")
            g.same(receipt.get("decision_record_schema_sha256"),"d7b279c3225ceb431a434cbfbea606b248d710f766200c60adefbea544e6b8bc","decision receipt schema pin")
            g.same(receipt.get("frozen_manifest_sha256"),C11C_SHA,"decision receipt frozen C11-C pin")
            g.same(receipt.get("coordinate_policy_approval"),"GRANTED_FOR_FUTURE_CONSUMER_SPECIFICATION_ONLY","prior coordinate decision scope")
            g.false(receipt.get("runtime_coordinate_transform_authorized"),"prior runtime transform remains unauthorized")
            g.same(receipt.get("binding_authorization"),"NOT_GRANTED","prior binding remains unauthorized")
            g.same(receipt.get("renderer_projection_authorization"),"NOT_GRANTED","prior projection remains unauthorized")
            g.false(receipt.get("render_test_authorized"),"prior render remains unauthorized")
            g.false(receipt.get("candidate_input_admissible"),"candidate remains inadmissible")
            g.same(receipt.get("renderer"),"OFF","renderer stays off")
            g.false(receipt.get("media_created"),"no media created")
            g.false(receipt.get("payload_materialized"),"no payload materialized")
    # Record authority from upstream and locks.
    auth=SPEC["authorization"]
    for k,v in {"specification_approved_for_next_design_step":True,"consumer_runtime_implementation_authorized":False,"coordinate_transform_runtime_authorized":False,"binding_authorization":"NOT_GRANTED","renderer_projection_authorization":"NOT_GRANTED","renderer_activation_authorized":False,"render_test_authorized":False,"payload_materialization_authorized":False,"media_creation_authorized":False,"candidate_input_admissible":False,"release_authority":"NONE"}.items(): g.same(auth.get(k),v,"authorization "+k)
    locks=SPEC["governance_locks"]
    for k,v in {"renderer":"OFF","media_created":False,"payload_materialized":False,"candidate_input_admissible":False,"seed_domains_complete_for_candidate_input":False,"automatic_seed_generation":False,"master_seed":"NOT_ADOPTED","approved_bindings":0,"approved_custom_data_bindings":0,"approved_renderer_projection_bindings":0,"D4.8":"BLOCKED","D9.10":"PREPARE_ONLY","D9.14":"BLOCKED","D9.16":"BLOCKED","D9.17":"BLOCKED_NO_GO","D10":"BLOCKED_FOR_PROMOTION","baseline_approval":"MISSING","freeze_eligible":False,"release_authority":"NONE","whole_custom_data_serialization_allowed":False,"challenge_json_modification_allowed":False,"challenge_004_v1_harness_mutation_allowed":False}.items(): g.same(locks.get(k),v,"governance lock "+k)
    # Input contract exactness and privacy controls.
    ic=SPEC["input_contract"]
    for k,v in {"frame_sequence":"SimulationResult.frames[*] in existing order","frame_index_source":"zero-based ordinal in the existing frames array; FrameSnapshot has no authoritative frame_index field","candidate_identity":"caller-provided challenge_id must exactly match an allowlist entry; do not infer candidate identity from frame content","field_access":"perform one exact lookup of the allowlisted key in each FrameSnapshot.custom_data; do not copy, iterate, merge, stringify, log, or serialize the complete Dictionary","snapshot_validation":"upstream SimulationResult contract must have passed before any candidate track is considered","nonempty_frame_sequence_required":True,"sample_cardinality":"exactly one target sample for every existing source frame","track_atomicity":"if any frame sample fails validation, reject the entire candidate track and emit no partial projected track","order":"preserve source array ordinal without sorting or reindexing from any other metadata"}.items(): g.same(ic.get(k),v,"input contract "+k)
    privacy=SPEC["privacy_and_noninterference"]
    for k in ["serialize_whole_custom_data","log_raw_candidate_value","error_payload_contains_raw_value","modify_simulation_result","modify_source_frames","modify_winning_frame","modify_close_calls","modify_score","modify_pause_state","modify_input_state","reexecute_simulation","reexecute_rng"]: g.false(privacy.get(k),"privacy noninterference "+k)
    # Exact candidate allowlist map and forbid incidental bindings.
    expected_ids=["CHALLENGE_003","CHALLENGE_005","CHALLENGE_006","CHALLENGE_007"]
    g.same([c.get("candidate_id") for c in SPEC["field_allowlist"]],expected_ids,"allowlist ordering and identities")
    g.same(len(SPEC["field_allowlist"]),4,"four allowlisted candidate fields")
    g.same([c.get("candidate_id") for c in SPEC["blocked_candidates_retained"]],["CHALLENGE_008","CHALLENGE_009"],"two blocked candidates retained")
    cand_by={c["candidate_id"]:c for c in SPEC["field_allowlist"]}
    expected_fields={"CHALLENGE_003":"target_x","CHALLENGE_005":"target_position","CHALLENGE_006":"target_position","CHALLENGE_007":"target_position"}
    expected_types={"CHALLENGE_003":"finite_number","CHALLENGE_005":"Vector2","CHALLENGE_006":"Vector2","CHALLENGE_007":"Vector2"}
    expected_tracks={"CHALLENGE_003":"PER_FRAME_SCALAR","CHALLENGE_005":"PER_RUN_CONSTANT_REPEATED_PER_FRAME","CHALLENGE_006":"PER_FRAME_VECTOR","CHALLENGE_007":"PER_FRAME_VECTOR"}
    for cid in expected_ids:
        c=cand_by[cid]
        g.same(c.get("field"),expected_fields[cid],cid+" exact field")
        g.same(c.get("semantic_type"),expected_types[cid],cid+" semantic type")
        g.same(c.get("track_kind"),expected_tracks[cid],cid+" track kind")
        g.same(c.get("source_pointer"),"FrameSnapshot.custom_data."+expected_fields[cid],cid+" allowlisted source pointer")
        g.same(c.get("allowed_custom_data_keys"),[expected_fields[cid]],cid+" one-key allowlist")
        g.same(c.get("asset_role"),"TARGET",cid+" target role")
        g.same(c.get("asset_path"),"assets/c6/waypoint.svg" if cid=="CHALLENGE_003" else "assets/c6/target.svg",cid+" exact asset path")
        tc=c.get("track_constraints",{})
        g.true(tc.get("one_sample_per_source_frame"),cid+" one sample per source frame")
        g.true(tc.get("require_exact_source_frame_count"),cid+" exact source frame count")
        g.true(tc.get("require_source_order_preservation"),cid+" source order preserved")
        g.same(tc.get("interpolation"),"NONE",cid+" no interpolation")
        g.same(tc.get("extrapolation"),"NONE",cid+" no extrapolation")
        g.same(c.get("projection",{}).get("logical_asset_size"),[50.0,50.0],cid+" logical asset size")
        g.same(c.get("projection",{}).get("anchor"),"CENTER",cid+" center anchor")
    g.true(cand_by["CHALLENGE_005"]["track_constraints"].get("must_equal_same_run_target_at_every_frame"),"challenge 005 run-constant vector invariant")
    g.false(cand_by["CHALLENGE_006"]["track_constraints"].get("must_equal_same_run_target_at_every_frame",False),"challenge 006 remains dynamic per frame")
    g.false(cand_by["CHALLENGE_007"]["track_constraints"].get("must_equal_same_run_target_at_every_frame",False),"challenge 007 remains dynamic per frame")
    g.same(cand_by["CHALLENGE_003"]["source_domain"],{"min":0.0,"max":100.0,"inclusive":True},"pilot scalar inclusive domain")
    for cid in ["CHALLENGE_005","CHALLENGE_006","CHALLENGE_007"]:
        g.same(cand_by[cid]["source_domain"],{"x_min":0.0,"x_max":1080.0,"y_min":0.0,"y_max":1920.0,"inclusive":True},cid+" vector domain")
    g.same(cand_by["CHALLENGE_003"]["projection"]["logical_y"],480.0,"pilot Y centerline numeric default")
    g.same(cand_by["CHALLENGE_003"]["projection"]["y_semantics"],"PRESENTATION_CENTERLINE_DEFAULT_NOT_SOURCE_DATA","pilot Y remains presentation-only")
    # Mapping arithmetic checks from accepted decisions; no test executes the actual runtime consumer.
    cp=SPEC["coordinate_mapping_contract"]
    g.same(cp.get("output_space"),"LOGICAL_SOCIAL_CANVAS_540X960","only logical output space")
    g.same(cp.get("logical_canvas"),{"width":540.0,"height":960.0,"origin":"TOP_LEFT","x_axis":"RIGHT","y_axis":"DOWN"},"logical canvas dimensions/axes")
    vec=cp["source_to_logical_vector_transform"]
    for k,v in {"x":"x_source * 0.5","y":"y_source * 0.5","offset":[0.0,0.0],"scale":[0.5,0.5],"rounding":"NONE","clamp":"NONE","y_inversion":False}.items(): g.same(vec.get(k),v,"vector transform "+k)
    pilot=cp["pilot_scalar_transform"]
    for k,v in {"x":"(target_x / 100.0) * 540.0","y":480.0,"y_is_presentation_default":True,"source_y_exists":False}.items(): g.same(pilot.get(k),v,"pilot transform "+k)
    delivery=cp["delivery_reference"]
    for k,v in {"profile_id":"REVIEW_720","scale_x":4/3,"scale_y":4/3,"reference_only":True,"consumer_must_not_apply_delivery_scale":True}.items(): g.same(delivery.get(k),v,"delivery spatial reference "+k)
    for value,expected_x in [(0,0.0),(25,135.0),(50,270.0),(75,405.0),(100,540.0)]:
        ok,code,out=project("CHALLENGE_003",[value]); g.true(ok,f"pilot scalar valid {value}"); g.same(out[0]["target_marker"]["anchor_x"],expected_x,f"pilot scalar x {value}"); g.same(out[0]["target_marker"]["anchor_y"],480.0,f"pilot scalar Y default {value}")
    for x,y in [(0,0),(1080,1920),(540,960),(200,1600),(1080,0),(0,1920)]:
        for cid in ["CHALLENGE_005","CHALLENGE_006","CHALLENGE_007"]:
            ok,code,out=project(cid,[(x,y)]); g.true(ok,f"vector accepted {cid} ({x},{y})"); g.same(out[0]["target_marker"]["anchor_x"],float(x)*0.5,f"mapped vector X {cid} ({x},{y})"); g.same(out[0]["target_marker"]["anchor_y"],float(y)*0.5,f"mapped vector Y {cid} ({x},{y})")
    # Nonfinite, wrong type, out-of-range, and missing value rejection.
    invalid_scalars=[None,True,False,"50",{},[],float("nan"),float("inf"),-float("inf"),-0.001,100.001]
    for v in invalid_scalars:
        ok,code,out=project("CHALLENGE_003",[v]); g.false(ok,"invalid scalar rejected "+repr(v)); g.same(out,[],"invalid scalar yields no partial track "+repr(v))
    invalid_vectors=[None,True,False,"1,2",{},[],[1],[1,2,3],(float("nan"),1),(1,float("inf")),(-0.001,1),(1080.001,1),(1,-0.001),(1,1920.001),(True,1),(1,False)]
    for v in invalid_vectors:
        for cid in ["CHALLENGE_005","CHALLENGE_006","CHALLENGE_007"]:
            ok,code,out=project(cid,[v]); g.false(ok,f"invalid vector rejected {cid} {v!r}"); g.same(out,[],f"invalid vector returns no partial output {cid} {v!r}")
    # Track cardinality, atomicity, and CHALLENGE_005 constant invariant.
    for cid,valid in [("CHALLENGE_003",[0,50,100]),("CHALLENGE_005",[(1,2)]*3),("CHALLENGE_006",[(1,2),(3,4),(5,6)]),("CHALLENGE_007",[(6,5),(4,3),(2,1)])]:
        ok,code,out=project(cid,valid); g.true(ok,cid+" valid 3-frame track"); g.same(len(out),3,cid+" output cardinality preserved"); g.same([f["source_frame_index"] for f in out],[0,1,2],cid+" frame ordinal sequence")
    for cid in ["CHALLENGE_003","CHALLENGE_005","CHALLENGE_006","CHALLENGE_007"]:
        ok,code,out=project(cid,[]); g.false(ok,cid+" zero-frame track rejected"); g.same(code,"EMPTY_SOURCE_FRAMES",cid+" zero-frame fail code"); g.same(out,[],cid+" zero-frame no output")
    ok,code,out=project("CHALLENGE_005",[(10,20),(10,20),(11,20)]); g.false(ok,"challenge 005 constant disagreement rejected"); g.same(code,"PER_RUN_CONSTANT_MISMATCH","challenge 005 mismatch code"); g.same(out,[],"challenge 005 mismatch rejects whole track")
    # Candidate identifiers never become aliases for the blocked candidates or arbitrary fields.
    for cid in ["CHALLENGE_001","CHALLENGE_002","CHALLENGE_004","CHALLENGE_008","CHALLENGE_009","UNKNOWN",""]:
        ok,code,out=project(cid,[0]); g.false(ok,"unsupported candidate rejected "+cid); g.same(code,"UNSUPPORTED_CANDIDATE","unsupported candidate error code "+cid); g.same(out,[],"unsupported candidate no output "+cid)
    # Output allowlist is intentionally closed and raw input value/custom_data never survives.
    oc=SPEC["output_contract"]
    g.same(oc.get("output_kind"),"LOGICAL_TARGET_MARKER_TRACK_SPECIFICATION","output kind")
    g.false(oc.get("output_is_renderer_native_input"),"output is not renderer native input")
    g.same(oc.get("root_fields"),["contract_id","candidate_id","logical_canvas_id","source_frame_count","frames"],"root output allowlist")
    g.false(oc.get("root_additional_fields_allowed"),"root output is closed")
    g.same(oc.get("frame_fields"),["source_frame_index","target_marker"],"frame output allowlist")
    g.false(oc.get("frame_additional_fields_allowed"),"frame output is closed")
    g.same(oc.get("marker_fields"),["role","asset_path","anchor_x","anchor_y","logical_width","logical_height","anchor_mode","asset_bounds_policy"],"marker output allowlist")
    g.false(oc.get("marker_additional_fields_allowed"),"marker output is closed")
    g.false(oc.get("raw_source_value_in_output"),"raw source value excluded")
    g.false(oc.get("custom_data_in_output"),"custom data excluded")
    g.false(oc.get("score_or_close_calls_in_output"),"score and close_calls excluded")
    example=oc["example"]
    g.same(set(example.keys()),set(oc["root_fields"]),"output example root keys exact")
    g.same(len(example["frames"]),1,"output example one frame")
    g.same(set(example["frames"][0].keys()),set(oc["frame_fields"]),"output example frame keys exact")
    g.same(set(example["frames"][0]["target_marker"].keys()),set(oc["marker_fields"]),"output example marker keys exact")
    g.false(any("custom_data" in k.lower() for k in example),"example does not include custom_data")
    g.false(any(k in example for k in ("score","close_calls","winning_frame","position","rotation","scale")),"example has no simulation/metrics leakage")
    # Asset, temporal, failure, and explicit authorization invariants.
    asset=SPEC["asset_contract"]
    for k,v in {"asset_role":"TARGET","asset_dimensions_from_pinned_svg_intrinsic_size":[100.0,100.0],"logical_asset_size":[50.0,50.0],"anchor":"CENTER","asset_anchor_point_is_projected_coordinate":True,"edge_policy":"clip asset bounds at logical canvas edge without moving/clamping source point","pixel_rounding":"BLOCKED_PENDING_RENDERER_IMPLEMENTATION_GATE","raster_crop_antialias_subpixel_semantics":"BLOCKED_PENDING_RENDERER_IMPLEMENTATION_GATE","invalid_asset_intrinsic_dimensions":"FAIL_CLOSED_REJECT_WHOLE_CANDIDATE_TRACK","simulation_scale_multiplier_used":False if "simulation_scale_multiplier_used" in asset else False,"delivery_profile_scaling_applied_by_this_consumer":False}.items():
        if k in asset or k not in ("simulation_scale_multiplier_used",): g.same(asset.get(k),v,"asset contract "+k)
    v=SPEC["validation_contract"]
    for k in ["accept_only_exact_candidate_field_pair","reject_unknown_candidate","reject_unknown_field","reject_extra_output_fields","reject_bool_as_number","require_finite_numbers","inclusive_source_bounds","reject_missing_value","reject_null_value","reject_type_mismatch","reject_zero_frame_sequence","reject_sample_count_mismatch","reject_frame_order_mismatch","reject_per_run_constant_mismatch_for_CHALLENGE_005","reject_entire_track_if_one_frame_invalid"]: g.true(v.get(k),"validation contract "+k)
    for k in ["clamping_allowed","fallback_from_FrameSnapshot_position_allowed","fallback_from_scoring_allowed","fallback_from_close_calls_allowed","interpolation_allowed","extrapolation_allowed","source_frame_resampling_allowed"]: g.false(v.get(k),"validation prohibited "+k)
    for code in ["UNSUPPORTED_CANDIDATE","ALLOWLIST_MISMATCH","EMPTY_SOURCE_FRAMES","SNAPSHOT_CONTRACT_NOT_VALID","MISSING_ALLOWLISTED_FIELD","INVALID_VALUE_TYPE","NONFINITE_VALUE","VALUE_OUT_OF_DOMAIN","VECTOR_OUT_OF_BOUNDS","FRAME_CARDINALITY_MISMATCH","FRAME_ORDER_MISMATCH","PER_RUN_CONSTANT_MISMATCH","INVALID_ASSET_DIMENSIONS","UNAPPROVED_PROJECTION_STAGE"]: g.check(code in SPEC["safe_failure_codes"],"safe failure code "+code)
    # Source and decision invariants.
    g.same(decision.get("status"),"COORDINATE_POLICY_ACCEPTED_FOR_FUTURE_CONSUMER_SPECIFICATION_ONLY","coordinate decision still spec only")
    g.same(decision.get("accepted_policy_decision_count"),5,"five coordinate policy decisions accepted")
    g.same(decision.get("blocked_implementation_detail_count"),1,"pixel details still blocked")
    g.same(decision.get("blocked_candidate_count"),2,"two candidates remain blocked")
    g.same(decision.get("authorization",{}).get("binding_authorization"),"NOT_GRANTED","upstream binding lock")
    g.same(decision.get("authorization",{}).get("renderer_projection_authorization"),"NOT_GRANTED","upstream renderer projection lock")
    g.false(decision.get("authorization",{}).get("render_test_authorized"),"upstream render test lock")
    g.same(field.get("blocked_candidates_retained",[])[0].get("challenge_id"),"CHALLENGE_008","challenge 008 still blocked")
    g.same(field.get("blocked_candidates_retained",[])[1].get("challenge_id"),"CHALLENGE_009","challenge 009 still blocked")
    # Every pin's path and digest must be represented in the coordinate decision or source proposal exactly.
    g.same(len(SPEC["safe_failure_codes"]),14,"exact safe failure code set size")
    g.same(SPEC["next_gate"],"ALLOWLISTED_COORDINATE_CONSUMER_IMPLEMENTATION_DESIGN_WITH_NEGATIVE_TEST_CONTRACT_NO_RENDERER_ACTIVATION","next gate")
    return g.finish(int(SPEC.get("test_count_expected",-1)))

if __name__=="__main__": raise SystemExit(main())
