class_name PresentationProfile
extends RefCounted

## C6-E / E2
## Presentation-only contract.
## MUST NOT own timeline, RNG, simulation truth or winning-frame truth.

const DEFAULT_ID: String = "social_default_v1"
const SOURCE_CANVAS_SIZE := Vector2(540.0, 960.0)
const MASTER_OUTPUT_SIZE := Vector2(1080.0, 1920.0)

var profile_id: String = DEFAULT_ID

# Physical presentation contracts.
var source_canvas_size: Vector2 = SOURCE_CANVAS_SIZE
var master_output_size: Vector2 = MASTER_OUTPUT_SIZE

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
		"typography": typography.duplicate(true),
		"composition": composition.duplicate(true),
		"colors": colors.duplicate(true),
		"asset_family": asset_family,
		"theme_name": theme_name,
		"phase": current_block,
		"content": content.duplicate(true)
	}