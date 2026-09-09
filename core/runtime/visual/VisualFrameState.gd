class_name VisualFrameState
extends RefCounted

## C6-F0.4.1 — Visual Frame State.
## Encapsulates the deterministic, stateless, render-ready logical state of a visual loop frame.
## This is the explicit output of the VisualLoopRuntime.

var frame_index: int = 0
var loop_frame: int = 0
var loop_iteration: int = 0
var generator_type: String = ""
var layer_states: Array[Dictionary] = []

func to_dictionary() -> Dictionary:
	return {
		"frame_index": frame_index,
		"loop_frame": loop_frame,
		"loop_iteration": loop_iteration,
		"generator_type": generator_type,
		"layer_states": layer_states.duplicate(true)
	}