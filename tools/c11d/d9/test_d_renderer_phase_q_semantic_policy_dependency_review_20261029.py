#!/usr/bin/env python3
"""Read-only Phase Q dependency review tests; no Godot/runtime/payload work."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MATRIX_PATH = ROOT / "docs/current/d/C11D_PHASE_Q_SEMANTIC_POLICY_DEPENDENCY_MATRIX_20261029_V1.json"
REVIEW_PATH = ROOT / "docs/current/d/C11D_PHASE_Q_SEMANTIC_POLICY_DEPENDENCY_REVIEW_20261029_V1.md"
PHASE_P_CONTRACT = ROOT / "definitions/c11d/production/D_RENDERER_PHASE_P_SOURCE_VALUE_VS_FRAME_VALUE_PROVENANCE_CONTRACT_V1.json"
SEMANTIC_DECISION = ROOT / "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_SEMANTIC_DECISION_RECORD_V1.json"
COORDINATE_PROPOSAL = ROOT / "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_COORDINATE_POLICY_PROPOSAL_V1.json"
VISIBILITY_PROPOSAL = ROOT / "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_PROPOSAL_V1.json"
TEMPORAL_PROPOSAL = ROOT / "definitions/c11d/production/D_RENDERER_CHALLENGE_TEMPORAL_ALIGNMENT_POLICY_PROPOSAL_V1.json"
DELIVERY_TIMEBASE = ROOT / "definitions/c11d/production/D_RENDERER_DELIVERY_TIMEBASE_PROJECTION_V1.json"
POLICY_DOCKET = ROOT / "definitions/c11d/production/D_RENDERER_POLICY_DECISION_DOCKET_V1.json"
EXPECTED_SELECTORS = [
    "CHALLENGE_003.target_x", "CHALLENGE_005.target_position",
    "CHALLENGE_006.target_position", "CHALLENGE_007.target_position",
    "CHALLENGE_008.active_selection", "CHALLENGE_009.displayed_count",
]
EXPECTED_AUTH_HASHES = {
    "release/C11C_FREEZE_PACKAGE_MANIFEST.json": "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953",
    "definitions/c11d/production/D_RENDERER_PHASE_P_SOURCE_VALUE_VS_FRAME_VALUE_PROVENANCE_CONTRACT_V1.json": "a237e950953e70406cecd4ef94460eb8617482d1d27feebce03e3ef2f6afbb6a",
    "docs/current/d/C11D_PHASE_P_SOURCE_FRAME_PROVENANCE_ACCEPTANCE_REVIEW_20261029_V1.md": "d75b13453fac89b01eb806aaff162771d33d7ff15d88d6f81c2825cf8bcc9132",
    "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_SEMANTIC_BINDING_PROPOSAL_V1.json": "d37cb74f360e19e664b94673bbf4b95462cad6e681a08215a95f4565c6e810aa",
    "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_SEMANTIC_DECISION_RECORD_V1.json": "cc3550cd4d13f228ec9b3d51eeaa199505c5975b42882fb06ba3e83c4a000e90",
    "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_COORDINATE_POLICY_PROPOSAL_V1.json": "44c1ec6507988023b7cd20cdcc8e0e722c99af610d9be02a6d658ce9b07e9f57",
    "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_PROPOSAL_V1.json": "f3afe4d7d08791c7634c9851500ca551438870babc195db1908440b93e740692",
    "definitions/c11d/production/D_RENDERER_CHALLENGE_TEMPORAL_ALIGNMENT_POLICY_PROPOSAL_V1.json": "39f6f979a5d8b189cbb3a375b0c33ed7fdb3f2b9bc59fcb587f31a6c65ede5a6",
    "definitions/c11d/production/D_RENDERER_DELIVERY_TIMEBASE_PROJECTION_V1.json": "4a76bc9613fbc4690f7a2bb3cc047ec5f6334444c4eccefd34fedccb1a830241",
    "definitions/c11d/production/D_RENDERER_POLICY_DECISION_DOCKET_V1.json": "e008217bd57303b638e13329d21e5ae56ee3b4efef790566e3702c89ee41a83f",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class PhaseQDependencyReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
        cls.review = REVIEW_PATH.read_text(encoding="utf-8")
        cls.candidates = cls.matrix["candidates"]
        cls.by_selector = {c["selector"]: c for c in cls.candidates}

    def test_01_matrix_schema_id(self): self.assertEqual(self.matrix["schema"], "C11D-PHASE-Q-SEMANTIC-POLICY-DEPENDENCY-MATRIX-V1")
    def test_02_matrix_status_is_prepared_only(self): self.assertEqual(self.matrix["status"], "PREPARED_READ_ONLY_POLICY_DEPENDENCY_REVIEW_NOT_OPERATOR_POLICY_APPROVAL")
    def test_03_exact_six_selectors(self): self.assertEqual([c["selector"] for c in self.candidates], EXPECTED_SELECTORS)
    def test_04_scope_is_read_only(self): self.assertTrue(self.matrix["scope"]["read_only"]); self.assertFalse(self.matrix["scope"]["project_source_modification"])
    def test_05_no_runtime_in_phase_q(self): self.assertFalse(self.matrix["scope"]["runtime_reexecution"]); self.assertFalse(self.matrix["scope"]["renderer_dispatch_invoked"])
    def test_06_no_media_or_payload(self): self.assertFalse(self.matrix["scope"]["media_created"]); self.assertFalse(self.matrix["scope"]["payload_materialized"])
    def test_07_frozen_manifest_pin(self): self.assertEqual(self.matrix["source_authority"][0]["sha256"], EXPECTED_AUTH_HASHES["release/C11C_FREEZE_PACKAGE_MANIFEST.json"])
    def test_08_runtime_report_pin(self): self.assertEqual(self.matrix["phase_p_runtime_evidence"]["report_sha256"], "9686240a0e2caa46f05cea4ca2c8fcaaa1499d006ac6ac75d128137693fc2ef7")
    def test_09_runtime_selector_counts(self): self.assertEqual(self.matrix["phase_p_runtime_evidence"]["selectors"], "6/6"); self.assertEqual(self.matrix["phase_p_runtime_evidence"]["godot_runtime_processes"], "12/12")
    def test_10_runtime_did_not_serialize_values(self): self.assertFalse(self.matrix["phase_p_runtime_evidence"]["actual_candidate_values_serialized"]); self.assertFalse(self.matrix["phase_p_runtime_evidence"]["whole_custom_data_map_serialized"])
    def test_11_all_candidates_binding_unauthorized(self): self.assertTrue(all(not c["current_binding_authorized"] for c in self.candidates))
    def test_12_all_candidates_projection_unauthorized(self): self.assertTrue(all(not c["current_renderer_projection_authorized"] for c in self.candidates))
    def test_13_pilot_remains_scalar(self): self.assertEqual(self.by_selector["CHALLENGE_003.target_x"]["semantic_type"], "float"); self.assertEqual(self.by_selector["CHALLENGE_003.target_x"]["track_kind"], "PER_FRAME_SCALAR")
    def test_14_pilot_y_is_presentation_only(self): self.assertTrue(any("y_logical=480" in x for x in self.by_selector["CHALLENGE_003.target_x"]["proposals_not_approved"]))
    def test_15_hit_target_is_per_run_constant(self): self.assertEqual(self.by_selector["CHALLENGE_005.target_position"]["track_kind"], "PER_RUN_CONSTANT_REPEATED_PER_FRAME")
    def test_16_catch_target_is_per_frame(self): self.assertEqual(self.by_selector["CHALLENGE_006.target_position"]["track_kind"], "PER_FRAME_VECTOR")
    def test_17_find_target_is_per_frame(self): self.assertEqual(self.by_selector["CHALLENGE_007.target_position"]["track_kind"], "PER_FRAME_VECTOR")
    def test_18_find_excludes_distractor_telemetry(self): self.assertIn("distractor topology", self.by_selector["CHALLENGE_007.target_position"]["excluded_data"])
    def test_19_choose_remains_blocked(self): self.assertTrue(self.by_selector["CHALLENGE_008.active_selection"]["semantic_definition_status"].startswith("BLOCKED_"))
    def test_20_count_remains_blocked(self): self.assertTrue(self.by_selector["CHALLENGE_009.displayed_count"]["semantic_definition_status"].startswith("BLOCKED_"))
    def test_21_choose_11_vs_12_preserved(self): self.assertEqual(self.by_selector["CHALLENGE_008.active_selection"]["timebase_conflict"]["phase_duration_sum_seconds"], 12); self.assertEqual(self.by_selector["CHALLENGE_008.active_selection"]["timebase_conflict"]["declared_total_duration_seconds"], 11)
    def test_22_count_11_vs_12_preserved(self): self.assertEqual(self.by_selector["CHALLENGE_009.displayed_count"]["timebase_conflict"]["phase_duration_sum_seconds"], 12); self.assertEqual(self.by_selector["CHALLENGE_009.displayed_count"]["timebase_conflict"]["declared_total_duration_seconds"], 11)
    def test_23_displayed_count_not_target_count(self): self.assertIn("target_count", self.by_selector["CHALLENGE_009.displayed_count"]["primary_track_relation"])
    def test_24_policy_dependencies_inventory(self): self.assertGreaterEqual(len(self.matrix["policy_dependencies"]), 6)
    def test_25_coordinate_proposal_not_approved(self): self.assertIn("PROPOSED_NOT_APPROVED", self.matrix["policy_dependencies"][1]["status"])
    def test_26_visibility_proposal_not_approved(self): self.assertIn("PROPOSED_NOT_APPROVED", self.matrix["policy_dependencies"][2]["status"])
    def test_27_rounding_unresolved(self): self.assertIn("UNRESOLVED", self.matrix["policy_dependencies"][3]["status"])
    def test_28_winning_frame_is_only_temporal_anchor(self): self.assertIn("winning_frame` es el único anclaje temporal", self.review)
    def test_29_close_calls_is_episode_counter(self): self.assertIn("`close_calls` cuenta episodios", self.review)
    def test_30_phase_q_next_gate_is_phase_r(self): self.assertTrue(self.matrix["next_gate"]["name"].startswith("Phase R"))
    def test_31_governance_renderer_off(self): self.assertEqual(self.matrix["governance"]["renderer"], "OFF")
    def test_32_governance_no_bindings(self): self.assertEqual(self.matrix["governance"]["approved_bindings"], 0); self.assertEqual(self.matrix["governance"]["approved_custom_data_bindings"], 0); self.assertEqual(self.matrix["governance"]["approved_renderer_projection_bindings"], 0)
    def test_33_governance_no_release_authority(self): self.assertEqual(self.matrix["governance"]["release_authority"], "NONE"); self.assertFalse(self.matrix["governance"]["freeze_eligible"])
    def test_34_review_contains_all_candidates(self): self.assertTrue(all(s in self.review for s in EXPECTED_SELECTORS))
    def test_35_review_preserves_temporal_conflict(self): self.assertIn("11s", self.review); self.assertIn("12s", self.review)
    def test_36_proposal_semantic_decision_statuses_match(self):
        self.assertTrue(SEMANTIC_DECISION.exists())
        d=json.loads(SEMANTIC_DECISION.read_text(encoding="utf-8"))
        by={f"{x['challenge_id']}.{x['field']}":x for x in d["decisions"]}
        for s in EXPECTED_SELECTORS: self.assertIn(s,by)
        for s in EXPECTED_SELECTORS[:4]: self.assertEqual(by[s]["semantic_decision"],"ACCEPT_SEMANTIC_DEFINITION_FOR_FUTURE_BINDING_SPECIFICATION")
        for s in EXPECTED_SELECTORS[4:]: self.assertEqual(by[s]["semantic_decision"],"BLOCKED_NEEDS_SOURCE_OR_POLICY_DECISION")
    def test_37_coordinate_proposal_scoped_to_four(self):
        d=json.loads(COORDINATE_PROPOSAL.read_text(encoding="utf-8"))
        self.assertEqual(d["status"],"PROPOSED_NOT_APPROVED_OPERATOR_REVIEW_REQUIRED")
        self.assertEqual(d["scope"]["included_challenge_fields"],EXPECTED_SELECTORS[:4])
        self.assertEqual(d["scope"]["excluded_blocked_challenge_fields"],EXPECTED_SELECTORS[4:])
    def test_38_visibility_proposal_scoped_to_four(self):
        d=json.loads(VISIBILITY_PROPOSAL.read_text(encoding="utf-8"))
        self.assertEqual(d["status"],"PROPOSED_NOT_APPROVED_OPERATOR_REVIEW_REQUIRED")
        self.assertEqual(d["scope"]["included_challenge_fields"],EXPECTED_SELECTORS[:4])
        self.assertEqual(d["scope"]["excluded_blocked_challenge_fields"],EXPECTED_SELECTORS[4:])
    def test_39_temporal_proposal_not_global_approval(self):
        d=json.loads(TEMPORAL_PROPOSAL.read_text(encoding="utf-8"))
        self.assertEqual(d["status"],"PROPOSAL_ONLY_NOT_RENDERER_INPUT")
        self.assertIn("NOT_EXECUTED_BY_THIS_CONTRACT",d["policy"]["sampling_rule"])
    def test_40_delivery_timebase_is_preparation_only(self):
        d=json.loads(DELIVERY_TIMEBASE.read_text(encoding="utf-8"))
        self.assertEqual(d["status"],"PREPARATION_ONLY_DELIVERY_TIMEBASE_PROJECTION_NOT_RENDERER_INPUT")
    def test_41_policy_docket_is_not_approved(self):
        d=json.loads(POLICY_DOCKET.read_text(encoding="utf-8"))
        self.assertEqual(d["status"],"PREPARATION_ONLY_DECISION_DOCKET_NOT_APPROVED")
        self.assertEqual(d["locks"]["approved_bindings"],0)
        self.assertEqual(d["locks"]["release_authority"],"NONE")
    def test_42_phase_p_contract_pin_matches_current(self):
        self.assertTrue(PHASE_P_CONTRACT.exists())
        self.assertEqual(sha(PHASE_P_CONTRACT),"a237e950953e70406cecd4ef94460eb8617482d1d27feebce03e3ef2f6afbb6a")
    def test_43_phase_p_acceptance_review_pin_matches(self):
        p=ROOT/"docs/current/d/C11D_PHASE_P_SOURCE_FRAME_PROVENANCE_ACCEPTANCE_REVIEW_20261029_V1.md"
        self.assertTrue(p.exists())
        self.assertEqual(sha(p),"d75b13453fac89b01eb806aaff162771d33d7ff15d88d6f81c2825cf8bcc9132")
    def test_44_authority_pin_list_has_accepted_phase_p(self):
        pins={x["path"]:x["sha256"] for x in self.matrix["source_authority"]}
        self.assertEqual(pins["docs/current/d/C11D_PHASE_P_SOURCE_FRAME_PROVENANCE_ACCEPTANCE_REVIEW_20261029_V1.md"],"d75b13453fac89b01eb806aaff162771d33d7ff15d88d6f81c2825cf8bcc9132")
    def test_45_all_repository_source_authority_pins_match(self):
        for entry in self.matrix["source_authority"]:
            if entry["path"] in ("runtime_evidence/phase_p_provenance_report.json", "release/C11C_FREEZE_PACKAGE_MANIFEST.json"):
                # These two pins are checked by the receipt and the guarded PowerShell apply preflight respectively.
                continue
            path = ROOT / entry["path"]
            self.assertTrue(path.is_file(), entry["path"])
            self.assertEqual(sha(path), entry["sha256"], entry["path"])


if __name__ == "__main__":
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(PhaseQDependencyReviewTests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    count=result.testsRun
    if result.wasSuccessful() and count==45:
        print(f"PHASE_Q_SEMANTIC_POLICY_DEPENDENCY_TESTS={count}/{count}")
        raise SystemExit(0)
    print(f"PHASE_Q_SEMANTIC_POLICY_DEPENDENCY_TESTS=FAIL; passed={count-len(result.failures)-len(result.errors)}; total={count}")
    raise SystemExit(1)
