# res://tests/C6F0_1_5CanonicalAssemblerTest.gd
extends SceneTree

const CanonicalV2Assembler = preload("res://core/authoring/CanonicalV2Assembler.gd")
const ChallengeAuthoringRequest = preload("res://core/authoring/ChallengeAuthoringRequest.gd")
const AuthoringMechanicRegistry = preload("res://core/authoring/AuthoringMechanicRegistry.gd")
const DifficultyProfileRegistry = preload("res://core/authoring/DifficultyProfileRegistry.gd")
const DifficultyResolver = preload("res://core/authoring/DifficultyResolver.gd")
const VideoProfileRegistry = preload("res://core/authoring/VideoProfileRegistry.gd")
const PresentationBindingValidator = preload("res://core/authoring/PresentationBindingValidator.gd")
const AssetFamilyRegistry = preload("res://core/authoring/AssetFamilyRegistry.gd")
const AssetFamilyValidator = preload("res://core/authoring/AssetFamilyValidator.gd")
const Schema = preload("res://core/validation/C6FChallengeSchemaValidator.gd")

var failures: Array[String] = []

func _initialize() -> void:
	print("[TEST] Running C6F0_1_5CanonicalAssemblerTest...")
	_run()
	if failures.is_empty():
		print("[C6F0_1_5_CANONICAL_ASSEMBLER_SUITE] PASS")
		quit(0)
		return
	for failure in failures:
		printerr("FAIL: " + failure)
	print("[C6F0_1_5_CANONICAL_ASSEMBLER_SUITE] FAIL count=%d" % failures.size())
	quit(1)

func _run() -> void:
	AuthoringMechanicRegistry.clear_registry()
	AuthoringMechanicRegistry.initialize_defaults()
	DifficultyProfileRegistry.clear_cache()
	VideoProfileRegistry.clear_cache()
	AssetFamilyRegistry.clear_cache()

	var request_result := ChallengeAuthoringRequest.create_from_dictionary({
		"mechanic": "pilot",
		"level": 3,
		"seed": 1337,
		"profile": "default_pilot",
		"overrides": {},
		"content": {
			"hook": "Hook",
			"reveal": "Reveal",
			"cta": "CTA"
		}
	})
	_assert(bool(request_result.get("success", false)), "Valid request creation failed.")
	if not bool(request_result.get("success", false)):
		return
	var request: ChallengeAuthoringRequest = request_result.get("request")

	var profile: Dictionary = DifficultyProfileRegistry.get_profile("default_pilot")
	_assert(not profile.is_empty(), "default_pilot profile must resolve.")
	if profile.is_empty():
		return

	var mock := {
		"mechanic": "pilot",
		"difficulty": {"level": 3, "overrides": {}},
		"simulation": {"parameters": {}}
	}
	var resolution: Dictionary = DifficultyResolver.resolve_for_challenge(mock, profile)
	_assert(bool(resolution.get("success", false)), "Difficulty resolution failed.")
	if not bool(resolution.get("success", false)):
		return

	var adapter: AuthoringMechanicAdapter = AuthoringMechanicRegistry.get_adapter("pilot")
	_assert(adapter != null, "Pilot authoring adapter missing.")
	if adapter == null:
		return

	var video_id := str(adapter.default_video_profile().get("value", ""))
	var video := VideoProfileRegistry.get_profile(video_id)
	_assert(not video.is_empty(), "Pilot video profile must resolve.")

	var presentation_id := str(adapter.default_presentation_profile().get("value", ""))
	var presentation_binding := PresentationBindingValidator.validate_binding(presentation_id)
	_assert(bool(presentation_binding.get("success", false)), "Presentation binding must succeed.")
	if not bool(presentation_binding.get("success", false)):
		return
	var presentation_profile: PresentationProfile = presentation_binding.get("profile")

	var family_id := str(adapter.required_assets().get("value", ""))
	var family := AssetFamilyRegistry.get_family(family_id)
	_assert(not family.is_empty(), "Pilot asset family must resolve.")
	var family_errors: Array = AssetFamilyValidator.validate(family)
	_assert(family_errors.is_empty(), "Pilot asset family validation failed: %s" % str(family_errors))

	var metadata := {"rng_version": str(adapter.rng_version().get("value", "")), "mechanic_version": "1.0"}
	var presentation_contract := {"coordinate_space": "CANVAS_1080X1920", "secondary_binding": "target_position", "profile_version": "1.0"}

	var assembled := CanonicalV2Assembler.assemble(
		request,
		resolution,
		metadata,
		video,
		presentation_profile,
		presentation_contract,
		family
	)
	_assert(bool(assembled.get("success", false)), "Canonical assembly failed: %s" % str(assembled.get("error", "")))
	if not bool(assembled.get("success", false)):
		return

	var canonical: Dictionary = assembled.get("challenge", {})
	var schema_result := Schema.validate_v2(canonical)
	_assert(bool(schema_result.get("is_valid", false)), "Canonical V2 rejected by executable schema validator: %s" % str(schema_result.get("errors", [])))
	_assert(canonical.get("content", {}).get("hook") == "Hook", "Content hook not preserved.")
	_assert(canonical.get("content", {}).get("reveal") == "Reveal", "Content reveal not preserved.")
	_assert(canonical.get("content", {}).get("cta") == "CTA", "Content CTA not preserved.")
	_assert(canonical.get("assets", {}).get("background_path", "").begins_with("res://"), "Canonical background asset path invalid.")

	var second := CanonicalV2Assembler.assemble(request, resolution, metadata, video, presentation_profile, presentation_contract, family)
	_assert(bool(second.get("success", false)), "Second canonical assembly failed.")
	_assert(canonical == second.get("challenge", {}), "Canonical assembly must be deterministic.")

func _assert(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)
