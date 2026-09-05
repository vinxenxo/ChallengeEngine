extends SceneTree

const ChallengeAuthoringRequest = preload("res://core/authoring/ChallengeAuthoringRequest.gd")
const ChallengeGenerator = preload("res://core/authoring/ChallengeGenerator.gd")
const AuthoringMechanicRegistry = preload("res://core/authoring/AuthoringMechanicRegistry.gd")
const ChallengeExecutionPipeline = preload("res://core/execution/ChallengeExecutionPipeline.gd")
const ChallengeTimelineBuilder = preload("res://core/execution/ChallengeTimelineBuilder.gd")
const VideoProfileRegistry = preload("res://core/authoring/VideoProfileRegistry.gd")

func _init() -> void:
	print("[TEST] Running C6F3TimelineBuilderTest...")
	
	AuthoringMechanicRegistry.clear_registry()
	AuthoringMechanicRegistry.initialize_defaults()
	VideoProfileRegistry.clear_cache()
	
	var failures: Array[String] = []
	
	# 1. Authoring Request & Generation (Pilot)
	var req_res = ChallengeAuthoringRequest.create_from_dictionary({
		"mechanic": "pilot",
		"level": 50,
		"seed": 112233,
		"profile": "default_pilot",
		"overrides": {}
	})
	
	if not req_res.get("success", false):
		failures.append("Failed to create authoring request.")
	else:
		var gen_res = ChallengeGenerator.generate(req_res.request)
		if not gen_res.get("success", false):
			failures.append("ChallengeGenerator failed.")
		else:
			var canonical_v2 = gen_res.get("challenge")
			
			# 2. Execution Pipeline (F3.1)
			var exec_res = ChallengeExecutionPipeline.execute(canonical_v2)
			if not exec_res.get("success", false):
				failures.append("ExecutionPipeline failed: " + exec_res.get("error"))
			else:
				var sim_result = exec_res.get("simulation_result")
				
				# 3. Timeline Builder (F3.2)
				var build_res = ChallengeTimelineBuilder.build(canonical_v2, sim_result)
				if not build_res.success:
					failures.append("ChallengeTimelineBuilder failed: " + build_res.error)
				else:
					var timeline = build_res.timeline
					if timeline == null:
						failures.append("TimelineBuilder returned null timeline.")
					else:
						# Verify structural profile binding coherence
						var video_profile_id = str(canonical_v2.get("video", ""))
						var video_profile = VideoProfileRegistry.get_profile(video_profile_id)
						
						if timeline.fps != int(video_profile.get("fps", 60)):
							failures.append("Timeline fps does not match VideoProfile fps.")
							
						# Check total_frames consistency assert
						var expected_total = timeline.hook_frames + timeline.game_frames + timeline.reveal_frames + timeline.cta_frames
						if timeline.total_frames != expected_total:
							failures.append("Timeline total_frames is inconsistent (%d != %d)." % [timeline.total_frames, expected_total])
							
						if timeline.game_frames <= 0:
							failures.append("Timeline has zero or negative game_frames.")
							
						if build_res.winning_frame < 0:
							failures.append("Winning frame detector yielded invalid index (< 0).")
							
						if build_res.winning_frame >= timeline.game_frames:
							failures.append("Winning frame index exceeds active game duration frames (local GAME boundary check).")

	if failures.is_empty():
		print("[C6F3_TIMELINE_BUILDER_SUITE] PASS")
		quit(0)
		return
		
	for failure in failures:
		printerr("FAIL: " + failure)
		
	print("[C6F3_TIMELINE_BUILDER_SUITE] FAIL count=%d" % failures.size())
	quit(1)