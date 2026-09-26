# res://core/presentation/C11CVisualEditorialLayer.gd
class_name C11CVisualEditorialLayer
extends RefCounted

## C11-C 2.16.2 — shared visual/editorial layer.
## Common to Visual Loops and Visual Drills.
## Presentation-only: never owns simulation, RNG, timing truth or mechanics.
## Global art-direction contract: 3-line header / up-to-3-line footer with visible separator rules and editorial spacing.

const C11CHeaderAnimatorV2Class = preload("res://tools/prototypes/c11c_common/C11CHeaderAnimatorV2.gd")
const C11CVisualTypographyClass = preload("res://core/presentation/C11CVisualTypography.gd")

const LOGICAL_CANVAS_SIZE := Vector2(540.0, 960.0)
const HEADER_HEIGHT := 144.0
const FOOTER_HEIGHT := 144.0
const CONTENT_WIDTH := 468.0
const CONTENT_X := 36.0
const HEADER_MAX_WIDTH := CONTENT_WIDTH
const HEADER_FONT_SIZE := 27
const HEADER_MIN_FONT_SIZE := 17
const HEADER_TEXT_Y := 0.0
const HEADER_TEXT_HEIGHT := 128.0
const HEADER_BOLD_EMBOLDEN := 0.70
const FOOTER_FONT_SIZE := 16
const FOOTER_MIN_FONT_SIZE := 12
const FOOTER_TEXT_Y := 28.0
const FOOTER_TEXT_HEIGHT := 116.0
const HEADER_SEPARATOR_Y := 140.0
const FOOTER_SEPARATOR_Y := 14.0
const SECTION_BACKGROUND := Color("05070B")

var _frame: UnifiedSocialFrame
var _header_root: Control
var _footer_root: Control
var _header_container: Control
var _footer_container: Control
var _header_text: Label
var _footer_text: Label
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

    _header_rule = _new_rule("C11CHeaderRule", Vector2(CONTENT_X, HEADER_SEPARATOR_Y))
    _footer_rule = _new_rule("C11CFooterRule", Vector2(CONTENT_X, FOOTER_SEPARATOR_Y))
    _header_container.add_child(_header_rule)
    _footer_container.add_child(_footer_rule)

    # One shared Label per region. Matrix states use the exact same font
    # resource, size and embolden role; only text content changes.
    _header_text = _new_label(
        "C11CHeaderText",
        Vector2(0.0, HEADER_TEXT_Y),
        Vector2(LOGICAL_CANVAS_SIZE.x, HEADER_TEXT_HEIGHT),
        HEADER_FONT_SIZE
    )
    _footer_text = _new_label(
        "C11CFooterText",
        Vector2(0.0, FOOTER_TEXT_Y),
        Vector2(LOGICAL_CANVAS_SIZE.x, FOOTER_TEXT_HEIGHT),
        FOOTER_FONT_SIZE,
        true
    )
    _header_container.add_child(_header_text)
    _footer_container.add_child(_footer_text)
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

    var header_primary: Color = _to_color(colors.get("header_primary", Color("FFFFFF")))
    var header_secondary: Color = _to_color(colors.get("header_secondary", Color("D6E8FF")))
    var footer_data: Color = _to_color(colors.get("footer_data", Color("FFFFFF")))
    var footer_secondary: Color = _to_color(colors.get("footer_secondary", Color("9CB8D8")))
    var rule_color: Color = _to_color(colors.get("rule", header_secondary))
    var section_background: Color = _to_color(colors.get("section_background", SECTION_BACKGROUND))

    var header_line_1: String = _single_line(str(header.get("line_1", "")).strip_edges().to_upper())
    var header_line_2: String = _single_line(str(header.get("line_2", "")).strip_edges().to_upper())
    var header_full_text: String = _compose_header_three_lines(header_line_1, header_line_2)
    var footer_full_text: String = _compose_footer_three_lines(footer)

    var matrix_enabled: bool = bool(editorial.get("matrix_enabled", true))
    var intro_active: bool = bool(editorial.get("intro_active", false))
    var intro_text: String = str(editorial.get("intro_text", "")).strip_edges().to_upper()

    # Every Matrix state is a 3-line block. The font size is calculated once
    # across the complete state sequence, preventing size jitter during swaps.
    var sequence: Array[String] = [
        header_full_text,
        _pad_three_lines(_wrap_three_lines(header_line_2)),
        _pad_three_lines(_wrap_three_lines(header_line_1)),
        _pad_three_lines(_wrap_footer_three_lines(str(footer.get("line_2", "")).strip_edges().to_upper())),
        _pad_three_lines(_wrap_footer_three_lines(str(footer.get("line_3", "")).strip_edges().to_upper()))
    ]
    var shared_header_font_size: int = _resolve_shared_header_font_size(sequence)
    _header_text.add_theme_font_size_override("font_size", shared_header_font_size)

    if intro_active and not intro_text.is_empty():
        _animator = null
        _animator_sequence_signature = ""
        _header_text.text = _pad_three_lines(_wrap_three_lines(intro_text))
        _header_text.modulate = Color(1.0, 1.0, 1.0, 0.96)
    elif matrix_enabled:
        var sequence_signature: String = "|".join(sequence)
        var seed_value: int = int(render_model.get("editorial_seed", 314159))
        if _animator == null or _animator_seed != seed_value:
            _animator = C11CHeaderAnimatorV2Class.new(header_full_text, header_line_2, seed_value)
            _animator_seed = seed_value
            _animator_sequence_signature = ""
        if _animator_sequence_signature != sequence_signature and _animator != null and _animator.has_method("set_sequence"):
            _animator.call("set_sequence", sequence)
            _animator_sequence_signature = sequence_signature
        var frame_index: int = int(render_model.get("editorial_frame_index", 0))
        var frame_count: int = int(render_model.get("editorial_frame_count", 1))
        var animated: Dictionary = _animator.call("display_sequence_at", frame_index, frame_count)
        _header_text.text = _pad_three_lines(str(animated.get("text", header_full_text)))
        _header_text.modulate = Color(1.0, 1.0, 1.0, 0.93 if bool(animated.get("transition", false)) else 1.0)
    else:
        _animator = null
        _animator_sequence_signature = ""
        _header_text.text = header_full_text
        _header_text.modulate = Color.WHITE

    _header_text.add_theme_color_override("font_color", header_primary if intro_active else header_secondary)
    _header_text.add_theme_color_override("font_outline_color", Color(0.0, 0.0, 0.0, 0.72))

    _footer_text.text = footer_full_text
    _footer_text.add_theme_color_override("font_color", footer_data)
    _footer_text.add_theme_color_override("font_outline_color", Color(0.0, 0.0, 0.0, 0.78))
    _fit_label(_footer_text, footer_full_text, FOOTER_FONT_SIZE, FOOTER_MIN_FONT_SIZE, 508.0)

    _header_rule.color = _with_alpha(rule_color, 0.34)
    _footer_rule.color = _with_alpha(rule_color, 0.34)
    # 2.16.1 restores the visible separator lines as part of the shared editorial composition.
    _header_rule.visible = true
    _footer_rule.visible = true
    _header_container.visible = bool(editorial.get("show_header", true))
    _footer_container.visible = bool(editorial.get("show_footer", true))
    if _header_background != null:
        _header_background.color = section_background
    if _footer_background != null:
        _footer_background.color = section_background

func clear() -> void:
    _mounted = false
    _animator = null
    _animator_sequence_signature = ""
    _frame = null
    _header_root = null
    _footer_root = null
    _header_container = null
    _footer_container = null
    _header_text = null
    _footer_text = null

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

func _new_label(node_name: String, position_value: Vector2, size_value: Vector2, font_size: int, footer_role: bool = false) -> Label:
    var label := Label.new()
    label.name = node_name
    label.position = position_value
    label.size = size_value
    label.mouse_filter = Control.MOUSE_FILTER_IGNORE
    label.add_theme_font_size_override("font_size", font_size)
    if footer_role:
        C11CVisualTypographyClass.apply_footer_to_label(label)
    else:
        C11CVisualTypographyClass.apply_header_to_label(label)
    label.vertical_alignment = VERTICAL_ALIGNMENT_TOP if footer_role else VERTICAL_ALIGNMENT_BOTTOM
    label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
    label.clip_text = true
    label.add_theme_constant_override("outline_size", 1)
    label.add_theme_constant_override("line_spacing", 0)
    return label

func _resolve_shared_header_font_size(blocks: Array[String]) -> int:
    if _header_text == null:
        return HEADER_FONT_SIZE
    var font: Font = _header_text.get_theme_font("font")
    if font == null:
        return HEADER_FONT_SIZE
    var fitted: int = HEADER_FONT_SIZE
    while fitted > HEADER_MIN_FONT_SIZE:
        var all_fit: bool = true
        for block in blocks:
            var widest: float = 0.0
            var lines: PackedStringArray = block.split("\n", true)
            for line in lines:
                widest = maxf(widest, font.get_string_size(line, HORIZONTAL_ALIGNMENT_LEFT, -1, fitted).x)
            if widest > HEADER_MAX_WIDTH:
                all_fit = false
                break
        if all_fit:
            break
        fitted -= 1
    return fitted

func _fit_label(label: Label, text_value: String, max_font_size: int, min_font_size: int, max_width: float) -> void:
    if label == null:
        return
    var font: Font = label.get_theme_font("font")
    if font == null:
        return
    var fitted: int = max_font_size
    var lines: PackedStringArray = text_value.split("\n", true)
    while fitted > min_font_size:
        var widest: float = 0.0
        for line in lines:
            widest = maxf(widest, font.get_string_size(line, HORIZONTAL_ALIGNMENT_LEFT, -1, fitted).x)
        if widest <= max_width:
            break
        fitted -= 1
    label.add_theme_font_size_override("font_size", fitted)

func _wrap_two_lines(text_value: String) -> String:
    var clean: String = text_value.strip_edges().replace("\r", "").replace("\n", " ")
    var words: PackedStringArray = clean.split(" ", false)
    if words.size() <= 1:
        return clean
    var font: Font = _header_text.get_theme_font("font") if _header_text != null else null
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
        var left_width: float = measure_font.get_string_size(left, HORIZONTAL_ALIGNMENT_LEFT, -1, HEADER_FONT_SIZE).x
        var right_width: float = measure_font.get_string_size(right, HORIZONTAL_ALIGNMENT_LEFT, -1, HEADER_FONT_SIZE).x
        var max_line: float = maxf(left_width, right_width)
        var overflow: float = maxf(0.0, max_line - HEADER_MAX_WIDTH)
        var balance: float = absf(left_width - right_width)
        var score: float = overflow * 100000.0 + balance
        if score < best_score:
            best_score = score
            best_break = i
    return " ".join(words.slice(0, best_break)) + "\n" + " ".join(words.slice(best_break))

func _wrap_three_lines(text_value: String) -> String:
    var clean: String = text_value.strip_edges().replace("\r", "").replace("\n", " ")
    var words: PackedStringArray = clean.split(" ", false)
    if words.size() <= 2:
        return clean
    var font: Font = _header_text.get_theme_font("font") if _header_text != null else null
    if font == null:
        return clean
    var measure_font := FontVariation.new()
    measure_font.base_font = font
    measure_font.variation_embolden = HEADER_BOLD_EMBOLDEN
    var best_a: int = 1
    var best_b: int = 2
    var best_score: float = 1.0e30
    for a in range(1, words.size() - 1):
        for b in range(a + 1, words.size()):
            var l1: String = " ".join(words.slice(0, a))
            var l2: String = " ".join(words.slice(a, b))
            var l3: String = " ".join(words.slice(b))
            var w1: float = measure_font.get_string_size(l1, HORIZONTAL_ALIGNMENT_LEFT, -1, HEADER_FONT_SIZE).x
            var w2: float = measure_font.get_string_size(l2, HORIZONTAL_ALIGNMENT_LEFT, -1, HEADER_FONT_SIZE).x
            var w3: float = measure_font.get_string_size(l3, HORIZONTAL_ALIGNMENT_LEFT, -1, HEADER_FONT_SIZE).x
            var max_line: float = maxf(w1, maxf(w2, w3))
            var balance: float = absf(w1 - w2) + absf(w2 - w3) + absf(w1 - w3)
            var overflow: float = maxf(0.0, max_line - HEADER_MAX_WIDTH)
            var score: float = overflow * 100000.0 + balance
            if score < best_score:
                best_score = score
                best_a = a
                best_b = b
    return " ".join(words.slice(0, best_a)) + "\n" + " ".join(words.slice(best_a, best_b)) + "\n" + " ".join(words.slice(best_b))

func _compose_header_three_lines(line_1: String, line_2: String) -> String:
    var primary: String = _single_line(line_1)
    var secondary: String = _single_line(line_2)
    if primary.is_empty():
        return _pad_three_lines(_wrap_three_lines(secondary))
    if secondary.is_empty():
        return _pad_three_lines(_wrap_three_lines(primary))
    return _pad_three_lines(primary + "\n" + _wrap_two_lines(secondary))

func _compose_footer_three_lines(footer: Dictionary) -> String:
    var line_1: String = _single_line(str(footer.get("line_1", "")).strip_edges().to_upper())
    var line_2: String = _single_line(str(footer.get("line_2", "")).strip_edges().to_upper())
    var line_3: String = _single_line(str(footer.get("line_3", "")).strip_edges().to_upper())
    var chunks: Array[String] = []
    for value in [line_1, line_2, line_3]:
        if not value.is_empty():
            chunks.append(value)
    if chunks.is_empty():
        return ""
    return _wrap_footer_three_lines(" | ".join(chunks))

func _wrap_footer_three_lines(text_value: String) -> String:
    var clean: String = text_value.strip_edges().replace("\r", "").replace("\n", " ")
    var words: PackedStringArray = clean.split(" ", false)
    if words.size() <= 1:
        return clean
    var font: Font = _footer_text.get_theme_font("font") if _footer_text != null else null
    if font == null:
        return clean
    var best_a: int = 1
    var best_b: int = mini(2, words.size() - 1)
    var best_score: float = 1.0e30
    for a in range(1, words.size() - 1):
        for b in range(a + 1, words.size()):
            var l1: String = " ".join(words.slice(0, a))
            var l2: String = " ".join(words.slice(a, b))
            var l3: String = " ".join(words.slice(b))
            var w1: float = font.get_string_size(l1, HORIZONTAL_ALIGNMENT_LEFT, -1, FOOTER_FONT_SIZE).x
            var w2: float = font.get_string_size(l2, HORIZONTAL_ALIGNMENT_LEFT, -1, FOOTER_FONT_SIZE).x
            var w3: float = font.get_string_size(l3, HORIZONTAL_ALIGNMENT_LEFT, -1, FOOTER_FONT_SIZE).x
            var widest: float = maxf(w1, maxf(w2, w3))
            var overflow: float = maxf(0.0, widest - 508.0)
            var balance: float = absf(w1 - w2) + absf(w2 - w3) + absf(w1 - w3)
            var score: float = overflow * 100000.0 + balance
            if score < best_score:
                best_score = score
                best_a = a
                best_b = b
    return " ".join(words.slice(0, best_a)) + "\n" + " ".join(words.slice(best_a, best_b)) + "\n" + " ".join(words.slice(best_b))

func _pad_three_lines(text_value: String) -> String:
    var clean: PackedStringArray = text_value.replace("\r", "").split("\n", true)
    while clean.size() < 3:
        clean.append("")
    if clean.size() > 3:
        clean = PackedStringArray(clean.slice(0, 3))
    return "\n".join(clean)

func _single_line(value: String) -> String:
    return value.strip_edges().replace("\r", "").replace("\n", " ")

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
