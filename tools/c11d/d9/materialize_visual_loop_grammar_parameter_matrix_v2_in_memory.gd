extends SceneTree

## Builds one exact, D-owned grammar parameter instance in memory from a canonical
## D9.9 request. The harness never creates a renderer, shader/material, payload file,
## renderer-native input, rendered output, or media.
const Profile = preload("res://tools/prototypes/c11c_common/C11CVariationProfile.gd")
const PROFILE_SOURCE := "res://tools/prototypes/c11c_common/C11CVariationProfile.gd"
const PROTOTYPE_SOURCE := "res://tools/prototypes/c11c_geometric_waves_v1/GeometricWavesPrototype.gd"
const RENDERER_SOURCE := "res://tools/prototypes/c11c_geometric_waves_v1/GeometricWavesRenderer.gd"
const SHADER_SOURCE := "res://tools/prototypes/c11c_geometric_waves_v1/GeometricWaves.gdshader"
const GRAMMAR_IDS: Array[String] = ["harmonic_membrane", "interference_plane", "parametric_ribbon", "lattice_wave", "orbital_wave"]
const SHADER_BRANCHES: Array[String] = ["field_harmonic_membrane", "field_interference_plane", "field_parametric_ribbon", "field_lattice_wave", "field_orbital_wave"]
const STYLE_KEYS: Array[String] = ["grammar_mode", "palette_mode", "morph", "wave_frequency", "line_width", "glow_strength", "polygon_sides", "wave_ratio", "shape_rotation", "layer_spread", "radial_wave_amplitude", "liss_x_frequency", "liss_y_frequency", "interference_scale", "hero_scale", "perspective_strength", "depth_strength", "secondary_phase", "color_phase", "stroke_scale"]
const PROFILE_INPUT_KEYS: Array[String] = ["grammar_mode", "palette_mode", "morph", "wave_frequency", "line_width", "glow", "polygon_sides", "wave_ratio", "shape_rotation", "layer_spread", "radial_wave_amplitude", "liss_x_frequency", "liss_y_frequency", "interference_scale", "hero_scale", "perspective_strength", "depth_strength", "secondary_phase", "color_phase", "stroke_scale"]
const INPUT_SCHEMA := "C11-D-D9-VISUAL-LOOP-GRAMMAR-PARAMETER-MATRIX-INPUT-V2"
const PROBE_SCHEMA := "C11-D-D9-VISUAL-LOOP-GRAMMAR-PARAMETER-MATRIX-PROBE-V2"
const MANIFEST_SHA := "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
const PREFIX := "C11D_VISUAL_LOOP_GRAMMAR_PARAMETER_MATRIX_V2_PROBE="

func _initialize() -> void:
    call_deferred("_run")

func _run() -> void:
    var input_value := _decode_input()
    if input_value.is_empty():
        _fail("missing or invalid base64 JSON input")
        return
    var errors := _validate_input(input_value)
    if not errors.is_empty():
        _fail("Invalid grammar parameter matrix input: " + "; ".join(errors))
        return
    var source_check_error := _source_checks_error()
    if not source_check_error.is_empty():
        _fail("Frozen C11-C profile/prototype/style source check failed: " + source_check_error)
        return

    var request: Dictionary = input_value["request"]
    var selection: Dictionary = request["selection"]
    var grammar_id := str(selection["subtype_id"])
    var grammar_index := GRAMMAR_IDS.find(grammar_id)
    if grammar_index < 0 or grammar_index >= GRAMMAR_IDS.size():
        _fail("Selected grammar is outside the fixed five-grammar matrix.")
        return
    if selection["content_type"] != "visual_loops" or selection["family_id"] != "c11c_geometric_waves_v1" or selection["variant_id"] != null:
        _fail("Selected request identity is not an exact Geometric Waves Visual Loop.")
        return

    var raw_a: Dictionary = Profile.build("geometric", int(request["seed"]))
    var raw_b: Dictionary = Profile.build("geometric", int(request["seed"]))
    if raw_a.is_empty() or raw_b.is_empty() or raw_a != raw_b:
        _fail("C11-C profile did not reproduce deterministically for this request seed.")
        return
    var bound_a: Dictionary = raw_a.duplicate(true)
    var bound_b: Dictionary = raw_b.duplicate(true)
    # The D-owned request selector is applied to local profile copies only. This
    # deliberately does not mutate C11-C or claim that a complete visual payload exists.
    bound_a["grammar_mode"] = grammar_index
    bound_a["grammar_name"] = grammar_id
    bound_b["grammar_mode"] = grammar_index
    bound_b["grammar_name"] = grammar_id
    var styles_a := _project_style_parameters(bound_a)
    var styles_b := _project_style_parameters(bound_b)
    if styles_a.size() != STYLE_KEYS.size() or styles_b.size() != STYLE_KEYS.size() or styles_a != styles_b:
        _fail("Selected grammar style projection is incomplete or non-deterministic.")
        return
    if int(styles_a.get("grammar_mode", -1)) != grammar_index:
        _fail("Projected grammar_mode does not match the exact requested grammar index.")
        return

    var instance_core := {
        "schema": "C11-D-D9-VISUAL-LOOP-GRAMMAR-PARAMETER-INSTANCE-V2",
        "schema_version": "2.0",
        "selection": selection.duplicate(true),
        "grammar_id": grammar_id,
        "grammar_index": grammar_index,
        "shader_branch": SHADER_BRANCHES[grammar_index],
        "shader_uniform": "grammar_mode",
        "style_parameter_count": STYLE_KEYS.size(),
        "style_parameters": styles_a,
        "gameplay_seed": int(request["seed"]),
        "request_hash": str(request["request_hash"])
    }
    var instance := instance_core.duplicate(true)
    instance["style_parameters_sha256"] = _sha256(styles_a)
    instance["parameter_instance_sha256"] = _sha256(instance_core)

    var report := {
        "schema": PROBE_SCHEMA,
        "schema_version": "2.0",
        "status": "PREPARATION_ONLY_REQUEST_BOUND_GRAMMAR_PARAMETER_INSTANCE_IN_MEMORY_NOT_EXACT_VISUAL_PAYLOAD",
        "contract_sha256": input_value["contract_sha256"],
        "request_id": request["request_id"],
        "request_hash": request["request_hash"],
        "selection": selection.duplicate(true),
        "gameplay_seed": int(request["seed"]),
        "music_seed": int(request["music_seed"]),
        "variation_index": int(request["variation_index"]),
        "presentation_profile_id": request["presentation_profile_id"],
        "delivery_profile_id": request["delivery_profile_id"],
        "canonical_chain": input_value["canonical_chain"].duplicate(true),
        "timing_review_reference": input_value["timing_review_reference"].duplicate(true),
        "parameter_instance": instance,
        "repeat_deterministic": true,
        "source_checks_passed": true,
        "request_input_persisted": false,
        "parameter_payload_files_written": false,
        "receipt_files_written": false,
        "renderer_instance_created": false,
        "renderer_native_input_emitted": false,
        "renderer_dispatch_invoked": false,
        "shader_executed": false,
        "media_created": false,
        "c11c_source_mutation": false,
        "candidate_input_admissible": false,
        "renderer": "OFF",
        "d4_8": "BLOCKED",
        "release_authority": "NONE",
        "d9_17": "BLOCKED_NO_GO",
        "d10": "BLOCKED"
    }
    print(PREFIX + JSON.stringify(_stable_value(report)))
    print("C11-D VISUAL LOOP GRAMMAR PARAMETER MATRIX V2 PROBE PASS | grammar=" + grammar_id + "@" + str(grammar_index) + " | style_parameters=20/20 | source_profile_copy_only=true | exact_selector_visual_payload=false | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
    quit(0)

func _decode_input() -> Dictionary:
    var args := OS.get_cmdline_user_args()
    if args.size() != 1:
        return {}
    var raw := Marshalls.base64_to_utf8(args[0])
    var parsed: Variant = JSON.parse_string(raw)
    if not (parsed is Dictionary):
        return {}
    return parsed

func _validate_input(v: Dictionary) -> Array[String]:
    var errors: Array[String] = []
    var expected_keys := ["schema", "schema_version", "contract_sha256", "frozen_c11c_manifest_sha256", "request", "canonical_chain", "timing_review_reference"]
    var keys: Array = v.keys(); keys.sort(); expected_keys.sort()
    if keys != expected_keys:
        errors.append("input object keys are not exact")
        return errors
    if str(v.get("schema", "")) != INPUT_SCHEMA or str(v.get("schema_version", "")) != "2.0": errors.append("input schema identity mismatch")
    if str(v.get("frozen_c11c_manifest_sha256", "")) != MANIFEST_SHA: errors.append("frozen C11-C manifest mismatch")
    if not _is_sha256(str(v.get("contract_sha256", ""))): errors.append("contract SHA-256 malformed")

    var request: Variant = v.get("request", null)
    if not (request is Dictionary):
        errors.append("request must be an object")
        return errors
    var request_keys := ["schema", "schema_version", "request_id", "request_hash", "selection", "seed", "music_seed", "variation_index", "presentation_profile_id", "delivery_profile_id"]
    var actual_request_keys: Array = request.keys(); actual_request_keys.sort(); request_keys.sort()
    if actual_request_keys != request_keys:
        errors.append("canonical request input keys are not exact")
        return errors
    if str(request.get("schema", "")) != "C11-D-D9-DYNAMIC-REQUEST-PAYLOAD-INPUT-V1" or str(request.get("schema_version", "")) != "1.0": errors.append("canonical request schema mismatch")
    if str(request.get("presentation_profile_id", "")) != "social_default_v1": errors.append("presentation profile outside the pinned review scope")
    if not ["REVIEW_720", "MIN_540", "MASTER_1080", "META_REELS_FINAL_V1"].has(str(request.get("delivery_profile_id", ""))): errors.append("delivery profile outside the pinned non-Longform review scope")
    if not _is_sha256(str(request.get("request_hash", ""))): errors.append("request hash malformed")
    if str(request.get("request_id", "")).is_empty() or str(request.get("request_id", "")).length() > 160: errors.append("request identity invalid")
    for key: String in ["seed", "music_seed"]:
        if not _is_integer_in_range(request.get(key, null), 1, 2147483646): errors.append("%s outside D9.9 seed domain" % key)
    if not _is_integer_in_range(request.get("variation_index", null), 0, 1000000): errors.append("variation_index outside D9.9 domain")
    var selection: Variant = request.get("selection", null)
    if not (selection is Dictionary):
        errors.append("selection must be an object")
        return errors
    var selector_keys := ["content_type", "family_id", "subtype_id", "variant_id"]
    var actual_selector_keys: Array = selection.keys(); actual_selector_keys.sort(); selector_keys.sort()
    if actual_selector_keys != selector_keys:
        errors.append("selector keys are not exact")
    else:
        if str(selection.get("content_type", "")) != "visual_loops" or str(selection.get("family_id", "")) != "c11c_geometric_waves_v1" or selection.get("variant_id", null) != null: errors.append("selector family/type/variant mismatch")
        if not GRAMMAR_IDS.has(str(selection.get("subtype_id", ""))): errors.append("selector grammar outside fixed matrix")

    for group_name in ["canonical_chain", "timing_review_reference"]:
        var group: Variant = v.get(group_name, null)
        if not (group is Dictionary):
            errors.append(group_name + " must be an object")
            continue
        var expected_group_keys: Array = []
        if group_name == "canonical_chain":
            expected_group_keys = ["plan_hash", "editorial_hash", "bridge_record_hash", "adapter_envelope_hash", "source_binding_sha256"]
        else:
            expected_group_keys = ["carrier_report_sha256", "selector_envelope_sha256", "shared_policy_reference_set_sha256", "policy_reference_count", "policy_values_consumed"]
        var actual_group_keys: Array = group.keys(); actual_group_keys.sort(); expected_group_keys.sort()
        if actual_group_keys != expected_group_keys:
            errors.append(group_name + " keys are not exact")
            continue
        if group_name == "canonical_chain":
            for key: String in expected_group_keys:
                if not _is_sha256(str(group.get(key, ""))): errors.append(group_name + " hash malformed: " + key)
        else:
            for key: String in ["carrier_report_sha256", "selector_envelope_sha256", "shared_policy_reference_set_sha256"]:
                if not _is_sha256(str(group.get(key, ""))): errors.append(group_name + " hash malformed: " + key)
            if group.get("policy_reference_count") != 9 or group.get("policy_values_consumed") != false: errors.append("timing/review reference boundary changed")
    return errors

func _source_checks_error() -> String:
    var profile := FileAccess.get_file_as_string(PROFILE_SOURCE)
    var proto := FileAccess.get_file_as_string(PROTOTYPE_SOURCE)
    var renderer := FileAccess.get_file_as_string(RENDERER_SOURCE)
    var shader := FileAccess.get_file_as_string(SHADER_SOURCE)
    if profile.is_empty() or proto.is_empty() or renderer.is_empty() or shader.is_empty(): return "cannot read required frozen C11-C geometric source"
    var geometric_start := profile.find("static func _geometric(seed_value: int) -> Dictionary:")
    var fractal_start := profile.find("static func _fractal(seed_value: int) -> Dictionary:")
    if geometric_start < 0 or fractal_start <= geometric_start: return "cannot locate geometric profile function boundaries"
    var geometric_profile := profile.substr(geometric_start, fractal_start - geometric_start)
    for token: String in ["var grammar_modes: Array[String] = [", "\"harmonic_membrane\"", "\"interference_plane\"", "\"parametric_ribbon\"", "\"lattice_wave\"", "\"orbital_wave\""]:
        if not geometric_profile.contains(token): return "geometric profile is missing token: " + token
    for token: String in ['OS.get_environment("C11C_VISUAL_GRAMMAR")', '_variation["grammar_mode"] = index', '_variation["grammar_name"] = technical_id']:
        if not proto.contains(token): return "prototype selector override path missing: " + token
    for token: String in ['func set_style(', '_material.set_shader_parameter("grammar_mode", clampi(grammar_mode, 0, 4))', '_material.set_shader_parameter("wave_frequency", max(wave_frequency, 5.0))']:
        if not renderer.contains(token): return "renderer style mapping missing: " + token
    if not shader.contains("uniform int grammar_mode = 0;"):
        return "shader grammar_mode uniform declaration missing"
    for index in range(4):
        if not shader.contains("if (grammar_mode == " + str(index) + ")") or not shader.contains("return " + SHADER_BRANCHES[index] + "(q, local_phase, layer);"):
            return "shader branch/index mapping missing or changed: " + GRAMMAR_IDS[index]
    if not shader.contains("return " + SHADER_BRANCHES[4] + "(q, local_phase, layer);"):
        return "shader final fallback branch missing or changed: " + GRAMMAR_IDS[4]
    return ""

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

func _stable_value(value: Variant) -> Variant:
    if value is Dictionary:
        var keys: Array = value.keys(); keys.sort()
        var stable: Dictionary = {}
        for key in keys: stable[str(key)] = _stable_value(value[key])
        return stable
    if value is Array:
        var result: Array = []
        for item in value: result.append(_stable_value(item))
        return result
    return value

func _sha256(value: Variant) -> String:
    var h := HashingContext.new()
    if h.start(HashingContext.HASH_SHA256) != OK: return ""
    h.update(JSON.stringify(_stable_value(value)).to_utf8_buffer())
    return h.finish().hex_encode()

func _is_sha256(value: String) -> bool:
    if value.length() != 64: return false
    for ch in value:
        if not ((ch >= "0" and ch <= "9") or (ch >= "a" and ch <= "f")): return false
    return true

func _is_integer_in_range(value: Variant, minimum: int, maximum: int) -> bool:
    if typeof(value) == TYPE_BOOL or typeof(value) == TYPE_NIL: return false
    if typeof(value) != TYPE_INT and typeof(value) != TYPE_FLOAT: return false
    var number := float(value)
    return is_finite(number) and number == floor(number) and number >= float(minimum) and number <= float(maximum)

func _fail(message: String) -> void:
    print("C11-D VISUAL LOOP GRAMMAR PARAMETER MATRIX V2 PROBE FAIL | " + message + " | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
    quit(1)
