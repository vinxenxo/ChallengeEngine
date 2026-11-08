# C11-E Continuation Master Prompt — V101

Continue the existing ChallengeEngine C11-D/C11-E implementation. Do not restart the project or repeat accepted phases. The active Windows checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS` is the only source authority. The V100 ZIP is an inspection snapshot, not a replacement source; never unpack it over the checkout. Do not inspect Git, HEAD, branches, status, diffs or `.git`. `GIT_CHECKS=SKIPPED`; operator owns commits. Enforce exact source SHA-256 pins and the C11-C frozen manifest.

## Mission

Deliver the future D+E audiovisual production factory that supersedes C11-C only after complete evidence, independent review, immutable freeze and a separate explicit promotion decision. Preserve C11-C production mechanics, family-specific visual/music behavior, binders, timing and RNG domains. Integrate D presentation/layout/editorial only at accepted family boundaries. Do not enable rendering or production dispatch by inference.

## Immutable baseline / permanent locks

C11-C 2.19.12 frozen manifest: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` (796,318 bytes). No modifications to the manifest, protected C11-C generators/mechanics/core audio, RNG, family binders, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, canonical definitions, C11-C shader/prototype/renderer/launcher/capture paths, or D4.8/D9.10 locks. No sixth module, parallel Producer or new binder. `request.seed` and `request.music_seed` are separate domains.

Renderer OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`. No production dispatch, media pipeline activation or promotion.

## Accepted gates — do not repeat absent regression

- E4A D99 GUI/CLI parity: PASS_TEST_ONLY.
- E4B static Loop family mapping: five families / 27 grammars.
- R1P: 27/27 PASS, 30 source pins; ZIP SHA `d49f54ffdee6026426c2bb87fcb72b5c8a68f09cb64fb91f71e25dc10fd26b52`.
- Option C: 27 handoffs PASS PREPARE_ONLY, 33 pins; general D compositor not implemented.
- Fractal Bloom A: visually accepted source SHA `7971ced1d9cdbb7dd76a0d8d76e766faa9a051fc27419c9e737c41264796f659`, 720×1280/30, 660 frames/22 s; reuse, do not recapture.
- FFmpeg9 decode compatibility and Windows path budget corrections have passed; do not reinstall or treat them as current blockers.

## Current phase: R1V five-family bounded A/V qualification — OPEN / FAIL-CLOSED

Latest run `Q5_040414_B6BE4D`; integrated test wrapper 52/52 PASS (zero skips/errors/failures). The A/V sequence completed 10 outputs, 10 inventories, 10 family-native music generations, 10 AAC muxes, 9 new C11-C launcher calls, and reused Fractal Bloom A once.

The run failed closed only at Geometric Waves / `harmonic_membrane`: 690/690 PTS and frame counts match, but pixel hashes match 0/690. Four other families (Fractal Bloom, Invisible Forces, Living Particles, Sacred Symmetry) are exact A/B pixel matches. Geometric A/B authoring JSON is byte-identical; gameplay seed 100001 and music seed 500001 are identical across repeats and remain separate; WAV and AAC streams match. The source MP4 SHA values differ (A `b7b841ed48b9ac28bdfa28bed63ab398ebaa611bc5cfabe9dddd0e33dc249eca`; B `a0225d0292f4bea8e13007cc05d5c694bde58687c20fa1ceb281c646e8faac7f`).

Read-only metrics: best frame offset zero; SSIM aggregate 0.984889 (Y 0.981865, U 0.991512, V 0.990359); PSNR average 35.61258 dB (Y 34.025303 dB). Variation is real, luminance-dominant, and not a small integer-frame shift. Metrics cannot localize it spatially.

Latest report SHA `85de2645621acd6f8183508e0da9b5466b8a00cf9d2cb340a170f7d2803285ba`; process receipt SHA `8820d36ffd6c1969eb4e148fe640f08f4324a243fe49ca1e43299e6db1201d26`; run manifest SHA `fe9df32e3bb939def95e2870f99601e795d75795cb7654dd020a323d5a80df7b`; metric JSON SHA `0c5ea4e15e041a05052d62febcc41d4ed8dedea41292f224c702ba2d28797a4e`. The runner-reported evidence ZIP SHA is `c5aca635ed5cc9c62f271506b17347f6fe8b07af961cf8f3e95f828ccde9d9e5`, but its ZIP is not in Library; the later no-movies diagnostic ZIP is likewise absent (its sidecar declares `7c32c087230761e7b835981dba040fc896e32d3abe30949464ef37a431be9f64`).

## Immediate next action — inspect existing Geometric A/B source MP4s, no rerun

Use the existing source pair in the active checkout:

A: `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS\artifacts/tests/c11e/r1v_av_five_family_qualification/Q5_040414_B6BE4D\source\geometric_waves\A\GeometricWaves_v1_seed_100001_Q5_040414_B6BE4D_GEOMETRIC_WAVES_A.mp4`

B: `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS\artifacts/tests/c11e/r1v_av_five_family_qualification/Q5_040414_B6BE4D\source\geometric_waves\B\GeometricWaves_v1_seed_100001_Q5_040414_B6BE4D_GEOMETRIC_WAVES_B.mp4`

They were excluded from the no-movies ZIP. Ask the operator to upload these two existing files (or inspect them locally via read-only spatial comparison). Compute same-index per-frame regional difference metrics and representative heatmaps/overlays for Header, Body, Footer. Do not re-render, regenerate music, re-mux, re-encode, run Godot, run FFmpeg capture, run the wrapper or repeat 52 tests to recreate these files. Preserve source files unchanged.

Source review: A/B logs show Godot 4.7.1, OpenGL 3.3, same Intel Arc driver 32.0.101.8132, 690 frames. Geometric shader derives phase from integer frame index and has no explicit wall-clock/TIME/unseeded-RNG/audio dependency. It uses `fwidth()` derivative-based antialiasing; this is a hypothesis only, not proven cause. C11-C `run_prototype.ps1` transcodes temporary AVI to H.264 and deletes AVI unless `-KeepAvi`; current run did not preserve AVI. Existing MP4s can localize visible regions but cannot establish whether the discrepancy is upstream GPU/Movie Maker or the AVI-to-H.264 stage. Any additional capture retaining AVI needs a separate bounded operator-approved amendment. Do not change C11-C to capture it.

## Remediation discipline

Do not relax exact pixel identity or change seeds/audio/comparator to force PASS. Do not make a code patch until the spatial and stage evidence supports a cause. C11-C is frozen; any eventual fix must be within a specifically authorized D/E diagnostic/qualification boundary. Use source-pinned, fail-closed PowerShell 5.1 installers; classify successor docs as ADD, verify all SHA pins and receipt lineage before staging, stage everything before apply; installers do not run tests or media processes.

After a justified fix, run the integrated 52-test wrapper only if a source dependency changes; do not repeat R1P, Option C, prior Fractal A, or manual subsets. Close R1V only after all five pairs pass exact frame/stream identity, all ten outputs pass objective QA, and human visual/layer + all-track audio reviews pass. Report marks Fractal Bloom A visual `OPERATOR_CONFIRMED_PASS`, other visual slots pending, all audio listening pending.

## Roadmap after R1V — strict order

1. R1V technical and human closeout.
2. Qualify remaining 22 Loop grammars with each family's native music.
3. Implement one generalized Option C D post-composition consumer over immutable C video; preserve C binders, mechanics, timing and family-native music.
4. Close E4B; implement E4C Drill with native music and correct phase/END_CTA precedence.
5. E5 cross-family determinism, seed isolation, no adapter/profile leakage, GUI/CLI parity.
6. E6 Smoke18 (six A/V cases per family).
7. E7 Matrix101 (54 Challenge +27 Loop +20 Drill); keep CH_008/009 held pending 11s/12s reconciliation.
8. E8 full historical C-to-E regression, independent acceptance, immutable freeze and separate promotion decision.

Do not jump gates or imply release authority from test-only success.
