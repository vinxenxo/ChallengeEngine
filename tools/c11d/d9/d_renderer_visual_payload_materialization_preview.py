"""Contracts and source-lineage checks for the in-memory D renderer visual-payload preview."""
from __future__ import annotations
import copy, hashlib, json, re
from collections.abc import Mapping
from pathlib import Path
from typing import Any

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_VISUAL_PAYLOAD_MATERIALIZATION_PREVIEW_V1.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_VISUAL_PAYLOAD_MATERIALIZATION_PREVIEW_SCHEMA_V1.json")
MANIFEST_REL = Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")
MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
CONTRACT_SCHEMA = "C11-D-RENDERER-VISUAL-PAYLOAD-MATERIALIZATION-PREVIEW-CONTRACT-V1"
OUTPUT_SCHEMA = "C11-D-D9-RENDERER-VISUAL-PAYLOAD-MATERIALIZATION-PREVIEW-V1"
GDSCRIPT_REL = Path("tools/c11d/d9/materialize_visual_payloads_in_memory.gd")

class VisualPayloadPreviewError(ValueError):
    pass

def _root(project_root: Path | str | None = None) -> Path:
    return Path(project_root).resolve() if project_root is not None else Path(__file__).resolve().parents[3]

def _read_json(path: Path) -> dict[str, Any]:
    try: value = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc: raise VisualPayloadPreviewError(f"Cannot read JSON source {path}: {exc}") from exc
    if not isinstance(value, dict): raise VisualPayloadPreviewError(f"Expected JSON object at {path}")
    return value

def _sha_file(path: Path) -> str:
    try: return hashlib.sha256(path.read_bytes()).hexdigest()
    except Exception as exc: raise VisualPayloadPreviewError(f"Cannot hash source {path}: {exc}") from exc

def _sha_json(value: Any) -> str:
    canonical = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

def validate_preview_contract(project_root: Path | str | None = None) -> dict[str, Any]:
    root = _root(project_root)
    spec = _read_json(root / CONTRACT_REL)
    if spec.get("schema") != CONTRACT_SCHEMA or spec.get("schema_version") != "1.0":
        raise VisualPayloadPreviewError("Preview contract identity/version mismatch")
    if spec.get("status") != "PREPARATION_ONLY_IN_MEMORY_VISUAL_PAYLOAD_PREVIEW_NOT_RENDERER_INPUT":
        raise VisualPayloadPreviewError("Preview contract cannot self-promote")
    if _sha_file(root / MANIFEST_REL) != MANIFEST_SHA256 or spec.get("source_of_truth", {}).get("frozen_c11c_manifest_sha256") != MANIFEST_SHA256:
        raise VisualPayloadPreviewError("Frozen C11-C manifest mismatch")
    expected_scope = ["visual_loops", "visual_drills"]
    if spec.get("scope", {}).get("materialized_content_types") != expected_scope or spec.get("scope", {}).get("not_materialized_content_types") != ["challenges"]:
        raise VisualPayloadPreviewError("V1 materialization scope must remain Visual Loop + Visual Drill only")
    fixtures = spec.get("scope", {}).get("request_fixtures")
    expected_fixtures = [
        {"content_type":"visual_loops","request_id":"D-PAYLOAD-BIND-VISUAL_LOOPS","family_id":"c11c_geometric_waves_v1","subtype_id":"harmonic_membrane","internal_generator":"geometric","seed":12345,"variation_index":0,"delivery_profile_id":"REVIEW_720"},
        {"content_type":"visual_drills","request_id":"D-PAYLOAD-BIND-VISUAL_DRILLS","family_id":"tracking","variant_id":"tier-2","internal_generator":"tracking","seed":12345,"variation_index":0,"delivery_profile_id":"REVIEW_720"},
    ]
    if fixtures != expected_fixtures: raise VisualPayloadPreviewError("Request fixture selection/identity drift")
    locks = {
        "renderer":"OFF","media_created":False,"d4_8":"BLOCKED","release_authority":"NONE",
        "c11c_source_mutation":False,"payload_file_written":False,"challenge_instance_materialized":False,
        "renderer_native_input_emitted":False,"renderer_dispatch_invoked":False,"renderer_activation":False,
        "production_execution":False,"output_artifact_path":None
    }
    if spec.get("required_locks") != locks: raise VisualPayloadPreviewError("Execution-boundary lock mismatch")
    expected_approval = {
      "payload_materialization_preview_approved":False,"selected_payload_instances_approved":False,
      "renderer_baseline_approved":False,"renderer_baseline_frozen":False,"d4_8_authorized":False,
      "d9_14_full_acceptance":"BLOCKED_AS_REQUIRED","d9_16_full_acceptance":"BLOCKED_AS_REQUIRED",
      "d9_17_closure":"BLOCKED_NO_GO","d10":"BLOCKED","release_authority":"NONE"
    }
    if spec.get("approval_state") != expected_approval: raise VisualPayloadPreviewError("Preview cannot grant approval/freeze/authority")
    raw = spec.get("source_lineage")
    if not isinstance(raw, list) or len(raw) < 20: raise VisualPayloadPreviewError("Pinned source lineage is incomplete")
    seen=set(); checked=[]
    for row in raw:
        if not isinstance(row, Mapping) or set(row) != {"path","sha256"}: raise VisualPayloadPreviewError("Malformed source lineage row")
        rel=str(row["path"]); expected=str(row["sha256"])
        if rel in seen or not re.fullmatch(r"[a-f0-9]{64}", expected): raise VisualPayloadPreviewError("Duplicate or malformed source lineage row")
        actual=_sha_file(root/rel)
        if actual != expected: raise VisualPayloadPreviewError(f"Pinned source drift: {rel}")
        seen.add(rel); checked.append({"path":rel,"sha256":actual})
    if not checked or checked[0]["path"] != str(MANIFEST_REL).replace("\\", "/"):
        raise VisualPayloadPreviewError("Frozen manifest must be first source-lineage entry")
    schema=_read_json(root/SCHEMA_REL)
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or schema.get("$id") != "urn:c11d:renderer-visual-payload-materialization-preview:v1" or schema.get("additionalProperties") is not False:
        raise VisualPayloadPreviewError("Output schema identity/strictness mismatch")
    harness=(root/GDSCRIPT_REL).read_text(encoding="utf-8-sig")
    banned_literals=("FileAccess.WRITE", "FileAccess.READ_WRITE", "store_string(", "store_buffer(", "DirAccess.make_dir", "OS.execute(", "OS.shell_open(", "SubViewport", "MovieWriter", "FFmpeg", "get_viewport().get_texture", "renderer_native_input_emitted = true", "renderer_activation = true")
    for token in banned_literals:
        if token.lower() in harness.lower(): raise VisualPayloadPreviewError(f"Potential side-effect/render path found in headless payload harness: {token}")
    for required in ("VisualAuthoringGenerator.gd", "VisualAuthoringRequest.gd", "VisualAuthoringAssemblyContext.gd", "C11CVariationProfile.gd", "C11CPaletteBank.gd", "C11CVisualLoopDuration.gd", "VisualDrillSeedVariation.gd", "harmonic_membrane", "VisualAuthoringGeneratorScript.generate", "C11CVisualLoopDurationScript.policy_seconds_for_cycles"):
        if required not in harness: raise VisualPayloadPreviewError(f"Headless harness is missing required source/route token: {required}")
    if spec.get("materialization_rules", {}).get("variation_index_is_metadata_only_in_v1") is not True:
        raise VisualPayloadPreviewError("V1 must state that variation_index is metadata-only")
    return {"source_lineage":checked,"schema":schema,"contract":spec,"harness":harness}

def validate_preview_record(record: Mapping[str, Any], project_root: Path | str | None = None) -> bool:
    parsed=validate_preview_contract(project_root); schema=parsed["schema"]
    if not isinstance(record, Mapping): raise VisualPayloadPreviewError("Preview record must be an object")
    required=set(schema.get("required", []))
    if set(record) != required: raise VisualPayloadPreviewError("Preview record top-level fields do not match strict schema")
    if record.get("schema") != OUTPUT_SCHEMA or record.get("schema_version") != "1.0" or record.get("status") != "IN_MEMORY_REVIEW_ONLY_NOT_RENDERER_INPUT":
        raise VisualPayloadPreviewError("Preview record identity/status mismatch")
    if record.get("frozen_c11c_manifest_sha256") != MANIFEST_SHA256: raise VisualPayloadPreviewError("Preview record frozen manifest mismatch")
    if record.get("unmaterialized_content_types") != ["challenges"] or record.get("challenge_runtime_payload_materialized") is not False:
        raise VisualPayloadPreviewError("Challenge payload cannot be claimed by visual-only harness")
    execution = record.get("execution_boundary")
    expected_execution={"mode":"IN_MEMORY_REVIEW_ONLY","payload_file_written":False,"renderer_native_input_emitted":False,"renderer_dispatch_invoked":False,"renderer_activation":False,"production_execution":False,"media_output_created":False,"output_artifact_path":None,"d4_8":"BLOCKED","release_authority":"NONE","c11c_source_mutation":False}
    if execution != expected_execution: raise VisualPayloadPreviewError("Preview record execution/governance boundary mismatch")
    instances=record.get("instances")
    if not isinstance(instances,list) or len(instances)!=2: raise VisualPayloadPreviewError("Exactly two visual payload summaries are expected")
    type_map={}
    instance_required=set(schema["properties"]["instances"]["items"]["required"])
    for item in instances:
        if not isinstance(item,Mapping) or set(item)!=instance_required: raise VisualPayloadPreviewError("Visual payload summary has unknown/missing fields")
        typ=item.get("content_type")
        if typ in type_map or typ not in {"visual_loops","visual_drills"}: raise VisualPayloadPreviewError("Duplicate/unsupported materialized type")
        type_map[typ]=item
        if item.get("seed") != 12345 or item.get("variation_index") != 0 or item.get("fps") != 30:
            raise VisualPayloadPreviewError("V1 request seed/variation/FPS fixture mismatch")
        for k in ("authoring_envelope_sha256","payload_instance_sha256"):
            if not isinstance(item.get(k),str) or not re.fullmatch(r"[a-f0-9]{64}",item[k]): raise VisualPayloadPreviewError(f"Malformed {k}")
        if item.get("materialization")!="IN_MEMORY_ONLY" or item.get("deterministic_repeat_pass") is not True or item.get("instance_parameters_bound") is not True:
            raise VisualPayloadPreviewError("Instance not deterministically bound in memory")
        if isinstance(item.get("frame_count"),bool) or not isinstance(item.get("frame_count"),int) or item["frame_count"]<1:
            raise VisualPayloadPreviewError("frame_count must be a positive integer")
        duration=item.get("duration_seconds")
        if isinstance(duration,bool) or not isinstance(duration,(int,float)) or duration<=0 or round(duration*item["fps"])!=item["frame_count"]:
            raise VisualPayloadPreviewError("Duration/frame_count/FPS arithmetic mismatch")
        if not isinstance(item.get("instance_id"),str) or len(item["instance_id"])<8: raise VisualPayloadPreviewError("Missing instance_id")
    if set(type_map)!={"visual_loops","visual_drills"}: raise VisualPayloadPreviewError("Required Visual Loop and Visual Drill payload summaries are missing")
    loop=type_map["visual_loops"]; drill=type_map["visual_drills"]
    if loop["selection"]!={"family_id":"c11c_geometric_waves_v1","subtype_id":"harmonic_membrane"}: raise VisualPayloadPreviewError("Selected loop grammar identity drift")
    if loop["duration_seconds"] not in (20,22,23) or loop["frame_count"] != loop["duration_seconds"]*30: raise VisualPayloadPreviewError("Loop timing differs from C11-C cycle duration policy")
    if drill["selection"]!={"family_id":"tracking","variant_id":"tier-2"} or drill["duration_seconds"]!=21 or drill["frame_count"]!=630: raise VisualPayloadPreviewError("Tracking tier-2 canonical timing/selection drift")
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        Draft202012Validator=None
    if Draft202012Validator is not None:
        Draft202012Validator(schema).validate(dict(record))
    return True
