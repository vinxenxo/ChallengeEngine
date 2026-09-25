extends SceneTree

const VariationProfileClass = preload("res://tools/prototypes/c11c_common/C11CVariationProfile.gd")

func _init() -> void:
    var args: PackedStringArray = OS.get_cmdline_user_args()
    if args.is_empty():
        _fail("Missing request JSON path", "")
        return
    var request_path: String = str(args[0])
    var file: FileAccess = FileAccess.open(request_path, FileAccess.READ)
    if file == null:
        _fail("Cannot open request JSON", request_path)
        return
    var parsed: Variant = JSON.parse_string(file.get_as_text())
    file.close()
    if not (parsed is Dictionary):
        _fail("Invalid request JSON", request_path)
        return
    var request: Dictionary = parsed
    var family: String = str(request.get("family", ""))
    var target_value: Variant = request.get("target", {})
    var target: Dictionary = target_value if target_value is Dictionary else {}
    var count: int = maxi(int(request.get("count", 1)), 1)
    var max_candidates: int = maxi(int(request.get("max_candidates", 300000)), count)
    var excluded: Dictionary = {}
    var excluded_value: Variant = request.get("excluded_seeds", [])
    if excluded_value is Array:
        for raw_seed: Variant in excluded_value:
            excluded[int(raw_seed)] = true
    var results: Array = []
    var seed: int = int(request.get("start_seed", 1000000))
    var step: int = int(request.get("step", 7919))
    var attempts: int = 0
    while attempts < max_candidates and results.size() < count:
        seed = _next_seed(seed, step)
        attempts += 1
        if excluded.has(seed):
            continue
        var profile: Dictionary = VariationProfileClass.build(family, seed)
        var scored: Dictionary = _score(profile, target)
        if not bool(scored.get("eligible", false)):
            continue
        results.append({"seed": seed, "score": float(scored.get("score", 0.0)), "profile": profile})
    results.sort_custom(func(a: Dictionary, b: Dictionary) -> bool:
        return float(a.get("score", 0.0)) < float(b.get("score", 0.0))
    )
    var response_path: String = request_path.get_base_dir().path_join("response.json")
    if results.size() < count:
        _write_response(response_path, {"ok": false, "error": "No hay suficientes seeds compatibles. Reduce los valores fijados o la cantidad."})
        quit(1)
        return
    _write_response(response_path, {"ok": true, "family": family, "attempts": attempts, "results": results.slice(0, count)})
    quit(0)

func _next_seed(value: int, step: int) -> int:
    var x: int = (value + step) & 0x7fffffff
    if x < 1000000:
        x += 1000000
    if x >= 2147483646:
        x = 1000000 + (x % 1147483646)
    return x

func _score(profile: Dictionary, target: Dictionary) -> Dictionary:
    var exact_strings: Array[String] = ["grammar_name", "palette_name"]
    var exact_numeric: Array[String] = ["loop_cycles", "polygon_sides", "liss_x_frequency", "liss_y_frequency", "zoom_cycles", "zoom_path", "symmetry_order", "gear_inner", "gear_outer", "mechanical_rate", "phase_rate"]
    var score: float = 0.0
    for key in exact_strings:
        if target.has(key) and str(profile.get(key, "")) != str(target[key]):
            return {"eligible": false, "score": 1.0e30}
    for key in exact_numeric:
        if target.has(key) and abs(float(profile.get(key, 0.0)) - float(target[key])) > 0.000001:
            return {"eligible": false, "score": 1.0e30}
    for raw_key: Variant in target.keys():
        var key: String = str(raw_key)
        if exact_strings.has(key) or exact_numeric.has(key) or not profile.has(key):
            continue
        var t: float = float(target[key])
        var p: float = float(profile[key])
        var bounds: Array = _range_for(key)
        var low: float = float(bounds[0])
        var high: float = float(bounds[1])
        var denominator: float = max(high - low, 0.000001)
        var normalized: float = (p - t) / denominator
        score += normalized * normalized
    return {"eligible": true, "score": score}

func _range_for(key: String) -> Array:
    match key:
        "wave_frequency": return [12.0, 28.0]
        "morph": return [0.18, 0.92]
        "line_width": return [0.0048, 0.0094]
        "glow": return [0.0, 1.0]
        "wave_ratio": return [0.62, 1.02]
        "shape_rotation": return [-0.42, 0.42]
        "layer_spread": return [0.0, 1.0]
        "radial_wave_amplitude": return [0.0, 1.0]
        "interference_scale": return [0.74, 1.42]
        "hero_scale": return [0.80, 1.03]
        "perspective_strength": return [0.35, 1.02]
        "depth_strength": return [0.42, 0.94]
        "secondary_phase": return [-1.10, 1.10]
        "color_phase": return [-3.1415927, 3.1415927]
        "stroke_scale": return [0.78, 1.28]
        "zoom_strength": return [0.10, 0.42]
        "warp_strength": return [0.012, 0.058]
        "bloom_strength": return [0.40, 0.82]
        "layer_softness": return [0.48, 1.04]
        "julia_x_bias": return [-0.060, 0.060]
        "julia_y_bias": return [-0.075, 0.075]
        "warp_frequency": return [2.0, 5.8]
        "breath_strength": return [0.035, 0.105]
        "branch_density": return [0.76, 1.32]
        "detail_scale": return [0.86, 1.34]
        "spiral_amount": return [0.45, 1.45]
        "color_diversity": return [0.82, 1.0]
        "ring_bias": return [0.30, 0.82]
        "ring_scale": return [0.90, 1.08]
        "core_scale": return [0.78, 1.18]
        "tick_density": return [0.82, 1.34]
        "macro_scale": return [0.86, 1.04]
        "node_density": return [0.72, 1.28]
        "fold_depth": return [0.78, 1.22]
        "particle_count": return [104.0, 170.0]
        "attractor_a_x": return [-0.22, -0.04]
        "attractor_a_y": return [-0.16, 0.09]
        "attractor_b_x": return [0.04, 0.22]
        "attractor_b_y": return [-0.05, 0.17]
        "swirl_bias": return [0.62, 1.48]
        "particle_spread": return [0.78, 1.18]
        "turbulence": return [0.012, 0.046]
        "attractor_strength": return [0.72, 1.44]
        "particle_size_scale": return [0.74, 1.30]
        "collision_strength": return [0.72, 1.40]
        "density_bias": return [0.86, 1.16]
        "trace_count": return [50.0, 88.0]
        "curvature": return [0.52, 1.16]
        "field_rotation": return [-0.42, 0.42]
        "storm_offset_x": return [-0.16, 0.16]
        "storm_offset_y": return [-0.12, 0.12]
        "pulse_speed": return [0.84, 1.34]
        "field_twist": return [0.62, 1.42]
        "pulse_width": return [0.62, 1.34]
        "storm_scale": return [0.74, 1.18]
        "lens_strength": return [0.42, 0.92]
        "basin_depth": return [0.45, 1.05]
        "pole_separation": return [0.16, 0.34]
        "quadrupole_skew": return [0.78, 1.28]
        _: return [0.0, 1.0]

func _write_response(path: String, data: Dictionary) -> void:
    var file: FileAccess = FileAccess.open(path, FileAccess.WRITE)
    if file != null:
        file.store_string(JSON.stringify(data))
        file.close()

func _fail(message: String, request_path: String) -> void:
    if request_path.is_empty():
        quit(1)
        return
    var response_path: String = request_path.get_base_dir().path_join("response.json")
    _write_response(response_path, {"ok": false, "error": message})
    quit(1)
