# res://core/runtime/ChallengeRuntime.gd
class_name ChallengeRuntime
extends ContentRuntime

## C6-F0.3.5 — Challenge runtime boundary adapter.
## Delegates entirely to the existing sovereign effective Challenge pipeline.
## This class exposes only a render-ready frame stream and never surfaces
## SimulationResult, WinningFrameDetector, RNG, or ChallengeMechanic through
## the common ContentRuntime contract.

const ChallengeRuntimeBridge = preload("res://core/execution/ChallengeRuntimeBridge.gd")

func _initialize_domain(definition: Dictionary) -> bool:
	if kind != "challenge":
		return _fail("CHALLENGE_KIND_MISMATCH")
	if not definition.has("definition") or not definition["definition"] is Dictionary:
		return _fail("CHALLENGE_DEFINITION_MISSING")
	var challenge_definition: Dictionary = definition["definition"].duplicate(true)

	var runtime_result: Dictionary = ChallengeRuntimeBridge.run_effective_pipeline(challenge_definition)
	if not bool(runtime_result.get("success", false)):
		return _fail("CHALLENGE_SOVEREIGN_RUNTIME_FAILED:%s" % str(runtime_result.get("error_code", "UNKNOWN")))

	var context = runtime_result.get("context")
	if context == null or context.simulation_result == null or context.timeline == null:
		return _fail("CHALLENGE_RUNTIME_CONTEXT_INCOMPLETE")

	var result: SimulationResult = context.simulation_result
	var timeline: VideoTimeline = context.timeline
	fps = timeline.fps
	var stream := RenderedFrameStream.new(kind, subtype, fps)
	for absolute_index in range(timeline.total_frames):
		var phase := _phase_for_absolute_frame(timeline, absolute_index)
		var payload_frame = null
		var game_index := absolute_index - timeline.hook_frames
		if phase == "GAME" and game_index >= 0 and game_index < result.frames.size():
			payload_frame = result.frames[game_index]
		var frame := {
			"frame_index": absolute_index,
			"payload": {
				"domain": "challenge",
				"phase": phase,
				"game_index": game_index if phase == "GAME" else -1,
				"snapshot": payload_frame
			}
		}
		if not stream.append_frame(frame):
			return _fail("CHALLENGE_FRAME_STREAM_APPEND_FAILED")

	return _mark_initialized(stream)

static func _phase_for_absolute_frame(timeline: VideoTimeline, absolute_frame: int) -> String:
	if absolute_frame < timeline.hook_frames:
		return "HOOK"
	var game_end := timeline.hook_frames + timeline.game_frames
	if absolute_frame < game_end:
		return "GAME"
	var reveal_end := game_end + timeline.reveal_frames
	if absolute_frame < reveal_end:
		return "REVEAL"
	return "CTA"
