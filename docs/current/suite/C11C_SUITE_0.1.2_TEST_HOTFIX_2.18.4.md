# C11-C Suite 0.1.2 — Test Hotfix 2.18.4

## Purpose

Correct two C11-C contract-test defects reported by the Windows batch runner.

## Repairs

### 1. Visual duration policy test

The test was still asserting the pre-CTA duration matrix:

- Tracking 24s gameplay / 30s total.
- Saccade 21s gameplay / 27s total.
- Pursuit 24s gameplay / 30s total.
- Peripheral Scan 21s gameplay / 27s total.

Current C11-C truth is:

- Tracking: 21s gameplay / 27s total / 810 frames.
- Saccade: 17s gameplay / 23s total / 690 frames.
- Pursuit: 17s gameplay / 23s total / 690 frames.
- Peripheral Scan: 17s gameplay / 23s total / 690 frames.

The declarative `profiles/presentation/c11c_visual_duration_policy.json` is aligned to that existing runtime contract. No mechanic or renderer was changed.

### 2. Longform source-artifact test

The new suite incorrectly inherited from `RefCounted`, so Godot refused to execute it with `--script`:

`Can't load the script ... as it doesn't inherit from SceneTree or MainLoop.`

It now inherits from `SceneTree`, uses `_initialize()` and exits explicitly with code 0/1.

## Scope boundary

No simulation, RNG, mechanic, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7 audio ownership or C9 authoring semantics were modified.

## Acceptance

```powershell
python .\c11c-suite\c11c-test\run_all.bat
python .\c11c-suite\c11c-test\run_suite.bat C11CVisualDurationPolicyContractTest.gd
python .\c11c-suite\c11c-test\run_suite.bat C11CVisualLoopLongformSourceArtifactContractTest.gd
```
