# res://core/mechanics/parking/ParkingMechanicV2.gd
class_name ParkingMechanicV2
extends ChallengeMechanic

const DETERMINISTIC_LCG = preload("res://core/deterministic/DeterministicLCG.gd")

var _rng_context: MechanicRNGContext = null

var start_pos: Vector2 = Vector2(150.0, 960.0)
var target_pos: Vector2 = Vector2(850.0, 960.0)
var target_angle_rad: float = 0.0
var max_speed: float = 12.0
var steering_noise: float = 0.05
var tolerance_distance_px: float = 15.0
var tolerance_angle_rad: float = deg_to_rad(6.0)

# Variables de compatibilidad legacy
var _rng_index: int = 0
var _rng_version: String = "1.0"
var _legacy_seed: int = 0

# Estado estructural per-attempt congelado en setup()
var _dodge_offset: float = 0.0
var _save_offset: float = 0.0
var _overshoot_dist: float = 0.0

# Estado temporal per-frame congelado en prepare()
var _steering_noise_samples: Array[Vector2] = []

func set_rng_context(ctx: MechanicRNGContext) -> void:
	_rng_context = ctx

func requires_temporal_preparation() -> bool:
	return true

func setup(config: Dictionary) -> void:
	_is_setup = false
	_is_prepared = false
	_error_state = "OK"

	_steering_noise_samples.clear()
	_rng_index = 0

	# C6-F4.4 Phase 2: Canonical V2 is authoritative.
	# All mechanical parking/tolerance parameters migrated by F1.1 live under
	# simulation.parameters. Legacy V1 remains a compatibility fallback only.
	var simulation_cfg: Dictionary = config.get("simulation", {})
	var params: Dictionary = {}
	if simulation_cfg is Dictionary and simulation_cfg.get("parameters", {}) is Dictionary:
		params = simulation_cfg.get("parameters", {}).duplicate(true)
	else:
		params = config.get("difficulty", {}).duplicate(true)

	var parking_cfg: Dictionary = params.get("parking", params)
	if not parking_cfg is Dictionary:
		parking_cfg = {}

	var start_arr: Array = parking_cfg.get("start_position", [150.0, 960.0])
	start_pos = Vector2(float(start_arr[0]), float(start_arr[1]))

	var target_arr: Array = parking_cfg.get("target_position", [850.0, 960.0])
	target_pos = Vector2(float(target_arr[0]), float(target_arr[1]))

	target_angle_rad = deg_to_rad(float(parking_cfg.get("target_angle_deg", 0.0)))
	max_speed = float(parking_cfg.get("max_speed_px", 12.0))
	steering_noise = float(parking_cfg.get("steering_noise", 0.05))

	var tol: Dictionary = params.get("tolerance", {})
	if not tol is Dictionary:
		tol = {}
	tolerance_distance_px = float(tol.get("distance_px", 15.0))
	tolerance_angle_rad = deg_to_rad(float(tol.get("angle_deg", 6.0)))

	# C6-F4.4 Phase 2: seed and RNG version are also canonical V2 fields.
	# No RNG algorithm or stream semantics are changed here.
	var generation_cfg: Dictionary = config.get("generation", {})
	if simulation_cfg is Dictionary:
		_rng_version = str(simulation_cfg.get("rng_version", generation_cfg.get("rng_version", "1.0")))
		_legacy_seed = int(simulation_cfg.get("seed", generation_cfg.get("seed", 0)))
	else:
		_rng_version = str(generation_cfg.get("rng_version", "1.0"))
		_legacy_seed = int(generation_cfg.get("seed", 0))

	if _rng_version == "2.0":
		if _rng_context == null:
			_error_state = "MISSING_RNG_CONTEXT"
			return

		_dodge_offset = _rng_context.sample_float_range(RNGStreamRegistry.STREAM_PARKING_DODGE, 0, -140.0, 140.0)
		_save_offset = _rng_context.sample_float_range(RNGStreamRegistry.STREAM_PARKING_SAVE, 0, -50.0, 50.0)
		_overshoot_dist = _rng_context.sample_float_range(RNGStreamRegistry.STREAM_PARKING_OVERSHOOT, 0, 60.0, 120.0)

		if _rng_context.error_state != "OK":
			_error_state = _rng_context.error_state
			return
	else:
		_dodge_offset = _sample_legacy_range(_legacy_seed, -140.0, 140.0)
		_save_offset = _sample_legacy_range(_legacy_seed, -50.0, 50.0)
		_overshoot_dist = _sample_legacy_range(_legacy_seed, 60.0, 120.0)

	_is_setup = true

func prepare(total_frames: int) -> void:
	_is_prepared = false
	_steering_noise_samples.clear()

	if not _is_setup or _error_state != "OK":
		return

	if total_frames <= 0:
		_error_state = "INVALID_FRAME_COUNT"
		return

	if _rng_version == "2.0":
		if _rng_context == null:
			_error_state = "MISSING_RNG_CONTEXT"
			return

		for f in range(total_frames):
			var nx: float = _rng_context.sample_float_range(RNGStreamRegistry.STREAM_PARKING_STEERING, f * 2, -steering_noise * 8.0, steering_noise * 8.0)
			var ny: float = _rng_context.sample_float_range(RNGStreamRegistry.STREAM_PARKING_STEERING, f * 2 + 1, -steering_noise * 8.0, steering_noise * 8.0)
			_steering_noise_samples.append(Vector2(nx, ny))

		if _rng_context.error_state != "OK":
			_error_state = _rng_context.error_state
			_steering_noise_samples.clear()
			return
	else:
		for f in range(total_frames):
			var nx: float = _sample_legacy_range(_legacy_seed, -steering_noise * 8.0, steering_noise * 8.0)
			var ny: float = _sample_legacy_range(_legacy_seed, -steering_noise * 8.0, steering_noise * 8.0)
			_steering_noise_samples.append(Vector2(nx, ny))

	_is_prepared = true

func simulate(
	total_game_frames: int,
	local_seed: int,
	config: Dictionary
) -> SimulationResult:

	if not _is_setup or _error_state != "OK" or not _is_prepared:
		var err := SimulationResult.new()
		err.winning_frame = -1
		err.metadata = {
			"mechanic": "parking_v2",
			"rng_version": _rng_version,
			"error": _error_state
		}
		return err

	if _steering_noise_samples.size() != total_game_frames:
		var err := SimulationResult.new()
		err.winning_frame = -1
		err.metadata = {
			"mechanic": "parking_v2",
			"rng_version": _rng_version,
			"error": "TEMPORAL_BUFFER_SIZE_MISMATCH"
		}
		return err

	var result := SimulationResult.new()
	result.tolerance_threshold = tolerance_distance_px

	var p0: Vector2 = start_pos
	var target_center: Vector2 = target_pos
	var mid_vector: Vector2 = target_center - p0
	var perp_vector: Vector2 = Vector2(-mid_vector.y, mid_vector.x).normalized()

	var p3: Vector2 = target_center + mid_vector.normalized() * _overshoot_dist
	var p1: Vector2 = p0 + mid_vector * 0.30 + perp_vector * _dodge_offset
	var p2: Vector2 = p0 + mid_vector * 0.65 + perp_vector * _save_offset

	var prev_pos: Vector2 = p0
	var prev_angle: float = 0.0

	for f in range(total_game_frames):
		var snapshot := FrameSnapshot.new()

		var t_anim: float = float(f) / float(total_game_frames - 1) if total_game_frames > 1 else 0.0
		var t_curve: float = t_anim

		if t_anim > 0.4 and t_anim < 0.8:
			var local_t: float = (t_anim - 0.4) / 0.4
			t_curve = 0.4 + smoothstep(0.0, 1.0, local_t) * 0.35
		elif t_anim >= 0.8:
			t_curve = 0.75 + (t_anim - 0.8) * 1.25

		var noise_factor: float = sin(PI * t_anim)
		
		# SIMULACIÓN PURA SIN CONTEXTO RNG
		var raw_noise: Vector2 = _steering_noise_samples[f]
		var noise: Vector2 = raw_noise * noise_factor

		var pos: Vector2 = _calculate_bezier(p0, p1, p2, p3, t_curve) + noise
		var tangent: Vector2 = _calculate_bezier_tangent(p0, p1, p2, p3, t_curve)
		var current_angle: float = tangent.angle() if tangent.length_squared() > 0.0001 else prev_angle
		
		var angle_err: float = abs(angle_difference(current_angle, target_angle_rad))
		var real_velocity: float = pos.distance_to(prev_pos) if f > 0 else 0.0
		var dist_to_plaza: float = pos.distance_to(target_center)
		var braking_val: float = smoothstep(180.0, 0.0, dist_to_plaza) if t_anim > 0.4 else 0.0
		var steering_val: float = clamp(angle_difference(current_angle, prev_angle) * 10.0, -1.0, 1.0)
		var spatial_dist: float = dist_to_plaza
		var angle_penalty: float = max(0.0, angle_err - tolerance_angle_rad) * 100.0
		var effective_distance: float = spatial_dist + angle_penalty

		snapshot.position = pos
		snapshot.rotation = current_angle
		snapshot.scale = Vector2.ONE
		snapshot.opacity = 1.0

		snapshot.custom_data = {
			"success_distance": effective_distance,
			"spatial_distance": spatial_dist,
			"velocity": real_velocity,
			"angle_error": angle_err,
			"steering": steering_val,
			"braking": braking_val,
			"dodge_offset": _dodge_offset,
			"save_offset": _save_offset,
			"overshoot_dist": _overshoot_dist
		}

		result.frames.append(snapshot)
		prev_pos = pos
		prev_angle = current_angle

	result.metadata = {
		"seed_used": local_seed,
		"mechanic": "parking_v2",
		"rng_version": _rng_version,
		"dodge_offset": _dodge_offset,
		"save_offset": _save_offset,
		"overshoot_dist": _overshoot_dist
	}

	return result

func _sample_legacy_range(seed: int, from: float, to: float) -> float:
	var value: float = DETERMINISTIC_LCG.sample_float_range(seed, 0, _rng_index, from, to)
	_rng_index += 1
	return value

func _calculate_bezier(p0: Vector2, p1: Vector2, p2: Vector2, p3: Vector2, t: float) -> Vector2:
	var u: float = 1.0 - t
	var tt: float = t * t
	var uu: float = u * u
	var uuu: float = uu * u
	var ttt: float = tt * t

	var p: Vector2 = uuu * p0
	p += 3.0 * uu * t * p1
	p += 3.0 * u * tt * p2
	p += ttt * p3
	return p

func _calculate_bezier_tangent(p0: Vector2, p1: Vector2, p2: Vector2, p3: Vector2, t: float) -> Vector2:
	var u: float = 1.0 - t
	return 3.0 * u * u * (p1 - p0) + 6.0 * u * t * (p2 - p1) + 3.0 * t * t * (p3 - p2)