extends SceneTree

## C11-C Producer Visual Drills overlay 0.1.1.
## Producer-side bridge only: delegates all authoring/seed variation to the frozen 2.10.1 backend.
const Request = preload("res://core/authoring/VisualAuthoringRequest.gd")
const Context = preload("res://core/authoring/VisualAuthoringAssemblyContext.gd")
const Generator = preload("res://core/authoring/VisualAuthoringGenerator.gd")
const ContentRuntimeRegistry = preload("res://core/runtime/ContentRuntimeRegistry.gd")

const VALID_FAMILIES: Array[String] = ["tracking", "saccade", "pursuit", "peripheral_scan"]
const FPS: int = 30
const RNG_VERSION: String = "2.0"
const CONTENT_VERSION: String = "1.0.0"
const ENGINE_VERSION: String = "4.7.1"
const AUTHORING_VERSION: String = "1.0"
const PRESENTATION_PROFILE: String = "social_default_v1"
const COORDINATE_SPACE: String = "2d"
const ASSET_FAMILY: String = "fam_001"
const AUDIO_PROFILE: String = "FAMILY_MUSIC_V3"

func _init() -> void:
    var args: PackedStringArray = OS.get_cmdline_user_args()
    if args.is_empty():
        _fail("Missing request JSON path", "")
        return
    var request_path: String = str(args[0])
    var file: FileAccess = FileAccess.open(request_path, FileAccess.READ)
    if file == null:
        _fail("Cannot open request JSON: %s" % request_path, request_path)
        return
    var parsed: Variant = JSON.parse_string(file.get_as_text())
    file.close()
    if not (parsed is Dictionary):
        _fail("Invalid request JSON", request_path)
        return

    var data: Dictionary = parsed
    var subtype: String = str(data.get("family", ""))
    var seed: int = int(data.get("seed", 0))
    var tier: int = int(data.get("difficulty_tier", 2))
    var speed: float = float(data.get("speed_multiplier", 1.0))
    var pacing: String = str(data.get("pacing_mode", "constant"))
    var no_sound: bool = bool(data.get("no_sound", false))

    if not VALID_FAMILIES.has(subtype):
        _fail("Unsupported Visual Drill family: %s" % subtype, request_path)
        return
    if seed < 1 or seed > 2147483646:
        _fail("Seed out of range: %d" % seed, request_path)
        return
    if tier < 1 or tier > 5:
        _fail("Difficulty tier must be 1..5", request_path)
        return
    if speed < 0.1 or speed > 3.0:
        _fail("Speed multiplier must be 0.1..3.0", request_path)
        return
    if not ["constant", "accelerating", "pulsed"].has(pacing):
        _fail("Unsupported pacing mode: %s" % pacing, request_path)
        return

    var gameplay_seconds: float = 21.0 if subtype == "tracking" else 17.0
    var custom_parameters: Dictionary = {
        "speed_multiplier": speed,
        "pacing_mode": pacing
    }

    var request: VisualAuthoringRequest = Request.new(
        "visual_drill", subtype, gameplay_seconds, FPS, tier, custom_parameters, AUTHORING_VERSION
    )
    var context: VisualAuthoringAssemblyContext = Context.new(
        seed, RNG_VERSION, "C11C_PRODUCER_${subtype.to_upper()}_T${tier}", CONTENT_VERSION, ENGINE_VERSION,
        {"profile_id": PRESENTATION_PROFILE, "coordinate_space": COORDINATE_SPACE},
        {"family_id": ASSET_FAMILY},
        {"profile_id": AUDIO_PROFILE, "enabled": not no_sound},
        {"author": "c11c_producer", "timestamp_ms": 0}
    )

    var result: Dictionary = Generator.generate(request, context)
    if not bool(result.get("success", false)):
        _fail("Authoring failed: %s" % str(result.get("errors", [])), request_path)
        return

    var envelope_variant: Variant = result.get("content", {})
    if not (envelope_variant is Dictionary) or (envelope_variant as Dictionary).is_empty():
        _fail("Empty envelope", request_path)
        return
    var envelope: Dictionary = envelope_variant

    # Validate against the same runtime registry used by C11-C presentation.
    var registry := ContentRuntimeRegistry.create_default()
    var resolution: Dictionary = registry.resolve(envelope)
    if not bool(resolution.get("success", false)):
        _fail("Runtime registry rejected envelope: %s" % str(resolution.get("error_code", "UNKNOWN")), request_path)
        return

    var root: String = request_path.get_base_dir()
    var env_path: String = root.path_join("envelope.json")
    var authoring_path: String = root.path_join("authoring.json")
    var payload_variant: Variant = envelope.get("payload", {})
    var payload: Dictionary = payload_variant if payload_variant is Dictionary else {}
    var task_variant: Variant = payload.get("task", {})
    var task: Dictionary = task_variant if task_variant is Dictionary else {}
    var trajectory_variant: Variant = payload.get("trajectory", {})
    var trajectory: Dictionary = trajectory_variant if trajectory_variant is Dictionary else {}

    var exercise_variant: Variant = payload.get("exercise_parameters", {})
    var exercise_parameters: Dictionary = exercise_variant if exercise_variant is Dictionary else {}
    var authoring_document: Dictionary = request.to_dictionary().duplicate(true)
    authoring_document["producer"] = {
        "seed": seed,
        "difficulty_tier": tier,
        "speed_multiplier": speed,
        "pacing_mode_requested": pacing,
        "pacing_mode_effective": str(exercise_parameters.get("pacing_mode", pacing)),
        "variation_source": "core/authoring/VisualDrillSeedVariation.gd",
        "answer_sheet": task.get("answer_sheet", {}),
        "trajectory": {
            "type": trajectory.get("type", ""),
            "profile": trajectory.get("profile", ""),
            "coordinate_space": trajectory.get("coordinate_space", "")
        }
    }

    _write_json(env_path, envelope)
    _write_json(authoring_path, authoring_document)
    _write_json(root.path_join("response.json"), {
        "ok": true,
        "envelope": env_path,
        "authoring": authoring_path,
        "duration": gameplay_seconds,
        "gameplay_frames": int(round(gameplay_seconds * float(FPS)))
    })
    print("[C11-C-PRODUCER-DRILL] Envelope PASS: %s seed=%d tier=%d speed=%.5f pacing=%s" % [subtype, seed, tier, speed, pacing])
    quit(0)

func _write_json(path: String, data: Dictionary) -> void:
    var file: FileAccess = FileAccess.open(path, FileAccess.WRITE)
    if file == null:
        push_error("Cannot write JSON: %s" % path)
        return
    file.store_string(JSON.stringify(data, "\t"))
    file.close()

func _fail(message: String, request_path: String) -> void:
    printerr("[C11-C-PRODUCER-DRILL] " + message)
    if not request_path.is_empty():
        _write_json(request_path.get_base_dir().path_join("response.json"), {"ok": false, "error": message})
    quit(1)
