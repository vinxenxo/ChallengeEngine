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
PRODUCER = Path(os.environ.get("C11E_TEST_SERVICE_DIR", ROOT / "c11c-suite" / "c11c-producer")).resolve()
if str(PRODUCER) not in sys.path:
    sys.path.insert(0, str(PRODUCER))

import c11e_production_service as service
import c11e_e4c_drill_visual_composition_consumer as consumer


def drill_request(*, title="E4C Drill Pixel Qualification", subtitle="Approved outer-band composition", cta="Continue", family_id="tracking", variant_id="tier-1", request_id="C11E-E4C-PIXEL-QUALIFICATION-001"):
    return {
        "schema": "C11-D-D9.9-UNIVERSAL-PRODUCER-REQUEST-V1",
        "schema_version": "1.0",
        "request_id": request_id,
        "mode": "PRODUCTION",
        "selection": {"content_type": "visual_drills", "family_id": family_id, "variant_id": variant_id},
        "seed": 12345,
        "music_seed": 840001,
        "delivery_profile_id": "REVIEW_720",
        "presentation_profile_id": "social_default_v1",
        "variation_index": 0,
        "audio_enabled": True,
        "personalization_enabled": True,
        "editorial_profile": {},
        "production_override": {
            "title": title,
            "subtitle": subtitle,
            "call_to_action": cta,
            "language": "en",
        },
        "provenance": {"source_revision": "E4C_DRILL_PIXEL_QUALIFICATION", "request_origin": "TEST"},
    }


class DrillVisualCompositionConsumerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.intent = service.prepare_c11e_production_intent(drill_request(), ROOT, request_origin="TEST")["intent"]
        cls.e1_validation = service.validate_c11e_production_intent(cls.intent, ROOT)
        cls.plan = consumer.build_composition_plan(cls.intent, ROOT)
        cls.qt_app = consumer._ensure_qt_app()
        cls.source = QImage(720, 1280, QImage.Format.Format_RGB888)
        cls.source.fill(QColor(20, 30, 40))
        cls.source_hash = hashlib.sha256(consumer._image_rgb_bytes(cls.source)).hexdigest()

    def test_01_valid_e1_drill_intent_is_accepted_by_existing_shared_service(self):
        self.assertEqual(self.e1_validation["status"], "PASS_E1_PREPARATION_ONLY")
        self.assertEqual(self.intent["schema_version"], "1.3")
        self.assertEqual(self.intent["request"]["content_type"], "visual_drills")

    def test_02_a3_historical_lineage_is_resolved_through_exact_v2_bridge(self):
        phase = self.intent["d9_boundary_preparation"]["native_phase_and_end_cta_contract"]
        window = phase["d_editorial_window_policy"]
        self.assertTrue(window["transitive_review_manifest_lineage_current"])
        self.assertEqual(window["lineage_resolution"]["status"], "PASS_A3_ATTESTED_SINGLE_POINTER_LINEAGE_BRIDGE")
        self.assertEqual(window["lineage_resolution"]["bridge_sha256"], "aec0e387f167f4b821b7d94f06a67f78f498be939fe3cda857d20ce550819cac")
        self.assertEqual(window["visual_consumer_status"], "READY_FOR_D_OWNED_ISOLATED_VISUAL_CONSUMER_TESTS")

    def test_03_plan_is_bound_to_exact_approved_composition_and_timebase_hashes(self):
        self.assertEqual(self.plan["approval"]["status"], "APPROVED_AS_PROPOSED_D_OWNED_DESIGN_CONTRACT_ONLY")
        self.assertEqual(self.plan["approval"]["composition_proposal_sha256"], consumer.COMPOSITION_SHA)
        self.assertEqual(self.plan["approval"]["timebase_proposal_sha256"], consumer.TIMEBASE_SHA)

    def test_04_plan_geometry_matches_720_review_canvas_and_contained_source(self):
        geometry = self.plan["geometry"]
        self.assertEqual((geometry["canvas"]["width"], geometry["canvas"]["height"]), (720, 1280))
        self.assertEqual((geometry["source_frame_viewport"]["x"], geometry["source_frame_viewport"]["y"], geometry["source_frame_viewport"]["width"], geometry["source_frame_viewport"]["height"]), (108, 192, 504, 896))
        self.assertEqual((geometry["top_editorial_band"]["height"], geometry["bottom_editorial_band"]["height"]), (192, 192))
        self.assertEqual(geometry["source_frame_transform"]["mode"], "UNIFORM_CONTAIN")
        self.assertEqual(geometry["source_frame_transform"]["scale_x"], geometry["source_frame_transform"]["scale_y"])
        self.assertFalse(geometry["source_frame_transform"]["temporal_resampling"])

    def test_05_exact_twenty_selector_domain_is_preserved_and_composes(self):
        selectors = [(family, tier) for family in consumer.DRILL_FAMILIES for tier in consumer.DRILL_TIERS]
        self.assertEqual(len(selectors), 20)
        self.assertEqual(len(set(selectors)), 20)
        self.assertEqual(consumer.EXPECTED_MUSIC_PROFILES, {
            "tracking": "FLOWING_VECTOR",
            "pursuit": "ORGANIC_BLOOM",
            "saccade": "CIRCUIT_PULSE",
            "peripheral_scan": "ORBITAL_RITUAL",
        })
        # One E1-prepared GAME frame is built and pixel-composed for every family/tier.
        # This does not rerun the accepted binder repeat/lineage qualification.
        for index, (family, tier) in enumerate(selectors):
            with self.subTest(family=family, tier=tier):
                request = drill_request(
                    family_id=family,
                    variant_id=tier,
                    request_id=f"C11E-E4C-PIXEL-QUALIFICATION-{index + 1:02d}",
                )
                intent = service.prepare_c11e_production_intent(request, ROOT, request_origin="TEST")["intent"]
                e1 = service.validate_c11e_production_intent(intent, ROOT)
                self.assertEqual(e1["status"], "PASS_E1_PREPARATION_ONLY")
                plan = consumer.build_composition_plan(intent, ROOT)
                self.assertEqual(plan["selection"], {"content_type": "visual_drills", "family_id": family, "variant_id": tier})
                frame = consumer.compose_frame(self.source, plan, "GAME", 0, 630, project_root=ROOT)
                self.assertEqual(frame["mode"], "D_OUTER_BAND_COMPOSITION")
                self.assertEqual((frame["image"].width(), frame["image"].height()), (720, 1280))
                self.assertEqual(frame["mapping"]["final_presentation_frame_index"], 90)
                self.assertTrue(frame["source_unchanged"])

    def test_06_plan_self_hash_is_valid(self):
        consumer.validate_plan(self.plan)

    def test_07_plan_tampering_is_rejected(self):
        altered = copy.deepcopy(self.plan)
        altered["geometry"]["source_frame_viewport"]["x"] = 107
        with self.assertRaises(consumer.DrillVisualConsumerError):
            consumer.validate_plan(altered)

    def test_08_prepayload_timebase_maps_first_and_last_preroll_frames(self):
        first = consumer.map_phase_frame("PRE_ROLL", 0, 630, 30, 1)
        last = consumer.map_phase_frame("PRE_ROLL", 89, 630, 30, 1)
        self.assertEqual(first["final_presentation_frame_index"], 0)
        self.assertEqual(last["final_presentation_frame_index"], 89)
        self.assertFalse(first["d_editorial_visible"])

    def test_09_game_timebase_maps_payload_zero_to_final_frame_90(self):
        mapped = consumer.map_phase_frame("GAME", 0, 630, 30, 1)
        self.assertEqual(mapped["final_presentation_frame_index"], 90)
        self.assertEqual(mapped["source_frame_index"], 0)
        self.assertTrue(mapped["d_editorial_visible"])

    def test_10_game_timebase_maps_last_payload_frame_to_719(self):
        mapped = consumer.map_phase_frame("GAME", 629, 630, 30, 1)
        self.assertEqual(mapped["final_presentation_frame_index"], 719)
        self.assertEqual(mapped["source_frame_index"], 629)

    def test_11_game_rejects_payload_index_outside_half_open_window(self):
        with self.assertRaises(consumer.DrillVisualConsumerError):
            consumer.map_phase_frame("GAME", 630, 630, 30, 1)

    def test_12_end_cta_keeps_native_final_stream_indices_and_last_source_frame(self):
        first = consumer.map_phase_frame("END_CTA", 720, 630, 30, 1)
        last = consumer.map_phase_frame("END_CTA", 809, 630, 30, 1)
        self.assertEqual(first["final_presentation_frame_index"], 720)
        self.assertEqual(last["final_presentation_frame_index"], 809)
        self.assertEqual(first["source_frame_index"], 629)
        self.assertFalse(first["d_editorial_visible"])

    def test_13_done_has_no_frame(self):
        result = consumer.map_phase_frame("DONE", 810, 630, 30, 1)
        self.assertIsNone(result["final_presentation_frame_index"])
        with self.assertRaises(consumer.DrillVisualConsumerError):
            consumer.compose_frame(self.source, self.plan, "DONE", 810, 630, project_root=ROOT)

    def test_14_pre_roll_composition_contains_source_but_no_d_text(self):
        result = consumer.compose_frame(self.source, self.plan, "PRE_ROLL", 0, 630, 30, 1, ROOT)
        self.assertEqual(result["mode"], "D_OUTER_BAND_COMPOSITION")
        self.assertEqual((result["image"].width(), result["image"].height()), (720, 1280))
        self.assertEqual(consumer._pixel_rgb(result["image"], 0, 0), (5, 7, 11))
        self.assertEqual(consumer._pixel_rgb(result["image"], 60, 50), (5, 7, 11))
        self.assertEqual(consumer._pixel_rgb(result["image"], 360, 640), (20, 30, 40))
        self.assertFalse(result["mapping"]["d_editorial_visible"])

    def test_15_game_composition_draws_d_editorial_in_top_and_bottom_bands(self):
        result = consumer.compose_frame(self.source, self.plan, "GAME", 0, 630, 30, 1, ROOT)
        image = result["image"]
        self.assertTrue(result["mapping"]["d_editorial_visible"])
        top = image.copy(36, 0, 648, 92).convertToFormat(QImage.Format.Format_RGB888)
        raw = consumer._image_rgb_bytes(top)
        triples = [raw[index:index + 3] for index in range(0, len(raw), 3)]
        self.assertGreater(len(set(triples)), 1)
        bright_pixels = sum(1 for pixel in triples if len(pixel) == 3 and min(pixel) > 180)
        self.assertGreater(bright_pixels, 10)

    def test_16_end_cta_composition_suppresses_d_text_and_preserves_source(self):
        result = consumer.compose_frame(self.source, self.plan, "END_CTA", 720, 630, 30, 1, ROOT)
        self.assertFalse(result["mapping"]["d_editorial_visible"])
        self.assertEqual(consumer._pixel_rgb(result["image"], 60, 50), (5, 7, 11))
        self.assertEqual(consumer._pixel_rgb(result["image"], 360, 640), (20, 30, 40))

    def test_17_contained_source_pixels_match_the_exact_qt_smooth_transform(self):
        expected = self.source.scaled(
            504, 896, consumer.Qt.AspectRatioMode.IgnoreAspectRatio,
            consumer.Qt.TransformationMode.SmoothTransformation,
        )
        result = consumer.compose_frame(self.source, self.plan, "GAME", 1, 630, 30, 1, ROOT)
        actual = result["image"].copy(108, 192, 504, 896)
        self.assertEqual(consumer._image_rgb_bytes(actual), consumer._image_rgb_bytes(expected))

    def test_18_input_source_frame_is_not_mutated(self):
        before = hashlib.sha256(consumer._image_rgb_bytes(self.source)).hexdigest()
        result = consumer.compose_frame(self.source, self.plan, "GAME", 2, 630, 30, 1, ROOT)
        after = hashlib.sha256(consumer._image_rgb_bytes(self.source)).hexdigest()
        self.assertEqual(before, after)
        self.assertEqual(result["source_rgb_sha256"], before)
        self.assertTrue(result["source_unchanged"])

    def test_19_all_empty_or_unknown_fields_use_full_frame_passthrough(self):
        altered = copy.deepcopy(self.plan)
        altered["text"]["visible_fields"] = {}
        altered["plan_sha256"] = consumer._json_sha({k: v for k, v in altered.items() if k != "plan_sha256"})
        result = consumer.compose_frame(self.source, altered, "GAME", 0, 630, 30, 1)
        self.assertEqual(result["mode"], "UNCHANGED_FULL_FRAME_PASSTHROUGH")
        self.assertEqual((result["image"].width(), result["image"].height()), (720, 1280))
        self.assertEqual(consumer._image_rgb_bytes(result["image"]), consumer._image_rgb_bytes(self.source))

    def test_20_empty_and_unknown_sentinels_are_suppressed_case_insensitively(self):
        fields = consumer._filtered_fields({"title": "", "subtitle": " UNKNOWN ", "call_to_action": "unknown", "language": "en"})
        self.assertEqual(fields, {})

    def test_21_language_remains_metadata_only(self):
        self.assertEqual(self.plan["text"]["language_metadata_only"], "en")
        self.assertNotIn("language", self.plan["text"]["visible_fields"])

    def test_22_editorial_160_codepoint_ceiling_is_enforced_without_truncation(self):
        value = "A" * 160
        self.assertEqual(len(consumer._filtered_fields({"title": value})["title"]), 160)
        with self.assertRaises(consumer.DrillVisualConsumerError):
            consumer._filtered_fields({"title": value + "A"})
        lines = consumer._wrap_text(value, consumer._font(ROOT, consumer.INTER_FONT_REL, 15), 648, 4, "title")
        self.assertEqual("".join(lines), value)
        self.assertLessEqual(len(lines), 4)

    def test_23_layout_breaks_long_tokens_without_changing_source_text(self):
        value = "A" * 160
        font = consumer._font(ROOT, consumer.INTER_FONT_REL, 15)
        lines = consumer._wrap_text(value, font, 648, 4, "title")
        self.assertEqual("".join(lines), value)
        self.assertTrue(all(consumer._text_advance(font, line) <= 648 for line in lines))

    def test_24_layout_capacity_failure_is_fail_closed_and_never_ellipsizes(self):
        value = "A" * 160
        font = consumer._font(ROOT, consumer.INTER_FONT_REL, 15)
        with self.assertRaises(consumer.DrillVisualConsumerError):
            consumer._wrap_text(value, font, 100, 1, "title")

    def test_25_font_cmap_covers_supported_spanish_copy(self):
        sample = "¡Árbol, acción, niño! ¿Qué tal?"
        for rel in (consumer.INTER_FONT_REL, consumer.MONO_FONT_REL):
            cmap = consumer._font_codepoints(ROOT / rel)
            missing = {ord(ch) for ch in sample if not ch.isspace()} - cmap
            self.assertEqual(missing, set(), f"font cmap coverage gap in {rel}: {missing}")
            font = consumer._font(ROOT, rel, 18)
            raw = consumer.QRawFont.fromFont(font)
            self.assertTrue(raw.isValid(), f"Qt did not load exact font {rel}")
            qt_missing = {ord(ch) for ch in sample if not ch.isspace() and not raw.supportsCharacter(ord(ch))}
            self.assertEqual(qt_missing, set(), f"Qt shaping font coverage gap in {rel}: {qt_missing}")

    def test_26_unsupported_glyph_fails_closed(self):
        plan = copy.deepcopy(self.plan)
        plan["text"]["visible_fields"]["title"] = "Smile 😀"
        plan["plan_sha256"] = consumer._json_sha({k: v for k, v in plan.items() if k != "plan_sha256"})
        with self.assertRaises(consumer.DrillVisualConsumerError):
            consumer.compose_frame(self.source, plan, "GAME", 0, 630, 30, 1, ROOT)

    def test_27_wrong_source_resolution_fails_closed(self):
        with self.assertRaises(consumer.DrillVisualConsumerError):
            wrong_size = QImage(540, 960, QImage.Format.Format_RGB888)
            consumer.compose_frame(wrong_size, self.plan, "GAME", 0, 630, project_root=ROOT)

    def test_28_phase_frame_indices_reject_boolean_and_unknown_phase(self):
        with self.assertRaises(consumer.DrillVisualConsumerError):
            consumer.map_phase_frame("GAME", True, 630)
        with self.assertRaises(consumer.DrillVisualConsumerError):
            consumer.map_phase_frame("INTRO", 0, 630)

    def test_29_fractional_fps_is_handled_by_exact_timebase_rounding(self):
        mapped = consumer.map_phase_frame("GAME", 0, 630, 30000, 1001)
        self.assertEqual(mapped["pre_roll_frames"], 90)
        self.assertEqual(mapped["final_presentation_frame_index"], 90)

    def test_30_governance_never_emits_native_input_or_media(self):
        consumer.validate_plan(self.plan)
        governance = self.plan["governance"]
        self.assertFalse(governance["renderer_native_input_emitted"])
        self.assertFalse(governance["renderer_dispatch_invoked"])
        self.assertFalse(governance["media_created"])
        self.assertFalse(governance["audio_generated"])
        self.assertEqual(governance["release_authority"], "NONE")


    def test_31_lineage_bridge_rejects_wrong_bridge_hash(self):
        from unittest.mock import patch
        proposal = consumer._read_json(ROOT, "definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json")
        manifest_rel = "definitions/c11d/production/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1.json"
        manifest_pin = service._file_identity(ROOT, manifest_rel)
        original = service._file_identity
        def altered(root, relative):
            result = original(root, relative)
            if relative == service.A3_LINEAGE_BRIDGE_REL:
                result = dict(result, sha256="0" * 64)
            return result
        with patch.object(service, "_file_identity", side_effect=altered):
            with self.assertRaises(service.C11EProductionServiceError):
                service._resolve_a3_review_manifest_lineage(ROOT, proposal, manifest_pin)

    def test_32_lineage_bridge_rejects_wrong_historical_archive_hash(self):
        from unittest.mock import patch
        proposal = consumer._read_json(ROOT, "definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json")
        manifest_rel = "definitions/c11d/production/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1.json"
        manifest_pin = service._file_identity(ROOT, manifest_rel)
        original = service._file_identity
        archive_rel = "docs/history/c11e/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1_PRE_D98_LINEAGE_REFRESH_20261106.json"
        def altered(root, relative):
            result = original(root, relative)
            if relative == archive_rel:
                result = dict(result, sha256="0" * 64)
            return result
        with patch.object(service, "_file_identity", side_effect=altered):
            with self.assertRaises(service.C11EProductionServiceError):
                service._resolve_a3_review_manifest_lineage(ROOT, proposal, manifest_pin)

    def test_33_lineage_bridge_rejects_wrong_d98_model_postimage(self):
        from unittest.mock import patch
        proposal = consumer._read_json(ROOT, "definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json")
        manifest_rel = "definitions/c11d/production/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1.json"
        manifest_pin = service._file_identity(ROOT, manifest_rel)
        original = service._file_identity
        model_rel = "definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json"
        def altered(root, relative):
            result = original(root, relative)
            if relative == model_rel:
                result = dict(result, sha256="0" * 64)
            return result
        with patch.object(service, "_file_identity", side_effect=altered):
            with self.assertRaises(service.C11EProductionServiceError):
                service._resolve_a3_review_manifest_lineage(ROOT, proposal, manifest_pin)

    def test_34_e1_phase_contract_pins_all_eight_audited_c11c_sources(self):
        expected = {
            "core/presentation/CountdownPresentationLogic.gd": "b163ea114cc48af2dfd957ee92d00d524ea5b96b5966850f5ca8d6e5ec933379",
            "core/presentation/VisualDrillPresentationPhaseLogic.gd": "6555d08ac3c0098b20a57e924b0c4ff2df006a23fa00a81b254fa5ebd5bb2494",
            "core/presentation/VisualDrillPresentationBinder.gd": "cb6acc408252b8b794177d8f5923a3b151646eebdfd1efe9a30fdd6221de82c0",
            "core/presentation/rendering/VisualContentPlayer.gd": "58d86d56ebd7507c9e800c83010103b9be12f1b5dca9356da61ca623e4cf0145",
            "core/presentation/C11CVisualEditorialLayer.gd": "f8f718c067a4d7a088cc16f244cc40209e7183bec93e44d8cb66eb6dd404cf7d",
            "core/presentation/PresentationUI.gd": "a55fea5a4525ea247144a4da88242f4ac602c3a014f7d02b50d032ce99224730",
            "core/presentation/SocialUIBinder.gd": "b15a062bf327d0c2bbc4ead0e877914f912528cc56e388df20dd84eb89863a3c",
            "core/presentation/UnifiedSocialFrame.gd": "d80c07103f56a2abfe34be60547285e61b0d03b50a5ed93c3c72d4241f6585ba",
        }
        rows = self.intent["d9_boundary_preparation"]["native_phase_and_end_cta_contract"]["source_pins"]
        actual = {row["path"]: row["sha256"] for row in rows}
        for path, digest in expected.items():
            self.assertEqual(actual.get(path), digest, path)

    def test_35_a3_bridge_archive_and_current_manifest_are_in_e1_source_pin_set(self):
        paths = {row["path"] for row in self.intent["source_identity"]["source_pins"]}
        required = {
            service.A3_LINEAGE_BRIDGE_REL,
            "definitions/c11d/production/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1.json",
            "docs/history/c11e/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1_PRE_D98_LINEAGE_REFRESH_20261106.json",
            "definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json",
        }
        self.assertTrue(required.issubset(paths), sorted(required - paths))

if __name__ == "__main__":
    unittest.main(verbosity=2)
