extends SceneTree

var failures: Array[String] = []

const EnvironmentSource = "res://core/presentation/rendering/C11CDrillEnvironment.gd"

func _initialize() -> void:
    var source := FileAccess.get_file_as_string("res://core/presentation/rendering/PeripheralScanRenderer.gd")
    _assert(source.find("_draw_anchor") >= 0, "Peripheral renderer must have a dedicated fixation anchor.")
    _assert(source.find("_draw_event") >= 0, "Peripheral renderer must have an explicit peripheral event renderer.")
    _assert(source.find("draw_arc(CENTER") >= 0, "Peripheral renderer must expose the orbital radar rings.")
    _assert(source.find("active_events") >= 0, "Peripheral renderer must consume authored active events.")
    _assert(source.find("draw_circle(CENTER + Vector2(cos(angle), sin(angle)) * radius") >= 0, "Peripheral event must remain a luminosity-based flare, not a solid node.")
    _assert(source.find("C11CDrillEnvironmentClass") >= 0, "Peripheral renderer must mount the shared restrained Body environment.")

    _assert(FileAccess.file_exists(EnvironmentSource), "Shared C11-C drill environment must be present.")
    _conclude()

func _assert(condition: bool, message: String) -> void:
    if not condition:
        failures.append(message)

func _conclude() -> void:
    if failures.is_empty():
        print("[C11C_PERIPHERAL_SCAN_PRESENTATION_CONTRACT_SUITE] PASS")
        quit(0)
    else:
        for failure in failures:
            push_error(failure)
        print("[C11C_PERIPHERAL_SCAN_PRESENTATION_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
        quit(1)
