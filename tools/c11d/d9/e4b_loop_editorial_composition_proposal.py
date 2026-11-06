from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

PROPOSAL_REL = Path("definitions/c11d/production/C11E_E4B_LOOP_EDITORIAL_COMPOSITION_PROPOSAL_V1.json")
PROPOSAL_SCHEMA = "C11E-E4B-LOOP-EDITORIAL-COMPOSITION-PROPOSAL-V1"
UNKNOWN = "UNKNOWN"
VISIBLE_FIELDS = ("title", "subtitle", "call_to_action")
CANONICAL_FIELDS = ("title", "subtitle", "call_to_action", "language")
MAX_FIELD_LENGTH = 160


class LoopCompositionProposalError(ValueError):
    pass


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def load_proposal(project_root: Path | str) -> dict[str, Any]:
    root = Path(project_root).resolve()
    path = root / PROPOSAL_REL
    try:
        proposal = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise LoopCompositionProposalError(f"Cannot load Loop composition proposal: {exc}") from exc
    if not isinstance(proposal, dict):
        raise LoopCompositionProposalError("Loop composition proposal must be a JSON object")
    return proposal


def validate_proposal(project_root: Path | str) -> dict[str, Any]:
    root = Path(project_root).resolve()
    proposal = load_proposal(root)
    if proposal.get("schema") != PROPOSAL_SCHEMA or proposal.get("schema_version") != "1.0":
        raise LoopCompositionProposalError("Unsupported Loop composition proposal identity")
    if proposal.get("status") != "PROPOSED_NOT_APPROVED_NOT_RENDERER_INPUT":
        raise LoopCompositionProposalError("Proposal status was promoted or altered")
    if proposal.get("authority", {}).get("frozen_c11c_manifest_sha256") != "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953":
        raise LoopCompositionProposalError("Frozen C11-C manifest lineage mismatch")
    manifest_path = root / "release" / "C11C_FREEZE_PACKAGE_MANIFEST.json"
    if not manifest_path.is_file() or _sha256_bytes(manifest_path.read_bytes()) != proposal["authority"]["frozen_c11c_manifest_sha256"]:
        raise LoopCompositionProposalError("Active frozen C11-C manifest does not match the proposal")

    geom = proposal.get("geometry", {})
    canvas = geom.get("canvas", {})
    top = geom.get("top_editorial_band", {})
    frame = geom.get("source_frame_viewport", {})
    bottom = geom.get("bottom_editorial_band", {})
    expected = {
        "canvas": {"width": 720, "height": 1280, "aspect_ratio": "9:16"},
        "top": (0, 0, 720, 192),
        "frame": (108, 192, 504, 896),
        "bottom": (0, 1088, 720, 192),
    }
    if canvas != expected["canvas"]:
        raise LoopCompositionProposalError("Review canvas geometry changed")
    if tuple(top.get(k) for k in ("x", "y", "width", "height")) != expected["top"]:
        raise LoopCompositionProposalError("Top band geometry changed")
    if tuple(frame.get(k) for k in ("x", "y", "width", "height")) != expected["frame"]:
        raise LoopCompositionProposalError("Contained C11-C frame geometry changed")
    if tuple(bottom.get(k) for k in ("x", "y", "width", "height")) != expected["bottom"]:
        raise LoopCompositionProposalError("Bottom band geometry changed")

    transform = geom.get("source_frame_transform", {})
    if transform.get("mode") != "UNIFORM_CONTAIN" or transform.get("scale_x") != transform.get("scale_y"):
        raise LoopCompositionProposalError("Source frame must use one uniform contain transform")
    if transform.get("cropping") is not False or transform.get("nonuniform_stretch") is not False:
        raise LoopCompositionProposalError("Cropping or nonuniform stretching is forbidden")
    if transform.get("temporal_resampling") is not False or transform.get("source_frame_count_mutation") is not False or transform.get("source_frame_order_mutation") is not False:
        raise LoopCompositionProposalError("Source timebase/frame sequence mutation is forbidden")
    if transform.get("yuv420p_chroma_alignment") != "EVEN_X_Y_WIDTH_HEIGHT":
        raise LoopCompositionProposalError("YUV420P chroma alignment requirement is missing")

    fields = proposal.get("scope", {}).get("canonical_editorial_fields")
    if fields != list(CANONICAL_FIELDS):
        raise LoopCompositionProposalError("Canonical Loop editorial key set changed")
    if proposal.get("scope", {}).get("max_field_length_codepoints") != MAX_FIELD_LENGTH:
        raise LoopCompositionProposalError("D9.8 max field length changed")
    if proposal.get("approval_gates", {}).get("loop_composition_approved") is not False:
        raise LoopCompositionProposalError("This proposal must remain unapproved")
    if proposal.get("approval_gates", {}).get("renderer_native_input_emitted") is not False:
        raise LoopCompositionProposalError("Proposal cannot emit renderer-native input")
    if proposal.get("approval_gates", {}).get("renderer_activation") is not False:
        raise LoopCompositionProposalError("Proposal cannot activate a renderer")
    if proposal.get("approval_gates", {}).get("production_dispatch") is not False or proposal.get("approval_gates", {}).get("media_created") is not False:
        raise LoopCompositionProposalError("Proposal cannot dispatch or create media")
    if proposal.get("approval_gates", {}).get("release_authority") != "NONE":
        raise LoopCompositionProposalError("Proposal cannot grant release authority")

    return {
        "schema": "C11E-E4B-LOOP-COMPOSITION-PROPOSAL-VALIDATION-V1",
        "status": "PASS_STATIC_PROPOSAL_VALIDATION_NOT_APPROVAL",
        "proposal_sha256": _sha256_bytes(_canonical_json(proposal)),
        "geometry": {
            "canvas": [720, 1280],
            "top_band": [0, 0, 720, 192],
            "source_frame_viewport": [108, 192, 504, 896],
            "bottom_band": [0, 1088, 720, 192],
            "uniform_scale": 0.7,
            "all_yuv420p_coordinates_even": True,
        },
        "canonical_fields": list(CANONICAL_FIELDS),
        "renderer_native_input_emitted": False,
        "renderer_activation": False,
        "production_dispatch": False,
        "media_created": False,
        "release_authority": "NONE",
    }


def build_layout(editorial: Mapping[str, Any], frame_count: int | None = None) -> dict[str, Any]:
    if not isinstance(editorial, Mapping) or set(editorial) != set(CANONICAL_FIELDS):
        raise LoopCompositionProposalError("All four canonical Loop editorial keys must be present; unknown or missing keys are rejected")
    if frame_count is not None and (isinstance(frame_count, bool) or not isinstance(frame_count, int) or frame_count <= 0):
        raise LoopCompositionProposalError("frame_count must be a positive integer supplied by the actual C11-C payload")

    values: dict[str, str] = {}
    visible: list[str] = []
    for field in CANONICAL_FIELDS:
        value = editorial[field]
        if not isinstance(value, str):
            raise LoopCompositionProposalError(f"Canonical editorial value must remain a string: {field}")
        if len(value) > MAX_FIELD_LENGTH:
            raise LoopCompositionProposalError(f"Canonical editorial value exceeds D9.8 max length: {field}")
        values[field] = value
        if field in VISIBLE_FIELDS and value.strip() and value.strip().upper() != UNKNOWN:
            visible.append(field)

    active = bool(visible)
    geometry = {
        "mode": "INSET_CONTAIN" if active else "FULL_FRAME_PASSTHROUGH",
        "canvas": [720, 1280],
        "source_frame_viewport": [108, 192, 504, 896] if active else [0, 0, 720, 1280],
        "uniform_scale": 0.7 if active else 1.0,
        "cropping": False,
        "nonuniform_stretch": False,
        "temporal_resampling": False,
        "source_frame_count_mutation": False,
        "source_frame_order_mutation": False,
    }
    windows = []
    if frame_count is not None:
        for field in visible:
            windows.append({"field": field, "start_frame": 0, "end_frame": frame_count, "interval": "HALF_OPEN"})

    return {
        "schema": "C11E-E4B-LOOP-EDITORIAL-LAYOUT-PLAN-V1",
        "status": "PROPOSED_NOT_APPROVED_NOT_RENDERER_INPUT",
        "editorial_values": values,
        "editorial_sha256": _sha256_bytes(_canonical_json(values)),
        "visible_fields": visible,
        "metadata_only_fields": ["language"],
        "geometry": geometry,
        "source_frame_count": frame_count,
        "visible_field_windows": windows,
        "frame_span_source": "ACTUAL_C11C_FAMILY_PAYLOAD_ONLY" if frame_count is not None else "NOT_AVAILABLE_IN_D9_REQUEST",
        "c11c_native_strings_mutated": False,
        "c11c_matrix_timing_mutated": False,
        "renderer_native_input_emitted": False,
        "renderer_activation": False,
        "production_dispatch": False,
        "media_created": False,
        "release_authority": "NONE",
    }
