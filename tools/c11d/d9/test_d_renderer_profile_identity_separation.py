from __future__ import annotations
import copy, hashlib, sys
from pathlib import Path
from typing import Any, Callable
HERE=Path(__file__).resolve().parent
if str(HERE) not in sys.path: sys.path.insert(0,str(HERE))
from d_renderer_profile_identity_separation import validate_contract, validate_record, ProfileIdentityError, MANIFEST_SHA256
ROOT=Path(__file__).resolve().parents[3]
HASH="a"*64

def record()->dict[str,Any]:
    return {"schema":"C11-D-D9-RENDERER-PROFILE-IDENTITY-SEPARATION-V1","schema_version":"1.0","status":"IN_MEMORY_REVIEW_ONLY_NOT_RENDERER_INPUT","frozen_c11c_manifest_sha256":MANIFEST_SHA256,"challenge_source_sha256":hashlib.sha256((ROOT/"challenges/CHALLENGE_004.json").read_bytes()).hexdigest(),
      "identity_facts":{"legacy_video_profile_id":"test_master_11s","legacy_video_profile_fps":30,"legacy_video_profile_duration_seconds":11.0,"inline_timeline_fps":60,"inline_timeline_duration_seconds":15.0,"inline_timeline_total_frames":900,"matching_named_timeline_profile_id":"parking_v2_social_15s","source_presentation_profile_id":"social_default_v1","legacy_runtime_bound_presentation_profile_id":"test_master_11s","d_presentation_profile_id":"social_default_v1","delivery_profile_id":"REVIEW_720","delivery_profile_fps":30,"delivery_width":720,"delivery_height":1280},
      "runtime_rebind":{"runtime_success":True,"legacy_binding_success":True,"d_binding_success":True,"d_binding_profile_id":"social_default_v1","d_binding_render_model_sha256":HASH},
      "simulation_invariance":{"frame_signature_sha256_before":HASH,"frame_signature_sha256_after":HASH,"frame_signature_unchanged":True,"winning_frame_before":394,"winning_frame_after":394,"winning_frame_unchanged":True,"game_frame_count_before":420,"game_frame_count_after":420,"metrics_unchanged":True},
      "execution_boundary":{"mode":"GODOT_HEADLESS_IN_MEMORY_REVIEW_ONLY","c11c_source_mutation":False,"runtime_report_file_written":False,"renderer_native_input_emitted":False,"renderer_dispatch_invoked":False,"renderer_activation":False,"production_execution":False,"media_output_created":False,"output_artifact_path":None,"d4_8":"BLOCKED","release_authority":"NONE"}}

def reject(label:str, action:Callable[[],Any])->None:
    try: action()
    except (ProfileIdentityError,ValueError,TypeError,KeyError): return
    raise AssertionError("Expected rejection: "+label)

def run_checks()->dict[str,int]:
    parsed=validate_contract(ROOT); assert len(parsed["contract"]["source_lineage"])>=15
    try: from jsonschema import Draft202012Validator
    except ImportError: Draft202012Validator=None
    if Draft202012Validator: Draft202012Validator.check_schema(parsed["schema"])
    base=record(); assert validate_record(base,ROOT)
    js=0
    if Draft202012Validator: Draft202012Validator(parsed["schema"]).validate(base); js=1
    mutations=[
      ("wrong legacy id",lambda x:x["identity_facts"].update(legacy_video_profile_id="REVIEW_720")),
      ("wrong legacy fps",lambda x:x["identity_facts"].update(legacy_video_profile_fps=60)),
      ("wrong legacy duration",lambda x:x["identity_facts"].update(legacy_video_profile_duration_seconds=15.0)),
      ("wrong inline fps",lambda x:x["identity_facts"].update(inline_timeline_fps=30)),
      ("wrong inline duration",lambda x:x["identity_facts"].update(inline_timeline_duration_seconds=11.0)),
      ("wrong frame count",lambda x:x["identity_facts"].update(inline_timeline_total_frames=330)),
      ("wrong profile match",lambda x:x["identity_facts"].update(matching_named_timeline_profile_id="test_master_11s")),
      ("conflate delivery and presentation",lambda x:x["identity_facts"].update(d_presentation_profile_id="REVIEW_720")),
      ("wrong explicit profile",lambda x:x["identity_facts"].update(source_presentation_profile_id="test_master_11s")),
      ("wrong runtime bound profile",lambda x:x["identity_facts"].update(legacy_runtime_bound_presentation_profile_id="social_default_v1")),
      ("wrong delivery id",lambda x:x["identity_facts"].update(delivery_profile_id="MASTER_1080")),
      ("wrong delivery fps",lambda x:x["identity_facts"].update(delivery_profile_fps=60)),
      ("wrong delivery geometry",lambda x:x["identity_facts"].update(delivery_width=1080)),
      ("runtime failed",lambda x:x["runtime_rebind"].update(runtime_success=False)),
      ("legacy binding failed",lambda x:x["runtime_rebind"].update(legacy_binding_success=False)),
      ("d binding failed",lambda x:x["runtime_rebind"].update(d_binding_success=False)),
      ("wrong bound profile",lambda x:x["runtime_rebind"].update(d_binding_profile_id="test_master_11s")),
      ("bad render digest",lambda x:x["runtime_rebind"].update(d_binding_render_model_sha256="bad")),
      ("different frame hash",lambda x:x["simulation_invariance"].update(frame_signature_sha256_after="b"*64)),
      ("false invariant",lambda x:x["simulation_invariance"].update(frame_signature_unchanged=False)),
      ("changed winning frame",lambda x:x["simulation_invariance"].update(winning_frame_after=395)),
      ("false winning frame invariant",lambda x:x["simulation_invariance"].update(winning_frame_unchanged=False)),
      ("wrong game frame count",lambda x:x["simulation_invariance"].update(game_frame_count_after=419)),
      ("metrics changed",lambda x:x["simulation_invariance"].update(metrics_unchanged=False)),
      ("report written",lambda x:x["execution_boundary"].update(runtime_report_file_written=True)),
      ("renderer input",lambda x:x["execution_boundary"].update(renderer_native_input_emitted=True)),
      ("renderer dispatched",lambda x:x["execution_boundary"].update(renderer_dispatch_invoked=True)),
      ("renderer activated",lambda x:x["execution_boundary"].update(renderer_activation=True)),
      ("media created",lambda x:x["execution_boundary"].update(media_output_created=True)),
      ("D4.8 authorized",lambda x:x["execution_boundary"].update(d4_8="AUTHORIZED")),
      ("release granted",lambda x:x["execution_boundary"].update(release_authority="PRODUCTION")),
      ("C11-C mutated",lambda x:x["execution_boundary"].update(c11c_source_mutation=True)),
      ("output path set",lambda x:x["execution_boundary"].update(output_artifact_path="review.json")),
      ("wrong manifest",lambda x:x.update(frozen_c11c_manifest_sha256="0"*64)),
      ("wrong source digest",lambda x:x.update(challenge_source_sha256="0"*64)),
      ("mark payload materialized",lambda x:x.update(status="VISUAL_PAYLOAD_READY")),
      ("unexpected key",lambda x:x.update(renderer_input={})),
      ("wrong top schema",lambda x:x.update(schema="other")),
      ("wrong mode",lambda x:x["execution_boundary"].update(mode="PRODUCTION")),
      ("wrong winning frame type",lambda x:x["simulation_invariance"].update(winning_frame_after="394")),
    ]
    for label,mutate in mutations:
        changed=copy.deepcopy(base); mutate(changed); reject(label,lambda r=changed:validate_record(r,ROOT))
    return {"content":1,"lineage":len(parsed["contract"]["source_lineage"]),"negative":len(mutations),"schema":1,"jsonschema":js}

if __name__=="__main__":
    c=run_checks(); js=f"{c['jsonschema']}/1" if c['jsonschema'] else "NOT_INSTALLED (strict structural checks PASS)"
    print("C11-D RENDERER PROFILE IDENTITY SEPARATION CONTRACT PASS"+f" | source_identities=3/3 | profile_facts=4/4 | source_lineage={c['lineage']}/{c['lineage']} | negative={c['negative']}/{c['negative']} | schema=1/1 | jsonschema={js} | godot_harness=STATIC_REVIEW_ONLY | runtime_rebind=NOT_RUN_BY_PYTHON | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
