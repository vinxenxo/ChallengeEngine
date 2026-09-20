# res://tools/prototypes/c11c_geometric_waves_v1/GeometricWavesPrototype.gd
extends Node2D

## C11-C.1 — Geometric Waves v1 single-reference prototype.
## Reference: 10.0 s / 30 FPS / 300 frames / 540x960 / seed 314159.
## The controller owns only prototype playback time; it does not touch VisualLoopRuntime.

const UnifiedSocialFrameScene = preload("res://core/presentation/UnifiedSocialFrame.tscn")
const GeometricWavesRendererClass = preload("res://tools/prototypes/c11c_geometric_waves_v1/GeometricWavesRenderer.gd")
const TechnobabbleGeneratorClass = preload("res://tools/prototypes/c11c_common/TechnobabbleGenerator.gd")

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
var _polygon_sides := 6
var _wave_frequency := 18.0

func _ready() -> void:
    _seed = _resolve_seed()
    _show_footer = _resolve_footer_visibility()
    _build_scene()
    set_process(true)

func _build_scene() -> void:
    var background := ColorRect.new()
    background.name = "AbyssalBackground"
    background.position = Vector2.ZERO
    background.size = Vector2(540.0, 960.0)
    background.color = Color("050811")
    background.mouse_filter = Control.MOUSE_FILTER_IGNORE
    add_child(background)

    var frame := UnifiedSocialFrameScene.instantiate() as UnifiedSocialFrame
    frame.name = "UnifiedSocialFrame"
    add_child(frame)

    _add_frame_decoration(frame)
    _add_header(frame.get_header_content_root())
    if _show_footer:
        _add_footer(frame.get_footer_content_root())

    _renderer = GeometricWavesRendererClass.new()
    _renderer.name = "GeometricWavesRenderer"
    frame.get_body_content_root().add_child(_renderer)

    var seed_phase := _seed_phase(_seed)
    _renderer.set_palette(
        Color(0.00, 0.82, 0.94, 1.0),
        Color(0.95, 0.08, 0.52, 1.0),
        Color(1.00, 1.00, 1.00, 1.0)
    )
    _polygon_sides = _choice([5, 6, 7, 8], 11)
    _wave_frequency = _choice([16.0, 18.0, 20.0, 22.0], 17)
    var morph := lerpf(0.54, 0.80, _seed01(23))
    var line_width := lerpf(0.0068, 0.0090, _seed01(29))
    var glow := lerpf(0.56, 0.70, _seed01(31))
    var wave_ratio := lerpf(0.78, 0.90, _seed01(37))
    _renderer.set_style(morph, _wave_frequency, line_width, glow, float(_polygon_sides), wave_ratio)
    _renderer.set_frame(0, FRAME_COUNT, seed_phase)

func _add_frame_decoration(frame: UnifiedSocialFrame) -> void:
    var header_line := ColorRect.new()
    header_line.name = "HeaderRule"
    header_line.position = Vector2(36.0, 102.0)
    header_line.size = Vector2(468.0, 1.0)
    header_line.color = Color(0.20, 0.30, 0.45, 0.34)
    header_line.mouse_filter = Control.MOUSE_FILTER_IGNORE
    frame.get_header_content_root().add_child(header_line)

    var footer_line := ColorRect.new()
    footer_line.name = "FooterRule"
    footer_line.position = Vector2(36.0, 30.0)
    footer_line.size = Vector2(468.0, 1.0)
    footer_line.color = Color(0.20, 0.30, 0.45, 0.34)
    footer_line.mouse_filter = Control.MOUSE_FILTER_IGNORE
    frame.get_footer_content_root().add_child(footer_line)

    var header_accent := ColorRect.new()
    header_accent.name = "HeaderAccent"
    header_accent.position = Vector2(36.0, 26.0)
    header_accent.size = Vector2(46.0, 2.0)
    header_accent.color = Color(0.00, 0.82, 0.94, 0.90)
    header_accent.mouse_filter = Control.MOUSE_FILTER_IGNORE
    frame.get_header_content_root().add_child(header_accent)

    var footer_accent := ColorRect.new()
    footer_accent.name = "FooterAccent"
    footer_accent.position = Vector2(458.0, 127.0)
    footer_accent.size = Vector2(46.0, 2.0)
    footer_accent.color = Color(0.95, 0.08, 0.52, 0.85)
    footer_accent.mouse_filter = Control.MOUSE_FILTER_IGNORE
    frame.get_footer_content_root().add_child(footer_accent)

func _add_header(root: Control) -> void:
    root.add_child(_new_header_math_label("φ(t)=2π·f/300   ·   POLY N=%d   ·   LISS 8:5   ·   3 LAYERS" % _polygon_sides, Vector2(36.0, 34.0), Vector2(468.0, 28.0), Color("D8E5F2")))
    root.add_child(_new_label("SEED %d   ·   BODY 540×672   ·   30 FPS   ·   T=10.00 s   ·   DETERMINISTIC" % _seed, Vector2(36.0, 68.0), Vector2(468.0, 20.0), 9, Color("7F93A8")))

func _add_footer(root: Control) -> void:
    root.add_child(_new_label("VISUAL LOOP  //  GEOMETRIC WAVES", Vector2(36.0, 33.0), Vector2(468.0, 18.0), 10, Color("7F93A8")))
    var geek_text: String = TechnobabbleGeneratorClass.generate_geek_text("geometric", _seed)
    root.add_child(_new_footer_geek_label(geek_text, Vector2(36.0, 51.0), Vector2(468.0, 20.0), Color("AAB7C7")))
    var hook := _new_label("CUANDO LAS ONDAS DIBUJAN GEOMETRÍA", Vector2(36.0, 72.0), Vector2(468.0, 28.0), 18, Color("F3F7FF"))
    hook.add_theme_constant_override("outline_size", 2)
    root.add_child(hook)
    root.add_child(_new_label("MATHEMATICAL GENERATIVE ART  /  v1", Vector2(36.0, 106.0), Vector2(468.0, 16.0), 9, Color("587086")))

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
func _new_label(
    text_value: String,
    pos: Vector2,
    box_size: Vector2,
    font_size: int,
    color: Color
) -> Label:
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

func _choice(values: Array, salt: int):
    return values[_seed_u32(salt) % values.size()]

func _seed01(salt: int) -> float:
    return float(_seed_u32(salt) % 100000) / 100000.0

func _seed_u32(salt: int) -> int:
    var x := (int(_seed) + salt * 374761393) & 0x7fffffff
    x = int((x ^ (x >> 13)) * 1274126177) & 0x7fffffff
    x = int((x ^ (x >> 16)) * 2246822519) & 0x7fffffff
    return int(x ^ (x >> 13)) & 0x7fffffff

func _seed_phase(seed_value: int) -> float:
    # Stable integer mixing; this is a presentation parameter, not the engine RNG.
    var x := int(seed_value) & 0x7fffffff
    x = int((x ^ (x >> 16)) * 2246822519) & 0x7fffffff
    x = int((x ^ (x >> 13)) * 3266489917) & 0x7fffffff
    x = int(x ^ (x >> 16))
    return TAU * float(x % 100000) / 100000.0
