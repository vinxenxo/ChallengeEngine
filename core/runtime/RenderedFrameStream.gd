# res://core/runtime/RenderedFrameStream.gd
class_name RenderedFrameStream
extends RefCounted

## C6-F0.3.5 — Logical/render-ready frame stream.
## Contains ordered frame state only. It never stores rasterized pixels or encoded video.

var kind: String = ""
var subtype: String = ""
var fps: int = 0
var _frames: Array[Dictionary] = []

func _init(p_kind: String, p_subtype: String, p_fps: int) -> void:
	kind = p_kind
	subtype = p_subtype
	fps = p_fps

func append_frame(frame: Dictionary) -> bool:
	if frame == null or not frame is Dictionary:
		return false
	if not frame.has("frame_index"):
		return false
	if int(frame["frame_index"]) != _frames.size():
		return false
	_frames.append(frame.duplicate(true))
	return true

func total_frames() -> int:
	return _frames.size()

func get_frame(index: int) -> Dictionary:
	if index < 0 or index >= _frames.size():
		return {}
	return _frames[index].duplicate(true)

func get_frames() -> Array[Dictionary]:
	var result: Array[Dictionary] = []
	for frame in _frames:
		result.append(frame.duplicate(true))
	return result

func validate_contract() -> Dictionary:
	var errors: Array[String] = []
	if kind.strip_edges().is_empty():
		errors.append("Frame stream kind is empty.")
	if subtype.strip_edges().is_empty():
		errors.append("Frame stream subtype is empty.")
	if fps <= 0:
		errors.append("Frame stream fps must be > 0.")
	for index in range(_frames.size()):
		var frame := _frames[index]
		if not frame.has("frame_index") or int(frame["frame_index"]) != index:
			errors.append("Frame index contract violation at position %d." % index)
		if not frame.has("payload"):
			errors.append("Frame %d is missing opaque payload." % index)
	return {"is_valid": errors.is_empty(), "errors": errors}
