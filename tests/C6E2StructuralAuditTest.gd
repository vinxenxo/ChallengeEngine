extends SceneTree

# ============================================================
# C6-E2 Hardening: Structural Boundary Audit
# ============================================================

func _init() -> void:
	print("[TEST] Running C6E2StructuralAuditTest...")
	
	var files_to_check = [
		"res://core/presentation/PresentationUI.gd",
		"res://core/presentation/components/RevealManager.gd"
	]
	
	var forbidden_terms = [
		"VideoTimeline",
		"SimulationResult",
		"winning_frame", # Prohibido el término exacto de la simulación
		"mechanic_id"
	]
	
	for file_path in files_to_check:
		var f = FileAccess.open(file_path, FileAccess.READ)
		if f == null:
			push_error("No se pudo abrir el archivo para auditoría: " + file_path)
			quit(1)
			return
			
		var content = f.get_as_text()
		
		for term in forbidden_terms:
			# Buscamos la ocurrencia exacta del string prohibido
			if content.find(term) != -1:
				push_error("Violación arquitectónica en %s: contiene el término prohibido '%s'." % [file_path, term])
				quit(1)
				return
				
	print("[C6E2_STRUCTURAL_AUDIT_SUITE] PASS")
	quit(0)