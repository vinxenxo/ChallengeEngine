# res://core/presentation/VisualDrillPresentationBinder.gd
class_name VisualDrillPresentationBinder
extends RefCounted

## C6-F0.5 — Visual Drill Presentation Binder.
## Transforms a RenderedFrameStream frame into a domain-specific RenderModel.
## Implements a minimal shared envelope (CTA, Badge) utilizing real PresentationProfile.composition.

const PresentationProfile = preload("res://core/presentation/PresentationProfile.gd")

func bind_frame(frame: Dictionary, profile: PresentationProfile, ui_state: String = "GAME") -> Dictionary:
	var model = {}
	
	# 1. Minimal Shared Envelope (Marketing / Overlay) utilizing real PresentationProfile contract
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
	
	# 2. Strict Domain Specific Content (Passed through directly from generator state)
	model["visual_drill_frame_state"] = frame.get("payload", {}).duplicate(true)
	
	return model