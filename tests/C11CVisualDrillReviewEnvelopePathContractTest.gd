extends SceneTree

## C11-C 2.19.12 — Visual Drill review envelope path contract.
## Prevents an absolute Windows output root from being passed through
## ProjectSettings.globalize_path(), which would reinterpret it relative to the project.
## Also locks the shared Drill duration contract: Tracking=21s, others=17s gameplay.

var _failures: int = 0

func _assert(condition: bool, message: String) -> void:
    if not condition:
        push_error("ASSERT FAILED: " + message)
        _failures += 1

func _read(path: String) -> String:
    var file := FileAccess.open(path, FileAccess.READ)
    _assert(file != null, "Missing readable file: " + path)
    if file == null:
        return ""
    return file.get_as_text()

func _initialize() -> void:
    var generator := _read("res://tools/prototypes/c11c_bulk/C11CVisualDrillReviewEnvelopeGenerator.gd")
    var review := _read("res://tools/prototypes/c11c_bulk/run_c11c_visual_drill_review.ps1")

    _assert(generator.find("const DEFAULT_GAMEPLAY_SECONDS: float = 17.0") >= 0, "Non-tracking Drill gameplay must be 17s in the envelope generator.")
    _assert(generator.find("const TRACKING_GAMEPLAY_SECONDS: float = 21.0") >= 0, "Tracking Drill gameplay must be 21s in the envelope generator.")
    _assert(generator.find("var absolute_root := output_root") >= 0, "Envelope generator must preserve the supplied absolute root.")
    _assert(generator.find("if not output_root.is_absolute_path():") >= 0, "Envelope generator must distinguish absolute and project-relative roots.")
    _assert(generator.find("absolute_root = ProjectSettings.globalize_path(output_root)") >= 0, "Relative roots must still be localized correctly.")
    _assert(generator.find("var absolute_root := ProjectSettings.globalize_path(output_root)") < 0, "The old unconditional globalize_path regression must not return.")
    _assert(generator.find("Envelope root resolved:") >= 0, "Generator must log the resolved envelope root for diagnostics.")
    _assert(review.find("$DefaultGameplayDurationSeconds=17.0") >= 0, "PowerShell review must use 17s default gameplay.")
    _assert(review.find("$TrackingGameplayDurationSeconds=21.0") >= 0, "PowerShell review must use 21s Tracking gameplay.")

    if _failures == 0:
        print("[C11C_VISUAL_DRILL_ENVELOPE_PATH_CONTRACT_SUITE] PASS")
        quit(0)
        return
    push_error("[C11C_VISUAL_DRILL_ENVELOPE_PATH_CONTRACT_SUITE] FAIL (%d failure(s))" % _failures)
    quit(1)
