extends SceneTree

## C11-C.7 — Saccade presentation contract test.

var failures: Array[String] = []

func _initialize() -> void:
    var renderer := FileAccess.get_file_as_string("res://core/presentation/rendering/SaccadeRenderer.gd")
    _assert(renderer.find("lerp(") < 0, "Saccade renderer must not interpolate spatial position.")
    _assert(renderer.find("scale") >= 0, "Saccade renderer must use scale transitions.")
    _assert(renderer.find("opacity") >= 0, "Saccade renderer must use opacity transitions.")
    _assert(renderer.find("flash_strength") >= 0, "Saccade renderer must support vanish flash.")
    _assert(renderer.find("BODY_RECT") >= 0, "Saccade renderer must use the logical Body.")
    _assert(renderer.find("var backgrounds: Array[Color]") >= 0, "Saccade must expose deterministic cosmetic palettes.")
    _assert(renderer.find("saccade_variant") >= 0, "Saccade palette selection must consume only the cosmetic variant.")
    _assert(renderer.find("Tron") < 0, "Random/polar Saccade baseline must not add decorative background.")
    if failures.is_empty():
        print("[C11C_SACCADE_PRESENTATION_CONTRACT_SUITE] PASS")
        quit(0)
    else:
        for failure in failures:
            push_error(failure)
        print("[C11C_SACCADE_PRESENTATION_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
        quit(1)

func _assert(condition: bool, message: String) -> void:
    if not condition:
        failures.append(message)
