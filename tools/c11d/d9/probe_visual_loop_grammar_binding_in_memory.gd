extends SceneTree

## Read-only probe of frozen C11-C profile values and the source-pinned
## geometric grammar-index mapping. This script does not instantiate a renderer,
## shader/material, prototype scene, payload instance, or media output.

const C11CVariationProfileScript = preload("res://tools/prototypes/c11c_common/C11CVariationProfile.gd")
const PROFILE_SOURCE := "res://tools/prototypes/c11c_common/C11CVariationProfile.gd"
const PROTOTYPE_SOURCE := "res://tools/prototypes/c11c_geometric_waves_v1/GeometricWavesPrototype.gd"
const RENDERER_SOURCE := "res://tools/prototypes/c11c_geometric_waves_v1/GeometricWavesRenderer.gd"
const SHADER_SOURCE := "res://tools/prototypes/c11c_geometric_waves_v1/GeometricWaves.gdshader"
const GRAMMAR_IDS: Array[String] = ["harmonic_membrane", "interference_plane", "parametric_ribbon", "lattice_wave", "orbital_wave"]
const SELECTED_GRAMMAR := "harmonic_membrane"
const SELECTED_INDEX := 0
const SEEDS: Array[int] = [12345, 54321, 0, 2147483646]
const STYLE_KEYS: Array[String] = [
    "grammar_mode", "palette_mode", "morph", "wave_frequency", "line_width",
    "glow_strength", "polygon_sides", "wave_ratio", "shape_rotation", "layer_spread",
    "radial_wave_amplitude", "liss_x_frequency", "liss_y_frequency", "interference_scale",
    "hero_scale", "perspective_strength", "depth_strength", "secondary_phase", "color_phase", "stroke_scale"
]
# Input profile names are intentionally separate from renderer/shader output names.
# C11CVariationProfile emits `glow`; the renderer shader parameter is `glow_strength`.
const PROFILE_INPUT_KEYS: Array[String] = [
    "grammar_mode", "palette_mode", "morph", "wave_frequency", "line_width",
    "glow", "polygon_sides", "wave_ratio", "shape_rotation", "layer_spread",
    "radial_wave_amplitude", "liss_x_frequency", "liss_y_frequency", "interference_scale",
    "hero_scale", "perspective_strength", "depth_strength", "secondary_phase", "color_phase", "stroke_scale"
]

func _initialize() -> void:
    call_deferred("_run")

func _run() -> void:
    if not _source_checks_pass():
        _fail("Pinned prototype/renderer/shader source mapping tokens are missing or drifted.")
        return
    var grammar_index := GRAMMAR_IDS.find(SELECTED_GRAMMAR)
    if grammar_index != SELECTED_INDEX:
        _fail("Selected grammar index changed.")
        return
    var seed_cases: Array[Dictionary] = []
    var style_hashes: Array[String] = []
    for seed_value: int in SEEDS:
        var raw_first: Dictionary = C11CVariationProfileScript.build("geometric", seed_value)
        var raw_second: Dictionary = C11CVariationProfileScript.build("geometric", seed_value)
        if raw_first.is_empty() or raw_second.is_empty():
            _fail("C11-C geometric VariationProfile did not return a profile.")
            return
        var raw_grammar_before: String = str(raw_first.get("grammar_name", ""))
        if raw_grammar_before.is_empty() or raw_first != raw_second:
            _fail("C11-C profile did not repeat deterministically for one seed.")
            return
        var bound_first: Dictionary = raw_first.duplicate(true)
        var bound_second: Dictionary = raw_second.duplicate(true)
        # Mirrors the frozen prototype's explicit C11C_VISUAL_GRAMMAR override mapping.
        bound_first["grammar_mode"] = grammar_index
        bound_first["grammar_name"] = SELECTED_GRAMMAR
        bound_second["grammar_mode"] = grammar_index
        bound_second["grammar_name"] = SELECTED_GRAMMAR
        var style_first := _project_style_parameters(bound_first)
        var style_second := _project_style_parameters(bound_second)
        if style_first.size() != STYLE_KEYS.size() or style_second.size() != STYLE_KEYS.size():
            _fail("The 20 style parameters could not be projected from the C11-C profile.")
            return
        if str(bound_first.get("grammar_name", "")) != SELECTED_GRAMMAR or int(bound_first.get("grammar_mode", -1)) != SELECTED_INDEX:
            _fail("Selected grammar was not bound independently of the seed-derived profile grammar.")
            return
        var first_hash := _sha256(style_first)
        var second_hash := _sha256(style_second)
        if first_hash.is_empty() or first_hash != second_hash:
            _fail("Projected style values were not deterministic for the same seed.")
            return
        style_hashes.append(first_hash)
        seed_cases.append({
            "seed": seed_value,
            "seed_profile_grammar_before_override": raw_grammar_before,
            "bound_grammar_id": SELECTED_GRAMMAR,
            "bound_grammar_index": SELECTED_INDEX,
            "style_parameter_count": style_first.size(),
            "style_sha256": first_hash,
            "repeat_style_sha256": second_hash,
            "deterministic_repeat": true
        })
    var unique_style_hashes: Dictionary = {}
    for digest: String in style_hashes:
        unique_style_hashes[digest] = true
    if unique_style_hashes.size() < 2:
        _fail("Seed changes did not produce distinct projected visual style evidence.")
        return
    var report := {
        "schema": "C11D-VISUAL-LOOP-GRAMMAR-BINDING-PROBE-RECEIPT-V1",
        "schema_version": "1.0",
        "status": "READ_ONLY_IN_MEMORY_PROTOTYPE_GRAMMAR_PARAMETER_PROBE",
        "selection": {"content_type":"visual_loops", "family_id":"c11c_geometric_waves_v1", "internal_family":"geometric", "subtype_id":SELECTED_GRAMMAR},
        "mapping": {"environment_override":"C11C_VISUAL_GRAMMAR", "grammar_ids":GRAMMAR_IDS, "selected_grammar_id":SELECTED_GRAMMAR, "selected_grammar_index":SELECTED_INDEX, "selected_shader_branch":"field_harmonic_membrane", "style_parameter_count":STYLE_KEYS.size()},
        "seed_cases": seed_cases,
        "findings": {
            "prototype_override_source_pinned":true,
            "renderer_set_style_source_pinned":true,
            "shader_branch_source_pinned":true,
            "family_envelope_grammar_gap_remains":true,
            "seed_profile_changes_style_parameters":true,
            "selected_grammar_is_seed_independent":true,
            "exact_selector_payload_materialized":false
        },
        "execution_boundary": {
            "probe_mode":"GODOT_HEADLESS_PROFILE_AND_SOURCE_PROBE_ONLY",
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
    }
    print("C11D_GRAMMAR_PROBE_RECEIPT=" + JSON.stringify(report))
    print("C11-D VISUAL LOOP GRAMMAR BINDING PROBE PASS | seeds=4/4 | selected_grammar=harmonic_membrane@0 | style_parameters=20/20 | exact_selector_payload_materialized=false | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
    quit(0)

func _source_checks_pass() -> bool:
    var prototype := FileAccess.get_file_as_string(PROTOTYPE_SOURCE)
    var renderer := FileAccess.get_file_as_string(RENDERER_SOURCE)
    var shader := FileAccess.get_file_as_string(SHADER_SOURCE)
    var profile := FileAccess.get_file_as_string(PROFILE_SOURCE)
    var prototype_tokens := [
        "C11C_VISUAL_GRAMMAR", "const GRAMMAR_IDS", "_variation[\"grammar_mode\"] = index",
        "_variation[\"grammar_name\"] = technical_id"
    ]
    var renderer_tokens := [
        "func set_style(", "_material.set_shader_parameter(\"grammar_mode\", clampi(grammar_mode, 0, 4))",
        "_material.set_shader_parameter(\"wave_frequency\", max(wave_frequency, 5.0))"
    ]
    for token: String in prototype_tokens:
        if not prototype.contains(token):
            return false
    for token: String in renderer_tokens:
        if not renderer.contains(token):
            return false
    if not shader.contains("uniform int grammar_mode = 0;") or not shader.contains("if (grammar_mode == 0)") or not shader.contains("return field_harmonic_membrane(q, local_phase, layer);"):
        return false
    if not profile.contains('"harmonic_membrane"') or not profile.contains('"orbital_wave"'):
        return false
    return true

func _project_style_parameters(value: Dictionary) -> Dictionary:
    for key: String in PROFILE_INPUT_KEYS:
        if not value.has(key):
            return {}
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
        var keys: Array = value.keys()
        keys.sort()
        var result: Dictionary = {}
        for key in keys:
            result[str(key)] = _stable_value(value[key])
        return result
    if value is Array:
        var items: Array = []
        for item: Variant in value:
            items.append(_stable_value(item))
        return items
    return value

func _sha256(value: Variant) -> String:
    var context := HashingContext.new()
    if context.start(HashingContext.HASH_SHA256) != OK:
        return ""
    context.update(JSON.stringify(_stable_value(value)).to_utf8_buffer())
    return context.finish().hex_encode()

func _fail(message: String) -> void:
    push_error("VISUAL LOOP GRAMMAR BINDING PROBE FAIL: " + message)
    print("C11-D VISUAL LOOP GRAMMAR BINDING PROBE FAIL | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
    quit(1)
