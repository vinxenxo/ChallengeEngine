class_name AssetFamilyValidator
extends RefCounted

const ALLOWED_ROOT_KEYS = [
	"family_id",
	"version",
	"description",
	"themes",
	"background_path",
	"target_path",
	"object_path"
]

static func validate(profile: Dictionary) -> Array:
	var errors: Array = []
	for k in profile:
		if not ALLOWED_ROOT_KEYS.has(k):
			errors.append("Unknown root field: '%s'" % str(k))
	if not profile.has("family_id") or typeof(profile["family_id"]) != TYPE_STRING or profile["family_id"].strip_edges() == "":
		errors.append("Missing or invalid 'family_id'")
	if not profile.has("version") or typeof(profile["version"]) != TYPE_STRING or profile["version"].strip_edges() == "":
		errors.append("Missing or invalid 'version'")
	if profile.has("themes"):
		if typeof(profile["themes"]) != TYPE_ARRAY:
			errors.append("'themes' must be an Array of strings")
		else:
			for t in profile["themes"]:
				if typeof(t) != TYPE_STRING:
					errors.append("Theme entry must be a string")
	for key in ["background_path", "target_path", "object_path"]:
		if profile.has(key):
			if typeof(profile[key]) != TYPE_STRING or not str(profile[key]).begins_with("res://"):
				errors.append("'%s' must be a valid res:// resource path" % key)
	return errors
