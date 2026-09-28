# C11-C Producer 0.9.7 — Start Prompt (2.19.5)

Continue from the active repository C11-C 2.19.5 final repair candidate.

Read `docs/current/producer/C11C_PRODUCER_0.9.7_CURRENT_STATE.md` and `docs/current/c11c/C11-C_2.19.5_CONSOLIDATED_STATE.md` first.

Keep Python/Producer orchestration-only. Do not duplicate backend mechanics, RNG, simulation or rendering truth.

The Art Direction worker architecture is per-worker temporary Godot project isolation with real `Workers=7` concurrency and no project-global mutex.

`c11c-suite/` is the canonical Suite surface. `c11c-studio/` is retired and must not be updated or used.
