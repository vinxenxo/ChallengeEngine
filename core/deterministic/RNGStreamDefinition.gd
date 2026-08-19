class_name RNGStreamDefinition
extends RefCounted

var _id: int
var _name: String
var _domain: int
var _owner: String
var _index_semantics: String
var _version_introduced: String
var _allowed_consumers: Array[String]

func _init(p_id: int, p_name: String, p_domain: int, p_owner: String, p_semantics: String, p_version: String, p_consumers: Array[String]) -> void:
	_id = p_id
	_name = p_name
	_domain = p_domain
	_owner = p_owner
	_index_semantics = p_semantics
	_version_introduced = p_version
	_allowed_consumers = p_consumers.duplicate()

func get_id() -> int:
	return _id

func get_name() -> String:
	return _name

func get_domain() -> int:
	return _domain

func get_owner() -> String:
	return _owner

func get_index_semantics() -> String:
	return _index_semantics

func get_version_introduced() -> String:
	return _version_introduced

func get_allowed_consumers() -> Array[String]:
	return _allowed_consumers.duplicate()
