class_name WinningHighlightComponent
extends RefCounted

## C6-E4 — Winning Frame Visual Emphasis
## Presentation-only. No simulation, RNG or winning-frame calculation.
## The caller supplies the already-resolved visual bounds of the affected elements.

const DEFAULT_BORDER_WIDTH: int = 6
const DEFAULT_PADDING: float = 12.0
const DEFAULT_CORNER_RADIUS: int = 10
const DEFAULT_ALPHA: float = 0.98

var root: Control
var highlight_nodes: Array[Panel] = []
var border_width: int = DEFAULT_BORDER_WIDTH
var padding: float = DEFAULT_PADDING
var corner_radius: int = DEFAULT_CORNER_RADIUS
var accent_color: Color = Color(0.18, 0.95, 0.35, DEFAULT_ALPHA)

func _init(parent: Control, config: Dictionary = {}):
    root = parent
    border_width = int(config.get("border_width", DEFAULT_BORDER_WIDTH))
    padding = float(config.get("padding", DEFAULT_PADDING))
    corner_radius = int(config.get("corner_radius", DEFAULT_CORNER_RADIUS))
    var configured_color = config.get("color", accent_color)
    if configured_color is Color:
        accent_color = configured_color
    _ensure_pool(2)
    hide()

func _ensure_pool(count: int) -> void:
    if root == null:
        return
    while highlight_nodes.size() < count:
        var panel := Panel.new()
        panel.name = "WinningHighlight_%d" % highlight_nodes.size()
        panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
        panel.z_index = 10
        root.add_child(panel)
        highlight_nodes.append(panel)
        _apply_style(panel)

func _apply_style(panel: Panel) -> void:
    var style := StyleBoxFlat.new()
    style.bg_color = Color(0.0, 0.0, 0.0, 0.0)
    style.border_color = accent_color
    style.set_border_width_all(border_width)
    style.set_corner_radius_all(corner_radius)
    panel.add_theme_stylebox_override("panel", style)

func show_for_rects(rects: Array) -> void:
    if root == null:
        return

    var valid_rects: Array[Rect2] = []
    for value in rects:
        if value is Rect2 and value.size.x > 0.0 and value.size.y > 0.0:
            valid_rects.append(value)

    _ensure_pool(max(2, valid_rects.size()))
    hide()

    if valid_rects.is_empty():
        return

    for i in range(valid_rects.size()):
        var panel: Panel = highlight_nodes[i]
        var rect: Rect2 = valid_rects[i].grow(padding)
        panel.position = rect.position
        panel.size = rect.size
        panel.visible = true
        _apply_style(panel)

func hide() -> void:
    for panel in highlight_nodes:
        if panel != null:
            panel.visible = false

func is_visible() -> bool:
    for panel in highlight_nodes:
        if panel != null and panel.visible:
            return true
    return false
