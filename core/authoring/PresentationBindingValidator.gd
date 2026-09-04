class_name PresentationBindingValidator
extends RefCounted

## C6-F2.8.2
## PresentationProfile Binding.
##
## Authority:
## - PresentationProfile (C6-E2/E3)
## - PresentationProfileValidator (C6-E3)
##
## This class owns only the authoring-time binding gate.
## It does NOT own:
## - timeline
## - RNG
## - simulation truth
## - winning-frame truth
## - presentation implementation
##
## IMPORTANT:
## C6-E3 does not provide a PresentationProfileRegistry.
## Therefore the binding resolves an ID through the canonical
## PresentationProfile.from_challenge() constructor and validates
## the resulting PresentationProfile with the sovereign validator.

const PresentationProfile = preload(
	"res://core/presentation/PresentationProfile.gd"
)

const PresentationProfileValidator = preload(
	"res://core/validation/PresentationProfileValidator.gd"
)


static func validate_binding(profile_id: String) -> Dictionary:
	var normalized_id := profile_id.strip_edges()

	# ---------------------------------------------------------
	# 1. Binding ID contract
	# ---------------------------------------------------------

	if normalized_id.is_empty():
		return {
			"success": false,
			"error": "Presentation profile ID cannot be empty."
		}

	# ---------------------------------------------------------
	# 2. Materialize canonical C6-E3 PresentationProfile
	# ---------------------------------------------------------
	#
	# We deliberately use the canonical constructor instead of
	# inventing a second registry or a parallel JSON schema.

	var config := {
		"presentation": {
			"profile": normalized_id
		}
	}

	var profile: PresentationProfile = (
		PresentationProfile.from_challenge(config)
	)

	# ---------------------------------------------------------
	# 3. Identity binding check
	# ---------------------------------------------------------

	if profile.profile_id != normalized_id:
		return {
			"success": false,
			"error": (
				"Presentation profile binding resolved to unexpected "
				+ "profile ID '%s' instead of '%s'."
			) % [profile.profile_id, normalized_id]
		}

	# ---------------------------------------------------------
	# 4. Sovereign structural validation
	# ---------------------------------------------------------

	var validation := (
		PresentationProfileValidator.validate_profile(profile)
	)

	if typeof(validation) != TYPE_DICTIONARY:
		return {
			"success": false,
			"error": (
				"Presentation profile validator returned an invalid "
				+ "result type for '%s'."
			) % normalized_id
		}

	if not bool(validation.get("is_valid", false)):
		return {
			"success": false,
			"error": (
				"Presentation profile '%s' failed structural validation: %s"
			) % [
				normalized_id,
				str(validation.get("errors", []))
			]
		}

	# ---------------------------------------------------------
	# 5. Successful binding
	# ---------------------------------------------------------

	return {
		"success": true,
		"error": "",
		"profile": profile
	}