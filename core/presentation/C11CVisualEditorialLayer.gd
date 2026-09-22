# res://core/presentation/C11CVisualEditorialLayer.gd
class_name C11CVisualEditorialLayer
extends RefCounted

## C11-C — Shared visual-content social/editorial presentation layer.
## Used by Visual Loop and Visual Drill presentation paths.
## Owns typography/layout decoration only. Never owns simulation, RNG, timing or mechanics.

const C11CEditorialAnimatorScript = preload("res://tools/prototypes/c11c_common/C11CEditorialAnimator.gd")

const LOGICAL_CANVAS_SIZE := Vector2(540.0, 960.0)
const HEADER_HEIGHT := 144.0
const FOOTER_HEIGHT := 144.0
const CONTENT_WIDTH := 468.0
const CONTENT_X := 36.0
const HEADER_MAX_WIDTH := 486.0
const HEADER_FONT_SIZE := 18
const HEADER_MIN_FONT_SIZE := 12
const HEADER_SECOND_FONT_SIZE := 18
const HEADER_BOLD_EMBOLDEN := 0.70
const HEADER_TOP_Y := 10.0
const HEADER_TOP_HEIGHT := 54.0
const HEADER_SEPARATOR_Y := 70.0
const HEADER_SECOND_Y := 74.0
const HEADER_SECOND_HEIGHT := 64.0
const FOOTER_SEPARATOR_Y := 14.0
const FOOTER_FONT_SIZE := 12
const FOOTER_MIN_FONT_SIZE := 10

const SECTION_BACKGROUND := Color("05070B")

var _frame: UnifiedSocialFrame
var _header_root: Control
var _footer_root: Control
var _header_container: Control
var _footer_container: Control
var _header_line_1: Label
var _header_line_2: Label
var _footer_line_1: Label
var _footer_line_2: Label
var _footer_line_3: Label
var _header_rule: ColorRect
var _footer_rule: ColorRect
var _header_background: ColorRect
var _footer_background: ColorRect
var _mounted: bool = false
var _animator: RefCounted = null

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

	_header_line_1 = _new_label("C11CHeaderLine1", Vector2(0.0, HEADER_TOP_Y), Vector2(LOGICAL_CANVAS_SIZE.x, HEADER_TOP_HEIGHT), HEADER_FONT_SIZE)
	_header_line_2 = _new_label("C11CHeaderLine2", Vector2(0.0, HEADER_SECOND_Y), Vector2(LOGICAL_CANVAS_SIZE.x, HEADER_SECOND_HEIGHT), HEADER_SECOND_FONT_SIZE)
	_footer_line_1 = _new_label("C11CFooterLine1", Vector2(0.0, 20.0), Vector2(LOGICAL_CANVAS_SIZE.x, 24.0), FOOTER_FONT_SIZE)
	_footer_line_2 = _new_label("C11CFooterLine2", Vector2(0.0, 47.0), Vector2(LOGICAL_CANVAS_SIZE.x, 24.0), FOOTER_FONT_SIZE)
	_footer_line_3 = _new_label("C11CFooterLine3", Vector2(0.0, 74.0), Vector2(LOGICAL_CANVAS_SIZE.x, 24.0), FOOTER_FONT_SIZE)

	_header_container.add_child(_header_line_1)
	_header_container.add_child(_header_line_2)
	_footer_container.add_child(_footer_line_1)
	_footer_container.add_child(_footer_line_2)
	_footer_container.add_child(_footer_line_3)
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
	var enabled: bool = bool(editorial.get("enabled", false))
	if not enabled:
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
	var header_secondary: Color = _to_color(colors.get("header_secondary", header_primary))
	var footer_data: Color = _to_color(colors.get("footer_data", Color("FFFFFF")))
	var footer_secondary: Color = _to_color(colors.get("footer_secondary", header_secondary))
	var footer_signature: Color = _to_color(colors.get("footer_signature", header_primary))
	var rule_color: Color = _to_color(colors.get("rule", header_secondary))

	var matrix_enabled: bool = bool(editorial.get("matrix_enabled", false))
	if matrix_enabled and _animator == null:
		_animator = C11CEditorialAnimatorScript.new(header.get("line_1", ""), header.get("line_2", ""), int(render_model.get("editorial_seed", 314159)))
	elif not matrix_enabled:
		_animator = null

	var header_1: String = str(header.get("line_1", "")).strip_edges()
	var header_2_raw: String = str(header.get("line_2", "")).strip_edges().to_upper()
	var header_2: String = _wrap_two_lines(header_2_raw, _header_line_2.get_theme_default_font(), HEADER_SECOND_FONT_SIZE, HEADER_MAX_WIDTH)

	if matrix_enabled and _animator != null:
		var frame_index := int(render_model.get("editorial_frame_index", 0))
		var frame_count := int(render_model.get("editorial_frame_count", 1))
		var animated: Dictionary = _animator.display_at(frame_index, frame_count)
		_header_line_1.text = str(animated.get("line1_text", header_1))
		_header_line_2.text = str(animated.get("line2_text", header_2))
	else:
		_header_line_1.text = header_1
		_header_line_2.text = header_2
	_header_line_1.add_theme_color_override("font_color", header_primary)
	_header_line_2.add_theme_color_override("font_color", header_secondary)
	_header_line_1 = _apply_bold(_header_line_1)
	_header_line_2 = _apply_bold(_header_line_2)
	_header_line_2.text = _wrap_two_lines(_header_line_2.text, _header_line_2.get_theme_default_font(), HEADER_SECOND_FONT_SIZE, HEADER_MAX_WIDTH)
	_fit_label(_header_line_1, _header_line_1.text, HEADER_FONT_SIZE, HEADER_MIN_FONT_SIZE, HEADER_MAX_WIDTH)
	_fit_label(_header_line_2, _header_line_2.text, HEADER_SECOND_FONT_SIZE, HEADER_MIN_FONT_SIZE, HEADER_MAX_WIDTH)

	_footer_line_1.text = str(footer.get("line_1", "")).strip_edges()
	_footer_line_2.text = str(footer.get("line_2", "")).strip_edges()
	_footer_line_3.text = str(footer.get("line_3", "")).strip_edges()
	_footer_line_1.add_theme_color_override("font_color", footer_data)
	_footer_line_2.add_theme_color_override("font_color", footer_secondary)
	_footer_line_3.add_theme_color_override("font_color", footer_signature)
	_fit_label(_footer_line_1, _footer_line_1.text, FOOTER_FONT_SIZE, FOOTER_MIN_FONT_SIZE, 508.0)
	_fit_label(_footer_line_2, _footer_line_2.text, FOOTER_FONT_SIZE, FOOTER_MIN_FONT_SIZE, 508.0)
	_fit_label(_footer_line_3, _footer_line_3.text, FOOTER_FONT_SIZE, FOOTER_MIN_FONT_SIZE, 508.0)

	_header_rule.color = _with_alpha(rule_color, 0.28)
	_footer_rule.color = _with_alpha(rule_color, 0.28)
	_header_rule.visible = bool(editorial.get("show_header_rule", true))
	_footer_rule.visible = bool(editorial.get("show_footer_rule", true))
	_footer_container.visible = bool(editorial.get("show_footer", true))
	_header_container.visible = bool(editorial.get("show_header", true))

func clear() -> void:
	_mounted = false
	_animator = null
	_hide_all()
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
	while fitted > min_font_size and font.get_string_size(text_value, HORIZONTAL_ALIGNMENT_LEFT, -1, fitted).x > max_width:
		fitted -= 1
	label.add_theme_font_size_override("font_size", fitted)

func _wrap_two_lines(text_value: String, font: Font, font_size: int, max_width: float) -> String:
	var clean := text_value.strip_edges().replace("\r", "").replace("\n", " ")
	var words: PackedStringArray = clean.split(" ", false)
	if words.size() <= 1:
		return clean
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
		var left_width := measure_font.get_string_size(left, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size).x
		var right_width := measure_font.get_string_size(right, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size).x
		var max_line := maxf(left_width, right_width)
		var overflow := maxf(0.0, max_line - max_width)
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
