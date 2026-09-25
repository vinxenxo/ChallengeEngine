extends SceneTree

## C11-C 2.14.1 — three-minute Visual Loop anthology contract.
var failures: Array[String] = []

func _initialize() -> void:
    var schedule_path := "res://profiles/presentation/c11c_visual_loop_longform_schedule.json"
    _assert(FileAccess.file_exists(schedule_path), "Longform schedule must exist.")
    var schedule: Variant = JSON.parse_string(FileAccess.get_file_as_string(schedule_path))
    _assert(schedule is Dictionary, "Longform schedule must be valid JSON.")
    if schedule is Dictionary:
        var families: Dictionary = schedule.get("families", {})
        _assert(families.size() == 5, "Longform schedule must cover the five Visual Loop families.")
        for family_id in ["geometric", "fractal", "sacred_symmetry", "living_particles", "invisible_forces"]:
            _assert(families.has(family_id), "Missing longform family: " + family_id)
            if families.has(family_id):
                var seconds := 0.0
                var segments: Array = families[family_id].get("segments", [])
                for segment in segments:
                    seconds += float(segment.get("duration_seconds", 0.0))
                    _assert(float(segment.get("duration_seconds", 0.0)) >= 20.0 and float(segment.get("duration_seconds", 0.0)) <= 23.0, "Longform segment must remain in the standard 20..23s range.")
                _assert(abs(seconds - 180.0) <= 0.01, "Longform family must total exactly 180s: " + family_id)
                _assert(segments.size() >= 5, "Longform family must combine multiple visual grammars.")
        var invisible: Array = families.get("invisible_forces", {}).get("segments", [])
        var invisible_grammars: Array[String] = []
        for segment in invisible: invisible_grammars.append(str(segment.get("grammar_id", "")))
        for required in ["dipole_field", "vortex_field", "saddle_field", "quadrupole_field", "gravitational_lens", "topographic_basin", "scalar_potential"]:
            _assert(invisible_grammars.has(required), "Invisible Forces longform must include " + required + ".")
    var composer := FileAccess.get_file_as_string("res://tools/prototypes/c11c_bulk/run_c11c_visual_loop_longform_production.ps1")
    _assert(composer.find("run_c11c_production.ps1") >= 0, "Longform composer must reuse canonical production launcher.")
    _assert(composer.find("ffmpeg") >= 0, "Longform composer must use FFmpeg composition instead of duplicating renderers.")
    _assert(composer.find("180.0") >= 0, "Longform composer must validate the 180s target.")
    if failures.is_empty():
        print("[C11C_VISUAL_LOOP_LONGFORM_CONTRACT_SUITE] PASS")
        quit(0)
        return
    for f in failures: push_error(f)
    print("[C11C_VISUAL_LOOP_LONGFORM_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
    quit(1)

func _assert(condition: bool, message: String) -> void:
    if not condition: failures.append(message)
