import hashlib, importlib.util, json, sys, tempfile, unittest, shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
RUNNER=ROOT/'tools/c11d/d9/d_renderer_visual_loop_timing_review_inheritance_audit.py'
spec=importlib.util.spec_from_file_location('timing_review_inheritance_audit',RUNNER)
audit=importlib.util.module_from_spec(spec); sys.modules[spec.name]=audit; spec.loader.exec_module(audit)
CONTRACT='definitions/c11d/production/D_RENDERER_VISUAL_LOOP_TIMING_REVIEW_INHERITANCE_V1.json'
SCHEMA='definitions/c11d/production/D_RENDERER_VISUAL_LOOP_TIMING_REVIEW_INHERITANCE_SCHEMA_V1.json'
class TimingReviewInheritanceAuditTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.contract=json.loads((ROOT/CONTRACT).read_text(encoding='utf-8'))
  cls.schema=json.loads((ROOT/SCHEMA).read_text(encoding='utf-8'))
 def test_contract_and_schema_are_strict_and_versioned(self):
  self.assertEqual(self.contract['schema_version'],'1.0')
  self.assertEqual(self.contract['status'],'PREPARATION_ONLY_SHARED_POLICY_INHERITANCE_PROPOSAL_NOT_APPROVAL_NOT_BINDING')
  self.assertFalse(self.contract['approval_state']['timing_review_inheritance_approved'])
  self.assertFalse(self.contract['authority']['renderer_admission_granted'])
  self.assertFalse(self.schema['additionalProperties'])
 def test_source_pins_are_exactly_seventeen_and_hash_shaped(self):
  pins=self.contract['source_lineage']; self.assertEqual(len(pins),17)
  self.assertEqual(len({x['path'] for x in pins}),17)
  for pin in pins: self.assertRegex(pin['sha256'],r'^[a-f0-9]{64}$')
 def test_exact_five_grammars_and_indices_are_pinned(self):
  rows=self.contract['scope']['selector_rows']
  self.assertEqual([r['grammar_id'] for r in rows],audit.EXPECTED_GRAMMARS)
  self.assertEqual([r['grammar_index'] for r in rows],list(range(5)))
 def test_each_selector_inherits_the_same_nine_shared_refs(self):
  expected=audit.EXPECTED_POLICY_IDS
  self.assertEqual(len(self.contract['shared_policy_refs']),9)
  for row in self.contract['scope']['selector_rows']: self.assertEqual(row['policy_refs'],expected)
 def test_no_implicit_family_exceptions(self):
  self.assertEqual(self.contract['scope']['family_exceptions'],[])
  for row in self.contract['scope']['selector_rows']: self.assertEqual(row['family_exception'],'NONE_DECLARED')
 def test_every_policy_ref_has_a_direct_source_pin(self):
  pins={x['path']:x['sha256'] for x in self.contract['source_lineage']}
  for ref in self.contract['shared_policy_refs']: self.assertEqual(pins[ref['path']],ref['sha256'])
 def test_all_policy_references_remain_unapproved(self):
  self.assertEqual(len(self.contract['shared_policy_refs']),9)
  for ref in self.contract['shared_policy_refs']:
   self.assertTrue(ref['approval_assertions'])
   self.assertTrue(all(v is False for v in ref['approval_assertions'].values()))
 def test_editorial_and_timebase_policies_are_proposals_only(self):
  refs={x['id']:x for x in self.contract['shared_policy_refs']}
  self.assertEqual(refs['LOOP_DRILL_EDITORIAL_FIELD_WINDOW_V1']['expected_status'],'PROPOSAL_ONLY_NOT_RENDERER_INPUT')
  self.assertEqual(refs['UNIFIED_DELIVERY_TIMEBASE_V1']['expected_status'],'PROPOSAL_ONLY_NOT_RENDERER_INPUT')
 def test_audio_policy_does_not_authorize_music_or_mix(self):
  refs={x['id']:x for x in self.contract['shared_policy_refs']}
  r=refs['UNIFIED_AUDIO_MUSIC_DELIVERY_V1']
  self.assertFalse(r['approval_assertions']['approval_state.music_selection_policy_approved'])
  self.assertIn('no music selection',r['purpose'].lower())
 def test_v1_binding_stays_one_accepted_and_four_blocked(self):
  b=self.contract['binding_boundary']
  self.assertEqual(b['currently_bound_grammars'],['harmonic_membrane'])
  self.assertEqual(b['currently_blocked_grammars'],audit.EXPECTED_GRAMMARS[1:])
  self.assertFalse(b['candidate_input_admissible'])
 def test_no_render_or_c11c_mutation(self):
  e=self.contract['execution_boundary']
  for key in ['godot_invoked','request_persisted','payload_materialized','renderer_native_input_emitted','renderer_dispatch_invoked','media_created','c11c_source_mutation']:
   self.assertFalse(e[key],key)
  self.assertEqual(e['renderer'],'OFF')
 def test_stale_source_pin_fails_closed(self):
  with tempfile.TemporaryDirectory() as td:
   target=Path(td)
   # copy only pinned files needed for audit; use full current tree via symlinks where available
   shutil.copytree(ROOT,target/'repo',dirs_exist_ok=True)
   root=target/'repo'
   pin=self.contract['source_lineage'][1]
   (root/pin['path']).write_text('{}',encoding='utf-8')
   with self.assertRaisesRegex(audit.AuditError,'Pinned source drift'):
    audit.audit(root)
 def test_audit_pass_preserves_gaps_and_governance_locks(self):
  summary=audit.audit(ROOT)
  self.assertEqual(summary['selectors'],5)
  self.assertEqual(summary['shared_policy_refs'],9)
  self.assertEqual(summary['source_pins'],17)
  self.assertEqual(summary['approvals_granted'],0)
  self.assertEqual(summary['canonical_bound'],1)
  self.assertEqual(summary['blocked_by_fixed_v1_scope'],4)
  self.assertFalse(summary['candidate_input_admissible'])
if __name__=='__main__': unittest.main(verbosity=2)
