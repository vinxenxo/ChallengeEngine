# C11-E Continuation Master Prompt — V102

Continue the existing ChallengeEngine C11-D/C11-E project. Active checkout sole authority: `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. The V100 ZIP is evidence/context only; never unpack over checkout. Do not inspect Git, HEAD, branches, status, diffs or `.git`. `GIT_CHECKS=SKIPPED`; operator manages commits. Enforce SHA-256 source pins and the C11-C frozen manifest.

## Mission and immutable governance

Deliver the D+E production factory only after complete independent evidence, human acceptance, immutable freeze and a separate promotion decision. Preserve C11-C family mechanics, binders, timing, RNG/audio domains and protected sources. C11-C 2.19.12 is immutable; frozen manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` (796318 bytes). No protected code, manifest, shader, prototype, renderer, launcher, C11-C audio, binder or RNG changes. No sixth module, parallel Producer or new binder.

Renderer OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`. `request.seed` and `request.music_seed` remain separate.

## Accepted work — do not repeat absent regression

- E4A D99 GUI/CLI parity PASS_TEST_ONLY.
- E4B static Loop mapping 5 families / 27 grammars.
- R1P closed PASS 27/27; accepted archive SHA `d49f54ffdee6026426c2bb87fcb72b5c8a68f09cb64fb91f71e25dc10fd26b52`; 30 source pins.
- Option C 27/27 PASS PREPARE_ONLY; D post-composition consumer not implemented.
- R1V integrated suite 52/52 PASS; A/V 10 outputs generated. Four of five family A/B pairs exact. Do not repeat full wrapper, R1P, Option C, Fractal A or accepted work without a concrete regression.
- Old FFmpeg9 `-vsync` and Windows MAX_PATH blockers are closed.

## Current phase — R1V remains OPEN / FAIL-CLOSED

Latest run `Q5_040414_B6BE4D`; wrapper `R1V_AV_WRAPPER_V1_20261108_030406_0C0B3ACA`; receipt SHA `e65462d3c96f27bbb7ed25c68e111a7a7584ae1e64c422f832d0a56d6d2910c9`. It passed 52/52 with zero skips/errors/failures and generated 10 A/V outputs, 10 inventories, 10 native WAVs and 10 AAC muxes. It failed closed only on Geometric Waves / `harmonic_membrane`: 690 frames/PTS match but 0/690 exact frame hashes. Other four family A/B pairs are exact. Authoring JSON identical (SHA `62d5d6fb2a04d42c190d641af3f142e24bab07157dd6335a0d2eb447a8acb07d`); gameplay seed 100001; music seed 500001; WAV/AAC exact.

Existing MP4 forensic report: `GEOMETRIC_WAVES_AB_FORENSIC_REPORT_V1.json`, SHA `aa0eac36e41057520fad0156f42862315aaf536b542ab2df77192ebd6f7192a4`. Operator ZIP `geometric_waves.zip` SHA `b40ba2ddab6518c456ee822acd22a8fee2f143dcfb98c541b2f6049bdb6cc86e` (29 entries, no AVI). Regional luma MAE: Header 1.754676188, Body 0.719716678, Footer 3.770366166. All best spatial translations are zero. Footer is most affected, but this does not prove footer/text is the cause. Full frame metrics: SSIM 0.984889, PSNR avg 35.61258 dB; exact 0/690. `fwidth()` in shader is only a hypothesis. Current code review found same seeded/frame-index header logic and static/frame-driven footer; no authoring/time/seed/audio mismatch.

**Critical limitation:** no original A/B AVI intermediate was retained. Therefore current MP4-only evidence cannot distinguish Movie Maker/AVI output variance from FFmpeg AVI→MP4 variance. Do not patch C11-C or weaken exact-pixel comparator.

## Prepared diagnostic — requires separate explicit operator approval

`C11E_GEOMETRIC_WAVES_AVI_INTERMEDIATE_DIAGNOSTIC_V1.zip`, SHA `86f18fc6de5706d99a9383b10ac23422916ad87d6bde8d1efacc33b12da6406e`. This no-install diagnostic uses the existing pinned C11-C launcher exactly twice for Geometric A/B only (seed 100001, grammar `harmonic_membrane`, 23 s, 720×1280@30), with `-NoSound -KeepAvi`. It will retain both AVI and MP4 artifacts and run framehash/FFprobe comparisons per stage. It does NOT run the integrated R1V wrapper, 52 tests, audio/music generation, mux, other families, Fractal A, R1P, Option C, or any code install/edit. It checks 23 source SHA pins before and after and verifies safe `override.cfg` restoration. The package is statically/smoke verified but has not been run.

The existing R1V authority does NOT authorize retaining AVI; a separate operator-approved bounded amendment is required. Wait for explicit approval before executing this diagnostic. If approved, use the README/PowerShell runner in a fresh Downloads folder; never extract into checkout. Do not repeat an existing diagnostic run.

Interpretation: AVI exact but MP4 non-exact localizes first divergence after AVI; AVI non-exact localizes it at/before Movie Maker AVI output, not necessarily GPU; both exact means the old anomaly did not reproduce and does not retroactively close R1V.

## Closure criteria and roadmap

R1V closes only when all five family A/B pairs pass exact pixel identity, objective A/V QA is valid, and remaining operator visual/layer and all-track audio reviews pass. Then admit remaining 22 Loop grammars; implement one generalized Option C D post-composition consumer over immutable C video; close E4B; then E4C Drill → E5 → E6 Smoke18 → E7 Matrix101 → E8. CH_008/CH_009 remain held until 11s/12s duration issue resolves.

Never infer production activation or promotion from test-only success. Keep renderer OFF, D4.8 BLOCKED and `release_authority=NONE`.
