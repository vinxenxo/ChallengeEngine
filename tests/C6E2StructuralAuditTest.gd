extends SceneTree

# ============================================================
# C6-E2 Hardening: Structural Boundary & Purity Audit (Complete)
# ============================================================

func _init() -> void:
	print("[TEST] Running C6E2StructuralAuditTest...")
	
	var files_to_check = [
		"res://core/presentation/PresentationUI.gd",
		"res://core/presentation/components/RevealManager.gd",
		"res://core/presentation/components/HookComponent.gd",
		"res://core/presentation/components/CountdownComponent.gd"
	]
	
	var forbidden_terms = [
		"VideoTimeline",
		"SimulationResult",
		"winning_frame", 
		"mechanic_id",
		"update_from_state",
		"set_state"
	]
	
	for file_path in files_to_check:
		var f = FileAccess.open(file_path, FileAccess.READ)
		if f == null:
			push_error("No se pudo abrir el archivo para auditoría: " + file_path)
			quit(1)
			return
			
		var content = f.get_as_text()
		
		for term in forbidden_terms:
			if content.find(term) != -1:
				push_error("Violación arquitectónica en %s: contiene el término prohibido '%s'." % [file_path, term])
				quit(1)
				return
				
	# Verificación estricta de pureza del RenderModel con llamada de 3 argumentos
	var ChallengePresentationBinder = load("res://core/presentation/ChallengePresentationBinder.gd")
	var sample_model = ChallengePresentationBinder.build_frame_render_model("HOOK", {"hook": "Test"}, null)
	var forbidden_model_keys = ["timeline", "VideoTimeline", "SimulationResult", "winning_frame", "mechanic_id", "state", "content"]
	for key in forbidden_model_keys:
		if sample_model.has(key):
			push_error("Violación arquitectónica en RenderModel: contiene la clave prohibida '%s'." % key)
			quit(1)
			return
				
	print("[C6E2_STRUCTURAL_AUDIT_SUITE] PASS")
	quit(0)