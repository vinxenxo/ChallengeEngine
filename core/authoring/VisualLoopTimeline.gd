class_name VisualLoopTimeline
extends TemporalCore

## C6-F0.3.4 — Visual Loop Timeline.
## Translates monotonic time into wrapped loop iterations via semantic boundaries.

func _init(duration: float, p_fps: int) -> void:
	super._init(p_fps)
	total_frames = duration_to_frames(duration)

## Proporciona el índice local de bucle, envolviendo el cursor monotónico.
func get_loop_frame() -> int:
	if total_frames <= 0:
		return 0
	return _current_frame % total_frames
	
## Proporciona el recuento de vueltas completas efectuadas.
func get_loop_iteration() -> int:
	if total_frames <= 0:
		return 0
	return _current_frame / total_frames