class_name ChallengeDeterminismTest
extends SceneTree

const ChallengeAuthoringRequest = preload("res://core/authoring/ChallengeAuthoringRequest.gd")
const ChallengeGenerator = preload("res://core/authoring/ChallengeGenerator.gd")

func _init():
	print("[TEST] Running C6F2AuthoringDeterminismTest...")
	
	AuthoringMechanicRegistry.clear_registry()
	AuthoringMechanicRegistry.initialize_defaults()
	
	var valid_dict = {
		"mechanic": "pilot",
		"level": 50,
		"seed": 998877,
		"profile": "default_pilot",
		"overrides": {}
	}
	
	var req_res_A = ChallengeAuthoringRequest.create_from_dictionary(valid_dict)
	var req_res_B = ChallengeAuthoringRequest.create_from_dictionary(valid_dict)
	
	var result_A = ChallengeGenerator.generate(req_res_A.request)
	var result_B = ChallengeGenerator.generate(req_res_B.request)
	
	# Verificación de Determinismo en el Fallo (Fail-Closed Idempotencia)
	if result_A.success != result_B.success:
		printerr("FAIL: Determinism broken. Success status differs.")
		quit(1)
		
	if result_A.stage != result_B.stage:
		printerr("FAIL: Determinism broken. Failure stages differ ('%s' vs '%s')." % [result_A.stage, result_B.stage])
		quit(1)
		
	if result_A.error != result_B.error:
		printerr("FAIL: Determinism broken. Error messages differ.")
		quit(1)
		
	print("[C6F2_AUTHORING_DETERMINISM_SUITE] PASS")
	quit(0)