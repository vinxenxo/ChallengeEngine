# CONTINUE.md — ChallengeEngineV01_STATELESS / C11-C 2.19.5

## Authoritative baseline

The active repository state is **C11-C 2.19.5 consolidated repair candidate — NOT FROZEN**.

Canonical first reads:

1. `AGENTS.md`
2. `.continue/rules/CONTINUE.md`
3. `docs/master-prompts/MASTER_HANDOVER_C11C_2.19.5_CONSOLIDATED.md`
4. `docs/master-prompts/START_PROMPT_C11C_2.19.5_CONSOLIDATED.md`
5. `docs/current/c11c/C11-C_2.19.5_CONSOLIDATED_STATE.md`
6. `docs/current/c11c/C11-C_2.19.5_ACCEPTANCE_GATE.md`
7. `docs/current/c11c/README.md`
8. `docs/current/suite/C11C_SUITE_0.1.4_RULES.md`
9. `docs/current/producer/C11C_PRODUCER_0.9.7_CURRENT_STATE.md`
10. `docs/current/c11c/C11-C_2.19.5_DOCUMENTATION_INDEX.md`

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

## Live C11-C manufacturing contract

- 27 Loop grammars / 5 families.
- 4 Drill families.
- Tracking 27 s / 810 frames; Saccade/Pursuit/Peripheral Scan 23 s / 690 frames.
- 5 Longforms / 180 s.
- Review 720×1280 @ 30 FPS; Master 1080×1920.
- Producer 0.9.7 under `c11c-suite/c11c-producer/`.
- Single Drill capture: temporary AVI Movie Maker → video-only MP4 → family music → final delivery.
- Movie Maker launch uses project-local `--path .` and no explicit `--resolution` on the proven Producer route.
- Hooks come from `profiles/presentation/c11c_visual_hooks.json`.

## Parallel review rule

Art Direction `Workers=7` is a real concurrency contract. Each worker gets an independent temporary Godot project root. `override.cfg` and `.godot` are worker-local. Do not reintroduce a global mutex or serialize the batch to “fix” resolution races.

## Suite ownership

`c11c-suite/` is the only active Suite source. `c11c-studio/` is retired and must not be modified. Do not add active launcher references to it.

## Test rule

Every new test must be registered in `tests/run_all.py` and exposed through the relevant Suite/GUI surface plus direct console execution. Run focused tests first, then the full candidate gate.

## D status

Do not start D work until C11-C 2.19.5 (or later consolidated candidate) is formally accepted and frozen.
