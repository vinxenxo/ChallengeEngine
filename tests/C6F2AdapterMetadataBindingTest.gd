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

		if video_binding.get("value") != "f4_legacy_60_h3_g7_r0_c2":
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
					"Pilot video profile 'f4_legacy_60_h3_g7_r0_c2' "
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

		if asset_binding.get("value") != "fam_pilot_01":
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
					"Pilot asset family 'fam_pilot_01' "
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
	# 2. READY MECHANICS — CURRENT DECLARED METADATA
	# =========================================================

	var expected_metadata: Dictionary = {
		"hit_v1": {"video": "f4_legacy_60_h0_g7_r0_c0", "assets": "fam_hit_01"},
		"catch_v1": {"video": "f4_legacy_60_h0_g7_r0_c2", "assets": "fam_catch_01"},
		"find_v1": {"video": "f4_legacy_60_h3_g7_r0_c0", "assets": "fam_find_01"},
		"choose_v1": {"video": "f4_legacy_60_h3_g7_r0_c2", "assets": "fam_choose_01"},
		"count_v1": {"video": "f4_legacy_60_h3_g7_r0_c2", "assets": "fam_count_01"}
	}

	for mechanic_id in expected_metadata.keys():
		var adapter := (
			AuthoringMechanicRegistry.get_adapter(
				mechanic_id
			)
		)

		if adapter == null:
			failures.append(
				"Adapter for '%s' not found." % mechanic_id
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

		var expected: Dictionary = expected_metadata[mechanic_id]

		if video_binding.get("source") != (
			AuthoringMechanicAdapter.Source.DECLARED
		):
			failures.append(
				"Mechanic '%s' video is not DECLARED." % mechanic_id
			)
		if video_binding.get("value") != expected.get("video"):
			failures.append(
				"Mechanic '%s' video binding mismatch: %s"
				% [mechanic_id, str(video_binding.get("value"))]
			)

		if asset_binding.get("source") != (
			AuthoringMechanicAdapter.Source.DECLARED
		):
			failures.append(
				"Mechanic '%s' assets are not DECLARED." % mechanic_id
			)
		if asset_binding.get("value") != expected.get("assets"):
			failures.append(
				"Mechanic '%s' asset family binding mismatch: %s"
				% [mechanic_id, str(asset_binding.get("value"))]
			)

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