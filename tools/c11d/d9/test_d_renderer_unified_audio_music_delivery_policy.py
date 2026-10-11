from __future__ import annotations
import copy
import sys
import unittest
from pathlib import Path
HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
sys.path.insert(0, str(HERE.parent))
from d_renderer_unified_audio_music_delivery_policy import (  # noqa: E402
    EXPECTED_LINEAGE, EXPECTED_MATRIX, EXPECTED_PROFILE, POLICY_ID,
    UnifiedAudioMusicDeliveryPolicyError, build_preview, validate_contract, validate_preview,
)

class UnifiedAudioMusicDeliveryPolicyTests(unittest.TestCase):
    def test_contract_schema_lineage_and_approval_boundary(self):
        contract, schema = validate_contract(ROOT, verify_sources=False)
        self.assertEqual(contract['schema'], 'C11-D-D9-UNIFIED-AUDIO-MUSIC-DELIVERY-POLICY-PROPOSAL-V1')
        self.assertEqual(len(contract['source_lineage']), len(EXPECTED_LINEAGE))
        self.assertEqual(contract['policy']['policy_id'], POLICY_ID)
        self.assertEqual(contract['policy']['state'], 'PROPOSED_NOT_APPROVED')
        self.assertFalse(contract['approval_state']['audio_delivery_profile_policy_approved'])
        self.assertFalse(contract['execution_boundary']['renderer_activation'])
        self.assertIs(schema['additionalProperties'], False)

    def test_pinned_review_profile_contains_audio_envelope(self):
        preview = build_preview(ROOT, verify_sources=False)
        self.assertEqual(preview['target_audio_profile'], EXPECTED_PROFILE)
        self.assertEqual((EXPECTED_PROFILE['audio_codec'], EXPECTED_PROFILE['audio_profile']), ('aac', 'aac_low'))
        self.assertEqual((EXPECTED_PROFILE['audio_bitrate_kbps'], EXPECTED_PROFILE['audio_sample_rate_hz'], EXPECTED_PROFILE['audio_channels']), (192, 48000, 2))

    def test_loop_exact_preencode_sample_count(self):
        row = EXPECTED_MATRIX[0]
        self.assertEqual((row['duration_seconds'], row['target_pcm_sample_count']), (20.0, 960000))
        self.assertEqual(row['target_pcm_sample_count'], int(row['duration_seconds'] * row['audio_sample_rate_hz']))

    def test_drill_exact_preencode_sample_count(self):
        row = EXPECTED_MATRIX[1]
        self.assertEqual((row['duration_seconds'], row['target_pcm_sample_count']), (21.0, 1008000))
        self.assertEqual(row['target_pcm_sample_count'], int(row['duration_seconds'] * row['audio_sample_rate_hz']))

    def test_challenge_exact_preencode_sample_count(self):
        row = EXPECTED_MATRIX[2]
        self.assertEqual((row['duration_seconds'], row['target_pcm_sample_count']), (15.0, 720000))
        self.assertEqual((row['delivery_fps'], row['delivery_frame_count']), (30, 450))
        self.assertEqual(row['target_pcm_sample_count'], int(row['duration_seconds'] * row['audio_sample_rate_hz']))

    def test_all_audio_timelines_follow_video_durations(self):
        self.assertEqual([(x['duration_seconds'], x['delivery_frame_count']) for x in EXPECTED_MATRIX], [(20.0,600),(21.0,630),(15.0,450)])
        self.assertTrue(all(x['timeline_rule'] == 'MATCH_VIDEO_DURATION_PRE_ENCODE' for x in EXPECTED_MATRIX))

    def test_preview_is_deterministic_and_unmaterialized(self):
        first = build_preview(ROOT, verify_sources=False)
        self.assertEqual(first, build_preview(ROOT, verify_sources=False))
        self.assertFalse(first['audio_payload_materialized'])
        self.assertFalse(first['audio_samples_emitted'])
        self.assertFalse(first['music_asset_selected'])
        self.assertFalse(first['policy_approved'])
        validate_preview(first, ROOT, verify_sources=False)

    def test_music_selection_and_loudness_remain_out_of_scope(self):
        contract, _ = validate_contract(ROOT, verify_sources=False)
        self.assertEqual(contract['policy']['music_asset_policy'], 'OUT_OF_SCOPE_NOT_SELECTED_NOT_EMITTED')
        self.assertEqual(contract['policy']['mixing_policy'], 'OUT_OF_SCOPE_NOT_DEFINED_NOT_APPLIED')
        self.assertEqual(contract['policy']['loudness_policy'], 'OUT_OF_SCOPE_NOT_DEFINED_NOT_APPLIED')
        self.assertEqual(contract['policy']['missing_audio_policy'], 'UNRESOLVED_NO_AUTOMATIC_SILENCE_OR_SYNTHESIS')

    def test_negative_policy_promotion_rejected(self):
        preview = build_preview(ROOT, verify_sources=False)
        preview['policy_state'] = 'APPROVED'
        with self.assertRaises(UnifiedAudioMusicDeliveryPolicyError):
            validate_preview(preview, ROOT, verify_sources=False)

    def test_negative_sample_count_drift_rejected(self):
        preview = build_preview(ROOT, verify_sources=False)
        preview['content_matrix'][0]['target_pcm_sample_count'] = 959999
        with self.assertRaises(UnifiedAudioMusicDeliveryPolicyError):
            validate_preview(preview, ROOT, verify_sources=False)

    def test_negative_music_selection_rejected(self):
        preview = build_preview(ROOT, verify_sources=False)
        preview['music_asset_selected'] = True
        with self.assertRaises(UnifiedAudioMusicDeliveryPolicyError):
            validate_preview(preview, ROOT, verify_sources=False)

    def test_negative_audio_sample_emission_rejected(self):
        preview = build_preview(ROOT, verify_sources=False)
        preview['audio_samples_emitted'] = True
        with self.assertRaises(UnifiedAudioMusicDeliveryPolicyError):
            validate_preview(preview, ROOT, verify_sources=False)

    def test_negative_codec_profile_drift_rejected(self):
        preview = build_preview(ROOT, verify_sources=False)
        preview['target_audio_profile']['audio_sample_rate_hz'] = 44100
        with self.assertRaises(UnifiedAudioMusicDeliveryPolicyError):
            validate_preview(preview, ROOT, verify_sources=False)

    def test_negative_execution_boundary_promotion_rejected(self):
        preview = build_preview(ROOT, verify_sources=False)
        preview['execution_boundary']['renderer_activation'] = True
        with self.assertRaises(UnifiedAudioMusicDeliveryPolicyError):
            validate_preview(preview, ROOT, verify_sources=False)

def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(UnifiedAudioMusicDeliveryPolicyTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        return 1
    print('C11-D RENDERER UNIFIED AUDIO/MUSIC DELIVERY POLICY PROPOSAL PASS | content_types=3/3 | sample_counts=960000/1008000/720000@48KHZ | AACLC=192KBPS_STEREO | music_selection=OUT_OF_SCOPE | policy=PROPOSED_NOT_APPROVED | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
