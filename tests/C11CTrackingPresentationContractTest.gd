extends SceneTree

## C11-C 2.4.0 — Tracking presentation contract.

var failures: Array[String] = []

func _initialize() -> void:
	var source: String = FileAccess.get_file_as_string("res://core/presentation/rendering/TrackingRenderer.gd")
	_assert(source.find("Rect2(0.0, 144.0, 540.0, 672.0)") >= 0, "Tracking Body must occupy the full 540px logical width.")
	_assert(source.find("growing_history") >= 0, "Tracking renderer must support growing history presentation.")
	_assert(source.find("C11CTronDepthBackground.gd") >= 0, "Tracking must mount the shared Tron depth background.")
	_assert(source.find("var backgrounds: Array[Color]") >= 0, "Tracking must expose deterministic mobile-safe color palettes.")
	var generator: String = FileAccess.get_file_as_string("res://core/runtime/visual_drill/generators/TrackingGenerator.gd")
	_assert(generator.find("trail_mode") >= 0, "Tracking generator must declare trail mode.")
	_assert(generator.find("first_frame: int = 0") >= 0, "Growing history must start at gameplay frame 0.")
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
