extends SceneTree

const VALIDATOR = preload("res://core/validation/PresentationProfileValidator.gd")
const CHALLENGE_VALIDATOR = preload("res://core/validation/ChallengeDefinitionValidator.gd")

func _initialize() -> void:
	var failures: Array[String] = []

	var valid_cfg := _load_json("res://challenges/CHALLENGE_001.json")
	var valid_profile := PresentationProfile.from_challenge(valid_cfg)
	var valid := VALIDATOR.validate_profile(valid_profile)
	if not bool(valid.get("is_valid", false)):
		failures.append("Valid profile rejected: %s" % valid.get("errors", []))

	# Profile invalid: safe area outside canvas.
	var bad_safe_cfg: Dictionary = valid_cfg.duplicate(true)
	bad_safe_cfg["presentation"]["profile_overrides"] = {
		"safe_area": {"left": 300.0, "right": 300.0, "top": 10.0, "bottom": 10.0}
	}
	var bad_safe := VALIDATOR.validate_challenge(bad_safe_cfg)
	if bool(bad_safe.get("is_valid", false)):
		failures.append("Invalid safe area was accepted.")

	# Profile invalid: typography too wide for safe area.
	var bad_typo_cfg: Dictionary = valid_cfg.duplicate(true)
	bad_typo_cfg["presentation"]["profile_overrides"] = {
		"typography": {"max_text_width": 9999}
	}
	var bad_typo := VALIDATOR.validate_challenge(bad_typo_cfg)
	if bool(bad_typo.get("is_valid", false)):
		failures.append("Impossible typography width was accepted.")

	# Profile invalid: unsupported composition token.
	var bad_comp_cfg: Dictionary = valid_cfg.duplicate(true)
	bad_comp_cfg["presentation"]["profile_overrides"] = {
		"composition": {"gameplay": "outside_canvas"}
	}
	var bad_comp := VALIDATOR.validate_challenge(bad_comp_cfg)
	if bool(bad_comp.get("is_valid", false)):
		failures.append("Unsupported gameplay composition was accepted.")

	# Profile invalid: scale out of bounds.
	var bad_scale_cfg: Dictionary = valid_cfg.duplicate(true)
	bad_scale_cfg["presentation"]["profile_overrides"] = {
		"typography": {"scale": 0.0}
	}
	var bad_scale := VALIDATOR.validate_challenge(bad_scale_cfg)
	if bool(bad_scale.get("is_valid", false)):
		failures.append("Invalid typography scale was accepted.")

	# Integration gate: the same invalid profile must fail before simulation/render.
	var challenge_gate := CHALLENGE_VALIDATOR.validate_definition(bad_comp_cfg)
	if bool(challenge_gate.get("is_valid", false)):
		failures.append("Layer 0 accepted an invalid presentation profile.")

	# Physical output contract.
	if valid_profile.source_canvas_size != Vector2(540, 960):
		failures.append("Unexpected source canvas size.")
	if valid_profile.master_output_size != Vector2(1080, 1920):
		failures.append("Unexpected master output size.")

	# Theme/font contract.
	var theme := PresentationTheme.get_theme_config(valid_profile.theme_name)
	if not (theme.get("font", null) is Font):
		failures.append("Configured presentation theme has no loadable font.")

	if failures.is_empty():
		print("[C6E3_PRESENTATION_VALIDATION_SUITE] PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		print("[C6E3_PRESENTATION_VALIDATION_SUITE] FAIL count=%d" % failures.size())
		quit(1)

func _load_json(path: String) -> Dictionary:
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		return {}
	var parsed = JSON.parse_string(file.get_as_text())
	if parsed is Dictionary:
		return parsed
	return {}
