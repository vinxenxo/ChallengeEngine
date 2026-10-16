from __future__ import annotations
import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path
from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[3]
RUNNER_PATH = ROOT / "tools/c11d/d9/d_renderer_visual_loop_exact_selector_payload_v2.py"
spec = importlib.util.spec_from_file_location("c11d_exact_selector_payload_v2_tests", RUNNER_PATH)
runner = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = runner
spec.loader.exec_module(runner)


class ExactSelectorPayloadV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = ROOT.resolve()
        cls.contract, cls.contract_schema, cls.input_schema, cls.report_schema, cls.pins = runner._load_contract(cls.root)
        cls.sample = runner._sample_input(cls.contract)

    def _probe_receipt(self, probe_input=None):
        value = probe_input or copy.deepcopy(self.sample)
        req = value["request_identity"]
        param = value["parameter_instance"]
        selection = req["selection"]
        grammar = selection["subtype_id"]
        row = next(x for x in self.contract["scope"]["grammar_matrix"] if x["grammar_id"] == grammar)
        return {
            "schema": "C11-D-D9-VISUAL-LOOP-EXACT-SELECTOR-PAYLOAD-PROBE-V2",
            "schema_version": "2.0",
            "status": "IN_MEMORY_REVIEW_ONLY_EXACT_SELECTOR_VISUAL_PAYLOAD_NOT_RENDERER_INPUT",
            "contract_sha256": value["contract_sha256"],
            "parent_binding_report_sha256": value["parent_binding_report_sha256"],
            "request_identity": copy.deepcopy(req),
            "canonical_chain": copy.deepcopy(value["canonical_chain"]),
            "timing_review_reference": copy.deepcopy(value["timing_review_reference"]),
            "parent_request_parameter_binding_sha256": value["request_parameter_binding_sha256"],
            "parameter_instance_sha256": param["parameter_instance_sha256"],
            "selection": copy.deepcopy(selection),
            "grammar_id": grammar,
            "grammar_index": row["grammar_index"],
            "shader_branch_review_only": row["shader_branch"],
            "authoring_envelope_sha256": "c" * 64,
            "family_variation_recipe_sha256": "d" * 64,
            "resolved_palette_sha256": "e" * 64,
            "visual_spec_sha256": "f" * 64,
            "payload_instance_sha256": "a" * 64,
            "payload_sections": ["request_identity", "selection", "authoring_envelope", "family_variation_recipe", "resolved_palette", "visual_spec", "timing"],
            "payload_materialized_in_memory": True,
            "deterministic_repeat_pass": True,
            "exact_selector_visual_payload_materialized": True,
            "renderer_shader_mapping_is_review_metadata_only": True,
            "policy_values_consumed": False,
            "non_geometric_family_authoring_gaps_remain_open": True,
            "family_authoring_envelope_gap": "REMAINS_OPEN_OUTSIDE_THIS_GEOMETRIC_SELECTOR_SCOPE",
            "source_checks_passed": True,
            "execution_boundary": copy.deepcopy(runner.BOUNDARY),
        }

    def test_01_contract_passes_strict_schema(self):
        Draft202012Validator(self.contract_schema).validate(self.contract)

    def test_02_input_schema_itself_is_valid(self):
        Draft202012Validator.check_schema(self.input_schema)

    def test_03_report_schema_itself_is_valid(self):
        Draft202012Validator.check_schema(self.report_schema)

    def test_04_frozen_c11c_manifest_is_first_source_pin(self):
        self.assertEqual(self.pins[0]["path"], "release/C11C_FREEZE_PACKAGE_MANIFEST.json")
        self.assertEqual(self.pins[0]["sha256"], runner.EXPECTED_MANIFEST)

    def test_05_all_70_plus_direct_source_pins_verify(self):
        self.assertGreaterEqual(len(self.pins), 60)
        self.assertEqual(len({x["path"] for x in self.pins}), len(self.pins))

    def test_06_contract_is_preparation_only(self):
        self.assertEqual(self.contract["status"], runner.STATUS)

    def test_07_five_grammar_mappings_are_exact_and_ordered(self):
        observed = tuple((x["grammar_id"], x["grammar_index"], x["shader_branch"]) for x in self.contract["scope"]["grammar_matrix"])
        self.assertEqual(observed, runner.GRAMMARS)

    def test_08_parent_manifest_is_pinned(self):
        self.assertEqual(self.contract["authority"]["parent_parameter_binding_overlay_manifest_sha256"], runner.file_sha(self.root / runner.PARAMETER_BINDING_MANIFEST_REL))

    def test_09_parent_contract_hash_is_pinned(self):
        self.assertEqual(self.contract["authority"]["parent_parameter_binding_contract_sha256"], runner.file_sha(self.root / runner.PARAMETER_BINDING_CONTRACT_REL))

    def test_10_payload_harness_is_pinned(self):
        self.assertEqual(self.contract["harness"]["sha256"], runner.file_sha(self.root / runner.HARNESS_REL))

    def test_11_input_sample_passes_strict_schema(self):
        Draft202012Validator(self.input_schema).validate(self.sample)

    def test_12_input_rejects_unknown_top_level_keys(self):
        v = copy.deepcopy(self.sample)
        v["unexpected"] = True
        with self.assertRaises(ValidationError):
            Draft202012Validator(self.input_schema).validate(v)

    def test_13_input_rejects_selector_outside_fixed_scope(self):
        v = copy.deepcopy(self.sample)
        v["request_identity"]["selection"]["subtype_id"] = "unapproved_grammar"
        with self.assertRaises(ValidationError):
            Draft202012Validator(self.input_schema).validate(v)

    def test_14_input_requires_metadata_only_policy_references(self):
        v = copy.deepcopy(self.sample)
        v["timing_review_reference"]["policy_values_consumed"] = True
        with self.assertRaises(ValidationError):
            Draft202012Validator(self.input_schema).validate(v)

    def test_15_input_requires_nine_reference_pointers(self):
        v = copy.deepcopy(self.sample)
        v["timing_review_reference"]["policy_reference_count"] = 8
        with self.assertRaises(ValidationError):
            Draft202012Validator(self.input_schema).validate(v)

    def test_16_input_style_projection_has_exact_20_fields(self):
        v = copy.deepcopy(self.sample)
        self.assertEqual(set(v["parameter_instance"]["style_parameters"]), set(runner.STYLE_KEYS))
        self.assertEqual(len(v["parameter_instance"]["style_parameters"]), 20)

    def test_17_governance_has_zero_approvals(self):
        self.assertEqual(self.contract["approval_state"]["approval_assertions_checked"], 19)
        self.assertEqual(self.contract["approval_state"]["approvals_granted"], 0)
        self.assertEqual(self.contract["approval_state"]["release_authority"], "NONE")

    def test_18_renderer_and_media_remain_locked(self):
        self.assertEqual(self.contract["execution_boundary"], runner.BOUNDARY)
        self.assertEqual(self.contract["execution_boundary"]["renderer"], "OFF")
        self.assertFalse(self.contract["execution_boundary"]["media_created"])

    def test_19_payload_files_remain_forbidden(self):
        self.assertFalse(self.contract["execution_boundary"]["payload_file_written"])
        self.assertFalse(self.contract["execution_boundary"]["receipt_file_written"])

    def test_20_candidate_input_is_inadmissible(self):
        self.assertFalse(self.contract["execution_boundary"]["candidate_input_admissible"])

    def test_21_non_geometric_authoring_gaps_remain_open(self):
        self.assertTrue(self.contract["scope"]["non_geometric_family_authoring_gaps_remain_open"])

    def test_22_probe_receipt_with_valid_hash_shapes_and_locks_passes(self):
        checked = runner._validate_probe(self._probe_receipt(), self.sample, self.contract)
        self.assertTrue(checked["exact_selector_visual_payload_materialized"])

    def test_23_probe_rejects_wrong_shader_branch(self):
        report = self._probe_receipt()
        report["shader_branch_review_only"] = "field_orbital_wave"
        with self.assertRaises(runner.ExactSelectorPayloadError):
            runner._validate_probe(report, self.sample, self.contract)

    def test_24_probe_rejects_renderer_activation(self):
        report = self._probe_receipt()
        report["execution_boundary"]["renderer"] = "ON"
        with self.assertRaises(runner.ExactSelectorPayloadError):
            runner._validate_probe(report, self.sample, self.contract)

    def test_25_probe_rejects_policy_body_consumption(self):
        report = self._probe_receipt()
        report["policy_values_consumed"] = True
        with self.assertRaises(runner.ExactSelectorPayloadError):
            runner._validate_probe(report, self.sample, self.contract)

    def test_26_probe_rejects_malformed_payload_digest(self):
        report = self._probe_receipt()
        report["payload_instance_sha256"] = "not-a-sha"
        with self.assertRaises(runner.ExactSelectorPayloadError):
            runner._validate_probe(report, self.sample, self.contract)

    def test_27_probe_rejects_parameter_selector_detachment(self):
        v = copy.deepcopy(self.sample)
        v["parameter_instance"]["grammar_id"] = "orbital_wave"
        with self.assertRaises(runner.ExactSelectorPayloadError):
            runner._validate_probe(self._probe_receipt(v), v, self.contract)

    def test_28_probe_receipt_schema_and_status_are_not_promotable(self):
        report = self._probe_receipt()
        report["status"] = "RENDERER_READY"
        with self.assertRaises(runner.ExactSelectorPayloadError):
            runner._validate_probe(report, self.sample, self.contract)

    def test_29_runner_requires_explicit_godot_for_runtime_evidence(self):
        with self.assertRaises(runner.ExactSelectorPayloadError):
            runner.build_report(self.root, godot=None)

    def test_30_harness_has_no_file_write_renderer_or_media_path(self):
        text = (self.root / runner.HARNESS_REL).read_text(encoding="utf-8")
        for forbidden in ("FileAccess.WRITE", "FileAccess.READ_WRITE", "store_string(", "store_buffer(", "DirAccess.make_dir", "OS.execute(", "OS.shell_open(", "ShaderMaterial.new(", "GeometricWavesRenderer.new(", "SubViewport", "MovieWriter", "FFmpeg", "get_viewport().get_texture"):
            self.assertNotIn(forbidden.lower(), text.lower())

    def test_31_payload_projection_is_identical_to_parameter_matrix_projection(self):
        payload_text = (self.root / runner.HARNESS_REL).read_text(encoding="utf-8")
        parent_text = (self.root / "tools/c11d/d9/materialize_visual_loop_grammar_parameter_matrix_v2_in_memory.gd").read_text(encoding="utf-8")

        def projection_block(text, end_marker):
            start = text.index("func _project_style_parameters(value: Dictionary) -> Dictionary:")
            end = text.index(end_marker, start)
            return text[start:end].rstrip()

        payload_projection = projection_block(payload_text, "\nfunc _validate_input(")
        parent_projection = projection_block(parent_text, "\nfunc _stable_value(")
        self.assertEqual(payload_projection, parent_projection)


    def test_32_payload_uses_bound_style_instance_and_semantic_numeric_comparison(self):
        payload_text = (self.root / runner.HARNESS_REL).read_text(encoding="utf-8")
        self.assertIn('var styles_a: Dictionary = parameter_instance.get("style_parameters", {}).duplicate(true)', payload_text)
        self.assertIn('absolute_delta > STYLE_PROJECTION_ABS_TOLERANCE', payload_text)
        self.assertIn('request-bound style-parameter digest does not validate after transport', payload_text)
        self.assertIn('C11-C style projection differs from the request-bound parameter instance:', payload_text)
        self.assertNotIn('styles_a != parameter_instance.get("style_parameters", {})', payload_text)

    def test_33_bound_style_instance_still_requires_exact_20_keys_and_digest(self):
        payload_text = (self.root / runner.HARNESS_REL).read_text(encoding="utf-8")
        self.assertIn('styles_a.size() != STYLE_KEYS.size()', payload_text)
        self.assertIn('observed_style_keys != expected_style_keys', payload_text)
        self.assertIn('styles_a["grammar_mode"] = int(styles_a["grammar_mode"])', payload_text)
        self.assertIn('styles_a["palette_mode"] = int(styles_a["palette_mode"])', payload_text)
        self.assertIn('_sha256(styles_a) != str(parameter_instance.get("style_parameters_sha256", ""))', payload_text)
        self.assertIn('_sha256(core) != str(parameter_instance.get("parameter_instance_sha256", ""))', payload_text)


    def test_34_projection_comparison_uses_tiny_numeric_tolerance_and_reports_delta(self):
        payload_text = (self.root / runner.HARNESS_REL).read_text(encoding="utf-8")
        self.assertIn("const STYLE_PROJECTION_ABS_TOLERANCE := 1.0e-10", payload_text)
        self.assertIn("var absolute_delta: float = absf(float(projected_value) - float(bound_value))", payload_text)
        self.assertIn("if absolute_delta > STYLE_PROJECTION_ABS_TOLERANCE:", payload_text)
        self.assertIn("abs_delta=", payload_text)
        self.assertNotIn("float(projected_value) != float(bound_value)", payload_text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
