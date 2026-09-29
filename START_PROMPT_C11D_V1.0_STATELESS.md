# START PROMPT — ChallengeEngineV01_STATELESS / C11-C 2.19.5

Continue the ChallengeEngineV01_STATELESS project from:
**C11-C 2.19.5 CONSOLIDATED REPAIR CANDIDATE — NOT FROZEN.**

Read first:

1. `AGENTS.md`
2. `docs/current/c11c/C11-C_2.19_CURRENT_STATE.md`
3. `docs/current/c11c/C11-C_2.19.5_ACCEPTANCE_GATE.md`
4. `docs/current/c11c/C11-C_2.19_DOCUMENTATION_INDEX.md`
5. `MASTER_HANDOVER_C11D_V1.0_STATELESS.md`

## Mandatory current decisions

- Preserve genuine Art Direction parallelism. `-Workers 7` must remain functional.
- The batch owns one 720x1280 Movie Maker override for the whole parallel stage.
- Workers inherit `C11C_SHARED_MOVIE_OVERRIDE=1` and never mutate/remove project-root `override.cfg`.
- Do not serialize workers as a workaround.
- The two review contract tests are source-only and must terminate without render processes.
- `run_suite.bat` is bounded at 120 seconds.
- `c11c-suite` is canonical.
- `c11c-studio` is retired and must not be updated or used.
- `c11c-maintenace` is compatibility-only and delegates to `c11c-maintenance`.

## First commands

```powershell
python .\c11c-suite\self_test.py
python .\c11c-suite\c11c-producer\self_test.py
.\c11c-suite\c11c-test\run_suite.bat C11CParallelReviewWorkerIsolationContractTest.gd
.\c11c-suite\c11c-test\run_suite.bat C11CVisualDrillReviewEnvelopePathContractTest.gd
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\qa\c11\verify_c11c_suite_launchers.ps1
```

Then follow `docs/current/c11c/C11-C_2.19.5_ACCEPTANCE_GATE.md`.

## No micro-patch cycle

Any further defect found in this acceptance cycle must be consolidated into the current 2.19.x candidate and reflected in current-state, acceptance and handover documentation. Do not restart a one-file patch chain.

## Freeze condition

No freeze while a direct test hangs, launcher verification fails, workers are serialized, a launcher references `c11c-studio`, or a 720x1280 review worker records 540x960.
