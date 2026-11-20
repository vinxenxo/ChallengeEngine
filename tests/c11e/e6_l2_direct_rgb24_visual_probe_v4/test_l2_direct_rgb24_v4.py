from __future__ import annotations
import hashlib, json, re, unittest, os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
POLICY = json.loads((ROOT/"definitions/c11e/test_only/C11E_E6_L2_DIRECT_RGB24_VISUAL_PROBE_SUCCESSOR_POLICY_V4.json").read_text(encoding="utf-8"))
MANIFEST = json.loads((ROOT/"definitions/c11e/test_only/C11E_E6_L2_DIRECT_RGB24_VISUAL_PROBE_EXECUTION_MANIFEST_V4.json").read_text(encoding="utf-8"))
PINS = json.loads((ROOT/"definitions/c11e/test_only/C11E_E6_L2_DIRECT_RGB24_SOURCE_PIN_MANIFEST_V4.json").read_text(encoding="utf-8"))
RUNNER = (ROOT/"tools/c11d/d9/RUN_C11E_E6_L2_DIRECT_RGB24_VISUAL_PROBE_V4.py").read_text(encoding="utf-8")
GDSCRIPT_PATH = ROOT/"tools/c11d/d9/c11e_e6_l2_direct_rgb24_visual_probe_v4/CaptureLoopFrame.gd"
CAPTURE_GD_REL = Path("tools/c11d/d9/c11e_e6_l2_direct_rgb24_visual_probe_v4/CaptureLoopFrame.gd")
GDSCRIPT = GDSCRIPT_PATH.read_text(encoding="utf-8")
INSTALLER_SOURCE = os.environ.get("C11E_L2_INSTALLER_SOURCE", "")
INSTALLER_PATH = Path(INSTALLER_SOURCE) if INSTALLER_SOURCE else None
INSTALLER = INSTALLER_PATH.read_text(encoding="utf-8") if INSTALLER_PATH and INSTALLER_PATH.is_file() else ""

class DirectRgb24V4Tests(unittest.TestCase):
    def test_01_policy_and_manifest_ids_match(self): self.assertEqual(POLICY["policy_id"], MANIFEST["policy_id"])
    def test_02_policy_is_v4_and_narrow(self): self.assertEqual(POLICY["revision"],4); self.assertEqual(POLICY["scope"]["max_captured_frames"],1)
    def test_03_selector_is_exact(self): self.assertEqual(MANIFEST["selector"]["selector_id"],"E6-L-01")
    def test_04_gameplay_seed_is_exact(self): self.assertEqual(MANIFEST["selector"]["gameplay_seed"],100006)
    def test_05_grammar_is_exact(self): self.assertEqual(MANIFEST["selector"]["grammar_id"],"radial_bloom")
    def test_06_frame_index_is_zero(self): self.assertEqual(MANIFEST["selector"]["frame_index"],0)
    def test_07_single_capture_and_composition(self): self.assertEqual(POLICY["scope"]["max_captured_frames"],1); self.assertEqual(POLICY["scope"]["max_composited_frames"],1)
    def test_08_two_godot_invocations_only(self): self.assertEqual(POLICY["scope"]["max_godot_processes"],2); self.assertEqual(len(MANIFEST["godot_invocations"]),2)
    def test_09_godot_executable_pin_sha256(self): self.assertEqual(len(MANIFEST["godot_executable_sha256"]),64); int(MANIFEST["godot_executable_sha256"],16)
    def test_10_qimage_module_pin_unchanged(self): self.assertEqual(MANIFEST["qimage_module_sha256"],"850054e6212f7e6f59be5550ec194df3d1a1ca69acb343c53b76803b007721e1")
    def test_11_qimage_backend_smoothtransformation(self): self.assertEqual(MANIFEST["qimage_transformation"],"SmoothTransformation")
    def test_12_source_rgba_bytes(self): self.assertEqual(MANIFEST["output"]["source_bytes"],720*1280*4)
    def test_13_source_rgb24_bytes(self): self.assertEqual(MANIFEST["output"]["source_rgb24_bytes"],720*1280*3)
    def test_14_source_rgb24_stride(self): self.assertEqual(MANIFEST["output"]["source_rgb24_stride"],2160)
    def test_15_output_content_rect(self): self.assertEqual(MANIFEST["output"]["content_rect"],[108,192,504,896])
    def test_16_colorimetry_is_undeclared(self):
        c=MANIFEST["colorimetry"]; self.assertEqual(c["primaries"],"UNDECLARED"); self.assertEqual(c["transfer"],"UNDECLARED"); self.assertEqual(c["matrix"],"UNDECLARED")
    def test_17_bt709_not_assumed(self): self.assertFalse(MANIFEST["colorimetry"]["bt709_assumed"])
    def test_18_no_color_transform(self): self.assertFalse(MANIFEST["colorimetry"]["color_transform_applied"])
    def test_19_historical_mp4_not_consumed(self): self.assertFalse(MANIFEST["colorimetry"]["historical_yuv_source_used"])
    def test_20_ffmpeg_forbidden(self): self.assertEqual(MANIFEST["process_limit"]["ffmpeg"],0)
    def test_21_ffprobe_forbidden(self): self.assertEqual(MANIFEST["process_limit"]["ffprobe"],0)
    def test_22_audio_mux_media_dispatch_forbidden(self):
        for k in ("audio","mux","media","dispatch","batch_id"): self.assertEqual(MANIFEST["process_limit"][k],0)
    def test_23_c11c_frozen_hash(self): self.assertEqual(MANIFEST["governance"]["c11c_frozen_manifest_sha256"],"e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953")
    def test_24_d48_hash_unchanged(self): self.assertEqual(MANIFEST["governance"]["d4_8_v2_sha256"],"0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07")
    def test_25_e6_stays_unaccepted(self): self.assertEqual(MANIFEST["governance"]["e6_accepted"],0); self.assertEqual(MANIFEST["governance"]["release_authority"],"NONE")
    def test_26_typography_label_dependency_present(self):
        rows={x[0]:x for x in MANIFEST["source_pins"]}; self.assertIn("core/presentation/components/TypographyLabel.gd",rows)
    def test_27_typography_label_sha256_exact(self):
        rows={x[0]:x for x in MANIFEST["source_pins"]}; row=rows["core/presentation/components/TypographyLabel.gd"]
        self.assertEqual(row[1],"d7c6ec47b33baec983a239dfe6218037d4126dc1532130c92d4202d56e6e8866"); self.assertEqual(row[2],1240)
    def test_28_source_pin_manifest_contains_same_typography_label(self):
        rows={x["path"]:x for x in PINS["source_files"]}; self.assertIn("core/presentation/components/TypographyLabel.gd",rows)
    def test_29_no_duplicate_source_pin_paths(self):
        paths=[x["path"] for x in PINS["source_files"]]; self.assertEqual(len(paths),len(set(paths)))
    def test_30_runner_contains_typography_pin(self): self.assertIn("core/presentation/components/TypographyLabel.gd",RUNNER)
    def test_31_import_gate_checks_global_class(self): self.assertIn("TYPOGRAPHYLABEL_GLOBAL_CLASS_NOT_REGISTERED",RUNNER)
    def test_32_import_gate_precedes_capture_invocation(self): self.assertLess(RUNNER.index("TYPOGRAPHYLABEL_GLOBAL_CLASS_NOT_REGISTERED"),RUNNER.index("ONE_FRAME_GODOT_VIEWPORT_CAPTURE"))
    def test_33_subviewport_is_explicitly_fixed_size(self): self.assertIn("capture_viewport.size = Vector2i(WIDTH, HEIGHT)",GDSCRIPT)
    def test_34_subviewport_is_the_scene_parent(self): self.assertIn("capture_viewport.add_child(scene_instance)",GDSCRIPT)
    def test_35_subviewport_texture_is_captured(self): self.assertIn("capture_viewport.get_texture().get_image()",GDSCRIPT)
    def test_36_root_window_dimensions_are_not_used(self): self.assertNotIn("root.get_viewport()",GDSCRIPT); self.assertNotIn("get_visible_rect()",GDSCRIPT)
    def test_37_capture_metadata_declares_subviewport(self): self.assertIn('"viewport_source": "FIXED_SUBVIEWPORT_NO_WINDOW_DPI_DEPENDENCY"',GDSCRIPT)
    def test_38_opaque_alpha_is_verified(self): self.assertIn("rgba[src + 3] != 255",GDSCRIPT)
    def test_39_source_process_is_frozen_on_frame_zero(self): self.assertIn("scene_instance.set_process(false)",GDSCRIPT); self.assertIn('"frame_index": 0',GDSCRIPT)
    def test_40_no_video_audio_or_movie_tools_in_capture_script(self):
        for token in ("OS.execute","OS.create_process","--write-movie","MovieMaker","AudioStream"): self.assertNotIn(token.lower(),GDSCRIPT.lower())
    def test_41_capture_requires_exact_scene_identity(self): self.assertIn("resolved_seed != SEED or resolved_grammar != GRAMMAR",GDSCRIPT)
    def test_42_capture_script_pin_matches_manifest(self): self.assertEqual(MANIFEST["capture_script_sha256"],hashlib.sha256(GDSCRIPT_PATH.read_bytes()).hexdigest())
    def test_43_capture_script_bytes_match_manifest(self): self.assertEqual(MANIFEST["capture_script_bytes"],GDSCRIPT_PATH.stat().st_size)
    def test_44_predecessor_l2_failure_is_pinned(self): self.assertEqual(MANIFEST["predecessors"]["l2_v1_failed_receipt_sha256"],"6743645274026f59e1c8a5018d55af4e0dd30e0c37fcda6e9fcd67deb1cccbc8")
    def test_45_new_artifact_root_is_versioned(self): self.assertIn('e6_l2_direct_rgb24_visual_probe_v4',RUNNER)
    def test_46_v1_receipt_is_not_referenced_as_output(self): self.assertNotIn('C11E_E6_L2_DIRECT_RGB24_VISUAL_PROBE_RECEIPT_V1.json',RUNNER)
    def test_47_no_git_checks(self): self.assertEqual(MANIFEST['governance']['git_checks'],'SKIPPED'); self.assertNotIn('git.exe',RUNNER.lower())
    def test_48_commits_operator_managed(self): self.assertEqual(MANIFEST['governance']['commits'],'OPERATOR_MANAGED')
    def test_49_runner_stages_source_pins_only(self): self.assertIn('for rel, digest, size in SOURCE_PINS',RUNNER)
    def test_50_active_checkout_sources_are_rehashed_after_probe(self): self.assertGreaterEqual(RUNNER.count('for rel,digest,size in SOURCE_PINS: verify_file(project_root,rel,digest,size)'),1)
    def test_51_installer_requires_windows_powershell_51_ast(self): self.assertIn('POWERSHELL_5_1_REQUIRED',INSTALLER); self.assertIn('Parser]::ParseFile',INSTALLER)
    def test_52_installer_checks_exact_29_zip_members(self): self.assertIn('$zip.Entries.Count -ne 29',INSTALLER); self.assertIn('DUPLICATE_ZIP_MEMBER',INSTALLER)
    def test_53_installer_checks_all_staged_hashes_before_write(self): self.assertIn('STAGED_MEMBER_PIN_MISMATCH',INSTALLER); self.assertLess(INSTALLER.index('INSTALL_PREFLIGHT=PASS'),INSTALLER.index('[System.IO.File]::Open($tmp'))
    def test_54_installer_is_add_only_on_collision(self): self.assertIn('ADD_ONLY_DESTINATION_COLLISION',INSTALLER)
    def test_55_installer_uses_same_directory_temporary_and_atomic_move(self): self.assertIn("$tmp=$row.dest+'.tmp.'",INSTALLER); self.assertIn('[System.IO.File]::Move($tmp,$row.dest)',INSTALLER)
    def test_56_installer_rolls_back_only_owned_matching_postimages(self): self.assertIn('$owned=New-Object System.Collections.ArrayList',INSTALLER); self.assertIn('(Get-Sha256 $row.dest) -eq $row.sha',INSTALLER)
    def test_57_installer_cleans_transaction_created_empty_directories(self): self.assertIn('$createdDirs=New-Object System.Collections.ArrayList',INSTALLER); self.assertIn('[System.IO.Directory]::Delete($dir,$false)',INSTALLER)
    def test_58_installer_has_stage_path_budget(self): self.assertIn('INSTALL_STAGE_PATH_BUDGET',INSTALLER); self.assertIn('INSTALL_STAGE_MEMBER_PATH_BUDGET',INSTALLER)
    def test_59_installer_has_destination_and_temp_path_budgets(self): self.assertIn('INSTALL_DESTINATION_PATH_BUDGET',INSTALLER); self.assertIn('INSTALL_TEMP_PATH_BUDGET',INSTALLER)
    def test_60_installer_has_receipt_path_budget(self): self.assertIn('INSTALL_RECEIPT_PATH_BUDGET',INSTALLER)
    def test_61_policy_artifact_root_uses_v4_namespace(self): self.assertIn('e6_l2_direct_rgb24_visual_probe_v4_run_id_only',POLICY['write_scope']['artifact_root'])
    def test_62_source_manifest_pins_v4_capture_harness(self): self.assertEqual(PINS['godot_capture_harness']['path'],'tools/c11d/d9/c11e_e6_l2_direct_rgb24_visual_probe_v4/CaptureLoopFrame.gd'); self.assertEqual(PINS['godot_capture_harness']['sha256'],hashlib.sha256(GDSCRIPT_PATH.read_bytes()).hexdigest())


    def test_63_v2_receipt_sidecar_temp_would_exceed_classic_max_path(self):
        root=r"C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS\artifacts\tests\c11e\e6_l2_direct_rgb24_visual_probe_v2_install\E6L2RGB24V2INST_20261120T091948Z_99D13208"
        receipt=root+r"\C11E_E6_L2_DIRECT_RGB24_VISUAL_PROBE_V2_INSTALL_RECEIPT.json"
        old_tmp=receipt+r".sha256.tmp."+"0"*32
        self.assertGreater(len(old_tmp),260)

    def test_64_v3_sidecar_temp_is_short_sibling_path(self):
        root=r"C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS\artifacts\tests\c11e\e6_l2_direct_rgb24_visual_probe_v4_install\E6L2RGB24V3INST_20261120T000000Z_00000000"
        side_tmp=root+r"\s."+"0"*32+r".tmp"
        self.assertLessEqual(len(side_tmp),240)
        self.assertLess(len(side_tmp),len(root+r"\C11E_E6_L2_DIRECT_RGB24_VISUAL_PROBE_V4_INSTALL_RECEIPT.json.sha256.tmp."+"0"*32))

    def test_65_v3_receipt_and_sidecar_temps_are_short_siblings(self):
        self.assertIn("Join-Path $receiptRoot ('r.'+[Guid]::NewGuid().ToString('N')+'.tmp')",INSTALLER)
        self.assertIn("Join-Path $receiptRoot ('s.'+[Guid]::NewGuid().ToString('N')+'.tmp')",INSTALLER)

    def test_66_v3_receipt_temp_paths_are_budgeted_before_writes(self):
        self.assertIn('INSTALL_RECEIPT_TEMP_PATH_BUDGET',INSTALLER)
        self.assertIn('INSTALL_RECEIPT_PATH_BUDGET',INSTALLER)
        self.assertIn('if ($receiptCandidate.Length -gt 240)',INSTALLER)

    def test_67_v3_receipt_directory_created_before_payload_writes(self):
        self.assertLess(INSTALLER.index("RECEIPT_DIRECTORY=PASS/CREATED_BEFORE_PAYLOAD_WRITES"),INSTALLER.index("$tmp=$row.dest+'.tmp.'"))

    def test_68_v3_stages_both_receipt_temps_before_final_moves(self):
        self.assertLess(INSTALLER.index('[System.IO.File]::WriteAllBytes($receiptTmp,$receiptBytes)'),INSTALLER.index('[System.IO.File]::Move($receiptTmp,$receiptPath)'))
        self.assertLess(INSTALLER.index('[System.IO.File]::WriteAllBytes($sideTmp,$sideBytes)'),INSTALLER.index('[System.IO.File]::Move($receiptTmp,$receiptPath)'))
        self.assertIn('INSTALL_RECEIPT_SIDECAR_TEMP_CONTENT_MISMATCH',INSTALLER)

    def test_69_v3_receipt_final_sidecar_and_temp_same_directory(self):
        self.assertIn('$receiptSidecarPath=$receiptPath+\'.sha256\'',INSTALLER)
        self.assertIn("Join-Path $receiptRoot ('s.'",INSTALLER)

    def test_70_v3_rollback_removes_only_owned_hash_matching_postimages(self):
        self.assertIn('$owned=New-Object System.Collections.ArrayList',INSTALLER)
        self.assertIn('(Get-Sha256 $row.dest) -eq $row.sha',INSTALLER)
        self.assertIn('[System.IO.Directory]::Delete($dir,$false)',INSTALLER)

    def test_71_v3_installer_never_reuses_v2_install_receipt_root(self):
        self.assertIn('e6_l2_direct_rgb24_visual_probe_v4_install',INSTALLER)
        self.assertNotIn('e6_l2_direct_rgb24_visual_probe_v2_install',INSTALLER)

    def test_72_v4_manifest_records_test_and_pin_repair_without_scope_widening(self):
        self.assertEqual(MANIFEST['revision'],4)
        self.assertEqual(MANIFEST['selector']['selector_id'],'E6-L-01')
        self.assertEqual(MANIFEST['selector']['gameplay_seed'],100006)
        self.assertEqual(MANIFEST['process_limit']['ffmpeg'],0)
        self.assertEqual(MANIFEST['process_limit']['ffprobe'],0)
        self.assertEqual(MANIFEST['governance']['e6_accepted'],0)


    def test_73_runner_capture_sha_matches_execution_manifest(self):
        m=re.search(r'^CAPTURE_GD_SHA = "([0-9a-f]{64})"$',RUNNER,re.M)
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1),MANIFEST["capture_script_sha256"])

    def test_74_runner_capture_bytes_match_execution_manifest(self):
        m=re.search(r'^CAPTURE_GD_BYTES = (\d+)$',RUNNER,re.M)
        self.assertIsNotNone(m)
        self.assertEqual(int(m.group(1)),MANIFEST["capture_script_bytes"])

    def test_75_runner_capture_path_matches_execution_manifest(self):
        self.assertEqual(str(CAPTURE_GD_REL).replace("\\","/"),MANIFEST["capture_script_path"])

    def test_76_runner_capture_pin_is_rehashed_before_godot(self):
        self.assertLess(RUNNER.index('capture_gd=verify_file'),RUNNER.index('ONE_FRAME_GODOT_VIEWPORT_CAPTURE'))

    def test_77_installer_source_is_explicit_external_zip_member(self):
        self.assertTrue(INSTALLER_PATH is not None and INSTALLER_PATH.is_file(),"Set C11E_L2_INSTALLER_SOURCE to the extracted ZIP root installer")
        self.assertNotEqual(INSTALLER_PATH.resolve(),(ROOT/"INSTALL_C11E_E6_L2_DIRECT_RGB24_VISUAL_PROBE_V4.ps1").resolve())

    def test_78_test_suite_does_not_assume_installer_is_repository_destination(self):
        source=Path(__file__).read_text(encoding="utf-8")
        self.assertIn('C11E_L2_INSTALLER_SOURCE',source)
        self.assertIsNone(re.search(r'(?m)^INSTALLER\s*=\s*\(ROOT\s*/',source))

if __name__ == "__main__": unittest.main()
