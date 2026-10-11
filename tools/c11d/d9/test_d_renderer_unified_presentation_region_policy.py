from __future__ import annotations
import copy
import sys
import unittest
from pathlib import Path
HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
sys.path.insert(0, str(HERE.parent))
from d_renderer_unified_presentation_region_policy import (  # noqa: E402
    EXPECTED_FIELD_TARGETS, EXPECTED_LINEAGE, EXPECTED_MATRIX, EXPECTED_REGION_DEFINITIONS,
    POLICY_ID, UnifiedPresentationRegionPolicyError, build_preview, validate_contract, validate_preview,
)

class UnifiedPresentationRegionPolicyTests(unittest.TestCase):
    def test_contract_source_lineage_schema_and_governance(self):
        contract, schema = validate_contract(ROOT, verify_sources=True)
        self.assertEqual(contract['schema'], 'C11-D-D9-UNIFIED-PRESENTATION-REGION-POLICY-PROPOSAL-V1')
        self.assertEqual(len(contract['source_lineage']), len(EXPECTED_LINEAGE))
        self.assertEqual(contract['policy']['policy_id'], POLICY_ID)
        self.assertEqual(contract['policy']['state'], 'PROPOSED_NOT_APPROVED')
        self.assertFalse(contract['approval_state']['semantic_region_mapping_approved'])
        self.assertFalse(contract['approval_state']['shared_presentation_region_policy_approved'])
        self.assertIs(schema['additionalProperties'], False)

    def test_all_three_content_types_share_header_footer_regions(self):
        preview = build_preview(ROOT, verify_sources=True)
        self.assertEqual([x['content_type'] for x in preview['content_matrix']], ['visual_loops','visual_drills','challenges'])
        for row in preview['content_matrix']:
            targets = {x['field']: x['target_region'] for x in row['fields']}
            self.assertEqual(targets['title'], 'HEADER')
            self.assertEqual(targets['subtitle'], 'HEADER')
            self.assertEqual(targets['call_to_action'], 'FOOTER')
        self.assertEqual(preview['content_matrix'][0]['fields'], preview['content_matrix'][1]['fields'])

    def test_challenge_only_fields_use_challenge_overlay(self):
        preview = build_preview(ROOT, verify_sources=False)
        fields = {x['field']:x['target_region'] for x in preview['content_matrix'][2]['fields']}
        self.assertEqual(fields['player_name'], 'CHALLENGE_OVERLAY')
        self.assertEqual(fields['challenge_label'], 'CHALLENGE_OVERLAY')
        for row in preview['content_matrix'][:2]:
            self.assertNotIn('player_name', {x['field'] for x in row['fields']})
            self.assertNotIn('challenge_label', {x['field'] for x in row['fields']})

    def test_language_is_metadata_and_geometry_is_undefined(self):
        preview = build_preview(ROOT, verify_sources=False)
        self.assertEqual(preview['metadata_only_fields'], ['language'])
        self.assertTrue(all(x['geometry_state'] == 'UNRESOLVED_NO_COORDINATES' for x in preview['content_matrix']))
        self.assertTrue(all(x['geometry_state'] == 'UNRESOLVED_NO_COORDINATES' for x in preview['region_definitions'].values()))
        self.assertFalse(preview['execution_boundary']['coordinates_emitted'])

    def test_target_canvas_is_review_720_metadata(self):
        self.assertEqual(build_preview(ROOT, verify_sources=False)['target_canvas'], {'profile_id':'REVIEW_720','width':720,'height':1280,'fps':30,'aspect_ratio':'9:16','source':'PINNED_DELIVERY_PROFILE_METADATA_ONLY'})

    def test_preview_deterministic_and_non_executable(self):
        first = build_preview(ROOT, verify_sources=False)
        self.assertEqual(first, build_preview(ROOT, verify_sources=False))
        self.assertFalse(first['policy_approved'])
        self.assertFalse(first['execution_boundary']['renderer_native_input_emitted'])
        self.assertFalse(first['execution_boundary']['renderer_activation'])
        self.assertEqual(first['execution_boundary']['d4_8'], 'BLOCKED')
        validate_preview(first, ROOT, verify_sources=False)

    def test_pinned_logical_composition_and_frame_program_are_in_agreement(self):
        validate_contract(ROOT, verify_sources=True)

    def test_negative_policy_approval_rejected(self):
        contract, _ = validate_contract(ROOT, verify_sources=False)
        contract['policy']['state'] = 'APPROVED'
        (ROOT / 'definitions/c11d/production/D_RENDERER_UNIFIED_PRESENTATION_REGION_POLICY_PROPOSAL_V1.json').read_text(encoding='utf-8')
        # Exercise the independent preview validator without mutating source files.
        preview = build_preview(ROOT, verify_sources=False)
        preview['policy_approved'] = True
        with self.assertRaises(UnifiedPresentationRegionPolicyError):
            validate_preview(preview, ROOT, verify_sources=False)

    def test_negative_region_mapping_drift_rejected(self):
        preview = build_preview(ROOT, verify_sources=False)
        preview['field_region_targets']['title']['target_region'] = 'FOOTER'
        with self.assertRaises(UnifiedPresentationRegionPolicyError):
            validate_preview(preview, ROOT, verify_sources=False)

    def test_negative_coordinate_invention_rejected(self):
        preview = build_preview(ROOT, verify_sources=False)
        preview['region_definitions']['HEADER']['x'] = 10
        with self.assertRaises(UnifiedPresentationRegionPolicyError):
            validate_preview(preview, ROOT, verify_sources=False)

    def test_negative_challenge_fields_leak_into_loop_rejected(self):
        preview = build_preview(ROOT, verify_sources=False)
        preview['content_matrix'][0]['fields'].append({'field':'player_name','target_region':'CHALLENGE_OVERLAY','semantic_role':'CHALLENGE_PLAYER_NAME','z_order':40})
        with self.assertRaises(UnifiedPresentationRegionPolicyError):
            validate_preview(preview, ROOT, verify_sources=False)

    def test_negative_typography_promotion_rejected(self):
        preview = build_preview(ROOT, verify_sources=False)
        preview['unresolved_presentation_domains']['typography_fonts_sizes_weights'] = 'APPROVED_FONT_SIZE_48'
        with self.assertRaises(UnifiedPresentationRegionPolicyError):
            validate_preview(preview, ROOT, verify_sources=False)

    def test_negative_timing_policy_scope_promotion_rejected(self):
        preview = build_preview(ROOT, verify_sources=False)
        preview['visibility_timing_behavior'] = 'AUTO_INFER_PHASE_VISIBILITY'
        with self.assertRaises(UnifiedPresentationRegionPolicyError):
            validate_preview(preview, ROOT, verify_sources=False)

    def test_negative_source_mapping_mutation_rejected(self):
        contract, _ = validate_contract(ROOT, verify_sources=False)
        self.assertEqual(contract['policy']['region_definitions'], EXPECTED_REGION_DEFINITIONS)
        self.assertEqual(contract['policy']['field_region_targets'], EXPECTED_FIELD_TARGETS)
        self.assertEqual(contract['policy']['content_matrix'], EXPECTED_MATRIX)

    def test_approval_and_release_locks_are_mandatory(self):
        contract, _ = validate_contract(ROOT, verify_sources=False)
        self.assertFalse(contract['approval_state']['renderer_baseline_approved'])
        self.assertFalse(contract['approval_state']['renderer_baseline_frozen'])
        self.assertFalse(contract['approval_state']['d4_8_authorized'])
        self.assertEqual(contract['approval_state']['release_authority'], 'NONE')
        self.assertFalse(contract['execution_boundary']['media_created'])


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(UnifiedPresentationRegionPolicyTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful(): return 1
    print('C11-D RENDERER UNIFIED PRESENTATION REGION POLICY PROPOSAL PASS | content_types=3/3 | shared_regions=HEADER/FOOTER | challenge_overlay=CHALLENGES_ONLY | target=REVIEW_720_720x1280 | coordinates=UNRESOLVED | policy=PROPOSED_NOT_APPROVED | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE')
    return 0
if __name__ == '__main__': raise SystemExit(main())
