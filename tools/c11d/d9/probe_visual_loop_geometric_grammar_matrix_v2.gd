extends SceneTree

## D-owned read-only probe for all five frozen C11-C geometric grammar parameter
## projections. It binds grammar IDs only into local dictionaries; it does not
## instantiate the C11-C renderer/shader or emit a renderer-native input.
const Profile = preload("res://tools/prototypes/c11c_common/C11CVariationProfile.gd")
const PROFILE_SOURCE := "res://tools/prototypes/c11c_common/C11CVariationProfile.gd"
const PROTOTYPE_SOURCE := "res://tools/prototypes/c11c_geometric_waves_v1/GeometricWavesPrototype.gd"
const RENDERER_SOURCE := "res://tools/prototypes/c11c_geometric_waves_v1/GeometricWavesRenderer.gd"
const SHADER_SOURCE := "res://tools/prototypes/c11c_geometric_waves_v1/GeometricWaves.gdshader"
const REGISTRY_SOURCE := "res://c11c-suite/c11c-producer/producer_schema.json"
const MANIFEST_SHA := "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
const INPUT_SCHEMA := "C11-D-D9-VISUAL-LOOP-GEOMETRIC-GRAMMAR-MATRIX-INPUT-V2"
const PROBE_SCHEMA := "C11-D-D9-VISUAL-LOOP-GEOMETRIC-GRAMMAR-MATRIX-PROBE-V2"
const PREFIX := "C11D_VISUAL_LOOP_GEOMETRIC_GRAMMAR_MATRIX_PROBE="
const GRAMMAR_MATRIX: Array[Dictionary] = [
    {"grammar_id":"harmonic_membrane", "grammar_index":0, "shader_branch":"field_harmonic_membrane"},
    {"grammar_id":"interference_plane", "grammar_index":1, "shader_branch":"field_interference_plane"},
    {"grammar_id":"parametric_ribbon", "grammar_index":2, "shader_branch":"field_parametric_ribbon"},
    {"grammar_id":"lattice_wave", "grammar_index":3, "shader_branch":"field_lattice_wave"},
    {"grammar_id":"orbital_wave", "grammar_index":4, "shader_branch":"field_orbital_wave"}
]
const SEEDS: Array[int] = [1, 12345, 54321, 2147483646]
const STYLE_KEYS: Array[String] = [
    "grammar_mode", "palette_mode", "morph", "wave_frequency", "line_width",
    "glow_strength", "polygon_sides", "wave_ratio", "shape_rotation", "layer_spread",
    "radial_wave_amplitude", "liss_x_frequency", "liss_y_frequency", "interference_scale",
    "hero_scale", "perspective_strength", "depth_strength", "secondary_phase", "color_phase", "stroke_scale"
]
const PROFILE_INPUT_KEYS: Array[String] = [
    "grammar_mode", "palette_mode", "morph", "wave_frequency", "line_width",
    "glow", "polygon_sides", "wave_ratio", "shape_rotation", "layer_spread",
    "radial_wave_amplitude", "liss_x_frequency", "liss_y_frequency", "interference_scale",
    "hero_scale", "perspective_strength", "depth_strength", "secondary_phase", "color_phase", "stroke_scale"
]

func _initialize() -> void:
    call_deferred("_run")

func _run() -> void:
    var input_value := _decode_input()
    if input_value.is_empty():
        _fail("missing or invalid base64 JSON input")
        return
    var input_error := _validate_input(input_value)
    if not input_error.is_empty():
        _fail(input_error)
        return
    var source_error := _source_check_error()
    if not source_error.is_empty():
        _fail(source_error)
        return

    var cases: Array[Dictionary] = []
    var per_grammar_hashes: Dictionary = {}
    for grammar_row: Dictionary in GRAMMAR_MATRIX:
        var grammar_id := str(grammar_row["grammar_id"])
        var grammar_index := int(grammar_row["grammar_index"])
        for seed_value: int in SEEDS:
            var profile_a: Dictionary = Profile.build("geometric", seed_value)
            var profile_b: Dictionary = Profile.build("geometric", seed_value)
            if profile_a.is_empty() or profile_b.is_empty() or profile_a != profile_b:
                _fail("C11-C profile did not repeat deterministically for %s seed %s" % [grammar_id, seed_value])
                return
            var seed_profile_grammar := str(profile_a.get("grammar_name", ""))
            if seed_profile_grammar.is_empty():
                _fail("C11-C geometric profile omitted its seed-derived grammar identity")
                return
            var bound_a: Dictionary = profile_a.duplicate(true)
            var bound_b: Dictionary = profile_b.duplicate(true)
            # Explicit selector mapping mirrors the audited C11-C prototype environment override.
            # These assignments touch only local copies owned by this read-only probe.
            bound_a["grammar_mode"] = grammar_index
            bound_a["grammar_name"] = grammar_id
            bound_b["grammar_mode"] = grammar_index
            bound_b["grammar_name"] = grammar_id
            var style_a := _project_style_parameters(bound_a)
            var style_b := _project_style_parameters(bound_b)
            if style_a.size() != STYLE_KEYS.size() or style_b.size() != STYLE_KEYS.size() or style_a != style_b:
                _fail("20-key style projection incomplete or non-deterministic for %s seed %s" % [grammar_id, seed_value])
                return
            if int(style_a.get("grammar_mode", -1)) != grammar_index:
                _fail("Grammar index was not bound exactly for %s" % grammar_id)
                return
            if not bound_a.has("grammar_name") or str(bound_a["grammar_name"]) != grammar_id:
                _fail("Grammar identity was not bound exactly for %s" % grammar_id)
                return
            var style_sha := _sha256(style_a)
            var repeat_style_sha := _sha256(style_b)
            var instance_core := {
                "schema":"C11-D-D9-VISUAL-LOOP-GEOMETRIC-GRAMMAR-PARAMETER-INSTANCE-V2",
                "schema_version":"2.0",
                "selection":{"content_type":"visual_loops", "family_id":"c11c_geometric_waves_v1", "subtype_id":grammar_id, "variant_id":null},
                "grammar_id":grammar_id,
                "grammar_index":grammar_index,
                "shader_branch":str(grammar_row["shader_branch"]),
                "shader_uniform":"grammar_mode",
                "gameplay_seed":seed_value,
                "style_parameter_count":STYLE_KEYS.size(),
                "style_parameters":style_a
            }
            var instance_sha := _sha256(instance_core)
            var repeat_instance_sha := _sha256({
                "schema":"C11-D-D9-VISUAL-LOOP-GEOMETRIC-GRAMMAR-PARAMETER-INSTANCE-V2",
                "schema_version":"2.0",
                "selection":{"content_type":"visual_loops", "family_id":"c11c_geometric_waves_v1", "subtype_id":grammar_id, "variant_id":null},
                "grammar_id":grammar_id,
                "grammar_index":grammar_index,
                "shader_branch":str(grammar_row["shader_branch"]),
                "shader_uniform":"grammar_mode",
                "gameplay_seed":seed_value,
                "style_parameter_count":STYLE_KEYS.size(),
                "style_parameters":style_b
            })
            if style_sha.is_empty() or style_sha != repeat_style_sha or instance_sha.is_empty() or instance_sha != repeat_instance_sha:
                _fail("Style or instance digest repeat mismatch for %s seed %s" % [grammar_id, seed_value])
                return
            var hash_key := grammar_id
            if not per_grammar_hashes.has(hash_key):
                per_grammar_hashes[hash_key] = []
            per_grammar_hashes[hash_key].append(style_sha)
            cases.append({
                "grammar_id":grammar_id,
                "grammar_index":grammar_index,
                "shader_branch":str(grammar_row["shader_branch"]),
                "gameplay_seed":seed_value,
                "seed_profile_grammar_before_override":seed_profile_grammar,
                "style_parameter_count":STYLE_KEYS.size(),
                "style_parameters":style_a,
                "repeat_style_parameters":style_b,
                "style_sha256":style_sha,
                "repeat_style_sha256":repeat_style_sha,
                "parameter_instance_sha256":instance_sha,
                "repeat_parameter_instance_sha256":repeat_instance_sha,
                "deterministic_repeat":true
            })

    for grammar_row: Dictionary in GRAMMAR_MATRIX:
        var grammar_id := str(grammar_row["grammar_id"])
        var hashes: Array = per_grammar_hashes.get(grammar_id, [])
        var unique: Dictionary = {}
        for digest: String in hashes:
            unique[digest] = true
        if hashes.size() != SEEDS.size() or unique.size() < 2:
            _fail("Gameplay-seed variation was not demonstrated for %s" % grammar_id)
            return

    var report := {
        "schema":PROBE_SCHEMA,
        "schema_version":"2.0",
        "status":"PREPARATION_ONLY_GEOMETRIC_GRAMMAR_PARAMETER_MATRIX_NOT_CANONICAL_REQUEST_BINDING_NOT_RENDERER_INPUT",
        "contract_sha256":str(input_value["contract_sha256"]),
        "frozen_c11c_manifest_sha256":MANIFEST_SHA,
        "selection_family":{"content_type":"visual_loops", "family_id":"c11c_geometric_waves_v1"},
        "grammar_count":GRAMMAR_MATRIX.size(),
        "seed_values":SEEDS,
        "cases":cases,
        "checks":{"case_count":cases.size(), "expected_case_count":GRAMMAR_MATRIX.size() * SEEDS.size(), "all_five_grammar_indices_bound":true, "style_parameters_per_case":20, "same_seed_repeat_deterministic":true, "gameplay_seed_variation_per_grammar":true, "profile_copy_only":true, "source_checks_passed":true},
        "execution_boundary":{"mode":"GODOT_HEADLESS_IN_MEMORY_GEOMETRIC_GRAMMAR_PARAMETER_MATRIX_ONLY", "canonical_request_chain_admitted":false, "canonical_selector_matrix_modified":false, "renderer_native_input_emitted":false, "renderer_instance_created":false, "renderer_dispatch_invoked":false, "shader_executed":false, "payload_files_written":false, "receipt_files_written":false, "media_created":false, "c11c_source_mutation":false, "renderer":"OFF", "d4_8":"BLOCKED", "release_authority":"NONE", "d9_14":"BLOCKED_AS_REQUIRED", "d9_16":"BLOCKED_AS_REQUIRED", "d9_17":"BLOCKED_NO_GO", "d10":"BLOCKED"}
    }
    print(PREFIX + JSON.stringify(_stable_value(report)))
    print("C11-D VISUAL LOOP GEOMETRIC GRAMMAR MATRIX V2 PASS | grammars=5/5 | seed_cases=20/20 | style_parameters=20/20_per_case | deterministic_repeats=20/20 | canonical_request_admission=false | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
    quit(0)

func _decode_input() -> Dictionary:
    var args := OS.get_cmdline_user_args()
    if args.size() != 1:
        return {}
    var parsed: Variant = JSON.parse_string(Marshalls.base64_to_utf8(args[0]))
    if not (parsed is Dictionary):
        return {}
    return parsed

func _validate_input(value: Dictionary) -> String:
    var keys := ["schema", "schema_version", "contract_sha256", "frozen_c11c_manifest_sha256", "grammar_matrix", "seeds"]
    var actual: Array = value.keys(); actual.sort(); keys.sort()
    if actual != keys: return "Input keys are not exact"
    if str(value.get("schema", "")) != INPUT_SCHEMA or str(value.get("schema_version", "")) != "2.0": return "Input schema identity/version mismatch"
    if str(value.get("frozen_c11c_manifest_sha256", "")) != MANIFEST_SHA: return "Frozen C11-C manifest mismatch"
    if not _is_sha256(str(value.get("contract_sha256", ""))): return "Contract SHA-256 malformed"
    var rows: Variant = value.get("grammar_matrix", null)
    if not (rows is Array) or rows.size() != GRAMMAR_MATRIX.size(): return "Grammar matrix must contain exactly five entries"
    for index in range(GRAMMAR_MATRIX.size()):
        var row_value: Variant = rows[index]
        if not (row_value is Dictionary):
            return "Grammar matrix row is not an object at index %s" % index
        var row: Dictionary = row_value
        var expected_row: Dictionary = GRAMMAR_MATRIX[index]
        var row_keys: Array = row.keys()
        var expected_row_keys: Array = expected_row.keys()
        row_keys.sort()
        expected_row_keys.sort()
        if row_keys != expected_row_keys:
            return "Grammar matrix row has unexpected keys at index %s" % index

        var grammar_id_value: Variant = row.get("grammar_id", null)
        if typeof(grammar_id_value) != TYPE_STRING or str(grammar_id_value) != str(expected_row["grammar_id"]):
            return "Grammar matrix grammar_id mismatch at index %s" % index

        # JSON defines a single number type, and Godot may deserialize a whole-valued
        # JSON number as float. Compare the numeric value explicitly instead of using
        # recursive Dictionary equality, while rejecting non-numeric/non-finite values.
        var grammar_index_value: Variant = row.get("grammar_index", null)
        if typeof(grammar_index_value) != TYPE_INT and typeof(grammar_index_value) != TYPE_FLOAT:
            return "Grammar matrix grammar_index is not numeric at index %s" % index
        var numeric_index := float(grammar_index_value)
        if not is_finite(numeric_index) or numeric_index != float(expected_row["grammar_index"]):
            return "Grammar matrix grammar_index mismatch at index %s" % index

        var shader_branch_value: Variant = row.get("shader_branch", null)
        if typeof(shader_branch_value) != TYPE_STRING or str(shader_branch_value) != str(expected_row["shader_branch"]):
            return "Grammar matrix shader_branch mismatch at index %s" % index
    var seeds: Variant = value.get("seeds", null)
    if not (seeds is Array) or seeds.size() != SEEDS.size():
        return "Seed matrix must contain exactly four pinned values"
    for seed_index in range(SEEDS.size()):
        var seed_value: Variant = seeds[seed_index]
        if typeof(seed_value) != TYPE_INT and typeof(seed_value) != TYPE_FLOAT:
            return "Seed matrix value is not numeric at index %s" % seed_index
        # JSON has one number type; Godot may decode integral values as floats.
        # Compare finite numeric values explicitly and retain the exact four pins.
        var numeric_seed := float(seed_value)
        if not is_finite(numeric_seed) or numeric_seed != float(SEEDS[seed_index]):
            return "Seed matrix mismatch at index %s" % seed_index
    return ""

func _source_check_error() -> String:
    var profile := FileAccess.get_file_as_string(PROFILE_SOURCE)
    var prototype := FileAccess.get_file_as_string(PROTOTYPE_SOURCE)
    var renderer := FileAccess.get_file_as_string(RENDERER_SOURCE)
    var shader := FileAccess.get_file_as_string(SHADER_SOURCE)
    var registry_text := FileAccess.get_file_as_string(REGISTRY_SOURCE)
    if profile.is_empty() or prototype.is_empty() or renderer.is_empty() or shader.is_empty() or registry_text.is_empty():
        return "One or more pinned geometric grammar sources could not be read"
    var geometric_start := profile.find("static func _geometric(seed_value: int) -> Dictionary:")
    var fractal_start := profile.find("static func _fractal(seed_value: int) -> Dictionary:")
    if geometric_start < 0 or fractal_start <= geometric_start: return "Cannot isolate frozen geometric profile block"
    var geometric_profile := profile.substr(geometric_start, fractal_start - geometric_start)
    for row: Dictionary in GRAMMAR_MATRIX:
        var grammar_id := str(row["grammar_id"])
        if not geometric_profile.contains('"' + grammar_id + '"'): return "Geometric profile is missing grammar " + grammar_id
        if not registry_text.contains('"' + grammar_id + '"'): return "Producer registry is missing grammar " + grammar_id
    for token: String in ['OS.get_environment("C11C_VISUAL_GRAMMAR")', '_variation["grammar_mode"] = index', '_variation["grammar_name"] = technical_id']:
        if not prototype.contains(token): return "Prototype grammar override mapping drifted: " + token
    if not renderer.contains('_material.set_shader_parameter("grammar_mode", clampi(grammar_mode, 0, 4))'):
        return "Renderer does not preserve five-value grammar_mode bounds"
    for row: Dictionary in GRAMMAR_MATRIX:
        var branch := str(row["shader_branch"])
        if not shader.contains(branch): return "Shader branch is missing: " + branch
    for token: String in ['if (grammar_mode == 0)', 'if (grammar_mode == 1)', 'if (grammar_mode == 2)', 'if (grammar_mode == 3)', 'return field_orbital_wave(q, local_phase, layer);']:
        if not shader.contains(token): return "Shader mode-to-branch mapping is incomplete: " + token
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
    var context := HashingContext.new()
    if context.start(HashingContext.HASH_SHA256) != OK: return ""
    context.update(JSON.stringify(_stable_value(value)).to_utf8_buffer())
    return context.finish().hex_encode()

func _is_sha256(value: String) -> bool:
    if value.length() != 64:
        return false
    for ch in value:
        if not ((ch >= "0" and ch <= "9") or (ch >= "a" and ch <= "f")):
            return false
    return true

func _fail(message: String) -> void:
    push_error(message)
    print("C11-D VISUAL LOOP GEOMETRIC GRAMMAR MATRIX V2 FAIL | " + message + " | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
    quit(2)
