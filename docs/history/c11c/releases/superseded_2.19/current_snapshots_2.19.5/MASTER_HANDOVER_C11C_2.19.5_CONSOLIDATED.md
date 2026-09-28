# MASTER HANDOVER — ChallengeEngineV01_STATELESS — C11-C 2.19.5 Final Consolidation

## 0. Exact authority

Continue this exact repository as:

**C11-C 2.19.5 FINAL REPAIR CANDIDATE — NOT FROZEN.**

The former 2.19.2 freeze claim is historical and invalid. 2.19.3-v2's project-global mutex is also historical and prohibited.

The current Art Direction architecture is genuine parallel worker-local isolation: one temporary Godot project root per worker. The remaining 2.19.5 workstation defects are now consolidated into this candidate:

- no named mutex in `C11CMovieCapture.ps1`;
- no serialization fallback;
- PowerShell worker error interpolation fixed from `$i:` to `${i}:`;
- focused worker contract uses `_initialize()` and checks the no-mutex/no-invalid-interpolation rules;
- full acceptance validates the runtime concurrency manifest;
- all active Suite launchers remain under `c11c-suite`; canonical BAT launchers execute from the repository root and propagate exit codes; `c11c-studio` is retired.

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

## 2. Parallel Art Direction — non-negotiable architecture

Canonical runner:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\tools\prototypes\c11c_bulk\run_c11c_art_direction_batch_v4.ps1 `
  -Workers 7 `
  -Loops `
  -Reset
```

Required properties:

- 1..7 temporary worker roots created before jobs start;
- each worker runs a real copy of the Godot project;
- source `artifacts`, `.godot`, `.git`, Python caches, `c11c-studio` and source `override.cfg` are excluded;
- each family launcher is invoked from worker root with `--path .`;
- Movie Maker helper performs a local override transaction only; **no `System.Threading.Mutex`**;
- `MAX_OBSERVED_CONCURRENCY > 1`;
- Movie Maker logs stay at 720×1280.

A one-video-at-a-time implementation is not an acceptable fix.

## 3. PowerShell parser rule

In a double-quoted PowerShell string, a variable immediately followed by `:` must use `${variable}:` when the colon is literal text. The worker helper therefore uses `${i}:`, not `$i:`.

## 4. Suite ownership

`c11c-suite/` is the sole active Suite implementation and launcher surface.

`c11c-studio/` is retired. Do not modify it, import code from it, or depend on it. The Suite self-test audits every operational `.py/.ps1/.bat/.cmd` file.

The misspelled `c11c-maintenace` path is compatibility-only and delegates to `c11c-maintenance`; it is not a second implementation.

## 5. Manufacturing constants

- Logical social geometry: 540×960.
- Physical review: 720×1280 @ 30 FPS.
- Master delivery: `MASTER_1080` / 1080×1920.
- Visual Loop families: 5 / 27 grammars.
- Visual Drill families: 4.
- Tracking: 27 s / 810 frames.
- Saccade, Pursuit, Peripheral Scan: 23 s / 690 frames each.
- Longforms: 5 × 180 s.
- Producer: 0.9.7.
- Suite: 0.1.4.

## 6. Acceptance sequence

Focused static/operator surface:

```powershell
python .\c11c-suite\self_test.py
python .\c11c-suite\c11c-producer\self_test.py
.\c11c-suite\c11c-test\run_suite.bat C11CParallelReviewWorkerIsolationContractTest.gd
```

Runtime concurrency proof:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\tools\prototypes\c11c_bulk\run_c11c_art_direction_batch_v4.ps1 `
  -Workers 7 `
  -Loops `
  -Reset
```

Then:

```powershell
python .\tests\run_all.py
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\FULL_ACCEPTANCE_C11C_2.19.5.ps1
```

## 7. Freeze boundary

Do not call the repository frozen until the complete workstation gate is green and the C11-C-specific freeze seal reports PASS. Do not start C11-D from this candidate.

## 8. Immutable engine boundary

Do not modify without an explicit checkpoint:

- C11-B simulation mathematics/mechanics;
- RNG algorithm/ownership/stream separation;
- `SimulationResult`;
- `winning_frame`;
- `close_calls`;
- `WinningFrameDetector`;
- `RenderedFrameStream`;
- C7 audio contracts/ownership;
- C9 semantics;
- logical 540×960 geometry.
