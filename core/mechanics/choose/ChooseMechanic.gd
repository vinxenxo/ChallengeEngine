class_name ChooseMechanic
extends ChallengeMechanic


var options_count: int = 3
var options_positions: Array[Vector2] = []
var winning_option: int = 0
var precomputed_selections: Array[int] = []

var _params: Dictionary = {}
var _config: Dictionary = {}


func setup(config: Dictionary) -> void:
	_is_setup = false
	_error_state = "OK"
	
	_config = config.duplicate(true)

	var params: Dictionary = {}

	# 1. Autoridad: Canonical V2
	if config.has("simulation") and config.get("simulation", {}).has("parameters"):
		var v2_params: Dictionary = config["simulation"]["parameters"]
		params = v2_params.get("choose", v2_params)
	
	# 2. Fallback: Legacy V1
	else:
		var difficulty_cfg: Dictionary = config.get("difficulty", {})
		var content_cfg: Dictionary = config.get("content", {})
		
		var diff_choose = difficulty_cfg.get("choose", difficulty_cfg)
		params = diff_choose.duplicate(true) if diff_choose is Dictionary else {}
		
		# Fusionar metadata/content histórico para CHOOSE
		if content_cfg is Dictionary:
			for key in content_cfg.keys():
				if not params.has(key):
					params[key] = content_cfg[key]

	# Centralizamos el acceso paramétrico
	_params = params.duplicate(true)

	options_count = int(_params.get("options_count", 3))

	if options_count < 2:
		_error_state = "INVALID_OPTIONS_COUNT"
		_is_setup = false
		return

	var default_positions: Array[Vector2] = [
		Vector2(270.0, 960.0),
		Vector2(540.0, 960.0),
		Vector2(810.0, 960.0)
	]

	options_positions.clear()

	var raw_positions = _params.get("positions", [])

	if raw_positions is Array and raw_positions.size() >= options_count:
		for i: int in range(options_count):
			var p = raw_positions[i]

			if not (p is Array):
				_error_state = "INVALID_OPTION_POSITION"
				_is_setup = false
				return

			if p.size() < 2:
				_error_state = "INVALID_OPTION_POSITION"
				_is_setup = false
				return

			var position: Vector2 = Vector2(
				float(p[0]),
				float(p[1])
			)

			options_positions.append(position)
	else:
		for i: int in range(options_count):
			if i >= default_positions.size():
				_error_state = "INVALID_OPTION_POSITION"
				_is_setup = false
				return

			options_positions.append(default_positions[i])

	# Autoridad de semilla: simulation.seed para V2, fallback a generation.seed
	var seed_val: int = 12345
	if config.has("simulation") and config.get("simulation", {}).has("seed"):
		seed_val = int(config["simulation"]["seed"])
	else:
		var generation_cfg: Dictionary = config.get("generation", {})
		seed_val = int(generation_cfg.get("seed", 12345))

	winning_option = seed_val % options_count

	_is_setup = true
	_error_state = "OK"


func requires_temporal_preparation() -> bool:
	return true


func prepare(game_frames: int) -> void:
	precomputed_selections.clear()

	if game_frames <= 0:
		_error_state = "INVALID_GAME_FRAMES"
		_is_prepared = false
		return

	var cycle_duration: int = max(
		30,
		int(game_frames / 6)
	)

	var lock_start_frame: int = int(game_frames * 0.75)

	for f: int in range(game_frames):
		var selection: int = 0

		if f >= lock_start_frame:
			selection = winning_option
		else:
			selection = int(f / cycle_duration) % options_count

		precomputed_selections.append(selection)

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

	if precomputed_selections.size() != game_frames:
		result.error_state = "INVALID_SELECTION_BUFFER"
		return result

	for f: int in range(game_frames):
		var selection: int = precomputed_selections[f]

		var success_distance: float = 0.0

		if selection == winning_option:
			success_distance = 0.0
		else:
			success_distance = 1.0

		var snapshot: FrameSnapshot = FrameSnapshot.new()

		if selection >= 0 and selection < options_positions.size():
			snapshot.position = options_positions[selection]
		else:
			snapshot.position = Vector2(540.0, 960.0)

		snapshot.rotation = 0.0
		snapshot.scale = Vector2.ONE
		snapshot.opacity = 1.0

		snapshot.custom_data = {
			"active_selection": selection,
			"success_distance": success_distance
		}

		frames.append(snapshot)

	result.frames = frames

	# CHOOSE_V1 es self-scored.
	# El frame ganador es exactamente el inicio del bloqueo final.
	result.winning_frame = lock_start_frame
	result.minimum_distance = 0.0
	result.score = 1.0
	result.tolerance_threshold = 0.0
	result.is_self_scored = true

	# Construcción explícita del array de posiciones para metadata.
	var metadata_positions: Array = []

	for i: int in range(options_positions.size()):
		var position: Vector2 = options_positions[i]

		metadata_positions.append([
			position.x,
			position.y
		])

	result.metadata = {
		"winning_option": winning_option,
		"options_count": options_count,
		"positions": metadata_positions,
		"close_calls": 1,
		"rng_version": "2.0"
	}

	result.error_state = "OK"

	return result


func validate_contract(game_frames: int) -> Dictionary:

	if options_count < 2:
		return {
			"is_valid": false,
			"error_code": "INVALID_OPTIONS_COUNT",
			"message": "Se requieren al menos 2 opciones."
		}

	if options_positions.size() != options_count:
		return {
			"is_valid": false,
			"error_code": "INVALID_OPTIONS_POSITIONS",
			"message": "El número de posiciones no coincide con options_count."
		}

	if precomputed_selections.size() != game_frames:
		return {
			"is_valid": false,
			"error_code": "INVALID_SELECTION_BUFFER",
			"message": "La secuencia temporal no coincide con game_frames."
		}

	if winning_option < 0 or winning_option >= options_count:
		return {
			"is_valid": false,
			"error_code": "INVALID_WINNING_OPTION",
			"message": "La opción ganadora está fuera del rango válido."
		}

	return {
		"is_valid": true,
		"error_code": "OK",
		"message": ""
	}