#!/usr/bin/env python3
"""Source contracts for the D-only Challenge -> C11C shared editorial adapter."""
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
ADAPTER = (HERE / "c11e_challenge_editorial_presentation_adapter.gd").read_text(encoding="utf-8")
MATERIALIZER = (HERE / "materialize_challenge_visual_payload_in_memory.gd").read_text(encoding="utf-8")


class ChallengeSharedLayerAdapterContracts(unittest.TestCase):
    def test_01_only_challenge_e1_intents_are_accepted(self):
        self.assertIn('request.get("content_type", "")', ADAPTER)
        self.assertIn('!= "challenges"', ADAPTER)
        self.assertIn("Challenge presentation option cannot be applied to Loop/Drill", ADAPTER)

    def test_02_legacy_intents_default_to_visible(self):
        self.assertIn('if not request.has("presentation_options")', ADAPTER)
        self.assertIn('"show_hook_countdown": true', ADAPTER)

    def test_03_explicit_visibility_option_is_strict_boolean(self):
        self.assertIn('typeof(visibility_value) != TYPE_BOOL', ADAPTER)
        self.assertIn('options.size() != 1', ADAPTER)

    def test_04_option_off_suppresses_native_hook_and_countdown_model(self):
        self.assertIn('adapted["show_hook"] = false', ADAPTER)
        self.assertIn('adapted["countdown_visible"] = false', ADAPTER)
        self.assertIn('adapted["countdown_value"] = ""', ADAPTER)

    def test_05_adapter_duplicates_native_c_render_model(self):
        self.assertIn('base_render_model.duplicate(true)', ADAPTER)
        self.assertIn('C11C binder', ADAPTER)

    def test_06_native_cta_has_one_owner(self):
        self.assertIn('adapted["cta_visible"] = false', ADAPTER)
        self.assertIn('D_C11C_SHARED_FOOTER', ADAPTER)
        self.assertIn('C_CHALLENGE_PRESENTATION_UI', ADAPTER)

    def test_07_uses_only_approved_common_fields(self):
        for field in ('title', 'subtitle', 'call_to_action'):
            self.assertIn(f'field_name == "{field}"', ADAPTER)
        self.assertIn('BLOCKED_GEOMETRY_UNRESOLVED', ADAPTER)

    def test_08_language_is_not_drawn(self):
        self.assertIn('disposition == "METADATA_ONLY"', ADAPTER)
        self.assertIn('field_name == "call_to_action" and region == "FOOTER"', ADAPTER)

    def test_09_empty_fields_are_omitted(self):
        self.assertIn('value.is_empty()', ADAPTER)
        self.assertIn('OMITTED_EMPTY', ADAPTER)

    def test_10_phase_windows_use_source_frame_half_open_intervals(self):
        self.assertIn('source_frame >= start_frame and source_frame < end_frame', ADAPTER)

    def test_11_adapter_reuses_c11c_visual_editorial_layer(self):
        self.assertIn('res://core/presentation/C11CVisualEditorialLayer.gd', ADAPTER)
        self.assertIn('layer.call("mount", frame)', ADAPTER)
        self.assertIn('layer.call("apply_render_model", shared_model["render_model"])', ADAPTER)

    def test_12_header_is_opaque_and_recomposes_native_hook_once(self):
        self.assertIn('header_background.color = Color("05070B")', ADAPTER)
        self.assertIn('header_native_hook_migrated', ADAPTER)
        self.assertIn('native_hook_overlap": false', ADAPTER)
        self.assertIn('recompose, do not overlay', ADAPTER.lower())

    def test_12a_native_hook_is_first_line_and_d_editorial_uses_remaining_header(self):
        self.assertIn('var header_line_1 := clean_hook if header_native_hook_migrated else title_text', ADAPTER)
        self.assertIn('var header_line_2: String = " · ".join(PackedStringArray(d_header_parts)) if header_native_hook_migrated else subtitle_text', ADAPTER)
        self.assertIn('var header_native_hook_migrated := header_active and show_hook_countdown', ADAPTER)

    def test_12aa_string_join_is_called_on_separator_not_packed_array(self):
        self.assertIn('" · ".join(PackedStringArray(d_header_parts))', ADAPTER)
        self.assertNotIn('PackedStringArray(d_header_parts).join', ADAPTER)

    def test_12b_c11c_three_line_layout_is_measured_after_mount(self):
        self.assertIn('get_header_layout_diagnostics', ADAPTER)
        self.assertIn('font.get_string_size(line', ADAPTER)
        self.assertIn('var max_width: float = 468.0', ADAPTER)
        self.assertIn('var box_height: float = 120.0', ADAPTER)
        self.assertIn('nonempty_lines.size() <= 3', ADAPTER)

    def test_13_footer_replaces_baked_native_cta_when_d_cta_exists(self):
        self.assertIn('Color("05070B")', ADAPTER)
        self.assertIn('replacing the pre-existing C CTA pixels', ADAPTER)

    def test_14_unresolved_challenge_fields_remain_blocked(self):
        self.assertIn('CHALLENGE_OVERLAY', ADAPTER)
        self.assertIn('unapproved Challenge visual field/region', ADAPTER)

    def test_15_materializer_uses_adapter_and_canonical_frame_scene(self):
        self.assertIn('ChallengeEditorialAdapter.build_shared_editorial_model', MATERIALIZER)
        self.assertIn('UnifiedSocialFrame.tscn', MATERIALIZER)
        self.assertIn('C11CVisualEditorialLayer', MATERIALIZER)

    def test_16_materializer_has_no_placeholder_label_drawer(self):
        self.assertNotIn('_make_e4a_test_label', MATERIALIZER)

    def test_17_option_off_is_not_claimed_to_erase_baked_base_pixels(self):
        self.assertIn('OFF_APPLIES_TO_LIVE_RENDER_MODEL_ONLY_NOT_BAKED_BASE_FRAME_PIXELS', MATERIALIZER)

    def test_18_no_production_dispatch_or_release_authority(self):
        self.assertIn('production_dispatch', MATERIALIZER)
        self.assertIn('release_authority', MATERIALIZER)
        self.assertIn('visual_placement": "UNAPPROVED_TEST_ONLY', ADAPTER)

    def test_19_godot_probe_covers_partial_and_empty_editorial_arrangements(self):
        for marker in (
            "empty_fields_omitted",
            "title_only_header",
            "subtitle_only_header",
            "cta_only_footer",
            "challenge_overlay_blocked",
        ):
            self.assertIn(marker, MATERIALIZER)
        self.assertIn("_build_adapter_probe_fields", MATERIALIZER)

    def test_20_native_cta_is_hidden_only_when_d_footer_owns_populated_cta(self):
        self.assertIn('"footer_active": true', MATERIALIZER)
        self.assertIn('"native_cta_owner": "D_C11C_SHARED_FOOTER"', ADAPTER)
        self.assertIn('native_cta_model.get("cta_visible") != true', MATERIALIZER)
        self.assertIn('native_cta_model.get("cta_visible") != true', MATERIALIZER)

    def test_21_both_real_viewport_wait_markers_are_preserved(self):
        self.assertIn("E4A3_VIEWPORT_WAIT_FRAME_POST_DRAW", MATERIALIZER)
        self.assertIn("E4A3_VIEWPORT_FRAME_POST_DRAW_OK", MATERIALIZER)
        self.assertIn("E4A_SHARED_LAYER_FRAME_POST_DRAW_OK", MATERIALIZER)


if __name__ == "__main__":
    unittest.main(verbosity=2)
