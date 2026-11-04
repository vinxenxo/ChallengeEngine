from __future__ import annotations

import ast
import re
import unittest
from pathlib import Path

MAIN = Path(__file__).resolve().parent / "main.py"
SOURCE = MAIN.read_text(encoding="utf-8")
TREE = ast.parse(SOURCE)


def method_source(name: str) -> str:
    for node in ast.walk(TREE):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
            return ast.get_source_segment(SOURCE, node) or ""
    raise AssertionError(f"Method not found: {name}")


class C11EE3GuiIntegrationTests(unittest.TestCase):
    def test_e3_is_added_to_existing_universal_editorial_surface(self):
        build = method_source("_build_d9_universal_editorial_tab")
        self.assertIn("C11-E E3 · AUDIO + MUX PILOT", build)
        self.assertIn("self.d9_e3_audio_pilot_button.clicked.connect(self._run_c11e_e3_audio_pilot)", build)
        self.assertIn("self.d9_output_tabs.addTab(view, title)", build)
        self.assertIn("C11-E · E3 AUDIO + MUX PILOT (TEST ONLY)", build)

    def test_main_window_does_not_gain_a_sixth_or_extra_top_level_tab(self):
        build = method_source("_build")
        additions = re.findall(r"self\.tabs\.addTab\(", build)
        self.assertEqual(len(additions), 3, "E3 must remain inside the existing D9.9 editorial surface")
        self.assertNotIn("addTab(self._build_e3", build)
        self.assertNotIn("c11e-control", SOURCE.lower())

    def test_gui_action_prepares_shared_e1_intent_before_starting_e3_runner(self):
        action = method_source("_run_c11e_e3_audio_pilot")
        self.assertIn("self._run_d9_universal_plan()", action)
        self.assertIn("self.e3_last_intent_path", action)
        self.assertIn("runner = ROOT / \"c11e_e3_audio_pilot.py\"", action)
        self.assertIn("self.e3_process.start()", action)
        self.assertIn("--intent", action)
        self.assertIn("--source-video", action)
        self.assertIn("--operator-gui", action)

    def test_gui_pilot_uses_fixed_r4_provenance_and_test_only_output(self):
        action = method_source("_run_c11e_e3_audio_pilot")
        for expected in (
            'self.d9_seed.setValue(193847)',
            'self.d9_music_seed.setValue(840001)',
            'self.d9_delivery.findData("REVIEW_720")',
            'self.d9_variant.findData("CHALLENGE_001")',
            'C11E_E3_AUDIO_PILOT_TESTS',
            'setWorkingDirectory(str(PROJECT))',
        ):
            self.assertIn(expected, action)
        self.assertNotIn("godot", action.lower())
        self.assertNotIn("godot", action.lower())

    def test_challenge_hook_countdown_checkbox_flows_through_e1_without_expanding_d99_schema(self):
        build = method_source("_build_d9_universal_editorial_tab")
        type_changed = method_source("_d9_universal_type_changed")
        plan = method_source("_run_d9_universal_plan")
        self.assertIn('QCheckBox("Mostrar hook y countdown en Challenge")', build)
        self.assertIn('self.d9_show_hook_countdown.setChecked(True)', build)
        self.assertIn('self.d9_show_hook_countdown.setEnabled(content_type == "challenges")', type_changed)
        self.assertIn('"presentation_options": (', plan)
        self.assertIn('{"show_hook_countdown": bool(self.d9_show_hook_countdown.isChecked())}', plan)
        self.assertIn('d9_request.pop("presentation_options", None)', plan)
        self.assertIn('e1_intent["request"].get("presentation_options") == e_cli_intent["request"].get("presentation_options")', plan)

    def test_shared_cli_compatibility_is_not_removed(self):
        plan = method_source("_run_d9_universal_plan")
        self.assertIn('request_origin="GUI"', plan)
        self.assertIn('"--origin", "CLI"', plan)
        self.assertIn("e1_parity_checks", plan)
        self.assertIn('"semantic_intent_hash_equal"', plan)


if __name__ == "__main__":
    unittest.main(verbosity=2)
