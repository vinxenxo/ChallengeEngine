# res://core/authoring/AuthoringMechanicRegistry.gd
class_name AuthoringMechanicRegistry
extends RefCounted

static var _adapters: Dictionary = {}

static func register_adapter(adapter: AuthoringMechanicAdapter) -> void:
	_adapters[adapter.mechanic_id()] = adapter

static func get_adapter(mechanic_id: String) -> AuthoringMechanicAdapter:
	return _adapters.get(mechanic_id, null)

static func is_registered(mechanic_id: String) -> bool:
	return _adapters.has(mechanic_id)

static func initialize_defaults() -> void:
	if _adapters.is_empty():
		register_adapter(load("res://core/authoring/adapters/PilotAuthoringAdapter.gd").new())
		register_adapter(load("res://core/authoring/adapters/HitAuthoringAdapter.gd").new())
		register_adapter(load("res://core/authoring/adapters/CatchAuthoringAdapter.gd").new())
		register_adapter(load("res://core/authoring/adapters/FindAuthoringAdapter.gd").new())
		register_adapter(load("res://core/authoring/adapters/ChooseAuthoringAdapter.gd").new())
		register_adapter(load("res://core/authoring/adapters/CountAuthoringAdapter.gd").new())

static func clear_registry() -> void:
	_adapters.clear()