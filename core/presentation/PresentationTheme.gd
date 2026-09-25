# res://core/presentation/PresentationTheme.gd
class_name PresentationTheme
extends RefCounted

const VIEWPORT_WIDTH: float = 540.0
const VIEWPORT_HEIGHT: float = 960.0

const C11CVisualTypographyClass = preload("res://core/presentation/C11CVisualTypography.gd")

# Compatibility alias retained for legacy callers. Active presentations now resolve
# through the shared role-based C11-C typography service.
const FONT_PATH: String = C11CVisualTypographyClass.HEADER_FONT_PATH
const HEADER_FONT_PATH: String = C11CVisualTypographyClass.HEADER_FONT_PATH
const FOOTER_FONT_PATH: String = C11CVisualTypographyClass.FOOTER_FONT_PATH

static func get_theme_config(theme_name: String) -> Dictionary:
	var custom_font: Font = C11CVisualTypographyClass.get_header_font()
	var footer_font: Font = C11CVisualTypographyClass.get_footer_font()

	return {
		"font": custom_font,
		"header_font": custom_font,
		"footer_font": footer_font,
		"hook_font_size": 36,
		"reveal_font_size": 32,
		"cta_font_size": 26,
		"button_font_size": 22,
		"hook_color": Color.WHITE,
		"hook_outline_size": 6,
		"hook_outline_color": Color(0.0, 0.0, 0.0, 0.85),
		"reveal_color": Color(0.2, 0.85, 0.3, 1.0),
		"reveal_outline_size": 6,
		"reveal_outline_color": Color(0.0, 0.0, 0.0, 0.85),
		"cta_color": Color.WHITE,
		"cta_outline_size": 4,
		"cta_outline_color": Color(0.0, 0.0, 0.0, 0.85),
		"button_bg": Color(0.12, 0.12, 0.16, 0.95),
		"button_border": Color(0.85, 0.85, 0.9, 1.0),
		"button_border_width": 2,
		"button_corner_radius": 12,
		"button_text_color": Color.WHITE,
		"button_min_width": 360.0,
		"button_height": 64.0,
		"difficulty_font_size": 16,
		"difficulty_text_color": Color.WHITE,
		"difficulty_bg": Color(0.12, 0.12, 0.16, 0.90),
		"difficulty_border": Color(0.85, 0.85, 0.9, 1.0),
		"difficulty_border_width": 2,
		"difficulty_corner_radius": 8,
		"difficulty_width": 90.0,
		"difficulty_height": 34.0,
		"countdown_font_size": 72,
		"countdown_color": Color.WHITE,
		"countdown_outline_size": 8,
		"countdown_outline_color": Color(0.0, 0.0, 0.0, 0.90)
	}
