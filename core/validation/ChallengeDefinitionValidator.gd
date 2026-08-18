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
	if not config.has("video") or not (config["video"] is Dictionary):
		errors.append("Missing or invalid mandatory section 'video'.")
	else:
		var video: Dictionary = config["video"]
		var fps: int = int(video.get("fps", 0))
		if fps <= 0:
			errors.append("Invalid 'fps' in video section: must be greater than 0.")

		var hook_dur: float = float(video.get("hook_duration", -1.0))
		var game_dur: float = float(video.get("game_duration", -1.0))
		var cta_dur: float = float(video.get("cta_duration", -1.0))

		if hook_dur < 0.0 or cta_dur < 0.0:
			errors.append("Durations 'hook_duration' and 'cta_duration' must be non-negative.")
		if game_dur <= 0.0:
			errors.append("'game_duration' must be strictly greater than 0.")

	# 4. Comprobación de parámetros de dificultad
	if not config.has("difficulty") or not (config["difficulty"] is Dictionary):
		errors.append("Missing or invalid mandatory section 'difficulty'.")

	if errors.is_empty():
		return {"is_valid": true, "errors": []}
	else:
		return {"is_valid": false, "errors": errors}