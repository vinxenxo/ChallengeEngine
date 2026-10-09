"""Cross-contract editorial review manifest. It is in-memory, non-renderable and fail-closed."""
from __future__ import annotations
import copy, hashlib, json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from editorial_render_bridge import build_bridge_planning_record, EditorialRenderBridgeError
from d_render_adapter import prepare_d_only_adapter_envelope, validate_d_only_adapter_envelope, DRenderAdapterError
from d_renderer_candidate import build_renderer_binding_preview, DRendererCandidateError, sha256_json
from d_renderer_logical_composition import build_logical_composition_plan, DRendererLogicalCompositionError
from d_renderer_frame_program import build_renderer_neutral_frame_program, DRendererFrameProgramError
from d_renderer_temporal_bound_preview import build_temporal_bound_preview, validate_temporal_bound_preview, DRendererTemporalBoundPreviewError

CONTRACT_REL = Path("definitions/c11d/production/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1.json")
SCHEMA_REL = Path("definitions/c11d/production/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_SCHEMA_V1.json")
MANIFEST_REL = Path("release/C11C_FREEZE_PACKAGE_MANIFEST.json")
CONTRACT_SCHEMA = "C11-D-RENDERER-EDITORIAL-REVIEW-MANIFEST-CONTRACT-V1"
OUTPUT_SCHEMA = "C11-D-D9-RENDERER-EDITORIAL-REVIEW-MANIFEST-V1"
STATUS = "PREPARATION_ONLY_EDITORIAL_REVIEW_MANIFEST_WITH_OPEN_RENDER_BINDINGS"
EXPECTED_MANIFEST_SHA256 = "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
SUPPORTED_TYPES = ("challenges", "visual_loops", "visual_drills")

class DRendererEditorialReviewError(ValueError):
    """Invalid canonical source chain, temporal alignment, hash or governance escalation."""

def _root(project_root: Path | str | None = None) -> Path:
    return Path(project_root).resolve() if project_root is not None else Path(__file__).resolve().parents[3]

def _read_json(root: Path, rel: str | Path) -> dict[str, Any]:
    try: value = json.loads((root / rel).read_text(encoding="utf-8-sig"))
    except Exception as exc: raise DRendererEditorialReviewError(f"Cannot read required JSON {rel}: {exc}") from exc
    if not isinstance(value, dict): raise DRendererEditorialReviewError(f"Expected JSON object at {rel}")
    return value

def _file_sha(path: Path) -> str:
    try: return hashlib.sha256(path.read_bytes()).hexdigest()
    except Exception as exc: raise DRendererEditorialReviewError(f"Cannot hash source {path}: {exc}") from exc

def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)

def _sha(value: Any) -> str: return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()
def _without_hash(value: Mapping[str, Any]) -> dict[str, Any]: return {str(k): copy.deepcopy(v) for k,v in value.items() if k != "review_manifest_sha256"}

def _assert_no_truth(value: Any, location: str = "editorial_review_manifest") -> None:
    forbidden = {"simulationresult","simulation_result","simulationtruth","simulation_truth","winning_frame","winningframe","close_calls","closecalls","derived_telemetry","derivedtelemetry","gameplay_rng","structural_rng"}
    if isinstance(value, Mapping):
        for key, child in value.items():
            if str(key).replace("-","_").lower() in forbidden: raise DRendererEditorialReviewError(f"Forbidden truth/telemetry field in {location}: {key}")
            _assert_no_truth(child, f"{location}.{key}")
    elif isinstance(value, list):
        for i,child in enumerate(value): _assert_no_truth(child, f"{location}[{i}]")

EXPECTED_SOURCE_PATHS = (
    "release/C11C_FREEZE_PACKAGE_MANIFEST.json",
    "c11c-suite/c11c-producer/producer_schema.json",
    "profiles/delivery/c11c_video_delivery_profiles.json",
    "challenges/CHALLENGE_004.json",
    "definitions/visual_loop_geometric_canonical.json",
    "definitions/visual_drill_tracking_canonical.json",
    "definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json",
    "definitions/c11d/production/C11D_EDITORIAL_RENDER_BRIDGE_D9_10_V1.json",
    "definitions/c11d/production/C11D_RENDER_ADAPTER_BOUNDARY_D9_10_V1.json",
    "definitions/c11d/production/D_RENDERER_REGION_HIERARCHY_RECONCILIATION_V1.json",
    "definitions/c11d/production/D_RENDERER_TEMPORAL_BOUND_PREVIEW_V1.json",
    "definitions/c11d/production/D_RENDERER_TEMPORAL_BOUND_PREVIEW_SCHEMA_V1.json",
    "definitions/c11d/production/D_RENDERER_CANDIDATE_BINDING_PREVIEW_V1.json",
    "definitions/c11d/production/D_RENDERER_CANDIDATE_BINDING_PREVIEW_SCHEMA_V1.json",
    "definitions/c11d/production/D_RENDERER_CANDIDATE_LOGICAL_COMPOSITION_V1.json",
    "definitions/c11d/production/D_RENDERER_CANDIDATE_LOGICAL_COMPOSITION_SCHEMA_V1.json",
    "definitions/c11d/production/D_RENDERER_NEUTRAL_FRAME_PROGRAM_V1.json",
    "definitions/c11d/production/D_RENDERER_NEUTRAL_FRAME_PROGRAM_SCHEMA_V1.json",
    "tools/c11d/d9/universal_producer.py",
    "tools/c11d/d9/editorial_render_bridge.py",
    "tools/c11d/d9/d_render_adapter.py",
    "tools/c11d/d9/d_renderer_candidate.py",
    "tools/c11d/d9/d_renderer_logical_composition.py",
    "tools/c11d/d9/d_renderer_frame_program.py",
    "tools/c11d/d9/d_renderer_temporal_bound_preview.py",
)
EXPECTED_SOURCE_OF_TRUTH = {
    "frozen_c11c_manifest_sha256": EXPECTED_MANIFEST_SHA256,
    "editorial_payload": "D9.9 canonical plan.editorial, identity carried through D9.10 bridge and PREPARE_ONLY adapter",
    "semantic_field_declarations": "validated D logical composition + renderer-neutral frame program; region IDs remain proposed/unapproved",
    "temporal_reference": "D renderer temporal bound preview generated from one existing canonical source per supported content type",
    "spatial_hierarchy": "D1.5 shared frame + existing profile and family presentation binder; no coordinates emitted",
    "selection_timing_alignment": {
        "challenges": "EXACT_CHALLENGE_VARIANT_SOURCE_REQUIRED",
        "visual_loops": "FAMILY_LEVEL_TIMING_REFERENCE_ONLY; SELECTED_GRAMMAR_VISUAL_INSTANCE_NOT_BOUND",
        "visual_drills": "DRILL_TYPE_AND_TIER_TIMING_REFERENCE; GENERATED_REQUEST_PAYLOAD_INSTANCE_NOT_BOUND",
    },
    "field_visibility": "No existing contract assigns a per-field start/end frame; manifest must keep visibility frame ranges null.",
    "fps_policy": "Source and delivery FPS are compared, never silently converted. A mismatch blocks video readiness until a separate normalization contract exists.",
    "delivery_profile_registry": "Pinned profiles/delivery/c11c_video_delivery_profiles.json; resolved dimensions/FPS are metadata only",
}
EXPECTED_OUTPUT_CONTRACT = {
    "schema": OUTPUT_SCHEMA,
    "schema_version": "1.0",
    "json_schema": str(SCHEMA_REL).replace("\\", "/"),
    "deterministic": "CANONICAL_JSON_SHA256",
    "construction": "IN_MEMORY_ONLY",
    "persistent_output": False,
    "renderer_native_input_emitted": False,
    "renderer_dispatch_invoked": False,
    "renderer_activation": False,
    "production_execution": False,
    "media_output_created": False,
    "output_artifact_path": None,
}
EXPECTED_REVIEW_RULES = {
    "editorial_value_source": "FRAME_PROGRAM_INSTRUCTIONS_REVALIDATED_AGAINST_D9_9_CANONICAL_PLAN",
    "field_text_integrity": "EXACT_STRING_AND_SHA256_PARITY; NO_REWRITING_OR_NORMALIZATION_AFTER_CANONICAL_RESOLUTION",
    "field_region_mapping": "PRESERVE_EXISTING_SEMANTIC_REGION_ID_AND_PROPOSED_STATE; NEVER_PROMOTE_TO_APPROVED",
    "timing": "REPORT_CANONICAL_SOURCE_SEGMENTS; DO_NOT_ASSIGN_TEXT_FIELD_FRAME_WINDOWS",
    "delivery_fps": "EXPLICIT_COMPARE_ONLY; NO_AUTOMATIC_FRAME_RATE_CONVERSION",
    "visual_loop_alignment": "FAMILY_REFERENCE_MAY_NOT_CLAIM_SELECTED_GRAMMAR_RENDER_PAYLOAD_IDENTITY",
    "visual_drill_alignment": "TYPE_AND_DIFFICULTY_TIER_REFERENCE_MAY_NOT_CLAIM_GENERATED_PAYLOAD_IDENTITY",
    "review_readiness": "HUMAN_COPY_REVIEW_ALLOWED_IF_CHAIN_PASSES; VIDEO_RENDER_READY_ALWAYS_FALSE_IN_THIS_CONTRACT",
    "unknown_type": "REJECT",
    "longform": "REJECT_UNTIL_CANONICAL_REQUEST_AND_TEMPORAL_CONTRACT_EXIST",
}
EXPECTED_APPROVAL_STATE = {
    "editorial_review_manifest_approved": False,
    "semantic_region_mapping_approved": False,
    "temporal_topology_approved": False,
    "renderer_baseline_approved": False,
    "renderer_baseline_frozen": False,
    "d4_8_authorized": False,
    "d9_14_full_acceptance": "BLOCKED_AS_REQUIRED",
    "d9_16_full_acceptance": "BLOCKED_AS_REQUIRED",
    "d9_17_closure": "BLOCKED_NO_GO",
    "d10": "BLOCKED",
    "release_authority": "NONE",
}

def _load_contract(root: Path) -> tuple[dict[str, Any],dict[str, Any],list[dict[str,str]]]:
    contract = _read_json(root, CONTRACT_REL); schema = _read_json(root, SCHEMA_REL)
    if contract.get("schema") != CONTRACT_SCHEMA or contract.get("schema_version") != "1.0": raise DRendererEditorialReviewError("Review manifest contract identity/version mismatch")
    if contract.get("status") != "PREPARATION_ONLY_EDITORIAL_REVIEW_MANIFEST_NOT_RENDERER_INPUT": raise DRendererEditorialReviewError("Review manifest cannot self-promote its status")
    if contract.get("supported_content_types") != list(SUPPORTED_TYPES): raise DRendererEditorialReviewError("Supported content-type contract drift")
    if contract.get("source_of_truth") != EXPECTED_SOURCE_OF_TRUTH: raise DRendererEditorialReviewError("Source-of-truth declarations drift or were promoted")
    if contract.get("output_contract") != EXPECTED_OUTPUT_CONTRACT: raise DRendererEditorialReviewError("Output-contract declarations drift or were promoted")
    if contract.get("review_rules") != EXPECTED_REVIEW_RULES: raise DRendererEditorialReviewError("Editorial review rules drift or were promoted")
    if contract.get("approval_state") != EXPECTED_APPROVAL_STATE: raise DRendererEditorialReviewError("Review manifest cannot grant baseline or production approval")
    if _file_sha(root/MANIFEST_REL) != EXPECTED_MANIFEST_SHA256 or contract.get("source_of_truth",{}).get("frozen_c11c_manifest_sha256") != EXPECTED_MANIFEST_SHA256: raise DRendererEditorialReviewError("Frozen C11-C manifest pin mismatch")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or schema.get("$id") != "urn:c11d:renderer-editorial-review-manifest:v1" or schema.get("additionalProperties") is not False: raise DRendererEditorialReviewError("Review manifest output schema mismatch")
    if set(schema.get("required",[])) != set(schema.get("properties",{})): raise DRendererEditorialReviewError("Review output schema must have exact top-level fields")
    expected_locks = {"review_mode":"IN_MEMORY_EDITORIAL_CHAIN_AUDIT","renderer_native_input_emitted":False,"renderer_dispatch_invoked":False,"renderer_activation":False,"production_execution":False,"media_output_created":False,"output_artifact_path":None,"d4_8":"BLOCKED","release_authority":"NONE","c11c_source_mutation":False,"video_render_ready":False}
    if contract.get("required_locks") != expected_locks: raise DRendererEditorialReviewError("Review manifest lock mismatch")
    entries=contract.get("source_lineage")
    if not isinstance(entries,list) or tuple(str(e.get("path")) if isinstance(e,Mapping) else "" for e in entries) != EXPECTED_SOURCE_PATHS: raise DRendererEditorialReviewError("Source-lineage paths/order do not match the exact pinned contract")
    seen=set(); lineage=[]
    for entry in entries:
        if not isinstance(entry,Mapping) or set(entry)!={"path","sha256"}: raise DRendererEditorialReviewError("Malformed source lineage entry")
        rel,expected=str(entry["path"]),str(entry["sha256"])
        if rel in seen or len(expected)!=64 or any(c not in "0123456789abcdef" for c in expected): raise DRendererEditorialReviewError("Duplicate/malformed source lineage entry")
        seen.add(rel); actual=_file_sha(root/rel)
        if actual != expected: raise DRendererEditorialReviewError(f"Pinned upstream source drift: {rel}")
        lineage.append({"path":rel,"sha256":actual})
    if entries[0].get("path") != str(MANIFEST_REL).replace("\\","/"): raise DRendererEditorialReviewError("C11-C manifest must lead source lineage")
    return contract,schema,lineage

def _validate_temporal_alignment(content_type: str, selection: Mapping[str,Any], temporal: Mapping[str,Any], root: Path) -> tuple[str,str]:
    """Return timing scope, assessment label and delivery-FPS relation without inventing conversions."""
    source=temporal["source_identity"]; schedule=temporal["temporal_schedule"]
    producer=_read_json(root,"c11c-suite/c11c-producer/producer_schema.json")
    if content_type == "challenges":
        variant=str(selection.get("variant_id")); source_id=str(source.get("source_id"))
        if variant != source_id or source.get("source_path") != f"challenges/{variant}.json": raise DRendererEditorialReviewError("Challenge temporal reference must be the exact selected challenge source")
        challenge=_read_json(root,source["source_path"])
        if challenge.get("mechanic") != selection.get("family_id"): raise DRendererEditorialReviewError("Challenge mechanic/family identity mismatch")
        scope="EXACT_CHALLENGE_VARIANT_SOURCE"; assessment="EXACT_CHALLENGE_ID"
    elif content_type == "visual_loops":
        families=producer.get("families",{}); family= families.get(selection.get("family_id"))
        if not isinstance(family,Mapping): raise DRendererEditorialReviewError("Selected Visual Loop family is absent from current Producer registry")
        if family.get("internal") != source.get("subtype"): raise DRendererEditorialReviewError("Visual Loop timing reference does not match selected technical family")
        grammar_ids=[row[0] for row in family.get("grammars",[]) if isinstance(row,list) and row]
        if selection.get("subtype_id") not in grammar_ids: raise DRendererEditorialReviewError("Selected Visual Loop grammar is absent from its canonical family")
        scope="FAMILY_LEVEL_TIMING_REFERENCE_GRAMMAR_INSTANCE_NOT_BOUND"; assessment="FAMILY_LEVEL_REFERENCE_ONLY"
    elif content_type == "visual_drills":
        drills=producer.get("drills",{}); drill=drills.get(selection.get("family_id"))
        if not isinstance(drill,Mapping): raise DRendererEditorialReviewError("Selected Visual Drill type is absent from current Producer registry")
        if drill.get("internal") != source.get("subtype"): raise DRendererEditorialReviewError("Visual Drill timing reference does not match selected type")
        tier=selection.get("difficulty_tier"); variant=str(selection.get("variant_id")); suffix=variant.removeprefix("tier-")
        if not isinstance(tier,int) or isinstance(tier,bool) or not suffix.isdigit() or int(suffix)!=tier: raise DRendererEditorialReviewError("Visual Drill tier identity is malformed")
        payload_source=_read_json(root,source["source_path"])
        params=payload_source.get("payload",{}).get("exercise_parameters",{})
        if params.get("difficulty_tier") != tier: raise DRendererEditorialReviewError("Canonical Drill timing source does not match selected difficulty tier")
        scope="DRILL_TYPE_AND_TIER_TIMING_REFERENCE_GENERATED_PAYLOAD_INSTANCE_NOT_BOUND"; assessment="TYPE_AND_TIER_REFERENCE_ONLY"
    else: raise DRendererEditorialReviewError("Unsupported content type; Longform fails closed")
    return scope,assessment

def _build(result: Mapping[str,Any], bridge_record: Mapping[str,Any], adapter_envelope: Mapping[str,Any], root: Path, contract: Mapping[str,Any], schema: Mapping[str,Any], lineage: list[dict[str,str]]) -> dict[str,Any]:
    if not isinstance(result,Mapping) or result.get("status") != "PLANNED": raise DRendererEditorialReviewError("Input must be a successful canonical D9.9 PLANNED result")
    request=result.get("canonical_request"); plan=result.get("plan")
    if not isinstance(request,Mapping) or not isinstance(plan,Mapping): raise DRendererEditorialReviewError("D9.9 canonical request and plan are required")
    try:
        expected_bridge=build_bridge_planning_record(result,root)
        if dict(bridge_record) != expected_bridge: raise DRendererEditorialReviewError("Bridge record differs from canonical D9.9 request/plan")
        expected_envelope=prepare_d_only_adapter_envelope(result,bridge_record,root)
        if dict(adapter_envelope) != expected_envelope: raise DRendererEditorialReviewError("D-only adapter envelope differs from canonical request/bridge")
        validate_d_only_adapter_envelope(adapter_envelope,root)
        binding=build_renderer_binding_preview(adapter_envelope,root)
        composition=build_logical_composition_plan(binding,adapter_envelope,root)
        frame_program=build_renderer_neutral_frame_program(composition,binding,adapter_envelope,root)
        temporal=build_temporal_bound_preview(str(plan.get("selection",{}).get("content_type")),root)
        validate_temporal_bound_preview(temporal,root)
    except (EditorialRenderBridgeError,DRenderAdapterError,DRendererCandidateError,DRendererLogicalCompositionError,DRendererFrameProgramError,DRendererTemporalBoundPreviewError,ValueError,TypeError,KeyError) as exc:
        if isinstance(exc,DRendererEditorialReviewError): raise
        raise DRendererEditorialReviewError(f"Upstream source contract rejected the review chain: {exc}") from exc
    selection=plan.get("selection")
    if not isinstance(selection,Mapping): raise DRendererEditorialReviewError("Canonical plan selection must be an object")
    content_type=str(selection.get("content_type"))
    if content_type not in SUPPORTED_TYPES: raise DRendererEditorialReviewError("Unsupported content type; Longform and unknown types fail closed")
    if frame_program.get("content_identity") != dict(selection) or binding.get("content_identity") != dict(selection) or composition.get("content_identity") != dict(selection): raise DRendererEditorialReviewError("Content identity drift across binding/composition/frame program")
    scope,alignment = _validate_temporal_alignment(content_type,selection,temporal,root)
    target=frame_program.get("canvas_descriptor",{})
    target_profile_id=request.get("resolved_delivery_profile_id",plan.get("resolved_delivery_profile_id"))
    if not target_profile_id: target_profile_id=plan.get("resolved_delivery_profile_id")
    fps_relation = "MATCH_REFERENCE_ONLY" if float(temporal["temporal_schedule"]["fps"]) == float(target.get("fps")) else "MISMATCH_REQUIRES_EXPLICIT_NORMALIZATION"
    profile_registry_sha = str(binding.get("delivery_profile",{}).get("registry_sha256"))
    actual_profile_registry_sha = _file_sha(root/"profiles/delivery/c11c_video_delivery_profiles.json")
    if profile_registry_sha != actual_profile_registry_sha: raise DRendererEditorialReviewError("Binding delivery-profile registry identity differs from the pinned source")
    fields=[]
    editorial_by_name=plan.get("editorial",{})
    seen=set()
    for instruction in frame_program.get("instructions",[]):
        field=instruction.get("source_field"); value=instruction.get("text_value"); digest=instruction.get("text_sha256")
        if field in seen: raise DRendererEditorialReviewError(f"Duplicate editorial field instruction: {field}")
        seen.add(field)
        if field not in editorial_by_name or editorial_by_name[field] != value: raise DRendererEditorialReviewError(f"Frame-program text differs from canonical editorial value: {field}")
        if digest != _sha(value): raise DRendererEditorialReviewError(f"Frame-program text digest mismatch: {field}")
        if instruction.get("target_mapping_state") != "PROPOSED_NOT_APPROVED" or instruction.get("layout_binding_state") != "UNRESOLVED_NO_COORDINATES" or instruction.get("temporal_binding_state") != "NOT_SCHEDULED_NO_FRAME_RANGE": raise DRendererEditorialReviewError("Editorial target/layout/temporal state was promoted")
        fields.append({"element_id":instruction["element_id"],"source_field":field,"text_value":value,"text_sha256":digest,"language":instruction["language"],"semantic_region_id":instruction["region_id"],"target_mapping_state":instruction["target_mapping_state"],"layout_binding_state":instruction["layout_binding_state"],"temporal_binding_state":instruction["temporal_binding_state"],"visibility_frame_range":None})
    if set(seen) != set(editorial_by_name)-{"language"}: raise DRendererEditorialReviewError("Editorial field coverage differs from canonical payload")
    schedule=temporal["temporal_schedule"]
    segments=[]
    for segment in schedule.get("segments",[]):
        segments.append({"segment_id":segment["segment_id"],"start_frame":segment["start_frame"],"end_frame_exclusive":segment["end_frame_exclusive"],"frame_count":segment["frame_count"],"source_duration_seconds":segment["source_duration_seconds"]})
    requested_id=plan.get("delivery_profile_id"); resolved_id=plan.get("resolved_delivery_profile_id")
    # delivery registry snapshot and resolved values are metadata only.
    registry=_read_json(root,"profiles/delivery/c11c_video_delivery_profiles.json")
    profiles=registry.get("profiles",{})
    profile_id=resolved_id or requested_id
    profile=profiles.get(profile_id)
    seen_alias=set()
    while isinstance(profile,Mapping) and profile.get("alias_of"):
        if profile_id in seen_alias: raise DRendererEditorialReviewError("Delivery profile alias cycle detected")
        seen_alias.add(profile_id); profile_id=profile["alias_of"]; profile=profiles.get(profile_id)
    if not isinstance(profile,Mapping): raise DRendererEditorialReviewError("Resolved delivery profile is absent")
    width=target.get("width"); height=target.get("height"); delivery_fps=target.get("fps")
    if width != profile.get("width") or height != profile.get("height") or float(delivery_fps) != float(profile.get("fps")): raise DRendererEditorialReviewError("Frame-program delivery descriptor differs from resolved delivery profile")
    if len(fields) != len(frame_program["instructions"]): raise DRendererEditorialReviewError("Visible editorial field count mismatch")
    source_identity={
      "request_hash":str(result["request_hash"]),"editorial_hash":str(result["editorial_hash"]),"plan_hash":str(result["plan_hash"]),
      "bridge_record_hash":str(bridge_record["record_hash"]),"adapter_envelope_hash":str(adapter_envelope["envelope_hash"]),
      "binding_preview_sha256":str(binding["preview_sha256"]),"composition_sha256":str(composition["composition_sha256"]),
      "frame_program_sha256":str(frame_program["program_sha256"]),"temporal_preview_sha256":str(temporal["preview_sha256"]),
      "frozen_c11c_manifest_sha256":EXPECTED_MANIFEST_SHA256,
      "review_contract_sha256":_file_sha(root/CONTRACT_REL),
      "review_schema_sha256":_file_sha(root/SCHEMA_REL),
      "review_implementation_sha256":_file_sha(Path(__file__).resolve()),
      "source_lineage_sha256":_sha(lineage),
    }
    manifest={
      "schema":OUTPUT_SCHEMA,"schema_version":"1.0","status":STATUS,"frozen_c11c_manifest_sha256":EXPECTED_MANIFEST_SHA256,
      "content_type":content_type,
      "review_identity":{"request_id":str(request.get("request_id")),"variant_scope_id":str(selection.get("variant_scope_id")),"selection":copy.deepcopy(dict(selection)),"editorial_value_count":len(fields),"human_copy_review_permitted":True},
      "source_identity":source_identity,
      "delivery_target":{"requested_profile_id":str(requested_id),"resolved_profile_id":str(resolved_id),"width":int(width),"height":int(height),"fps":float(delivery_fps),"profile_registry_sha256":profile_registry_sha,"metadata_only":True},
      "temporal_reference":{
        "source_scope":scope,"source_path":str(temporal["source_identity"]["source_path"]),"source_id":str(temporal["source_identity"]["source_id"]),"source_sha256":str(temporal["source_identity"]["source_sha256"]),
        "source_fps":int(schedule["fps"]),"source_duration_seconds":float(schedule["source_duration_sum_seconds"]),"total_frames":int(schedule["total_frames"]),"segments":segments,
        "fps_alignment":"MATCH_FOR_REFERENCE_ONLY" if fps_relation=="MATCH_REFERENCE_ONLY" else "MISMATCH_REQUIRES_EXPLICIT_NORMALIZATION",
        "per_field_visibility_windows_defined":False,"per_field_frame_ranges":None,"selection_specific_visual_payload_bound":False
      },
      "editorial_fields":fields,
      "review_assessment":{
        "canonical_editorial_parity":"PASS","upstream_chain_parity":"PASS","temporal_source_alignment":alignment,
        "delivery_fps_reconciliation":"MATCH_REFERENCE_ONLY" if fps_relation=="MATCH_REFERENCE_ONLY" else "REQUIRES_EXPLICIT_NORMALIZATION_POLICY",
        "field_visibility_policy":"UNRESOLVED_NO_PER_FIELD_FRAME_WINDOWS","editorial_review_status":"HUMAN_COPY_REVIEWABLE_WITH_OPEN_RENDER_BINDINGS","video_render_ready":False
      },
      "execution_boundary":{"review_mode":"IN_MEMORY_EDITORIAL_CHAIN_AUDIT","renderer_native_input_emitted":False,"renderer_dispatch_invoked":False,"renderer_activation":False,"production_execution":False,"media_output_created":False,"output_artifact_path":None,"d4_8":"BLOCKED","release_authority":"NONE","c11c_source_mutation":False,"video_render_ready":False}
    }
    manifest["review_manifest_sha256"]=_sha(manifest)
    _assert_no_truth(manifest)
    return manifest

def build_editorial_review_manifest(result: Mapping[str,Any], bridge_record: Mapping[str,Any], adapter_envelope: Mapping[str,Any], project_root: Path | str | None = None) -> dict[str,Any]:
    root=_root(project_root); contract,schema,lineage=_load_contract(root)
    manifest=_build(result,bridge_record,adapter_envelope,root,contract,schema,lineage)
    validate_editorial_review_manifest(manifest,result,bridge_record,adapter_envelope,root)
    return manifest

def validate_editorial_review_manifest(candidate: Mapping[str,Any], result: Mapping[str,Any], bridge_record: Mapping[str,Any], adapter_envelope: Mapping[str,Any], project_root: Path | str | None = None) -> bool:
    root=_root(project_root); contract,schema,lineage=_load_contract(root)
    if not isinstance(candidate,Mapping) or candidate.get("schema") != OUTPUT_SCHEMA or candidate.get("status") != STATUS: raise DRendererEditorialReviewError("Unsupported/non-preparation editorial review manifest")
    if set(candidate) != set(schema.get("required",[])) or set(candidate) != set(schema.get("properties",{})): raise DRendererEditorialReviewError("Manifest output shape drift")
    if candidate.get("review_manifest_sha256") != _sha(_without_hash(candidate)): raise DRendererEditorialReviewError("Review manifest SHA-256 mismatch")
    expected=_build(result,bridge_record,adapter_envelope,root,contract,schema,lineage)
    if dict(candidate) != expected: raise DRendererEditorialReviewError("Manifest differs from canonical editorial/temporal source chain or violates review locks")
    _assert_no_truth(candidate)
    return True

