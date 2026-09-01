extends Node2D

# ============================================================
# ChallengeEngineV01_STATELESS
# GeneradorMaestro.gd
# C6-D3 — Presentation orchestration built on the D2 baseline.
#
# PRINCIPIO:
# - No modifica la simulación ni el RNG.
# - No reemplaza el pipeline de validación.
# - No asume nodos UI legacy.
# - PresentationUI recibe SIEMPRE un único Dictionary de estado.
# - El contador y dificultad se inyectan en ese Dictionary.
# - Los sprites de la mecánica siguen gobernados exclusivamente
#   por FamilyAssets + FrameSnapshot.
# ============================================================

var timeline: VideoTimeline
var verified_history: Array[FrameSnapshot] = []
var final_winning_frame: int = -1
var config_cache: Dictionary = {}
var validate_only: bool = false
var final_result: SimulationResult

# Estado de resolución de referencia universal (C6-A)
var reference_frame_index: int = -1
var reference_frame_mode: ReferenceFrameResolver.ReferenceMode = ReferenceFrameResolver.ReferenceMode.NONE

# Configuración espacial declarativa de presentación (C6-A)
var current_coord_space: CoordinateMapper.CoordinateSpace = CoordinateMapper.CoordinateSpace.CANVAS_1080X1920
var secondary_binding_type: String = "target_position"

# Calibración visual declarativa (C6-D)
var object_scale: float = 1.0
var object_offset: Vector2 = Vector2.ZERO
var target_scale: float = 1.0
var target_offset: Vector2 = Vector2.ZERO

# Capa de presentación UI unificada (C6-D.1 / D3)
var presentation_ui: PresentationUI

# Infraestructura RNG V2.0 (Composition Root)
var rng_registry: RNGStreamRegistry
var structural_rng: StructuralRNG
var cosmetic_rng: CosmeticRNG


@onready var bg_sprite: Sprite2D = $OptimizadorVertical/PantallaVideo/GestorJuego/FondoEstatico
@onready var target_sprite: Sprite2D = $OptimizadorVertical/PantallaVideo/GestorJuego/MetaContenedor
@onready var object_sprite: Sprite2D = $OptimizadorVertical/PantallaVideo/GestorJuego/ObjetoMovil
@onready var presentation_ui_root: Control = get_node_or_null(
	"OptimizadorVertical/PantallaVideo/PresentationUILayer"
)


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

	var def_validation: Dictionary = ChallengeDefinitionValidator.validate_definition(
		config_cache
	)

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

	# --------------------------------------------------------
	# Presentación declarativa
	# --------------------------------------------------------

	setup_presentation_bindings()
	setup_visual_calibration()

	if presentation_ui_root == null:
		var presentation_parent: Node = get_node_or_null(
			"OptimizadorVertical/PantallaVideo"
		)

		if presentation_parent == null:
			emit_engine_error(
				"C6_UI_PARENT_MISSING",
				"No existe el nodo PantallaVideo parent.",
				"OptimizadorVertical/PantallaVideo"
			)
			get_tree().quit(1)
			return

		presentation_ui_root = Control.new()
		presentation_ui_root.name = "PresentationUILayer"
		presentation_parent.add_child(presentation_ui_root)

		presentation_ui_root.position = Vector2.ZERO
		presentation_ui_root.size = Vector2(
			PresentationTheme.VIEWPORT_WIDTH,
			PresentationTheme.VIEWPORT_HEIGHT
		)

		print("[C6_UI] PresentationUILayer creado dinámicamente.")

	var pres_cfg: Dictionary = config_cache.get(
		"presentation",
		{}
	)

	var ui_cfg: Dictionary = pres_cfg.get(
		"ui",
		{}
	)

	var ui_theme_name: String = str(
		ui_cfg.get(
			"theme",
			"default_c6"
		)
	)

	presentation_ui = PresentationUI.new(
		presentation_ui_root,
		ui_theme_name
	)

	print(
		"[C6_UI] root=",
		presentation_ui_root,
		" size=",
		presentation_ui_root.size if presentation_ui_root != null else Vector2(-1.0, -1.0),
		" position=",
		presentation_ui_root.position if presentation_ui_root != null else Vector2(-1.0, -1.0)
	)

	if presentation_ui_root != null:
		presentation_ui_root.mouse_filter = Control.MOUSE_FILTER_IGNORE

	# --------------------------------------------------------
	# RNG / simulación
	# --------------------------------------------------------

	var rng_init: Dictionary = initialize_rng_infrastructure()

	if not bool(rng_init.get("valid", false)):
		emit_engine_error(
			str(
				rng_init.get(
					"error_code",
					"RNG_CONTEXT_INVALID"
				)
			),
			"Falló la inicialización de la infraestructura RNG.",
			str(
				rng_init.get(
					"details",
					[]
				)
			)
		)
		get_tree().quit(1)
		return

	var validation_package: Dictionary = run_validation_pipeline()

	if not bool(
		validation_package.get(
			"valid",
			false
		)
	):
		var error_code: String = str(
			validation_package.get(
				"error_code",
				"SIMULATION_FAILED"
			)
		)

		var error_msg: String = str(
			validation_package.get(
				"message",
				"Fallo en la simulación o autovetting."
			)
		)

		var details: String = str(
			validation_package.get(
				"errors",
				[]
			)
		)

		emit_engine_error(
			error_code,
			error_msg,
			details
		)
		get_tree().quit(1)
		return

	final_result = validation_package["result"]
	var validation: ValidationResult = validation_package["validation"]

	verified_history = final_result.frames
	final_winning_frame = validation.absolute_winning_frame

	# --------------------------------------------------------
	# Frame de referencia certificado
	# --------------------------------------------------------

	var reference_resolution: Dictionary = ReferenceFrameResolver.resolve(
		final_result
	)

	reference_frame_index = int(
		reference_resolution.get(
			"frame_index",
			-1
		)
	)

	reference_frame_mode = reference_resolution.get(
		"mode",
		ReferenceFrameResolver.ReferenceMode.NONE
	)

	print(
		"[C6_REFERENCE_FRAME] ",
		"index=",
		reference_frame_index,
		" mode=",
		str(
			reference_resolution.get(
				"mode_name",
				"NONE"
			)
		),
		" reason=",
		str(
			reference_resolution.get(
				"reason",
				""
			)
		)
	)

	var challenge_id: String = str(
		config_cache.get(
			"challenge_id",
			config_cache.get(
				"id",
				"UNKNOWN"
			)
		)
	)

	var mechanic_id: String = str(
		config_cache.get(
			"mechanic",
			""
		)
	)

	print(
		"[C6_SWEEP_AUDIT] id=",
		challenge_id,
		" mechanic=",
		mechanic_id,
		" mode=",
		str(
			reference_resolution.get(
				"mode_name",
				"NONE"
			)
		),
		" frame_idx=",
		reference_frame_index,
		" reason=",
		str(
			reference_resolution.get(
				"reason",
				""
			)
		)
	)

	var winning_frame_game: int = final_result.winning_frame
	var fps_f: float = float(timeline.fps)

	var telemetry: Dictionary = {
		"initial_seed": int(
			final_result.metadata.get(
				"initial_seed",
				0
			)
		),
		"final_seed": int(
			final_result.metadata.get(
				"final_seed",
				0
			)
		),
		"seed_used": int(
			final_result.metadata.get(
				"seed_used",
				0
			)
		),
		"attempts": int(
			final_result.metadata.get(
				"attempts",
				0
			)
		),
		"rng_version": str(
			final_result.metadata.get(
				"rng_version",
				"1.0"
			)
		),
		"winning_frame_game": winning_frame_game,
		"winning_frame": final_winning_frame,
		"winning_time_game": float(
			winning_frame_game
		) / fps_f,
		"winning_time": float(
			final_winning_frame
		) / fps_f,
		"total_frames": timeline.total_frames,
		"hook_frames": timeline.hook_frames,
		"game_frames": timeline.game_frames,
		"reveal_frames": timeline.reveal_frames,
		"cta_frames": timeline.cta_frames,
		"minimum_distance": validation.minimum_distance,
		"score": validation.score,
		"close_calls": validation.close_calls,
		"winning_frame_in_valid_window": validation.winning_frame_in_valid_window,
		"godot_version": Engine.get_version_info().string,
		"validate_only": validate_only
	}

	print(
		"[TELEMETRY_JSON]"
		+ JSON.stringify(telemetry)
	)

	if validate_only:
		get_tree().quit(0)
		return

	# --------------------------------------------------------
	# Assets
	# --------------------------------------------------------

	var nodes_map: Dictionary = {
		"background": bg_sprite,
		"target": target_sprite,
		"object": object_sprite
	}

	FamilyAssets.configure_presentation(
		config_cache,
		nodes_map
	)

	# Pivot explícito; no altera la simulación.
	target_sprite.centered = true
	object_sprite.centered = true

	# --------------------------------------------------------
	# Estado inicial de los sprites
	#
	# Importante:
	# - Fondo siempre visible.
	# - Target y objeto no se fuerzan a estar visibles antes
	#   de que el bloque temporal correspondiente los utilice.
	# --------------------------------------------------------

	bg_sprite.visible = true

	object_sprite.visible = false
	object_sprite.modulate = Color.WHITE

	target_sprite.visible = true
	target_sprite.modulate = Color.WHITE

	# --------------------------------------------------------
	# Posición inicial declarativa del target.
	# Se conserva exactamente la lógica D2.
	# --------------------------------------------------------

	var raw_target_pos: Vector2 = Vector2(
		850.0,
		960.0
	)

	if secondary_binding_type == "static_position":
		var static_pos_arr = pres_cfg.get(
			"static_target_position",
			[540.0, 960.0]
		)

		if (
			static_pos_arr is Array
			and static_pos_arr.size() >= 2
		):
			raw_target_pos = Vector2(
				float(static_pos_arr[0]),
				float(static_pos_arr[1])
			)

	else:
		var difficulty_cfg: Dictionary = config_cache.get(
			"difficulty",
			{}
		)

		if difficulty_cfg is Dictionary:
			var parking_cfg: Dictionary = difficulty_cfg.get(
				"parking",
				{}
			)

			if (
				parking_cfg is Dictionary
				and parking_cfg.has("target_position")
			):
				var target_pos_arr = parking_cfg.get(
					"target_position",
					[850.0, 960.0]
				)

				if (
					target_pos_arr is Array
					and target_pos_arr.size() >= 2
				):
					raw_target_pos = Vector2(
						float(target_pos_arr[0]),
						float(target_pos_arr[1])
					)

	target_sprite.position = (
		CoordinateMapper.map_position(
			raw_target_pos,
			current_coord_space
		)
		+ target_offset
	)

	target_sprite.scale = (
		Vector2.ONE
		* target_scale
	)

	print(
		"[C6_TARGET] space=",
		current_coord_space,
		" presentation_pos=",
		target_sprite.position
	)

	# --------------------------------------------------------
	# Validación estricta de assets
	# --------------------------------------------------------

	if bg_sprite.texture == null:
		push_error(
			"C6_ASSET_MISSING: FondoEstatico no tiene textura asignada."
		)

	if target_sprite.texture == null:
		push_error(
			"C6_ASSET_MISSING: MetaContenedor no tiene textura asignada."
		)

	if object_sprite.texture == null:
		push_error(
			"C6_ASSET_MISSING: ObjetoMovil no tiene textura asignada."
	)


func setup_presentation_bindings() -> void:
	var pres_cfg: Dictionary = config_cache.get(
		"presentation",
		{}
	)

	var space_str: String = str(
		pres_cfg.get(
			"coordinate_space",
			"CANVAS_1080X1920"
		)
	)

	current_coord_space = (
		CoordinateMapper.get_space_from_string(
			space_str
		)
	)

	secondary_binding_type = str(
		pres_cfg.get(
			"secondary_binding",
			"target_position"
		)
	)


func setup_visual_calibration() -> void:
	var pres_cfg: Dictionary = config_cache.get(
		"presentation",
		{}
	)

	var visual_cfg: Dictionary = pres_cfg.get(
		"visual",
		{}
	)

	if visual_cfg is not Dictionary:
		return

	object_scale = float(
		visual_cfg.get(
			"object_scale",
			1.0
		)
	)

	var obj_off = visual_cfg.get(
		"object_offset",
		[0.0, 0.0]
	)

	if (
		obj_off is Array
		and obj_off.size() >= 2
	):
		object_offset = Vector2(
			float(obj_off[0]),
			float(obj_off[1])
		)

	target_scale = float(
		visual_cfg.get(
			"target_scale",
			1.0
		)
	)

	var tgt_off = visual_cfg.get(
		"target_offset",
		[0.0, 0.0]
	)

	if (
		tgt_off is Array
		and tgt_off.size() >= 2
	):
		target_offset = Vector2(
			float(tgt_off[0]),
			float(tgt_off[1])
		)


func initialize_rng_infrastructure() -> Dictionary:
	rng_registry = RNGStreamRegistry.new()
	structural_rng = StructuralRNG.new(
		rng_registry
	)
	cosmetic_rng = CosmeticRNG.new(
		rng_registry
	)

	return {
		"valid": true,
		"error_code": "OK"
	}


func create_mechanic_rng_context(
	seed: int,
	consumer_id: String,
	allowed_streams: Array[int]
):
	return MechanicRNGContext.create(
		seed,
		"2.0",
		consumer_id,
		allowed_streams,
		structural_rng,
		rng_registry
	)


func create_presentation_rng_context(
	seed: int,
	consumer_id: String,
	allowed_streams: Array[int]
):
	return PresentationRNGContext.create(
		seed,
		"2.0",
		consumer_id,
		allowed_streams,
		cosmetic_rng,
		rng_registry
	)


func run_validation_pipeline() -> Dictionary:
	var mechanic_id: String = str(
		config_cache.get(
			"mechanic",
			""
		)
	)

	var mechanic: ChallengeMechanic = (
		MechanicRegistry.create_mechanic(
			mechanic_id
		)
	)

	if mechanic == null:
		return {
			"valid": false,
			"error_code":
				"UNKNOWN_MECHANIC_ID",
			"message":
				"La mecánica requerida '%s' no está registrada en MechanicRegistry." % mechanic_id,
			"errors": [
				("Unregistered mechanic_id: %s"
				% mechanic_id)
			]
		}

	var generation_config: Dictionary = (
		config_cache.get(
			"generation",
			{}
		)
	)

	var initial_seed: int = int(
		generation_config.get(
			"seed",
			12345
		)
	)

	var rng_version: String = str(
		generation_config.get(
			"rng_version",
			"1.0"
		)
	)

	var current_seed: int = initial_seed

	var sim_result: SimulationResult = null
	var sim_validation: ValidationResult = null

	var is_v2: bool = (
		rng_version == "2.0"
	)

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

	var catch_v1_allowed_streams: Array[int] = [
		RNGStreamRegistry.STREAM_CATCH_TARGET_MOTION,
		RNGStreamRegistry.STREAM_CATCH_PURSUER_BIAS,
		RNGStreamRegistry.STREAM_CATCH_INITIAL_PHASE
	]

	var find_v1_allowed_streams: Array[int] = [
		RNGStreamRegistry.STREAM_FIND_SPATIAL_PLACEMENT,
		RNGStreamRegistry.STREAM_FIND_TOPOLOGY_GENERATION,
		RNGStreamRegistry.STREAM_FIND_SCANNER_TRAJECTORY,
		RNGStreamRegistry.STREAM_FIND_TARGET_DRIFT
	]

	var attempts: int = 0
	const MAX_ATTEMPTS: int = 100

	while attempts < MAX_ATTEMPTS:
		attempts += 1

		var context_result = null

		if is_v2:
			match mechanic_id.to_lower():

				"pilot":
					context_result = create_mechanic_rng_context(
						current_seed,
						"PilotMechanic",
						pilot_allowed_streams
					)

				"parking_v2":
					context_result = create_mechanic_rng_context(
						current_seed,
						"ParkingMechanic",
						parking_v2_allowed_streams
					)

				"hit_v1":
					context_result = create_mechanic_rng_context(
						current_seed,
						"HitMechanic",
						hit_v1_allowed_streams
					)

				"catch_v1":
					context_result = create_mechanic_rng_context(
						current_seed,
						"CatchMechanic",
						catch_v1_allowed_streams
					)

				"find_v1":
					context_result = create_mechanic_rng_context(
						current_seed,
						"FindMechanic",
						find_v1_allowed_streams
					)

				"choose_v1":
					context_result = create_mechanic_rng_context(
						current_seed,
						"ChooseMechanic",
						[]
					)

				"count_v1":
					context_result = create_mechanic_rng_context(
						current_seed,
						"CountMechanic",
						[]
					)

				_:
					return {
						"valid": false,
						"error_code":
							"RNG_CONTEXT_INVALID",
						"message":
							"No existe contrato RNG V2.0 para la mecánica '%s'." % mechanic_id,
						"errors": [
							("Missing V2.0 mechanic RNG contract: "
							+ mechanic_id)
						]
					}

			if not context_result.is_valid:
				return {
					"valid": false,
					"error_code":
						str(
							context_result.error_code
						),
					"message":
						"No se pudo crear la capability RNG de la mecánica.",
					"errors": [
						str(
							context_result.error_code
						)
					]
				}

			mechanic.set_rng_context(
				context_result.context
			)

		mechanic.setup(
			config_cache
		)

		if (
			not mechanic._is_setup
			or mechanic._error_state != "OK"
		):
			current_seed = lcg_next_seed(
				current_seed
			)
			continue

		if mechanic.requires_temporal_preparation():
			mechanic.prepare(
				timeline.game_frames
			)

			if (
				not mechanic._is_prepared
				or mechanic._error_state != "OK"
			):
				current_seed = lcg_next_seed(
					current_seed
				)
				continue

		var test_result: SimulationResult = (
			mechanic.simulate(
				timeline.game_frames,
				current_seed,
				config_cache
			)
		)

		if (
			is_v2
			and mechanic_id.to_lower()
			in [
				"pilot",
				"parking_v2",
				"hit_v1",
				"catch_v1",
				"find_v1",
				"choose_v1",
				"count_v1"
			]
			and context_result.context.error_state != "OK"
		):
			return {
				"valid": false,
				"error_code":
					"MECHANIC_SIMULATION_ERROR",
				"message":
					"El contexto RNG reportó un error durante la simulación.",
				"errors": [
					str(
						context_result.context.error_state
					)
				]
			}

		var contract_check: Dictionary = (
			test_result.validate_contract(
				timeline.game_frames
			)
		)

		if not bool(
			contract_check.get(
				"is_valid",
				false
			)
		):
			return {
				"valid": false,
				"error_code":
					str(
						contract_check.get(
							"error_code",
							"SIMULATION_CONTRACT_VIOLATION"
						)
					),
				"message":
					str(
						contract_check.get(
							"message",
							""
						)
					),
				"errors": [
					str(
						contract_check.get(
							"message",
							""
						)
					)
				]
			}

		SimulationMetricsResolver.resolve_metrics(
			test_result
		)

		if test_result.error_state != "OK":
			return {
				"valid": false,
				"error_code":
					test_result.error_state,
				"message":
					"Fallo en la resolución de métricas: %s"
					% test_result.error_state,
				"errors": [
					test_result.error_state
				]
			}

		WinningFrameDetector.analyze_and_score(
			test_result
		)

		var validation: ValidationResult = (
			ChallengeValidator.validate(
				test_result,
				timeline.hook_frames,
				timeline.game_frames
			)
		)

		if validation.is_valid:
			sim_result = test_result
			sim_validation = validation
			break

		current_seed = lcg_next_seed(
			current_seed
		)

	if (
		sim_result == null
		or sim_validation == null
	):
		return {
			"valid": false,
			"error_code":
				"NO_VALID_SIMULATION",
			"message":
				"No se encontró una simulación válida que cumpliera los criterios narrativos tras %d intentos." % attempts,
			"errors": [
				"Exhausted %d seed attempts without finding a valid simulation." % attempts
			]
		}

	sim_result.metadata["initial_seed"] = (
		initial_seed
	)
	sim_result.metadata["final_seed"] = (
		current_seed
	)
	sim_result.metadata["seed_used"] = (
		current_seed
	)
	sim_result.metadata["attempts"] = (
		attempts
	)
	sim_result.metadata["rng_version"] = (
		rng_version
	)

	return {
		"valid": true,
		"result": sim_result,
		"validation": sim_validation,
		"errors": []
	}


func lcg_next_seed(seed: int) -> int:
	return int(
		(
			seed * 1103515245
			+ 12345
		)
		& 0x7fffffff
	)


func emit_engine_error(
	code: String,
	message: String,
	details: String
) -> void:

	var challenge_id: String = str(
		config_cache.get(
			"challenge_id",
			config_cache.get(
				"id",
				"UNKNOWN"
			)
		)
	)

	var error_payload: Dictionary = {
		"error": true,
		"code": code,
		"message": message,
		"details": details,
		"challenge_id": challenge_id,
		"godot_version": Engine.get_version_info().string
	}

	print(
		"[ERROR_JSON]"
		+ JSON.stringify(error_payload)
	)


func apply_frame_snapshot(
	frame_state: FrameSnapshot
) -> void:

	# Entidad primaria
	object_sprite.position = (
		CoordinateMapper.map_position(
			frame_state.position,
			current_coord_space
		)
		+ object_offset
	)

	object_sprite.rotation = (
		frame_state.rotation
	)

	object_sprite.scale = (
		frame_state.scale
		* object_scale
	)

	object_sprite.modulate.a = (
		frame_state.opacity
	)

	# Entidad secundaria
	if (
		secondary_binding_type == "target_position"
		and frame_state.custom_data.has(
			"target_position"
		)
	):
		var t_pos = (
			frame_state.custom_data[
				"target_position"
			]
		)

		if t_pos is Vector2:
			target_sprite.position = (
				CoordinateMapper.map_position(
					t_pos,
					current_coord_space
				)
				+ target_offset
			)

			target_sprite.scale = (
				Vector2.ONE
				* target_scale
			)

			target_sprite.visible = true

	elif (
		secondary_binding_type == "target_x"
		and frame_state.custom_data.has(
			"target_x"
		)
	):
		var t_x = float(
			frame_state.custom_data[
				"target_x"
			]
		)

		var mapped_x = (
			CoordinateMapper.map_scalar_x(
				t_x,
				current_coord_space
			)
		)

		target_sprite.position = (
			Vector2(
				mapped_x,
				object_sprite.position.y
			)
			+ target_offset
		)

		target_sprite.scale = (
			Vector2.ONE
			* target_scale
		)

		target_sprite.visible = true

	elif secondary_binding_type == "static_position":
		target_sprite.scale = (
			Vector2.ONE
			* target_scale
		)

		target_sprite.visible = true


func apply_reference_frame() -> void:
	if reference_frame_index < 0:
		return

	if (
		reference_frame_index
		>= verified_history.size()
	):
		return

	apply_frame_snapshot(
		verified_history[
			reference_frame_index
		]
	)


# ============================================================
# UI STATE BUILDER
# ============================================================

func build_ui_content(
	current_block: String,
	state_frame: int
) -> Dictionary:

	var ui_content: Dictionary = {}

	var content_cfg = config_cache.get(
		"content",
		{}
	)

	if content_cfg is Dictionary:
		ui_content = content_cfg.duplicate()

	var difficulty_cfg = config_cache.get(
		"difficulty",
		{}
	)

	if difficulty_cfg is Dictionary:
		ui_content["difficulty_level"] = int(
			difficulty_cfg.get(
				"level",
				3
			)
		)

	# Estado temporal explícito para PresentationUI.
	# Se mantienen estos valores dentro del Dictionary para
	# que PresentationUI NO dependa de una firma de 4 parámetros.
	ui_content["ui_state"] = current_block
	ui_content["ui_state_frame"] = max(
		0,
		state_frame
	)
	ui_content["ui_fps"] = timeline.fps
	ui_content["winning_frame"] = final_winning_frame
	ui_content["reference_frame"] = reference_frame_index

	return ui_content


# ============================================================
# TEMPORAL STATE
# ============================================================

func get_current_state_frame(
	current_block: String
) -> int:

	var state_frame: int = 0

	match current_block:

		"HOOK":
			state_frame = (
				timeline.current_frame
			)

		"GAME":
			state_frame = (
				timeline.current_frame
				- timeline.hook_frames
			)

		"REVEAL":
			state_frame = (
				timeline.current_frame
				- timeline.hook_frames
				- timeline.game_frames
			)

		"CTA":
			state_frame = (
				timeline.current_frame
				- timeline.hook_frames
				- timeline.game_frames
				- timeline.reveal_frames
			)

		_:
			state_frame = 0

	return max(
		0,
		state_frame
	)


# ============================================================
# RUNTIME RENDER
# ============================================================

func _process(_delta: float) -> void:

	if validate_only or timeline == null:
		return

	if timeline.is_finished():
		get_tree().quit(0)
		return

	var current_block: String = (
		timeline.get_current_block()
	)

	var state_frame: int = (
		get_current_state_frame(
			current_block
		)
	)

	var ui_content: Dictionary = (
		build_ui_content(
			current_block,
			state_frame
		)
	)

	# --------------------------------------------------------
	# Cada frame comienza con un estado visual explícito.
	# El objetivo es impedir "residuos" de una fase anterior.
	# --------------------------------------------------------

	match current_block:

		"HOOK":
			# Solo Fondo + objeto/estado de referencia.
			object_sprite.visible = true
			object_sprite.modulate.a = 1.0

			apply_reference_frame()

			# D3: PresentationUI recibe UN Dictionary.
			if presentation_ui != null:
				presentation_ui.set_state(
					"HOOK",
					ui_content
				)

		"GAME":
			object_sprite.visible = true
			object_sprite.modulate.a = 1.0

			var game_idx: int = (
				timeline.get_game_index()
			)

			if (
				game_idx >= 0
				and game_idx < verified_history.size()
			):
				var frame_state: FrameSnapshot = (
					verified_history[
						game_idx
					]
				)

				apply_frame_snapshot(
					frame_state
				)
			else:
				# Protección: si el frame no existe, no
				# simulamos un estado inventado.
				object_sprite.visible = false

			if presentation_ui != null:
				presentation_ui.set_state(
					"GAME",
					ui_content
				)

		"REVEAL":
			object_sprite.visible = true
			object_sprite.modulate.a = 1.0

			# Mantener exclusivamente el frame ganador certificado.
			apply_reference_frame()

			if presentation_ui != null:
				presentation_ui.set_state(
					"REVEAL",
					ui_content
				)

		"CTA":
			object_sprite.visible = true
			object_sprite.modulate.a = 1.0

			# Mantener la escena final certificada.
			apply_reference_frame()

			if presentation_ui != null:
				presentation_ui.set_state(
					"CTA",
					ui_content
				)

		_:
			object_sprite.visible = false

	timeline.advance()


# ============================================================
# CLI
# ============================================================

func parse_cli_arguments() -> Dictionary:
	var args: PackedStringArray = (
		OS.get_cmdline_user_args()
	)

	var config_path: String = ""

	for arg: String in args:
		if arg.begins_with(
			"--config="
		):
			config_path = arg.substr(
				"--config=".length()
			)

	if (
		config_path.is_empty()
		or not FileAccess.file_exists(
			config_path
		)
	):
		return {}

	var file: FileAccess = FileAccess.open(
		config_path,
		FileAccess.READ
	)

	if file == null:
		return {}

	var json: JSON = JSON.new()

	var parse_error: Error = (
		json.parse(
			file.get_as_text()
		)
	)

	if (
		parse_error != OK
		or not (
			json.data is Dictionary
		)
	):
		return {}

	return json.data


func has_user_flag(
	flag: String
) -> bool:
	var args: PackedStringArray = (
		OS.get_cmdline_user_args()
	)
	return args.has(flag)
