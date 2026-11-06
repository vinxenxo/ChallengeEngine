from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from e4b_loop_editorial_composition_proposal import (
    CANONICAL_FIELDS,
    LoopCompositionProposalError,
    build_layout,
    validate_proposal,
)

ROOT = Path(__file__).resolve().parents[3]
FIELDS_UNKNOWN = {"title": "UNKNOWN", "subtitle": "UNKNOWN", "call_to_action": "UNKNOWN", "language": "es"}
FIELDS_ACTIVE = {
    "title": "Título editorial Loop — composición armónica en movimiento",
    "subtitle": "Explora el patrón geométrico, observa sus ciclos y descubre cómo evoluciona la forma",
    "call_to_action": "Guarda este loop y comparte tu patrón favorito",
    "language": "es",
}


class LoopEditorialCompositionProposalTests(unittest.TestCase):
    def test_01_proposal_is_static_valid_and_unapproved(self):
        report = validate_proposal(ROOT)
        self.assertEqual(report["status"], "PASS_STATIC_PROPOSAL_VALIDATION_NOT_APPROVAL")
        self.assertFalse(report["renderer_native_input_emitted"])
        self.assertEqual(report["release_authority"], "NONE")

    def test_02_geometry_is_exact_9_16_and_yuv420p_aligned(self):
        p = json.loads((ROOT / "definitions/c11d/production/C11E_E4B_LOOP_EDITORIAL_COMPOSITION_PROPOSAL_V1.json").read_text(encoding="utf-8"))
        g = p["geometry"]
        self.assertEqual(g["canvas"]["width"] * 16, g["canvas"]["height"] * 9)
        frame = g["source_frame_viewport"]
        self.assertEqual(frame["width"] * 16, frame["height"] * 9)
        self.assertEqual((frame["x"], frame["y"], frame["width"], frame["height"]), (108, 192, 504, 896))
        self.assertTrue(all(v % 2 == 0 for v in (frame["x"], frame["y"], frame["width"], frame["height"])))

    def test_03_bands_do_not_overlap_source_frame(self):
        p = json.loads((ROOT / "definitions/c11d/production/C11E_E4B_LOOP_EDITORIAL_COMPOSITION_PROPOSAL_V1.json").read_text(encoding="utf-8"))
        g = p["geometry"]
        self.assertEqual(g["top_editorial_band"]["y"] + g["top_editorial_band"]["height"], g["source_frame_viewport"]["y"])
        self.assertEqual(g["source_frame_viewport"]["y"] + g["source_frame_viewport"]["height"], g["bottom_editorial_band"]["y"])
        self.assertEqual(g["bottom_editorial_band"]["y"] + g["bottom_editorial_band"]["height"], g["canvas"]["height"])

    def test_04_empty_visible_fields_keep_full_frame_and_all_keys(self):
        plan = build_layout(FIELDS_UNKNOWN)
        self.assertEqual(plan["visible_fields"], [])
        self.assertEqual(plan["geometry"]["mode"], "FULL_FRAME_PASSTHROUGH")
        self.assertEqual(set(plan["editorial_values"]), set(CANONICAL_FIELDS))
        self.assertEqual(plan["editorial_values"], FIELDS_UNKNOWN)

    def test_05_nonempty_visible_field_activates_contain_layout(self):
        plan = build_layout(FIELDS_ACTIVE)
        self.assertEqual(plan["visible_fields"], ["title", "subtitle", "call_to_action"])
        self.assertEqual(plan["geometry"]["mode"], "INSET_CONTAIN")
        self.assertEqual(plan["geometry"]["source_frame_viewport"], [108, 192, 504, 896])
        self.assertEqual(plan["geometry"]["uniform_scale"], 0.7)

    def test_06_language_is_metadata_only(self):
        values = dict(FIELDS_UNKNOWN, language="es-MX")
        plan = build_layout(values)
        self.assertEqual(plan["metadata_only_fields"], ["language"])
        self.assertNotIn("language", plan["visible_fields"])

    def test_07_full_span_windows_use_only_actual_supplied_frame_count(self):
        plan = build_layout(FIELDS_ACTIVE, frame_count=450)
        self.assertEqual([(x["field"], x["start_frame"], x["end_frame"]) for x in plan["visible_field_windows"]], [
            ("title", 0, 450), ("subtitle", 0, 450), ("call_to_action", 0, 450)
        ])
        self.assertEqual(plan["frame_span_source"], "ACTUAL_C11C_FAMILY_PAYLOAD_ONLY")
        self.assertEqual(build_layout(FIELDS_ACTIVE)["frame_span_source"], "NOT_AVAILABLE_IN_D9_REQUEST")

    def test_08_all_160_char_fields_fit_declared_line_budget(self):
        p = json.loads((ROOT / "definitions/c11d/production/C11E_E4B_LOOP_EDITORIAL_COMPOSITION_PROPOSAL_V1.json").read_text(encoding="utf-8"))
        blocks = p["geometry"]["editorial_text_blocks"]
        self.assertLessEqual(160, blocks["title"]["max_chars_per_line_conservative"] * blocks["title"]["max_lines"])
        self.assertLessEqual(160, blocks["subtitle"]["max_chars_per_line_conservative"] * blocks["subtitle"]["max_lines"])
        self.assertLessEqual(160, blocks["call_to_action"]["max_chars_per_line_conservative"] * blocks["call_to_action"]["max_lines"])
        self.assertLessEqual(blocks["title"]["max_lines"] * blocks["title"]["line_height_px"] + blocks["title"]["padding_vertical_px"], blocks["title"]["height"])
        self.assertLessEqual(blocks["subtitle"]["max_lines"] * blocks["subtitle"]["line_height_px"] + blocks["subtitle"]["padding_vertical_px"], blocks["subtitle"]["height"])
        self.assertLessEqual(blocks["call_to_action"]["max_lines"] * blocks["call_to_action"]["line_height_px"], blocks["call_to_action"]["height"])

    def test_09_native_c11c_and_matrix_invariants_are_explicit(self):
        p = json.loads((ROOT / "definitions/c11d/production/C11E_E4B_LOOP_EDITORIAL_COMPOSITION_PROPOSAL_V1.json").read_text(encoding="utf-8"))
        inv = p["ownership_invariants"]
        self.assertIn("PRESERVED_IN_SOURCE_FRAME", inv["c11c_native_header_footer_source_strings"])
        self.assertIn("PRESERVED_IN_SOURCE_FRAME", inv["c11c_matrix_sequence_and_timing"])
        self.assertFalse(inv["c11c_shared_layer_modified"])
        self.assertFalse(inv["c11c_family_scenes_modified"])
        self.assertFalse(inv["c11c_generator_or_music_source_modified"])

    def test_10_no_editorial_truncation_policy(self):
        p = json.loads((ROOT / "definitions/c11d/production/C11E_E4B_LOOP_EDITORIAL_COMPOSITION_PROPOSAL_V1.json").read_text(encoding="utf-8"))
        self.assertIn("NO_TRUNCATION_NO_ELLIPSIS_FAIL_CLOSED", p["geometry"]["overflow_policy"])

    def test_11_reject_missing_or_extra_canonical_fields(self):
        with self.assertRaises(LoopCompositionProposalError):
            build_layout({"title": "x", "subtitle": "x", "call_to_action": "x"})
        with self.assertRaises(LoopCompositionProposalError):
            build_layout(dict(FIELDS_UNKNOWN, extra="x"))

    def test_12_reject_non_string_and_overlength_fields(self):
        with self.assertRaises(LoopCompositionProposalError):
            build_layout(dict(FIELDS_UNKNOWN, title=None))
        with self.assertRaises(LoopCompositionProposalError):
            build_layout(dict(FIELDS_UNKNOWN, title="X" * 161))

    def test_13_reject_invalid_frame_counts(self):
        for frame_count in (0, -1, True, 1.5):
            with self.subTest(frame_count=frame_count):
                with self.assertRaises(LoopCompositionProposalError):
                    build_layout(FIELDS_ACTIVE, frame_count=frame_count)

    def test_14_proposal_cannot_be_promoted_by_editing_status(self):
        pth = ROOT / "definitions/c11d/production/C11E_E4B_LOOP_EDITORIAL_COMPOSITION_PROPOSAL_V1.json"
        data = json.loads(pth.read_text(encoding="utf-8"))
        data["status"] = "APPROVED"
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "definitions/c11d/production").mkdir(parents=True)
            (root / "release").mkdir(parents=True)
            (root / "definitions/c11d/production/C11E_E4B_LOOP_EDITORIAL_COMPOSITION_PROPOSAL_V1.json").write_text(json.dumps(data), encoding="utf-8")
            manifest = (ROOT / "release/C11C_FREEZE_PACKAGE_MANIFEST.json").read_bytes()
            (root / "release/C11C_FREEZE_PACKAGE_MANIFEST.json").write_bytes(manifest)
            with self.assertRaises(LoopCompositionProposalError):
                validate_proposal(root)

    def test_15_execution_boundary_is_fail_closed(self):
        plan = build_layout(FIELDS_ACTIVE, frame_count=450)
        self.assertFalse(plan["renderer_native_input_emitted"])
        self.assertFalse(plan["renderer_activation"])
        self.assertFalse(plan["production_dispatch"])
        self.assertFalse(plan["media_created"])
        self.assertEqual(plan["release_authority"], "NONE")

    def test_16_active_catalog_retains_five_families_and_27_concrete_grammars(self):
        schema = json.loads((ROOT / "c11c-suite/c11c-producer/producer_schema.json").read_text(encoding="utf-8"))
        expected = {
            "c11c_geometric_waves_v1": 5,
            "c11c_fractal_bloom_v1": 5,
            "c11c_sacred_symmetry_v1": 5,
            "c11c_living_particles_v1": 5,
            "c11c_invisible_forces_v1": 7,
        }
        families = schema["families"]
        self.assertEqual(set(families), set(expected))
        observed_total = 0
        for family_id, expected_count in expected.items():
            grammar_ids = [row[0] for row in families[family_id]["grammars"] if row[0] != "auto"]
            self.assertEqual(len(grammar_ids), expected_count, family_id)
            self.assertEqual(len(grammar_ids), len(set(grammar_ids)), family_id + " duplicate grammar")
            observed_total += len(grammar_ids)
        self.assertEqual(observed_total, 27)

    def test_17_family_music_profiles_are_preserved_for_all_loop_families(self):
        registry = json.loads((ROOT / "profiles/presentation/c11c_visual_music_profiles.json").read_text(encoding="utf-8"))
        bindings = registry["bindings"]
        expected = {
            "visual_loop/geometric": "CIRCUIT_PULSE",
            "visual_loop/fractal": "ORGANIC_BLOOM",
            "visual_loop/sacred_symmetry": "ORBITAL_RITUAL",
            "visual_loop/living_particles": "ORGANIC_BLOOM",
            "visual_loop/invisible_forces": "FLOWING_VECTOR",
        }
        for key, profile in expected.items():
            self.assertEqual(bindings[key]["profile"], profile, key)
            self.assertEqual(bindings[key]["music_semantic_inputs"], ["seed", "visual_grammar"], key)



if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(LoopEditorialCompositionProposalTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print("C11E E4B LOOP EDITORIAL COMPOSITION PROPOSAL " + ("PASS" if result.wasSuccessful() else "FAIL") + " | tests=17 | geometry=720x1280 | frame=504x896@0.7 | title/subtitle=4x19px | cta=3x22px | families=5/27 | proposal=NOT_APPROVED | renderer=OFF | media_created=false | release_authority=NONE")
    raise SystemExit(not result.wasSuccessful())
