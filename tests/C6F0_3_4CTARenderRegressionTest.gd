extends SceneTree

const Binder = preload("res://core/presentation/ChallengePresentationBinder.gd")
const PresentationProfile = preload("res://core/presentation/PresentationProfile.gd")
const PresentationUI = preload("res://core/presentation/PresentationUI.gd")

func _init() -> void:
	print("[TEST] Running C6F0_3_4CTARenderRegressionTest...")
	var failures := 0

	var profile := PresentationProfile.new()
	var render_model := Binder.build_frame_render_model("CTA", {"ui_state_frame": 0, "ui_fps": 60}, profile)
	if str(render_model.get("cta_main", "")) != "LINK IN BIO":
		print("[FAIL] CTA main text contract was not restored: '%s'." % str(render_model.get("cta_main", "")))
		failures += 1
	else:
		print("[PASS] CTA main default restored")

	if str(render_model.get("cta_sub", "")) != "¡Juega ahora!":
		print("[FAIL] CTA sub text contract was not restored: '%s'." % str(render_model.get("cta_sub", "")))
		failures += 1
	else:
		print("[PASS] CTA sub default restored")

	var root := Control.new()
	root.size = Vector2(540, 960)
	get_root().add_child(root)
	var ui := PresentationUI.new(root, "default_c6", profile)
	ui.apply_render_model(render_model)
	if str(ui.cta.label_main.text) != "LINK IN BIO":
		print("[FAIL] CTA main label text mismatch: '%s'." % str(ui.cta.label_main.text))
		failures += 1
	else:
		print("[PASS] CTA main label restored")

	if str(ui.cta.label_sub.text) != "¡Juega ahora!":
		print("[FAIL] CTA sub label text mismatch: '%s'." % str(ui.cta.label_sub.text))
		failures += 1
	else:
		print("[PASS] CTA sub label restored")

	if not bool(render_model.get("cta_visible", false)):
		print("[FAIL] CTA visibility flag mismatch.")
		failures += 1
	else:
		print("[PASS] timeline/presentation CTA visibility contract")

	if failures == 0:
		print("[C6F0_3_4_CTA_RENDER_REGRESSION_SUITE] PASS")
		quit(0)
	else:
		print("[C6F0_3_4_CTA_RENDER_REGRESSION_SUITE] FAIL failures=%d" % failures)
		quit(1)
