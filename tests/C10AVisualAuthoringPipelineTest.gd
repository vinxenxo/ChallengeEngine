extends SceneTree

## C10-A.1 — 9/9 production visual authoring matrix.
## Uses real production identifiers already present in the repository.
## Does not touch C6-F0.8 runtime, generators or RNG implementation.

const Request = preload("res://core/authoring/VisualAuthoringRequest.gd")
const Context = preload("res://core/authoring/VisualAuthoringAssemblyContext.gd")
const Generator = preload("res://core/authoring/VisualAuthoringGenerator.gd")
const PolicyRegistry = preload("res://core/authoring/VisualAuthoringPolicyRegistry.gd")
const ContentRuntimeRegistry = preload("res://core/runtime/ContentRuntimeRegistry.gd")

const LOOP_SUBTYPES := ["fractal", "vector_field", "particle_flow", "kaleidoscope", "geometric"]
const DRILL_SUBTYPES := ["tracking", "pursuit", "saccade", "peripheral_scan"]

var failures: Array[String] = []

func _init() -> void:
    print("[TEST] Running C10AVisualAuthoringPipelineTest...")
    _test_full_9_of_9_matrix()
    _test_policy_baseline_tier_2()
    _test_rng_level_custom_parameters_fail_closed()
    _test_seed_is_external_and_changes_only_envelope_seed()
    _conclude()

func _assert(condition: bool, message: String) -> void:
    if not condition:
        failures.append(message)

func _context(seed_value: int, content_id: String) -> Context:
    return Context.new(
        seed_value,
        "2.0",
        content_id,
        "1.0.0",
        "4.7.1",
        {
            "profile_id": "social_default_v1",
            "coordinate_space": "2d"
        },
        {
            "family_id": "fam_001"
        },
        {
            "profile_id": "default_procedural_music",
            "enabled": false
        },
        {
            "author": "c10_visual_authoring",
            "timestamp_ms": 0
        }
    )

func _request(domain_family: String, subtype: String, tier: int = 2, custom: Dictionary = {}) -> Request:
    return Request.new(domain_family, subtype, 2.0, 30, tier, custom)

func _generate(domain_family: String, subtype: String, seed_value: int = 12345, tier: int = 2, custom: Dictionary = {}) -> Dictionary:
    var req := _request(domain_family, subtype, tier, custom)
    var content_id := "C10A1_%s_%s" % [domain_family.to_upper(), subtype.to_upper()]
    return Generator.generate(req, _context(seed_value, content_id))

func _test_full_9_of_9_matrix() -> void:
    var passed := 0
    var runtime_registry = ContentRuntimeRegistry.create_default()

    for subtype in LOOP_SUBTYPES:
        var result := _generate("visual_loop", subtype)
        _assert(bool(result.get("success", false)), "visual_loop/%s authoring failed: %s" % [subtype, str(result.get("errors", []))])
        if not bool(result.get("success", false)):
            continue

        var definition: Dictionary = result.get("content", {})
        _assert(definition.get("kind", "") == "visual_loop", "visual_loop/%s kind mismatch" % subtype)
        _assert(definition.get("subtype", "") == subtype, "visual_loop/%s subtype mismatch" % subtype)
        _assert(definition.get("presentation", {}).get("profile_id", "") == "social_default_v1", "visual_loop/%s presentation ID mismatch" % subtype)
        _assert(definition.get("assets", {}).get("family_id", "") == "fam_001", "visual_loop/%s asset family ID mismatch" % subtype)
        _assert(definition.get("audio", {}).get("profile_id", "") == "default_procedural_music", "visual_loop/%s audio profile ID mismatch" % subtype)
        _assert(int(definition.get("payload", {}).get("frame_count", -1)) == 60, "visual_loop/%s frame_count mismatch" % subtype)
        _assert(definition.get("payload", {}).get("visual_parameters", {}).get("generator", "") == subtype, "visual_loop/%s generator mismatch" % subtype)
        _assert(definition.get("payload", {}).get("visual_parameters", {}).get("layers", []).size() == 1, "visual_loop/%s must emit one layer" % subtype)

        var resolution: Dictionary = runtime_registry.resolve(definition)
        _assert(bool(resolution.get("success", false)), "visual_loop/%s failed ContentRuntimeRegistry resolution: %s" % [subtype, str(resolution.get("error", ""))])
        if bool(resolution.get("success", false)):
            var runtime = resolution.get("runtime")
            _assert(runtime != null, "visual_loop/%s runtime instance missing" % subtype)
            if runtime != null:
                _assert(runtime.is_initialized(), "visual_loop/%s runtime not initialized" % subtype)
        passed += 1

    for subtype in DRILL_SUBTYPES:
        var result := _generate("visual_drill", subtype)
        _assert(bool(result.get("success", false)), "visual_drill/%s authoring failed: %s" % [subtype, str(result.get("errors", []))])
        if not bool(result.get("success", false)):
            continue

        var definition: Dictionary = result.get("content", {})
        _assert(definition.get("kind", "") == "visual_drill", "visual_drill/%s kind mismatch" % subtype)
        _assert(definition.get("subtype", "") == subtype, "visual_drill/%s subtype mismatch" % subtype)
        _assert(definition.get("presentation", {}).get("profile_id", "") == "social_default_v1", "visual_drill/%s presentation ID mismatch" % subtype)
        _assert(definition.get("assets", {}).get("family_id", "") == "fam_001", "visual_drill/%s asset family ID mismatch" % subtype)
        _assert(definition.get("audio", {}).get("profile_id", "") == "default_procedural_music", "visual_drill/%s audio profile ID mismatch" % subtype)
        _assert(int(definition.get("payload", {}).get("frame_count", -1)) == 60, "visual_drill/%s frame_count mismatch" % subtype)
        _assert(definition.get("payload", {}).get("exercise_parameters", {}).get("difficulty_tier", -1) == 2, "visual_drill/%s difficulty tier mismatch" % subtype)
        _assert(definition.get("payload", {}).get("exercise_parameters", {}).get("generator", "") == subtype, "visual_drill/%s generator mismatch" % subtype)
        _assert(definition.get("payload", {}).get("task", {}).get("type", "") == subtype, "visual_drill/%s task type mismatch" % subtype)

        var resolution: Dictionary = runtime_registry.resolve(definition)
        _assert(bool(resolution.get("success", false)), "visual_drill/%s failed ContentRuntimeRegistry resolution: %s" % [subtype, str(resolution.get("error", ""))])
        if bool(resolution.get("success", false)):
            var runtime = resolution.get("runtime")
            _assert(runtime != null, "visual_drill/%s runtime instance missing" % subtype)
            if runtime != null:
                _assert(runtime.is_initialized(), "visual_drill/%s runtime not initialized" % subtype)
        passed += 1

    print("[C10A1] Matrix candidates resolved: %d/9" % passed)
    _assert(passed == 9, "C10-A.1 matrix must resolve exactly 9/9 candidates")

func _test_policy_baseline_tier_2() -> void:
    for subtype in LOOP_SUBTYPES:
        var policy: Dictionary = PolicyRegistry.get_policy("visual_loop", subtype)
        _assert(not policy.is_empty(), "Missing production policy for visual_loop/%s" % subtype)
        if not policy.is_empty():
            _assert(int(policy.get("canonical_baseline_tier", -1)) == 2, "visual_loop/%s baseline tier must be 2" % subtype)
            _assert(float(policy.get("tiers", {}).get("2", {}).get("speed", -1.0)) == 1.0, "visual_loop/%s tier2 speed must equal canonical baseline" % subtype)
            _assert(int(policy.get("tiers", {}).get("2", {}).get("complexity", -1)) == 2, "visual_loop/%s tier2 complexity must equal canonical baseline" % subtype)

    for subtype in DRILL_SUBTYPES:
        var policy: Dictionary = PolicyRegistry.get_policy("visual_drill", subtype)
        _assert(not policy.is_empty(), "Missing production policy for visual_drill/%s" % subtype)
        if not policy.is_empty():
            _assert(int(policy.get("canonical_baseline_tier", -1)) == 2, "visual_drill/%s baseline tier must be 2" % subtype)
            _assert(float(policy.get("tiers", {}).get("2", {}).get("speed_multiplier", -1.0)) == 1.0, "visual_drill/%s tier2 speed multiplier must equal canonical baseline" % subtype)
            _assert(str(policy.get("base_parameters", {}).get("task", {}).get("type", "")) == subtype, "visual_drill/%s policy task type mismatch" % subtype)

func _test_rng_level_custom_parameters_fail_closed() -> void:
    var forbidden := {
        "fractal": "palette_variant",
        "vector_field": "turbulence_variant",
        "particle_flow": "emission_variant",
        "kaleidoscope": "symmetry_variant",
        "geometric": "shape_variant"
    }
    for subtype in LOOP_SUBTYPES:
        var bad := {str(forbidden[subtype]): 0.5}
        var result := _generate("visual_loop", subtype, 12345, 2, bad)
        _assert(not bool(result.get("success", false)), "visual_loop/%s accepted RNG-level custom parameter" % subtype)

    var drill_forbidden := {
        "tracking": "tracking_variant",
        "pursuit": "pursuit_variant",
        "saccade": "saccade_variant",
        "peripheral_scan": "pattern_variant"
    }
    for subtype in DRILL_SUBTYPES:
        var bad := {str(drill_forbidden[subtype]): 0.5}
        var result := _generate("visual_drill", subtype, 12345, 2, bad)
        _assert(not bool(result.get("success", false)), "visual_drill/%s accepted RNG-level custom parameter" % subtype)

func _test_seed_is_external_and_changes_only_envelope_seed() -> void:
    var request := _request("visual_loop", "fractal", 2, {})
    _assert(not request.to_dictionary().has("seed"), "VisualAuthoringRequest must not own seed")

    var a := Generator.generate(request, _context(12345, "C10A1_VISUAL_LOOP_FRACTAL"))
    var b := Generator.generate(request, _context(12345, "C10A1_VISUAL_LOOP_FRACTAL"))
    var c := Generator.generate(request, _context(54321, "C10A1_VISUAL_LOOP_FRACTAL"))

    _assert(bool(a.get("success", false)) and bool(b.get("success", false)) and bool(c.get("success", false)), "Seed externality test could not generate all candidates")
    if bool(a.get("success", false)) and bool(b.get("success", false)) and bool(c.get("success", false)):
        var da: Dictionary = a.get("content", {})
        var db: Dictionary = b.get("content", {})
        var dc: Dictionary = c.get("content", {})
        _assert(da == db, "Same external seed must yield identical authoring envelope")
        _assert(int(da.get("seed", -1)) == 12345 and int(db.get("seed", -1)) == 12345, "Seed 12345 must be injected externally")
        _assert(int(dc.get("seed", -1)) == 54321, "Seed 54321 must be injected externally")
        var da_without_seed := da.duplicate(true)
        var dc_without_seed := dc.duplicate(true)
        da_without_seed.erase("seed")
        dc_without_seed.erase("seed")
        _assert(da_without_seed == dc_without_seed, "Changing seed must not alter product-authoring parameters")

func _conclude() -> void:
    if failures.is_empty():
        print("[C10A_VISUAL_AUTHORING_PIPELINE_SUITE] PASS — C10-A.1 9/9")
        quit(0)
        return

    for failure in failures:
        push_error(failure)
    print("[C10A_VISUAL_AUTHORING_PIPELINE_SUITE] FAIL failures=%d" % failures.size())
    quit(1)
