class_name CatchMechanic
extends ChallengeMechanic

var _rng_context: MechanicRNGContext = null
var _is_setup: bool = false

func set_rng_context(ctx: MechanicRNGContext) -> void:
	_rng_context = ctx

func setup(config: Dictionary) -> void:
	_is_setup = true

func simulate(total_frames: int, initial_seed: int, config: Dictionary) -> SimulationResult:
	if not _is_setup or _rng_context == null:
		return null

	var catch_cfg: Dictionary = config.get("difficulty", {}).get("catch", {})
	
	# Parámetros de configuración base del escenario cinemático
	var catcher_orig_arr: Array = catch_cfg.get("catcher_origin", [540.0, 1700.0])
	var catcher_dir_arr: Array = catch_cfg.get("catcher_direction", [0.0, -1.0])
	var catcher_speed_base: float = float(catch_cfg.get("catcher_speed_base", 6.0))
	
	var target_orig_arr: Array = catch_cfg.get("target_origin", [540.0, 400.0])
	var target_direction_arr: Array = catch_cfg.get("target_direction", [0.0, 1.0])
	var target_speed_base: float = float(catch_cfg.get("target_speed_base", 2.5))
	
	var catch_radius: float = maxf(0.001, float(catch_cfg.get("catch_radius", 45.0)))

	var c0: Vector2 = Vector2(float(catcher_orig_arr[0]), float(catcher_orig_arr[1]))
	var t0: Vector2 = Vector2(float(target_orig_arr[0]), float(target_orig_arr[1]))
	
	var dir_c: Vector2 = Vector2(float(catcher_dir_arr[0]), float(catcher_dir_arr[1]))
	var dir_t: Vector2 = Vector2(float(target_direction_arr[0]), float(target_direction_arr[1]))

	# Validación estricta de normalización y magnitudes de vectores directores
	if dir_c.length() == 0.0 or dir_t.length() == 0.0 or catcher_speed_base < 0.0 or target_speed_base < 0.0:
		var err_res = SimulationResult.new()
		err_res.winning_frame = -1
		return err_res

	var u_c: Vector2 = dir_c.normalized()
	var u_t: Vector2 = dir_t.normalized()

	# 1. Stream 100 (Índice 0): Target Motion δ_target ∈ [-0.20, 0.20]
	var delta_target: float = _rng_context.sample_float_range(100, 0, -0.20, 0.20)
	# 2. Stream 110 (Índice 0): Pursuer Bias δ_bias ∈ [-0.15, 0.15]
	var delta_bias: float = _rng_context.sample_float_range(110, 0, -0.15, 0.15)
	# 3. Stream 120 (Índice 0): Initial Phase Δx_phase ∈ [-50.0, 50.0]
	var delta_phase_x: float = _rng_context.sample_float_range(120, 0, -50.0, 50.0)

	# Si ocurrió un error DDI (ej. stream no autorizado), abortamos la simulación
	if _rng_context.error_state != "OK":
		var err_res = SimulationResult.new()
		err_res.winning_frame = -1
		return err_res

	var v_t_eff: float = target_speed_base * (1.0 + delta_target)
	var v_c_eff: float = catcher_speed_base * (1.0 + delta_bias)

	var v_t: Vector2 = u_t * v_t_eff
	var v_c: Vector2 = u_c * v_c_eff

	var t0_prime: Vector2 = t0 + Vector2(delta_phase_x, 0.0)

	var frames: Array[FrameSnapshot] = []
	var min_dist: float = INF
	var winning_frame: int = -1

	# Generación de la cinemática discreta por fotograma
	for f in range(total_frames):
		var p_t: Vector2 = t0_prime + (v_t * float(f))
		var p_c: Vector2 = c0 + (v_c * float(f))
		var d_f: float = p_c.distance_to(p_t)

		var snap: FrameSnapshot = FrameSnapshot.new()
		snap.position = p_c
		snap.rotation = 0.0
		snap.scale = Vector2.ONE
		snap.opacity = 1.0
		frames.append(snap)

		# Argmin discreto estricto (< garantiza desempate manteniendo el primer índice)
		if d_f < min_dist:
			min_dist = d_f
			winning_frame = f

	# Cálculo de métricas contractuales de salida
	var captured: bool = min_dist <= catch_radius
	var score: float = clampf(1.0 - (min_dist / catch_radius), 0.0, 1.0)
	var closing_velocity: float = (v_c - v_t).length()

	# Segunda pasada para close_calls (d_f <= catch_radius * 3.5, excluyendo estrictamente winning_frame)
	var close_threshold: float = catch_radius
	var close_calls: int = 0
	for f in range(total_frames):
		if f != winning_frame:
			var p_t_f: Vector2 = t0_prime + (v_t * float(f))
			var p_c_f: Vector2 = c0 + (v_c * float(f))
			var d_f: float = p_c_f.distance_to(p_t_f)
			if d_f <= close_threshold:
				close_calls += 1

	var result: SimulationResult = SimulationResult.new()
	result.frames = frames
	result.winning_frame = winning_frame
	result.minimum_distance = min_dist
	result.score = score
	result.tolerance_threshold = catch_radius
	
	result.metadata = {
		"captured": captured,
		"closing_velocity": closing_velocity,
		"close_calls": close_calls,
		"delta_target": delta_target,
		"delta_bias": delta_bias,
		"delta_phase_x": delta_phase_x
	}
	return result