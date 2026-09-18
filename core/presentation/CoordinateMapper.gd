# res://core/presentation/CoordinateMapper.gd
class_name CoordinateMapper
extends RefCounted

## C11-B.0 — Presentation-only coordinate mapping.
##
## The logical simulation canvas remains 1080x1920.
## A target_rect can constrain the presentation to a social body region
## without changing simulation mathematics or frame truth.
##
## Aspect ratio is preserved by default. The source canvas is fitted inside
## the target rect and centered; no clipping or distortion is introduced.

enum CoordinateSpace {
	CANVAS_1080X1920,
	PILOT_0X100
}

const PRESENTATION_SIZE: Vector2 = Vector2(540.0, 960.0)
const SIMULATION_CANVAS_SIZE: Vector2 = Vector2(1080.0, 1920.0)
const DEFAULT_SOCIAL_BODY_RECT: Rect2 = Rect2(0.0, 144.0, 540.0, 672.0)

static func get_space_from_string(space_name: String) -> CoordinateSpace:
	match space_name.to_upper():
		"PILOT_0X100", "0_100":
			return CoordinateSpace.PILOT_0X100
		_:
			return CoordinateSpace.CANVAS_1080X1920

static func resolve_target_rect(
	viewport_size: Vector2 = PRESENTATION_SIZE,
	target_rect: Rect2 = Rect2()
) -> Rect2:
	if target_rect.size.x > 0.0 and target_rect.size.y > 0.0:
		return target_rect
	return Rect2(Vector2.ZERO, viewport_size)

static func get_fit_transform(
	target_rect: Rect2,
	preserve_aspect: bool = true
) -> Dictionary:
	if target_rect.size.x <= 0.0 or target_rect.size.y <= 0.0:
		return {
			"valid": false,
			"scale": Vector2.ZERO,
			"offset": target_rect.position,
			"mapped_size": Vector2.ZERO,
			"target_rect": target_rect
		}

	var scale_vec: Vector2
	if preserve_aspect:
		var uniform_scale := minf(
			target_rect.size.x / SIMULATION_CANVAS_SIZE.x,
			target_rect.size.y / SIMULATION_CANVAS_SIZE.y
		)
		scale_vec = Vector2.ONE * uniform_scale
	else:
		scale_vec = Vector2(
			target_rect.size.x / SIMULATION_CANVAS_SIZE.x,
			target_rect.size.y / SIMULATION_CANVAS_SIZE.y
		)

	var mapped_size := SIMULATION_CANVAS_SIZE * scale_vec
	var offset := target_rect.position + (target_rect.size - mapped_size) * 0.5

	return {
		"valid": true,
		"scale": scale_vec,
		"offset": offset,
		"mapped_size": mapped_size,
		"target_rect": target_rect
	}

static func map_position(
	pos: Vector2,
	space: CoordinateSpace,
	viewport_size: Vector2 = PRESENTATION_SIZE,
	target_rect: Rect2 = Rect2()
) -> Vector2:
	var target := resolve_target_rect(viewport_size, target_rect)

	match space:
		CoordinateSpace.PILOT_0X100:
			var norm_x: float = clampf(pos.x / 100.0, 0.0, 1.0)
			var screen_x: float = target.position.x + norm_x * target.size.x
			var screen_y: float = target.position.y + target.size.y * 0.5
			return Vector2(screen_x, screen_y)

		CoordinateSpace.CANVAS_1080X1920:
			var transform := get_fit_transform(target, true)
			return transform["offset"] + pos * transform["scale"]

	return Vector2.ZERO

static func map_scalar_x(
	x: float,
	space: CoordinateSpace,
	viewport_size: Vector2 = PRESENTATION_SIZE,
	target_rect: Rect2 = Rect2()
) -> float:
	var target := resolve_target_rect(viewport_size, target_rect)

	match space:
		CoordinateSpace.PILOT_0X100:
			var norm_x: float = clampf(x / 100.0, 0.0, 1.0)
			return target.position.x + norm_x * target.size.x

		CoordinateSpace.CANVAS_1080X1920:
			var transform := get_fit_transform(target, true)
			return transform["offset"].x + x * transform["scale"].x

	return 0.0

static func map_rect(
	logical_rect: Rect2,
	target_rect: Rect2 = Rect2(),
	viewport_size: Vector2 = PRESENTATION_SIZE
) -> Rect2:
	var target := resolve_target_rect(viewport_size, target_rect)
	var transform := get_fit_transform(target, true)
	if not bool(transform["valid"]):
		return Rect2()

	return Rect2(
		transform["offset"] + logical_rect.position * transform["scale"],
		logical_rect.size * transform["scale"]
	)
