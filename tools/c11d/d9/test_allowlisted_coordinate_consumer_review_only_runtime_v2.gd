extends SceneTree

## Actual runtime test harness for isolated C11-D V2-B logical consumer revision 2.
## Runs headlessly and does not create a scene, Node, texture, image, or media.

const ConsumerScript = preload("res://tools/c11d/d9/allowlisted_coordinate_consumer_review_only_v2.gd")
const SimulationResultScript = preload("res://core/simulation/SimulationResult.gd")
const FrameSnapshotScript = preload("res://core/data/FrameSnapshot.gd")

const CANDIDATES: Array = ["CHALLENGE_003", "CHALLENGE_005", "CHALLENGE_006", "CHALLENGE_007"]
const VECTOR_CANDIDATES: Array = ["CHALLENGE_005", "CHALLENGE_006", "CHALLENGE_007"]
const ROOT_KEYS: Array = ["contract_id", "candidate_id", "logical_canvas_id", "source_frame_count", "frames"]
const FRAME_KEYS: Array = ["source_frame_index", "target_marker"]
const MARKER_KEYS: Array = ["role", "asset_path", "anchor_x", "anchor_y", "logical_width", "logical_height", "anchor_mode", "asset_bounds_policy"]
const EMPTY_SHA: String = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

var _consumer: RefCounted
var _failures: Array[String] = []
var _case_total: int = 0
var _negative_count: int = 0
var _positive_count: int = 0
var _pair_negative_count: int = 0
var _pair_positive_count: int = 0
var _closed_output_count: int = 0

func _initialize() -> void:
    call_deferred("_run")

func _run() -> void:
    _consumer = ConsumerScript.new()
    _run_positive_contract_cases()
    _run_candidate_field_relations()
    _run_closed_output_cases()
    _run_wrong_field_negative_cases()
    _run_unsupported_candidate_cases()
    _run_missing_field_cases()
    _run_invalid_scalar_cases()
    _run_invalid_vector_cases()
    _run_invalid_upstream_cases()
    _run_empty_frame_cases()
    _run_atomicity_cases()
    _run_constant_position_cases()
    _run_malformed_provenance_cases()

    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_POSITIVE_RUNTIME_CASES=%d/36" % _positive_count)
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_NEGATIVE_RUNTIME_CASES=%d/241" % _negative_count)
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_NEGATIVE_PAIR_CASES=%d/6" % _pair_negative_count)
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_POSITIVE_SHARED_FIELD_RELATIONS=%d/6" % _pair_positive_count)
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_CLOSED_OUTPUT_MUTATIONS=%d/20" % _closed_output_count)
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_RUNTIME_CASES=%d/277" % _case_total)
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_CUSTOM_DATA_LOOKUPS_PER_FRAME=1")
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_CUSTOM_DATA_ENUMERATION=FORBIDDEN")
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_RUNTIME_IMPLEMENTATION=ISOLATED_REVIEW_ONLY")
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_RUNTIME_IMPLEMENTATION_REVISION=V2_SAFE_SENTINEL_TYPE_GUARD")
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_PRODUCTION_CALLS=0")
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_RENDERER=OFF")
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_RENDER_TEST_AUTHORIZATION=NOT_GRANTED")
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_MEDIA_CREATED=false")
    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_C11C_IMMUTABLE=true")

    if not _failures.is_empty() or _case_total != 277 or _negative_count != 241 or _positive_count != 36 or _pair_negative_count != 6 or _pair_positive_count != 6 or _closed_output_count != 20:
        for failure: String in _failures:
            printerr("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_CASE_FAILURE=" + failure)
        printerr("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_RUNTIME_TEST_STATUS=FAIL")
        quit(1)
        return

    print("C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_RUNTIME_TEST_STATUS=PASS")
    quit(0)

func _record(case_id: String, passed: bool) -> void:
    _case_total += 1
    if not passed:
        _failures.append(case_id)

func _positive(case_id: String, passed: bool) -> void:
    _positive_count += 1
    _record(case_id, passed)

func _negative(case_id: String, candidate_id: Variant, sim_result: Variant, validation: Variant, expected_code: String) -> void:
    _negative_count += 1
    var output: Dictionary = _consumer.project_allowlisted_target_marker_track(candidate_id, sim_result, validation)
    var passed: bool = output.size() == 2 and output.get("ok", null) == false and output.get("error_code", "") == expected_code and not output.has("frames")
    _record(case_id, passed)

func _new_result(candidate_id: Variant, values: Array, missing_positions: Array = [], extras: Dictionary = {}, foreign_field: String = "") -> Variant:
    var simulation_result: Variant = SimulationResultScript.new()
    simulation_result.frames.clear()
    simulation_result.winning_frame = -1
    simulation_result.score = 0.0
    var allowed_field: String = ConsumerScript.expected_field_for_candidate(candidate_id)

    for frame_index in range(values.size()):
        var frame: Variant = FrameSnapshotScript.new()
        if not missing_positions.has(frame_index) and not allowed_field.is_empty():
            frame.custom_data[allowed_field] = values[frame_index]
        elif missing_positions.has(frame_index) and not foreign_field.is_empty():
            frame.custom_data[foreign_field] = values[frame_index]

        for extra_key: Variant in extras.keys():
            frame.custom_data[extra_key] = extras[extra_key]
        simulation_result.frames.append(frame)

    return simulation_result

func _bind_validation(simulation_result: Variant, expected_count: int) -> Dictionary:
    var validation: Dictionary = simulation_result.validate_contract(expected_count)
    # SimulationResult.validate_contract() currently returns no result identity.
    # The review-only caller attaches a WeakRef proof to that same dictionary.
    validation["_c11d_v2b_source_result_ref"] = weakref(simulation_result)
    validation["_c11d_v2b_expected_game_frames"] = expected_count
    return validation

func _successful_shape(output: Dictionary, candidate_id: String, expected_count: int) -> bool:
    if output.size() != ROOT_KEYS.size():
        return false
    for key: String in ROOT_KEYS:
        if not output.has(key):
            return false
    if output.get("contract_id", "") != "C11D_V2B_ALLOWLISTED_COORDINATE_CONSUMER_CONTRACT_V1":
        return false
    if output.get("candidate_id", "") != candidate_id or output.get("logical_canvas_id", "") != "LOGICAL_SOCIAL_CANVAS_540X960":
        return false
    var frames_value: Variant = output.get("frames", null)
    if not (frames_value is Array) or frames_value.size() != expected_count or int(output.get("source_frame_count", -1)) != expected_count:
        return false

    for frame_index in range(frames_value.size()):
        var frame_value: Variant = frames_value[frame_index]
        if not (frame_value is Dictionary) or frame_value.size() != FRAME_KEYS.size():
            return false
        for frame_key: String in FRAME_KEYS:
            if not frame_value.has(frame_key):
                return false
        if typeof(frame_value.get("source_frame_index", null)) != TYPE_INT or int(frame_value.get("source_frame_index", -1)) != frame_index:
            return false
        var marker_value: Variant = frame_value.get("target_marker", null)
        if not (marker_value is Dictionary) or marker_value.size() != MARKER_KEYS.size():
            return false
        for marker_key: String in MARKER_KEYS:
            if not marker_value.has(marker_key):
                return false
        if marker_value.get("role", "") != "TARGET" or marker_value.get("logical_width", -1.0) != 50.0 or marker_value.get("logical_height", -1.0) != 50.0:
            return false
        if marker_value.get("anchor_mode", "") != "CENTER" or marker_value.get("asset_bounds_policy", "") != "CLIP_BOUNDS_WITHOUT_MOVING_POINT":
            return false
        if marker_value.get("asset_path", "") != ("assets/c6/waypoint.svg" if candidate_id == "CHALLENGE_003" else "assets/c6/target.svg"):
            return false
    return not _contains_object_reference(output)

func _contains_object_reference(value: Variant) -> bool:
    if typeof(value) == TYPE_OBJECT:
        return true
    if value is Dictionary:
        for key: Variant in value.keys():
            if _contains_object_reference(key) or _contains_object_reference(value[key]):
                return true
    elif value is Array:
        for item: Variant in value:
            if _contains_object_reference(item):
                return true
    return false

func _run_positive_contract_cases() -> void:
    # 1: CHALLENGE_003 includes both inclusive scalar endpoints and center.
    var scalar_result: Variant = _new_result("CHALLENGE_003", [0.0, 50.0, 100.0])
    var scalar_output: Dictionary = _consumer.project_allowlisted_target_marker_track("CHALLENGE_003", scalar_result, _bind_validation(scalar_result, 3))
    var scalar_frames: Array = scalar_output.get("frames", [])
    var scalar_ok: bool = _successful_shape(scalar_output, "CHALLENGE_003", 3)
    if scalar_ok:
        scalar_ok = is_equal_approx(float(scalar_frames[0]["target_marker"]["anchor_x"]), 0.0) and is_equal_approx(float(scalar_frames[1]["target_marker"]["anchor_x"]), 270.0) and is_equal_approx(float(scalar_frames[2]["target_marker"]["anchor_x"]), 540.0)
        scalar_ok = scalar_ok and is_equal_approx(float(scalar_frames[0]["target_marker"]["anchor_y"]), 480.0) and is_equal_approx(float(scalar_frames[1]["target_marker"]["anchor_y"]), 480.0) and is_equal_approx(float(scalar_frames[2]["target_marker"]["anchor_y"]), 480.0)
    _positive("positive_challenge_003_scalar_endpoints_center", scalar_ok)

    # 2: CHALLENGE_005 is run-constant and retains the inclusive lower corner.
    var constant_result: Variant = _new_result("CHALLENGE_005", [Vector2(0.0, 0.0), Vector2(0.0, 0.0), Vector2(0.0, 0.0)])
    var constant_output: Dictionary = _consumer.project_allowlisted_target_marker_track("CHALLENGE_005", constant_result, _bind_validation(constant_result, 3))
    var constant_frames: Array = constant_output.get("frames", [])
    var constant_ok: bool = _successful_shape(constant_output, "CHALLENGE_005", 3)
    if constant_ok:
        constant_ok = is_equal_approx(float(constant_frames[0]["target_marker"]["anchor_x"]), 0.0) and is_equal_approx(float(constant_frames[0]["target_marker"]["anchor_y"]), 0.0)
        for frame_index in range(1, constant_frames.size()):
            constant_ok = constant_ok and constant_frames[frame_index]["target_marker"]["anchor_x"] == constant_frames[0]["target_marker"]["anchor_x"] and constant_frames[frame_index]["target_marker"]["anchor_y"] == constant_frames[0]["target_marker"]["anchor_y"]
    _positive("positive_challenge_005_constant_lower_corner", constant_ok)

    # 3: CHALLENGE_006 accepts a dynamic vector track and maps corners/center.
    var vector_006: Array = [Vector2(0.0, 0.0), Vector2(540.0, 960.0), Vector2(1080.0, 1920.0)]
    var result_006: Variant = _new_result("CHALLENGE_006", vector_006)
    var output_006: Dictionary = _consumer.project_allowlisted_target_marker_track("CHALLENGE_006", result_006, _bind_validation(result_006, 3))
    var frames_006: Array = output_006.get("frames", [])
    var ok_006: bool = _successful_shape(output_006, "CHALLENGE_006", 3)
    if ok_006:
        ok_006 = is_equal_approx(float(frames_006[0]["target_marker"]["anchor_x"]), 0.0) and is_equal_approx(float(frames_006[0]["target_marker"]["anchor_y"]), 0.0)
        ok_006 = ok_006 and is_equal_approx(float(frames_006[1]["target_marker"]["anchor_x"]), 270.0) and is_equal_approx(float(frames_006[1]["target_marker"]["anchor_y"]), 480.0)
        ok_006 = ok_006 and is_equal_approx(float(frames_006[2]["target_marker"]["anchor_x"]), 540.0) and is_equal_approx(float(frames_006[2]["target_marker"]["anchor_y"]), 960.0)
    _positive("positive_challenge_006_dynamic_vector_corners_center", ok_006)

    # 4: CHALLENGE_007 accepts dynamic vectors and keeps source order.
    var values_007: Array = [Vector2(100.0, 200.0), Vector2(300.0, 400.0), Vector2(500.0, 1000.0)]
    var result_007: Variant = _new_result("CHALLENGE_007", values_007)
    var output_007: Dictionary = _consumer.project_allowlisted_target_marker_track("CHALLENGE_007", result_007, _bind_validation(result_007, 3))
    var frames_007: Array = output_007.get("frames", [])
    var ok_007: bool = _successful_shape(output_007, "CHALLENGE_007", 3)
    if ok_007:
        ok_007 = is_equal_approx(float(frames_007[0]["target_marker"]["anchor_x"]), 50.0) and is_equal_approx(float(frames_007[0]["target_marker"]["anchor_y"]), 100.0)
        ok_007 = ok_007 and is_equal_approx(float(frames_007[1]["target_marker"]["anchor_x"]), 150.0) and is_equal_approx(float(frames_007[1]["target_marker"]["anchor_y"]), 200.0)
        ok_007 = ok_007 and is_equal_approx(float(frames_007[2]["target_marker"]["anchor_x"]), 250.0) and is_equal_approx(float(frames_007[2]["target_marker"]["anchor_y"]), 500.0)
    _positive("positive_challenge_007_dynamic_vector_and_order", ok_007)

    # 5: all four declared candidate-field pairs produce the exact closed shape.
    var all_candidates_ok: bool = true
    for candidate_id: String in CANDIDATES:
        var sample_values: Array = [50.0, 50.0] if candidate_id == "CHALLENGE_003" else [Vector2(100.0, 200.0), Vector2(100.0, 200.0)]
        var sim: Variant = _new_result(candidate_id, sample_values)
        var output: Dictionary = _consumer.project_allowlisted_target_marker_track(candidate_id, sim, _bind_validation(sim, 2))
        all_candidates_ok = all_candidates_ok and _successful_shape(output, candidate_id, 2)
    _positive("positive_all_four_exact_candidate_field_pairs", all_candidates_ok)

    # 6: target asset contract is static and no raster/resource operation is involved.
    var consumer_asset_ok: bool = ConsumerScript.ASSET_INTRINSIC_SIZE == Vector2(100.0, 100.0) and ConsumerScript.LOGICAL_ASSET_SIZE == Vector2(50.0, 50.0)
    consumer_asset_ok = consumer_asset_ok and ConsumerScript.ASSET_FOR_CANDIDATE["CHALLENGE_003"] == "assets/c6/waypoint.svg" and ConsumerScript.ASSET_FOR_CANDIDATE["CHALLENGE_006"] == "assets/c6/target.svg"
    _positive("positive_static_asset_contract", consumer_asset_ok)

    # 7: exact logical frame ordinal is emitted, not snapshot metadata.
    var order_result: Variant = _new_result("CHALLENGE_006", [Vector2(100.0, 100.0), Vector2(200.0, 200.0), Vector2(300.0, 300.0), Vector2(400.0, 400.0)])
    order_result.winning_frame = 2
    var order_output: Dictionary = _consumer.project_allowlisted_target_marker_track("CHALLENGE_006", order_result, _bind_validation(order_result, 4))
    var order_frames: Array = order_output.get("frames", [])
    var order_ok: bool = _successful_shape(order_output, "CHALLENGE_006", 4)
    if order_ok:
        for frame_index in range(4):
            order_ok = order_ok and int(order_frames[frame_index]["source_frame_index"]) == frame_index
    _positive("positive_source_array_ordinals_and_cardinality", order_ok)

    # 8: output contains neither input custom_data nor simulation metrics.
    var leak_result: Variant = _new_result("CHALLENGE_006", [Vector2(123.0, 456.0)])
    leak_result.score = 0.77
    leak_result.metadata["private_note"] = "DO_NOT_LEAK"
    var leak_validation: Dictionary = _bind_validation(leak_result, 1)
    var leak_output: Dictionary = _consumer.project_allowlisted_target_marker_track("CHALLENGE_006", leak_result, leak_validation)
    var leak_ok: bool = _successful_shape(leak_output, "CHALLENGE_006", 1) and not leak_output.has("score") and not leak_output.has("metadata") and not leak_output.has("custom_data")
    _positive("positive_no_source_data_leakage", leak_ok)

    # 9: projection has no rounding/clamping at a non-integer half coordinate.
    var precise_result: Variant = _new_result("CHALLENGE_007", [Vector2(1.0, 3.0)])
    var precise_output: Dictionary = _consumer.project_allowlisted_target_marker_track("CHALLENGE_007", precise_result, _bind_validation(precise_result, 1))
    var precise_frames: Array = precise_output.get("frames", [])
    var precise_ok: bool = _successful_shape(precise_output, "CHALLENGE_007", 1)
    if precise_ok:
        precise_ok = float(precise_frames[0]["target_marker"]["anchor_x"]) == 0.5 and float(precise_frames[0]["target_marker"]["anchor_y"]) == 1.5
    _positive("positive_no_rounding_or_clamping", precise_ok)

    # 10: non-winning frames remain in track; winning_frame is not a selector.
    var winner_result: Variant = _new_result("CHALLENGE_006", [Vector2(100.0, 100.0), Vector2(200.0, 200.0), Vector2(300.0, 300.0)])
    winner_result.winning_frame = 1
    var winner_output: Dictionary = _consumer.project_allowlisted_target_marker_track("CHALLENGE_006", winner_result, _bind_validation(winner_result, 3))
    var winner_frames: Array = winner_output.get("frames", [])
    var winner_ok: bool = _successful_shape(winner_output, "CHALLENGE_006", 3) and winner_frames.size() == 3
    _positive("positive_winning_frame_does_not_filter_track", winner_ok)

func _run_candidate_field_relations() -> void:
    # Three vector IDs intentionally share target_position. Those cross-owner
    # relations are valid, not mismatches; the V1 design's 12-negative count
    # overcounted them because it treated shared field names as distinct fields.
    for candidate_id: String in VECTOR_CANDIDATES:
        for source_owner: String in VECTOR_CANDIDATES:
            if source_owner == candidate_id:
                continue
            var result_code: String = ConsumerScript._candidate_field_pair_failure(candidate_id, ConsumerScript.expected_field_for_candidate(source_owner))
            _pair_positive_count += 1
            _positive("shared_field_relation_%s_%s" % [candidate_id, source_owner], result_code.is_empty())

func _run_wrong_field_negative_cases() -> void:
    # Six ordered cross-family relations really mismatch the string field name.
    for candidate_id: String in CANDIDATES:
        for source_owner: String in CANDIDATES:
            if source_owner == candidate_id:
                continue
            var foreign_field: String = ConsumerScript.expected_field_for_candidate(source_owner)
            if foreign_field == ConsumerScript.expected_field_for_candidate(candidate_id):
                continue
            var result_code: String = ConsumerScript._candidate_field_pair_failure(candidate_id, foreign_field)
            _pair_negative_count += 1
            _record_pair_negative("wrong_field_pair_%s_from_%s" % [candidate_id, source_owner], result_code == "ALLOWLIST_MISMATCH")

func _record_pair_negative(case_id: String, passed: bool) -> void:
    _negative_count += 1
    _record(case_id, passed)

func _run_unsupported_candidate_cases() -> void:
    var unsupported_ids: Array = ["CHALLENGE_001", "CHALLENGE_002", "CHALLENGE_004", "CHALLENGE_008", "CHALLENGE_009", "UNKNOWN", ""]
    for candidate_id: String in unsupported_ids:
        _negative("unsupported_candidate_%s" % candidate_id, candidate_id, null, null, "UNSUPPORTED_CANDIDATE")

func _run_missing_field_cases() -> void:
    for candidate_id: String in CANDIDATES:
        var values: Array = [50.0, 50.0, 50.0] if candidate_id == "CHALLENGE_003" else [Vector2(100.0, 200.0), Vector2(100.0, 200.0), Vector2(100.0, 200.0)]
        var foreign_field: String = "target_position" if candidate_id == "CHALLENGE_003" else "target_x"
        for bad_index in range(3):
            var sim: Variant = _new_result(candidate_id, values, [bad_index], {}, foreign_field)
            _negative("missing_allowlisted_field_%s_%d" % [candidate_id, bad_index], candidate_id, sim, _bind_validation(sim, 3), "MISSING_ALLOWLISTED_FIELD")

func _run_invalid_scalar_cases() -> void:
    var variants: Array = [
        {"name": "null", "value": null, "code": "INVALID_VALUE_TYPE"},
        {"name": "true", "value": true, "code": "INVALID_VALUE_TYPE"},
        {"name": "false", "value": false, "code": "INVALID_VALUE_TYPE"},
        {"name": "string", "value": "50", "code": "INVALID_VALUE_TYPE"},
        {"name": "object_dictionary", "value": {"x": 50.0}, "code": "INVALID_VALUE_TYPE"},
        {"name": "array", "value": [50.0], "code": "INVALID_VALUE_TYPE"},
        {"name": "nan", "value": NAN, "code": "NONFINITE_VALUE"},
        {"name": "positive_infinity", "value": INF, "code": "NONFINITE_VALUE"},
        {"name": "negative_infinity", "value": -INF, "code": "NONFINITE_VALUE"},
        {"name": "below_minimum", "value": -0.001, "code": "VALUE_OUT_OF_DOMAIN"},
        {"name": "above_maximum", "value": 100.001, "code": "VALUE_OUT_OF_DOMAIN"},
    ]
    # Exactly eleven invalid scalar classes x first/middle/last frame.
    for variant: Dictionary in variants:
        for bad_index in range(3):
            var values: Array = [50.0, 50.0, 50.0]
            values[bad_index] = variant["value"]
            var sim: Variant = _new_result("CHALLENGE_003", values)
            _negative("invalid_scalar_%s_at_%d" % [variant["name"], bad_index], "CHALLENGE_003", sim, _bind_validation(sim, 3), str(variant["code"]))

func _run_invalid_vector_cases() -> void:
    var variants: Array = [
        {"name": "null", "value": null, "code": "INVALID_VALUE_TYPE"},
        {"name": "true", "value": true, "code": "INVALID_VALUE_TYPE"},
        {"name": "false", "value": false, "code": "INVALID_VALUE_TYPE"},
        {"name": "string", "value": "1,2", "code": "INVALID_VALUE_TYPE"},
        {"name": "dictionary", "value": {"x": 1.0, "y": 2.0}, "code": "INVALID_VALUE_TYPE"},
        {"name": "array", "value": [1.0, 2.0], "code": "INVALID_VALUE_TYPE"},
        {"name": "wrong_dimension_zero", "value": PackedFloat32Array(), "code": "INVALID_VALUE_TYPE"},
        {"name": "wrong_dimension_one", "value": PackedFloat32Array([1.0]), "code": "INVALID_VALUE_TYPE"},
        {"name": "wrong_dimension_three", "value": Vector3(1.0, 2.0, 3.0), "code": "INVALID_VALUE_TYPE"},
        {"name": "nan_x", "value": Vector2(NAN, 1.0), "code": "NONFINITE_VALUE"},
        {"name": "positive_infinity_y", "value": Vector2(1.0, INF), "code": "NONFINITE_VALUE"},
        {"name": "negative_infinity_x", "value": Vector2(-INF, 1.0), "code": "NONFINITE_VALUE"},
        {"name": "below_x_min", "value": Vector2(-0.001, 1.0), "code": "VECTOR_OUT_OF_BOUNDS"},
        {"name": "above_x_max", "value": Vector2(1080.001, 1.0), "code": "VECTOR_OUT_OF_BOUNDS"},
        {"name": "below_y_min", "value": Vector2(1.0, -0.001), "code": "VECTOR_OUT_OF_BOUNDS"},
        {"name": "above_y_max", "value": Vector2(1.0, 1920.001), "code": "VECTOR_OUT_OF_BOUNDS"},
        # A Vector2 cannot encode bool components. The dictionary below is the
        # closest representable malicious x/y pair and must fail the strict type gate.
        {"name": "boolean_component_surrogate", "value": {"x": true, "y": 0.0}, "code": "INVALID_VALUE_TYPE"},
    ]

    for candidate_id: String in VECTOR_CANDIDATES:
        for variant: Dictionary in variants:
            for bad_index in range(3):
                var values: Array = [Vector2(100.0, 200.0), Vector2(100.0, 200.0), Vector2(100.0, 200.0)]
                values[bad_index] = variant["value"]
                var sim: Variant = _new_result(candidate_id, values)
                _negative("invalid_vector_%s_%s_at_%d" % [candidate_id, variant["name"], bad_index], candidate_id, sim, _bind_validation(sim, 3), str(variant["code"]))

func _run_invalid_upstream_cases() -> void:
    var sim: Variant = _new_result("CHALLENGE_006", [Vector2(10.0, 20.0)])
    _negative("upstream_missing_dictionary", "CHALLENGE_006", sim, {}, "SNAPSHOT_CONTRACT_NOT_VALID")
    _negative("upstream_null", "CHALLENGE_006", sim, null, "SNAPSHOT_CONTRACT_NOT_VALID")
    _negative("upstream_non_dictionary", "CHALLENGE_006", sim, "not-a-dictionary", "SNAPSHOT_CONTRACT_NOT_VALID")

    var invalid_flag: Dictionary = _bind_validation(sim, 1)
    invalid_flag["is_valid"] = false
    _negative("upstream_is_valid_false", "CHALLENGE_006", sim, invalid_flag, "SNAPSHOT_CONTRACT_NOT_VALID")

    var invalid_code: Dictionary = _bind_validation(sim, 1)
    invalid_code["error_code"] = "NOT_OK"
    _negative("upstream_error_code_not_ok", "CHALLENGE_006", sim, invalid_code, "SNAPSHOT_CONTRACT_NOT_VALID")

    var other_sim: Variant = _new_result("CHALLENGE_006", [Vector2(10.0, 20.0)])
    _negative("upstream_proof_for_other_result", "CHALLENGE_006", sim, _bind_validation(other_sim, 1), "SNAPSHOT_CONTRACT_NOT_VALID")

func _run_empty_frame_cases() -> void:
    for candidate_id: String in CANDIDATES:
        var empty_values: Array = []
        var sim: Variant = _new_result(candidate_id, empty_values)
        _negative("empty_frames_%s" % candidate_id, candidate_id, sim, _bind_validation(sim, 0), "EMPTY_SOURCE_FRAMES")

func _run_atomicity_cases() -> void:
    for candidate_id: String in CANDIDATES:
        var valid_value: Variant = 50.0 if candidate_id == "CHALLENGE_003" else Vector2(100.0, 200.0)
        for bad_index in range(3):
            var values: Array = [valid_value, valid_value, valid_value]
            values[bad_index] = "INVALID_ATOMIC_SAMPLE"
            var sim: Variant = _new_result(candidate_id, values)
            _negative("atomic_no_partial_track_%s_%d" % [candidate_id, bad_index], candidate_id, sim, _bind_validation(sim, 3), "INVALID_VALUE_TYPE")

func _run_constant_position_cases() -> void:
    var mismatch_first: Variant = _new_result("CHALLENGE_005", [Vector2(10.0, 20.0), Vector2(11.0, 20.0), Vector2(10.0, 20.0)])
    _negative("constant_mismatch_frame_1", "CHALLENGE_005", mismatch_first, _bind_validation(mismatch_first, 3), "PER_RUN_CONSTANT_MISMATCH")

    var mismatch_last: Variant = _new_result("CHALLENGE_005", [Vector2(10.0, 20.0), Vector2(10.0, 20.0), Vector2(11.0, 20.0)])
    _negative("constant_mismatch_last_frame", "CHALLENGE_005", mismatch_last, _bind_validation(mismatch_last, 3), "PER_RUN_CONSTANT_MISMATCH")

func _run_malformed_provenance_cases() -> void:
    var sim: Variant = _new_result("CHALLENGE_006", [Vector2(10.0, 20.0), Vector2(20.0, 30.0)])

    var missing_ref: Dictionary = sim.validate_contract(2)
    missing_ref["_c11d_v2b_expected_game_frames"] = 2
    _negative("provenance_missing_source_ref", "CHALLENGE_006", sim, missing_ref, "SNAPSHOT_CONTRACT_NOT_VALID")

    var non_weak_ref: Dictionary = _bind_validation(sim, 2)
    non_weak_ref["_c11d_v2b_source_result_ref"] = "not-a-weakref"
    _negative("provenance_non_weak_ref", "CHALLENGE_006", sim, non_weak_ref, "SNAPSHOT_CONTRACT_NOT_VALID")

    var missing_count: Dictionary = _bind_validation(sim, 2)
    missing_count.erase("_c11d_v2b_expected_game_frames")
    _negative("provenance_missing_expected_count", "CHALLENGE_006", sim, missing_count, "SNAPSHOT_CONTRACT_NOT_VALID")

    var string_count: Dictionary = _bind_validation(sim, 2)
    string_count["_c11d_v2b_expected_game_frames"] = "2"
    _negative("provenance_string_expected_count", "CHALLENGE_006", sim, string_count, "SNAPSHOT_CONTRACT_NOT_VALID")

    var bool_count: Dictionary = _bind_validation(sim, 2)
    bool_count["_c11d_v2b_expected_game_frames"] = true
    _negative("provenance_bool_expected_count", "CHALLENGE_006", sim, bool_count, "SNAPSHOT_CONTRACT_NOT_VALID")

    var mismatch_count: Dictionary = _bind_validation(sim, 2)
    mismatch_count["_c11d_v2b_expected_game_frames"] = 3
    _negative("provenance_expected_count_mismatch", "CHALLENGE_006", sim, mismatch_count, "FRAME_CARDINALITY_MISMATCH")

func _run_closed_output_cases() -> void:
    var mutation_names: Array = [
        "extra_root_key", "extra_frame_key", "extra_marker_key", "raw_source_value", "custom_data_reference",
        "custom_data_copy", "score", "close_calls", "winning_frame", "snapshot_position", "rotation", "scale",
        "simulation_result_object", "input_dictionary", "pause_state", "result_state", "frame_object",
        "untrusted_asset_path", "delivery_scaled_coordinates", "clamped_coordinates"
    ]

    for mutation_name: String in mutation_names:
        var sim: Variant = _new_result("CHALLENGE_006", [Vector2(123.0, 456.0), Vector2(234.0, 567.0)])
        var first_frame: Variant = sim.frames[0]
        match mutation_name:
            "extra_root_key":
                sim.metadata["extra_root_key"] = "ROOT_SECRET"
            "extra_frame_key":
                first_frame.custom_data["extra_frame_key"] = "FRAME_SECRET"
            "extra_marker_key":
                first_frame.custom_data["extra_marker_key"] = "MARKER_SECRET"
            "raw_source_value":
                first_frame.custom_data["raw_source_value"] = Vector2(123.0, 456.0)
            "custom_data_reference":
                first_frame.custom_data["custom_data_reference"] = sim.frames[1].custom_data
            "custom_data_copy":
                first_frame.custom_data["custom_data_copy"] = first_frame.custom_data.duplicate()
            "score":
                sim.score = 0.91
            "close_calls":
                first_frame.custom_data["close_calls"] = 17
            "winning_frame":
                sim.winning_frame = 1
            "snapshot_position":
                first_frame.position = Vector2(99999.0, -99999.0)
            "rotation":
                first_frame.rotation = 2.25
            "scale":
                first_frame.scale = Vector2(4.0, 6.0)
            "simulation_result_object":
                first_frame.custom_data["simulation_result_object"] = SimulationResultScript.new()
            "input_dictionary":
                first_frame.custom_data["input_dictionary"] = {"secret": "INPUT_SECRET"}
            "pause_state":
                first_frame.custom_data["pause_state"] = true
            "result_state":
                first_frame.custom_data["result_state"] = "WIN"
            "frame_object":
                first_frame.custom_data["frame_object"] = FrameSnapshotScript.new()
            "untrusted_asset_path":
                first_frame.custom_data["asset_path"] = "../../untrusted.svg"
            "delivery_scaled_coordinates":
                first_frame.custom_data["delivery_scaled_coordinates"] = Vector2(960.0, 1706.6667)
            "clamped_coordinates":
                first_frame.custom_data["clamped_coordinates"] = Vector2(0.0, 0.0)

        var output: Dictionary = _consumer.project_allowlisted_target_marker_track("CHALLENGE_006", sim, _bind_validation(sim, 2))
        _closed_output_count += 1
        _positive("closed_output_mutation_%s" % mutation_name, _successful_shape(output, "CHALLENGE_006", 2))
