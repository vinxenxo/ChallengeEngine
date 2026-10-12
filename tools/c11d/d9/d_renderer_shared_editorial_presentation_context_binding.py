"""D9 request-scoped shared editorial/presentation identity binding.

Consumes the canonical D9.9 result and D9.10 planning bridge; emits a strict
identity/context receipt to memory/stdout only. It does not generate renderer input.
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from collections.abc import Mapping
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_SHARED_EDITORIAL_PRESENTATION_CONTEXT_BINDING_CONTRACT_V1.json")
CONTRACT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_SHARED_EDITORIAL_PRESENTATION_CONTEXT_BINDING_CONTRACT_SCHEMA_V1.json")
OUTPUT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_SHARED_EDITORIAL_PRESENTATION_CONTEXT_BINDING_SCHEMA_V1.json")
REGISTRY_REL = Path("definitions/c11d/production/D_RENDERER_SHARED_PRESENTATION_PROFILE_REFERENCE_REGISTRY_V1.json")
REGISTRY_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_SHARED_PRESENTATION_PROFILE_REFERENCE_REGISTRY_SCHEMA_V1.json")
MODEL_REL = Path("definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json")
INHERITANCE_REL = Path("definitions/c11d/production/D_RENDERER_SHARED_EDITORIAL_PRESENTATION_INHERITANCE_V1.json")
BRIDGE_CONTRACT_REL = Path("definitions/c11d/production/C11D_EDITORIAL_RENDER_BRIDGE_D9_10_V1.json")
OUTPUT_SCHEMA = "C11-D-D9-SHARED-EDITORIAL-PRESENTATION-CONTEXT-BINDING-V1"
CONTRACT_SCHEMA = "C11-D-D9-SHARED-EDITORIAL-PRESENTATION-CONTEXT-BINDING-CONTRACT-V1"
REGISTRY_SCHEMA = "C11-D-D9-SHARED-PRESENTATION-PROFILE-REFERENCE-REGISTRY-V1"
class SharedContextBindingError(ValueError):
    pass

def _root(project_root: Path | str | None = None) -> Path:
    return Path(project_root).resolve() if project_root is not None else ROOT

def _read_json(root: Path, rel: Path) -> dict[str, Any]:
    try:
        value = json.loads((root / rel).read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise SharedContextBindingError(f"Cannot read {rel.as_posix()}: {exc}") from exc
    if not isinstance(value, dict):
        raise SharedContextBindingError(f"Expected JSON object: {rel.as_posix()}")
    return value

def _canonical(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(k): _canonical(value[k]) for k in sorted(value, key=lambda item: str(item))}
    if isinstance(value, (list, tuple)):
        return [_canonical(item) for item in value]
    return value

def canonical_json(value: Any) -> str:
    return json.dumps(_canonical(value), ensure_ascii=False, separators=(",", ":"), allow_nan=False)

def sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()

def _file_sha(root: Path, rel: str) -> str:
    try:
        return hashlib.sha256((root / rel).read_bytes()).hexdigest()
    except Exception as exc:
        raise SharedContextBindingError(f"Cannot hash pinned source {rel}: {exc}") from exc

def _validate_json_schema(instance: dict[str, Any], schema: dict[str, Any], label: str) -> None:
    try:
        import jsonschema
        jsonschema.Draft202012Validator.check_schema(schema)
        errors = sorted(jsonschema.Draft202012Validator(schema).iter_errors(instance), key=lambda e: list(map(str, e.path)))
    except ImportError as exc:
        raise SharedContextBindingError("jsonschema is required for strict D9 context binding validation") from exc
    except Exception as exc:
        raise SharedContextBindingError(f"Invalid {label} schema: {exc}") from exc
    if errors:
        raise SharedContextBindingError(f"{label} schema violation: {errors[0].message}")

def validate_contract(project_root: Path | str | None = None) -> dict[str, Any]:
    root = _root(project_root)
    contract = _read_json(root, CONTRACT_REL)
    if contract.get("schema") != CONTRACT_SCHEMA or contract.get("schema_version") != "1.0":
        raise SharedContextBindingError("Context-binding contract identity mismatch")
    if contract.get("status") != "PREPARE_ONLY_SHARED_CONTEXT_BINDING_NOT_RENDERER_INPUT":
        raise SharedContextBindingError("Context-binding contract must remain preparation-only")
    if contract.get("supported_content_types") != ["challenges", "visual_loops", "visual_drills"]:
        raise SharedContextBindingError("Supported content type matrix drift")
    if contract.get("governance") != {"renderer_activation": False, "production_execution": False, "media_created": False, "c11c_source_mutation": False, "d4_8": "BLOCKED", "release_authority": "NONE", "d9_17": "BLOCKED_NO_GO", "d10": "BLOCKED"}:
        raise SharedContextBindingError("Execution/governance locks drift")
    pins = contract.get("source_lineage")
    if not isinstance(pins, list) or len(pins) < 14 or not pins or pins[0].get("path") != "release/C11C_FREEZE_PACKAGE_MANIFEST.json" or pins[0].get("sha256") != MANIFEST_SHA256:
        raise SharedContextBindingError("Frozen C11-C manifest must lead source lineage")
    seen: set[str] = set()
    for row in pins:
        if not isinstance(row, Mapping) or set(row) != {"path", "role", "sha256"}:
            raise SharedContextBindingError("Malformed context-binding source lineage row")
        rel = str(row["path"]); digest = str(row["sha256"])
        path = PurePosixPath(rel)
        if path.is_absolute() or ".." in path.parts or "\\" in rel or rel in seen:
            raise SharedContextBindingError(f"Unsafe or duplicate source pin: {rel}")
        if not re.fullmatch(r"[a-f0-9]{64}", digest):
            raise SharedContextBindingError(f"Invalid source digest: {rel}")
        if _file_sha(root, rel) != digest:
            raise SharedContextBindingError(f"Pinned source drift: {rel}")
        seen.add(rel)
    contract_schema = _read_json(root, CONTRACT_SCHEMA_REL)
    output_schema = _read_json(root, OUTPUT_SCHEMA_REL)
    registry = _read_json(root, REGISTRY_REL)
    registry_schema = _read_json(root, REGISTRY_SCHEMA_REL)
    try:
        import jsonschema
        jsonschema.Draft202012Validator.check_schema(output_schema)
    except ImportError as exc:
        raise SharedContextBindingError("jsonschema is required for strict D9 context binding validation") from exc
    except Exception as exc:
        raise SharedContextBindingError(f"Invalid context-binding output schema: {exc}") from exc
    _validate_json_schema(contract, contract_schema, "Context-binding contract")
    _validate_json_schema(registry, registry_schema, "Presentation reference registry")
    if registry.get("schema") != REGISTRY_SCHEMA or registry.get("schema_version") != "1.0" or registry.get("status") != "REFERENCE_IDENTITY_ONLY_NOT_PHYSICAL_BINDING":
        raise SharedContextBindingError("Presentation reference registry identity/status mismatch")
    source_lineage = registry.get("source_lineage", [])
    if len(source_lineage) < 3 or source_lineage[0].get("sha256") != MANIFEST_SHA256:
        raise SharedContextBindingError("Profile registry lineage must lead with frozen C11-C manifest")
    registry_seen: set[str] = set()
    for row in source_lineage:
        if not isinstance(row, Mapping) or set(row) != {"path", "role", "sha256"}:
            raise SharedContextBindingError("Malformed profile registry source lineage")
        rel = str(row["path"])
        if rel in registry_seen or _file_sha(root, rel) != str(row["sha256"]):
            raise SharedContextBindingError(f"Profile registry source drift/duplicate: {rel}")
        registry_seen.add(rel)
    profile_source = (root / "core/presentation/PresentationProfile.gd").read_text(encoding="utf-8-sig")
    entries = registry.get("profiles")
    if not isinstance(entries, list) or not entries:
        raise SharedContextBindingError("Presentation profile registry is empty")
    ids: set[str] = set(); defaults = 0
    for entry in entries:
        if not isinstance(entry, Mapping):
            raise SharedContextBindingError("Presentation profile entry must be an object")
        profile_id = entry.get("profile_id")
        if not isinstance(profile_id, str) or not profile_id.strip() or profile_id in ids:
            raise SharedContextBindingError("Empty or duplicate presentation profile ID")
        ids.add(profile_id)
        if entry.get("identity_source") != "core/presentation/PresentationProfile.gd" or entry.get("identity_token") not in profile_source:
            raise SharedContextBindingError(f"Unproven presentation identity: {profile_id}")
        if entry.get("status") != "REGISTERED_REFERENCE_ONLY" or entry.get("geometry_state") != "NOT_RESOLVED_BY_IDENTITY_REGISTRY" or entry.get("render_ready") is not False:
            raise SharedContextBindingError("Presentation registry may contain references only, not render-ready profiles")
        defaults += int(entry.get("default") is True)
    if registry.get("default_profile_id") not in ids or defaults != 1:
        raise SharedContextBindingError("Presentation registry must have one registered default profile")
    model = _read_json(root, MODEL_REL)
    inheritance = _read_json(root, INHERITANCE_REL)
    bridge_contract = _read_json(root, BRIDGE_CONTRACT_REL)
    if inheritance.get("schema") != "C11-D-D9-SHARED-EDITORIAL-PRESENTATION-INHERITANCE-CONTRACT-V1":
        raise SharedContextBindingError("Shared inheritance contract identity mismatch")
    if inheritance.get("authority", {}).get("renderer_activation") is not False or inheritance.get("authority", {}).get("release_authority") != "NONE":
        raise SharedContextBindingError("Shared inheritance contract authority locks drift")
    if bridge_contract.get("schema") != "C11-D-D9.10-EDITORIAL-RENDER-BRIDGE-CONTRACT-V1":
        raise SharedContextBindingError("D9.10 bridge contract identity mismatch")
    _validate_json_schema(registry, registry_schema, "Presentation reference registry")
    return {"root": root, "contract": contract, "contract_schema": contract_schema, "output_schema": output_schema,
            "registry": registry, "registry_schema": registry_schema, "model": model, "inheritance": inheritance,
            "bridge_contract": bridge_contract, "lineage_count": len(pins)}

def build_context_binding_from_result(result: Mapping[str, Any], project_root: Path | str | None = None) -> dict[str, Any]:
    root = _root(project_root)
    state = validate_contract(root)
    if not isinstance(result, Mapping) or result.get("status") != "PLANNED":
        raise SharedContextBindingError("Input must be a successful canonical D9.9 PLANNED result")
    request = result.get("canonical_request"); plan = result.get("plan")
    if not isinstance(request, Mapping) or not isinstance(plan, Mapping):
        raise SharedContextBindingError("Canonical result must include request and plan objects")
    from editorial_render_bridge import build_bridge_planning_record, EditorialRenderBridgeError
    bridge = build_bridge_planning_record(result, root)
    if result.get("request_hash") != sha256(request) or plan.get("request_hash") != result.get("request_hash"):
        raise SharedContextBindingError("Request identity does not match canonical request/plan")
    if result.get("plan_hash") != sha256(plan):
        raise SharedContextBindingError("Plan hash mismatch")
    selection = plan.get("selection")
    if not isinstance(selection, Mapping) or selection != request.get("selection"):
        raise SharedContextBindingError("Canonical request and plan selection mismatch")
    content_type = selection.get("content_type")
    if content_type not in state["contract"]["supported_content_types"]:
        raise SharedContextBindingError(f"Unsupported content type: {content_type!r}")
    editorial = plan.get("editorial")
    if not isinstance(editorial, Mapping) or editorial != request.get("editorial"):
        raise SharedContextBindingError("Editorial values must match canonical request and plan")
    model_content = state["model"].get("content_types", {}).get(content_type, {})
    allowlist = model_content.get("editable_fields", [])
    if not isinstance(allowlist, list) or set(editorial) != set(allowlist):
        raise SharedContextBindingError("Canonical editorial fields do not exactly match the D9.8 content-type allowlist")
    if any(not isinstance(value, str) for value in editorial.values()):
        raise SharedContextBindingError("Every canonical editorial value must be a normalized string")
    shared_fields = state["inheritance"]["shared_editorial_layer"]["shared_enabled_fields"]
    if any(field not in editorial for field in shared_fields):
        raise SharedContextBindingError("The request lacks one or more canonical shared editorial fields")
    challenge_fields = state["inheritance"]["shared_editorial_layer"]["challenge_only_enabled_fields"] if content_type == "challenges" else []
    if any(field not in editorial for field in challenge_fields):
        raise SharedContextBindingError("Challenge-specific canonical field missing")
    if content_type != "challenges" and set(editorial) & set(state["inheritance"]["shared_editorial_layer"]["challenge_only_enabled_fields"]):
        raise SharedContextBindingError("Challenge-only editorial fields cannot cross into Loops/Drills")
    if result.get("editorial_hash") != sha256({"selection": selection, "editorial": editorial}) or plan.get("editorial_hash") != result.get("editorial_hash"):
        raise SharedContextBindingError("Editorial value hash mismatch")
    pid = request.get("presentation_profile_id")
    if not isinstance(pid, str) or not pid.strip() or pid == "UNKNOWN":
        raise SharedContextBindingError("An explicit registered presentation_profile_id is required")
    if plan.get("presentation_profile_id") != pid or bridge.get("presentation_profile_id") != pid:
        raise SharedContextBindingError("Presentation profile identity differs across request, plan and bridge")
    entry_matches = [entry for entry in state["registry"]["profiles"] if entry.get("profile_id") == pid]
    if len(entry_matches) != 1:
        raise SharedContextBindingError(f"Unregistered presentation_profile_id: {pid}")
    entry = entry_matches[0]
    if bridge.get("identity", {}).get("request_hash") != result.get("request_hash") or bridge.get("identity", {}).get("plan_hash") != result.get("plan_hash") or bridge.get("identity", {}).get("editorial_hash") != result.get("editorial_hash"):
        raise SharedContextBindingError("D9.10 bridge identity does not match the canonical result")
    if bridge.get("editorial", {}).get("values_hash") != sha256(editorial):
        raise SharedContextBindingError("D9.10 bridge editorial values hash mismatch")
    bridge_without_hash = dict(bridge); bridge_hash = bridge_without_hash.pop("record_hash", None)
    if bridge_hash != sha256(bridge_without_hash):
        raise SharedContextBindingError("D9.10 bridge record self-hash mismatch")

    shared_values = {field: editorial[field] for field in shared_fields}
    display_values = {field: editorial[field] for field in state["inheritance"]["shared_editorial_layer"]["shared_display_text_fields"]}
    metadata_values = {field: editorial[field] for field in state["inheritance"]["shared_editorial_layer"]["shared_metadata_fields"]}
    content_specific_values = {field: editorial[field] for field in challenge_fields}
    source_contracts = {
        "binding_contract_sha256": sha256(state["contract"]),
        "editorial_model_sha256": sha256(state["model"]),
        "bridge_contract_sha256": sha256(state["bridge_contract"]),
        "inheritance_contract_sha256": sha256(state["inheritance"]),
        "profile_registry_schema_sha256": sha256(state["registry_schema"]),
        "profile_registry_sha256": sha256(state["registry"]),
    }
    context = {
        "schema": OUTPUT_SCHEMA,
        "schema_version": "1.0",
        "status": "REQUEST_SCOPED_SHARED_CONTEXT_BOUND_NOT_RENDERER_INPUT",
        "identity": {
            "request_id": request.get("request_id"), "content_type": content_type,
            "request_sha256": result["request_hash"], "editorial_sha256": result["editorial_hash"],
            "plan_sha256": result["plan_hash"], "bridge_record_sha256": bridge_hash,
        },
        "selection": _canonical(selection),
        "editorial_binding": {
            "source_model": MODEL_REL.as_posix(), "source_plan_field": "plan.editorial",
            "model_sha256": sha256(state["model"]), "resolved_values": _canonical(editorial),
            "field_names": sorted(editorial), "shared_display_text_fields": display_values,
            "shared_metadata_fields": metadata_values, "content_specific_fields": content_specific_values,
            "inheritance_layers": list(request.get("editorial_layers_applied", [])),
            "values_sha256": sha256(editorial), "shared_values_sha256": sha256(shared_values),
            "resolution_state": "CANONICAL_D9_8_MODEL_VIA_D9_9_PLAN",
        },
        "presentation_binding": {
            "profile_id": pid, "registry_status": "REGISTERED_REFERENCE_IDENTITY_CONFIRMED",
            "registry_sha256": sha256(state["registry"]), "registry_entry_sha256": sha256(entry),
            "identity_source": entry["identity_source"], "identity_token": entry["identity_token"],
            "reference_source": "canonical_request.presentation_profile_id", "geometry_resolution": "NOT_PERFORMED",
            "presentation_policy_approved": False, "renderer_profile_object_created": False,
        },
        "domain_binding": {
            "gameplay_seed": plan["seed"], "gameplay_seed_source": "canonical_request.seed", "gameplay_domain": "GAMEPLAY",
            "music_seed": plan["music_seed"], "music_seed_source": "canonical_request.music_seed", "music_domain": "MUSIC",
            "cross_domain_sharing": "FORBIDDEN", "automatic_generation": False, "runtime_derivation": False,
        },
        "delivery_binding": {
            "requested_delivery_profile_id": request["delivery_profile_id"],
            "resolved_delivery_profile_id": plan["resolved_delivery_profile_id"],
            "variation_index": plan["variation_index"], "audio_enabled": plan["audio_enabled"],
        },
        "source_contracts": source_contracts,
        "execution_boundary": {
            "mode": "IN_MEMORY_REQUEST_CONTEXT_BINDING_ONLY", "report_persisted": False,
            "renderer_native_input_emitted": False, "renderer_dispatch_invoked": False,
            "renderer_activation": False, "production_execution": False, "media_created": False,
            "c11c_source_mutation": False, "candidate_input_admissible": False,
            "d4_8": "BLOCKED", "release_authority": "NONE", "d9_17": "BLOCKED_NO_GO", "d10": "BLOCKED",
        },
    }
    context_hash = sha256(context)
    record = dict(context)
    record["binding_context_sha256"] = context_hash
    record["record_sha256"] = sha256(record)
    _validate_json_schema(record, state["output_schema"], "Shared context binding record")
    return record

def build_context_binding(raw_request: Mapping[str, Any], project_root: Path | str | None = None) -> dict[str, Any]:
    root = _root(project_root)
    try:
        from universal_producer import evaluate_universal_request
        result = evaluate_universal_request(raw_request, root)
    except Exception as exc:
        raise SharedContextBindingError(f"Canonical D9.9 request evaluation failed: {exc}") from exc
    return build_context_binding_from_result(result, root)

def validate_binding_record(record: Mapping[str, Any], canonical_result: Mapping[str, Any], project_root: Path | str | None = None) -> bool:
    if not isinstance(record, Mapping):
        raise SharedContextBindingError("Binding record must be an object")
    expected = build_context_binding_from_result(canonical_result, project_root)
    if dict(record) != expected:
        raise SharedContextBindingError("Binding record does not match the canonical request/plan and current registered source contracts")
    return True

def audit(project_root: Path | str | None = None) -> dict[str, int]:
    state = validate_contract(project_root)
    return {"source_pins": state["lineage_count"], "registered_profiles": len(state["registry"]["profiles"]), "supported_content_types": len(state["contract"]["supported_content_types"]), "shared_fields": len(state["inheritance"]["shared_editorial_layer"]["shared_enabled_fields"]), "reserved_fields": len(state["inheritance"]["shared_editorial_layer"]["reserved_disabled_fields"])}

def main() -> int:
    parser = argparse.ArgumentParser(description="D9 request-scoped shared editorial/presentation context binding; no renderer input")
    parser.add_argument("--project-root", type=Path, default=None)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--request", type=Path, help="Existing canonical D9.9 request JSON, read-only")
    group.add_argument("--audit-only", action="store_true", help="Verify pinned sources and registry only")
    args = parser.parse_args()
    try:
        if args.audit_only:
            counts = audit(args.project_root)
            print("C11-D SHARED EDITORIAL/PRESENTATION CONTEXT BINDING AUDIT PASS | "
                  f"source_pins={counts['source_pins']}/{counts['source_pins']} | "
                  f"profiles={counts['registered_profiles']}/{counts['registered_profiles']} | "
                  f"content_types={counts['supported_content_types']}/3 | shared_fields={counts['shared_fields']}/4 | "
                  f"reserved_fields={counts['reserved_fields']} | binding_output=IN_MEMORY_ONLY | "
                  "renderer_input=NOT_EMITTED | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
            return 0
        raw = json.loads(args.request.read_text(encoding="utf-8-sig"))
        record = build_context_binding(raw, args.project_root)
        # CLI stdout is a machine-readable JSON protocol. ASCII escaping prevents the
        # bytes emitted by Windows code pages from corrupting UTF-8 subprocess readers.
        print(json.dumps(record, ensure_ascii=True, indent=2, sort_keys=True))
        return 0
    except Exception as exc:
        print(f"C11-D SHARED EDITORIAL/PRESENTATION CONTEXT BINDING FAIL | {exc} | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
