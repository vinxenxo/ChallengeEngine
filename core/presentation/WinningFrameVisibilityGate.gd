# res://core/presentation/WinningFrameVisibilityGate.gd
class_name WinningFrameVisibilityGate
extends RefCounted

## C11-B.0 — presentation-only gate.
## Validates the already-rendered geometry at the winning frame.
## It never recalculates SimulationResult, winning_frame or RNG state.

const EPSILON: float = 0.01

static func rect_encloses_with_epsilon(container: Rect2, child: Rect2, epsilon: float = EPSILON) -> bool:
	return (
		child.position.x >= container.position.x - epsilon
		and child.position.y >= container.position.y - epsilon
		and child.end.x <= container.end.x + epsilon
		and child.end.y <= container.end.y + epsilon
	)

static func evaluate_screen_rects(
	entities: Array,
	body_rect: Rect2,
	epsilon: float = EPSILON
) -> Dictionary:
	var failures: Array[String] = []
	var mapped_entities: Array = []

	if body_rect.size.x <= 0.0 or body_rect.size.y <= 0.0:
		return {
			"pass": false,
			"errors": ["BodyRegion is empty or invalid."],
			"entities": []
		}

	for entity in entities:
		if not (entity is Dictionary):
			failures.append("Entity audit entry is not a Dictionary.")
			continue

		var entity_id := str(entity.get("id", "unknown"))
		var visible := bool(entity.get("visible", true))
		var has_geometry := bool(entity.get("has_geometry", entity.has("screen_rect")))
		var raw_rect = entity.get("screen_rect", Rect2())
		var screen_rect: Rect2 = raw_rect if raw_rect is Rect2 else Rect2()

		var entry := {
			"id": entity_id,
			"visible": visible,
			"has_geometry": has_geometry,
			"screen_rect": screen_rect
		}
		mapped_entities.append(entry)

		if not visible:
			failures.append("%s is not visible at winning frame." % entity_id)
			continue
		if not has_geometry or screen_rect.size.x <= 0.0 or screen_rect.size.y <= 0.0:
			failures.append("%s has no valid visible geometry." % entity_id)
			continue
		if not rect_encloses_with_epsilon(body_rect, screen_rect, epsilon):
			failures.append("%s escapes BodyRegion: %s" % [entity_id, str(screen_rect)])

	return {
		"pass": failures.is_empty(),
		"errors": failures,
		"entities": mapped_entities,
		"body_rect": body_rect
	}
