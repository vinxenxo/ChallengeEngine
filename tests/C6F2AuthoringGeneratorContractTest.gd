class_name ChallengeGeneratorTest
extends SceneTree

const ChallengeAuthoringRequest = preload("res://core/authoring/ChallengeAuthoringRequest.gd")
const ChallengeGenerator = preload("res://core/authoring/ChallengeGenerator.gd")

func _init():
	print("[TEST] Running C6F2AuthoringGeneratorContractTest...")
	
	AuthoringMechanicRegistry.clear_registry()
	AuthoringMechanicRegistry.initialize_defaults()
	
	var valid_dict = {
		"mechanic": "find_v1",
		"level": 82,
		"seed": 472819,
		"profile": "default_find_v1",
		"overrides": { "capture_radius": 25.0 }
	}
	
	var req_res = ChallengeAuthoringRequest.create_from_dictionary(valid_dict)
	var gen_result = ChallengeGenerator.generate(req_res.request)
	
	# Como los adaptadores actuales devuelven UNAVAILABLE para vídeo/presentación/assets,
	# el generador debe fallar en la etapa de metadata_validation de forma determinista y explícita.
	if gen_result.success:
		printerr("FAIL: ChallengeGenerator succeeded despite unavailable contractual metadata.")
		quit(1)
		
	if gen_result.stage != "metadata_validation":
		printerr("FAIL: Expected failure stage 'metadata_validation', got '%s'." % gen_result.stage)
		quit(1)
		
	if not gen_result.error.contains("Metadata unavailable"):
		printerr("FAIL: Unexpected error message: " + gen_result.error)
		quit(1)
		
	print("[C6F2_AUTHORING_GENERATOR_CONTRACT_SUITE] PASS")
	quit(0)