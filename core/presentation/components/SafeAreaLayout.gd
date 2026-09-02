extends MarginContainer
class_name SafeAreaLayout

func _init() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)

func apply_profile(profile: PresentationProfile) -> void:
	if profile == null:
		return

	var safe: Rect2 = profile.safe_area
	var canvas: Vector2 = profile.source_canvas_size

	var left: float = safe.position.x
	var top: float = safe.position.y
	var right: float = canvas.x - safe.end.x
	var bottom: float = canvas.y - safe.end.y

	add_theme_constant_override("margin_left", int(left))
	add_theme_constant_override("margin_top", int(top))
	add_theme_constant_override("margin_right", int(right))
	add_theme_constant_override("margin_bottom", int(bottom))