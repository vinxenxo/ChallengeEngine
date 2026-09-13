# res://core/presentation/rendering/VectorFieldRenderer.gd
class_name VectorFieldRenderer
extends Node2D

## C6-F0.8-D4 — Vector Field Renderer (Passive)
## Binds Logical Layer State directly to GPU Shader parameters.

const FIELD_SHADER = preload("res://core/presentation/rendering/shaders/vector_field.gdshader")

var _rect: ColorRect
var _material: ShaderMaterial

func _init() -> void:
	_rect = ColorRect.new()
	_material = ShaderMaterial.new()
	_material.shader = FIELD_SHADER
	_rect.material = _material
	add_child(_rect)

func apply_state(model: Dictionary) -> void:
	# 1. Geometry Binding Contract
	var geometry: Dictionary = model.get("geometry", {})
	var content_rect: Rect2 = geometry.get("content_rect", Rect2(0, 0, 1080, 1920))
	
	_rect.position = content_rect.position
	_rect.size = content_rect.size
	
	# 2. Extract State Payload
	var v_state: Dictionary = model.get("visual_frame_state", model)
	var layers: Array = v_state.get("layers", v_state.get("layer_states", []))
	if layers.is_empty():
		return
		
	var layer: Dictionary = layers[0]
	var params: Dictionary = layer.get("parameters", layer)
	
	# 3. GPU Injection (Dumb binding)
	_material.set_shader_parameter("flow_angle", float(params.get("flow_angle", 0.0)))
	_material.set_shader_parameter("turbulence", float(params.get("turbulence", 0.0)))
	_material.set_shader_parameter("grid_density", float(params.get("grid_density", 10.0)))
	_material.set_shader_parameter("global_rotation", float(params.get("global_rotation", 0.0)))
	_material.set_shader_parameter("zoom", float(params.get("zoom", 1.0)))
	
	if layer.get("color_palette", "") == "ocean":
		_material.set_shader_parameter("base_color", Color(0.1, 0.7, 0.9, 1.0))
	else:
		_material.set_shader_parameter("base_color", Color(0.8, 0.3, 0.5, 1.0))