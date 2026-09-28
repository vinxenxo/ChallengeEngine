# START PROMPT — ChallengeEngineV01_STATELESS — C11-C 2.19.6

Continue from **C11-C 2.19.6 FINAL REPAIR CANDIDATE — NOT FROZEN**.

## Read first

1. `C11C_2.19.6_CONTEXT_INDEX.md`
2. `AGENTS.md`
3. `.continue/rules/CONTINUE.md`
4. `docs/master-prompts/MASTER_HANDOVER_C11C_2.19.6_CONSOLIDATED.md`
5. `docs/current/c11c/C11-C_2.19.6_CONSOLIDATED_STATE.md`
6. `docs/current/c11c/C11-C_2.19.6_ACCEPTANCE_GATE.md`

## Immediate objective

First verify the focused worker contract. Then run the real parallel loop review.

```powershell
python .\c11c-suite\self_test.py
python .\c11c-suite\c11c-producer\self_test.py
.\c11c-suite\c11c-test\run_suite.bat C11CParallelReviewWorkerIsolationContractTest.gd

powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\tools\prototypes\c11c_bulk\run_c11c_art_direction_batch_v4.ps1 `
  -Workers 7 -Loops -Reset
```

The Art Direction log must show class-cache bootstrap PASS for each worker and then genuine capture concurrency. The required runtime proof is `MAX_OBSERVED_CONCURRENCY > 1`; every Movie Maker loop must report 720×1280 @ 30 FPS.

If a worker has a `PresentationProfile` parse error, do not accept its video. The bootstrap is specifically intended to prevent that failure.

## Do not regress concurrency

Never replace worker isolation with a global mutex. Never serialize captures one-by-one. Initialization may be sequential because it happens before any captures; the capture pool itself must remain concurrent.

## Suite ownership

`c11c-suite/` is the only active Suite surface. `c11c-studio/` is retired and must remain untouched.

## After runtime proof

Run:

```powershell
python .\tests\run_all.py
.\FULL_ACCEPTANCE_C11C_2.19.6.ps1
```

Only after a full PASS may the 2.19.6 freeze seal be considered.
