# C11-B.0.1 — Presentation Space Audit

## Purpose

This checkpoint does not modify simulation, RNG, `SimulationResult`, `winning_frame`, or the visibility gate semantics.

It diagnoses any discrepancy between:

1. logical simulation coordinates;
2. the coordinates that `CoordinateMapper` says should be rendered inside `BodyRegion`;
3. the actual `Sprite2D` position observed by the presentation scene at the winning frame.

## Decision

Do not force-project coordinates inside `WinningFrameVisibilityGate`.
That would make the audit compare a reconstructed geometry rather than the geometry actually presented by the scene.

## Required output

The existing `[C11B_VISIBILITY_JSON]` payload now includes `mapping_audit` with:

- `object_logical_position`
- `object_expected_screen_position`
- `object_actual_screen_position`
- `object_delta`
- `object_mapping_match`
- equivalent target diagnostics where `target_position` exists

A non-zero delta identifies a presentation integration problem rather than a simulation problem.

## Expected CHALLENGE_001 examples

With BodyRegion `Rect2(0,144,540,672)` and aspect-preserving fit, the logical sample `Y=1359.253` maps to approximately `Y=619.739`; `Y=821.9901` maps to approximately `Y=431.697`.

Both are inside the BodyRegion. If the actual screen position reports the original logical Y instead, the render boundary is not consuming the mapper result as intended.

## Acceptance

C11-B.0.1 is diagnostic only. The final C11-B.0 gate remains based on actual presentation geometry.
