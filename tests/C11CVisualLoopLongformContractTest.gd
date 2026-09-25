extends SceneTree

## C11-C 2.15.0 — three-minute Visual Loop anthology contract.
var failures: Array[String] = []

func _initialize() -> void:
    var schedule_path: String = "res://profiles/presentation/c11c_visual_loop_longform_schedule.json"
    _assert(FileAccess.file_exists(schedule_path), "Longform schedule must exist.")
    var schedule: Variant = JSON.parse_string(FileAccess.get_file_as_string(schedule_path))
    _assert(schedule is Dictionary, "Longform schedule must be valid JSON.")
    if schedule is Dictionary:
        var families: Dictionary = schedule.get("families", {})
        _assert(families.size() == 5, "Longform schedule must cover five families.")
        for family_id in ["geometric", "fractal", "sacred_symmetry", "living_particles", "invisible_forces"]:
            _assert(families.has(family_id), "Missing longform family: " + family_id)
            if families.has(family_id):
                var raw_seconds: float = 0.0
                var segments: Array = families[family_id].get("segments", [])
                _assert(segments.size() == 8, "Longform family must contain eight authored segments: " + family_id)
                for segment in segments:
                    var segment_seconds: float = float(segment.get("duration_seconds", 0.0))
                    raw_seconds += segment_seconds
                    _assert(segment_seconds >= 20.0 and segment_seconds <= 23.0, "Longform segment must remain in 20..23s range.")
                var transition_seconds: float = float(schedule.get("transition_duration_seconds", 0.0))
                var composed_seconds: float = raw_seconds - transition_seconds * float(segments.size() - 1)
                _assert(abs(raw_seconds - 184.0) <= 0.01, "Eight 23s source segments must total 184s: " + family_id)
                _assert(abs(composed_seconds - 180.0) <= 0.01, "Composed longform must total 180s: " + family_id)
        _assert(abs(float(schedule.get("transition_duration_seconds", 0.0)) - (4.0 / 7.0)) <= 0.0001, "Longform transition must be 4/7s.")
        _assert(float(schedule.get("final_fade_seconds", 0.0)) == 1.0, "Longform must end with a 1s final fade.")
        _assert(str(schedule.get("transition", "")).find("never_through_black") >= 0, "Inter-segment transitions must never go through black.")
        _assert(str(schedule.get("final_fade_color", "")) == "black", "Final fade must be black.")
        _assert(str(schedule.get("composition_model", "")) == "crossfade_continuity_v2", "Longform composition model must be crossfade_continuity_v2.")
    var composer: String = FileAccess.get_file_as_string("res://tools/prototypes/c11c_bulk/run_c11c_visual_loop_longform_production.ps1")
    _assert(composer.find("run_c11c_production.ps1") >= 0, "Longform must reuse canonical production launcher.")
    _assert(composer.find("xfade=transition=fade") >= 0, "Longform must use source-to-source video xfade.")
    _assert(composer.find("acrossfade") >= 0, "Longform must use audio acrossfade.")
    _assert(composer.find("color=black") >= 0, "Longform must have an explicit final fade to black.")
    _assert(composer.find("never_through_black") >= 0, "Longform must declare no black between chapters.")
    if failures.is_empty():
        print("[C11C_VISUAL_LOOP_LONGFORM_CONTRACT_SUITE] PASS")
        quit(0)
        return
    for f in failures: push_error(f)
    print("[C11C_VISUAL_LOOP_LONGFORM_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
    quit(1)

func _assert(condition: bool, message: String) -> void:
    if not condition: failures.append(message)
