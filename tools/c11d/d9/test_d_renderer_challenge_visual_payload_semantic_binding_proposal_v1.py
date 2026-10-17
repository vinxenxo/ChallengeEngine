"""Fail-closed tests for the source-derived semantic-binding proposal."""
from __future__ import annotations
import copy, json, sys, unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE))
from d_renderer_challenge_visual_payload_semantic_binding_proposal_v1 import (
    CONTRACT_REL, SCHEMA_REL, REPORT_SCHEMA_REL, ProposalError, read_json, validate_proposal, validate_contract, dotted, validate_binding_approval, validate_custom_candidate
)

class ChallengeVisualSemanticBindingProposalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract=read_json(ROOT/CONTRACT_REL)
        cls.schema=read_json(ROOT/SCHEMA_REL)
        cls.report_schema=read_json(ROOT/REPORT_SCHEMA_REL)
        cls.report=validate_proposal(ROOT)

    def test_proposal_audit_summary(self):
        self.assertEqual(self.report['summary']['selectors'],'9/9')
        self.assertEqual(self.report['summary']['source_pins'],'43/43')
        self.assertEqual(self.report['summary']['secondary_binding_proposals'],'9/9')

    def test_27_asset_references_and_15_unique_assets(self):
        self.assertEqual(self.report['summary']['asset_reference_bindings'],'27/27')
        self.assertEqual(self.report['summary']['unique_assets'],'15/15')

    def test_base_track_has_exactly_six_v1_fields(self):
        for row in self.contract['selector_semantics']:
            self.assertEqual(row['base_track']['fields'],['position','rotation','scale','opacity','texture_index','variant_id'])

    def test_proposals_do_not_approve_bindings(self):
        self.assertEqual(self.report['summary']['approved_bindings'],0)
        for row in self.contract['selector_semantics']:
            binding=row['secondary_binding_proposal']
            self.assertEqual(binding['proposal_status'],'PROPOSAL_ONLY_NOT_APPROVED')
            self.assertFalse(binding['binding_authorized'])
            self.assertFalse(binding['renderer_projection_approved'])

    def test_exact_six_custom_data_candidates(self):
        rows={r['challenge_id']:r for r in self.contract['selector_semantics']}
        expected={'CHALLENGE_003':'target_x','CHALLENGE_005':'target_position','CHALLENGE_006':'target_position','CHALLENGE_007':'target_position','CHALLENGE_008':'active_selection','CHALLENGE_009':'displayed_count'}
        actual={cid:r['secondary_binding_proposal']['candidate_custom_data_field'] for cid,r in rows.items() if r['secondary_binding_proposal']['candidate_custom_data_field']}
        self.assertEqual(actual,expected)

    def test_static_targets_are_source_declared_not_telemetry(self):
        rows={r['challenge_id']:r for r in self.contract['selector_semantics']}
        expected={'CHALLENGE_001':'presentation.static_target_position','CHALLENGE_002':'difficulty.parking.target_position','CHALLENGE_004':'difficulty.parking.target_position'}
        for cid,pointer in expected.items():
            row=rows[cid]
            self.assertEqual(row['secondary_binding_proposal']['source_pointer'],pointer)
            self.assertIsNone(row['secondary_binding_proposal']['candidate_custom_data_field'])

    def test_pilot_target_x_remains_scalar(self):
        row=next(r for r in self.contract['selector_semantics'] if r['challenge_id']=='CHALLENGE_003')
        binding=row['secondary_binding_proposal']
        self.assertEqual(binding['semantic_type'],'float')
        self.assertEqual(row['coordinate_space'],'PILOT_0X100')
        self.assertEqual(binding['coordinate_policy'],'PILOT_0X100_SCALAR_ONLY_NO_2D_POSITION_CONVERSION')

    def test_hit_catch_find_use_separate_vector2_candidate(self):
        rows={r['challenge_id']:r for r in self.contract['selector_semantics']}
        for cid in ('CHALLENGE_005','CHALLENGE_006','CHALLENGE_007'):
            binding=rows[cid]['secondary_binding_proposal']
            self.assertEqual(binding['candidate_custom_data_field'],'target_position')
            self.assertEqual(binding['semantic_type'],'Vector2')
            self.assertEqual(binding['asset_role'],'TARGET')

    def test_choose_and_count_are_withheld_for_timebase(self):
        rows={r['challenge_id']:r for r in self.contract['selector_semantics']}
        self.assertEqual(rows['CHALLENGE_008']['secondary_binding_proposal']['candidate_custom_data_field'],'active_selection')
        self.assertEqual(rows['CHALLENGE_009']['secondary_binding_proposal']['candidate_custom_data_field'],'displayed_count')
        for cid in ('CHALLENGE_008','CHALLENGE_009'):
            self.assertEqual(rows[cid]['runtime_preview_target_scope'],'WITHHOLD_FOR_TIMEBASE_DECISION')

    def test_timebase_conflict_set_is_exact(self):
        conflicts={k:v for k,v in self.contract['temporal_review'].items() if k.startswith('CHALLENGE_')}
        self.assertEqual(set(conflicts),{'CHALLENGE_008','CHALLENGE_009'})
        for row in conflicts.values():
            self.assertEqual(row['declared_total_seconds'],11.0)
            self.assertEqual(row['component_sum_seconds'],12.0)
            self.assertEqual(row['status'],'UNRESOLVED_BLOCKED_FROM_RUNTIME_MATERIALIZATION')

    def test_telemetry_denylist_is_not_removed(self):
        expected={'success_distance','spatial_distance','velocity','angle_error','steering','braking','dodge_offset','save_offset','overshoot_dist','target_count','score','minimum_distance','winning_frame','close_calls'}
        self.assertTrue(expected.issubset(set(self.contract['never_bind_by_default'])))

    def test_whole_custom_data_map_is_forbidden(self):
        scope=self.contract['scope']
        self.assertIn('NEVER_SERIALIZE_WHOLE_MAP',scope['custom_data_policy'])
        self.assertEqual(scope['approved_custom_data_bindings'],0)

    def test_all_source_pointers_resolve_or_are_explicit_custom_data(self):
        for row in self.contract['selector_semantics']:
            binding=row['secondary_binding_proposal']
            if binding['candidate_custom_data_field']:
                self.assertEqual(binding['source_pointer'],'FrameSnapshot.custom_data.'+binding['candidate_custom_data_field'])
            else:
                challenge=read_json(ROOT/row['challenge_source_path'])
                value=dotted(challenge,binding['source_pointer'])
                self.assertEqual(len(value),2)

    def test_godot_and_payload_are_not_used_by_audit(self):
        self.assertEqual(self.report['summary']['godot_invocations'],0)
        self.assertFalse(self.report['summary']['payload_materialized'])
        self.assertFalse(self.contract['scope']['payload_files_written'])

    def test_governance_locks_remain_closed(self):
        locks=self.contract['governance_locks']
        self.assertEqual(locks['renderer'],'OFF')
        self.assertEqual(locks['d4_8'],'BLOCKED')
        self.assertEqual(locks['d9_10'],'PREPARE_ONLY')
        self.assertEqual(locks['d9_17'],'BLOCKED_NO_GO')
        self.assertEqual(locks['d10'],'BLOCKED_FOR_PROMOTION')
        self.assertEqual(locks['release_authority'],'NONE')

    def test_frozen_manifest_pin_is_correct(self):
        self.assertEqual(self.contract['source_authority']['frozen_c11c_manifest_sha256'],'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953')

    def test_negative_binding_self_approval_fails_closed(self):
        binding=copy.deepcopy(self.contract['selector_semantics'][2]['secondary_binding_proposal'])
        binding['binding_authorized']=True
        with self.assertRaises(ProposalError):
            validate_binding_approval('CHALLENGE_003',binding)

    def test_negative_arbitrary_custom_data_field_fails_closed(self):
        with self.assertRaises(ProposalError):
            validate_custom_candidate('CHALLENGE_001','velocity')
        with self.assertRaises(ProposalError):
            validate_custom_candidate('CHALLENGE_005','score')

    def test_schema_identity_is_strict(self):
        self.assertEqual(self.schema['$id'],'urn:c11d:challenge-visual-payload-semantic-binding-proposal:v1')
        self.assertFalse(self.schema['additionalProperties'])
        self.assertEqual(self.report_schema['$id'],'urn:c11d:challenge-visual-payload-semantic-binding-proposal-report:v1')
        self.assertFalse(self.report_schema['additionalProperties'])

    def test_json_schema_validation(self):
        try: import jsonschema
        except ImportError: self.skipTest('jsonschema optional')
        jsonschema.Draft202012Validator.check_schema(self.schema)
        jsonschema.Draft202012Validator(self.schema).validate(self.contract)
        jsonschema.Draft202012Validator.check_schema(self.report_schema)
        jsonschema.Draft202012Validator(self.report_schema).validate(self.report)

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(ChallengeVisualSemanticBindingProposalTests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful():
        s=validate_proposal(ROOT)['summary']
        print('C11-D CHALLENGE VISUAL PAYLOAD SEMANTIC BINDING PROPOSAL V1 TEST PASS | selectors=9/9 | source_pins=43/43 | unit_tests=20/20 | approved_bindings=0 | godot_invocations=0 | payload_materialized=false | renderer=OFF | release_authority=NONE')
        raise SystemExit(0)
    raise SystemExit(1)
