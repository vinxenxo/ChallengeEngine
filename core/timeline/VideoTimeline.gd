class_name VideoTimeline
extends RefCounted

var fps: int = 60
var hook_frames: int = 0
var game_frames: int = 0
var reveal_frames: int = 0
var cta_frames: int = 0
var total_frames: int = 0

var _current_frame: int = 0

func _init(video_cfg: Dictionary) -> void:
	fps = int(video_cfg.get("fps", 60))
	if fps <= 0:
		fps = 60

	hook_frames = duration_to_frames(float(video_cfg.get("hook_duration", 2.0)))
	game_frames = duration_to_frames(float(video_cfg.get("game_duration", 7.0)))
	reveal_frames = duration_to_frames(float(video_cfg.get("reveal_duration", 0.0))) # Fallback 0.0
	cta_frames = duration_to_frames(float(video_cfg.get("cta_duration", 2.0))) # Fallback original restaurado
	total_frames = hook_frames + game_frames + reveal_frames + cta_frames

func duration_to_frames(duration_seconds: float) -> int:
	return maxi(0, int(round(duration_seconds * float(fps))))

func advance() -> void:
	_current_frame += 1

func get_current_frame() -> int:
	return _current_frame

func is_finished() -> bool:
	return _current_frame >= total_frames

func get_current_block() -> String:
	if _current_frame < hook_frames:
		return "HOOK"
	if _current_frame < hook_frames + game_frames:
		return "GAME"
	if _current_frame < hook_frames + game_frames + reveal_frames:
		return "REVEAL"
	return "CTA"

func get_game_index() -> int:
	if _current_frame < hook_frames:
		return -1
	return _current_frame - hook_frames