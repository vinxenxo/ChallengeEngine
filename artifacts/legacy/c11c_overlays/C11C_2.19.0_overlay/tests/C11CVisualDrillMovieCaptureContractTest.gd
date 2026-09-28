extends SceneTree

## C11-C 2.19.0 — single Visual Drill Movie Maker capture contract.
## AVI is a temporary intermediate only; the Producer does not expose or retain AVI products.
var failures: Array[String] = []

func _initialize() -> void:
    var source := FileAccess.get_file_as_string("res://c11c-suite/c11c-producer/run_visual_drill_production.ps1")
    _assert(source.find("$avi=Join-Path $stage ($baseProductId+'.avi')") >= 0, "Producer Drill must stage a temporary AVI capture.")
    _assert(source.find("'--write-movie',$avi") >= 0, "Producer Drill must pass the AVI path to Movie Maker.")
    _assert(source.find("$movieProcess=Start-Process -FilePath $godotExecutable") >= 0, "Producer Drill must use the proven Start-Process Movie Maker launch path.")
    _assert(source.find("@(''--path'','.'") >= 0, "Producer Drill Movie Maker must launch with project-local --path . like the proven review runner.")
    _assert(source.find("'--resolution'") < 0, "Producer Drill must rely on Enter-C11CMovieOverride rather than a divergent --resolution CLI argument.")
    _assert(source.find("Wait-ForStableFile -Path $avi") >= 0, "Producer Drill must wait for the AVI capture to stabilize.")
    _assert(source.find("-i $avi -an") >= 0, "Producer Drill must convert AVI video without retaining Movie Maker audio.")
    _assert(source.find("'temporary_avi'") >= 0, "Producer manifest must identify the temporary AVI capture format.")
    _assert(source.find("KeepAvi") < 0, "Single Producer Drill must not expose an AVI retention option.")
    if failures.is_empty():
        print("[C11C_VISUAL_DRILL_MOVIE_CAPTURE_CONTRACT_SUITE] PASS")
        quit(0)
        return
    for f in failures:
        push_error(f)
    print("[C11C_VISUAL_DRILL_MOVIE_CAPTURE_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
    quit(1)

func _assert(condition: bool, message: String) -> void:
    if not condition:
        failures.append(message)
