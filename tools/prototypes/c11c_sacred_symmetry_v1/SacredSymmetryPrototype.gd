extends Node2D

## C11-C editorial/audio/loop presentation prototype v2.2.1.
## R4: shared two-line Matrix intro/midpoint swap + family-synced ambient audio.
## Family: SACRED SYMMETRY
## Presentation-only: no core, simulation, SimulationResult, engine RNG or C7 changes.

const UnifiedSocialFrameScene = preload("res://core/presentation/UnifiedSocialFrame.tscn")
const RendererClass = preload("res://tools/prototypes/c11c_sacred_symmetry_v1/SacredSymmetryRenderer.gd")
const TechnobabbleGeneratorClass = preload("res://tools/prototypes/c11c_common/TechnobabbleGenerator.gd")
const VariationProfileClass = preload("res://tools/prototypes/c11c_common/C11CVariationProfile.gd")
const PaletteBankClass = preload("res://tools/prototypes/c11c_common/C11CPaletteBank.gd")
const C11CThemeClass = preload("res://tools/prototypes/c11c_common/C11CTheme.gd")
const EditorialColorsClass = preload("res://tools/prototypes/c11c_common/C11CEditorialColors.gd")
const ColorBoostClass = preload("res://tools/prototypes/c11c_common/C11CColorBoost.gd")
const C11CVisualEditorialLayerClass = preload("res://core/presentation/C11CVisualEditorialLayer.gd")
const C11CVisualLoopDurationClass = preload("res://tools/prototypes/c11c_common/C11CVisualLoopDuration.gd")

const REFERENCE_SEED := 314159
const DEFAULT_LOOP_DURATION := 0.0
const FPS := C11CVisualLoopDurationClass.FPS
const GRAMMAR_IDS: Array[String] = ["astrolabe", "gear_train", "polygon_orrery", "origami_mandala", "celestial_chart"]
const GRAMMAR_NAMES: Array[String] = ["ASTROLABE", "GEAR TRAIN", "POLYGON ORRERY", "ORIGAMI MANDALA", "CELESTIAL CHART"]
const OUTPUT_SCALE := 4.0 / 3.0
const BLACK: Color = C11CThemeClass.SECTION_BACKGROUND

var _renderer: Node2D
var _frame_index: int = 0
var _seed: int = REFERENCE_SEED
var _show_footer: bool = true
var _variation: Dictionary = {}
var _palette: Dictionary = {}
var _text_colors: Dictionary = {}
var _editorial_layer: RefCounted = null
var _editorial_model: Dictionary = {}
var _authoring_json_path: String = ""
var _loop_duration: float = 0.0
var _frame_count: int = 0

func _ready() -> void:
    scale = Vector2(OUTPUT_SCALE, OUTPUT_SCALE)
    _seed = _resolve_seed()
    _show_footer = _resolve_footer_visibility()
    _variation = VariationProfileClass.build("sacred_symmetry", _seed)
    _apply_grammar_override()
    var duration_policy: Dictionary = C11CVisualLoopDurationClass.resolve(int(_variation["loop_cycles"]), DEFAULT_LOOP_DURATION)
    _loop_duration = float(duration_policy["duration_seconds"])
    _frame_count = int(duration_policy["frame_count"])
    _palette = PaletteBankClass.palette("sacred_symmetry", int(_variation["palette_mode"]))
    _text_colors = EditorialColorsClass.palette("sacred_symmetry", _palette)
    var authoring_override: String = OS.get_environment("C11C_AUTHORING_OUTPUT_PATH").strip_edges()
    if authoring_override.is_empty():
        _authoring_json_path = "res://artifacts/prototypes/c11c_sacred_symmetry_v1/SacredSymmetry_v1_seed_%d_authoring.json" % _seed
    else:
        _authoring_json_path = authoring_override
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
    _mount_editorial(frame)

    _renderer = RendererClass.new()
    _renderer.name = "SacredSymmetryRenderer"
    frame.get_body_content_root().add_child(_renderer)
    _renderer.set_background(BLACK)
    _renderer.set_palette(ColorBoostClass.vivid(Color(str(_palette["primary"]))), ColorBoostClass.vivid(Color(str(_palette["secondary"]))), ColorBoostClass.vivid(Color(str(_palette["highlight"]))), ColorBoostClass.vivid(Color(str(_palette["white_gold"])), 1.12, 1.06), ColorBoostClass.vivid(Color(str(_palette["accent"]))))
    _renderer.set_style(
        int(_variation["grammar_mode"]), float(_variation["symmetry_order"]), float(_variation["ring_bias"]), float(_variation["glow"]), float(_variation["gear_inner"]), float(_variation["gear_outer"]),
        float(_variation["ring_scale"]), float(_variation["core_scale"]), float(_variation["tick_density"]), float(_variation["mechanical_rate"]), float(_variation["macro_scale"]),
        float(_variation["node_density"]), float(_variation["fold_depth"]), float(_variation["color_diversity"]), float(_variation["color_phase"])
    )
    _renderer.set_frame(0, _frame_count, _seed_phase(_seed), float(_variation["loop_cycles"]))

func _mount_editorial(frame: UnifiedSocialFrame) -> void:
    _editorial_layer = C11CVisualEditorialLayerClass.new()
    if _editorial_layer == null or not _editorial_layer.mount(frame):
        push_error("[C11-C 2.2.1] Shared editorial layer could not be mounted for c11c_sacred_symmetry_v1.")
        _editorial_layer = null
        return
    var grammar_index: int = int(_variation["grammar_mode"])
    var grammar_name: String = GRAMMAR_NAMES[grammar_index].to_upper()
    var line1: String = "%s | N=%d | GEAR %d:%d" % [grammar_name.replace(" ", "_"), int(_variation["symmetry_order"]), int(_variation["gear_inner"]), int(_variation["gear_outer"])]
    var header_line_2: String = TechnobabbleGeneratorClass.generate_geek_text("sacred_symmetry", _seed, _variation).to_upper()
    var footer_line2: String = "SEED %d | BODY 720X896 | T=%.2fS | N=%d | GEAR %d:%d" % [_seed, _loop_duration, int(_variation["symmetry_order"]), int(_variation["gear_inner"]), int(_variation["gear_outer"])]
    var footer_line3: String = "PALETTE %s | LOOP x%d | FAMILY MUSIC V4" % [str(_palette["name"]).to_upper(), int(_variation["loop_cycles"])]
    var footer_line_3: String = "PRECISION CELESTIAL MECHANISM / v2.2.1"

    _editorial_model = {
        "editorial": {
            "enabled": true,
            "show_header": true,
            "show_footer": _show_footer,
            "show_header_rule": true,
            "show_footer_rule": true,
            "matrix_enabled": true,
            "header": {
                "line_1": line1,
                "line_2": header_line_2
            },
            "footer": {
                "line_1": footer_line2,
                "line_2": footer_line3,
                "line_3": footer_line_3
            },
            "colors": {
                "header_secondary": _text_colors["header_hook"],
                "footer_data": _text_colors["footer_data"],
                "rule": _text_colors["rule"]
            }
        },
        "editorial_seed": _seed,
        "editorial_frame_index": 0,
        "editorial_frame_count": _frame_count
    }
    _editorial_layer.apply_render_model(_editorial_model)

func _resolve_footer_visibility() -> bool:
    var raw: String = OS.get_environment("C11C_SHOW_FOOTER").strip_edges().to_lower()
    return raw not in ["0", "false", "off", "no"]

func _apply_grammar_override() -> void:
    var requested: String = OS.get_environment("C11C_VISUAL_GRAMMAR").strip_edges().to_lower()
    if requested.is_empty():
        return
    requested = requested.replace("-", "_").replace(" ", "_")
    for index in range(GRAMMAR_IDS.size()):
        var technical_id: String = GRAMMAR_IDS[index]
        var artistic_id: String = GRAMMAR_NAMES[index].to_lower().replace(" ", "_")
        if requested == technical_id or requested == artistic_id:
            _variation["grammar_mode"] = index
            _variation["grammar_name"] = technical_id
            return
    push_error("Unknown visual grammar override for c11c_sacred_symmetry_v1: %s" % requested)

func _resolve_seed() -> int:
    var raw: String = OS.get_environment("C11C_SEED").strip_edges()
    return int(raw) if raw.is_valid_int() else REFERENCE_SEED

func _process(_delta: float) -> void:
    if _renderer == null:
        return
    _renderer.set_frame(_frame_index, _frame_count, _seed_phase(_seed), float(_variation["loop_cycles"]))
    if _editorial_layer != null and not _editorial_model.is_empty():
        _editorial_model["editorial_frame_index"] = _frame_index
        _editorial_layer.apply_render_model(_editorial_model)
    if _frame_index >= _frame_count - 1:
        get_tree().quit()
    else:
        _frame_index += 1

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
    var grammar_name: String = GRAMMAR_NAMES[grammar_index]
    var header_line_2: String = TechnobabbleGeneratorClass.generate_geek_text("sacred_symmetry", _seed, _variation).to_upper()
    var header_math: String = "%s | N=%d | GEAR %d:%d" % [grammar_name.replace(" ", "_"), int(_variation["symmetry_order"]), int(_variation["gear_inner"]), int(_variation["gear_outer"])]
    var sound_raw: String = OS.get_environment("C11C_SOUND_ENABLED").strip_edges().to_lower()
    var sound_enabled: bool = sound_raw not in ["0", "false", "off", "no"]
    var snapshot := {
        "family_id": "sacred_symmetry",
        "audio_profile": "ORBITAL_RITUAL",
        "audio_pairing_mode": "FAMILY_MUSIC_V4",
        "display_name": "SACRED SYMMETRY",
        "seed": _seed,
        "grammar_mode": grammar_index,
        "grammar_id": GRAMMAR_IDS[grammar_index],
        "grammar": grammar_name,
        "palette_mode": int(_variation["palette_mode"]),
        "palette": str(_variation["palette_name"]),
        "loop_cycles": float(_variation["loop_cycles"]),
        "duration_seconds": _loop_duration,
        "fps": FPS,
        "frame_count": _frame_count,
        "header_primary": header_line_2,
        "header_line_1": header_math,
        "header_line_2": header_line_2,
        "header_secondary": "VISUAL LOOP / SACRED SYMMETRY",
        "header_math": header_math,
        "technobabble": TechnobabbleGeneratorClass.generate_geek_text("sacred_symmetry", _seed, _variation),
        "technobabble_revision": TechnobabbleGeneratorClass.revision(),
        "audio_style": "soft celestial chime bed / aligned harmonics / restrained bell overtones / midpoint orbit swell",
        "sound_enabled": sound_enabled,
        "background": "000000",
        "footer_enabled": _show_footer,
        "editorial_revision": "2.2.1",
        "loop_closed": true
    }
    var file := FileAccess.open(absolute_path, FileAccess.WRITE)
    if file != null:
        file.store_string(JSON.stringify(snapshot, "  "))
        file.close()

