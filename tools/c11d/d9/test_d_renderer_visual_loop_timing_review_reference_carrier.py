import hashlib, importlib.util, json, shutil, sys, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
RUNNER=ROOT/'tools/c11d/d9/d_renderer_visual_loop_timing_review_reference_carrier.py'
spec=importlib.util.spec_from_file_location('timing_review_reference_carrier',RUNNER)
carrier=importlib.util.module_from_spec(spec); sys.modules[spec.name]=carrier; spec.loader.exec_module(carrier)
CONTRACT='definitions/c11d/production/D_RENDERER_VISUAL_LOOP_TIMING_REVIEW_REFERENCE_CARRIER_CANDIDATE_V1.json'
SCHEMA='definitions/c11d/production/D_RENDERER_VISUAL_LOOP_TIMING_REVIEW_REFERENCE_CARRIER_CANDIDATE_SCHEMA_V1.json'
REPORT_SCHEMA='definitions/c11d/production/D_RENDERER_VISUAL_LOOP_TIMING_REVIEW_REFERENCE_CARRIER_REPORT_SCHEMA_V1.json'
class VisualLoopTimingReviewReferenceCarrierTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.contract=json.loads((ROOT/CONTRACT).read_text(encoding='utf-8'))
  cls.parent=json.loads((ROOT/cls.contract['parents']['timing_review_inheritance_contract_path']).read_text(encoding='utf-8'))
  cls.schema=json.loads((ROOT/SCHEMA).read_text(encoding='utf-8'))
  cls.report_schema=json.loads((ROOT/REPORT_SCHEMA).read_text(encoding='utf-8'))
 def test_contract_schema_is_draft_2020_12_strict_and_valid(self):
  from jsonschema import Draft202012Validator
  Draft202012Validator.check_schema(self.schema)
  self.assertEqual(list(Draft202012Validator(self.schema).iter_errors(self.contract)),[])
  self.assertFalse(self.schema['additionalProperties'])
 def test_contract_has_exact_direct_source_pins(self):
  self.assertEqual(len(self.contract['source_lineage']),16)
  self.assertEqual(len({r['path'] for r in self.contract['source_lineage']}),16)
  self.assertEqual(self.contract['source_lineage'][0]['path'],'release/C11C_FREEZE_PACKAGE_MANIFEST.json')
 def test_exact_five_selector_identity_order(self):
  self.assertEqual(self.contract['scope']['selector_ids'],carrier.EXPECTED_GRAMMARS)
  self.assertEqual([r['grammar_id'] for r in self.contract['scope']['selector_rows']],carrier.EXPECTED_GRAMMARS)
  self.assertEqual([r['grammar_index'] for r in self.contract['scope']['selector_rows']],list(range(5)))
 def test_every_selector_has_same_nine_reference_ids(self):
  refs=self.parent['shared_policy_refs']; expected=carrier.EXPECTED_POLICY_IDS
  self.assertEqual([r['id'] for r in refs],expected)
  for row in self.contract['scope']['selector_rows']:
   env=carrier.build_envelope(row,refs)
   self.assertEqual([r['id'] for r in env['policy_references']],expected)
 def test_reference_envelopes_are_metadata_not_policy_values(self):
  env=carrier.build_envelope(self.contract['scope']['selector_rows'][0],self.parent['shared_policy_refs'])
  for key in ('policy_source_bodies_copied','policy_values_copied','renderer_instructions_emitted','canonical_request_modified','canonical_payload_modified','request_bound','payload_materialized','renderer_native_input_emitted','canonical_binding_admitted'):
   self.assertIs(env[key],False)
  self.assertNotIn('policy_body',env); self.assertNotIn('instructions',env)
  self.assertTrue(all(r['reference_role']=='PROVENANCE_ONLY_NOT_INSTRUCTIONS' for r in env['policy_references']))
 def test_reference_bundle_digest_is_repeatable(self):
  row=self.contract['scope']['selector_rows'][0]; refs=self.parent['shared_policy_refs']
  self.assertEqual(carrier.build_envelope(row,refs),carrier.build_envelope(row,refs))
 def test_shared_reference_digest_is_identical_across_selectors(self):
  envelopes=[carrier.build_envelope(row,self.parent['shared_policy_refs']) for row in self.contract['scope']['selector_rows']]
  self.assertEqual(len({e['shared_reference_set_sha256'] for e in envelopes}),1)
 def test_selector_digest_binds_full_selector_identity_and_is_unique(self):
  envelopes=[carrier.build_envelope(row,self.parent['shared_policy_refs']) for row in self.contract['scope']['selector_rows']]
  self.assertEqual(len({e['selector_envelope_sha256'] for e in envelopes}),5)
  changed=dict(self.contract['scope']['selector_rows'][0]); changed['shader_branch']='altered_branch'
  self.assertNotEqual(carrier.build_envelope(changed,self.parent['shared_policy_refs'])['selector_envelope_sha256'],envelopes[0]['selector_envelope_sha256'])
 def test_unknown_selector_fails_closed(self):
  row=dict(self.contract['scope']['selector_rows'][0]); row['grammar_id']='longform'
  with self.assertRaises(carrier.ReferenceCarrierError): carrier.build_envelope(row,self.parent['shared_policy_refs'])
 def test_selector_index_mismatch_fails_closed(self):
  row=dict(self.contract['scope']['selector_rows'][2]); row['grammar_index']=0
  with self.assertRaises(carrier.ReferenceCarrierError): carrier.build_envelope(row,self.parent['shared_policy_refs'])
 def test_missing_duplicate_or_reordered_policy_refs_fail_closed(self):
  refs=self.parent['shared_policy_refs']; row=self.contract['scope']['selector_rows'][0]
  with self.assertRaises(carrier.ReferenceCarrierError): carrier.build_envelope(row,refs[:-1])
  duplicate=list(refs); duplicate[1]=dict(duplicate[0])
  with self.assertRaises(carrier.ReferenceCarrierError): carrier.build_envelope(row,duplicate)
  reordered=list(refs); reordered[0],reordered[1]=reordered[1],reordered[0]
  with self.assertRaises(carrier.ReferenceCarrierError): carrier.build_envelope(row,reordered)
 def test_any_policy_approval_assertion_true_is_rejected(self):
  refs=json.loads(json.dumps(self.parent['shared_policy_refs']))
  refs[0]['approval_assertions'][next(iter(refs[0]['approval_assertions']))]=True
  with self.assertRaises(carrier.ReferenceCarrierError): carrier.build_envelope(self.contract['scope']['selector_rows'][0],refs)
 def test_v1_binding_boundary_stays_one_of_five(self):
  rows=self.contract['scope']['selector_rows']
  self.assertEqual(sum(r['current_canonical_binding_status']=='SOURCE_BINDING_REVIEW_ONLY' for r in rows),1)
  self.assertEqual(sum(r['current_canonical_binding_status']=='BLOCKED_BY_FIXED_V1_TIMING_REVIEW_SCOPE' for r in rows),4)
  self.assertTrue(all(not r['canonical_binding_admitted'] for r in rows))
 def test_no_policy_or_renderer_approvals_or_actions_are_granted(self):
  a=self.contract['authority']; b=self.contract['admission_boundary']; x=self.contract['execution_boundary']
  self.assertFalse(a['canonical_binder_v1_mutated']); self.assertFalse(a['canonical_binding_v2_activated'])
  self.assertFalse(a['policy_approval_granted']); self.assertFalse(a['renderer_admission_granted'])
  self.assertFalse(b['current_candidate_input_admissible']); self.assertFalse(b['current_D4_8_authorized'])
  self.assertTrue(all(v is False for k,v in x.items() if k not in ('renderer','D4.8','release_authority')))
  self.assertEqual(x['renderer'],'OFF'); self.assertEqual(x['D4.8'],'BLOCKED'); self.assertEqual(x['release_authority'],'NONE')
 def test_report_schema_strict(self):
  from jsonschema import Draft202012Validator
  Draft202012Validator.check_schema(self.report_schema)
  self.assertFalse(self.report_schema['additionalProperties'])
 def test_direct_source_drift_fails_closed(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td)
   for item in self.contract['source_lineage']:
    src=ROOT/item['path']; dst=root/item['path']; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst)
   mutated=dict(self.contract); mutated['source_lineage']=[dict(x) for x in mutated['source_lineage']]
   p=mutated['source_lineage'][1]['path']; (root/p).write_bytes((root/p).read_bytes()+b'x')
   with self.assertRaises(carrier.ReferenceCarrierError): carrier.verify_direct_pins(root,mutated)
 def test_full_audit_prepares_five_envelopes_but_admits_none(self):
  report=carrier.audit(ROOT)
  self.assertEqual(len(report['envelopes']),5)
  self.assertEqual(report['summary']['reference_descriptors'],45)
  self.assertEqual(report['summary']['direct_source_pins'],'16/16')
  self.assertFalse(report['summary']['candidate_input_admissible'])
  self.assertEqual(report['summary']['approvals_granted'],0)
  self.assertEqual(len({e['selector_envelope_sha256'] for e in report['envelopes']}),5)
 def test_report_self_hash_and_governance_locks(self):
  report=carrier.audit(ROOT)
  expected=carrier.digest({k:v for k,v in report.items() if k!='report_sha256'})
  self.assertEqual(report['report_sha256'],expected)
  self.assertFalse(report['governance']['media_created']); self.assertEqual(report['governance']['renderer'],'OFF')
  self.assertEqual(report['governance']['D4.8'],'BLOCKED'); self.assertEqual(report['governance']['D9.17'],'BLOCKED_NO_GO')
if __name__=='__main__': unittest.main(verbosity=2)
