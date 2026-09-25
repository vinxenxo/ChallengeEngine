# C11-C CHANGELOG — v2.10.0

> HISTORICAL / REJECTED CHECKPOINT: workstation validation found a shared C11-C presentation compilation defect. See `CHANGELOG_C11-C_2.10.1.md` for the repair.

## Scope

C11-C presentation/audio foundation refinement after the full 2.9.1 Visual Drill corpus reached green status. No frozen C11-B simulation truth, C7 ownership, C9 authoring contracts, or gameplay mechanics were reopened.

## 2.10.0 changes

### CTA / footer residual surface
- The Visual Drill END_CTA remains Header-owned.
- The shared FooterRegion remains visible during END_CTA so telemetry text stays on screen.
- The stale success `WinningHighlightComponent` is restricted to `GAME` presentation phase, preventing a residual rectangular game highlight from appearing during END_CTA.
- Social sidecars now declare `FOOTER DURING CTA: VISIBLE`.

### Typography foundation
- Replaced the previous single-font C11-C Courier utility with role-based shared typography.
- Header: Inter Bold.
- Footer: Noto Sans Mono Regular.
- Legacy C6 Comic Sans/Courier assets are intentionally retained only for their historical contracts.
- All current Visual Loop prototypes continue through the common C11-C editorial layer.

### Palette bank expansion
- Expanded each Visual Drill semantic palette bank from 18 to 24 authored worlds.
- Added six new chromatic combinations per family so seed variation has a larger color vocabulary.
- Selection logic is unchanged; the change is presentation-only.

### Family-aware music
- Introduced `FAMILY_MUSIC_V3`.
- Added five semantic music profiles with deterministic seed/family variation.
- Paired Drill/Loop identities share a musical profile: Tracking/Invisible Forces, Saccade/Geometric Waves, Pursuit/Fractal Bloom, Peripheral Scan/Sacred Symmetry.
- Preserved a PRISMATIC_MEMORY profile for the historical Kaleidoscope route.
- Removed dependency on one global ambient master from the active Drill/Loop production path.
- Kept C7 ownership untouched.

### Delivery metadata
- Visual Drill and Visual Loop manifests declare typography roles and music profile IDs.
- Social sidecars declare active family music mode/profile and font roles.
- Added a dedicated music binding regression suite.

## Validation intent

Closure is not claimed from source edits alone. Required validation remains the existing focused C11-C suites, full `tests/run_all.py`, and physical render review on the project workstation.


## 2.10.0-r1 — Closure repair after Windows runtime validation

- Restored the shared editorial measurement constant `HEADER_BOLD_EMBOLDEN` accidentally omitted while separating header/footer font roles.
- Corrected the Saccade jump counter to explicitly use the footer typography role required by the C11-C typography contract.
- Extended the typography contract test to load and instantiate `C11CVisualEditorialLayer`, preventing a presentation-layer parse failure from escaping the focused typography suite.
- No simulation, authoring, RNG, `SimulationResult`, `RenderedFrameStream`, `WinningFrameDetector`, C7 audio ownership or C9 authoring contract was changed.
