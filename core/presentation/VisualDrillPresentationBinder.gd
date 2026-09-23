# res://core/presentation/VisualDrillPresentationBinder.gd
class_name VisualDrillPresentationBinder
extends RefCounted

## C11-C / C6-F0.5 — Visual Drill Presentation Binder.
## Produces the shared C11-C social/editorial model plus domain-specific drill state.
## Does not alter simulation, RNG, timeline or winning-frame truth.

const PresentationProfile = preload("res://core/presentation/PresentationProfile.gd")

const DISPLAY_NAMES := {
	"tracking": "TRACKING",
	"saccade": "SACCADE",
	"pursuit": "PURSUIT",
	"peripheral_scan": "PERIPHERAL SCAN"
}

const HEADER_DESCRIPTORS := {
	"tracking": "SMOOTH PURSUIT / TRAJECTORY LOCK",
	"saccade": "DISCRETE RELOCATION / SPATIAL PRECISION",
	"pursuit": "CONTINUOUS FOLLOWING / MOTION LOCK",
	"peripheral_scan": "FIXATION / ECCENTRIC STIMULUS"
}

const SIGNATURES := {
	"tracking": "VISUAL DRILL / TRACKING / C11-C",
	"saccade": "VISUAL DRILL / SACCADE / C11-C",
	"pursuit": "VISUAL DRILL / PURSUIT / C11-C",
	"peripheral_scan": "VISUAL DRILL / PERIPHERAL SCAN / C11-C"
}

var _definition_context: Dictionary = {}

func set_definition_context(definition: Dictionary) -> void:
	_definition_context = definition.duplicate(true) if definition is Dictionary else {}

func bind_frame(frame: Dictionary, profile: PresentationProfile, ui_state: String = "GAME") -> Dictionary:
	var model := {}

	# Shared C6/C11-C geometry payload. The logical composition remains 540x960;
	# physical 720x1280 is a capture concern and is intentionally not baked into the frame state.
	if profile != null:
		model["geometry"] = profile.get_composition_geometry()
		model["social_geometry"] = profile.get_social_regions()
		model["source_canvas_size"] = profile.source_canvas_size
		model["master_output_size"] = profile.master_output_size
	else:
		model["geometry"] = {}
		model["social_geometry"] = {
			"canvas_rect": Rect2(0.0, 0.0, 540.0, 960.0),
			"header_rect": Rect2(0.0, 0.0, 540.0, 144.0),
			"body_rect": Rect2(0.0, 144.0, 540.0, 672.0),
			"footer_rect": Rect2(0.0, 816.0, 540.0, 144.0)
		}
		model["source_canvas_size"] = Vector2(540.0, 960.0)
		model["master_output_size"] = Vector2(1080.0, 1920.0)

	var composition: Dictionary = {}
	if profile != null:
		composition = profile.composition.duplicate(true)

	model["badge_text"] = str(composition.get("badge_text", ""))
	model["cta_main"] = str(composition.get("cta_main", "LINK IN BIO"))
	model["cta_sub"] = str(composition.get("cta_sub", "¡Juega ahora!"))
	model["show_badge"] = (ui_state == "HOOK")
	model["cta_visible"] = (ui_state == "CTA")
	model["show_hook"] = false
	model["countdown_visible"] = false
	model["countdown_value"] = ""

	var drill_state: Dictionary = frame.get("payload", {}).duplicate(true)
	model["visual_drill_frame_state"] = drill_state
	model["drill_frame_state"] = drill_state

	model["editorial"] = _build_editorial_model(frame, profile)
	return model

func bind(frame: Dictionary, profile: PresentationProfile, ui_state: String = "GAME") -> Dictionary:
	return bind_frame(frame, profile, ui_state)

func _build_editorial_model(frame: Dictionary, profile: PresentationProfile) -> Dictionary:
	var drill_state: Dictionary = frame.get("payload", {})
	var subtype := str(drill_state.get("generator_type", "visual_drill"))
	var display_name := str(DISPLAY_NAMES.get(subtype, subtype.to_upper()))
	var descriptor := str(HEADER_DESCRIPTORS.get(subtype, "PERCEPTUAL VISUAL EXERCISE"))
	var signature := str(SIGNATURES.get(subtype, "VISUAL DRILL / C11-C"))
	
	var definition := _definition_context
	var definition_payload: Dictionary = definition.get("payload", {}) if definition is Dictionary else {}
	var definition_seed := int(definition.get("seed", 0)) if definition is Dictionary else 0
	var exercise: Dictionary = definition_payload.get("exercise_parameters", {}) if definition_payload is Dictionary else {}
	if not exercise is Dictionary:
		exercise = {}
	var tier := int(exercise.get("difficulty_tier", 0))
	var params: Dictionary = drill_state.get("parameters", {})
	var speed := float(exercise.get("speed_multiplier", 1.0))
	var duration := float(definition_payload.get("duration", 0.0)) if definition_payload is Dictionary else 0.0
	var fps := int(definition_payload.get("fps", 30)) if definition_payload is Dictionary else 30
	var audio_node = definition.get("audio", {}) if definition is Dictionary else {}
	
	var generator_variant := _variant_summary(subtype, params)
	var header_line_1 := "%s | TIER %d | SPEED %.2f" % [display_name, tier, speed]
	if generator_variant.is_empty() == false:
		header_line_1 = "%s | %s | SPEED %.2f" % [display_name, generator_variant, speed]

	var audio_enabled := true
	if audio_node is Dictionary and audio_node.has("enabled"):
		audio_enabled = bool(audio_node.get("enabled"))
	
	return {
		"enabled": true,
		"show_header": true,
		"show_footer": true,
		"show_footer_rule": true,
		"show_header_rule": true,
		"matrix_enabled": true,
		"header": {
			"line_1": header_line_1,
			"line_2": descriptor
		},
		"footer": {
			"line_1": "SEED %d | BODY 720X896 | T=%.2fS | %d FPS | TIER %d" % [definition_seed, duration, fps, tier],
			"line_2": "GEN %s | AUDIO %s | SOCIAL 720X1280" % [display_name, "AMBIENT" if audio_enabled else "OFF"],
			"line_3": signature
		},
		"colors": {
			"header_primary": Color("FFFFFF"),
			"header_secondary": Color("D6E8FF"),
			"footer_data": Color("FFFFFF"),
			"footer_secondary": Color("9CB8D8"),
			"footer_signature": Color("9CB8D8"),
			"rule": Color("6FA6D9")
		}
	}

func _variant_summary(subtype: String, params: Dictionary) -> String:
	match subtype:
		"tracking":
			return "VAR %.2f" % float(params.get("tracking_variant", 0.0))
		"pursuit":
			return "VAR %.2f" % float(params.get("pursuit_variant", 0.0))
		"saccade":
			return "VAR %.2f" % float(params.get("saccade_variant", 0.0))
		"peripheral_scan":
			return "PAT %.2f / AMP %.2f" % [float(params.get("pattern_variant", 0.0)), float(params.get("amplitude_variant", 0.5))]
		_:
			return ""
