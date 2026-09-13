# res://core/presentation/CoordinateMapper.gd
class_name CoordinateMapper
extends RefCounted

enum CoordinateSpace {
	CANVAS_1080X1920,
	PILOT_0X100
}

const PRESENTATION_SIZE: Vector2 = Vector2(540.0, 960.0)
const SIMULATION_CANVAS_SIZE: Vector2 = Vector2(1080.0, 1920.0)

static func get_space_from_string(space_name: String) -> CoordinateSpace:
	match space_name.to_upper():
		"PILOT_0X100", "0_100":
			return CoordinateSpace.PILOT_0X100
		_:
			return CoordinateSpace.CANVAS_1080X1920

static func map_position(
	pos: Vector2,
	space: CoordinateSpace,
	viewport_size: Vector2 = PRESENTATION_SIZE
) -> Vector2:
	match space:
		CoordinateSpace.PILOT_0X100:
			var norm_x: float = clampf(pos.x / 100.0, 0.0, 1.0)
			var screen_x: float = norm_x * viewport_size.x
			var screen_y: float = viewport_size.y * 0.5
			return Vector2(screen_x, screen_y)

		CoordinateSpace.CANVAS_1080X1920:
			var scale_x: float = viewport_size.x / SIMULATION_CANVAS_SIZE.x
			var scale_y: float = viewport_size.y / SIMULATION_CANVAS_SIZE.y
			return Vector2(
				pos.x * scale_x,
				pos.y * scale_y
			)

	return Vector2.ZERO

static func map_scalar_x(
	x: float,
	space: CoordinateSpace,
	viewport_size: Vector2 = PRESENTATION_SIZE
) -> float:
	match space:
		CoordinateSpace.PILOT_0X100:
			var norm_x: float = clampf(x / 100.0, 0.0, 1.0)
			return norm_x * viewport_size.x

		CoordinateSpace.CANVAS_1080X1920:
			var scale_x: float = viewport_size.x / SIMULATION_CANVAS_SIZE.x
			return x * scale_x

	return 0.0