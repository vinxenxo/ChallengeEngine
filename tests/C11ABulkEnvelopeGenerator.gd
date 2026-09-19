extends SceneTree

## C11-A — Visual Seed Qualification & Bulk Envelope Generator.
## Product intent comes from VisualAuthoringRequest.
## Infrastructure comes from VisualAuthoringAssemblyContext.
## No RNG access, no renderer access, no mutation of C6-F0.8/C10 runtime.

const Request = preload("res://core/authoring/VisualAuthoringRequest.gd")
const Context = preload("res://core/authoring/VisualAuthoringAssemblyContext.gd")
const Generator = preload("res://core/authoring/VisualAuthoringGenerator.gd")
const ContentRuntimeRegistry = preload("res://core/runtime/ContentRuntimeRegistry.gd")

const OUTPUT_BASE: String = "res://artifacts/qa/c11a_visual/runs"

const DURATION_SECONDS: float = 2.0
const FPS: int = 30
const TIER: int = 2
const RNG_VERSION: String = "2.0"
const CONTENT_VERSION: String = "1.0.0"
const ENGINE_VERSION: String = "4.7.1"
const PRESENTATION_PROFILE: String = "social_default_v1"
const COORDINATE_SPACE: String = "2d"
const ASSET_FAMILY: String = "fam_001"
const AUDIO_PROFILE: String = "default_procedural_music"
const AUTHOR: String = "c11_visual_bulk_harness"

const ROUTES: Array[Dictionary] = [
    {"family": "visual_loop", "subtype": "fractal"},
    {"family": "visual_loop", "subtype": "vector_field"},
    {"family": "visual_loop", "subtype": "particle_flow"},
    {"family": "visual_loop", "subtype": "kaleidoscope"},
    {"family": "visual_loop", "subtype": "geometric"},
    {"family": "visual_drill", "subtype": "tracking"},
    {"family": "visual_drill", "subtype": "pursuit"},
    {"family": "visual_drill", "subtype": "saccade"},
    {"family": "visual_drill", "subtype": "peripheral_scan"}
]

const SEEDS: Array[Dictionary] = [
    {"value": 12345, "role": "A"},
    {"value": 54321, "role": "NONE"},
    {"value": 314159, "role": "NONE"},
    {"value": 7770001, "role": "NONE"},
    {"value": 998877, "role": "NONE"},
    {"value": 12345, "role": "B"}
]

func _init() -> void:
    print("[C11A] Starting Visual Bulk Envelope Generation...")

    var absolute_root := ProjectSettings.globalize_path(OUTPUT_BASE)
    if not DirAccess.make_dir_recursive_absolute(absolute_root) == OK:
        # Existing directories return OK on current Godot versions; any actual
        # write failure is still caught by FileAccess below.
        pass

    var registry := ContentRuntimeRegistry.create_default()
    var success_count: int = 0
    var expected_count: int = ROUTES.size() * SEEDS.size()

    for route in ROUTES:
        var family: String = str(route["family"])
        var subtype: String = str(route["subtype"])
        # A/B are presentation-independent QA roles. They intentionally share
        # the same content_id so the generated envelope is byte-identical.
        var content_id := "C11A_%s_%s_T%d" % [family.to_upper(), subtype.to_upper(), TIER]

        for seed_data in SEEDS:
            var seed_value: int = int(seed_data["value"])
            var seed_role: String = str(seed_data["role"])
            var run_id := "%s_%s_seed_%d" % [family, subtype, seed_value]
            if seed_role != "NONE":
                run_id += "_%s" % seed_role

            var run_dir := absolute_root.path_join(run_id)
            if not DirAccess.make_dir_recursive_absolute(run_dir) == OK:
                # Continue to FileAccess so the resulting error remains explicit.
                pass

            var request := Request.new(
                family,
                subtype,
                DURATION_SECONDS,
                FPS,
                TIER,
                {}
            )

            var context := Context.new(
                seed_value,
                RNG_VERSION,
                content_id,
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
                printerr("[FATAL] Authoring failed for %s: %s" % [run_id, str(result.get("errors", []))])
                quit(1)
                return

            var envelope: Dictionary = result.get("content", {})
            if envelope.is_empty():
                printerr("[FATAL] Empty envelope for %s" % run_id)
                quit(1)
                return

            var resolution: Dictionary = registry.resolve(envelope)
            if not bool(resolution.get("success", false)):
                printerr(
                    "[FATAL] Runtime Registry rejected %s: %s"
                    % [run_id, str(resolution.get("error_code", "UNKNOWN"))]
                )
                quit(1)
                return

            var request_path := run_dir.path_join("authoring.json")
            var request_file := FileAccess.open(request_path, FileAccess.WRITE)
            if request_file == null:
                printerr("[FATAL] Unable to write authoring.json for %s" % run_id)
                quit(1)
                return
            request_file.store_string(JSON.stringify(request.to_dictionary(), "\t"))
            request_file.close()

            var envelope_path := run_dir.path_join("envelope.json")
            var envelope_file := FileAccess.open(envelope_path, FileAccess.WRITE)
            if envelope_file == null:
                printerr("[FATAL] Unable to write envelope.json for %s" % run_id)
                quit(1)
                return
            envelope_file.store_string(JSON.stringify(envelope, "\t"))
            envelope_file.close()

            success_count += 1
            print("[C11A] Generated & Validated %d/%d: %s" % [success_count, expected_count, run_id])

    if success_count != expected_count:
        printerr("[C11A] FAIL — generated %d/%d envelopes." % [success_count, expected_count])
        quit(1)
        return

    print("[C11A] PASS — Successfully generated %d/%d envelopes." % [success_count, expected_count])
    quit(0)
