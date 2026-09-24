extends SceneTree

## C11-C 2.6.0 — Tracking presentation contract test.

var failures: Array[String] = []

func _initialize() -> void:
	var renderer := FileAccess.get_file_as_string("res://core/presentation/rendering/TrackingRenderer.gd")
	_assert(renderer.find("LivingParticlesTronRoad") < 0, "Tracking must no longer use the Tron background.")
	_assert(renderer.find("C11CTronDepthBackground") < 0, "Tracking must not use the former Tron depth background.")
	_assert(renderer.find("draw_ellipse") < 0, "Tracking must not render the removed circular/elliptical background object.")
	_assert(renderer.find("trail_points") >= 0, "Tracking must render emitted history points.")
	_assert(renderer.find("TRAIL_FADE_SECONDS") >= 0, "Tracking trail must use time-based fading.")
	_assert(renderer.find("GROWING_HISTORY") >= 0, "Tracking must retain growing-history presentation semantics.")
	_assert(renderer.find("C11CDrillPaletteBank") >= 0, "Tracking must use the shared drill palette bank.")
	_assert(renderer.find("secondary_color") >= 0, "Tracking palette must expose a secondary accent for richer trail rendering.")
	_assert(renderer.find("TARGET_Z_INDEX: int = 100") >= 0, "Tracking target must remain the perceptual hero at z100.")
	_assert(renderer.find("future trajectory") < 0, "Tracking renderer must not draw a future trajectory path.")
	if failures.is_empty():
		print("[C11C_TRACKING_PRESENTATION_CONTRACT_SUITE] PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		print("[C11C_TRACKING_PRESENTATION_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
		quit(1)

func _assert(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)
