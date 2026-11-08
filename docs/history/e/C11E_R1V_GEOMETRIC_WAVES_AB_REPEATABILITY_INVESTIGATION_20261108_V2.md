# C11-E R1V — Geometric Waves A/B Repeatability Investigation V2
**Date:** 2026-11-08  
**Status:** OPEN — `FAIL_CLOSED_PIXEL_NONDETERMINISM_GEOMETRIC_WAVES`  
**Scope:** Read-only forensic analysis of the existing `Q5_040414_B6BE4D` media plus a prepared, not-yet-authorized AVI-intermediate diagnostic. This document is not an acceptance receipt and does not authorize new rendering.

## 1. Confirmed execution state

The latest integrated wrapper run is `R1V_AV_WRAPPER_V1_20261108_030406_0C0B3ACA`. Its single integrated test gate passed 52/52, zero skips/errors/failures. The capture phase produced 10 A/V outputs, 10 source inventories, 10 family-native WAVs, 10 AAC muxes, nine new C11-C launches and one reuse of the previously accepted Fractal Bloom A. The A/B comparison then correctly stopped fail-closed on Geometric Waves / `harmonic_membrane`.

Four of five selector pairs are exact A/B matches: Fractal Bloom, Invisible Forces, Living Particles and Sacred Symmetry. Geometric Waves has 690 frames per side, matching PTS, 0/690 exact decoded-frame hashes, identical authoring JSON and identical WAV/AAC streams. Gameplay seed is 100001; music seed is 500001. There is no evidence of seed-domain or audio contamination.

## 2. Existing MP4 forensic evidence

Operator supplied `geometric_waves.zip`, 27,358,093 bytes, SHA-256 `b40ba2ddab6518c456ee822acd22a8fee2f143dcfb98c541b2f6049bdb6cc86e`, 29 ZIP entries, CRC clean. It contains the exact two silent source MP4s and supporting logs/manifests/authoring JSON, but **no AVI intermediate**.

| Item | A | B |
|---|---:|---:|
| Source MP4 bytes | 13,728,044 | 13,504,690 |
| Source MP4 SHA-256 | `b7b841ed48b9ac28bdfa28bed63ab398ebaa611bc5cfabe9dddd0e33dc249eca` | `a0225d0292f4bea8e13007cc05d5c694bde58687c20fa1ceb281c646e8faac7f` |
| Frames | 690 | 690 |
| Resolution / rate | 720×1280 / 30 fps | 720×1280 / 30 fps |
| PTS sequence | equal | equal |

The authoring JSON is byte-identical (SHA-256 `62d5d6fb2a04d42c190d641af3f142e24bab07157dd6335a0d2eb447a8acb07d`). Both runs use Godot `4.7.1.stable.mono.official.a13da4feb`, OpenGL 3.3 Compatibility and Intel Arc Graphics. The header animator is seed/frame-index driven; the footer content is static/frame-driven. No wall-clock or unseeded RNG dependency was found in the reviewed geometric shader/prototype path. `fwidth()` is present in the shader, but remains a hypothesis, not a proven cause.

## 3. Spatial comparison of the existing MP4s

The read-only forensic report is `GEOMETRIC_WAVES_AB_FORENSIC_REPORT_V1.json`, SHA-256 `aa0eac36e41057520fad0156f42862315aaf536b542ab2df77192ebd6f7192a4`. It used same-index frames and no video re-encode. Each band was compared independently; the best spatial translation for all bands was `(dx=0, dy=0)`.

| Region | Y coordinates | Mean absolute luma difference | Exact luma pixel fraction | SSIM all |
|---|---:|---:|---:|---:|
| Header | 0–191 | 1.754676188 | 0.753511295 | 0.986652 |
| Body | 192–1087 | 0.719716678 | 0.502719483 | 0.988397 |
| Footer | 1088–1279 | 3.770366166 | 0.682131769 | 0.966355 |

The Footer band has the largest average luma difference, followed by Header, then Body. The contact sheet retains the same broad geometric composition; fine differences are visible around text edges and body linework. This locality does **not** prove that text rendering caused the mismatch: the same-index source video contains all pixels composited by the capture pipeline. It also does not prove `fwidth()` or GPU nondeterminism.

Previously reported whole-frame metrics remain: exact hashes 0/690, best temporal offset 0, SSIM 0.984889 (Y 0.981865), average PSNR 35.61258 dB (Y 34.025303 dB). Exact-pixel acceptance is not to be relaxed.

## 4. Why the capture stage is not yet identified

The existing C11-C `run_prototype.ps1` emits an AVI intermediate and converts it to H.264 MP4 via FFmpeg. Its temporary AVI is deleted on exit unless the supported `-KeepAvi` switch is used. The two historic AVI files were not retained and are absent from `geometric_waves.zip`. Therefore existing MP4-only metrics cannot determine whether the first A/B divergence appears in Godot Movie Maker's AVI output or in AVI-to-H.264 conversion.

## 5. Prepared diagnostic — separate operator approval required

A no-install diagnostic kit is prepared:

- ZIP: `C11E_GEOMETRIC_WAVES_AVI_INTERMEDIATE_DIAGNOSTIC_V1.zip`
- SHA-256: `86f18fc6de5706d99a9383b10ac23422916ad87d6bde8d1efacc33b12da6406e`
- Scope: only `c11c_geometric_waves_v1` / `harmonic_membrane`, gameplay seed 100001, 23 seconds, 720×1280@30, 690 expected frames, slots A and B.
- It invokes the already-existing pinned C11-C launcher exactly twice, with `-NoSound -KeepAvi`, into new isolated output directories. No music generation, no mux audio, no other family, no Fractal A recapture, no R1V wrapper, no 52-test suite, no R1P, no Option C and no source code writes.
- The analyzer computes SHA-256 per decoded frame through FFmpeg `framehash` independently for AVI A/B and MP4 A/B. It also records FFprobe metadata. It does not create frame image files or alter the source media.
- It pins 23 active-checkout source inputs, checks them before and after, and verifies the known `override.cfg` restoration boundary. Unexpected override bytes are left untouched and cause a failed diagnostic.

**This capture is NOT authorized by the existing R1V scope.** The investigation V1 explicitly required a separate bounded operator-approved amendment for any AVI-retaining rerun. The kit has been prepared and statically/smoke verified; it has not been run. Operator approval must precede its execution.

### Interpretation of the stage result

- AVI A/B exact; MP4 A/B non-exact: divergence first appears after the AVI stage, in the conversion/packaging path or its handling of AVI metadata.
- AVI A/B non-exact; MP4 A/B non-exact: divergence is already present by the end of the Godot Movie Maker AVI stage. This localizes the first differing output boundary; it does not by itself prove a GPU hardware defect.
- Both AVI and MP4 exact: the focused pair did not reproduce the historical mismatch. It does not retroactively turn the historical failed run into PASS.
- Other mixed outcomes must be reported precisely from framehash/PTS counts; no automatic acceptance inference.

## 6. Prohibited shortcuts and acceptance

Do not modify C11-C 2.19.12, its shader, prototype, renderer, launcher, Movie Maker helper, family binders, RNG, audio, or frozen manifest. Do not change `fwidth()`, normalize hashes, introduce SSIM tolerance, waive exact identity, or modify seeds/music to force a PASS. Do not rerun the integrated 52-test wrapper merely to repeat this focused diagnostic.

R1V remains OPEN / FAIL-CLOSED until all five A/B pairs pass exact pixel identity, objective A/V QA is valid, and the outstanding operator visual/layer and all-track audio reviews are complete. After R1V closeout, roadmap order remains: remaining 22 Loop grammars → generalized Option C D post-composition consumer → E4B closeout → E4C Drill → E5 → E6 Smoke18 → E7 Matrix101 → E8. CH_008/CH_009 remain held for the declared 11s versus 12s timing discrepancy.

## 7. Governance

C11-C frozen manifest remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Renderer OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`. `GIT_CHECKS=SKIPPED`; operator manages commits.
