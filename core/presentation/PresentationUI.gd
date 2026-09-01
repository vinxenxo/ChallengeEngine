class_name PresentationUI
extends RefCounted

var container: Control
var hook_label: Label
var reveal_label: Label
var cta_question_label: Label
var cta_button_panel: Panel
var cta_button_label: Label
var difficulty_badge: Panel
var difficulty_label: Label
var countdown_label: Label
var theme_config: Dictionary = {}

func _init(root: Control, theme_name: String = "default_c6") -> void:
	container = root
	theme_config = PresentationTheme.get_theme_config(theme_name)
	build_or_bind_elements()
	set_state("HOOK", {})

func build_or_bind_elements() -> void:
	if container == null:
		return

	hook_label = _get_or_create_label("HookLabel")
	reveal_label = _get_or_create_label("RevealLabel")
	cta_question_label = _get_or_create_label("CTALabel")
	countdown_label = _get_or_create_label("CountdownLabel")
	difficulty_badge = _get_or_create_panel("DifficultyBadge")
	difficulty_label = _get_or_create_child_label(difficulty_badge, "DifficultyText")
	cta_button_panel = _get_or_create_panel("ActionButtonPanel")
	cta_button_label = _get_or_create_child_label(cta_button_panel, "ButtonText")

	_apply_label_defaults(hook_label)
	_apply_label_defaults(reveal_label)
	_apply_label_defaults(cta_question_label)
	_apply_label_defaults(countdown_label)
	_apply_label_defaults(difficulty_label)
	_apply_label_defaults(cta_button_label)

	_apply_layout()
	_apply_theme()

func _get_or_create_label(node_name: String) -> Label:
	var node := container.get_node_or_null(node_name) as Label
	if node == null:
		node = Label.new()
		node.name = node_name
		container.add_child(node)
	return node

func _get_or_create_panel(node_name: String) -> Panel:
	var node := container.get_node_or_null(node_name) as Panel
	if node == null:
		node = Panel.new()
		node.name = node_name
		container.add_child(node)
	return node

func _get_or_create_child_label(parent: Panel, node_name: String) -> Label:
	if parent == null:
		return null
	var node := parent.get_node_or_null(node_name) as Label
	if node == null:
		node = Label.new()
		node.name = node_name
		parent.add_child(node)
	return node

func _apply_label_defaults(label: Label) -> void:
	if label == null:
		return
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE

func _apply_font_if_available(label: Label) -> void:
	if label == null:
		return
	var font = theme_config.get("font", null)
	if font is Font:
		label.add_theme_font_override("font", font)

func _apply_layout() -> void:
	if hook_label != null:
		hook_label.position = Vector2(30.0, 60.0)
		hook_label.size = Vector2(480.0, 80.0)

	if reveal_label != null:
		reveal_label.position = Vector2(30.0, 60.0)
		reveal_label.size = Vector2(480.0, 80.0)

	if difficulty_badge != null:
		difficulty_badge.position = Vector2(435.0, 22.0)
		difficulty_badge.size = Vector2(
			float(theme_config.get("difficulty_width", 90.0)),
			float(theme_config.get("difficulty_height", 34.0))
		)

	if difficulty_label != null:
		difficulty_label.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)

	if countdown_label != null:
		countdown_label.position = Vector2(0.0, 380.0)
		countdown_label.size = Vector2(540.0, 200.0)

	if cta_question_label != null:
		cta_question_label.position = Vector2(30.0, 775.0)
		cta_question_label.size = Vector2(480.0, 55.0)

	if cta_button_panel != null:
		var button_w := float(theme_config.get("button_min_width", 360.0))
		var button_h := float(theme_config.get("button_height", 64.0))
		cta_button_panel.position = Vector2(
			(PresentationTheme.VIEWPORT_WIDTH - button_w) * 0.5,
			840.0
		)
		cta_button_panel.size = Vector2(button_w, button_h)

	if cta_button_label != null:
		cta_button_label.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)

func _apply_theme() -> void:
	_apply_font_if_available(hook_label)
	_apply_font_if_available(reveal_label)
	_apply_font_if_available(cta_question_label)
	_apply_font_if_available(countdown_label)
	_apply_font_if_available(difficulty_label)
	_apply_font_if_available(cta_button_label)

	if hook_label != null:
		hook_label.add_theme_font_size_override("font_size", int(theme_config.get("hook_font_size", 36)))
		hook_label.add_theme_color_override("font_color", theme_config.get("hook_color", Color.WHITE))
		hook_label.add_theme_constant_override("outline_size", int(theme_config.get("hook_outline_size", 6)))
		hook_label.add_theme_color_override("font_outline_color", theme_config.get("hook_outline_color", Color.BLACK))

	if reveal_label != null:
		reveal_label.add_theme_font_size_override("font_size", int(theme_config.get("reveal_font_size", 32)))
		reveal_label.add_theme_color_override("font_color", theme_config.get("reveal_color", Color(0.2, 0.85, 0.3, 1.0)))
		reveal_label.add_theme_constant_override("outline_size", int(theme_config.get("reveal_outline_size", 6)))
		reveal_label.add_theme_color_override("font_outline_color", theme_config.get("reveal_outline_color", Color.BLACK))

	if cta_question_label != null:
		cta_question_label.add_theme_font_size_override("font_size", int(theme_config.get("cta_font_size", 26)))
		cta_question_label.add_theme_color_override("font_color", theme_config.get("cta_color", Color.WHITE))
		cta_question_label.add_theme_constant_override("outline_size", int(theme_config.get("cta_outline_size", 4)))
		cta_question_label.add_theme_color_override("font_outline_color", theme_config.get("cta_outline_color", Color.BLACK))

	if countdown_label != null:
		countdown_label.add_theme_font_size_override("font_size", int(theme_config.get("countdown_font_size", 72)))
		countdown_label.add_theme_color_override("font_color", theme_config.get("countdown_color", Color.WHITE))
		countdown_label.add_theme_constant_override("outline_size", int(theme_config.get("countdown_outline_size", 8)))
		countdown_label.add_theme_color_override("font_outline_color", theme_config.get("countdown_outline_color", Color.BLACK))

	if difficulty_label != null:
		difficulty_label.add_theme_font_size_override("font_size", int(theme_config.get("difficulty_font_size", 16)))
		difficulty_label.add_theme_color_override("font_color", theme_config.get("difficulty_text_color", Color.WHITE))

	if cta_button_label != null:
		cta_button_label.add_theme_font_size_override("font_size", int(theme_config.get("button_font_size", 22)))
		cta_button_label.add_theme_color_override("font_color", theme_config.get("button_text_color", Color.WHITE))

	if difficulty_badge != null:
		difficulty_badge.add_theme_stylebox_override("panel", _make_stylebox(
			theme_config.get("difficulty_bg", Color(0.12, 0.12, 0.16, 0.9)),
			theme_config.get("difficulty_border", Color(0.85, 0.85, 0.9, 1.0)),
			int(theme_config.get("difficulty_border_width", 2)),
			int(theme_config.get("difficulty_corner_radius", 8))
		))

	if cta_button_panel != null:
		cta_button_panel.add_theme_stylebox_override("panel", _make_stylebox(
			theme_config.get("button_bg", Color(0.12, 0.12, 0.16, 0.95)),
			theme_config.get("button_border", Color(0.85, 0.85, 0.9, 1.0)),
			int(theme_config.get("button_border_width", 2)),
			int(theme_config.get("button_corner_radius", 12))
		))

func _make_stylebox(bg: Color, border: Color, border_width: int, radius: int) -> StyleBoxFlat:
	var box := StyleBoxFlat.new()
	box.bg_color = bg
	box.border_color = border
	box.set_border_width_all(border_width)
	box.set_corner_radius_all(radius)
	return box


func _update_countdown(
	content: Dictionary,
	state: String
) -> void:
	if countdown_label == null:
		return

	# Estado por defecto: contador apagado.
	countdown_label.visible = false
	countdown_label.text = ""

	# La cuenta atrás SOLO existe al principio de GAME.
	if state != "GAME":
		return

	var fps: int = max(
		1,
		int(
			content.get(
				"ui_fps",
				60
			)
		)
	)

	var state_frame: int = max(
		0,
		int(
			content.get(
				"ui_state_frame",
				0
			)
		)
	)

	# Ventana fija de 3 segundos al inicio del GAME.
	var countdown_duration_frames: int = fps * 3

	if state_frame >= countdown_duration_frames:
		return

	var elapsed_seconds: int = (
		state_frame / fps
	)

	var countdown_value: int = (
		3 - elapsed_seconds
	)

	countdown_value = clampi(
		countdown_value,
		1,
		3
	)

	countdown_label.text = str(
		countdown_value
	)

	countdown_label.visible = true


func _set_phase_hidden() -> void:
	if hook_label != null:
		hook_label.visible = false
	if reveal_label != null:
		reveal_label.visible = false
	if cta_question_label != null:
		cta_question_label.visible = false
	if cta_button_panel != null:
		cta_button_panel.visible = false
	if countdown_label != null:
		countdown_label.visible = false
	# El badge de dificultad es persistente y NO se oculta entre fases.

func _set_difficulty(content: Dictionary) -> void:
	if difficulty_badge == null or difficulty_label == null:
		return
	var level := int(content.get("difficulty_level", 0))
	if level > 0:
		difficulty_label.text = "DIF. %d" % level
		difficulty_badge.visible = true
	else:
		difficulty_label.text = ""
		difficulty_badge.visible = false

func set_state(
	state: String,
	content: Dictionary
) -> void:
	if container == null:
		return

	# Estado visual base: todas las capas de fase ocultas.
	_set_phase_hidden()

	# El nivel de dificultad permanece independiente de la fase.
	_set_difficulty(content)

	# El countdown se gobierna EXCLUSIVAMENTE aquí.
	_update_countdown(
		content,
		state
	)

	match state:
		"HOOK":
			if hook_label != null:
				hook_label.text = str(
					content.get(
						"hook",
						""
					)
				)
				hook_label.visible = true

		"GAME":
			# No hacemos nada más.
			# El countdown ya ha sido resuelto por _update_countdown().
			pass

		"REVEAL":
			if reveal_label != null:
				reveal_label.text = (
					"🎯 ¡LO HAS CLAVADO!"
				)
				reveal_label.visible = true

		"CTA":
			if cta_question_label != null:
				cta_question_label.text = str(
					content.get(
						"cta",
						""
					)
				)
				cta_question_label.visible = true

			if cta_button_panel != null:
				cta_button_panel.visible = true

			if cta_button_label != null:
				cta_button_label.text = (
					"JUGAR OTRA VEZ"
				)