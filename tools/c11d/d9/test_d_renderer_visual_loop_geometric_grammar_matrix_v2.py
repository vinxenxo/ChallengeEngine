from __future__ import annotations
import base64
import copy
import json
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import d_renderer_visual_loop_geometric_grammar_matrix_v2 as audit

ROOT = HERE.parents[2]


def _mock_probe_input(command: list[str]) -> dict:
    token = command[-1]
    return json.loads(base64.b64decode(token.encode("ascii")).decode("utf-8"))


def _fake_probe_report(probe_input: dict) -> dict:
    cases = []
    for grammar in audit.GRAMMAR_MATRIX:
        for seed in audit.SEEDS:
            idx = grammar["grammar_index"]
            style = {
                "grammar_mode": idx,
                "palette_mode": (seed + idx) % 5,
                "morph": 0.25 + (seed % 17) / 100.0,
                "wave_frequency": 10.0 + (seed % 10) + idx,
                "line_width": 0.005 + (seed % 10) / 10000.0,
                "glow_strength": 0.4 + (seed % 5) * 0.03,
                "polygon_sides": float(5 + ((seed + idx) % 4)),
                "wave_ratio": 0.7 + (seed % 20) / 100.0,
                "shape_rotation": -0.4 + (seed % 80) / 100.0,
                "layer_spread": 0.02 + (seed % 50) / 1000.0,
                "radial_wave_amplitude": 0.012 + (seed % 40) / 1000.0,
                "liss_x_frequency": float(5 + (seed % 7)),
                "liss_y_frequency": float(3 + (seed % 6)),
                "interference_scale": 0.75 + (seed % 50) / 100.0,
                "hero_scale": 0.81 + (seed % 20) / 100.0,
                "perspective_strength": 0.36 + (seed % 60) / 100.0,
                "depth_strength": 0.43 + (seed % 45) / 100.0,
                "secondary_phase": -1.0 + (seed % 100) / 50.0,
                "color_phase": -3.0 + (seed % 600) / 100.0,
                "stroke_scale": 0.79 + (seed % 40) / 100.0,
            }
            identity = {
                "schema": "C11-D-D9-VISUAL-LOOP-GEOMETRIC-GRAMMAR-PARAMETER-INSTANCE-V2",
                "schema_version": "2.0",
                "selection": {"content_type": "visual_loops", "family_id": "c11c_geometric_waves_v1", "subtype_id": grammar["grammar_id"], "variant_id": None},
                "grammar_id": grammar["grammar_id"],
                "grammar_index": idx,
                "shader_branch": grammar["shader_branch"],
                "shader_uniform": "grammar_mode",
                "gameplay_seed": seed,
                "style_parameter_count": 20,
                "style_parameters": style,
            }
            digest = audit._sha_json(style)
            instance = audit._sha_json(identity)
            before = audit.GRAMMAR_MATRIX[(seed + idx) % len(audit.GRAMMAR_MATRIX)]["grammar_id"]
            cases.append({
                "grammar_id": grammar["grammar_id"],
                "grammar_index": idx,
                "shader_branch": grammar["shader_branch"],
                "gameplay_seed": seed,
                "seed_profile_grammar_before_override": before,
                "style_parameter_count": 20,
                "style_parameters": style,
                "repeat_style_parameters": copy.deepcopy(style),
                "style_sha256": digest,
                "repeat_style_sha256": digest,
                "parameter_instance_sha256": instance,
                "repeat_parameter_instance_sha256": instance,
                "deterministic_repeat": True,
            })
    return {
        "schema": audit.PROBE_SCHEMA_ID,
        "schema_version": "2.0",
        "status": "PREPARATION_ONLY_GEOMETRIC_GRAMMAR_PARAMETER_MATRIX_NOT_CANONICAL_REQUEST_BINDING_NOT_RENDERER_INPUT",
        "contract_sha256": probe_input["contract_sha256"],
        "frozen_c11c_manifest_sha256": audit.EXPECTED_MANIFEST_SHA256,
        "selection_family": {"content_type": "visual_loops", "family_id": "c11c_geometric_waves_v1"},
        "grammar_count": 5,
        "seed_values": list(audit.SEEDS),
        "cases": cases,
        "checks": {
            "case_count": 20,
            "expected_case_count": 20,
            "all_five_grammar_indices_bound": True,
            "style_parameters_per_case": 20,
            "same_seed_repeat_deterministic": True,
            "gameplay_seed_variation_per_grammar": True,
            "profile_copy_only": True,
            "source_checks_passed": True,
        },
        "execution_boundary": copy.deepcopy(audit.BOUNDARY),
    }


class VisualLoopGeometricGrammarMatrixV2Tests(unittest.TestCase):
    def _mock_process_runner(self, command, **kwargs):
        if command[-1] == "--version":
            return SimpleNamespace(returncode=0, stdout=audit.EXPECTED_GODOT_VERSION, stderr="")
        probe_input = _mock_probe_input(command)
        report = _fake_probe_report(probe_input)
        return SimpleNamespace(returncode=0, stdout=audit.PROBE_PREFIX + json.dumps(report, separators=(",", ":")), stderr="")

    def test_contract_has_exact_frozen_manifest_and_twelve_pins(self):
        contract, _, _, _, _, lineage = audit.load_contract(ROOT)
        self.assertEqual(contract["source_of_truth"]["frozen_c11c_manifest_sha256"], audit.EXPECTED_MANIFEST_SHA256)
        self.assertEqual(len(lineage), 12)
        self.assertEqual(lineage[0]["path"], audit.MANIFEST_REL.as_posix())

    def test_probe_uses_exact_field_validation_for_json_numeric_grammar_indices(self):
        probe_source = (ROOT / audit.HARNESS_REL).read_text(encoding="utf-8")
        self.assertNotIn("rows[index] != GRAMMAR_MATRIX[index]", probe_source)
        self.assertIn('var row_keys: Array = row.keys()', probe_source)
        self.assertIn('var grammar_index_value: Variant = row.get("grammar_index", null)', probe_source)
        self.assertIn('numeric_index != float(expected_row["grammar_index"])', probe_source)
        self.assertIn('shader_branch mismatch at index %s', probe_source)

    def test_probe_validates_json_numeric_seed_values_without_array_type_equality(self):
        probe_source = (ROOT / audit.HARNESS_REL).read_text(encoding="utf-8")
        self.assertNotIn("seeds != SEEDS", probe_source)
        self.assertIn('seeds.size() != SEEDS.size()', probe_source)
        self.assertIn('var seed_value: Variant = seeds[seed_index]', probe_source)
        self.assertIn('typeof(seed_value) != TYPE_INT and typeof(seed_value) != TYPE_FLOAT', probe_source)
        self.assertIn('numeric_seed != float(SEEDS[seed_index])', probe_source)
        self.assertIn('not is_finite(numeric_seed)', probe_source)

    def test_input_contains_only_five_geometric_grammars_and_four_seeds(self):
        contract, *_ = audit.load_contract(ROOT)
        probe_input = audit.build_input(ROOT, contract)
        self.assertEqual(len(probe_input["grammar_matrix"]), 5)
        self.assertEqual(probe_input["seeds"], list(audit.SEEDS))
        self.assertEqual(probe_input["grammar_matrix"], list(audit.GRAMMAR_MATRIX))

    def test_complete_twenty_case_matrix_passes_and_receipt_is_self_hashed(self):
        with patch.object(audit.subprocess, "run", side_effect=self._mock_process_runner):
            receipt = audit.run_audit("mock-godot.exe", 10, ROOT, audit.subprocess.run)
        self.assertEqual(receipt["matrix"]["cases"], 20)
        self.assertEqual(receipt["source_pin_count"], 12)
        self.assertTrue(audit._validate_receipt(receipt, ROOT, audit._read_json(ROOT / audit.AUDIT_SCHEMA_REL)))

    def test_duplicate_case_is_rejected(self):
        contract, *_ = audit.load_contract(ROOT)
        probe_input = audit.build_input(ROOT, contract)
        report = _fake_probe_report(probe_input)
        report["cases"][1] = copy.deepcopy(report["cases"][0])
        with self.assertRaisesRegex(audit.GrammarMatrixAuditError, "duplicate"):
            audit.validate_probe_report(report, probe_input, audit._read_json(ROOT / audit.PROBE_SCHEMA_REL))

    def test_missing_case_is_rejected(self):
        contract, *_ = audit.load_contract(ROOT)
        probe_input = audit.build_input(ROOT, contract)
        report = _fake_probe_report(probe_input)
        report["cases"].pop()
        with self.assertRaisesRegex(audit.GrammarMatrixAuditError, "exactly 20"):
            audit.validate_probe_report(report, probe_input, audit._read_json(ROOT / audit.PROBE_SCHEMA_REL))

    def test_repeat_hash_mismatch_is_rejected(self):
        contract, *_ = audit.load_contract(ROOT)
        probe_input = audit.build_input(ROOT, contract)
        report = _fake_probe_report(probe_input)
        report["cases"][0]["repeat_style_sha256"] = "0" * 64
        with self.assertRaisesRegex(audit.GrammarMatrixAuditError, "repeat digest mismatch"):
            audit.validate_probe_report(report, probe_input, audit._read_json(ROOT / audit.PROBE_SCHEMA_REL))

    def test_unvaried_gameplay_seed_matrix_is_rejected(self):
        contract, *_ = audit.load_contract(ROOT)
        probe_input = audit.build_input(ROOT, contract)
        report = _fake_probe_report(probe_input)
        grammar = audit.GRAMMAR_MATRIX[0]["grammar_id"]
        rows = [row for row in report["cases"] if row["grammar_id"] == grammar]
        for row in rows[1:]:
            row["style_parameters"] = copy.deepcopy(rows[0]["style_parameters"])
            row["repeat_style_parameters"] = copy.deepcopy(rows[0]["style_parameters"])
            row["style_sha256"] = audit._sha_json(row["style_parameters"])
            row["repeat_style_sha256"] = row["style_sha256"]
            core = {
                "schema": "C11-D-D9-VISUAL-LOOP-GEOMETRIC-GRAMMAR-PARAMETER-INSTANCE-V2",
                "schema_version": "2.0",
                "selection": {"content_type": "visual_loops", "family_id": "c11c_geometric_waves_v1", "subtype_id": row["grammar_id"], "variant_id": None},
                "grammar_id": row["grammar_id"], "grammar_index": row["grammar_index"],
                "shader_branch": row["shader_branch"], "shader_uniform": "grammar_mode",
                "gameplay_seed": row["gameplay_seed"], "style_parameter_count": 20,
                "style_parameters": row["style_parameters"],
            }
            row["parameter_instance_sha256"] = audit._sha_json(core)
            row["repeat_parameter_instance_sha256"] = row["parameter_instance_sha256"]
        with self.assertRaisesRegex(audit.GrammarMatrixAuditError, "did not produce varying style"):
            audit.validate_probe_report(report, probe_input, audit._read_json(ROOT / audit.PROBE_SCHEMA_REL))

    def test_governance_boundary_cannot_be_weakened(self):
        contract, *_ = audit.load_contract(ROOT)
        probe_input = audit.build_input(ROOT, contract)
        report = _fake_probe_report(probe_input)
        report["execution_boundary"]["renderer"] = "ON"
        with self.assertRaisesRegex(audit.GrammarMatrixAuditError, "governance/execution boundary"):
            audit.validate_probe_report(report, probe_input, audit._read_json(ROOT / audit.PROBE_SCHEMA_REL))

    def test_canonical_request_and_renderer_admission_remain_false(self):
        contract, *_ = audit.load_contract(ROOT)
        probe_input = audit.build_input(ROOT, contract)
        report = _fake_probe_report(probe_input)
        receipt = audit.build_receipt(ROOT, contract, contract["source_lineage"], audit.EXPECTED_GODOT_VERSION, report)
        self.assertFalse(receipt["findings"]["canonical_request_chain_admitted"])
        self.assertFalse(receipt["findings"]["exact_selector_payload_materialized"])
        self.assertFalse(receipt["findings"]["video_render_ready"])

    def test_nonzero_godot_exit_is_rejected(self):
        with patch.object(audit.subprocess, "run", return_value=SimpleNamespace(returncode=1, stdout="", stderr="engine failure")):
            with self.assertRaises(audit.GrammarMatrixAuditError):
                audit.run_audit("mock-godot.exe", 10, ROOT, audit.subprocess.run)

    def test_receipt_tampering_is_detected(self):
        contract, *_ = audit.load_contract(ROOT)
        probe_input = audit.build_input(ROOT, contract)
        report = _fake_probe_report(probe_input)
        receipt = audit.build_receipt(ROOT, contract, contract["source_lineage"], audit.EXPECTED_GODOT_VERSION, report)
        receipt["matrix"]["cases"] = 19
        with self.assertRaisesRegex(audit.GrammarMatrixAuditError, "audit SHA-256"):
            audit._validate_receipt(receipt, ROOT, audit._read_json(ROOT / audit.AUDIT_SCHEMA_REL))


if __name__ == "__main__":
    unittest.main(verbosity=2)
