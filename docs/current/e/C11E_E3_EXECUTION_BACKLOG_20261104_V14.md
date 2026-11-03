# C11-E Execution Backlog — V14

**Date:** 2026-11-04. **Immediate objective:** finish E4A.2 real gameplay BODY pixel proof using the already-generated C11-C MP4; do not rerun Godot.

## 1. Closed / reusable

E0/E1, bounded E2 R4, E3.2, E3 Challenge audio/mux pilot and E3 50/50 negative controls remain accepted within scope. E4A source discovery, GUI contract successor, Gate A assessment and approved Policy V1 are accepted within scope. E4A.1 is closed only as neutral-body Godot fixture (23/23 tests, 18 PNGs at 540×960, 12 comparisons); gameplay BODY was not rasterized there.

## 2. E4A.2 Windows attempt and diagnosis

`RUN_20261103_235800_fd6fb07c.zip` is 4,698,162 bytes, SHA `2430588990a6d82aad68082fab000b71b5218af42f27cce75633b7153e06a53d`. It contains a successfully generated, operator-reviewed-as-OK CHALLENGE_004 C11-C base MP4, H.264 720×1280, 60fps/900 frames/15s, `yuvj420p/pc`, no audio. The C11-C manifest declares `pixel_format=yuv420p`, so the encoded-stream discrepancy is explicitly retained.

The first E4A.2 runner's 30fps/450/yuv420p direct-input assertion was wrong. It failed before PNG extraction. Focused tests were 25/25, but the runner exit was 1. A later manually printed PASS line after the exception is invalid. Frozen C11-C manifest remained unchanged.

## 3. Corrected E4A.2 V2

- Probe source stream as 60fps/900 and validate CHALLENGE_004, seed 314159, REVIEW_720 and silence.
- Preserve the original C11-C MP4 exactly.
- Create a test-only derivative at 30fps/450 using correct source-range-aware FFmpeg conversion: full-range `yuvj420p/pc` → limited-range `yuv420p/tv`; never treat known limited-range `yuv420p/tv` as full range.
- FFprobe the derivative, then generate 18 PNGs and 12 comparisons at delivery samples 0/89/90/300/390/449.
- Verify no BODY pixels change A→B and B/C identity; title/subtitle only HEADER/HOOK; CTA only FOOTER/CTA.
- `--reuse-c11c-base-run` accepts only the prior approved E4A RUN directory and bypasses Godot/C11-C regeneration.
- Runner SHA `5c0e8765bb29b58ddefc1b9593be188227e77725431c3dc959c1ce6866529a9b`; tests SHA `657f459ce11621a2dde133da5234ea27754c56b3acb5a10c8b37ff952a48d07b`; 33/33 preparation tests and compile PASS.
- The exact uploaded MP4 was replayed locally through the corrected normalization/pixel path: 18/18 PNG, 12/12 comparisons, zero BODY differences and B/C identity. Windows corrected replay remains required.

## 4. Visual caveat and following work

The test montage shows test-only title/subtitle coordinates overlap the existing C11-C hook headline. D1.5 has no accepted safe-area or generic typography parameters. Treat E4A.2 as a pixel-region/BODY invariance proof only; visual placement remains unapproved. No guessed coordinate changes.

Next sequence:
1. Apply V2 overlay and run 33 tests.
2. Run corrected Python runner with `--reuse-c11c-base-run ".\artifacts\tests\c11e\e4a_real_body_pixel_review\RUN_20261103_235800_fd6fb07c"`; inspect complete evidence ZIP. Do not rerender Godot.
3. E4A.3: integrate D-owned composition into actual D Challenge visual consumer and resolve layout stacking/geometry from canonical evidence, not C11-C aliases.
4. E4A.4: test-only A/V qualification using accepted E3 D3 V5/mux/FFprobe; operator visual review; only then close E4A.
5. E4B Loop → E4C Drill → E5 seed/determinism/family/profile/GUI-CLI parity → E6 Smoke18 → E7 Matrix101 (99 provisional while CH_008/009 11s/12s timing discrepancy held) → E8 historic C11-C corpus reconciliation, independent acceptance, freeze and explicit promotion.

## 5. Governance

Frozen C11-C manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` remains untouched. No C mechanics/generator/core/audio/D3 V5/E1 service modifications. D renderer OFF; D9.10 PREPARE_ONLY; D4.8 blocked; D9.14/D9.16 blocked; D9.17 no-go; D10 blocked; release authority NONE.
