class_name ContentRuntimeRegistry
extends RefCounted

## C6-F0.3.5 — Exact runtime routing registry.
## Routing key is strictly (kind, subtype). Unknown combinations fail closed.
## Visual subtype registration is explicit because the frozen schema intentionally
## leaves subtype open-ended; this registry must not invent a wildcard fallback.

const KNOWN_CHALLENGE_SUBTYPES := [
	"key", "parking", "pilot", "parking_v2", "hit_v1", "catch_v1",
	"find_v1", "choose_v1", "count_v1"
]

var _routes: Dictionary = {}

static func create_default() -> ContentRuntimeRegistry:
	var registry := ContentRuntimeRegistry.new()
	for subtype in KNOWN_CHALLENGE_SUBTYPES:
		registry.register_runtime("challenge", subtype, func(): return ChallengeRuntime.new())
	return registry

func register_runtime(kind: String, subtype: String, factory: Callable) -> Dictionary:
	var normalized_kind := kind.strip_edges()
	var normalized_subtype := subtype.strip_edges()
	if normalized_kind.is_empty() or normalized_subtype.is_empty():
		return {"success": false, "error_code": "ROUTE_KEY_INVALID"}
	if not factory.is_valid():
		return {"success": false, "error_code": "ROUTE_FACTORY_INVALID"}
	var key := _route_key(normalized_kind, normalized_subtype)
	if _routes.has(key):
		return {"success": false, "error_code": "ROUTE_DUPLICATE"}
	_routes[key] = factory
	return {"success": true, "error_code": ""}

func has_route(kind: String, subtype: String) -> bool:
	return _routes.has(_route_key(kind.strip_edges(), subtype.strip_edges()))

func resolve(definition: Dictionary) -> Dictionary:
	if definition == null or not definition is Dictionary:
		return _failure("RUNTIME_DEFINITION_INVALID")
	if not definition.has("kind") or not definition.has("subtype"):
		return _failure("RUNTIME_ROUTING_METADATA_MISSING")
	if not definition["kind"] is String or not definition["subtype"] is String:
		return _failure("RUNTIME_ROUTING_METADATA_TYPE_INVALID")

	var kind := str(definition["kind"]).strip_edges()
	var subtype := str(definition["subtype"]).strip_edges()
	if kind.is_empty() or subtype.is_empty():
		return _failure("RUNTIME_ROUTING_METADATA_EMPTY")

	var key := _route_key(kind, subtype)
	if not _routes.has(key):
		return _failure("RUNTIME_ROUTE_NOT_REGISTERED:%s" % key)

	var factory: Callable = _routes[key]
	if not factory.is_valid():
		return _failure("RUNTIME_ROUTE_FACTORY_INVALID:%s" % key)
	var runtime = factory.call()
	if runtime == null or not runtime is ContentRuntime:
		return _failure("RUNTIME_FACTORY_RETURN_INVALID:%s" % key)
	if not runtime.initialize(definition):
		return _failure("RUNTIME_INITIALIZATION_FAILED:%s" % runtime.get_error(), runtime)
	return {
		"success": true,
		"error_code": "",
		"runtime": runtime,
		"route": {"kind": kind, "subtype": subtype}
	}

func registered_routes() -> Array[String]:
	var result: Array[String] = []
	for key in _routes.keys():
		result.append(str(key))
	result.sort()
	return result

func _route_key(kind: String, subtype: String) -> String:
	return "%s::%s" % [kind, subtype]

func _failure(error_code: String, runtime = null) -> Dictionary:
	var result := {
		"success": false,
		"error_code": error_code,
		"runtime": runtime,
		"route": null
	}
	return result
