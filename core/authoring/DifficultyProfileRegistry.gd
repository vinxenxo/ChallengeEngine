class_name DifficultyProfileRegistry
extends RefCounted

## C6-F2.1 — Deterministic, read-only profile lookup.
## Profiles are authoring data. The registry does not mutate them.

static var _cache: Dictionary = {}

static func get_profile(profile_id: String) -> Dictionary:
	if profile_id.is_empty():
		return {}
	if _cache.has(profile_id):
		return _cache[profile_id]

	var path: String = "res://profiles/difficulty/%s.json" % profile_id
	if not FileAccess.file_exists(path):
		return {}

	var file: FileAccess = FileAccess.open(path, FileAccess.READ)
	if file == null:
		return {}
	var text: String = file.get_as_text()
	file.close()

	var parsed: Variant = JSON.parse_string(text)
	if parsed is Dictionary:
		var profile: Dictionary = parsed
		_cache[profile_id] = profile
		return profile

	return {}

static func clear_cache() -> void:
	_cache.clear()
