class_name VisualLoopGenerator
extends RefCounted

## C6-F0.4.1 — Visual Loop Generator Abstract Base Interface.
## Enforces stateless, pure functional transformations from temporal frame to a logical layer state dictionary.
## Generator Output Contract: returns a Logical Layer State (Dictionary).

func generate(loop_frame: int, total_frames: int, layer_params: Dictionary) -> Dictionary:
	push_error("VisualLoopGenerator base class is abstract and must be subclassed.")
	return {}