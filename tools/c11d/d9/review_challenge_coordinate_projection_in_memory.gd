extends SceneTree

## C11-D review-only coordinate projection. This computes a detached projected
## coordinate record set in memory; it creates no SceneTree nodes, does not draw,
## does not resample frames, does not dispatch renderer input, and writes no files.
const RuntimeBridge = preload("res://core/execution/ChallengeRuntimeBridge.gd")
const PresentationBinder = preload("res://core/presentation/ChallengePresentationBinder.gd")
const CoordinateMapper = preload("res://core/presentation/CoordinateMapper.gd")
const ChallengePath := "res://challenges/CHALLENGE_004.json"
const ManifestPath := "res://release/C11C_FREEZE_PACKAGE_MANIFEST.json"
const ContractPath := "res://definitions/c11d/production/D_RENDERER_CHALLENGE_COORDINATE_PROJECTION_V1.json"
const SchemaPath := "res://definitions/c11d/production/D_RENDERER_CHALLENGE_COORDINATE_PROJECTION_SCHEMA_V1.json"
const DeliveryProfilesPath := "res://profiles/delivery/c11c_video_delivery_profiles.json"
const FrozenManifestSha := "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
const ChallengeSha := "6a674c02c2d8831a872691954f1cc40e2492193f9b136f60656730a7be686b71"
const ContractId := "C11-D-D9-RENDERER-CHALLENGE-COORDINATE-PROJECTION-CONTRACT-V1"
const ReportId := "C11-D-D9-RENDERER-CHALLENGE-COORDINATE-PROJECTION-PREVIEW-V1"
const SourcePins := {
    "challenges/CHALLENGE_004.json": "6a674c02c2d8831a872691954f1cc40e2492193f9b136f60656730a7be686b71",
    "core/presentation/CoordinateMapper.gd": "244bace2eaf87e29d653715ae18c0b4824cdf9503e915932be53d0f52bbe461c",
    "core/presentation/PresentationProfile.gd": "187b1cf8ab96b9031785a0f36b0054a60383c97cb3d81906c7d9bbcd373bef24",
    "core/presentation/ChallengePresentationBinder.gd": "755ecfc9cc6e1ee51738938583217ab8a470c1a1f290bb107e91e19990d74b47",
    "core/execution/ChallengeRuntimeBridge.gd": "c53f04df064b3697f8dd02cd779f8ef002a4e3e2d40fa0e01aa7d9b1a80a8191",
    "core/execution/ChallengeTimelineBuilder.gd": "35a47ad126a2e11577933a03b251f47732e580693e5c08e45d3b6af047c8c9af",
    "core/mechanics/parking/ParkingMechanicV2.gd": "c78dbc1adcc95ad4981f3c704c69630edc54c25473c479f10bb154efe6f105cd",
    "core/data/FrameSnapshot.gd": "61060d0937063400447cd5f2513265cb82d8e38017f5bd097c2870da03967180",
    "profiles/delivery/c11c_video_delivery_profiles.json": "967831513eb225e6eafd56496ce0d0a0b0f0e158d205b5985e7bba11b0534ae3",
    "assets/c6/garage_background.svg": "c9d8acdae725ca7726fc8ad23a046e4aac4d9e454b45db40d2c770732b31ab1e",
    "assets/c6/car.svg": "93a6f78d9654f7917ab2287800858a937e9c68c458cc60bf417d6f2b98c1a96d",
    "assets/c6/parking_target.svg": "ec2dcafd7dfc99ff501eb2d93b93906680a30c48cf0741807cbbdd915a18cfb3",
    "definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_PREVIEW_V1.json": "67daa1f83ac151906059695bb4d87974819c2d16d3715b78b00657bfdac54f7a"
}
const ExpectedAssetSizes := {
    "BACKGROUND": Vector2i(1080, 1920),
    "ANIMATED_OBJECT": Vector2i(160, 320),
    "TARGET": Vector2i(200, 400)
}

func _initialize() -> void:
    call_deferred("_run")

func _run() -> void:
    var manifest_bytes: PackedByteArray = FileAccess.get_file_as_bytes(ManifestPath)
    if manifest_bytes.is_empty() or _sha256_bytes(manifest_bytes) != FrozenManifestSha:
        _fail("Frozen C11-C manifest identity mismatch.")
        return
    if not _verify_sources():
        return
    var contract_bytes: PackedByteArray = FileAccess.get_file_as_bytes(ContractPath)
    var contract_value: Variant = JSON.parse_string(contract_bytes.get_string_from_utf8())
    if not (contract_value is Dictionary) or not _contract_guard(contract_value):
        _fail("Coordinate projection contract/schema/governance guard failed.")
        return
    var challenge_bytes: PackedByteArray = FileAccess.get_file_as_bytes(ChallengePath)
    var challenge_value: Variant = JSON.parse_string(challenge_bytes.get_string_from_utf8())
    if not (challenge_value is Dictionary):
        _fail("CHALLENGE_004 source is not an object.")
        return
    var source: Dictionary = challenge_value
    if str(source.get("challenge_id", "")) != "CHALLENGE_004" or str(source.get("mechanic", "")) != "parking_v2":
        _fail("Canonical challenge identity mismatch.")
        return

    var delivery_bytes: PackedByteArray = FileAccess.get_file_as_bytes(DeliveryProfilesPath)
    var delivery_value: Variant = JSON.parse_string(delivery_bytes.get_string_from_utf8())
    if not (delivery_value is Dictionary):
        _fail("Delivery profiles registry is invalid.")
        return
    var delivery_registry: Dictionary = delivery_value
    var delivery_profiles: Dictionary = delivery_registry.get("profiles", {})
    var delivery_profile: Dictionary = delivery_profiles.get("REVIEW_720", {})
    if int(delivery_profile.get("width", 0)) != 720 or int(delivery_profile.get("height", 0)) != 1280 or int(delivery_profile.get("fps", 0)) != 30:
        _fail("REVIEW_720 delivery profile does not match its pinned 720x1280@30 contract.")
        return
    var presentation_canvas := Vector2(540.0, 960.0)
    var delivery_canvas := Vector2(720.0, 1280.0)
    var source_canvas := Vector2(1080.0, 1920.0)
    var transform: Dictionary = CoordinateMapper.get_fit_transform(Rect2(Vector2.ZERO, presentation_canvas), true)
    if not bool(transform.get("valid", false)):
        _fail("CoordinateMapper rejected the presentation source canvas.")
        return
    var mapper_scale: Vector2 = transform.get("scale", Vector2.ZERO)
    var mapper_offset: Vector2 = transform.get("offset", Vector2.ZERO)
    var delivery_scale := Vector2(delivery_canvas.x / presentation_canvas.x, delivery_canvas.y / presentation_canvas.y)
    var combined_scale := Vector2(mapper_scale.x * delivery_scale.x, mapper_scale.y * delivery_scale.y)
    if not _near(mapper_scale.x, 0.5) or not _near(mapper_scale.y, 0.5) or not _near(mapper_offset.x, 0.0) or not _near(mapper_offset.y, 0.0):
        _fail("CoordinateMapper transform no longer matches the declared 1080x1920 -> 540x960 mapping.")
        return
    if not _near(delivery_scale.x, 4.0 / 3.0) or not _near(delivery_scale.y, 4.0 / 3.0) or not _near(combined_scale.x, 2.0 / 3.0) or not _near(combined_scale.y, 2.0 / 3.0):
        _fail("The composed projection is not a uniform 2/3 transform.")
        return
    if not _near(source_canvas.x / source_canvas.y, presentation_canvas.x / presentation_canvas.y) or not _near(presentation_canvas.x / presentation_canvas.y, delivery_canvas.x / delivery_canvas.y):
        _fail("The projection canvases do not share a 9:16 aspect ratio.")
        return
    var mapped_origin: Vector2 = CoordinateMapper.map_position(Vector2.ZERO, CoordinateMapper.CoordinateSpace.CANVAS_1080X1920, presentation_canvas)
    var mapped_end: Vector2 = CoordinateMapper.map_position(source_canvas, CoordinateMapper.CoordinateSpace.CANVAS_1080X1920, presentation_canvas)
    if not _near(mapped_origin.x, 0.0) or not _near(mapped_origin.y, 0.0) or not _near(mapped_end.x, 540.0) or not _near(mapped_end.y, 960.0):
        _fail("CoordinateMapper endpoint behavior is inconsistent with the declared source canvas.")
        return

    var first_result: Dictionary = RuntimeBridge.run_effective_pipeline(source)
    var second_result: Dictionary = RuntimeBridge.run_effective_pipeline(source)
    if not bool(first_result.get("success", false)) or not bool(second_result.get("success", false)):
        _fail("Frozen runtime execution failed during coordinate projection preview.")
        return
    var first_context: Variant = first_result.get("context", null)
    var second_context: Variant = second_result.get("context", null)
    if first_context == null or second_context == null or first_context.simulation_result == null or second_context.simulation_result == null or first_context.timeline == null:
        _fail("Frozen runtime returned incomplete simulation/timeline context.")
        return
    var sim: Variant = first_context.simulation_result
    var sim_repeat: Variant = second_context.simulation_result
    var timeline: Variant = first_context.timeline
    if str(sim.error_state) != "OK" or int(sim.frames.size()) != 420 or int(timeline.fps) != 60 or int(timeline.total_frames) != 900:
        _fail("Source timebase or GAME snapshot count changed.")
        return
    var signature_before: String = _frame_signature_sha256(sim)
    var signature_repeat: String = _frame_signature_sha256(sim_repeat)
    if signature_before.is_empty() or signature_before != signature_repeat:
        _fail("Runtime source frame signature did not repeat deterministically.")
        return
    var before_winning: int = int(sim.winning_frame)
    var before_score: float = float(sim.score)
    var before_minimum: float = float(sim.minimum_distance)
    var before_tolerance: float = float(sim.tolerance_threshold)

    var bind_result: Dictionary = _bind_d_profile(source, first_context)
    var bind_repeat: Dictionary = _bind_d_profile(source, second_context)
    if not bool(bind_result.get("success", false)) or not bool(bind_repeat.get("success", false)):
        _fail("D presentation binding failed: %s" % str(bind_result.get("error", bind_repeat.get("error", "unknown"))))
        return
    if str(bind_result.get("render_model_sha256", "")) != str(bind_repeat.get("render_model_sha256", "")):
        _fail("D presentation render model did not repeat deterministically.")
        return

    var source_frame_records: Array[Dictionary] = []
    var projected_frame_records: Array[Dictionary] = []
    for index: int in range(sim.frames.size()):
        var frame: Variant = sim.frames[index]
        if frame == null or not frame.is_valid_snapshot():
            _fail("Invalid source GAME snapshot at index %d." % index)
            return
        var source_position: Vector2 = frame.position
        var presentation_position: Vector2 = CoordinateMapper.map_position(source_position, CoordinateMapper.CoordinateSpace.CANVAS_1080X1920, presentation_canvas)
        var delivery_position := Vector2(presentation_position.x * delivery_scale.x, presentation_position.y * delivery_scale.y)
        source_frame_records.append({
            "source_game_frame_index": index,
            "position": _vector2_value(source_position),
            "rotation_radians": float(frame.rotation),
            "scale": _vector2_value(frame.scale),
            "opacity": float(frame.opacity),
            "texture_index": int(frame.texture_index),
            "variant_id": int(frame.variant_id)
        })
        projected_frame_records.append({
            "source_game_frame_index": index,
            "source_position": _vector2_value(source_position),
            "presentation_canvas_position": _vector2_value(presentation_position),
            "delivery_position": _vector2_value(delivery_position),
            "rotation_radians_preserved": float(frame.rotation),
            "local_scale_multiplier_preserved": _vector2_value(frame.scale),
            "opacity_preserved": float(frame.opacity),
            "texture_index_preserved": int(frame.texture_index),
            "variant_id_preserved": int(frame.variant_id)
        })
    if source_frame_records.size() != 420 or projected_frame_records.size() != 420:
        _fail("Coordinate projection did not preserve all 420 GAME frame records.")
        return

    var projected_asset_nodes: Array[Dictionary] = []
    var source_assets: Dictionary = source.get("assets", {})
    var visual_cfg: Dictionary = source.get("presentation", {}).get("visual", {})
    var parking_cfg: Dictionary = source.get("difficulty", {}).get("parking", {})
    var asset_specs: Array[Dictionary] = [
        {"role": "BACKGROUND", "path": str(source_assets.get("background_path", "")), "rel": "assets/c6/garage_background.svg", "size": Vector2i(1080, 1920), "declared_scale": 1.0, "declared_offset": [0.0, 0.0]},
        {"role": "ANIMATED_OBJECT", "path": str(source_assets.get("object_path", "")), "rel": "assets/c6/car.svg", "size": Vector2i(160, 320), "declared_scale": float(visual_cfg.get("object_scale", 0.85)), "declared_offset": visual_cfg.get("object_offset", [0.0, 0.0])},
        {"role": "TARGET", "path": str(source_assets.get("target_path", "")), "rel": "assets/c6/parking_target.svg", "size": Vector2i(200, 400), "declared_scale": float(visual_cfg.get("target_scale", 0.85)), "declared_offset": visual_cfg.get("target_offset", [0.0, 0.0])}
    ]
    for spec: Dictionary in asset_specs:
        var path: String = str(spec.get("path", ""))
        var bytes: PackedByteArray = FileAccess.get_file_as_bytes(path)
        if bytes.is_empty():
            _fail("Canonical asset missing/empty: %s" % path)
            return
        var texture_resource: Resource = ResourceLoader.load(path) as Resource
        if texture_resource == null or not (texture_resource is Texture2D):
            _fail("Canonical asset did not load as Texture2D: %s" % path)
            return
        var texture: Texture2D = texture_resource as Texture2D
        var expected_size: Vector2i = spec.get("size", Vector2i.ZERO)
        var pinned_expected: Vector2i = ExpectedAssetSizes.get(str(spec.get("role", "")), Vector2i.ZERO)
        if expected_size != pinned_expected or int(texture.get_width()) != expected_size.x or int(texture.get_height()) != expected_size.y:
            _fail("Canonical asset intrinsic size mismatch: %s" % path)
            return
        var projected_size := Vector2(float(expected_size.x) * combined_scale.x, float(expected_size.y) * combined_scale.y)
        var declared_offset: Array = spec.get("declared_offset", [0.0, 0.0])
        if declared_offset.size() != 2:
            _fail("Canonical asset declared offset must contain exactly two coordinates: %s" % path)
            return
        var projected_offset: Array[float] = []
        projected_offset.append(float(declared_offset[0]) * combined_scale.x)
        projected_offset.append(float(declared_offset[1]) * combined_scale.y)
        projected_asset_nodes.append({
            "role": str(spec.get("role", "")),
            "resource_path": path,
            "sha256": _sha256_bytes(bytes),
            "intrinsic_size": [expected_size.x, expected_size.y],
            "projected_delivery_base_size": _vector2_value(projected_size),
            "declared_scale_preserved_separately": float(spec.get("declared_scale", 1.0)),
            "declared_offset_source": declared_offset,
            "declared_offset_delivery": projected_offset,
            "loaded_as_texture2d": true
        })

    var target_values: Array = parking_cfg.get("target_position", [])
    if target_values.size() != 2:
        _fail("Canonical target position is missing or malformed.")
        return
    var target_source := Vector2(float(target_values[0]), float(target_values[1]))
    var target_presentation := CoordinateMapper.map_position(target_source, CoordinateMapper.CoordinateSpace.CANVAS_1080X1920, presentation_canvas)
    var target_delivery := Vector2(target_presentation.x * delivery_scale.x, target_presentation.y * delivery_scale.y)
    # Godot Vector2 uses single-precision components in this build. The source-to-
    # presentation coordinates are integral and checked tightly; the composed
    # 4/3 delivery multiplier is not exactly representable, so allow 1e-4 px for
    # the X result instead of the generic 1e-6 comparison tolerance.
    var target_projection_ok: bool = (
        _near(target_presentation.x, 425.0)
        and _near(target_presentation.y, 480.0)
        and _near(target_delivery.x, 850.0 * 2.0 / 3.0, 0.0001)
        and _near(target_delivery.y, 640.0, 0.0001)
    )
    if not target_projection_ok:
        _fail(
            "Canonical target position projected incorrectly: source=%s presentation=%s delivery=%s expected_presentation=(425,480) expected_delivery=(566.666667,640) tolerance_delivery_px=0.0001"
            % [_vector2_value(target_source), _vector2_value(target_presentation), _vector2_value(target_delivery)]
        )
        return

    var source_records_sha: String = _sha256_text(JSON.stringify(_stable_value(source_frame_records)))
    var projected_records_sha: String = _sha256_text(JSON.stringify(_stable_value(projected_frame_records)))
    var source_records_sha_repeat: String = _sha256_text(JSON.stringify(_stable_value(_source_frame_records(sim_repeat))))
    var projected_repeat: Array[Dictionary] = _project_frame_records(sim_repeat, presentation_canvas, delivery_scale)
    if source_records_sha.is_empty() or projected_records_sha.is_empty() or source_records_sha != source_records_sha_repeat or projected_records_sha != _sha256_text(JSON.stringify(_stable_value(projected_repeat))):
        _fail("Source/projected frame hashes did not repeat deterministically.")
        return

    var signature_after: String = _frame_signature_sha256(sim)
    var invariance: bool = signature_before == signature_after and int(sim.winning_frame) == before_winning and is_equal_approx(float(sim.score), before_score) and is_equal_approx(float(sim.minimum_distance), before_minimum) and is_equal_approx(float(sim.tolerance_threshold), before_tolerance) and int(sim.frames.size()) == 420
    if not invariance:
        _fail("Projection preview altered SimulationResult truth.")
        return

    var lineage: Array[Dictionary] = [{"path": "release/C11C_FREEZE_PACKAGE_MANIFEST.json", "sha256": FrozenManifestSha}]
    for rel_path: String in SourcePins.keys():
        lineage.append({"path": rel_path, "sha256": str(SourcePins[rel_path])})
    lineage.sort_custom(func(a: Dictionary, b: Dictionary) -> bool: return str(a.get("path", "")) < str(b.get("path", "")))

    var report: Dictionary = {
        "schema": ReportId,
        "schema_version": "1.0",
        "status": "IN_MEMORY_REVIEW_ONLY_PROJECTION_PREVIEW_NOT_RENDERER_INPUT",
        "frozen_c11c_manifest_sha256": FrozenManifestSha,
        "challenge_source_sha256": ChallengeSha,
        "projection": {
            "policy_id": "C11D_CHALLENGE_COORDINATE_PROJECTION_1080_TO_540_TO_REVIEW720_V1",
            "state": "PROPOSED_NOT_APPROVED",
            "source_coordinate_space": "CANVAS_1080X1920",
            "source_size": {"width": 1080, "height": 1920},
            "presentation_source_canvas": {"width": 540, "height": 960},
            "presentation_master_output": {"width": 1080, "height": 1920},
            "delivery_size": {"width": 720, "height": 1280},
            "stage_scales": [[mapper_scale.x, mapper_scale.y], [delivery_scale.x, delivery_scale.y]],
            "stage_offsets": [[mapper_offset.x, mapper_offset.y], [0.0, 0.0]],
            "combined_scale": [combined_scale.x, combined_scale.y],
            "combined_offset": [0.0, 0.0],
            "target_position": {"source": _vector2_array(target_source), "presentation_canvas": _vector2_array(target_presentation), "delivery": _vector2_array(target_delivery)},
            "transform_semantics": "POSITIONS_AND_INTRINSIC_BASE_DIMENSIONS_PROJECTED; LOCAL_SIMULATION_SCALE_ROTATION_OPACITY_TEXTURE_INDEX_VARIANT_ID_PRESERVED",
            "sampling_or_interpolation": "UNRESOLVED_NOT_APPLIED"
        },
        "source_timeline": {"fps": 60, "total_frames": 900, "duration_seconds": 15.0, "game_frame_count": 420},
        "delivery_profile": {"profile_id": "REVIEW_720", "fps": 30, "width": 720, "height": 1280, "total_frames": 450, "duration_seconds": 15.0},
        "projected_frames": {"source_records": 420, "projected_records": 420, "source_records_sha256": source_records_sha, "projected_records_sha256": projected_records_sha, "order_preserved": true, "local_scale_preserved": true, "other_snapshot_fields_preserved": true},
        "assets": projected_asset_nodes,
        "determinism": {"runtime_repeat_equal": true, "projection_repeat_equal": true, "source_frame_signature_repeat_equal": signature_before == signature_repeat},
        "simulation_invariance": {"frame_signature_unchanged": signature_before == signature_after, "winning_frame_unchanged": int(sim.winning_frame) == before_winning, "metrics_unchanged": is_equal_approx(float(sim.score), before_score) and is_equal_approx(float(sim.minimum_distance), before_minimum) and is_equal_approx(float(sim.tolerance_threshold), before_tolerance), "frame_count_unchanged": int(sim.frames.size()) == 420},
        "execution_boundary": {"mode": "GODOT_HEADLESS_IN_MEMORY_REVIEW_ONLY", "source_mutation": false, "projected_payload_written": false, "renderer_native_input_emitted": false, "renderer_dispatch_invoked": false, "renderer_activation": false, "media_created": false, "d4_8": "BLOCKED", "release_authority": "NONE"},
        "source_lineage": lineage
    }
    if not _validate_report(report):
        _fail("Coordinate projection report failed its own contract validation.")
        return
    print("C11-D RENDERER CHALLENGE COORDINATE PROJECTION PREVIEW PASS | source_points=420/420 | projected_points=420/420 | scales=0.5>1.333333>0.666667 | assets=3/3 | deterministic=2/2 | simulation_invariance=PASS | policy=PROPOSED_NOT_APPROVED | delivery_resampling=UNRESOLVED_NOT_APPLIED | renderer_input=NOT_EMITTED | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
    print("C11-D CHALLENGE COORDINATE PROJECTION SUMMARY=" + JSON.stringify(_stable_value(report)))
    quit(0)

func _bind_d_profile(source: Dictionary, context: Variant) -> Dictionary:
    var canonical: Dictionary = context.canonical_v2.duplicate(true)
    var presentation: Dictionary = canonical.get("presentation", {}).duplicate(true)
    presentation["profile_id"] = "social_default_v1"
    canonical["presentation"] = presentation
    var binding: Variant = PresentationBinder.bind(canonical, context.timeline, context.simulation_result)
    if binding == null or not bool(binding.success) or binding.presentation_profile == null:
        return {"success": false, "error": str(binding.error if binding != null else "null binding")}
    if str(binding.presentation_profile.profile_id) != "social_default_v1":
        return {"success": false, "error": "D presentation profile identity mismatch"}
    if binding.presentation_profile.source_canvas_size != Vector2(540.0, 960.0) or binding.presentation_profile.master_output_size != Vector2(1080.0, 1920.0):
        return {"success": false, "error": "Presentation profile canvas dimensions changed"}
    return {"success": true, "render_model_sha256": _sha256_text(JSON.stringify(_stable_value(binding.presentation_render_model)))}

func _project_frame_records(sim: Variant, presentation_canvas: Vector2, delivery_scale: Vector2) -> Array[Dictionary]:
    var records: Array[Dictionary] = []
    for index: int in range(sim.frames.size()):
        var frame: Variant = sim.frames[index]
        if frame == null or not frame.is_valid_snapshot():
            return []
        var source_position: Vector2 = frame.position
        var presentation_position: Vector2 = CoordinateMapper.map_position(source_position, CoordinateMapper.CoordinateSpace.CANVAS_1080X1920, presentation_canvas)
        var delivery_position := Vector2(presentation_position.x * delivery_scale.x, presentation_position.y * delivery_scale.y)
        records.append({
            "source_game_frame_index": index,
            "source_position": _vector2_value(source_position),
            "presentation_canvas_position": _vector2_value(presentation_position),
            "delivery_position": _vector2_value(delivery_position),
            "rotation_radians_preserved": float(frame.rotation),
            "local_scale_multiplier_preserved": _vector2_value(frame.scale),
            "opacity_preserved": float(frame.opacity),
            "texture_index_preserved": int(frame.texture_index),
            "variant_id_preserved": int(frame.variant_id)
        })
    return records

func _source_frame_records(sim: Variant) -> Array[Dictionary]:
    var records: Array[Dictionary] = []
    for index: int in range(sim.frames.size()):
        var frame: Variant = sim.frames[index]
        if frame == null or not frame.is_valid_snapshot():
            return []
        records.append({
            "source_game_frame_index": index,
            "position": _vector2_value(frame.position),
            "rotation_radians": float(frame.rotation),
            "scale": _vector2_value(frame.scale),
            "opacity": float(frame.opacity),
            "texture_index": int(frame.texture_index),
            "variant_id": int(frame.variant_id)
        })
    return records

func _verify_sources() -> bool:
    for rel_path: String in SourcePins.keys():
        var bytes: PackedByteArray = FileAccess.get_file_as_bytes("res://" + rel_path)
        if bytes.is_empty() or _sha256_bytes(bytes) != str(SourcePins[rel_path]):
            _fail("Pinned source hash mismatch: %s" % rel_path)
            return false
    return true

func _contract_guard(value: Variant) -> bool:
    if not (value is Dictionary): return false
    var contract: Dictionary = value
    if str(contract.get("schema", "")) != ContractId or str(contract.get("status", "")) != "PROPOSED_NOT_APPROVED_NOT_FROZEN": return false
    if str(contract.get("authority", {}).get("frozen_c11c_manifest_sha256", "")) != FrozenManifestSha or str(contract.get("authority", {}).get("challenge_source_sha256", "")) != ChallengeSha: return false
    var pins_value: Variant = contract.get("source_pins", [])
    if not (pins_value is Array) or pins_value.size() != SourcePins.size(): return false
    var pin_map: Dictionary = {}
    for item: Variant in pins_value:
        if not (item is Dictionary): return false
        var pin: Dictionary = item
        pin_map[str(pin.get("path", ""))] = str(pin.get("sha256", ""))
    if pin_map != SourcePins: return false
    var locks: Dictionary = contract.get("governance_locks", {})
    if locks.get("c11c_source_mutation") != false or locks.get("policy_approved") != false or locks.get("renderer_input_emitted") != false or locks.get("renderer_activation") != false or locks.get("media_created") != false or str(locks.get("d4_8", "")) != "BLOCKED" or str(locks.get("release_authority", "")) != "NONE": return false
    var schema_bytes: PackedByteArray = FileAccess.get_file_as_bytes(SchemaPath)
    if schema_bytes.is_empty(): return false
    var schema_value: Variant = JSON.parse_string(schema_bytes.get_string_from_utf8())
    return schema_value is Dictionary and str(schema_value.get("$id", "")) == "urn:c11d:renderer-challenge-coordinate-projection-preview:v1"

func _validate_report(report: Dictionary) -> bool:
    if str(report.get("schema", "")) != ReportId or str(report.get("status", "")) != "IN_MEMORY_REVIEW_ONLY_PROJECTION_PREVIEW_NOT_RENDERER_INPUT": return false
    if int(report.get("source_timeline", {}).get("game_frame_count", 0)) != 420 or int(report.get("projected_frames", {}).get("projected_records", 0)) != 420: return false
    if str(report.get("projection", {}).get("state", "")) != "PROPOSED_NOT_APPROVED" or str(report.get("projection", {}).get("sampling_or_interpolation", "")) != "UNRESOLVED_NOT_APPLIED": return false
    if report.get("execution_boundary", {}).get("projected_payload_written") != false or report.get("execution_boundary", {}).get("renderer_native_input_emitted") != false or report.get("execution_boundary", {}).get("media_created") != false: return false
    return true

func _frame_signature_sha256(sim: Variant) -> String:
    var parts := PackedStringArray()
    for index: int in range(sim.frames.size()):
        var frame: Variant = sim.frames[index]
        if frame == null or not frame.is_valid_snapshot(): return ""
        parts.append("%d|%.9f|%.9f|%.9f|%.9f|%.9f|%.9f|%.9f|%d|%d|%s" % [index, frame.position.x, frame.position.y, frame.rotation, frame.scale.x, frame.scale.y, frame.opacity, float(frame.texture_index), int(frame.variant_id), int(frame.custom_data.size()), JSON.stringify(_stable_value(frame.custom_data))])
    return _sha256_text("\n".join(parts))

func _vector2_value(value: Vector2) -> Dictionary:
    return {"x": value.x, "y": value.y}

func _vector2_array(value: Vector2) -> Array[float]:
    var output: Array[float] = []
    output.append(value.x)
    output.append(value.y)
    return output

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

func _near(left: float, right: float, tolerance: float = 0.000001) -> bool:
    return is_finite(left) and is_finite(right) and absf(left - right) <= tolerance

func _fail(message: String) -> void:
    printerr("C11-D RENDERER CHALLENGE COORDINATE PROJECTION PREVIEW FAIL | %s" % message)
    quit(1)
