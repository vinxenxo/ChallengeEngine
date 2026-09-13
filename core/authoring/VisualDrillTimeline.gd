# res://core/authoring/VisualDrillTimeline.gd
class_name VisualDrillTimeline
extends TemporalCore

## C6-F0.3.4 — Visual Drill Timeline.
## Inherits base temporal progression. Phase semantics pending explicit JSON schema definition.

func _init(duration: float, p_fps: int) -> void:
	super._init(p_fps)
	total_frames = duration_to_frames(duration)