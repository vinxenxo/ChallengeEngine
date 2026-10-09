"""D9.10 plan-only bridge from universal editorial plans to a future D renderer.

This module records mappings and readiness gates. It deliberately does not emit
renderer inputs, call a renderer, materialize media, or grant production authority.
"""
from __future__ import annotations

import copy
import hashlib
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

CONTRACT_REL = Path("definitions/c11d/production/C11D_EDITORIAL_RENDER_BRIDGE_D9_10_V1.json")
MODEL_REL = Path("definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json")
CONTRACT_SCHEMA = "C11-D-D9.10-EDITORIAL-RENDER-BRIDGE-CONTRACT-V1"
RECORD_SCHEMA = "C11-D-D9.10-EDITORIAL-RENDER-BRIDGE-PLAN-V1"
PLAN_SCHEMA = "C11-D-D9.9-UNIVERSAL-PRODUCER-PLAN-V1"


class EditorialRenderBridgeError(ValueError):
    """Raised when an input is not a valid plan-only bridge candidate."""


def _root(path: Path | str | None = None) -> Path:
    return Path(path).resolve() if path is not None else Path(__file__).resolve().parents[3]


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise EditorialRenderBridgeError(f"Cannot load bridge contract input {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise EditorialRenderBridgeError(f"Expected JSON object: {path}")
    return value


def _canonical(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _canonical(value[key]) for key in sorted(value, key=lambda item: str(item))}
    if isinstance(value, (list, tuple)):
        return [_canonical(item) for item in value]
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(_canonical(value), ensure_ascii=False, separators=(",", ":"), allow_nan=False)


def sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def load_contract(path: Path | str | None = None) -> dict[str, Any]:
    root = _root(path)
    contract = _read_json(root / CONTRACT_REL)
    if contract.get("schema") != CONTRACT_SCHEMA or contract.get("schema_version") != "1.0":
        raise EditorialRenderBridgeError("Unsupported D9.10 bridge contract identity/version")
    if contract.get("output", {}).get("schema") != RECORD_SCHEMA:
        raise EditorialRenderBridgeError("Bridge contract output schema mismatch")
    gates = contract.get("governance", {})
    if gates.get("renderer_activation") is not False or gates.get("production_execution") is not False:
        raise EditorialRenderBridgeError("D9.10 bridge contract may not activate renderer/production")
    if gates.get("d4_8") != "BLOCKED" or gates.get("release_authority") != "NONE":
        raise EditorialRenderBridgeError("D9.10 bridge contract governance must remain blocked")
    return contract


def build_bridge_planning_record(result: Mapping[str, Any], project_root: Path | str | None = None) -> dict[str, Any]:
    """Validate a canonical D9.9 result and derive an inspectable bridge plan record only."""
    root = _root(project_root)
    contract = load_contract(root)
    model = _read_json(root / MODEL_REL)
    if not isinstance(result, Mapping) or result.get("status") != "PLANNED":
        raise EditorialRenderBridgeError("Input must be a successful canonical D9.9 PLANNED result")
    plan = result.get("plan")
    request = result.get("canonical_request")
    if not isinstance(plan, Mapping) or not isinstance(request, Mapping):
        raise EditorialRenderBridgeError("Canonical result must include plan and canonical_request objects")
    if plan.get("schema") != PLAN_SCHEMA:
        raise EditorialRenderBridgeError("Unsupported canonical plan schema; renderer plans are not accepted")
    if result.get("request_hash") != sha256(request):
        raise EditorialRenderBridgeError("Canonical request hash mismatch")
    if result.get("plan_hash") != sha256(plan):
        raise EditorialRenderBridgeError("Canonical plan hash mismatch")
    if result.get("editorial_hash") != sha256({"selection": plan.get("selection"), "editorial": plan.get("editorial")}):
        raise EditorialRenderBridgeError("Canonical editorial hash mismatch")

    governance = contract["governance"]
    locked_false = (
        (result.get("renderer"), "result.renderer"),
        (result.get("execution"), "result.execution"),
        (plan.get("renderer_activation"), "plan.renderer_activation"),
        (plan.get("production_execution"), "plan.production_execution"),
        (plan.get("simulation_truth_mutation"), "plan.simulation_truth_mutation"),
        (plan.get("winning_frame_mutation"), "plan.winning_frame_mutation"),
        (plan.get("close_calls_mutation"), "plan.close_calls_mutation"),
        (plan.get("gameplay_rng_consumption"), "plan.gameplay_rng_consumption"),
        (plan.get("structural_rng_consumption"), "plan.structural_rng_consumption"),
        (plan.get("automatic_seed_generation"), "plan.automatic_seed_generation"),
        (plan.get("runtime_seed_derivation"), "plan.runtime_seed_derivation"),
    )
    for value, label in locked_false:
        if value is not False:
            raise EditorialRenderBridgeError(f"Governance invariant must be false: {label}")
    if result.get("release_authority") != governance["release_authority"] or plan.get("release_authority") != governance["release_authority"]:
        raise EditorialRenderBridgeError("release_authority must remain NONE")
    if plan.get("d4_8") != governance["d4_8"]:
        raise EditorialRenderBridgeError("D4.8 must remain BLOCKED")

    selection = plan.get("selection")
    editorial = plan.get("editorial")
    content_type = selection.get("content_type") if isinstance(selection, Mapping) else None
    if content_type not in contract["supported_content_types"]:
        raise EditorialRenderBridgeError(f"Unsupported content type for D9.10: {content_type!r}")
    if content_type not in model.get("content_types", {}):
        raise EditorialRenderBridgeError(f"Content type missing from canonical model: {content_type!r}")
    if not isinstance(editorial, Mapping):
        raise EditorialRenderBridgeError("Plan editorial payload must be an object")
    allowed_fields = set(model["content_types"][content_type].get("editable_fields", []))
    unexpected_fields = set(editorial) - allowed_fields
    if unexpected_fields:
        raise EditorialRenderBridgeError("Non-editorial fields in bridge payload: " + ", ".join(sorted(unexpected_fields)))

    for name in ("seed", "music_seed"):
        value = plan.get(name)
        if isinstance(value, bool) or not isinstance(value, int) or value < 1 or value > 2147483646:
            raise EditorialRenderBridgeError(f"{name} must be an explicit canonical integer seed")
    if plan.get("seed") != request.get("seed"):
        raise EditorialRenderBridgeError("Gameplay seed must remain bound to canonical request.seed")
    if plan.get("music_seed") != request.get("music_seed"):
        raise EditorialRenderBridgeError("Music seed must remain bound to canonical request.music_seed")

    route = contract["routes"][content_type]
    if plan.get("plan_kind") != route["required_plan_kind"]:
        raise EditorialRenderBridgeError(f"Plan kind mismatch for content type {content_type}")
    if plan.get("d4_subplan_status") != route["required_d4_subplan_status"]:
        raise EditorialRenderBridgeError(f"D4 subplan status mismatch for content type {content_type}")
    if content_type == "challenges":
        if not result.get("d4_evidence") or result["d4_evidence"].get("status") != "PASS":
            raise EditorialRenderBridgeError("Challenge bridge route requires passing canonical D4 subordinate evidence")
        if not plan.get("d4_request_hash") or not plan.get("d4_plan_hash"):
            raise EditorialRenderBridgeError("Challenge bridge route requires canonical D4 request/plan identities")
    elif result.get("d4_evidence") is not None or plan.get("d4_request_hash") is not None or plan.get("d4_plan_hash") is not None:
        raise EditorialRenderBridgeError("Loop/Drill must not claim a non-existent canonical D4 subplan")

    record: dict[str, Any] = {
        "schema": RECORD_SCHEMA,
        "schema_version": "1.0",
        "status": "PLANNING_ONLY_NOT_RENDERABLE",
        "contract_schema": contract["schema"],
        "contract_identity": {
            "schema": contract["schema"],
            "schema_version": contract["schema_version"],
            "sha256": sha256(contract),
        },
        "editorial_model_identity": {
            "schema": model.get("schema"),
            "schema_version": model.get("schema_version"),
            "checkpoint": model.get("checkpoint"),
            "sha256": sha256(model),
        },
        "request_id": request.get("request_id"),
        "content_type": content_type,
        "route": copy.deepcopy(route),
        "identity": {
            "request_hash": result["request_hash"],
            "editorial_hash": result["editorial_hash"],
            "plan_hash": result["plan_hash"],
            "d4_request_hash": plan.get("d4_request_hash"),
            "d4_plan_hash": plan.get("d4_plan_hash"),
        },
        "selection": copy.deepcopy(selection),
        "editorial": {
            "fields": sorted(editorial),
            "allowlist_source": MODEL_REL.as_posix(),
            "destination_contract": "FUTURE_D_RENDERER_BINDER_NOT_DEFINED",
            "values_hash": sha256(editorial),
        },
        "field_mappings": copy.deepcopy(contract["mapping_contract"]),
        "seed_contract": {
            "gameplay_seed_source": "canonical_plan.seed",
            "gameplay_seed": plan["seed"],
            "gameplay_seed_domain": "GAMEPLAY",
            "music_seed_source": "canonical_plan.music_seed",
            "music_seed": plan["music_seed"],
            "music_seed_domain": "MUSIC",
            "cross_domain_seed_sharing": "FORBIDDEN",
            "automatic_seed_generation": False,
            "runtime_seed_derivation": False,
        },
        "delivery_profile_id": plan.get("resolved_delivery_profile_id"),
        "presentation_profile_id": plan.get("presentation_profile_id"),
        "variation_index": plan.get("variation_index"),
        "audio_enabled": plan.get("audio_enabled"),
        "future_d_frozen_baseline_gates": list(contract["future_d_frozen_baseline_gates"]),
        "governance": copy.deepcopy(governance),
        "renderer_input_emitted": False,
        "renderer_adapter_invoked": False,
        "renderer_activation": False,
        "production_execution": False,
        "media_output_created": False,
        "output_artifact_path": None,
        "d4_8": "BLOCKED",
        "release_authority": "NONE",
    }
    record["record_hash"] = sha256(record)
    return record
