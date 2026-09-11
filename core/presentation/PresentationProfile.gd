class_name PresentationProfile
extends RefCounted

## C6-E / E2 & C6-F0.8-A.1
## Presentation-only contract.
## MUST NOT own timeline, RNG, simulation truth or winning-frame truth.

const DEFAULT_ID: String = "social_default_v1"
const SOURCE_CANVAS_SIZE := Vector2(540.0, 960.0)
const MASTER_OUTPUT_SIZE := Vector2(1080.0, 1920.0)

var profile_id: String = DEFAULT_ID

# Physical presentation contracts.
var source_canvas_size: Vector2 = SOURCE_CANVAS_SIZE
var master_output_size: Vector2 = MASTER_OUTPUT_SIZE

# Composition Geometry Ratios (C6-F0.8-A.1)
var header_ratio: float = 0.15
var footer_ratio: float = 0.15

# E2 Safe Area contract.
var safe_area: Rect2 = Rect2(
	24.0,
	24.0,
	492.0,
	912.0
)

# E2 Typography contract.
var typography: Dictionary = {
	"scale": 1.0,
	"headline_size": 48,
	"body_size": 32,
	"badge_size": 24,
	"cta_size": 36,
	"countdown_size": 64,
	"max_text_width": 460
}

# E2 Composition contract.
var composition: Dictionary = {
	"hook": "top",
	"gameplay": "center",
	"difficulty_badge": "top_right",
	"reveal": "center",
	"cta": "bottom"
}

# E2 Colors contract.
var colors: Dictionary = {
	"primary": Color.WHITE,
	"accent": Color(1.0, 0.8, 0.0)
}

var asset_family: String = ""
var theme_name: String = "default_c6"
var show_difficulty_badge: bool = true

static func from_challenge(config: Dictionary) -> PresentationProfile:
	var profile := PresentationProfile.new()

	var presentation = config.get("presentation", {})
	if not (presentation is Dictionary):
		presentation = {}

	profile.profile_id = str(
		presentation.get("profile", DEFAULT_ID)
	)

	profile.asset_family = str(
		config.get(
			"asset_family",
			presentation.get("asset_family", "")
		)
	)

	var ui_cfg = presentation.get("ui", {})
	if not (ui_cfg is Dictionary):
		ui_cfg = {}

	profile.theme_name = str(
		ui_cfg.get(
			"theme",
			presentation.get("theme", "default_c6")
		)
	)

	# ---------------------------------------------------------
	# PROFILE OVERRIDES
	# ---------------------------------------------------------

	var overrides = presentation.get(
		"profile_overrides",
		{}
	)

	if not (overrides is Dictionary):
		overrides = {}

	# Composition Geometry Ratios -----------------------------
	if overrides.has("header_ratio") and (overrides["header_ratio"] is float or overrides["header_ratio"] is int):
		profile.header_ratio = float(overrides["header_ratio"])
	if overrides.has("footer_ratio") and (overrides["footer_ratio"] is float or overrides["footer_ratio"] is int):
		profile.footer_ratio = float(overrides["footer_ratio"])

	# Safe area ------------------------------------------------

	var safe_cfg = overrides.get(
		"safe_area",
		{}
	)

	if safe_cfg is Dictionary:
		var left := float(
			safe_cfg.get(
				"left",
				profile.safe_area.position.x
			)
		)

		var top := float(
			safe_cfg.get(
				"top",
				profile.safe_area.position.y
			)
		)

		var right := float(
			safe_cfg.get(
				"right",
				profile.source_canvas_size.x
				- profile.safe_area.end.x
			)
		)

		var bottom := float(
			safe_cfg.get(
				"bottom",
				profile.source_canvas_size.y
				- profile.safe_area.end.y
			)
		)

		profile.safe_area = Rect2(
			left,
			top,
			profile.source_canvas_size.x - left - right,
			profile.source_canvas_size.y - top - bottom
		)

	# Typography ----------------------------------------------

	var type_cfg = overrides.get(
		"typography",
		{}
	)

	if type_cfg is Dictionary:
		profile.typography.merge(
			type_cfg,
			true
		)

	# Composition ---------------------------------------------

	var composition_cfg = overrides.get(
		"composition",
		{}
	)

	if composition_cfg is Dictionary:
		profile.composition.merge(
			composition_cfg,
			true
		)

	# Colors --------------------------------------------------

	var color_cfg = overrides.get(
		"colors",
		{}
	)

	if color_cfg is Dictionary:
		profile.colors.merge(
			color_cfg,
			true
		)

	# Component preferences -----------------------------------

	if presentation.has("show_difficulty_badge"):
		profile.show_difficulty_badge = bool(
			presentation["show_difficulty_badge"]
		)

	return profile

func validate() -> Dictionary:
	var errors: Array[String] = []

	if profile_id.is_empty():
		errors.append("profile_id must not be empty")

	if source_canvas_size != SOURCE_CANVAS_SIZE:
		errors.append("source_canvas_size is immutable and must remain 540x960")

	if master_output_size != MASTER_OUTPUT_SIZE:
		errors.append("master_output_size is immutable and must remain 1080x1920")

	if header_ratio <= 0.0 or footer_ratio <= 0.0 or (header_ratio + footer_ratio) >= 1.0:
		errors.append("header_ratio and footer_ratio must be positive and their sum must be less than 1.0")

	if safe_area.size.x <= 0.0:
		errors.append("safe_area width must be greater than zero")

	if safe_area.size.y <= 0.0:
		errors.append("safe_area height must be greater than zero")

	if safe_area.position.x < 0.0:
		errors.append("safe_area left must be non-negative")

	if safe_area.position.y < 0.0:
		errors.append("safe_area top must be non-negative")

	if safe_area.end.x > source_canvas_size.x:
		errors.append("safe_area exceeds source canvas width")

	if safe_area.end.y > source_canvas_size.y:
		errors.append("safe_area exceeds source canvas height")

	var typography_scale := float(typography.get("scale", 1.0))

	if typography_scale <= 0.0:
		errors.append("typography.scale must be greater than zero")

	var geom_res = validate_composition_geometry()
	if not bool(geom_res["is_valid"]):
		for err in geom_res["errors"]:
			errors.append(str(err))

	return {
		"is_valid": errors.is_empty(),
		"errors": errors
	}

func get_composition_geometry() -> Dictionary:
	var canvas_width := source_canvas_size.x
	var canvas_height := source_canvas_size.y
	
	var header_height := canvas_height * header_ratio
	var header_rect := Rect2(0.0, 0.0, canvas_width, header_height)
	
	var footer_height := canvas_height * footer_ratio
	var footer_rect := Rect2(0.0, canvas_height - footer_height, canvas_width, footer_height)
	
	# Content Viewport se restringe estrictamente al safe_area horizontal y al espacio remanente vertical entre header y footer
	var content_y := maxf(header_rect.end.y, safe_area.position.y)
	var content_bottom := minf(footer_rect.position.y, safe_area.end.y)
	var content_height := maxf(0.0, content_bottom - content_y)
	
	var content_rect := Rect2(
		safe_area.position.x,
		content_y,
		safe_area.size.x,
		content_height
	)
	
	return {
		"canvas_rect": Rect2(Vector2.ZERO, source_canvas_size),
		"safe_rect": safe_area,
		"header_rect": header_rect,
		"content_rect": content_rect,
		"footer_rect": footer_rect
	}

func validate_composition_geometry() -> Dictionary:
	var geom := get_composition_geometry()
	var canvas: Rect2 = geom["canvas_rect"]
	var header: Rect2 = geom["header_rect"]
	var content: Rect2 = geom["content_rect"]
	var footer: Rect2 = geom["footer_rect"]
	var errors: Array[String] = []
	
	if not canvas.encloses(header):
		errors.append("header_rect escapes canvas bounds")
	if not canvas.encloses(footer):
		errors.append("footer_rect escapes canvas bounds")
		
	if header.end.y > content.position.y:
		errors.append("header_rect overlaps with content_rect")
	if content.end.y > footer.position.y:
		errors.append("content_rect overlaps with footer_rect")
		
	if not safe_area.encloses(content):
		errors.append("content_rect must be strictly enclosed within safe_area")
		
	return {
		"is_valid": errors.is_empty(),
		"errors": errors
	}

func build_render_model(current_block: String, content: Dictionary) -> Dictionary:
	return {
		"profile_id": profile_id,
		"source_canvas_size": source_canvas_size,
		"master_output_size": master_output_size,
		"safe_area": safe_area,
		"geometry": get_composition_geometry(),
		"typography": typography.duplicate(true),
		"composition": composition.duplicate(true),
		"colors": colors.duplicate(true),
		"asset_family": asset_family,
		"theme_name": theme_name,
		"phase": current_block,
		"content": content.duplicate(true)
	}