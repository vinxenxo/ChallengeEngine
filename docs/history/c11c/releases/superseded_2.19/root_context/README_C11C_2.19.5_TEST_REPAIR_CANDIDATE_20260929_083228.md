# C11-C 2.19.5 — Consolidated Test-Harness Repair Candidate

## What was found

The 2.19.4 parallel worker isolation contract test was declared as `extends SceneTree` but implemented its entrypoint as `_ready()`. Godot's command-line script mode uses a `MainLoop`/`SceneTree` initialization lifecycle; `_initialize()` is the documented callback. The test therefore started Godot but never reached its assertions or `quit()`.

## Repair

`tests/C11CParallelReviewWorkerIsolationContractTest.gd` now runs its body from `_initialize()`.

`c11c-suite/self_test.py` additionally asserts that this contract test contains `_initialize()` and does not contain `_ready()`.

## What was not changed

The worker implementation remains the true parallel design:

- one temporary Godot project root per worker;
- source `override.cfg` excluded from worker copies;
- `.godot` state isolated per worker;
- generated `artifacts/` excluded from worker copies;
- no project-global mutex;
- `Workers=7` remains a genuine concurrency contract.

## Verification

Focused test:

```powershell
.\c11c-suite\c11c-test\run_suite.bat C11CParallelReviewWorkerIsolationContractTest.gd
```

Runtime concurrency:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\tools\prototypes\c11c_bulk\run_c11c_art_direction_batch_v4.ps1 `
  -Workers 7 `
  -Loops `
  -Reset
```

The runtime acceptance is considered proven only when `MAX_OBSERVED_CONCURRENCY > 1` appears.
