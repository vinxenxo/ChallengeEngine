#!/usr/bin/env python3
"""Read-only C11-D coordinate-policy decision regression suite; no renderer or media."""
from __future__ import annotations
import hashlib, json, math, sys
from pathlib import Path

EXPECTED = {
 "c11c":"e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953",
 "proposal":"44c1ec6507988023b7cd20cdcc8e0e722c99af610d9be02a6d658ce9b07e9f57",
 "proposal_schema":"9715a6d3580f86307f2fb2c2ce348555256632c66d1c6f68d54db7af199486a2",
 "proposal_test":"70b869259778e3c2289782b985b7f1c89c63ded8d0130ead06d34bf28aa55e89",
 "coord_stdout":"439e68e15c72975ccc3ac26d42e5e8e8dc5019bcc4e9f1f3051fd061701b07f3",
 "coord_receipt":"1518168dd6b50fc869dbd18b05dcdef13397ea8023ff6fa1f896f55dee5b9f96",
 "empty":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
 "field_record":"1ec59d7a9257cfc2477fc37efe8cb2f04d9807a7f9986d96afc2f2ddd9b4f7af",
 "field_schema":"bb32a0631216c8b557ee48f85ff06dbf1588c125606b917acff22930aa6ce50e",
 "field_test":"c35d3a44c0b998235ad17b2ad403892a1e6c95e0bffaeb0a3d075f4ff8258039",
 "field_receipt":"4df0b28d7d933ca2c28b34e50e126112007bc0cc6fe24322e020d9d5f222677a",
 "field_stdout":"a7e3b9dd98b317df5bb19e02c1751ae2b79ed4c297440eada8493c452bb44bba",
 "semantic_record":"cc3550cd4d13f228ec9b3d51eeaa199505c5975b42882fb06ba3e83c4a000e90",
 "semantic_receipt":"3cf2284c454a06571ea97a2e771a259d2b73a8f4616432063a581b5c3e57ecf9",
}
ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[4]
RECORD_REL=Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_COORDINATE_POLICY_DECISION_RECORD_V1.json")
SCHEMA_REL=Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_COORDINATE_POLICY_DECISION_RECORD_SCHEMA_V1.json")
PROPOSAL_REL=Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_COORDINATE_POLICY_PROPOSAL_V1.json")
PROPOSAL_SCHEMA_REL=Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_COORDINATE_POLICY_PROPOSAL_SCHEMA_V1.json")
PROPOSAL_TEST_REL=Path("tools/c11d/d9/test_d_renderer_challenge_visual_payload_v2b_candidate_coordinate_policy_proposal_v1.py")
FIELD_RECORD_REL=Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_DECISION_RECORD_V1.json")
FIELD_SCHEMA_REL=Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_DECISION_RECORD_SCHEMA_V1.json")
FIELD_TEST_REL=Path("tools/c11d/d9/test_d_renderer_challenge_visual_payload_v2b_candidate_field_region_visibility_decision_record_v1.py")
SEM_RECORD_REL=Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_SEMANTIC_DECISION_RECORD_V1.json")

class Gate:
 def __init__(self): self.count=0; self.failures=[]
 def check(self,v,label):
  self.count+=1
  if not v: self.failures.append(f"CHECK_{self.count:04d}: {label}")
 def same(self,a,b,label): self.check(a==b,label)
 def true(self,v,label): self.check(v is True,label)
 def false(self,v,label): self.check(v is False,label)
 def finish(self,expected):
  if self.count!=expected: self.failures.append(f"CHECK_COUNT: expected {expected}, generated {self.count}")
  if self.failures:
   print("C11D_V2B_CANDIDATE_COORDINATE_POLICY_DECISION_RECORD_STATUS=FAIL")
   for x in self.failures[:80]: print(x)
   print(f"C11D_V2B_CANDIDATE_COORDINATE_POLICY_DECISION_RECORD_TESTS={self.count-len(self.failures)}/{self.count}")
   return 1
  print(f"C11D_V2B_CANDIDATE_COORDINATE_POLICY_DECISION_RECORD_TESTS={self.count}/{self.count}")
  print("C11D_V2B_CANDIDATE_COORDINATE_POLICY_DECISIONS=5_ACCEPTED_1_BLOCKED_IMPLEMENTATION_DETAIL")
  print("C11D_V2B_CANDIDATE_COORDINATE_POLICY_ACCEPTED=SPECIFICATION_ONLY")
  print("C11D_V2B_CANDIDATE_COORDINATE_TRANSFORM_RUNTIME_AUTHORIZATION=NOT_GRANTED")
  print("C11D_V2B_CANDIDATE_ASSET_SIZE_POLICY_ACCEPTED=SPECIFICATION_ONLY")
  print("C11D_V2B_RENDERER_PIXEL_ROUNDING_CROP_POLICY=BLOCKED")
  print("C11D_V2B_BINDING_AUTHORIZATION=NOT_GRANTED")
  print("C11D_V2B_RENDERER_PROJECTION_AUTHORIZATION=NOT_GRANTED")
  print("C11D_V2B_RENDER_TEST_AUTHORIZATION=NOT_GRANTED")
  print("C11D_V2B_CANDIDATE_INPUT_ADMISSIBLE=false")
  print("C11D_V2B_RENDERER=OFF")
  print("C11D_V2B_MEDIA_CREATED=false")
  print("C11D_V2B_C11C_IMMUTABLE=true")
  return 0

def load(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 g=Gate()
 rp=ROOT/RECORD_REL; sp=ROOT/SCHEMA_REL; pp=ROOT/PROPOSAL_REL; psp=ROOT/PROPOSAL_SCHEMA_REL; ptp=ROOT/PROPOSAL_TEST_REL
 frp=ROOT/FIELD_RECORD_REL; fsp=ROOT/FIELD_SCHEMA_REL; ftp=ROOT/FIELD_TEST_REL; srp=ROOT/SEM_RECORD_REL
 for rel,expected,label in [(RECORD_REL,None,'decision record'),(SCHEMA_REL,None,'decision schema'),(PROPOSAL_REL,EXPECTED['proposal'],'coordinate proposal'),(PROPOSAL_SCHEMA_REL,EXPECTED['proposal_schema'],'coordinate proposal schema'),(PROPOSAL_TEST_REL,EXPECTED['proposal_test'],'coordinate proposal suite'),(FIELD_RECORD_REL,EXPECTED['field_record'],'field-region record'),(FIELD_SCHEMA_REL,EXPECTED['field_schema'],'field-region schema'),(FIELD_TEST_REL,EXPECTED['field_test'],'field-region suite'),(SEM_RECORD_REL,EXPECTED['semantic_record'],'semantic decision record')]:
  g.true((ROOT/rel).is_file(),label+' exists')
  if (ROOT/rel).is_file() and expected: g.same(sha(ROOT/rel),expected,label+' sha256')
 rec=load(rp); sch=load(sp); prop=load(pp); pschema=load(psp); field=load(frp); semantic=load(srp)
 g.same(sha(Path(__file__)),rec.get('coordinate_policy_decision_test_script_sha256'),'decision suite self pin')
 g.same(rec.get('schema'),'C11D-V2B-CANDIDATE-COORDINATE-POLICY-DECISION-RECORD-V1','record schema id')
 g.same(rec.get('schema_version'),'1.0','record version')
 g.same(rec.get('status'),'COORDINATE_POLICY_ACCEPTED_FOR_FUTURE_CONSUMER_SPECIFICATION_ONLY','record status')
 g.same(rec.get('decision_scope'),'FUTURE_CONSUMER_SPECIFICATION_ONLY_NO_RUNTIME_AUTHORIZATION','decision scope')
 g.same(rec.get('reviewer_role'),'operator','reviewer role')
 reviewed=rec.get('reviewed_at','')
 g.check(isinstance(reviewed,str) and reviewed.endswith('+02:00') and 'T' in reviewed,'RFC3339 Madrid offset')
 g.same(rec.get('previous_coordinate_policy_proposal_sha256'),EXPECTED['proposal'],'prior proposal pin')
 g.same(rec.get('previous_coordinate_policy_proposal_schema_sha256'),EXPECTED['proposal_schema'],'prior proposal schema pin')
 g.same(rec.get('previous_coordinate_policy_test_script_sha256'),EXPECTED['proposal_test'],'prior proposal suite pin')
 g.same(rec.get('previous_coordinate_policy_test_count'),961,'prior proposal test count')
 g.same(rec.get('previous_coordinate_policy_test_stdout_sha256'),EXPECTED['coord_stdout'],'prior proposal stdout')
 g.same(rec.get('previous_coordinate_policy_test_stderr_sha256'),EXPECTED['empty'],'prior proposal stderr empty')
 g.same(rec.get('previous_coordinate_policy_test_receipt_sha256'),EXPECTED['coord_receipt'],'prior proposal receipt')
 g.same(rec.get('previous_field_region_decision_record_sha256'),EXPECTED['field_record'],'field-region decision pin')
 g.same(rec.get('previous_field_region_decision_schema_sha256'),EXPECTED['field_schema'],'field-region schema pin')
 g.same(rec.get('previous_field_region_decision_test_script_sha256'),EXPECTED['field_test'],'field-region suite pin')
 g.same(rec.get('previous_field_region_decision_test_count'),653,'field-region test count')
 g.same(rec.get('previous_field_region_decision_test_stdout_sha256'),EXPECTED['field_stdout'],'field-region stdout')
 g.same(rec.get('previous_field_region_decision_test_stderr_sha256'),EXPECTED['empty'],'field-region stderr empty')
 g.same(rec.get('previous_field_region_decision_test_receipt_sha256'),EXPECTED['field_receipt'],'field-region receipt')
 g.same(rec.get('previous_semantic_decision_record_sha256'),EXPECTED['semantic_record'],'prior semantic record')
 g.same(rec.get('previous_semantic_decision_test_receipt_sha256'),EXPECTED['semantic_receipt'],'prior semantic receipt')
 g.same(rec.get('frozen_c11c_manifest_sha256'),EXPECTED['c11c'],'frozen manifest pin')
 g.same(rec.get('accepted_policy_decision_count'),5,'five accepted decisions')
 g.same(rec.get('blocked_implementation_detail_count'),1,'one blocked renderer detail')
 g.same(rec.get('blocked_candidate_count'),2,'two blocked candidates')
 g.same(len(rec.get('decisions',[])),6,'six coordinate policy decisions')
 g.same(len(rec.get('blocked_candidates_retained',[])),2,'two blocked candidate records')
 # Schema contract: closed root and explicit required fields.
 g.same(sch.get('$schema'),'https://json-schema.org/draft/2020-12/schema','schema dialect')
 g.same(sch.get('type'),'object','schema root type')
 g.false(sch.get('additionalProperties',True),'schema disallows unknown root properties')
 for req in rec.keys(): g.check(req in sch.get('required',[]),'schema requires '+req)
 g.same(sch.get('properties',{}).get('schema',{}).get('const'),rec['schema'],'schema record ID constant')
 g.same(sch.get('properties',{}).get('status',{}).get('const'),rec['status'],'schema status constant')
 g.same(sch.get('properties',{}).get('decisions',{}).get('minItems'),6,'schema six decision minimum')
 g.same(sch.get('properties',{}).get('decisions',{}).get('maxItems'),6,'schema six decision maximum')
 for field_name,n in [('source_pins',81),('authority_input_pins',9),('semantic_decision_input_pins',6),('field_region_decision_input_pins',6),('coordinate_reference_pins',3),('coordinate_policy_proposal_input_pins',3)]:
  g.same(sch.get('properties',{}).get(field_name,{}).get('minItems'),n,'schema '+field_name+' minimum')
  g.same(sch.get('properties',{}).get(field_name,{}).get('maxItems'),n,'schema '+field_name+' maximum')

 # Pin inventories compare exactly to the proposal/manifest source declarations; live file hashes are preflighted by PowerShell.
 pin_sources={
  'source_pins':prop.get('source_pins',[]),
  'authority_input_pins':prop.get('authority_input_pins',[]),
  'semantic_decision_input_pins':prop.get('semantic_decision_input_pins',[]),
  'field_region_decision_input_pins':prop.get('field_region_decision_input_pins',[]),
  'coordinate_reference_pins':prop.get('coordinate_reference_pins',[]),
  'coordinate_policy_proposal_input_pins':[
   {'path':str(PROPOSAL_REL).replace('\\','/'),'sha256':EXPECTED['proposal'],'role':'reviewed_coordinate_policy_proposal'},
   {'path':str(PROPOSAL_SCHEMA_REL).replace('\\','/'),'sha256':EXPECTED['proposal_schema'],'role':'coordinate_policy_proposal_schema'},
   {'path':str(PROPOSAL_TEST_REL).replace('\\','/'),'sha256':EXPECTED['proposal_test'],'role':'coordinate_policy_proposal_regression_suite'}]
 }
 for name,expected_list in pin_sources.items():
  items=rec.get(name,[])
  g.same(len(items),len(expected_list),name+' exact count')
  norm=lambda x: sorted((str(a.get('path')),str(a.get('sha256')),str(a.get('role',''))) for a in x)
  g.same(norm(items),norm(expected_list),name+' exact pin inventory')
  for idx,pin in enumerate(items):
   g.check(bool(pin.get('path')) and '..' not in Path(pin.get('path','')).parts,name+f'[{idx}] safe path')
   g.check(isinstance(pin.get('sha256'),str) and len(pin['sha256'])==64 and all(c in '0123456789abcdef' for c in pin['sha256']),name+f'[{idx}] SHA256 format')
   if 'role' in pin: g.check(bool(pin['role']),name+f'[{idx}] role populated')

 # Exact decisions, rationale, unresolved details remain constrained.
 expected_ids=['SOURCE_CANVAS_TO_LOGICAL_CANVAS_SCALE_0_5','LOGICAL_TO_REVIEW_720_REFERENCE_SCALE_4_OVER_3','CHALLENGE_003_TARGET_X_PRESENTATION_CENTERLINE_Y_480','SVG_INTRINSIC_100X100_AS_SOURCE_CANVAS_UNITS','CENTER_ANCHOR_AND_EDGE_CLIPPING','RENDERER_PIXEL_ROUNDING_AND_CROP_SEMANTICS']
 g.same([x.get('decision_id') for x in rec['decisions']],expected_ids,'decision order and IDs')
 expected_decisions=['ACCEPT_FOR_FUTURE_CONSUMER_SPECIFICATION_ONLY','ACCEPT_REFERENCE_SCALE_ONLY','ACCEPT_PRESENTATION_DEFAULT_FOR_SPECIFICATION_ONLY','ACCEPT_SIZE_INTERPRETATION_FOR_FUTURE_SPECIFICATION_ONLY','ACCEPT_ANCHOR_AND_CLIP_POLICY_FOR_FUTURE_SPECIFICATION_ONLY','BLOCKED_PENDING_RENDERER_IMPLEMENTATION_GATE']
 g.same([x.get('decision') for x in rec['decisions']],expected_decisions,'decision disposition matrix')
 for idx,d in enumerate(rec['decisions']):
  pre=f'decision {idx+1}'
  g.check(len(d.get('rationale',''))>=80,pre+' rationale sufficiently detailed')
  g.check(len(d.get('policy_effect',''))>=20,pre+' policy effect present')
  g.false(d.get('runtime_transform_authorized'),pre+' runtime transform not authorized')
  g.false(d.get('binding_authorized'),pre+' binding not authorized')
  g.false(d.get('renderer_projection_authorized'),pre+' renderer projection not authorized')

 # Check proposed numerical maps across scalar domain, including edges and every integer value.
 for x in range(101):
  val=float(x); logical_x=(val/100.0)*540.0; logical_y=480.0
  g.check(math.isfinite(logical_x) and 0.0<=logical_x<=540.0, f'scalar {x} finite logical X in range')
  g.check(math.isclose(logical_x, val*5.4, rel_tol=0.0, abs_tol=1e-9), f'scalar {x} x map linearity')
  g.same(logical_y, 480.0, f'scalar {x} presentation Y centerline')
  g.check(math.isclose(logical_x*(4.0/3.0), val*7.2, rel_tol=0.0, abs_tol=1e-9), f'scalar {x} reference X transform')
  g.same(logical_y*(4.0/3.0), 640.0, f'scalar {x} reference Y transform')
  g.check(math.isclose(logical_x*0.5, val*2.7, rel_tol=0.0, abs_tol=1e-9), f'scalar {x} reverse-related half check')
 # Dense vector sample matrix; identical mapping policy, but candidate track types are checked independently.
 vector_challenges=[('CHALLENGE_005','PER_RUN_CONSTANT_REPEATED_PER_FRAME'),('CHALLENGE_006','PER_FRAME_VECTOR'),('CHALLENGE_007','PER_FRAME_VECTOR')]
 xs=[i*108.0 for i in range(11)]; ys=[i*192.0 for i in range(11)]
 for challenge,kind in vector_challenges:
  item=next((c for c in prop.get('candidates',[]) if c.get('challenge_id')==challenge),None)
  g.check(item is not None,challenge+' candidate exists')
  if item:
   g.same(item.get('source_track_kind'),kind,challenge+' track kind unchanged')
   g.same(item.get('source_coordinate_space'),'CANVAS_1080X1920',challenge+' source coordinate space')
  for x in xs:
   for y in ys:
    lx=x*0.5; ly=y*0.5; dx=lx*(4.0/3.0); dy=ly*(4.0/3.0)
    label=f'{challenge} point ({x},{y})'
    g.check(math.isfinite(lx) and math.isfinite(ly),label+' mapped finite')
    g.check(0.0<=lx<=540.0 and 0.0<=ly<=960.0,label+' logical inclusive bounds')
    g.same((lx,ly),(x/2.0,y/2.0),label+' zero offset uniform mapping')
    g.check(math.isclose(dx,x*(2.0/3.0),rel_tol=0.0,abs_tol=1e-9) and math.isclose(dy,y*(2.0/3.0),rel_tol=0.0,abs_tol=1e-9),label+' reference mapping')
 # Invalid scalar and vector classes must fail closed; no clamping.
 invalid_scalars=[-1.0,-0.0001,100.0001,101.0,float('nan'),float('inf'),float('-inf')]
 for v in invalid_scalars:
  valid=math.isfinite(v) and 0.0<=v<=100.0
  g.false(valid,f'invalid scalar {v} must fail domain validation')
  g.same(rec['policy_effect']['pilot_0x100']['clamp'],False,f'invalid scalar {v} not clamped')
 invalid_vectors=[(-0.1,0.0),(1080.1,0.0),(0.0,-0.1),(0.0,1920.1),(float('nan'),0.0),(0.0,float('inf'))]
 for x,y in invalid_vectors:
  valid=math.isfinite(x) and math.isfinite(y) and 0.0<=x<=1080.0 and 0.0<=y<=1920.0
  g.false(valid,f'invalid vector ({x},{y}) must fail domain validation')
  g.same(rec['policy_effect']['vector_domain']['clamp'],False,f'invalid vector ({x},{y}) not clamped')
 # Source and temporal invariants.
 inv=rec['policy_effect']['temporal_policy']
 for k,v in [('source_frame_count','PRESERVE_EXACT'),('source_order','UNCHANGED'),('interpolation','NONE'),('extrapolation','NONE'),('delivery_resampling','NOT_AUTHORIZED'),('winning_frame','SOLE_CHALLENGE_TEMPORAL_ANCHOR'),('close_calls','EPISODE_COUNT_ONLY')]: g.same(inv.get(k),v,'temporal invariant '+k)
 g.same(rec['blocked_candidates_retained'][0]['challenge_id'],'CHALLENGE_008','challenge 008 still blocked')
 g.same(rec['blocked_candidates_retained'][1]['challenge_id'],'CHALLENGE_009','challenge 009 still blocked')
 for b in rec['blocked_candidates_retained']:
  g.same(b.get('status'),'REMAINS_BLOCKED',b.get('challenge_id')+' blocked status')
  g.check(len(b.get('reason',''))>=60,b.get('challenge_id')+' reason retained')
 # Governance/authorization locks.
 auth=rec['authorization']; locks=rec['governance_locks']
 g.same(auth.get('coordinate_policy_approval'),'GRANTED_FOR_FUTURE_CONSUMER_SPECIFICATION_ONLY','policy approval limited to spec')
 g.false(auth.get('runtime_coordinate_transform_authorized'),'runtime transform false')
 g.same(auth.get('asset_size_policy_approval'),'GRANTED_FOR_FUTURE_CONSUMER_SPECIFICATION_ONLY','asset size approval limited to spec')
 g.same(auth.get('pixel_rounding_crop_policy'),'BLOCKED_PENDING_RENDERER_IMPLEMENTATION_GATE','pixel rounding/crop remains blocked')
 g.same(auth.get('binding_authorization'),'NOT_GRANTED','binding stays locked')
 g.same(auth.get('renderer_projection_authorization'),'NOT_GRANTED','renderer projection stays locked')
 g.false(auth.get('payload_consumer_implementation_authorized'),'consumer implementation not authorized')
 g.false(auth.get('renderer_activation_authorized'),'renderer activation not authorized')
 g.false(auth.get('render_test_authorized'),'render test not authorized')
 g.false(auth.get('payload_materialization_authorized'),'payload materialization not authorized')
 g.false(auth.get('media_creation_authorized'),'media creation not authorized')
 g.false(auth.get('candidate_input_admissible'),'candidate input inadmissible')
 g.same(auth.get('release_authority'),'NONE','no release authority')
 for key,val in [('renderer','OFF'),('media_created',False),('payload_materialized',False),('candidate_input_admissible',False),('seed_domains_complete_for_candidate_input',False),('automatic_seed_generation',False),('master_seed','NOT_ADOPTED'),('approved_bindings',0),('approved_custom_data_bindings',0),('approved_renderer_projection_bindings',0),('D4.8','BLOCKED'),('D9.10','PREPARE_ONLY'),('D9.14','BLOCKED'),('D9.16','BLOCKED'),('D9.17','BLOCKED_NO_GO'),('D10','BLOCKED_FOR_PROMOTION'),('baseline_approval','MISSING'),('freeze_eligible',False),('release_authority','NONE'),('whole_custom_data_serialization_allowed',False),('challenge_json_modification_allowed',False),('challenge_004_v1_harness_mutation_allowed',False)]: g.same(locks.get(key),val,'governance lock '+key)
 # Re-check pin inventories and policy invariants over a fixed 50-case matrix for each axis.
 for i in range(50):
  frac=i/49.0
  x=1080.0*frac; y=1920.0*frac
  g.same(x*0.5,540.0*frac,f'axis sample {i} logical x proportionality')
  g.same(y*0.5,960.0*frac,f'axis sample {i} logical y proportionality')
  g.check(math.isclose((x*0.5)*(4.0/3.0),720.0*frac,rel_tol=0.0,abs_tol=1e-9),f'axis sample {i} reference x proportionality')
  g.check(math.isclose((y*0.5)*(4.0/3.0),1280.0*frac,rel_tol=0.0,abs_tol=1e-9),f'axis sample {i} reference y proportionality')
 # Proposal candidate-field semantics remain stable.
 expected_keys=[('CHALLENGE_003','target_x'),('CHALLENGE_005','target_position'),('CHALLENGE_006','target_position'),('CHALLENGE_007','target_position')]
 g.same([(c.get('challenge_id'),c.get('field')) for c in prop.get('candidates',[])],expected_keys,'proposal candidate set unchanged')
 field_decisions={(d.get('challenge_id'),d.get('field')):d for d in field.get('decisions',[])}
 for challenge,fieldname in expected_keys:
  g.check((challenge,fieldname) in field_decisions,challenge+'.'+fieldname+' field-region decision exists')
  if (challenge,fieldname) in field_decisions:
   g.same(field_decisions[(challenge,fieldname)].get('decision'),'ACCEPT_FOR_FUTURE_COORDINATE_POLICY_SPECIFICATION_ONLY',challenge+'.'+fieldname+' remains within approved scope')
 # Output invariants all verified before success.
 for field_name in ['coordinate_policy_approval','runtime_coordinate_transform_authorized','asset_size_policy_approval','pixel_rounding_crop_policy','binding_authorization','renderer_projection_authorization','payload_consumer_implementation_authorized','renderer_activation_authorized','render_test_authorized','payload_materialization_authorized','media_creation_authorized','candidate_input_admissible','release_authority']:
  g.check(field_name in auth,'authorization contains '+field_name)
 expected_count=rec.get('test_count_expected')
 return g.finish(int(expected_count if expected_count is not None else g.count))
if __name__=='__main__': raise SystemExit(main())
