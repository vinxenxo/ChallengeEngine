extends VBoxContainer
class_name CTAComponent

var label_main: TypographyLabel
var label_sub: TypographyLabel

func _init() -> void:
	alignment = BoxContainer.ALIGNMENT_CENTER

	label_main = TypographyLabel.new()
	label_main.role = TypographyLabel.Role.CTA
	label_main.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	add_child(label_main)

	label_sub = TypographyLabel.new()
	label_sub.role = TypographyLabel.Role.BODY
	label_sub.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	add_child(label_sub)

func configure(
	text: String,
	subtext: String,
	profile: PresentationProfile
) -> void:
	if profile == null:
		return

	label_main.text = text
	label_sub.text = subtext

	label_main.apply_profile(profile)
	label_sub.apply_profile(profile)

	var accent: Color = profile.colors.get(
		"accent",
		Color(1.0, 0.8, 0.0)
	)

	label_main.add_theme_color_override(
		"font_color",
		accent
	)