extends TypographyLabel
class_name CountdownComponent

func _init() -> void:
	role = TypographyLabel.Role.COUNTDOWN
	horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	set_anchors_preset(Control.PRESET_CENTER)
	grow_horizontal = Control.GROW_DIRECTION_BOTH
	grow_vertical = Control.GROW_DIRECTION_BOTH

func update_from_state(state: String, content: Dictionary) -> void:
	visible = false
	text = ""

	if state != "HOOK":
		return

	var fps: int = max(1, int(content.get("ui_fps", 60)))
	var state_frame: int = max(0, int(content.get("ui_state_frame", 0)))

	var countdown_value: int = 0

	if state_frame < fps:
		countdown_value = 3
	elif state_frame < fps * 2:
		countdown_value = 2
	elif state_frame < fps * 3:
		countdown_value = 1
	else:
		return

	text = str(countdown_value)
	visible = true