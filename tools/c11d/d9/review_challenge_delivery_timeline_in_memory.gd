extends SceneTree
## D-owned review-only join of the frozen Challenge runtime, D presentation identity and proposed delivery-timebase projection.
## It does not write files, select simulation samples, map winning_frame, or invoke a renderer.
const RuntimeBridge = preload("res://core/execution/ChallengeRuntimeBridge.gd")
const PresentationBinder = preload("res://core/presentation/ChallengePresentationBinder.gd")
const ManifestPath := "res://release/C11C_FREEZE_PACKAGE_MANIFEST.json"
const ChallengePath := "res://challenges/CHALLENGE_004.json"
const DeliveryPath := "res://profiles/delivery/c11c_video_delivery_profiles.json"
const TimebaseContractPath := "res://definitions/c11d/production/D_RENDERER_DELIVERY_TIMEBASE_PROJECTION_V1.json"
const ContractPath := "res://definitions/c11d/production/D_RENDERER_CHALLENGE_DELIVERY_TIMELINE_REVIEW_V1.json"
const FrozenManifestSha256 := "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
const OutputSchema := "C11-D-D9-RENDERER-CHALLENGE-DELIVERY-TIMELINE-REVIEW-V1"

func _initialize() -> void:
    call_deferred("_run")

func _run() -> void:
    var manifest_bytes: PackedByteArray = FileAccess.get_file_as_bytes(ManifestPath)
    if manifest_bytes.is_empty() or _sha256_bytes(manifest_bytes) != FrozenManifestSha256:
        _fail("Frozen C11-C manifest hash mismatch."); return
    var source_bytes: PackedByteArray = FileAccess.get_file_as_bytes(ChallengePath)
    if source_bytes.is_empty():
        _fail("CHALLENGE_004 source missing."); return
    var source_value: Variant = JSON.parse_string(source_bytes.get_string_from_utf8())
    if not (source_value is Dictionary):
        _fail("CHALLENGE_004 source is not a dictionary."); return
    var source: Dictionary = source_value
    if str(source.get("challenge_id", "")) != "CHALLENGE_004" or str(source.get("video_profile", "")) != "test_master_11s":
        _fail("Challenge identity/legacy alias drift."); return
    var presentation_source: Dictionary = source.get("presentation", {})
    var source_presentation_id: String = str(presentation_source.get("profile", "")).strip_edges()
    if source_presentation_id != "social_default_v1":
        _fail("Explicit source presentation identity drift."); return

    var contract_value: Variant = _read_json(ContractPath)
    if not (contract_value is Dictionary):
        _fail("Delivery timeline review contract missing/invalid."); return
    var contract: Dictionary = contract_value
    if str(contract.get("schema", "")) != OutputSchema:
        _fail("Delivery timeline review contract identity mismatch."); return
    var lineage: Array = contract.get("source_lineage", [])
    if not _verify_lineage(lineage):
        _fail("Pinned source lineage missing or has a SHA-256 mismatch."); return

    var timebase_value: Variant = _read_json(TimebaseContractPath)
    if not (timebase_value is Dictionary):
        _fail("Delivery timebase proposal missing/invalid."); return
    var timebase: Dictionary = timebase_value
    var normalization: Dictionary = timebase.get("normalization_policy", {})
    if str(normalization.get("name", "")) != "CUMULATIVE_SOURCE_BOUNDARY_NEAREST_DELIVERY_TICK" or str(normalization.get("state", "")) != "PROPOSED_NOT_APPROVED":
        _fail("Timebase policy drifted or has been silently promoted."); return

    var delivery_registry: Dictionary = _read_json(DeliveryPath)
    var delivery_profiles: Dictionary = delivery_registry.get("profiles", {})
    var delivery_profile: Dictionary = delivery_profiles.get("REVIEW_720", {})
    var delivery_fps: int = int(delivery_profile.get("fps", -1))
    if delivery_fps != 30 or int(delivery_profile.get("width", -1)) != 720 or int(delivery_profile.get("height", -1)) != 1280:
        _fail("REVIEW_720 delivery profile facts drifted."); return

    var first: Dictionary = RuntimeBridge.run_effective_pipeline(source)
    if not bool(first.get("success", false)):
        _fail("First frozen runtime call failed: %s" % str(first.get("error", "unknown"))); return
    var second: Dictionary = RuntimeBridge.run_effective_pipeline(source)
    if not bool(second.get("success", false)):
        _fail("Second frozen runtime call failed: %s" % str(second.get("error", "unknown"))); return
    var ctx = first.get("context", null)
    var ctx2 = second.get("context", null)
    if ctx == null or ctx2 == null or ctx.simulation_result == null or ctx.timeline == null or ctx.canonical_v2 == null:
        _fail("Frozen runtime context incomplete."); return
    if ctx2.simulation_result == null or ctx2.timeline == null:
        _fail("Repeated runtime context incomplete."); return
    var timeline = ctx.timeline
    var sim = ctx.simulation_result
    var sim2 = ctx2.simulation_result
    if str(sim.error_state) != "OK" or str(sim2.error_state) != "OK":
        _fail("Simulation error state is not OK."); return
    var source_fps: int = int(timeline.fps)
    var source_total_frames: int = int(timeline.total_frames)
    var counts: Array = [int(timeline.hook_frames), int(timeline.game_frames), int(timeline.reveal_frames), int(timeline.cta_frames)]
    if source_fps != 60 or source_total_frames != 900 or counts != [180, 420, 180, 120] or sim.frames.size() != 420 or sim2.frames.size() != 420:
        _fail("Runtime timeline/frame counts do not match pinned CHALLENGE_004 facts."); return

    # D rebind operates on a deep copy. The original C11-C context remains unchanged.
    var canonical_copy: Dictionary = (ctx.canonical_v2 as Dictionary).duplicate(true)
    var presentation_copy: Dictionary = canonical_copy.get("presentation", {}).duplicate(true)
    presentation_copy["profile_id"] = source_presentation_id
    canonical_copy["presentation"] = presentation_copy
    var d_binding: Variant = PresentationBinder.bind(canonical_copy, timeline, sim)
    if d_binding == null or not bool(d_binding.success) or d_binding.presentation_profile == null:
        _fail("D presentation binding failed: %s" % str(d_binding.error if d_binding != null else "no result")); return
    if str(d_binding.presentation_profile.profile_id) != source_presentation_id:
        _fail("D presentation binding selected a different profile than the explicit source."); return

    var before_hash: String = _frame_signature_sha256(sim)
    var repeat_hash: String = _frame_signature_sha256(sim2)
    var before_winning: int = int(sim.winning_frame)
    var repeat_winning: int = int(sim2.winning_frame)
    var before_score: float = float(sim.score)
    var before_distance: float = float(sim.minimum_distance)
    var before_tolerance: float = float(sim.tolerance_threshold)
    var after_hash: String = _frame_signature_sha256(ctx.simulation_result)
    var metrics_unchanged: bool = is_equal_approx(float(sim.score), before_score) and is_equal_approx(float(sim.minimum_distance), before_distance) and is_equal_approx(float(sim.tolerance_threshold), before_tolerance) and is_equal_approx(float(sim2.score), before_score) and is_equal_approx(float(sim2.minimum_distance), before_distance) and is_equal_approx(float(sim2.tolerance_threshold), before_tolerance)
    var frame_signature_unchanged: bool = not before_hash.is_empty() and before_hash == after_hash
    var repeat_deterministic: bool = not before_hash.is_empty() and before_hash == repeat_hash and before_winning == repeat_winning
    var winning_unchanged: bool = int(ctx.simulation_result.winning_frame) == before_winning
    if not repeat_deterministic or not frame_signature_unchanged or not winning_unchanged or not metrics_unchanged:
        _fail("Runtime repeat or simulation-invariance check failed."); return

    var source_segments: Array = []
    var delivery_segments: Array = []
    var phases: Array = ["HOOK", "GAME", "REVEAL", "CTA"]
    var source_cursor: int = 0
    for index in range(phases.size()):
        var source_start: int = source_cursor
        var source_end: int = source_start + int(counts[index])
        var delivery_start: int = _project_boundary(source_start, source_fps, delivery_fps)
        var delivery_end: int = _project_boundary(source_end, source_fps, delivery_fps)
        source_segments.append({"phase": phases[index], "start_frame": source_start, "end_frame": source_end, "frame_count": source_end - source_start})
        delivery_segments.append({"phase": phases[index], "start_frame": delivery_start, "end_frame": delivery_end, "frame_count": delivery_end - delivery_start})
        source_cursor = source_end
    if source_cursor != 900 or _segment_counts(delivery_segments) != [90, 210, 90, 60]:
        _fail("Projected segment boundaries/counts are invalid."); return

    var render_model_hash: String = _sha256_text(JSON.stringify(_stable_value(d_binding.presentation_render_model)))
    if render_model_hash.length() != 64:
        _fail("D presentation render-model digest invalid."); return
    var report: Dictionary = {
        "schema": OutputSchema,
        "schema_version": "1.0",
        "status": "IN_MEMORY_REVIEW_ONLY_NOT_RENDERER_INPUT",
        "frozen_c11c_manifest_sha256": FrozenManifestSha256,
        "challenge_source_sha256": _sha256_bytes(source_bytes),
        "profile_identity": {
            "challenge_id": "CHALLENGE_004",
            "legacy_video_profile_id": str(source.get("video_profile", "")),
            "source_presentation_profile_id": source_presentation_id,
            "d_presentation_profile_id": str(d_binding.presentation_profile.profile_id),
            "delivery_profile_id": "REVIEW_720"
        },
        "source_timeline": {
            "fps": source_fps,
            "total_frames": source_total_frames,
            "duration_seconds": 15,
            "phase_order": phases,
            "boundary_frames": [0, 180, 600, 780, 900]
        },
        "delivery_profile": {"profile_id": "REVIEW_720", "fps": delivery_fps, "width": int(delivery_profile.width), "height": int(delivery_profile.height)},
        "source_segments": source_segments,
        "delivery_segments": delivery_segments,
        "field_visibility": {"state": "UNRESOLVED_NO_PER_FIELD_FRAME_WINDOWS", "frame_ranges": null},
        "runtime_evidence": {
            "mode": "GODOT_HEADLESS_IN_MEMORY_REVIEW_ONLY",
            "runtime_success": true,
            "repeat_deterministic": repeat_deterministic,
            "simulation_frame_signature_unchanged": frame_signature_unchanged,
            "winning_frame_unchanged": winning_unchanged,
            "metrics_unchanged": metrics_unchanged,
            "game_frame_count": int(sim.frames.size())
        },
        "policy_state": "PROPOSED_NOT_APPROVED",
        "source_lineage": lineage,
        "identity_evidence": {
            "legacy_runtime_bound_presentation_profile_id": str(ctx.presentation_binding.presentation_profile.profile_id),
            "d_presentation_render_model_sha256": render_model_hash,
            "winning_frame_mapping": "NOT_MAPPED_BY_POLICY"
        },
        "execution_boundary": {
            "report_file_written": false,
            "renderer_native_input_emitted": false,
            "renderer_dispatch_invoked": false,
            "renderer_activation": false,
            "media_created": false,
            "c11c_source_mutation": false,
            "output_artifact_path": null,
            "d4_8": "BLOCKED",
            "release_authority": "NONE",
            "video_render_ready": false
        }
    }
    if not _validate_report(report):
        _fail("In-memory review report failed structural/invariant validation."); return
    print("C11-D RENDERER CHALLENGE DELIVERY TIMELINE REVIEW PASS | source=900@60FPS | delivery=450@30FPS | phase_counts=90>210>90>60 | simulation_invariance=PASS | field_windows=UNRESOLVED | policy=PROPOSED_NOT_APPROVED | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
    print("C11-D CHALLENGE DELIVERY TIMELINE REVIEW SUMMARY=" + JSON.stringify(report))
    quit(0)

func _project_boundary(source_boundary: int, source_fps: int, delivery_fps: int) -> int:
    var numerator: int = 2 * source_boundary * delivery_fps + source_fps
    var denominator: int = 2 * source_fps
    return int(numerator / denominator)

func _segment_counts(segments: Array) -> Array:
    var counts: Array = []
    for segment in segments:
        counts.append(int(segment.get("frame_count", -1)))
    return counts

func _segment_boundaries(segments: Array) -> Array:
    if segments.is_empty(): return []
    var boundaries: Array = [int(segments[0].get("start_frame", -1))]
    for segment in segments:
        if int(segment.get("end_frame", -2)) - int(segment.get("start_frame", -1)) != int(segment.get("frame_count", -3)): return []
        boundaries.append(int(segment.get("end_frame", -1)))
    return boundaries

func _validate_report(report: Dictionary) -> bool:
    if str(report.get("schema", "")) != OutputSchema or str(report.get("status", "")) != "IN_MEMORY_REVIEW_ONLY_NOT_RENDERER_INPUT": return false
    if str(report.get("frozen_c11c_manifest_sha256", "")) != FrozenManifestSha256: return false
    var identity: Dictionary = report.get("profile_identity", {})
    if identity.get("challenge_id", "") != "CHALLENGE_004" or identity.get("source_presentation_profile_id", "") != "social_default_v1" or identity.get("d_presentation_profile_id", "") != "social_default_v1" or identity.get("delivery_profile_id", "") != "REVIEW_720": return false
    var source_timeline: Dictionary = report.get("source_timeline", {})
    if int(source_timeline.get("fps", -1)) != 60 or int(source_timeline.get("total_frames", -1)) != 900 or source_timeline.get("boundary_frames", []) != [0, 180, 600, 780, 900]: return false
    var delivery: Dictionary = report.get("delivery_profile", {})
    if int(delivery.get("fps", -1)) != 30 or int(delivery.get("width", -1)) != 720 or int(delivery.get("height", -1)) != 1280: return false
    var source_segments: Array = report.get("source_segments", [])
    var delivery_segments: Array = report.get("delivery_segments", [])
    if _segment_counts(source_segments) != [180, 420, 180, 120] or _segment_counts(delivery_segments) != [90, 210, 90, 60]: return false
    if _segment_boundaries(source_segments) != [0, 180, 600, 780, 900] or _segment_boundaries(delivery_segments) != [0, 90, 300, 390, 450]: return false
    var fields: Dictionary = report.get("field_visibility", {})
    if fields.get("state", "") != "UNRESOLVED_NO_PER_FIELD_FRAME_WINDOWS" or fields.get("frame_ranges", "not-null") != null: return false
    var runtime: Dictionary = report.get("runtime_evidence", {})
    if runtime.get("runtime_success") != true or runtime.get("repeat_deterministic") != true or runtime.get("simulation_frame_signature_unchanged") != true or runtime.get("winning_frame_unchanged") != true or runtime.get("metrics_unchanged") != true or int(runtime.get("game_frame_count", -1)) != 420: return false
    if report.get("policy_state", "") != "PROPOSED_NOT_APPROVED": return false
    var boundary: Dictionary = report.get("execution_boundary", {})
    for key in ["report_file_written", "renderer_native_input_emitted", "renderer_dispatch_invoked", "renderer_activation", "media_created", "c11c_source_mutation"]:
        if boundary.get(key) != false: return false
    return boundary.get("output_artifact_path", "not-null") == null and boundary.get("d4_8", "") == "BLOCKED" and boundary.get("release_authority", "") == "NONE" and boundary.get("video_render_ready") == false

func _verify_lineage(lineage: Array) -> bool:
    if lineage.size() != 15: return false
    for item in lineage:
        if not (item is Dictionary): return false
        var rel: String = str(item.get("path", ""))
        var expected: String = str(item.get("sha256", ""))
        if rel.is_empty() or expected.length() != 64: return false
        var bytes: PackedByteArray = FileAccess.get_file_as_bytes("res://" + rel)
        if bytes.is_empty() or _sha256_bytes(bytes) != expected: return false
    return true

func _read_json(path: String) -> Variant:
    var bytes: PackedByteArray = FileAccess.get_file_as_bytes(path)
    if bytes.is_empty(): return null
    return JSON.parse_string(bytes.get_string_from_utf8())

func _frame_signature_sha256(sim) -> String:
    var parts := PackedStringArray()
    for index in range(sim.frames.size()):
        var frame = sim.frames[index]
        if frame == null or not frame.is_valid_snapshot(): return ""
        parts.append("%d|%.9f|%.9f|%.9f|%.9f|%.9f|%.9f|%.9f|%d|%d|%s" % [index, frame.position.x, frame.position.y, frame.rotation, frame.scale.x, frame.scale.y, frame.opacity, float(frame.texture_index), int(frame.variant_id), int(frame.custom_data.size()), JSON.stringify(_stable_value(frame.custom_data))])
    return _sha256_text("\n".join(parts))

func _stable_value(value: Variant) -> Variant:
    if value is Dictionary:
        var output: Dictionary = {}
        var keys: Array = value.keys()
        keys.sort_custom(func(a, b): return str(a) < str(b))
        for key in keys: output[str(key)] = _stable_value(value[key])
        return output
    if value is Array:
        var output_array: Array = []
        for item in value: output_array.append(_stable_value(item))
        return output_array
    if value is Vector2: return {"$type":"Vector2", "x":value.x, "y":value.y}
    if value is Vector2i: return {"$type":"Vector2i", "x":value.x, "y":value.y}
    if value is Vector3: return {"$type":"Vector3", "x":value.x, "y":value.y, "z":value.z}
    if value is Color: return {"$type":"Color", "r":value.r, "g":value.g, "b":value.b, "a":value.a}
    if value is Rect2: return {"$type":"Rect2", "position":_stable_value(value.position), "size":_stable_value(value.size)}
    if value is String or value is StringName or value is int or value is float or value is bool or value == null: return value
    return str(value)

func _sha256_text(value: String) -> String:
    return _sha256_bytes(value.to_utf8_buffer())

func _sha256_bytes(bytes: PackedByteArray) -> String:
    var context := HashingContext.new()
    context.start(HashingContext.HASH_SHA256)
    context.update(bytes)
    return context.finish().hex_encode()

func _fail(message: String) -> void:
    printerr("C11-D RENDERER CHALLENGE DELIVERY TIMELINE REVIEW FAIL | %s" % message)
    quit(1)
