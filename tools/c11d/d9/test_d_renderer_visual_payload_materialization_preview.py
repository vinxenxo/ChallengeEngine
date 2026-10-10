from __future__ import annotations
import copy, json, re, sys
from pathlib import Path
from typing import Any, Callable
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
if str(HERE) not in sys.path: sys.path.insert(0,str(HERE))
from d_renderer_visual_payload_materialization_preview import validate_preview_contract, validate_preview_record, VisualPayloadPreviewError, MANIFEST_SHA256

HASH="a"*64

def _record(loop_duration: int = 22) -> dict[str,Any]:
    loop_frames=loop_duration*30
    return {
      "schema":"C11-D-D9-RENDERER-VISUAL-PAYLOAD-MATERIALIZATION-PREVIEW-V1",
      "schema_version":"1.0",
      "status":"IN_MEMORY_REVIEW_ONLY_NOT_RENDERER_INPUT",
      "frozen_c11c_manifest_sha256":MANIFEST_SHA256,
      "instances":[
        {"content_type":"visual_loops","instance_id":"D-VLP-1234567890abcdef","selection":{"family_id":"c11c_geometric_waves_v1","subtype_id":"harmonic_membrane"},"seed":12345,"variation_index":0,"fps":30,"duration_seconds":loop_duration,"frame_count":loop_frames,"authoring_envelope_sha256":HASH,"payload_instance_sha256":"b"*64,"materialization":"IN_MEMORY_ONLY","deterministic_repeat_pass":True,"instance_parameters_bound":True},
        {"content_type":"visual_drills","instance_id":"D-VDP-1234567890abcdef","selection":{"family_id":"tracking","variant_id":"tier-2"},"seed":12345,"variation_index":0,"fps":30,"duration_seconds":21,"frame_count":630,"authoring_envelope_sha256":"c"*64,"payload_instance_sha256":"d"*64,"materialization":"IN_MEMORY_ONLY","deterministic_repeat_pass":True,"instance_parameters_bound":True}
      ],
      "unmaterialized_content_types":["challenges"],
      "challenge_runtime_payload_materialized":False,
      "execution_boundary":{"mode":"IN_MEMORY_REVIEW_ONLY","payload_file_written":False,"renderer_native_input_emitted":False,"renderer_dispatch_invoked":False,"renderer_activation":False,"production_execution":False,"media_output_created":False,"output_artifact_path":None,"d4_8":"BLOCKED","release_authority":"NONE","c11c_source_mutation":False}
    }

def _reject(label: str, action: Callable[[],Any]) -> None:
    try: action()
    except (VisualPayloadPreviewError, ValueError, TypeError, KeyError): return
    raise AssertionError("Expected rejection: " + label)

def run_checks() -> dict[str,int]:
    parsed=validate_preview_contract(ROOT)
    schema=parsed["schema"]
    assert schema["$schema"]=="https://json-schema.org/draft/2020-12/schema" and schema["additionalProperties"] is False
    try: from jsonschema import Draft202012Validator
    except ImportError: Draft202012Validator=None
    if Draft202012Validator is not None: Draft202012Validator.check_schema(schema)
    base=_record()
    assert validate_preview_record(base,ROOT) is True
    jsonschema_count=0
    if Draft202012Validator is not None:
        Draft202012Validator(schema).validate(base)
        jsonschema_count=1
    negatives=[]
    mutations=[
      ("claim challenge materialized",lambda x:x.update(challenge_runtime_payload_materialized=True)),
      ("add challenge to instances",lambda x:x["instances"].append(copy.deepcopy(x["instances"][0]))),
      ("promote payload file written",lambda x:x["execution_boundary"].update(payload_file_written=True)),
      ("emit renderer input",lambda x:x["execution_boundary"].update(renderer_native_input_emitted=True)),
      ("invoke renderer dispatch",lambda x:x["execution_boundary"].update(renderer_dispatch_invoked=True)),
      ("activate renderer",lambda x:x["execution_boundary"].update(renderer_activation=True)),
      ("create media",lambda x:x["execution_boundary"].update(media_output_created=True)),
      ("authorize D4.8",lambda x:x["execution_boundary"].update(d4_8="AUTHORIZED")),
      ("grant release authority",lambda x:x["execution_boundary"].update(release_authority="PRODUCTION")),
      ("mutate C11-C",lambda x:x["execution_boundary"].update(c11c_source_mutation=True)),
      ("output path",lambda x:x["execution_boundary"].update(output_artifact_path="video.mp4")),
      ("mark persistent",lambda x:x["instances"][0].update(materialization="PERSISTED_FILE")),
      ("nondeterministic loop",lambda x:x["instances"][0].update(deterministic_repeat_pass=False)),
      ("unbound params",lambda x:x["instances"][1].update(instance_parameters_bound=False)),
      ("wrong loop grammar",lambda x:x["instances"][0]["selection"].update(subtype_id="invented_grammar")),
      ("wrong loop family",lambda x:x["instances"][0]["selection"].update(family_id="other_family")),
      ("wrong drill type",lambda x:x["instances"][1]["selection"].update(variant_id="tier-3")),
      ("wrong seed",lambda x:x["instances"][0].update(seed=999)),
      ("variation index not V1 fixture",lambda x:x["instances"][1].update(variation_index=1)),
      ("wrong FPS",lambda x:x["instances"][0].update(fps=24)),
      ("inconsistent frame count",lambda x:x["instances"][0].update(frame_count=1)),
      ("invalid duration",lambda x:x["instances"][1].update(duration_seconds=0)),
      ("malformed envelope hash",lambda x:x["instances"][0].update(authoring_envelope_sha256="bad")),
      ("malformed payload hash",lambda x:x["instances"][1].update(payload_instance_sha256="not-a-hash")),
      ("remove one content type",lambda x:x["instances"].pop()),
      ("duplicate content type",lambda x:x["instances"][1].update(content_type="visual_loops")),
      ("claim video ready extra field",lambda x:x.update(video_render_ready=True)),
      ("wrong frozen manifest",lambda x:x.update(frozen_c11c_manifest_sha256="0"*64)),
      ("unknown output status",lambda x:x.update(status="RENDERABLE")),
    ]
    for label,mutate in mutations:
        changed=copy.deepcopy(base); mutate(changed)
        _reject(label,lambda v=changed:validate_preview_record(v,ROOT)); negatives.append(label)
    # Contract source lineage, lock set, and approval states are separately checked on disk above.
    harness=parsed["harness"]
    assert "VisualAuthoringGeneratorScript.generate(request, context, {})" in harness
    assert "VisualDrillSeedVariation.gd" in harness and "C11CVariationProfile.gd" in harness
    assert "payload_file_written" in harness and "renderer_native_input_emitted" in harness
    assert len(parsed["source_lineage"])>=20
    assert parsed["source_lineage"][0]["sha256"]==MANIFEST_SHA256
    return {"content":2,"lineage":len(parsed["source_lineage"]),"schema":1,"jsonschema":jsonschema_count,"negative":len(negatives)}

if __name__=="__main__":
    c=run_checks()
    js=f"{c['jsonschema']}/1" if c["jsonschema"] else "NOT_INSTALLED (strict structural checks PASS)"
    print("C11-D RENDERER VISUAL PAYLOAD MATERIALIZATION PREVIEW CONTRACT PASS"
      +f" | content_types={c['content']}/2 | source_lineage={c['lineage']}/{c['lineage']} | negative={c['negative']}/29"
      +f" | schema=1/1 | jsonschema={js} | godot_harness=STATIC_REVIEW_ONLY"
      +" | challenge_runtime_payload=NOT_MATERIALIZED | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
