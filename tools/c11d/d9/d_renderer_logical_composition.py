"""D-owned logical composition candidate; in-memory and non-dispatchable.

This module transforms the verified D renderer binding preview into a semantic
composition plan. Editorial strings become text_value properties on logical
text elements, proving intended data flow beyond provenance metadata. It does
not produce renderer-native input, touch disk at runtime, launch processes,
activate a renderer, or create media.
"""
from __future__ import annotations

import copy
import hashlib
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from d_renderer_candidate import (
    DRendererCandidateError,
    PREVIEW_SCHEMA,
    canonical_json,
    sha256_json,
    validate_renderer_binding_preview,
)

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_CANDIDATE_LOGICAL_COMPOSITION_V1.json")
OUTPUT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_CANDIDATE_LOGICAL_COMPOSITION_SCHEMA_V1.json")
BINDING_CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_CANDIDATE_BINDING_PREVIEW_V1.json")
CONTRACT_SCHEMA = "C11-D-RENDERER-CANDIDATE-LOGICAL-COMPOSITION-CONTRACT-V1"
PLAN_SCHEMA = "C11-D-D9-LOGICAL-COMPOSITION-PLAN-V1"
PLAN_STATUS = "PREPARATION_ONLY_LOGICAL_SCENE_NOT_RENDERER_INPUT"
SUPPORTED_TYPES = ("challenges", "visual_loops", "visual_drills")
COMMON_FIELDS = ("title", "subtitle", "call_to_action", "language")
CHALLENGE_FIELDS = ("player_name", "challenge_label")
EXPECTED_REQUIRED_FIELDS = {
    "challenges": ["title", "subtitle", "call_to_action", "language", "player_name", "challenge_label"],
    "visual_loops": ["title", "subtitle", "call_to_action", "language"],
    "visual_drills": ["title", "subtitle", "call_to_action", "language"],
}
EXPECTED_FIELD_TARGETS = {
    "title": {"source_preview_slot_id": "social_frame.header.title", "element_id": "editorial.title", "semantic_role": "HEADER_TITLE", "target_region": "HEADER", "z_order": 20, "mapping_state": "PROPOSED_NOT_APPROVED"},
    "subtitle": {"source_preview_slot_id": "social_frame.header.subtitle", "element_id": "editorial.subtitle", "semantic_role": "HEADER_SUBTITLE", "target_region": "HEADER", "z_order": 21, "mapping_state": "PROPOSED_NOT_APPROVED"},
    "call_to_action": {"source_preview_slot_id": "social_frame.footer.call_to_action", "element_id": "editorial.call_to_action", "semantic_role": "FOOTER_CALL_TO_ACTION", "target_region": "FOOTER", "z_order": 80, "mapping_state": "PROPOSED_NOT_APPROVED"},
    "player_name": {"source_preview_slot_id": "challenge_overlay.player_name", "element_id": "editorial.player_name", "semantic_role": "CHALLENGE_PLAYER_NAME", "target_region": "CHALLENGE_OVERLAY", "z_order": 40, "mapping_state": "PROPOSED_NOT_APPROVED"},
    "challenge_label": {"source_preview_slot_id": "challenge_overlay.challenge_label", "element_id": "editorial.challenge_label", "semantic_role": "CHALLENGE_LABEL", "target_region": "CHALLENGE_OVERLAY", "z_order": 41, "mapping_state": "PROPOSED_NOT_APPROVED"},
}


class DRendererLogicalCompositionError(ValueError):
    """Raised when source lineage or logical composition contracts fail."""


def _root(project_root: Path | str | None = None) -> Path:
    return Path(project_root).resolve() if project_root is not None else Path(__file__).resolve().parents[3]


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise DRendererLogicalCompositionError(f"Cannot read required logical composition contract input {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise DRendererLogicalCompositionError(f"Expected JSON object in {path}")
    return value


def _file_sha256(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except Exception as exc:
        raise DRendererLogicalCompositionError(f"Cannot hash required composition source {path}: {exc}") from exc


def _without_composition_hash(plan: Mapping[str, Any]) -> dict[str, Any]:
    return {str(key): copy.deepcopy(value) for key, value in plan.items() if key != "composition_sha256"}


def _load_contract(root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    contract_path = root / CONTRACT_REL
    contract = _read_json(contract_path)
    if contract.get("schema") != CONTRACT_SCHEMA or contract.get("schema_version") != "1.0":
        raise DRendererLogicalCompositionError("Unsupported logical composition contract identity/version")
    if contract.get("status") != "PREPARATION_ONLY_NOT_APPROVED_NOT_FROZEN":
        raise DRendererLogicalCompositionError("Logical composition contract cannot claim approval or freeze")
    output_contract = contract.get("output_contract")
    if not isinstance(output_contract, Mapping):
        raise DRendererLogicalCompositionError("Logical composition output contract is missing")
    expected_output_locks = {
        "schema": PLAN_SCHEMA,
        "json_schema": str(OUTPUT_SCHEMA_REL).replace("\\", "/"),
        "status": PLAN_STATUS,
        "persistence": "IN_MEMORY_ONLY",
        "renderer_input_emitted": False,
        "renderer_dispatch_invoked": False,
        "renderer_activation": False,
        "production_execution": False,
        "media_output_created": False,
        "output_artifact_path": None,
    }
    for key, expected in expected_output_locks.items():
        if output_contract.get(key) != expected:
            raise DRendererLogicalCompositionError(f"Logical composition output lock mismatch: {key}")
    if contract.get("supported_content_types") != list(SUPPORTED_TYPES):
        raise DRendererLogicalCompositionError("Logical composition supported content scope mismatch")
    if contract.get("required_editorial_fields") != EXPECTED_REQUIRED_FIELDS:
        raise DRendererLogicalCompositionError("Logical composition required editorial field contract mismatch")
    if contract.get("field_targets") != EXPECTED_FIELD_TARGETS:
        raise DRendererLogicalCompositionError("Logical composition semantic field targets changed without implementation review")
    required_locks = {
        "source_adapter_mode": "PREPARE_ONLY",
        "renderer_input_emitted": False,
        "renderer_dispatch_invoked": False,
        "renderer_activation": False,
        "production_execution": False,
        "media_output_created": False,
        "output_artifact_path": None,
        "d4_8": "BLOCKED",
        "release_authority": "NONE",
        "c11c_source_mutation": False,
    }
    locks = contract.get("required_locks", {})
    for key, expected in required_locks.items():
        if locks.get(key) != expected:
            raise DRendererLogicalCompositionError(f"Logical composition governance lock mismatch: {key}")
    approval = contract.get("approval_state", {})
    if approval.get("renderer_baseline_approved") is not False or approval.get("renderer_baseline_frozen") is not False:
        raise DRendererLogicalCompositionError("Candidate logical composition contract cannot self-approve/freeze")
    if approval.get("d4_8_authorized") is not False or approval.get("release_authority") != "NONE":
        raise DRendererLogicalCompositionError("Candidate logical composition cannot grant D4.8/release authority")

    schema_doc = _read_json(root / OUTPUT_SCHEMA_REL)
    if schema_doc.get("$id") != "urn:c11d:renderer-candidate-logical-composition:v1":
        raise DRendererLogicalCompositionError("Logical composition output schema identity mismatch")
    if schema_doc.get("properties", {}).get("schema", {}).get("const") != PLAN_SCHEMA:
        raise DRendererLogicalCompositionError("Logical composition output schema contract mismatch")
    if schema_doc.get("additionalProperties") is not False:
        raise DRendererLogicalCompositionError("Logical composition output schema must reject unknown top-level fields")

    binding_spec = _read_json(root / BINDING_CONTRACT_REL)
    if binding_spec.get("schema") != "C11-D-RENDERER-CANDIDATE-BINDING-PREVIEW-CONTRACT-V1":
        raise DRendererLogicalCompositionError("Source binding-preview contract identity mismatch")
    source_slots = binding_spec.get("proposed_editorial_slot_ids")
    targets = contract.get("field_targets")
    if not isinstance(source_slots, Mapping) or not isinstance(targets, Mapping):
        raise DRendererLogicalCompositionError("Logical composition field-target mappings are malformed")
    for field, target in targets.items():
        if not isinstance(target, Mapping) or source_slots.get(field) != target.get("source_preview_slot_id"):
            raise DRendererLogicalCompositionError(f"Logical composition target does not match binding-preview slot for {field}")
    return contract, schema_doc, binding_spec


def _assert_no_truth_fields(value: Any, location: str = "logical_composition") -> None:
    forbidden = {
        "simulationresult", "simulation_result", "simulationtruth", "simulation_truth",
        "winning_frame", "winningframe", "close_calls", "closecalls", "derived_telemetry",
        "derivedtelemetry", "gameplay_rng", "structural_rng",
    }
    if isinstance(value, Mapping):
        for key, child in value.items():
            normalized = str(key).replace("-", "_").lower()
            if normalized in forbidden:
                raise DRendererLogicalCompositionError(f"Forbidden simulation/telemetry field in {location}: {key}")
            _assert_no_truth_fields(child, f"{location}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _assert_no_truth_fields(child, f"{location}[{index}]")


def _build_core(
    preview: Mapping[str, Any], source_envelope: Mapping[str, Any], root: Path,
    contract: Mapping[str, Any], schema_doc: Mapping[str, Any], binding_spec: Mapping[str, Any],
) -> dict[str, Any]:
    try:
        validate_renderer_binding_preview(preview, source_envelope, root)
    except (DRendererCandidateError, ValueError, TypeError, KeyError) as exc:
        raise DRendererLogicalCompositionError(f"Binding preview/source envelope rejected: {exc}") from exc
    if preview.get("schema") != PREVIEW_SCHEMA or preview.get("status") != "PREPARATION_ONLY_NOT_RENDERER_INPUT":
        raise DRendererLogicalCompositionError("Source must be a verified non-renderable binding preview")

    identity = preview.get("content_identity")
    editorial_list = preview.get("editorial_binding_preview")
    if not isinstance(identity, Mapping) or not isinstance(editorial_list, list):
        raise DRendererLogicalCompositionError("Binding preview identity/editorial list malformed")
    content_type = identity.get("content_type")
    if content_type not in SUPPORTED_TYPES:
        raise DRendererLogicalCompositionError(f"Unsupported logical composition content type: {content_type!r}")
    expected_fields = contract.get("required_editorial_fields", {}).get(content_type)
    if not isinstance(expected_fields, list) or not expected_fields:
        raise DRendererLogicalCompositionError("No required editorial field set for content type")

    values: dict[str, dict[str, Any]] = {}
    for item in editorial_list:
        if not isinstance(item, Mapping):
            raise DRendererLogicalCompositionError("Editorial binding entry must be an object")
        field = item.get("source_field")
        if not isinstance(field, str) or field in values:
            raise DRendererLogicalCompositionError("Editorial source fields must be unique non-empty strings")
        values[field] = dict(item)
    if set(values) != set(expected_fields):
        raise DRendererLogicalCompositionError(
            f"Editorial fields do not match the exact required set for {content_type}: "
            f"expected={sorted(expected_fields)}, actual={sorted(values)}"
        )

    language_item = values.get("language")
    if not isinstance(language_item, Mapping) or not isinstance(language_item.get("value"), str) or not language_item["value"].strip():
        raise DRendererLogicalCompositionError("Canonical editorial language must be explicit and non-empty")
    language = language_item["value"]
    targets = contract.get("field_targets", {})
    ordered_elements: list[dict[str, Any]] = []
    for field in expected_fields:
        if field == "language":
            continue
        item = values[field]
        if not isinstance(item.get("value"), str) or not item["value"].strip():
            raise DRendererLogicalCompositionError(f"Visible editorial field must be a non-empty string: {field}")
        if item.get("value_sha256") != sha256_json(item["value"]):
            raise DRendererLogicalCompositionError(f"Editorial value hash mismatch: {field}")
        target = targets.get(field)
        if not isinstance(target, Mapping):
            raise DRendererLogicalCompositionError(f"No logical text target defined for editorial field: {field}")
        if item.get("proposed_slot_id") != target.get("source_preview_slot_id"):
            raise DRendererLogicalCompositionError(f"Binding-preview slot mismatch for editorial field: {field}")
        if item.get("mapping_state") != "PROPOSED_NOT_APPROVED":
            raise DRendererLogicalCompositionError(f"Editorial target cannot be promoted without review: {field}")
        ordered_elements.append({
            "element_id": target["element_id"],
            "semantic_role": target["semantic_role"],
            "target_region": target["target_region"],
            "z_order": target["z_order"],
            "source_field": field,
            "source_preview_slot_id": item["proposed_slot_id"],
            "target_mapping_state": "PROPOSED_NOT_APPROVED",
            "text_value": item["value"],
            "text_sha256": sha256_json(item["value"]),
            "language": language,
            "content_binding": "DIRECT_CANONICAL_EDITORIAL_VALUE",
        })
    ordered_elements.sort(key=lambda item: (item["z_order"], item["element_id"]))

    delivery = preview.get("delivery_profile")
    if not isinstance(delivery, Mapping) or not isinstance(delivery.get("profile"), Mapping):
        raise DRendererLogicalCompositionError("Resolved delivery profile is missing")
    delivery_profile = delivery["profile"]
    width, height, fps = delivery_profile.get("width"), delivery_profile.get("height"), delivery_profile.get("fps")
    if isinstance(width, bool) or not isinstance(width, int) or width <= 0:
        raise DRendererLogicalCompositionError("Delivery width must be a positive integer")
    if isinstance(height, bool) or not isinstance(height, int) or height <= 0:
        raise DRendererLogicalCompositionError("Delivery height must be a positive integer")
    if isinstance(fps, bool) or not isinstance(fps, (int, float)) or fps <= 0:
        raise DRendererLogicalCompositionError("Delivery fps must be a positive number")

    source_id = preview.get("source_identity")
    if not isinstance(source_id, Mapping):
        raise DRendererLogicalCompositionError("Binding preview source identity is missing")
    for name in ("request_hash", "editorial_hash", "plan_hash", "bridge_record_hash", "adapter_envelope_hash"):
        digest = source_id.get(name)
        if not isinstance(digest, str) or len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
            raise DRendererLogicalCompositionError(f"Invalid source lineage hash: {name}")

    seed_contract = preview.get("seed_contract")
    if not isinstance(seed_contract, Mapping):
        raise DRendererLogicalCompositionError("Canonical seed-domain rules are missing")
    if seed_contract.get("gameplay_seed_domain") != "GAMEPLAY" or seed_contract.get("music_seed_domain") != "MUSIC":
        raise DRendererLogicalCompositionError("Gameplay/music seed domains are not isolated")
    if seed_contract.get("cross_domain_seed_sharing") != "FORBIDDEN" or seed_contract.get("automatic_seed_generation") is not False or seed_contract.get("runtime_seed_derivation") is not False:
        raise DRendererLogicalCompositionError("Seed isolation policy mismatch")

    source_hashes = {name: source_id[name] for name in ("request_hash", "editorial_hash", "plan_hash", "bridge_record_hash", "adapter_envelope_hash")}
    plan = {
        "schema": PLAN_SCHEMA,
        "schema_version": "1.0",
        "status": PLAN_STATUS,
        "contract_identity": {
            "schema": CONTRACT_SCHEMA,
            "schema_version": "1.0",
            "sha256": _file_sha256(root / CONTRACT_REL),
            "output_schema_sha256": _file_sha256(root / OUTPUT_SCHEMA_REL),
            "binding_preview_contract_sha256": _file_sha256(root / BINDING_CONTRACT_REL),
        },
        "implementation_identity": {
            "module": "tools/c11d/d9/d_renderer_logical_composition.py",
            "version": "0.2.0-preparation",
            "sha256": _file_sha256(Path(__file__).resolve()),
        },
        "source_identity": {**source_hashes, "binding_preview_sha256": preview.get("preview_sha256")},
        "content_identity": copy.deepcopy(dict(identity)),
        "canvas_target": {
            "delivery_profile_requested_id": delivery.get("requested_profile_id"),
            "delivery_profile_resolved_id": delivery.get("resolved_profile_id"),
            "width": width,
            "height": height,
            "aspect_ratio": delivery_profile.get("aspect_ratio"),
            "fps": fps,
            "pixel_format": delivery_profile.get("pixel_format"),
            "canvas_semantics": "DELIVERY_TARGET_ONLY_NOT_CAPTURE_OR_RENDER_AUTHORIZATION",
        },
        "localization": {
            "locale": language,
            "applies_to_all_text_elements": True,
            "source_field": "language",
            "source_value_sha256": sha256_json(language),
        },
        "text_elements": ordered_elements,
        "seed_isolation": {
            "gameplay_seed_source": seed_contract["gameplay_seed_source"],
            "gameplay_seed_domain": seed_contract["gameplay_seed_domain"],
            "music_seed_source": seed_contract["music_seed_source"],
            "music_seed_domain": seed_contract["music_seed_domain"],
            "cross_domain_seed_sharing": "FORBIDDEN",
            "scene_elements_seed_derived": False,
            "audio_rendered": False,
        },
        "truth_and_telemetry": {"simulation_truth": "NOT_BOUND", "derived_telemetry": "NOT_BOUND"},
        "execution_boundary": {
            "composition_mode": "IN_MEMORY_SEMANTIC_REVIEW_ONLY",
            "renderer_input_emitted": False,
            "renderer_dispatch_invoked": False,
            "renderer_activation": False,
            "production_execution": False,
            "media_output_created": False,
            "output_artifact_path": None,
            "d4_8": "BLOCKED",
            "release_authority": "NONE",
            "c11c_source_mutation": False,
        },
    }
    _assert_no_truth_fields({"content_identity": plan["content_identity"], "text_elements": plan["text_elements"]})
    plan["composition_sha256"] = sha256_json(plan)
    return plan


def build_logical_composition_plan(
    preview: Mapping[str, Any], source_envelope: Mapping[str, Any], project_root: Path | str | None = None,
) -> dict[str, Any]:
    """Build an in-memory logical composition proof; no files/media/processes are created."""
    root = _root(project_root)
    contract, schema_doc, binding_spec = _load_contract(root)
    plan = _build_core(preview, source_envelope, root, contract, schema_doc, binding_spec)
    validate_logical_composition_plan(plan, preview, source_envelope, root)
    return plan


def validate_logical_composition_plan(
    plan: Mapping[str, Any], preview: Mapping[str, Any], source_envelope: Mapping[str, Any], project_root: Path | str | None = None,
) -> bool:
    """Reject altered plan payloads, unapproved target promotion and source drift."""
    root = _root(project_root)
    contract, schema_doc, binding_spec = _load_contract(root)
    if not isinstance(plan, Mapping) or plan.get("schema") != PLAN_SCHEMA:
        raise DRendererLogicalCompositionError("Unsupported logical composition plan schema")
    if plan.get("status") != PLAN_STATUS:
        raise DRendererLogicalCompositionError("Logical composition plan must remain preparation-only")
    required = set(schema_doc.get("required", []))
    if set(plan) != required:
        raise DRendererLogicalCompositionError("Logical composition plan has missing or unknown top-level fields")
    if plan.get("composition_sha256") != sha256_json(_without_composition_hash(plan)):
        raise DRendererLogicalCompositionError("Logical composition hash mismatch")
    expected_boundary = {
        "composition_mode": "IN_MEMORY_SEMANTIC_REVIEW_ONLY",
        "renderer_input_emitted": False,
        "renderer_dispatch_invoked": False,
        "renderer_activation": False,
        "production_execution": False,
        "media_output_created": False,
        "output_artifact_path": None,
        "d4_8": "BLOCKED",
        "release_authority": "NONE",
        "c11c_source_mutation": False,
    }
    if plan.get("execution_boundary") != expected_boundary:
        raise DRendererLogicalCompositionError("Logical composition execution/governance lock mismatch")
    if plan.get("truth_and_telemetry") != {"simulation_truth": "NOT_BOUND", "derived_telemetry": "NOT_BOUND"}:
        raise DRendererLogicalCompositionError("Simulation truth/telemetry must remain unbound")
    _assert_no_truth_fields({"content_identity": plan.get("content_identity"), "text_elements": plan.get("text_elements")})
    expected = _build_core(preview, source_envelope, root, contract, schema_doc, binding_spec)
    if dict(plan) != expected:
        raise DRendererLogicalCompositionError("Logical composition does not match canonical editorial source / current contracts")

    # Schema validation is an acceptance/test responsibility; the implementation itself
    # remains standard-library-only and performs exact structural checks above.
    return True
