from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
EXECUTOR_DIR = PROJECT / "tools" / "c11d" / "d9"
if str(EXECUTOR_DIR) not in sys.path:
    sys.path.insert(0, str(EXECUTOR_DIR))

from c11e_e4c_drill_execution import (  # noqa: E402
    DrillExecutionError,
    changed_music_seed,
    phase_for_final_frame,
    product_id_for,
    require_visible_editorial,
    validate_request,
    _source_pins,
)


class DrillExecutionHelpersTests(unittest.TestCase):
    def test_phase_mapping_tracking_810_frames(self):
        gameplay = 630
        self.assertEqual(phase_for_final_frame(0, gameplay), ("PRE_ROLL", 0))
        self.assertEqual(phase_for_final_frame(89, gameplay), ("PRE_ROLL", 89))
        self.assertEqual(phase_for_final_frame(90, gameplay), ("GAME", 0))
        self.assertEqual(phase_for_final_frame(405, gameplay), ("GAME", 315))
        self.assertEqual(phase_for_final_frame(719, gameplay), ("GAME", 629))
        self.assertEqual(phase_for_final_frame(720, gameplay), ("END_CTA", 720))
        self.assertEqual(phase_for_final_frame(809, gameplay), ("END_CTA", 809))

    def test_phase_mapping_23_second_drill(self):
        gameplay = 510
        self.assertEqual(phase_for_final_frame(90, gameplay), ("GAME", 0))
        self.assertEqual(phase_for_final_frame(599, gameplay), ("GAME", 509))
        self.assertEqual(phase_for_final_frame(600, gameplay), ("END_CTA", 600))
        self.assertEqual(phase_for_final_frame(689, gameplay), ("END_CTA", 689))

    def test_phase_mapping_rejects_out_of_range(self):
        with self.assertRaisesRegex(DrillExecutionError, "outside"):
            phase_for_final_frame(690, 510)
        with self.assertRaisesRegex(DrillExecutionError, "positive"):
            phase_for_final_frame(0, 0)

    def test_changed_music_seed_never_collides_and_expected_c_seed(self):
        self.assertEqual(changed_music_seed(840001, 12345), 840002)
        changed = changed_music_seed(12344, 12345)
        self.assertNotEqual(changed, 12345)
        self.assertNotEqual(changed, 12344)
        changed_edge = changed_music_seed(2147483646, 12345)
        self.assertNotEqual(changed_edge, 2147483646)
        self.assertNotEqual(changed_edge, 12345)

    def test_product_id_uses_native_source_naming(self):
        self.assertEqual(product_id_for("tracking", 12345, 1, 0.75), "VisualDrill_tracking_seed_12345_T1_constant_S075")
        self.assertEqual(product_id_for("peripheral_scan", 12345, 5, 1.5), "VisualDrill_peripheral_scan_seed_12345_T5_constant_S150")

    def valid_request(self):
        return {
            "request_id": "D99-GUI-ABC123",
            "mode": "PRODUCTION",
            "selection": {"content_type": "visual_drills", "family_id": "tracking", "variant_id": "tier-1"},
            "seed": 12345,
            "music_seed": 840001,
            "delivery_profile_id": "REVIEW_720",
            "audio_enabled": True,
            "personalization_enabled": True,
            "variation_index": 0,
        }

    def test_request_accepts_only_canonical_drill_review_av(self):
        request = self.valid_request()
        self.assertEqual(validate_request(request)[:4], ("tracking", 1, 12345, 840001))
        request["music_seed"] = 12345
        with self.assertRaisesRegex(DrillExecutionError, "numerically distinct"):
            validate_request(request)

    def test_request_rejects_wrong_family_or_audio_disabled(self):
        request = self.valid_request()
        request["selection"]["family_id"] = "fractal"
        with self.assertRaisesRegex(DrillExecutionError, "exact 4-family"):
            validate_request(request)
        request["selection"]["family_id"] = "tracking"
        request["audio_enabled"] = False
        with self.assertRaisesRegex(DrillExecutionError, "audio_enabled=true"):
            validate_request(request)

    def test_request_rejects_non_production_or_non_review_profile(self):
        request = self.valid_request()
        request["mode"] = "REVIEW"
        with self.assertRaisesRegex(DrillExecutionError, "mode=PRODUCTION"):
            validate_request(request)
        request["mode"] = "PRODUCTION"
        request["delivery_profile_id"] = "SOCIAL_1080"
        with self.assertRaisesRegex(DrillExecutionError, "REVIEW_720"):
            validate_request(request)

    def test_visible_editorial_is_required_and_phase_scoped(self):
        blank = {"text": {"visible_fields": {}, "phase_visibility": {"GAME": False, "PRE_ROLL": False, "END_CTA": False, "DONE": False}}}
        with self.assertRaisesRegex(DrillExecutionError, "at least one non-empty"):
            require_visible_editorial(blank)
        plan = {"text": {"visible_fields": {"title": "  Reto  ", "subtitle": " ", "call_to_action": "unknown"}, "phase_visibility": {"GAME": True, "PRE_ROLL": False, "END_CTA": False, "DONE": False}}}
        self.assertEqual(require_visible_editorial(plan), {"title": "Reto"})

    def test_visible_editorial_rejects_wrong_phase_contract(self):
        plan = {"text": {"visible_fields": {"title": "Reto"}, "phase_visibility": {"GAME": True, "PRE_ROLL": True, "END_CTA": False, "DONE": False}}}
        with self.assertRaisesRegex(DrillExecutionError, "hidden during PRE_ROLL"):
            require_visible_editorial(plan)

    def test_source_pin_paths_fail_closed_before_manifest_access(self):
        root = Path(tempfile.mkdtemp())
        intent = {"source_identity": {"source_pins": [{"path": "../outside", "bytes": 1, "sha256": "0" * 64}]}}
        with self.assertRaisesRegex(DrillExecutionError, "unsafe or duplicated"):
            _source_pins(intent, root)

    def test_existing_cli_exposes_opt_in_without_changing_e1_default(self):
        cli = PROJECT / "c11c-suite" / "c11c-producer" / "c11e_production_cli.py"
        source = cli.read_text(encoding="utf-8")
        self.assertIn('\"--execute-drill-av\", action=\"store_true\"', source)
        self.assertIn('if args.execute_drill_av:', source)
        self.assertIn('prepare_c11e_production_intent(raw, root, request_origin=args.origin)', source)
        self.assertIn('from c11e_e4c_drill_execution import execute_drill_av_request', source)

    def test_existing_gui_calls_same_shared_adapter_only_after_visible_editorial(self):
        main = PROJECT / "c11c-suite" / "c11c-producer" / "main.py"
        source = main.read_text(encoding="utf-8")
        self.assertIn('"c11e_e4c_drill_execution.py"', source)
        self.assertIn('"--origin", "GUI"', source)
        self.assertIn("and _has_visible_editorial", source)
        self.assertIn("self.e4c_drill_process.setProgram(sys.executable)", source)


if __name__ == "__main__":
    unittest.main(verbosity=2)
