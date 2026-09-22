# res://core/presentation/rendering/VisualContentPlayer.gd
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
const PresentationUI = preload("res://core/presentation/PresentationUI.gd")
const PresentationProfile = preload("res://core/presentation/PresentationProfile.gd")
const SocialUIBinder = preload("res://core/presentation/SocialUIBinder.gd")
const C11CVisualEditorialLayer = preload("res://core/presentation/C11CVisualEditorialLayer.gd")
const UnifiedSocialFrameScene = preload("res://core/presentation/UnifiedSocialFrame.tscn")

const LOGICAL_SOCIAL_CANVAS_SIZE := Vector2(540.0, 960.0)
const PHYSICAL_SOCIAL_OUTPUT_SIZE := Vector2(720.0, 1280.0)
const PHYSICAL_SOCIAL_SCALE: float = PHYSICAL_SOCIAL_OUTPUT_SIZE.x / LOGICAL_SOCIAL_CANVAS_SIZE.x

@export var content_definition_path: String = ""

@onready var unified_social_frame: UnifiedSocialFrame = get_node_or_null("UnifiedSocialFrame") as UnifiedSocialFrame

var _runtime = null
var _renderer_host: ContentRendererHost = null
var _binder = null
var _stream = null
var _current_frame_index: int = 0
var _total_frames: int = 0
var is_ready_initialized: bool = false
var playback_finished: bool = false
var presentation_ui: PresentationUI
var social_ui_binder: SocialUIBinder
var presentation_profile: PresentationProfile
var qa_mode: bool = false
var qa_header_text: String = ""
var qa_footer_text: String = ""
var _definition_context: Dictionary = {}
var c11c_editorial_layer: C11CVisualEditorialLayer = null

func _ready() -> void:
	print("[VISUAL_CONTENT_PLAYER] Initializing playback host...")

	# C11-B.1 backward compatibility: legacy tests and callers may still
	# instantiate VisualContentPlayer.gd directly instead of the TSCN.
	if unified_social_frame == null:
		unified_social_frame = UnifiedSocialFrameScene.instantiate() as UnifiedSocialFrame
		if unified_social_frame != null:
			unified_social_frame.name = "UnifiedSocialFrame"
			add_child(unified_social_frame)

	if unified_social_frame == null:
		push_error("[VISUAL_CONTENT_PLAYER] UnifiedSocialFrame could not be mounted.")
		return
	
	_renderer_host = ContentRendererHost.new()
	_renderer_host.name = "ContentRendererHost"
	unified_social_frame.get_body_content_root().add_child(_renderer_host)
	
	var definition: Dictionary = _load_definition()
	_definition_context = definition.duplicate(true)
	if definition.is_empty():
		push_error("[VISUAL_CONTENT_PLAYER] Failed to load valid content definition.")
		return
		
	var registry: ContentRuntimeRegistry = ContentRuntimeRegistry.create_default()
	var resolution: Dictionary = registry.resolve(definition)
	
	if not bool(resolution.get("success", false)):
		push_error("[VISUAL_CONTENT_PLAYER] Runtime resolution failed: %s" % str(resolution.get("error_code", "")))
		return
		
	presentation_profile = _build_presentation_profile(definition)
	_configure_qa_overlay(definition)
	if str(definition.get("kind", "")) == "visual_drill":
		# C11-C physical social delivery: keep all logical coordinates in the
		# frozen 540x960 frame and scale the complete composition to 720x1280.
		scale = Vector2.ONE * PHYSICAL_SOCIAL_SCALE
	unified_social_frame.apply_profile(presentation_profile)
	var use_shared_social_editorial: bool = str(definition.get("kind", "")) == "visual_drill"
	presentation_ui = PresentationUI.new(unified_social_frame, presentation_profile.theme_name, presentation_profile, use_shared_social_editorial)
	social_ui_binder = SocialUIBinder.new(presentation_ui, presentation_profile)

	_runtime = resolution.get("runtime")
	_total_frames = int(_runtime.get_frame_count())
	
	_stream = _runtime.get_rendered_frame_stream()
	var binder_registry: PresentationBinderRegistry = PresentationBinderRegistry.create_default()
	var binder_res: Dictionary = binder_registry.resolve_stream(_stream)
	
	if not bool(binder_res.get("success", false)):
		push_error("[VISUAL_CONTENT_PLAYER] Presentation binder resolution failed.")
		return
		
	_binder = binder_res.get("binder")

	if _binder != null and _binder.has_method("set_definition_context"):
		_binder.set_definition_context(definition)

	if str(definition.get("kind", "")) == "visual_drill":
		c11c_editorial_layer = C11CVisualEditorialLayer.new()
		if c11c_editorial_layer == null:
			push_error("[VISUAL_CONTENT_PLAYER] Shared C11-C editorial layer could not be instantiated.")
			return
		if not c11c_editorial_layer.mount(unified_social_frame):
			push_error("[VISUAL_CONTENT_PLAYER] Shared C11-C editorial layer could not be mounted.")
			c11c_editorial_layer = null
			return

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
		
	var render_model: Dictionary = _binder.bind_frame(frame, presentation_profile, "GAME")
	render_model["editorial_frame_index"] = _current_frame_index
	render_model["editorial_frame_count"] = _total_frames
	render_model["editorial_seed"] = int(_definition_context.get("seed", 314159))
	if qa_mode:
		render_model["show_hook"] = true
		render_model["hook_text"] = qa_header_text
		render_model["show_badge"] = true
		render_model["badge_text"] = "C11 QA"
		render_model["cta_visible"] = true
		render_model["cta_main"] = qa_footer_text
		render_model["cta_sub"] = ""
	if social_ui_binder != null:
		social_ui_binder.bind_render_model(render_model)
	if c11c_editorial_layer != null:
		c11c_editorial_layer.apply_render_model(render_model)

	var domain_state: Dictionary = {}
	if _stream.kind == "visual_loop":
		domain_state = render_model.get("visual_frame_state", {})
	elif _stream.kind == "visual_drill":
		domain_state = render_model.get("visual_drill_frame_state", {})
		
	_renderer_host.forward_state(domain_state)
	_current_frame_index += 1

func _configure_qa_overlay(definition: Dictionary) -> void:
	qa_mode = false
	qa_header_text = ""
	qa_footer_text = ""
	for arg in OS.get_cmdline_user_args():
		if arg == "--qa-mode":
			qa_mode = true
		elif arg.begins_with("--qa-label="):
			qa_mode = true
			qa_header_text = arg.trim_prefix("--qa-label=").strip_edges()

	if not qa_mode:
		return

	var kind: String = str(definition.get("kind", "visual_content"))
	var subtype: String = str(definition.get("subtype", "unknown"))
	var seed_text: String = str(definition.get("seed", definition.get("generation", {}).get("seed", "?")))
	var rng: String = str(definition.get("rng_version", definition.get("generation", {}).get("rng_version", "?")))
	var payload: Dictionary = definition.get("payload", {})
	var fps: int = int(payload.get("fps", 30))
	var frame_count: int = int(payload.get("frame_count", 0))

	if qa_header_text.is_empty():
		qa_header_text = "QA · %s/%s · SEED %s" % [kind, subtype, seed_text]
	qa_footer_text = "TEST · RNG %s · %d FPS · %d FRAMES" % [rng, fps, frame_count]

func _build_presentation_profile(definition: Dictionary) -> PresentationProfile:
	var profile: PresentationProfile = PresentationProfile.new()
	var presentation = definition.get("presentation", {})
	if presentation is Dictionary:
		profile.profile_id = str(presentation.get("profile_id", PresentationProfile.DEFAULT_ID))
		profile.theme_name = str(presentation.get("theme", "default_c6"))
	return profile

func _load_definition() -> Dictionary:
	# 1. Check CLI arguments for --definition=<path>
	var target_file: String = ""
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
		var text: String = FileAccess.get_file_as_string(target_file)
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
