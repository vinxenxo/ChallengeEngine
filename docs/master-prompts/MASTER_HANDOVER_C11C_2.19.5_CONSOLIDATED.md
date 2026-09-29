# MASTER HANDOVER — ChallengeEngineV01_STATELESS — C11-C 2.19.5 Consolidated

## 0. Exact authority

Continue this exact repository as:

**C11-C 2.19.5 CONSOLIDATED REPAIR CANDIDATE — NOT FROZEN.**

The 2.19.2 freeze claim is historical and invalidated for final-freeze purposes by later workstation acceptance findings.

2.19.3-v2's project-global mutex is also historical/superseded. It must not be revived because it serializes the required worker pool.

2.19.4 established the current production architecture: independent temporary Godot project roots per concurrent Art Direction worker.

2.19.5 repairs one defect in the new static contract test: `C11CParallelReviewWorkerIsolationContractTest.gd` used `_ready()` even though it is a command-line `SceneTree/MainLoop` script. The correct entrypoint is `_initialize()`. This test-harness repair does not alter production worker behavior.

## 1. Read order

1. `C11C_2.19.5_CONTEXT_INDEX.md`
2. `AGENTS.md`
3. `.continue/rules/CONTINUE.md`
4. this handover
5. `START_PROMPT_C11C_2.19.5_CONSOLIDATED.md`
6. `docs/current/c11c/C11-C_2.19.5_CONSOLIDATED_STATE.md`
7. `docs/current/c11c/C11-C_2.19.5_ACCEPTANCE_GATE.md`
8. `docs/current/c11c/C11-C_2.19.5_DOCUMENTATION_INDEX.md`
9. `docs/current/suite/C11C_SUITE_0.1.4_RULES.md`
10. `docs/current/producer/C11C_PRODUCER_0.9.7_CURRENT_STATE.md`
11. `docs/history/c11c/releases/C11-C_2.19_CONSOLIDATED_HISTORY.md`

## 2. Parallel Art Direction contract

Canonical runner:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\tools\prototypes\c11c_bulk\run_c11c_art_direction_batch_v4.ps1 `
  -Workers 7 `
  -All `
  -Reset
```

The meaning of `Workers=7` is genuine concurrency, not seven logical slots over a serialized capture.

Implementation contract:

- create a temporary worker pool outside the repository;
- copy the current source tree into one independent Godot project root per worker;
- exclude generated `artifacts/`;
- exclude source `.godot/` and `.git/`;
- exclude Python caches;
- exclude retired `c11c-studio/`;
- exclude any source `override.cfg`;
- execute the family launcher from inside each worker root;
- allow each worker to own its Movie Maker override and `.godot` state;
- record worker slot/root activity markers;
- report `MAX_OBSERVED_CONCURRENCY`;
- fail a multi-task run when observed concurrency never exceeds one worker.

No global mutex is permitted.

## 3. Why the latest test hung

The focused command:

```powershell
.\c11c-suite\c11c-test\run_suite.bat C11CParallelReviewWorkerIsolationContractTest.gd
```

started Godot successfully but did not print the PASS marker because the test body was attached to `_ready()`.

For a command-line script inheriting `SceneTree`/`MainLoop`, Godot's MainLoop lifecycle calls `_initialize()`. Therefore `_ready()` was never reached and the test never called `quit()`. The corrected 2.19.5 test uses `_initialize()`.

Do not “fix” this by adding a serialization mechanism to production.

## 4. Suite ownership

`c11c-suite/` is the only active Suite source and launcher surface.

`c11c-studio/` is retired. Do not modify it, do not import implementation from it, and do not make active `.py/.ps1/.bat/.cmd` launchers depend on it.

The Suite self-test statically audits this rule.

Canonical launcher surface includes:

```text
c11c-suite/run.bat
c11c-suite/c11c-test/run.bat
c11c-suite/c11c-test/run_all.bat
c11c-suite/c11c-test/run_suite.bat
c11c-suite/c11c-producer/run.bat
c11c-suite/c11c-producer/test_gui_contract.bat
c11c-suite/c11c-maintenance/run.bat
c11c-suite/c11c-catalog/run.bat
c11c-suite/c11c-config/run.bat
c11c-suite/test_retro_reference_contract.bat
```

`c11c-maintenace/run.bat` is retained only as the historical compatibility launcher and delegates to canonical `c11c-maintenance`; it is not a second implementation.

## 5. Manufacturing constants

- Logical social geometry: 540×960.
- Physical review: 720×1280 @ 30 FPS.
- Master delivery: `MASTER_1080` / 1080×1920.
- Visual Loop families: 5.
- Visual Loop grammars: 27.
- Visual Drill families: 4.
- Tracking: 27 s / 810 frames.
- Saccade: 23 s / 690 frames.
- Pursuit: 23 s / 690 frames.
- Peripheral Scan: 23 s / 690 frames.
- Longforms: 5 × 180 s.
- Producer: 0.9.7.
- Suite: 0.1.4.

Family mapping remains:

`geometric` → Geometric Waves → `c11c_geometric_waves_v1`

`fractal` → Fractal Bloom → `c11c_fractal_bloom_v1`

`kaleidoscope` → Sacred Symmetry → `c11c_sacred_symmetry_v1`

`particle_flow` → Living Particles → `c11c_living_particles_v1`

`vector_field` → Invisible Forces → `c11c_invisible_forces_v1`

These are historical/technical aliases for the same five current families, not duplicate families.

## 6. AVI and review production

The established single-Drill capture route remains temporary AVI Movie Maker output, followed by video-only MP4 conversion and canonical audio/delivery handling. Do not replace this with an alternative capture architecture merely to solve worker isolation.

Visual Loop review remains a 23 s review capture where the current batch contract requires it; production manifests remain governed by their existing source revision contracts.

## 7. Immutable boundaries

Do not modify without an explicit checkpoint:

- C11-B simulation mathematics/mechanics;
- RNG algorithm, ownership or stream separation;
- `SimulationResult`;
- `winning_frame`;
- `close_calls`;
- `WinningFrameDetector`;
- `RenderedFrameStream`;
- C7 audio contracts/ownership;
- C9 semantics;
- logical 540×960 social geometry.

Producer and presentation remain orchestration/presentation surfaces and must not absorb simulation truth.

## 8. Acceptance sequence

First:

```powershell
python .\c11c-suite\self_test.py
python .\c11c-suite\c11c-producer\self_test.py
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

The log must show `MAX_OBSERVED_CONCURRENCY > 1`.

Then:

```powershell
python .\tests\run_all.py
```

Then:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\FULL_ACCEPTANCE_C11C_2.19.5.ps1
```

## 9. Freeze / D boundary

Do not call this repository frozen until the workstation gate is fully green and runtime concurrency is demonstrated.

Do not begin C11-D from this candidate. D starts only after a new formal C11-C freeze receipt is produced from a fully accepted state. The first D activity remains D0 repository/challenge recovery.
