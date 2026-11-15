# C11E_E4C_PURSUIT_TIMELINE_CONTRACT_RECONCILIATION_20261115_V2 — authoritative update

Date: 2026-11-15

## Root cause

The first Pursuit tier-batch attempt used a coordinator copied from Tracking and contained a fixed assumption of 810 video frames at 30 fps / 27.0 seconds, with phases PRE_ROLL=90, GAME=630 and END_CTA=90. Pursuit tier-1's child CLI had already completed successfully. Its batch summary reports 690 source/composed frames and the final A MP4 SHA-256 `c31632868968e24f29c88b435386efbcabb128ec6f28ffd35c8ebec8702d34f3`. The coordinator failed only after child completion with `pursuit/tier-1_NATIVE_TIMELINE_MISMATCH`; it did not prove a renderer failure.

## Native selector contract

The pinned `definitions/visual_drill_pursuit_canonical.json` has SHA-256 `dfe2bce9913df8ebe4f92d06eec5d22736338214e71b497dde3562a6927600bc`. Its payload declares 30 fps, 510 gameplay frames and 17.0 seconds. The existing D visual consumer uses a 3.0-second PRE_ROLL and a 3.0-second END_CTA: 90 frames each at 30 fps. Thus Pursuit is:

| Phase | Frames | Seconds |
|---|---:|---:|
| PRE_ROLL | 90 | 3.0 |
| GAME (Pursuit native) | 510 | 17.0 |
| END_CTA | 90 | 3.0 |
| **Total** | **690** | **23.0** |

The 810-frame / 27-second 90+630+90 example is valid for Tracking's 630 gameplay frames; it must not be generalized across Drill selectors. The D visual consumer already accepts the selector's dynamic gameplay frame count. No consumer or canonical source change is necessary.

## V5 code disposition

V5 replaces only the E4C Pursuit batch coordinator/tests/runner/runner-contract tests. The coordinator derives the expected frame counts from the pinned Pursuit definition and verifies the receipt, D composition phase counts, FFprobe video duration/frame count, A/V start alignment, codec profile and physical file SHA-256. For every successful row, it requires the receipt's three 91-entry source-pin inventories to be identical, unique, safe relative paths with positive byte counts and valid SHA-256 values; it then checks every file's actual size/hash.

The consumed V4 tier-1 output is never rerendered. Recovery requires the exact original one-shot lock, execution authorization, failed progress record, row-failure receipt, request and CLI summary; then it validates the full qualification receipt and existing A/C media/music. A newly generated V5 batch ID can execute only T2–T5. The runner's default is PREPARE_ONLY; `-Execute` remains explicit.

## Governance / acceptance boundary

The install is a test-only harness correction. It grants no release authority, does not turn renderer or dispatch on, does not change C11-C or its frozen manifest, and does not complete visual/auditory review. Operator must independently audit installation evidence, T1 recovery result, later T2–T5 A/V artifacts, and family acceptance. `GIT_CHECKS=SKIPPED`; commits remain operator-managed.

V5.1's installer was unusable because it addressed the atomic helper under the wrong staging directory and omitted dot-sourcing it. V5.3 corrects those installer-only defects and proves helper availability plus JSON atomic writing before transaction. This does not change the 690/23 Pursuit contract.

## V5.3 installer deep-hardening addendum — 2026-11-15

The first complete static review found that V5.3 still set `transaction_started=true` before making its four replacement backups. This was corrected: backup preparation/journaling now runs with `transaction_started=false`; every backup is hash/byte verified and persisted; all 20 targets are rechecked immediately before the transaction boundary; and each individual target is rechecked just before its atomic operation. The installer also scans ZIP member names and duplicate paths before extraction. The staged canonical fixture is copied to both `tests/fixtures` and `definitions`, matching the test imports and canonical path consumers. The staged suite now contains 37 Python tests. The receipt and failure record carry backup records.

Status is **BUILT, NOT INSTALLED**. The Linux build environment cannot execute Windows PowerShell 5.1, so native AST/atomic-I/O checks remain mandatory operator gates. No renderer or media generation is part of installation. V5/V5.1 remain invalid.

V5.3 refuerza además el límite transaccional: exige que existan previamente todos los directorios padre; comprueba el binding exacto de cada destino REPLACE con su payload; usa creación atómica exclusiva para ADD (no sobrescribe un destino concurrente); y limita el rollback a operaciones confirmadas o a la operación REPLACE en vuelo. Los temporales en vuelo se limpian en fallo. La suite Python se exige exactamente en 37/37 y la prueba atómica amplía a 7/7 con colisión ADD.
