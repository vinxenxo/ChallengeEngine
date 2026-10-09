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
from d_renderer_editorial_review_manifest import build_editorial_review_manifest, validate_editorial_review_manifest, DRendererEditorialReviewError, sha256_json

def _raw(selection: dict[str,Any], request_id: str) -> dict[str,Any]:
    return {
      "schema":REQUEST_SCHEMA_ID,"schema_version":"1.0","request_id":request_id,"mode":"REVIEW","selection":selection,
      "seed":12345,"music_seed":840001,"delivery_profile_id":"REVIEW_720","presentation_profile_id":"social_default_v1",
      "variation_index":0,"audio_enabled":True,"personalization_enabled":True,"editorial_profile":{},
      "production_override":{"title":"Prueba editorial · título","subtitle":"Subtítulo de revisión","call_to_action":"Continuar","language":"es", **({"player_name":"ANA","challenge_label":"RETO"} if selection["content_type"]=="challenges" else {})},
      "provenance":{"source_revision":"C11D-D9.9-0.11.1","request_origin":"TEST"}
    }

def _fixtures() -> dict[str,dict[str,Any]]:
    return {
      "challenges":{"content_type":"challenges","family_id":"parking_v2","variant_id":"CHALLENGE_004"},
      "visual_loops":{"content_type":"visual_loops","family_id":"c11c_geometric_waves_v1","subtype_id":"harmonic_membrane"},
      "visual_drills":{"content_type":"visual_drills","family_id":"tracking","variant_id":"tier-2"}
    }

def _reject(label: str, action: Callable[[],Any]) -> None:
    try: action()
    except (DRendererEditorialReviewError, ValueError, TypeError, KeyError): return
    raise AssertionError(f"Expected rejection: {label}")

def run_checks() -> dict[str,int]:
    src=(HERE/"d_renderer_editorial_review_manifest.py").read_text(encoding="utf-8")
    tree=ast.parse(src)
    forbidden_modules={"subprocess","ffmpeg","godot","socket","multiprocessing"}
    forbidden_calls={"write_text","write_bytes","Popen","system","startfile","run","call","check_call","check_output"}
    for node in ast.walk(tree):
        if isinstance(node,ast.Import): assert not any(alias.name.split('.')[0] in forbidden_modules for alias in node.names)
        elif isinstance(node,ast.ImportFrom): assert (node.module or '').split('.')[0] not in forbidden_modules
        elif isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute): assert node.func.attr not in forbidden_calls, f"Persistence/dispatch call in manifest module: {node.func.attr}"
    schema=json.loads((ROOT/"definitions/c11d/production/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_SCHEMA_V1.json").read_text(encoding="utf-8-sig"))
    assert schema["$schema"]=="https://json-schema.org/draft/2020-12/schema" and schema["additionalProperties"] is False
    assert set(schema["required"])==set(schema["properties"])
    try:
        from jsonschema import Draft202012Validator
    except ImportError: Draft202012Validator=None
    if Draft202012Validator is not None: Draft202012Validator.check_schema(schema)
    counts={"content":0,"deterministic":0,"editorial":0,"temporal":0,"schema":0,"jsonschema":0}
    fixtures={}
    for content_type,selection in _fixtures().items():
        request=_raw(selection,f"D-EDITORIAL-REVIEW-{content_type.upper()}")
        result=evaluate_universal_request(request,ROOT)
        bridge=build_bridge_planning_record(result,ROOT)
        envelope=prepare_d_only_adapter_envelope(result,bridge,ROOT)
        manifest=build_editorial_review_manifest(result,bridge,envelope,ROOT)
        assert manifest==build_editorial_review_manifest(copy.deepcopy(result),copy.deepcopy(bridge),copy.deepcopy(envelope),ROOT)
        assert validate_editorial_review_manifest(manifest,result,bridge,envelope,ROOT) is True
        assert manifest["content_type"]==content_type
        assert manifest["review_assessment"]["canonical_editorial_parity"]=="PASS"
        assert manifest["review_assessment"]["upstream_chain_parity"]=="PASS"
        assert manifest["review_assessment"]["video_render_ready"] is False
        assert manifest["execution_boundary"]=={"review_mode":"IN_MEMORY_EDITORIAL_CHAIN_AUDIT","renderer_native_input_emitted":False,"renderer_dispatch_invoked":False,"renderer_activation":False,"production_execution":False,"media_output_created":False,"output_artifact_path":None,"d4_8":"BLOCKED","release_authority":"NONE","c11c_source_mutation":False,"video_render_ready":False}
        assert manifest["source_identity"]["request_hash"]==result["request_hash"]
        assert manifest["source_identity"]["bridge_record_hash"]==bridge["record_hash"]
        assert manifest["source_identity"]["adapter_envelope_hash"]==envelope["envelope_hash"]
        assert manifest["frozen_c11c_manifest_sha256"]=="e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
        for identity_key in ("review_contract_sha256","review_schema_sha256","review_implementation_sha256","source_lineage_sha256"):
            assert len(manifest["source_identity"][identity_key])==64
            assert all(c in "0123456789abcdef" for c in manifest["source_identity"][identity_key])
        for identity_key, source_path in (("review_contract_sha256", ROOT/"definitions/c11d/production/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1.json"), ("review_schema_sha256", ROOT/"definitions/c11d/production/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_SCHEMA_V1.json"), ("review_implementation_sha256", HERE/"d_renderer_editorial_review_manifest.py")):
            assert manifest["source_identity"][identity_key] == hashlib.sha256(source_path.read_bytes()).hexdigest()
        contract=json.loads((ROOT/"definitions/c11d/production/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1.json").read_text(encoding="utf-8-sig"))
        assert len(contract["source_lineage"])==25
        lineage=[{"path":entry["path"],"sha256":hashlib.sha256((ROOT/entry["path"]).read_bytes()).hexdigest()} for entry in contract["source_lineage"]]
        lineage_digest=hashlib.sha256(json.dumps(lineage,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False).encode("utf-8")).hexdigest()
        assert manifest["source_identity"]["source_lineage_sha256"]==lineage_digest
        fields={item["source_field"]:item for item in manifest["editorial_fields"]}
        assert set(fields)==set(result["plan"]["editorial"])-{"language"}
        for key, field in fields.items():
            assert field["text_value"]==result["plan"]["editorial"][key]
            assert field["text_sha256"]==sha256_json(field["text_value"])
            assert field["target_mapping_state"]=="PROPOSED_NOT_APPROVED"
            assert field["visibility_frame_range"] is None
        tr=manifest["temporal_reference"]
        assert tr["per_field_visibility_windows_defined"] is False and tr["per_field_frame_ranges"] is None
        assert sum(s["frame_count"] for s in tr["segments"])==tr["total_frames"]
        for i,seg in enumerate(tr["segments"]):
            assert seg["end_frame_exclusive"]-seg["start_frame"]==seg["frame_count"]
            if i: assert seg["start_frame"]==tr["segments"][i-1]["end_frame_exclusive"]
        if content_type=="challenges":
            assert tr["source_scope"]=="EXACT_CHALLENGE_VARIANT_SOURCE"
            assert tr["source_id"]=="CHALLENGE_004" and tr["total_frames"]==900 and tr["source_fps"]==60
            assert tr["fps_alignment"]=="MISMATCH_REQUIRES_EXPLICIT_NORMALIZATION"
            assert manifest["review_assessment"]["delivery_fps_reconciliation"]=="REQUIRES_EXPLICIT_NORMALIZATION_POLICY"
            assert [x["segment_id"] for x in tr["segments"]]==["HOOK","GAME","REVEAL","CTA"]
            assert len(fields)==5
        elif content_type=="visual_loops":
            assert tr["source_scope"]=="FAMILY_LEVEL_TIMING_REFERENCE_GRAMMAR_INSTANCE_NOT_BOUND"
            assert tr["source_id"]=="visual_loop_geometric_canonical" and tr["total_frames"]==60 and tr["source_fps"]==30
            assert tr["fps_alignment"]=="MATCH_FOR_REFERENCE_ONLY"
            assert len(fields)==3
        else:
            assert tr["source_scope"]=="DRILL_TYPE_AND_TIER_TIMING_REFERENCE_GENERATED_PAYLOAD_INSTANCE_NOT_BOUND"
            assert tr["source_id"]=="visual_drill_tracking_canonical" and tr["total_frames"]==630 and tr["source_fps"]==30
            assert tr["fps_alignment"]=="MATCH_FOR_REFERENCE_ONLY"
            assert len(fields)==3
        assert set(manifest)==set(schema["required"])
        assert "manifest_sha256" not in manifest
        assert manifest["frozen_c11c_manifest_sha256"]==manifest["source_identity"]["frozen_c11c_manifest_sha256"]
        assert manifest["review_manifest_sha256"]==sha256_json({k:v for k,v in manifest.items() if k!="review_manifest_sha256"})
        counts["content"]+=1; counts["deterministic"]+=1; counts["editorial"]+=1; counts["temporal"]+=1; counts["schema"]+=1
        if Draft202012Validator is not None:
            Draft202012Validator(schema).validate(manifest); counts["jsonschema"]+=1
        fixtures[content_type]=(result,bridge,envelope,manifest)
    result,bridge,envelope,base=fixtures["visual_loops"]
    negatives=[]
    def bad(label,mutate):
        c=copy.deepcopy(base); mutate(c)
        _reject(label,lambda:validate_editorial_review_manifest(c,result,bridge,envelope,ROOT)); negatives.append(label)
    bad("text mutation",lambda x:x["editorial_fields"][0].update(text_value="FORGED"))
    bad("text digest mutation",lambda x:x["editorial_fields"][0].update(text_sha256="0"*64))
    bad("promoted target mapping",lambda x:x["editorial_fields"][0].update(target_mapping_state="APPROVED"))
    bad("invented coordinates",lambda x:x["editorial_fields"][0].update(layout_binding_state="PIXEL_BOUND"))
    bad("invented field frame window",lambda x:x["editorial_fields"][0].update(visibility_frame_range={"start":0,"end":10}))
    bad("temporal per-field binding enabled",lambda x:x["temporal_reference"].update(per_field_visibility_windows_defined=True))
    bad("timing source identity mutation",lambda x:x["temporal_reference"].update(source_id="forged"))
    bad("timeline frame count mutation",lambda x:x["temporal_reference"]["segments"][0].update(frame_count=999))
    bad("fps relation mutated",lambda x:x["temporal_reference"].update(fps_alignment="MISMATCH_REQUIRES_EXPLICIT_NORMALIZATION"))
    bad("selection-specific payload overclaim",lambda x:x["temporal_reference"].update(selection_specific_visual_payload_bound=True))
    bad("review marked ready for video",lambda x:x["review_assessment"].update(video_render_ready=True))
    bad("renderer input enabled",lambda x:x["execution_boundary"].update(renderer_native_input_emitted=True))
    bad("media output enabled",lambda x:x["execution_boundary"].update(media_output_created=True))
    bad("D4.8 escalated",lambda x:x["execution_boundary"].update(d4_8="AUTHORIZED"))
    bad("release authority escalated",lambda x:x["execution_boundary"].update(release_authority="GRANTED"))
    bad("manifest hash changed",lambda x:x.update(review_manifest_sha256="0"*64))
    bad("unknown field",lambda x:x.update(uncontracted_dispatch=True))
    bad("manifest status promoted",lambda x:x.update(status="APPROVED_RENDERER_INPUT"))
    bad("source request identity changed",lambda x:x["source_identity"].update(request_hash="0"*64))
    bad("review implementation provenance changed",lambda x:x["source_identity"].update(review_implementation_sha256="0"*64))
    bad("source lineage provenance changed",lambda x:x["source_identity"].update(source_lineage_sha256="0"*64))
    bad("frozen C11-C digest field ambiguous/changed",lambda x:x.update(frozen_c11c_manifest_sha256="0"*64))
    bad("region mapping state mutated",lambda x:x["editorial_fields"][0].update(semantic_region_id="CANONICAL_FIXED_RECTANGLE"))
    bad("temporal scope overclaim",lambda x:x["temporal_reference"].update(source_scope="EXACT_CHALLENGE_VARIANT_SOURCE"))
    # Mutated inputs are rejected before a self-attestation can make them valid.
    altered=copy.deepcopy(result); altered["request_hash"]="0"*64
    _reject("tampered canonical request hash",lambda:build_editorial_review_manifest(altered,bridge,envelope,ROOT)); negatives.append("tampered canonical request hash")
    altered_bridge=copy.deepcopy(bridge); altered_bridge["record_hash"]="0"*64
    _reject("tampered bridge record",lambda:build_editorial_review_manifest(result,altered_bridge,envelope,ROOT)); negatives.append("tampered bridge record")
    altered_env=copy.deepcopy(envelope); altered_env["envelope_hash"]="0"*64
    _reject("tampered adapter envelope",lambda:build_editorial_review_manifest(result,bridge,altered_env,ROOT)); negatives.append("tampered adapter envelope")
    _reject("unsupported longform",lambda:build_editorial_review_manifest({"status":"PLANNED","plan":{"selection":{"content_type":"longform"}}},{},{},ROOT)); negatives.append("unsupported longform")
    return {**counts,"negative":len(negatives)}

def main()->int:
    r=run_checks()
    print("C11-D RENDERER EDITORIAL REVIEW MANIFEST PASS"
      f" | content_types={r['content']}/3 | deterministic={r['deterministic']}/3"
      f" | editorial_chain={r['editorial']}/3 | temporal_reference={r['temporal']}/3"
      f" | negative={r['negative']}/{r['negative']} | schema={r['schema']}/3"
      + (f" | jsonschema={r['jsonschema']}/3" if r['jsonschema']==3 else " | jsonschema=NOT_INSTALLED (strict structural checks PASS)")
      + " | challenge=EXACT_SOURCE_FPS_NORMALIZATION_REQUIRED"
      + " | loop=FAMILY_TIMING_REFERENCE_ONLY | drill=TYPE_TIER_TIMING_REFERENCE_ONLY"
      + " | field_frame_windows=UNRESOLVED | video_render_ready=false"
      + " | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
    return 0
if __name__=="__main__": raise SystemExit(main())

