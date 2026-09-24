extends Node2D

## C11-C.8 — Pursuit / El Monolito en el Vacío.
## Presentation-only. No spline math or event generation occurs here.

const BODY_RECT := Rect2(0.0, 144.0, 540.0, 672.0)
const PursuitTargetLayerClass = preload("res://core/presentation/rendering/PursuitTargetLayer.gd")
const DrillPaletteBankClass = preload("res://tools/prototypes/c11c_common/C11CDrillPaletteBank.gd")
const DOF_SHADER = preload("res://core/presentation/rendering/shaders/pursuit_dof.gdshader")

var _frame_state: Dictionary = {}
var _background := Color("020710")
var _accent := Color("59E7FF")
var _secondary := Color("8D7CFF")
var _tertiary := Color("B7F5FF")
var _target := Color("FFFFFF")
var _target_soft := Color("E8FBFF")
var _target_layer: Node2D = null
var _dof_rect: ColorRect = null
var _dof_material: ShaderMaterial = null
var _palette_name := "VOID_CYAN"

func _ready() -> void:
    _target_layer = PursuitTargetLayerClass.new()
    _target_layer.name = "PursuitTargetHero"
    _target_layer.z_index = 100
    add_child(_target_layer)

    _dof_rect = ColorRect.new()
    _dof_rect.name = "PursuitRadialDOF"
    _dof_rect.position = BODY_RECT.position
    _dof_rect.size = BODY_RECT.size
    _dof_rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
    _dof_rect.z_index = 20
    _dof_material = ShaderMaterial.new()
    _dof_material.shader = DOF_SHADER
    _dof_rect.material = _dof_material
    add_child(_dof_rect)

func apply_state(model: Dictionary) -> void:
    _frame_state = model.duplicate(true)
    _apply_palette()
    _update_layers()
    queue_redraw()

func _apply_palette() -> void:
    var drill_state: Dictionary = _frame_state.get("drill_frame_state", _frame_state)
    var params: Dictionary = drill_state.get("parameters", {})
    var variant := clampf(float(params.get("pursuit_variant", 0.0)), 0.0, 0.999999)
    var palette := DrillPaletteBankClass.pursuit(variant)
    _palette_name = str(palette.get("name", "VOID_CYAN"))
    _background = Color(str(palette.get("background", "020710")))
    _accent = Color(str(palette.get("accent", "59E7FF")))
    _secondary = Color(str(palette.get("secondary", "8D7CFF")))
    _tertiary = Color(str(palette.get("tertiary", "B7F5FF")))
    _target = Color(str(palette.get("target", "FFFFFF")))
    _target_soft = Color(str(palette.get("target_soft", "E8FBFF")))

func _update_layers() -> void:
    if _target_layer == null:
        return
    var drill_state: Dictionary = _frame_state.get("drill_frame_state", _frame_state)
    var trajectory: Dictionary = drill_state.get("trajectory_state", {})
    var task: Dictionary = drill_state.get("task_state", {})
    var target_states: Array = drill_state.get("target_states", [])
    if target_states.size() != 1:
        _target_layer.visible = false
        return
    var target: Dictionary = target_states[0]
    var position := Vector2(float(target.get("x", 270.0)), float(target.get("y", 480.0)))
    var radius := float(target.get("radius", 20.0))
    var contrast := float(trajectory.get("camouflage_contrast", 1.0))
    var presentation_frame := int(_frame_state.get("presentation_frame_index", 0))
    var rotation_phase := float(presentation_frame) * 0.012
    _target_layer.visible = true
    _target_layer.configure(position, radius, _target, _accent, _secondary, _tertiary, contrast, rotation_phase, bool(task.get("sizygia_active", false)))

    if _dof_material != null:
        var focus_u := position.x / BODY_RECT.size.x
        var focus_v := (position.y - BODY_RECT.position.y) / BODY_RECT.size.y
        _dof_material.set_shader_parameter("focus_uv", Vector2(focus_u, focus_v))
        _dof_material.set_shader_parameter("focus_strength", 0.82)
        _dof_material.set_shader_parameter("focus_radius", 0.16)
        _dof_material.set_shader_parameter("outer_radius", 0.62)

func _draw() -> void:
    if _frame_state.is_empty():
        return
    draw_rect(BODY_RECT, _background, true)

    var seed_value := int(_frame_state.get("editorial_seed", 314159))
    var drill_state: Dictionary = _frame_state.get("drill_frame_state", _frame_state)
    var trajectory: Dictionary = drill_state.get("trajectory_state", {})
    var target_states: Array = drill_state.get("target_states", [])
    var target_position := Vector2(270.0, 480.0)
    if target_states.size() == 1:
        target_position = Vector2(float(target_states[0].get("x", 270.0)), float(target_states[0].get("y", 480.0)))

    # Sparse stars. Their apparent defocus is encoded by size/alpha before the
    # low-cost radial screen filter runs above them.
    for i in range(42):
        var h := _hash01(seed_value, 1200 + i * 17)
        var hx := _hash01(seed_value, 1300 + i * 19)
        var x := BODY_RECT.position.x + h * BODY_RECT.size.x
        var y := BODY_RECT.position.y + hx * BODY_RECT.size.y
        var point := Vector2(x, y)
        var distance_factor := clampf(point.distance_to(target_position) / 360.0, 0.0, 1.0)
        var radius := lerpf(0.45, 2.2, distance_factor)
        var alpha := lerpf(0.20, 0.055, distance_factor)
        draw_circle(point, radius, Color(_target_soft.r, _target_soft.g, _target_soft.b, alpha))

    # Quiet route echo: no future path disclosure, only a minimal spatial field.
    if not trajectory.is_empty():
        draw_circle(target_position, 58.0, Color(_accent.r, _accent.g, _accent.b, 0.018))
        draw_arc(target_position, 84.0, 0.0, TAU, 64, Color(_secondary.r, _secondary.g, _secondary.b, 0.035), 1.0, true)

    # Authored camouflage zones lower local target/background separation without
    # changing the authoritative target state.
    var camouflage := float(trajectory.get("camouflage_contrast", 1.0))
    if camouflage < 0.999:
        var suppression := clampf(1.0 - camouflage, 0.0, 0.95)
        draw_circle(target_position, 96.0, Color(_background.r, _background.g, _background.b, 0.18 * suppression))
        draw_circle(target_position, 60.0, Color(_background.r, _background.g, _background.b, 0.10 * suppression))

func _hash01(seed_value: int, salt: int) -> float:
    var x := (seed_value ^ int(salt * 374761393)) & 0x7fffffff
    x = int(((x ^ (x >> 13)) * 1274126177) & 0x7fffffff)
    x = int(((x ^ (x >> 16)) * 2246822519) & 0x7fffffff)
    return float((x ^ (x >> 13)) & 0x7fffffff) / 2147483647.0
