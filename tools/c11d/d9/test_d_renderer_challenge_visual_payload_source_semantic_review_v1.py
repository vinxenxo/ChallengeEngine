#!/usr/bin/env python3
"""Fail-closed contract/source checks for the C11-D semantic review record V1."""
from __future__ import annotations
import hashlib
import json
import sys
import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REVIEW_PATH = ROOT / "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_SOURCE_SEMANTIC_REVIEW_V1.json"
SCHEMA_PATH = ROOT / "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_SOURCE_SEMANTIC_REVIEW_SCHEMA_V1.json"
PROPOSAL_PATH = ROOT / "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_SEMANTIC_BINDING_PROPOSAL_V1.json"
CAPABILITY_PATH = ROOT / "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_CAPABILITY_MATRIX_V1.json"
C11C_PATH = ROOT / "release/C11C_FREEZE_PACKAGE_MANIFEST.json"
V2C_PATH = ROOT / "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2C_SOURCE_FRAME_RUNTIME_RECEIPT_V1.json"

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

class SourceSemanticReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.review = json.loads(REVIEW_PATH.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.proposal = json.loads(PROPOSAL_PATH.read_text(encoding="utf-8"))
        cls.capability = json.loads(CAPABILITY_PATH.read_text(encoding="utf-8"))
        cls.source_by_path = {p["path"]: p["sha256"] for p in cls.review["source_pins"]}
        cls.rows = {r["challenge_id"]: r for r in cls.review["selector_reviews"]}

    def test_01_contract_schema_identifier(self):
        self.assertEqual(self.review["schema"], "C11-D-RENDERER-CHALLENGE-VISUAL-PAYLOAD-SOURCE-SEMANTIC-REVIEW-CONTRACT-V1")

    def test_02_contract_status_is_review_not_approval(self):
        self.assertEqual(self.review["status"], "SOURCE_REVIEW_COMPLETE_BINDINGS_NOT_APPROVED")

    def test_03_proposal_contract_pin_matches_file(self):
        expected = "d37cb74f360e19e664b94673bbf4b95462cad6e681a08215a95f4565c6e810aa"
        self.assertEqual(sha(PROPOSAL_PATH), expected)
        self.assertEqual(self.review["source_authority"]["semantic_binding_proposal_contract_sha256"], expected)

    def test_04_capability_contract_pin_matches_file(self):
        expected = "3b4375957da12d16a6c7f652c1ba2536ce1a819b781b68b15e5dd3f0ee4bda75"
        self.assertEqual(sha(CAPABILITY_PATH), expected)
        self.assertEqual(self.review["source_authority"]["capability_matrix_contract_sha256"], expected)

    def test_05_frozen_c11c_manifest_pin_matches_file(self):
        expected = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
        self.assertEqual(sha(C11C_PATH), expected)
        self.assertEqual(self.review["source_authority"]["frozen_c11c_manifest_sha256"], expected)

    def test_06_v2c_contract_pin_matches_file(self):
        expected = "6d3c59214edbdd917cf63fe9ca4859edb6968d503368ec84e867bdd56a8df74c"
        self.assertEqual(sha(V2C_PATH), expected)
        self.assertEqual(self.review["source_authority"]["v2c_runtime_receipt_contract_sha256"], expected)

    def test_07_schema_contract_shape(self):
        self.assertEqual(self.schema["properties"]["review_summary"]["properties"]["approved_bindings"]["const"], 0)
        self.assertEqual(self.schema["properties"]["selector_reviews"]["maxItems"], 9)
        self.assertEqual(self.schema["properties"]["custom_data_candidate_reviews"]["maxItems"], 6)

    def test_08_exact_nine_selector_reviews(self):
        self.assertEqual(len(self.review["selector_reviews"]), 9)

    def test_09_canonical_selector_order(self):
        self.assertEqual([r["challenge_id"] for r in self.review["selector_reviews"]], [f"CHALLENGE_{i:03}" for i in range(1, 10)])

    def test_10_selector_ids_are_unique(self):
        ids = [r["challenge_id"] for r in self.review["selector_reviews"]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_11_each_review_row_is_backed_by_the_proposal(self):
        p = {r["challenge_id"]: r for r in self.proposal["selector_semantics"]}
        self.assertEqual(set(p), set(self.rows))
        for challenge_id, row in self.rows.items():
            self.assertEqual(row["challenge_source_path"], p[challenge_id]["challenge_source_path"])
            self.assertEqual(row["challenge_source_sha256"], p[challenge_id]["challenge_source_sha256"])
            self.assertEqual(row["mechanic_source_path"], p[challenge_id]["mechanic_source_path"])
            self.assertEqual(row["mechanic_source_sha256"], p[challenge_id]["mechanic_source_sha256"])

    def test_12_all_nine_bindings_remain_unauthorized(self):
        self.assertTrue(all(r["binding_authorized"] is False for r in self.review["selector_reviews"]))

    def test_13_all_nine_renderer_projections_remain_unapproved(self):
        self.assertTrue(all(r["renderer_projection_approved"] is False for r in self.review["selector_reviews"]))

    def test_14_three_static_target_candidates_are_identified(self):
        rows = [r for r in self.review["selector_reviews"] if r["proposed_binding"]["candidate_custom_data_field"] is None]
        self.assertEqual({r["challenge_id"] for r in rows}, {"CHALLENGE_001", "CHALLENGE_002", "CHALLENGE_004"})

    def test_15_challenge_001_duplicate_target_authority_is_explicit(self):
        row = self.rows["CHALLENGE_001"]
        self.assertIn("DUPLICATE_TARGET_AUTHORITY", row["review_disposition"])
        self.assertIn("does not read presentation.static_target_position", row["runtime_relation"])

    def test_16_challenge_002_coordinate_space_remains_undeclared(self):
        row = self.rows["CHALLENGE_002"]
        self.assertIn("UNDECLARED_COORDINATE_SPACE", row["review_disposition"])
        self.assertIn("UNDECLARED_IN_CHALLENGE_SOURCE", row["units_and_coordinate_space"])

    def test_17_pilot_target_x_is_scalar_only(self):
        row = self.rows["CHALLENGE_003"]
        self.assertEqual(row["proposed_binding"]["semantic_type"], "float")
        self.assertEqual(row["coordinate_space"], "PILOT_0X100")
        self.assertIn("Never invent Y", row["missing_value_behavior"])
        self.assertIn("not directly seed-sensitive", row["seed_expectation"])

    def test_18_challenge_004_v1_regression_is_locked(self):
        row = self.rows["CHALLENGE_004"]
        self.assertIn("V1_REGRESSION_ONLY", row["review_disposition"])
        self.assertIn("byte-for-byte unchanged", row["remaining_gate"])

    def test_19_hit_target_position_is_per_run_constant(self):
        row = self.rows["CHALLENGE_005"]
        self.assertIn("PER_RUN_CONSTANT_VECTOR", row["review_disposition"])
        self.assertIn("_target_prime", row["runtime_relation"])
        self.assertIn("STREAM_HIT_TARGET_OFFSET", row["sampling_lifecycle"])

    def test_20_catch_target_position_is_per_frame_and_separate(self):
        row = self.rows["CHALLENGE_006"]
        self.assertIn("PER_FRAME_TARGET_VECTOR", row["review_disposition"])
        self.assertIn("p_c", row["runtime_relation"])
        self.assertIn("p_t", row["runtime_relation"])

    def test_21_find_target_position_is_separate_from_scanner(self):
        row = self.rows["CHALLENGE_007"]
        self.assertIn("p_scan", row["runtime_relation"])
        self.assertIn("p_target", row["runtime_relation"])
        self.assertIn("distractor topology", row["missing_value_behavior"])

    def test_22_choose_active_selection_is_integer_index(self):
        row = self.rows["CHALLENGE_008"]
        self.assertEqual(row["proposed_binding"]["semantic_type"], "int")
        self.assertIn("index", row["source_semantics"])
        self.assertIn("TIMEBASE_CONFLICT", row["review_disposition"])

    def test_23_count_displayed_count_is_integer_and_position_derived(self):
        row = self.rows["CHALLENGE_009"]
        self.assertEqual(row["proposed_binding"]["semantic_type"], "int")
        self.assertIn("mathematically encoded in primary position", row["runtime_relation"])
        self.assertIn("TIMEBASE_CONFLICT", row["review_disposition"])

    def test_24_exact_six_custom_data_candidate_rows(self):
        self.assertEqual(len(self.review["custom_data_candidate_reviews"]), 6)
        self.assertEqual([(r["challenge_id"], r["field"]) for r in self.review["custom_data_candidate_reviews"]], [
            ("CHALLENGE_003", "target_x"),
            ("CHALLENGE_005", "target_position"),
            ("CHALLENGE_006", "target_position"),
            ("CHALLENGE_007", "target_position"),
            ("CHALLENGE_008", "active_selection"),
            ("CHALLENGE_009", "displayed_count"),
        ])

    def test_25_custom_data_candidates_all_remain_unapproved(self):
        self.assertTrue(all("NOT_APPROVED" in row["review_disposition"] for row in self.review["custom_data_candidate_reviews"]))
        self.assertEqual(self.review["review_summary"]["approved_custom_data_bindings"], 0)

    def test_26_whole_custom_data_map_is_prohibited(self):
        self.assertEqual(self.review["custom_data_policy"]["whole_map_serialization"], "PROHIBITED")
        self.assertEqual(self.review["custom_data_policy"]["unlisted_custom_data"], "NEVER_PROJECT_BY_DEFAULT")

    def test_27_six_base_snapshot_fields_remain_review_only(self):
        self.assertEqual([r["field"] for r in self.review["base_snapshot_fields"]], ["position", "rotation", "scale", "opacity", "texture_index", "variant_id"])
        self.assertTrue(all("NOT_APPROVED" in r["status"] for r in self.review["base_snapshot_fields"]))

    def test_28_timebase_conflicts_are_preserved(self):
        t = self.review["shared_temporal_policy"]
        self.assertEqual(t["challenge_008_declared_total_seconds"], 11)
        self.assertEqual(t["challenge_008_phase_sum_seconds"], 12)
        self.assertEqual(t["challenge_009_declared_total_seconds"], 11)
        self.assertEqual(t["challenge_009_phase_sum_seconds"], 12)
        self.assertEqual(t["decision"], "UNRESOLVED_NO_PRECEDENCE_INFERRED")
        self.assertIs(t["challenge_json_edits_performed"], False)

    def test_29_source_pin_count_and_uniqueness(self):
        self.assertEqual(len(self.review["source_pins"]), 81)
        self.assertEqual(len(self.source_by_path), 81)
        self.assertTrue(all(len(p["sha256"]) == 64 for p in self.review["source_pins"]))

    def test_30_all_eighty_one_source_pins_match_checkout(self):
        for rel, expected in self.source_by_path.items():
            path = ROOT / rel
            self.assertTrue(path.is_file(), f"missing source pin: {rel}")
            self.assertEqual(sha(path), expected, rel)

    def test_31_row_source_pins_exist_in_eighty_one_pin_set(self):
        for row in self.review["selector_reviews"]:
            self.assertEqual(self.source_by_path[row["challenge_source_path"]], row["challenge_source_sha256"])
            self.assertEqual(self.source_by_path[row["mechanic_source_path"]], row["mechanic_source_sha256"])

    def test_32_runtime_bridge_signature_and_dual_video_binding_are_source_grounded(self):
        bridge = (ROOT / "core/execution/ChallengeRuntimeBridge.gd").read_text(encoding="utf-8-sig")
        self.assertIn("static func run_effective_pipeline(legacy_config: Dictionary)", bridge)
        self.assertIn("if video_binding is Dictionary", bridge)
        self.assertIn("var video_profile_id := str(video_binding)", bridge)
        self.assertIn("VideoProfileRegistry.get_profile(video_profile_id)", bridge)

    def test_33_frame_snapshot_actual_field_types_are_source_grounded(self):
        frame = (ROOT / "core/data/FrameSnapshot.gd").read_text(encoding="utf-8-sig")
        for line in ["var position: Vector2", "var rotation: float", "var scale: Vector2", "var opacity: float", "var texture_index: int", "var variant_id: int", "var custom_data: Dictionary = {}"]:
            self.assertIn(line, frame)

    def test_34_governance_locks_and_v2b_boundary_are_preserved(self):
        g = self.review["governance_locks"]
        self.assertEqual(g["renderer"], "OFF")
        self.assertIs(g["media_created"], False)
        self.assertIs(g["candidate_input_admissible"], False)
        self.assertIs(g["seed_domains_complete_for_candidate_input"], False)
        self.assertEqual(g["master_seed"], "NOT_ADOPTED")
        self.assertEqual(g["D4.8"], "BLOCKED")
        self.assertEqual(g["D9.10"], "PREPARE_ONLY")
        self.assertEqual(g["D9.14"], "BLOCKED")
        self.assertEqual(g["D9.16"], "BLOCKED")
        self.assertEqual(g["D9.17"], "BLOCKED_NO_GO")
        self.assertEqual(g["D10"], "BLOCKED_FOR_PROMOTION")
        self.assertEqual(g["release_authority"], "NONE")
        self.assertEqual(g["visual_seed_sensitivity"], "NOT_TESTED")
        self.assertEqual(self.review["next_gate"]["implementation_status"], "NOT_DESIGNED_IN_THIS_INCREMENT")

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(SourceSemanticReviewTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful() or result.testsRun != 34:
        sys.exit(1)
    print("C11D_SOURCE_SEMANTIC_REVIEW_TESTS_PASS=34/34")
