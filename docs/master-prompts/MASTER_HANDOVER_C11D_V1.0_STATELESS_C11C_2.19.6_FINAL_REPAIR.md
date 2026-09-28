# MASTER HANDOVER — ChallengeEngineV01_STATELESS — C11-D V1.0

## Entry condition

C11-D MUST NOT begin until C11-C 2.19.6 has a formal **CLOSED / CERTIFIED / FROZEN** seal. The current 2.19.6 final-repair package is still NOT FROZEN.

## Starting baseline

When the C freeze seal is green, the authoritative D baseline is the exact frozen repository plus its formal freeze manifest. Do not reconstruct C from memory and do not apply historical 2.19 patches one by one.

## Read first

1. `AGENTS.md`
2. `.continue/rules/CONTINUE.md`
3. the formal C11-C frozen current-state document produced by the freeze seal
4. `docs/master-prompts/MASTER_HANDOVER_C11D_V1.0_STATELESS_C11C_2.19.6_FINAL_REPAIR.md`
5. `docs/master-prompts/START_PROMPT_C11D_V1.0_STATELESS_C11C_2.19.6_FINAL_REPAIR.md`
6. `C11-D_ROADMAP_V1.0_STATELESS.md`
7. `MASTER_HANDOVER_C11D_V1.0_STATELESS.md`

## C boundary to preserve

D is additive. Do not reopen C11-B/C simulation truth, RNG ownership, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7/C9 semantics or logical 540×960 geometry without a new explicit checkpoint.

## Suite ownership

`c11c-suite/` remains the active Suite implementation. `c11c-studio/` is retired and must remain untouched.

## Challenge recovery sequence

D must first recover and verify the original challenge/asset requirements and their provenance from the frozen baseline. Do not invent replacements merely because an old patch is convenient.

Recommended sequencing:

1. inventory and provenance recovery;
2. challenge/asset intent verification;
3. deterministic authoring integration;
4. runtime/presentation integration through existing passive contracts;
5. producer orchestration only after the underlying contract is stable;
6. focused tests, full regression and documented freeze/checkpoint.

## Documentation rule

Every D change must land in the current D documentation and continuity prompt. Historical C11-C documents remain historical and must not be rewritten to describe D.
