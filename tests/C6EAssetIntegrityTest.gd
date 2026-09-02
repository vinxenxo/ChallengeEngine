extends SceneTree

const VALIDATOR = preload("res://core/validation/ChallengeDefinitionValidator.gd")

func _initialize() -> void:
	var failures: Array[String] = []
	var valid_cfg := _load_json("res://challenges/CHALLENGE_009.json")
	var valid_result := VALIDATOR.validate_definition(valid_cfg)
	if not bool(valid_result.get("is_valid", false)):
		failures.append("CHALLENGE_009 should pass asset integrity after the fix: %s" % valid_result.get("errors", []))

	var broken_cfg: Dictionary = valid_cfg.duplicate(true)
	broken_cfg["assets"]["background_path"] = "res://assets/c6/does_not_exist.svg"
	var broken_result := VALIDATOR.validate_definition(broken_cfg)
	if bool(broken_result.get("is_valid", false)):
		failures.append("Missing mandatory asset was accepted by Layer 0.")
	else:
		var errors_text := " ".join(broken_result.get("errors", []))
		if "does_not_exist.svg" not in errors_text:
			failures.append("Missing asset error did not expose the failing path: %s" % errors_text)

	if failures.is_empty():
		print("[C6E_ASSET_INTEGRITY_SUITE] PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		print("[C6E_ASSET_INTEGRITY_SUITE] FAIL count=%d" % failures.size())
		quit(1)

func _load_json(path: String) -> Dictionary:
	var file := FileAccess.open(path, FileAccess.READ)
	var json := JSON.new()
	var error := json.parse(file.get_as_text())
	if error != OK or not (json.data is Dictionary):
		return {}
	return json.data
