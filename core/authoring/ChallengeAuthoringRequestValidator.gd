class_name ChallengeAuthoringRequestValidator
extends RefCounted

const AuthoringMechanicRegistry = preload("res://core/authoring/AuthoringMechanicRegistry.gd")
const DifficultyProfileRegistry = preload("res://core/authoring/DifficultyProfileRegistry.gd")
const DifficultyProfileValidator = preload("res://core/authoring/DifficultyProfileValidator.gd")

static func validate(request: ChallengeAuthoringRequest) -> Array:
	var errors = []
	
	AuthoringMechanicRegistry.initialize_defaults()
	var adapter = AuthoringMechanicRegistry.get_adapter(request.mechanic_id)
	if adapter == null:
		errors.append("Mechanic '%s' is not registered in the system." % request.mechanic_id)
		
	# Resolución de límites de nivel dinámicos basados en el perfil o contrato estándar [1, 100]
	var min_level = 1
	var max_level = 100
	
	var profile = DifficultyProfileRegistry.get_profile(request.profile_id)
	if profile.is_empty():
		errors.append("Profile '%s' could not be loaded from registry." % request.profile_id)
	else:
		# Si el perfil declara límites específicos de nivel, los respetamos de forma soberana
		if profile.has("min_level"):
			min_level = int(profile.get("min_level"))
		if profile.has("max_level"):
			max_level = int(profile.get("max_level"))
			
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

	if request.level < min_level or request.level > max_level:
		errors.append("Level '%d' violates contractual bounds [%d, %d]." % [request.level, min_level, max_level])
			
	return errors