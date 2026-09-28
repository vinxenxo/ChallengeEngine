# MASTER HANDOVER — ChallengeEngineV01_STATELESS — C11-C 2.19.4 Consolidated Repair Candidate

## 0. Context authority

Continue this exact repository as **C11-C 2.19.4 consolidated repair candidate — NOT FROZEN**.

The previous 2.19.2 freeze claim is invalidated for final-freeze purposes by later workstation acceptance findings. The current objective is to finish one consolidated acceptance pass and then create a new freeze receipt. Do not reopen C11-B truth merely to solve tooling problems.

Read in this order:

0. `C11C_2.19.4_CONTEXT_INDEX.md`

1. `AGENTS.md`
2. `.continue/rules/CONTINUE.md`
3. this file
4. `START_PROMPT_C11C_2.19.4_CONSOLIDATED.md`
5. `docs/current/c11c/C11-C_2.19.4_CONSOLIDATED_STATE.md`
6. `docs/current/c11c/C11-C_2.19.4_ACCEPTANCE_GATE.md`
7. `docs/current/c11c/README.md`
8. `docs/current/suite/C11C_SUITE_0.1.4_RULES.md`
9. `docs/current/producer/C11C_PRODUCER_0.9.7_CURRENT_STATE.md`
10. `docs/history/c11c/releases/C11-C_2.19_CONSOLIDATED_HISTORY.md`
11. `docs/current/c11c/C11-C_2.19.4_DOCUMENTATION_INDEX.md`

## 1. What 2.19.4 is consolidating

2.19.0 restored temporary AVI Movie Maker capture for the single Drill Producer.

2.19.1 corrected the canonical social-hook source.

2.19.2 aligned the two production/capture tests with the final AVI route. A freeze was then recorded, but later acceptance disproved that freeze as the final current authority.

2.19.3 consolidated acceptance repairs: C11-A.1 factory isolation, Drill duration policy, Longform `_assert`, C10-C QA-mode duration handling, unique acceptance roots, quarantine tooling and Art Direction source restoration.

2.19.3-v2 tried a named mutex around the project-global Movie Maker override. That prevented the resolution race but made the 7-worker pool serial. It is **superseded**.

2.19.4 replaces the mutex with **one temporary Godot project root per worker** and keeps the active Suite under `c11c-suite` only.

## 2. Parallel review contract

The canonical Art Direction command remains:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\tools\prototypes\c11c_bulk\run_c11c_art_direction_batch_v4.ps1 `
  -Workers 7 `
  -All `
  -Reset
```

This must mean real concurrency. The implementation:

- creates a temporary worker pool;
- copies the current source tree into independent worker project roots;
- excludes `artifacts/`, `.godot/`, `.git/`, caches and retired `c11c-studio/`;
- excludes any source `override.cfg`;
- runs the family prototype directly inside each worker root;
- lets each worker create/restore its own `override.cfg`;
- records `.c11c_worker_active` markers;
- records `MAX_OBSERVED_CONCURRENCY` in the batch output and final corpus manifest.

Do **not** reintroduce a project-global mutex, do not point all workers at the real project root, and do not serialize captures to avoid the resolution race.

## 3. `c11c-studio` status

`c11c-studio/` is retired. It is not an active implementation, Suite surface or dependency.

Do not modify it.

All active Suite changes belong under `c11c-suite/`.

Operational `.py/.ps1/.bat/.cmd` files under `c11c-suite/` must not reference `c11c-studio`. The Suite static self-test checks this.

## 4. Manufacturing contracts

- Logical social geometry: 540×960.
- Physical review: 720×1280 @ 30 FPS.
- Master: `MASTER_1080` / 1080×1920.
- Visual Loops: 27 grammars / 5 families.
- Visual Drills: Tracking 27 s; Saccade/Pursuit/Peripheral Scan 23 s.
- Longforms: 5 × 180 s.
- Producer: 0.9.7.
- Canonical hook bank: `profiles/presentation/c11c_visual_hooks.json`.
- Single Drill capture: temporary AVI → video-only MP4 → family music → final delivery.

Family mapping is one-to-one, not duplicate families:

`geometric`/Geometric Waves, `fractal`/Fractal Bloom, `kaleidoscope`/Sacred Symmetry, `particle_flow`/Living Particles, `vector_field`/Invisible Forces.

## 5. Frozen C boundary

Unless a formal checkpoint explicitly says otherwise, do not modify:

- C11-B simulation mathematics or mechanics;
- RNG algorithm/ownership/stream separation;
- `SimulationResult`;
- `winning_frame`;
- `close_calls`;
- `WinningFrameDetector`;
- `RenderedFrameStream`;
- C7 audio contracts/ownership;
- C9 semantics;
- logical 540×960 social geometry.

Producer and presentation remain orchestration/passive presentation surfaces.

## 6. Current acceptance sequence

First:

```powershell
python .\c11c-suite\self_test.py
python .\c11c-suite\c11c-producer\self_test.py
.\c11c-suite\c11c-test\run_suite.bat C11CParallelReviewWorkerIsolationContractTest.gd
```

Then:

```powershell
python .\tests\run_all.py
```

Then the workstation gate:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\FULL_ACCEPTANCE_C11C_2.19.4.ps1
```

The Art Direction stage must show `MAX_OBSERVED_CONCURRENCY` greater than 1. Any fallback to one-at-a-time execution is a regression and must be repaired before freeze.

## 7. New-context stopping rule

Do not begin D work from this candidate. D is activated only after a new C11-C freeze is created and its acceptance evidence is recorded.

The first D task remains D0 repository/Challenge recovery, not new mechanics.
