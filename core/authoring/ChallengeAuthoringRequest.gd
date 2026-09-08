class_name ChallengeAuthoringRequest
extends RefCounted

var mechanic_id: String = ""
var level: int = 1
var seed: int = 0
var profile_id: String = ""
var _overrides: Dictionary = {}
var _content: Dictionary = {}

func _init(p_mechanic: String, p_level: int, p_seed: int, p_profile: String, p_overrides: Dictionary = {}, p_content: Dictionary = {}):
	mechanic_id = p_mechanic
	level = p_level
	seed = p_seed
	profile_id = p_profile
	_overrides = p_overrides.duplicate(true)
	_content = p_content.duplicate(true)

func get_overrides() -> Dictionary:
	return _overrides.duplicate(true)

func get_content() -> Dictionary:
	return _content.duplicate(true)

static func create_from_dictionary(data: Dictionary) -> Dictionary:
	var errors = []
	
	if not data.has("mechanic") or typeof(data["mechanic"]) != TYPE_STRING or data["mechanic"].strip_edges() == "":
		errors.append("Missing or invalid 'mechanic' field.")
	
	if not data.has("level") or (typeof(data["level"]) != TYPE_INT and typeof(data["level"]) != TYPE_FLOAT):
		errors.append("Missing or invalid 'level' field.")
	else:
		var lvl = int(data["level"])
		if lvl < 1 or lvl > 100:
			errors.append("Level '%d' out of bounds. Must be between 1 and 100." % lvl)
			
	if not data.has("seed") or (typeof(data["seed"]) != TYPE_INT and typeof(data["seed"]) != TYPE_FLOAT):
		errors.append("Missing or invalid 'seed' field.")
		
	if not data.has("profile") or typeof(data["profile"]) != TYPE_STRING or data["profile"].strip_edges() == "":
		errors.append("Missing or invalid 'profile' field.")
		
	var overrides = data.get("overrides", {})
	if typeof(overrides) != TYPE_DICTIONARY:
		errors.append("Field 'overrides' must be a Dictionary.")

	var content = data.get("content", {})
	if typeof(content) != TYPE_DICTIONARY:
		errors.append("Field 'content' must be a Dictionary.")
		
	if errors.size() > 0:
		return {
			"success": false,
			"errors": errors,
			"request": null
		}
		
	var req = ChallengeAuthoringRequest.new(
		str(data["mechanic"]),
		int(data["level"]),
		int(data["seed"]),
		str(data["profile"]),
		overrides,
		content
	)
	
	return {
		"success": true,
		"errors": [],
		"request": req
	}