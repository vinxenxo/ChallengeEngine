"""Canonical D9.9 universal Producer request and plan adapter.

The existing Producer GUI and the CLI both call this module. Challenge selections
reuse the closed D4 normalizer/personalization/orchestrator path as a subordinate
plan. Loop/Drill selections receive a deterministic universal editorial-intent plan;
that plan is explicitly non-executable until the future D renderer baseline.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import re
import sys
from collections import OrderedDict
from pathlib import Path
from typing import Any, Mapping

_THIS_DIR = Path(__file__).resolve().parent
if str(_THIS_DIR) not in sys.path:
    sys.path.insert(0, str(_THIS_DIR))

from universal_editorial_model import (
    EditorialModelError,
    build_catalog,
    load_model,
    resolve_editorial_values,
)

REQUEST_SCHEMA_REL = Path("definitions/c11d/production/C11D_UNIVERSAL_PRODUCER_REQUEST_D9_9_V1.json")
DELIVERY_REL = Path("profiles/delivery/c11c_video_delivery_profiles.json")
CHALLENGES_REL = Path("challenges")
REQUEST_SCHEMA_ID = "C11-D-D9.9-UNIVERSAL-PRODUCER-REQUEST-V1"
PLAN_SCHEMA_ID = "C11-D-D9.9-UNIVERSAL-PRODUCER-PLAN-V1"
VERSION = "0.11.0"
SEED_MIN = 1
SEED_MAX = 2147483646
ALLOWED_MODES = {"REVIEW", "PRODUCTION"}
FORBIDDEN_EDITORIAL_FIELDS = {
    "seed", "music_seed", "master_seed", "fps", "duration_seconds", "frame_count",
    "palette_name", "system_id", "winning_frame", "close_calls", "simulation_result",
    "simulation_truth", "mechanic", "mechanics", "target", "speed", "collision", "timing",
    "gameplay_rng", "structural_rng", "provenance", "request_id", "plan_hash",
    "artifact_sha256", "media_sha256", "difficulty_tier",
}


class UniversalProducerError(ValueError):
    """Raised when a universal D9.9 request violates the canonical contract."""


def project_root(path: Path | str | None = None) -> Path:
    if path is None:
        return Path(__file__).resolve().parents[3]
    return Path(path).resolve()


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise UniversalProducerError(f"Cannot load canonical JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise UniversalProducerError(f"Canonical JSON must be an object: {path}")
    return value


def _load_module(name: str, path: Path):
    key = f"_c11d_d99_{name}"
    if key in sys.modules:
        return sys.modules[key]
    spec = importlib.util.spec_from_file_location(key, path)
    if spec is None or spec.loader is None:
        raise UniversalProducerError(f"Unable to load canonical adapter: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[key] = module
    spec.loader.exec_module(module)
    return module


def _canonical(value: Any) -> Any:
    if isinstance(value, Mapping):
        return OrderedDict((str(k), _canonical(value[k])) for k in sorted(value, key=lambda x: str(x)))
    if isinstance(value, list):
        return [_canonical(item) for item in value]
    if isinstance(value, tuple):
        return [_canonical(item) for item in value]
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(_canonical(value), ensure_ascii=False, separators=(",", ":"), allow_nan=False)


def sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _require_string(value: Any, field: str, maximum: int = 160) -> str:
    if not isinstance(value, str) or not value.strip():
        raise UniversalProducerError(f"{field} must be a non-empty string")
    result = value.strip()
    if len(result) > maximum:
        raise UniversalProducerError(f"{field} exceeds {maximum} characters")
    return result


def _require_int(value: Any, field: str, minimum: int = 0, maximum: int = 2147483646) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise UniversalProducerError(f"{field} must be an integer")
    if not minimum <= value <= maximum:
        raise UniversalProducerError(f"{field} must be in the range {minimum}..{maximum}")
    return value


def _reject_forbidden_editorial(payload: Any, path: str = "production_override") -> None:
    if isinstance(payload, Mapping):
        for key, value in payload.items():
            normalized = str(key).strip().lower()
            if normalized in FORBIDDEN_EDITORIAL_FIELDS:
                raise UniversalProducerError(f"Forbidden non-editorial field: {path}.{key}")
            _reject_forbidden_editorial(value, f"{path}.{key}")
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            _reject_forbidden_editorial(value, f"{path}[{index}]")


def _load_delivery_inputs(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    delivery = _read_json(root / DELIVERY_REL)
    schema = _read_json(root / REQUEST_SCHEMA_REL)
    return delivery, schema


def normalize_universal_request(raw: Mapping[str, Any], root: Path | str | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
    """Validate, resolve and canonicalize the universal request and editorial values."""
    root = project_root(root)
    if not isinstance(raw, Mapping):
        raise UniversalProducerError("Universal Producer Request must be an object")
    delivery_config, request_schema = _load_delivery_inputs(root)
    if request_schema.get("schema") != REQUEST_SCHEMA_ID or request_schema.get("schema_version") != "1.0":
        raise UniversalProducerError("Unsupported D9.9 universal request schema")
    top_allowed = set(request_schema.get("top_level_fields", []))
    extras = set(raw) - top_allowed
    if extras:
        raise UniversalProducerError("Unknown universal request field(s): " + ", ".join(sorted(map(str, extras))))
    if raw.get("schema", REQUEST_SCHEMA_ID) != REQUEST_SCHEMA_ID:
        raise UniversalProducerError("schema must identify the canonical D9.9 universal request")
    if raw.get("schema_version", "1.0") != "1.0":
        raise UniversalProducerError("schema_version must be 1.0")
    request_id = _require_string(raw.get("request_id"), "request_id")
    if not re.fullmatch(r"[A-Za-z0-9_.-]{1,160}", request_id):
        raise UniversalProducerError("request_id may contain only letters, numbers, dot, underscore and hyphen")
    mode = _require_string(raw.get("mode"), "mode")
    if mode not in ALLOWED_MODES:
        raise UniversalProducerError("mode must be REVIEW or PRODUCTION")

    selection_raw = raw.get("selection")
    if not isinstance(selection_raw, Mapping):
        raise UniversalProducerError("selection must be an object")
    selection_allowed = set(request_schema.get("selection_fields", []))
    unknown_selection = set(selection_raw) - selection_allowed
    if unknown_selection:
        raise UniversalProducerError("Unknown selection field(s): " + ", ".join(sorted(map(str, unknown_selection))))
    selection_for_resolver = {key: value for key, value in selection_raw.items() if value is not None}
    try:
        model = load_model(root)
        resolution = resolve_editorial_values(
            selection_for_resolver,
            profile=raw.get("editorial_profile", {}),
            production_override=raw.get("production_override", {}),
            project_root=root,
        )
    except (EditorialModelError, TypeError) as exc:
        raise UniversalProducerError(str(exc)) from exc
    resolved_selection = resolution["selection"]
    content_type = str(resolved_selection["content_type"])
    if content_type not in request_schema.get("supported_content_types", []):
        raise UniversalProducerError(f"Content type is not supported for D9.9 planning: {content_type}")

    seed = _require_int(raw.get("seed"), "seed", SEED_MIN, SEED_MAX)
    music_seed = _require_int(raw.get("music_seed"), "music_seed", SEED_MIN, SEED_MAX)
    delivery_id = _require_string(raw.get("delivery_profile_id"), "delivery_profile_id")
    profiles = delivery_config.get("profiles", {})
    d4_schema_path = root / "definitions" / "c11d" / "production" / "C11D_PRODUCTION_REQUEST_SCHEMA_V1.json"
    d4_schema = _read_json(d4_schema_path)
    d4_delivery_ids = {
        str(value)
        for field in d4_schema.get("fields", [])
        if field.get("name") == "delivery_profile_id"
        for value in field.get("evidence_values", [])
    }
    if delivery_id not in profiles or delivery_id not in d4_delivery_ids:
        raise UniversalProducerError(f"Unknown or non-canonical delivery_profile_id: {delivery_id}")
    provenance = raw.get("provenance", {})
    if not isinstance(provenance, Mapping):
        raise UniversalProducerError("provenance must be an object")
    unknown_provenance = set(provenance) - {"source_revision", "request_origin"}
    if unknown_provenance:
        raise UniversalProducerError("Unknown provenance field(s): " + ", ".join(sorted(map(str, unknown_provenance))))
    origin = provenance.get("request_origin", "UNKNOWN")
    if origin not in {"GUI", "CLI", "API", "TEST", "UNKNOWN"}:
        raise UniversalProducerError("provenance.request_origin must be GUI, CLI, API, TEST or UNKNOWN")
    adapter = _load_module("gui_request", root / "c11c-suite" / "c11c-producer" / "c11d_gui_request.py")
    try:
        resolved_delivery_id, resolved_delivery = adapter.resolve_delivery_profile_data(delivery_id, delivery_config)
    except ValueError as exc:
        raise UniversalProducerError(str(exc)) from exc
    presentation_id = _require_string(raw.get("presentation_profile_id", "UNKNOWN"), "presentation_profile_id")
    variation_index = _require_int(raw.get("variation_index", 0), "variation_index", 0, 1000000)
    audio_enabled = raw.get("audio_enabled", True)
    personalization_enabled = raw.get("personalization_enabled", True)
    if not isinstance(audio_enabled, bool):
        raise UniversalProducerError("audio_enabled must be boolean")
    if not isinstance(personalization_enabled, bool):
        raise UniversalProducerError("personalization_enabled must be boolean")
    profile = raw.get("editorial_profile", {})
    override = raw.get("production_override", {})
    if not isinstance(profile, Mapping) or not isinstance(override, Mapping):
        raise UniversalProducerError("editorial_profile and production_override must be objects")
    _reject_forbidden_editorial(profile, "editorial_profile")
    _reject_forbidden_editorial(override)
    if not personalization_enabled:
        if profile or override:
            raise UniversalProducerError("Disabled personalization cannot carry editorial profile or override values")
        resolved_values = {field: "UNKNOWN" for field in resolved_selection["editable_fields"]}
        resolution = dict(resolution)
        resolution["values"] = resolved_values
        resolution["applied_layers"] = []
    else:
        resolved_values = dict(resolution["values"])

    # This is a semantic universal request: source GUI/CLI and field order do not affect identity.
    canonical_selection = OrderedDict([
        ("content_type", resolved_selection["content_type"]),
        ("family_id", resolved_selection.get("family_id")),
        ("subtype_id", resolved_selection.get("subtype_id")),
        ("variant_id", resolved_selection.get("variant_id")),
        ("variant_scope_id", resolved_selection.get("variant_scope_id")),
        ("difficulty_tier", resolved_selection.get("difficulty_tier")),
    ])
    canonical = OrderedDict([
        ("schema", REQUEST_SCHEMA_ID),
        ("schema_version", "1.0"),
        ("request_id", request_id),
        ("mode", mode),
        ("selection", canonical_selection),
        ("seed", seed),
        ("music_seed", music_seed),
        ("delivery_profile_id", delivery_id),
        ("resolved_delivery_profile_id", resolved_delivery_id),
        ("presentation_profile_id", presentation_id),
        ("variation_index", variation_index),
        ("audio_enabled", audio_enabled),
        ("personalization_enabled", personalization_enabled),
        ("editorial", OrderedDict((field, resolved_values[field]) for field in resolved_selection["editable_fields"])),
        ("editorial_layers_applied", list(resolution.get("applied_layers", []))),
        ("source_revision", "C11D-D9.9-PRODUCER-0.11.0"),
        ("request_origin", "UNKNOWN"),
    ])
    # Validate all editorial payloads again after model resolution; this rejects any unsafe nested additions.
    _reject_forbidden_editorial(canonical["editorial"], "editorial")
    return canonical, {
        "editorial_resolution": resolution,
        "delivery_profile": resolved_delivery,
        "model": model,
        "raw_profile": _canonical(profile),
        "raw_override": _canonical(override),
    }


def _challenge_document(root: Path, challenge_id: str) -> dict[str, Any]:
    path = root / CHALLENGES_REL / f"{challenge_id}.json"
    if not path.exists():
        raise UniversalProducerError(f"Challenge definition missing: {challenge_id}")
    document = _read_json(path)
    if str(document.get("challenge_id")) != challenge_id:
        raise UniversalProducerError(f"Challenge ID/file mismatch: {challenge_id}")
    return document


def evaluate_universal_request(raw: Mapping[str, Any], root: Path | str | None = None) -> dict[str, Any]:
    """Build a stable universal plan; never executes production or activates rendering."""
    root = project_root(root)
    canonical_request, context = normalize_universal_request(raw, root)
    selection = canonical_request["selection"]
    content_type = selection["content_type"]
    request_hash = sha256(canonical_request)
    editorial_hash = sha256({"selection": selection, "editorial": canonical_request["editorial"]})
    d4_evidence: dict[str, Any] | None = None
    d4_plan_hash: str | None = None
    d4_request_hash: str | None = None
    plan_kind: str

    if content_type == "challenges":
        challenge_id = str(selection["variant_id"])
        document = _challenge_document(root, challenge_id)
        gui_adapter = _load_module("gui_request", root / "c11c-suite" / "c11c-producer" / "c11d_gui_request.py")
        editorial = dict(canonical_request["editorial"])
        d4_request = gui_adapter.build_production_request(
            request_id=canonical_request["request_id"],
            mode=canonical_request["mode"],
            challenge_document=document,
            delivery_profile_id=canonical_request["delivery_profile_id"],
            resolved_delivery_profile=context["delivery_profile"],
            presentation_profile_id=canonical_request["presentation_profile_id"],
            seed=canonical_request["seed"],
            music_seed=canonical_request["music_seed"],
            audio_enabled=canonical_request["audio_enabled"],
            variation_index=canonical_request["variation_index"],
            personalization_enabled=canonical_request["personalization_enabled"],
            editorial_values={
                "title": editorial.get("title", "UNKNOWN"),
                "subtitle": editorial.get("subtitle", "UNKNOWN"),
                "call_to_action": editorial.get("call_to_action", "UNKNOWN"),
                "language": editorial.get("language", "UNKNOWN"),
                "player_name": editorial.get("player_name", "UNKNOWN"),
                "challenge_label": editorial.get("challenge_label", "UNKNOWN"),
            },
            source_revision="C11D-D9.9-PRODUCER-0.11.0",
        )
        d4_result = gui_adapter.evaluate_gui_request(d4_request, root)
        d4_plan_hash = d4_result["plan_hash"]
        d4_request_hash = d4_result["request_hash"]
        d4_evidence = {
            "status": d4_result["parity"]["status"],
            "request_hash": d4_request_hash,
            "plan_hash": d4_plan_hash,
            "parity": d4_result["parity"],
            "runtime_authority": d4_result["plan"].get("runtime_authority"),
            "renderer_activation": d4_result["plan"].get("renderer_activation"),
            "orchestrator_execution": d4_result["plan"].get("orchestrator_execution"),
        }
        if d4_result["parity"]["status"] != "PASS":
            raise UniversalProducerError("Canonical D4 Challenge subplan did not pass GUI/CLI parity")
        plan_kind = "UNIVERSAL_PLAN_WITH_CANONICAL_D4_CHALLENGE_SUBPLAN"
    else:
        plan_kind = "UNIVERSAL_EDITORIAL_INTENT_PLAN_ONLY"

    plan = OrderedDict([
        ("schema", PLAN_SCHEMA_ID),
        ("plan_version", "1.0"),
        ("request_id", canonical_request["request_id"]),
        ("mode", canonical_request["mode"]),
        ("plan_kind", plan_kind),
        ("request_hash", request_hash),
        ("editorial_hash", editorial_hash),
        ("selection", selection),
        ("editorial", canonical_request["editorial"]),
        ("seed", canonical_request["seed"]),
        ("music_seed", canonical_request["music_seed"]),
        ("delivery_profile_id", canonical_request["delivery_profile_id"]),
        ("resolved_delivery_profile_id", canonical_request["resolved_delivery_profile_id"]),
        ("presentation_profile_id", canonical_request["presentation_profile_id"]),
        ("variation_index", canonical_request["variation_index"]),
        ("audio_enabled", canonical_request["audio_enabled"]),
        ("d4_subplan_status", "PASS" if d4_evidence else "NOT_APPLICABLE_NO_D4_LOOP_DRILL_CONTRACT"),
        ("d4_request_hash", d4_request_hash),
        ("d4_plan_hash", d4_plan_hash),
        ("steps", [
            OrderedDict([("step_id", "validate_universal_request"), ("type", "VALIDATION"), ("authority", "C11D_D9.9_CANONICAL_ADAPTER")]),
            OrderedDict([("step_id", "resolve_content_identity"), ("type", "CONTENT_SELECTION"), ("content_type", content_type), ("variant_scope_id", selection["variant_scope_id"]), ("authority", "D9.8_UNIVERSAL_EDITORIAL_MODEL")]),
            OrderedDict([("step_id", "resolve_editorial"), ("type", "EDITORIAL_RESOLUTION"), ("editorial_hash", editorial_hash), ("authority", "D9.8_UNIVERSAL_EDITORIAL_MODEL")]),
            OrderedDict([("step_id", "preserve_seed_contract"), ("type", "SEED_GOVERNANCE"), ("gameplay_seed_field", "seed"), ("music_seed_field", "music_seed"), ("cross_domain_sharing", "FORBIDDEN"), ("automatic_generation", False), ("runtime_derivation", False)]),
            OrderedDict([("step_id", "resolve_delivery_profile"), ("type", "DELIVERY_PROFILE"), ("requested_id", canonical_request["delivery_profile_id"]), ("resolved_id", canonical_request["resolved_delivery_profile_id"])]),
            OrderedDict([("step_id", "production_intent_plan"), ("type", "PLAN_ONLY"), ("renderer", False), ("production_execution", False), ("release_authority", "NONE")]),
        ]),
        ("runtime_authority", "NONE"),
        ("simulation_truth_mutation", False),
        ("winning_frame_mutation", False),
        ("close_calls_mutation", False),
        ("gameplay_rng_consumption", False),
        ("structural_rng_consumption", False),
        ("automatic_seed_generation", False),
        ("runtime_seed_derivation", False),
        ("renderer_activation", False),
        ("production_execution", False),
        ("release_authority", "NONE"),
        ("d4_8", "BLOCKED"),
    ])
    plan_hash = sha256(plan)
    return {
        "status": "PLANNED",
        "canonical_request": canonical_request,
        "request_hash": request_hash,
        "editorial_resolution": context["editorial_resolution"],
        "editorial_hash": editorial_hash,
        "plan": plan,
        "plan_hash": plan_hash,
        "d4_evidence": d4_evidence,
        "renderer": False,
        "execution": False,
        "release_authority": "NONE",
    }
