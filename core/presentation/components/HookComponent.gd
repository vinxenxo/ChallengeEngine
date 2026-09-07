class_name HookComponent
extends Control

var label: TypographyLabel

func _init() -> void:
	label = TypographyLabel.new()
	label.role = TypographyLabel.Role.HEADLINE
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	label.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(label)

func apply_profile(profile: PresentationProfile) -> void:
	if label != null and profile != null:
		label.apply_profile(profile)

func apply_font(font: Font) -> void:
	if label != null and font != null:
		label.apply_font(font)

func apply_render_model(render_model: Dictionary) -> void:
	visible = render_model.get("show_hook", false)
	if label != null:
		label.text = render_model.get("hook_text", "")