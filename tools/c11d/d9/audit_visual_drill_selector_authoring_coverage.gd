extends SceneTree

## D-only, read-only capability audit for all canonical Visual Drill type/tier combinations.
## Tests authoring adapter output in memory only; it is not the dynamic request/payload binder,
## does not emit renderer input, invoke a renderer, run shaders, or create media.

const MANIFEST_SHA := "e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953"
const CONTRACT_PATH := "res://definitions/c11d/production/D_RENDERER_VISUAL_DRILL_SELECTOR_AUTHORING_COVERAGE_V1.json"
const SCHEMA_PATH := "res://definitions/c11d/production/D_RENDERER_VISUAL_DRILL_SELECTOR_AUTHORING_COVERAGE_SCHEMA_V1.json"
const OUTPUT_PREFIX := "C11-D VISUAL DRILL AUTHORING COVERAGE RECEIPT="
const SUMMARY_PREFIX := "C11-D VISUAL DRILL AUTHORING COVERAGE SUMMARY="

const VisualAuthoringGeneratorScript = preload("res://core/authoring/VisualAuthoringGenerator.gd")
const VisualAuthoringRequestScript = preload("res://core/authoring/VisualAuthoringRequest.gd")
const VisualAuthoringAssemblyContextScript = preload("res://core/authoring/VisualAuthoringAssemblyContext.gd")

const EXPECTED_FAMILIES: Array[String] = ["peripheral_scan", "pursuit", "saccade", "tracking"]
const EXPECTED_TIERS: Array[int] = [1, 2, 3, 4, 5]
const BASE_SEED := 12345
const ALTERNATE_SEED := 54321

func _initialize() -> void:
    call_deferred("_run")

func _run() -> void:
    var contract_bytes := FileAccess.get_file_as_bytes(CONTRACT_PATH)
    if contract_bytes.is_empty():
        _fail("Coverage contract is missing.")
        return
    var contract_value: Variant = JSON.parse_string(contract_bytes.get_string_from_utf8())
    if not (contract_value is Dictionary):
        _fail("Coverage contract is not a JSON object.")
        return
    var contract: Dictionary = contract_value
    if str(contract.get("schema", "")) != "C11-D-D9-VISUAL-DRILL-SELECTOR-AUTHORING-COVERAGE-CONTRACT-V1" or str(contract.get("status", "")) != "PREPARATION_ONLY_AUTHORIZING_ADAPTER_CAPABILITY_AUDIT_NOT_DYNAMIC_PAYLOAD_BINDING_OR_RENDERER_INPUT":
        _fail("Coverage contract identity/status mismatch.")
        return
    if str(contract.get("frozen_c11c_manifest_sha256", "")) != MANIFEST_SHA:
        _fail("Frozen C11-C manifest pin mismatch in coverage contract.")
        return
    var matrix: Dictionary = contract.get("selector_matrix", {})
    var family_ids_value: Variant = matrix.get("family_ids", null)
    var tiers_value: Variant = matrix.get("tiers", null)
    var selector_count_value: Variant = matrix.get("expected_selector_count", null)
    if not (family_ids_value is Array) or not (tiers_value is Array):
        _fail("The canonical V1 matrix must provide JSON arrays for family_ids and tiers.")
        return

    # JSON.parse_string returns untyped Variant arrays. Normalize their members explicitly
    # instead of comparing a JSON Array directly to typed constant Arrays.
    var matrix_family_ids: Array[String] = []
    for family_value in family_ids_value:
        matrix_family_ids.append(str(family_value))
    var matrix_tiers: Array[int] = []
    for tier_value in tiers_value:
        if not (tier_value is int or tier_value is float):
            _fail("The canonical V1 matrix contains a non-numeric tier value.")
            return
        var numeric_tier := float(tier_value)
        if not is_finite(numeric_tier) or numeric_tier != float(int(numeric_tier)):
            _fail("The canonical V1 matrix contains a non-integral tier value.")
            return
        matrix_tiers.append(int(numeric_tier))

    if not (selector_count_value is int or selector_count_value is float):
        _fail("The canonical V1 matrix selector count must be numeric.")
        return
    var numeric_selector_count := float(selector_count_value)
    if not is_finite(numeric_selector_count) or numeric_selector_count != 20.0:
        _fail("The canonical V1 matrix must declare exactly 20 selectors.")
        return

    if matrix_family_ids.size() != EXPECTED_FAMILIES.size():
        _fail("The canonical V1 matrix must contain exactly four family IDs.")
        return
    for family_index in range(EXPECTED_FAMILIES.size()):
        if matrix_family_ids[family_index] != EXPECTED_FAMILIES[family_index]:
            _fail("The canonical V1 family ID order/content is invalid at index %d." % family_index)
            return
    if matrix_tiers.size() != EXPECTED_TIERS.size():
        _fail("The canonical V1 matrix must contain exactly five tiers.")
        return
    for tier_index in range(EXPECTED_TIERS.size()):
        if matrix_tiers[tier_index] != EXPECTED_TIERS[tier_index]:
            _fail("The canonical V1 tier order/content is invalid at index %d." % tier_index)
            return
    var pins_value: Variant = contract.get("source_lineage", null)
    if not (pins_value is Array) or pins_value.is_empty():
        _fail("Coverage source-lineage pins are missing.")
        return
    var pins: Array = pins_value
    if str(pins[0].get("path", "")) != "release/C11C_FREEZE_PACKAGE_MANIFEST.json" or str(pins[0].get("sha256", "")) != MANIFEST_SHA:
        _fail("Frozen C11-C manifest must be the first exact source pin.")
        return
    var previous := ""
    for index in range(pins.size()):
        var pin: Dictionary = pins[index]
        var rel := str(pin.get("path", ""))
        var expected := str(pin.get("sha256", ""))
        if rel.is_empty() or rel.begins_with("/") or rel.contains("\\") or rel.split("/").has("..") or not _is_sha256(expected):
            _fail("Unsafe or malformed coverage source pin: %s" % rel)
            return
        if index > 1 and rel <= previous:
            _fail("Coverage source pins must be sorted and unique after the frozen manifest.")
            return
        previous = rel
        var source_bytes := FileAccess.get_file_as_bytes("res://" + rel)
        if source_bytes.is_empty() or _sha256_bytes(source_bytes) != expected:
            _fail("Pinned authoring/catalog source drift: %s" % rel)
            return
    var manifest_bytes := FileAccess.get_file_as_bytes("res://release/C11C_FREEZE_PACKAGE_MANIFEST.json")
    if manifest_bytes.is_empty() or _sha256_bytes(manifest_bytes) != MANIFEST_SHA:
        _fail("Frozen C11-C manifest file differs from its canonical SHA-256.")
        return
    var source_lineage_sha := _sha256(pins)
    var receipts: Array[Dictionary] = []
    var unique_selectors := {}
    var deterministic_count := 0
    var seed_change_count := 0
    var identity_count := 0
    var policy_count := 0
    for family in EXPECTED_FAMILIES:
        var canonical_path := "definitions/visual_drill_%s_canonical.json" % family
        var policy_path := "profiles/difficulty/visual_drill_%s.json" % family
        var canonical_bytes := FileAccess.get_file_as_bytes("res://" + canonical_path)
        var policy_bytes := FileAccess.get_file_as_bytes("res://" + policy_path)
        if canonical_bytes.is_empty() or policy_bytes.is_empty():
            _fail("Canonical drill source or difficulty policy is missing for %s." % family)
            return
        var canonical_value: Variant = JSON.parse_string(canonical_bytes.get_string_from_utf8())
        var policy_value: Variant = JSON.parse_string(policy_bytes.get_string_from_utf8())
        if not (canonical_value is Dictionary) or not (policy_value is Dictionary):
            _fail("Canonical drill source or difficulty policy is malformed for %s." % family)
            return
        var canonical: Dictionary = canonical_value
        var policy: Dictionary = policy_value
        if str(canonical.get("subtype", "")) != family or str(policy.get("subtype", "")) != family:
            _fail("Canonical type/profile identity differs for %s." % family)
            return
        var base_payload_value: Variant = canonical.get("payload", null)
        if not (base_payload_value is Dictionary):
            _fail("Canonical payload object is missing for %s." % family)
            return
        var canonical_payload: Dictionary = base_payload_value
        var duration := float(canonical_payload.get("duration", -1.0))
        var fps := int(canonical_payload.get("fps", -1))
        var frame_count := int(canonical_payload.get("frame_count", -1))
        if duration <= 0.0 or fps != 30 or frame_count != int(round(duration * float(fps))):
            _fail("Canonical duration/fps/frame_count relation is invalid for %s." % family)
            return
        var policy_tiers_value: Variant = policy.get("tiers", null)
        if not (policy_tiers_value is Dictionary):
            _fail("Canonical type has no tier policy table: %s." % family)
            return
        var policy_tiers: Dictionary = policy_tiers_value
        if not policy_tiers.has("2"):
            _fail("Canonical type has no tier-2 policy entry: %s." % family)
            return
        for tier in EXPECTED_TIERS:
            var selector_key := "%s/tier-%d" % [family, tier]
            if unique_selectors.has(selector_key):
                _fail("Duplicate canonical Visual Drill selector: %s" % selector_key)
                return
            unique_selectors[selector_key] = true
            var request: VisualAuthoringRequest = VisualAuthoringRequestScript.new("visual_drill", family, duration, fps, tier, {})
            var context_a: VisualAuthoringAssemblyContext = _make_context(BASE_SEED, family)
            var context_b: VisualAuthoringAssemblyContext = _make_context(BASE_SEED, family)
            var context_c: VisualAuthoringAssemblyContext = _make_context(ALTERNATE_SEED, family)
            var result_a: Dictionary = VisualAuthoringGeneratorScript.generate(request, context_a, {})
            var result_b: Dictionary = VisualAuthoringGeneratorScript.generate(request, context_b, {})
            var result_c: Dictionary = VisualAuthoringGeneratorScript.generate(request, context_c, {})
            if not bool(result_a.get("success", false)) or not bool(result_b.get("success", false)) or not bool(result_c.get("success", false)):
                _fail("Authoring adapter failed for %s: tier-%d. A=%s B=%s C=%s" % [family, tier, str(result_a.get("errors", [])), str(result_b.get("errors", [])), str(result_c.get("errors", []))])
                return
            var envelope_a: Dictionary = result_a.get("content", {})
            var envelope_b: Dictionary = result_b.get("content", {})
            var envelope_c: Dictionary = result_c.get("content", {})
            var payload_a: Dictionary = envelope_a.get("payload", {})
            var payload_b: Dictionary = envelope_b.get("payload", {})
            var payload_c: Dictionary = envelope_c.get("payload", {})
            var task_a: Dictionary = payload_a.get("task", {})
            var exercise: Dictionary = payload_a.get("exercise_parameters", {})
            var trajectory_a: Dictionary = payload_a.get("trajectory", {})
            var trajectory_b: Dictionary = payload_b.get("trajectory", {})
            var trajectory_c: Dictionary = payload_c.get("trajectory", {})
            var motion_a: Dictionary = payload_a.get("seed_motion", {})
            var motion_b: Dictionary = payload_b.get("seed_motion", {})
            var motion_c: Dictionary = payload_c.get("seed_motion", {})
            if str(envelope_a.get("kind", "")) != "visual_drill" or str(envelope_a.get("subtype", "")) != family or str(exercise.get("generator", "")) != family or int(exercise.get("difficulty_tier", -1)) != tier:
                _fail("Authoring output identity/tier mismatch for %s tier-%d." % [family, tier])
                return
            if int(payload_a.get("fps", -1)) != fps or int(payload_a.get("frame_count", -1)) != frame_count or float(payload_a.get("duration", -1.0)) != duration:
                _fail("Authoring output canonical timing differs for %s tier-%d." % [family, tier])
                return
            if motion_a.is_empty() or motion_b.is_empty() or motion_c.is_empty():
                _fail("Seed-driven visual authoring evidence is absent for %s tier-%d." % [family, tier])
                return
            if int(motion_a.get("seed", -1)) != BASE_SEED or int(motion_b.get("seed", -1)) != BASE_SEED or int(motion_c.get("seed", -1)) != ALTERNATE_SEED:
                _fail("Seed-domain identity mismatch for %s tier-%d." % [family, tier])
                return
            var payload_hash_a := _sha256(payload_a)
            var payload_hash_b := _sha256(payload_b)
            var payload_hash_c := _sha256(payload_c)
            var visual_a := _visual_state(payload_a)
            var visual_b := _visual_state(payload_b)
            var visual_c := _visual_state(payload_c)
            var visual_hash_a := _sha256(visual_a)
            var visual_hash_b := _sha256(visual_b)
            var visual_hash_c := _sha256(visual_c)
            if not _is_sha256(payload_hash_a) or payload_hash_a != payload_hash_b or visual_hash_a != visual_hash_b:
                _fail("Same seed does not reproduce exact payload/state for %s tier-%d." % [family, tier])
                return
            if payload_hash_a == payload_hash_c or visual_hash_a == visual_hash_c:
                _fail("Alternate seed did not change authored payload and visual state for %s tier-%d." % [family, tier])
                return
            if str(task_a.get("type", "")) != family or not policy_tiers.has(str(tier)):
                _fail("Task/policy tier mismatch for %s tier-%d." % [family, tier])
                return
            var receipt: Dictionary = {
                "selection":{"content_type":"visual_drills", "family_id":family, "subtype_id":null, "variant_id":"tier-%d" % tier},
                "canonical_source_path":canonical_path,
                "canonical_source_sha256":_sha256_bytes(canonical_bytes),
                "difficulty_policy_path":policy_path,
                "difficulty_policy_sha256":_sha256_bytes(policy_bytes),
                "canonical_duration_seconds":duration,
                "fps":fps,
                "frame_count":frame_count,
                "base_seed":BASE_SEED,
                "alternate_seed":ALTERNATE_SEED,
                "payload_sha256":payload_hash_a,
                "repeat_payload_sha256":payload_hash_b,
                "alternate_seed_payload_sha256":payload_hash_c,
                "visual_state_sha256":visual_hash_a,
                "repeat_visual_state_sha256":visual_hash_b,
                "alternate_seed_visual_state_sha256":visual_hash_c,
                "deterministic_repeat_pass":true,
                "visual_seed_change_observed":true,
                "selection_identity_matches":true,
                "policy_tier_resolved":true
            }
            receipts.append(receipt)
            deterministic_count += 1
            seed_change_count += 1
            identity_count += 1
            policy_count += 1
            print(OUTPUT_PREFIX + JSON.stringify(_stable_value(receipt)))
    if receipts.size() != 20 or unique_selectors.size() != 20:
        _fail("Expected exactly 20 unique Visual Drill type/tier combinations.")
        return
    var governance := {
        "scope":"AUTHORING_ADAPTER_CAPABILITY_ONLY_NOT_REQUEST_BOUND_PAYLOAD_BINDING",
        "request_bound_payload_manifest_created":false,
        "renderer_native_input_emitted":false,
        "renderer_dispatch_invoked":false,
        "renderer_activation":"OFF",
        "production_execution":false,
        "media_created":false,
        "c11c_source_mutation":false,
        "d4_8":"BLOCKED",
        "release_authority":"NONE",
        "baseline_approval":"MISSING",
        "freeze_eligible":false
    }
    print(SUMMARY_PREFIX + JSON.stringify({
        "schema":"C11-D-D9-VISUAL-DRILL-SELECTOR-AUTHORING-COVERAGE-RUNTIME-V1",
        "schema_version":"1.0",
        "status":"PREPARATION_ONLY_AUTHORING_ADAPTER_CAPABILITY_AUDIT_NOT_DYNAMIC_PAYLOAD_BINDING_OR_RENDERER_INPUT",
        "frozen_c11c_manifest_sha256":MANIFEST_SHA,
        "source_lineage_sha256":source_lineage_sha,
        "family_count":4,
        "selector_count":receipts.size(),
        "deterministic_repeat":deterministic_count,
        "visual_seed_change":seed_change_count,
        "identity_match":identity_count,
        "policy_tier_resolved":policy_count,
        "governance":governance
    }))
    print("C11-D VISUAL DRILL SELECTOR AUTHORING COVERAGE PASS | families=4/4 | selectors=20/20 | deterministic_repeat=20/20 | visual_seed_change=20/20 | identity=20/20 | policy_tier=20/20 | request_bound_manifest=NOT_TESTED | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
    quit(0)

func _make_context(seed_value: int, family_id: String) -> VisualAuthoringAssemblyContext:
    return VisualAuthoringAssemblyContextScript.new(
        seed_value,
        "2.0",
        "C11D-DRILL-COVERAGE-" + family_id,
        "1.0",
        "C11-C-2.19.12",
        {"profile_id":"social_default_v1", "coordinate_space":"CANVAS_540X960"},
        {"family_id":family_id},
        {"profile_id":"default_procedural_music", "enabled":true},
        {"author":"C11D_VISUAL_DRILL_SELECTOR_COVERAGE_REVIEW_ONLY", "timestamp_ms":0}
    )

func _visual_state(payload_value: Dictionary) -> Dictionary:
    var trajectory: Dictionary = payload_value.get("trajectory", {}).duplicate(true)
    var motion: Dictionary = payload_value.get("seed_motion", {}).duplicate(true)
    for key in ["seed_authoring_version", "seed_motion_variant", "seed_spatial_variant"]:
        trajectory.erase(key)
    for key in ["seed", "version", "enabled", "family"]:
        motion.erase(key)
    var exercise: Dictionary = payload_value.get("exercise_parameters", {}).duplicate(true)
    return {"trajectory":trajectory, "seed_motion_parameters":motion, "exercise_parameters":exercise}

func _stable_value(value: Variant) -> Variant:
    if value is Dictionary:
        var keys: Array = value.keys()
        keys.sort()
        var result: Dictionary = {}
        for key in keys:
            result[str(key)] = _stable_value(value[key])
        return result
    if value is Array:
        var array: Array = []
        for item in value:
            array.append(_stable_value(item))
        return array
    return value

func _sha256(value: Variant) -> String:
    var context := HashingContext.new()
    if context.start(HashingContext.HASH_SHA256) != OK:
        return ""
    context.update(JSON.stringify(_stable_value(value)).to_utf8_buffer())
    return context.finish().hex_encode()

func _sha256_bytes(value: PackedByteArray) -> String:
    var context := HashingContext.new()
    if context.start(HashingContext.HASH_SHA256) != OK:
        return ""
    context.update(value)
    return context.finish().hex_encode()

func _is_sha256(value: String) -> bool:
    if value.length() != 64 or value != value.to_lower():
        return false
    for char in value:
        if not "0123456789abcdef".contains(char):
            return false
    return true

func _fail(message: String) -> void:
    push_error("VISUAL DRILL SELECTOR AUTHORING COVERAGE FAIL: " + message)
    print("C11-D VISUAL DRILL SELECTOR AUTHORING COVERAGE FAIL | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE")
    quit(1)
