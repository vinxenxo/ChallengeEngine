# C11-C.1 — Geometric Waves v1 isolated prototype

Status: `PROTOTYPE_ONLY / READY FOR PHYSICAL EXPORT`

This overlay is intentionally outside `core/` and does not replace the frozen
`GeometricGenerator.gd` or `GeometricRenderer.gd`.

## Reference

- Seed: `314159`
- Canvas: `540x960`
- Body: `y=144..816`
- Duration: `10.0 s`
- FPS: `30`
- Frames: `300`
- Rendering mode: graphical Godot Compatibility renderer + Movie Maker
- External/AI visual assets: none

## Run in the real C11-B repository

From repository root:

```powershell
godot --path . --scene tools/prototypes/c11c_geometric_waves_v1/GeometricWavesPrototype.tscn `
  --write-movie artifacts/prototypes/c11c_geometric_waves_v1/GeometricWaves_v1_seed_314159.avi `
  --fixed-fps 30 `
  --quit-after 300
```

Package with FFmpeg:

```powershell
ffmpeg -y -hide_banner -loglevel error `
  -i artifacts/prototypes/c11c_geometric_waves_v1/GeometricWaves_v1_seed_314159.avi `
  -an -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p -movflags +faststart `
  artifacts/prototypes/c11c_geometric_waves_v1/GeometricWaves_v1_seed_314159.mp4
```

Preview GIF:

```powershell
ffmpeg -y -hide_banner -loglevel error `
  -i artifacts/prototypes/c11c_geometric_waves_v1/GeometricWaves_v1_seed_314159.mp4 `
  -vf "fps=30,scale=540:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=256[p];[s1][p]paletteuse=dither=sierra2_4a" `
  -loop 0 `
  artifacts/prototypes/c11c_geometric_waves_v1/GeometricWaves_v1_seed_314159.gif
```

Contract probe:

```powershell
ffprobe -v error -select_streams v:0 `
  -show_entries stream=width,height,r_frame_rate,nb_frames,duration `
  -of json `
  artifacts/prototypes/c11c_geometric_waves_v1/GeometricWaves_v1_seed_314159.mp4
```

Expected physical output: `540x960`, `30/1`, `300` frames, approximately `10.0 s`.

## Acceptance gate

No second implementation is authorized before the first physical GIF is visually reviewed.

The first review must answer:

1. Does it read as mathematical generative art rather than a screensaver?
2. Are the geometric lines sharp at 540x960?
3. Does the motion have transformation/intent rather than decorative rotation?
4. Does the composition remain comfortably inside Body?
5. Are the dominant/secondary/highlight relationships restrained?
6. Is the loop boundary perceptually invisible?
