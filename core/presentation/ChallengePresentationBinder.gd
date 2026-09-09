class_name ChallengePresentationBinder
extends RefCounted

const PresentationBindingValidator = preload("res://core/authoring/PresentationBindingValidator.gd")
const PresentationProfile = preload("res://core/presentation/PresentationProfile.gd")
const AudioProfileRegistry = preload("res://core/authoring/AudioProfileRegistry.gd")
const AudioProfileValidator = preload("res://core/authoring/AudioProfileValidator.gd")
const AssetFamilyRegistry = preload("res://core/authoring/AssetFamilyRegistry.gd")
const AssetFamilyValidator = preload("res://core/authoring/AssetFamilyValidator.gd")
const PresentationBindingResult = preload("res://core/presentation/PresentationBindingResult.gd")
const VideoTimeline = preload("res://core/timeline/VideoTimeline.gd")

static func bind(canonical_v2: Dictionary, timeline: VideoTimeline, simulation_result: SimulationResult) -> PresentationBindingResult:
	var result = PresentationBindingResult.new()
	
	if canonical_v2.is_empty():
		result.error = "Canonical V2 definition is empty."
		return result
		
	if timeline == null:
		result.error = "Supplied VideoTimeline is null."
		return result
		
	if simulation_result == null or simulation_result.error_state != "OK":
		result.error = "SimulationResult is null or in an error state."
		return result

	var pres_input = canonical_v2.get("presentation", "")
	var pres_id = ""
	if typeof(pres_input) == TYPE_STRING:
		pres_id = pres_input.strip_edges()
	elif typeof(pres_input) == TYPE_DICTIONARY:
		pres_id = str(pres_input.get("profile_id", "")).strip_edges()
		
	if pres_id.is_empty():
		result.error = "Missing or empty presentation profile identifier in Canonical V2."
		return result
		
	var pres_res = PresentationBindingValidator.validate_binding(pres_id)
	if not bool(pres_res.get("success", false)):
		result.error = "Presentation profile binding failed: " + str(pres_res.get("error", "unknown error"))
		return result
		
	var profile: PresentationProfile = pres_res.get("profile")
	if profile == null:
		result.error = "Presentation validator succeeded without returning a profile object."
		return result
		
	result.presentation_profile = profile
	result.presentation_render_model = profile.build_render_model("GAME", {})

	if canonical_v2.has("audio"):
		var audio_input = canonical_v2.get("audio")
		var audio_id = ""
		if typeof(audio_input) == TYPE_STRING:
			audio_id = audio_input.strip_edges()
		elif typeof(audio_input) == TYPE_DICTIONARY:
			audio_id = str(audio_input.get("profile_id", "")).strip_edges()
			
		if not audio_id.is_empty():
			var audio_data = AudioProfileRegistry.get_profile(audio_id)
			if audio_data.is_empty():
				result.error = "Audio profile '%s' could not be resolved from registry." % audio_id
				return result
			var audio_errs = AudioProfileValidator.validate(audio_data)
			if audio_errs.size() > 0:
				result.error = "Audio profile '%s' failed validation: %s" % [audio_id, str(audio_errs)]
				return result
			result.audio_profile = audio_data

	var asset_family_id = str(canonical_v2.get("asset_family", "")).strip_edges()
	if asset_family_id.is_empty():
		result.error = "Missing or empty asset_family identifier in Canonical V2."
		return result
		
	var asset_family_data = AssetFamilyRegistry.get_family(asset_family_id)
	if asset_family_data.is_empty():
		result.error = "Asset family '%s' could not be resolved from registry." % asset_family_id
		return result
		
	var asset_errs = AssetFamilyValidator.validate(asset_family_data)
	if asset_errs.size() > 0:
		result.error = "Asset family '%s' failed validation: %s" % [asset_family_id, str(asset_errs)]
		return result
		
	result.asset_family_meta = asset_family_data

	var physical = canonical_v2.get("assets", {})
	if typeof(physical) == TYPE_DICTIONARY:
		result.physical_assets = physical.duplicate(true)

	result.timeline = timeline
	result.winning_frame = simulation_result.winning_frame

	result.success = true
	return result

## E2-Hardening: Frontera única que recibe el diccionario de contenido y extrae las autoridades de forma encapsulada
static func build_frame_render_model(
	state: String,
	content: Dictionary,
	profile: PresentationProfile
) -> Dictionary:
	var absolute_frame = int(content.get("absolute_frame", content.get("ui_state_frame", 0)))
	var winning_frame = int(content.get("winning_frame", -1))
	var timeline = content.get("timeline", null)
	
	var model = {}
	
	var overrides = {}
	if profile != null:
		if "overrides" in profile and typeof(profile.overrides) == TYPE_DICTIONARY:
			overrides = profile.overrides
		elif "composition" in profile and typeof(profile.composition) == TYPE_DICTIONARY:
			overrides = profile.composition
	
	model["badge_text"] = str(overrides.get("badge_text", ""))
	# Preserve the certified E2 CTA presentation contract.
	# The later E2 hardening revision replaced these historical defaults with
	# empty strings, leaving the CTA container present but visually blank.
	model["cta_main"] = str(overrides.get("cta_main", "LINK IN BIO"))
	model["cta_sub"] = str(overrides.get("cta_sub", "¡Juega ahora!"))
	model["success_text"] = str(overrides.get("success_text", ""))
	
	model["show_badge"] = (state == "HOOK")
	model["cta_visible"] = (state == "CTA")
	model["show_hook"] = (state == "HOOK")
	model["hook_text"] = str(content.get("hook", ""))
	
	# Countdown state & contract calculation (3 -> 2 -> 1 -> hidden)
	var countdown_vis = (state == "HOOK")
	var countdown_val = ""
	if countdown_vis:
		var fps = max(1, int(content.get("ui_fps", 60)))
		var state_frame = max(0, int(content.get("ui_state_frame", 0)))
		
		if state_frame < fps:
			countdown_val = "3"
		elif state_frame < fps * 2:
			countdown_val = "2"
		elif state_frame < fps * 3:
			countdown_val = "1"
		else:
			countdown_vis = false
			
	model["countdown_visible"] = countdown_vis
	model["countdown_value"] = countdown_val
	
	model["success_visible"] = (absolute_frame == winning_frame and state == "GAME")
	
	var is_reveal = false
	var reveal_prog = 0.0
	var hide_success_text = false
	
	if timeline != null and timeline.has_method("get_phase_at_frame"):
		var phase = str(timeline.get_phase_at_frame(absolute_frame)).to_upper()
		is_reveal = (phase == "REVEAL")
		
		if is_reveal:
			if absolute_frame > winning_frame + 60:
				hide_success_text = true
				
			var phase_start = 0
			if timeline.has_method("get_phase_start_frame"):
				phase_start = timeline.get_phase_start_frame("REVEAL")
				
			var duration = 0
			if "durations" in timeline and timeline.durations is Dictionary:
				duration = timeline.durations.get("REVEAL", 0)
				
			if duration > 0:
				reveal_prog = float(absolute_frame - phase_start) / float(duration)
				
	model["reveal_visible"] = is_reveal
	model["reveal_progress"] = reveal_prog
	model["hide_success_text"] = hide_success_text
	
	var w_frame_game = int(content.get("winning_frame_game", -1))
	var current_game_frame = int(content.get("ui_state_frame", -1))
	
	model["is_success_game"] = (current_game_frame == w_frame_game and state == "GAME")
	model["success_highlight_rects"] = content.get("winning_highlight_rects", [])
	
	return model