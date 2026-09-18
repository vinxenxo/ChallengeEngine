# C11-B.0 — Unified Social Frame & Body Visibility

## Status
OPEN → IMPLEMENTED DELTA / NOT YET CERTIFIED

C11-A and C11-A.1 remain frozen. This phase changes presentation mapping only.
No simulation, RNG, SimulationResult or winning-frame mathematics are changed.

## Canonical canvas

Export canvas: `540x960`.

- HeaderRegion: `Rect2(0, 0, 540, 144)`
- BodyRegion: `Rect2(0, 144, 540, 672)`
- FooterRegion: `Rect2(0, 816, 540, 144)`

Header/body/footer are structural regions shared by every product family.
Content roles such as hook, CTA, countdown, branding and information are not separate layouts.

## Coordinate projection

The logical challenge simulation remains `1080x1920`.

`CoordinateMapper.map_position()` and `map_scalar_x()` now accept an optional `target_rect`.
When supplied for `CANVAS_1080X1920`, the source is fitted into the target rectangle with a uniform scale and centered offset.

For the canonical BodyRegion the fit is:

- uniform scale: `0.35`
- mapped logical canvas: `378x672`
- horizontal centering: `81px` left/right
- logical `(0,0)` → `(81,144)`
- logical `(1080,1920)` → `(459,816)`
- logical `(540,1700)` → `(270,739)`

No simulation coordinate is clamped or rewritten.

## Winning-frame visibility gate

`WinningFrameVisibilityGate.gd` validates the actual presentation rectangles at the authoritative winning frame.

A run fails when a visible winning entity:

- has no geometry;
- is not visible; or
- extends outside BodyRegion.

The gate is presentation-only and consumes already-produced geometry.

## Challenge integration

`GeneradorMaestro.gd` now projects challenge object/target presentation through BodyRegion.
The background and social UI remain on the full canvas.

A dedicated audit mode exists:

`--validate-only --c11b-visibility-audit`

It emits `[C11B_VISIBILITY_JSON]` and exits non-zero when the gate fails.

## 54-run audit

`tools/run_c11b_body_visibility_audit.ps1` consumes the frozen C11-A.1 run set and reuses each `challenge_definition.json`.

It does not render, alter source challenges or regenerate C11-A.1 artifacts.

Output:

`qa/c11b_visibility_qa/C11B0_BODY_VISIBILITY_MANIFEST.json`

Formal C11-B.0 PASS requires:

`54/54 visibility_pass`.

## Deliberate scope boundary

This checkpoint does not yet migrate `PresentationUI` and `VisualContentPlayer` onto `UnifiedSocialFrame`.
That integration belongs to C11-B.1, after the geometry contract and challenge visibility gate are proven.

### v3 correction
The `target_position` secondary binding is mapped through the same `BodyRegion` target rect as the primary entity. This keeps both winning-frame entities under the Unified Social Frame geometry.
