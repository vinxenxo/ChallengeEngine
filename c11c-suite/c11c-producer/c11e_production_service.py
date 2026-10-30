"""C11-E shared GUI/CLI production-intent service.

E1 is deliberately preparation-only. This service is the single entry point for
GUI and CLI requests, delegates request semantics to the accepted D9.9 resolver,
and emits a sealed E-owned intent. It does not call D9.10, a C runner, Godot,
FFmpeg, or any renderer.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import re
import sys
from collections.abc import Mapping
from pathlib import Path, PurePosixPath
from typing import Any

SERVICE_SCHEMA = "C11-E-PRODUCTION-INTENT-V1"
SERVICE_VERSION = "0.1.0-E1"
EXPECTED_C11C_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
EXPECTED_C11C_MANIFEST_BYTES = 796318
SUPPORTED_CONTENT_TYPES = ("challenges", "visual_loops", "visual_drills")
ALLOWED_ORIGINS = {"GUI", "CLI", "API", "TEST", "UNKNOWN"}

# These three implementations were captured from the active checkout during the
# E0/E1 review. A changed resolver is a new E1 source set and must be reviewed.
EXPECTED_D9_SOURCE_PINS = {
    "tools/c11d/d9/universal_producer.py": "9ad2adbf54946f2225ae2ed36b88abfc5717387f2ff03bbed684aa8bd32d87d1",
    "tools/c11d/d9/universal_editorial_model.py": "5c575be1942ba0613d66579d14db5cf9d7786e7062dfb001bd7be8a2e9c18ae5",
    "c11c-suite/c11c-producer/c11d_gui_request.py": "0e95109ffd3ba5655d28292309196349470ab7958a467f096543a2c98c22976e",
}


class C11EProductionServiceError(ValueError):
    """Raised when an E1 request or its source identity is invalid."""


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _canonical(value[key]) for key in sorted(value, key=lambda item: str(item))}
    if isinstance(value, (list, tuple)):
        return [_canonical(item) for item in value]
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(_canonical(value), ensure_ascii=False, separators=(",", ":"), allow_nan=False)


def sha256(value: Any) -> str:
    return _sha256_bytes(canonical_json(value).encode("utf-8"))


def _root(project_root: Path | str | None) -> Path:
    if project_root is None:
        # c11c-suite/c11c-producer/c11e_production_service.py -> repo root
        return Path(__file__).resolve().parents[2]
    result = Path(project_root).resolve()
    if not result.is_dir():
        raise C11EProductionServiceError(f"Project root does not exist: {result}")
    return result


def _safe_request_id(value: Any) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,159}", value):
        raise C11EProductionServiceError("request_id must be a safe single path segment")
    if value in {".", ".."} or ".." in value or "/" in value or "\\" in value:
        raise C11EProductionServiceError("request_id may not contain traversal segments")
    return value


def _file_identity(root: Path, relative: str) -> dict[str, Any]:
    rel = PurePosixPath(relative)
    if rel.is_absolute() or ".." in rel.parts or "\\" in relative:
        raise C11EProductionServiceError(f"Unsafe source identity path: {relative}")
    path = root.joinpath(*rel.parts)
    try:
        resolved = path.resolve(strict=True)
        resolved.relative_to(root)
    except Exception as exc:
        raise C11EProductionServiceError(f"Source identity path is missing or escapes project root: {relative}") from exc
    if not resolved.is_file() or path.is_symlink():
        raise C11EProductionServiceError(f"Source identity is not a regular file: {relative}")
    data = resolved.read_bytes()
    return {"path": relative, "bytes": len(data), "sha256": _sha256_bytes(data)}


def _load_d9_resolver(root: Path):
    module_dir = root / "tools" / "c11d" / "d9"
    module_path = module_dir / "universal_producer.py"
    if str(module_dir) not in sys.path:
        sys.path.insert(0, str(module_dir))
    key = "c11e_d9_universal_producer_shared"
    module = sys.modules.get(key)
    if module is not None:
        return module
    spec = importlib.util.spec_from_file_location(key, module_path)
    if spec is None or spec.loader is None:
        raise C11EProductionServiceError(f"Cannot load canonical D9.9 resolver: {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[key] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(key, None)
        raise
    return module


def _source_identity(root: Path, canonical_request: Mapping[str, Any]) -> dict[str, Any]:
    manifest_path = root / "release" / "C11C_FREEZE_PACKAGE_MANIFEST.json"
    if not manifest_path.is_file():
        raise C11EProductionServiceError("Frozen C11-C manifest is missing")
    manifest_bytes = manifest_path.read_bytes()
    manifest_sha = _sha256_bytes(manifest_bytes)
    if len(manifest_bytes) != EXPECTED_C11C_MANIFEST_BYTES or manifest_sha != EXPECTED_C11C_MANIFEST_SHA256:
        raise C11EProductionServiceError("Frozen C11-C manifest identity mismatch")
    try:
        manifest = json.loads(manifest_bytes.decode("utf-8-sig"))
    except Exception as exc:
        raise C11EProductionServiceError(f"Frozen C11-C manifest is invalid JSON: {exc}") from exc
    manifest_entries = {
        str(row.get("path", "")).replace("\\", "/"): row
        for row in manifest.get("source_files", [])
        if isinstance(row, dict)
    }

    pins: list[dict[str, Any]] = []
    for relative, expected_sha in EXPECTED_D9_SOURCE_PINS.items():
        identity = _file_identity(root, relative)
        if identity["sha256"] != expected_sha:
            raise C11EProductionServiceError(f"Reviewed D9 source pin drift: {relative}")
        pins.append(identity)

    model_paths = (
        "definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json",
        "definitions/c11d/production/C11D_UNIVERSAL_PRODUCER_REQUEST_D9_9_V1.json",
        "profiles/delivery/c11c_video_delivery_profiles.json",
        # D9.9 derives Loop/Drill selector identity from the active Producer schema.
        # This schema is a D integration file, so record its live digest rather
        # than incorrectly requiring equality with its historical C11-C preimage.
        "c11c-suite/c11c-producer/producer_schema.json",
    )
    for relative in model_paths:
        pins.append(_file_identity(root, relative))

    selection = canonical_request["selection"]
    if selection["content_type"] == "challenges":
        challenge_id = str(selection["variant_id"])
        relative = f"challenges/{challenge_id}.json"
        identity = _file_identity(root, relative)
        manifest_row = manifest_entries.get(relative)
        if not isinstance(manifest_row, dict):
            raise C11EProductionServiceError(f"Selected Challenge is not present in frozen C11-C manifest: {relative}")
        if identity["bytes"] != manifest_row.get("bytes") or identity["sha256"] != manifest_row.get("sha256"):
            raise C11EProductionServiceError(f"Selected Challenge differs from frozen C11-C source: {relative}")
        pins.append(identity)

    return {
        "c11c_manifest": {
            "path": "release/C11C_FREEZE_PACKAGE_MANIFEST.json",
            "bytes": len(manifest_bytes),
            "sha256": manifest_sha,
            "disposition": "IMMUTABLE_REFERENCE_ONLY",
        },
        "source_pins": pins,
    }


def _assert_resolver_result(result: Mapping[str, Any], resolver: Any) -> None:
    if result.get("status") != "PLANNED":
        raise C11EProductionServiceError("D9.9 must return status PLANNED")
    canonical_request = result.get("canonical_request")
    plan = result.get("plan")
    if not isinstance(canonical_request, Mapping) or not isinstance(plan, Mapping):
        raise C11EProductionServiceError("D9.9 canonical request or plan is missing")
    if resolver.sha256(canonical_request) != result.get("request_hash"):
        raise C11EProductionServiceError("D9.9 request hash mismatch")
    expected_editorial_hash = resolver.sha256({
        "selection": canonical_request.get("selection"),
        "editorial": canonical_request.get("editorial"),
    })
    if expected_editorial_hash != result.get("editorial_hash"):
        raise C11EProductionServiceError("D9.9 editorial hash mismatch")
    if resolver.sha256(plan) != result.get("plan_hash"):
        raise C11EProductionServiceError("D9.9 plan hash mismatch")
    if plan.get("request_hash") != result.get("request_hash") or plan.get("editorial_hash") != result.get("editorial_hash"):
        raise C11EProductionServiceError("D9.9 plan references different request/editorial identity")
    if plan.get("seed") != canonical_request.get("seed") or plan.get("music_seed") != canonical_request.get("music_seed"):
        raise C11EProductionServiceError("D9.9 plan seed domains diverge from canonical request")
    if plan.get("renderer_activation") is not False or plan.get("production_execution") is not False:
        raise C11EProductionServiceError("D9.9 plan crossed its preparation-only boundary")
    if plan.get("runtime_authority") != "NONE" or plan.get("release_authority") != "NONE" or plan.get("d4_8") != "BLOCKED":
        raise C11EProductionServiceError("D9.9 plan governance identity is not fail-closed")
    if result.get("renderer") is not False or result.get("execution") is not False or result.get("release_authority") != "NONE":
        raise C11EProductionServiceError("D9.9 result crossed its execution boundary")
    selection = canonical_request.get("selection", {})
    if selection.get("content_type") not in SUPPORTED_CONTENT_TYPES:
        raise C11EProductionServiceError("C11-E E1 supports only Challenge, Visual Loop and Visual Drill requests")


def prepare_c11e_production_intent(
    raw_request: Mapping[str, Any],
    project_root: Path | str | None = None,
    *,
    request_origin: str | None = None,
    resolver_module: Any | None = None,
) -> dict[str, Any]:
    """Resolve one GUI/CLI request into the same sealed E1 intent; never dispatches."""
    root = _root(project_root)
    if not isinstance(raw_request, Mapping):
        raise C11EProductionServiceError("C11-E request must be a JSON object")
    request = copy.deepcopy(dict(raw_request))
    provenance = request.get("provenance")
    if not isinstance(provenance, Mapping):
        provenance = {}
    else:
        provenance = dict(provenance)
    if request_origin is not None:
        provenance["request_origin"] = request_origin
    origin = provenance.get("request_origin", "UNKNOWN")
    if origin not in ALLOWED_ORIGINS:
        raise C11EProductionServiceError("request_origin must be GUI, CLI, API, TEST or UNKNOWN")
    request["provenance"] = provenance

    resolver = resolver_module or _load_d9_resolver(root)
    try:
        resolved = resolver.evaluate_universal_request(request, root)
    except Exception as exc:
        raise C11EProductionServiceError(f"Canonical D9.9 request resolution failed: {exc}") from exc
    _assert_resolver_result(resolved, resolver)

    canonical_request = resolved["canonical_request"]
    request_id = _safe_request_id(canonical_request.get("request_id"))
    content_type = str(canonical_request["selection"]["content_type"])
    editorial = dict(canonical_request.get("editorial", {}))
    source_identity = _source_identity(root, canonical_request)
    output_root = f"artifacts/production/c11e/{request_id}"
    output_path = root / Path(*PurePosixPath(output_root).parts)
    output_root_exists = output_path.exists()
    if output_root_exists:
        raise C11EProductionServiceError(
            f"Output root already exists and overwrite is forbidden: {output_root}"
        )

    field_consumption = {
        field: {
            "resolved": True,
            "consumer_status": "NOT_CONSUMED_E1",
            "required_gate": "E2" if content_type == "challenges" else "E4",
        }
        for field in editorial
    }
    adapter_gate = "E2" if content_type == "challenges" else "E4"
    intent_semantics = {
        "request_id": request_id,
        "mode": canonical_request["mode"],
        "selection": canonical_request["selection"],
        "request_hash": resolved["request_hash"],
        "editorial_hash": resolved["editorial_hash"],
        "plan_hash": resolved["plan_hash"],
        "gameplay_seed": canonical_request["seed"],
        "music_seed": canonical_request["music_seed"],
        "delivery_profile_id": canonical_request["resolved_delivery_profile_id"],
        "presentation_profile_id": canonical_request["presentation_profile_id"],
        "audio_enabled": canonical_request["audio_enabled"],
        "editorial": editorial,
        "source_identity": source_identity,
        "output_root": output_root,
    }
    intent: dict[str, Any] = {
        "schema": SERVICE_SCHEMA,
        "schema_version": "1.0",
        "service_version": SERVICE_VERSION,
        "status": "PREPARED_E1_NOT_DISPATCHED",
        "request_origin": origin,
        "request": {
            "request_id": request_id,
            "mode": canonical_request["mode"],
            "content_type": content_type,
            "selection": canonical_request["selection"],
        },
        "identity": {
            "request_hash": resolved["request_hash"],
            "editorial_hash": resolved["editorial_hash"],
            "plan_hash": resolved["plan_hash"],
            "intent_hash": sha256(intent_semantics),
        },
        "seed_domains": {
            "gameplay": {"field": "request.seed", "value": canonical_request["seed"]},
            "music": {"field": "request.music_seed", "value": canonical_request["music_seed"]},
            "independent_domains": True,
            "cross_domain_sharing": "FORBIDDEN",
            "automatic_generation": False,
            "runtime_derivation": False,
        },
        "delivery": {
            "requested_profile_id": canonical_request["delivery_profile_id"],
            "resolved_profile_id": canonical_request["resolved_delivery_profile_id"],
            "presentation_profile_id": canonical_request["presentation_profile_id"],
            "audio_enabled": canonical_request["audio_enabled"],
        },
        "editorial": editorial,
        "editorial_field_consumption": field_consumption,
        "family_adapter": {
            "adapter_id": f"c11e_{content_type}_adapter",
            "status": "NOT_CONNECTED_E1",
            "target_gate": adapter_gate,
            "renderer_input_emitted": False,
        },
        "source_identity": source_identity,
        "output": {
            "planned_root": output_root,
            "planned_root_exists": output_root_exists,
            "overwrite_policy": "DENY_EXISTING",
            "created": False,
        },
        "execution_boundary": {
            "dispatch_authorized": False,
            "renderer_input_emitted": False,
            "renderer_dispatch_invoked": False,
            "renderer_activation": False,
            "production_execution": False,
            "media_created": False,
            "d4_8": "BLOCKED",
            "release_authority": "NONE",
        },
    }
    intent["intent_sha256"] = sha256(intent)
    return {"intent": intent, "resolver_result": resolved}


def validate_c11e_production_intent(
    intent: Mapping[str, Any],
    project_root: Path | str | None = None,
) -> dict[str, Any]:
    """Validate self-seal, D9 hashes, seed separation, source pins and fail-closed flags."""
    root = _root(project_root)
    if not isinstance(intent, Mapping) or intent.get("schema") != SERVICE_SCHEMA or intent.get("schema_version") != "1.0":
        raise C11EProductionServiceError("C11-E intent schema mismatch")
    supplied = intent.get("intent_sha256")
    unsigned = dict(intent)
    unsigned.pop("intent_sha256", None)
    if not isinstance(supplied, str) or sha256(unsigned) != supplied:
        raise C11EProductionServiceError("C11-E intent self-hash mismatch")
    if intent.get("status") != "PREPARED_E1_NOT_DISPATCHED":
        raise C11EProductionServiceError("C11-E E1 status must remain preparation-only")
    origin = intent.get("request_origin")
    if origin not in ALLOWED_ORIGINS:
        raise C11EProductionServiceError("Invalid request origin in C11-E intent")
    request = intent.get("request", {})
    request_id = _safe_request_id(request.get("request_id"))
    if request.get("content_type") not in SUPPORTED_CONTENT_TYPES:
        raise C11EProductionServiceError("Unsupported C11-E content type")
    seeds = intent.get("seed_domains", {})
    gameplay = seeds.get("gameplay", {})
    music = seeds.get("music", {})
    if gameplay.get("field") != "request.seed" or music.get("field") != "request.music_seed":
        raise C11EProductionServiceError("Gameplay/music seed field identity mismatch")
    for name, block in (("gameplay", gameplay), ("music", music)):
        value = block.get("value")
        if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= 2147483646:
            raise C11EProductionServiceError(f"Invalid {name} seed value")
    if seeds.get("independent_domains") is not True or seeds.get("cross_domain_sharing") != "FORBIDDEN" or seeds.get("automatic_generation") is not False or seeds.get("runtime_derivation") is not False:
        raise C11EProductionServiceError("Seed governance invariant mismatch")
    boundary = intent.get("execution_boundary", {})
    expected_boundary = {
        "dispatch_authorized": False,
        "renderer_input_emitted": False,
        "renderer_dispatch_invoked": False,
        "renderer_activation": False,
        "production_execution": False,
        "media_created": False,
        "d4_8": "BLOCKED",
        "release_authority": "NONE",
    }
    if boundary != expected_boundary:
        raise C11EProductionServiceError("E1 execution boundary drift")
    output = intent.get("output", {})
    expected_root = f"artifacts/production/c11e/{request_id}"
    if output.get("planned_root") != expected_root or output.get("overwrite_policy") != "DENY_EXISTING" or output.get("created") is not False or output.get("planned_root_exists") is not False:
        raise C11EProductionServiceError("Unsafe E1 output policy")
    if (root / Path(*PurePosixPath(expected_root).parts)).exists():
        raise C11EProductionServiceError("E1 output root appeared after preparation; overwrite is forbidden")
    adapter = intent.get("family_adapter", {})
    expected_gate = "E2" if request.get("content_type") == "challenges" else "E4"
    if adapter.get("status") != "NOT_CONNECTED_E1" or adapter.get("target_gate") != expected_gate or adapter.get("renderer_input_emitted") is not False:
        raise C11EProductionServiceError("Family adapter must remain unconnected in E1")
    identity = intent.get("identity", {})
    for field in ("request_hash", "editorial_hash", "plan_hash", "intent_hash"):
        value = identity.get(field)
        if not isinstance(value, str) or not re.fullmatch(r"[a-f0-9]{64}", value):
            raise C11EProductionServiceError(f"Malformed C11-E identity hash: {field}")
    source_identity = intent.get("source_identity", {})
    manifest = _file_identity(root, "release/C11C_FREEZE_PACKAGE_MANIFEST.json")
    if manifest["bytes"] != EXPECTED_C11C_MANIFEST_BYTES or manifest["sha256"] != EXPECTED_C11C_MANIFEST_SHA256:
        raise C11EProductionServiceError("Frozen C11-C manifest identity mismatch during intent validation")
    if source_identity.get("c11c_manifest", {}).get("sha256") != EXPECTED_C11C_MANIFEST_SHA256:
        raise C11EProductionServiceError("C11-E intent references a different C11-C manifest")
    for path, expected in EXPECTED_D9_SOURCE_PINS.items():
        current = _file_identity(root, path)
        if current["sha256"] != expected:
            raise C11EProductionServiceError(f"Reviewed D9 source pin drift: {path}")
    pinned = source_identity.get("source_pins")
    if not isinstance(pinned, list):
        raise C11EProductionServiceError("C11-E source pin list is malformed")
    for row in pinned:
        if not isinstance(row, Mapping) or set(row) != {"path", "bytes", "sha256"}:
            raise C11EProductionServiceError("Malformed C11-E source pin row")
        current = _file_identity(root, str(row["path"]))
        if current != dict(row):
            raise C11EProductionServiceError(f"C11-E source pin has drifted: {row['path']}")
    return {"valid": True, "status": "PASS_E1_PREPARATION_ONLY", "intent_sha256": supplied, "source_pin_count": len(pinned), "renderer": False, "media_created": False}
