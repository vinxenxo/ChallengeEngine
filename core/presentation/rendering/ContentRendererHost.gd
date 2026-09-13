# res://core/presentation/rendering/ContentRendererHost.gd
class_name ContentRendererHost
extends Node2D

## C6-F0.5 Step 2 — Content Renderer Host.
## Pure agnostic container. It does NOT route, decide domains, or preload them.
## It only mounts an externally resolved renderer and forwards logical state to it.

var _current_renderer: Node2D = null

func mount_renderer(renderer: Node2D) -> void:
	if _current_renderer != null:
		remove_child(_current_renderer)
		_current_renderer.queue_free()
		_current_renderer = null
		
	_current_renderer = renderer
	if _current_renderer != null:
		add_child(_current_renderer)

func forward_state(payload: Dictionary) -> void:
	if _current_renderer != null and _current_renderer.has_method("apply_state"):
		_current_renderer.apply_state(payload)