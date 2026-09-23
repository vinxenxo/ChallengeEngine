# res://core/presentation/C11CVisualEditorialLayer.gd
class_name C11CVisualEditorialLayer
extends RefCounted

## C11-C 2.2.2 — Shared visual-content social/editorial presentation layer.
## Common to Visual Loops and Visual Drills.
## Presentation-only: never owns simulation, RNG, timing truth or mechanics.

const C11CHeaderAnimatorV2Class = preload("res://tools/prototypes/c11c_common/C11CHeaderAnimatorV2.gd")

const LOGICAL_CANVAS_SIZE := Vector2(540.0, 960.0)
const HEADER_HEIGHT := 144.0
const FOOTER_HEIGHT := 144.0
const CONTENT_WIDTH := 468.0
const CONTENT_X := 36.0
const HEADER_MAX_WIDTH := CONTENT_WIDTH
const HEADER_FONT_SIZE := 23
const HEADER_MIN_FONT_SIZE := 15
const HEADER_SECOND_Y := 74.0
const HEADER_SECOND_HEIGHT := 64.0
const HEADER_BOLD_EMBOLDEN := 0.70
const FOOTER_FONT_SIZE := 14
const FOOTER_MIN_FONT_SIZE := 11
const FOOTER_LINE_Y := 20.0
const FOOTER_LINE_HEIGHT := 34.0
const HEADER_SEPARATOR_Y := 140.0
const FOOTER_SEPARATOR_Y := 14.0
const SECTION_BACKGROUND := Color("05070B")

var _frame: UnifiedSocialFrame
var _header_root: Control
var _footer_root: Control
var _header_container: Control
var _footer_container: Control
var _header_line_2: Label
var _footer_line_1: Label
var _header_rule: ColorRect
var _footer_rule: ColorRect
var _header_background: ColorRect
var _footer_background: ColorRect
var _mounted: bool = false
var _animator: RefCounted = null
var _animator_seed: int = 0
var _animator_sequence_signature: String = ""

func mount(frame: UnifiedSocialFrame) -> bool:
    if frame == null:
        return false
    _frame = frame
    _header_root = frame.get_header_content_root()
    _footer_root = frame.get_footer_content_root()
    if _header_root == null or _footer_root == null:
        return false

    _clear_mount(_header_root, "C11CVisualEditorialHeader")
    _clear_mount(_footer_root, "C11CVisualEditorialFooter")

    _header_container = Control.new()
    _header_container.name = "C11CVisualEditorialHeader"
    _header_container.set_anchors_preset(Control.PRESET_FULL_RECT)
    _header_container.mouse_filter = Control.MOUSE_FILTER_IGNORE

    _footer_container = Control.new()
    _footer_container.name = "C11CVisualEditorialFooter"
    _footer_container.set_anchors_preset(Control.PRESET_FULL_RECT)
    _footer_container.mouse_filter = Control.MOUSE_FILTER_IGNORE

    _header_root.add_child(_header_container)
    _footer_root.add_child(_footer_container)

    _header_background = _new_background("C11CHeaderBackground", HEADER_HEIGHT)
    _footer_background = _new_background("C11CFooterBackground", FOOTER_HEIGHT)
    _header_container.add_child(_header_background)
    _footer_container.add_child(_footer_background)

    # The former first header text keeps its entire upper space; only the
    # double-line header block remains visible there. The rule moves below it.
    _header_rule = _new_rule("C11CHeaderRule", Vector2(CONTENT_X, HEADER_SEPARATOR_Y))
    _footer_rule = _new_rule("C11CFooterRule", Vector2(CONTENT_X, FOOTER_SEPARATOR_Y))
    _header_container.add_child(_header_rule)
    _footer_container.add_child(_footer_rule)

    _header_line_2 = _new_label(
        "C11CHeaderLine2",
        Vector2(0.0, HEADER_SECOND_Y),
        Vector2(LOGICAL_CANVAS_SIZE.x, HEADER_SECOND_HEIGHT),
        HEADER_FONT_SIZE
    )
    _footer_line_1 = _new_label(
        "C11CFooterLine1",
        Vector2(0.0, FOOTER_LINE_Y),
        Vector2(LOGICAL_CANVAS_SIZE.x, FOOTER_LINE_HEIGHT),
        FOOTER_FONT_SIZE
    )
    _header_line_2 = _apply_bold(_header_line_2)
    _footer_line_1 = _apply_bold(_footer_line_1)

    _header_container.add_child(_header_line_2)
    _footer_container.add_child(_footer_line_1)
    _mounted = true
    return true

func apply_render_model(render_model: Dictionary) -> void:
    if not _mounted:
        return

    var editorial_variant: Variant = render_model.get("editorial", {})
    if not editorial_variant is Dictionary:
        _hide_all()
        return
    var editorial: Dictionary = editorial_variant
    if not bool(editorial.get("enabled", false)):
        _hide_all()
        return

    _show_all()

    var header_variant: Variant = editorial.get("header", {})
    var footer_variant: Variant = editorial.get("footer", {})
    var colors_variant: Variant = editorial.get("colors", {})
    var header: Dictionary = header_variant if header_variant is Dictionary else {}
    var footer: Dictionary = footer_variant if footer_variant is Dictionary else {}
    var colors: Dictionary = colors_variant if colors_variant is Dictionary else {}

    var header_secondary: Color = _to_color(colors.get("header_secondary", Color("D6E8FF")))
    var footer_data: Color = _to_color(colors.get("footer_data", Color("FFFFFF")))
    var rule_color: Color = _to_color(colors.get("rule", header_secondary))

    var header_primary_text: String = str(header.get("line_1", "")).strip_edges().to_upper()
    var header_double_text: String = _wrap_two_lines(str(header.get("line_2", "")).strip_edges().to_upper())
    var footer_line_1: String = str(footer.get("line_1", "")).strip_edges().to_upper()
    var footer_removed_2: String = _wrap_two_lines(str(footer.get("line_2", "")).strip_edges().to_upper())
    var footer_removed_3: String = _wrap_two_lines(str(footer.get("line_3", "")).strip_edges().to_upper())

    var matrix_enabled: bool = bool(editorial.get("matrix_enabled", true))
    if matrix_enabled:
        var sequence: Array[String] = [
            header_double_text,
            _wrap_two_lines(header_primary_text),
            footer_removed_2,
            footer_removed_3
        ]
        var sequence_signature := "|".join(sequence)
        var seed_value := int(render_model.get("editorial_seed", 314159))
        if _animator == null or _animator_seed != seed_value:
            _animator = C11CHeaderAnimatorV2Class.new(header_double_text, header_primary_text, seed_value)
            _animator_seed = seed_value
            _animator_sequence_signature = ""
        if _animator_sequence_signature != sequence_signature and _animator != null and _animator.has_method("set_sequence"):
            _animator.call("set_sequence", sequence)
            _animator_sequence_signature = sequence_signature

        var frame_index := int(render_model.get("editorial_frame_index", 0))
        var frame_count := int(render_model.get("editorial_frame_count", 1))
        var animated: Dictionary = _animator.call("display_sequence_at", frame_index, frame_count)
        _header_line_2.text = str(animated.get("text", header_double_text))
        _header_line_2.modulate = Color(1.0, 1.0, 1.0, 0.90 if bool(animated.get("transition", false)) else 1.0)
    else:
        _animator = null
        _animator_sequence_signature = ""
        _header_line_2.text = header_double_text
        _header_line_2.modulate = Color.WHITE

    _header_line_2.add_theme_color_override("font_color", header_secondary)
    _footer_line_1.text = footer_line_1
    _footer_line_1.add_theme_color_override("font_color", footer_data)

    _fit_label(_header_line_2, _header_line_2.text, HEADER_FONT_SIZE, HEADER_MIN_FONT_SIZE, HEADER_MAX_WIDTH)
    _fit_label(_footer_line_1, footer_line_1, FOOTER_FONT_SIZE, FOOTER_MIN_FONT_SIZE, 508.0)

    _header_rule.color = _with_alpha(rule_color, 0.34)
    _footer_rule.color = _with_alpha(rule_color, 0.34)
    _header_rule.visible = bool(editorial.get("show_header_rule", true))
    _footer_rule.visible = bool(editorial.get("show_footer_rule", true))
    _header_container.visible = bool(editorial.get("show_header", true))
    _footer_container.visible = bool(editorial.get("show_footer", true))

func clear() -> void:
    _mounted = false
    _animator = null
    _animator_sequence_signature = ""
    _frame = null
    _header_root = null
    _footer_root = null
    _header_container = null
    _footer_container = null

func _new_background(node_name: String, height: float) -> ColorRect:
    var rect := ColorRect.new()
    rect.name = node_name
    rect.position = Vector2.ZERO
    rect.size = Vector2(LOGICAL_CANVAS_SIZE.x, height)
    rect.color = SECTION_BACKGROUND
    rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
    rect.z_index = -100
    return rect

func _new_rule(node_name: String, position_value: Vector2) -> ColorRect:
    var rule := ColorRect.new()
    rule.name = node_name
    rule.position = position_value
    rule.size = Vector2(CONTENT_WIDTH, 1.0)
    rule.mouse_filter = Control.MOUSE_FILTER_IGNORE
    return rule

func _new_label(node_name: String, position_value: Vector2, size_value: Vector2, font_size: int) -> Label:
    var label := Label.new()
    label.name = node_name
    label.position = position_value
    label.size = size_value
    label.mouse_filter = Control.MOUSE_FILTER_IGNORE
    label.add_theme_font_size_override("font_size", font_size)
    label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
    label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
    label.clip_text = true
    label.add_theme_constant_override("outline_size", 1)
    label.add_theme_constant_override("line_spacing", 0)
    return label

func _apply_bold(label: Label) -> Label:
    var base_font: Font = label.get_theme_default_font()
    if base_font == null:
        return label
    var bold_font := FontVariation.new()
    bold_font.base_font = base_font
    bold_font.variation_embolden = HEADER_BOLD_EMBOLDEN
    label.add_theme_font_override("font", bold_font)
    return label

func _fit_label(label: Label, text_value: String, max_font_size: int, min_font_size: int, max_width: float) -> void:
    if label == null:
        return
    var font: Font = label.get_theme_default_font()
    if font == null:
        return
    var fitted: int = max_font_size
    var lines := text_value.split("\n", true)
    while fitted > min_font_size:
        var widest: float = 0.0
        for line in lines:
            widest = maxf(widest, font.get_string_size(line, HORIZONTAL_ALIGNMENT_LEFT, -1, fitted).x)
        if widest <= max_width:
            break
        fitted -= 1
    label.add_theme_font_size_override("font_size", fitted)

func _wrap_two_lines(text_value: String) -> String:
    var clean := text_value.strip_edges().replace("\r", "").replace("\n", " ")
    var words: PackedStringArray = clean.split(" ", false)
    if words.size() <= 1:
        return clean
    var font: Font = _header_line_2.get_theme_default_font() if _header_line_2 != null else null
    if font == null:
        return clean
    var measure_font := FontVariation.new()
    measure_font.base_font = font
    measure_font.variation_embolden = HEADER_BOLD_EMBOLDEN
    var best_break: int = 1
    var best_score: float = 1.0e30
    for i in range(1, words.size()):
        var left: String = " ".join(words.slice(0, i))
        var right: String = " ".join(words.slice(i))
        var left_width := measure_font.get_string_size(left, HORIZONTAL_ALIGNMENT_LEFT, -1, HEADER_FONT_SIZE).x
        var right_width := measure_font.get_string_size(right, HORIZONTAL_ALIGNMENT_LEFT, -1, HEADER_FONT_SIZE).x
        var max_line := maxf(left_width, right_width)
        var overflow := maxf(0.0, max_line - HEADER_MAX_WIDTH)
        var balance := absf(left_width - right_width)
        var score := overflow * 100000.0 + balance
        if score < best_score:
            best_score = score
            best_break = i
    return " ".join(words.slice(0, best_break)) + "\n" + " ".join(words.slice(best_break))

func _to_color(value) -> Color:
    if value is Color:
        return value
    if value is String:
        return Color(str(value))
    return Color("FFFFFF")

func _with_alpha(color_value: Color, alpha: float) -> Color:
    var result := color_value
    result.a = clampf(alpha, 0.0, 1.0)
    return result

func _clear_mount(parent: Control, child_name: String) -> void:
    var existing := parent.get_node_or_null(child_name)
    if existing != null:
        existing.free()

func _hide_all() -> void:
    if _header_container != null:
        _header_container.visible = false
    if _footer_container != null:
        _footer_container.visible = false

func _show_all() -> void:
    if _header_container != null:
        _header_container.visible = true
    if _footer_container != null:
        _footer_container.visible = true
