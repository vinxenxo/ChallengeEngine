"""Proposal-only unified delivery timebase policy for Loop, Drill and Challenge.

This module verifies a review contract. It does not resample frames, emit renderer input,
create media, or authorize policy/renderer execution.
"""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_UNIFIED_DELIVERY_TIMEBASE_POLICY_PROPOSAL_V1.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_UNIFIED_DELIVERY_TIMEBASE_POLICY_PROPOSAL_SCHEMA_V1.json")
MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
REGISTRY_SHA256 = "967831513eb225e6eafd56496ce0d0a0b0f0e158d205b5985e7bba11b0534ae3"
POLICY_ID = "C11D_UNIFIED_DELIVERY_TIMEBASE_ALL_CONTENT_TYPES_V1"
CONTRACT_SCHEMA = "C11-D-D9-UNIFIED-DELIVERY-TIMEBASE-POLICY-PROPOSAL-V1"
OUTPUT_SCHEMA = "C11-D-D9-UNIFIED-DELIVERY-TIMEBASE-POLICY-PREVIEW-V1"
EXPECTED_LINEAGE = [
    ("release/C11C_FREEZE_PACKAGE_MANIFEST.json", MANIFEST_SHA256),
    ("profiles/delivery/c11c_video_delivery_profiles.json", REGISTRY_SHA256),
    ("challenges/CHALLENGE_004.json", "6a674c02c2d8831a872691954f1cc40e2492193f9b136f60656730a7be686b71"),
    ("definitions/visual_loop_geometric_canonical.json", "648eb36225dd4c090457b4da3c9e8eca218c26c8f995cf02a39914cf3f860dcc"),
    ("definitions/visual_drill_tracking_canonical.json", "54d432c80f190f4ac5dcb8ef5b135e16f18c378da120f35723fd5be944719ec3"),
    ("definitions/c11d/production/D_RENDERER_DELIVERY_TIMEBASE_PROJECTION_V1.json", "4a76bc9613fbc4690f7a2bb3cc047ec5f6334444c4eccefd34fedccb1a830241"),
    ("definitions/c11d/production/D_RENDERER_PROFILE_IDENTITY_SEPARATION_V1.json", "7fa2acc1d38d2ee4e027ded101286d6ee774a9fbb35a633ea451101959ec03e1"),
    ("definitions/c11d/production/D_RENDERER_CHALLENGE_DELIVERY_TIMELINE_REVIEW_V1.json", "5d61271f49296935cef2f8b29210e538738cac01b7a93c4c2adfed3c1f8927df"),
    ("definitions/c11d/production/D_RENDERER_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json", "4bb817b3d782b4f7c61d93a48df9c11766c78018b6c9e7ea43155cb96bda5229"),
    ("definitions/c11d/production/D_RENDERER_CHALLENGE_COORDINATE_PROJECTION_V1.json", "c1caf8e640595bc89957f17ef8bbd7abe80a92cac18cf77974633a1ddde0e264"),
    ("definitions/c11d/production/D_RENDERER_CHALLENGE_SIMULATION_SAMPLE_SELECTION_PROPOSAL_V1.json", "dbd12b8e71f55223b29a479c93c7b4565b2fee3dfe0da54816900cf6da10d33b"),
    ("definitions/c11d/production/D_RENDERER_CHALLENGE_COORDINATE_SAMPLE_COMPOSITION_PROPOSAL_V1.json", "a201d713bbfc5b07fa083d298bd135eaef58e7234746bbc42c6bd7faf13012dd"),
    ("definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json", "609a4d183aac07c2cbe1abaf41444160fdd137217faffbead3aef618320d57dc"),
    ("definitions/c11d/production/D_RENDERER_CHALLENGE_TEMPORAL_ALIGNMENT_POLICY_PROPOSAL_V1.json", "39f6f979a5d8b189cbb3a375b0c33ed7fdb3f2b9bc59fcb587f31a6c65ede5a6"),
]
EXPECTED_TARGET_PROFILE = {
    "profile_id": "REVIEW_720", "width": 720, "height": 1280, "fps": 30,
    "aspect_ratio": "9:16", "codec": "h264", "container": "mp4", "constant_fps": True,
    "profile_fields_are_metadata_only": True, "resolved_alias_count": 0,
}
EXPECTED_MATRIX = [
    {"content_type": "visual_loops", "source_fps": 30, "delivery_fps": 30, "source_frame_count": 600, "delivery_frame_count": 600, "duration_seconds": 20.0, "timebase_mode": "IDENTITY_NO_RESAMPLING", "sampling_policy": "PRESERVE_REQUEST_SCOPED_PAYLOAD_FRAME_TIMELINE", "source_snapshot_count": 600, "delivery_snapshot_count": 600, "delivery_candidate_materialized": False},
    {"content_type": "visual_drills", "source_fps": 30, "delivery_fps": 30, "source_frame_count": 630, "delivery_frame_count": 630, "duration_seconds": 21.0, "timebase_mode": "IDENTITY_NO_RESAMPLING", "sampling_policy": "PRESERVE_REQUEST_SCOPED_PAYLOAD_FRAME_TIMELINE", "source_snapshot_count": 630, "delivery_snapshot_count": 630, "delivery_candidate_materialized": False},
    {"content_type": "challenges", "source_fps": 60, "delivery_fps": 30, "source_frame_count": 900, "delivery_frame_count": 450, "duration_seconds": 15.0, "timebase_mode": "CUMULATIVE_BOUNDARY_PROJECTION_AND_SEPARATE_GAME_SAMPLE_SELECTION_PROPOSAL", "sampling_policy": "EVERY_SECOND_ZERO_BASED_GAME_LOCAL_SNAPSHOT_PROPOSAL_NOT_APPLIED", "source_snapshot_count": 420, "delivery_snapshot_count": 210, "source_phase_boundaries": [0, 180, 600, 780, 900], "delivery_phase_boundaries": [0, 90, 300, 390, 450], "source_phase_frame_counts": [180, 420, 180, 120], "delivery_phase_frame_counts": [90, 210, 90, 60], "winning_frame_source_absolute_index": 574, "winning_frame_delivery_absolute_index": 287, "interpolation": "NONE", "delivery_candidate_materialized": False},
]
EXPECTED_SHARED_INVARIANTS = [
    "DELIVERY_PROFILE_IS_EXPLICIT_AND_RESOLVED_ONCE", "PRESERVE_ELAPSED_DURATION",
    "PRESERVE_PHASE_ORDER_AND_HALF_OPEN_BOUNDARY_CONTINUITY", "DO_NOT_MUTATE_SOURCE_SIMULATION_OR_CANONICAL_CONTENT",
    "NO_INTERPOLATED_SIMULATION_STATE", "WINNING_FRAME_IS_READ_ONLY_AND_NOT_A_SAMPLE_SELECTION_INPUT",
    "CLOSE_CALLS_IS_COUNT_ONLY_AND_NOT_TIMING",
]
EXPECTED_APPROVAL = {
    "unified_delivery_timebase_policy_approved": False, "loop_drill_no_resampling_policy_approved": False,
    "challenge_sample_selection_policy_approved": False, "challenge_temporal_alignment_policy_approved": False,
    "coordinate_projection_policy_approved": False, "editorial_field_window_policy_approved": False,
    "music_audio_policy_approved": False, "renderer_baseline_approved": False, "renderer_baseline_frozen": False,
    "d4_8_authorized": False, "d9_14_full_acceptance": "BLOCKED_AS_REQUIRED",
    "d9_16_full_acceptance": "BLOCKED_AS_REQUIRED", "d9_17_closure": "BLOCKED_NO_GO",
    "d10": "BLOCKED", "release_authority": "NONE",
}
EXPECTED_LOCKS = {
    "mode": "STATIC_UNIFIED_DELIVERY_POLICY_REVIEW_ONLY", "delivery_candidate_materialized": False,
    "payload_files_written": False, "renderer_native_input_emitted": False, "renderer_dispatch_invoked": False,
    "renderer_activation": False, "production_execution": False, "media_created": False,
    "c11c_source_mutation": False, "d4_8": "BLOCKED", "release_authority": "NONE", "video_render_ready": False,
}

class UnifiedDeliveryPolicyError(ValueError):
    """Unified delivery-timebase proposal mismatch or attempted governance escalation."""

def _root(project_root: Path | str | None = None) -> Path:
    return Path(project_root).resolve() if project_root is not None else Path(__file__).resolve().parents[3]

def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise UnifiedDeliveryPolicyError(f"Cannot read required JSON: {path}") from exc
    if not isinstance(value, dict):
        raise UnifiedDeliveryPolicyError(f"JSON root must be object: {path}")
    return value

def _sha(raw: bytes) -> str: return hashlib.sha256(raw).hexdigest()
def _canonical(value: Any) -> str: return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
def sha256_json(value: Any) -> str: return _sha(_canonical(value).encode("utf-8"))

def validate_contract(project_root: Path | str | None = None, *, verify_sources: bool = True) -> tuple[dict[str, Any], dict[str, Any]]:
    root = _root(project_root)
    contract = _read_json(root / CONTRACT_REL)
    schema = _read_json(root / SCHEMA_REL)
    if contract.get("schema") != CONTRACT_SCHEMA or contract.get("schema_version") != "1.0":
        raise UnifiedDeliveryPolicyError("Unified delivery policy contract identity/version drift")
    if contract.get("status") != "PROPOSAL_ONLY_NOT_RENDERER_INPUT":
        raise UnifiedDeliveryPolicyError("Unified delivery policy cannot self-promote status")
    if contract.get("source_lineage") != [{"path": p, "sha256": h} for p, h in EXPECTED_LINEAGE]:
        raise UnifiedDeliveryPolicyError("Unified delivery policy source-lineage declaration drift")
    if contract.get("target_delivery_profile") != EXPECTED_TARGET_PROFILE:
        raise UnifiedDeliveryPolicyError("Target delivery profile or metadata-only boundary drift")
    policy = contract.get("policy", {})
    if policy.get("policy_id") != POLICY_ID or policy.get("state") != "PROPOSED_NOT_APPROVED":
        raise UnifiedDeliveryPolicyError("Unified delivery policy identity/state mismatch")
    if policy.get("target_profile_id") != "REVIEW_720" or policy.get("target_fps") != 30 or policy.get("target_canvas") != [720, 1280] or policy.get("target_profile_metadata_only") is not True:
        raise UnifiedDeliveryPolicyError("Unified delivery target profile drift")
    if contract.get("content_matrix") != EXPECTED_MATRIX:
        raise UnifiedDeliveryPolicyError("Cross-content delivery timebase matrix drift")
    if policy.get("content_specific_timebase_rules") != {
        "visual_loops": "SOURCE_AND_DELIVERY_FPS_MATCH; PRESERVE_REQUEST_SCOPED_PAYLOAD_FRAME_COUNT_AND_ORDER; NO_RESAMPLING",
        "visual_drills": "SOURCE_AND_DELIVERY_FPS_MATCH; PRESERVE_REQUEST_SCOPED_PAYLOAD_FRAME_COUNT_AND_ORDER; NO_RESAMPLING",
        "challenges": "PROJECT_CUMULATIVE_PHASE_BOUNDARIES_60_TO_30; USE_SEPARATE_EVEN_GAME_SNAPSHOT_SELECTION_PROPOSAL; NO_INTERPOLATION",
    }:
        raise UnifiedDeliveryPolicyError("Content-specific timebase rules drift")
    if policy.get("common_timebase_invariants") != EXPECTED_SHARED_INVARIANTS:
        raise UnifiedDeliveryPolicyError("Common delivery-timebase invariants drift")
    if policy.get("audio_music_policy") != "OUT_OF_SCOPE_NOT_DEFINED_NOT_EMITTED" or contract.get("excluded_policy_domains", {}).get("audio_music") != "OUT_OF_SCOPE_NOT_DEFINED_NOT_EMITTED":
        raise UnifiedDeliveryPolicyError("Unified delivery policy cannot claim audio/music processing")
    if contract.get("approval_state") != EXPECTED_APPROVAL:
        raise UnifiedDeliveryPolicyError("Unified delivery policy approval locks drift")
    if contract.get("execution_boundary") != EXPECTED_LOCKS:
        raise UnifiedDeliveryPolicyError("Unified delivery policy execution/governance locks drift")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or schema.get("$id") != "urn:c11d:unified-delivery-timebase-policy-proposal:v1" or schema.get("additionalProperties") is not False:
        raise UnifiedDeliveryPolicyError("Unified delivery policy schema identity/strictness drift")
    if set(schema.get("required", [])) != set(schema.get("properties", {})):
        raise UnifiedDeliveryPolicyError("Unified delivery policy schema required/property mismatch")
    if verify_sources:
        for rel, expected_hash in EXPECTED_LINEAGE:
            source = root / rel
            if not source.is_file() or _sha(source.read_bytes()) != expected_hash:
                raise UnifiedDeliveryPolicyError(f"Pinned source missing/hash mismatch: {rel}")
    # Explicit profile registry resolution: aliases are forbidden in this proposal.
    registry = _read_json(root / "profiles/delivery/c11c_video_delivery_profiles.json")
    profile = registry.get("profiles", {}).get("REVIEW_720", {})
    if any(profile.get(key) != EXPECTED_TARGET_PROFILE[key] for key in ("width", "height", "fps", "aspect_ratio", "codec", "container", "constant_fps")):
        raise UnifiedDeliveryPolicyError("Pinned REVIEW_720 profile facts differ from the delivery proposal")
    for rel, expected_kind in (("definitions/visual_loop_geometric_canonical.json", "visual_loop"), ("definitions/visual_drill_tracking_canonical.json", "visual_drill")):
        canonical = _read_json(root / rel)
        if canonical.get("kind") != expected_kind or canonical.get("payload", {}).get("fps") != 30:
            raise UnifiedDeliveryPolicyError(f"Canonical 30 FPS source definition drift: {expected_kind}")
    # All referenced proposals must still be unapproved; the review may not promote them.
    temporal = _read_json(root / "definitions/c11d/production/D_RENDERER_CHALLENGE_TEMPORAL_ALIGNMENT_POLICY_PROPOSAL_V1.json")
    sample = _read_json(root / "definitions/c11d/production/D_RENDERER_CHALLENGE_SIMULATION_SAMPLE_SELECTION_PROPOSAL_V1.json")
    composition = _read_json(root / "definitions/c11d/production/D_RENDERER_CHALLENGE_COORDINATE_SAMPLE_COMPOSITION_PROPOSAL_V1.json")
    loop_drill = _read_json(root / "definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json")
    if temporal.get("policy", {}).get("state") != "PROPOSED_NOT_APPROVED" or sample.get("status") != "PROPOSAL_ONLY_NOT_RENDERER_INPUT" or composition.get("status") != "PROPOSED_NOT_APPROVED_NOT_FROZEN" or loop_drill.get("mapping_policy", {}).get("state") != "PROPOSED_NOT_APPROVED":
        raise UnifiedDeliveryPolicyError("A referenced sub-policy is missing or was promoted outside the approval process")
    if verify_sources:
        try:
            import jsonschema  # type: ignore
        except ImportError:
            jsonschema = None
        if jsonschema is not None:
            try: jsonschema.Draft202012Validator(schema).validate(contract)
            except jsonschema.ValidationError as exc: raise UnifiedDeliveryPolicyError(f"Unified delivery policy schema validation failed: {exc.message}") from exc
    return contract, schema

def build_preview(project_root: Path | str | None = None, *, verify_sources: bool = True) -> dict[str, Any]:
    root = _root(project_root)
    contract, _ = validate_contract(root, verify_sources=verify_sources)
    preview = {
        "schema": OUTPUT_SCHEMA,
        "schema_version": "1.0",
        "policy_id": POLICY_ID,
        "policy_state": "PROPOSED_NOT_APPROVED",
        "proposal_contract_sha256": _sha((root / CONTRACT_REL).read_bytes()),
        "target_delivery_profile": copy.deepcopy(contract["target_delivery_profile"]),
        "content_matrix": copy.deepcopy(contract["content_matrix"]),
        "shared_invariants": copy.deepcopy(EXPECTED_SHARED_INVARIANTS),
        "audio_music_policy": "OUT_OF_SCOPE_NOT_DEFINED_NOT_EMITTED",
        "delivery_candidate_materialized": False,
        "policy_approved": False,
        "renderer_native_input_emitted": False,
        "media_created": False,
        "approval_state": copy.deepcopy(contract["approval_state"]),
        "execution_boundary": copy.deepcopy(contract["execution_boundary"]),
    }
    return preview

def validate_preview(preview: Mapping[str, Any], project_root: Path | str | None = None, *, verify_sources: bool = True) -> dict[str, Any]:
    expected = build_preview(project_root, verify_sources=verify_sources)
    if dict(preview) != expected:
        raise UnifiedDeliveryPolicyError("Unified delivery policy preview mismatch, policy promotion, or execution boundary drift")
    return copy.deepcopy(expected)

