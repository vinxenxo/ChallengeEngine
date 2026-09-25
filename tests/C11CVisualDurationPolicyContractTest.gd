extends SceneTree

## C11-C 2.13.0 — standard 20..30s visual duration policy contract.
var failures: Array[String] = []

func _initialize() -> void:
    var policy := FileAccess.get_file_as_string("res://profiles/presentation/c11c_visual_duration_policy.json")
    _assert(policy.find("\"min\": 20.0") >= 0, "Duration policy minimum must be 20s.")
    _assert(policy.find("\"max\": 30.0") >= 0, "Duration policy maximum must be 30s.")
    _assert(policy.find("\"1\": 24.0") >= 0, "One-cycle Visual Loop duration must be 24s.")
    _assert(policy.find("\"2\": 27.0") >= 0, "Two-cycle Visual Loop duration must be 27s.")
    _assert(policy.find("\"3\": 30.0") >= 0, "Three-cycle Visual Loop duration must be 30s.")
    _assert(policy.find("\"tracking\": 24.0") >= 0, "Tracking gameplay duration must be 24s.")
    _assert(policy.find("\"saccade\": 21.0") >= 0, "Saccade gameplay duration must be 21s.")
    _assert(policy.find("\"pursuit\": 24.0") >= 0, "Pursuit gameplay duration must be 24s.")
    _assert(policy.find("\"peripheral_scan\": 21.0") >= 0, "Peripheral Scan gameplay duration must be 21s.")
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
    _assert(drill_review.find("$DefaultGameplayDurationSeconds=21.0") >= 0, "Drill review standard gameplay must be 21s.")
    _assert(drill_review.find("$TrackingGameplayDurationSeconds=24.0") >= 0, "Tracking gameplay must be 24s.")
    if failures.is_empty():
        print("[C11C_VISUAL_DURATION_POLICY_CONTRACT_SUITE] PASS")
        quit(0)
        return
    for f in failures: push_error(f)
    print("[C11C_VISUAL_DURATION_POLICY_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
    quit(1)

func _assert(condition: bool, message: String) -> void:
    if not condition: failures.append(message)
