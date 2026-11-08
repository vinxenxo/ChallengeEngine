# C11-D / C11-E Blocker Remediation Register — V22
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
