from __future__ import annotations
import hashlib, importlib.util, json, os, re, sys, tempfile, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
HELPER=ROOT/"tools/c11d/d9/c11e_e6_l2_qimage_import_v5.py"
RUNNER=ROOT/"tools/c11d/d9/RUN_C11E_E6_L2_QIMAGE_COMPOSITION_REPAIR_V5.py"
INSTALLER=Path(os.environ.get("C11E_L2_V5_INSTALLER_SOURCE", str(ROOT/"INSTALL_C11E_E6_L2_QIMAGE_COMPOSITION_REPAIR_V5.ps1")))
POLICY=ROOT/"definitions/c11e/test_only/C11E_E6_L2_QIMAGE_COMPOSITION_SUCCESSOR_POLICY_V5.json"
MANIFEST=ROOT/"definitions/c11e/test_only/C11E_E6_L2_QIMAGE_COMPOSITION_EXECUTION_MANIFEST_V5.json"
PINS=ROOT/"definitions/c11e/test_only/C11E_E6_L2_QIMAGE_REPAIR_SOURCE_MANIFEST_V5.json"

spec=importlib.util.spec_from_file_location("v5_test_loader",HELPER)
helper=importlib.util.module_from_spec(spec); sys.modules[spec.name]=helper; spec.loader.exec_module(helper)

class RegisteredImportTests(unittest.TestCase):
    def test_01_loader_registers_before_exec_for_future_annotations(self):
        source='''from __future__ import annotations\nfrom dataclasses import dataclass\nfrom typing import ClassVar, Any\nimport sys\nassert sys.modules[__name__] is not None\n@dataclass(frozen=True)\nclass Sample:\n    marker: ClassVar[str] = "registered"\n    rect: tuple[int, int, int, int]\n    payload: dict[str, Any]\n'''
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"sample.py"; p.write_text(source,encoding="utf-8")
            mod=helper.load_module_registered(p,"c11e_v5_dataclass_fixture")
            self.assertIs(sys.modules["c11e_v5_dataclass_fixture"],mod)
            obj=mod.Sample((1,2,3,4),{"ok":True})
            self.assertEqual(obj.rect,(1,2,3,4))
            self.assertEqual(mod.Sample.marker,"registered")
            sys.modules.pop("c11e_v5_dataclass_fixture",None)

    def test_02_unregistered_import_reproduces_original_v4_failure(self):
        source='''from __future__ import annotations\nfrom dataclasses import dataclass\nfrom typing import ClassVar\n@dataclass\nclass Sample:\n    marker: ClassVar[str] = "x"\n    value: tuple[int, int]\n'''
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"sample.py"; p.write_text(source,encoding="utf-8")
            spec=importlib.util.spec_from_file_location("c11e_v4_unregistered_fixture",p)
            mod=importlib.util.module_from_spec(spec)
            with self.assertRaises(AttributeError) as ctx: spec.loader.exec_module(mod)
            self.assertIn("__dict__",str(ctx.exception))
            self.assertNotIn("c11e_v4_unregistered_fixture",sys.modules)

    def test_03_failed_import_removes_partial_module_registration(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"broken.py"; p.write_text("raise RuntimeError('fixture failure')\n",encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError,"fixture failure"):
                helper.load_module_registered(p,"c11e_v5_failed_fixture")
            self.assertNotIn("c11e_v5_failed_fixture",sys.modules)

    def test_04_existing_module_name_is_rejected(self):
        name="c11e_v5_existing_fixture"; sentinel=object(); sys.modules[name]=sentinel
        try:
            with tempfile.TemporaryDirectory() as d:
                p=Path(d)/"x.py"; p.write_text("value=1\n",encoding="utf-8")
                with self.assertRaisesRegex(RuntimeError,"MODULE_NAME_ALREADY_REGISTERED"):
                    helper.load_module_registered(p,name)
                self.assertIs(sys.modules[name],sentinel)
        finally: sys.modules.pop(name,None)

    def test_05_missing_source_is_rejected(self):
        with self.assertRaises(FileNotFoundError): helper.load_module_registered(Path("missing-v5-module.py"),"c11e_v5_missing")

    def test_06_invalid_module_name_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"x.py"; p.write_text("value=1\n",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"MODULE_NAME_INVALID"):
                helper.load_module_registered(p,"bad name")

    def test_07_module_remains_registered_after_success(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"x.py"; p.write_text("value=42\n",encoding="utf-8")
            mod=helper.load_module_registered(p,"c11e_v5_success_fixture")
            self.assertIs(sys.modules["c11e_v5_success_fixture"],mod)
            self.assertEqual(mod.value,42)
            sys.modules.pop("c11e_v5_success_fixture",None)

class ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy=json.loads(POLICY.read_text(encoding="utf-8"))
        cls.manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.pins=json.loads(PINS.read_text(encoding="utf-8"))
        cls.runner=RUNNER.read_text(encoding="utf-8")
        cls.helper=HELPER.read_text(encoding="utf-8")

    def test_08_v5_policy_is_qimage_only(self): self.assertEqual(self.policy["revision"],5); self.assertEqual(self.policy["scope"]["max_qimage_compositions"],1)
    def test_09_v5_policy_uses_existing_v4_capture(self): self.assertEqual(self.policy["source_capture"]["receipt_sha256"],"b36f319a3b7e3290be965dfc1bfa28fdff789b6054e89fc9c3cba182130aad88")
    def test_10_no_godot_process_allowed(self): self.assertEqual(self.manifest["process_limit"]["godot"],0); self.assertIn("GODOT_INVOCATIONS=0",self.runner)
    def test_11_no_media_tools_allowed(self):
        for k in ("ffmpeg","ffprobe","audio","mux","dispatch","batch_id"): self.assertEqual(self.manifest["process_limit"][k],0)
    def test_12_single_selector_preserved(self): self.assertEqual(self.manifest["selector"],["E6-L-01","fractal_bloom","radial_bloom",100006,0])
    def test_13_single_frame_source_format_rgba8(self): self.assertEqual(self.manifest["source_capture"]["source_format"],"RGBA8")
    def test_14_input_rgb24_exact_bytes(self): self.assertEqual(self.manifest["source_capture"]["rgb24_bytes"],2764800)
    def test_15_input_rgb24_exact_stride(self): self.assertEqual(self.manifest["source_capture"]["rgb24_stride_bytes"],2160)
    def test_16_capture_buffer_hash_is_frozen(self): self.assertEqual(self.manifest["source_capture"]["rgb24_sha256"],"a0803353be7dca53a75903a1c863bd814a4367b534e698018d8ab434f5506d03")
    def test_17_source_png_hash_is_frozen(self): self.assertEqual(self.manifest["source_capture"]["png_sha256"],"39ae0a4df012faf1b2fd087443ccadf963bb59610affc2756c1732fa42669908")
    def test_18_source_capture_run_id_is_exact(self): self.assertIn("E6L2RGB24V4_20261120T095847Z_A8AA1CA7",self.runner)
    def test_19_v4_receipt_sha_is_frozen(self): self.assertEqual(self.manifest["source_capture"]["receipt_sha256"],"b36f319a3b7e3290be965dfc1bfa28fdff789b6054e89fc9c3cba182130aad88")
    def test_20_v4_receipt_failure_signature_is_exact(self): self.assertIn("AttributeError:'NoneType' object has no attribute '__dict__'",self.runner)
    def test_21_v4_processes_must_both_exit_zero(self): self.assertIn("any(p.get(\"exit_code\")!=0 for p in procs)",self.runner)
    def test_22_capture_log_pass_marker_is_required(self): self.assertIn("C11E_L2_CAPTURE=PASS/ONE_FRAME",self.runner)
    def test_23_typography_class_log_is_required(self): self.assertIn("TypographyLabel",self.runner)
    def test_24_v4_install_receipt_is_frozen(self): self.assertEqual(self.manifest["source_capture"]["install_receipt_sha256"],"2afb58e86cddfa6bea3c412071f3ba0ca882a95af8c8274382d478d34ef840eb")
    def test_25_v4_install_semantics_checked(self): self.assertIn("V4_INSTALL_RECEIPT_SEMANTICS_MISMATCH",self.runner)
    def test_26_qimage_module_hash_is_exact(self): self.assertEqual(self.pins["qimage_module"]["sha256"],"850054e6212f7e6f59be5550ec194df3d1a1ca69acb343c53b76803b007721e1")
    def test_27_import_helper_registers_before_exec(self): self.assertLess(self.helper.index("sys.modules[module_name] = module"),self.helper.index("spec.loader.exec_module(module)"))
    def test_28_runner_uses_safe_loader(self): self.assertIn("load_module_registered(qimage_path",self.runner)
    def test_29_runner_does_not_use_unregistered_module_from_spec(self): self.assertNotIn("module_from_spec(spec)",self.runner)
    def test_30_dataclass_failure_cleanup_is_tested(self): self.assertIn("unregistered_import_reproduces_original_v4_failure",(ROOT/"tests/c11e/e6_l2_direct_rgb24_qimage_composition_v5/test_l2_qimage_composition_v5.py").read_text())
    def test_31_output_geometry_fixed(self): self.assertIn("QIMAGE_COMPOSED_GEOMETRY_INVALID",self.runner)
    def test_32_output_black_bands_checked(self):
        for k in ("QIMAGE_HEADER_BAND_NOT_BLACK","QIMAGE_FOOTER_BAND_NOT_BLACK","QIMAGE_LEFT_GUTTER_NOT_BLACK","QIMAGE_RIGHT_GUTTER_NOT_BLACK"): self.assertIn(k,self.runner)
    def test_33_saved_png_is_pixel_verified(self): self.assertIn("QIMAGE_SAVED_PNG_PIXEL_POSTIMAGE_MISMATCH",self.runner)
    def test_34_composition_cardinality_exact(self): self.assertIn('"qimage_composition_count":1',self.runner)
    def test_35_runner_receipt_is_v5(self): self.assertIn("C11E-E6-L2-QIMAGE-COMPOSITION-REPAIR-RECEIPT-V5",self.runner)
    def test_36_l2_remains_pending_visual_review(self): self.assertIn("PENDING_OPERATOR_VISUAL_REVIEW",self.runner)
    def test_37_no_color_assumption(self): self.assertIn('"bt709_assumed":False',self.runner)
    def test_38_no_git_checks(self): self.assertEqual(self.manifest["governance"]["git_checks"],"SKIPPED"); self.assertNotIn("git.exe",self.runner.lower())
    def test_39_commits_operator_managed(self): self.assertEqual(self.manifest["governance"]["commits"],"OPERATOR_MANAGED")
    def test_40_c11c_frozen(self): self.assertEqual(self.manifest["governance"]["c11c_frozen_manifest_sha256"],"e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953")
    def test_41_d4_8_immutable(self): self.assertEqual(self.manifest["governance"]["d4_8_v2_sha256"],"0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07")
    def test_42_e6_accepted_zero(self): self.assertEqual(self.manifest["governance"]["e6_accepted"],0)
    def test_43_release_authority_none(self): self.assertEqual(self.manifest["governance"]["release_authority"],"NONE")
    def test_44_output_root_v5_only(self): self.assertIn("e6_l2_direct_rgb24_qimage_composition_v5",self.runner)
    def test_45_v4_source_artifact_read_only(self): self.assertIn("copyfile(src,dst)",self.runner)
    def test_46_original_v4_receipt_is_not_written(self): self.assertNotIn("receipt_path.write_text",self.runner)
    def test_47_qimage_source_not_redecoded_from_mp4(self): self.assertIn("V4_CAPTURE_EVIDENCE=PASS/REUSED_NO_GODOT",self.runner); self.assertIn('"historical_mp4_consumed":False',self.runner)
    def test_48_compositor_rgb24_source_length_validated(self): self.assertIn("V4_RGB24_BUFFER_REVALIDATION_FAILED",self.runner)
    def test_49_png_and_rgb24_are_compared(self): self.assertIn("V4_SOURCE_PNG_RGB24_DOES_NOT_MATCH_CAPTURE_BUFFER",self.runner)
    def test_50_pyside6_exact_version_is_checked(self): self.assertIn('PySide6.__version__!="6.11.2"',self.runner)
    def test_51_python_exact_version_is_checked(self): self.assertIn("sys.version_info[:3]!=(3,13,14)",self.runner)
    def test_52_source_pins_are_rechecked_after_composition(self): self.assertIn("for rel,digest,size in SOURCE_PINS: verify_file(project_root/Path(rel),digest,size)",self.runner)
    def test_53_receipt_sidecar_is_written(self): self.assertIn(".sha256",self.runner)
    def test_54_all_artifacts_get_hashes(self): self.assertIn('"artifacts":{name:',self.runner)
    def test_55_policy_forbids_source_modification(self): self.assertFalse(self.policy["scope"]["active_checkout_source_writes"])
    def test_56_policy_forbids_new_godot(self): self.assertFalse(self.policy["scope"]["godot_invocations"])
    def test_57_execution_manifest_matches_v5_run(self): self.assertEqual(self.manifest["revision"],5)
    def test_58_source_pin_count_is_twenty(self): self.assertEqual(len(self.pins["source_files"]),20)
    def test_59_source_pin_digests_are_sha256(self): self.assertTrue(all(re.fullmatch(r"[0-9a-f]{64}",p["sha256"]) for p in self.pins["source_files"]))
    def test_60_source_pin_paths_are_unique(self): self.assertEqual(len({p["path"] for p in self.pins["source_files"]}),20)
    def test_61_no_godot_subprocess_in_runner(self): self.assertNotIn("subprocess",self.runner)
    def test_62_no_os_process_invocation_in_runner(self):
        for t in ("subprocess.run(","subprocess.Popen(","os.system(","os.popen(","OS.execute(","--write-movie"):
            self.assertNotIn(t.lower(),self.runner.lower())
    def test_63_installer_source_pin_is_versioned(self): self.assertIn("QIMAGE_COMPOSITION_REPAIR_V5",INSTALLER.read_text(encoding="utf-8"))

if __name__=="__main__": unittest.main(verbosity=2)
