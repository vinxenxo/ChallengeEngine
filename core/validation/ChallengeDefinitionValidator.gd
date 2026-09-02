class_name ChallengeDefinitionValidator
extends RefCounted

## Validador de Capa 0: Garantiza que el JSON cargado cumple con el contrato mínimo para ser simulado.
static func validate_definition(config: Dictionary) -> Dictionary:
	var errors: Array[String] = []

	# 1. Comprobación de campos raíz obligatorios
	if not config.has("challenge_id") and not config.has("id"):
		errors.append("Missing mandatory identifier ('challenge_id' or 'id').")

	if not config.has("mechanic") or not (config["mechanic"] is String) or String(config["mechanic"]).is_empty():
		errors.append("Missing or invalid mandatory field 'mechanic'.")

	# 2. Comprobación de metadatos de generación (Seed)
	if not config.has("generation") or not (config["generation"] is Dictionary):
		errors.append("Missing or invalid mandatory section 'generation'.")
	else:
		var gen: Dictionary = config["generation"]
		if not gen.has("seed"):
			errors.append("Missing mandatory 'seed' in 'generation' section.")

		if gen.has("rng_version"):
			var rng_version: String = str(gen.get("rng_version", ""))
			if rng_version != "1.0" and rng_version != "2.0":
				errors.append("Unsupported 'rng_version': %s. Expected '1.0' or '2.0'." % rng_version)

	# 3. Comprobación de estructura temporal del vídeo (Capa 0 -> Video)
	# Contrato C6-D4: duración 0 = fase omitida; GAME debe ser > 0.
	if not config.has("video") or not (config["video"] is Dictionary):
		errors.append("Missing or invalid mandatory section 'video'.")
	else:
		var video: Dictionary = config["video"]
		var fps: int = int(video.get("fps", 0))
		if fps <= 0:
			errors.append("Invalid 'fps' in video section: must be greater than 0.")

		var hook_dur: float = float(video.get("hook_duration", -1.0))
		var game_dur: float = float(video.get("game_duration", -1.0))
		var reveal_dur: float = float(video.get("reveal_duration", 0.0))
		var cta_dur: float = float(video.get("cta_duration", -1.0))

		if hook_dur < 0.0 or cta_dur < 0.0:
			errors.append("Durations 'hook_duration' and 'cta_duration' must be non-negative (0 disables the phase).")
		if reveal_dur < 0.0:
			errors.append("Duration 'reveal_duration' must be non-negative (0 disables the phase).")
		if game_dur <= 0.0:
			errors.append("'game_duration' must be strictly greater than 0.")

	# 4. Integridad de assets obligatorios (antes de simulación/render)
	_validate_required_assets(config, errors)

	# 5. Contrato mínimo de presentation profile (sin autoridad temporal)
	_validate_presentation_profile(config, errors)

	# 6. Comprobación de parámetros de dificultad
	if not config.has("difficulty") or not (config["difficulty"] is Dictionary):
		errors.append("Missing or invalid mandatory section 'difficulty'.")

	if errors.is_empty():
		return {"is_valid": true, "errors": [], "error_codes": []}
	else:
		return {"is_valid": false, "errors": errors, "error_codes": ["CHALLENGE_INVALID"]}

static func _validate_required_assets(config: Dictionary, errors: Array[String]) -> void:
	if not config.has("assets") or not (config["assets"] is Dictionary):
		errors.append("Missing or invalid mandatory section 'assets'.")
		return

	var assets_cfg: Dictionary = config["assets"]
	var required_paths := {
		"background_path": "background",
		"target_path": "target",
		"object_path": "object"
	}

	for path_key in required_paths.keys():
		if not assets_cfg.has(path_key):
			errors.append("Missing mandatory asset path '%s'." % path_key)
			continue

		var asset_path: String = str(assets_cfg.get(path_key, ""))
		if asset_path.is_empty():
			errors.append("Mandatory asset path '%s' is empty." % path_key)
			continue

		if not asset_path.begins_with("res://"):
			errors.append("Mandatory asset '%s' must use a res:// path: %s" % [path_key, asset_path])
			continue

		if not ResourceLoader.exists(asset_path):
			errors.append("Missing mandatory asset '%s': %s" % [path_key, asset_path])


static func _validate_presentation_profile(config: Dictionary, errors: Array[String]) -> void:
	if not config.has("presentation"):
		return

	if not (config["presentation"] is Dictionary):
		errors.append("'presentation' must be a Dictionary when provided.")
		return

	var presentation: Dictionary = config["presentation"]
	if presentation.has("profile"):
		var profile_id := str(presentation.get("profile", ""))
		if profile_id.is_empty():
			errors.append("'presentation.profile' must be a non-empty string.")

	if presentation.has("profile_overrides") and not (presentation["profile_overrides"] is Dictionary):
		errors.append("'presentation.profile_overrides' must be a Dictionary when provided.")
