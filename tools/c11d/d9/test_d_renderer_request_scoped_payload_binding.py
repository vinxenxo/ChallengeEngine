from __future__ import annotations
import ast, copy, hashlib, json, sys
from pathlib import Path
from typing import Any, Callable
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
if str(HERE) not in sys.path: sys.path.insert(0,str(HERE))
from universal_producer import REQUEST_SCHEMA_ID, evaluate_universal_request
from editorial_render_bridge import build_bridge_planning_record
from d_render_adapter import prepare_d_only_adapter_envelope
from d_renderer_request_scoped_payload_binding import build_request_scoped_payload_binding, validate_request_scoped_payload_binding, DRendererRequestScopedPayloadBindingError, _sha

def _raw(selection: dict[str,Any], request_id: str) -> dict[str,Any]:
    return {"schema":REQUEST_SCHEMA_ID,"schema_version":"1.0","request_id":request_id,"mode":"REVIEW","selection":selection,
      "seed":12345,"music_seed":840001,"delivery_profile_id":"REVIEW_720","presentation_profile_id":"social_default_v1",
      "variation_index":0,"audio_enabled":True,"personalization_enabled":True,"editorial_profile":{},
      "production_override":{"title":"Prueba editorial · título","subtitle":"Subtítulo de revisión","call_to_action":"Continuar","language":"es", **({"player_name":"ANA","challenge_label":"RETO"} if selection["content_type"]=="challenges" else {})},
      "provenance":{"source_revision":"C11D-D9.9-0.11.1","request_origin":"TEST"}}

def _fixtures() -> dict[str,dict[str,Any]]:
    return {"challenges":{"content_type":"challenges","family_id":"parking_v2","variant_id":"CHALLENGE_004"},
      "visual_loops":{"content_type":"visual_loops","family_id":"c11c_geometric_waves_v1","subtype_id":"harmonic_membrane"},
      "visual_drills":{"content_type":"visual_drills","family_id":"tracking","variant_id":"tier-2"}}

def _chain(selection: dict[str,Any], request_id: str):
    result=evaluate_universal_request(_raw(selection,request_id),ROOT)
    bridge=build_bridge_planning_record(result,ROOT)
    envelope=prepare_d_only_adapter_envelope(result,bridge,ROOT)
    return result,bridge,envelope

def _reject(label: str, action: Callable[[],Any]) -> None:
    try: action()
    except (DRendererRequestScopedPayloadBindingError,ValueError,TypeError,KeyError): return
    raise AssertionError(f"Expected rejection: {label}")

def run_checks() -> dict[str,int]:
    src=(HERE/"d_renderer_request_scoped_payload_binding.py").read_text(encoding="utf-8")
    tree=ast.parse(src)
    forbidden_modules={"subprocess","socket","multiprocessing","ffmpeg","godot"}
    forbidden_calls={"write_text","write_bytes","Popen","system","startfile","check_call","check_output","dispatch","render","render_video"}
    for node in ast.walk(tree):
        if isinstance(node,ast.Import): assert not any(alias.name.split('.')[0] in forbidden_modules for alias in node.names)
        elif isinstance(node,ast.ImportFrom): assert (node.module or '').split('.')[0] not in forbidden_modules
        elif isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute): assert node.func.attr not in forbidden_calls, f"Side effect call in binding module: {node.func.attr}"
    schema=json.loads((ROOT/"definitions/c11d/production/D_RENDERER_REQUEST_SCOPED_PAYLOAD_BINDING_SCHEMA_V1.json").read_text(encoding="utf-8-sig"))
    assert schema["$schema"]=="https://json-schema.org/draft/2020-12/schema" and schema["additionalProperties"] is False
    assert set(schema["required"])==set(schema["properties"])
    try: from jsonschema import Draft202012Validator
    except ImportError: Draft202012Validator=None
    if Draft202012Validator is not None: Draft202012Validator.check_schema(schema)
    counts={"content":0,"deterministic":0,"chain":0,"source":0,"schema":0,"jsonschema":0}
    built={}
    for content_type,selection in _fixtures().items():
        result,bridge,envelope=_chain(selection,f"D-PAYLOAD-BIND-{content_type.upper()}")
        record=build_request_scoped_payload_binding(result,bridge,envelope,ROOT)
        assert record==build_request_scoped_payload_binding(copy.deepcopy(result),copy.deepcopy(bridge),copy.deepcopy(envelope),ROOT)
        assert validate_request_scoped_payload_binding(record,result,bridge,envelope,ROOT) is True
        assert record["content_type"]==content_type
        assert record["readiness"]=={"canonical_selection_resolved":True,"source_definition_hash_bound":True,"selected_family_or_variant_reference_resolved":True,"request_scoped_visual_payload_instance_bound":False,"payload_instance_materialized":False,"editorial_review_chain_passed":True,"video_render_ready":False}
        assert record["source_binding"]["exact_request_payload_instance_materialized"] is False
        assert record["source_binding"]["payload_instance_id"] is None and record["source_binding"]["payload_instance_sha256"] is None
        assert record["execution_boundary"]["renderer_native_input_emitted"] is False and record["execution_boundary"]["d4_8"]=="BLOCKED"
        assert record["source_identity"]["request_hash"]==result["request_hash"]
        assert record["source_identity"]["bridge_record_hash"]==bridge["record_hash"]
        assert record["source_identity"]["adapter_envelope_hash"]==envelope["envelope_hash"]
        assert record["source_identity"]["frozen_c11c_manifest_sha256"]=="e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
        assert record["binding_sha256"]==_sha({k:v for k,v in record.items() if k!="binding_sha256"})
        for key in ("request_hash","plan_hash","bridge_record_hash","adapter_envelope_hash","binding_preview_sha256","logical_composition_sha256","frame_program_sha256","temporal_preview_sha256","delivery_projection_sha256","editorial_review_manifest_sha256","definition_source_sha256","registry_sha256","source_lineage_sha256"):
            value=record["source_identity"][key]; assert isinstance(value,str) and len(value)==64 and all(c in "0123456789abcdef" for c in value)
        if content_type=="challenges":
            assert record["source_binding"]["resolved_identity"]["challenge_id"]=="CHALLENGE_004"
            assert record["source_binding"]["selection_resolution_state"]=="EXACT_CHALLENGE_SOURCE_RESOLVED_RUNTIME_MEDIA_PAYLOAD_NOT_MATERIALIZED"
        elif content_type=="visual_loops":
            assert record["source_binding"]["resolved_identity"]["selected_grammar_id"]=="harmonic_membrane"
            assert record["source_binding"]["source_class"]=="FAMILY_CANONICAL_VISUAL_LOOP_DEFINITION_NOT_GRAMMAR_INSTANCE"
            assert record["source_binding"]["selected_grammar_materialized"] is False
        else:
            assert record["source_binding"]["resolved_identity"]["selected_tier"]==2
            assert record["source_binding"]["selected_tier_materialized"] is True
            assert record["source_binding"]["exact_request_payload_instance_materialized"] is False
        assert set(record)==set(schema["required"])
        if Draft202012Validator is not None:
            Draft202012Validator(schema).validate(record); counts["jsonschema"]+=1
        counts["content"]+=1; counts["deterministic"]+=1; counts["chain"]+=1; counts["source"]+=1; counts["schema"]+=1
        built[content_type]=(record,result,bridge,envelope)
    negatives=[]
    for content_type,(base,result,bridge,envelope) in built.items():
        mutations=[
          ("forged request hash",lambda x:x["source_identity"].update(request_hash="0"*64)),
          ("forged plan hash",lambda x:x["source_identity"].update(plan_hash="0"*64)),
          ("forged definition sha",lambda x:x["source_binding"]["definition_reference"].update(sha256="0"*64)),
          ("wrong definition path",lambda x:x["source_binding"]["definition_reference"].update(path="fake.json")),
          ("promote instance materialized",lambda x:x["source_binding"].update(exact_request_payload_instance_materialized=True)),
          ("invent instance id",lambda x:x["source_binding"].update(payload_instance_id="made-up")),
          ("invent instance sha",lambda x:x["source_binding"].update(payload_instance_sha256="0"*64)),
          ("invent output path",lambda x:x["source_binding"].update(payload_output_path="out.mp4")),
          ("wrong selected identity",lambda x:x["source_binding"]["resolved_identity"].update(fake_id="wrong")),
          ("promote render readiness",lambda x:x["readiness"].update(video_render_ready=True)),
          ("claim request instance bound",lambda x:x["readiness"].update(request_scoped_visual_payload_instance_bound=True)),
          ("enable renderer",lambda x:x["execution_boundary"].update(renderer_activation=True)),
          ("emit renderer input",lambda x:x["execution_boundary"].update(renderer_native_input_emitted=True)),
          ("create media",lambda x:x["execution_boundary"].update(media_output_created=True)),
          ("authorize d4.8",lambda x:x["execution_boundary"].update(d4_8="AUTHORIZED")),
          ("grant release authority",lambda x:x["execution_boundary"].update(release_authority="PRODUCTION")),
        ]
        for label,mutate in mutations:
            changed=copy.deepcopy(base); mutate(changed); _reject(f"{content_type}:{label}",lambda c=changed:validate_request_scoped_payload_binding(c,result,bridge,envelope,ROOT)); negatives.append(label)
    # Source-chain substitution is also rejected even if the supplied record itself is well-formed.
    base,result,bridge,envelope=built["visual_loops"]
    bad_bridge=copy.deepcopy(bridge); bad_bridge["selection"]["subtype_id"]="interference_plane"
    _reject("substituted bridge",lambda:build_request_scoped_payload_binding(result,bad_bridge,envelope,ROOT)); negatives.append("substituted bridge")
    bad_env=copy.deepcopy(envelope); bad_env["status"]="RENDERABLE"
    _reject("substituted adapter",lambda:build_request_scoped_payload_binding(result,bridge,bad_env,ROOT)); negatives.append("substituted adapter")
    bad_result=copy.deepcopy(result); bad_result["canonical_request"]["selection"]["subtype_id"]="interference_plane"
    _reject("substituted request selection",lambda:build_request_scoped_payload_binding(bad_result,bridge,envelope,ROOT)); negatives.append("substituted request selection")
    counts["negative"]=len(negatives)
    assert counts["negative"]==51, counts
    return counts

if __name__=="__main__":
    c=run_checks()
    js=f"{c['jsonschema']}/3" if c["jsonschema"] else "NOT_INSTALLED (strict structural checks PASS)"
    print("C11-D RENDERER REQUEST-SCOPED PAYLOAD BINDING PASS"
      +f" | content_types={c['content']}/3 | deterministic={c['deterministic']}/3 | chain_parity={c['chain']}/3 | source_resolution={c['source']}/3"
      +f" | negative={c['negative']}/51 | schema={c['schema']}/3 | jsonschema={js}"
      +" | challenge=EXACT_VARIANT_SOURCE_RUNTIME_PAYLOAD_NOT_MATERIALIZED"
      +" | loop=FAMILY_AND_GRAMMAR_RESOLVED_INSTANCE_REQUIRED"
      +" | drill=TYPE_AND_TIER_RESOLVED_REQUEST_INSTANCE_REQUIRED"
      +" | payload_instance=NOT_MATERIALIZED | video_render_ready=false"
      +" | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
