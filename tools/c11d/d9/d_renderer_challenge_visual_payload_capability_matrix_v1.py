"""Static source/capability inventory for the planned Challenge visual materializer V2-A.

This audit does not invoke Godot, create payloads, touch runtime behavior, or grant renderer authority.
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path
from typing import Any, Mapping

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_CAPABILITY_MATRIX_V1.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_CAPABILITY_MATRIX_SCHEMA_V1.json")
REPORT_SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_CAPABILITY_MATRIX_REPORT_SCHEMA_V1.json")
MANIFEST_REL = Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")
FROZEN_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
CONTRACT_ID = "C11-D-RENDERER-CHALLENGE-VISUAL-PAYLOAD-CAPABILITY-MATRIX-CONTRACT-V1"
REPORT_ID = "C11-D-RENDERER-CHALLENGE-VISUAL-PAYLOAD-CAPABILITY-MATRIX-REPORT-V1"
STATUS = "PREPARATION_ONLY_STATIC_CAPABILITY_INVENTORY_NOT_PAYLOAD_MATERIALIZATION"
EXPECTED_IDS = [f"CHALLENGE_{i:03d}" for i in range(1, 10)]
PHASE_KEYS = ("hook_duration", "game_duration", "reveal_duration", "cta_duration")
ASSET_KEYS = {"BACKGROUND": "background_path", "TARGET": "target_path", "ANIMATED_OBJECT": "object_path"}

class CapabilityMatrixError(ValueError):
    """Raised when source lineage, selector coverage or governance constraints fail closed."""

def sha256_bytes(data: bytes) -> str: return hashlib.sha256(data).hexdigest()
def sha256_file(path: Path) -> str: return sha256_bytes(path.read_bytes())
def sha256_json(value: Any) -> str:
    return sha256_bytes(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8"))
def project_root() -> Path: return Path(__file__).resolve().parents[3]
def read_json(path: Path) -> dict[str, Any]:
    try: value = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc: raise CapabilityMatrixError(f"Cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict): raise CapabilityMatrixError(f"Expected JSON object at {path}")
    return value

def asset_bindings(source: Mapping[str, Any]) -> dict[str, str]:
    assets = source.get("assets", {})
    if not isinstance(assets, Mapping): raise CapabilityMatrixError("Challenge assets must be an object")
    result = {}
    for role, field in ASSET_KEYS.items():
        if field in assets:
            value = assets[field]
            if not isinstance(value, str) or not value.startswith("res://"):
                raise CapabilityMatrixError(f"Asset binding {field} must be a res:// path")
            result[role] = value.removeprefix("res://")
    if set(result) != set(ASSET_KEYS): raise CapabilityMatrixError("Every selector must define the three expected asset role references")
    return result

def custom_data_keys(source_text: str) -> list[str]:
    found: set[str] = set()
    for match in re.finditer(r"(?:snapshot|snap)\.custom_data\s*=\s*\{([^}]*)\}", source_text, re.S):
        found.update(re.findall(r'"([A-Za-z0-9_]+)"\s*:', match.group(1)))
    return sorted(found)

def registry_routes(registry_text: str) -> dict[str, str]:
    routes = {}
    for match in re.finditer(r'"([a-z0-9_]+)"\s*:\s*\n?\s*return\s+([A-Za-z0-9_]+)\.new\(\)', registry_text):
        routes[match.group(1)] = match.group(2)
    return routes

def validate_governance(contract: Mapping[str, Any]) -> None:
    expected_locks = {"renderer":"OFF", "media_created":False,"candidate_input_admissible":False,"seed_domains_complete_for_candidate_input":False,"automatic_seed_generation":False,"master_seed_adopted":False,"d4_8":"BLOCKED","d9_10":"PREPARE_ONLY","d9_17":"BLOCKED_NO_GO","d10":"BLOCKED_FOR_PROMOTION","release_authority":"NONE","source_mutation":False,"godot_invocations_by_this_preflight":0,"payload_materialized":False,"payload_files_written":False,"renderer_native_input_emitted":False,"renderer_dispatch_invoked":False,"media_output_created":False}
    if contract.get("governance_locks") != expected_locks: raise CapabilityMatrixError("Governance lock mismatch")
    if contract.get("status") != STATUS: raise CapabilityMatrixError("Contract may not self-promote")
    if contract.get("capability_policy", {}).get("scope") != "STATIC_SOURCE_CAPABILITY_AND_LINEAGE_ONLY": raise CapabilityMatrixError("Capability scope must remain static-only")
    if contract.get("custom_data_semantics", {}).get("status") != "UNMAPPED_REQUIRES_SELECTOR_SPECIFIC_SEMANTIC_REVIEW": raise CapabilityMatrixError("custom_data mapping cannot be marked approved")

def _load_contract(root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    contract, schema, report_schema = (read_json(root / rel) for rel in (CONTRACT_REL, SCHEMA_REL, REPORT_SCHEMA_REL))
    if contract.get("schema") != CONTRACT_ID or contract.get("schema_version") != "1.0": raise CapabilityMatrixError("Contract identity/version mismatch")
    if schema.get("$id") != "urn:c11d:challenge-visual-payload-capability-matrix-contract:v1" or schema.get("additionalProperties") is not False: raise CapabilityMatrixError("Contract schema identity/strictness mismatch")
    if report_schema.get("$id") != "urn:c11d:challenge-visual-payload-capability-matrix-report:v1" or report_schema.get("additionalProperties") is not False: raise CapabilityMatrixError("Report schema identity/strictness mismatch")
    if contract.get("source_authority", {}).get("frozen_c11c_manifest_sha256") != FROZEN_MANIFEST_SHA256: raise CapabilityMatrixError("Frozen manifest contract pin mismatch")
    if sha256_file(root / MANIFEST_REL) != FROZEN_MANIFEST_SHA256: raise CapabilityMatrixError("Frozen C11-C manifest changed")
    validate_governance(contract)
    return contract, schema, report_schema

def validate_source_pins(root: Path | None = None, contract_override: Mapping[str, Any] | None = None) -> dict[str, int]:
    root = root or project_root()
    contract = dict(contract_override) if contract_override is not None else _load_contract(root)[0]
    pins = contract.get("pinned_sources")
    if not isinstance(pins, list) or len(pins) != 43: raise CapabilityMatrixError("Expected 43 immutable source/asset pins")
    seen: set[str] = set()
    for item in pins:
        if not isinstance(item, Mapping): raise CapabilityMatrixError("Malformed source pin")
        rel = str(item.get("path", "")); digest = item.get("sha256")
        path_obj = Path(rel)
        if not rel or path_obj.is_absolute() or ".." in path_obj.parts or rel in seen: raise CapabilityMatrixError(f"Unsafe/duplicate source pin path: {rel}")
        seen.add(rel)
        if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None: raise CapabilityMatrixError(f"Invalid SHA-256 pin: {rel}")
        path = root / path_obj
        if not path.is_file(): raise CapabilityMatrixError(f"Pinned source missing: {rel}")
        if sha256_file(path) != digest: raise CapabilityMatrixError(f"Pinned source hash mismatch: {rel}")
    if source_pin(root, contract, "release/C11C_FREEZE_PACKAGE_MANIFEST.json") != FROZEN_MANIFEST_SHA256: raise CapabilityMatrixError("Manifest source pin mismatch")
    return {"source_pins": len(pins), "challenge_source_pins": 9, "runtime_contract_pins": 4, "unique_asset_pins": len([p for p in pins if str(p.get("path", "")).startswith("assets/")])}

def source_pin(root: Path, contract: Mapping[str, Any], rel: str) -> str:
    for item in contract.get("pinned_sources", []):
        if item.get("path") == rel: return str(item.get("sha256", ""))
    raise CapabilityMatrixError(f"No source pin for {rel}")

def validate_inventory(root: Path | None = None, contract_override: Mapping[str, Any] | None = None) -> dict[str, Any]:
    root = root or project_root()
    contract = dict(contract_override) if contract_override is not None else _load_contract(root)[0]
    validate_governance(contract)
    pins = validate_source_pins(root, contract)
    matrix = contract.get("selector_matrix")
    if not isinstance(matrix, list) or [str(row.get("challenge_id")) for row in matrix] != EXPECTED_IDS: raise CapabilityMatrixError("Selector matrix must contain exactly CHALLENGE_001 through CHALLENGE_009 in order")
    registry = (root / "core/mechanics/MechanicRegistry.gd").read_text(encoding="utf-8-sig")
    routes = registry_routes(registry)
    unique_assets: set[str] = set(); asset_refs = 0; custom_verified = 0; preview_ids=[]; time_conflicts=[]; results=[]
    for row in matrix:
        cid = str(row["challenge_id"]); rel = f"challenges/{cid}.json"; source = read_json(root / rel)
        if source.get("challenge_id") != cid: raise CapabilityMatrixError(f"Identity mismatch in {rel}")
        mechanic = str(source.get("mechanic", ""))
        if row.get("mechanic") != mechanic: raise CapabilityMatrixError(f"Mechanic matrix drift for {cid}")
        mapped_class = routes.get(mechanic)
        if not mapped_class: raise CapabilityMatrixError(f"Mechanic not registered in canonical registry: {mechanic}")
        expected_path = str(row.get("mechanic_source_path", ""))
        expected_class = Path(expected_path).stem
        if mapped_class != expected_class: raise CapabilityMatrixError(f"Mechanic registry route mismatch for {cid}: {mapped_class} != {expected_class}")
        if not (root / expected_path).is_file(): raise CapabilityMatrixError(f"Mechanic implementation missing: {expected_path}")
        if source_pin(root, contract, expected_path) != sha256_file(root / expected_path): raise CapabilityMatrixError(f"Mechanic source pin changed: {expected_path}")
        if row.get("mechanic_source_sha256") != sha256_file(root / expected_path): raise CapabilityMatrixError(f"Mechanic matrix lineage mismatch: {cid}")
        actual_keys = custom_data_keys((root / expected_path).read_text(encoding="utf-8-sig"))
        if row.get("custom_data_keys_inventory_only") != actual_keys: raise CapabilityMatrixError(f"FrameSnapshot.custom_data inventory drift for {cid}")
        custom_verified += 1
        bindings = asset_bindings(source)
        if row.get("asset_bindings") != bindings: raise CapabilityMatrixError(f"Asset role map drift for {cid}")
        for asset_rel in bindings.values():
            asset_refs += 1; unique_assets.add(asset_rel)
            if not (root / asset_rel).is_file(): raise CapabilityMatrixError(f"Referenced asset missing: {asset_rel}")
            source_pin(root, contract, asset_rel)
        video=source.get("video", {}); phases={key: video[key] for key in PHASE_KEYS if key in video}
        if row.get("phase_duration_fields_present") != list(phases.keys()) or row.get("phase_durations_seconds") != phases: raise CapabilityMatrixError(f"Source phase inventory drift for {cid}")
        phase_sum=sum(float(video.get(key,0.0)) for key in PHASE_KEYS)
        if abs(float(row.get("component_duration_sum_seconds", -999))-phase_sum)>1e-9: raise CapabilityMatrixError(f"Phase sum inventory drift for {cid}")
        total=video.get("total_duration")
        if row.get("declared_total_duration_seconds") != total: raise CapabilityMatrixError(f"Declared total duration drift for {cid}")
        if total is not None and abs(float(total)-phase_sum)>1e-9:
            time_conflicts.append(cid)
            expected_status="DECLARED_TOTAL_CONFLICTS_WITH_PHASE_SUM"
        elif total is not None: expected_status="DECLARED_TOTAL_MATCHES_PHASE_SUM"
        else: expected_status="TOTAL_DURATION_NOT_DECLARED"
        if row.get("temporal_status") != expected_status: raise CapabilityMatrixError(f"Temporal status drift for {cid}")
        if int(video.get("fps",0)) != 60: raise CapabilityMatrixError(f"Unexpected source fps for {cid}")
        if bool(row.get("existing_challenge_visual_payload_preview_harness")):
            preview_ids.append(cid)
            if cid != "CHALLENGE_004" or row.get("payload_runtime_status") != "EXISTING_REVIEW_ONLY_V1_HARNESS": raise CapabilityMatrixError("Existing V1 preview scope was widened beyond CHALLENGE_004")
        elif row.get("payload_runtime_status") != "NOT_YET_RUNTIME_MATERIALIZED": raise CapabilityMatrixError(f"False runtime support claim for {cid}")
        if row.get("visual_projection_approval") != "NONE": raise CapabilityMatrixError(f"Projection falsely approved for {cid}")
        results.append({"challenge_id":cid,"mechanic":mechanic,"mechanic_class":mapped_class,"mechanic_source_path":expected_path,"asset_bindings":bindings,"custom_data_keys_inventory_only":actual_keys,"fps":int(video["fps"]),"phase_durations_seconds":phases,"component_duration_sum_seconds":phase_sum,"declared_total_duration_seconds":total,"temporal_status":expected_status,"existing_challenge_visual_payload_preview_harness":cid in preview_ids,"visual_projection_approval":"NONE"})
    if asset_refs != 27 or len(unique_assets) != int(contract["capability_policy"]["unique_asset_count_expected"]): raise CapabilityMatrixError("Asset role-reference matrix is incomplete")
    if time_conflicts != ["CHALLENGE_008", "CHALLENGE_009"]: raise CapabilityMatrixError(f"Unexpected explicit-total temporal conflicts: {time_conflicts}")
    if preview_ids != ["CHALLENGE_004"]: raise CapabilityMatrixError("V1 payload preview scope must remain precisely CHALLENGE_004")
    return {"pins":pins,"selectors":results,"asset_reference_count":asset_refs,"unique_assets":sorted(unique_assets),"custom_data_inventory_verified":custom_verified,"temporal_conflicts":time_conflicts,"preview_ids":preview_ids}

def build_report(root: Path | None = None) -> dict[str, Any]:
    root = root or project_root()
    contract, contract_schema, report_schema = _load_contract(root)
    inventory = validate_inventory(root, contract)
    summary={
      "selectors":f"{len(inventory['selectors'])}/9", "source_pins":f"{inventory['pins']['source_pins']}/43",
      "mechanic_registry_routes":f"{len(inventory['selectors'])}/9", "asset_reference_bindings":f"{inventory['asset_reference_count']}/27",
      "unique_assets":f"{len(inventory['unique_assets'])}/{contract['capability_policy']['unique_asset_count_expected']}",
      "custom_data_inventory":f"{inventory['custom_data_inventory_verified']}/9", "explicit_total_timebase_conflicts":len(inventory['temporal_conflicts']),
      "existing_runtime_payload_preview_coverage":f"{len(inventory['preview_ids'])}/9", "godot_invocations":0,
      "payload_materialized":False,"visual_projection_approval":"NONE","candidate_input_admissible":False,
      "seed_domains_complete_for_candidate_input":False,"renderer":"OFF","media_created":False,"D4.8":"BLOCKED","release_authority":"NONE"
    }
    temporal=[{"challenge_id":row["challenge_id"],"component_duration_sum_seconds":row["component_duration_sum_seconds"],"declared_total_duration_seconds":row["declared_total_duration_seconds"],"status":row["temporal_status"],"policy_decision":"UNRESOLVED_NOT_APPROVED" if row["temporal_status"]=="DECLARED_TOTAL_CONFLICTS_WITH_PHASE_SUM" else "SOURCE_INVENTORY_ONLY"} for row in inventory['selectors']]
    lineage=[{"path":x["path"],"sha256":x["sha256"],"kind":x["kind"]} for x in contract['pinned_sources']]
    lineage.append({"path":CONTRACT_REL.as_posix(),"sha256":sha256_file(root/CONTRACT_REL),"kind":"capability_matrix_contract"})
    lineage.sort(key=lambda x:x["path"])
    return {"schema":REPORT_ID,"schema_version":"1.0","status":"PASS_STATIC_CAPABILITY_AND_LINEAGE_ONLY_NO_PAYLOAD_MATERIALIZATION","contract_sha256":sha256_file(root/CONTRACT_REL),"summary":summary,"selector_matrix":inventory['selectors'],"temporal_review":temporal,"source_lineage":lineage,"governance":dict(contract['governance_locks'])}

def main(argv: list[str] | None = None) -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root",default=".")
    parser.add_argument("--full-report",action="store_true")
    args=parser.parse_args(argv); root=Path(args.root).resolve()
    try:
        report=build_report(root)
        s=report['summary']
        print("C11-D CHALLENGE VISUAL PAYLOAD CAPABILITY MATRIX V1 PASS | selectors=%s | source_pins=%s | mechanic_registry_routes=%s | asset_reference_bindings=%s | unique_assets=%s | custom_data_inventory=%s | explicit_total_timebase_conflicts=%s | existing_preview_coverage=%s | godot_invocations=0 | payload_materialized=false | candidate_input_admissible=false | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE" % (s['selectors'],s['source_pins'],s['mechanic_registry_routes'],s['asset_reference_bindings'],s['unique_assets'],s['custom_data_inventory'],s['explicit_total_timebase_conflicts'],s['existing_runtime_payload_preview_coverage']))
        if args.full_report: print("C11D_CHALLENGE_VISUAL_PAYLOAD_CAPABILITY_MATRIX_REPORT="+json.dumps(report,ensure_ascii=False,sort_keys=True,separators=(",",":")))
        return 0
    except Exception as exc:
        print("C11-D CHALLENGE VISUAL PAYLOAD CAPABILITY MATRIX V1 FAIL | "+str(exc),file=sys.stderr)
        return 1
if __name__=="__main__": raise SystemExit(main())
