class_name C11CVisualTypography
extends RefCounted

## C11-C 2.10.1 — shared typography service.
## Presentation-only. C11-C Visual Drills and Visual Loops use role-based fonts.
## Legacy C6 typography remains untouched.

const HEADER_FONT_PATH: String = "res://assets/fonts/Inter-Bold.otf"
const FOOTER_FONT_PATH: String = "res://assets/fonts/NotoSansMono-Regular.ttf"
# Compatibility alias for callers that still request the shared C11-C font.
const FONT_PATH: String = HEADER_FONT_PATH

static func get_header_font() -> Font:
    var resource: Resource = load(HEADER_FONT_PATH)
    return resource as Font

static func get_footer_font() -> Font:
    var resource: Resource = load(FOOTER_FONT_PATH)
    return resource as Font

static func get_font(role: String = "header") -> Font:
    return get_footer_font() if role.to_lower() == "footer" else get_header_font()

static func apply_header_to_label(label: Label) -> void:
    if label == null:
        return
    var font: Font = get_header_font()
    if font != null:
        label.add_theme_font_override("font", font)

static func apply_footer_to_label(label: Label) -> void:
    if label == null:
        return
    var font: Font = get_footer_font()
    if font != null:
        label.add_theme_font_override("font", font)

static func apply_to_label(label: Label) -> void:
    apply_header_to_label(label)

static func apply_header_to_typography_label(label: TypographyLabel) -> void:
    if label == null:
        return
    var font: Font = get_header_font()
    if font != null:
        label.apply_font(font)

static func apply_footer_to_typography_label(label: TypographyLabel) -> void:
    if label == null:
        return
    var font: Font = get_footer_font()
    if font != null:
        label.apply_font(font)

static func apply_to_typography_label(label: TypographyLabel) -> void:
    apply_header_to_typography_label(label)

static func metadata() -> Dictionary:
    return {
        "header": {"family": "Inter", "style": "Bold", "path": HEADER_FONT_PATH, "license": "SIL Open Font License 1.1"},
        "footer": {"family": "Noto Sans Mono", "style": "Regular", "path": FOOTER_FONT_PATH, "license": "SIL Open Font License 1.1"}
    }
