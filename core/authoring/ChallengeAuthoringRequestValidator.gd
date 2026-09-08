class_name ChallengeAuthoringRequestValidator
extends RefCounted

const AuthoringMechanicRegistry = preload("res://core/authoring/AuthoringMechanicRegistry.gd")
const DifficultyProfileRegistry = preload("res://core/authoring/DifficultyProfileRegistry.gd")
const DifficultyProfileValidator = preload("res://core/authoring/DifficultyProfileValidator.gd")

static func validate(request: ChallengeAuthoringRequest) -> Array:
	var errors: Array = []

	AuthoringMechanicRegistry.initialize_defaults()
	var adapter: AuthoringMechanicAdapter = AuthoringMechanicRegistry.get_adapter(request.mechanic_id)
	if adapter == null:
		errors.append("Mechanic '%s' is not registered in the authoring registry." % request.mechanic_id)

	if request.level < 1 or request.level > 100:
		errors.append("Level '%d' violates contractual bounds [1, 100]." % request.level)

	var profile: Dictionary = DifficultyProfileRegistry.get_profile(request.profile_id)
	if profile.is_empty():
		errors.append("Profile '%s' could not be loaded from registry." % request.profile_id)
	else:
		var profile_mech: String = str(profile.get("mechanic", ""))
		if profile_mech != request.mechanic_id:
			errors.append("Profile/Mechanic mismatch: profile is for '%s' but request is for '%s'." % [profile_mech, request.mechanic_id])

		var challenge_mock: Dictionary = {
			"mechanic": request.mechanic_id,
			"difficulty": {
				"level": request.level,
				"overrides": request.get_overrides()
			}
		}
		var difficulty_errors: Array = DifficultyProfileValidator.validate(challenge_mock, profile)
		for err in difficulty_errors:
			errors.append("Override validation error: " + str(err))

	return errors

