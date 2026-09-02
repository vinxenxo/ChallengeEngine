extends SceneTree

func _init():
	print("[TEST] Running E2 Countdown Contract Test...")
	
	var profile = PresentationProfile.new()
	var countdown = CountdownComponent.new()
	countdown.apply_profile(profile)
	
	# Matriz de validación (Estado, Frame, FPS Esperado, Texto Esperado, Visible)
	var test_cases = [
		{"state": "HOOK", "frame": 0,   "fps": 60, "text": "3", "visible": true},
		{"state": "HOOK", "frame": 59,  "fps": 60, "text": "3", "visible": true},
		{"state": "HOOK", "frame": 60,  "fps": 60, "text": "2", "visible": true},
		{"state": "HOOK", "frame": 119, "fps": 60, "text": "2", "visible": true},
		{"state": "HOOK", "frame": 120, "fps": 60, "text": "1", "visible": true},
		{"state": "HOOK", "frame": 179, "fps": 60, "text": "1", "visible": true},
		{"state": "HOOK", "frame": 180, "fps": 60, "text": "",  "visible": false},
		{"state": "GAME", "frame": 0,   "fps": 60, "text": "",  "visible": false},
		{"state": "REVEAL", "frame": 0, "fps": 60, "text": "",  "visible": false},
		{"state": "CTA", "frame": 0,    "fps": 60, "text": "",  "visible": false},
		# Variación a 30 FPS
		{"state": "HOOK", "frame": 0,   "fps": 30, "text": "3", "visible": true},
		{"state": "HOOK", "frame": 30,  "fps": 30, "text": "2", "visible": true},
		{"state": "HOOK", "frame": 60,  "fps": 30, "text": "1", "visible": true},
		{"state": "HOOK", "frame": 90,  "fps": 30, "text": "",  "visible": false},
	]
	
	for i in range(test_cases.size()):
		var tc = test_cases[i]
		var content = {"ui_state_frame": tc["frame"], "ui_fps": tc["fps"]}
		countdown.update_from_state(tc["state"], content)
		
		if countdown.visible != tc["visible"] or countdown.text != tc["text"]:
			printerr("FAIL: Case ", i, " (state=", tc["state"], ", frame=", tc["frame"], ", fps=", tc["fps"], ") -> Expected text '", tc["text"], "' visible=", tc["visible"], " | Got text '", countdown.text, "' visible=", countdown.visible)
			quit(1)
			
	print("[C6E2_COUNTDOWN_CONTRACT_SUITE] PASS")
	quit(0)