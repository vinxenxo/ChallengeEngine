from __future__ import annotations
import copy
import json
import unittest
from pathlib import Path

from d_renderer_editorial_field_routing_visibility_reconciliation import (
    CONTRACT_REL, SCHEMA_REL, EditorialRoutingReconciliationError,
    _read_json, _root, build_reconciliation, validate_reconciliation, _sha_json,
)

ROOT = Path(__file__).resolve().parents[3]

class EditorialFieldRoutingVisibilityReconciliationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = ROOT
        cls.contract = _read_json(ROOT, CONTRACT_REL)
        cls.schema = _read_json(ROOT, SCHEMA_REL)
        cls.report = build_reconciliation(ROOT)

    def test_exact_fourteen_field_instances_and_content_scope(self):
        routes = self.contract['field_routes']
        self.assertEqual(len(routes), 14)
        self.assertEqual(len(self.contract['source_lineage']), 27)
        self.assertEqual(self.report['summary']['content_types_reviewed'], 3)
        self.assertEqual(self.report['summary']['field_instances_reviewed'], 14)
        counts = {ct: sum(r['content_type'] == ct for r in routes) for ct in ('challenges','visual_loops','visual_drills')}
        self.assertEqual(counts, {'challenges': 6, 'visual_loops': 4, 'visual_drills': 4})

    def test_mapping_agrees_across_composition_frame_program_and_semantic_region(self):
        self.assertEqual(self.report['summary']['canonical_review_chain_parity'], 'PASS_14_OF_14')
        for row in self.contract['field_routes']:
            if row['field_kind'] == 'METADATA':
                self.assertIsNone(row['semantic_region_id'])
                continue
            self.assertIn(row['semantic_region_id'], {'HEADER','FOOTER','CHALLENGE_OVERLAY'})
            self.assertEqual(row['region_mapping_state'], 'PROPOSED_NOT_APPROVED')

    def test_loop_and_drill_windows_are_rules_not_evaluated_intervals(self):
        routes = [r for r in self.contract['field_routes'] if r['content_type'] in ('visual_loops','visual_drills') and r['field_kind']=='VISUAL_TEXT']
        self.assertEqual(len(routes), 6)
        self.assertTrue(all(r['visibility_policy_id']=='C11D_LOOP_DRILL_NONEMPTY_VISUAL_FIELDS_FULL_CONTINUOUS_SPAN_V1' for r in routes))
        self.assertTrue(all(r['visibility_rule']=='FULL_CONTINUOUS_PAYLOAD_SPAN_IF_NONEMPTY' for r in routes))
        self.assertTrue(all(r['evaluated_window'] is None for r in routes))
        self.assertTrue(all(r['visibility_state']=='PROPOSED_RULE_NOT_EVALUATED_RAW_EDITORIAL_VALUES_NOT_EXPOSED' for r in routes))

    def test_challenge_universal_fields_do_not_borrow_phase_windows(self):
        routes = [r for r in self.contract['field_routes'] if r['content_type']=='challenges' and r['field_kind']=='VISUAL_TEXT']
        self.assertEqual(len(routes), 5)
        self.assertTrue(all(r['visibility_policy_id'] is None and r['visibility_rule'] is None and r['evaluated_window'] is None for r in routes))
        self.assertTrue(all(r['visibility_state']=='NO_D9_9_FIELD_WINDOW_MAPPING' for r in routes))

    def test_phase_namespace_explicitly_prohibits_implicit_aliases(self):
        domain = self.contract['field_domain_separation']
        self.assertFalse(domain['challenge_phase_fields_are_aliases_of_universal_fields'])
        self.assertEqual(domain['challenge_phase_fields'], ['hook','reveal','cta'])
        aliases = {(x['phase_field'],x['universal_field']) for x in domain['prohibited_implicit_aliases']}
        self.assertEqual(aliases, {('hook','title'),('reveal','subtitle'),('cta','call_to_action')})

    def test_language_is_metadata_only_without_region_or_window(self):
        rows = [r for r in self.contract['field_routes'] if r['source_field']=='language']
        self.assertEqual(len(rows),3)
        for row in rows:
            self.assertEqual(row['field_kind'],'METADATA')
            self.assertIsNone(row['semantic_region_id'])
            self.assertEqual(row['visibility_state'],'METADATA_ONLY_NO_WINDOW')
            self.assertIsNone(row['evaluated_window'])

    def test_challenge_overlay_is_semantic_only_and_geometry_stays_unresolved(self):
        rows = [r for r in self.contract['field_routes'] if r['semantic_region_id']=='CHALLENGE_OVERLAY']
        self.assertEqual({r['source_field'] for r in rows},{'player_name','challenge_label'})
        self.assertTrue(all(r['geometry_state']=='UNRESOLVED_NO_COORDINATES' for r in rows))
        self.assertNotIn('bounds_permille', json.dumps(self.report))

    def test_payload_consumption_remains_zero_and_no_readiness_claim_is_made(self):
        self.assertEqual(self.report['summary']['current_visual_payload_consumption'],'ZERO_OF_14')
        self.assertEqual(self.report['summary']['evaluated_visibility_windows'],0)
        self.assertFalse(self.report['summary']['candidate_input_admissible'])
        self.assertFalse(self.report['approval_state']['editorial_values_visually_consumed'])

    def test_contract_schema_is_strict_and_validates_when_jsonschema_exists(self):
        self.assertIs(self.schema['additionalProperties'],False)
        self.assertEqual(set(self.schema['required']),set(self.schema['properties']))
        self.assertEqual(self.schema['$schema'],'https://json-schema.org/draft/2020-12/schema')
        try:
            import jsonschema
        except ImportError:
            # Structural fallback: schema and instance are both parsed, and top-level is exact.
            self.assertEqual(self.contract['schema'],'C11-D-RENDERER-EDITORIAL-FIELD-ROUTING-VISIBILITY-RECONCILIATION-V1')
        else:
            jsonschema.Draft202012Validator.check_schema(self.schema)
            jsonschema.Draft202012Validator(self.schema).validate(self.contract)

    def test_in_memory_report_revalidates_deterministically(self):
        second = build_reconciliation(ROOT)
        self.assertEqual(second,self.report)
        self.assertTrue(validate_reconciliation(self.report,ROOT))
        self.assertFalse(self.report['execution_boundary']['persistent_report_written'])
        self.assertFalse(self.report['execution_boundary']['renderer_native_input_emitted'])

    def test_tampered_report_digest_is_rejected(self):
        bad=copy.deepcopy(self.report)
        bad['field_routes'][0]['semantic_region_id']='FOOTER'
        with self.assertRaises(EditorialRoutingReconciliationError):
            validate_reconciliation(bad,ROOT)

    def test_resigned_but_promoted_mapping_is_rejected(self):
        bad=copy.deepcopy(self.report)
        bad['field_routes'][0]['semantic_region_id']='FOOTER'
        bad['reconciliation_sha256']=_sha_json({k:v for k,v in bad.items() if k!='reconciliation_sha256'})
        with self.assertRaises(EditorialRoutingReconciliationError):
            validate_reconciliation(bad,ROOT)

    def test_governance_locks_are_fail_closed(self):
        self.assertFalse(self.contract['approval_state']['routing_matrix_approved'])
        self.assertFalse(self.contract['approval_state']['semantic_region_mapping_approved'])
        self.assertFalse(self.contract['approval_state']['editorial_field_window_policy_approved'])
        self.assertFalse(self.contract['approval_state']['renderer_baseline_approved'])
        self.assertEqual(self.contract['approval_state']['release_authority'],'NONE')
        self.assertFalse(self.contract['execution_boundary']['media_created'])
        self.assertEqual(self.contract['execution_boundary']['d4_8'],'BLOCKED')

if __name__=='__main__':
    unittest.main(verbosity=2)
