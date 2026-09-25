extends SceneTree

## C11-C 2.15.0 — lightweight production output contract.
var failures: Array[String] = []

func _initialize() -> void:
    var family_launchers := {
        "geometric": "res://tools/prototypes/c11c_geometric_waves_v1/run_prototype.ps1",
        "fractal": "res://tools/prototypes/c11c_fractal_bloom_v1/run_prototype.ps1",
        "sacred_symmetry": "res://tools/prototypes/c11c_sacred_symmetry_v1/run_prototype.ps1",
        "living_particles": "res://tools/prototypes/c11c_living_particles_v1/run_prototype.ps1",
        "invisible_forces": "res://tools/prototypes/c11c_invisible_forces_v1/run_prototype.ps1"
    }
    for family in family_launchers.keys():
        var path: String = str(family_launchers[family])
        var source := FileAccess.get_file_as_string(path)
        _assert(source.find("[switch]$ExportGif") >= 0, path + " must make GIF export optional.")
        _assert(source.find("[switch]$KeepAvi") >= 0, path + " must expose optional AVI retention.")
        _assert(source.find("[string]$OutputRoot") >= 0, path + " must accept an alternate output root for extraordinary reviews.")
        _assert(source.find("GetTempPath") >= 0, path + " must stage AVI in temporary storage by default.")
        _assert(source.find("$ExportGif") >= 0, path + " must gate GIF generation.")
        _assert(source.find("Remove-Item -Force -LiteralPath $Avi") >= 0, path + " must clean the temporary AVI in finally.")
        _assert(source.find("20.0,23.0") >= 0, path + " must enforce the 20..23s Visual Loop range.")
    var production := FileAccess.get_file_as_string("res://tools/prototypes/c11c_bulk/run_c11c_production.ps1")
    _assert(production.find("[switch]$ExportGif") >= 0, "Production runner must expose optional GIF export.")
    _assert(production.find("[switch]$KeepAvi") >= 0, "Production runner must expose optional AVI retention.")
    var drill := FileAccess.get_file_as_string("res://tools/prototypes/c11c_bulk/run_c11c_visual_drill_review.ps1")
    _assert(drill.find("[switch]$ExportGif") >= 0, "Drill review must make GIF export optional.")
    _assert(drill.find("ReviewRootOverride") >= 0, "Drill review must accept an extraordinary review root.")
    _assert(drill.find("[switch]$KeepAvi") >= 0, "Drill review must expose optional AVI retention.")
    if failures.is_empty():
        print("[C11C_ART_DIRECTION_PRODUCTION_HYGIENE_CONTRACT_SUITE] PASS")
        quit(0)
        return
    for f in failures: push_error(f)
    print("[C11C_ART_DIRECTION_PRODUCTION_HYGIENE_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
    quit(1)

func _assert(condition: bool, message: String) -> void:
    if not condition: failures.append(message)
