class_name VisualDrillRenderer
extends Node2D

## Visual Drill Renderer Router.
## Hosts all visual drill renderers (Peripheral Scan, Tracking, Pursuit, Saccade).

const PeripheralScanRendererClass = preload("res://core/presentation/rendering/PeripheralScanRenderer.gd")
const TrackingRendererClass = preload("res://core/presentation/rendering/TrackingRenderer.gd")

var _frame_state: Dictionary = {}
var _peripheral_renderer: Node2D = null
var _tracking_renderer: Node2D = null

func _ready() -> void:
	_peripheral_renderer = PeripheralScanRendererClass.new()
	_peripheral_renderer.visible = false
	add_child(_peripheral_renderer)
	
	_tracking_renderer = TrackingRendererClass.new()
	_tracking_renderer.visible = false
	add_child(_tracking_renderer)

func apply_state(model: Dictionary) -> void:
	_frame_state = model.duplicate(true)
	
	var drill_state: Dictionary = model.get("drill_frame_state", model)
	var generator_type := str(drill_state.get("generator_type", ""))
	
	if _peripheral_renderer != null:
		_peripheral_renderer.visible = (generator_type == "peripheral_scan")
	if _tracking_renderer != null:
		_tracking_renderer.visible = (generator_type == "tracking")
	
	if generator_type == "peripheral_scan" and _peripheral_renderer != null:
		_peripheral_renderer.apply_state(model)
	elif generator_type == "tracking" and _tracking_renderer != null:
		_tracking_renderer.apply_state(model)
		
	queue_redraw()

func _draw() -> void:
	var p_vis = _peripheral_renderer != null and _peripheral_renderer.visible
	var t_vis = _tracking_renderer != null and _tracking_renderer.visible
	
	if _frame_state.is_empty() or p_vis or t_vis:
		return
		
	# Fallback geométrico básico para subtipos en desarrollo (Pursuit / Saccade)
	var drill_state: Dictionary = _frame_state.get("drill_frame_state", _frame_state)
	var stimulus: Dictionary = drill_state.get("stimulus_state", {})
	var x := float(stimulus.get("x", 540.0))
	var y := float(stimulus.get("y", 960.0))
	
	draw_circle(Vector2(x, y), 25.0, Color(1.0, 0.8, 0.2, 1.0))