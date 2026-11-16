# C11-D to C11-E Full Family Roadmap — V111 (2026-11-16)

## Current checkpoint

E4C is **15/20 accepted**. Tracking, Pursuit and Saccade are each 5/5 and operator-approved. Peripheral Scan is the sole remaining family at 0/5.

## Execution sequence

| Order | Phase | Entry condition | Exit condition |
|---:|---|---|---|
| 1 | E4C Peripheral Scan | Combined V2 overlay gates pass; `-ExecuteBatch` | Five technical PASS rows and five operator A/V approvals; E4C 20/20 |
| 2 | E5 | E4C 20/20 accepted | E5 scope-specific qualification gates pass |
| 3 | E6 Smoke18 | E5 accepted | 18 smoke scenarios pass |
| 4 | E7 Matrix101 | E6 accepted | 101 rows or approved disposition; CH_008/009 remain held for 11s-vs-12s duration mismatch; 99 provisional runnable |
| 5 | E8 | E7 disposition accepted | Regression evidence, independent acceptance and governed transition decision |

## Peripheral Scan contract

- Five independent, one-shot selectors: `peripheral_scan/tier-1` through `peripheral_scan/tier-5`.
- Family music `ORBITAL_RITUAL`; canonical `definitions/visual_drill_peripheral_scan_canonical.json`, SHA `aaf50f9223bad678df15589110dfcd6ff42dda89326a0a84bc5a5f51d133a904`.
- Native gameplay 510 frames /17s/30fps; D presentation 90 PRE_ROLL + 510 GAME + 90 END_CTA = 690 frames /23s.
- Each tier proves three equal physical 91-file inventories (pre-execution, immediately-before-renderer and post-execution); runtime pins 38/38 equal pre/post.
- Video H.264 High, 720x1280, yuv420p TV, 30fps, 690 frames; audio AAC-LC 48kHz stereo, zero A/V start drift. A/B same-seed music identical; changed-seed C distinct; A/C video bitstreams identical.

## Combined install and execute

`C11E_E4C_PERIPHERAL_SCAN_COMBINED_OVERLAY_V2_20261116.zip` contains the single installer entry point. One explicit `-ExecuteBatch` invocation verifies archive, manifest, sources, frozen C11-C, PowerShell, Python, atomic I/O and staged/installed PREPARE_ONLY; commits exactly 21 ADD_ONLY files and immutable install receipt/journal; then launches the installed runner once. The driver creates its own BatchId after collision checks. No separate runner command, no caller-supplied BatchId, no automatic retries.

A batch failure after install commit preserves the committed installation and all batch evidence. E4C requires operator A/V acceptance in addition to technical PASS; E5 remains blocked until 20/20.

## Architecture objective

The long-term objective is a validated, governed transition from C to D+E as the video factory. This roadmap does not promote E1, enable production dispatch or grant release authority. C11-C remains the immutable reference baseline until independent closeout and governance gates are satisfied. Historical V110 and earlier are superseded.
