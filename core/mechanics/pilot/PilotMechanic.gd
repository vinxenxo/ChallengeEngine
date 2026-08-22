class_name PilotMechanic
extends ChallengeMechanic

const RNG_REGISTRY = preload("res://core/deterministic/RNGStreamRegistry.gd")

var _rng_context: MechanicRNGContext

var start_x: float = 0.0
var end_x: float = 100.0
var target_start: float = 0.0
var target_velocity: float = 0.0
var trajectory_amplitude: float = 2.0
var control_amplitude: float = 0.5
var tolerance_distance: float = 5.0

func setup(config: Dictionary) -> void:
	_is_setup = false
	_is_prepared = false
	_error_state = "OK"
	var content: Dictionary = config.get("content", {})
	start_x = float(content.get("start_x", 0.0))
	end_x = float(content.get("end_x", 100.0))
	target_start = float(content.get("target_start", 0.0))
	target_velocity = float(content.get("target_velocity", 0.0))
	trajectory_amplitude = float(content.get("trajectory_amplitude", 2.0))
	control_amplitude = float(content.get("control_amplitude", 0.5))

	var tolerance: Dictionary = config.get("difficulty", {}).get("tolerance", {})
	tolerance_distance = float(tolerance.get("distance_px", 5.0))
	_is_setup = true

func set_rng_context(context: MechanicRNGContext) -> void:
	_rng_context = context
	_error_state = "OK"

func clear_rng_context() -> void:
	_rng_context = null
	_error_state = "OK"

func simulate(
	total_game_frames: int,
	_local_seed: int,
	config: Dictionary
) -> SimulationResult:
	setup(config)

	var result: SimulationResult = SimulationResult.new()
	result.tolerance_threshold = tolerance_distance

	if _rng_context == null:
		result.metadata = {
			"mechanic": "pilot",
			"rng_version": "2.0",
			"simulation_error": "RNG_CONTEXT_INVALID"
		}
		return result

	if _error_state != "OK":
		result.metadata = {
			"mechanic": "pilot",
			"rng_version": "2.0",
			"simulation_error": _error_state
		}
		return result

	var trajectory_stream: int = RNG_REGISTRY.STREAM_TRAJECTORY
	var control_stream: int = RNG_REGISTRY.STREAM_CONTROL

	for f in range(total_game_frames):
		var snapshot: FrameSnapshot = FrameSnapshot.new()
		var normalized_frame: float = (
			float(f) / float(total_game_frames - 1)
			if total_game_frames > 1
			else 0.0
		)

		var base_position: float = (
			start_x + (end_x - start_x) * normalized_frame
		)

		var trajectory_sample: float = _rng_context.sample_float(
			trajectory_stream,
			f
		)
		var control_sample: float = _rng_context.sample_float(
			control_stream,
			f
		)

		if _rng_context.error_state != "OK":
			result.metadata = {
				"mechanic": "pilot",
				"rng_version": "2.0",
				"simulation_error": _rng_context.error_state,
				"error_frame": f
			}
			return result

		var trajectory_noise: float = (
			(trajectory_sample * 2.0 - 1.0) * trajectory_amplitude
		)
		var control_offset: float = (
			(control_sample * 2.0 - 1.0) * control_amplitude
		)

		var x: float = (
			base_position
			+ trajectory_noise
			+ control_offset
		)

		var target_x: float = target_start + target_velocity * float(f)
		var success_distance: float = abs(x - target_x)
		var velocity: float = 0.0

		if f > 0:
			var previous_normalized: float = float(f - 1) / float(total_game_frames - 1)
			var previous_base: float = start_x + (end_x - start_x) * previous_normalized
			var previous_trajectory: float = _rng_context.sample_float(
				trajectory_stream,
				f - 1
			)
			var previous_control: float = _rng_context.sample_float(
				control_stream,
				f - 1
			)

			if _rng_context.error_state != "OK":
				result.metadata = {
					"mechanic": "pilot",
					"rng_version": "2.0",
					"simulation_error": _rng_context.error_state,
					"error_frame": f
				}
				return result

			var previous_x: float = (
				previous_base
				+ (previous_trajectory * 2.0 - 1.0) * trajectory_amplitude
				+ (previous_control * 2.0 - 1.0) * control_amplitude
			)
			velocity = abs(x - previous_x)

		snapshot.position = Vector2(x, 0.0)
		snapshot.rotation = 0.0
		snapshot.scale = Vector2.ONE
		snapshot.opacity = 1.0
		snapshot.custom_data = {
			"success_distance": success_distance,
			"velocity": velocity,
			"target_x": target_x,
			"base_x": base_position,
			"trajectory_noise": trajectory_noise,
			"control_offset": control_offset
		}

		result.frames.append(snapshot)

	result.metadata = {
		"mechanic": "pilot",
		"rng_version": "2.0"
	}

	return result
