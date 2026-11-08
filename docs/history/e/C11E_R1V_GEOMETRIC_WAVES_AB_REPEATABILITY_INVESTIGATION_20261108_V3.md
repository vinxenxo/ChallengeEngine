# C11-E R1V Geometric Waves A/B Repeatability Investigation — V3
**Date:** 2026-11-08. **Disposition:** AVI and MP4 diagnostic pair PASS; historic R1V qualification remains OPEN / FAIL-CLOSED.

## Diagnostic evidence and stage outcome

Operator explicitly authorized exactly two diagnostic captures with AVI retention. Run `GWDIAG_192813_C56B9C` completed 2/2. Evidence ZIP SHA-256 `b76e1fb276d91c831f11bcba6069e751cab7afbc8248300b89c97843753b53d9`; receipt SHA-256 `56e95b8c16590126d4ab082d1519988bed6edac6f3bfbe06463e5178f5b375f2`; comparison JSON SHA-256 `eb533995f76617665040013933eea159b3c4c583787c029ae285d279652a3402`.

- AVI A/B: 690/690 exact frame hashes; equal PTS/DTS; file bytes 50,692,122; both SHA-256 `78be4ab46e7b04f3d7544e628c58e2d2f1d018e1ee7992e8db57bbd819ab6a1a`.
- MP4 A/B: 690/690 exact frame hashes; equal PTS/DTS; file bytes 13,728,044; both SHA-256 `b7b841ed48b9ac28bdfa28bed63ab398ebaa611bc5cfabe9dddd0e33dc249eca`.
- Authoring JSON A/B equal; SHA-256 `62d5d6fb2a04d42c190d641af3f142e24bab07157dd6335a0d2eb447a8acb07d`.
- 23/23 source pins were unchanged before/after; `override.cfg` remained absent. Both Godot capture slots exit 0.
- Stage classification: `BOTH_STAGES_EXACT_REPEATABLE_DIAGNOSTIC_DID_NOT_REPRODUCE_DIVERGENCE`. No tolerance/SSIM was used.

## Interpretation — bounded, not causal

The new MP4 pair is byte-identical to historic Geometric A, not to historic B. Historic B SHA remains `a0225d0292f4bea8e13007cc05d5c694bde58687c20fa1ceb281c646e8faac7f`. Therefore this diagnostic establishes repeatability for this new two-run pair but does not explain the historical B outlier. It does not prove a systematic Movie Maker, FFmpeg, GPU, `fwidth()`, timing, or shader defect. No code change is justified. C11-C remains frozen.

Historic `Q5_040414_B6BE4D` is still fail-closed: Geometric 0/690 exact A/B pixels, though 690 frames/PTS, authoring JSON, WAV, AAC and seeds match; four other family A/B pairs are exact. The earlier spatial comparison had zero best alignment offset, SSIM 0.984889, PSNR average 35.61258 dB; footer luma MAE 3.770366166, header 1.754676188, body 0.719716678. These metrics describe the old pair only and are not causal evidence.

## Next controlled step

Run the read-only `C11E_R1V_GEOMETRIC_WAVES_AV_REUSE_PREFLIGHT_V1.zip` (SHA-256 `efe7d2de99b0b2a7ab925a482b5a815d93516774bf65cfd1c471ad164ab31fda`). It verifies prior WAV/PCM/AAC/AV assets and the new exact diagnostic pair; no media is created. If it passes, a separate, explicitly authorized two-output A/V mux-only requalification can be designed using the new MP4 video and existing approved audio. No integrated wrapper, C11-C capture, audio generation, other family, or 52-test rerun.

R1V will not close until historical B divergence is resolved by evidence and all outstanding visual/layer and audio reviews pass. Remaining 22 Loop grammars stay blocked.
