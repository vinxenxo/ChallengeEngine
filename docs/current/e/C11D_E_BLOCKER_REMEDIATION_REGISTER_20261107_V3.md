# C11-D / C11-E Blocker Remediation Register — V3

**Date:** 2026-11-07. This register distinguishes integration implementation from permission to execute a renderer or release.

| ID | Blocker | Current status | Required evidence / exit condition |
|---|---|---|---|
| B-E4B-INSTALL | V2 installer emitted `Argument types do not match` after backup preflight | V3 recovery verifies 6 source postimages, 15 add-only outputs and 6 source backups before it writes anything | V3 recovery receipt PASS; runner 25/25 + D9.8 + syntax PASS |
| B-E4B-PAYLOAD | Static contracts are not request-scoped media payloads | OPEN | 27 immutable actual payload receipts, one per Loop grammar |
| B-D-CONSUMER | D9.10 remains preparation-only; no accepted consumer reading source pixels | OPEN | D-only consumer proof at existing seam, preserving frame identity/order |
| B-D4.8 | Renderer baseline and execution authority | BLOCKED | Separate candidate, evidence, verifier, independent review and explicit approval |
| B-D9.15 | Operator evidence checkpoint | REVALIDATE | Live status tool and all referenced evidence in active checkout; snapshot omission is not live absence |
| B-D-BASELINE | D baseline validation / hook configuration | REVALIDATE | Run read-only diagnostic on active checkout; classify missing hook paths, do not invent or recreate protected hooks |
| B-D9.14 | D authority / policy gate | BLOCKED | Complete its specific evidence and authorization docket |
| B-D9.16 | D integration gate | BLOCKED | Prove real consumer and acceptance conditions; no plan-only inference |
| B-D9.17 | No-go gate | BLOCKED_NO_GO | Must be resolved by its explicit closure criteria, not bypassed |
| B-D10 | Promotion | BLOCKED_FOR_PROMOTION | E8 independent acceptance, immutable freeze and separate operator promotion approval |
| B-E4C | Drill family | NOT_STARTED | Preserve distinct timeline, binder and music contract after E4B visual acceptance |
| B-E5/E6/E7/E8 | Cross-family, Smoke18, Matrix101 and final acceptance | NOT_STARTED | Sequential entry criteria and evidence in roadmap/backlog |
| B-CH008/009 | 11s declaration vs 12s phase sum | HELD | Resolve temporal contract; 99 provisional runnable, not 101 |

## V2 PowerShell failure root cause

The V2 installer constructs `System.Collections.Generic.List[object]` through `New-Object` and later uses `@($sourceReceipts)` while building the receipt. Windows PowerShell 5.1 has a reproducible `ArgumentException: Argument types do not match` for this pattern. See https://github.com/PowerShell/PowerShell/issues/27558. The error is outside the guarded install transaction, so the V2 source patches/add-only writes likely completed before the receipt exception. V3 verifies the complete post-state and the six backups rather than assuming success.

## Closure policy

No blocker is waived by a test count, static selector match, operator policy decision or historical file presence. Do not modify C11-C frozen sources or invoke launchers/renderer/media under this register.
