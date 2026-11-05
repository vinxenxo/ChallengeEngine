# C11-E Execution Backlog — V36

**Date:** 2026-11-05.

## Immediate task — finish E4A.6 postprocess without recapture

Run `RUN_C11E_E4A6_LIVE_PIXEL_POSTPROCESS_V4.ps1` from Downloads. Reuse the already captured AVI with SHA `135dae5c21e6a459cefce7a1bacafe5d4aeec0886b6acda88652de81515abf0b`; do not rerun Godot or Movie Maker.

V1 had a 63-character manifest-SHA typo. V2 surfaced an empty process ExitCode at SOURCE_FFPROBE. V3 fixed the process wrapper and successfully reached boundary-still extraction, but the operator's FFmpeg rejected `-vsync`. V3 therefore left a generated silent MP4 in `review_delivery\POSTPROCESS_V3`, then the next V3 run blocked rather than resuming because that MP4 already existed. V4 specifically handles this: FFprobe-revalidate and reuse the V3 MP4 when it matches the expected media contract; otherwise encode to a temporary candidate, validate it, and preserve invalid prior output before promotion. Extract stills using `-fps_mode vfr`, with no `-vsync`, into a fresh temporary directory and promote the complete eight-frame set only after count validation.

Essential invariants remain:
- Windows PowerShell 5.1 AST parse; process logs and concrete exit codes.
- Frozen manifest 796,318 bytes / SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- `GeneradorMaestro.gd` read-only pin `d42782e8f5bb94ff0ede653a1c4624dc91541cc8203abf136b09a8fc288a7d82` before/after.
- V3 live-root receipt, E1 envelope and Movie Maker semantic markers/telemetry.
- Exact AVI SHA; source FFprobe 540x960/60 FPS/900 frames/15s; PCM only discarded after <= -90 dB mean and peak measurement.
- Silent review MP4 H.264 High, 720x1280/30 FPS/450 frames/15s, `yuv420p/tv`, zero audio streams; eight stills and contact sheet.
- Add-only versioned docs; no runtime source edit, manifest rewrite, Git mutation, D3, mux, Godot or Movie Maker.

## After postprocess

Resolve the `GeneradorMaestro.gd` frozen-manifest source-path divergence before any further runtime patch. Then run full E4A A/V using the normalized D-composited MP4 as the video source; reuse the accepted E4A.4 D3 V5/D3.3 mastering/mux/FFprobe contract, preserve independent gameplay/music seeds, same-seed A/B and changed-music-seed C, same video elementary stream, AAC 48 kHz stereo, non-silent audio and A/V drift <=0.15s. Operator listening/visual review and GUI/CLI parity remain mandatory.

## Held roadmap

E4B Loop -> E4C Drill -> E5 determinism/seed isolation/family isolation/GUI-CLI parity -> E6 Smoke18 -> E7 Matrix101 (54+27+20; CH_008/009 held pending 11s/12s resolution) -> E8 full regression map, independent acceptance, freeze and separate promotion.

## Invariants

C11-C 2.19.12 frozen artifact and manifest remain untouched. No mechanics/RNG/simulation-truth changes. No sixth Suite module, parallel producer or binder. `request.seed` and `request.music_seed` stay independent; automatic seed generation disabled. Production renderer/dispatch/media OFF; `release_authority=NONE`.
