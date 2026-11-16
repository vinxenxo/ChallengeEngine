# C11-E Current Authority — V170 (2026-11-16)

## Current authoritative snapshot

- E4C Visual Drill acceptance is **15/20**. Tracking 5/5, Pursuit 5/5 and Saccade 5/5 are technically qualified and explicitly operator-approved. Peripheral Scan is the only remaining family (0/5).
- Saccade batch: `E4C-SACCADE-T1-5-20261115T235737Z-57fdf44b`. Five selectors technical PASS; operator approved layout, editorial, music and execution for all five tiers.
- Saccade evidence ZIP: `e4c_saccade_tier_batch.zip`, SHA-256 `73e2c931fcf34809f1c11af7bd605167661e51ee2a4dee0db61ba1b201870183`. Runner evidence ZIP: `C11E_E4C_SACCADE_BATCH_RUNNER_4ad0e5e404c043c4b042e2cf172d1214.zip`, SHA-256 `fa9bc7c792dcdbfbfa5f1676b6200edea313d022b0e9ac3b6edf3eb9d085ed49`.
- Saccade uses `CIRCUIT_PULSE`, canonical SHA `daba3fa558f6898a17107ab68894d15c58fa5b2127e8da7d7b11b203f4ddfaa1`, and 90+510+90 = 690 frames / 23 seconds. Runtime pins 37/37 pre/post equal. The evidence ZIP contains BATCH_RESULT, locks, authorization, row summaries/logs and hashes; full media/full receipts remain in the active project at the recorded paths.
- Peripheral Scan is the final E4C family: `peripheral_scan/tier-1..tier-5`, `ORBITAL_RITUAL`, canonical SHA `aaf50f9223bad678df15589110dfcd6ff42dda89326a0a84bc5a5f51d133a904`, 510 native gameplay frames /17s plus 90/90 presentation = 690 frames /23s. It has 38 runtime pins and three physical 91-file inventories per tier.
- Authorized package: `C11E_E4C_PERIPHERAL_SCAN_COMBINED_OVERLAY_V2_20261116.zip`. One explicit `-ExecuteBatch` invocation installs 21 ADD_ONLY files, persists immutable installation receipts, runs all gates and staged/installed PREPARE_ONLY checks, then launches the five-tier batch once. No separate runner invocation and no caller-supplied BatchId.

## E4C acceptance matrix

| Family | Technical | Operator A/V | Accepted |
|---|---:|---|---:|
| Tracking | 5/5 PASS | Approved | 5/5 |
| Pursuit | 5/5 PASS | Approved | 5/5 |
| Saccade | 5/5 PASS | Approved | 5/5 |
| Peripheral Scan | 0/5 | Pending | 0/5 |
| **Total** | **15/20** |  | **15/20** |

## Immutable baseline and governance

- C11-C 2.19.12 remains frozen. `release/C11C_FREEZE_PACKAGE_MANIFEST.json`: 796,318 bytes; SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- No changes to protected C11-C mechanics/generators, simulation truth, canonical locks, core audio, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector` or `RenderedFrameStream`.
- No new Producer, binder, renderer, compositor or mechanic. The family coordinator uses the existing CLI and D-owned execution/composition path only.
- `E1=PREPARE_ONLY`; `family_adapter=NOT_CONNECTED_E1`; `PRODUCTION_DISPATCH=FALSE`; `RELEASE_AUTHORITY=NONE`.
- `GIT_CHECKS=SKIPPED`; commits are `OPERATOR_MANAGED`; `SOURCE_FILE_PINS=ENFORCED`.
- Every family tier is one-shot. Driver-generated BatchId is reserved only after collision checks and authorization persistence. Any failure after reservation consumes that ID permanently; preserve evidence and never retry it.

## Next gates

1. Run the Peripheral Scan combined overlay once with `-ExecuteBatch`. A pre-commit install failure and a post-commit batch failure have different recovery policies; preserve the relevant journal/receipt/lock/logs and never rerun automatically.
2. Audit ZIP, manifest, immutable install receipt/journal, 20 postimages, 38 source pins, frozen manifest, batch launch receipt, combined execution receipt, BATCH_RESULT, five full qualification receipts/media hashes and 91-entry inventories.
3. Obtain explicit operator visual/audio approval for all five Peripheral Scan tiers.
4. E4C closes only at 20/20 accepted. E5 remains blocked until then; sequence E5 → E6 Smoke18 → E7 Matrix101 (CH_008/CH_009 remain held for 11s-vs-12s mismatch; 99 provisional runnable) → E8.

Historical authority snapshots V169 and earlier are retained for audit and superseded by this V170. Do not use older next-action statements as current.
