# res://tools/prototypes/c11c_geometric_waves_v1/GeometricWavesPrototype.gd
extends Node2D

## C11-C.1 — Geometric Waves v1 single-reference prototype.
## Reference: 10.0 s / 30 FPS / 300 frames / 540x960 / seed 314159.
## The controller owns only prototype playback time; it does not touch VisualLoopRuntime.

const UnifiedSocialFrameScene = preload("res://core/presentation/UnifiedSocialFrame.tscn")
const GeometricWavesRendererClass = preload("res://tools/prototypes/c11c_geometric_waves_v1/GeometricWavesRenderer.gd")

const REFERENCE_SEED := 314159
const LOOP_DURATION := 10.0
const FPS := 30
const FRAME_COUNT := 300

var _renderer: Node2D
var _frame_index := 0

func _ready() -> void:
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
    _add_footer(frame.get_footer_content_root())

    _renderer = GeometricWavesRendererClass.new()
    _renderer.name = "GeometricWavesRenderer"
    frame.get_body_content_root().add_child(_renderer)

    var seed_phase := _seed_phase(REFERENCE_SEED)
    _renderer.set_palette(
        Color(0.00, 0.82, 0.94, 1.0),
        Color(0.95, 0.08, 0.52, 1.0),
        Color(1.00, 1.00, 1.00, 1.0)
    )
    _renderer.set_style(0.66, 18.0, 0.008, 0.62)
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
    var eyebrow := _new_label(
        "VISUAL LOOP  //  GEOMETRIC WAVES",
        Vector2(36.0, 40.0),
        Vector2(468.0, 18.0),
        11,
        Color("7F93A8")
    )
    root.add_child(eyebrow)

    var hook := _new_label(
        "CUANDO LAS ONDAS DIBUJAN GEOMETRÍA",
        Vector2(36.0, 61.0),
        Vector2(468.0, 38.0),
        23,
        Color("F3F7FF")
    )
    hook.add_theme_constant_override("outline_size", 2)
    hook.add_theme_color_override("font_outline_color", Color(0.00, 0.82, 0.94, 0.10))
    root.add_child(hook)

func _add_footer(root: Control) -> void:
    var math_line := _new_label(
        "φ(t)=2π·f/300   ·   N=6   ·   LISS 8:5   ·   3 LAYERS",
        Vector2(36.0, 47.0),
        Vector2(468.0, 20.0),
        12,
        Color("D8E5F2")
    )
    root.add_child(math_line)

    var data_line := _new_label(
        "SEED 314159   ·   BODY 540×672   ·   30 FPS   ·   T=10.00 s   ·   DETERMINISTIC",
        Vector2(36.0, 72.0),
        Vector2(468.0, 20.0),
        10,
        Color("7F93A8")
    )
    root.add_child(data_line)

    var signature := _new_label(
        "MATHEMATICAL GENERATIVE ART  /  v1",
        Vector2(36.0, 101.0),
        Vector2(468.0, 18.0),
        9,
        Color("587086")
    )
    root.add_child(signature)

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

    _renderer.set_frame(_frame_index, FRAME_COUNT, _seed_phase(REFERENCE_SEED))
    _frame_index = (_frame_index + 1) % FRAME_COUNT

func _seed_phase(seed_value: int) -> float:
    # Stable integer mixing; this is a presentation parameter, not the engine RNG.
    var x := int(seed_value) & 0x7fffffff
    x = int((x ^ (x >> 16)) * 2246822519) & 0x7fffffff
    x = int((x ^ (x >> 13)) * 3266489917) & 0x7fffffff
    x = int(x ^ (x >> 16))
    return TAU * float(x % 100000) / 100000.0
