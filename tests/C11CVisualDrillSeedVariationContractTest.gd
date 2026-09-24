extends SceneTree

## C11-C 2.8.0 — Seeded Visual Drill authoring variation contract.
## Verifies that visual-drill content seeds create deterministic but materially different
## Tracking mechanics before runtime, without touching presentation RNG or simulation.

const SeedVariationClass = preload("res://core/authoring/VisualDrillSeedVariation.gd")
const TrackingGeneratorClass = preload("res://core/runtime/visual_drill/generators/TrackingGenerator.gd")

var failures: Array[String] = []

func _initialize() -> void:
    _test_same_seed_is_stable()
    _test_different_seeds_change_motion()
    _test_motion_stays_inside_contract_bounds()
    _test_saccade_seeds_change_spatial_sequence()
    _test_pursuit_variation()
    _test_peripheral_scan_variation()
    if failures.is_empty():
        print("[C11C_VISUAL_DRILL_SEED_VARIATION_CONTRACT_SUITE] PASS")
        quit(0)
    else:
        for failure in failures:
            push_error(failure)
        print("[C11C_VISUAL_DRILL_SEED_VARIATION_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
        quit(1)

func _test_same_seed_is_stable() -> void:
    var payload := _tracking_payload()
    var a := SeedVariationClass.apply("tracking", 314159, payload)
    var b := SeedVariationClass.apply("tracking", 314159, payload)
    _assert(a == b, "The same Tracking seed must produce identical authored motion parameters.")

func _test_different_seeds_change_motion() -> void:
    var payload := _tracking_payload()
    var seeds: Array[int] = [314159, 944296688, 1411540143, 489652843, 1266632463, 1881088635]
    var signatures := {}
    for seed_value in seeds:
        var result: Dictionary = SeedVariationClass.apply("tracking", seed_value, payload)
        var trajectory: Dictionary = result.get("trajectory", {})
        var signature := "%d:%d:%.5f:%.5f:%.3f:%.3f:%.5f" % [
            int(trajectory.get("x_frequency", 0.0)),
            int(trajectory.get("y_frequency", 0.0)),
            float(trajectory.get("phase_x", 0.0)),
            float(trajectory.get("phase_y", 0.0)),
            float(trajectory.get("travel_cycles", 0.0)),
            float(trajectory.get("motion_speed_multiplier", 0.0)),
            float(trajectory.get("amplitude_x", 0.0))
        ]
        signatures[signature] = true
    _assert(signatures.size() >= 5, "Tracking seeds must create materially different motion signatures; only %d/%d were distinct." % [signatures.size(), seeds.size()])

    var generator := TrackingGeneratorClass.new()
    var authored_a: Dictionary = SeedVariationClass.apply("tracking", seeds[0], payload)
    var authored_b: Dictionary = SeedVariationClass.apply("tracking", seeds[1], payload)
    var frame_a: Dictionary = generator.generate(157, 630, authored_a)
    var frame_b: Dictionary = generator.generate(157, 630, authored_b)
    _assert(frame_a.get("trajectory_state", {}).get("position", {}) != frame_b.get("trajectory_state", {}).get("position", {}), "Different Tracking seeds must produce different runtime positions.")
    _assert(absf(float(frame_a.get("trajectory_state", {}).get("speed_px_per_second", 0.0)) - float(frame_b.get("trajectory_state", {}).get("speed_px_per_second", 0.0))) > 0.5, "Different Tracking seeds must materially vary instantaneous speed.")

func _test_motion_stays_inside_contract_bounds() -> void:
    var payload := _tracking_payload()
    var generator := TrackingGeneratorClass.new()
    for seed_value in [1, 12345, 314159, 2147483646]:
        var authored: Dictionary = SeedVariationClass.apply("tracking", seed_value, payload)
        var trajectory: Dictionary = authored.get("trajectory", {})
        _assert(float(trajectory.get("amplitude_x", 0.0)) >= 138.0 and float(trajectory.get("amplitude_x", 0.0)) <= 184.0, "Tracking seeded amplitude_x outside authoring range.")
        _assert(float(trajectory.get("amplitude_y", 0.0)) >= 184.0 and float(trajectory.get("amplitude_y", 0.0)) <= 248.0, "Tracking seeded amplitude_y outside authoring range.")
        _assert(float(trajectory.get("motion_speed_multiplier", 0.0)) >= 0.72 and float(trajectory.get("motion_speed_multiplier", 0.0)) <= 1.38, "Tracking seeded speed multiplier outside authoring range.")
        for frame_index in range(0, 630, 31):
            var frame: Dictionary = generator.generate(frame_index, 630, authored)
            var target: Dictionary = frame.get("target_states", [])[0]
            var x := float(target.get("x", 0.0))
            var y := float(target.get("y", 0.0))
            _assert(x >= 48.0 and x <= 492.0, "Tracking seeded target escaped horizontal safe zone.")
            _assert(y >= 180.0 and y <= 780.0, "Tracking seeded target escaped vertical safe zone.")


func _test_saccade_seeds_change_spatial_sequence() -> void:
    var payload := {
        "trajectory": {
            "type": "polar_golden_angle"
        }
    }
    var seeds: Array[int] = [314159, 944296688, 1411540143, 489652843, 1266632463, 1881088635]
    var signatures := {}
    var generator := preload("res://core/runtime/visual_drill/generators/SaccadeGenerator.gd").new()
    for seed_value in seeds:
        var authored: Dictionary = SeedVariationClass.apply("saccade", seed_value, payload)
        var trajectory: Dictionary = authored.get("trajectory", {})
        var signature := "%.6f:%.6f:%.3f:%.3f" % [
            float(trajectory.get("angle_step", 0.0)),
            float(trajectory.get("angle_offset", 0.0)),
            float(trajectory.get("radius_base", 0.0)),
            float(trajectory.get("radius_variation", 0.0))
        ]
        signatures[signature] = true
        for frame in [8, 26, 44, 62, 80]:
            var state: Dictionary = generator.generate(frame, 510, authored)
            var saccade: Dictionary = state.get("saccade_state", {})
            if int(saccade.get("jump_index", 0)) > 0:
                var distance := float(saccade.get("jump_distance", 0.0))
                _assert(distance >= 180.0 and distance <= 300.0, "Seeded Saccade jump distance left the 180..300 px contract.")
    _assert(signatures.size() >= 4, "Saccade seeds must create multiple authored spatial signatures; only %d/%d were distinct." % [signatures.size(), seeds.size()])

func _tracking_payload() -> Dictionary:
    return {
        "duration": 21.0,
        "fps": 30,
        "frame_count": 630,
        "exercise_parameters": {
            "generator": "tracking",
            "difficulty_tier": 2,
            "speed_multiplier": 1.0,
            "pacing_mode": "constant"
        },
        "trajectory": {
            "type": "lissajous",
            "profile": "lissajous_2_3_bounded_v1",
            "center_x": 270.0,
            "center_y": 480.0,
            "amplitude_x": 160.0,
            "amplitude_y": 210.0,
            "x_frequency": 2.0,
            "y_frequency": 3.0,
            "travel_cycles": 0.75,
            "phase_x": 0.25,
            "phase_y": -0.65,
            "target_radius": 12.0,
            "trail_length_frames": 630,
            "trail_mode": "growing_history"
        }
    }



func _test_pursuit_variation() -> void:
    var base := {"frame_count": 510, "exercise_parameters": {"difficulty_tier": 2}, "trajectory": {}, "task": {"type": "pursuit"}}
    var a := VisualDrillSeedVariation.apply("pursuit", 5409, base)
    var b := VisualDrillSeedVariation.apply("pursuit", 7770001, base)
    _assert(str(a.get("trajectory", {}).get("control_points_normalized", [])) != str(b.get("trajectory", {}).get("control_points_normalized", [])), "Pursuit seeds must author different B-spline control points.")
    _assert(int(a.get("task", {}).get("sizygia_count", 0)) == 4, "Pursuit seed 5409 must author four sizygias.")
    _assert(a.get("trajectory", {}).get("arc_length_parameterized", false) == true, "Pursuit seed variation must author arc-length parameterization.")

func _test_peripheral_scan_variation() -> void:
    var base := {"frame_count": 510, "exercise_parameters": {"difficulty_tier": 2}, "trajectory": {}, "task": {"type": "peripheral_scan"}}
    var a := VisualDrillSeedVariation.apply("peripheral_scan", 5409, base)
    var b := VisualDrillSeedVariation.apply("peripheral_scan", 7770001, base)
    _assert(str(a.get("task", {}).get("events", [])) != str(b.get("task", {}).get("events", [])), "Peripheral Scan seeds must author different event schedules.")
    _assert(int(a.get("task", {}).get("threat_count", 0)) > 0, "Peripheral Scan must author threats.")
    _assert(int(a.get("task", {}).get("distractor_count", 0)) > 0, "Peripheral Scan must author distractors.")
    _assert(a.get("task", {}).get("answer_sheet", {}).has("threat_frame_starts"), "Peripheral Scan answer sheet must expose threat frame starts.")
    _assert(a.get("task", {}).get("answer_sheet", {}).get("threat_count", -1) == int(a.get("task", {}).get("threat_count", -2)), "Peripheral Scan answer sheet threat count must match authored count.")
    _assert(a.get("task", {}).get("answer_sheet", {}).get("distractor_count", -1) == int(a.get("task", {}).get("distractor_count", -2)), "Peripheral Scan answer sheet distractor count must match authored count.")

func _assert(condition: bool, message: String) -> void:
    if not condition:
        failures.append(message)

func _conclude() -> void:
    if failures.is_empty():
        print("[C11C_VISUAL_DRILL_SEED_VARIATION_CONTRACT_SUITE] PASS")
        quit(0)
    else:
        for failure in failures:
            push_error(failure)
        print("[C11C_VISUAL_DRILL_SEED_VARIATION_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
        quit(1)
