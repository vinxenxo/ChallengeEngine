extends SceneTree

## C11-C.6 Tracking mechanic contract test v1.0.
## Verifies deterministic smooth-pursuit state without touching frozen challenge simulation.

const TrackingGeneratorClass = preload("res://core/runtime/visual_drill/generators/TrackingGenerator.gd")

const BODY_RECT := Rect2(0.0, 144.0, 540.0, 672.0)
const TARGET_RADIUS: float = 12.0

var failures: Array[String] = []

func _initialize() -> void:
	var generator := TrackingGeneratorClass.new()
	var params := _params()

	_test_state_shape(generator, params)
	_test_target_motion(generator, params)
	_test_body_containment(generator, params)
	_test_history_only_trail(generator, params)
	_test_cosmetic_variant_does_not_change_mechanics(generator, params)
	_test_determinism(generator, params)

	if failures.is_empty():
		print("[C11C_TRACKING_MECHANIC_CONTRACT_SUITE] PASS")
		quit(0)
		return

	for failure in failures:
		push_error(failure)
	print("[C11C_TRACKING_MECHANIC_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
	quit(1)

func _test_state_shape(generator: TrackingGeneratorClass, params: Dictionary) -> void:
	var state := generator.generate_with_variation(20, 60, params, {"tracking_variant": 0.25})
	_assert(str(state.get("generator_type", "")) == "tracking", "Generator type must be tracking.")
	_assert(state.get("target_states", []).size() == 1, "Tracking must emit exactly one target.")
	_assert(str(state.get("trajectory_state", {}).get("type", "")) == "lissajous", "Tracking trajectory must be Lissajous.")
	_assert(str(state.get("task_state", {}).get("type", "")) == "tracking", "Tracking task type must preserve the canonical subtype contract.")
	_assert(str(state.get("task_state", {}).get("mode", "")) == "smooth_pursuit", "Tracking task mode must be smooth_pursuit.")
	_assert(state.get("distractor_states", []).is_empty(), "Canonical tracking baseline must not render distractors.")

func _test_target_motion(generator: TrackingGeneratorClass, params: Dictionary) -> void:
	var state_a := generator.generate(0, 60, params)
	var state_b := generator.generate(30, 60, params)
	var a := Vector2(float(state_a.get("target_states", [])[0].get("x", 0.0)), float(state_a.get("target_states", [])[0].get("y", 0.0)))
	var b := Vector2(float(state_b.get("target_states", [])[0].get("x", 0.0)), float(state_b.get("target_states", [])[0].get("y", 0.0)))
	_assert(a.distance_to(b) > 20.0, "Tracking target must travel materially across the exercise.")

	for frame in range(0, 59):
		var state0 := generator.generate(frame, 60, params)
		var state1 := generator.generate(frame + 1, 60, params)
		var target0: Dictionary = state0.get("target_states", [])[0]
		var target1: Dictionary = state1.get("target_states", [])[0]
		var p0 := Vector2(float(target0.get("x", 0.0)), float(target0.get("y", 0.0)))
		var p1 := Vector2(float(target1.get("x", 0.0)), float(target1.get("y", 0.0)))
		_assert(p0.distance_to(p1) < 80.0, "Tracking frame-to-frame displacement is too large for continuous pursuit.")

	var previous_speed := -1.0
	for frame in range(60):
		var state := generator.generate(frame, 60, params)
		var speed := float(state.get("trajectory_state", {}).get("speed_px_per_second", 0.0))
		_assert(speed >= 0.0 and is_finite(speed), "Tracking emitted an invalid speed value.")
		_assert(speed <= 600.0, "Tracking baseline speed is too high for the intended smooth-pursuit presentation.")
		if previous_speed >= 0.0:
			_assert(abs(speed - previous_speed) < 450.0, "Tracking speed changes too abruptly between frames.")
		previous_speed = speed

func _test_body_containment(generator: TrackingGeneratorClass, params: Dictionary) -> void:
	for frame in range(60):
		var state := generator.generate(frame, 60, params)
		var target: Dictionary = state.get("target_states", [])[0]
		var p := Vector2(float(target.get("x", 0.0)), float(target.get("y", 0.0)))
		_assert(BODY_RECT.grow(-TARGET_RADIUS).has_point(p), "Tracking target escaped Body or touched a forbidden edge margin.")

		var trajectory: Dictionary = state.get("trajectory_state", {})
		var bounds: Dictionary = trajectory.get("bounds", {})
		_assert(float(bounds.get("left", 0.0)) >= TARGET_RADIUS, "Trajectory left bound lacks target clearance.")
		_assert(float(bounds.get("right", 540.0)) <= BODY_RECT.end.x - TARGET_RADIUS, "Trajectory right bound lacks target clearance.")
		_assert(float(bounds.get("top", 0.0)) >= BODY_RECT.position.y + TARGET_RADIUS, "Trajectory top bound lacks target clearance.")
		_assert(float(bounds.get("bottom", 960.0)) <= BODY_RECT.end.y - TARGET_RADIUS, "Trajectory bottom bound lacks target clearance.")

func _test_history_only_trail(generator: TrackingGeneratorClass, params: Dictionary) -> void:
	var state := generator.generate(30, 60, params)
	var trail: Array = state.get("trajectory_state", {}).get("trail_points", [])
	_assert(trail.size() <= 19, "Tracking trail must remain a short history window.")
	_assert(trail.size() > 1, "Tracking trail must include history once movement has started.")
	var current: Dictionary = state.get("target_states", [])[0]
	var current_p := Vector2(float(current.get("x", 0.0)), float(current.get("y", 0.0)))
	var trail_last: Dictionary = trail[trail.size() - 1]
	var last_p := Vector2(float(trail_last.get("x", 0.0)), float(trail_last.get("y", 0.0)))
	_assert(current_p.distance_to(last_p) < 0.01, "Trail last point must equal current target position.")

func _test_cosmetic_variant_does_not_change_mechanics(generator: TrackingGeneratorClass, params: Dictionary) -> void:
	var base := generator.generate_with_variation(24, 60, params, {"tracking_variant": 0.0})
	var variant := generator.generate_with_variation(24, 60, params, {"tracking_variant": 0.99})
	_assert(base.get("target_states", []) == variant.get("target_states", []), "Cosmetic tracking_variant must not alter target mechanic state.")
	_assert(base.get("trajectory_state", {}) == variant.get("trajectory_state", {}), "Cosmetic tracking_variant must not alter trajectory mechanic state.")

func _test_determinism(generator: TrackingGeneratorClass, params: Dictionary) -> void:
	var state_a := generator.generate(37, 60, params)
	var state_b := generator.generate(37, 60, params)
	_assert(state_a == state_b, "Same tracking inputs must generate byte-equivalent state dictionaries.")

func _params() -> Dictionary:
	return {
		"duration": 2.0,
		"fps": 30,
		"frame_count": 60,
		"exercise_parameters": {
			"speed_multiplier": 1.0,
			"pacing_mode": "constant"
		},
		"stimulus": {"type": "dot", "radius": 12.0, "active": true, "x": 270.0, "y": 480.0},
		"targets": [{"id": "t1", "x": 270.0, "y": 480.0, "highlighted": true, "status": "active"}],
		"distractors": [],
		"trajectory": {"type": "lissajous"},
		"task": {"type": "tracking", "mode": "smooth_pursuit", "target_id": "t1"}
	}

func _assert(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)
