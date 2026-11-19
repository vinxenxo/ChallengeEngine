from __future__ import annotations
import hashlib
import unittest
from PySide6.QtGui import QColor, QImage
from tools.c11d.d9.c11e_e6_option_c_qimage_frame_compositor_v1 import (
    BACKEND, CANVAS_HEIGHT, CANVAS_WIDTH, CONTENT_HEIGHT, CONTENT_WIDTH,
    CONTENT_X, CONTENT_Y, FOOTER_Y, HEADER_HEIGHT, RIGHT_GUTTER_X,
    OptionCNativeCompositionError, build_composition_plan,
    compose_rgb24_frame, compose_rgb24_image,
)

W, H = 720, 1280

def constant_frame(rgb=(17, 83, 149)):
    pixel = bytes(rgb)
    return pixel * (W * H)

class GeometryTests(unittest.TestCase):
    def test_01_plan_schema_and_backend(self):
        p = build_composition_plan(W, H)
        self.assertEqual(p.schema, "C11E-E6-OPTION-C-QIMAGE-FRAME-COMPOSITOR-V1")
        self.assertEqual(p.backend, BACKEND)
    def test_02_canvas_exact(self):
        p = build_composition_plan(W, H)
        self.assertEqual((p.canvas_width, p.canvas_height), (720, 1280))
    def test_03_content_rect_exact(self):
        self.assertEqual(build_composition_plan(W,H).content_rect, (108,192,504,896))
    def test_04_header_exact(self):
        self.assertEqual(build_composition_plan(W,H).header_rect, (0,0,720,192))
    def test_05_footer_exact(self):
        self.assertEqual(build_composition_plan(W,H).footer_rect, (0,1088,720,192))
    def test_06_left_gutter_exact(self):
        self.assertEqual(build_composition_plan(W,H).left_gutter_rect, (0,192,108,896))
    def test_07_right_gutter_exact(self):
        self.assertEqual(build_composition_plan(W,H).right_gutter_rect, (612,192,108,896))
    def test_08_aspect_ratio(self):
        self.assertEqual(build_composition_plan(W,H).aspect_ratio, "9:16")
    def test_09_no_crop_or_distortion(self):
        p=build_composition_plan(W,H); self.assertFalse(p.crop); self.assertFalse(p.non_uniform_scaling)
    def test_10_no_upscale(self):
        self.assertFalse(build_composition_plan(W,H).upscale)
    def test_11_editorial_not_drawn(self):
        self.assertFalse(build_composition_plan(W,H).editorial_text_drawn)
    def test_12_audio_or_media_not_created(self):
        self.assertFalse(build_composition_plan(W,H).audio_or_media_created)
    def test_13_zero_width_rejected(self):
        with self.assertRaises(OptionCNativeCompositionError): build_composition_plan(0,H)
    def test_14_zero_height_rejected(self):
        with self.assertRaises(OptionCNativeCompositionError): build_composition_plan(W,0)
    def test_15_boolean_dimension_rejected(self):
        with self.assertRaises(OptionCNativeCompositionError): build_composition_plan(True,H)
    def test_16_noninteger_dimension_rejected(self):
        with self.assertRaises(OptionCNativeCompositionError): build_composition_plan(720.0,H)
    def test_17_aspect_mismatch_rejected(self):
        with self.assertRaises(OptionCNativeCompositionError): build_composition_plan(720,1200)
    def test_18_upscale_rejected(self):
        with self.assertRaises(OptionCNativeCompositionError): build_composition_plan(360,640)

class PixelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.src = constant_frame()
        cls.src_sha = hashlib.sha256(cls.src).hexdigest()
        cls.image = compose_rgb24_image(cls.src,W,H)
        cls.raw = bytes(cls.image.constBits())
    def test_19_output_image_dimensions(self):
        self.assertEqual((self.image.width(),self.image.height()),(720,1280))
    def test_20_output_is_rgb888(self):
        self.assertEqual(self.image.format(),QImage.Format.Format_RGB888)
    def test_21_output_stride(self):
        self.assertEqual(self.image.bytesPerLine(),2160)
    def test_22_output_exact_byte_count(self):
        self.assertEqual(len(self.raw),720*1280*3)
    def test_23_header_is_black(self):
        self.assertEqual(self.image.pixelColor(360,32),QColor(0,0,0))
    def test_24_footer_is_black(self):
        self.assertEqual(self.image.pixelColor(360,1200),QColor(0,0,0))
    def test_25_left_gutter_is_black(self):
        self.assertEqual(self.image.pixelColor(40,640),QColor(0,0,0))
    def test_26_right_gutter_is_black(self):
        self.assertEqual(self.image.pixelColor(680,640),QColor(0,0,0))
    def test_27_constant_content_rgb_preserved(self):
        self.assertEqual(self.image.pixelColor(360,640),QColor(17,83,149))
    def test_28_source_bytes_unchanged(self):
        self.assertEqual(hashlib.sha256(self.src).hexdigest(),self.src_sha)
    def test_29_repeat_output_deterministic(self):
        out=compose_rgb24_frame(self.src,W,H)
        self.assertEqual(hashlib.sha256(out).hexdigest(),hashlib.sha256(self.raw).hexdigest())
    def test_30_bytearray_rejected(self):
        with self.assertRaises(OptionCNativeCompositionError): compose_rgb24_frame(bytearray(self.src),W,H)
    def test_31_wrong_buffer_size_rejected(self):
        with self.assertRaises(OptionCNativeCompositionError): compose_rgb24_frame(self.src[:-1],W,H)
    def test_32_alpha_or_non_rgb_output_not_emitted(self):
        self.assertEqual(self.image.format(),QImage.Format.Format_RGB888)
        self.assertEqual(self.image.depth(),24)
    def test_33_image_null_false(self):
        self.assertFalse(self.image.isNull())
    def test_34_plan_serialization_stable(self):
        p=build_composition_plan(W,H)
        self.assertEqual(p.to_dict(),build_composition_plan(W,H).to_dict())

class BandedSamplingTests(unittest.TestCase):
    def test_35_gradient_fixture_has_nonblack_content(self):
        row=bytearray()
        for y in range(H):
            for x in range(W): row.extend((x%256,y%256,(x+y)%256))
        im=compose_rgb24_image(bytes(row),W,H)
        self.assertNotEqual(im.pixelColor(360,640),QColor(0,0,0))
    def test_36_checkerboard_output_stays_in_source_channel_bounds(self):
        row=bytearray()
        for y in range(H):
            for x in range(W):
                v=255 if ((x+y)&1)==0 else 0
                row.extend((v,v,v))
        im=compose_rgb24_image(bytes(row),W,H)
        p=im.pixelColor(360,640)
        self.assertGreaterEqual(p.red(),0); self.assertLessEqual(p.red(),255)
    def test_37_checkerboard_reduction_is_not_binary_at_sample(self):
        row=bytearray()
        for y in range(H):
            for x in range(W):
                v=255 if ((x+y)&1)==0 else 0
                row.extend((v,v,v))
        im=compose_rgb24_image(bytes(row),W,H)
        self.assertGreater(im.pixelColor(360,640).red(),0)
        self.assertLess(im.pixelColor(360,640).red(),255)

if __name__ == "__main__":
    unittest.main(verbosity=2)
