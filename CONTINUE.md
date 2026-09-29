# CONTINUE.md — ChallengeEngineV01_STATELESS / C11-C 2.19.12

## Authoritative baseline

The active repository state is **C11-C 2.19.12 final closure candidate — NOT FROZEN**.

Canonical first reads:

1. `AGENTS.md`
2. `.continue/rules/CONTINUE.md`
3. `MASTER_HANDOVER_C11C_2.19_CONSOLIDATED.md`
4. `START_PROMPT_C11C_2.19_CONSOLIDATED.md`
5. `docs/current/c11c/C11-C_2.19_CONSOLIDATED_STATE.md`
6. `docs/current/c11c/C11-C_2.19_CONSOLIDATED_ACCEPTANCE_GATE.md`
7. `docs/current/c11c/C11C_2.19.12_FINAL_CLOSURE_AND_2.16_CONTINUITY.md`

## Frozen C boundary

Do not alter mechanics/simulation mathematics, RNG algorithm/streams/ownership, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7 audio contracts/ownership, C9 semantics or logical 540x960 social geometry without an explicit checkpoint.

## Logical test corpus

The current tree contains 139 registered `*Test.gd` suites. PASS markers are part of the runner contract and must match canonical emitted output.

## Logical runner

`tests/run_all.py` retries only the exact Windows process exit `0xC06D007F` up to three additional attempts. This is process/runtime recovery, not a contract waiver.

## Parallel review

Art Direction `Workers=7` is a real concurrency contract. Each worker gets an independent temporary Godot root. No global mutex and no serial fallback.

## Suite ownership

`c11c-suite/` is the only active Suite source. `c11c-studio/` is retired.

## D status

Do not start D until C11-C 2.19.12 is formally accepted and frozen.
