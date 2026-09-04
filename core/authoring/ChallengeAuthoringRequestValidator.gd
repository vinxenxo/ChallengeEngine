class_name ChallengeAuthoringRequestValidator
extends RefCounted

const REGISTERED_MECHANICS = [
	"key", "parking", "pilot", "parking_v2", 
	"hit_v1", "catch_v1", "find_v1", "choose_v1", "count_v1"
]

static func validate(request: ChallengeAuthoringRequest) -> Array:
	var errors = []
	
	if not REGISTERED_MECHANICS.has(request.mechanic_id):
		errors.append("Mechanic '%s' is not registered in the system." % request.mechanic_id)
		
	if request.level < 1 or request.level > 100:
		errors.append("Level '%d' violates contractual bounds [1, 100]." % request.level)
		
	var profile = DifficultyProfileRegistry.get_profile(request.profile_id)
	if profile.is_empty():
		errors.append("Profile '%s' could not be loaded from registry." % request.profile_id)
	else:
		var profile_mech = profile.get("mechanic", "")
		if profile_mech != request.mechanic_id:
			errors.append("Profile/Mechanic mismatch: profile is for '%s' but request is for '%s'." % [profile_mech, request.mechanic_id])
			
		var challenge_mock = {
			"mechanic": request.mechanic_id,
			"difficulty": {
				"level": request.level,
				"overrides": request.get_overrides()
			}
		}
		var validation_errors = DifficultyProfileValidator.validate(challenge_mock, profile)
		for err in validation_errors:
			errors.append("Override validation error: " + err)
			
	return errors