extends SceneTree

## C11-C Producer regression: REVIEW_720 must not copy an MP4 onto itself.
## This test protects the production-wrapper orchestration contract only.

func _init() -> void:
    var path := "res://tools/prototypes/c11c_bulk/run_c11c_production.ps1"
    var text := FileAccess.get_file_as_string(path)
    assert(not text.is_empty())
    assert(text.find("$sourceFull=[System.IO.Path]::GetFullPath($sourceMp4)") >= 0)
    assert(text.find("$finalFull=[System.IO.Path]::GetFullPath($finalMp4)") >= 0)
    assert(text.find("System.StringComparison]::OrdinalIgnoreCase") >= 0)
    print("[C11C_PRODUCTION_REVIEW_COPY_SAFETY_SUITE] PASS")
    quit()
