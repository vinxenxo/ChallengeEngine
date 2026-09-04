class_name ChallengeGenerator
extends RefCounted

static func generate(request: ChallengeAuthoringRequest) -> Dictionary:
	# 1. Request Validation Stage
	var validation_errors = ChallengeAuthoringRequestValidator.validate(request)
	if validation_errors.size() > 0:
		return {
			"success": false,
			"stage": "request_validation",
			"error": "Request validation failed: " + str(validation_errors),
			"challenge": null
		}
		
	# 2. Difficulty Resolution Stage
	var profile = DifficultyProfileRegistry.get_profile(request.profile_id)
	if profile.is_empty():
		return {
			"success": false,
			"stage": "difficulty_resolution",
			"error": "Profile '%s' could not be loaded." % request.profile_id,
			"challenge": null
		}
		
	var challenge_mock = {
		"mechanic": request.mechanic_id,
		"difficulty": {
			"level": request.level,
			"overrides": request.get_overrides()
		},
		"simulation": { "parameters": {} }
	}
	
	var resolution = DifficultyResolver.resolve_for_challenge(challenge_mock, profile)
	if not resolution.success:
		return {
			"success": false,
			"stage": "difficulty_resolution",
			"error": "Difficulty resolution failed: " + resolution.error,
			"challenge": null
		}
		
	var effective_params = resolution.effective_parameters
	
	# 3. Adapter Resolution Stage
	AuthoringMechanicRegistry.initialize_defaults()
	var adapter = AuthoringMechanicRegistry.get_adapter(request.mechanic_id)
	if adapter == null:
		return {
			"success": false,
			"stage": "adapter_resolution",
			"error": "No AuthoringMechanicAdapter registered for mechanic '%s'." % request.mechanic_id,
			"challenge": null
		}
		
	# 4. Metadata Contractual & Structural Validation Stage
	var rng_res = adapter.rng_version()
	if rng_res.source == AuthoringMechanicAdapter.Source.UNAVAILABLE:
		return {
			"success": false,
			"stage": "metadata_validation",
			"error": "Metadata unavailable [rng_version]: " + rng_res.error,
			"challenge": null
		}
		
	var video_res = adapter.default_video_profile()
	if video_res.source == AuthoringMechanicAdapter.Source.UNAVAILABLE:
		return {
			"success": false,
			"stage": "metadata_validation",
			"error": "Metadata unavailable [default_video_profile]: " + video_res.error,
			"challenge": null
		}
		
	var pres_res = adapter.default_presentation_profile()
	if pres_res.source == AuthoringMechanicAdapter.Source.UNAVAILABLE:
		return {
			"success": false,
			"stage": "metadata_validation",
			"error": "Metadata unavailable [default_presentation_profile]: " + pres_res.error,
			"challenge": null
		}
		
	var assets_res = adapter.required_assets()
	if assets_res.source == AuthoringMechanicAdapter.Source.UNAVAILABLE:
		return {
			"success": false,
			"stage": "metadata_validation",
			"error": "Metadata unavailable [required_assets]: " + assets_res.error,
			"challenge": null
		}
		
	var struct_res = adapter.build_structural_parameters(request, effective_params)
	if struct_res.source == AuthoringMechanicAdapter.Source.UNAVAILABLE:
		return {
			"success": false,
			"stage": "metadata_validation",
			"error": "Structural parameters unavailable: " + struct_res.error,
			"challenge": null
		}
		
	# 5. Assembly Stage (Solo ocurre si todo lo anterior es DECLARED o DERIVED)
	var canonical_v2 = {
		"schema_version": "2.0",
		"challenge_id": "GEN_%s_%d" % [request.mechanic_id.to_upper(), request.seed],
		"engine_version": "1.0",
		"mechanic": request.mechanic_id,
		"mechanic_version": "1.0",
		"asset_family": assets_res.value,
		"asset_family_version": "1.0",
		"theme": "default",
		"generation": {
			"seed": request.seed,
			"rng_version": rng_res.value
		},
		"simulation": {
			"seed": request.seed,
			"rng_version": rng_res.value,
			"parameters": struct_res.value
		},
		"video": video_res.value,
		"content": {},
		"difficulty": {
			"level": request.level,
			"label": DifficultyResolver.get_band_for_level(request.level),
			"profile": request.profile_id,
			"overrides": request.get_overrides()
		},
		"presentation": pres_res.value
	}
	
	return {
		"success": true,
		"stage": "assembly",
		"error": "",
		"challenge": canonical_v2
	}