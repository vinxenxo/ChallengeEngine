# res://core/presentation/rendering/TrackingRenderer.gd
extends Node2D

## C6-F0.8-E2 — Tracking Drill Renderer (Passive)
## Binds Logical Drill State directly to GPU Shader parameters for Stream 2011.

const TRACKING_SHADER = preload("res://core/presentation/rendering/shaders/tracking.gdshader")

var _rect: ColorRect
var _material: ShaderMaterial

func _init() -> void:
	_rect = ColorRect.new()
	_material = ShaderMaterial.new()
	_material.shader = TRACKING_SHADER
	_rect.material = _material
	add_child(_rect)

func apply_state(model: Dictionary) -> void:
	var geometry: Dictionary = model.get("geometry", {})
	var content_rect: Rect2 = geometry.get("content_rect", Rect2(0, 0, 1080, 1920))
	
	_rect.position = content_rect.position
	_rect.size = content_rect.size
	
	var drill_state: Dictionary = model.get("drill_frame_state", model)
	var progress := float(drill_state.get("progress", 0.0))
	var stimulus: Dictionary = drill_state.get("stimulus_state", {})
	var params: Dictionary = drill_state.get("parameters", {})
	
	var stim_x := float(stimulus.get("x", 50.0)) / 100.0
	var stim_y := float(stimulus.get("y", 50.0)) / 100.0
	
	_material.set_shader_parameter("progress", progress)
	_material.set_shader_parameter("stimulus_pos", Vector2(stim_x, stim_y))
	_material.set_shader_parameter("tracking_variant", float(params.get("tracking_variant", 0.0)))
	_material.set_shader_parameter("base_color", Color(0.2, 0.6, 1.0, 1.0))