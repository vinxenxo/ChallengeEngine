from __future__ import annotations

import ast
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(os.environ.get("C11E_PROJECT_ROOT", Path(__file__).resolve().parents[3])).resolve()
PRODUCER = ROOT / "c11c-suite" / "c11c-producer"
D9_DIR = ROOT / "tools" / "c11d" / "d9"
MAIN_SOURCE = Path(os.environ.get("C11E_D99_GUI_SOURCE_PATH", PRODUCER / "main.py")).resolve()
for import_path in (D9_DIR, PRODUCER):
    if str(import_path) not in sys.path:
        sys.path.insert(0, str(import_path))

from c11e_production_service import prepare_c11e_production_intent  # noqa: E402
from universal_producer import evaluate_universal_request  # noqa: E402


class E1GuiEditorialContractTests(unittest.TestCase):
    def test_gui_request_has_no_noncanonical_presentation_options(self) -> None:
        source = MAIN_SOURCE.read_text(encoding="utf-8")
        tree = ast.parse(source)
        method = next(
            node for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name == "_run_d9_universal_plan"
        )
        raw_request = next(
            node.value for node in ast.walk(method)
            if isinstance(node, ast.Assign)
            and any(isinstance(target, ast.Name) and target.id == "raw_request" for target in node.targets)
            and isinstance(node.value, ast.Dict)
        )
        keys = {key.value for key in raw_request.keys if isinstance(key, ast.Constant)}
        self.assertNotIn("presentation_options", keys)
        self.assertNotIn("d9_show_hook_countdown", source)
        self.assertIn('d9_request = dict(raw_request)', source)
        self.assertTrue({"personalization_enabled", "editorial_profile", "production_override"}.issubset(keys))

        build_tab = next(
            node for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name == "_build_d9_universal_editorial_tab"
        )
        editor_fields = next(
            node.value for node in ast.walk(build_tab)
            if isinstance(node, ast.Assign)
            and any(
                isinstance(target, ast.Attribute) and target.attr == "d9_editorial_fields"
                for target in node.targets
            )
            and isinstance(node.value, ast.Dict)
        )
        gui_fields = {key.value for key in editor_fields.keys if isinstance(key, ast.Constant)}
        self.assertEqual(
            gui_fields,
            {"title", "subtitle", "call_to_action", "language", "player_name", "challenge_label"},
        )

    def test_challenge_canonical_request_always_carries_all_six_editorial_fields(self) -> None:
        raw = {
            "schema": "C11-D-D9.9-UNIVERSAL-PRODUCER-REQUEST-V1",
            "schema_version": "1.0",
            "request_id": "C11E-D99-EDITORIAL-BLANK-CHALLENGE",
            "mode": "REVIEW",
            "selection": {"content_type": "challenges", "variant_id": "CHALLENGE_004"},
            "seed": 314159,
            "music_seed": 840001,
            "delivery_profile_id": "REVIEW_720",
            "presentation_profile_id": "social_default_v1",
            "variation_index": 0,
            "audio_enabled": True,
            "personalization_enabled": True,
            "editorial_profile": {},
            "production_override": {},
            "provenance": {"source_revision": "C11E-D99-EDITORIAL-CONTRACT", "request_origin": "TEST"},
        }
        expected = {"title", "subtitle", "call_to_action", "language", "player_name", "challenge_label"}
        d9 = evaluate_universal_request(raw, ROOT)
        self.assertEqual(set(d9["canonical_request"]["editorial"]), expected)
        self.assertEqual(set(d9["canonical_request"]["editorial"].values()), {"UNKNOWN"})

        e1 = prepare_c11e_production_intent(raw, ROOT, request_origin="TEST")
        self.assertEqual(set(e1["intent"]["editorial"]), expected)
        self.assertEqual(set(e1["intent"]["editorial"].values()), {"UNKNOWN"})

        # Even when the general personalization toggle is OFF, canonical field keys remain present.
        raw_disabled = dict(raw, request_id="C11E-D99-EDITORIAL-DISABLED-CHALLENGE", personalization_enabled=False)
        d9_disabled = evaluate_universal_request(raw_disabled, ROOT)
        self.assertEqual(set(d9_disabled["canonical_request"]["editorial"]), expected)

        # The option is E1-internal and keeps its existing default; it is never sent to D9.9.
        self.assertEqual(e1["intent"]["request"].get("presentation_options"), {"show_hook_countdown": True})
        self.assertNotIn("presentation_options", d9["canonical_request"])

    def test_loop_and_drill_keep_their_four_shared_editorial_fields(self) -> None:
        cases = [
            (
                "visual_loops",
                {"content_type": "visual_loops", "family_id": "c11c_geometric_waves_v1", "subtype_id": "harmonic_membrane"},
            ),
            (
                "visual_drills",
                {"content_type": "visual_drills", "family_id": "tracking", "variant_id": "tier-1"},
            ),
        ]
        expected = {"title", "subtitle", "call_to_action", "language"}
        for content_type, selection in cases:
            with self.subTest(content_type=content_type):
                raw = {
                    "schema": "C11-D-D9.9-UNIVERSAL-PRODUCER-REQUEST-V1",
                    "schema_version": "1.0",
                    "request_id": f"C11E-D99-EDITORIAL-BLANK-{content_type.upper()}",
                    "mode": "REVIEW",
                    "selection": selection,
                    "seed": 314159,
                    "music_seed": 840001,
                    "delivery_profile_id": "REVIEW_720",
                    "presentation_profile_id": "social_default_v1",
                    "variation_index": 0,
                    "audio_enabled": True,
                    "personalization_enabled": True,
                    "editorial_profile": {},
                    "production_override": {},
                    "provenance": {"source_revision": "C11E-D99-EDITORIAL-CONTRACT", "request_origin": "TEST"},
                }
                result = evaluate_universal_request(raw, ROOT)
                self.assertEqual(set(result["canonical_request"]["editorial"]), expected)
                self.assertEqual(set(result["canonical_request"]["editorial"].values()), {"UNKNOWN"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
