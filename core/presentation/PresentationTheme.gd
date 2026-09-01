class_name PresentationTheme
extends RefCounted

const VIEWPORT_WIDTH: float = 540.0
const VIEWPORT_HEIGHT: float = 960.0

# Tipografía distribuida con la propia fábrica.
const FONT_PATH: String = "res://assets/fonts/Comic-Sans-MS.ttf"

static func get_theme_config(theme_name: String) -> Dictionary:
	var custom_font: Font = null
	var font_available: bool = false

	if ResourceLoader.exists(FONT_PATH):
		var loaded_font = load(FONT_PATH)
		if loaded_font is Font:
			custom_font = loaded_font
			font_available = true

	return {
		"theme_name": theme_name,

		"font": custom_font,
		"font_available": font_available,

		# -------------------------
		# HOOK
		# -------------------------
		"hook_font_size": 36,
		"hook_color": Color.WHITE,
		"hook_outline_size": 6,
		"hook_outline_color": Color(0.0, 0.0, 0.0, 0.85),

		# -------------------------
		# REVEAL
		# -------------------------
		"reveal_font_size": 32,
		"reveal_color": Color(0.2, 0.85, 0.3, 1.0),
		"reveal_outline_size": 6,
		"reveal_outline_color": Color(0.0, 0.0, 0.0, 0.85),

		# -------------------------
		# CTA
		# -------------------------
		"cta_font_size": 26,
		"cta_color": Color.WHITE,
		"cta_outline_size": 4,
		"cta_outline_color": Color(0.0, 0.0, 0.0, 0.85),

		# -------------------------
		# CTA BUTTON
		# -------------------------
		"button_font_size": 22,
		"button_text_color": Color.WHITE,
		"button_bg": Color(0.12, 0.12, 0.16, 0.95),
		"button_border": Color(0.85, 0.85, 0.9, 1.0),
		"button_border_width": 2,
		"button_corner_radius": 12,
		"button_min_width": 360.0,
		"button_height": 64.0,

		# -------------------------
		# DIFFICULTY
		# -------------------------
		"difficulty_font_size": 16,
		"difficulty_text_color": Color.WHITE,
		"difficulty_bg": Color(0.12, 0.12, 0.16, 0.90),
		"difficulty_border": Color(0.85, 0.85, 0.90, 1.0),
		"difficulty_border_width": 2,
		"difficulty_corner_radius": 8,
		"difficulty_width": 96.0,
		"difficulty_height": 34.0,

		# -------------------------
		# COUNTDOWN
		# -------------------------
		"countdown_font_size": 72,
		"countdown_color": Color.WHITE,
		"countdown_outline_size": 8,
		"countdown_outline_color": Color(0.0, 0.0, 0.0, 0.90)
	}