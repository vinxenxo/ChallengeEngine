extends SceneTree

const UnifiedSocialFrameScene = preload("res://core/presentation/UnifiedSocialFrame.tscn")
const PresentationUI = preload("res://core/presentation/PresentationUI.gd")
const PresentationProfile = preload("res://core/presentation/PresentationProfile.gd")
const SocialUIBinder = preload("res://core/presentation/SocialUIBinder.gd")

var failures: Array[String] = []

func _initialize() -> void:
	var frame := UnifiedSocialFrameScene.instantiate() as UnifiedSocialFrame
	if frame == null:
		failures.append("UnifiedSocialFrame scene could not instantiate.")
		_conclude()
		return
	root.add_child(frame)
	await process_frame

	_assert_rect(frame.get_header_rect(), Rect2(0, 0, 540, 144), "HeaderRegion")
	_assert_rect(frame.get_body_rect(), Rect2(0, 144, 540, 672), "BodyRegion")
	_assert_rect(frame.get_footer_rect(), Rect2(0, 816, 540, 144), "FooterRegion")

	var profile := PresentationProfile.new()
	var ui := PresentationUI.new(frame, "default_c6", profile)
	var binder := SocialUIBinder.new(ui, profile)
	var result := binder.bind_render_model({"show_hook": true, "hook_text": "B1 TEST HOOK", "show_badge": true, "badge_text": "B1", "cta_visible": true, "cta_main": "B1 CTA", "cta_sub": "TEST"})
	if not bool(result.get("success", false)):
		failures.append("SocialUIBinder failed to route render model.")
	if ui.hook_label == null or not ui.hook_label.visible or ui.hook_label.label.text != "B1 TEST HOOK":
		failures.append("Header hook routing failed.")
	if ui.cta == null or not ui.cta.visible or ui.cta.label_main.text != "B1 CTA":
		failures.append("Footer CTA routing failed.")

	var source := {"presentation": {"profile_id": "social_default_v1", "coordinate_space": "2d"}}
	var metadata := binder.extract_presentation_metadata(source)
	if metadata.get("profile_id", "") != "social_default_v1":
		failures.append("ContentEnvelope presentation metadata extraction failed.")
	if source != {"presentation": {"profile_id": "social_default_v1", "coordinate_space": "2d"}}:
		failures.append("SocialUIBinder mutated source envelope.")

	var main_text := FileAccess.get_file_as_string("res://Main.tscn")
	if not main_text.contains("UnifiedSocialFrame"):
		failures.append("Main.tscn missing UnifiedSocialFrame.")
	var visual_text := FileAccess.get_file_as_string("res://core/presentation/rendering/VisualContentPlayer.tscn")
	if not visual_text.contains("UnifiedSocialFrame"):
		failures.append("VisualContentPlayer.tscn missing UnifiedSocialFrame.")

	frame.queue_free()
	_conclude()

func _assert_rect(actual: Rect2, expected: Rect2, label: String) -> void:
	if actual != expected:
		failures.append("%s geometry mismatch: got %s expected %s" % [label, actual, expected])

func _conclude() -> void:
	if failures.is_empty():
		print("[C11B1_SOCIAL_UI_INTEGRATION_CONTRACT_SUITE] PASS")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		print("[C11B1_SOCIAL_UI_INTEGRATION_CONTRACT_SUITE] FAIL failures=%d" % failures.size())
		quit(1)
