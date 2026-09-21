# res://tools/prototypes/c11c_geometric_waves_v1/GeometricWavesPrototype.gd
extends Node2D

## C11-C.1 v1.5 — Geometric Waves visual-family prototype.
## The seed selects a wave grammar, composition parameters and palette variant.
## No core, simulation, RNG stream or C7 contract is touched.

const UnifiedSocialFrameScene = preload("res://core/presentation/UnifiedSocialFrame.tscn")
const GeometricWavesRendererClass = preload("res://tools/prototypes/c11c_geometric_waves_v1/GeometricWavesRenderer.gd")
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
    _variation = VariationProfileClass.build("geometric", _seed)
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

    _renderer.set_palette(_palette_dominant(), _palette_secondary(), Color("FFFFFF"))
    _renderer.set_style(
        int(_variation["grammar_mode"]),
        int(_variation["palette_mode"]),
        float(_variation["morph"]),
        float(_variation["wave_frequency"]),
        float(_variation["line_width"]),
        float(_variation["glow"]),
        float(_variation["polygon_sides"]),
        float(_variation["wave_ratio"]),
        float(_variation["shape_rotation"]),
        float(_variation["layer_spread"]),
        float(_variation["radial_wave_amplitude"]),
        float(_variation["liss_x_frequency"]),
        float(_variation["liss_y_frequency"]),
        float(_variation["interference_scale"]),
        float(_variation["hero_scale"]),
        float(_variation["perspective_strength"]),
        float(_variation["depth_strength"]),
        float(_variation["secondary_phase"]),
        float(_variation["color_phase"]),
        float(_variation["stroke_scale"])
    )
    _renderer.set_frame(0, FRAME_COUNT, _seed_phase(_seed))

func _palette_dominant() -> Color:
    match int(_variation["palette_mode"]):
        0: return Color("16E6FF")
        1: return Color("5B8CFF")
        2: return Color("38E5D0")
        3: return Color("9AD7FF")
        4: return Color("FFB347")
        _: return Color("16E6FF")

func _palette_secondary() -> Color:
    match int(_variation["palette_mode"]):
        0: return Color("FF3EBA")
        1: return Color("B07CFF")
        2: return Color("D887FF")
        3: return Color("5C79FF")
        4: return Color("35D4FF")
        _: return Color("FF3EBA")

func _grammar_label() -> String:
    match int(_variation["grammar_mode"]):
        0: return "HARMONIC MEMBRANE"
        1: return "INTERFERENCE PLANE"
        2: return "PARAMETRIC RIBBON"
        3: return "LATTICE WAVE"
        4: return "ORBITAL WAVE"
        _: return "HARMONIC MEMBRANE"

func _math_header() -> String:
    match int(_variation["grammar_mode"]):
        0: return "h(x,y,t)=sin(ωx+φ)·cos(ωy−φ)   ·   MEMBRANE"
        1: return "I(x,y,t)=sin(ω₁x+φ₁)·sin(ω₂y+φ₂)   ·   INTERFERENCE"
        2: return "R(u)=(u,A·sin(ωu+φ))   ·   PARAMETRIC RIBBON"
        3: return "G(x,y,t)=sin(ωx+δ)·sin(ωy−δ)   ·   LATTICE"
        4: return "ρ(a,t)=ρ₀+A·sin(kr−ωt)   ·   ORBITAL"
        _: return "h(x,y,t)=sin(ωx+φ)·cos(ωy−φ)   ·   MEMBRANE"

func _add_frame_decoration(frame: UnifiedSocialFrame) -> void:
    var accent_a := _palette_dominant()
    var accent_b := _palette_secondary()

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
    header_accent.color = accent_a
    header_accent.mouse_filter = Control.MOUSE_FILTER_IGNORE
    frame.get_header_content_root().add_child(header_accent)

    var footer_accent := ColorRect.new()
    footer_accent.name = "FooterAccent"
    footer_accent.position = Vector2(458.0, 127.0)
    footer_accent.size = Vector2(46.0, 2.0)
    footer_accent.color = accent_b
    footer_accent.mouse_filter = Control.MOUSE_FILTER_IGNORE
    frame.get_footer_content_root().add_child(footer_accent)

func _add_header(root: Control) -> void:
    root.add_child(_new_header_math_label(_math_header(), Vector2(36.0, 34.0), Vector2(468.0, 28.0), Color("E8F2FA")))
    root.add_child(_new_label("MODE %s   ·   PALETTE %s   ·   HERO %.2fx" % [_grammar_label(), str(_variation["palette_name"]).to_upper(), float(_variation["hero_scale"])], Vector2(36.0, 68.0), Vector2(468.0, 20.0), 9, Color("7F93A8")))

func _add_footer(root: Control) -> void:
    root.add_child(_new_label("VISUAL LOOP  //  GEOMETRIC WAVES", Vector2(36.0, 33.0), Vector2(468.0, 18.0), 10, Color("7F93A8")))
    var geek_text: String = TechnobabbleGeneratorClass.generate_geek_text("geometric", _seed)
    root.add_child(_new_footer_geek_label(geek_text, Vector2(36.0, 51.0), Vector2(468.0, 20.0), Color("AAB7C7")))
    var hook := _new_label("CUANDO LAS ONDAS DIBUJAN GEOMETRÍA", Vector2(36.0, 72.0), Vector2(468.0, 28.0), 18, Color("F3F7FF"))
    hook.add_theme_constant_override("outline_size", 2)
    root.add_child(hook)
    root.add_child(_new_label("MATHEMATICAL GENERATIVE ART  /  v1.5", Vector2(36.0, 106.0), Vector2(468.0, 16.0), 9, Color("587086")))

func _resolve_footer_visibility() -> bool:
    var raw: String = OS.get_environment("C11C_SHOW_FOOTER").strip_edges().to_lower()
    return raw not in ["0", "false", "off", "no"]

func _resolve_seed() -> int:
    var raw: String = OS.get_environment("C11C_SEED").strip_edges()
    if raw.is_valid_int():
        return int(raw)
    return REFERENCE_SEED

func _new_header_math_label(text_value: String, pos: Vector2, box_size: Vector2, color: Color) -> Label:
    var label := _new_label(text_value, pos, box_size, HEADER_MAX_FONT_SIZE, color)
    var font: Font = label.get_theme_default_font()
    var fitted: int = HEADER_MAX_FONT_SIZE
    while fitted > HEADER_MIN_FONT_SIZE and font.get_string_size(text_value, HORIZONTAL_ALIGNMENT_LEFT, -1, fitted).x > HEADER_MAX_WIDTH:
        fitted -= 1
    label.add_theme_font_size_override("font_size", fitted)
    return label

func _new_footer_geek_label(text_value: String, pos: Vector2, box_size: Vector2, color: Color) -> Label:
    var label := _new_label(text_value, pos, box_size, 10, color)
    var font: Font = label.get_theme_default_font()
    var fitted: int = 10
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

func _seed_u32(salt: int) -> int:
    var x: int = (int(_seed) + salt * 374761393) & 0x7fffffff
    x = int((x ^ (x >> 13)) * 1274126177) & 0x7fffffff
    x = int((x ^ (x >> 16)) * 2246822519) & 0x7fffffff
    return int(x ^ (x >> 13)) & 0x7fffffff

func _seed_phase(seed_value: int) -> float:
    var x: int = int(seed_value) & 0x7fffffff
    x = int((x ^ (x >> 16)) * 2246822519) & 0x7fffffff
    x = int((x ^ (x >> 13)) * 3266489917) & 0x7fffffff
    x = int(x ^ (x >> 16))
    return TAU * float(x % 100000) / 100000.0
