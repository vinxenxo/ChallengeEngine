class_name AudioProfileRegistry
extends RefCounted

static var _cache: Dictionary = {}

static func get_profile(profile_id: String) -> Dictionary:
	if _cache.has(profile_id):
		return _cache[profile_id]
		
	var path = "res://profiles/audio/" + profile_id + ".json"
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
	if typeof(data) != TYPE_DICTIONARY:
		return {}
		
	# Identity validation
	if not data.has("profile_id") or typeof(data["profile_id"]) != TYPE_STRING or data["profile_id"] != profile_id:
		return {}
		
	_cache[profile_id] = data
	return data

static func clear_cache() -> void:
	_cache.clear()