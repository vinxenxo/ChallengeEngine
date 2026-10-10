extends SceneTree

## C11-D D9 review harness: materialize exact Visual Loop + Visual Drill payload descriptors in memory only.
## It reuses frozen C11-C authoring/variation APIs and never invokes a renderer, simulation runtime, or filesystem writes.

const VisualAuthoringGeneratorScript = preload("res://core/authoring/VisualAuthoringGenerator.gd")
const VisualAuthoringRequestScript = preload("res://core/authoring/VisualAuthoringRequest.gd")
const VisualAuthoringAssemblyContextScript = preload("res://core/authoring/VisualAuthoringAssemblyContext.gd")
const C11CVariationProfileScript = preload("res://tools/prototypes/c11c_common/C11CVariationProfile.gd")
const C11CPaletteBankScript = preload("res://tools/prototypes/c11c_common/C11CPaletteBank.gd")
const C11CVisualLoopDurationScript = preload("res://tools/prototypes/c11c_common/C11CVisualLoopDuration.gd")
const VisualDrillSeedVariationScript = preload("res://core/authoring/VisualDrillSeedVariation.gd")

const FROZEN_C11C_MANIFEST_SHA256 := "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
const OUTPUT_SCHEMA := "C11-D-D9-RENDERER-VISUAL-PAYLOAD-MATERIALIZATION-PREVIEW-V1"
const REQUEST_SEED := 12345
const VARIATION_INDEX := 0
const FPS := 30
const GEOMETRIC_GRAMMARS: Array[String] = ["harmonic_membrane", "interference_plane", "parametric_ribbon", "lattice_wave", "orbital_wave"]

func _initialize() -> void:
    call_deferred("_run")

func _run() -> void:
    var loop_a: Dictionary = _build_visual_loop_instance()
    var loop_b: Dictionary = _build_visual_loop_instance()
    var drill_a: Dictionary = _build_visual_drill_instance()
    var drill_b: Dictionary = _build_visual_drill_instance()
    if not bool(loop_a.get("success", false)) or not bool(loop_b.get("success", false)):
        push_error("Visual Loop payload preview failed: %s" % str(loop_a.get("error", loop_b.get("error", "unknown"))))
        quit(1)
        return
    if not bool(drill_a.get("success", false)) or not bool(drill_b.get("success", false)):
        push_error("Visual Drill payload preview failed: %s" % str(drill_a.get("error", drill_b.get("error", "unknown"))))
        quit(1)
        return
    var loop_summary: Dictionary = loop_a["summary"].duplicate(true)
    var drill_summary: Dictionary = drill_a["summary"].duplicate(true)
    loop_summary["deterministic_repeat_pass"] = loop_a["summary"]["payload_instance_sha256"] == loop_b["summary"]["payload_instance_sha256"]
    drill_summary["deterministic_repeat_pass"] = drill_a["summary"]["payload_instance_sha256"] == drill_b["summary"]["payload_instance_sha256"]
    if not bool(loop_summary["deterministic_repeat_pass"]) or not bool(drill_summary["deterministic_repeat_pass"]):
        push_error("Repeated request generation did not preserve the same payload hash.")
        quit(1)
        return
    var report: Dictionary = {
        "schema": OUTPUT_SCHEMA,
        "schema_version": "1.0",
        "status": "IN_MEMORY_REVIEW_ONLY_NOT_RENDERER_INPUT",
        "frozen_c11c_manifest_sha256": FROZEN_C11C_MANIFEST_SHA256,
        "instances": [loop_summary, drill_summary],
        "unmaterialized_content_types": ["challenges"],
        "challenge_runtime_payload_materialized": false,
        "execution_boundary": {
            "mode": "IN_MEMORY_REVIEW_ONLY",
            "payload_file_written": false,
            "renderer_native_input_emitted": false,
            "renderer_dispatch_invoked": false,
            "renderer_activation": false,
            "production_execution": false,
            "media_output_created": false,
            "output_artifact_path": null,
            "d4_8": "BLOCKED",
            "release_authority": "NONE",
            "c11c_source_mutation": false
        }
    }
    var errors: Array[String] = _validate_report(report)
    if not errors.is_empty():
        push_error("Preview report contract failed: %s" % str(errors))
        quit(1)
        return
    print("C11-D RENDERER VISUAL PAYLOAD MATERIALIZATION PREVIEW PASS | materialized=2/3 | deterministic=2/2 | loop=%d_FRAMES@%dFPS:%s | drill=%d_FRAMES@%dFPS:%s | challenge=FROZEN_RUNTIME_OUTPUT_REQUIRED | variation_index=METADATA_ONLY_V1 | payload_files=NONE | renderer_input=NOT_EMITTED | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE" % [loop_summary["frame_count"], FPS, loop_summary["selection"]["subtype_id"], drill_summary["frame_count"], FPS, drill_summary["selection"]["variant_id"]])
    print("C11-D VISUAL PAYLOAD PREVIEW SUMMARY=" + JSON.stringify(report))
    quit(0)

func _build_visual_loop_instance() -> Dictionary:
    var variation: Dictionary = C11CVariationProfileScript.build("geometric", REQUEST_SEED)
    var grammar_index: int = GEOMETRIC_GRAMMARS.find("harmonic_membrane")
    if grammar_index < 0:
        return {"success": false, "error": "Selected grammar is absent from frozen C11-C geometric grammar list."}
    variation["grammar_mode"] = grammar_index
    variation["grammar_name"] = "harmonic_membrane"
    var loop_cycles: int = int(round(float(variation.get("loop_cycles", 1.0))))
    var duration_seconds: float = float(C11CVisualLoopDurationScript.policy_seconds_for_cycles(loop_cycles))
    var frame_count: int = int(round(duration_seconds * float(FPS)))
    var palette: Dictionary = C11CPaletteBankScript.palette("geometric", int(variation.get("palette_mode", 0)), REQUEST_SEED)
    var request: VisualAuthoringRequest = VisualAuthoringRequestScript.new("visual_loop", "geometric", duration_seconds, FPS, 2, {"color_palette": str(variation.get("palette_name", "default"))})
    var context: VisualAuthoringAssemblyContext = _make_context("visual_loop", "c11c_geometric_waves_v1")
    var generated: Dictionary = VisualAuthoringGeneratorScript.generate(request, context, {})
    if not bool(generated.get("success", false)):
        return {"success": false, "error": "VisualAuthoringGenerator rejected the Visual Loop request: %s" % str(generated.get("errors", []))}
    var envelope: Dictionary = generated.get("content", {})
    var envelope_payload: Dictionary = envelope.get("payload", {})
    if envelope.get("kind") != "visual_loop" or envelope.get("subtype") != "geometric":
        return {"success": false, "error": "Visual Loop authoring envelope identity mismatch."}
    if int(envelope_payload.get("fps", -1)) != FPS or int(envelope_payload.get("frame_count", -1)) != frame_count or float(envelope_payload.get("duration", -1.0)) != duration_seconds:
        return {"success": false, "error": "Visual Loop authoring envelope timing disagrees with C11-C duration policy."}
    var layers: Array = envelope_payload.get("visual_parameters", {}).get("layers", [])
    if layers.is_empty() or str(layers[0].get("color_palette", "")) != str(variation.get("palette_name", "")):
        return {"success": false, "error": "Visual Loop palette is not bound to the selected deterministic variation."}
    var instance_payload: Dictionary = {
        "instance_schema": "C11-D-REVIEW-ONLY-VISUAL-LOOP-PAYLOAD-V1",
        "request_identity": {"request_id":"D-PAYLOAD-BIND-VISUAL_LOOPS","content_type":"visual_loops","family_id":"c11c_geometric_waves_v1","subtype_id":"harmonic_membrane","seed":REQUEST_SEED,"variation_index":VARIATION_INDEX,"delivery_profile_id":"REVIEW_720"},
        "authoring_envelope": envelope,
        "family_variation_recipe": variation,
        "resolved_palette": palette,
        "timing": {"fps":FPS,"duration_seconds":duration_seconds,"frame_count":frame_count,"duration_source":"C11CVisualLoopDuration.policy_seconds_for_cycles"}
    }
    var envelope_hash: String = _sha256(envelope)
    var instance_hash: String = _sha256(instance_payload)
    return {"success":true,"instance_payload":instance_payload,"summary":{
        "content_type":"visual_loops","instance_id":"D-VLP-" + instance_hash.substr(0, 16),
        "selection":{"family_id":"c11c_geometric_waves_v1","subtype_id":"harmonic_membrane"},
        "seed":REQUEST_SEED,"variation_index":VARIATION_INDEX,"fps":FPS,"duration_seconds":duration_seconds,"frame_count":frame_count,
        "authoring_envelope_sha256":envelope_hash,"payload_instance_sha256":instance_hash,
        "materialization":"IN_MEMORY_ONLY","deterministic_repeat_pass":false,"instance_parameters_bound":true
    }}

func _build_visual_drill_instance() -> Dictionary:
    var duration_seconds: float = 21.0
    var frame_count: int = int(round(duration_seconds * float(FPS)))
    var request: VisualAuthoringRequest = VisualAuthoringRequestScript.new("visual_drill", "tracking", duration_seconds, FPS, 2, {})
    var context: VisualAuthoringAssemblyContext = _make_context("visual_drill", "tracking")
    var generated: Dictionary = VisualAuthoringGeneratorScript.generate(request, context, {})
    if not bool(generated.get("success", false)):
        return {"success":false,"error":"VisualAuthoringGenerator rejected the Visual Drill request: %s" % str(generated.get("errors", []))}
    var envelope: Dictionary = generated.get("content", {})
    var envelope_payload: Dictionary = envelope.get("payload", {})
    var exercise: Dictionary = envelope_payload.get("exercise_parameters", {})
    var trajectory: Dictionary = envelope_payload.get("trajectory", {})
    var seed_motion: Dictionary = envelope_payload.get("seed_motion", {})
    if envelope.get("kind") != "visual_drill" or envelope.get("subtype") != "tracking":
        return {"success":false,"error":"Visual Drill authoring envelope identity mismatch."}
    if int(exercise.get("difficulty_tier", -1)) != 2 or str(exercise.get("generator", "")) != "tracking":
        return {"success":false,"error":"Visual Drill selected tier/generator was not materialized."}
    if int(envelope_payload.get("fps", -1)) != FPS or int(envelope_payload.get("frame_count", -1)) != frame_count or float(envelope_payload.get("duration", -1.0)) != duration_seconds:
        return {"success":false,"error":"Visual Drill authoring envelope timing mismatch."}
    if seed_motion.is_empty() or int(seed_motion.get("seed", -1)) != REQUEST_SEED or trajectory.get("seed_authoring_version") != "2.9.0":
        return {"success":false,"error":"Seeded C11-C VisualDrillSeedVariation was not present in the materialized payload."}
    var instance_payload: Dictionary = {
        "instance_schema":"C11-D-REVIEW-ONLY-VISUAL-DRILL-PAYLOAD-V1",
        "request_identity":{"request_id":"D-PAYLOAD-BIND-VISUAL_DRILLS","content_type":"visual_drills","family_id":"tracking","variant_id":"tier-2","seed":REQUEST_SEED,"variation_index":VARIATION_INDEX,"delivery_profile_id":"REVIEW_720"},
        "authoring_envelope":envelope,
        "timing":{"fps":FPS,"duration_seconds":duration_seconds,"frame_count":frame_count,"duration_source":"definitions/visual_drill_tracking_canonical.json"}
    }
    var envelope_hash: String = _sha256(envelope)
    var instance_hash: String = _sha256(instance_payload)
    return {"success":true,"instance_payload":instance_payload,"summary":{
        "content_type":"visual_drills","instance_id":"D-VDP-" + instance_hash.substr(0, 16),
        "selection":{"family_id":"tracking","variant_id":"tier-2"},
        "seed":REQUEST_SEED,"variation_index":VARIATION_INDEX,"fps":FPS,"duration_seconds":duration_seconds,"frame_count":frame_count,
        "authoring_envelope_sha256":envelope_hash,"payload_instance_sha256":instance_hash,
        "materialization":"IN_MEMORY_ONLY","deterministic_repeat_pass":false,"instance_parameters_bound":true
    }}

func _make_context(content_kind: String, asset_family_id: String) -> VisualAuthoringAssemblyContext:
    var request_id: String = "D-PAYLOAD-BIND-VISUAL_LOOPS" if content_kind == "visual_loop" else "D-PAYLOAD-BIND-VISUAL_DRILLS"
    return VisualAuthoringAssemblyContextScript.new(
        REQUEST_SEED,
        "2.0",
        request_id,
        "1.0",
        "C11-C-2.19.12",
        {"profile_id":"social_default_v1","coordinate_space":"CANVAS_540X960"},
        {"family_id":asset_family_id},
        {"profile_id":"default_procedural_music","enabled":true},
        {"author":"C11D_IN_MEMORY_REVIEW_PREVIEW","timestamp_ms":0}
    )

func _validate_report(report: Dictionary) -> Array[String]:
    var errors: Array[String] = []
    if report.get("schema") != OUTPUT_SCHEMA or report.get("schema_version") != "1.0" or report.get("status") != "IN_MEMORY_REVIEW_ONLY_NOT_RENDERER_INPUT":
        errors.append("report identity/status mismatch")
    if report.get("frozen_c11c_manifest_sha256") != FROZEN_C11C_MANIFEST_SHA256:
        errors.append("frozen C11-C manifest mismatch")
    var instances: Array = report.get("instances", [])
    if instances.size() != 2:
        errors.append("exactly two materialized visual instance summaries required")
    var types: Array[String] = []
    for item in instances:
        if not (item is Dictionary):
            errors.append("instance summary must be a Dictionary")
            continue
        types.append(str(item.get("content_type", "")))
        if item.get("materialization") != "IN_MEMORY_ONLY" or item.get("deterministic_repeat_pass") != true:
            errors.append("instance summary must be in-memory and deterministic")
        if int(item.get("frame_count", 0)) != int(round(float(item.get("duration_seconds", 0.0)) * float(item.get("fps", 0)))):
            errors.append("instance frame_count/FPS/duration mismatch")
        for field in ["authoring_envelope_sha256", "payload_instance_sha256"]:
            if not _is_sha256(str(item.get(field, ""))): errors.append("malformed digest: " + field)
    types.sort()
    if types != ["visual_drills", "visual_loops"]:
        errors.append("only the selected Visual Loop and Visual Drill instances may be materialized")
    if report.get("unmaterialized_content_types") != ["challenges"] or report.get("challenge_runtime_payload_materialized") != false:
        errors.append("Challenge runtime payload must remain unmaterialized")
    var boundary: Dictionary = report.get("execution_boundary", {})
    var expected: Dictionary = {"mode":"IN_MEMORY_REVIEW_ONLY","payload_file_written":false,"renderer_native_input_emitted":false,"renderer_dispatch_invoked":false,"renderer_activation":false,"production_execution":false,"media_output_created":false,"output_artifact_path":null,"d4_8":"BLOCKED","release_authority":"NONE","c11c_source_mutation":false}
    if boundary != expected: errors.append("execution boundary/governance locks mismatch")
    return errors

func _canonicalize(value: Variant) -> Variant:
    if value is Dictionary:
        var keys: Array = value.keys()
        keys.sort()
        var result: Dictionary = {}
        for key in keys:
            result[str(key)] = _canonicalize(value[key])
        return result
    if value is Array:
        var result_array: Array = []
        for item in value:
            result_array.append(_canonicalize(item))
        return result_array
    return value

func _sha256(value: Variant) -> String:
    var ctx := HashingContext.new()
    var start_error: int = ctx.start(HashingContext.HASH_SHA256)
    if start_error != OK:
        return ""
    ctx.update(JSON.stringify(_canonicalize(value)).to_utf8_buffer())
    return ctx.finish().hex_encode()

func _is_sha256(value: String) -> bool:
    if value.length() != 64:
        return false
    for character in value:
        if not "0123456789abcdef".contains(character):
            return false
    return true
