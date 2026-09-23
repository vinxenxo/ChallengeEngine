extends SceneTree

## C11-C — Shared visual social/editorial presentation contract test.
## Presentation-only. Does not touch simulation, RNG, C7 or C9.

const UnifiedSocialFrameScene = preload("res://core/presentation/UnifiedSocialFrame.tscn")
const PresentationProfile = preload("res://core/presentation/PresentationProfile.gd")
const VisualDrillPresentationBinder = preload("res://core/presentation/VisualDrillPresentationBinder.gd")
const C11CVisualEditorialLayer = preload("res://core/presentation/C11CVisualEditorialLayer.gd")
const VisualContentPlayer = preload("res://core/presentation/rendering/VisualContentPlayer.gd")
const C11CHeaderAnimatorV2Class = preload("res://tools/prototypes/c11c_common/C11CHeaderAnimatorV2.gd")

var failures: Array[String] = []

func _initialize() -> void:
	var frame := UnifiedSocialFrameScene.instantiate() as UnifiedSocialFrame
	if frame == null:
		failures.append("UnifiedSocialFrame could not instantiate.")
		_conclude()
		return
	root.add_child(frame)
	await process_frame

	_assert(frame.get_header_rect() == Rect2(0, 0, 540, 144), "Header geometry changed.")
	_assert(frame.get_body_rect() == Rect2(0, 144, 540, 672), "Body geometry changed.")
	_assert(frame.get_footer_rect() == Rect2(0, 816, 540, 144), "Footer geometry changed.")

	var profile := PresentationProfile.new()
	var binder := VisualDrillPresentationBinder.new()
	binder.set_definition_context({
		"kind": "visual_drill",
		"subtype": "tracking",
		"seed": 12345,
		"audio": {"enabled": true},
		"payload": {
			"duration": 2.0,
			"fps": 30,
			"exercise_parameters": {"difficulty_tier": 2, "speed_multiplier": 1.0}
		}
	})
	var source_frame := {
		"frame_index": 0,
		"payload": {
			"generator_type": "tracking",
			"progress": 0.0,
			"stimulus_state": {"x": 50.0, "y": 50.0},
			"target_states": [],
			"distractor_states": [],
			"task_state": {},
			"parameters": {"tracking_variant": 0.25}
		}
	}
	var model := binder.bind_frame(source_frame, profile, "GAME")
	_assert(model.has("geometry"), "VisualDrill binder must expose composition geometry.")
	_assert(model.has("social_geometry"), "VisualDrill binder must expose social geometry.")
	_assert(model.has("source_canvas_size"), "VisualDrill binder must expose source canvas size.")
	_assert(model.has("master_output_size"), "VisualDrill binder must expose master output size.")
	_assert(model.has("editorial"), "VisualDrill binder must expose C11-C editorial model.")

	var editorial: Dictionary = model.get("editorial", {})
	_assert(bool(editorial.get("enabled", false)), "Editorial layer must be enabled for Visual Drill.")
	_assert(bool(editorial.get("matrix_enabled", false)), "Visual Drill editorial Matrix must be enabled.")
	_assert(str(editorial.get("header", {}).get("line_1", "")).begins_with("TRACKING"), "Tracking header source line must identify the drill.")
	_assert(str(editorial.get("footer", {}).get("line_3", "")).find("VISUAL DRILL") >= 0, "Footer signature source line must identify Visual Drill.")
	_assert(str(editorial.get("footer", {}).get("line_1", "")).find("720X896") >= 0, "Footer must expose the physical Body size used by the social composition.")
	_assert(is_equal_approx(VisualContentPlayer.PHYSICAL_SOCIAL_SCALE, 4.0 / 3.0), "Visual Drill physical social scale must map 540x960 logical space to 720x1280.")
	_assert(VisualContentPlayer.LOGICAL_SOCIAL_CANVAS_SIZE == Vector2(540.0, 960.0), "Logical social canvas must remain 540x960.")
	_assert(VisualContentPlayer.PHYSICAL_SOCIAL_OUTPUT_SIZE == Vector2(720.0, 1280.0), "Physical social output must remain 720x1280.")

	var animator := C11CHeaderAnimatorV2Class.new("A\nB", "C\nD", 12345)
	animator.set_sequence(["A\nB", "C\nD", "E\nF", "G\nH"])
	_assert(str(animator.display_sequence_at(0, 120).get("text", "")) == "A\nB", "Matrix sequence must begin with the existing double-line header text.")
	_assert(str(animator.display_sequence_at(30, 120).get("text", "")) == "C\nD", "Matrix sequence must advance deterministically through all editorial texts.")
	_assert(str(animator.display_sequence_at(60, 120).get("text", "")) == "E\nF", "Matrix sequence third state missing.")
	_assert(str(animator.display_sequence_at(90, 120).get("text", "")) == "G\nH", "Matrix sequence fourth state missing.")

	var layer := C11CVisualEditorialLayer.new()
	_assert(layer.mount(frame), "Shared C11CVisualEditorialLayer failed to mount.")
	layer.apply_render_model(model)
	_assert(frame.get_header_content_root().get_node_or_null("C11CVisualEditorialHeader/C11CHeaderLine1") == null, "Former header line 1 must no longer be rendered.")
	_assert(frame.get_header_content_root().get_node_or_null("C11CVisualEditorialHeader/C11CHeaderLine2") != null, "Shared header double-line block missing.")
	_assert(frame.get_footer_content_root().get_node_or_null("C11CVisualEditorialFooter/C11CFooterLine1") != null, "Shared footer line 1 missing.")
	_assert(frame.get_footer_content_root().get_node_or_null("C11CVisualEditorialFooter/C11CFooterLine2") == null, "Former footer line 2 must no longer be rendered.")
	_assert(frame.get_footer_content_root().get_node_or_null("C11CVisualEditorialFooter/C11CFooterLine3") == null, "Former footer line 3 must no longer be rendered.")
	_assert(frame.get_header_content_root().get_node("C11CVisualEditorialHeader/C11CHeaderRule").position.y == 140.0, "Header separator must move below the double-line block.")
	_assert(frame.get_footer_content_root().get_node("C11CVisualEditorialFooter/C11CFooterRule").position.y == 14.0, "Footer separator position must remain the leading separator.")
	_assert(frame.get_header_content_root().visible, "Shared layer must not hide the C11-B header root.")
	_assert(frame.get_footer_content_root().visible, "Shared layer must not hide the C11-B footer root.")

	var disabled_model := model.duplicate(true)
	disabled_model["editorial"]["show_header"] = false
	disabled_model["editorial"]["show_footer"] = false
	layer.apply_render_model(disabled_model)
	_assert(frame.get_header_content_root().visible, "Disabling shared header must not hide the structural header root.")
	_assert(frame.get_footer_content_root().visible, "Disabling shared footer must not hide the structural footer root.")
	_assert(not frame.get_header_content_root().get_node("C11CVisualEditorialHeader").visible, "Shared header container must hide cleanly.")
	_assert(not frame.get_footer_content_root().get_node("C11CVisualEditorialFooter").visible, "Shared footer container must hide cleanly.")

	frame.queue_free()
	await process_frame
	_conclude()

func _assert(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)

func _conclude() -> void:
	if failures.is_empty():
		print("[C11C_VISUAL_DRILL_SOCIAL_PRESENTATION_CONTRACT_SUITE] PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		print("[C11C_VISUAL_DRILL_SOCIAL_PRESENTATION_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
		quit(1)
