# res://tests/C6E2ComponentLayoutValidationTest.gd
extends SceneTree

func _init():
	print("[TEST] Running E2 Component Layout Validation...")
	
	var root = Control.new()
	root.size = Vector2(540, 960)
	root.name = "Root"
	self.root.add_child(root)
	
	# -- PROFILE A (Márgenes estándar 40x80) --
	var cfg_a = {
		"presentation": {
			"profile_overrides": {
				"safe_area": {"top": 80.0, "bottom": 120.0, "left": 40.0, "right": 40.0}
			}
		}
	}
	var profile_a = PresentationProfile.from_challenge(cfg_a)
	var ui_a = PresentationUI.new(root, "default_c6", profile_a)
	
	await self.process_frame
	
	var safe_rect_a = ui_a.safe_area.get_global_rect()
	var badge_rect_a = ui_a.badge_label.get_global_rect()
	
	if not safe_rect_a.encloses(badge_rect_a):
		printerr("FAIL: Profile A - Badge no está encerrado en SafeArea")
		quit(1)
		
	for child in root.get_children():
		child.queue_free()
	await self.process_frame
	
	# -- PROFILE B (Márgenes extremos) --
	var cfg_b = {
		"presentation": {
			"profile_overrides": {
				"safe_area": {"top": 200.0, "bottom": 250.0, "left": 100.0, "right": 100.0}
			}
		}
	}
	var profile_b = PresentationProfile.from_challenge(cfg_b)
	var ui_b = PresentationUI.new(root, "default_c6", profile_b)
	ui_b.cta.visible = true
	
	await self.process_frame
	
	var safe_rect_b = ui_b.safe_area.get_global_rect()
	var badge_rect_b = ui_b.badge_label.get_global_rect()
	var cta_rect_b = ui_b.cta.get_global_rect()
	var gameplay_rect_b = ui_b.gameplay_envelope.get_global_rect()
	
	if not safe_rect_b.encloses(badge_rect_b):
		printerr("FAIL: Profile B - Badge excedió SafeArea extrema")
		quit(1)
		
	if not safe_rect_b.encloses(cta_rect_b):
		printerr("FAIL: Profile B - CTA excedió SafeArea extrema")
		quit(1)
		
	if not safe_rect_b.encloses(gameplay_rect_b):
		printerr("FAIL: Profile B - Gameplay Envelope rompió los límites")
		quit(1)
		
	print("[C6E2_COMPONENT_LAYOUT_VALIDATION_SUITE] PASS")
	quit(0)