# C11-E Installer Incident Register — V56

**Date:** 2026-11-19

## New closed incidents

| Package | Incident | Disposition |
|---|---|---|
| Option C V2.4 | `Expand-Archive` failed before installer extraction due legacy path budget; installer was never invoked | CLOSED AS EXTRACTION FAILURE; no V2.4 install transaction |
| Option C V2.6 | PS5.1 parsed `-and` as a `Test-Path` parameter in a `Where-Object` expression during post-write documentation verification | CLOSED; rollback PASS removed 16 owned additions; no PASS receipt |
| Option C V2.7 | Short-path transaction/docs repair and source-pinned QImage runner | PASS_ADD_ONLY 18/18; docs 11/11; 8/8 bootstrap; 37/37 QImage; P95 5.5743 ms |

## Retained evidence
- V2.7 install receipt: `artifacts/tests/c11e/e6_qt_install/E6QTI27_20261119T225450Z_CBA13490/r.json`, SHA `48dc18147f2e2f3eaed4b72d42df1d97fa39eb20b0a464eea9debc6b3acd6173`.
- V2.7 QImage receipt: `artifacts/tests/c11e/e6_option_c_native_qt_probe_v2_7/E6OPTCQTV2_7_20261119T225516Z_6DCBCB1C/C11E_E6_OPTION_C_NATIVE_QT_PROBE_RECEIPT_V2_7.json`, SHA `95819ea730283ded149faa490b21e0df392341366a853b3c0913318fb203d783`.

## Permanent installer rules
- PS5.1 AST self-parse for each script.
- Preflight complete ZIP/member hashes, source pins, destination collisions, reparse points and route budgets before the first write.
- Explicit `foreach` for complex predicate counts; avoid cmdlet parameter-binding ambiguities.
- Add-only; no overwrite; rollback only the exact postimages created by the current transaction.
- Docs must be verified under repository `docs/` paths before issuing PASS.
- Failure: `NO_PASS_EMITTED=TRUE`; preserve receipt/logs; do not rerun predecessor tests blindly.
