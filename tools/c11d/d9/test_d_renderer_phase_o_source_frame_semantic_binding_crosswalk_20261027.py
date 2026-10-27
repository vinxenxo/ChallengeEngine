#!/usr/bin/env python3
"""Unit tests for the Phase O read-only source-frame/semantic-proposal crosswalk."""
from __future__ import annotations
import ast
import importlib.util
import sys
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("audit_d_renderer_phase_o_source_frame_semantic_binding_crosswalk_20261027.py")
spec = importlib.util.spec_from_file_location("phase_o_crosswalk", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class PhaseOCrosswalkTests(unittest.TestCase):
    def test_canonical_json_hash_ignores_dictionary_insertion_order(self):
        self.assertEqual(module.canonical_json_sha256({"b": 2, "a": 1}), module.canonical_json_sha256({"a": 1, "b": 2}))

    def test_canonical_json_hash_preserves_array_order(self):
        self.assertNotEqual(module.canonical_json_sha256([1, 2]), module.canonical_json_sha256([2, 1]))

    def test_dotted_path_finds_top_level_key(self):
        self.assertEqual(module.get_dotted({"a": 1}, "a"), (True, 1))

    def test_dotted_path_finds_nested_key(self):
        self.assertEqual(module.get_dotted({"a": {"b": {"c": 2}}}, "a.b.c"), (True, 2))

    def test_dotted_path_reports_missing_key(self):
        self.assertEqual(module.get_dotted({"a": {}}, "a.b"), (False, None))

    def test_value_type_for_null(self):
        self.assertEqual(module.value_type(None), "null")

    def test_value_type_for_boolean_not_integer(self):
        self.assertEqual(module.value_type(True), "bool")

    def test_value_type_for_integer(self):
        self.assertEqual(module.value_type(7), "int")

    def test_value_type_for_float(self):
        self.assertEqual(module.value_type(7.0), "float")

    def test_value_type_for_string(self):
        self.assertEqual(module.value_type("abc"), "string")

    def test_value_type_for_numeric_vector(self):
        self.assertEqual(module.value_type([1.0, 2.0]), "array[float]")

    def test_value_type_for_mixed_vector_records_both_types(self):
        self.assertEqual(module.value_type([1, 2.0]), "array[float,int]")

    def test_without_process_ignores_process_identity(self):
        a = {"process": {"pid": 1}, "source_frames": {"count": 420}}
        b = {"process": {"pid": 2}, "source_frames": {"count": 420}}
        self.assertEqual(module.without_process(a), module.without_process(b))

    def test_receipt_diff_keys_reports_only_changed_fields(self):
        self.assertEqual(module.receipt_diff_keys({"a": 1, "b": 2}, {"a": 1, "b": 3}), ["b"])

    def test_custom_data_observation_absent_from_both_receipts(self):
        row = module.analyze_candidate_observation("target_x", {}, {})
        self.assertEqual(row["category"], "absent")
        self.assertTrue(row["repeat_presence_and_type_agreement"])
        self.assertFalse(row["actual_custom_data_values_serialized"])
        self.assertFalse(row["binding_approved"])

    def test_custom_data_observation_presence_and_type_stable(self):
        observed = {"target_x": {"present_frames": 420, "type_histogram": {"float": 420}}}
        row = module.analyze_candidate_observation("target_x", observed, observed)
        self.assertEqual(row["category"], "custom_data_candidate")
        self.assertEqual(row["status"], "PRESENCE_AND_TYPE_ONLY_VALUES_NOT_SERIALIZED")
        self.assertTrue(row["repeat_presence_and_type_agreement"])
        self.assertFalse(row["binding_approved"])

    def test_custom_data_observation_mismatch_is_unresolved(self):
        a = {"target_x": {"present_frames": 420, "type_histogram": {"float": 420}}}
        b = {"target_x": {"present_frames": 419, "type_histogram": {"float": 419}}}
        row = module.analyze_candidate_observation("target_x", a, b)
        self.assertEqual(row["category"], "custom_data_candidate")
        self.assertEqual(row["status"], "REPEAT_OBSERVATION_MISMATCH")
        self.assertFalse(row["repeat_presence_and_type_agreement"])

    def test_custom_data_present_in_only_one_receipt_is_unresolved(self):
        a = {"target_x": {"present_frames": 420, "type_histogram": {"float": 420}}}
        row = module.analyze_candidate_observation("target_x", a, {})
        self.assertEqual(row["category"], "unresolved")
        self.assertEqual(row["status"], "PRESENT_IN_ONLY_ONE_RECEIPT")

    def test_winning_frame_is_temporal_anchor_not_binding(self):
        row = module.classify_temporal_field("winning_frame")
        self.assertEqual(row["category"], "temporal_anchor")
        self.assertFalse(row["binding_approved"])
        self.assertFalse(row["runtime_receipt_serialized"])

    def test_close_calls_is_episode_counter_not_binding(self):
        row = module.classify_temporal_field("close_calls")
        self.assertEqual(row["category"], "episode_counter")
        self.assertFalse(row["binding_approved"])
        self.assertIn("COUNT_ONLY", row["policy"])

    def test_expected_challenge_ids_are_nine_and_ordered(self):
        self.assertEqual(len(module.CHALLENGE_IDS), 9)
        self.assertEqual(module.CHALLENGE_IDS[0], "CHALLENGE_001")
        self.assertEqual(module.CHALLENGE_IDS[-1], "CHALLENGE_009")

    def test_six_selector_specific_custom_data_candidates_are_pinned(self):
        self.assertEqual(len(module.EXPECTED_CUSTOM_FIELDS), 6)
        self.assertEqual(module.EXPECTED_CUSTOM_FIELDS["CHALLENGE_003"], "target_x")
        self.assertEqual(module.EXPECTED_CUSTOM_FIELDS["CHALLENGE_009"], "displayed_count")

    def test_only_challenges_008_and_009_have_timebase_conflict(self):
        self.assertEqual(module.EXPECTED_TIMEBASE_CONFLICTS, {"CHALLENGE_008", "CHALLENGE_009"})

    def test_base_fields_are_six_and_shapes_are_explicit(self):
        self.assertEqual(len(module.BASE_FIELDS), 6)
        self.assertEqual(set(module.BASE_FIELDS), set(module.EXPECTED_BASE_SHAPES))

    def test_all_governance_locks_keep_renderer_disabled(self):
        self.assertEqual(module.GOVERNANCE_LOCKS["renderer"], "OFF")
        self.assertFalse(module.GOVERNANCE_LOCKS["media_created"])
        self.assertFalse(module.GOVERNANCE_LOCKS["candidate_input_admissible"])
        self.assertEqual(module.GOVERNANCE_LOCKS["release_authority"], "NONE")

    def test_every_repo_path_call_supplies_root_and_relative(self):
        source = MODULE_PATH.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(MODULE_PATH))
        calls = [
            node for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "resolve_repo_path"
        ]
        self.assertGreater(len(calls), 0)
        self.assertTrue(
            all(len(call.args) == 2 for call in calls),
            "Every resolve_repo_path call must pass (root, relative).",
        )

    def test_editorial_sidecar_total_slots_are_fourteen(self):
        self.assertEqual(sum(len(fields) for fields in module.SIDECAR_FIELDS_BY_TYPE.values()), 14)

    def test_challenge_editorial_sidecar_has_six_fields(self):
        self.assertEqual(len(module.SIDECAR_FIELDS_BY_TYPE["challenges"]), 6)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(PhaseOCrosswalkTests)
    result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(suite)
    print(f"PHASE_O_UNIT_TESTS={result.testsRun - len(result.failures) - len(result.errors)}/{result.testsRun}")
    raise SystemExit(0 if result.wasSuccessful() else 1)
