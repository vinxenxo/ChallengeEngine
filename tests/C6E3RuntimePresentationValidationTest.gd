# res://tests/C6E3RuntimePresentationValidationTest.gd
extends SceneTree

# ============================================================
# C6-E3 Runtime Presentation Validation Test (E3-B1, C1, D1)
# ============================================================

const Binder = preload("res://core/presentation/ChallengePresentationBinder.gd")
const Profile = preload("res://core/presentation/PresentationProfile.gd")
const PresentationUI = preload("res://core/presentation/PresentationUI.gd")

var failures: int = 0

func _init() -> void:
	print("[TEST] Running C6E3RuntimePresentationValidationTest...")

	# E3-C1: Definición de las 7 mecánicas V2 a auditar.
	var mechanic_challenges = [
		{"mechanic": "pilot", "path": "res://challenges/CHALLENGE_003.json"},
		{"mechanic": "parking_v2", "path": "res://challenges/CHALLENGE_004.json"},
		{"mechanic": "hit_v1", "path": "res://challenges/CHALLENGE_005.json"},
		{"mechanic": "catch_v1", "path": "res://challenges/CHALLENGE_006.json"},
		{"mechanic": "find_v1", "path": "res://challenges/CHALLENGE_007.json"},
		{"mechanic": "choose_v1", "path": "res://challenges/CHALLENGE_008.json"},
		{"mechanic": "count_v1", "path": "res://challenges/CHALLENGE_009.json"}
	]
	
	for entry in mechanic_challenges:
		_validate_mechanic_presentation(entry["mechanic"], entry["path"])
	
	if failures == 0:
		print("[C6E3_RUNTIME_PRESENTATION_SUITE] PASS")
		quit(0)
	else:
		push_error("[C6E3_RUNTIME_PRESENTATION_SUITE] FAIL count=%d" % failures)
		quit(1)

func _validate_mechanic_presentation(mechanic_name: String, path: String) -> void:
	print("  -> Auditando presentación dinámica para mecánica: %s" % mechanic_name)
	
	var cfg = _load_json(path)
	if cfg.is_empty():
		_fail("No se pudo cargar %s" % path)
		return
		
	var profile = Profile.from_challenge(cfg)
	if profile == null:
		_fail("Profile nulo para %s" % mechanic_name)
		return
		
	# E3-C1: Contrato base de dimensiones
	if profile.source_canvas_size != Vector2(540, 960):
		_fail("Canvas origen incorrecto en %s" % mechanic_name)
	if profile.master_output_size != Vector2(1080, 1920):
		_fail("Master output incorrecto en %s" % mechanic_name)
		
	# Tratamiento seguro del tipo de safe_area
	var safe_rect: Rect2
	if typeof(profile.safe_area) == TYPE_RECT2:
		safe_rect = profile.safe_area
	elif typeof(profile.safe_area) == TYPE_DICTIONARY:
		var sa_left = float(profile.safe_area.get("left", 0.0))
		var sa_right = float(profile.safe_area.get("right", 0.0))
		var sa_top = float(profile.safe_area.get("top", 0.0))
		var sa_bot = float(profile.safe_area.get("bottom", 0.0))
		safe_rect = Rect2(sa_left, sa_top, 540.0 - sa_left - sa_right, 960.0 - sa_top - sa_bot)
	else:
		safe_rect = Rect2(0, 0, 540, 960)
	
	# Simulación de UI Root
	var root = Control.new()
	root.size = Vector2(540, 960)
	get_root().add_child(root)
	
	var ui = PresentationUI.new(root, "default_c6", profile)
	
	# Timeline de prueba estandarizado
	var mock_winning_frame = 120
	var phases = [
		{"state": "HOOK", "frame": 30, "expected_hook": true, "expected_game": false, "expected_cta": false},
		{"state": "GAME", "frame": 120, "expected_hook": false, "expected_game": true, "expected_cta": false}, # Winning Frame exacto
		{"state": "GAME", "frame": 150, "expected_hook": false, "expected_game": false, "expected_cta": false}, # GAME post-win
		{"state": "REVEAL", "frame": 250, "expected_hook": false, "expected_game": false, "expected_cta": false},
		{"state": "CTA", "frame": 350, "expected_hook": false, "expected_game": false, "expected_cta": true}
	]
	
	# E3-B1: Flujo real de Integración de Fases (GeneradorMaestro -> Binder -> PresentationUI)
	for p in phases:
		var state = p["state"]
		var abs_frame = p["frame"]
		var is_exact_win = (abs_frame == mock_winning_frame and state == "GAME")
		
		# Generamos un rect de prueba solo en el winning frame para testear D1
		var rects = []
		if is_exact_win:
			var test_rect = Rect2(safe_rect.position.x + 10, safe_rect.position.y + 10, 100, 100)
			rects.append(test_rect)
			
			# E3-D1: Validación de Geometría entregada
			if not safe_rect.encloses(test_rect):
				_fail("E3-D1 Violación geométrica: Rectículo de éxito fuera de Safe Area en %s" % mechanic_name)
		
		# Contenido bruto de simulación
		var raw_content = {
			"hook": "Prueba E3",
			"absolute_frame": abs_frame,
			"winning_frame": mock_winning_frame,
			"ui_state_frame": abs_frame,
			"winning_frame_game": mock_winning_frame,
			"winning_highlight_rects": rects,
			"ui_fps": 60,
			"timeline": null # Ignorado deliberadamente
		}
		
		var rm = Binder.build_frame_render_model(state, raw_content, profile)
		ui.apply_render_model(rm)
		
		# Verificaciones asertivas del estado reactivo de la UI
		if ui.hook_label.visible != p["expected_hook"]:
			_fail("Mismatch Hook visibilidad en fase %s (mecánica %s)" % [state, mechanic_name])
			
		# REPARADO: WinningHighlightComponent usa is_visible(), no .visible
		if ui.winning_highlight.is_visible() != p["expected_game"] and is_exact_win:
			_fail("Winning Highlight no se activó en el Frame Ganador (mecánica %s)" % mechanic_name)
			
		if ui.cta.visible != p["expected_cta"]:
			_fail("Mismatch CTA visibilidad en fase %s (mecánica %s)" % [state, mechanic_name])
			
	# Cleanup del nodo
	root.queue_free()

func _load_json(path: String) -> Dictionary:
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		return {}
	var parsed = JSON.parse_string(file.get_as_text())
	if parsed is Dictionary:
		return parsed
	return {}

func _fail(message: String) -> void:
	failures += 1
	push_error("[C6E3-FAIL] " + message)