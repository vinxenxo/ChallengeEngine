# Production and Distribution — Current

## Frozen C11-C review profile

- MP4
- 720×1280
- 30 FPS fixed
- H.264 / yuv420p
- family-aware deterministic audio
- AVI temporary by default
- GIF opt-in

The frozen review profile is intentionally not the final Meta Reels delivery profile.

## Meta final profile

A separate `META_REELS_FINAL_V1` target is documented for the next delivery layer: 1080×1920, 30 FPS for C11-C visual content, H.264, yuv420p, explicit closed GOP, AAC-LC, 48 kHz stereo.

This profile is additive and does not rewrite the frozen 2.16 manufacturing profile.

## Artifact policy

Generated video/audio belongs under `artifacts/`. Intermediate AVI is temporary unless explicitly retained. Historical review output is evidence and is not silently replaced by a later render.
