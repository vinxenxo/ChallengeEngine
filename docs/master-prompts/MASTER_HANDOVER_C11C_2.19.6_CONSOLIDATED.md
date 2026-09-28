# MASTER HANDOVER — ChallengeEngineV01_STATELESS — C11-C 2.19.6 Consolidated

## 0. Exact authority

Continue this exact repository as:

**C11-C 2.19.6 FINAL REPAIR CANDIDATE — NOT FROZEN.**

The former 2.19.2 freeze claim is historical and invalidated. The 2.19.3-v2 global mutex experiment is rejected.

### Latest workstation defect that this candidate repairs

2.19.5 isolated each worker into a private project root and correctly excluded source `.godot`. That exposed a second-order dependency: a fresh Godot project did not yet have `global_script_class_cache.cfg`, so `UnifiedSocialFrame.gd` could not resolve the named class `PresentationProfile`. The runtime then emitted gray/empty Movie Maker frames.

2.19.6 fixes this at worker bootstrap level only:

- copy project into private worker root;
- exclude source `.godot` and `override.cfg`;
- run one worker-local headless editor bootstrap;
- require `.godot/global_script_class_cache.cfg`;
- require `PresentationProfile` in that cache;
- after every worker is prepared, capture concurrently.

This is not a serialization workaround. Only preparation is sequential.

## 1. Read order

1. `C11C_2.19.6_CONTEXT_INDEX.md`
2. `AGENTS.md`
3. `.continue/rules/CONTINUE.md`
4. this handover
5. `START_PROMPT_C11C_2.19.6_CONSOLIDATED.md`
6. `docs/current/c11c/C11-C_2.19.6_CONSOLIDATED_STATE.md`
7. `docs/current/c11c/C11-C_2.19.6_ACCEPTANCE_GATE.md`
8. `docs/current/c11c/C11-C_2.19.6_DOCUMENTATION_INDEX.md`
9. `docs/current/suite/C11C_SUITE_0.1.4_RULES.md`
10. `docs/current/producer/C11C_PRODUCER_0.9.7_CURRENT_STATE.md`
11. `docs/history/c11c/releases/C11-C_2.19_CONSOLIDATED_HISTORY.md`

## 2. Parallel Art Direction — non-negotiable

Canonical runner:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\tools\prototypes\c11c_bulk\run_c11c_art_direction_batch_v4.ps1 `
  -Workers 7 -Loops -Reset
```

Required properties:

- one real temporary Godot project root per worker;
- source `.godot`, source `override.cfg`, artifacts and caches excluded;
- one `godot.exe --headless --editor --path <worker> --audio-driver Dummy --quit` bootstrap per worker;
- bootstrap requires `.godot/global_script_class_cache.cfg` and `PresentationProfile`;
- no global mutex;
- no one-at-a-time fallback;
- captures run concurrently after bootstrap;
- `MAX_OBSERVED_CONCURRENCY > 1`;
- every Movie Maker review capture logs 720×1280 @ 30 FPS.

## 3. Suite ownership

`c11c-suite/` is the sole active Suite implementation and launcher surface. `c11c-studio/` is retired. Do not modify it, import from it or depend on it. The misspelled `c11c-maintenace` path is compatibility-only.

## 4. Manufacturing constants

- Logical social geometry: 540×960.
- Physical review: 720×1280 @ 30 FPS.
- Master: `MASTER_1080` / 1080×1920.
- Visual Loops: 5 families / 27 grammars.
- Visual Drills: 4 families.
- Tracking: 27 s / 810 frames.
- Saccade/Pursuit/Peripheral Scan: 23 s / 690 frames.
- Longforms: 5 × 180 s.
- Producer: 0.9.7.
- Suite: 0.1.4.

## 5. Immutable engine boundary

Do not modify without explicit checkpoint:

- C11-B simulation mathematics/mechanics;
- RNG algorithm, streams and ownership;
- `SimulationResult`;
- `winning_frame`;
- `close_calls`;
- `WinningFrameDetector`;
- `RenderedFrameStream`;
- C7 audio contracts/ownership;
- C9 semantics;
- logical 540×960 geometry.

## 6. Acceptance

```powershell
python .\c11c-suite\self_test.py
python .\c11c-suite\c11c-producer\self_test.py
.\c11c-suite\c11c-test\run_suite.bat C11CParallelReviewWorkerIsolationContractTest.gd
python .\tests\run_all.py
.\FULL_ACCEPTANCE_C11C_2.19.6.ps1
```

Then run the formal 2.19.6 freeze seal only after workstation acceptance is green. Do not start C11-D before the freeze.
