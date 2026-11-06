from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

import c11e_e4b_loop_family_matrix as matrix

ROOT = Path(__file__).resolve().parents[3]


class LoopFamilyMatrixTests(unittest.TestCase):
    def setUp(self) -> None:
        self.template = matrix._default_cli_template(ROOT)

    def test_registry_has_exactly_five_families_and_27_concrete_grammars(self) -> None:
        selectors = matrix.enumerate_loop_selectors(ROOT)
        self.assertEqual(len(selectors), 27)
        self.assertEqual(
            {family: sum(row["family_id"] == family for row in selectors) for family in matrix.EXPECTED_FAMILY_GRAMMAR_COUNTS},
            matrix.EXPECTED_FAMILY_GRAMMAR_COUNTS,
        )
        self.assertEqual(len({(row["family_id"], row["subtype_id"]) for row in selectors}), 27)

    def test_family_music_profile_map_is_read_from_frozen_c11c_registry(self) -> None:
        selectors = matrix.enumerate_loop_selectors(ROOT)
        observed = {}
        for row in selectors:
            observed[row["family_id"]] = row["music_profile_id"]
        self.assertEqual(observed, matrix.EXPECTED_FAMILY_MUSIC_PROFILES)

    def test_template_rejects_non_loop_content(self) -> None:
        invalid = copy.deepcopy(self.template)
        invalid["selection"]["content_type"] = "challenges"
        with self.assertRaises(matrix.LoopFamilyMatrixError):
            matrix._validate_template(invalid, "CLI")

    def test_template_rejects_equal_seed_domains(self) -> None:
        invalid = copy.deepcopy(self.template)
        invalid["music_seed"] = invalid["seed"]
        with self.assertRaises(matrix.LoopFamilyMatrixError):
            matrix._validate_template(invalid, "CLI")

    def test_template_rejects_challenge_presentation_options(self) -> None:
        invalid = copy.deepcopy(self.template)
        invalid["presentation_options"] = {"show_hook_countdown": True}
        with self.assertRaises(matrix.LoopFamilyMatrixError):
            matrix._validate_template(invalid, "CLI")

    def test_template_rejects_production_mode(self) -> None:
        invalid = copy.deepcopy(self.template)
        invalid["mode"] = "PRODUCTION"
        with self.assertRaises(matrix.LoopFamilyMatrixError):
            matrix._validate_template(invalid, "CLI")

    def test_case_builder_preserves_family_selector_and_mutates_one_seed_domain(self) -> None:
        selector = matrix.enumerate_loop_selectors(ROOT)[0]
        baseline = matrix._build_case_request(self.template, selector, "BASELINE", 1, 314159, 840001)
        gameplay = matrix._build_case_request(self.template, selector, "GAMEPLAY_SEED_ONLY_CHANGED", 1, 314159, 840001)
        music = matrix._build_case_request(self.template, selector, "MUSIC_SEED_ONLY_CHANGED", 1, 314159, 840001)
        self.assertEqual(baseline["selection"], gameplay["selection"])
        self.assertEqual(baseline["selection"], music["selection"])
        self.assertEqual((gameplay["seed"], gameplay["music_seed"]), (314160, 840001))
        self.assertEqual((music["seed"], music["music_seed"]), (314159, 840002))

    def test_full_27_grammar_three_seed_scenario_d9_e1_matrix_passes(self) -> None:
        report = matrix.run_loop_family_matrix(ROOT, self.template, request_origin="CLI")
        self.assertEqual(report["status"], "PASS_LOOP_FAMILY_PLAN_MATRIX_ONLY")
        self.assertEqual(report["scope"]["family_count"], 5)
        self.assertEqual(report["scope"]["grammar_count"], 27)
        self.assertEqual(report["scope"]["case_count"], 81)
        self.assertEqual(len(report["seed_domain_relations"]), 27)
        self.assertTrue(all(all(row["checks"].values()) for row in report["seed_domain_relations"]))
        self.assertTrue(all(case["editorial_fields_preserved"] for case in report["cases"]))
        self.assertTrue(all(all(case["deterministic_repeat"].values()) for case in report["cases"]))
        self.assertTrue(all(all(case["governance"].values()) for case in report["cases"]))
        self.assertFalse(report["governance"]["renderer"])
        self.assertFalse(report["governance"]["renderer_input_emitted"])
        self.assertFalse(report["governance"]["renderer_dispatch_invoked"])
        self.assertFalse(report["governance"]["c11c_baseline_modified"])
        self.assertFalse(report["governance"]["godot_invoked"])
        self.assertFalse(report["governance"]["c11c_family_visual_generators_invoked"])
        self.assertFalse(report["governance"]["c11c_family_music_generator_invoked"])
        self.assertFalse(report["governance"]["d3_v5_invoked"])
        self.assertFalse(report["governance"]["ffmpeg_invoked"])
        self.assertEqual(report["governance"]["d4_8"], "BLOCKED")
        self.assertEqual(report["governance"]["d9_10"], "PREPARE_ONLY")
        self.assertEqual(report["governance"]["d9_14"], "BLOCKED")
        self.assertEqual(report["governance"]["d9_16"], "BLOCKED")
        self.assertEqual(report["governance"]["d9_17"], "BLOCKED_NO_GO")
        self.assertEqual(report["governance"]["d10"], "BLOCKED_FOR_PROMOTION")

    def test_report_written_add_only_and_hash_sidecar_matches(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "e4b_matrix"
            report = matrix.run_loop_family_matrix(ROOT, self.template, request_origin="CLI", output_root=output)
            report_bytes = (output / "matrix_report.json").read_bytes()
            sidecar = (output / "matrix_report.sha256").read_text(encoding="ascii").split()[0]
            template_path = output / "matrix_request_template.json"
            template_sidecar = (output / "matrix_request_template.sha256").read_text(encoding="ascii").split()[0]
            self.assertEqual(matrix._sha256_bytes(report_bytes), sidecar)
            self.assertEqual(matrix._sha256_bytes(template_path.read_bytes()), template_sidecar)
            self.assertEqual(report["scope"]["case_count"], 81)
            with self.assertRaises(matrix.LoopFamilyMatrixError):
                matrix.run_loop_family_matrix(ROOT, self.template, request_origin="CLI", output_root=output)

    def test_cli_rejects_gui_evidence_if_integrity_sidecar_is_tampered(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            gui_root = Path(tmp) / "gui"
            matrix.run_loop_family_matrix(ROOT, self.template, request_origin="GUI", output_root=gui_root)
            (gui_root / "matrix_request_template.sha256").write_text("0" * 64 + "  matrix_request_template.json\n", encoding="ascii")
            with self.assertRaises(matrix.LoopFamilyMatrixError):
                matrix._load_gui_matrix(ROOT, gui_root)

    def test_gui_cli_matrix_parity_checks_editorial_and_family_semantics(self) -> None:
        gui_template = matrix._validate_template(self.template, "GUI")
        gui = matrix.run_loop_family_matrix(ROOT, gui_template, request_origin="GUI")
        cli_template = matrix._validate_template(gui_template, "CLI")
        cli = matrix.run_loop_family_matrix(ROOT, cli_template, request_origin="CLI", compare_gui_report=gui)
        self.assertEqual(cli["gui_cli_parity"]["status"], "PASS_GUI_CLI_ALL_27_SELECTOR_PARITY_ONLY")
        self.assertEqual(cli["gui_cli_parity"]["case_count"], 81)

    def test_existing_producer_gui_exposes_matrix_action_in_d99_tab(self) -> None:
        source_path = ROOT / "c11c-suite" / "c11c-producer" / "main.py"
        source = source_path.read_text(encoding="utf-8")
        compile(source, str(source_path), "exec")
        self.assertIn("C11-E E4B · VALIDAR 5 FAMILIAS / 27 GRAMÁTICAS · PLAN ONLY", source)
        self.assertIn("self.d9_loop_family_matrix_button.clicked.connect(self._run_e4b_loop_family_matrix)", source)
        self.assertIn("self.d9_output_tabs.addTab(view, title)", source)
        self.assertIn("from c11e_e4b_loop_family_matrix import run_loop_family_matrix", source)
        self.assertNotIn("class C11ELoopProducer", source)

    def test_gui_matrix_action_is_review_only_and_exports_reusable_template(self) -> None:
        source = (ROOT / "c11c-suite" / "c11c-producer" / "main.py").read_text(encoding="utf-8")
        self.assertIn('self.d9_mode.currentData() or "") != "REVIEW"', source)
        self.assertIn('not self.d9_audio.isChecked() or not self.d9_personalization.isChecked()', source)
        self.assertIn('"request_origin": "GUI"', source)
        self.assertIn('"audio_enabled": True', source)
        self.assertIn('"personalization_enabled": True', source)
        self.assertIn('"e4b_loop_family_matrix"', source)
        self.assertNotIn("self.e3_last_intent_path = None", source[source.index("def _run_e4b_loop_family_matrix"):source.index("def _run_c11e_e3_audio_pilot")])


if __name__ == "__main__":
    unittest.main(verbosity=2)
