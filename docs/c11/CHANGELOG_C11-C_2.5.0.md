# C11-C 2.5.0 — Tracking presentation refinement + Saccade mechanic foundation

## Tracking

- Fixes the tracking presentation contract to recognize growing history support.
- Extends Tracking gameplay to 21 s; combined with the common 3 s pre-roll, total presentation is 24 s.
- Keeps the analytic bounded Lissajous 2:3 trajectory and existing difficulty tiers.
- Reuses the existing Living Particles perspective Tron road implementation instead of duplicating a second road renderer.
- Separates full-width Body underlay, Tron road, history trail and explicit Z=100 target layer.
- Adds six deterministic, mobile-safe high-contrast Tracking palette families.
- Makes trail fade explicitly time-based while retaining growing history behavior.

## Saccade

- Replaces the legacy static/linear presentation baseline with a deterministic polar golden-angle endpoint sequence.
- No spatial interpolation between endpoints.
- Adds APPEAR / IDLE / VANISH state machine with scale/opacity/flash presentation.
- Guarantees 180–300 px jump distances in the baseline.
- Random/polar baseline has no decorative background.
- Adds dedicated mechanic and presentation contracts.
- Updates playback validation to state-level checks with watchdog and pre-roll validation.

## Common drill pipeline

- Visual Drills are hard-bounded to 20–30 s total including the shared 3 s countdown; playback rejects definitions outside this envelope.
- Tracking uses 24 s total; the other canonical drills remain 20 s for this phase.
- Review audio master is extended to 24 s and remains common/deterministic.

## Frozen boundaries

No changes to C11-B simulation mathematics, RNG ownership, SimulationResult, winning_frame, close_calls, C7 audio contracts, C9 authoring contracts or frozen logical 540x960 geometry.

## Review tooling

`run_c11c_visual_drill_review.ps1` now accepts `-Families` to review one or more drill families while preserving the default four-family matrix. This supports focused Tracking variation reviews without running unrelated families.

## 2.5.0 pre-roll validation hotfix
- Corrected the Saccade playback test to inspect PRE_ROLL after the first rendered presentation frame instead of before renderer state was applied.
