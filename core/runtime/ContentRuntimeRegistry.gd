class_name ContentRuntimeRegistry
extends RefCounted

## C6-F0.3.5 — Exact polymorphic runtime routing.
## Contract:
##   - route key = exact (kind, subtype)
##   - no trimming / lowercasing / wildcard fallback
##   - runtime initialization is part of resolution
##   - failed initialization never leaks a runtime instance

const ChallengeRuntimeClass = preload("res://core/runtime/ChallengeRuntime.gd")
const VisualLoopRuntimeClass = preload("res://core/runtime/VisualLoopRuntime.gd")
const VisualDrillRuntimeClass = preload("res://core/runtime/VisualDrillRuntime.gd")

const KNOWN_CHALLENGE_SUBTYPES: Array[String] = [
	"key",
	"parking",
	"pilot",
	"parking_v2",
	"hit_v1",
	"catch_v1",
	"find_v1",
	"choose_v1",
	"count_v1"
]

const KNOWN_VISUAL_LOOP_SUBTYPES: Array[String] = [
	"fractal",
	"vector_field",
	"particle_flow",
	"kaleidoscope",
	"geometric"
]

const KNOWN_VISUAL_DRILL_SUBTYPES: Array[String] = [
	"tracking",
	"pursuit",
	"saccade",
	"peripheral_scan"
]

var _registry: Dictionary = {}


static func create_default() -> ContentRuntimeRegistry:
	var registry := ContentRuntimeRegistry.new()

	for subtype in KNOWN_CHALLENGE_SUBTYPES:
		var result: Dictionary = registry.register_runtime(
			"challenge",
			subtype,
			func(): return ChallengeRuntimeClass.new()
		)
		if not bool(result.get("success", false)):
			push_error("Failed to register Challenge route: %s" % str(result.get("error_code", "")))

	for subtype in KNOWN_VISUAL_LOOP_SUBTYPES:
		var result: Dictionary = registry.register_runtime(
			"visual_loop",
			subtype,
			func(): return VisualLoopRuntimeClass.new()
		)
		if not bool(result.get("success", false)):
			push_error("Failed to register Visual Loop route: %s" % str(result.get("error_code", "")))

	for subtype in KNOWN_VISUAL_DRILL_SUBTYPES:
		var result: Dictionary = registry.register_runtime(
			"visual_drill",
			subtype,
			func(): return VisualDrillRuntimeClass.new()
		)
		if not bool(result.get("success", false)):
			push_error("Failed to register Visual Drill route: %s" % str(result.get("error_code", "")))

	return registry


func register_runtime(kind: String, subtype: String, factory: Callable) -> Dictionary:
	# Exact routing only. Silent normalization is forbidden.
	if kind.is_empty() or subtype.is_empty():
		return _failure("ROUTE_KEY_INVALID")

	if kind.strip_edges() != kind or subtype.strip_edges() != subtype:
		return _failure("ROUTE_KEY_NON_CANONICAL")

	if not factory.is_valid():
		return _failure("ROUTE_FACTORY_INVALID")

	var key := _route_key(kind, subtype)
	if _registry.has(key):
		return _failure("ROUTE_DUPLICATE:%s" % key)

	_registry[key] = factory

	return {
		"success": true,
		"error_code": "",
		"route": {
			"kind": kind,
			"subtype": subtype
		}
	}


func has_route(kind: String, subtype: String) -> bool:
	if kind.strip_edges() != kind or subtype.strip_edges() != subtype:
		return false
	return _registry.has(_route_key(kind, subtype))


func resolve(definition: Dictionary) -> Dictionary:
	if definition.is_empty():
		return _failure("EMPTY_DEFINITION")

	if not definition.has("kind") or not definition.has("subtype"):
		return _failure("RUNTIME_ROUTING_METADATA_MISSING")

	if not definition["kind"] is String or not definition["subtype"] is String:
		return _failure("RUNTIME_ROUTING_METADATA_TYPE_INVALID")

	var kind: String = definition["kind"]
	var subtype: String = definition["subtype"]

	# Exact canonical routing: do not normalize caller input.
	if kind.is_empty() or subtype.is_empty():
		return _failure("RUNTIME_ROUTING_METADATA_EMPTY")

	if kind.strip_edges() != kind or subtype.strip_edges() != subtype:
		return _failure("RUNTIME_ROUTING_METADATA_NON_CANONICAL")

	var key := _route_key(kind, subtype)
	if not _registry.has(key):
		return _failure("RUNTIME_ROUTE_NOT_REGISTERED:%s" % key)

	var factory: Callable = _registry[key]
	if not factory.is_valid():
		return _failure("RUNTIME_ROUTE_FACTORY_INVALID:%s" % key)

	var runtime = factory.call()
	if runtime == null or not runtime is ContentRuntime:
		return _failure("RUNTIME_FACTORY_RETURN_INVALID:%s" % key)

	# Resolution includes initialization. A failed runtime must never leak.
	if not runtime.initialize(definition):
		var runtime_error: String = runtime.get_error()
		return _failure(
			"RUNTIME_INITIALIZATION_FAILED:%s" % runtime_error,
			{"kind": kind, "subtype": subtype}
		)

	return {
		"success": true,
		"error_code": "",
		"runtime": runtime,
		"route": {
			"kind": kind,
			"subtype": subtype
		}
	}


func registered_routes() -> Array[String]:
	var result: Array[String] = []
	for key in _registry.keys():
		result.append(str(key))
	result.sort()
	return result


func _route_key(kind: String, subtype: String) -> String:
	return "%s::%s" % [kind, subtype]


func _failure(error_code: String, route = null) -> Dictionary:
	return {
		"success": false,
		"error_code": error_code,
		"runtime": null,
		"route": route
	}
