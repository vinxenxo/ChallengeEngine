# res://core/authoring/AssetFamilyRegistry.gd
class_name AssetFamilyRegistry
extends RefCounted

static var _cache: Dictionary = {}

static func get_family(family_id: String) -> Dictionary:
	if _cache.has(family_id):
		return _cache[family_id]
		
	var path = "res://profiles/assets/" + family_id + ".json"
	if not FileAccess.file_exists(path):
		return {}
		
	var file = FileAccess.open(path, FileAccess.READ)
	if not file:
		return {}
		
	var content = file.get_as_text()
	file.close()
	
	var json = JSON.new()
	if json.parse(content) != OK:
		return {}
		
	var data = json.get_data()
	if typeof(data) == TYPE_DICTIONARY:
		_cache[family_id] = data
		return data
		
	return {}

static func clear_cache() -> void:
	_cache.clear()