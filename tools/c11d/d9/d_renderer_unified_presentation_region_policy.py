"""Proposal-only shared semantic presentation-region policy for C11-D.

This module reconciles existing text-region declarations for three content types.
It never assigns geometry or executes a render program.
"""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_UNIFIED_PRESENTATION_REGION_POLICY_PROPOSAL_V1.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_UNIFIED_PRESENTATION_REGION_POLICY_PROPOSAL_SCHEMA_V1.json")
LOGICAL_REL = Path("definitions/c11d/production/D_RENDERER_CANDIDATE_LOGICAL_COMPOSITION_V1.json")
FRAME_REL = Path("definitions/c11d/production/D_RENDERER_NEUTRAL_FRAME_PROGRAM_V1.json")
MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
REGISTRY_SHA256 = "967831513eb225e6eafd56496ce0d0a0b0f0e158d205b5985e7bba11b0534ae3"
LOGICAL_SHA256 = "f8a6d83014c329067584decc322c5d6b24be93d5372b2526c67749f3f993cf7e"
FRAME_SHA256 = "3a4ada319d3e6e487c3497446e13b9a9f106396c4d528ab04a633ea2d0c13315"
POLICY_SHA256 = "101092bb32127bb8854a501a9215c0b6cf69581594383903716907d49719c01a"
POLICY_ID = "C11D_UNIFIED_PRESENTATION_SEMANTIC_REGIONS_ALL_CONTENT_TYPES_V1"
CONTRACT_SCHEMA = "C11-D-D9-UNIFIED-PRESENTATION-REGION-POLICY-PROPOSAL-V1"
OUTPUT_SCHEMA = "C11-D-D9-UNIFIED-PRESENTATION-REGION-POLICY-PREVIEW-V1"
SUPPORTED_TYPES = ["visual_loops", "visual_drills", "challenges"]
EXPECTED_LINEAGE = [
    ("release/C11C_FREEZE_PACKAGE_MANIFEST.json", MANIFEST_SHA256),
    ("profiles/delivery/c11c_video_delivery_profiles.json", REGISTRY_SHA256),
    (str(LOGICAL_REL).replace("\\", "/"), LOGICAL_SHA256),
    (str(FRAME_REL).replace("\\", "/"), FRAME_SHA256),
]
EXPECTED_FIELD_TARGETS = {
    "title": {"target_region": "HEADER", "semantic_role": "HEADER_TITLE", "z_order": 20},
    "subtitle": {"target_region": "HEADER", "semantic_role": "HEADER_SUBTITLE", "z_order": 21},
    "call_to_action": {"target_region": "FOOTER", "semantic_role": "FOOTER_CALL_TO_ACTION", "z_order": 80},
    "player_name": {"target_region": "CHALLENGE_OVERLAY", "semantic_role": "CHALLENGE_PLAYER_NAME", "z_order": 40},
    "challenge_label": {"target_region": "CHALLENGE_OVERLAY", "semantic_role": "CHALLENGE_LABEL", "z_order": 41},
}
EXPECTED_REGION_DEFINITIONS = {
    "HEADER": {"semantic_scope": "EDITORIAL_TITLE_AND_SUBTITLE", "mapping_state": "PROPOSED_NOT_APPROVED", "geometry_state": "UNRESOLVED_NO_COORDINATES"},
    "FOOTER": {"semantic_scope": "EDITORIAL_CALL_TO_ACTION", "mapping_state": "PROPOSED_NOT_APPROVED", "geometry_state": "UNRESOLVED_NO_COORDINATES"},
    "CHALLENGE_OVERLAY": {"semantic_scope": "CHALLENGE_SPECIFIC_EDITORIAL_LABELS", "mapping_state": "PROPOSED_NOT_APPROVED", "geometry_state": "UNRESOLVED_NO_COORDINATES"},
}
EXPECTED_MATRIX = [
    {"content_type": "visual_loops", "fields": [{"field": k, **copy.deepcopy(EXPECTED_FIELD_TARGETS[k])} for k in ("title", "subtitle", "call_to_action")], "metadata_only_fields": ["language"], "geometry_state": "UNRESOLVED_NO_COORDINATES", "visibility_windows": "NOT_COMPUTED_BY_REGION_POLICY"},
    {"content_type": "visual_drills", "fields": [{"field": k, **copy.deepcopy(EXPECTED_FIELD_TARGETS[k])} for k in ("title", "subtitle", "call_to_action")], "metadata_only_fields": ["language"], "geometry_state": "UNRESOLVED_NO_COORDINATES", "visibility_windows": "NOT_COMPUTED_BY_REGION_POLICY"},
    {"content_type": "challenges", "fields": [{"field": k, **copy.deepcopy(EXPECTED_FIELD_TARGETS[k])} for k in ("title", "subtitle", "player_name", "challenge_label", "call_to_action")], "metadata_only_fields": ["language"], "geometry_state": "UNRESOLVED_NO_COORDINATES", "visibility_windows": "DELEGATED_TO_SEPARATE_EDITORIAL_WINDOW_PROPOSALS"},
]
EXPECTED_INVARIANTS = [
    "SUPPORT_EXACTLY_VISUAL_LOOPS_VISUAL_DRILLS_AND_CHALLENGES",
    "COPY_CANONICAL_EDITORIAL_FIELD_IDENTITIES_WITHOUT_REWRITING_TEXT",
    "TITLE_AND_SUBTITLE_TARGET_HEADER_FOR_ALL_THREE_CONTENT_TYPES",
    "CALL_TO_ACTION_TARGETS_FOOTER_FOR_ALL_THREE_CONTENT_TYPES",
    "PLAYER_NAME_AND_CHALLENGE_LABEL_TARGET_CHALLENGE_OVERLAY_ONLY",
    "LANGUAGE_IS_METADATA_ONLY_NOT_A_VISIBLE_REGION_ELEMENT",
    "REGION_IDS_ARE_SEMANTIC_LABELS_NOT_COORDINATES_OR_SAFE_AREAS",
    "VISIBILITY_TIMING_REMAINS_SEPARATE_FROM_REGION_MAPPING",
    "NO_SIMULATION_TRUTH_OR_DERIVED_TELEMETRY_IS_BOUND",
]
EXPECTED_UNRESOLVED = {
    "region_geometry": "UNRESOLVED_NO_COORDINATES",
    "safe_area_and_margins": "NOT_DEFINED_NOT_APPROVED",
    "typography_fonts_sizes_weights": "NOT_DEFINED_NOT_APPROVED",
    "color_contrast_outlines_shadows": "NOT_DEFINED_NOT_APPROVED",
    "animation_entry_exit_transitions": "NOT_DEFINED_NOT_APPROVED",
    "z_order_runtime_compositing": "DECLARATIVE_SOURCE_ORDER_ONLY_NOT_RENDERED",
    "content_specific_style_variants": "NOT_DEFINED_NOT_APPROVED",
}
EXPECTED_APPROVAL = {
    "semantic_region_mapping_approved": False, "shared_presentation_region_policy_approved": False,
    "frame_program_approved": False, "renderer_baseline_approved": False, "renderer_baseline_frozen": False,
    "d4_8_authorized": False, "d9_14_full_acceptance": "BLOCKED_AS_REQUIRED",
    "d9_16_full_acceptance": "BLOCKED_AS_REQUIRED", "d9_17_closure": "BLOCKED_NO_GO",
    "d10": "BLOCKED", "release_authority": "NONE",
}
EXPECTED_EXECUTION = {
    "mode": "STATIC_SHARED_PRESENTATION_REGION_POLICY_REVIEW_ONLY", "region_mapping_policy_approved": False,
    "coordinates_emitted": False, "renderer_native_input_emitted": False, "renderer_dispatch_invoked": False,
    "renderer_activation": False, "production_execution": False, "media_created": False,
    "c11c_source_mutation": False, "d4_8": "BLOCKED", "release_authority": "NONE", "video_render_ready": False,
}

class UnifiedPresentationRegionPolicyError(ValueError):
    """The shared semantic presentation mapping proposal is inconsistent or escalated."""

def _root(project_root: Path | str | None = None) -> Path:
    return Path(project_root).resolve() if project_root is not None else Path(__file__).resolve().parents[3]

def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise UnifiedPresentationRegionPolicyError(f"Cannot read required JSON: {path}") from exc
    if not isinstance(value, dict):
        raise UnifiedPresentationRegionPolicyError(f"JSON root must be object: {path}")
    return value

def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def validate_contract(project_root: Path | str | None = None, *, verify_sources: bool = True) -> tuple[dict[str, Any], dict[str, Any]]:
    root = _root(project_root)
    contract = _read_json(root / CONTRACT_REL)
    schema = _read_json(root / SCHEMA_REL)
    expected_lineage = [{"path": p, "sha256": h} for p, h in EXPECTED_LINEAGE]
    authority = {
        "frozen_c11c_manifest_sha256": MANIFEST_SHA256,
        "delivery_profile_registry_sha256": REGISTRY_SHA256,
        "logical_composition_contract_sha256": LOGICAL_SHA256,
        "neutral_frame_program_contract_sha256": FRAME_SHA256,
        "target_profile_id": "REVIEW_720",
    }
    if contract.get("schema") != CONTRACT_SCHEMA or contract.get("schema_version") != "1.0":
        raise UnifiedPresentationRegionPolicyError("Shared presentation policy contract identity/version drift")
    if contract.get("status") != "PROPOSAL_ONLY_NOT_RENDERER_INPUT" or contract.get("supported_content_types") != SUPPORTED_TYPES:
        raise UnifiedPresentationRegionPolicyError("Shared presentation policy must remain proposal-only and cover exactly the three supported content types")
    if contract.get("authority") != authority or contract.get("source_lineage") != expected_lineage:
        raise UnifiedPresentationRegionPolicyError("Shared presentation policy authority/source lineage drift")
    policy = contract.get("policy", {})
    if policy.get("policy_id") != POLICY_ID or policy.get("state") != "PROPOSED_NOT_APPROVED" or policy.get("scope") != "SHARED_SEMANTIC_FIELD_TO_REGION_MAPPING_ONLY":
        raise UnifiedPresentationRegionPolicyError("Shared presentation policy identity, state or scope drift")
    if policy.get("target_delivery_profile_id") != "REVIEW_720" or policy.get("target_canvas") != {"profile_id":"REVIEW_720","width":720,"height":1280,"fps":30,"aspect_ratio":"9:16","source":"PINNED_DELIVERY_PROFILE_METADATA_ONLY"}:
        raise UnifiedPresentationRegionPolicyError("Target canvas metadata must match pinned REVIEW_720 delivery profile identity")
    registry = _read_json(root / "profiles/delivery/c11c_video_delivery_profiles.json")
    review_profile = registry.get("profiles", {}).get("REVIEW_720", {})
    if (review_profile.get("width"), review_profile.get("height"), review_profile.get("fps"), review_profile.get("aspect_ratio")) != (720, 1280, 30, "9:16"):
        raise UnifiedPresentationRegionPolicyError("Pinned delivery registry REVIEW_720 canvas metadata mismatch")
    logical = _read_json(root / LOGICAL_REL)
    frame = _read_json(root / FRAME_REL)
    if logical.get("status") != "PREPARATION_ONLY_NOT_APPROVED_NOT_FROZEN" or frame.get("status") != "PREPARATION_ONLY_NOT_APPROVED_NOT_FROZEN":
        raise UnifiedPresentationRegionPolicyError("Logical composition/frame program source status has escalated")
    logical_targets = logical.get("field_targets")
    frame_targets = frame.get("field_region_targets")
    frame_regions = frame.get("region_definitions")
    if not isinstance(logical_targets, Mapping) or not isinstance(frame_targets, Mapping) or not isinstance(frame_regions, Mapping):
        raise UnifiedPresentationRegionPolicyError("Logical composition/frame-program region declarations are missing")
    expected_region_only = {field: target["target_region"] for field, target in EXPECTED_FIELD_TARGETS.items()}
    if frame_targets != expected_region_only:
        raise UnifiedPresentationRegionPolicyError("Neutral frame program field-to-region mapping drift")
    for field, expected in EXPECTED_FIELD_TARGETS.items():
        actual = logical_targets.get(field)
        if not isinstance(actual, Mapping) or any(actual.get(k) != v for k, v in expected.items()) or actual.get("mapping_state") != "PROPOSED_NOT_APPROVED":
            raise UnifiedPresentationRegionPolicyError(f"Logical composition target mismatch for {field}")
    if frame_regions != EXPECTED_REGION_DEFINITIONS or policy.get("region_definitions") != EXPECTED_REGION_DEFINITIONS:
        raise UnifiedPresentationRegionPolicyError("Semantic region definitions diverge from the neutral frame program")
    if policy.get("field_region_targets") != EXPECTED_FIELD_TARGETS or policy.get("content_matrix") != EXPECTED_MATRIX:
        raise UnifiedPresentationRegionPolicyError("Shared field-to-region matrix drift")
    if policy.get("metadata_only_fields") != ["language"] or policy.get("empty_field_behavior") != "INHERIT_SEPARATE_EDITORIAL_RULES_SUPPRESS_EMPTY_NO_PLACEHOLDER" or policy.get("visibility_timing_behavior") != "NOT_DEFINED_HERE_USE_SEPARATELY_REVIEWED_PROPOSAL_CONTRACTS":
        raise UnifiedPresentationRegionPolicyError("Metadata, empty-field or temporal ownership boundary drift")
    if policy.get("unresolved_presentation_domains") != EXPECTED_UNRESOLVED:
        raise UnifiedPresentationRegionPolicyError("Unresolved presentation domains must remain explicit")
    if policy.get("shared_invariants") != EXPECTED_INVARIANTS:
        raise UnifiedPresentationRegionPolicyError("Shared presentation invariants drift")
    if contract.get("approval_state") != EXPECTED_APPROVAL:
        raise UnifiedPresentationRegionPolicyError("Shared presentation region/frame-program approvals must remain false or blocked")
    if contract.get("execution_boundary") != EXPECTED_EXECUTION:
        raise UnifiedPresentationRegionPolicyError("Shared presentation execution/governance boundary drift")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or schema.get("additionalProperties") is not False:
        raise UnifiedPresentationRegionPolicyError("Shared presentation policy schema must be strict Draft 2020-12")
    try:
        import jsonschema  # type: ignore
    except ImportError:
        jsonschema = None
    if jsonschema is not None:
        try:
            jsonschema.Draft202012Validator(schema).validate(contract)
        except jsonschema.ValidationError as exc:
            raise UnifiedPresentationRegionPolicyError(f"Shared presentation policy schema validation failed: {exc.message}") from exc
    if verify_sources:
        for rel, digest in EXPECTED_LINEAGE:
            path = root / rel
            if not path.is_file():
                raise UnifiedPresentationRegionPolicyError(f"Pinned presentation source missing: {rel}")
            actual = _sha(path.read_bytes())
            if actual != digest:
                raise UnifiedPresentationRegionPolicyError(f"Pinned presentation source SHA-256 mismatch: {rel}")
    return contract, schema

def build_preview(project_root: Path | str | None = None, *, verify_sources: bool = True) -> dict[str, Any]:
    root = _root(project_root)
    contract, _ = validate_contract(root, verify_sources=verify_sources)
    policy = contract["policy"]
    return {
        "schema": OUTPUT_SCHEMA,
        "schema_version": "1.0",
        "policy_id": POLICY_ID,
        "policy_state": "PROPOSED_NOT_APPROVED",
        "proposal_contract_sha256": POLICY_SHA256,
        "target_canvas": copy.deepcopy(policy["target_canvas"]),
        "field_region_targets": copy.deepcopy(policy["field_region_targets"]),
        "region_definitions": copy.deepcopy(policy["region_definitions"]),
        "content_matrix": copy.deepcopy(policy["content_matrix"]),
        "metadata_only_fields": copy.deepcopy(policy["metadata_only_fields"]),
        "empty_field_behavior": policy["empty_field_behavior"],
        "visibility_timing_behavior": policy["visibility_timing_behavior"],
        "unresolved_presentation_domains": copy.deepcopy(policy["unresolved_presentation_domains"]),
        "shared_invariants": copy.deepcopy(policy["shared_invariants"]),
        "policy_approved": False,
        "approval_state": copy.deepcopy(contract["approval_state"]),
        "execution_boundary": copy.deepcopy(contract["execution_boundary"]),
    }

def validate_preview(preview: Mapping[str, Any], project_root: Path | str | None = None, *, verify_sources: bool = True) -> dict[str, Any]:
    expected = build_preview(project_root, verify_sources=verify_sources)
    if dict(preview) != expected:
        raise UnifiedPresentationRegionPolicyError("Shared presentation preview mismatch, promotion or geometry/execution boundary drift")
    return copy.deepcopy(expected)
