#!/usr/bin/env python3
"""Static/source audit for the V2-B runtime acceptance harness; never runs Godot or the 45-run matrix."""
from __future__ import annotations
import ast
import hashlib
import importlib.util
import json
import re
import sys
import unittest
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SAFE_PROJECTION_RUNTIME_CONTRACT_V1.json")
CONTRACT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SAFE_PROJECTION_RUNTIME_CONTRACT_SCHEMA_V1.json")
DESIGN_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SAFE_VISUAL_PROJECTION_DESIGN_V1.json")
MATRIX_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SEED_TEST_MATRIX_V1.json")
RECEIPT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SAFE_PROJECTION_RUNTIME_RECEIPT_SCHEMA_V1.json")
REPORT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SAFE_PROJECTION_RUNTIME_REPORT_SCHEMA_V1.json")
HARNESS_REL = Path("tools/c11d/d9/challenge_visual_payload_v2b_safe_projection_runtime_in_memory.gd")
RUNNER_REL = Path("tools/c11d/d9/d_renderer_challenge_visual_payload_v2b_safe_projection_runtime.py")
V2C_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2C_SOURCE_FRAME_RUNTIME_RECEIPT_V1.json")
FROZEN_SHA = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
DESIGN_SHA = "e4f02e37fd4b9b2c89cbaa7597162f87b180da43182dc576d664263c1b937cfc"
MATRIX_SHA = "d69c3fb2aca78a26c3afbfda0084f7f7aef458ee404b37f65261c6d22e43121a"
V2C_SHA = "6d3c59214edbdd917cf63fe9ca4859edb6968d503368ec84e867bdd56a8df74c"
CONTRACT_SHA = "f89235640f40c81be6100f01f1007ed4e787990a1bbf7927fcd8d676ef2cb9a3"
CONTRACT_SCHEMA_ID = "C11D-CHALLENGE-VISUAL-PAYLOAD-V2B-SAFE-PROJECTION-RUNTIME-CONTRACT-SCHEMA-V1"
CONTRACT_ID = "C11D-CHALLENGE-VISUAL-PAYLOAD-V2B-SAFE-PROJECTION-RUNTIME-CONTRACT-V1"
DESIGN_ID = "C11D-CHALLENGE-VISUAL-PAYLOAD-V2B-SAFE-VISUAL-PROJECTION-DESIGN-CONTRACT-V1"
V2C_ID = "C11D-CHALLENGE-VISUAL-PAYLOAD-V2C-SOURCE-FRAME-RUNTIME-RECEIPT-CONTRACT-V1"
IDS = [f"CHALLENGE_{i:03d}" for i in range(1, 10)]
ROLES = ["BASELINE_R1", "BASELINE_R2", "GAMEPLAY_SEED_MUTATION", "MUSIC_SEED_MUTATION", "EDITORIAL_MUTATION"]
EXPECTED_BASE_FIELDS = ["position", "rotation", "scale", "opacity", "texture_index", "variant_id"]
EXPECTED_PROJECTION_TUPLE = ["local_frame_index", "position_x", "position_y", "rotation", "scale_x", "scale_y", "opacity", "texture_index", "variant_id"]
EXPECTED_CANDIDATES = {
    "CHALLENGE_001": None, "CHALLENGE_002": None, "CHALLENGE_003": "target_x",
    "CHALLENGE_004": None, "CHALLENGE_005": "target_position", "CHALLENGE_006": "target_position",
    "CHALLENGE_007": "target_position", "CHALLENGE_008": "active_selection", "CHALLENGE_009": "displayed_count",
}
EXPECTED_FAMILY = {
    "CHALLENGE_001": "key", "CHALLENGE_002": "parking", "CHALLENGE_003": "pilot",
    "CHALLENGE_004": "parking_v2", "CHALLENGE_005": "hit_v1", "CHALLENGE_006": "catch_v1",
    "CHALLENGE_007": "find_v1", "CHALLENGE_008": "choose_v1", "CHALLENGE_009": "count_v1",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(rel: Path) -> dict[str, Any]:
    value = json.loads((ROOT / rel).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{rel.as_posix()} must be an object")
    return value


CONTRACT = read_json(CONTRACT_REL)
CONTRACT_SCHEMA = read_json(CONTRACT_SCHEMA_REL)
DESIGN = read_json(DESIGN_REL)
MATRIX = read_json(MATRIX_REL)
RECEIPT_SCHEMA = read_json(RECEIPT_SCHEMA_REL)
REPORT_SCHEMA = read_json(REPORT_SCHEMA_REL)
V2C = read_json(V2C_REL)
RUNNER_PATH = ROOT / RUNNER_REL
HARNESS_PATH = ROOT / HARNESS_REL
RUNNER_TEXT = RUNNER_PATH.read_text(encoding="utf-8")
HARNESS_TEXT = HARNESS_PATH.read_text(encoding="utf-8")
SPEC = importlib.util.spec_from_file_location("c11d_v2b_safe_projection_runtime_test_import", RUNNER_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load V2-B runtime runner for static helper tests")
RUNTIME = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = RUNTIME
SPEC.loader.exec_module(RUNTIME)


class RuntimeContractTests(unittest.TestCase):
    def test_contract_file_sha_is_the_pinned_value(self):
        self.assertEqual(digest(ROOT / CONTRACT_REL), CONTRACT_SHA)

    def test_contract_identity_and_non_acceptance_status(self):
        self.assertEqual(CONTRACT["schema"], CONTRACT_ID)
        self.assertEqual(CONTRACT["status"], "IMPLEMENTED_NOT_RUNTIME_ACCEPTED")
        self.assertEqual(CONTRACT["runtime_status"], "NOT_EXECUTED_BY_DESIGN_OR_IMPLEMENTATION_TESTS")

    def test_contract_schema_identity_and_strict_root(self):
        self.assertEqual(CONTRACT_SCHEMA["schema"], CONTRACT_SCHEMA_ID)
        self.assertIs(CONTRACT_SCHEMA["additionalProperties"], False)

    def test_contract_schema_sha_matches_contract_implementation_pin(self):
        self.assertEqual(digest(ROOT / CONTRACT_SCHEMA_REL), CONTRACT["implementation"]["contract_schema_sha256"])

    def test_contract_root_keys_are_exactly_schema_required_and_properties(self):
        keys = set(CONTRACT)
        self.assertEqual(keys, set(CONTRACT_SCHEMA["required"]))
        self.assertEqual(keys, set(CONTRACT_SCHEMA["properties"]))

    def test_runtime_contract_source_schema_and_design_pins(self):
        self.assertEqual(CONTRACT["design_contract_path"], DESIGN_REL.as_posix())
        self.assertEqual(CONTRACT["design_contract_sha256"], DESIGN_SHA)
        self.assertEqual(digest(ROOT / DESIGN_REL), DESIGN_SHA)

    def test_seed_matrix_pin(self):
        self.assertEqual(CONTRACT["seed_test_matrix_path"], MATRIX_REL.as_posix())
        self.assertEqual(CONTRACT["seed_test_matrix_sha256"], MATRIX_SHA)
        self.assertEqual(digest(ROOT / MATRIX_REL), MATRIX_SHA)

    def test_frozen_manifest_sha_is_the_immutable_c11c_pin(self):
        self.assertEqual(CONTRACT["frozen_c11c_manifest_sha256"], FROZEN_SHA)
        self.assertEqual(digest(ROOT / "release/C11C_FREEZE_PACKAGE_MANIFEST.json"), FROZEN_SHA)

    def test_nine_selectors_are_fixed_in_order(self):
        self.assertEqual(CONTRACT["selector_ids"], IDS)
        self.assertEqual(CONTRACT["expected_selector_count"], 9)
        self.assertEqual(len(DESIGN["selectors"]), 9)

    def test_selector_denominator_explicitly_matches_design(self):
        self.assertIs(CONTRACT["expected_selector_count_matches_design_contract"], True)

    def test_five_roles_and_45_by_45_matrix(self):
        self.assertEqual(CONTRACT["variant_roles"], ROLES)
        self.assertEqual(CONTRACT["variants_per_selector"], 5)
        self.assertEqual(CONTRACT["canonical_planner_invocations_expected"], 45)
        self.assertEqual(CONTRACT["godot_processes_expected"], 45)
        self.assertEqual(MATRIX["whole_increment_invocations"], {"selector_count": 9, "canonical_planner_invocations": 45, "godot_runtime_processes": 45})

    def test_per_selector_matrix_has_five_planner_and_godot_runs(self):
        self.assertEqual(MATRIX["per_selector_invocations"], {"canonical_planner_invocations": 5, "godot_runtime_processes": 5})

    def test_source_pin_denominators_are_81_and_9(self):
        self.assertEqual(CONTRACT["source_pin_count"], 81)
        self.assertEqual(CONTRACT["authority_input_pin_count"], 9)
        self.assertEqual(len(DESIGN["source_pins"]), 81)
        self.assertEqual(len(DESIGN["authority_input_pins"]), 9)

    def test_runtime_runner_static_tests_gate_runtime_execution(self):
        self.assertIn('ap.add_argument("--implementation-test-receipt", required=True)', RUNNER_TEXT)
        self.assertIn("validate_implementation_test_receipt", RUNNER_TEXT)
        self.assertIn("PASS_IMPLEMENTATION_STATIC_TESTS", RUNNER_TEXT)

    def test_runtime_runner_has_fail_closed_result(self):
        self.assertIn('"status": "BLOCKED"', RUNNER_TEXT)
        self.assertIn("raise SystemExit(main())", RUNNER_TEXT)
        self.assertIn("return 0 if report[\"status\"] == \"PASS_SAFE_PROJECTION_SEED_SENSITIVITY\" else 1", RUNNER_TEXT)

    def test_runtime_harness_entrypoint_is_the_existing_bridge(self):
        self.assertEqual(HARNESS_TEXT.count("RuntimeBridge.run_effective_pipeline(source)"), 1)

    def test_design_only_contract_remains_unmodified_and_not_implemented(self):
        self.assertEqual(DESIGN["schema"], DESIGN_ID)
        self.assertEqual(DESIGN["status"], "DESIGN_ONLY_NOT_IMPLEMENTED")
        self.assertIs(DESIGN["runtime_implementation_authorized"], False)

    def test_runtime_contract_does_not_claim_matrix_execution(self):
        self.assertEqual(CONTRACT["runtime_status"], "NOT_EXECUTED_BY_DESIGN_OR_IMPLEMENTATION_TESTS")
        self.assertEqual(CONTRACT["governance_locks"]["visual_seed_sensitivity"], "NOT_TESTED_UNTIL_V2B_RUNTIME_ACCEPTED")

    def test_upstream_source_pins_reconcile_cleanly(self):
        _, _, errors = RUNTIME.load_upstream(ROOT, CONTRACT)
        self.assertEqual(errors, [])

    def test_validate_runtime_contract_accepts_the_actual_pinned_contract(self):
        RUNTIME.validate_runtime_contract(CONTRACT, CONTRACT_SHA)

    def test_validator_rejects_wrong_contract_sha_shape(self):
        with self.assertRaises(RUNTIME.ContractError):
            RUNTIME.validate_runtime_contract(CONTRACT, "not-a-sha")

    def test_validator_rejects_binding_approval(self):
        mutated = json.loads(json.dumps(CONTRACT))
        mutated["approved_bindings"] = 1
        with self.assertRaises(RUNTIME.ContractError):
            RUNTIME.validate_runtime_contract(mutated, CONTRACT_SHA)

    def test_validator_rejects_payload_materialization(self):
        mutated = json.loads(json.dumps(CONTRACT))
        mutated["payload_materialized"] = True
        with self.assertRaises(RUNTIME.ContractError):
            RUNTIME.validate_runtime_contract(mutated, CONTRACT_SHA)

    def test_validator_rejects_renderer_activation(self):
        mutated = json.loads(json.dumps(CONTRACT))
        mutated["renderer"] = "ON"
        with self.assertRaises(RUNTIME.ContractError):
            RUNTIME.validate_runtime_contract(mutated, CONTRACT_SHA)

    def test_seed_mutation_wrap_is_deterministic(self):
        self.assertEqual(RUNTIME.next_gameplay_seed(1), 2)
        self.assertEqual(RUNTIME.next_gameplay_seed(2147483645), 2147483646)
        self.assertEqual(RUNTIME.next_gameplay_seed(2147483646), 1)

    def test_seed_mutation_rejects_bool(self):
        with self.assertRaises(RUNTIME.ContractError):
            RUNTIME.next_gameplay_seed(True)

    def test_seed_mutation_rejects_zero(self):
        with self.assertRaises(RUNTIME.ContractError):
            RUNTIME.next_gameplay_seed(0)

    def test_seed_mutation_rejects_above_limit(self):
        with self.assertRaises(RUNTIME.ContractError):
            RUNTIME.next_gameplay_seed(2147483647)

    def test_path_guard_accepts_repository_relative_path(self):
        self.assertEqual(RUNTIME.safe_child(ROOT, "challenges/CHALLENGE_001.json"), ROOT / "challenges/CHALLENGE_001.json")

    def test_path_guard_rejects_parent_escape(self):
        with self.assertRaises(RUNTIME.ContractError):
            RUNTIME.safe_child(ROOT, "../outside.json")

    def test_path_guard_rejects_absolute_path(self):
        with self.assertRaises(RUNTIME.ContractError):
            RUNTIME.safe_child(ROOT, "/outside.json")

    def test_path_guard_rejects_backslash_path(self):
        with self.assertRaises(RUNTIME.ContractError):
            RUNTIME.safe_child(ROOT, "challenges\\CHALLENGE_001.json")

    def test_exact_object_helper_rejects_unknown_fields(self):
        with self.assertRaises(RUNTIME.ContractError):
            RUNTIME.exact({"allowed": 1, "extra": 2}, {"allowed"}, "test object")

    def test_baseline_music_seed_is_separate_from_gameplay_mutation(self):
        self.assertEqual(CONTRACT["baseline_music_seed"], 840001)
        self.assertEqual(CONTRACT["music_seed_mutation"], 840002)
        self.assertEqual(CONTRACT["gameplay_seed_mutation_rule"], "DETERMINISTIC_NEXT_INTEGER_WITH_WRAP; source seed + 1, wrap 2147483646 to 1; no automatic seed generation")

    def test_music_and_gameplay_domains_are_noncolliding_by_policy(self):
        self.assertEqual(CONTRACT["seed_limits"]["cross_domain_seed_collision"], "BLOCK")
        self.assertEqual(CONTRACT["seed_limits"]["minimum"], 1)
        self.assertEqual(CONTRACT["seed_limits"]["maximum"], 2147483646)

    def test_safe_projection_allowlist_is_exact(self):
        self.assertEqual(CONTRACT["safe_projection"]["allowlisted_frame_fields"], EXPECTED_BASE_FIELDS)

    def test_safe_projection_tuple_preserves_frame_index_and_raw_fields(self):
        self.assertEqual(CONTRACT["safe_projection"]["canonical_tuple"], EXPECTED_PROJECTION_TUPLE)

    def test_custom_data_is_a_forbidden_base_projection_field(self):
        self.assertIn("custom_data", CONTRACT["safe_projection"]["forbidden_frame_fields"])

    def test_projection_forbids_transform_resampling_and_interpolation(self):
        self.assertEqual(CONTRACT["safe_projection"]["coordinate_transform"], "NONE")
        self.assertEqual(CONTRACT["safe_projection"]["resampling"], "PROHIBITED")
        self.assertEqual(CONTRACT["safe_projection"]["frame_interpolation"], "PROHIBITED")

    def test_projection_forbids_scene_and_render_nodes(self):
        self.assertIs(CONTRACT["safe_projection"]["must_not_create_scene_or_render_nodes"], True)
        self.assertEqual(CONTRACT["safe_projection"]["rendering_server"], "PROHIBITED")
        self.assertEqual(CONTRACT["safe_projection"]["viewport_capture"], "PROHIBITED")

    def test_projection_serialization_is_ordered_arrays_and_finite_only(self):
        self.assertIn("ordered array-of-arrays", CONTRACT["safe_projection"]["serialization"])
        self.assertIn("finite values only", CONTRACT["safe_projection"]["serialization"])

    def test_candidate_allowlist_exact(self):
        self.assertEqual(CONTRACT["candidate_observation"]["allowlisted_fields"], ["target_x", "target_position", "active_selection", "displayed_count"])

    def test_candidate_raw_values_prohibited(self):
        self.assertIs(CONTRACT["candidate_observation"]["raw_values_in_receipt"], False)
        self.assertEqual(CONTRACT["candidate_observation"]["whole_custom_data_map_access"], "PROHIBITED")

    def test_approved_binding_counts_are_zero_in_root_and_candidate_policy(self):
        self.assertEqual(CONTRACT["approved_bindings"], 0)
        self.assertEqual(CONTRACT["approved_custom_data_bindings"], 0)
        self.assertEqual(CONTRACT["candidate_observation"]["approved_bindings"], 0)
        self.assertEqual(CONTRACT["candidate_observation"]["approved_custom_data_bindings"], 0)

    def test_runtime_contract_has_correct_governance_locks(self):
        self.assertEqual(CONTRACT["governance_locks"], RUNTIME.GOVERNANCE)

    def test_challenge_008_009_timebase_conflict_stays_blocked(self):
        self.assertEqual(CONTRACT["governance_locks"]["challenge_008_009_phase_timeline_acceptance"], "BLOCKED_TIMEBASE_CONFLICT_SOURCE_FRAME_ONLY")

    def test_challenge_004_v1_fixture_stays_immutable(self):
        self.assertEqual(CONTRACT["governance_locks"]["challenge_004_v1_fixture"], "IMMUTABLE")

    def test_next_gate_requires_static_test_receipt_before_runtime(self):
        self.assertIn("implementation_test_receipt.json", CONTRACT["next_gate"]["entry_condition"])
        self.assertIn("Static implementation tests", CONTRACT["next_gate"]["entry_condition"])

    def test_next_gate_prohibitions_include_no_payload_media_or_renderer(self):
        forbidden = CONTRACT["next_gate"]["must_not_do"]
        self.assertIn("materialize payload/media", forbidden)
        self.assertIn("emit renderer-native input", forbidden)
        self.assertIn("change C11-C", forbidden)
        self.assertIn("enable renderer", forbidden)

    def test_candidate_semantics_pilot_exception(self):
        self.assertIn("expected invariant", CONTRACT["candidate_observation"]["pilot_target_x"])

    def test_candidate_semantics_hit_is_run_constant(self):
        self.assertIn("per-run vector repeated", CONTRACT["candidate_observation"]["hit_target_position"])

    def test_candidate_semantics_catch_find_are_frame_tracks(self):
        self.assertIn("frame-aligned track", CONTRACT["candidate_observation"]["catch_find_target_position"])

    def test_candidate_semantics_choose_is_index(self):
        self.assertIn("option bounds", CONTRACT["candidate_observation"]["choose_active_selection"])

    def test_candidate_semantics_count_uses_displayed_count_not_target_count(self):
        self.assertIn("never read target_count", CONTRACT["candidate_observation"]["count_displayed_count"])

    def test_runner_syntax_parses_without_executing_main(self):
        ast.parse(RUNNER_TEXT, filename=RUNNER_REL.as_posix())

    def test_runtime_test_script_does_not_invoke_godot_or_runner_main(self):
        tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
        called = set()
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            current = node.func
            parts = []
            while isinstance(current, ast.Attribute):
                parts.append(current.attr)
                current = current.value
            if isinstance(current, ast.Name):
                parts.append(current.id)
                called.add(".".join(reversed(parts)))
        for forbidden_call in ("RUNTIME.main", "subprocess.Popen", "subprocess.run", "RUNTIME.run_godot"):
            self.assertNotIn(forbidden_call, called)

    def test_runtime_test_suite_never_executes_the_45_by_45_matrix(self):
        tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
        called_names = {node.func.id for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)}
        self.assertNotIn("make_planner", called_names)
        self.assertNotIn("version_probe", called_names)
        self.assertNotIn("run_godot", called_names)

    def test_runner_builds_canonical_request_not_a_cloned_planner(self):
        self.assertIn("planner.evaluate_universal_request(raw, root)", RUNNER_TEXT)
        self.assertIs(CONTRACT["planner_route"]["do_not_clone_planner_or_mechanics"], True)

    def test_planning_bridge_and_adapter_stay_nonrenderable(self):
        self.assertIn('bridge.get("status") != "PLANNING_ONLY_NOT_RENDERABLE"', RUNNER_TEXT)
        self.assertIn('adapter.get("status") != "PREPARED_NOT_DISPATCHED_RENDERER_DISABLED"', RUNNER_TEXT)

    def test_runner_verifies_runner_harness_and_all_three_schemas(self):
        impl = CONTRACT["implementation"]
        self.assertEqual(digest(ROOT / RUNNER_REL), impl["runtime_runner_sha256"])
        self.assertEqual(digest(ROOT / HARNESS_REL), impl["harness_sha256"])
        self.assertEqual(digest(ROOT / RECEIPT_SCHEMA_REL), impl["receipt_schema_sha256"])
        self.assertEqual(digest(ROOT / REPORT_SCHEMA_REL), impl["report_schema_sha256"])
        self.assertEqual(impl["runtime_runner_path"], RUNNER_REL.as_posix())

    def test_runner_pins_v2c_family_contract_as_authority(self):
        self.assertEqual(digest(ROOT / V2C_REL), V2C_SHA)
        self.assertIn('{"path": "' + V2C_REL.as_posix() + '", "sha256": "' + V2C_SHA + '"', json.dumps(DESIGN["authority_input_pins"]))
        self.assertIn("def family_for_selector(", RUNNER_TEXT)

    def test_runner_uses_resolved_canonical_family_not_nonexistent_v2b_family_id(self):
        self.assertIn("family_id = family_for_selector(root, selector)", RUNNER_TEXT)
        self.assertNotIn('selector["family_id"]', RUNNER_TEXT)

    def test_receipt_schema_is_strict(self):
        self.assertIs(RECEIPT_SCHEMA["additionalProperties"], False)
        self.assertEqual(set(RECEIPT_SCHEMA["required"]), set(RECEIPT_SCHEMA["properties"]))

    def test_report_schema_is_strict(self):
        self.assertIs(REPORT_SCHEMA["additionalProperties"], False)
        self.assertEqual(set(REPORT_SCHEMA["required"]), set(REPORT_SCHEMA["properties"]))

    def test_receipt_schema_prohibits_raw_candidate_values(self):
        obs = RECEIPT_SCHEMA["properties"]["candidate_field_observations"]["items"]["properties"]
        self.assertIs(obs["raw_values_emitted"]["const"], False)
        self.assertIs(obs["renderer_binding_approved"]["const"], False)

    def test_receipt_schema_payload_must_not_be_created(self):
        props = RECEIPT_SCHEMA["properties"]["identity"]["properties"]
        self.assertEqual(props["payload_identity"]["const"], "NOT_CREATED")

    def test_report_schema_denominators_are_fixed(self):
        props = REPORT_SCHEMA["properties"]
        self.assertEqual(props["selector_count_expected"]["const"], 9)
        self.assertEqual(props["planner_invocations_expected"]["const"], 45)
        self.assertEqual(props["godot_runtime_processes_expected"]["const"], 45)

    def test_report_schema_requires_governance_and_evidence(self):
        self.assertIn("governance_locks", REPORT_SCHEMA["required"])
        self.assertIn("evidence", REPORT_SCHEMA["required"])

    def test_godot_harness_only_reads_allowlisted_frame_fields_for_projection(self):
        self.assertIn("frame.position", HARNESS_TEXT)
        self.assertIn("frame.rotation", HARNESS_TEXT)
        self.assertIn("frame.scale", HARNESS_TEXT)
        self.assertIn("frame.opacity", HARNESS_TEXT)
        self.assertIn("frame.texture_index", HARNESS_TEXT)
        self.assertIn("frame.variant_id", HARNESS_TEXT)

    def test_godot_harness_never_enumerates_custom_data(self):
        self.assertNotIn("custom_data.keys()", HARNESS_TEXT)
        self.assertNotRegex(HARNESS_TEXT, r"for\s+\w+\s+in\s+frame\.custom_data")
        self.assertNotRegex(HARNESS_TEXT, r"JSON\.stringify\([^\n]*custom_data")

    def test_godot_candidate_probe_reads_one_field_by_key(self):
        self.assertIn("frame.custom_data.has(field_name)", HARNESS_TEXT)
        self.assertIn("frame.custom_data[field_name]", HARNESS_TEXT)
        self.assertIn("const ApprovedProbeFields", HARNESS_TEXT)

    def test_godot_harness_does_not_use_renderer_or_scene_creation_apis(self):
        for forbidden in ("RenderingServer", "SubViewport", "ViewportTexture", "ResourceSaver", "PackedScene", "FileAccess.WRITE", "FileAccess.open(", "Image.save("):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, HARNESS_TEXT)

    def test_godot_harness_uses_read_only_file_access(self):
        self.assertIn("FileAccess.get_file_as_bytes", HARNESS_TEXT)
        self.assertNotRegex(HARNESS_TEXT, r"\.store_(?:8|16|32|64|var|buffer|string)\s*\(")

    def test_godot_harness_does_not_create_a_payload_or_media(self):
        self.assertIn('"payload_identity": "NOT_CREATED"', HARNESS_TEXT)
        self.assertIn('"payload_materialized": false', HARNESS_TEXT)
        self.assertIn('"media_created": false', HARNESS_TEXT)

    def test_godot_harness_keeps_governance_locks(self):
        self.assertIn('governance.get("renderer") != "OFF"', HARNESS_TEXT)
        self.assertIn('governance.get("D4.8") != "BLOCKED"', HARNESS_TEXT)
        self.assertIn('governance.get("D9.10") != "PREPARE_ONLY"', HARNESS_TEXT)
        self.assertIn('governance.get("release_authority") != "NONE"', HARNESS_TEXT)

    def test_godot_harness_pins_runtime_contract_schema(self):
        self.assertIn("RuntimeContractSchemaPath", HARNESS_TEXT)
        self.assertIn("RUNTIME_CONTRACT_SCHEMA_SOURCE_PIN_MISMATCH", HARNESS_TEXT)
        self.assertIn(CONTRACT_SCHEMA_ID, HARNESS_TEXT)

    def test_godot_harness_runtime_bridge_version_guard_is_mono_launcher_guard(self):
        self.assertIn('verified_godot_version.to_lower().contains("mono")', HARNESS_TEXT)
        self.assertIn('version_info.get("patch", -1)) != 1', HARNESS_TEXT)

    def test_all_candidate_probe_types_are_explicit(self):
        expected_types = {"target_x": "float", "target_position": "Vector2", "active_selection": "int", "displayed_count": "int"}
        self.assertEqual({k: v for k, v in [("target_x", "float"), ("target_position", "Vector2"), ("active_selection", "int"), ("displayed_count", "int")]}, expected_types)
        for token in ('type_name = "float"', 'type_name = "Vector2"', 'type_name = "int"'):
            self.assertIn(token, HARNESS_TEXT)

    def test_challenge_008_009_keep_source_frame_only_timebase_lock(self):
        self.assertIn('var conflict := _challenge_id in ["CHALLENGE_008", "CHALLENGE_009"]', HARNESS_TEXT)
        self.assertIn("BLOCKED_TIMEBASE_CONFLICT_SOURCE_FRAME_ONLY", HARNESS_TEXT)

    def test_runtime_runner_stops_after_first_selector_failure(self):
        self.assertIn("if failure:\n                break", RUNNER_TEXT)
        self.assertIn("NOT_RUN_AFTER_FIRST_FAILURE", RUNNER_TEXT)

    def test_runtime_runner_writes_reports_to_explicit_evidence_dir(self):
        self.assertIn('ap.add_argument("--evidence-dir", required=True)', RUNNER_TEXT)
        self.assertIn('report_path = ev / "report.json"', RUNNER_TEXT)

    def test_runtime_runner_requires_clean_evidence_directory(self):
        self.assertIn("EVIDENCE_DIR_NOT_EMPTY", RUNNER_TEXT)

    def test_runtime_runner_records_godot_stdout_and_stderr_separately(self):
        self.assertIn('(prefix.with_suffix(".out")).write_bytes(ob)', RUNNER_TEXT)
        self.assertIn('(prefix.with_suffix(".err")).write_bytes(eb)', RUNNER_TEXT)

    def test_runtime_runner_acceptance_depends_on_state_hash(self):
        self.assertIn('"safe_projection_state_sha256"] != id0["safe_projection_state_sha256"]', RUNNER_TEXT)
        self.assertNotIn("request_hash changed therefore gameplay state changed", RUNNER_TEXT.lower())

    def test_runtime_runner_compares_candidate_field_hashes_separately(self):
        self.assertIn("candidate_hash_map", RUNNER_TEXT)
        self.assertIn("PILOT_TARGET_X_EXPECTED_INVARIANCE_FAILED", RUNNER_TEXT)
        self.assertIn("GAMEPLAY_SEED_CANDIDATE_CHANGE_NOT_OBSERVED", RUNNER_TEXT)

    def test_runtime_runner_checks_music_orthogonality(self):
        self.assertIn("MUSIC_SEED_CHANGED_SIMULATION_STATE_OR_CANDIDATE", RUNNER_TEXT)
        self.assertIn("MUSIC_SEED_ORTHOGONALITY_FAILED", RUNNER_TEXT)

    def test_runtime_runner_checks_editorial_orthogonality(self):
        self.assertIn("EDITORIAL_MUTATION_CHANGED_SIMULATION_STATE_OR_CANDIDATE", RUNNER_TEXT)
        self.assertIn("EDITORIAL_ORTHOGONALITY_FAILED", RUNNER_TEXT)

    def test_runtime_runner_probes_exact_godot_version(self):
        self.assertIn('"4.7.1" not in version', RUNNER_TEXT)
        self.assertIn('"mono" not in version.lower()', RUNNER_TEXT)

    def test_runtime_runner_checks_pins_before_and_after_runtime(self):
        self.assertIn("pin_errors_before", RUNNER_TEXT)
        self.assertIn("pin_errors_after", RUNNER_TEXT)
        self.assertIn("SOURCE_PIN_DRIFT_AFTER_RUNTIME", RUNNER_TEXT)

    def test_runtime_runner_does_not_auto_select_a_seed(self):
        self.assertIn("no RNG and no automatic seed selection", RUNNER_TEXT)
        self.assertNotIn("random.", RUNNER_TEXT.lower())

    def test_runtime_runner_has_no_output_video_generation_api(self):
        for forbidden in ("movie_writer", "render_video", "ffmpeg", "Image.save", "RenderingServer", "SubViewport"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden.lower(), RUNNER_TEXT.lower())

    def test_runtime_runner_implementation_test_receipt_is_strict(self):
        self.assertIn('exact(receipt, fields, "implementation test receipt")', RUNNER_TEXT)
        self.assertIn('receipt["status"] != "PASS_IMPLEMENTATION_STATIC_TESTS"', RUNNER_TEXT)

    def test_runtime_runner_checks_implementation_artifacts_against_receipt(self):
        self.assertIn("implementation_test_sha256", RUNNER_TEXT)
        self.assertIn("contract_schema_sha256", RUNNER_TEXT)
        self.assertIn("receipt does not match active file", RUNNER_TEXT)

    def test_runtime_runner_family_resolver_rejects_mismatched_source_lineage(self):
        self.assertIn("pinned selector/family lineage mismatch", RUNNER_TEXT)

    def test_runtime_runner_output_does_not_claim_authority_promotion(self):
        self.assertIn("D10=BLOCKED_FOR_PROMOTION", RUNNER_TEXT)
        self.assertIn("release_authority=NONE", RUNNER_TEXT)

    def test_runtime_runner_candidate_probe_semantic_type_is_checked(self):
        self.assertIn('semantic_types = {"target_x": "float", "target_position": "Vector2", "active_selection": "int", "displayed_count": "int"}', RUNNER_TEXT)
        self.assertIn("type_histogram", RUNNER_TEXT)


# Expand individual source pins and authority-input pins into independent test cases.
class IndividualSourcePinTests(unittest.TestCase):
    pass


class IndividualAuthorityPinTests(unittest.TestCase):
    pass


class IndividualSelectorFamilyTests(unittest.TestCase):
    pass


def _make_pin_test(rel: str, expected_sha: str):
    def test(self: unittest.TestCase) -> None:
        posix = PurePosixPath(rel)
        self.assertFalse(posix.is_absolute(), rel)
        self.assertNotIn("..", posix.parts, rel)
        self.assertNotIn("\\", rel, rel)
        path = ROOT.joinpath(*posix.parts)
        self.assertTrue(path.is_file(), rel)
        self.assertEqual(digest(path), expected_sha, rel)
    return test


for index, pin in enumerate(DESIGN["source_pins"], 1):
    setattr(IndividualSourcePinTests, f"test_source_pin_{index:03d}", _make_pin_test(pin["path"], pin["sha256"]))
for index, pin in enumerate(DESIGN["authority_input_pins"], 1):
    setattr(IndividualAuthorityPinTests, f"test_authority_input_pin_{index:02d}", _make_pin_test(pin["path"], pin["sha256"]))


def _make_selector_test(selector: dict[str, Any]):
    cid = selector["challenge_id"]
    def test(self: unittest.TestCase) -> None:
        v2c_matches = [item for item in V2C["selectors"] if item.get("challenge_id") == cid]
        self.assertEqual(len(v2c_matches), 1)
        v2c = v2c_matches[0]
        self.assertEqual(v2c.get("family_id"), EXPECTED_FAMILY[cid])
        self.assertEqual(v2c.get("mechanic"), selector.get("mechanic"))
        self.assertEqual(v2c.get("source_path"), selector.get("challenge_source_path"))
        self.assertEqual(v2c.get("source_sha256"), selector.get("challenge_source_sha256"))
        self.assertEqual(RUNTIME.family_for_selector(ROOT, selector), EXPECTED_FAMILY[cid])
        self.assertEqual(selector.get("custom_data_candidate_field"), EXPECTED_CANDIDATES[cid])
    return test


for selector in DESIGN["selectors"]:
    test_name = "test_" + selector["challenge_id"].lower() + "_family_lineage_and_candidate_scope"
    setattr(IndividualSelectorFamilyTests, test_name, _make_selector_test(selector))


class RuntimeContractFamilyNegativeTests(unittest.TestCase):
    def test_family_resolver_rejects_unknown_selector(self):
        with self.assertRaises(RUNTIME.ContractError):
            RUNTIME.family_for_selector(ROOT, {"challenge_id": "CHALLENGE_999", "mechanic": "unknown"})

    def test_family_resolver_rejects_mechanic_mismatch(self):
        selector = dict(DESIGN["selectors"][0])
        selector["mechanic"] = "wrong_mechanic"
        with self.assertRaises(RUNTIME.ContractError):
            RUNTIME.family_for_selector(ROOT, selector)

    def test_family_resolver_rejects_source_hash_mismatch(self):
        selector = dict(DESIGN["selectors"][0])
        selector["challenge_source_sha256"] = "0" * 64
        with self.assertRaises(RUNTIME.ContractError):
            RUNTIME.family_for_selector(ROOT, selector)


class ReportingTestRunner(unittest.TextTestRunner):
    def run(self, test: unittest.TestSuite) -> unittest.result.TestResult:
        result = super().run(test)
        if result.wasSuccessful():
            print(f"C11D_V2B_RUNTIME_IMPLEMENTATION_TESTS_PASS={result.testsRun}/{result.testsRun}")
        else:
            print(f"C11D_V2B_RUNTIME_IMPLEMENTATION_TESTS_FAIL={len(result.failures)}_FAILURES_{len(result.errors)}_ERRORS")
        return result


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    outcome = ReportingTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if outcome.wasSuccessful() else 1)
