from __future__ import annotations
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path.cwd()
CONTRACT_PATH = ROOT / "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SAFE_VISUAL_PROJECTION_DESIGN_V1.json"
SCHEMA_PATH = ROOT / "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SAFE_VISUAL_PROJECTION_DESIGN_SCHEMA_V1.json"
RECEIPT_SCHEMA_PATH = ROOT / "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SAFE_PROJECTION_RECEIPT_SCHEMA_V1.json"
MATRIX_PATH = ROOT / "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SEED_TEST_MATRIX_V1.json"

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

CONTRACT = load_json(CONTRACT_PATH)
SCHEMA = load_json(SCHEMA_PATH)
RECEIPT_SCHEMA = load_json(RECEIPT_SCHEMA_PATH)
MATRIX = load_json(MATRIX_PATH)
IDS = [f"CHALLENGE_{i:03d}" for i in range(1, 10)]
BASE_FIELDS = ["position", "rotation", "scale", "opacity", "texture_index", "variant_id"]
CANDIDATE_ROWS = {
    ("CHALLENGE_003", "target_x"), ("CHALLENGE_005", "target_position"),
    ("CHALLENGE_006", "target_position"), ("CHALLENGE_007", "target_position"),
    ("CHALLENGE_008", "active_selection"), ("CHALLENGE_009", "displayed_count"),
}
EXPECTED_INPUTS = {
 "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_CAPABILITY_MATRIX_V1.json": "3b4375957da12d16a6c7f652c1ba2536ce1a819b781b68b15e5dd3f0ee4bda75",
 "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_SEMANTIC_BINDING_PROPOSAL_V1.json": "d37cb74f360e19e664b94673bbf4b95462cad6e681a08215a95f4565c6e810aa",
 "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_SOURCE_SEMANTIC_REVIEW_SCHEMA_V1.json": "fa6529c8e6c7c8f96f186da26fe44e17004e92fd489184089ba62df204592a9f",
 "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_SOURCE_SEMANTIC_REVIEW_V1.json": "374472b2d7ab0a70d94ed1f650302869b829252dcf06a7afe29c7c2e18e345dc",
 "tools/c11d/d9/test_d_renderer_challenge_visual_payload_source_semantic_review_v1.py": "5f8d255d91a0496f7502c4c68c281a8a918dbae954e92823a4ff8ef04b5fafba",
 "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2C_SOURCE_FRAME_RUNTIME_RECEIPT_V1.json": "6d3c59214edbdd917cf63fe9ca4859edb6968d503368ec84e867bdd56a8df74c",
 "tools/c11d/d9/challenge_visual_payload_v2c_source_frame_runtime_in_memory.gd": "ba8500c1db0b86539953c667bc1c48bc765e960f765f7ecef935ff4d206e2a9d",
 "tools/c11d/d9/d_renderer_challenge_visual_payload_v2c_source_frame_runtime.py": "a4f5aab8febfb49ec25a97d12f4604137dcbf1c63049a50b0fafe5c0c0c5cdcf",
 "tools/c11d/d9/test_d_renderer_challenge_visual_payload_v2c_source_frame_runtime.py": "f8cb0717f9f90b46071dcbf292a4c308e3dac04b4090a3fd4a0ea53bf627ebfb",
}

class TestV2BDesignContract(unittest.TestCase):
    def test_01_contract_schema_id(self): self.assertEqual(CONTRACT["schema"], "C11D-CHALLENGE-VISUAL-PAYLOAD-V2B-SAFE-VISUAL-PROJECTION-DESIGN-CONTRACT-V1")
    def test_02_schema_draft_valid(self): self.assertIn("2020-12", SCHEMA["$schema"])
    def test_03_contract_schema_version(self): self.assertEqual(CONTRACT["schema_version"], "1.0")
    def test_04_design_only_status(self): self.assertEqual(CONTRACT["status"], "DESIGN_ONLY_NOT_IMPLEMENTED")
    def test_05_runtime_not_authorized(self): self.assertIs(CONTRACT["runtime_implementation_authorized"], False)
    def test_06_baseline_zip_sha_pinned(self): self.assertEqual(CONTRACT["authority"]["analysis_baseline_zip_sha256"], "aced079f3f553d81121e84940e6a7d9f2be4c278912b94abee75f277b8f32df2")
    def test_07_frozen_manifest_pin(self): self.assertEqual(CONTRACT["authority"]["frozen_c11c_manifest_sha256"], "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953")
    def test_08_review_authority_passed(self): self.assertEqual(CONTRACT["authority"]["review_tests_operator_confirmed"], "34/34")
    def test_09_approved_binding_count_zero(self): self.assertEqual(CONTRACT["authority"]["approved_bindings"], 0)
    def test_10_candidate_binding_count_zero(self): self.assertEqual(CONTRACT["authority"]["approved_custom_data_bindings"], 0)
    def test_11_selector_count(self): self.assertEqual(len(CONTRACT["selectors"]), 9)
    def test_12_selector_order(self): self.assertEqual([s["challenge_id"] for s in CONTRACT["selectors"]], IDS)
    def test_13_selector_ids_unique(self): self.assertEqual(len({s["challenge_id"] for s in CONTRACT["selectors"]}), 9)
    def test_14_source_pins_count(self): self.assertEqual(len(CONTRACT["source_pins"]), 81)
    def test_15_source_pins_unique(self): self.assertEqual(len({p["path"] for p in CONTRACT["source_pins"]}), 81)
    def test_16_source_pin_hash_format(self): self.assertTrue(all(len(p["sha256"]) == 64 and all(c in "0123456789abcdef" for c in p["sha256"]) for p in CONTRACT["source_pins"]))
    def test_17_authority_pin_count(self): self.assertEqual(len(CONTRACT["authority_input_pins"]), 9)
    def test_18_authority_pins_unique(self): self.assertEqual(len({p["path"] for p in CONTRACT["authority_input_pins"]}), 9)
    def test_19_authority_gate_inputs_have_valid_hashes(self): self.assertTrue(all(len(p["sha256"]) == 64 for p in CONTRACT["authority_input_pins"]))
    def test_20_authority_input_hashes_match_fixed_list(self): self.assertEqual({p["path"]:p["sha256"] for p in CONTRACT["authority_input_pins"]}, EXPECTED_INPUTS)
    def test_21_safe_allowlist_exact(self): self.assertEqual(CONTRACT["safe_projection"]["allowlisted_frame_fields"], BASE_FIELDS)
    def test_22_custom_data_excluded_from_allowlist(self): self.assertNotIn("custom_data", CONTRACT["safe_projection"]["allowlisted_frame_fields"])
    def test_23_whole_custom_data_forbidden(self): self.assertIs(CONTRACT["candidate_observation_policy"]["serialize_whole_custom_data_map"], False)
    def test_24_custom_data_not_in_safe_projection(self): self.assertIs(CONTRACT["candidate_observation_policy"]["include_custom_data_in_safe_projection"], False)
    def test_25_candidate_probe_is_not_approval(self): self.assertIs(CONTRACT["candidate_observation_policy"]["candidate_field_probe_is_binding_approval"], False)
    def test_26_candidate_rows_exact(self): self.assertEqual({(c["challenge_id"],c["field"]) for c in CONTRACT["candidate_observation_policy"]["candidate_fields"]}, CANDIDATE_ROWS)
    def test_27_all_candidate_rows_unapproved(self): self.assertTrue(all(c["renderer_binding_approved"] is False for c in CONTRACT["candidate_observation_policy"]["candidate_fields"]))
    def test_28_pilot_target_x_scalar(self):
        c=next(x for x in CONTRACT["candidate_observation_policy"]["candidate_fields"] if x["challenge_id"]=="CHALLENGE_003")
        self.assertEqual(c["semantic_type"], "float"); self.assertEqual(c["gameplay_seed_probe_expectation"], "EXPECTED_INVARIANT_ACROSS_GAMEPLAY_SEED_VARIANT")
    def test_29_hit_target_per_run_constant(self):
        c=next(x for x in CONTRACT["candidate_observation_policy"]["candidate_fields"] if x["challenge_id"]=="CHALLENGE_005")
        self.assertEqual(c["sampling_lifecycle"], "SAME_FINITE_VECTOR_REPEATED_FOR_ALL_FRAMES")
    def test_30_catch_target_per_frame(self):
        c=next(x for x in CONTRACT["candidate_observation_policy"]["candidate_fields"] if x["challenge_id"]=="CHALLENGE_006")
        self.assertEqual(c["sampling_lifecycle"], "FRAME_ALIGNED_VECTOR_TRACK")
    def test_31_find_target_per_frame(self):
        c=next(x for x in CONTRACT["candidate_observation_policy"]["candidate_fields"] if x["challenge_id"]=="CHALLENGE_007")
        self.assertEqual(c["sampling_lifecycle"], "FRAME_ALIGNED_VECTOR_TRACK")
    def test_32_choose_index_semantics(self):
        c=next(x for x in CONTRACT["candidate_observation_policy"]["candidate_fields"] if x["challenge_id"]=="CHALLENGE_008")
        self.assertEqual(c["semantic_type"], "int"); self.assertIn("SOURCE_FRAME_ONLY", c["gameplay_seed_probe_expectation"])
    def test_33_count_semantics(self):
        c=next(x for x in CONTRACT["candidate_observation_policy"]["candidate_fields"] if x["challenge_id"]=="CHALLENGE_009")
        self.assertEqual(c["semantic_type"], "int"); self.assertIn("SOURCE_FRAME_ONLY", c["gameplay_seed_probe_expectation"])
    def test_34_exact_variant_roles(self): self.assertEqual([v["role"] for v in MATRIX["variant_definitions"]], ["BASELINE_R1","BASELINE_R2","GAMEPLAY_SEED_MUTATION","MUSIC_SEED_MUTATION","EDITORIAL_MUTATION"])
    def test_35_base_music_seed_constant(self): self.assertEqual(MATRIX["variant_definitions"][0]["music_seed"], 840001)
    def test_36_music_seed_mutation_explicit(self): self.assertEqual(MATRIX["variant_definitions"][3]["music_seed"], 840002)
    def test_37_gameplay_seed_mutation_does_not_touch_music_seed(self):
        v=next(v for v in MATRIX["variant_definitions"] if v["role"]=="GAMEPLAY_SEED_MUTATION")
        self.assertEqual(v["music_seed"], 840001)
    def test_38_editorial_variant_changes_only_editorial(self):
        v=next(v for v in MATRIX["variant_definitions"] if v["role"]=="EDITORIAL_MUTATION")
        self.assertEqual(v["gameplay_seed"], "SOURCE_EFFECTIVE_GAMEPLAY_SEED"); self.assertEqual(v["music_seed"], 840001)
        self.assertEqual(v["editorial"], "CHANGE_TITLE_SUBTITLE_CALL_TO_ACTION_ONLY")
    def test_39_invocations_per_selector(self): self.assertEqual(MATRIX["per_selector_invocations"], {"canonical_planner_invocations":5,"godot_runtime_processes":5})
    def test_40_invocation_totals(self): self.assertEqual(MATRIX["whole_increment_invocations"], {"selector_count":9,"canonical_planner_invocations":45,"godot_runtime_processes":45})
    def test_41_identity_separation(self):
        model=CONTRACT["identity_model"]
        for k in ("canonical_request_hash","canonical_plan_hash","projection_instance_identity_sha256","safe_projection_state_sha256","candidate_field_probe_sha256"):
            self.assertIn(k, model)
    def test_42_payload_identity_not_created(self): self.assertIn("NOT_CREATED", CONTRACT["identity_model"]["payload_identity"])
    def test_43_receipt_schema_forbids_payload(self): self.assertIn("not", RECEIPT_SCHEMA); self.assertIn("payload_sha256", json.dumps(RECEIPT_SCHEMA))
    def test_44_temporal_conflicts_remain_blocked(self):
        for cid in ("CHALLENGE_008","CHALLENGE_009"):
            s=next(x for x in CONTRACT["selectors"] if x["challenge_id"]==cid)
            self.assertEqual(s["timeline_acceptance"], "BLOCKED_TIMEBASE_CONFLICT")
            self.assertEqual(s["timeline_scope"], "SOURCE_FRAME_ONLY_TIMEBASE_CONFLICT")
    def test_45_no_coordinate_transform(self): self.assertEqual(CONTRACT["safe_projection"]["coordinate_transform"], "NONE")
    def test_46_no_resampling(self): self.assertEqual(CONTRACT["safe_projection"]["resampling"], "PROHIBITED")
    def test_47_seed_oracle_is_state_hash(self): self.assertIn("actual gameplay seed sensitivity oracle", CONTRACT["identity_model"]["safe_projection_state_sha256"])
    def test_48_request_plan_hash_not_sensitivity_proof(self): self.assertIn("not proof of output change", CONTRACT["identity_model"]["canonical_plan_hash"])
    def test_49_runtime_bridge_reuse_required(self): self.assertEqual(CONTRACT["runtime_matrix"]["bridge"], "ChallengeRuntimeBridge.run_effective_pipeline(legacy_config: Dictionary) -> Dictionary")
    def test_50_no_planner_clone(self): self.assertIs(CONTRACT["runtime_matrix"]["do_not_clone_planner_or_mechanics"], True)
    def test_51_gameplay_seed_injection_in_memory_only(self): self.assertIn("never write the source JSON", CONTRACT["runtime_matrix"]["gameplay_seed_injection"])
    def test_52_music_seed_not_simulation_seed(self): self.assertIs(CONTRACT["runtime_matrix"]["music_seed_must_not_be_copied_into_simulation_seed"], True)
    def test_53_editorial_invariance_rule(self): self.assertIn("preserves safe projection", next(p["condition"] for p in MATRIX["proof_rules"] if p["id"]=="EDITORIAL_INVARIANCE"))
    def test_54_gameplay_variant_uses_output_hash(self): self.assertIn("safe_projection_state_sha256", next(p["condition"] for p in MATRIX["proof_rules"] if p["id"]=="GAMEPLAY_SEED_SENSITIVITY"))
    def test_55_music_orthogonality_rule(self): self.assertIn("MUSIC_SEED_MUTATION", next(p["condition"] for p in MATRIX["proof_rules"] if p["id"]=="MUSIC_ORTHOGONALITY"))
    def test_56_fail_closed_cases_count(self): self.assertEqual(len(CONTRACT["fail_closed_negative_cases"]), 44)
    def test_57_fail_closed_cases_unique(self): self.assertEqual(len(set(CONTRACT["fail_closed_negative_cases"])), 44)
    def test_58_forbidden_whole_custom_data_negative_exists(self): self.assertIn("custom_data_whole_map_access", CONTRACT["fail_closed_negative_cases"])
    def test_59_timeline_negatives_exist(self): self.assertIn("phase_acceptance_for_008", CONTRACT["fail_closed_negative_cases"]); self.assertIn("phase_acceptance_for_009", CONTRACT["fail_closed_negative_cases"])
    def test_60_governance_renderer_off(self): self.assertEqual(CONTRACT["governance_locks"]["renderer"], "OFF")
    def test_61_governance_release_none(self): self.assertEqual(CONTRACT["governance_locks"]["release_authority"], "NONE")
    def test_62_candidate_input_false(self): self.assertIs(CONTRACT["governance_locks"]["candidate_input_admissible"], False)
    def test_63_master_seed_not_adopted(self): self.assertEqual(CONTRACT["governance_locks"]["master_seed"], "NOT_ADOPTED")
    def test_64_d10_blocked(self): self.assertEqual(CONTRACT["governance_locks"]["D10"], "BLOCKED_FOR_PROMOTION")
    def test_65_challenge004_fixture_immutable(self): self.assertEqual(CONTRACT["governance_locks"]["challenge_004_v1_fixture"], "IMMUTABLE")
    def test_66_source_pin_paths_are_safe(self): self.assertTrue(all(not Path(p["path"]).is_absolute() and ".." not in Path(p["path"]).parts for p in CONTRACT["source_pins"]))
    def test_67_source_pin_hashes_current(self):
        for pin in CONTRACT["source_pins"]:
            p=ROOT / pin["path"]
            self.assertTrue(p.is_file(), f"missing pin: {pin['path']}")
            self.assertEqual(sha(p), pin["sha256"], f"pin drift: {pin['path']}")
    def test_68_authority_input_files_match_pins(self):
        for pin in CONTRACT["authority_input_pins"]:
            p=ROOT / pin["path"]
            self.assertTrue(p.is_file(), f"missing authority input: {pin['path']}")
            self.assertEqual(sha(p), pin["sha256"], f"authority input drift: {pin['path']}")
    def test_69_runtime_harness_has_canonical_bridge_call(self):
        s=(ROOT/"tools/c11d/d9/challenge_visual_payload_v2c_source_frame_runtime_in_memory.gd").read_text(encoding="utf-8")
        self.assertIn("RuntimeBridge.run_effective_pipeline(source)", s)
    def test_70_bridge_declares_effective_pipeline(self):
        s=(ROOT/"core/execution/ChallengeRuntimeBridge.gd").read_text(encoding="utf-8")
        self.assertIn("static func run_effective_pipeline(legacy_config: Dictionary) -> Dictionary:", s)
    def test_71_snapshot_base_fields_exist(self):
        s=(ROOT/"core/data/FrameSnapshot.gd").read_text(encoding="utf-8")
        for field in BASE_FIELDS: self.assertRegex(s, rf"var\s+{field}\s*:")
    def test_72_pilot_scalar_source_contract(self):
        s=(ROOT/"core/mechanics/pilot/PilotMechanic.gd").read_text(encoding="utf-8")
        self.assertIn('"target_x": target_x', s)
    def test_73_hit_target_is_per_run_member(self):
        s=(ROOT/"core/mechanics/hit/HitMechanic.gd").read_text(encoding="utf-8")
        self.assertIn('"target_position": _target_prime', s)
    def test_74_catch_target_is_target_track(self):
        s=(ROOT/"core/mechanics/catch/CatchMechanic.gd").read_text(encoding="utf-8")
        self.assertIn('"target_position": p_t', s)
    def test_75_find_target_is_target_track(self):
        s=(ROOT/"core/mechanics/find/FindMechanic.gd").read_text(encoding="utf-8")
        self.assertIn('"target_position": p_target', s)
    def test_76_choose_selection_is_integer_track(self):
        s=(ROOT/"core/mechanics/choose/ChooseMechanic.gd").read_text(encoding="utf-8")
        self.assertIn('"active_selection": selection', s)
    def test_77_count_displayed_count_is_integer_track(self):
        s=(ROOT/"core/mechanics/count/CountMechanic.gd").read_text(encoding="utf-8")
        self.assertIn('"displayed_count": displayed', s)
    def test_78_timebase_conflict_source_pin_008(self):
        p=ROOT/"challenges/CHALLENGE_008.json"; d=load_json(p)
        self.assertEqual(d["video"]["total_duration"], 11.0)
        self.assertEqual(sum(float(d["video"].get(k,0)) for k in ("hook_duration","game_duration","reveal_duration","cta_duration")), 12.0)
    def test_79_timebase_conflict_source_pin_009(self):
        p=ROOT/"challenges/CHALLENGE_009.json"; d=load_json(p)
        self.assertEqual(d["video"]["total_duration"], 11.0)
        self.assertEqual(sum(float(d["video"].get(k,0)) for k in ("hook_duration","game_duration","reveal_duration","cta_duration")), 12.0)
    def test_80_no_runtime_harness_in_this_increment(self):
        files=[p["path"] for p in []]
        self.assertIs(CONTRACT["runtime_implementation_authorized"], False)
        self.assertEqual(CONTRACT["next_gate"]["implementation_status"], "NOT_IMPLEMENTED_IN_THIS_INCREMENT")
    def test_81_next_gate_is_v2b_implementation(self): self.assertEqual(CONTRACT["next_gate"]["name"], "V2B_SAFE_VISUAL_PROJECTION_RUNTIME_HARNESS_IMPLEMENTATION")
    def test_82_v2c_evidence_scope_limited(self): self.assertEqual(CONTRACT["authority"]["v2c_runtime_report_sha256"], "35e5985f47055fc11cbc0fcd7317f4d0a4ebe6bfe4d8bb22bdab67b7bcbe56a7")
    def test_83_no_candidate_values_in_receipt(self): self.assertIs(CONTRACT["candidate_observation_policy"]["candidate_values_in_receipt"], False)
    def test_84_frame_order_preserved(self): self.assertEqual(CONTRACT["safe_projection"]["source_frame_order"], "PRESERVE_EXACTLY")
    def test_85_receipt_schema_rejects_extra_properties(self): self.assertIs(RECEIPT_SCHEMA["additionalProperties"], False)
    def test_86_projection_hash_not_payload_hash(self): self.assertNotIn("payload_sha256", CONTRACT["identity_model"])
    def test_87_projection_receipt_explicitly_no_payload(self): self.assertIn("payload_identity_created", RECEIPT_SCHEMA["properties"]["identity"]["required"])
    def test_88_all_selectors_use_source_frame_scope(self): self.assertTrue(all(s["raw_frame_state_observation"].startswith("ALLOWED") for s in CONTRACT["selectors"]))
    def test_89_source_timebase_is_not_rewritten(self): self.assertTrue(all(s["timeline_scope"].startswith("SOURCE_FRAME_ONLY") for s in CONTRACT["selectors"]))
    def test_90_design_test_matrix_not_execution_evidence(self): self.assertEqual(MATRIX["status"], "DESIGN_ONLY_NOT_EXECUTED")

if __name__ == "__main__":
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(TestV2BDesignContract)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful() and result.testsRun == 90:
        print("C11D_V2B_DESIGN_CONTRACT_TESTS_PASS=90/90")
        raise SystemExit(0)
    print(f"C11D_V2B_DESIGN_CONTRACT_TESTS_FAIL={result.testsRun};failures={len(result.failures)};errors={len(result.errors)}")
    raise SystemExit(1)
