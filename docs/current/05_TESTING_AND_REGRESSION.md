# Testing and Regression — C11-C 2.19.12

## Current status

The repository is under consolidated repair acceptance. The former 2.19.2 freeze claim is not the current acceptance authority.

The 2.19.12 consolidated candidate retains the worker-isolation contract and Suite checks for retired-studio isolation. Runtime Windows/Godot proof of concurrent capture remains an explicit acceptance gate.

## Canonical logical commands

```powershell
python .\c11c-suite\self_test.py
python .\c11c-suite\c11c-producer\self_test.py
python .\c11c-suite\c11c-producer\test_producer_gui_contract.py
python .\tests\run_all.py
```

Focused worker contract:

```powershell
.\c11c-suite\c11c-test\run_suite.bat C11CParallelReviewWorkerIsolationContractTest.gd
```

## Runtime concurrency proof

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\tools\prototypes\c11c_bulk\run_c11c_art_direction_batch_v4.ps1 `
  -Workers 7 `
  -Loops `
  -Reset
```

The run must report `MAX_OBSERVED_CONCURRENCY` greater than one. A one-at-a-time run is a failure of the C11-C 2.19.12 concurrency contract.

## Full candidate gate

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\FULL_ACCEPTANCE_C11C_2.19.12.ps1
```

Physical production success does not replace logical regression, and a static concurrency contract does not replace a real multi-worker capture.
