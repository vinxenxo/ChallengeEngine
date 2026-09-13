# res://core/runtime/visual_drill/VisualDrillFrameState.gd
class_name VisualDrillFrameState
extends RefCounted

## C6-F0.4.2 — Visual Drill Frame State.
## Encapsulates the deterministic, stateless, render-ready logical state of a visual drill frame.

var frame_index: int = 0
var progress: float = 0.0
var generator_type: String = ""
var stimulus_state: Dictionary = {}
var target_states: Array = []
var distractor_states: Array = []
var trajectory_state: Dictionary = {}
var task_state: Dictionary = {}

func to_dictionary() -> Dictionary:
	return {
		"frame_index": frame_index,
		"progress": progress,
		"generator_type": generator_type,
		"stimulus_state": stimulus_state.duplicate(true),
		"target_states": target_states.duplicate(true),
		"distractor_states": distractor_states.duplicate(true),
		"trajectory_state": trajectory_state.duplicate(true),
		"task_state": task_state.duplicate(true)
	}