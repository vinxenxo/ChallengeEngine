#!/usr/bin/env python3
"""Focused contract tests for the C11-E E4A Challenge pixel-review runner."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
import c11e_e4a_challenge_pixel_review as pixel_review  # noqa: E402


class E4AChallengePixelReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.approval = pixel_review.load_json(ROOT / pixel_review.APPROVAL_REL)
        cls.gd = (ROOT / pixel_review.MATERIALIZER_REL).read_text(encoding="utf-8-sig")
        cls.py = (ROOT / Path("tools/c11d/d9/c11e_e4a_challenge_pixel_review.py")).read_text(encoding="utf-8")

    def valid_intent(self) -> dict[str, Any]:
        editorial = {field: "UNKNOWN" for field in pixel_review.EXPECTED_FIELDS}
        return {
            "schema": "C11-E-PRODUCTION-INTENT-V1",
            "schema_version": "1.1",
            "service_version": "0.2.0-E3.2",
            "status": "PREPARED_E1_NOT_DISPATCHED",
            "request_origin": "TEST",
            "request": {
                "request_id": "E4A-PIXEL-TEST-A",
                "mode": "REVIEW",
                "content_type": "challenges",
                "selection": {"content_type": "challenges", "family_id": "parking_v2", "variant_id": "CHALLENGE_004"},
            },
            "identity": {k: "a" * 64 for k in ("request_hash", "editorial_hash", "plan_hash", "intent_hash")},
            "seed_domains": {
                "gameplay": {"field": "request.seed", "value": 314159},
                "music": {"field": "request.music_seed", "value": 840001},
                "independent_domains": True,
            },
            "delivery": {"resolved_profile_id": "REVIEW_720", "presentation_profile_id": "social_default_v1", "audio_enabled": False},
            "editorial": editorial,
            "editorial_field_consumption": {field: {"consumer_status": "NOT_CONSUMED_E1"} for field in pixel_review.EXPECTED_FIELDS},
            "output": {"created": False},
            "execution_boundary": {
                "dispatch_authorized": False,
                "renderer_input_emitted": False,
                "renderer_dispatch_invoked": False,
                "renderer_activation": False,
                "production_execution": False,
                "media_created": False,
                "d4_8": "BLOCKED",
                "release_authority": "NONE",
            },
        }

    def assert_intent_rejected(self, mutate) -> None:
        intent = self.valid_intent()
        mutate(intent)
        with self.assertRaises(pixel_review.E4APixelReviewError):
            pixel_review.validate_e1_intent(intent, "A")

    def test_01_authority_pins_match(self):
        self.assertEqual(pixel_review.MANIFEST_SHA256, "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953")
        self.assertEqual(pixel_review.CHALLENGE_SHA256, "6a674c02c2d8831a872691954f1cc40e2492193f9b136f60656730a7be686b71")
        self.assertEqual(pixel_review.APPROVAL_SHA256, "764629384896a255cf992da89fa427c19f60f9b2e623b81ad17d909674b466b5")
        if (ROOT / pixel_review.MANIFEST_REL).is_file():
            observed = pixel_review.validate_static_authorities(ROOT)
            self.assertEqual(observed["frozen_manifest"], pixel_review.MANIFEST_SHA256)

    def test_02_approved_policy_has_exact_six_fields(self):
        names = {row["field"] for row in self.approval["fields"]}
        self.assertEqual(names, pixel_review.EXPECTED_FIELDS)

    def test_03_title_and_subtitle_route_to_header_hook(self):
        rows = {row["field"]: row for row in self.approval["fields"]}
        for field in ("title", "subtitle"):
            self.assertEqual(rows[field]["region"], "HEADER")
            self.assertEqual(rows[field]["source_phase_windows"], ["HOOK"])

    def test_04_call_to_action_routes_to_footer_cta(self):
        row = next(row for row in self.approval["fields"] if row["field"] == "call_to_action")
        self.assertEqual(row["region"], "FOOTER")
        self.assertEqual(row["source_phase_windows"], ["CTA"])

    def test_05_challenge_overlay_remains_semantic_only(self):
        rows = {row["field"]: row for row in self.approval["fields"]}
        for field in ("player_name", "challenge_label"):
            self.assertEqual(rows[field]["region"], "CHALLENGE_OVERLAY")
            self.assertEqual(rows[field]["source_phase_windows"], ["HOOK", "GAME"])
        self.assertIn('BLOCKED_GEOMETRY_UNRESOLVED', self.gd)

    def test_06_language_is_metadata_only(self):
        row = next(row for row in self.approval["fields"] if row["field"] == "language")
        self.assertEqual(row["kind"], "metadata_only")
        self.assertIsNone(row["region"])
        self.assertEqual(row["source_phase_windows"], [])

    def test_07_d15_regions_are_exactly_pinned(self):
        text = (ROOT / pixel_review.LAYOUT_REL).read_text(encoding="utf-8-sig")
        for value in ("Rect2(0, 0, 540, 144)", "Rect2(0, 144, 540, 672)", "Rect2(0, 816, 540, 144)"):
            self.assertIn(value, text)

    def test_08_e1_valid_intent_accepted(self):
        pixel_review.validate_e1_intent(self.valid_intent(), "A")

    def test_09_wrong_service_version_rejected(self):
        self.assert_intent_rejected(lambda x: x.update(service_version="0.2.0-E3.1"))

    def test_10_wrong_selector_rejected(self):
        self.assert_intent_rejected(lambda x: x["request"]["selection"].update(variant_id="CHALLENGE_005"))

    def test_11_wrong_family_rejected(self):
        self.assert_intent_rejected(lambda x: x["request"]["selection"].update(family_id="hit_v1"))

    def test_12_wrong_seed_domain_rejected(self):
        self.assert_intent_rejected(lambda x: x["seed_domains"]["music"].update(value=314159))

    def test_13_dispatch_authorization_rejected(self):
        self.assert_intent_rejected(lambda x: x["execution_boundary"].update(dispatch_authorized=True))

    def test_14_editorial_extra_field_rejected(self):
        self.assert_intent_rejected(lambda x: x["editorial"].update(hook="do not alias"))

    def test_15_editorial_missing_field_rejected(self):
        self.assert_intent_rejected(lambda x: x["editorial"].pop("language"))

    def test_16_editorial_carrier_must_remain_unconsumed_in_e1(self):
        self.assert_intent_rejected(lambda x: x["editorial_field_consumption"]["title"].update(consumer_status="CONSUMED"))

    def test_17_materializer_keeps_default_preview_path_and_adds_opt_in_pixel_path(self):
        self.assertIn('var e4a_config_path: String = _cmdline_value("--e4a-config")', self.gd)
        self.assertIn('func _build_payload(source: Dictionary, context: Variant)', self.gd)
        self.assertIn('C11-D RENDERER CHALLENGE VISUAL PAYLOAD PREVIEW PASS', self.gd)
        self.assertIn('C11E E4A CHALLENGE EDITORIAL PIXEL RENDER PASS', self.gd)

    def test_18_pixel_probe_uses_actual_offscreen_subviewport(self):
        self.assertIn("SubViewport.new()", self.gd)
        self.assertIn("RenderingServer.frame_post_draw", self.gd)
        self.assertIn("save_png(output_path)", self.gd)

    def test_19_pixel_probe_does_not_call_production_dispatch(self):
        self.assertIn('"production_dispatch": false', self.gd)
        self.assertIn('"production_media_created": false', self.gd)
        self.assertIn('"d9_10": "PREPARE_ONLY"', self.gd)
        self.assertIn('"release_authority": "NONE"', self.gd)
        self.assertNotIn("ProductionDispatch.dispatch(", self.gd)

    def test_20_report_does_not_claim_gameplay_body_pixel_identity(self):
        self.assertIn('"gameplay_body_pixel_identity": "NOT_TESTED_GAMEPLAY_NOT_RASTERIZED_IN_THIS_EDITORIAL_LAYER_FIXTURE"', self.gd)
        self.assertIn('fixture_body_pixels_unchanged=true', self.gd)
        self.assertNotIn(' body_pixels_unchanged=true |', self.gd)

    def test_21_runner_calls_existing_shared_e1_service(self):
        self.assertIn("prepare_c11e_production_intent", self.py)
        self.assertIn("_load_d9_resolver", self.py)
        self.assertIn('"request_origin": "TEST"', self.py)

    def test_22_runner_never_invokes_ffmpeg_or_c_producer(self):
        self.assertNotIn("ffmpeg", self.py.lower())
        self.assertNotIn("c11c_challenge_bulk_qa", self.py.lower())
        self.assertNotIn("run_c11c_challenge_production", self.py.lower())

    def test_23_runner_records_pngs_and_real_godot_exit_code(self):
        self.assertIn("godot_exit_code", self.py)
        self.assertIn("pixel_png_count", self.py)
        self.assertIn("_png_dimensions", self.py)
        self.assertIn("C11E_E4A_CHALLENGE_PIXEL_REVIEW=PASS_ISOLATED_TEST_ONLY", self.py)


if __name__ == "__main__":
    unittest.main(verbosity=2)
