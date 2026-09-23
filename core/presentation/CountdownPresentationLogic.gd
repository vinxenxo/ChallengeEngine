# res://core/presentation/CountdownPresentationLogic.gd
class_name CountdownPresentationLogic
extends RefCounted

## C11-C 2.4.0 — Shared 3-second countdown presentation logic.
## Extracted from the established ChallengePresentationBinder behavior.
## Presentation-only: never owns simulation, RNG, timeline or mechanic truth.

const COUNTDOWN_SECONDS: float = 3.0

static func resolve(active: bool, frame_index: int, fps: int) -> Dictionary:
	var visible: bool = false
	var value: String = ""
	if active:
		var safe_fps: int = maxi(1, fps)
		var safe_frame: int = maxi(0, frame_index)
		if safe_frame < safe_fps:
			visible = true
			value = "3"
		elif safe_frame < safe_fps * 2:
			visible = true
			value = "2"
		elif safe_frame < safe_fps * 3:
			visible = true
			value = "1"
	return {"countdown_visible": visible, "countdown_value": value}

static func apply_to_render_model(model: Dictionary, active: bool, frame_index: int, fps: int) -> Dictionary:
	var result: Dictionary = model
	var countdown: Dictionary = resolve(active, frame_index, fps)
	result["countdown_visible"] = bool(countdown.get("countdown_visible", false))
	result["countdown_value"] = str(countdown.get("countdown_value", ""))
	return result
