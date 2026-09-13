# res://core/presentation/rendering/GeometricRenderer.gd
extends Node2D

## C6-F0.8-D7 — Geometric Renderer (Passive)
## Binds Logical Layer State directly to GPU Shader parameters.

const GEOMETRIC_SHADER = preload("res://core/presentation/rendering/shaders/geometric.gdshader")

var _rect: ColorRect
var _material: ShaderMaterial

func _init() -> void:
	_rect = ColorRect.new()
	_material = ShaderMaterial.new()
	_material.shader = GEOMETRIC_SHADER
	_rect.material = _material
	add_child(_rect)

func apply_state(model: Dictionary) -> void:
	var geometry: Dictionary = model.get("geometry", {})
	var content_rect: Rect2 = geometry.get("content_rect", Rect2(0, 0, 1080, 1920))
	
	_rect.position = content_rect.position
	_rect.size = content_rect.size
	
	var v_state: Dictionary = model.get("visual_frame_state", model)
	var layers: Array = v_state.get("layers", v_state.get("layer_states", []))
	if layers.is_empty():
		return
		
	var layer: Dictionary = layers[0]
	var params: Dictionary = layer.get("parameters", layer)
	
	_material.set_shader_parameter("rotation_angle", float(params.get("rotation_angle", 0.0)))
	_material.set_shader_parameter("sides", float(params.get("sides", 4.0)))
	_material.set_shader_parameter("zoom", float(params.get("zoom", 1.0)))
	
	if layer.get("color_palette", "") == "amethyst":
		_material.set_shader_parameter("base_color", Color(0.7, 0.2, 0.9, 1.0))
	else:
		_material.set_shader_parameter("base_color", Color(0.6, 0.3, 0.9, 1.0))