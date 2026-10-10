"""Contract checks for the in-memory Challenge visual payload preview.

The Godot harness performs the authoritative runtime materialization. This
module only validates immutable source lineage, contract/schema structure and
summary safety; it does not launch Godot, create renderer input or write media.
"""
from __future__ import annotations

import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Mapping

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_PREVIEW_V1.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_PREVIEW_SCHEMA_V1.json")
CONTRACT_SCHEMA = "C11-D-D9-RENDERER-CHALLENGE-VISUAL-PAYLOAD-PREVIEW-CONTRACT-V1"
PAYLOAD_SCHEMA = "C11-D-D9-CHALLENGE-VISUAL-PAYLOAD-PREVIEW-V1"
FROZEN_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
CHALLENGE_SHA256 = "6a674c02c2d8831a872691954f1cc40e2492193f9b136f60656730a7be686b71"
EXPECTED_ASSETS = {
    "BACKGROUND": ("assets/c6/garage_background.svg", "c9d8acdae725ca7726fc8ad23a046e4aac4d9e454b45db40d2c770732b31ab1e", 1080, 1920),
    "ANIMATED_OBJECT": ("assets/c6/car.svg", "93a6f78d9654f7917ab2287800858a937e9c68c458cc60bf417d6f2b98c1a96d", 160, 320),
    "TARGET": ("assets/c6/parking_target.svg", "ec2dcafd7dfc99ff501eb2d93b93906680a30c48cf0741807cbbdd915a18cfb3", 200, 400),
}


class ChallengeVisualPayloadError(ValueError):
    """Raised when the D Challenge visual payload preview contract is violated."""


def project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise ChallengeVisualPayloadError(f"Cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ChallengeVisualPayloadError(f"Expected JSON object at {path}")
    return value


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_json(value: Any) -> str:
    canonical = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return sha256_bytes(canonical.encode("utf-8"))


def _contract(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    contract = read_json(root / CONTRACT_REL)
    schema = read_json(root / SCHEMA_REL)
    if contract.get("schema") != CONTRACT_SCHEMA or contract.get("schema_version") != "1.0":
        raise ChallengeVisualPayloadError("Unsupported contract identity/version")
    if contract.get("status") != "PREPARATION_ONLY_NOT_APPROVED_NOT_FROZEN":
        raise ChallengeVisualPayloadError("Contract cannot approve or freeze itself")
    if schema.get("$id") != "urn:c11d:renderer-challenge-visual-payload-preview:v1":
        raise ChallengeVisualPayloadError("Output schema identity mismatch")
    if schema.get("additionalProperties") is not False:
        raise ChallengeVisualPayloadError("Output schema must reject unknown top-level fields")
    source_authority = contract.get("source_authority", {})
    if source_authority.get("frozen_manifest_sha256") != FROZEN_MANIFEST_SHA256:
        raise ChallengeVisualPayloadError("Frozen C11-C manifest pin mismatch")
    if source_authority.get("challenge_source_sha256") != CHALLENGE_SHA256:
        raise ChallengeVisualPayloadError("Challenge source pin mismatch")
    expected_runtime = {
        "challenge_id": "CHALLENGE_004",
        "mechanic": "parking_v2",
        "mechanic_version": "2.0",
        "presentation_profile_id": "social_default_v1",
        "source_coordinate_space": "CANVAS_1080X1920",
        "source_fps": 60,
        "source_total_frames": 900,
        "source_duration_seconds": 15,
        "phase_order": ["HOOK", "GAME", "REVEAL", "CTA"],
        "phase_frames": {"HOOK": 180, "GAME": 420, "REVEAL": 180, "CTA": 120},
        "simulation_snapshot_fields": ["position", "rotation", "scale", "opacity", "texture_index", "variant_id"],
        "simulation_fields_excluded": ["custom_data", "score", "minimum_distance", "tolerance_threshold", "winning_frame", "close_calls"],
        "source_frame_sampling": "PRESERVE_ALL_420_GAME_SNAPSHOTS_AT_SOURCE_60FPS",
        "delivery_resampling": "UNRESOLVED_NOT_APPLIED",
        "coordinate_projection": "UNRESOLVED_NOT_APPLIED",
        "editorial_window_binding": "NOT_APPLIED_BY_THIS_CONTRACT",
    }
    if contract.get("runtime_contract") != expected_runtime:
        raise ChallengeVisualPayloadError("Runtime scope or included/excluded simulation field contract changed")
    payload = contract.get("payload_contract", {})
    expected_payload = {
        "schema": PAYLOAD_SCHEMA,
        "status": "IN_MEMORY_REVIEW_ONLY_SOURCE_TIMEBASE_VISUAL_PAYLOAD_NOT_RENDERER_INPUT",
        "payload_persistence": "NONE",
        "payload_instances_expected": 1,
        "asset_nodes_expected": 3,
        "game_frame_records_expected": 420,
        "deterministic_repetition_expected": True,
        "resource_load_required": True,
        "render_nodes_created": False,
        "renderer_native_input_emitted": False,
        "renderer_dispatch_invoked": False,
        "renderer_activation": False,
        "media_output_created": False,
        "output_artifact_path": None,
    }
    if payload != expected_payload:
        raise ChallengeVisualPayloadError("Payload boundary must remain in-memory and non-dispatchable")
    locks = contract.get("governance_locks", {})
    for key, expected in {
        "source_adapter_mode": "PREPARE_ONLY", "c11c_source_mutation": False,
        "d4_8": "BLOCKED", "release_authority": "NONE",
        "renderer_baseline_approved": False, "renderer_baseline_frozen": False,
        "d9_14_full_acceptance": "BLOCKED_AS_REQUIRED", "d9_16_full_acceptance": "BLOCKED_AS_REQUIRED",
        "d9_17_closure": "BLOCKED_NO_GO", "d10": "BLOCKED",
    }.items():
        if locks.get(key) != expected:
            raise ChallengeVisualPayloadError(f"Governance lock mismatch: {key}")
    return contract, schema


def validate_source_pins(root: Path | None = None) -> dict[str, int]:
    root = root or project_root()
    contract, _ = _contract(root)
    pins = contract.get("pinned_sources")
    if not isinstance(pins, list) or len(pins) != 10:
        raise ChallengeVisualPayloadError("Expected exactly 10 pinned source/asset files")
    verified = 0
    for item in pins:
        if not isinstance(item, Mapping):
            raise ChallengeVisualPayloadError("Malformed source pin")
        rel = Path(str(item.get("path", "")))
        if rel.is_absolute() or ".." in rel.parts:
            raise ChallengeVisualPayloadError("Source pin path escapes project root")
        path = root / rel
        if not path.is_file():
            raise ChallengeVisualPayloadError(f"Pinned source missing: {rel.as_posix()}")
        digest = sha256_bytes(path.read_bytes())
        if digest != item.get("sha256"):
            raise ChallengeVisualPayloadError(f"Pinned source hash mismatch: {rel.as_posix()}")
        verified += 1
        role = item.get("role")
        if role:
            try:
                xml_root = ET.fromstring(path.read_bytes())
            except ET.ParseError as exc:
                raise ChallengeVisualPayloadError(f"Asset is not valid XML/SVG: {rel.as_posix()}") from exc
            if not xml_root.tag.endswith("svg"):
                raise ChallengeVisualPayloadError(f"Asset root must be SVG: {rel.as_posix()}")
            if xml_root.attrib.get("width") != str(item.get("width")) or xml_root.attrib.get("height") != str(item.get("height")):
                raise ChallengeVisualPayloadError(f"Asset intrinsic dimensions changed: {rel.as_posix()}")
    if verified != 10:
        raise ChallengeVisualPayloadError("Not all pinned source files were verified")
    source = read_json(root / "challenges/CHALLENGE_004.json")
    if source.get("challenge_id") != "CHALLENGE_004" or source.get("mechanic") != "parking_v2":
        raise ChallengeVisualPayloadError("Canonical Challenge identity mismatch")
    presentation = source.get("presentation", {})
    if presentation.get("profile") != "social_default_v1" or presentation.get("coordinate_space") != "CANVAS_1080X1920":
        raise ChallengeVisualPayloadError("Challenge presentation identity/coordinate space changed")
    assets = source.get("assets", {})
    expected_paths = {role: details[0] for role, details in EXPECTED_ASSETS.items()}
    source_asset_map = {
        "BACKGROUND": str(assets.get("background_path", "")).removeprefix("res://"),
        "ANIMATED_OBJECT": str(assets.get("object_path", "")).removeprefix("res://"),
        "TARGET": str(assets.get("target_path", "")).removeprefix("res://"),
    }
    if source_asset_map != expected_paths:
        raise ChallengeVisualPayloadError("Physical asset bindings do not match pinned semantic roles")
    video = source.get("video", {})
    durations = [video.get("hook_duration"), video.get("game_duration"), video.get("reveal_duration"), video.get("cta_duration")]
    if int(video.get("fps", -1)) != 60 or any(not isinstance(x, (int, float)) for x in durations) or sum(float(x) for x in durations) != 15.0:
        raise ChallengeVisualPayloadError("Challenge source timeline must remain 15s at 60 FPS")
    if video.get("game_duration") != 7.0:
        raise ChallengeVisualPayloadError("Challenge GAME duration drifted")
    return {"source_hash_pins": verified, "asset_pins": 3, "asset_dimensions": 3}


def validate_report_shape(report: Mapping[str, Any], root: Path | None = None) -> bool:
    root = root or project_root()
    _, schema = _contract(root)
    if report.get("schema") != PAYLOAD_SCHEMA or report.get("schema_version") != "1.0":
        raise ChallengeVisualPayloadError("Unsupported visual payload summary schema")
    if report.get("status") != "IN_MEMORY_REVIEW_ONLY_SOURCE_TIMEBASE_VISUAL_PAYLOAD_NOT_RENDERER_INPUT":
        raise ChallengeVisualPayloadError("Visual payload summary claims an invalid execution mode")
    if report.get("frozen_c11c_manifest_sha256") != FROZEN_MANIFEST_SHA256 or report.get("challenge_source_sha256") != CHALLENGE_SHA256:
        raise ChallengeVisualPayloadError("Visual payload summary source identity mismatch")
    boundary = report.get("execution_boundary", {})
    expected_boundary = {
        "mode": "GODOT_HEADLESS_IN_MEMORY_REVIEW_ONLY", "payload_written": False,
        "media_output_created": False, "renderer_native_input_emitted": False,
        "renderer_dispatch_invoked": False, "renderer_activation": False,
        "c11c_source_mutation": False, "d4_8": "BLOCKED", "release_authority": "NONE",
        "output_artifact_path": None,
    }
    if boundary != expected_boundary:
        raise ChallengeVisualPayloadError("Execution/governance boundary mismatch")
    payload_identity = report.get("payload_identity", {})
    if payload_identity != {
        "challenge_id": "CHALLENGE_004", "mechanic": "parking_v2", "mechanic_version": "2.0",
        "presentation_profile_id": "social_default_v1", "coordinate_space": "CANVAS_1080X1920",
        "materialization": "IN_MEMORY_ONLY_SOURCE_TIMEBASE",
    }:
        raise ChallengeVisualPayloadError("Payload identity mismatch")
    assets = report.get("asset_nodes")
    if not isinstance(assets, list) or len(assets) != 3 or {a.get("role") for a in assets} != set(EXPECTED_ASSETS):
        raise ChallengeVisualPayloadError("Payload must bind exactly the three canonical physical assets")
    for asset in assets:
        expected = EXPECTED_ASSETS.get(str(asset.get("role")))
        if expected is None or asset.get("resource_path") != "res://" + expected[0] or asset.get("intrinsic_width") != expected[2] or asset.get("intrinsic_height") != expected[3]:
            raise ChallengeVisualPayloadError("Asset node does not match canonical source role/dimensions")
        if asset.get("resource_loaded_as_texture2d") is not True or not re.fullmatch(r"[0-9a-f]{64}", str(asset.get("sha256", ""))):
            raise ChallengeVisualPayloadError("Asset resource/hash proof malformed")
    timeline = report.get("source_timeline", {})
    if timeline.get("fps") != 60 or timeline.get("total_frames") != 900 or timeline.get("duration_seconds") != 15:
        raise ChallengeVisualPayloadError("Source timeline must remain 900 frames at 60 FPS")
    animation = report.get("animation", {})
    if animation.get("frame_source") != "SimulationResult.frames" or animation.get("source_fps") != 60 or animation.get("game_frame_count") != 420 or animation.get("frame_record_count") != 420:
        raise ChallengeVisualPayloadError("Visual animation source must preserve all 420 GAME samples")
    if animation.get("simulation_telemetry_included") is not False or animation.get("winning_frame_sampling_used") is not False or animation.get("delivery_resampling") != "UNRESOLVED_NOT_APPLIED":
        raise ChallengeVisualPayloadError("Visual payload may not bind telemetry or invent sample mapping")
    presentation = report.get("presentation", {})
    if presentation.get("coordinate_projection") != "UNRESOLVED_NOT_APPLIED" or presentation.get("source_coordinate_space") != "CANVAS_1080X1920":
        raise ChallengeVisualPayloadError("Unapproved coordinate projection must remain unresolved")
    determinism = report.get("determinism", {})
    if determinism != {"runtime_repeat_equal": True, "payload_repeat_equal": True, "frame_signature_repeat_equal": True, "simulation_invariance": True}:
        raise ChallengeVisualPayloadError("Payload determinism evidence incomplete")
    try:
        import jsonschema  # type: ignore
    except ImportError:
        jsonschema = None
    if jsonschema is not None:
        jsonschema.Draft202012Validator(schema).validate(dict(report))
    return True


def static_contract_summary(root: Path | None = None) -> dict[str, Any]:
    root = root or project_root()
    contract, schema = _contract(root)
    pins = validate_source_pins(root)
    script = (root / "tools/c11d/d9/materialize_challenge_visual_payload_in_memory.gd").read_text(encoding="utf-8")
    required_tokens = ["run_effective_pipeline", "PresentationBinder.bind", "ResourceLoader.load", "SimulationResult.frames", "renderer_native_input_emitted", "winning_frame_sampling_used"]
    if any(token not in script for token in required_tokens):
        raise ChallengeVisualPayloadError("Godot harness is missing a required contract token")
    forbidden_tokens = ["Image.save_png", "MovieWriter", "RenderingServer", "SubViewport", "Sprite2D.new", "TextureRect.new", "FileAccess.WRITE_READ", "FileAccess.WRITE", "DirAccess.make_dir", ".instantiate()"]
    found = [token for token in forbidden_tokens if token in script]
    if found:
        raise ChallengeVisualPayloadError(f"Godot harness contains rendering/persistence operation: {found[0]}")
    if contract.get("payload_contract", {}).get("renderer_activation") is not False:
        raise ChallengeVisualPayloadError("Renderer must remain OFF")
    if schema.get("properties", {}).get("status", {}).get("const") != "IN_MEMORY_REVIEW_ONLY_SOURCE_TIMEBASE_VISUAL_PAYLOAD_NOT_RENDERER_INPUT":
        raise ChallengeVisualPayloadError("Summary schema status mismatch")
    return {**pins, "contract_schema": 1, "summary_schema": 1, "governance_locks": 10}
