extends SceneTree

const PresentationBindingValidator = preload(
	"res://core/authoring/PresentationBindingValidator.gd"
)

const PresentationProfile = preload(
	"res://core/presentation/PresentationProfile.gd"
)

const PresentationProfileValidator = preload(
	"res://core/validation/PresentationProfileValidator.gd"
)


func _init() -> void:
	print("[TEST] Running C6F2PresentationBindingContractTest...")

	var failures: Array[String] = []

	# ---------------------------------------------------------
	# 1. Valid binding using the canonical C6-E3 default ID
	# ---------------------------------------------------------

	var valid_id := PresentationProfile.DEFAULT_ID

	var valid_res := (
		PresentationBindingValidator.validate_binding(valid_id)
	)

	if not bool(valid_res.get("success", false)):
		failures.append(
			"Valid presentation profile '%s' rejected: %s"
			% [
				valid_id,
				str(valid_res.get("error", "unknown error"))
			]
		)
	else:
		var valid_profile = valid_res.get("profile", null)

		if valid_profile == null:
			failures.append(
				"Successful binding returned no PresentationProfile."
			)
		elif not (valid_profile is PresentationProfile):
			failures.append(
				"Successful binding did not return PresentationProfile."
			)
		elif valid_profile.profile_id != valid_id:
			failures.append(
				"Binding returned unexpected profile_id '%s'."
				% valid_profile.profile_id
			)

	# ---------------------------------------------------------
	# 2. Empty ID must fail closed
	# ---------------------------------------------------------

	var empty_res := (
		PresentationBindingValidator.validate_binding("")
	)

	if bool(empty_res.get("success", false)):
		failures.append(
			"Empty presentation profile ID was incorrectly accepted."
		)

	if not str(empty_res.get("error", "")).contains(
		"cannot be empty"
	):
		failures.append(
			"Unexpected error for empty presentation profile ID: %s"
			% str(empty_res.get("error", ""))
		)

	# ---------------------------------------------------------
	# 3. Whitespace-only ID must fail closed
	# ---------------------------------------------------------

	var whitespace_res := (
		PresentationBindingValidator.validate_binding("   ")
	)

	if bool(whitespace_res.get("success", false)):
		failures.append(
			"Whitespace-only presentation profile ID was accepted."
		)

	# ---------------------------------------------------------
	# 4. Sovereign validator agreement
	# ---------------------------------------------------------
	#
	# The binding must return a profile that the same C6-E3
	# validator accepts independently.

	var canonical_profile := PresentationProfile.from_challenge(
		{
			"presentation": {
				"profile": valid_id
			}
		}
	)

	var canonical_validation := (
		PresentationProfileValidator.validate_profile(
			canonical_profile
		)
	)

	if not bool(canonical_validation.get("is_valid", false)):
		failures.append(
			"Canonical C6-E3 PresentationProfile is not valid: %s"
			% str(canonical_validation.get("errors", []))
		)

	# ---------------------------------------------------------
	# 5. Difficulty orthogonality
	# ---------------------------------------------------------
	#
	# Two authoring configurations with different difficulty
	# levels must produce the same presentation binding when
	# presentation profile ID is unchanged.

	var low_config := {
		"mechanic": "pilot",
		"seed": 1234,
		"difficulty": {
			"level": 10
		},
		"presentation": {
			"profile": valid_id
		}
	}

	var high_config := {
		"mechanic": "pilot",
		"seed": 5678,
		"difficulty": {
			"level": 90
		},
		"presentation": {
			"profile": valid_id
		}
	}

	var low_profile := PresentationProfile.from_challenge(
		low_config
	)

	var high_profile := PresentationProfile.from_challenge(
		high_config
	)

	var low_validation := (
		PresentationProfileValidator.validate_profile(
			low_profile
		)
	)

	var high_validation := (
		PresentationProfileValidator.validate_profile(
			high_profile
		)
	)

	if not bool(low_validation.get("is_valid", false)):
		failures.append(
			"Low-difficulty presentation profile became invalid: %s"
			% str(low_validation.get("errors", []))
		)

	if not bool(high_validation.get("is_valid", false)):
		failures.append(
			"High-difficulty presentation profile became invalid: %s"
			% str(high_validation.get("errors", []))
		)

	# The binding identity must remain unchanged.
	if low_profile.profile_id != high_profile.profile_id:
		failures.append(
			"Presentation profile ID changed with difficulty."
		)

	# Canonical presentation properties must also remain identical.
	if low_profile.source_canvas_size != high_profile.source_canvas_size:
		failures.append(
			"source_canvas_size changed with difficulty."
		)

	if low_profile.master_output_size != high_profile.master_output_size:
		failures.append(
			"master_output_size changed with difficulty."
		)

	if low_profile.safe_area != high_profile.safe_area:
		failures.append(
			"safe_area changed with difficulty."
		)

	if low_profile.typography != high_profile.typography:
		failures.append(
			"typography changed with difficulty."
		)

	if low_profile.composition != high_profile.composition:
		failures.append(
			"composition changed with difficulty."
		)

	if low_profile.colors != high_profile.colors:
		failures.append(
			"colors changed with difficulty."
		)

	if low_profile.theme_name != high_profile.theme_name:
		failures.append(
			"theme_name changed with difficulty."
		)

	if low_profile.show_difficulty_badge != high_profile.show_difficulty_badge:
		failures.append(
			"show_difficulty_badge changed with difficulty."
		)

	# ---------------------------------------------------------
	# 6. Deterministic repeated binding
	# ---------------------------------------------------------

	var binding_a := (
		PresentationBindingValidator.validate_binding(valid_id)
	)

	var binding_b := (
		PresentationBindingValidator.validate_binding(valid_id)
	)

	if not bool(binding_a.get("success", false)):
		failures.append(
			"First deterministic binding attempt failed."
		)

	if not bool(binding_b.get("success", false)):
		failures.append(
			"Second deterministic binding attempt failed."
		)

	if bool(binding_a.get("success", false)) and bool(
		binding_b.get("success", false)
	):
		var profile_a: PresentationProfile = (
			binding_a.get("profile")
		)

		var profile_b: PresentationProfile = (
			binding_b.get("profile")
		)

		if profile_a.profile_id != profile_b.profile_id:
			failures.append(
				"Repeated binding returned different profile IDs."
			)

		if profile_a.source_canvas_size != profile_b.source_canvas_size:
			failures.append(
				"Repeated binding changed source canvas size."
			)

		if profile_a.master_output_size != profile_b.master_output_size:
			failures.append(
				"Repeated binding changed master output size."
			)

		if profile_a.safe_area != profile_b.safe_area:
			failures.append(
				"Repeated binding changed safe area."
			)

		if profile_a.typography != profile_b.typography:
			failures.append(
				"Repeated binding changed typography."
			)

		if profile_a.composition != profile_b.composition:
			failures.append(
				"Repeated binding changed composition."
			)

		if profile_a.colors != profile_b.colors:
			failures.append(
				"Repeated binding changed colors."
			)

		if profile_a.theme_name != profile_b.theme_name:
			failures.append(
				"Repeated binding changed theme."
			)

	# ---------------------------------------------------------
	# Final result
	# ---------------------------------------------------------

	if failures.is_empty():
		print(
			"[C6F2_PRESENTATION_BINDING_CONTRACT_SUITE] PASS"
		)
		quit(0)
		return

	for failure in failures:
		printerr("FAIL: " + failure)

	print(
		"[C6F2_PRESENTATION_BINDING_CONTRACT_SUITE] "
		+ "FAIL count=%d"
		% failures.size()
	)

	quit(1)