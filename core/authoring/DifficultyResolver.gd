class_name DifficultyResolver
extends RefCounted

## C6-F2.1 — Pure difficulty resolution.
## No RNG, no time, no filesystem access, no mutation of caller dictionaries.

const BAND_EASY: String = "EASY"
const BAND_NORMAL: String = "NORMAL"
const BAND_HARD: String = "HARD"
const BAND_EXTREME: String = "EXTREME"

static func get_band_for_level(level: int) -> String:
	if level < 25:
		return BAND_EASY
	if level < 50:
		return BAND_NORMAL
	if level < 75:
		return BAND_HARD
	return BAND_EXTREME

static func resolve(level: int, profile_data: Dictionary, overrides: Dictionary = {}) -> Dictionary:
	var allowed_variant: Variant = profile_data.get("allowed_parameters", [])
	if not (allowed_variant is Array):
		return {
			"success": false,
			"error": "Profile field 'allowed_parameters' must be an Array.",
			"effective_parameters": {}
		}
	var allowed: Array = allowed_variant

	var invalid_keys: Array[String] = []
	for key in overrides.keys():
		if not allowed.has(key):
			invalid_keys.append(str(key))

	if not invalid_keys.is_empty():
		return {
			"success": false,
			"error": "Firewall breach: invalid override keys: %s" % str(invalid_keys),
			"effective_parameters": {}
		}

	var base_variant: Variant = profile_data.get("base_parameters", {})
	if not (base_variant is Dictionary):
		return {
			"success": false,
			"error": "Profile field 'base_parameters' must be a Dictionary.",
			"effective_parameters": {}
		}
	var base: Dictionary = base_variant

	var scaling_variant: Variant = profile_data.get("scaling", {})
	if not (scaling_variant is Dictionary):
		return {
			"success": false,
			"error": "Profile field 'scaling' must be a Dictionary.",
			"effective_parameters": {}
		}
	var scaling: Dictionary = scaling_variant

	var effective: Dictionary = {}
	for key in base.keys():
		effective[key] = base[key]

	var band: String = get_band_for_level(level)
	if scaling.has(band):
		var band_variant: Variant = scaling[band]
		if not (band_variant is Dictionary):
			return {
				"success": false,
				"error": "Profile scaling band '%s' must be a Dictionary." % band,
				"effective_parameters": {}
			}
		var band_parameters: Dictionary = band_variant
		for key in band_parameters.keys():
			effective[key] = band_parameters[key]

	for key in overrides.keys():
		effective[key] = overrides[key]

	return {
		"success": true,
		"error": "",
		"effective_parameters": effective
	}
