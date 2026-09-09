class_name VisualLoopRuntime
extends ContentRuntime

const VisualLoopTimeline = preload("res://core/authoring/VisualLoopTimeline.gd")
const VisualFrameStateClass = preload("res://core/runtime/visual/VisualFrameState.gd")
const VisualLoopGeneratorRegistryClass = preload("res://core/runtime/visual/VisualLoopGeneratorRegistry.gd")

var timeline: VisualLoopTimeline = null
var payload: Dictionary = {}
var _generator_type: String = ""
var _generator = null
var _visual_parameters: Dictionary = {}
var _current_render_state: VisualFrameState = null

func _initialize_domain(definition: Dictionary) -> bool:
	if kind != "visual_loop":
		return _fail("VISUAL_LOOP_KIND_MISMATCH")
	if not definition.has("payload") or not definition["payload"] is Dictionary:
		return _fail("VISUAL_LOOP_PAYLOAD_MISSING")

	payload = definition["payload"].duplicate(true)

	if not payload.has("duration") or not payload.has("fps") or not payload.has("frame_count"):
		return _fail("VISUAL_LOOP_TEMPORAL_FIELDS_MISSING")
	if not payload.has("visual_parameters") or not payload["visual_parameters"] is Dictionary:
		return _fail("VISUAL_LOOP_PARAMETERS_MISSING")
	if int(payload["fps"]) <= 0 or int(payload["frame_count"]) <= 0:
		return _fail("VISUAL_LOOP_TEMPORAL_VALUES_INVALID")

	fps = int(payload["fps"])
	var duration: float = float(payload["duration"])
	var expected_frames: int = int(round(duration * float(fps)))
	if expected_frames != int(payload["frame_count"]):
		return _fail("VISUAL_LOOP_FRAME_COUNT_MISMATCH")

	_visual_parameters = payload["visual_parameters"].duplicate(true)
	_generator_type = str(_visual_parameters.get("generator", ""))
	if _generator_type.is_empty():
		return _fail("VISUAL_LOOP_GENERATOR_MISSING")

	_generator = VisualLoopGeneratorRegistryClass.get_generator(_generator_type)
	if _generator == null:
		return _fail("VISUAL_LOOP_GENERATOR_UNKNOWN")

	timeline = VisualLoopTimeline.new(duration, fps)
	var stream := RenderedFrameStream.new(kind, subtype, fps)

	for index in range(timeline.total_frames):
		var state: VisualFrameState = _build_render_state(index)
		var frame := {
			"frame_index": index,
			"payload": {
				"domain": "visual_loop",
				"loop_frame": state.loop_frame,
				"loop_iteration": state.loop_iteration,
				"generator": state.generator_type,
				"layers": state.layer_states.duplicate(true),
				"loop": payload.get("loop", {}).duplicate(true)
			}
		}
		if not stream.append_frame(frame):
			_current_render_state = null
			return _fail("VISUAL_LOOP_FRAME_STREAM_APPEND_FAILED")

	if not _mark_initialized(stream):
		return false

	_current_render_state = null
	return true

func next_frame() -> Dictionary:
	var frame: Dictionary = super.next_frame()
	if frame.is_empty():
		return frame

	var absolute_index: int = int(frame.get("frame_index", 0))
	_current_render_state = _build_render_state(absolute_index)
	if timeline != null:
		timeline.advance()
	return frame

func get_current_render_state() -> VisualFrameState:
	return _current_render_state

func _build_render_state(absolute_frame: int) -> VisualFrameState:
	var state: VisualFrameState = VisualFrameStateClass.new()
	state.frame_index = absolute_frame
	state.loop_frame = absolute_frame % maxi(1, total_frames)
	state.loop_iteration = int(floor(float(absolute_frame) / float(maxi(1, total_frames))))
	state.generator_type = _generator_type
	state.layer_states = []

	var layers: Array = _visual_parameters.get("layers", [])
	if layers.is_empty():
		layers = [{}]

	for layer_value in layers:
		var layer_params: Dictionary = {}
		if layer_value is Dictionary:
			layer_params = layer_value.duplicate(true)
		layer_params["speed"] = float(layer_params.get("speed", _visual_parameters.get("speed", 1.0)))
		layer_params["complexity"] = int(layer_params.get("complexity", _visual_parameters.get("complexity", 1)))
		if _visual_parameters.has("blend_mode") and not layer_params.has("blend_mode"):
			layer_params["blend_mode"] = _visual_parameters["blend_mode"]
		state.layer_states.append(_generator.generate(state.loop_frame, maxi(1, total_frames), layer_params))

	return state
