extends SceneTree

## D9 preparation-only exact-selector payload materializer.
## Creates an ephemeral, review-only descriptor from the pinned C11-C authoring envelope
## and the request-bound grammar parameter instance. No renderer, material, shader,
## filesystem output, native renderer input, or media is created.

const VisualAuthoringGeneratorScript = preload("res://core/authoring/VisualAuthoringGenerator.gd")
const VisualAuthoringRequestScript = preload("res://core/authoring/VisualAuthoringRequest.gd")
const VisualAuthoringAssemblyContextScript = preload("res://core/authoring/VisualAuthoringAssemblyContext.gd")
const C11CVariationProfileScript = preload("res://tools/prototypes/c11c_common/C11CVariationProfile.gd")
const C11CPaletteBankScript = preload("res://tools/prototypes/c11c_common/C11CPaletteBank.gd")
const C11CVisualLoopDurationScript = preload("res://tools/prototypes/c11c_common/C11CVisualLoopDuration.gd")

const FROZEN_C11C_MANIFEST_SHA256 := "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
const INPUT_SCHEMA := "C11-D-D9-VISUAL-LOOP-EXACT-SELECTOR-PAYLOAD-INPUT-V2"
const PROBE_SCHEMA := "C11-D-D9-VISUAL-LOOP-EXACT-SELECTOR-PAYLOAD-PROBE-V2"
const PREFIX := "C11D_VISUAL_LOOP_EXACT_SELECTOR_PAYLOAD_V2_PROBE="
const FPS := 30
const GRAMMAR_IDS: Array[String] = ["harmonic_membrane", "interference_plane", "parametric_ribbon", "lattice_wave", "orbital_wave"]
const SHADER_BRANCHES: Array[String] = ["field_harmonic_membrane", "field_interference_plane", "field_parametric_ribbon", "field_lattice_wave", "field_orbital_wave"]
const STYLE_PROJECTION_ABS_TOLERANCE := 1.0e-10
const STYLE_KEYS: Array[String] = ["grammar_mode", "palette_mode", "morph", "wave_frequency", "line_width", "glow_strength", "polygon_sides", "wave_ratio", "shape_rotation", "layer_spread", "radial_wave_amplitude", "liss_x_frequency", "liss_y_frequency", "interference_scale", "hero_scale", "perspective_strength", "depth_strength", "secondary_phase", "color_phase", "stroke_scale"]
const PROFILE_INPUT_KEYS: Array[String] = ["grammar_mode", "palette_mode", "morph", "wave_frequency", "line_width", "glow", "polygon_sides", "wave_ratio", "shape_rotation", "layer_spread", "radial_wave_amplitude", "liss_x_frequency", "liss_y_frequency", "interference_scale", "hero_scale", "perspective_strength", "depth_strength", "secondary_phase", "color_phase", "stroke_scale"]
const BOUNDARY := {
    "payload_materialized_in_memory": true,
    "payload_file_written": false,
    "receipt_file_written": false,
    "renderer_instance_created": false,
    "shader_material_created": false,
    "shader_executed": false,
    "renderer_native_input_emitted": false,
    "renderer_dispatch_invoked": false,
    "renderer_activation": false,
    "media_created": false,
    "c11c_source_mutation": false,
    "candidate_input_admissible": false,
    "renderer": "OFF",
    "D4.8": "BLOCKED",
    "release_authority": "NONE",
    "D9.10": "PREPARE_ONLY",
    "D9.17": "BLOCKED_NO_GO",
    "D10": "BLOCKED"
}

func _initialize() -> void:
    call_deferred("_run")

func _run() -> void:
    var input_value := _decode_input()
    if input_value.is_empty():
        _fail("missing or invalid base64 JSON input")
        return
    var input_errors := _validate_input(input_value)
    if not input_errors.is_empty():
        _fail("invalid exact-selector payload input: " + "; ".join(input_errors))
        return
    var source_error := _source_checks_error()
    if not source_error.is_empty():
        _fail(source_error)
        return

    var first := _build_payload(input_value)
    var second := _build_payload(input_value)
    if not bool(first.get("success", false)) or not bool(second.get("success", false)):
        _fail(str(first.get("error", second.get("error", "unknown payload build failure"))))
        return
    var first_payload: Dictionary = first["payload"]
    var second_payload: Dictionary = second["payload"]
    var payload_hash := _sha256(first_payload)
    var repeat_hash := _sha256(second_payload)
    if payload_hash.is_empty() or payload_hash != repeat_hash:
        _fail("independent payload materializations are not byte-canonical deterministic")
        return

    var request: Dictionary = input_value["request_identity"]
    var selection: Dictionary = request["selection"]
    var parameter_instance: Dictionary = input_value["parameter_instance"]
    var envelope: Dictionary = first["envelope"]
    var variation: Dictionary = first["variation"]
    var palette: Dictionary = first["palette"]
    var spec: Dictionary = first_payload["visual_spec"]
    var report := {
        "schema": PROBE_SCHEMA,
        "schema_version": "2.0",
        "status": "IN_MEMORY_REVIEW_ONLY_EXACT_SELECTOR_VISUAL_PAYLOAD_NOT_RENDERER_INPUT",
        "contract_sha256": str(input_value["contract_sha256"]),
        "parent_binding_report_sha256": str(input_value["parent_binding_report_sha256"]),
        "request_identity": request.duplicate(true),
        "canonical_chain": input_value["canonical_chain"].duplicate(true),
        "timing_review_reference": input_value["timing_review_reference"].duplicate(true),
        "parent_request_parameter_binding_sha256": str(input_value["request_parameter_binding_sha256"]),
        "parameter_instance_sha256": str(parameter_instance["parameter_instance_sha256"]),
        "selection": selection.duplicate(true),
        "grammar_id": str(parameter_instance["grammar_id"]),
        "grammar_index": int(parameter_instance["grammar_index"]),
        "shader_branch_review_only": str(parameter_instance["shader_branch"]),
        "authoring_envelope_sha256": _sha256(envelope),
        "family_variation_recipe_sha256": _sha256(variation),
        "resolved_palette_sha256": _sha256(palette),
        "visual_spec_sha256": _sha256(spec),
        "payload_instance_sha256": payload_hash,
        "payload_sections": ["request_identity", "selection", "authoring_envelope", "family_variation_recipe", "resolved_palette", "visual_spec", "timing"],
        "payload_materialized_in_memory": true,
        "deterministic_repeat_pass": true,
        "exact_selector_visual_payload_materialized": true,
        "renderer_shader_mapping_is_review_metadata_only": true,
        "policy_values_consumed": false,
        "non_geometric_family_authoring_gaps_remain_open": true,
        "family_authoring_envelope_gap": "REMAINS_OPEN_OUTSIDE_THIS_GEOMETRIC_SELECTOR_SCOPE",
        "source_checks_passed": true,
        "execution_boundary": BOUNDARY.duplicate(true)
    }
    print(PREFIX + JSON.stringify(_stable_value(report)))
    print("C11-D VISUAL LOOP EXACT SELECTOR PAYLOAD V2 PROBE PASS | grammar=" + str(report["grammar_id"]) + "@" + str(report["grammar_index"]) + " | payload_materialized_in_memory=true | deterministic_repeat=true | renderer_input=false | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
    quit(0)

func _build_payload(v: Dictionary) -> Dictionary:
    var request: Dictionary = v["request_identity"]
    var selection: Dictionary = request["selection"]
    var grammar_id := str(selection["subtype_id"])
    var grammar_index := GRAMMAR_IDS.find(grammar_id)
    var parameter_instance: Dictionary = v["parameter_instance"]
    if grammar_index < 0 or int(parameter_instance.get("grammar_index", -1)) != grammar_index or str(parameter_instance.get("grammar_id", "")) != grammar_id:
        return {"success": false, "error": "request selector and bound parameter instance do not match"}
    if str(parameter_instance.get("shader_branch", "")) != SHADER_BRANCHES[grammar_index] or str(parameter_instance.get("shader_uniform", "")) != "grammar_mode":
        return {"success": false, "error": "shader branch review mapping does not match the selected grammar"}

    var seed := int(request["gameplay_seed"])
    var variation_a: Dictionary = C11CVariationProfileScript.build("geometric", seed)
    var variation_b: Dictionary = C11CVariationProfileScript.build("geometric", seed)
    if variation_a.is_empty() or variation_b.is_empty() or variation_a != variation_b:
        return {"success": false, "error": "C11-C variation profile is not deterministic"}
    variation_a["grammar_mode"] = grammar_index
    variation_a["grammar_name"] = grammar_id
    variation_b["grammar_mode"] = grammar_index
    variation_b["grammar_name"] = grammar_id
    var profile_styles_a := _project_style_parameters(variation_a)
    var profile_styles_b := _project_style_parameters(variation_b)
    if profile_styles_a != profile_styles_b:
        return {"success": false, "error": "independent C11-C profile projections are not deterministic"}

    # The parent binder has already derived, hashed, and validated these exact 20 values
    # in its own Godot probe. Consume that request-bound instance rather than compare a
    # second JSON-round-tripped Dictionary with strict Variant-type equality.
    var styles_a: Dictionary = parameter_instance.get("style_parameters", {}).duplicate(true)
    # JSON transport can deserialize integer-valued style fields as floats.
    # Restore the canonical types used when the upstream digests were created.
    if styles_a.has("grammar_mode"):
        styles_a["grammar_mode"] = int(styles_a["grammar_mode"])
    if styles_a.has("palette_mode"):
        styles_a["palette_mode"] = int(styles_a["palette_mode"])
    var expected_style_keys: Array[String] = STYLE_KEYS.duplicate()
    var observed_style_keys: Array = styles_a.keys()
    observed_style_keys.sort()
    expected_style_keys.sort()
    if styles_a.size() != STYLE_KEYS.size() or observed_style_keys != expected_style_keys:
        return {"success": false, "error": "request-bound style instance must contain the exact 20 named parameters"}

    var projection_mismatches: Array[String] = []
    for key: String in STYLE_KEYS:
        if not profile_styles_a.has(key) or not styles_a.has(key):
            projection_mismatches.append(key + "(missing)")
            continue
        var projected_value: Variant = profile_styles_a[key]
        var bound_value: Variant = styles_a[key]
        var projected_type := typeof(projected_value)
        var bound_type := typeof(bound_value)
        if (projected_type != TYPE_INT and projected_type != TYPE_FLOAT) or (bound_type != TYPE_INT and bound_type != TYPE_FLOAT):
            if projected_value != bound_value:
                projection_mismatches.append(key + "(profile=" + str(projected_value) + ",bound=" + str(bound_value) + ")")
        else:
            var absolute_delta: float = absf(float(projected_value) - float(bound_value))
            if absolute_delta > STYLE_PROJECTION_ABS_TOLERANCE:
                projection_mismatches.append(key + "(profile=" + str(projected_value) + ",bound=" + str(bound_value) + ",abs_delta=" + str(absolute_delta) + ",tolerance=" + str(STYLE_PROJECTION_ABS_TOLERANCE) + ")")
    if not projection_mismatches.is_empty():
        return {"success": false, "error": "C11-C style projection differs from the request-bound parameter instance: " + "; ".join(projection_mismatches)}

    if int(styles_a.get("grammar_mode", -1)) != grammar_index:
        return {"success": false, "error": "bound style grammar_mode differs from the selected grammar index"}
    if _sha256(styles_a) != str(parameter_instance.get("style_parameters_sha256", "")):
        return {"success": false, "error": "request-bound style-parameter digest does not validate after transport"}

    var core := {
        "schema": str(parameter_instance.get("schema", "")),
        "schema_version": str(parameter_instance.get("schema_version", "")),
        "selection": selection.duplicate(true),
        "grammar_id": grammar_id,
        "grammar_index": grammar_index,
        "shader_branch": SHADER_BRANCHES[grammar_index],
        "shader_uniform": "grammar_mode",
        "style_parameter_count": STYLE_KEYS.size(),
        "style_parameters": styles_a,
        "gameplay_seed": seed,
        "request_hash": str(request["request_hash"])
    }
    if _sha256(core) != str(parameter_instance.get("parameter_instance_sha256", "")):
        return {"success": false, "error": "parameter-instance digest does not match the exact selector/values"}

    var loop_cycles := int(round(float(variation_a.get("loop_cycles", 1.0))))
    var duration_seconds := float(C11CVisualLoopDurationScript.policy_seconds_for_cycles(loop_cycles))
    var frame_count := int(round(duration_seconds * float(FPS)))
    var palette: Dictionary = C11CPaletteBankScript.palette("geometric", int(styles_a["palette_mode"]), seed)
    var palette_name := str(variation_a.get("palette_name", "default"))
    var authoring_request: VisualAuthoringRequest = VisualAuthoringRequestScript.new("visual_loop", "geometric", duration_seconds, FPS, 2, {"color_palette": palette_name})
    var context: VisualAuthoringAssemblyContext = _make_context(request, "c11c_geometric_waves_v1")
    var generated: Dictionary = VisualAuthoringGeneratorScript.generate(authoring_request, context, {})
    if not bool(generated.get("success", false)):
        return {"success": false, "error": "VisualAuthoringGenerator rejected the canonical geometric authoring request: " + str(generated.get("errors", []))}
    var envelope: Dictionary = generated.get("content", {})
    var envelope_payload: Dictionary = envelope.get("payload", {})
    if envelope.get("kind") != "visual_loop" or envelope.get("subtype") != "geometric":
        return {"success": false, "error": "canonical C11-C authoring envelope identity mismatch"}
    if int(envelope_payload.get("fps", -1)) != FPS or int(envelope_payload.get("frame_count", -1)) != frame_count or float(envelope_payload.get("duration", -1.0)) != duration_seconds:
        return {"success": false, "error": "authored duration/frame count does not match the frozen C11-C Visual Loop duration policy"}
    var layers: Array = envelope_payload.get("visual_parameters", {}).get("layers", [])
    if layers.is_empty() or str(layers[0].get("color_palette", "")) != palette_name:
        return {"success": false, "error": "authoring envelope palette selection diverges from C11-C profile"}

    var selected_payload := {
        "schema": "C11-D-D9-REVIEW-ONLY-EXACT-SELECTOR-VISUAL-LOOP-PAYLOAD-V2",
        "schema_version": "2.0",
        "status": "IN_MEMORY_REVIEW_ONLY_NOT_RENDERER_INPUT",
        "frozen_c11c_manifest_sha256": FROZEN_C11C_MANIFEST_SHA256,
        "request_identity": request.duplicate(true),
        "selection": selection.duplicate(true),
        "authoring_envelope": envelope.duplicate(true),
        "family_variation_recipe": variation_a.duplicate(true),
        "resolved_palette": palette.duplicate(true),
        "visual_spec": {
            "family_id": "c11c_geometric_waves_v1",
            "grammar_id": grammar_id,
            "grammar_index": grammar_index,
            "style_parameter_count": STYLE_KEYS.size(),
            "style_parameters": styles_a.duplicate(true),
            "palette": palette.duplicate(true),
            "timing": {"fps": FPS, "duration_seconds": duration_seconds, "frame_count": frame_count, "loop_cycles": loop_cycles}
        },
        "timing": {"fps": FPS, "duration_seconds": duration_seconds, "frame_count": frame_count, "loop_cycles": loop_cycles, "source": "C11CVisualLoopDuration.policy_seconds_for_cycles"}
    }
    if _contains_forbidden_truth(selected_payload):
        return {"success": false, "error": "visual payload contains prohibited simulation-truth or telemetry fields"}
    return {"success": true, "payload": selected_payload, "envelope": envelope, "variation": variation_a, "palette": palette}

func _make_context(request: Dictionary, asset_family_id: String) -> VisualAuthoringAssemblyContext:
    return VisualAuthoringAssemblyContextScript.new(
        int(request["gameplay_seed"]),
        "2.0",
        str(request["request_id"]),
        "1.0",
        "C11-C-2.19.12",
        {"profile_id": str(request["presentation_profile_id"]), "coordinate_space": "CANVAS_540X960"},
        {"family_id": asset_family_id},
        {"profile_id": "default_procedural_music", "enabled": true},
        {"author": "C11D_IN_MEMORY_EXACT_SELECTOR_PAYLOAD_V2", "timestamp_ms": 0}
    )

func _project_style_parameters(value: Dictionary) -> Dictionary:
    for key: String in PROFILE_INPUT_KEYS:
        if not value.has(key): return {}
    return {
        "grammar_mode": clampi(int(value["grammar_mode"]), 0, 4),
        "palette_mode": clampi(int(value["palette_mode"]), 0, 4),
        "morph": clamp(float(value["morph"]), 0.0, 1.0),
        "wave_frequency": max(float(value["wave_frequency"]), 5.0),
        "line_width": max(float(value["line_width"]), 0.001),
        "glow_strength": clamp(float(value["glow"]), 0.0, 1.0),
        "polygon_sides": clamp(float(value["polygon_sides"]), 5.0, 8.0),
        "wave_ratio": clamp(float(value["wave_ratio"]), 0.60, 1.05),
        "shape_rotation": float(value["shape_rotation"]),
        "layer_spread": clamp(float(value["layer_spread"]), 0.0, 0.10),
        "radial_wave_amplitude": clamp(float(value["radial_wave_amplitude"]), 0.008, 0.08),
        "liss_x_frequency": clamp(float(value["liss_x_frequency"]), 3.0, 16.0),
        "liss_y_frequency": clamp(float(value["liss_y_frequency"]), 2.0, 12.0),
        "interference_scale": clamp(float(value["interference_scale"]), 0.65, 1.55),
        "hero_scale": clamp(float(value["hero_scale"]), 0.76, 1.06),
        "perspective_strength": clamp(float(value["perspective_strength"]), 0.20, 1.20),
        "depth_strength": clamp(float(value["depth_strength"]), 0.20, 1.0),
        "secondary_phase": float(value["secondary_phase"]),
        "color_phase": float(value["color_phase"]),
        "stroke_scale": clamp(float(value["stroke_scale"]), 0.72, 1.40)
    }

func _validate_input(v: Dictionary) -> Array[String]:
    var errors: Array[String] = []
    var expected_keys := ["schema", "schema_version", "contract_sha256", "frozen_c11c_manifest_sha256", "parent_binding_report_sha256", "request_identity", "canonical_chain", "timing_review_reference", "request_parameter_binding_sha256", "parameter_instance"]
    var actual_keys: Array = v.keys(); actual_keys.sort(); expected_keys.sort()
    if actual_keys != expected_keys:
        errors.append("input keys do not match the strict contract")
        return errors
    if str(v.get("schema", "")) != INPUT_SCHEMA or str(v.get("schema_version", "")) != "2.0": errors.append("input identity/version mismatch")
    if str(v.get("frozen_c11c_manifest_sha256", "")) != FROZEN_C11C_MANIFEST_SHA256: errors.append("frozen C11-C manifest mismatch")
    for key: String in ["contract_sha256", "parent_binding_report_sha256", "request_parameter_binding_sha256"]:
        if not _is_sha256(str(v.get(key, ""))): errors.append("invalid digest: " + key)

    var request: Variant = v.get("request_identity", null)
    if not (request is Dictionary):
        errors.append("request_identity must be a Dictionary")
        return errors
    var selection: Variant = request.get("selection", null)
    if not (selection is Dictionary):
        errors.append("request selection must be a Dictionary")
        return errors
    var selection_keys: Array = selection.keys(); selection_keys.sort()
    if selection_keys != ["content_type", "family_id", "subtype_id", "variant_id"]: errors.append("selection keys are not exact")
    var grammar_id := str(selection.get("subtype_id", ""))
    if str(selection.get("content_type", "")) != "visual_loops" or str(selection.get("family_id", "")) != "c11c_geometric_waves_v1" or selection.get("variant_id") != null or not GRAMMAR_IDS.has(grammar_id): errors.append("selection outside the fixed Geometric Waves selector matrix")
    if not _is_sha256(str(request.get("request_hash", ""))): errors.append("request hash malformed")
    var request_keys: Array = request.keys(); request_keys.sort()
    var expected_request_keys: Array = ["request_id", "request_hash", "selection", "gameplay_seed", "music_seed", "variation_index", "presentation_profile_id", "delivery_profile_id"]
    expected_request_keys.sort()
    if request_keys != expected_request_keys: errors.append("request identity keys are not exact")
    if int(request.get("gameplay_seed", 0)) < 1 or int(request.get("music_seed", 0)) < 1: errors.append("seed outside D9.9 domain")
    if int(request.get("variation_index", -1)) < 0: errors.append("variation_index outside D9.9 domain")
    if str(request.get("presentation_profile_id", "")) != "social_default_v1" or str(request.get("delivery_profile_id", "")) != "REVIEW_720": errors.append("request profile outside the review fixture scope")

    var param: Variant = v.get("parameter_instance", null)
    if not (param is Dictionary):
        errors.append("parameter_instance must be a Dictionary")
        return errors
    var param_grammar := str(param.get("grammar_id", ""))
    if param_grammar != grammar_id or int(param.get("grammar_index", -1)) != GRAMMAR_IDS.find(grammar_id): errors.append("parameter instance selector mismatch")
    if str(param.get("request_hash", "")) != str(request.get("request_hash", "")) or int(param.get("gameplay_seed", 0)) != int(request.get("gameplay_seed", -1)): errors.append("parameter instance request identity mismatch")
    var style: Variant = param.get("style_parameters", null)
    if not (style is Dictionary):
        errors.append("style_parameters must be a Dictionary")
    else:
        var style_keys: Array = style.keys(); style_keys.sort()
        var expected_style_keys: Array = STYLE_KEYS.duplicate(); expected_style_keys.sort()
        if style_keys != expected_style_keys or int(param.get("style_parameter_count", -1)) != STYLE_KEYS.size(): errors.append("style parameter set/count mismatch")
    var chain: Variant = v.get("canonical_chain", null)
    if not (chain is Dictionary): errors.append("canonical_chain must be a Dictionary")
    else:
        for key: String in ["plan_hash", "editorial_hash", "bridge_record_hash", "adapter_envelope_hash", "source_binding_sha256"]:
            if not _is_sha256(str(chain.get(key, ""))): errors.append("canonical chain digest malformed: " + key)
        if str(chain.get("plan_hash", "")) == str(chain.get("editorial_hash", "")): errors.append("plan and editorial hashes must remain distinct")
    var refs: Variant = v.get("timing_review_reference", null)
    if not (refs is Dictionary): errors.append("timing_review_reference must be a Dictionary")
    else:
        for key: String in ["carrier_report_sha256", "selector_envelope_sha256", "shared_policy_reference_set_sha256"]:
            if not _is_sha256(str(refs.get(key, ""))): errors.append("timing/review digest malformed: " + key)
        if int(refs.get("policy_reference_count", 0)) != 9 or refs.get("policy_values_consumed") != false: errors.append("timing/review boundary mismatch")
    return errors

func _source_checks_error() -> String:
    var manifest := FileAccess.get_file_as_string("res://release/C11C_FREEZE_PACKAGE_MANIFEST.json")
    var profile := FileAccess.get_file_as_string("res://tools/prototypes/c11c_common/C11CVariationProfile.gd")
    var palette_bank := FileAccess.get_file_as_string("res://tools/prototypes/c11c_common/C11CPaletteBank.gd")
    var shader := FileAccess.get_file_as_string("res://tools/prototypes/c11c_geometric_waves_v1/GeometricWaves.gdshader")
    var renderer := FileAccess.get_file_as_string("res://tools/prototypes/c11c_geometric_waves_v1/GeometricWavesRenderer.gd")
    var prototype := FileAccess.get_file_as_string("res://tools/prototypes/c11c_geometric_waves_v1/GeometricWavesPrototype.gd")
    if manifest.is_empty() or profile.is_empty() or palette_bank.is_empty() or shader.is_empty() or renderer.is_empty() or prototype.is_empty(): return "required frozen source is unreadable"
    var manifest_bytes := FileAccess.get_file_as_bytes("res://release/C11C_FREEZE_PACKAGE_MANIFEST.json")
    if _sha256_bytes(manifest_bytes) != FROZEN_C11C_MANIFEST_SHA256: return "frozen C11-C manifest hash mismatch"
    for grammar_id in GRAMMAR_IDS:
        if not profile.contains('"' + grammar_id + '"') or not shader.contains("field_" + grammar_id): return "grammar identity absent from frozen profile/shader: " + grammar_id
    for branch in SHADER_BRANCHES:
        if not shader.contains("vec4 " + branch + "("): return "shader branch source missing: " + branch
    for key in STYLE_KEYS:
        var token := '"' + key + '"'
        var renderer_token := '"' + key + '"'
        if key != "glow_strength" and not renderer.contains(renderer_token): return "renderer style binding token missing: " + key
    if not prototype.contains("_apply_grammar_override") or not prototype.contains("_seed_phase"): return "frozen geometric prototype route changed"
    return ""

func _contains_forbidden_truth(value: Variant) -> bool:
    var forbidden := ["simulation_result", "simulationresult", "simulation_truth", "simulationtruth", "winning_frame", "winningframe", "close_calls", "closecalls", "gameplay_rng", "structural_rng", "derived_telemetry"]
    if value is Dictionary:
        for key in value.keys():
            var normalized := str(key).to_lower().replace("-", "_")
            if forbidden.has(normalized) or _contains_forbidden_truth(value[key]): return true
    elif value is Array:
        for item in value:
            if _contains_forbidden_truth(item): return true
    return false

func _decode_input() -> Dictionary:
    var args := OS.get_cmdline_user_args()
    if args.size() != 1: return {}
    var parsed: Variant = JSON.parse_string(Marshalls.base64_to_utf8(args[0]))
    if not (parsed is Dictionary): return {}
    return parsed

func _canonicalize(value: Variant) -> Variant:
    if value is Dictionary:
        var keys: Array = value.keys(); keys.sort()
        var result: Dictionary = {}
        for key in keys: result[str(key)] = _canonicalize(value[key])
        return result
    if value is Array:
        var items: Array = []
        for child in value: items.append(_canonicalize(child))
        return items
    return value

func _sha256(value: Variant) -> String:
    var ctx := HashingContext.new()
    if ctx.start(HashingContext.HASH_SHA256) != OK: return ""
    ctx.update(JSON.stringify(_canonicalize(value)).to_utf8_buffer())
    return ctx.finish().hex_encode()

func _sha256_string(value: String) -> String:
    var ctx := HashingContext.new()
    if ctx.start(HashingContext.HASH_SHA256) != OK: return ""
    ctx.update(value.to_utf8_buffer())
    return ctx.finish().hex_encode()

func _sha256_bytes(value: PackedByteArray) -> String:
    var ctx := HashingContext.new()
    if ctx.start(HashingContext.HASH_SHA256) != OK: return ""
    ctx.update(value)
    return ctx.finish().hex_encode()

func _is_sha256(value: String) -> bool:
    if value.length() != 64: return false
    for character in value:
        if not "0123456789abcdef".contains(character): return false
    return true

func _stable_value(value: Variant) -> Variant:
    return _canonicalize(value)

func _fail(message: String) -> void:
    push_error("C11-D VISUAL LOOP EXACT SELECTOR PAYLOAD V2 PROBE FAIL | " + message)
    quit(1)
