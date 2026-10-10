from __future__ import annotations
import copy, hashlib, json, math, re, sys
from pathlib import Path
from typing import Any, Callable
HERE=Path(__file__).resolve().parent
if str(HERE) not in sys.path: sys.path.insert(0,str(HERE))
from d_renderer_challenge_runtime_output_preview import validate_preview_contract, validate_preview_record, ChallengeRuntimePreviewError, MANIFEST_SHA256
ROOT=Path(__file__).resolve().parents[3]
HASH="a"*64

def _record() -> dict[str,Any]:
    return {
      "schema":"C11-D-D9-RENDERER-CHALLENGE-RUNTIME-OUTPUT-PREVIEW-V1","schema_version":"1.0","status":"IN_MEMORY_REVIEW_ONLY_NOT_RENDERER_INPUT",
      "frozen_c11c_manifest_sha256":MANIFEST_SHA256,"challenge_source_sha256":hashlib.sha256((ROOT/"challenges/CHALLENGE_004.json").read_bytes()).hexdigest(),
      "challenge_runtime_output_materialized":True,"challenge_visual_payload_materialized":False,
      "instance":{
        "content_type":"challenges","challenge_id":"CHALLENGE_004","mechanic":"parking_v2","mechanic_version":"2.0","asset_family":"fam_garage_01","asset_family_version":"1.0",
        "seed_requested":314159,"seed_used":314159,"rng_version":"2.0","editorial_content":{"hook":"¡SOLO EL 1% APARCA SIN ROZAR!","reveal":"","cta":"¿Lo has clavado?"},
        "fps":60,"phase_frames":{"hook":180,"game":420,"reveal":180,"cta":120},"total_frames":900,"duration_seconds":15.0,"game_frame_count":420,
        "winning_frame_local":210,"score":0.8,"minimum_distance":2.5,"tolerance_threshold":15.0,"simulation_error_state":"OK","attempts":1,
        "frame_signature_sha256":HASH,"presentation_binding_success":True,"presentation_profile_id":"social_default_v1",
        "physical_asset_bindings":{"background_path":"res://assets/c6/garage_background.svg","target_path":"res://assets/c6/parking_target.svg","object_path":"res://assets/c6/car.svg"},
        "presentation_render_model_sha256":HASH,"runtime_output_sha256":HASH,"materialization":"IN_MEMORY_ONLY_RUNTIME_RESULT_NOT_VISUAL_PAYLOAD"
      },"deterministic_repeat_pass":True,
      "execution_boundary":{"mode":"GODOT_HEADLESS_IN_MEMORY_REVIEW_ONLY","runtime_called":True,"simulation_executed":True,"runtime_report_file_written":False,"renderer_native_input_emitted":False,"renderer_dispatch_invoked":False,"renderer_activation":False,"production_execution":False,"media_output_created":False,"output_artifact_path":None,"d4_8":"BLOCKED","release_authority":"NONE","c11c_source_mutation":False}
    }

def _reject(label:str, action:Callable[[],Any])->None:
    try: action()
    except (ChallengeRuntimePreviewError,ValueError,TypeError,KeyError): return
    raise AssertionError("Expected rejection: "+label)

def run_checks()->dict[str,int]:
    parsed=validate_preview_contract(ROOT); schema=parsed["schema"]
    assert schema.get("$schema")=="https://json-schema.org/draft/2020-12/schema" and schema.get("additionalProperties") is False
    try: from jsonschema import Draft202012Validator
    except ImportError: Draft202012Validator=None
    if Draft202012Validator is not None: Draft202012Validator.check_schema(schema)
    record=_record(); assert validate_preview_record(record,ROOT)
    jsonschema_count=0
    if Draft202012Validator is not None:
        Draft202012Validator(schema).validate(record); jsonschema_count=1
    mutations=[
      ("wrong challenge ID",lambda x:x["instance"].update(challenge_id="CHALLENGE_001")),
      ("wrong mechanic",lambda x:x["instance"].update(mechanic="pilot")),
      ("wrong mechanic version",lambda x:x["instance"].update(mechanic_version="1.0")),
      ("wrong family",lambda x:x["instance"].update(asset_family="fam_001")),
      ("wrong family version",lambda x:x["instance"].update(asset_family_version="2.0")),
      ("wrong requested seed",lambda x:x["instance"].update(seed_requested=999)),
      ("wrong rng version",lambda x:x["instance"].update(rng_version="1.0")),
      ("wrong FPS",lambda x:x["instance"].update(fps=30)),
      ("wrong hook frames",lambda x:x["instance"]["phase_frames"].update(hook=181)),
      ("wrong game frames",lambda x:x["instance"]["phase_frames"].update(game=421)),
      ("wrong reveal frames",lambda x:x["instance"]["phase_frames"].update(reveal=0)),
      ("wrong CTA frames",lambda x:x["instance"]["phase_frames"].update(cta=60)),
      ("wrong total frames",lambda x:x["instance"].update(total_frames=901)),
      ("wrong duration",lambda x:x["instance"].update(duration_seconds=14.9)),
      ("wrong game output frame count",lambda x:x["instance"].update(game_frame_count=419)),
      ("winning frame no longer local",lambda x:x["instance"].update(winning_frame_local=420)),
      ("negative frame index",lambda x:x["instance"].update(winning_frame_local=-2)),
      ("invalid score high",lambda x:x["instance"].update(score=1.1)),
      ("invalid score NaN",lambda x:x["instance"].update(score=float("nan"))),
      ("invalid distance",lambda x:x["instance"].update(minimum_distance=-1)),
      ("invalid tolerance",lambda x:x["instance"].update(tolerance_threshold=-1)),
      ("simulation error",lambda x:x["instance"].update(simulation_error_state="ERROR")),
      ("no presentation binding",lambda x:x["instance"].update(presentation_binding_success=False)),
      ("editorial hook drift",lambda x:x["instance"]["editorial_content"].update(hook="invented")),
      ("editorial CTA drift",lambda x:x["instance"]["editorial_content"].update(cta="invented")),
      ("asset path not res",lambda x:x["instance"]["physical_asset_bindings"].update(background_path="C:/image.svg")),
      ("bad frame digest",lambda x:x["instance"].update(frame_signature_sha256="bad")),
      ("bad model digest",lambda x:x["instance"].update(presentation_render_model_sha256="bad")),
      ("bad output digest",lambda x:x["instance"].update(runtime_output_sha256="bad")),
      ("non-deterministic repeats",lambda x:x.update(deterministic_repeat_pass=False)),
      ("claim visual payload ready",lambda x:x.update(challenge_visual_payload_materialized=True)),
      ("claim output file written",lambda x:x["execution_boundary"].update(runtime_report_file_written=True)),
      ("emit renderer input",lambda x:x["execution_boundary"].update(renderer_native_input_emitted=True)),
      ("dispatch renderer",lambda x:x["execution_boundary"].update(renderer_dispatch_invoked=True)),
      ("activate renderer",lambda x:x["execution_boundary"].update(renderer_activation=True)),
      ("create media",lambda x:x["execution_boundary"].update(media_output_created=True)),
      ("authorize D4.8",lambda x:x["execution_boundary"].update(d4_8="AUTHORIZED")),
      ("grant release authority",lambda x:x["execution_boundary"].update(release_authority="PRODUCTION")),
      ("mutate C11-C",lambda x:x["execution_boundary"].update(c11c_source_mutation=True)),
      ("write output path",lambda x:x["execution_boundary"].update(output_artifact_path="challenge.json")),
      ("wrong source manifest",lambda x:x.update(frozen_c11c_manifest_sha256="0"*64)),
      ("wrong challenge source hash",lambda x:x.update(challenge_source_sha256="0"*64)),
      ("mark persistent output",lambda x:x["instance"].update(materialization="PERSISTED")),
      ("add unexpected field",lambda x:x.update(renderer_input=True)),
    ]
    for label,mutate in mutations:
        changed=copy.deepcopy(record); mutate(changed); _reject(label,lambda r=changed:validate_preview_record(r,ROOT))
    assert len(parsed["source_lineage"])>=16
    return {"content":1,"lineage":len(parsed["source_lineage"]),"schema":1,"jsonschema":jsonschema_count,"negative":len(mutations)}

if __name__=="__main__":
    c=run_checks(); js=f"{c['jsonschema']}/1" if c["jsonschema"] else "NOT_INSTALLED (strict structural checks PASS)"
    print("C11-D RENDERER CHALLENGE RUNTIME OUTPUT PREVIEW CONTRACT PASS"+f" | content_types={c['content']}/1 | source_lineage={c['lineage']}/{c['lineage']} | negative={c['negative']}/{c['negative']} | schema=1/1 | jsonschema={js} | godot_harness=STATIC_REVIEW_ONLY | challenge_runtime_result=NOT_RUN_BY_PYTHON | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
