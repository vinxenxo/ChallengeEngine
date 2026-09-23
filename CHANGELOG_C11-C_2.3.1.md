# C11-C 2.3.1 — Tracking mechanic hotfix

## Purpose

Hotfix over C11-C 2.3.0 to make the Tracking baseline compile cleanly on Godot 4.7.1 and reduce the initial pursuit speed after physical review.

## Fixes

- Typed Variant-derived locals in `TrackingRenderer.gd` to prevent Godot static inference errors (`rx`, `ry`).
- Typed `trail_last` in `C11CTrackingMechanicContractTest.gd` to prevent Variant inference failure.
- The `VisualDrillRenderer` runtime `new()` failure is resolved by restoring successful compilation of its preloaded `TrackingRenderer.gd` dependency.
- Tracking default travel cycles reduced from `0.50` to `0.25` while preserving the same bounded Lissajous 2:3 path shape.
- Canonical/profile tracking definitions updated to `travel_cycles = 0.25`.
- Contract test adds a conservative `<= 600 px/s` baseline speed ceiling.

## Future presentation note

A fully drawn trajectory preview can be added later as a presentation variant. It should be emitted/rendered as a deliberate preview channel and must not become hidden trajectory math inside the renderer. It is intentionally not included in 2.3.1.

## Frozen boundaries

No changes to Challenge simulation, SimulationResult, winning_frame, close_calls, structural RNG ownership, C7 audio contracts, C9 authoring contracts, or C11-B logical geometry.
