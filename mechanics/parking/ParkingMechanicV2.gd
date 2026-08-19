class_name ParkingMechanicV2
extends ChallengeMechanic

const REGISTRY = preload("res://core/deterministic/RNGStreamRegistry.gd")

# Inyección de dependencias requerida por DDI
var rng_context: MechanicRNGContext

# Estado estructural
var start_pos: Vector2 = Vector2(150.0, 960.0)
var target_pos: Vector2 = Vector2(850.0, 960.0)
var target_angle_rad: float = 0.0
var max_speed: float = 12.0
var steering_noise: float = 0.05
var tolerance_distance_px: float = 15.0
var tolerance_angle_rad: float = deg_to_rad(6.0)

func setup(config: Dictionary) -> void:
	var diff: Dictionary = config.get("difficulty", {})
	var parking_cfg: Dictionary = diff.get("parking", {})

	var start_arr: Array = parking_cfg.get("start_position", [150.0, 960.0])
	start_pos = Vector2(float(start_arr[0]), float(start_arr[1]))

	var target_arr: Array = parking_cfg.get("target_position", [850.0, 960.0])
	target_pos = Vector2(float(target_arr[0]), float(target_arr[1]))

	target_angle_rad = deg_to_rad(float(parking_cfg.get("target_angle_deg", 0.0)))
	max_speed = float(parking_cfg.get("max_speed_px", 12.0))
	steering_noise = float(parking_cfg.get("steering_noise", 0.05))

	var tol: Dictionary = diff.get("tolerance", {})
	tolerance_distance_px = float(tol.get("distance_px", 15.0))
	tolerance_angle_rad = deg_to_rad(float(tol.get("angle_deg", 6.0)))

func simulate(total_game_frames: int, local_seed: int, config: Dictionary) -> SimulationResult:
	var result: SimulationResult = SimulationResult.new()
	
	if rng_context == null:
		# Violación de la inyección de dependencias
		return result
		
	setup(config)
	result.tolerance_threshold = tolerance_distance_px

	var p0: Vector2 = start_pos
	var target_center: Vector2 = target_pos
	var mid_vector: Vector2 = target_center - p0
	var perp_vector: Vector2 = Vector2(-mid_vector.y, mid_vector.x).normalized()

	# 1. PARÁMETROS GEOMÉTRICOS DE GENERACIÓN (Consumo discreto en index 0)
	var dodge_offset = rng_context.sample_float_range(
		REGISTRY.STREAM_PARKING_DODGE, 
		0, 
		-140.0, 
		140.0
	)
	if rng_context.error_state != "OK":
		return result

	var save_offset = rng_context.sample_float_range(
		REGISTRY.STREAM_PARKING_SAVE, 
		0, 
		-50.0, 
		50.0
	)
	if rng_context.error_state != "OK":
		return result

	var overshoot_dist = rng_context.sample_float_range(
		REGISTRY.STREAM_PARKING_OVERSHOOT, 
		0, 
		60.0, 
		120.0
	)
	if rng_context.error_state != "OK":
		return result

	# Puntos de Control Bézier
	var p3: Vector2 = target_center + mid_vector.normalized() * overshoot_dist
	var p1: Vector2 = p0 + mid_vector * 0.30 + perp_vector * dodge_offset
	var p2: Vector2 = p0 + mid_vector * 0.65 + perp_vector * save_offset

	var prev_pos: Vector2 = p0
	var prev_angle: float = 0.0

	# 2. SIMULACIÓN TEMPORAL POR FRAME
	for f in range(total_game_frames):
		var snapshot: FrameSnapshot = FrameSnapshot.new()
		
		# t_anim lineal estricto
		var t_anim: float = float(f) / float(total_game_frames - 1) if total_game_frames > 1 else 0.0
		
		# t_curve Piecewise determinista
		var t_curve: float = t_anim
		if t_anim > 0.4 and t_anim < 0.8:
			var local_t: float = (t_anim - 0.4) / 0.4
			t_curve = 0.4 + smoothstep(0.0, 1.0, local_t) * 0.35
		elif t_anim >= 0.8:
			t_curve = 0.75 + (t_anim - 0.8) * 1.25

		# 3. PERTURBACIÓN (STEERING NOISE) POR FRAME
		var noise_x = rng_context.sample_float_range(
			REGISTRY.STREAM_PARKING_STEERING, 
			f * 2, 
			-steering_noise * 8.0, 
			steering_noise * 8.0
		)
		if rng_context.error_state != "OK":
			return SimulationResult.new() # Abortar devolviendo resultado vacío

		var noise_y = rng_context.sample_float_range(
			REGISTRY.STREAM_PARKING_STEERING, 
			f * 2 + 1, 
			-steering_noise * 8.0, 
			steering_noise * 8.0
		)
		if rng_context.error_state != "OK":
			return SimulationResult.new() # Abortar devolviendo resultado vacío

		var noise_factor: float = sin(PI * t_anim)
		var noise: Vector2 = Vector2(noise_x * noise_factor, noise_y * noise_factor)

		# 4. MATEMÁTICA Y GEOMETRÍA DERIVADA
		var pos: Vector2 = _calculate_bezier(p0, p1, p2, p3, t_curve) + noise
		var tangent: Vector2 = _calculate_bezier_tangent(p0, p1, p2, p3, t_curve)

		var current_angle: float = tangent.angle() if tangent.length_squared() > 0.0001 else prev_angle
		var angle_err: float = abs(angle_difference(current_angle, target_angle_rad))
		
		var real_velocity: float = pos.distance_to(prev_pos) if f > 0 else 0.0
		var spatial_dist: float = pos.distance_to(target_center)

		# Controles simulados sin RNG adicional
		var braking_val: float = smoothstep(180.0, 0.0, spatial_dist) if t_anim > 0.4 else 0.0
		var steering_val: float = clamp(angle_difference(current_angle, prev_angle) * 10.0, -1.0, 1.0)

		# Métrica Definitiva de Evaluación V2.0
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
			"dodge_offset": dodge_offset,
			"save_offset": save_offset,
			"overshoot_dist": overshoot_dist
		}

		result.frames.append(snapshot)
		prev_pos = pos
		prev_angle = current_angle

	result.metadata = {
		"seed_used": local_seed,
		"mechanic": "parking_v2",
		"rng_version": "2.0",
		"dodge_offset": dodge_offset,
		"save_offset": save_offset,
		"overshoot_dist": overshoot_dist
	}

	return result

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