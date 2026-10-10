"""Static contract for C11-D's proposed Challenge coordinate projection preview.

The Godot harness is the authority for the runtime/frame projection. This
module validates pinned source lineage, transform math and safety boundaries;
it never invokes Godot, writes payloads, or creates media.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any, Mapping, Sequence

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_COORDINATE_PROJECTION_V1.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_COORDINATE_PROJECTION_SCHEMA_V1.json")
CONTRACT_ID = "C11-D-D9-RENDERER-CHALLENGE-COORDINATE-PROJECTION-CONTRACT-V1"
REPORT_ID = "C11-D-D9-RENDERER-CHALLENGE-COORDINATE-PROJECTION-PREVIEW-V1"
FROZEN_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
EXPECTED_SOURCE_PINS: dict[str, str] = {
    "challenges/CHALLENGE_004.json": "6a674c02c2d8831a872691954f1cc40e2492193f9b136f60656730a7be686b71",
    "core/presentation/CoordinateMapper.gd": "244bace2eaf87e29d653715ae18c0b4824cdf9503e915932be53d0f52bbe461c",
    "core/presentation/PresentationProfile.gd": "187b1cf8ab96b9031785a0f36b0054a60383c97cb3d81906c7d9bbcd373bef24",
    "core/presentation/ChallengePresentationBinder.gd": "755ecfc9cc6e1ee51738938583217ab8a470c1a1f290bb107e91e19990d74b47",
    "core/execution/ChallengeRuntimeBridge.gd": "c53f04df064b3697f8dd02cd779f8ef002a4e3e2d40fa0e01aa7d9b1a80a8191",
    "core/execution/ChallengeTimelineBuilder.gd": "35a47ad126a2e11577933a03b251f47732e580693e5c08e45d3b6af047c8c9af",
    "core/mechanics/parking/ParkingMechanicV2.gd": "c78dbc1adcc95ad4981f3c704c69630edc54c25473c479f10bb154efe6f105cd",
    "core/data/FrameSnapshot.gd": "61060d0937063400447cd5f2513265cb82d8e38017f5bd097c2870da03967180",
    "profiles/delivery/c11c_video_delivery_profiles.json": "967831513eb225e6eafd56496ce0d0a0b0f0e158d205b5985e7bba11b0534ae3",
    "assets/c6/garage_background.svg": "c9d8acdae725ca7726fc8ad23a046e4aac4d9e454b45db40d2c770732b31ab1e",
    "assets/c6/car.svg": "93a6f78d9654f7917ab2287800858a937e9c68c458cc60bf417d6f2b98c1a96d",
    "assets/c6/parking_target.svg": "ec2dcafd7dfc99ff501eb2d93b93906680a30c48cf0741807cbbdd915a18cfb3",
    "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_PREVIEW_V1.json": "67daa1f83ac151906059695bb4d87974819c2d16d3715b78b00657bfdac54f7a",
}
EXPECTED_SIZES = {
    "BACKGROUND": (1080, 1920),
    "ANIMATED_OBJECT": (160, 320),
    "TARGET": (200, 400),
}


class CoordinateProjectionError(ValueError):
    """Raised when the coordinate-projection contract is inconsistent."""


def project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise CoordinateProjectionError(f"Cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise CoordinateProjectionError(f"Expected JSON object: {path}")
    return value


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_json(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def nearly_equal(left: float, right: float, tolerance: float = 1e-8) -> bool:
    return math.isfinite(float(left)) and math.isfinite(float(right)) and abs(float(left) - float(right)) <= tolerance


def projection_facts(
    source_size: Sequence[int] = (1080, 1920),
    presentation_size: Sequence[int] = (540, 960),
    delivery_size: Sequence[int] = (720, 1280),
) -> dict[str, Any]:
    if any(len(size) != 2 for size in (source_size, presentation_size, delivery_size)):
        raise CoordinateProjectionError("Every canvas size must be a width/height pair")
    src_w, src_h = map(int, source_size)
    pres_w, pres_h = map(int, presentation_size)
    out_w, out_h = map(int, delivery_size)
    if min(src_w, src_h, pres_w, pres_h, out_w, out_h) <= 0:
        raise CoordinateProjectionError("Canvas dimensions must be positive")
    source_scale_x, source_scale_y = pres_w / src_w, pres_h / src_h
    delivery_scale_x, delivery_scale_y = out_w / pres_w, out_h / pres_h
    if not nearly_equal(source_scale_x, source_scale_y):
        raise CoordinateProjectionError("Source-to-presentation transform is non-uniform")
    if not nearly_equal(delivery_scale_x, delivery_scale_y):
        raise CoordinateProjectionError("Presentation-to-delivery transform is non-uniform")
    return {
        "source_size": [src_w, src_h],
        "presentation_source_canvas": [pres_w, pres_h],
        "delivery_size": [out_w, out_h],
        "source_to_presentation_scale": [source_scale_x, source_scale_y],
        "presentation_to_delivery_scale": [delivery_scale_x, delivery_scale_y],
        "combined_scale": [source_scale_x * delivery_scale_x, source_scale_y * delivery_scale_y],
    }


def project_point(position: Sequence[float], facts: Mapping[str, Any]) -> dict[str, list[float]]:
    if len(position) != 2:
        raise CoordinateProjectionError("Position must be a pair")
    x, y = float(position[0]), float(position[1])
    if not math.isfinite(x) or not math.isfinite(y):
        raise CoordinateProjectionError("Position coordinates must be finite")
    sx, sy = facts["source_to_presentation_scale"]
    dx, dy = facts["presentation_to_delivery_scale"]
    p = [x * sx, y * sy]
    d = [p[0] * dx, p[1] * dy]
    return {"source": [x, y], "presentation_canvas": p, "delivery": d}


def projected_asset_size(size: Sequence[int], facts: Mapping[str, Any]) -> list[float]:
    if len(size) != 2 or int(size[0]) <= 0 or int(size[1]) <= 0:
        raise CoordinateProjectionError("Asset intrinsic size must be a positive width/height pair")
    sx, sy = facts["combined_scale"]
    return [float(size[0]) * float(sx), float(size[1]) * float(sy)]


def validate_contract_and_sources(root: Path | None = None) -> dict[str, Any]:
    root = root or project_root()
    contract = read_json(root / CONTRACT_REL)
    schema = read_json(root / SCHEMA_REL)
    if contract.get("schema") != CONTRACT_ID or contract.get("schema_version") != "1.0":
        raise CoordinateProjectionError("Unsupported coordinate projection contract identity/version")
    if contract.get("status") != "PROPOSED_NOT_APPROVED_NOT_FROZEN":
        raise CoordinateProjectionError("Proposal cannot approve or freeze itself")
    if contract.get("authority", {}).get("frozen_c11c_manifest_sha256") != FROZEN_MANIFEST_SHA256:
        raise CoordinateProjectionError("Frozen C11-C manifest identity mismatch")
    if contract.get("authority", {}).get("challenge_source_sha256") != EXPECTED_SOURCE_PINS["challenges/CHALLENGE_004.json"]:
        raise CoordinateProjectionError("Challenge source pin mismatch")
    if contract.get("source_pins") != [
        {"path": path, "sha256": sha} for path, sha in EXPECTED_SOURCE_PINS.items()
    ]:
        raise CoordinateProjectionError("Source pin registry differs from the contract constants")
    if schema.get("$id") != "urn:c11d:renderer-challenge-coordinate-projection-preview:v1":
        raise CoordinateProjectionError("Coordinate projection schema identity mismatch")
    pins_verified = 0
    for rel, expected in EXPECTED_SOURCE_PINS.items():
        path = root / rel
        if not path.is_file():
            raise CoordinateProjectionError(f"Pinned source missing: {rel}")
        actual = sha256_file(path)
        if actual != expected:
            raise CoordinateProjectionError(f"Pinned source hash mismatch: {rel}; expected={expected}, actual={actual}")
        pins_verified += 1
    facts = projection_facts()
    expected_facts = {
        "source_to_presentation_scale": [0.5, 0.5],
        "presentation_to_delivery_scale": [4 / 3, 4 / 3],
        "combined_scale": [2 / 3, 2 / 3],
    }
    for key, values in expected_facts.items():
        if len(facts[key]) != 2 or not all(nearly_equal(a, b) for a, b in zip(facts[key], values)):
            raise CoordinateProjectionError(f"Projection scale mismatch: {key}")
    target = project_point([850.0, 960.0], facts)
    if not nearly_equal(target["presentation_canvas"][0], 425.0) or not nearly_equal(target["presentation_canvas"][1], 480.0):
        raise CoordinateProjectionError("Target position does not map to the presentation canvas as expected")
    if not nearly_equal(target["delivery"][0], 850 * 2 / 3) or not nearly_equal(target["delivery"][1], 640.0):
        raise CoordinateProjectionError("Target delivery position mismatch")
    asset_sizes = {role: projected_asset_size(size, facts) for role, size in EXPECTED_SIZES.items()}
    if not nearly_equal(asset_sizes["BACKGROUND"][0], 720.0) or not nearly_equal(asset_sizes["BACKGROUND"][1], 1280.0):
        raise CoordinateProjectionError("Background must fill the delivery canvas in projected base geometry")
    if contract.get("projection", {}).get("state") != "PROPOSED_NOT_APPROVED":
        raise CoordinateProjectionError("Projection must remain unapproved")
    locks = contract.get("governance_locks", {})
    if locks.get("policy_approved") is not False or locks.get("renderer_input_emitted") is not False or locks.get("renderer_activation") is not False or locks.get("media_created") is not False or locks.get("d4_8") != "BLOCKED" or locks.get("release_authority") != "NONE":
        raise CoordinateProjectionError("Governance lock mismatch")
    return {
        "source_hash_pins": pins_verified,
        "contract_schema_valid": True,
        "projection_math_valid": True,
        "projected_asset_sizes": asset_sizes,
        "target_position": target,
        "projection_facts": facts,
    }


def validate_report_shape(report: Mapping[str, Any], root: Path | None = None) -> bool:
    root = root or project_root()
    _, schema = (read_json(root / CONTRACT_REL), read_json(root / SCHEMA_REL))
    if report.get("schema") != REPORT_ID or report.get("schema_version") != "1.0":
        raise CoordinateProjectionError("Unsupported coordinate projection report schema")
    if report.get("status") != "IN_MEMORY_REVIEW_ONLY_PROJECTION_PREVIEW_NOT_RENDERER_INPUT":
        raise CoordinateProjectionError("Report claims an invalid materialization mode")
    if report.get("frozen_c11c_manifest_sha256") != FROZEN_MANIFEST_SHA256 or report.get("challenge_source_sha256") != EXPECTED_SOURCE_PINS["challenges/CHALLENGE_004.json"]:
        raise CoordinateProjectionError("Report source identity mismatch")
    projection = report.get("projection", {})
    if projection.get("policy_id") != "C11D_CHALLENGE_COORDINATE_PROJECTION_1080_TO_540_TO_REVIEW720_V1" or projection.get("state") != "PROPOSED_NOT_APPROVED":
        raise CoordinateProjectionError("Projection policy identity/state mismatch")
    if projection.get("source_coordinate_space") != "CANVAS_1080X1920":
        raise CoordinateProjectionError("Source coordinate space mismatch")
    stages = projection.get("stage_scales", [])
    combined = projection.get("combined_scale", [])
    if not isinstance(stages, list) or len(stages) != 2 or any(not isinstance(stage, list) or len(stage) != 2 for stage in stages):
        raise CoordinateProjectionError("Transform stages are malformed")
    expected_stages = [[0.5, 0.5], [4 / 3, 4 / 3]]
    if not all(nearly_equal(a, b, 1e-5) for stage, expected in zip(stages, expected_stages) for a, b in zip(stage, expected)):
        raise CoordinateProjectionError("Transform stages are inconsistent")
    if not isinstance(combined, list) or len(combined) != 2 or not all(nearly_equal(a, 2 / 3, 1e-5) for a in combined):
        raise CoordinateProjectionError("Combined transform scale is inconsistent")
    src = report.get("source_timeline", {})
    delivery = report.get("delivery_profile", {})
    if src != {"fps": 60, "total_frames": 900, "duration_seconds": 15.0, "game_frame_count": 420}:
        raise CoordinateProjectionError("Source timeline was changed")
    if delivery != {"profile_id": "REVIEW_720", "fps": 30, "width": 720, "height": 1280, "total_frames": 450, "duration_seconds": 15.0}:
        raise CoordinateProjectionError("Delivery timing/profile mismatch")
    frames = report.get("projected_frames", {})
    if frames.get("source_records") != 420 or frames.get("projected_records") != 420 or frames.get("order_preserved") is not True or frames.get("local_scale_preserved") is not True or frames.get("other_snapshot_fields_preserved") is not True:
        raise CoordinateProjectionError("Projected GAME frame record count/order/invariants mismatch")
    for field in ("source_records_sha256", "projected_records_sha256"):
        if not isinstance(frames.get(field), str) or len(str(frames[field])) != 64:
            raise CoordinateProjectionError(f"Malformed frame digest: {field}")
    if report.get("determinism") != {"runtime_repeat_equal": True, "projection_repeat_equal": True, "source_frame_signature_repeat_equal": True}:
        raise CoordinateProjectionError("Determinism evidence missing")
    if report.get("simulation_invariance") != {"frame_signature_unchanged": True, "winning_frame_unchanged": True, "metrics_unchanged": True, "frame_count_unchanged": True}:
        raise CoordinateProjectionError("Simulation invariance failed")
    boundary = report.get("execution_boundary", {})
    expected_boundary = {"mode": "GODOT_HEADLESS_IN_MEMORY_REVIEW_ONLY", "source_mutation": False, "projected_payload_written": False, "renderer_native_input_emitted": False, "renderer_dispatch_invoked": False, "renderer_activation": False, "media_created": False, "d4_8": "BLOCKED", "release_authority": "NONE"}
    if boundary != expected_boundary:
        raise CoordinateProjectionError("Execution/governance boundary mismatch")
    import jsonschema  # type: ignore
    jsonschema.Draft202012Validator(schema).validate(dict(report))
    return True


def static_contract_summary(root: Path | None = None) -> dict[str, Any]:
    return validate_contract_and_sources(root)
