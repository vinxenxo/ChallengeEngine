class_name ChallengeTimeline
extends TemporalCore

## C6-F0.3.4 — Challenge Timeline.
## Retains strict frozen phase semantics for F1/F2/F3 interactives.

var hook_frames: int = 0
var game_frames: int = 0
var reveal_frames: int = 0
var cta_frames: int = 0

func _init(video_cfg: Dictionary) -> void:
	super._init(int(video_cfg.get("fps", 60)))

	hook_frames = duration_to_frames(float(video_cfg.get("hook_duration", 2.0)))
	game_frames = duration_to_frames(float(video_cfg.get("game_duration", 7.0)))
	reveal_frames = duration_to_frames(float(video_cfg.get("reveal_duration", 0.0)))
	cta_frames = duration_to_frames(float(video_cfg.get("cta_duration", 2.0)))
	
	total_frames = hook_frames + game_frames + reveal_frames + cta_frames

func get_current_block() -> String:
	# Zero-frame phases are omitted seamlessly via ordered bounds checking.
	if _current_frame < hook_frames:
		return "HOOK"

	var game_end: int = hook_frames + game_frames
	if _current_frame < game_end:
		return "GAME"

	var reveal_end: int = game_end + reveal_frames
	if _current_frame < reveal_end:
		return "REVEAL"

	return "CTA"

func is_phase_enabled(phase: String) -> bool:
	match phase.to_upper():
		"HOOK":
			return hook_frames > 0
		"GAME":
			return game_frames > 0
		"REVEAL":
			return reveal_frames > 0
		"CTA":
			return cta_frames > 0
		_:
			return false

func get_game_index() -> int:
	if _current_frame < hook_frames:
		return -1
	return _current_frame - hook_frames