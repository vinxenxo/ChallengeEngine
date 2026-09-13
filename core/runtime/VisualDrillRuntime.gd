# res://core/runtime/VisualDrillRuntime.gd
class_name VisualDrillRuntime
extends ContentRuntime

## Visual Drill Runtime Engine.
## Coordinates VisualDrillTimeline, generator resolution, and structured VisualDrillFrameState creation with RNG Streams (2011-2014).

const VisualDrillTimeline = preload("res://core/authoring/VisualDrillTimeline.gd")
const VisualDrillGeneratorRegistry = preload("res://core/runtime/visual_drill/VisualDrillGeneratorRegistry.gd")
const VisualDrillFrameState = preload("res://core/runtime/visual_drill/VisualDrillFrameState.gd")
const RNGStreamRegistryClass = preload("res://core/deterministic/RNGStreamRegistry.gd")
const CosmeticRNGClass = preload("res://core/deterministic/CosmeticRNG.gd")
const PresentationRNGContextClass = preload("res://core/deterministic/PresentationRNGContext.gd")

var timeline: VisualDrillTimeline = null
var payload: Dictionary = {}
var primary_subtype: String = ""

var _rng_context = null
var _active_stream_id: int = -1

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

	if not _initialize_cosmetic_rng(definition):
		return false

	timeline = VisualDrillTimeline.new(duration, fps)
	var stream := RenderedFrameStream.new(kind, subtype, fps)
	
	for index in range(timeline.total_frames):
		var variation: Dictionary = _build_variation()
		if variation.has("_failed"):
			return _fail("VISUAL_DRILL_RNG_SAMPLE_FAILED")

		var progress := float(index) / float(maxi(1, timeline.total_frames - 1))
		var drill_state: Dictionary = gen.generate_with_variation(index, timeline.total_frames, payload, variation)
		
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
		if drill_state.has("parameters"):
			frame_payload["parameters"] = drill_state["parameters"].duplicate(true)

		var frame := {
			"frame_index": index,
			"payload": frame_payload
		}

		if not stream.append_frame(frame):
			return _fail("VISUAL_DRILL_FRAME_STREAM_APPEND_FAILED")

	return _mark_initialized(stream)

func _initialize_cosmetic_rng(definition: Dictionary) -> bool:
	_rng_context = null
	_active_stream_id = -1

	var stream_id: int = -1
	var consumer_id: String = ""

	match primary_subtype:
		"tracking":
			stream_id = RNGStreamRegistryClass.STREAM_VISUAL_DRILL_TRACKING
			consumer_id = "TrackingGenerator"
		"pursuit":
			stream_id = RNGStreamRegistryClass.STREAM_VISUAL_DRILL_PURSUIT
			consumer_id = "PursuitGenerator"
		"saccade":
			stream_id = RNGStreamRegistryClass.STREAM_VISUAL_DRILL_SACCADE
			consumer_id = "SaccadeGenerator"
		"peripheral_scan":
			stream_id = RNGStreamRegistryClass.STREAM_VISUAL_DRILL_PERIPHERAL_SCAN
			consumer_id = "PeripheralScanGenerator"
		_:
			return true

	var seed_value: int = int(definition.get("seed", 0))
	var rng_version: String = str(definition.get("rng_version", "2.0"))

	var registry := RNGStreamRegistryClass.new()

	if not registry.is_registered(stream_id):
		return _fail("VISUAL_DRILL_RNG_STREAM_NOT_REGISTERED")

	if not registry.is_consumer_authorized(stream_id, consumer_id):
		return _fail("VISUAL_DRILL_RNG_CONSUMER_NOT_AUTHORIZED")

	var cosmetic_rng := CosmeticRNGClass.new(registry)
	var streams: Array[int] = [stream_id]

	var creation := PresentationRNGContextClass.create(
		seed_value,
		rng_version,
		consumer_id,
		streams,
		cosmetic_rng,
		registry
	)

	if not creation.is_valid:
		return _fail("VISUAL_DRILL_RNG_CONTEXT_INVALID")

	_rng_context = creation.context
	_active_stream_id = stream_id

	return true

func _build_variation() -> Dictionary:
	if _rng_context == null or _active_stream_id == -1:
		return {}

	var variation := {}

	match primary_subtype:
		"tracking":
			variation["tracking_variant"] = _rng_context.sample_float(_active_stream_id, 0)
		"pursuit":
			variation["pursuit_variant"] = _rng_context.sample_float(_active_stream_id, 0)
		"saccade":
			variation["saccade_variant"] = _rng_context.sample_float(_active_stream_id, 0)
		"peripheral_scan":
			variation["pattern_variant"] = _rng_context.sample_float(_active_stream_id, 0)
			variation["amplitude_variant"] = _rng_context.sample_float(_active_stream_id, 1)
		_:
			pass

	if _rng_context.error_state != "OK":
		return {"_failed": true}

	return variation

func next_frame() -> Dictionary:
	var frame := super.next_frame()
	if frame.is_empty():
		return frame
	if timeline != null:
		timeline.advance()
	return frame