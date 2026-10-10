extends SceneTree

## D9 review-only harness: invokes the existing effective C11-C runtime twice and hashes the in-memory result.
## It never writes a report/payload, loads visual assets, creates frames, or invokes a renderer.
const ChallengeRuntimeBridgeScript = preload("res://core/execution/ChallengeRuntimeBridge.gd")
const FrozenManifestPath := "res://release/C11C_FREEZE_PACKAGE_MANIFEST.json"
const ChallengeSourcePath := "res://challenges/CHALLENGE_004.json"
const FrozenManifestSha256 := "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
const OutputSchema := "C11-D-D9-RENDERER-CHALLENGE-RUNTIME-OUTPUT-PREVIEW-V1"

func _initialize() -> void:
    call_deferred("_run")

func _run() -> void:
    var manifest_bytes := FileAccess.get_file_as_bytes(FrozenManifestPath)
    if manifest_bytes.is_empty() or _sha256_bytes(manifest_bytes) != FrozenManifestSha256:
        _fail("Frozen C11-C manifest hash mismatch.")
        return
    var challenge_bytes := FileAccess.get_file_as_bytes(ChallengeSourcePath)
    if challenge_bytes.is_empty():
        _fail("CHALLENGE_004 source is missing or unreadable.")
        return
    var legacy_config: Variant = JSON.parse_string(challenge_bytes.get_string_from_utf8())
    if not (legacy_config is Dictionary) or legacy_config.get("challenge_id", "") != "CHALLENGE_004":
        _fail("CHALLENGE_004 source identity mismatch.")
        return
    if not _validate_source_fixture(legacy_config):
        _fail("CHALLENGE_004 source fixture drifted from the pinned temporal/editorial contract.")
        return

    var first := _execute_runtime(legacy_config)
    if not bool(first.get("success", false)):
        _fail("First frozen effective runtime invocation failed: %s" % str(first.get("error", "unknown error")))
        return
    var second := _execute_runtime(legacy_config)
    if not bool(second.get("success", false)):
        _fail("Second frozen effective runtime invocation failed: %s" % str(second.get("error", "unknown error")))
        return
    var first_summary: Dictionary = first["summary"]
    var second_summary: Dictionary = second["summary"]
    var repeated := str(first_summary.get("runtime_output_sha256", "")) == str(second_summary.get("runtime_output_sha256", ""))
    if not repeated:
        _fail("Repeated ChallengeRuntimeBridge execution produced different runtime-output hashes.")
        return

    var source_sha := _sha256_bytes(challenge_bytes)
    var report := {
        "schema": OutputSchema,
        "schema_version": "1.0",
        "status": "IN_MEMORY_REVIEW_ONLY_NOT_RENDERER_INPUT",
        "frozen_c11c_manifest_sha256": FrozenManifestSha256,
        "challenge_source_sha256": source_sha,
        "challenge_runtime_output_materialized": true,
        "challenge_visual_payload_materialized": false,
        "instance": first_summary,
        "deterministic_repeat_pass": true,
        "execution_boundary": {
            "mode": "GODOT_HEADLESS_IN_MEMORY_REVIEW_ONLY",
            "runtime_called": true,
            "simulation_executed": true,
            "runtime_report_file_written": false,
            "renderer_native_input_emitted": false,
            "renderer_dispatch_invoked": false,
            "renderer_activation": false,
            "production_execution": false,
            "media_output_created": false,
            "output_artifact_path": null,
            "d4_8": "BLOCKED",
            "release_authority": "NONE",
            "c11c_source_mutation": false
        }
    }
    var errors := _validate_report(report)
    if not errors.is_empty():
        _fail("Runtime preview contract validation failed: %s" % str(errors))
        return
    print("C11-D RENDERER CHALLENGE RUNTIME OUTPUT PREVIEW PASS | materialized=1/1 | deterministic=2/2 | challenge=CHALLENGE_004:parking_v2 | phases=180>420>180>120 | total=900_FRAMES@60FPS | simulation_frames=%d | winning_frame=GAME_LOCAL_READ_ONLY | presentation_binding=PASS | visual_payload=NOT_MATERIALIZED | runtime_files=NONE | renderer_input=NOT_EMITTED | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE" % int(first_summary["game_frame_count"]))
    print("C11-D CHALLENGE RUNTIME OUTPUT PREVIEW SUMMARY=" + JSON.stringify(report))
    quit(0)

func _execute_runtime(legacy_config: Dictionary) -> Dictionary:
    var result: Dictionary = ChallengeRuntimeBridgeScript.run_effective_pipeline(legacy_config)
    if not bool(result.get("success", false)):
        return {"success": false, "error": str(result.get("error", result.get("error_code", "runtime failed")))}
    var context = result.get("context", null)
    if context == null or context.simulation_result == null or context.timeline == null or context.presentation_binding == null:
        return {"success": false, "error": "Effective runtime returned an incomplete ChallengeRuntimeContext."}
    var sim = context.simulation_result
    var timeline = context.timeline
    var binding = context.presentation_binding
    if sim.error_state != "OK" or not binding.success:
        return {"success": false, "error": "Simulation or presentation binding is not valid."}
    if sim.frames.size() != int(timeline.game_frames) or int(timeline.total_frames) != 900:
        return {"success": false, "error": "Runtime frame cardinality disagrees with the canonical timeline."}

    var canonical: Dictionary = context.canonical_v2
    var runtime_input: Dictionary = result.get("runtime_input", {})
    var content: Dictionary = canonical.get("content", {})
    var assets: Dictionary = binding.physical_assets
    var seed_meta: Dictionary = sim.metadata
    var frame_hash := _frame_signature_sha256(sim)
    var model_hash := _sha256_text(JSON.stringify(_stable_value(binding.presentation_render_model)))
    var phases := {"hook": int(timeline.hook_frames), "game": int(timeline.game_frames), "reveal": int(timeline.reveal_frames), "cta": int(timeline.cta_frames)}
    var timeline_seconds := float(timeline.total_frames) / float(timeline.fps)
    var summary_payload := {
        "content_type": "challenges",
        "challenge_id": str(canonical.get("challenge_id", "")),
        "mechanic": str(canonical.get("mechanic", "")),
        "mechanic_version": str(canonical.get("mechanic_version", "")),
        "asset_family": str(canonical.get("asset_family", "")),
        "asset_family_version": str(canonical.get("asset_family_version", "")),
        "seed_requested": 314159,
        "seed_used": int(seed_meta.get("seed_used", seed_meta.get("final_seed", 314159))),
        "rng_version": str(seed_meta.get("rng_version", "")),
        "editorial_content": {"hook": str(content.get("hook", "")), "reveal": str(content.get("reveal", "")), "cta": str(content.get("cta", ""))},
        "fps": int(timeline.fps),
        "phase_frames": phases,
        "total_frames": int(timeline.total_frames),
        "duration_seconds": timeline_seconds,
        "game_frame_count": int(sim.frames.size()),
        "winning_frame_local": int(sim.winning_frame),
        "score": float(sim.score),
        "minimum_distance": float(sim.minimum_distance),
        "tolerance_threshold": float(sim.tolerance_threshold),
        "simulation_error_state": str(sim.error_state),
        "attempts": int(seed_meta.get("attempts", 1)),
        "frame_signature_sha256": frame_hash,
        "presentation_binding_success": bool(binding.success),
        "presentation_profile_id": str(binding.presentation_profile.profile_id) if binding.presentation_profile != null else "",
        "physical_asset_bindings": {"background_path": str(assets.get("background_path", "")), "target_path": str(assets.get("target_path", "")), "object_path": str(assets.get("object_path", ""))},
        "presentation_render_model_sha256": model_hash,
        "materialization": "IN_MEMORY_ONLY_RUNTIME_RESULT_NOT_VISUAL_PAYLOAD"
    }
    var runtime_digest_input := {
        "source_challenge_id": str(legacy_config.get("challenge_id", "")),
        "runtime_input": _stable_value(runtime_input),
        "canonical_v2": _stable_value(canonical),
        "summary": summary_payload,
        "frame_signature_sha256": frame_hash
    }
    summary_payload["runtime_output_sha256"] = _sha256_text(JSON.stringify(_stable_value(runtime_digest_input)))
    return {"success": true, "summary": summary_payload}

func _frame_signature_sha256(sim) -> String:
    var parts := PackedStringArray()
    for index in range(sim.frames.size()):
        var frame = sim.frames[index]
        if frame == null or not frame.is_valid_snapshot():
            return ""
        parts.append("%d|%.9f|%.9f|%.9f|%.9f|%.9f|%.9f|%.9f|%d|%d|%s" % [
            index, frame.position.x, frame.position.y, frame.rotation, frame.scale.x, frame.scale.y,
            frame.opacity, float(frame.texture_index), int(frame.variant_id), int(frame.custom_data.size()),
            JSON.stringify(_stable_value(frame.custom_data))
        ])
    return _sha256_text("\n".join(parts))

func _stable_value(value: Variant) -> Variant:
    if value is Dictionary:
        var output: Dictionary = {}
        var keys: Array = value.keys()
        keys.sort_custom(func(a, b): return str(a) < str(b))
        for key in keys:
            output[str(key)] = _stable_value(value[key])
        return output
    if value is Array:
        var output_array: Array = []
        for item in value:
            output_array.append(_stable_value(item))
        return output_array
    if value is Vector2:
        return {"$type": "Vector2", "x": value.x, "y": value.y}
    if value is Vector2i:
        return {"$type": "Vector2i", "x": value.x, "y": value.y}
    if value is Vector3:
        return {"$type": "Vector3", "x": value.x, "y": value.y, "z": value.z}
    if value is Color:
        return {"$type": "Color", "r": value.r, "g": value.g, "b": value.b, "a": value.a}
    if value is Rect2:
        return {"$type": "Rect2", "position": _stable_value(value.position), "size": _stable_value(value.size)}
    if value is String or value is StringName or value is int or value is float or value is bool or value == null:
        return value
    return str(value)

func _validate_source_fixture(source: Dictionary) -> bool:
    if str(source.get("mechanic", "")) != "parking_v2" or str(source.get("mechanic_version", "")) != "2.0": return false
    if str(source.get("asset_family", "")) != "fam_garage_01" or str(source.get("asset_family_version", "")) != "1.0": return false
    if int(source.get("generation", {}).get("seed", -1)) != 314159 or str(source.get("generation", {}).get("rng_version", "")) != "2.0": return false
    var video: Dictionary = source.get("video", {})
    if int(video.get("fps", -1)) != 60: return false
    if float(video.get("hook_duration", -1.0)) != 3.0 or float(video.get("game_duration", -1.0)) != 7.0 or float(video.get("reveal_duration", -1.0)) != 3.0 or float(video.get("cta_duration", -1.0)) != 2.0: return false
    var content: Dictionary = source.get("content", {})
    return str(content.get("hook", "")) == "¡SOLO EL 1% APARCA SIN ROZAR!" and str(content.get("cta", "")) == "¿Lo has clavado?"

func _validate_report(report: Dictionary) -> Array[String]:
    var errors: Array[String] = []
    if report.get("schema", "") != OutputSchema: errors.append("schema identity")
    if report.get("status", "") != "IN_MEMORY_REVIEW_ONLY_NOT_RENDERER_INPUT": errors.append("status")
    if report.get("frozen_c11c_manifest_sha256", "") != FrozenManifestSha256: errors.append("frozen manifest")
    if report.get("challenge_runtime_output_materialized") != true or report.get("challenge_visual_payload_materialized") != false: errors.append("materialization boundary")
    if report.get("deterministic_repeat_pass") != true: errors.append("repeat determinism")
    var instance: Dictionary = report.get("instance", {})
    if instance.get("challenge_id", "") != "CHALLENGE_004" or instance.get("mechanic", "") != "parking_v2": errors.append("challenge identity")
    if instance.get("phase_frames", {}) != {"hook": 180, "game": 420, "reveal": 180, "cta": 120} or instance.get("total_frames", 0) != 900: errors.append("timeline phase contract")
    if instance.get("game_frame_count", 0) != 420 or instance.get("simulation_error_state", "") != "OK": errors.append("simulation result contract")
    if instance.get("editorial_content", {}).get("hook", "") != "¡SOLO EL 1% APARCA SIN ROZAR!" or instance.get("editorial_content", {}).get("cta", "") != "¿Lo has clavado?": errors.append("editorial source fidelity")
    if not bool(instance.get("presentation_binding_success", false)): errors.append("presentation binding")
    for digest_field in ["frame_signature_sha256", "presentation_render_model_sha256", "runtime_output_sha256"]:
        if not str(instance.get(digest_field, "")).is_valid_hex_number() or str(instance.get(digest_field, "")).length() != 64: errors.append("digest %s" % digest_field)
    var boundary: Dictionary = report.get("execution_boundary", {})
    for key in ["runtime_report_file_written", "renderer_native_input_emitted", "renderer_dispatch_invoked", "renderer_activation", "production_execution", "media_output_created", "c11c_source_mutation"]:
        if boundary.get(key) != false: errors.append("boundary %s" % key)
    if boundary.get("d4_8", "") != "BLOCKED" or boundary.get("release_authority", "") != "NONE" or boundary.get("output_artifact_path", "not-null") != null: errors.append("authority/output")
    return errors

func _sha256_text(text_value: String) -> String:
    return _sha256_bytes(text_value.to_utf8_buffer())

func _sha256_bytes(bytes: PackedByteArray) -> String:
    var context := HashingContext.new()
    context.start(HashingContext.HASH_SHA256)
    context.update(bytes)
    return context.finish().hex_encode()

func _fail(message: String) -> void:
    printerr("C11-D RENDERER CHALLENGE RUNTIME OUTPUT PREVIEW FAIL | %s" % message)
    quit(1)
