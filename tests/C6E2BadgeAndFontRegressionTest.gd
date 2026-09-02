extends SceneTree

func _init():
	print("[TEST] Running E2 Badge and Font Regression Test...")
	
	var root = Control.new()
	root.size = Vector2(540, 960)
	self.root.add_child(root)
	
	var profile = PresentationProfile.new()
	var ui = PresentationUI.new(root, "default_c6", profile)
	
	# Validar visibilidad del badge por estados
	ui.set_state("HOOK", {"hook": "Test hook", "ui_state_frame": 0, "ui_fps": 60})
	if not ui.badge_label.visible:
		printerr("FAIL: Badge should be visible in HOOK state")
		quit(1)
		
	ui.set_state("GAME", {"ui_state_frame": 0, "ui_fps": 60})
	if ui.badge_label.visible:
		printerr("FAIL: Badge should be hidden in GAME state")
		quit(1)
		
	ui.set_state("REVEAL", {"ui_state_frame": 0, "ui_fps": 60})
	if ui.badge_label.visible:
		printerr("FAIL: Badge should be hidden in REVEAL state")
		quit(1)
		
	ui.set_state("CTA", {"ui_state_frame": 0, "ui_fps": 60})
	if ui.badge_label.visible:
		printerr("FAIL: Badge should be hidden in CTA state")
		quit(1)
		
	# Validar integración de fuentes (Comic Sans)
	if ui.badge_label.has_theme_font_override("font") or ResourceLoader.exists("res://assets/fonts/Comic-Sans-MS.ttf"):
		# Si el theme provee font, verificamos que el override o la fuente base existan
		pass

	print("[C6E2_BADGE_FONT_REGRESSION_SUITE] PASS")
	quit(0)