# CONTINUE.md — ChallengeEngineV01_STATELESS / C11-C 2.19.6

## Authoritative baseline

The active repository state is **C11-C 2.19.6 consolidated final repair candidate — NOT FROZEN**.

Read in order:

1. `AGENTS.md`
2. `.continue/rules/CONTINUE.md`
3. `C11C_2.19.6_CONTEXT_INDEX.md`
4. `docs/master-prompts/MASTER_HANDOVER_C11C_2.19.6_CONSOLIDATED.md`
5. `docs/master-prompts/START_PROMPT_C11C_2.19.6_CONSOLIDATED.md`
6. `docs/current/c11c/C11-C_2.19.6_CONSOLIDATED_STATE.md`
7. `docs/current/c11c/C11-C_2.19.6_ACCEPTANCE_GATE.md`
8. `docs/current/c11c/C11-C_2.19.6_DOCUMENTATION_INDEX.md`

## Frozen C boundary

Do not alter without an explicit checkpoint:

- mechanics/simulation mathematics;
- RNG algorithm, streams and ownership;
- `SimulationResult`;
- `winning_frame`;
- `close_calls`;
- `WinningFrameDetector`;
- `RenderedFrameStream`;
- C7 audio contracts/ownership;
- C9 semantics;
- logical 540×960 social geometry.

## Live C11-C worker contract

Art Direction `Workers=7` is real concurrency. Each worker owns an independent temporary Godot project root. The source `.godot` is excluded, then the worker runs one headless editor class-cache bootstrap and verifies `global_script_class_cache.cfg` plus `PresentationProfile`. Only preparation is sequential; all Movie Maker captures remain concurrent.

Do not reintroduce a global mutex or serialize the batch. A run that only generates one video at a time is a contract failure.

## Suite ownership

`c11c-suite/` is the only active Suite surface. `c11c-studio/` is retired and must remain untouched. Operational Suite launcher sources must not depend on it.

## D status

Do not start D work until C11-C 2.19.6 (or later) is formally accepted and frozen.
