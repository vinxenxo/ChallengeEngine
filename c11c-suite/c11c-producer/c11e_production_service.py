"""C11-E shared GUI/CLI production-intent service.

E1 is deliberately preparation-only and is the single entry point for GUI and
CLI requests. It delegates request semantics to the accepted D9.9 resolver.
For Visual Loop requests it also prepares the existing D9.10 bridge, D-only
adapter envelope and family-stage contract, then seals them into the E intent.
It never dispatches a C runner, invokes Godot/FFmpeg, emits renderer-native
input, or creates audio/video media.
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
SERVICE_VERSION = "0.3.0-E4B"
EXPECTED_C11C_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
EXPECTED_C11C_MANIFEST_BYTES = 796318
SUPPORTED_CONTENT_TYPES = ("challenges", "visual_loops", "visual_drills")
ALLOWED_ORIGINS = {"GUI", "CLI", "API", "TEST", "UNKNOWN"}

# These three implementations were captured from the active checkout during the
# E0/E1 review. A changed resolver is a new E1 source set and must be reviewed.
EXPECTED_D9_SOURCE_PINS = {
    "tools/c11d/d9/universal_producer.py": "9ad2adbf54946f2225ae2ed36b88abfc5717387f2ff03bbed684aa8bd32d87d1",
    "tools/c11d/d9/universal_editorial_model.py": "dac95fb698b52f96432a517d8ec3196a397e5e6bd3c025300350dd55ddce3afd",
    "c11c-suite/c11c-producer/c11d_gui_request.py": "0e95109ffd3ba5655d28292309196349470ab7958a467f096543a2c98c22976e",
}

MUSIC_CONTRACT_PATH = "definitions/c11e/music/C11E_E3_2_D3_V5_E1_MUSIC_CONTRACT_V1.json"
EXPECTED_MUSIC_SOURCE_PINS = {
    "tools/c11d/d3/c11d_music_engine_v5.py": "03ae7e2997796e0c67ca15c8886b1e5b290791a142b6631a572d1cba6eba4eb1",
    "definitions/c11d/music/C11D_MUSIC_ENGINE_V5_SPEC_V1.json": "8970f4e93c878285b727697f3d269f5ee464b6029fe79eabc5fcbf4245e9dbf2",
    "definitions/c11d/music/C11D_CHALLENGE_8BIT_STYLE_PROFILE_V1.json": "0c877cbe6e1c288890da31fc4481a58e1051749b45a50b2290cbef5d1120d2de",
    MUSIC_CONTRACT_PATH: "12c59ce2a2135a49ce0d5968a29905a1e5890743507db1ee0039da1374efcfe8",
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


def _load_d9_boundary_module(root: Path, module_name: str):
    """Load one reviewed D9 boundary module by its canonical project path."""
    module_dir = root / "tools" / "c11d" / "d9"
    module_path = module_dir / f"{module_name}.py"
    if str(module_dir) not in sys.path:
        sys.path.insert(0, str(module_dir))
    module = sys.modules.get(module_name)
    if module is not None:
        return module
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise C11EProductionServiceError(f"Cannot load reviewed D9 boundary module: {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(module_name, None)
        raise
    return module


LOOP_OPERATOR_DECISION_REL = "docs/current/e/C11E_E4B_OPERATOR_POLICY_DECISION_RECORD_20261106_V1.json"
LOOP_APPROVED_PROPOSALS = {
    "A.1_SHARED_PRESENTATION_REGIONS": ("definitions/c11d/production/D_RENDERER_UNIFIED_PRESENTATION_REGION_POLICY_PROPOSAL_V1.json", "101092bb32127bb8854a501a9215c0b6cf69581594383903716907d49719c01a"),
    "A.3_LOOP_DRILL_EDITORIAL_WINDOWS": ("definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json", "609a4d183aac07c2cbe1abaf41444160fdd137217faffbead3aef618320d57dc"),
    "E4B_LOOP_COMPOSITION": ("definitions/c11d/production/C11E_E4B_LOOP_EDITORIAL_COMPOSITION_PROPOSAL_V1.json", "9e206704665ea85226ecc10854be9f679c32fe9ed7efb690a829f6e8456d43da"),
    "B.1_UNIFIED_DELIVERY_TIMEBASE": ("definitions/c11d/production/D_RENDERER_UNIFIED_DELIVERY_TIMEBASE_POLICY_PROPOSAL_V1.json", "41a62b0766db47cd99772f28642ef67766314f20f0f7891789d6b7497bbfee85"),
    "D.1_AUDIO_MUSIC_DELIVERY_ENVELOPE": ("definitions/c11d/production/D_RENDERER_UNIFIED_AUDIO_MUSIC_DELIVERY_POLICY_PROPOSAL_V1.json", "3dd4874e1b6506de6d9ddbe6ad1b567a284b94cc00ef1bac0d35d1731af05e23"),
}


def _assert_loop_operator_approvals(root: Path) -> dict[str, Any]:
    """Require the exact five approved current-hash decisions and their scope locks."""
    path = root / LOOP_OPERATOR_DECISION_REL
    try:
        record = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise C11EProductionServiceError(f"E4B operator decision record is unavailable: {exc}") from exc
    if record.get("schema") != "C11E-E4B-OPERATOR-POLICY-DECISION-RECORD-V1":
        raise C11EProductionServiceError("E4B operator decision record schema mismatch")
    rows = record.get("decisions")
    if not isinstance(rows, list) or len(rows) != 5:
        raise C11EProductionServiceError("E4B requires exactly five recorded operator approvals")
    by_id = {row.get("decision_id"): row for row in rows if isinstance(row, Mapping)}
    if set(by_id) != set(LOOP_APPROVED_PROPOSALS):
        raise C11EProductionServiceError("E4B operator decision set mismatch")
    for decision_id, (proposal_path, proposal_sha) in LOOP_APPROVED_PROPOSALS.items():
        row = by_id[decision_id]
        if row.get("proposal_path") != proposal_path or row.get("proposal_sha256") != proposal_sha or row.get("decision") != "APPROVE_AS_PROPOSED":
            raise C11EProductionServiceError(f"E4B decision is missing/current-hash mismatch: {decision_id}")
        identity = _file_identity(root, proposal_path)
        if identity["sha256"] != proposal_sha:
            raise C11EProductionServiceError(f"E4B approved proposal changed after operator decision: {decision_id}")
    scope = record.get("scope_boundary", {})
    required = {
        "d_only_design_and_contract_implementation_authorized": True,
        "renderer_native_input_emission_authorized": False,
        "renderer_activation_authorized": False,
        "production_dispatch_authorized": False,
        "media_creation_authorized": False,
        "audio_asset_selection_authorized": False,
        "audio_generation_authorized": False,
        "audio_payload_materialization_authorized": False,
        "release_promotion_authorized": False,
        "d4_8": "BLOCKED",
        "d9_10": "PREPARE_ONLY",
        "d9_14": "BLOCKED",
        "d9_16": "BLOCKED",
        "d9_17": "BLOCKED_NO_GO",
        "d10": "BLOCKED_FOR_PROMOTION",
        "release_authority": "NONE",
    }
    if any(scope.get(key) != value for key, value in required.items()):
        raise C11EProductionServiceError("E4B operator approval scope boundary is not fail-closed")
    if record.get("policy_proposal_files_mutated") is not False or record.get("historical_packet_v1_mutated") is not False:
        raise C11EProductionServiceError("E4B policy proposal immutability record mismatch")
    if record.get("c11c_frozen_baseline_sha256") != EXPECTED_C11C_MANIFEST_SHA256:
        raise C11EProductionServiceError("E4B decision record references another C11-C baseline")
    return record


def _prepare_loop_family_boundary(root: Path, resolved: Mapping[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Prepare the approved D9.9→D9.10→Loop family contract once in the shared E service."""
    _assert_loop_operator_approvals(root)
    bridge_module = _load_d9_boundary_module(root, "editorial_render_bridge")
    adapter_module = _load_d9_boundary_module(root, "d_render_adapter")
    family_module = _load_d9_boundary_module(root, "c11e_e4b_loop_family_stage_contract")
    bridge = bridge_module.build_bridge_planning_record(resolved, root)
    adapter = adapter_module.prepare_d_only_adapter_envelope(resolved, bridge, root)
    family_contract = family_module.build_loop_family_stage_contract(resolved, bridge, root)
    if not family_module.validate_loop_family_stage_contract(family_contract):
        raise C11EProductionServiceError("E4B Loop family-stage contract self-validation failed")
    if family_contract.get("request_identity", {}).get("d_only_adapter_envelope_hash") != adapter.get("envelope_hash"):
        raise C11EProductionServiceError("E4B Loop family-stage contract is not bound to the shared D-only envelope")
    if family_contract.get("request_identity", {}).get("bridge_record_hash") != bridge.get("record_hash"):
        raise C11EProductionServiceError("E4B Loop family-stage contract is not bound to the D9.10 bridge record")
    if family_contract.get("governance", {}).get("renderer_native_input_emitted") is not False:
        raise C11EProductionServiceError("E4B Loop family-stage contract crossed renderer-input boundary")

    selection = resolved.get("canonical_request", {}).get("selection", {})
    schema = json.loads((root / "c11c-suite" / "c11c-producer" / "producer_schema.json").read_text(encoding="utf-8-sig"))
    family = schema.get("families", {}).get(selection.get("family_id"), {})
    launcher = family.get("prototype")
    if not isinstance(launcher, str):
        raise C11EProductionServiceError("E4B Loop selected family has no canonical launcher")
    source_paths = [
        "tools/c11d/d9/editorial_render_bridge.py",
        "tools/c11d/d9/d_render_adapter.py",
        "tools/c11d/d9/c11e_e4b_loop_family_stage_contract.py",
        "definitions/c11d/production/C11D_EDITORIAL_RENDER_BRIDGE_D9_10_V1.json",
        "definitions/c11d/production/C11D_RENDER_ADAPTER_BOUNDARY_D9_10_V1.json",
        "profiles/presentation/c11c_visual_music_profiles.json",
        LOOP_OPERATOR_DECISION_REL,
        launcher.replace("\\", "/"),
    ] + [value[0] for value in LOOP_APPROVED_PROPOSALS.values()]
    extra_pins = []
    seen = set()
    for relative in source_paths:
        normalized = relative.replace("\\", "/")
        if normalized in seen:
            continue
        seen.add(normalized)
        extra_pins.append(_file_identity(root, normalized))

    preparation = {
        "schema": "C11E-E4B-SHARED-LOOP-BOUNDARY-PREPARATION-V1",
        "status": "LOOP_FAMILY_STAGE_PREPARED_NOT_DISPATCHABLE",
        "bridge_planning_record": bridge,
        "d_only_adapter_envelope": adapter,
        "loop_family_stage_contract": family_contract,
        "required_source_pin_paths": sorted(seen),
        "renderer_input_emitted": False,
        "renderer_dispatch_invoked": False,
        "launcher_invoked": False,
        "media_created": False,
        "release_authority": "NONE",
    }
    preparation["preparation_sha256"] = sha256(preparation)
    return preparation, extra_pins


def _build_music_contract(root: Path, canonical_request: Mapping[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Resolve a sealed, non-dispatchable music binding; never imports or calls V5."""
    selection = canonical_request["selection"]
    content_type = str(selection["content_type"])
    audio_enabled = canonical_request["audio_enabled"]
    music_seed = canonical_request["music_seed"]
    variation_index = canonical_request["variation_index"]
    if content_type != "challenges":
        # Do not even read or pin Challenge V5 sources for protected Loop/Drill requests.
        protected_binding = {
            "contract_id": "C11E_E3_2_D3_V5_E1_MUSIC_CONTRACT_V1",
            "contract_version": "1.0",
            "contract_path": None,
            "contract_sha256": None,
            "status": "PROTECTED_FAMILY_NOT_REWIRED",
            "route": "PRESERVE_EXISTING_C11C_FAMILY_MUSIC_PATH",
            "audio_enabled": audio_enabled,
            "music_seed_field": "request.music_seed",
            "music_seed": music_seed,
            "variation_index": variation_index,
            "engine": None,
            "style_profile": None,
            "engine_request": None,
            "unresolved_engine_parameters": [],
            "dispatchable": False,
            "dispatch_authorized": False,
            "engine_invoked": False,
            "audio_created": False,
            "renderer_invoked": False,
            "ffmpeg_mux_invoked": False,
            "release_authority": "NONE",
        }
        return protected_binding, []

    identities: dict[str, dict[str, Any]] = {}
    for relative, expected_sha in EXPECTED_MUSIC_SOURCE_PINS.items():
        identity = _file_identity(root, relative)
        if identity["sha256"] != expected_sha:
            raise C11EProductionServiceError(f"Reviewed D3 V5 music source pin drift: {relative}")
        identities[relative] = identity

    def read_json(relative: str) -> dict[str, Any]:
        try:
            value = json.loads((root / Path(*PurePosixPath(relative).parts)).read_text(encoding="utf-8-sig"))
        except Exception as exc:
            raise C11EProductionServiceError(f"Invalid D3 V5 music contract JSON: {relative}: {exc}") from exc
        if not isinstance(value, dict):
            raise C11EProductionServiceError(f"D3 V5 music contract source must be a JSON object: {relative}")
        return value

    contract = read_json(MUSIC_CONTRACT_PATH)
    spec = read_json("definitions/c11d/music/C11D_MUSIC_ENGINE_V5_SPEC_V1.json")
    profile = read_json("definitions/c11d/music/C11D_CHALLENGE_8BIT_STYLE_PROFILE_V1.json")
    engine_id = str(contract.get("engine", {}).get("engine_id", ""))
    engine_version = str(contract.get("engine", {}).get("engine_version", ""))
    profile_id = str(profile.get("style_profile_id", profile.get("profile_id", "")))
    profile_version = str(profile.get("style_profile_version", profile.get("profile_version", "")))
    if contract.get("schema") != "C11E-E3.2-D3-V5-E1-MUSIC-CONTRACT" or contract.get("contract_version") != "1.0":
        raise C11EProductionServiceError("Unsupported C11-E E3.2 music contract identity")
    if spec.get("engine_id") != engine_id or str(spec.get("engine_version")) != engine_version:
        raise C11EProductionServiceError("D3 V5 engine specification identity mismatch")
    if profile_id != contract.get("style_profile", {}).get("canonical_id") or profile_version != contract.get("style_profile", {}).get("canonical_version"):
        raise C11EProductionServiceError("D3 V5 style profile identity mismatch")
    if profile.get("engine_id") != engine_id or str(profile.get("engine_version")) != engine_version:
        raise C11EProductionServiceError("D3 V5 style profile references a different engine")

    selection = canonical_request["selection"]
    content_type = str(selection["content_type"])
    audio_enabled = canonical_request["audio_enabled"]
    music_seed = canonical_request["music_seed"]
    variation_index = canonical_request["variation_index"]
    if content_type == "challenges":
        route = "D3_V5_CHALLENGE_8BIT_PLANNING_BINDING_ONLY"
        status = "PLANNED_NOT_RENDERED" if audio_enabled else "DISABLED_BY_REQUEST"
        engine = {
            "engine_id": engine_id,
            "engine_version": engine_version,
            "source_path": contract["engine"]["path"],
            "source_sha256": identities[contract["engine"]["path"]]["sha256"],
            "spec_path": contract["engine"]["spec_path"],
            "spec_sha256": identities[contract["engine"]["spec_path"]]["sha256"],
        }
        style_profile = {
            "profile_id": profile_id,
            "profile_version": profile_version,
            "source_path": contract["style_profile"]["path"],
            "source_sha256": identities[contract["style_profile"]["path"]]["sha256"],
        }
        engine_request = None if not audio_enabled else {
            "music_seed": music_seed,
            "style_profile_id": profile_id,
            "style_profile_version": profile_version,
            "variation_index": variation_index,
            "tempo_bpm": None,
            "duration_seconds": None,
        }
        unresolved = ["tempo_bpm", "duration_seconds"] if audio_enabled else []
    else:
        route = "PRESERVE_EXISTING_C11C_FAMILY_MUSIC_PATH"
        status = "PROTECTED_FAMILY_NOT_REWIRED"
        engine = None
        style_profile = None
        engine_request = None
        unresolved = []

    binding = {
        "contract_id": contract["contract_id"],
        "contract_version": contract["contract_version"],
        "contract_path": MUSIC_CONTRACT_PATH,
        "contract_sha256": identities[MUSIC_CONTRACT_PATH]["sha256"],
        "status": status,
        "route": route,
        "audio_enabled": audio_enabled,
        "music_seed_field": "request.music_seed",
        "music_seed": music_seed,
        "variation_index": variation_index,
        "engine": engine,
        "style_profile": style_profile,
        "engine_request": engine_request,
        "unresolved_engine_parameters": unresolved,
        "dispatchable": False,
        "dispatch_authorized": False,
        "engine_invoked": False,
        "audio_created": False,
        "renderer_invoked": False,
        "ffmpeg_mux_invoked": False,
        "release_authority": "NONE",
    }
    return binding, list(identities.values())


def _source_identity(
    root: Path,
    canonical_request: Mapping[str, Any],
    extra_pins: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
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

    seen_pin_paths = {row["path"] for row in pins}
    for row in extra_pins or []:
        if row["path"] not in seen_pin_paths:
            pins.append(row)
            seen_pin_paths.add(row["path"])
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
    # E4A.1: presentation visibility is an E1 request option, not a D9.9
    # canonical field. Remove it before invoking the strict D9.9 resolver.
    option_supplied = "presentation_options" in request
    raw_presentation_options = request.pop("presentation_options", None)
    raw_selection = request.get("selection")
    raw_content_type = raw_selection.get("content_type") if isinstance(raw_selection, Mapping) else None
    if raw_content_type == "challenges":
        if not option_supplied:
            presentation_options: dict[str, Any] | None = {"show_hook_countdown": True}
        elif (
            not isinstance(raw_presentation_options, Mapping)
            or set(raw_presentation_options) != {"show_hook_countdown"}
            or type(raw_presentation_options.get("show_hook_countdown")) is not bool
        ):
            raise C11EProductionServiceError(
                "Challenge presentation_options must contain only boolean show_hook_countdown"
            )
        else:
            presentation_options = {
                "show_hook_countdown": raw_presentation_options["show_hook_countdown"]
            }
    else:
        if option_supplied:
            raise C11EProductionServiceError(
                "presentation_options.show_hook_countdown is Challenge-only"
            )
        presentation_options = None
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
    music_contract, music_source_pins = _build_music_contract(root, canonical_request)
    loop_boundary_preparation = None
    loop_boundary_source_pins: list[dict[str, Any]] = []
    if content_type == "visual_loops":
        loop_boundary_preparation, loop_boundary_source_pins = _prepare_loop_family_boundary(root, resolved)
    source_identity = _source_identity(root, canonical_request, music_source_pins + loop_boundary_source_pins)
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
        "music_contract": music_contract,
        "source_identity": source_identity,
        "output_root": output_root,
    }
    if content_type == "challenges":
        intent_semantics["presentation_options"] = presentation_options
    if loop_boundary_preparation is not None:
        intent_semantics["d9_boundary_preparation_identity"] = {
            "preparation_sha256": loop_boundary_preparation["preparation_sha256"],
            "bridge_record_hash": loop_boundary_preparation["bridge_planning_record"]["record_hash"],
            "d_only_adapter_envelope_hash": loop_boundary_preparation["d_only_adapter_envelope"]["envelope_hash"],
            "loop_family_stage_contract_sha256": loop_boundary_preparation["loop_family_stage_contract"]["contract_sha256"],
        }
    intent_request = {
        "request_id": request_id,
        "mode": canonical_request["mode"],
        "content_type": content_type,
        "selection": canonical_request["selection"],
        "variation_index": canonical_request["variation_index"],
    }
    if content_type == "challenges":
        intent_request["presentation_options"] = presentation_options
    intent: dict[str, Any] = {
        "schema": SERVICE_SCHEMA,
        "schema_version": "1.2" if loop_boundary_preparation is not None else "1.1",
        "service_version": SERVICE_VERSION,
        "status": "PREPARED_E1_NOT_DISPATCHED",
        "request_origin": origin,
        "request": intent_request,
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
        "music_contract": music_contract,
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
    if loop_boundary_preparation is not None:
        intent["d9_boundary_preparation"] = loop_boundary_preparation
    intent["intent_sha256"] = sha256(intent)
    return {"intent": intent, "resolver_result": resolved}


def validate_c11e_production_intent(
    intent: Mapping[str, Any],
    project_root: Path | str | None = None,
) -> dict[str, Any]:
    """Validate self-seal, D9 hashes, seed separation, source pins and fail-closed flags."""
    root = _root(project_root)
    if not isinstance(intent, Mapping) or intent.get("schema") != SERVICE_SCHEMA or intent.get("schema_version") not in {"1.1", "1.2"}:
        raise C11EProductionServiceError("C11-E intent schema mismatch")
    supplied = intent.get("intent_sha256")
    unsigned = dict(intent)
    unsigned.pop("intent_sha256", None)
    if not isinstance(supplied, str) or sha256(unsigned) != supplied:
        raise C11EProductionServiceError("C11-E intent self-hash mismatch")
    if intent.get("service_version") != SERVICE_VERSION:
        raise C11EProductionServiceError("C11-E service version mismatch")
    if intent.get("status") != "PREPARED_E1_NOT_DISPATCHED":
        raise C11EProductionServiceError("C11-E E1 status must remain preparation-only")
    origin = intent.get("request_origin")
    if origin not in ALLOWED_ORIGINS:
        raise C11EProductionServiceError("Invalid request origin in C11-E intent")
    request = intent.get("request", {})
    request_id = _safe_request_id(request.get("request_id"))
    if request.get("content_type") not in SUPPORTED_CONTENT_TYPES:
        raise C11EProductionServiceError("Unsupported C11-E content type")
    content_type = request.get("content_type")
    expected_schema_version = "1.2" if content_type == "visual_loops" else "1.1"
    if intent.get("schema_version") != expected_schema_version:
        raise C11EProductionServiceError("C11-E schema version does not match the family preparation contract")
    options_present = "presentation_options" in request
    presentation_options = request.get("presentation_options")
    if request.get("content_type") == "challenges":
        # Older sealed E1 intents predate the optional visibility flag. They
        # remain valid and retain the historical default (visible). New intents
        # carry the explicit boolean and seal it into intent_hash.
        if options_present and (
            not isinstance(presentation_options, Mapping)
            or set(presentation_options) != {"show_hook_countdown"}
            or type(presentation_options.get("show_hook_countdown")) is not bool
        ):
            raise C11EProductionServiceError("Invalid sealed Challenge presentation_options")
    elif options_present:
        raise C11EProductionServiceError("Non-Challenge E1 request contains Challenge presentation_options")
    variation_index = request.get("variation_index")
    if isinstance(variation_index, bool) or not isinstance(variation_index, int) or not 0 <= variation_index <= 1000000:
        raise C11EProductionServiceError("Invalid C11-E variation_index")
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
    delivery = intent.get("delivery", {})
    if not isinstance(delivery.get("audio_enabled"), bool):
        raise C11EProductionServiceError("Invalid E1 audio_enabled flag")
    music_request = {
        "selection": {"content_type": request.get("content_type")},
        "music_seed": music.get("value"),
        "variation_index": request.get("variation_index"),
        "audio_enabled": delivery.get("audio_enabled"),
    }
    expected_music, expected_music_pins = _build_music_contract(root, music_request)
    if intent.get("music_contract") != expected_music:
        raise C11EProductionServiceError("C11-E music contract binding mismatch")
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
    expected_gate = "E2" if content_type == "challenges" else "E4"
    if adapter.get("target_gate") != expected_gate or adapter.get("renderer_input_emitted") is not False:
        raise C11EProductionServiceError("Family adapter boundary identity mismatch")
    loop_preparation_identity = None
    if content_type == "visual_loops":
        preparation = intent.get("d9_boundary_preparation")
        if not isinstance(preparation, Mapping) or preparation.get("schema") != "C11E-E4B-SHARED-LOOP-BOUNDARY-PREPARATION-V1" or preparation.get("status") != "LOOP_FAMILY_STAGE_PREPARED_NOT_DISPATCHABLE":
            raise C11EProductionServiceError("E4B shared Loop boundary preparation is missing")
        unsigned_preparation = {key: value for key, value in preparation.items() if key != "preparation_sha256"}
        if preparation.get("preparation_sha256") != sha256(unsigned_preparation):
            raise C11EProductionServiceError("E4B shared Loop preparation self-hash mismatch")
        bridge = preparation.get("bridge_planning_record")
        envelope = preparation.get("d_only_adapter_envelope")
        family_stage = preparation.get("loop_family_stage_contract")
        if not all(isinstance(value, Mapping) for value in (bridge, envelope, family_stage)):
            raise C11EProductionServiceError("E4B shared Loop boundary records are incomplete")
        bridge_module = _load_d9_boundary_module(root, "editorial_render_bridge")
        adapter_module = _load_d9_boundary_module(root, "d_render_adapter")
        family_module = _load_d9_boundary_module(root, "c11e_e4b_loop_family_stage_contract")
        if bridge.get("schema") != bridge_module.RECORD_SCHEMA or bridge.get("status") != "PLANNING_ONLY_NOT_RENDERABLE":
            raise C11EProductionServiceError("D9.10 bridge is not planning-only")
        if bridge.get("record_hash") != bridge_module.sha256({key: value for key, value in bridge.items() if key != "record_hash"}):
            raise C11EProductionServiceError("D9.10 bridge record hash mismatch")
        adapter_module.validate_d_only_adapter_envelope(envelope, root)
        family_module.validate_loop_family_stage_contract(family_stage)
        if family_stage.get("request_identity", {}).get("bridge_record_hash") != bridge.get("record_hash") or family_stage.get("request_identity", {}).get("d_only_adapter_envelope_hash") != envelope.get("envelope_hash"):
            raise C11EProductionServiceError("E4B family-stage contract is not bound to D9.10 records")
        if family_stage.get("content_identity", {}).get("family_id") != request.get("selection", {}).get("family_id") or family_stage.get("content_identity", {}).get("grammar_id") != request.get("selection", {}).get("subtype_id"):
            raise C11EProductionServiceError("E4B family-stage contract selector differs from the E1 request")
        if preparation.get("renderer_input_emitted") is not False or preparation.get("renderer_dispatch_invoked") is not False or preparation.get("launcher_invoked") is not False or preparation.get("media_created") is not False or preparation.get("release_authority") != "NONE":
            raise C11EProductionServiceError("E4B shared Loop preparation crossed its execution boundary")
        required_paths = set(preparation.get("required_source_pin_paths", []))
        pinned_paths = {row.get("path") for row in intent.get("source_identity", {}).get("source_pins", []) if isinstance(row, Mapping)}
        if not required_paths or not required_paths.issubset(pinned_paths):
            raise C11EProductionServiceError("E4B shared Loop source-pin coverage is incomplete")
        if adapter.get("status") != "NOT_CONNECTED_E1":
            raise C11EProductionServiceError("E1 family consumer must remain unconnected; D-only preparation is not render consumption")
        loop_preparation_identity = {
            "preparation_sha256": preparation["preparation_sha256"],
            "bridge_record_hash": bridge["record_hash"],
            "d_only_adapter_envelope_hash": envelope["envelope_hash"],
            "loop_family_stage_contract_sha256": family_stage["contract_sha256"],
        }
    else:
        if adapter.get("status") != "NOT_CONNECTED_E1" or "d9_boundary_preparation" in intent:
            raise C11EProductionServiceError("Non-Loop E1 family adapter must remain unconnected")
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
    pin_map = {str(row["path"]): dict(row) for row in pinned}
    for expected_pin in expected_music_pins:
        if pin_map.get(expected_pin["path"]) != expected_pin:
            raise C11EProductionServiceError(f"C11-E music source pin is missing or altered: {expected_pin['path']}")
    editorial = intent.get("editorial", {})
    output_root = output.get("planned_root")
    intent_semantics = {
        "request_id": request_id,
        "mode": request.get("mode"),
        "selection": request.get("selection"),
        "request_hash": identity.get("request_hash"),
        "editorial_hash": identity.get("editorial_hash"),
        "plan_hash": identity.get("plan_hash"),
        "gameplay_seed": gameplay.get("value"),
        "music_seed": music.get("value"),
        "delivery_profile_id": delivery.get("resolved_profile_id"),
        "presentation_profile_id": delivery.get("presentation_profile_id"),
        "audio_enabled": delivery.get("audio_enabled"),
        "editorial": editorial,
        "music_contract": expected_music,
        "source_identity": source_identity,
        "output_root": output_root,
    }
    if options_present:
        intent_semantics["presentation_options"] = presentation_options
    if loop_preparation_identity is not None:
        intent_semantics["d9_boundary_preparation_identity"] = loop_preparation_identity
    if sha256(intent_semantics) != identity.get("intent_hash"):
        raise C11EProductionServiceError("C11-E semantic intent hash mismatch")
    return {"valid": True, "status": "PASS_E1_PREPARATION_ONLY", "intent_sha256": supplied, "source_pin_count": len(pinned), "renderer": False, "media_created": False}
