# C11-C 2.3.0 — Tracking Mechanic Baseline

## Scope

This release starts the family-specific mechanic refinement phase with `visual_drill/tracking`.

## Mechanical changes

- Replaced static target coordinates with a deterministic bounded Lissajous 2:3 trajectory.
- One active target only; canonical distractor set is empty.
- Emits target position and velocity as frame state.
- Emits short history-only trajectory trail; future path is never exposed.
- Supports constant pacing plus smooth `accelerating` and `pulsed` phase-rate modulation.
- Keeps trajectory entirely inside the logical Body with explicit clearance.
- Cosmetic `tracking_variant` no longer alters mechanic truth.

## Presentation changes

- Tracking renderer now consumes emitted trajectory/target state directly.
- Procedural target is visually dominant.
- Short luminous history trail and quiet mathematical operating field support trajectory clarity without showing future motion.
- No external/new raster asset is introduced in this mechanic phase; robust asset treatment remains open for a later art review.

## Regression coverage

- Added `C11CTrackingMechanicContractTest.gd`.
- Updated `C6F08TrackingPlaybackValidationTest.gd` from shader-specific assertions to state-level tracking assertions.
- Registered the new suite in `tests/run_all.py`.

## Frozen boundaries

No changes to challenge simulation, `SimulationResult`, `winning_frame`, `close_calls`, structural RNG ownership, C7 audio contracts, C9 authoring contracts or C11-B logical social geometry.
