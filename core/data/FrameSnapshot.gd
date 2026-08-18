class_name FrameSnapshot
extends RefCounted

var position: Vector2 = Vector2.ZERO
var rotation: float = 0.0
var scale: Vector2 = Vector2.ONE
var opacity: float = 1.0
var texture_index: int = 0
var variant_id: int = 0

# Almacena variables dinámicas específicas de cada mecánica
var custom_data: Dictionary = {}

## Valida que la transformación no contenga valores corruptos (NaN o Infinito)
func is_valid_snapshot() -> bool:
	if is_nan(position.x) or is_nan(position.y) or is_inf(position.x) or is_inf(position.y):
		return false
	if is_nan(rotation) or is_inf(rotation):
		return false
	if is_nan(scale.x) or is_nan(scale.y) or is_inf(scale.x) or is_inf(scale.y):
		return false
	if is_nan(opacity) or is_inf(opacity):
		return false
	return true