from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import c11e_e6_challenge_plan_only_v1 as audit  # noqa: E402

ROOT = Path(os.environ.get("C11E_PROJECT_ROOT", HERE.parents[3])).resolve()


class C11EE6ChallengePlanOnlyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.matrix = audit.analyze_matrix(ROOT)

    def test_selected_six_have_expected_identity(self):
        self.assertEqual(
            self.matrix["selected_ids"],
            ["CHALLENGE_001", "CHALLENGE_002", "CHALLENGE_004", "CHALLENGE_005", "CHALLENGE_006", "CHALLENGE_007"],
        )

    def test_candidate_pool_is_exactly_seven(self):
        self.assertEqual(self.matrix["candidate_pool_count"], 7)
        self.assertEqual(len(self.matrix["candidate_pool"]), 7)

    def test_selected_mechanics_are_distinct(self):
        mechanics = [row["mechanic"] for row in self.matrix["selected_rows"]]
        self.assertEqual(len(set(mechanics)), 6)

    def test_selected_gameplay_seeds_are_distinct(self):
        seeds = [row["gameplay_seed"] for row in self.matrix["selected_rows"]]
        self.assertEqual(len(set(seeds)), 6)

    def test_challenge_003_excluded_for_pilot_and_seed_duplicate(self):
        self.assertEqual(self.matrix["excluded_id"], "CHALLENGE_003")
        self.assertIn("RNG-isolation", self.matrix["excluded_reason"])

    def test_source_fps_is_sixty_for_all_seven(self):
        self.assertTrue(all(row["source_fps"] == 60 for row in self.matrix["candidate_pool"]))

    def test_phase_sum_frames_match_canonical_timelines(self):
        actual = {row["challenge_id"]: row["source_frames"] for row in self.matrix["candidate_pool"]}
        self.assertEqual(actual, {
            "CHALLENGE_001": 540,
            "CHALLENGE_002": 600,
            "CHALLENGE_003": 720,
            "CHALLENGE_004": 900,
            "CHALLENGE_005": 420,
            "CHALLENGE_006": 540,
            "CHALLENGE_007": 600,
        })

    def test_challenge_002_phase_sum_is_ten_seconds(self):
        row = next(row for row in self.matrix["candidate_pool"] if row["challenge_id"] == "CHALLENGE_002")
        self.assertEqual(row["phase_sum_seconds"], 10.0)
        self.assertEqual(row["source_frames"], 600)

    def test_review_frame_counts_are_derived_at_thirty_fps(self):
        actual = {row["challenge_id"]: row["proposed_review_frames"] for row in self.matrix["selected_rows"]}
        self.assertEqual(actual, {
            "CHALLENGE_001": 270,
            "CHALLENGE_002": 300,
            "CHALLENGE_004": 450,
            "CHALLENGE_005": 210,
            "CHALLENGE_006": 270,
            "CHALLENGE_007": 300,
        })

    def test_008_and_009_are_not_selected(self):
        self.assertNotIn("CHALLENGE_008", self.matrix["selected_ids"])
        self.assertNotIn("CHALLENGE_009", self.matrix["selected_ids"])

    def test_music_fixture_pair_is_distinct_from_gameplay_seeds(self):
        music_seeds = {audit.MUSIC_FIXTURES["A"], audit.MUSIC_FIXTURES["C_CHANGED_MUSIC_SEED"]}
        gameplay_seeds = {row["gameplay_seed"] for row in self.matrix["selected_rows"]}
        self.assertTrue(music_seeds.isdisjoint(gameplay_seeds))
        self.assertEqual(audit.MUSIC_FIXTURES["A"], audit.MUSIC_FIXTURES["B_REPEAT"])
        self.assertNotEqual(audit.MUSIC_FIXTURES["A"], audit.MUSIC_FIXTURES["C_CHANGED_MUSIC_SEED"])

    def test_music_tempo_is_marked_historical_fixture_only(self):
        self.assertEqual(audit.MUSIC_TEMPO_BPM, 104)
        self.assertEqual(audit.MUSIC_PROFILE_ID, "challenge_8bit_v1")

    def test_generic_gdscript_consumer_uses_dynamic_challenge_identity(self):
        source = (ROOT / audit.ENVELOPE_CONSUMER_REL).read_text(encoding="utf-8")
        self.assertIn('envelope.get("challenge_id", "")', source)
        self.assertIn('challenge_config.get("challenge_id", challenge_config.get("id", ""))', source)
        self.assertNotIn("CHALLENGE_004", source)

    def test_existing_e4a6_envelope_builder_is_challenge_004_scoped(self):
        source = (ROOT / audit.E4A6_BUILDER_REL).read_text(encoding="utf-8")
        self.assertIn('Path("challenges/CHALLENGE_004.json")', source)
        self.assertIn('variant_id") != "CHALLENGE_004"', source)

    def test_existing_e4a7_av_worker_is_challenge_004_scoped(self):
        source = (ROOT / audit.E4A7_RUNNER_REL).read_text(encoding="utf-8")
        self.assertIn("CHALLENGE_004", source)
        self.assertIn("ISOLATED_CHALLENGE_004", source)

    def test_existing_e3_audio_pipeline_is_challenge_001_scoped(self):
        source = (ROOT / audit.E3_AUDIO_PIPELINE_REL).read_text(encoding="utf-8")
        self.assertIn('variant_id") != "CHALLENGE_001"', source)
        self.assertIn("PILOT_GAMEPLAY_SEED = 193847", source)

    def test_e1_service_leaves_tempo_and_duration_unresolved(self):
        source = (ROOT / audit.E1_SERVICE_REL).read_text(encoding="utf-8")
        self.assertIn('"tempo_bpm": None', source)
        self.assertIn('"duration_seconds": None', source)
        self.assertIn('["tempo_bpm", "duration_seconds"]', source)

    def test_plan_authority_never_grants_media(self):
        self.assertEqual(audit.MUSIC_FIXTURES["A"], 840001)
        self.assertEqual(audit.MUSIC_FIXTURES["C_CHANGED_MUSIC_SEED"], 840002)
        self.assertEqual(audit.D4_8_POLICY_SHA256, "0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07")


if __name__ == "__main__":
    unittest.main(verbosity=2)
