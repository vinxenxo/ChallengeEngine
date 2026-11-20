from __future__ import annotations
import binascii, importlib, json, os, struct, sys, zlib
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]
RUNNER_DIR = ROOT / "tools" / "c11d" / "d9"
if str(RUNNER_DIR) not in sys.path:
    sys.path.insert(0, str(RUNNER_DIR))
import c11e_e6_l3_loop_negative_controls_v1 as audit

POLICY = ROOT / "definitions/c11e/test_only/C11E_E6_L3_LOOP_NEGATIVE_CONTROL_POLICY_V1.json"
MANIFEST = ROOT / "definitions/c11e/test_only/C11E_E6_L3_LOOP_NEGATIVE_CONTROL_EXECUTION_MANIFEST_V1.json"
SOURCE_MANIFEST = ROOT / "definitions/c11e/test_only/C11E_E6_L3_LOOP_NEGATIVE_CONTROL_SOURCE_MANIFEST_V1.json"
REPORT_SCHEMA = ROOT / "definitions/c11e/test_only/C11E_E6_L3_LOOP_NEGATIVE_CONTROL_REPORT_SCHEMA_V1.json"


def make_png(width, height, channels, rows, filter_type=0):
    def chunk(kind, payload):
        return struct.pack('>I', len(payload)) + kind + payload + struct.pack('>I', binascii.crc32(kind + payload) & 0xffffffff)
    ctype = 2 if channels == 3 else 6
    ihdr = struct.pack('>IIBBBBB', width, height, 8, ctype, 0, 0, 0)
    scan = b''.join(bytes([filter_type]) + row for row in rows)
    return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr) + chunk(b'IDAT', zlib.compress(scan)) + chunk(b'IEND', b'')


class PNGDecoderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(__file__).parent / '_png_fixtures'
        self.tmp.mkdir(exist_ok=True)
    def tearDown(self):
        for p in self.tmp.glob('*'):
            p.unlink()
        self.tmp.rmdir()
    def write(self, name, data):
        p = self.tmp / name
        p.write_bytes(data)
        return p
    def test_01_rgb_png_decode(self):
        raw = bytes([1,2,3,4,5,6])
        p = self.write('rgb.png', make_png(2,1,3,[raw]))
        self.assertEqual(audit.decode_png_rgb(p)[:3], (2,1,raw))
    def test_02_rgba_png_extracts_rgb_and_requires_opaque_alpha(self):
        raw = bytes([1,2,3,255,4,5,6,255])
        p = self.write('rgba.png', make_png(2,1,4,[raw]))
        self.assertEqual(audit.decode_png_rgb(p)[:3], (2,1,bytes([1,2,3,4,5,6])))
    def test_03_bad_signature_rejected(self):
        p = self.write('bad.png', b'notpng')
        with self.assertRaises(audit.L3AuditError): audit.decode_png_rgb(p)
    def test_04_crc_mismatch_rejected(self):
        b = bytearray(make_png(1,1,3,[bytes([1,2,3])]))
        b[-5] ^= 1
        p = self.write('crc.png', bytes(b))
        with self.assertRaises(audit.L3AuditError): audit.decode_png_rgb(p)
    def test_05_wrong_alpha_rejected(self):
        p = self.write('alpha.png', make_png(1,1,4,[bytes([1,2,3,254])]))
        with self.assertRaises(audit.L3AuditError): audit.decode_png_rgb(p)
    def test_06_filter_sub_supported(self):
        p = self.write('sub.png', make_png(2,1,3,[bytes([1,2,3,3,3,3])], filter_type=1))
        self.assertEqual(audit.decode_png_rgb(p)[2], bytes([1,2,3,4,5,6]))
    def test_07_filter_up_supported(self):
        # A single row with filter Up is equivalent to no predictor from previous row.
        p = self.write('up.png', make_png(1,1,3,[bytes([7,8,9])], filter_type=2))
        self.assertEqual(audit.decode_png_rgb(p)[2], bytes([7,8,9]))
    def test_08_filter_average_supported(self):
        p = self.write('avg.png', make_png(1,1,3,[bytes([7,8,9])], filter_type=3))
        self.assertEqual(audit.decode_png_rgb(p)[2], bytes([7,8,9]))
    def test_09_filter_paeth_supported(self):
        p = self.write('paeth.png', make_png(1,1,3,[bytes([7,8,9])], filter_type=4))
        self.assertEqual(audit.decode_png_rgb(p)[2], bytes([7,8,9]))
    def test_10_unsupported_interlace_rejected(self):
        data = bytearray(make_png(1,1,3,[bytes([1,2,3])]))
        data[28] = 1
        # Repair IHDR CRC so the explicit interlace check is exercised.
        data[29:33] = struct.pack('>I', binascii.crc32(b'IHDR' + bytes(data[16:29])) & 0xffffffff)
        p = self.write('interlace.png', bytes(data))
        with self.assertRaises(audit.L3AuditError): audit.decode_png_rgb(p)


class ContractTests(unittest.TestCase):
    def good(self):
        return dict(width=720,height=1280,stride=2160,byte_count=2764800,digest=audit.SOURCE_RGB_SHA,
                    frame_index=0,pixel_format='RGB24',source_kind='DIRECT_CAPTURE',color_transform_applied=False)
    def test_01_valid_rgb24_contract_passes(self):
        audit.validate_rgb24_contract(**self.good())
    def test_02_wrong_width_fails(self):
        with self.assertRaises(audit.L3AuditError): audit.validate_rgb24_contract(**{**self.good(),'width':719})
    def test_03_wrong_height_fails(self):
        with self.assertRaises(audit.L3AuditError): audit.validate_rgb24_contract(**{**self.good(),'height':1279})
    def test_04_wrong_stride_fails(self):
        with self.assertRaises(audit.L3AuditError): audit.validate_rgb24_contract(**{**self.good(),'stride':2159})
    def test_05_wrong_byte_count_fails(self):
        with self.assertRaises(audit.L3AuditError): audit.validate_rgb24_contract(**{**self.good(),'byte_count':2764799})
    def test_06_wrong_hash_fails(self):
        with self.assertRaises(audit.L3AuditError): audit.validate_rgb24_contract(**{**self.good(),'digest':'0'*64})
    def test_07_frame_index_mismatch_fails(self):
        with self.assertRaises(audit.L3AuditError): audit.validate_rgb24_contract(**{**self.good(),'frame_index':1})
    def test_08_wrong_pixel_format_fails(self):
        with self.assertRaises(audit.L3AuditError): audit.validate_rgb24_contract(**{**self.good(),'pixel_format':'YUV420P'})
    def test_09_historical_mp4_decode_fails(self):
        with self.assertRaises(audit.L3AuditError): audit.validate_rgb24_contract(**{**self.good(),'source_kind':'HISTORICAL_MP4_DECODE'})
    def test_10_color_transform_fails(self):
        with self.assertRaises(audit.L3AuditError): audit.validate_rgb24_contract(**{**self.good(),'color_transform_applied':True})
    def test_11_approved_geometry_passes(self):
        audit.validate_geometry((720,1280),(108,192,504,896))
    def test_12_wrong_canvas_fails(self):
        with self.assertRaises(audit.L3AuditError): audit.validate_geometry((720,1279),(108,192,504,896))
    def test_13_wrong_content_rect_fails(self):
        with self.assertRaises(audit.L3AuditError): audit.validate_geometry((720,1280),(107,192,504,896))
    def test_14_content_rect_out_of_bounds_fails(self):
        with self.assertRaises(audit.L3AuditError): audit.validate_geometry((720,1280),(300,192,504,896))
    def test_15_protected_write_path_is_denied(self):
        protected = Path('C:/protected')
        out = Path('C:/output')
        with self.assertRaises(audit.L3AuditError): audit.guard_write_path(protected/'x.bin',out,(protected,))
    def test_16_outside_output_path_is_denied(self):
        protected = Path('C:/protected')
        out = Path('C:/output')
        with self.assertRaises(audit.L3AuditError): audit.guard_write_path(Path('C:/other')/'x.bin',out,(protected,))
    def test_17_l3_output_path_allowed(self):
        out = Path('C:/output')
        self.assertEqual(audit.guard_write_path(out/'report.json',out,(Path('C:/protected'),)),(out/'report.json').resolve())
    def test_18_zero_process_scope_passes(self):
        audit.validate_process_scope(dict(godot=0,ffmpeg=0,ffprobe=0,audio=0,mux=0,qimage_composition=0,dispatch=0,batch_id=0))
    def test_19_godot_process_is_rejected(self):
        with self.assertRaises(audit.L3AuditError): audit.validate_process_scope(dict(godot=1,ffmpeg=0,ffprobe=0,audio=0,mux=0,qimage_composition=0,dispatch=0,batch_id=0))
    def test_20_qimage_composition_is_rejected(self):
        with self.assertRaises(audit.L3AuditError): audit.validate_process_scope(dict(godot=0,ffmpeg=0,ffprobe=0,audio=0,mux=0,qimage_composition=1,dispatch=0,batch_id=0))
    def test_21_nine_negative_controls_reject(self):
        out = Path('C:/output')
        protected = (Path('C:/protected'),Path('C:/protected-install'))
        results = audit.run_negative_controls(out,protected)
        self.assertEqual(len(results),9)
        self.assertTrue(all(x['status']=='REJECTED_AS_EXPECTED' for x in results))
    def test_22_negative_control_ids_unique(self):
        ids = [x['id'] for x in audit.run_negative_controls(Path('C:/out'),(Path('C:/p'),Path('C:/pi')))]
        self.assertEqual(len(ids),len(set(ids)))


class PackageAndGovernanceTests(unittest.TestCase):
    def test_01_policy_and_manifest_ids_match(self):
        p=json.loads(POLICY.read_text(encoding='utf-8')); m=json.loads(MANIFEST.read_text(encoding='utf-8'))
        self.assertEqual(p['policy_id'],m['policy_id'])
        self.assertTrue(p['execution_authorized'])
    def test_02_scope_is_one_selector(self):
        m=json.loads(MANIFEST.read_text(encoding='utf-8'))
        self.assertEqual(m['selector'],['E6-L-01','fractal_bloom','radial_bloom',100006,0])
    def test_03_v5_receipt_pin_exact(self):
        m=json.loads(MANIFEST.read_text(encoding='utf-8'))
        self.assertEqual(m['predecessor']['l2_v5_receipt_sha256'],audit.V5_RECEIPT_SHA)
    def test_04_v4_capture_receipt_pin_exact(self):
        m=json.loads(MANIFEST.read_text(encoding='utf-8'))
        self.assertEqual(m['predecessor']['v4_capture_receipt_sha256'],audit.V4_RECEIPT_SHA)
    def test_05_geometry_manifest_exact(self):
        m=json.loads(MANIFEST.read_text(encoding='utf-8'))
        self.assertEqual(m['geometry']['content_rect'],[108,192,504,896])
    def test_06_all_nine_negative_controls_are_declared(self):
        m=json.loads(MANIFEST.read_text(encoding='utf-8'))
        self.assertEqual(len(m['negative_controls']),9)
    def test_07_process_limits_are_zero(self):
        m=json.loads(MANIFEST.read_text(encoding='utf-8'))
        self.assertTrue(all(v==0 for v in m['limits'].values()))
    def test_08_source_manifest_pin_count(self):
        s=json.loads(SOURCE_MANIFEST.read_text(encoding='utf-8'))
        self.assertEqual(s['source_dependency_manifest']['expected_source_file_count'],20)
    def test_09_source_manifest_has_receipt_and_artifact_hashes(self):
        s=json.loads(SOURCE_MANIFEST.read_text(encoding='utf-8'))
        self.assertEqual(len(s['protected_inputs']),16)
    def test_10_report_schema_keeps_human_review_pending(self):
        s=json.loads(REPORT_SCHEMA.read_text(encoding='utf-8'))
        self.assertIn('PENDING_OPERATOR_VISUAL_REVIEW',s['visual_review_values'])
    def test_11_operator_review_not_auto_accepted(self):
        p=json.loads(POLICY.read_text(encoding='utf-8'))
        self.assertIn('operator visual resampler decision remains separate',p['approval_basis']['scope'])
    def test_12_l2_l3_ready_false_until_review(self):
        s=json.loads(REPORT_SCHEMA.read_text(encoding='utf-8'))
        self.assertIn('L2_READY and L3_READY remain false',s['global_acceptance_rule'])
    def test_13_c11c_frozen_sha(self):
        p=json.loads(POLICY.read_text(encoding='utf-8'))
        self.assertEqual(p['governance']['c11c_frozen_manifest_sha256'],'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953')
    def test_14_d48_immutable_sha(self):
        p=json.loads(POLICY.read_text(encoding='utf-8'))
        self.assertEqual(p['governance']['d4_8_v2_sha256'],'0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07')
    def test_15_e6_accepted_zero(self):
        p=json.loads(POLICY.read_text(encoding='utf-8'))
        self.assertEqual(p['governance']['e6_accepted'],0)
    def test_16_release_authority_none(self):
        p=json.loads(POLICY.read_text(encoding='utf-8'))
        self.assertEqual(p['governance']['release_authority'],'NONE')
    def test_17_git_checks_skipped(self):
        p=json.loads(POLICY.read_text(encoding='utf-8'))
        self.assertEqual(p['governance']['git_checks'],'SKIPPED')
    def test_18_commits_operator_managed(self):
        p=json.loads(POLICY.read_text(encoding='utf-8'))
        self.assertEqual(p['governance']['commits'],'OPERATOR_MANAGED')
    def test_19_runner_uses_no_subprocess(self):
        src=(RUNNER_DIR/'c11e_e6_l3_loop_negative_controls_v1.py').read_text(encoding='utf-8')
        self.assertNotIn('subprocess',src)
        self.assertNotIn('os.system',src)
    def test_20_runner_does_not_launch_godot_or_media_tools(self):
        src=(RUNNER_DIR/'c11e_e6_l3_loop_negative_controls_v1.py').read_text(encoding='utf-8')
        self.assertNotIn('Popen(',src)
        self.assertNotIn('QImage(',src)
    def test_21_runner_rechecks_protected_inputs_after(self):
        src=(RUNNER_DIR/'c11e_e6_l3_loop_negative_controls_v1.py').read_text(encoding='utf-8')
        self.assertIn('protected_hashes_before',src)
        self.assertIn('PROTECTED_EVIDENCE_CHANGED_DURING_L3_AUDIT',src)
    def test_22_runner_writes_only_new_l3_root(self):
        src=(RUNNER_DIR/'c11e_e6_l3_loop_negative_controls_v1.py').read_text(encoding='utf-8')
        self.assertIn('e6_l3_loop_negative_controls_v1',src)
        self.assertIn('L3_RUN_DIRECTORY_COLLISION',src)
    def test_23_runner_does_not_change_l2_ready(self):
        src=(RUNNER_DIR/'c11e_e6_l3_loop_negative_controls_v1.py').read_text(encoding='utf-8')
        self.assertIn('"l2_ready":False',src)
        self.assertIn('PENDING_OPERATOR_VISUAL_REVIEW',src)
    def test_24_installer_path_is_supplied_explicitly(self):
        installer=os.environ.get('C11E_L3_INSTALLER_SOURCE')
        self.assertTrue(installer and Path(installer).is_file())
        src=Path(installer).read_text(encoding='utf-8')
        self.assertIn('POWERSHELL_5_1_REQUIRED',src)
        self.assertIn('INSTALL_STATUS=PASS_ADD_ONLY',src)
    def test_25_source_manifest_json_valid(self):
        json.loads(SOURCE_MANIFEST.read_text(encoding='utf-8'))
    def test_26_no_colorimetry_assumption(self):
        p=json.loads(POLICY.read_text(encoding='utf-8'))
        self.assertIn('BT.709 assumption',p['prohibited'])
    def test_27_l4_not_authorized_by_this_run(self):
        m=json.loads(MANIFEST.read_text(encoding='utf-8'))
        self.assertEqual(m['status'],'AUTHORIZED_SINGLE_RUN_READ_ONLY_TECHNICAL_AUDIT_PENDING_OPERATOR_VISUAL_REVIEW')
    def test_28_no_write_to_v4_v5_sources(self):
        p=json.loads(POLICY.read_text(encoding='utf-8'))
        self.assertIn('source/V4/V5 evidence modification',p['prohibited'])
    def test_29_v4_install_receipt_is_in_protected_source_manifest(self):
        s=json.loads(SOURCE_MANIFEST.read_text(encoding='utf-8'))
        names=[Path(x['path']).name for x in s['protected_inputs']]
        self.assertIn('C11E_E6_L2_DIRECT_RGB24_VISUAL_PROBE_V3_INSTALL_RECEIPT.json',names)
    def test_30_v4_install_sidecar_is_in_protected_source_manifest(self):
        s=json.loads(SOURCE_MANIFEST.read_text(encoding='utf-8'))
        names=[Path(x['path']).name for x in s['protected_inputs']]
        self.assertIn('C11E_E6_L2_DIRECT_RGB24_VISUAL_PROBE_V3_INSTALL_RECEIPT.json.sha256',names)
    def test_31_runner_loads_and_validates_l3_source_manifest(self):
        src=(RUNNER_DIR/'c11e_e6_l3_loop_negative_controls_v1.py').read_text(encoding='utf-8')
        self.assertIn('L3_SOURCE_MANIFEST_SHA',src)
        self.assertIn('L3_SOURCE_MANIFEST_SCHEMA_OR_COUNT_MISMATCH',src)
    def test_32_runner_guards_actual_output_writes(self):
        src=(RUNNER_DIR/'c11e_e6_l3_loop_negative_controls_v1.py').read_text(encoding='utf-8')
        self.assertIn('guard_write_path(candidate, output_root, allowed_roots)',src)
    def test_33_l3_source_manifest_pins_qimage_module_and_v5_manifest(self):
        src=(RUNNER_DIR/'c11e_e6_l3_loop_negative_controls_v1.py').read_text(encoding='utf-8')
        self.assertIn('qimage_module_sha256',src)
        self.assertIn('source_dependency_manifest',src)


if __name__ == '__main__':
    unittest.main(verbosity=2)
