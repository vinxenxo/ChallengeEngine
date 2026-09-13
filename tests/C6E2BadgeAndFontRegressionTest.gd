# res://tests/C6E2BadgeAndFontRegressionTest.gd
extends SceneTree

func _init():
	print("[TEST] Running E2 Badge and Font Regression Test...")
	
	var root = Control.new()
	root.size = Vector2(540, 960)
	self.root.add_child(root)
	
	var profile = PresentationProfile.new()
	var ui = PresentationUI.new(root, "default_c6", profile)
	var Binder = load("res://core/presentation/ChallengePresentationBinder.gd")
	
	# Validar visibilidad del badge por estados usando RenderModel
	var rm_hook = Binder.build_frame_render_model("HOOK", {"hook": "Test hook", "ui_state_frame": 0, "ui_fps": 60}, profile)
	ui.apply_render_model(rm_hook)
	if not ui.badge_label.visible:
		printerr("FAIL: Badge should be visible in HOOK state")
		quit(1)
		
	var rm_game = Binder.build_frame_render_model("GAME", {"ui_state_frame": 0, "ui_fps": 60}, profile)
	ui.apply_render_model(rm_game)
	if ui.badge_label.visible:
		printerr("FAIL: Badge should be hidden in GAME state")
		quit(1)
		
	var rm_reveal = Binder.build_frame_render_model("REVEAL", {"ui_state_frame": 0, "ui_fps": 60}, profile)
	ui.apply_render_model(rm_reveal)
	if ui.badge_label.visible:
		printerr("FAIL: Badge should be hidden in REVEAL state")
		quit(1)
		
	var rm_cta = Binder.build_frame_render_model("CTA", {"ui_state_frame": 0, "ui_fps": 60}, profile)
	ui.apply_render_model(rm_cta)
	if ui.badge_label.visible:
		printerr("FAIL: Badge should be hidden in CTA state")
		quit(1)

	print("[C6E2_BADGE_FONT_REGRESSION_SUITE] PASS")
	quit(0)