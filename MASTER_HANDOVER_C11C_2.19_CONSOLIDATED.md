# MASTER HANDOVER — ChallengeEngineV01_STATELESS / C11-C 2.19 CONSOLIDATED

**Current state: C11-C 2.19.12 FULL CONSOLIDATED REPAIR CANDIDATE — NOT FROZEN.**

This is the single operational handover for the 2.19 branch. Individual 2.19.x repair packages remain historical evidence.

## Read first

1. `AGENTS.md`
2. `.continue/rules/CONTINUE.md`
3. `MASTER_HANDOVER_C11C_2.19_CONSOLIDATED.md`
4. `START_PROMPT_C11C_2.19_CONSOLIDATED.md`
5. `docs/current/c11c/C11-C_2.19_CONSOLIDATED_STATE.md`
6. `docs/current/c11c/C11-C_2.19_CONSOLIDATED_ACCEPTANCE_GATE.md`
7. `docs/current/c11c/C11-C_2.19_COMPLETE_VIDEO_REVIEW_RUNBOOK.md`
8. `docs/current/c11c/C11-C_2.19_COMMAND_SHEET.md`
9. `docs/current/c11c/C11-C_2.19_DOCUMENTATION_INDEX.md`
10. `docs/history/c11c/releases/C11-C_2.19_CONSOLIDATED_HISTORY.md`

## Authoritative current facts

- C11-C revision: 2.19.12, not frozen.
- Suite: 0.1.4.
- Producer: 0.9.7.
- Five Visual Loop families / 27 grammars.
- Four Visual Drill families.
- 5 Longforms.
- Complete review corpus: 52 videos.
- Physical review: 720x1280 @ 30 FPS.
- Tracking: 27s total / 810 frames.
- Other drills: 23s total / 690 frames.
- Art Direction `Workers=7` must be genuine concurrency.
- Each worker receives a private temporary Godot project root.
- No global mutex and no serial fallback.

## 2.19.12 exclusive bugfix repair

The 2.19.11 lifecycle fix remains in place. The 2.19.12 delta adds two tooling fixes discovered after the 2.19.11 consolidation: `test_gui_contract.bat` now launches the existing `test_producer_gui_contract.py`, and `C11CReviewWorkerIsolation.ps1` exposes canonical `WorkerRoot` values for private worker sandboxes while keeping the compatibility alias `Root`. The Art Direction scheduler consumes `WorkerRoot`.

## Focused validation launcher

```powershell
.\c11c-suite\c11c-test\run_c11c_focused_validation.bat
```

This is the preferred first runtime gate for a new context.

## Suite ownership

All Suite launcher/UI/test changes belong in `c11c-suite/` and the canonical root tools it launches. `c11c-studio/` is retired, must not be modified, and must not be a runtime/launcher dependency. `c11c-maintenace` is compatibility-only.

## Freeze boundaries

Do not reopen C11-B simulation truth, RNG ownership/algorithm, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7 audio contracts, C9 semantics or logical 540x960 social geometry without an explicit engine checkpoint.

## C11-A.1 closure hardening

The historical 54-run qualification delegates execution to `build_factory.py`. The runner resolves the factory manifest from the reported `manifest_path`, the historical canonical location, or a unique valid manifest discovered inside the current run. Missing or ambiguous manifests are hard failures. Factory artifacts are resolved relative to the resolved manifest directory.

## Freeze rule

2.19.12 cannot be frozen until fresh workstation PASS evidence exists for the focused contracts, Suite/Producer/launcher tests, one-video smoke, full `tests/run_all.py`, complete 52-video review with observed concurrency >1, producer runtime smoke, C11-A.1 54-run qualification and final acceptance.
