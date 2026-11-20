# C11-E Installer Incident Register — V58

**Date:** 2026-11-20

## Closed predecessor incidents

| Package | Incident | Disposition |
|---|---|---|
| Option C V2.4 | `Expand-Archive` path budget failure before installer invocation | CLOSED AS EXTRACTION FAILURE; no V2.4 install transaction |
| Option C V2.6 | PS5.1 parsed `-and` as a `Test-Path` parameter in documentation verification | CLOSED; rollback PASS removed 16 owned additions; no PASS receipt |
| Option C V2.7 | Short-path transaction/docs repair and source-pinned QImage runner | PASS_ADD_ONLY 18/18; docs 11/11; bootstrap 8/8; QImage 37/37; P95 5.5743 ms |
| E6 L1 reconciliation V1 | `expected_bytes=null` incorrectly treated as required exact size | CLOSED BY V2; 21/21 tests and 18/18 read-only checks PASS |

## V1 phase-reconciliation incident — final disposition

- V1 blocked receipt SHA: `5c231dba4ebd3eab1520506e45bdcb4572367755f01fa0c5befdd2ba391dbed0`.
- Four affected source rows had exact expected/actual SHA-256 equality and `expected_bytes=null`.
- V2 kept SHA-256 mandatory; enforced exact byte count only when declared; malformed declared values still block.
- V2 install receipt SHA: `deb78605c224398dc6f612c157aacba901b34270eb8c198ca4968b00be4de36e`.
- V2 read-only reconciliation receipt SHA: `24c2a4f09901a3d1c888d972aabf2a7016496f48e5011b512a1e261338d72474`; 18/18 PASS.
- V1 blocked receipt remains preserved; no historical source receipt was rewritten.

## Permanent installer/documentation rules

- PS5.1 AST self-parse for each PowerShell installer/runner on target.
- Preflight complete ZIP/member hashes, self pin, immutable C11-C/D4.8 pins, destination collisions, reparse points and path budgets before first write.
- Add-only; no overwrite; rollback only exact postimages owned by the current transaction.
- Historical documentation goes into a versioned `docs/history/c11e/overlays/<overlay>/` directory. Current documents go to `docs/current/e/`; prompts go to `prompts/`.
- Project documentation must be verified in repository destinations before PASS; it must not be left only in Downloads.
- Failure emits no PASS; preserve receipts/logs and isolate the failing condition before creating a recovery package.
