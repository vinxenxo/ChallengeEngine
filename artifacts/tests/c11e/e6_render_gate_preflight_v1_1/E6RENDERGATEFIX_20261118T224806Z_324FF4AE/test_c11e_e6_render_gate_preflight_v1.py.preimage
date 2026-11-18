import importlib.util, json, tempfile, unittest, hashlib
from pathlib import Path
P=Path(__file__).resolve().parents[1]/'tools/c11d/d9/c11e_e6_render_gate_preflight_v1.py'
spec=importlib.util.spec_from_file_location('gate',P); gate=importlib.util.module_from_spec(spec); spec.loader.exec_module(gate)
class RenderGatePreflightTests(unittest.TestCase):
 def test_01_schema(self): self.assertEqual(gate.SCHEMA,'C11E-E6-RENDER-GATE-PREFLIGHT-RECEIPT-V1')
 def test_02_safe_relative_path(self):
  with tempfile.TemporaryDirectory() as d: self.assertEqual(gate.safe_rel(Path(d),'a').parent,Path(d).resolve())
 def test_03_reject_parent_traversal(self):
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaises(ValueError): gate.safe_rel(Path(d),'../outside')
 def test_04_reject_absolute_path(self):
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaises(ValueError): gate.safe_rel(Path(d),'/tmp/outside')
 def test_05_hash_function(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'x'; p.write_bytes(b'abc'); self.assertEqual(gate.sha(p),hashlib.sha256(b'abc').hexdigest())
 def test_06_scope_18(self):
  x=json.loads((Path(__file__).resolve().parents[1]/'definitions/c11e/test_only/C11E_E6_RENDER_GATE_PREFLIGHT_INPUTS_V1.json').read_text()); self.assertEqual(x['scope']['smoke18_top_level'],18)
 def test_07_scope_30(self):
  x=json.loads((Path(__file__).resolve().parents[1]/'definitions/c11e/test_only/C11E_E6_RENDER_GATE_PREFLIGHT_INPUTS_V1.json').read_text()); self.assertEqual(x['scope']['editorial_targets'],30)
 def test_08_challenge_18(self):
  x=json.loads((Path(__file__).resolve().parents[1]/'definitions/c11e/test_only/C11E_E6_RENDER_GATE_PREFLIGHT_INPUTS_V1.json').read_text()); self.assertEqual(x['scope']['challenge_editorial_targets'],18)
 def test_09_loop_6(self):
  x=json.loads((Path(__file__).resolve().parents[1]/'definitions/c11e/test_only/C11E_E6_RENDER_GATE_PREFLIGHT_INPUTS_V1.json').read_text()); self.assertEqual(x['scope']['loop_editorial_targets'],6)
 def test_10_drill_6(self):
  x=json.loads((Path(__file__).resolve().parents[1]/'definitions/c11e/test_only/C11E_E6_RENDER_GATE_PREFLIGHT_INPUTS_V1.json').read_text()); self.assertEqual(x['scope']['drill_editorial_targets'],6)
 def test_11_tools_do_not_authorize_execution(self):
  x=json.loads((Path(__file__).resolve().parents[1]/'definitions/c11e/test_only/C11E_E6_RENDER_GATE_PREFLIGHT_INPUTS_V1.json').read_text()); self.assertTrue(all(not t['execution_allowed'] for t in x['external_runtime_tools']))
 def test_12_governance_keeps_d48_blocked(self):
  x=json.loads((Path(__file__).resolve().parents[1]/'definitions/c11e/test_only/C11E_E6_RENDER_GATE_PREFLIGHT_INPUTS_V1.json').read_text()); self.assertEqual(x['governance']['d4_8'],'BLOCKED')
 def test_13_governance_keeps_renderer_off(self):
  x=json.loads((Path(__file__).resolve().parents[1]/'definitions/c11e/test_only/C11E_E6_RENDER_GATE_PREFLIGHT_INPUTS_V1.json').read_text()); self.assertEqual(x['governance']['renderer'],'OFF')
 def test_14_e6_not_authorized(self):
  x=json.loads((Path(__file__).resolve().parents[1]/'definitions/c11e/test_only/C11E_E6_RENDER_GATE_PREFLIGHT_INPUTS_V1.json').read_text()); self.assertFalse(x['governance']['e6_test_only_authorized'])
 def test_15_zero_acceptance(self):
  x=json.loads((Path(__file__).resolve().parents[1]/'definitions/c11e/test_only/C11E_E6_RENDER_GATE_PREFLIGHT_INPUTS_V1.json').read_text()); self.assertEqual(x['governance']['e6_accepted_scenarios'],0)
 def test_16_no_batch_id(self):
  x=json.loads((Path(__file__).resolve().parents[1]/'definitions/c11e/test_only/C11E_E6_RENDER_GATE_PREFLIGHT_INPUTS_V1.json').read_text()); self.assertFalse(x['governance']['batch_id_reserved'])
 def test_17_ch004_old_editorial_drift_unresolved(self):
  x=json.loads((Path(__file__).resolve().parents[1]/'definitions/c11e/test_only/C11E_E6_RENDER_GATE_PREFLIGHT_INPUTS_V1.json').read_text()); self.assertIn('UNRESOLVED',x['known_open_gates'][0]['status'])
 def test_18_loop_consumer_blocked(self):
  x=json.loads((Path(__file__).resolve().parents[1]/'definitions/c11e/test_only/C11E_E6_RENDER_GATE_PREFLIGHT_INPUTS_V1.json').read_text()); self.assertIn('NOT_IMPLEMENTED',x['known_open_gates'][2]['status'])
 def test_19_drill_readback_not_proven(self):
  x=json.loads((Path(__file__).resolve().parents[1]/'definitions/c11e/test_only/C11E_E6_RENDER_GATE_PREFLIGHT_INPUTS_V1.json').read_text()); self.assertEqual(x['known_open_gates'][3]['status'],'NOT_PROVEN')
 def test_20_global_baseline_held(self):
  x=json.loads((Path(__file__).resolve().parents[1]/'definitions/c11e/test_only/C11E_E6_RENDER_GATE_PREFLIGHT_INPUTS_V1.json').read_text()); self.assertIn('0_OF_10',x['known_open_gates'][6]['status'])
 def test_21_successor_policy_is_draft(self):
  x=json.loads((Path(__file__).resolve().parents[1]/'definitions/c11e/test_only/C11E_E6_SMOKE18_SUCCESSOR_POLICY_DRAFT_V2.json').read_text()); self.assertIn('NOT_APPROVED',x['status'])
 def test_22_policy_does_not_mutate_d48(self):
  x=json.loads((Path(__file__).resolve().parents[1]/'definitions/c11e/test_only/C11E_E6_SMOKE18_SUCCESSOR_POLICY_DRAFT_V2.json').read_text()); self.assertEqual(x['supersedes_for_scope_only']['original'],'IMMUTABLE_BLOCKED_UNCHANGED')
 def test_23_editorial_fixture_test_only(self):
  x=json.loads((Path(__file__).resolve().parents[1]/'definitions/c11e/test_only/C11E_E6_SMOKE18_SUCCESSOR_POLICY_DRAFT_V2.json').read_text()); self.assertIn('TEST_ONLY',x['approved_test_only_fixtures']['family_editorial']['status'])
 def test_24_music_keeps_e1_null(self):
  x=json.loads((Path(__file__).resolve().parents[1]/'definitions/c11e/test_only/C11E_E6_SMOKE18_SUCCESSOR_POLICY_DRAFT_V2.json').read_text()); self.assertEqual(x['approved_test_only_fixtures']['challenge_music']['e1_tempo_bpm'],'MUST_REMAIN_NULL')
 def test_25_release_none(self):
  x=json.loads((Path(__file__).resolve().parents[1]/'definitions/c11e/test_only/C11E_E6_RENDER_GATE_PREFLIGHT_INPUTS_V1.json').read_text()); self.assertEqual(x['governance']['release_authority'],'NONE')
 def test_26_git_skipped(self):
  x=json.loads((Path(__file__).resolve().parents[1]/'definitions/c11e/test_only/C11E_E6_RENDER_GATE_PREFLIGHT_INPUTS_V1.json').read_text()); self.assertEqual(x['governance']['git_checks'],'SKIPPED')
 def test_27_commits_operator_managed(self):
  x=json.loads((Path(__file__).resolve().parents[1]/'definitions/c11e/test_only/C11E_E6_RENDER_GATE_PREFLIGHT_INPUTS_V1.json').read_text()); self.assertEqual(x['governance']['commits'],'OPERATOR_MANAGED')
 def test_28_no_media_invocation_flags(self):
  x=json.loads((Path(__file__).resolve().parents[1]/'definitions/c11e/test_only/C11E_E6_RENDER_GATE_PREFLIGHT_INPUTS_V1.json').read_text()); self.assertFalse(any(x['execution_prohibition'].values()))
 def test_29_successor_gate_requires_operator_authorization(self):
  x=json.loads((Path(__file__).resolve().parents[1]/'definitions/c11e/test_only/C11E_E6_SMOKE18_SUCCESSOR_POLICY_DRAFT_V2.json').read_text()); self.assertIn('separate explicit operator E6 TEST_ONLY execution authorization',x['authorization_gates'])
 def test_30_receipt_pins_count(self):
  x=json.loads((Path(__file__).resolve().parents[1]/'definitions/c11e/test_only/C11E_E6_RENDER_GATE_PREFLIGHT_INPUTS_V1.json').read_text()); self.assertEqual(len(x['receipt_pins']),8)
 def test_31_source_pin_count(self):
  x=json.loads((Path(__file__).resolve().parents[1]/'definitions/c11e/test_only/C11E_E6_RENDER_GATE_PREFLIGHT_INPUTS_V1.json').read_text()); self.assertEqual(len(x['project_source_pins']),20)
 def test_32_tool_count(self):
  x=json.loads((Path(__file__).resolve().parents[1]/'definitions/c11e/test_only/C11E_E6_RENDER_GATE_PREFLIGHT_INPUTS_V1.json').read_text()); self.assertEqual(len(x['external_runtime_tools']),5)
 def test_33_preflight_does_not_run_commands(self):
  s=P.read_text(encoding='utf-8'); self.assertNotIn('subprocess.run(',s); self.assertNotIn('os.system(',s)
 def test_34_no_production_mutation_in_policy(self):
  x=json.loads((Path(__file__).resolve().parents[1]/'definitions/c11e/test_only/C11E_E6_SMOKE18_SUCCESSOR_POLICY_DRAFT_V2.json').read_text()); self.assertFalse(x['explicit_non_authorizations']['production_dispatch'])
 def test_35_tool_hashes_anchored(self):
  x=json.loads((Path(__file__).resolve().parents[1]/'definitions/c11e/test_only/C11E_E6_RENDER_GATE_PREFLIGHT_INPUTS_V1.json').read_text()); self.assertTrue(all(len(t['sha256'])==64 for t in x['external_runtime_tools']))
 def test_36_duplicate_receipt_ids_absent(self):
  x=json.loads((Path(__file__).resolve().parents[1]/'definitions/c11e/test_only/C11E_E6_RENDER_GATE_PREFLIGHT_INPUTS_V1.json').read_text()); ids=[r['id'] for r in x['receipt_pins']]; self.assertEqual(len(ids),len(set(ids)))
 def test_37_duplicate_source_paths_absent(self):
  x=json.loads((Path(__file__).resolve().parents[1]/'definitions/c11e/test_only/C11E_E6_RENDER_GATE_PREFLIGHT_INPUTS_V1.json').read_text()); paths=[r['path'] for r in x['project_source_pins']]; self.assertEqual(len(paths),len(set(paths)))
 def test_38_output_root_is_test_only(self):
  x=json.loads((Path(__file__).resolve().parents[1]/'definitions/c11e/test_only/C11E_E6_RENDER_GATE_PREFLIGHT_INPUTS_V1.json').read_text()); self.assertTrue(x['output_root_relative'].startswith('artifacts/tests/'))
class EvaluationTests(unittest.TestCase):
 def test_39_evaluate_emits_blockers_for_missing_inputs(self):
  with tempfile.TemporaryDirectory() as d:
   sample={'project_source_pins':[{'path':'nope','sha256':'0'*64}],'receipt_pins':[],'external_runtime_tools':[],'output_root_relative':'artifacts/tests/gate','known_open_gates':[],'governance':{},'execution_prohibition':{}}
   result=gate.evaluate(Path(d),sample,'TEST'); self.assertIn('SOURCE_PIN_MISSING:nope',result['blockers'])
 def test_40_evaluate_never_authorizes(self):
  with tempfile.TemporaryDirectory() as d:
   sample={'project_source_pins':[],'receipt_pins':[],'external_runtime_tools':[],'output_root_relative':'artifacts/tests/gate','known_open_gates':[],'governance':{'e6_test_only_authorized':False},'execution_prohibition':{'godot_invoked':False}}
   result=gate.evaluate(Path(d),sample,'TEST'); self.assertEqual(result['governance']['e6_test_only_authorized'],False)
if __name__=='__main__': unittest.main(verbosity=2)
