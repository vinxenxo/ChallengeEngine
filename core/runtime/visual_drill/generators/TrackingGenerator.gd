# res://core/runtime/visual_drill/generators/TrackingGenerator.gd
class_name TrackingGenerator
extends VisualDrillGenerator

## C11-C.6 / Tracking mechanic baseline v1.0.
## Generates deterministic, frame-addressable smooth-pursuit state.
## The mechanic owns trajectory math; the presentation layer only renders the emitted state.

const BODY_RECT := Rect2(0.0, 144.0, 540.0, 672.0)
const DEFAULT_CENTER := Vector2(270.0, 480.0)
const DEFAULT_AMPLITUDE_X: float = 160.0
const DEFAULT_AMPLITUDE_Y: float = 210.0
const DEFAULT_FREQUENCY_X: float = 2.0
const DEFAULT_FREQUENCY_Y: float = 3.0
const DEFAULT_TRAVEL_CYCLES: float = 0.50
const DEFAULT_PHASE_X: float = 0.25
const DEFAULT_PHASE_Y: float = -0.65
const DEFAULT_TARGET_RADIUS: float = 12.0
const DEFAULT_TRAIL_LENGTH_FRAMES: int = 18
const MIN_EDGE_CLEARANCE: float = 36.0

func generate(frame_index: int, total_frames: int, drill_parameters: Dictionary) -> Dictionary:
	return generate_with_variation(frame_index, total_frames, drill_parameters, {})

func generate_with_variation(frame_index: int, total_frames: int, drill_parameters: Dictionary, variation: Dictionary) -> Dictionary:
	var progress := _resolve_progress(frame_index, total_frames)
	var exercise: Dictionary = drill_parameters.get("exercise_parameters", {})
	if not exercise is Dictionary:
		exercise = {}

	var trajectory := _resolve_trajectory(drill_parameters.get("trajectory", {}))
	var target_radius := float(trajectory.get("target_radius", DEFAULT_TARGET_RADIUS))
	var speed_multiplier := clampf(float(exercise.get("speed_multiplier", 1.0)), 0.1, 3.0)
	var pacing_mode := str(exercise.get("pacing_mode", "constant"))
	var paced_progress := _resolve_paced_progress(progress, pacing_mode)
	var phase_scale := TAU * float(trajectory.get("travel_cycles", DEFAULT_TRAVEL_CYCLES)) * speed_multiplier
	var phase := phase_scale * paced_progress

	var position := _sample_position(phase, trajectory)
	var velocity := _sample_velocity(phase, phase_scale, progress, pacing_mode, drill_parameters, trajectory)
	var trail_points := _build_history_trail(frame_index, total_frames, drill_parameters, speed_multiplier, pacing_mode, trajectory)

	var target := {
		"id": "t1",
		"x": position.x,
		"y": position.y,
		"radius": target_radius,
		"highlighted": true,
		"status": "active",
		"role": "tracking_target"
	}

	var stimulus := {
		"type": "dot",
		"radius": target_radius,
		"active": true,
		"x": position.x,
		"y": position.y
	}

	# The established tracking_variant stays in the cosmetic/presentation channel.
	# It intentionally does not alter mechanic truth in this baseline.
	var tracking_var := float(variation.get("tracking_variant", 0.0))

	return {
		"generator_type": "tracking",
		"progress": progress,
		"stimulus_state": stimulus,
		"target_states": [target],
		"distractor_states": [],
		"trajectory_state": {
			"type": "lissajous",
			"position": {"x": position.x, "y": position.y},
			"velocity": {"x": velocity.x, "y": velocity.y},
			"speed_px_per_second": velocity.length(),
			"phase": phase,
			"phase_progress": paced_progress,
			"x_frequency": float(trajectory.get("x_frequency", DEFAULT_FREQUENCY_X)),
			"y_frequency": float(trajectory.get("y_frequency", DEFAULT_FREQUENCY_Y)),
			"amplitude_x": float(trajectory.get("amplitude_x", DEFAULT_AMPLITUDE_X)),
			"amplitude_y": float(trajectory.get("amplitude_y", DEFAULT_AMPLITUDE_Y)),
			"center_x": float(trajectory.get("center_x", DEFAULT_CENTER.x)),
			"center_y": float(trajectory.get("center_y", DEFAULT_CENTER.y)),
			"trail_points": trail_points,
			"bounds": {
				"left": float(trajectory.get("center_x", DEFAULT_CENTER.x)) - float(trajectory.get("amplitude_x", DEFAULT_AMPLITUDE_X)),
				"right": float(trajectory.get("center_x", DEFAULT_CENTER.x)) + float(trajectory.get("amplitude_x", DEFAULT_AMPLITUDE_X)),
				"top": float(trajectory.get("center_y", DEFAULT_CENTER.y)) - float(trajectory.get("amplitude_y", DEFAULT_AMPLITUDE_Y)),
				"bottom": float(trajectory.get("center_y", DEFAULT_CENTER.y)) + float(trajectory.get("amplitude_y", DEFAULT_AMPLITUDE_Y)),
				"target_radius": target_radius
			}
		},
		"task_state": {
			"type": "tracking",
			"mode": "smooth_pursuit",
			"target_id": "t1"
		},
		"parameters": {
			"tracking_variant": tracking_var,
			"trajectory_profile": "lissajous_2_3_bounded_v1",
			"speed_multiplier": speed_multiplier,
			"pacing_mode": pacing_mode
		}
	}

func _resolve_trajectory(raw_trajectory: Variant) -> Dictionary:
	var raw: Dictionary = raw_trajectory if raw_trajectory is Dictionary else {}
	var center_x := clampf(float(raw.get("center_x", DEFAULT_CENTER.x)), BODY_RECT.position.x + MIN_EDGE_CLEARANCE, BODY_RECT.end.x - MIN_EDGE_CLEARANCE)
	var center_y := clampf(float(raw.get("center_y", DEFAULT_CENTER.y)), BODY_RECT.position.y + MIN_EDGE_CLEARANCE, BODY_RECT.end.y - MIN_EDGE_CLEARANCE)

	var max_amplitude_x := maxf(1.0, minf(center_x - (BODY_RECT.position.x + MIN_EDGE_CLEARANCE), (BODY_RECT.end.x - MIN_EDGE_CLEARANCE) - center_x))
	var max_amplitude_y := maxf(1.0, minf(center_y - (BODY_RECT.position.y + MIN_EDGE_CLEARANCE), (BODY_RECT.end.y - MIN_EDGE_CLEARANCE) - center_y))

	var amplitude_x := clampf(absf(float(raw.get("amplitude_x", DEFAULT_AMPLITUDE_X))), 1.0, max_amplitude_x)
	var amplitude_y := clampf(absf(float(raw.get("amplitude_y", DEFAULT_AMPLITUDE_Y))), 1.0, max_amplitude_y)
	var frequency_x := clampf(absf(float(raw.get("x_frequency", DEFAULT_FREQUENCY_X))), 1.0, 4.0)
	var frequency_y := clampf(absf(float(raw.get("y_frequency", DEFAULT_FREQUENCY_Y))), 1.0, 4.0)
	var travel_cycles := clampf(absf(float(raw.get("travel_cycles", DEFAULT_TRAVEL_CYCLES))), 0.1, 2.0)
	var target_radius := clampf(absf(float(raw.get("target_radius", DEFAULT_TARGET_RADIUS))), 8.0, 16.0)
	var trail_length := clampi(int(raw.get("trail_length_frames", DEFAULT_TRAIL_LENGTH_FRAMES)), 0, 24)
	var phase_x := float(raw.get("phase_x", DEFAULT_PHASE_X))
	var phase_y := float(raw.get("phase_y", DEFAULT_PHASE_Y))
	var trajectory_type := str(raw.get("type", "lissajous"))

	if trajectory_type != "lissajous":
		trajectory_type = "lissajous"

	return {
		"type": trajectory_type,
		"center_x": center_x,
		"center_y": center_y,
		"amplitude_x": amplitude_x,
		"amplitude_y": amplitude_y,
		"x_frequency": frequency_x,
		"y_frequency": frequency_y,
		"travel_cycles": travel_cycles,
		"phase_x": phase_x,
		"phase_y": phase_y,
		"target_radius": target_radius,
		"trail_length_frames": trail_length
	}

func _resolve_progress(frame_index: int, total_frames: int) -> float:
	if total_frames <= 1:
		return 0.0
	return clampf(float(frame_index) / float(maxi(1, total_frames - 1)), 0.0, 1.0)

func _resolve_paced_progress(progress: float, pacing_mode: String) -> float:
	match pacing_mode:
		"accelerating":
			return progress + (0.22 / TAU) * sin(TAU * progress)
		"pulsed":
			return progress + (0.16 / (2.0 * TAU)) * sin(2.0 * TAU * progress)
		_:
			return progress

func _sample_position(phase: float, trajectory: Dictionary) -> Vector2:
	return Vector2(
		float(trajectory.get("center_x", DEFAULT_CENTER.x)) + float(trajectory.get("amplitude_x", DEFAULT_AMPLITUDE_X)) * sin(float(trajectory.get("x_frequency", DEFAULT_FREQUENCY_X)) * phase + float(trajectory.get("phase_x", DEFAULT_PHASE_X))),
		float(trajectory.get("center_y", DEFAULT_CENTER.y)) + float(trajectory.get("amplitude_y", DEFAULT_AMPLITUDE_Y)) * sin(float(trajectory.get("y_frequency", DEFAULT_FREQUENCY_Y)) * phase + float(trajectory.get("phase_y", DEFAULT_PHASE_Y)))
	)

func _resolve_duration(drill_parameters: Dictionary) -> float:
	return maxf(0.001, float(drill_parameters.get("duration", 2.0)))

func _pacing_first_derivative(progress: float, pacing_mode: String) -> float:
	match pacing_mode:
		"accelerating":
			return 1.0 + 0.22 * cos(TAU * progress)
		"pulsed":
			return 1.0 + 0.16 * cos(2.0 * TAU * progress)
		_:
			return 1.0

func _sample_velocity(
	phase: float,
	phase_scale: float,
	progress: float,
	pacing_mode: String,
	drill_parameters: Dictionary,
	trajectory: Dictionary
) -> Vector2:
	var progress_clamped := clampf(progress, 0.0, 1.0)
	var d_paced := _pacing_first_derivative(progress_clamped, pacing_mode)
	var dphase_dt := phase_scale * d_paced / _resolve_duration(drill_parameters)
	var frequency_x := float(trajectory.get("x_frequency", DEFAULT_FREQUENCY_X))
	var frequency_y := float(trajectory.get("y_frequency", DEFAULT_FREQUENCY_Y))
	var amplitude_x := float(trajectory.get("amplitude_x", DEFAULT_AMPLITUDE_X))
	var amplitude_y := float(trajectory.get("amplitude_y", DEFAULT_AMPLITUDE_Y))
	var phase_x := float(trajectory.get("phase_x", DEFAULT_PHASE_X))
	var phase_y := float(trajectory.get("phase_y", DEFAULT_PHASE_Y))

	return Vector2(
		amplitude_x * frequency_x * cos(frequency_x * phase + phase_x) * dphase_dt,
		amplitude_y * frequency_y * cos(frequency_y * phase + phase_y) * dphase_dt
	)

func _build_history_trail(
	frame_index: int,
	total_frames: int,
	drill_parameters: Dictionary,
	speed_multiplier: float,
	pacing_mode: String,
	trajectory: Dictionary
) -> Array:
	var trail: Array = []
	var trail_length := int(trajectory.get("trail_length_frames", DEFAULT_TRAIL_LENGTH_FRAMES))
	var first_frame := maxi(0, frame_index - trail_length)
	for sample_frame in range(first_frame, frame_index + 1):
		var sample_progress := _resolve_progress(sample_frame, total_frames)
		var sample_paced := _resolve_paced_progress(sample_progress, pacing_mode)
		var sample_phase := TAU * float(trajectory.get("travel_cycles", DEFAULT_TRAVEL_CYCLES)) * speed_multiplier * sample_paced
		var sample_position := _sample_position(sample_phase, trajectory)
		trail.append({"x": sample_position.x, "y": sample_position.y})
	return trail
