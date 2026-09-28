# START PROMPT — ChallengeEngineV01_STATELESS — C11-C 2.19.4 Consolidated

Continue `ChallengeEngineV01_STATELESS` from the exact repository state:

**C11-C 2.19.4 — CONSOLIDATED REPAIR CANDIDATE — NOT FROZEN.**

Do not treat C11-C 2.19.2 as the current freeze. Its final-freeze claim was invalidated by later workstation acceptance findings.

## Read first

0. `C11C_2.19.4_CONTEXT_INDEX.md`
1. `AGENTS.md`
2. `.continue/rules/CONTINUE.md`
3. `docs/master-prompts/MASTER_HANDOVER_C11C_2.19.4_CONSOLIDATED.md`
4. `docs/current/c11c/C11-C_2.19.4_CONSOLIDATED_STATE.md`
5. `docs/current/c11c/C11-C_2.19.4_ACCEPTANCE_GATE.md`
6. `docs/current/c11c/README.md`
7. `docs/current/suite/C11C_SUITE_0.1.4_RULES.md`
8. `docs/current/producer/C11C_PRODUCER_0.9.7_CURRENT_STATE.md`
9. `docs/history/c11c/releases/C11-C_2.19_CONSOLIDATED_HISTORY.md`
10. `docs/current/c11c/C11-C_2.19.4_DOCUMENTATION_INDEX.md`

## Immediate objective

Finish the consolidated 2.19.4 acceptance. Do not add another isolated micro-patch when the problem can be corrected in the consolidated candidate.

### A. Prove the worker fix

Run:

```powershell
.\c11c-suite\c11c-test\run_suite.bat C11CParallelReviewWorkerIsolationContractTest.gd
```

Then:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\tools\prototypes\c11c_bulk\run_c11c_art_direction_batch_v4.ps1 `
  -Workers 7 `
  -Loops `
  -Reset
```

Expected:

- multiple worker-local Godot roots;
- Movie Maker logs remain 720×1280;
- no resolution fallback to 540×960;
- the run reports `MAX_OBSERVED_CONCURRENCY` > 1;
- all selected loop artifacts complete.

### B. Verify Suite ownership

`c11c-suite/` is the only active Suite source.

`c11c-studio/` is retired and must remain untouched.

No active Suite launcher may reference it.

### C. Run complete candidate acceptance

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\FULL_ACCEPTANCE_C11C_2.19.4.ps1
```

## Immutable C11-B/C boundaries

Do not modify without an explicit checkpoint:

- simulation truth;
- RNG ownership/algorithm;
- `SimulationResult`;
- `winning_frame`;
- `close_calls`;
- `WinningFrameDetector`;
- `RenderedFrameStream`;
- C7/C9 contracts;
- logical 540×960 social geometry.

## Manufacturing facts

- 27 Visual Loop grammars / 5 families.
- 4 Visual Drill families.
- Tracking 27 s / 810 frames.
- Saccade/Pursuit/Peripheral Scan 23 s / 690 frames.
- 5 Longforms / 180 s.
- Review 720×1280 @ 30 FPS.
- Master 1080×1920.
- Producer 0.9.7.
- Drill capture route remains temporary AVI → video-only MP4 → family music → delivery.

## After acceptance

Only after the workstation gate is fully green should the next formal C11-C freeze be prepared. Then D may begin at D0.
