# AGENTS.md — ChallengeEngineV01_STATELESS

## Current authority

**C11-C 2.19.6 is the active consolidated FINAL REPAIR CANDIDATE. It is NOT FROZEN.**

The 2.19.6 runtime architecture is already proven on the workstation with genuine `Workers=7` Art Direction concurrency. The remaining repair is a false-negative assertion in the focused worker contract test: the old test compared the pool creation against the `Start-LoopReviewJob` function declaration instead of the first invocation. The production batch must remain concurrent and unchanged.

The former 2.19.2 freeze claim is historical and invalidated. The 2.19.3-v2 global mutex experiment is rejected and must never be revived.

Read first:

1. `C11C_2.19.6_CONTEXT_INDEX.md`
2. `docs/master-prompts/MASTER_HANDOVER_C11C_2.19.6_CONSOLIDATED.md`
3. `docs/master-prompts/START_PROMPT_C11C_2.19.6_CONSOLIDATED.md`
4. `docs/current/c11c/C11-C_2.19.6_CONSOLIDATED_STATE.md`
5. `docs/current/c11c/C11-C_2.19.6_ACCEPTANCE_GATE.md`
6. `docs/current/suite/C11C_SUITE_0.1.4_RULES.md`
7. `docs/current/producer/C11C_PRODUCER_0.9.7_CURRENT_STATE.md`
8. `docs/history/c11c/releases/C11-C_2.19_CONSOLIDATED_HISTORY.md`

## Frozen C boundary

Do not modify without an explicit checkpoint:

- C11-B simulation mathematics/mechanics;
- RNG algorithm, streams and ownership;
- `SimulationResult`;
- `winning_frame`;
- `close_calls`;
- `WinningFrameDetector`;
- `RenderedFrameStream`;
- C7 audio contracts/ownership;
- C9 semantics;
- logical 540×960 C11-B/C social geometry.

## C11-C manufacturing contracts

- 5 Visual Loop families / 27 grammars.
- `geometric` → Geometric Waves; `fractal` → Fractal Bloom; `kaleidoscope` → Sacred Symmetry; `particle_flow` → Living Particles; `vector_field` → Invisible Forces.
- 4 Visual Drill families.
- Tracking = 27 s / 810 frames.
- Saccade, Pursuit and Peripheral Scan = 23 s / 690 frames.
- 5 Longforms = 180 s each.
- Review capture = 720×1280 @ 30 FPS.
- Master = `MASTER_1080` / 1080×1920.
- Producer = `c11c-suite/c11c-producer/`, 0.9.7.
- Suite = `c11c-suite/`, 0.1.4.

## Parallel Art Direction invariant

`run_c11c_art_direction_batch_v4.ps1 -Workers 7` must use one private temporary Godot project per worker. Source `.godot` and source `override.cfg` are excluded. Each worker performs one headless editor class-cache bootstrap, requiring `.godot/global_script_class_cache.cfg` and `PresentationProfile`, before capture. Only initialization is sequential; captures remain concurrent.

There is no global mutex and no one-at-a-time fallback. `MAX_OBSERVED_CONCURRENCY > 1` is required runtime evidence.

## Suite ownership

`c11c-suite/` is the only active Suite implementation and launcher surface. `c11c-studio/` is retired and untouched. The misspelled `c11c-maintenace` route is compatibility-only and delegates to canonical maintenance.

All active Suite BAT/CMD/PS1 launchers must have no `c11c-studio` dependency.

## Final-repair rule

The focused worker test is static and must compare **real call sites**:

```text
$workerPool=New-C11CReviewWorkerPool
    <
Start-LoopReviewJob -FamilyId
```

It must never compare the pool call against `function Start-LoopReviewJob {`, because that is the declaration rather than a capture invocation.

## Acceptance

Run the static verifier, focused test, real 7-worker loop review and full acceptance. Do not declare a freeze until the formal freeze seal is green.
