class_name ChallengeGenerator
extends RefCounted

const AuthoringMechanicAdapter = preload(
	"res://core/authoring/AuthoringMechanicAdapter.gd"
)

const ChallengeAuthoringRequestValidator = preload(
	"res://core/authoring/ChallengeAuthoringRequestValidator.gd"
)

const AuthoringMechanicRegistry = preload(
	"res://core/authoring/AuthoringMechanicRegistry.gd"
)

const DifficultyProfileRegistry = preload(
	"res://core/authoring/DifficultyProfileRegistry.gd"
)

const DifficultyResolver = preload(
	"res://core/authoring/DifficultyResolver.gd"
)

const VideoProfileRegistry = preload(
	"res://core/authoring/VideoProfileRegistry.gd"
)

const VideoProfileValidator = preload(
	"res://core/authoring/VideoProfileValidator.gd"
)

const PresentationBindingValidator = preload(
	"res://core/authoring/PresentationBindingValidator.gd"
)

const AssetFamilyRegistry = preload(
	"res://core/authoring/AssetFamilyRegistry.gd"
)

const AssetFamilyValidator = preload(
	"res://core/authoring/AssetFamilyValidator.gd"
)

const CanonicalV2Assembler = preload(
	"res://core/authoring/CanonicalV2Assembler.gd"
)

const ChallengeAuthoringPolicy = preload(
	"res://core/authoring/ChallengeAuthoringPolicy.gd"
)


static func generate(request: ChallengeAuthoringRequest) -> Dictionary:
	# =========================================================
	# 1. REQUEST VALIDATION
	# =========================================================

	var validation_errors := (
		ChallengeAuthoringRequestValidator.validate(request)
	)

	if validation_errors.size() > 0:
		return {
			"success": false,
			"stage": "request_validation",
			"error": (
				"Request validation failed: "
				+ str(validation_errors)
			),
			"challenge": null
		}

	# =========================================================
	# 2. DIFFICULTY RESOLUTION
	# =========================================================

	var difficulty_profile := (
		DifficultyProfileRegistry.get_profile(
			request.profile_id
		)
	)

	if difficulty_profile.is_empty():
		return {
			"success": false,
			"stage": "difficulty_resolution",
			"error": (
				"Profile '%s' could not be loaded."
				% request.profile_id
			),
			"challenge": null
		}

	var challenge_mock := {
		"mechanic": request.mechanic_id,
		"difficulty": {
			"level": request.level,
			"overrides": request.get_overrides()
		},
		"simulation": {
			"parameters": {}
		}
	}

	var resolution := DifficultyResolver.resolve_for_challenge(
		challenge_mock,
		difficulty_profile
	)

	if not bool(resolution.get("success", false)):
		return {
			"success": false,
			"stage": "difficulty_resolution",
			"error": (
				"Difficulty resolution failed: "
				+ str(resolution.get("error", "unknown error"))
			),
			"challenge": null
		}

	var effective_params: Dictionary = (
		resolution.get("effective_parameters", {})
	)

	# =========================================================
	# 3. ADAPTER RESOLUTION
	# =========================================================

	AuthoringMechanicRegistry.initialize_defaults()

	var adapter := (
		AuthoringMechanicRegistry.get_adapter(
			request.mechanic_id
		)
	)

	if adapter == null:
		return {
			"success": false,
			"stage": "adapter_resolution",
			"error": (
				"No AuthoringMechanicAdapter registered "
				+ "for mechanic '%s'."
				% request.mechanic_id
			),
			"challenge": null
		}

	# =========================================================
	# 4. METADATA + STRUCTURAL CONTRACT VALIDATION
	# =========================================================

	# ---------------------------------------------------------
	# 4.1 RNG
	# ---------------------------------------------------------

	var rng_res: Dictionary = adapter.rng_version()

	if rng_res.get("source") == (
		AuthoringMechanicAdapter.Source.UNAVAILABLE
	):
		return {
			"success": false,
			"stage": "metadata_validation",
			"error": (
				"Metadata unavailable [rng_version]: "
				+ str(rng_res.get("error", "unknown error"))
			),
			"challenge": null
		}

	# ---------------------------------------------------------
	# 4.2 VIDEO PROFILE
	# ---------------------------------------------------------

	var video_res: Dictionary = (
		adapter.default_video_profile()
	)

	if video_res.get("source") == (
		AuthoringMechanicAdapter.Source.UNAVAILABLE
	):
		return {
			"success": false,
			"stage": "metadata_validation",
			"error": (
				"Metadata unavailable "
				+ "[default_video_profile]: "
				+ str(video_res.get("error", "unknown error"))
			),
			"challenge": null
		}

	var video_profile_id := str(
		video_res.get("value", "")
	).strip_edges()

	if video_profile_id.is_empty():
		return {
			"success": false,
			"stage": "metadata_validation",
			"error": (
				"Invalid video profile binding: "
				+ "profile ID is empty."
			),
			"challenge": null
		}

	var video_profile := (
		VideoProfileRegistry.get_profile(
			video_profile_id
		)
	)

	if video_profile.is_empty():
		return {
			"success": false,
			"stage": "metadata_validation",
			"error": (
				"Video profile '%s' could not be resolved."
				% video_profile_id
			),
			"challenge": null
		}

	var video_errors := (
		VideoProfileValidator.validate(
			video_profile
		)
	)

	if video_errors.size() > 0:
		return {
			"success": false,
			"stage": "metadata_validation",
			"error": (
				"Video profile '%s' failed validation: %s"
				% [
					video_profile_id,
					str(video_errors)
				]
			),
			"challenge": null
		}

	# ---------------------------------------------------------
	# 4.3 PRESENTATION PROFILE
	# ---------------------------------------------------------

	var presentation_res: Dictionary = (
		adapter.default_presentation_profile()
	)

	if presentation_res.get("source") == (
		AuthoringMechanicAdapter.Source.UNAVAILABLE
	):
		return {
			"success": false,
			"stage": "metadata_validation",
			"error": (
				"Metadata unavailable "
				+ "[default_presentation_profile]: "
				+ str(
					presentation_res.get(
						"error",
						"unknown error"
					)
				)
			),
			"challenge": null
		}

	var presentation_profile_id := str(
		presentation_res.get("value", "")
	).strip_edges()

	if presentation_profile_id.is_empty():
		return {
			"success": false,
			"stage": "metadata_validation",
			"error": (
				"Invalid presentation profile binding: "
				+ "profile ID is empty."
			),
			"challenge": null
		}

	var presentation_binding := (
		PresentationBindingValidator.validate_binding(
			presentation_profile_id
		)
	)

	if not bool(
		presentation_binding.get("success", false)
	):
		return {
			"success": false,
			"stage": "metadata_validation",
			"error": (
				"Presentation profile binding failed: "
				+ str(
					presentation_binding.get(
						"error",
						"unknown error"
					)
				)
			),
			"challenge": null
		}

	var presentation_profile = (
		presentation_binding.get("profile")
	)

	if presentation_profile == null:
		return {
			"success": false,
			"stage": "metadata_validation",
			"error": (
				"Presentation profile binding succeeded "
				+ "without returning a profile."
			),
			"challenge": null
		}

	# ---------------------------------------------------------
	# 4.4 ASSET FAMILY
	# ---------------------------------------------------------

	var assets_res: Dictionary = (
		adapter.required_assets()
	)

	if assets_res.get("source") == (
		AuthoringMechanicAdapter.Source.UNAVAILABLE
	):
		return {
			"success": false,
			"stage": "metadata_validation",
			"error": (
				"Metadata unavailable [required_assets]: "
				+ str(
					assets_res.get(
						"error",
						"unknown error"
					)
				)
			),
			"challenge": null
		}

	var asset_family_id := str(
		assets_res.get("value", "")
	).strip_edges()

	if asset_family_id.is_empty():
		return {
			"success": false,
			"stage": "metadata_validation",
			"error": (
				"Invalid asset family binding: "
				+ "family ID is empty."
			),
			"challenge": null
		}

	var asset_family := (
		AssetFamilyRegistry.get_family(
			asset_family_id
		)
	)

	if asset_family.is_empty():
		return {
			"success": false,
			"stage": "metadata_validation",
			"error": (
				"Asset family '%s' could not be resolved."
				% asset_family_id
			),
			"challenge": null
		}

	var asset_errors := (
		AssetFamilyValidator.validate(
			asset_family
		)
	)

	if asset_errors.size() > 0:
		return {
			"success": false,
			"stage": "metadata_validation",
			"error": (
				"Asset family '%s' failed validation: %s"
				% [
					asset_family_id,
					str(asset_errors)
				]
			),
			"challenge": null
		}

	# ---------------------------------------------------------
	# 4.5 STRUCTURAL PARAMETERS
	# ---------------------------------------------------------

	var struct_res: Dictionary = (
		adapter.build_structural_parameters(
			request,
			effective_params
		)
	)

	if struct_res.get("source") == (
		AuthoringMechanicAdapter.Source.UNAVAILABLE
	):
		return {
			"success": false,
			"stage": "metadata_validation",
			"error": (
				"Structural parameters unavailable: "
				+ str(
					struct_res.get(
						"error",
						"unknown error"
					)
				)
			),
			"challenge": null
		}

	# =========================================================
	# 5. CANONICAL V2 ASSEMBLY
	# =========================================================
	#
	# IMPORTANT:
	# No simulation is executed here.
	# No RNG is consumed here.
	# Metadata has already crossed its sovereign validation
	# gates above.
	#
	# Existing F2.7.2 output shape is preserved to avoid
	# reopening the canonical V2 contract during F2.8.6.

	var canonical_v2 := {
		"schema_version": "2.0",

		"challenge_id": (
			"GEN_%s_%d"
			% [
				request.mechanic_id.to_upper(),
				request.seed
			]
		),

		"engine_version": "1.0",

		"mechanic": request.mechanic_id,
		"mechanic_version": "1.0",

		# Resolved authoritative asset metadata.
		"asset_family": asset_family.get(
			"family_id",
			asset_family_id
		),

		"asset_family_version": asset_family.get(
			"version",
			""
		),

		# Resolved from the sovereign PresentationProfile.
		"theme": presentation_profile.theme_name,

		"generation": {
			"seed": request.seed,
			"rng_version": rng_res.get("value")
		},

		"simulation": {
			"seed": request.seed,
			"rng_version": rng_res.get("value"),
			"parameters": struct_res.get("value")
		},

		# Preserve the established V2 reference shape.
		"video": video_profile_id,

		"content": {},

		"difficulty": {
			"level": request.level,
			"label": DifficultyResolver.get_band_for_level(
				request.level
			),
			"profile": request.profile_id,
			"overrides": request.get_overrides()
		},

		"presentation": presentation_profile_id
	}

	return {
		"success": true,
		"stage": "assembly",
		"error": "",
		"challenge": canonical_v2
	}

static func generate_normative(request: ChallengeAuthoringRequest) -> Dictionary:
	var validation_errors: Array = ChallengeAuthoringRequestValidator.validate(request)
	if not validation_errors.is_empty():
		return {
			"success": false,
			"stage": "request_validation",
			"error": "Request validation failed: " + str(validation_errors),
			"challenge": null
		}

	var difficulty_profile: Dictionary = DifficultyProfileRegistry.get_profile(request.profile_id)
	if difficulty_profile.is_empty():
		return {
			"success": false,
			"stage": "difficulty_resolution",
			"error": "Profile '%s' could not be loaded." % request.profile_id,
			"challenge": null
		}

	var challenge_mock: Dictionary = {
		"mechanic": request.mechanic_id,
		"difficulty": {
			"level": request.level,
			"overrides": request.get_overrides()
		},
		"simulation": {
			"parameters": {}
		}
	}

	var resolution: Dictionary = DifficultyResolver.resolve_for_challenge(
		challenge_mock,
		difficulty_profile
	)
	if not bool(resolution.get("success", false)):
		return {
			"success": false,
			"stage": "difficulty_resolution",
			"error": "Difficulty resolution failed: " + str(resolution.get("error", "unknown error")),
			"challenge": null
		}

	AuthoringMechanicRegistry.initialize_defaults()
	var adapter: AuthoringMechanicAdapter = AuthoringMechanicRegistry.get_adapter(request.mechanic_id)
	if adapter == null:
		return {
			"success": false,
			"stage": "adapter_resolution",
			"error": "No authoring adapter registered for mechanic '%s'." % request.mechanic_id,
			"challenge": null
		}

	var rng_res: Dictionary = adapter.rng_version()
	var video_res: Dictionary = adapter.default_video_profile()
	var presentation_res: Dictionary = adapter.default_presentation_profile()
	var asset_res: Dictionary = adapter.required_assets()

	for binding in [rng_res, video_res, presentation_res, asset_res]:
		if binding.get("source") == AuthoringMechanicAdapter.Source.UNAVAILABLE:
			return {
				"success": false,
				"stage": "metadata_validation",
				"error": "Required authoring metadata unavailable: " + str(binding.get("error", "unknown error")),
				"challenge": null
			}

	var video_profile_id: String = str(video_res.get("value", "")).strip_edges()
	var video_profile: Dictionary = VideoProfileRegistry.get_profile(video_profile_id)
	if video_profile.is_empty():
		return {"success": false, "stage": "metadata_validation", "error": "Video profile '%s' could not be resolved." % video_profile_id, "challenge": null}
	var video_errors: Array = VideoProfileValidator.validate(video_profile)
	if not video_errors.is_empty():
		return {"success": false, "stage": "metadata_validation", "error": "Video profile '%s' failed validation: %s" % [video_profile_id, str(video_errors)], "challenge": null}

	var presentation_id: String = str(presentation_res.get("value", "")).strip_edges()
	var presentation_binding: Dictionary = PresentationBindingValidator.validate_binding(presentation_id)
	if not bool(presentation_binding.get("success", false)):
		return {"success": false, "stage": "metadata_validation", "error": "Presentation profile binding failed: " + str(presentation_binding.get("error", "unknown error")), "challenge": null}
	var presentation_profile: PresentationProfile = presentation_binding.get("profile")
	if presentation_profile == null:
		return {"success": false, "stage": "metadata_validation", "error": "Presentation binding returned no profile.", "challenge": null}

	var asset_family_id: String = str(asset_res.get("value", "")).strip_edges()
	var asset_family: Dictionary = AssetFamilyRegistry.get_family(asset_family_id)
	if asset_family.is_empty():
		return {"success": false, "stage": "metadata_validation", "error": "Asset family '%s' could not be resolved." % asset_family_id, "challenge": null}
	var asset_errors: Array = AssetFamilyValidator.validate(asset_family)
	if not asset_errors.is_empty():
		return {"success": false, "stage": "metadata_validation", "error": "Asset family '%s' failed validation: %s" % [asset_family_id, str(asset_errors)], "challenge": null}

	var struct_res: Dictionary = adapter.build_structural_parameters(request, resolution.get("effective_parameters", {}))
	if struct_res.get("source") == AuthoringMechanicAdapter.Source.UNAVAILABLE:
		return {"success": false, "stage": "metadata_validation", "error": "Structural parameters unavailable: " + str(struct_res.get("error", "unknown error")), "challenge": null}

	var adapter_metadata: Dictionary = {
		"rng_version": str(rng_res.get("value", "")),
		"mechanic_version": ChallengeAuthoringPolicy.DEFAULT_MECHANIC_VERSION
	}

	var assembly := CanonicalV2Assembler.assemble(
		request,
		resolution,
		adapter_metadata,
		video_profile,
		presentation_profile,
		ChallengeAuthoringPolicy.build_presentation_binding(),
		asset_family
	)

	if not bool(assembly.get("success", false)):
		return {"success": false, "stage": "assembly", "error": str(assembly.get("error", "unknown error")), "challenge": null}

	return {"success": true, "stage": "assembly", "error": "", "challenge": assembly.get("challenge")}
