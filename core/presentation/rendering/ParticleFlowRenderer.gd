class_name ParticleFlowRenderer
extends Node2D

## C6-F0.8-D5 — Particle Flow Renderer (Passive)
## Binds Logical Layer State directly to GPU Shader parameters.

const PARTICLE_SHADER = preload("res://core/presentation/rendering/shaders/particle_flow.gdshader")

var _rect: ColorRect
var _material: ShaderMaterial

func _init() -> void:
	_rect = ColorRect.new()
	_material = ShaderMaterial.new()
	_material.shader = PARTICLE_SHADER
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
	
	_material.set_shader_parameter("time_cycle", float(params.get("time_cycle", 0.0)))
	_material.set_shader_parameter("dispersion", float(params.get("dispersion", 0.0)))
	_material.set_shader_parameter("particle_count", float(params.get("particle_count", 16.0)))
	_material.set_shader_parameter("global_rotation", float(params.get("global_rotation", 0.0)))
	_material.set_shader_parameter("zoom", float(params.get("zoom", 1.0)))
	
	if layer.get("color_palette", "") == "fire":
		_material.set_shader_parameter("base_color", Color(0.9, 0.4, 0.2, 1.0))
	else:
		_material.set_shader_parameter("base_color", Color(0.3, 0.9, 0.5, 1.0))