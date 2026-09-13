# res://core/authoring/VideoProfileValidator.gd
class_name VideoProfileValidator
extends RefCounted

const ALLOWED_ROOT_KEYS = ["profile_id", "fps", "phases"]
const ALLOWED_PHASE_KEYS = ["hook_duration", "game_duration", "reveal_duration", "cta_duration"]

static func validate(profile: Dictionary) -> Array:
	var errors = []
	
	# 1. Strict Root Key Check
	for k in profile:
		if not ALLOWED_ROOT_KEYS.has(k):
			errors.append("Unknown root field: '%s'" % str(k))
			
	if not profile.has("profile_id") or typeof(profile["profile_id"]) != TYPE_STRING or profile["profile_id"].strip_edges() == "":
		errors.append("Missing or invalid 'profile_id'")
		
	if not profile.has("fps") or (typeof(profile["fps"]) != TYPE_INT and typeof(profile["fps"]) != TYPE_FLOAT) or int(profile["fps"]) <= 0:
		errors.append("'fps' must be an integer > 0")
		
	if not profile.has("phases") or typeof(profile["phases"]) != TYPE_DICTIONARY:
		errors.append("Missing or invalid 'phases' dictionary")
		return errors
		
	var phases = profile["phases"]
	var total_duration = 0.0
	
	# 2. Strict Phase Key Check
	for k in phases:
		if not ALLOWED_PHASE_KEYS.has(k):
			errors.append("Unknown phase field: '%s'" % str(k))
			
	# 3. Game Duration (Mandatory > 0)
	var game = phases.get("game_duration", 0.0)
	if (typeof(game) != TYPE_FLOAT and typeof(game) != TYPE_INT) or float(game) <= 0.0:
		errors.append("'game_duration' must be a number > 0")
	else:
		total_duration += float(game)
		
	# 4. Optional Phases (Allowed to be 0, but must be >= 0)
	var optionals = ["hook_duration", "reveal_duration", "cta_duration"]
	for opt in optionals:
		if phases.has(opt):
			var val = phases[opt]
			if (typeof(val) != TYPE_FLOAT and typeof(val) != TYPE_INT) or float(val) < 0.0:
				errors.append("'%s' must be a number >= 0" % opt)
			else:
				total_duration += float(val)
		
	# 5. Sanity Check Total
	if total_duration <= 0.0:
		errors.append("Total duration must be > 0")
		
	return errors