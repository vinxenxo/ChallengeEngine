extends SceneTree

## C10-B — Visual Authoring determinism and reproducibility.
## Scope: product authoring only.
## Does not modify or inspect generator math, runtime state, RNG sampling, or rendering.

const Request = preload("res://core/authoring/VisualAuthoringRequest.gd")
const Context = preload("res://core/authoring/VisualAuthoringAssemblyContext.gd")
const Generator = preload("res://core/authoring/VisualAuthoringGenerator.gd")
const PolicyRegistry = preload("res://core/authoring/VisualAuthoringPolicyRegistry.gd")
const Resolver = preload("res://core/authoring/VisualDifficultyResolver.gd")
const SeedVariation = preload("res://core/authoring/VisualDrillSeedVariation.gd")

const LOOP_SUBTYPES := ["fractal", "vector_field", "particle_flow", "kaleidoscope", "geometric"]
const DRILL_SUBTYPES := ["tracking", "pursuit", "saccade", "peripheral_scan"]
const ALL_ROUTES := [
    {"domain_family": "visual_loop", "subtype": "fractal"},
    {"domain_family": "visual_loop", "subtype": "vector_field"},
    {"domain_family": "visual_loop", "subtype": "particle_flow"},
    {"domain_family": "visual_loop", "subtype": "kaleidoscope"},
    {"domain_family": "visual_loop", "subtype": "geometric"},
    {"domain_family": "visual_drill", "subtype": "tracking"},
    {"domain_family": "visual_drill", "subtype": "pursuit"},
    {"domain_family": "visual_drill", "subtype": "saccade"},
    {"domain_family": "visual_drill", "subtype": "peripheral_scan"}
]

const SEED_A := 12345
const SEED_B := 54321
const TIER_BASELINE := 2
const TIER_VARIANT := 4

var failures: Array[String] = []

func _init() -> void:
    print("[TEST] Running C10BDeterminismTest...")
    _test_same_request_same_context_is_bitwise_equal_9_of_9()
    _test_seed_injection_isolation_9_of_9()
    _test_tier_4_propagates_declared_policy_without_touching_seed_9_of_9()
    _test_request_immutability_and_context_immutability_9_of_9()
    _conclude()

func _assert(condition: bool, message: String) -> void:
    if not condition:
        failures.append(message)

func _request(domain_family: String, subtype: String, tier: int = TIER_BASELINE, custom: Dictionary = {}) -> Request:
    return Request.new(domain_family, subtype, 2.0, 30, tier, custom)

func _context(seed_value: int, content_id: String) -> Context:
    return Context.new(
        seed_value,
        "2.0",
        content_id,
        "1.0.0",
        "4.7.1",
        {"profile_id": "social_default_v1", "coordinate_space": "2d"},
        {"family_id": "fam_001"},
        {"profile_id": "default_procedural_music", "enabled": false},
        {"author": "c10_visual_authoring", "timestamp_ms": 0}
    )

func _generate(route: Dictionary, seed_value: int, tier: int) -> Dictionary:
    var domain_family := str(route["domain_family"])
    var subtype := str(route["subtype"])
    var req := _request(domain_family, subtype, tier)
    var content_id := "C10B_%s_%s" % [domain_family.to_upper(), subtype.to_upper()]
    return Generator.generate(req, _context(seed_value, content_id))

func _without_seed(value: Variant) -> Variant:
    if value is Dictionary:
        var out: Dictionary = {}
        for key in value.keys():
            if str(key) == "seed":
                continue
            out[key] = _without_seed(value[key])
        return out
    if value is Array:
        var arr: Array = []
        for item in value:
            arr.append(_without_seed(item))
        return arr
    return value

func _test_same_request_same_context_is_bitwise_equal_9_of_9() -> void:
    var passed := 0
    for route in ALL_ROUTES:
        var a := _generate(route, SEED_A, TIER_BASELINE)
        var b := _generate(route, SEED_A, TIER_BASELINE)
        var subtype := str(route["subtype"])

        _assert(bool(a.get("success", false)), "A generation failed for %s/%s" % [str(route["domain_family"]), subtype])
        _assert(bool(b.get("success", false)), "B generation failed for %s/%s" % [str(route["domain_family"]), subtype])
        if bool(a.get("success", false)) and bool(b.get("success", false)):
            var env_a: Dictionary = a.get("content", {})
            var env_b: Dictionary = b.get("content", {})
            _assert(env_a == env_b, "A != B structurally for identical request/context at %s/%s" % [str(route["domain_family"]), subtype])
            _assert(JSON.stringify(env_a) == JSON.stringify(env_b), "A != B byte-level JSON serialization for identical request/context at %s/%s" % [str(route["domain_family"]), subtype])
            passed += 1

    print("[C10B] Identity determinism: %d/9" % passed)
    _assert(passed == 9, "C10-B identity determinism must pass 9/9")

func _test_seed_injection_isolation_9_of_9() -> void:
    var passed := 0
    for route in ALL_ROUTES:
        var a := _generate(route, SEED_A, TIER_BASELINE)
        var b := _generate(route, SEED_B, TIER_BASELINE)
        var subtype := str(route["subtype"])

        _assert(bool(a.get("success", false)) and bool(b.get("success", false)), "Seed-isolation generation failed for %s/%s" % [str(route["domain_family"]), subtype])
        if bool(a.get("success", false)) and bool(b.get("success", false)):
            var env_a: Dictionary = a.get("content", {})
            var env_b: Dictionary = b.get("content", {})

            _assert(int(env_a.get("seed", -1)) == SEED_A, "Seed A was not preserved for %s/%s" % [str(route["domain_family"]), subtype])
            _assert(int(env_b.get("seed", -1)) == SEED_B, "Seed B was not preserved for %s/%s" % [str(route["domain_family"]), subtype])
            var env_a_no_seed = _without_seed(env_a)
            var env_b_no_seed = _without_seed(env_b)
            if str(route["domain_family"]) == "visual_drill" and subtype in ["tracking", "saccade"]:
                _assert(env_a_no_seed != env_b_no_seed, "C11-C 2.6.0 %s seed variation must alter authored motion data for %s/%s" % [subtype.to_upper(), str(route["domain_family"]), subtype])
            else:
                _assert(env_a_no_seed == env_b_no_seed, "Changing seed altered non-seed authoring data for %s/%s" % [str(route["domain_family"]), subtype])
                _assert(JSON.stringify(env_a_no_seed) == JSON.stringify(env_b_no_seed), "Changing seed altered non-seed JSON serialization for %s/%s" % [str(route["domain_family"]), subtype])
            passed += 1

    print("[C10B] Seed injection isolation: %d/9" % passed)
    _assert(passed == 9, "C10-B seed isolation must pass 9/9")

func _test_tier_4_propagates_declared_policy_without_touching_seed_9_of_9() -> void:
    var passed := 0

    for route in ALL_ROUTES:
        var domain_family := str(route["domain_family"])
        var subtype := str(route["subtype"])
        var baseline := _generate(route, SEED_A, TIER_BASELINE)
        var variant := _generate(route, SEED_A, TIER_VARIANT)

        _assert(bool(baseline.get("success", false)) and bool(variant.get("success", false)), "Tier comparison generation failed for %s/%s" % [domain_family, subtype])
        if not bool(baseline.get("success", false)) or not bool(variant.get("success", false)):
            continue

        var policy := PolicyRegistry.get_policy(domain_family, subtype)
        _assert(not policy.is_empty(), "Missing policy for tier comparison %s/%s" % [domain_family, subtype])
        if policy.is_empty():
            continue

        var expected_resolution := Resolver.resolve(TIER_VARIANT, policy, {})
        _assert(bool(expected_resolution.get("success", false)), "Policy tier-4 resolution failed for %s/%s" % [domain_family, subtype])
        if not bool(expected_resolution.get("success", false)):
            continue

        var expected: Dictionary = expected_resolution.get("effective_parameters", {})
        var actual: Dictionary = variant.get("effective_parameters", {})

        _assert(actual == expected, "Tier-4 effective parameters do not match declarative policy for %s/%s" % [domain_family, subtype])

        var baseline_env: Dictionary = baseline.get("content", {})
        var variant_env: Dictionary = variant.get("content", {})
        _assert(int(variant_env.get("seed", -1)) == SEED_A, "Tier-4 changed external seed for %s/%s" % [domain_family, subtype])

        if domain_family == "visual_loop":
            var expected_speed = expected.get("speed", null)
            var expected_complexity = expected.get("complexity", null)
            var layer: Dictionary = variant_env.get("payload", {}).get("visual_parameters", {}).get("layers", [{}])[0]
            _assert(layer.get("speed", null) == expected_speed, "Tier-4 speed not propagated for %s/%s" % [domain_family, subtype])
            _assert(layer.get("complexity", null) == expected_complexity, "Tier-4 complexity not propagated for %s/%s" % [domain_family, subtype])
        else:
            var payload: Dictionary = variant_env.get("payload", {})
            var exercise: Dictionary = payload.get("exercise_parameters", {})

            # The frozen visual_drill payload keeps product execution parameters
            # inside exercise_parameters, while the canonical drill state blocks
            # remain direct payload siblings. Do not collapse those two contracts.
            for key in ["generator", "difficulty_tier", "speed_multiplier", "pacing_mode"]:
                if expected.has(key):
                    _assert(exercise.get(key, null) == expected[key], "Tier-4 exercise parameter '%s' not propagated for %s/%s" % [str(key), domain_family, subtype])

            for key in ["stimulus", "targets", "distractors", "trajectory"]:
                if expected.has(key):
                    var expected_value: Variant = expected[key]
                    if subtype in ["tracking", "saccade"] and key == "trajectory":
                        expected_value = SeedVariation.apply(subtype, SEED_A, {"trajectory": expected[key]}).get("trajectory", expected[key])
                    _assert(payload.get(key, null) == expected_value, "Tier-4 payload parameter '%s' not propagated for %s/%s" % [str(key), domain_family, subtype])

            var task_expected: Dictionary = expected.get("task", {})
            _assert(payload.get("task", {}) == task_expected, "Tier-4 task mapping mismatch for %s/%s" % [domain_family, subtype])

        var baseline_without_seed: Dictionary = _without_seed(baseline_env)
        var variant_without_seed: Dictionary = _without_seed(variant_env)
        _assert(baseline_without_seed != variant_without_seed, "Tier-4 must change domain authoring output for %s/%s" % [domain_family, subtype])
        passed += 1

    print("[C10B] Tier-4 policy propagation: %d/9" % passed)
    _assert(passed == 9, "C10-B tier-4 propagation must pass 9/9")

func _test_request_immutability_and_context_immutability_9_of_9() -> void:
    var passed := 0

    for route in ALL_ROUTES:
        var domain_family := str(route["domain_family"])
        var subtype := str(route["subtype"])
        var req := _request(domain_family, subtype, TIER_BASELINE)
        var ctx := _context(SEED_A, "C10B_%s_%s" % [domain_family.to_upper(), subtype.to_upper()])
        var req_before := req.to_dictionary().duplicate(true)
        var seed_before := ctx.seed
        var rng_before := ctx.rng_version
        var presentation_before := ctx.presentation.duplicate(true)
        var assets_before := ctx.assets.duplicate(true)
        var audio_before := ctx.audio.duplicate(true)
        var provenance_before := ctx.provenance.duplicate(true)

        var result := Generator.generate(req, ctx)
        _assert(bool(result.get("success", false)), "Immutability generation failed for %s/%s" % [domain_family, subtype])

        _assert(req.to_dictionary() == req_before, "Request mutated during authoring for %s/%s" % [domain_family, subtype])
        _assert(ctx.seed == seed_before, "Context seed mutated during authoring for %s/%s" % [domain_family, subtype])
        _assert(ctx.rng_version == rng_before, "Context RNG version mutated during authoring for %s/%s" % [domain_family, subtype])
        _assert(ctx.presentation == presentation_before, "Context presentation mutated during authoring for %s/%s" % [domain_family, subtype])
        _assert(ctx.assets == assets_before, "Context assets mutated during authoring for %s/%s" % [domain_family, subtype])
        _assert(ctx.audio == audio_before, "Context audio mutated during authoring for %s/%s" % [domain_family, subtype])
        _assert(ctx.provenance == provenance_before, "Context provenance mutated during authoring for %s/%s" % [domain_family, subtype])

        passed += 1

    print("[C10B] Input immutability: %d/9" % passed)
    _assert(passed == 9, "C10-B input immutability must pass 9/9")

func _conclude() -> void:
    if failures.is_empty():
        print("[C10B_VISUAL_AUTHORING_DETERMINISM_SUITE] PASS — C10-B 9/9")
        quit(0)
        return

    for failure in failures:
        push_error(failure)
    print("[C10B_VISUAL_AUTHORING_DETERMINISM_SUITE] FAIL failures=%d" % failures.size())
    quit(1)
