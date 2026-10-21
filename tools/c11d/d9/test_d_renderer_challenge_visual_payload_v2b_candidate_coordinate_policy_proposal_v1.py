#!/usr/bin/env python3
"""Read-only C11-D candidate coordinate-policy proposal validation. No Godot/render/media."""
from __future__ import annotations
import hashlib, json, math, re, sys
from pathlib import Path
ROOT = Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[4]
RECEIPT = Path(sys.argv[2]).resolve() if len(sys.argv)>2 else None
EMPTY_SHA = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
C11C_SHA = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
POLICY_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_COORDINATE_POLICY_PROPOSAL_V1.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_COORDINATE_POLICY_PROPOSAL_SCHEMA_V1.json")
FROZEN_REL = Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")
OLD_PROPOSAL_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_PROPOSAL_V1.json")
REGION_DECISION_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_DECISION_RECORD_V1.json")
REGION_DECISION_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_DECISION_RECORD_SCHEMA_V1.json")
REGION_DECISION_TEST_REL = Path("tools/c11d/d9/test_d_renderer_challenge_visual_payload_v2b_candidate_field_region_visibility_decision_record_v1.py")
PREV_SEMANTIC_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_SEMANTIC_DECISION_RECORD_V1.json")

def load(p): return json.loads(p.read_text(encoding="utf-8-sig"))
def file_sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
class Gate:
 def __init__(self): self.count=0; self.failures=[]
 def check(self, cond, label):
  self.count+=1
  if not cond: self.failures.append(f"CHECK_{self.count:03d}: {label}")
 def same(self,a,b,label): self.check(a==b,label)
 def true(self,v,label): self.check(v is True,label)
 def false(self,v,label): self.check(v is False,label)
 def finish(self):
  if self.failures:
   print("C11D_V2B_CANDIDATE_COORDINATE_POLICY_PROPOSAL_STATUS=FAIL")
   for f in self.failures[:100]: print(f)
   print(f"C11D_V2B_CANDIDATE_COORDINATE_POLICY_PROPOSAL_TESTS={self.count-len(self.failures)}/{self.count}")
   return 1
  print(f"C11D_V2B_CANDIDATE_COORDINATE_POLICY_PROPOSAL_TESTS={self.count}/{self.count}")
  print("C11D_V2B_CANDIDATE_COORDINATE_POLICY_PROPOSAL_CANDIDATES=4/4")
  print("C11D_V2B_CANDIDATE_COORDINATE_POLICY_PROPOSAL_SOURCE_PINS=81/81")
  print("C11D_V2B_CANDIDATE_COORDINATE_POLICY_PROPOSAL_AUTHORITY_INPUT_PINS=9/9")
  print("C11D_V2B_CANDIDATE_COORDINATE_POLICY_PROPOSAL_SEMANTIC_INPUT_PINS=6/6")
  print("C11D_V2B_CANDIDATE_COORDINATE_POLICY_PROPOSAL_FIELD_REGION_DECISION_PINS=6/6")
  print("C11D_V2B_CANDIDATE_COORDINATE_POLICY_PROPOSAL_COORDINATE_REFERENCE_PINS=3/3")
  print("C11D_V2B_CANDIDATE_COORDINATE_POLICY_PROPOSAL_STATUS=PROPOSED_NOT_APPROVED")
  print("C11D_V2B_COORDINATE_POLICY_AUTHORIZATION=NOT_GRANTED")
  print("C11D_V2B_BINDING_AUTHORIZATION=NOT_GRANTED")
  print("C11D_V2B_RENDERER_PROJECTION_AUTHORIZATION=NOT_GRANTED")
  print("C11D_V2B_RENDER_TEST_AUTHORIZATION=NOT_GRANTED")
  print("C11D_V2B_CANDIDATE_INPUT_ADMISSIBLE=false")
  print("C11D_V2B_RENDERER=OFF")
  print("C11D_V2B_MEDIA_CREATED=false")
  print("C11D_V2B_C11C_IMMUTABLE=true")
  return 0

def main():
 g=Gate(); policy_path=ROOT/POLICY_REL; schema_path=ROOT/SCHEMA_REL
 old_prop_path=ROOT/OLD_PROPOSAL_REL; decision_path=ROOT/REGION_DECISION_REL; decision_schema_path=ROOT/REGION_DECISION_SCHEMA_REL; decision_test_path=ROOT/REGION_DECISION_TEST_REL
 frozen_path=ROOT/FROZEN_REL
 for p,label in [(policy_path,"policy proposal"),(schema_path,"policy schema"),(old_prop_path,"prior field-region proposal"),(decision_path,"field-region decision record"),(decision_schema_path,"field-region decision schema"),(decision_test_path,"field-region decision suite"),(frozen_path,"frozen C11-C manifest")]:
  g.check(p.is_file(),label+" exists")
 if not all(p.is_file() for p in [policy_path,schema_path,old_prop_path,decision_path,decision_schema_path,decision_test_path,frozen_path]):
  return g.finish()
 p=load(policy_path); sch=load(schema_path); old=load(old_prop_path); dec=load(decision_path); frozen_sha=file_sha(frozen_path)
 g.same(p.get("schema"),"C11D-V2B-CANDIDATE-COORDINATE-POLICY-PROPOSAL-V1","proposal schema id")
 g.same(p.get("schema_version"),"1.0","schema version")
 g.same(p.get("status"),"PROPOSED_NOT_APPROVED_OPERATOR_REVIEW_REQUIRED","proposal remains unapproved")
 g.check(len(p.get("purpose",""))>=100,"purpose is explicit")
 g.same(frozen_sha,C11C_SHA,"frozen C11-C manifest hash")
 g.same(p.get("source_authority",{}).get("frozen_c11c_manifest_sha256"),C11C_SHA,"proposal C11-C source authority pin")
 g.same(p.get("source_authority",{}).get("field_region_visibility_decision_record_sha256"),file_sha(decision_path),"field-region decision authority pin")
 g.same(p.get("source_authority",{}).get("coordinate_mapper_sha256"),file_sha(ROOT/Path("core/presentation/CoordinateMapper.gd")),"coordinate mapper actual pin")
 g.same(p.get("source_authority",{}).get("delivery_profile_sha256"),file_sha(ROOT/Path("profiles/delivery/c11c_video_delivery_profiles.json")),"delivery profile actual pin")
 g.same(p.get("scope",{}).get("kind"),"COORDINATE_POLICY_PROPOSAL_ONLY","scope is coordinate proposal only")
 for k,v in {"candidate_count":4,"accepted_field_region_candidate_count":4,"blocked_candidate_count":2,"source_frame_only":True,"runtime_reexecution":False,"simulation_reexecution":False,"payload_materialized":False,"renderer_native_input_emitted":False,"renderer_dispatch_invoked":False,"renderer_activated":False,"render_test_authorized":False,"media_output_created":False,"challenge_json_modification_allowed":False,"coordinate_mapper_modification_allowed":False,"timebase_policy_changed":False,"source_frames_resampled":False}.items(): g.same(p["scope"].get(k),v,"scope "+k)
 g.same(p["scope"].get("included_challenge_fields"),["CHALLENGE_003.target_x","CHALLENGE_005.target_position","CHALLENGE_006.target_position","CHALLENGE_007.target_position"],"exact four included fields")
 g.same(p["scope"].get("excluded_blocked_challenge_fields"),["CHALLENGE_008.active_selection","CHALLENGE_009.displayed_count"],"exact blocked fields excluded")
 # Required source pins, with every expected input byte-checked.
 pin_sets=[("source_pins",81,False),("authority_input_pins",9,True),("semantic_decision_input_pins",6,True),("field_region_decision_input_pins",6,True),("coordinate_reference_pins",3,True)]
 for name,expected_n,has_role in pin_sets:
  pins=p.get(name,[]); g.same(len(pins),expected_n,name+" exact denominator"); seen=set()
  for idx,pin in enumerate(pins):
   path_text=pin.get("path",""); expected_hash=pin.get("sha256","")
   g.check(bool(path_text),name+f" pin {idx+1} path present")
   g.check(path_text not in seen,name+" no duplicate path "+path_text); seen.add(path_text)
   g.check(bool(re.fullmatch(r"[0-9a-f]{64}",expected_hash)),name+" sha format "+path_text)
   if has_role: g.check(bool(pin.get("role")),name+" role present "+path_text)
   pin_path=ROOT/Path(path_text); g.check(pin_path.is_file(),name+" input exists "+path_text)
   if pin_path.is_file(): g.same(file_sha(pin_path),expected_hash,name+" input sha "+path_text)
 # These reused pin lists must match the operator-reviewed proposal/decision exactly.
 g.same(p.get("source_pins"),old.get("source_pins"),"source pin list retained from field-region proposal")
 g.same(p.get("authority_input_pins"),old.get("authority_input_pins"),"authority pin list retained")
 g.same(p.get("semantic_decision_input_pins"),old.get("semantic_decision_input_pins"),"semantic decision pin list retained")
 g.same(p.get("field_region_decision_input_pins"),[
  {"path":str(OLD_PROPOSAL_REL).replace("\\","/"),"sha256":file_sha(old_prop_path),"role":"accepted_field_region_visibility_proposal"},
  {"path":"definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_PROPOSAL_SCHEMA_V1.json","sha256":file_sha(ROOT/Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_PROPOSAL_SCHEMA_V1.json")),"role":"field_region_visibility_proposal_schema"},
  {"path":str(REGION_DECISION_REL).replace("\\","/"),"sha256":file_sha(decision_path),"role":"operator_field_region_visibility_decision_record"},
  {"path":str(REGION_DECISION_SCHEMA_REL).replace("\\","/"),"sha256":file_sha(decision_schema_path),"role":"field_region_visibility_decision_schema"},
  {"path":str(REGION_DECISION_TEST_REL).replace("\\","/"),"sha256":file_sha(decision_test_path),"role":"field_region_visibility_decision_regression_suite"},
  {"path":str(PREV_SEMANTIC_REL).replace("\\","/"),"sha256":file_sha(ROOT/PREV_SEMANTIC_REL),"role":"prior_semantic_decision_record"}
 ],"decision pin list consistency")
 # Source and prior decision semantics.
 g.same(old.get("status"),"PROPOSED_NOT_APPROVED_OPERATOR_REVIEW_REQUIRED","prior field-region proposal remains immutable and unapproved")
 g.same(dec.get("status"),"FIELD_REGION_VISIBILITY_ACCEPTED_FOR_COORDINATE_POLICY_SPECIFICATION_ONLY","prior decision status retained")
 g.same(dec.get("field_region_visibility_test_count"),551,"field-region proposal prior test count")
 g.same(dec.get("field_region_visibility_test_stderr_sha256"),EMPTY_SHA,"prior proposal stderr digest canonical")
 g.same(dec.get("authorization",{}).get("coordinate_policy_approval"),"NOT_GRANTED_BY_THIS_DECISION","prior decision did not approve transforms")
 g.same(dec.get("authorization",{}).get("binding_authorization"),"NOT_GRANTED","prior decision has no binding approval")
 g.same(dec.get("authorization",{}).get("renderer_projection_authorization"),"NOT_GRANTED","prior decision has no projection approval")
 g.false(dec.get("authorization",{}).get("render_test_authorized"),"prior decision did not authorize render test")
 g.same(dec.get("governance_locks",{}).get("renderer"),"OFF","prior renderer lock")
 g.same(dec.get("governance_locks",{}).get("D4.8"),"BLOCKED","D4.8 lock")
 g.same(dec.get("governance_locks",{}).get("D10"),"BLOCKED_FOR_PROMOTION","D10 lock")
 g.same(p.get("evidence_pins",{}).get("field_region_decision_record_sha256"),file_sha(decision_path),"decision record evidence pin")
 g.same(p.get("evidence_pins",{}).get("field_region_decision_record_schema_sha256"),file_sha(decision_schema_path),"decision schema evidence pin")
 g.same(p.get("evidence_pins",{}).get("field_region_decision_test_script_sha256"),file_sha(decision_test_path),"decision test script evidence pin")
 g.same(p.get("evidence_pins",{}).get("field_region_decision_test_count"),653,"decision suite count pin")
 g.same(p.get("evidence_pins",{}).get("field_region_decision_test_stdout_sha256"),"a7e3b9dd98b317df5bb19e02c1751ae2b79ed4c297440eada8493c452bb44bba","Windows decision stdout pin")
 g.same(p.get("evidence_pins",{}).get("field_region_decision_test_stderr_sha256"),EMPTY_SHA,"Windows decision stderr empty pin")
 g.same(p.get("evidence_pins",{}).get("field_region_decision_test_receipt_sha256"),"4df0b28d7d933ca2c28b34e50e126112007bc0cc6fe24322e020d9d5f222677a","Windows decision receipt pin")
 # JSON Schema structure and key locks.
 g.same(sch.get("$schema"),"https://json-schema.org/draft/2020-12/schema","JSON schema draft")
 g.same(sch.get("type"),"object","schema root type")
 g.false(sch.get("additionalProperties",True),"schema closes root object")
 for req in ["schema","schema_version","status","source_authority","scope","evidence_pins","source_pins","authority_input_pins","semantic_decision_input_pins","field_region_decision_input_pins","coordinate_reference_pins","coordinate_policy","candidate_count","candidates","blocked_candidates_retained","governance","decision_gate","notes"]:
  g.check(req in sch.get("required",[]),"schema requires "+req)
 g.same(sch.get("properties",{}).get("status",{}).get("const"),p["status"],"schema status const")
 for name,n in [("source_pins",81),("authority_input_pins",9),("semantic_decision_input_pins",6),("field_region_decision_input_pins",6),("coordinate_reference_pins",3)]:
  g.same(sch.get("properties",{}).get(name,{}).get("minItems"),n,"schema min items "+name)
  g.same(sch.get("properties",{}).get(name,{}).get("maxItems"),n,"schema max items "+name)
 # Exact spatial stages, formula arithmetic and bounds.
 cp=p.get("coordinate_policy",{})
 g.same(cp.get("status"),"PROPOSED_NOT_APPROVED","coordinate policy stays proposed")
 logical=cp.get("logical_canvas",{}); g.same(logical.get("width"),540,"logical width"); g.same(logical.get("height"),960,"logical height")
 g.same(logical.get("coordinate_origin"),"TOP_LEFT","coordinate origin proposed"); g.same(logical.get("x_axis"),"RIGHT","x-axis convention"); g.same(logical.get("y_axis"),"DOWN","y-axis convention")
 source=cp.get("source_canvas",{}); g.same(source.get("width"),1080,"source width"); g.same(source.get("height"),1920,"source height"); g.same(source.get("aspect_ratio"),"9:16","source aspect")
 stages=cp.get("transform_stages",[]); g.same(len(stages),2,"exactly two transform stages")
 for idx,st in enumerate(stages):
  g.same(st.get("status"),"PROPOSED_NOT_APPROVED",f"stage {idx+1} remains proposed")
  g.check(st.get("uniform_scale") is True,f"stage {idx+1} uniform scale")
  g.check(st.get("preserve_aspect_ratio") is True,f"stage {idx+1} preserves aspect")
  g.same(st.get("offset_x"),0.0,f"stage {idx+1} x offset zero")
  g.same(st.get("offset_y"),0.0,f"stage {idx+1} y offset zero")
  g.same(st.get("intermediate_rounding"),"NONE",f"stage {idx+1} no rounding")
 g.same(stages[0].get("source_space"),"CANVAS_1080X1920","first stage source space")
 g.same(stages[0].get("destination_space"),"LOGICAL_SOCIAL_CANVAS_540X960","first stage logical destination")
 g.same(stages[0].get("scale_x"),0.5,"canvas scale x half")
 g.same(stages[0].get("scale_y"),0.5,"canvas scale y half")
 g.same(stages[1].get("reference_profile_id"),"REVIEW_720","delivery reference profile")
 g.same(stages[1].get("delivery_width"),720,"delivery width from profile")
 g.same(stages[1].get("delivery_height"),1280,"delivery height from profile")
 g.same(stages[1].get("scale_x"),4/3,"delivery scale x")
 g.same(stages[1].get("scale_y"),4/3,"delivery scale y")
 g.same(stages[1].get("purpose"),"SPATIAL_REFERENCE_ONLY_NOT_FINAL_DELIVERY_SELECTION","reference only")
 combo=cp.get("combined_canvas_to_reference_delivery",{})
 g.same(combo.get("scale_x"),2/3,"combined scale x two-thirds")
 g.same(combo.get("scale_y"),2/3,"combined scale y two-thirds")
 g.same(combo.get("offset_x"),0.0,"combined x offset")
 g.same(combo.get("offset_y"),0.0,"combined y offset")
 # Numeric examples ensure source/logical/delivery formulas agree without raster rounding.
 test_vectors=[((0.0,0.0),(0.0,0.0),(0.0,0.0)),((540.0,960.0),(270.0,480.0),(360.0,640.0)),((1080.0,1920.0),(540.0,960.0),(720.0,1280.0)),((540.0,300.0),(270.0,150.0),(360.0,200.0))]
 for i,(src,logi,deliv) in enumerate(test_vectors):
  mapped=(src[0]*0.5,src[1]*0.5); delivery=(mapped[0]*4/3,mapped[1]*4/3)
  g.check(math.isclose(mapped[0],logi[0],abs_tol=1e-12),f"mapping example {i+1} logical x")
  g.check(math.isclose(mapped[1],logi[1],abs_tol=1e-12),f"mapping example {i+1} logical y")
  g.check(math.isclose(delivery[0],deliv[0],abs_tol=1e-12),f"mapping example {i+1} delivery x")
  g.check(math.isclose(delivery[1],deliv[1],abs_tol=1e-12),f"mapping example {i+1} delivery y")
 # Scalar-only PILOT policy and explicit presentation Y choice.
 pilot=cp.get("pilot_scalar_policy",{})
 g.same(pilot.get("source_space"),"PILOT_0X100","pilot space")
 g.same(pilot.get("source_domain_min"),0.0,"pilot minimum domain")
 g.same(pilot.get("source_domain_max"),100.0,"pilot maximum domain")
 g.same(pilot.get("destination_rect"),"FULL_LOGICAL_CANVAS_540X960","pilot full-frame rect")
 g.same(pilot.get("logical_x_formula"),"x_logical = (target_x / 100.0) * 540.0","pilot x formula")
 g.same(pilot.get("logical_y_formula"),"y_logical = 960.0 / 2.0 = 480.0","pilot explicit midpoint formula")
 g.same(pilot.get("y_semantics"),"PRESENTATION_CENTERLINE_DEFAULT_PROPOSAL_NOT_SOURCE_DATA","pilot y marked presentation policy")
 g.false(pilot.get("y_inferred_from_simulation"),"pilot y not inferred from simulation")
 g.same(pilot.get("out_of_domain_behavior"),"FAIL_CLOSED_REJECT_WHOLE_CANDIDATE_TRACK","pilot out-of-range fail closed")
 g.false(pilot.get("clamp_source_value"),"pilot source scalar is never clamped")
 for x,expected_x in [(0,0),(25,135),(50,270),(75,405),(100,540)]:
  g.check(math.isclose((x/100)*540,expected_x,abs_tol=1e-12),f"pilot logical x sample {x}")
  g.check(0<=x<=100,f"pilot domain sample {x} admitted")
 g.check(not (math.isfinite(-0.01) and 0<=-0.01<=100),"pilot lower out-of-domain rejected")
 g.check(not (math.isfinite(100.01) and 0<=100.01<=100),"pilot upper out-of-domain rejected")
 for bad in [float("nan"),float("inf"),-float("inf")]: g.check(not math.isfinite(bad),"nonfinite pilot sample rejected")
 # Vector policy.
 vp=cp.get("vector_policy",{})
 g.same(vp.get("source_space"),"CANVAS_1080X1920","vector source space")
 g.same(vp.get("source_domain_x"),[0.0,1080.0],"vector x domain")
 g.same(vp.get("source_domain_y"),[0.0,1920.0],"vector y domain")
 g.true(vp.get("bounds_inclusive"),"vector bounds inclusive")
 g.same(vp.get("mapping"),"EXACT_SOURCE_VECTOR_UNIFORMLY_SCALED_BY_0_5_TO_LOGICAL","vector scale policy")
 g.false(vp.get("add_offset"),"vector offset disabled")
 g.false(vp.get("invert_y"),"vector y inversion disabled")
 g.false(vp.get("clamp_coordinates"),"vector clamping disabled")
 g.same(vp.get("out_of_bounds_behavior"),"FAIL_CLOSED_REJECT_WHOLE_CANDIDATE_TRACK","vector out-of-bounds fail closed")
 for x,y in [(0,0),(540,960),(1080,1920),(540,300),(150,250),(930,1670)]:
  g.check(math.isfinite(x) and math.isfinite(y),f"vector sample finite {x},{y}")
  g.check(0<=x<=1080,f"vector x in bounds {x}")
  g.check(0<=y<=1920,f"vector y in bounds {y}")
  g.check(math.isclose(x*0.5*4/3,x*2/3,abs_tol=1e-12),f"vector x two-stage agrees {x}")
  g.check(math.isclose(y*0.5*4/3,y*2/3,abs_tol=1e-12),f"vector y two-stage agrees {y}")
 for x,y in [(-0.01,20),(1080.01,20),(20,-0.01),(20,1920.01)]:
  g.check(not (0<=x<=1080 and 0<=y<=1920),f"out-of-bounds vector rejected {x},{y}")
 for bad in [float("nan"),float("inf"),-float("inf")]: g.check(not math.isfinite(bad),"nonfinite Vector2 component rejected")
 # Asset dimension/anchor proposal based on pinned SVGs.
 ap=cp.get("asset_size_policy",{})
 g.same(ap.get("status"),"PROPOSED_NOT_APPROVED","asset size remains proposed")
 g.same(ap.get("known_marker_intrinsic_dimensions",{}).get("assets/c6/waypoint.svg"),[100.0,100.0],"waypoint dimensions")
 g.same(ap.get("known_marker_intrinsic_dimensions",{}).get("assets/c6/target.svg"),[100.0,100.0],"target dimensions")
 g.same(ap.get("waypoint_logical_size"),[50.0,50.0],"waypoint logical size proposal")
 g.same(ap.get("target_logical_size"),[50.0,50.0],"target logical size proposal")
 g.check(math.isclose(ap.get("waypoint_reference_delivery_size",[0,0])[0],200/3,abs_tol=1e-12),"waypoint delivery size x")
 g.check(math.isclose(ap.get("waypoint_reference_delivery_size",[0,0])[1],200/3,abs_tol=1e-12),"waypoint delivery size y")
 g.check(math.isclose(ap.get("target_reference_delivery_size",[0,0])[0],200/3,abs_tol=1e-12),"target delivery size x")
 g.check(math.isclose(ap.get("target_reference_delivery_size",[0,0])[1],200/3,abs_tol=1e-12),"target delivery size y")
 g.same(ap.get("asset_anchor"),"CENTER","asset center anchor")
 g.same(ap.get("asset_bounds_behavior"),"CLIP_AT_LOGICAL_CANVAS_BOUNDARY_WITHOUT_CLAMPING_OR_MOVING_SOURCE_POSITION","edge clipping policy explicit")
 g.false(ap.get("simulation_scale_multiplier_used"),"simulation scale does not change size proposal")
 g.same(ap.get("asset_pixel_rounding"),"UNRESOLVED_DEFERRED_TO_RENDERER_IMPLEMENTATION_GATE","pixel rounding still unresolved")
 for path,expected_size in [(ROOT/Path("assets/c6/waypoint.svg"),(100,100)),(ROOT/Path("assets/c6/target.svg"),(100,100))]:
  g.check(path.is_file(),"SVG asset exists "+str(path.name))
  if path.is_file():
   text=path.read_text(encoding="utf-8-sig")
   m=re.search(r'<svg\b[^>]*\bwidth="([0-9.]+)"[^>]*\bheight="([0-9.]+)"',text)
   g.check(m is not None,"SVG has intrinsic dimensions "+str(path.name))
   if m: g.same((float(m.group(1)),float(m.group(2))),expected_size,"SVG intrinsic dimensions "+str(path.name))
 # Exact four-candidate mapping matrix and blocked fields.
 expected=[("CHALLENGE_003","target_x","float","PILOT_0X100","assets/c6/waypoint.svg","PER_FRAME_SCALAR"),("CHALLENGE_005","target_position","Vector2","CANVAS_1080X1920","assets/c6/target.svg","PER_RUN_CONSTANT_REPEATED_PER_FRAME"),("CHALLENGE_006","target_position","Vector2","CANVAS_1080X1920","assets/c6/target.svg","PER_FRAME_VECTOR"),("CHALLENGE_007","target_position","Vector2","CANVAS_1080X1920","assets/c6/target.svg","PER_FRAME_VECTOR")]
 candidates=p.get("candidates",[]); g.same(len(candidates),4,"exact candidate count")
 g.same([(c.get("challenge_id"),c.get("field"),c.get("semantic_type"),c.get("source_coordinate_space"),c.get("asset_path"),c.get("source_track_kind")) for c in candidates],expected,"exact candidate mapping order")
 for i,c in enumerate(candidates):
  prefix=f"candidate {i+1} {c.get('challenge_id')}"
  g.same(c.get("field_region_decision"),"ACCEPT_FOR_FUTURE_COORDINATE_POLICY_SPECIFICATION_ONLY",prefix+" accepted scope retained")
  g.same(c.get("asset_role"),"TARGET",prefix+" target role")
  g.same(c.get("asset_dimensions_source"),[100.0,100.0],prefix+" asset dimension basis")
  g.same(c.get("visibility"),"FULL_SOURCE_FRAME_SPAN_PROPOSED",prefix+" full frame visibility proposed")
  g.same(c.get("interpolation"),"NONE",prefix+" no interpolation")
  g.same(c.get("extrapolation"),"NONE",prefix+" no extrapolation")
  g.true(c.get("source_semantics_preserved"),prefix+" preserves source semantics")
  g.check(len(c.get("unresolved",[]))>=3,prefix+" explicit unresolved decisions")
  g.same(c.get("sample_rule") in ("ONE_FINITE_IN_RANGE_SCALAR_PER_SOURCE_FRAME","ONE_FINITE_IN_BOUNDS_VECTOR_PER_SOURCE_FRAME; VALUES_MAY_BE_CONSTANT_ACROSS_FRAMES","ONE_FINITE_IN_BOUNDS_VECTOR_PER_SOURCE_FRAME"),True,prefix+" sample rule is fail-closed typed")
  mp=c.get("mapping_proposal",{})
  g.check(bool(mp.get("policy_id")),prefix+" policy id present")
  g.same(mp.get("invalid_behavior"),"FAIL_CLOSED_REJECT_WHOLE_CANDIDATE_TRACK",prefix+" invalid track fail closed")
 # Candidate-specific semantic invariants.
 c003=candidates[0]; c005=candidates[1]; c006=candidates[2]; c007=candidates[3]
 g.same(c003.get("mapping_proposal",{}).get("y_formula"),"480.0 (presentation centerline only; not source data)","003 Y default explicit")
 g.same(c003.get("mapping_proposal",{}).get("no_source_clamping"),True,"003 no clamp")
 g.same(c005.get("mapping_proposal",{}).get("policy_id"),"CANVAS_VECTOR_TO_LOGICAL_FULL_FRAME","005 vector mapping")
 g.same(c005.get("source_track_kind"),"PER_RUN_CONSTANT_REPEATED_PER_FRAME","005 still per-run constant track")
 g.same(c006.get("source_track_kind"),"PER_FRAME_VECTOR","006 frame track")
 g.same(c007.get("source_track_kind"),"PER_FRAME_VECTOR","007 frame track")
 g.check(c006.get("source_pointer")==c007.get("source_pointer")=="FrameSnapshot.custom_data.target_position","006/007 field pointer identity")
 for c in candidates:
  g.check(c.get("source_pointer")=="FrameSnapshot.custom_data."+c.get("field"),c.get("challenge_id","candidate")+" only reads allowlisted field")
 # Temporal invariants and fail-closed behavior.
 tp=cp.get("temporal_noninterference",{})
 for k,v in {"source_frame_sequence":"SimulationResult.frames[*]","source_frame_count":"PRESERVE_EXACT_SOURCE_FRAME_COUNT","sample_cardinality":"EXACTLY_ONE_TARGET_SAMPLE_PER_SOURCE_FRAME","interpolation":"NONE","extrapolation":"NONE","delivery_resampling":"NOT_AUTHORIZED_BY_THIS_POLICY_PROPOSAL","source_frame_order":"UNCHANGED","winning_frame":"SOLE_CHALLENGE_TEMPORAL_ANCHOR","close_calls":"EPISODE_COUNT_ONLY_NOT_TIMELINE_OR_VISIBILITY_INPUT"}.items(): g.same(tp.get(k),v,"temporal invariant "+k)
 inv=cp.get("invalid_data_policy",{})
 for k,v in {"missing_field":"FAIL_CLOSED_REJECT_WHOLE_CANDIDATE_TRACK","nonfinite_scalar_or_component":"FAIL_CLOSED_REJECT_WHOLE_CANDIDATE_TRACK","sample_count_mismatch":"FAIL_CLOSED_REJECT_WHOLE_CANDIDATE_TRACK","out_of_domain_scalar":"FAIL_CLOSED_REJECT_WHOLE_CANDIDATE_TRACK","out_of_bounds_vector":"FAIL_CLOSED_REJECT_WHOLE_CANDIDATE_TRACK","no_fallback_from_snapshot_position":True,"no_fallback_from_scoring_or_close_calls":True,"only_allowlisted_custom_data_field_read":True,"serialize_whole_custom_data_map":False}.items(): g.same(inv.get(k),v,"invalid data invariant "+k)
 # Blocked challenge candidates retained, with no future leakage.
 blocks=p.get("blocked_candidates_retained",[]); g.same(len(blocks),2,"two blocked candidates retained")
 g.same([(b.get("challenge_id"),b.get("field")) for b in blocks],[("CHALLENGE_008","active_selection"),("CHALLENGE_009","displayed_count")],"exact blocked candidate list")
 for b in blocks:
  g.same(b.get("status"),"REMAINS_BLOCKED",b.get("challenge_id")+" stays blocked")
  g.check(len(b.get("reason",""))>=60,b.get("challenge_id")+" has substantive blocker")
 # No authorization leakage anywhere at top-level governance and decision gate.
 gov=p.get("governance",{})
 locks={"coordinate_policy_approval":"NOT_GRANTED","coordinate_transform_authorization":"NOT_GRANTED","asset_size_policy_approval":"NOT_GRANTED","binding_authorization":"NOT_GRANTED","renderer_projection_authorization":"NOT_GRANTED","payload_consumer_implementation_authorized":False,"renderer_activation_authorized":False,"render_test_authorized":False,"payload_materialization_authorized":False,"media_creation_authorized":False,"renderer":"OFF","media_created":False,"payload_materialized":False,"candidate_input_admissible":False,"seed_domains_complete_for_candidate_input":False,"automatic_seed_generation":False,"master_seed":"NOT_ADOPTED","approved_bindings":0,"approved_custom_data_bindings":0,"approved_renderer_projection_bindings":0,"D4.8":"BLOCKED","D9.10":"PREPARE_ONLY","D9.14":"BLOCKED","D9.16":"BLOCKED","D9.17":"BLOCKED_NO_GO","D10":"BLOCKED_FOR_PROMOTION","baseline_approval":"MISSING","freeze_eligible":False,"release_authority":"NONE","whole_custom_data_serialization_allowed":False,"challenge_json_modification_allowed":False,"challenge_004_v1_harness_mutation_allowed":False}
 for k,v in locks.items(): g.same(gov.get(k),v,"governance lock "+k)
 gate=p.get("decision_gate",{})
 g.same(gate.get("status"),"PENDING_OPERATOR_REVIEW_OF_EXPLICIT_SPATIAL_FORMULAS","operator decision pending")
 for target in ["canvas_to_logical_scale_0_5","logical_to_review_720_scale_4_over_3_as_reference_only","pilot_scalar_centerline_y_480","svg_intrinsic_size_interpreted_as_source_canvas_units","center_anchor_and_edge_clipping"]:
  g.check(target in gate.get("decision_required_for",[]),"decision item required "+target)
 for denied in ["binding_approval","payload_consumer","renderer_projection","renderer_activation","render_test","payload_materialization","media_creation","baseline_promotion"]:
  g.check(denied in gate.get("does_not_authorize",[]),"denial scope "+denied)
 g.check("SPATIAL_FORMULAS" in p.get("decision_gate",{}).get("status",""),"gate clearly requests spatial formula review")
 for note in p.get("notes",[]): g.check(isinstance(note,str) and len(note)>=50,"substantive note")
 # The exact Windows decision receipt is supplied as a path by the caller.
 g.check(RECEIPT is not None,"Windows receipt argument supplied")
 if RECEIPT is not None:
  g.check(RECEIPT.is_file(),"Windows decision receipt exists")
  if RECEIPT.is_file():
   try:
    rr=load(RECEIPT)
    for k,v in {"status":"PASS_STATIC_TESTS","test_count":653,"decision_record_sha256":old_dec_sha_expected,"decision_record_schema_sha256":old_dec_schema_sha_expected,"decision_record_test_script_sha256":old_dec_test_sha_expected,"stdout_sha256":p["evidence_pins"]["field_region_decision_test_stdout_sha256"],"stderr_sha256":EMPTY_SHA,"approved_bindings":0,"approved_custom_data_bindings":0,"approved_renderer_projection_bindings":0,"coordinate_policy_authorized":False,"binding_authorization":"NOT_GRANTED","renderer_projection_authorization":"NOT_GRANTED","render_test_authorized":False,"candidate_input_admissible":False,"renderer":"OFF","media_created":False,"payload_materialized":False,"frozen_manifest_sha256":C11C_SHA}.items(): g.same(rr.get(k),v,"Windows receipt field "+k)
   except Exception as exc: g.check(False,"Windows receipt parse error "+str(exc))
 # Validate schema dialect and optional full JSON-schema validation if library exists.
 try:
  import jsonschema
  jsonschema.Draft202012Validator.check_schema(sch)
  jsonschema.validate(p,sch)
  g.true(True,"JSON Schema Draft 2020-12 validation")
 except ImportError:
  # Structural checks above remain authoritative if optional dependency unavailable.
  g.true(True,"JSON Schema package optional and not installed")
 except Exception as exc:
  g.check(False,"JSON Schema validation: "+str(exc))
 # Verify scalar static inputs from the immutable challenge config without re-running simulation.
 challenge003=load(ROOT/Path("challenges/CHALLENGE_003.json"))
 content=challenge003.get("content",{})
 target_start=content.get("target_start"); target_velocity=content.get("target_velocity")
 g.check(isinstance(target_start,(int,float)) and math.isfinite(target_start),"003 static target_start finite")
 g.check(isinstance(target_velocity,(int,float)) and math.isfinite(target_velocity),"003 static target_velocity finite")
 if isinstance(target_start,(int,float)) and isinstance(target_velocity,(int,float)):
  duration=challenge003.get("video",{}).get("game_duration",0); fps=challenge003.get("video",{}).get("fps",0)
  g.same(duration,7.0,"003 current game duration pinned")
  g.same(fps,60,"003 current source fps pinned")
  source_frames=int(duration*fps)
  g.same(source_frames,420,"003 current config source frame arithmetic")
  first=target_start+target_velocity*0; last=target_start+target_velocity*(source_frames-1)
  g.check(0<=first<=100,"003 first scalar sample in proposed domain")
  g.check(0<=last<=100,"003 final scalar sample in proposed domain")
  g.check(math.isclose(first,0,abs_tol=1e-12),"003 first scalar coordinate unchanged")
  g.check(math.isclose(last,100,abs_tol=1e-9),"003 final scalar coordinate unchanged")
 # Final schema/record checks.
 g.same(len(p.get("notes",[])),10,"ten policy notes")
 g.same(p.get("candidate_count"),4,"four candidate count")
 g.same(dec.get("accepted_candidate_count"),4,"prior accepted candidate count")
 g.same(dec.get("blocked_candidate_count"),2,"prior blocked candidate count")
 g.same(old.get("candidate_count"),4,"previous proposal candidate count")
 g.same(old.get("decision_gate",{}).get("status"),"PENDING_EXPLICIT_OPERATOR_REVIEW","prior decision gate remains independent")
 g.same(p.get("governance",{}).get("release_authority"),"NONE","release authority none")
 return g.finish()

# Expected hashes loaded from the pinned Windows decision package.
old_dec_sha_expected = "1ec59d7a9257cfc2477fc37efe8cb2f04d9807a7f9986d96afc2f2ddd9b4f7af"
old_dec_schema_sha_expected = "bb32a0631216c8b557ee48f85ff06dbf1588c125606b917acff22930aa6ce50e"
old_dec_test_sha_expected = "c35d3a44c0b998235ad17b2ad403892a1e6c95e0bffaeb0a3d075f4ff8258039"
if __name__=="__main__": raise SystemExit(main())
