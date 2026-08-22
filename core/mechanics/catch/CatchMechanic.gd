class_name CatchMechanic
extends ChallengeMechanic

var _rng_context: MechanicRNGContext = null

# Estado estructural per-attempt congelado en setup()
var _c0: Vector2 = Vector2.ZERO
var _t0: Vector2 = Vector2.ZERO
var _u_c: Vector2 = Vector2.UP
var _u_t: Vector2 = Vector2.DOWN
var _catcher_speed_base: float = 6.0
var _target_speed_base: float = 2.5
var _catch_radius: float = 45.0

var _delta_target: float = 0.0
var _delta_bias: float = 0.0
var _delta_phase_x: float = 0.0

func set_rng_context(ctx: MechanicRNGContext) -> void:
	_rng_context = ctx

func requires_temporal_preparation() -> bool:
	return false

func setup(config: Dictionary) -> void:
	_is_setup = false
	_is_prepared = false
	_error_state = "OK"

	# Axioma 4: Amnesia por intento
	_c0 = Vector2.ZERO
	_t0 = Vector2.ZERO
	_u_c = Vector2.UP
	_u_t = Vector2.DOWN
	_catcher_speed_base = 6.0
	_target_speed_base = 2.5
	_catch_radius = 45.0
	
	_delta_target = 0.0
	_delta_bias = 0.0
	_delta_phase_x = 0.0

	if _rng_context == null:
		_error_state = "MISSING_RNG_CONTEXT"
		return

	var catch_cfg: Dictionary = config.get("difficulty", {}).get("catch", {})
	
	var catcher_orig_arr: Array = catch_cfg.get("catcher_origin", [540.0, 1700.0])
	var catcher_dir_arr: Array = catch_cfg.get("catcher_direction", [0.0, -1.0])
	_catcher_speed_base = float(catch_cfg.get("catcher_speed_base", 6.0))
	
	var target_orig_arr: Array = catch_cfg.get("target_origin", [540.0, 400.0])
	var target_direction_arr: Array = catch_cfg.get("target_direction", [0.0, 1.0])
	_target_speed_base = float(catch_cfg.get("target_speed_base", 2.5))
	
	_catch_radius = maxf(0.001, float(catch_cfg.get("catch_radius", 45.0)))

	_c0 = Vector2(float(catcher_orig_arr[0]), float(catcher_orig_arr[1]))
	_t0 = Vector2(float(target_orig_arr[0]), float(target_orig_arr[1]))
	
	var dir_c: Vector2 = Vector2(float(catcher_dir_arr[0]), float(catcher_dir_arr[1]))
	var dir_t: Vector2 = Vector2(float(target_direction_arr[0]), float(target_direction_arr[1]))

	if dir_c.length() == 0.0 or dir_t.length() == 0.0 or _catcher_speed_base < 0.0 or _target_speed_base < 0.0:
		_error_state = "INVALID_CONFIG_PARAMETERS"
		return

	_u_c = dir_c.normalized()
	_u_t = dir_t.normalized()

	# C3-F-A: Migración de consumo RNG a fase de setup estructural
	_delta_target = _rng_context.sample_float_range(100, 0, -0.20, 0.20)
	_delta_bias = _rng_context.sample_float_range(110, 0, -0.15, 0.15)
	_delta_phase_x = _rng_context.sample_float_range(120, 0, -50.0, 50.0)

	if _rng_context.error_state != "OK":
		_error_state = _rng_context.error_state
		return

	# C3-F Modelo A: Mecánicas estructurales completan el ciclo temporal aquí
	_is_setup = true
	_is_prepared = true

func simulate(total_frames: int, initial_seed: int, _config: Dictionary) -> SimulationResult:
	
	# Axioma 3: Secuencialidad Estricta
	if not _is_setup or _error_state != "OK" or not _is_prepared:
		var err_res = SimulationResult.new()
		err_res.winning_frame = -1
		err_res.metadata["error"] = _error_state
		return err_res

	# SIMULACIÓN PURA - Cero RNG
	var v_t_eff: float = _target_speed_base * (1.0 + _delta_target)
	var v_c_eff: float = _catcher_speed_base * (1.0 + _delta_bias)

	var v_t: Vector2 = _u_t * v_t_eff
	var v_c: Vector2 = _u_c * v_c_eff
	var t0_prime: Vector2 = _t0 + Vector2(_delta_phase_x, 0.0)

	var frames: Array[FrameSnapshot] = []
	var min_dist: float = INF
	var winning_frame: int = -1

	for f in range(total_frames):
		var p_t: Vector2 = t0_prime + (v_t * float(f))
		var p_c: Vector2 = _c0 + (v_c * float(f))
		var d_f: float = p_c.distance_to(p_t)

		var snap: FrameSnapshot = FrameSnapshot.new()
		snap.position = p_c
		snap.rotation = 0.0
		snap.scale = Vector2.ONE
		snap.opacity = 1.0
		
		snap.custom_data = {
			"target_position": p_t
		}
		
		frames.append(snap)

		if d_f < min_dist:
			min_dist = d_f
			winning_frame = f

	var captured: bool = min_dist <= _catch_radius
	var score: float = clampf(1.0 - (min_dist / _catch_radius), 0.0, 1.0)
	var closing_velocity: float = (v_c - v_t).length()

	var close_threshold: float = _catch_radius
	var close_calls: int = 0
	for f in range(total_frames):
		if f != winning_frame:
			var p_t_f: Vector2 = t0_prime + (v_t * float(f))
			var p_c_f: Vector2 = _c0 + (v_c * float(f))
			var d_f: float = p_c_f.distance_to(p_t_f)
			if d_f <= close_threshold:
				close_calls += 1

	var result: SimulationResult = SimulationResult.new()
	result.frames = frames
	result.winning_frame = winning_frame
	result.minimum_distance = min_dist
	result.score = score
	result.tolerance_threshold = _catch_radius
	
	result.metadata = {
		"captured": captured,
		"closing_velocity": closing_velocity,
		"close_calls": close_calls,
		"delta_target": _delta_target,
		"delta_bias": _delta_bias,
		"delta_phase_x": _delta_phase_x
	}
	return result