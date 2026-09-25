extends SceneTree

## C11-C 2.9.0 — Request-specific Visual Drill review envelope generator.
## Generates review-only envelopes for exactly the seeds requested by the PowerShell
## reviewer. Uses the canonical authoring generator; does not mutate simulation or RNG.

const Request = preload("res://core/authoring/VisualAuthoringRequest.gd")
const Context = preload("res://core/authoring/VisualAuthoringAssemblyContext.gd")
const Generator = preload("res://core/authoring/VisualAuthoringGenerator.gd")
const ContentRuntimeRegistry = preload("res://core/runtime/ContentRuntimeRegistry.gd")

const OUTPUT_ENV := "C11C_DRILL_REVIEW_ENVELOPE_ROOT"
const SEEDS_ENV := "C11C_DRILL_REVIEW_SEEDS"
const FAMILIES_ENV := "C11C_DRILL_REVIEW_FAMILIES"
const DEFAULT_GAMEPLAY_SECONDS: float = 17.0
const TRACKING_GAMEPLAY_SECONDS: float = 21.0
const FPS: int = 30
const TIER: int = 2
const RNG_VERSION: String = "2.0"
const CONTENT_VERSION: String = "1.0.0"
const ENGINE_VERSION: String = "4.7.1"
const PRESENTATION_PROFILE: String = "social_default_v1"
const COORDINATE_SPACE: String = "2d"
const ASSET_FAMILY: String = "fam_001"
const AUDIO_PROFILE: String = "FAMILY_MUSIC_V3"
const AUTHOR: String = "c11c_visual_drill_review"
const DRILLS: Array[String] = ["tracking", "saccade", "pursuit", "peripheral_scan"]

func _init() -> void:
    var output_root := OS.get_environment(OUTPUT_ENV).strip_edges()
    var seeds_raw := OS.get_environment(SEEDS_ENV).strip_edges()
    var families_raw := OS.get_environment(FAMILIES_ENV).strip_edges()
    if output_root.is_empty() or seeds_raw.is_empty():
        printerr("[C11-C-DRILL] Review envelope generator requires output root and seeds environment variables.")
        quit(1)
        return

    var seeds: Array[int] = []
    for raw in seeds_raw.split(",", false):
        var token := raw.strip_edges()
        if not token.is_valid_int():
            printerr("[C11-C-DRILL] Invalid review seed: %s" % token)
            quit(1)
            return
        var value := int(token)
        if value < 1 or value > 2147483646:
            printerr("[C11-C-DRILL] Seed out of range: %d" % value)
            quit(1)
            return
        if not seeds.has(value):
            seeds.append(value)

    if seeds.is_empty():
        printerr("[C11-C-DRILL] No review seeds requested.")
        quit(1)
        return

    var absolute_root := ProjectSettings.globalize_path(output_root)
    DirAccess.make_dir_recursive_absolute(absolute_root)
    var registry := ContentRuntimeRegistry.create_default()
    var selected_drills: Array[String] = []
    if families_raw.is_empty():
        selected_drills = DRILLS.duplicate()
    else:
        for raw_family in families_raw.split(",", false):
            var family := raw_family.strip_edges()
            if not DRILLS.has(family):
                printerr("[C11-C-DRILL] Unknown Visual Drill family: %s" % family)
                quit(1)
                return
            if not selected_drills.has(family):
                selected_drills.append(family)
    if selected_drills.is_empty():
        printerr("[C11-C-DRILL] No Visual Drill families requested.")
        quit(1)
        return

    var expected_count := selected_drills.size() * seeds.size()
    var success_count := 0

    for subtype in selected_drills:
        for seed_value in seeds:
            var run_id := "visual_drill_%s_seed_%d" % [subtype, seed_value]
            var run_dir := absolute_root.path_join(run_id)
            DirAccess.make_dir_recursive_absolute(run_dir)

            var gameplay_seconds: float = TRACKING_GAMEPLAY_SECONDS if subtype == "tracking" else DEFAULT_GAMEPLAY_SECONDS
            var request := Request.new(
                "visual_drill",
                subtype,
                gameplay_seconds,
                FPS,
                TIER,
                {}
            )
            var context := Context.new(
                seed_value,
                RNG_VERSION,
                "C11C_REVIEW_%s_T%d" % [subtype.to_upper(), TIER],
                CONTENT_VERSION,
                ENGINE_VERSION,
                {
                    "profile_id": PRESENTATION_PROFILE,
                    "coordinate_space": COORDINATE_SPACE
                },
                {
                    "family_id": ASSET_FAMILY
                },
                {
                    "profile_id": AUDIO_PROFILE,
                    "enabled": false
                },
                {
                    "author": AUTHOR,
                    "timestamp_ms": 0
                }
            )

            var result: Dictionary = Generator.generate(request, context)
            if not bool(result.get("success", false)):
                printerr("[C11-C-DRILL] Authoring failed for %s: %s" % [run_id, str(result.get("errors", []))])
                quit(1)
                return

            var envelope: Dictionary = result.get("content", {})
            if envelope.is_empty():
                printerr("[C11-C-DRILL] Empty envelope for %s" % run_id)
                quit(1)
                return

            var resolution: Dictionary = registry.resolve(envelope)
            if not bool(resolution.get("success", false)):
                printerr("[C11-C-DRILL] Runtime registry rejected %s: %s" % [run_id, str(resolution.get("error_code", "UNKNOWN"))])
                quit(1)
                return

            var authoring_path := run_dir.path_join("authoring.json")
            var authoring_file := FileAccess.open(authoring_path, FileAccess.WRITE)
            if authoring_file == null:
                printerr("[C11-C-DRILL] Unable to write authoring.json for %s" % run_id)
                quit(1)
                return

            # Preserve the original request document and append the deterministic
            # authored study sheet. The seed remains external to VisualAuthoringRequest;
            # it is recorded here as artifact provenance only.
            var authoring_document: Dictionary = request.to_dictionary().duplicate(true)
            var authored_payload: Dictionary = envelope.get("payload", {}) if envelope.get("payload", {}) is Dictionary else {}
            var authored_task: Dictionary = authored_payload.get("task", {}) if authored_payload.get("task", {}) is Dictionary else {}
            var authored_trajectory: Dictionary = authored_payload.get("trajectory", {}) if authored_payload.get("trajectory", {}) is Dictionary else {}
            authoring_document["authored"] = {
                "seed": seed_value,
                "variation_version": "VisualDrillSeedVariation/2.9.0",
                "trajectory": {
                    "type": authored_trajectory.get("type", ""),
                    "profile": authored_trajectory.get("profile", ""),
                    "coordinate_space": authored_trajectory.get("coordinate_space", "")
                },
                "answer_sheet": authored_task.get("answer_sheet", {}),
                "task_summary": {
                    "type": authored_task.get("type", subtype),
                    "sizygia_count": authored_task.get("sizygia_count", null),
                    "threat_count": authored_task.get("threat_count", null),
                    "distractor_count": authored_task.get("distractor_count", null)
                }
            }
            authoring_file.store_string(JSON.stringify(authoring_document, "\t"))
            authoring_file.close()

            var envelope_path := run_dir.path_join("envelope.json")
            var envelope_file := FileAccess.open(envelope_path, FileAccess.WRITE)
            if envelope_file == null:
                printerr("[C11-C-DRILL] Unable to write envelope.json for %s" % run_id)
                quit(1)
                return
            envelope_file.store_string(JSON.stringify(envelope, "\t"))
            envelope_file.close()

            success_count += 1
            print("[C11-C-DRILL] Envelope %d/%d: %s" % [success_count, expected_count, run_id])

    print("[C11-C-DRILL] Request-specific envelope generation PASS — %d/%d" % [success_count, expected_count])
    quit(0)
