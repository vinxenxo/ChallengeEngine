# res://core/runtime/ContentRuntime.gd
class_name ContentRuntime
extends RefCounted

## C6-F0.3.5 — Common runtime boundary.
## Domain-agnostic lifecycle and render-ready frame stream contract.
## This class must remain independent of domain simulation, RNG, UI, and export internals.

var kind: String = ""
var subtype: String = ""
var fps: int = 0
var total_frames: int = 0
var _current_frame: int = 0
var _initialized: bool = false
var _error: String = ""
var _stream: RenderedFrameStream = null

func initialize(definition: Dictionary) -> bool:
	_error = ""
	_initialized = false
	_current_frame = 0
	_stream = null

	if definition == null or not definition is Dictionary:
		return _fail("RUNTIME_DEFINITION_INVALID")
	if not definition.has("kind") or not definition.has("subtype"):
		return _fail("RUNTIME_ROUTING_METADATA_MISSING")
	if not definition["kind"] is String or str(definition["kind"]).strip_edges().is_empty():
		return _fail("RUNTIME_KIND_INVALID")
	if not definition["subtype"] is String or str(definition["subtype"]).strip_edges().is_empty():
		return _fail("RUNTIME_SUBTYPE_INVALID")

	kind = str(definition["kind"])
	subtype = str(definition["subtype"])
	return _initialize_domain(definition)

func _initialize_domain(_definition: Dictionary) -> bool:
	return _fail("RUNTIME_INITIALIZATION_NOT_IMPLEMENTED")

func is_initialized() -> bool:
	return _initialized

func get_error() -> String:
	return _error

func get_current_frame() -> int:
	return _current_frame

func is_finished() -> bool:
	return _initialized and _current_frame >= total_frames

func get_frame_count() -> int:
	return total_frames

func get_fps() -> int:
	return fps

func get_rendered_frame_stream() -> RenderedFrameStream:
	return _stream

func next_frame() -> Dictionary:
	if not _initialized:
		return {}
	if is_finished():
		return {}
	var frame: Dictionary = _stream.get_frame(_current_frame)
	_current_frame += 1
	return frame

func _mark_initialized(frame_stream: RenderedFrameStream) -> bool:
	if frame_stream == null:
		return _fail("RUNTIME_FRAME_STREAM_NULL")
	if frame_stream.total_frames() <= 0:
		return _fail("RUNTIME_FRAME_STREAM_EMPTY")
	_stream = frame_stream
	total_frames = frame_stream.total_frames()
	_current_frame = 0
	_initialized = true
	return true

func _fail(code: String) -> bool:
	_error = code
	_initialized = false
	return false
