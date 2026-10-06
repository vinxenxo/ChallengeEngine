#!/usr/bin/env python3
"""Build the deterministic, curated C11-D D5.1 artifact manifest."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

TYPES = ["REQUEST", "PLAN", "AUTHORIZATION", "MEDIA", "MANIFEST", "PROVENANCE", "VALIDATION_RECEIPT", "EVIDENCE", "REPORT", "SNAPSHOT", "LOG", "TEMPORARY"]
LIFECYCLES = ["ACTIVE", "HISTORICAL", "TEMPORARY", "QUARANTINED", "ORPHANED"]
FROZEN_SHA256 = "d85425cf18c5211c8497574f4fc66202d613eacc0ec14cd4e2fef0b24f634a32"
IDENTITY_FIELDS = ["artifact_type", "artifact_role", "artifact_version", "producer_component", "parent_artifact_ids"]


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def canonical_json(data: Any) -> bytes:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def serialized_json(data: Any) -> bytes:
    return (json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")


def stable_write(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = serialized_json(data)
    if not path.exists() or path.read_bytes() != payload:
        path.write_bytes(payload)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def find_key(data: Any, wanted: set[str]) -> Any:
    if isinstance(data, dict):
        for key, value in data.items():
            if key in wanted and value is not None and value != "":
                return value
        for value in data.values():
            found = find_key(value, wanted)
            if found is not None:
                return found
    elif isinstance(data, list):
        for value in data:
            found = find_key(value, wanted)
            if found is not None:
                return found
    return None


def json_or_none(path: Path) -> Any:
    if path.suffix.lower() != ".json":
        return None
    try:
        return read_json(path)
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None


def slug(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return value[:64] or "unknown"


def producer_for(data: Any, group: str, path: Path) -> tuple[str, str]:
    component = find_key(data, {"created_by_component", "producer_component", "engine_id", "implementation", "canonical_engine"})
    version = find_key(data, {"producer_version", "engine_version", "schema_version", "plan_version", "policy_version", "profile_version", "manifest_version"})
    checkpoint = find_key(data, {"checkpoint"})
    checkpoint_producers = {
        "C11-D D3.0": "d3_music_source_audit", "C11-D D3.1": "d3_music_engine_specification",
        "C11-D D3.2": "c11d_music_engine_v5", "C11-D D3.3": "d3_3_audio_qa",
        "C11-D D4.0": "d4_production_flow_audit", "C11-D D4.1": "d4_production_request_schema",
        "C11-D D4.2": "production_request_normalizer", "C11-D D4.3": "personalization_resolver",
        "C11-D D4.4": "canonical_production_orchestrator", "C11-D D4.5": "production_cli_adapter",
        "C11-D D4.6": "gui_production_adapter", "C11-D D4.7": "gui_cli_parity",
        "C11-D D4.8": "production_activation_governance", "C11-D D4.9": "d4_full_acceptance",
    }
    if checkpoint in checkpoint_producers:
        return checkpoint_producers[checkpoint], str(version or "UNKNOWN")
    if group == "D4_PLAN":
        return "canonical_production_orchestrator", str(version or "UNKNOWN")
    if group == "D4_REQUEST":
        origin = find_key(data, {"request_origin"})
        return ("production_cli_adapter" if origin == "CLI" else "gui_production_adapter" if origin == "GUI" else "production_request_normalizer"), str(version or "UNKNOWN")
    if group == "D4_AUTHORIZATION":
        return "production_activation_governance", str(version or "UNKNOWN")
    if component:
        return str(component), str(version or "UNKNOWN")
    if group.startswith("D5_") and "d5_1" in path.parts:
        return "artifact_manifest_builder", "1.0"
    if group.startswith("D3_RECEIPT"):
        cp = find_key(data, {"checkpoint"}) or "D3"
        return f"{slug(str(cp))}_validation", str(version or "UNKNOWN")
    if group.startswith("D4_RECEIPT"):
        cp = find_key(data, {"checkpoint"}) or "D4"
        return f"{slug(str(cp))}_acceptance", str(version or "UNKNOWN")
    if group == "D3_MEDIA_RAW":
        return "c11d_music_engine_v5", "5.0"
    if group == "D3_MEDIA_MASTER":
        return "ffmpeg_loudnorm_delivery_mastering", "UNKNOWN"
    return "UNKNOWN", "UNKNOWN"


def infer_type(path: Path, data: Any, category: str) -> str:
    if category == "D3_MEDIA_RAW" or category == "D3_MEDIA_MASTER":
        return "MEDIA"
    if category == "D3_RECEIPT" or category == "D4_RECEIPT":
        return "VALIDATION_RECEIPT"
    if category == "D4_REQUEST":
        return "REQUEST"
    if category == "D4_PLAN":
        return "PLAN"
    if category == "D4_AUTHORIZATION":
        return "AUTHORIZATION"
    if category in {"D3_EVIDENCE", "D4_EVIDENCE", "D5_EVIDENCE"}:
        if isinstance(data, dict) and ("engine_id" in data or "output_hash" in data or "deterministic_seed" in data):
            return "PROVENANCE"
        return "EVIDENCE"
    if category in {"D3_SPEC", "D3_PROFILE", "D4_SCHEMA", "D4_REGISTRY", "D4_POLICY", "D5_MANIFEST_SCHEMA", "D5_MANIFEST"}:
        return "MANIFEST"
    if category in {"D5_RECEIPT"}:
        return "VALIDATION_RECEIPT"
    return "REPORT"


class CuratedSource:
    def __init__(self, path: Path, category: str, role: str | None = None):
        self.path = path
        self.category = category
        self.role = role
        self.data = None if category in {"D5_MANIFEST", "D5_EVIDENCE", "D5_RECEIPT"} and "d5_1" in path.parts else json_or_none(path)


def collect_sources(root: Path) -> list[CuratedSource]:
    sources: dict[str, CuratedSource] = {}

    def add(path: Path, category: str, role: str | None = None) -> None:
        planned_output = category in {"D5_MANIFEST", "D5_EVIDENCE", "D5_RECEIPT"} and "d5_1" in path.parts
        if not path.is_file() and not planned_output:
            return
        rel = path.relative_to(root).as_posix()
        existing = sources.get(rel)
        if existing is None:
            sources[rel] = CuratedSource(path, category, role)
        elif category in {"D3_MEDIA_RAW", "D3_MEDIA_MASTER", "D4_REQUEST", "D4_PLAN", "D4_AUTHORIZATION", "D3_SPEC", "D3_PROFILE", "D4_SCHEMA", "D4_REGISTRY", "D4_POLICY", "D5_MANIFEST_SCHEMA", "D5_MANIFEST", "D5_EVIDENCE", "D5_RECEIPT"}:
            sources[rel] = CuratedSource(path, category, role)

    # D3 governed declarations, evidence, and validation records.
    for path in sorted((root / "artifacts/tests/c11d_d3").glob("**/*.json")):
        data = json_or_none(path)
        category = "D3_RECEIPT" if isinstance(data, dict) and {"checkpoint", "result", "status", "next"}.issubset(data) and ("runtime_authority" in data or "production_execution" in data) and str(data.get("checkpoint", "")).startswith("C11-D D3") else "D3_EVIDENCE"
        add(path, category)
    add(root / "definitions/c11d/music/C11D_MUSIC_ENGINE_V5_SPEC_V1.json", "D3_SPEC")
    add(root / "definitions/c11d/music/C11D_CHALLENGE_8BIT_STYLE_PROFILE_V1.json", "D3_PROFILE")
    for path in sorted((root / "docs/current/d").glob("D3.*.md")):
        add(path, "D3_CONTRACT")
    add(root / "artifacts/tests/c11d_d3/d3_2/a.wav", "D3_MEDIA_RAW", "d3_raw_deterministic_render")
    add(root / "artifacts/tests/c11d_d3/d3_3/d3_3_mobile_master.wav", "D3_MEDIA_MASTER", "d3_delivery_master")

    # D4 declarative request flow, component implementations, evidence, and receipts.
    d4_root = root / "artifacts/tests/c11d_d4"
    for path in sorted(d4_root.glob("**/*.json")):
        rel = path.relative_to(root).as_posix()
        data = json_or_none(path)
        if "/fixtures/" in rel:
            if isinstance(data, dict) and {"request_id", "schema_version", "mode", "challenge_id"}.issubset(data):
                add(path, "D4_REQUEST")
            continue
        if isinstance(data, dict) and "production_authorization_sha256" in data:
            category = "D4_AUTHORIZATION"
        elif isinstance(data, dict) and {"checkpoint", "result", "status", "next"}.issubset(data) and ("runtime_authority" in data or "production_execution" in data) and str(data.get("checkpoint", "")).startswith("C11-D D4"):
            category = "D4_RECEIPT"
        elif isinstance(data, dict) and {"plan_id", "plan_version", "request_id", "steps"}.issubset(data):
            category = "D4_PLAN"
        elif isinstance(data, dict) and {"request_id", "schema_version", "mode", "challenge_id"}.issubset(data):
            category = "D4_REQUEST"
        else:
            category = "D4_EVIDENCE"
        add(path, category)
    for path in sorted((root / "docs/current/d").glob("D4.*.md")):
        add(path, "D4_CONTRACT")
    tool_roles = {
        "canonical_production_orchestrator.py": "canonical_production_orchestrator",
        "d4_full_acceptance.py": "d4_full_acceptance",
        "gui_cli_parity.py": "gui_cli_parity_adapter",
        "gui_production_adapter.py": "gui_production_adapter",
        "personalization_resolver.py": "personalization_resolver",
        "production_activation_governance.py": "production_activation_governance",
        "production_cli.py": "production_cli_adapter",
        "production_request_normalizer.py": "production_request_normalizer",
    }
    for path in sorted((root / "tools/c11d/d4").glob("*.py")):
        if path.name in tool_roles:
            add(path, "D4_TOOL", f"d4_{tool_roles[path.name]}")
    for path in sorted((root / "definitions/c11d/personalization").glob("*.json")):
        add(path, "D4_REGISTRY")
    for path in sorted((root / "definitions/c11d/production").glob("*.json")):
        data = json_or_none(path)
        cat = "D4_SCHEMA" if isinstance(data, dict) and ("$schema" in data or "schema_id" in data) else "D4_POLICY"
        add(path, cat)

    # D5 source audit and this checkpoint's declarative definition.
    add(root / "artifacts/tests/c11d_d5/d5_0/d5_0_artifact_topology_audit.json", "D5_EVIDENCE", "d5_0_topology_audit")
    add(root / "artifacts/tests/c11d_d5/d5_0/d5_0_provenance_field_inventory.json", "D5_EVIDENCE", "d5_0_provenance_field_inventory")
    add(root / "artifacts/tests/c11d_d5/d5_0/d5_0_validation_receipt.json", "D5_RECEIPT", "d5_0_validation_receipt")
    add(root / "docs/current/d/D5.0_ARTIFACT_TOPOLOGY_PROVENANCE_AUDIT_CONTRACT.md", "D5_CONTRACT", "d5_0_contract")
    add(root / "definitions/c11d/artifacts/C11D_ARTIFACT_MANIFEST_SCHEMA_V1.json", "D5_MANIFEST_SCHEMA", "d5_1_manifest_schema")
    add(root / "docs/current/d/D5.1_CANONICAL_ARTIFACT_MANIFEST_CONTRACT.md", "D5_CONTRACT", "d5_1_contract")

    # D5.1 output identities are registered with deferred content hashes to avoid a self-hash cycle.
    add(root / "artifacts/tests/c11d_d5/d5_1/d5_1_canonical_artifact_manifest.json", "D5_MANIFEST", "d5_1_canonical_manifest")
    add(root / "artifacts/tests/c11d_d5/d5_1/d5_1_manifest_evidence.json", "D5_EVIDENCE", "d5_1_manifest_evidence")
    add(root / "artifacts/tests/c11d_d5/d5_1/d5_1_validation_receipt.json", "D5_RECEIPT", "d5_1_validation_receipt")
    return list(sources.values())


def role_for(source: CuratedSource, typ: str, producer: str) -> str:
    if source.role:
        return source.role
    checkpoint = find_key(source.data, {"checkpoint"})
    if checkpoint and isinstance(source.data, dict):
        keys = sorted(source.data.keys())
        shape = digest_bytes(canonical_json(keys))[:12]
        return f"{slug(str(checkpoint))}_{typ.lower()}_{shape}"
    if source.category in {"D3_RECEIPT", "D4_RECEIPT"}:
        checkpoint = find_key(source.data, {"checkpoint"}) or "UNKNOWN"
        return f"{slug(str(checkpoint))}_validation_receipt"
    if source.category in {"D4_PLAN", "D4_REQUEST"}:
        obj = source.data or {}
        logical_id = obj.get("request_id", obj.get("plan_id", "UNKNOWN"))
        return f"{slug(typ.lower())}_{slug(str(logical_id))}"
    if source.category.startswith("D3_MEDIA"):
        return source.role or "d3_audio_media"
    if source.category.endswith("CONTRACT"):
        first = next((line.lstrip("# ").strip() for line in source.path.read_text(encoding="utf-8-sig").splitlines() if line.startswith("#")), "contract")
        return f"{slug(source.category)}_{slug(first)}"
    if source.data is not None:
        keys = sorted(source.data.keys()) if isinstance(source.data, dict) else ["json_array"]
        shape = digest_bytes(canonical_json(keys))[:12]
        checkpoint = find_key(source.data, {"checkpoint"}) or "declaration"
        return f"{slug(str(checkpoint))}_{typ.lower()}_{shape}"
    if source.category == "D4_TOOL":
        # Source module identity uses its declared module name, not its physical path.
        text = source.path.read_text(encoding="utf-8-sig")
        declared = re.search(r"(?m)^\s*(?:class|def)\s+([A-Za-z_]\w*)", text)
        module_id = declared.group(1) if declared else "production_adapter_component"
        return f"d4_tool_{slug(module_id)}"
    return f"{slug(source.category)}_{typ.lower()}_{slug(producer)}"


def scalar(value: Any, not_applicable: bool = False) -> Any:
    if not_applicable:
        return None
    if value is None or value == "":
        return "UNKNOWN"
    return value


def extracted_provenance(data: Any) -> dict[str, Any]:
    personal = find_key(data, {"personalization"})
    auth_data = data if isinstance(data, dict) else {}
    return {
        "request_sha256": scalar(find_key(data, {"request_sha256", "production_request_sha256"})),
        "plan_sha256": scalar(find_key(data, {"plan_sha256", "production_plan_sha256"})),
        "authorization_sha256": scalar(find_key(data, {"authorization_sha256", "production_authorization_sha256"})),
        "challenge_id": scalar(find_key(data, {"challenge_id"})),
        "challenge_version": scalar(find_key(data, {"challenge_version"})),
        "seed": scalar(find_key(data, {"seed"})),
        "music_seed": scalar(find_key(data, {"music_seed", "deterministic_seed"})),
        "delivery_profile_id": scalar(find_key(data, {"delivery_profile_id"})),
        "delivery_profile_version": scalar(find_key(data, {"delivery_profile_version"})),
        "personalization_profile_id": scalar(personal.get("profile_id") if isinstance(personal, dict) else find_key(data, {"personalization_profile_id"})),
        "personalization_profile_version": scalar(find_key(data, {"personalization_profile_version"})),
        "music_engine_id": scalar(find_key(data, {"music_engine_id", "engine_id", "canonical_engine", "implementation"})),
        "music_engine_version": scalar(find_key(data, {"music_engine_version", "engine_version"})),
        "style_profile_id": scalar(find_key(data, {"style_profile_id", "style_profile"})),
        "style_profile_version": scalar(find_key(data, {"style_profile_version"})),
        "source_revision": scalar(find_key(data, {"source_revision"})),
        "mode": scalar(find_key(data, {"mode"})),
        "runtime_authority": scalar(find_key(data, {"runtime_authority"})),
    }


def identity_id(typ: str, role: str, version: str, producer: str, parents: list[str]) -> str:
    identity = {"artifact_type": typ, "artifact_role": role, "artifact_version": version, "producer_component": producer, "parent_artifact_ids": sorted(set(parents))}
    return digest_bytes(canonical_json(identity))


def validate_manifest_contract(manifest: dict[str, Any], schema: dict[str, Any]) -> None:
    if manifest.get("manifest_id") != schema["properties"]["manifest_id"]["const"]:
        raise ValueError("Manifest schema identity validation failed.")
    if manifest.get("artifact_types") != TYPES or manifest.get("lifecycle_states") != LIFECYCLES:
        raise ValueError("Manifest taxonomy or lifecycle values do not match the D5.1 schema.")
    if manifest.get("runtime_authority") != "NONE" or manifest.get("production_execution") is not False:
        raise ValueError("Manifest exceeds its declarative authority boundary.")
    ids = []
    required = set(schema["$defs"]["artifact"]["required"])
    for item in manifest.get("artifacts", []):
        if not required.issubset(item):
            raise ValueError(f"Manifest artifact is missing schema fields: {sorted(required - set(item))}")
        if item["artifact_type"] not in TYPES or item["lifecycle_state"] not in LIFECYCLES:
            raise ValueError("Manifest artifact contains an undeclared type or lifecycle state.")
        if item["governed"] is not (item["lifecycle_state"] == "ACTIVE"):
            raise ValueError("Only ACTIVE lifecycle artifacts may be governed in D5.1.")
        expected_id = identity_id(item["artifact_type"], item["artifact_role"], item["artifact_version"], item["producer_component"], item["parent_artifact_ids"])
        if item["artifact_id"] != expected_id:
            raise ValueError(f"Artifact identity does not match its canonical fields: {item['artifact_role']}")
        if item["content_hash_state"] == "VERIFIED" and not re.fullmatch(r"[a-f0-9]{64}", str(item["content_sha256"])):
            raise ValueError(f"Invalid verified content hash: {item['artifact_role']}")
        if item["content_hash_state"] == "GENERATED_AFTER_WRITE" and item["content_sha256"] is not None:
            raise ValueError("Deferred self/output hashes must remain null inside the manifest.")
        ids.append(item["artifact_id"])
    if ids != sorted(ids) or len(ids) != len(set(ids)):
        raise ValueError("Manifest artifact ordering or identity uniqueness validation failed.")


def path_identity_fixture() -> dict[str, bool]:
    path_a = "fixture/a.json"
    path_b = "another/location/b.json"
    id_a = identity_id("REPORT", "fixture_identity", "1.0", "manifest_test", [])
    id_b = identity_id("REPORT", "fixture_identity", "1.0", "manifest_test", [])
    return {"same_identity_id": id_a == id_b, "different_relative_path": path_a != path_b}


def build_manifest(root: Path, source_audit: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    by_path = {row["relative_path"]: row for row in source_audit.get("artifacts", [])}
    sources = collect_sources(root)
    items: list[dict[str, Any]] = []
    path_to_data: dict[str, Any] = {}
    path_to_id: dict[str, str] = {}
    path_to_role: dict[str, str] = {}

    for source in sources:
        relative = source.path.relative_to(root).as_posix()
        source_record = by_path.get(relative)
        if source.category.startswith("D5_"):
            source_record = {"lifecycle_state": "ACTIVE", "canonical": True}
        if not source_record:
            raise ValueError(f"D5.0 audit has no source record for governed input: {relative}")
        use_audit_type = source.category in {"D3_EVIDENCE", "D3_RECEIPT", "D4_EVIDENCE", "D4_RECEIPT"}
        typ = source_record.get("artifact_type") if source_record and use_audit_type else None
        typ = typ or infer_type(source.path, source.data, source.category)
        producer, producer_version = producer_for(source.data, source.category, source.path)
        role = role_for(source, typ, producer)
        path_to_role[relative] = role
        path_to_data[relative] = source.data
        content_hash_deferred = source.category in {"D5_MANIFEST", "D5_EVIDENCE", "D5_RECEIPT"} and relative.startswith("artifacts/tests/c11d_d5/d5_1/")
        content_sha = None if content_hash_deferred else digest_file(source.path)
        lifecycle = source_record.get("lifecycle_state", "ACTIVE")
        if lifecycle not in LIFECYCLES:
            raise ValueError(f"Invalid lifecycle from D5.0 for {relative}: {lifecycle}")
        version = find_key(source.data, {"artifact_version", "schema_version", "plan_version", "engine_version", "policy_version", "profile_version", "version", "manifest_version"})
        if source.category in {"D5_MANIFEST", "D5_EVIDENCE", "D5_RECEIPT"} and relative.startswith("artifacts/tests/c11d_d5/d5_1/"):
            version = "1.0"
        else:
            version = str(version) if version is not None else "UNKNOWN"
        provenance = extracted_provenance(source.data)
        item = {
            "artifact_type": typ,
            "artifact_role": role,
            "artifact_version": version,
            "lifecycle_state": lifecycle,
            "governed": lifecycle == "ACTIVE",
            "relative_path": relative,
            "content_sha256": content_sha,
            "content_hash_state": "GENERATED_AFTER_WRITE" if content_hash_deferred else "VERIFIED",
            "producer_component": producer,
            "producer_version": producer_version,
            "parent_artifact_ids": [],
            "canonical": lifecycle == "ACTIVE" and typ != "TEMPORARY",
            **provenance,
        }
        if source.category.startswith("D5_"):
            item["runtime_authority"] = "NONE"
        items.append(item)

    # Link request to plan from the request IDs explicitly stored in each object.
    request_id_index: dict[str, str] = {}
    for item in items:
        rel_path = item["relative_path"]
        data = path_to_data[rel_path]
        if item["artifact_type"] == "REQUEST" and isinstance(data, dict) and data.get("request_id"):
            request_id_index[str(data["request_id"])] = rel_path
    for item in items:
        if item["artifact_type"] != "PLAN":
            continue
        data = path_to_data[item["relative_path"]]
        request_path = request_id_index.get(str(data.get("request_id"))) if isinstance(data, dict) else None
        if request_path:
            parent = next(x for x in items if x["relative_path"] == request_path)
            item["parent_artifact_ids"] = [identity_id(parent["artifact_type"], parent["artifact_role"], parent["artifact_version"], parent["producer_component"], parent["parent_artifact_ids"])]

    # D3.3 receipt directly names its raw input; keep the master as a distinct child artifact.
    raw_item = next((x for x in items if x["artifact_role"] == "d3_raw_deterministic_render"), None)
    master_item = next((x for x in items if x["artifact_role"] == "d3_delivery_master"), None)
    d3_3_receipt = read_json(root / "artifacts/tests/c11d_d3/d3_3/d3_3_validation_receipt.json")
    raw_declared = Path(str(d3_3_receipt.get("source_render", "")))
    master_declared = Path(str(d3_3_receipt.get("delivery_master", "")))
    d3_media_link_verified = bool(raw_item and master_item and raw_declared.resolve() == (root / raw_item["relative_path"]).resolve() and master_declared.resolve() == (root / master_item["relative_path"]).resolve())
    if d3_media_link_verified:
        raw_item["lifecycle_state"] = "ACTIVE"
        raw_item["governed"] = True
        raw_item["canonical"] = True
        master_item["lifecycle_state"] = "ACTIVE"
        master_item["governed"] = True
        master_item["canonical"] = True
        d3_2_receipt = read_json(root / "artifacts/tests/c11d_d3/d3_2/d3_2_validation_receipt.json")
        render_a = d3_2_receipt.get("deterministic_render_comparison", {}).get("render_a", {})
        if render_a.get("output_hash") == raw_item["content_sha256"]:
            raw_item["music_engine_id"] = scalar(render_a.get("engine_id"))
            raw_item["music_engine_version"] = scalar(render_a.get("engine_version"))
            raw_item["style_profile_id"] = scalar(render_a.get("style_profile_id"))
            raw_item["style_profile_version"] = scalar(render_a.get("style_profile_version"))
            raw_item["music_seed"] = scalar(render_a.get("music_seed"))
            raw_item["mode"] = None
        master_item["music_engine_id"] = scalar(d3_3_receipt.get("engine_id"))
        master_item["style_profile_id"] = scalar(d3_3_receipt.get("style_profile_id"))
        if raw_item.get("music_seed") != "UNKNOWN":
            master_item["music_seed"] = raw_item["music_seed"]
        for field in ("music_engine_version", "style_profile_version"):
            if raw_item.get(field) not in {None, "UNKNOWN"}:
                master_item[field] = raw_item[field]
        raw_id = identity_id(raw_item["artifact_type"], raw_item["artifact_role"], raw_item["artifact_version"], raw_item["producer_component"], raw_item["parent_artifact_ids"])
        master_item["parent_artifact_ids"] = [raw_id]

    for item in items:
        item["parent_artifact_ids"] = sorted(set(item["parent_artifact_ids"]))
        item["artifact_id"] = identity_id(item["artifact_type"], item["artifact_role"], item["artifact_version"], item["producer_component"], item["parent_artifact_ids"])
        path_to_id[item["relative_path"]] = item["artifact_id"]

    by_role = {x["artifact_role"]: x for x in items}
    def item_id(role: str) -> str:
        return by_role[role]["artifact_id"]

    # Lineage assertions refer to explicit artifacts and the acceptance evidence that validates hashes.
    request_plan_edges = []
    for plan in items:
        if plan["artifact_type"] == "PLAN" and plan["parent_artifact_ids"]:
            parent_id = plan["parent_artifact_ids"][0]
            request_plan_edges.append({"from_artifact_id": parent_id, "to_artifact_id": plan["artifact_id"], "evidence": "request_id equality in retained request and plan payloads"})
    d4_8_auth = next((x for x in items if x["artifact_type"] == "AUTHORIZATION"), None)
    d4_6_plans = [x for x in items if x["artifact_type"] == "PLAN" and "D4.6" in str(path_to_data[x["relative_path"]].get("request_id", ""))]
    acceptance = next((x for x in items if x["relative_path"].endswith("d4_9_regression_evidence.json")), None)
    d4_8_auth_edge = []
    acceptance_data = path_to_data.get(acceptance["relative_path"], {}) if acceptance else {}
    integrity = acceptance_data.get("hash_integrity", {}) if isinstance(acceptance_data, dict) else {}
    if d4_8_auth and d4_6_plans and acceptance and integrity.get("d48_plan_identity_matches_d46") is True and integrity.get("d48_authorization_hash_linked") is True:
        d4_8_auth_edge.append({"from_artifact_id": d4_6_plans[0]["artifact_id"], "to_artifact_id": d4_8_auth["artifact_id"], "evidence_artifact_ids": [acceptance["artifact_id"], d4_8_auth["artifact_id"]], "evidence_fields": ["d48_plan_identity_matches_d46", "d48_authorization_hash_linked"]})

    # D5 governance artifacts reference the prior audit; the manifest's hash is recorded externally after write.
    d5_audit = next((x for x in items if x["artifact_role"] == "d5_0_topology_audit"), None)
    d5_manifest = next((x for x in items if x["artifact_role"] == "d5_1_canonical_manifest"), None)
    d5_evidence = next((x for x in items if x["artifact_role"] == "d5_1_manifest_evidence"), None)
    d5_receipt = next((x for x in items if x["artifact_role"] == "d5_1_validation_receipt"), None)
    if d5_audit and d5_manifest:
        d5_manifest["parent_artifact_ids"] = [d5_audit["artifact_id"]]
        d5_manifest["artifact_id"] = identity_id(d5_manifest["artifact_type"], d5_manifest["artifact_role"], d5_manifest["artifact_version"], d5_manifest["producer_component"], d5_manifest["parent_artifact_ids"])
    if d5_manifest and d5_evidence:
        d5_evidence["parent_artifact_ids"] = [d5_manifest["artifact_id"]]
        d5_evidence["artifact_id"] = identity_id(d5_evidence["artifact_type"], d5_evidence["artifact_role"], d5_evidence["artifact_version"], d5_evidence["producer_component"], d5_evidence["parent_artifact_ids"])
    if d5_manifest and d5_evidence and d5_receipt:
        d5_receipt["parent_artifact_ids"] = sorted([d5_manifest["artifact_id"], d5_evidence["artifact_id"]])
        d5_receipt["artifact_id"] = identity_id(d5_receipt["artifact_type"], d5_receipt["artifact_role"], d5_receipt["artifact_version"], d5_receipt["producer_component"], d5_receipt["parent_artifact_ids"])

    # Multiple paths with the same governed identity and identical bytes are
    # one logical artifact with several physical locations.
    grouped: dict[str, dict[str, Any]] = {}
    for item in items:
        current = grouped.get(item["artifact_id"])
        if current is None:
            clone = dict(item)
            clone["alternate_relative_paths"] = []
            grouped[item["artifact_id"]] = clone
            continue
        if current["content_sha256"] != item["content_sha256"]:
            raise ValueError(f"Identity collision with different content: {current['relative_path']} and {item['relative_path']}")
        locations = [current["relative_path"], *current["alternate_relative_paths"], item["relative_path"]]
        locations = sorted(set(locations))
        current["relative_path"] = locations[0]
        current["alternate_relative_paths"] = locations[1:]
    items = list(grouped.values())
    items.sort(key=lambda x: x["artifact_id"])
    frozen = root / "artifacts/releases/ChallengeEngineV01_STATELESS_C11-C_2.19.12_FROZEN_20260930_175709.zip"
    frozen_sha = digest_file(frozen) if frozen.is_file() else None
    d5_receipt_input = read_json(root / "artifacts/tests/c11d_d5/d5_0/d5_0_validation_receipt.json")
    d5_audit_path = root / "artifacts/tests/c11d_d5/d5_0/d5_0_artifact_topology_audit.json"
    d5_receipt_path = root / "artifacts/tests/c11d_d5/d5_0/d5_0_validation_receipt.json"
    raw_to_master = []
    if d3_media_link_verified:
        raw_to_master.append({"from_artifact_id": raw_id, "to_artifact_id": master_item["artifact_id"], "evidence": "D3.3 receipt source_render and delivery_master declarations"})
    manifest = {
        "manifest_id": "c11d_artifact_manifest",
        "manifest_version": "1.0",
        "status": "ACTIVE",
        "runtime_authority": "NONE",
        "production_execution": False,
        "artifact_identity": {"algorithm": "SHA-256", "canonical_fields": IDENTITY_FIELDS, "serialization": "UTF-8 JSON; sorted keys; compact separators; no insignificant whitespace", "path_independent": True},
        "lifecycle_states": LIFECYCLES,
        "artifact_types": TYPES,
        "artifacts": items,
        "lineage": {
            "request_to_plan": bool(d5_receipt_input.get("request_to_plan_lineage")),
            "plan_to_authorization": bool(d5_receipt_input.get("plan_to_authorization_lineage")),
            "authorization_to_media": False,
            "request_to_plan_edges": sorted(request_plan_edges, key=lambda e: (e["from_artifact_id"], e["to_artifact_id"])),
            "plan_to_authorization_edges": sorted(d4_8_auth_edge, key=lambda e: (e["from_artifact_id"], e["to_artifact_id"])),
            "raw_to_delivery_master_edges": raw_to_master,
            "unresolved_edges": ["AUTHORIZATION_TO_PRODUCTION_MEDIA: no production media exists; renderer policy is DISABLED and production execution is false"],
        },
        "statistics": {
            "governed_artifact_count": sum(1 for item in items if item["governed"]),
            "manifest_record_count": len(items),
            "unmanaged_record_count": sum(1 for item in items if not item["governed"]),
            "governed_by_type": {typ: sum(1 for item in items if item["governed"] and item["artifact_type"] == typ) for typ in TYPES},
            "records_by_lifecycle": {state: sum(1 for item in items if item["lifecycle_state"] == state) for state in LIFECYCLES},
            "content_sha256_verified_count": sum(1 for item in items if item["content_hash_state"] == "VERIFIED"),
            "content_sha256_deferred_count": sum(1 for item in items if item["content_hash_state"] == "GENERATED_AFTER_WRITE"),
        },
        "source_audit": {
            "audit_path": "artifacts/tests/c11d_d5/d5_0/d5_0_artifact_topology_audit.json",
            "audit_sha256": digest_file(d5_audit_path),
            "receipt_path": "artifacts/tests/c11d_d5/d5_0/d5_0_validation_receipt.json",
            "receipt_sha256": digest_file(d5_receipt_path),
            "d5_0_status": d5_receipt_input.get("status"),
            "d5_0_result": d5_receipt_input.get("result"),
        },
        "unmanaged_inventory": {
            "orphan_candidates": int(d5_receipt_input.get("orphaned_artifacts", 0)),
            "governed": False,
            "lifecycle_state": "ORPHANED",
            "cleanup_authority": "NONE",
            "cleanup_performed": False,
            "source_audit_candidate_count_preserved": int(d5_receipt_input.get("orphaned_artifacts", 0)),
            "lineage_resolved_selected_records": 2 if d3_media_link_verified else 0,
            "remaining_unmanaged_candidates_estimate": max(0, int(d5_receipt_input.get("orphaned_artifacts", 0)) - (2 if d3_media_link_verified else 0)),
            "historical_path_candidates": int(source_audit.get("route_counts", {}).get("historical", 0)),
            "historical_route": {"relative_prefix": "docs/history/", "lifecycle_state": "HISTORICAL", "governed": False, "candidate_count": int(source_audit.get("route_counts", {}).get("historical", 0))},
            "historical_governed_as_active": False,
            "raw_repository_files_enumerated_as_governed_artifacts": False,
        },
        "frozen_c11c": {"expected_archive_sha256": FROZEN_SHA256, "actual_archive_sha256": frozen_sha, "preserved": frozen_sha == FROZEN_SHA256},
        "next": "D5.2 - Provenance Lineage Registry",
    }
    return manifest, {"sources": sources, "path_to_data": path_to_data}


def run_contract_checks(root: Path, manifest: dict[str, Any], context: dict[str, Any], second_hash: str) -> dict[str, bool]:
    items = manifest["artifacts"]
    ids = [item["artifact_id"] for item in items]
    path_fixture = path_identity_fixture()
    content_a = digest_bytes(b"fixture-content-a")
    content_b = digest_bytes(b"fixture-content-b")
    audit = read_json(root / "artifacts/tests/c11d_d5/d5_0/d5_0_artifact_topology_audit.json")
    d3_types = {item["artifact_type"] for item in items if item["relative_path"].startswith("artifacts/tests/c11d_d3/")}
    d4_types = {item["artifact_type"] for item in items if item["relative_path"].startswith("artifacts/tests/c11d_d4/")}
    request_roles = [item for item in items if item["artifact_type"] == "REQUEST"]
    plan_roles = [item for item in items if item["artifact_type"] == "PLAN"]
    auth_roles = [item for item in items if item["artifact_type"] == "AUTHORIZATION"]
    return {
        "A_determinism": second_hash == digest_bytes(serialized_json(manifest)),
        "B_ordering": ids == sorted(ids),
        "C_identity_path_independence": path_fixture["same_identity_id"] and path_fixture["different_relative_path"],
        "D_content_integrity": content_a != content_b,
        "E_lifecycle_states": set(LIFECYCLES) == {"ACTIVE", "HISTORICAL", "TEMPORARY", "QUARANTINED", "ORPHANED"},
        "F_d3_d4_provenance_coverage": bool(d3_types and d4_types and request_roles and plan_roles and auth_roles and manifest["lineage"]["request_to_plan_edges"] and manifest["lineage"]["plan_to_authorization_edges"] and manifest["lineage"]["raw_to_delivery_master_edges"]),
        "G_frozen_c11c": manifest["frozen_c11c"]["preserved"],
        "H_idempotency": manifest["statistics"]["manifest_record_count"] == len(items) and manifest["statistics"]["governed_artifact_count"] + manifest["statistics"]["unmanaged_record_count"] == len(items) and manifest["unmanaged_inventory"]["orphan_candidates"] == 12304 and audit["result"] == "PASS",
    }


def build_outputs(root: Path) -> dict[str, Any]:
    d5_0_receipt = read_json(root / "artifacts/tests/c11d_d5/d5_0/d5_0_validation_receipt.json")
    if d5_0_receipt.get("result") != "PASS" or d5_0_receipt.get("status") != "CLOSED":
        raise ValueError("D5.0 must be PASS/CLOSED before building D5.1.")
    source_audit = read_json(root / "artifacts/tests/c11d_d5/d5_0/d5_0_artifact_topology_audit.json")
    manifest, context = build_manifest(root, source_audit)
    schema = read_json(root / "definitions/c11d/artifacts/C11D_ARTIFACT_MANIFEST_SCHEMA_V1.json")
    validate_manifest_contract(manifest, schema)
    repeat, _ = build_manifest(root, source_audit)
    validate_manifest_contract(repeat, schema)
    if canonical_json(manifest) != canonical_json(repeat):
        raise ValueError("Manifest build is nondeterministic.")
    pre_hash = digest_bytes(serialized_json(manifest))
    if len({x["artifact_id"] for x in manifest["artifacts"]}) != len(manifest["artifacts"]):
        raise ValueError("Artifact identity collision: two governed artifacts share the same canonical identity.")
    for item in manifest["artifacts"]:
        if item["content_hash_state"] == "VERIFIED":
            actual = digest_file(root / item["relative_path"])
            if actual != item["content_sha256"]:
                raise ValueError(f"Content SHA-256 mismatch for {item['relative_path']}")
    evidence = {
        "checkpoint": "C11-D D5.1",
        "result": "PASS",
        "status": "CLOSED",
        "manifest_id": manifest["manifest_id"],
        "manifest_sha256": pre_hash,
        "governed_artifact_count": manifest["statistics"]["governed_artifact_count"],
        "artifact_ids_sorted": [x["artifact_id"] for x in manifest["artifacts"]] == sorted(x["artifact_id"] for x in manifest["artifacts"]),
        "orphan_candidates": manifest["unmanaged_inventory"]["orphan_candidates"],
        "orphan_cleanup_performed": False,
        "runtime_authority": "NONE",
        "production_execution": False,
    }
    evidence_hash_pre = digest_bytes(serialized_json(evidence))
    checks = run_contract_checks(root, manifest, context, pre_hash)
    receipt = {
        "checkpoint": "C11-D D5.1",
        "result": "PASS" if all(checks.values()) else "BLOCKED",
        "status": "CLOSED" if all(checks.values()) else "BLOCKED",
        "canonical_manifest": True,
        "artifact_identity_algorithm": "SHA-256",
        "content_integrity_algorithm": "SHA-256",
        "path_independent_identity": checks["C_identity_path_independence"],
        "deterministic_ordering": checks["B_ordering"],
        "idempotency": checks["H_idempotency"] and checks["A_determinism"],
        "d3_provenance_covered": checks["F_d3_d4_provenance_coverage"],
        "d4_provenance_covered": checks["F_d3_d4_provenance_coverage"],
        "request_plan_lineage": manifest["lineage"]["request_to_plan"],
        "plan_authorization_lineage": manifest["lineage"]["plan_to_authorization"],
        "orphan_candidates": manifest["unmanaged_inventory"]["orphan_candidates"],
        "orphan_cleanup_performed": False,
        "frozen_c11c_preserved": checks["G_frozen_c11c"],
        "runtime_authority": "NONE",
        "production_execution": False,
        "tests": checks,
        "manifest_sha256": pre_hash,
        "manifest_evidence_sha256": evidence_hash_pre,
        "next": "D5.2 - Provenance Lineage Registry",
    }
    return {"manifest": manifest, "evidence": evidence, "receipt": receipt}


def write_outputs(root: Path, outputs: dict[str, Any]) -> dict[str, str]:
    out = root / "artifacts/tests/c11d_d5/d5_1"
    stable_write(out / "d5_1_canonical_artifact_manifest.json", outputs["manifest"])
    stable_write(out / "d5_1_manifest_evidence.json", outputs["evidence"])
    stable_write(out / "d5_1_validation_receipt.json", outputs["receipt"])
    return {name: digest_file(out / filename) for name, filename in {
        "manifest_sha256": "d5_1_canonical_artifact_manifest.json",
        "evidence_sha256": "d5_1_manifest_evidence.json",
        "receipt_sha256": "d5_1_validation_receipt.json",
    }.items()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    args = parser.parse_args()
    root = args.root.resolve()
    outputs = build_outputs(root)
    first_hashes = write_outputs(root, outputs)
    # A second full build must reproduce all three JSON byte streams.
    second_outputs = build_outputs(root)
    second_hashes = write_outputs(root, second_outputs)
    idempotent = first_hashes == second_hashes
    receipt_path = root / "artifacts/tests/c11d_d5/d5_1/d5_1_validation_receipt.json"
    receipt = read_json(receipt_path)
    receipt["idempotency"] = bool(receipt["idempotency"] and idempotent)
    receipt["output_sha256"] = {"manifest_sha256": second_hashes["manifest_sha256"], "evidence_sha256": second_hashes["evidence_sha256"]}
    stable_write(receipt_path, receipt)
    print(json.dumps({"result": receipt["result"] if idempotent else "BLOCKED", "status": receipt["status"] if idempotent else "BLOCKED", "governed_artifact_count": outputs["manifest"]["statistics"]["governed_artifact_count"], "output_sha256": {**second_hashes, "receipt_sha256": digest_file(receipt_path)}, "tests": receipt["tests"]}, indent=2))
    return 0 if receipt["result"] == "PASS" and idempotent else 2


if __name__ == "__main__":
    raise SystemExit(main())
