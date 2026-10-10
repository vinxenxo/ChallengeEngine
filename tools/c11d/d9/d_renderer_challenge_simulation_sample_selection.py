"""In-memory preview for a PROPOSED C11-D challenge snapshot sampling policy.

This module only calculates frame-index mappings. It does not load SimulationResult,
change canonical state, interpolate snapshots, call Godot/FFmpeg, persist output, or
provide renderer-native input. The proposal remains unapproved.
"""
from __future__ import annotations

import copy
import hashlib
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_SIMULATION_SAMPLE_SELECTION_PROPOSAL_V1.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_SIMULATION_SAMPLE_SELECTION_PREVIEW_SCHEMA_V1.json")
CONTRACT_ID = "C11-D-D9-RENDERER-CHALLENGE-SIMULATION-SAMPLE-SELECTION-PROPOSAL-V1"
OUTPUT_ID = "C11-D-D9-RENDERER-CHALLENGE-SIMULATION-SAMPLE-SELECTION-PREVIEW-V1"
MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
EXPECTED_SOURCE_LINEAGE = [
    {"path":"release/C11C_FREEZE_PACKAGE_MANIFEST.json","sha256":"e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"},
    {"path":"challenges/CHALLENGE_004.json","sha256":"6a674c02c2d8831a872691954f1cc40e2492193f9b136f60656730a7be686b71"},
    {"path":"profiles/delivery/c11c_video_delivery_profiles.json","sha256":"967831513eb225e6eafd56496ce0d0a0b0f0e158d205b5985e7bba11b0534ae3"},
    {"path":"definitions/c11d/production/D_RENDERER_CHALLENGE_RUNTIME_OUTPUT_PREVIEW_V1.json","sha256":"ed56660d77de32e288eb3f4106499e94e390785d6d6503c5c028fc3399dd20c5"},
    {"path":"definitions/c11d/production/D_RENDERER_CHALLENGE_DELIVERY_TIMELINE_REVIEW_V1.json","sha256":"30381dba04a07d6e0ea1d82b186f46b78ab7193ecaa82efe3e484dd5bcd64e22"},
    {"path":"definitions/c11d/production/D_RENDERER_DELIVERY_TIMEBASE_PROJECTION_V1.json","sha256":"602c938cbf8378e8f71aefc6fb46d61496e78f9ab84d595f9efab982a2820a38"},
    {"path":"definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_PREVIEW_V1.json","sha256":"67daa1f83ac151906059695bb4d87974819c2d16d3715b78b00657bfdac54f7a"},
    {"path":"definitions/c11d/production/D_RENDERER_CHALLENGE_COORDINATE_PROJECTION_V1.json","sha256":"c1caf8e640595bc89957f17ef8bbd7abe80a92cac18cf77974633a1ddde0e264"},
]

class ChallengeSampleSelectionError(ValueError):
    """Input, pinned lineage, proposal, output, or governance mismatch."""

def _root(project_root: Path | str | None = None) -> Path:
    return Path(project_root).resolve() if project_root is not None else Path(__file__).resolve().parents[3]

def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)

def _sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def _sha_json(value: Any) -> str:
    return _sha_bytes(_canonical(value).encode("utf-8"))

def _read_json(root: Path, rel: Path) -> dict[str, Any]:
    try:
        value = json.loads((root / rel).read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ChallengeSampleSelectionError(f"Cannot read required JSON: {rel}") from exc
    if not isinstance(value, dict):
        raise ChallengeSampleSelectionError(f"Expected JSON object: {rel}")
    return value

def _load_contract(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    contract = _read_json(root, CONTRACT_REL)
    schema = _read_json(root, SCHEMA_REL)
    if contract.get("schema") != CONTRACT_ID or contract.get("schema_version") != "1.0":
        raise ChallengeSampleSelectionError("Sampling proposal contract identity/version mismatch")
    if contract.get("status") != "PROPOSAL_ONLY_NOT_RENDERER_INPUT":
        raise ChallengeSampleSelectionError("Sampling policy cannot self-promote")
    if contract.get("source_lineage") != EXPECTED_SOURCE_LINEAGE:
        raise ChallengeSampleSelectionError("Pinned source lineage declaration drift")
    if contract.get("content_identity", {}).get("frozen_c11c_manifest_sha256") != MANIFEST_SHA256:
        raise ChallengeSampleSelectionError("Frozen C11-C identity declaration drift")
    if contract.get("sampling_policy", {}).get("state") != "PROPOSED_NOT_APPROVED":
        raise ChallengeSampleSelectionError("Sampling proposal approval state must remain unapproved")
    sampling = contract.get("sampling_policy", {})
    if sampling.get("interpolation") != "NONE" or sampling.get("synthetic_or_interpolated_simulation_states") is not False:
        raise ChallengeSampleSelectionError("Proposal cannot create/interpolate simulation snapshots")
    if sampling.get("simulation_result_mutation") is not False or sampling.get("canonical_payload_mutation") is not False:
        raise ChallengeSampleSelectionError("Proposal must be read-only")
    if contract.get("approval_state", {}).get("simulation_sample_selection_policy_approved") is not False:
        raise ChallengeSampleSelectionError("Proposal must not grant sample-selection approval")
    if contract.get("required_execution_boundary", {}).get("d4_8") != "BLOCKED" or contract.get("required_execution_boundary", {}).get("release_authority") != "NONE":
        raise ChallengeSampleSelectionError("Governance boundary drift")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or schema.get("$id") != "urn:c11d:renderer-challenge-simulation-sample-selection-preview:v1" or schema.get("additionalProperties") is not False:
        raise ChallengeSampleSelectionError("Preview schema identity/strictness mismatch")
    required = schema.get("required", [])
    properties = schema.get("properties", {})
    if set(required) != set(properties):
        raise ChallengeSampleSelectionError("Preview schema must require all and only declared top-level properties")
    for entry in EXPECTED_SOURCE_LINEAGE:
        path = root / entry["path"]
        try:
            actual = _sha_bytes(path.read_bytes())
        except OSError as exc:
            raise ChallengeSampleSelectionError(f"Pinned source missing: {entry['path']}") from exc
        if actual != entry["sha256"]:
            raise ChallengeSampleSelectionError(f"Pinned source SHA-256 mismatch: {entry['path']}")
    return contract, schema

def _nearest_delivery_tick_half_up(source_frame_index: int, source_fps: int, delivery_fps: int) -> int:
    """Map a zero-based source frame index to a nearest delivery tick using integer math."""
    if isinstance(source_frame_index, bool) or not isinstance(source_frame_index, int) or source_frame_index < 0:
        raise ChallengeSampleSelectionError("Source frame index must be a non-negative integer")
    if isinstance(source_fps, bool) or not isinstance(source_fps, int) or source_fps <= 0:
        raise ChallengeSampleSelectionError("Source FPS must be a positive integer")
    if isinstance(delivery_fps, bool) or not isinstance(delivery_fps, int) or delivery_fps <= 0:
        raise ChallengeSampleSelectionError("Delivery FPS must be a positive integer")
    # floor(n/d + 0.5), entirely in integers; ties go to the later tick.
    return (2 * source_frame_index * delivery_fps + source_fps) // (2 * source_fps)

def build_sample_selection_preview(project_root: Path | str | None = None) -> dict[str, Any]:
    root = _root(project_root)
    contract, schema = _load_contract(root)
    ident = contract["content_identity"]
    tb = contract["timebases"]
    seg = contract["game_segment"]
    policy = contract["sampling_policy"]
    fixture = contract["reference_runtime_fixture"]
    ratio = tb["ratio_source_frames_per_delivery_frame"]
    source_fps = tb["source_timeline_fps"]
    delivery_fps = tb["delivery_timeline_fps"]
    if source_fps != 60 or delivery_fps != 30 or ratio != 2:
        raise ChallengeSampleSelectionError("This proposal supports only the pinned CHALLENGE_004 60-to-30 FPS case")
    if seg["source_snapshot_count"] != seg["delivery_snapshot_count"] * ratio:
        raise ChallengeSampleSelectionError("Game snapshot counts are not an exact 2:1 cadence")
    if seg["source_end_frame_exclusive"] - seg["source_start_frame"] != seg["source_snapshot_count"]:
        raise ChallengeSampleSelectionError("Source game segment range/count mismatch")
    if seg["delivery_end_frame_exclusive"] - seg["delivery_start_frame"] != seg["delivery_snapshot_count"]:
        raise ChallengeSampleSelectionError("Delivery game segment range/count mismatch")
    samples = []
    for delivery_local in range(seg["delivery_snapshot_count"]):
        source_local = delivery_local * ratio
        samples.append({
            "delivery_game_frame_index": delivery_local,
            "delivery_absolute_frame_index": seg["delivery_start_frame"] + delivery_local,
            "source_game_snapshot_index": source_local,
            "source_absolute_frame_index": seg["source_start_frame"] + source_local,
        })
    win_local = fixture["winning_frame_local_game_index"]
    if win_local < 0 or win_local >= seg["source_snapshot_count"]:
        raise ChallengeSampleSelectionError("Reference winning_frame is outside the GAME snapshot window")
    win_abs_source = seg["source_start_frame"] + win_local
    delivery_game_win = _nearest_delivery_tick_half_up(win_local, source_fps, delivery_fps)
    delivery_abs_win = seg["delivery_start_frame"] + delivery_game_win
    source_selected = win_local % ratio == 0
    anchor_status = "EXACT_SELECTED_SAMPLE_AND_DELIVERY_TICK" if source_selected and delivery_game_win * ratio == win_local else "NEAREST_DELIVERY_TICK_NOT_A_SELECTED_SOURCE_SNAPSHOT"
    source_indices = [item["source_game_snapshot_index"] for item in samples]
    preview: dict[str, Any] = {
        "schema": "C11-D-D9-RENDERER-CHALLENGE-SIMULATION-SAMPLE-SELECTION-PREVIEW-V1",
        "schema_version": "1.0",
        "status": "PROPOSAL_PREVIEW_ONLY_NOT_RENDERER_INPUT",
        "proposal_id": policy["policy_id"],
        "proposal_state": policy["state"],
        "proposal_contract_sha256": _sha_bytes((root / CONTRACT_REL).read_bytes()),
        "frozen_c11c_manifest_sha256": ident["frozen_c11c_manifest_sha256"],
        "content_identity": {k: ident[k] for k in ("challenge_id", "mechanic", "mechanic_version", "seed_requested", "seed_used")},
        "source_timebase": {"fps": source_fps, "total_frames": tb["source_timeline_total_frames"]},
        "delivery_timebase": {"fps": delivery_fps, "total_frames": tb["delivery_timeline_total_frames"]},
        "game_segment": {
            "source_start_frame": seg["source_start_frame"],
            "source_end_frame_exclusive": seg["source_end_frame_exclusive"],
            "source_snapshot_count": seg["source_snapshot_count"],
            "delivery_start_frame": seg["delivery_start_frame"],
            "delivery_end_frame_exclusive": seg["delivery_end_frame_exclusive"],
            "delivery_snapshot_count": seg["delivery_snapshot_count"],
            "duration_seconds": seg["duration_seconds"],
        },
        "sampling_policy": {
            "policy_id": policy["policy_id"],
            "state": policy["state"],
            "sampling_origin": policy["sampling_origin"],
            "selection_formula": policy["selection_formula"],
            "interpolation": policy["interpolation"],
            "synthetic_or_interpolated_simulation_states": policy["synthetic_or_interpolated_simulation_states"],
            "output_order": policy["output_order"],
            "source_snapshot_stride": ratio,
            "anchor_mapping_formula": policy["anchor_mapping_formula"],
            "anchor_tie_rule": policy["anchor_tie_rule"],
            "winning_frame_role": policy["winning_frame_role"],
            "close_calls_role": policy["close_calls_role"],
            "simulation_result_mutation": policy["simulation_result_mutation"],
            "canonical_payload_mutation": policy["canonical_payload_mutation"],
        },
        "samples": samples,
        "sample_assessment": {
            "source_snapshot_count": seg["source_snapshot_count"],
            "delivery_snapshot_count": len(samples),
            "stride": ratio,
            "first_source_snapshot_index": source_indices[0],
            "last_source_snapshot_index": source_indices[-1],
            "source_index_sha256": _sha_json(source_indices),
            "all_source_indices_unique": len(set(source_indices)) == len(source_indices),
            "delivery_indices_contiguous": [x["delivery_game_frame_index"] for x in samples] == list(range(len(samples))),
            "source_indices_follow_stride": source_indices == list(range(0, seg["source_snapshot_count"], ratio)),
            "sample_ratio_exact": len(samples) * ratio == seg["source_snapshot_count"],
            "interpolation_used": False,
        },
        "anchor_mapping": {
            "winning_frame_local_game_index": win_local,
            "winning_frame_absolute_source_index": win_abs_source,
            "winning_delivery_game_frame_index": delivery_game_win,
            "winning_absolute_delivery_frame_index": delivery_abs_win,
            "anchor_mapping_status": anchor_status,
            "winning_source_snapshot_selected": source_selected,
            "source_frame_rounding_error_numerator": win_abs_source - delivery_abs_win * (source_fps // delivery_fps),
            "source_frame_rounding_error_denominator": 1,
            "close_calls_count": fixture["close_calls_count"],
            "close_calls_used_for_timing": False,
        },
        "governance": copy.deepcopy(contract["required_execution_boundary"]),
        "approval_state": copy.deepcopy(contract["approval_state"]),
        "source_lineage": copy.deepcopy(contract["source_lineage"]),
    }
    preview["preview_sha256"] = _sha_json(preview)
    # Structural validation remains available even when jsonschema isn't installed.
    _validate_shape(preview, schema)
    return preview

def _validate_shape(candidate: Mapping[str, Any], schema: Mapping[str, Any]) -> None:
    if set(candidate) != set(schema.get("required", [])):
        raise ChallengeSampleSelectionError("Preview top-level shape mismatch")
    if candidate.get("schema") != OUTPUT_ID or candidate.get("status") != "PROPOSAL_PREVIEW_ONLY_NOT_RENDERER_INPUT":
        raise ChallengeSampleSelectionError("Preview identity/status mismatch")
    if candidate.get("proposal_state") != "PROPOSED_NOT_APPROVED":
        raise ChallengeSampleSelectionError("Preview cannot promote the proposal")
    if not isinstance(candidate.get("samples"), list) or len(candidate["samples"]) != 210:
        raise ChallengeSampleSelectionError("Expected 210 gameplay sample mappings")
    for row in candidate["samples"]:
        if not isinstance(row, Mapping) or set(row) != {"delivery_game_frame_index", "delivery_absolute_frame_index", "source_game_snapshot_index", "source_absolute_frame_index"}:
            raise ChallengeSampleSelectionError("Sample mapping row shape mismatch")
    if candidate.get("frozen_c11c_manifest_sha256") != MANIFEST_SHA256:
        raise ChallengeSampleSelectionError("Frozen C11-C manifest mismatch")
    if candidate.get("governance", {}).get("renderer_native_input_emitted") is not False or candidate.get("governance", {}).get("media_created") is not False or candidate.get("governance", {}).get("d4_8") != "BLOCKED" or candidate.get("governance", {}).get("release_authority") != "NONE":
        raise ChallengeSampleSelectionError("Preview governance boundary mismatch")
    if candidate.get("approval_state", {}).get("simulation_sample_selection_policy_approved") is not False or candidate.get("approval_state", {}).get("interpolation_policy_approved") is not False:
        raise ChallengeSampleSelectionError("Preview cannot grant policy approval")
    base = {str(k): copy.deepcopy(v) for k, v in candidate.items() if k != "preview_sha256"}
    if candidate.get("preview_sha256") != _sha_json(base):
        raise ChallengeSampleSelectionError("Preview SHA-256 mismatch")

def validate_sample_selection_preview(candidate: Any, project_root: Path | str | None = None) -> bool:
    root = _root(project_root)
    contract, schema = _load_contract(root)
    if not isinstance(candidate, Mapping):
        raise ChallengeSampleSelectionError("Preview must be an object")
    _validate_shape(candidate, schema)
    # Cross-check every field against a fresh deterministic build from pinned sources.
    expected = build_sample_selection_preview(root)
    if dict(candidate) != expected:
        raise ChallengeSampleSelectionError("Preview differs from the current pinned proposal build")
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        Draft202012Validator = None
    if Draft202012Validator is not None:
        Draft202012Validator(schema).validate(dict(candidate))
    return True
