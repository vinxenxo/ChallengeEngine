extends SceneTree

## C11-D dynamic request -> in-memory payload binding proof.
## Supports only the three currently pinned representative selector identities.
## It never writes payload/receipt files, creates render nodes, emits renderer input,
## dispatches a renderer, or produces media.

const RuntimeBridge = preload("res://core/execution/ChallengeRuntimeBridge.gd")
const PresentationBinder = preload("res://core/presentation/ChallengePresentationBinder.gd")
const VisualAuthoringGeneratorScript = preload("res://core/authoring/VisualAuthoringGenerator.gd")
const VisualAuthoringRequestScript = preload("res://core/authoring/VisualAuthoringRequest.gd")
const VisualAuthoringAssemblyContextScript = preload("res://core/authoring/VisualAuthoringAssemblyContext.gd")
const C11CVariationProfileScript = preload("res://tools/prototypes/c11c_common/C11CVariationProfile.gd")
const C11CPaletteBankScript = preload("res://tools/prototypes/c11c_common/C11CPaletteBank.gd")
const C11CVisualLoopDurationScript = preload("res://tools/prototypes/c11c_common/C11CVisualLoopDuration.gd")
const FROZEN_C11C_MANIFEST_SHA256 := "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
const OUTPUT_SCHEMA := "C11-D-D9-DYNAMIC-REQUEST-PAYLOAD-MATERIALIZATION-V1"
const CHALLENGE_SOURCE_SHA256 := "6a674c02c2d8831a872691954f1cc40e2492193f9b136f60656730a7be686b71"
const CHALLENGE_ASSETS := [
    {"role":"BACKGROUND", "path":"res://assets/c6/garage_background.svg", "width":1080, "height":1920},
    {"role":"ANIMATED_OBJECT", "path":"res://assets/c6/car.svg", "width":160, "height":320},
    {"role":"TARGET", "path":"res://assets/c6/parking_target.svg", "width":200, "height":400}
]
const LOOP_GRAMMARS: Array[String] = ["harmonic_membrane", "interference_plane", "parametric_ribbon", "lattice_wave", "orbital_wave"]
const ALLOWED_DELIVERY_PROFILES: Array[String] = ["REVIEW_720", "MIN_540", "MASTER_1080", "META_REELS_FINAL_V1"]
const MAX_SEED := 2147483646

func _initialize() -> void:
    call_deferred("_run")

func _run() -> void:
    var input_request: Dictionary = _decode_request()
    var errors: Array[String] = _validate_request(input_request)
    if not errors.is_empty():
        _fail("Invalid dynamic request: %s" % "; ".join(errors))
        return
    var first: Dictionary = _materialize(input_request)
    var second: Dictionary = _materialize(input_request)
    if not bool(first.get("success", false)) or not bool(second.get("success", false)):
        _fail(str(first.get("error", second.get("error", "request payload materialization failed"))))
        return
    var first_hash := _sha256(first.get("payload", {}))
    var second_hash := _sha256(second.get("payload", {}))
    var first_visual_state_hash := str(first.get("visual_state_sha256", ""))
    var second_visual_state_hash := str(second.get("visual_state_sha256", ""))
    if first_hash.is_empty() or first_hash != second_hash:
        _fail("Repeated in-memory payload materialization is not deterministic.")
        return
    if not _is_sha256(first_visual_state_hash) or first_visual_state_hash != second_visual_state_hash:
        _fail("Repeated request produced invalid or different visual-state evidence.")
        return
    var request_selection: Dictionary = input_request.get("selection", {})
    var report: Dictionary = {
        "schema": OUTPUT_SCHEMA,
        "schema_version": "1.0",
        "status": "PREPARATION_ONLY_DYNAMIC_REQUEST_BOUND_IN_MEMORY_INSTANCE_NOT_RENDERER_INPUT",
        "request_id": str(input_request.get("request_id", "")),
        "request_hash": str(input_request.get("request_hash", "")),
        "content_type": str(request_selection.get("content_type", "")),
        "selection": request_selection.duplicate(true),
        "gameplay_seed": int(input_request.get("seed", 0)),
        "music_seed": int(input_request.get("music_seed", 0)),
        "variation_index": int(input_request.get("variation_index", 0)),
        "presentation_profile_id": str(input_request.get("presentation_profile_id", "")),
        "delivery_profile_id": str(input_request.get("delivery_profile_id", "")),
        "payload_sha256": first_hash,
        "visual_state_sha256": first_visual_state_hash,
        "payload_scope": str(first.get("payload_scope", "")),
        "exact_selector_payload_materialized": bool(first.get("exact_selector_payload_materialized", false)),
        "payload_deterministic_repeat": true,
        "payload_materialization": "IN_MEMORY_ONLY",
        "semantic_limits": {
            "music_seed_in_visual_payload": false,
            "variation_index_semantics": "METADATA_ONLY_NOT_A_VISUAL_VARIANT_SELECTOR",
            "delivery_profile_semantics": "IDENTITY_ONLY_PROJECTION_NOT_APPLIED",
            "presentation_geometry": "UNRESOLVED_NOT_APPLIED",
            "editorial_visual_consumption": "NOT_APPLIED",
            "simulation_telemetry_included": false,
            "winning_frame_used_as_timing": false,
            "close_calls_used_as_timing": false
        },
        "execution_boundary": {
            "mode": "GODOT_HEADLESS_IN_MEMORY_DYNAMIC_REQUEST_REVIEW_ONLY",
            "request_input_persisted": false,
            "payload_files_written": false,
            "receipt_files_written": false,
            "renderer_native_input_emitted": false,
            "renderer_dispatch_invoked": false,
            "renderer_activation": false,
            "production_execution": false,
            "media_output_created": false,
            "output_artifact_path": null,
            "c11c_source_mutation": false,
            "d4_8": "BLOCKED",
            "release_authority": "NONE",
            "d9_14": "BLOCKED_AS_REQUIRED",
            "d9_16": "BLOCKED_AS_REQUIRED",
            "d9_17": "BLOCKED_NO_GO",
            "d10": "BLOCKED"
        }
    }
    print("C11-D DYNAMIC REQUEST PAYLOAD MATERIALIZATION SUMMARY=" + JSON.stringify(report))
    print("C11-D DYNAMIC REQUEST PAYLOAD MATERIALIZATION PASS | content_type=%s | deterministic=2/2 | gameplay_seed=%d | music_seed_visual_influence=NONE | variation_index=METADATA_ONLY | payload_files=NONE | renderer_input=NOT_EMITTED | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE" % [report["content_type"], int(input_request.get("seed", 0))])
    quit(0)

func _decode_request() -> Dictionary:
    var args: PackedStringArray = OS.get_cmdline_user_args()
    if args.size() != 1:
        return {}
    var raw_text: String = Marshalls.base64_to_utf8(args[0])
    var parsed: Variant = JSON.parse_string(raw_text)
    if not (parsed is Dictionary):
        return {}
    return parsed

func _validate_request(value: Dictionary) -> Array[String]:
    var errors: Array[String] = []
    var expected_keys := ["schema", "schema_version", "request_id", "request_hash", "selection", "seed", "music_seed", "variation_index", "presentation_profile_id", "delivery_profile_id"]
    var actual_keys: Array = value.keys()
    actual_keys.sort()
    expected_keys.sort()
    if actual_keys != expected_keys:
        errors.append("request envelope keys are not exact")
        return errors
    if str(value.get("schema", "")) != "C11-D-D9-DYNAMIC-REQUEST-PAYLOAD-INPUT-V1" or str(value.get("schema_version", "")) != "1.0":
        errors.append("request input schema identity/version mismatch")
    if not _is_sha256(str(value.get("request_hash", ""))):
        errors.append("canonical request hash is malformed")
    var request_id := str(value.get("request_id", ""))
    if request_id.is_empty() or request_id.length() > 160:
        errors.append("request_id is missing or oversized")
    else:
        var request_id_pattern := RegEx.new()
        var regex_error := request_id_pattern.compile("^[A-Za-z0-9_.-]+$")
        if regex_error != OK or request_id_pattern.search(request_id) == null:
            errors.append("request_id contains characters outside the canonical D9.9 envelope domain")
    # Godot's JSON parser may represent JSON numbers as TYPE_FLOAT even when
    # the source JSON literal is an integer. Accept integer-valued numbers only;
    # reject booleans, fractions, infinities/NaN and values outside canonical bounds.
    # The upstream Python JSON Schema validation independently constrains these fields.
    for key in ["seed", "music_seed"]:
        var item: Variant = value.get(key, null)
        if not _is_json_integer_in_range(item, 1, MAX_SEED):
            errors.append("%s must be an integer in the canonical D9.9 seed domain" % key)
    var variation: Variant = value.get("variation_index", null)
    if not _is_json_integer_in_range(variation, 0, 1000000):
        errors.append("variation_index is outside the canonical D9.9 domain")
    if str(value.get("presentation_profile_id", "")) != "social_default_v1":
        errors.append("only the reviewed social_default_v1 presentation identity is in scope")
    if not ALLOWED_DELIVERY_PROFILES.has(str(value.get("delivery_profile_id", ""))):
        errors.append("delivery profile is not an admitted non-Longform profile")
    var selection: Variant = value.get("selection", null)
    if not (selection is Dictionary):
        errors.append("selection must be an object")
        return errors
    var selection_keys: Array = selection.keys()
    selection_keys.sort()
    var expected_selection_keys := ["content_type", "family_id", "subtype_id", "variant_id"]
    expected_selection_keys.sort()
    if selection_keys != expected_selection_keys:
        errors.append("selection keys are not exact")
        return errors
    var content_type := str(selection.get("content_type", ""))
    if content_type == "challenges":
        if str(selection.get("family_id", "")) != "parking_v2" or str(selection.get("variant_id", "")) != "CHALLENGE_004" or selection.get("subtype_id", null) != null:
            errors.append("Challenge selector is outside the pinned CHALLENGE_004 / parking_v2 scope")
    elif content_type == "visual_loops":
        if str(selection.get("family_id", "")) != "c11c_geometric_waves_v1" or str(selection.get("subtype_id", "")) != "harmonic_membrane" or selection.get("variant_id", null) != null:
            errors.append("Visual Loop selector is outside the pinned geometric / harmonic_membrane scope")
    elif content_type == "visual_drills":
        if str(selection.get("family_id", "")) != "tracking" or str(selection.get("variant_id", "")) != "tier-2" or selection.get("subtype_id", null) != null:
            errors.append("Visual Drill selector is outside the pinned tracking / tier-2 scope")
    else:
        errors.append("unsupported content type; Longform remains disabled")
    return errors

func _materialize(input_request: Dictionary) -> Dictionary:
    var selection: Dictionary = input_request["selection"]
    match str(selection["content_type"]):
        "challenges":
            return _build_challenge_payload(int(input_request["seed"]))
        "visual_loops":
            return _build_visual_loop_payload(int(input_request["seed"]))
        "visual_drills":
            return _build_visual_drill_payload(int(input_request["seed"]))
    return {"success": false, "error": "Unsupported content type."}

func _build_visual_loop_payload(seed: int) -> Dictionary:
    var variation: Dictionary = C11CVariationProfileScript.build("geometric", seed)
    var grammar_index: int = LOOP_GRAMMARS.find("harmonic_membrane")
    if grammar_index < 0:
        return {"success": false, "error": "Selected grammar is absent from the frozen C11-C grammar list."}
    variation["grammar_mode"] = grammar_index
    variation["grammar_name"] = "harmonic_membrane"
    var loop_cycles: int = int(round(float(variation.get("loop_cycles", 1.0))))
    var duration_seconds: float = float(C11CVisualLoopDurationScript.policy_seconds_for_cycles(loop_cycles))
    var frame_count: int = int(round(duration_seconds * 30.0))
    var palette: Dictionary = C11CPaletteBankScript.palette("geometric", int(variation.get("palette_mode", 0)), seed)
    var request: VisualAuthoringRequest = VisualAuthoringRequestScript.new("visual_loop", "geometric", duration_seconds, 30, 2, {"color_palette": str(variation.get("palette_name", "default"))})
    var context: VisualAuthoringAssemblyContext = _make_context(seed, "visual_loop", "c11c_geometric_waves_v1")
    var generated: Dictionary = VisualAuthoringGeneratorScript.generate(request, context, {})
    if not bool(generated.get("success", false)):
        return {"success": false, "error": "Visual Loop authoring rejected request: %s" % str(generated.get("errors", []))}
    var envelope: Dictionary = generated.get("content", {})
    var envelope_payload: Dictionary = envelope.get("payload", {})
    if envelope.get("kind") != "visual_loop" or envelope.get("subtype") != "geometric":
        return {"success": false, "error": "Visual Loop envelope identity mismatch."}
    if int(envelope_payload.get("fps", -1)) != 30 or int(envelope_payload.get("frame_count", -1)) != frame_count or float(envelope_payload.get("duration", -1.0)) != duration_seconds:
        return {"success": false, "error": "Visual Loop canonical duration/frame relationship mismatch."}
    var layers: Array = envelope_payload.get("visual_parameters", {}).get("layers", [])
    if layers.is_empty() or str(layers[0].get("color_palette", "")) != str(variation.get("palette_name", "")):
        return {"success": false, "error": "Seeded palette was not present in the materialized Visual Loop envelope."}
    var visual_palette: Dictionary = palette.duplicate(true)
    visual_palette.erase("palette_variant_seed")
    var visual_state_sha256: String = _sha256({
        "family_variation": variation,
        "palette": visual_palette,
        "authoring_visual_parameters": envelope_payload.get("visual_parameters", {}),
        "timing": {"fps":30, "duration_seconds":duration_seconds, "frame_count":frame_count}
    })
    var payload: Dictionary = {
        "instance_schema": "C11-D-REVIEW-ONLY-DYNAMIC-VISUAL-LOOP-PAYLOAD-V1",
        "source_identity": {"content_type":"visual_loops", "family_id":"c11c_geometric_waves_v1", "subtype_id":"harmonic_membrane", "gameplay_seed":seed, "presentation_profile_id":"social_default_v1"},
        "authoring_envelope": envelope,
        "family_variation_recipe": variation,
        "resolved_palette": palette,
        "timing": {"fps":30, "duration_seconds":duration_seconds, "frame_count":frame_count, "duration_source":"C11CVisualLoopDuration.policy_seconds_for_cycles"}
    }
    return {"success":true, "payload":payload, "visual_state_sha256":visual_state_sha256, "payload_scope":"VISUAL_LOOP_FAMILY_ENVELOPE_GRAMMAR_INSTANCE_UNRESOLVED", "exact_selector_payload_materialized":false}

func _build_visual_drill_payload(seed: int) -> Dictionary:
    var duration_seconds: float = 21.0
    var frame_count: int = int(round(duration_seconds * 30.0))
    var request: VisualAuthoringRequest = VisualAuthoringRequestScript.new("visual_drill", "tracking", duration_seconds, 30, 2, {})
    var context: VisualAuthoringAssemblyContext = _make_context(seed, "visual_drill", "tracking")
    var generated: Dictionary = VisualAuthoringGeneratorScript.generate(request, context, {})
    if not bool(generated.get("success", false)):
        return {"success":false, "error":"Visual Drill authoring rejected request: %s" % str(generated.get("errors", []))}
    var envelope: Dictionary = generated.get("content", {})
    var envelope_payload: Dictionary = envelope.get("payload", {})
    var exercise: Dictionary = envelope_payload.get("exercise_parameters", {})
    var trajectory: Dictionary = envelope_payload.get("trajectory", {})
    var seed_motion: Dictionary = envelope_payload.get("seed_motion", {})
    if envelope.get("kind") != "visual_drill" or envelope.get("subtype") != "tracking":
        return {"success":false, "error":"Visual Drill envelope identity mismatch."}
    if int(exercise.get("difficulty_tier", -1)) != 2 or str(exercise.get("generator", "")) != "tracking":
        return {"success":false, "error":"Selected Drill tier/generator was not materialized."}
    if int(envelope_payload.get("fps", -1)) != 30 or int(envelope_payload.get("frame_count", -1)) != frame_count or float(envelope_payload.get("duration", -1.0)) != duration_seconds:
        return {"success":false, "error":"Visual Drill duration/frame relationship mismatch."}
    if seed_motion.is_empty() or int(seed_motion.get("seed", -1)) != seed or trajectory.get("seed_authoring_version") != "2.9.0":
        return {"success":false, "error":"Seed-bound VisualDrillSeedVariation was not materialized."}
    var visual_trajectory: Dictionary = trajectory.duplicate(true)
    visual_trajectory.erase("seed_authoring_version")
    visual_trajectory.erase("seed_motion_variant")
    var visual_motion: Dictionary = seed_motion.duplicate(true)
    visual_motion.erase("seed")
    visual_motion.erase("version")
    visual_motion.erase("enabled")
    var visual_state_sha256: String = _sha256({"trajectory":visual_trajectory, "seed_motion_parameters":visual_motion})
    var payload: Dictionary = {
        "instance_schema":"C11-D-REVIEW-ONLY-DYNAMIC-VISUAL-DRILL-PAYLOAD-V1",
        "source_identity":{"content_type":"visual_drills", "family_id":"tracking", "variant_id":"tier-2", "gameplay_seed":seed, "presentation_profile_id":"social_default_v1"},
        "authoring_envelope":envelope,
        "timing":{"fps":30, "duration_seconds":duration_seconds, "frame_count":frame_count, "duration_source":"definitions/visual_drill_tracking_canonical.json"}
    }
    return {"success":true, "payload":payload, "visual_state_sha256":visual_state_sha256, "payload_scope":"VISUAL_DRILL_TIER_SEED_PAYLOAD", "exact_selector_payload_materialized":true}

func _build_challenge_payload(seed: int) -> Dictionary:
    var manifest_bytes: PackedByteArray = FileAccess.get_file_as_bytes("res://release/C11C_FREEZE_PACKAGE_MANIFEST.json")
    if manifest_bytes.is_empty() or _sha256_bytes(manifest_bytes) != FROZEN_C11C_MANIFEST_SHA256:
        return {"success":false, "error":"Frozen C11-C manifest SHA-256 mismatch."}
    var source_bytes: PackedByteArray = FileAccess.get_file_as_bytes("res://challenges/CHALLENGE_004.json")
    if source_bytes.is_empty() or _sha256_bytes(source_bytes) != CHALLENGE_SOURCE_SHA256:
        return {"success":false, "error":"Pinned CHALLENGE_004 source bytes/hash mismatch."}
    var source_value: Variant = JSON.parse_string(source_bytes.get_string_from_utf8())
    if not (source_value is Dictionary):
        return {"success":false, "error":"Canonical Challenge source is not a JSON object."}
    var source: Dictionary = source_value.duplicate(true)
    if str(source.get("challenge_id", "")) != "CHALLENGE_004" or str(source.get("mechanic", "")) != "parking_v2":
        return {"success":false, "error":"Challenge identity mismatch."}
    var generation: Dictionary = source.get("generation", {}).duplicate(true)
    generation["seed"] = seed
    source["generation"] = generation
    var first_result: Dictionary = RuntimeBridge.run_effective_pipeline(source.duplicate(true))
    var second_result: Dictionary = RuntimeBridge.run_effective_pipeline(source.duplicate(true))
    if not bool(first_result.get("success", false)) or not bool(second_result.get("success", false)):
        return {"success":false, "error":"Challenge runtime failed for the dynamic request seed."}
    var first_context: Variant = first_result.get("context", null)
    var second_context: Variant = second_result.get("context", null)
    if first_context == null or second_context == null or first_context.simulation_result == null or second_context.simulation_result == null or first_context.timeline == null:
        return {"success":false, "error":"Challenge runtime returned an incomplete source payload."}
    var first_sim: Variant = first_context.simulation_result
    var second_sim: Variant = second_context.simulation_result
    if int(first_sim.frames.size()) != 420 or int(second_sim.frames.size()) != 420 or int(first_context.timeline.total_frames) != 900:
        return {"success":false, "error":"Challenge source-timebase frame counts diverged."}
    var canonical: Dictionary = first_context.canonical_v2.duplicate(true)
    var presentation: Dictionary = canonical.get("presentation", {}).duplicate(true)
    presentation["profile_id"] = "social_default_v1"
    canonical["presentation"] = presentation
    var binding: Variant = PresentationBinder.bind(canonical, first_context.timeline, first_sim)
    if binding == null or not bool(binding.success) or binding.presentation_profile == null or str(binding.presentation_profile.profile_id) != "social_default_v1":
        return {"success":false, "error":"D Challenge presentation identity rebind failed."}
    var assets: Array[Dictionary] = []
    for spec_value: Variant in CHALLENGE_ASSETS:
        var spec: Dictionary = spec_value
        var path: String = str(spec["path"])
        var bytes: PackedByteArray = FileAccess.get_file_as_bytes(path)
        var resource: Resource = ResourceLoader.load(path) as Resource
        if bytes.is_empty() or resource == null or not (resource is Texture2D):
            return {"success":false, "error":"Canonical Challenge visual asset failed to load: %s" % path}
        var texture: Texture2D = resource as Texture2D
        if int(texture.get_width()) != int(spec["width"]) or int(texture.get_height()) != int(spec["height"]):
            return {"success":false, "error":"Canonical Challenge asset dimension mismatch: %s" % path}
        assets.append({"role":str(spec["role"]), "resource_path":path, "sha256":_sha256_bytes(bytes), "intrinsic_width":int(texture.get_width()), "intrinsic_height":int(texture.get_height())})
    var game_records: Array[Dictionary] = []
    for index: int in range(first_sim.frames.size()):
        var frame: Variant = first_sim.frames[index]
        if frame == null or not frame.is_valid_snapshot():
            return {"success":false, "error":"Invalid simulation visual snapshot at GAME index %d." % index}
        game_records.append({
            "source_game_frame_index":index,
            "position":{"x":float(frame.position.x), "y":float(frame.position.y)},
            "rotation_radians":float(frame.rotation),
            "scale":{"x":float(frame.scale.x), "y":float(frame.scale.y)},
            "opacity":float(frame.opacity),
            "texture_index":int(frame.texture_index),
            "variant_id":int(frame.variant_id)
        })
    var repeat_records: Array[Dictionary] = []
    for index: int in range(second_sim.frames.size()):
        var frame: Variant = second_sim.frames[index]
        if frame == null or not frame.is_valid_snapshot():
            return {"success":false, "error":"Repeated simulation snapshot invalid at GAME index %d." % index}
        repeat_records.append({
            "source_game_frame_index":index,
            "position":{"x":float(frame.position.x), "y":float(frame.position.y)},
            "rotation_radians":float(frame.rotation),
            "scale":{"x":float(frame.scale.x), "y":float(frame.scale.y)},
            "opacity":float(frame.opacity),
            "texture_index":int(frame.texture_index),
            "variant_id":int(frame.variant_id)
        })
    var first_signature := _sha256(game_records)
    var second_signature := _sha256(repeat_records)
    if game_records.size() != 420 or first_signature.is_empty() or first_signature != second_signature:
        return {"success":false, "error":"Repeated Challenge GAME visual frames differ."}
    var render_model: Dictionary = binding.presentation_render_model
    var payload: Dictionary = {
        "instance_schema":"C11-D-REVIEW-ONLY-DYNAMIC-CHALLENGE-VISUAL-PAYLOAD-V1",
        "source_identity":{"content_type":"challenges", "challenge_id":"CHALLENGE_004", "mechanic":"parking_v2", "gameplay_seed":seed, "presentation_profile_id":"social_default_v1"},
        "challenge_source_sha256":CHALLENGE_SOURCE_SHA256,
        "source_timebase":{"fps":60, "total_frames":900, "game_frame_count":420},
        "asset_nodes":assets,
        "game_visual_frames":game_records,
        "game_visual_frames_sha256":first_signature,
        "presentation_render_model_sha256":_sha256(render_model),
        "semantics":{"source_frame_sampling":"PRESERVE_ALL_SOURCE_GAME_FRAMES", "delivery_resampling":"UNRESOLVED_NOT_APPLIED", "coordinate_projection":"UNRESOLVED_NOT_APPLIED", "simulation_telemetry_included":false, "winning_frame_used_as_timing":false, "close_calls_used_as_timing":false}
    }
    return {"success":true, "payload":payload, "visual_state_sha256":first_signature, "payload_scope":"CHALLENGE_RUNTIME_VISUAL_PAYLOAD_SOURCE_TIMEBASE", "exact_selector_payload_materialized":true}

func _make_context(seed: int, content_kind: String, asset_family_id: String) -> VisualAuthoringAssemblyContext:
    return VisualAuthoringAssemblyContextScript.new(
        seed,
        "2.0",
        "C11D-DYNAMIC-" + content_kind.to_upper(),
        "1.0",
        "C11-C-2.19.12",
        {"profile_id":"social_default_v1", "coordinate_space":"CANVAS_540X960"},
        {"family_id":asset_family_id},
        {"profile_id":"default_procedural_music", "enabled":true},
        {"author":"C11D_DYNAMIC_REQUEST_IN_MEMORY_REVIEW", "timestamp_ms":0}
    )

func _stable_value(value: Variant) -> Variant:
    if value is Dictionary:
        var keys: Array = value.keys()
        keys.sort()
        var result: Dictionary = {}
        for key in keys:
            result[str(key)] = _stable_value(value[key])
        return result
    if value is Array:
        var result_array: Array = []
        for item in value:
            result_array.append(_stable_value(item))
        return result_array
    return value

func _sha256(value: Variant) -> String:
    var ctx := HashingContext.new()
    if ctx.start(HashingContext.HASH_SHA256) != OK:
        return ""
    ctx.update(JSON.stringify(_stable_value(value)).to_utf8_buffer())
    return ctx.finish().hex_encode()

func _sha256_bytes(value: PackedByteArray) -> String:
    var ctx := HashingContext.new()
    if ctx.start(HashingContext.HASH_SHA256) != OK:
        return ""
    ctx.update(value)
    return ctx.finish().hex_encode()

func _is_json_integer_in_range(value: Variant, minimum: int, maximum: int) -> bool:
    var value_type: int = typeof(value)
    if value_type != TYPE_INT and value_type != TYPE_FLOAT:
        return false
    var numeric: float = float(value)
    if not is_finite(numeric):
        return false
    if numeric < float(minimum) or numeric > float(maximum):
        return false
    return floor(numeric) == numeric

func _is_sha256(value: String) -> bool:
    if value.length() != 64 or value != value.to_lower():
        return false
    for character in value:
        if not "0123456789abcdef".contains(character):
            return false
    return true

func _fail(message: String) -> void:
    push_error("DYNAMIC REQUEST PAYLOAD MATERIALIZATION FAIL: " + message)
    print("C11-D DYNAMIC REQUEST PAYLOAD MATERIALIZATION FAIL | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
    quit(1)
