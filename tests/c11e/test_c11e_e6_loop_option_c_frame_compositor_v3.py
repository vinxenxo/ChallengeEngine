"""Offline tests for dependency-free C11-E E6 Loop Option C compositor V3."""
from __future__ import annotations
import hashlib, json, sys, unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "tools" / "c11d" / "d9"))
import c11e_e6_loop_option_c_frame_compositor_v3 as compositor
# Resolve the package-specific decision record using portable path components.
DECISION_PATH = PROJECT_ROOT.joinpath(*['docs', 'history', 'c11e', 'overlays', 'C11E_E6_OPTION_C_COMPOSITOR_V4_20261119_2040Z', 'C11E_E6_LOOP_OPTION_C_GEOMETRY_DECISION_V3.json'])


class OptionCGeometryTests(unittest.TestCase):
    def test_01_canvas_exact(self):
        self.assertEqual((compositor.CANVAS_WIDTH, compositor.CANVAS_HEIGHT), (720, 1280))
    def test_02_content_rect_exact(self):
        self.assertEqual(compositor.build_composition_plan(720, 1280).content_rect, compositor.Rect(108,192,504,896))
    def test_03_header_rect_exact(self):
        self.assertEqual(compositor.build_composition_plan(720,1280).header_rect, compositor.Rect(0,0,720,192))
    def test_04_footer_rect_exact(self):
        self.assertEqual(compositor.build_composition_plan(720,1280).footer_rect, compositor.Rect(0,1088,720,192))
    def test_05_left_gutter_exact(self):
        self.assertEqual(compositor.build_composition_plan(720,1280).left_gutter_rect, compositor.Rect(0,192,108,896))
    def test_06_right_gutter_exact(self):
        self.assertEqual(compositor.build_composition_plan(720,1280).right_gutter_rect, compositor.Rect(612,192,108,896))
    def test_07_scale_is_exact_seven_tenths(self):
        p=compositor.build_composition_plan(720,1280); self.assertEqual((p.scale.numerator,p.scale.denominator),(7,10))
    def test_08_no_crop(self): self.assertFalse(compositor.build_composition_plan(720,1280).crop)
    def test_09_no_nonuniform_scaling(self): self.assertFalse(compositor.build_composition_plan(720,1280).non_uniform_scaling)
    def test_10_larger_source_scale(self):
        p=compositor.build_composition_plan(1080,1920); self.assertEqual((p.scale.numerator,p.scale.denominator),(7,15))
    def test_11_reject_non_9_16(self):
        with self.assertRaisesRegex(compositor.OptionCCompositionError,"SOURCE_ASPECT_RATIO_MUST_BE_9_16"): compositor.build_composition_plan(1280,720)
    def test_12_reject_upscale(self):
        with self.assertRaisesRegex(compositor.OptionCCompositionError,"SOURCE_UPSCALE_NOT_ALLOWED"): compositor.build_composition_plan(360,640)
    def test_13_reject_zero_dimension(self):
        with self.assertRaisesRegex(compositor.OptionCCompositionError,"SOURCE_DIMENSIONS_MUST_BE_POSITIVE"): compositor.build_composition_plan(0,0)
    def test_14_reject_boolean_dimension(self):
        with self.assertRaisesRegex(compositor.OptionCCompositionError,"SOURCE_DIMENSIONS_MUST_BE_INTEGERS"): compositor.build_composition_plan(True,1280)
    def test_15_editorial_not_drawn(self): self.assertFalse(compositor.build_composition_plan(720,1280).editorial_text_drawn)
    def test_16_no_audio_or_media(self): self.assertFalse(compositor.build_composition_plan(720,1280).audio_or_media_created)
    def test_17_plan_serialization_stable(self):
        p=compositor.build_composition_plan(720,1280).to_dict(); self.assertEqual(p['scale'],'7/10'); self.assertEqual(p['resampler'],compositor.RESAMPLER)
    def test_18_geometry_decision_approved(self):
        d=json.loads(DECISION_PATH.read_text(encoding='utf-8')); self.assertEqual(d['decision_status'],'APPROVED_GEOMETRY_RETAINED_RESAMPLER_IMPLEMENTATION_ONLY')
        self.assertEqual(d['canvas'],{'width':720,'height':1280,'pixel_format':'RGB24','background_rgb':[0,0,0]})
    def test_19_resampler_quality_not_approved(self):
        d=json.loads(DECISION_PATH.read_text(encoding='utf-8')); self.assertIn('REQUIRES_SYNTHETIC_VISUAL_REVIEW',d['transform']['quality_status'])


class ExactAreaWeightTests(unittest.TestCase):
    def test_20_horizontal_weights_sum_to_source_width(self):
        w=compositor._axis_area_weights(720,504); self.assertTrue(all(sum(x[1] for x in row)==720 for row in w))
    def test_21_vertical_weights_sum_to_source_height(self):
        w=compositor._axis_area_weights(1280,896); self.assertTrue(all(sum(x[1] for x in row)==1280 for row in w))
    def test_22_weights_are_positive_and_in_bounds(self):
        for src,dst in ((720,504),(1280,896)):
            for row in compositor._axis_area_weights(src,dst):
                self.assertTrue(all(0<=i<src and w>0 for i,w in row))
    def test_23_weights_cover_every_destination_pixel(self):
        self.assertEqual(len(compositor._axis_area_weights(720,504)),504)
        self.assertEqual(len(compositor._axis_area_weights(1280,896)),896)
    def test_24_invalid_zero_axis_rejected(self):
        with self.assertRaisesRegex(compositor.OptionCCompositionError,'RESAMPLE_AXIS_LENGTHS_INVALID'):
            compositor._axis_area_weights(0,0)
    def test_25_noninteger_axis_rejected(self):
        with self.assertRaisesRegex(compositor.OptionCCompositionError,'RESAMPLE_AXIS_LENGTHS_MUST_BE_INTEGERS'):
            compositor._axis_area_weights(True,7)
    def test_26_upscale_axis_rejected(self):
        with self.assertRaisesRegex(compositor.OptionCCompositionError,'RESAMPLE_AXIS_LENGTHS_INVALID'):
            compositor._axis_area_weights(7,10)
    def test_27_each_axis_uses_at_most_three_source_pixels(self):
        self.assertLessEqual(max(len(row) for row in compositor._axis_area_weights(720,504)),3)
        self.assertLessEqual(max(len(row) for row in compositor._axis_area_weights(1280,896)),3)


class OptionCPixelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.solid_source = bytes((17,89,203)) * (720*1280)
        cls.output = compositor.compose_rgb24_frame(cls.solid_source,720,1280)
    def pixel(self, frame, x, y):
        i=(y*720+x)*3; return tuple(frame[i:i+3])
    def test_28_output_size_exact(self): self.assertEqual(len(self.output),720*1280*3)
    def test_29_header_is_black(self):
        self.assertEqual(self.pixel(self.output,360,0),(0,0,0)); self.assertEqual(self.pixel(self.output,360,191),(0,0,0))
    def test_30_footer_is_black(self):
        self.assertEqual(self.pixel(self.output,360,1088),(0,0,0)); self.assertEqual(self.pixel(self.output,360,1279),(0,0,0))
    def test_31_side_gutters_are_black(self):
        for x in (0,107,612,719): self.assertEqual(self.pixel(self.output,x,640),(0,0,0))
    def test_32_constant_source_preserved_exactly(self):
        for x,y in ((108,192),(360,640),(611,1087)): self.assertEqual(self.pixel(self.output,x,y),(17,89,203))
    def test_33_source_bytes_immutable(self):
        before=hashlib.sha256(self.solid_source).digest(); repeated=compositor.compose_rgb24_frame(self.solid_source,720,1280)
        self.assertEqual(repeated,self.output)
        self.assertEqual(hashlib.sha256(self.solid_source).digest(),before)
    def test_34_reject_bytearray(self):
        with self.assertRaisesRegex(compositor.OptionCCompositionError,'SOURCE_FRAME_MUST_BE_IMMUTABLE_BYTES'):
            compositor.compose_rgb24_frame(bytearray(720*1280*3),720,1280)
    def test_35_reject_wrong_source_byte_count(self):
        with self.assertRaisesRegex(compositor.OptionCCompositionError,'SOURCE_RGB24_BYTE_COUNT_MISMATCH'):
            compositor.compose_rgb24_frame(b'\x00'*12,720,1280)
    def test_36_area_filter_has_no_checkerboard_overshoot(self):
        dark=bytes((64,64,64))*720
        light=bytes((192,192,192))*720
        checker_source=b''.join(dark if y%2==0 else light for y in range(1280))
        filtered=compositor.compose_rgb24_frame(checker_source,720,1280)
        low=255; high=0
        for y in range(192,1088):
            start=(y*720+108)*3
            row=filtered[start:start+504*3]
            low=min(low,min(row)); high=max(high,max(row))
        self.assertGreaterEqual(low,64); self.assertLessEqual(high,192)
    def test_37_no_external_imaging_dependency(self):
        import ast, inspect
        tree=ast.parse(inspect.getsource(compositor))
        imported=[]
        for node in ast.walk(tree):
            if isinstance(node, ast.Import): imported.extend(alias.name.split('.')[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module: imported.append(node.module.split('.')[0])
        self.assertFalse(set(('PIL','numpy','cv2')) & set(imported))

if __name__ == '__main__':
    suite=unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    result=unittest.TextTestRunner(stream=sys.stdout,verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
