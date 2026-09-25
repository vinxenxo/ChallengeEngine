extends SceneTree

var failures: Array[String] = []
const COVERAGE := "res://tools/prototypes/c11c_bulk/run_c11c_visual_loops_subtype_music_coverage.ps1"

func _initialize() -> void:
    var s := FileAccess.get_file_as_string(COVERAGE)
    _assert(s.find("total=27") >= 0, "Visual Loop subtype/music coverage must cover 27 subtypes.")
    _assert(s.find("-Grammar ([string]$case.Grammar)") >= 0, "Coverage runner must force the requested technical grammar.")
    _assert(s.find("grammar_id") >= 0, "Coverage must validate technical grammar IDs, not artistic display labels.")
    _assert(s.find("audio.mode -ne 'FAMILY_MUSIC_V4'") >= 0, "Coverage must validate FAMILY_MUSIC_V4.")
    _assert(s.find("scalar_potential") >= 0, "Coverage must include Scalar Potential.")
    if failures.is_empty():
        print("[C11C_VISUAL_LOOP_SUBTYPE_MUSIC_COVERAGE_CONTRACT_SUITE] PASS")
        quit(0)
    for f in failures: push_error(f)
    print("[C11C_VISUAL_LOOP_SUBTYPE_MUSIC_COVERAGE_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
    quit(1)

func _assert(condition: bool, message: String) -> void:
    if not condition: failures.append(message)
