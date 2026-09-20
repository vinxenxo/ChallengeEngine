# C11-C.1 — Geometric Waves v1 isolated prototype

**Prototype overlay revision: C11C v1.0.2.**

Status: `PROTOTYPE_ONLY / READY FOR PHYSICAL EXPORT`

This overlay is intentionally outside `core/` and does not replace the frozen
`GeometricGenerator.gd`, `GeometricRenderer.gd`, `RenderedFrameStream`, C7 or
C9 contracts.

## What changed in v1.0.2

### Social frame editorial layer

The existing C11-B `UnifiedSocialFrame` is still the structural owner. The
prototype now populates:

- Header: `VISUAL LOOP // GEOMETRIC WAVES` + `CUANDO LAS ONDAS DIBUJAN GEOMETRÍA`
- Footer: equation, polygon order, Lissajous ratio, layer count, seed, body size,
  frame rate and duration.

No C11-B geometry is redefined.

### Audio

The prototype now creates a deterministic 10-second stereo music bed locally
from `generate_geometric_waves_music.py`, then muxes it into the final MP4.
This is deliberately prototype-only and does not modify the frozen C7 audio
contracts or core audio code.

The GIF remains silent by nature.

## Run

From the repository root:

```powershell
.\tools\prototypes\c11c_geometric_waves_v1\run_prototype.ps1
```

Expected final assets:

- `GeometricWaves_v1_seed_314159.mp4` — video + procedural audio
- `GeometricWaves_v1_seed_314159.gif` — silent visual review
- `GeometricWaves_v1_seed_314159_music.wav` — deterministic source music
- `GeometricWaves_v1_seed_314159_ffprobe.json` — final A/V probe
- `GeometricWaves_v1_seed_314159_manifest.json` — prototype manifest

The physical render remains the review authority; technical PASS does not
constitute artistic acceptance.
