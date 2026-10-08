"""C11-D D9.8 canonical resolver for editorial-only values.

This module reads the declared model and the existing Producer inventory. It does
not construct D4 requests, compute production/personalization identity, generate
seeds, invoke a renderer, or mutate simulation/render state. D4 remains the owner
of request normalization and plan identity; non-Challenge request parity is a D9.9
integration gate, not something this resolver pretends is already available.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Mapping

MODEL_REL = Path("definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json")
PRODUCER_SCHEMA_REL = Path("c11c-suite/c11c-producer/producer_schema.json")
CONTENT_TYPES = ("challenges", "visual_loops", "visual_drills", "longform")
PROFILE_LAYERS = ("global", "content_type", "family", "subtype", "variant")
MAX_TEXT_LENGTH = 160


class EditorialModelError(ValueError):
    """Raised for invalid selections, unsupported editorial fields, or unsafe edits."""


def _project_root(project_root: Path | str | None = None) -> Path:
    if project_root is None:
        return Path(__file__).resolve().parents[3]
    return Path(project_root).resolve()


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise EditorialModelError(f"Cannot load canonical JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise EditorialModelError(f"Canonical JSON must contain an object: {path}")
    return value


def load_model(project_root: Path | str | None = None) -> dict[str, Any]:
    """Load the model registry; callers receive a fresh mutable JSON value."""
    root = _project_root(project_root)
    model = _read_json(root / MODEL_REL)
    validate_model_definition(model)
    return model


def load_producer_schema(project_root: Path | str | None = None) -> dict[str, Any]:
    root = _project_root(project_root)
    return _read_json(root / PRODUCER_SCHEMA_REL)


def validate_model_definition(model: Mapping[str, Any]) -> None:
    if model.get("schema") != "C11-D-D9-UNIVERSAL-EDITORIAL-MODEL-V1":
        raise EditorialModelError("Unsupported universal editorial model schema")
    if model.get("checkpoint") != "D9.8" or model.get("status") != "CANONICAL_DECLARATIVE_MODEL":
        raise EditorialModelError("D9.8 model identity/status mismatch")
    authority = model.get("authority", {})
    for key, expected in (("runtime_authority", "NONE"), ("renderer_activation", False), ("production_execution", False), ("release_authority", "NONE")):
        if authority.get(key) != expected:
            raise EditorialModelError(f"Forbidden authority setting in model: {key}")
    seed = model.get("seed_contract", {})
    invariants = {
        "master_seed": "NOT_ADOPTED",
        "gameplay_seed": "request.seed",
        "music_seed": "request.music_seed",
        "cross_domain_seed_sharing": "FORBIDDEN",
        "runtime_seed_derivation": False,
        "automatic_seed_generation": False,
        "editorial_changes_may_mutate_gameplay_seed": False,
        "editorial_changes_may_mutate_music_seed": False,
        "editorial_changes_may_mutate_simulation_truth": False,
        "music_seed_changes_are_audio_domain_only": True,
    }
    for key, expected in invariants.items():
        if seed.get(key) != expected:
            raise EditorialModelError(f"Seed/simulation invariant changed: {key}")
    layers = model.get("inheritance_order")
    if layers != ["global", "content_type", "family", "subtype", "variant", "production_override"]:
        raise EditorialModelError("Editorial inheritance order is not canonical")
    fields = model.get("editorial_fields", {})
    if not isinstance(fields, dict):
        raise EditorialModelError("editorial_fields must be an object")
    content_types = model.get("content_types", {})
    if not isinstance(content_types, dict) or set(content_types) != set(CONTENT_TYPES):
        raise EditorialModelError("Model must explicitly declare Challenge, Loop, Drill and Longform")
    for name, declaration in fields.items():
        if not isinstance(declaration, dict):
            raise EditorialModelError(f"Invalid editorial field declaration: {name}")
        if declaration.get("enabled") and declaration.get("type") != "string":
            raise EditorialModelError(f"D9.8 only enables typed text fields in V1: {name}")
        applicable_types = declaration.get("content_types", [])
        if not isinstance(applicable_types, list) or any(item not in CONTENT_TYPES for item in applicable_types):
            raise EditorialModelError(f"Invalid content_types declaration on editorial field: {name}")
    for content_type, declaration in content_types.items():
        if not isinstance(declaration, dict):
            raise EditorialModelError(f"Invalid content type declaration: {content_type}")
        allowed = declaration.get("editable_fields", [])
        if not isinstance(allowed, list):
            raise EditorialModelError(f"editable_fields must be a list: {content_type}")
        for field_name in allowed:
            field = fields.get(field_name, {})
            if field.get("enabled") is not True or content_type not in field.get("content_types", []):
                raise EditorialModelError(f"Content type {content_type} references an unavailable editorial field: {field_name}")
    longform = content_types["longform"]
    if longform.get("enabled_for_selection") is not False or longform.get("editable_fields") != []:
        raise EditorialModelError("Longform must remain explicitly disabled until its D request contract exists")
    enabled_field_names = {name for name, spec in fields.items() if spec.get("enabled")}
    data_classes = model.get("data_classes", {})
    editable_names = set(data_classes.get("editable_editorial", {}).get("editable_keys", []))
    if not editable_names.issubset(enabled_field_names):
        raise EditorialModelError("Editable data class references disabled/unknown fields")
    for group_name in ("derived_telemetry", "provenance", "simulation_truth"):
        group = data_classes.get(group_name, {})
        if group.get("editable") is not False:
            raise EditorialModelError(f"Protected data class must remain non-editable: {group_name}")
        if editable_names.intersection(group.get("fields", [])):
            raise EditorialModelError(f"Protected field classified as editorial in {group_name}")


def _enabled_fields(model: Mapping[str, Any], content_type: str) -> list[str]:
    declaration = model["content_types"][content_type]
    allowed = declaration.get("editable_fields", [])
    return [name for name in allowed if model["editorial_fields"].get(name, {}).get("enabled") is True]


def build_catalog(project_root: Path | str | None = None) -> dict[str, Any]:
    """Resolve current choices from Producer's live schema without duplicating it."""
    root = _project_root(project_root)
    model = load_model(root)
    schema = load_producer_schema(root)
    catalog: dict[str, Any] = {"model_id": model["model_id"], "schema": model["schema"], "content_types": {}}

    declared_types = {row[0] for row in schema.get("video_types", []) if isinstance(row, list) and row}
    for required in ("challenges", "visual_loops", "visual_drills"):
        if required not in declared_types:
            raise EditorialModelError(f"Producer schema no longer declares required content type: {required}")

    challenge_rows = schema.get("challenges")
    if not isinstance(challenge_rows, list) or not challenge_rows:
        raise EditorialModelError("Producer challenge inventory is missing or malformed")
    challenge_families: dict[str, list[dict[str, Any]]] = {}
    seen_challenges: set[str] = set()
    for row in challenge_rows:
        if not isinstance(row, dict) or not row.get("id") or not row.get("mechanic"):
            raise EditorialModelError("Challenge inventory row must declare id and mechanic")
        challenge_id = str(row["id"])
        if challenge_id in seen_challenges:
            raise EditorialModelError(f"Duplicate Challenge identity: {challenge_id}")
        seen_challenges.add(challenge_id)
        mechanic = str(row["mechanic"])
        challenge_families.setdefault(mechanic, []).append({"id": challenge_id, "label": challenge_id, "mechanic": mechanic})
    catalog["content_types"]["challenges"] = {
        "state": model["content_types"]["challenges"]["model_state"],
        "request_plan_compatible": True,
        "editable_fields": _enabled_fields(model, "challenges"),
        "families": [
            {"id": mechanic, "label": mechanic.replace("_", " ").title(), "variants": sorted(variants, key=lambda x: x["id"])}
            for mechanic, variants in sorted(challenge_families.items())
        ],
        "variant_count": len(seen_challenges),
    }

    loop_source = schema.get("families")
    if not isinstance(loop_source, dict) or not loop_source:
        raise EditorialModelError("Visual Loop family inventory is missing or malformed")
    loop_families = []
    concrete_loop_grammars = 0
    for family_id, declaration in sorted(loop_source.items()):
        grammars = declaration.get("grammars") if isinstance(declaration, dict) else None
        if not isinstance(grammars, list) or not grammars:
            raise EditorialModelError(f"Visual Loop family has no grammar declarations: {family_id}")
        resolved = []
        seen_grammar_ids: set[str] = set()
        for grammar in grammars:
            if not isinstance(grammar, list) or len(grammar) < 2:
                raise EditorialModelError(f"Malformed grammar declaration in family {family_id}")
            grammar_id, label = str(grammar[0]), str(grammar[1])
            if grammar_id in seen_grammar_ids:
                raise EditorialModelError(f"Duplicate grammar identity in {family_id}: {grammar_id}")
            seen_grammar_ids.add(grammar_id)
            is_selector = grammar_id in model["content_types"]["visual_loops"]["inventory"]["selector_modes"]
            resolved.append({"id": grammar_id, "label": label, "selection_mode": is_selector, "concrete_variant": not is_selector})
            if not is_selector:
                concrete_loop_grammars += 1
        loop_families.append({"id": family_id, "label": str(declaration.get("name", family_id)), "internal_id": str(declaration.get("internal", family_id)), "subtypes": resolved})
    catalog["content_types"]["visual_loops"] = {
        "state": model["content_types"]["visual_loops"]["model_state"],
        "request_plan_compatible": False,
        "compatibility_reason": model["content_types"]["visual_loops"]["request_plan_compatibility"],
        "editable_fields": _enabled_fields(model, "visual_loops"),
        "families": loop_families,
        "family_count": len(loop_families),
        "concrete_grammar_count": concrete_loop_grammars,
    }

    drill_source = schema.get("drills")
    if not isinstance(drill_source, dict) or not drill_source:
        raise EditorialModelError("Visual Drill inventory is missing or malformed")
    drills = []
    drill_variant_count = 0
    for drill_id, declaration in sorted(drill_source.items()):
        if not isinstance(declaration, dict):
            raise EditorialModelError(f"Malformed Visual Drill declaration: {drill_id}")
        tiers = declaration.get("difficulty_values")
        if not isinstance(tiers, list) or not tiers:
            raise EditorialModelError(f"Visual Drill type has no explicit difficulty variants: {drill_id}")
        variants = []
        seen_tiers: set[int] = set()
        for tier_value in tiers:
            if isinstance(tier_value, bool) or not isinstance(tier_value, int) or tier_value <= 0:
                raise EditorialModelError(f"Invalid explicit Visual Drill tier in {drill_id}: {tier_value!r}")
            if tier_value in seen_tiers:
                raise EditorialModelError(f"Duplicate Visual Drill tier in {drill_id}: {tier_value}")
            seen_tiers.add(tier_value)
            variants.append({"id": f"tier-{tier_value}", "difficulty_tier": tier_value})
        drill_variant_count += len(variants)
        drills.append({"id": drill_id, "label": str(declaration.get("name", drill_id)), "variants": variants})
    catalog["content_types"]["visual_drills"] = {
        "state": model["content_types"]["visual_drills"]["model_state"],
        "request_plan_compatible": False,
        "compatibility_reason": model["content_types"]["visual_drills"]["request_plan_compatibility"],
        "editable_fields": _enabled_fields(model, "visual_drills"),
        "families": drills,
        "family_count": len(drills),
        "variant_count": drill_variant_count,
    }

    longform = model["content_types"]["longform"]
    catalog["content_types"]["longform"] = {
        "state": longform["model_state"],
        "request_plan_compatible": False,
        "enabled_for_selection": False,
        "editable_fields": [],
        "families": [],
        "reason": longform["reason"],
    }
    catalog["inventory_summary"] = {
        "challenge_variants": catalog["content_types"]["challenges"]["variant_count"],
        "visual_loop_families": catalog["content_types"]["visual_loops"]["family_count"],
        "visual_loop_concrete_grammars": catalog["content_types"]["visual_loops"]["concrete_grammar_count"],
        "visual_drill_types": catalog["content_types"]["visual_drills"]["family_count"],
        "visual_drill_variants": catalog["content_types"]["visual_drills"]["variant_count"],
        "longform_enabled": False,
    }
    return catalog


def _require_id(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise EditorialModelError(f"{name} is required as a non-empty canonical ID")
    return value.strip()


def resolve_selection(selection: Mapping[str, Any], project_root: Path | str | None = None) -> dict[str, Any]:
    """Validate one content selector against the live Producer schema."""
    if not isinstance(selection, Mapping):
        raise EditorialModelError("Selection must be an object")
    model = load_model(project_root)
    catalog = build_catalog(project_root)
    content_type = _require_id(selection.get("content_type"), "content_type")
    if content_type not in CONTENT_TYPES:
        raise EditorialModelError(f"Unknown content_type: {content_type}")
    content_spec = model["content_types"][content_type]
    if content_spec.get("enabled_for_selection") is False or content_type == "longform":
        raise EditorialModelError("Longform is visible in the model but is not selectable until the canonical D request contract supports it")

    family_value = selection.get("family_id")
    subtype_value = selection.get("subtype_id")
    variant_value = selection.get("variant_id")
    node: dict[str, Any] = {
        "content_type": content_type,
        "family_id": None,
        "subtype_id": None,
        "variant_id": None,
        "variant_scope_id": None,
        "scope_keys": {"content_type": content_type, "family": None, "subtype": None, "variant": None},
        "request_plan_compatible": bool(catalog["content_types"][content_type]["request_plan_compatible"]),
    }

    if content_type == "challenges":
        variant_id = _require_id(variant_value, "variant_id")
        all_variants = {v["id"]: (f["id"], v) for f in catalog["content_types"]["challenges"]["families"] for v in f["variants"]}
        if variant_id not in all_variants:
            raise EditorialModelError(f"Unknown Challenge variant_id: {variant_id}")
        mechanic_id, _variant = all_variants[variant_id]
        if family_value not in (None, "", mechanic_id):
            raise EditorialModelError(f"Challenge family_id conflicts with canonical mechanic: {mechanic_id}")
        if subtype_value not in (None, ""):
            raise EditorialModelError("Challenge subtype_id is not declared by the current Challenge inventory")
        node.update(family_id=mechanic_id, variant_id=variant_id, variant_scope_id=f"challenge:{variant_id}")
        node["scope_keys"]["family"] = f"challenge-family:{mechanic_id}"
        node["scope_keys"]["variant"] = f"challenge:{variant_id}"
    elif content_type == "visual_loops":
        family_id = _require_id(family_value, "family_id")
        families = {family["id"]: family for family in catalog["content_types"]["visual_loops"]["families"]}
        if family_id not in families:
            raise EditorialModelError(f"Unknown Visual Loop family_id: {family_id}")
        subtype_id = _require_id(subtype_value, "subtype_id")
        subtypes = {row["id"]: row for row in families[family_id]["subtypes"]}
        if subtype_id not in subtypes:
            raise EditorialModelError(f"Unknown Visual Loop grammar/subtype_id: {subtype_id} for {family_id}")
        if variant_value not in (None, ""):
            raise EditorialModelError("A separate native Visual Loop variant registry is not declared in V1; use the explicit production_override layer")
        node.update(family_id=family_id, subtype_id=subtype_id, variant_scope_id=f"visual-loop:{family_id}/{subtype_id}")
        node["scope_keys"]["family"] = f"visual-loop-family:{family_id}"
        node["scope_keys"]["subtype"] = f"visual-loop-grammar:{family_id}/{subtype_id}"
        node["scope_keys"]["variant"] = node["variant_scope_id"]
    else:  # visual_drills
        family_id = _require_id(family_value, "family_id")
        families = {family["id"]: family for family in catalog["content_types"]["visual_drills"]["families"]}
        if family_id not in families:
            raise EditorialModelError(f"Unknown Visual Drill type/family_id: {family_id}")
        if subtype_value not in (None, ""):
            raise EditorialModelError("Visual Drill subtype_id is not declared; use the tier variant selector")
        if isinstance(variant_value, bool):
            raise EditorialModelError("Visual Drill variant_id must be an explicit difficulty tier")
        match = re.fullmatch(r"(?:tier-)?([0-9]+)", str(variant_value)) if variant_value is not None else None
        if not match:
            raise EditorialModelError("Visual Drill variant_id must be an explicit tier-N value")
        tier = int(match.group(1))
        variant_ids = {v["difficulty_tier"] for v in families[family_id]["variants"]}
        if tier not in variant_ids:
            raise EditorialModelError(f"Unknown Visual Drill variant tier: {family_id} tier-{tier}")
        variant_id = f"tier-{tier}"
        node.update(family_id=family_id, variant_id=variant_id, variant_scope_id=f"visual-drill:{family_id}:{variant_id}")
        node["scope_keys"]["family"] = f"visual-drill-type:{family_id}"
        node["scope_keys"]["variant"] = node["variant_scope_id"]
        node["difficulty_tier"] = tier

    node["editable_fields"] = _enabled_fields(model, content_type)
    node["request_plan_compatibility"] = content_spec.get("request_plan_compatibility")
    return node


def _normalize_value(field_name: str, value: Any, model: Mapping[str, Any]) -> str:
    spec = model["editorial_fields"][field_name]
    if value is None:
        return "UNKNOWN"
    if not isinstance(value, str):
        raise EditorialModelError(f"Editorial value must be a string or null: {field_name}")
    normalized = value.strip()
    if len(normalized) > int(spec.get("max_length", MAX_TEXT_LENGTH)):
        raise EditorialModelError(f"Editorial value exceeds max length for {field_name}")
    if not normalized:
        return "UNKNOWN"
    if field_name == "language":
        normalized = normalized.lower()
    return normalized


def _validate_layer(layer_name: str, values: Any, allowed_fields: set[str], global_fields: set[str], model: Mapping[str, Any]) -> dict[str, str]:
    if values is None:
        return {}
    if not isinstance(values, Mapping):
        raise EditorialModelError(f"Editorial profile layer must be an object: {layer_name}")
    out: dict[str, str] = {}
    for field_name, value in values.items():
        if not isinstance(field_name, str) or field_name not in model["editorial_fields"]:
            raise EditorialModelError(f"Unknown editorial field: {field_name}")
        declaration = model["editorial_fields"][field_name]
        if declaration.get("enabled") is not True:
            raise EditorialModelError(f"Editorial field is reserved/not enabled: {field_name}")
        if field_name not in allowed_fields:
            raise EditorialModelError(f"Editorial field is not allowed for this content/layer: {field_name}")
        if layer_name == "global" and field_name not in global_fields:
            raise EditorialModelError(f"Field is not universal and cannot be set globally: {field_name}")
        out[field_name] = _normalize_value(field_name, value, model)
    return out


def resolve_editorial_values(
    selection: Mapping[str, Any],
    profile: Mapping[str, Any] | None = None,
    production_override: Mapping[str, Any] | None = None,
    project_root: Path | str | None = None,
) -> dict[str, Any]:
    """Merge the applicable editorial layers and return values, not a D4 request/plan."""
    model = load_model(project_root)
    node = resolve_selection(selection, project_root)
    allowed_fields = set(node["editable_fields"])
    global_fields = set(model["inheritance_policy"]["global_layer_fields"])
    if profile is None:
        profile = {}
    if not isinstance(profile, Mapping):
        raise EditorialModelError("Editorial profile must be an object")
    unknown_layers = set(profile) - set(PROFILE_LAYERS)
    if unknown_layers:
        raise EditorialModelError(f"Unknown editorial profile layer(s): {', '.join(sorted(map(str, unknown_layers)))}")

    # Validate every declared profile scope, not only the scope selected in this call.
    # This prevents dormant, malformed or protected edits from hiding in another variant.
    catalog = build_catalog(project_root)
    per_type_fields = {item: set(_enabled_fields(model, item)) for item in CONTENT_TYPES}
    family_allowlists: dict[str, set[str]] = {}
    subtype_allowlists: dict[str, set[str]] = {}
    variant_allowlists: dict[str, set[str]] = {}
    for family in catalog["content_types"]["challenges"]["families"]:
        family_allowlists[f"challenge-family:{family['id']}"] = per_type_fields["challenges"]
        for variant in family["variants"]:
            variant_allowlists[f"challenge:{variant['id']}"] = per_type_fields["challenges"]
    for family in catalog["content_types"]["visual_loops"]["families"]:
        family_allowlists[f"visual-loop-family:{family['id']}"] = per_type_fields["visual_loops"]
        for subtype in family["subtypes"]:
            scope = f"visual-loop-grammar:{family['id']}/{subtype['id']}"
            subtype_allowlists[scope] = per_type_fields["visual_loops"]
            variant_allowlists[f"visual-loop:{family['id']}/{subtype['id']}"] = per_type_fields["visual_loops"]
    for family in catalog["content_types"]["visual_drills"]["families"]:
        family_allowlists[f"visual-drill-type:{family['id']}"] = per_type_fields["visual_drills"]
        for variant in family["variants"]:
            variant_allowlists[f"visual-drill:{family['id']}:{variant['id']}"] = per_type_fields["visual_drills"]

    validated_profile: dict[str, Any] = {}
    global_values = profile.get("global", {})
    if not isinstance(global_values, Mapping):
        raise EditorialModelError("Editorial profile layer must be an object: global")
    _validate_layer("global", global_values, global_fields, global_fields, model)
    validated_profile["global"] = global_values
    scope_allowlists: dict[str, dict[str, set[str]]] = {
        "content_type": per_type_fields,
        "family": family_allowlists,
        "subtype": subtype_allowlists,
        "variant": variant_allowlists,
    }
    for layer_name, known_scopes in scope_allowlists.items():
        declared_scopes = profile.get(layer_name, {})
        if not isinstance(declared_scopes, Mapping):
            raise EditorialModelError(f"Editorial profile layer must be a scope-to-values object: {layer_name}")
        checked_scopes: dict[str, Any] = {}
        for scope_id, values in declared_scopes.items():
            if not isinstance(scope_id, str) or scope_id not in known_scopes:
                raise EditorialModelError(f"Unknown {layer_name} editorial scope: {scope_id}")
            _validate_layer(layer_name, values, known_scopes[scope_id], global_fields, model)
            checked_scopes[scope_id] = values
        validated_profile[layer_name] = checked_scopes

    effective = {field: "UNKNOWN" for field in node["editable_fields"]}
    selected_layers: list[tuple[str, Any]] = [("global", validated_profile["global"])]
    selected_layers.append(("content_type", validated_profile["content_type"].get(node["content_type"], {})))
    scope_keys = node["scope_keys"]
    if scope_keys.get("family"):
        selected_layers.append(("family", validated_profile["family"].get(scope_keys["family"], {})))
    if scope_keys.get("subtype"):
        selected_layers.append(("subtype", validated_profile["subtype"].get(scope_keys["subtype"], {})))
    if scope_keys.get("variant"):
        selected_layers.append(("variant", validated_profile["variant"].get(scope_keys["variant"], {})))

    for layer_name, layer_values in selected_layers:
        normalized = _validate_layer(layer_name, layer_values, allowed_fields, global_fields, model)
        effective.update(normalized)
    if production_override is None:
        production_override = {}
    normalized_override = _validate_layer("production_override", production_override, allowed_fields, global_fields, model)
    effective.update(normalized_override)

    return {
        "schema": "C11-D-D9-UNIVERSAL-EDITORIAL-RESOLUTION-V1",
        "model_id": model["model_id"],
        "selection": node,
        "values": effective,
        "applied_layers": [name for name, values in selected_layers if bool(values)] + (["production_override"] if normalized_override else []),
        "request_plan_compatible": node["request_plan_compatible"],
        "request_plan_state": "CURRENT_D4_CHALLENGE_PATH" if node["request_plan_compatible"] else "PENDING_D9_9_UNIVERSAL_REQUEST_ADAPTER",
        "runtime_authority": "NONE",
        "renderer_activation": False,
        "production_execution": False,
        "release_authority": "NONE",
    }
