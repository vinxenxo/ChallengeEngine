# C6-E4 — Runtime Integration

## Baseline

`1.2.0-C6-F-F1.1-DELTA-FIX4` with the E4 component already present.

## Runtime contract

The winning highlight is presentation-only.

- `SimulationResult`, `WinningFrameDetector`, RNG and mechanic math are untouched.
- `winning_frame_game` remains the already-certified game-relative winning frame.
- `WinningHighlightComponent` receives only visual `Rect2` bounds.
- Bounds are obtained after `apply_frame_snapshot()` has positioned the sprites for the current render frame.
- The highlight is visible only when `state == "GAME"` and `ui_state_frame == winning_frame_game`.
- Therefore the intended temporal behavior is exactly:
  - winning frame - 1: OFF
  - winning frame: ON
  - winning frame + 1: OFF

## Geometry

`GeneradorMaestro.build_winning_highlight_rects()` derives axis-aligned presentation bounds from the already-rendered `object_sprite` and `target_sprite`.

No collision, tolerance, distance, angle, seed, simulation state, or winning-frame calculation is performed by E4.

## Validation

Run:

```powershell
godot --headless --path . --editor --quit
godot --headless --path . --script tests/C6E4WinningHighlightContractTest.gd
python .\tests\run_all.py
```

Then render at least one real challenge:

```powershell
python build_factory.py --config ./challenges/CHALLENGE_001.json --output ./output_e4
```

Inspect `output_e4/CHALLENGE_001/CHALLENGE_001.gif` or the MP4 and verify that the green frame appears for exactly one source frame at the winning point.

## Certification status

This delta is **E4 runtime integration work in progress** until the real video is visually verified and the complete regression/batch suite passes on the user's Godot environment.
