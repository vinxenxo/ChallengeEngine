"""Read-only source audit for D-owned separation of legacy, presentation and delivery profile identities."""
from __future__ import annotations
import hashlib, json, re
from collections.abc import Mapping
from pathlib import Path
from typing import Any

CONTRACT_REL=Path("definitions/c11d/production/D_RENDERER_PROFILE_IDENTITY_SEPARATION_V1.json")
SCHEMA_REL=Path("definitions/c11d/production/D_RENDERER_PROFILE_IDENTITY_SEPARATION_SCHEMA_V1.json")
MANIFEST_SHA256="e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
CONTRACT_SCHEMA="C11-D-RENDERER-PROFILE-IDENTITY-SEPARATION-CONTRACT-V1"
OUTPUT_SCHEMA="C11-D-D9-RENDERER-PROFILE-IDENTITY-SEPARATION-V1"
GDSCRIPT_REL=Path("tools/c11d/d9/rebind_challenge_presentation_profile_in_memory.gd")
class ProfileIdentityError(ValueError): pass

def _root(project_root: Path | str | None=None)->Path:
    return Path(project_root).resolve() if project_root is not None else Path(__file__).resolve().parents[3]
def _json(root:Path, rel:Path)->dict[str,Any]:
    try: value=json.loads((root/rel).read_text(encoding="utf-8-sig"))
    except Exception as exc: raise ProfileIdentityError(f"Cannot read {rel}: {exc}") from exc
    if not isinstance(value,dict): raise ProfileIdentityError(f"Expected object: {rel}")
    return value
def _sha(path:Path)->str:
    try: return hashlib.sha256(path.read_bytes()).hexdigest()
    except Exception as exc: raise ProfileIdentityError(f"Cannot hash {path}: {exc}") from exc

def validate_contract(project_root:Path | str | None=None)->dict[str,Any]:
    root=_root(project_root); spec=_json(root,CONTRACT_REL)
    if spec.get("schema")!=CONTRACT_SCHEMA or spec.get("schema_version")!="1.0": raise ProfileIdentityError("Contract identity mismatch")
    if spec.get("status")!="PREPARATION_ONLY_IDENTITY_RECONCILIATION_NOT_RENDERER_INPUT": raise ProfileIdentityError("Identity audit must remain preparation-only")
    if _sha(root/"release/C11C_FREEZE_PACKAGE_MANIFEST.json")!=MANIFEST_SHA256: raise ProfileIdentityError("Frozen C11-C manifest drift")
    if spec.get("source_lineage",[{}])[0].get("sha256")!=MANIFEST_SHA256: raise ProfileIdentityError("Frozen manifest must lead lineage")
    seen=set()
    for row in spec.get("source_lineage",[]):
        if not isinstance(row,Mapping) or set(row)!={"path","sha256"}: raise ProfileIdentityError("Malformed source lineage")
        rel=str(row["path"]); digest=str(row["sha256"])
        if rel in seen or not re.fullmatch(r"[a-f0-9]{64}",digest): raise ProfileIdentityError("Duplicate or invalid source digest")
        if _sha(root/rel)!=digest: raise ProfileIdentityError(f"Pinned source drift: {rel}")
        seen.add(rel)
    if len(seen)<15: raise ProfileIdentityError("Insufficient source lineage")
    challenge=_json(root,Path("challenges/CHALLENGE_004.json"))
    legacy=_json(root,Path("profiles/video/test_master_11s.json"))
    social=_json(root,Path("profiles/video/parking_v2_social_15s.json"))
    delivery=_json(root,Path("profiles/delivery/c11c_video_delivery_profiles.json"))
    testprof=legacy.get("phases",{}); socialprof=social.get("phases",{})
    if challenge.get("video_profile")!="test_master_11s": raise ProfileIdentityError("Legacy profile alias drift")
    if challenge.get("presentation",{}).get("profile")!="social_default_v1": raise ProfileIdentityError("Explicit source presentation profile drift")
    inline=challenge.get("video",{})
    if inline!={"fps":60,"hook_duration":3.0,"game_duration":7.0,"reveal_duration":3.0,"cta_duration":2.0}: raise ProfileIdentityError("Inline canonical timeline drift")
    if legacy.get("fps")!=30 or testprof!={"hook_duration":2.0,"game_duration":6.0,"reveal_duration":1.0,"cta_duration":2.0}: raise ProfileIdentityError("test_master_11s facts drift")
    if social.get("fps")!=60 or socialprof!={"hook_duration":3.0,"game_duration":7.0,"reveal_duration":3.0,"cta_duration":2.0}: raise ProfileIdentityError("parking_v2_social_15s facts drift")
    profiles=delivery.get("profiles",{}); review=profiles.get("REVIEW_720",{})
    if (review.get("fps"),review.get("width"),review.get("height"))!=(30,720,1280): raise ProfileIdentityError("REVIEW_720 facts drift")
    bridge=(root/"core/execution/ChallengeRuntimeBridge.gd").read_text(encoding="utf-8-sig")
    migration=(root/"core/authoring/ChallengeMigrationAdapter.gd").read_text(encoding="utf-8-sig")
    timeline=(root/"core/execution/ChallengeTimelineBuilder.gd").read_text(encoding="utf-8-sig")
    if '"default_profile_id": "test_master_11s"' not in bridge: raise ProfileIdentityError("Legacy bridge fallback behavior changed; revise this audit, do not loosen it")
    if 'var profile_id := str(config.get("video_profile", policy.get("default_profile_id", "")))' not in migration: raise ProfileIdentityError("Legacy profile migration behavior changed")
    if "_normalize_inline_canonical_video(video_binding)" not in timeline: raise ProfileIdentityError("Inline video timeline path changed")
    if spec.get("required_locks")!={"mode":"GODOT_HEADLESS_IN_MEMORY_REVIEW_ONLY","c11c_source_mutation":False,"runtime_report_file_written":False,"renderer_native_input_emitted":False,"renderer_dispatch_invoked":False,"renderer_activation":False,"production_execution":False,"media_output_created":False,"output_artifact_path":None,"d4_8":"BLOCKED","release_authority":"NONE","video_render_ready":False}: raise ProfileIdentityError("Execution locks drift")
    approvals=spec.get("approval_state",{})
    if approvals.get("profile_identity_separation_approved") is not False or approvals.get("renderer_baseline_frozen") is not False or approvals.get("d4_8_authorized") is not False or approvals.get("release_authority")!="NONE": raise ProfileIdentityError("Audit cannot self-approve baseline or authority")
    sch=_json(root,SCHEMA_REL)
    if sch.get("$schema")!="https://json-schema.org/draft/2020-12/schema" or sch.get("additionalProperties") is not False: raise ProfileIdentityError("Strict schema missing")
    harness=(root/GDSCRIPT_REL).read_text(encoding="utf-8-sig")
    for token in ["RuntimeBridge.run_effective_pipeline(source)","PresentationBinder.bind(d_canonical, ctx.timeline, ctx.simulation_result)","source_presentation_profile", "winning_frame_unchanged", "renderer_native_input_emitted"]:
        if token not in harness: raise ProfileIdentityError(f"Harness token missing: {token}")
    for banned in ["FileAccess.open(OUTPUT", "RenderingServer", "Image.save_png", "MovieWriter", "--render", "renderer_dispatch("]:
        if banned in harness: raise ProfileIdentityError(f"Harness contains forbidden operation: {banned}")
    return {"contract":spec,"schema":sch,"lineage_count":len(seen),"challenge":challenge,"legacy_profile":legacy,"matching_timeline_profile":social,"delivery_profile":review}

def validate_record(record:dict[str,Any],project_root:Path | str | None=None)->bool:
    parsed=validate_contract(project_root); root=_root(project_root)
    if not isinstance(record,dict): raise ProfileIdentityError("Record must be a JSON object")
    if record.get("schema")!=OUTPUT_SCHEMA or record.get("schema_version")!="1.0" or record.get("status")!="IN_MEMORY_REVIEW_ONLY_NOT_RENDERER_INPUT": raise ProfileIdentityError("Record identity/status mismatch")
    expected_top={"schema","schema_version","status","frozen_c11c_manifest_sha256","challenge_source_sha256","identity_facts","runtime_rebind","simulation_invariance","execution_boundary"}
    if set(record)!=expected_top: raise ProfileIdentityError("Missing or unexpected top-level keys")
    if record.get("frozen_c11c_manifest_sha256")!=MANIFEST_SHA256: raise ProfileIdentityError("Manifest binding mismatch")
    if record.get("challenge_source_sha256")!=_sha(root/"challenges/CHALLENGE_004.json"): raise ProfileIdentityError("Challenge source hash mismatch")
    facts=record.get("identity_facts",{})
    expected_facts={"legacy_video_profile_id":"test_master_11s","legacy_video_profile_fps":30,"legacy_video_profile_duration_seconds":11.0,"inline_timeline_fps":60,"inline_timeline_duration_seconds":15.0,"inline_timeline_total_frames":900,"matching_named_timeline_profile_id":"parking_v2_social_15s","source_presentation_profile_id":"social_default_v1","legacy_runtime_bound_presentation_profile_id":"test_master_11s","d_presentation_profile_id":"social_default_v1","delivery_profile_id":"REVIEW_720","delivery_profile_fps":30,"delivery_width":720,"delivery_height":1280}
    if facts!=expected_facts: raise ProfileIdentityError("Profile identity facts do not match the explicit reconciliation contract")
    reb=record.get("runtime_rebind",{})
    if reb.get("runtime_success") is not True or reb.get("legacy_binding_success") is not True or reb.get("d_binding_success") is not True or reb.get("d_binding_profile_id")!="social_default_v1" or not re.fullmatch(r"[a-f0-9]{64}",str(reb.get("d_binding_render_model_sha256",""))): raise ProfileIdentityError("D presentation binding invalid")
    inv=record.get("simulation_invariance",{})
    for key in ["frame_signature_sha256_before","frame_signature_sha256_after"]:
        if not re.fullmatch(r"[a-f0-9]{64}",str(inv.get(key,""))): raise ProfileIdentityError("Invalid frame signature")
    if inv.get("frame_signature_sha256_before")!=inv.get("frame_signature_sha256_after") or inv.get("frame_signature_unchanged") is not True or inv.get("winning_frame_unchanged") is not True or inv.get("metrics_unchanged") is not True or inv.get("winning_frame_before")!=inv.get("winning_frame_after") or inv.get("game_frame_count_before")!=420 or inv.get("game_frame_count_after")!=420: raise ProfileIdentityError("Presentation rebind changed or cannot prove simulation invariance")
    boundary=record.get("execution_boundary",{})
    expected_boundary={"mode":"GODOT_HEADLESS_IN_MEMORY_REVIEW_ONLY","c11c_source_mutation":False,"runtime_report_file_written":False,"renderer_native_input_emitted":False,"renderer_dispatch_invoked":False,"renderer_activation":False,"production_execution":False,"media_output_created":False,"output_artifact_path":None,"d4_8":"BLOCKED","release_authority":"NONE"}
    if boundary!=expected_boundary: raise ProfileIdentityError("Execution boundary mismatch or privilege escalation")
    try:
        from jsonschema import Draft202012Validator
        Draft202012Validator(parsed["schema"]).validate(record)
    except ImportError: pass
    return True
