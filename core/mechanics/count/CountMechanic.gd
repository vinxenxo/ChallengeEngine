# res://core/mechanics/count/CountMechanic.gd
class_name CountMechanic
extends ChallengeMechanic

var min_value: int = 3
var max_value: int = 10
var target_count: int = 0
var precomputed_counts: Array[int] = []

var start_pos: Vector2 = Vector2(180.0, 850.0)
var step_x: float = 100.0

func setup(config_cache: Dictionary) -> void:
	_is_setup = false
	_error_state = "OK"

	var params: Dictionary = {}
	var simulation_cfg: Dictionary = config_cache.get("simulation", {})

	# 1. Autoridad: Canonical V2
	if simulation_cfg.has("parameters"):
		var simulation_params = simulation_cfg.get("parameters", {})
		if simulation_params is Dictionary:
			# Extrae "count" si existe, si no, usa el propio simulation_params aplanado
			var v2_count = simulation_params.get("count", simulation_params)
			if v2_count is Dictionary and not v2_count.is_empty():
				params = v2_count.duplicate(true)
			else:
				params = simulation_params.duplicate(true)
	
	# 2. Fallback: Legacy V1
	else:
		var difficulty_cfg: Dictionary = config_cache.get("difficulty", {})
		var content_cfg: Dictionary = config_cache.get("content", {})
		
		var diff_count = difficulty_cfg.get("count", difficulty_cfg)
		params = diff_count.duplicate(true) if diff_count is Dictionary else {}
		
		# Fusionar metadata/content histórico
		if content_cfg is Dictionary:
			for key in content_cfg.keys():
				if not params.has(key):
					params[key] = content_cfg[key]

	# Asignación de variables desde el diccionario resuelto
	min_value = int(params.get("min_value", 3))
	max_value = int(params.get("max_value", 10))

	if min_value >= max_value:
		_error_state = "INVALID_COUNT_RANGE"
		_is_setup = false
		return

	var raw_start = params.get("start_pos", [])
	if raw_start is Array and raw_start.size() >= 2:
		start_pos = Vector2(float(raw_start[0]), float(raw_start[1]))

	step_x = float(params.get("step_x", 100.0))

	# Autoridad de semilla: simulation.seed para V2, fallback a generation.seed
	var seed_val: int = 12345
	if simulation_cfg.has("seed"):
		seed_val = int(simulation_cfg.get("seed"))
	else:
		var generation_cfg: Dictionary = config_cache.get("generation", {})
		seed_val = int(generation_cfg.get("seed", 12345))

	var range_size: int = (max_value - min_value) + 1
	target_count = min_value + (seed_val % range_size)

	_is_setup = true
	_error_state = "OK"

func requires_temporal_preparation() -> bool:
	return true

func prepare(game_frames: int) -> void:
	precomputed_counts.clear()

	if game_frames <= 0:
		_error_state = "INVALID_GAME_FRAMES"
		_is_prepared = false
		return

	var range_size: int = (max_value - min_value) + 1
	var cycle_duration: int = max(20, int(game_frames / (range_size * 2)))
	var lock_start_frame: int = int(game_frames * 0.75)

	for f: int in range(game_frames):
		var current_display: int = 0

		if f >= lock_start_frame:
			current_display = target_count
		else:
			var step_index: int = int(f / cycle_duration) % range_size
			current_display = min_value + step_index

		precomputed_counts.append(current_display)

	_is_prepared = true
	_error_state = "OK"

func simulate(
	game_frames: int,
	seed: int,
	config_cache: Dictionary
) -> SimulationResult:

	var result: SimulationResult = SimulationResult.new()
	var frames: Array[FrameSnapshot] = []

	var lock_start_frame: int = int(game_frames * 0.75)

	if precomputed_counts.size() != game_frames:
		result.error_state = "INVALID_COUNT_BUFFER"
		return result

	for f: int in range(game_frames):
		var displayed: int = precomputed_counts[f]
		var success_distance: float = 0.0

		if displayed == target_count:
			success_distance = 0.0
		else:
			success_distance = 1.0

		var snapshot: FrameSnapshot = FrameSnapshot.new()

		var offset_index: float = float(displayed - min_value)
		snapshot.position = Vector2(start_pos.x + (offset_index * step_x), start_pos.y)
		
		snapshot.rotation = 0.0
		snapshot.scale = Vector2.ONE
		snapshot.opacity = 1.0

		snapshot.custom_data = {
			"displayed_count": displayed,
			"target_count": target_count,
			"success_distance": success_distance
		}

		frames.append(snapshot)

	result.frames = frames

	result.winning_frame = lock_start_frame
	result.minimum_distance = 0.0
	result.score = 1.0
	result.tolerance_threshold = 0.0
	result.is_self_scored = true

	result.metadata = {
		"target_count": target_count,
		"min_value": min_value,
		"max_value": max_value,
		"close_calls": 1,
		"rng_version": "2.0"
	}

	result.error_state = "OK"

	return result

func validate_contract(game_frames: int) -> Dictionary:
	if min_value >= max_value:
		return {
			"is_valid": false,
			"error_code": "INVALID_COUNT_RANGE",
			"message": "min_value debe ser menor que max_value."
		}

	if precomputed_counts.size() != game_frames:
		return {
			"is_valid": false,
			"error_code": "INVALID_COUNT_BUFFER",
			"message": "La secuencia temporal no coincide con game_frames."
		}

	if target_count < min_value or target_count > max_value:
		return {
			"is_valid": false,
			"error_code": "INVALID_TARGET_COUNT",
			"message": "El target_count está fuera del rango permitido."
		}

	return {
		"is_valid": true,
		"error_code": "OK",
		"message": ""
	}