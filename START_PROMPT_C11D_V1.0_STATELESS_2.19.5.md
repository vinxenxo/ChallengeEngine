# START PROMPT — ChallengeEngineV01_STATELESS / C11-C 2.19.5

You are continuing the ChallengeEngineV01_STATELESS project.

Current authoritative project state:
**C11-C 2.19.5 CONSOLIDATED REPAIR CANDIDATE — NOT FROZEN.**

Before changing anything, read:
- `AGENTS.md`
- `docs/current/c11c/C11-C_2.19_CURRENT_STATE.md`
- `docs/current/c11c/C11-C_2.19.5_ACCEPTANCE_GATE.md`
- `MASTER_HANDOVER_C11D_V1.0_STATELESS_2.19.5.md`

## Current objective

Finish workstation acceptance of the consolidated 2.19.x toolchain, freeze only after all gates pass, then begin C11-D recovery. Do not add another isolated micro-patch if a defect belongs in the consolidated candidate.

## Known repair facts

- Art Direction workers must remain parallel (`-Workers 7`).
- The historical 540x960/720x1280 regression came from multiple workers mutating the same project-root `override.cfg`.
- The repaired architecture has one batch-owned 720x1280 override plus `C11C_SHARED_MOVIE_OVERRIDE=1` inherited by all workers.
- Direct single-test execution is bounded at 120 seconds.
- `C11CParallelReviewWorkerIsolationContractTest.gd` and `C11CVisualDrillReviewEnvelopePathContractTest.gd` are static contract tests and must exit without launching render tooling.
- `c11c-suite` is canonical. `c11c-studio` is retired and must not be updated or used.

## Required next commands

```powershell
python .\c11c-suite\self_test.py
python .\c11c-suite\c11c-producer\self_test.py
.\c11c-suite\c11c-test\run_suite.bat C11CParallelReviewWorkerIsolationContractTest.gd
.\c11c-suite\c11c-test\run_suite.bat C11CVisualDrillReviewEnvelopePathContractTest.gd
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\qa\c11\verify_c11c_suite_launchers.ps1
```

Then run the focused contracts and representative game tests from the acceptance gate.

Only if those pass, run the parallel Art Direction review and then the remaining full acceptance suite.

## Hard boundaries

Do not alter C11-B simulation truth, RNG ownership, `SimulationResult`, `winning_frame`, `close_calls`, `RenderedFrameStream`, C7 audio contracts, C9 semantics or 540x960 logical social geometry as part of a C11-C tooling repair.

## Freeze condition

No freeze declaration while any test hangs, any launcher references `c11c-studio`, workers are silently serialized, or any render falls back to 540x960 during the 720x1280 review corpus.
