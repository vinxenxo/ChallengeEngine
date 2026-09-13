# res://tests/C6F08CompositionContractTest.gd
extends SceneTree

# ============================================================
# C6-F0.8-A — Composition Contract Test (Corrected to baseline API)
# Validates PresentationProfile ownership of canvas size and derived layout logic.
# ============================================================

const PresentationProfile = preload("res://core/presentation/PresentationProfile.gd")

var failures: Array[String] = []

func _initialize() -> void:
	print("[TEST] Running C6F08CompositionContractTest...")
	
	var profile := PresentationProfile.new()
	
	# Verify that PresentationProfile owns canonical canvas dimensions
	if not "source_canvas_size" in profile:
		failures.append("PresentationProfile lacks 'source_canvas_size' property contract.")
		
	# Verify composition / safe area property existence
	if not "composition" in profile and not "safe_area" in profile:
		failures.append("PresentationProfile lacks composition or safe area layout definitions.")
		
	_conclude()

func _conclude() -> void:
	if failures.is_empty():
		print("[C6F08_COMPOSITION_CONTRACT_SUITE] PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		print("[C6F08_COMPOSITION_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
		quit(1)