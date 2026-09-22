extends Node2D

## C11-C editorial/audio/loop presentation prototype v2.1.4.
## R4: shared two-line Matrix intro/midpoint swap + family-synced ambient audio.
## Family: LIVING PARTICLES
## Presentation-only: no core, simulation, SimulationResult, engine RNG or C7 changes.

const UnifiedSocialFrameScene = preload("res://core/presentation/UnifiedSocialFrame.tscn")
const RendererClass = preload("res://tools/prototypes/c11c_living_particles_v1/LivingParticlesRenderer.gd")
const TechnobabbleGeneratorClass = preload("res://tools/prototypes/c11c_common/TechnobabbleGenerator.gd")
const VariationProfileClass = preload("res://tools/prototypes/c11c_common/C11CVariationProfile.gd")
const PaletteBankClass = preload("res://tools/prototypes/c11c_common/C11CPaletteBank.gd")
const HEADER_ANIMATOR_SCRIPT = preload("res://tools/prototypes/c11c_common/C11CHeaderAnimatorV2.gd")
const C11CThemeClass = preload("res://tools/prototypes/c11c_common/C11CTheme.gd")
const EditorialColorsClass = preload("res://tools/prototypes/c11c_common/C11CEditorialColors.gd")
const ColorBoostClass = preload("res://tools/prototypes/c11c_common/C11CColorBoost.gd")

const REFERENCE_SEED := 314159
const HEADER_MAX_WIDTH := 486.0
const HEADER_FONT_SIZE := 18
const HEADER_BOLD_EMBOLDEN := 0.70
const HEADER_LABEL_WIDTH := 540.0
const HEADER_TOP_Y := 12.0
const HEADER_TOP_HEIGHT := 56.0
const HEADER_SEPARATOR_Y := 70.0
const HEADER_SECOND_Y := 74.0
const HEADER_SECOND_HEIGHT := 66.0
const FOOTER_FONT_SIZE := 13
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
var _header_math: Label
var _header_hook: Label
var _header_animator: RefCounted
var _authoring_json_path: String = ""

func _ready() -> void:
    scale = Vector2(OUTPUT_SCALE, OUTPUT_SCALE)
    _seed = _resolve_seed()
    _show_footer = _resolve_footer_visibility()
    _variation = VariationProfileClass.build("living_particles", _seed)
    _palette = PaletteBankClass.palette("living_particles", int(_variation["palette_mode"]), _seed)
    _text_colors = EditorialColorsClass.palette("living_particles", _palette)
    _authoring_json_path = "res://artifacts/prototypes/c11c_living_particles_v1/LivingParticles_v1_seed_%d_authoring.json" % _seed
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
    _renderer.name = "LivingParticlesRenderer"
    frame.get_body_content_root().add_child(_renderer)
    _renderer.set_background(BLACK)
    _renderer.set_palette(ColorBoostClass.vivid(Color(str(_palette["deep"])), 1.24, 1.03), ColorBoostClass.vivid(Color(str(_palette["mid"]))), ColorBoostClass.vivid(Color(str(_palette["bright"]))), ColorBoostClass.vivid(Color(str(_palette["highlight"]))))
    _renderer.set_style(
        int(_variation["grammar_mode"]), float(_variation["particle_count"]), float(_variation["glow"]),
        Vector2(float(_variation["attractor_a_x"]), float(_variation["attractor_a_y"])), Vector2(float(_variation["attractor_b_x"]), float(_variation["attractor_b_y"])),
        float(_variation["swirl_bias"]), float(_variation["particle_spread"]), float(_variation["turbulence"]), float(_variation["attractor_strength"]),
        float(_variation["particle_size_scale"]), float(_variation["phase_rate"]), float(_variation["collision_strength"]), float(_variation["core_scale"]),
        float(_variation["density_bias"]), float(_variation["color_diversity"]), float(_variation["color_phase"])
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
    rule_a.position = Vector2(36.0, HEADER_SEPARATOR_Y)
    rule_a.size = Vector2(468.0, 1.0)
    rule_a.color = rule_color
    frame.get_header_content_root().add_child(rule_a)

    var rule_b := ColorRect.new()
    rule_b.position = Vector2(36.0, 14.0)
    rule_b.size = Vector2(468.0, 1.0)
    rule_b.color = rule_color
    frame.get_footer_content_root().add_child(rule_b)

func _add_header(root: Control) -> void:
    var grammar_names: Array[String] = ["SWARM", "VORTEX", "COLLISION CLOUD", "ORGANIC PULSE", "MAGNETIC FILAMENT CLOUD"]
    var grammar_index: int = int(_variation["grammar_mode"])
    var grammar_name: String = grammar_names[grammar_index].to_upper()
    var line1: String = "%s | DENSITY %.2f | FLOW %.2f" % [grammar_name.replace(" ", "_"), float(_variation["density_bias"]), float(_variation["swirl_bias"])]
    var line2: String = TechnobabbleGeneratorClass.generate_geek_text("living_particles", _seed, _variation).to_upper()
    var wrapped_line2: String = HEADER_ANIMATOR_SCRIPT.wrap_two_lines(line2, root.get_theme_default_font(), HEADER_FONT_SIZE, HEADER_MAX_WIDTH)

    # Both editorial blocks share the same 18 px bold treatment. The second block
    # is explicitly wrapped at word boundaries so no word is ever split.
    _header_math = _new_header_label(line1, Vector2(0.0, HEADER_TOP_Y), Vector2(HEADER_LABEL_WIDTH, HEADER_TOP_HEIGHT), _text_colors["header_math"])
    _header_math.add_theme_constant_override("outline_size", 1)
    _header_math = HEADER_ANIMATOR_SCRIPT.apply_bold(_header_math, HEADER_BOLD_EMBOLDEN)
    root.add_child(_header_math)

    _header_hook = _new_header_label(wrapped_line2, Vector2(0.0, HEADER_SECOND_Y), Vector2(HEADER_LABEL_WIDTH, HEADER_SECOND_HEIGHT), _text_colors["header_hook"])
    _header_hook.add_theme_constant_override("outline_size", 1)
    _header_hook = HEADER_ANIMATOR_SCRIPT.apply_bold(_header_hook, HEADER_BOLD_EMBOLDEN)
    root.add_child(_header_hook)

    _header_animator = HEADER_ANIMATOR_SCRIPT.new(line1, wrapped_line2, _seed + 7919)

func _add_footer(root: Control) -> void:
    var line2: String = "SEED %d | BODY 720X896 | T=18.00S | PARTICLES %d | FLOW %.2f" % [_seed, int(round(float(_variation["particle_count"]))), float(_variation["swirl_bias"])]
    var line3: String = "PALETTE %s | LOOP x%d | AUDIO AMBIENT" % [str(_palette["name"]).to_upper(), int(_variation["loop_cycles"])]
    var line4: String = "SYNTHETIC MATTER / v2.1.4"
    root.add_child(_new_footer_label(line2, Vector2(0.0, 20.0), _text_colors["footer_data"]))
    root.add_child(_new_footer_label(line3, Vector2(0.0, 47.0), _text_colors["footer_palette"]))
    root.add_child(_new_footer_label(line4, Vector2(0.0, 74.0), _text_colors["footer_signature"]))

func _new_footer_label(text_value: String, pos: Vector2, color: Color) -> Label:
    var label := _new_label(text_value, pos, Vector2(540.0, 24.0), FOOTER_FONT_SIZE, color)
    var font: Font = label.get_theme_default_font()
    var fitted: int = FOOTER_FONT_SIZE
    while fitted > 12 and font.get_string_size(text_value, HORIZONTAL_ALIGNMENT_LEFT, -1, fitted).x > 508.0:
        fitted -= 1
    label.add_theme_font_size_override("font_size", fitted)
    return label

func _new_header_label(text_value: String, pos: Vector2, box_size: Vector2, color: Color) -> Label:
    var label := _new_label(text_value, pos, box_size, HEADER_FONT_SIZE, color)
    label.add_theme_constant_override("line_spacing", 0)
    return label

func _resolve_footer_visibility() -> bool:
    var raw: String = OS.get_environment("C11C_SHOW_FOOTER").strip_edges().to_lower()
    return raw not in ["0", "false", "off", "no"]

func _resolve_seed() -> int:
    var raw: String = OS.get_environment("C11C_SEED").strip_edges()
    return int(raw) if raw.is_valid_int() else REFERENCE_SEED

func _new_label(text_value: String, pos: Vector2, box_size: Vector2, font_size: int, color: Color) -> Label:
    var label := Label.new()
    label.text = text_value
    label.position = pos
    label.size = box_size
    label.mouse_filter = Control.MOUSE_FILTER_IGNORE
    label.add_theme_font_size_override("font_size", font_size)
    label.add_theme_color_override("font_color", color)
    label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
    label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
    label.clip_text = true
    return label

func _process(_delta: float) -> void:
    if _renderer == null:
        return
    _renderer.set_frame(_frame_index, FRAME_COUNT, _seed_phase(_seed), float(_variation["loop_cycles"]))
    if _header_animator != null:
        var editorial: Dictionary = _header_animator.display_at(_frame_index, FRAME_COUNT)
        _header_math.text = str(editorial["line1_text"])
        _header_hook.text = str(editorial["line2_text"])
        var alpha: float = 0.90 if bool(editorial["transition"]) else 1.0
        _header_math.modulate = Color(1.0, 1.0, 1.0, alpha)
        _header_hook.modulate = Color(1.0, 1.0, 1.0, alpha)
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
    var grammar_names: Array[String] = ["SWARM", "VORTEX", "COLLISION CLOUD", "ORGANIC PULSE", "MAGNETIC FILAMENT CLOUD"]
    var grammar_name: String = grammar_names[grammar_index]
    var header_line_2: String = TechnobabbleGeneratorClass.generate_geek_text("living_particles", _seed, _variation).to_upper()
    var header_math: String = "%s | DENSITY %.2f | FLOW %.2f" % [grammar_name.replace(" ", "_"), float(_variation["density_bias"]), float(_variation["swirl_bias"])]
    var sound_raw: String = OS.get_environment("C11C_SOUND_ENABLED").strip_edges().to_lower()
    var sound_enabled: bool = sound_raw not in ["0", "false", "off", "no"]
    var snapshot := {
        "family_id": "living_particles",
        "display_name": "LIVING PARTICLES",
        "seed": _seed,
        "grammar_mode": grammar_index,
        "grammar": grammar_name,
        "palette_mode": int(_variation["palette_mode"]),
        "palette": str(_variation["palette_name"]),
        "loop_cycles": float(_variation["loop_cycles"]),
        "duration_seconds": LOOP_DURATION,
        "fps": FPS,
        "frame_count": FRAME_COUNT,
        "header_primary": header_line_2,
        "header_line_1": header_math,
        "header_line_2": header_line_2,
        "header_secondary": "VISUAL LOOP / LIVING PARTICLES",
        "header_math": header_math,
        "technobabble": TechnobabbleGeneratorClass.generate_geek_text("living_particles", _seed, _variation),
        "technobabble_revision": TechnobabbleGeneratorClass.revision(),
        "audio_style": "soft pulsed matter bed / rounded particle tones / fluid harmonic drift / midpoint swirl swell",
        "sound_enabled": sound_enabled,
        "background": "000000",
        "footer_enabled": _show_footer,
        "editorial_revision": "2.1.4",
        "loop_closed": true
    }
    var file := FileAccess.open(absolute_path, FileAccess.WRITE)
    if file != null:
        file.store_string(JSON.stringify(snapshot, "  "))
        file.close()

