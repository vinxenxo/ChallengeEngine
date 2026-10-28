from __future__ import annotations
import ast, hashlib, importlib.util, json, re, sys, unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
MODULE_PATH=HERE/'audit_d_renderer_phase_p_source_value_frame_value_provenance_20261028.py'
HARNESS_PATH=HERE/'phase_p_source_value_frame_value_provenance_in_memory.gd'
CONTRACT_PATH=HERE.parent.parent.parent/'definitions'/'c11d'/'production'/'D_RENDERER_PHASE_P_SOURCE_VALUE_VS_FRAME_VALUE_PROVENANCE_CONTRACT_V1.json'
SCHEMA_PATH=HERE.parent.parent.parent/'definitions'/'c11d'/'production'/'D_RENDERER_PHASE_P_SOURCE_VALUE_VS_FRAME_VALUE_PROVENANCE_CONTRACT_SCHEMA_V1.json'
spec=importlib.util.spec_from_file_location('phase_p_audit',MODULE_PATH); mod=importlib.util.module_from_spec(spec); assert spec and spec.loader; sys.modules[spec.name]=mod; spec.loader.exec_module(mod)

class PhasePProvenanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract=json.loads(CONTRACT_PATH.read_text(encoding='utf-8'))
        cls.schema=json.loads(SCHEMA_PATH.read_text(encoding='utf-8'))
        cls.harness=HARNESS_PATH.read_text(encoding='utf-8')
        cls.runner=MODULE_PATH.read_text(encoding='utf-8')
    def test_contract_identity_and_selector_count(self):
        mod.validate_contract(self.contract,self.schema); self.assertEqual(self.contract['expected_selector_count'],6)
    def test_exact_six_selector_order(self):
        self.assertEqual([x['challenge_id'] for x in self.contract['selectors']],mod.EXPECTED_IDS)
    def test_candidate_field_allowlist(self):
        self.assertEqual({x['challenge_id']:x['candidate_field'] for x in self.contract['selectors']},mod.EXPECTED_FIELDS)
    def test_expected_type_inventory(self):
        self.assertEqual({x['challenge_id']:x['expected_frame_value_type'] for x in self.contract['selectors']},mod.EXPECTED_TYPES)
    def test_expected_relation_inventory(self):
        self.assertEqual(len({x['relation_policy'] for x in self.contract['selectors']}),6)
    def test_every_source_input_path_nonempty(self):
        self.assertTrue(all(x['source_input_paths'] for x in self.contract['selectors']))
    def test_phase_p_contract_source_pin_denominator(self):
        self.assertEqual(self.contract['source_pin_count'],len(self.contract['source_pins']))
    def test_phase_p_schema_strict_root(self):
        self.assertFalse(self.schema['additionalProperties'])
    def test_frozen_manifest_hash_and_size_are_canonical(self):
        self.assertEqual(self.contract['frozen_c11c']['manifest_sha256'],mod.FROZEN_SHA); self.assertEqual(self.contract['frozen_c11c']['manifest_bytes'],mod.FROZEN_BYTES)
    def test_governance_locks_hold(self):
        self.assertEqual(self.contract['governance_locks']['renderer'],'OFF'); self.assertFalse(self.contract['governance_locks']['media_created']); self.assertFalse(self.contract['governance_locks']['payload_materialized']); self.assertEqual(self.contract['governance_locks']['release_authority'],'NONE')
    def test_no_candidate_approvals(self):
        p=self.contract['semantic_binding_policy']; self.assertEqual(p['approved_bindings'],0); self.assertEqual(p['approved_custom_data_bindings'],0); self.assertEqual(p['approved_renderer_projection_bindings'],0)
    def test_timebase_conflicts_only_on_008_009(self):
        self.assertEqual({s['challenge_id'] for s in self.contract['selectors'] if s['timebase_issue_preserved']},{'CHALLENGE_008','CHALLENGE_009'})
    def test_pilot_target_x_keeps_float_scalar(self):
        s=next(x for x in self.contract['selectors'] if x['challenge_id']=='CHALLENGE_003'); self.assertEqual(s['expected_frame_value_type'],'float'); self.assertEqual(s['relation_policy'],'PILOT_TARGET_X_SOURCE_FORMULA')
    def test_hit_is_per_run_constant_policy(self):
        s=next(x for x in self.contract['selectors'] if x['challenge_id']=='CHALLENGE_005'); self.assertEqual(s['relation_policy'],'HIT_TARGET_CONSTANT_AFTER_SEEDED_OFFSET')
    def test_catch_and_find_are_track_only_not_formula_equality(self):
        d={s['challenge_id']:s['relation_policy'] for s in self.contract['selectors']}; self.assertEqual(d['CHALLENGE_006'],'CATCH_TARGET_TRACK_PINNED_MECHANIC'); self.assertEqual(d['CHALLENGE_007'],'FIND_TARGET_TRACK_PINNED_MECHANIC')
    def test_choose_count_relation_checks(self):
        d={s['challenge_id']:s['relation_policy'] for s in self.contract['selectors']}; self.assertEqual(d['CHALLENGE_008'],'CHOOSE_SELECTION_SOURCE_SCHEDULE'); self.assertEqual(d['CHALLENGE_009'],'COUNT_DISPLAY_SOURCE_SCHEDULE')
    def test_harness_emits_hashes_not_values(self):
        self.assertIn('frame_value_series_sha256',self.harness); self.assertIn('source_input_value_sha256',self.harness); self.assertNotIn('JSON.stringify(frame.custom_data)',self.harness); self.assertNotIn('JSON.stringify(value)',self.harness)
    def test_harness_reads_only_allowlisted_key(self):
        self.assertIn('frame.custom_data.has(field)',self.harness); self.assertIn('frame.custom_data[field]',self.harness); self.assertNotIn('frame.custom_data.keys()',self.harness); self.assertNotIn('for key in frame.custom_data',self.harness)
    def test_harness_checks_bounded_values_not_dictionary_copy(self):
        self.assertIn('actual_candidate_values_serialized',self.harness); self.assertIn('whole_custom_data_map_serialized',self.harness); self.assertIn('approved_custom_data_bindings',self.harness)
    def test_harness_preserves_timebase_receipt(self):
        self.assertIn('known_conflict',self.harness); self.assertIn('phase_timeline_acceptance',self.harness)
    def test_harness_does_not_create_renderer_or_media(self):
        forbidden=['RenderingServer.','ViewportTexture','SubViewport','PackedScene','ResourceSaver.save','FileAccess.open(']
        for term in forbidden: self.assertNotIn(term,self.harness)
    def test_runner_requires_python_313(self): self.assertIn('Python 3.13 required',self.runner)
    def test_runner_requires_two_processes_per_selector(self): self.assertIn('for n in (1,2)',self.runner); self.assertIn('runtime_calls!=12',self.runner)
    def test_runner_rejects_pins_before_and_after(self): self.assertIn('PHASE_P_SOURCE_PIN_RECONCILIATION_FAILED',self.runner); self.assertIn('FINAL_PHASE_P_SOURCE_PIN_RECONCILIATION_FAILED',self.runner)
    def test_runner_checks_canonical_planner(self): self.assertIn('base.make_planner(root,base_s)',self.runner); self.assertIn('CANONICAL_PLANNER_BLOCKED',self.runner)
    def test_runner_stops_without_success_on_first_failure(self): self.assertIn('raise AuditError(f"{cid} {run_id} failed closed',self.runner); self.assertNotIn('unconditional_success',self.runner)
    def test_runner_checks_independent_repeat_hashes(self): self.assertIn('INDEPENDENT_PROCESS_PROVENANCE_HASH_MISMATCH',self.runner)
    def test_runner_never_reports_binding_approval(self): self.assertIn("'approved_custom_data_bindings':0",self.runner); self.assertIn("'renderer':'OFF'",self.runner)
    def test_phase_p_doc_is_explicitly_prepared_not_accepted(self):
        p=(HERE.parent.parent.parent/'docs/current/d/C11D_PHASE_P_SOURCE_VALUE_VS_FRAME_VALUE_PROVENANCE_IMPLEMENTATION_CHECKPOINT_20261028_V1.md').read_text(encoding='utf-8'); self.assertIn('PREPARED_NOT_WINDOWS_ACCEPTED',p)
    def test_static_ast_is_valid_python(self): ast.parse(self.runner); ast.parse(MODULE_PATH.read_text(encoding='utf-8'))

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(PhasePProvenanceTests); result=unittest.TextTestRunner(stream=sys.stdout,verbosity=2).run(suite); passed=result.testsRun-len(result.failures)-len(result.errors); print(f'PHASE_P_IMPLEMENTATION_STATIC_TESTS={passed}/{result.testsRun}'); raise SystemExit(0 if result.wasSuccessful() else 1)
