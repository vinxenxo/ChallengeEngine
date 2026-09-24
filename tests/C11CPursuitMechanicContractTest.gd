extends SceneTree

## C11-C.8 2.8.0 — Pursuit mechanic contract.
## Authoring owns B-spline + arc-length tables + cognitive event answer sheet.

const Variation = preload("res://core/authoring/VisualDrillSeedVariation.gd")
const Generator = preload("res://core/runtime/visual_drill/generators/PursuitGenerator.gd")

var failures: Array[String] = []

func _initialize() -> void:
    _run_tests()
    _conclude()

func _run_tests() -> void:
    var base := {
        "duration": 17.0,
        "fps": 30,
        "frame_count": 510,
        "exercise_parameters": {"difficulty_tier": 2, "speed_multiplier": 1.0, "pacing_mode": "constant"},
        "stimulus": {"type": "pursuit_target", "radius": 20.0, "active": true, "x": 270.0, "y": 480.0},
        "targets": [{"id": "t1", "x": 270.0, "y": 480.0, "highlighted": true, "status": "active"}],
        "distractors": [],
        "trajectory": {},
        "task": {"type": "pursuit", "target_id": "t1"}
    }
    var a := Variation.apply("pursuit", 5409, base)
    var b := Variation.apply("pursuit", 5409, base)
    var c := Variation.apply("pursuit", 7770001, base)
    _assert(str(a) == str(b), "Same Pursuit seed must author identically.")
    _assert(str(a.get("trajectory", {}).get("control_points_normalized", [])) != str(c.get("trajectory", {}).get("control_points_normalized", [])), "Different Pursuit seeds must change the authored path.")

    var trajectory: Dictionary = a.get("trajectory", {})
    var lut: Array = trajectory.get("arc_length_lut", [])
    var samples: Array = trajectory.get("position_samples_normalized", [])
    _assert(trajectory.get("arc_length_parameterized", false) == true, "Pursuit must use authored arc-length parameterization.")
    _assert(samples.size() == 510, "Pursuit must author one position sample per gameplay frame.")
    _assert(lut.size() > 100, "Pursuit arc-length LUT is unexpectedly small.")
    var previous_distance := -1.0
    for item in lut:
        var distance_value := float(item.get("distance", -1.0))
        _assert(distance_value >= previous_distance, "Pursuit arc-length LUT must be monotonic.")
        previous_distance = distance_value
        _assert(float(item.get("x", 0.0)) >= 0.10 and float(item.get("x", 0.0)) <= 0.90, "Pursuit normalized X leaves the safe body envelope.")
        _assert(float(item.get("y", 0.0)) >= 0.10 and float(item.get("y", 0.0)) <= 0.90, "Pursuit normalized Y leaves the safe body envelope.")

    var task: Dictionary = a.get("task", {})
    _assert(int(task.get("sizygia_count", 0)) == 4, "Seed 5409 must author exactly 4 sizygias in the canonical example path.")
    var events: Array = task.get("sizygia_events", [])
    _assert(events.size() == int(task.get("sizygia_count", 0)), "Sizygia event count must equal the answer-sheet count.")
    for event in events:
        var duration := int(event.get("duration_frames", 0))
        _assert(duration == 5 or duration == 6, "Sizygia duration must be 150–200 ms at 30 FPS.")

    var generator := Generator.new()
    var frame0 := generator.generate_with_variation(0, 510, a, {"pursuit_variant": 0.2})
    var frame1 := generator.generate_with_variation(1, 510, a, {"pursuit_variant": 0.2})
    _assert(frame0.get("trajectory_state", {}).get("parameterization", "") == "arc_length", "Runtime Pursuit state must declare arc-length parameterization.")
    _assert(frame0.get("target_states", []).size() == 1, "Pursuit must expose exactly one target.")
    _assert(frame1.get("target_states", []).size() == 1, "Pursuit must expose exactly one target on every frame.")
    _assert(str(frame0.get("trajectory_state", {}).get("parameterization", "")) != "time_step", "Pursuit may not use direct t-step traversal.")

func _assert(condition: bool, message: String) -> void:
    if not condition:
        failures.append(message)

func _conclude() -> void:
    if failures.is_empty():
        print("[C11C_PURSUIT_MECHANIC_CONTRACT_SUITE] PASS")
        quit(0)
    else:
        for failure in failures:
            push_error(failure)
        print("[C11C_PURSUIT_MECHANIC_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
        quit(1)
