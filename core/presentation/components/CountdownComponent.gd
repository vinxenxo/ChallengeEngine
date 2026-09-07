class_name CountdownComponent
extends TypographyLabel

func _init() -> void:
	role = TypographyLabel.Role.COUNTDOWN
	horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	set_anchors_preset(Control.PRESET_CENTER)
	grow_horizontal = Control.GROW_DIRECTION_BOTH
	grow_vertical = Control.GROW_DIRECTION_BOTH

func apply_profile(profile: PresentationProfile) -> void:
	if profile != null:
		super.apply_profile(profile)

func apply_render_model(render_model: Dictionary) -> void:
	visible = bool(render_model.get("countdown_visible", false))
	text = str(render_model.get("countdown_value", ""))