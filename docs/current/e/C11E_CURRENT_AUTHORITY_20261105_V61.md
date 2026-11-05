# C11-E Current Authority — V61

**Date:** 2026-11-05. Supersedes V60 for the V3 postprocess incident and corrected V4 recovery path. Earlier evidence remains immutable.

## Working checkout and baseline identity

The sole working checkout is `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. Never extract a snapshot/evidence ZIP over it. The operator controls local commits; no runner may stage, commit, reset, clean, switch branches, rebase, amend or push.

The canonical C11-C 2.19.12 freeze manifest is 796,318 bytes with SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

## C11-C source-manifest distinction — `GeneradorMaestro.gd`

The frozen C11-C manifest pins the original 36,991-byte `GeneradorMaestro.gd` at SHA-256 `4f10144c62c7bc149bd46aa37494b1df40c7185544b8477153150eec71c1aaf9`. The active D-only postimage is `d42782e8f5bb94ff0ede653a1c4624dc91541cc8203abf136b09a8fc288a7d82`. The frozen manifest/artifact remain unchanged, but the active worktree does not byte-match this manifest entry. Do not edit or restore this file blindly. A separate source-isolation decision is required before further runtime changes. The postprocess runner only reads/hashes this file.

## E4A.6 accepted test-only evidence

- Live-root receipt SHA: `03e568bf78d442949c70495c946ab1995e07ee48b98db00fcc6efb729c7494fe`; 17/17 focused tests; Godot 4.7.1; 900 frames; one shared layer mount; D header 180 frames; D footer 120 frames; native CTA owner 0; production dispatch/media/release false.
- Existing Movie Maker AVI SHA: `135dae5c21e6a459cefce7a1bacafe5d4aeec0886b6acda88652de81515abf0b`; 540x960, 60 FPS, 900 frames, 15 seconds. The configured marker, 180/420/180/120 phase telemetry, disabled audio export and recording-completion markers are present. No Movie Maker/Godot rerun is needed.
- The AVI contains a PCM S16LE stereo 48 kHz stream near -91 dB. It is not D3 music and must be excluded from the silent visual-review MP4.

## Postprocess incidents and current correction

- V1 stopped before work because its expected manifest SHA was 63 characters (missing `58`).
- V2 stopped at `SOURCE_FFPROBE` with an empty wrapper `ExitCode` and empty stderr; this did not establish an FFprobe diagnostic failure.
- V3 fixed process invocation/exit-code capture and progressed through source FFprobe, PCM measurement, silent H.264 encode and review-MP4 FFprobe. The first V3 attempt then failed at `BOUNDARY_STILLS`: the user's FFmpeg rejected the legacy `-vsync` option (`Unrecognized option 'vsync'`). The resulting MP4 remained in `review_delivery\POSTPROCESS_V3`. A subsequent V3 rerun correctly refused to overwrite that existing MP4, but did not resume from it. V3 therefore has no complete postprocess receipt and is not PASS.
- V4 reuses the exact captured AVI and revalidates the pre-existing V3 MP4 by FFprobe before reuse. If that MP4 is absent or fails the required video contract, V4 produces a candidate in its evidence directory, verifies it, then promotes it while preserving any invalid prior output in the evidence folder. Boundary extraction uses `-fps_mode vfr` and does not use `-vsync`. Stills are generated in a fresh per-run working directory and promoted only after all eight are present. Repeated runs can reuse a valid V4 MP4 and regenerate the stills without colliding with partial output.

The V4 output contract remains H.264 High, 720x1280, 30 FPS, 450 frames, 15 seconds, `yuv420p`, limited `tv` range and zero audio streams; eight boundary PNGs correspond to delivery frames 0, 89, 90, 299, 300, 389, 390 and 449.

## Current phase disposition

- E4A.6 live-root consumer: `PASS_TEST_ONLY`.
- E4A.6 Movie Maker capture: `PASS_TEST_ONLY_CAPTURED`.
- E4A.6 postprocess V1: `BLOCKED_BEFORE_WORK` (runner SHA literal typo).
- E4A.6 postprocess V2: `BLOCKED_AT_SOURCE_FFPROBE` (wrapper ExitCode observation defect).
- E4A.6 postprocess V3: `BLOCKED_AT_BOUNDARY_STILLS` (unsupported `-vsync` option); its already-produced MP4 is retained and will be revalidated/reused by V4. No complete V3 receipt exists.
- E4A.6 postprocess V4: package prepared; Windows execution remains pending. No claim of PASS until the receipt is produced.
- Operator visual feedback: no obvious defect reported. General D1.5/D1.1/D1.7 geometry/safe-area approval remains `NOT_GRANTED`.
- E4A final D-composited A/V remains pending D3 V5/D3.3 generation, mux/FFprobe, seed A/B/C isolation, listening/sync and GUI/CLI parity.
- E4B Loop and E4C Drill remain HELD until full E4A closes.

## Next ordered work

1. Run `RUN_C11E_E4A6_LIVE_PIXEL_POSTPROCESS_V4.ps1` once. It must reuse/revalidate the existing V3 MP4 when valid, extract the eight stills with `-fps_mode vfr`, create the contact sheet and install the included documentation add-only. Do not rerun Godot or Movie Maker.
2. Resolve the `GeneradorMaestro.gd` C11-C manifest divergence as a separate source-isolation decision before further runtime changes.
3. Complete the D-composited Challenge A/V test using D3 V5/D3.3 and the accepted E4A.4 mux/FFprobe contract.
4. Only after full E4A acceptance proceed to E4B Loop, E4C Drill, E5, E6 Smoke18, E7 Matrix101 and E8 independent acceptance/freeze/separate promotion.

CH_008/CH_009 remain held: declared 11 seconds versus 12 seconds phase sum (3+7+0+2).

## Governance

C11-C 2.19.12 remains the only production-authoritative frozen artifact. Production renderer OFF, production dispatch OFF, production media OFF. D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`. No Git mutation by runners.
