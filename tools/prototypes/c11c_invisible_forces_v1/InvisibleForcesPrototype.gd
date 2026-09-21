extends Node2D

## C11-C.5_INVISIBLE_FORCES_V1 — single-reference radial/field prototype.
## Isolated from simulation and production runtime.

const UnifiedSocialFrameScene = preload("res://core/presentation/UnifiedSocialFrame.tscn")
const RendererClass = preload("res://tools/prototypes/c11c_invisible_forces_v1/InvisibleForcesRenderer.gd")
const TechnobabbleGeneratorClass = preload("res://tools/prototypes/c11c_common/TechnobabbleGenerator.gd")
const VariationProfileClass = preload("res://tools/prototypes/c11c_common/C11CVariationProfile.gd")

const REFERENCE_SEED := 314159
const HEADER_MAX_WIDTH := 468.0
const HEADER_MAX_FONT_SIZE := 16
const HEADER_MIN_FONT_SIZE := 11
const LOOP_DURATION := 10.0
const FPS := 30
const FRAME_COUNT := 300

var _renderer: Node2D
var _frame_index := 0
var _seed := REFERENCE_SEED
var _show_footer := true
var _variation: Dictionary = {}

func _ready() -> void:
    _seed = _resolve_seed()
    _show_footer = _resolve_footer_visibility()
    _variation = VariationProfileClass.build("invisible_forces", _seed)
    _build_scene()
    set_process(true)

func _build_scene() -> void:
    var background := ColorRect.new()
    background.name = "AbyssalBackground"
    background.position = Vector2.ZERO
    background.size = Vector2(540.0, 960.0)
    background.color = Color("0A0505")
    background.mouse_filter = Control.MOUSE_FILTER_IGNORE
    add_child(background)

    var frame := UnifiedSocialFrameScene.instantiate() as UnifiedSocialFrame
    frame.name = "UnifiedSocialFrame"
    add_child(frame)
    _add_frame_decoration(frame)
    _add_header(frame.get_header_content_root())
    if _show_footer:
        _add_footer(frame.get_footer_content_root())

    _renderer = RendererClass.new()
    _renderer.name = "InvisibleForcesRenderer"
    frame.get_body_content_root().add_child(_renderer)

    var palette_index: int = int(_variation["palette_mode"])
    match palette_index:
        0: _renderer.set_palette(Color("4E0C18"), Color("C72536"), Color("FF5A1F"), Color("FFD34E"))
        1: _renderer.set_palette(Color("430B12"), Color("C62E24"), Color("FF6B26"), Color("FFD166"))
        2: _renderer.set_palette(Color("3A0A0A"), Color("A71D31"), Color("E85D2A"), Color("FFC857"))
        3: _renderer.set_palette(Color("4A1007"), Color("D53A0A"), Color("FF7A00"), Color("FFD84A"))
        _: _renderer.set_palette(Color("24100D"), Color("8B3A2D"), Color("C76435"), Color("FFD27A"))
    var storm_offset: Vector2 = Vector2(float(_variation["storm_offset_x"]), float(_variation["storm_offset_y"]))
    _renderer.set_style(
        int(_variation["grammar_mode"]), float(_variation["trace_count"]), float(_variation["curvature"]), float(_variation["glow"]),
        float(_variation["field_rotation"]), storm_offset, float(_variation["pulse_speed"]),
        float(_variation["field_twist"]), float(_variation["pulse_width"]), float(_variation["storm_scale"]),
        float(_variation["lens_strength"]), float(_variation["basin_depth"]), float(_variation["pole_separation"]),
        float(_variation["quadrupole_skew"])
    )
    _renderer.set_frame(0, FRAME_COUNT, _seed_phase(_seed))

func _add_frame_decoration(frame: UnifiedSocialFrame) -> void:
    var header_line := ColorRect.new()
    header_line.position = Vector2(36.0, 102.0)
    header_line.size = Vector2(468.0, 1.0)
    header_line.color = Color(0.30, 0.24, 0.16, 0.34)
    header_line.mouse_filter = Control.MOUSE_FILTER_IGNORE
    frame.get_header_content_root().add_child(header_line)

    var footer_line := ColorRect.new()
    footer_line.position = Vector2(36.0, 30.0)
    footer_line.size = Vector2(468.0, 1.0)
    footer_line.color = Color(0.30, 0.24, 0.16, 0.34)
    footer_line.mouse_filter = Control.MOUSE_FILTER_IGNORE
    frame.get_footer_content_root().add_child(footer_line)

    var header_accent := ColorRect.new()
    header_accent.position = Vector2(36.0, 26.0)
    header_accent.size = Vector2(46.0, 2.0)
    header_accent.color = Color("F16A2E")
    header_accent.mouse_filter = Control.MOUSE_FILTER_IGNORE
    frame.get_header_content_root().add_child(header_accent)

    var footer_accent := ColorRect.new()
    footer_accent.position = Vector2(458.0, 127.0)
    footer_accent.size = Vector2(46.0, 2.0)
    footer_accent.color = Color("B83B2B")
    footer_accent.mouse_filter = Control.MOUSE_FILTER_IGNORE
    frame.get_footer_content_root().add_child(footer_accent)

func _add_header(root: Control) -> void:
    root.add_child(_new_header_math_label("%s  |  %d TRACES  |  PULSE %.2f" % [str(_variation["grammar_name"]).to_upper(), int(_variation["trace_count"]), float(_variation["pulse_speed"])], Vector2(36.0, 34.0), Vector2(468.0, 28.0), Color("FFE6D6")))
    root.add_child(_new_label("SEED %d   |   BODY 540x672   |   30 FPS   |   T=10.00 s   |   32 FLOW TRACES" % _seed, Vector2(36.0, 68.0), Vector2(468.0, 20.0), 9, Color("AA7E6A")))

func _add_footer(root: Control) -> void:
    root.add_child(_new_label("VISUAL LOOP  //  INVISIBLE FORCES", Vector2(36.0, 33.0), Vector2(468.0, 18.0), 10, Color("AA7E6A")))
    var geek_text: String = TechnobabbleGeneratorClass.generate_geek_text("vector_field", _seed)
    root.add_child(_new_footer_geek_label(geek_text, Vector2(36.0, 51.0), Vector2(468.0, 20.0), Color("AAB7C7")))
    var hook := _new_label("NO VES LA FUERZA, SOLO SU RASTRO", Vector2(36.0, 72.0), Vector2(468.0, 28.0), 18, Color("FFF2EC"))
    hook.add_theme_constant_override("outline_size", 2)
    root.add_child(hook)
    root.add_child(_new_label("DETERMINISTIC FIELD ART / v1", Vector2(36.0, 106.0), Vector2(468.0, 16.0), 9, Color("7D5547")))

func _resolve_footer_visibility() -> bool:
    var raw := OS.get_environment("C11C_SHOW_FOOTER").strip_edges().to_lower()
    return raw not in ["0", "false", "off", "no"]

func _resolve_seed() -> int:
    var raw := OS.get_environment("C11C_SEED").strip_edges()
    if raw.is_valid_int():
        return int(raw)
    return REFERENCE_SEED

func _new_header_math_label(text_value: String, pos: Vector2, box_size: Vector2, color: Color) -> Label:
    var label := _new_label(text_value, pos, box_size, HEADER_MAX_FONT_SIZE, color)
    var font := label.get_theme_default_font()
    var fitted := HEADER_MAX_FONT_SIZE
    while fitted > HEADER_MIN_FONT_SIZE and font.get_string_size(text_value, HORIZONTAL_ALIGNMENT_LEFT, -1, fitted).x > HEADER_MAX_WIDTH:
        fitted -= 1
    label.add_theme_font_size_override("font_size", fitted)
    return label


func _new_footer_geek_label(text_value: String, pos: Vector2, box_size: Vector2, color: Color) -> Label:
    var label := _new_label(text_value, pos, box_size, 10, color)
    var font := label.get_theme_default_font()
    var fitted := 10
    while fitted > 8 and font.get_string_size(text_value, HORIZONTAL_ALIGNMENT_LEFT, -1, fitted).x > HEADER_MAX_WIDTH:
        fitted -= 1
    label.add_theme_font_size_override("font_size", fitted)
    return label
func _new_label(text_value: String, pos: Vector2, box_size: Vector2, font_size: int, color: Color) -> Label:
    var label := Label.new()
    label.text = text_value
    label.position = pos
    label.size = box_size
    label.mouse_filter = Control.MOUSE_FILTER_IGNORE
    label.add_theme_font_size_override("font_size", font_size)
    label.add_theme_color_override("font_color", color)
    label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
    label.clip_text = true
    return label

func _process(_delta: float) -> void:
    if _renderer == null:
        return
    _renderer.set_frame(_frame_index, FRAME_COUNT, _seed_phase(_seed))
    _frame_index = (_frame_index + 1) % FRAME_COUNT

func _seed01(salt: int) -> float:
    var x := (int(_seed) + salt * 374761393) & 0x7fffffff
    x = int((x ^ (x >> 13)) * 1274126177) & 0x7fffffff
    x = int((x ^ (x >> 16)) * 2246822519) & 0x7fffffff
    return float((int(x ^ (x >> 13)) & 0x7fffffff) % 100000) / 100000.0

func _seed_phase(seed_value: int) -> float:
    var x := int(seed_value) & 0x7fffffff
    x = int((x ^ (x >> 16)) * 2246822519) & 0x7fffffff
    x = int((x ^ (x >> 13)) * 3266489917) & 0x7fffffff
    x = int(x ^ (x >> 16))
    return TAU * float(x % 100000) / 100000.0
