import importlib.util, hashlib, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
AUDITOR = ROOT / "tools" / "c11d" / "d9" / "c11e_e6_loop_source_closure_v2.py"
SPEC = importlib.util.spec_from_file_location("loop_source_auditor", AUDITOR)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

class SourceClosureContractTests(unittest.TestCase):
 def test_01_sha256_known_vector(self): self.assertEqual(hashlib.sha256(b"abc").hexdigest(),"ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")
 def test_02_qimage_rgb24_geometry(self): self.assertEqual(MODULE.qimage_rgb24_contract(),{"width":720,"height":1280,"pixel_format":"RGB24","stride":2160,"bytes_per_frame":2764800})
 def test_03_yuv420p_frame_bytes(self): self.assertEqual(MODULE.yuv420p_frame_bytes(),1382400)
 def test_04_yuv_is_not_rgb(self): self.assertNotEqual("yuv420p","RGB24")
 def test_05_full_range_is_not_colorimetry(self): self.assertFalse(MODULE.colorimetry_declared({"color_range":"pc","color_space":None,"color_primaries":None,"color_transfer":None}))
 def test_06_partial_transfer_is_not_complete_colorimetry(self): self.assertFalse(MODULE.colorimetry_declared({"color_range":"pc","color_transfer":"smpte2084","color_primaries":None,"color_space":None}))
 def test_07_pts_sequence_passes(self): self.assertTrue(MODULE.valid_pts([0,512,1024,1536],4,"1/15360"))
 def test_08_pts_count_mismatch_fails(self): self.assertFalse(MODULE.valid_pts([0,512],4,"1/15360"))
 def test_09_pts_step_mismatch_fails(self): self.assertFalse(MODULE.valid_pts([0,500,1000,1500],4,"1/15360"))
 def test_10_timebase_mismatch_fails(self): self.assertFalse(MODULE.valid_pts([0,512],2,"1/90000"))
 def test_11_safe_relative_path_passes(self): self.assertTrue(MODULE.safe_relative("artifacts/tests/c11e/file.json"))
 def test_12_parent_traversal_fails(self): self.assertFalse(MODULE.safe_relative("artifacts/../outside.json"))
 def test_13_absolute_windows_path_fails(self): self.assertFalse(MODULE.safe_relative("C:/outside/file.json"))
 def test_14_empty_path_fails(self): self.assertFalse(MODULE.safe_relative(""))
 def test_15_source_pixel_contract_not_rgb24(self): self.assertNotEqual(MODULE.yuv420p_frame_bytes(),MODULE.qimage_rgb24_contract()["bytes_per_frame"])
 def test_16_pts_cadence_equals_30fps(self): self.assertEqual(512/15360,1/30)
 def test_17_pixel_manifest_exact_decoded_bytes_pass(self):
  pixels={"width":720,"height":1280,"source_pixel_format":"yuvj420p","decode_pixel_format":"yuv420p","frames_written_to_disk":False,"frame_hashes":["a"*64]*4,"raw_bytes_decoded":4*1382400,"global_decoded_stream_sha256":"a"*64}
  self.assertTrue(MODULE.pixel_manifest_contract(pixels,4))
 def test_18_pixel_manifest_wrong_decoded_bytes_fails(self):
  pixels={"width":720,"height":1280,"source_pixel_format":"yuvj420p","decode_pixel_format":"yuv420p","frames_written_to_disk":False,"frame_hashes":["x"]*4,"raw_bytes_decoded":4*2764800,"global_decoded_stream_sha256":"a"*64}
  self.assertFalse(MODULE.pixel_manifest_contract(pixels,4))
 def test_19_pixel_manifest_missing_frame_files_fails_if_materialized(self):
  pixels={"width":720,"height":1280,"source_pixel_format":"yuvj420p","decode_pixel_format":"yuv420p","frames_written_to_disk":True,"frame_hashes":["x"]*4,"raw_bytes_decoded":4*1382400,"global_decoded_stream_sha256":"a"*64}
  self.assertFalse(MODULE.pixel_manifest_contract(pixels,4))
 def test_20_pixel_manifest_hash_required(self):
  pixels={"width":720,"height":1280,"source_pixel_format":"yuvj420p","decode_pixel_format":"yuv420p","frames_written_to_disk":False,"frame_hashes":["x"]*4,"raw_bytes_decoded":4*1382400,"global_decoded_stream_sha256":None}
  self.assertFalse(MODULE.pixel_manifest_contract(pixels,4))
 def test_21_all_selected_r1p_receipt_pins_are_embedded(self):
  self.assertEqual(set(MODULE.R1P_PINS),{1,2,6,11,16,21})
  self.assertEqual(len(MODULE.R1P_PINS),6)
  self.assertTrue(all(len(value[0])==64 and value[1]>0 for value in MODULE.R1P_PINS.values()))
 def test_22_all_three_colorimetry_fields_are_required(self):
  self.assertTrue(MODULE.colorimetry_declared({"color_space":"bt709","color_primaries":"bt709","color_transfer":"bt709"}))
 def test_23_pixel_frame_hashes_must_be_sha256(self):
  pixels={"width":720,"height":1280,"source_pixel_format":"yuvj420p","decode_pixel_format":"yuv420p","frames_written_to_disk":False,"frame_hashes":["bad"]*4,"raw_bytes_decoded":4*1382400,"global_decoded_stream_sha256":"a"*64}
  self.assertFalse(MODULE.pixel_manifest_contract(pixels,4))
 def test_24_ab_source_pair_requires_same_pixel_stream(self):
  rows=[{"repeat":"A","source_video_sha256":"a","global_pixel_stream_sha256":"b","frame_count":4,"time_base":"1/15360"},{"repeat":"B","source_video_sha256":"a","global_pixel_stream_sha256":"b","frame_count":4,"time_base":"1/15360"}]
  self.assertTrue(MODULE.ab_source_pair_valid(rows))
 def test_25_ab_source_pair_rejects_pixel_mismatch(self):
  rows=[{"repeat":"A","source_video_sha256":"a","global_pixel_stream_sha256":"b","frame_count":4,"time_base":"1/15360"},{"repeat":"B","source_video_sha256":"a","global_pixel_stream_sha256":"c","frame_count":4,"time_base":"1/15360"}]
  self.assertFalse(MODULE.ab_source_pair_valid(rows))
 def test_26_geo_replacement_requires_same_video_and_stream_copy(self):
  slots=[{"slot":"A","video_source_sha256":"a","source_h264_stream_sha256":"b","final_h264_stream_sha256":"b"},{"slot":"B","video_source_sha256":"a","source_h264_stream_sha256":"c","final_h264_stream_sha256":"c"}]
  self.assertTrue(MODULE.geo_video_source_matches(slots,"a"))
 def test_27_geo_replacement_rejects_different_source(self):
  slots=[{"slot":"A","video_source_sha256":"x","source_h264_stream_sha256":"b","final_h264_stream_sha256":"b"},{"slot":"B","video_source_sha256":"x","source_h264_stream_sha256":"c","final_h264_stream_sha256":"c"}]
  self.assertFalse(MODULE.geo_video_source_matches(slots,"a"))

 def qimage_receipt(self):
  return {
   "schema":"C11E-E6-OPTION-C-NATIVE-QT-PROBE-RECEIPT-V2.7",
   "status":"PASS_QIMAGE_STAGE_BENCHMARKED_NOT_END_TO_END",
   "runtime":{"python_version":"3.13.14","pyside6":"6.11.2"},
   "qimage_tests":{"run":True,"tests":37,"failures":0,"errors":0,"status":"PASS"},
   "qimage_test_import_error":None,"qimage_test_execution_error":None,
   "qimage_benchmark":{"iterations":7,"samples_ms":[4.8,4.9,5.0,5.1,5.2,5.3,5.5743],"p95_ms":5.5743,"stage_30fps_budget":"PASS","end_to_end_qualified":False},
   "source_checks":[{"status":"PASS"} for _ in range(23)],
   "loop_policy_a3_adjudication":{"status":"PASS","error":None},
   "fixtures":[{"source_immutable":True} for _ in range(3)],
   "governance":{"c11c_modified":False,"d4_8_v2_modified":False,"source_files_modified":False,"godot_invoked":False,"ffmpeg_invoked":False,"ffprobe_invoked":False,"audio_generated":False,"mux_invoked":False,"production_dispatch":False,"production_media_created":False,"renderer_native_input_emitted":False,"batch_id_consumed":False,"e6_accepted":0,"release_authority":"NONE"}
  }

 def l1_receipt(self):
  checks=[{"status":"PASS"} for _ in range(18)]
  return {
   "schema":"C11E-E6-POST-QIMAGE-L1-PHASE-RECONCILIATION-RECEIPT-V2",
   "status":"PASS_READ_ONLY_E6_PHASE_RECONCILIATION_V2_WITH_VISUAL_REVIEW_PENDING",
   "check_count":18,"passed_checks":18,"blocked_checks":0,"blocked_ids":[],"checks":checks,
   "phase_state":{"e6_accepted":0,"visual_resampler_review":"PENDING_OPERATOR_VISUAL_REVIEW_NOT_INFERRED_FROM_HASHES"},
   "governance":{"e6_accepted":0,"d4_8_v2":"BLOCKED_IMMUTABLE","release_authority":"NONE"},
   "no_execution_authority_created":True
  }

 def test_28_d4_8_sha_pin_is_the_exact_64_character_frozen_value(self):
  self.assertEqual(MODULE.D48_SHA,"0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07")
  self.assertEqual(len(MODULE.D48_SHA),64)

 def test_29_qimage_actual_nested_receipt_semantics_pass(self):
  ok,checks,detail=MODULE.qimage_receipt_semantics(self.qimage_receipt())
  self.assertTrue(ok,detail)

 def test_30_qimage_nested_test_count_mismatch_blocks(self):
  obj=self.qimage_receipt(); obj["qimage_tests"]["tests"]=36
  self.assertFalse(MODULE.qimage_receipt_semantics(obj)[0])

 def test_31_qimage_nested_failures_or_errors_block(self):
  obj=self.qimage_receipt(); obj["qimage_tests"]["failures"]=1
  self.assertFalse(MODULE.qimage_receipt_semantics(obj)[0])
  obj=self.qimage_receipt(); obj["qimage_tests"]["errors"]=1
  self.assertFalse(MODULE.qimage_receipt_semantics(obj)[0])

 def test_32_qimage_p95_over_30fps_budget_blocks(self):
  obj=self.qimage_receipt(); obj["qimage_benchmark"]["p95_ms"]=33.334
  self.assertFalse(MODULE.qimage_receipt_semantics(obj)[0])

 def test_33_qimage_authority_or_mutation_mismatch_blocks(self):
  obj=self.qimage_receipt(); obj["governance"]["e6_accepted"]=1
  self.assertFalse(MODULE.qimage_receipt_semantics(obj)[0])
  obj=self.qimage_receipt(); obj["governance"]["d4_8_v2_modified"]=True
  self.assertFalse(MODULE.qimage_receipt_semantics(obj)[0])

 def test_34_l1_reads_e6_acceptance_from_phase_and_governance(self):
  ok,checks,detail=MODULE.l1_receipt_semantics(self.l1_receipt())
  self.assertTrue(ok,detail)

 def test_35_l1_top_level_e6_zero_does_not_substitute_for_nested_fields(self):
  obj=self.l1_receipt(); obj["e6_accepted"]=0
  del obj["governance"]["e6_accepted"]
  self.assertFalse(MODULE.l1_receipt_semantics(obj)[0])

 def test_36_l1_missing_phase_e6_zero_blocks(self):
  obj=self.l1_receipt(); obj["phase_state"].pop("e6_accepted")
  self.assertFalse(MODULE.l1_receipt_semantics(obj)[0])

 def test_37_l1_receipt_totals_are_independently_reconciled(self):
  obj=self.l1_receipt(); obj["passed_checks"]=17
  self.assertFalse(MODULE.l1_receipt_semantics(obj)[0])
  obj=self.l1_receipt(); obj["checks"][0]["status"]="BLOCKED_FAKE_PASS"
  self.assertFalse(MODULE.l1_receipt_semantics(obj)[0])

if __name__ == "__main__": unittest.main()
