class_name VisualLoopRuntime
extends ContentRuntime

const VisualLoopTimeline = preload("res://core/authoring/VisualLoopTimeline.gd")
const VisualFrameStateClass = preload("res://core/runtime/visual/VisualFrameState.gd")
const VisualLoopGeneratorRegistryClass = preload("res://core/runtime/visual/VisualLoopGeneratorRegistry.gd")
const RNGStreamRegistryClass = preload("res://core/deterministic/RNGStreamRegistry.gd")
const CosmeticRNGClass = preload("res://core/deterministic/CosmeticRNG.gd")
const PresentationRNGContextClass = preload("res://core/deterministic/PresentationRNGContext.gd")

var timeline: VisualLoopTimeline = null
var payload: Dictionary = {}
var _generator_type: String = ""
var _generator = null
var _visual_parameters: Dictionary = {}
var _current_render_state: VisualFrameState = null

var _rng_context = null
var _active_stream_id: int = -1

func _initialize_domain(definition: Dictionary) -> bool:
	if kind != "visual_loop":
		return _fail("VISUAL_LOOP_KIND_MISMATCH")
		
	if definition.has("payload") and definition["payload"] is Dictionary:
		payload = definition["payload"].duplicate(true)
	elif definition.has("content") and definition["content"] is Dictionary:
		payload = definition["content"].duplicate(true)
	else:
		return _fail("VISUAL_LOOP_PAYLOAD_MISSING")

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

	# C6-F0.8-D2-B: Inicialización segura de RNG Cosmético
	if not _initialize_cosmetic_rng(definition):
		return false

	timeline = VisualLoopTimeline.new(duration, fps)
	var stream := RenderedFrameStream.new(kind, subtype, fps)

	for index in range(timeline.total_frames):
		var state: VisualFrameState = _build_render_state(index)
		
		# Abortar estrictamente si la generación de estado (incluyendo RNG) falló
		if state == null:
			_current_render_state = null
			return _fail("VISUAL_LOOP_RNG_SAMPLE_FAILED")
			
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

func _initialize_cosmetic_rng(definition: Dictionary) -> bool:
	_rng_context = null
	_active_stream_id = -1

	var stream_id: int = -1
	var consumer_id: String = ""

	match _generator_type:
		"fractal":
			stream_id = RNGStreamRegistryClass.STREAM_VISUAL_LOOP_FRACTAL
			consumer_id = "FractalGenerator"
		"vector_field":
			stream_id = RNGStreamRegistryClass.STREAM_VISUAL_LOOP_VECTOR_FIELD
			consumer_id = "VectorFieldGenerator"
		"particle_flow":
			stream_id = RNGStreamRegistryClass.STREAM_VISUAL_LOOP_PARTICLE_FLOW
			consumer_id = "ParticleFlowGenerator"
		"kaleidoscope":
			stream_id = RNGStreamRegistryClass.STREAM_VISUAL_LOOP_KALEIDOSCOPE
			consumer_id = "KaleidoscopeGenerator"
		"geometric":
			stream_id = RNGStreamRegistryClass.STREAM_VISUAL_LOOP_GEOMETRIC
			consumer_id = "GeometricGenerator"
		_:
			return true

	var seed_value: int = int(definition.get("seed", 0))
	var rng_version: String = str(definition.get("rng_version", "2.0"))

	var registry := RNGStreamRegistryClass.new()

	if not registry.is_registered(stream_id):
		return _fail("VISUAL_LOOP_RNG_STREAM_NOT_REGISTERED")

	if not registry.is_consumer_authorized(stream_id, consumer_id):
		return _fail("VISUAL_LOOP_RNG_CONSUMER_NOT_AUTHORIZED")

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
		return _fail("VISUAL_LOOP_RNG_CONTEXT_INVALID")

	_rng_context = creation.context
	_active_stream_id = stream_id

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

func _build_variation() -> Dictionary:
	if _rng_context == null or _active_stream_id == -1:
		return {}

	var variation := {
		"palette_variant": _rng_context.sample_float(_active_stream_id, 0),
		"complexity_variant": _rng_context.sample_float(_active_stream_id, 1),
		"phase_offset": _rng_context.sample_float(_active_stream_id, 2),
		"rotation_offset": _rng_context.sample_float(_active_stream_id, 3)
	}

	# Validación estricta D2-B: Si algún sample falló, la variación está corrupta.
	if _rng_context.error_state != "OK":
		return {"_failed": true}

	return variation

func _build_render_state(absolute_frame: int) -> VisualFrameState:
	var variation: Dictionary = _build_variation()
	
	# Propagación del fallo al generador del frame
	if variation.has("_failed"):
		return null
		
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

		layer_params["speed"] = float(
			layer_params.get("speed", _visual_parameters.get("speed", 1.0))
		)

		layer_params["complexity"] = int(
			layer_params.get("complexity", _visual_parameters.get("complexity", 1))
		)

		if _visual_parameters.has("blend_mode") and not layer_params.has("blend_mode"):
			layer_params["blend_mode"] = _visual_parameters["blend_mode"]

		state.layer_states.append(
			_generator.generate_with_variation(
				state.loop_frame,
				maxi(1, total_frames),
				layer_params,
				variation
			)
		)

	return state