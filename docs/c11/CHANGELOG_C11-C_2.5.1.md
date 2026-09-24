# C11-C 2.5.1 — Tracking/Saccade Visual Hotfix + Aesthetic Recovery

## Scope

2.5.1 is a presentation/runtime hotfix on top of C11-C 2.5.0. The validated Tracking and Saccade mechanic contracts are unchanged.

## Fixes

- Fixed `TrackingRenderer.gd` helper name collision with native `CanvasItem.draw_ellipse()` by using `_draw_ellipse()`.
- The previous parse failure cascaded into `VisualDrillRenderer` and falsely manifested as `SaccadeRendererClass.new()` being unavailable.
- Restored/enhanced Tracking history trail with visible live-head accent and soft glow, while keeping history-only semantics and time-based fade.
- Preserved the established Living Particles Tron road reuse and deterministic six-palette Tracking treatment.
- Strengthened Saccade presentation with the same six-family cosmetic palette language, compact target stack, cardinal ticks, halo and phase-driven flash; no path or spatial interpolation is introduced.
- Updated visual review banner to 2.5.1 and reflected the intended Drill presentation matrix state as OFF.

## Boundary

No changes to simulation truth, structural RNG, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, or the C11-B functional freeze.
