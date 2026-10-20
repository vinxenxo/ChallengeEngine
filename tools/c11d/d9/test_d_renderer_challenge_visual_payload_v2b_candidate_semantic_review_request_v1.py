#!/usr/bin/env python3
"""Static validation for the source-bound V2-B semantic review request; no runtime work."""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path

C11C="e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
DESIGN="e4f02e37fd4b9b2c89cbaa7597162f87b180da43182dc576d664263c1b937cfc"
MATRIX="d69c3fb2aca78a26c3afbfda0084f7f7aef458ee404b37f65261c6d22e43121a"
V2C="6d3c59214edbdd917cf63fe9ca4859edb6968d503368ec84e867bdd56a8df74c"
RUNTIME_CONTRACT="f89235640f40c81be6100f01f1007ed4e787990a1bbf7927fcd8d676ef2cb9a3"
RUNTIME_REPORT="f7a1522695cbd6d3f3681d3f266b625e3062d5141c32cddbb4532bcb466e0446"
AUDIT_SHA="8c4503c128355fa21e670be0aaea25b093a73c325253a2afcec2a066a92e5f00"
IMPL_RECEIPT="e64cfd259914c471d03e8578b955140ad487b04694c5f682834517d823fcbfc4"
AUDIT_TEST_RECEIPT="1a57d59a41c87696a07128fd397db0f031f74d87ac42fb1877a084a1c2c5631d"
FIX_TEST_RECEIPT="6b8b166c36a1341ceec23cde38c4999d7aa6aacb26a5153459ce05879fec1043"
SOURCE_REVIEW_SHA="374472b2d7ab0a70d94ed1f650302869b829252dcf06a7afe29c7c2e18e345dc"
EXPECTED = {
 "CHALLENGE_003": ("target_x", "float", "PILOT_0X100", "INVARIANT_EXPECTED_AND_OBSERVED_NOT_A_SEED_SENSITIVITY_ORACLE"),
 "CHALLENGE_005": ("target_position", "Vector2", "CANVAS_1080X1920", "CHANGES_WITH_GAMEPLAY_SEED_AS_EXPECTED"),
 "CHALLENGE_006": ("target_position", "Vector2", "CANVAS_1080X1920", "CHANGES_WITH_GAMEPLAY_SEED_AS_EXPECTED"),
 "CHALLENGE_007": ("target_position", "Vector2", "CANVAS_1080X1920", "CHANGES_WITH_GAMEPLAY_SEED_AS_EXPECTED"),
 "CHALLENGE_008": ("active_selection", "int", "Option index; declared option positions use CANVAS_1080X1920", "CHANGES_WITH_GAMEPLAY_SEED_AS_EXPECTED"),
 "CHALLENGE_009": ("displayed_count", "int", "Count integer plus positional encoding in CANVAS_1080X1920", "CHANGES_WITH_GAMEPLAY_SEED_AS_EXPECTED"),
}
def sha(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()
def jread(path: Path): return json.loads(path.read_text(encoding="utf-8"))
def main() -> int:
 p=argparse.ArgumentParser()
 p.add_argument('--repo-root', type=Path, default=Path.cwd())
 p.add_argument('--candidate-audit-json', type=Path, required=True)
 p.add_argument('--expected-candidate-audit-sha256', required=True)
 a=p.parse_args(); root=a.repo_root.resolve(); checks=[]
 def add(name, fn):
  try:
   assert fn(), name
   checks.append((name,True))
  except Exception as exc:
   print(f"FAIL {name}: {exc}",file=sys.stderr); return False
  return True
 request_path=root/'definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_SEMANTIC_REVIEW_REQUEST_V1.json'
 schema_path=root/'definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_SEMANTIC_REVIEW_REQUEST_SCHEMA_V1.json'
 decision_schema_path=root/'definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_SEMANTIC_DECISION_RECORD_SCHEMA_V1.json'
 source_path=root/'definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_SOURCE_SEMANTIC_REVIEW_V1.json'
 design_path=root/'definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SAFE_VISUAL_PROJECTION_DESIGN_V1.json'
 matrix_path=root/'definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SEED_TEST_MATRIX_V1.json'
 v2c_path=root/'definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2C_SOURCE_FRAME_RUNTIME_RECEIPT_V1.json'
 runtime_contract_path=root/'definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SAFE_PROJECTION_RUNTIME_CONTRACT_V1.json'
 frozen_path=root/'release/C11C_FREEZE_PACKAGE_MANIFEST.json'
 candidate_audit_path=a.candidate_audit_json.resolve()
 for nm, path in [('request',request_path),('schema',schema_path),('decision schema',decision_schema_path),('source semantic review',source_path),('design',design_path),('matrix',matrix_path),('V2-C',v2c_path),('runtime contract',runtime_contract_path),('C11-C',frozen_path),('candidate audit JSON',candidate_audit_path)]:
  if not add('file exists: '+nm, path.is_file): return 1
 checks_json = {}
 for nm,path,expected in [
  ('source semantic review',source_path,SOURCE_REVIEW_SHA),('design',design_path,DESIGN),('matrix',matrix_path,MATRIX),('V2-C',v2c_path,V2C),('runtime contract',runtime_contract_path,RUNTIME_CONTRACT),('C11-C',frozen_path,C11C),('candidate audit',candidate_audit_path,AUDIT_SHA)]:
  if not add('pinned SHA: '+nm, lambda path=path,expected=expected: sha(path)==expected): return 1
 if a.expected_candidate_audit_sha256.lower()!=AUDIT_SHA: print('FAIL CLI audit SHA pin',file=sys.stderr); return 1
 req=jread(request_path); sch=jread(schema_path); dsch=jread(decision_schema_path); src=jread(source_path); design=jread(design_path); audit=jread(candidate_audit_path)
 for name, condition in [
  ('request schema id',req.get('schema')=='C11D-V2B-CANDIDATE-SEMANTIC-REVIEW-REQUEST-V1'),
  ('request schema version',req.get('schema_version')=='1.0'),
  ('request status pending',req.get('status')=='PENDING_EXPLICIT_SEMANTIC_DECISIONS'),
  ('schema id matches request',sch.get('properties',{}).get('schema',{}).get('const')==req.get('schema')),
  ('schema strict root',sch.get('additionalProperties') is False),
  ('decision schema strict root',dsch.get('additionalProperties') is False),
  ('decision schema id',dsch.get('properties',{}).get('schema',{}).get('const')=='C11D-V2B-CANDIDATE-SEMANTIC-DECISION-RECORD-V1'),
  ('decision schema does not authorize binding',dsch.get('properties',{}).get('binding_authorization',{}).get('const')=='NOT_GRANTED_BY_SEMANTIC_REVIEW'),
  ('audit status accepted',audit.get('status')=='PASS_CANDIDATE_EVIDENCE_AUDIT'),
  ('audit root id',audit.get('schema')=='C11D-V2B-CANDIDATE-EVIDENCE-AUDIT-V1'),
  ('audit root has 9 selectors',len(audit.get('selectors',[]))==9),
  ('audit planner count 45',audit.get('planner_invocations')==45),
  ('audit Godot count 45',audit.get('godot_runtime_processes')==45),
  ('audit approved bindings zero',audit.get('approved_bindings')==0),
  ('audit approved custom_data bindings zero',audit.get('approved_custom_data_bindings')==0),
  ('audit raw values disabled',audit.get('raw_candidate_values_included') is False),
  ('request audit pin matches CLI',req.get('evidence_pins',{}).get('candidate_evidence_audit_json_sha256')==sha(candidate_audit_path)),
  ('request runtime hash matches audit',req.get('evidence_pins',{}).get('runtime_report_sha256')==audit.get('runtime_report_sha256')==RUNTIME_REPORT),
  ('request static receipt hash matches audit',req.get('evidence_pins',{}).get('implementation_test_receipt_sha256')==audit.get('implementation_test_receipt_sha256')==IMPL_RECEIPT),
  ('request source review pin',req.get('evidence_pins',{}).get('source_semantic_review_sha256')==SOURCE_REVIEW_SHA),
  ('request design pin',req.get('evidence_pins',{}).get('v2b_design_contract_sha256')==DESIGN),
  ('request seed matrix pin',req.get('evidence_pins',{}).get('v2b_seed_matrix_sha256')==MATRIX),
  ('request V2-C pin',req.get('evidence_pins',{}).get('v2c_source_frame_contract_sha256')==V2C),
  ('request frozen manifest pin',req.get('evidence_pins',{}).get('frozen_c11c_manifest_sha256')==C11C),
  ('runtime gate status',req.get('runtime_acceptance_scope',{}).get('status')=='PASS_SAFE_PROJECTION_SEED_SENSITIVITY'),
  ('source review has zero approved bindings',src.get('review_summary',{}).get('approved_bindings')==0),
  ('source review has six custom candidates',len(src.get('custom_data_candidate_reviews',[]))==6),
  ('design pins denominators 81/9',len(design.get('source_pins',[]))==81 and len(design.get('authority_input_pins',[]))==9),
  ('candidate count 6',req.get('candidate_count')==6 and len(req.get('candidates',[]))==6),
  ('candidate IDs exact and ordered',[r.get('challenge_id') for r in req.get('candidates',[])]==list(EXPECTED)),
  ('candidate semantics match source review',[(r.get('challenge_id'),r.get('field'),r.get('semantic_type')) for r in req.get('candidates',[])]==[(r.get('challenge_id'),r.get('field'),r.get('semantic_type')) for r in src.get('custom_data_candidate_reviews',[])]),
  ('all decisions pending',all(r.get('decision_status')=='PENDING_EXPLICIT_SEMANTIC_REVIEW' and r.get('semantic_decision') is None for r in req.get('candidates',[]))),
  ('all binding flags false',all(r.get('binding_authorized') is False and r.get('renderer_projection_approved') is False for r in req.get('candidates',[]))),
  ('all candidate values excluded',all(r.get('runtime_evidence',{}).get('raw_candidate_values_included') is False for r in req.get('candidates',[]))),
  ('runtime audit reference is hash-only',all(r.get('runtime_evidence',{}).get('candidate_audit_json_sha256')==AUDIT_SHA for r in req.get('candidates',[]))),
  ('candidate runtime selectors exist',[r.get('challenge_id') for r in req['candidates']]==[r.get('runtime_evidence',{}).get('audit_selector_id') for r in req['candidates']]),
  ('CHALLENGE_003 remains scalar',req['candidates'][0].get('field')=='target_x' and req['candidates'][0].get('semantic_type')=='float' and req['candidates'][0].get('coordinate_space')=='PILOT_0X100'),
  ('CHALLENGE_003 is not seed sensitivity oracle','NOT_A_SEED_SENSITIVITY_ORACLE' in req['candidates'][0].get('runtime_evidence',{}).get('gameplay_seed_candidate_relation','')),
  ('CHALLENGE_005 per-run constant', 'per simulation attempt' in req['candidates'][1].get('lifecycle','')),
  ('CHALLENGE_006 target separate from catcher', 'p_c' in req['candidates'][2].get('risk_and_boundary','') or 'catcher' in req['candidates'][2].get('review_question','').lower()),
  ('CHALLENGE_007 no distractor telemetry', 'distractor' in req['candidates'][3].get('risk_and_boundary','').lower()),
  ('CHALLENGE_008 timing remains blocked',req['candidates'][4].get('temporal_review_status')=='BLOCKED_TIMEBASE_CONFLICT_SOURCE_FRAME_ONLY'),
  ('CHALLENGE_009 timing remains blocked',req['candidates'][5].get('temporal_review_status')=='BLOCKED_TIMEBASE_CONFLICT_SOURCE_FRAME_ONLY'),
  ('CHALLENGE_009 does not use target_count','target_count' in req['candidates'][5].get('missing_value_behavior','')),
  ('all candidates require 8 review dimensions',all(len(r.get('required_review_dimensions',[]))==8 for r in req.get('candidates',[]))),
  ('next gate is semantic decision only',req.get('next_gate')=='OPERATOR_SEMANTIC_DECISION_RECORD_REQUIRED; NO_BINDING_APPROVAL; NO_PAYLOAD_CONSUMER'),
  ('global renderer lock',req.get('governance_locks',{}).get('renderer')=='OFF'),
  ('global candidate input inadmissible',req.get('governance_locks',{}).get('candidate_input_admissible') is False),
  ('global payload not materialized',req.get('governance_locks',{}).get('payload_materialized') is False),
  ('global no media',req.get('governance_locks',{}).get('media_created') is False),
  ('global release authority none',req.get('governance_locks',{}).get('release_authority')=='NONE'),
  ('global approved bindings zero',req.get('governance_locks',{}).get('approved_bindings')==0 and req.get('governance_locks',{}).get('approved_custom_data_bindings')==0),
  ('no binding approval in policy',req.get('decision_record_policy',{}).get('explicit_binding_approval')=='NOT_GRANTED_BY_THIS_REVIEW'),
  ('decision options include accept/reject/block',set(req.get('decision_record_policy',{}).get('allowed_semantic_decisions',[]))=={'ACCEPT_SEMANTIC_DEFINITION_FOR_FUTURE_BINDING_SPECIFICATION','REJECT_CANDIDATE_SEMANTIC_DEFINITION','BLOCKED_NEEDS_SOURCE_OR_POLICY_DECISION'}),
  ('all required sources still pinned',all((root/str(pin['path'])).is_file() and sha(root/str(pin['path']))==pin['sha256'] for pin in design['source_pins'])),
  ('all authority inputs still pinned',all((root/str(pin['path'])).is_file() and sha(root/str(pin['path']))==pin['sha256'] for pin in design['authority_input_pins'])),
  ('source review and contract pins stable',sha(source_path)==SOURCE_REVIEW_SHA and sha(request_path)==hashlib.sha256(request_path.read_bytes()).hexdigest()),
 ]:
  if not add(name, lambda condition=condition: bool(condition)): return 1
 # Explicit absence of any source raw candidate data or renderer-approval toggles being true.
 if not add('no raw values or positive approval flags in request', lambda: req.get('raw_candidate_values_included') is False and all(v.get('binding_authorized') is False and v.get('renderer_projection_approved') is False for v in req['candidates'])): return 1
 print(f"C11D_V2B_CANDIDATE_SEMANTIC_REVIEW_REQUEST_TESTS={len(checks)}/{len(checks)}")
 print("C11D_V2B_CANDIDATE_SEMANTIC_REVIEW_DECISIONS=PENDING")
 print("C11D_V2B_CANDIDATE_BINDINGS_APPROVED=0")
 print("C11D_V2B_CANDIDATE_RAW_VALUES_INCLUDED=false")
 return 0
if __name__=='__main__': raise SystemExit(main())
