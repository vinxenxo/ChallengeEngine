class_name ChooseMechanicIsolationTest
extends RefCounted

static func run_test() -> Dictionary:
	var mechanic = ChooseMechanic.new()
	var config = {
		"challenge_id": "CHALLENGE_008",
		"mechanic": "choose_v1",
		"generation": {"seed": 20260824, "rng_version": "2.0"},
		"difficulty": {
			"choose": {
				"options_count": 3,
				"positions": [[270, 960], [540, 960], [810, 960]]
			}
		}
	}
	
	mechanic.setup(config)
	if not mechanic._is_setup or mechanic._error_state != "OK":
		return {"success": false, "error": "Setup failed"}
		
	mechanic.prepare(420)
	if not mechanic._is_prepared or mechanic._error_state != "OK":
		return {"success": false, "error": "Prepare failed"}
		
	var sim_result = mechanic.simulate(420, 20260824, config)
	if sim_result == null or sim_result.error_state != "OK":
		return {"success": false, "error": "Simulation failed"}
		
	if sim_result.winning_frame < 0 or sim_result.frames.size() != 420:
		return {"success": false, "error": "Invalid frame output"}
		
	return {"success": true, "message": "ChooseMechanic isolation test passed successfully."}