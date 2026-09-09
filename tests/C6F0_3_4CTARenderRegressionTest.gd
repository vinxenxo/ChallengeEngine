extends SceneTree

# ============================================================
# C6-F0.3.4 CTA Render Regression Test
# Guards the certified E2 CTA presentation contract while verifying
# the extracted ChallengeTimeline still reaches its terminal CTA frame.
# ============================================================

const VideoTimeline = preload("res://core/timeline/VideoTimeline.gd")
const PresentationProfile = preload("res://core/presentation/PresentationProfile.gd")
const PresentationUI = preload("res://core/presentation/PresentationUI.gd")
const Binder = preload("res://core/presentation/ChallengePresentationBinder.gd")

var failures: int = 0

func _init() -> void:
	print("[TEST] Running C6F0_3_4CTARenderRegressionTest...")

	_test_challenge_timeline_reaches_cta()
	_test_render_model_restores_cta_payload()
	_test_presentation_ui_renders_cta_text()

	if failures == 0:
		print("[C6F0_3_4_CTA_RENDER_REGRESSION_SUITE] PASS")
		quit(0)
	else:
		push_error("[C6F0_3_4_CTA_RENDER_REGRESSION_SUITE] FAIL failures=%d" % failures)
		quit(1)

func _test_challenge_timeline_reaches_cta() -> void:
	var timeline := VideoTimeline.new({
		"fps": 60,
		"hook_duration": 0.0,
		"game_duration": 7.0,
		"reveal_duration": 0.0,
		"cta_duration": 2.0
	})

	if timeline.cta_frames != 120:
		_fail("Expected CTA to contain 120 frames, got %d." % timeline.cta_frames)
		return

	if timeline.total_frames != 540:
		_fail("Expected total timeline to contain 540 frames, got %d." % timeline.total_frames)
		return

	timeline._current_frame = timeline.total_frames - 1
	if timeline.get_current_block() != "CTA":
		_fail("Final timeline frame must resolve to CTA, got '%s'." % timeline.get_current_block())
	else:
		print("[PASS] _test_challenge_timeline_reaches_cta")

func _test_render_model_restores_cta_payload() -> void:
	var profile := PresentationProfile.new()
	var content := {
		"cta": "LEGACY CONTENT CTA",
		"ui_state_frame": 0,
		"ui_fps": 60
	}
	var model := Binder.build_frame_render_model("CTA", content, profile)

	if not bool(model.get("cta_visible", false)):
		_fail("CTA render model must mark CTA visible in CTA state.")
		return
	if str(model.get("cta_main", "")) != "LINK IN BIO":
		_fail("CTA main text contract was not restored: '%s'." % str(model.get("cta_main", "")))
		return
	if str(model.get("cta_sub", "")) != "¡Juega ahora!":
		_fail("CTA sub text contract was not restored: '%s'." % str(model.get("cta_sub", "")))
		return

	print("[PASS] _test_render_model_restores_cta_payload")

func _test_presentation_ui_renders_cta_text() -> void:
	var root := Control.new()
	root.size = Vector2(540, 960)
	get_root().add_child(root)

	var profile := PresentationProfile.new()
	var ui := PresentationUI.new(root, "default_c6", profile)
	var model := Binder.build_frame_render_model("CTA", {
		"ui_state_frame": 0,
		"ui_fps": 60
	}, profile)
	ui.apply_render_model(model)

	if not ui.cta.visible:
		_fail("PresentationUI CTA component must be visible in CTA state.")
	elif ui.cta.label_main.text != "LINK IN BIO":
		_fail("CTA main label text mismatch: '%s'." % ui.cta.label_main.text)
	elif ui.cta.label_sub.text != "¡Juega ahora!":
		_fail("CTA sub label text mismatch: '%s'." % ui.cta.label_sub.text)
	else:
		print("[PASS] _test_presentation_ui_renders_cta_text")

	root.queue_free()

func _fail(message: String) -> void:
	failures += 1
	print("[FAIL] " + message)
