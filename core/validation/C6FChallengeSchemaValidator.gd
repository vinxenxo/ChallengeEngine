# res://core/validation/C6FChallengeSchemaValidator.gd
class_name C6FChallengeSchemaValidator
extends RefCounted

## Executable subset of the normative challenge_schema.json contract.
## The JSON Schema remains the normative artifact; this class enforces the same
## boundary inside Godot without introducing a third-party JSON-Schema runtime.

static func validate_v2(config: Dictionary) -> Dictionary:
	var errors: Array[String] = []
	_check_string_const(config, "schema_version", "2.0", errors)
	_check_semver(config, "version", errors)
	for key in ["challenge_id", "engine_version", "mechanic", "mechanic_version", "asset_family", "asset_family_version", "theme"]:
		if not config.has(key) or not (config[key] is String) or str(config[key]).is_empty():
			errors.append("Missing or invalid canonical field '%s'." % key)
	if not config.has("simulation") or not (config["simulation"] is Dictionary): errors.append("Missing or invalid 'simulation'.")
	else: _validate_simulation(config["simulation"], errors)
	if not config.has("video") or not (config["video"] is Dictionary): errors.append("Missing or invalid 'video'.")
	else: _validate_video(config["video"], errors)
	if not config.has("difficulty") or not (config["difficulty"] is Dictionary): errors.append("Missing or invalid 'difficulty'.")
	if not config.has("content") or not (config["content"] is Dictionary): errors.append("Missing or invalid 'content'.")
	if not config.has("presentation") or not (config["presentation"] is Dictionary): errors.append("Missing or invalid 'presentation'.")
	else: _validate_presentation(config["presentation"], errors)
	if not config.has("assets") or not (config["assets"] is Dictionary): errors.append("Missing or invalid 'assets'.")
	else: _validate_assets(config["assets"], errors)
	return {"is_valid": errors.is_empty(), "errors": errors}

static func _validate_simulation(cfg: Dictionary, errors: Array[String]) -> void:
	for key in ["seed", "rng_version", "parameters"]:
		if not cfg.has(key): errors.append("Missing mandatory 'simulation.%s'." % key)
	if cfg.has("seed") and not (cfg["seed"] is int): errors.append("'simulation.seed' must be an integer.")
	if cfg.has("rng_version") and str(cfg["rng_version"]) not in ["1.0", "2.0"]: errors.append("Unsupported 'simulation.rng_version'.")
	if cfg.has("parameters") and not (cfg["parameters"] is Dictionary): errors.append("'simulation.parameters' must be an object.")

static func _validate_video(cfg: Dictionary, errors: Array[String]) -> void:
	for key in ["fps", "hook_duration", "game_duration", "reveal_duration", "cta_duration"]:
		if not cfg.has(key): errors.append("Missing mandatory 'video.%s'." % key)
	if cfg.has("fps"):
		var fps_value = cfg["fps"]
		var fps_numeric := false
		if fps_value is int:
			fps_numeric = int(fps_value) > 0
		elif fps_value is float:
			fps_numeric = float(fps_value) > 0.0 and is_equal_approx(float(fps_value), round(float(fps_value)))
		if not fps_numeric:
			errors.append("'video.fps' must be a positive integer.")
	for key in ["hook_duration", "reveal_duration", "cta_duration"]:
		if cfg.has(key) and float(cfg[key]) < 0.0: errors.append("'video.%s' must be non-negative." % key)
	if cfg.has("game_duration") and float(cfg["game_duration"]) <= 0.0: errors.append("'video.game_duration' must be > 0.")

static func _validate_presentation(cfg: Dictionary, errors: Array[String]) -> void:
	for key in ["profile_id", "coordinate_space", "secondary_binding"]:
		if not cfg.has(key) or not (cfg[key] is String) or str(cfg[key]).is_empty(): errors.append("Missing or invalid 'presentation.%s'." % key)
	if cfg.has("secondary_binding") and str(cfg["secondary_binding"]) not in ["static_position", "target_position", "target_x", "target_state"]: errors.append("Invalid 'presentation.secondary_binding'.")
	if cfg.has("static_target_position") and (not (cfg["static_target_position"] is Array) or cfg["static_target_position"].size() != 2): errors.append("'presentation.static_target_position' must contain exactly two values.")

static func _validate_assets(cfg: Dictionary, errors: Array[String]) -> void:
	for key in ["background_path", "target_path", "object_path"]:
		if not cfg.has(key) or not (cfg[key] is String) or not str(cfg[key]).begins_with("res://"):
			errors.append("Invalid mandatory asset path '%s'." % key)

static func _check_string_const(cfg: Dictionary, key: String, expected: String, errors: Array[String]) -> void:
	if str(cfg.get(key, "")) != expected: errors.append("'%s' must equal '%s'." % [key, expected])

static func _check_semver(cfg: Dictionary, key: String, errors: Array[String]) -> void:
	var value := str(cfg.get(key, ""))
	var parts := value.split(".")
	if parts.size() != 3: errors.append("'%s' must be semantic version X.Y.Z." % key)
	else:
		for p in parts:
			if p.is_empty() or not p.is_valid_int(): errors.append("'%s' must be semantic version X.Y.Z." % key); break
