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
REVIEW_MANIFEST_REL = Path("definitions/c11d/production/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1.json")
REVIEW_MANIFEST_ARCHIVE_REL = Path("docs/history/c11e/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1_PRE_D98_LINEAGE_REFRESH_20261106.json")
LINEAGE_RECONCILIATION_REL = Path("docs/current/e/C11E_E4C_A3_REVIEW_MANIFEST_LINEAGE_RECONCILIATION_20261110_V2.json")
OPERATOR_DECISION_REL = Path("docs/current/e/C11E_E4B_OPERATOR_POLICY_DECISION_RECORD_20261106_V1.json")
D98_RECONCILIATION_REL = Path("docs/current/e/C11E_E4B_D98_D99_SEMANTIC_RECONCILIATION_20261107_V4.md")
CURRENT_REVIEW_MANIFEST_SHA256 = "5702092bc1c88e4b333dd30cc150f0d383cd2006121037b0198905c75a3af795"
HISTORICAL_REVIEW_MANIFEST_SHA256 = "2075da9c33c689861a68d3bd8fb19b7ed593c6e76010ab200880746aa6d1a470"
CURRENT_D98_MODEL_SHA256 = "dabb458fc2215156ddb5ebea7e8ebec811098886ce2858733ba9fb13f6075ccb"
OPERATOR_DECISION_SHA256 = "49efd5494f351f09d7597c4699e9c12e361b36884b6bfadacd822e6ff1480e04"
A3_PROPOSAL_SHA256 = "609a4d183aac07c2cbe1abaf41444160fdd137217faffbead3aef618320d57dc"
A1_PROPOSAL_SHA256 = "101092bb32127bb8854a501a9215c0b6cf69581594383903716907d49719c01a"
LINEAGE_RECONCILIATION_SHA256 = "aec0e387f167f4b821b7d94f06a67f78f498be939fe3cda857d20ce550819cac"
D98_RECONCILIATION_SHA256 = "8ec940c0eafddfdea2ded77d2f6319d1c64ca512f1d690d217329a3b4944c751"
ALLOWED_REVIEW_MANIFEST_DIFF = "/source_lineage/6/sha256"
D98_MODEL_REL = "definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json"
A3_PROPOSAL_REL = "definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json"
A1_PROPOSAL_REL = "definitions/c11d/production/D_RENDERER_UNIFIED_PRESENTATION_REGION_POLICY_PROPOSAL_V1.json"



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


def _json_pointer_escape(value: str) -> str:
    return value.replace("~", "~0").replace("/", "~1")


def _json_diff_paths(left: Any, right: Any, path: str = "") -> list[str]:
    """Return exact JSON Pointer paths whose values differ."""
    if type(left) is not type(right):
        return [path or "/"]
    if isinstance(left, dict):
        paths: list[str] = []
        for key in sorted(set(left) | set(right)):
            child = path + "/" + _json_pointer_escape(str(key))
            if key not in left or key not in right:
                paths.append(child)
            else:
                paths.extend(_json_diff_paths(left[key], right[key], child))
        return paths
    if isinstance(left, list):
        if len(left) != len(right):
            return [path + "/length"]
        paths: list[str] = []
        for index, (a, b) in enumerate(zip(left, right)):
            paths.extend(_json_diff_paths(a, b, path + "/" + str(index)))
        return paths
    return [] if left == right else [path or "/"]


def validate_review_manifest_lineage(root: Path, contract: dict[str, Any]) -> dict[str, Any]:
    """Validate an immutable historical A.3 pin against the single reviewed D9.8 lineage refresh."""
    root = root.resolve()
    bridge_path = root / LINEAGE_RECONCILIATION_REL
    archive_path = root / REVIEW_MANIFEST_ARCHIVE_REL
    current_path = root / REVIEW_MANIFEST_REL
    decision_path = root / OPERATOR_DECISION_REL
    model_path = root / D98_MODEL_REL
    a3_path = root / A3_PROPOSAL_REL
    a1_path = root / A1_PROPOSAL_REL
    d98_doc_path = root / D98_RECONCILIATION_REL

    for path, label in ((bridge_path, "lineage reconciliation"), (archive_path, "historical review manifest"),
                        (current_path, "current review manifest"), (decision_path, "operator policy decision record"),
                        (model_path, "current D9.8 model"), (a3_path, "A.3 proposal"),
                        (a1_path, "A.1 proposal"), (d98_doc_path, "D9.8/D9.9 reconciliation")):
        if not path.is_file():
            raise FieldWindowProposalError(f"required A.3 lineage bridge source is missing: {label}: {path}")

    if sha256_file(bridge_path) != LINEAGE_RECONCILIATION_SHA256:
        raise FieldWindowProposalError("A.3 lineage reconciliation record SHA-256 mismatch")
    if sha256_file(archive_path) != HISTORICAL_REVIEW_MANIFEST_SHA256:
        raise FieldWindowProposalError("historical editorial review manifest archive SHA-256 mismatch")
    if sha256_file(current_path) != CURRENT_REVIEW_MANIFEST_SHA256:
        raise FieldWindowProposalError("current editorial review manifest SHA-256 mismatch")
    if sha256_file(decision_path) != OPERATOR_DECISION_SHA256:
        raise FieldWindowProposalError("operator policy decision record SHA-256 mismatch")
    if sha256_file(model_path) != CURRENT_D98_MODEL_SHA256:
        raise FieldWindowProposalError("current D9.8 editorial model SHA-256 mismatch")
    if sha256_file(a3_path) != A3_PROPOSAL_SHA256 or sha256_file(a1_path) != A1_PROPOSAL_SHA256:
        raise FieldWindowProposalError("A.1/A.3 approved proposal SHA-256 mismatch")
    if sha256_file(d98_doc_path) != D98_RECONCILIATION_SHA256:
        raise FieldWindowProposalError("D9.8/D9.9 semantic reconciliation V4 SHA-256 mismatch")

    bridge = load_json(bridge_path)
    if bridge.get("schema") != "C11E-E4C-A3-REVIEW-MANIFEST-LINEAGE-RECONCILIATION-V2" or bridge.get("status") != "ATTESTED_SINGLE_SOURCE_LINEAGE_POINTER_REFRESH_NO_POLICY_CHANGE":
        raise FieldWindowProposalError("unexpected A.3 lineage reconciliation identity or status")
    if bridge.get("frozen_c11c", {}).get("sha256") != EXPECTED_SOURCES["release/C11C_FREEZE_PACKAGE_MANIFEST.json"]:
        raise FieldWindowProposalError("lineage bridge frozen C11-C pin mismatch")

    proposal = load_json(a3_path)
    if proposal.get("status") != "PROPOSAL_ONLY_NOT_RENDERER_INPUT":
        raise FieldWindowProposalError("A.3 proposal was promoted or mutated")
    if proposal.get("authority", {}).get("editorial_review_manifest_sha256") != HISTORICAL_REVIEW_MANIFEST_SHA256:
        raise FieldWindowProposalError("A.3 historical review-manifest authority pin changed")
    if sha256_file(a3_path) != bridge.get("approved_policy", {}).get("a3", {}).get("sha256"):
        raise FieldWindowProposalError("A.3 bridge does not point to the exact approved proposal")

    decision = load_json(decision_path)
    if decision.get("schema") != "C11E-E4B-OPERATOR-POLICY-DECISION-RECORD-V1" or decision.get("decision_source") != "EXPLICIT_OPERATOR_MESSAGE_IN_CONVERSATION":
        raise FieldWindowProposalError("operator policy decision record identity/source mismatch")
    if decision.get("decision_semantics") != "APPROVE_AS_PROPOSED_FOR_D_OWNED_DESIGN_AND_CONTRACT_IMPLEMENTATION_ONLY":
        raise FieldWindowProposalError("operator policy decision scope semantics changed")
    decisions = {item.get("decision_id"): item for item in decision.get("decisions", [])}
    for decision_id, expected_sha in (("A.3_LOOP_DRILL_EDITORIAL_WINDOWS", A3_PROPOSAL_SHA256), ("A.1_SHARED_PRESENTATION_REGIONS", A1_PROPOSAL_SHA256)):
        item = decisions.get(decision_id)
        if not isinstance(item, dict) or item.get("decision") != "APPROVE_AS_PROPOSED" or item.get("proposal_sha256") != expected_sha:
            raise FieldWindowProposalError(f"explicit operator approval missing or stale: {decision_id}")
    scope = decision.get("scope_boundary", {})
    required_false = ("renderer_native_input_emission_authorized", "renderer_activation_authorized", "production_dispatch_authorized", "media_creation_authorized", "audio_asset_selection_authorized", "audio_generation_authorized", "audio_payload_materialization_authorized", "release_promotion_authorized")
    if any(scope.get(key) is not False for key in required_false):
        raise FieldWindowProposalError("operator decision record has broadened beyond D-owned design/contract scope")

    old_manifest = load_json(archive_path)
    current_manifest = load_json(current_path)
    diff_paths = _json_diff_paths(old_manifest, current_manifest)
    if diff_paths != [ALLOWED_REVIEW_MANIFEST_DIFF]:
        raise FieldWindowProposalError(f"editorial review manifest changed outside the single approved lineage pointer: {diff_paths}")
    old_rows = old_manifest.get("source_lineage", [])
    new_rows = current_manifest.get("source_lineage", [])
    if len(old_rows) <= 6 or len(new_rows) <= 6:
        raise FieldWindowProposalError("editorial review manifest source lineage is incomplete")
    old_row = old_rows[6]
    new_row = new_rows[6]
    if old_row != {"path": D98_MODEL_REL, "sha256": "50655c82521a353f1db6920f4d099cad92452ae369251f9fbde45cbaee4e8c53"}:
        raise FieldWindowProposalError("historical D9.8 source-lineage row differs from the pinned predecessor")
    if new_row != {"path": D98_MODEL_REL, "sha256": CURRENT_D98_MODEL_SHA256}:
        raise FieldWindowProposalError("current D9.8 source-lineage row differs from the pinned successor")
    if current_manifest.get("status") != "PREPARATION_ONLY_EDITORIAL_REVIEW_MANIFEST_NOT_RENDERER_INPUT":
        raise FieldWindowProposalError("current editorial review manifest is not preparation-only")
    approvals = current_manifest.get("approval_state", {})
    if not approvals or any(value is not False and value not in ("BLOCKED_AS_REQUIRED", "BLOCKED_NO_GO", "BLOCKED", "NONE") for value in approvals.values()):
        raise FieldWindowProposalError("current editorial review manifest approval state was broadened")
    if current_manifest.get("approval_state") != old_manifest.get("approval_state"):
        raise FieldWindowProposalError("editorial review manifest approval state changed during lineage refresh")
    if bridge.get("review_manifest_lineage", {}).get("allowed_json_pointer_difference") != [ALLOWED_REVIEW_MANIFEST_DIFF]:
        raise FieldWindowProposalError("lineage bridge allowed-difference declaration mismatch")
    if bridge.get("review_manifest_lineage", {}).get("old_pointer_value") != old_row.get("sha256") or bridge.get("review_manifest_lineage", {}).get("new_pointer_value") != new_row.get("sha256"):
        raise FieldWindowProposalError("lineage bridge pointer values mismatch")
    if bridge.get("d98_context", {}).get("plan_compatibility") != "D9_9_PLAN_ONLY_COMPATIBILITY_TRUE" or bridge.get("d98_context", {}).get("d4_executable_compatibility") is not False or bridge.get("d98_context", {}).get("renderer_admission") is not False:
        raise FieldWindowProposalError("D9.8 plan-only versus D4 executable boundary was weakened")
    preservation = bridge.get("preservation", {})
    for key in ("a3_proposal_mutated", "a1_proposal_mutated", "operator_decision_record_mutated", "review_manifest_approval_booleans_changed", "a3_mapping_semantics_changed", "renderer_native_input_emitted", "renderer_activation", "production_dispatch", "media_created", "audio_generation"):
        if preservation.get(key) is not False:
            raise FieldWindowProposalError(f"lineage bridge preservation boundary must remain false: {key}")
    if preservation.get("review_manifest_current_file_mutated_by_this_reconciliation") is not True or preservation.get("review_manifest_changed_only_by_pinned_single_pointer_replacement") is not True:
        raise FieldWindowProposalError("bridge must disclose the exact current-manifest replacement performed by this overlay")
    transition = bridge.get("review_manifest_lineage", {}).get("installed_transition", {})
    if transition.get("operation") != "PINNED_REPLACE" or transition.get("preimage_sha256") != HISTORICAL_REVIEW_MANIFEST_SHA256 or transition.get("postimage_sha256") != CURRENT_REVIEW_MANIFEST_SHA256 or transition.get("only_changed_json_pointer") != ALLOWED_REVIEW_MANIFEST_DIFF or transition.get("historical_bytes_preserved_as_add_only_archive") is not True:
        raise FieldWindowProposalError("review-manifest installed transition is not the exact approved preimage/postimage pair")
    if preservation.get("release_authority") != "NONE" or preservation.get("d4_8") != "BLOCKED":
        raise FieldWindowProposalError("lineage bridge governance lock mismatch")

    return {
        "historical_review_manifest_sha256": HISTORICAL_REVIEW_MANIFEST_SHA256,
        "current_review_manifest_sha256": CURRENT_REVIEW_MANIFEST_SHA256,
        "allowed_json_pointer_difference": diff_paths,
        "current_d98_model_sha256": CURRENT_D98_MODEL_SHA256,
        "approved_a3_proposal_sha256": A3_PROPOSAL_SHA256,
        "operator_decision_record_sha256": OPERATOR_DECISION_SHA256,
        "decision_scope": "D_OWNED_DESIGN_AND_CONTRACT_IMPLEMENTATION_ONLY",
        "renderer_native_input_emitted": False,
        "renderer_activation": False,
        "media_created": False,
    }


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
        if path == REVIEW_MANIFEST_REL.as_posix():
            continue  # The proposal keeps its historical reviewed pin; validate the exact bridge below.
        source = root / path
        if not source.is_file():
            raise FieldWindowProposalError(f"required lineage source is missing: {path}")
        if sha256_file(source) != digest:
            raise FieldWindowProposalError(f"source SHA-256 mismatch: {path}")

    lineage_reconciliation = validate_review_manifest_lineage(root, contract)

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
    return {"contract": contract, "schema": schema, "fixtures": fixtures, "lineage_reconciliation": lineage_reconciliation}


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
