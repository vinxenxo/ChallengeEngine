# res://core/presentation/components/CTAComponent.gd
extends VBoxContainer
class_name CTAComponent

var label_main: TypographyLabel
var label_sub: TypographyLabel

func _init() -> void:
    alignment = BoxContainer.ALIGNMENT_CENTER
    add_theme_constant_override("separation", 2)
    mouse_filter = Control.MOUSE_FILTER_IGNORE

    label_main = TypographyLabel.new()
    label_main.role = TypographyLabel.Role.CTA
    label_main.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
    label_main.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
    label_main.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    add_child(label_main)

    label_sub = TypographyLabel.new()
    label_sub.role = TypographyLabel.Role.BODY
    label_sub.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
    label_sub.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
    label_sub.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    add_child(label_sub)

func configure(
    text: String,
    subtext: String,
    profile: PresentationProfile,
    colors: Dictionary = {}
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
    var secondary: Color = profile.colors.get(
        "primary",
        Color.WHITE
    )
    if colors is Dictionary:
        accent = _to_color(colors.get("cta_main", colors.get("accent", accent)), accent)
        secondary = _to_color(colors.get("cta_sub", colors.get("text_secondary", secondary)), secondary)

    label_main.add_theme_color_override("font_color", accent)
    label_sub.add_theme_color_override("font_color", secondary)

    label_main.add_theme_color_override("font_outline_color", Color(0.0, 0.0, 0.0, 0.72))
    label_sub.add_theme_color_override("font_outline_color", Color(0.0, 0.0, 0.0, 0.78))
    label_main.add_theme_constant_override("outline_size", 2)
    label_sub.add_theme_constant_override("outline_size", 1)

func apply_presentation_motion(progress: float) -> void:
    var p := clampf(progress, 0.0, 1.0)
    var eased := 1.0 - pow(1.0 - p, 3.0)
    var alpha := lerpf(0.0, 1.0, eased)
    var entry_scale := lerpf(0.88, 1.0, eased)
    var pulse := 1.0 + sin(p * PI) * 0.012
    pivot_offset = size * 0.5
    scale = Vector2.ONE * entry_scale * pulse
    modulate = Color(1.0, 1.0, 1.0, alpha)

func reset_presentation_motion() -> void:
    pivot_offset = size * 0.5
    scale = Vector2.ONE
    modulate = Color.WHITE

func _to_color(value, fallback: Color) -> Color:
    if value is Color:
        return value
    if value is String:
        return Color(str(value))
    return fallback
