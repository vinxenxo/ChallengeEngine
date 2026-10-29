from __future__ import annotations
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PACKET_PATH = ROOT / "docs/current/d/C11D_PHASE_R_OPERATOR_POLICY_DECISION_PACKET_20261029_V1.json"
REVIEW_PATH = ROOT / "docs/current/d/C11D_PHASE_R_OPERATOR_POLICY_DECISION_PACKET_20261029_V1.md"
SCHEMA_PATH = ROOT / "definitions/c11d/review/D_RENDERER_PHASE_R_OPERATOR_POLICY_DECISION_PACKET_SCHEMA_V1.json"
Q_MATRIX_PATH = ROOT / "docs/current/d/C11D_PHASE_Q_SEMANTIC_POLICY_DEPENDENCY_MATRIX_20261029_V1.json"
EXPECTED_SELECTORS = [
    "CHALLENGE_003.target_x", "CHALLENGE_005.target_position", "CHALLENGE_006.target_position",
    "CHALLENGE_007.target_position", "CHALLENGE_008.active_selection", "CHALLENGE_009.displayed_count"
]
EXPECTED_DECISIONS = [
    "R-01-TIMEBASE-SAMPLING", "R-02-SPATIAL-MAPPING", "R-03-PILOT-SCALAR-X-AND-PRESENTATION-Y",
    "R-04-VISIBILITY-AND-REGION-OWNERSHIP", "R-05-ASSET-GEOMETRY-ANCHOR-CROP-ROUNDING",
    "R-06-INVALID-DATA-AND-TRACK-INTEGRITY", "R-07-SEMANTIC-VISUAL-OWNERSHIP",
    "R-08-CHALLENGE-008-DURATION-CONFLICT", "R-09-CHALLENGE-009-DURATION-AND-COUNT-ROLE"
]
EXPECTED_PINS = {
    "release/C11C_FREEZE_PACKAGE_MANIFEST.json": "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953",
    "AGENTS.md": "e1501c3ef2c3ebf8cd025df152e2659f36bdb84f149ce401f331ac4030305412",
    ".continue/rules/CONTINUE.md": "cf96ba6de31018e8a807687822f968f90530c25ed84220e5e4f37ed599725b1f",
    "docs/current/d/C11D_PHASE_P_SOURCE_FRAME_PROVENANCE_ACCEPTANCE_REVIEW_20261029_V1.md": "d75b13453fac89b01eb806aaff162771d33d7ff15d88d6f81c2825cf8bcc9132",
    "docs/current/d/C11D_ENGINEERING_PHASE_LEDGER_20261029_V3.md": "be6edb1dd6ffd2131e030505d2553e95f542dca278f21a46ea3a8ee2d301d06a",
    "docs/current/d/C11D_FULL_CONTEXT_CONTINUITY_CHECKPOINT_20261029_V26.md": "66f0f16c6dbeb758c5cb9d5b648f3f984a56246c449a5c176eb6226dd729d669",
    "prompts/C11D_D_FINAL_CLOSEOUT_HANDOVER_MASTER_PROMPT_20261029_V26.md": "277967b7cba738b833a22a598e705e6309f087a6db2132c6dd7f65267aa2d2d6",
    "prompts/C11D_D_FINAL_CLOSEOUT_START_PROMPT_20261029_V26.md": "c158bc5e841a4009529092c200df42bcd587e387bfdcdfb96d703bffce4b0c9f",
    "definitions/c11d/production/D_RENDERER_PHASE_P_SOURCE_VALUE_VS_FRAME_VALUE_PROVENANCE_CONTRACT_V1.json": "a237e950953e70406cecd4ef94460eb8617482d1d27feebce03e3ef2f6afbb6a",
    "docs/current/d/C11D_PHASE_Q_SEMANTIC_POLICY_DEPENDENCY_REVIEW_20261029_V1.md": "4cffdb3ef7edb3f4d201391b8156e4691ad0b98fdad2859703bcc20f589dd62f",
    "docs/current/d/C11D_PHASE_Q_SEMANTIC_POLICY_DEPENDENCY_MATRIX_20261029_V1.json": "de2d5e548e00442ee8f15ca7514744b402c6400b4a8497b2b6f6671d29b00390",
    "definitions/c11d/review/D_RENDERER_PHASE_Q_SEMANTIC_POLICY_DEPENDENCY_MATRIX_SCHEMA_V1.json": "cca024de2dd6a01805f431d3b140c77dce12bf781d12aee11df35fd426af910b",
    "tools/c11d/d9/test_d_renderer_phase_q_semantic_policy_dependency_review_20261029.py": "6cfa58e7f442d866d172a4ec5ee6d2e091ca0e6ff2c788cb776bf05e5e0aff1a",
    "docs/current/d/C11D_PHASE_Q_VERIFIER_RECOVERY_AND_REVIEW_CLOSEOUT_20261029_2175920e62954eb0b0fba64555870767.md": "5a8e62f9d38bbf31cfb64066fec57f17d2f931da2349f0078b7ea62ed77851d1",
}
def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

class PhaseROperatorPolicyPacketTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packet = json.loads(PACKET_PATH.read_text(encoding="utf-8"))
        cls.review = REVIEW_PATH.read_text(encoding="utf-8")
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.q_matrix = json.loads(Q_MATRIX_PATH.read_text(encoding="utf-8"))
        cls.decisions = {x["decision_id"]: x for x in cls.packet["decisions"]}
        cls.candidates = {x["selector"]: x for x in cls.packet["candidate_semantics"]}

    def test_01_packet_schema_identifier(self): self.assertEqual(self.packet["schema"], "C11D-PHASE-R-OPERATOR-POLICY-DECISION-PACKET-V1")
    def test_02_packet_is_preparation_only(self): self.assertEqual(self.packet["status"], "PREPARED_READ_ONLY_DECISION_PACKET_NOT_ADJUDICATED")
    def test_03_mode_read_only(self): self.assertEqual(self.packet["mode"], "READ_ONLY_DECISION_PREPARATION")
    def test_04_scope_does_not_modify_production(self): self.assertFalse(self.packet["scope"]["production_source_modification"]); self.assertFalse(self.packet["scope"]["challenge_definition_modification"])
    def test_05_no_runtime_or_godot(self): self.assertFalse(self.packet["scope"]["runtime_reexecution"]); self.assertFalse(self.packet["scope"]["godot_invoked"])
    def test_06_no_renderer_payload_or_media(self): self.assertFalse(self.packet["scope"]["renderer_dispatch_invoked"]); self.assertFalse(self.packet["scope"]["payload_materialized"]); self.assertFalse(self.packet["scope"]["media_created"])
    def test_07_operator_decisions_not_recorded(self): self.assertFalse(self.packet["scope"]["operator_decisions_recorded"])
    def test_08_exact_six_unique_selectors(self): self.assertEqual(self.packet["scope"]["selectors"], EXPECTED_SELECTORS); self.assertEqual(len(set(self.packet["scope"]["selectors"])), 6)
    def test_09_exact_nine_decision_ids(self): self.assertEqual(list(self.decisions), EXPECTED_DECISIONS)
    def test_10_decisions_are_unselected(self): self.assertTrue(all(d["status"] in ("UNDECIDED_NO_POLICY_AUTHORIZED", "BLOCKED_EXPLICIT_AUTHORITY_REQUIRED") for d in self.packet["decisions"]))
    def test_11_all_decisions_have_authority(self): self.assertTrue(all(len(d["authority_required"]) > 20 for d in self.packet["decisions"]))
    def test_12_all_options_explain_consequences(self): self.assertTrue(all(all(o.get("id") and o.get("definition") and o.get("consequence") for o in d["options"]) for d in self.packet["decisions"]))
    def test_13_every_decision_has_future_tests(self): self.assertTrue(all(len(d["future_tests"]) >= 4 for d in self.packet["decisions"]))
    def test_14_keep_blocked_is_a_live_option(self): self.assertTrue(all(any("KEEP_BLOCKED" in o["id"] or o["id"] == "RETAIN_BLOCK" or o["id"] == "KEEP_UNDECIDED" or o["id"] == "REJECT_MAPPING_OR_KEEP_BLOCKED" for o in d["options"]) for d in self.packet["decisions"]))
    def test_15_default_is_no_adoption(self): self.assertEqual(self.packet["authority_and_decision_rules"]["default_when_unresolved"], "KEEP_BLOCKED_NO_POLICY_ADOPTION")
    def test_16_no_implicit_acceptance(self): self.assertTrue(self.packet["authority_and_decision_rules"]["no_implicit_acceptance"])
    def test_17_pilot_remains_scalar(self): self.assertIn("float scalar", self.candidates["CHALLENGE_003.target_x"]["accepted_semantics"])
    def test_18_scalar_y_not_source_data(self): self.assertIn("Any source Y", self.candidates["CHALLENGE_003.target_x"]["not_authorized"])
    def test_19_hit_target_constant(self): self.assertIn("constant per run", self.candidates["CHALLENGE_005.target_position"]["accepted_semantics"])
    def test_20_catch_target_per_frame(self): self.assertIn("Per-frame", self.candidates["CHALLENGE_006.target_position"]["accepted_semantics"])
    def test_21_find_target_per_frame_and_telemetry_excluded(self): self.assertIn("Per-frame", self.candidates["CHALLENGE_007.target_position"]["accepted_semantics"]); self.assertIn("close_calls", self.candidates["CHALLENGE_007.target_position"]["not_authorized"])
    def test_22_displayed_count_distinct_from_target_count(self): self.assertIn("distinct from target_count", self.candidates["CHALLENGE_009.displayed_count"]["accepted_semantics"])
    def test_23_ch008_conflict_is_11_vs_12(self): self.assertEqual(self.decisions["R-08-CHALLENGE-008-DURATION-CONFLICT"]["conflict"]["declared_total_duration_seconds"], 11); self.assertEqual(self.decisions["R-08-CHALLENGE-008-DURATION-CONFLICT"]["conflict"]["phase_duration_sum_seconds"], 12)
    def test_24_ch009_conflict_is_11_vs_12(self): self.assertEqual(self.decisions["R-09-CHALLENGE-009-DURATION-AND-COUNT-ROLE"]["conflict"]["declared_total_duration_seconds"], 11); self.assertEqual(self.decisions["R-09-CHALLENGE-009-DURATION-AND-COUNT-ROLE"]["conflict"]["phase_duration_sum_seconds"], 12)
    def test_25_both_duration_conflicts_remain_blockers(self): self.assertEqual(self.decisions["R-08-CHALLENGE-008-DURATION-CONFLICT"]["conflict"]["status"], "BLOCKER_NO_CORRECTION_INFERRED"); self.assertEqual(self.decisions["R-09-CHALLENGE-009-DURATION-AND-COUNT-ROLE"]["conflict"]["status"], "BLOCKER_NO_CORRECTION_INFERRED")
    def test_26_policy_includes_no_interpolation_or_extrapolation(self): self.assertTrue(any("No interpolation or extrapolation" in x for x in self.decisions["R-01-TIMEBASE-SAMPLING"]["non_negotiables"]))
    def test_27_spatial_mapping_not_approved(self): self.assertEqual(self.decisions["R-02-SPATIAL-MAPPING"]["status"], "UNDECIDED_NO_POLICY_AUTHORIZED")
    def test_28_scalar_x_and_y_are_separate_decisions(self): self.assertIn("two explicit decisions", self.decisions["R-03-PILOT-SCALAR-X-AND-PRESENTATION-Y"]["options"][0]["consequence"])
    def test_29_visibility_not_inferred_from_close_calls(self): self.assertTrue(any("close_calls" in x for x in self.decisions["R-04-VISIBILITY-AND-REGION-OWNERSHIP"]["non_negotiables"]))
    def test_30_rounding_must_be_exact(self): self.assertTrue(any("rounding" in x.lower() for x in self.decisions["R-05-ASSET-GEOMETRY-ANCHOR-CROP-ROUNDING"]["non_negotiables"]))
    def test_31_invalid_data_no_silent_clamping(self): self.assertTrue(any("No silent coercion or clamping" in x for x in self.decisions["R-06-INVALID-DATA-AND-TRACK-INTEGRITY"]["non_negotiables"]))
    def test_32_no_raw_candidate_or_whole_custom_data_serialization(self): self.assertFalse(self.packet["governance"]["whole_custom_data_serialization_allowed"]); self.assertTrue(any("raw" in x.lower() for x in self.decisions["R-06-INVALID-DATA-AND-TRACK-INTEGRITY"]["non_negotiables"]))
    def test_33_governance_renderer_off(self): self.assertEqual(self.packet["governance"]["renderer"], "OFF")
    def test_34_governance_bindings_zero(self): self.assertEqual(self.packet["governance"]["approved_bindings"], 0); self.assertEqual(self.packet["governance"]["approved_custom_data_bindings"], 0); self.assertEqual(self.packet["governance"]["approved_renderer_projection_bindings"], 0)
    def test_35_governance_release_blocked(self): self.assertEqual(self.packet["governance"]["release_authority"], "NONE"); self.assertFalse(self.packet["governance"]["freeze_eligible"])
    def test_36_c11c_remains_authoritative(self): self.assertIn("immutable", self.packet["future_gate_requirements"]["C11C"])
    def test_37_phase_q_closeout_pin_is_current(self): self.assertEqual(self.packet["phase_q_closeout"]["sha256"], EXPECTED_PINS["docs/current/d/C11D_PHASE_Q_VERIFIER_RECOVERY_AND_REVIEW_CLOSEOUT_20261029_2175920e62954eb0b0fba64555870767.md"])
    def test_38_phase_q_matrix_selector_set_matches(self): self.assertEqual([c["selector"] for c in self.q_matrix["candidates"]], EXPECTED_SELECTORS)
    def test_39_phase_q_conflicts_unmodified(self):
        for idx in (4,5):
            self.assertEqual(self.q_matrix["candidates"][idx]["timebase_conflict"]["declared_total_duration_seconds"],11)
            self.assertEqual(self.q_matrix["candidates"][idx]["timebase_conflict"]["phase_duration_sum_seconds"],12)
    def test_40_phase_q_governance_unchanged_in_inventory(self): self.assertEqual(self.q_matrix["governance"]["renderer"], "OFF"); self.assertEqual(self.q_matrix["governance"]["approved_bindings"], 0)
    def test_41_review_contains_all_decision_ids(self): self.assertTrue(all(x in self.review for x in EXPECTED_DECISIONS))
    def test_42_review_preserves_timing_conflict(self): self.assertIn("11 s", self.review); self.assertIn("12 s", self.review)
    def test_43_schema_identifier_matches_packet(self): self.assertEqual(self.schema["properties"]["schema"]["const"], self.packet["schema"])
    def test_44_schema_requires_nine_decisions(self): self.assertEqual(self.schema["properties"]["decisions"]["minItems"], 9); self.assertEqual(self.schema["properties"]["decisions"]["maxItems"], 9)
    def test_45_schema_forces_governance_locks(self): self.assertEqual(self.schema["properties"]["governance"]["properties"]["renderer"]["const"], "OFF"); self.assertEqual(self.schema["properties"]["governance"]["properties"]["approved_bindings"]["const"], 0)
    def test_46_all_pinned_sources_exist_and_match(self):
        for rel, expected in EXPECTED_PINS.items():
            p = ROOT / rel
            self.assertTrue(p.is_file(), rel)
            self.assertEqual(sha(p), expected, rel)
    def test_47_manifest_size_unchanged(self): self.assertEqual((ROOT/"release/C11C_FREEZE_PACKAGE_MANIFEST.json").stat().st_size, 796318)
    def test_48_phase_r_exit_criteria_nonempty(self): self.assertGreaterEqual(len(self.packet["phase_r_exit_criteria"]), 6)
    def test_49_next_gate_does_not_auto_adopt(self): self.assertTrue(self.packet["next_gate"]["start_condition"].startswith("Phase R packet is accepted")); self.assertIn("No policy is adopted", self.packet["next_gate"]["start_condition"])
    def test_50_static_files_are_readable(self): self.assertTrue(PACKET_PATH.is_file()); self.assertTrue(REVIEW_PATH.is_file()); self.assertTrue(SCHEMA_PATH.is_file())

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(PhaseROperatorPolicyPacketTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    count = result.testsRun
    if result.wasSuccessful() and count == 50:
        print(f"PHASE_R_OPERATOR_POLICY_PACKET_TESTS={count}/{count}")
        raise SystemExit(0)
    print(f"PHASE_R_OPERATOR_POLICY_PACKET_TESTS=FAIL; passed={count-len(result.failures)-len(result.errors)}; total={count}")
    raise SystemExit(1)
