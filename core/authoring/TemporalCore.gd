# res://core/authoring/TemporalCore.gd
class_name TemporalCore
extends RefCounted

## C6-F0.3.4 — Temporal Abstraction Core.
## Strict, pure monotonic frame counter and base cardinality calculator.
## Does not know about content phases, loop seamlessness, or challenge semantics.

var fps: int = 60
var total_frames: int = 0
var _current_frame: int = 0

func _init(p_fps: int = 60) -> void:
	fps = p_fps
	if fps <= 0:
		fps = 60

## La única autoridad matemática de conversión temporal en el motor.
func duration_to_frames(duration_seconds: float) -> int:
	return maxi(0, int(round(duration_seconds * float(fps))))

## Avance monotónico absoluto, sin clamps, loops ni cortes.
func advance() -> void:
	_current_frame += 1

func get_current_frame() -> int:
	return _current_frame

func is_finished() -> bool:
	return _current_frame >= total_frames