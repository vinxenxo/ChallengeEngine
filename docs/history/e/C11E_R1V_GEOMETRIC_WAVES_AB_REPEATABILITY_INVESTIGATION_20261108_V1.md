# C11-E R1V — Geometric Waves A/B Repeatability Investigation V1
**Date:** 2026-11-08  
**Status:** OPEN — `FAIL_CLOSED_PIXEL_NONDETERMINISM_GEOMETRIC_WAVES`  
**Scope:** Read-only investigation of the latest bounded R1V A/V run. This document is not an acceptance receipt and does not authorize new rendering, source changes, or promotion.

## Executive result

The current active R1V attempt is `Q5_040414_B6BE4D`. The integrated wrapper's 52-test gate passed 52/52 with zero skips, errors, or failures. The integrated audiovisual stage completed all ten slots: ten source inventories, ten native-family music generations, ten AAC muxes, nine fresh C11-C source launcher invocations, and one reuse of the previously accepted Fractal Bloom A capture. The run then correctly failed closed on the Geometric Waves A/B pixel-determinism assertion.

The failure is narrowly isolated to `c11c_geometric_waves_v1` / `harmonic_membrane`:

- 690/690 frames and their PTS sequence match structurally; no integer-frame offset (±3) improves pixel similarity.
- Exact per-frame pixel-hash matches: 0/690; global decoded pixel-stream SHA-256 differs.
- Both A/B inputs have identical authoring JSON bytes, grammar, gameplay seed `100001`, duration 23 s, 30 fps, 690 frames, three loop cycles, palette, and style parameters.
- The music seed is `500001` in both repeats and remains distinct from gameplay seed. WAV/PCM and AAC elementary-stream digests match A/B.
- A/B source MP4 SHA-256 values differ: A `b7b841ed48b9ac28bdfa28bed63ab398ebaa611bc5cfabe9dddd0e33dc249eca`; B `a0225d0292f4bea8e13007cc05d5c694bde58687c20fa1ceb281c646e8faac7f`.
- Four other family pairs are exact A/B matches: Fractal Bloom (660 frames), Invisible Forces (660), Living Particles (600), Sacred Symmetry (690).

Read-only pixel metrics on the existing Geometric Waves source MP4 pair (`0c5ea4e15e041a05052d62febcc41d4ed8dedea41292f224c702ba2d28797a4e`): best same-index alignment offset 0; SSIM Y `0.981865`, U `0.991512`, V `0.990359`, aggregate `0.984889`; PSNR Y `34.025303 dB`, U `49.624752 dB`, V `42.702112 dB`, reported average `35.61258 dB`. The difference is real, luminance-dominant and not explained by a frame-start offset. These global metrics do not locate the affected screen regions.

## Evidence and integrity

- R1V report: `artifacts/tests/c11e/r1v_av_five_family_qualification/Q5_040414_B6BE4D/r1v_av_report.json`, SHA-256 `85de2645621acd6f8183508e0da9b5466b8a00cf9d2cb340a170f7d2803285ba`.
- Process receipt: `artifacts/tests/c11e/r1v_av_five_family_qualification/Q5_040414_B6BE4D/r1v_av_process_receipt.json`, SHA-256 `8820d36ffd6c1969eb4e148fe640f08f4324a243fe49ca1e43299e6db1201d26`.
- Run manifest SHA-256: `fe9df32e3bb939def95e2870f99601e795d75795cb7654dd020a323d5a80df7b`.
- Wrapper process receipt SHA-256: `e65462d3c96f27bbb7ed25c68e111a7a7584ae1e64c422f832d0a56d6d2910c9`.
- Pixel metrics JSON: `artifacts/tests/c11e/r1v_av_five_family_qualification/Q5_040414_B6BE4D/diagnostics/GEOMETRIC_WAVES_AB_PIXEL_METRICS_V1.json`, SHA-256 `0c5ea4e15e041a05052d62febcc41d4ed8dedea41292f224c702ba2d28797a4e`.
- The capture runner reported `Q5_040414_B6BE4D_EVIDENCE.zip` SHA-256 `c5aca635ed5cc9c62f271506b17347f6fe8b07af961cf8f3e95f828ccde9d9e5`; its ZIP bytes are not present in the accessible Library listing. A later no-movies diagnostic packer produced a `.sha256` sidecar declaring `7c32c087230761e7b835981dba040fc896e32d3abe30949464ef37a431be9f64` for `Q5_040414_B6BE4D_EVIDENCE_FAILURE_DIAGNOSTICS_NO_MOVIES.zip`, but that ZIP is also absent. V100-LATEST carries the report, inventories, authoring snapshots, logs, FFprobe outputs and pixel hashes, without video media.
- The FFmpeg 9 decode compatibility issue (`-vsync 0` → `-fps_mode passthrough`) and Windows path-budget issue were both passed before this run. FFmpeg decoded both Geometric A/B sources successfully to 690 frames each. Neither is the current blocker.
- Frozen C11-C manifest remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

## Source-code review — observations, not root-cause claims

The A/B Godot logs identify the same runtime: Godot `4.7.1.stable.mono.official.a13da4feb`, OpenGL API `3.3.0`, Intel driver `32.0.101.8132`, Intel Arc Graphics. Both runs recorded 690 frames at 30 fps. The authoring snapshots are byte-identical.

The Geometric Waves shader is deterministic by authored code path: the renderer derives `phase` from integer frame index, frame count and loop cycles; the prototype passes its frame index to both the shader and editorial layer; source inspection found no `TIME`, wall-clock, unseeded RNG, noise or audio input in this path. However, `GeometricWaves.gdshader` uses derivative-based antialiasing (`fwidth(value)`) in `line_from_zero()` and `contour_line()`. This is a diagnostic candidate only, not a proven cause. Do not remove/replace it based on this evidence alone.

The frozen C11-C `run_prototype.ps1` captures a temporary AVI using Godot Movie Maker (`--fixed-fps 30`, 720×1280), transcodes it to H.264 with FFmpeg (`libx264`, `preset fast`, `crf 18`, `yuv420p`), and deletes the AVI unless `-KeepAvi` is set. The R1V invocation did not retain the AVI. Thus the available evidence cannot yet distinguish an upstream rendered-frame variation from a later AVI-to-H.264 conversion difference. Do not change C11-C to retain or alter media as part of this documentation overlay.

## Required next diagnostic — no re-render

Use only the two already-generated *silent source MP4s* from `Q5_040414_B6BE4D`:

A: `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS\artifacts/tests/c11e/r1v_av_five_family_qualification/Q5_040414_B6BE4D\source\geometric_waves\A\GeometricWaves_v1_seed_100001_Q5_040414_B6BE4D_GEOMETRIC_WAVES_A.mp4`  
B: `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS\artifacts/tests/c11e/r1v_av_five_family_qualification/Q5_040414_B6BE4D\source\geometric_waves\B\GeometricWaves_v1_seed_100001_Q5_040414_B6BE4D_GEOMETRIC_WAVES_B.mp4`

Inspect their same-index decoded frames and produce spatial difference evidence for the existing 720×1280 videos: per-region (header/body/footer) SSIM/PSNR and absolute-difference summaries; per-frame distribution; visual overlays/heatmaps sampled at representative frames; distinguish broad low-amplitude drift from localized antialiasing/text/edge changes. Preserve original files and hashes. Do not re-encode or rewrite them.

The two MP4 files were deliberately excluded from the no-movies evidence archive. Uploading these two existing files is the next best step; do not rerun Godot, FFmpeg capture, the wrapper, or the 52 tests to recreate them. If the videos cannot be provided, a local read-only ROI diagnostic may be run against these exact paths and its JSON/heatmaps supplied.

## Decision gates

1. **Spatial localization:** determine whether differences are in body shader pixels, editorial/header/footer pixels, or spread across the canvas.
2. **Stage attribution:** current MP4s can localize the visible difference but cannot prove whether it was already present in the temporary AVI. Only if the ROI evidence requires it should a separately bounded, operator-approved diagnostic plan consider another capture preserving the intermediate AVI. No extra launch is implied by this document.
3. **Root-cause proof:** tie any proposed mechanism to evidence. `fwidth()`/GPU derivative sensitivity is a hypothesis, not a conclusion. Do not change the pixel comparison tolerance or waive the exact-determinism requirement.
4. **Correction boundary:** C11-C 2.19.12 is immutable. No changes to its shader, prototype, renderer, launcher, common audio, RNG, family binders or frozen manifest. Any correction must be confined to an authorized D/E-side adapter/diagnostic/qualification boundary and preserve the source media and C11-C mechanics.
5. **Regression and requalification:** only after a causal fix is justified, prepare a source-pinned overlay with a fail-closed installer. Re-run the combined 52-test wrapper only if the correction changes its dependencies; do not rerun R1P, Option C, Fractal A, or manual subsets. R1V closes only when all five A/B pairs are exact, all ten A/V outputs have passed technical QA, and outstanding human visual/layer and audio reviews are complete.

## Current human-review fields

The R1V report records Fractal Bloom A visual as `OPERATOR_CONFIRMED_PASS`; the other visual slots remain `PENDING_OPERATOR_REVIEW`, and listening across all audio slots remains `PENDING_OPERATOR_REVIEW`. Do not infer these reviews complete.

## Non-negotiable governance

`renderer=OFF`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14/D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `release_authority=NONE`. No production dispatch, no D compositor PASS, no E4B closure, and no successor phase admission is implied. No Git checks/bookkeeping; operator commits.
