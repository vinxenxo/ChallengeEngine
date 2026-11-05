from pathlib import Path
import os
import unittest

ROOT = Path(os.environ["C11E_TEST_ROOT"]) if "C11E_TEST_ROOT" in os.environ else Path(__file__).resolve().parents[3]
CONSUMER = ROOT / "tools" / "c11d" / "d9" / "C11EChallengeLiveEditorialConsumer.gd"
SHARED_LAYER = ROOT / "core" / "presentation" / "C11CVisualEditorialLayer.gd"


class ReservedBandsBlackContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.consumer = CONSUMER.read_text(encoding="utf-8")
        cls.shared_layer = SHARED_LAYER.read_text(encoding="utf-8")

    def test_shared_layer_mounts_once_for_every_enabled_d_envelope(self):
        self.assertIn("if not _mounted:", self.consumer)
        self.assertNotIn("if editorial_enabled and not _mounted:", self.consumer)
        self.assertEqual(self.consumer.count('"mount", _frame'), 1)

    def test_inactive_bands_remain_opaque_black(self):
        helper = self.consumer[
            self.consumer.index("func _apply_reserved_band_state"):
            self.consumer.index("func get_runtime_summary")
        ]
        self.assertIn("Color(0.0, 0.0, 0.0, 1.0)", helper)
        self.assertIn("_header_container.visible = true", helper)
        self.assertIn("_footer_container.visible = true", helper)
        self.assertIn("_header_background.visible = true", helper)
        self.assertIn("_footer_background.visible = true", helper)
        self.assertIn("_header_background.color = opaque_black", helper)
        self.assertIn("_footer_background.color = opaque_black", helper)

    def test_only_active_regions_show_editorial_text_and_separator(self):
        helper = self.consumer[
            self.consumer.index("func _apply_reserved_band_state"):
            self.consumer.index("func get_runtime_summary")
        ]
        self.assertIn("_header_text.visible = header_active", helper)
        self.assertIn("_header_rule.visible = header_active", helper)
        self.assertIn("_footer_text.visible = footer_active", helper)
        self.assertIn("_footer_rule.visible = footer_active", helper)

    def test_band_state_is_applied_after_shared_layer_render_model_each_frame(self):
        section = self.consumer[
            self.consumer.index("func apply_after_native_bind"):
            self.consumer.index("func _apply_reserved_band_state")
        ]
        self.assertLess(
            section.index('_layer.call("apply_render_model", shared_model_result["render_model"])'),
            section.index("_apply_reserved_band_state(")
        )

    def test_runtime_summary_reports_full_coverage_without_changing_c_shared_layer(self):
        summary = self.consumer[
            self.consumer.index("func get_runtime_summary"):
            self.consumer.index("func _expected_phase_ranges")
        ]
        self.assertIn('"reserved_band_policy": "OPAQUE_BLACK_ALWAYS_WHILE_D_ENVELOPE_ENABLED"', summary)
        self.assertIn('"reserved_band_black_frames": _reserved_band_black_frames', summary)
        self.assertIn("SECTION_BACKGROUND := Color(\"05070B\")", self.shared_layer)
        self.assertIn("_header_container.visible = bool(editorial.get(\"show_header\", true))", self.shared_layer)


if __name__ == "__main__":
    unittest.main(verbosity=2)
