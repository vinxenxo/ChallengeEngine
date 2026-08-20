class_name HitMechanic
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

	var hit_cfg: Dictionary = config.get("difficulty", {}).get("hit", {})
	var origin_arr: Array = hit_cfg.get("origin", [540.0, 1500.0])
	var target_arr: Array = hit_cfg.get("target", [540.0, 300.0])
	var speed_base: float = float(hit_cfg.get("speed_base", 3.5))
	var hitbox_radius: float = maxf(0.001, float(hit_cfg.get("hitbox_radius", 30.0)))

	var origin: Vector2 = Vector2(float(origin_arr[0]), float(origin_arr[1]))
	var base_target: Vector2 = Vector2(float(target_arr[0]), float(target_arr[1]))

	# 1. Stream 90 (Índices 0, 1): Target Offset (Regla 1)
	var dx: float = _rng_context.sample_float_range(90, 0, -60.0, 60.0)
	var dy: float = _rng_context.sample_float_range(90, 1, -60.0, 60.0)
	var target_prime: Vector2 = base_target + Vector2(dx, dy)

	# 2. Vector Director Normalizado
	var direction: Vector2 = target_prime - origin
	var u: Vector2 = direction.normalized() if direction.length() > 0.0 else Vector2.UP

	# 3. Stream 70 (Índice 0): Speed Variance (Regla 2)
	var dv: float = _rng_context.sample_float_range(70, 0, -0.20, 0.20)
	var v: float = speed_base * (1.0 + dv)

	var frames: Array[FrameSnapshot] = []
	var min_dist: float = INF
	var winning_frame: int = -1

	# Generación de trayectoria (Regla 4: f = 0..total_frames-1)
	for f in range(total_frames):
		# Stream 80 (Índice f): Trajectory Noise (Regla 3)
		var eps_f: float = _rng_context.sample_float_range(80, f, -4.0, 4.0)
		
		# Ecuación de posición discreta y distancia
		var p_f: Vector2 = origin + (u * v * float(f)) + Vector2(0.0, eps_f)
		var d_f: float = p_f.distance_to(target_prime)
		
		var snap: FrameSnapshot = FrameSnapshot.new()
		snap.position = p_f
		snap.rotation = 0.0
		snap.scale = Vector2.ONE
		snap.opacity = 1.0
		frames.append(snap)
		
		# Argmin discreto estricto. El "<" garantiza desempate manteniendo el primer índice (Regla 5)
		if d_f < min_dist:
			min_dist = d_f
			winning_frame = f

	# Si ocurrió un error RNG (ej. consumo no autorizado), abortamos cálculo de validación
	if _rng_context.error_state != "OK":
		var err_result = SimulationResult.new()
		err_result.winning_frame = -1
		err_result.frames = frames
		return err_result

	# Cálculo de close_calls en una segunda pasada aislando el winning_frame (Regla 6)
	var close_calls: int = 0
	for f in range(total_frames):
		if f != winning_frame:
			var d_f: float = frames[f].position.distance_to(target_prime)
			if d_f <= hitbox_radius:
				close_calls += 1

	# Cálculo de score
	var score: float = clampf(1.0 - (min_dist / hitbox_radius), 0.0, 1.0)

	var result: SimulationResult = SimulationResult.new()
	result.frames = frames
	result.winning_frame = winning_frame
	
	# Exposición explícita de propiedades raíz requeridas por ChallengeValidator
	result.minimum_distance = min_dist
	result.score = score
	result.tolerance_threshold = hitbox_radius

	result.metadata = {
		"minimum_distance": min_dist,
		"score": score,
		"impact_velocity": v,
		"close_calls": close_calls,
		"target_prime_x": target_prime.x,
		"target_prime_y": target_prime.y
	}
	return result