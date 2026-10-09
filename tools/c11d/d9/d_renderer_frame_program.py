"""Renderer-neutral, in-memory frame-program declaration candidate.

This module converts a validated logical composition into a deterministic ordered
list of semantic text-binding declarations. Declarations are review data, not
executable commands or renderer-native input. It creates no files/media and
never dispatches to a renderer.
"""
from __future__ import annotations

import copy
import hashlib
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from d_renderer_logical_composition import (
    DRendererLogicalCompositionError,
    CONTRACT_REL as LOGICAL_CONTRACT_REL,
    OUTPUT_SCHEMA_REL as LOGICAL_SCHEMA_REL,
    PLAN_SCHEMA as LOGICAL_PLAN_SCHEMA,
    PLAN_STATUS as LOGICAL_PLAN_STATUS,
    validate_logical_composition_plan,
)
from d_renderer_candidate import sha256_json

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_NEUTRAL_FRAME_PROGRAM_V1.json")
OUTPUT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_NEUTRAL_FRAME_PROGRAM_SCHEMA_V1.json")
CONTRACT_SCHEMA = "C11-D-RENDERER-NEUTRAL-FRAME-PROGRAM-CONTRACT-V1"
PROGRAM_SCHEMA = "C11-D-D9-RENDERER-NEUTRAL-FRAME-PROGRAM-V1"
PROGRAM_STATUS = "PREPARATION_ONLY_RENDERER_NEUTRAL_FRAME_PROGRAM_NOT_RENDERER_INPUT"
SUPPORTED_TYPES = ("challenges", "visual_loops", "visual_drills")
EXPECTED_FIELD_REGIONS = {
    "title": "HEADER",
    "subtitle": "HEADER",
    "call_to_action": "FOOTER",
    "player_name": "CHALLENGE_OVERLAY",
    "challenge_label": "CHALLENGE_OVERLAY",
}
REGION_ORDER = ("HEADER", "CHALLENGE_OVERLAY", "FOOTER")
EXPECTED_REGIONS = {
    "HEADER": {
        "semantic_scope": "EDITORIAL_TITLE_AND_SUBTITLE",
        "mapping_state": "PROPOSED_NOT_APPROVED",
        "geometry_state": "UNRESOLVED_NO_COORDINATES",
    },
    "FOOTER": {
        "semantic_scope": "EDITORIAL_CALL_TO_ACTION",
        "mapping_state": "PROPOSED_NOT_APPROVED",
        "geometry_state": "UNRESOLVED_NO_COORDINATES",
    },
    "CHALLENGE_OVERLAY": {
        "semantic_scope": "CHALLENGE_SPECIFIC_EDITORIAL_LABELS",
        "mapping_state": "PROPOSED_NOT_APPROVED",
        "geometry_state": "UNRESOLVED_NO_COORDINATES",
    },
}


class DRendererFrameProgramError(ValueError):
    """Raised for invalid lineage, schema drift or a forbidden program promotion."""


def _root(project_root: Path | str | None = None) -> Path:
    return Path(project_root).resolve() if project_root is not None else Path(__file__).resolve().parents[3]


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise DRendererFrameProgramError(f"Cannot read required frame-program contract input {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise DRendererFrameProgramError(f"Expected JSON object in {path}")
    return value


def _file_sha256(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except Exception as exc:
        raise DRendererFrameProgramError(f"Cannot hash required frame-program contract input {path}: {exc}") from exc


def _without_program_hash(program: Mapping[str, Any]) -> dict[str, Any]:
    return {str(key): copy.deepcopy(value) for key, value in program.items() if key != "program_sha256"}


def _load_contract(root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    contract = _read_json(root / CONTRACT_REL)
    if contract.get("schema") != CONTRACT_SCHEMA or contract.get("schema_version") != "1.0":
        raise DRendererFrameProgramError("Unsupported renderer-neutral frame-program contract identity/version")
    if contract.get("status") != "PREPARATION_ONLY_NOT_APPROVED_NOT_FROZEN":
        raise DRendererFrameProgramError("Frame-program contract cannot claim approval or freeze")
    expected_output = {
        "schema": PROGRAM_SCHEMA,
        "json_schema": str(OUTPUT_SCHEMA_REL).replace("\\", "/"),
        "status": PROGRAM_STATUS,
        "persistence": "IN_MEMORY_ONLY",
        "program_executable": False,
        "renderer_native_input_emitted": False,
        "renderer_dispatch_invoked": False,
        "renderer_activation": False,
        "production_execution": False,
        "media_output_created": False,
        "output_artifact_path": None,
    }
    if contract.get("output_contract") != expected_output:
        raise DRendererFrameProgramError("Frame-program output/lock contract mismatch")
    if contract.get("supported_content_types") != list(SUPPORTED_TYPES):
        raise DRendererFrameProgramError("Frame-program supported content scope mismatch")
    if contract.get("field_region_targets") != EXPECTED_FIELD_REGIONS or contract.get("region_definitions") != EXPECTED_REGIONS:
        raise DRendererFrameProgramError("Frame-program semantic region mappings changed without review")
    rules = contract.get("program_rules")
    expected_rules = {
        "instruction_semantics": "DECLARATIONS_ONLY_NOT_EXECUTABLE_COMMANDS",
        "instruction_order": "ASCENDING_SOURCE_Z_ORDER_THEN_ELEMENT_ID",
        "editorial_flow": "Copy exact text_value/text_sha256/language from the validated logical composition.",
        "region_mapping": "Only semantic region IDs are bound; every mapping remains PROPOSED_NOT_APPROVED with no pixel coordinates.",
        "temporal_model": "No frame ranges, durations, transitions, animation curves or frame schedule are defined in this increment.",
        "canvas_descriptor": "Resolved delivery-profile metadata only; no capture/render authorization and no pixel geometry is emitted.",
        "seed_isolation": "Visual declarations are not seed-derived; gameplay and music seed domains remain separate.",
        "determinism": "Stable instruction order and canonical JSON SHA-256; no timestamp, random ID, environment path or mutable external state.",
    }
    if rules != expected_rules:
        raise DRendererFrameProgramError("Frame-program rule set changed without implementation review")
    expected_locks = {
        "source_adapter_mode": "PREPARE_ONLY",
        "program_executable": False,
        "renderer_native_input_emitted": False,
        "renderer_dispatch_invoked": False,
        "renderer_activation": False,
        "production_execution": False,
        "media_output_created": False,
        "output_artifact_path": None,
        "frame_schedule_defined": False,
        "pixel_coordinates_emitted": False,
        "d4_8": "BLOCKED",
        "release_authority": "NONE",
        "c11c_source_mutation": False,
    }
    if contract.get("required_locks") != expected_locks:
        raise DRendererFrameProgramError("Frame-program governance lock mismatch")
    approval = contract.get("approval_state")
    expected_approval = {
        "semantic_region_mapping_approved": False,
        "frame_program_approved": False,
        "renderer_baseline_approved": False,
        "renderer_baseline_frozen": False,
        "d4_8_authorized": False,
        "d9_14_full_acceptance": "BLOCKED_AS_REQUIRED",
        "d9_16_full_acceptance": "BLOCKED_AS_REQUIRED",
        "d9_17_closure": "BLOCKED_NO_GO",
        "release_authority": "NONE",
    }
    if approval != expected_approval:
        raise DRendererFrameProgramError("Frame-program contract cannot self-approve, freeze or grant authority")

    schema_doc = _read_json(root / OUTPUT_SCHEMA_REL)
    if schema_doc.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or schema_doc.get("$id") != "urn:c11d:renderer-neutral-frame-program:v1":
        raise DRendererFrameProgramError("Frame-program JSON Schema identity mismatch")
    if schema_doc.get("additionalProperties") is not False or schema_doc.get("properties", {}).get("schema", {}).get("const") != PROGRAM_SCHEMA:
        raise DRendererFrameProgramError("Frame-program schema must be exact and reject unknown fields")

    logical_contract = _read_json(root / LOGICAL_CONTRACT_REL)
    if logical_contract.get("schema") != "C11-D-RENDERER-CANDIDATE-LOGICAL-COMPOSITION-CONTRACT-V1" or logical_contract.get("schema_version") != "1.0":
        raise DRendererFrameProgramError("Source logical-composition contract identity mismatch")
    if logical_contract.get("status") != "PREPARATION_ONLY_NOT_APPROVED_NOT_FROZEN":
        raise DRendererFrameProgramError("Source logical-composition contract is not preparation-only")
    targets = logical_contract.get("field_targets")
    if not isinstance(targets, Mapping):
        raise DRendererFrameProgramError("Source logical-composition field-target map missing")
    for field, region_id in EXPECTED_FIELD_REGIONS.items():
        target = targets.get(field)
        if not isinstance(target, Mapping) or target.get("target_region") != region_id or target.get("mapping_state") != "PROPOSED_NOT_APPROVED":
            raise DRendererFrameProgramError(f"Frame-program region declaration disagrees with logical composition for {field}")
    return contract, schema_doc, logical_contract


def _assert_no_truth_fields(value: Any, location: str = "frame_program") -> None:
    forbidden = {
        "simulationresult", "simulation_result", "simulationtruth", "simulation_truth",
        "winning_frame", "winningframe", "close_calls", "closecalls", "derived_telemetry",
        "derivedtelemetry", "gameplay_rng", "structural_rng",
    }
    if isinstance(value, Mapping):
        for key, child in value.items():
            normalized = str(key).replace("-", "_").lower()
            if normalized in forbidden:
                raise DRendererFrameProgramError(f"Forbidden simulation/telemetry field in {location}: {key}")
            _assert_no_truth_fields(child, f"{location}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _assert_no_truth_fields(child, f"{location}[{index}]")


def _build_core(
    composition: Mapping[str, Any], preview: Mapping[str, Any], source_envelope: Mapping[str, Any],
    root: Path, contract: Mapping[str, Any], schema_doc: Mapping[str, Any], logical_contract: Mapping[str, Any],
) -> dict[str, Any]:
    try:
        validate_logical_composition_plan(composition, preview, source_envelope, root)
    except (DRendererLogicalCompositionError, ValueError, TypeError, KeyError) as exc:
        raise DRendererFrameProgramError(f"Source logical composition rejected: {exc}") from exc
    if composition.get("schema") != LOGICAL_PLAN_SCHEMA or composition.get("status") != LOGICAL_PLAN_STATUS:
        raise DRendererFrameProgramError("Source must be a validated preparation-only logical composition")

    content_identity = composition.get("content_identity")
    elements = composition.get("text_elements")
    if not isinstance(content_identity, Mapping) or content_identity.get("content_type") not in SUPPORTED_TYPES:
        raise DRendererFrameProgramError("Unsupported/missing frame-program content identity")
    if not isinstance(elements, list) or not elements:
        raise DRendererFrameProgramError("Logical composition must contain at least one text element")

    required_fields = logical_contract.get("required_editorial_fields", {}).get(content_identity["content_type"])
    if not isinstance(required_fields, list):
        raise DRendererFrameProgramError("No exact field set for selected content type")
    expected_visible_fields = [field for field in required_fields if field != "language"]
    actual_visible_fields = [item.get("source_field") for item in elements if isinstance(item, Mapping)]
    if len(actual_visible_fields) != len(elements) or actual_visible_fields != sorted(actual_visible_fields, key=lambda field: (next((t.get("z_order", 0) for t in elements if t.get("source_field") == field), 0), next((t.get("element_id", "") for t in elements if t.get("source_field") == field), ""))):
        raise DRendererFrameProgramError("Logical text elements are not in canonical z-order")
    if set(actual_visible_fields) != set(expected_visible_fields) or len(actual_visible_fields) != len(set(actual_visible_fields)):
        raise DRendererFrameProgramError("Logical composition field set is incomplete or duplicated")

    instructions: list[dict[str, Any]] = []
    used_regions: set[str] = set()
    for index, element in enumerate(elements):
        field = element.get("source_field")
        expected_region = EXPECTED_FIELD_REGIONS.get(field)
        if expected_region is None or element.get("target_region") != expected_region:
            raise DRendererFrameProgramError(f"Unapproved semantic region for source field {field!r}")
        if element.get("target_mapping_state") != "PROPOSED_NOT_APPROVED":
            raise DRendererFrameProgramError("Frame program cannot promote proposed field mappings")
        text = element.get("text_value")
        digest = element.get("text_sha256")
        locale = element.get("language")
        if not isinstance(text, str) or not text.strip() or digest != sha256_json(text):
            raise DRendererFrameProgramError(f"Invalid editorial value/hash for {field}")
        if not isinstance(locale, str) or locale != composition.get("localization", {}).get("locale"):
            raise DRendererFrameProgramError(f"Locale mismatch for {field}")
        if element.get("content_binding") != "DIRECT_CANONICAL_EDITORIAL_VALUE":
            raise DRendererFrameProgramError(f"Non-canonical editorial value flow for {field}")
        used_regions.add(expected_region)
        instructions.append({
            "instruction_index": index,
            "instruction_type": "DECLARE_SEMANTIC_TEXT_BINDING",
            "element_id": element["element_id"],
            "semantic_role": element["semantic_role"],
            "source_field": field,
            "region_id": expected_region,
            "z_order": element["z_order"],
            "text_value": text,
            "text_sha256": digest,
            "language": locale,
            "content_binding": "DIRECT_CANONICAL_EDITORIAL_VALUE",
            "target_mapping_state": "PROPOSED_NOT_APPROVED",
            "layout_binding_state": "UNRESOLVED_NO_COORDINATES",
            "temporal_binding_state": "NOT_SCHEDULED_NO_FRAME_RANGE",
        })

    region_declarations = []
    for region_id in REGION_ORDER:
        if region_id in used_regions:
            region_declarations.append({"region_id": region_id, **copy.deepcopy(EXPECTED_REGIONS[region_id])})

    canvas = composition.get("canvas_target")
    if not isinstance(canvas, Mapping):
        raise DRendererFrameProgramError("Resolved delivery descriptor missing")
    source_id = composition.get("source_identity")
    if not isinstance(source_id, Mapping):
        raise DRendererFrameProgramError("Source lineage missing")
    hash_fields = ("request_hash", "editorial_hash", "plan_hash", "bridge_record_hash", "adapter_envelope_hash", "binding_preview_sha256")
    for field in hash_fields:
        digest = source_id.get(field)
        if not isinstance(digest, str) or len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest):
            raise DRendererFrameProgramError(f"Invalid upstream hash: {field}")
    if not isinstance(composition.get("composition_sha256"), str) or len(composition["composition_sha256"]) != 64:
        raise DRendererFrameProgramError("Logical composition hash missing/invalid")
    seed_contract = composition.get("seed_isolation")
    if not isinstance(seed_contract, Mapping) or seed_contract.get("gameplay_seed_domain") != "GAMEPLAY" or seed_contract.get("music_seed_domain") != "MUSIC" or seed_contract.get("cross_domain_seed_sharing") != "FORBIDDEN":
        raise DRendererFrameProgramError("Gameplay/music seed isolation contract mismatch")

    program = {
        "schema": PROGRAM_SCHEMA,
        "schema_version": "1.0",
        "status": PROGRAM_STATUS,
        "contract_identity": {
            "schema": CONTRACT_SCHEMA,
            "schema_version": "1.0",
            "sha256": _file_sha256(root / CONTRACT_REL),
            "output_schema_sha256": _file_sha256(root / OUTPUT_SCHEMA_REL),
            "logical_composition_contract_sha256": _file_sha256(root / LOGICAL_CONTRACT_REL),
            "logical_composition_schema_sha256": _file_sha256(root / LOGICAL_SCHEMA_REL),
        },
        "implementation_identity": {
            "module": "tools/c11d/d9/d_renderer_frame_program.py",
            "version": "0.1.0-preparation",
            "sha256": _file_sha256(Path(__file__).resolve()),
        },
        "source_identity": {
            "request_hash": source_id["request_hash"],
            "editorial_hash": source_id["editorial_hash"],
            "plan_hash": source_id["plan_hash"],
            "bridge_record_hash": source_id["bridge_record_hash"],
            "adapter_envelope_hash": source_id["adapter_envelope_hash"],
            "binding_preview_sha256": source_id["binding_preview_sha256"],
            "logical_composition_sha256": composition["composition_sha256"],
        },
        "content_identity": copy.deepcopy(dict(content_identity)),
        "canvas_descriptor": {
            "delivery_profile_requested_id": canvas["delivery_profile_requested_id"],
            "delivery_profile_resolved_id": canvas["delivery_profile_resolved_id"],
            "width": canvas["width"],
            "height": canvas["height"],
            "aspect_ratio": canvas["aspect_ratio"],
            "fps": canvas["fps"],
            "pixel_format": canvas["pixel_format"],
            "descriptor_semantics": "DELIVERY_METADATA_ONLY_NOT_RENDER_AUTHORIZATION",
            "pixel_coordinates_emitted": False,
        },
        "localization": {
            "locale": composition["localization"]["locale"],
            "source_field": "language",
            "source_value_sha256": composition["localization"]["source_value_sha256"],
        },
        "region_declarations": region_declarations,
        "instructions": instructions,
        "temporal_model": {
            "schedule_state": "NOT_DEFINED",
            "frame_ranges_defined": False,
            "frame_ranges": None,
            "duration_frames": None,
            "timing_source": "NOT_PROVIDED_BY_LOGICAL_COMPOSITION",
        },
        "seed_isolation": {
            "gameplay_seed_source": seed_contract["gameplay_seed_source"],
            "gameplay_seed_domain": "GAMEPLAY",
            "music_seed_source": seed_contract["music_seed_source"],
            "music_seed_domain": "MUSIC",
            "cross_domain_seed_sharing": "FORBIDDEN",
            "visual_instructions_seed_derived": False,
            "audio_rendered": False,
        },
        "truth_and_telemetry": {"simulation_truth": "NOT_BOUND", "derived_telemetry": "NOT_BOUND"},
        "execution_boundary": {
            "program_mode": "IN_MEMORY_DECLARATIVE_REVIEW_ONLY",
            "program_executable": False,
            "renderer_native_input_emitted": False,
            "renderer_dispatch_invoked": False,
            "renderer_activation": False,
            "production_execution": False,
            "media_output_created": False,
            "output_artifact_path": None,
            "frame_schedule_defined": False,
            "pixel_coordinates_emitted": False,
            "d4_8": "BLOCKED",
            "release_authority": "NONE",
            "c11c_source_mutation": False,
        },
    }
    _assert_no_truth_fields({"content_identity": program["content_identity"], "instructions": program["instructions"]})
    program["program_sha256"] = sha256_json(program)
    return program


def build_renderer_neutral_frame_program(
    composition: Mapping[str, Any], preview: Mapping[str, Any], source_envelope: Mapping[str, Any],
    project_root: Path | str | None = None,
) -> dict[str, Any]:
    """Return deterministic in-memory declaration data; never execute or persist it."""
    root = _root(project_root)
    contract, schema_doc, logical_contract = _load_contract(root)
    program = _build_core(composition, preview, source_envelope, root, contract, schema_doc, logical_contract)
    validate_renderer_neutral_frame_program(program, composition, preview, source_envelope, root)
    return program


def validate_renderer_neutral_frame_program(
    program: Mapping[str, Any], composition: Mapping[str, Any], preview: Mapping[str, Any],
    source_envelope: Mapping[str, Any], project_root: Path | str | None = None,
) -> bool:
    """Validate exact lineage and all no-render/no-timing/no-geometry locks."""
    root = _root(project_root)
    contract, schema_doc, logical_contract = _load_contract(root)
    if not isinstance(program, Mapping) or program.get("schema") != PROGRAM_SCHEMA or program.get("status") != PROGRAM_STATUS:
        raise DRendererFrameProgramError("Unsupported or non-preparation frame program")
    if set(program) != set(schema_doc.get("required", [])) or set(program) != set(schema_doc.get("properties", {})):
        raise DRendererFrameProgramError("Frame program has missing or unknown top-level fields")
    if program.get("program_sha256") != sha256_json(_without_program_hash(program)):
        raise DRendererFrameProgramError("Frame-program SHA-256 mismatch")
    expected_boundary = {
        "program_mode": "IN_MEMORY_DECLARATIVE_REVIEW_ONLY",
        "program_executable": False,
        "renderer_native_input_emitted": False,
        "renderer_dispatch_invoked": False,
        "renderer_activation": False,
        "production_execution": False,
        "media_output_created": False,
        "output_artifact_path": None,
        "frame_schedule_defined": False,
        "pixel_coordinates_emitted": False,
        "d4_8": "BLOCKED",
        "release_authority": "NONE",
        "c11c_source_mutation": False,
    }
    if program.get("execution_boundary") != expected_boundary:
        raise DRendererFrameProgramError("Frame-program execution/governance lock mismatch")
    if program.get("temporal_model") != {
        "schedule_state": "NOT_DEFINED", "frame_ranges_defined": False,
        "frame_ranges": None, "duration_frames": None,
        "timing_source": "NOT_PROVIDED_BY_LOGICAL_COMPOSITION",
    }:
        raise DRendererFrameProgramError("Frame program cannot invent a temporal schedule")
    if program.get("truth_and_telemetry") != {"simulation_truth": "NOT_BOUND", "derived_telemetry": "NOT_BOUND"}:
        raise DRendererFrameProgramError("Simulation truth/telemetry must remain unbound")
    _assert_no_truth_fields({"content_identity": program.get("content_identity"), "instructions": program.get("instructions")})
    expected = _build_core(composition, preview, source_envelope, root, contract, schema_doc, logical_contract)
    if dict(program) != expected:
        raise DRendererFrameProgramError("Frame program does not match validated source composition/current contracts")
    return True
