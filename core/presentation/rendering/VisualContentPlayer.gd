class_name VisualContentPlayer
extends Node2D

## C6-F0.6 — Visual Content Player Composition Root.
## Agnostic playback host for Visual Loop and Visual Drill runtimes.
## Supports content definition loading via export path, command line --definition argument,
## or canonical fallbacks for zero-config execution.

const ContentRuntimeRegistry = preload("res://core/runtime/ContentRuntimeRegistry.gd")
const PresentationBinderRegistry = preload("res://core/presentation/PresentationBinderRegistry.gd")
const ContentRendererHost = preload("res://core/presentation/rendering/ContentRendererHost.gd")
const VisualLoopRenderer = preload("res://core/presentation/rendering/VisualLoopRenderer.gd")
const VisualDrillRenderer = preload("res://core/presentation/rendering/VisualDrillRenderer.gd")

@export var content_definition_path: String = ""

var _runtime = null
var _renderer_host: ContentRendererHost = null
var _binder = null
var _stream = null
var _current_frame_index: int = 0
var _total_frames: int = 0
var is_ready_initialized: bool = false
var playback_finished: bool = false

func _ready() -> void:
	print("[VISUAL_CONTENT_PLAYER] Initializing playback host...")
	
	_renderer_host = ContentRendererHost.new()
	add_child(_renderer_host)
	
	var definition: Dictionary = _load_definition()
	if definition.is_empty():
		push_error("[VISUAL_CONTENT_PLAYER] Failed to load valid content definition.")
		return
		
	var registry := ContentRuntimeRegistry.create_default()
	var resolution: Dictionary = registry.resolve(definition)
	
	if not bool(resolution.get("success", false)):
		push_error("[VISUAL_CONTENT_PLAYER] Runtime resolution failed: %s" % str(resolution.get("error_code", "")))
		return
		
	_runtime = resolution.get("runtime")
	_total_frames = int(_runtime.get_frame_count())
	
	_stream = _runtime.get_rendered_frame_stream()
	var binder_registry := PresentationBinderRegistry.create_default()
	var binder_res: Dictionary = binder_registry.resolve_stream(_stream)
	
	if not bool(binder_res.get("success", false)):
		push_error("[VISUAL_CONTENT_PLAYER] Presentation binder resolution failed.")
		return
		
	_binder = binder_res.get("binder")
	
	if _stream.kind == "visual_loop":
		_renderer_host.mount_renderer(VisualLoopRenderer.new())
	elif _stream.kind == "visual_drill":
		_renderer_host.mount_renderer(VisualDrillRenderer.new())
	else:
		push_error("[VISUAL_CONTENT_PLAYER] Unsupported stream kind for visual player: %s" % _stream.kind)
		return
		
	is_ready_initialized = true
	print("[VISUAL_CONTENT_PLAYER] Ready [%s/%s]. Starting playback for %d frames." % [_stream.kind, _stream.subtype, _total_frames])
	set_process(true)

func _process(_delta: float) -> void:
	if _runtime == null or _runtime.is_finished():
		if not playback_finished:
			playback_finished = true
			print("[VISUAL_CONTENT_PLAYER] Playback finished. Awaiting Movie Maker completion.")
		return
		
	var frame: Dictionary = _runtime.next_frame()
	if frame.is_empty():
		return
		
	var render_model: Dictionary = _binder.bind_frame(frame, null, "GAME")
	
	var domain_state: Dictionary = {}
	if _stream.kind == "visual_loop":
		domain_state = render_model.get("visual_frame_state", {})
	elif _stream.kind == "visual_drill":
		domain_state = render_model.get("visual_drill_frame_state", {})
		
	_renderer_host.forward_state(domain_state)
	_current_frame_index += 1

func _load_definition() -> Dictionary:
	# 1. Check CLI arguments for --definition=<path>
	var target_file := ""
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--definition="):
			target_file = arg.trim_prefix("--definition=")
			break
	if target_file.is_empty():
		for arg in OS.get_cmdline_args():
			if arg.begins_with("--definition="):
				target_file = arg.trim_prefix("--definition=")
				break
				
	# 2. Fallback to @export var path
	if target_file.is_empty():
		target_file = content_definition_path
		
	# Load file if resolved
	if not target_file.is_empty() and FileAccess.file_exists(target_file):
		var text := FileAccess.get_file_as_string(target_file)
		var parsed = JSON.parse_string(text)
		if parsed is Dictionary:
			print("[VISUAL_CONTENT_PLAYER] Loaded definition from path: %s" % target_file)
			return parsed
			
	# Default fallback definition (visual_loop/fractal)
	return {
		"kind": "visual_loop",
		"subtype": "fractal",
		"payload": {
			"duration": 2.0,
			"fps": 30,
			"frame_count": 60,
			"loop": {
				"seamless": true,
				"boundary_tolerance": 0.01
			},
			"visual_parameters": {
				"generator": "fractal",
				"layers": [
					{
						"blend_mode": "normal",
						"speed": 1.0,
						"complexity": 2
					}
				]
			}
		}
	}
