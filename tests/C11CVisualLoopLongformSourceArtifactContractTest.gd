extends RefCounted

func _ready():
    var root := ProjectSettings.globalize_path("res://")
    var path := root.path_join("tools/prototypes/c11c_bulk/run_c11c_visual_loop_longform_production.ps1")
    var file := FileAccess.open(path, FileAccess.READ)
    if file == null:
        push_error("[C11C_LONGFORM_SOURCE_ARTIFACT_CONTRACT_SUITE] FAIL - wrapper missing")
        return
    var text := file.get_as_text()
    var checks := [
        ['production_manifest.json', 'Longform must consume the canonical production manifest.'],
        ['artifacts\\prototypes\\$production', 'Longform must resolve canonical prototype music from the existing audio surface.'],
        ['-DeliveryProfile REVIEW_720', 'Longform segment generation must use canonical REVIEW_720 delivery.'],
        ['$sourceMp4', 'Longform must consume the production product MP4.'],
        ['$productionManifestPath', 'Longform must consume the product production_manifest.json.'],
    ]
    for check in checks:
        if text.find(str(check[0])) < 0:
            push_error("[C11C_LONGFORM_SOURCE_ARTIFACT_CONTRACT_SUITE] FAIL - " + str(check[1]))
            return
    if text.find("$source.Manifest") >= 0:
        push_error("[C11C_LONGFORM_SOURCE_ARTIFACT_CONTRACT_SUITE] FAIL - stale source.Manifest contract remains")
        return
    if text.find("if(-not(Test-Path -LiteralPath $req)){throw \"Missing segment artifact") < 0:
        push_error("[C11C_LONGFORM_SOURCE_ARTIFACT_CONTRACT_SUITE] FAIL - required artifact fail-closed guard missing")
        return
    print("[C11C_LONGFORM_SOURCE_ARTIFACT_CONTRACT_SUITE] PASS")
