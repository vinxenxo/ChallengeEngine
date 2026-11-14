"""D-owned Visual Drill V2 consumer with social-body pixel identity.

GAME copies only PresentationProfile.get_social_regions().body_rect into the
720x1280 REVIEW_720 body, without scaling or interpolation. The user-directed
D-owned family-title bridge replaces only the native PRE_ROLL title footprint
and draws the same title style in GAME; PRE_ROLL body/footer and END_CTA remain
pixel-identical to native frames. This module never launches C11-C, Godot,
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
from pathlib import Path, PurePosixPath
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
EDITORIAL_STYLE_AMENDMENT_REL = "definitions/c11d/production/C11E_E4C_DRILL_EDITORIAL_FAMILY_TITLE_AMENDMENT_R1_20261114.json"
EDITORIAL_STYLE_AMENDMENT_SHA = "1d0d5393368ca1e1ecb867059314e28463205fffc81e8af902909896e0ac7331"
FAMILY_TITLE_STYLE = {
    "font": "Inter-Bold",
    "font_size_px": 22,
    "line_height_px": 29,
    "color_rgb": [235, 215, 161],
    "alignment": "CENTER",
    "rect": {"x": 36, "y": 63, "width": 648, "height": 104},
    "native_title_mask": {"x": 184, "y": 64, "width": 352, "height": 102},
    "max_lines": 3,
    "animation": "STATIC_NO_ANIMATION_OBSERVED_IN_TRACKING_TIER_1_PRE_ROLL",
}
GAME_SUBTITLE_BLOCK = {
    "font": "Inter-Bold", "font_size_px": 15, "line_height_px": 19, "max_lines": 1,
    "region": "TOP_BAND", "x": 36, "y": 169, "width": 648, "height": 21,
}

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


def _editorial_amendment_path(root: Path) -> Path:
    """Resolve the immutable amendment from the active project, or a test-only staged path."""
    override = os.environ.get("C11E_EDITORIAL_AMENDMENT_PATH")
    return Path(override).resolve() if override else root / Path(*EDITORIAL_STYLE_AMENDMENT_REL.split("/"))


def _read_json(root: Path, relative: str) -> dict[str, Any]:
    path = _editorial_amendment_path(root) if relative == EDITORIAL_STYLE_AMENDMENT_REL else root / Path(*relative.split("/"))
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
        (EDITORIAL_STYLE_AMENDMENT_REL, EDITORIAL_STYLE_AMENDMENT_SHA),
    )
    for relative, digest in expected:
        source_path = _editorial_amendment_path(root) if relative == EDITORIAL_STYLE_AMENDMENT_REL else root / relative
        if _sha_file(source_path) != digest:
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
    amendment = _read_json(root, EDITORIAL_STYLE_AMENDMENT_REL)
    if amendment.get("schema") != "C11E-E4C-DRILL-EDITORIAL-FAMILY-TITLE-AMENDMENT-V1" or amendment.get("status") != "USER_DIRECTED_D_OWNED_PRESENTATION_AMENDMENT":
        raise DrillVisualConsumerError("family-title editorial amendment schema/status mismatch")
    if amendment.get("scope", {}).get("native_renderer_mutation") is not False or amendment.get("scope", {}).get("c11c_source_mutation") is not False:
        raise DrillVisualConsumerError("family-title amendment crosses the protected C11-C boundary")
    if amendment.get("family_title_style") != FAMILY_TITLE_STYLE:
        raise DrillVisualConsumerError("family-title style differs from the immutable amendment contract")
    if amendment.get("game_subtitle_block") != GAME_SUBTITLE_BLOCK:
        raise DrillVisualConsumerError("GAME subtitle block differs from the approved family-title layout amendment")
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


def _normalized_historical_source_pins(rows: Any, label: str) -> list[dict[str, Any]]:
    """Validate and canonicalize a frozen E1 pin inventory without re-running E1 dispatch guards."""
    if not isinstance(rows, list) or len(rows) != 91:
        raise DrillVisualConsumerError(f"{label} must contain exactly 91 source pins")
    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    for row in rows:
        if not isinstance(row, Mapping):
            raise DrillVisualConsumerError(f"{label} contains a malformed source-pin row")
        path = row.get("path")
        digest = row.get("sha256")
        byte_count = row.get("bytes")
        if not isinstance(path, str) or not path or "\\" in path:
            raise DrillVisualConsumerError(f"{label} contains an invalid source-pin path")
        pure = PurePosixPath(path)
        if pure.is_absolute() or ".." in pure.parts or "." in pure.parts or ":" in path:
            raise DrillVisualConsumerError(f"{label} contains an unsafe source-pin path: {path}")
        if path in seen:
            raise DrillVisualConsumerError(f"{label} contains a duplicate source-pin path: {path}")
        seen.add(path)
        if not isinstance(byte_count, int) or isinstance(byte_count, bool) or byte_count < 0:
            raise DrillVisualConsumerError(f"{label} contains an invalid byte count: {path}")
        if not isinstance(digest, str) or len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
            raise DrillVisualConsumerError(f"{label} contains an invalid SHA-256: {path}")
        normalized.append({"path": path, "bytes": byte_count, "sha256": digest})
    return sorted(normalized, key=lambda item: item["path"])


def _resolved_under_root(root: Path, candidate: Path, label: str) -> Path:
    resolved_root = root.resolve()
    resolved_candidate = candidate.resolve()
    try:
        resolved_candidate.relative_to(resolved_root)
    except ValueError as exc:
        raise DrillVisualConsumerError(f"{label} escapes the active project root") from exc
    return resolved_candidate


def _validate_historical_intent(
    root: Path,
    intent: Mapping[str, Any],
    accepted_e1_receipt: Mapping[str, Any],
    expected_existing_output_root: Path | str,
) -> dict[str, Any]:
    """Validate an already-executed E1 evidence set for D-only requalification.

    This deliberately does not call c11e_production_service.validate_*: the
    E1 DENY_EXISTING guard is a new-dispatch guard, not a historical receipt
    validator. The ordinary build_composition_plan() path remains unchanged.
    """
    if not root.is_dir():
        raise DrillVisualConsumerError(f"project root does not exist: {root}")
    if not isinstance(accepted_e1_receipt, Mapping):
        raise DrillVisualConsumerError("accepted historical E1 execution receipt is missing")
    if intent.get("schema_version") != "1.3" or intent.get("schema") != "C11-E-PRODUCTION-INTENT-V1":
        raise DrillVisualConsumerError("historical consumer requires the exact E1 schema 1.3 production intent")
    if intent.get("status") != "PREPARED_E1_NOT_DISPATCHED" or intent.get("request", {}).get("content_type") != "visual_drills":
        raise DrillVisualConsumerError("historical E1 intent is not a prepared Visual Drill intent")
    unsigned_intent = dict(intent)
    supplied_intent_sha = unsigned_intent.pop("intent_sha256", None)
    if supplied_intent_sha != _json_sha(unsigned_intent):
        raise DrillVisualConsumerError("historical E1 intent self-hash mismatch")
    if intent.get("request_origin") != "CLI":
        raise DrillVisualConsumerError("historical intent origin is not the accepted CLI source")

    request_id = intent.get("request", {}).get("request_id")
    if not request_id or accepted_e1_receipt.get("request_id") != request_id:
        raise DrillVisualConsumerError("historical E1 receipt request identity mismatch")
    if accepted_e1_receipt.get("schema") != "C11E-E4C-DRILL-SHARED-EXECUTION-RECEIPT-V1":
        raise DrillVisualConsumerError("historical E1 receipt schema mismatch")
    if accepted_e1_receipt.get("status") != "PASS_E4C_DRILL_SINGLE_SELECTOR_A_V_QUALIFICATION":
        raise DrillVisualConsumerError("historical E1 receipt is not an accepted single-selector A/V qualification")
    if accepted_e1_receipt.get("request_origin") != "CLI":
        raise DrillVisualConsumerError("historical E1 receipt origin mismatch")

    e1_validation = accepted_e1_receipt.get("e1_validation", {})
    if not isinstance(e1_validation, Mapping) or any((
        e1_validation.get("status") != "PASS_E1_PREPARATION_ONLY",
        e1_validation.get("valid") is not True,
        e1_validation.get("intent_sha256") != supplied_intent_sha,
        e1_validation.get("source_pin_count") != 91,
        e1_validation.get("media_created") is not False,
        e1_validation.get("renderer") is not False,
    )):
        raise DrillVisualConsumerError("historical E1 preparation receipt is invalid or not bound to this intent")
    parity = accepted_e1_receipt.get("e1_gui_cli_parity", {})
    if not isinstance(parity, Mapping) or any((
        parity.get("status") != "PASS_E1_SHARED_GUI_CLI_INTENT_PARITY",
        parity.get("semantic_identity_equal") is not True,
        parity.get("cli_intent_sha256") != supplied_intent_sha,
        parity.get("origin_used_for_execution") != "CLI",
    )):
        raise DrillVisualConsumerError("historical E1 shared GUI/CLI parity receipt is invalid")
    if accepted_e1_receipt.get("family_adapter_preparation_status") != "NOT_CONNECTED_E1":
        raise DrillVisualConsumerError("historical E1 receipt crossed the family-adapter preparation boundary")
    if accepted_e1_receipt.get("production_dispatch") is not False or accepted_e1_receipt.get("release_authority") != "NONE":
        raise DrillVisualConsumerError("historical E1 receipt crossed the dispatch/release boundary")
    if accepted_e1_receipt.get("c11c_source_mutation") is not False:
        raise DrillVisualConsumerError("historical E1 receipt records a C11-C source mutation")
    if accepted_e1_receipt.get("source_pin_count") != 91:
        raise DrillVisualConsumerError("historical E1 shared receipt top-level source-pin count mismatch")
    if accepted_e1_receipt.get("c11c_manifest_sha256") != "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953" or accepted_e1_receipt.get("c11c_frozen_manifest_unchanged") is not True:
        raise DrillVisualConsumerError("historical E1 receipt does not bind the frozen C11-C baseline")
    c11c_manifest = intent.get("source_identity", {}).get("c11c_manifest", {})
    if not isinstance(c11c_manifest, Mapping) or c11c_manifest != {
        "bytes": 796318,
        "disposition": "IMMUTABLE_REFERENCE_ONLY",
        "path": "release/C11C_FREEZE_PACKAGE_MANIFEST.json",
        "sha256": "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953",
    }:
        raise DrillVisualConsumerError("historical E1 intent does not bind the exact immutable C11-C manifest")

    output = intent.get("output", {})
    if not isinstance(output, Mapping) or any((
        output.get("created") is not False,
        output.get("overwrite_policy") != "DENY_EXISTING",
        output.get("planned_root_exists") is not False,
    )):
        raise DrillVisualConsumerError("historical E1 intent no longer carries its immutable no-overwrite preparation snapshot")
    planned_root_text = output.get("planned_root")
    if not isinstance(planned_root_text, str) or not planned_root_text:
        raise DrillVisualConsumerError("historical E1 intent has no planned output root")
    planned_relative = PurePosixPath(planned_root_text.replace("\\", "/"))
    if planned_relative.is_absolute() or ".." in planned_relative.parts or "." in planned_relative.parts or ":" in planned_root_text:
        raise DrillVisualConsumerError("historical E1 planned output root is unsafe")
    planned_root = _resolved_under_root(root, root.joinpath(*planned_relative.parts), "historical E1 planned output root")
    expected_root = _resolved_under_root(root, Path(expected_existing_output_root), "expected historical evidence root")
    receipt_root_raw = accepted_e1_receipt.get("evidence_root")
    if not isinstance(receipt_root_raw, str) or not receipt_root_raw:
        raise DrillVisualConsumerError("historical E1 receipt has no evidence_root")
    receipt_root = _resolved_under_root(root, Path(receipt_root_raw), "historical E1 receipt evidence root")
    import os as _os
    normalized = lambda p: _os.path.normcase(str(p))
    if normalized(planned_root) != normalized(expected_root) or normalized(receipt_root) != normalized(expected_root):
        raise DrillVisualConsumerError("historical E1 planned root, accepted receipt root and requested evidence root differ")
    if not expected_root.is_dir():
        raise DrillVisualConsumerError("historical E1 evidence root is not present for isolated requalification")

    # Tie both on-disk source records to the objects already validated by the
    # requalifier. This is not a new E1 production validation or dispatch.
    receipt_file = expected_root / "E4C_DRILL_AV_QUALIFICATION_RECEIPT.json"
    intent_file = expected_root / "e1_intent.json"
    if not receipt_file.is_file() or not intent_file.is_file():
        raise DrillVisualConsumerError("historical E1 evidence root is missing its accepted receipt or intent file")
    try:
        disk_receipt = json.loads(receipt_file.read_text(encoding="utf-8-sig"))
        disk_intent = json.loads(intent_file.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise DrillVisualConsumerError(f"cannot re-read historical E1 evidence records: {exc}") from exc
    if not isinstance(disk_receipt, Mapping) or _json_sha(disk_receipt) != _json_sha(accepted_e1_receipt):
        raise DrillVisualConsumerError("on-disk historical E1 receipt differs from the accepted receipt supplied to D")
    if not isinstance(disk_intent, Mapping) or _json_sha(disk_intent) != _json_sha(intent):
        raise DrillVisualConsumerError("on-disk historical E1 intent differs from the accepted intent supplied to D")

    execution_boundary = intent.get("execution_boundary", {})
    if not isinstance(execution_boundary, Mapping):
        raise DrillVisualConsumerError("historical E1 execution boundary is missing")
    for key in ("dispatch_authorized", "media_created", "production_execution", "renderer_activation", "renderer_dispatch_invoked", "renderer_input_emitted"):
        if execution_boundary.get(key) is not False:
            raise DrillVisualConsumerError(f"historical E1 intent crossed its non-dispatchable boundary: {key}")
    if execution_boundary.get("d4_8") != "BLOCKED" or execution_boundary.get("release_authority") != "NONE":
        raise DrillVisualConsumerError("historical E1 execution boundary status changed")
    family_adapter = intent.get("family_adapter", {})
    if not isinstance(family_adapter, Mapping) or family_adapter.get("status") != "NOT_CONNECTED_E1" or family_adapter.get("renderer_input_emitted") is not False:
        raise DrillVisualConsumerError("historical E1 intent changed the family-adapter boundary")

    preparation = intent.get("d9_boundary_preparation")
    if not isinstance(preparation, Mapping) or preparation.get("status") != "DRILL_FAMILY_STAGE_PREPARED_NOT_DISPATCHABLE":
        raise DrillVisualConsumerError("historical E1 Drill boundary preparation missing or dispatchable")
    unsigned_preparation = {key: value for key, value in preparation.items() if key != "preparation_sha256"}
    if preparation.get("preparation_sha256") != _json_sha(unsigned_preparation):
        raise DrillVisualConsumerError("historical E1 Drill boundary preparation self-hash mismatch")
    for key in ("renderer_input_emitted", "renderer_dispatch_invoked", "media_created", "audio_generation_invoked", "ffmpeg_invoked", "godot_invoked", "launcher_invoked"):
        if preparation.get(key) is not False:
            raise DrillVisualConsumerError(f"historical D9 preparation crossed its non-dispatchable boundary: {key}")
    if preparation.get("release_authority") != "NONE":
        raise DrillVisualConsumerError("historical D9 preparation unexpectedly carries release authority")

    intent_pins = _normalized_historical_source_pins(intent.get("source_identity", {}).get("source_pins"), "E1 intent source pins")
    receipt_pre = _normalized_historical_source_pins(accepted_e1_receipt.get("source_pins_pre_execution"), "E1 receipt pre-execution pins")
    receipt_pre_renderer = _normalized_historical_source_pins(accepted_e1_receipt.get("source_pins_immediately_pre_renderer"), "E1 receipt pre-renderer pins")
    receipt_post = _normalized_historical_source_pins(accepted_e1_receipt.get("source_pins_post_execution"), "E1 receipt post-execution pins")
    if not (intent_pins == receipt_pre == receipt_pre_renderer == receipt_post):
        raise DrillVisualConsumerError("historical E1 intent and receipt 91-pin inventories are not identical")
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
        return {"phase": phase, "final_presentation_frame_index": player_frame_index, "source_frame_index": 0, "d_editorial_visible": False, "d_editorial_title_slot_open": True, "pre_roll_frames": pre, "gameplay_frames": gameplay_frame_count, "end_cta_frames": end, "total_frames": total}
    if phase == "GAME":
        if not 0 <= player_frame_index < gameplay_frame_count:
            raise DrillVisualConsumerError("GAME payload index outside [0, gameplay_frame_count)")
        return {"phase": phase, "final_presentation_frame_index": pre + player_frame_index, "source_frame_index": player_frame_index, "d_editorial_visible": True, "d_editorial_title_slot_open": True, "pre_roll_frames": pre, "gameplay_frames": gameplay_frame_count, "end_cta_frames": end, "total_frames": total}
    if phase == "END_CTA":
        if not pre + gameplay_frame_count <= player_frame_index < total:
            raise DrillVisualConsumerError("END_CTA index outside native final-stream phase range")
        return {"phase": phase, "final_presentation_frame_index": player_frame_index, "source_frame_index": gameplay_frame_count - 1, "d_editorial_visible": False, "d_editorial_title_slot_open": False, "pre_roll_frames": pre, "gameplay_frames": gameplay_frame_count, "end_cta_frames": end, "total_frames": total}
    if phase == "DONE":
        return {"phase": phase, "final_presentation_frame_index": None, "source_frame_index": None, "d_editorial_visible": False, "pre_roll_frames": pre, "gameplay_frames": gameplay_frame_count, "end_cta_frames": end, "total_frames": total}
    raise DrillVisualConsumerError(f"unknown native Drill phase: {phase}")


def _build_composition_plan_from_preparation(
    intent: Mapping[str, Any], project_root: Path | str, preparation: Mapping[str, Any]
) -> dict[str, Any]:
    root = Path(project_root).resolve()
    if not root.is_dir():
        raise DrillVisualConsumerError(f"project root does not exist: {root}")
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
        "approval": {"decision_record_sha256": DECISION_SHA, "composition_proposal_sha256": COMPOSITION_SHA, "timebase_proposal_sha256": TIMEBASE_SHA, "editorial_family_title_amendment_sha256": EDITORIAL_STYLE_AMENDMENT_SHA, "status": "USER_DIRECTED_V2_D_OWNED_CONTRACT_ONLY"},
        "geometry": geometry,
        "text": {
            "raw_editorial_preserved": True,
            "visible_fields": fields,
            "language_metadata_only": editor.get("language"),
            "layout_static_for_sequence": bool(fields),
            "family_title_style": dict(FAMILY_TITLE_STYLE),
            "game_subtitle_block": dict(GAME_SUBTITLE_BLOCK),
            "phase_visibility": {"PRE_ROLL": bool(fields.get("title")), "GAME": bool(fields), "END_CTA": False, "DONE": False},
            "field_phase_visibility": {
                "title": ["PRE_ROLL", "GAME"] if fields.get("title") else [],
                "subtitle": ["GAME"] if fields.get("subtitle") else [],
                "call_to_action": ["GAME"] if fields.get("call_to_action") else [],
            },
        },
        "timebase": {"formula": "final_presentation_frame_index = pre_roll_frames + game_payload_frame_index", "pre_roll_seconds": 3.0, "end_cta_seconds": 3.0, "source_fps_is_authoritative": True, "frame_count_order_fps_preserved": True, "temporal_resampling": False},
        "native_phase_ownership": {"source_phase_contract_sha256": phase_contract.get("phase_contract_sha256"), "native_end_cta_header_authoritative": True, "d_may_override_native_end_cta": False},
        "source_pins": {**font_hashes, "presentation_profile": {"path": PRESENTATION_PROFILE_REL, "bytes": 8837, "sha256": PRESENTATION_PROFILE_SHA}, "editorial_family_title_amendment": {"path": EDITORIAL_STYLE_AMENDMENT_REL, "sha256": EDITORIAL_STYLE_AMENDMENT_SHA}, "c11c_phase_source_pins": phase_contract.get("source_pins", [])},
        "governance": {"renderer_native_input_emitted": False, "renderer_dispatch_invoked": False, "renderer_activation": False, "godot_invoked": False, "ffmpeg_invoked": False, "media_created": False, "audio_generated": False, "c11c_source_mutation": False, "d4_8": "BLOCKED", "d9_10": "PREPARE_ONLY", "release_authority": "NONE"},
    }
    plan["plan_sha256"] = _json_sha(plan)
    return plan


def build_composition_plan(intent: Mapping[str, Any], project_root: Path | str) -> dict[str, Any]:
    """Build a plan for the ordinary E1 path; retains the strict shared-service guard."""
    root = Path(project_root).resolve()
    if not root.is_dir():
        raise DrillVisualConsumerError(f"project root does not exist: {root}")
    preparation = _validate_intent(root, intent)
    return _build_composition_plan_from_preparation(intent, root, preparation)


def build_composition_plan_for_existing_media(
    intent: Mapping[str, Any],
    project_root: Path | str,
    accepted_e1_receipt: Mapping[str, Any],
    expected_existing_output_root: Path | str,
) -> dict[str, Any]:
    """Build only for a receipt-verified historical output; never creates or dispatches E1."""
    root = Path(project_root).resolve()
    if not root.is_dir():
        raise DrillVisualConsumerError(f"project root does not exist: {root}")
    preparation = _validate_historical_intent(root, intent, accepted_e1_receipt, expected_existing_output_root)
    return _build_composition_plan_from_preparation(intent, root, preparation)


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
    if approval.get("editorial_family_title_amendment_sha256") != EDITORIAL_STYLE_AMENDMENT_SHA:
        raise DrillVisualConsumerError("D Drill V2 plan is not bound to the user-directed family-title amendment")
    text_contract = plan.get("text", {})
    if text_contract.get("family_title_style") != FAMILY_TITLE_STYLE:
        raise DrillVisualConsumerError("D Drill V2 family-title rendering style changed")
    if text_contract.get("game_subtitle_block") != GAME_SUBTITLE_BLOCK:
        raise DrillVisualConsumerError("D Drill V2 GAME subtitle placement changed")
    fields = text_contract.get("visible_fields", {})
    expected_visibility = {
        "PRE_ROLL": bool(fields.get("title")),
        "GAME": bool(fields),
        "END_CTA": False,
        "DONE": False,
    }
    if text_contract.get("phase_visibility") != expected_visibility:
        raise DrillVisualConsumerError("D Drill V2 phase visibility differs from the family-title amendment")
    expected_field_visibility = {
        "title": ["PRE_ROLL", "GAME"] if fields.get("title") else [],
        "subtitle": ["GAME"] if fields.get("subtitle") else [],
        "call_to_action": ["GAME"] if fields.get("call_to_action") else [],
    }
    if text_contract.get("field_phase_visibility") != expected_field_visibility:
        raise DrillVisualConsumerError("D Drill V2 field-level phase visibility changed")
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
    amendment_pin = plan.get("source_pins", {}).get("editorial_family_title_amendment", {})
    if amendment_pin != {"path": EDITORIAL_STYLE_AMENDMENT_REL, "sha256": EDITORIAL_STYLE_AMENDMENT_SHA}:
        raise DrillVisualConsumerError("V2 plan lacks the exact family-title amendment source pin")
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

def _row_median_background(source: QImage, y: int, left_x: int, right_x: int) -> QColor:
    """Estimate the undisturbed header row from pixels outside the native title mask."""
    samples = []
    for x in range(0, left_x, 4):
        c = source.pixelColor(x, y)
        samples.append((c.red(), c.green(), c.blue()))
    for x in range(right_x, source.width(), 4):
        c = source.pixelColor(x, y)
        samples.append((c.red(), c.green(), c.blue()))
    if not samples:
        raise DrillVisualConsumerError("cannot sample native header background outside title mask")
    channels = []
    for channel in range(3):
        values = sorted(row[channel] for row in samples)
        channels.append(values[len(values) // 2])
    return QColor(*channels)


def _clear_native_title(source: QImage, style: Mapping[str, Any]) -> QImage:
    """Remove only the known native family-title footprint, preserving row background and all other pixels."""
    result = source.copy()
    mask = style["native_title_mask"]
    x, y, width, height = (int(mask[k]) for k in ("x", "y", "width", "height"))
    if x <= 0 or y < 0 or x + width >= source.width() or y + height >= 188:
        raise DrillVisualConsumerError("native title replacement mask is outside the approved family header area")
    painter = QPainter(result)
    if not painter.isActive():
        raise DrillVisualConsumerError("Qt QPainter could not activate for native title replacement")
    try:
        for row in range(y, y + height):
            painter.fillRect(x, row, width, 1, _row_median_background(source, row, x, x + width))
    finally:
        painter.end()
    return result


def _draw_family_title(painter: QPainter, root: Path, text: str, style: Mapping[str, Any]) -> dict[str, Any]:
    """Draw the D editorial title with the native Drill family title typographic signature."""
    if not text:
        return {"visible": False, "line_count": 0}
    if style != FAMILY_TITLE_STYLE:
        raise DrillVisualConsumerError("family-title style does not match the approved amendment")
    font = _font(root, INTER_FONT_REL, int(style["font_size_px"]))
    cmap = _font_codepoints(root / INTER_FONT_REL)
    missing = sorted({ord(ch) for ch in text if not ch.isspace()} - cmap)
    raw_font = QRawFont.fromFont(font)
    missing.extend(ord(ch) for ch in text if not ch.isspace() and not raw_font.supportsCharacter(ord(ch)))
    if missing:
        preview = ",".join(f"U+{cp:04X}" for cp in sorted(set(missing))[:8])
        raise DrillVisualConsumerError(f"family title font coverage is incomplete: {preview}")
    rect = style["rect"]
    bx, by, bwidth, bheight = (int(rect[k]) for k in ("x", "y", "width", "height"))
    lines = _wrap_text(text, font, bwidth, int(style["max_lines"]), "family_title")
    line_height = int(style["line_height_px"])
    total_height = len(lines) * line_height
    if total_height > bheight:
        raise DrillVisualConsumerError("family title exceeds its native-style header height")
    metrics = QFontMetricsF(font)
    ascent = float(metrics.ascent())
    top = by + (bheight - total_height) / 2.0
    painter.setFont(font)
    painter.setPen(QColor(*style["color_rgb"]))
    for index, line in enumerate(lines):
        advance = _text_advance(font, line)
        left = bx + (bwidth - advance) / 2.0
        baseline = top + index * line_height + ascent
        bounds = metrics.tightBoundingRect(line)
        if left + bounds.left() < bx or left + bounds.left() + bounds.width() > bx + bwidth:
            raise DrillVisualConsumerError("centered family title glyphs exceed the native-style header width")
        if baseline + bounds.top() < by or baseline + bounds.top() + bounds.height() > by + bheight:
            raise DrillVisualConsumerError("centered family title glyphs exceed the native-style header height")
        painter.drawText(QPointF(float(left), baseline), line)
    return {"visible": True, "line_count": len(lines), "alignment": "CENTER", "font": style["font"], "font_size_px": style["font_size_px"], "color_rgb": style["color_rgb"], "animation": style["animation"]}


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
    """Apply the D family-title bridge in PRE_ROLL/GAME; preserve native GAME body and END_CTA."""
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

    text_contract = plan.get("text", {})
    fields = text_contract.get("visible_fields", {})
    title = fields.get("title", "")
    mapping["d_editorial_title_slot_open"] = bool(title) and phase in ("PRE_ROLL", "GAME")
    style = text_contract.get("family_title_style", FAMILY_TITLE_STYLE)
    root = Path(project_root).resolve() if project_root is not None else None

    if phase == "PRE_ROLL":
        if not title:
            passthrough = source_rgb.copy()
            return {"image": passthrough, "mapping": mapping, "mode": "NATIVE_PHASE_FULL_FRAME_PASSTHROUGH_NO_EDITORIAL_TITLE", "source_rgb_sha256": original_sha, "source_unchanged": _image_rgb_sha256(source_rgb) == original_sha, "native_full_frame_identity": _image_rgb_sha256(passthrough) == original_sha, "d_editorial_title_visible": False}
        if root is None or not root.is_dir():
            raise DrillVisualConsumerError("project_root is required for PRE_ROLL family-title replacement")
        replaced = _clear_native_title(source_rgb, style)
        painter = QPainter(replaced)
        if not painter.isActive():
            raise DrillVisualConsumerError("Qt QPainter could not activate for PRE_ROLL family-title rendering")
        try:
            painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)
            title_render = _draw_family_title(painter, root, title, style)
        finally:
            painter.end()
        body = source_rgb.copy(0, 192, 720, 896)
        body_out = replaced.copy(0, 192, 720, 896)
        footer = source_rgb.copy(0, 1088, 720, 192)
        footer_out = replaced.copy(0, 1088, 720, 192)
        body_same = _image_rgb_bytes(body) == _image_rgb_bytes(body_out)
        footer_same = _image_rgb_bytes(footer) == _image_rgb_bytes(footer_out)
        if not body_same or not footer_same:
            raise DrillVisualConsumerError("PRE_ROLL family-title replacement modified native body/countdown or footer")
        return {
            "image": replaced, "mapping": mapping, "mode": "D_PREROLL_FAMILY_TITLE_REPLACEMENT_NATIVE_BODY_PRESERVED",
            "source_rgb_sha256": original_sha, "source_unchanged": _image_rgb_sha256(source_rgb) == original_sha,
            "native_body_pixel_identity": body_same, "native_footer_pixel_identity": footer_same,
            "native_title_replaced": True, "d_editorial_title_visible": True, "family_title_render": title_render,
        }

    if phase == "END_CTA":
        passthrough = source_rgb.copy()
        return {
            "image": passthrough, "mapping": mapping, "mode": "NATIVE_PHASE_FULL_FRAME_PASSTHROUGH",
            "source_rgb_sha256": original_sha, "source_unchanged": _image_rgb_sha256(source_rgb) == original_sha,
            "native_full_frame_identity": _image_rgb_sha256(passthrough) == original_sha, "d_editorial_title_visible": False,
        }

    if phase != "GAME":
        raise DrillVisualConsumerError(f"unsupported delivery phase: {phase}")
    if not fields:
        passthrough = source_rgb.copy()
        return {"image": passthrough, "mapping": mapping, "mode": "UNCHANGED_FULL_FRAME_PASSTHROUGH", "source_rgb_sha256": original_sha, "source_unchanged": _image_rgb_sha256(source_rgb) == original_sha, "d_editorial_title_visible": False}
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
    title_render: dict[str, Any] = {"visible": False}
    try:
        painter.drawImage(QPoint(x, y), native_body)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)
        if title:
            title_render = _draw_family_title(painter, root, title, style)
        blocks = geometry["editorial_text_blocks"]
        for key in ("subtitle", "call_to_action"):
            value = fields.get(key)
            if not value:
                continue
            block = text_contract["game_subtitle_block"] if key == "subtitle" else blocks[key]
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
                painter.setPen(QColor(245, 247, 250) if key == "subtitle" else QColor(205, 208, 210))
                painter.drawText(QPointF(float(bx), baseline), line)
    finally:
        painter.end()
    body_identity = _image_rgb_sha256(composed.copy(x, y, width, height)) == _image_rgb_sha256(native_body)
    return {
        "image": composed, "mapping": mapping, "mode": "D_GAME_BODY_PIXEL_EXACT_FAMILY_TITLE_COMPOSITION",
        "source_rgb_sha256": original_sha, "native_body_rgb_sha256": _image_rgb_sha256(native_body),
        "source_unchanged": _image_rgb_sha256(source_rgb) == original_sha,
        "native_body_pixel_identity": body_identity, "d_editorial_title_visible": bool(title),
        "family_title_render": title_render,
    }

