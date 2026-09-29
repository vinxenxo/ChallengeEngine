# START PROMPT — ChallengeEngineV01_STATELESS — C11-C 2.19.5 Consolidated

Continue the repository from:

**C11-C 2.19.5 CONSOLIDATED REPAIR CANDIDATE — NOT FROZEN.**

Read, in order:

1. `C11C_2.19.5_CONTEXT_INDEX.md`
2. `AGENTS.md`
3. `.continue/rules/CONTINUE.md`
4. `docs/master-prompts/MASTER_HANDOVER_C11C_2.19.5_CONSOLIDATED.md`
5. `docs/current/c11c/C11-C_2.19.5_CONSOLIDATED_STATE.md`
6. `docs/current/c11c/C11-C_2.19.5_ACCEPTANCE_GATE.md`
7. `docs/current/c11c/C11-C_2.19.5_DOCUMENTATION_INDEX.md`

## Immediate objective

1. Run the focused parallel worker contract and confirm it exits with:

```text
[C11C_PARALLEL_REVIEW_WORKER_ISOLATION_CONTRACT_SUITE] PASS
```

2. Run a real multi-worker loop review:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\tools\prototypes\c11c_bulk\run_c11c_art_direction_batch_v4.ps1 `
  -Workers 7 `
  -Loops `
  -Reset
```

Require `MAX_OBSERVED_CONCURRENCY > 1` and 720×1280 Movie Maker logs. Do not accept a serialized fallback.

3. Run `python .\tests\run_all.py`.

4. Run `FULL_ACCEPTANCE_C11C_2.19.5.ps1`.

## Critical interpretation

The previous hang was a test lifecycle defect: the new `extends SceneTree` contract test used `_ready()` instead of `_initialize()`. It is now repaired. This is not a reason to change the worker architecture.

## Suite ownership

All active Suite implementation and launchers belong under `c11c-suite/`.

`c11c-studio/` is retired and must remain untouched.

## Immutable boundaries

Do not reopen C11-B simulation truth, RNG ownership/algorithm, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7/C9 contracts or logical 540×960 geometry.

## Stop condition

Do not freeze or start D until the workstation acceptance gate is fully green and genuine worker concurrency is evidenced.
