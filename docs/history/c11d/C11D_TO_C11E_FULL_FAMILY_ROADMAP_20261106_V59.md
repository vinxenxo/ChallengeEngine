# C11-D to C11-E Full-Family Roadmap — V59

**Date:** 2026-11-06. Continue from V56. This roadmap advances evidence status only; it does not alter production governance.

## Product outcome

One coherent E factory through the established Producer GUI and CLI for Challenge, Visual Loop and Visual Drill. Preserve C11-C generators/mechanics and family binders/timelines. D supplies approved presentation/layout/editorial capabilities and Challenge music integration; E orchestrates family-correct audio, mastering, mux, FFprobe/audio QA, provenance and GUI/CLI parity.

## Challenge state

- **E4A.6 visual/reserved bands: PASS_TEST_ONLY + user visual review PASS.** Recovery V1.2 silent D-composited MP4 SHA `841b035...`, 720×1280/30fps/450 frames/15 s; 12/12 inactive-black and 4/4 active HOOK/CTA checks.
- **E4A.7 D-composited A/V: PASS_TEST_ONLY, independently audited.** Evidence ZIP SHA `ad4024...`; receipt `102cf0...`; 267/267 checksums. D3 V5 raw/master A/B repeatability; C seed difference; D3.3 loudness/peak/mono; three AAC muxes; H.264 copy identity; FFprobe 0.000 s start/end drift.
- **Full E4A remains IN_PROGRESS.** The D99 V1 runner passed all content pins and targeted tests, but its source replacement failed because `File.Replace` received a null backup pathname; the catch path then failed on bare `false` values. V2 repairs only those runner mechanics and installs current docs add-only. The operator listening A/B/C is PASS. One new post-patch GUI/E1/D9.9 parity run from the existing Producer is still required.

## Immediate ordered actions

1. A/B/C listening review is PASS by operator confirmation; do not repeat.
2. Apply the approved D99 GUI request contract patch using the corrected self-contained V2 runner. The source postimage remains the reviewed D-owned `main.py` change only: remove the Hook/countdown checkbox and serialized `presentation_options`; preserve all D9.8 canonical editorial fields and the E1 default. V2 fixes the V1 runner's null `File.Replace` backup-path and catch-boolean defects. No new GUI, module, producer, binder or render runner is added; no renderer or media is called.
3. Re-run one existing Producer GUI request in `C11-D · EDITORIAL UNIVERSAL (D9.9)` with the pinned Challenge fixture in parity plan V3 (`REVIEW_720`, personalization enabled); inspect the uploaded `D99-GUI-<ID>` evidence folder; require E1 semantic parity, D9 plan/bridge/adapter parity, lifecycle validation and fail-closed boundary.
4. Close full E4A after the corrected GUI/E1/D9.9 parity run PASS; listening is already accepted.

## Ordered gates after E4A

E4B Visual Loop (preserve grammar/variant timeline, binder/music) → E4C Visual Drill (preserve phases/END_CTA/binder/music) → E5 cross-family determinism/independent seed domains/profile isolation/GUI-CLI parity → E6 Smoke18 (six full A/V tests per family) → E7 Matrix101 (54 Challenge + 27 Loop + 20 Drill; CH_008/009 held, 99 provisional runnable) → E8 full historical C-to-E regression mapping, independent acceptance, immutable freeze and separate explicit promotion.

## Permanent constraints

C11-C 2.19.12 remains production authority; frozen manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Never change protected C mechanics, RNG, simulation truth, binders, timelines, shared presentation, core audio or manifest. No sixth module, second Producer or parallel binder. No Git in runners. Renderer/dispatch/production media OFF; `release_authority=NONE` until E8 and separately authorized promotion.


## D99 runner correction record

The V1 runner's tests and content pins passed; the failure was an installer API defect, not a discrepancy in the reviewed GUI source patch. V2 is the minimal recovery. E4B is intentionally not started until the required new GUI parity receipt closes full E4A; this preserves the campaign order and avoids testing Loop against an unclosed Challenge family integration gate.
