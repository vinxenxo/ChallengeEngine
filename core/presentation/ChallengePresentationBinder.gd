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
	
	# 1. Null and State Gate Checks (Fail-Closed)
	if canonical_v2.is_empty():
		result.error = "Canonical V2 definition is empty."
		return result
		
	if timeline == null:
		result.error = "Supplied VideoTimeline is null."
		return result
		
	if simulation_result == null or simulation_result.error_state != "OK":
		result.error = "SimulationResult is null or in an error state."
		return result

	# 2. Presentation Profile Binding Resolution & Validation
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

	# 3. Audio Profile Binding Resolution & Validation (Optional pass-through, strict if present)
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

	# 4. Asset Family Binding Resolution & Validation (Identity)
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

	# 5. Physical Assets Pass-through
	var physical = canonical_v2.get("assets", {})
	if typeof(physical) == TYPE_DICTIONARY:
		result.physical_assets = physical.duplicate(true)

	# 6. Temporal & Winning Frame Ingestion (Strict reference preservation, no recalculation)
	result.timeline = timeline
	result.winning_frame = simulation_result.winning_frame

	result.success = true
	return result