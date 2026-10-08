# Producer 0.10.0 — Current State

**Version:** 0.10.0  
**Location:** `c11c-suite/c11c-producer`  
**D milestone:** D9.5.1  
**Backend logic modified:** false  
**C11-C backend fingerprint:** unchanged (`f7df994d8842183275bc331decd75762a153f3100248c7cc8b590e34c1347e2d`)

## Existing behavior preserved

Producer continues to expose its existing C11-C Challenges, Visual Loops and Visual Drills creation/review workflows, queue, QProcess execution and delivery profile behavior. This update is additive to the current app; it is not a new suite.

## Added D tab

`C11-D · REQUEST + PERSONALIZACIÓN` collects D4 Production Request and D4.3 editorial inputs, invokes canonical D4.6 planning and confirms D4.5 CLI parity. It writes isolated request/plan evidence under `artifacts/tests/c11d_d9/producer_gui/<request_id>/` and shows hashes, plan, personalization and reproduction command. It verifies D4.2, D4.3, D4.4, D4.6 and D4.7 receipts before performing the UI planning action.

## Governance

Plan-only boundary: execution false, renderer false, D4.8 BLOCKED, runtime authority NONE, release authority NONE. The six editorial inputs are request/plan values at this milestone; actual rendered-media effect is not certified until D9.5.2.

## Acceptance

Canonical helper contract: 90/90 core cases, 12/12 personalization cases, 4/4 negatives. `self_test.py` and `test_producer_gui_contract.py` PASS on the extracted source tree. Windows Qt launch, user interaction and real media generated through the new GUI tab remain pending.
