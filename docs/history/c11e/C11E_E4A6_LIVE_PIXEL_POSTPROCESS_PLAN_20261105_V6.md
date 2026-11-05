# C11-E E4A.6 Live Pixel Postprocess Plan — V6

## Purpose

Finish the existing Challenge 004 D-composited visual capture. Reuse the immutable AVI and, when validated, the silent MP4 already created by the first V3 attempt. No recapture.

## Pinned inputs

- V3 live-root receipt: `03e568bf78d442949c70495c946ab1995e07ee48b98db00fcc6efb729c7494fe`.
- E1 envelope: `d7f3814ef1bcce4719f59e4eab013ff6f650475a77f5d290d7f46c142f6914ec`.
- Movie Maker AVI: `135dae5c21e6a459cefce7a1bacafe5d4aeec0886b6acda88652de81515abf0b`.
- Active `GeneradorMaestro.gd` D-only postimage read-only pin: `d42782e8f5bb94ff0ede653a1c4624dc91541cc8203abf136b09a8fc288a7d82`.
- Frozen C11-C manifest: 796,318 bytes / SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

## V3 incident and V4 correction

V3 successfully encoded and FFprobe-validated the silent MP4, but boundary extraction failed because the operator's FFmpeg does not recognize `-vsync`. Its rerun then refused to overwrite that already-created file. V4 first validates an existing V4 MP4, then the V3 MP4, and reuses a valid match. If neither qualifies, it encodes to a temporary candidate, FFprobe-validates it, preserves any invalid prior output and promotes the verified candidate. Stills are extracted to a clean per-run workspace with `-fps_mode vfr`, checked as a complete eight-frame set and promoted as a set; the contact sheet is built from the staged frames.

## Output contract

- `CHALLENGE_004_D_LIVE_VISUAL_ONLY_720x1280_30FPS_SILENT.mp4`: H.264 High, 720x1280, 30 FPS, 450 frames, 15 seconds, `yuv420p`, `color_range=tv`, zero audio streams.
- Eight 720x1280 PNGs for delivery frames 0/89/90/299/300/389/390/449; source frame identity is delivery frame x2.
- Contact sheet 4x2, FFprobe JSON, PCM volume log, tool logs, output hashes and V4 receipt.

No runtime source writes, manifest rewrite, Git staging/commit, Godot, Movie Maker, D3 music generation or audio mux. Documentation installation is add-only and occurs only after media processing succeeds.
