from __future__ import annotations
import base64, copy, importlib.util, json, math, shutil, tempfile, unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[3]
RUNNER = ROOT / "tools/c11d/d9/d_renderer_visual_loop_request_scoped_grammar_parameter_binding_v2.py"
spec = importlib.util.spec_from_file_location("grammar_parameter_binding_v2_under_test", RUNNER)
audit = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = audit
assert spec.loader is not None
spec.loader.exec_module(audit)


def fake_probe(probe_input: dict, contract: dict) -> dict:
    req = probe_input["request"]
    selection = copy.deepcopy(req["selection"])
    row = next(x for x in contract["scope"]["grammar_matrix"] if x["grammar_id"] == selection["subtype_id"])
    idx = row["grammar_index"]
    style = {key: float((i + 2) / 10.0) for i, key in enumerate(audit.STYLE_KEYS)}
    style["grammar_mode"] = idx
    style_core = copy.deepcopy(style)
    instance_core = {
        "schema": "C11-D-D9-VISUAL-LOOP-GRAMMAR-PARAMETER-INSTANCE-V2",
        "schema_version": "2.0",
        "selection": selection,
        "grammar_id": row["grammar_id"],
        "grammar_index": idx,
        "shader_branch": row["shader_branch"],
        "shader_uniform": "grammar_mode",
        "style_parameter_count": 20,
        "style_parameters": style_core,
        "gameplay_seed": req["seed"],
        "request_hash": req["request_hash"],
    }
    instance = copy.deepcopy(instance_core)
    instance["style_parameters_sha256"] = audit.digest(style_core)
    instance["parameter_instance_sha256"] = audit.digest(instance_core)
    report = {
        "schema": "C11-D-D9-VISUAL-LOOP-GRAMMAR-PARAMETER-MATRIX-PROBE-V2",
        "schema_version": "2.0",
        "status": "PREPARATION_ONLY_REQUEST_BOUND_GRAMMAR_PARAMETER_INSTANCE_IN_MEMORY_NOT_EXACT_VISUAL_PAYLOAD",
        "contract_sha256": probe_input["contract_sha256"],
        "request_id": req["request_id"],
        "request_hash": req["request_hash"],
        "selection": selection,
        "gameplay_seed": req["seed"],
        "music_seed": req["music_seed"],
        "variation_index": req["variation_index"],
        "presentation_profile_id": req["presentation_profile_id"],
        "delivery_profile_id": req["delivery_profile_id"],
        "canonical_chain": copy.deepcopy(probe_input["canonical_chain"]),
        "timing_review_reference": copy.deepcopy(probe_input["timing_review_reference"]),
        "parameter_instance": instance,
        "repeat_deterministic": True,
        "source_checks_passed": True,
        **audit.PROBE_BOUNDARY,
    }
    return report


def fake_process_factory(contract, mutation=None):
    calls = []
    def fake_process(command, **kwargs):
        if command[-1] == "--version":
            calls.append((command, None, None))
            return SimpleNamespace(returncode=0, stdout=audit.EXPECTED_GODOT_VERSION + "\n", stderr="")
        probe_input = json.loads(base64.b64decode(command[-1]).decode("utf-8"))
        receipt = fake_probe(probe_input, contract)
        if mutation is not None:
            mutation(receipt)
        calls.append((command, probe_input, receipt))
        stdout = audit.PROBE_PREFIX + json.dumps(receipt, ensure_ascii=False, separators=(",", ":")) + "\n"
        stdout += "C11-D VISUAL LOOP GRAMMAR PARAMETER MATRIX V2 PROBE PASS\n"
        return SimpleNamespace(returncode=0, stdout=stdout, stderr="")
    return fake_process, calls


class GrammarParameterBindingV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract, cls.schema, cls.input_schema, cls.report_schema, cls.pins = audit._load_contract(ROOT)
        cls.fake_process, cls.runtime_calls = fake_process_factory(cls.contract)
        # Run the expensive parent-chain reconstruction once for the entire test class.
        cls.sample_report = audit._build_report(ROOT, "C:/Godot/Godot_v4.7.1-stable_win64_console.exe", 120, cls.fake_process)

    def test_contract_pins_frozen_manifest_first_and_45_sources(self):
        self.assertGreaterEqual(len(self.pins), 40)
        self.assertEqual(self.pins[0], {"path": "release/C11C_FREEZE_PACKAGE_MANIFEST.json", "sha256": audit.EXPECTED_MANIFEST})
        self.assertEqual(len({row["path"] for row in self.pins}), len(self.pins))
        self.assertEqual(len(self.pins), len(self.contract["source_lineage"]))

    def test_contract_fixes_five_selector_order_and_branches(self):
        actual = tuple((x["grammar_id"], x["grammar_index"], x["shader_branch"]) for x in self.contract["scope"]["grammar_matrix"])
        self.assertEqual(actual, audit.GRAMMARS)

    def test_contract_has_no_approval_or_release_authority(self):
        approval = self.contract["approval_state"]
        self.assertEqual(approval["approval_assertions_checked"], 19)
        self.assertEqual(approval["approvals_granted"], 0)
        self.assertEqual(approval["release_authority"], "NONE")
        self.assertTrue(all(value is False for key, value in approval.items() if key.endswith("_approved") or key.endswith("_authorized") or key in ("candidate_io_contract_complete", "renderer_baseline_frozen")))

    def test_contract_never_claims_exact_visual_payload_materialization(self):
        self.assertIs(self.contract["scope"]["exact_selector_visual_payload_materialized"], False)
        self.assertIs(self.contract["execution_boundary"]["renderer_native_input_emitted"], False)
        self.assertIs(self.contract["execution_boundary"]["media_created"], False)

    def test_schema_definitions_validate(self):
        from jsonschema import Draft202012Validator
        for schema in (self.schema, self.input_schema, self.report_schema):
            Draft202012Validator.check_schema(schema)
        Draft202012Validator(self.schema).validate(self.contract)

    def test_source_pins_cover_parent_matrix_contract_lineage(self):
        local = {row["path"]: row["sha256"] for row in self.pins}
        parent = json.loads((ROOT / "definitions/c11d/production/D_RENDERER_VISUAL_LOOP_REQUEST_SCOPED_BINDING_MATRIX_V2.json").read_text())
        for row in parent["source_lineage"]:
            self.assertEqual(local.get(row["path"]), row["sha256"])

    def test_input_schema_rejects_grammar_outside_exact_matrix(self):
        good = self._sample_input("harmonic_membrane")
        candidate = copy.deepcopy(good)
        candidate["request"]["selection"]["subtype_id"] = "made_up_grammar"
        from jsonschema import Draft202012Validator
        with self.assertRaises(Exception):
            Draft202012Validator(self.input_schema).validate(candidate)

    def test_input_schema_rejects_policy_value_consumption(self):
        candidate = self._sample_input("lattice_wave")
        candidate["timing_review_reference"]["policy_values_consumed"] = True
        from jsonschema import Draft202012Validator
        with self.assertRaises(Exception):
            Draft202012Validator(self.input_schema).validate(candidate)

    def test_input_schema_rejects_missing_chain_hash(self):
        candidate = self._sample_input("parametric_ribbon")
        del candidate["canonical_chain"]["plan_hash"]
        from jsonschema import Draft202012Validator
        with self.assertRaises(Exception):
            Draft202012Validator(self.input_schema).validate(candidate)

    def test_fake_godot_matrix_emits_five_bound_instances(self):
        report = self.sample_report
        self.assertEqual(len([x for x in self.runtime_calls if x[1] is not None]), 5)
        self.assertEqual(report["summary"]["request_parameter_bindings"], "5/5")
        self.assertEqual(report["summary"]["selected_grammar_parameter_instances_bound"], "5/5")
        self.assertEqual(report["summary"]["selected_grammar_payload_instances_bound"], "0/5")
        self.assertEqual(report["summary"]["policy_reference_pairs"], "45/45")
        self.assertEqual(report["governance"]["approvals_granted"], 0)
        self.assertIs(report["governance"]["candidate_input_admissible"], False)
        self.assertEqual([x["parameter_instance"]["grammar_index"] for x in report["cases"]], [0, 1, 2, 3, 4])

    def test_runner_sends_one_request_for_each_grammar(self):
        self.assertEqual([x[1]["request"]["selection"]["subtype_id"] for x in self.runtime_calls if x[1] is not None], [x[0] for x in audit.GRAMMARS])

    def test_request_parameter_binding_hashes_are_unique(self):
        report = self.sample_report
        hashes = [row["request_parameter_binding_sha256"] for row in report["cases"]]
        self.assertEqual(len(hashes), 5)
        self.assertEqual(len(set(hashes)), 5)

    def test_probe_rejects_different_request_hash(self):
        data = self._sample_input("harmonic_membrane")
        report = fake_probe(data, self.contract)
        report["request_hash"] = "f" * 64
        with self.assertRaises(audit.GrammarParameterBindingError):
            audit._validate_probe(report, data, self.contract)

    def test_probe_rejects_wrong_shader_branch(self):
        data = self._sample_input("interference_plane")
        report = fake_probe(data, self.contract)
        report["parameter_instance"]["shader_branch"] = "field_harmonic_membrane"
        core = {k: v for k, v in report["parameter_instance"].items() if k not in ("style_parameters_sha256", "parameter_instance_sha256")}
        report["parameter_instance"]["parameter_instance_sha256"] = audit.digest(core)
        with self.assertRaises(audit.GrammarParameterBindingError):
            audit._validate_probe(report, data, self.contract)

    def test_probe_rejects_renderer_activation(self):
        data = self._sample_input("orbital_wave")
        report = fake_probe(data, self.contract)
        report["renderer_native_input_emitted"] = True
        with self.assertRaises(audit.GrammarParameterBindingError):
            audit._validate_probe(report, data, self.contract)

    def test_probe_rejects_metadata_reference_value_consumption(self):
        data = self._sample_input("lattice_wave")
        report = fake_probe(data, self.contract)
        report["timing_review_reference"]["policy_values_consumed"] = True
        with self.assertRaises(audit.GrammarParameterBindingError):
            audit._validate_probe(report, data, self.contract)

    def test_probe_rejects_missing_style_parameter(self):
        data = self._sample_input("parametric_ribbon")
        report = fake_probe(data, self.contract)
        report["parameter_instance"]["style_parameters"].pop("glow_strength")
        with self.assertRaises(audit.GrammarParameterBindingError):
            audit._validate_probe(report, data, self.contract)

    def test_probe_rejects_non_finite_style_value(self):
        data = self._sample_input("orbital_wave")
        report = fake_probe(data, self.contract)
        report["parameter_instance"]["style_parameters"]["morph"] = float("nan")
        with self.assertRaises(audit.GrammarParameterBindingError):
            audit._validate_probe(report, data, self.contract)

    def test_probe_rejects_style_hash_mismatch(self):
        data = self._sample_input("harmonic_membrane")
        report = fake_probe(data, self.contract)
        report["parameter_instance"]["style_parameters_sha256"] = "0" * 64
        with self.assertRaises(audit.GrammarParameterBindingError):
            audit._validate_probe(report, data, self.contract)

    def test_probe_rejects_parameter_instance_hash_mismatch(self):
        data = self._sample_input("interference_plane")
        report = fake_probe(data, self.contract)
        report["parameter_instance"]["parameter_instance_sha256"] = "0" * 64
        with self.assertRaises(audit.GrammarParameterBindingError):
            audit._validate_probe(report, data, self.contract)

    def test_probe_rejects_forged_reference_envelope_digest(self):
        data = self._sample_input("parametric_ribbon")
        report = fake_probe(data, self.contract)
        report["timing_review_reference"]["selector_envelope_sha256"] = "f" * 64
        with self.assertRaises(audit.GrammarParameterBindingError):
            audit._validate_probe(report, data, self.contract)

    def test_probe_rejects_exact_payload_claim(self):
        data = self._sample_input("orbital_wave")
        report = fake_probe(data, self.contract)
        report["exact_selector_visual_payload_materialized"] = True
        with self.assertRaises(audit.GrammarParameterBindingError):
            audit._validate_probe(report, data, self.contract)

    def test_report_schema_rejects_promotion(self):
        report = copy.deepcopy(self.sample_report)
        report["summary"]["selected_grammar_payload_instances_bound"] = "5/5"
        from jsonschema import Draft202012Validator
        with self.assertRaises(Exception):
            Draft202012Validator(self.report_schema).validate(report)

    def test_harness_does_not_instantiate_renderer_or_write_files(self):
        source = (ROOT / audit.HARNESS_REL).read_text(encoding="utf-8")
        for token in ('Profile.build("geometric"', 'grammar_index', 'STYLE_KEYS', 'source_profile_copy_only=true'):
            self.assertIn(token.lower(), source.lower())
        for banned in ("ShaderMaterial.new", "GeometricWavesRenderer.new", "DirAccess.make_dir", "FileAccess.open(", "FileAccess.store_string"):
            self.assertNotIn(banned, source)

    def test_cli_requires_explicit_godot_runtime(self):
        source = RUNNER.read_text(encoding="utf-8")
        self.assertIn('parser.add_argument("--godot", required=True', source)
        self.assertIn('parser.add_argument("--timeout", type=float, default=120)', source)

    def _sample_input(self, grammar: str) -> dict:
        idx = next(i for i, row in enumerate(audit.GRAMMARS) if row[0] == grammar)
        return {
            "schema": "C11-D-D9-VISUAL-LOOP-GRAMMAR-PARAMETER-MATRIX-INPUT-V2",
            "schema_version": "2.0",
            "contract_sha256": "a" * 64,
            "frozen_c11c_manifest_sha256": audit.EXPECTED_MANIFEST,
            "request": {
                "schema": "C11-D-D9-DYNAMIC-REQUEST-PAYLOAD-INPUT-V1",
                "schema_version": "1.0",
                "request_id": f"TEST-{grammar.upper()}",
                "request_hash": "b" * 64,
                "selection": {"content_type": "visual_loops", "family_id": "c11c_geometric_waves_v1", "subtype_id": grammar, "variant_id": None},
                "seed": 12345,
                "music_seed": 840001,
                "variation_index": 0,
                "presentation_profile_id": "social_default_v1",
                "delivery_profile_id": "REVIEW_720",
            },
            "canonical_chain": {"plan_hash":"c"*64,"editorial_hash":"d"*64,"bridge_record_hash":"e"*64,"adapter_envelope_hash":"1"*64,"source_binding_sha256":"2"*64},
            "timing_review_reference": {"carrier_report_sha256":"3"*64,"selector_envelope_sha256":hex(0x100+idx)[2:].rjust(64,"0"),"shared_policy_reference_set_sha256":"4"*64,"policy_reference_count":9,"policy_values_consumed":False},
        }

if __name__ == "__main__":
    unittest.main(verbosity=2)
