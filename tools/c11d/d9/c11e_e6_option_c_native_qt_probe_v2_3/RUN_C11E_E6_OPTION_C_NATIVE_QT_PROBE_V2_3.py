from __future__ import annotations
import argparse, binascii, hashlib, importlib.util, json, os, platform, re, statistics, struct, sys, time, unittest, uuid, zipfile
from datetime import datetime, timezone
from pathlib import Path

EXPECTED_PYTHON = (3,13,14)
EXPECTED_PYSIDE6 = "6.11.2"
C11C_SHA = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
C11C_BYTES = 796318
D4_8_SHA = "0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07"
D4_8_BYTES = 12996
OPTIONC_PY_SHA = "2c91a5539b02e492620ffd0ec5b45fbbf7953f4627ed060fe4cf7e46501e8093"
OPTIONC_PY_BYTES = 7795
INSTALL_RECEIPT_SHA = "f15f6b0dd58f992ef7be4d3af86fdae48fbdeca5db2d42e4cc68c91f08a33adb"
BENCH_RECEIPT_SHA = "de759af6ec2eed1cd7ef76c92df0b95ba65f024325ce05d1688d205210fb949a"
BENCH_ZIP_SHA = "f3c432f8faac86aee7b95533d7d85cdd2feb7868b12fbfcf4d6b6cac7c416dad"
LOOP_V2_SHA = "5afc42ca84480ba1d025d288f2653d009e85af053fff5b62133e067a17dfb4be"
A3_DIAG_SHA = "6a49a65b4658b119e9ed331f50296449ddb3ba248937c09eab30a3f3fc32bd4a"
BRIDGE_SHA = "fe9d40052b0f4ff6f1c862c010ae7b3b13070b6ce935be6d62f9dcaec63a644a"
ADAPTER_SHA = "222742677cd498368429a3ec0dcdd922c44197bb5ada3638081138fb77c31bf1"
FAMILY_STAGE_SHA = "bfbfa0cc108f00b78003e5480c86af1ee5ca63772d24a7792f8cdb6953b6af5d"
RESOLVER_SHA = "dac95fb698b52f96432a517d8ec3196a397e5e6bd3c025300350dd55ddce3afd"
E1_SERVICE_SHA = "e5dbf9baa72d4c066ff8ba24006df954700d72a5b0f11f9f88aec653e84dce87"
BOUNDARY_SHA = "795be1da157dd07fd4992d3ec6d7cf091a015eed72d16d86df13085db296098b"
DECISION_SHA = "22cec26baecfb6018a814750cc781143f5fa13f897d3dce708f6e9e074f669ac"
GEOMETRY_DECISION_SHA = "ae21ab52827a58404dbc4e96c041de54578089cb558895028a97715bc544f6b8"
A3_ADJUDICATOR_V3_SHA = "2094769bba1993f26ca40f36a1070e871d06e0c9b01443d4a3a846136a07e5b7"

REL = {
    "c11c_manifest": ("release/C11C_FREEZE_PACKAGE_MANIFEST.json", C11C_SHA, C11C_BYTES),
    "d4_8_v2": ("definitions/c11d/production/C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V2.json", D4_8_SHA, D4_8_BYTES),
    "option_c_python_reference": ("tools/c11d/d9/c11e_e6_loop_option_c_frame_compositor_v3.py", OPTIONC_PY_SHA, OPTIONC_PY_BYTES),
    "d9_bridge": ("tools/c11d/d9/editorial_render_bridge.py", BRIDGE_SHA, 10868),
    "d9_adapter": ("tools/c11d/d9/d_render_adapter.py", ADAPTER_SHA, 15051),
    "d9_loop_family_stage": ("tools/c11d/d9/c11e_e4b_loop_family_stage_contract.py", FAMILY_STAGE_SHA, 19331),
    "d9_resolver": ("tools/c11d/d9/universal_editorial_model.py", RESOLVER_SHA, 27585),
    "e1_service": ("c11c-suite/c11c-producer/c11e_production_service.py", E1_SERVICE_SHA, 86687),
    "option_c_boundary_v1": ("definitions/c11d/production/C11E_OPTION_C_D_POSTCOMPOSITION_BOUNDARY_V1.json", BOUNDARY_SHA, 3576),
    "option_c_decision_v1": ("definitions/c11d/production/C11E_OPTION_C_D_POSTCOMPOSITION_DECISION_V1.json", DECISION_SHA, 2342),
    "geometry_decision_v3": ("docs/history/c11e/overlays/C11E_E6_OPTION_C_COMPOSITOR_V4_20261119_2040Z/C11E_E6_LOOP_OPTION_C_GEOMETRY_DECISION_V3.json", GEOMETRY_DECISION_SHA, 2920),
    "a3_bridge": ("docs/current/e/C11E_E4C_A3_REVIEW_MANIFEST_LINEAGE_RECONCILIATION_20261110_V2.json", "aec0e387f167f4b821b7d94f06a67f78f498be939fe3cda857d20ce550819cac", 4770),
    "a3_historical_manifest": ("docs/history/c11e/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1_PRE_D98_LINEAGE_REFRESH_20261106.json", "2075da9c33c689861a68d3bd8fb19b7ed593c6e76010ab200880746aa6d1a470", 8591),
    "a3_current_manifest": ("definitions/c11d/production/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1.json", "5702092bc1c88e4b333dd30cc150f0d383cd2006121037b0198905c75a3af795", 8591),
    "a3_d98_model": ("definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json", "dabb458fc2215156ddb5ebea7e8ebec811098886ce2858733ba9fb13f6075ccb", 12932),
    "e4b_operator_decision": ("docs/current/e/C11E_E4B_OPERATOR_POLICY_DECISION_RECORD_20261106_V1.json", "49efd5494f351f09d7597c4699e9c12e361b36884b6bfadacd822e6ff1480e04", 3737),
    "smoke18_reuse_requalification": ("artifacts/tests/c11e/e6_smoke18_reuse_requalification/E6SMK18REQUAL_20261119T141719Z_A5555D34/E6_SMOKE18_REUSE_REQUALIFICATION_RECEIPT_V1.json", "2071d276429fa102c080018ee1421f5397cc3c5be74a7b0451e2ccad2ced494d", None),
    "option_c_v4_install_receipt": ("artifacts/tests/c11e/e6_loop_option_c_frame_compositor_install_v4/E6OPTCINSTALLV4_20261119T201123Z_429B16C0/C11E_E6_LOOP_OPTION_C_FRAME_COMPOSITOR_INSTALL_RECEIPT_V4.json", INSTALL_RECEIPT_SHA, None),
    "benchmark_receipt": ("artifacts/tests/c11e/e6_option_c_target_benchmark/E6OPTCBENCH_20261119T202929Z_FDA0D2B8/C11E_E6_OPTION_C_TARGET_BENCHMARK_RECEIPT_V1.json", BENCH_RECEIPT_SHA, 4242),
    "loop_policy_v2_receipt": ("artifacts/tests/c11e/e6_loop_policy_pin_reconciliation_v2/E6LOOPPOLICYV2_20261119T184655Z_9466C358/E6_LOOP_POLICY_PIN_RECONCILIATION_RECEIPT_V2.json", LOOP_V2_SHA, None),
    "a3_diagnostic_v1": ("artifacts/tests/c11e/e6_smoke18_continuation_diagnostic/E6SMK18DIAG_20261119T191211Z_861BF8D4/C11E_E6_SMOKE18_CONTINUATION_A3_DIAGNOSTIC_V1.json", A3_DIAG_SHA, None),
}

BENCH_PNGS = {
    "OPTION_C_color_bars_registration.png": "49750125370d2a619e37da6271161692d1300fe5c1391b75048bad7df89faaa3",
    "OPTION_C_smooth_rgb_gradient.png": "74af7630fefe0f1e5d7b4a490fcf6860c9bddf194be6cc2e515d0c83da569023",
    "OPTION_C_one_pixel_checkerboard.png": "bd461ec410472a5d609091ba55e728739dab7ad93af36601d56de4c2d6027391",
}

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""): h.update(block)
    return h.hexdigest()

def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def png_contract(data: bytes) -> dict:
    sig=b"\x89PNG\r\n\x1a\n"
    if not data.startswith(sig): raise ValueError("PNG_SIGNATURE_INVALID")
    pos=8; chunks=[]; ihdr=None; idat=0; iend=False
    while pos < len(data):
        if pos+12>len(data): raise ValueError("PNG_CHUNK_TRUNCATED")
        length=struct.unpack(">I",data[pos:pos+4])[0]
        kind=data[pos+4:pos+8]
        end=pos+12+length
        if end>len(data): raise ValueError("PNG_CHUNK_LENGTH_INVALID")
        payload=data[pos+8:pos+8+length]
        crc=struct.unpack(">I",data[pos+8+length:end])[0]
        actual=binascii.crc32(kind+payload)&0xffffffff
        if crc!=actual: raise ValueError("PNG_CHUNK_CRC_MISMATCH")
        if kind==b"IHDR":
            if length!=13: raise ValueError("PNG_IHDR_LENGTH_INVALID")
            width,height,depth,color,compression,filter_method,interlace=struct.unpack(">IIBBBBB",payload)
            ihdr={"width":width,"height":height,"bit_depth":depth,"color_type":color,"compression":compression,"filter":filter_method,"interlace":interlace}
        elif kind==b"IDAT": idat+=length
        elif kind==b"IEND": iend=True; pos=end; break
        chunks.append(kind.decode("ascii"))
        pos=end
    if ihdr is None or idat<=0 or not iend: raise ValueError("PNG_REQUIRED_CHUNKS_MISSING")
    if pos!=len(data): raise ValueError("PNG_TRAILING_BYTES")
    if (ihdr["width"],ihdr["height"],ihdr["bit_depth"],ihdr["color_type"])!=(720,1280,8,2): raise ValueError("PNG_NOT_720X1280_RGB24")
    if ihdr["compression"]!=0 or ihdr["filter"]!=0 or ihdr["interlace"]!=0: raise ValueError("PNG_IHDR_METHOD_MISMATCH")
    return {"width":ihdr["width"],"height":ihdr["height"],"bit_depth":ihdr["bit_depth"],"pixel_format":"RGB24","idat_bytes":idat,"chunk_crc":"PASS"}

def verify_file(root: Path, name: str, row: tuple[str,str,int|None]) -> dict:
    rel, expected_sha, expected_bytes = row
    path=root/rel
    if not path.is_file(): return {"id":name,"path":rel,"status":"FAIL_MISSING"}
    st=path.stat(); actual_sha=sha256_file(path)
    ok=actual_sha==expected_sha and (expected_bytes is None or st.st_size==expected_bytes)
    return {"id":name,"path":rel,"expected_sha256":expected_sha,"actual_sha256":actual_sha,"bytes":st.st_size,"expected_bytes":expected_bytes,"status":"PASS" if ok else "FAIL_PIN_MISMATCH"}

def generate_color_bars(width=720,height=1280) -> bytes:
    colors=[(255,255,255),(255,255,0),(0,255,255),(0,255,0),(255,0,255),(255,0,0),(0,0,255),(32,32,32)]
    buf=bytearray(width*height*3)
    for y in range(height):
        for x in range(width):
            c=colors[min(len(colors)-1,x*len(colors)//width)]
            # 1px registration grid at regular intervals, in source pixels.
            if x%90==0 or y%160==0: c=(128,128,128)
            o=(y*width+x)*3; buf[o:o+3]=bytes(c)
    return bytes(buf)

def generate_gradient(width=720,height=1280) -> bytes:
    buf=bytearray(width*height*3)
    for y in range(height):
        for x in range(width):
            o=(y*width+x)*3
            buf[o]=round(x*255/(width-1)); buf[o+1]=round(y*255/(height-1)); buf[o+2]=round((x+y)*255/(width+height-2))
    return bytes(buf)

def generate_checkerboard(width=720,height=1280) -> bytes:
    buf=bytearray(width*height*3)
    for y in range(height):
        for x in range(width):
            v=255 if ((x+y)&1)==0 else 0; o=(y*width+x)*3; buf[o]=buf[o+1]=buf[o+2]=v
    return bytes(buf)

def load_pinned_adjudicator(path: Path, expected_sha256: str):
    """Load an exact pinned Python file without resolving a generic package name."""
    if not path.is_file():
        raise FileNotFoundError("A3_ADJUDICATOR_FILE_MISSING:" + str(path))
    actual = sha256_file(path)
    if actual != expected_sha256:
        raise ValueError("A3_ADJUDICATOR_SHA256_MISMATCH:" + actual)
    module_name = "_c11e_a3_lineage_adjudicator_v3_pinned"
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    if spec is None or spec.loader is None:
        raise ImportError("A3_ADJUDICATOR_FILE_SPEC_UNAVAILABLE")
    module = importlib.util.module_from_spec(spec)
    previous = sys.modules.get(module_name)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        if previous is None:
            sys.modules.pop(module_name, None)
        else:
            sys.modules[module_name] = previous
        raise
    if not callable(getattr(module, "adjudicate_loop_a3", None)):
        raise ImportError("A3_ADJUDICATOR_ENTRYPOINT_MISSING")
    return module

def main() -> int:
    ap=argparse.ArgumentParser(description="Read-only E6 Option C native Qt/QImage synthetic-frame probe V2.3.2")
    ap.add_argument("--project-root",required=True)
    ap.add_argument("--package-root",default=str(Path(__file__).resolve().parent))
    ap.add_argument("--iterations",type=int,default=7)
    args=ap.parse_args()
    project=Path(args.project_root).resolve(); package=Path(args.package_root).resolve()
    # The V2.2 runner owns its new adjudicator, while the QImage implementation
    # and 37-test target suite remain the already-installed, hash-pinned V2 payload.
    payload_package = project / "tools/c11d/d9/c11e_e6_option_c_native_qt_probe_v2"
    if not payload_package.is_dir():
        print("QIMAGE_V2_PINNED_PAYLOAD_MISSING=" + str(payload_package))
        return 2
    if str(payload_package) not in sys.path: sys.path.insert(0,str(payload_package))
    adjudicator_path = package / "support/a3_lineage_adjudicator_v3.py"
    # Do not import via the generic top-level package name `support`. On some
    # Windows Python installations it may already be resolved from another
    # package namespace. Load the exact hash-pinned file by absolute path instead.
    try:
        adjudicator_module = load_pinned_adjudicator(adjudicator_path, A3_ADJUDICATOR_V3_SHA)
        adjudicate_loop_a3 = adjudicator_module.adjudicate_loop_a3
    except Exception as exc:
        actual = sha256_file(adjudicator_path) if adjudicator_path.is_file() else "MISSING"
        print("A3_ADJUDICATOR_FILE_LOAD=BLOCKED:" + type(exc).__name__ + ":" + str(exc))
        print("A3_ADJUDICATOR_V3_ACTUAL_SHA256=" + actual)
        return 2
    legacy_module_path = project / "tools/c11d/d9/c11e_e6_option_c_native_qt_probe_v2_3/support/a3_lineage_adjudicator_v3.py"
    legacy_module_sha = sha256_file(legacy_module_path) if legacy_module_path.is_file() else "MISSING"
    print("V2_2_ADJUDICATOR_FILE=" + ("PIN_MATCH" if legacy_module_sha == A3_ADJUDICATOR_V3_SHA else "NOT_PRESENT_OR_DIFFERENT"))
    run_id="E6OPTCQTV2_3_"+datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ_")+uuid.uuid4().hex[:8].upper()
    out_rel=Path("artifacts/tests/c11e/e6_option_c_native_qt_probe_v2_3")/run_id
    out=project/out_rel
    if out.exists():
        print("OUTPUT_COLLISION=FAIL"); return 2
    out.mkdir(parents=True,exist_ok=False)
    source_checks=[verify_file(project,k,v) for k,v in REL.items()]
    # Verify benchmark evidence archive and its exact payload set before relying on it.
    evidence_zip=payload_package/"reference"/"e6_option_c_target_benchmark.zip"
    evidence_zip_sha=sha256_file(evidence_zip) if evidence_zip.is_file() else None
    archive_rows=[]; archive_receipt=None
    try:
        if evidence_zip_sha!=BENCH_ZIP_SHA: raise ValueError("BENCHMARK_EVIDENCE_ZIP_SHA_MISMATCH")
        with zipfile.ZipFile(evidence_zip) as z:
            names=[n for n in z.namelist() if not n.endswith("/")]
            expected={
             "e6_option_c_target_benchmark/E6OPTCBENCH_20261119T202929Z_FDA0D2B8/C11E_E6_OPTION_C_TARGET_BENCHMARK_RECEIPT_V1.json",
             "e6_option_c_target_benchmark/E6OPTCBENCH_20261119T202929Z_FDA0D2B8/C11E_E6_OPTION_C_TARGET_BENCHMARK_RECEIPT_V1.json.sha256",
             *["e6_option_c_target_benchmark/E6OPTCBENCH_20261119T202929Z_FDA0D2B8/"+n for n in BENCH_PNGS]
            }
            if set(names)!=expected: raise ValueError("BENCHMARK_EVIDENCE_MEMBER_SET_MISMATCH")
            pfx="e6_option_c_target_benchmark/E6OPTCBENCH_20261119T202929Z_FDA0D2B8/"
            for n,expected_sha in BENCH_PNGS.items():
                data=z.read(pfx+n); actual=sha256_bytes(data); contract=png_contract(data)
                archive_rows.append({"name":n,"sha256":actual,"expected_sha256":expected_sha,"png":contract,"status":"PASS" if actual==expected_sha else "FAIL"})
            rec_bytes=z.read(pfx+"C11E_E6_OPTION_C_TARGET_BENCHMARK_RECEIPT_V1.json")
            if sha256_bytes(rec_bytes)!=BENCH_RECEIPT_SHA: raise ValueError("BENCHMARK_ARCHIVE_RECEIPT_SHA_MISMATCH")
            side=z.read(pfx+"C11E_E6_OPTION_C_TARGET_BENCHMARK_RECEIPT_V1.json.sha256").decode("ascii").strip()
            if side!=BENCH_RECEIPT_SHA+"  C11E_E6_OPTION_C_TARGET_BENCHMARK_RECEIPT_V1.json": raise ValueError("BENCHMARK_ARCHIVE_RECEIPT_SIDECAR_MISMATCH")
            rec=json.loads(rec_bytes)
            b=rec.get("benchmark",{}); m=rec.get("module",{}); g=rec.get("governance",{})
            if rec.get("status")!="BLOCKED_PYTHON_REFERENCE_NOT_30FPS_HOT_PATH_USE_NATIVE_D_BOUNDARY": raise ValueError("BENCHMARK_ARCHIVE_STATUS_MISMATCH")
            if b.get("iterations")!=7 or b.get("median_ms")!=1277.7267 or b.get("p95_ms")!=2050.1467: raise ValueError("BENCHMARK_ARCHIVE_TIMING_MISMATCH")
            if m.get("actual_sha256")!=OPTIONC_PY_SHA or m.get("actual_bytes")!=OPTIONC_PY_BYTES: raise ValueError("BENCHMARK_ARCHIVE_MODULE_PIN_MISMATCH")
            for flag in ["source_files_modified","c11c_modified","d4_8_v2_modified","godot_invoked","ffmpeg_invoked","ffprobe_invoked","audio_generated","mux_invoked","production_media_created"]:
                if g.get(flag) is not False: raise ValueError("BENCHMARK_ARCHIVE_GOVERNANCE_MISMATCH:"+flag)
            archive_receipt=rec
    except Exception as exc:
        archive_error=str(exc)
    else: archive_error=None
    # Compare active project artifact payloads with the separately uploaded evidence archive.
    active_png_rows=[]
    if archive_error is None:
        base=project/"artifacts/tests/c11e/e6_option_c_target_benchmark/E6OPTCBENCH_20261119T202929Z_FDA0D2B8"
        for n,expected_sha in BENCH_PNGS.items():
            p=base/n
            if not p.is_file(): active_png_rows.append({"name":n,"status":"FAIL_MISSING"}); continue
            actual=sha256_file(p); active_png_rows.append({"name":n,"sha256":actual,"expected_sha256":expected_sha,"status":"PASS" if actual==expected_sha else "FAIL_PIN_MISMATCH"})
    # Correctly classify the specialized A3 PASS without modifying old receipts.
    adjudication=None; adjudication_error=None
    try:
        loop=read_json(project/REL["loop_policy_v2_receipt"][0])
        diag=read_json(project/REL["a3_diagnostic_v1"][0])
        reuse=read_json(project/REL["smoke18_reuse_requalification"][0])
        summary=reuse.get("candidate_summary",{})
        if reuse.get("status")!="PASS_REUSE_EVIDENCE_LINKAGE_REQUALIFIED_NOT_E6_ACCEPTANCE": raise ValueError("SMOKE18_REUSE_STATUS_MISMATCH")
        if summary.get("smoke18_rows")!=18 or summary.get("reconciled_reuse_candidates")!=13 or summary.get("e6_accepted")!=0: raise ValueError("SMOKE18_REUSE_SUMMARY_MISMATCH")
        adjudication=adjudicate_loop_a3(project,loop,diag)
    except Exception as exc: adjudication_error=str(exc)
    # Runtime preflight. No installation or dependency provisioning.
    runtime={"python_version":".".join(map(str,sys.version_info[:3])),"platform":platform.platform(),"pyside6":"NOT_CHECKED"}
    runtime_error=None; qimg_module=None
    if tuple(sys.version_info[:3])!=EXPECTED_PYTHON: runtime_error="PYTHON_VERSION_MISMATCH"
    else:
        try:
            import PySide6
            runtime["pyside6"]=PySide6.__version__
            if PySide6.__version__!=EXPECTED_PYSIDE6: runtime_error="PYSIDE6_VERSION_MISMATCH"
            else:
                from PySide6.QtCore import qVersion
                runtime["qt_version"]=qVersion()
                from payload.tools.c11d.d9 import c11e_e6_option_c_qimage_frame_compositor_v1 as qimg_module
        except Exception as exc:
            runtime_error="PYSIDE6_PREFLIGHT_FAILED:"+type(exc).__name__+":"+str(exc)
    tests_summary={"run":False,"tests":0,"failures":0,"errors":0,"status":"NOT_RUN"}
    fixtures=[]; benchmark={"status":"NOT_RUN","iterations":args.iterations}
    if runtime_error is None and archive_error is None and adjudication_error is None and all(r["status"]=="PASS" for r in source_checks) and all(r["status"]=="PASS" for r in active_png_rows):
        tests_path=payload_package/"payload/tests/c11e/test_c11e_e6_option_c_qimage_frame_compositor_v1.py"
        spec=importlib.util.spec_from_file_location("qimage_target_tests",tests_path)
        tests_mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(tests_mod)
        suite=unittest.defaultTestLoader.loadTestsFromModule(tests_mod)
        result_stream=open(out/"unit_tests.txt","w",encoding="utf-8")
        result=unittest.TextTestRunner(stream=result_stream,verbosity=2).run(suite)
        result_stream.close()
        tests_summary={"run":True,"tests":result.testsRun,"failures":len(result.failures),"errors":len(result.errors),"status":"PASS" if result.wasSuccessful() else "FAIL"}
        if result.wasSuccessful():
            # Synthetic fixtures only; these are the exact approved output dimensions and RGB24 format.
            module=qimg_module
            fixture_sources={"color_bars_registration":generate_color_bars(),"smooth_rgb_gradient":generate_gradient(),"one_pixel_checkerboard":generate_checkerboard()}
            for name,src in fixture_sources.items():
                src_sha=sha256_bytes(src); image=module.compose_rgb24_image(src,720,1280); raw=bytes(image.constBits())
                png_path=out/("OPTION_C_QT_"+name+".png")
                if not image.save(str(png_path),"PNG"): raise RuntimeError("QIMAGE_PNG_SAVE_FAILED:"+name)
                png_bytes=png_path.read_bytes(); png_info=png_contract(png_bytes)
                fixtures.append({"id":name,"source_sha256":src_sha,"output_rgb24_sha256":sha256_bytes(raw),"preview_path":str(out_rel/png_path.name).replace("\\","/"),"preview_sha256":sha256_bytes(png_bytes),"preview_validation":png_info,"source_immutable":sha256_bytes(src)==src_sha})
            # Per-frame stage timing on a smooth deterministic 720x1280 source.
            bench_src=fixture_sources["smooth_rgb_gradient"]
            module.compose_rgb24_frame(bench_src,720,1280) # warmup
            samples=[]
            for _ in range(args.iterations):
                t0=time.perf_counter_ns(); module.compose_rgb24_frame(bench_src,720,1280); samples.append((time.perf_counter_ns()-t0)/1_000_000.0)
            ordered=sorted(samples); p50=statistics.median(ordered); p95=ordered[max(0,__import__('math').ceil(.95*len(ordered))-1)]
            fps=1000.0/p95 if p95>0 else 0.0
            benchmark={"iterations":args.iterations,"samples_ms":samples,"p50_ms":p50,"p95_ms":p95,"max_ms":max(samples),"approx_frames_per_second_at_p95":fps,"frame_interval_ms":1000.0/30.0,"preferred_stage_budget_ms":1000.0/60.0,"stage_30fps_budget":"PASS" if p95<=1000.0/30.0 else "BLOCKED","preferred_budget":"PASS" if p95<=1000.0/60.0 else "NOT_MET","end_to_end_qualified":False}
    # Read exact user-provided native benchmark result; it remains the admission reference for Python backend.
    bench_old=archive_receipt.get("benchmark",{}) if archive_receipt else {}
    old_module=archive_receipt.get("module",{}) if archive_receipt else {}
    overall="PASS_QIMAGE_STAGE_BENCHMARKED_NOT_END_TO_END" if tests_summary["status"]=="PASS" and benchmark.get("stage_30fps_budget")=="PASS" else ("BLOCKED_QIMAGE_NATIVE_STAGE_OVER_BUDGET" if tests_summary["status"]=="PASS" else "BLOCKED_NATIVE_QT_PROBE")
    if runtime_error or archive_error or adjudication_error or any(r["status"]!="PASS" for r in source_checks) or any(r["status"]!="PASS" for r in active_png_rows): overall="BLOCKED_NATIVE_QT_PROBE_PREFLIGHT"
    receipt={
      "schema":"C11E-E6-OPTION-C-NATIVE-QT-PROBE-RECEIPT-V2.3","run_id":run_id,"created_utc":datetime.now(timezone.utc).isoformat(),"status":overall,
      "source_checks":source_checks,"benchmark_evidence_archive":{"sha256":evidence_zip_sha,"expected_sha256":BENCH_ZIP_SHA,"error":archive_error,"pngs":archive_rows},
      "active_benchmark_pngs":active_png_rows,"previous_python_benchmark":{"receipt_sha256":BENCH_RECEIPT_SHA,"status":bench_old.get("python_reference_admission"),"p50_ms":bench_old.get("median_ms"),"p95_ms":bench_old.get("p95_ms"),"fps_at_p95":bench_old.get("approx_frames_per_second_at_p95"),"module_sha256":old_module.get("actual_sha256")},
      "loop_policy_a3_adjudication":{"status":"PASS" if adjudication else "BLOCKED","result":adjudication,"error":adjudication_error,"source_receipt_sha256":LOOP_V2_SHA,"diagnostic_sha256":A3_DIAG_SHA},
      "runtime":runtime,"runtime_error":runtime_error,"qimage_tests":tests_summary,"fixtures":fixtures,"qimage_benchmark":benchmark,
      "governance":{"c11c_modified":False,"d4_8_v2_modified":False,"source_files_modified":False,"renderer_invoked":False,"renderer_native_input_emitted":False,"production_dispatch":False,"godot_invoked":False,"ffmpeg_invoked":False,"ffprobe_invoked":False,"audio_generated":False,"mux_invoked":False,"production_media_created":False,"batch_id_consumed":False,"e6_accepted":0,"release_authority":"NONE","git_checks":"SKIPPED","commits":"OPERATOR_MANAGED","source_file_pins":"ENFORCED"},
      "next_stage":"D_ONLY_QIMAGE_CONSUMER_INTEGRATION_AND_L1_NATIVE_PIXEL_QUALIFICATION" if overall=="PASS_QIMAGE_STAGE_BENCHMARKED_NOT_END_TO_END" else "PRESERVE_RECEIPT_AND_REMEDIATE_EXACT_PREFLIGHT_OR_PERFORMANCE_BLOCKER"
    }
    data=(json.dumps(receipt,indent=2,ensure_ascii=False)+"\n").encode("utf-8")
    rp=out/"C11E_E6_OPTION_C_NATIVE_QT_PROBE_RECEIPT_V2_3.json"; rp.write_bytes(data)
    rh=sha256_bytes(data); side=(rh+"  "+rp.name+"\n").encode("ascii"); sp=out/(rp.name+".sha256"); sp.write_bytes(side)
    print("A3_ADJUDICATOR_V3_PIN=PASS/PATH_LOADED")
    print("OPTION_C_V4_MODULE_PIN="+("PASS" if source_checks[2]["status"]=="PASS" else "FAIL"))
    print("LOOP_POLICY_A3_V3_ADJUDICATION="+(adjudication["status"] if adjudication else "BLOCKED/"+str(adjudication_error)))
    print("BENCHMARK_EVIDENCE_ARCHIVE="+("PASS" if archive_error is None else "FAIL/"+str(archive_error)))
    print("PYTHON_VERSION="+runtime["python_version"])
    print("PYSIDE6_VERSION="+str(runtime["pyside6"]))
    print("QIMAGE_TESTS="+str(tests_summary["tests"])+"; STATUS="+tests_summary["status"])
    if benchmark.get("status")!="NOT_RUN": print("QIMAGE_BENCHMARK_ITERATIONS=%d; P50_MS=%.4f; P95_MS=%.4f; FPS_AT_P95=%.4f"%(args.iterations,benchmark["p50_ms"],benchmark["p95_ms"],benchmark["approx_frames_per_second_at_p95"]))
    print("OPTION_C_NATIVE_QT_PROBE_V2_3_STATUS="+overall)
    print("RECEIPT="+str(rp)); print("RECEIPT_SHA256="+rh); print("RECEIPT_SIDECAR="+str(sp))
    print("SOURCE_FILES_MODIFIED=FALSE; C11C_MODIFIED=FALSE; D4_8_V2_MODIFIED=FALSE")
    print("GODOT_INVOKED=FALSE; FFMPEG_INVOKED=FALSE; FFPROBE_INVOKED=FALSE; AUDIO_GENERATED=FALSE; MUX_INVOKED=FALSE")
    return 0 if overall=="PASS_QIMAGE_STAGE_BENCHMARKED_NOT_END_TO_END" else 2

if __name__=="__main__":
    raise SystemExit(main())
