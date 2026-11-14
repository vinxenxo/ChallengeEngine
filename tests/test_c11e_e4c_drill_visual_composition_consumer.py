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
TOOLS = ROOT / "tools" / "c11d" / "d9"
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
                "status": "USER_DIRECTED_V2_D_OWNED_CONTRACT_ONLY",
            },
            "geometry": geometry,
            "text": {
                "raw_editorial_preserved": True,
                "visible_fields": {
                    "title": "SEGUIMIENTO VISUAL · NIVEL 1",
                    "subtitle": "Sigue el objetivo con precisión",
                    "call_to_action": "Mantén la mirada en el objetivo",
                },
                "language_metadata_only": "es",
                "layout_static_for_sequence": True,
                "phase_visibility": {"PRE_ROLL": False, "GAME": True, "END_CTA": False, "DONE": False},
            },
            "source_pins": {
                "presentation_profile": {
                    "path": consumer.PRESENTATION_PROFILE_REL,
                    "bytes": 8837,
                    "sha256": consumer.PRESENTATION_PROFILE_SHA,
                }
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
        painter.fillRect(0, 192, 720, 896, QColor(10, 170, 20))
        painter.fillRect(0, 1088, 720, 192, QColor(10, 20, 170))
        painter.end()
        cls.source_hash = consumer._image_rgb_sha256(cls.source)

    def test_01_exact_v2_proposal_schema_decision_and_timebase_pins(self):
        self.assertEqual(consumer._sha_file(ROOT / consumer.COMPOSITION_PROPOSAL_REL), consumer.COMPOSITION_SHA)
        self.assertEqual(consumer._sha_file(ROOT / consumer.COMPOSITION_SCHEMA_REL), consumer.COMPOSITION_SCHEMA_SHA)
        self.assertEqual(consumer._sha_file(ROOT / consumer.DECISION_REL), consumer.DECISION_SHA)
        self.assertEqual(consumer._sha_file(ROOT / consumer.TIMEBASE_PROPOSAL_REL), consumer.TIMEBASE_SHA)
        self.assertEqual(consumer._sha_file(ROOT / consumer.TIMEBASE_SCHEMA_REL), consumer.TIMEBASE_SCHEMA_SHA)

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

    def test_05_preroll_is_complete_native_frame_passthrough(self):
        result = consumer.compose_frame(self.source, self.plan, "PRE_ROLL", 0, 630, 30, 1, ROOT)
        self.assertEqual(result["mode"], "NATIVE_PHASE_FULL_FRAME_PASSTHROUGH")
        self.assertEqual(consumer._image_rgb_bytes(result["image"]), consumer._image_rgb_bytes(self.source))
        self.assertTrue(result["native_full_frame_identity"])
        self.assertFalse(result["mapping"]["d_editorial_visible"])

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
        self.assertEqual(result["mode"], "D_GAME_BODY_PIXEL_EXACT_COMPOSITION")

    def test_08_native_header_and_footer_are_not_embedded_in_game_body(self):
        result = consumer.compose_frame(self.source, self.plan, "GAME", 200, 630, 30, 1, ROOT)
        output = result["image"]
        self.assertEqual(consumer._pixel_rgb(output, 350, 500), (10, 170, 20))
        self.assertEqual(consumer._pixel_rgb(output, 700, 190), (5, 7, 11))
        self.assertEqual(consumer._pixel_rgb(output, 700, 1279), (5, 7, 11))

    def test_09_d_editorial_is_drawn_only_during_game(self):
        game = consumer.compose_frame(self.source, self.plan, "GAME", 0, 630, 30, 1, ROOT)
        self.assertTrue(game["mapping"]["d_editorial_visible"])
        for phase, index in (("PRE_ROLL", 0), ("END_CTA", 720)):
            result = consumer.compose_frame(self.source, self.plan, phase, index, 630, 30, 1, ROOT)
            self.assertFalse(result["mapping"]["d_editorial_visible"])
            self.assertEqual(result["mode"], "NATIVE_PHASE_FULL_FRAME_PASSTHROUGH")

    def test_10_d_editorial_renders_in_top_and_bottom_bands_on_game(self):
        result = consumer.compose_frame(self.source, self.plan, "GAME", 1, 630, 30, 1, ROOT)
        for rect in ((36, 0, 648, 92), (36, 1151, 648, 66)):
            patch = result["image"].copy(*rect).convertToFormat(QImage.Format.Format_RGB888)
            raw = consumer._image_rgb_bytes(patch)
            bright = sum(1 for i in range(0, len(raw), 3) if min(raw[i:i+3]) > 180)
            self.assertGreater(bright, 8)

    def test_11_empty_editorial_uses_full_frame_passthrough(self):
        altered = copy.deepcopy(self.plan)
        altered["text"]["visible_fields"] = {}
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

    def _historical_fixture(self):
        import json
        import tempfile
        from pathlib import Path
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name).resolve()
        relative = "artifacts/production/c11e/accepted-smoke"
        evidence = root.joinpath(*relative.split("/"))
        evidence.mkdir(parents=True)
        pins = [
            {"path": f"source/pin_{index:02d}.py", "bytes": index + 1, "sha256": hashlib.sha256(f"pin-{index}".encode()).hexdigest()}
            for index in range(91)
        ]
        preparation = {
            "schema": "C11E-DRILL-FAMILY-STAGE-PREPARATION-V1",
            "status": "DRILL_FAMILY_STAGE_PREPARED_NOT_DISPATCHABLE",
            "renderer_input_emitted": False, "renderer_dispatch_invoked": False,
            "renderer_activation": False, "media_created": False, "audio_generation_invoked": False,
            "ffmpeg_invoked": False, "godot_invoked": False, "launcher_invoked": False,
            "release_authority": "NONE",
        }
        preparation["preparation_sha256"] = consumer._json_sha(preparation)
        intent = {
            "schema": "C11-E-PRODUCTION-INTENT-V1", "schema_version": "1.3",
            "status": "PREPARED_E1_NOT_DISPATCHED", "request_origin": "CLI",
            "request": {"content_type": "visual_drills", "request_id": "accepted-smoke", "selection": {"family_id": "tracking", "variant_id": "tier-1"}},
            "output": {"created": False, "overwrite_policy": "DENY_EXISTING", "planned_root": relative, "planned_root_exists": False},
            "d9_boundary_preparation": preparation,
            "execution_boundary": {"d4_8": "BLOCKED", "dispatch_authorized": False, "media_created": False, "production_execution": False, "release_authority": "NONE", "renderer_activation": False, "renderer_dispatch_invoked": False, "renderer_input_emitted": False},
            "family_adapter": {"status": "NOT_CONNECTED_E1", "renderer_input_emitted": False},
            "source_identity": {"source_pins": pins, "c11c_manifest": {"bytes": 796318, "disposition": "IMMUTABLE_REFERENCE_ONLY", "path": "release/C11C_FREEZE_PACKAGE_MANIFEST.json", "sha256": "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"}},
        }
        intent["intent_sha256"] = consumer._json_sha(intent)
        receipt = {
            "schema": "C11E-E4C-DRILL-SHARED-EXECUTION-RECEIPT-V1",
            "status": "PASS_E4C_DRILL_SINGLE_SELECTOR_A_V_QUALIFICATION",
            "request_origin": "CLI", "request_id": "accepted-smoke", "evidence_root": str(evidence),
            "e1_validation": {"status": "PASS_E1_PREPARATION_ONLY", "valid": True, "intent_sha256": intent["intent_sha256"], "source_pin_count": 91, "media_created": False, "renderer": False},
            "e1_gui_cli_parity": {"status": "PASS_E1_SHARED_GUI_CLI_INTENT_PARITY", "semantic_identity_equal": True, "cli_intent_sha256": intent["intent_sha256"], "origin_used_for_execution": "CLI"},
            "family_adapter_preparation_status": "NOT_CONNECTED_E1", "production_dispatch": False, "release_authority": "NONE", "c11c_source_mutation": False, "source_pin_count": 91,
            "c11c_manifest_sha256": "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953", "c11c_frozen_manifest_unchanged": True,
            "source_pins_pre_execution": pins, "source_pins_immediately_pre_renderer": copy.deepcopy(pins), "source_pins_post_execution": copy.deepcopy(pins),
        }
        (evidence / "E4C_DRILL_AV_QUALIFICATION_RECEIPT.json").write_text(json.dumps(receipt), encoding="utf-8")
        (evidence / "e1_intent.json").write_text(json.dumps(intent), encoding="utf-8")
        return temp, root, evidence, intent, receipt

    def test_21_historical_existing_media_accepts_exact_prepared_intent_and_receipt(self):
        temp, root, evidence, intent, receipt = self._historical_fixture()
        try:
            from unittest.mock import patch
            preparation = consumer._validate_historical_intent(root, intent, receipt, evidence)
            self.assertEqual(preparation["status"], "DRILL_FAMILY_STAGE_PREPARED_NOT_DISPATCHABLE")
            with patch.object(consumer, "_build_composition_plan_from_preparation", return_value={"test_plan": True}) as build:
                result = consumer.build_composition_plan_for_existing_media(intent, root, receipt, evidence)
            self.assertEqual(result, {"test_plan": True})
            build.assert_called_once_with(intent, root, preparation)
        finally:
            temp.cleanup()

    def test_22_historical_receipt_intent_hash_mismatch_is_rejected(self):
        temp, root, evidence, intent, receipt = self._historical_fixture()
        try:
            receipt["e1_validation"]["intent_sha256"] = "0" * 64
            (evidence / "E4C_DRILL_AV_QUALIFICATION_RECEIPT.json").write_text(__import__("json").dumps(receipt), encoding="utf-8")
            with self.assertRaises(consumer.DrillVisualConsumerError):
                consumer._validate_historical_intent(root, intent, receipt, evidence)
        finally:
            temp.cleanup()

    def test_23_non_pass_e1_preparation_receipt_is_rejected(self):
        temp, root, evidence, intent, receipt = self._historical_fixture()
        try:
            receipt["e1_validation"]["status"] = "FAIL"
            (evidence / "E4C_DRILL_AV_QUALIFICATION_RECEIPT.json").write_text(__import__("json").dumps(receipt), encoding="utf-8")
            with self.assertRaises(consumer.DrillVisualConsumerError):
                consumer._validate_historical_intent(root, intent, receipt, evidence)
        finally:
            temp.cleanup()

    def test_24_historical_source_pin_mismatch_is_rejected(self):
        temp, root, evidence, intent, receipt = self._historical_fixture()
        try:
            receipt["source_pins_post_execution"][0]["sha256"] = "0" * 64
            (evidence / "E4C_DRILL_AV_QUALIFICATION_RECEIPT.json").write_text(__import__("json").dumps(receipt), encoding="utf-8")
            with self.assertRaises(consumer.DrillVisualConsumerError):
                consumer._validate_historical_intent(root, intent, receipt, evidence)
        finally:
            temp.cleanup()

    def test_25_historical_output_root_mismatch_and_traversal_are_rejected(self):
        temp, root, evidence, intent, receipt = self._historical_fixture()
        try:
            with self.assertRaises(consumer.DrillVisualConsumerError):
                consumer._validate_historical_intent(root, intent, receipt, root / "other")
            altered = copy.deepcopy(intent)
            altered["output"]["planned_root"] = "../../outside"
            altered["intent_sha256"] = consumer._json_sha({k: v for k, v in altered.items() if k != "intent_sha256"})
            receipt["e1_validation"]["intent_sha256"] = altered["intent_sha256"]
            receipt["e1_gui_cli_parity"]["cli_intent_sha256"] = altered["intent_sha256"]
            (evidence / "e1_intent.json").write_text(__import__("json").dumps(altered), encoding="utf-8")
            (evidence / "E4C_DRILL_AV_QUALIFICATION_RECEIPT.json").write_text(__import__("json").dumps(receipt), encoding="utf-8")
            with self.assertRaises(consumer.DrillVisualConsumerError):
                consumer._validate_historical_intent(root, altered, receipt, evidence)
        finally:
            temp.cleanup()

    def test_26_historical_output_creation_snapshot_must_remain_deny_existing_false(self):
        temp, root, evidence, intent, receipt = self._historical_fixture()
        try:
            altered = copy.deepcopy(intent)
            altered["output"]["planned_root_exists"] = True
            altered["intent_sha256"] = consumer._json_sha({k: v for k, v in altered.items() if k != "intent_sha256"})
            (evidence / "e1_intent.json").write_text(__import__("json").dumps(altered), encoding="utf-8")
            receipt["e1_validation"]["intent_sha256"] = altered["intent_sha256"]
            receipt["e1_gui_cli_parity"]["cli_intent_sha256"] = altered["intent_sha256"]
            (evidence / "E4C_DRILL_AV_QUALIFICATION_RECEIPT.json").write_text(__import__("json").dumps(receipt), encoding="utf-8")
            with self.assertRaises(consumer.DrillVisualConsumerError):
                consumer._validate_historical_intent(root, altered, receipt, evidence)
        finally:
            temp.cleanup()

    def test_27_ordinary_plan_builder_still_uses_strict_e1_validation(self):
        import tempfile
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as td:
            root = Path(td).resolve()
            intent = {"request": {"request_id": "live-path"}}
            preparation = {"status": "LIVE_E1_VALIDATED"}
            with patch.object(consumer, "_validate_intent", return_value=preparation) as validate, patch.object(consumer, "_build_composition_plan_from_preparation", return_value={"live_path": True}) as build:
                result = consumer.build_composition_plan(intent, root)
            self.assertEqual(result, {"live_path": True})
            validate.assert_called_once_with(root, intent)
            build.assert_called_once_with(intent, root, preparation)


if __name__ == "__main__":
    unittest.main(verbosity=2)
