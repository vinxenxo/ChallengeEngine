"""Static contract/source-lineage validation for the in-memory CHALLENGE_004 runtime preview."""
from __future__ import annotations
import copy, hashlib, json, math, re
from collections.abc import Mapping
from pathlib import Path
from typing import Any

CONTRACT_REL=Path("definitions/c11d/production/D_RENDERER_CHALLENGE_RUNTIME_OUTPUT_PREVIEW_V1.json")
SCHEMA_REL=Path("definitions/c11d/production/D_RENDERER_CHALLENGE_RUNTIME_OUTPUT_PREVIEW_SCHEMA_V1.json")
MANIFEST_REL=Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")
CHALLENGE_REL=Path("challenges/CHALLENGE_004.json")
MANIFEST_SHA256="e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
CONTRACT_SCHEMA="C11-D-RENDERER-CHALLENGE-RUNTIME-OUTPUT-PREVIEW-CONTRACT-V1"
OUTPUT_SCHEMA="C11-D-D9-RENDERER-CHALLENGE-RUNTIME-OUTPUT-PREVIEW-V1"
GDSCRIPT_REL=Path("tools/c11d/d9/materialize_challenge_runtime_output_in_memory.gd")

class ChallengeRuntimePreviewError(ValueError): pass

def _root(project_root: Path | str | None=None)->Path:
    return Path(project_root).resolve() if project_root is not None else Path(__file__).resolve().parents[3]

def _read_json(path:Path)->dict[str,Any]:
    try: value=json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc: raise ChallengeRuntimePreviewError(f"Cannot read JSON source {path}: {exc}") from exc
    if not isinstance(value,dict): raise ChallengeRuntimePreviewError(f"Expected JSON object: {path}")
    return value

def _sha(path:Path)->str:
    try: return hashlib.sha256(path.read_bytes()).hexdigest()
    except Exception as exc: raise ChallengeRuntimePreviewError(f"Cannot hash {path}: {exc}") from exc

def validate_preview_contract(project_root:Path | str | None=None)->dict[str,Any]:
    root=_root(project_root); spec=_read_json(root/CONTRACT_REL)
    if spec.get("schema")!=CONTRACT_SCHEMA or spec.get("schema_version")!="1.0": raise ChallengeRuntimePreviewError("Contract identity/version mismatch")
    if spec.get("status")!="PREPARATION_ONLY_RUNTIME_RESULT_PREVIEW_NOT_RENDERER_INPUT": raise ChallengeRuntimePreviewError("Contract must remain preparation-only")
    if _sha(root/MANIFEST_REL)!=MANIFEST_SHA256 or spec.get("source_of_truth",{}).get("frozen_c11c_manifest_sha256")!=MANIFEST_SHA256: raise ChallengeRuntimePreviewError("Frozen C11-C manifest hash mismatch")
    challenge=_read_json(root/CHALLENGE_REL)
    expected_source={"challenge_id":"CHALLENGE_004","mechanic":"parking_v2","mechanic_version":"2.0","asset_family":"fam_garage_01","asset_family_version":"1.0","video":{"fps":60,"hook_duration":3.0,"game_duration":7.0,"reveal_duration":3.0,"cta_duration":2.0},"generation":{"seed":314159,"rng_version":"2.0"}}
    for key,value in expected_source.items():
        if challenge.get(key)!=value: raise ChallengeRuntimePreviewError(f"CHALLENGE_004 fixture drift: {key}")
    scope=spec.get("scope",{})
    if scope.get("challenge_id")!="CHALLENGE_004" or scope.get("mechanic")!="parking_v2" or scope.get("seed_requested")!=314159 or scope.get("fps")!=60: raise ChallengeRuntimePreviewError("Challenge scope drift")
    if scope.get("phases_frames")!={"hook":180,"game":420,"reveal":180,"cta":120} or scope.get("total_frames")!=900 or scope.get("duration_seconds")!=15.0: raise ChallengeRuntimePreviewError("Expected challenge timeline contract drift")
    locks={"renderer":"OFF","media_created":False,"d4_8":"BLOCKED","release_authority":"NONE","c11c_source_mutation":False,"runtime_report_file_written":False,"challenge_runtime_result_in_memory":True,"challenge_visual_payload_materialized":False,"renderer_native_input_emitted":False,"renderer_dispatch_invoked":False,"renderer_activation":False,"production_execution":False,"output_artifact_path":None}
    if spec.get("required_locks")!=locks: raise ChallengeRuntimePreviewError("Execution boundary can not self-promote")
    approvals={"challenge_runtime_preview_approved":False,"selected_payload_instances_approved":False,"renderer_baseline_approved":False,"renderer_baseline_frozen":False,"d4_8_authorized":False,"d9_14_full_acceptance":"BLOCKED_AS_REQUIRED","d9_16_full_acceptance":"BLOCKED_AS_REQUIRED","d9_17_closure":"BLOCKED_NO_GO","d10":"BLOCKED","release_authority":"NONE"}
    if spec.get("approval_state")!=approvals: raise ChallengeRuntimePreviewError("Preview can not grant acceptance/freeze/authority")
    lineage=spec.get("source_lineage")
    if not isinstance(lineage,list) or len(lineage)<16: raise ChallengeRuntimePreviewError("Source lineage too short")
    seen=set()
    for row in lineage:
        if not isinstance(row,Mapping) or set(row)!={"path","sha256"}: raise ChallengeRuntimePreviewError("Malformed source lineage item")
        rel=str(row["path"]); expected=str(row["sha256"])
        if rel in seen or not re.fullmatch(r"[a-f0-9]{64}",expected): raise ChallengeRuntimePreviewError("Duplicate/malformed source hash")
        if _sha(root/rel)!=expected: raise ChallengeRuntimePreviewError(f"Pinned source drift: {rel}")
        seen.add(rel)
    if lineage[0]["path"]!=str(MANIFEST_REL).replace("\\","/") or lineage[0]["sha256"]!=MANIFEST_SHA256: raise ChallengeRuntimePreviewError("Frozen manifest must lead source lineage")
    schema=_read_json(root/SCHEMA_REL)
    if schema.get("$schema")!="https://json-schema.org/draft/2020-12/schema" or schema.get("additionalProperties") is not False: raise ChallengeRuntimePreviewError("Invalid strict output JSON Schema")
    harness=(root/GDSCRIPT_REL).read_text(encoding="utf-8-sig")
    for token in ["ChallengeRuntimeBridgeScript.run_effective_pipeline(legacy_config)","CHALLENGE_004.json","runtime_report_file_written","renderer_native_input_emitted","challenge_visual_payload_materialized"]:
        if token not in harness: raise ChallengeRuntimePreviewError(f"Harness contract token missing: {token}")
    for banned in ["FileAccess.open(OUTPUT", "--render", "RenderingServer", "Image.save_png", "MovieWriter"]:
        if banned in harness: raise ChallengeRuntimePreviewError(f"Harness includes prohibited persistence/render token: {banned}")
    return {"contract":spec,"schema":schema,"source_lineage":lineage,"challenge_source_sha256":_sha(root/CHALLENGE_REL),"harness":harness}

def validate_preview_record(record:dict[str,Any],project_root:Path | str | None=None)->bool:
    parsed=validate_preview_contract(project_root); root=_root(project_root)
    if not isinstance(record,dict): raise ChallengeRuntimePreviewError("Runtime preview record must be an object")
    if record.get("schema")!=OUTPUT_SCHEMA or record.get("schema_version")!="1.0" or record.get("status")!="IN_MEMORY_REVIEW_ONLY_NOT_RENDERER_INPUT": raise ChallengeRuntimePreviewError("Output identity/status mismatch")
    if record.get("frozen_c11c_manifest_sha256")!=MANIFEST_SHA256: raise ChallengeRuntimePreviewError("Runtime preview references wrong frozen baseline")
    if record.get("challenge_source_sha256")!=parsed["challenge_source_sha256"]: raise ChallengeRuntimePreviewError("Challenge source digest mismatch")
    if record.get("challenge_runtime_output_materialized") is not True or record.get("challenge_visual_payload_materialized") is not False: raise ChallengeRuntimePreviewError("Runtime result must be in memory; visual payload must remain unmaterialized")
    if record.get("deterministic_repeat_pass") is not True: raise ChallengeRuntimePreviewError("Two effective runtime executions must match")
    if set(record)!={"schema","schema_version","status","frozen_c11c_manifest_sha256","challenge_source_sha256","challenge_runtime_output_materialized","challenge_visual_payload_materialized","instance","deterministic_repeat_pass","execution_boundary"}: raise ChallengeRuntimePreviewError("Unexpected or missing output fields")
    ins=record.get("instance")
    if not isinstance(ins,dict): raise ChallengeRuntimePreviewError("Missing challenge runtime instance")
    expected={"content_type":"challenges","challenge_id":"CHALLENGE_004","mechanic":"parking_v2","mechanic_version":"2.0","asset_family":"fam_garage_01","asset_family_version":"1.0","seed_requested":314159,"rng_version":"2.0","fps":60,"phase_frames":{"hook":180,"game":420,"reveal":180,"cta":120},"total_frames":900,"duration_seconds":15.0,"game_frame_count":420,"simulation_error_state":"OK","presentation_binding_success":True,"materialization":"IN_MEMORY_ONLY_RUNTIME_RESULT_NOT_VISUAL_PAYLOAD"}
    for key,value in expected.items():
        if ins.get(key)!=value: raise ChallengeRuntimePreviewError(f"Challenge instance contract mismatch: {key}")
    if not isinstance(ins.get("seed_used"),int) or ins["seed_used"]<1: raise ChallengeRuntimePreviewError("Invalid effective seed")
    if not isinstance(ins.get("winning_frame_local"),int) or not -1<=ins["winning_frame_local"]<420: raise ChallengeRuntimePreviewError("winning_frame_local must remain local to GAME")
    if not isinstance(ins.get("attempts"),int) or not 1<=ins["attempts"]<=100: raise ChallengeRuntimePreviewError("Invalid attempt count")
    for key in ["score","minimum_distance","tolerance_threshold"]:
        if not isinstance(ins.get(key),(int,float)) or not math.isfinite(float(ins[key])): raise ChallengeRuntimePreviewError(f"Invalid numeric runtime metric: {key}")
    if not 0<=float(ins["score"])<=1 or float(ins["minimum_distance"])<0 or float(ins["tolerance_threshold"])<0: raise ChallengeRuntimePreviewError("Runtime metric outside allowed bounds")
    editorial=ins.get("editorial_content")
    if not isinstance(editorial,dict) or set(editorial)!={"hook","reveal","cta"} or editorial.get("hook")!="¡SOLO EL 1% APARCA SIN ROZAR!" or editorial.get("cta")!="¿Lo has clavado?" or not isinstance(editorial.get("reveal"),str): raise ChallengeRuntimePreviewError("Editorial copy differs from canonical challenge source")
    assets=ins.get("physical_asset_bindings")
    if not isinstance(assets,dict) or set(assets)!={"background_path","target_path","object_path"} or any(not isinstance(x,str) or not x.startswith("res://") for x in assets.values()): raise ChallengeRuntimePreviewError("Physical asset bindings malformed")
    for key in ["frame_signature_sha256","presentation_render_model_sha256","runtime_output_sha256"]:
        if not isinstance(ins.get(key),str) or not re.fullmatch(r"[a-f0-9]{64}",ins[key]): raise ChallengeRuntimePreviewError(f"Invalid digest: {key}")
    if not isinstance(ins.get("presentation_profile_id"),str) or not ins["presentation_profile_id"]: raise ChallengeRuntimePreviewError("Presentation profile not bound")
    boundary={"mode":"GODOT_HEADLESS_IN_MEMORY_REVIEW_ONLY","runtime_called":True,"simulation_executed":True,"runtime_report_file_written":False,"renderer_native_input_emitted":False,"renderer_dispatch_invoked":False,"renderer_activation":False,"production_execution":False,"media_output_created":False,"output_artifact_path":None,"d4_8":"BLOCKED","release_authority":"NONE","c11c_source_mutation":False}
    if record.get("execution_boundary")!=boundary: raise ChallengeRuntimePreviewError("Execution boundary mismatch or privilege escalation")
    if parsed["schema"].get("properties",{}).get("instance",{}).get("properties",{}).get("runtime_output_sha256",{}).get("pattern")!='^[a-f0-9]{64}$': raise ChallengeRuntimePreviewError("Schema digest validation missing")
    try:
        from jsonschema import Draft202012Validator
        Draft202012Validator(parsed["schema"]).validate(record)
    except ImportError:
        pass
    return True
