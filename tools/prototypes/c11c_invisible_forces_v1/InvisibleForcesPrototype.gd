extends Node2D

## C11-C editorial/audio/loop presentation prototype v1.9.
## Family: INVISIBLE FORCES
## Presentation-only: no core, simulation, SimulationResult, engine RNG or C7 changes.

const UnifiedSocialFrameScene = preload("res://core/presentation/UnifiedSocialFrame.tscn")
const RendererClass = preload("res://tools/prototypes/c11c_invisible_forces_v1/InvisibleForcesRenderer.gd")
const TechnobabbleGeneratorClass = preload("res://tools/prototypes/c11c_common/TechnobabbleGenerator.gd")
const VariationProfileClass = preload("res://tools/prototypes/c11c_common/C11CVariationProfile.gd")
const PaletteBankClass = preload("res://tools/prototypes/c11c_common/C11CPaletteBank.gd")
const EDITORIAL_ANIMATOR_SCRIPT = preload("res://tools/prototypes/c11c_common/C11CEditorialAnimator.gd")
const C11CThemeClass = preload("res://tools/prototypes/c11c_common/C11CTheme.gd")
const EditorialColorsClass = preload("res://tools/prototypes/c11c_common/C11CEditorialColors.gd")
const ColorBoostClass = preload("res://tools/prototypes/c11c_common/C11CColorBoost.gd")

const REFERENCE_SEED := 314159
const HEADER_MAX_WIDTH := 468.0
const HEADER_MAX_FONT_SIZE := 16
const HEADER_MIN_FONT_SIZE := 11
const HEADER_HOOK_FONT_SIZE := 18
const LOOP_DURATION := 18.0
const FPS := 30
const FRAME_COUNT := 540
const OUTPUT_SCALE := 4.0 / 3.0
const BLACK: Color = C11CThemeClass.SECTION_BACKGROUND

var _renderer: Node2D
var _frame_index: int = 0
var _seed: int = REFERENCE_SEED
var _show_footer: bool = true
var _variation: Dictionary = {}
var _palette: Dictionary = {}
var _text_colors: Dictionary = {}
var _header_hook: Label
var _header_animator: RefCounted
var _authoring_json_path: String = ""

func _ready() -> void:
    scale = Vector2(OUTPUT_SCALE, OUTPUT_SCALE)
    _seed = _resolve_seed()
    _show_footer = _resolve_footer_visibility()
    _variation = VariationProfileClass.build("invisible_forces", _seed)
    _palette = PaletteBankClass.palette("invisible_forces", int(_variation["palette_mode"]))
    _text_colors = EditorialColorsClass.palette("invisible_forces", _palette)
    _authoring_json_path = "res://artifacts/prototypes/c11c_invisible_forces_v1/InvisibleForces_v1_seed_%d_authoring.json" % _seed
    _write_authoring_snapshot()
    _build_scene()
    set_process(true)

func _build_scene() -> void:
    var background := ColorRect.new()
    background.name = "UnifiedBlackBackground"
    background.position = Vector2.ZERO
    background.size = Vector2(540.0, 960.0)
    background.color = BLACK
    background.mouse_filter = Control.MOUSE_FILTER_IGNORE
    add_child(background)

    var frame := UnifiedSocialFrameScene.instantiate() as UnifiedSocialFrame
    frame.name = "UnifiedSocialFrame"
    add_child(frame)
    _add_section_background(frame.get_header_content_root())
    _add_section_background(frame.get_footer_content_root())
    _add_frame_decoration(frame)
    _add_header(frame.get_header_content_root())
    if _show_footer:
        _add_footer(frame.get_footer_content_root())

    _renderer = RendererClass.new()
    _renderer.name = "InvisibleForcesRenderer"
    frame.get_body_content_root().add_child(_renderer)
    _renderer.set_background(BLACK)
    _renderer.set_palette(ColorBoostClass.vivid(Color(str(_palette["deep"])), 1.24, 1.03), ColorBoostClass.vivid(Color(str(_palette["primary"]))), ColorBoostClass.vivid(Color(str(_palette["secondary"]))), ColorBoostClass.vivid(Color(str(_palette["highlight"]))))
    var storm_offset: Vector2 = Vector2(float(_variation["storm_offset_x"]), float(_variation["storm_offset_y"]))
    _renderer.set_style(
        int(_variation["grammar_mode"]), float(_variation["trace_count"]), float(_variation["curvature"]), float(_variation["glow"]),
        float(_variation["field_rotation"]), storm_offset, float(_variation["pulse_speed"]), float(_variation["field_twist"]), float(_variation["pulse_width"]),
        float(_variation["storm_scale"]), float(_variation["lens_strength"]), float(_variation["basin_depth"]), float(_variation["pole_separation"]), float(_variation["quadrupole_skew"]), float(_variation["color_phase"])
    )
    _renderer.set_frame(0, FRAME_COUNT, _seed_phase(_seed), float(_variation["loop_cycles"]))

func _add_section_background(root: Control) -> void:
    var section_bg := ColorRect.new()
    section_bg.name = "SectionBlackBackground"
    section_bg.position = Vector2.ZERO
    section_bg.size = Vector2(540.0, 144.0)
    section_bg.color = BLACK
    section_bg.mouse_filter = Control.MOUSE_FILTER_IGNORE
    section_bg.z_index = -100
    root.add_child(section_bg)

func _add_frame_decoration(frame: UnifiedSocialFrame) -> void:
    var rule_color: Color = _text_colors["rule"]
    rule_color.a = 0.28

    var rule_a := ColorRect.new()
    rule_a.position = Vector2(36.0, 104.0)
    rule_a.size = Vector2(468.0, 1.0)
    rule_a.color = rule_color
    frame.get_header_content_root().add_child(rule_a)

    var rule_b := ColorRect.new()
    rule_b.position = Vector2(36.0, 30.0)
    rule_b.size = Vector2(468.0, 1.0)
    rule_b.color = rule_color
    frame.get_footer_content_root().add_child(rule_b)

func _add_header(root: Control) -> void:
    var grammar_names: Array[String] = ["DIPOLE FIELD", "VORTEX FIELD", "SADDLE FIELD", "QUADRUPOLE FIELD", "GRAVITATIONAL LENS", "TOPOGRAPHIC BASIN"]
    var hooks: Array[String] = ["NO VES LA FUERZA, SOLO SU RASTRO", "OBSERVA UNA FUERZA HECHA VISIBLE", "SIGUE EL RASTRO DE LA FISICA", "LEE EL MAPA DE UNA FUERZA", "LA FISICA DEJA UNA HUELLA", "DESCUBRE EL CAMPO OCULTO"]
    var grammar_index: int = int(_variation["grammar_mode"])
    var grammar_name: String = grammar_names[grammar_index].to_upper()
    var hook: String = hooks[grammar_index % hooks.size()]
    var line1: String = "%s | %d TRACES | PULSE %.2f" % [grammar_name.replace(" ", "_"), int(_variation["trace_count"]), float(_variation["pulse_speed"])]
    root.add_child(_new_header_math_label(line1, Vector2(36.0, 27.0), Vector2(468.0, 32.0), _text_colors["header_math"]))
    _header_hook = _new_label(hook, Vector2(36.0, 66.0), Vector2(468.0, 34.0), HEADER_HOOK_FONT_SIZE, _text_colors["header_hook"])
    _header_hook.add_theme_constant_override("outline_size", 1)
    root.add_child(_header_hook)
    _header_animator = EDITORIAL_ANIMATOR_SCRIPT.new(hook, "VISUAL LOOP / INVISIBLE FORCES", _seed)

func _add_footer(root: Control) -> void:
    var geek_text: String = TechnobabbleGeneratorClass.generate_geek_text("invisible_forces", _seed, _variation)
    var line1: String = geek_text
    var line2: String = "SEED %d | BODY 720X896 | T=18.00S | %d FLOW TRACES | PULSE %.2f" % [_seed, int(_variation["trace_count"]), float(_variation["pulse_speed"])]
    var line3: String = "PALETTE %s | LOOP x%d | AUDIO AMBIENT" % [str(_palette["name"]).to_upper(), int(_variation["loop_cycles"])]
    var line4: String = "DETERMINISTIC FIELD ART / v2.0.8"
    root.add_child(_new_footer_label(line1, Vector2(36.0, 42.0), _text_colors["footer_geek"]))
    root.add_child(_new_footer_label(line2, Vector2(36.0, 62.0), _text_colors["footer_data"]))
    root.add_child(_new_footer_label(line3, Vector2(36.0, 82.0), _text_colors["footer_palette"]))
    root.add_child(_new_footer_label(line4, Vector2(36.0, 102.0), _text_colors["footer_signature"]))

func _new_footer_label(text_value: String, pos: Vector2, color: Color) -> Label:
    return _new_label(text_value, pos, Vector2(468.0, 16.0), 9, color)

func _resolve_footer_visibility() -> bool:
    var raw: String = OS.get_environment("C11C_SHOW_FOOTER").strip_edges().to_lower()
    return raw not in ["0", "false", "off", "no"]

func _resolve_seed() -> int:
    var raw: String = OS.get_environment("C11C_SEED").strip_edges()
    return int(raw) if raw.is_valid_int() else REFERENCE_SEED

func _new_header_math_label(text_value: String, pos: Vector2, box_size: Vector2, color: Color) -> Label:
    var label := _new_label(text_value, pos, box_size, HEADER_MAX_FONT_SIZE, color)
    var font: Font = label.get_theme_default_font()
    var fitted: int = HEADER_MAX_FONT_SIZE
    while fitted > HEADER_MIN_FONT_SIZE and font.get_string_size(text_value, HORIZONTAL_ALIGNMENT_LEFT, -1, fitted).x > HEADER_MAX_WIDTH:
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
    _renderer.set_frame(_frame_index, FRAME_COUNT, _seed_phase(_seed), float(_variation["loop_cycles"]))
    if _header_hook != null and _header_animator != null:
        var editorial: Dictionary = _header_animator.display_at(_frame_index, FRAME_COUNT)
        _header_hook.text = str(editorial["text"])
        _header_hook.modulate = Color(1.0, 1.0, 1.0, 1.0 if not bool(editorial["transition"]) else 0.90)
    _frame_index = (_frame_index + 1) % FRAME_COUNT

func _seed_index(salt: int, size: int) -> int:
    return _seed_mix(salt) % maxi(size, 1)

func _seed_mix(salt: int) -> int:
    var x: int = (int(_seed) ^ int(salt * 374761393)) & 0x7fffffff
    x = int((x ^ (x >> 13)) * 1274126177) & 0x7fffffff
    x = int((x ^ (x >> 16)) * 2246822519) & 0x7fffffff
    return int(x ^ (x >> 13)) & 0x7fffffff

func _seed_phase(seed_value: int) -> float:
    var x: int = int(seed_value) & 0x7fffffff
    x = int((x ^ (x >> 16)) * 2246822519) & 0x7fffffff
    x = int((x ^ (x >> 13)) * 3266489917) & 0x7fffffff
    x = int(x ^ (x >> 16))
    return TAU * float(x % 100000) / 100000.0

func _write_authoring_snapshot() -> void:
    var absolute_path: String = ProjectSettings.globalize_path(_authoring_json_path)
    var dir_path: String = absolute_path.get_base_dir()
    DirAccess.make_dir_recursive_absolute(dir_path)
    var grammar_index: int = int(_variation["grammar_mode"])
    var grammar_names: Array[String] = ["DIPOLE FIELD", "VORTEX FIELD", "SADDLE FIELD", "QUADRUPOLE FIELD", "GRAVITATIONAL LENS", "TOPOGRAPHIC BASIN"]
    var hooks: Array[String] = ["NO VES LA FUERZA, SOLO SU RASTRO", "OBSERVA UNA FUERZA HECHA VISIBLE", "SIGUE EL RASTRO DE LA FISICA", "LEE EL MAPA DE UNA FUERZA", "LA FISICA DEJA UNA HUELLA", "DESCUBRE EL CAMPO OCULTO"]
    var grammar_name: String = grammar_names[grammar_index]
    var header_primary: String = hooks[grammar_index % hooks.size()]
    var header_math: String = "%s | %d TRACES | PULSE %.2f" % [grammar_name.replace(" ", "_"), int(_variation["trace_count"]), float(_variation["pulse_speed"])]
    var sound_raw: String = OS.get_environment("C11C_SOUND_ENABLED").strip_edges().to_lower()
    var sound_enabled: bool = sound_raw not in ["0", "false", "off", "no"]
    var snapshot := {
        "family_id": "invisible_forces",
        "display_name": "INVISIBLE FORCES",
        "seed": _seed,
        "grammar_mode": grammar_index,
        "grammar": grammar_name,
        "palette_mode": int(_variation["palette_mode"]),
        "palette": str(_variation["palette_name"]),
        "loop_cycles": float(_variation["loop_cycles"]),
        "duration_seconds": LOOP_DURATION,
        "fps": FPS,
        "frame_count": FRAME_COUNT,
        "header_primary": header_primary,
        "header_secondary": "VISUAL LOOP / INVISIBLE FORCES",
        "header_math": header_math,
        "technobabble": TechnobabbleGeneratorClass.generate_geek_text("invisible_forces", _seed, _variation),
        "technobabble_revision": TechnobabbleGeneratorClass.revision(),
        "audio_style": "deep deterministic ambient / singing bowls / low drone / family-synced pulses",
        "sound_enabled": sound_enabled,
        "background": "000000",
        "footer_enabled": _show_footer,
        "editorial_revision": "2.0.0",
        "loop_closed": true
    }
    var file := FileAccess.open(absolute_path, FileAccess.WRITE)
    if file != null:
        file.store_string(JSON.stringify(snapshot, "  "))
        file.close()

