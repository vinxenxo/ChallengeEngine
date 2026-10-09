"""C11-D-only renderer binding adapter, prepare-only and fail-closed.

This module binds a validated D9.9 canonical plan plus D9.10 bridge record into a
versioned inspection envelope. It never imports C11-C renderer code, launches a
renderer, emits renderer-native input, creates media, or grants production authority.
"""
from __future__ import annotations

import copy
import hashlib
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from editorial_render_bridge import (
    CONTRACT_REL as BRIDGE_CONTRACT_REL,
    MODEL_REL,
    RECORD_SCHEMA as BRIDGE_RECORD_SCHEMA,
    EditorialRenderBridgeError,
    _canonical,
    _read_json,
    _root,
    canonical_json,
    sha256,
)

ADAPTER_CONTRACT_REL = Path("definitions/c11d/production/C11D_RENDER_ADAPTER_BOUNDARY_D9_10_V1.json")
ADAPTER_SCHEMA = "C11-D-D9.10-D-ONLY-RENDER-ADAPTER-ENVELOPE-V1"
ADAPTER_CONTRACT_SCHEMA = "C11-D-D9.10-RENDER-ADAPTER-BOUNDARY-CONTRACT-V1"
PLAN_SCHEMA = "C11-D-D9.9-UNIVERSAL-PRODUCER-PLAN-V1"


class DRenderAdapterError(ValueError):
    """Raised when a canonical plan cannot safely cross the D adapter boundary."""


def _read_adapter_contract(root: Path) -> dict[str, Any]:
    try:
        contract = _read_json(root / ADAPTER_CONTRACT_REL)
    except Exception as exc:
        raise DRenderAdapterError(f"Cannot load D-only render adapter boundary: {exc}") from exc
    if contract.get("schema") != ADAPTER_CONTRACT_SCHEMA or contract.get("schema_version") != "1.0":
        raise DRenderAdapterError("Unsupported D-only render adapter contract identity/version")
    policy = contract.get("policy", {})
    required_locks = {
        "scope": "C11-D_ONLY",
        "adapter_prepare_enabled": True,
        "renderer_dispatch_enabled": False,
        "renderer_activation": False,
        "renderer_input_emitted": False,
        "production_execution": False,
        "media_output_created": False,
        "d4_8": "BLOCKED",
        "release_authority": "NONE",
        "c11c_source_mutation": False,
    }
    for key, expected in required_locks.items():
        if policy.get(key) != expected:
            raise DRenderAdapterError(f"D-only adapter policy invariant mismatch: {key}")
    return contract


def _without_hash(envelope: Mapping[str, Any]) -> dict[str, Any]:
    return {str(key): copy.deepcopy(value) for key, value in envelope.items() if key != "envelope_hash"}


def validate_d_only_adapter_envelope(envelope: Mapping[str, Any], project_root: Path | str | None = None) -> bool:
    """Audit the envelope self-hash and all non-activating policy locks."""
    root = _root(project_root)
    contract = _read_adapter_contract(root)
    if not isinstance(envelope, Mapping) or envelope.get("schema") != ADAPTER_SCHEMA:
        raise DRenderAdapterError("Unsupported D-only adapter envelope schema")
    if envelope.get("status") != "PREPARED_NOT_DISPATCHED_RENDERER_DISABLED":
        raise DRenderAdapterError("D-only adapter envelope status cannot claim renderability")
    if envelope.get("adapter_contract_identity", {}).get("sha256") != sha256(contract):
        raise DRenderAdapterError("D-only adapter contract identity/hash mismatch")
    locked = {
        "d_only_adapter_prepare_invoked": True,
        "renderer_dispatch_invoked": False,
        "renderer_activation": False,
        "renderer_input_emitted": False,
        "production_execution": False,
        "media_output_created": False,
        "output_artifact_path": None,
        "d4_8": "BLOCKED",
        "release_authority": "NONE",
        "c11c_source_mutation": False,
    }
    for key, expected in locked.items():
        if envelope.get(key) != expected:
            raise DRenderAdapterError(f"D-only adapter envelope governance invariant mismatch: {key}")
    if envelope.get("envelope_hash") != sha256(_without_hash(envelope)):
        raise DRenderAdapterError("D-only adapter envelope hash mismatch")
    adapter_execution = envelope.get("adapter_execution")
    if not isinstance(adapter_execution, Mapping):
        raise DRenderAdapterError("D-only adapter execution boundary must be an object")
    nested_locks = {
        "mode": "PREPARE_ONLY",
        "scope": "C11-D_ONLY",
        "adapter_prepare_enabled": True,
        "renderer_dispatch_invoked": False,
        "reason_not_dispatched": "D4.8_BLOCKED_AND_D_BASELINE_NOT_APPROVED",
    }
    for key, expected in nested_locks.items():
        if adapter_execution.get(key) != expected:
            raise DRenderAdapterError(f"D-only adapter execution invariant mismatch: {key}")
    bindings = envelope.get("binding_preview")
    if not isinstance(bindings, Mapping):
        raise DRenderAdapterError("D-only adapter binding preview must be an object")
    if bindings.get("simulation_truth") != "NOT_BOUND" or bindings.get("derived_telemetry") != "NOT_BOUND":
        raise DRenderAdapterError("D-only adapter may not bind simulation truth/derived telemetry")
    identity = envelope.get("content_identity", {})
    content_type = identity.get("content_type") if isinstance(identity, Mapping) else None
    model = _read_json(root / MODEL_REL)
    content_types = model.get("content_types", {})
    if content_type not in content_types:
        raise DRenderAdapterError("D-only adapter envelope has unsupported content identity")
    expected_allowlist = sorted(content_types[content_type].get("editable_fields", []))
    if bindings.get("editorial_allowlist_fields") != expected_allowlist:
        raise DRenderAdapterError("D-only adapter envelope editable-field registry identity mismatch")
    editorial_bindings = bindings.get("editorial_bindings")
    if not isinstance(editorial_bindings, Mapping) or set(editorial_bindings) - set(expected_allowlist):
        raise DRenderAdapterError("D-only adapter envelope contains non-allowlisted editorial fields")
    seed_contract = bindings.get("seed_contract", {})
    for key in ("gameplay_seed", "music_seed"):
        seed = seed_contract.get(key)
        if isinstance(seed, bool) or not isinstance(seed, int) or seed < 1 or seed > 2147483646:
            raise DRenderAdapterError(f"D-only adapter envelope invalid seed identity: {key}")
    if seed_contract.get("gameplay_seed_source") != "canonical_request.seed" or seed_contract.get("gameplay_seed_domain") != "GAMEPLAY":
        raise DRenderAdapterError("Gameplay seed binding source/domain mismatch")
    if seed_contract.get("music_seed_source") != "canonical_request.music_seed" or seed_contract.get("music_seed_domain") != "MUSIC":
        raise DRenderAdapterError("Music seed binding source/domain mismatch")
    if seed_contract.get("cross_domain_seed_sharing") != "FORBIDDEN" or seed_contract.get("automatic_seed_generation") is not False or seed_contract.get("runtime_seed_derivation") is not False:
        raise DRenderAdapterError("D-only adapter envelope violates seed governance")
    if seed_contract["gameplay_seed"] == seed_contract["music_seed"]:
        raise DRenderAdapterError("Gameplay and music seed values must remain isolated")
    return True


def prepare_d_only_adapter_envelope(
    result: Mapping[str, Any],
    bridge_record: Mapping[str, Any],
    project_root: Path | str | None = None,
) -> dict[str, Any]:
    """Prepare a hash-bound D render-binding envelope without renderer dispatch.

    This is intentionally a pure preparation step: it emits an inspectable JSON
    envelope, not renderer-native input. No files, media or processes are created.
    """
    root = _root(project_root)
    adapter_contract = _read_adapter_contract(root)
    bridge_contract = _read_json(root / BRIDGE_CONTRACT_REL)
    model = _read_json(root / MODEL_REL)

    if not isinstance(result, Mapping) or result.get("status") != "PLANNED":
        raise DRenderAdapterError("Adapter requires a successful canonical D9.9 PLANNED result")
    if not isinstance(bridge_record, Mapping) or bridge_record.get("schema") != BRIDGE_RECORD_SCHEMA:
        raise DRenderAdapterError("Adapter requires a D9.10 bridge planning record")
    if bridge_record.get("status") != "PLANNING_ONLY_NOT_RENDERABLE":
        raise DRenderAdapterError("Bridge record cannot claim renderer readiness")
    if bridge_record.get("record_hash") != sha256({key: value for key, value in bridge_record.items() if key != "record_hash"}):
        raise DRenderAdapterError("Bridge record hash mismatch")
    if bridge_record.get("contract_identity", {}).get("sha256") != sha256(bridge_contract):
        raise DRenderAdapterError("Bridge contract identity mismatch")
    if bridge_record.get("editorial_model_identity", {}).get("sha256") != sha256(model):
        raise DRenderAdapterError("Universal editorial model identity mismatch")

    plan = result.get("plan")
    request = result.get("canonical_request")
    if not isinstance(plan, Mapping) or not isinstance(request, Mapping) or plan.get("schema") != PLAN_SCHEMA:
        raise DRenderAdapterError("Adapter input is not a canonical D9.9 request/plan pair")
    if result.get("request_hash") != sha256(request) or result.get("plan_hash") != sha256(plan):
        raise DRenderAdapterError("Canonical request/plan hash mismatch")
    if result.get("editorial_hash") != sha256({"selection": plan.get("selection"), "editorial": plan.get("editorial")}):
        raise DRenderAdapterError("Canonical editorial hash mismatch")

    for key, expected in (
        ("request_hash", result["request_hash"]),
        ("editorial_hash", result["editorial_hash"]),
        ("plan_hash", result["plan_hash"]),
    ):
        if bridge_record.get("identity", {}).get(key) != expected:
            raise DRenderAdapterError(f"Bridge record is not bound to canonical {key}")

    selection = plan.get("selection")
    editorial = plan.get("editorial")
    if not isinstance(selection, Mapping) or not isinstance(editorial, Mapping):
        raise DRenderAdapterError("Canonical plan selection/editorial must be objects")
    content_type = selection.get("content_type")
    model_types = model.get("content_types", {})
    if content_type not in model_types:
        raise DRenderAdapterError(f"Unsupported D-only adapter content type: {content_type!r}")
    allowlist = set(model_types[content_type].get("editable_fields", []))
    unexpected = set(editorial) - allowlist
    if unexpected:
        raise DRenderAdapterError("Editorial bindings exceed the canonical allowlist: " + ", ".join(sorted(unexpected)))
    if bridge_record.get("editorial", {}).get("values_hash") != sha256(editorial):
        raise DRenderAdapterError("Bridge editorial values are not bound to canonical editorial payload")
    if bridge_record.get("editorial", {}).get("fields") != sorted(editorial):
        raise DRenderAdapterError("Bridge editorial field list does not match canonical payload")
    if bridge_record.get("selection") != dict(selection):
        raise DRenderAdapterError("Bridge content identity does not match canonical plan")

    seed_contract = bridge_record.get("seed_contract", {})
    for key, expected in (("gameplay_seed", request.get("seed")), ("music_seed", request.get("music_seed"))):
        actual = plan.get("seed" if key == "gameplay_seed" else "music_seed")
        if isinstance(expected, bool) or not isinstance(expected, int) or actual != expected or seed_contract.get(key) != expected:
            raise DRenderAdapterError(f"Seed domain binding mismatch: {key}")
    if seed_contract.get("cross_domain_seed_sharing") != "FORBIDDEN":
        raise DRenderAdapterError("Gameplay/music seed domains must remain isolated")
    if plan.get("seed") == plan.get("music_seed"):
        raise DRenderAdapterError("Gameplay and music seed values must remain isolated")
    if plan.get("renderer_activation") is not False or plan.get("production_execution") is not False:
        raise DRenderAdapterError("Canonical plan cannot request renderer activation or production")
    if result.get("release_authority") != "NONE" or plan.get("release_authority") != "NONE" or plan.get("d4_8") != "BLOCKED":
        raise DRenderAdapterError("Governance escalation rejected at D-only adapter boundary")

    policy = adapter_contract["policy"]
    envelope: dict[str, Any] = {
        "schema": ADAPTER_SCHEMA,
        "schema_version": "1.0",
        "status": "PREPARED_NOT_DISPATCHED_RENDERER_DISABLED",
        "adapter_contract_identity": {
            "schema": adapter_contract["schema"],
            "schema_version": adapter_contract["schema_version"],
            "sha256": sha256(adapter_contract),
        },
        "bridge_contract_identity": copy.deepcopy(bridge_record["contract_identity"]),
        "editorial_model_identity": copy.deepcopy(bridge_record["editorial_model_identity"]),
        "source_identity": {
            "request_id": request.get("request_id"),
            "request_hash": result["request_hash"],
            "editorial_hash": result["editorial_hash"],
            "plan_hash": result["plan_hash"],
            "bridge_record_hash": bridge_record["record_hash"],
        },
        "content_identity": copy.deepcopy(dict(selection)),
        "binding_preview": {
            "editorial_bindings": copy.deepcopy(dict(editorial)),
            "editorial_allowlist_fields": sorted(allowlist),
            "delivery_profile_id": plan.get("resolved_delivery_profile_id"),
            "presentation_profile_id": plan.get("presentation_profile_id"),
            "variation_index": plan.get("variation_index"),
            "audio_enabled": plan.get("audio_enabled"),
            "seed_contract": {
                "gameplay_seed": request["seed"],
                "gameplay_seed_source": "canonical_request.seed",
                "gameplay_seed_domain": "GAMEPLAY",
                "music_seed": request["music_seed"],
                "music_seed_source": "canonical_request.music_seed",
                "music_seed_domain": "MUSIC",
                "cross_domain_seed_sharing": "FORBIDDEN",
                "automatic_seed_generation": False,
                "runtime_seed_derivation": False,
            },
            "simulation_truth": "NOT_BOUND",
            "derived_telemetry": "NOT_BOUND",
        },
        "adapter_execution": {
            "mode": "PREPARE_ONLY",
            "scope": "C11-D_ONLY",
            "adapter_prepare_enabled": True,
            "renderer_dispatch_invoked": False,
            "reason_not_dispatched": "D4.8_BLOCKED_AND_D_BASELINE_NOT_APPROVED",
        },
        "d_only_adapter_prepare_invoked": True,
        "renderer_dispatch_invoked": False,
        "renderer_input_emitted": False,
        "renderer_activation": False,
        "production_execution": False,
        "media_output_created": False,
        "output_artifact_path": None,
        "d4_8": "BLOCKED",
        "release_authority": "NONE",
        "c11c_source_mutation": False,
        "policy_identity": policy.get("policy_id"),
    }
    envelope["envelope_hash"] = sha256(envelope)
    validate_d_only_adapter_envelope(envelope, root)
    return envelope
