# res://tests/C6F08CompositionGeometryTest.gd
extends SceneTree

# ============================================================
# C6-F0.8-A.1 — Composition Geometry Contract Test
# Validates deterministic viewport derivations and bounds from PresentationProfile.
# ============================================================

const PresentationProfile = preload("res://core/presentation/PresentationProfile.gd")

var failures: Array[String] = []

func _initialize() -> void:
	print("[TEST] Running C6F08CompositionGeometryTest...")
	_run_tests()
	_conclude()

func _assert(condition: bool, fail_msg: String) -> void:
	if not condition:
		failures.append(fail_msg)

func _run_tests() -> void:
	var profile := PresentationProfile.new()
	
	# 1. Validación estructural y geométrica general del perfil
	var val_res := profile.validate()
	_assert(val_res.is_valid, "Fallo de validación en PresentationProfile: " + str(val_res.errors))
	
	var geom = profile.get_composition_geometry()
	var canvas: Rect2 = geom["canvas_rect"]
	var safe: Rect2 = geom["safe_rect"]
	var header: Rect2 = geom["header_rect"]
	var content: Rect2 = geom["content_rect"]
	var footer: Rect2 = geom["footer_rect"]
	
	# 2. Comprobación de límites dentro del canvas
	_assert(canvas.encloses(header), "Header excede los límites del canvas.")
	_assert(canvas.encloses(footer), "Footer excede los límites del canvas.")
	
	# 3. Comprobación estricta de solapamientos
	_assert(header.end.y <= content.position.y, "Header invade el área de contenido.")
	_assert(content.end.y <= footer.position.y, "Contenido invade el área de footer.")
	
	# 4. El contenido debe estar estrictamente dentro del safe_area
	_assert(safe.encloses(content), "El content_rect debe estar estrictamente contenido dentro del safe_area.")
	
	# 5. Reproducibilidad / Pureza determinista
	var geom_second := profile.get_composition_geometry()
	_assert(geom["content_rect"] == geom_second["content_rect"], "La derivación geométrica no es reproducible/determinista.")
	_assert(geom["header_rect"] == geom_second["header_rect"], "Header geométrico no reproducible.")
	_assert(geom["footer_rect"] == geom_second["footer_rect"], "Footer geométrico no reproducible.")

func _conclude() -> void:
	if failures.is_empty():
		print("[C6F08_COMPOSITION_GEOMETRY_SUITE] PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		print("[C6F08_COMPOSITION_GEOMETRY_SUITE] FAIL failures=%d" % failures.size())
		quit(1)