# C11-E E6 — phase ledger and next gates — V21

**Date:** 2026-11-19. This ledger carries accepted evidence forward and records the V2 correction. It does not accept E6 or authorize rendering.

## Current exact state

| Item | State | Evidence / constraint |
|---|---|---|
| C11-C 2.19.12 | FROZEN / IMMUTABLE | Manifest 796,318 bytes / SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` |
| D4.8 V2 | BLOCKED | 12,996 bytes / SHA `0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07`; unchanged |
| Option C architecture | Operator-approved | Single D-only post-compositor; source C immutable; distinct D output |
| Option C geometry V3 | APPROVED_GEOMETRY_RETAINED_RESAMPLER_IMPLEMENTATION_ONLY | 720×1280 / content 504×896 @ (108,192) / black bands & gutters |
| Python compositor V4 | NOT HOT-PATH QUALIFIED | Windows P95 2050.1467ms, 0.48777 fps |
| QImage probe V1 | BLOCKED BY RUNNER DEFECT | A3 comparator false negative; 0/37 tests executed; receipt retained |
| QImage probe V2 | PENDING WINDOWS EXECUTION | Corrected adjudicator; then 37 tests and 7-iteration benchmark |
| Resampler quality | NOT APPROVED | Synthetic visual review is not real Loop content approval |
| E6 | ACCEPTED 0 | Probe tests are not E6 rows or rendered videos |
| Renderer/dispatch/media | OFF | No process execution until exact successor policy + execution manifest |
| E1 | PREPARE_ONLY | Existing shared service remains single seam |
| D9.10 | PREPARE_ONLY | No D9.10 dispatch |
| D9.14/D9.16 | BLOCKED | No bypass |
| D9.17 | BLOCKED_NO_GO | No bypass |
| D10 | BLOCKED_FOR_PROMOTION | `release_authority=NONE` |

## Reconciliation and coverage

- Smoke18 contains 18 top-level rows (6 Challenge, 6 Loop, 6 Drill); nested Challenge A/B/C probes do not increase the top-level row count.
- Reuse requalification has 13 candidate rows and zero E6-accepted rows. CH004 semantic non-interference only enables ledger requalification; it is not E6 acceptance.
- The six Loop A/V closeout artifacts are reuse candidates; six Smoke18 D-composited Loop outputs are still outstanding.
- Six Drill A/V closeouts and their nested refs are reusable candidates; they do not replace Smoke18 acceptance predicates.
- Five fresh Challenge A/V outputs remain, in addition to existing nested probes.
- CH_008/009 remain held (11-second declaration vs 12-second phase sum). Matrix101 is not frozen.

## Ordered next steps

1. Install V2 add-only and run it on Windows 11 / Python 3.13.14 / PySide6 6.11.2. Confirm A3 PASS, QImage 37/37 and P95 <=33.333ms. This only qualifies a synthetic native pixel stage.
2. Review the QImage preview outputs and explicitly qualify/decline `SmoothTransformation` quality. Geometry approval does not imply resampler quality approval.
3. Perform source closure against the actual immutable C input and D9.9/D9.10/R1P metadata; establish that the real per-frame input is exact RGB24, ordered and separately pinned. Do not use a guessed decoder path.
4. Obtain a narrowly scoped successor to D4.8 and an E6 TEST_ONLY execution manifest identifying exact executable paths, hashes, versions, arguments, inputs, output roots, and prohibited side effects.
5. Only then perform a one-selector copied-frame proof (L2), negative controls and human review (L3), widen the same consumer to six Loop selectors (L4), then integrate eligible rows into Smoke18 (L5).
6. In parallel, maintain the full C→E coverage map for Challenge/Loop/Drill; do not equate Smoke18 with full historical acceptance.
7. Finish E5 seed/family isolation and GUI/CLI parity, E6 Smoke18, E7 Matrix101, historical regression, E8 independent acceptance and a separate promotion decision.

## Permanent operating constraints

`GIT_CHECKS=SKIPPED`; `COMMITS=OPERATOR_MANAGED`; `SOURCE_FILE_PINS=ENFORCED`. Active checkout is the sole authority. Evidence ZIPs are never applied over it. No C11-C generator/mechanics/core audio/manifest changes, no sixth module, no parallel Producer, binder or family adapter. `request.seed` and `request.music_seed` stay orthogonal. C11-C remains production authority until E8 plus explicit promotion.
