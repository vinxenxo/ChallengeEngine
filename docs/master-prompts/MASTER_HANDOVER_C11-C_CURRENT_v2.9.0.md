# MASTER HANDOVER — C11-C CURRENT v2.9.0

## Baseline authority

Use the sealed C11-B repository freeze plus the active C11-C source tree through **2.9.0**.

Do not reopen C11-B simulation mathematics, RNG ownership, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7 contracts or C9 frozen authoring semantics.

## Current Visual Drill families

```text
tracking
saccade
pursuit
peripheral_scan
```

## Presentation envelope

- 540×960 logical
- 720×1280 physical
- 30 FPS
- 3 s PRE_ROLL
- gameplay: Tracking 21 s / others 17 s
- 3 s END_CTA
- CTA in Header
- entire FooterRegion hidden during END_CTA

## Current shared utilities

- `C11CVisualTypography.gd`
- `C11CDrillEnvironment.gd`
- `C11CDrillPaletteBank.gd`
- `VisualDrillPresentationPhaseLogic.gd`
- common `CTAComponent`

## Seed rules

Seeded mechanical variation is authored in `VisualDrillSeedVariation/2.9.0`. Renderer variants remain presentation-only.

## Pursuit

Use authored uniform cubic B-spline + arc-length LUT + emitted frame state. Sizygia count and exact event frames are part of `authoring.json.answer_sheet`.

## Peripheral Scan

Use authored polar/logistic event schedule. Threat/distractor count and exact frame starts are part of `authoring.json.answer_sheet`.

## Audio

Use one global `drill_motion_ambient_v2` master for Visual Drill review. Do not use family-specific event-locked music unless a separate C11-C checkpoint defines it.

## Social output

Every physical review render must emit `VisualDrill_<family>_seed_<seed>_social.txt` and fail closed when the sidecar is absent.

## Current gate

2.9.0 is a candidate working state. Final status must be based on runtime/physical validation in Godot 4.7.1, not on static construction alone.
