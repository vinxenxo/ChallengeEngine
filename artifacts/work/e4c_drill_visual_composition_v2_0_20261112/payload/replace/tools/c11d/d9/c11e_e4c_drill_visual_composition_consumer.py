"""D-owned Visual Drill V2 consumer with social-body pixel identity.

GAME copies only PresentationProfile.get_social_regions().body_rect into the
720x1280 REVIEW_720 body, without scaling or interpolation. PRE_ROLL and END_CTA
are full-frame native passthrough. This module never launches C11-C, Godot,
FFmpeg, audio generation, or production renderer dispatch.
"""
from __future__ import annotations

import hashlib
from functools import lru_cache
import json
import math
import os
import struct
import sys
import unicodedata
from pathlib import Path
from typing import Any, Mapping

from PySide6.QtCore import QPoint, QPointF, Qt
from PySide6.QtGui import (
    QColor,
    QFont,
    QFontDatabase,
    QFontInfo,
    QFontMetricsF,
    QGuiApplication,
    QImage,
    QPainter,
    QRawFont,
)

COMPOSITION_PROPOSAL_REL = "definitions/c11d/production/C11E_E4C_DRILL_EDITORIAL_COMPOSITION_PROPOSAL_V2.json"
COMPOSITION_SCHEMA_REL = "definitions/c11d/production/C11E_E4C_DRILL_EDITORIAL_COMPOSITION_PROPOSAL_SCHEMA_V2.json"
TIMEBASE_PROPOSAL_REL = "definitions/c11d/production/C11E_E4C_DRILL_PRESENTATION_TIMEBASE_PROPOSAL_V1.json"
TIMEBASE_SCHEMA_REL = "definitions/c11d/production/C11E_E4C_DRILL_PRESENTATION_TIMEBASE_PROPOSAL_SCHEMA_V1.json"
DECISION_REL = "docs/current/e/C11E_E4C_DRILL_COMPOSITION_OPERATOR_DECISION_RECORD_20261112_V2.json"
INTER_FONT_REL = "assets/fonts/Inter-Bold.otf"
MONO_FONT_REL = "assets/fonts/NotoSansMono-Regular.ttf"
PRESENTATION_PROFILE_REL = "core/presentation/PresentationProfile.gd"
PRESENTATION_PROFILE_SHA = "187b1cf8ab96b9031785a0f36b0054a60383c97cb3d81906c7d9bbcd373bef24"

# Exact REVIEW_720 projection of PresentationProfile.get_social_regions().
# The canvas carries aspect_ratio metadata in addition to its rectangle fields.
# Keep this as the single geometry oracle for both proposal and plan validation.
EXPECTED_SOCIAL_REGIONS = {
    "canvas": {"x": 0, "y": 0, "width": 720, "height": 1280, "aspect_ratio": "9:16"},
    "header_rect": {"x": 0, "y": 0, "width": 720, "height": 192},
    "body_rect": {"x": 0, "y": 192, "width": 720, "height": 896},
    "footer_rect": {"x": 0, "y": 1088, "width": 720, "height": 192},
}

COMPOSITION_SHA = "700447531e299be44d119c52caa44ee797ec00fbad6a0d7a08ad5bbeff82b5e2"
COMPOSITION_SCHEMA_SHA = "9de12b1ede0849de14446af50345769502165dc7a2191aca71f20702fb855baa"
TIMEBASE_SHA = "44ab3b0fa09a6f7d42cd8cf2f1122cada6cbffe16a7a6b53c2af5e88d5daddc8"
TIMEBASE_SCHEMA_SHA = "c5cedcd749a6702dc47b1de0bd67c57721bb9a06cee5cb3709cdc1b17d8a6806"
DECISION_SHA = "bceef9a22c27447ccbef5487339c25626e4cb4c5d32509809b832411655914e8"
FONT_PINS = {
    INTER_FONT_REL: "9fc6261e817d0b1b2bf1953d8799bb1c837d11aeebbf83ae352e7b4d6de6425d",
    MONO_FONT_REL: "6b692c4b6d15ccf59f1c1fe8d11cb8a92f51960f3e9f1f523781755a3af7e29f",
}
DRILL_FAMILIES = ("tracking", "pursuit", "saccade", "peripheral_scan")
DRILL_TIERS = tuple(f"tier-{n}" for n in range(1, 6))
EXPECTED_MUSIC_PROFILES = {
    "tracking": "FLOWING_VECTOR",
    "pursuit": "ORGANIC_BLOOM",
    "saccade": "CIRCUIT_PULSE",
    "peripheral_scan": "ORBITAL_RITUAL",
}

class DrillVisualConsumerError(ValueError):
    """A malformed or out-of-scope Visual Drill composition request."""


_QT_APP = None
_QT_FONT_IDS: dict[str, int] = {}
_QT_FONT_FAMILIES: dict[str, str] = {}


def _ensure_qt_app():
    """Reuse the Producer's existing QGuiApplication or create a test-only one."""
    global _QT_APP
    app = QGuiApplication.instance()
    if app is None:
        if os.name != "nt":
            os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
        _QT_APP = QGuiApplication(["C11E-E4C-DRILL-VISUAL-CONSUMER"])
        app = _QT_APP
    return app


def _image_rgb_bytes(image: QImage) -> bytes:
    """Return stable RGB888 bytes for the fixed 720/504 pixel-width frames."""
    rgb = image.convertToFormat(QImage.Format.Format_RGB888)
    bits = rgb.constBits()
    try:
        bits.setsize(rgb.sizeInBytes())
    except AttributeError:
        # Current PySide6 exposes constBits as a sized memoryview; older
        # bindings expose a pointer requiring setsize. Support both safely.
        pass
    raw = bytes(bits)
    expected = int(rgb.sizeInBytes())
    if len(raw) < expected:
        raise DrillVisualConsumerError(f"Qt RGB buffer shorter than QImage storage: {len(raw)} < {expected}")
    return raw[:expected]


def _image_rgb_sha256(image: QImage) -> str:
    return _sha_bytes(_image_rgb_bytes(image))


def _pixel_rgb(image: QImage, x: int, y: int) -> tuple[int, int, int]:
    color = image.pixelColor(x, y)
    return color.red(), color.green(), color.blue()


def _sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha_file(path: Path) -> str:
    if not path.is_file():
        raise DrillVisualConsumerError(f"required source file missing: {path}")
    return _sha_bytes(path.read_bytes())


def _canonical(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _canonical(value[key]) for key in sorted(value, key=lambda x: str(x))}
    if isinstance(value, (list, tuple)):
        return [_canonical(x) for x in value]
    return value


def _json_sha(value: Any) -> str:
    payload = json.dumps(_canonical(value), ensure_ascii=False, separators=(",", ":"), allow_nan=False)
    return _sha_bytes(payload.encode("utf-8"))


def _read_json(root: Path, relative: str) -> dict[str, Any]:
    path = root / Path(*relative.split("/"))
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise DrillVisualConsumerError(f"cannot read JSON {relative}: {exc}") from exc
    if not isinstance(value, dict):
        raise DrillVisualConsumerError(f"JSON root must be an object: {relative}")
    return value


def _verify_decision_and_proposals(root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    composition = _read_json(root, COMPOSITION_PROPOSAL_REL)
    composition_schema = _read_json(root, COMPOSITION_SCHEMA_REL)
    timebase = _read_json(root, TIMEBASE_PROPOSAL_REL)
    timebase_schema = _read_json(root, TIMEBASE_SCHEMA_REL)
    decision = _read_json(root, DECISION_REL)
    expected = (
        (COMPOSITION_PROPOSAL_REL, COMPOSITION_SHA),
        (COMPOSITION_SCHEMA_REL, COMPOSITION_SCHEMA_SHA),
        (TIMEBASE_PROPOSAL_REL, TIMEBASE_SHA),
        (TIMEBASE_SCHEMA_REL, TIMEBASE_SCHEMA_SHA),
        (DECISION_REL, DECISION_SHA),
        (PRESENTATION_PROFILE_REL, PRESENTATION_PROFILE_SHA),
    )
    for relative, digest in expected:
        if _sha_file(root / relative) != digest:
            raise DrillVisualConsumerError(f"approved V2 design/source pin mismatch: {relative}")
    if decision.get("decision_semantics") != "USER_DIRECTED_V2_D_OWNED_CONTRACT_AND_ISOLATED_REQUALIFICATION_ONLY":
        raise DrillVisualConsumerError("V2 user decision does not have the exact D-owned scope")
    if decision.get("c11c_frozen_baseline_sha256") != "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953":
        raise DrillVisualConsumerError("V2 decision references another C11-C baseline")
    expected_decisions = {
        "E4C_DRILL_SOCIAL_BODY_PIXEL_EXACT_GEOMETRY": COMPOSITION_SHA,
        "E4C_DRILL_GAME_TO_FINAL_PRESENTATION_TIMEBASE": TIMEBASE_SHA,
    }
    actual = {row.get("decision_id"): row for row in decision.get("decisions", []) if isinstance(row, Mapping)}
    for decision_id, digest in expected_decisions.items():
        row = actual.get(decision_id)
        if not isinstance(row, Mapping) or row.get("decision") != "USER_DIRECTED_APPROVE_D_OWNED_V2" or row.get("proposal_sha256") != digest:
            raise DrillVisualConsumerError(f"missing exact V2 user direction: {decision_id}")
    scope = decision.get("scope_boundary", {})
    required_false = (
        "renderer_native_input_emission_authorized", "renderer_activation_authorized",
        "production_dispatch_authorized", "production_media_creation_authorized",
        "new_native_capture_authorized", "audio_generation_authorized",
        "audio_payload_materialization_authorized", "release_promotion_authorized",
        "c11c_source_or_mechanics_mutation_authorized",
    )
    for key in required_false:
        if scope.get(key) is not False:
            raise DrillVisualConsumerError(f"V2 decision unexpectedly authorizes {key}")
    if scope.get("d_only_design_and_contract_implementation_authorized") is not True:
        raise DrillVisualConsumerError("V2 D-owned design implementation is not explicitly authorized")
    if scope.get("isolated_requalification_from_existing_captured_media_authorized") is not True:
        raise DrillVisualConsumerError("V2 existing-media isolated requalification is not authorized")
    if composition.get("status") != "USER_DIRECTED_D_OWNED_V2_CONTRACT" or timebase.get("status") != "PROPOSED_NOT_APPROVED_NOT_RENDERER_INPUT":
        raise DrillVisualConsumerError("V2 composition approval or immutable V1 timebase status changed")
    geometry = composition.get("geometry", {})
    for key, expected_region in EXPECTED_SOCIAL_REGIONS.items():
        if geometry.get(key) != expected_region:
            raise DrillVisualConsumerError(f"V2 social-region geometry mismatch: {key}")

    # Verify that the 720x1280 delivery rectangles are the exact 4:3 projection
    # of the frozen 540x960 logical PresentationProfile social regions. This
    # proves the output-space crop coordinates instead of trusting duplicated
    # proposal constants.
    source_geometry = geometry.get("source_geometry_authority", {})
    if source_geometry.get("logical_source_canvas") != {"width": 540, "height": 960}:
        raise DrillVisualConsumerError("V2 logical PresentationProfile canvas mismatch")
    if source_geometry.get("header_ratio") != 0.15 or source_geometry.get("footer_ratio") != 0.15 or source_geometry.get("body_ratio") != 0.7:
        raise DrillVisualConsumerError("V2 PresentationProfile social-region ratios mismatch")
    expected_scale = 720.0 / 540.0
    if not math.isclose(float(source_geometry.get("pixel_scale", -1)), expected_scale, rel_tol=0.0, abs_tol=1e-12):
        raise DrillVisualConsumerError("V2 PresentationProfile to REVIEW_720 pixel scale mismatch")
    transform = geometry.get("source_frame_transform", {})
    if transform.get("mode") != "PIXEL_EXACT_BODY_CROP" or transform.get("scale") != 1.0 or transform.get("interpolation") is not False:
        raise DrillVisualConsumerError("V2 must use pixel-exact body crop without scaling/interpolation")
    return composition, composition_schema, timebase, timebase_schema


def _validate_intent(root: Path, intent: Mapping[str, Any]) -> dict[str, Any]:
    if intent.get("schema_version") != "1.3" or intent.get("request", {}).get("content_type") != "visual_drills":
        raise DrillVisualConsumerError("consumer requires a schema 1.3 E1 Visual Drill intent")
    unsigned_intent = dict(intent)
    supplied_intent_sha = unsigned_intent.pop("intent_sha256", None)
    if supplied_intent_sha != _json_sha(unsigned_intent):
        raise DrillVisualConsumerError("E1 intent self-hash mismatch")
    sys.path.insert(0, str(root / "c11c-suite" / "c11c-producer"))
    try:
        import c11e_production_service
        validation = c11e_production_service.validate_c11e_production_intent(intent, root)
    except Exception as exc:
        raise DrillVisualConsumerError(f"existing E1 shared service rejected the Drill intent: {exc}") from exc
    finally:
        with_context = str(root / "c11c-suite" / "c11c-producer")
        if with_context in sys.path:
            sys.path.remove(with_context)
    if validation.get("status") != "PASS_E1_PREPARATION_ONLY":
        raise DrillVisualConsumerError("existing E1 shared service did not validate the Drill intent")
    preparation = intent.get("d9_boundary_preparation")
    if not isinstance(preparation, Mapping) or preparation.get("status") != "DRILL_FAMILY_STAGE_PREPARED_NOT_DISPATCHABLE":
        raise DrillVisualConsumerError("E1 Drill boundary preparation missing or dispatchable")
    for key, record_key in (
        ("preparation_sha256", "preparation_sha256"),
    ):
        unsigned = {k: v for k, v in preparation.items() if k != record_key}
        if preparation.get(record_key) != _json_sha(unsigned):
            raise DrillVisualConsumerError("E1 Drill preparation self-hash mismatch")
    return dict(preparation)


@lru_cache(maxsize=8)
def _font_codepoints(path: Path) -> set[int]:
    """Read TrueType/OpenType cmap tables (format 4/12) without third-party font tooling."""
    data = path.read_bytes()
    if len(data) < 12:
        raise DrillVisualConsumerError(f"invalid font file: {path}")
    num_tables = struct.unpack_from(">H", data, 4)[0]
    cmap_offset = cmap_length = None
    for index in range(num_tables):
        pos = 12 + index * 16
        if pos + 16 > len(data):
            break
        tag = data[pos:pos + 4]
        offset, length = struct.unpack_from(">II", data, pos + 8)
        if tag == b"cmap":
            cmap_offset, cmap_length = offset, length
            break
    if cmap_offset is None or cmap_offset + cmap_length > len(data):
        raise DrillVisualConsumerError(f"font has no valid cmap table: {path}")
    cmap = data[cmap_offset:cmap_offset + cmap_length]
    num_records = struct.unpack_from(">H", cmap, 2)[0]
    subtables: list[tuple[int, int]] = []
    for index in range(num_records):
        pos = 4 + index * 8
        if pos + 8 > len(cmap):
            break
        offset = struct.unpack_from(">I", cmap, pos + 4)[0]
        if offset + 2 <= len(cmap):
            fmt = struct.unpack_from(">H", cmap, offset)[0]
            subtables.append((fmt, offset))
    supported: set[int] = set()
    # Format 12 first; covers all Unicode scalar values.
    for fmt, offset in subtables:
        if fmt != 12 or offset + 16 > len(cmap):
            continue
        length = struct.unpack_from(">I", cmap, offset + 4)[0]
        groups = struct.unpack_from(">I", cmap, offset + 12)[0]
        if offset + length > len(cmap) or groups > (length - 16) // 12:
            raise DrillVisualConsumerError(f"malformed format-12 cmap: {path}")
        for index in range(groups):
            start, end, glyph = struct.unpack_from(">III", cmap, offset + 16 + index * 12)
            if glyph == 0 and start == end:
                continue
            supported.update(range(start + (1 if glyph == 0 else 0), end + 1))
    # Format 4 for BMP characters; only add characters which map to nonzero glyphs.
    for fmt, offset in subtables:
        if fmt != 4 or offset + 16 > len(cmap):
            continue
        length, seg_count_x2 = struct.unpack_from(">HH", cmap, offset + 2)
        seg_count = seg_count_x2 // 2
        if not seg_count or offset + length > len(cmap):
            continue
        end_base = offset + 14
        start_base = offset + 16 + 2 * seg_count
        delta_base = start_base + 2 * seg_count
        range_base = delta_base + 2 * seg_count
        for cp in range(0x10000):
            end_index = None
            for i in range(seg_count):
                end_code = struct.unpack_from(">H", cmap, end_base + 2 * i)[0]
                start_code = struct.unpack_from(">H", cmap, start_base + 2 * i)[0]
                if start_code <= cp <= end_code:
                    end_index = (i, start_code)
                    break
            if end_index is None:
                continue
            i, start_code = end_index
            delta = struct.unpack_from(">h", cmap, delta_base + 2 * i)[0]
            range_offset = struct.unpack_from(">H", cmap, range_base + 2 * i)[0]
            if range_offset == 0:
                glyph = (cp + delta) & 0xFFFF
            else:
                glyph_pos = range_base + 2 * i + range_offset + 2 * (cp - start_code)
                if glyph_pos + 2 > offset + length:
                    continue
                glyph = struct.unpack_from(">H", cmap, glyph_pos)[0]
                if glyph:
                    glyph = (glyph + delta) & 0xFFFF
            if glyph:
                supported.add(cp)
    return supported


@lru_cache(maxsize=16)
def _font(root: Path, relative: str, size: int) -> QFont:
    """Load the exact pinned font through the Producer's existing Qt font engine."""
    _ensure_qt_app()
    path = root / Path(*relative.split("/"))
    expected = FONT_PINS.get(relative)
    if expected is None or _sha_file(path) != expected:
        raise DrillVisualConsumerError(f"font asset pin mismatch: {relative}")
    if relative not in _QT_FONT_FAMILIES:
        font_id = QFontDatabase.addApplicationFont(str(path))
        if font_id < 0:
            raise DrillVisualConsumerError(f"Qt cannot register the pinned font: {relative}")
        families = QFontDatabase.applicationFontFamilies(font_id)
        if not families:
            raise DrillVisualConsumerError(f"Qt returned no family for pinned font: {relative}")
        _QT_FONT_IDS[relative] = font_id
        _QT_FONT_FAMILIES[relative] = str(families[0])
    family = _QT_FONT_FAMILIES[relative]
    font = QFont(family)
    font.setPixelSize(int(size))
    font.setWeight(QFont.Weight.Bold if relative == INTER_FONT_REL else QFont.Weight.Normal)
    info = QFontInfo(font)
    raw = QRawFont.fromFont(font)
    if not raw.isValid() or info.family().casefold() != family.casefold() or raw.familyName().casefold() != family.casefold():
        raise DrillVisualConsumerError(f"Qt font resolution did not select the pinned family: {relative}")
    return font


def _text_advance(font: QFont, text: str) -> float:
    """Measure fully laid-out text using Qt's shaping-aware font metrics."""
    return float(QFontMetricsF(font).horizontalAdvance(text))

def _filtered_fields(editorial: Mapping[str, Any]) -> dict[str, str]:
    visible: dict[str, str] = {}
    for key in ("title", "subtitle", "call_to_action"):
        raw = editorial.get(key, "")
        if raw is None:
            continue
        if not isinstance(raw, str):
            raise DrillVisualConsumerError(f"editorial field must remain a string: {key}")
        if len(raw) > 160:
            raise DrillVisualConsumerError(f"editorial field exceeds 160 codepoints: {key}")
        if raw.strip() and raw.strip().casefold() != "unknown":
            visible[key] = raw.strip()
    return visible


def _round_frames(seconds: float, fps_num: int, fps_den: int) -> int:
    if fps_num <= 0 or fps_den <= 0:
        raise DrillVisualConsumerError("FPS numerator and denominator must be positive")
    value = seconds * fps_num / fps_den
    return int(math.floor(value + 0.5))


def map_phase_frame(phase: str, player_frame_index: int, gameplay_frame_count: int, fps_num: int = 30, fps_den: int = 1) -> dict[str, Any]:
    """Map native player phase/index to final output index; never infer phase from index."""
    if isinstance(player_frame_index, bool) or not isinstance(player_frame_index, int):
        raise DrillVisualConsumerError("player_frame_index must be an integer")
    if isinstance(gameplay_frame_count, bool) or not isinstance(gameplay_frame_count, int) or gameplay_frame_count <= 0:
        raise DrillVisualConsumerError("gameplay_frame_count must be a positive integer")
    pre = _round_frames(3.0, fps_num, fps_den)
    end = _round_frames(3.0, fps_num, fps_den)
    total = pre + gameplay_frame_count + end
    if phase == "PRE_ROLL":
        if not 0 <= player_frame_index < pre:
            raise DrillVisualConsumerError("PRE_ROLL index outside native phase range")
        return {"phase": phase, "final_presentation_frame_index": player_frame_index, "source_frame_index": 0, "d_editorial_visible": False, "pre_roll_frames": pre, "gameplay_frames": gameplay_frame_count, "end_cta_frames": end, "total_frames": total}
    if phase == "GAME":
        if not 0 <= player_frame_index < gameplay_frame_count:
            raise DrillVisualConsumerError("GAME payload index outside [0, gameplay_frame_count)")
        return {"phase": phase, "final_presentation_frame_index": pre + player_frame_index, "source_frame_index": player_frame_index, "d_editorial_visible": True, "pre_roll_frames": pre, "gameplay_frames": gameplay_frame_count, "end_cta_frames": end, "total_frames": total}
    if phase == "END_CTA":
        if not pre + gameplay_frame_count <= player_frame_index < total:
            raise DrillVisualConsumerError("END_CTA index outside native final-stream phase range")
        return {"phase": phase, "final_presentation_frame_index": player_frame_index, "source_frame_index": gameplay_frame_count - 1, "d_editorial_visible": False, "pre_roll_frames": pre, "gameplay_frames": gameplay_frame_count, "end_cta_frames": end, "total_frames": total}
    if phase == "DONE":
        return {"phase": phase, "final_presentation_frame_index": None, "source_frame_index": None, "d_editorial_visible": False, "pre_roll_frames": pre, "gameplay_frames": gameplay_frame_count, "end_cta_frames": end, "total_frames": total}
    raise DrillVisualConsumerError(f"unknown native Drill phase: {phase}")


def build_composition_plan(intent: Mapping[str, Any], project_root: Path | str) -> dict[str, Any]:
    root = Path(project_root).resolve()
    if not root.is_dir():
        raise DrillVisualConsumerError(f"project root does not exist: {root}")
    preparation = _validate_intent(root, intent)
    composition, composition_schema, timebase, timebase_schema = _verify_decision_and_proposals(root)
    stage = preparation.get("drill_family_stage_contract", {})
    request = intent.get("request", {})
    selection = request.get("selection", {})
    family_id = selection.get("family_id")
    variant_id = selection.get("variant_id")
    if family_id not in DRILL_FAMILIES or variant_id not in DRILL_TIERS:
        raise DrillVisualConsumerError("E1 selector outside the exact 20-selector Drill V2 matrix")
    if stage.get("content_identity", {}).get("family_id") != family_id or stage.get("content_identity", {}).get("variant_id") != variant_id:
        raise DrillVisualConsumerError("E1 stage selector and request selector differ")
    expected_profile = EXPECTED_MUSIC_PROFILES[family_id]
    if stage.get("native_family_music", {}).get("profile_id") != expected_profile:
        raise DrillVisualConsumerError("C11-C FAMILY_MUSIC_V4 profile mismatch for selected Drill family")
    phase_contract = preparation.get("native_phase_and_end_cta_contract", {})
    phase_rows = phase_contract.get("phase_sequence", [])
    if [row.get("phase") for row in phase_rows] != ["PRE_ROLL", "GAME", "END_CTA", "DONE"]:
        raise DrillVisualConsumerError("native phase sequence has changed")
    if phase_contract.get("end_cta_precedence", {}).get("native_cta_header_authoritative") is not True or phase_contract.get("end_cta_precedence", {}).get("d_adapter_may_override_native_cta") is not False:
        raise DrillVisualConsumerError("native C11-C END_CTA precedence changed")
    editor = intent.get("editorial", {})
    fields = _filtered_fields(editor)
    geometry = composition["geometry"]
    source_pin_rows = intent.get("source_identity", {}).get("source_pins", [])
    profile_rows = [row for row in source_pin_rows if isinstance(row, Mapping) and row.get("path") == PRESENTATION_PROFILE_REL]
    if len(profile_rows) != 1 or profile_rows[0].get("sha256") != PRESENTATION_PROFILE_SHA or profile_rows[0].get("bytes") != 8837:
        raise DrillVisualConsumerError("E1 intent does not include the exact pinned PresentationProfile.gd social geometry source")
    font_hashes = {rel: _sha_file(root / rel) for rel in FONT_PINS}
    plan = {
        "schema": "C11E-E4C-DRILL-VISUAL-COMPOSITION-PLAN-V2",
        "status": "D_OWNED_V2_SOCIAL_BODY_CONSUMER_READY_FOR_ISOLATED_REQUALIFICATION",
        "intent_identity": {
            "request_id": request.get("request_id"),
            "request_hash": intent.get("identity", {}).get("request_hash"),
            "editorial_hash": intent.get("identity", {}).get("editorial_hash"),
            "plan_hash": intent.get("identity", {}).get("plan_hash"),
            "intent_sha256": intent.get("intent_sha256"),
        },
        "selection": {"content_type": "visual_drills", "family_id": family_id, "variant_id": variant_id},
        "family_music": {"route": "PRESERVE_EXISTING_C11C_FAMILY_MUSIC_V4", "profile_id": expected_profile, "gameplay_seed_field": "request.seed", "music_seed_field": "request.music_seed", "d3_v5_invoked": False},
        "approval": {"decision_record_sha256": DECISION_SHA, "composition_proposal_sha256": COMPOSITION_SHA, "timebase_proposal_sha256": TIMEBASE_SHA, "status": "USER_DIRECTED_V2_D_OWNED_CONTRACT_ONLY"},
        "geometry": geometry,
        "text": {"raw_editorial_preserved": True, "visible_fields": fields, "language_metadata_only": editor.get("language"), "layout_static_for_sequence": bool(fields), "phase_visibility": {"PRE_ROLL": False, "GAME": bool(fields), "END_CTA": False, "DONE": False}},
        "timebase": {"formula": "final_presentation_frame_index = pre_roll_frames + game_payload_frame_index", "pre_roll_seconds": 3.0, "end_cta_seconds": 3.0, "source_fps_is_authoritative": True, "frame_count_order_fps_preserved": True, "temporal_resampling": False},
        "native_phase_ownership": {"source_phase_contract_sha256": phase_contract.get("phase_contract_sha256"), "native_end_cta_header_authoritative": True, "d_may_override_native_end_cta": False},
        "source_pins": {**font_hashes, "presentation_profile": {"path": PRESENTATION_PROFILE_REL, "bytes": 8837, "sha256": PRESENTATION_PROFILE_SHA}, "c11c_phase_source_pins": phase_contract.get("source_pins", [])},
        "governance": {"renderer_native_input_emitted": False, "renderer_dispatch_invoked": False, "renderer_activation": False, "godot_invoked": False, "ffmpeg_invoked": False, "media_created": False, "audio_generated": False, "c11c_source_mutation": False, "d4_8": "BLOCKED", "d9_10": "PREPARE_ONLY", "release_authority": "NONE"},
    }
    plan["plan_sha256"] = _json_sha(plan)
    return plan


def validate_plan(plan: Mapping[str, Any]) -> None:
    unsigned = dict(plan)
    supplied = unsigned.pop("plan_sha256", None)
    if supplied != _json_sha(unsigned):
        raise DrillVisualConsumerError("D Drill V2 composition plan self-hash mismatch")
    if plan.get("schema") != "C11E-E4C-DRILL-VISUAL-COMPOSITION-PLAN-V2":
        raise DrillVisualConsumerError("consumer requires the exact V2 social-body plan schema")
    approval = plan.get("approval", {})
    if approval.get("composition_proposal_sha256") != COMPOSITION_SHA or approval.get("timebase_proposal_sha256") != TIMEBASE_SHA or approval.get("decision_record_sha256") != DECISION_SHA:
        raise DrillVisualConsumerError("D Drill V2 plan is not bound to its exact decision/proposal/timebase hashes")
    geometry = plan.get("geometry", {})
    for key, expected in EXPECTED_SOCIAL_REGIONS.items():
        if geometry.get(key) != expected:
            raise DrillVisualConsumerError(f"V2 plan social region mismatch: {key}")
    if geometry.get("source_frame_viewport") != EXPECTED_SOCIAL_REGIONS["body_rect"]:
        raise DrillVisualConsumerError(
            "V2 source viewport must be the exact social_regions.body_rect"
        )
    transform = geometry.get("source_frame_transform", {})
    if transform.get("mode") != "PIXEL_EXACT_BODY_CROP" or transform.get("scale") != 1.0 or transform.get("interpolation") is not False:
        raise DrillVisualConsumerError("V2 plan attempted a transform other than pixel-exact body crop")
    profile_pin = plan.get("source_pins", {}).get("presentation_profile", {})
    if profile_pin != {"path": PRESENTATION_PROFILE_REL, "bytes": 8837, "sha256": PRESENTATION_PROFILE_SHA}:
        raise DrillVisualConsumerError("V2 plan lacks the exact PresentationProfile.gd social geometry pin")
    governance = plan.get("governance", {})
    for key in ("renderer_native_input_emitted", "renderer_dispatch_invoked", "renderer_activation", "godot_invoked", "ffmpeg_invoked", "media_created", "audio_generated", "c11c_source_mutation"):
        if governance.get(key) is not False:
            raise DrillVisualConsumerError(f"visual consumer plan crossed execution boundary: {key}")


def _grapheme_clusters(text: str) -> list[str]:
    clusters: list[str] = []
    join_next = False
    for character in text:
        codepoint = ord(character)
        variation = 0xFE00 <= codepoint <= 0xFE0F or 0xE0100 <= codepoint <= 0xE01EF
        if not clusters or (not unicodedata.combining(character) and not variation and not join_next and character != "\u200d"):
            clusters.append(character)
        else:
            clusters[-1] += character
        join_next = character == "\u200d"
    return clusters


def _wrap_text(text: str, font: QFont, max_width: int, max_lines: int, field: str) -> list[str]:
    words = text.split()
    if not words:
        return []
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else current + " " + word
        if _text_advance(font, candidate) <= max_width:
            current = candidate
            continue
        if current:
            lines.append(current)
            current = ""
        # A long token is broken only at grapheme-cluster boundaries. The
        # canonical source value remains unchanged; only D-owned visual layout
        # receives line breaks. There is no ellipsis or character truncation.
        partial = ""
        for cluster in _grapheme_clusters(word):
            trial = partial + cluster
            if partial and _text_advance(font, trial) > max_width:
                lines.append(partial)
                partial = cluster
            elif not partial and _text_advance(font, trial) > max_width:
                raise DrillVisualConsumerError(f"single grapheme exceeds {field} width; no truncation allowed")
            else:
                partial = trial
        current = partial
    if current:
        lines.append(current)
    if len(lines) > max_lines:
        raise DrillVisualConsumerError(f"{field} exceeds approved line capacity ({max_lines}); no ellipsis/truncation")
    return lines

def compose_frame(
    source_frame: QImage,
    plan: Mapping[str, Any],
    phase: str,
    player_frame_index: int,
    gameplay_frame_count: int,
    fps_num: int = 30,
    fps_den: int = 1,
    project_root: Path | str | None = None,
) -> dict[str, Any]:
    """Return native phase passthrough or exact GAME social-body composition."""
    validate_plan(plan)
    if not isinstance(source_frame, QImage):
        raise DrillVisualConsumerError("source_frame must be a Qt QImage")
    if source_frame.width() != 720 or source_frame.height() != 1280:
        raise DrillVisualConsumerError("C11-C source frame must be REVIEW_720 720x1280")
    source_rgb = source_frame.convertToFormat(QImage.Format.Format_RGB888)
    original_sha = _image_rgb_sha256(source_rgb)
    mapping = map_phase_frame(phase, player_frame_index, gameplay_frame_count, fps_num, fps_den)
    if phase == "DONE":
        raise DrillVisualConsumerError("DONE has no delivery frame")

    # Native C11-C owns the complete PRE_ROLL and END_CTA frames. Do not compose
    # a D canvas around these phases, even when GAME editorial fields exist.
    if phase in ("PRE_ROLL", "END_CTA"):
        passthrough = source_rgb.copy()
        return {
            "image": passthrough,
            "mapping": mapping,
            "mode": "NATIVE_PHASE_FULL_FRAME_PASSTHROUGH",
            "source_rgb_sha256": original_sha,
            "source_unchanged": _image_rgb_sha256(source_rgb) == original_sha,
            "native_full_frame_identity": _image_rgb_sha256(passthrough) == original_sha,
        }

    fields = plan.get("text", {}).get("visible_fields", {})
    if not fields:
        passthrough = source_rgb.copy()
        return {
            "image": passthrough,
            "mapping": mapping,
            "mode": "UNCHANGED_FULL_FRAME_PASSTHROUGH",
            "source_rgb_sha256": original_sha,
            "source_unchanged": _image_rgb_sha256(source_rgb) == original_sha,
        }
    if phase != "GAME" or mapping.get("d_editorial_visible") is not True:
        raise DrillVisualConsumerError("D editorial composition is allowed only on GAME frames")

    root = Path(project_root).resolve() if project_root is not None else None
    if root is None or not root.is_dir():
        raise DrillVisualConsumerError("project_root is required when GAME editorial composition is active")
    geometry = plan["geometry"]
    canvas = geometry["canvas"]
    body_rect = geometry["body_rect"]
    viewport = geometry["source_frame_viewport"]
    if (canvas["width"], canvas["height"], body_rect["x"], body_rect["y"], body_rect["width"], body_rect["height"]) != (720, 1280, 0, 192, 720, 896):
        raise DrillVisualConsumerError("approved V2 social body crop changed")
    if viewport != {"x": 0, "y": 192, "width": 720, "height": 896}:
        raise DrillVisualConsumerError("V2 source viewport must be the exact social_regions.body_rect")

    x, y, width, height = (int(body_rect[key]) for key in ("x", "y", "width", "height"))
    native_body = source_rgb.copy(x, y, width, height)
    if native_body.isNull() or (native_body.width(), native_body.height()) != (width, height):
        raise DrillVisualConsumerError("Qt could not extract the exact native social body rectangle")
    composed = QImage(720, 1280, QImage.Format.Format_RGB888)
    background = tuple(bytes.fromhex(geometry["background_rgb_hex"]))
    composed.fill(QColor(*background))
    painter = QPainter(composed)
    if not painter.isActive():
        raise DrillVisualConsumerError("Qt QPainter could not activate on the D-owned RGB canvas")
    # No source scaling, filtering or resampling. Source body pixel (x,y) is
    # copied to the identical destination coordinate (x,y).
    painter.drawImage(QPoint(x, y), native_body)
    try:
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)
        painter.setPen(QColor(245, 247, 250))
        blocks = geometry["editorial_text_blocks"]
        for key in ("title", "subtitle", "call_to_action"):
            value = fields.get(key)
            if not value:
                continue
            block = blocks[key]
            rel_font = INTER_FONT_REL if block["font"] == "Inter-Bold" else MONO_FONT_REL
            font = _font(root, rel_font, int(block["font_size_px"]))
            cmap = _font_codepoints(root / rel_font)
            missing = sorted({ord(ch) for ch in value if not ch.isspace()} - cmap)
            raw_font = QRawFont.fromFont(font)
            missing.extend(ord(ch) for ch in value if not ch.isspace() and not raw_font.supportsCharacter(ord(ch)))
            missing = sorted(set(missing))
            if missing:
                preview = ",".join(f"U+{cp:04X}" for cp in missing[:8])
                raise DrillVisualConsumerError(f"{key} font coverage is incomplete: {preview}")
            lines = _wrap_text(value, font, int(block["width"]), int(block["max_lines"]), key)
            metrics = QFontMetricsF(font)
            line_height = int(block["line_height_px"])
            bx, by, bwidth, bheight = (int(block[k]) for k in ("x", "y", "width", "height"))
            if len(lines) * line_height > bheight:
                raise DrillVisualConsumerError(f"{key} lines exceed approved block height")
            painter.setFont(font)
            ascent = float(metrics.ascent())
            for index, line in enumerate(lines):
                baseline = float(by + index * line_height) + ascent
                bounds = metrics.tightBoundingRect(line)
                left = float(bx) + bounds.left()
                top = baseline + bounds.top()
                right = left + bounds.width()
                bottom = top + bounds.height()
                if left < bx or right > bx + bwidth or top < by or bottom > by + bheight:
                    raise DrillVisualConsumerError(f"{key} shaped glyphs exceed approved text block")
                painter.drawText(QPointF(float(bx), baseline), line)
    finally:
        painter.end()
    return {
        "image": composed,
        "mapping": mapping,
        "mode": "D_GAME_BODY_PIXEL_EXACT_COMPOSITION",
        "source_rgb_sha256": original_sha,
        "native_body_rgb_sha256": _image_rgb_sha256(native_body),
        "source_unchanged": _image_rgb_sha256(source_rgb) == original_sha,
        "native_body_pixel_identity": _image_rgb_sha256(composed.copy(x, y, width, height)) == _image_rgb_sha256(native_body),
    }

