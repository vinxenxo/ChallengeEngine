from __future__ import annotations
import hashlib, json, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
POLICY = json.loads((ROOT/"definitions/c11e/test_only/C11E_E6_L2_DIRECT_RGB24_VISUAL_PROBE_SUCCESSOR_POLICY_V1.json").read_text(encoding="utf-8"))
MANIFEST = json.loads((ROOT/"definitions/c11e/test_only/C11E_E6_L2_DIRECT_RGB24_VISUAL_PROBE_EXECUTION_MANIFEST_V1.json").read_text(encoding="utf-8"))
PINS = json.loads((ROOT/"definitions/c11e/test_only/C11E_E6_L2_DIRECT_RGB24_SOURCE_PIN_MANIFEST_V1.json").read_text(encoding="utf-8"))
class DirectRgb24ManifestTests(unittest.TestCase):
    def test_01_policy_and_manifest_ids_match(self):
        self.assertEqual(POLICY["policy_id"], MANIFEST["policy_id"])
    def test_02_scope_is_single_selector(self):
        self.assertEqual(MANIFEST["selector"]["selector_id"], "E6-L-01")
        self.assertEqual(POLICY["scope"]["max_captured_frames"], 1)
        self.assertEqual(POLICY["scope"]["max_composited_frames"], 1)
    def test_03_exact_gameplay_seed(self):
        self.assertEqual(MANIFEST["selector"]["gameplay_seed"], 100006)
    def test_04_exact_grammar(self):
        self.assertEqual(MANIFEST["selector"]["grammar_id"], "radial_bloom")
    def test_05_capture_frame_is_zero(self):
        self.assertEqual(MANIFEST["selector"]["frame_index"], 0)
    def test_06_source_is_not_historical_mp4(self):
        self.assertIn("VIEWPORT_RECAPTURE", POLICY["source_method"])
        self.assertFalse(MANIFEST["colorimetry"]["historical_yuv_source_used"])
    def test_07_colorimetry_not_invented(self):
        c=MANIFEST["colorimetry"]
        self.assertEqual(c["primaries"], "UNDECLARED")
        self.assertEqual(c["transfer"], "UNDECLARED")
        self.assertEqual(c["matrix"], "UNDECLARED")
        self.assertFalse(c["bt709_assumed"])
    def test_08_no_color_transform_authorized(self):
        self.assertFalse(MANIFEST["colorimetry"]["color_transform_applied"])
        self.assertFalse(POLICY["colorimetry"]["yuv_to_rgb_conversion"])
    def test_09_source_operation_requires_opaque_alpha(self):
        self.assertIn("opaque RGBA8", POLICY["colorimetry"]["allowed_operation"])
    def test_10_rgb24_buffer_bytes(self):
        self.assertEqual(MANIFEST["output"]["source_rgb24_bytes"], 720*1280*3)
    def test_11_rgb24_stride(self):
        self.assertEqual(MANIFEST["output"]["source_rgb24_stride"], 720*3)
    def test_12_rgba8_buffer_bytes(self):
        self.assertEqual(MANIFEST["output"]["source_bytes"], 720*1280*4)
    def test_13_output_geometry_is_approved(self):
        self.assertEqual(MANIFEST["output"]["content_rect"], [108,192,504,896])
    def test_14_qimage_existing_module_pin(self):
        self.assertEqual(MANIFEST["qimage_module_sha256"], "850054e6212f7e6f59be5550ec194df3d1a1ca69acb343c53b76803b007721e1")
    def test_15_godot_executable_sha_is_sha256(self):
        self.assertEqual(len(MANIFEST["godot_executable_sha256"]),64)
        int(MANIFEST["godot_executable_sha256"],16)
    def test_16_godot_invocation_cardinality(self):
        self.assertEqual(len(MANIFEST["godot_invocations"]),2)
        self.assertTrue(all(x["max_invocations"]==1 for x in MANIFEST["godot_invocations"]))
    def test_17_ffmpeg_and_ffprobe_are_forbidden(self):
        self.assertEqual(MANIFEST["process_limit"]["ffmpeg"],0)
        self.assertEqual(MANIFEST["process_limit"]["ffprobe"],0)
    def test_18_audio_mux_media_dispatch_are_forbidden(self):
        for k in ("audio","mux","media","dispatch","batch_id"):
            self.assertEqual(MANIFEST["process_limit"][k],0)
    def test_19_c11c_and_d48_immutable_hashes(self):
        self.assertEqual(MANIFEST["governance"]["c11c_frozen_manifest_sha256"],"e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953")
        self.assertEqual(MANIFEST["governance"]["d4_8_v2_sha256"],"0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07")
    def test_20_e6_not_accepted(self):
        self.assertEqual(MANIFEST["governance"]["e6_accepted"],0)
        self.assertEqual(MANIFEST["governance"]["release_authority"],"NONE")
    def test_21_policy_is_narrowly_authorized(self):
        self.assertTrue(POLICY["execution_authorized"])
        self.assertEqual(POLICY["scope"]["max_godot_processes"],2)
    def test_22_source_pin_manifest_contains_transitive_files(self):
        self.assertGreaterEqual(len(PINS["source_files"]),18)
    def test_23_all_source_pin_hashes_well_formed(self):
        for row in PINS["source_files"]:
            self.assertEqual(len(row["sha256"]),64)
            int(row["sha256"],16)
    def test_24_no_duplicate_source_pin_paths(self):
        paths=[x["path"] for x in PINS["source_files"]]
        self.assertEqual(len(paths),len(set(paths)))
    def test_25_direct_capture_script_enforces_alpha_and_frame_zero(self):
        gd=(ROOT/"tools/c11d/d9/c11e_e6_l2_direct_rgb24_visual_probe_v1/CaptureLoopFrame.gd").read_text(encoding="utf-8")
        self.assertIn("scene_instance.set_process(false)",gd)
        self.assertIn("rgba[src + 3] != 255",gd)
        self.assertIn('"frame_index": 0',gd)
    def test_26_capture_does_not_call_video_or_audio_tools(self):
        gd=(ROOT/"tools/c11d/d9/c11e_e6_l2_direct_rgb24_visual_probe_v1/CaptureLoopFrame.gd").read_text(encoding="utf-8")
        for token in ("OS.execute", "OS.create_process", "--write-movie", "MovieMaker", "AudioStream"):
            self.assertNotIn(token.lower(),gd.lower())
    def test_27_compositor_resampler_is_smoothtransformation(self):
        self.assertEqual(MANIFEST["qimage_backend"],"PYSIDE6_QIMAGE_CPP_SMOOTH_TRANSFORMATION_V1")
        self.assertEqual(MANIFEST["qimage_transformation"],"SmoothTransformation")
    def test_28_historical_receipts_are_pinned_not_modified(self):
        self.assertEqual(MANIFEST["predecessors"]["loop_source_closure_receipt_sha256"],"4763bf2e9b7e23ece40801407d615b80a58d84b91b33353c668d70d06502da4b")
        self.assertEqual(MANIFEST["predecessors"]["qimage_v2_7_receipt_sha256"],"95819ea730283ded149faa490b21e0df392341366a853b3c0913318fb203d783")
if __name__ == "__main__": unittest.main()
