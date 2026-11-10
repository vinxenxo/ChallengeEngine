"""Proposal-only editorial field windows for continuous Visual Loop and Drill payloads.

This module validates source contracts and computes review metadata in memory. It
never writes payloads, emits renderer input, dispatches a renderer, or creates media.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_SCHEMA_V1.json")
EXPECTED_SOURCES = {
    "release/C11C_FREEZE_PACKAGE_MANIFEST.json": "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953",
    "profiles/delivery/c11c_video_delivery_profiles.json": "967831513eb225e6eafd56496ce0d0a0b0f0e158d205b5985e7bba11b0534ae3",
    "definitions/visual_loop_geometric_canonical.json": "648eb36225dd4c090457b4da3c9e8eca218c26c8f995cf02a39914cf3f860dcc",
    "definitions/visual_drill_tracking_canonical.json": "54d432c80f190f4ac5dcb8ef5b135e16f18c378da120f35723fd5be944719ec3",
    "definitions/c11d/production/D_RENDERER_VISUAL_PAYLOAD_MATERIALIZATION_PREVIEW_V1.json": "53b6da626131c56f770172129e0cc1cd40947098228bfaa499a1e8e8e76ad411",
    "definitions/c11d/production/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1.json": "2075da9c33c689861a68d3bd8fb19b7ed593c6e76010ab200880746aa6d1a470",
    "definitions/c11d/production/D_RENDERER_CANDIDATE_LOGICAL_COMPOSITION_V1.json": "f8a6d83014c329067584decc322c5d6b24be93d5372b2526c67749f3f993cf7e",
    "definitions/c11d/production/D_RENDERER_NEUTRAL_FRAME_PROGRAM_V1.json": "3a4ada319d3e6e487c3497446e13b9a9f106396c4d528ab04a633ea2d0c13315",
    "definitions/c11d/production/D_RENDERER_TEMPORAL_BOUND_PREVIEW_V1.json": "ff203026f6a4dee4ae2ccb47992b3dde7c7d9644320427eabd17eddc0a4ac646",
    "definitions/c11d/production/D_RENDERER_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json": "4bb817b3d782b4f7c61d93a48df9c11766c78018b6c9e7ea43155cb96bda5229",
}
EXPECTED_FIXTURES = {
    "visual_loops": {"frame_count": 600, "fps": 30, "duration_seconds": 20.0, "instance_id": "D-VLP-5ac67e64ff717d97", "payload_instance_sha256": "5ac67e64ff717d9756b37152dd1ee1ff81a1b0e754f83c06a618964c9a62e090"},
    "visual_drills": {"frame_count": 630, "fps": 30, "duration_seconds": 21.0, "instance_id": "D-VDP-1a96afdd7a0d950e", "payload_instance_sha256": "1a96afdd7a0d950ef3eabb5531fe13496b4206a7d4fd1d7f233892b0329a592b"},
}
VISIBLE_FIELD_REGIONS = {"title": "HEADER", "subtitle": "HEADER", "call_to_action": "FOOTER"}
METADATA_ONLY_FIELDS = {"language"}


class FieldWindowProposalError(ValueError):
    """Raised when the proposal, source pins, or input editorial fields are inconsistent."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise FieldWindowProposalError(f"cannot read valid JSON: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise FieldWindowProposalError(f"JSON root must be an object: {path}")
    return data


def validate_contract(root: Path) -> dict[str, Any]:
    root = root.resolve()
    contract = load_json(root / CONTRACT_REL)
    schema = load_json(root / SCHEMA_REL)
    if contract.get("schema") != "C11-D-D9-RENDERER-LOOP-DRILL-EDITORIAL-FIELD-WINDOW-PROPOSAL-V1":
        raise FieldWindowProposalError("unexpected loop/drill field-window proposal identity")
    if contract.get("status") != "PROPOSAL_ONLY_NOT_RENDERER_INPUT":
        raise FieldWindowProposalError("editorial field-window proposal cannot be promoted by validation")
    try:
        import jsonschema  # type: ignore
        jsonschema.Draft202012Validator(schema).validate(contract)
    except ImportError as exc:
        raise FieldWindowProposalError("jsonschema is required for contract validation") from exc
    except Exception as exc:
        raise FieldWindowProposalError(f"JSON Schema validation failed: {exc}") from exc

    actual_lineage = {(row.get("path"), row.get("sha256")) for row in contract["source_lineage"]}
    expected_lineage = set(EXPECTED_SOURCES.items())
    if actual_lineage != expected_lineage:
        raise FieldWindowProposalError("source_lineage does not match the exact pinned source set")
    authority = contract["authority"]
    for path, digest in EXPECTED_SOURCES.items():
        source = root / path
        if not source.is_file():
            raise FieldWindowProposalError(f"required lineage source is missing: {path}")
        if sha256_file(source) != digest:
            raise FieldWindowProposalError(f"source SHA-256 mismatch: {path}")

    named_authority_pins = {
        "frozen_c11c_manifest_sha256": EXPECTED_SOURCES["release/C11C_FREEZE_PACKAGE_MANIFEST.json"],
        "delivery_profile_registry_sha256": EXPECTED_SOURCES["profiles/delivery/c11c_video_delivery_profiles.json"],
        "visual_loop_canonical_sha256": EXPECTED_SOURCES["definitions/visual_loop_geometric_canonical.json"],
        "visual_drill_canonical_sha256": EXPECTED_SOURCES["definitions/visual_drill_tracking_canonical.json"],
        "visual_payload_preview_contract_sha256": EXPECTED_SOURCES["definitions/c11d/production/D_RENDERER_VISUAL_PAYLOAD_MATERIALIZATION_PREVIEW_V1.json"],
        "editorial_review_manifest_sha256": EXPECTED_SOURCES["definitions/c11d/production/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1.json"],
        "logical_composition_contract_sha256": EXPECTED_SOURCES["definitions/c11d/production/D_RENDERER_CANDIDATE_LOGICAL_COMPOSITION_V1.json"],
        "neutral_frame_program_contract_sha256": EXPECTED_SOURCES["definitions/c11d/production/D_RENDERER_NEUTRAL_FRAME_PROGRAM_V1.json"],
        "temporal_bound_preview_contract_sha256": EXPECTED_SOURCES["definitions/c11d/production/D_RENDERER_TEMPORAL_BOUND_PREVIEW_V1.json"],
        "challenge_field_window_proposal_sha256": EXPECTED_SOURCES["definitions/c11d/production/D_RENDERER_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json"],
    }
    for name, digest in named_authority_pins.items():
        if authority.get(name) != digest:
            raise FieldWindowProposalError(f"authority SHA-256 pin mismatch: {name}")

    policy = contract["mapping_policy"]
    if policy.get("state") != "PROPOSED_NOT_APPROVED" or policy.get("approval_state") != "PROPOSED_NOT_APPROVED":
        raise FieldWindowProposalError("mapping policy must remain PROPOSED_NOT_APPROVED")
    field_rows = policy["visible_fields"]
    if {row["field_id"]: row["target_region"] for row in field_rows} != VISIBLE_FIELD_REGIONS:
        raise FieldWindowProposalError("visual field target regions disagree with pinned logical-composition contract")
    logical = load_json(root / "definitions/c11d/production/D_RENDERER_CANDIDATE_LOGICAL_COMPOSITION_V1.json")
    expected_fields = ["title", "subtitle", "call_to_action", "language"]
    for content_type in ("visual_loops", "visual_drills"):
        if logical.get("required_editorial_fields", {}).get(content_type) != expected_fields:
            raise FieldWindowProposalError(f"logical-composition required fields changed for {content_type}")

    fixtures = {item["content_type"]: item for item in contract["review_fixtures"]}
    if set(fixtures) != set(EXPECTED_FIXTURES):
        raise FieldWindowProposalError("review fixtures must cover exactly visual_loops and visual_drills")
    for content_type, expected in EXPECTED_FIXTURES.items():
        fixture = fixtures[content_type]
        for key, value in expected.items():
            if fixture.get(key) != value:
                raise FieldWindowProposalError(f"review fixture identity mismatch: {content_type}.{key}")
        if fixture["frame_count"] != fixture["fps"] * fixture["duration_seconds"]:
            raise FieldWindowProposalError(f"fixture duration/frame-count mismatch: {content_type}")
        if fixture.get("delivery_profile_id") != "REVIEW_720" or fixture.get("timing_source") != "MATERIALIZED_REQUEST_SCOPED_PAYLOAD":
            raise FieldWindowProposalError(f"fixture timing authority mismatch: {content_type}")

    approval = contract["approval_state"]
    must_remain_false = ("loop_editorial_field_mapping_approved", "drill_editorial_field_mapping_approved", "field_window_policy_approved", "delivery_timebase_projection_approved", "renderer_baseline_approved", "renderer_baseline_frozen", "d4_8_authorized")
    if any(approval.get(key) is not False for key in must_remain_false):
        raise FieldWindowProposalError("approval state attempted to cross a governance boundary")
    boundary = contract["execution_boundary"]
    if boundary.get("renderer") != "OFF" or boundary.get("d4_8") != "BLOCKED" or boundary.get("release_authority") != "NONE":
        raise FieldWindowProposalError("renderer, D4.8 and release locks must remain closed")
    for key in ("renderer_native_input_emitted", "renderer_dispatch_invoked", "renderer_activation", "production_execution", "payload_files_written", "media_created", "c11c_source_mutation", "video_render_ready"):
        if boundary.get(key) is not False:
            raise FieldWindowProposalError(f"execution lock must remain false: {key}")
    return {"contract": contract, "schema": schema, "fixtures": fixtures}


def propose_field_windows(content_type: str, frame_count: int, editorial_fields: Mapping[str, str]) -> dict[str, Any]:
    """Return review metadata; no files or renderer-native input are emitted."""
    if content_type not in EXPECTED_FIXTURES:
        raise FieldWindowProposalError("unsupported content type; this proposal supports visual_loops and visual_drills only")
    if isinstance(frame_count, bool) or not isinstance(frame_count, int) or frame_count <= 0:
        raise FieldWindowProposalError("frame_count must be a positive integer from the materialized payload")
    if not isinstance(editorial_fields, Mapping):
        raise FieldWindowProposalError("editorial_fields must be a mapping")
    allowed = set(VISIBLE_FIELD_REGIONS) | METADATA_ONLY_FIELDS
    unknown = set(editorial_fields) - allowed
    if unknown:
        raise FieldWindowProposalError("unknown editorial field; explicit mapping required: " + ", ".join(sorted(unknown)))
    required = {"title", "subtitle", "call_to_action", "language"}
    if set(editorial_fields) != required:
        raise FieldWindowProposalError("all four canonical universal editorial fields must be supplied exactly once")
    for field_id, value in editorial_fields.items():
        if not isinstance(value, str):
            raise FieldWindowProposalError(f"editorial value must be a string: {field_id}")

    windows: list[dict[str, Any]] = []
    suppressed: list[str] = []
    metadata_only: list[str] = ["language"]
    for field_id, region in VISIBLE_FIELD_REGIONS.items():
        value = editorial_fields[field_id]
        if value == "":
            suppressed.append(field_id)
        else:
            windows.append({"field_id": field_id, "target_region": region, "start_frame": 0, "end_frame": frame_count, "frame_count": frame_count, "state": "PROPOSED_VISIBLE_WINDOW", "source_text": value})
    return {
        "content_type": content_type,
        "frame_count": frame_count,
        "interval_convention": "ZERO_BASED_HALF_OPEN",
        "field_windows": windows,
        "suppressed_empty_fields": suppressed,
        "metadata_only_fields": metadata_only,
        "policy_state": "PROPOSED_NOT_APPROVED",
        "renderer_native_input_emitted": False,
        "media_created": False,
    }


def status_line(result: dict[str, Any]) -> str:
    contract = result["contract"]
    fixtures = result["fixtures"]
    loop = fixtures["visual_loops"]
    drill = fixtures["visual_drills"]
    return (
        "C11-D RENDERER LOOP/DRILL EDITORIAL FIELD-WINDOW PROPOSAL PASS"
        f" | loop={loop['frame_count']}@{loop['fps']}FPS"
        f" | drill={drill['frame_count']}@{drill['fps']}FPS"
        " | visible_fields=title,subtitle,call_to_action"
        " | rule=FULL_CONTINUOUS_SPAN_NONEMPTY_ONLY"
        " | language=METADATA_ONLY"
        " | subphases=NOT_INFERRED"
        " | policy=PROPOSED_NOT_APPROVED"
        " | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE"
    )
