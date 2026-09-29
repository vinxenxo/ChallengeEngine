# MASTER HANDOVER — ChallengeEngineV01_STATELESS — C11-C 2.19.6 Final Repair

## Authority

Continue this exact repository as **C11-C 2.19.6 FINAL REPAIR CANDIDATE — NOT FROZEN**.

The runtime worker architecture is proven: 7 isolated worker roots, class-cache bootstrap and genuine concurrent capture. The remaining 2.19.6 defect was a false-negative focused test ordering assertion.

## Exact repair

The old worker contract test used:

```text
batch.find("New-C11CReviewWorkerPool") < batch.find("Start-LoopReviewJob")
```

The latter matched the function declaration. The repaired test compares the actual invocation markers:

```text
$workerPool=New-C11CReviewWorkerPool
Start-LoopReviewJob -FamilyId
```

No production Art Direction runner change is required for this final repair.

## Parallel Art Direction invariant

- Worker roots are private and temporary.
- Source `.godot` and source `override.cfg` are not copied.
- Each worker receives one `godot.exe --headless --editor --path <worker> --audio-driver Dummy --quit` bootstrap.
- `.godot/global_script_class_cache.cfg` and `PresentationProfile` are required.
- Initialization may be sequential. Capture must remain concurrent.
- No global mutex.
- No one-at-a-time fallback.
- Required evidence: `MAX_OBSERVED_CONCURRENCY > 1`; workstation already showed `7`.

## Suite ownership

`c11c-suite/` is the sole active Suite surface. `c11c-studio/` is retired and untouched. The active Suite launcher set has been audited for no `c11c-studio` dependency.

## Immutable C boundary

Do not modify C11-B simulation truth, RNG, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7/C9 contracts or logical 540×960 geometry.

## Read order

1. `C11C_2.19.6_CONTEXT_INDEX.md`
2. `AGENTS.md`
3. `.continue/rules/CONTINUE.md`
4. this handover
5. `docs/master-prompts/START_PROMPT_C11C_2.19.6_CONSOLIDATED.md`
6. current state and acceptance gate
7. Suite and Producer current rules
8. consolidated 2.19 history

## Final acceptance

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\maintenance\verify_c11c_2_19_6_final_repair.ps1
.\c11c-suite\c11c-test\run_suite.bat C11CParallelReviewWorkerIsolationContractTest.gd

powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\tools\prototypes\c11c_bulk\run_c11c_art_direction_batch_v4.ps1 `
  -Workers 7 -Loops -Reset

python .\tests\run_all.py
.\FULL_ACCEPTANCE_C11C_2.19.6.ps1
```

Only after complete PASS may `tools/c11freeze/finalize_c11c_2_19_6_freeze.ps1` close C11-C. C11-D work remains blocked until then.
