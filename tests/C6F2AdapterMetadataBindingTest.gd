# res://tests/C6F2AdapterMetadataBindingTest.gd
extends SceneTree

const AuthoringMechanicAdapter = preload(
	"res://core/authoring/AuthoringMechanicAdapter.gd"
)

const AuthoringMechanicRegistry = preload(
	"res://core/authoring/AuthoringMechanicRegistry.gd"
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


func _init() -> void:
	print("[TEST] Running C6F2AdapterMetadataBindingTest...")

	AuthoringMechanicRegistry.clear_registry()
	AuthoringMechanicRegistry.initialize_defaults()

	VideoProfileRegistry.clear_cache()
	AssetFamilyRegistry.clear_cache()

	var failures: Array[String] = []

	# =========================================================
	# 1. PILOT — COMPLETE HISTORICAL METADATA
	# =========================================================

	var pilot_adapter = (
		AuthoringMechanicRegistry.get_adapter("pilot")
	)

	if pilot_adapter == null:
		failures.append(
			"Pilot adapter not found in registry."
		)
	else:
		var video_binding: Dictionary = (
			pilot_adapter.default_video_profile()
		)

		var presentation_binding: Dictionary = (
			pilot_adapter.default_presentation_profile()
		)

		var asset_binding: Dictionary = (
			pilot_adapter.required_assets()
		)

		# -----------------------------------------------------
		# Video
		# -----------------------------------------------------

		if video_binding.get("source") != (
			AuthoringMechanicAdapter.Source.DECLARED
		):
			failures.append(
				"Pilot video profile is not DECLARED."
			)

		if video_binding.get("value") != "test_master_11s":
			failures.append(
				"Pilot video profile binding mismatch: %s"
				% str(video_binding.get("value"))
			)
		else:
			var video_data := (
				VideoProfileRegistry.get_profile(
					str(video_binding.get("value"))
				)
			)

			if video_data.is_empty():
				failures.append(
					"Pilot video profile 'test_master_11s' "
					+ "could not be resolved."
				)
			else:
				var video_errors := (
					VideoProfileValidator.validate(video_data)
				)

				if video_errors.size() > 0:
					failures.append(
						"Pilot video profile failed validation: %s"
						% str(video_errors)
					)

		# -----------------------------------------------------
		# Presentation
		# -----------------------------------------------------

		if presentation_binding.get("source") != (
			AuthoringMechanicAdapter.Source.DECLARED
		):
			failures.append(
				"Pilot presentation profile is not DECLARED."
			)

		if presentation_binding.get("value") != (
			"social_default_v1"
		):
			failures.append(
				"Pilot presentation profile binding mismatch: %s"
				% str(presentation_binding.get("value"))
			)
		else:
			var presentation_result := (
				PresentationBindingValidator.validate_binding(
					str(presentation_binding.get("value"))
				)
			)

			if not bool(
				presentation_result.get("success", false)
			):
				failures.append(
					"Pilot presentation binding failed: %s"
					% str(
						presentation_result.get(
							"error",
							"unknown error"
						)
					)
				)

		# -----------------------------------------------------
		# Asset Family
		# -----------------------------------------------------

		if asset_binding.get("source") != (
			AuthoringMechanicAdapter.Source.DECLARED
		):
			failures.append(
				"Pilot asset family is not DECLARED."
			)

		if asset_binding.get("value") != "fam_001":
			failures.append(
				"Pilot asset family binding mismatch: %s"
				% str(asset_binding.get("value"))
			)
		else:
			var asset_data := (
				AssetFamilyRegistry.get_family(
					str(asset_binding.get("value"))
				)
			)

			if asset_data.is_empty():
				failures.append(
					"Pilot asset family 'fam_001' "
					+ "could not be resolved."
				)
			else:
				var asset_errors := (
					AssetFamilyValidator.validate(
						asset_data
					)
				)

				if asset_errors.size() > 0:
					failures.append(
						"Pilot asset family failed validation: %s"
						% str(asset_errors)
					)

	# =========================================================
	# 2. PARTIAL READY MECHANICS
	# =========================================================

	var partial_mechanics := [
		"hit_v1",
		"catch_v1",
		"find_v1",
		"choose_v1",
		"count_v1"
	]

	for mechanic_id in partial_mechanics:
		var adapter := (
			AuthoringMechanicRegistry.get_adapter(
				mechanic_id
			)
		)

		if adapter == null:
			failures.append(
				"Adapter for '%s' not found."
				% mechanic_id
			)
			continue

		var video_binding: Dictionary = (
			adapter.default_video_profile()
		)

		var presentation_binding: Dictionary = (
			adapter.default_presentation_profile()
		)

		var asset_binding: Dictionary = (
			adapter.required_assets()
		)

		# -----------------------------------------------------
		# Video MUST remain UNAVAILABLE
		# -----------------------------------------------------

		if video_binding.get("source") != (
			AuthoringMechanicAdapter.Source.UNAVAILABLE
		):
			failures.append(
				"Mechanic '%s' incorrectly declares "
				+ "a video profile."
				% mechanic_id
			)

		# -----------------------------------------------------
		# Assets MUST remain UNAVAILABLE
		# -----------------------------------------------------

		if asset_binding.get("source") != (
			AuthoringMechanicAdapter.Source.UNAVAILABLE
		):
			failures.append(
				"Mechanic '%s' incorrectly declares "
				+ "an asset family."
				% mechanic_id
			)

		# -----------------------------------------------------
		# Presentation MUST be declared
		# -----------------------------------------------------

		if presentation_binding.get("source") != (
			AuthoringMechanicAdapter.Source.DECLARED
		):
			failures.append(
				"Mechanic '%s' presentation is not DECLARED."
				% mechanic_id
			)

		if presentation_binding.get("value") != (
			"social_default_v1"
		):
			failures.append(
				"Mechanic '%s' presentation binding mismatch."
				% mechanic_id
			)

	# =========================================================
	# 3. NO PARALLEL get_* API
	# =========================================================
	#
	# The adapters must expose the canonical F2.7.2 metadata API.
	# The accidental get_* methods introduced during integration
	# must not be used.

	var pilot_check := (
		AuthoringMechanicRegistry.get_adapter("pilot")
	)

	if pilot_check != null:
		if pilot_check.has_method("get_video_profile"):
			failures.append(
				"Pilot exposes forbidden parallel API "
				+ "'get_video_profile'."
			)

		if pilot_check.has_method("get_presentation_profile"):
			failures.append(
				"Pilot exposes forbidden parallel API "
				+ "'get_presentation_profile'."
			)

		if pilot_check.has_method("get_asset_family"):
			failures.append(
				"Pilot exposes forbidden parallel API "
				+ "'get_asset_family'."
			)

	# =========================================================
	# FINAL RESULT
	# =========================================================

	if failures.is_empty():
		print(
			"[C6F2_ADAPTER_METADATA_BINDING_SUITE] PASS"
		)
		quit(0)
		return

	for failure in failures:
		printerr("FAIL: " + failure)

	print(
		"[C6F2_ADAPTER_METADATA_BINDING_SUITE] "
		+ "FAIL count=%d"
		% failures.size()
	)

	quit(1)