class_name VisualLoopRuntime
extends ContentRuntime

## C6-F0.3.5 — Visual Loop runtime.
## Uses VisualLoopTimeline for temporal wrap semantics and emits logical frame state.
## No challenge semantics, score, winning frame, RNG, or rasterization.

const VisualLoopTimeline = preload("res://core/authoring/VisualLoopTimeline.gd")

var timeline: VisualLoopTimeline = null
var payload: Dictionary = {}

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
	var duration := float(payload["duration"])
	var expected_frames := int(round(duration * float(fps)))
	if expected_frames != int(payload["frame_count"]):
		return _fail("VISUAL_LOOP_FRAME_COUNT_MISMATCH")

	timeline = VisualLoopTimeline.new(duration, fps)
	var stream := RenderedFrameStream.new(kind, subtype, fps)
	for index in range(timeline.total_frames):
		var frame := {
			"frame_index": index,
			"payload": {
				"domain": "visual_loop",
				"loop_frame": index,
				"loop_iteration": 0,
				"generator": str(payload["visual_parameters"].get("generator", "")),
				"layers": (payload["visual_parameters"].get("layers", []) as Array).duplicate(true),
				"loop": payload.get("loop", {}).duplicate(true)
			}
		}
		if not stream.append_frame(frame):
			return _fail("VISUAL_LOOP_FRAME_STREAM_APPEND_FAILED")

	# The stream represents one declared loop pass. The timeline retains the
	# absolute cursor + wrapping semantics for consumers that progress over it.
	return _mark_initialized(stream)

func next_frame() -> Dictionary:
	var frame := super.next_frame()
	if frame.is_empty():
		return frame
	if timeline != null:
		var absolute_index := int(frame["frame_index"])
		frame["payload"]["loop_frame"] = timeline.get_loop_frame() if timeline.get_current_frame() == absolute_index else absolute_index
		frame["payload"]["loop_iteration"] = timeline.get_loop_iteration()
		timeline.advance()
	return frame
