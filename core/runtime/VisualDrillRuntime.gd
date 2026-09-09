class_name VisualDrillRuntime
extends ContentRuntime

## C6-F0.4.2 — Visual Drill Runtime Engine.
## Coordinates VisualDrillTimeline, generator resolution, and structured VisualDrillFrameState creation.

const VisualDrillTimeline = preload("res://core/authoring/VisualDrillTimeline.gd")
const VisualDrillGeneratorRegistry = preload("res://core/runtime/visual_drill/VisualDrillGeneratorRegistry.gd")
const VisualDrillFrameState = preload("res://core/runtime/visual_drill/VisualDrillFrameState.gd")

var timeline: VisualDrillTimeline = null
var payload: Dictionary = {}
var primary_subtype: String = ""

func _initialize_domain(definition: Dictionary) -> bool:
	if kind != "visual_drill":
		return _fail("VISUAL_DRILL_KIND_MISMATCH")
		
	primary_subtype = subtype
	var gen := VisualDrillGeneratorRegistry.get_generator(primary_subtype)
	if gen == null:
		return _fail("VISUAL_DRILL_UNKNOWN_SUBTYPE")
		
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
		var drill_state := gen.generate(index, timeline.total_frames, payload)
		
		var vdfs := VisualDrillFrameState.new()
		vdfs.frame_index = index
		vdfs.progress = progress
		vdfs.generator_type = primary_subtype
		vdfs.stimulus_state = drill_state.get("stimulus_state", {})
		vdfs.target_states = drill_state.get("target_states", [])
		vdfs.distractor_states = drill_state.get("distractor_states", [])
		vdfs.trajectory_state = drill_state.get("trajectory_state", {})
		vdfs.task_state = drill_state.get("task_state", {})
		
		var frame_payload: Dictionary = vdfs.to_dictionary()
		frame_payload["domain"] = "visual_drill"

		var frame := {
			"frame_index": index,
			"payload": frame_payload
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