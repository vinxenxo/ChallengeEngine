# C11-E Master Handover — V4 (2026-11-18)

## Sole authority and workflow

Active Windows checkout: `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. Never extract ZIPs over it. Nightly ZIP is evidence/reference only. Operator manages commits. Do not invoke Git or inspect HEAD/status/branch. SHA-256 source pins and frozen C11-C manifest are authoritative.

## Accepted work — do not repeat

- E4A Challenge, E4B Loop, E4C Drill 20/20 and E5 Cross-Family accepted in their declared scopes.
- E5 visible Qt Producer runtime 3/3 PASS; blank `language=es` in one GUI check was an operator input omission, not a software defect.
- R1V visual/editorial/layout/audio closeout 10/10 accepted; Loop22 44/44 outputs and operator visual/audio approvals accepted. Do not rerun.
- E6 hydration V2: 1,801/1,803 checks passed; the only two findings were CH004 historical E4A.7 source-pin divergences. No other failures.
- D9 Challenge multi-selector PREPARE_ONLY: six Challenge groups, 18 linked E1 intents and 18 D envelopes. One visual source per selector shared by A/B/B_REPEAT/C_CHANGED_MUSIC_SEED probes.
- D9 dependency reconciliation V2 and repair applicator: active-checkout PASS; V2 focused tests 13/13; fixed evidence/sidecar pins 13/13; accepted source pins 33/33; route dependencies 9/9; observed current CH004 hashes 2/2; zero reconciliation failures. Exact report `E6D9PINREC_20261118T094345Z_2B9358D1`, SHA-256 `0e2c977f1122d9cfc69da255d8fa539720a23f00cdc2f4c030d48bd01019a59a`.

## Current phase: E6 CH004 historical source-pin adjudication

The V2 reconciliation closes the operational repair and confirms all current accepted pins. It does not auto-waive historical E4A.7 source pins.

E4A.7 (2026-11-06) pinned these source preimages:
- D9 editorial model: `5c575be1942ba0613d66579d14db5cf9d7786e7062dfb001bd7be8a2e9c18ae5` (26,574 bytes).
- E1 production service: `348997e575d985fe153a4f433f089c5f205be5d4d8f3853baf07be917a134951` (32,885 bytes).

E4B V2 source-patch manifest and E4B V3 recovery receipt document later preimage→postimage transitions and identify the exact backup paths `b/05.bak` and `b/01.bak`. Run `C11E_E6_CH004_HISTORICAL_SOURCE_PIN_ADJUDICATION_V1` to verify the exact backup bytes and create a semantic diff only when both historic preimages match exact hashes and sizes. V2 hardens path/reparse-point checks and requires full backup path equality against the receipt.

Even when both exact backups are found, CH004 remains only `REUSE_CANDIDATE_PENDING_SEMANTIC_DIFF_REVIEW_AND_E6_LEDGER_REQUALIFICATION`. No automatic reuse acceptance. If either backup is absent or mismatched, CH004 stays ineligible; do not restore old code or regenerate historic evidence.

## After CH004 adjudication

1. Manually review the generated diff for impact on E4A.7 request semantics, editorial resolution, Challenge composition, output identity, A/B/C outputs and E6 acceptance predicates.
2. Refresh D9 capture plan V2 from the exact 2026-11-18 33-pin reconciliation; leave plan V1/receipt immutable and retire only the stale nine-dependency observation.
3. Freeze six Challenge groups, six Loop groups and six Drill groups (18 top-level Smoke18 rows), with exact E1/D references, seeds, timebases, receipts, media hashes and reuse dispositions. A/B/C are Challenge sub-probes, not extra top-level rows.
4. Prepare a separate E6 TEST_ONLY authorization with exact binaries, hashes, argv, invocation limits, output roots, stop conditions, one-shot identity and operator acceptance. Obtain explicit governance resolution of D4.8 before media.

## Timing history

The operator explains one/two-second Challenge timing discrepancies as early design experimentation before countdown/HOOK/CTA structure and optimal social duration were settled. Preserve that historical provenance. Keep CH008/009 declared 11-second duration separate from the 12-second phase sum; do not rewrite definitions or frames. Canonical delivery duration requires a later explicit policy decision.

## Render and governance boundary

D4.8 R1V V2 is immutable and prohibits Smoke18, Godot capture, D3/audio/PCM and FFmpeg filters/mux. Engineering approval is not media authorization. C11-C 2.19.12 remains sole production authority; frozen manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. D4.8 SHA `0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07`. E1 PREPARE_ONLY; D9 PREPARE_ONLY; renderer OFF; dispatch/media false; `release_authority=NONE`. No protected C11-C mutation, no parallel Producer/binder/renderer or sixth module. No Git checks; commits operator-managed; source pins enforced.
