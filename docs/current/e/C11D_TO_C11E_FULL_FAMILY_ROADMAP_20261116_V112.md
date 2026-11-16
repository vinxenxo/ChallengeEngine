# C11-D to C11-E Full-Family Roadmap — V112 (2026-11-16)

## Current checkpoint

E4C is **20/20 accepted and closed**. Tracking, Pursuit, Saccade and Peripheral Scan are each 5/5 technically qualified and operator-approved. Peripheral Scan closeout is `C11E_E4C_PERIPHERAL_SCAN_FAMILY_CLOSEOUT_20261116_V1.md`.

## Execution sequence

| Order | Phase | Entry condition | Exit condition |
|---:|---|---|---|
| 1 | E4C | Closed | 20/20 accepted; no family reruns |
| 2 | E5 Cross-family qualification | E4C 20/20; E5 plan/inventory reviewed | Determinism, seed isolation, adapter/profile non-leakage and GUI/CLI parity pass across Challenge, Loop and Drill |
| 3 | E6 Smoke18 | E5 accepted | 18 A/V smoke scenarios pass: six per family |
| 4 | E7 Matrix101 | E6 accepted | 101 rows or approved disposition; CH_008/CH_009 held for 11s-vs-12s mismatch; 99 provisional runnable |
| 5 | E8 | E7 disposition accepted | Historical regression, independent acceptance, immutable freeze and governed transition decision |

## E5 opening canary — operator proposal adopted

The proposed single test that launches Challenge, Visual Loop and Visual Drill is appropriate as the **first E5 cross-family canary**. It should not be an unqualified ad-hoc batch and must not be described as E6 Smoke18.

Use one representative family contract per route, selected from accepted active-checkout definitions. Run fresh E5-scoped requests through the existing shared E1 service from both CLI and the current Producer GUI. Verify:

- same-request deterministic replay;
- fixed gameplay seed with independent music seed;
- A/B repeatability and changed-music-seed C distinction;
- changing gameplay seed does not perturb the music stream when the music seed is held fixed;
- no Challenge/Loop/Drill profile, binder, grammar or timeline leakage;
- GUI and CLI parity because both call the same business service;
- media/container/codec/timeline/audio QA, immutable receipts and source-pin stability.

The canary is a design/entry test for the E5 scope. Before implementation, record the exact three selectors, each family's native canonical/timebase, family music route/profile, gameplay/music seeds, GUI/CLI request equality, expected output cardinality and evidence paths. Do not infer these from another family or reuse E4 batch IDs. No E4 acceptance evidence is regenerated.

## Remaining phases

- **E6 Smoke18:** six audiovisual scenarios per family (Challenge 6, Loop 6, Drill 6). This is broader than the three-family E5 canary.
- **E7 Matrix101:** 54 Challenge + 27 Loop + 20 Drill. CH_008/CH_009 remain held until the 11-second declared duration versus 12-second phase sum is reconciled; 99 remain provisional runnable.
- **E8:** complete historical C11-C corpus reconciliation, row-by-row regression evidence, independent acceptance, immutable freeze and an explicit separately governed C-to-D+E transition decision.

## Architecture and governance

C11-C 2.19.12 remains the immutable reference baseline. Preserve each family's binder, grammar, timeline, music and mechanics. Shared orchestration is not permission to flatten family semantics or add a parallel Producer/binder/renderer. E1 remains PREPARE_ONLY, production dispatch false and release authority NONE until E8 and separate governance approval.
