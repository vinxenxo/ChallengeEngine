"""D-owned renderer candidate binding preview; intentionally non-executable.

This module starts the D renderer preparation track by producing an in-memory,
canonical inspection object from a validated D9.10 PREPARE_ONLY envelope. It does
not emit renderer-native input, create files/media, invoke a renderer, or grant
approval/dispatch authority. Proposed slot IDs remain unapproved design targets.
"""
from __future__ import annotations

import copy
import hashlib
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from d_render_adapter import ADAPTER_CONTRACT_REL, ADAPTER_SCHEMA, DRenderAdapterError, validate_d_only_adapter_envelope

SPEC_REL = Path("definitions/c11d/production/D_RENDERER_CANDIDATE_BINDING_PREVIEW_V1.json")
OUTPUT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_CANDIDATE_BINDING_PREVIEW_SCHEMA_V1.json")
EDITORIAL_MODEL_REL = Path("definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json")
DELIVERY_PROFILES_REL = Path("profiles/delivery/c11c_video_delivery_profiles.json")
SPEC_SCHEMA = "C11-D-RENDERER-CANDIDATE-BINDING-PREVIEW-CONTRACT-V1"
PREVIEW_SCHEMA = "C11-D-D9-RENDERER-CANDIDATE-BINDING-PREVIEW-V1"
SUPPORTED_TYPES = ("challenges", "visual_loops", "visual_drills")


class DRendererCandidateError(ValueError):
    """Raised when a binding preview violates the candidate contract."""


def _root(project_root: Path | str | None = None) -> Path:
    return Path(project_root).resolve() if project_root is not None else Path(__file__).resolve().parents[3]


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise DRendererCandidateError(f"Cannot read required D renderer candidate contract input {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise DRendererCandidateError(f"Expected JSON object in {path}")
    return value


def _canonical(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _canonical(value[key]) for key in sorted(value, key=lambda item: str(item))}
    if isinstance(value, (list, tuple)):
        return [_canonical(item) for item in value]
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(_canonical(value), ensure_ascii=False, separators=(",", ":"), allow_nan=False)


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _without_preview_hash(preview: Mapping[str, Any]) -> dict[str, Any]:
    return {str(key): copy.deepcopy(value) for key, value in preview.items() if key != "preview_sha256"}


def _load_spec(root: Path) -> dict[str, Any]:
    spec_path = root / SPEC_REL
    spec = _read_json(spec_path)
    if spec.get("schema") != SPEC_SCHEMA or spec.get("schema_version") != "1.0":
        raise DRendererCandidateError("Unsupported D renderer candidate binding-preview contract identity/version")
    if spec.get("status") != "PREPARATION_ONLY_NOT_APPROVED_NOT_FROZEN":
        raise DRendererCandidateError("Renderer candidate contract cannot claim approval or freeze")
    preview_contract = spec.get("preview_contract", {})
    if preview_contract.get("schema") != PREVIEW_SCHEMA:
        raise DRendererCandidateError("Renderer candidate preview schema identity mismatch")
    if preview_contract.get("json_schema") != str(OUTPUT_SCHEMA_REL).replace("\\", "/"):
        raise DRendererCandidateError("Renderer candidate output JSON Schema path mismatch")
    output_schema = _read_json(root / OUTPUT_SCHEMA_REL)
    if output_schema.get("$id") != "urn:c11d:renderer-candidate-binding-preview:v1" or output_schema.get("properties", {}).get("schema", {}).get("const") != PREVIEW_SCHEMA:
        raise DRendererCandidateError("Renderer candidate output JSON Schema identity mismatch")
    if output_schema.get("additionalProperties") is not False:
        raise DRendererCandidateError("Renderer candidate output schema must reject unknown top-level fields")
    preview_locks = {
        "status": "PREPARATION_ONLY_NOT_RENDERER_INPUT",
        "file_output": False,
        "renderer_input_emitted": False,
        "renderer_dispatch_invoked": False,
        "renderer_activation": False,
        "production_execution": False,
        "media_output_created": False,
        "output_artifact_path": None,
    }
    for key, expected in preview_locks.items():
        if preview_contract.get(key) != expected:
            raise DRendererCandidateError(f"Renderer candidate preview contract lock mismatch: {key}")
    if spec.get("scope", {}).get("supported_content_types") != list(SUPPORTED_TYPES):
        raise DRendererCandidateError("Renderer candidate supported content scope mismatch")
    locks = spec.get("required_locks", {})
    required_locks = {
        "adapter_mode": "PREPARE_ONLY",
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
    for key, expected in required_locks.items():
        if locks.get(key) != expected:
            raise DRendererCandidateError(f"Renderer candidate contract governance lock mismatch: {key}")
    approval = spec.get("approval_state", {})
    if approval.get("renderer_baseline_approved") is not False or approval.get("renderer_baseline_frozen") is not False:
        raise DRendererCandidateError("Renderer candidate specification cannot approve/freeze itself")
    if approval.get("d4_8_authorized") is not False or approval.get("release_authority") != "NONE":
        raise DRendererCandidateError("Renderer candidate specification cannot grant D4.8/release authority")
    return spec


def _resolve_delivery_profile(root: Path, profile_id: Any) -> dict[str, Any]:
    if not isinstance(profile_id, str) or not profile_id.strip():
        raise DRendererCandidateError("Delivery profile identity must be an explicit non-empty string")
    registry_path = root / DELIVERY_PROFILES_REL
    registry = _read_json(registry_path)
    profiles = registry.get("profiles")
    if not isinstance(profiles, Mapping) or profile_id not in profiles:
        raise DRendererCandidateError(f"Unknown delivery profile reference: {profile_id!r}")
    current_id = profile_id
    current = profiles[current_id]
    seen: set[str] = set()
    while isinstance(current, Mapping) and current.get("alias_of"):
        if current_id in seen:
            raise DRendererCandidateError("Delivery profile alias cycle detected")
        seen.add(current_id)
        target_id = current.get("alias_of")
        if not isinstance(target_id, str) or target_id not in profiles:
            raise DRendererCandidateError("Delivery profile alias target is missing or invalid")
        current_id = target_id
        current = profiles[current_id]
    if not isinstance(current, Mapping):
        raise DRendererCandidateError("Resolved delivery profile must be an object")
    field_names = (
        "width", "height", "aspect_ratio", "fps", "fps_min", "fps_max", "codec",
        "container", "pixel_format", "constant_fps", "scan", "audio_codec",
        "audio_profile", "audio_bitrate_kbps", "audio_sample_rate_hz", "audio_channels",
        "duration_min_s", "duration_max_s", "encoder", "preset", "crf", "gop_frames",
    )
    profile_snapshot = {key: copy.deepcopy(current[key]) for key in field_names if key in current}
    if not profile_snapshot or any(isinstance(profile_snapshot.get(name), bool) or not isinstance(profile_snapshot.get(name), int) for name in ("width", "height")):
        raise DRendererCandidateError("Resolved delivery profile has no valid explicit frame geometry")
    fps = profile_snapshot.get("fps")
    if isinstance(fps, bool) or not isinstance(fps, (int, float)) or fps <= 0:
        raise DRendererCandidateError("Resolved delivery profile has no valid explicit frame rate")
    return {
        "requested_profile_id": profile_id,
        "resolved_profile_id": current_id,
        "registry_schema": registry.get("schema"),
        "registry_revision": registry.get("revision"),
        "registry_sha256": _sha256_file(registry_path),
        "resolved_profile_sha256": sha256_json({"profile_id": current_id, "profile": profile_snapshot}),
        "profile": profile_snapshot,
    }


def _assert_no_truth_fields(value: Any, location: str = "candidate_binding") -> None:
    forbidden = {
        "simulationresult", "simulation_result", "simulationtruth", "simulation_truth",
        "winning_frame", "winningframe", "close_calls", "closecalls", "derived_telemetry",
        "derivedtelemetry", "gameplay_rng", "structural_rng",
    }
    if isinstance(value, Mapping):
        for key, child in value.items():
            normalized = str(key).replace("-", "_").lower()
            if normalized in forbidden:
                raise DRendererCandidateError(f"Forbidden simulation/telemetry field in {location}: {key}")
            _assert_no_truth_fields(child, f"{location}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _assert_no_truth_fields(child, f"{location}[{index}]")


def _build_core(adapter_envelope: Mapping[str, Any], root: Path, spec: Mapping[str, Any]) -> dict[str, Any]:
    try:
        validate_d_only_adapter_envelope(adapter_envelope, root)
    except DRenderAdapterError as exc:
        raise DRendererCandidateError(f"D9.10 adapter envelope rejected: {exc}") from exc
    if adapter_envelope.get("schema") != ADAPTER_SCHEMA:
        raise DRendererCandidateError("Unsupported source adapter envelope schema")
    if adapter_envelope.get("status") != "PREPARED_NOT_DISPATCHED_RENDERER_DISABLED":
        raise DRendererCandidateError("Source envelope must remain prepared-only and non-renderable")
    identity = adapter_envelope.get("content_identity")
    bindings = adapter_envelope.get("binding_preview")
    source = adapter_envelope.get("source_identity")
    if not isinstance(identity, Mapping) or not isinstance(bindings, Mapping) or not isinstance(source, Mapping):
        raise DRendererCandidateError("Adapter envelope lacks required identity/binding/provenance objects")
    content_type = identity.get("content_type")
    if content_type not in SUPPORTED_TYPES:
        raise DRendererCandidateError(f"Unsupported renderer candidate content type: {content_type!r}")

    model_path = root / EDITORIAL_MODEL_REL
    model = _read_json(model_path)
    content_contract = model.get("content_types", {}).get(content_type)
    if not isinstance(content_contract, Mapping):
        raise DRendererCandidateError("Canonical editorial model has no content type definition")
    allowlist = content_contract.get("editable_fields")
    editorial_values = bindings.get("editorial_bindings")
    if not isinstance(allowlist, list) or not isinstance(editorial_values, Mapping):
        raise DRendererCandidateError("Editorial allowlist/bindings are malformed")
    if bindings.get("editorial_allowlist_fields") != sorted(allowlist) or set(editorial_values) - set(allowlist):
        raise DRendererCandidateError("Adapter editorial allowlist/bindings mismatch canonical model")
    source_editorial_hash = source.get("editorial_hash")
    recomputed_editorial_hash = sha256_json({"selection": dict(identity), "editorial": dict(editorial_values)})
    if source_editorial_hash != recomputed_editorial_hash:
        raise DRendererCandidateError("Editorial binding values do not match the immutable source editorial hash")
    _assert_no_truth_fields({"content_identity": identity, "editorial_bindings": editorial_values})

    slots = spec.get("proposed_editorial_slot_ids", {})
    editorial_preview: list[dict[str, Any]] = []
    for field in sorted(editorial_values):
        value = editorial_values[field]
        if field not in slots:
            raise DRendererCandidateError(f"No proposed target slot exists for editorial field: {field}")
        if not isinstance(value, str):
            raise DRendererCandidateError(f"Editorial field must remain a canonical string: {field}")
        editorial_preview.append({
            "source_field": field,
            "proposed_slot_id": slots[field],
            "mapping_state": "PROPOSED_NOT_APPROVED",
            "value": value,
            "value_sha256": sha256_json(value),
        })

    seed = bindings.get("seed_contract")
    if not isinstance(seed, Mapping):
        raise DRendererCandidateError("Seed-domain contract is missing")
    game_seed, music_seed = seed.get("gameplay_seed"), seed.get("music_seed")
    for name, number in (("gameplay_seed", game_seed), ("music_seed", music_seed)):
        if isinstance(number, bool) or not isinstance(number, int) or not 1 <= number <= 2147483646:
            raise DRendererCandidateError(f"Invalid isolated seed value: {name}")
    if game_seed == music_seed:
        raise DRendererCandidateError("Gameplay and music seed values must remain distinct")
    seed_rules = {
        "gameplay_seed_source": "canonical_request.seed",
        "gameplay_seed_domain": "GAMEPLAY",
        "music_seed_source": "canonical_request.music_seed",
        "music_seed_domain": "MUSIC",
        "cross_domain_seed_sharing": "FORBIDDEN",
        "automatic_seed_generation": False,
        "runtime_seed_derivation": False,
    }
    for key, expected in seed_rules.items():
        if seed.get(key) != expected:
            raise DRendererCandidateError(f"Seed-domain contract mismatch: {key}")

    delivery = _resolve_delivery_profile(root, bindings.get("delivery_profile_id"))
    presentation_id = bindings.get("presentation_profile_id")
    if not isinstance(presentation_id, str) or not presentation_id.strip() or presentation_id == "UNKNOWN":
        raise DRendererCandidateError("Presentation profile must be an explicit canonical reference")
    variation = bindings.get("variation_index")
    if isinstance(variation, bool) or not isinstance(variation, int) or variation < 0:
        raise DRendererCandidateError("Variation index must be an explicit non-negative integer")
    audio_enabled = bindings.get("audio_enabled")
    if not isinstance(audio_enabled, bool):
        raise DRendererCandidateError("Audio flag must be an explicit boolean")
    if bindings.get("simulation_truth") != "NOT_BOUND" or bindings.get("derived_telemetry") != "NOT_BOUND":
        raise DRendererCandidateError("Simulation truth and derived telemetry must remain unbound")

    source_hashes: dict[str, str] = {}
    for key in ("request_hash", "editorial_hash", "plan_hash", "bridge_record_hash"):
        digest = source.get(key)
        if not isinstance(digest, str) or len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest):
            raise DRendererCandidateError(f"Missing or malformed immutable source identity: {key}")
        source_hashes[key] = digest

    adapter_contract_path = root / ADAPTER_CONTRACT_REL
    payload = {
        "schema": PREVIEW_SCHEMA,
        "schema_version": "1.0",
        "status": "PREPARATION_ONLY_NOT_RENDERER_INPUT",
        "contract_identity": {
            "schema": SPEC_SCHEMA,
            "schema_version": "1.0",
            "sha256": _sha256_file(root / SPEC_REL),
            "output_schema_sha256": _sha256_file(root / OUTPUT_SCHEMA_REL),
        },
        "source_contract_identities": {
            "adapter_contract_canonical_sha256": adapter_envelope.get("adapter_contract_identity", {}).get("sha256"),
            "adapter_contract_file_sha256": _sha256_file(adapter_contract_path),
            "editorial_model_canonical_sha256": adapter_envelope.get("editorial_model_identity", {}).get("sha256"),
            "editorial_model_file_sha256": _sha256_file(model_path),
            "delivery_registry_file_sha256": delivery["registry_sha256"],
        },
        "implementation_identity": {
            "module": "tools/c11d/d9/d_renderer_candidate.py",
            "version": "0.1.0-preparation",
            "sha256": _sha256_file(Path(__file__).resolve()),
        },
        "source_identity": {**source_hashes, "adapter_envelope_hash": adapter_envelope.get("envelope_hash")},
        "content_identity": copy.deepcopy(dict(identity)),
        "editorial_binding_preview": editorial_preview,
        "delivery_profile": delivery,
        "presentation_profile_id": presentation_id,
        "variation_index": variation,
        "audio_enabled": audio_enabled,
        "seed_contract": {
            "gameplay_seed": game_seed,
            "gameplay_seed_source": seed_rules["gameplay_seed_source"],
            "gameplay_seed_domain": seed_rules["gameplay_seed_domain"],
            "music_seed": music_seed,
            "music_seed_source": seed_rules["music_seed_source"],
            "music_seed_domain": seed_rules["music_seed_domain"],
            "cross_domain_seed_sharing": seed_rules["cross_domain_seed_sharing"],
            "automatic_seed_generation": seed_rules["automatic_seed_generation"],
            "runtime_seed_derivation": seed_rules["runtime_seed_derivation"],
        },
        "truth_and_telemetry": {"simulation_truth": "NOT_BOUND", "derived_telemetry": "NOT_BOUND"},
        "execution_boundary": {
            "candidate_mode": "NON_EXECUTABLE_BINDING_REVIEW",
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
    payload["preview_sha256"] = sha256_json(payload)
    return payload


def build_renderer_binding_preview(
    adapter_envelope: Mapping[str, Any], project_root: Path | str | None = None
) -> dict[str, Any]:
    """Build a deterministic, in-memory preview; no files, media or processes are created."""
    root = _root(project_root)
    spec = _load_spec(root)
    preview = _build_core(adapter_envelope, root, spec)
    validate_renderer_binding_preview(preview, adapter_envelope, root)
    return preview


def validate_renderer_binding_preview(
    preview: Mapping[str, Any],
    source_envelope: Mapping[str, Any],
    project_root: Path | str | None = None,
) -> bool:
    """Validate preview self-hash, source-envelope lineage and every governance lock."""
    root = _root(project_root)
    spec = _load_spec(root)
    if not isinstance(preview, Mapping) or preview.get("schema") != PREVIEW_SCHEMA:
        raise DRendererCandidateError("Unsupported renderer candidate preview schema")
    if preview.get("status") != "PREPARATION_ONLY_NOT_RENDERER_INPUT":
        raise DRendererCandidateError("Renderer candidate preview may not claim renderer readiness")
    schema_doc = _read_json(root / OUTPUT_SCHEMA_REL)
    required_fields = set(schema_doc.get("required", []))
    if set(preview) != required_fields:
        raise DRendererCandidateError("Renderer candidate preview has missing or unknown top-level fields")
    if preview.get("preview_sha256") != sha256_json(_without_preview_hash(preview)):
        raise DRendererCandidateError("Renderer candidate preview hash mismatch")
    locks = preview.get("execution_boundary")
    required_locks = {
        "candidate_mode": "NON_EXECUTABLE_BINDING_REVIEW",
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
    if not isinstance(locks, Mapping):
        raise DRendererCandidateError("Renderer candidate execution boundary is missing")
    for key, expected in required_locks.items():
        if locks.get(key) != expected:
            raise DRendererCandidateError(f"Renderer candidate execution lock mismatch: {key}")
    truth_fields = {key: preview[key] for key in ("content_identity", "editorial_binding_preview") if key in preview}
    _assert_no_truth_fields(truth_fields)
    expected = _build_core(source_envelope, root, spec)
    if dict(preview) != expected:
        raise DRendererCandidateError("Renderer candidate preview does not match its validated source envelope")
    return True
