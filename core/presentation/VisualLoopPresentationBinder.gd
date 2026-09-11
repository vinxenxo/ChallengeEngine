class_name VisualLoopPresentationBinder
extends RefCounted

## C6-F0.5 / C6-F0.8-D0 — Visual Loop Presentation Binder.
## Transforms a RenderedFrameStream frame into a domain-specific RenderModel.
## Implements a minimal shared envelope utilizing real PresentationProfile composition and geometry.

const PresentationProfile = preload("res://core/presentation/PresentationProfile.gd")

func bind_frame(frame: Dictionary, profile: PresentationProfile, ui_state: String = "GAME") -> Dictionary:
	var model = {}
	
	# 1. Geometry Contract Integration (C6-F0.8-A.1 / D0)
	if profile != null:
		model["geometry"] = profile.get_composition_geometry()
		model["source_canvas_size"] = profile.source_canvas_size
		model["master_output_size"] = profile.master_output_size
	else:
		model["geometry"] = {}
		model["source_canvas_size"] = Vector2(540.0, 960.0)
		model["master_output_size"] = Vector2(1080.0, 1920.0)

	# 2. Minimal Shared Envelope (Marketing / Overlay) utilizing real PresentationProfile contract
	var composition: Dictionary = {}
	if profile != null:
		composition = profile.composition.duplicate(true)
			
	model["badge_text"] = str(composition.get("badge_text", ""))
	model["cta_main"] = str(composition.get("cta_main", "LINK IN BIO"))
	model["cta_sub"] = str(composition.get("cta_sub", "¡Juega ahora!"))
	
	model["show_badge"] = (ui_state == "HOOK")
	model["cta_visible"] = (ui_state == "CTA")
	model["show_hook"] = (ui_state == "HOOK")
	
	model["countdown_visible"] = false
	model["countdown_value"] = ""
	
	# 3. Strict Domain Specific Content (Passed through directly from generator state)
	model["visual_frame_state"] = frame.get("payload", {}).duplicate(true)
	
	return model

func bind(frame: Dictionary, profile: PresentationProfile, ui_state: String = "GAME") -> Dictionary:
	return bind_frame(frame, profile, ui_state)