extends SceneTree

## V2-C: source-frame-only receipt. One invocation per independent process.
## No payload materialization, resource loading for visuals, scene/render nodes, renderer dispatch or output-file writes.
const RuntimeBridge = preload("res://core/execution/ChallengeRuntimeBridge.gd")
const VideoProfileRegistry = preload("res://core/authoring/VideoProfileRegistry.gd")
const ContractPath := "res://definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2C_SOURCE_FRAME_RUNTIME_RECEIPT_V1.json"
const ManifestPath := "res://release/C11C_FREEZE_PACKAGE_MANIFEST.json"
const FrozenManifestSha := "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
const ReceiptSchema := "C11D-CHALLENGE-VISUAL-PAYLOAD-V2C-SOURCE-FRAME-RUNTIME-RECEIPT-V1"
const ProjectionFields := ["position.x", "position.y", "rotation", "scale.x", "scale.y", "opacity", "texture_index", "variant_id"]
const ShapeFields := ["position:Vector2", "rotation:float", "scale:Vector2", "opacity:float", "texture_index:int", "variant_id:int"]

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
    var version_info: Dictionary = Engine.get_version_info()
    var engine_version := str(version_info.get("string", ""))
    if int(version_info.get("major", -1)) != 4 or int(version_info.get("minor", -1)) != 7 or int(version_info.get("patch", -1)) != 1:
        _fail("GODOT_4_7_1_ENGINE_VERSION_REQUIRED:" + engine_version)
        return
    # The engine's display string omits the .mono suffix on this official build.
    # The parent runner has already probed the exact executable with --version;
    # preserve that verified launcher identity separately from Engine version info.
    var verified_godot_version := str(_args.get("godot-version", ""))
    if not verified_godot_version.contains("4.7.1") or not verified_godot_version.to_lower().contains("mono"):
        _fail("GODOT_4_7_1_MONO_LAUNCHER_VERSION_REQUIRED:" + verified_godot_version)
        return

    var contract_bytes := FileAccess.get_file_as_bytes(ContractPath)
    if contract_bytes.is_empty():
        _fail("V2C_CONTRACT_MISSING_OR_EMPTY")
        return
    var supplied_contract_sha := str(_args.get("contract-sha256", ""))
    if supplied_contract_sha.length() != 64 or _sha256_bytes(contract_bytes) != supplied_contract_sha:
        _fail("V2C_CONTRACT_SHA_MISMATCH")
        return
    var contract_value: Variant = JSON.parse_string(contract_bytes.get_string_from_utf8())
    if not (contract_value is Dictionary):
        _fail("V2C_CONTRACT_JSON_INVALID")
        return
    var contract: Dictionary = contract_value
    if contract.get("schema", "") != "C11D-CHALLENGE-VISUAL-PAYLOAD-V2C-SOURCE-FRAME-RUNTIME-RECEIPT-CONTRACT-V1" or int(contract.get("expected_selector_count", 0)) != 9:
        _fail("V2C_CONTRACT_IDENTITY_OR_DENOMINATOR_MISMATCH")
        return
    if int(contract.get("semantic_binding_policy", {}).get("approved_bindings", -1)) != 0 or int(contract.get("semantic_binding_policy", {}).get("approved_custom_data_bindings", -1)) != 0:
        _fail("SEMANTIC_BINDINGS_MUST_REMAIN_UNAPPROVED")
        return
    var manifest_bytes := FileAccess.get_file_as_bytes(ManifestPath)
    if manifest_bytes.is_empty() or _sha256_bytes(manifest_bytes) != FrozenManifestSha:
        _fail("FROZEN_C11C_MANIFEST_SHA_MISMATCH")
        return

    var pin_map: Dictionary = {}
    var source_pins: Variant = contract.get("source_pins", [])
    if not (source_pins is Array) or source_pins.size() != int(contract.get("source_pin_count", -1)):
        _fail("SOURCE_PIN_LIST_OR_COUNT_INVALID")
        return
    for pin_value: Variant in source_pins:
        if not (pin_value is Dictionary):
            _fail("SOURCE_PIN_ROW_INVALID")
            return
        var pin: Dictionary = pin_value
        var rel := str(pin.get("path", ""))
        var expected_sha := str(pin.get("sha256", ""))
        if rel.is_empty() or expected_sha.length() != 64 or pin_map.has(rel):
            _fail("SOURCE_PIN_PATH_OR_SHA_INVALID:" + rel)
            return
        var bytes := FileAccess.get_file_as_bytes("res://" + rel)
        if bytes.is_empty() or _sha256_bytes(bytes) != expected_sha:
            _fail("SOURCE_PIN_MISMATCH:" + rel)
            return
        pin_map[rel] = expected_sha

    var selector: Dictionary = {}
    var selectors: Variant = contract.get("selectors", [])
    if not (selectors is Array) or selectors.size() != 9:
        _fail("CONTRACT_SELECTOR_DENOMINATOR_INVALID")
        return
    for item_value: Variant in selectors:
        if item_value is Dictionary and str(item_value.get("challenge_id", "")) == _challenge_id:
            selector = item_value
            break
    if selector.is_empty():
        _fail("SELECTOR_NOT_IN_CONTRACT:" + _challenge_id)
        return
    var request_hash := str(_args.get("planner-request-hash", ""))
    var plan_hash := str(_args.get("planner-plan-hash", ""))
    if not _valid_sha(request_hash) or not _valid_sha(plan_hash):
        _fail("CANONICAL_PLANNER_HASHES_MISSING_OR_INVALID")
        return

    var challenge_path := "res://" + str(selector.get("source_path", ""))
    var challenge_bytes := FileAccess.get_file_as_bytes(challenge_path)
    if challenge_bytes.is_empty() or _sha256_bytes(challenge_bytes) != str(selector.get("source_sha256", "")):
        _fail("CHALLENGE_SOURCE_PIN_MISMATCH:" + _challenge_id)
        return
    var source_value: Variant = JSON.parse_string(challenge_bytes.get_string_from_utf8())
    if not (source_value is Dictionary):
        _fail("CHALLENGE_SOURCE_JSON_INVALID:" + _challenge_id)
        return
    var source: Dictionary = source_value
    if str(source.get("challenge_id", "")) != _challenge_id or str(source.get("mechanic", "")) != str(selector.get("mechanic", "")):
        _fail("CHALLENGE_SOURCE_IDENTITY_MISMATCH:" + _challenge_id)
        return

    # Exactly one authoritative call to the existing effective runtime path in this process.
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
    # The canonical bridge deliberately supports both native-V2 inline timing
    # dictionaries and legacy VideoProfile ID bindings. Resolve the latter with
    # the same registry as the bridge; never substitute another/default profile.
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
        var video_profile_id := str(runtime_video).strip_edges()
        if video_profile_id.is_empty():
            _fail("EFFECTIVE_RUNTIME_VIDEO_PROFILE_ID_EMPTY")
            return
        var resolved_video_profile: Dictionary = VideoProfileRegistry.get_profile(video_profile_id)
        if resolved_video_profile.is_empty():
            _fail("EFFECTIVE_RUNTIME_VIDEO_PROFILE_UNRESOLVED:" + video_profile_id)
            return
        var profile_phases: Variant = resolved_video_profile.get("phases", {})
        if not (profile_phases is Dictionary) or not profile_phases.has("game_duration") or not resolved_video_profile.has("fps"):
            _fail("EFFECTIVE_RUNTIME_VIDEO_PROFILE_TIMEBASE_INVALID:" + video_profile_id)
            return
        source_fps = int(round(float(resolved_video_profile.get("fps", 0))))
        hook_duration = float(profile_phases.get("hook_duration", 0.0))
        game_duration = float(profile_phases.get("game_duration", 0.0))
        reveal_duration = float(profile_phases.get("reveal_duration", 0.0))
        cta_duration = float(profile_phases.get("cta_duration", 0.0))
    else:
        _fail("EFFECTIVE_RUNTIME_VIDEO_BINDING_TYPE_INVALID:" + type_string(typeof(runtime_video)))
        return

    # The resolved effective timebase must agree with the challenge source pin.
    # This is source-binding integrity, not phase/timeline acceptance.
    var pinned_timebase: Dictionary = selector.get("source_timebase", {})
    var pinned_fps := int(pinned_timebase.get("fps", 0))
    var pinned_hook_duration := float(pinned_timebase.get("hook_duration_seconds", 0.0))
    var pinned_game_duration := float(pinned_timebase.get("game_duration_seconds", 0.0))
    var pinned_reveal_duration := float(pinned_timebase.get("reveal_duration_seconds", 0.0))
    var pinned_cta_duration := float(pinned_timebase.get("cta_duration_seconds", 0.0))
    if source_fps != pinned_fps or not is_equal_approx(hook_duration, pinned_hook_duration) or not is_equal_approx(game_duration, pinned_game_duration) or not is_equal_approx(reveal_duration, pinned_reveal_duration) or not is_equal_approx(cta_duration, pinned_cta_duration):
        _fail("EFFECTIVE_RUNTIME_TIMEBASE_SOURCE_PIN_MISMATCH:effective_fps=%d:pinned_fps=%d:effective_hook=%.9f:pinned_hook=%.9f:effective_game=%.9f:pinned_game=%.9f:effective_reveal=%.9f:pinned_reveal=%.9f:effective_cta=%.9f:pinned_cta=%.9f" % [source_fps, pinned_fps, hook_duration, pinned_hook_duration, game_duration, pinned_game_duration, reveal_duration, pinned_reveal_duration, cta_duration, pinned_cta_duration])
        return

    var expected_frames := int(round(game_duration * float(source_fps)))
    if source_fps < 1 or game_duration <= 0.0 or expected_frames < 1:
        _fail("EFFECTIVE_RUNTIME_FRAME_CARDINALITY_INVALID")
        return
    var sim = context.simulation_result
    if sim.frames.size() != expected_frames:
        _fail("SOURCE_FRAME_COUNT_MISMATCH:expected=%d:actual=%d" % [expected_frames, sim.frames.size()])
        return
    var projection_parts: PackedStringArray = PackedStringArray()
    var finite_frames := 0
    for index in range(sim.frames.size()):
        var frame = sim.frames[index]
        if frame == null or not frame.is_valid_snapshot():
            _fail("INVALID_FRAME_SNAPSHOT:%d" % index)
            return
        if typeof(frame.position) != TYPE_VECTOR2 or typeof(frame.rotation) != TYPE_FLOAT or typeof(frame.scale) != TYPE_VECTOR2 or typeof(frame.opacity) != TYPE_FLOAT or typeof(frame.texture_index) != TYPE_INT or typeof(frame.variant_id) != TYPE_INT:
            _fail("FRAME_SNAPSHOT_SHAPE_MISMATCH:%d" % index)
            return
        finite_frames += 1
        # Deliberately never inspect/serialize custom_data in the base projection.
        projection_parts.append("%d|%.9f|%.9f|%.9f|%.9f|%.9f|%.9f|%d|%d" % [index, frame.position.x, frame.position.y, frame.rotation, frame.scale.x, frame.scale.y, frame.opacity, frame.texture_index, frame.variant_id])
    var projection_sha := _sha256_text("\n".join(projection_parts))

    var candidate_observations: Dictionary = {}
    var candidates: Array = selector.get("custom_data_candidate_fields", [])
    for key_value: Variant in candidates:
        var key := str(key_value)
        if not ["target_x", "target_position", "active_selection", "displayed_count"].has(key):
            _fail("UNAPPROVED_CUSTOM_DATA_CANDIDATE_KEY:" + key)
            return
        var present_frames := 0
        var histogram: Dictionary = {}
        for frame_value: Variant in sim.frames:
            var frame = frame_value
            # Read only the exact allowlisted candidate key; never enumerate or serialize the map.
            if frame.custom_data.has(key):
                present_frames += 1
                var field_type := _type_label(typeof(frame.custom_data[key]))
                histogram[field_type] = int(histogram.get(field_type, 0)) + 1
        candidate_observations[key] = {"present_frames": present_frames, "type_histogram": histogram}

    var source_video: Dictionary = source.get("video", {})
    var contract_tb: Dictionary = selector.get("source_timebase", {})
    var hook_s := float(source_video.get("hook_duration", 0.0))
    var game_s := float(source_video.get("game_duration", 0.0))
    var reveal_s := float(source_video.get("reveal_duration", 0.0))
    var cta_s := float(source_video.get("cta_duration", 0.0))
    var declared_total: Variant = source_video.get("total_duration", null)
    var phase_sum := hook_s + game_s + reveal_s + cta_s
    if int(source_video.get("fps", 0)) != int(contract_tb.get("fps", -1)) or not is_equal_approx(game_s, float(contract_tb.get("game_duration_seconds", -1.0))) or not is_equal_approx(phase_sum, float(contract_tb.get("phase_duration_sum_seconds", -1.0))):
        _fail("SOURCE_TIMEBASE_RECEIPT_MISMATCH")
        return
    if declared_total != contract_tb.get("declared_total_duration_seconds", null):
        _fail("DECLARED_TOTAL_DURATION_SOURCE_MISMATCH")
        return
    var known_conflict := bool(contract_tb.get("timebase_conflict", false))
    if known_conflict and (not is_equal_approx(float(declared_total), 11.0) or not is_equal_approx(phase_sum, 12.0)):
        _fail("KNOWN_TIMEBASE_CONFLICT_CHANGED")
        return
    var phase_acceptance := "BLOCKED_TIMEBASE_CONFLICT_SOURCE_FRAME_ONLY" if known_conflict else "NOT_EVALUATED_SOURCE_FRAME_ONLY"

    var asset_pins: Dictionary = {}
    var declared_assets: Dictionary = selector.get("declared_assets", {})
    for alias_value: Variant in declared_assets.keys():
        var alias := str(alias_value)
        var full_path := str(declared_assets[alias])
        if not full_path.begins_with("res://"):
            _fail("ASSET_PATH_NOT_PROJECT_RESOURCE:" + alias)
            return
        var relative_path := full_path.substr(6)
        if not pin_map.has(relative_path):
            _fail("ASSET_SOURCE_NOT_PINNED:" + relative_path)
            return
        asset_pins[alias] = {"source_key": relative_path, "sha256": str(pin_map[relative_path])}

    var receipt := {
        "schema": ReceiptSchema,
        "schema_version": "1.0",
        "status": "SOURCE_FRAME_RECEIPT",
        "selector": {"challenge_id": _challenge_id, "mechanic": str(selector.get("mechanic", "")), "family_id": str(selector.get("family_id", ""))},
        "process": {"run_id": _run_id, "process_id": OS.get_process_id(), "exit_code": 0},
        "runtime": {"godot_version": verified_godot_version, "engine_version_info": version_info},
        "lineage": {
            "contract_sha256": supplied_contract_sha,
            "frozen_manifest_sha256": FrozenManifestSha,
            "challenge_source_sha256": str(selector.get("source_sha256", "")),
            "mechanic_source_sha256": str(pin_map.get(str(selector.get("mechanic_source", "")), "")),
            "runtime_bridge_sha256": str(pin_map.get("core/execution/ChallengeRuntimeBridge.gd", "")),
            "frame_snapshot_sha256": str(pin_map.get("core/data/FrameSnapshot.gd", "")),
            "verified_source_pin_count": pin_map.size()
        },
        "route": {
            "effective_mechanic": effective_mechanic,
            "runtime_bridge_method": "ChallengeRuntimeBridge.run_effective_pipeline",
            "planner_request_hash": request_hash,
            "planner_plan_hash": plan_hash,
            "bridge_status": "PLANNING_ONLY_NOT_RENDERABLE",
            "adapter_status": "PREPARED_NOT_DISPATCHED_RENDERER_DISABLED",
            "renderer": "OFF",
            "release_authority": "NONE"
        },
        "source_frames": {
            "count": sim.frames.size(), "expected_game_frames": expected_frames, "source_fps": source_fps,
            "game_duration_seconds": game_duration, "finite_transform_frames": finite_frames,
            "frame_shape": ShapeFields, "projection_fields": ProjectionFields, "projection_sha256": projection_sha
        },
        "source_timebase": {
            "declared_total_duration_seconds": declared_total, "hook_duration_seconds": hook_s,
            "game_duration_seconds": game_s, "reveal_duration_seconds": reveal_s, "cta_duration_seconds": cta_s,
            "phase_duration_sum_seconds": phase_sum, "known_conflict": known_conflict,
            "phase_timeline_acceptance": phase_acceptance
        },
        "source_asset_pins": asset_pins,
        "candidate_field_observations": candidate_observations,
        "semantic_binding_state": {"approved_bindings": 0, "approved_custom_data_bindings": 0, "custom_data_values_serialized": false},
        "side_effects": {
            "payload_file_written": false, "media_created": false, "renderer_native_input_emitted": false,
            "render_nodes_created": false, "rendering_server_called": false, "viewport_captured": false,
            "canonical_state_mutated": false, "production_dispatched": false
        }
    }
    print("C11D_V2C_SOURCE_FRAME_RECEIPT=" + JSON.stringify(receipt))
    quit(0)

func _fail(reason: String) -> void:
    var block := {"challenge_id": _challenge_id, "run_id": _run_id, "block_reason": reason, "renderer": "OFF", "media_created": false, "payload_materialized": false, "approved_bindings": 0}
    print("C11D_V2C_SOURCE_FRAME_BLOCKED=" + JSON.stringify(block))
    push_error("C11D V2-C BLOCKED: " + reason)
    quit(1)

func _valid_challenge_id(value: String) -> bool:
    return ["CHALLENGE_001", "CHALLENGE_002", "CHALLENGE_003", "CHALLENGE_004", "CHALLENGE_005", "CHALLENGE_006", "CHALLENGE_007", "CHALLENGE_008", "CHALLENGE_009"].has(value)

func _valid_sha(value: String) -> bool:
    if value.length() != 64:
        return false
    for character in value:
        if not "0123456789abcdef".contains(character):
            return false
    return true

func _type_label(value_type: int) -> String:
    match value_type:
        TYPE_FLOAT: return "float"
        TYPE_INT: return "int"
        TYPE_VECTOR2: return "Vector2"
        _: return "other"

func _sha256_bytes(bytes: PackedByteArray) -> String:
    var context := HashingContext.new()
    if context.start(HashingContext.HASH_SHA256) != OK:
        return ""
    context.update(bytes)
    return context.finish().hex_encode()

func _sha256_text(value: String) -> String:
    return _sha256_bytes(value.to_utf8_buffer())
