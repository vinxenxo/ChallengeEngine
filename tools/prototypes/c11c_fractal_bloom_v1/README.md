# C11-C.2 — Fractal Bloom v1 Prototype

Isolated radial prototype for the `VisualLoop / fractal` family.

## Artistic target

**Bioluminescent mycelium / neural synapses / microscopic infinite universe.**

The structure is procedural: dynamic Julia iteration + orbit traps + domain warping + analytical periodic zoom. No visual PNG/JPG assets are used.

## Reference

- seed: `314159`
- canvas: `540×960`
- body: `y=144..816`
- fps: `30`
- duration: `10.0 s`
- exported frames: `300`
- depth layers: `3`

## Run

From the project root:

```powershell
.\tools\prototypes\c11c_fractal_bloom_v1\run_prototype.ps1
```

Expected artifacts:

```text
artifacts/prototypes/c11c_fractal_bloom_v1/
  FractalBloom_v1_seed_314159.mp4
  FractalBloom_v1_seed_314159.gif
  FractalBloom_v1_seed_314159_music.wav
  FractalBloom_v1_seed_314159_ffprobe.json
  FractalBloom_v1_seed_314159_manifest.json
  FractalBloom_v1_seed_314159_godot.log
```

The audio layer is prototype-only. It does not modify C7.

## Review rule

This package is not a productive integration. The first physical GIF/MP4 is the visual review surface. Do not create a second artistic implementation before reviewing it.
