"""D-owned composition seam joining GUI state and editorial draft to the shared backend.

This module is an in-memory view-model builder, not a second resolver or renderer.
All selection/catalog decisions, draft rules, editorial resolution and backend
preparation are delegated to their existing canonical D9 services. It does not
modify GUI widgets, persist data, emit renderer-native input, dispatch, or create media.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
DEFAULT_ROOT = HERE.parents[2]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from shared_production_context_gui_catalog import (
    SharedProductionGUICatalogError,
    audit_dynamic_gui_catalog,
    get_family_options,
    get_selector_options,
    resolve_gui_catalog_selection,
)
from shared_production_context_gui_editorial_draft import (
    SharedProductionGUIEditorialDraftError,
    audit_gui_editorial_draft_contract,
    preview_gui_editorial_draft,
)
from shared_production_context_gui_state import (
    SharedProductionGUIStateError,
    audit_gui_state_contract,
    build_canonical_request_from_gui_state,
    prepare_gui_state_context,
)
from shared_production_context_gui_adapter import audit_gui_adapter
from shared_production_context_service import (
    SharedProductionContextError,
    audit as audit_shared_facade,
    prepare_shared_production_context,
)
from d_renderer_shared_editorial_presentation_context_binding import validate_contract as validate_editorial_presentation_binding_contract

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_EDITORIAL_VIEW_MODEL_CONTRACT_V1.json")
CONTRACT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_EDITORIAL_VIEW_MODEL_CONTRACT_SCHEMA_V1.json")
VIEW_MODEL_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_SHARED_PRODUCTION_CONTEXT_GUI_EDITORIAL_VIEW_MODEL_SCHEMA_V1.json")
MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
CONTRACT_ID = "C11-D-SHARED-PRODUCTION-CONTEXT-GUI-EDITORIAL-VIEW-MODEL-CONTRACT-V1"
VIEW_MODEL_ID = "C11-D-SHARED-PRODUCTION-CONTEXT-GUI-EDITORIAL-VIEW-MODEL-V1"
SUPPORTED_TYPES = {"challenges", "visual_loops", "visual_drills"}
EDITORIAL_FIELDS = {"title", "subtitle", "call_to_action", "language", "player_name", "challenge_label"}


class SharedProductionGUIEditorialViewModelError(ValueError):
    """Invalid or inconsistent GUI/editorial draft composition."""


def _root(project_root: Path | str | None = None) -> Path:
    return Path(project_root).resolve() if project_root is not None else DEFAULT_ROOT


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise SharedProductionGUIEditorialViewModelError(f"Cannot read JSON contract/input {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SharedProductionGUIEditorialViewModelError(f"Expected JSON object: {path}")
    return value


def _file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _canonical(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _canonical(value[key]) for key in sorted(value, key=lambda item: str(item))}
    if isinstance(value, (list, tuple)):
        return [_canonical(item) for item in value]
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(_canonical(value), ensure_ascii=False, separators=(",", ":"), allow_nan=False)


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _validate_json_schema(instance: Any, schema: Mapping[str, Any], label: str) -> None:
    try:
        import jsonschema
        jsonschema.Draft202012Validator.check_schema(dict(schema))
        errors = sorted(
            jsonschema.Draft202012Validator(dict(schema)).iter_errors(instance),
            key=lambda error: (list(map(str, error.path)), error.message),
        )
    except Exception as exc:
        raise SharedProductionGUIEditorialViewModelError(f"Cannot validate {label}: {exc}") from exc
    if errors:
        raise SharedProductionGUIEditorialViewModelError(
            f"{label} schema violation at {list(errors[0].path)}: {errors[0].message}"
        )


def _verify_gui_editorial_view_model_sources(root: Path) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    """Validate the view-model contract, strict schemas, and all exact source pins.

    This source-only verification is used for each build. Parent services are then
    invoked through their canonical APIs, which perform their own contract checks.
    The explicit parent-audit join is reserved for --audit-only to avoid repeating
    the entire recursive audit tree before every ordinary view-model calculation.
    """
    contract = _read_json(root / CONTRACT_REL)
    contract_schema = _read_json(root / CONTRACT_SCHEMA_REL)
    view_schema = _read_json(root / VIEW_MODEL_SCHEMA_REL)
    _validate_json_schema(contract, contract_schema, "GUI editorial view-model contract")

    if contract.get("schema") != CONTRACT_ID or contract.get("schema_version") != "1.0":
        raise SharedProductionGUIEditorialViewModelError("GUI editorial view-model contract identity/version mismatch")
    if contract.get("status") != "PREPARE_ONLY_GUI_DRAFT_TO_CANONICAL_CONTEXT_COMPOSITION":
        raise SharedProductionGUIEditorialViewModelError("GUI editorial view-model cannot claim execution or renderer readiness")
    if contract.get("view_model_schema_sha256") != _file_sha(root / VIEW_MODEL_SCHEMA_REL):
        raise SharedProductionGUIEditorialViewModelError("GUI editorial view-model output schema hash drift")
    if contract.get("contract_schema_sha256") != _file_sha(root / CONTRACT_SCHEMA_REL):
        raise SharedProductionGUIEditorialViewModelError("GUI editorial view-model contract schema hash drift")
    if view_schema.get("$id") != "C11-D-SHARED-PRODUCTION-CONTEXT-GUI-EDITORIAL-VIEW-MODEL-SCHEMA-V1":
        raise SharedProductionGUIEditorialViewModelError("GUI editorial view-model schema identity mismatch")
    if view_schema.get("properties", {}).get("schema", {}).get("const") != VIEW_MODEL_ID:
        raise SharedProductionGUIEditorialViewModelError("GUI editorial view-model output schema ID mismatch")
    if view_schema.get("additionalProperties") is not False:
        raise SharedProductionGUIEditorialViewModelError("GUI editorial view-model schema must reject unknown top-level fields")

    lineage = contract.get("source_lineage")
    if not isinstance(lineage, list) or len(lineage) < 25:
        raise SharedProductionGUIEditorialViewModelError("GUI editorial view-model needs the full, explicit parent source lineage")
    if lineage[0].get("path") != "release/C11C_FREEZE_PACKAGE_MANIFEST.json" or lineage[0].get("sha256") != MANIFEST_SHA256:
        raise SharedProductionGUIEditorialViewModelError("Frozen C11-C manifest must lead GUI editorial view-model lineage")

    seen: set[str] = set()
    for row in lineage:
        if not isinstance(row, Mapping) or set(row) != {"path", "role", "sha256"}:
            raise SharedProductionGUIEditorialViewModelError("Malformed GUI editorial view-model lineage row")
        rel = row["path"]
        digest = row["sha256"]
        if not isinstance(rel, str) or not rel or "\\" in rel or Path(rel).is_absolute() or ".." in Path(rel).parts or rel in seen:
            raise SharedProductionGUIEditorialViewModelError(f"Unsafe or duplicate source pin: {rel!r}")
        if not isinstance(digest, str) or not re.fullmatch(r"[a-f0-9]{64}", digest):
            raise SharedProductionGUIEditorialViewModelError(f"Malformed source hash: {rel}")
        path = root / rel
        if not path.is_file():
            raise SharedProductionGUIEditorialViewModelError(f"Pinned view-model source is missing: {rel}")
        if _file_sha(path) != digest:
            raise SharedProductionGUIEditorialViewModelError(f"Pinned view-model source drift: {rel}")
        seen.add(rel)
    return contract, view_schema, lineage


def audit_gui_editorial_view_model_contract(project_root: Path | str | None = None) -> dict[str, Any]:
    """Verify this contract and exact pins, then audit each canonical parent API."""
    root = _root(project_root)
    _, _, lineage = _verify_gui_editorial_view_model_sources(root)

    # Use the existing authorities. No local catalog, profile or editorial resolver is created.
    try:
        reactive = __import__("shared_production_context_gui_reactive_selection").audit_reactive_selection_contract(root)
        catalog = audit_dynamic_gui_catalog(root)
        state = audit_gui_state_contract(root)
        draft = audit_gui_editorial_draft_contract(root)
        adapter = audit_gui_adapter(root)
        facade = audit_shared_facade(root)
        binding = validate_editorial_presentation_binding_contract(root)
    except Exception as exc:
        raise SharedProductionGUIEditorialViewModelError(f"A canonical parent contract failed: {exc}") from exc

    return {
        "source_pins": len(lineage),
        "reactive_selection_source_pins": reactive.get("source_pins"),
        "catalog_source_pins": catalog.get("source_pins"),
        "gui_state_source_pins": state.get("source_pins"),
        "editorial_draft_source_pins": draft.get("source_pins"),
        "gui_adapter_source_pins": adapter.get("source_pins"),
        "facade_source_pins": facade.get("source_pins"),
        "editorial_presentation_contract_valid": bool(binding),
        "supported_content_types": 3,
        "renderer": "OFF",
        "media_created": False,
        "d4_8": "BLOCKED",
        "release_authority": "NONE",
    }

def _selection_from_draft(draft_state: Mapping[str, Any]) -> dict[str, Any]:
    binding = draft_state.get("selection_binding")
    if not isinstance(binding, Mapping):
        raise SharedProductionGUIEditorialViewModelError("Editorial draft state has no canonical selection binding")
    if binding.get("selection_path_complete") is not True or binding.get("canonical_selection_resolved") is not True:
        raise SharedProductionGUIEditorialViewModelError("Editorial draft selection is incomplete; shared context cannot be prepared")
    content_type = binding.get("content_type")
    family_id = binding.get("family_id")
    selector_field = binding.get("selector_field")
    selector_id = binding.get("selector_id")
    if content_type not in SUPPORTED_TYPES or not isinstance(family_id, str) or not family_id:
        raise SharedProductionGUIEditorialViewModelError("Editorial draft selection has invalid content/family identity")
    if selector_field not in {"subtype_id", "variant_id"} or not isinstance(selector_id, str) or not selector_id:
        raise SharedProductionGUIEditorialViewModelError("Editorial draft selection has invalid selector identity")
    return {"content_type": content_type, "family_id": family_id, selector_field: selector_id}


def _assert_selection_parity(gui_state: Mapping[str, Any], draft_state: Mapping[str, Any]) -> dict[str, Any]:
    expected = _selection_from_draft(draft_state)
    supplied = gui_state.get("selection")
    if not isinstance(supplied, Mapping) or dict(supplied) != expected:
        raise SharedProductionGUIEditorialViewModelError(
            "GUI state selection differs from the editorial draft's bound selection; stale drafts are rejected"
        )
    if gui_state.get("mode") != draft_state.get("selection_binding", {}).get("mode"):
        raise SharedProductionGUIEditorialViewModelError("GUI state mode differs from editorial draft selection mode")
    return expected


def _without_hash(value: Mapping[str, Any], hash_key: str) -> dict[str, Any]:
    return {str(key): copy.deepcopy(child) for key, child in value.items() if key != hash_key}


def build_gui_editorial_view_model(
    gui_state: Mapping[str, Any],
    editorial_draft_state: Mapping[str, Any],
    project_root: Path | str | None = None,
) -> dict[str, Any]:
    """Join selected GUI controls and editorial draft into a canonical, in-memory context view."""
    root = _root(project_root)
    if not isinstance(gui_state, Mapping) or not isinstance(editorial_draft_state, Mapping):
        raise SharedProductionGUIEditorialViewModelError("GUI state and editorial draft state must be mappings")

    original_gui_sha = canonical_sha256(gui_state)
    original_draft_sha = canonical_sha256(editorial_draft_state)
    _verify_gui_editorial_view_model_sources(root)
    selection = _assert_selection_parity(gui_state, editorial_draft_state)

    try:
        draft_preview = preview_gui_editorial_draft(editorial_draft_state, root)
        mode = gui_state.get("mode")
        family_options = get_family_options(selection["content_type"], mode=mode, project_root=root)
        selector_options = get_selector_options(
            selection["content_type"], selection["family_id"], mode=mode, project_root=root
        )
        catalog_selection = resolve_gui_catalog_selection(
            selection["content_type"],
            selection["family_id"],
            selection.get("subtype_id", selection.get("variant_id")),
            mode=mode,
            project_root=root,
        )
    except Exception as exc:
        raise SharedProductionGUIEditorialViewModelError(f"Canonical selection/catalog/editorial preview rejected the view model: {exc}") from exc

    if draft_preview.get("status") != "READY_FOR_EDITORIAL_REVIEW_ONLY" or not isinstance(draft_preview.get("effective_values"), Mapping):
        raise SharedProductionGUIEditorialViewModelError("Editorial draft has no resolved effective values for this selection")
    canonical_catalog_selection = {
        key: value for key, value in catalog_selection.get("selection", {}).items() if value is not None
    }
    if canonical_catalog_selection != selection:
        raise SharedProductionGUIEditorialViewModelError("Canonical catalog resolver disagrees with the GUI/draft selection")

    # The draft is the sole source of editable editorial state at this boundary.
    # This is an explicit composition, not a second resolver; D9.8 still resolves values.
    composed_gui_state = copy.deepcopy(dict(gui_state))
    composed_gui_state["editorial"] = {
        "profile": copy.deepcopy(editorial_draft_state.get("profile", {})),
        "overrides": copy.deepcopy(editorial_draft_state.get("overrides", {})),
    }

    try:
        raw_request = build_canonical_request_from_gui_state(composed_gui_state, root)
        context = prepare_gui_state_context(composed_gui_state, root)
        cli_context_equivalent = prepare_shared_production_context(raw_request, root)
    except Exception as exc:
        raise SharedProductionGUIEditorialViewModelError(f"Canonical GUI/CLI backend preparation rejected the view model: {exc}") from exc

    if context != cli_context_equivalent:
        raise SharedProductionGUIEditorialViewModelError("GUI adapter and direct shared CLI facade do not return exact equal records")
    resolved = context.get("shared_context_binding", {}).get("editorial_binding", {}).get("resolved_values")
    if not isinstance(resolved, Mapping) or dict(resolved) != dict(draft_preview["effective_values"]):
        raise SharedProductionGUIEditorialViewModelError("D9.8 draft preview and canonical D9.9/D9.10 editorial values differ")
    if raw_request.get("production_override") != dict(editorial_draft_state.get("overrides", {})):
        raise SharedProductionGUIEditorialViewModelError("Editorial draft overrides were not preserved in the canonical request")
    if raw_request.get("editorial_profile") != dict(editorial_draft_state.get("profile", {})):
        raise SharedProductionGUIEditorialViewModelError("Editorial draft profile was not preserved in the canonical request")

    allowed_modes = catalog_selection.get("mode") == mode and mode in next(
        row["allowed_modes"] for row in family_options if row["id"] == selection["family_id"]
    )
    identity = {
        "request_id": raw_request["request_id"],
        "content_type": selection["content_type"],
        "selection": copy.deepcopy(selection),
        "catalog_sha256": editorial_draft_state["selection_binding"]["catalog_sha256"],
        "selection_snapshot_sha256": editorial_draft_state["selection_binding"]["selection_snapshot_sha256"],
        "request_sha256": context["identity"]["request_sha256"],
        "editorial_sha256": context["identity"]["editorial_sha256"],
        "plan_sha256": context["identity"]["plan_sha256"],
        "bridge_record_sha256": context["identity"]["bridge_record_sha256"],
        "adapter_envelope_sha256": context["identity"]["adapter_envelope_sha256"],
        "shared_context_binding_sha256": context["identity"]["shared_context_binding_sha256"],
    }
    view_model: dict[str, Any] = {
        "schema": VIEW_MODEL_ID,
        "schema_version": "1.0",
        "status": "PREPARED_SHARED_GUI_CONTEXT_NOT_RENDERER_INPUT",
        "mode": mode,
        "selection": {
            **copy.deepcopy(selection),
            "selector_field": "subtype_id" if "subtype_id" in selection else "variant_id",
            "selector_id": selection.get("subtype_id", selection.get("variant_id")),
            "request_plan_compatible": bool(catalog_selection.get("request_plan_compatible")),
            "exact_concrete_grammar": catalog_selection.get("exact_concrete_grammar"),
        },
        "controls": {
            "family_options": copy.deepcopy(family_options),
            "selector_options": copy.deepcopy(selector_options),
            "production": copy.deepcopy(dict(gui_state.get("production", {}))),
            "personalization_enabled": bool(gui_state.get("production", {}).get("personalization_enabled")),
        },
        "editorial": {
            "profile": copy.deepcopy(editorial_draft_state.get("profile", {})),
            "overrides": copy.deepcopy(editorial_draft_state.get("overrides", {})),
            "active_fields": copy.deepcopy(draft_preview["active_fields"]),
            "effective_values": copy.deepcopy(dict(resolved)),
            "applied_layers": copy.deepcopy(draft_preview.get("applied_layers", [])),
            "draft_state_sha256": editorial_draft_state.get("state_sha256"),
            "draft_preview_sha256": draft_preview.get("preview_sha256"),
            "resolved_by": "CANONICAL_D9_8_EDITORIAL_MODEL_VIA_D9_9_PLAN",
        },
        "identity": identity,
        "canonical_request_preview": copy.deepcopy(raw_request),
        "shared_context_record": copy.deepcopy(context),
        "readiness": {
            "selection_complete": True,
            "canonical_context_prepared": True,
            "catalog_mode_allowed": bool(allowed_modes),
            "request_plan_compatible": bool(catalog_selection.get("request_plan_compatible")),
            "renderer_input_admissible": False,
            "render_ready": False,
        },
        "execution_boundary": {
            "gui_widgets_modified": False,
            "state_persisted": False,
            "canonical_context_persisted": False,
            "renderer_native_input_emitted": False,
            "renderer_dispatch_invoked": False,
            "renderer_activation": False,
            "production_execution": False,
            "media_created": False,
            "c11c_source_mutation": False,
            "d4_8": "BLOCKED",
            "release_authority": "NONE",
            "d9_17": "BLOCKED_NO_GO",
            "d10": "BLOCKED",
        },
    }
    view_model["view_model_sha256"] = canonical_sha256(view_model)

    _validate_json_schema(view_model, _read_json(root / VIEW_MODEL_SCHEMA_REL), "GUI editorial view model")
    if canonical_sha256(gui_state) != original_gui_sha or canonical_sha256(editorial_draft_state) != original_draft_sha:
        raise SharedProductionGUIEditorialViewModelError("GUI state or editorial draft input was mutated")
    if view_model["shared_context_record"]["execution_boundary"]["renderer_native_input_emitted"] is not False:
        raise SharedProductionGUIEditorialViewModelError("Prepared context violates renderer-input boundary")
    if view_model["execution_boundary"]["media_created"] is not False or view_model["execution_boundary"]["release_authority"] != "NONE":
        raise SharedProductionGUIEditorialViewModelError("GUI editorial view-model governance boundary escalated")
    return view_model


def validate_gui_editorial_view_model(
    view_model: Mapping[str, Any],
    gui_state: Mapping[str, Any],
    editorial_draft_state: Mapping[str, Any],
    project_root: Path | str | None = None,
) -> bool:
    if not isinstance(view_model, Mapping):
        raise SharedProductionGUIEditorialViewModelError("View model must be a mapping")
    expected = build_gui_editorial_view_model(gui_state, editorial_draft_state, project_root)
    if dict(view_model) != expected:
        raise SharedProductionGUIEditorialViewModelError("View model differs from canonical recomputation")
    return True


def audit(project_root: Path | str | None = None) -> dict[str, Any]:
    report = audit_gui_editorial_view_model_contract(project_root)
    return {
        "source_pins": report["source_pins"],
        "content_types": report["supported_content_types"],
        "composition_order": ["CATALOG_SELECTION", "EDITORIAL_DRAFT", "GUI_STATE_MAPPING", "D9_8_RESOLUTION", "SHARED_D9_9_D9_10_CONTEXT"],
        "backend_parity": "GUI_ADAPTER_EQUALS_DIRECT_SHARED_FACADE",
        "render_ready": False,
        "renderer": report["renderer"],
        "media_created": report["media_created"],
        "d4_8": report["d4_8"],
        "release_authority": report["release_authority"],
    }


def _write_stdout(payload: str) -> None:
    encoded = payload.encode("ascii", errors="backslashreplace")
    stream = getattr(sys.stdout, "buffer", None)
    if stream is not None:
        stream.write(encoded)
        stream.flush()
    else:
        sys.stdout.write(encoded.decode("ascii"))
        sys.stdout.flush()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="C11-D GUI editorial view-model composition; no widgets or render dispatch")
    parser.add_argument("--project-root", type=Path, default=None)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--audit-only", action="store_true")
    group.add_argument("--inputs", action="store_true", help="Read GUI state and editorial draft JSON files")
    parser.add_argument("--gui-state", type=Path)
    parser.add_argument("--editorial-draft", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.audit_only:
            result = audit(args.project_root)
            _write_stdout(json.dumps({"audit": result, "result": "PASS"}, ensure_ascii=True, sort_keys=True) + "\n")
            return 0
        if args.gui_state is None or args.editorial_draft is None:
            raise SharedProductionGUIEditorialViewModelError("--inputs requires both --gui-state and --editorial-draft")
        gui_state = _read_json(args.gui_state)
        draft_state = _read_json(args.editorial_draft)
        result = build_gui_editorial_view_model(gui_state, draft_state, args.project_root)
        _write_stdout(json.dumps(result, ensure_ascii=True, sort_keys=True, indent=2) + "\n")
        return 0
    except Exception as exc:
        message = (
            f"C11-D GUI EDITORIAL VIEW MODEL FAIL | {exc} | renderer=OFF | media_created=false | "
            "D4.8=BLOCKED | release_authority=NONE\n"
        )
        _write_stdout(message)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
