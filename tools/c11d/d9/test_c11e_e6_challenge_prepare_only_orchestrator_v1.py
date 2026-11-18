from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

import c11e_e6_challenge_prepare_only_orchestrator_v1 as orch

ROOT = Path(__import__("os").environ.get("C11E_PROJECT_ROOT", Path(__file__).resolve().parents[3])).resolve()
MANIFEST_PATH = ROOT / "definitions/c11d/production/C11E_E6_CHALLENGE_PREPARE_ONLY_INPUT_MANIFEST_V1.json"


class E6ChallengePrepareOnlyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        cls.pin_doc = json.loads((ROOT / orch.PINS_REL).read_text(encoding="utf-8"))

    def mutated(self):
        return copy.deepcopy(self.manifest)

    def test_01_manifest_schema_and_status(self):
        orch.validate_manifest(self.manifest)
        self.assertEqual(self.manifest["status"], "DRAFT_PLAN_ONLY_NOT_FROZEN_NOT_EXECUTION_AUTHORITY")

    def test_02_exactly_six_challenge_groups(self):
        self.assertEqual(len(self.manifest["scenario_groups"]), 6)

    def test_03_exactly_eighteen_probe_subruns(self):
        self.assertEqual(sum(len(row["probes"]) for row in self.manifest["scenario_groups"]), 18)

    def test_04_probe_variants_are_a_b_c_in_order(self):
        for row in self.manifest["scenario_groups"]:
            self.assertEqual([p["variant"] for p in row["probes"]], ["A", "B_REPEAT", "C_CHANGED_MUSIC_SEED"])

    def test_05_gameplay_seeds_are_distinct(self):
        values = [r["gameplay_seed"] for r in self.manifest["scenario_groups"]]
        self.assertEqual(len(set(values)), 6)

    def test_06_mechanics_are_distinct(self):
        values = [r["mechanic"] for r in self.manifest["scenario_groups"]]
        self.assertEqual(len(set(values)), 6)

    def test_07_a_and_b_music_seeds_match(self):
        for row in self.manifest["scenario_groups"]:
            self.assertEqual(row["probes"][0]["music_seed"], row["probes"][1]["music_seed"])

    def test_08_c_music_seed_changes(self):
        for row in self.manifest["scenario_groups"]:
            self.assertNotEqual(row["probes"][0]["music_seed"], row["probes"][2]["music_seed"])

    def test_09_all_music_seeds_are_proposal_only(self):
        for row in self.manifest["scenario_groups"]:
            self.assertEqual(row["music_seed_authority"], "PROPOSAL_ONLY_NOT_AUTHORIZED")
            self.assertTrue(all(p["music_seed_status"] == "PROPOSAL_ONLY_NOT_AUTHORIZED" for p in row["probes"]))

    def test_10_request_template_is_explicit(self):
        template = self.manifest["request_template"]
        self.assertEqual(template["mode"], "REVIEW")
        self.assertEqual(template["delivery_profile_id"], "REVIEW_720")
        self.assertEqual(template["presentation_profile_id"], "social_default_v1")
        self.assertIn("show_hook_countdown", template["presentation_options"])

    def test_11_music_fixture_parameters_stay_unresolved(self):
        fixture = self.manifest["music_fixture"]
        self.assertFalse(fixture["tempo_bpm_sent_to_e1"])
        self.assertFalse(fixture["duration_seconds_sent_to_e1"])
        self.assertEqual(fixture["e1_unresolved_parameters"], ["tempo_bpm", "duration_seconds"])

    def test_12_manifest_rejects_unknown_selector(self):
        data = self.mutated()
        data["scenario_groups"][0]["selector"] = "CHALLENGE_999"
        with self.assertRaisesRegex(orch.OrchestratorError, "UNKNOWN_OR_UNAPPROVED_SELECTOR"):
            orch.validate_manifest(data)

    def test_13_manifest_rejects_missing_gameplay_seed(self):
        data = self.mutated()
        del data["scenario_groups"][0]["gameplay_seed"]
        with self.assertRaises(orch.OrchestratorError):
            orch.validate_manifest(data)

    def test_14_manifest_rejects_missing_music_seed(self):
        data = self.mutated()
        del data["scenario_groups"][0]["probes"][0]["music_seed"]
        with self.assertRaises(orch.OrchestratorError):
            orch.validate_manifest(data)

    def test_15_manifest_rejects_a_b_seed_mismatch(self):
        data = self.mutated()
        data["scenario_groups"][0]["probes"][1]["music_seed"] += 1
        with self.assertRaisesRegex(orch.OrchestratorError, "A_B_C_MUSIC_SEED_RELATION_INVALID"):
            orch.validate_manifest(data)

    def test_16_manifest_rejects_unchanged_c_seed(self):
        data = self.mutated()
        data["scenario_groups"][0]["probes"][2]["music_seed"] = data["scenario_groups"][0]["probes"][0]["music_seed"]
        with self.assertRaisesRegex(orch.OrchestratorError, "A_B_C_MUSIC_SEED_RELATION_INVALID"):
            orch.validate_manifest(data)

    def test_17_manifest_rejects_timebase_arithmetic_mismatch(self):
        data = self.mutated()
        data["scenario_groups"][0]["source_timebase"]["frames"] += 1
        with self.assertRaisesRegex(orch.OrchestratorError, "DECLARED_TIMEBASE_ARITHMETIC_MISMATCH"):
            orch.validate_manifest(data)

    def test_18_manifest_rejects_malformed_probe_order(self):
        data = self.mutated()
        data["scenario_groups"][0]["probes"].reverse()
        with self.assertRaisesRegex(orch.OrchestratorError, "PROBE_ORDER_OR_IDENTITY_MISMATCH"):
            orch.validate_manifest(data)

    def test_19_manifest_rejects_definition_path_identity_disagreement(self):
        data = self.mutated()
        data["scenario_groups"][0]["canonical_definition_path"] = "challenges/OTHER.json"
        with self.assertRaisesRegex(orch.OrchestratorError, "CANONICAL_DEFINITION_PATH_OR_SCENARIO_ID_MISMATCH"):
            orch.validate_manifest(data)

    def test_20_manifest_rejects_selector_identity_not_in_candidates(self):
        data = self.mutated()
        data["scenario_groups"][0]["selector"] = "CHALLENGE_008"
        with self.assertRaises(orch.OrchestratorError):
            orch.validate_manifest(data)

    def test_21_absolute_path_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(orch.OrchestratorError, "UNSAFE_RELATIVE_PATH"):
                orch.safe_project_path(Path(temp), "C:/Windows/system.ini")

    def test_22_parent_traversal_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(orch.OrchestratorError, "PATH_TRAVERSAL_REJECTED"):
                orch.safe_project_path(Path(temp), "../../outside.json")

    def test_23_backslash_path_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(orch.OrchestratorError, "UNSAFE_RELATIVE_PATH"):
                orch.safe_project_path(Path(temp), r"challenges\CHALLENGE_001.json")

    def test_24_execution_attempt_is_rejected(self):
        data = self.mutated()
        data["execution_boundary"]["media_authorized"] = True
        with self.assertRaisesRegex(orch.OrchestratorError, "EXECUTION_BOUNDARY_MUST_BE_EXACT_PREPARE_ONLY"):
            orch.validate_manifest(data)

    def test_25_unknown_execution_field_is_rejected(self):
        data = self.mutated()
        data["execution_boundary"]["execute"] = True
        with self.assertRaisesRegex(orch.OrchestratorError, "EXECUTION_BOUNDARY_MUST_BE_EXACT_PREPARE_ONLY"):
            orch.validate_manifest(data)

    def test_26_production_mode_is_rejected(self):
        data = self.mutated()
        data["request_template"]["mode"] = "PRODUCTION"
        with self.assertRaisesRegex(orch.OrchestratorError, "PREPARE_ONLY_MODE_MUST_BE_REVIEW"):
            orch.validate_manifest(data)

    def test_27_editorial_override_is_rejected(self):
        data = self.mutated()
        data["request_template"]["production_override"] = {"title": "Injected"}
        with self.assertRaisesRegex(orch.OrchestratorError, "PREPARE_ONLY_MANIFEST_MUST_NOT_INJECT_EDITORIAL_OVERRIDES"):
            orch.validate_manifest(data)

    def test_28_music_authority_change_is_rejected(self):
        data = self.mutated()
        data["scenario_groups"][0]["probes"][0]["music_seed_status"] = "AUTHORIZED"
        with self.assertRaisesRegex(orch.OrchestratorError, "MUSIC_SEED_NOT_EXPLICITLY_PROPOSAL_ONLY"):
            orch.validate_manifest(data)

    def test_29_wrong_presentation_options_are_rejected(self):
        data = self.mutated()
        data["request_template"]["presentation_options"] = {}
        with self.assertRaisesRegex(orch.OrchestratorError, "PRESENTATION_OPTIONS_MUST_BE_EXPLICIT_BOOLEAN"):
            orch.validate_manifest(data)

    def test_30_profile_id_must_be_explicit(self):
        data = self.mutated()
        data["music_fixture"]["profile_id"] = ""
        with self.assertRaisesRegex(orch.OrchestratorError, "MUSIC_FIXTURE_PROFILE_MUST_BE_EXPLICIT"):
            orch.validate_manifest(data)

    def test_31_int_seed_bool_is_rejected(self):
        data = self.mutated()
        data["scenario_groups"][0]["gameplay_seed"] = True
        with self.assertRaises(orch.OrchestratorError):
            orch.validate_manifest(data)

    def test_32_envelope_wrong_selector_is_rejected(self):
        group = self.manifest["scenario_groups"][0]
        probe = group["probes"][0]
        template = self.manifest["request_template"]
        intent = {
            "identity": {"intent_hash": "a" * 64},
            "delivery": {"requested_profile_id": template["delivery_profile_id"], "presentation_profile_id": template["presentation_profile_id"], "audio_enabled": template["audio_enabled"]},
            "music_contract": {"engine_request": {"music_seed": probe["music_seed"], "tempo_bpm": None, "duration_seconds": None}, "unresolved_engine_parameters": ["tempo_bpm", "duration_seconds"]},
            "request": {"presentation_options": template["presentation_options"]}
        }
        envelope = {"challenge_id": "CHALLENGE_WRONG"}
        fake_builder = type("Builder", (), {"validate_e1_intent": staticmethod(lambda *args: None)})
        with self.assertRaisesRegex(orch.OrchestratorError, "D_ENVELOPE_SELECTOR_MISMATCH"):
            orch.validate_e1_and_envelope(intent, envelope, {}, group, probe, template, [], fake_builder)

    def test_33_source_pin_document_hash_is_embedded_and_valid(self):
        self.assertEqual(orch.sha256_file(ROOT / orch.PINS_REL), orch.PINS_SHA256)

    def test_34_source_pin_rows_have_no_duplicates(self):
        rows = self.pin_doc["checkout_files"] + self.pin_doc["upstream_evidence_files"]
        paths = [row["path"] for row in rows]
        self.assertEqual(len(paths), len(set(paths)))

    def test_35_canonical_definition_hashes_are_valid_sha256(self):
        for group in self.manifest["scenario_groups"]:
            self.assertRegex(group["canonical_definition_sha256"], r"^[0-9a-f]{64}$")

    def test_36_evidence_run_id_is_not_a_batch_id(self):
        self.assertRegex("E6CHPREP_20261118T210430Z_A1B2C3D4", orch.RUN_ID_PATTERN)
        self.assertNotRegex("BATCH_20261118T210430Z_A1B2C3D4", orch.RUN_ID_PATTERN)

    def test_37_new_top_level_scenario_count_is_not_inflated(self):
        self.assertTrue(self.manifest["selection"]["probe_rows_are_subruns_not_additional_smoke18_scenarios"])
        self.assertEqual(self.manifest["selection"]["expected_group_count"], 6)

    def test_38_orchestrator_has_no_embedded_selector_seed_or_legacy_plan_defaults(self):
        source = (ROOT / "tools/c11d/d9/c11e_e6_challenge_prepare_only_orchestrator_v1.py").read_text(encoding="utf-8")
        self.assertNotRegex(source, r"CHALLENGE_00[0-9]")
        self.assertNotIn("840001", source)
        self.assertNotIn("840002", source)
        self.assertNotIn("run_plan(", source)
        self.assertNotIn("_challenge_request(", source)
        self.assertIn("plan_builder.build_envelope(root, intent, definition)", source)

    def test_39_receipt_pins_input_copy_and_sidecar(self):
        source = (ROOT / "tools/c11d/d9/c11e_e6_challenge_prepare_only_orchestrator_v1.py").read_text(encoding="utf-8")
        self.assertIn('"copy_path": f"{OUTPUT_REL}/{run_id}/{input_copy_rel}"', source)
        self.assertIn('"copy_sha256": input_copy_sha', source)
        self.assertIn('"copy_sidecar": f"{OUTPUT_REL}/{run_id}/{input_copy_rel}.sha256"', source)

    def test_40_input_manifest_matches_source_pin_document(self):
        rel = self.pin_doc["input_manifest_path"]
        actual = orch.sha256_file(ROOT / rel)
        self.assertEqual(actual, self.pin_doc["input_manifest_sha256"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
