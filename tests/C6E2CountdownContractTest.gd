# res://tests/C6E2CountdownContractTest.gd
extends SceneTree

# ============================================================
# C6-E2 Countdown Contract Test (Purified RenderModel based)
# ============================================================

func _init() -> void:
	print("[TEST] Running E2 Countdown Contract Test...")
	
	var CountdownComponent = load("res://core/presentation/components/CountdownComponent.gd")
	var ChallengePresentationBinder = load("res://core/presentation/ChallengePresentationBinder.gd")
	
	var countdown = CountdownComponent.new()
	
	var cases = [
		{"state": "HOOK", "frame": 0, "fps": 30, "expected_text": "3", "expected_visible": true},
		{"state": "HOOK", "frame": 15, "fps": 30, "expected_text": "3", "expected_visible": true},
		{"state": "HOOK", "frame": 30, "fps": 30, "expected_text": "2", "expected_visible": true},
		{"state": "HOOK", "frame": 45, "fps": 30, "expected_text": "2", "expected_visible": true},
		{"state": "HOOK", "frame": 60, "fps": 30, "expected_text": "1", "expected_visible": true},
		{"state": "HOOK", "frame": 90, "fps": 30, "expected_text": "", "expected_visible": false},
		{"state": "GAME", "frame": 0, "fps": 30, "expected_text": "", "expected_visible": false},
	]
	
	for i in range(cases.size()):
		var tc = cases[i]
		var content = {"ui_state_frame": tc["frame"], "ui_fps": tc["fps"]}
		
		# Llamada correcta con 3 argumentos
		var render_model = ChallengePresentationBinder.build_frame_render_model(
			tc["state"], content, null
		)
		
		countdown.apply_render_model(render_model)
		
		if countdown.visible != tc["expected_visible"] or countdown.text != tc["expected_text"]:
			push_error("FAIL: Case %d (state=%s, frame=%d, fps=%d) -> Expected text '%s' visible=%s | Got text '%s' visible=%s" % [
				i, tc["state"], tc["frame"], tc["fps"], 
				tc["expected_text"], str(tc["expected_visible"]), 
				countdown.text, str(countdown.visible)
			])
			quit(1)
			return
			
	print("[C6E2_COUNTDOWN_CONTRACT_SUITE] PASS")
	quit(0)