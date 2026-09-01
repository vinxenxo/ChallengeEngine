class_name CountMechanic
extends ChallengeMechanic

var min_value: int = 3
var max_value: int = 10
var target_count: int = 0
var precomputed_counts: Array[int] = []

var start_pos: Vector2 = Vector2(180.0, 850.0)
var step_x: float = 100.0

func setup(config_cache: Dictionary) -> void:
	var diff_cfg: Dictionary = config_cache.get("difficulty", {}).get("count", {})

	min_value = int(diff_cfg.get("min_value", 3))
	max_value = int(diff_cfg.get("max_value", 10))

	if min_value >= max_value:
		_error_state = "INVALID_COUNT_RANGE"
		_is_setup = false
		return

	var raw_start = diff_cfg.get("start_pos", [])
	if raw_start is Array and raw_start.size() >= 2:
		start_pos = Vector2(float(raw_start[0]), float(raw_start[1]))

	step_x = float(diff_cfg.get("step_x", 100.0))

	var generation_cfg: Dictionary = config_cache.get("generation", {})
	var seed_val: int = int(generation_cfg.get("seed", 12345))

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