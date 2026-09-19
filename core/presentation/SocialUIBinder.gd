# res://core/presentation/SocialUIBinder.gd
class_name SocialUIBinder
extends RefCounted

## C11-B.1 — Presentation-only bridge from normalized render data to UnifiedSocialFrame.
## Does not alter ContentEnvelope, SimulationResult, RNG, timeline or frame truth.

var presentation_ui: PresentationUI
var current_profile: PresentationProfile

func _init(ui: PresentationUI = null, profile: PresentationProfile = null) -> void:
	presentation_ui = ui
	current_profile = profile

func bind_render_model(render_model: Dictionary) -> Dictionary:
	if presentation_ui == null:
		return {"success": false, "error": "PresentationUI is null."}
	presentation_ui.apply_render_model(render_model)
	return {"success": true, "error": ""}

func bind_content_source(content: Dictionary, ui_state: String = "GAME", persistent_footer: bool = false) -> Dictionary:
	if presentation_ui == null:
		return {"success": false, "error": "PresentationUI is null."}
	var model: Dictionary = content.duplicate(true)
	model["ui_state"] = ui_state
	model["show_hook"] = ui_state == "HOOK"
	model["hook_text"] = str(content.get("hook", ""))
	model["cta_main"] = str(content.get("cta", content.get("cta_main", "")))
	model["cta_sub"] = str(content.get("cta_sub", ""))
	model["cta_visible"] = persistent_footer or ui_state == "CTA"
	model["show_badge"] = ui_state == "HOOK"
	return bind_render_model(model)

func extract_presentation_metadata(envelope: Dictionary) -> Dictionary:
	var presentation = envelope.get("presentation", {})
	if not presentation is Dictionary:
		return {}
	return {
		"profile_id": str(presentation.get("profile_id", "")),
		"coordinate_space": str(presentation.get("coordinate_space", "")),
		"theme": str(presentation.get("theme", "default_c6"))
	}
