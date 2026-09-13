# res://core/authoring/ChallengeMigrationAdapter.gd
class_name ChallengeMigrationAdapter
extends RefCounted

## C6-F/F1.1 — Explicit legacy V1 -> canonical V2 migration.
## The adapter never guesses missing authoring metadata silently.
## Migration defaults must be supplied explicitly by the caller.

static func migrate_legacy_v1_to_v2(config: Dictionary, policy: Dictionary = {}) -> Dictionary:
	var errors: Array[String] = []
	if not _is_legacy(config):
		errors.append("Input is not a legacy V1 challenge definition.")
		return {"is_valid": false, "errors": errors, "config": {}}

	for key in ["challenge_id", "mechanic", "generation", "video", "difficulty", "assets"]:
		if not config.has(key):
			errors.append("Missing legacy mandatory field '%s'." % key)

	if not errors.is_empty():
		return {"is_valid": false, "errors": errors, "config": {}}

	var generation: Dictionary = config["generation"]
	var video: Dictionary = config["video"]
	var difficulty: Dictionary = config["difficulty"]
	var content: Dictionary = config.get("content", {})
	var presentation: Dictionary = config.get("presentation", {})
	var assets: Dictionary = config["assets"]

	var authoring_version := str(policy.get("authoring_version", ""))
	if authoring_version.is_empty():
		errors.append("Migration policy must explicitly provide 'authoring_version'.")
	var engine_version := str(config.get("engine_version", policy.get("default_engine_version", "")))
	if engine_version.is_empty():
		errors.append("Migration policy/value missing for 'engine_version'.")
	var asset_family := str(config.get("asset_family", policy.get("default_asset_family", "")))
	var asset_family_version := str(config.get("asset_family_version", policy.get("default_asset_family_version", "")))
	var theme := str(config.get("theme", policy.get("default_theme", "")))
	var profile_id := str(config.get("video_profile", policy.get("default_profile_id", "")))
	var profile_version := str(config.get("video_profile_version", policy.get("default_profile_version", "")))
	for pair in [["asset_family", asset_family],["asset_family_version", asset_family_version],["theme", theme],["profile_id", profile_id],["profile_version", profile_version]]:
		if str(pair[1]).is_empty():
			errors.append("Migration policy/value missing for '%s'." % str(pair[0]))

	if not errors.is_empty():
		return {"is_valid": false, "errors": errors, "config": {}}

	# Generic schema owns only the boundary. The whole legacy difficulty block is
	# retained under simulation.parameters so no mechanic-specific semantics are lost.
	var parameters: Dictionary = _deep_copy_dictionary(difficulty)

	# PILOT V2 historically stores simulation parameters in content. Move only the
	# numeric/mechanical fields; preserve hook/cta as authoring copy.
	if str(config["mechanic"]) == "pilot":
		for key in ["start_x", "end_x", "target_start", "target_velocity", "trajectory_amplitude", "control_amplitude"]:
			if content.has(key):
				parameters[key] = content[key]

	var canonical_content := {}
	for key in ["hook", "reveal", "cta"]:
		if content.has(key):
			canonical_content[key] = content[key]

	var canonical_presentation: Dictionary = {
		"profile_id": profile_id,
		"profile_version": profile_version,
		"coordinate_space": str(presentation.get("coordinate_space", "CANVAS_1080X1920")),
		"secondary_binding": str(presentation.get("secondary_binding", "target_position"))
	}
	for key in ["static_target_position", "visual", "ui"]:
		if presentation.has(key):
			canonical_presentation[key] = _deep_copy_value(presentation[key])

	var canonical_video: Dictionary = {}
	for key in ["fps", "hook_duration", "game_duration", "reveal_duration", "cta_duration"]:
		if video.has(key):
			canonical_video[key] = video[key]
		elif key == "reveal_duration":
			canonical_video[key] = 0.0
	if canonical_video.has("fps"):
		canonical_video["fps"] = int(round(float(canonical_video["fps"])))

	var canonical := {
		"schema_version": "2.0",
		"version": authoring_version,
		"challenge_id": str(config["challenge_id"]),
		"engine_version": engine_version,
		"mechanic": str(config["mechanic"]),
		"mechanic_version": str(config.get("mechanic_version", policy.get("default_mechanic_version", ""))),
		"asset_family": asset_family,
		"asset_family_version": asset_family_version,
		"theme": theme,
		"simulation": {
			"seed": int(generation["seed"]),
			"rng_version": str(generation.get("rng_version", "1.0")),
			"parameters": parameters
		},
		"video": canonical_video,
		"difficulty": {"level": int(difficulty.get("level", 0))} if difficulty.has("level") else {},
		"content": canonical_content,
		"presentation": canonical_presentation,
		"assets": _deep_copy_dictionary(assets)
	}
	if canonical["difficulty"].is_empty():
		canonical["difficulty"] = {"level": int(policy.get("default_difficulty_level", 0))}
	for key in ["label"]:
		if difficulty.has(key):
			canonical["difficulty"][key] = difficulty[key]
	if config.has("autovetting"):
		canonical["autovetting"] = _deep_copy_value(config["autovetting"])
	var metadata: Dictionary = _deep_copy_dictionary(config.get("metadata", {}))
	if metadata.is_empty():
		metadata = _deep_copy_dictionary(config.get("metadata", {}))
	if not metadata.is_empty():
		canonical["metadata"] = metadata

	var result = {"is_valid": true, "errors": [], "config": canonical}
	return result

static func canonical_v2_to_runtime_v1(config: Dictionary) -> Dictionary:
	var difficulty: Dictionary = _deep_copy_dictionary(config.get("simulation", {}).get("parameters", {}))
	var content: Dictionary = _deep_copy_dictionary(config.get("content", {}))
	if str(config.get("mechanic", "")) == "pilot":
		for key in ["start_x", "end_x", "target_start", "target_velocity", "trajectory_amplitude", "control_amplitude"]:
			if difficulty.has(key):
				content[key] = difficulty[key]
				difficulty.erase(key)

	var presentation: Dictionary = _deep_copy_dictionary(config.get("presentation", {}))
	presentation.erase("profile_id")
	presentation.erase("profile_version")

	return {
		"schema_version": "1.0",
		"engine_version": str(config.get("engine_version", "")),
		"challenge_id": str(config.get("challenge_id", "")),
		"mechanic": str(config.get("mechanic", "")),
		"mechanic_version": str(config.get("mechanic_version", "")),
		"video_profile": str(config.get("presentation", {}).get("profile_id", "")),
		"video_profile_version": str(config.get("presentation", {}).get("profile_version", "")),
		"asset_family": str(config.get("asset_family", "")),
		"asset_family_version": str(config.get("asset_family_version", "")),
		"theme": str(config.get("theme", "")),
		"generation": {
			"seed": int(config.get("simulation", {}).get("seed", 0)),
			"rng_version": str(config.get("simulation", {}).get("rng_version", "1.0"))
		},
		"video": _deep_copy_dictionary(config.get("video", {})),
		"difficulty": difficulty,
		"content": content,
		"presentation": presentation,
		"assets": _deep_copy_dictionary(config.get("assets", {}))
	}

static func _is_legacy(config: Dictionary) -> bool:
	return config.has("generation") and config.has("video") and not config.has("simulation")

static func _deep_copy_dictionary(value: Dictionary) -> Dictionary:
	return _deep_copy_value(value)

static func _deep_copy_value(value):
	if value is Dictionary:
		var out: Dictionary = {}
		for key in value.keys():
			out[key] = _deep_copy_value(value[key])
		return out
	if value is Array:
		var out_array: Array = []
		for item in value:
			out_array.append(_deep_copy_value(item))
		return out_array
	return value
