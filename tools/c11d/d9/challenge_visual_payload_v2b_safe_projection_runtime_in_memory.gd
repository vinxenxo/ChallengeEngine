extends SceneTree

## V2-B runtime measurement only. No payload/media, rendering, dispatch, or source JSON writes.
const RuntimeBridge = preload("res://core/execution/ChallengeRuntimeBridge.gd")
const VideoProfileRegistry = preload("res://core/authoring/VideoProfileRegistry.gd")
const RuntimeContractPath := "res://definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SAFE_PROJECTION_RUNTIME_CONTRACT_V1.json"
const RuntimeContractSchemaPath := "res://definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SAFE_PROJECTION_RUNTIME_CONTRACT_SCHEMA_V1.json"
const DesignContractPath := "res://definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SAFE_VISUAL_PROJECTION_DESIGN_V1.json"
const ManifestPath := "res://release/C11C_FREEZE_PACKAGE_MANIFEST.json"
const FrozenManifestSha := "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
const RuntimeContractId := "C11D-CHALLENGE-VISUAL-PAYLOAD-V2B-SAFE-PROJECTION-RUNTIME-CONTRACT-V1"
const RuntimeContractSchemaId := "C11D-CHALLENGE-VISUAL-PAYLOAD-V2B-SAFE-PROJECTION-RUNTIME-CONTRACT-SCHEMA-V1"
const DesignContractId := "C11D-CHALLENGE-VISUAL-PAYLOAD-V2B-SAFE-VISUAL-PROJECTION-DESIGN-CONTRACT-V1"
const ReceiptSchema := "C11D-CHALLENGE-VISUAL-PAYLOAD-V2B-SAFE-PROJECTION-RUNTIME-RECEIPT-V1"
const BaseProjectionFields := ["position", "rotation", "scale", "opacity", "texture_index", "variant_id"]
const ProjectionTupleFields := ["local_frame_index", "position_x", "position_y", "rotation", "scale_x", "scale_y", "opacity", "texture_index", "variant_id"]
const ShapeFields := ["position:Vector2", "rotation:float", "scale:Vector2", "opacity:float", "texture_index:int", "variant_id:int"]
const ApprovedProbeFields := ["target_x", "target_position", "active_selection", "displayed_count"]

var _args: Dictionary = {}
var _challenge_id := ""
var _run_id := ""

func _initialize() -> void:
    for token: String in OS.get_cmdline_user_args():
        var split_at := token.find("=")
        if token.begins_with("--") and split_at > 2:
            _args[token.substr(2, split_at - 2)] = token.substr(split_at + 1)
    _challenge_id = str(_args.get("challenge-id", ""))
    _run_id = str(_args.get("run-id", ""))
    call_deferred("_run")

func _run() -> void:
    if not _valid_challenge_id(_challenge_id) or _run_id.is_empty():
        _fail("INVALID_OR_MISSING_SELECTOR_ARGUMENTS")
        return
    var role := str(_args.get("variant-role", ""))
    if not ["BASELINE_R1", "BASELINE_R2", "GAMEPLAY_SEED_MUTATION", "MUSIC_SEED_MUTATION", "EDITORIAL_MUTATION"].has(role):
        _fail("UNKNOWN_VARIANT_ROLE")
        return
    var version_info: Dictionary = Engine.get_version_info()
    var engine_version := str(version_info.get("string", ""))
    if int(version_info.get("major", -1)) != 4 or int(version_info.get("minor", -1)) != 7 or int(version_info.get("patch", -1)) != 1:
        _fail("GODOT_4_7_1_ENGINE_VERSION_REQUIRED:" + engine_version)
        return
    var verified_godot_version := str(_args.get("godot-version", ""))
    if not verified_godot_version.contains("4.7.1") or not verified_godot_version.to_lower().contains("mono"):
        _fail("GODOT_4_7_1_MONO_LAUNCHER_VERSION_REQUIRED:" + verified_godot_version)
        return

    var runtime_contract_bytes := FileAccess.get_file_as_bytes(RuntimeContractPath)
    var supplied_contract_sha := str(_args.get("contract-sha256", ""))
    if runtime_contract_bytes.is_empty() or not _valid_sha(supplied_contract_sha) or _sha256_bytes(runtime_contract_bytes) != supplied_contract_sha:
        _fail("RUNTIME_CONTRACT_MISSING_OR_SHA_MISMATCH")
        return
    var runtime_value: Variant = JSON.parse_string(runtime_contract_bytes.get_string_from_utf8())
    if not (runtime_value is Dictionary):
        _fail("RUNTIME_CONTRACT_JSON_INVALID")
        return
    var runtime_contract: Dictionary = runtime_value
    var implementation_value: Variant = runtime_contract.get("implementation", {})
    if not (implementation_value is Dictionary):
        _fail("RUNTIME_CONTRACT_IMPLEMENTATION_BLOCK_INVALID")
        return
    var implementation: Dictionary = implementation_value
    var contract_schema_sha := str(implementation.get("contract_schema_sha256", ""))
    var contract_schema_bytes := FileAccess.get_file_as_bytes(RuntimeContractSchemaPath)
    if implementation.get("contract_schema_path", "") != RuntimeContractSchemaPath.substr(6) or not _valid_sha(contract_schema_sha) or contract_schema_bytes.is_empty() or _sha256_bytes(contract_schema_bytes) != contract_schema_sha:
        _fail("RUNTIME_CONTRACT_SCHEMA_SOURCE_PIN_MISMATCH")
        return
    var contract_schema_value: Variant = JSON.parse_string(contract_schema_bytes.get_string_from_utf8())
    if not (contract_schema_value is Dictionary) or contract_schema_value.get("schema", "") != RuntimeContractSchemaId or contract_schema_value.get("additionalProperties", true) != false:
        _fail("RUNTIME_CONTRACT_SCHEMA_IDENTITY_OR_STRICTNESS_INVALID")
        return
    if runtime_contract.get("schema", "") != RuntimeContractId or runtime_contract.get("schema_version", "") != "1.0" or runtime_contract.get("status", "") != "IMPLEMENTED_NOT_RUNTIME_ACCEPTED":
        _fail("RUNTIME_CONTRACT_IDENTITY_OR_STATUS_MISMATCH")
        return
    if int(runtime_contract.get("expected_selector_count", 0)) != 9 or int(runtime_contract.get("variants_per_selector", 0)) != 5 or int(runtime_contract.get("godot_processes_expected", 0)) != 45:
        _fail("RUNTIME_CONTRACT_DENOMINATOR_MISMATCH")
        return
    if int(runtime_contract.get("approved_bindings", -1)) != 0 or int(runtime_contract.get("approved_custom_data_bindings", -1)) != 0:
        _fail("SEMANTIC_BINDINGS_MUST_REMAIN_UNAPPROVED")
        return
    if runtime_contract.get("payload_materialized", true) != false or runtime_contract.get("media_created", true) != false or runtime_contract.get("renderer", "") != "OFF":
        _fail("PROHIBITED_SIDE_EFFECT_POLICY_CHANGED")
        return
    var governance_value: Variant = runtime_contract.get("governance_locks", {})
    if not (governance_value is Dictionary):
        _fail("GOVERNANCE_LOCKS_INVALID")
        return
    var governance: Dictionary = governance_value
    if governance.get("renderer") != "OFF" or governance.get("media_created") != false or governance.get("payload_materialized") != false or governance.get("candidate_input_admissible") != false or governance.get("seed_domains_complete_for_candidate_input") != false or governance.get("automatic_seed_generation") != false or governance.get("master_seed") != "NOT_ADOPTED" or governance.get("D4.8") != "BLOCKED" or governance.get("D9.10") != "PREPARE_ONLY" or governance.get("D9.14") != "BLOCKED" or governance.get("D9.16") != "BLOCKED" or governance.get("D9.17") != "BLOCKED_NO_GO" or governance.get("D10") != "BLOCKED_FOR_PROMOTION" or governance.get("baseline_approval") != "MISSING" or governance.get("freeze_eligible") != false or governance.get("release_authority") != "NONE":
        _fail("GOVERNANCE_LOCKS_CHANGED")
        return

    var harness_pin := str(implementation.get("harness_sha256", ""))
    var harness_bytes := FileAccess.get_file_as_bytes("res://tools/c11d/d9/challenge_visual_payload_v2b_safe_projection_runtime_in_memory.gd")
    if not _valid_sha(harness_pin) or harness_bytes.is_empty() or _sha256_bytes(harness_bytes) != harness_pin:
        _fail("RUNTIME_HARNESS_SOURCE_PIN_MISMATCH")
        return
    var receipt_schema_path := str(implementation.get("receipt_schema_path", ""))
    var receipt_schema_sha := str(implementation.get("receipt_schema_sha256", ""))
    var receipt_schema_bytes := FileAccess.get_file_as_bytes("res://" + receipt_schema_path)
    if receipt_schema_bytes.is_empty() or _sha256_bytes(receipt_schema_bytes) != receipt_schema_sha:
        _fail("RUNTIME_RECEIPT_SCHEMA_PIN_MISMATCH")
        return

    var design_bytes := FileAccess.get_file_as_bytes(DesignContractPath)
    var design_sha := str(runtime_contract.get("design_contract_sha256", ""))
    if design_bytes.is_empty() or not _valid_sha(design_sha) or _sha256_bytes(design_bytes) != design_sha:
        _fail("DESIGN_CONTRACT_SOURCE_PIN_MISMATCH")
        return
    var design_value: Variant = JSON.parse_string(design_bytes.get_string_from_utf8())
    if not (design_value is Dictionary):
        _fail("DESIGN_CONTRACT_JSON_INVALID")
        return
    var design: Dictionary = design_value
    if design.get("schema", "") != DesignContractId or design.get("status", "") != "DESIGN_ONLY_NOT_IMPLEMENTED":
        _fail("DESIGN_CONTRACT_IDENTITY_OR_STATUS_MISMATCH")
        return
    if int(design.get("authority", {}).get("approved_bindings", -1)) != 0 or int(design.get("authority", {}).get("approved_custom_data_bindings", -1)) != 0:
        _fail("DESIGN_AUTHORITY_BINDINGS_NOT_ZERO")
        return

    var manifest_bytes := FileAccess.get_file_as_bytes(ManifestPath)
    if manifest_bytes.is_empty() or _sha256_bytes(manifest_bytes) != FrozenManifestSha:
        _fail("FROZEN_C11C_MANIFEST_SHA_MISMATCH")
        return
    var pin_map: Dictionary = {}
    var source_pins: Variant = design.get("source_pins", [])
    if not (source_pins is Array) or source_pins.size() != int(design.get("source_pin_count", -1)) or source_pins.size() != 81:
        _fail("DESIGN_SOURCE_PIN_LIST_OR_COUNT_INVALID")
        return
    for pin_value: Variant in source_pins:
        if not (pin_value is Dictionary):
            _fail("SOURCE_PIN_ROW_INVALID")
            return
        var pin: Dictionary = pin_value
        var rel := str(pin.get("path", ""))
        var expected_sha := str(pin.get("sha256", ""))
        if rel.is_empty() or not _valid_sha(expected_sha) or pin_map.has(rel):
            _fail("SOURCE_PIN_PATH_OR_SHA_INVALID:" + rel)
            return
        var source_bytes := FileAccess.get_file_as_bytes("res://" + rel)
        if source_bytes.is_empty() or _sha256_bytes(source_bytes) != expected_sha:
            _fail("SOURCE_PIN_MISMATCH:" + rel)
            return
        pin_map[rel] = expected_sha
    var authority_pins: Variant = design.get("authority_input_pins", [])
    if not (authority_pins is Array) or authority_pins.size() != int(design.get("authority_input_pin_count", -1)) or authority_pins.size() != 9:
        _fail("AUTHORITY_INPUT_PIN_LIST_OR_COUNT_INVALID")
        return
    for pin_value: Variant in authority_pins:
        if not (pin_value is Dictionary):
            _fail("AUTHORITY_INPUT_PIN_ROW_INVALID")
            return
        var authority_pin: Dictionary = pin_value
        var authority_path := str(authority_pin.get("path", ""))
        var authority_sha := str(authority_pin.get("sha256", ""))
        if authority_path.is_empty() or not _valid_sha(authority_sha):
            _fail("AUTHORITY_INPUT_PIN_INVALID:" + authority_path)
            return
        var authority_bytes := FileAccess.get_file_as_bytes("res://" + authority_path)
        if authority_bytes.is_empty() or _sha256_bytes(authority_bytes) != authority_sha:
            _fail("AUTHORITY_INPUT_PIN_MISMATCH:" + authority_path)
            return

    var selector: Dictionary = {}
    var selectors: Variant = design.get("selectors", [])
    if not (selectors is Array) or selectors.size() != 9:
        _fail("DESIGN_SELECTOR_DENOMINATOR_INVALID")
        return
    for item_value: Variant in selectors:
        if item_value is Dictionary and str(item_value.get("challenge_id", "")) == _challenge_id:
            selector = item_value
            break
    if selector.is_empty():
        _fail("SELECTOR_NOT_IN_DESIGN_CONTRACT:" + _challenge_id)
        return
    var request_hash := str(_args.get("planner-request-hash", ""))
    var plan_hash := str(_args.get("planner-plan-hash", ""))
    var editorial_hash := str(_args.get("editorial-hash", ""))
    if not _valid_sha(request_hash) or not _valid_sha(plan_hash) or not _valid_sha(editorial_hash):
        _fail("CANONICAL_PLANNER_OR_EDITORIAL_HASH_MISSING_OR_INVALID")
        return
    var gameplay_seed := int(str(_args.get("gameplay-seed", "0")))
    var music_seed := int(str(_args.get("music-seed", "0")))
    if gameplay_seed < 1 or gameplay_seed > 2147483646 or music_seed < 1 or music_seed > 2147483646 or gameplay_seed == music_seed:
        _fail("SEED_DOMAIN_VALUE_INVALID_OR_COLLIDING")
        return

    var challenge_path := "res://" + str(selector.get("challenge_source_path", ""))
    var challenge_bytes := FileAccess.get_file_as_bytes(challenge_path)
    if challenge_bytes.is_empty() or _sha256_bytes(challenge_bytes) != str(selector.get("challenge_source_sha256", "")):
        _fail("CHALLENGE_SOURCE_PIN_MISMATCH:" + _challenge_id)
        return
    var source_value: Variant = JSON.parse_string(challenge_bytes.get_string_from_utf8())
    if not (source_value is Dictionary):
        _fail("CHALLENGE_SOURCE_JSON_INVALID:" + _challenge_id)
        return
    var pinned_source: Dictionary = source_value
    if str(pinned_source.get("challenge_id", "")) != _challenge_id or str(pinned_source.get("mechanic", "")) != str(selector.get("mechanic", "")):
        _fail("CHALLENGE_SOURCE_IDENTITY_MISMATCH:" + _challenge_id)
        return
    var source: Dictionary = pinned_source.duplicate(true)
    var generation_value: Variant = source.get("generation", {})
    if not (generation_value is Dictionary) or not generation_value.has("seed"):
        _fail("EXPLICIT_SOURCE_GAMEPLAY_SEED_MISSING")
        return
    var source_seed := int(generation_value.get("seed", 0))
    var requested_source_seed := int(str(_args.get("source-gameplay-seed", "0")))
    if source_seed < 1 or source_seed > 2147483646 or source_seed != requested_source_seed:
        _fail("SOURCE_GAMEPLAY_SEED_DOES_NOT_MATCH_PINNED_SOURCE")
        return
    generation_value = generation_value.duplicate(true)
    generation_value["seed"] = gameplay_seed
    source["generation"] = generation_value
    if int(source.get("generation", {}).get("seed", -1)) != gameplay_seed:
        _fail("IN_MEMORY_GAMEPLAY_SEED_INJECTION_FAILED")
        return

    var sim_input: Dictionary = source.duplicate(true)
    var sim_content_value: Variant = sim_input.get("content", {})
    if sim_content_value is Dictionary:
        var sim_content: Dictionary = sim_content_value.duplicate(true)
        for editorial_key in ["title", "subtitle", "hook", "cta", "call_to_action"]:
            sim_content.erase(editorial_key)
        sim_input["content"] = sim_content
    var simulation_input_sha := _sha256_bytes(JSON.stringify(sim_input, "", true, true).to_utf8_buffer())

    # This is the one canonical production bridge entry in this independent process.
    var runtime_result: Dictionary = RuntimeBridge.run_effective_pipeline(source)
    if not bool(runtime_result.get("success", false)):
        _fail("CHALLENGE_RUNTIME_BRIDGE_FAILED:" + str(runtime_result.get("error", runtime_result.get("error_code", "unknown"))))
        return
    var context: Variant = runtime_result.get("context", null)
    var runtime_input: Variant = runtime_result.get("runtime_input", null)
    if context == null or context.simulation_result == null or context.timeline == null or context.presentation_binding == null or not (runtime_input is Dictionary):
        _fail("EFFECTIVE_RUNTIME_CONTEXT_INCOMPLETE")
        return
    var effective_mechanic := str(context.canonical_v2.get("mechanic", source.get("mechanic", "")))
    if effective_mechanic != str(selector.get("mechanic", "")):
        _fail("EFFECTIVE_MECHANIC_ROUTE_MISMATCH:" + effective_mechanic)
        return
    var sim = context.simulation_result
    var effective_metadata: Dictionary = sim.metadata if sim.metadata is Dictionary else {}
    var initial_seed := int(effective_metadata.get("initial_seed", -1))
    var effective_seed_used := int(effective_metadata.get("seed_used", effective_metadata.get("final_seed", -1)))
    var seed_attempts := int(effective_metadata.get("attempts", 0))
    if initial_seed != gameplay_seed or effective_seed_used < 1 or effective_seed_used > 2147483646 or seed_attempts < 1:
        _fail("EFFECTIVE_GAMEPLAY_SEED_PRECEDENCE_UNRESOLVED:requested=%d:initial=%d:used=%d:attempts=%d" % [gameplay_seed, initial_seed, effective_seed_used, seed_attempts])
        return

    var runtime_video: Variant = runtime_input.get("video", {})
    var source_fps := 0
    var hook_duration := 0.0
    var game_duration := 0.0
    var reveal_duration := 0.0
    var cta_duration := 0.0
    if runtime_video is Dictionary:
        if not runtime_video.has("fps") or not runtime_video.has("game_duration"):
            _fail("EFFECTIVE_RUNTIME_VIDEO_TIMEBASE_INVALID:INLINE_FIELDS_MISSING")
            return
        source_fps = int(round(float(runtime_video.get("fps", 0))))
        hook_duration = float(runtime_video.get("hook_duration", 0.0))
        game_duration = float(runtime_video.get("game_duration", 0.0))
        reveal_duration = float(runtime_video.get("reveal_duration", 0.0))
        cta_duration = float(runtime_video.get("cta_duration", 0.0))
    elif runtime_video is String:
        var profile_id := str(runtime_video).strip_edges()
        if profile_id.is_empty():
            _fail("EFFECTIVE_RUNTIME_VIDEO_PROFILE_ID_EMPTY")
            return
        var profile: Dictionary = VideoProfileRegistry.get_profile(profile_id)
        if profile.is_empty():
            _fail("EFFECTIVE_RUNTIME_VIDEO_PROFILE_UNRESOLVED:" + profile_id)
            return
        var phases: Variant = profile.get("phases", {})
        if not (phases is Dictionary) or not phases.has("game_duration") or not profile.has("fps"):
            _fail("EFFECTIVE_RUNTIME_VIDEO_PROFILE_TIMEBASE_INVALID:" + profile_id)
            return
        source_fps = int(round(float(profile.get("fps", 0))))
        hook_duration = float(phases.get("hook_duration", 0.0))
        game_duration = float(phases.get("game_duration", 0.0))
        reveal_duration = float(phases.get("reveal_duration", 0.0))
        cta_duration = float(phases.get("cta_duration", 0.0))
    else:
        _fail("EFFECTIVE_RUNTIME_VIDEO_BINDING_TYPE_INVALID:" + type_string(typeof(runtime_video)))
        return

    var source_video: Dictionary = source.get("video", {})
    var declared_total: Variant = source_video.get("total_duration", null)
    var phase_sum := float(source_video.get("hook_duration", 0.0)) + float(source_video.get("game_duration", 0.0)) + float(source_video.get("reveal_duration", 0.0)) + float(source_video.get("cta_duration", 0.0))
    if source_fps < 1 or game_duration <= 0.0 or source_fps != int(source_video.get("fps", 0)) or not _approx(game_duration, float(source_video.get("game_duration", -1.0))):
        _fail("SOURCE_TIMEBASE_BINDING_MISMATCH")
        return
    var expected_frames := int(round(game_duration * float(source_fps)))
    if expected_frames < 1 or sim.frames.size() != expected_frames:
        _fail("SOURCE_FRAME_CARDINALITY_MISMATCH:expected=%d:actual=%d" % [expected_frames, sim.frames.size()])
        return
    var conflict := _challenge_id in ["CHALLENGE_008", "CHALLENGE_009"]
    if conflict and (declared_total == null or not _approx(float(declared_total), 11.0) or not _approx(phase_sum, 12.0)):
        _fail("KNOWN_TIMEBASE_CONFLICT_CHANGED")
        return
    if not conflict and declared_total != null and not _finite(float(declared_total)):
        _fail("DECLARED_TOTAL_DURATION_INVALID")
        return

    var projection_rows: Array = []
    for index in range(sim.frames.size()):
        var frame = sim.frames[index]
        if frame == null or not frame.is_valid_snapshot():
            _fail("INVALID_FRAME_SNAPSHOT:%d" % index)
            return
        if typeof(frame.position) != TYPE_VECTOR2 or typeof(frame.rotation) != TYPE_FLOAT or typeof(frame.scale) != TYPE_VECTOR2 or typeof(frame.opacity) != TYPE_FLOAT or typeof(frame.texture_index) != TYPE_INT or typeof(frame.variant_id) != TYPE_INT:
            _fail("FRAME_SNAPSHOT_SHAPE_MISMATCH:%d" % index)
            return
        if not _finite(frame.position.x) or not _finite(frame.position.y) or not _finite(frame.rotation) or not _finite(frame.scale.x) or not _finite(frame.scale.y) or not _finite(frame.opacity):
            _fail("NONFINITE_FRAME_PROJECTION_VALUE:%d" % index)
            return
        projection_rows.append([index, frame.position.x, frame.position.y, frame.rotation, frame.scale.x, frame.scale.y, frame.opacity, frame.texture_index, frame.variant_id])
    var state_serialization := JSON.stringify(projection_rows, "", true, true)
    var safe_state_sha := _sha256_bytes(state_serialization.to_utf8_buffer())

    var candidate_field: Variant = selector.get("custom_data_candidate_field", null)
    var candidate_observations: Array = []
    var candidate_hash_pairs: Array = []
    if candidate_field is String and not candidate_field.is_empty():
        if not ApprovedProbeFields.has(candidate_field):
            _fail("UNAPPROVED_CUSTOM_DATA_CANDIDATE_FIELD:" + str(candidate_field))
            return
        var probe_result := _probe_candidate(str(candidate_field), sim, source, _challenge_id)
        if not bool(probe_result.get("success", false)):
            _fail(str(probe_result.get("error", "CANDIDATE_PROBE_FAILED")))
            return
        var observation: Dictionary = probe_result["observation"]
        candidate_observations.append(observation)
        candidate_hash_pairs.append([str(observation["field"]), str(observation["value_stream_sha256"])])
    elif candidate_field != null:
        _fail("CANDIDATE_FIELD_SHAPE_INVALID")
        return
    var candidate_probe_sha: Variant = null
    if not candidate_hash_pairs.is_empty():
        candidate_probe_sha = _sha256_bytes(JSON.stringify(candidate_hash_pairs, "", true, true).to_utf8_buffer())

    var instance_inputs := [
        _challenge_id,
        str(selector.get("mechanic", "")),
        str(selector.get("challenge_source_sha256", "")),
        str(selector.get("mechanic_source_sha256", "")),
        "V2B_SAFE_SOURCE_STATE_PROJECTION_V1",
        str(gameplay_seed),
        str(music_seed),
        editorial_hash
    ]
    var instance_sha := _sha256_bytes(JSON.stringify(instance_inputs, "", true, true).to_utf8_buffer())
    var assets: Dictionary = {}
    var source_assets: Variant = source.get("assets", {})
    if source_assets is Dictionary:
        for alias_value in source_assets.keys():
            var alias := str(alias_value)
            var resource_path := str(source_assets[alias])
            if not resource_path.begins_with("res://"):
                _fail("ASSET_PATH_NOT_PROJECT_RESOURCE:" + alias)
                return
            var relative_path := resource_path.substr(6)
            if not pin_map.has(relative_path) or pin_map[relative_path] != _hash_resource(relative_path):
                _fail("ASSET_SOURCE_NOT_PINNED_OR_CHANGED:" + relative_path)
                return
            assets[alias] = {"source_path": relative_path, "sha256": str(pin_map[relative_path])}

    var phase_acceptance := "BLOCKED_TIMEBASE_CONFLICT_SOURCE_FRAME_ONLY" if conflict else "NOT_EVALUATED_SOURCE_FRAME_ONLY"
    var receipt := {
        "schema": ReceiptSchema,
        "schema_version": "1.0",
        "status": "SAFE_PROJECTION_RECEIPT",
        "selector": {"challenge_id": _challenge_id, "mechanic": str(selector.get("mechanic", ""))},
        "process": {"run_id": _run_id, "process_id": OS.get_process_id(), "variant_role": role, "exit_code": 0},
        "runtime": {"godot_version": verified_godot_version, "engine_version_info": version_info},
        "lineage": {
            "runtime_contract_sha256": supplied_contract_sha,
            "design_contract_sha256": design_sha,
            "frozen_manifest_sha256": FrozenManifestSha,
            "challenge_source_sha256": str(selector.get("challenge_source_sha256", "")),
            "mechanic_source_sha256": str(selector.get("mechanic_source_sha256", "")),
            "runtime_bridge_sha256": str(pin_map.get("core/execution/ChallengeRuntimeBridge.gd", "")),
            "frame_snapshot_sha256": str(pin_map.get("core/data/FrameSnapshot.gd", "")),
            "verified_source_pin_count": pin_map.size(),
            "verified_authority_input_pin_count": authority_pins.size()
        },
        "identity": {
            "canonical_request_hash": request_hash,
            "canonical_plan_hash": plan_hash,
            "editorial_hash": editorial_hash,
            "projection_instance_identity_sha256": instance_sha,
            "safe_projection_state_sha256": safe_state_sha,
            "candidate_field_probe_sha256": candidate_probe_sha,
            "payload_identity": "NOT_CREATED"
        },
        "seeds": {
            "source_gameplay_seed": source_seed,
            "requested_gameplay_seed": gameplay_seed,
            "initial_seed": initial_seed,
            "effective_seed_used": effective_seed_used,
            "seed_attempts": seed_attempts,
            "music_seed_request_domain": music_seed,
            "music_seed_copied_into_simulation": false
        },
        "simulation_input_sha256": simulation_input_sha,
        "source_frames": {
            "count": sim.frames.size(),
            "expected_game_frames": expected_frames,
            "source_fps": source_fps,
            "game_duration_seconds": game_duration,
            "projection_fields": ProjectionTupleFields,
            "frame_shape": ShapeFields,
            "coordinate_transform": "NONE",
            "resampling": "PROHIBITED",
            "projection_sha256": safe_state_sha
        },
        "source_timebase": {
            "declared_total_duration_seconds": declared_total,
            "hook_duration_seconds": float(source_video.get("hook_duration", 0.0)),
            "game_duration_seconds": float(source_video.get("game_duration", 0.0)),
            "reveal_duration_seconds": float(source_video.get("reveal_duration", 0.0)),
            "cta_duration_seconds": float(source_video.get("cta_duration", 0.0)),
            "phase_duration_sum_seconds": phase_sum,
            "known_conflict": conflict,
            "phase_timeline_acceptance": phase_acceptance
        },
        "source_asset_pins": assets,
        "candidate_field_observations": candidate_observations,
        "authority": {"approved_bindings": 0, "approved_custom_data_bindings": 0, "renderer": "OFF", "payload_materialized": false, "media_created": false, "release_authority": "NONE"}
    }
    print("C11D_V2B_SAFE_PROJECTION_RECEIPT=" + JSON.stringify(receipt, "", true, true))
    quit(0)

func _probe_candidate(field_name: String, sim, source: Dictionary, challenge_id: String) -> Dictionary:
    var expected_type := TYPE_NIL
    var type_name := ""
    match field_name:
        "target_x":
            expected_type = TYPE_FLOAT
            type_name = "float"
        "target_position":
            expected_type = TYPE_VECTOR2
            type_name = "Vector2"
        "active_selection", "displayed_count":
            expected_type = TYPE_INT
            type_name = "int"
        _:
            return {"success": false, "error": "UNKNOWN_CANDIDATE_FIELD:" + field_name}
    var stream: Array = []
    var histogram: Dictionary = {}
    var first_vector: Vector2 = Vector2.ZERO
    var have_first_vector := false
    var difficulty: Dictionary = source.get("difficulty", {})
    var choose_params: Dictionary = difficulty.get("choose", {}) if difficulty.get("choose", {}) is Dictionary else {}
    var count_params: Dictionary = difficulty.get("count", {}) if difficulty.get("count", {}) is Dictionary else {}
    var option_positions: Variant = choose_params.get("positions", [])
    var options_count := int(choose_params.get("options_count", option_positions.size() if option_positions is Array else 0))
    var min_value := int(count_params.get("min_value", 3))
    var max_value := int(count_params.get("max_value", 10))
    var start_arr: Variant = count_params.get("start_pos", [180.0, 850.0])
    if not (start_arr is Array) or start_arr.size() < 2:
        return {"success": false, "error": "COUNT_START_POSITION_INVALID"}
    var start_x := float(start_arr[0])
    var start_y := float(start_arr[1])
    var step_x := float(count_params.get("step_x", 100.0))
    if field_name == "active_selection" and (not (option_positions is Array) or options_count < 2 or option_positions.size() != options_count):
        return {"success": false, "error": "CHOOSE_OPTION_POSITION_METADATA_INVALID"}
    if field_name == "displayed_count" and (min_value >= max_value or not _finite(step_x)):
        return {"success": false, "error": "COUNT_RANGE_OR_STEP_INVALID"}

    for index in range(sim.frames.size()):
        var frame = sim.frames[index]
        # Deliberately access exactly one allowlisted key; never enumerate custom_data.
        if not frame.custom_data.has(field_name):
            return {"success": false, "error": "CANDIDATE_FIELD_MISSING:%s:%d" % [field_name, index]}
        var value: Variant = frame.custom_data[field_name]
        if typeof(value) != expected_type:
            return {"success": false, "error": "CANDIDATE_FIELD_WRONG_TYPE:%s:%d:expected=%s:actual=%s" % [field_name, index, type_name, type_string(typeof(value))]}
        if not histogram.has(type_name):
            histogram[type_name] = 0
        histogram[type_name] = int(histogram[type_name]) + 1
        if field_name == "target_x":
            if not _finite(float(value)):
                return {"success": false, "error": "PILOT_TARGET_X_NONFINITE:%d" % index}
            stream.append([index, float(value)])
        elif field_name == "target_position":
            var target: Vector2 = value
            if not _finite(target.x) or not _finite(target.y):
                return {"success": false, "error": "TARGET_POSITION_NONFINITE:%d" % index}
            if challenge_id == "CHALLENGE_005":
                if not have_first_vector:
                    first_vector = target
                    have_first_vector = true
                elif target != first_vector:
                    return {"success": false, "error": "HIT_TARGET_POSITION_NOT_RUN_CONSTANT:%d" % index}
            stream.append([index, target.x, target.y])
        elif field_name == "active_selection":
            var selected := int(value)
            if selected < 0 or selected >= options_count:
                return {"success": false, "error": "ACTIVE_SELECTION_OUT_OF_RANGE:%d:%d" % [index, selected]}
            var selected_position: Variant = option_positions[selected]
            if not (selected_position is Array) or selected_position.size() < 2:
                return {"success": false, "error": "CHOOSE_SELECTED_POSITION_INVALID:%d" % index}
            if not _approx(frame.position.x, float(selected_position[0])) or not _approx(frame.position.y, float(selected_position[1])):
                return {"success": false, "error": "CHOOSE_POSITION_INDEX_INCONSISTENT:%d" % index}
            stream.append([index, selected])
        elif field_name == "displayed_count":
            var displayed := int(value)
            if displayed < min_value or displayed > max_value:
                return {"success": false, "error": "DISPLAYED_COUNT_OUT_OF_RANGE:%d:%d" % [index, displayed]}
            var expected_x := start_x + (float(displayed - min_value) * step_x)
            if not _approx(frame.position.x, expected_x) or not _approx(frame.position.y, start_y):
                return {"success": false, "error": "DISPLAYED_COUNT_POSITION_ENCODING_MISMATCH:%d" % index}
            stream.append([index, displayed])

    var stream_sha := _sha256_bytes(JSON.stringify(stream, "", true, true).to_utf8_buffer())
    var observation := {
        "field": field_name,
        "semantic_type": type_name,
        "present_frames": sim.frames.size(),
        "type_histogram": histogram,
        "value_stream_sha256": stream_sha,
        "raw_values_emitted": false,
        "renderer_binding_approved": false
    }
    return {"success": true, "observation": observation}

func _hash_resource(relative_path: String) -> String:
    var bytes := FileAccess.get_file_as_bytes("res://" + relative_path)
    return _sha256_bytes(bytes) if not bytes.is_empty() else ""

func _fail(reason: String) -> void:
    push_error("C11D_V2B_RUNTIME_ERROR=" + reason)
    quit(2)

func _valid_challenge_id(value: String) -> bool:
    return value in ["CHALLENGE_001", "CHALLENGE_002", "CHALLENGE_003", "CHALLENGE_004", "CHALLENGE_005", "CHALLENGE_006", "CHALLENGE_007", "CHALLENGE_008", "CHALLENGE_009"]

func _valid_sha(value: String) -> bool:
    if value.length() != 64:
        return false
    for ch in value:
        if not ((ch >= "0" and ch <= "9") or (ch >= "a" and ch <= "f")):
            return false
    return true

func _finite(value: float) -> bool:
    return not is_nan(value) and not is_inf(value)

func _approx(a: float, b: float) -> bool:
    return abs(a - b) <= 0.000001

func _sha256_bytes(value: PackedByteArray) -> String:
    var ctx := HashingContext.new()
    var err := ctx.start(HashingContext.HASH_SHA256)
    if err != OK:
        return ""
    ctx.update(value)
    return ctx.finish().hex_encode()
