extends SceneTree

## Creates a grammar-specific parameter dictionary from a canonical D9.9-bound
## request and a copy of frozen C11-CVariationProfile values. No renderer, shader,
## material, native input, persistent payload or media is created.
const Profile = preload("res://tools/prototypes/c11c_common/C11CVariationProfile.gd")
const PROFILE_SOURCE := "res://tools/prototypes/c11c_common/C11CVariationProfile.gd"
const PROTOTYPE_SOURCE := "res://tools/prototypes/c11c_geometric_waves_v1/GeometricWavesPrototype.gd"
const RENDERER_SOURCE := "res://tools/prototypes/c11c_geometric_waves_v1/GeometricWavesRenderer.gd"
const SHADER_SOURCE := "res://tools/prototypes/c11c_geometric_waves_v1/GeometricWaves.gdshader"
const GRAMMAR_IDS: Array[String] = ["harmonic_membrane", "interference_plane", "parametric_ribbon", "lattice_wave", "orbital_wave"]
const SELECTED := "harmonic_membrane"
const SELECTED_INDEX := 0
const STYLE_KEYS: Array[String] = ["grammar_mode", "palette_mode", "morph", "wave_frequency", "line_width", "glow_strength", "polygon_sides", "wave_ratio", "shape_rotation", "layer_spread", "radial_wave_amplitude", "liss_x_frequency", "liss_y_frequency", "interference_scale", "hero_scale", "perspective_strength", "depth_strength", "secondary_phase", "color_phase", "stroke_scale"]
const PROFILE_INPUT_KEYS: Array[String] = ["grammar_mode", "palette_mode", "morph", "wave_frequency", "line_width", "glow", "polygon_sides", "wave_ratio", "shape_rotation", "layer_spread", "radial_wave_amplitude", "liss_x_frequency", "liss_y_frequency", "interference_scale", "hero_scale", "perspective_strength", "depth_strength", "secondary_phase", "color_phase", "stroke_scale"]
const INPUT_SCHEMA := "C11-D-D9-VISUAL-LOOP-GRAMMAR-PARAMETER-INPUT-V1"
const PROBE_SCHEMA := "C11-D-D9-VISUAL-LOOP-GRAMMAR-PARAMETER-PROBE-V1"
const MANIFEST_SHA := "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
const PREFIX := "C11D_GRAMMAR_PARAMETER_INSTANCE_PROBE="

func _initialize() -> void:
    call_deferred("_run")

func _run() -> void:
    var input_value := _decode_input()
    if input_value.is_empty():
        _fail("missing or invalid base64 JSON request input")
        return
    var errors := _validate_input(input_value)
    if not errors.is_empty():
        _fail("Invalid grammar parameter input: " + "; ".join(errors))
        return
    var source_check_error := _source_checks_error()
    if not source_check_error.is_empty():
        _fail("Frozen C11-C grammar/profile/style source check failed: " + source_check_error)
        return
    var request: Dictionary = input_value["request"]
    var grammar_index := GRAMMAR_IDS.find(SELECTED)
    if grammar_index != SELECTED_INDEX:
        _fail("Pinned grammar ID no longer maps to index 0.")
        return
    var raw_a: Dictionary = Profile.build("geometric", int(request["seed"]))
    var raw_b: Dictionary = Profile.build("geometric", int(request["seed"]))
    if raw_a.is_empty() or raw_b.is_empty() or raw_a != raw_b:
        _fail("C11-C profile does not reproduce deterministically for this request seed.")
        return
    var bound_a: Dictionary = raw_a.duplicate(true)
    var bound_b: Dictionary = raw_b.duplicate(true)
    # Explicit D-owned instance binding mirrors the audited frozen prototype override,
    # but is applied only to local copies. It never mutates the frozen source profile.
    bound_a["grammar_mode"] = grammar_index
    bound_a["grammar_name"] = SELECTED
    bound_b["grammar_mode"] = grammar_index
    bound_b["grammar_name"] = SELECTED
    var styles_a := _project_style_parameters(bound_a)
    var styles_b := _project_style_parameters(bound_b)
    if styles_a.size() != 20 or styles_b.size() != 20 or styles_a != styles_b:
        _fail("Request-bound style projection is incomplete or not deterministic.")
        return
    if int(styles_a.get("grammar_mode", -1)) != SELECTED_INDEX:
        _fail("Exact grammar index was not applied to the parameter instance.")
        return
    var selection: Dictionary = request["selection"]
    var instance_core := {
        "schema": "C11-D-D9-VISUAL-LOOP-GRAMMAR-PARAMETER-INSTANCE-V1",
        "schema_version": "1.0",
        "selection": {"content_type":"visual_loops", "family_id":"c11c_geometric_waves_v1", "subtype_id":"harmonic_membrane", "variant_id":null},
        "grammar_id": SELECTED,
        "grammar_index": SELECTED_INDEX,
        "shader_branch": "field_harmonic_membrane",
        "shader_uniform": "grammar_mode",
        "style_parameter_count": STYLE_KEYS.size(),
        "style_parameters": styles_a,
    }
    var instance := instance_core.duplicate(true)
    instance["style_parameters_sha256"] = _sha256(styles_a)
    instance["parameter_instance_sha256"] = _sha256(instance_core)
    var report := {
        "schema": PROBE_SCHEMA,
        "schema_version":"1.0",
        "status":"PREPARATION_ONLY_EXACT_GRAMMAR_PARAMETER_INSTANCE_IN_MEMORY_NOT_RENDERER_INPUT",
        "contract_sha256":input_value["contract_sha256"],
        "request_id":request["request_id"],
        "request_hash":request["request_hash"],
        "selection":selection,
        "gameplay_seed":int(request["seed"]),
        "music_seed":int(request["music_seed"]),
        "variation_index":int(request["variation_index"]),
        "presentation_profile_id":request["presentation_profile_id"],
        "delivery_profile_id":request["delivery_profile_id"],
        "canonical_chain":input_value["canonical_chain"],
        "parameter_instance":instance,
        "repeat_deterministic":true,
        "source_checks_passed":true,
        "renderer_native_input_emitted":false,
        "renderer_instance_created":false,
        "renderer_dispatch_invoked":false,
        "shader_executed":false,
        "media_created":false,
        "disk_writes":false,
        "c11c_source_mutation":false,
        "candidate_input_admissible":false,
        "renderer":"OFF",
        "d4_8":"BLOCKED",
        "release_authority":"NONE",
        "d9_17":"BLOCKED_NO_GO",
        "d10":"BLOCKED"
    }
    print(PREFIX + JSON.stringify(_stable_value(report)))
    print("C11-D VISUAL LOOP GRAMMAR PARAMETER PROBE PASS | grammar=harmonic_membrane@0 | style_parameters=20/20 | source_profile_copy_only=true | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
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
    var keys := ["schema", "schema_version", "contract_sha256", "frozen_c11c_manifest_sha256", "request", "canonical_chain"]
    var got: Array = v.keys(); got.sort(); keys.sort()
    if got != keys:
        errors.append("input keys are not exact")
        return errors
    if str(v.get("schema", "")) != INPUT_SCHEMA or str(v.get("schema_version", "")) != "1.0": errors.append("input schema identity mismatch")
    if str(v.get("frozen_c11c_manifest_sha256", "")) != MANIFEST_SHA: errors.append("frozen C11-C manifest mismatch")
    if not _is_sha256(str(v.get("contract_sha256", ""))): errors.append("contract hash malformed")
    var request: Variant = v.get("request", null)
    if not (request is Dictionary):
        errors.append("request must be an object")
        return errors
    var reqkeys := ["schema", "schema_version", "request_id", "request_hash", "selection", "seed", "music_seed", "variation_index", "presentation_profile_id", "delivery_profile_id"]
    var actual_reqkeys: Array = request.keys(); actual_reqkeys.sort(); reqkeys.sort()
    if actual_reqkeys != reqkeys:
        errors.append("canonical request input keys are not exact")
        return errors
    if str(request.get("schema", "")) != "C11-D-D9-DYNAMIC-REQUEST-PAYLOAD-INPUT-V1" or str(request.get("schema_version", "")) != "1.0": errors.append("canonical request schema mismatch")
    if str(request.get("presentation_profile_id", "")) != "social_default_v1": errors.append("presentation profile is not in scope")
    if not ["REVIEW_720", "MIN_540", "MASTER_1080", "META_REELS_FINAL_V1"].has(str(request.get("delivery_profile_id", ""))): errors.append("delivery profile is outside reviewed non-Longform scope")
    if not _is_sha256(str(request.get("request_hash", ""))): errors.append("canonical request hash malformed")
    if str(request.get("request_id", "")).is_empty() or str(request.get("request_id", "")).length() > 160: errors.append("request identity invalid")
    for key: String in ["seed", "music_seed"]:
        var n: Variant = request.get(key, null)
        if not _is_integer_in_range(n, 1, 2147483646): errors.append("%s outside canonical D9.9 seed domain" % key)
    if not _is_integer_in_range(request.get("variation_index", null), 0, 1000000): errors.append("variation_index outside canonical D9.9 domain")
    var selection: Variant = request.get("selection", null)
    if not (selection is Dictionary):
        errors.append("selection must be an object")
    else:
        var skeys := ["content_type", "family_id", "subtype_id", "variant_id"]
        var actual_skeys: Array = selection.keys(); actual_skeys.sort(); skeys.sort()
        if actual_skeys != skeys: errors.append("selection keys are not exact")
        if str(selection.get("content_type", "")) != "visual_loops" or str(selection.get("family_id", "")) != "c11c_geometric_waves_v1" or str(selection.get("subtype_id", "")) != SELECTED or selection.get("variant_id", null) != null: errors.append("selector not exact pinned harmonic_membrane Visual Loop")
    var chain: Variant = v.get("canonical_chain", null)
    if not (chain is Dictionary):
        errors.append("canonical_chain must be an object")
    else:
        var ckeys := ["plan_hash", "editorial_hash", "bridge_record_hash", "adapter_envelope_hash", "source_binding_sha256"]
        var actual_ckeys: Array = chain.keys(); actual_ckeys.sort(); ckeys.sort()
        if actual_ckeys != ckeys: errors.append("canonical chain keys are not exact")
        for key: String in ckeys:
            if not _is_sha256(str(chain.get(key, ""))): errors.append("canonical chain %s malformed" % key)
    return errors

func _source_checks_error() -> String:
    var profile := FileAccess.get_file_as_string(PROFILE_SOURCE)
    var proto := FileAccess.get_file_as_string(PROTOTYPE_SOURCE)
    var renderer := FileAccess.get_file_as_string(RENDERER_SOURCE)
    var shader := FileAccess.get_file_as_string(SHADER_SOURCE)
    if profile.is_empty(): return "cannot read frozen C11-C variation profile"
    if proto.is_empty(): return "cannot read frozen C11-C geometric prototype"
    if renderer.is_empty(): return "cannot read frozen C11-C geometric renderer"
    if shader.is_empty(): return "cannot read frozen C11-C geometric shader"

    # The frozen profile deliberately formats grammar_modes as a multiline array.
    # Scope token checks to the geometric function instead of requiring an inline array.
    var geometric_start := profile.find("static func _geometric(seed_value: int) -> Dictionary:")
    var fractal_start := profile.find("static func _fractal(seed_value: int) -> Dictionary:")
    if geometric_start < 0 or fractal_start <= geometric_start:
        return "cannot locate geometric profile function boundaries"
    var geometric_profile := profile.substr(geometric_start, fractal_start - geometric_start)
    for token: String in [
        "var grammar_modes: Array[String] = [",
        "\"harmonic_membrane\"",
        "\"interference_plane\"",
        "\"parametric_ribbon\"",
        "\"lattice_wave\"",
        "\"orbital_wave\""
    ]:
        if not geometric_profile.contains(token): return "geometric profile block missing token: " + token

    for token: String in ['OS.get_environment("C11C_VISUAL_GRAMMAR")', '_variation["grammar_mode"] = index', '_variation["grammar_name"] = technical_id']:
        if not proto.contains(token): return "geometric prototype missing token: " + token
    for token: String in ['func set_style(', '_material.set_shader_parameter("grammar_mode", clampi(grammar_mode, 0, 4))', '_material.set_shader_parameter("wave_frequency", max(wave_frequency, 5.0))']:
        if not renderer.contains(token): return "geometric renderer missing token: " + token
    for token: String in ['uniform int grammar_mode = 0;', 'if (grammar_mode == 0)', 'return field_harmonic_membrane(q, local_phase, layer);']:
        if not shader.contains(token): return "geometric shader missing token: " + token
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
    if not is_finite(number) or number != floor(number) or number < float(minimum) or number > float(maximum): return false
    return true

func _fail(message: String) -> void:
    push_error("VISUAL LOOP GRAMMAR PARAMETER INSTANCE PROBE FAIL: " + message)
    print("C11-D VISUAL LOOP GRAMMAR PARAMETER INSTANCE PROBE FAIL | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
    quit(1)
