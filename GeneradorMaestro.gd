extends Node2D

var timeline: VideoTimeline
var verified_history: Array[FrameSnapshot] = []
var final_winning_frame: int = -1
var config_cache: Dictionary = {}
var validate_only: bool = false

# Infraestructura RNG V2.0 (Composition Root)
var rng_registry: RNGStreamRegistry
var structural_rng: StructuralRNG
var cosmetic_rng: CosmeticRNG

@onready var bg_sprite: Sprite2D = $OptimizadorVertical/PantallaVideo/GestorJuego/FondoEstatico
@onready var target_sprite: Sprite2D = $OptimizadorVertical/PantallaVideo/GestorJuego/MetaContenedor
@onready var object_sprite: Sprite2D = $OptimizadorVertical/PantallaVideo/GestorJuego/ObjetoMovil
@onready var main_label: Label = $OptimizadorVertical/PantallaVideo/UI_Gancho/TextoTitulo

func _ready() -> void:
	print("=== GENERADOR MAESTRO INICIADO ===")

	config_cache = parse_cli_arguments()
	if config_cache.is_empty():
		emit_engine_error(
			"CHALLENGE_INVALID",
			"No se proporcionó una configuración válida desde la CLI o el archivo no existe.",
			""
		)
		get_tree().quit(1)
		return

	var def_validation: Dictionary = ChallengeDefinitionValidator.validate_definition(config_cache)
	if not bool(def_validation.get("is_valid", false)):
		emit_engine_error(
			"CHALLENGE_INVALID",
			"La estructura de entrada de Capa 0 viola el esquema requerido.",
			str(def_validation.get("errors", []))
		)
		get_tree().quit(1)
		return

	validate_only = has_user_flag("--validate-only")
	timeline = VideoTimeline.new(config_cache.get("video", {}))

	var rng_init: Dictionary = initialize_rng_infrastructure()
	if not bool(rng_init.get("valid", false)):
		emit_engine_error(
			str(rng_init.get("error_code", "RNG_CONTEXT_INVALID")),
			"Falló la inicialización de la infraestructura RNG.",
			str(rng_init.get("details", []))
		)
		get_tree().quit(1)
		return

	var validation_package: Dictionary = run_validation_pipeline()
	if not bool(validation_package.get("valid", false)):
		var error_code: String = str(validation_package.get("error_code", "SIMULATION_FAILED"))
		var error_msg: String = str(validation_package.get("message", "Fallo en la simulación o autovetting."))
		var details: String = str(validation_package.get("errors", []))
		
		emit_engine_error(error_code, error_msg, details)
		get_tree().quit(1)
		return

	var final_result: SimulationResult = validation_package["result"]
	var validation: ValidationResult = validation_package["validation"]

	verified_history = final_result.frames
	final_winning_frame = validation.absolute_winning_frame

	var winning_frame_game: int = final_result.winning_frame
	var fps_f: float = float(timeline.fps)

	var telemetry: Dictionary = {
		# Trazabilidad estricta de semillas
		"initial_seed": int(final_result.metadata.get("initial_seed", 0)),
		"final_seed": int(final_result.metadata.get("final_seed", 0)),
		"seed_used": int(final_result.metadata.get("seed_used", 0)),
		"attempts": int(final_result.metadata.get("attempts", 0)),
		"rng_version": str(final_result.metadata.get("rng_version", "1.0")),

		# Fotogramas y Tiempos Unificados (GAME vs Absoluto de Vídeo)
		"winning_frame_game": winning_frame_game,
		"winning_frame": final_winning_frame,
		"winning_time_game": float(winning_frame_game) / fps_f,
		"winning_time": float(final_winning_frame) / fps_f,

		# Estructura Temporal Unificada (VideoTimeline)
		"total_frames": timeline.total_frames,
		"hook_frames": timeline.hook_frames,
		"game_frames": timeline.game_frames,
		"cta_frames": timeline.cta_frames,

		# Métricas de Autovetting
		"minimum_distance": validation.minimum_distance,
		"score": validation.score,
		"close_calls": validation.close_calls,

		# Metadatos específicos de la trayectoria
		"dodge_offset": final_result.metadata.get("dodge_offset", 0.0),
		"save_offset": final_result.metadata.get("save_offset", 0.0),
		"overshoot_dist": final_result.metadata.get("overshoot_dist", 0.0),

		"winning_frame_in_valid_window": validation.winning_frame_in_valid_window,
		"godot_version": Engine.get_version_info().string,
		"validate_only": validate_only
	}

	print("[TELEMETRY_JSON]" + JSON.stringify(telemetry))

	if validate_only:
		get_tree().quit(0)
		return

	var parking_cfg: Dictionary = config_cache.get("difficulty", {}).get("parking", {})
	var target_pos_arr: Array = parking_cfg.get("target_position", [540.0, 960.0])
	target_sprite.position = Vector2(float(target_pos_arr[0]), float(target_pos_arr[1]))

	var nodes_map: Dictionary = {
		"background": bg_sprite,
		"target": target_sprite,
		"object": object_sprite
	}
	FamilyAssets.configure_presentation(config_cache, nodes_map)
	main_label.text = str(config_cache.get("content", {}).get("hook", ""))

func initialize_rng_infrastructure() -> Dictionary:
	rng_registry = RNGStreamRegistry.new()
	structural_rng = StructuralRNG.new(rng_registry)
	cosmetic_rng = CosmeticRNG.new(rng_registry)

	return {
		"valid": true,
		"error_code": "OK"
	}

func create_mechanic_rng_context(seed: int, consumer_id: String, allowed_streams: Array[int]):
	return MechanicRNGContext.create(
		seed,
		"2.0",
		consumer_id,
		allowed_streams,
		structural_rng,
		rng_registry
	)

func create_presentation_rng_context(seed: int, consumer_id: String, allowed_streams: Array[int]):
	return PresentationRNGContext.create(
		seed,
		"2.0",
		consumer_id,
		allowed_streams,
		cosmetic_rng,
		rng_registry
	)

func run_validation_pipeline() -> Dictionary:
	var mechanic_id: String = str(config_cache.get("mechanic", ""))
	var mechanic: ChallengeMechanic = MechanicRegistry.create_mechanic(mechanic_id)

	if mechanic == null:
		return {
			"valid": false,
			"error_code": "UNKNOWN_MECHANIC_ID",
			"message": "La mecánica requerida '%s' no está registrada en MechanicRegistry." % mechanic_id,
			"errors": ["Unregistered mechanic_id: %s" % mechanic_id]
		}

	mechanic.setup(config_cache)

	var generation_config: Dictionary = config_cache.get("generation", {})
	var initial_seed: int = int(
		generation_config.get("seed", 12345)
	)
	var rng_version: String = str(
		generation_config.get("rng_version", "1.0")
	)

	var current_seed: int = initial_seed
	var final_result: SimulationResult = null
	var final_validation: ValidationResult = null

	var is_v2: bool = rng_version == "2.0"
	var pilot_allowed_streams: Array[int] = [
		RNGStreamRegistry.STREAM_TRAJECTORY,
		RNGStreamRegistry.STREAM_CONTROL
	]
	var parking_v2_allowed_streams: Array[int] = [
		RNGStreamRegistry.STREAM_PARKING_DODGE,
		RNGStreamRegistry.STREAM_PARKING_SAVE,
		RNGStreamRegistry.STREAM_PARKING_OVERSHOOT,
		RNGStreamRegistry.STREAM_PARKING_STEERING
	]
	var hit_v1_allowed_streams: Array[int] = [
		RNGStreamRegistry.STREAM_HIT_SPEED_VARIANCE,
		RNGStreamRegistry.STREAM_HIT_TRAJECTORY_NOISE,
		RNGStreamRegistry.STREAM_HIT_TARGET_OFFSET
	]

	var attempts: int = 0
	const MAX_ATTEMPTS: int = 100

	while attempts < MAX_ATTEMPTS:
		attempts += 1

		var context_result = null
		if is_v2:
			if mechanic_id.to_lower() == "pilot":
				context_result = create_mechanic_rng_context(
					current_seed,
					"PilotMechanic",
					pilot_allowed_streams
				)
			elif mechanic_id.to_lower() == "parking_v2":
				context_result = create_mechanic_rng_context(
					current_seed,
					"ParkingMechanic",
					parking_v2_allowed_streams
				)
			elif mechanic_id.to_lower() == "hit_v1":
				context_result = create_mechanic_rng_context(
					current_seed,
					"HitMechanic",
					hit_v1_allowed_streams
				)
			else:
				return {
					"valid": false,
					"error_code": "RNG_CONTEXT_INVALID",
					"message": "No existe todavía un contrato RNG V2.0 para la mecánica '%s'." % mechanic_id,
					"errors": ["Missing V2.0 mechanic RNG contract: %s" % mechanic_id]
				}

			if not context_result.is_valid:
				return {
					"valid": false,
					"error_code": str(context_result.error_code),
					"message": "No se pudo crear la capability RNG de la mecánica.",
					"errors": [str(context_result.error_code)]
				}
			mechanic.set_rng_context(context_result.context)

		var test_result: SimulationResult = mechanic.simulate(
			timeline.game_frames,
			current_seed,
			config_cache
		)

		if is_v2 and mechanic_id.to_lower() in ["pilot", "parking_v2", "hit_v1"] and context_result.context.error_state != "OK":
			return {
				"valid": false,
				"error_code": "MECHANIC_SIMULATION_ERROR",
				"message": "El contexto RNG reportó un error durante la simulación.",
				"errors": [str(context_result.context.error_state)]
			}

		var contract_check: Dictionary = test_result.validate_contract(timeline.game_frames)
		if not bool(contract_check.get("is_valid", false)):
			return {
				"valid": false,
				"error_code": str(contract_check.get("error_code", "SIMULATION_CONTRACT_VIOLATION")),
				"message": str(contract_check.get("message", "")),
				"errors": [str(contract_check.get("message", ""))]
			}

		# Respetar la soberanía matemática de HIT: no pasa por el WinningFrameDetector genérico
		if mechanic_id.to_lower() != "hit_v1":
			WinningFrameDetector.analyze_and_score(test_result)

		var validation: ValidationResult = ChallengeValidator.validate(
			test_result,
			timeline.hook_frames,
			timeline.game_frames
		)

		if validation.is_valid:
			final_result = test_result
			final_validation = validation
			break

		current_seed = lcg_next_seed(current_seed)

	if final_result == null or final_validation == null:
		return {
			"valid": false,
			"error_code": "NO_VALID_SIMULATION",
			"message": "No se encontró una simulación válida que cumpliera los criterios narrativos tras %d intentos." % attempts,
			"errors": ["Exhausted %d seed attempts without finding a valid simulation." % attempts]
		}

	final_result.metadata["initial_seed"] = initial_seed
	final_result.metadata["final_seed"] = current_seed
	final_result.metadata["seed_used"] = current_seed
	final_result.metadata["attempts"] = attempts
	final_result.metadata["rng_version"] = rng_version

	return {
		"valid": true,
		"result": final_result,
		"validation": final_validation,
		"errors": []
	}

func lcg_next_seed(seed: int) -> int:
	return int((seed * 1103515245 + 12345) & 0x7fffffff)

func emit_engine_error(code: String, message: String, details: String) -> void:
	var challenge_id: String = str(config_cache.get("challenge_id", config_cache.get("id", "UNKNOWN")))
	var error_payload: Dictionary = {
		"error": true,
		"code": code,
		"message": message,
		"details": details,
		"challenge_id": challenge_id,
		"godot_version": Engine.get_version_info().string
	}
	print("[ERROR_JSON]" + JSON.stringify(error_payload))

func _process(_delta: float) -> void:
	if validate_only or timeline == null:
		return

	if timeline.is_finished():
		get_tree().quit(0)
		return

	match timeline.get_current_block():
		"HOOK":
			object_sprite.visible = true
			object_sprite.position = Vector2(540.0, 960.0)
			object_sprite.rotation = 0.0
			object_sprite.modulate.a = 0.5

		"GAME":
			object_sprite.visible = true
			object_sprite.modulate.a = 1.0

			var game_idx: int = timeline.get_game_index()
			if game_idx >= 0 and game_idx < verified_history.size():
				var frame_state: FrameSnapshot = verified_history[game_idx]
				object_sprite.position = frame_state.position
				object_sprite.rotation = frame_state.rotation
				object_sprite.scale = frame_state.scale
				object_sprite.modulate.a = frame_state.opacity

		"CTA":
			object_sprite.visible = false
			main_label.text = str(config_cache.get("content", {}).get("cta", ""))

	timeline.advance()

func parse_cli_arguments() -> Dictionary:
	var args: PackedStringArray = OS.get_cmdline_user_args()
	var config_path: String = ""

	for arg: String in args:
		if arg.begins_with("--config="):
			config_path = arg.substr("--config=".length())

	if config_path.is_empty() or not FileAccess.file_exists(config_path):
		return {}

	var file: FileAccess = FileAccess.open(config_path, FileAccess.READ)
	if file == null:
		return {}

	var json: JSON = JSON.new()
	var parse_error: Error = json.parse(file.get_as_text())
	if parse_error != OK or not (json.data is Dictionary):
		return {}

	return json.data

func has_user_flag(flag: String) -> bool:
	var args: PackedStringArray = OS.get_cmdline_user_args()
	return args.has(flag)