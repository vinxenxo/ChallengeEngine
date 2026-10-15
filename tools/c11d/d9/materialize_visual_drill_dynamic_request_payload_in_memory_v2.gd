extends SceneTree

## C11-D D9 renderer dynamic-request payload binder extension V2.
## Visual Drill selector/tier payloads only: preparation review in memory, never renderer input.
const VisualAuthoringGeneratorScript = preload("res://core/authoring/VisualAuthoringGenerator.gd")
const VisualAuthoringRequestScript = preload("res://core/authoring/VisualAuthoringRequest.gd")
const VisualAuthoringAssemblyContextScript = preload("res://core/authoring/VisualAuthoringAssemblyContext.gd")
const FROZEN_C11C_MANIFEST_SHA256 := "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
const INPUT_SCHEMA := "C11-D-D9-DYNAMIC-REQUEST-PAYLOAD-INPUT-V2"
const OUTPUT_SCHEMA := "C11-D-D9-VISUAL-DRILL-REQUEST-PAYLOAD-MATERIALIZATION-V2"
const OUTPUT_SUMMARY_PREFIX := "C11-D DYNAMIC REQUEST PAYLOAD MATERIALIZATION SUMMARY="
const PAYLOAD_SCOPE := "VISUAL_DRILL_REQUEST_SELECTOR_TIER_PAYLOAD_V2"
const ALLOWED_DELIVERY_PROFILES: Array[String] = ["REVIEW_720", "MIN_540", "MASTER_1080", "META_REELS_FINAL_V1"]
const FAMILIES: Array[String] = ["peripheral_scan", "pursuit", "saccade", "tracking"]
const TIERS: Array[String] = ["tier-1", "tier-2", "tier-3", "tier-4", "tier-5"]
const MAX_SEED := 2147483646

# These pins cover every canonical definition/policy and every shared authoring component
# used to resolve the request. The Python contract validates the same bytes independently.
const SOURCE_PINS := {
    "release/C11C_FREEZE_PACKAGE_MANIFEST.json": "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953",
    "definitions/visual_drill_tracking_canonical.json": "54d432c80f190f4ac5dcb8ef5b135e16f18c378da120f35723fd5be944719ec3",
    "definitions/visual_drill_pursuit_canonical.json": "dfe2bce9913df8ebe4f92d06eec5d22736338214e71b497dde3562a6927600bc",
    "definitions/visual_drill_saccade_canonical.json": "daba3fa558f6898a17107ab68894d15c58fa5b2127e8da7d7b11b203f4ddfaa1",
    "definitions/visual_drill_peripheral_scan_canonical.json": "aaf50f9223bad678df15589110dfcd6ff42dda89326a0a84bc5a5f51d133a904",
    "profiles/difficulty/visual_drill_tracking.json": "6de8812bd46904e122ecdd0eae22fb2979bd75399c34779248c6569e833c921e",
    "profiles/difficulty/visual_drill_pursuit.json": "ab6a29af53bdb45fb6976bfdd558e3275c477eb7ad9afd61b9d01e36d43afb05",
    "profiles/difficulty/visual_drill_saccade.json": "6be50f582ef5ce11d36b72943750b88e72da67d858d67c3ac3d38d33c11ccf38",
    "profiles/difficulty/visual_drill_peripheral_scan.json": "7c52112bf9c106152d7fe03b646bde0f415881a04efb75560d731fa3f18fa73e",
    "core/authoring/VisualAuthoringGenerator.gd": "abbe109b7ca625dce7a044bb6dc37582a6b6ee5156faa439c63c420a5758195e",
    "core/authoring/VisualAuthoringRequest.gd": "02100b371603167964c20f127e984f8968e03af08016cc60cc820e0e2e37b0c1",
    "core/authoring/VisualAuthoringAssemblyContext.gd": "c57fc199d7c3ef46b0fae0d7be8d70090c816979184c259908b0484138b1f896",
    "core/authoring/VisualAuthoringRequestValidator.gd": "85eb9ec5050a78133bacb54d34a4a5464f014a41feff3599e5a2f8e76a14a30c",
    "core/authoring/VisualAuthoringRegistry.gd": "f39ec38bfa39723c88bbcb067b8ea2d2052aa5ef2b8e66653431650518156af8",
    "core/authoring/VisualAuthoringPolicyRegistry.gd": "f84a94566900aff055813f537892577c929caa1d11c76f7187faf33ca52de437",
    "core/authoring/VisualDifficultyResolver.gd": "8f46acb2b54dba99de19db7290883a5849037afb336eb21c5f725f29ee4ecd8b",
    "core/authoring/VisualDrillSeedVariation.gd": "ecd07dca143886fac355c040b1bfcee3badb7dacbe4abd95ed340c4dcb8a3567",
    "core/authoring/adapters/VisualDrillAuthoringAdapter.gd": "d0b547b032101c592912cf4db25ba787a6aa4a6e7b4c01211397ea187502a263"
}

func _initialize() -> void:
    call_deferred("_run")

func _run() -> void:
    var input_request: Dictionary = _decode_request()
    var errors: Array[String] = _validate_request(input_request)
    if not errors.is_empty():
        _fail("Invalid Visual Drill dynamic request: %s" % "; ".join(errors))
        return
    var first: Dictionary = _materialize(input_request)
    var second: Dictionary = _materialize(input_request)
    if not bool(first.get("success", false)) or not bool(second.get("success", false)):
        _fail(str(first.get("error", second.get("error", "Visual Drill payload materialization failed"))))
        return
    var first_hash := _sha256(first.get("payload", {}))
    var second_hash := _sha256(second.get("payload", {}))
    var first_visual_state_hash := str(first.get("visual_state_sha256", ""))
    var second_visual_state_hash := str(second.get("visual_state_sha256", ""))
    if first_hash.is_empty() or first_hash != second_hash:
        _fail("Repeated in-memory selector/tier payload materialization is not deterministic.")
        return
    if not _is_sha256(first_visual_state_hash) or first_visual_state_hash != second_visual_state_hash:
        _fail("Repeated selector/tier request produced invalid or different visual-state evidence.")
        return
    var selection: Dictionary = input_request["selection"]
    var report: Dictionary = {
        "schema": OUTPUT_SCHEMA,
        "schema_version": "2.0",
        "status": "PREPARATION_ONLY_DYNAMIC_REQUEST_BOUND_IN_MEMORY_INSTANCE_NOT_RENDERER_INPUT",
        "request_id": str(input_request["request_id"]),
        "request_hash": str(input_request["request_hash"]),
        "content_type": "visual_drills",
        "selection": selection.duplicate(true),
        "gameplay_seed": int(input_request["seed"]),
        "music_seed": int(input_request["music_seed"]),
        "variation_index": int(input_request["variation_index"]),
        "presentation_profile_id": str(input_request["presentation_profile_id"]),
        "delivery_profile_id": str(input_request["delivery_profile_id"]),
        "payload_sha256": first_hash,
        "visual_state_sha256": first_visual_state_hash,
        "payload_scope": PAYLOAD_SCOPE,
        "exact_selector_payload_materialized": true,
        "grammar_parameter_evidence": null,
        "visual_drill_authoring_evidence": first["visual_drill_authoring_evidence"].duplicate(true),
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
    print(OUTPUT_SUMMARY_PREFIX + JSON.stringify(report))
    print("C11-D VISUAL DRILL DYNAMIC REQUEST MATERIALIZATION PASS | family=%s | tier=%s | deterministic_repeat=2/2 | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE" % [str(selection["family_id"]), str(selection["variant_id"])])
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
    if str(value.get("schema", "")) != INPUT_SCHEMA or str(value.get("schema_version", "")) != "2.0":
        errors.append("request input schema identity/version mismatch")
    if not _is_sha256(str(value.get("request_hash", ""))):
        errors.append("canonical request hash is malformed")
    var request_id := str(value.get("request_id", ""))
    if request_id.is_empty() or request_id.length() > 160:
        errors.append("request_id is missing or oversized")
    else:
        var id_pattern := RegEx.new()
        if id_pattern.compile("^[A-Za-z0-9_.-]+$") != OK or id_pattern.search(request_id) == null:
            errors.append("request_id contains unsupported characters")
    for key in ["seed", "music_seed"]:
        if not _is_json_integer_in_range(value.get(key, null), 1, MAX_SEED):
            errors.append("%s is outside the canonical seed domain" % key)
    if not _is_json_integer_in_range(value.get("variation_index", null), 0, 1000000):
        errors.append("variation_index is outside the canonical D9.9 domain")
    if str(value.get("presentation_profile_id", "")) != "social_default_v1":
        errors.append("presentation profile is not admitted")
    if not ALLOWED_DELIVERY_PROFILES.has(str(value.get("delivery_profile_id", ""))):
        errors.append("delivery profile is not admitted")
    var selection: Variant = value.get("selection", null)
    if not (selection is Dictionary):
        errors.append("selection must be an object")
        return errors
    var keys: Array = selection.keys()
    keys.sort()
    var wanted := ["content_type", "family_id", "subtype_id", "variant_id"]
    wanted.sort()
    if keys != wanted:
        errors.append("selection keys are not exact")
        return errors
    var family := str(selection.get("family_id", ""))
    var variant := str(selection.get("variant_id", ""))
    if str(selection.get("content_type", "")) != "visual_drills" or not FAMILIES.has(family) or not TIERS.has(variant) or selection.get("subtype_id", null) != null:
        errors.append("selector/tier is outside the exact 4-family × tier-1..5 matrix")
    return errors

func _materialize(input_request: Dictionary) -> Dictionary:
    var selection: Dictionary = input_request["selection"]
    var family := str(selection["family_id"])
    var variant := str(selection["variant_id"])
    var tier := int(variant.trim_prefix("tier-"))
    var canonical_path := "definitions/visual_drill_%s_canonical.json" % family
    var policy_path := "profiles/difficulty/visual_drill_%s.json" % family
    var pin_error := _verify_source_pins()
    if not pin_error.is_empty():
        return {"success":false, "error":pin_error}
    var canonical_bytes: PackedByteArray = FileAccess.get_file_as_bytes("res://" + canonical_path)
    var policy_bytes: PackedByteArray = FileAccess.get_file_as_bytes("res://" + policy_path)
    var canonical_value: Variant = JSON.parse_string(canonical_bytes.get_string_from_utf8())
    var policy_value: Variant = JSON.parse_string(policy_bytes.get_string_from_utf8())
    if not (canonical_value is Dictionary) or not (policy_value is Dictionary):
        return {"success":false, "error":"Pinned canonical source/policy is not a JSON object."}
    var canonical: Dictionary = canonical_value
    var policy: Dictionary = policy_value
    if str(canonical.get("subtype", "")) != family or str(policy.get("domain_family", "")) != "visual_drill" or str(policy.get("subtype", "")) != family:
        return {"success":false, "error":"Canonical definition/policy identity mismatch."}
    var canonical_payload: Dictionary = canonical.get("payload", {})
    var duration_seconds := float(canonical_payload.get("duration", -1.0))
    var fps := int(canonical_payload.get("fps", -1))
    var frame_count := int(canonical_payload.get("frame_count", -1))
    if duration_seconds <= 0.0 or fps != 30 or frame_count < 1 or frame_count != int(round(duration_seconds * float(fps))):
        return {"success":false, "error":"Canonical duration/fps/frame_count relationship is invalid."}
    var tiers: Dictionary = policy.get("tiers", {})
    if not tiers.has(str(tier)) or tiers.size() != 5:
        return {"success":false, "error":"Selected tier is absent from pinned difficulty policy."}
    var request: VisualAuthoringRequest = VisualAuthoringRequestScript.new("visual_drill", family, duration_seconds, fps, tier, {})
    var context: VisualAuthoringAssemblyContext = _make_context(int(input_request["seed"]), family)
    var generated: Dictionary = VisualAuthoringGeneratorScript.generate(request, context, {})
    if not bool(generated.get("success", false)):
        return {"success":false, "error":"Canonical Visual Drill authoring rejected request: %s" % str(generated.get("errors", []))}
    var envelope: Dictionary = generated.get("content", {})
    var payload_source: Dictionary = envelope.get("payload", {})
    var exercise: Dictionary = payload_source.get("exercise_parameters", {})
    var trajectory: Dictionary = payload_source.get("trajectory", {})
    var seed_motion: Dictionary = payload_source.get("seed_motion", {})
    var task: Dictionary = payload_source.get("task", {})
    if str(envelope.get("kind", "")) != "visual_drill" or str(envelope.get("subtype", "")) != family:
        return {"success":false, "error":"Authoring adapter envelope selector identity mismatch."}
    if int(exercise.get("difficulty_tier", -1)) != tier or str(exercise.get("generator", "")) != family or str(task.get("type", "")) != family:
        return {"success":false, "error":"Selected tier/generator/task was not exactly materialized."}
    if int(payload_source.get("fps", -1)) != fps or int(payload_source.get("frame_count", -1)) != frame_count or abs(float(payload_source.get("duration", -1.0)) - duration_seconds) > 0.000001:
        return {"success":false, "error":"Materialized timing diverges from canonical definition."}
    if seed_motion.is_empty() or int(seed_motion.get("seed", -1)) != int(input_request["seed"]) or str(trajectory.get("seed_authoring_version", "")) != "2.9.0":
        return {"success":false, "error":"Seed-bound VisualDrillSeedVariation evidence is missing or inconsistent."}
    var visual_trajectory: Dictionary = trajectory.duplicate(true)
    for key in ["seed_authoring_version", "seed_motion_variant", "seed_spatial_variant"]:
        visual_trajectory.erase(key)
    var visual_motion: Dictionary = seed_motion.duplicate(true)
    for key in ["seed", "version", "enabled", "family"]:
        visual_motion.erase(key)
    var visual_state_sha256 := _sha256({"trajectory":visual_trajectory, "seed_motion_parameters":visual_motion, "exercise_parameters":exercise.duplicate(true)})
    var authoring_evidence: Dictionary = _authoring_evidence(family, variant, tier, canonical_path, policy_path, canonical_bytes, policy_bytes, generated, exercise, payload_source, duration_seconds, fps, frame_count, int(input_request["seed"]))
    var payload: Dictionary = {
        "instance_schema":"C11-D-REVIEW-ONLY-DYNAMIC-VISUAL-DRILL-PAYLOAD-V2",
        "source_identity":{"content_type":"visual_drills", "family_id":family, "variant_id":variant, "gameplay_seed":int(input_request["seed"]), "presentation_profile_id":"social_default_v1"},
        "authoring_evidence":authoring_evidence.duplicate(true),
        "authoring_envelope":envelope,
        "timing":{"fps":fps, "duration_seconds":duration_seconds, "frame_count":frame_count, "duration_source":canonical_path}
    }
    return {"success":true, "payload":payload, "visual_state_sha256":visual_state_sha256, "payload_scope":PAYLOAD_SCOPE, "exact_selector_payload_materialized":true, "visual_drill_authoring_evidence":authoring_evidence}

func _authoring_evidence(family: String, variant: String, tier: int, canonical_path: String, policy_path: String, canonical_bytes: PackedByteArray, policy_bytes: PackedByteArray, generated: Dictionary, exercise: Dictionary, payload_source: Dictionary, duration_seconds: float, fps: int, frame_count: int, seed: int) -> Dictionary:
    var parameters: Dictionary = generated.get("effective_parameters", {})
    var materialized_task: Dictionary = payload_source.get("task", {})
    var pins: Dictionary = {
        "policy_registry_path":"core/authoring/VisualAuthoringPolicyRegistry.gd",
        "policy_registry_sha256":str(SOURCE_PINS["core/authoring/VisualAuthoringPolicyRegistry.gd"]),
        "difficulty_resolver_path":"core/authoring/VisualDifficultyResolver.gd",
        "difficulty_resolver_sha256":str(SOURCE_PINS["core/authoring/VisualDifficultyResolver.gd"]),
        "authoring_registry_path":"core/authoring/VisualAuthoringRegistry.gd",
        "authoring_registry_sha256":str(SOURCE_PINS["core/authoring/VisualAuthoringRegistry.gd"]),
        "authoring_generator_path":"core/authoring/VisualAuthoringGenerator.gd",
        "authoring_generator_sha256":str(SOURCE_PINS["core/authoring/VisualAuthoringGenerator.gd"]),
        "request_validator_path":"core/authoring/VisualAuthoringRequestValidator.gd",
        "request_validator_sha256":str(SOURCE_PINS["core/authoring/VisualAuthoringRequestValidator.gd"]),
        "visual_drill_adapter_path":"core/authoring/adapters/VisualDrillAuthoringAdapter.gd",
        "visual_drill_adapter_sha256":str(SOURCE_PINS["core/authoring/adapters/VisualDrillAuthoringAdapter.gd"]),
        "seed_variation_path":"core/authoring/VisualDrillSeedVariation.gd",
        "seed_variation_sha256":str(SOURCE_PINS["core/authoring/VisualDrillSeedVariation.gd"]),
        "request_model_path":"core/authoring/VisualAuthoringRequest.gd",
        "request_model_sha256":str(SOURCE_PINS["core/authoring/VisualAuthoringRequest.gd"]),
        "assembly_context_path":"core/authoring/VisualAuthoringAssemblyContext.gd",
        "assembly_context_sha256":str(SOURCE_PINS["core/authoring/VisualAuthoringAssemblyContext.gd"])
    }
    return {
        "content_type":"visual_drills",
        "family_id":family,
        "variant_id":variant,
        "authoring_domain_family":"visual_drill",
        "authoring_subtype":family,
        "difficulty_tier":tier,
        "canonical_source_path":canonical_path,
        "canonical_source_sha256":_sha256_bytes(canonical_bytes),
        "difficulty_policy_path":policy_path,
        "difficulty_policy_sha256":_sha256_bytes(policy_bytes),
        "policy_registry_path":pins["policy_registry_path"],
        "policy_registry_sha256":pins["policy_registry_sha256"],
        "difficulty_resolver_path":pins["difficulty_resolver_path"],
        "difficulty_resolver_sha256":pins["difficulty_resolver_sha256"],
        "authoring_registry_path":pins["authoring_registry_path"],
        "authoring_registry_sha256":pins["authoring_registry_sha256"],
        "authoring_generator_path":pins["authoring_generator_path"],
        "authoring_generator_sha256":pins["authoring_generator_sha256"],
        "request_validator_path":pins["request_validator_path"],
        "request_validator_sha256":pins["request_validator_sha256"],
        "visual_drill_adapter_path":pins["visual_drill_adapter_path"],
        "visual_drill_adapter_sha256":pins["visual_drill_adapter_sha256"],
        "seed_variation_path":pins["seed_variation_path"],
        "seed_variation_sha256":pins["seed_variation_sha256"],
        "request_model_path":pins["request_model_path"],
        "request_model_sha256":pins["request_model_sha256"],
        "assembly_context_path":pins["assembly_context_path"],
        "assembly_context_sha256":pins["assembly_context_sha256"],
        "resolved_effective_parameters_sha256":_sha256(parameters),
        "materialized_difficulty_tier":int(exercise.get("difficulty_tier", -1)),
        "materialized_generator":str(exercise.get("generator", "")),
        "materialized_task_type":str(materialized_task.get("type", "")),
        "seed_motion_seed":seed,
        "canonical_duration_seconds":duration_seconds,
        "canonical_fps":fps,
        "canonical_frame_count":frame_count,
        "materialized_duration_seconds":float(payload_source.get("duration", -1.0)),
        "materialized_fps":int(payload_source.get("fps", -1)),
        "materialized_frame_count":int(payload_source.get("frame_count", -1))
    }

func _verify_source_pins() -> String:
    for path in SOURCE_PINS.keys():
        var bytes: PackedByteArray = FileAccess.get_file_as_bytes("res://" + str(path))
        if bytes.is_empty():
            return "Pinned authoring source is unavailable: %s" % str(path)
        if _sha256_bytes(bytes) != str(SOURCE_PINS[path]):
            return "Pinned authoring source SHA-256 mismatch: %s" % str(path)
    return ""

func _make_context(seed: int, family: String) -> VisualAuthoringAssemblyContext:
    return VisualAuthoringAssemblyContextScript.new(
        seed,
        "2.0",
        "C11D-DYNAMIC-VISUAL-DRILLS",
        "2.0",
        "C11-C-2.19.12",
        {"profile_id":"social_default_v1", "coordinate_space":"CANVAS_540X960"},
        {"family_id":family},
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
    if not is_finite(numeric) or numeric < float(minimum) or numeric > float(maximum):
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
    push_error("VISUAL DRILL DYNAMIC REQUEST PAYLOAD MATERIALIZATION FAIL: " + message)
    print("C11-D VISUAL DRILL DYNAMIC REQUEST PAYLOAD MATERIALIZATION FAIL | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
    quit(1)
