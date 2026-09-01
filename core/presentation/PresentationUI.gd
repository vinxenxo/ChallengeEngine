class_name PresentationUI
extends RefCounted

var container: Control

var hook_label: Label
var reveal_label: Label

var difficulty_badge: Panel
var difficulty_label: Label

var countdown_label: Label

var cta_question_label: Label
var cta_button_panel: Panel
var cta_button_label: Label

var theme_config: Dictionary = {}


func _init(
	ui_root_node: Control,
	theme_name: String = "default_c6"
) -> void:

	container = ui_root_node

	if container:
		container.position = Vector2.ZERO
		container.size = Vector2(
			PresentationTheme.VIEWPORT_WIDTH,
			PresentationTheme.VIEWPORT_HEIGHT
		)
		container.set_anchors_preset(
			Control.PRESET_TOP_LEFT
		)

	theme_config = PresentationTheme.get_theme_config(
		theme_name
	)

	build_or_bind_elements()


func build_or_bind_elements() -> void:

	if container == null:
		return

	# =====================================================
	# HOOK
	# =====================================================

	hook_label = container.get_node_or_null(
		"HookLabel"
	) as Label

	if hook_label == null:
		hook_label = Label.new()
		hook_label.name = "HookLabel"
		container.add_child(hook_label)

	configure_top_label(
		hook_label,
		int(theme_config.get(
			"hook_font_size",
			36
		)),
		theme_config.get(
			"hook_color",
			Color.WHITE
		)
	)


	# =====================================================
	# REVEAL
	# =====================================================

	reveal_label = container.get_node_or_null(
		"RevealLabel"
	) as Label

	if reveal_label == null:
		reveal_label = Label.new()
		reveal_label.name = "RevealLabel"
		container.add_child(reveal_label)

	configure_reveal_label(
		reveal_label,
		int(theme_config.get(
			"reveal_font_size",
			32
		)),
		theme_config.get(
			"reveal_color",
			Color(0.2, 0.85, 0.3, 1.0)
		)
	)


	# =====================================================
	# DIFFICULTY BADGE
	# =====================================================

	difficulty_badge = container.get_node_or_null(
		"DifficultyBadge"
	) as Panel

	if difficulty_badge == null:
		difficulty_badge = Panel.new()
		difficulty_badge.name = "DifficultyBadge"
		container.add_child(difficulty_badge)

	configure_difficulty_badge(
		difficulty_badge
	)

	difficulty_label = difficulty_badge.get_node_or_null(
		"DifficultyText"
	) as Label

	if difficulty_label == null:
		difficulty_label = Label.new()
		difficulty_label.name = "DifficultyText"
		difficulty_badge.add_child(
			difficulty_label
		)

	configure_difficulty_label(
		difficulty_label,
		int(theme_config.get(
			"difficulty_font_size",
			16
		))
	)


	# =====================================================
	# COUNTDOWN
	# =====================================================

	countdown_label = container.get_node_or_null(
		"CountdownLabel"
	) as Label

	if countdown_label == null:
		countdown_label = Label.new()
		countdown_label.name = "CountdownLabel"
		container.add_child(countdown_label)

	configure_countdown_label(
		countdown_label,
		int(theme_config.get(
			"countdown_font_size",
			72
		)),
		theme_config.get(
			"countdown_color",
			Color.WHITE
		)
	)


	# =====================================================
	# CTA QUESTION
	# =====================================================

	cta_question_label = container.get_node_or_null(
		"CTALabel"
	) as Label

	if cta_question_label == null:
		cta_question_label = Label.new()
		cta_question_label.name = "CTALabel"
		container.add_child(
			cta_question_label
		)

	configure_cta_label(
		cta_question_label,
		int(theme_config.get(
			"cta_font_size",
			26
		)),
		theme_config.get(
			"cta_color",
			Color.WHITE
		)
	)


	# =====================================================
	# CTA BUTTON
	# =====================================================

	cta_button_panel = container.get_node_or_null(
		"ActionButtonPanel"
	) as Panel

	if cta_button_panel == null:
		cta_button_panel = Panel.new()
		cta_button_panel.name = "ActionButtonPanel"
		container.add_child(
			cta_button_panel
		)

	configure_cta_panel(
		cta_button_panel
	)

	cta_button_label = cta_button_panel.get_node_or_null(
		"ButtonText"
	) as Label

	if cta_button_label == null:
		cta_button_label = Label.new()
		cta_button_label.name = "ButtonText"
		cta_button_panel.add_child(
			cta_button_label
		)

	configure_button_label(
		cta_button_label,
		int(theme_config.get(
			"button_font_size",
			22
		))
	)

	_set_all_hidden()


# =========================================================
# FONT
# =========================================================

func apply_font_if_available(lbl: Label) -> void:

	if lbl == null:
		return

	var font = theme_config.get(
		"font",
		null
	)

	if font != null:
		lbl.add_theme_font_override(
			"font",
			font
		)


# =========================================================
# HOOK
# =========================================================

func configure_top_label(
	lbl: Label,
	font_size: int,
	color: Color
) -> void:

	lbl.position = Vector2(
		30.0,
		60.0
	)

	lbl.size = Vector2(
		480.0,
		80.0
	)

	lbl.horizontal_alignment = (
		HORIZONTAL_ALIGNMENT_CENTER
	)

	lbl.vertical_alignment = (
		VERTICAL_ALIGNMENT_CENTER
	)

	lbl.autowrap_mode = (
		TextServer.AUTOWRAP_WORD_SMART
	)

	lbl.add_theme_font_size_override(
		"font_size",
		font_size
	)

	lbl.add_theme_color_override(
		"font_color",
		color
	)

	apply_font_if_available(
		lbl
	)

	var outline_size := int(
		theme_config.get(
			"hook_outline_size",
			0
		)
	)

	if outline_size > 0:
		lbl.add_theme_constant_override(
			"outline_size",
			outline_size
		)

		lbl.add_theme_color_override(
			"outline_color",
			theme_config.get(
				"hook_outline_color",
				Color.BLACK
			)
		)


# =========================================================
# REVEAL
# =========================================================

func configure_reveal_label(
	lbl: Label,
	font_size: int,
	color: Color
) -> void:

	lbl.position = Vector2(
		30.0,
		60.0
	)

	lbl.size = Vector2(
		480.0,
		80.0
	)

	lbl.horizontal_alignment = (
		HORIZONTAL_ALIGNMENT_CENTER
	)

	lbl.vertical_alignment = (
		VERTICAL_ALIGNMENT_CENTER
	)

	lbl.autowrap_mode = (
		TextServer.AUTOWRAP_WORD_SMART
	)

	lbl.add_theme_font_size_override(
		"font_size",
		font_size
	)

	lbl.add_theme_color_override(
		"font_color",
		color
	)

	apply_font_if_available(
		lbl
	)

	var outline_size := int(
		theme_config.get(
			"reveal_outline_size",
			0
		)
	)

	if outline_size > 0:
		lbl.add_theme_constant_override(
			"outline_size",
			outline_size
		)

		lbl.add_theme_color_override(
			"outline_color",
			theme_config.get(
				"reveal_outline_color",
				Color.BLACK
			)
		)


# =========================================================
# DIFFICULTY
# =========================================================

func configure_difficulty_badge(
	panel: Panel
) -> void:

	var width := float(
		theme_config.get(
			"difficulty_width",
			96.0
		)
	)

	var height := float(
		theme_config.get(
			"difficulty_height",
			34.0
		)
	)

	panel.position = Vector2(
		420.0,
		22.0
	)

	panel.size = Vector2(
		width,
		height
	)

	var style := StyleBoxFlat.new()

	style.bg_color = theme_config.get(
		"difficulty_bg",
		Color(0.12, 0.12, 0.16, 0.90)
	)

	style.border_color = theme_config.get(
		"difficulty_border",
		Color(0.85, 0.85, 0.90, 1.0)
	)

	style.set_border_width_all(
		int(theme_config.get(
			"difficulty_border_width",
			2
		))
	)

	style.set_corner_radius_all(
		int(theme_config.get(
			"difficulty_corner_radius",
			8
		))
	)

	panel.add_theme_stylebox_override(
		"panel",
		style
)


func configure_difficulty_label(
	lbl: Label,
	font_size: int
) -> void:

	lbl.position = Vector2.ZERO
	lbl.size = difficulty_badge.size

	lbl.horizontal_alignment = (
		HORIZONTAL_ALIGNMENT_CENTER
	)

	lbl.vertical_alignment = (
		VERTICAL_ALIGNMENT_CENTER
	)

	lbl.add_theme_font_size_override(
		"font_size",
		font_size
	)

	lbl.add_theme_color_override(
		"font_color",
		theme_config.get(
			"difficulty_text_color",
			Color.WHITE
		)
	)

	apply_font_if_available(
		lbl
	)


# =========================================================
# COUNTDOWN
# =========================================================

func configure_countdown_label(
	lbl: Label,
	font_size: int,
	color: Color
) -> void:

	lbl.position = Vector2(
		0.0,
		380.0
	)

	lbl.size = Vector2(
		540.0,
		200.0
	)

	lbl.horizontal_alignment = (
		HORIZONTAL_ALIGNMENT_CENTER
	)

	lbl.vertical_alignment = (
		VERTICAL_ALIGNMENT_CENTER
	)

	lbl.add_theme_font_size_override(
		"font_size",
		font_size
	)

	lbl.add_theme_color_override(
		"font_color",
		color
	)

	apply_font_if_available(
		lbl
	)

	var outline_size := int(
		theme_config.get(
			"countdown_outline_size",
			0
		)
	)

	if outline_size > 0:
		lbl.add_theme_constant_override(
			"outline_size",
			outline_size
		)

		lbl.add_theme_color_override(
			"outline_color",
			theme_config.get(
				"countdown_outline_color",
				Color.BLACK
			)
		)


# =========================================================
# CTA
# =========================================================

func configure_cta_label(
	lbl: Label,
	font_size: int,
	color: Color
) -> void:

	lbl.position = Vector2(
		30.0,
		775.0
	)

	lbl.size = Vector2(
		480.0,
		55.0
	)

	lbl.horizontal_alignment = (
		HORIZONTAL_ALIGNMENT_CENTER
	)

	lbl.vertical_alignment = (
		VERTICAL_ALIGNMENT_CENTER
	)

	lbl.autowrap_mode = (
		TextServer.AUTOWRAP_WORD_SMART
	)

	lbl.add_theme_font_size_override(
		"font_size",
		font_size
	)

	lbl.add_theme_color_override(
		"font_color",
		color
	)

	apply_font_if_available(
		lbl
	)

	var outline_size := int(
		theme_config.get(
			"cta_outline_size",
			0
		)
	)

	if outline_size > 0:
		lbl.add_theme_constant_override(
			"outline_size",
			outline_size
		)

		lbl.add_theme_color_override(
			"outline_color",
			theme_config.get(
				"cta_outline_color",
				Color.BLACK
			)
		)


func configure_cta_panel(
	panel: Panel
) -> void:

	var btn_width := float(
		theme_config.get(
			"button_min_width",
			360.0
		)
	)

	var btn_height := float(
		theme_config.get(
			"button_height",
			64.0
		)
	)

	panel.position = Vector2(
		(
			PresentationTheme.VIEWPORT_WIDTH
			- btn_width
		) / 2.0,
		840.0
	)

	panel.size = Vector2(
		btn_width,
		btn_height
	)

	var style := StyleBoxFlat.new()

	style.bg_color = theme_config.get(
		"button_bg",
		Color(0.12, 0.12, 0.16, 0.95)
	)

	style.border_color = theme_config.get(
		"button_border",
		Color(0.85, 0.85, 0.90, 1.0)
	)

	style.set_border_width_all(
		int(theme_config.get(
			"button_border_width",
			2
		))
	)

	style.set_corner_radius_all(
		int(theme_config.get(
			"button_corner_radius",
			12
		))
	)

	style.shadow_color = Color(
		0.0,
		0.0,
		0.0,
		0.35
	)

	style.shadow_size = 8
	style.shadow_offset = Vector2(
		0.0,
		4.0
	)

	panel.add_theme_stylebox_override(
		"panel",
		style
)


func configure_button_label(
	lbl: Label,
	font_size: int
) -> void:

	lbl.position = Vector2.ZERO
	lbl.size = cta_button_panel.size

	lbl.horizontal_alignment = (
		HORIZONTAL_ALIGNMENT_CENTER
	)

	lbl.vertical_alignment = (
		VERTICAL_ALIGNMENT_CENTER
	)

	lbl.add_theme_font_size_override(
		"font_size",
		font_size
	)

	lbl.add_theme_color_override(
		"font_color",
		theme_config.get(
			"button_text_color",
			Color.WHITE
		)
	)

	apply_font_if_available(
		lbl
	)


# =========================================================
# VISIBILIDAD
# =========================================================

func _set_all_hidden() -> void:

	if hook_label:
		hook_label.visible = false

	if reveal_label:
		reveal_label.visible = false

	if difficulty_badge:
		difficulty_badge.visible = false

	if countdown_label:
		countdown_label.visible = false

	if cta_question_label:
		cta_question_label.visible = false

	if cta_button_panel:
		cta_button_panel.visible = false


# =========================================================
# ESTADO
# =========================================================

func set_state(
	state: String,
	content: Dictionary,
	state_frame: int = 0,
	fps: int = 60
) -> void:

	_set_all_hidden()

	# El nivel es HUD persistente durante todo el vídeo.
	if (
		difficulty_badge != null
		and difficulty_label != null
		and content.has("difficulty_level")
	):
		difficulty_label.text = (
			"NIVEL "
			+ str(content["difficulty_level"])
		)

		difficulty_badge.visible = true


	match state:

		"HOOK":
			if hook_label:
				hook_label.text = str(
					content.get(
						"hook",
						"¡RETO EN CURSO!"
					)
				)

				hook_label.add_theme_color_override(
					"font_color",
					theme_config.get(
						"hook_color",
						Color.WHITE
					)
				)

				hook_label.visible = true


		"GAME":
			# Juego limpio salvo el DifficultyBadge.
			pass


		"REVEAL":
			if reveal_label:
				reveal_label.text = (
					"🎯 ¡LO HAS CLAVADO!"
				)

				reveal_label.visible = true

			if countdown_label and fps > 0:

				# Reveal = exactamente 3 s.
				# 0-59   -> 3
				# 60-119 -> 2
				# 120-179 -> 1
				var seconds_left := (
					3
					- int(
						state_frame / fps
					)
				)

				if seconds_left < 1:
					seconds_left = 1

				countdown_label.text = str(
					seconds_left
				)

				countdown_label.visible = true


		"CTA":
			if cta_question_label:

				cta_question_label.text = str(
					content.get(
						"cta",
						"¿Lo has clavado?"
					)
				)

				cta_question_label.visible = true

			if cta_button_panel:

				if cta_button_label:
					cta_button_label.text = (
						"JUGAR OTRA VEZ"
					)

				cta_button_panel.visible = true