# C11-E Gates and Acceptance Matrix — V24

**Date:** 2026-11-03
**Authority:** `C11E_CURRENT_AUTHORITY_20261103_V24.md`
**Code anchor:** `3cc1caa6d740b1525a4ebb30a4ff7f02868ac5a8`

| Gate | Scope / evidence | State | Next permitted action |
|---|---|---|---|
| E0 | Baseline restart, immutable manifest and receipts | PASS / CLOSED | Reuse; do not repeat |
| E1 | Shared GUI/CLI service, automated tests | AUTOMATED PASS / CLOSED | Reuse; retain GUI observation as a separate pending operator check |
| E2-A | Godot numeric preflight, Python contract | PASS | No rerun |
| E2-B | R4 isolated CH001 A/B render, immutable receipt/evidence | PASS | Reuse only |
| E2-C | 540/540 gameplay identity, 540/540 title-slot difference | PASS | No source edits |
| E2-D | FFprobe: 720×1280, 30 fps, 270 frames, 9s, no audio | PASS | Reuse R4 video as E3 input after hash verification |
| E2-E | Full decoded-frame visual audit and formal bounded closure | PASS / CLOSED for CH001 title-to-pixels only | No E2 rerun |
| E3.1 | Historical source review packages | SUPPORTING EVIDENCE | Not a live source-pin acceptance |
| E3-A | Active source-pin refresh after E3.2 commit; D3/D9 contract review | REQUIRED / NOT YET ACCEPTED | Read-only pin and contract reconciliation |
| E3.2 | D3 V5 to E1 intent contract; 8 new + 13 existing tests | PASS / COMMITTED | Reuse; no rerun absent source changes |
| E3-B | Challenge raw D3 V5 WAV, repeatability, seed isolation | NOT RUN | After E3-A and dedicated run plan |
| E3-C | D3.3 mastering/QA, raw WAV preservation, final-duration adaptation | NOT RUN | After E3-B |
| E3-D | FFmpeg A/V mux and FFprobe validation | NOT RUN | After E3-C |
| E3-GUI | Existing Producer GUI execution, output/status/error/provenance | PENDING | Include in next E3 implementation/acceptance |
| E3-CLI | Separate-process service parity and automation | PENDING for E3 dispatch | Tests only; no separate user workflow |
| E4A | Challenge complete presentation/editorial adapter | BLOCKED | After E3 acceptance |
| E4B | Loop family adapter, binder, editorial projection, C music generator integration | BLOCKED | After E3 acceptance and E4A seam review |
| E4C | Drill family adapter, phase-aware editorial projection and C music generator integration | BLOCKED | After E3 acceptance and family seam review |
| E5 | Cross-family determinism, music/gameplay seed isolation, GUI/CLI parity | BLOCKED | After E4A/B/C |
| E6 | Smoke18: six full A/V cases per family | BLOCKED | After E5 |
| E7 | Matrix101: 54 Challenge + 27 Loop + 20 Drill | BLOCKED; 99 provisionally runnable | After E6 and CH_008/009 resolution |
| E8 | Independent acceptance, freeze package, explicit promotion | BLOCKED | After all previous gates |

## Interpretations that must not be collapsed

- E2 closure is bounded to CHALLENGE_001 title-to-pixels. It is not full Challenge editorial acceptance.
- E3.2 proves a validated contract binding and deterministic V5 behavior in temporary test outputs. It does not prove a physical C11-E audio/mux product.
- D9.10's D-only envelope remains PREPARE_ONLY. E uses its own C11-E service/dispatch and does not change D9.10 or D4.8.
- E1 automated PASS is not an operator GUI runtime observation. E3 must make and record the real Producer GUI execution.
- CLI/GUI parity must be tested through the same service; the CLI is not the user's operational workflow from this point onward.
- `release_authority=NONE`, `baseline_promotion=false`, `freeze_eligible=false` until E8.

## Matrix arithmetic correction

The target Matrix101 is 54 Challenge + 27 Visual Loop + 20 Visual Drill = 101. CH_008 and CH_009 are two Challenge cases held due the declared 11-second duration conflicting with a 12-second phase sum. Therefore the provisional runnable population is **52 Challenge + 27 Loop + 20 Drill = 99**. The V13 parenthetical `54+27+18` is arithmetically 99 but conflicts with the declared family matrix; treat it as a documentation arithmetic error, not as a reduction of the Drill population. Confirm exact IDs against the live producer schema before E7.
