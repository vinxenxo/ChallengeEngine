from __future__ import annotations
import argparse, hashlib, json, os, shutil, sys, uuid
from datetime import datetime, timezone
from pathlib import Path

from PySide6.QtGui import QImage

PROJECT_ROOT_BOOTSTRAP = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT_BOOTSTRAP) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT_BOOTSTRAP))

from tools.c11d.d9.c11e_e6_l2_qimage_import_v5 import load_module_registered

C11C_SHA = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
C11C_BYTES = 796318
D48_SHA = "0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07"
D48_BYTES = 12996
CLOSURE_SHA = "4763bf2e9b7e23ece40801407d615b80a58d84b91b33353c668d70d06502da4b"
QIMAGE_RECEIPT_SHA = "95819ea730283ded149faa490b21e0df392341366a853b3c0913318fb203d783"
QIMAGE_MODULE_SHA = "850054e6212f7e6f59be5550ec194df3d1a1ca69acb343c53b76803b007721e1"
V4_RECEIPT_SHA = "b36f319a3b7e3290be965dfc1bfa28fdff789b6054e89fc9c3cba182130aad88"
V4_INSTALL_RECEIPT_SHA = "2afb58e86cddfa6bea3c412071f3ba0ca882a95af8c8274382d478d34ef840eb"
CAPTURE_META_SHA = "aa37687434e714a15f1124282d81015f64e77a441b8a470ea1b98b80d2ad0679"
SOURCE_PNG_SHA = "39ae0a4df012faf1b2fd087443ccadf963bb59610affc2756c1732fa42669908"
SOURCE_RGB_SHA = "a0803353be7dca53a75903a1c863bd814a4367b534e698018d8ab434f5506d03"
IMPORT_LOG_SHA = "9f7ca4e42666d6b72bac0a8ebe2f557d0055fb440b90f2cba5e59c19053e8570"
CAPTURE_LOG_SHA = "f27be5cae4260dfbb0bbd4ad1efe799d9d2c2431480add1af97b6e99de708ed1"
QIMAGE_REL = Path("tools/c11d/d9/c11e_e6_option_c_native_qt_probe_v2/payload/tools/c11d/d9/c11e_e6_option_c_qimage_frame_compositor_v1.py")
C11C_REL = Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")
D48_REL = Path("definitions/c11d/production/C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V2.json")
CLOSURE_REL = Path("artifacts/tests/c11e/e6_loop_source_closure_v2/E6LOOPSRCV2_20261120T073829Z_F66E421D/C11E_E6_LOOP_SOURCE_CLOSURE_RECEIPT_V2.json")
QIMAGE_RECEIPT_REL = Path("artifacts/tests/c11e/e6_option_c_native_qt_probe_v2_7/E6OPTCQTV2_7_20261119T225516Z_6DCBCB1C/C11E_E6_OPTION_C_NATIVE_QT_PROBE_RECEIPT_V2_7.json")
V4_ROOT_REL = Path("artifacts/tests/c11e/e6_l2_direct_rgb24_visual_probe_v4/E6L2RGB24V4_20261120T095847Z_A8AA1CA7")
V4_INSTALL_ROOT_REL = Path("artifacts/tests/c11e/e6_l2_direct_rgb24_visual_probe_v4_install/E6L2RGB24V4INST_20261120T095822Z_76051BF3")
V4_RECEIPT_NAME = "C11E_E6_L2_DIRECT_RGB24_VISUAL_PROBE_RECEIPT_V4.json"
V4_INSTALL_RECEIPT_NAME = "C11E_E6_L2_DIRECT_RGB24_VISUAL_PROBE_V3_INSTALL_RECEIPT.json"

SOURCE_PINS = [('assets/fonts/Inter-Bold.otf', '9fc6261e817d0b1b2bf1953d8799bb1c837d11aeebbf83ae352e7b4d6de6425d', 631880), ('assets/fonts/NotoSansMono-Regular.ttf', '6b692c4b6d15ccf59f1c1fe8d11cb8a92f51960f3e9f1f523781755a3af7e29f', 510612), ('core/presentation/C11CVisualEditorialLayer.gd', 'f8f718c067a4d7a088cc16f244cc40209e7183bec93e44d8cb66eb6dd404cf7d', 19047), ('core/presentation/C11CVisualTypography.gd', '9ee823a28cef721a26f66436b5b168d92f5b9d1597ed6e4e3f518debb0910633', 2211), ('core/presentation/PresentationProfile.gd', '187b1cf8ab96b9031785a0f36b0054a60383c97cb3d81906c7d9bbcd373bef24', 8837), ('core/presentation/UnifiedSocialFrame.gd', 'd80c07103f56a2abfe34be60547285e61b0d03b50a5ed93c3c72d4241f6585ba', 2087), ('core/presentation/UnifiedSocialFrame.tscn', 'a89051019ab78bc35757acaa8b46a3b62526432bfa86582f07a66187e80e1b4b', 1471), ('core/presentation/components/TypographyLabel.gd', 'd7c6ec47b33baec983a239dfe6218037d4126dc1532130c92d4202d56e6e8866', 1240), ('tools/prototypes/c11c_common/C11CColorBoost.gd', 'ea585997b03aba00a13c3cb87640a7c626081316b43306093265757dd09c6607', 478), ('tools/prototypes/c11c_common/C11CEditorialColors.gd', '46326fbd732d514b5bfa2d964b99bdd14f2933dd01ec65689749bf40fda32632', 1827), ('tools/prototypes/c11c_common/C11CHeaderAnimatorV2.gd', '44c4a9a11c334e6e84fcc1413667accac175781787866c3d6b894beeba3ea255', 9631), ('tools/prototypes/c11c_common/C11CPaletteBank.gd', '6b64d99afb148b0dc5b0f8e27b50558e9b77df4d2fdff98d52495d81d53fdd14', 16138), ('tools/prototypes/c11c_common/C11CTheme.gd', '7e73c62221ca8149a174b4633900b732b67047e0eddd20ee73e9d8f2f83cab64', 255), ('tools/prototypes/c11c_common/C11CVariationProfile.gd', 'f7df994d8842183275bc331decd75762a153f3100248c7cc8b590e34c1347e2d', 13703), ('tools/prototypes/c11c_common/C11CVisualLoopDuration.gd', '4ea0b0decbd3a22ade42023e819a74872f312b63facc1163dc73a7c656fdbaf8', 1048), ('tools/prototypes/c11c_common/TechnobabbleGenerator.gd', 'f2fbef4ee4b8b07d1b4ebe7781bc5d987e37c43a5f5eb317397a377288890c9f', 7054), ('tools/prototypes/c11c_fractal_bloom_v1/FractalBloom.gdshader', '38288d4342afa2196b0e40aad7eddbbc012fab7e7664499ce2b0c302f658ba7c', 10052), ('tools/prototypes/c11c_fractal_bloom_v1/FractalBloomPrototype.gd', 'b596ecba5eeae80ba615d7cb8a741dffcab9db4c44296e660f4f9d6919cc5c55', 11196), ('tools/prototypes/c11c_fractal_bloom_v1/FractalBloomPrototype.tscn', '806bed600f7550e7aa5c10175359c7ce545581ce206dc73e31c7c265cc398d5e', 224), ('tools/prototypes/c11c_fractal_bloom_v1/FractalBloomRenderer.gd', '78102f64829bda24ae56d50b5ad16a69b8674569b22133509e335649f08861f7', 3478)]


def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def verify_file(path: Path, expected_sha: str, expected_bytes: int|None=None):
    if not path.is_file(): raise RuntimeError(f"PINNED_FILE_MISSING:{path}")
    if expected_bytes is not None and path.stat().st_size != expected_bytes:
        raise RuntimeError(f"PINNED_FILE_BYTES_MISMATCH:{path}:{path.stat().st_size}")
    actual=sha256(path)
    if actual != expected_sha: raise RuntimeError(f"PINNED_FILE_SHA256_MISMATCH:{path}:{actual}")
    return path

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))

def require_sidecar(path: Path, digest: str):
    side=Path(str(path)+".sha256")
    expected=f"{digest}  {path.name}"
    if not side.is_file() or side.read_text(encoding="ascii").strip()!=expected:
        raise RuntimeError(f"SIDECAR_MISMATCH:{side}")
    return side

def verify_v4_evidence(project_root: Path):
    v4=project_root/V4_ROOT_REL
    receipt=verify_file(v4/V4_RECEIPT_NAME,V4_RECEIPT_SHA,2621)
    side=require_sidecar(receipt,V4_RECEIPT_SHA)
    data=load_json(receipt)
    if data.get("status")!="BLOCKED_L2_DIRECT_RGB24_VISUAL_PROBE":
        raise RuntimeError("V4_RECEIPT_STATUS_UNEXPECTED")
    if data.get("blocking_error")!="AttributeError:'NoneType' object has no attribute '__dict__'":
        raise RuntimeError("V4_FAILURE_SIGNATURE_MISMATCH")
    if data.get("source_pins_verified") is not True or data.get("l2_ready") is not False:
        raise RuntimeError("V4_RECEIPT_SOURCE_OR_GOVERNANCE_MISMATCH")
    procs=data.get("godot_processes",[])
    if len(procs)!=2 or data.get("godot_invocations")!=2:
        raise RuntimeError("V4_GODOT_PROCESS_CARDINALITY_MISMATCH")
    if [p.get("purpose") for p in procs] != ["ISOLATED_TEST_PROJECT_IMPORT_AND_CLASS_SCAN","ONE_FRAME_GODOT_VIEWPORT_CAPTURE"]:
        raise RuntimeError("V4_GODOT_PROCESS_PURPOSE_MISMATCH")
    if any(p.get("exit_code")!=0 for p in procs): raise RuntimeError("V4_GODOT_PROCESS_NOT_PASS")
    meta=verify_file(v4/"capture_metadata.json",CAPTURE_META_SHA,1144)
    metadata=load_json(meta)
    exact={
      "status":"PASS_CAPTURED_ONE_DIRECT_RGB24_FRAME","selector_id":"E6-L-01",
      "family_id":"fractal_bloom","grammar_id":"radial_bloom","gameplay_seed":100006,
      "frame_index":0,"viewport_width":720,"viewport_height":1280,
      "viewport_source":"FIXED_SUBVIEWPORT_NO_WINDOW_DPI_DEPENDENCY",
      "source_image_format":"RGBA8","source_rgba_bytes":3686400,"alpha_all_opaque":True,
      "rgb_pixel_format":"RGB24","rgb_bytes":2764800,"rgb_stride_bytes":2160,
      "rgb_sha256":SOURCE_RGB_SHA,"color_transform_applied":False,
      "historical_mp4_consumed":False,"audio_generated":False,"ffmpeg_invoked":False,
      "ffprobe_invoked":False,"mux_invoked":False,
    }
    for k,v in exact.items():
        if metadata.get(k)!=v: raise RuntimeError(f"V4_CAPTURE_METADATA_MISMATCH:{k}:{metadata.get(k)!r}")
    rgb=verify_file(v4/"source_frame.rgb24",SOURCE_RGB_SHA,2764800)
    png=verify_file(v4/"source_frame.png",SOURCE_PNG_SHA)
    import_log=verify_file(v4/"godot_import.log",IMPORT_LOG_SHA)
    capture_log=verify_file(v4/"godot_capture.log",CAPTURE_LOG_SHA)
    if procs[0].get("log_sha256")!=IMPORT_LOG_SHA or procs[1].get("log_sha256")!=CAPTURE_LOG_SHA:
        raise RuntimeError("V4_LOG_RECEIPT_HASH_LINK_MISMATCH")
    if "TypographyLabel" not in import_log.read_text(encoding="utf-8",errors="replace"):
        raise RuntimeError("V4_TYPOGRAPHYLABEL_CLASS_REGISTRATION_MISSING")
    cap_text=capture_log.read_text(encoding="utf-8",errors="replace")
    if "C11E_L2_CAPTURE=PASS/ONE_FRAME" not in cap_text:
        raise RuntimeError("V4_CAPTURE_PASS_MARKER_MISSING")
    install_root=project_root/V4_INSTALL_ROOT_REL
    install_receipt=verify_file(install_root/V4_INSTALL_RECEIPT_NAME,V4_INSTALL_RECEIPT_SHA,11308)
    require_sidecar(install_receipt,V4_INSTALL_RECEIPT_SHA)
    install_data=load_json(install_receipt)
    if install_data.get("status")!="PASS_ADD_ONLY" or install_data.get("destination_count")!=24 or install_data.get("add_count")!=24:
        raise RuntimeError("V4_INSTALL_RECEIPT_SEMANTICS_MISMATCH")
    return {"v4_root":v4,"receipt":receipt,"sidecar":side,"metadata":meta,"rgb":rgb,"png":png,
            "import_log":import_log,"capture_log":capture_log,"install_receipt":install_receipt,
            "install_sidecar":Path(str(install_receipt)+".sha256"),"metadata_json":metadata}

def atomic_write(path: Path, payload: bytes):
    tmp=path.parent/("."+path.stem+"."+uuid.uuid4().hex[:8]+".tmp")
    try:
        with tmp.open("xb") as f:
            f.write(payload); f.flush(); os.fsync(f.fileno())
        os.replace(tmp,path)
    finally:
        if tmp.exists(): tmp.unlink()

def run(project_root: Path):
    project_root=project_root.resolve()
    if not project_root.is_dir(): raise RuntimeError("PROJECT_ROOT_MISSING")
    if sys.version_info[:3]!=(3,13,14): raise RuntimeError(f"PYTHON_VERSION_MISMATCH:{sys.version.split()[0]}")
    import PySide6
    if PySide6.__version__!="6.11.2": raise RuntimeError(f"PYSIDE6_VERSION_MISMATCH:{PySide6.__version__}")
    c11c=verify_file(project_root/C11C_REL,C11C_SHA,C11C_BYTES)
    d48=verify_file(project_root/D48_REL,D48_SHA,D48_BYTES)
    for rel,digest,size in SOURCE_PINS:
        verify_file(project_root/Path(rel),digest,size)
    qimage_path=verify_file(project_root/QIMAGE_REL,QIMAGE_MODULE_SHA,6483)
    closure=verify_file(project_root/CLOSURE_REL,CLOSURE_SHA)
    qimage_receipt=verify_file(project_root/QIMAGE_RECEIPT_REL,QIMAGE_RECEIPT_SHA)
    closure_data=load_json(closure); qrec=load_json(qimage_receipt)
    if closure_data.get("status")!="PASS_LOOP_SOURCE_PROVENANCE_RECONCILED_WITH_COLORIMETRY_AND_VISUAL_REVIEW_PENDING":
        raise RuntimeError("LOOP_SOURCE_CLOSURE_PREDECESSOR_STATUS_MISMATCH")
    if qrec.get("status")!="PASS_QIMAGE_STAGE_BENCHMARKED_NOT_END_TO_END":
        raise RuntimeError("QIMAGE_V2_7_PREDECESSOR_STATUS_MISMATCH")
    v4=verify_v4_evidence(project_root)

    run_id="E6L2QIMGV5_"+datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ_")+uuid.uuid4().hex[:8].upper()
    artifact_root=project_root/"artifacts/tests/c11e/e6_l2_direct_rgb24_qimage_composition_v5"/run_id
    if artifact_root.exists(): raise RuntimeError("RUN_DIRECTORY_COLLISION")
    artifact_root.mkdir(parents=True,exist_ok=False)
    receipt={
      "schema":"C11E-E6-L2-QIMAGE-COMPOSITION-REPAIR-RECEIPT-V5","run_id":run_id,
      "created_utc":datetime.now(timezone.utc).isoformat(),
      "status":"BLOCKED_QIMAGE_COMPOSITION_REPAIR_V5","l2_ready":False,
      "scope":"ONE_QIMAGE_COMPOSITION_FROM_ALREADY_CAPTURED_V4_RGB24_EVIDENCE_NO_NEW_GODOT",
      "source_capture_run_id":"E6L2RGB24V4_20261120T095847Z_A8AA1CA7",
      "source_capture_receipt_sha256":V4_RECEIPT_SHA,"source_rgb24_sha256":SOURCE_RGB_SHA,
      "source_frame_png_sha256":SOURCE_PNG_SHA,"qimage_module_sha256":QIMAGE_MODULE_SHA,
      "python_version":sys.version.split()[0],"pyside6_version":PySide6.__version__,
      "godot_invocations":0,"audio_generated":False,"ffmpeg_invoked":False,"ffprobe_invoked":False,"mux_invoked":False,
      "historical_mp4_consumed":False,"bt709_assumed":False,"color_transform_applied":False,
      "renderer_production":False,"production_dispatch":False,"e6_accepted":0,"release_authority":"NONE",
      "c11c_modified":False,"d4_8_v2_modified":False,"source_files_modified":False,
      "visual_resampler_review":"PENDING_OPERATOR_VISUAL_REVIEW","artifacts":{}
    }
    try:
        # Preserve immutable copies of the exact predecessor source and logs in this new evidence folder.
        copy_names=[V4_RECEIPT_NAME,V4_RECEIPT_NAME+".sha256","capture_metadata.json","source_frame.png","source_frame.rgb24",
                    "authoring_snapshot.json","godot_import.log","godot_capture.log"]
        copied={}
        for name in copy_names:
            src=v4["v4_root"]/name
            if not src.is_file(): raise RuntimeError(f"V4_SOURCE_ARTIFACT_MISSING:{name}")
            dst=artifact_root/name
            shutil.copyfile(src,dst)
            if sha256(dst)!=sha256(src): raise RuntimeError(f"V4_SOURCE_COPY_HASH_MISMATCH:{name}")
            copied[name]=dst
        shutil.copyfile(v4["install_receipt"],artifact_root/v4["install_receipt"].name)
        shutil.copyfile(v4["install_sidecar"],artifact_root/v4["install_sidecar"].name)

        source_bytes=(artifact_root/"source_frame.rgb24").read_bytes()
        if len(source_bytes)!=2764800 or hashlib.sha256(source_bytes).hexdigest()!=SOURCE_RGB_SHA:
            raise RuntimeError("V4_RGB24_BUFFER_REVALIDATION_FAILED")
        source_png=QImage(str(artifact_root/"source_frame.png"))
        if source_png.isNull() or (source_png.width(),source_png.height())!=(720,1280):
            raise RuntimeError("V4_SOURCE_PNG_DECODE_OR_GEOMETRY_FAILED")
        png_rgb=source_png.convertToFormat(QImage.Format.Format_RGB888)
        if png_rgb.isNull() or png_rgb.bytesPerLine()!=2160 or bytes(png_rgb.constBits())!=source_bytes:
            raise RuntimeError("V4_SOURCE_PNG_RGB24_DOES_NOT_MATCH_CAPTURE_BUFFER")
        print("V4_CAPTURE_EVIDENCE=PASS/REUSED_NO_GODOT")
        print("SOURCE_RGB24=PASS/2764800_BYTES_SHA_MATCH")

        qimage_module=load_module_registered(qimage_path,"c11e_l2_pinned_qimage_v5")
        if sys.modules.get("c11e_l2_pinned_qimage_v5") is not qimage_module:
            raise RuntimeError("QIMAGE_MODULE_SYS_MODULE_REGISTRATION_MISSING")
        if getattr(qimage_module,"BACKEND",None)!="PYSIDE6_QIMAGE_CPP_SMOOTH_TRANSFORMATION_V1":
            raise RuntimeError("QIMAGE_BACKEND_PIN_MISMATCH")
        if not callable(getattr(qimage_module,"compose_rgb24_image",None)):
            raise RuntimeError("QIMAGE_COMPOSITOR_API_MISSING")

        # Exactly one QImage composition. This consumes the immutable V4 RGB24 buffer.
        composed=qimage_module.compose_rgb24_image(source_bytes,720,1280)
        if composed.isNull() or (composed.width(),composed.height())!=(720,1280):
            raise RuntimeError("QIMAGE_COMPOSED_GEOMETRY_INVALID")
        if composed.format()!=QImage.Format.Format_RGB888 or composed.bytesPerLine()!=2160 or composed.sizeInBytes()!=2764800:
            raise RuntimeError("QIMAGE_COMPOSED_PIXEL_CONTRACT_INVALID")
        if composed.pixelColor(360,80).getRgb()[:3]!=(0,0,0): raise RuntimeError("QIMAGE_HEADER_BAND_NOT_BLACK")
        if composed.pixelColor(360,1200).getRgb()[:3]!=(0,0,0): raise RuntimeError("QIMAGE_FOOTER_BAND_NOT_BLACK")
        if composed.pixelColor(40,640).getRgb()[:3]!=(0,0,0): raise RuntimeError("QIMAGE_LEFT_GUTTER_NOT_BLACK")
        if composed.pixelColor(680,640).getRgb()[:3]!=(0,0,0): raise RuntimeError("QIMAGE_RIGHT_GUTTER_NOT_BLACK")
        composed_rgb=bytes(composed.constBits())
        if len(composed_rgb)!=2764800: raise RuntimeError("QIMAGE_OUTPUT_BUFFER_LENGTH_INVALID")
        atomic_write(artifact_root/"composited_frame.rgb24",composed_rgb)
        png_tmp=artifact_root/".composited_frame.tmp.png"
        if not composed.save(str(png_tmp),"PNG"): raise RuntimeError("QIMAGE_COMPOSITED_PNG_SAVE_FAILED")
        os.replace(png_tmp,artifact_root/"composited_frame.png")
        saved_png=QImage(str(artifact_root/"composited_frame.png"))
        saved_rgb=saved_png.convertToFormat(QImage.Format.Format_RGB888)
        if saved_png.isNull() or (saved_png.width(),saved_png.height())!=(720,1280) or bytes(saved_rgb.constBits())!=composed_rgb:
            raise RuntimeError("QIMAGE_SAVED_PNG_PIXEL_POSTIMAGE_MISMATCH")

        # Recheck all source pins after composition; no source or predecessor writes.
        for rel,digest,size in SOURCE_PINS: verify_file(project_root/Path(rel),digest,size)
        verify_file(project_root/C11C_REL,C11C_SHA,C11C_BYTES)
        verify_file(project_root/D48_REL,D48_SHA,D48_BYTES)
        verify_file(project_root/QIMAGE_REL,QIMAGE_MODULE_SHA,6483)
        required=["source_frame.png","source_frame.rgb24","capture_metadata.json","godot_import.log","godot_capture.log",
                  "C11E_E6_L2_DIRECT_RGB24_VISUAL_PROBE_RECEIPT_V4.json","C11E_E6_L2_DIRECT_RGB24_VISUAL_PROBE_RECEIPT_V4.json.sha256",
                  "composited_frame.png","composited_frame.rgb24"]
        missing=[n for n in required if not (artifact_root/n).is_file()]
        if missing: raise RuntimeError("EXPECTED_ARTIFACTS_MISSING:"+",".join(missing))
        receipt.update({
          "status":"PASS_L2_QIMAGE_COMPOSITION_FROM_V4_CAPTURE_PENDING_OPERATOR_VISUAL_REVIEW",
          "qimage_module_import":"PASS_SYS_MODULE_REGISTERED_BEFORE_EXEC_MODULE",
          "qimage_composition_count":1,"godot_invocations":0,
          "compositor_backend":qimage_module.BACKEND,"compositor_output_format":"RGB24",
          "compositor_output_width":720,"compositor_output_height":1280,"compositor_output_stride_bytes":2160,
          "compositor_output_bytes":len(composed_rgb),"compositor_output_rgb24_sha256":hashlib.sha256(composed_rgb).hexdigest(),
          "compositor_output_png_sha256":sha256(artifact_root/"composited_frame.png"),
          "geometry":{"canvas":"720x1280","content_rect":[108,192,504,896],"header_height":192,"footer_y":1088,"footer_height":192,"side_gutters":108,"body_black_bands":True},
          "colorimetry":{"primaries":"UNDECLARED","transfer":"UNDECLARED","matrix":"UNDECLARED","bt709_assumed":False,"color_transform_applied":False,"operation":"QImage RGB24 resampling only"},
          "l2_probe":"PASS_TEST_ONLY_FROM_PRIOR_CAPTURE_NOT_FAMILY_ACCEPTANCE","l2_ready":False,
          "l3_negative_controls":"NOT_RUN","l4_six_loop_selectors":"NOT_RUN","smoke18":"NOT_AUTHORIZED_BY_THIS_MANIFEST",
          "artifacts":{name:{"bytes":(artifact_root/name).stat().st_size,"sha256":sha256(artifact_root/name)} for name in required}
        })
        print("QIMAGE_IMPORT=PASS/SYS_MODULE_REGISTERED_BEFORE_EXEC_MODULE")
        print("QIMAGE_COMPOSITION=PASS/1")
        print("QIMAGE_OUTPUT=720x1280_RGB24; BYTES=2764800; STRIDE=2160")
    except Exception as exc:
        receipt["status"]="BLOCKED_QIMAGE_COMPOSITION_REPAIR_V5"
        receipt["blocking_error"]=f"{type(exc).__name__}:{exc}"
        raise
    finally:
        receipt["completed_utc"]=datetime.now(timezone.utc).isoformat()
        recpath=artifact_root/"C11E_E6_L2_QIMAGE_COMPOSITION_RECEIPT_V5.json"
        payload=(json.dumps(receipt,indent=2,ensure_ascii=False)+"\n").encode("utf-8")
        atomic_write(recpath,payload)
        recsha=sha256(recpath)
        atomic_write(Path(str(recpath)+".sha256"),f"{recsha}  {recpath.name}\n".encode("ascii"))
        print("L2_QIMAGE_COMPOSITION_STATUS="+receipt["status"])
        print("GODOT_INVOCATIONS=0; V4_CAPTURE_REUSED=TRUE")
        print("AUDIO=OFF; FFMPEG=OFF; FFPROBE=OFF; MUX=OFF")
        print("L2_READY=FALSE; VISUAL_REVIEW=PENDING; E6_ACCEPTED=0; RELEASE_AUTHORITY=NONE")
        print("RECEIPT="+str(recpath)); print("RECEIPT_SHA256="+recsha)
    return 0

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--project-root",required=True)
    p.add_argument("--python-exe",required=True)
    a=p.parse_args()
    if Path(sys.executable).resolve()!=Path(a.python_exe).resolve(): raise SystemExit("RUNNER_PYTHON_EXECUTABLE_MISMATCH")
    return run(Path(a.project_root))

if __name__=="__main__": raise SystemExit(main())
