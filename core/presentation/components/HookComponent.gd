extends TypographyLabel
class_name HookComponent

func _init() -> void:
	role = TypographyLabel.Role.HEADLINE
	horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	set_anchors_preset(Control.PRESET_TOP_WIDE)
	grow_horizontal = Control.GROW_DIRECTION_BOTH
	grow_vertical = Control.GROW_DIRECTION_END

func update_from_state(state: String, content: Dictionary) -> void:
	visible = false
	text = ""

	if state != "HOOK":
		return

	text = str(content.get("hook", ""))
	visible = not text.is_empty()