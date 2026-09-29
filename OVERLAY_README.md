# C11-C 2.19.12 V19 - A1 StrictMode closure + freeze documentation

ROOT-RELATIVE INCREMENTAL OVERLAY

V19 is a surgical repair on V18. It fixes the observed Windows PowerShell 5.1 `Set-StrictMode -Version Latest` failure where `canonical_producer_manifest` was assigned to the per-run record after creation without being predeclared.

V19 also updates the active C11-C closure documentation and the C11-D entry handover so the next fresh context uses C11-C 2.19.12 as the intended immutable baseline after the final acceptance PASS.

Changed:
- tools/qa/c11/run_c11a1_challenge_bulk_qa.ps1
- tests/C11A1FactoryIsolationContractTest.gd
- MASTER_HANDOVER_C11C_2.19_CONSOLIDATED.md
- START_PROMPT_C11C_2.19_CONSOLIDATED.md
- docs/current/c11c/C11-C_2.19.12_CLOSURE_AND_FREEZE_READINESS.md
- docs/current/c11c/C11C_2.19.12_A1_CLOSURE_CHANGELOG_V19.md
- MASTER_HANDOVER_C11D_V1.0_STATELESS.md
- START_PROMPT_C11D_V1.0_STATELESS.md
- C11C_2.19.12_A1_CLOSURE_RECEIPT_V19.md

Not changed:
- no `core/` files;
- no simulation or mechanic files;
- no RNG implementation;
- no C7/C9 contracts;
- no authoritative `build_factory.py` recovery.

The V18 compatibility `build_factory.py` is intentionally left untouched. The operator has located the last historical copy and will supply it at freeze time. Its provenance and SHA-256 must be recorded in the final freeze receipt.

Apply at repository root with:

`Expand-Archive -LiteralPath <zip> -DestinationPath . -Force`

Fast validation:

`.\c11c-suite\c11c-test\run_suite.bat C11A1FactoryIsolationContractTest.gd`

`.\c11c-suite\c11c-test\test_powershell_parse.bat`

`.\FULL_ACCEPTANCE_C11C_2.19.12_A1_SINGLE.ps1 -ChallengeId CHALLENGE_001 -Seed 12345`

Final closure remains:

`.\FULL_ACCEPTANCE_C11C_2.19.12.ps1`
