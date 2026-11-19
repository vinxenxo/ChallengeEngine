# C11-E Installer Incident Register — V57

**Date:** 2026-11-20

## Closed predecessor incidents
| Package | Incident | Disposition |
|---|---|---|
| Option C V2.4 | `Expand-Archive` path budget failure before installer invocation | CLOSED AS EXTRACTION FAILURE; no V2.4 install transaction |
| Option C V2.6 | PS5.1 parsed `-and` as a `Test-Path` parameter in documentation verification | CLOSED; rollback PASS removed 16 owned additions; no PASS receipt |
| Option C V2.7 | Short-path transaction/docs repair and source-pinned QImage runner | PASS_ADD_ONLY 18/18; docs 11/11; bootstrap 8/8; QImage 37/37; P95 5.5743 ms |

## V1 phase-reconciliation incident — corrected by V2
- V1 audit receipt: `artifacts/tests/c11e/e6_post_qimage_l1_reconciliation/E6L1RECON_20261119T232143Z_582B5874/C11E_E6_POST_QIMAGE_L1_PHASE_RECONCILIATION_RECEIPT_V1.json`, SHA `5c231dba4ebd3eab1520506e45bdcb4572367755f01fa0c5befdd2ba391dbed0`.
- Failure was limited to `v2_7_qt_receipt.source_pins`.
- Four active source rows had exact expected/actual SHA-256 equality but `expected_bytes=null`; V1 compared actual size to null and incorrectly blocked them.
- V2 keeps SHA-256 mandatory and checks sizes exactly only when declared. Malformed non-null sizes still block. All other V1 checks were already passing.
- V1 failure receipt is preserved; V2 writes new paths and never mutates it.

## Permanent installer rules
- PS5.1 AST self-parse for each script.
- Preflight complete ZIP/member hashes, source pins, destination collisions, reparse points and route budgets before the first write.
- Add-only; no overwrite; rollback only exact postimages created by the current transaction.
- Docs verified under repository `docs/` and prompts under repository `prompts/` before PASS; no project documentation installed into Downloads.
- Failure: `NO_PASS_EMITTED=TRUE`; preserve receipts/logs; do not rerun predecessor tests blindly.
