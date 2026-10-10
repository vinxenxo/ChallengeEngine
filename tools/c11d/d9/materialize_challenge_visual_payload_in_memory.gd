extends SceneTree

## Materializes a D-owned semantic Challenge payload from frozen C11-C runtime outputs.
## Review-only: loads SVG resources, stores frame descriptors in memory, and exits.
## It does not create scene nodes, render frames, dispatch renderer input, or write artifacts.
const RuntimeBridge = preload("res://core/execution/ChallengeRuntimeBridge.gd")
const PresentationBinder = preload("res://core/presentation/ChallengePresentationBinder.gd")
const ChallengePath := "res://challenges/CHALLENGE_004.json"
const ManifestPath := "res://release/C11C_FREEZE_PACKAGE_MANIFEST.json"
const ContractPath := "res://definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_PREVIEW_V1.json"
const FrozenManifestSha := "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
const ChallengeSha := "6a674c02c2d8831a872691954f1cc40e2492193f9b136f60656730a7be686b71"
const OutputSchema := "C11-D-D9-CHALLENGE-VISUAL-PAYLOAD-PREVIEW-V1"
const SourcePins := {
    "challenges/CHALLENGE_004.json": "6a674c02c2d8831a872691954f1cc40e2492193f9b136f60656730a7be686b71",
    "core/execution/ChallengeRuntimeBridge.gd": "c53f04df064b3697f8dd02cd779f8ef002a4e3e2d40fa0e01aa7d9b1a80a8191",
    "core/execution/ChallengeTimelineBuilder.gd": "35a47ad126a2e11577933a03b251f47732e580693e5c08e45d3b6af047c8c9af",
    "core/presentation/ChallengePresentationBinder.gd": "755ecfc9cc6e1ee51738938583217ab8a470c1a1f290bb107e91e19990d74b47",
    "core/presentation/PresentationProfile.gd": "187b1cf8ab96b9031785a0f36b0054a60383c97cb3d81906c7d9bbcd373bef24",
    "core/mechanics/parking/ParkingMechanicV2.gd": "c78dbc1adcc95ad4981f3c704c69630edc54c25473c479f10bb154efe6f105cd",
    "core/data/FrameSnapshot.gd": "61060d0937063400447cd5f2513265cb82d8e38017f5bd097c2870da03967180",
    "assets/c6/garage_background.svg": "c9d8acdae725ca7726fc8ad23a046e4aac4d9e454b45db40d2c770732b31ab1e",
    "assets/c6/car.svg": "93a6f78d9654f7917ab2287800858a937e9c68c458cc60bf417d6f2b98c1a96d",
    "assets/c6/parking_target.svg": "ec2dcafd7dfc99ff501eb2d93b93906680a30c48cf0741807cbbdd915a18cfb3"
}

func _initialize() -> void:
    call_deferred("_run")

func _run() -> void:
    var manifest_bytes: PackedByteArray = FileAccess.get_file_as_bytes(ManifestPath)
    if manifest_bytes.is_empty() or _sha256_bytes(manifest_bytes) != FrozenManifestSha:
        _fail("Frozen C11-C manifest hash mismatch.")
        return
    var source_bytes: PackedByteArray = FileAccess.get_file_as_bytes(ChallengePath)
    if source_bytes.is_empty() or _sha256_bytes(source_bytes) != ChallengeSha:
        _fail("CHALLENGE_004 source bytes/hash mismatch.")
        return
    for rel_path: String in SourcePins.keys():
        var bytes: PackedByteArray = FileAccess.get_file_as_bytes("res://" + rel_path)
        if bytes.is_empty() or _sha256_bytes(bytes) != str(SourcePins[rel_path]):
            _fail("Pinned C11-C source or physical asset hash mismatch: %s" % rel_path)
            return

    var source_value: Variant = JSON.parse_string(source_bytes.get_string_from_utf8())
    if not (source_value is Dictionary):
        _fail("Canonical Challenge source is not a JSON object.")
        return
    var source: Dictionary = source_value
    if str(source.get("challenge_id", "")) != "CHALLENGE_004" or str(source.get("mechanic", "")) != "parking_v2":
        _fail("Challenge identity changed.")
        return
    if not _contract_guard():
        _fail("Visual payload contract or governance locks changed.")
        return

    var first_result: Dictionary = RuntimeBridge.run_effective_pipeline(source)
    if not bool(first_result.get("success", false)):
        _fail("First frozen runtime invocation failed: %s" % str(first_result.get("error", "unknown")))
        return
    var second_result: Dictionary = RuntimeBridge.run_effective_pipeline(source)
    if not bool(second_result.get("success", false)):
        _fail("Repeated frozen runtime invocation failed.")
        return
    var first_context: Variant = first_result.get("context", null)
    var second_context: Variant = second_result.get("context", null)
    if first_context == null or second_context == null:
        _fail("Frozen runtime returned incomplete context.")
        return

    var first_payload_result: Dictionary = _build_payload(source, first_context)
    if not bool(first_payload_result.get("success", false)):
        _fail("First Challenge visual payload build failed: %s" % str(first_payload_result.get("error", "unknown")))
        return
    var second_payload_result: Dictionary = _build_payload(source, second_context)
    if not bool(second_payload_result.get("success", false)):
        _fail("Repeated Challenge visual payload build failed: %s" % str(second_payload_result.get("error", "unknown")))
        return

    var first_payload_hash: String = str(first_payload_result.get("payload_sha256", ""))
    var second_payload_hash: String = str(second_payload_result.get("payload_sha256", ""))
    var first_frame_hash: String = str(first_payload_result.get("frame_signature_sha256", ""))
    var second_frame_hash: String = str(second_payload_result.get("frame_signature_sha256", ""))
    var repeated_equal: bool = first_payload_hash == second_payload_hash and first_frame_hash == second_frame_hash
    if not repeated_equal:
        _fail("Repeated runtime did not produce identical visual payload/frame signatures.")
        return

    var payload: Dictionary = first_payload_result["payload"]
    var assets: Array = first_payload_result["asset_nodes"]
    var timeline: Dictionary = first_payload_result["source_timeline"]
    var frame_records_hash: String = str(first_payload_result["frame_records_sha256"])
    var model_hash: String = str(first_payload_result["render_model_sha256"])
    var inv: Dictionary = first_payload_result["simulation_invariance"]
    if not bool(inv.get("simulation_invariance", false)):
        _fail("Presentation rebind changed simulation frames or metrics.")
        return
    if not _validate_payload_in_memory(payload, assets, first_payload_hash, timeline, frame_records_hash):
        _fail("Materialized visual payload failed invariant checks.")
        return

    var source_lineage: Array[Dictionary] = []
    source_lineage.append({"path": "release/C11C_FREEZE_PACKAGE_MANIFEST.json", "sha256": FrozenManifestSha})
    for rel_path: String in SourcePins.keys():
        source_lineage.append({"path": rel_path, "sha256": str(SourcePins[rel_path])})
    source_lineage.sort_custom(func(a: Dictionary, b: Dictionary) -> bool: return str(a.get("path", "")) < str(b.get("path", "")))

    var report: Dictionary = {
        "schema": OutputSchema,
        "schema_version": "1.0",
        "status": "IN_MEMORY_REVIEW_ONLY_SOURCE_TIMEBASE_VISUAL_PAYLOAD_NOT_RENDERER_INPUT",
        "frozen_c11c_manifest_sha256": FrozenManifestSha,
        "challenge_source_sha256": ChallengeSha,
        "payload_sha256": first_payload_hash,
        "payload_identity": {
            "challenge_id": "CHALLENGE_004",
            "mechanic": "parking_v2",
            "mechanic_version": "2.0",
            "presentation_profile_id": "social_default_v1",
            "coordinate_space": "CANVAS_1080X1920",
            "materialization": "IN_MEMORY_ONLY_SOURCE_TIMEBASE"
        },
        "asset_nodes": assets,
        "source_timeline": timeline,
        "animation": {
            "frame_source": "SimulationResult.frames",
            "source_fps": 60,
            "game_frame_count": 420,
            "frame_record_count": 420,
            "frame_records_sha256": frame_records_hash,
            "snapshot_fields_included": ["position", "rotation", "scale", "opacity", "texture_index", "variant_id"],
            "simulation_telemetry_included": false,
            "winning_frame_sampling_used": false,
            "delivery_resampling": "UNRESOLVED_NOT_APPLIED"
        },
        "presentation": {
            "render_model_sha256": model_hash,
            "profile_source_canvas": {"width": 540, "height": 960},
            "profile_master_output": {"width": 1080, "height": 1920},
            "source_coordinate_space": "CANVAS_1080X1920",
            "coordinate_projection": "UNRESOLVED_NOT_APPLIED"
        },
        "determinism": {
            "runtime_repeat_equal": true,
            "payload_repeat_equal": first_payload_hash == second_payload_hash,
            "frame_signature_repeat_equal": first_frame_hash == second_frame_hash,
            "simulation_invariance": true
        },
        "execution_boundary": {
            "mode": "GODOT_HEADLESS_IN_MEMORY_REVIEW_ONLY",
            "payload_written": false,
            "media_output_created": false,
            "renderer_native_input_emitted": false,
            "renderer_dispatch_invoked": false,
            "renderer_activation": false,
            "c11c_source_mutation": false,
            "d4_8": "BLOCKED",
            "release_authority": "NONE",
            "output_artifact_path": null
        },
        "source_lineage": source_lineage
    }
    print("C11-D RENDERER CHALLENGE VISUAL PAYLOAD PREVIEW PASS | payload=1/1 | assets=3/3 | game_frames=420/420@60FPS | deterministic=2/2 | coordinate_projection=UNRESOLVED_NOT_APPLIED | delivery_resampling=UNRESOLVED_NOT_APPLIED | telemetry=NOT_BOUND | renderer_input=NOT_EMITTED | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
    print("C11-D CHALLENGE VISUAL PAYLOAD PREVIEW SUMMARY=" + JSON.stringify(report))
    quit(0)

func _build_payload(source: Dictionary, context: Variant) -> Dictionary:
    if context == null or context.simulation_result == null or context.timeline == null or context.presentation_binding == null:
        return {"success": false, "error": "Incomplete runtime context."}
    var sim: Variant = context.simulation_result
    var timeline_obj: Variant = context.timeline
    if str(sim.error_state) != "OK" or sim.frames.size() != 420 or int(timeline_obj.fps) != 60 or int(timeline_obj.total_frames) != 900:
        return {"success": false, "error": "Runtime timeline/simulation frame count mismatch."}
    var before_signature: String = _frame_signature_sha256(sim)
    if before_signature.is_empty():
        return {"success": false, "error": "Simulation frame signature is invalid."}
    var before_winning: int = int(sim.winning_frame)
    var before_score: float = float(sim.score)
    var before_distance: float = float(sim.minimum_distance)
    var before_tolerance: float = float(sim.tolerance_threshold)

    var canonical: Dictionary = context.canonical_v2.duplicate(true)
    var d_presentation: Dictionary = canonical.get("presentation", {}).duplicate(true)
    d_presentation["profile_id"] = "social_default_v1"
    canonical["presentation"] = d_presentation
    var d_binding: Variant = PresentationBinder.bind(canonical, timeline_obj, sim)
    if d_binding == null or not bool(d_binding.success) or d_binding.presentation_profile == null:
        return {"success": false, "error": "D presentation binding failed: %s" % str(d_binding.error if d_binding != null else "null binding")}
    if str(d_binding.presentation_profile.profile_id) != "social_default_v1":
        return {"success": false, "error": "D presentation profile identity mismatch."}

    var render_model: Dictionary = d_binding.presentation_render_model
    var render_model_hash: String = _sha256_text(JSON.stringify(_stable_value(render_model)))
    var source_assets: Dictionary = source.get("assets", {})
    var bound_assets: Dictionary = d_binding.physical_assets
    if bound_assets.get("background_path", "") != source_assets.get("background_path", "") or bound_assets.get("object_path", "") != source_assets.get("object_path", "") or bound_assets.get("target_path", "") != source_assets.get("target_path", ""):
        return {"success": false, "error": "D presentation binding changed canonical asset paths."}

    var visual_cfg: Dictionary = source.get("presentation", {}).get("visual", {})
    var parking_cfg: Dictionary = source.get("difficulty", {}).get("parking", {})
    var asset_nodes: Array[Dictionary] = []
    var asset_specs: Array[Dictionary] = [
        {"role": "BACKGROUND", "path": str(bound_assets.get("background_path", "")), "rel": "assets/c6/garage_background.svg", "binding_source": "CanonicalV2.assets.background_path", "transform": {"policy": "INTRINSIC_SOURCE_ASSET", "projection_applied": false}},
        {"role": "ANIMATED_OBJECT", "path": str(bound_assets.get("object_path", "")), "rel": "assets/c6/car.svg", "binding_source": "CanonicalV2.assets.object_path", "transform": {"policy": "PRESERVE_SIMULATION_FRAME_TRANSFORMS_AND_DECLARED_PRESENTATION_METADATA_SEPARATELY", "declared_scale": float(visual_cfg.get("object_scale", 0.85)), "declared_offset": visual_cfg.get("object_offset", [0.0, 0.0]), "projection_applied": false}},
        {"role": "TARGET", "path": str(bound_assets.get("target_path", "")), "rel": "assets/c6/parking_target.svg", "binding_source": "CanonicalV2.assets.target_path", "transform": {"policy": "PRESERVE_CANONICAL_STATIC_TARGET_METADATA_SEPARATELY", "position_source": "CHALLENGE_004.difficulty.parking.target_position", "declared_position": parking_cfg.get("target_position", []), "declared_scale": float(visual_cfg.get("target_scale", 0.85)), "declared_offset": visual_cfg.get("target_offset", [0.0, 0.0]), "projection_applied": false}}
    ]
    for spec: Dictionary in asset_specs:
        var path: String = str(spec.get("path", ""))
        var bytes: PackedByteArray = FileAccess.get_file_as_bytes(path)
        if path.is_empty() or bytes.is_empty():
            return {"success": false, "error": "Physical asset missing/unreadable: %s" % path}
        var loaded_resource: Resource = ResourceLoader.load(path) as Resource
        if loaded_resource == null or not (loaded_resource is Texture2D):
            return {"success": false, "error": "Physical asset did not load as Texture2D: %s" % path}
        var texture: Texture2D = loaded_resource as Texture2D
        var expected_sizes: Dictionary = {"BACKGROUND": [1080, 1920], "ANIMATED_OBJECT": [160, 320], "TARGET": [200, 400]}
        var expected_size: Array = expected_sizes.get(str(spec.get("role", "")), [])
        if expected_size.size() != 2 or int(texture.get_width()) != int(expected_size[0]) or int(texture.get_height()) != int(expected_size[1]):
            return {"success": false, "error": "Loaded asset intrinsic size changed: %s" % path}
        var asset_node: Dictionary = {
            "role": str(spec.get("role", "")),
            "resource_path": path,
            "sha256": _sha256_bytes(bytes),
            "resource_loaded_as_texture2d": true,
            "intrinsic_width": int(texture.get_width()),
            "intrinsic_height": int(texture.get_height()),
            "binding_source": str(spec.get("binding_source", "")),
            "declared_transform": spec.get("transform", {})
        }
        asset_nodes.append(asset_node)

    var game_records: Array[Dictionary] = []
    for index: int in range(sim.frames.size()):
        var frame: Variant = sim.frames[index]
        if frame == null or not frame.is_valid_snapshot():
            return {"success": false, "error": "Invalid simulation visual snapshot at GAME index %d." % index}
        game_records.append({
            "source_game_frame_index": index,
            "position": {"x": float(frame.position.x), "y": float(frame.position.y)},
            "rotation_radians": float(frame.rotation),
            "scale": {"x": float(frame.scale.x), "y": float(frame.scale.y)},
            "opacity": float(frame.opacity),
            "texture_index": int(frame.texture_index),
            "variant_id": int(frame.variant_id)
        })
    if game_records.size() != 420:
        return {"success": false, "error": "Visual frame payload did not preserve all 420 GAME snapshots."}

    var phase_segments: Array[Dictionary] = []
    var boundary: int = 0
    var phase_data: Array[Dictionary] = [
        {"phase": "HOOK", "frame_count": int(timeline_obj.hook_frames)},
        {"phase": "GAME", "frame_count": int(timeline_obj.game_frames)},
        {"phase": "REVEAL", "frame_count": int(timeline_obj.reveal_frames)},
        {"phase": "CTA", "frame_count": int(timeline_obj.cta_frames)}
    ]
    for phase: Dictionary in phase_data:
        var count: int = int(phase.get("frame_count", 0))
        phase_segments.append({"phase": str(phase.get("phase", "")), "start_frame": boundary, "end_frame": boundary + count, "frame_count": count})
        boundary += count
    if boundary != 900:
        return {"success": false, "error": "Source phase ranges do not sum to 900 frames."}

    var frames_hash: String = _sha256_text(JSON.stringify(_stable_value(game_records)))
    var payload: Dictionary = {
        "schema": OutputSchema,
        "schema_version": "1.0",
        "status": "IN_MEMORY_REVIEW_ONLY_SOURCE_TIMEBASE_VISUAL_PAYLOAD_NOT_RENDERER_INPUT",
        "identity": {"challenge_id": "CHALLENGE_004", "mechanic": "parking_v2", "mechanic_version": "2.0", "presentation_profile_id": "social_default_v1", "coordinate_space": str(source.get("presentation", {}).get("coordinate_space", "")), "materialization": "IN_MEMORY_ONLY_SOURCE_TIMEBASE"},
        "asset_nodes": asset_nodes,
        "presentation_render_model": _stable_value(render_model),
        "presentation_render_model_sha256": render_model_hash,
        "timeline": {"fps": int(timeline_obj.fps), "total_frames": int(timeline_obj.total_frames), "duration_seconds": float(timeline_obj.total_frames) / float(timeline_obj.fps), "phase_order": ["HOOK", "GAME", "REVEAL", "CTA"], "phase_segments": phase_segments},
        "animation": {"frame_source": "SimulationResult.frames", "source_fps": int(timeline_obj.fps), "game_frame_count": int(sim.frames.size()), "frame_records": game_records, "frame_records_sha256": frames_hash, "fields_included": ["position", "rotation", "scale", "opacity", "texture_index", "variant_id"], "telemetry_included": false, "winning_frame_sampling_used": false, "delivery_resampling": "UNRESOLVED_NOT_APPLIED"},
        "source_coordinate_space": str(source.get("presentation", {}).get("coordinate_space", "")),
        "profile_source_canvas": {"width": int(d_binding.presentation_profile.source_canvas_size.x), "height": int(d_binding.presentation_profile.source_canvas_size.y)},
        "profile_master_output": {"width": int(d_binding.presentation_profile.master_output_size.x), "height": int(d_binding.presentation_profile.master_output_size.y)},
        "coordinate_projection": "UNRESOLVED_NOT_APPLIED",
        "editorial_visibility": "NOT_APPLIED_BY_THIS_PAYLOAD_PREVIEW",
        "execution_boundary": {"payload_written": false, "media_output_created": false, "renderer_native_input_emitted": false, "renderer_dispatch_invoked": false, "renderer_activation": false, "c11c_source_mutation": false, "d4_8": "BLOCKED", "release_authority": "NONE", "output_artifact_path": null}
    }
    var payload_sha: String = _sha256_text(JSON.stringify(_stable_value(payload)))

    var after_signature: String = _frame_signature_sha256(sim)
    var invariance: bool = before_signature == after_signature and int(sim.winning_frame) == before_winning and is_equal_approx(float(sim.score), before_score) and is_equal_approx(float(sim.minimum_distance), before_distance) and is_equal_approx(float(sim.tolerance_threshold), before_tolerance) and sim.frames.size() == 420
    if not invariance:
        return {"success": false, "error": "Simulation invariance check failed during payload materialization."}
    return {
        "success": true,
        "payload": payload,
        "payload_sha256": payload_sha,
        "asset_nodes": asset_nodes,
        "source_timeline": {"fps": int(timeline_obj.fps), "total_frames": int(timeline_obj.total_frames), "duration_seconds": float(timeline_obj.total_frames) / float(timeline_obj.fps), "phase_order": ["HOOK", "GAME", "REVEAL", "CTA"], "phase_segments": phase_segments},
        "frame_records_sha256": frames_hash,
        "render_model_sha256": render_model_hash,
        "frame_signature_sha256": after_signature,
        "simulation_invariance": {"simulation_invariance": invariance, "winning_frame_sampling_used": false}
    }

func _validate_payload_in_memory(payload: Dictionary, assets: Array, payload_hash: String, timeline: Dictionary, frames_hash: String) -> bool:
    if str(payload.get("schema", "")) != OutputSchema or str(payload.get("status", "")) != "IN_MEMORY_REVIEW_ONLY_SOURCE_TIMEBASE_VISUAL_PAYLOAD_NOT_RENDERER_INPUT":
        return false
    if assets.size() != 3 or int(payload.get("animation", {}).get("frame_records", []).size()) != 420:
        return false
    if payload_hash.length() != 64 or frames_hash.length() != 64:
        return false
    if int(timeline.get("fps", 0)) != 60 or int(timeline.get("total_frames", 0)) != 900 or float(timeline.get("duration_seconds", 0.0)) != 15.0:
        return false
    if str(payload.get("coordinate_projection", "")) != "UNRESOLVED_NOT_APPLIED" or str(payload.get("animation", {}).get("delivery_resampling", "")) != "UNRESOLVED_NOT_APPLIED":
        return false
    if bool(payload.get("animation", {}).get("telemetry_included", true)) or bool(payload.get("animation", {}).get("winning_frame_sampling_used", true)):
        return false
    if _contains_key(payload, "winning_frame") or _contains_key(payload, "close_calls") or _contains_key(payload, "minimum_distance") or _contains_key(payload, "score") or _contains_key(payload, "custom_data"):
        return false
    var roles: Dictionary = {}
    var expected_paths: Dictionary = {"BACKGROUND": "res://assets/c6/garage_background.svg", "ANIMATED_OBJECT": "res://assets/c6/car.svg", "TARGET": "res://assets/c6/parking_target.svg"}
    for node: Dictionary in assets:
        var role: String = str(node.get("role", ""))
        if roles.has(role) or not bool(node.get("resource_loaded_as_texture2d", false)):
            return false
        if str(node.get("resource_path", "")) != str(expected_paths.get(role, "")):
            return false
        roles[role] = true
    return roles.has("BACKGROUND") and roles.has("ANIMATED_OBJECT") and roles.has("TARGET")

func _contract_guard() -> bool:
    var bytes: PackedByteArray = FileAccess.get_file_as_bytes(ContractPath)
    if bytes.is_empty(): return false
    var value: Variant = JSON.parse_string(bytes.get_string_from_utf8())
    if not (value is Dictionary): return false
    var contract: Dictionary = value
    if str(contract.get("schema", "")) != "C11-D-D9-RENDERER-CHALLENGE-VISUAL-PAYLOAD-PREVIEW-CONTRACT-V1": return false
    if str(contract.get("status", "")) != "PREPARATION_ONLY_NOT_APPROVED_NOT_FROZEN": return false
    if str(contract.get("source_authority", {}).get("frozen_manifest_sha256", "")) != FrozenManifestSha: return false
    if str(contract.get("source_authority", {}).get("challenge_source_sha256", "")) != ChallengeSha: return false
    var pins_value: Variant = contract.get("pinned_sources", [])
    if not (pins_value is Array) or pins_value.size() != SourcePins.size(): return false
    var declared_pins: Dictionary = {}
    for pin_value: Variant in pins_value:
        if not (pin_value is Dictionary): return false
        var pin: Dictionary = pin_value
        declared_pins[str(pin.get("path", ""))] = str(pin.get("sha256", ""))
    if declared_pins != SourcePins: return false
    var locks: Dictionary = contract.get("governance_locks", {})
    return str(locks.get("source_adapter_mode", "")) == "PREPARE_ONLY" and str(locks.get("d4_8", "")) == "BLOCKED" and str(locks.get("release_authority", "")) == "NONE" and locks.get("renderer_baseline_approved") == false and locks.get("renderer_baseline_frozen") == false

func _contains_key(value: Variant, forbidden: String) -> bool:
    if value is Dictionary:
        for key: Variant in value.keys():
            if str(key).to_lower() == forbidden.to_lower(): return true
            if _contains_key(value[key], forbidden): return true
    elif value is Array:
        for item: Variant in value:
            if _contains_key(item, forbidden): return true
    return false

func _frame_signature_sha256(sim: Variant) -> String:
    var parts := PackedStringArray()
    for index: int in range(sim.frames.size()):
        var frame: Variant = sim.frames[index]
        if frame == null or not frame.is_valid_snapshot(): return ""
        parts.append("%d|%.9f|%.9f|%.9f|%.9f|%.9f|%.9f|%.9f|%d|%d|%s" % [index, frame.position.x, frame.position.y, frame.rotation, frame.scale.x, frame.scale.y, frame.opacity, float(frame.texture_index), int(frame.variant_id), int(frame.custom_data.size()), JSON.stringify(_stable_value(frame.custom_data))])
    return _sha256_text("\n".join(parts))

func _stable_value(value: Variant) -> Variant:
    if value is Dictionary:
        var output: Dictionary = {}
        var keys: Array = value.keys()
        keys.sort_custom(func(a: Variant, b: Variant) -> bool: return str(a) < str(b))
        for key: Variant in keys: output[str(key)] = _stable_value(value[key])
        return output
    if value is Array:
        var output_array: Array = []
        for item: Variant in value: output_array.append(_stable_value(item))
        return output_array
    if value is Vector2: return {"$type": "Vector2", "x": value.x, "y": value.y}
    if value is Vector2i: return {"$type": "Vector2i", "x": value.x, "y": value.y}
    if value is Vector3: return {"$type": "Vector3", "x": value.x, "y": value.y, "z": value.z}
    if value is Color: return {"$type": "Color", "r": value.r, "g": value.g, "b": value.b, "a": value.a}
    if value is Rect2: return {"$type": "Rect2", "position": _stable_value(value.position), "size": _stable_value(value.size)}
    if value is String or value is StringName or value is int or value is float or value is bool or value == null: return value
    return str(value)

func _sha256_text(value: String) -> String:
    return _sha256_bytes(value.to_utf8_buffer())

func _sha256_bytes(bytes: PackedByteArray) -> String:
    if bytes.is_empty(): return "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    var context := HashingContext.new()
    context.start(HashingContext.HASH_SHA256)
    context.update(bytes)
    return context.finish().hex_encode()

func _fail(message: String) -> void:
    printerr("C11-D RENDERER CHALLENGE VISUAL PAYLOAD PREVIEW FAIL | %s" % message)
    quit(1)
