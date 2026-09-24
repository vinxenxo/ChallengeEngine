class_name VisualDrillPresentationPhaseLogic
extends RefCounted

## C11-C 2.7.0 — Shared Visual Drill presentation phases.
const CountdownPresentationLogic = preload("res://core/presentation/CountdownPresentationLogic.gd")

## Presentation-only companion to CountdownPresentationLogic.
## This does not alter VisualDrillRuntime, RenderedFrameStream or mechanic truth.

const COUNTDOWN_SECONDS: float = CountdownPresentationLogic.COUNTDOWN_SECONDS
const END_CTA_SECONDS: float = 3.0

static func countdown_frames(fps: int) -> int:
    return int(round(COUNTDOWN_SECONDS * float(maxi(1, fps))))

static func end_cta_frames(fps: int) -> int:
    return int(round(END_CTA_SECONDS * float(maxi(1, fps))))

static func total_presentation_frames(gameplay_frames: int, fps: int) -> int:
    return countdown_frames(fps) + maxi(0, gameplay_frames) + end_cta_frames(fps)

static func total_presentation_seconds(gameplay_frames: int, fps: int) -> float:
    var effective_fps := float(maxi(1, fps))
    return float(maxi(0, gameplay_frames)) / effective_fps + COUNTDOWN_SECONDS + END_CTA_SECONDS

static func phase_for_frame(presentation_frame_index: int, gameplay_frames: int, fps: int) -> String:
    var index := maxi(0, presentation_frame_index)
    var pre_roll := countdown_frames(fps)
    var game_end := pre_roll + maxi(0, gameplay_frames)
    var total := game_end + end_cta_frames(fps)
    if index < pre_roll:
        return "PRE_ROLL"
    if index < game_end:
        return "GAME"
    if index < total:
        return "END_CTA"
    return "DONE"

static func end_cta_progress(presentation_frame_index: int, gameplay_frames: int, fps: int) -> float:
    var start := countdown_frames(fps) + maxi(0, gameplay_frames)
    var frames := maxi(1, end_cta_frames(fps))
    var denominator := maxi(1, frames - 1)
    return clampf(float(presentation_frame_index - start) / float(denominator), 0.0, 1.0)
