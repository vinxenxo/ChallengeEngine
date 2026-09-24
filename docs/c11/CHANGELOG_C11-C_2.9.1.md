# C11-C 2.9.1 — Visual Drill Runtime Dependency Hotfix + Phase Closure

## Status
Hotfix over C11-C 2.9.0. No gameplay truth, authoring contracts, seed semantics, CTA timing, audio contract, or visual-family mechanics changed.

## Root cause
`PeripheralScanRenderer.gd` referenced `_environment` in presentation code without declaring an instance variable. Godot 4.7.1 therefore failed to parse the renderer. Because `VisualDrillRenderer` depends on all visual-drill renderers, this single parse error cascaded into Tracking, Saccade, Pursuit and Visual Loop playback suites in the aggregate runner.

## Fix
- Declare `_environment` as a `Node2D` instance owned by `PeripheralScanRenderer`.
- Instantiate it eagerly so the renderer can safely use it during presentation setup/draw lifecycle.
- Do not change the authored Peripheral Scan schedule, anchor, threat/distractor truth, seed mapping, or palette selection.

## Validation intent
After applying this hotfix the expected regression state is:
- C11-C Visual Drill contract suites: PASS.
- C6F playback/pilot suites: PASS with no `SCRIPT ERROR`.
- `python tests/run_all.py`: PASS with zero failing suites.

## Phase closure
C11-C Visual Drills now contains the four families:
- Tracking — seeded trajectory variation, history trail, mobile-safe presentation.
- Saccade — discrete jumps, jump counter, seeded spatial variation.
- Pursuit — authored cubic B-spline with arc-length parameterization, sizygia answer sheet, foveal-load presentation.
- Peripheral Scan — polar orbital schedule, threat/distractor answer sheet, central anchor and flare presentation.

Common presentation includes countdown, terminal self-evaluation CTA in Header, shared typography, social sidecar generation, shared ambient audio master and semantic palette infrastructure.
