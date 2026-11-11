"""C11-E shared GUI/CLI production-intent service.

E1 is deliberately preparation-only and is the single entry point for GUI and
CLI requests. It delegates request semantics to the accepted D9.9 resolver.
For Visual Loop requests it prepares the existing D9.10 bridge, D-only adapter
envelope and family-stage contract. Visual Drill uses the same D9.9/D9.10 chain
and the existing D9 dynamic-request binder V2 (4 types × 5 tiers), in a strict
non-rendering preparation preview. Neither path invokes a renderer or media.
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
SERVICE_VERSION = "0.4.0-E4C"
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



def _drill_source_text(root: Path, relative: str) -> str:
    identity = _file_identity(root, relative)
    return (root / Path(*PurePosixPath(relative).parts)).read_text(encoding="utf-8-sig")


A3_LINEAGE_BRIDGE_REL = "docs/current/e/C11E_E4C_A3_REVIEW_MANIFEST_LINEAGE_RECONCILIATION_20261110_V2.json"
A3_LINEAGE_BRIDGE_SHA256 = "aec0e387f167f4b821b7d94f06a67f78f498be939fe3cda857d20ce550819cac"
A3_HISTORICAL_REVIEW_MANIFEST_SHA256 = "2075da9c33c689861a68d3bd8fb19b7ed593c6e76010ab200880746aa6d1a470"
A3_CURRENT_REVIEW_MANIFEST_SHA256 = "5702092bc1c88e4b333dd30cc150f0d383cd2006121037b0198905c75a3af795"
A3_FIELD_WINDOW_PROPOSAL_SHA256 = "609a4d183aac07c2cbe1abaf41444160fdd137217faffbead3aef618320d57dc"
A3_POLICY_DECISION_RECORD_SHA256 = "49efd5494f351f09d7597c4699e9c12e361b36884b6bfadacd822e6ff1480e04"


def _resolve_a3_review_manifest_lineage(
    root: Path, window_proposal: Mapping[str, Any], review_manifest_pin: Mapping[str, Any]
) -> dict[str, Any]:
    """Resolve the immutable A.3 predecessor reference through the attested V2 bridge.

    The A.3 proposal remains byte-identical and still names the historical review-manifest
    preimage. V5 installed the reviewed successor as a single-pointer refresh and archived
    the exact preimage. This function verifies that attestation rather than mutating A.3.
    """
    def read_json(relative: str) -> dict[str, Any]:
        try:
            value = json.loads((root / Path(*PurePosixPath(relative).parts)).read_text(encoding="utf-8-sig"))
        except Exception as exc:
            raise C11EProductionServiceError(f"A.3 lineage bridge JSON invalid: {relative}: {exc}") from exc
        if not isinstance(value, dict):
            raise C11EProductionServiceError(f"A.3 lineage bridge record must be an object: {relative}")
        return value

    bridge_path = root / Path(*PurePosixPath(A3_LINEAGE_BRIDGE_REL).parts)
    bridge_identity = _file_identity(root, A3_LINEAGE_BRIDGE_REL)
    if bridge_identity["sha256"] != A3_LINEAGE_BRIDGE_SHA256:
        raise C11EProductionServiceError("A.3 lineage bridge SHA-256 mismatch")
    bridge = read_json(A3_LINEAGE_BRIDGE_REL)
    if bridge.get("schema") != "C11E-E4C-A3-REVIEW-MANIFEST-LINEAGE-RECONCILIATION-V2" or bridge.get("status") != "ATTESTED_SINGLE_SOURCE_LINEAGE_POINTER_REFRESH_NO_POLICY_CHANGE":
        raise C11EProductionServiceError("A.3 lineage bridge schema/status mismatch")

    proposal_path = "definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json"
    proposal_identity = _file_identity(root, proposal_path)
    if proposal_identity["sha256"] != A3_FIELD_WINDOW_PROPOSAL_SHA256:
        raise C11EProductionServiceError("A.3 field-window proposal is not the approved immutable proposal")
    policy = bridge.get("approved_policy", {})
    a3 = policy.get("a3", {})
    decision_ref = policy.get("a3_decision_record", {})
    if a3.get("path") != proposal_path or a3.get("sha256") != A3_FIELD_WINDOW_PROPOSAL_SHA256 or a3.get("decision") != "APPROVE_AS_PROPOSED":
        raise C11EProductionServiceError("A.3 lineage bridge does not bind the exact approved field-window proposal")
    if decision_ref.get("sha256") != A3_POLICY_DECISION_RECORD_SHA256:
        raise C11EProductionServiceError("A.3 lineage bridge references another operator decision record")
    decision_record = read_json(decision_ref["path"])
    if _file_identity(root, decision_ref["path"])["sha256"] != A3_POLICY_DECISION_RECORD_SHA256:
        raise C11EProductionServiceError("A.3 operator decision record SHA-256 mismatch")
    a3_decisions = {row.get("decision_id"): row for row in decision_record.get("decisions", []) if isinstance(row, Mapping)}
    accepted = a3_decisions.get("A.3_LOOP_DRILL_EDITORIAL_WINDOWS")
    if not isinstance(accepted, Mapping) or accepted.get("decision") != "APPROVE_AS_PROPOSED" or accepted.get("proposal_sha256") != A3_FIELD_WINDOW_PROPOSAL_SHA256:
        raise C11EProductionServiceError("A.3 exact-hash operator approval is missing")

    lineage = bridge.get("review_manifest_lineage", {})
    manifest_rel = "definitions/c11d/production/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1.json"
    archive_rel = "docs/history/c11e/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1_PRE_D98_LINEAGE_REFRESH_20261106.json"
    if lineage.get("path") != manifest_rel or lineage.get("historical_archive_path") != archive_rel:
        raise C11EProductionServiceError("A.3 bridge review-manifest path identity mismatch")
    if lineage.get("historical_sha256") != A3_HISTORICAL_REVIEW_MANIFEST_SHA256 or lineage.get("current_sha256") != A3_CURRENT_REVIEW_MANIFEST_SHA256:
        raise C11EProductionServiceError("A.3 bridge historical/current review-manifest hash mismatch")
    if lineage.get("allowed_json_pointer_difference") != ["/source_lineage/6/sha256"]:
        raise C11EProductionServiceError("A.3 bridge permits an unexpected structural difference")
    if lineage.get("installed_transition", {}).get("only_changed_json_pointer") != "/source_lineage/6/sha256":
        raise C11EProductionServiceError("A.3 installed transition is not the single approved pointer update")
    archive_identity = _file_identity(root, archive_rel)
    if archive_identity["sha256"] != A3_HISTORICAL_REVIEW_MANIFEST_SHA256 or archive_identity["bytes"] != 8591:
        raise C11EProductionServiceError("A.3 historical review-manifest archive is absent or changed")
    current_identity = _file_identity(root, manifest_rel)
    if current_identity["sha256"] != A3_CURRENT_REVIEW_MANIFEST_SHA256 or current_identity["bytes"] != 8591:
        raise C11EProductionServiceError("A.3 current review-manifest postimage is absent or changed")
    if dict(review_manifest_pin) != current_identity:
        raise C11EProductionServiceError("A.3 current review-manifest pin differs from bridge attestation")

    historical = read_json(archive_rel)
    current = read_json(manifest_rel)
    expected_current = copy.deepcopy(historical)
    try:
        old_pointer = expected_current["source_lineage"][6]["sha256"]
        new_pointer = lineage["new_pointer_value"]
        expected_current["source_lineage"][6]["sha256"] = new_pointer
    except Exception as exc:
        raise C11EProductionServiceError("A.3 review-manifest pointer location is malformed") from exc
    if old_pointer != lineage.get("old_pointer_value") or new_pointer != "dabb458fc2215156ddb5ebea7e8ebec811098886ce2858733ba9fb13f6075ccb":
        raise C11EProductionServiceError("A.3 old/new D9.8 pointer values differ from attestation")
    if current != expected_current:
        raise C11EProductionServiceError("A.3 review manifest differs beyond the single attested JSON pointer")
    model_rel = "definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json"
    model_identity = _file_identity(root, model_rel)
    if model_identity["sha256"] != new_pointer or lineage.get("pointer_target_path") != model_rel:
        raise C11EProductionServiceError("A.3 new lineage pointer does not target the pinned D9.8 model")

    proposal_lineage = window_proposal.get("source_lineage", [])
    historical_reference = any(
        isinstance(row, Mapping) and row.get("path") == manifest_rel and row.get("sha256") == A3_HISTORICAL_REVIEW_MANIFEST_SHA256
        for row in proposal_lineage
    )
    if not historical_reference:
        raise C11EProductionServiceError("A.3 immutable field-window proposal does not reference the attested historical manifest")
    return {
        "status": "PASS_A3_ATTESTED_SINGLE_POINTER_LINEAGE_BRIDGE",
        "bridge_path": A3_LINEAGE_BRIDGE_REL,
        "bridge_sha256": A3_LINEAGE_BRIDGE_SHA256,
        "field_window_proposal_sha256": A3_FIELD_WINDOW_PROPOSAL_SHA256,
        "historical_manifest_sha256": A3_HISTORICAL_REVIEW_MANIFEST_SHA256,
        "current_manifest_sha256": A3_CURRENT_REVIEW_MANIFEST_SHA256,
        "historical_archive_path": archive_rel,
        "single_pointer_difference": "/source_lineage/6/sha256",
        "d98_model_sha256": new_pointer,
        "proposal_bytes_mutated": False,
        "renderer_admission": False,
        "release_authority": "NONE",
    }


def _prepare_drill_family_boundary(
    root: Path,
    resolved: Mapping[str, Any],
    raw_request: Mapping[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Prepare the existing D9.9/D9.10 + Drill V2 binder chain; no Godot/media.

    The V2 binder is reused as-is. Its 20-selector real-Godot matrix remains a
    separately gated evidence run; this E1 preparation records only the exact
    canonical request/source-binding preview.
    """
    record = _assert_loop_operator_approvals(root)
    by_id = {row["decision_id"]: row for row in record["decisions"]}
    # E4B's composition approval is not consumed by Drill. These four exact
    # current-hash decisions are the only policy identities recorded here.
    drill_policy_ids = (
        "A.1_SHARED_PRESENTATION_REGIONS",
        "A.3_LOOP_DRILL_EDITORIAL_WINDOWS",
        "B.1_UNIFIED_DELIVERY_TIMEBASE",
        "D.1_AUDIO_MUSIC_DELIVERY_ENVELOPE",
    )
    drill_policy_decisions = []
    for decision_id in drill_policy_ids:
        row = by_id[decision_id]
        drill_policy_decisions.append({
            "decision_id": decision_id,
            "proposal_path": row["proposal_path"],
            "proposal_sha256": row["proposal_sha256"],
            "decision": row["decision"],
            "scope": "D_ONLY_DESIGN_AND_CONTRACT_IMPLEMENTATION_ONLY",
        })

    binder = _load_d9_boundary_module(root, "d_renderer_dynamic_request_payload_binding")
    try:
        contract_data = binder._load_contract_for_mode(root, "visual_drill_v2")
        contract = contract_data[0]
        canonical_selection = resolved["canonical_request"]["selection"]
        # D9.9 produces a normalized selection. Feed the existing V2 binder an
        # explicit four-key selector without adding aliases or a new binder.
        drill_request = copy.deepcopy(dict(raw_request))
        drill_request["selection"] = {
            "content_type": "visual_drills",
            "family_id": canonical_selection.get("family_id"),
            "subtype_id": None,
            "variant_id": canonical_selection.get("variant_id"),
        }
        chain = binder._build_canonical_chain(drill_request, root, allow_visual_drill_matrix=True)
    except Exception as exc:
        raise C11EProductionServiceError(f"Existing Drill dynamic binder V2 rejected the E1 request: {exc}") from exc

    bound_result = chain["result"]
    for key in ("request_hash", "editorial_hash", "plan_hash"):
        if bound_result.get(key) != resolved.get(key):
            raise C11EProductionServiceError(f"Drill V2 binder and E1 service disagree on canonical {key}")
    bound_request = bound_result.get("canonical_request", {})
    if bound_request.get("selection", {}).get("content_type") != "visual_drills":
        raise C11EProductionServiceError("Drill V2 binder did not preserve visual_drills content type")
    if bound_request.get("seed") != resolved["canonical_request"].get("seed") or bound_request.get("music_seed") != resolved["canonical_request"].get("music_seed"):
        raise C11EProductionServiceError("Drill V2 binder changed gameplay/music seed domains")
    if bound_request.get("seed") == bound_request.get("music_seed"):
        raise C11EProductionServiceError("Drill gameplay and music seeds must remain distinct")

    family_id = str(canonical_selection.get("family_id"))
    variant_id = str(canonical_selection.get("variant_id"))
    tier_match = re.fullmatch(r"tier-([1-5])", variant_id)
    if not tier_match:
        raise C11EProductionServiceError("Drill variant must be one canonical tier-1..tier-5 selector")
    tier = int(tier_match.group(1))

    producer_schema = json.loads((root / "c11c-suite" / "c11c-producer" / "producer_schema.json").read_text(encoding="utf-8-sig"))
    drill_definition = producer_schema.get("drills", {}).get(family_id)
    if not isinstance(drill_definition, Mapping):
        raise C11EProductionServiceError(f"C11-C Producer schema does not define Drill family {family_id}")
    if tier not in drill_definition.get("difficulty_values", []):
        raise C11EProductionServiceError(f"Drill tier is not admitted by C11-C family schema: {family_id}/{tier}")
    launcher = drill_definition.get("production_launcher")
    if launcher != "c11c-suite/c11c-producer/run_visual_drill_production.ps1":
        raise C11EProductionServiceError("Drill family must retain the canonical C11-C Drill launcher")

    music_registry_rel = "profiles/presentation/c11c_visual_music_profiles.json"
    music_registry = json.loads((root / music_registry_rel).read_text(encoding="utf-8-sig"))
    music_binding = music_registry.get("bindings", {}).get(f"visual_drill/{family_id}")
    if not isinstance(music_binding, Mapping):
        raise C11EProductionServiceError(f"C11-C FAMILY_MUSIC_V4 Drill binding missing: {family_id}")
    if music_binding.get("music_semantic_inputs") != ["seed"]:
        raise C11EProductionServiceError("C11-C Drill family music must remain seeded only by its explicit music seed")
    profile_id = music_binding.get("profile")
    valid_profiles = {row.get("id") for row in music_registry.get("profiles", []) if isinstance(row, Mapping)}
    if profile_id not in valid_profiles:
        raise C11EProductionServiceError("C11-C Drill music profile is not in the canonical profile registry")

    # Source-derived phase model. These C11-C files remain read-only and the
    # D/E contract records their current identities; it never reimplements them.
    phase_paths = [
        # The exact eight immutable C11-C presentation owners audited by A.3.
        "core/presentation/CountdownPresentationLogic.gd",
        "core/presentation/VisualDrillPresentationPhaseLogic.gd",
        "core/presentation/VisualDrillPresentationBinder.gd",
        "core/presentation/rendering/VisualContentPlayer.gd",
        "core/presentation/C11CVisualEditorialLayer.gd",
        "core/presentation/PresentationUI.gd",
        "core/presentation/SocialUIBinder.gd",
        "core/presentation/UnifiedSocialFrame.gd",
        # Read-only D/E launcher and envelope references; neither is modified.
        launcher,
        "c11c-suite/c11c-producer/C11CVisualDrillProducerEnvelopeGenerator.gd",
    ]
    phase_text = {path: _drill_source_text(root, path) for path in phase_paths}
    phase_logic = phase_text["core/presentation/VisualDrillPresentationPhaseLogic.gd"]
    countdown_logic = phase_text["core/presentation/CountdownPresentationLogic.gd"]
    binder_text = phase_text["core/presentation/VisualDrillPresentationBinder.gd"]
    player_text = phase_text["core/presentation/rendering/VisualContentPlayer.gd"]
    ui_text = phase_text["core/presentation/PresentationUI.gd"]
    launcher_text = phase_text[launcher]
    required_markers = (
        ("phase_logic", 'const END_CTA_SECONDS: float = 3.0' in phase_logic and '"PRE_ROLL"' in phase_logic and '"GAME"' in phase_logic and '"END_CTA"' in phase_logic and '"DONE"' in phase_logic),
        ("countdown", 'const COUNTDOWN_SECONDS: float = 3.0' in countdown_logic),
        ("binder_end_cta", 'if ui_state == "END_CTA":' in binder_text and 'model["cta_main"] = "¿LO CONSEGUISTE?"' in binder_text),
        ("header_precedence", 'editorial_model["header"]["line_1"] = ""' in binder_text and 'editorial_model["header"]["line_2"] = ""' in binder_text and 'The CTA owns the header during END_CTA' in binder_text),
        ("player_phase_dispatch", '"END_CTA"' in player_text and '"PRE_ROLL"' in player_text and '"GAME"' in player_text),
        ("ui_header_owner", 'The CTA owns Header only.' in ui_text),
        ("silent_launcher", '[switch]$NoSound' in launcher_text and 'if($NoSound)' in launcher_text),
    )
    failed_markers = [name for name, passed in required_markers if not passed]
    if failed_markers:
        raise C11EProductionServiceError("Drill C11-C phase/END_CTA contract markers changed: " + ", ".join(failed_markers))

    music_generator_rel = "tools/prototypes/c11c_common/generate_c11c_family_music.py"
    music_wrapper_rel = "tools/prototypes/c11c_common/C11CSafeAmbient.py"
    music_generator_text = _drill_source_text(root, music_generator_rel)
    music_wrapper_text = _drill_source_text(root, music_wrapper_rel)
    sample_rate_match = re.search(r"(?m)^SAMPLE_RATE\s*=\s*(\d+)\s*$", music_generator_text)
    channels_match = re.search(r"(?m)^CHANNELS\s*=\s*(\d+)\s*$", music_generator_text)
    if not sample_rate_match or not channels_match:
        raise C11EProductionServiceError("C11-C FAMILY_MUSIC_V4 native WAV format cannot be source-resolved")
    if 'visual_drill/' not in music_wrapper_text or "FAMILY_MUSIC_V4" not in music_registry.get("mode", ""):
        raise C11EProductionServiceError("C11-C native Drill music wrapper/registry identity mismatch")
    # The historic C11-C Drill launcher currently passes its gameplay $Seed to
    # its built-in audio call. E4C must therefore invoke it silently and use the
    # exact native helper separately with request.music_seed; C11-C stays intact.
    seed_coupling_present = bool(re.search(r"\$AudioGenerator\s+\$audio\s+\$Seed\b", launcher_text))
    if not seed_coupling_present:
        raise C11EProductionServiceError("C11-C Drill audio seed route changed; review before E4C orchestration")

    policy_paths = [
        "definitions/c11d/production/D_RENDERER_UNIFIED_PRESENTATION_REGION_POLICY_PROPOSAL_V1.json",
        "definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json",
        "definitions/c11d/production/D_RENDERER_UNIFIED_DELIVERY_TIMEBASE_POLICY_PROPOSAL_V1.json",
        "definitions/c11d/production/D_RENDERER_UNIFIED_AUDIO_MUSIC_DELIVERY_POLICY_PROPOSAL_V1.json",
        LOOP_OPERATOR_DECISION_REL,
    ]
    family_paths = [
        "c11c-suite/c11c-producer/producer_schema.json",
        f"definitions/visual_drill_{family_id}_canonical.json",
        f"profiles/difficulty/visual_drill_{family_id}.json",
        music_registry_rel,
        music_wrapper_rel,
        music_generator_rel,
    ]
    # Carry the full V2 lineage plus family-specific and phase/music sources.
    extra_paths = {row["path"] for row in contract_data[3]}
    extra_paths.update({
        "definitions/c11d/production/D_RENDERER_DYNAMIC_REQUEST_PAYLOAD_BINDING_V2.json",
        "definitions/c11d/production/D_RENDERER_DYNAMIC_REQUEST_PAYLOAD_INPUT_SCHEMA_V2.json",
        "definitions/c11d/production/D_RENDERER_DYNAMIC_REQUEST_PAYLOAD_BINDING_SCHEMA_V2.json",
        "tools/c11d/d9/d_renderer_dynamic_request_payload_binding.py",
        "tools/c11d/d9/editorial_render_bridge.py",
        "tools/c11d/d9/d_render_adapter.py",
        "definitions/c11d/production/C11D_EDITORIAL_RENDER_BRIDGE_D9_10_V1.json",
        "definitions/c11d/production/C11D_RENDER_ADAPTER_BOUNDARY_D9_10_V1.json",
        *phase_paths,
        *policy_paths,
        *family_paths,
        A3_LINEAGE_BRIDGE_REL,
        "definitions/c11d/production/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1.json",
        "docs/history/c11e/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1_PRE_D98_LINEAGE_REFRESH_20261106.json",
        "definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json",
    })
    extra_pins = [_file_identity(root, path) for path in sorted(extra_paths)]

    bridge = chain["bridge"]
    envelope = chain["envelope"]
    binding = chain["source_binding"]
    binding_preview = {
        "schema": "C11E-E4C-DRILL-DYNAMIC-BINDING-PREVIEW-V1",
        "status": "EXISTING_D9_V2_REQUEST_CHAIN_VALIDATED_NOT_GODOT_MATERIALIZED",
        "contract_identity": {
            "path": "definitions/c11d/production/D_RENDERER_DYNAMIC_REQUEST_PAYLOAD_BINDING_V2.json",
            "schema": contract.get("schema"),
            "schema_version": contract.get("schema_version"),
            "sha256": _file_identity(root, "definitions/c11d/production/D_RENDERER_DYNAMIC_REQUEST_PAYLOAD_BINDING_V2.json")["sha256"],
            "lineage_count": len(contract_data[3]),
        },
        "input_preview": binder._godot_input(chain, contract),
        "request_scoped_source_binding_sha256": binder._sha_json(binding),
        "request_scoped_source_binding_status": binding.get("status"),
        "request_payload_manifest": "NOT_MATERIALIZED_BY_E1_REQUIRES_REAL_GODOT_V2_EXECUTION",
        "runtime_repeat": "NOT_RUN_BY_E1",
        "renderer_native_input_emitted": False,
        "renderer_dispatch_invoked": False,
        "media_created": False,
        "release_authority": "NONE",
    }
    binding_preview["preview_sha256"] = sha256(binding_preview)

    # The native D9.8 model/window proposal source chain has a known transitive
    # stale-reference finding in the isolated V109 reconciliation. We do not
    # use it to emit visible text here; this boundary only prepares canonical
    # selector/source binding and records the C11-C native phase owner.
    review_manifest_pin = _file_identity(root, "definitions/c11d/production/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1.json")
    window_proposal = json.loads((root / policy_paths[1]).read_text(encoding="utf-8-sig"))
    lineage_resolution = _resolve_a3_review_manifest_lineage(root, window_proposal, review_manifest_pin)
    review_lineage_match = lineage_resolution.get("status") == "PASS_A3_ATTESTED_SINGLE_POINTER_LINEAGE_BRIDGE"

    phase_contract = {
        "schema": "C11E-E4C-DRILL-NATIVE-PHASE-AND-END-CTA-CONTRACT-V1",
        "status": "SOURCE_BOUND_NATIVE_PHASES_PRESERVED_NO_VISUAL_CONSUMPTION",
        "source_pins": [_file_identity(root, path) for path in phase_paths],
        "phase_sequence": [
            {"phase": "PRE_ROLL", "duration_source": "CountdownPresentationLogic.COUNTDOWN_SECONDS", "duration_seconds": 3.0},
            {"phase": "GAME", "duration_source": "ACTUAL_C11C_GENERATED_GAMEPLAY_FRAME_COUNT / FPS", "duration_seconds": None},
            {"phase": "END_CTA", "duration_source": "VisualDrillPresentationPhaseLogic.END_CTA_SECONDS", "duration_seconds": 3.0},
            {"phase": "DONE", "duration_source": "AFTER_TOTAL_PRESENTATION_FRAME_COUNT", "duration_seconds": 0.0},
        ],
        "frame_model": "ZERO_BASED_PRESENTATION_FRAME_INDEX; PRE_ROLL + GAME + END_CTA; C11-C PHASE LOGIC IS THE AUTHORITY",
        "end_cta_precedence": {
            "owner": "C11-C VisualDrillPresentationBinder",
            "native_cta_header_authoritative": True,
            "editorial_header_lines_1_and_2_suppressed_during_end_cta": True,
            "footer_telemetry_remains_visible": True,
            "d_adapter_may_override_native_cta": False,
        },
        "d_editorial_window_policy": {
            "decision_id": "A.3_LOOP_DRILL_EDITORIAL_WINDOWS",
            "approved_proposal_sha256": by_id["A.3_LOOP_DRILL_EDITORIAL_WINDOWS"]["proposal_sha256"],
            "field_window_consumption": "NOT_ENABLED_BY_E1",
            "transitive_review_manifest_lineage_current": review_lineage_match,
            "lineage_resolution": lineage_resolution,
            "visual_consumer_status": "READY_FOR_D_OWNED_ISOLATED_VISUAL_CONSUMER_TESTS" if review_lineage_match else "BLOCKED_PENDING_CURRENT_POLICY_LINEAGE_RECONCILIATION",
        },
        "renderer_native_input_emitted": False,
        "media_created": False,
    }
    phase_contract["phase_contract_sha256"] = sha256(phase_contract)

    stage = {
        "schema": "C11E-E4C-DRILL-FAMILY-STAGE-CONTRACT-V1",
        "status": "DRILL_FAMILY_BOUND_PREPARATION_NOT_DISPATCHABLE",
        "request_identity": {
            "request_id": str(bound_request.get("request_id")),
            "request_hash": bound_result["request_hash"],
            "plan_hash": bound_result["plan_hash"],
            "editorial_hash": bound_result["editorial_hash"],
            "bridge_record_hash": bridge["record_hash"],
            "d_only_adapter_envelope_hash": envelope["envelope_hash"],
            "drill_dynamic_binding_preview_sha256": binding_preview["preview_sha256"],
        },
        "content_identity": {
            "content_type": "visual_drills",
            "family_id": family_id,
            "variant_id": variant_id,
            "difficulty_tier": tier,
            "canonical_source_path": f"definitions/visual_drill_{family_id}_canonical.json",
            "difficulty_policy_path": f"profiles/difficulty/visual_drill_{family_id}.json",
        },
        "family_visual_stage": {
            "launcher_path": launcher,
            "argument_vector": [
                "-Family", family_id,
                "-Seed", str(bound_request["seed"]),
                "-DifficultyTier", str(tier),
                "-SpeedMultiplier", "1.0",
                "-PacingMode", "constant",
                "-DeliveryProfile", str(bound_request["delivery_profile_id"]),
                "-NoSound",
                "-OutputRoot", "<FRESH_ISOLATED_E4C_TEST_ROOT>",
            ],
            "parameter_policy": "E4C_DETERMINISTIC_REVIEW_DEFAULTS_V1_SPEED_1_0_PACING_CONSTANT; REVIEW_ONLY_UNTIL_EXPLICIT_REQUEST_FIELDS_EXIST",
            "audio_switch": "-NoSound",
            "gameplay_seed": bound_request["seed"],
            "music_seed": bound_request["music_seed"],
            "music_seed_passed_to_visual_launcher": False,
            "launcher_execution": False,
            "reason_not_executed": "D4_8_BLOCKED_AND_NO_RENDERER_EXECUTION_AUTHORITY",
        },
        "native_family_music": {
            "route": "PRESERVE_EXISTING_C11C_FAMILY_MUSIC_V4",
            "family_binding_id": f"visual_drill/{family_id}",
            "profile_id": profile_id,
            "registry_semantic_inputs": music_binding["music_semantic_inputs"],
            "request_music_seed_field": "request.music_seed",
            "generator_wrapper_path": music_wrapper_rel,
            "generator_source_path": music_generator_rel,
            "native_pcm_sample_rate_hz": int(sample_rate_match.group(1)),
            "native_pcm_channels": int(channels_match.group(1)),
            "music_seed_passed_as_native_generator_seed": True,
            "audio_selection_or_generation_authorized": False,
            "audio_generation_invoked": False,
            "audio_payload_materialized": False,
            "d3_v5_invoked": False,
            "duration_source": "C11-C_GENERATED_DRILL_TOTAL_DURATION; MUST MATCH PRE_ROLL + GAME + END_CTA",
        },
        "dynamic_request_binding_preview": binding_preview,
        "phase_and_end_cta_contract": phase_contract,
        "policy_decisions": drill_policy_decisions,
        "editorial": {
            "values_preserved_in_d9_request": True,
            "payload_field_consumption": "NOT_CONSUMED_E1",
            "visual_field_windows": "NOT_EMITTED",
            "visual_consumer": "BLOCKED_PENDING_E4C_PHASE_AND_POLICY_CLOSEOUT",
        },
        "governance": {
            "family_stage_contract_created_in_memory": True,
            "renderer_native_input_emitted": False,
            "renderer_dispatch_invoked": False,
            "launcher_invoked": False,
            "godot_invoked": False,
            "ffmpeg_invoked": False,
            "media_created": False,
            "audio_generated": False,
            "c11c_source_mutation": False,
            "d4_8": "BLOCKED",
            "d9_10": "PREPARE_ONLY",
            "release_authority": "NONE",
        },
    }
    stage["contract_sha256"] = sha256(stage)

    preparation = {
        "schema": "C11E-E4C-SHARED-DRILL-BOUNDARY-PREPARATION-V1",
        "status": "DRILL_FAMILY_STAGE_PREPARED_NOT_DISPATCHABLE",
        "bridge_planning_record": bridge,
        "d_only_adapter_envelope": envelope,
        "drill_family_stage_contract": stage,
        "dynamic_request_binding_preview": binding_preview,
        "native_phase_and_end_cta_contract": phase_contract,
        "required_source_pin_paths": sorted(extra_paths | {"tools/c11d/d9/d_renderer_dynamic_request_payload_binding.py"}),
        "renderer_input_emitted": False,
        "renderer_dispatch_invoked": False,
        "launcher_invoked": False,
        "godot_invoked": False,
        "ffmpeg_invoked": False,
        "audio_generation_invoked": False,
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
    drill_boundary_preparation = None
    drill_boundary_source_pins: list[dict[str, Any]] = []
    if content_type == "visual_loops":
        loop_boundary_preparation, loop_boundary_source_pins = _prepare_loop_family_boundary(root, resolved)
    elif content_type == "visual_drills":
        drill_boundary_preparation, drill_boundary_source_pins = _prepare_drill_family_boundary(root, resolved, request)
    source_identity = _source_identity(root, canonical_request, music_source_pins + loop_boundary_source_pins + drill_boundary_source_pins)
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
    if drill_boundary_preparation is not None:
        intent_semantics["d9_boundary_preparation_identity"] = {
            "preparation_sha256": drill_boundary_preparation["preparation_sha256"],
            "bridge_record_hash": drill_boundary_preparation["bridge_planning_record"]["record_hash"],
            "d_only_adapter_envelope_hash": drill_boundary_preparation["d_only_adapter_envelope"]["envelope_hash"],
            "drill_family_stage_contract_sha256": drill_boundary_preparation["drill_family_stage_contract"]["contract_sha256"],
            "dynamic_request_binding_preview_sha256": drill_boundary_preparation["dynamic_request_binding_preview"]["preview_sha256"],
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
        "schema_version": "1.3" if drill_boundary_preparation is not None else ("1.2" if loop_boundary_preparation is not None else "1.1"),
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
    if drill_boundary_preparation is not None:
        intent["d9_boundary_preparation"] = drill_boundary_preparation
    intent["intent_sha256"] = sha256(intent)
    return {"intent": intent, "resolver_result": resolved}


def validate_c11e_production_intent(
    intent: Mapping[str, Any],
    project_root: Path | str | None = None,
) -> dict[str, Any]:
    """Validate self-seal, D9 hashes, seed separation, source pins and fail-closed flags."""
    root = _root(project_root)
    if not isinstance(intent, Mapping) or intent.get("schema") != SERVICE_SCHEMA or intent.get("schema_version") not in {"1.1", "1.2", "1.3"}:
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
    expected_schema_version = "1.3" if content_type == "visual_drills" else ("1.2" if content_type == "visual_loops" else "1.1")
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
    identity = intent.get("identity", {})
    loop_preparation_identity = None
    drill_preparation_identity = None
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
    elif content_type == "visual_drills":
        preparation = intent.get("d9_boundary_preparation")
        if not isinstance(preparation, Mapping) or preparation.get("schema") != "C11E-E4C-SHARED-DRILL-BOUNDARY-PREPARATION-V1" or preparation.get("status") != "DRILL_FAMILY_STAGE_PREPARED_NOT_DISPATCHABLE":
            raise C11EProductionServiceError("E4C shared Drill boundary preparation is missing")
        unsigned_preparation = {key: value for key, value in preparation.items() if key != "preparation_sha256"}
        if preparation.get("preparation_sha256") != sha256(unsigned_preparation):
            raise C11EProductionServiceError("E4C shared Drill preparation self-hash mismatch")
        bridge = preparation.get("bridge_planning_record")
        envelope = preparation.get("d_only_adapter_envelope")
        stage = preparation.get("drill_family_stage_contract")
        binding_preview = preparation.get("dynamic_request_binding_preview")
        phase_contract = preparation.get("native_phase_and_end_cta_contract")
        if not all(isinstance(value, Mapping) for value in (bridge, envelope, stage, binding_preview, phase_contract)):
            raise C11EProductionServiceError("E4C Drill preparation records are incomplete")
        bridge_module = _load_d9_boundary_module(root, "editorial_render_bridge")
        adapter_module = _load_d9_boundary_module(root, "d_render_adapter")
        binder_module = _load_d9_boundary_module(root, "d_renderer_dynamic_request_payload_binding")
        if bridge.get("schema") != bridge_module.RECORD_SCHEMA or bridge.get("status") != "PLANNING_ONLY_NOT_RENDERABLE":
            raise C11EProductionServiceError("E4C D9.10 bridge is not planning-only")
        if bridge.get("record_hash") != bridge_module.sha256({key: value for key, value in bridge.items() if key != "record_hash"}):
            raise C11EProductionServiceError("E4C D9.10 bridge self-hash mismatch")
        adapter_module.validate_d_only_adapter_envelope(envelope, root)
        if stage.get("schema") != "C11E-E4C-DRILL-FAMILY-STAGE-CONTRACT-V1" or stage.get("status") != "DRILL_FAMILY_BOUND_PREPARATION_NOT_DISPATCHABLE":
            raise C11EProductionServiceError("E4C Drill stage identity/status mismatch")
        unsigned_stage = {key: value for key, value in stage.items() if key != "contract_sha256"}
        if stage.get("contract_sha256") != sha256(unsigned_stage):
            raise C11EProductionServiceError("E4C Drill stage self-hash mismatch")
        if binding_preview.get("schema") != "C11E-E4C-DRILL-DYNAMIC-BINDING-PREVIEW-V1" or binding_preview.get("status") != "EXISTING_D9_V2_REQUEST_CHAIN_VALIDATED_NOT_GODOT_MATERIALIZED":
            raise C11EProductionServiceError("E4C Drill dynamic binding preview is not the existing V2 binder path")
        unsigned_binding_preview = {key: value for key, value in binding_preview.items() if key != "preview_sha256"}
        if binding_preview.get("preview_sha256") != sha256(unsigned_binding_preview):
            raise C11EProductionServiceError("E4C Drill dynamic binding preview self-hash mismatch")
        if binding_preview.get("contract_identity", {}).get("schema") != binder_module.DRILL_V2_CONTRACT_ID or binding_preview.get("contract_identity", {}).get("schema_version") != "2.0":
            raise C11EProductionServiceError("E4C Drill did not reuse the existing Dynamic Request Binding V2 contract")
        input_preview = binding_preview.get("input_preview", {})
        selected = request.get("selection", {})
        if input_preview.get("request_hash") != identity.get("request_hash") or input_preview.get("selection", {}).get("content_type") != "visual_drills" or input_preview.get("selection", {}).get("family_id") != selected.get("family_id") or input_preview.get("selection", {}).get("variant_id") != selected.get("variant_id"):
            raise C11EProductionServiceError("E4C Drill request-bound preview differs from E1 canonical selector identity")
        if input_preview.get("seed") != gameplay.get("value") or input_preview.get("music_seed") != music.get("value") or input_preview.get("seed") == input_preview.get("music_seed"):
            raise C11EProductionServiceError("E4C Drill dynamic preview seed domains are not independent")
        if phase_contract.get("schema") != "C11E-E4C-DRILL-NATIVE-PHASE-AND-END-CTA-CONTRACT-V1" or phase_contract.get("status") != "SOURCE_BOUND_NATIVE_PHASES_PRESERVED_NO_VISUAL_CONSUMPTION":
            raise C11EProductionServiceError("E4C Drill native phase/END_CTA contract identity mismatch")
        unsigned_phase = {key: value for key, value in phase_contract.items() if key != "phase_contract_sha256"}
        if phase_contract.get("phase_contract_sha256") != sha256(unsigned_phase):
            raise C11EProductionServiceError("E4C Drill phase/END_CTA contract self-hash mismatch")
        a3_window = phase_contract.get("d_editorial_window_policy", {})
        lineage_resolution = a3_window.get("lineage_resolution", {})
        if a3_window.get("transitive_review_manifest_lineage_current") is not True or lineage_resolution.get("status") != "PASS_A3_ATTESTED_SINGLE_POINTER_LINEAGE_BRIDGE" or lineage_resolution.get("bridge_sha256") != A3_LINEAGE_BRIDGE_SHA256:
            raise C11EProductionServiceError("E4C Drill A.3 transitive policy lineage is not bridged to the installed review-manifest postimage")
        if a3_window.get("visual_consumer_status") != "READY_FOR_D_OWNED_ISOLATED_VISUAL_CONSUMER_TESTS":
            raise C11EProductionServiceError("E4C Drill visual consumer is not cleared for isolated D-owned tests")
        if phase_contract.get("end_cta_precedence", {}).get("native_cta_header_authoritative") is not True or phase_contract.get("end_cta_precedence", {}).get("d_adapter_may_override_native_cta") is not False:
            raise C11EProductionServiceError("E4C Drill END_CTA precedence was weakened")
        if stage.get("request_identity", {}).get("bridge_record_hash") != bridge.get("record_hash") or stage.get("request_identity", {}).get("d_only_adapter_envelope_hash") != envelope.get("envelope_hash") or stage.get("request_identity", {}).get("drill_dynamic_binding_preview_sha256") != binding_preview.get("preview_sha256"):
            raise C11EProductionServiceError("E4C Drill stage is not bound to the existing D9.10/V2 records")
        if stage.get("content_identity", {}).get("family_id") != selected.get("family_id") or stage.get("content_identity", {}).get("variant_id") != selected.get("variant_id") or stage.get("content_identity", {}).get("content_type") != "visual_drills":
            raise C11EProductionServiceError("E4C Drill stage selector differs from the E1 request")
        if stage.get("family_visual_stage", {}).get("audio_switch") != "-NoSound" or stage.get("family_visual_stage", {}).get("music_seed_passed_to_visual_launcher") is not False:
            raise C11EProductionServiceError("E4C Drill C11-C visual launcher must remain silent and gameplay-seeded only")
        if stage.get("native_family_music", {}).get("route") != "PRESERVE_EXISTING_C11C_FAMILY_MUSIC_V4" or stage.get("native_family_music", {}).get("request_music_seed_field") != "request.music_seed" or stage.get("native_family_music", {}).get("d3_v5_invoked") is not False:
            raise C11EProductionServiceError("E4C Drill native family music route/seed identity changed")
        if stage.get("governance", {}).get("d4_8") != "BLOCKED" or stage.get("governance", {}).get("d9_10") != "PREPARE_ONLY" or stage.get("governance", {}).get("release_authority") != "NONE":
            raise C11EProductionServiceError("E4C Drill governance boundary changed")
        for field in ("renderer_native_input_emitted", "renderer_dispatch_invoked", "launcher_invoked", "godot_invoked", "ffmpeg_invoked", "media_created", "audio_generated", "c11c_source_mutation"):
            if stage.get("governance", {}).get(field) is not False:
                raise C11EProductionServiceError(f"E4C Drill stage execution boundary changed: {field}")
        required_paths = set(preparation.get("required_source_pin_paths", []))
        pinned_paths = {row.get("path") for row in intent.get("source_identity", {}).get("source_pins", []) if isinstance(row, Mapping)}
        if not required_paths or not required_paths.issubset(pinned_paths):
            raise C11EProductionServiceError("E4C Drill dynamic binder/family source-pin coverage is incomplete")
        if preparation.get("renderer_input_emitted") is not False or preparation.get("renderer_dispatch_invoked") is not False or preparation.get("launcher_invoked") is not False or preparation.get("godot_invoked") is not False or preparation.get("ffmpeg_invoked") is not False or preparation.get("audio_generation_invoked") is not False or preparation.get("media_created") is not False or preparation.get("release_authority") != "NONE":
            raise C11EProductionServiceError("E4C Drill shared boundary crossed its prepare-only execution limits")
        if adapter.get("status") != "NOT_CONNECTED_E1":
            raise C11EProductionServiceError("E1 Drill visual consumer remains not connected; binding preview is not visual consumption")
        drill_preparation_identity = {
            "preparation_sha256": preparation["preparation_sha256"],
            "bridge_record_hash": bridge["record_hash"],
            "d_only_adapter_envelope_hash": envelope["envelope_hash"],
            "drill_family_stage_contract_sha256": stage["contract_sha256"],
            "dynamic_request_binding_preview_sha256": binding_preview["preview_sha256"],
        }
    else:
        if adapter.get("status") != "NOT_CONNECTED_E1" or "d9_boundary_preparation" in intent:
            raise C11EProductionServiceError("Non-family E1 adapter must remain unconnected")
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
    if drill_preparation_identity is not None:
        intent_semantics["d9_boundary_preparation_identity"] = drill_preparation_identity
    if sha256(intent_semantics) != identity.get("intent_hash"):
        raise C11EProductionServiceError("C11-E semantic intent hash mismatch")
    return {"valid": True, "status": "PASS_E1_PREPARATION_ONLY", "intent_sha256": supplied, "source_pin_count": len(pinned), "renderer": False, "media_created": False}
