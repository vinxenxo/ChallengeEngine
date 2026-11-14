from __future__ import annotations

import copy
import hashlib
import os
import sys
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from PySide6.QtGui import QColor, QImage

ROOT = Path(os.environ.get("C11E_TEST_PROJECT_ROOT", Path(__file__).resolve().parents[3])).resolve()
TOOLS = Path(os.environ.get("C11E_TEST_CONSUMER_MODULE_DIR", ROOT / "tools" / "c11d" / "d9")).resolve()
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))
import c11e_e4c_drill_visual_composition_consumer as consumer


class DrillVisualCompositionConsumerV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.composition, cls.schema, cls.timebase, cls.timebase_schema = consumer._verify_decision_and_proposals(ROOT)
        geometry = cls.composition["geometry"]
        cls.plan = {
            "schema": "C11E-E4C-DRILL-VISUAL-COMPOSITION-PLAN-V2",
            "status": "D_OWNED_V2_SOCIAL_BODY_CONSUMER_READY_FOR_ISOLATED_REQUALIFICATION",
            "approval": {
                "decision_record_sha256": consumer.DECISION_SHA,
                "composition_proposal_sha256": consumer.COMPOSITION_SHA,
                "timebase_proposal_sha256": consumer.TIMEBASE_SHA,
                "editorial_family_title_amendment_sha256": consumer.EDITORIAL_STYLE_AMENDMENT_SHA,
                "editorial_role_style_amendment_sha256": consumer.EDITORIAL_ROLE_STYLE_AMENDMENT_SHA,
                "status": "USER_DIRECTED_V2_D_OWNED_CONTRACT_ONLY",
            },
            "geometry": geometry,
            "selection": {"content_type": "visual_drills", "family_id": "tracking", "variant_id": "tier-1"},
            "text": {
                "raw_editorial_preserved": True,
                "visible_fields": {
                    "title": "SEGUIMIENTO VISUAL · NIVEL 1",
                    "subtitle": "Sigue el objetivo con precisión",
                    "call_to_action": "Mantén la mirada en el objetivo",
                },
                "language_metadata_only": "es",
                "layout_static_for_sequence": True,
                "family_title_style": dict(consumer.FAMILY_TITLE_STYLE),
                "game_subtitle_block": dict(consumer.GAME_SUBTITLE_ROLE_BLOCK),
                "editorial_role_style_contract": consumer.EDITORIAL_ROLE_STYLE_CONTRACT,
                "phase_visibility": {"PRE_ROLL": True, "GAME": True, "END_CTA": False, "DONE": False},
                "field_phase_visibility": {
                    "title": ["PRE_ROLL", "GAME"],
                    "subtitle": ["GAME"],
                    "call_to_action": ["GAME"],
                },
            },
            "source_pins": {
                "presentation_profile": {
                    "path": consumer.PRESENTATION_PROFILE_REL,
                    "bytes": 8837,
                    "sha256": consumer.PRESENTATION_PROFILE_SHA,
                },
                "editorial_family_title_amendment": {
                    "path": consumer.EDITORIAL_STYLE_AMENDMENT_REL,
                    "sha256": consumer.EDITORIAL_STYLE_AMENDMENT_SHA,
                },
                "editorial_role_style_amendment": {"path": consumer.EDITORIAL_ROLE_STYLE_AMENDMENT_REL, "sha256": consumer.EDITORIAL_ROLE_STYLE_AMENDMENT_SHA},
                "c11c_editorial_layer": {"path": consumer.C11C_EDITORIAL_LAYER_REL, "sha256": consumer.C11C_EDITORIAL_LAYER_SHA},
                "c11c_typography": {"path": consumer.C11C_TYPOGRAPHY_REL, "sha256": consumer.C11C_TYPOGRAPHY_SHA},
                "drill_palette_bank": {"path": consumer.DRILL_PALETTE_BANK_REL, "sha256": consumer.DRILL_PALETTE_BANK_SHA},
            },
            "governance": {
                "renderer_native_input_emitted": False, "renderer_dispatch_invoked": False,
                "renderer_activation": False, "godot_invoked": False, "ffmpeg_invoked": False,
                "media_created": False, "audio_generated": False, "c11c_source_mutation": False,
                "release_authority": "NONE",
            },
        }
        cls.plan["plan_sha256"] = consumer._json_sha(cls.plan)
        cls.app = consumer._ensure_qt_app()
        cls.source = QImage(720, 1280, QImage.Format.Format_RGB888)
        cls.source.fill(QColor(20, 30, 40))
        painter = consumer.QPainter(cls.source)
        painter.fillRect(0, 0, 720, 192, QColor(170, 10, 20))
        # Exact C11C TRACKING/AQUAMARINE_SUN native GAME body background.
        painter.fillRect(0, 192, 720, 896, QColor(3, 17, 13))
        painter.fillRect(0, 1088, 720, 192, QColor(10, 20, 170))
        painter.end()
        cls.source_hash = consumer._image_rgb_sha256(cls.source)

    def test_01_exact_v2_proposal_schema_decision_and_timebase_pins(self):
        self.assertEqual(consumer._sha_file(ROOT / consumer.COMPOSITION_PROPOSAL_REL), consumer.COMPOSITION_SHA)
        self.assertEqual(consumer._sha_file(ROOT / consumer.COMPOSITION_SCHEMA_REL), consumer.COMPOSITION_SCHEMA_SHA)
        self.assertEqual(consumer._sha_file(ROOT / consumer.DECISION_REL), consumer.DECISION_SHA)
        self.assertEqual(consumer._sha_file(ROOT / consumer.TIMEBASE_PROPOSAL_REL), consumer.TIMEBASE_SHA)
        self.assertEqual(consumer._sha_file(ROOT / consumer.TIMEBASE_SCHEMA_REL), consumer.TIMEBASE_SCHEMA_SHA)
        self.assertEqual(consumer._sha_file(consumer._editorial_amendment_path(ROOT)), consumer.EDITORIAL_STYLE_AMENDMENT_SHA)
        self.assertEqual(consumer._sha_file(consumer._editorial_role_style_amendment_path(ROOT)), consumer.EDITORIAL_ROLE_STYLE_AMENDMENT_SHA)
        self.assertEqual(consumer._sha_file(ROOT / consumer.C11C_EDITORIAL_LAYER_REL), consumer.C11C_EDITORIAL_LAYER_SHA)
        self.assertEqual(consumer._sha_file(ROOT / consumer.C11C_TYPOGRAPHY_REL), consumer.C11C_TYPOGRAPHY_SHA)
        self.assertEqual(consumer._sha_file(ROOT / consumer.DRILL_PALETTE_BANK_REL), consumer.DRILL_PALETTE_BANK_SHA)

    def test_02_geometry_is_exact_full_width_social_regions(self):
        g = self.plan["geometry"]
        self.assertEqual(g["canvas"], {"x": 0, "y": 0, "width": 720, "height": 1280, "aspect_ratio": "9:16"})
        self.assertEqual(g["header_rect"], {"x": 0, "y": 0, "width": 720, "height": 192})
        self.assertEqual(g["body_rect"], {"x": 0, "y": 192, "width": 720, "height": 896})
        self.assertEqual(g["footer_rect"], {"x": 0, "y": 1088, "width": 720, "height": 192})
        self.assertEqual(g["source_frame_viewport"], g["body_rect"])

    def test_03_source_profile_authority_is_exact_and_pinned(self):
        self.assertEqual(consumer._sha_file(ROOT / consumer.PRESENTATION_PROFILE_REL), consumer.PRESENTATION_PROFILE_SHA)
        self.assertEqual(self.plan["source_pins"]["presentation_profile"]["bytes"], 8837)

    def test_04_v1_centered_contain_geometry_is_rejected(self):
        altered = copy.deepcopy(self.plan)
        altered["geometry"]["source_frame_viewport"] = {"x": 108, "y": 192, "width": 504, "height": 896}
        altered["plan_sha256"] = consumer._json_sha({k: v for k, v in altered.items() if k != "plan_sha256"})
        with self.assertRaises(consumer.DrillVisualConsumerError):
            consumer.validate_plan(altered)

    def test_05_preroll_replaces_family_title_from_first_frame_and_preserves_native_body(self):
        result = consumer.compose_frame(self.source, self.plan, "PRE_ROLL", 0, 630, 30, 1, ROOT)
        self.assertEqual(result["mode"], "D_PREROLL_FAMILY_TITLE_REPLACEMENT_NATIVE_BODY_PRESERVED")
        self.assertTrue(result["native_title_replaced"])
        self.assertTrue(result["d_editorial_title_visible"])
        self.assertTrue(result["mapping"]["d_editorial_title_slot_open"])
        self.assertFalse(result["mapping"]["d_editorial_visible"])
        self.assertTrue(result["native_body_pixel_identity"])
        self.assertTrue(result["native_footer_pixel_identity"])
        self.assertEqual(consumer._image_rgb_bytes(result["image"].copy(0, 192, 720, 896)), consumer._image_rgb_bytes(self.source.copy(0, 192, 720, 896)))
        self.assertEqual(consumer._image_rgb_bytes(result["image"].copy(0, 1088, 720, 192)), consumer._image_rgb_bytes(self.source.copy(0, 1088, 720, 192)))
        self.assertNotEqual(consumer._image_rgb_bytes(result["image"].copy(0, 0, 720, 192)), consumer._image_rgb_bytes(self.source.copy(0, 0, 720, 192)))
        self.assertEqual(result["family_title_render"]["alignment"], "CENTER")
        self.assertEqual(result["family_title_render"]["font"], "Inter-Bold")
        self.assertEqual(result["family_title_render"]["font_size_px"], 22)

    def test_06_end_cta_is_complete_native_frame_passthrough(self):
        result = consumer.compose_frame(self.source, self.plan, "END_CTA", 720, 630, 30, 1, ROOT)
        self.assertEqual(result["mode"], "NATIVE_PHASE_FULL_FRAME_PASSTHROUGH")
        self.assertEqual(consumer._image_rgb_bytes(result["image"]), consumer._image_rgb_bytes(self.source))
        self.assertTrue(result["native_full_frame_identity"])
        self.assertFalse(result["mapping"]["d_editorial_visible"])

    def test_07_game_body_is_pixel_exact_and_same_position(self):
        result = consumer.compose_frame(self.source, self.plan, "GAME", 0, 630, 30, 1, ROOT)
        expected = self.source.copy(0, 192, 720, 896)
        actual = result["image"].copy(0, 192, 720, 896)
        self.assertEqual(consumer._image_rgb_bytes(actual), consumer._image_rgb_bytes(expected))
        self.assertTrue(result["native_body_pixel_identity"])
        self.assertEqual(result["mode"], "D_GAME_BODY_PIXEL_EXACT_FAMILY_TITLE_COMPOSITION")

    def test_08_native_header_and_footer_are_not_embedded_in_game_body(self):
        result = consumer.compose_frame(self.source, self.plan, "GAME", 200, 630, 30, 1, ROOT)
        output = result["image"]
        self.assertEqual(consumer._pixel_rgb(output, 350, 500), (3, 17, 13))
        self.assertEqual(consumer._pixel_rgb(output, 700, 190), (5, 7, 11))
        self.assertEqual(consumer._pixel_rgb(output, 700, 1279), (5, 7, 11))

    def test_09_same_family_title_style_is_used_in_preroll_and_game(self):
        pre = consumer.compose_frame(self.source, self.plan, "PRE_ROLL", 0, 630, 30, 1, ROOT)
        game = consumer.compose_frame(self.source, self.plan, "GAME", 0, 630, 30, 1, ROOT)
        self.assertTrue(pre["d_editorial_title_visible"])
        self.assertTrue(game["d_editorial_title_visible"])
        self.assertFalse(pre["mapping"]["d_editorial_visible"])
        self.assertTrue(game["mapping"]["d_editorial_visible"])
        self.assertEqual(pre["family_title_render"], game["family_title_render"])
        self.assertFalse(consumer.compose_frame(self.source, self.plan, "END_CTA", 720, 630, 30, 1, ROOT)["d_editorial_title_visible"])

    def test_10_family_title_subtitle_and_cta_use_distinct_approved_regions(self):
        result = consumer.compose_frame(self.source, self.plan, "GAME", 1, 630, 30, 1, ROOT)
        self.assertEqual(consumer.FAMILY_TITLE_STYLE["color_rgb"], [235, 215, 161])
        self.assertEqual(result["editorial_role_style_resolution"]["palette_name"], "AQUAMARINE_SUN")
        roles = result["editorial_role_render"]
        self.assertEqual(roles["subtitle"]["role"], "C11C_HEADER")
        self.assertEqual(roles["subtitle"]["font"], "Inter-Bold")
        self.assertEqual(roles["subtitle"]["font_size_px"], 22)
        self.assertEqual(roles["subtitle"]["alignment"], "CENTER")
        self.assertEqual(roles["subtitle"]["color_rgb"], [255, 249, 232])
        self.assertEqual(roles["subtitle"]["outline_width_px"], 1)
        self.assertEqual(roles["subtitle"]["vertical_alignment"], "BOTTOM")
        self.assertEqual(roles["call_to_action"]["role"], "C11C_FOOTER")
        self.assertEqual(roles["call_to_action"]["font"], "NotoSansMono-Regular")
        self.assertEqual(roles["call_to_action"]["font_size_px"], 16)
        self.assertEqual(roles["call_to_action"]["alignment"], "CENTER")
        self.assertEqual(roles["call_to_action"]["color_rgb"], [230, 255, 248])
        self.assertEqual(roles["call_to_action"]["outline_width_px"], 1)
        self.assertEqual(roles["call_to_action"]["vertical_alignment"], "TOP")
        regions = (
            ("family_title_gold", (36, 63, 648, 104), (180, 160, 110)),
            ("subtitle_palette", (36, 163, 648, 29), (180, 180, 180)),
            ("cta_palette", (36, 1151, 648, 66), (180, 180, 180)),
        )
        for label, rect, floor_rgb in regions:
            patch = result["image"].copy(*rect).convertToFormat(QImage.Format.Format_RGB888)
            raw = consumer._image_rgb_bytes(patch)
            qualifying = sum(
                1 for i in range(0, len(raw), 3)
                if raw[i] > floor_rgb[0] and raw[i + 1] > floor_rgb[1] and raw[i + 2] > floor_rgb[2]
            )
            self.assertGreater(qualifying, 8, f"{label} missing from its approved region")
        self.assertEqual(roles["subtitle"]["line_count"], 1)
        self.assertEqual(roles["call_to_action"]["line_count"], 1)

    def test_11_empty_editorial_uses_full_frame_passthrough(self):
        altered = copy.deepcopy(self.plan)
        altered["text"]["visible_fields"] = {}
        altered["text"]["phase_visibility"] = {"PRE_ROLL": False, "GAME": False, "END_CTA": False, "DONE": False}
        altered["text"]["field_phase_visibility"] = {"title": [], "subtitle": [], "call_to_action": []}
        altered["plan_sha256"] = consumer._json_sha({k: v for k, v in altered.items() if k != "plan_sha256"})
        result = consumer.compose_frame(self.source, altered, "GAME", 0, 630, 30, 1, ROOT)
        self.assertEqual(result["mode"], "UNCHANGED_FULL_FRAME_PASSTHROUGH")
        self.assertEqual(consumer._image_rgb_bytes(result["image"]), consumer._image_rgb_bytes(self.source))

    def test_12_input_frame_is_not_mutated(self):
        before = consumer._image_rgb_sha256(self.source)
        consumer.compose_frame(self.source, self.plan, "GAME", 9, 630, 30, 1, ROOT)
        self.assertEqual(consumer._image_rgb_sha256(self.source), before)
        self.assertEqual(before, self.source_hash)

    def test_13_timebase_remains_90_630_90_without_resampling(self):
        self.assertEqual(consumer.map_phase_frame("PRE_ROLL", 89, 630)["final_presentation_frame_index"], 89)
        self.assertEqual(consumer.map_phase_frame("GAME", 0, 630)["final_presentation_frame_index"], 90)
        self.assertEqual(consumer.map_phase_frame("GAME", 629, 630)["final_presentation_frame_index"], 719)
        self.assertEqual(consumer.map_phase_frame("END_CTA", 720, 630)["final_presentation_frame_index"], 720)
        self.assertEqual(self.timebase["candidate_mapping"]["pre_roll_frames"], "round(3.0 * actual_stream_fps)")

    def test_14_plan_hash_and_governance_are_valid(self):
        consumer.validate_plan(self.plan)
        for key in ("renderer_native_input_emitted", "renderer_dispatch_invoked", "renderer_activation", "godot_invoked", "ffmpeg_invoked", "media_created", "audio_generated", "c11c_source_mutation"):
            self.assertFalse(self.plan["governance"][key])
        self.assertEqual(self.plan["governance"]["release_authority"], "NONE")

    def test_15_plan_hash_detects_tampering(self):
        altered = copy.deepcopy(self.plan)
        altered["geometry"]["body_rect"]["x"] = 1
        with self.assertRaises(consumer.DrillVisualConsumerError):
            consumer.validate_plan(altered)

    def test_16_spanish_font_coverage_is_pinned_and_supported(self):
        sample = "¡Árbol, acción, niño! ¿Qué tal?"
        for rel in (consumer.INTER_FONT_REL, consumer.MONO_FONT_REL):
            cmap = consumer._font_codepoints(ROOT / rel)
            self.assertFalse({ord(ch) for ch in sample if not ch.isspace()} - cmap)
            font = consumer._font(ROOT, rel, 18)
            self.assertTrue(consumer.QRawFont.fromFont(font).isValid())

    def test_17_unavailable_glyph_fails_closed(self):
        altered = copy.deepcopy(self.plan)
        altered["text"]["visible_fields"]["title"] = "Unsupported glyph 🧿"
        altered["plan_sha256"] = consumer._json_sha({k: v for k, v in altered.items() if k != "plan_sha256"})
        with self.assertRaises(consumer.DrillVisualConsumerError):
            consumer.compose_frame(self.source, altered, "GAME", 0, 630, 30, 1, ROOT)

    def test_18_unknown_sentinel_is_suppressed_without_removing_canonical_keys(self):
        fields = consumer._filtered_fields({"title": "", "subtitle": " UNKNOWN ", "call_to_action": "unknown", "language": "es"})
        self.assertEqual(fields, {})

    def test_19_canvas_aspect_ratio_is_part_of_the_exact_geometry_contract(self):
        altered = copy.deepcopy(self.plan)
        altered["geometry"]["canvas"]["aspect_ratio"] = "1:1"
        altered["plan_sha256"] = consumer._json_sha({k: v for k, v in altered.items() if k != "plan_sha256"})
        with self.assertRaises(consumer.DrillVisualConsumerError):
            consumer.validate_plan(altered)

    def test_20_profile_logical_regions_project_exactly_to_review_720(self):
        source = self.composition["geometry"]["source_geometry_authority"]
        self.assertEqual(source["logical_source_canvas"], {"width": 540, "height": 960})
        self.assertAlmostEqual(source["pixel_scale"], 4.0 / 3.0, places=12)
        self.assertEqual(self.composition["geometry"]["canvas"], consumer.EXPECTED_SOCIAL_REGIONS["canvas"])
        self.assertEqual(self.composition["geometry"]["body_rect"], consumer.EXPECTED_SOCIAL_REGIONS["body_rect"])
        consumer.validate_plan(self.plan)

    def test_21_amendment_is_bound_by_exact_sha_in_plan_and_approval(self):
        self.assertEqual(self.plan["approval"]["editorial_family_title_amendment_sha256"], consumer.EDITORIAL_STYLE_AMENDMENT_SHA)
        self.assertEqual(self.plan["source_pins"]["editorial_family_title_amendment"]["sha256"], consumer.EDITORIAL_STYLE_AMENDMENT_SHA)

    def test_22_family_title_style_geometry_and_animation_match_source_observation(self):
        self.assertEqual(consumer.FAMILY_TITLE_STYLE["font_size_px"], 22)
        self.assertEqual(consumer.FAMILY_TITLE_STYLE["line_height_px"], 29)
        self.assertEqual(consumer.FAMILY_TITLE_STYLE["rect"], {"x": 36, "y": 63, "width": 648, "height": 104})
        self.assertEqual(consumer.FAMILY_TITLE_STYLE["color_rgb"], [235, 215, 161])
        self.assertEqual(consumer.GAME_SUBTITLE_BLOCK["y"], 169)
        self.assertEqual(consumer.GAME_SUBTITLE_ROLE_BLOCK["y"], 163)
        self.assertEqual(consumer.GAME_SUBTITLE_ROLE_BLOCK["font_size_px"], 22)
        self.assertEqual(consumer.FAMILY_TITLE_STYLE["animation"], "STATIC_NO_ANIMATION_OBSERVED_IN_TRACKING_TIER_1_PRE_ROLL")
        self.assertEqual(consumer.compose_frame(self.source, self.plan, "PRE_ROLL", 30, 630, 30, 1, ROOT)["family_title_render"]["animation"], consumer.FAMILY_TITLE_STYLE["animation"])

    def test_23_countdown_pixels_remain_exact_for_all_preroll_samples(self):
        for frame_index in (0, 15, 30, 45, 60, 75, 89):
            result = consumer.compose_frame(self.source, self.plan, "PRE_ROLL", frame_index, 630, 30, 1, ROOT)
            self.assertEqual(consumer._image_rgb_bytes(result["image"].copy(0, 192, 720, 896)), consumer._image_rgb_bytes(self.source.copy(0, 192, 720, 896)))

    def test_24_title_phase_visibility_rejects_late_only_title(self):
        altered = copy.deepcopy(self.plan)
        altered["text"]["phase_visibility"]["PRE_ROLL"] = False
        altered["plan_sha256"] = consumer._json_sha({k: v for k, v in altered.items() if k != "plan_sha256"})
        with self.assertRaises(consumer.DrillVisualConsumerError):
            consumer.validate_plan(altered)

    def test_25_subtitle_glyphs_do_not_overlap_family_title_glyphs(self):
        result = consumer.compose_frame(self.source, self.plan, "GAME", 0, 630, 30, 1, ROOT)
        title_rows = result["family_title_render"]["line_rows"]
        subtitle_rows = result["editorial_role_render"]["subtitle"]["line_rows"]
        title_bottom = max(row["glyph_bounds"][3] for row in title_rows)
        subtitle_top = min(row["glyph_bounds"][1] for row in subtitle_rows)
        self.assertGreaterEqual(subtitle_top, title_bottom)
        self.assertEqual(consumer.GAME_SUBTITLE_ROLE_BLOCK["y"] + consumer.GAME_SUBTITLE_ROLE_BLOCK["height"], 192)

    def test_26_preroll_footer_is_not_repainted_by_title_bridge(self):
        result = consumer.compose_frame(self.source, self.plan, "PRE_ROLL", 89, 630, 30, 1, ROOT)
        self.assertEqual(consumer._image_rgb_bytes(result["image"].copy(0, 1088, 720, 192)), consumer._image_rgb_bytes(self.source.copy(0, 1088, 720, 192)))

    def test_27_end_cta_remains_exact_full_frame_passthrough(self):
        result = consumer.compose_frame(self.source, self.plan, "END_CTA", 809, 630, 30, 1, ROOT)
        self.assertTrue(result["native_full_frame_identity"])
        self.assertEqual(consumer._image_rgb_bytes(result["image"]), consumer._image_rgb_bytes(self.source))

    def test_28_role_palette_resolver_reads_selected_family_palette_dynamically(self):
        resolved = consumer._resolve_native_palette_style(self.source, ROOT, "tracking")
        self.assertEqual(resolved["palette_name"], "AQUAMARINE_SUN")
        self.assertEqual(resolved["palette_background_rgb"], [3, 17, 13])
        self.assertEqual(resolved["header_secondary_rgb"], [255, 249, 232])
        self.assertEqual(resolved["footer_data_rgb"], [230, 255, 248])
        self.assertGreaterEqual(resolved["confidence_margin"], 1)

        # The accepted R6 native GAME body has median edge RGB (1,15,12).
        # Five palettes lie inside the old +/-8 radius; nearest-neighbor ranking
        # must select AQUAMARINE_SUN with a confidence margin of four levels.
        native_r6 = QImage(720, 1280, QImage.Format.Format_RGB888)
        native_r6.fill(QColor(1, 15, 12))
        resolved_native = consumer._resolve_native_palette_style(native_r6, ROOT, "tracking")
        self.assertEqual(resolved_native["palette_name"], "AQUAMARINE_SUN")
        self.assertEqual(resolved_native["max_channel_delta"], 2)
        self.assertEqual(resolved_native["runner_up_max_channel_delta"], 6)
        self.assertEqual(resolved_native["confidence_margin"], 4)

    def test_29_unmatched_or_ambiguous_native_palette_fails_closed(self):
        unknown = QImage(720, 1280, QImage.Format.Format_RGB888)
        unknown.fill(QColor(77, 81, 83))
        with self.assertRaises(consumer.DrillVisualConsumerError):
            consumer._resolve_native_palette_style(unknown, ROOT, "tracking")

        # This RGB is equidistant from AQUAMARINE_SUN and MOSS_CORAL (delta 2).
        # A tie must never silently choose by ordering.
        ambiguous = QImage(720, 1280, QImage.Format.Format_RGB888)
        ambiguous.fill(QColor(5, 17, 12))
        with self.assertRaises(consumer.DrillVisualConsumerError):
            consumer._resolve_native_palette_style(ambiguous, ROOT, "tracking")

    def test_30_all_four_drill_families_have_distinct_pinned_palette_rows(self):
        for family in consumer.DRILL_FAMILIES:
            rows = consumer._drill_palette_rows(str(ROOT), family)
            self.assertEqual(len(rows), 24)
            self.assertEqual(len({tuple(row["background_rgb"]) for row in rows}), 24)
            for row in rows:
                source = QImage(720, 1280, QImage.Format.Format_RGB888)
                source.fill(QColor(1, 2, 3))
                color = QColor(*row["background_rgb"])
                painter = consumer.QPainter(source)
                painter.fillRect(0, 192, 720, 896, color)
                painter.end()
                resolved = consumer._resolve_native_palette_style(source, ROOT, family)
                self.assertEqual(resolved["palette_name"], row["name"])
                self.assertEqual(resolved["max_channel_delta"], 0)
                self.assertGreaterEqual(resolved["confidence_margin"], 1)

    def test_31_role_style_contract_is_bound_to_c11c_frozen_sources(self):
        contract = consumer.EDITORIAL_ROLE_STYLE_CONTRACT
        self.assertEqual(contract["style_authority"]["editorial_layer"]["sha256"], consumer.C11C_EDITORIAL_LAYER_SHA)
        self.assertEqual(contract["style_authority"]["typography_service"]["sha256"], consumer.C11C_TYPOGRAPHY_SHA)
        self.assertEqual(contract["style_authority"]["drill_palette_bank"]["sha256"], consumer.DRILL_PALETTE_BANK_SHA)
        self.assertFalse(contract["scope"]["c11c_source_mutation"])
        self.assertEqual(contract["scope"]["release_authority"], "NONE")

    def test_32_role_style_metadata_is_stable_for_repeated_game_frames(self):
        a = consumer.compose_frame(self.source, self.plan, "GAME", 10, 630, 30, 1, ROOT)
        b = consumer.compose_frame(self.source, self.plan, "GAME", 400, 630, 30, 1, ROOT)
        self.assertEqual(a["editorial_role_style_resolution"], b["editorial_role_style_resolution"])
        self.assertEqual(a["editorial_role_render"], b["editorial_role_render"])
        self.assertTrue(a["native_body_pixel_identity"] and b["native_body_pixel_identity"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
