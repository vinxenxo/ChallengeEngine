# res://core/runtime/visual_drill/VisualDrillGenerator.gd
class_name VisualDrillGenerator
extends RefCounted

## C6-F0.4.2 — Visual Drill Generator Abstract Base Interface.
## Enforces stateless, pure functional transformations from temporal frame to logical exercise state.

func generate(frame_index: int, total_frames: int, drill_parameters: Dictionary) -> Dictionary:
	push_error("VisualDrillGenerator base class is abstract and must be subclassed.")
	return {}