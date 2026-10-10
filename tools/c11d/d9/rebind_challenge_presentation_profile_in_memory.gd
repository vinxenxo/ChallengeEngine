extends SceneTree
## D-owned read-only identity split preview. Uses C11-C runtime and presentation binder without mutation or rendering.
const RuntimeBridge = preload("res://core/execution/ChallengeRuntimeBridge.gd")
const PresentationBinder = preload("res://core/presentation/ChallengePresentationBinder.gd")
const ChallengePath := "res://challenges/CHALLENGE_004.json"
const ManifestPath := "res://release/C11C_FREEZE_PACKAGE_MANIFEST.json"
const LegacyProfilePath := "res://profiles/video/test_master_11s.json"
const MatchingTimelineProfilePath := "res://profiles/video/parking_v2_social_15s.json"
const DeliveryPath := "res://profiles/delivery/c11c_video_delivery_profiles.json"
const FrozenManifestSha := "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
const OutputSchema := "C11-D-D9-RENDERER-PROFILE-IDENTITY-SEPARATION-V1"

func _initialize() -> void:
    call_deferred("_run")

func _run() -> void:
    var manifest_bytes := FileAccess.get_file_as_bytes(ManifestPath)
    if manifest_bytes.is_empty() or _sha256_bytes(manifest_bytes) != FrozenManifestSha:
        _fail("Frozen C11-C manifest hash mismatch."); return
    var source_bytes := FileAccess.get_file_as_bytes(ChallengePath)
    if source_bytes.is_empty(): _fail("Challenge source missing."); return
    var source: Variant = JSON.parse_string(source_bytes.get_string_from_utf8())
    if not (source is Dictionary): _fail("Challenge source is not a dictionary."); return
    var legacy_profile: Dictionary = _read_json(LegacyProfilePath)
    var matching_profile: Dictionary = _read_json(MatchingTimelineProfilePath)
    var delivery_registry: Dictionary = _read_json(DeliveryPath)
    if str(source.get("challenge_id", "")) != "CHALLENGE_004": _fail("Wrong challenge source."); return
    if str(source.get("video_profile", "")) != "test_master_11s": _fail("Legacy profile alias drift."); return
    var requested_presentation_profile := str(source.get("presentation", {}).get("profile", "")).strip_edges()
    if requested_presentation_profile != "social_default_v1": _fail("Explicit source presentation profile drift."); return
    if not _validate_static_profile_facts(source, legacy_profile, matching_profile, delivery_registry): _fail("Profile/timeline facts drifted."); return

    var first := RuntimeBridge.run_effective_pipeline(source)
    if not bool(first.get("success", false)): _fail("Frozen runtime failed: %s" % str(first.get("error", "unknown"))); return
    var second := RuntimeBridge.run_effective_pipeline(source)
    if not bool(second.get("success", false)): _fail("Repeated frozen runtime failed."); return
    var ctx = first.get("context", null)
    var ctx2 = second.get("context", null)
    if ctx == null or ctx2 == null or ctx.simulation_result == null or ctx.timeline == null or ctx.presentation_binding == null: _fail("Incomplete runtime context."); return
    if ctx.simulation_result.error_state != "OK" or ctx2.simulation_result.error_state != "OK": _fail("Simulation error state."); return
    var source_canonical: Dictionary = ctx.canonical_v2
    var canonical2: Dictionary = ctx2.canonical_v2
    var legacy_binding_profile := str(ctx.presentation_binding.presentation_profile.profile_id)
    if legacy_binding_profile != "test_master_11s": _fail("Legacy binding behavior changed; review contract."); return
    var timeline = ctx.timeline
    if int(timeline.fps) != 60 or int(timeline.total_frames) != 900 or int(timeline.game_frames) != 420: _fail("Runtime inline timeline does not match source contract."); return
    var before_hash := _frame_signature_sha256(ctx.simulation_result)
    var repeated_hash := _frame_signature_sha256(ctx2.simulation_result)
    var before_winning := int(ctx.simulation_result.winning_frame)
    var before_score := float(ctx.simulation_result.score)
    var before_min_dist := float(ctx.simulation_result.minimum_distance)
    var before_tolerance := float(ctx.simulation_result.tolerance_threshold)
    if before_hash.is_empty() or before_hash != repeated_hash: _fail("Simulation frame signature is not deterministic."); return

    # Crucially, modify a deep copy of canonical V2; never mutate the original runtime context.
    var d_canonical: Dictionary = source_canonical.duplicate(true)
    var presentation: Dictionary = d_canonical.get("presentation", {}).duplicate(true)
    presentation["profile_id"] = requested_presentation_profile
    d_canonical["presentation"] = presentation
    var d_binding = PresentationBinder.bind(d_canonical, ctx.timeline, ctx.simulation_result)
    if not d_binding.success or d_binding.presentation_profile == null: _fail("D presentation rebind failed: %s" % str(d_binding.error)); return
    if str(d_binding.presentation_profile.profile_id) != requested_presentation_profile: _fail("D presentation binding resolved to wrong profile."); return
    if str(ctx.presentation_binding.presentation_profile.profile_id) != legacy_binding_profile: _fail("Original runtime binding object changed."); return
    var after_hash := _frame_signature_sha256(ctx.simulation_result)
    var winning_unchanged := int(ctx.simulation_result.winning_frame) == before_winning
    var metrics_unchanged := is_equal_approx(float(ctx.simulation_result.score), before_score) and is_equal_approx(float(ctx.simulation_result.minimum_distance), before_min_dist) and is_equal_approx(float(ctx.simulation_result.tolerance_threshold), before_tolerance)
    var frames_unchanged := before_hash == after_hash and ctx.simulation_result.frames.size() == 420
    if not frames_unchanged or not winning_unchanged or not metrics_unchanged: _fail("D presentation binding mutated simulation state."); return

    var review_profile: Dictionary = delivery_registry.get("profiles", {}).get("REVIEW_720", {})
    var model_hash := _sha256_text(JSON.stringify(_stable_value(d_binding.presentation_render_model)))
    if model_hash.length() != 64: _fail("Invalid D presentation render-model digest."); return
    var report := {
      "schema": OutputSchema,
      "schema_version":"1.0",
      "status":"IN_MEMORY_REVIEW_ONLY_NOT_RENDERER_INPUT",
      "frozen_c11c_manifest_sha256":FrozenManifestSha,
      "challenge_source_sha256":_sha256_bytes(source_bytes),
      "identity_facts":{
        "legacy_video_profile_id":"test_master_11s",
        "legacy_video_profile_fps":int(legacy_profile.get("fps", -1)),
        "legacy_video_profile_duration_seconds":_profile_duration(legacy_profile),
        "inline_timeline_fps":int(source.get("video", {}).get("fps", -1)),
        "inline_timeline_duration_seconds":_inline_duration(source.get("video", {})),
        "inline_timeline_total_frames":int(source.get("video", {}).get("fps", 0) * _inline_duration(source.get("video", {}))),
        "matching_named_timeline_profile_id":"parking_v2_social_15s",
        "source_presentation_profile_id":requested_presentation_profile,
        "legacy_runtime_bound_presentation_profile_id":legacy_binding_profile,
        "d_presentation_profile_id":str(d_binding.presentation_profile.profile_id),
        "delivery_profile_id":"REVIEW_720",
        "delivery_profile_fps":int(review_profile.get("fps", -1)),
        "delivery_width":int(review_profile.get("width", -1)),
        "delivery_height":int(review_profile.get("height", -1))
      },
      "runtime_rebind":{"runtime_success":true,"legacy_binding_success":bool(ctx.presentation_binding.success),"d_binding_success":bool(d_binding.success),"d_binding_profile_id":str(d_binding.presentation_profile.profile_id),"d_binding_render_model_sha256":model_hash},
      "simulation_invariance":{"frame_signature_sha256_before":before_hash,"frame_signature_sha256_after":after_hash,"frame_signature_unchanged":before_hash==after_hash,"winning_frame_before":before_winning,"winning_frame_after":int(ctx.simulation_result.winning_frame),"winning_frame_unchanged":winning_unchanged,"game_frame_count_before":420,"game_frame_count_after":ctx.simulation_result.frames.size(),"metrics_unchanged":metrics_unchanged},
      "execution_boundary":{"mode":"GODOT_HEADLESS_IN_MEMORY_REVIEW_ONLY","c11c_source_mutation":false,"runtime_report_file_written":false,"renderer_native_input_emitted":false,"renderer_dispatch_invoked":false,"renderer_activation":false,"production_execution":false,"media_output_created":false,"output_artifact_path":null,"d4_8":"BLOCKED","release_authority":"NONE"}
    }
    if not _validate_report(report): _fail("Identity separation report invalid."); return
    print("C11-D RENDERER PROFILE IDENTITY SEPARATION PASS | source_identities=3/3 | legacy_timeline_conflict=EXPLICITLY_ISOLATED | runtime_rebind=PASS | profile=test_master_11s->social_default_v1 | delivery=REVIEW_720@30FPS | timeline=900@60FPS | simulation_invariance=PASS | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
    print("C11-D PROFILE IDENTITY SEPARATION SUMMARY=" + JSON.stringify(report))
    quit(0)

func _read_json(path: String) -> Dictionary:
    var bytes := FileAccess.get_file_as_bytes(path)
    var value: Variant = JSON.parse_string(bytes.get_string_from_utf8()) if not bytes.is_empty() else null
    return value if value is Dictionary else {}

func _validate_static_profile_facts(source: Dictionary, legacy: Dictionary, matching: Dictionary, delivery: Dictionary) -> bool:
    var source_video: Dictionary = source.get("video", {})
    var source_phases := {"hook_duration":3.0,"game_duration":7.0,"reveal_duration":3.0,"cta_duration":2.0}
    var legacy_phases: Dictionary = legacy.get("phases", {})
    var legacy_expected := {"hook_duration":2.0,"game_duration":6.0,"reveal_duration":1.0,"cta_duration":2.0}
    var matching_expected := {"hook_duration":3.0,"game_duration":7.0,"reveal_duration":3.0,"cta_duration":2.0}
    var delivery_profile: Dictionary = delivery.get("profiles", {}).get("REVIEW_720", {})
    return int(source_video.get("fps", -1)) == 60 and source_video.size() == 5 and source_phases == _timeline_phases(source_video) and int(legacy.get("fps", -1)) == 30 and legacy_phases == legacy_expected and int(matching.get("fps", -1)) == 60 and matching.get("phases", {}) == matching_expected and int(delivery_profile.get("fps", -1)) == 30 and int(delivery_profile.get("width", -1)) == 720 and int(delivery_profile.get("height", -1)) == 1280

func _timeline_phases(video: Dictionary) -> Dictionary:
    return {"hook_duration":float(video.get("hook_duration", -1)),"game_duration":float(video.get("game_duration", -1)),"reveal_duration":float(video.get("reveal_duration", -1)),"cta_duration":float(video.get("cta_duration", -1))}

func _profile_duration(profile: Dictionary) -> float:
    var phases: Dictionary = profile.get("phases", {})
    return float(phases.get("hook_duration", 0)) + float(phases.get("game_duration", 0)) + float(phases.get("reveal_duration", 0)) + float(phases.get("cta_duration", 0))

func _inline_duration(video: Dictionary) -> float:
    return float(video.get("hook_duration", 0)) + float(video.get("game_duration", 0)) + float(video.get("reveal_duration", 0)) + float(video.get("cta_duration", 0))

func _validate_report(report: Dictionary) -> bool:
    if report.get("schema", "") != OutputSchema or report.get("status", "") != "IN_MEMORY_REVIEW_ONLY_NOT_RENDERER_INPUT": return false
    if report.get("frozen_c11c_manifest_sha256", "") != FrozenManifestSha: return false
    var f: Dictionary = report.get("identity_facts", {})
    if f.get("legacy_video_profile_id", "") != "test_master_11s" or f.get("legacy_video_profile_duration_seconds", 0) != 11.0 or f.get("inline_timeline_duration_seconds", 0) != 15.0 or f.get("inline_timeline_total_frames", 0) != 900: return false
    if f.get("legacy_runtime_bound_presentation_profile_id", "") != "test_master_11s" or f.get("source_presentation_profile_id", "") != "social_default_v1" or f.get("d_presentation_profile_id", "") != "social_default_v1": return false
    if f.get("delivery_profile_id", "") != "REVIEW_720" or f.get("delivery_profile_fps", 0) != 30: return false
    var rb: Dictionary = report.get("runtime_rebind", {})
    if rb.get("runtime_success") != true or rb.get("d_binding_success") != true or rb.get("d_binding_profile_id", "") != "social_default_v1": return false
    var inv: Dictionary = report.get("simulation_invariance", {})
    if inv.get("frame_signature_unchanged") != true or inv.get("winning_frame_unchanged") != true or inv.get("metrics_unchanged") != true or inv.get("game_frame_count_before") != 420 or inv.get("game_frame_count_after") != 420: return false
    var boundary: Dictionary = report.get("execution_boundary", {})
    for key in ["c11c_source_mutation","runtime_report_file_written","renderer_native_input_emitted","renderer_dispatch_invoked","renderer_activation","production_execution","media_output_created"]:
        if boundary.get(key) != false: return false
    return boundary.get("d4_8", "") == "BLOCKED" and boundary.get("release_authority", "") == "NONE" and boundary.get("output_artifact_path", "not-null") == null

func _frame_signature_sha256(sim) -> String:
    var parts := PackedStringArray()
    for index in range(sim.frames.size()):
        var frame = sim.frames[index]
        if frame == null or not frame.is_valid_snapshot(): return ""
        parts.append("%d|%.9f|%.9f|%.9f|%.9f|%.9f|%.9f|%.9f|%d|%d|%s" % [index,frame.position.x,frame.position.y,frame.rotation,frame.scale.x,frame.scale.y,frame.opacity,float(frame.texture_index),int(frame.variant_id),int(frame.custom_data.size()),JSON.stringify(_stable_value(frame.custom_data))])
    return _sha256_text("\n".join(parts))

func _stable_value(value: Variant) -> Variant:
    if value is Dictionary:
        var output: Dictionary = {}; var keys: Array = value.keys(); keys.sort_custom(func(a,b): return str(a)<str(b))
        for key in keys: output[str(key)] = _stable_value(value[key])
        return output
    if value is Array:
        var output_array: Array = []; for item in value: output_array.append(_stable_value(item)); return output_array
    if value is Vector2: return {"$type":"Vector2","x":value.x,"y":value.y}
    if value is Vector2i: return {"$type":"Vector2i","x":value.x,"y":value.y}
    if value is Color: return {"$type":"Color","r":value.r,"g":value.g,"b":value.b,"a":value.a}
    if value is Rect2: return {"$type":"Rect2","position":_stable_value(value.position),"size":_stable_value(value.size)}
    if value is String or value is StringName or value is int or value is float or value is bool or value == null: return value
    return str(value)

func _sha256_text(value: String) -> String:
    return _sha256_bytes(value.to_utf8_buffer())
func _sha256_bytes(bytes: PackedByteArray) -> String:
    var context := HashingContext.new(); context.start(HashingContext.HASH_SHA256); context.update(bytes); return context.finish().hex_encode()
func _fail(message: String) -> void:
    printerr("C11-D RENDERER PROFILE IDENTITY SEPARATION FAIL | %s" % message); quit(1)
