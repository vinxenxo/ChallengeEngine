extends RefCounted
class_name C11EChallengeEditorialPresentationAdapter

## D-owned, Challenge-only adapter from approved E1 editorial intent to the
## mature C11-C shared visual/editorial layer. This module is invoked only by
## the isolated E4A pixel test path; it does not dispatch or emit renderer input.
## It preserves the output contract of the C11C binder and never mutates that
## binder or its native render_model; it only adapts a deep copy at the D edge.
## The C11C shared layer's mount(frame) entrypoint is invoked below through
## Object.call so the D adapter does not become coupled to a second binder.
## CHALLENGE_OVERLAY remains BLOCKED_GEOMETRY_UNRESOLVED; any unapproved
## Any unapproved Challenge visual field/region is rejected before reaching the shared layer.

const SharedLayerScript = preload("res://core/presentation/C11CVisualEditorialLayer.gd")
const AdapterSchema := "C11E-CHALLENGE-SHARED-EDITORIAL-ADAPTER-V1"

static func resolve_hook_countdown_option(intent: Dictionary) -> Dictionary:
    if str(intent.get("schema", "")) != "C11-E-PRODUCTION-INTENT-V1":
        return {"success": false, "error": "E1 intent schema mismatch."}
    if str(intent.get("status", "")) != "PREPARED_E1_NOT_DISPATCHED":
        return {"success": false, "error": "E1 intent is not preparation-only."}
    var request_value: Variant = intent.get("request", null)
    if not (request_value is Dictionary):
        return {"success": false, "error": "E1 request is missing."}
    var request: Dictionary = request_value
    if str(request.get("content_type", "")) != "challenges":
        return {"success": false, "error": "Challenge presentation option cannot be applied to Loop/Drill."}
    # Challenge-only option cannot be applied to Loop/Drill; this is fail-closed.
    var selection_value: Variant = request.get("selection", null)
    if not (selection_value is Dictionary) or str(selection_value.get("content_type", "")) != "challenges":
        return {"success": false, "error": "E1 Challenge selector identity is invalid."}
    # Pre-E4A.1 sealed intents omit the option and retain historical ON behavior.
    if not request.has("presentation_options"):
        return {"success": true, "show_hook_countdown": true, "source": "LEGACY_E1_DEFAULT_ON"}
    var options_value: Variant = request.get("presentation_options", null)
    if not (options_value is Dictionary):
        return {"success": false, "error": "Challenge presentation_options must be an object."}
    var options: Dictionary = options_value
    if options.size() != 1 or not options.has("show_hook_countdown"):
        return {"success": false, "error": "Challenge presentation_options allowlist mismatch."}
    var visibility_value: Variant = options.get("show_hook_countdown")
    if typeof(visibility_value) != TYPE_BOOL:
        return {"success": false, "error": "show_hook_countdown must be boolean."}
    return {"success": true, "show_hook_countdown": bool(visibility_value), "source": "SEALED_E1_REQUEST_OPTION"}

static func adapt_native_challenge_render_model(base_render_model: Dictionary, intent: Dictionary, shared_model: Dictionary = {}) -> Dictionary:
    var option_result: Dictionary = resolve_hook_countdown_option(intent)
    if not bool(option_result.get("success", false)):
        return option_result
    var adapted: Dictionary = base_render_model.duplicate(true)
    if not bool(option_result.get("show_hook_countdown", true)):
        adapted["show_hook"] = false
        adapted["countdown_visible"] = false
        adapted["countdown_value"] = ""
    # The source video already contains the C hook pixels. When D editorial is
    # active, the shared header recomposes that hook exactly once; suppress the
    # native UI hook in the adapted model to prevent a second live copy.
    if bool(shared_model.get("header_native_hook_migrated", false)):
        adapted["show_hook"] = false
    # CTA has one owner: D's shared footer replaces the native Challenge CTA
    # only during CTA frames where a non-empty approved D CTA is active.
    if bool(shared_model.get("footer_active", false)):
        adapted["cta_visible"] = false
    return {
        "success": true,
        "render_model": adapted,
        "show_hook_countdown": bool(option_result.get("show_hook_countdown", true)),
        "option_source": str(option_result.get("source", "")),
        "native_cta_owner": "D_C11C_SHARED_FOOTER" if bool(shared_model.get("footer_active", false)) else "C_CHALLENGE_PRESENTATION_UI"
    }

static func build_shared_editorial_model(
    field_rows: Array,
    source_frame: int,
    source_frame_count: int,
    editorial_seed: int = 314159,
    native_hook_text: String = "",
    show_hook_countdown: bool = true
) -> Dictionary:
    if source_frame < 0 or source_frame_count <= 0 or source_frame >= source_frame_count:
        return {"success": false, "error": "Source-frame index is outside the Challenge source timebase."}
    if field_rows.size() != 6:
        return {"success": false, "error": "Approved E4A field set must contain exactly six rows."}
    var seen: Dictionary = {}
    var title_text := ""
    var subtitle_text := ""
    var cta_text := ""
    for field_value: Variant in field_rows:
        if not (field_value is Dictionary):
            return {"success": false, "error": "Editorial field row is malformed."}
        var field: Dictionary = field_value
        var field_name := str(field.get("field", ""))
        if field_name.is_empty() or seen.has(field_name):
            return {"success": false, "error": "Editorial field row is unknown or duplicated."}
        seen[field_name] = true
        var disposition := str(field.get("disposition", ""))
        if disposition == "OMITTED_EMPTY" or disposition == "METADATA_ONLY" or disposition == "BLOCKED_GEOMETRY_UNRESOLVED":
            continue
        if disposition != "READY_FOR_ISOLATED_TEST_PIXEL_DRAW":
            return {"success": false, "error": "Unsupported editorial field disposition: %s" % disposition}
        var value := str(field.get("effective_value", "")).strip_edges()
        if value.is_empty():
            continue
        var ranges_value: Variant = field.get("source_frame_ranges", null)
        if not (ranges_value is Array) or ranges_value.is_empty():
            return {"success": false, "error": "Renderable editorial field has no source-time visibility window."}
        var active := false
        for range_value: Variant in ranges_value:
            if not (range_value is Dictionary):
                return {"success": false, "error": "Editorial source-frame range is malformed."}
            var frame_range: Dictionary = range_value
            var start_frame := int(frame_range.get("start_frame", -1))
            var end_frame := int(frame_range.get("end_frame", -1))
            if start_frame < 0 or end_frame <= start_frame or end_frame > source_frame_count:
                return {"success": false, "error": "Editorial source-frame range is invalid."}
            if source_frame >= start_frame and source_frame < end_frame:
                active = true
        if not active:
            continue
        var region := str(field.get("region", ""))
        if field_name == "title" and region == "HEADER":
            title_text = value
        elif field_name == "subtitle" and region == "HEADER":
            subtitle_text = value
        elif field_name == "call_to_action" and region == "FOOTER":
            cta_text = value
        else:
            return {"success": false, "error": "Unapproved Challenge visual field/region reached the shared layer: %s/%s" % [field_name, region]}
    var header_active := not title_text.is_empty() or not subtitle_text.is_empty()
    var footer_active := not cta_text.is_empty()
    var clean_hook := native_hook_text.strip_edges().replace("\r", "").replace("\n", " ")
    var header_native_hook_migrated := header_active and show_hook_countdown and not clean_hook.is_empty()
    if header_active and show_hook_countdown and clean_hook.is_empty():
        return {"success": false, "error": "Cannot composite Challenge editorial over a baked HOOK frame without the native hook text."}
    var d_header_parts: Array[String] = []
    if not title_text.is_empty():
        d_header_parts.append(title_text)
    if not subtitle_text.is_empty():
        d_header_parts.append(subtitle_text)
    # The existing C11C shared header is a three-line, fit-down block. Use its
    # first line for the native Challenge hook and its remaining two-line
    # capacity for optional D title/subtitle. The opaque header background
    # later covers the already-baked C hook, so the content has one owner.
    var header_line_1 := clean_hook if header_native_hook_migrated else title_text
    var header_line_2: String = " · ".join(PackedStringArray(d_header_parts)) if header_native_hook_migrated else subtitle_text
    var editorial := {
        "enabled": header_active or footer_active,
        "header": {"line_1": header_line_1, "line_2": header_line_2},
        "footer": {"line_1": cta_text, "line_2": "", "line_3": ""},
        "show_header": header_active,
        "show_footer": footer_active,
        "matrix_enabled": false,
        "intro_active": false
    }
    return {
        "success": true,
        "schema": AdapterSchema,
        "render_model": {"editorial": editorial, "editorial_frame_index": source_frame, "editorial_frame_count": source_frame_count, "editorial_seed": editorial_seed},
        "header_active": header_active,
        "footer_active": footer_active,
        "header_native_hook_migrated": header_native_hook_migrated,
        "native_hook_overlap": false,
        "native_hook_owner": "D_C11C_SHARED_HEADER" if header_native_hook_migrated else "C11C_BASE_FRAME_HOOK",
        "countdown_visibility_option": "ON_PIXELS_PRESERVED_IN_BASE" if show_hook_countdown else "OFF_IS_LIVE_MODEL_ONLY_NOT_BAKED_BASE_PIXELS",
        "native_cta_owner": "D_C11C_SHARED_FOOTER" if footer_active else "C_CHALLENGE_PRESENTATION_UI",
        "visual_placement": "UNAPPROVED_TEST_ONLY"
    }

static func apply_to_shared_layer(frame: UnifiedSocialFrame, layer: RefCounted, shared_model: Dictionary) -> Dictionary:
    if frame == null or layer == null or not (shared_model.get("render_model", null) is Dictionary):
        return {"success": false, "error": "Shared-layer adapter inputs are incomplete."}
    var mounted_value: Variant = layer.call("mount", frame)
    if typeof(mounted_value) != TYPE_BOOL or not bool(mounted_value):
        return {"success": false, "error": "C11CVisualEditorialLayer could not mount on UnifiedSocialFrame."}
    layer.call("apply_render_model", shared_model["render_model"])
    # Recompose, do not overlay: the shared header must cover the native HOOK
    # already baked into the C base frame before drawing hook + D editorial.
    # C11CVisualEditorialLayer supplies the established three-line layout and
    # its deterministic 29px-to-17px fit-down over the 468px content width.
    if bool(shared_model.get("header_active", false)):
        var header_background := frame.get_header_content_root().get_node_or_null("C11CVisualEditorialHeader/C11CHeaderBackground") as ColorRect
        if header_background == null:
            return {"success": false, "error": "Shared header background node is missing."}
        header_background.color = Color("05070B")
    if bool(shared_model.get("footer_active", false)):
        # The opaque shared footer is the only owner of the approved D CTA,
        # replacing the pre-existing C CTA pixels without a second label.
        var footer_background := frame.get_footer_content_root().get_node_or_null("C11CVisualEditorialFooter/C11CFooterBackground") as ColorRect
        if footer_background == null:
            return {"success": false, "error": "Shared footer background node is missing."}
        footer_background.color = Color("05070B")
    return {"success": true, "visual_placement": "UNAPPROVED_TEST_ONLY", "native_cta_owner": str(shared_model.get("native_cta_owner", "")), "header_native_hook_migrated": bool(shared_model.get("header_native_hook_migrated", false))}

static func get_header_layout_diagnostics(frame: UnifiedSocialFrame, shared_model: Dictionary) -> Dictionary:
    if frame == null or not bool(shared_model.get("header_active", false)):
        return {"success": true, "header_active": false, "line_count": 0, "widest_line_width": 0.0}
    var label := frame.get_header_content_root().get_node_or_null("C11CVisualEditorialHeader/C11CHeaderText") as Label
    if label == null:
        return {"success": false, "error": "Shared C11C header label is missing after mount."}
    var font: Font = label.get_theme_font("font")
    if font == null:
        return {"success": false, "error": "Shared C11C header font did not resolve."}
    var font_size: int = label.get_theme_font_size("font_size")
    var lines: PackedStringArray = label.text.split("\n", true)
    var nonempty_lines: Array[String] = []
    var widest: float = 0.0
    for line in lines:
        if line.strip_edges().is_empty():
            continue
        nonempty_lines.append(line)
        widest = maxf(widest, font.get_string_size(line, HORIZONTAL_ALIGNMENT_LEFT, -1.0, font_size).x)
    var line_height: float = font.get_height(font_size)
    var estimated_height: float = line_height * float(nonempty_lines.size())
    var max_width: float = 468.0
    var box_height: float = 120.0
    var success: bool = nonempty_lines.size() <= 3 and widest <= max_width and estimated_height <= box_height
    return {
        "success": success,
        "header_active": true,
        "line_count": nonempty_lines.size(),
        "lines": nonempty_lines,
        "font_size": font_size,
        "line_height": line_height,
        "estimated_text_height": estimated_height,
        "text_box_height": box_height,
        "widest_line_width": widest,
        "max_width": max_width,
        "native_hook_migrated": bool(shared_model.get("header_native_hook_migrated", false)),
        "error": "Shared header exceeds the existing C11C three-line fit contract." if not success else ""
    }
