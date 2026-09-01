class_name PresentationUI
extends RefCounted

var container: Control
var hook_label: Label
var cta_question_label: Label
var cta_button_panel: Panel
var cta_button_label: Label

var theme_config: Dictionary = {}

func _init(ui_root_node: Control, theme_name: String = "default_c6") -> void:
	container = ui_root_node

	if container:
		container.position = Vector2.ZERO
		container.size = Vector2(
			PresentationTheme.VIEWPORT_WIDTH,
			PresentationTheme.VIEWPORT_HEIGHT
		)
		container.set_anchors_preset(Control.PRESET_TOP_LEFT)

	theme_config = PresentationTheme.get_theme_config(theme_name)
	build_or_bind_elements()

func build_or_bind_elements() -> void:
	if not container:
		return

	# 1. Hook / Reveal Label (Zona superior central mediante posiciones directas)
	hook_label = container.get_node_or_null("HookLabel") as Label
	if not hook_label:
		hook_label = Label.new()
		hook_label.name = "HookLabel"
		container.add_child(hook_label)
	configure_top_label(hook_label, int(theme_config.get("hook_font_size", 34)), theme_config.get("hook_color", Color.WHITE))

	# 2. CTA Question Label (Zona inferior segura pregunta)
	cta_question_label = container.get_node_or_null("CTALabel") as Label
	if not cta_question_label:
		cta_question_label = Label.new()
		cta_question_label.name = "CTALabel"
		container.add_child(cta_question_label)
	configure_cta_label(cta_question_label, int(theme_config.get("cta_font_size", 24)), theme_config.get("cta_color", Color.WHITE))

	# 3. CTA Button Panel + Label (Contenedor visual estilo social-video con sombra)
	cta_button_panel = container.get_node_or_null("ActionButtonPanel") as Panel
	if not cta_button_panel:
		cta_button_panel = Panel.new()
		cta_button_panel.name = "ActionButtonPanel"
		container.add_child(cta_button_panel)
	configure_cta_panel(cta_button_panel)

	cta_button_label = cta_button_panel.get_node_or_null("ButtonText") as Label
	if not cta_button_label:
		cta_button_label = Label.new()
		cta_button_label.name = "ButtonText"
		cta_button_panel.add_child(cta_button_label)
	configure_button_label(cta_button_label, int(theme_config.get("button_font_size", 22)))

func configure_top_label(lbl: Label, font_size: int, color: Color) -> void:
	lbl.position = Vector2(30.0, 65.0)
	lbl.size = Vector2(480.0, 70.0)

	lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	lbl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART

	lbl.add_theme_font_size_override("font_size", font_size)
	lbl.add_theme_color_override("font_color", color)

	var outline_size: int = int(theme_config.get("hook_outline_size", 0))
	if outline_size > 0:
		lbl.add_theme_constant_override("outline_size", outline_size)
		lbl.add_theme_color_override(
			"outline_color",
			theme_config.get("hook_outline_color", Color.BLACK)
		)

func configure_cta_label(lbl: Label, font_size: int, color: Color) -> void:
	lbl.position = Vector2(30.0, 780.0)
	lbl.size = Vector2(480.0, 50.0)

	lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	lbl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART

	lbl.add_theme_font_size_override("font_size", font_size)
	lbl.add_theme_color_override("font_color", color)

	var outline_size: int = int(theme_config.get("cta_outline_size", 0))
	if outline_size > 0:
		lbl.add_theme_constant_override("outline_size", outline_size)
		lbl.add_theme_color_override(
			"outline_color",
			theme_config.get("cta_outline_color", Color.BLACK)
		)

func configure_cta_panel(panel: Panel) -> void:
	var btn_width: float = float(
		theme_config.get("button_min_width", 360.0)
	)
	var btn_height: float = float(
		theme_config.get("button_height", 64.0)
	)

	panel.position = Vector2(
		(PresentationTheme.VIEWPORT_WIDTH - btn_width) / 2.0,
		845.0
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
		Color(0.85, 0.85, 0.9, 1.0)
	)

	style.set_border_width_all(
		int(theme_config.get("button_border_width", 2))
	)

	style.set_corner_radius_all(
		int(theme_config.get("button_corner_radius", 12))
	)

	style.shadow_color = Color(0.0, 0.0, 0.0, 0.35)
	style.shadow_size = 8
	style.shadow_offset = Vector2(0.0, 4.0)

	panel.add_theme_stylebox_override("panel", style)

func configure_button_label(lbl: Label, font_size: int) -> void:
	lbl.position = Vector2.ZERO
	lbl.size = cta_button_panel.size

	lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	lbl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER

	lbl.add_theme_font_size_override("font_size", font_size)
	lbl.add_theme_color_override(
		"font_color",
		theme_config.get("button_text_color", Color.WHITE)
	)

func set_state(state: String, content: Dictionary) -> void:
	if hook_label:
		hook_label.visible = false

	if cta_question_label:
		cta_question_label.visible = false

	if cta_button_panel:
		cta_button_panel.visible = false

	match state:
		"HOOK":
			if hook_label:
				hook_label.text = str(
					content.get("hook", "¡RETO EN CURSO!")
				)
				hook_label.add_theme_color_override(
					"font_color",
					theme_config.get("hook_color", Color.WHITE)
				)
				hook_label.visible = true

		"GAME":
			pass

		"REVEAL":
			if hook_label:
				hook_label.text = "✅ ¡COMPLETADO!"
				hook_label.add_theme_color_override(
					"font_color",
					theme_config.get(
						"reveal_color",
						Color(0.2, 0.85, 0.3, 1.0)
					)
				)
				hook_label.visible = true

		"CTA":
			if cta_question_label:
				cta_question_label.text = str(
					content.get("cta", "¿Lo has clavado?")
				)
				cta_question_label.visible = true

			if cta_button_panel:
				if cta_button_label:
					cta_button_label.text = "JUGAR OTRA VEZ"

				cta_button_panel.visible = true