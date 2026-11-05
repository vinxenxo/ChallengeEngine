# C11-E E4A.6 Live Pixel Capture and Postprocess — Postmortem V4

**Date:** 2026-11-05.

## Capture disposition

Movie Maker completed successfully. Its stdout contains the start marker, `C11E_E4A6_LIVE_CONSUMER_CONFIGURED` with success=true, expected envelope SHA, 900 source frames, phase telemetry HOOK/GAME/REVEAL/CTA = 180/420/180/120, audio export disabled, recording completion and 900 frames at 60 FPS. The captured AVI SHA is `135dae5c21e6a459cefce7a1bacafe5d4aeec0886b6acda88652de81515abf0b`. No recapture is required.

## Earlier runner incidents

- V1 had a malformed 63-character manifest SHA and stopped before work.
- V2 corrected the SHA but surfaced an empty process ExitCode at SOURCE_FFPROBE; stderr was empty, so no FFprobe diagnostic failure was established.
- V3 replaced the process wrapper with `.NET System.Diagnostics.Process`. The first V3 run passed source FFprobe, measured the known near-silent PCM track, encoded the silent H.264 MP4, and passed the MP4 FFprobe contract. It then failed at `BOUNDARY_STILLS` because the operator's FFmpeg rejected `-vsync` (`Unrecognized option 'vsync'`). The second V3 run refused to overwrite the MP4 created by the first attempt. The MP4 is retained; V3 has no complete receipt and is not PASS.

## V4 recovery behavior

V4 validates the existing V3 MP4 with FFprobe and reuses it when its contract matches: one H.264 High video stream, 720x1280, 30 FPS, 450 frames, 15 seconds, `yuv420p`, `tv` range, no audio. If that output is absent or invalid, V4 encodes a temporary candidate from the pinned AVI, verifies the candidate, and only then promotes it; an invalid prior file is preserved in the run evidence. V4 extracts the eight selected frames with `-fps_mode vfr`, not `-vsync`, into a fresh per-run workspace, checks that all eight exist, and only then copies them to the delivery directory. A contact sheet is generated from that staged frame set. This makes the postprocess resumable without repeating capture or destructively overwriting an unverified video.

The source PCM stream is discarded only after exact codec/rate/channel checks and volume measurement at <= -90 dB mean and peak. The final review MP4 must contain zero audio streams. No Godot, Movie Maker, D3, mux, producer or source-code write occurs.

## Remaining limits

A successful V4 receipt proves the technical media postprocess only. It does not grant formal visual/layout approval, source isolation, D3 integration, mux acceptance, production dispatch, release, freeze or promotion. `GeneradorMaestro.gd` remains a D-only postimage divergent from the frozen C11-C manifest entry; resolve that boundary separately before further runtime edits.
