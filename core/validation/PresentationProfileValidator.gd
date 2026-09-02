class_name PresentationProfileValidator
extends RefCounted

## C6-E / E3 — Hard presentation-profile validation gate.
## Presentation-only. Never owns timeline, RNG or simulation truth.

const REQUIRED_TYPOGRAPHY_KEYS := [
	"scale",
	"headline_size",
	"body_size",
	"badge_size",
	"cta_size",
	"countdown_size",
	"max_text_width"
]

const REQUIRED_COMPOSITION_KEYS := [
	"hook",
	"gameplay",
	"difficulty_badge",
	"reveal",
	"cta"
]

const ALLOWED_COMPOSITION_VALUES := {
	"hook": ["top", "center", "bottom"],
	"gameplay": ["center", "lower_center", "upper_center"],
	"difficulty_badge": ["top_right", "top_left"],
	"reveal": ["center", "top", "bottom"],
	"cta": ["bottom", "center", "top"]
}

static func validate_profile(profile: PresentationProfile) -> Dictionary:
	var errors: Array[String] = []

	if profile == null:
		return _result(["presentation profile is null"])

	var base: Dictionary = profile.validate()
	if not bool(base.get("is_valid", false)):
		for error in base.get("errors", []):
			errors.append(str(error))

	if profile.theme_name.is_empty():
		errors.append("theme_name must not be empty")

	_validate_typography(profile.typography, profile.safe_area.size.x, errors)
	_validate_composition(profile.composition, errors)
	_validate_theme(profile.theme_name, errors)

	if profile.has_method("build_render_model"):
		var model: Dictionary = profile.build_render_model("GAME", {})
		for key in [
			"profile_id",
			"source_canvas_size",
			"master_output_size",
			"safe_area",
			"typography",
			"composition",
			"asset_family",
			"theme_name",
			"phase",
			"content"
		]:
			if not model.has(key):
				errors.append("render model missing required key '%s'" % key)

	return _result(errors)


static func validate_challenge(config: Dictionary) -> Dictionary:
	if not config.has("presentation"):
		return {"is_valid": true, "errors": [], "error_codes": []}

	if not (config["presentation"] is Dictionary):
		return _result(["'presentation' must be a Dictionary when provided"])

	var profile := PresentationProfile.from_challenge(config)
	return validate_profile(profile)


static func _validate_typography(typography: Dictionary, safe_width: float, errors: Array[String]) -> void:
	for key in REQUIRED_TYPOGRAPHY_KEYS:
		if not typography.has(key):
			errors.append("typography missing required key '%s'" % key)

	var scale := float(typography.get("scale", 1.0))
	if not is_finite(scale) or scale <= 0.0 or scale > 4.0:
		errors.append("typography.scale must be finite and in (0, 4]")

	for key in [
		"headline_size",
		"body_size",
		"badge_size",
		"cta_size",
		"countdown_size"
	]:
		var value := float(typography.get(key, 0))
		if not is_finite(value) or value <= 0.0 or value > 256.0:
			errors.append("typography.%s must be finite and in (0, 256]" % key)

	var max_text_width := float(typography.get("max_text_width", 0))
	if not is_finite(max_text_width) or max_text_width <= 0.0:
		errors.append("typography.max_text_width must be finite and greater than 0")
	elif max_text_width > safe_width:
		errors.append("typography.max_text_width must not exceed safe_area width")


static func _validate_composition(composition: Dictionary, errors: Array[String]) -> void:
	for key in REQUIRED_COMPOSITION_KEYS:
		if not composition.has(key):
			errors.append("composition missing required key '%s'" % key)
			continue

		var value := str(composition.get(key, ""))
		var allowed: Array = ALLOWED_COMPOSITION_VALUES.get(key, [])
		if value not in allowed:
			errors.append("composition.%s has unsupported value '%s'" % [key, value])


static func _validate_theme(theme_name: String, errors: Array[String]) -> void:
	var theme: Dictionary = PresentationTheme.get_theme_config(theme_name)
	if theme.is_empty():
		errors.append("theme '%s' resolved to an empty configuration" % theme_name)
		return

	if not theme.has("font") or not (theme["font"] is Font):
		errors.append("theme '%s' has no loadable Font" % theme_name)

	for key in ["hook_font_size", "reveal_font_size", "cta_font_size", "countdown_font_size", "difficulty_font_size"]:
		var value := float(theme.get(key, 0))
		if not is_finite(value) or value <= 0.0:
			errors.append("theme.%s must be finite and greater than 0" % key)


static func _result(errors: Array[String]) -> Dictionary:
	if errors.is_empty():
		return {"is_valid": true, "errors": [], "error_codes": []}
	return {
		"is_valid": false,
		"errors": errors,
		"error_codes": ["PRESENTATION_PROFILE_INVALID"]
	}
