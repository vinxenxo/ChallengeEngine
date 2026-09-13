# res://tests/C6F2AuthoringAdapterContractTest.gd
extends SceneTree

const AuthoringMechanicRegistry = preload("res://core/authoring/AuthoringMechanicRegistry.gd")
const AuthoringMechanicAdapter = preload("res://core/authoring/AuthoringMechanicAdapter.gd")
const ChallengeAuthoringRequest = preload("res://core/authoring/ChallengeAuthoringRequest.gd")

func _init():
	print("[TEST] Running C6F2AuthoringAdapterContractTest...")
	
	# Inicializamos el registro
	AuthoringMechanicRegistry.clear_registry()
	AuthoringMechanicRegistry.initialize_defaults()
	
	var expected_ready = ["pilot", "hit_v1", "catch_v1", "find_v1", "choose_v1", "count_v1"]
	var blocked_partial = ["key", "parking", "parking_v2"]
	
	# 1. Verificar registros
	for mech in expected_ready:
		if not AuthoringMechanicRegistry.is_registered(mech):
			printerr("FAIL: Expected READY mechanic '%s' is not registered." % mech)
			quit(1)
			
	for mech in blocked_partial:
		if AuthoringMechanicRegistry.is_registered(mech):
			printerr("FAIL: PARTIAL mechanic '%s' was incorrectly registered as READY." % mech)
			quit(1)
			
	# 2. Auditar cada adapter registrado
	var dummy_request = ChallengeAuthoringRequest.new("dummy", 50, 1234, "dummy_profile", {})
	var dummy_params = {"mock_param": 100}
	
	for mech in expected_ready:
		var adapter = AuthoringMechanicRegistry.get_adapter(mech)
		
		# Verificación de identidad
		if adapter.mechanic_id() != mech:
			printerr("FAIL: Adapter identity mismatch. Expected '%s', got '%s'." % [mech, adapter.mechanic_id()])
			quit(1)
			
		# Verificación RNG (Deben ser explícitamente DECLARED y 2.0 por el manifest actual)
		var rng_res = adapter.rng_version()
		if rng_res.source != AuthoringMechanicAdapter.Source.DECLARED or rng_res.value != "2.0":
			printerr("FAIL: rng_version contract broken on %s." % mech)
			quit(1)
			
		# Verificación de Bloqueo de Defaults Inventados (Deben ser UNAVAILABLE)
		if adapter.default_video_profile().source != AuthoringMechanicAdapter.Source.UNAVAILABLE:
			printerr("FAIL: default_video_profile on %s illegally returned a value instead of UNAVAILABLE." % mech)
			quit(1)
			
		if adapter.default_presentation_profile().source != AuthoringMechanicAdapter.Source.UNAVAILABLE:
			printerr("FAIL: default_presentation_profile on %s illegally returned a value instead of UNAVAILABLE." % mech)
			quit(1)
			
		if adapter.required_assets().source != AuthoringMechanicAdapter.Source.UNAVAILABLE:
			printerr("FAIL: required_assets on %s illegally returned a value instead of UNAVAILABLE." % mech)
			quit(1)
			
		# Verificación Estructural
		var struct_res = adapter.build_structural_parameters(dummy_request, dummy_params)
		if struct_res.source != AuthoringMechanicAdapter.Source.DERIVED or struct_res.value.get("mock_param") != 100:
			printerr("FAIL: build_structural_parameters on %s failed to derive structural baseline." % mech)
			quit(1)
			
	print("[C6F2_AUTHORING_ADAPTER_CONTRACT_SUITE] PASS")
	quit(0)