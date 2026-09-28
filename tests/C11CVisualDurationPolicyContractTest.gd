extends SceneTree

## C11-C 2.18.4 — current Visual Loop / Visual Drill duration policy contract.
## Presentation/authoring contract only. No simulation/mechanics ownership.
var failures: Array[String] = []

func _initialize() -> void:
    var policy := FileAccess.get_file_as_string("res://profiles/presentation/c11c_visual_duration_policy.json")
    _assert(policy.find("\"duration_range_seconds\":") >= 0, "Visual Loop duration range must be explicitly declared.")
    _assert(policy.find("\"visual_loops\":") >= 0, "Duration policy must define Visual Loop duration policy.")
    _assert(policy.find("\"max\": 23.0") >= 0, "Visual Loop duration maximum must be 23s.")
    _assert(policy.find("\"1\": 20.0") >= 0, "One-cycle Visual Loop duration must be 20s.")
    _assert(policy.find("\"2\": 22.0") >= 0, "Two-cycle Visual Loop duration must be 22s.")
    _assert(policy.find("\"3\": 23.0") >= 0, "Three-cycle Visual Loop duration must be 23s.")
    _assert(policy.find("\"tracking\": 21.0") >= 0, "Tracking gameplay duration must be 21s.")
    _assert(policy.find("\"saccade\": 17.0") >= 0, "Saccade gameplay duration must be 17s.")
    _assert(policy.find("\"pursuit\": 17.0") >= 0, "Pursuit gameplay duration must be 17s.")
    _assert(policy.find("\"peripheral_scan\": 17.0") >= 0, "Peripheral Scan gameplay duration must be 17s.")
    _assert(policy.find("\"tracking\": 27.0") >= 0, "Tracking total presentation duration must be 27s.")
    _assert(policy.find("\"saccade\": 23.0") >= 0, "Saccade total presentation duration must be 23s.")
    _assert(policy.find("\"pursuit\": 23.0") >= 0, "Pursuit total presentation duration must be 23s.")
    _assert(policy.find("\"peripheral_scan\": 23.0") >= 0, "Peripheral Scan total presentation duration must be 23s.")

    for path in [
        "res://tools/prototypes/c11c_geometric_waves_v1/GeometricWavesPrototype.gd",
        "res://tools/prototypes/c11c_fractal_bloom_v1/FractalBloomPrototype.gd",
        "res://tools/prototypes/c11c_sacred_symmetry_v1/SacredSymmetryPrototype.gd",
        "res://tools/prototypes/c11c_living_particles_v1/LivingParticlesPrototype.gd",
        "res://tools/prototypes/c11c_invisible_forces_v1/InvisibleForcesPrototype.gd"
    ]:
        var source := FileAccess.get_file_as_string(path)
        _assert(source.find("C11CVisualLoopDuration.gd") >= 0, path + " must consume shared duration policy.")
        _assert(source.find("_frame_count") >= 0, path + " must resolve an exact frame count.")

    var drill_review := FileAccess.get_file_as_string("res://tools/prototypes/c11c_bulk/run_c11c_visual_drill_review.ps1")
    _assert(drill_review.find("$DefaultGameplayDurationSeconds=17.0") >= 0, "Visual Drill default gameplay must be 17s.")
    _assert(drill_review.find("$TrackingGameplayDurationSeconds=21.0") >= 0, "Tracking gameplay must be 21s.")

    if failures.is_empty():
        print("[C11C_VISUAL_DURATION_POLICY_CONTRACT_SUITE] PASS")
        quit(0)
        return
    for failure in failures:
        push_error(failure)
    print("[C11C_VISUAL_DURATION_POLICY_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
    quit(1)

func _assert(condition: bool, message: String) -> void:
    if not condition:
        failures.append(message)
