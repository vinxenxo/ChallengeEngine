# START PROMPT — ChallengeEngineV01_STATELESS — C11-D V1.0

Enter D only from the formally frozen C11-C baseline.

## Preconditions

Verify that the C11-C freeze manifest and receipt both state `CLOSED_CERTIFIED_FROZEN` before modifying anything. If they do not, stop D work and finish C acceptance first.

## Read order

1. `AGENTS.md`
2. `.continue/rules/CONTINUE.md`
3. frozen C11-C state and freeze receipt
4. `C11-D_ROADMAP_V1.0_STATELESS.md`
5. `docs/master-prompts/MASTER_HANDOVER_C11D_V1.0_STATELESS_C11C_2.19.6_FINAL_REPAIR.md`

## First D task

Recover the original challenge and asset requirements from authoritative artifacts before implementing new challenge work. Record the recovered intent, provenance and acceptance tests.

Do not reopen or refactor the frozen C engine merely to make D work easier. D must consume the existing deterministic contracts.

## Suite

Use `c11c-suite/` only. Do not update or use `c11c-studio`.

## Rule

No silent contract changes. Every boundary crossing is an explicit checkpoint with tests and documentation.
