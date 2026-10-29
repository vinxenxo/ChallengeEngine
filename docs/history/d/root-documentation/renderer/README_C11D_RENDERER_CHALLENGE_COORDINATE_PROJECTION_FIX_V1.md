# C11-D Coordinate Projection Preview — Godot Precision Fix V1

## Purpose

Fixes the Godot 4.7.1 false negative at the canonical parking target projection check. The transform is correct; the composed `4/3` delivery multiplication can produce a small single-precision float error in `Vector2`, which exceeded the prior `1e-6` comparison tolerance.

## Files

- `tools/c11d/d9/review_challenge_coordinate_projection_in_memory.gd`
- `tools/c11d/d9/test_d_renderer_challenge_coordinate_projection.py`

## Apply

Extract this ZIP at the repository root with `Expand-Archive -DestinationPath . -Force`.

## Verify

```powershell
python -m py_compile .\tools\c11d\d9\test_d_renderer_challenge_coordinate_projection.py
python .\tools\c11d\d9\test_d_renderer_challenge_coordinate_projection.py
godot --headless --path . --script res://tools/c11d/d9/review_challenge_coordinate_projection_in_memory.gd
```

The test contract remains `PROPOSED_NOT_APPROVED`; no renderer input, media, persistent report, or C11-C source mutation is introduced. The only numeric relaxation is for the composed delivery-space target position (`1e-4` pixel), with source and presentation-space coordinates still held to the tighter default tolerance. Failure messages now include the observed source/presentation/delivery positions.
