class_name PresentationFramer
extends RefCounted

## C11-B.0.2 — Presentation Framing Contract.
## Presentation-only transform. It never mutates SimulationResult,
## FrameSnapshot, winning_frame, RNG state or validation truth.
## Framing consumes already-computed presentation-space geometry only.

const POLICY_STATIC_CANVAS := "STATIC_CANVAS"
const POLICY_PRIMARY_FOCUS := "PRIMARY_FOCUS"
const POLICY_FIT_ENTITIES := "FIT_ENTITIES"

static func resolve_policy(config: Dictionary) -> String:
	var presentation = config.get("presentation", {})
	if not (presentation is Dictionary):
		return POLICY_STATIC_CANVAS
	var raw := str(presentation.get("framing_policy", POLICY_STATIC_CANVAS)).to_upper().strip_edges()
	if raw == POLICY_PRIMARY_FOCUS:
		return POLICY_PRIMARY_FOCUS
	if raw == POLICY_FIT_ENTITIES:
		return POLICY_FIT_ENTITIES
	return POLICY_STATIC_CANVAS

static func calculate_presentation_offset(
	entities: Array,
	body_rect: Rect2,
	policy: String,
	primary_id: String = "object"
) -> Vector2:
	match policy:
		POLICY_STATIC_CANVAS, POLICY_FIT_ENTITIES:
			return Vector2.ZERO
		POLICY_PRIMARY_FOCUS:
			for entity in entities:
				if not (entity is Dictionary):
					continue
				if str(entity.get("id", "")) != primary_id:
					continue
				if not bool(entity.get("visible", true)):
					continue
				var raw_rect = entity.get("screen_rect", Rect2())
				if not (raw_rect is Rect2):
					continue
				var rect: Rect2 = raw_rect
				if rect.size.x <= 0.0 or rect.size.y <= 0.0:
					continue
				var entity_center := rect.position + rect.size * 0.5
				var body_center := body_rect.position + body_rect.size * 0.5
				return body_center - entity_center
	return Vector2.ZERO
