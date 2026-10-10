extends SceneTree
## D-owned proposal-only editorial field window mapping over a previously reviewed frozen Challenge timeline.
## It never derives simulation sampling, maps winning_frame, emits renderer input or writes report files.
const RuntimeBridge = preload("res://core/execution/ChallengeRuntimeBridge.gd")
const PresentationBinder = preload("res://core/presentation/ChallengePresentationBinder.gd")
const ManifestPath := "res://release/C11C_FREEZE_PACKAGE_MANIFEST.json"
const ChallengePath := "res://challenges/CHALLENGE_004.json"
const DeliveryPath := "res://profiles/delivery/c11c_video_delivery_profiles.json"
const TimebaseContractPath := "res://definitions/c11d/production/D_RENDERER_DELIVERY_TIMEBASE_PROJECTION_V1.json"
const ContractPath := "res://definitions/c11d/production/D_RENDERER_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json"
const FrozenManifestSha256 := "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
const OutputSchema := "C11-D-D9-RENDERER-EDITORIAL-FIELD-WINDOW-PROPOSAL-V1"
const EmptySha256 := "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
const ExpectedLineage := [
    {"path": "release/C11C_FREEZE_PACKAGE_MANIFEST.json", "sha256": "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"},
    {"path": "challenges/CHALLENGE_004.json", "sha256": "6a674c02c2d8831a872691954f1cc40e2492193f9b136f60656730a7be686b71"},
    {"path": "profiles/delivery/c11c_video_delivery_profiles.json", "sha256": "967831513eb225e6eafd56496ce0d0a0b0f0e158d205b5985e7bba11b0534ae3"},
    {"path": "definitions/c11d/production/D_RENDERER_PROFILE_IDENTITY_SEPARATION_V1.json", "sha256": "e217d0d94a580747e754be68aba18bcadc4cf954c09d60f97a07e2b9c35fbb77"},
    {"path": "definitions/c11d/production/D_RENDERER_DELIVERY_TIMEBASE_PROJECTION_V1.json", "sha256": "602c938cbf8378e8f71aefc6fb46d61496e78f9ab84d595f9efab982a2820a38"},
    {"path": "definitions/c11d/production/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1.json", "sha256": "660f20bf39f6c797e5b3f06615e19efe490353c35637effcacd2e7d4acc447fd"},
    {"path": "definitions/c11d/production/D_RENDERER_CHALLENGE_RUNTIME_OUTPUT_PREVIEW_V1.json", "sha256": "ed56660d77de32e288eb3f4106499e94e390785d6d6503c5c028fc3399dd20c5"},
    {"path": "definitions/c11d/production/D_RENDERER_CHALLENGE_DELIVERY_TIMELINE_REVIEW_V1.json", "sha256": "30381dba04a07d6e0ea1d82b186f46b78ab7193ecaa82efe3e484dd5bcd64e22"}
]

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
    if str(contract.get("schema", "")) != "C11-D-RENDERER-EDITORIAL-FIELD-WINDOW-PROPOSAL-CONTRACT-V1" or str(contract.get("status", "")) != "PROPOSAL_ONLY_NOT_RENDERER_INPUT":
        _fail("Editorial field-window proposal contract identity/status mismatch."); return
    var policy: Dictionary = contract.get("mapping_policy", {})
    if str(policy.get("policy_id", "")) != "C11D_SAME_NAME_EDITORIAL_FIELD_TO_PHASE_FULL_WINDOW_V1" or str(policy.get("state", "")) != "PROPOSED_NOT_APPROVED":
        _fail("Field-window policy drifted or has been silently approved."); return
    var lineage: Array = contract.get("source_lineage", [])
    if lineage != ExpectedLineage:
        _fail("Pinned source-lineage declarations drifted."); return
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

    # The field-to-phase relation is explicit in this D proposal; it is not inferred solely from phase names.
    var canonical_content: Dictionary = (ctx.canonical_v2 as Dictionary).get("content", {})
    var field_specs: Array = [
        {"field_id": "hook", "phase": "HOOK"},
        {"field_id": "reveal", "phase": "REVEAL"},
        {"field_id": "cta", "phase": "CTA"}
    ]
    var field_windows: Array = []
    for spec in field_specs:
        var field_id: String = str(spec["field_id"])
        var phase_id: String = str(spec["phase"])
        var field_text: String = str(canonical_content.get(field_id, ""))
        var phase_segment: Dictionary = _segment_for_phase(delivery_segments, phase_id)
        if phase_segment.is_empty():
            _fail("No projected phase range found for explicitly mapped field %s." % field_id); return
        var field_record: Dictionary = {
            "field_id": field_id,
            "phase": phase_id,
            "source_text": field_text,
            "source_text_sha256": _sha256_text(field_text)
        }
        if field_text.strip_edges().is_empty():
            field_record["state"] = "SUPPRESSED_EMPTY_EDITORIAL_FIELD"
            field_record["visibility_range"] = null
        else:
            field_record["state"] = "PROPOSED_VISIBLE_WINDOW"
            field_record["visibility_range"] = {
                "start_frame": int(phase_segment["start_frame"]),
                "end_frame": int(phase_segment["end_frame"]),
                "frame_count": int(phase_segment["frame_count"])
            }
        field_windows.append(field_record)
    if field_windows.size() != 3 or field_windows[0].get("visibility_range", {}) != {"start_frame": 0, "end_frame": 90, "frame_count": 90}:
        _fail("HOOK field window proposal mismatch."); return
    if field_windows[1].get("state", "") != "SUPPRESSED_EMPTY_EDITORIAL_FIELD" or field_windows[1].get("visibility_range", "not-null") != null:
        _fail("Empty REVEAL must not receive a visible window."); return
    if field_windows[2].get("visibility_range", {}) != {"start_frame": 390, "end_frame": 450, "frame_count": 60}:
        _fail("CTA field window proposal mismatch."); return
    if field_windows[0].get("source_text", "") != "¡SOLO EL 1% APARCA SIN ROZAR!" or field_windows[2].get("source_text", "") != "¿Lo has clavado?":
        _fail("Editorial source copy mismatch."); return

    var render_model_hash: String = _sha256_text(JSON.stringify(_stable_value(d_binding.presentation_render_model)))
    if render_model_hash.length() != 64:
        _fail("D presentation render-model digest invalid."); return
    var report: Dictionary = {
        "schema": OutputSchema,
        "schema_version": "1.0",
        "status": "IN_MEMORY_REVIEW_ONLY_NOT_RENDERER_INPUT",
        "frozen_c11c_manifest_sha256": FrozenManifestSha256,
        "challenge_source_sha256": _sha256_bytes(source_bytes),
        "challenge_id": "CHALLENGE_004",
        "profile_identity": {
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
        "delivery_profile": {"profile_id": "REVIEW_720", "fps": delivery_fps, "total_frames": 450, "width": int(delivery_profile.width), "height": int(delivery_profile.height)},
        "source_segments": source_segments,
        "delivery_segments": delivery_segments,
        "policy": {
            "policy_id": "C11D_SAME_NAME_EDITORIAL_FIELD_TO_PHASE_FULL_WINDOW_V1",
            "state": "PROPOSED_NOT_APPROVED",
            "interval_convention": "ZERO_BASED_HALF_OPEN_DELIVERY_FRAME_RANGE",
            "visible_window_rule": "ASSIGN_THE_FULL_DELIVERY_PHASE_RANGE_ONLY_AFTER_EXPLICIT_FIELD_TO_PHASE_MAPPING",
            "empty_value_rule": "SUPPRESS_FIELD_AND_ASSIGN_NO_WINDOW"
        },
        "fields": field_windows,
        "unresolved_content_types": {"visual_loops": "NO_EDITORIAL_FIELD_WINDOW_MAPPING_DECLARED", "visual_drills": "NO_EDITORIAL_FIELD_WINDOW_MAPPING_DECLARED"},
        "source_lineage": lineage,
        "runtime_evidence": {
            "mode": "GODOT_HEADLESS_IN_MEMORY_REVIEW_ONLY",
            "runtime_success": true,
            "repeat_deterministic": repeat_deterministic,
            "simulation_frame_signature_unchanged": frame_signature_unchanged,
            "winning_frame_unchanged": winning_unchanged,
            "metrics_unchanged": metrics_unchanged,
            "game_frame_count": int(sim.frames.size())
        },
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
    report["proposal_sha256"] = _sha256_text(JSON.stringify(_stable_value(report)))
    if not _validate_report(report):
        _fail("In-memory editorial field-window proposal failed structural/invariant validation."); return
    print("C11-D RENDERER EDITORIAL FIELD WINDOW PROPOSAL PASS | fields=3/3 | visible_windows=2/3 | hook=[0,90) | reveal=EMPTY_SUPPRESSED | cta=[390,450) | simulation_invariance=PASS | policy=PROPOSED_NOT_APPROVED | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
    print("C11-D EDITORIAL FIELD WINDOW PROPOSAL SUMMARY=" + JSON.stringify(report))
    quit(0)

func _project_boundary(source_boundary: int, source_fps: int, delivery_fps: int) -> int:
    var numerator: int = 2 * source_boundary * delivery_fps + source_fps
    var denominator: int = 2 * source_fps
    return int(numerator / denominator)

func _segment_for_phase(segments: Array, phase: String) -> Dictionary:
    for segment in segments:
        if str(segment.get("phase", "")) == phase:
            return segment
    return {}

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
    if str(report.get("frozen_c11c_manifest_sha256", "")) != FrozenManifestSha256 or str(report.get("challenge_source_sha256", "")) != "6a674c02c2d8831a872691954f1cc40e2492193f9b136f60656730a7be686b71": return false
    if str(report.get("challenge_id", "")) != "CHALLENGE_004": return false
    var identity: Dictionary = report.get("profile_identity", {})
    if identity != {"legacy_video_profile_id": "test_master_11s", "source_presentation_profile_id": "social_default_v1", "d_presentation_profile_id": "social_default_v1", "delivery_profile_id": "REVIEW_720"}: return false
    var source_timeline: Dictionary = report.get("source_timeline", {})
    if source_timeline.get("fps") != 60 or source_timeline.get("total_frames") != 900 or source_timeline.get("duration_seconds") != 15 or source_timeline.get("phase_order") != ["HOOK", "GAME", "REVEAL", "CTA"] or source_timeline.get("boundary_frames") != [0, 180, 600, 780, 900]: return false
    var delivery: Dictionary = report.get("delivery_profile", {})
    if delivery != {"profile_id": "REVIEW_720", "fps": 30, "total_frames": 450, "width": 720, "height": 1280}: return false
    var source_segments: Array = report.get("source_segments", [])
    var delivery_segments: Array = report.get("delivery_segments", [])
    if _segment_counts(source_segments) != [180, 420, 180, 120] or _segment_counts(delivery_segments) != [90, 210, 90, 60]: return false
    if _segment_boundaries(source_segments) != [0, 180, 600, 780, 900] or _segment_boundaries(delivery_segments) != [0, 90, 300, 390, 450]: return false
    var policy: Dictionary = report.get("policy", {})
    if policy.get("policy_id", "") != "C11D_SAME_NAME_EDITORIAL_FIELD_TO_PHASE_FULL_WINDOW_V1" or policy.get("state", "") != "PROPOSED_NOT_APPROVED" or policy.get("interval_convention", "") != "ZERO_BASED_HALF_OPEN_DELIVERY_FRAME_RANGE": return false
    var unresolved: Dictionary = report.get("unresolved_content_types", {})
    if unresolved != {"visual_loops": "NO_EDITORIAL_FIELD_WINDOW_MAPPING_DECLARED", "visual_drills": "NO_EDITORIAL_FIELD_WINDOW_MAPPING_DECLARED"}: return false
    var field_rows: Array = report.get("fields", [])
    if field_rows.size() != 3: return false
    if field_rows[0].get("field_id", "") != "hook" or field_rows[0].get("source_text", "") != "¡SOLO EL 1% APARCA SIN ROZAR!" or field_rows[0].get("source_text_sha256", "") != _sha256_text("¡SOLO EL 1% APARCA SIN ROZAR!") or field_rows[0].get("visibility_range", {}) != {"start_frame": 0, "end_frame": 90, "frame_count": 90}: return false
    if field_rows[1].get("field_id", "") != "reveal" or field_rows[1].get("source_text", "") != "" or field_rows[1].get("source_text_sha256", "") != _sha256_text("") or field_rows[1].get("state", "") != "SUPPRESSED_EMPTY_EDITORIAL_FIELD" or field_rows[1].get("visibility_range", "not-null") != null: return false
    if field_rows[2].get("field_id", "") != "cta" or field_rows[2].get("source_text", "") != "¿Lo has clavado?" or field_rows[2].get("source_text_sha256", "") != _sha256_text("¿Lo has clavado?") or field_rows[2].get("visibility_range", {}) != {"start_frame": 390, "end_frame": 450, "frame_count": 60}: return false
    var runtime: Dictionary = report.get("runtime_evidence", {})
    if runtime.get("mode", "") != "GODOT_HEADLESS_IN_MEMORY_REVIEW_ONLY" or runtime.get("runtime_success") != true or runtime.get("repeat_deterministic") != true or runtime.get("simulation_frame_signature_unchanged") != true or runtime.get("winning_frame_unchanged") != true or runtime.get("metrics_unchanged") != true or int(runtime.get("game_frame_count", -1)) != 420: return false
    var identity_evidence: Dictionary = report.get("identity_evidence", {})
    if identity_evidence.get("legacy_runtime_bound_presentation_profile_id", "") != "test_master_11s" or str(identity_evidence.get("d_presentation_render_model_sha256", "")).length() != 64 or identity_evidence.get("winning_frame_mapping", "") != "NOT_MAPPED_BY_POLICY": return false
    var without_digest: Dictionary = report.duplicate(true)
    var supplied_digest: String = str(without_digest.get("proposal_sha256", ""))
    without_digest.erase("proposal_sha256")
    if supplied_digest.length() != 64 or supplied_digest != _sha256_text(JSON.stringify(_stable_value(without_digest))): return false
    var boundary: Dictionary = report.get("execution_boundary", {})
    for key in ["report_file_written", "renderer_native_input_emitted", "renderer_dispatch_invoked", "renderer_activation", "media_created", "c11c_source_mutation", "video_render_ready"]:
        if boundary.get(key) != false: return false
    return boundary.get("output_artifact_path", "not-null") == null and boundary.get("d4_8", "") == "BLOCKED" and boundary.get("release_authority", "") == "NONE"

func _verify_lineage(lineage: Array) -> bool:
    if lineage.size() != 8: return false
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
    # Godot HashingContext.update() rejects an empty PackedByteArray. SHA-256(empty)
    # is a defined digest; return the standard value without invoking update().
    if bytes.is_empty():
        return EmptySha256
    var context := HashingContext.new()
    context.start(HashingContext.HASH_SHA256)
    context.update(bytes)
    return context.finish().hex_encode()

func _fail(message: String) -> void:
    printerr("C11-D RENDERER CHALLENGE DELIVERY TIMELINE REVIEW FAIL | %s" % message)
    quit(1)
