from __future__ import annotations
import copy
import sys
import unittest
from pathlib import Path
HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
sys.path.insert(0, str(HERE.parent))
from d_renderer_unified_delivery_timebase_policy import (  # noqa: E402
    CONTRACT_REL, EXPECTED_LINEAGE, EXPECTED_MATRIX, POLICY_ID, UnifiedDeliveryPolicyError,
    build_preview, validate_contract, validate_preview,
)

class UnifiedDeliveryTimebasePolicyTests(unittest.TestCase):
    def test_contract_lineage_schema_and_proposal_state(self):
        contract, schema = validate_contract(ROOT)
        self.assertEqual(contract['schema'], 'C11-D-D9-UNIFIED-DELIVERY-TIMEBASE-POLICY-PROPOSAL-V1')
        self.assertEqual(len(contract['source_lineage']), len(EXPECTED_LINEAGE))
        self.assertEqual(contract['policy']['policy_id'], POLICY_ID)
        self.assertEqual(contract['policy']['state'], 'PROPOSED_NOT_APPROVED')
        self.assertFalse(contract['approval_state']['unified_delivery_timebase_policy_approved'])
        self.assertFalse(contract['execution_boundary']['renderer_activation'])
        self.assertIs(schema['additionalProperties'], False)

    def test_loop_is_identity_30_fps_without_resampling(self):
        row = EXPECTED_MATRIX[0]
        self.assertEqual((row['source_fps'], row['delivery_fps']), (30, 30))
        self.assertEqual((row['source_frame_count'], row['delivery_frame_count']), (600, 600))
        self.assertEqual(row['timebase_mode'], 'IDENTITY_NO_RESAMPLING')
        self.assertFalse(row['delivery_candidate_materialized'])

    def test_drill_is_identity_30_fps_without_resampling(self):
        row = EXPECTED_MATRIX[1]
        self.assertEqual((row['source_fps'], row['delivery_fps']), (30, 30))
        self.assertEqual((row['source_frame_count'], row['delivery_frame_count']), (630, 630))
        self.assertEqual(row['timebase_mode'], 'IDENTITY_NO_RESAMPLING')

    def test_challenge_uses_separate_temporal_and_sampling_proposals(self):
        row = EXPECTED_MATRIX[2]
        self.assertEqual((row['source_fps'], row['delivery_fps']), (60, 30))
        self.assertEqual((row['source_frame_count'], row['delivery_frame_count']), (900, 450))
        self.assertEqual(row['source_phase_boundaries'], [0,180,600,780,900])
        self.assertEqual(row['delivery_phase_boundaries'], [0,90,300,390,450])
        self.assertEqual((row['source_snapshot_count'], row['delivery_snapshot_count']), (420,210))
        self.assertEqual(row['interpolation'], 'NONE')
        self.assertFalse(row['delivery_candidate_materialized'])

    def test_preview_is_deterministic_and_has_shared_target_profile(self):
        first = build_preview(ROOT)
        second = build_preview(ROOT)
        self.assertEqual(first, second)
        self.assertEqual(first['target_delivery_profile']['profile_id'], 'REVIEW_720')
        self.assertEqual(first['target_delivery_profile']['fps'], 30)
        self.assertEqual(len(first['content_matrix']), 3)
        self.assertFalse(first['delivery_candidate_materialized'])

    def test_audio_music_is_explicitly_out_of_scope(self):
        preview = build_preview(ROOT)
        self.assertEqual(preview['audio_music_policy'], 'OUT_OF_SCOPE_NOT_DEFINED_NOT_EMITTED')
        self.assertFalse(preview['policy_approved'])

    def test_negative_changed_matrix_rejected(self):
        preview = build_preview(ROOT)
        preview['content_matrix'][0]['delivery_frame_count'] = 599
        with self.assertRaises(UnifiedDeliveryPolicyError): validate_preview(preview, ROOT)

    def test_negative_policy_promotion_rejected(self):
        preview = build_preview(ROOT)
        preview['policy_state'] = 'APPROVED'
        with self.assertRaises(UnifiedDeliveryPolicyError): validate_preview(preview, ROOT)

    def test_negative_renderer_activation_rejected(self):
        preview = build_preview(ROOT)
        preview['execution_boundary']['renderer_activation'] = True
        with self.assertRaises(UnifiedDeliveryPolicyError): validate_preview(preview, ROOT)

    def test_negative_media_creation_rejected(self):
        preview = build_preview(ROOT)
        preview['media_created'] = True
        with self.assertRaises(UnifiedDeliveryPolicyError): validate_preview(preview, ROOT)

    def test_negative_music_policy_cannot_be_claimed(self):
        preview = build_preview(ROOT)
        preview['audio_music_policy'] = 'NORMALIZED'
        with self.assertRaises(UnifiedDeliveryPolicyError): validate_preview(preview, ROOT)

    def test_negative_profile_change_rejected(self):
        preview = build_preview(ROOT)
        preview['target_delivery_profile']['fps'] = 60
        with self.assertRaises(UnifiedDeliveryPolicyError): validate_preview(preview, ROOT)

    def test_negative_source_lineage_digest_mismatch(self):
        contract, _ = validate_contract(ROOT)
        contract_path = ROOT / CONTRACT_REL
        original_bytes = contract_path.read_bytes()
        original = original_bytes.decode('utf-8')
        try:
            data = __import__('json').loads(original)
            data['source_lineage'][1]['sha256'] = '0' * 64
            contract_path.write_text(__import__('json').dumps(data), encoding='utf-8')
            with self.assertRaises(UnifiedDeliveryPolicyError): validate_contract(ROOT)
        finally:
            # Restore the exact bytes, not text-normalized bytes: the source contract's
            # line endings are covered by downstream SHA-256 lineage pins.
            contract_path.write_bytes(original_bytes)
            self.assertEqual(contract_path.read_bytes(), original_bytes)

def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(UnifiedDeliveryTimebasePolicyTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        return 1
    print("C11-D RENDERER UNIFIED DELIVERY TIMEBASE POLICY PROPOSAL PASS | content_types=3/3 | loop=600@30FPS_IDENTITY | drill=630@30FPS_IDENTITY | challenge=900@60_TO_450@30FPS | target=REVIEW_720_720x1280 | audio_music=OUT_OF_SCOPE | policy=PROPOSED_NOT_APPROVED | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
