class_name VisualDrillRuntime
extends ContentRuntime

## C6-F0.3.5 — Visual Drill runtime.
## No phase model is introduced. It emits only schema-defined exercise state
## plus monotonic frame/progress information required for rendering.

const VisualDrillTimeline = preload("res://core/authoring/VisualDrillTimeline.gd")

var timeline: VisualDrillTimeline = null
var payload: Dictionary = {}

func _initialize_domain(definition: Dictionary) -> bool:
	if kind != "visual_drill":
		return _fail("VISUAL_DRILL_KIND_MISMATCH")
	if not definition.has("payload") or not definition["payload"] is Dictionary:
		return _fail("VISUAL_DRILL_PAYLOAD_MISSING")

	payload = definition["payload"].duplicate(true)
	for required in ["duration", "fps", "frame_count", "exercise_parameters", "stimulus", "targets", "distractors", "trajectory", "task"]:
		if not payload.has(required):
			return _fail("VISUAL_DRILL_FIELD_MISSING_%s" % str(required).to_upper())
	if int(payload["fps"]) <= 0 or int(payload["frame_count"]) <= 0:
		return _fail("VISUAL_DRILL_TEMPORAL_VALUES_INVALID")

	fps = int(payload["fps"])
	var duration := float(payload["duration"])
	var expected_frames := int(round(duration * float(fps)))
	if expected_frames != int(payload["frame_count"]):
		return _fail("VISUAL_DRILL_FRAME_COUNT_MISMATCH")

	timeline = VisualDrillTimeline.new(duration, fps)
	var stream := RenderedFrameStream.new(kind, subtype, fps)
	for index in range(timeline.total_frames):
		var progress := float(index) / float(maxi(1, timeline.total_frames - 1))
		var frame := {
			"frame_index": index,
			"payload": {
				"domain": "visual_drill",
				"progress": progress,
				"exercise_parameters": payload["exercise_parameters"].duplicate(true),
				"stimulus": payload["stimulus"].duplicate(true),
				"targets": payload["targets"].duplicate(true),
				"distractors": payload["distractors"].duplicate(true),
				"trajectory": payload["trajectory"].duplicate(true),
				"task": payload["task"].duplicate(true)
			}
		}
		if not stream.append_frame(frame):
			return _fail("VISUAL_DRILL_FRAME_STREAM_APPEND_FAILED")

	return _mark_initialized(stream)

func next_frame() -> Dictionary:
	var frame := super.next_frame()
	if frame.is_empty():
		return frame
	if timeline != null:
		timeline.advance()
	return frame
