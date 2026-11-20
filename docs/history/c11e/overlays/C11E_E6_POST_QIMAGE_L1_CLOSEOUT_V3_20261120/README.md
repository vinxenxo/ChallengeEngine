# E6 QImage L1 closeout and Loop source gate — V3 overlay

**Date:** 2026-11-20  
**Status:** V2 read-only phase reconciliation PASS; visual resampler review and Loop source closure remain OPEN.

## Why this overlay exists

This overlay records the operator-confirmed completion of the V2 reconciliation correction and establishes the next two independent E6 gates. It supplements, and does not rewrite, the V1 incident overlay or V2 correction overlay.

## Closed in this checkpoint

- V2.7 Option C native Qt/QImage L1 synthetic pixel-stage result: `PASS_QIMAGE_STAGE_BENCHMARKED_NOT_END_TO_END`; 37/37 QImage tests; seven benchmark iterations; P50 4.7681 ms; P95 5.5743 ms.
- V2 read-only phase reconciliation: 18/18 checks PASS.
- V2 focused tests: 21/21 PASS.
- V2 package installation: ADD_ONLY; 18/18 files verified; 15/15 documentation/prompt files verified in repository destinations.
- V1 null optional byte-count defect closed by V2. SHA-256 remains mandatory; byte count is checked exactly when declared; malformed declared values remain fail-closed.

## V2 operator evidence

| Evidence | Value |
|---|---|
| V2 install receipt SHA-256 | `deb78605c224398dc6f612c157aacba901b34270eb8c198ca4968b00be4de36e` |
| V2 phase reconciliation receipt | `artifacts/tests/c11e/e6_post_qimage_l1_reconciliation_v2/E6L1RECONV2_20261119T233934Z_11996B28/C11E_E6_POST_QIMAGE_L1_PHASE_RECONCILIATION_RECEIPT_V2.json` |
| V2 phase reconciliation receipt SHA-256 | `24c2a4f09901a3d1c888d972aabf2a7016496f48e5011b512a1e261338d72474` |
| V2.7 QImage receipt SHA-256 | `95819ea730283ded149faa490b21e0df392341366a853b3c0913318fb203d783` |
| V2.7 installer receipt SHA-256 | `48dc18147f2e2f3eaed4b72d42df1d97fa39eb20b0a464eea9debc6b3acd6173` |

## What is not closed

- Human visual decision for Qt `SmoothTransformation` remains pending. PNG integrity is not a visual quality decision.
- Read-only closure of actual Loop frame/source/selector/PTS/timebase/pixel-layout/color/lineage remains pending.
- D-only one-frame consumer, six-selector Loop proof, Challenge runtime readback and Drill runtime readback remain independent gates.
- `E6_ACCEPTED=0`; Smoke18 remains draft/unarmed; D4.8 V2 remains immutable/BLOCKED; renderer/media/dispatch remain OFF; release authority remains NONE.

## Repository installation destinations

This overlay belongs under `docs/history/c11e/overlays/`. Current state belongs under `docs/current/e/`; continuation prompts belong under `prompts/`. No project documentation is to be installed into Downloads.
