extends SceneTree

## C11-C 2.9.0 — Typography contract for newly authored Visual Drill presentation text.
## Challenge/C6 legacy theme remains untouched; C11-C content uses Courier Regular.

const Typography = preload("res://core/presentation/C11CVisualTypography.gd")

var failures: Array[String] = []

func _initialize() -> void:
    _assert(Typography.FONT_PATH == "res://assets/fonts/courier-regular.ttf", "C11-C Visual Drill typography must use Courier Regular.")
    _assert(FileAccess.file_exists(Typography.FONT_PATH), "Courier Regular font asset must exist.")
    var font: Font = Typography.get_font()
    _assert(font != null, "C11-C typography utility must resolve a usable Font resource.")
    var editorial_source := FileAccess.get_file_as_string("res://core/presentation/C11CVisualEditorialLayer.gd")
    var cta_source := FileAccess.get_file_as_string("res://core/presentation/PresentationUI.gd")
    var counter_source := FileAccess.get_file_as_string("res://core/presentation/rendering/SaccadeRenderer.gd")
    _assert(editorial_source.find("C11CVisualTypographyClass.apply_to_label") >= 0, "Shared C11-C editorial labels must use the C11-C typography utility.")
    _assert(cta_source.find("C11CVisualTypographyClass.apply_to_typography_label") >= 0, "Visual Drill CTA labels must use the C11-C typography utility.")
    _assert(cta_source.find("C11CVisualTypographyClass.get_font()") >= 0, "Visual Drill countdown must resolve the C11-C typography font on the shared path.")
    _assert(counter_source.find("C11CVisualTypographyClass.apply_to_label") >= 0, "Saccade jump counter must use the C11-C typography utility.")
    _assert(editorial_source.find("Comic-Sans-MS.ttf") < 0, "C11-C editorial layer must not directly use Comic Sans.")
    _assert(cta_source.find("Comic-Sans-MS.ttf") < 0, "Visual Drill CTA path must not directly use Comic Sans.")
    if failures.is_empty():
        print("[C11C_VISUAL_DRILL_TYPOGRAPHY_CONTRACT_SUITE] PASS")
        quit(0)
    else:
        for failure in failures:
            push_error(failure)
        print("[C11C_VISUAL_DRILL_TYPOGRAPHY_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
        quit(1)

func _assert(condition: bool, message: String) -> void:
    if not condition:
        failures.append(message)
