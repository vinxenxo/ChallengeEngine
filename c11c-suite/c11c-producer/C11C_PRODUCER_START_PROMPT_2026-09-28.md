# C11-C Producer 0.9.7 — Start Prompt — 2026-09-28

Continue `ChallengeEngineV01_STATELESS` from **C11-C 2.19.6 FINAL REPAIR CANDIDATE — NOT FROZEN**.

Read first:

1. `C11C_2.19.6_CONTEXT_INDEX.md`
2. `docs/master-prompts/MASTER_HANDOVER_C11C_2.19.6_CONSOLIDATED.md`
3. `docs/master-prompts/START_PROMPT_C11C_2.19.6_CONSOLIDATED.md`
4. `docs/current/c11c/C11-C_2.19.6_CONSOLIDATED_STATE.md`
5. `docs/current/c11c/C11-C_2.19.6_ACCEPTANCE_GATE.md`

Producer version: **0.9.7**. Suite: **0.1.4**.

## Mandatory architecture

`c11c-suite/` is the only active Suite surface. Do not modify/use `c11c-studio/`. Art Direction `Workers=7` must remain genuine concurrency. Each worker gets an isolated temporary Godot project root, then one headless editor class-cache bootstrap that must create `.godot/global_script_class_cache.cfg` and register `PresentationProfile`. Only bootstrap preparation is sequential; Movie Maker capture is concurrent.

Never add a global mutex or one-at-a-time fallback.

## Required verification

```powershell
python .\c11c-suite\self_test.py
python .\c11c-suite\c11c-producer\self_test.py
.\c11c-suite\c11c-test\run_suite.bat C11CParallelReviewWorkerIsolationContractTest.gd

powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\tools\prototypes\c11c_bulk\run_c11c_art_direction_batch_v4.ps1 `
  -Workers 7 -Loops -Reset
```

Require bootstrap PASS for all workers, 720×1280 Movie Maker logs and `MAX_OBSERVED_CONCURRENCY > 1`. Then run the full 2.19.6 acceptance gate.
