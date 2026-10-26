from __future__ import annotations
import contextlib
import hashlib
import io
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CONTRACT_PATH = ROOT / "definitions/c11d/production/D_RENDERER_UNIVERSAL_EDITORIAL_FIELD_VISIBILITY_POLICY_PROPOSAL_V1.json"
SCHEMA_PATH = ROOT / "definitions/c11d/production/D_RENDERER_UNIVERSAL_EDITORIAL_FIELD_VISIBILITY_POLICY_PROPOSAL_SCHEMA_V1.json"
RUNNER_PATH = ROOT / "tools/c11d/d9/d_renderer_universal_editorial_field_visibility_policy_proposal.py"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class UniversalEditorialFieldVisibilityProposalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = load(CONTRACT_PATH)
        cls.schema = load(SCHEMA_PATH)

    def test_contract_and_strict_schema_validate(self):
        import jsonschema
        jsonschema.Draft202012Validator.check_schema(self.schema)
        jsonschema.Draft202012Validator(self.schema).validate(self.contract)
        self.assertEqual(self.contract["status"], "PROPOSAL_ONLY_NOT_RENDERER_INPUT")

    def test_all_current_source_pins_match(self):
        for pin in self.contract["source_lineage"]:
            with self.subTest(path=pin["path"]):
                self.assertEqual(digest(ROOT / pin["path"]), pin["sha256"])

    def test_exact_three_content_types(self):
        self.assertEqual([x["content_type"] for x in self.contract["content_matrix"]], ["challenges", "visual_loops", "visual_drills"])

    def test_exact_fourteen_field_instances(self):
        self.assertEqual(sum(len(x["field_rules"]) for x in self.contract["content_matrix"]), 14)

    def test_challenge_has_six_universal_fields(self):
        row = self.contract["content_matrix"][0]
        self.assertEqual([f["field_id"] for f in row["field_rules"]], ["title", "subtitle", "call_to_action", "player_name", "challenge_label", "language"])

    def test_loop_has_four_universal_fields(self):
        row = self.contract["content_matrix"][1]
        self.assertEqual([f["field_id"] for f in row["field_rules"]], ["title", "subtitle", "call_to_action", "language"])

    def test_drill_has_four_universal_fields(self):
        row = self.contract["content_matrix"][2]
        self.assertEqual([f["field_id"] for f in row["field_rules"]], ["title", "subtitle", "call_to_action", "language"])

    def test_visual_window_rule_count_is_eleven(self):
        rules = [f for c in self.contract["content_matrix"] for f in c["field_rules"] if f["field_class"] == "VISUAL_TEXT"]
        self.assertEqual(len(rules), 11)
        self.assertTrue(all(f["candidate_window_rule"] == "FULL_DELIVERY_TIMELINE_IF_NONEMPTY" for f in rules))

    def test_language_is_metadata_only_in_all_content_types(self):
        rules = [next(f for f in c["field_rules"] if f["field_id"] == "language") for c in self.contract["content_matrix"]]
        self.assertEqual(len(rules), 3)
        for rule in rules:
            self.assertEqual(rule["field_class"], "METADATA_ONLY")
            self.assertIsNone(rule["target_region"])
            self.assertEqual(rule["candidate_window_rule"], "NO_VISIBILITY_WINDOW")
            self.assertIsNone(rule["candidate_interval_formula"])

    def test_shared_field_region_mapping(self):
        expected = {"title": "HEADER", "subtitle": "HEADER", "call_to_action": "FOOTER", "player_name": "CHALLENGE_OVERLAY", "challenge_label": "CHALLENGE_OVERLAY"}
        for content in self.contract["content_matrix"]:
            for field in content["field_rules"]:
                if field["field_id"] in expected:
                    self.assertEqual(field["target_region"], expected[field["field_id"]])

    def test_challenge_only_fields_do_not_leak(self):
        for content in self.contract["content_matrix"][1:]:
            names = [f["field_id"] for f in content["field_rules"]]
            self.assertNotIn("player_name", names)
            self.assertNotIn("challenge_label", names)

    def test_candidate_delivery_timeline_fixtures(self):
        expected = [(60,30,450,15.0),(30,30,600,20.0),(30,30,630,21.0)]
        for content, wanted in zip(self.contract["content_matrix"], expected):
            self.assertEqual((content["source_fps"],content["delivery_fps"],content["candidate_delivery_frame_count"],content["candidate_duration_seconds"]), wanted)
            self.assertEqual(content["timeline_basis"], "EXISTING_UNAPPROVED_DELIVERY_TIMEBASE_REVIEW_FIXTURE_ONLY")

    def test_intervals_are_zero_based_half_open(self):
        self.assertEqual(self.contract["policy"]["interval_convention"], "ZERO_BASED_HALF_OPEN_DELIVERY_FRAME_RANGE_START_INCLUSIVE_END_EXCLUSIVE")
        self.assertEqual(self.contract["policy"]["candidate_window_formula"], "[0,delivery_frame_count)")

    def test_windows_remain_unevaluated(self):
        self.assertEqual(self.contract["policy"]["window_evaluation_state"], "NOT_EVALUATED_RAW_FIELD_VALUES_ARE_NOT_EXPOSED_BY_CURRENT_RUNTIME_SUMMARY")
        self.assertEqual(self.contract["review_output"]["evaluated_visibility_windows"], 0)
        self.assertTrue(all(f["window_evaluated"] is False for c in self.contract["content_matrix"] for f in c["field_rules"]))

    def test_challenge_phase_namespace_cannot_alias_universal_fields(self):
        text = self.contract["policy"]["challenge_phase_namespace_rule"]
        self.assertIn("HOOK_REVEAL_CTA_REMAIN_DISTINCT", text)
        self.assertIn("NO_IMPLICIT_ALIAS", text)
        self.assertNotIn("phase", [f["field_id"] for c in self.contract["content_matrix"] for f in c["field_rules"]])

    def test_empty_values_are_suppressed(self):
        self.assertEqual(self.contract["policy"]["empty_value_rule"], "SUPPRESS_FIELD_AND_ASSIGN_NO_WINDOW")

    def test_exact_text_is_preserved_without_transformations(self):
        self.assertEqual(self.contract["policy"]["text_value_rule"], "PRESERVE_EXACT_SOURCE_STRING_NO_TRIM_TRANSLATION_NORMALIZATION_OR_REWRITE")

    def test_no_raw_editorial_values_embedded(self):
        serialized = json.dumps(self.contract, ensure_ascii=False)
        self.assertNotIn("¡SOLO EL 1% APARCA SIN ROZAR!", serialized)
        self.assertNotIn("¿Lo has clavado?", serialized)
        self.assertNotIn('"text_value"', serialized)

    def test_geometry_stays_unresolved(self):
        self.assertEqual(self.contract["region_policy"]["geometry_state"], "UNRESOLVED_NO_COORDINATES")
        self.assertFalse(self.contract["region_policy"]["pixel_placement_authorized"])

    def test_all_approval_and_renderer_locks_are_closed(self):
        state = self.contract["approval_state"]
        self.assertFalse(state["universal_editorial_field_window_policy_approved"])
        self.assertFalse(state["unified_presentation_region_policy_approved"])
        self.assertFalse(state["delivery_timebase_policy_approved"])
        self.assertFalse(state["payload_consumer_implementation_authorized"])
        self.assertFalse(state["d4_8_authorized"])
        self.assertEqual(state["release_authority"], "NONE")
        self.assertEqual(self.contract["execution_boundary"]["renderer"], "OFF")
        self.assertFalse(self.contract["execution_boundary"]["media_created"])
        self.assertFalse(self.contract["execution_boundary"]["candidate_input_admissible"])
        self.assertEqual(self.contract["execution_boundary"]["approved_bindings"], 0)

    def test_unknown_fields_fail_closed(self):
        self.assertEqual(self.contract["policy"]["unknown_field_rule"], "REJECT_UNTIL_EXPLICIT_POLICY_MAPPING_IS_ADDED")

    def test_runner_does_not_write_persistent_receipt(self):
        before = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*receipt*") if p.is_file()}
        from importlib.util import spec_from_file_location, module_from_spec
        spec = spec_from_file_location("proposal_runner", RUNNER_PATH)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        report1 = module.validate(ROOT)
        report2 = module.validate(ROOT)
        after = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*receipt*") if p.is_file()}
        self.assertEqual(report1, report2)
        self.assertEqual(before, after)
        self.assertEqual(report1["evaluated_windows"], 0)

    def test_runner_emits_fail_closed_not_video_ready(self):
        from importlib.util import spec_from_file_location, module_from_spec
        spec = spec_from_file_location("proposal_runner", RUNNER_PATH)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        report = module.validate(ROOT)
        self.assertEqual(report["status"], "PREPARATION_ONLY_PROPOSAL_VALIDATED_NOT_APPROVED")
        self.assertFalse(report["candidate_input_admissible"])
        self.assertEqual(report["renderer"], "OFF")
        self.assertEqual(report["release_authority"], "NONE")


if __name__ == "__main__":
    unittest.main(verbosity=2)
