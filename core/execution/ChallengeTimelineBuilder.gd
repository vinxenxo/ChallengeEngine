class_name ChallengeTimelineBuilder
extends RefCounted

const VideoTimeline = preload("res://core/timeline/VideoTimeline.gd")
const WinningFrameDetector = preload("res://core/validation/WinningFrameDetector.gd")
const VideoProfileRegistry = preload("res://core/authoring/VideoProfileRegistry.gd")

class BuildResult:
	var success: bool = false
	var error: String = ""
	var timeline: VideoTimeline = null
	var winning_frame: int = -1

static func build(canonical_v2: Dictionary, simulation_result: SimulationResult) -> BuildResult:
	var result = BuildResult.new()
	
	if simulation_result == null:
		result.error = "TimelineBuilder received null SimulationResult."
		return result
		
	if simulation_result.error_state != "OK":
		result.error = "Cannot build timeline for failed simulation (error_state: %s)." % simulation_result.error_state
		return result

	# 1. Delegate winning-frame truth to WinningFrameDetector
	WinningFrameDetector.analyze_and_score(simulation_result)
	if simulation_result.error_state != "OK":
		result.error = "WinningFrameDetector failed with error state: %s" % simulation_result.error_state
		return result

	# 2. Strict validation of video profile binding in Canonical V2
	if not canonical_v2.has("video"):
		result.error = "TimelineBuilder missing video profile binding."
		return result

	var video_binding = canonical_v2.get("video", "")
	var video_profile: Dictionary = {}
	var video_profile_label := "inline canonical V2 video"
	if video_binding is Dictionary:
		video_profile = _normalize_inline_canonical_video(video_binding)
	else:
		var video_profile_id: String = str(video_binding)
		if video_profile_id.strip_edges().is_empty():
			result.error = "TimelineBuilder received empty video profile id."
			return result
		video_profile_label = video_profile_id
		video_profile = VideoProfileRegistry.get_profile(video_profile_id)

	if video_profile.is_empty():
		result.error = "TimelineBuilder failed to resolve video profile binding: '%s'" % video_profile_label
		return result

	# 3. Extract exact temporal configuration from the sovereign profile without synthetic defaults
	if not video_profile.has("fps"):
		result.error = "Video profile '%s' missing mandatory 'fps'." % video_profile_label
		return result

	var phases: Dictionary = video_profile.get("phases", {})
	if not phases.has("game_duration"):
		result.error = "Video profile '%s' phases missing mandatory 'game_duration'." % video_profile_label
		return result

	var timeline_config := {
		"fps": video_profile.get("fps"),
		"hook_duration": phases.get("hook_duration", 0.0),
		"game_duration": phases.get("game_duration"),
		"reveal_duration": phases.get("reveal_duration", 0.0),
		"cta_duration": phases.get("cta_duration", 0.0)
	}

	# 4. Construct the VideoTimeline matching the profile configuration contract
	var timeline = VideoTimeline.new(timeline_config)
	
	result.success = true
	result.timeline = timeline
	result.winning_frame = simulation_result.winning_frame # Sovereign local index of GAME
	return result

static func _normalize_inline_canonical_video(video: Dictionary) -> Dictionary:
	# F4.4 Phase 1: adapt the flat Canonical V2 video contract to the
	# internal VideoProfile temporal shape without mutating the source.
	if not video.has("fps") or not video.has("game_duration"):
		return {}

	return {
		"profile_id": "__inline_canonical_v2__",
		"fps": int(round(float(video.get("fps", 30)))),
		"phases": {
			"hook_duration": float(video.get("hook_duration", 0.0)),
			"game_duration": float(video.get("game_duration")),
			"reveal_duration": float(video.get("reveal_duration", 0.0)),
			"cta_duration": float(video.get("cta_duration", 0.0))
		}
	}

