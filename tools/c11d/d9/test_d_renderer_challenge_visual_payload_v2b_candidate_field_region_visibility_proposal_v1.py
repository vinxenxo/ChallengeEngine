#!/usr/bin/env python3
"""Static regression tests for V2-B field-to-region/visibility proposal. No Godot, renderer or writes."""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path
C11C='e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953'
DESIGN='e4f02e37fd4b9b2c89cbaa7597162f87b180da43182dc576d664263c1b937cfc'
BINDING='d37cb74f360e19e664b94673bbf4b95462cad6e681a08215a95f4565c6e810aa'
BINDING_SCHEMA='f017a8a0081cc42f08af6381e7d47accb7a522ce89301ab9724d003a51c2dcf7'
REQUEST='b576612dd0913ce8f706a5272a5b9ca5ceb6c7a1f39d832323d9db98578b5d01'
REQUEST_SCHEMA='66e75d5fc136c0e3ffeeb2861abae8ac73d2e43eded257e54aadbd2736f2c68c'
DECISION_SCHEMA='ab09a617e9efc0aacb2111d9f6b02fc5764850f667cfdb33005451c5d4b073b9'
DECISION_RECORD='cc3550cd4d13f228ec9b3d51eeaa199505c5975b42882fb06ba3e83c4a000e90'
DECISION_TEST='d9e2c2516a248b62b60706f97f8b3d8132e871eb2b24117ebf3f594e69cb5e5f'
SOURCE_REVIEW='374472b2d7ab0a70d94ed1f650302869b829252dcf06a7afe29c7c2e18e345dc'
MATRIX='d69c3fb2aca78a26c3afbfda0084f7f7aef458ee404b37f65261c6d22e43121a'
V2C='6d3c59214edbdd917cf63fe9ca4859edb6968d503368ec84e867bdd56a8df74c'
RUNTIME_CONTRACT='f89235640f40c81be6100f01f1007ed4e787990a1bbf7927fcd8d676ef2cb9a3'
RUNTIME_REPORT='f7a1522695cbd6d3f3681d3f266b625e3062d5141c32cddbb4532bcb466e0446'
AUDIT='8c4503c128355fa21e670be0aaea25b093a73c325253a2afcec2a066a92e5f00'
IMPL_RECEIPT='e64cfd259914c471d03e8578b955140ad487b04694c5f682834517d823fcbfc4'
REQUEST_TEST='8de93859cd82e391d541d190f21d95a98a5508a7d5ee5952fe65eff256d1d53d'
DECISION_TEST_RECEIPT='3cf2284c454a06571ea97a2e771a259d2b73a8f4616432063a581b5c3e57ecf9'
ACCEPT='ACCEPT_SEMANTIC_DEFINITION_FOR_FUTURE_BINDING_SPECIFICATION'
EXPECTED=[('CHALLENGE_003','target_x','float','PILOT_0X100','assets/c6/waypoint.svg','PER_FRAME_SCALAR'),('CHALLENGE_005','target_position','Vector2','CANVAS_1080X1920','assets/c6/target.svg','PER_RUN_CONSTANT_REPEATED_PER_FRAME'),('CHALLENGE_006','target_position','Vector2','CANVAS_1080X1920','assets/c6/target.svg','PER_FRAME_VECTOR'),('CHALLENGE_007','target_position','Vector2','CANVAS_1080X1920','assets/c6/target.svg','PER_FRAME_VECTOR')]
def sha(p:Path): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p:Path): return json.loads(p.read_text(encoding='utf-8'))
def main()->int:
 root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd().resolve()
 n=0
 def ck(label, cond):
  nonlocal n
  if not cond:
   print('FAIL '+label,file=sys.stderr); raise AssertionError(label)
  n+=1
 p=root/'definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_PROPOSAL_V1.json'
 s=root/'definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_PROPOSAL_SCHEMA_V1.json'
 dp=root/'definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_SEMANTIC_DECISION_RECORD_V1.json'
 ds=root/'definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_SEMANTIC_DECISION_RECORD_SCHEMA_V1.json'
 rp=root/'definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_SEMANTIC_REVIEW_REQUEST_V1.json'
 rs=root/'definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_SEMANTIC_REVIEW_REQUEST_SCHEMA_V1.json'
 designp=root/'definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SAFE_VISUAL_PROJECTION_DESIGN_V1.json'
 bp=root/'definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_SEMANTIC_BINDING_PROPOSAL_V1.json'
 bsp=root/'definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_SEMANTIC_BINDING_PROPOSAL_SCHEMA_V1.json'
 srcp=root/'definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_SOURCE_SEMANTIC_REVIEW_V1.json'
 mp=root/'definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SEED_TEST_MATRIX_V1.json'
 v2cp=root/'definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2C_SOURCE_FRAME_RUNTIME_RECEIPT_V1.json'
 runtimep=root/'definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SAFE_PROJECTION_RUNTIME_CONTRACT_V1.json'
 frozenp=root/'release/C11C_FREEZE_PACKAGE_MANIFEST.json'
 tp=root/'tools/c11d/d9/test_d_renderer_challenge_visual_payload_v2b_candidate_field_region_visibility_proposal_v1.py'
 required=[p,s,dp,ds,rp,rs,designp,bp,bsp,srcp,mp,v2cp,runtimep,frozenp,tp]
 for x in required: ck('required '+x.name,x.is_file())
 proposal=read(p); schema=read(s); decision=read(dp); decisionschema=read(ds); request=read(rp); request_schema=read(rs); design=read(designp); binding=read(bp); binding_schema=read(bsp); source_review=read(srcp); matrix=read(mp); v2c=read(v2cp); runtime=read(runtimep)
 ck('proposal schema ID',proposal.get('schema')=='C11D-V2B-CANDIDATE-FIELD-REGION-VISIBILITY-PROPOSAL-V1')
 ck('proposal schema version',proposal.get('schema_version')=='1.0')
 ck('proposal stays unapproved',proposal.get('status')=='PROPOSED_NOT_APPROVED_OPERATOR_REVIEW_REQUIRED')
 ck('root strict schema',schema.get('additionalProperties') is False)
 ck('schema ID matches proposal',schema.get('properties',{}).get('schema',{}).get('const')==proposal.get('schema'))
 ck('schema version matches proposal',schema.get('properties',{}).get('schema_version',{}).get('const')==proposal.get('schema_version'))
 ck('schema root required exact',set(proposal.keys())==set(schema.get('required',[])))
 ck('proposal has no unknown root keys',set(proposal.keys()).issubset(set(schema.get('properties',{}))))
 ck('candidate objects strict schema',schema.get('properties',{}).get('candidates',{}).get('items',{}).get('additionalProperties') is False)
 ck('nested region strict schema',schema.get('properties',{}).get('candidates',{}).get('items',{}).get('properties',{}).get('region_mapping',{}).get('additionalProperties') is False)
 ck('nested visibility strict schema',schema.get('properties',{}).get('candidates',{}).get('items',{}).get('properties',{}).get('visibility_policy',{}).get('additionalProperties') is False)
 ck('nested sample contract strict schema',schema.get('properties',{}).get('candidates',{}).get('items',{}).get('properties',{}).get('sample_contract',{}).get('additionalProperties') is False)
 ck('source authority strict schema',schema.get('properties',{}).get('source_authority',{}).get('additionalProperties') is False)
 ck('governance strict schema',schema.get('properties',{}).get('governance',{}).get('additionalProperties') is False)
 ck('decision gate strict schema',schema.get('properties',{}).get('decision_gate',{}).get('additionalProperties') is False)
 ck('provenance decision record SHA',sha(dp)==DECISION_RECORD)
 ck('provenance decision schema SHA',sha(ds)==DECISION_SCHEMA)
 ck('provenance review request SHA',sha(rp)==REQUEST)
 ck('provenance review request schema SHA',sha(rs)==REQUEST_SCHEMA)
 ck('provenance design SHA',sha(designp)==DESIGN)
 ck('provenance binding proposal SHA',sha(bp)==BINDING)
 ck('provenance binding proposal schema SHA',sha(bsp)==BINDING_SCHEMA)
 ck('provenance source review SHA',sha(srcp)==SOURCE_REVIEW)
 ck('provenance seed matrix SHA',sha(mp)==MATRIX)
 ck('provenance V2-C SHA',sha(v2cp)==V2C)
 ck('provenance runtime contract SHA',sha(runtimep)==RUNTIME_CONTRACT)
 ck('frozen C11-C manifest SHA',sha(frozenp)==C11C)
 ck('request remains immutable and pending in source',request.get('status')=='PENDING_EXPLICIT_SEMANTIC_DECISIONS')
 ck('decision record is separately recorded',decision.get('status')=='SEMANTIC_DECISIONS_RECORDED_BINDINGS_NOT_APPROVED')
 ck('decision record binding authorization not granted',decision.get('binding_authorization')=='NOT_GRANTED_BY_SEMANTIC_REVIEW')
 ck('decision record renderer authorization not granted',decision.get('renderer_projection_authorization')=='NOT_GRANTED_BY_SEMANTIC_REVIEW')
 ck('decision schema strict',decisionschema.get('additionalProperties') is False)
 ck('review request schema strict',request_schema.get('additionalProperties') is False)
 ck('binding proposal stays proposal-only',binding.get('status')=='PREPARATION_ONLY_PROPOSAL_NOT_APPROVED_NOT_RUNTIME_ACCEPTANCE')
 ck('binding proposal schema strict',binding_schema.get('additionalProperties') is False)
 ck('design has 81 source pins',len(design.get('source_pins',[]))==81)
 ck('proposal source pin count 81',len(proposal.get('source_pins',[]))==81)
 ck('source pins copied exactly from design',proposal.get('source_pins')==design.get('source_pins'))
 ck('source pin paths unique',len({x.get('path') for x in proposal.get('source_pins',[])})==81)
 for pin in proposal['source_pins']:
  f=root/pin['path']; ck('source pin path '+pin['path'],f.is_file())
  ck('source pin sha '+pin['path'],sha(f)==pin['sha256'])
 ck('design has nine authority pins',len(design.get('authority_input_pins',[]))==9)
 ck('proposal authority pin count nine',len(proposal.get('authority_input_pins',[]))==9)
 ck('authority pins copied exactly from design',proposal.get('authority_input_pins')==design.get('authority_input_pins'))
 ck('authority pin paths unique',len({x.get('path') for x in proposal.get('authority_input_pins',[])})==9)
 for pin in proposal['authority_input_pins']:
  f=root/pin['path']; ck('authority path '+pin['path'],f.is_file())
  ck('authority sha '+pin['path'],sha(f)==pin['sha256'])
 ck('six semantic decision input pins',len(proposal.get('semantic_decision_input_pins',[]))==6)
 for pin in proposal['semantic_decision_input_pins']:
  f=root/pin['path']; ck('decision input path '+pin['path'],f.is_file())
  ck('decision input sha '+pin['path'],sha(f)==pin['sha256'])
 ck('source authority frozen pin',proposal['source_authority']['frozen_c11c_manifest_sha256']==C11C)
 ck('source authority design pin',proposal['source_authority']['design_contract_sha256']==DESIGN)
 ck('source authority binding proposal pin',proposal['source_authority']['semantic_binding_proposal_sha256']==BINDING)
 ck('source authority request pin',proposal['source_authority']['semantic_review_request_sha256']==REQUEST)
 ck('source authority decision record pin',proposal['source_authority']['semantic_decision_record_sha256']==DECISION_RECORD)
 ck('evidence audit hash pinned',proposal['evidence_pins']['candidate_evidence_audit_json_sha256']==AUDIT)
 ck('runtime report hash pinned',proposal['evidence_pins']['runtime_report_sha256']==RUNTIME_REPORT)
 ck('implementation receipt hash pinned',proposal['evidence_pins']['implementation_test_receipt_sha256']==IMPL_RECEIPT)
 ck('review-request test receipt hash pinned',proposal['evidence_pins']['semantic_review_request_test_receipt_sha256']==REQUEST_TEST)
 ck('decision record test count is 146',proposal['evidence_pins']['semantic_decision_record_test_count']==146)
 ck('operator-provided decision stdout SHA pinned',proposal['evidence_pins']['semantic_decision_record_test_stdout_sha256']=='e0c05466cb7d14cfb7efb049a1d9f2ac8f5fb5b73a4d81b769b073edbf4c96f7')
 ck('decision stderr empty SHA pinned',proposal['evidence_pins']['semantic_decision_record_test_stderr_sha256']=='e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')
 ck('operator-provided decision receipt SHA pinned',proposal['evidence_pins']['semantic_decision_record_test_receipt_sha256']==DECISION_TEST_RECEIPT)
 ck('candidate count field exact',proposal.get('candidate_count')==4)
 ck('candidate list cardinality exact',len(proposal.get('candidates',[]))==4)
 ck('candidate identity/order exact',[(x.get('challenge_id'),x.get('field'),x.get('semantic_type'),x.get('coordinate_space'),x.get('asset_path'),x.get('source_track_kind')) for x in proposal['candidates']]==EXPECTED)
 ck('four accepted decisions only in scope',all(x.get('semantic_decision')==ACCEPT for x in proposal['candidates']))
 ck('blocked 008/009 excluded',proposal['scope']['excluded_blocked_challenge_fields']==['CHALLENGE_008.active_selection','CHALLENGE_009.displayed_count'])
 ck('source decision record still has six decisions',len(decision.get('decisions',[]))==6)
 ck('source decision record first four accepted',all(x.get('semantic_decision')==ACCEPT for x in decision['decisions'][:4]))
 ck('source decision record last two remain blocked',all(x.get('semantic_decision')=='BLOCKED_NEEDS_SOURCE_OR_POLICY_DECISION' for x in decision['decisions'][4:]))
 ck('no blocked candidate is copied into proposal',not any(x.get('challenge_id') in {'CHALLENGE_008','CHALLENGE_009'} for x in proposal['candidates']))
 ck('semantic scope only',proposal['scope']['kind']=='FIELD_TO_REGION_AND_VISIBILITY_PROPOSAL_ONLY')
 ck('source-frame-only proposal',proposal['scope']['source_frame_only'] is True)
 ck('runtime reexecution forbidden',proposal['scope']['runtime_reexecution'] is False)
 ck('payload materialization forbidden',proposal['scope']['payload_materialized'] is False)
 ck('consumer output forbidden',proposal['scope']['payload_files_written_by_consumer'] is False)
 ck('renderer native input absent',proposal['scope']['renderer_native_input_emitted'] is False)
 ck('renderer dispatch absent',proposal['scope']['renderer_dispatch_invoked'] is False)
 ck('media absent',proposal['scope']['media_output_created'] is False)
 ck('challenge modifications forbidden',proposal['scope']['challenge_json_modification_allowed'] is False)
 ck('renderer OFF',proposal['governance']['renderer']=='OFF')
 ck('media_created false',proposal['governance']['media_created'] is False)
 ck('payload_materialized false',proposal['governance']['payload_materialized'] is False)
 ck('candidate input inadmissible',proposal['governance']['candidate_input_admissible'] is False)
 ck('seed domains incomplete',proposal['governance']['seed_domains_complete_for_candidate_input'] is False)
 ck('automatic seed generation false',proposal['governance']['automatic_seed_generation'] is False)
 ck('master seed not adopted',proposal['governance']['master_seed']=='NOT_ADOPTED')
 ck('approved bindings zero',proposal['governance']['approved_bindings']==0)
 ck('approved custom-data bindings zero',proposal['governance']['approved_custom_data_bindings']==0)
 ck('approved renderer projections zero',proposal['governance']['approved_renderer_projection_bindings']==0)
 ck('binding authorization not granted',proposal['governance']['binding_authorization']=='NOT_GRANTED')
 ck('projection authorization not granted',proposal['governance']['renderer_projection_authorization']=='NOT_GRANTED')
 ck('consumer implementation not authorized',proposal['governance']['payload_consumer_implementation_authorized'] is False)
 ck('runtime reexecution not authorized',proposal['governance']['runtime_reexecution_authorized'] is False)
 ck('D4.8 remains blocked',proposal['governance']['D4.8']=='BLOCKED')
 ck('D9.10 stays prepare-only',proposal['governance']['D9.10']=='PREPARE_ONLY')
 ck('D9.14 remains blocked',proposal['governance']['D9.14']=='BLOCKED')
 ck('D9.16 remains blocked',proposal['governance']['D9.16']=='BLOCKED')
 ck('D9.17 remains no-go',proposal['governance']['D9.17']=='BLOCKED_NO_GO')
 ck('D10 promotion blocked',proposal['governance']['D10']=='BLOCKED_FOR_PROMOTION')
 ck('baseline approval missing',proposal['governance']['baseline_approval']=='MISSING')
 ck('freeze eligibility false',proposal['governance']['freeze_eligible'] is False)
 ck('release authority none',proposal['governance']['release_authority']=='NONE')
 ck('whole custom-data map never allowed',proposal['governance']['whole_custom_data_serialization_allowed'] is False)
 ck('Challenge004 V1 harness frozen',proposal['governance']['challenge_004_v1_harness_mutation_allowed'] is False)
 ck('decision gate pending operator review',proposal['decision_gate']['status']=='PENDING_EXPLICIT_OPERATOR_REVIEW')
 ck('next gate requires separate record','OPERATOR_FIELD_REGION_VISIBILITY_DECISION_RECORD_REQUIRED' in proposal['decision_gate']['next_gate'])
 ck('future approval does not grant bindings',proposal['decision_gate']['accepted_proposal_decision_does_not_grant_binding_or_renderer_authority'] is True)
 ck('coordinate policy separated',proposal['decision_gate']['coordinate_projection_requires_separate_explicit_policy_and_authorization'] is True)
 ck('decision record separate',proposal['decision_gate']['review_record_must_be_separate_from_this_immutable_proposal'] is True)
 ck('proposal count four decisions',proposal['decision_gate']['required_candidate_decisions']==4)
 ck('design nine selectors retained',matrix.get('whole_increment_invocations',{}).get('selector_count')==9)
 ck('V2-C source frame contract retained',v2c.get('schema')=='C11D-CHALLENGE-VISUAL-PAYLOAD-V2C-SOURCE-FRAME-RUNTIME-RECEIPT-CONTRACT-V1')
 ck('runtime contract renderer lock',runtime.get('renderer')=='OFF')
 ck('runtime contract media lock',runtime.get('media_created') is False)
 ck('runtime contract payload lock',runtime.get('payload_materialized') is False)
 ck('source review zero approved bindings',source_review.get('review_summary',{}).get('approved_bindings')==0)
 ck('source review zero approved custom bindings',source_review.get('review_summary',{}).get('approved_custom_data_bindings')==0)
 ck('existing semantic binding proposal has 9 selector semantics',len(binding.get('selector_semantics',[]))==9)
 ck('asset role owner uses exact existing semantic source',all(x.get('asset_role')=='TARGET' and x.get('asset_role_source')=='EXISTING_SEMANTIC_BINDING_PROPOSAL_ONLY' for x in proposal['candidates']))
 # Candidate-by-candidate structural and semantic tests.
 for c in proposal['candidates']:
  cid=c['challenge_id']; r=c['region_mapping']; sample=c['sample_contract']; vis=c['visibility_policy']; track=c['track_specific_policy']
  ck(cid+' accepted semantic decision',c['semantic_decision']==ACCEPT)
  ck(cid+' candidate remains proposal only',c['proposal_status']=='PROPOSED_NOT_APPROVED')
  ck(cid+' binding false',c['binding_authorized'] is False)
  ck(cid+' renderer projection false',c['renderer_projection_approved'] is False)
  ck(cid+' consumer not authorized',c['payload_consumer_implementation_authorized'] is False)
  ck(cid+' not renderable',c['candidate_renderable'] is False)
  ck(cid+' source challenge pinned',c['source_challenge_sha256']==next(x['sha256'] for x in design['source_pins'] if x['path']==c['source_challenge_path']))
  ck(cid+' source mechanic pinned',c['source_mechanic_sha256']==next(x['sha256'] for x in design['source_pins'] if x['path']==c['source_mechanic_path']))
  ck(cid+' source pointer field allowlisted',c['source_pointer']=='FrameSnapshot.custom_data.'+c['field'])
  ck(cid+' semantic owner target marker',r['semantic_owner']=='CHALLENGE_TARGET_MARKER')
  ck(cid+' region pending',r['proposal_status']=='PROPOSED_NOT_APPROVED')
  ck(cid+' region asset role TARGET',r['asset_role']=='TARGET')
  ck(cid+' asset path source pinned',r['asset_path'] in {x['path'] for x in design['source_pins']})
  ck(cid+' center anchor proposal labelled',r['anchor_policy']=='ASSET_CENTER_AT_SOURCE_SEMANTIC_POSITION_PROPOSED_NOT_APPROVED')
  ck(cid+' destination unresolved',r['renderer_destination_space']=='UNRESOLVED_NOT_APPROVED')
  ck(cid+' logical 540x960 not invented',r['logical_frame_540x960_bounds'] is None)
  ck(cid+' delivery transform not invented',r['delivery_profile_720x1280_transform'] is None)
  ck(cid+' destination bounds absent',r['destination_region_bounds'] is None)
  ck(cid+' transform not applied',r['coordinate_transform_applied'] is False)
  ck(cid+' transform not authorized',r['coordinate_transform_authorized'] is False)
  ck(cid+' pixel placement not authorized',r['actual_pixel_placement_authorized'] is False)
  ck(cid+' asset scale unresolved',r['asset_scale_policy']=='UNRESOLVED_NOT_APPROVED')
  ck(cid+' expected count exactly source frames',sample['expected_sample_count']=='EXACT_SOURCE_FRAME_COUNT')
  ck(cid+' source frame index zero origin',sample['frame_index_origin']==0)
  ck(cid+' source frame index unit step',sample['frame_index_step']==1)
  ck(cid+' finite samples required',sample['require_finite_values'] is True)
  ck(cid+' missing values fail closed',sample['missing_sample_behavior']=='FAIL_CLOSED_REJECT_WHOLE_CANDIDATE_TRACK')
  ck(cid+' nonfinite values fail closed',sample['nonfinite_sample_behavior']=='FAIL_CLOSED_REJECT_WHOLE_CANDIDATE_TRACK')
  ck(cid+' cardinality mismatch fail closed',sample['cardinality_mismatch_behavior']=='FAIL_CLOSED_REJECT_WHOLE_CANDIDATE_TRACK')
  ck(cid+' interpolation prohibited',sample['interpolation']=='NONE')
  ck(cid+' extrapolation prohibited',sample['extrapolation']=='NONE')
  ck(cid+' delivery resampling not allowed',sample['delivery_resampling']=='NOT_ALLOWED_BY_THIS_PROPOSAL')
  ck(cid+' allowlist only',sample['only_allowlisted_field_read'] is True)
  ck(cid+' whole custom_data map never serialized',sample['serialize_whole_custom_data_map'] is False)
  ck(cid+' visibility proposal not approved',vis['status']=='PROPOSED_NOT_APPROVED')
  ck(cid+' full source-frame span proposed',vis['candidate_window']=='FULL_SOURCE_FRAME_SPAN')
  ck(cid+' first visible sample frame 0',vis['first_source_frame_index']==0)
  ck(cid+' last frame uses frame-count sentinel',vis['last_source_frame_index']=='SOURCE_FRAME_COUNT_MINUS_ONE')
  ck(cid+' exact finite field sample for visibility',vis['visible_sample_condition']=='EXACT_FIELD_SAMPLE_PRESENT_AND_FINITE_FOR_EVERY_SOURCE_FRAME')
  ck(cid+' invalid values fail whole track',vis['invalid_sample_behavior']=='FAIL_CLOSED_REJECT_WHOLE_CANDIDATE_TRACK_NOT_HIDE_ONE_FRAME_OR_FALLBACK')
  ck(cid+' no phase inference',vis['no_phase_inference'] is True)
  ck(cid+' close calls not visibility signal',vis['no_visibility_change_from_close_calls'] is True)
  ck(cid+' winning_frame is sole challenge anchor','WINNING_FRAME_REMAINS_THE_ONLY_CHALLENGE_TEMPORAL_ANCHOR' in vis['winning_frame_policy'])
  ck(cid+' close_calls episode-only','EPISODE_COUNT_ONLY' in vis['close_calls_policy'])
  ck(cid+' render-enable remains blocked',vis['actual_render_enablement'].startswith('BLOCKED_UNTIL_'))
  ck(cid+' operator review pending',vis['visibility_window_approval']=='PENDING_OPERATOR_REVIEW')
  ck(cid+' candidate track kind exact',track['kind']==c['source_track_kind'])
  ck(cid+' fallback none',track['extra_semantic_fallback']=='NONE')
  ck(cid+' prohibited inputs list complete',len(c['prohibited_inputs'])==8)
  ck(cid+' no score-result fallback','SIMULATION_SCORE_OR_RESULT_TELEMETRY' in c['prohibited_inputs'])
  ck(cid+' no raw map', 'WHOLE_FRAME_SNAPSHOT_CUSTOM_DATA_MAP' in c['prohibited_inputs'])
 # Candidate-specific meaning checks.
 c3,c5,c6,c7=proposal['candidates']
 ck('003 field remains scalar target_x',c3['semantic_type']=='float' and c3['field']=='target_x')
 ck('003 pilot coordinate space retained',c3['coordinate_space']=='PILOT_0X100')
 ck('003 X only no invented Y',c3['coordinate_policy']=='X_AXIS_ONLY_NO_2D_POSITION_CONVERSION')
 ck('003 missing Y mapping blocker explicit','Y_COORDINATE_ABSENT' in c3['mapping_blocker'])
 ck('003 asset waypoint role retained',c3['asset_path']=='assets/c6/waypoint.svg')
 ck('003 scalar per source frame',c3['sample_rule']=='ONE_FINITE_SCALAR_PER_SOURCE_FRAME')
 ck('003 track may vary by frame','MAY_VARY' in c3['constancy_rule'])
 ck('005 vector semantic type',c5['semantic_type']=='Vector2')
 ck('005 target remains source-canvas point',c5['coordinate_space']=='CANVAS_1080X1920')
 ck('005 run-constant repeated track',c5['source_track_kind']=='PER_RUN_CONSTANT_REPEATED_PER_FRAME')
 ck('005 exact constant vector rule','EQUAL_ACROSS_ALL_FRAMES' in c5['sample_rule'])
 ck('005 no trajectory substitution',c5['constancy_rule']=='SAME_TARGET_VECTOR_FOR_ALL_SOURCE_FRAMES_IN_ONE_RUN')
 ck('005 projectile remains primary track',c5['track_specific_policy']['primary_snapshot_position_role']=='PROJECTILE_PRIMARY_POSITION_REMAINS_SEPARATE_FROM_TARGET_POSITION')
 ck('006 source track is per-frame Vector2',c6['source_track_kind']=='PER_FRAME_VECTOR' and c6['semantic_type']=='Vector2')
 ck('006 catcher position separate',c6['track_specific_policy']['primary_snapshot_position_role']=='CATCHER_PRIMARY_POSITION_REMAINS_SEPARATE_FROM_TARGET_POSITION')
 ck('006 exact frame cardinality',c6['sample_rule']=='ONE_FINITE_VECTOR2_PER_SOURCE_FRAME_EXACT_CARDINALITY')
 ck('007 scanner position separate',c7['track_specific_policy']['primary_snapshot_position_role']=='SCANNER_PRIMARY_POSITION_REMAINS_SEPARATE_FROM_TARGET_POSITION')
 ck('007 exact frame cardinality',c7['sample_rule']=='ONE_FINITE_VECTOR2_PER_SOURCE_FRAME_EXACT_CARDINALITY')
 ck('007 distractor topology prohibited','DISTRACTOR_TOPOLOGY' in c7['prohibited_inputs'])
 ck('008/009 timebase conflict still present in request',any(x.get('challenge_id')=='CHALLENGE_008' for x in request['candidates']) and any(x.get('challenge_id')=='CHALLENGE_009' for x in request['candidates']))
 ck('no timing conflict silently solved',not any('CHALLENGE_008' in x or 'CHALLENGE_009' in x for x in proposal['scope']['included_challenge_fields']))
 ck('governance scope says no challenge changes',proposal['scope']['challenge_json_modification_allowed'] is False)
 ck('manifest C11-C unchanged after audit',sha(frozenp)==C11C)
 ck('proposal static test denominator pinned',proposal['evidence_pins']['field_region_visibility_test_count_expected']==551)
 ck('static test denominator remains fixed',n==550)
 print(f'C11D_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_PROPOSAL_TESTS={n}/551')
 print('C11D_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_CANDIDATES=4/4')
 print('C11D_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_SOURCE_PINS=81/81')
 print('C11D_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_AUTHORITY_INPUT_PINS=9/9')
 print('C11D_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_DECISION_INPUT_PINS=6/6')
 print('C11D_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_STATUS=PROPOSED_NOT_APPROVED')
 print('C11D_V2B_BINDING_AUTHORIZATION=NOT_GRANTED')
 print('C11D_V2B_RENDERER_PROJECTION_AUTHORIZATION=NOT_GRANTED')
 print('C11D_V2B_CANDIDATE_INPUT_ADMISSIBLE=false')
 print('C11D_V2B_RENDERER=OFF')
 print('C11D_V2B_MEDIA_CREATED=false')
 return 0
if __name__=='__main__': raise SystemExit(main())
