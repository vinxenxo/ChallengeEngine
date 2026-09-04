class_name DifficultyResolver
extends RefCounted

const BAND_EASY = "EASY"
const BAND_NORMAL = "NORMAL"
const BAND_HARD = "HARD"
const BAND_EXTREME = "EXTREME"

static func get_band_for_level(level: int) -> String:
	if level < 25: return BAND_EASY
	if level < 50: return BAND_NORMAL
	if level < 75: return BAND_HARD
	return BAND_EXTREME

static func resolve(level: int, profile_data: Dictionary, overrides: Dictionary = {}) -> Dictionary:
	var allowed = profile_data.get("allowed_parameters", [])
	
	# 1. Firewall estricto
	var invalid_keys = []
	for k in overrides:
		if not allowed.has(k):
			invalid_keys.append(k)
			
	if invalid_keys.size() > 0:
		return {
			"success": false,
			"error": "Firewall breach: Invalid override keys detected: " + str(invalid_keys),
			"effective_parameters": {}
		}
		
	var effective = {}
	
	# 2. Base parameters
	var base = profile_data.get("base_parameters", {})
	for k in base:
		effective[k] = base[k]
		
	# 3. Band scaling
	var band = get_band_for_level(level)
	var scaling = profile_data.get("scaling", {})
	if scaling.has(band):
		var band_params = scaling[band]
		for k in band_params:
			effective[k] = band_params[k]
			
	# 4. Overrides
	for k in overrides:
		effective[k] = overrides[k]
		
	return {
		"success": true,
		"error": "",
		"effective_parameters": effective
	}

# =========================================================================
# F2.4 RUNTIME INTEGRATION (Precedencia y Resolución orquestada)
# =========================================================================
static func resolve_for_challenge(challenge_data: Dictionary, profile_data: Dictionary) -> Dictionary:
	# 1. PRECEDENCIA ABSOLUTA: Si el desafío ya tiene simulation.parameters explícitos, 
	# no se debe resolver nada. Se asume como un contrato ya cerrado (e.g. fixtures legacy o autoría directa).
	var sim_params = challenge_data.get("simulation", {}).get("parameters", {})
	if typeof(sim_params) == TYPE_DICTIONARY and not sim_params.is_empty():
		return {
			"success": true,
			"error": "",
			"effective_parameters": sim_params.duplicate(true)
		}
		
	# 2. Si no hay parámetros explícitos, resolvemos la intención de autoría
	var diff = challenge_data.get("difficulty", {})
	var level = diff.get("level", 50)
	var overrides = diff.get("overrides", {})
	
	# 3. Validar contrato de perfil (F2.5)
	var validation_errors = DifficultyProfileValidator.validate(challenge_data, profile_data)
	if validation_errors.size() > 0:
		return {
			"success": false,
			"error": "Profile validation failed: " + str(validation_errors),
			"effective_parameters": {}
		}
		
	# 4. Resolver
	return resolve(level, profile_data, overrides)