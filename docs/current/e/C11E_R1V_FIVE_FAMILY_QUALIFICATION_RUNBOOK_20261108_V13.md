# C11-E R1V Five-Family A/V Qualification Runbook — V13
**Current run:** `Q5_040414_B6BE4D`. **State:** OPEN / FAIL-CLOSED on one geometric A/B pixel determinism mismatch.

## Accepted setup and executed gate

- The bounded scope remains five representative Loop selectors × A/B = ten A/V outputs. Fractal Bloom A was reused; nine new C11-C launches were performed. Family-native `FAMILY_MUSIC_V4` consumed the R1P `music_seed`, with AAC 192 kb/s / 44.1 kHz / stereo and source H.264 copied unchanged.
- The combined Windows test gate passed 52/52 with zero skips/errors/failures. Do not repeat it without an actual dependency change.
- The run completed 10 A/V outputs, 10 source inventories, 10 music generations and 10 AAC muxes. FFmpeg 9 decode and path preflight both passed.

## Latest result

`FAIL_R1V_AV_FIVE_FAMILY_QUALIFICATION_STOPPED_FAIL_CLOSED` on `c11c_geometric_waves_v1` / `harmonic_membrane`:

- A/B: 690 frames each, matching PTS; no integer-frame alignment offset found.
- Exact pixel matches: 0/690. Source A SHA `b7b841ed48b9ac28bdfa28bed63ab398ebaa611bc5cfabe9dddd0e33dc249eca`; B SHA `a0225d0292f4bea8e13007cc05d5c694bde58687c20fa1ceb281c646e8faac7f`.
- Identical authoring JSON bytes, gameplay seed 100001, music seed 500001, grammar, duration, FPS, cycles, palette and style. WAV/AAC streams match.
- Metrics JSON SHA `0c5ea4e15e041a05052d62febcc41d4ed8dedea41292f224c702ba2d28797a4e`: aggregate SSIM 0.984889, Y 0.981865, U 0.991512, V 0.990359; average PSNR 35.61258 dB, Y 34.025303 dB; best offset 0.
- Fractal Bloom, Invisible Forces, Living Particles and Sacred Symmetry A/B source/pixel streams match exactly.

## No-rerun action

First analyze the two *existing* silent source MP4s spatially. Exact paths:

`C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS\artifacts/tests/c11e/r1v_av_five_family_qualification/Q5_040414_B6BE4D\source\geometric_waves\A\GeometricWaves_v1_seed_100001_Q5_040414_B6BE4D_GEOMETRIC_WAVES_A.mp4`

`C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS\artifacts/tests/c11e/r1v_av_five_family_qualification/Q5_040414_B6BE4D\source\geometric_waves\B\GeometricWaves_v1_seed_100001_Q5_040414_B6BE4D_GEOMETRIC_WAVES_B.mp4`

Produce same-index regional SSIM/PSNR and difference maps for Header, Body and Footer; inspect representative and worst frames. No new Godot capture, no FFmpeg transcode, no music regeneration, no mux, no wrapper and no 52-test rerun. The videos were excluded from the no-movies ZIP, so they must be supplied separately or processed locally with a read-only script.

The two AVI intermediates were not retained (`-KeepAvi` false); launcher cleanup removed them. Therefore the current data do not identify whether divergence first appears in GPU/Movie Maker or AVI-to-H.264. Another AVI-retaining capture is not authorized here and would require a separate bounded operator amendment. `fwidth()` in the geometric shader is a plausible investigation point, not a proven cause.

## Acceptance

Do not weaken exact pixel-hash checks. R1V remains open until five pairs exact, objective A/V QA passes, and all remaining human visual/layer plus ten-track listening reviews pass. Only then admit remaining 22 Loop grammars. C11-C baseline and governance locks are unchanged.
