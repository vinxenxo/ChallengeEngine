# C11-C 2.7.0 — Visual Drill Terminal Self-Evaluation CTA

## Status

Implemented as an additive presentation revision on top of C11-C 2.6.0. No frozen C11-B simulation boundary is changed.

## Shared Visual Drill presentation

Added the reusable `VisualDrillPresentationPhaseLogic` companion to the existing `CountdownPresentationLogic`.

Effective presentation order:

```text
PRE_ROLL 3s → GAME canonical stream → END_CTA 3s
```

The terminal phase is presentation-only. The gameplay `RenderedFrameStream` remains unchanged and is frozen before the terminal phase starts.

## Reuse of Challenge CTA

Visual Drills now reuse the existing Challenge `CTAComponent` through `PresentationUI` rather than creating a second CTA implementation.

Terminal copy:

```text
¿LO CONSEGUISTE?
¿HASTA DÓNDE LLEGASTE?
```

A small deterministic entry motion is controlled by terminal-phase progress. This is presentation-only.

## Current durations

| Family | Gameplay | Countdown | End CTA | Total | @30 FPS |
|---|---:|---:|---:|---:|---:|
| Tracking | 21s | 3s | 3s | 27s | 810 |
| Saccade | 17s | 3s | 3s | 23s | 690 |
| Pursuit | 17s | 3s | 3s | 23s | 690 |
| Peripheral Scan | 17s | 3s | 3s | 23s | 690 |

The 20–30 second Visual Drill presentation contract remains enforced.

## Editorial / palette application

Tracking and Saccade palette colors are now applied visibly to:

- header text;
- footer telemetry;
- separator rules;
- social section backgrounds;
- terminal CTA main/sub text.

The palette source remains deterministic and presentation-only.

## Review/export pipeline

`run_c11c_visual_drill_review.ps1` now accounts for the extra 3-second terminal CTA in `--quit-after`, frame-count validation, duration validation, manifests and social sidecars.

The shared review audio master is generated for 27 seconds so the longest Visual Drill presentation is fully covered.

## Audio direction

Added `docs/c11/C11-C_VISUAL_DRILL_AUDIO_DIRECTION_v1.0.md` as the next-pass sonic specification. The current generator remains shared, deterministic and mobile-safe; no family-specific audio ownership is introduced.

## Pursuit handoff

Added `docs/c11/C11-C.8_PURSUIT_ART_DIRECTION_v1.0.md` capturing the approved next-family direction:

- uniform cubic B-spline path;
- arc-length parameterization;
- complex monolith/tesseract/gyroscope target;
- radial depth-of-field presentation;
- exact sizygia count in authoring data;
- deterministic seed-driven event schedule.

No Pursuit gameplay implementation is part of 2.7.0.

## Regression coverage

Added and registered:

`tests/C11CVisualDrillEndCTAContractTest.gd`

Updated duration/playback contracts:

- `C11CVisualDrillCountdownContractTest.gd`
- `C11CVisualDrillSocialPresentationContractTest.gd`
- `C6F06VisualDrillPlaybackTest.gd`
- `C6F08TrackingPlaybackValidationTest.gd`
- `C6F08SaccadePlaybackValidationTest.gd`

## Frozen boundaries preserved

No changes to:

- simulation mathematics;
- `SimulationResult`;
- `winning_frame`;
- `close_calls`;
- `WinningFrameDetector`;
- `RenderedFrameStream` mechanics;
- structural RNG ownership;
- C7 audio contract ownership;
- C9 authoring schema contract;
- C11-B 540x960 Header/Body/Footer geometry.
