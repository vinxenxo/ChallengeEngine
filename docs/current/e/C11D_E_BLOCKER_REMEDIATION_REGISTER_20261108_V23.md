# C11-D / C11-E Blocker Remediation Register — V23
**Date:** 2026-11-08. **Current blocking item:** R1V Geometric Waves pixel repeatability. The earlier FFmpeg 9 `-vsync` and Win32 path-budget defects are resolved by installed corrections and passed in the latest active integrated run.

| ID | Blocker | Evidence / current state | Required remediation | Gate effect |
|---|---|---|---|---|
| R1V-GEO-AB-PIXEL-01 | A/B pixels differ in Geometric Waves `harmonic_membrane` | `Q5_040414_B6BE4D`; 0/690 exact frames; same 690 PTS; SSIM 0.984889; PSNR avg 35.61258 dB; same authoring JSON/seeds/audio; other 4 family pairs exact | Read-only spatial pixel/ROI analysis of existing A/B source MP4s; then prove source stage and cause. No code changes until evidenced. | R1V remains OPEN / FAIL-CLOSED; remaining 22 Loop grammars stay gated |
| R1V-HUMAN-REVIEW | Remaining visual/layer and all audio review fields pending | Latest report says only Fractal Bloom A visual confirmed | Operator review all other A/B videos/layers and listen to ten outputs after technical repeatability is addressed | Blocks R1V closeout |
| OPTION-C-D-CONSUMER | D post-composition consumer is not implemented | 27/27 handoffs PASS PREPARE_ONLY; 33 pins | Implement one generalized consumer after Loop qualification, over immutable C video | Blocks E4B closure |
| E4C-DRILL | Drill layout/editorial/audio/phase handling not complete | Roadmap dependency | Start only after E4B | Blocks E4C/E5 |
| E5/E6/E7/E8 | Later qualification sequence not reached | Roadmap V47 | Execute in strict sequence after upstream gates | Blocks promotion |
| CH-008/009 timing | Declared 11s vs phase sum 12s | Known unresolved mismatch | Reconcile contract before admitting these cases | Keep two cases held |

## Closed compatibility incidents

- FFmpeg 9 no longer accepts `-vsync 0`; R1V now decodes with `-fps_mode passthrough`. This is verified by the successful 690-frame A/B pixel-metrics run and the ten-slot capture run. Not a current blocker.
- Win32 MAX_PATH overrun was corrected with compact run IDs and complete path preflight. Latest run passed preflight. Not a current blocker.
- V1/V2 installer lineage and SHA pin failures were resolved; do not retry obsolete V1 packages.

## C11-C and governance locks

No edit to C11-C 2.19.12 shader, renderer, prototype, launcher, core audio, RNG, family binders or frozen manifest `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. No tolerance relaxation. Renderer OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`. Operator owns commits; no Git checks.


## R1V-GW-REPEATABILITY — OPEN / FAIL-CLOSED

**Observed:** `Q5_040414_B6BE4D`, 52/52 tests PASS; 10 A/V outputs completed; four of five family pairs exact. Geometric Waves is 0/690 exact frame matches. PTS, authoring JSON, WAV and AAC match. MP4 regional luma MAE: Header 1.754676188; Body 0.719716678; Footer 3.770366166; spatial translation zero. Source evidence has no AVI intermediate.

**Root cause:** NOT YET ATTRIBUTED. `fwidth()` and GPU derivative sensitivity remain hypotheses only. No code edits authorized.

**Next:** prepared two-slot `-KeepAvi` diagnostic ZIP SHA `86f18fc6de5706d99a9383b10ac23422916ad87d6bde8d1efacc33b12da6406e`; status PREPARED / NOT RUN / NOT AUTHORIZED. Await separate operator approval. It is test-only diagnostic authority for exactly two Geometric A/B captures, not general renderer authority or R1V acceptance.

**Prohibited:** change C11-C code, shader, capture/launcher path, hash comparator, seeds or music; repeat accepted 52 tests or complete A/V runs; advance remaining 22 loops; enable renderer or release authority.


## V3 authoritative status update — 2026-11-08

This section supersedes any earlier statement in this document that the AVI-retaining diagnostic was pending, prepared, or not authorized. The operator installed documentation overlay V2 successfully (11/11 ADD files; install manifest SHA-256 `1b4c36ee2ed9d6ce8e7604cba585247d2cbabd4370b86ac9b662b488c802dd32`) and explicitly authorized exactly two Geometric Waves A/B captures with `-KeepAvi`. Those two captures are complete and independently audited.

**Diagnostic disposition:** `PASS_DIAGNOSTIC_NOT_REPRODUCED`. Run `GWDIAG_192813_C56B9C`; evidence ZIP SHA-256 `b76e1fb276d91c831f11bcba6069e751cab7afbc8248300b89c97843753b53d9`; diagnostic receipt SHA-256 `56e95b8c16590126d4ab082d1519988bed6edac6f3bfbe06463e5178f5b375f2`; AVI/MP4 stage-comparison JSON SHA-256 `eb533995f76617665040013933eea159b3c4c583787c029ae285d279652a3402`. Both slots exited 0. The A and B AVI files are byte-identical (50,692,122 bytes; SHA-256 `78be4ab46e7b04f3d7544e628c58e2d2f1d018e1ee7992e8db57bbd819ab6a1a`); the A and B MP4 files are byte-identical (13,728,044 bytes; SHA-256 `b7b841ed48b9ac28bdfa28bed63ab398ebaa611bc5cfabe9dddd0e33dc249eca`). Each stage has 690/690 exact framehash matches and equal PTS/DTS. The authoring JSON for A/B is identical (SHA-256 `62d5d6fb2a04d42c190d641af3f142e24bab07157dd6335a0d2eb447a8acb07d`). All 23 source pins matched before/after; `override.cfg` was absent before and after. No tests, full R1V wrapper, music generator, Git, or source modification occurred in this diagnostic.

**Critical distinction:** the new pair reproduces the historic R1V Geometric A source MP4 exactly, but does not explain or erase the historic B outlier (`a0225d0292f4bea8e13007cc05d5c694bde58687c20fa1ceb281c646e8faac7f`). Historical run `Q5_040414_B6BE4D` remains `FAIL_R1V_AV_FIVE_FAMILY_QUALIFICATION_STOPPED_FAIL_CLOSED`, with 0/690 exact Geometric A/B frame matches. The diagnostic proves that the two newly captured runs are repeatable at both AVI and MP4 stages; it does **not** establish the cause of the earlier B divergence or prove the pipeline is universally deterministic. Do not attribute the old event to Movie Maker, FFmpeg, GPU, `fwidth()`, timing, or any other component without new evidence. Do not relax pixel-hash acceptance and do not patch C11-C.

**Current R1V remains OPEN / FAIL-CLOSED.** Four other family A/B pairs remain accepted; do not repeat them. Do not repeat the 52/52 integrated test gate, R1P, Option C, or Fractal Bloom A absent a real dependency regression. Visual operator review is still only confirmed for Fractal Bloom A; all other required visual/layer slots are pending. All ten audio listening reviews remain pending.

**Next bounded action:** run the separate read-only kit `C11E_R1V_GEOMETRIC_WAVES_AV_REUSE_PREFLIGHT_V1.zip` (SHA-256 `efe7d2de99b0b2a7ab925a482b5a815d93516774bf65cfd1c471ad164ab31fda`). It verifies the existing historical source MP4s, WAV/PCM/AAC outputs, final mux streams, new AVI/MP4 pair, historic reports/receipts, and 23 active source pins. It invokes FFmpeg/FFprobe only to probe and hash existing streams in memory and writes one JSON report plus SHA sidecar. It does **not** render, capture, generate music, mux, or alter source/media files. Expected marker: `PASS_READY_FOR_SCOPED_GEO_AV_REBUILD_NOT_EXECUTED`. On any mismatch, stop fail-closed.

Only after that preflight passes, prepare a separate exact-scope two-output Geometric Waves mux-only requalification using the new identical MP4 A/B videos and reuse of the already-validated identical AAC audio streams from the historic A/V outputs. That future action is not part of the preflight and has not been authorized or executed here. It must not invoke C11-C capture, the music generator, the integrated five-family runner, the other four families, or the 52-test suite. Require separate explicit authorization before media mux. R1V acceptance remains withheld until the historical B discrepancy is formally resolved by evidence and the ten visual/layer plus ten audio listening reviews are complete.

Governance remains unchanged: C11-C 2.19.12 immutable; frozen manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; renderer OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`; Git checks skipped and commits operator-managed. Remaining 22 Loop grammars and every downstream phase remain blocked pending R1V closeout.
