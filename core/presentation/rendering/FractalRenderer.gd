class_name FractalRenderer
extends Node2D

## C6-F0.8-D2-C — Fractal Renderer (Passive)
## Purely visual node. Decoupled from simulation and RNG.
## Binds Logical Layer State directly to GPU Shader parameters and adheres to PresentationProfile Geometry.

const FRACTAL_SHADER = preload("res://core/presentation/rendering/shaders/fractal.gdshader")

var _rect: ColorRect
var _material: ShaderMaterial

func _init() -> void:
	_rect = ColorRect.new()
	_material = ShaderMaterial.new()
	_material.shader = FRACTAL_SHADER
	_rect.material = _material
	add_child(_rect)

func apply_state(model: Dictionary) -> void:
	# 1. Geometry Binding Contract (C6-F0.8-A.1 / D0)
	var geometry: Dictionary = model.get("geometry", {})
	var content_rect: Rect2 = geometry.get("content_rect", Rect2(0, 0, 1080, 1920))
	
	_rect.position = content_rect.position
	_rect.size = content_rect.size
	
	# 2. Extract State Payload with robustness for raw payload injections (Testing/Legacy contexts)
	var v_state: Dictionary = model.get("visual_frame_state", model)
	var layers: Array = v_state.get("layers", v_state.get("layer_states", []))
	if layers.is_empty():
		return
		
	var layer: Dictionary = layers[0]
	var params: Dictionary = layer.get("parameters", layer) # Compatibilidad adicional de contrato
	
	# 3. GPU Injection (Dumb binding)
	_material.set_shader_parameter("zoom", float(params.get("zoom", 1.0)))
	_material.set_shader_parameter("rotation", float(params.get("rotation", 0.0)))
	_material.set_shader_parameter("phase", float(params.get("phase", 0.0)))
	_material.set_shader_parameter("complexity", float(params.get("complexity", 1.0)))
	
	if layer.get("color_palette", "") == "neon":
		_material.set_shader_parameter("base_color", Color(0.9, 0.1, 0.8, 1.0))
	else:
		_material.set_shader_parameter("base_color", Color(0.2, 0.6, 0.9, 1.0))