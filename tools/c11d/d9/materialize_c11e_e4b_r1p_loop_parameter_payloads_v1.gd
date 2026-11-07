extends SceneTree

## R1P: request-scoped C11-C family parameter payload materializer.
## Uses only the existing deterministic C11-C RefCounted helpers. It does not
## preload or instantiate any prototype/renderer/scene, create buffers/pixels,
## invoke family launchers, touch audio, or write files.

const VariationProfile = preload("res://C11CVariationProfile.gd")
const PaletteBank = preload("res://C11CPaletteBank.gd")
const EditorialColors = preload("res://C11CEditorialColors.gd")
const LoopDuration = preload("res://C11CVisualLoopDuration.gd")
const Technobabble = preload("res://TechnobabbleGenerator.gd")

const INPUT_SCHEMA := "C11E-E4B-R1P-GODOT-INPUT-V1"
const RESULT_SCHEMA := "C11E-E4B-R1P-GODOT-RESULT-V1"
const RESULT_PREFIX := "C11E_E4B_R1P_RESULT="
const FPS := 30

func _initialize() -> void:
    call_deferred("_run")

func _run() -> void:
    var input_path := OS.get_environment("C11E_R1P_INPUT_PATH").strip_edges()
    if input_path.is_empty():
        _fail("C11E_R1P_INPUT_PATH is not set")
        return
    if not OS.get_environment("C11C_DURATION_SECONDS").strip_edges().is_empty():
        _fail("C11C_DURATION_SECONDS must be unset; R1P requires the canonical prototype duration policy")
        return

    var input_file := FileAccess.open(input_path, FileAccess.READ)
    if input_file == null:
        _fail("Cannot open R1P input JSON: " + input_path)
        return
    var parsed: Variant = JSON.parse_string(input_file.get_as_text())
    input_file.close()
    if not (parsed is Dictionary):
        _fail("R1P input must be a JSON object")
        return
    var input_data: Dictionary = parsed
    if input_data.get("schema") != INPUT_SCHEMA or input_data.get("schema_version") != "1.0":
        _fail("R1P input schema mismatch")
        return
    var cases: Variant = input_data.get("cases", null)
    if not (cases is Array) or cases.size() != 27:
        _fail("R1P input must contain exactly 27 canonical request bindings")
        return

    var output_cases: Array[Dictionary] = []
    var seen_case_ids: Dictionary = {}
    for case_value in cases:
        if not (case_value is Dictionary):
            _fail("R1P case entry is not a Dictionary")
            return
        var case_data: Dictionary = case_value
        var case_id := str(case_data.get("case_id", ""))
        if case_id.is_empty() or seen_case_ids.has(case_id):
            _fail("R1P case id is empty or duplicated: " + case_id)
            return
        seen_case_ids[case_id] = true
        var first := _build_payload(case_data)
        var second := _build_payload(case_data)
        if not bool(first.get("success", false)) or not bool(second.get("success", false)):
            _fail(case_id + ": " + str(first.get("error", second.get("error", "unknown payload error"))))
            return
        var first_payload: Dictionary = first["payload"]
        var second_payload: Dictionary = second["payload"]
        var first_canonical := JSON.stringify(_canonicalize(first_payload))
        var second_canonical := JSON.stringify(_canonicalize(second_payload))
        var first_hash := _sha256_string(first_canonical)
        var second_hash := _sha256_string(second_canonical)
        if first_hash.is_empty() or first_hash != second_hash or first_canonical != second_canonical:
            _fail(case_id + ": independent parameter materializations are not byte-canonical deterministic")
            return
        output_cases.append({
            "case_id": case_id,
            "payload": first_payload,
            "payload_canonical_json": first_canonical,
            "payload_sha256": first_hash,
            "repeat_payload_sha256": second_hash,
            "deterministic_repeat_pass": true,
            "source_pins": case_data.get("source_pins", {}).duplicate(true),
            "governance": {
                "godot_invoked": true,
                "renderer_instantiated": false,
                "prototype_node_instantiated": false,
                "shader_created": false,
                "frame_buffers_created": false,
                "pixels_created": false,
                "renderer_native_input_emitted": false,
                "renderer_dispatch_invoked": false,
                "launchers_invoked": false,
                "audio_or_d3_invoked": false,
                "ffmpeg_invoked": false,
                "media_created": false,
                "godot_checkout_files_written": false,
                "release_authority": "NONE"
            }
        })

    var result := {
        "schema": RESULT_SCHEMA,
        "status": "PASS_R1P_PARAMETER_PAYLOADS_27_OF_27",
        "run_id": str(input_data.get("run_id", "")),
        "case_count": output_cases.size(),
        "family_count": 5,
        "grammar_count": 27,
        "cases": output_cases,
        "governance": {
            "godot_invoked": true,
            "prototype_nodes_instantiated": false,
            "renderer_instantiated": false,
            "shader_created": false,
            "frame_buffers_created": false,
            "pixels_created": false,
            "renderer_input_emitted": false,
            "renderer_dispatch_invoked": false,
            "launchers_invoked": false,
            "audio_or_d3_invoked": false,
            "ffmpeg_invoked": false,
            "media_created": false,
            "godot_checkout_files_written": false,
            "release_authority": "NONE"
        }
    }
    print(RESULT_PREFIX + JSON.stringify(_canonicalize(result)))
    quit(0)

func _build_payload(case_data: Dictionary) -> Dictionary:
    var family_id := str(case_data.get("family_id", ""))
    var internal_id := str(case_data.get("internal_family_id", ""))
    var grammar_id := str(case_data.get("grammar_id", ""))
    var grammar_index := int(case_data.get("grammar_index", -1))
    var gameplay_seed := int(case_data.get("gameplay_seed", 0))
    var music_seed := int(case_data.get("music_seed", 0))
    var identity: Variant = case_data.get("request_identity", null)
    var local_pins: Variant = case_data.get("source_pins", null)
    if family_id.is_empty() or internal_id.is_empty() or grammar_id.is_empty() or grammar_index < 0:
        return {"success": false, "error": "missing family/grammar selector identity"}
    if gameplay_seed < 1 or gameplay_seed > 2147483646 or music_seed < 1 or music_seed > 2147483646 or gameplay_seed == music_seed:
        return {"success": false, "error": "gameplay/music seed domains must be explicit, valid and distinct"}
    if not (identity is Dictionary) or not (local_pins is Dictionary):
        return {"success": false, "error": "request identity/source pins must be dictionaries"}

    # Match each C11-C prototype's _ready() path exactly:
    # build the family recipe from request.seed, then apply its explicit
    # C11C_VISUAL_GRAMMAR index/name override.
    var request_identity: Dictionary = identity
    var case_source_pins: Dictionary = local_pins

    var variation: Dictionary = VariationProfile.build(internal_id, gameplay_seed)
    if variation.is_empty() or str(variation.get("family", "")) != internal_id:
        return {"success": false, "error": "C11CVariationProfile returned an empty/wrong family recipe"}
    variation["grammar_mode"] = grammar_index
    variation["grammar_name"] = grammar_id

    # Exact prototype order: duration is resolved before palette selection.
    # DEFAULT_LOOP_DURATION=0.0; C11CVisualLoopDuration also reads the duration
    # environment override, which the runner explicitly unsets.
    var timing: Dictionary = LoopDuration.resolve(int(variation.get("loop_cycles", 0.0)), 0.0)
    if timing.is_empty() or int(timing.get("fps", 0)) != FPS:
        return {"success": false, "error": "C11CVisualLoopDuration returned an invalid timebase"}
    var duration_seconds := float(timing.get("duration_seconds", 0.0))
    var frame_count := int(timing.get("frame_count", 0))
    if (duration_seconds != 20.0 and duration_seconds != 22.0 and duration_seconds != 23.0) or frame_count != int(round(duration_seconds * float(FPS))):
        return {"success": false, "error": "C11C duration/frame policy does not match 20/22/23s at 30 FPS"}
    timing["loop_cycles"] = int(variation.get("loop_cycles", 0.0))
    timing["source"] = "C11CVisualLoopDuration.resolve(loop_cycles, DEFAULT_LOOP_DURATION=0.0)"

    # Exact prototype behavior: palette family + variation palette index;
    # intentionally do NOT pass a seed (no seed-derived palette variant).
    var palette: Dictionary = PaletteBank.palette(internal_id, int(variation.get("palette_mode", -1)))
    if palette.is_empty() or not palette.has("name"):
        return {"success": false, "error": "C11CPaletteBank failed to resolve the family palette"}

    # Preserve the C11-C editorial text-color mapping, serialized as stable
    # six-digit HTML hex values rather than Godot Color Variants.
    var raw_text_colors: Dictionary = EditorialColors.palette(internal_id, palette)
    var editorial_text_colors: Dictionary = {}
    var color_keys: Array = raw_text_colors.keys()
    color_keys.sort()
    for color_key in color_keys:
        var color_value: Color = raw_text_colors[color_key]
        editorial_text_colors[str(color_key)] = color_value.to_html(false).to_upper()
    if editorial_text_colors.size() != 7:
        return {"success": false, "error": "C11CEditorialColors returned an incomplete color map"}

    # Same deterministic family editorial call used by the prototypes.
    var generated_text: String = Technobabble.generate_geek_text(internal_id, gameplay_seed, variation)
    if generated_text.strip_edges().is_empty():
        return {"success": false, "error": "TechnobabbleGenerator returned empty editorial text"}
    var visual_parameters := {
        "family_id": family_id,
        "internal_family_id": internal_id,
        "variation_recipe": variation.duplicate(true),
        "palette": palette.duplicate(true),
        "editorial_text_colors": editorial_text_colors,
        "technobabble": {
            "revision": Technobabble.revision(),
            "generated_text": generated_text,
            "display_text": generated_text.to_upper()
        }
    }
    var visual_canonical_json := JSON.stringify(_canonicalize(visual_parameters))
    var visual_hash := _sha256_string(visual_canonical_json)
    var payload := {
        "schema": "C11E-E4B-R1P-VISUAL-PARAMETER-PAYLOAD-V1",
        "request_binding": {
            "request_identity": request_identity.duplicate(true),
            "request_id": str(request_identity.get("request_id", "")),
            "family_music_profile_id": str(case_data.get("family_music_profile_id", ""))
        },
        "selection": {
            "content_type": "visual_loops",
            "family_id": family_id,
            "grammar_id": grammar_id,
            "grammar_index": grammar_index
        },
        "seed_domains": {
            "gameplay_seed": gameplay_seed,
            "music_seed": music_seed,
            "visual_parameters_use": "request.seed",
            "music_seed_consumed_by_visual_parameters": false,
            "automatic_seed_generation": false,
            "runtime_seed_derivation": false
        },
        "visual_parameters": visual_parameters,
        "visual_parameters_canonical_json": visual_canonical_json,
        "visual_parameters_sha256": visual_hash,
        "timing": timing,
        "governance": {
            "parameter_payload_materialized_in_memory": true,
            "renderer_instantiated": false,
            "prototype_node_instantiated": false,
            "frame_buffers_created": false,
            "frame_inventory_materialized": false,
            "pixels_created": false,
            "renderer_native_input_emitted": false,
            "renderer_dispatch_invoked": false,
            "launchers_invoked": false,
            "audio_or_d3_invoked": false,
            "ffmpeg_invoked": false,
            "media_created": false,
            "godot_checkout_files_written": false,
            "release_authority": "NONE"
        }
    }
    return {"success": true, "payload": payload}

func _canonicalize(value: Variant) -> Variant:
    if value is Dictionary:
        var keys: Array = value.keys()
        keys.sort()
        var result: Dictionary = {}
        for key in keys:
            result[str(key)] = _canonicalize(value[key])
        return result
    if value is Array:
        var result_array: Array = []
        for item in value:
            result_array.append(_canonicalize(item))
        return result_array
    return value

func _sha256(value: Variant) -> String:
    return _sha256_string(JSON.stringify(_canonicalize(value)))

func _sha256_string(value: String) -> String:
    var context := HashingContext.new()
    if context.start(HashingContext.HASH_SHA256) != OK:
        return ""
    context.update(value.to_utf8_buffer())
    return context.finish().hex_encode()

func _fail(message: String) -> void:
    push_error("C11-E E4B R1P PARAMETER PAYLOAD FAIL | " + message)
    quit(1)
