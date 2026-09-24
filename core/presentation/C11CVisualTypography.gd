# res://core/presentation/C11CVisualTypography.gd
class_name C11CVisualTypography
extends RefCounted

## C11-C 2.9.0 — Shared typography utility for C11-C Visual content.
## Presentation-only. Keeps the C6/Challenge theme unchanged while ensuring
## newly authored C11-C text uses the approved technical/editorial font.

const FONT_PATH: String = "res://assets/fonts/courier-regular.ttf"

static func get_font() -> Font:
    var resource: Resource = load(FONT_PATH)
    return resource as Font

static func apply_to_label(label: Label) -> void:
    if label == null:
        return
    var font: Font = get_font()
    if font != null:
        label.add_theme_font_override("font", font)

static func apply_to_typography_label(label: TypographyLabel) -> void:
    if label == null:
        return
    var font: Font = get_font()
    if font != null:
        label.apply_font(font)
