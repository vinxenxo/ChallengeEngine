# C11-C Suite 0.1.4 — Operational Rules

## Ownership

`c11c-suite/` is the canonical active Suite. `c11c-studio/` is retired and must not be updated, imported or required for operation.

## Launcher contract

Operational Suite BAT/CMD launchers resolve the repository through `C11C_PROJECT_ROOT`, change to the project root and propagate the child exit code. `c11c-maintenace/run.bat` is compatibility-only and delegates to `c11c-maintenance/run.bat`.

The 2.19.6 final repair normalizes active BAT launchers to UTF-8 without BOM. It does not change their command semantics.

## Art Direction worker contract

`run_c11c_art_direction_batch_v4.ps1 -Workers 7` uses isolated project roots and a per-worker class-cache bootstrap. Initialization is sequential; Movie Maker capture is concurrent. Global mutexes are prohibited.

## Contract-test lifecycle

Command-line Godot tests using `extends SceneTree` must enter through `_initialize()` and must terminate explicitly.

## Validation

```powershell
python .\c11c-suite\self_test.py
python .\c11c-suite\c11c-producer\self_test.py
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\maintenance\verify_c11c_2_19_6_final_repair.ps1
.\c11c-suite\c11c-test\run_suite.bat C11CParallelReviewWorkerIsolationContractTest.gd
python .\tests\run_all.py
.\FULL_ACCEPTANCE_C11C_2.19.6.ps1
```
