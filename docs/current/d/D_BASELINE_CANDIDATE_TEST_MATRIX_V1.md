# C11-D Baseline Candidate Test Matrix V1

| Gate | Assertion | Current expected result |
|---|---|---|
| Historical reference | C11-C manifest SHA-256 equals the frozen identity | PASS |
| C inventory | Every historical manifest path exists at source or is exactly reconciled by the verified legacy quarantine ledger/archive | PASS only when source/archive disposition is valid |
| C protected source | Each protected path matches its historical byte count and SHA-256 | PASS |
| D extension isolation | Historical-manifest differences are inside declared D integration/documentation roots | PASS |
| Operator topology | Exactly the five canonical surfaces are registered | PASS |
| D9.14 | Real-media gate is not falsely promoted | BLOCKED_AS_REQUIRED |
| D9.15 | Operator evidence remains required until the five-surface ledger exists | BLOCKED_AS_REQUIRED |
| D9.16 | Full acceptance is not inferred from preflight | BLOCKED_AS_REQUIRED |
| D9.17 | NO-GO closure adjudication remains recorded | BLOCKED_AS_REQUIRED |
| Legacy surface | `c11d-control` remains unregistered; quarantine requires explicit operator action | DISPOSITION_REQUIRED |
| Freeze/release | Candidate audit creates no archive/media and grants no authority | PASS |

The overall tool exit code is zero if integrity checks pass and the open gates remain fail-closed. Overall wording is `PREFLIGHT_PASS_CANDIDATE_FREEZE_BLOCKED_AS_REQUIRED`; this must not be shortened to `FREEZE PASS` or interpreted as freeze eligibility.
