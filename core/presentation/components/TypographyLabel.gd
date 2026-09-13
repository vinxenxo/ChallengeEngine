# res://core/presentation/components/TypographyLabel.gd
extends Label
class_name TypographyLabel

enum Role {
	HEADLINE,
	BODY,
	BADGE,
	CTA,
	COUNTDOWN
}

var role: int = Role.BODY

func apply_profile(profile: PresentationProfile) -> void:
	if profile == null:
		return

	autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	vertical_alignment = VERTICAL_ALIGNMENT_CENTER

	var typo: Dictionary = profile.typography

	var scale_factor: float = float(
		typo.get("scale", 1.0)
	)

	var font_size: int = int(
		typo.get("body_size", 32)
	)

	match role:
		Role.HEADLINE:
			font_size = int(
				typo.get("headline_size", 48)
			)

		Role.BODY:
			font_size = int(
				typo.get("body_size", 32)
			)

		Role.BADGE:
			font_size = int(
				typo.get("badge_size", 24)
			)

		Role.CTA:
			font_size = int(
				typo.get("cta_size", 36)
			)

		Role.COUNTDOWN:
			font_size = int(
				typo.get("countdown_size", 64)
			)

	var max_width: int = int(
		typo.get("max_text_width", 460)
	)

	custom_minimum_size.x = max_width

	add_theme_font_size_override(
		"font_size",
		int(font_size * scale_factor)
	)

func apply_font(font: Font) -> void:
	if font != null:
		add_theme_font_override("font", font)