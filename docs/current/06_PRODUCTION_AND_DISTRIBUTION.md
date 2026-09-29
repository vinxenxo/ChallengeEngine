# Production and Distribution — C11-C 2.19.5 Candidate

## Standard delivery

`MASTER_1080` is the default master: 1080×1920, 30 FPS, H.264/yuv420p with profile-defined GOP/encoder settings and AAC-LC 48 kHz stereo when audio is enabled.

## Capture versus delivery

- Historical Challenges keep their own canonical source/delivery boundary.
- Visual Loops/Drills review capture is 720×1280 @ 30 FPS.
- Delivery profiles may scale to 540×960, 720×1280 or 1080×1920 without changing simulation truth or logical social geometry.

## Single-Drill Producer route

```text
Movie Maker temporary AVI
    ↓
stable-file wait
    ↓
FFmpeg video-only silent source MP4
    ↓
FAMILY_MUSIC_V4 generated separately
    ↓
mux / profile delivery
    ↓
FINAL PRODUCT
```

Godot Movie Maker uses project-local `--path .`, no explicit `--resolution` on the proven single-Drill route, the canonical `VisualContentPlayer` scene, the resolved envelope, fixed 30 FPS and the resolved total frame count.

AVI is an implementation intermediate only. OGV/PNG routes are historical and superseded.

## Art Direction review concurrency

The review batch uses temporary per-worker project roots. Each concurrent worker owns its own `override.cfg` and `.godot` state. The project-global mutex experiment from 2.19.3-v2 is not part of the current design.

## Social copy / hook source

Visual Drill social hooks are read from `profiles/presentation/c11c_visual_hooks.json` and selected deterministically. `authoring.json.content.hook` is not a valid live contract field.

## Artifact policy

Durable products and evidence belong under `artifacts/`. Scratch AVI and temporary worker roots are not source truth.
