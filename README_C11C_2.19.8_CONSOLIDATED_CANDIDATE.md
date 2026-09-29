# C11-C 2.19.8 - Consolidated Repair Candidate

This archive is an overlay for the existing workstation-validated C11-C 2.19 functional state. It consolidates the 2.19 documentation/tooling line and fixes the canonical complete-video-review PowerShell parser failure.

It does **not** reopen or alter C11-C visual mechanics, worker isolation implementation, C11-B simulation truth, RNG ownership, C7 audio contracts, C9 semantics or logical 540x960 geometry.

## Apply

Extract the ZIP at the repository root with overwrite enabled. No wrapper folder is used.

## Verify

Run:

```powershell
python .\c11c-suite\self_test.py
python .\c11c-suite\c11c-producer\self_test.py
python .\c11c-suite\c11c-producer\test_producer_gui_contract.py
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\qa\c11\verify_c11c_suite_launchers.ps1
.\c11c-suite\c11c-test\run_suite.bat C11CParallelReviewWorkerIsolationContractTest.gd
python .\tests\run_all.py
```

Then run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\FULL_ACCEPTANCE_C11C_2.19.8.ps1
```

The candidate is not frozen.
