extends SceneTree

func _init():
	print("[TEST] Running C6E2ComponentSystemTest...")
	
	var root = Control.new()
	root.size = Vector2(540, 960)
	self.root.add_child(root)
	
	var profile = PresentationProfile.new()
	var ui = PresentationUI.new(root, "default_c6", profile)
	
	if ui.safe_area == null or ui.cta == null or ui.badge_label == null:
		printerr("FAIL: UI components failed to instantiate correctly")
		quit(1)
		
	print("[C6E2_COMPONENT_SYSTEM_SUITE] PASS")
	quit(0)