# C11-E Gates and Acceptance Matrix — V26

**Date:** 2026-11-03  
**Checkpoint:** E3 GUI audio pilot manually reviewed PASS; V1.5 negative controls prepared, not yet run.

| Gate | Status | Evidence / outstanding item |
|---|---|---|
| E0 foundation | PASS | Retained; no rerun |
| E1 shared service | PASS | GUI/CLI semantic identity; CLI separate-process adapter test retained |
| E2 R4 | PASS | Bounded CH001 A/B source-frame control only |
| E3.2 D3 V5/E1 | PASS | Contract/binding and source pins accepted |
| E3 V1.3 | PASS_APPLIED | Do not reapply |
| E3 V1.4 automated | PASS 31/31 | Python 3.13.14; compile PASS; old pins only |
| E3-GUI-01 | PASS | Existing Producer GUI launched, control invoked worker via QProcess |
| E3 physical audio/mux pilot | PASS | Receipt SHA `910d600e06dcdb2356f9f787fd0c82d45db203e35b471cd5c7cdba10d6ec5aab` |
| E3 operator A/C review | PASS_USER_CONFIRMED | User confirms expected renders/audio without defects |
| E3 V1.5 negative controls | READY_NOT_RUN | New 19 tests + full 31 prior regression = 50 expected |
| E3 formal closure | PENDING | Close only after V1.5 Windows suite PASS |
| E4A Challenge | NOT_STARTED | Full Challenge D presentation/layout/editorial integration |
| E4B Visual Loop | NOT_STARTED | Grammar-aware binding/editorial/layout + existing family music |
| E4C Visual Drill | NOT_STARTED | Phase and END_CTA precedence + family music |
| E5 cross-family | NOT_STARTED | All families; seed domains, determinism, CLI and GUI paths |
| E6 Smoke18 | NOT_STARTED | 6 test cases per family |
| E7 Matrix101 | NOT_STARTED | 54 + 27 + 20; CH_008/009 held pending duration reconciliation |
| E8 independent acceptance | NOT_STARTED | Immutable freeze and explicit promotion authority |

## CLI / GUI development contract

Engineering is CLI-first where practical, followed by integration of the same scripts/service into the current low-fidelity Producer GUI. Both execution paths remain testable in this development phase; GUI dispatches existing scripts and contains no duplicated production logic. The later GUI-only operator workflow belongs to the future post-C-replacement production GUI. CLI remains available for automated compatibility and controlled testing.

## V1.5 acceptance rule

The E3 pipeline's final mux validation changes in V1.5. Consequently, the Windows runner must execute all `test_c11e*.py` tests (expected 50/50), not just the added 19. No gameplay render or production output is permitted. Failure blocks E3 closure and E4A start.

C11-C 2.19.12 remains the production baseline; frozen manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` remains immutable. `release_authority=NONE`; `baseline_promotion=false`; `freeze_eligible=false`.
