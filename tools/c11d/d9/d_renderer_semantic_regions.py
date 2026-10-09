"""Renderer semantic-region layout proposal; deterministic, in-memory, and non-renderable."""
from __future__ import annotations
import copy, hashlib, json
from collections.abc import Mapping
from pathlib import Path
from typing import Any
from d_renderer_candidate import sha256_json
from d_renderer_frame_program import (
    CONTRACT_REL as FRAME_CONTRACT_REL, OUTPUT_SCHEMA_REL as FRAME_SCHEMA_REL,
    PROGRAM_SCHEMA as FRAME_PROGRAM_SCHEMA, PROGRAM_STATUS as FRAME_PROGRAM_STATUS,
    DRendererFrameProgramError, validate_renderer_neutral_frame_program,
)
CONTRACT_REL=Path("definitions/c11d/production/D_RENDERER_SEMANTIC_REGION_PROPOSAL_V1.json")
OUTPUT_SCHEMA_REL=Path("definitions/c11d/production/D_RENDERER_SEMANTIC_REGION_PROPOSAL_SCHEMA_V1.json")
CONTRACT_SCHEMA="C11-D-RENDERER-SEMANTIC-REGION-PROPOSAL-CONTRACT-V1"
OUTPUT_SCHEMA="C11-D-D9-RENDERER-SEMANTIC-REGION-PROPOSAL-V1"
OUTPUT_STATUS="PREPARATION_ONLY_SEMANTIC_REGION_PROPOSAL_NOT_RENDERER_INPUT"
FIELD_TARGETS={"title":"HEADER","subtitle":"HEADER","player_name":"CHALLENGE_OVERLAY","challenge_label":"CHALLENGE_OVERLAY","call_to_action":"FOOTER"}
REGIONS=(
 {"region_id":"HEADER","semantic_scope":"EDITORIAL_TITLE_AND_SUBTITLE","mapped_fields":["title","subtitle"],"bounds_permille":{"x":50,"y":40,"width":900,"height":140},"layer_policy":"ABOVE_CONTENT_STAGE","overlap_policy":"NO_OVERLAP_WITH_CONTENT_STAGE_OR_FOOTER","geometry_state":"PROPOSED_NOT_APPROVED"},
 {"region_id":"CONTENT_STAGE","semantic_scope":"PRIMARY_CHALLENGE_OR_VISUAL_LOOP_OR_DRILL_CONTENT","mapped_fields":[],"bounds_permille":{"x":35,"y":200,"width":930,"height":610},"layer_policy":"PRIMARY_VISUAL_STAGE","overlap_policy":"CHALLENGE_OVERLAY_MAY_OVERLAP_CONTENT_STAGE","geometry_state":"PROPOSED_NOT_APPROVED","payload_contract":"NOT_DEFINED_NOT_BOUND"},
 {"region_id":"CHALLENGE_OVERLAY","semantic_scope":"CHALLENGE_SPECIFIC_EDITORIAL_LABELS","mapped_fields":["player_name","challenge_label"],"bounds_permille":{"x":70,"y":705,"width":860,"height":85},"layer_policy":"OVERLAY_ABOVE_CONTENT_STAGE","overlap_policy":"INTENTIONAL_CONTAINED_OVERLAP_WITH_CONTENT_STAGE","geometry_state":"PROPOSED_NOT_APPROVED"},
 {"region_id":"FOOTER","semantic_scope":"EDITORIAL_CALL_TO_ACTION","mapped_fields":["call_to_action"],"bounds_permille":{"x":50,"y":850,"width":900,"height":100},"layer_policy":"BELOW_CONTENT_STAGE","overlap_policy":"NO_OVERLAP_WITH_HEADER_OR_CONTENT_STAGE","geometry_state":"PROPOSED_NOT_APPROVED"},
)
class DRendererSemanticRegionError(ValueError):
    """Raised for invalid lineage or an invalid/unapproved semantic-region proposal."""
def _root(project_root: Path|str|None=None)->Path:
    return Path(project_root).resolve() if project_root is not None else Path(__file__).resolve().parents[3]
def _read_json(path:Path)->dict[str,Any]:
    try: v=json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc: raise DRendererSemanticRegionError(f"Cannot read required semantic-region contract input {path}: {exc}") from exc
    if not isinstance(v,dict): raise DRendererSemanticRegionError(f"Expected JSON object in {path}")
    return v
def _file_sha256(path:Path)->str:
    try: return hashlib.sha256(path.read_bytes()).hexdigest()
    except Exception as exc: raise DRendererSemanticRegionError(f"Cannot hash {path}: {exc}") from exc
def _load_contract(root:Path):
    c=_read_json(root/CONTRACT_REL); s=_read_json(root/OUTPUT_SCHEMA_REL)
    if c.get("schema")!=CONTRACT_SCHEMA or c.get("schema_version")!="1.0" or c.get("status")!="PREPARATION_ONLY_NOT_APPROVED_NOT_FROZEN":
        raise DRendererSemanticRegionError("Semantic-region contract identity/status mismatch")
    if c.get("field_targets")!=FIELD_TARGETS or c.get("regions")!=list(REGIONS):
        raise DRendererSemanticRegionError("Semantic-region field/geometry proposal changed without review")
    locks={"source_adapter_mode":"PREPARE_ONLY","region_layout_approved":False,"pixel_coordinates_emitted":False,"frame_schedule_defined":False,"renderer_native_input_emitted":False,"renderer_dispatch_invoked":False,"renderer_activation":False,"production_execution":False,"media_output_created":False,"output_artifact_path":None,"d4_8":"BLOCKED","release_authority":"NONE","c11c_source_mutation":False}
    if c.get("required_locks")!=locks: raise DRendererSemanticRegionError("Semantic-region proposal lock mismatch")
    approval={"semantic_region_mapping_approved":False,"temporal_schedule_approved":False,"renderer_baseline_approved":False,"renderer_baseline_frozen":False,"d4_8_authorized":False,"d9_14_full_acceptance":"BLOCKED_AS_REQUIRED","d9_16_full_acceptance":"BLOCKED_AS_REQUIRED","d9_17_closure":"BLOCKED_NO_GO","release_authority":"NONE"}
    if c.get("approval_state")!=approval: raise DRendererSemanticRegionError("Semantic-region proposal cannot self-approve or grant authority")
    if s.get("$schema")!="https://json-schema.org/draft/2020-12/schema" or s.get("$id")!="urn:c11d:renderer-semantic-region-proposal:v1" or s.get("additionalProperties") is not False:
        raise DRendererSemanticRegionError("Semantic-region strict JSON Schema identity mismatch")
    framec=_read_json(root/FRAME_CONTRACT_REL); frames=_read_json(root/FRAME_SCHEMA_REL)
    if framec.get("schema")!="C11-D-RENDERER-NEUTRAL-FRAME-PROGRAM-CONTRACT-V1" or framec.get("status")!="PREPARATION_ONLY_NOT_APPROVED_NOT_FROZEN" or frames.get("$id")!="urn:c11d:renderer-neutral-frame-program:v1":
        raise DRendererSemanticRegionError("Source frame-program contract/schema identity mismatch")
    return c,s,framec,frames
def _build_core(frame_program:Mapping[str,Any],root:Path,c:Mapping[str,Any],s:Mapping[str,Any],framec:Mapping[str,Any],frames:Mapping[str,Any])->dict[str,Any]:
    if frame_program.get("schema")!=FRAME_PROGRAM_SCHEMA or frame_program.get("status")!=FRAME_PROGRAM_STATUS:
        raise DRendererSemanticRegionError("Unsupported source frame-program status/schema")
    if frame_program.get("execution_boundary",{}).get("renderer_activation") is not False or frame_program.get("execution_boundary",{}).get("media_output_created") is not False:
        raise DRendererSemanticRegionError("Source frame program violates renderer/media locks")
    src=frame_program.get("source_identity")
    content=frame_program.get("content_identity")
    canvas=frame_program.get("canvas_descriptor")
    if not isinstance(src,Mapping) or not isinstance(content,Mapping) or not isinstance(canvas,Mapping): raise DRendererSemanticRegionError("Source identity/content/canvas missing")
    if content.get("content_type") not in ("challenges","visual_loops","visual_drills"): raise DRendererSemanticRegionError("Unsupported content type; Longform/unknown fail closed")
    instructions=frame_program.get("instructions")
    if not isinstance(instructions,list): raise DRendererSemanticRegionError("Frame-program instructions must be a list")
    bindings=[]
    for instruction in instructions:
        sf=instruction.get("source_field"); region=FIELD_TARGETS.get(sf)
        if region is None or instruction.get("region_id")!=region: raise DRendererSemanticRegionError(f"Frame-program source field/region mismatch: {sf}")
        bindings.append({"element_id":instruction.get("element_id"),"source_field":sf,"region_id":region,"text_sha256":instruction.get("text_sha256"),"mapping_state":"PROPOSED_NOT_APPROVED"})
    if len(bindings)<3 or len(bindings)>5 or len({b['element_id'] for b in bindings})!=len(bindings): raise DRendererSemanticRegionError("Invalid/duplicate source text binding count")
    raw={
      "schema":OUTPUT_SCHEMA,"schema_version":"1.0","status":OUTPUT_STATUS,
      "contract_identity":{"schema":c["schema"],"schema_version":c["schema_version"],"sha256":_file_sha256(root/CONTRACT_REL),"output_schema_sha256":_file_sha256(root/OUTPUT_SCHEMA_REL),"frame_program_contract_sha256":_file_sha256(root/FRAME_CONTRACT_REL),"frame_program_schema_sha256":_file_sha256(root/FRAME_SCHEMA_REL)},
      "source_identity":{**dict(src),"frame_program_sha256":frame_program.get("program_sha256")},
      "content_identity":copy.deepcopy(dict(content)),
      "canvas_descriptor":{"delivery_profile_requested_id":canvas.get("delivery_profile_requested_id"),"delivery_profile_resolved_id":canvas.get("delivery_profile_resolved_id"),"width":canvas.get("width"),"height":canvas.get("height"),"aspect_ratio":canvas.get("aspect_ratio"),"fps":canvas.get("fps"),"pixel_format":canvas.get("pixel_format"),"canvas_semantics":"DELIVERY_PROFILE_METADATA_ONLY_NOT_RENDER_AUTHORIZATION"},
      "coordinate_model":{"space":"NORMALIZED_PERMILLE","x_axis_max":1000,"y_axis_max":1000,"pixel_coordinates_emitted":False,"layout_state":"PROPOSED_NOT_APPROVED"},
      "regions":copy.deepcopy(list(REGIONS)),
      "text_element_bindings":bindings,
      "timing_model":{"state":"NOT_DEFINED","frame_schedule_defined":False,"durations_emitted":False},
      "execution_boundary":{"proposal_only":True,"region_layout_approved":False,"pixel_coordinates_emitted":False,"frame_schedule_defined":False,"renderer_native_input_emitted":False,"renderer_dispatch_invoked":False,"renderer_activation":False,"production_execution":False,"media_output_created":False,"output_artifact_path":None,"d4_8":"BLOCKED","release_authority":"NONE","c11c_source_mutation":False}
    }
    raw['layout_sha256']=sha256_json(raw)
    return raw
def build_semantic_region_proposal(frame_program:Mapping[str,Any],composition:Mapping[str,Any],preview:Mapping[str,Any],envelope:Mapping[str,Any],project_root:Path|str|None=None)->dict[str,Any]:
    root=_root(project_root)
    try: validate_renderer_neutral_frame_program(frame_program,composition,preview,envelope,root)
    except Exception as exc: raise DRendererSemanticRegionError(f"Source frame-program validation failed: {exc}") from exc
    c,s,framec,frames=_load_contract(root)
    out=_build_core(frame_program,root,c,s,framec,frames)
    validate_semantic_region_proposal(out,frame_program,composition,preview,envelope,root)
    return out
def validate_semantic_region_proposal(candidate:Mapping[str,Any],frame_program:Mapping[str,Any],composition:Mapping[str,Any],preview:Mapping[str,Any],envelope:Mapping[str,Any],project_root:Path|str|None=None)->bool:
    root=_root(project_root)
    try: validate_renderer_neutral_frame_program(frame_program,composition,preview,envelope,root)
    except Exception as exc: raise DRendererSemanticRegionError(f"Source frame-program validation failed: {exc}") from exc
    c,s,framec,frames=_load_contract(root)
    expected=_build_core(frame_program,root,c,s,framec,frames)
    if dict(candidate)!=expected: raise DRendererSemanticRegionError("Semantic-region proposal differs from independently rebuilt proposal/lineage/locks")
    return True
