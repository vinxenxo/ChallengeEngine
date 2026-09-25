extends SceneTree

## C11-C 2.10.1 — role-based typography contract for all current C11-C visual content.

const Typography = preload("res://core/presentation/C11CVisualTypography.gd")
const PresentationTheme = preload("res://core/presentation/PresentationTheme.gd")
const EditorialLayer = preload("res://core/presentation/C11CVisualEditorialLayer.gd")

var failures: Array[String] = []

func _initialize() -> void:
    _assert(Typography.HEADER_FONT_PATH == "res://assets/fonts/Inter-Bold.otf", "C11-C header typography must use Inter Bold.")
    _assert(Typography.FOOTER_FONT_PATH == "res://assets/fonts/NotoSansMono-Regular.ttf", "C11-C footer typography must use Noto Sans Mono Regular.")
    _assert(FileAccess.file_exists(Typography.HEADER_FONT_PATH), "C11-C header font asset must exist.")
    _assert(FileAccess.file_exists(Typography.FOOTER_FONT_PATH), "C11-C footer font asset must exist.")
    _assert(Typography.get_header_font() != null, "Header font must resolve to a usable Font resource.")
    _assert(Typography.get_footer_font() != null, "Footer font must resolve to a usable Font resource.")
    var editorial_layer = EditorialLayer.new()
    _assert(editorial_layer != null, "Shared C11-C editorial layer must compile and instantiate.")
    _assert(PresentationTheme.FONT_PATH == Typography.HEADER_FONT_PATH, "Legacy PresentationTheme must delegate its active font to the shared C11-C header font.")
    var theme_config: Dictionary = PresentationTheme.get_theme_config("default_c6")
    _assert(theme_config.get("font", null) != null, "Legacy PresentationTheme must resolve the shared active font.")
    _assert(theme_config.get("header_font", null) != null, "PresentationTheme must expose the shared header font role.")
    _assert(theme_config.get("footer_font", null) != null, "PresentationTheme must expose the shared footer font role.")

    var editorial_source := FileAccess.get_file_as_string("res://core/presentation/C11CVisualEditorialLayer.gd")
    var cta_source := FileAccess.get_file_as_string("res://core/presentation/PresentationUI.gd")
    var theme_source := FileAccess.get_file_as_string("res://core/presentation/PresentationTheme.gd")
    var counter_source := FileAccess.get_file_as_string("res://core/presentation/rendering/SaccadeRenderer.gd")
    _assert(editorial_source.find("apply_header_to_label") >= 0, "Shared C11-C editorial header text must use the header role.")
    _assert(editorial_source.find("apply_footer_to_label") >= 0, "Shared C11-C editorial footer text must use the footer role.")
    _assert(cta_source.find("apply_header_to_typography_label") >= 0, "Visual Drill CTA must use the header typography role.")
    _assert(cta_source.find("get_header_font()") >= 0, "Visual Drill countdown must use the header typography role.")
    _assert(counter_source.find("apply_footer_to_label") >= 0, "Saccade jump counter must use the footer typography role.")
    _assert(editorial_source.find("Comic-Sans-MS.ttf") < 0, "C11-C editorial layer must not directly use Comic Sans.")
    _assert(cta_source.find("Comic-Sans-MS.ttf") < 0, "Visual Drill CTA path must not directly use Comic Sans.")
    _assert(editorial_source.find("courier-regular.ttf") < 0, "C11-C editorial layer must not fall back to the old Courier asset.")
    _assert(theme_source.find("Comic-Sans-MS.ttf") < 0, "Active PresentationTheme must not use Comic Sans.")
    _assert(theme_source.find("C11CVisualTypography.gd") >= 0, "PresentationTheme must delegate active font resolution to the shared typography service.")
    _assert(FileAccess.file_exists("res://assets/fonts/Inter-Bold.otf"), "Inter Bold asset must exist for C11-C delivery.")
    _assert(FileAccess.file_exists("res://assets/fonts/NotoSansMono-Regular.ttf"), "Noto Sans Mono Regular asset must exist for C11-C delivery.")
    for loop_source_path in [
        "res://tools/prototypes/c11c_geometric_waves_v1/GeometricWavesPrototype.gd",
        "res://tools/prototypes/c11c_fractal_bloom_v1/FractalBloomPrototype.gd",
        "res://tools/prototypes/c11c_sacred_symmetry_v1/SacredSymmetryPrototype.gd",
        "res://tools/prototypes/c11c_living_particles_v1/LivingParticlesPrototype.gd",
        "res://tools/prototypes/c11c_invisible_forces_v1/InvisibleForcesPrototype.gd"
    ]:
        var loop_source := FileAccess.get_file_as_string(loop_source_path)
        _assert(loop_source.find("C11CVisualEditorialLayerClass") >= 0, "%s must consume the shared C11-C editorial typography layer." % loop_source_path)


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
