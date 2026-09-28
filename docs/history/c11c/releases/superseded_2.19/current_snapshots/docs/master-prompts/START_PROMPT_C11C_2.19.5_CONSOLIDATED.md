# START PROMPT — ChallengeEngineV01_STATELESS — C11-C 2.19.5 Final Consolidation

Continue the repository from:

**C11-C 2.19.5 FINAL REPAIR CANDIDATE — NOT FROZEN.**

Read first:

1. `C11C_2.19.5_CONTEXT_INDEX.md`
2. `AGENTS.md`
3. `.continue/rules/CONTINUE.md`
4. `docs/master-prompts/MASTER_HANDOVER_C11C_2.19.5_CONSOLIDATED.md`
5. `docs/current/c11c/C11-C_2.19.5_CONSOLIDATED_STATE.md`
6. `docs/current/c11c/C11-C_2.19.5_ACCEPTANCE_GATE.md`

## Immediate objective

Verify the final repair candidate on Windows/Godot 4.7.1:

```powershell
python .\c11c-suite\self_test.py
python .\c11c-suite\c11c-producer\self_test.py
.\c11c-suite\c11c-test\run_suite.bat C11CParallelReviewWorkerIsolationContractTest.gd
```

Then prove real multi-worker operation:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\tools\prototypes\c11c_bulk\run_c11c_art_direction_batch_v4.ps1 `
  -Workers 7 `
  -Loops `
  -Reset
```

The output must show multiple worker slots active, `MAX_OBSERVED_CONCURRENCY > 1`, and 720×1280 Movie Maker captures. Do not replace this with a mutex or a one-at-a-time fallback.

Then run:

```powershell
python .\tests\run_all.py
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\FULL_ACCEPTANCE_C11C_2.19.5.ps1
```

Only after all evidence is green run the C11-C 2.19.5 freeze seal script documented in `docs/current/c11c/C11-C_2.19.5_FREEZE_COMMANDS.md`.

## Suite rule

All active Suite implementation and launchers are under `c11c-suite/`. Canonical BAT launchers are root-independent and preserve child exit codes. `c11c-studio/` is retired and must remain untouched.

## Immutable boundaries

Do not reopen C11-B simulation truth, RNG, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7/C9 contracts or logical 540×960 geometry.
