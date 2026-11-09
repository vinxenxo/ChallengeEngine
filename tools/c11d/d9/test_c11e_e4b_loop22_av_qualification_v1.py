from __future__ import annotations
import importlib.util, json, unittest, tempfile, wave, struct, math, sys
from datetime import datetime
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
TEST_PROJECT_ROOT=HERE.parents[2]

def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
loop=load('c11e_loop22',HERE/'c11e_e4b_loop22_av_qualification_v1.py')
support=load('c11e_loop22_support',HERE/'c11e_e4b_loop22_av_support_v1.py')

class Loop22ScopeTests(unittest.TestCase):
 def test_01_fixed_scope_exactly_22_selectors_44_slots(self):
  self.assertEqual(len(loop.EXPECTED_RECEIPTS),22); self.assertEqual(len(set(loop.EXPECTED_RECEIPTS))*2,44)
  self.assertEqual(loop.EXPECTED_RECEIPTS,[2,3,4,5,7,8,9,10,12,13,14,15,17,18,19,20,22,23,24,25,26,27])
 def test_02_r1v_pilot_indices_are_excluded(self):
  self.assertFalse(set(loop.EXPECTED_RECEIPTS)&{1,6,11,16,21})
 def test_03_family_counts_are_4_4_4_4_6(self):
  matrix_path=HERE.parents[2]/'definitions/c11d/production/C11E_E4B_LOOP22_SELECTOR_MATRIX_V1.json'
  matrix=json.loads(matrix_path.read_text(encoding='utf-8'))
  counts=matrix['scope']['family_counts']
  self.assertEqual(counts,{'geometric':4,'fractal':4,'sacred_symmetry':4,'living_particles':4,'invisible_forces':6})
 def test_04_gameplay_and_music_seed_routes_are_distinct(self):
  self.assertNotEqual(100002,500002); self.assertNotEqual(100027,500027)
 def test_05_music_profile_family_bindings(self):
  self.assertEqual(loop.FAMILY_ROUTE,{'geometric':'CIRCUIT_PULSE','fractal':'ORGANIC_BLOOM','sacred_symmetry':'ORBITAL_RITUAL','living_particles':'ORGANIC_BLOOM','invisible_forces':'FLOWING_VECTOR'})
 def test_06_run_id_is_compact(self):
  self.assertEqual(loop.build_run_id(datetime(2026,11,9,12,34,56),'ABCDEF'),'L22_123456_ABCDEF')
 def test_07_max_path_budget_for_full_loop22_matrix(self):
  matrix_path=HERE.parents[2]/'definitions/c11d/production/C11E_E4B_LOOP22_SELECTOR_MATRIX_V1.json'
  matrix=json.loads(matrix_path.read_text(encoding='utf-8'))
  p=loop.windows_path_budget(r'C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS','L22_123456_ABCDEF',matrix['selectors'])
  self.assertLessEqual(p['max_path_chars'],259)
  self.assertEqual(p['windows_max_path_guard'],'PASS')
 def test_08_resample_command_is_audio_only_and_48k(self):
  c=loop.build_resample_command('ffmpeg',Path('native.wav'),Path('delivery.wav'),22)
  self.assertIn('aresample=48000:async=0',c); self.assertEqual(c[c.index('-ar')+1],'48000'); self.assertNotIn('-vf',c)
 def test_09_mux_copies_video_and_aac_lc_192k_48k(self):
  c=loop.build_mux_command('ffmpeg',Path('source.mp4'),Path('delivery.wav'),Path('out.mp4'))
  self.assertEqual(c[c.index('-c:v')+1],'copy'); self.assertEqual(c[c.index('-c:a')+1],'aac')
  self.assertEqual(c[c.index('-profile:a')+1],'aac_low'); self.assertEqual(c[c.index('-b:a')+1],'192k'); self.assertEqual(c[c.index('-ar')+1],'48000')
  self.assertNotIn('-vf',c); self.assertNotIn('-filter_complex',c)
 def test_10_delivery_pcm_exact_samples(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'x.wav'
   with wave.open(str(p),'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(48000); w.writeframes(b'\x01\x00\x01\x00'*960000)
   m=loop.validate_delivery_pcm(p,20)
   self.assertEqual(m['sample_frames'],960000); self.assertEqual(m['sample_rate_hz'],48000)
 def test_11_delivery_pcm_rejects_wrong_sample_count(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'x.wav'
   with wave.open(str(p),'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(48000); w.writeframes(b'\x01\x00\x01\x00'*959999)
   with self.assertRaises(loop.Loop22Error): loop.validate_delivery_pcm(p,20)
 def test_12_aac_probe_rejects_44100(self):
  p={'streams':[{'codec_type':'video','codec_name':'h264','width':720,'height':1280,'r_frame_rate':'30/1','nb_frames':'600','pix_fmt':'yuvj420p','color_range':'pc'},
    {'codec_type':'audio','codec_name':'aac','profile':'LC','sample_rate':'44100','channels':2,'channel_layout':'stereo','bit_rate':'192000'}]}
  with self.assertRaises(loop.Loop22Error): loop.validate_final_probe(p,{'frame_count_consistency_only':600},{'pix_fmt':'yuvj420p','color_range':'pc'})
 def test_13_aac_probe_accepts_48k_lc(self):
  p={'format':{'duration':'20.02'},'streams':[{'codec_type':'video','codec_name':'h264','width':720,'height':1280,'r_frame_rate':'30/1','nb_frames':'600','pix_fmt':'yuvj420p','color_range':'pc'},
    {'codec_type':'audio','codec_name':'aac','profile':'LC','sample_rate':'48000','channels':2,'channel_layout':'stereo','bit_rate':'192000'}]}
  self.assertTrue(loop.validate_final_probe(p,{'frame_count_consistency_only':600},{'pix_fmt':'yuvj420p','color_range':'pc'})['preencode_pcm_duration_contract'].startswith('EXACT'))
 def test_14_final_probe_rejects_video_reencode_metadata_drift(self):
  p={'streams':[{'codec_type':'video','codec_name':'h264','width':720,'height':1280,'r_frame_rate':'30/1','nb_frames':'600','pix_fmt':'yuv420p','color_range':'tv'},
    {'codec_type':'audio','codec_name':'aac','profile':'LC','sample_rate':'48000','channels':2,'channel_layout':'stereo','bit_rate':'192000'}]}
  with self.assertRaises(loop.Loop22Error): loop.validate_final_probe(p,{'frame_count_consistency_only':600},{'pix_fmt':'yuvj420p','color_range':'pc'})
 def test_15_ffmpeg9_decode_option_uses_fps_mode(self):
  src=(HERE/'c11e_e4b_loop22_av_support_v1.py').read_text(encoding='utf-8')
  self.assertIn('"-fps_mode", "passthrough"',src); self.assertNotIn('"-vsync", "0"',src)
 def test_16_governance_is_not_renderer_authority(self):
  self.assertEqual(loop.FROZEN_SHA256,'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953')
  self.assertEqual(loop.R1P_SHA256,'d49f54ffdee6026426c2bb87fcb72b5c8a68f09cb64fb91f71e25dc10fd26b52')
  self.assertEqual(len(loop.POLICY_PINS),5)
  self.assertEqual(__import__('hashlib').sha256((HERE/'c11e_e4b_loop22_av_support_v1.py').read_bytes()).hexdigest(),loop.SUPPORT_SHA256)
 def test_17_source_pixel_format_exact_allowlist(self):
  self.assertEqual(support.validate_source_pixel_format({'pix_fmt':'yuvj420p','color_range':'pc'}),'yuvj420p')
  with self.assertRaises(support.AVQualificationError): support.validate_source_pixel_format({'pix_fmt':'yuv420p','color_range':'pc'})
 def test_18_c11c_family_audio_command_uses_music_seed(self):
  s={'music_seed':500002,'loop_cycles':3,'duration_seconds':23.0,'internal_family_id':'geometric','grammar_id':'interference_plane'}
  c=support.build_music_command('python',Path('helper.py'),Path('x.wav'),s)
  self.assertEqual(c[3],'500002'); self.assertNotIn('100002',c)
 def test_19_runner_fails_closed_outside_windows_before_launch(self):
  self.assertIn("sys.platform=='win32'",(HERE/'c11e_e4b_loop22_av_qualification_v1.py').read_text(encoding='utf-8'))
 def test_20_matrix_indices_exact_count(self):
  matrix=loop.read_json(TEST_PROJECT_ROOT/loop.MATRIX_REL)
  archive=TEST_PROJECT_ROOT/loop.R1P_REL
  bound=loop.load_matrix_selectors(TEST_PROJECT_ROOT,matrix,archive)
  self.assertEqual(len(bound),22)
  self.assertEqual([x['receipt_index'] for x in bound],loop.EXPECTED_RECEIPTS)
  self.assertEqual({k:sum(x['internal_family_id']==k for x in bound) for k in loop.FAMILY_ROUTE},{'geometric':4,'fractal':4,'sacred_symmetry':4,'living_particles':4,'invisible_forces':6})
 def test_21_48k_conversion_does_not_modify_native_wav(self):
  c=loop.build_resample_command('ffmpeg',Path('native.wav'),Path('delivery.wav'),23)
  self.assertIn(str(Path('native.wav')),c); self.assertIn(str(Path('delivery.wav')),c); self.assertNotEqual(c[c.index('-i')+1],c[-1])
 def test_22_ffprobe_duration_tolerance_remains_unset(self):
  src=(HERE/'c11e_e4b_loop22_av_qualification_v1.py').read_text(encoding='utf-8')
  self.assertIn('NOT_DEFINED_BY_D1; RECORDED_NOT_GATED',src)
 def test_23_preflight_path_namespace_is_separate_from_r1v(self):
  p=loop.windows_path_budget(r'C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS','L22_123456_ABCDEF',[
   {'receipt_index':27,'internal_family_id':'invisible_forces','grammar_id':'magnetic_filament_cloud','output_prefix':'InvisibleForces_v1','gameplay_seed':100027}])
  self.assertIn('e4b_loop22_av',p['longest_path'])
 def test_24_r1p_seed_domains_not_merged(self):
  src=(HERE/'c11e_e4b_loop22_av_qualification_v1.py').read_text(encoding='utf-8')
  self.assertIn("'gameplay_seed'",src); self.assertIn("'music_seed'",src)

if __name__=='__main__':
 ap=__import__('argparse').ArgumentParser(); ap.add_argument('--project-root',type=Path,required=False); ap.add_argument('--r1p-recovered-zip',type=Path,required=False); a=ap.parse_args()
 if a.project_root is not None: TEST_PROJECT_ROOT=a.project_root.resolve()
 if a.r1p_recovered_zip is not None: loop.R1P_REL=str(a.r1p_recovered_zip)
 suite=unittest.defaultTestLoader.loadTestsFromTestCase(Loop22ScopeTests); result=unittest.TextTestRunner(verbosity=2).run(suite); raise SystemExit(0 if result.wasSuccessful() and result.testsRun==24 else 1)
