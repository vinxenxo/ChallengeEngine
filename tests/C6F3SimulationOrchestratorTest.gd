extends SceneTree

const ChallengeAuthoringRequest = preload("res://core/authoring/ChallengeAuthoringRequest.gd")
const ChallengeGenerator = preload("res://core/authoring/ChallengeGenerator.gd")
const AuthoringMechanicRegistry = preload("res://core/authoring/AuthoringMechanicRegistry.gd")
const ChallengeExecutionPipeline = preload("res://core/execution/ChallengeExecutionPipeline.gd")

func _init() -> void:
	print("[TEST] Running C6F3SimulationOrchestratorTest...")
	
	AuthoringMechanicRegistry.clear_registry()
	AuthoringMechanicRegistry.initialize_defaults()
	
	var failures: Array[String] = []
	
	# =========================================================
	# CASE A: Pilot Productive Generation & Execution E2E
	# =========================================================
	var req_res = ChallengeAuthoringRequest.create_from_dictionary({
		"mechanic": "pilot",
		"level": 50,
		"seed": 987654,
		"profile": "default_pilot",
		"overrides": {}
	})
	
	if not req_res.get("success", false):
		failures.append("Failed to create authoring request for pilot: " + str(req_res.get("errors")))
	else:
		var gen_res = ChallengeGenerator.generate(req_res.request)
		if not gen_res.get("success", false):
			failures.append("ChallengeGenerator failed for pilot: " + gen_res.get("error"))
		else:
			var canonical_v2 = gen_res.get("challenge")
			
			# Execute via Pipeline F3.1
			var exec_res = ChallengeExecutionPipeline.execute(canonical_v2)
			if not exec_res.get("success", false):
				failures.append("ChallengeExecutionPipeline failed: " + exec_res.get("error"))
			else:
				var sim_result = exec_res.get("simulation_result")
				if sim_result == null:
					failures.append("Pipeline succeeded but returned null SimulationResult.")
				else:
					if sim_result.frames.size() == 0:
						failures.append("SimulationResult contains 0 frames.")
						
					# =========================================================
					# CASE B: Deterministic V2 Execution Replay
					# =========================================================
					var exec_res_replay = ChallengeExecutionPipeline.execute(canonical_v2)
					var sim_replay = exec_res_replay.get("simulation_result")
					
					if sim_replay == null:
						failures.append("Replay simulation returned null.")
					else:
						if sim_result.winning_frame != sim_replay.winning_frame:
							failures.append("Determinism violation: winning_frame changed (%d != %d)" % [sim_result.winning_frame, sim_replay.winning_replay if "winning_replay" in sim_replay else sim_replay.winning_frame])
							
						if sim_result.frames.size() != sim_replay.frames.size():
							failures.append("Determinism violation: frame count changed.")
						else:
							for i in range(sim_result.frames.size()):
								var fa = sim_result.frames[i]
								var fb = sim_replay.frames[i]
								if not fa.position.is_equal_approx(fb.position) or not is_equal_approx(fa.rotation, fb.rotation) or not is_equal_approx(fa.opacity, fb.opacity):
									failures.append("Determinism violation: frame snapshot mismatch at index %d." % i)
									break
									
					# =========================================================
					# CASE C: RNG Isolation (Same seed gives identical output independently)
					# =========================================================
					var canonical_v2_alt = canonical_v2.duplicate(true)
					# Executing with a fresh pipeline call using the same seed structure
					var exec_res_alt = ChallengeExecutionPipeline.execute(canonical_v2_alt)
					var sim_alt = exec_res_alt.get("simulation_result")
					if sim_alt == null or sim_alt.winning_frame != sim_result.winning_frame:
						failures.append("RNG isolation test failed: isolated execution produced different outcome.")

	# ---------------------------------------------------------
	# Final Result
	# ---------------------------------------------------------
	if failures.is_empty():
		print("[C6F3_SIMULATION_ORCHESTRATOR_SUITE] PASS")
		quit(0)
		return
		
	for failure in failures:
		printerr("FAIL: " + failure)
		
	print("[C6F3_SIMULATION_ORCHESTRATOR_SUITE] FAIL count=%d" % failures.size())
	quit(1)