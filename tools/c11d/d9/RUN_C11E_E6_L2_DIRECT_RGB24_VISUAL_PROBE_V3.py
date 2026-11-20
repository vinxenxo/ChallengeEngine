from __future__ import annotations
import argparse, hashlib, importlib.util, json, os, shutil, subprocess, sys, tempfile, time, uuid
from datetime import datetime, timezone
from pathlib import Path

C11C_SHA = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
C11C_BYTES = 796318
D48_SHA = "0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07"
D48_BYTES = 12996
CLOSURE_RECEIPT_SHA = "4763bf2e9b7e23ece40801407d615b80a58d84b91b33353c668d70d06502da4b"
QIMAGE_RECEIPT_SHA = "95819ea730283ded149faa490b21e0df392341366a853b3c0913318fb203d783"
QIMAGE_MODULE_SHA = "850054e6212f7e6f59be5550ec194df3d1a1ca69acb343c53b76803b007721e1"
GODOT_EXE = r"C:\Users\vinxe\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine.Mono_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.1-stable_mono_win64\godot.exe"
GODOT_SHA = "8ec33ba6a6a953226170cda2a56a58810f6617261a71d6bd6d6ba7cce5e7b79d"
GODOT_BYTES = 179589128
QIMAGE_REL = r"tools\c11d\d9\c11e_e6_option_c_native_qt_probe_v2\payload\tools\c11d\d9\c11e_e6_option_c_qimage_frame_compositor_v1.py"
CAPTURE_GD_REL = Path("tools/c11d/d9/c11e_e6_l2_direct_rgb24_visual_probe_v3/CaptureLoopFrame.gd")
D48_REL = Path("definitions/c11d/production/C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V2.json")
C11C_REL = Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")
CLOSURE_REL = Path("artifacts/tests/c11e/e6_loop_source_closure_v2/E6LOOPSRCV2_20261120T073829Z_F66E421D/C11E_E6_LOOP_SOURCE_CLOSURE_RECEIPT_V2.json")
QIMAGE_RECEIPT_REL = Path("artifacts/tests/c11e/e6_option_c_native_qt_probe_v2_7/E6OPTCQTV2_7_20261119T225516Z_6DCBCB1C/C11E_E6_OPTION_C_NATIVE_QT_PROBE_RECEIPT_V2_7.json")

SOURCE_PINS = [
    ("core/presentation/C11CVisualEditorialLayer.gd", "f8f718c067a4d7a088cc16f244cc40209e7183bec93e44d8cb66eb6dd404cf7d", 19047),
    ("core/presentation/C11CVisualTypography.gd", "9ee823a28cef721a26f66436b5b168d92f5b9d1597ed6e4e3f518debb0910633", 2211),
    ("core/presentation/components/TypographyLabel.gd", "d7c6ec47b33baec983a239dfe6218037d4126dc1532130c92d4202d56e6e8866", 1240),
    ("core/presentation/PresentationProfile.gd", "187b1cf8ab96b9031785a0f36b0054a60383c97cb3d81906c7d9bbcd373bef24", 8837),
    ("core/presentation/UnifiedSocialFrame.gd", "d80c07103f56a2abfe34be60547285e61b0d03b50a5ed93c3c72d4241f6585ba", 2087),
    ("core/presentation/UnifiedSocialFrame.tscn", "a89051019ab78bc35757acaa8b46a3b62526432bfa86582f07a66187e80e1b4b", 1471),
    ("tools/prototypes/c11c_common/C11CColorBoost.gd", "ea585997b03aba00a13c3cb87640a7c626081316b43306093265757dd09c6607", 478),
    ("tools/prototypes/c11c_common/C11CEditorialColors.gd", "46326fbd732d514b5bfa2d964b99bdd14f2933dd01ec65689749bf40fda32632", 1827),
    ("tools/prototypes/c11c_common/C11CHeaderAnimatorV2.gd", "44c4a9a11c334e6e84fcc1413667accac175781787866c3d6b894beeba3ea255", 9631),
    ("tools/prototypes/c11c_common/C11CPaletteBank.gd", "6b64d99afb148b0dc5b0f8e27b50558e9b77df4d2fdff98d52495d81d53fdd14", 16138),
    ("tools/prototypes/c11c_common/C11CTheme.gd", "7e73c62221ca8149a174b4633900b732b67047e0eddd20ee73e9d8f2f83cab64", 255),
    ("tools/prototypes/c11c_common/C11CVariationProfile.gd", "f7df994d8842183275bc331decd75762a153f3100248c7cc8b590e34c1347e2d", 13703),
    ("tools/prototypes/c11c_common/C11CVisualLoopDuration.gd", "4ea0b0decbd3a22ade42023e819a74872f312b63facc1163dc73a7c656fdbaf8", 1048),
    ("tools/prototypes/c11c_common/TechnobabbleGenerator.gd", "f2fbef4ee4b8b07d1b4ebe7781bc5d987e37c43a5f5eb317397a377288890c9f", 7054),
    ("tools/prototypes/c11c_fractal_bloom_v1/FractalBloom.gdshader", "38288d4342afa2196b0e40aad7eddbbc012fab7e7664499ce2b0c302f658ba7c", 10052),
    ("tools/prototypes/c11c_fractal_bloom_v1/FractalBloomPrototype.gd", "b596ecba5eeae80ba615d7cb8a741dffcab9db4c44296e660f4f9d6919cc5c55", 11196),
    ("tools/prototypes/c11c_fractal_bloom_v1/FractalBloomPrototype.tscn", "806bed600f7550e7aa5c10175359c7ce545581ce206dc73e31c7c265cc398d5e", 224),
    ("tools/prototypes/c11c_fractal_bloom_v1/FractalBloomRenderer.gd", "78102f64829bda24ae56d50b5ad16a69b8674569b22133509e335649f08861f7", 3478),
    ("assets/fonts/Inter-Bold.otf", "9fc6261e817d0b1b2bf1953d8799bb1c837d11aeebbf83ae352e7b4d6de6425d", 631880),
    ("assets/fonts/NotoSansMono-Regular.ttf", "6b692c4b6d15ccf59f1c1fe8d11cb8a92f51960f3e9f1f523781755a3af7e29f", 510612),
]

PROJECT_CONFIG = '''config_version=5\n\n[application]\nconfig/name="C11E_E6_L2_Direct_RGB24_Test_Only"\nconfig/features=PackedStringArray("4.7", "GL Compatibility")\n\n[display]\nwindow/size/viewport_width=540\nwindow/size/viewport_height=960\nwindow/size/window_width_override=540\nwindow/size/window_height_override=960\nwindow/stretch/mode="canvas_items"\n\n[rendering]\nrenderer/rendering_method="gl_compatibility"\nrenderer/rendering_method.mobile="gl_compatibility"\n'''
MAIN_SCENE = '''[gd_scene format=3]\n\n[node name="ProbeMain" type="Node"]\n'''


def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))

def verify_file(project_root: Path, rel: str, expected_sha: str, expected_bytes: int|None=None):
    p=project_root/Path(rel)
    if not p.is_file(): raise RuntimeError(f"PINNED_FILE_MISSING:{rel}")
    if expected_bytes is not None and p.stat().st_size != expected_bytes: raise RuntimeError(f"PINNED_FILE_BYTES_MISMATCH:{rel}")
    actual=sha256(p)
    if actual != expected_sha: raise RuntimeError(f"PINNED_FILE_SHA256_MISMATCH:{rel}:{actual}")
    return p

def import_qimage_module(path: Path):
    spec=importlib.util.spec_from_file_location("c11e_l2_pinned_qimage", path)
    if spec is None or spec.loader is None: raise RuntimeError("QIMAGE_MODULE_SPEC_FAILED")
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def copy_staging_tree(project_root: Path, stage_root: Path):
    for rel, digest, size in SOURCE_PINS:
        src=verify_file(project_root, rel, digest, size)
        dst=stage_root/Path(rel)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src,dst)
        if dst.stat().st_size != src.stat().st_size or sha256(dst) != digest:
            raise RuntimeError(f"STAGE_COPY_POSTIMAGE_MISMATCH:{rel}")
    gd_source=verify_file(project_root,str(CAPTURE_GD_REL).replace('\\','/'), CAPTURE_GD_SHA, CAPTURE_GD_BYTES)
    gd_dest=stage_root/CAPTURE_GD_REL
    gd_dest.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(gd_source,gd_dest)
    if sha256(gd_dest) != CAPTURE_GD_SHA: raise RuntimeError("CAPTURE_GDSCRIPT_STAGE_PIN_MISMATCH")
    (stage_root/"project.godot").write_text(PROJECT_CONFIG,encoding="utf-8",newline="\n")
    (stage_root/"ProbeMain.tscn").write_text(MAIN_SCENE,encoding="utf-8",newline="\n")

def validate_predecessor_receipt(path: Path, expected_sha: str, expected_status: str, sidecar_name: str):
    if not path.is_file(): raise RuntimeError(f"PREDECESSOR_RECEIPT_MISSING:{path}")
    if sha256(path) != expected_sha: raise RuntimeError(f"PREDECESSOR_RECEIPT_SHA_MISMATCH:{path}")
    side=Path(str(path)+".sha256")
    if not side.is_file(): raise RuntimeError(f"PREDECESSOR_SIDECAR_MISSING:{side}")
    text=side.read_text(encoding="ascii").strip()
    if text != f"{expected_sha}  {sidecar_name}": raise RuntimeError(f"PREDECESSOR_SIDECAR_MISMATCH:{side}")
    data=load_json(path)
    if data.get("status") != expected_status: raise RuntimeError(f"PREDECESSOR_STATUS_MISMATCH:{path}")
    return data

def run(project_root: Path, python_exe: Path):
    project_root=project_root.resolve()
    if not project_root.is_dir(): raise RuntimeError("PROJECT_ROOT_MISSING")
    if sys.version_info[:3] != (3,13,14): raise RuntimeError(f"PYTHON_VERSION_MISMATCH:{sys.version.split()[0]}")
    import PySide6
    if PySide6.__version__ != "6.11.2": raise RuntimeError(f"PYSIDE6_VERSION_MISMATCH:{PySide6.__version__}")
    c11c=verify_file(project_root,str(C11C_REL),C11C_SHA,C11C_BYTES)
    d48=verify_file(project_root,str(D48_REL),D48_SHA,D48_BYTES)
    for rel,digest,size in SOURCE_PINS: verify_file(project_root,rel,digest,size)
    qimage_path=verify_file(project_root,QIMAGE_REL,QIMAGE_MODULE_SHA)
    capture_gd=verify_file(project_root,str(CAPTURE_GD_REL).replace('\\','/'),CAPTURE_GD_SHA,CAPTURE_GD_BYTES)
    godot=Path(GODOT_EXE)
    if not godot.is_file() or godot.stat().st_size != GODOT_BYTES or sha256(godot) != GODOT_SHA:
        raise RuntimeError("PINNED_GODOT_EXECUTABLE_MISMATCH")
    closure=validate_predecessor_receipt(project_root/CLOSURE_REL,CLOSURE_RECEIPT_SHA,
        "PASS_LOOP_SOURCE_PROVENANCE_RECONCILED_WITH_COLORIMETRY_AND_VISUAL_REVIEW_PENDING",
        "C11E_E6_LOOP_SOURCE_CLOSURE_RECEIPT_V2.json")
    qimage_receipt=validate_predecessor_receipt(project_root/QIMAGE_RECEIPT_REL,QIMAGE_RECEIPT_SHA,
        "PASS_QIMAGE_STAGE_BENCHMARKED_NOT_END_TO_END",
        "C11E_E6_OPTION_C_NATIVE_QT_PROBE_RECEIPT_V2_7.json")
    qt_tests=qimage_receipt.get("qimage_tests",{})
    qt_bench=qimage_receipt.get("qimage_benchmark",{})
    if (not isinstance(qt_tests,dict) or qt_tests.get("run") is not True or qt_tests.get("tests") != 37
        or qt_tests.get("failures") != 0 or qt_tests.get("errors") != 0 or qt_tests.get("status") != "PASS"):
        raise RuntimeError("QIMAGE_PREDECESSOR_RECEIPT_SEMANTICS_MISMATCH")
    if (not isinstance(qt_bench,dict) or qt_bench.get("iterations") != 7
        or not isinstance(qt_bench.get("p95_ms"),(int,float)) or qt_bench.get("p95_ms") > 33.333
        or qt_bench.get("end_to_end_qualified") is not False):
        raise RuntimeError("QIMAGE_PREDECESSOR_BENCHMARK_SEMANTICS_MISMATCH")

    run_id="E6L2RGB24V3_"+datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ_")+uuid.uuid4().hex[:8].upper()
    artifact_root=project_root/"artifacts"/"tests"/"c11e"/"e6_l2_direct_rgb24_visual_probe_v3"/run_id
    if artifact_root.exists(): raise RuntimeError("RUN_DIRECTORY_COLLISION")
    artifact_root.mkdir(parents=True,exist_ok=False)
    stage_root=Path(tempfile.gettempdir())/("c11eL2_"+uuid.uuid4().hex[:8])
    if stage_root.exists(): raise RuntimeError("STAGE_DIRECTORY_COLLISION")
    stage_root.mkdir(parents=True,exist_ok=False)
    source_root=stage_root/"project"
    source_root.mkdir()
    process_rows=[]
    receipt={
        "schema":"C11E-E6-L2-DIRECT-RGB24-VISUAL-PROBE-RECEIPT-V3",
        "run_id":run_id,
        "created_utc":datetime.now(timezone.utc).isoformat(),
        "status":"BLOCKED_PREFLIGHT",
        "l2_ready":False,
        "scope":"ONE_TEST_ONLY_DIRECT_RECAPTURE_AND_QIMAGE_COMPOSITION_FIXED_SUBVIEWPORT",
        "selector":{"selector_id":"E6-L-01","family_id":"fractal_bloom","grammar_id":"radial_bloom","gameplay_seed":100006,"music_seed":500006,"frame_index":0},
        "source_origin":"C11C_SCENE_DIRECT_VIEWPORT_RECAPTURE_NOT_HISTORICAL_MP4_FRAME",
        "source_pins_verified":False,
        "predecessor_closure_receipt_sha256":CLOSURE_RECEIPT_SHA,
        "predecessor_qimage_receipt_sha256":QIMAGE_RECEIPT_SHA,
        "godot_executable_sha256":GODOT_SHA,
        "godot_executable_bytes":GODOT_BYTES,
        "godot_invocations":0,
        "godot_processes":process_rows,
        "historical_mp4_consumed":False,
        "colorimetry":{"primaries":"UNDECLARED","transfer":"UNDECLARED","matrix":"UNDECLARED","bt709_assumed":False,"yuv_to_rgb_conversion":False,"direct_rgba8_capture":True},
        "audio_generated":False,"ffmpeg_invoked":False,"ffprobe_invoked":False,"mux_invoked":False,
        "renderer_production":False,"production_dispatch":False,"e6_accepted":0,"release_authority":"NONE",
        "d4_8_v2_modified":False,"c11c_modified":False,"source_files_modified":False,
        "artifacts":{},
    }
    try:
        # Build a minimal, isolated Godot project from a strict, pinned transitive dependency closure.
        copy_staging_tree(project_root,source_root)
        receipt["source_pins_verified"]=True
        print("SOURCE_DEPENDENCY_PINS=PASS/"+str(len(SOURCE_PINS)))
        (artifact_root/"godot_stage_root.txt").write_text(str(source_root),encoding="utf-8")
        env=os.environ.copy()
        env.update({
            "C11C_SEED":"100006",
            "C11C_VISUAL_GRAMMAR":"radial_bloom",
            "C11C_SOUND_ENABLED":"0",
            "C11C_SHOW_FOOTER":"1",
            "C11C_AUTHORING_OUTPUT_PATH":str(artifact_root/"authoring_snapshot.json"),
            "C11E_L2_CAPTURE_ROOT":str(artifact_root),
        })
        log1=artifact_root/"godot_import.log"
        cmd1=[str(godot),"--headless","--editor","--path",str(source_root),"--import","--quit"]
        p1=subprocess.run(cmd1,cwd=str(source_root),env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding="utf-8",errors="replace",timeout=180)
        log1.write_text(p1.stdout,encoding="utf-8")
        process_rows.append({"purpose":"ISOLATED_TEST_PROJECT_IMPORT_AND_CLASS_SCAN","argv":cmd1[1:],"exit_code":p1.returncode,"log_sha256":sha256(log1)})
        receipt["godot_invocations"]+=1
        if p1.returncode != 0: raise RuntimeError(f"GODOT_IMPORT_FAILED:{p1.returncode}")
        import_errors = [line for line in p1.stdout.splitlines() if any(token in line for token in ("SCRIPT ERROR:", "Parse Error:", "Compile Error:", "Failed to load script"))]
        if import_errors: raise RuntimeError("GODOT_IMPORT_SCRIPT_ERRORS:" + " | ".join(import_errors[:8]))
        class_cache = source_root/".godot"/"global_script_class_cache.cfg"
        if not class_cache.is_file(): raise RuntimeError("GODOT_GLOBAL_SCRIPT_CLASS_CACHE_MISSING")
        class_cache_text = class_cache.read_text(encoding="utf-8",errors="replace")
        if "TypographyLabel" not in class_cache_text or "core/presentation/components/TypographyLabel.gd" not in class_cache_text:
            raise RuntimeError("TYPOGRAPHYLABEL_GLOBAL_CLASS_NOT_REGISTERED")
        print("GODOT_GLOBAL_CLASS=PASS/TypographyLabel")
        log2=artifact_root/"godot_capture.log"
        gd_script="res://"+str(CAPTURE_GD_REL).replace('\\','/')
        cmd2=[str(godot),"--path",str(source_root),"--script",gd_script]
        p2=subprocess.run(cmd2,cwd=str(source_root),env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding="utf-8",errors="replace",timeout=180)
        log2.write_text(p2.stdout,encoding="utf-8")
        process_rows.append({"purpose":"ONE_FRAME_GODOT_VIEWPORT_CAPTURE","argv":cmd2[1:],"exit_code":p2.returncode,"log_sha256":sha256(log2)})
        receipt["godot_invocations"]+=1
        if p2.returncode != 0: raise RuntimeError(f"GODOT_CAPTURE_FAILED:{p2.returncode}")
        capture_meta=load_json(artifact_root/"capture_metadata.json")
        if "C11E_L2_CAPTURE=PASS/ONE_FRAME" not in p2.stdout or "C11E_L2_CAPTURE=BLOCKED/" in p2.stdout:
            raise RuntimeError("GODOT_CAPTURE_LOG_MARKER_MISMATCH")
        if capture_meta.get("status") != "PASS_CAPTURED_ONE_DIRECT_RGB24_FRAME": raise RuntimeError("GODOT_CAPTURE_RECEIPT_STATUS_MISMATCH")
        exact_capture = {
            "selector_id":"E6-L-01", "family_id":"fractal_bloom", "grammar_id":"radial_bloom",
            "gameplay_seed":100006, "frame_index":0, "viewport_width":720, "viewport_height":1280,
            "viewport_source":"FIXED_SUBVIEWPORT_NO_WINDOW_DPI_DEPENDENCY",
            "source_image_format":"RGBA8", "source_rgba_bytes":3686400, "alpha_all_opaque":True,
            "rgb_pixel_format":"RGB24", "rgb_bytes":2764800, "rgb_stride_bytes":2160,
            "color_transform_applied":False, "historical_mp4_consumed":False
        }
        for key, expected in exact_capture.items():
            if capture_meta.get(key) != expected: raise RuntimeError(f"CAPTURE_METADATA_MISMATCH:{key}:{capture_meta.get(key)!r}")
        if capture_meta.get("rgb_sha256") != sha256(artifact_root/"source_frame.rgb24"): raise RuntimeError("CAPTURE_RGB24_SHA_MISMATCH")
        if capture_meta.get("alpha_all_opaque") is not True or capture_meta.get("color_transform_applied") is not False: raise RuntimeError("CAPTURE_ALPHA_OR_COLOR_TRANSFORM_CONTRACT_MISMATCH")
        if capture_meta.get("source_origin") != "C11C_SCENE_DIRECT_VIEWPORT_RECAPTURE_NOT_HISTORICAL_MP4_FRAME": raise RuntimeError("CAPTURE_SOURCE_ORIGIN_MISMATCH")
        source_bytes=(artifact_root/"source_frame.rgb24").read_bytes()
        if len(source_bytes)!=2764800: raise RuntimeError("SOURCE_RGB24_BYTES_INVALID")
        qimage_module=import_qimage_module(qimage_path)
        if getattr(qimage_module,"BACKEND",None) != "PYSIDE6_QIMAGE_CPP_SMOOTH_TRANSFORMATION_V1":
            raise RuntimeError("QIMAGE_BACKEND_PIN_MISMATCH")
        if not callable(getattr(qimage_module,"compose_rgb24_image",None)):
            raise RuntimeError("QIMAGE_COMPOSITOR_API_MISSING")
        composed=qimage_module.compose_rgb24_image(source_bytes,720,1280)
        if composed.isNull() or composed.width()!=720 or composed.height()!=1280: raise RuntimeError("QIMAGE_COMPOSED_GEOMETRY_INVALID")
        if composed.bytesPerLine()!=2160 or composed.sizeInBytes()!=2764800: raise RuntimeError("QIMAGE_COMPOSED_STRIDE_OR_SIZE_INVALID")
        composed_rgb=bytes(composed.constBits())
        if len(composed_rgb) != 2764800: raise RuntimeError("QIMAGE_OUTPUT_BUFFER_LENGTH_INVALID")
        (artifact_root/"composited_frame.rgb24").write_bytes(composed_rgb)
        output_png=artifact_root/"composited_frame.png"
        if not composed.save(str(output_png),"PNG"): raise RuntimeError("QIMAGE_COMPOSITED_PNG_SAVE_FAILED")
        # Preserve all source-file pins after the temporary project build and probe.
        for rel,digest,size in SOURCE_PINS: verify_file(project_root,rel,digest,size)
        verify_file(project_root,str(C11C_REL),C11C_SHA,C11C_BYTES)
        verify_file(project_root,str(D48_REL),D48_SHA,D48_BYTES)
        verify_file(project_root,QIMAGE_REL,QIMAGE_MODULE_SHA)
        required_artifacts = ["capture_metadata.json","source_frame.rgb24","source_frame.png","authoring_snapshot.json","godot_import.log","godot_capture.log","composited_frame.rgb24","composited_frame.png"]
        missing_artifacts=[name for name in required_artifacts if not (artifact_root/name).is_file()]
        if missing_artifacts: raise RuntimeError("EXPECTED_ARTIFACTS_MISSING:"+",".join(missing_artifacts))
        receipt.update({
            "status":"PASS_L2_ONE_FRAME_DIRECT_RGB24_COMPOSITION_PENDING_OPERATOR_VISUAL_REVIEW",
            "source_format":"RGBA8_OPAQUE_DIRECT_VIEWPORT_CAPTURE",
            "viewport_source":"FIXED_SUBVIEWPORT_720x1280_NO_WINDOW_DPI_DEPENDENCY",
            "source_rgb24_bytes":len(source_bytes),
            "source_rgb24_sha256":sha256(artifact_root/"source_frame.rgb24"),
            "source_preview_png_sha256":sha256(artifact_root/"source_frame.png"),
            "qimage_module_sha256":QIMAGE_MODULE_SHA,
            "qimage_backend":"PYSIDE6_QIMAGE_CPP_SMOOTH_TRANSFORMATION_V1",
            "pyside6_version":PySide6.__version__,
            "compositor_output_format":"RGB24",
            "compositor_output_width":720,
            "compositor_output_height":1280,
            "compositor_output_stride_bytes":2160,
            "compositor_output_bytes":len(composed_rgb),
            "compositor_output_rgb24_sha256":hashlib.sha256(composed_rgb).hexdigest(),
            "compositor_output_png_sha256":sha256(output_png),
            "geometry":{"canvas":"720x1280","content_rect":[108,192,504,896],"header_height":192,"footer_y":1088,"footer_height":192,"side_gutters":108,"body_black_bands":True},
            "visual_resampler_review":"PENDING_OPERATOR_VISUAL_REVIEW",
            "historical_mp4_consumed":False,
            "colorimetry":{"primaries":"UNDECLARED","transfer":"UNDECLARED","matrix":"UNDECLARED","bt709_assumed":False,"yuv_to_rgb_conversion":False,"direct_rgba8_capture":True,"qimage_pixel_operation":"RGB24 resampling; no matrix/transfer/primaries conversion asserted"},
            "godot_invocations":2,
            "godot_processes":process_rows,
            "l2_single_frame_probe":"PASS_TEST_ONLY_NOT_FAMILY_ACCEPTANCE",
            "l2_ready":False,
            "l3_negative_controls":"NOT_RUN",
            "l4_six_loop_selectors":"NOT_RUN",
            "smoke18":"NOT_AUTHORIZED_BY_THIS_MANIFEST",
            "artifacts":{name:{"bytes":(artifact_root/name).stat().st_size,"sha256":sha256(artifact_root/name)} for name in required_artifacts},
        })
    except Exception as exc:
        receipt["status"]="BLOCKED_L2_DIRECT_RGB24_VISUAL_PROBE"
        receipt["blocking_error"]=f"{type(exc).__name__}:{exc}"
        receipt["godot_invocations"]=len(process_rows)
        receipt["godot_processes"]=process_rows
        raise
    finally:
        # A test-only isolated staging tree is always removed; all authored evidence stays under the unique artifact run root.
        shutil.rmtree(stage_root,ignore_errors=True)
        receipt["completed_utc"]=datetime.now(timezone.utc).isoformat()
        receipt_path=artifact_root/"C11E_E6_L2_DIRECT_RGB24_VISUAL_PROBE_RECEIPT_V3.json"
        receipt_path.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
        receipt_sha=sha256(receipt_path)
        sidecar=artifact_root/(receipt_path.name+".sha256")
        sidecar.write_text(f"{receipt_sha}  {receipt_path.name}\n",encoding="ascii")
        print("L2_DIRECT_RGB24_VISUAL_PROBE_STATUS="+str(receipt.get("status")))
        print("GODOT_INVOCATIONS="+str(receipt.get("godot_invocations")))
        print("AUDIO=OFF; FFMPEG=OFF; FFPROBE=OFF; MUX=OFF")
        print("HISTORICAL_MP4_CONSUMED=FALSE; BT709_ASSUMED=FALSE")
        print("L2_READY=FALSE; RENDERER_PRODUCTION=OFF; MEDIA=OFF; E6_ACCEPTED=0; RELEASE_AUTHORITY=NONE")
        print("RECEIPT="+str(receipt_path))
        print("RECEIPT_SHA256="+receipt_sha)
        print("RECEIPT_SIDECAR="+str(sidecar))
    return 0

# The source harness is pinned separately by the package manifest.
CAPTURE_GD_SHA = "348bf590c175f40f313b099b38f876f2ef9083f29783c095dcfd6c44ccdf1d6d"
CAPTURE_GD_BYTES = 6640

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--project-root",required=True)
    parser.add_argument("--python-exe",required=True)
    args=parser.parse_args()
    python_exe=Path(args.python_exe)
    if not python_exe.is_file(): raise SystemExit("PYTHON_EXE_MISSING")
    if Path(sys.executable).resolve()!=python_exe.resolve(): raise SystemExit("RUNNER_PYTHON_EXECUTABLE_MISMATCH")
    return run(Path(args.project_root),python_exe)

if __name__=="__main__":
    raise SystemExit(main())
