# res://core/presentation/PresentationBinderRegistry.gd
class_name PresentationBinderRegistry
extends RefCounted

## C6-F0.5 — Polymorphic Presentation Binder Registry.
## Enforces strict fail-closed routing based on the authoritative RenderedFrameStream (kind, subtype).
## Does NOT normalize strings, use wildcards, or read from frame payload domains.

const RenderedFrameStream = preload("res://core/runtime/RenderedFrameStream.gd")

var _registry: Dictionary = {}

func register_binder(kind: String, subtype: String, factory: Callable) -> Dictionary:
	if kind.is_empty() or subtype.is_empty():
		return {"success": false, "error_code": "BINDER_ROUTE_EMPTY"}
		
	var key := kind + ":" + subtype # Strict match, no strip_edges()
	if _registry.has(key):
		return {"success": false, "error_code": "BINDER_DUPLICATE"}
		
	if not factory.is_valid():
		return {"success": false, "error_code": "BINDER_FACTORY_INVALID"}
		
	_registry[key] = factory
	return {"success": true, "error_code": "", "route": key}

func resolve_stream(stream: RenderedFrameStream) -> Dictionary:
	if stream == null:
		return {"success": false, "error_code": "STREAM_NULL", "binder": null}
		
	var kind: String = stream.kind
	var subtype: String = stream.subtype
	
	if kind.is_empty() or subtype.is_empty():
		return {"success": false, "error_code": "MISSING_KIND_OR_SUBTYPE", "binder": null}
		
	var key := kind + ":" + subtype
	if not _registry.has(key):
		return {"success": false, "error_code": "BINDER_NOT_FOUND", "binder": null}
		
	var factory: Callable = _registry[key]
	if not factory.is_valid():
		return {"success": false, "error_code": "INVALID_FACTORY", "binder": null}
		
	var binder = factory.call()
	return {"success": true, "error_code": "", "binder": binder}

static func create_default() -> PresentationBinderRegistry:
	var registry := PresentationBinderRegistry.new()
	
	# Visual Loop Binders
	var loop_subtypes = ["fractal", "vector_field", "particle_flow", "kaleidoscope", "geometric"]
	for subtype in loop_subtypes:
		registry.register_binder("visual_loop", subtype, func(): return VisualLoopPresentationBinder.new())
		
	# Visual Drill Binders
	var drill_subtypes = ["tracking", "pursuit", "saccade", "peripheral_scan"]
	for subtype in drill_subtypes:
		registry.register_binder("visual_drill", subtype, func(): return VisualDrillPresentationBinder.new())
		
	# ChallengePresentationBinder remains untouched and is handled via its historical static pipeline for now.
	return registry