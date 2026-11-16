# E4C Visual Drill Execution Plan — V58 (2026-11-16)

## Accepted family state

| Family | Technical | Operator visual/audio | Accepted |
|---|---:|---|---:|
| Tracking | 5/5 | Approved | 5/5 |
| Pursuit | 5/5 | Approved | 5/5 |
| Saccade | 5/5 | Approved | 5/5 |
| Peripheral Scan | 0/5 | Pending | 0/5 |
| **Total** | **15/20** |  | **15/20** |

Saccade batch `E4C-SACCADE-T1-5-20261115T235737Z-57fdf44b` completed all five technical rows and has explicit operator A/V approval. It is accepted 5/5 and must not be rerun.

## Remaining family — Peripheral Scan

- Selectors `peripheral_scan/tier-1..tier-5`, family music `ORBITAL_RITUAL`, independent one-shot tiers.
- Canonical SHA `aaf50f9223bad678df15589110dfcd6ff42dda89326a0a84bc5a5f51d133a904`; 510 gameplay frames /17s; presentation 90/510/90 =690 frames/23s/30fps.
- 38 runtime pins; three equal physical 91-source snapshots per tier; A/B music repeatability, changed-C distinction, A/C video bitstream isolation and exact FFprobe contract.

## Authorized combined operation

One combined V2 overlay uses `-ExecuteBatch`. It performs all gates, commits 21 ADD_ONLY files and immutable install receipt/journal, then launches the installed five-tier runner once and writes launch/combined receipts. No separate runner, caller-supplied BatchId or automatic retry. Batch failure after install commit does not rollback the installed files.

E4C remains open at 15/20 until Peripheral Scan has five technical PASS rows and explicit operator A/V approval for all five. E5 remains blocked until then.
