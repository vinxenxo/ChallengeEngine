extends SceneTree

## C11-C 2.18.6 — Longform source-artifact contract.
## Contract-only test: validates that the compositor consumes the canonical
## Producer REVIEW_720 product surface without touching rendering/mechanics.

var failures: Array[String] = []

func _assert(condition: bool, message: String) -> void:
    if not condition:
        failures.append(message)

func _initialize() -> void:
    var root := ProjectSettings.globalize_path("res://")
    var path := root.path_join("tools/prototypes/c11c_bulk/run_c11c_visual_loop_longform_production.ps1")
    var file := FileAccess.open(path, FileAccess.READ)
    _assert(file != null, "Longform producer wrapper must exist.")
    if file == null:
        _finish()
        return

    var source := file.get_as_text()
    var checks := [
        ["production_manifest.json", "Longform must consume the canonical production manifest."],
        ["artifacts\\prototypes\\$production", "Longform must resolve canonical prototype music from the established audio surface."],
        ["-DeliveryProfile REVIEW_720", "Longform segment generation must use canonical REVIEW_720 delivery."],
        ["$sourceMp4", "Longform must consume the produced segment MP4."],
        ["$productionManifestPath", "Longform must consume the product production_manifest.json."],
    ]
    for check in checks:
        _assert(source.find(str(check[0])) >= 0, str(check[1]))

    _assert(source.find("$source.Manifest") < 0, "Stale source.Manifest contract must not remain.")
    _assert(source.find("if(-not(Test-Path -LiteralPath $req)){throw \"Missing segment artifact") >= 0, "Required artifact fail-closed guard is missing.")
    _assert(source.find("if((Test-Path -LiteralPath $sourceMp4) -and ([System.IO.Path]::GetFullPath($sourceMp4) -eq [System.IO.Path]::GetFullPath($finalMp4)))") < 0, "Legacy self-copy guard must not replace the canonical producer output flow.")

    _finish()

func _finish() -> void:
    if failures.is_empty():
        print("[C11C_LONGFORM_SOURCE_ARTIFACT_CONTRACT_SUITE] PASS")
        quit(0)
        return
    for failure in failures:
        push_error(failure)
    print("[C11C_LONGFORM_SOURCE_ARTIFACT_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
    quit(1)
