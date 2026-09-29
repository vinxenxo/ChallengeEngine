# MASTER HANDOVER - ChallengeEngineV01_STATELESS / C11-C 2.19 CONSOLIDATED

**Current state: C11-C 2.19.12 final repair candidate - NOT FROZEN.**

This is the operational handover for the closing C11-C branch. Historical 2.19.x repair files remain evidence, not active instructions.

## Read first

1. `AGENTS.md`
2. `.continue/rules/CONTINUE.md`
3. `MASTER_HANDOVER_C11C_2.19_CONSOLIDATED.md`
4. `START_PROMPT_C11C_2.19_CONSOLIDATED.md`
5. `docs/current/c11c/C11-C_2.19.12_CLOSURE_AND_FREEZE_READINESS.md`
6. `docs/current/c11c/C11-C_2.19_CONSOLIDATION_AND_FAILURE_PREVENTION.md`
7. `docs/current/c11c/C11-C_2.19_COMPLETE_VIDEO_REVIEW_RUNBOOK.md`
8. `docs/current/c11c/C11-C_2.19_COMMAND_SHEET.md`
9. `docs/current/c11c/C11-C_2.19_DOCUMENTATION_INDEX.md`

## Current operational facts

- Suite: 0.1.4.
- Producer: 0.9.7.
- Five Visual Loop families / 27 grammars.
- Four Visual Drill families.
- Challenge family: nine canonical definitions.
- Challenge capture: definition-driven FPS; current C11-C review delivery is video-only.
- Visual review: 720x1280 @ 30 FPS.
- Complete physical review target: 52 products.
- Art Direction review must preserve genuine `Workers=7` concurrency.
- Each review worker must use an isolated temporary project root and private `.godot` state.
- `c11c-studio` is retired and must not be used.

## C11-A.1 closure architecture

The historical A1 qualification remains available for compatibility evidence, but its actual production route is now the canonical C11-C Challenge producer:

`tools/prototypes/c11c_bulk/run_c11c_challenge_production.ps1`

The legacy A1 manifest shape is preserved by an adapter. No second gameplay factory is introduced.

Under Windows PowerShell 5.1 `Set-StrictMode`, the A1 run record predeclares all properties that are assigned later, including:

- `producer_exit_code`
- `canonical_producer_manifest`

The contract test guards those declarations.

## build_factory.py

The repository may contain a temporary non-authoritative compatibility wrapper until the operator supplies the last historical copy. The supplied historical copy is to be recorded and hashed at freeze time.

Do not make `build_factory.py` the current A1 authority merely because the file exists. The canonical producer remains the accepted production backend unless final repository evidence establishes a different current contract.

## Hard boundaries

Do not modify C11-B simulation truth, RNG ownership/algorithm, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7 contracts, C9 semantics or logical 540x960 geometry during closure.

## Freeze gate

Do not declare C11-C frozen until fresh workstation evidence passes:

1. Suite self-test.
2. Producer self-test and GUI contract.
3. PowerShell 5.1 parse audit.
4. Focused contracts and one-video smoke.
5. Full logical `tests/run_all.py`.
6. C11-A.1 54/54 fresh runs.
7. Retrocompatibility checks.
8. C10 physical smoke/export.
9. Complete 52-video review with genuine concurrency > 1.
10. Producer runtime smoke.
11. Root `override.cfg` integrity.

The exact final marker is:

`C11-C 2.19.12 - FINAL CONSOLIDATED ACCEPTANCE PASS`

After that, freeze the repository and begin C11-D from the frozen tree.
