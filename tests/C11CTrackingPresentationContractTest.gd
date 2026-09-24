extends SceneTree

## C11-C 2.5.0 — Tracking presentation contract.

var failures: Array[String] = []

func _initialize() -> void:
    var source: String = FileAccess.get_file_as_string("res://core/presentation/rendering/TrackingRenderer.gd")
    _assert(source.find("Rect2(0.0, 144.0, 540.0, 672.0)") >= 0, "Tracking Body must occupy the full 540px logical width.")
    _assert(source.find("GROWING_HISTORY") >= 0, "Tracking renderer must declare growing history presentation.")
    _assert(source.find("draw_circle(head") >= 0, "Tracking history must retain a visible live head/estela accent.")
    _assert(source.find("_draw_ellipse") >= 0, "Tracking operating field helper must avoid native CanvasItem name collisions.")
    _assert(source.find("LivingParticlesTronRoad.gd") >= 0, "Tracking must reuse the established Living Particles Tron road implementation.")
    _assert(source.find("set_intensity_scale(0.72)") >= 0, "Tracking Tron environment must remain visually subordinate to the target.")
    _assert(source.find("var backgrounds: Array[Color]") >= 0, "Tracking must expose deterministic mobile-safe color palettes.")
    _assert(source.find("TARGET_Z_INDEX: int = 100") >= 0, "Tracking target must use the explicit Z=100 presentation layer.")
    _assert(source.find("age_seconds") >= 0, "Tracking trail fade must be based on elapsed time.")
    _assert(source.find("TRAIL_FADE_SECONDS") >= 0, "Tracking trail must expose a time-based fade window.")
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
