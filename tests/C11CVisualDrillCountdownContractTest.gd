extends SceneTree

## C11-C 2.4.0 — Shared Visual Drill countdown contract.
## Verifies reuse of the historical Challenge 3/2/1 presentation behavior without duplicating UI.

const CountdownPresentationLogic = preload("res://core/presentation/CountdownPresentationLogic.gd")
const VisualDrillPresentationBinder = preload("res://core/presentation/VisualDrillPresentationBinder.gd")
const PresentationProfile = preload("res://core/presentation/PresentationProfile.gd")

var failures: Array[String] = []

func _initialize() -> void:
	_test_countdown_logic()
	_test_challenge_compatibility()
	_test_visual_drill_binder()
	_test_canonical_duration_contract()
	_conclude()

func _test_countdown_logic() -> void:
	var cases: Array[Dictionary] = [
		{"frame": 0, "value": "3", "visible": true},
		{"frame": 29, "value": "3", "visible": true},
		{"frame": 30, "value": "2", "visible": true},
		{"frame": 59, "value": "2", "visible": true},
		{"frame": 60, "value": "1", "visible": true},
		{"frame": 89, "value": "1", "visible": true},
		{"frame": 90, "value": "", "visible": false}
	]
	for tc: Dictionary in cases:
		var state: Dictionary = CountdownPresentationLogic.resolve(true, int(tc["frame"]), 30)
		_assert(bool(state.get("countdown_visible", false)) == bool(tc["visible"]), "Countdown visibility mismatch at frame %d." % int(tc["frame"]))
		_assert(str(state.get("countdown_value", "")) == str(tc["value"]), "Countdown value mismatch at frame %d." % int(tc["frame"]))

func _test_challenge_compatibility() -> void:
	var challenge_binder = load("res://core/presentation/ChallengePresentationBinder.gd")
	var model_3: Dictionary = challenge_binder.build_frame_render_model("HOOK", {"ui_state_frame": 0, "ui_fps": 30}, null)
	var model_2: Dictionary = challenge_binder.build_frame_render_model("HOOK", {"ui_state_frame": 30, "ui_fps": 30}, null)
	var model_1: Dictionary = challenge_binder.build_frame_render_model("HOOK", {"ui_state_frame": 60, "ui_fps": 30}, null)
	var model_off: Dictionary = challenge_binder.build_frame_render_model("HOOK", {"ui_state_frame": 90, "ui_fps": 30}, null)
	_assert(str(model_3.get("countdown_value", "")) == "3", "Challenge countdown compatibility failed at 3.")
	_assert(str(model_2.get("countdown_value", "")) == "2", "Challenge countdown compatibility failed at 2.")
	_assert(str(model_1.get("countdown_value", "")) == "1", "Challenge countdown compatibility failed at 1.")
	_assert(not bool(model_off.get("countdown_visible", true)), "Challenge countdown compatibility failed to hide at frame 90.")

func _test_visual_drill_binder() -> void:
	var profile := PresentationProfile.new()
	var binder := VisualDrillPresentationBinder.new()
	binder.set_definition_context({
		"kind": "visual_drill",
		"subtype": "tracking",
		"seed": 12345,
		"payload": {
			"duration": 21.0,
			"fps": 30,
			"exercise_parameters": {"difficulty_tier": 2, "speed_multiplier": 1.0}
		}
	})
	var frame: Dictionary = {
		"frame_index": 0,
		"payload": {"generator_type": "tracking", "parameters": {"tracking_variant": 0.25}, "target_states": [], "distractor_states": [], "trajectory_state": {}, "task_state": {}}
	}
	var pre_roll: Dictionary = binder.bind_frame(frame, profile, "PRE_ROLL", 0, 30)
	_assert(bool(pre_roll.get("countdown_visible", false)), "Visual Drill countdown must be visible during PRE_ROLL.")
	_assert(str(pre_roll.get("countdown_value", "")) == "3", "Visual Drill countdown must begin at 3.")
	var editorial: Dictionary = pre_roll.get("editorial", {})
	_assert(bool(editorial.get("intro_active", false)), "Visual Drill intro text must be active during countdown.")
	_assert(str(editorial.get("intro_text", "")).find("SEGUIR EL OBJETO") >= 0, "Tracking intro copy missing.")

	var game: Dictionary = binder.bind_frame(frame, profile, "GAME", 90, 30)
	_assert(not bool(game.get("countdown_visible", true)), "Visual Drill countdown must hide when gameplay starts.")
	var game_editorial: Dictionary = game.get("editorial", {})
	_assert(not bool(game_editorial.get("intro_active", true)), "Tracking intro must disappear at gameplay start.")
	_assert(bool(game_editorial.get("matrix_enabled", false)), "Visual Drill Matrix must resume during gameplay.")

func _test_canonical_duration_contract() -> void:
	var paths: Array[String] = [
		"res://definitions/visual_drill_tracking_canonical.json",
		"res://definitions/visual_drill_saccade_canonical.json",
		"res://definitions/visual_drill_pursuit_canonical.json",
		"res://definitions/visual_drill_peripheral_scan_canonical.json"
	]
	for path: String in paths:
		var parsed = JSON.parse_string(FileAccess.get_file_as_string(path))
		_assert(parsed is Dictionary, "%s must contain a valid JSON object." % path)
		if parsed is Dictionary:
			var payload: Dictionary = parsed.get("payload", {})
			var subtype: String = str(parsed.get("subtype", ""))
			var expected_gameplay: float = 21.0 if subtype == "tracking" else 17.0
			var expected_frames: int = int(round(expected_gameplay * 30.0))
			var total_seconds: float = expected_gameplay + CountdownPresentationLogic.COUNTDOWN_SECONDS
			_assert(is_equal_approx(float(payload.get("duration", 0.0)), expected_gameplay), "%s gameplay duration mismatch." % path)
			_assert(int(payload.get("frame_count", 0)) == expected_frames, "%s gameplay frame_count mismatch." % path)
			_assert(total_seconds >= 20.0 and total_seconds <= 30.0, "%s total presentation duration must be within 20-30s." % path)

func _assert(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)

func _conclude() -> void:
	if failures.is_empty():
		print("[C11C_VISUAL_DRILL_COUNTDOWN_CONTRACT_SUITE] PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		print("[C11C_VISUAL_DRILL_COUNTDOWN_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
		quit(1)
