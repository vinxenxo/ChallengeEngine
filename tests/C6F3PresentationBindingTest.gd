# res://tests/C6F3PresentationBindingTest.gd
extends SceneTree

const ChallengeAuthoringRequest = preload("res://core/authoring/ChallengeAuthoringRequest.gd")
const ChallengeGenerator = preload("res://core/authoring/ChallengeGenerator.gd")
const AuthoringMechanicRegistry = preload("res://core/authoring/AuthoringMechanicRegistry.gd")
const ChallengeExecutionPipeline = preload("res://core/execution/ChallengeExecutionPipeline.gd")
const ChallengeTimelineBuilder = preload("res://core/execution/ChallengeTimelineBuilder.gd")
const ChallengePresentationBinder = preload("res://core/presentation/ChallengePresentationBinder.gd")
const PresentationBindingResult = preload("res://core/presentation/PresentationBindingResult.gd")

func _init() -> void:
	print("[TEST] Running C6F3PresentationBindingTest...")
	
	AuthoringMechanicRegistry.clear_registry()
	AuthoringMechanicRegistry.initialize_defaults()
	
	var failures: Array[String] = []
	
	var req_res = ChallengeAuthoringRequest.create_from_dictionary({
		"mechanic": "pilot",
		"level": 50,
		"seed": 554433,
		"profile": "default_pilot",
		"overrides": {}
	})
	
	if not req_res.get("success", false):
		failures.append("Failed to create base request for pilot.")
		_report_and_quit(failures)
		return
		
	var gen_res = ChallengeGenerator.generate(req_res.request)
	if not gen_res.get("success", false):
		failures.append("ChallengeGenerator failed.")
		_report_and_quit(failures)
		return
		
	var canonical_v2 = gen_res.get("challenge")
	
	# Inject mock physical assets pass-through for testing hybrid legacy/V2 compatibility
	canonical_v2["assets"] = {
		"background_path": "res://assets/mock_bg.png",
		"target_path": "res://assets/mock_target.png",
		"object_path": "res://assets/mock_object.png"
	}
	
	var exec_res = ChallengeExecutionPipeline.execute(canonical_v2)
	if not exec_res.get("success", false):
		failures.append("ExecutionPipeline failed.")
		_report_and_quit(failures)
		return
	var sim_result = exec_res.get("simulation_result")
	
	var timeline_res = ChallengeTimelineBuilder.build(canonical_v2, sim_result)
	if not timeline_res.success:
		failures.append("TimelineBuilder failed.")
		_report_and_quit(failures)
		return
	var timeline = timeline_res.timeline

	# Case A, B, C, D: Complete Binding & Isolation Checks
	var binding_res = ChallengePresentationBinder.bind(canonical_v2, timeline, sim_result)
	if not binding_res.success:
		failures.append("ChallengePresentationBinder failed on valid pilot input: " + binding_res.error)
	else:
		if binding_res.timeline != timeline:
			failures.append("Timeline isolation violation: binder did not preserve the exact timeline instance.")
			
		if binding_res.winning_frame != sim_result.winning_frame:
			failures.append("Winning frame mismatch: %d != %d" % [binding_res.winning_frame, sim_result.winning_frame])
			
		if binding_res.asset_family_meta.get("family_id", "") != "fam_001":
			failures.append("Asset family meta family_id mismatch.")
		
		if binding_res.presentation_profile == null or binding_res.presentation_render_model.is_empty():
			failures.append("Presentation profile or render model failed to materialize.")

		if binding_res.physical_assets.get("background_path", "") == "":
			failures.append("Physical asset background_path was not preserved.")

		if binding_res.physical_assets.get("target_path", "") == "":
			failures.append("Physical asset target_path was not preserved.")

		if binding_res.physical_assets.get("object_path", "") == "":
			failures.append("Physical asset object_path was not preserved.")

	# Case E: Audio Missing (Optional pass-through, success true)
	var v2_no_audio = canonical_v2.duplicate(true)
	v2_no_audio.erase("audio")
	var binding_no_audio = ChallengePresentationBinder.bind(v2_no_audio, timeline, sim_result)
	if not binding_no_audio.success:
		failures.append("Binder failed when audio metadata was absent.")
	elif not binding_no_audio.audio_profile.is_empty():
		failures.append("Audio profile expected to be empty when audio metadata is absent.")

	# Case F: Fail-Closed Checks
	var v2_no_pres = canonical_v2.duplicate(true)
	v2_no_pres.erase("presentation")
	var res_no_pres = ChallengePresentationBinder.bind(v2_no_pres, timeline, sim_result)
	if res_no_pres.success:
		failures.append("Fail-closed violation: accepted missing presentation.")

	# Presentation ID empty check (PresentationProfile dynamically materializes non-empty strings)
	var v2_empty_pres = canonical_v2.duplicate(true)
	v2_empty_pres["presentation"] = "   "
	var res_empty_pres = ChallengePresentationBinder.bind(v2_empty_pres, timeline, sim_result)
	if res_empty_pres.success:
		failures.append("Fail-closed violation: accepted whitespace presentation ID.")

	var v2_no_assets = canonical_v2.duplicate(true)
	v2_no_assets.erase("asset_family")
	var res_no_assets = ChallengePresentationBinder.bind(v2_no_assets, timeline, sim_result)
	if res_no_assets.success:
		failures.append("Fail-closed violation: accepted missing asset_family.")

	var res_null_timeline = ChallengePresentationBinder.bind(canonical_v2, null, sim_result)
	if res_null_timeline.success:
		failures.append("Fail-closed violation: accepted null timeline.")

	var res_null_sim = ChallengePresentationBinder.bind(canonical_v2, timeline, null)
	if res_null_sim.success:
		failures.append("Fail-closed violation: accepted null simulation result.")

	_report_and_quit(failures)

func _report_and_quit(failures: Array[String]) -> void:
	if failures.is_empty():
		print("[C6F3_PRESENTATION_BINDING_SUITE] PASS")
		quit(0)
		return
		
	for failure in failures:
		printerr("FAIL: " + failure)
		
	print("[C6F3_PRESENTATION_BINDING_SUITE] FAIL count=%d" % failures.size())
	quit(1)