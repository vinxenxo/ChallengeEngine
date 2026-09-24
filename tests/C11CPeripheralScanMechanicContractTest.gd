extends SceneTree

const Variation = preload("res://core/authoring/VisualDrillSeedVariation.gd")
const GENERATOR_PATH := "res://core/runtime/visual_drill/generators/PeripheralScanGenerator.gd"

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
        "stimulus": {"type": "central_fixation_anchor", "radius": 24.0, "active": true, "x": 270.0, "y": 480.0},
        "targets": [{"id": "central_anchor", "x": 270.0, "y": 480.0, "highlighted": true, "status": "active"}],
        "distractors": [],
        "trajectory": {},
        "task": {"type": "peripheral_scan", "target_id": "central_anchor"}
    }
    var a := Variation.apply("peripheral_scan", 5409, base)
    var b := Variation.apply("peripheral_scan", 5409, base)
    var c := Variation.apply("peripheral_scan", 7770001, base)
    _assert(str(a) == str(b), "Same Peripheral Scan seed must author identically.")
    _assert(str(a.get("task", {}).get("events", [])) != str(c.get("task", {}).get("events", [])), "Different Peripheral Scan seeds must change the authored event schedule.")

    var trajectory: Dictionary = a.get("trajectory", {})
    var task: Dictionary = a.get("task", {})
    var center: Array = trajectory.get("center_normalized", [])
    _assert(center.size() == 2 and is_equal_approx(float(center[0]), 0.5) and is_equal_approx(float(center[1]), 0.5), "Peripheral fixation anchor must remain at normalized center.")
    var events: Array = task.get("events", [])
    _assert(events.size() == int(task.get("threat_count", 0)) + int(task.get("distractor_count", 0)), "Threat + distractor count must equal total authored events.")
    _assert(int(task.get("threat_count", 0)) > 0, "Peripheral schedule must contain threats.")
    _assert(int(task.get("distractor_count", 0)) > 0, "Peripheral schedule must contain distractors.")
    for event in events:
        var radius_norm := float(event.get("radius_norm", 0.0))
        _assert(radius_norm >= 0.20 and radius_norm <= 0.48, "Peripheral event radius must stay inside the three orbital bands.")
        var angle := float(event.get("angle_rad", -1.0))
        _assert(angle >= 0.0 and angle <= TAU, "Peripheral event angle must be polar and bounded to 0..TAU.")
        var duration := int(event.get("duration_frames", 0))
        _assert(duration >= 6 and duration <= 18, "Peripheral event duration must stay within the 200–600 ms contract.")
        if str(event.get("kind", "")) == "threat":
            _assert(str(event.get("pulse_pattern", "")) == "double", "Threats must use the double-flash signature.")
        else:
            _assert(str(event.get("pulse_pattern", "")) == "single", "Distractors must use the single-flash signature.")

    var generator_script: Script = load(GENERATOR_PATH) as Script
    _assert(generator_script != null, "PeripheralScanGenerator script must load successfully.")
    if generator_script == null or not generator_script.can_instantiate():
        _assert(false, "PeripheralScanGenerator must be instantiable; parse/load failures must fail this suite.")
        return
    var generator: VisualDrillGenerator = generator_script.new() as VisualDrillGenerator
    _assert(generator != null and is_instance_valid(generator), "PeripheralScanGenerator must instantiate successfully.")
    if generator == null or not is_instance_valid(generator):
        return
    var frame0 := generator.generate_with_variation(0, 510, a, {"pattern_variant": 0.25, "amplitude_variant": 0.75})
    _assert(frame0.get("target_states", []).size() == 1, "Peripheral Scan must expose exactly one central fixation anchor.")
    var anchor_state: Dictionary = frame0.get("task_state", {}).get("anchor_state", {})
    _assert(is_equal_approx(float(anchor_state.get("x", -1.0)), 270.0), "Peripheral anchor X must remain fixed at 270.")
    _assert(is_equal_approx(float(anchor_state.get("y", -1.0)), 480.0), "Peripheral anchor Y must remain fixed at 480.")

func _assert(condition: bool, message: String) -> void:
    if not condition:
        failures.append(message)

func _conclude() -> void:
    if failures.is_empty():
        print("[C11C_PERIPHERAL_SCAN_MECHANIC_CONTRACT_SUITE] PASS")
        quit(0)
    else:
        for failure in failures:
            push_error(failure)
        print("[C11C_PERIPHERAL_SCAN_MECHANIC_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
        quit(1)
