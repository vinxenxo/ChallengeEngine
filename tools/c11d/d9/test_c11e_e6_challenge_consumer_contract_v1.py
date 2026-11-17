from __future__ import annotations

import copy
import os
import unittest
from pathlib import Path

import c11e_e6_challenge_consumer_contract_v1 as audit

PROJECT_ROOT = Path(os.environ.get("C11E_PROJECT_ROOT", Path.cwd())).resolve()
PLAN_ROOT = PROJECT_ROOT / audit.PLAN_ROOT


class ChallengeConsumerContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = PROJECT_ROOT
        cls.receipt = audit.load_json(cls.root / audit.PLAN_RECEIPT_REL)
        cls.plan = audit.load_json(cls.root / audit.PLAN_JSON_REL)
        cls.selected = {x["challenge_id"]: x for x in cls.receipt["challenge_matrix"]["selected_rows"]}
        cls.e1_rows = {(x["challenge_id"], x["label"]): x for x in cls.receipt["e1_intents"]["rows"]}
        cls.d_rows = {(x["challenge_id"], x["label"]): x for x in cls.receipt["d_envelopes"]["rows"]}

    def _pair(self, challenge_id, variant):
        row = self.selected[challenge_id]
        erow = self.e1_rows[(challenge_id, variant)]
        drow = self.d_rows[(challenge_id, variant)]
        intent = audit.load_json(self.root / erow["intent_path"])
        envelope = audit.load_json(self.root / drow["envelope_path"])
        return row, erow, drow, intent, envelope

    def assert_envelope_mutation_rejected(self, mutator):
        row, erow, drow, intent, envelope = self._pair("CHALLENGE_004", "A")
        changed = copy.deepcopy(envelope)
        mutator(changed)
        with self.assertRaises(ValueError):
            audit.validate_envelope(changed, row, intent, "A")

    def test_01_all_24_source_pins_match(self):
        rows = {**audit.PINNED_20, **audit.PINNED_EXTRA}
        self.assertEqual(len(rows), 24)
        for rel, expected in rows.items():
            with self.subTest(path=rel):
                self.assertEqual(audit.sha256_file(self.root / rel), expected)

    def test_02_plan_receipt_and_sidecar_are_pinned(self):
        audit.check_file_and_sidecar(self.root / audit.PLAN_RECEIPT_REL, audit.PLAN_RECEIPT_SHA256, "PLAN_RECEIPT")

    def test_03_plan_json_and_sidecar_are_pinned(self):
        audit.check_file_and_sidecar(self.root / audit.PLAN_JSON_REL, audit.PLAN_JSON_SHA256, "PLAN_JSON")

    def test_04_recovery_receipt_is_the_successful_idempotent_recovery(self):
        path = self.root / audit.RECOVERY_RECEIPT_REL
        audit.check_file_and_sidecar(path, audit.RECOVERY_RECEIPT_SHA256, "RECOVERY_RECEIPT")
        obj = audit.load_json(path)
        self.assertEqual(obj["status"], "PASS_ADD_ONLY_IDEMPOTENT_RECOVERY")
        self.assertEqual((obj["files_expected"], obj["files_added"], obj["files_skipped_identical"], obj["files_final_verified"]), (7, 0, 7, 7))

    def test_05_predecessor_e6_audit_is_pinned_and_read_only(self):
        path = self.root / audit.PREDECESSOR_AUDIT_REL
        audit.check_file_and_sidecar(path, audit.PREDECESSOR_AUDIT_SHA256, "PREDECESSOR_AUDIT")
        obj = audit.load_json(path)
        self.assertEqual(obj["status"], "PASS_AUDIT_READ_ONLY_EVIDENCE_RECONCILED_EXECUTION_HELD")

    def test_06_exact_selected_six_and_candidate_pool(self):
        pool = self.receipt["challenge_matrix"]["candidate_pool"]
        self.assertEqual(len(pool), 7)
        self.assertEqual({x["challenge_id"] for x in pool}, {f"CHALLENGE_{i:03d}" for i in range(1, 8)})
        self.assertEqual(self.receipt["challenge_matrix"]["selected_ids"], audit.SELECTED_IDS)
        self.assertNotIn("CHALLENGE_008", self.receipt["challenge_matrix"]["selected_ids"])
        self.assertNotIn("CHALLENGE_009", self.receipt["challenge_matrix"]["selected_ids"])
        self.assertEqual(next(x for x in pool if x["challenge_id"] == "CHALLENGE_003")["selection_disposition"], "EXCLUDED_PILOT_DUPLICATE_GAMEPLAY_SEED")

    def test_07_six_selected_gameplay_seeds_are_distinct(self):
        seeds = [int(x["gameplay_seed"]) for x in self.receipt["challenge_matrix"]["selected_rows"]]
        self.assertEqual(len(seeds), 6)
        self.assertEqual(len(set(seeds)), 6)

    def test_08_all_six_canonical_timelines_match_plan(self):
        for cid, row in self.selected.items():
            with self.subTest(challenge_id=cid):
                audit.check_canonical_row(self.root, row)

    def test_09_native_timeline_is_60fps_and_review_derivation_is_30fps(self):
        for cid, row in self.selected.items():
            with self.subTest(challenge_id=cid):
                self.assertEqual(row["source_fps"], 60)
                self.assertEqual(row["proposed_review_fps"], 30)
                self.assertEqual(row["proposed_review_frames"] * 2, row["source_frames"])

    def test_10_exactly_18_e1_intent_rows_exist(self):
        self.assertEqual(len(self.e1_rows), 18)
        self.assertEqual(self.receipt["e1_intents"]["passed"], 18)

    def test_11_exactly_18_d_envelope_rows_exist(self):
        self.assertEqual(len(self.d_rows), 18)
        self.assertEqual(self.receipt["d_envelopes"]["passed"], 18)

    def test_12_all_18_intents_pass_the_e1_preparation_contract(self):
        for cid in audit.SELECTED_IDS:
            row = self.selected[cid]
            for variant in audit.VARIANTS:
                with self.subTest(challenge_id=cid, variant=variant):
                    _, erow, _, intent, _ = self._pair(cid, variant)
                    audit.check_file_and_sidecar(self.root / erow["intent_path"], erow["intent_sha256"], f"{cid}:{variant}")
                    audit.validate_intent(intent, row, variant, erow["request_id"])

    def test_13_all_18_d_envelopes_match_the_consumer_contract(self):
        for cid in audit.SELECTED_IDS:
            row = self.selected[cid]
            for variant in audit.VARIANTS:
                with self.subTest(challenge_id=cid, variant=variant):
                    _, _, drow, intent, envelope = self._pair(cid, variant)
                    audit.check_file_and_sidecar(self.root / drow["envelope_path"], drow["envelope_sha256"], f"{cid}:{variant}")
                    audit.validate_envelope(envelope, row, intent, variant)

    def test_14_ab_repeat_and_c_changed_music_seed_relations(self):
        for cid in audit.SELECTED_IDS:
            a = self._pair(cid, "A")[3]["seed_domains"]
            b = self._pair(cid, "B_REPEAT")[3]["seed_domains"]
            c = self._pair(cid, "C_CHANGED_MUSIC_SEED")[3]["seed_domains"]
            with self.subTest(challenge_id=cid):
                self.assertEqual(a["gameplay"]["value"], b["gameplay"]["value"])
                self.assertEqual(a["gameplay"]["value"], c["gameplay"]["value"])
                self.assertEqual(a["music"]["value"], b["music"]["value"])
                self.assertNotEqual(a["music"]["value"], c["music"]["value"])

    def test_15_e1_tempo_and_duration_remain_unresolved(self):
        for cid in audit.SELECTED_IDS:
            for variant in audit.VARIANTS:
                intent = self._pair(cid, variant)[3]
                request = intent["music_contract"]["engine_request"]
                with self.subTest(challenge_id=cid, variant=variant):
                    self.assertIsNone(request["tempo_bpm"])
                    self.assertIsNone(request["duration_seconds"])
                    self.assertFalse(intent["music_contract"]["engine_invoked"])

    def test_16_all_editorial_fields_are_omitted_empty_in_this_preflight(self):
        for cid in audit.SELECTED_IDS:
            for variant in audit.VARIANTS:
                envelope = self._pair(cid, variant)[4]
                with self.subTest(challenge_id=cid, variant=variant):
                    self.assertEqual([x["field"] for x in envelope["fields"]], audit.EXPECTED_FIELDS)
                    self.assertTrue(all(x["disposition"] == "OMITTED_EMPTY" and x["effective_value"] == "" for x in envelope["fields"]))

    def test_17_gdscript_consumer_contract_is_unchanged_and_dynamic(self):
        result = audit.validate_consumer_source(self.root)
        self.assertTrue(result["consumer_dynamic_challenge_identity"])
        self.assertEqual(result["legacy_e4a6_scope"], "CHALLENGE_004_ONLY")

    def test_18_adapter_remains_selector_generic_and_challenge_only(self):
        src = (self.root / "tools/c11d/d9/c11e_challenge_editorial_presentation_adapter.gd").read_text(encoding="utf-8")
        self.assertIn('str(request.get("content_type", "")) != "challenges"', src)
        self.assertNotIn("CHALLENGE_004", src)

    def test_19_generator_keeps_native_bind_then_existing_d_consumer_four_phase_hook(self):
        gen = (self.root / "GeneradorMaestro.gd").read_text(encoding="utf-8")
        self.assertEqual(gen.count("_apply_c11e_live_editorial_after_native_bind(rm)"), 4)
        self.assertIn('load("res://tools/c11d/d9/C11EChallengeLiveEditorialConsumer.gd")', gen)

    def test_20_legacy_media_entrypoints_are_still_scoped(self):
        e4a6 = (self.root / "tools/c11d/d9/c11e_e4a6_challenge_live_editorial_envelope.py").read_text(encoding="utf-8")
        e4a7 = (self.root / "tools/c11d/d9/c11e_e4a_challenge_av_review.py").read_text(encoding="utf-8")
        e3 = (self.root / "c11c-suite/c11c-producer/c11e_e3_audio_pipeline.py").read_text(encoding="utf-8")
        self.assertIn("CHALLENGE_004", e4a6)
        self.assertIn("CHALLENGE_004", e4a7)
        self.assertIn("CHALLENGE_001", e3)

    def test_21_preflight_does_not_claim_runtime_or_media_authority(self):
        self.assertFalse(self.plan["execution"]["godot_invoked"])
        self.assertFalse(self.plan["execution"]["audio_generated"])
        self.assertFalse(self.plan["execution"]["media_created"])
        self.assertFalse(self.plan["execution"]["new_batch_id_consumed"])
        self.assertFalse(self.plan["execution"]["production_dispatch"])
        self.assertEqual(self.plan["execution"]["release_authority"], "NONE")

    def test_22_negative_top_level_challenge_identity(self):
        self.assert_envelope_mutation_rejected(lambda x: x.__setitem__("challenge_id", "CHALLENGE_001"))

    def test_23_negative_nested_e1_selector_identity(self):
        self.assert_envelope_mutation_rejected(lambda x: x["e1_intent"]["request"]["selection"].__setitem__("variant_id", "CHALLENGE_001"))

    def test_24_negative_intent_hash_link(self):
        self.assert_envelope_mutation_rejected(lambda x: x.__setitem__("intent_hash", "0" * 64))

    def test_25_negative_request_id_link(self):
        self.assert_envelope_mutation_rejected(lambda x: x.__setitem__("request_id", "tampered"))

    def test_26_negative_wrong_native_fps(self):
        self.assert_envelope_mutation_rejected(lambda x: x["source_timebase"].__setitem__("fps", 30))

    def test_27_negative_wrong_phase_end_frame(self):
        self.assert_envelope_mutation_rejected(lambda x: x["source_phase_ranges"][1].__setitem__("end_frame", 419))

    def test_28_negative_wrong_policy_hash(self):
        self.assert_envelope_mutation_rejected(lambda x: x.__setitem__("policy_sha256", "0" * 64))

    def test_29_negative_missing_editorial_field(self):
        self.assert_envelope_mutation_rejected(lambda x: x["fields"].pop())

    def test_30_negative_duplicate_editorial_field(self):
        self.assert_envelope_mutation_rejected(lambda x: x["fields"].__setitem__(5, copy.deepcopy(x["fields"][0])))

    def test_31_negative_field_region(self):
        self.assert_envelope_mutation_rejected(lambda x: x["fields"][0].__setitem__("region", "FOOTER"))

    def test_32_negative_field_phase_window(self):
        self.assert_envelope_mutation_rejected(lambda x: x["fields"][0].__setitem__("source_phase_windows", ["GAME"]))

    def test_33_negative_effective_value_hash(self):
        self.assert_envelope_mutation_rejected(lambda x: x["fields"][0].__setitem__("value_sha256", "0" * 64))

    def test_34_negative_governance_media_boundary(self):
        self.assert_envelope_mutation_rejected(lambda x: x["governance"].__setitem__("media_created", True))

    def test_35_negative_release_authority(self):
        self.assert_envelope_mutation_rejected(lambda x: x["governance"].__setitem__("release_authority", "APPROVED"))

    def test_36_d4_8_v2_explicitly_forbids_smoke18_audio_and_mux(self):
        policy = audit.load_json(self.root / "definitions/c11d/production/C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V2.json")
        forbidden = policy["forbidden"]
        allowances = policy["allowances"]
        governance = policy["governance"]
        self.assertTrue(forbidden["smoke18_or_matrix99"])
        self.assertTrue(forbidden["d3_music_engine"])
        self.assertTrue(forbidden["pcm_audio_generation"])
        self.assertTrue(forbidden["ffmpeg_filter_or_mux"])
        self.assertFalse(allowances["audio_or_music_generation"])
        self.assertFalse(allowances["ffmpeg_filters"])
        self.assertFalse(allowances["ffmpeg_mux"])
        self.assertEqual(governance["d4_8_general_production"], "BLOCKED")
        self.assertEqual(governance["release_authority"], "NONE")


if __name__ == "__main__":
    unittest.main(verbosity=2)
