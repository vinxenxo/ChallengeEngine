from __future__ import annotations
import argparse, binascii, hashlib, json, os, struct, uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

FROZEN_C11C_SHA = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
FROZEN_C11C_BYTES = 796318
D48_V2_SHA = "0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07"
D48_V2_BYTES = 12996
V27_INSTALL_RECEIPT = {
    "path": "artifacts/tests/c11e/e6_qt_install/E6QTI27_20261119T225450Z_CBA13490/r.json",
    "sha256": "48dc18147f2e2f3eaed4b72d42df1d97fa39eb20b0a464eea9debc6b3acd6173",
}
V27_QT_RECEIPT = {
    "path": "artifacts/tests/c11e/e6_option_c_native_qt_probe_v2_7/E6OPTCQTV2_7_20261119T225516Z_6DCBCB1C/C11E_E6_OPTION_C_NATIVE_QT_PROBE_RECEIPT_V2_7.json",
    "sha256": "95819ea730283ded149faa490b21e0df392341366a853b3c0913318fb203d783",
}
CHALLENGE_READBACK = {
    "receipt": "artifacts/tests/c11e/e6_challenge_live_consumer_readback_prepare_only/E6CHLIVECONTRACT_20261119T081811Z_D0FCF727/E6_CHALLENGE_LIVE_CONSUMER_READBACK_RECEIPT_V1.json",
    "receipt_sha256": "b12e3e45e48917b6f4af7aa6b0e54f113473e17825641482f6c39763feab1eb0",
    "plan": "artifacts/tests/c11e/e6_challenge_live_consumer_readback_prepare_only/E6CHLIVECONTRACT_20261119T081811Z_D0FCF727/E6_CHALLENGE_LIVE_CONSUMER_READBACK_PLAN_V1.json",
    "plan_sha256": "e6ee9c9ac850df2a5579c26743c116392ade1ae349fb905a36b55f907dd43e82",
}
CH004_SOURCE = {
    "receipt": "artifacts/tests/c11e/e6_ch004_source_pin_adjudication/E6CH004ADJ_20261118T101236Z_6C62AE7F/E6CH004ADJ_20261118T101236Z_6C62AE7F_REPORT_V1.json",
    "sha256": "d99cec7ac6b0edb71665eadfd25314bd4eebece0bca9e17f05fa9cf943fa6ebd",
    "diff": "artifacts/tests/c11e/e6_ch004_source_pin_adjudication/E6CH004ADJ_20261118T101236Z_6C62AE7F/E6CH004ADJ_20261118T101236Z_6C62AE7F_SOURCE_DIFFS_V1.txt",
    "diff_sha256": "d4b277e9296adc3a0a61aeeb391f5931d978a646101f88679a56565a2735e6c2",
}
CH004_SEMANTIC = {
    "receipt": "artifacts/tests/c11e/e6_ch004_semantic_noninterference/E6CH004SEM_20261118T113817Z_462AEF1F/E6CH004SEM_20261118T113817Z_462AEF1F_REPORT_V3.json",
    "sha256": "ded460447cf69f9360d5761627b0ae6a191a6c687043d8ae2ba4eeeeb01a105a",
}
SMOKE18_REQUAL = {
    "receipt": "artifacts/tests/c11e/e6_smoke18_reuse_requalification/E6SMK18REQUAL_20261119T141719Z_A5555D34/E6_SMOKE18_REUSE_REQUALIFICATION_RECEIPT_V1.json",
    "sha256": "2071d276429fa102c080018ee1421f5397cc3c5be74a7b0451e2ccad2ced494d",
}
LOOP_POLICY_V2 = {
    "receipt": "artifacts/tests/c11e/e6_loop_policy_pin_reconciliation_v2/E6LOOPPOLICYV2_20261119T184655Z_9466C358/E6_LOOP_POLICY_PIN_RECONCILIATION_RECEIPT_V2.json",
    "sha256": "5afc42ca84480ba1d025d288f2653d009e85af053fff5b62133e067a17dfb4be",
}
MATRIX = {
    "path": "definitions/c11e/test_only/C11E_E6_SMOKE18_SCENARIO_MATRIX_20261119_V1.json",
    "sha256": "98e391738c0409c5d9d94576195d48cabcd885957434858062a44a44fe77fb75",
}
POLICY_V2 = {
    "path": "definitions/c11e/test_only/C11E_E6_SMOKE18_SUCCESSOR_POLICY_DRAFT_V2.json",
    "sha256": "86620daa1fe87b946da5c27a2a1b228d566bc341709371f537b112d5f8100ec0",
}
AUTH_DRAFT_V1 = {
    "path": "definitions/c11e/test_only/C11E_E6_SMOKE18_TEST_ONLY_AUTHORIZATION_DRAFT_20261119_V1.json",
    "sha256": "244caf60073428e9e9dc5e4af50502be845d097403c0c951cb2626136d813a56",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_rgb24_png(path: Path) -> dict[str, Any]:
    """Verify PNG structure, chunk CRCs and the exact 720x1280 RGB24 contract."""
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("PNG_SIGNATURE_INVALID")
    pos = 8
    ihdr = None
    idat_bytes = 0
    found_iend = False
    while pos < len(data):
        if pos + 12 > len(data):
            raise ValueError("PNG_CHUNK_TRUNCATED")
        size = struct.unpack(">I", data[pos:pos + 4])[0]
        kind = data[pos + 4:pos + 8]
        end = pos + 12 + size
        if end > len(data):
            raise ValueError("PNG_CHUNK_LENGTH_INVALID")
        payload = data[pos + 8:pos + 8 + size]
        expected_crc = struct.unpack(">I", data[pos + 8 + size:end])[0]
        actual_crc = binascii.crc32(kind + payload) & 0xffffffff
        if actual_crc != expected_crc:
            raise ValueError("PNG_CHUNK_CRC_MISMATCH")
        if kind == b"IHDR":
            if size != 13:
                raise ValueError("PNG_IHDR_LENGTH_INVALID")
            width, height, depth, color, compression, filter_method, interlace = struct.unpack(">IIBBBBB", payload)
            ihdr = (width, height, depth, color, compression, filter_method, interlace)
        elif kind == b"IDAT":
            idat_bytes += size
        elif kind == b"IEND":
            if size != 0:
                raise ValueError("PNG_IEND_INVALID")
            found_iend = True
            pos = end
            break
        pos = end
    if not found_iend or ihdr is None or idat_bytes <= 0 or pos != len(data):
        raise ValueError("PNG_REQUIRED_CHUNKS_OR_TRAILING_DATA_INVALID")
    if ihdr != (720, 1280, 8, 2, 0, 0, 0):
        raise ValueError("PNG_NOT_720X1280_RGB24")
    return {"width": 720, "height": 1280, "bit_depth": 8, "pixel_format": "RGB24", "chunk_crc": "PASS", "idat_bytes": idat_bytes}


def verify_install_postimages(root: Path, rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Rehash every V2.7 installed postimage, including all 11 repository docs."""
    checks = []
    seen = set()
    for row in rows:
        rel = row.get("path")
        expected_sha = row.get("sha256")
        expected_bytes = row.get("bytes")
        if not isinstance(rel, str) or not isinstance(expected_sha, str) or not isinstance(expected_bytes, int):
            checks.append({"path": rel, "status": "BLOCKED_INSTALL_ROW_MALFORMED"})
            continue
        if rel in seen:
            checks.append({"path": rel, "status": "BLOCKED_INSTALL_ROW_DUPLICATE"})
            continue
        seen.add(rel)
        try:
            target = relative_file(root, rel)
            exists = target.is_file()
            actual_sha = sha256_file(target) if exists else None
            actual_bytes = target.stat().st_size if exists else None
            ok = exists and actual_sha == expected_sha and actual_bytes == expected_bytes and row.get("status") in {"ADDED_AND_VERIFIED", "VERIFIED_IDENTICAL"}
            checks.append({"path": rel, "expected_sha256": expected_sha, "actual_sha256": actual_sha, "expected_bytes": expected_bytes, "actual_bytes": actual_bytes, "row_status": row.get("status"), "status": "PASS" if ok else "BLOCKED_INSTALL_POSTIMAGE_MISMATCH"})
        except Exception as exc:
            checks.append({"path": rel, "status": "BLOCKED_INSTALL_POSTIMAGE_ERROR", "error": type(exc).__name__ + ":" + str(exc)})
    docs = [row for row in checks if isinstance(row.get("path"), str) and (row["path"].startswith("docs/") or row["path"].startswith("prompts/"))]
    okay = len(rows) == 18 and len(checks) == 18 and all(row.get("status") == "PASS" for row in checks) and len(docs) == 11
    return {"status": "PASS" if okay else "BLOCKED_INSTALL_POSTIMAGES", "file_count": len(checks), "documentation_count": len(docs), "rows": checks}


def relative_file(root: Path, relative: str) -> Path:
    candidate = (root / relative).resolve()
    root_resolved = root.resolve()
    if candidate != root_resolved and root_resolved not in candidate.parents:
        raise ValueError("PATH_ESCAPE:" + relative)
    return candidate


def verify_sidecar(receipt_path: Path, expected_sha: str | None = None) -> dict[str, Any]:
    sidecar = Path(str(receipt_path) + ".sha256")
    if not sidecar.is_file():
        return {"status": "BLOCKED_SIDECAR_MISSING", "path": str(sidecar)}
    token = sidecar.read_text(encoding="ascii").strip().split()
    actual = sha256_file(receipt_path)
    okay = bool(token) and token[0].lower() == actual and (expected_sha is None or actual == expected_sha)
    return {"status": "PASS" if okay else "BLOCKED_SIDECAR_OR_RECEIPT_SHA_MISMATCH", "path": str(sidecar), "receipt_sha256": actual, "sidecar_sha256": token[0].lower() if token else None}


def verify_pinned_json(root: Path, row: dict[str, str]) -> tuple[dict[str, Any], dict[str, Any] | None]:
    path = relative_file(root, row["path"])
    if not path.is_file():
        return {"id": row.get("id", row["path"]), "path": row["path"], "status": "BLOCKED_MISSING"}, None
    actual_sha = sha256_file(path)
    if actual_sha != row["sha256"]:
        return {"id": row.get("id", row["path"]), "path": row["path"], "expected_sha256": row["sha256"], "actual_sha256": actual_sha, "status": "BLOCKED_SHA256_MISMATCH"}, None
    try:
        obj = read_json(path)
    except Exception as exc:
        return {"id": row.get("id", row["path"]), "path": row["path"], "status": "BLOCKED_JSON_INVALID", "error": type(exc).__name__ + ":" + str(exc)}, None
    return {"id": row.get("id", row["path"]), "path": row["path"], "sha256": actual_sha, "bytes": path.stat().st_size, "status": "PASS"}, obj


def validate_v27_install(root: Path) -> tuple[dict[str, Any], dict[str, Any] | None]:
    path = relative_file(root, V27_INSTALL_RECEIPT["path"])
    if not path.is_file():
        return {"id": "v2_7_install_receipt", "status": "BLOCKED_MISSING", "path": V27_INSTALL_RECEIPT["path"]}, None
    actual = sha256_file(path)
    if actual != V27_INSTALL_RECEIPT["sha256"]:
        return {"id": "v2_7_install_receipt", "status": "BLOCKED_SHA256_MISMATCH", "expected_sha256": V27_INSTALL_RECEIPT["sha256"], "actual_sha256": actual}, None
    obj = read_json(path)
    side = verify_sidecar(path, actual)
    installed_rows = obj.get("installed_files", [])
    postimages = verify_install_postimages(root, installed_rows if isinstance(installed_rows, list) else [])
    expected_zip_sha = "5a6b008047d702014100987f814ae7d98bd75c1f909fa2da0eb75b872f85eb27"
    checks = {
        "schema": obj.get("schema") == "C11E-E6-OPTION-C-NATIVE-QT-PROBE-INSTALL-RECEIPT-V2",
        "status": obj.get("status") == "PASS_ADD_ONLY",
        "revision": obj.get("installer_revision") == "V2.7_PS51_DOCS_TRANSACTION_AND_QIMAGE_SOURCE_PIN_FIX",
        "package_zip": obj.get("package_zip_sha256") == expected_zip_sha,
        "package_members": obj.get("package_members") == 20,
        "destinations": obj.get("install_destinations") == 18,
        "add_count": obj.get("add_count") == 18,
        "skip_count": obj.get("skip_identical_count") == 0,
        "installed_files": len(installed_rows) == 18,
        "docs_count": obj.get("documentation_files") == 11,
        "docs_roots": obj.get("documentation_roots") == ["docs/history/c11e/overlays/C11E_E6_OPTION_C_NATIVE_QT_PROBE_V2_7_PS51_DOCS_FIX_20261119", "docs/current/e"],
        "current_doc_index": obj.get("current_doc_index") == "docs/current/e/C11E_CURRENT_DOC_INDEX_20261119_V175.md",
        "gate_matrix": obj.get("gate_matrix") == "docs/current/e/C11E_GATES_ACCEPTANCE_MATRIX_20261119_V174.md",
        "frozen_c11c": obj.get("c11c_manifest_sha256") == FROZEN_C11C_SHA,
        "d4_8": obj.get("d4_8_v2_sha256") == D48_V2_SHA,
        "governance": obj.get("source_files_modified") is False and obj.get("c11c_modified") is False and obj.get("d4_8_v2_modified") is False and obj.get("release_authority") == "NONE",
        "postimages": postimages.get("status") == "PASS",
        "sidecar": side.get("status") == "PASS",
    }
    okay = all(checks.values())
    return {"id": "v2_7_install_receipt", "path": V27_INSTALL_RECEIPT["path"], "sha256": actual, "checks": checks, "postimages": postimages, "status": "PASS" if okay else "BLOCKED_RECEIPT_CONTRACT_OR_POSTIMAGE", "sidecar": side}, obj


def validate_v27_qt(root: Path) -> tuple[dict[str, Any], dict[str, Any] | None]:
    path = relative_file(root, V27_QT_RECEIPT["path"])
    if not path.is_file():
        return {"id": "v2_7_qt_receipt", "status": "BLOCKED_MISSING", "path": V27_QT_RECEIPT["path"]}, None
    actual = sha256_file(path)
    if actual != V27_QT_RECEIPT["sha256"]:
        return {"id": "v2_7_qt_receipt", "status": "BLOCKED_SHA256_MISMATCH", "expected_sha256": V27_QT_RECEIPT["sha256"], "actual_sha256": actual}, None
    obj = read_json(path)
    side = verify_sidecar(path, actual)
    runtime = obj.get("runtime", {})
    tests = obj.get("qimage_tests", {})
    bench = obj.get("qimage_benchmark", {})
    a3 = obj.get("loop_policy_a3_adjudication", {})
    governance = obj.get("governance", {})
    source_checks = obj.get("source_checks", [])
    fixtures = obj.get("fixtures", [])
    active_source_rows = []
    active_source_ok = True
    for row in source_checks:
        rel = row.get("path")
        expected_sha = row.get("expected_sha256")
        expected_bytes = row.get("expected_bytes")
        try:
            if not isinstance(rel, str) or not isinstance(expected_sha, str):
                raise ValueError("SOURCE_PIN_ROW_MALFORMED")
            source_path = relative_file(root, rel)
            actual_sha = sha256_file(source_path) if source_path.is_file() else None
            actual_bytes = source_path.stat().st_size if source_path.is_file() else None
            row_ok = source_path.is_file() and row.get("status") == "PASS" and actual_sha == expected_sha and actual_bytes == expected_bytes
            active_source_rows.append({"id": row.get("id"), "path": rel, "expected_sha256": expected_sha, "actual_sha256": actual_sha, "expected_bytes": expected_bytes, "actual_bytes": actual_bytes, "status": "PASS" if row_ok else "BLOCKED_ACTIVE_SOURCE_PIN_MISMATCH"})
            active_source_ok = active_source_ok and row_ok
        except Exception as exc:
            active_source_rows.append({"id": row.get("id"), "path": rel, "status": "BLOCKED_ACTIVE_SOURCE_PIN_ERROR", "error": type(exc).__name__ + ":" + str(exc)})
            active_source_ok = False
    checks = {
        "schema": obj.get("schema") == "C11E-E6-OPTION-C-NATIVE-QT-PROBE-RECEIPT-V2.7",
        "status": obj.get("status") == "PASS_QIMAGE_STAGE_BENCHMARKED_NOT_END_TO_END",
        "source_pins": len(source_checks) == 23 and all(row.get("status") == "PASS" for row in source_checks) and active_source_ok,
        "a3_v4": a3.get("status") == "PASS" and a3.get("error") is None and a3.get("source_receipt_sha256") == LOOP_POLICY_V2["sha256"],
        "python": runtime.get("python_version") == "3.13.14",
        "pyside6": runtime.get("pyside6") == "6.11.2",
        "qimage_module_runtime_pin": runtime.get("qimage_module_sha256") == "850054e6212f7e6f59be5550ec194df3d1a1ca69acb343c53b76803b007721e1" and runtime.get("qimage_module_path") == str(relative_file(root, "tools/c11d/d9/c11e_e6_option_c_native_qt_probe_v2/payload/tools/c11d/d9/c11e_e6_option_c_qimage_frame_compositor_v1.py")),
        "qimage_tests": tests.get("run") is True and tests.get("tests") == 37 and tests.get("failures") == 0 and tests.get("errors") == 0 and tests.get("status") == "PASS" and obj.get("qimage_test_import_error") is None and obj.get("qimage_test_execution_error") is None,
        "benchmark_iterations": bench.get("iterations") == 7 and len(bench.get("samples_ms", [])) == 7,
        "benchmark_p95": isinstance(bench.get("p95_ms"), (int, float)) and float(bench["p95_ms"]) <= (1000.0 / 30.0),
        "benchmark_stage_budget": bench.get("stage_30fps_budget") == "PASS" and bench.get("end_to_end_qualified") is False,
        "synthetic_fixtures": len(fixtures) == 3 and all(item.get("source_immutable") is True for item in fixtures),
        "governance": governance.get("c11c_modified") is False and governance.get("d4_8_v2_modified") is False and governance.get("source_files_modified") is False and governance.get("godot_invoked") is False and governance.get("ffmpeg_invoked") is False and governance.get("ffprobe_invoked") is False and governance.get("audio_generated") is False and governance.get("mux_invoked") is False and governance.get("production_dispatch") is False and governance.get("production_media_created") is False and governance.get("renderer_native_input_emitted") is False and governance.get("batch_id_consumed") is False and governance.get("e6_accepted") == 0 and governance.get("release_authority") == "NONE",
        "sidecar": side.get("status") == "PASS",
    }
    preview_rows = []
    preview_ok = True
    for item in fixtures:
        rel = item.get("preview_path")
        if not isinstance(rel, str):
            preview_rows.append({"id": item.get("id"), "status": "BLOCKED_PREVIEW_PATH_MISSING"}); preview_ok = False; continue
        try:
            preview = relative_file(root, rel)
            if not preview.is_file():
                preview_rows.append({"id": item.get("id"), "path": rel, "status": "BLOCKED_PREVIEW_FILE_MISSING"}); preview_ok = False; continue
            actual_png = sha256_file(preview)
            png_contract = validate_rgb24_png(preview)
            row_ok = actual_png == item.get("preview_sha256") and item.get("preview_validation", {}).get("chunk_crc") == "PASS" and png_contract.get("chunk_crc") == "PASS"
            preview_rows.append({"id": item.get("id"), "path": rel, "expected_sha256": item.get("preview_sha256"), "actual_sha256": actual_png, "png_contract": png_contract, "status": "PASS" if row_ok else "BLOCKED_PREVIEW_SHA_OR_FORMAT_MISMATCH"})
            preview_ok = preview_ok and row_ok
        except Exception as exc:
            preview_rows.append({"id": item.get("id"), "status": "BLOCKED_PREVIEW_PATH_INVALID", "error": str(exc)}); preview_ok = False
    checks["preview_bytes"] = preview_ok and len(preview_rows) == 3
    okay = all(checks.values())
    return {
        "id": "v2_7_qt_receipt", "path": V27_QT_RECEIPT["path"], "sha256": actual,
        "checks": checks, "source_pin_count": len(source_checks), "active_source_rehash_rows": active_source_rows, "qimage_test_count": tests.get("tests"),
        "benchmark": {"iterations": bench.get("iterations"), "p50_ms": bench.get("p50_ms"), "p95_ms": bench.get("p95_ms"), "fps_at_p95": bench.get("approx_frames_per_second_at_p95")},
        "a3_adjudication": a3.get("status"), "preview_files": preview_rows,
        "visual_resampler_review": "PENDING_OPERATOR_VISUAL_REVIEW_NOT_INFERRED_FROM_HASHES",
        "sidecar": side, "status": "PASS" if okay else "BLOCKED_RECEIPT_CONTRACT_OR_PREVIEW_BYTES"
    }, obj


def audit_project(project_root: str | Path) -> dict[str, Any]:
    root = Path(project_root).resolve()
    if not root.is_dir():
        raise FileNotFoundError("PROJECT_ROOT_NOT_FOUND:" + str(root))
    checks: list[dict[str, Any]] = []
    # Immutable baseline pins.
    for row in [
        {"id": "frozen_c11c_manifest", "path": "release/C11C_FREEZE_PACKAGE_MANIFEST.json", "sha256": FROZEN_C11C_SHA, "bytes": FROZEN_C11C_BYTES},
        {"id": "d4_8_v2", "path": "definitions/c11d/production/C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V2.json", "sha256": D48_V2_SHA, "bytes": D48_V2_BYTES},
        {"id": "qimage_module", "path": "tools/c11d/d9/c11e_e6_option_c_native_qt_probe_v2/payload/tools/c11d/d9/c11e_e6_option_c_qimage_frame_compositor_v1.py", "sha256": "850054e6212f7e6f59be5550ec194df3d1a1ca69acb343c53b76803b007721e1", "bytes": 6483},
        {"id": "qimage_test_suite", "path": "tools/c11d/d9/c11e_e6_option_c_native_qt_probe_v2/payload/tests/c11e/test_c11e_e6_option_c_qimage_frame_compositor_v1.py", "sha256": "9e0017ec5112372b9fb683e6dce4b42f6233db9cdb82fe787b7e0f92a6204306", "bytes": 6528},
        {"id": "challenge_live_consumer", "path": "tools/c11d/d9/C11EChallengeLiveEditorialConsumer.gd", "sha256": "eba81fff4c24ca75033c8f963665df1961136046c41fee0e88681fe55a631203", "bytes": 26367},
        {"id": "challenge_adapter", "path": "tools/c11d/d9/c11e_challenge_editorial_presentation_adapter.gd", "sha256": "d17568882eb63ba2eb48649cb9cd46edafe122d72c0c5ed29275e79b8d6d5846", "bytes": 14167},
        {"id": "d9_resolver", "path": "tools/c11d/d9/universal_editorial_model.py", "sha256": "dac95fb698b52f96432a517d8ec3196a397e5e6bd3c025300350dd55ddce3afd", "bytes": 27585},
        {"id": "d98_model", "path": "definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json", "sha256": "dabb458fc2215156ddb5ebea7e8ebec811098886ce2858733ba9fb13f6075ccb", "bytes": 12932},
    ]:
        p = relative_file(root, row["path"])
        if not p.is_file():
            checks.append({"id": row["id"], "path": row["path"], "status": "BLOCKED_MISSING"}); continue
        actual_sha = sha256_file(p); actual_bytes = p.stat().st_size
        ok = actual_sha == row["sha256"] and actual_bytes == row["bytes"]
        checks.append({"id": row["id"], "path": row["path"], "expected_sha256": row["sha256"], "actual_sha256": actual_sha, "expected_bytes": row["bytes"], "actual_bytes": actual_bytes, "status": "PASS" if ok else "BLOCKED_PIN_MISMATCH"})

    install_check, install_receipt = validate_v27_install(root); checks.append(install_check)
    qt_check, qt_receipt = validate_v27_qt(root); checks.append(qt_check)

    # Challenge static consumer contract: no Godot execution or live readback implied.
    readback_row = {"id": "challenge_static_readback", "path": CHALLENGE_READBACK["receipt"], "sha256": CHALLENGE_READBACK["receipt_sha256"]}
    readback_check, readback = verify_pinned_json(root, readback_row)
    if readback is not None:
        plan_row = {"id": "challenge_static_readback_plan", "path": CHALLENGE_READBACK["plan"], "sha256": CHALLENGE_READBACK["plan_sha256"]}
        plan_check, plan = verify_pinned_json(root, plan_row)
        checks.append(plan_check)
        if plan is not None:
            counts = plan.get("counts", {})
            plan_check["contract"] = counts == {"envelopes_static_compatible": 18, "frame_sample_vectors": 117, "omitted_zero_window_field_slots": 27, "probes": 18, "selectors": 6, "visible_field_slots": 27}
            if not plan_check["contract"]: plan_check["status"] = "BLOCKED_PLAN_COUNTS"
        readback_check["contract"] = readback.get("status") == "PASS_STATIC_CONSUMER_CONTRACT_18_ENVELOPES_RUNTIME_READBACK_NOT_PERFORMED" and readback.get("runtime_editorial_readback") == "NOT_PERFORMED" and readback.get("governance", {}).get("godot_invoked") is False
        if not readback_check["contract"]: readback_check["status"] = "BLOCKED_READBACK_CONTRACT"
        plan_sha = readback.get("plan_sha256")
        readback_check["plan_sha_binding"] = plan_sha == CHALLENGE_READBACK["plan_sha256"]
        if not readback_check["plan_sha_binding"]: readback_check["status"] = "BLOCKED_PLAN_BINDING"
    checks.append(readback_check)

    # CH004 historical pins and semantic noninterference are evidence, not row acceptance.
    ch_source_row = {"id": "ch004_source_pin_adjudication", **CH004_SOURCE}
    ch_source_check, ch_source = verify_pinned_json(root, {"id": ch_source_row["id"], "path": ch_source_row["receipt"], "sha256": ch_source_row["sha256"]})
    if ch_source is not None:
        diff = relative_file(root, ch_source.get("diff_artifact", {}).get("path", ""))
        actual_diff = sha256_file(diff) if diff.is_file() else None
        ch_source_check["historical_preimages"] = ch_source.get("historical_preimage_count") == "2/2"
        ch_source_check["manual_review_required"] = ch_source.get("manual_review_required") is True
        ch_source_check["diff_artifact"] = actual_diff == CH004_SOURCE["diff_sha256"]
        ch_source_check["disposition"] = ch_source.get("ch004_e6_reuse_disposition") == "REUSE_CANDIDATE_PENDING_SEMANTIC_DIFF_REVIEW_AND_E6_LEDGER_REQUALIFICATION"
        if not all(ch_source_check[k] for k in ["historical_preimages", "manual_review_required", "diff_artifact", "disposition"]): ch_source_check["status"] = "BLOCKED_CH004_SOURCE_ADJUDICATION_CONTRACT"
    checks.append(ch_source_check)

    sem_check, sem = verify_pinned_json(root, {"id": "ch004_semantic_noninterference_v3", "path": CH004_SEMANTIC["receipt"], "sha256": CH004_SEMANTIC["sha256"]})
    if sem is not None:
        sem_check["contract"] = sem.get("status") == "PASS_CH004_SEMANTIC_NONINTERFERENCE_CONFIRMED_REQUIRES_E6_LEDGER_REQUALIFICATION" and len(sem.get("checks", [])) == 7 and sem.get("automatic_e6_acceptance") is False and sem.get("e6_ledger_requalification_required") is True and sem.get("ch004_reuse_disposition") == "ELIGIBLE_FOR_E6_LEDGER_REQUALIFICATION_NOT_ACCEPTED"
        if not sem_check["contract"]: sem_check["status"] = "BLOCKED_CH004_SEMANTIC_CONTRACT"
    checks.append(sem_check)

    requal_check, requal = verify_pinned_json(root, {"id": "smoke18_reuse_requalification_v1", "path": SMOKE18_REQUAL["receipt"], "sha256": SMOKE18_REQUAL["sha256"]})
    if requal is not None:
        summary = requal.get("candidate_summary", {})
        ch_sem_link = requal.get("ch004_v4_semantic_review", {})
        requal_check["contract"] = requal.get("status") == "PASS_REUSE_EVIDENCE_LINKAGE_REQUALIFIED_NOT_E6_ACCEPTANCE" and requal.get("check_count") == 21 and requal.get("passed_checks") == 21 and requal.get("failed_checks") == 0 and summary.get("smoke18_rows") == 18 and summary.get("reconciled_reuse_candidates") == 13 and summary.get("e6_accepted") == 0 and summary.get("fresh_challenge_av_required") == 5 and ch_sem_link.get("sha256") == CH004_SEMANTIC["sha256"] and ch_sem_link.get("disposition") == "ELIGIBLE_FOR_E6_LEDGER_REQUALIFICATION_NOT_ACCEPTED"
        if not requal_check["contract"]: requal_check["status"] = "BLOCKED_REQUALIFICATION_CONTRACT"
    checks.append(requal_check)

    loop_check, loop = verify_pinned_json(root, {"id": "loop_policy_pin_reconciliation_v2", "path": LOOP_POLICY_V2["receipt"], "sha256": LOOP_POLICY_V2["sha256"]})
    if loop is not None:
        a3 = None
        for item in loop.get("checks", []):
            if item.get("id") == "a3_lineage_single_pointer_reconciliation": a3 = item
        loop_check["contract"] = loop.get("status") == "PASS_LOOP_POLICY_DECISIONS_RECONCILED_NOT_COMPOSITOR_ACCEPTANCE" and loop.get("check_count") == 18 and loop.get("passed_checks") == 17 and loop.get("failed_checks") == 0 and isinstance(a3, dict) and a3.get("status") == "PASS_SINGLE_POINTER_LINEAGE_RECONCILIATION"
        if not loop_check["contract"]: loop_check["status"] = "BLOCKED_LOOP_POLICY_CONTRACT"
    checks.append(loop_check)

    matrix_check, matrix = verify_pinned_json(root, {"id": "smoke18_candidate_matrix", **MATRIX})
    if matrix is not None:
        matrix_check["contract"] = matrix.get("status") == "DRAFT_CANDIDATE_MATRIX_NOT_FROZEN_NOT_E6_ACCEPTED" and matrix.get("scenario_count") == 18 and matrix.get("challenge_probe_count") == 18 and matrix.get("reuse_candidate_count") == 13 and matrix.get("e6_accepted") == 0
        if not matrix_check["contract"]: matrix_check["status"] = "BLOCKED_MATRIX_CONTRACT"
    checks.append(matrix_check)

    # Sidecars for all immutable historical evidence are checked explicitly.
    sidecar_rows = []
    for rel in [CH004_SOURCE["receipt"], CH004_SOURCE["diff"], CH004_SEMANTIC["receipt"], SMOKE18_REQUAL["receipt"], LOOP_POLICY_V2["receipt"], CHALLENGE_READBACK["receipt"], CHALLENGE_READBACK["plan"]]:
        path = relative_file(root, rel)
        if not path.is_file(): sidecar_rows.append({"path": rel, "status": "BLOCKED_SOURCE_MISSING"}); continue
        sidecar_rows.append({"path": rel, **verify_sidecar(path)})
    sidecars_ok = all(row.get("status") == "PASS" for row in sidecar_rows)
    checks.append({"id": "predecessor_sidecars", "status": "PASS" if sidecars_ok else "BLOCKED_SIDECAR_INTEGRITY", "rows": sidecar_rows})

    pass_count = sum(1 for row in checks if row.get("status") == "PASS")
    fail_count = len(checks) - pass_count
    blocked_ids = [row.get("id", "UNKNOWN") for row in checks if row.get("status") != "PASS"]
    all_pass = fail_count == 0
    overall = "PASS_READ_ONLY_E6_PHASE_RECONCILIATION_WITH_VISUAL_REVIEW_PENDING" if all_pass else "BLOCKED_READ_ONLY_E6_PHASE_RECONCILIATION"
    report = {
        "schema": "C11E-E6-POST-QIMAGE-L1-PHASE-RECONCILIATION-RECEIPT-V1",
        "run_id": "E6L1RECON_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ_") + uuid.uuid4().hex[:8].upper(),
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "project_root": str(root),
        "status": overall,
        "check_count": len(checks), "passed_checks": pass_count, "blocked_checks": fail_count, "blocked_ids": blocked_ids,
        "checks": checks,
        "phase_state": {
            "option_c_qimage_l1": "PASS_QIMAGE_STAGE_BENCHMARKED_NOT_END_TO_END" if qt_check.get("status") == "PASS" else "BLOCKED",
            "qimage_p95_ms": qt_check.get("benchmark", {}).get("p95_ms"),
            "qimage_tests": qt_check.get("qimage_test_count"),
            "a3_v4": "PASS" if loop_check.get("status") == "PASS" and qt_check.get("a3_adjudication") == "PASS" else "BLOCKED",
            "visual_resampler_review": "PENDING_OPERATOR_VISUAL_REVIEW_NOT_INFERRED_FROM_HASHES",
            "challenge_static_consumer": "PASS_STATIC_RUNTIME_READBACK_NOT_PERFORMED" if readback_check.get("status") == "PASS" else "BLOCKED",
            "ch004": "ELIGIBLE_FOR_E6_LEDGER_REQUALIFICATION_NOT_ACCEPTED" if sem_check.get("status") == "PASS" and requal_check.get("status") == "PASS" else "BLOCKED_OR_UNRESOLVED",
            "smoke18_rows": 18 if matrix_check.get("status") == "PASS" else None,
            "reuse_candidates": 13 if requal_check.get("status") == "PASS" else None,
            "e6_accepted": 0,
            "fresh_challenge_av_required": 5,
            "loop_d_composites_outstanding": 6,
            "drill_runtime_readback": "NOT_PROVEN",
            "smoke18_matrix_frozen": False,
        },
        "governance": {
            "c11c_manifest_sha256": FROZEN_C11C_SHA,
            "d4_8_v2_sha256": D48_V2_SHA,
            "d4_8_v2": "BLOCKED_IMMUTABLE",
            "e1": "PREPARE_ONLY", "renderer": "OFF", "production_dispatch": False,
            "production_media": False, "godot_invoked": False, "ffmpeg_invoked": False,
            "ffprobe_invoked": False, "audio_generated": False, "mux_invoked": False,
            "batch_id_consumed": False, "e6_accepted": 0, "release_authority": "NONE",
            "git_checks": "SKIPPED", "commits": "OPERATOR_MANAGED", "source_file_pins": "ENFORCED"
        },
        "next_gate": "OPERATOR_VISUAL_REVIEW_OF_THREE_QIMAGE_SYNTHETIC_PREVIEWS_THEN_READ_ONLY_LOOP_FRAME_SOURCE_CLOSURE_AND_UNARMED_SUCCESSOR_POLICY_REVIEW",
        "no_execution_authority_created": True,
    }
    return report


def write_new(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only C11-E post-QImage L1 reconciliation; no engine/media execution")
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    report = audit_project(root)
    rel = Path("artifacts/tests/c11e/e6_post_qimage_l1_reconciliation") / report["run_id"]
    out = root / rel
    if out.exists():
        print("NO_PASS_EMITTED=TRUE")
        raise SystemExit("OUTPUT_COLLISION:" + str(out))
    out.mkdir(parents=True, exist_ok=False)
    raw = (json.dumps(report, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    receipt = out / "C11E_E6_POST_QIMAGE_L1_PHASE_RECONCILIATION_RECEIPT_V1.json"
    sidecar = Path(str(receipt) + ".sha256")
    write_new(receipt, raw)
    receipt_sha = sha256_bytes(raw)
    write_new(sidecar, (receipt_sha + "  " + receipt.name + "\n").encode("ascii"))
    # Re-read both immutable outputs after creation.
    if sha256_file(receipt) != receipt_sha or sidecar.read_text(encoding="ascii").split()[0] != receipt_sha:
        print("NO_PASS_EMITTED=TRUE")
        return 2
    print("READ_ONLY_EVIDENCE_CHECKS=%d/%d %s" % (report["passed_checks"], report["check_count"], "PASS" if report["blocked_checks"] == 0 else "BLOCKED"))
    print("OPTION_C_QIMAGE_L1=" + report["phase_state"]["option_c_qimage_l1"])
    print("QIMAGE_P95_MS=" + str(report["phase_state"]["qimage_p95_ms"]))
    print("QIMAGE_TESTS=" + str(report["phase_state"]["qimage_tests"]))
    print("CHALLENGE_STATIC_CONSUMER=" + report["phase_state"]["challenge_static_consumer"])
    print("CH004_DISPOSITION=" + report["phase_state"]["ch004"])
    print("E6_ACCEPTED=0")
    print("VISUAL_RESAMPLER_REVIEW=PENDING_OPERATOR_VISUAL_REVIEW")
    print("D4_8_V2=BLOCKED/UNCHANGED; RENDERER=OFF; MEDIA=OFF; RELEASE_AUTHORITY=NONE")
    print("PHASE_RECONCILIATION_STATUS=" + report["status"])
    print("RECEIPT=" + str(receipt))
    print("RECEIPT_SHA256=" + receipt_sha)
    print("RECEIPT_SIDECAR=" + str(sidecar))
    print("GODOT_INVOKED=FALSE; FFMPEG_INVOKED=FALSE; FFPROBE_INVOKED=FALSE; AUDIO_GENERATED=FALSE; MUX_INVOKED=FALSE")
    return 0 if report["blocked_checks"] == 0 else 2

if __name__ == "__main__":
    raise SystemExit(main())
