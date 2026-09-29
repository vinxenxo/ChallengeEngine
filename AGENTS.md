# AGENTS.md — ChallengeEngineV01_STATELESS

## Authority / current state

**C11-C 2.19.12 is the final closure candidate. It is NOT FROZEN until fresh final acceptance is green.**

Read first:

1. `AGENTS.md`
2. `.continue/rules/CONTINUE.md`
3. `MASTER_HANDOVER_C11C_2.19_CONSOLIDATED.md`
4. `START_PROMPT_C11C_2.19_CONSOLIDATED.md`
5. `docs/current/c11c/C11-C_2.19_CONSOLIDATED_STATE.md`
6. `docs/current/c11c/C11C_2.19.12_FINAL_CLOSURE_AND_2.16_CONTINUITY.md`

## Frozen C boundary

Do not modify simulation mathematics, mechanic semantics, RNG algorithm/streams/ownership, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7 audio ownership/contracts, C9 semantics or logical 540x960 social geometry without an explicit checkpoint.

## C11-C manufacturing contracts

- 27 Visual Loop grammars / 5 families.
- `geometric`, `fractal`, `kaleidoscope`, `particle_flow`, `vector_field` are historical technical IDs mapped to the five editorial families.
- 4 Visual Drill families.
- Tracking = 27 s / 810 frames.
- Saccade, Pursuit and Peripheral Scan = 23 s / 690 frames.
- 5 Longforms = 180 s each.
- Review capture = 720x1280 @ 30 FPS.
- Producer = 0.9.7 under `c11c-suite/c11c-producer/`.

## Test discipline

Every new `*Test.gd` must be registered in `tests/run_all.py` and exposed through the relevant Suite route. The logical runner may retry only exact process-level `0xC06D007F`; deterministic FAIL markers, stale/missing PASS markers, and other failures remain hard failures. The current corpus contains 139 registered logical suites.

## Worker isolation

Art Direction `Workers=7` is genuine concurrency with private temporary Godot roots, private `.godot`/class-cache state, canonical `WorkerRoot`, no global mutex and no serial fallback.

## Suite ownership

`c11c-suite/` is the only active Suite surface. `c11c-studio/` is retired and must not be modified or required for operation.

## D status

D is blocked until C11-C 2.19.12 is formally accepted and frozen.
