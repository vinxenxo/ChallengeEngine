#!/usr/bin/env python3
"""Unit/source contracts for E4A.6 live Challenge editorial envelope + consumer."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = Path(__file__).with_name("c11e_e4a6_challenge_live_editorial_envelope.py")
spec = importlib.util.spec_from_file_location("e4a6_envelope", MODULE_PATH)
assert spec and spec.loader
E = importlib.util.module_from_spec(spec)
spec.loader.exec_module(E)

CONSUMER_PATH = Path(__file__).with_name("C11EChallengeLiveEditorialConsumer.gd")
GENERATOR_PATH = ROOT / "GeneradorMaestro.gd"


def fake_intent() -> dict:
    return {
        "schema": "C11-E-PRODUCTION-INTENT-V1",
        "schema_version": "1.1",
        "service_version": "0.2.0-E3.2",
        "status": "PREPARED_E1_NOT_DISPATCHED",
        "request_origin": "TEST",
        "request": {
            "request_id": "E4A6-TEST-CH004",
            "mode": "REVIEW",
            "content_type": "challenges",
            "selection": {"content_type": "challenges", "family_id": "parking_v2", "variant_id": "CHALLENGE_004"},
            "presentation_options": {"show_hook_countdown": True},
        },
        "identity": {key: hashlib.sha256(key.encode()).hexdigest() for key in ("request_hash", "editorial_hash", "plan_hash", "intent_hash")},
        "editorial": {
            "title": "TITLE LIVE",
            "subtitle": "SUBTITLE LIVE",
            "player_name": "BLOCKED PLAYER",
            "challenge_label": "BLOCKED LABEL",
            "call_to_action": "FOLLOW NOW",
            "language": "es",
        },
        "execution_boundary": {
            "dispatch_authorized": False,
            "renderer_input_emitted": False,
            "renderer_dispatch_invoked": False,
            "renderer_activation": False,
            "production_execution": False,
            "media_created": False,
            "release_authority": "NONE",
            "d4_8": "BLOCKED",
        },
        "seed_domains": {"independent_domains": True},
        "output": {"created": False},
    }


class EnvelopeBuilderTests(unittest.TestCase):
    def test_builds_envelope_bound_to_challenge_source_timebase(self):
        result = E.build_envelope(ROOT, fake_intent())
        self.assertEqual(result["schema"], E.SCHEMA)
        self.assertEqual(result["status"], "PREPARED_E1_NOT_DISPATCHED")
        self.assertEqual(result["challenge_id"], "CHALLENGE_004")
        self.assertEqual(result["source_timebase"], {"fps": 60, "total_frames": 900, "kind": "SOURCE_FRAME_INDEX"})
        self.assertEqual(result["source_phase_ranges"], [
            {"phase": "HOOK", "start_frame": 0, "end_frame": 180, "timebase": "SOURCE_FPS_HALF_OPEN"},
            {"phase": "GAME", "start_frame": 180, "end_frame": 600, "timebase": "SOURCE_FPS_HALF_OPEN"},
            {"phase": "REVEAL", "start_frame": 600, "end_frame": 780, "timebase": "SOURCE_FPS_HALF_OPEN"},
            {"phase": "CTA", "start_frame": 780, "end_frame": 900, "timebase": "SOURCE_FPS_HALF_OPEN"},
        ])

    def test_exact_six_field_allowlist_and_blocked_geometry(self):
        result = E.build_envelope(ROOT, fake_intent())
        by_name = {row["field"]: row for row in result["fields"]}
        self.assertEqual(set(by_name), set(E.EXPECTED_FIELDS))
        self.assertEqual(by_name["player_name"]["disposition"], "BLOCKED_GEOMETRY_UNRESOLVED")
        self.assertEqual(by_name["challenge_label"]["disposition"], "BLOCKED_GEOMETRY_UNRESOLVED")
        self.assertEqual(by_name["language"]["disposition"], "METADATA_ONLY")
        self.assertEqual(by_name["title"]["disposition"], "READY_FOR_ISOLATED_TEST_PIXEL_DRAW")
        self.assertEqual(by_name["call_to_action"]["source_frame_ranges"][0]["start_frame"], 780)

    def test_empty_fields_are_omitted_without_inventing_ranges(self):
        intent = fake_intent()
        intent["editorial"]["title"] = "UNKNOWN"
        intent["editorial"]["subtitle"] = "   "
        result = E.build_envelope(ROOT, intent)
        by_name = {row["field"]: row for row in result["fields"]}
        self.assertEqual(by_name["title"]["disposition"], "OMITTED_EMPTY")
        self.assertEqual(by_name["title"]["effective_value"], "")
        self.assertEqual(by_name["subtitle"]["disposition"], "OMITTED_EMPTY")
        self.assertEqual(by_name["subtitle"]["effective_value"], "")
        self.assertEqual(by_name["title"]["source_frame_ranges"][0]["start_frame"], 0)

    def test_hook_countdown_option_off_is_preserved_from_e1(self):
        intent = fake_intent()
        intent["request"]["presentation_options"]["show_hook_countdown"] = False
        result = E.build_envelope(ROOT, intent)
        self.assertIs(result["presentation_options"]["show_hook_countdown"], False)

    def test_rejects_wrong_e1_challenge_identity(self):
        intent = fake_intent()
        intent["request"]["selection"]["variant_id"] = "CHALLENGE_999"
        with self.assertRaises(E.EnvelopeError):
            E.build_envelope(ROOT, intent)

    def test_rejects_dispatch_or_media_boundary_crossing(self):
        intent = fake_intent()
        intent["execution_boundary"]["renderer_input_emitted"] = True
        with self.assertRaises(E.EnvelopeError):
            E.build_envelope(ROOT, intent)

    def test_rejects_incomplete_or_mutated_e1_identity(self):
        intent = fake_intent()
        intent["identity"]["intent_hash"] = "not-a-hash"
        with self.assertRaises(E.EnvelopeError):
            E.build_envelope(ROOT, intent)

    def test_envelope_has_explicit_production_locks(self):
        result = E.build_envelope(ROOT, fake_intent())
        governance = result["governance"]
        self.assertIs(governance["renderer_input_emitted"], False)
        self.assertIs(governance["production_dispatch"], False)
        self.assertIs(governance["media_created"], False)
        self.assertEqual(governance["release_authority"], "NONE")
        self.assertEqual(governance["d4_8"], "BLOCKED")
        self.assertEqual(governance["d9_10"], "PREPARE_ONLY")


class LiveConsumerSourceContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.consumer = CONSUMER_PATH.read_text(encoding="utf-8")
        cls.generator = GENERATOR_PATH.read_text(encoding="utf-8")

    def test_consumer_is_optional_and_uses_separate_cli_envelope(self):
        self.assertIn('get_cli_arg_value("--c11e-editorial-envelope")', self.generator)
        self.assertIn('load("res://tools/c11d/d9/C11EChallengeLiveEditorialConsumer.gd")', self.generator)
        self.assertNotIn('preload("res://tools/c11d/d9/C11EChallengeLiveEditorialConsumer.gd")', self.generator)
        self.assertIn('if envelope_path.strip_edges().is_empty():', self.consumer)
        self.assertIn('envelope_path + ".sha256"', self.consumer)
        self.assertIn('"reason": "NO_D_ENVELOPE_ARGUMENT"', self.consumer)

    def test_all_four_native_binders_have_exactly_one_post_bind_consumer(self):
        self.assertEqual(self.generator.count("social_ui_binder.bind_render_model(rm)"), 4)
        self.assertEqual(self.generator.count("_apply_c11e_live_editorial_after_native_bind(rm)"), 4)
        for phase in ('HOOK', 'GAME', 'REVEAL', 'CTA'):
            block_start = self.generator.index(f'\t\t"{phase}":', self.generator.index('func _process('))
            next_match = self.generator.find('\n\t\t"', block_start + 1)
            block = self.generator[block_start: next_match if next_match >= 0 else None]
            self.assertIn("social_ui_binder.bind_render_model(rm)", block)
            self.assertIn("_apply_c11e_live_editorial_after_native_bind(rm)", block)

    def test_native_timeline_advances_once_after_match(self):
        process = self.generator[self.generator.index("func _process("):self.generator.index("func _configure_c11e_live_editorial_consumer")]
        self.assertEqual(process.count("timeline.advance()"), 1)
        self.assertGreater(process.index("timeline.advance()"), process.index('"CTA":'))

    def test_d_consumer_does_not_call_full_native_binder_or_full_presentation_ui(self):
        self.assertNotIn("bind_render_model", self.consumer)
        self.assertNotIn("apply_render_model(native", self.consumer)
        self.assertNotIn("PresentationUI.apply_render_model", self.consumer)
        self.assertIn('SharedLayerScript.new()', self.consumer)
        self.assertEqual(self.consumer.count('"mount", _frame'), 1)
        self.assertIn('"apply_render_model", shared_model_result["render_model"]', self.consumer)

    def test_visibility_overrides_are_limited_to_hook_countdown_and_cta(self):
        self.assertIn("_presentation_ui.hook_label.visible =", self.consumer)
        self.assertIn("_presentation_ui.countdown.visible =", self.consumer)
        self.assertIn("_presentation_ui.cta.visible =", self.consumer)
        self.assertNotIn("_presentation_ui.reveal_manager", self.consumer)
        self.assertNotIn("_presentation_ui.winning_highlight", self.consumer)

    def test_envelope_pins_identity_timebase_six_fields_and_governance(self):
        for token in (
            "EnvelopeSchema", "ApprovedPolicySha", "LayoutContractSha",
            "source_timebase", "source_phase_ranges", "ExpectedFields",
            "PREPARED_E1_NOT_DISPATCHED", "production_dispatch", "media_created",
            "release_authority", "SOURCE_FPS_HALF_OPEN",
        ):
            self.assertIn(token, self.consumer)

    def test_source_frame_ranges_use_explicit_schema_comparison(self):
        self.assertIn("func _source_frame_ranges_match(actual_value: Variant, expected_ranges: Array) -> bool:", self.consumer)
        self.assertIn('int(actual_row.get("start_frame", -1))', self.consumer)
        self.assertIn('int(actual_row.get("end_frame", -1))', self.consumer)
        self.assertIn('JSON.stringify(expected_ranges)', self.consumer)
        self.assertNotIn('ranges_value != expected_ranges', self.consumer)

    def test_does_not_mutate_native_render_model_or_protected_c_mechanics(self):
        self.assertNotIn('native_render_model[', self.consumer)
        for protected in ("SimulationResult", "FrameSnapshot", "winning_frame", "close_calls", "WinningFrameDetector"):
            self.assertNotIn(protected, self.consumer)

    def test_summary_records_single_mount_and_test_only_boundary(self):
        summary = self.consumer[self.consumer.index("func get_runtime_summary") : self.consumer.index("func _expected_phase_ranges")]
        self.assertIn('"mount_count": _mount_count', summary)
        self.assertIn('"production_dispatch": false', summary)
        self.assertIn('"media_created": false', summary)
        self.assertIn('"release_authority": "NONE"', summary)


if __name__ == "__main__":
    unittest.main(verbosity=2)
