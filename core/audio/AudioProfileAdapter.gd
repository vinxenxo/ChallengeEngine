# core/audio/AudioProfileAdapter.gd
class_name AudioProfileAdapter
extends RefCounted

# Traduce el esquema authoring real al objeto semántico AudioProfile de forma fail-closed operacional
static func from_authoring_profile(profile_id: String, event_id: String) -> AudioProfile:
	var dict = AudioProfileRegistry.get_profile(profile_id)
	if dict.is_empty():
		push_error("C7_AUDIO_PROFILE_NOT_FOUND: " + profile_id)
		return null
	
	var sfx_section = dict.get("sfx", {})
	if typeof(sfx_section) != TYPE_DICTIONARY:
		push_error("C7_AUDIO_PROFILE_INVALID_SFX_SECTION: " + profile_id)
		return null
		
	if not sfx_section.get("enabled", false):
		push_error("C7_AUDIO_SFX_DISABLED: " + profile_id)
		return null
	
	var events_map = sfx_section.get("events", {})
	if typeof(events_map) != TYPE_DICTIONARY:
		push_error("C7_AUDIO_INVALID_EVENTS_MAP: " + profile_id)
		return null
		
	if not events_map.has(event_id):
		push_error("C7_AUDIO_EVENT_UNBOUND: " + event_id + " in profile " + profile_id)
		return null
	
	var asset_id = events_map[event_id]
	if typeof(asset_id) != TYPE_STRING or asset_id.is_empty():
		push_error("C7_AUDIO_INVALID_ASSET_ID for event: " + event_id)
		return null
	
	var asset_config = AudioAssetRegistry.resolve_asset(asset_id)
	if asset_config.is_empty():
		push_error("C7_AUDIO_ASSET_RESOLUTION_FAILED: " + asset_id)
		return null
	
	var gen_type: String = asset_config["generator_type"]
	var params: Dictionary = asset_config["parameters"]
	
	return AudioProfile.new(profile_id, gen_type, params)