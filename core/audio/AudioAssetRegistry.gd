# core/audio/AudioAssetRegistry.gd
class_name AudioAssetRegistry
extends RefCounted

const ASSET_CATALOG_PATH = "res://profiles/audio/audio_assets.json"

# Resuelve de forma estrictamente declarativa, fail-closed y normalizada un asset_id a su definición semántica
static func resolve_asset(asset_id: String) -> Dictionary:
	if not FileAccess.file_exists(ASSET_CATALOG_PATH):
		push_error("C7_AUDIO_ASSET_CATALOG_MISSING: " + ASSET_CATALOG_PATH)
		return {}

	var file = FileAccess.open(ASSET_CATALOG_PATH, FileAccess.READ)
	if file == null:
		push_error("C7_AUDIO_ASSET_CATALOG_OPEN_FAILED: " + ASSET_CATALOG_PATH)
		return {}

	var parsed = JSON.parse_string(file.get_as_text())
	file.close()

	if typeof(parsed) != TYPE_DICTIONARY:
		push_error("C7_AUDIO_ASSET_CATALOG_INVALID_ROOT")
		return {}

	if not parsed.has("assets") or typeof(parsed["assets"]) != TYPE_DICTIONARY:
		push_error("C7_AUDIO_ASSET_CATALOG_INVALID_ASSETS")
		return {}

	var assets: Dictionary = parsed["assets"]

	if not assets.has(asset_id):
		push_error("C7_AUDIO_ASSET_UNKNOWN: " + asset_id)
		return {}

	var definition = assets[asset_id]

	if typeof(definition) != TYPE_DICTIONARY:
		push_error("C7_AUDIO_ASSET_INVALID_DEFINITION: " + asset_id)
		return {}

	if (
		not definition.has("generator_type")
		or typeof(definition["generator_type"]) != TYPE_STRING
		or definition["generator_type"].is_empty()
	):
		push_error("C7_AUDIO_ASSET_INVALID_GENERATOR: " + asset_id)
		return {}

	if (
		not definition.has("parameters")
		or typeof(definition["parameters"]) != TYPE_DICTIONARY
	):
		push_error("C7_AUDIO_ASSET_INVALID_PARAMETERS: " + asset_id)
		return {}

	var gen_type: String = definition["generator_type"]
	var raw_params: Dictionary = definition["parameters"]
	var normalized_params = {}

	# Normalización estricta de tipos sin alias ambiguos de final_frequency
	if gen_type == "tone_burst":
		if raw_params.has("frequency_hz"):
			normalized_params["frequency_hz"] = float(raw_params["frequency_hz"])

		if raw_params.has("amplitude"):
			normalized_params["amplitude"] = float(raw_params["amplitude"])

		if raw_params.has("attack_frames"):
			normalized_params["attack_frames"] = int(raw_params["attack_frames"])

		if raw_params.has("release_frames"):
			normalized_params["release_frames"] = int(raw_params["release_frames"])
	else:
		for key in raw_params.keys():
			normalized_params[key] = raw_params[key]

	return {
		"generator_type": gen_type,
		"parameters": normalized_params
	}