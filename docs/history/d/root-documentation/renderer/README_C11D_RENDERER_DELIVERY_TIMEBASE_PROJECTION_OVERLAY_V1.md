# C11-D Renderer Delivery Timebase Projection Overlay V1

This ZIP is a minimal overlay for `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`.

## Package SHA-256

`See the expected SHA-256 in the assistant handoff; do not infer it from this README.`

## Apply

```powershell
cd C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS
Get-FileHash "$env:USERPROFILE\Downloads\C11D_RENDERER_DELIVERY_TIMEBASE_PROJECTION_OVERLAY_V1.zip" -Algorithm SHA256
Expand-Archive -LiteralPath "$env:USERPROFILE\Downloads\C11D_RENDERER_DELIVERY_TIMEBASE_PROJECTION_OVERLAY_V1.zip" -DestinationPath "." -Force
```

## Focused validation

```powershell
python -m py_compile `
  .\tools\c11d\d9\d_renderer_delivery_timebase_projection.py `
  .\tools\c11d\d9\test_d_renderer_delivery_timebase_projection.py
python .\tools\c11d\d9\test_d_renderer_delivery_timebase_projection.py
```

Expected summary: `content_types=3/3`, `deterministic=3/3`, `source_lineage=3/3`, `frame_ranges=3/3`, `negative=42/42`, `schema=3/3`, and `jsonschema=3/3` when the optional validator is installed. It reports Challenge 900@60 FPS → 450@30 FPS using boundaries 90/210/90/60. This remains a review-only proposed policy.

Then run the existing focused regression scripts and aggregate suite listed in the conversation. The existing 22-step aggregate is not changed by this overlay.

## Safety/governance boundary

The proposal writes no output during execution and makes no renderer calls. It does not solve simulation sampling, interpolation, event anchors, audio resampling or per-field visibility timing; it is not video-render-ready. C11-C and its frozen manifest stay immutable. Adapter `PREPARE_ONLY`, renderer OFF, media false, D4.8 BLOCKED, release authority NONE, D9 OPEN, D10 BLOCKED.
