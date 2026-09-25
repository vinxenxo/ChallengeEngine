class_name C11CVisualLoopDuration
extends RefCounted

## C11-C 2.14.0 — compact shared Visual Loop duration policy.
## Presentation-only: no gameplay truth, no RNG ownership, no C7/C9 changes.

const FPS: int = 30
const MIN_SECONDS: float = 20.0
const MAX_SECONDS: float = 23.0

static func policy_seconds_for_cycles(loop_cycles: int) -> float:
    match clampi(loop_cycles, 1, 3):
        1:
            return 20.0
        2:
            return 22.0
        _:
            return 23.0

static func resolve(loop_cycles: int, default_seconds: float = 0.0) -> Dictionary:
    var requested := OS.get_environment("C11C_DURATION_SECONDS").strip_edges()
    var seconds := default_seconds if default_seconds > 0.0 else policy_seconds_for_cycles(loop_cycles)
    if requested.is_valid_float():
        seconds = float(requested)
    seconds = clampf(seconds, MIN_SECONDS, MAX_SECONDS)
    var frames := maxi(1, int(round(seconds * float(FPS))))
    return {
        "duration_seconds": seconds,
        "fps": FPS,
        "frame_count": frames
    }
