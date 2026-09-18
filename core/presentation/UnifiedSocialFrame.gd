# res://core/presentation/UnifiedSocialFrame.gd
class_name UnifiedSocialFrame
extends Control

## C11-B.0 — Unified Social Frame.
## Shared canvas topology for Challenges, Visual Loops, Visual Drills and future families.
## This node owns geometry/regions only. It does not own simulation, RNG or timing truth.

@onready var header_region: Control = $HeaderRegion
@onready var body_region: Control = $BodyRegion
@onready var footer_region: Control = $FooterRegion

var current_profile: PresentationProfile

func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	_apply_geometry(PresentationProfile.new())

func apply_profile(profile: PresentationProfile) -> void:
	if profile == null:
		return
	current_profile = profile
	_apply_geometry(profile)

func _apply_geometry(profile: PresentationProfile) -> void:
	var regions := profile.get_social_regions()
	var canvas: Rect2 = regions["canvas_rect"]
	var header: Rect2 = regions["header_rect"]
	var body: Rect2 = regions["body_rect"]
	var footer: Rect2 = regions["footer_rect"]

	size = canvas.size
	header_region.position = header.position
	header_region.size = header.size
	body_region.position = body.position
	body_region.size = body.size
	footer_region.position = footer.position
	footer_region.size = footer.size

func get_body_rect() -> Rect2:
	return Rect2(body_region.position, body_region.size)

func get_header_rect() -> Rect2:
	return Rect2(header_region.position, header_region.size)

func get_footer_rect() -> Rect2:
	return Rect2(footer_region.position, footer_region.size)
