from __future__ import annotations
import copy, json, sys, unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE))
from d_renderer_challenge_visual_payload_capability_matrix_v1 import (  # noqa: E402
    CONTRACT_REL,SCHEMA_REL,REPORT_SCHEMA_REL,CapabilityMatrixError,read_json,
    validate_source_pins,validate_inventory,build_report,registry_routes,custom_data_keys,
)

class ChallengeVisualPayloadCapabilityMatrixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract=read_json(ROOT/CONTRACT_REL)

    def test_contract_and_schemas_are_versioned_strict(self):
        self.assertEqual(self.contract['status'],'PREPARATION_ONLY_STATIC_CAPABILITY_INVENTORY_NOT_PAYLOAD_MATERIALIZATION')
        self.assertFalse(read_json(ROOT/SCHEMA_REL).get('additionalProperties',True))
        self.assertFalse(read_json(ROOT/REPORT_SCHEMA_REL).get('additionalProperties',True))

    def test_all_pinned_source_and_asset_hashes(self):
        result=validate_source_pins(ROOT)
        self.assertEqual(result['source_pins'],43)
        self.assertEqual(result['challenge_source_pins'],9)
        self.assertEqual(result['runtime_contract_pins'],4)
        self.assertEqual(result['unique_asset_pins'],15)

    def test_nine_selectors_in_canonical_order(self):
        report=validate_inventory(ROOT,self.contract)
        self.assertEqual([x['challenge_id'] for x in report['selectors']],[f'CHALLENGE_{i:03}' for i in range(1,10)])

    def test_registry_routes_all_nine_mechanics(self):
        report=validate_inventory(ROOT,self.contract)
        self.assertEqual(len({x['mechanic'] for x in report['selectors']}),9)
        self.assertEqual(len({x['mechanic_class'] for x in report['selectors']}),9)

    def test_all_27_asset_role_references_are_resolved_and_pinned(self):
        result=validate_inventory(ROOT,self.contract)
        self.assertEqual(result['asset_reference_count'],27)
        self.assertEqual(len(result['unique_assets']),15)

    def test_custom_data_is_inventory_only_for_each_mechanic(self):
        result=validate_inventory(ROOT,self.contract)
        self.assertEqual(result['custom_data_inventory_verified'],9)
        semantics=self.contract['custom_data_semantics']
        self.assertEqual(semantics['status'],'UNMAPPED_REQUIRES_SELECTOR_SPECIFIC_SEMANTIC_REVIEW')
        self.assertIn('target_position',semantics['known_visual_projection_candidates'])
        self.assertEqual({x['visual_projection_approval'] for x in result['selectors']},{'NONE'})

    def test_only_challenge_004_has_preexisting_runtime_preview(self):
        result=validate_inventory(ROOT,self.contract)
        self.assertEqual(result['preview_ids'],['CHALLENGE_004'])
        self.assertEqual(sum(bool(x['existing_challenge_visual_payload_preview_harness']) for x in result['selectors']),1)

    def test_explicit_total_duration_conflicts_remain_visible(self):
        result=validate_inventory(ROOT,self.contract)
        self.assertEqual(result['temporal_conflicts'],['CHALLENGE_008','CHALLENGE_009'])
        for row in result['selectors']:
            if row['challenge_id'] in ('CHALLENGE_008','CHALLENGE_009'):
                self.assertEqual(row['component_duration_sum_seconds'],12.0)
                self.assertEqual(row['declared_total_duration_seconds'],11.0)
                self.assertEqual(row['temporal_status'],'DECLARED_TOTAL_CONFLICTS_WITH_PHASE_SUM')

    def test_report_governance_stays_blocked_and_plan_only(self):
        report=build_report(ROOT)
        self.assertEqual(report['summary']['godot_invocations'],0)
        self.assertFalse(report['summary']['payload_materialized'])
        self.assertFalse(report['summary']['candidate_input_admissible'])
        self.assertFalse(report['summary']['seed_domains_complete_for_candidate_input'])
        self.assertEqual(report['summary']['renderer'],'OFF')
        self.assertEqual(report['summary']['release_authority'],'NONE')
        self.assertFalse(report['governance']['media_output_created'])

    def test_negative_missing_source_pin_fails_closed(self):
        bad=copy.deepcopy(self.contract)
        bad['pinned_sources'][0]['sha256']='0'*64
        with self.assertRaises(CapabilityMatrixError): validate_source_pins(ROOT,bad)

    def test_negative_unsupported_selector_fails_closed(self):
        bad=copy.deepcopy(self.contract)
        bad['selector_matrix'][4]['mechanic']='unknown_mechanic'
        with self.assertRaises(CapabilityMatrixError): validate_inventory(ROOT,bad)

    def test_negative_visual_projection_promotion_fails_closed(self):
        bad=copy.deepcopy(self.contract)
        bad['selector_matrix'][0]['visual_projection_approval']='APPROVED'
        with self.assertRaises(CapabilityMatrixError): validate_inventory(ROOT,bad)

    def test_negative_preview_coverage_escalation_fails_closed(self):
        bad=copy.deepcopy(self.contract)
        bad['selector_matrix'][0]['existing_challenge_visual_payload_preview_harness']=True
        with self.assertRaises(CapabilityMatrixError): validate_inventory(ROOT,bad)

    def test_negative_governance_unlock_fails_closed(self):
        bad=copy.deepcopy(self.contract)
        bad['governance_locks']['renderer']='ON'
        with self.assertRaises(CapabilityMatrixError): validate_inventory(ROOT,bad)

    def test_json_schemas_validate_contract_and_report(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest('jsonschema is an optional development dependency')
        contract_schema=read_json(ROOT/SCHEMA_REL)
        report_schema=read_json(ROOT/REPORT_SCHEMA_REL)
        jsonschema.Draft202012Validator.check_schema(contract_schema)
        jsonschema.Draft202012Validator(contract_schema).validate(self.contract)
        jsonschema.Draft202012Validator.check_schema(report_schema)
        jsonschema.Draft202012Validator(report_schema).validate(build_report(ROOT))

if __name__=='__main__': unittest.main(verbosity=2)
