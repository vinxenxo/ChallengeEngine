# C11-D Unified Content Review Fix V5 — float-safe target projection guard

Minimal overlay for `ChallengeEngineV01_STATELESS`. Fixes the canonical target-position guard in the coordinate-projection preview. It does not change coordinate mapping, simulation outputs, frame selection, delivery policy, renderer state, or governance.

## Root cause

`CoordinateMapper.map_position` returns a `Vector2`. The final delivery position is therefore represented at Godot's `Vector2` component precision, while the expected scalar `850.0 * 2.0 / 3.0` is evaluated as a higher-precision scalar. The x-coordinate can differ by approximately `2e-5` pixels, larger than the previous `1e-6` epsilon. The valid projection was rejected by an over-strict floating-point comparison.

The fix retains `1e-6` checks for the exact source-to-presentation coordinates and uses a still sub-pixel `1e-4` tolerance only for the final delivery `Vector2`. If the guard fails again, it prints source, presentation, delivery, and expected coordinates for diagnosis.

## Apply

Run from the repository root:

```powershell
Expand-Archive `
  -LiteralPath "$env:USERPROFILE\Downloads\C11D_RENDERER_UNIFIED_CONTENT_REVIEW_FIX_V5.zip" `
  -DestinationPath "." `
  -Force
```

## Validate

```powershell
python -m py_compile `
  .\tools\c11d\d9\d_renderer_unified_content_review.py `
  .\tools\c11d\d9\test_d_renderer_unified_content_review.py
python .\tools\c11d\d9\test_d_renderer_unified_content_review.py
python .\tools\c11d\d9\run_d_renderer_unified_content_review.py --godot godot
```

The coordinate-projection harness should now pass its canonical target guard. Overall acceptance is still pending until the unified coordinator reports PASS. The allowed governance state remains `renderer=OFF`, `media_created=false`, `D4.8=BLOCKED`, and `release_authority=NONE`. This overlay does not authorize video creation.
