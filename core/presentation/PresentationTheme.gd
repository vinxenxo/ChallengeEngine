class_name PresentationTheme
extends RefCounted

const VIEWPORT_WIDTH: float = 540.0
const VIEWPORT_HEIGHT: float = 960.0

static func get_theme_config(theme_name: String) -> Dictionary:
	return {
		"hook_font_size": 34,
		"reveal_font_size": 32,
		"cta_font_size": 24,
		"button_font_size": 22,
		
		"hook_color": Color.WHITE,
		"hook_outline_size": 6,
		"hook_outline_color": Color(0.0, 0.0, 0.0, 0.85),
		
		"reveal_color": Color(0.2, 0.85, 0.3, 1.0),
		
		"cta_color": Color.WHITE,
		"cta_outline_size": 4,
		"cta_outline_color": Color(0.0, 0.0, 0.0, 0.85),
		
		"button_bg": Color(0.12, 0.12, 0.16, 0.95),
		"button_border": Color(0.85, 0.85, 0.9, 1.0),
		"button_border_width": 2,
		"button_corner_radius": 12,
		"button_text_color": Color.WHITE,
		"button_min_width": 360.0,
		"button_height": 64.0
	}