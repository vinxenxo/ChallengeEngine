extends SceneTree

## C10-C — Writes two representative Content Envelope V2 definitions for physical export.
## This is an explicit fixture-preparation step; production runtime code is not modified.

const Request = preload("res://core/authoring/VisualAuthoringRequest.gd")
const Context = preload("res://core/authoring/VisualAuthoringAssemblyContext.gd")
const Generator = preload("res://core/authoring/VisualAuthoringGenerator.gd")

const OUTPUT_DIR: String = "res://artifacts/qa/physical_smoke/c10c_e2e/definitions"
const SEED: int = 12345
const TIER: int = 2
const DURATION_SECONDS: float = 2.0
const FPS: int = 30

const FIXTURES: Array[Dictionary] = [
    {"domain_family": "visual_loop", "subtype": "fractal", "filename": "c10c_visual_loop_fractal.json"},
    {"domain_family": "visual_drill", "subtype": "tracking", "filename": "c10c_visual_drill_tracking.json"}
]

func _init() -> void:
    print("[TEST] Running C10CPreparePhysicalFixtures...")
    var errors: Array[String] = []

    var absolute_dir: String = ProjectSettings.globalize_path(OUTPUT_DIR)
    DirAccess.make_dir_recursive_absolute(absolute_dir)

    for fixture in FIXTURES:
        var domain_family: String = str(fixture["domain_family"])
        var subtype: String = str(fixture["subtype"])
        var filename: String = str(fixture["filename"])
        var request: Request = Request.new(domain_family, subtype, DURATION_SECONDS, FPS, TIER, {})
        var content_id: String = "C10C_PHYSICAL_%s_%s" % [domain_family.to_upper(), subtype.to_upper()]
        var context: Context = Context.new(
            SEED,
            "2.0",
            content_id,
            "1.0.0",
            "4.7.1",
            {"profile_id": "social_default_v1", "coordinate_space": "2d"},
            {"family_id": "fam_001"},
            {"profile_id": "default_procedural_music", "enabled": false},
            {"author": "c10_visual_authoring_physical_smoke", "timestamp_ms": 0}
        )

        var result: Dictionary = Generator.generate(request, context)
        if not bool(result.get("success", false)):
            errors.append("Generation failed for %s/%s: %s" % [domain_family, subtype, str(result.get("errors", []))])
            continue

        var content: Dictionary = result.get("content", {})
        var target_path: String = OUTPUT_DIR + "/" + filename
        var file: FileAccess = FileAccess.open(target_path, FileAccess.WRITE)
        if file == null:
            errors.append("Unable to open fixture path for write: %s" % target_path)
            continue

        file.store_string(JSON.stringify(content))
        file.close()
        print("[C10C] Fixture written: %s" % target_path)

    if errors.is_empty():
        print("[C10C_PHYSICAL_FIXTURE_PREPARATION] PASS — 2/2")
        quit(0)
        return

    for error_text in errors:
        push_error(error_text)
    print("[C10C_PHYSICAL_FIXTURE_PREPARATION] FAIL failures=%d" % errors.size())
    quit(1)
