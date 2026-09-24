# res://core/runtime/visual_drill/generators/SaccadeGenerator.gd
class_name SaccadeGenerator
extends VisualDrillGenerator

## C11-C.7 / Saccade mechanic baseline v1.1 / C11-C 2.6.0.
## Position changes are discrete: no spatial interpolation between endpoints.
## Presentation expresses APPEAR / IDLE / VANISH using scale and opacity only.

const BODY_RECT := Rect2(0.0, 144.0, 540.0, 672.0)
const CENTER := Vector2(270.0, 480.0)
const POSITION_RADIUS: float = 140.0
const RADIUS_VARIATION: float = 20.0
const GOLDEN_ANGLE: float = 2.399963229728653
const MIN_ANGLE_STEP: float = 2.09439510239
const MAX_ANGLE_STEP: float = 2.53072741539
const MIN_RADIUS_BASE: float = 136.0
const MAX_RADIUS_BASE: float = 144.0
const MIN_RADIUS_VARIATION: float = 14.0
const MAX_RADIUS_VARIATION: float = 18.0
const POSITION_MARGIN: float = 44.0
const MIN_JUMP_DISTANCE: float = 180.0
const MAX_JUMP_DISTANCE: float = 300.0
const APPEAR_FRAMES: int = 6
const VANISH_FRAMES: int = 2
const DEFAULT_IDLE_FRAMES: int = 18

func generate(frame_index: int, total_frames: int, drill_parameters: Dictionary) -> Dictionary:
    return generate_with_variation(frame_index, total_frames, drill_parameters, {})

func generate_with_variation(frame_index: int, total_frames: int, drill_parameters: Dictionary, variation: Dictionary) -> Dictionary:
    var progress: float = 0.0 if total_frames <= 1 else clampf(float(frame_index) / float(maxi(1, total_frames - 1)), 0.0, 1.0)
    var exercise: Dictionary = drill_parameters.get("exercise_parameters", {})
    if not exercise is Dictionary:
        exercise = {}
    var tier: int = clampi(int(exercise.get("difficulty_tier", 2)), 1, 5)
    var speed_multiplier: float = clampf(float(exercise.get("speed_multiplier", 1.0)), 0.1, 3.0)
    var idle_frames: int = _idle_frames_for_tier(tier, speed_multiplier)
    var cycle_frames: int = APPEAR_FRAMES + idle_frames + VANISH_FRAMES
    var jump_index: int = maxi(0, frame_index) / maxi(1, cycle_frames)
    var within_cycle: int = posmod(maxi(0, frame_index), maxi(1, cycle_frames))
    var trajectory: Dictionary = _resolve_trajectory(drill_parameters.get("trajectory", {}))
    var position: Vector2 = _position_for_jump(jump_index, trajectory)
    var previous_position: Vector2 = _position_for_jump(maxi(0, jump_index - 1), trajectory)
    var jump_distance: float = position.distance_to(previous_position) if jump_index > 0 else 0.0

    var phase: String = "IDLE"
    var scale: float = 1.0
    var opacity: float = 1.0
    var flash_strength: float = 0.0

    if within_cycle < APPEAR_FRAMES:
        phase = "APPEAR"
        var t: float = float(within_cycle + 1) / float(APPEAR_FRAMES)
        var e: float = _smoothstep(t)
        scale = e
        opacity = e
        flash_strength = 0.18 * sin(PI * e)
    elif within_cycle < APPEAR_FRAMES + idle_frames:
        phase = "IDLE"
    else:
        phase = "VANISH"
        var vanish_index: int = within_cycle - APPEAR_FRAMES - idle_frames
        var t: float = float(vanish_index + 1) / float(VANISH_FRAMES)
        var e: float = _smoothstep(t)
        scale = 1.0 - e
        opacity = 1.0 - e
        flash_strength = 0.28 * sin(PI * t)

    var target := {
        "id": "t1",
        "x": position.x,
        "y": position.y,
        "radius": 12.0,
        "highlighted": true,
        "status": "active" if phase != "VANISH" or opacity > 0.0 else "vanishing",
        "role": "saccade_target",
        "scale": scale,
        "opacity": opacity,
        "visible": opacity > 0.001
    }

    return {
        "generator_type": "saccade",
        "progress": progress,
        "stimulus_state": {"type": "dot", "radius": 12.0, "active": true, "x": position.x, "y": position.y},
        "target_states": [target],
        "distractor_states": [],
        "task_state": {
            "type": "saccade",
            "mode": "discrete_relocation",
            "target_id": "t1"
        },
        "saccade_state": {
            "phase": phase,
            "jump_index": jump_index,
            "position": {"x": position.x, "y": position.y},
            "previous_position": {"x": previous_position.x, "y": previous_position.y},
            "jump_distance": jump_distance,
            "min_jump_distance": MIN_JUMP_DISTANCE,
            "max_jump_distance": MAX_JUMP_DISTANCE,
            "appear_frames": APPEAR_FRAMES,
            "idle_frames": idle_frames,
            "vanish_frames": VANISH_FRAMES,
            "scale": scale,
            "opacity": opacity,
            "flash_strength": flash_strength,
            "distribution": "polar_golden_angle",
            "trajectory_profile": str(trajectory.get("profile", "polar_golden_angle_v1")),
            "angle_step": float(trajectory.get("angle_step", GOLDEN_ANGLE)),
            "angle_offset": float(trajectory.get("angle_offset", 0.0)),
            "radius_base": float(trajectory.get("radius_base", POSITION_RADIUS)),
            "radius_variation": float(trajectory.get("radius_variation", RADIUS_VARIATION))
        },
        "parameters": {
            "saccade_variant": float(variation.get("saccade_variant", 0.0)),
            "difficulty_tier": tier,
            "speed_multiplier": speed_multiplier
        }
    }

func _idle_frames_for_tier(tier: int, speed_multiplier: float) -> int:
    var base: int = DEFAULT_IDLE_FRAMES
    match tier:
        1:
            base = 24
        2:
            base = 18
        3:
            base = 14
        4:
            base = 11
        5:
            base = 9
    var adjusted: int = int(round(float(base) / clampf(speed_multiplier, 0.75, 1.5)))
    return maxi(6, adjusted)

func _resolve_trajectory(raw_trajectory: Variant) -> Dictionary:
    var raw: Dictionary = raw_trajectory if raw_trajectory is Dictionary else {}
    return {
        "angle_step": clampf(float(raw.get("angle_step", GOLDEN_ANGLE)), MIN_ANGLE_STEP, MAX_ANGLE_STEP),
        "angle_offset": clampf(float(raw.get("angle_offset", 0.0)), -PI, PI),
        "radius_base": clampf(float(raw.get("radius_base", POSITION_RADIUS)), MIN_RADIUS_BASE, MAX_RADIUS_BASE),
        "radius_variation": clampf(float(raw.get("radius_variation", RADIUS_VARIATION)), MIN_RADIUS_VARIATION, MAX_RADIUS_VARIATION),
        "profile": str(raw.get("profile", "polar_golden_angle_v1"))
    }

func _position_for_jump(index: int, trajectory: Dictionary) -> Vector2:
    var safe_index: int = maxi(0, index)
    var angle_step: float = float(trajectory.get("angle_step", GOLDEN_ANGLE))
    var angle_offset: float = float(trajectory.get("angle_offset", 0.0))
    var radius_base: float = float(trajectory.get("radius_base", POSITION_RADIUS))
    var radius_variation: float = float(trajectory.get("radius_variation", RADIUS_VARIATION))
    var angle: float = float(safe_index) * angle_step + angle_offset
    var radius: float = radius_base + radius_variation * sin(float(safe_index) * 1.61803398875 + 0.7)
    var position: Vector2 = CENTER + Vector2(cos(angle), sin(angle)) * radius
    position.x = clampf(position.x, BODY_RECT.position.x + POSITION_MARGIN, BODY_RECT.end.x - POSITION_MARGIN)
    position.y = clampf(position.y, BODY_RECT.position.y + POSITION_MARGIN, BODY_RECT.end.y - POSITION_MARGIN)
    return position

func _smoothstep(t: float) -> float:
    var x: float = clampf(t, 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)
