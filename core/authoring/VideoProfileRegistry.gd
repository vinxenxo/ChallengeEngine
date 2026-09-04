class_name VideoProfileRegistry
extends RefCounted

static var _cache: Dictionary = {}

static func get_profile(profile_id: String) -> Dictionary:
	if _cache.has(profile_id):
		return _cache[profile_id]
		
	var path = "res://profiles/video/" + profile_id + ".json"
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
		# Se carga en caché de forma ciega; el validador actúa como firewall.
		_cache[profile_id] = data
		return data
		
	return {}

static func clear_cache() -> void:
	_cache.clear()