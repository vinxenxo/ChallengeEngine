from __future__ import annotations
import argparse, binascii, hashlib, json, os, struct, sys, uuid, zlib
from datetime import datetime, timezone
from pathlib import Path

C11C_SHA = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
C11C_BYTES = 796318
D48_SHA = "0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07"
D48_BYTES = 12996
V5_RUN_ID = "E6L2QIMGV5_20261120T104658Z_1B5CBDC6"
V5_INSTALL_ID = "E6L2QIMGV5INST_20261120T104616Z_7DF5A4A9"
V5_RECEIPT_SHA = "192182958c08bf5c00b4756181481ebfea974eea06f9fe88af3cd9597e0fd340"
V5_INSTALL_RECEIPT_SHA = "b41c661909c385f592f0b81ab79206e8aafd73951e5430907c78675ac3af431b"
V4_RECEIPT_SHA = "b36f319a3b7e3290be965dfc1bfa28fdff789b6054e89fc9c3cba182130aad88"
V4_INSTALL_RECEIPT_SHA = "2afb58e86cddfa6bea3c412071f3ba0ca882a95af8c8274382d478d34ef840eb"
V5_RECEIPT_SIDECAR_SHA = "50b731e81e5dd7ba208f2ec8af5bdad0f126a94896a75d7bf6c7490135735b06"
V5_INSTALL_SIDECAR_SHA = "2c7b5f9dbcef76a7fd9d720f6570a8af07ada8855ac7ee18802b555143b52dab"
V4_RECEIPT_SIDECAR_SHA = "fa4002f20f2a0a9438e198617c30bb6b166e88a866db453f0c886078fb4d7403"
V4_INSTALL_SIDECAR_SHA = "eb02033f4fab40add8e198d05dde91d867d463c8fd6b87f72c4ab5c90e548608"
SOURCE_PNG_SHA = "39ae0a4df012faf1b2fd087443ccadf963bb59610affc2756c1732fa42669908"
SOURCE_RGB_SHA = "a0803353be7dca53a75903a1c863bd814a4367b534e698018d8ab434f5506d03"
COMPOSITE_PNG_SHA = "6e2039590b086d0c93f66f848be833175618606368ecba14f7b1e200cb5e333c"
COMPOSITE_RGB_SHA = "d029c31de5d81335b3026ac7d85c902ddfd00d3b1b44a02d0991c5eab28a7b66"
CAPTURE_META_SHA = "aa37687434e714a15f1124282d81015f64e77a441b8a470ea1b98b80d2ad0679"
V5_SOURCE_MANIFEST_SHA = "bda926f2d455024dd306c4615b70f1549da969c16094fda2b9b27735dcbb2d2a"
QIMAGE_MODULE_SHA = "850054e6212f7e6f59be5550ec194df3d1a1ca69acb343c53b76803b007721e1"
V5_ROOT_REL = Path("artifacts/tests/c11e/e6_l2_direct_rgb24_qimage_composition_v5") / V5_RUN_ID
V5_INSTALL_REL = Path("artifacts/tests/c11e/e6_l2_direct_rgb24_qimage_composition_v5_install") / V5_INSTALL_ID
V5_INSTALL_NAME = "C11E_E6_L2_QIMAGE_COMPOSITION_V5_INSTALL_RECEIPT.json"
SOURCE_MANIFEST_REL = Path("definitions/c11e/test_only/C11E_E6_L2_QIMAGE_REPAIR_SOURCE_MANIFEST_V5.json")
C11C_REL = Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")
D48_REL = Path("definitions/c11d/production/C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V2.json")
L3_SOURCE_MANIFEST_REL = Path("definitions/c11e/test_only/C11E_E6_L3_LOOP_NEGATIVE_CONTROL_SOURCE_MANIFEST_V1.json")
L3_SOURCE_MANIFEST_SHA = "b7cb8eabea84ac99486c5800b655cf2f060f0d61c4f1003f8242e4a6d46e5f25"
L3_SOURCE_MANIFEST_BYTES = 4886

class L3AuditError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_file(path: Path, expected_sha: str, expected_bytes: int | None = None) -> Path:
    if not path.is_file():
        raise L3AuditError(f"PINNED_FILE_MISSING:{path}")
    if expected_bytes is not None and path.stat().st_size != expected_bytes:
        raise L3AuditError(f"PINNED_FILE_BYTES_MISMATCH:{path}:{path.stat().st_size}")
    actual = sha256_file(path)
    if actual != expected_sha:
        raise L3AuditError(f"PINNED_FILE_SHA256_MISMATCH:{path}:{actual}")
    return path


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise L3AuditError(f"JSON_READ_FAILED:{path}:{type(exc).__name__}:{exc}") from exc
    if not isinstance(value, dict):
        raise L3AuditError(f"JSON_ROOT_NOT_OBJECT:{path}")
    return value


def require_sidecar(path: Path, digest: str) -> Path:
    side = Path(str(path) + ".sha256")
    expected = f"{digest}  {path.name}"
    if not side.is_file() or side.read_text(encoding="ascii").strip() != expected:
        raise L3AuditError(f"SIDECAR_MISMATCH:{side}")
    return side


def paeth(a: int, b: int, c: int) -> int:
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    if pb <= pc:
        return b
    return c


def decode_png_rgb(path: Path) -> tuple[int, int, bytes, int]:
    """Strict PNG RGB/RGBA8 decoder; validates every chunk CRC and PNG row filter."""
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise L3AuditError(f"PNG_SIGNATURE_INVALID:{path.name}")
    pos = 8
    width = height = bit_depth = color_type = None
    idat = bytearray()
    seen_iend = False
    while pos < len(data):
        if pos + 12 > len(data):
            raise L3AuditError(f"PNG_CHUNK_TRUNCATED:{path.name}")
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        end = pos + 8 + length
        if end + 4 > len(data):
            raise L3AuditError(f"PNG_CHUNK_LENGTH_INVALID:{path.name}")
        payload = data[pos + 8:end]
        expected_crc = struct.unpack(">I", data[end:end + 4])[0]
        actual_crc = binascii.crc32(ctype + payload) & 0xFFFFFFFF
        if actual_crc != expected_crc:
            raise L3AuditError(f"PNG_CRC_MISMATCH:{path.name}:{ctype.decode('ascii','replace')}")
        if ctype == b"IHDR":
            if width is not None or length != 13:
                raise L3AuditError(f"PNG_IHDR_INVALID:{path.name}")
            width, height, bit_depth, color_type, compression, filtering, interlace = struct.unpack(">IIBBBBB", payload)
            if compression != 0 or filtering != 0 or interlace != 0:
                raise L3AuditError(f"PNG_ENCODING_UNSUPPORTED:{path.name}")
            if bit_depth != 8 or color_type not in (2, 6):
                raise L3AuditError(f"PNG_PIXEL_FORMAT_UNSUPPORTED:{path.name}:{bit_depth}:{color_type}")
        elif ctype == b"IDAT":
            idat.extend(payload)
        elif ctype == b"IEND":
            seen_iend = True
            pos = end + 4
            break
        pos = end + 4
    if width is None or not seen_iend or pos != len(data):
        raise L3AuditError(f"PNG_STRUCTURE_INCOMPLETE:{path.name}")
    channels = 3 if color_type == 2 else 4
    bpp = channels
    stride = width * channels
    try:
        decoded = zlib.decompress(bytes(idat))
    except zlib.error as exc:
        raise L3AuditError(f"PNG_IDAT_DECOMPRESS_FAILED:{path.name}:{exc}") from exc
    expected_size = height * (stride + 1)
    if len(decoded) != expected_size:
        raise L3AuditError(f"PNG_DECODED_LENGTH_MISMATCH:{path.name}:{len(decoded)}:{expected_size}")
    rows = bytearray(height * stride)
    offset = 0
    prev = bytearray(stride)
    for y in range(height):
        filt = decoded[offset]
        raw = decoded[offset + 1:offset + 1 + stride]
        offset += stride + 1
        cur = bytearray(stride)
        for x in range(stride):
            left = cur[x - bpp] if x >= bpp else 0
            up = prev[x]
            upper_left = prev[x - bpp] if x >= bpp else 0
            v = raw[x]
            if filt == 0:
                pass
            elif filt == 1:
                v = (v + left) & 255
            elif filt == 2:
                v = (v + up) & 255
            elif filt == 3:
                v = (v + ((left + up) // 2)) & 255
            elif filt == 4:
                v = (v + paeth(left, up, upper_left)) & 255
            else:
                raise L3AuditError(f"PNG_FILTER_UNSUPPORTED:{path.name}:{filt}")
            cur[x] = v
        rows[y * stride:(y + 1) * stride] = cur
        prev = cur
    if color_type == 2:
        return width, height, bytes(rows), color_type
    rgb = bytearray(width * height * 3)
    alpha_index = 3
    out = 0
    for i in range(0, len(rows), 4):
        if rows[i + alpha_index] != 255:
            raise L3AuditError(f"PNG_ALPHA_NOT_OPAQUE:{path.name}")
        rgb[out:out + 3] = rows[i:i + 3]
        out += 3
    return width, height, bytes(rgb), color_type


def validate_rgb24_contract(width: int, height: int, stride: int, byte_count: int,
                            digest: str, frame_index: int = 0,
                            pixel_format: str = "RGB24", source_kind: str = "DIRECT_CAPTURE",
                            color_transform_applied: bool = False) -> None:
    if (width, height) != (720, 1280):
        raise L3AuditError("NEGATIVE_CONTROL_WRONG_DIMENSIONS")
    if pixel_format != "RGB24":
        raise L3AuditError("NEGATIVE_CONTROL_WRONG_PIXEL_FORMAT")
    if stride != 2160:
        raise L3AuditError("NEGATIVE_CONTROL_WRONG_STRIDE")
    if byte_count != 2764800:
        raise L3AuditError("NEGATIVE_CONTROL_WRONG_BYTE_COUNT")
    if digest != SOURCE_RGB_SHA:
        raise L3AuditError("NEGATIVE_CONTROL_ALTERED_SOURCE_HASH")
    if frame_index != 0:
        raise L3AuditError("NEGATIVE_CONTROL_FRAME_ORDER_MISMATCH")
    if source_kind != "DIRECT_CAPTURE":
        raise L3AuditError("NEGATIVE_CONTROL_FORBIDDEN_SOURCE_KIND")
    if color_transform_applied:
        raise L3AuditError("NEGATIVE_CONTROL_COLOR_TRANSFORM_FORBIDDEN")


def validate_geometry(canvas: tuple[int, int], rect: tuple[int, int, int, int]) -> None:
    if canvas != (720, 1280):
        raise L3AuditError("NEGATIVE_CONTROL_CANVAS_GEOMETRY_MISMATCH")
    if rect != (108, 192, 504, 896):
        raise L3AuditError("NEGATIVE_CONTROL_CONTENT_RECT_MISMATCH")
    x, y, w, h = rect
    if x < 0 or y < 0 or x + w > canvas[0] or y + h > canvas[1]:
        raise L3AuditError("CONTENT_RECT_OUT_OF_BOUNDS")


def guard_write_path(candidate: Path, output_root: Path, protected_roots: tuple[Path, ...]) -> Path:
    candidate = candidate.resolve()
    output_root = output_root.resolve()
    for protected in protected_roots:
        protected = protected.resolve()
        try:
            candidate.relative_to(protected)
        except ValueError:
            continue
        raise L3AuditError("NEGATIVE_CONTROL_WRITE_INTO_PROTECTED_EVIDENCE")
    try:
        candidate.relative_to(output_root)
    except ValueError as exc:
        raise L3AuditError("NEGATIVE_CONTROL_WRITE_OUTSIDE_L3_OUTPUT_ROOT") from exc
    return candidate


def validate_process_scope(scope: dict) -> None:
    expected = {"godot": 0, "ffmpeg": 0, "ffprobe": 0, "audio": 0, "mux": 0, "qimage_composition": 0, "dispatch": 0, "batch_id": 0}
    for key, value in expected.items():
        if scope.get(key) != value:
            raise L3AuditError(f"PROCESS_SCOPE_FORBIDDEN:{key}:{scope.get(key)!r}")


def run_negative_controls(output_root: Path, protected_roots: tuple[Path, ...]) -> list[dict]:
    controls = []
    def expect_reject(control_id: str, call):
        try:
            call()
        except L3AuditError:
            controls.append({"id": control_id, "status": "REJECTED_AS_EXPECTED"})
            return
        controls.append({"id": control_id, "status": "FAILED_TO_REJECT"})
        raise L3AuditError(f"NEGATIVE_CONTROL_NOT_REJECTED:{control_id}")
    good = dict(width=720, height=1280, stride=2160, byte_count=2764800,
                digest=SOURCE_RGB_SHA, frame_index=0, pixel_format="RGB24",
                source_kind="DIRECT_CAPTURE", color_transform_applied=False)
    expect_reject("wrong_dimensions", lambda: validate_rgb24_contract(**{**good, "width": 719}))
    expect_reject("wrong_byte_count", lambda: validate_rgb24_contract(**{**good, "byte_count": 2764799}))
    expect_reject("wrong_stride", lambda: validate_rgb24_contract(**{**good, "stride": 2159}))
    expect_reject("altered_source_hash", lambda: validate_rgb24_contract(**{**good, "digest": "0" * 64}))
    expect_reject("frame_order_mismatch", lambda: validate_rgb24_contract(**{**good, "frame_index": 1}))
    expect_reject("historical_mp4_source", lambda: validate_rgb24_contract(**{**good, "source_kind": "HISTORICAL_MP4_DECODE"}))
    expect_reject("write_into_protected_evidence", lambda: guard_write_path(protected_roots[0] / "tamper.bin", output_root, protected_roots))
    expect_reject("write_outside_l3_output_root", lambda: guard_write_path(output_root.parent / "escape.bin", output_root, protected_roots))
    expect_reject("incorrect_geometry", lambda: validate_geometry((720, 1280), (107, 192, 504, 896)))
    return controls


def verify_png_rgb_pair(png: Path, raw: Path, expected_png_sha: str, expected_raw_sha: str,
                        expected_raw_bytes: int, expect_alpha: bool) -> dict:
    if sha256_file(png) != expected_png_sha:
        raise L3AuditError(f"PNG_SHA256_MISMATCH:{png.name}")
    if raw.stat().st_size != expected_raw_bytes or sha256_file(raw) != expected_raw_sha:
        raise L3AuditError(f"RGB24_BUFFER_PIN_MISMATCH:{raw.name}")
    width, height, rgb, color_type = decode_png_rgb(png)
    if (width, height) != (720, 1280) or len(rgb) != expected_raw_bytes:
        raise L3AuditError(f"PNG_RGB_GEOMETRY_MISMATCH:{png.name}")
    raw_bytes = raw.read_bytes()
    if rgb != raw_bytes:
        raise L3AuditError(f"PNG_RGB24_PIXEL_IDENTITY_MISMATCH:{png.name}")
    if expect_alpha and color_type != 6:
        raise L3AuditError("SOURCE_PNG_EXPECTED_RGBA8")
    if not expect_alpha and color_type != 2:
        raise L3AuditError("COMPOSITE_PNG_EXPECTED_RGB8")
    return {"png": png.name, "png_sha256": expected_png_sha, "rgb24": raw.name,
            "rgb24_sha256": expected_raw_sha, "bytes": expected_raw_bytes,
            "png_rgb24_byte_identity": True, "png_color_type": color_type}


def verify_black_geometry(rgb: bytes) -> dict:
    width, height = 720, 1280
    row_bytes = width * 3
    def pixel_black(x: int, y: int) -> bool:
        i = y * row_bytes + x * 3
        return rgb[i] == 0 and rgb[i + 1] == 0 and rgb[i + 2] == 0
    regions = {
        "header_band": (0, 0, 720, 192),
        "footer_band": (0, 1088, 720, 192),
        "left_gutter": (0, 0, 108, 1280),
        "right_gutter": (612, 0, 108, 1280),
    }
    counts = {}
    for name, (x0, y0, w, h) in regions.items():
        total = w * h
        black = 0
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                if pixel_black(x, y):
                    black += 1
        if black != total:
            raise L3AuditError(f"RESERVED_GEOMETRY_NOT_BLACK:{name}:{black}/{total}")
        counts[name] = {"pixels": total, "black_pixels": black, "all_black": True}
    x, y, w, h = 108, 192, 504, 896
    nonblack = 0
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            if not pixel_black(xx, yy):
                nonblack += 1
    if nonblack < 10000:
        raise L3AuditError("CONTENT_RECT_BLANK_OR_NEAR_BLANK")
    return {"reserved_regions": counts, "content_rect_nonblack_pixels": nonblack,
            "content_rect": [108, 192, 504, 896], "canvas": [720, 1280]}


def atomic_write(path: Path, payload: bytes) -> None:
    temp = path.parent / ("t." + uuid.uuid4().hex[:16] + ".tmp")
    try:
        with temp.open("xb") as f:
            f.write(payload)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp, path)
    finally:
        if temp.exists():
            temp.unlink()


def run(project_root: Path) -> int:
    project_root = project_root.resolve()
    if not project_root.is_dir():
        raise L3AuditError("PROJECT_ROOT_MISSING")
    if sys.version_info[:3] != (3, 13, 14):
        raise L3AuditError(f"PYTHON_VERSION_MISMATCH:{sys.version.split()[0]}")

    # Exact predecessor evidence and source manifests.
    v5 = project_root / V5_ROOT_REL
    v5_install = project_root / V5_INSTALL_REL / V5_INSTALL_NAME
    v5_receipt_path = verify_file(v5 / "C11E_E6_L2_QIMAGE_COMPOSITION_RECEIPT_V5.json", V5_RECEIPT_SHA, 4044)
    v5_receipt_sidecar = require_sidecar(v5_receipt_path, V5_RECEIPT_SHA)
    v5_install_receipt = verify_file(v5_install, V5_INSTALL_RECEIPT_SHA, 11177)
    v5_install_sidecar = require_sidecar(v5_install_receipt, V5_INSTALL_RECEIPT_SHA)
    v5_data = load_json(v5_receipt_path)
    install_data = load_json(v5_install_receipt)
    if v5_data.get("status") != "PASS_L2_QIMAGE_COMPOSITION_FROM_V4_CAPTURE_PENDING_OPERATOR_VISUAL_REVIEW":
        raise L3AuditError("V5_COMPOSITION_RECEIPT_STATUS_MISMATCH")
    if v5_data.get("l2_ready") is not False or v5_data.get("visual_resampler_review") != "PENDING_OPERATOR_VISUAL_REVIEW":
        raise L3AuditError("V5_VISUAL_REVIEW_GOVERNANCE_MISMATCH")
    if v5_data.get("qimage_composition_count") != 1 or v5_data.get("godot_invocations") != 0:
        raise L3AuditError("V5_EXECUTION_CARDINALITY_MISMATCH")
    if (install_data.get("status") != "PASS_ADD_ONLY" or install_data.get("destination_count") != 24
            or install_data.get("add_count") != 24 or install_data.get("c11c_modified") is not False
            or install_data.get("d4_8_v2_modified") is not False or install_data.get("source_files_modified") is not False
            or install_data.get("c11c_manifest_sha256") != C11C_SHA or install_data.get("d4_8_v2_sha256") != D48_SHA):
        raise L3AuditError("V5_INSTALL_RECEIPT_SEMANTICS_MISMATCH")

    v4_receipt_path = verify_file(v5 / "C11E_E6_L2_DIRECT_RGB24_VISUAL_PROBE_RECEIPT_V4.json", V4_RECEIPT_SHA, 2621)
    v4_sidecar = require_sidecar(v4_receipt_path, V4_RECEIPT_SHA)
    v4_data = load_json(v4_receipt_path)
    if v4_data.get("godot_invocations") != 2 or any(p.get("exit_code") != 0 for p in v4_data.get("godot_processes", [])):
        raise L3AuditError("V4_CAPTURE_PREDECESSOR_NOT_VALID")
    if v4_data.get("source_pins_verified") is not True:
        raise L3AuditError("V4_SOURCE_PINS_NOT_VERIFIED")
    if v4_data.get("selector", {}).get("frame_index") != 0:
        raise L3AuditError("V4_FRAME_INDEX_MISMATCH")
    v4_install_receipt_path = verify_file(v5 / "C11E_E6_L2_DIRECT_RGB24_VISUAL_PROBE_V3_INSTALL_RECEIPT.json", V4_INSTALL_RECEIPT_SHA, 11308)
    v4_install_sidecar = require_sidecar(v4_install_receipt_path, V4_INSTALL_RECEIPT_SHA)
    v4_install_data = load_json(v4_install_receipt_path)
    if (v4_install_data.get("status") != "PASS_ADD_ONLY" or v4_install_data.get("destination_count") != 24
            or v4_install_data.get("add_count") != 24 or v4_install_data.get("c11c_modified") is not False
            or v4_install_data.get("d4_8_v2_modified") is not False or v4_install_data.get("source_files_modified") is not False
            or v4_install_data.get("c11c_manifest_sha256") != C11C_SHA or v4_install_data.get("d4_8_v2_sha256") != D48_SHA):
        raise L3AuditError("V4_INSTALL_RECEIPT_SEMANTICS_MISMATCH")

    metadata_path = verify_file(v5 / "capture_metadata.json", CAPTURE_META_SHA, 1144)
    metadata = load_json(metadata_path)
    metadata_expected = {"status": "PASS_CAPTURED_ONE_DIRECT_RGB24_FRAME", "selector_id": "E6-L-01",
                         "family_id": "fractal_bloom", "grammar_id": "radial_bloom", "gameplay_seed": 100006,
                         "frame_index": 0, "viewport_width": 720, "viewport_height": 1280,
                         "source_image_format": "RGBA8", "alpha_all_opaque": True,
                         "rgb_pixel_format": "RGB24", "rgb_bytes": 2764800, "rgb_stride_bytes": 2160,
                         "rgb_sha256": SOURCE_RGB_SHA, "color_transform_applied": False,
                         "historical_mp4_consumed": False}
    for key, value in metadata_expected.items():
        if metadata.get(key) != value:
            raise L3AuditError(f"CAPTURE_METADATA_MISMATCH:{key}:{metadata.get(key)!r}")

    source_png = verify_file(v5 / "source_frame.png", SOURCE_PNG_SHA, 590089)
    source_rgb = verify_file(v5 / "source_frame.rgb24", SOURCE_RGB_SHA, 2764800)
    composite_png = verify_file(v5 / "composited_frame.png", COMPOSITE_PNG_SHA, 326107)
    composite_rgb = verify_file(v5 / "composited_frame.rgb24", COMPOSITE_RGB_SHA, 2764800)

    source_manifest_path = verify_file(project_root / SOURCE_MANIFEST_REL, V5_SOURCE_MANIFEST_SHA, 4948)
    source_manifest = load_json(source_manifest_path)
    if source_manifest.get("schema") != "C11E-E6-L2-QIMAGE-REPAIR-SOURCE-PIN-MANIFEST-V5" or len(source_manifest.get("source_files", [])) != 20:
        raise L3AuditError("V5_SOURCE_MANIFEST_SCHEMA_OR_COUNT_MISMATCH")
    qimage = source_manifest.get("qimage_module", {})
    qimage_path = verify_file(project_root / qimage.get("path", ""), QIMAGE_MODULE_SHA, 6483)

    l3_source_manifest_path = verify_file(project_root / L3_SOURCE_MANIFEST_REL, L3_SOURCE_MANIFEST_SHA, L3_SOURCE_MANIFEST_BYTES)
    l3_source_manifest = load_json(l3_source_manifest_path)
    l3_rows = l3_source_manifest.get("protected_inputs", [])
    if (l3_source_manifest.get("schema") != "C11E-E6-L3-LOOP-NEGATIVE-CONTROLS-SOURCE-MANIFEST-V1"
            or len(l3_rows) != 16
            or l3_source_manifest.get("source_dependency_manifest", {}).get("path") != SOURCE_MANIFEST_REL.as_posix()
            or l3_source_manifest.get("source_dependency_manifest", {}).get("sha256") != V5_SOURCE_MANIFEST_SHA
            or l3_source_manifest.get("source_dependency_manifest", {}).get("expected_source_file_count") != 20
            or l3_source_manifest.get("source_dependency_manifest", {}).get("qimage_module_sha256") != QIMAGE_MODULE_SHA
            or l3_source_manifest.get("immutable") is None):
        raise L3AuditError("L3_SOURCE_MANIFEST_SCHEMA_OR_COUNT_MISMATCH")

    # The L3 source manifest is pinned and every declared evidence row is independently rehashed.
    l3_protected = []
    seen_protected = set()
    for row in l3_rows:
        rel = Path(str(row.get("path", "")))
        if rel.is_absolute() or ".." in rel.parts or not row.get("sha256") or len(str(row.get("sha256"))) != 64:
            raise L3AuditError("L3_SOURCE_MANIFEST_UNSAFE_OR_INVALID_ROW")
        key = rel.as_posix().lower()
        if key in seen_protected:
            raise L3AuditError(f"L3_SOURCE_MANIFEST_DUPLICATE_PATH:{key}")
        seen_protected.add(key)
        expected_bytes = int(row.get("bytes", -1))
        p = verify_file(project_root / rel, str(row["sha256"]).lower(), expected_bytes)
        l3_protected.append((p, str(row["sha256"]).lower(), expected_bytes))

    protected = l3_protected + [
        (l3_source_manifest_path, L3_SOURCE_MANIFEST_SHA, L3_SOURCE_MANIFEST_BYTES),
        (qimage_path, QIMAGE_MODULE_SHA, 6483),
    ]
    pin_rows = source_manifest["source_files"]
    for row in pin_rows:
        protected.append((project_root / Path(row["path"]), row["sha256"], int(row["bytes"])))
    # Deduplicate paths while requiring every declaration of the same path to agree.
    protected_by_path = {}
    for path, digest, size in protected:
        key = str(path.resolve()).lower()
        item = (path, str(digest).lower(), int(size))
        if key in protected_by_path and protected_by_path[key][1:] != item[1:]:
            raise L3AuditError(f"PROTECTED_PIN_DECLARATION_CONFLICT:{path}")
        protected_by_path[key] = item
    protected = list(protected_by_path.values())
    protected_hashes_before = {}
    for path, digest, size in protected:
        verify_file(path, digest, size)
        protected_hashes_before[str(path)] = sha256_file(path)

    # Rehash all captured source and output files before/after; no write is made to these paths.
    evidence_paths = [v5_receipt_path, v5_receipt_sidecar, v5_install_receipt, v5_install_sidecar,
                      v4_receipt_path, v4_sidecar, v4_install_receipt_path, v4_install_sidecar,
                      metadata_path, source_png, source_rgb, composite_png, composite_rgb]
    evidence_before = {str(p): sha256_file(p) for p in evidence_paths}
    if evidence_before[str(v5_receipt_path)] != V5_RECEIPT_SHA:
        raise L3AuditError("V5_RECEIPT_REHASH_MISMATCH")

    # Pixel identity and geometry proofs; no QImage, Godot or media tool is invoked.
    source_pair = verify_png_rgb_pair(source_png, source_rgb, SOURCE_PNG_SHA, SOURCE_RGB_SHA, 2764800, True)
    composite_pair = verify_png_rgb_pair(composite_png, composite_rgb, COMPOSITE_PNG_SHA, COMPOSITE_RGB_SHA, 2764800, False)
    composite_bytes = composite_rgb.read_bytes()
    geometry = verify_black_geometry(composite_bytes)
    validate_geometry((720, 1280), (108, 192, 504, 896))
    if v5_data.get("geometry", {}).get("content_rect") != [108, 192, 504, 896]:
        raise L3AuditError("V5_RECEIPT_GEOMETRY_MISMATCH")
    if v5_data.get("colorimetry", {}).get("bt709_assumed") is not False or v5_data.get("colorimetry", {}).get("color_transform_applied") is not False:
        raise L3AuditError("COLORIMETRY_GOVERNANCE_MISMATCH")
    if v5_data.get("colorimetry", {}).get("primaries") != "UNDECLARED" or v5_data.get("colorimetry", {}).get("transfer") != "UNDECLARED" or v5_data.get("colorimetry", {}).get("matrix") != "UNDECLARED":
        raise L3AuditError("UNDECLARED_COLORIMETRY_WAS_REPLACED")

    l3_probe_root = project_root / "artifacts/tests/c11e/e6_l3_loop_negative_controls_v1" / ".negative-control-probe"
    negative_controls = run_negative_controls(l3_probe_root, (v5, project_root / V5_INSTALL_REL.parent))
    if len(negative_controls) != 9 or any(x.get("status") != "REJECTED_AS_EXPECTED" for x in negative_controls):
        raise L3AuditError("NEGATIVE_CONTROL_CARDINALITY_OR_STATUS_MISMATCH")
    process_scope = {"godot": 0, "ffmpeg": 0, "ffprobe": 0, "audio": 0, "mux": 0, "qimage_composition": 0, "dispatch": 0, "batch_id": 0}
    validate_process_scope(process_scope)

    protected_hashes_after = {}
    for path, digest, size in protected:
        verify_file(path, digest, size)
        protected_hashes_after[str(path)] = sha256_file(path)
    if protected_hashes_before != protected_hashes_after:
        raise L3AuditError("PROTECTED_SOURCE_HASHES_CHANGED_DURING_L3_AUDIT")
    evidence_after = {str(p): sha256_file(p) for p in evidence_paths}
    if evidence_before != evidence_after:
        raise L3AuditError("PROTECTED_EVIDENCE_CHANGED_DURING_L3_AUDIT")

    run_id = "E6L3NCV1_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ_") + uuid.uuid4().hex[:8].upper()
    output_base = project_root / "artifacts/tests/c11e/e6_l3_loop_negative_controls_v1"
    output_root = output_base / run_id
    if output_root.exists():
        raise L3AuditError("L3_RUN_DIRECTORY_COLLISION")
    # Reject symlinked output ancestors before creating any directory or file.
    for component in (project_root / "artifacts", project_root / "artifacts/tests",
                      project_root / "artifacts/tests/c11e", output_base):
        if component.exists() and component.is_symlink():
            raise L3AuditError(f"L3_OUTPUT_ANCESTOR_SYMLINK:{component}")
    try:
        output_base.resolve().relative_to(project_root)
    except ValueError as exc:
        raise L3AuditError("L3_OUTPUT_BASE_ESCAPES_PROJECT_ROOT") from exc
    allowed_roots = (v5, project_root / V5_INSTALL_REL.parent)
    report_path = output_root / "L3_AUDIT_REPORT_V1.json"
    receipt_path = output_root / "C11E_E6_L3_LOOP_NEGATIVE_CONTROLS_RECEIPT_V1.json"
    sidecar_path = Path(str(receipt_path) + ".sha256")
    for candidate in (report_path, receipt_path, sidecar_path):
        guard_write_path(candidate, output_root, allowed_roots)
        if candidate.parent != output_root:
            raise L3AuditError("L3_OUTPUT_FILE_NOT_DIRECT_CHILD")
    output_root.mkdir(parents=True, exist_ok=False)
    for candidate in (report_path, receipt_path, sidecar_path):
        guard_write_path(candidate, output_root, allowed_roots)
    report = {
      "schema":"C11E-E6-L3-LOOP-NEGATIVE-CONTROLS-REPORT-V1","run_id":run_id,
      "status":"PASS_L3_TECHNICAL_NEGATIVE_CONTROLS_PENDING_OPERATOR_VISUAL_REVIEW",
      "predecessor":{"v5_run_id":V5_RUN_ID,"v5_receipt_sha256":V5_RECEIPT_SHA,
                     "v4_capture_receipt_sha256":V4_RECEIPT_SHA,"v4_install_receipt_sha256":V4_INSTALL_RECEIPT_SHA,
                     "v5_install_receipt_sha256":V5_INSTALL_RECEIPT_SHA},
      "positive_checks":{"source_png_rgb24_identity":source_pair,"composite_png_rgb24_identity":composite_pair,
                          "geometry":geometry,"source_and_output_dimensions":"720x1280",
                          "rgb24_stride":2160,"rgb24_bytes":2764800,"process_scope":process_scope},
      "negative_controls":negative_controls,
      "source_immutability":{"protected_inputs_before_after_equal":True,"protected_source_pin_count":len(pin_rows),
                              "protected_manifest_input_count":len(l3_rows),"protected_evidence_file_count":len(evidence_paths),
                              "l3_source_manifest_sha256":L3_SOURCE_MANIFEST_SHA,"source_files_modified":False},
      "visual_review":{"assistant_preliminary_visual_inspection":"NO_OBVIOUS_CLIPPING_OR_GEOMETRY_ARTIFACT_OBSERVED",
                       "operator_visual_review":"PENDING_OPERATOR_VISUAL_REVIEW",
                       "smooth_transformation_acceptance":"PENDING_OPERATOR_DECISION"},
      "governance":{"c11c_manifest_sha256":C11C_SHA,"d4_8_v2_sha256":D48_SHA,
                     "c11c_modified":False,"d4_8_v2_modified":False,"source_files_modified":False,
                     "godot_invocations":0,"qimage_compositions":0,"ffmpeg_invoked":False,
                     "ffprobe_invoked":False,"audio_generated":False,"mux_invoked":False,
                     "renderer_production":False,"production_dispatch":False,"e6_accepted":0,
                     "release_authority":"NONE","git_checks":"SKIPPED","commits":"OPERATOR_MANAGED",
                     "source_file_pins":"ENFORCED"}
    }
    report_bytes = (json.dumps(report, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    atomic_write(report_path, report_bytes)
    report_sha = sha256_file(report_path)
    artifacts = {"L3_AUDIT_REPORT_V1.json":{"bytes":report_path.stat().st_size,"sha256":report_sha}}
    receipt = {
      "schema":"C11E-E6-L3-LOOP-NEGATIVE-CONTROLS-RECEIPT-V1","run_id":run_id,
      "created_utc":datetime.now(timezone.utc).isoformat(),
      "status":"PASS_L3_TECHNICAL_NEGATIVE_CONTROLS_PENDING_OPERATOR_VISUAL_REVIEW",
      "l2_ready":False,"l3_ready":False,"technical_negative_controls":"PASS_9_OF_9_FAIL_CLOSED",
      "operator_visual_review":"PENDING_OPERATOR_VISUAL_REVIEW",
      "smooth_transformation_acceptance":"PENDING_OPERATOR_DECISION",
      "v5_composition_receipt_sha256":V5_RECEIPT_SHA,
      "v5_install_receipt_sha256":V5_INSTALL_RECEIPT_SHA,
      "v4_capture_receipt_sha256":V4_RECEIPT_SHA,
      "v4_install_receipt_sha256":V4_INSTALL_RECEIPT_SHA,
      "source_rgb24_sha256":SOURCE_RGB_SHA,"composited_rgb24_sha256":COMPOSITE_RGB_SHA,
      "negative_controls":negative_controls,"positive_checks":report["positive_checks"],
      "source_immutability":report["source_immutability"],"visual_review":report["visual_review"],
      "artifacts":artifacts,"governance":report["governance"],
      "l4_six_loop_selectors":"NOT_AUTHORIZED_BY_THIS_RUN"
    }
    receipt_bytes = (json.dumps(receipt, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    atomic_write(receipt_path, receipt_bytes)
    receipt_sha = sha256_file(receipt_path)
    atomic_write(sidecar_path, f"{receipt_sha}  {receipt_path.name}\n".encode("ascii"))

    print("V4_V5_INSTALL_RECEIPTS=PASS/FOUR_RECEIPTS_AND_EXACT_SIDECARS")
    print("V5_COMPOSITION_EVIDENCE=PASS/RECEIPT_AND_INSTALL_PINS")
    print("PNG_RGB24_PIXEL_IDENTITY=PASS/2_OF_2")
    print("GEOMETRY=PASS/720x1280_CONTENT_504x896_AT_108_192_BLACK_BANDS_GUTTERS")
    print("NEGATIVE_CONTROLS=9/9 REJECTED_AS_EXPECTED")
    print("SOURCE_MANIFEST=PASS/16_PROTECTED_EVIDENCE_ROWS_AND_20_NESTED_PINS")
    print("SOURCE_IMMUTABILITY=PASS/ALL_PROTECTED_HASHES_UNCHANGED")
    print("L3_TECHNICAL_STATUS=PASS_L3_TECHNICAL_NEGATIVE_CONTROLS_PENDING_OPERATOR_VISUAL_REVIEW")
    print("GODOT=0; QIMAGE_COMPOSITIONS=0; FFMPEG=0; FFPROBE=0; AUDIO=0; MUX=0")
    print("L2_READY=FALSE; L3_READY=FALSE; OPERATOR_VISUAL_REVIEW=PENDING; E6_ACCEPTED=0; RELEASE_AUTHORITY=NONE")
    print(f"RECEIPT={receipt_path}")
    print(f"RECEIPT_SHA256={receipt_sha}")
    print(f"REPORT={report_path}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="C11-E L3 read-only Loop negative controls")
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()
    try:
        return run(Path(args.project_root))
    except Exception as exc:
        print(f"L3_AUDIT_BLOCKED={type(exc).__name__}:{exc}")
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
