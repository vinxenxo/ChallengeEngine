extends Node2D

const ChallengeRuntimeBridge = preload("res://core/execution/ChallengeRuntimeBridge.gd")
const ChallengeLegacyRuntimeOracle = preload("res://core/execution/ChallengeLegacyRuntimeOracle.gd")

# ============================================================
# ChallengeEngineV01_STATELESS
# GeneradorMaestro.gd
# C6-F4.3 — Effective Runtime Composition Root.
#
# PRINCIPIO:
# - C6 Runtime es la ruta efectiva de producción.
# - El LegacyRuntimeOracle existe solo para auditoría cruzada.
# - GeneradorMaestro no implementa simulación, RNG ni seed retry.
# - Presentation consume exclusivamente SimulationResult + VideoTimeline.
# - Los sprites de la mecánica siguen gobernados exclusivamente
#   por FamilyAssets + FrameSnapshot.
# ============================================================

var timeline: VideoTimeline
var verified_history: Array[FrameSnapshot] = []
var final_winning_frame: int = -1
var config_cache: Dictionary = {}
var validate_only: bool = false
var final_result: SimulationResult
var runtime_context: ChallengeRuntimeContext = null

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
var presentation_profile: PresentationProfile


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

	# --------------------------------------------------------
	# C6-F4.3: EFFECTIVE C6 RUNTIME
	# Production state is resolved through the certified runtime bridge.
	# --------------------------------------------------------
	var effective_package: Dictionary = ChallengeRuntimeBridge.run_effective_pipeline(
		config_cache
	)

	if not bool(effective_package.get("success", false)):
		emit_engine_error(
			str(effective_package.get("error_code", "EFFECTIVE_RUNTIME_FAILED")),
			str(effective_package.get("error", "C6 effective runtime failed.")),
			str(effective_package.get("failures", []))
		)
		get_tree().quit(1)
		return

	runtime_context = effective_package.get("context") as ChallengeRuntimeContext
	if runtime_context == null or runtime_context.simulation_result == null or runtime_context.timeline == null:
		emit_engine_error(
			"EFFECTIVE_RUNTIME_INVALID",
			"El runtime C6 devolvió un contexto incompleto.",
			"simulation_result/timeline/context required"
		)
		get_tree().quit(1)
		return

	final_result = runtime_context.simulation_result
	timeline = runtime_context.timeline
	verified_history = final_result.frames

	var effective_validation: ValidationResult = effective_package.get("validation")
	if effective_validation == null or not effective_validation.is_valid:
		emit_engine_error(
			"EFFECTIVE_VALIDATION_FAILED",
			"La validación del resultado efectivo C6 no es válida.",
			str(effective_validation.errors if effective_validation != null else [])
		)
		get_tree().quit(1)
		return

	final_winning_frame = effective_validation.absolute_winning_frame

	# --------------------------------------------------------
	# C6-F4.3: INDEPENDENT LEGACY ORACLE
	# Never used as production state; only audits exact equivalence.
	# --------------------------------------------------------
	var oracle_package: Dictionary = ChallengeLegacyRuntimeOracle.run(config_cache)
	if not bool(oracle_package.get("valid", false)):
		emit_engine_error(
			str(oracle_package.get("error_code", "LEGACY_ORACLE_FAILED")),
			str(oracle_package.get("message", "Legacy runtime oracle failed.")),
			str(oracle_package.get("errors", []))
		)
		get_tree().quit(1)
		return

	var oracle_result: SimulationResult = oracle_package.get("result")
	var oracle_timeline: VideoTimeline = oracle_package.get("timeline")
	var equivalence := ChallengeRuntimeBridge.verify_equivalence(
		oracle_timeline,
		oracle_result,
		runtime_context
	)

	if not bool(equivalence.get("success", false)):
		emit_engine_error(
			"F4_RUNTIME_EQUIVALENCE_FAILED",
			"El runtime C6 efectivo no coincide con el oráculo legacy.",
			str(equivalence.get("failures", []))
		)
		get_tree().quit(1)
		return

	print("[C6-F4.3] Effective Runtime + independent legacy oracle: PASS")

	# --------------------------------------------------------
	# C6-E E1: profile declarativo, únicamente de presentación.
	# Se inicializa antes de crear PresentationUI; no interviene
	# en SimulationResult, RNG ni VideoTimeline.
	# --------------------------------------------------------
	presentation_profile = PresentationProfile.from_challenge(config_cache)
	var profile_validation := presentation_profile.validate()
	if not bool(profile_validation.get("is_valid", false)):
		emit_engine_error(
			"PRESENTATION_PROFILE_INVALID",
			"El Presentation Profile viola su contrato de presentación.",
			str(profile_validation.get("errors", []))
		)
		get_tree().quit(1)
		return

	print(
		"[C6E_PROFILE] id=", presentation_profile.profile_id,
		" source=", presentation_profile.source_canvas_size,
		" master=", presentation_profile.master_output_size,
		" safe=", presentation_profile.safe_area
	)

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

	var ui_theme_name: String = presentation_profile.theme_name
	if ui_cfg.has("theme"):
		ui_theme_name = str(ui_cfg.get("theme", presentation_profile.theme_name))

	presentation_ui = PresentationUI.new(
		presentation_ui_root,
		ui_theme_name,
		presentation_profile
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
		"minimum_distance": effective_validation.minimum_distance,
		"score": effective_validation.score,
		"close_calls": effective_validation.close_calls,
		"winning_frame_in_valid_window": effective_validation.winning_frame_in_valid_window,
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


func build_winning_highlight_rects() -> Array:
	# E4 es estrictamente presentación: obtenemos la caja visible
	# de los sprites que ya han sido posicionados para este frame.
	# No consultamos SimulationResult, validaciones ni recalculamos win.
	var rects: Array = []

	for sprite in [object_sprite, target_sprite]:
		if sprite == null or not sprite.visible or sprite.texture == null:
			continue

		var local_rect: Rect2 = sprite.get_rect()
		var canvas_rect: Rect2 = sprite.get_global_transform() * local_rect

		if presentation_ui_root != null:
			var to_ui: Transform2D = presentation_ui_root.get_global_transform().affine_inverse()
			canvas_rect = to_ui * canvas_rect

		if canvas_rect.size.x > 0.0 and canvas_rect.size.y > 0.0:
			rects.append(canvas_rect)

	return rects


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

	ui_content["ui_state"] = current_block
	ui_content["ui_state_frame"] = max(
		0,
		state_frame
	)
	ui_content["ui_fps"] = timeline.fps
	ui_content["absolute_frame"] = timeline.get_current_frame()
	ui_content["winning_frame"] = final_winning_frame
	ui_content["winning_frame_game"] = final_result.winning_frame if final_result != null else -1
	ui_content["reference_frame"] = reference_frame_index
	ui_content["timeline"] = timeline

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
				timeline.get_current_frame()
			)

		"GAME":
			state_frame = (
				timeline.get_current_frame()
				- timeline.hook_frames
			)

		"REVEAL":
			state_frame = (
				timeline.get_current_frame()
				- timeline.hook_frames
				- timeline.game_frames
			)

		"CTA":
			state_frame = (
				timeline.get_current_frame()
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

	# C6-D4: phases with duration 0 never become an active block.
	# Timeline remains the single source of temporal truth.

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
			object_sprite.visible = true
			object_sprite.modulate.a = 1.0

			apply_reference_frame()

			if presentation_ui != null:
				var rm = ChallengePresentationBinder.build_frame_render_model(
					"HOOK", ui_content, presentation_ui.current_profile
				)
				presentation_ui.apply_render_model(rm)

		"GAME":
			object_sprite.visible = true
			object_sprite.modulate.a = 1.0

			var game_idx: int = timeline.get_game_index()

			if game_idx >= 0 and game_idx < verified_history.size():
				var frame_state: FrameSnapshot = verified_history[game_idx]
				apply_frame_snapshot(frame_state)
			else:
				object_sprite.visible = false

			ui_content["winning_highlight_rects"] = build_winning_highlight_rects()

			if presentation_ui != null:
				var rm = ChallengePresentationBinder.build_frame_render_model(
					"GAME", ui_content, presentation_ui.current_profile
				)
				presentation_ui.apply_render_model(rm)

		"REVEAL":
			object_sprite.visible = true
			object_sprite.modulate.a = 1.0

			apply_reference_frame()

			if presentation_ui != null:
				var rm = ChallengePresentationBinder.build_frame_render_model(
					"REVEAL", ui_content, presentation_ui.current_profile
				)
				presentation_ui.apply_render_model(rm)

		"CTA":
			object_sprite.visible = true
			object_sprite.modulate.a = 1.0

			apply_reference_frame()

			if presentation_ui != null:
				var rm = ChallengePresentationBinder.build_frame_render_model(
					"CTA", ui_content, presentation_ui.current_profile
				)
				presentation_ui.apply_render_model(rm)

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
