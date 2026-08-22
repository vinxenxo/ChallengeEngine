class_name HitMechanic
extends ChallengeMechanic

var _rng_context: MechanicRNGContext = null

# Estado estructural per-attempt congelado en setup() — C3-B1
var _origin: Vector2 = Vector2.ZERO
var _target: Vector2 = Vector2.ZERO
var _target_prime: Vector2 = Vector2.ZERO
var _direction: Vector2 = Vector2.ZERO
var _velocity: float = 3.5
var _hitbox_radius: float = 30.0
var _speed_base: float = 3.5

# Estado temporal per-frame congelado en prepare() — C3-B2
var _trajectory_noise: Array[float] = []

func set_rng_context(ctx: MechanicRNGContext) -> void:
	_rng_context = ctx

func requires_temporal_preparation() -> bool:
	return true

func setup(config: Dictionary) -> void:
	_is_setup = false
	_is_prepared = false
	_error_state = "OK"

	# Reseteo estricto por intento
	_origin = Vector2.ZERO
	_target = Vector2.ZERO
	_target_prime = Vector2.ZERO
	_direction = Vector2.ZERO
	_velocity = 3.5
	_trajectory_noise.clear()

	if _rng_context == null:
		_error_state = "MISSING_RNG_CONTEXT"
		return

	var hit_cfg: Dictionary = config.get("difficulty", {}).get("hit", {})

	var origin_arr = hit_cfg.get("origin", [540.0, 1500.0])
	var target_arr = hit_cfg.get("target", [540.0, 300.0])

	_speed_base = float(hit_cfg.get("speed_base", 3.5))
	_hitbox_radius = maxf(
		float(hit_cfg.get("hitbox_radius", 30.0)),
		0.001
	)

	_origin = Vector2(
		float(origin_arr[0]),
		float(origin_arr[1])
	)

	_target = Vector2(
		float(target_arr[0]),
		float(target_arr[1])
	)

	# ============================================================
	# C3-B1 — Stream 90: Target Offset
	# ORDEN INNEGOCIABLE: PRIMERO
	# ============================================================

	var dx = _rng_context.sample_float_range(
		RNGStreamRegistry.STREAM_HIT_TARGET_OFFSET,
		0,
		-60.0,
		60.0
	)

	var dy = _rng_context.sample_float_range(
		RNGStreamRegistry.STREAM_HIT_TARGET_OFFSET,
		1,
		-60.0,
		60.0
	)

	_target_prime = _target + Vector2(dx, dy)
	_direction = (_target_prime - _origin).normalized()

	# ============================================================
	# C3-B1 — Stream 70: Speed Variance
	# ORDEN INNEGOCIABLE: SEGUNDO
	# ============================================================

	var dv = _rng_context.sample_float_range(
		RNGStreamRegistry.STREAM_HIT_SPEED_VARIANCE,
		0,
		-0.2,
		0.2
	)

	_velocity = _speed_base * (1.0 + dv)

	if _rng_context.error_state != "OK":
		_error_state = _rng_context.error_state
		return

	_is_setup = true


func prepare(total_frames: int) -> void:
	_is_prepared = false
	_trajectory_noise.clear()

	if not _is_setup or _error_state != "OK":
		return

	if total_frames <= 0:
		_error_state = "INVALID_FRAME_COUNT"
		return

	if _rng_context == null:
		_error_state = "MISSING_RNG_CONTEXT"
		return

	# ============================================================
	# C3-B2 — Stream 80: Trajectory Noise
	# Consumo exclusivamente indexado por frame.
	# Rango congelado: [-4.0, +4.0]
	# ============================================================

	for f in range(total_frames):
		var eps_f: float = _rng_context.sample_float_range(
			RNGStreamRegistry.STREAM_HIT_TRAJECTORY_NOISE,
			f,
			-4.0,
			4.0
		)

		_trajectory_noise.append(eps_f)

	if _rng_context.error_state != "OK":
		_error_state = _rng_context.error_state
		_is_prepared = false
		return

	_is_prepared = true


func simulate(
	total_frames: int,
	initial_seed: int,
	config: Dictionary
) -> SimulationResult:

	# ============================================================
	# C3-B2 — SIMULATE PURA
	# Cero RNG.
	# Cero acceso al contexto.
	# Cero materialización estructural.
	# ============================================================

	if not _is_setup or _error_state != "OK" or not _is_prepared:
		var err = SimulationResult.new()
		err.winning_frame = -1
		err.metadata["error"] = _error_state
		return err

	var frames: Array[FrameSnapshot] = []
	var min_dist: float = INF
	var winning_frame: int = -1

	for f in range(total_frames):
		var eps_f: float = _trajectory_noise[f]

		var p_f = (
			_origin
			+ (_direction * _velocity * float(f))
			+ Vector2(0.0, eps_f)
		)

		var d_f = p_f.distance_to(_target_prime)

		if d_f < min_dist:
			min_dist = d_f
			winning_frame = f

		var snap = FrameSnapshot.new()
		snap.position = p_f
		snap.custom_data = {
			"target_position": _target_prime
		}

		frames.append(snap)

	# Segunda pasada original para close_calls.
	# El winning_frame se excluye explícitamente.
	var close_calls: int = 0

	for f in range(total_frames):
		if f != winning_frame:
			var d_f = frames[f].position.distance_to(_target_prime)

			if d_f <= _hitbox_radius:
				close_calls += 1

	var captured: bool = min_dist <= _hitbox_radius

	var score: float = clampf(
		1.0 - (min_dist / _hitbox_radius),
		0.0,
		1.0
	)

	var result = SimulationResult.new()

	result.frames = frames
	result.winning_frame = winning_frame
	result.minimum_distance = min_dist
	result.score = score
	result.tolerance_threshold = _hitbox_radius

	result.metadata = {
		"captured": captured,
		"initial_seed": initial_seed,
		"close_calls": close_calls,
		"impact_velocity": _velocity,
		"target_prime_x": _target_prime.x,
		"target_prime_y": _target_prime.y
	}

	return result