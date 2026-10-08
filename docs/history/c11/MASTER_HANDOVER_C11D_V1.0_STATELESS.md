# MASTER HANDOVER — ChallengeEngineV01_STATELESS
## C11-C 2.19.5 CONSOLIDATED REPAIR CANDIDATE → C11-D

**STATUS: C11-C 2.19.5 CONSOLIDATED REPAIR CANDIDATE — NOT FROZEN**

This is the current operational handover. It supersedes the older root-level handover for active context purposes.

## Read first in a new context

1. `AGENTS.md`
2. `docs/current/c11c/C11-C_2.19_CURRENT_STATE.md`
3. `docs/current/c11c/C11-C_2.19.5_ACCEPTANCE_GATE.md`
4. `docs/current/c11c/C11-C_2.19_DOCUMENTATION_INDEX.md`
5. this file
6. `START_PROMPT_C11D_V1.0_STATELESS.md`
7. `NEXT-PROMPT-C11C-2.19.5.txt`

## Current architecture decision

The Art Direction review remains genuinely parallel. `-Workers 7` is valid and must not be replaced by serial execution to hide a race.

The race was at the project-root Movie Maker override: multiple workers previously attempted to enter/exit the same `override.cfg`. The consolidated repair makes the parent batch the sole owner:

- parent creates one 720x1280 override;
- parent sets `C11C_SHARED_MOVIE_OVERRIDE=1`;
- every worker inherits the flag;
- worker-side `Enter-C11CMovieOverride` becomes externally managed and does not mutate the root override;
- parent restores the single override after every selected stage completes.

Worker artifact paths remain independent through family/grammar/seed naming and explicit per-worker authoring paths.

## Test architecture decision

`C11CParallelReviewWorkerIsolationContractTest.gd` and `C11CVisualDrillReviewEnvelopePathContractTest.gd` are static source-contract tests. They must never spawn PowerShell, FFmpeg or Movie Maker.

`c11c-suite/c11c-test/run_suite.bat` is bounded through `run_suite.py` with a 120-second timeout.

## Suite ownership

`c11c-suite` is the canonical operational suite. `c11c-studio` is retired legacy material. Do not update it, launch it, import from it or make it a dependency.

`c11c-maintenace` is a historical typo path retained only as a compatibility delegator to canonical `c11c-maintenance`.

## Frozen boundaries

Do not modify as part of this tooling repair:

- C11-B simulation truth or RNG ownership;
- `SimulationResult`;
- `winning_frame`, `close_calls`, `WinningFrameDetector`;
- `RenderedFrameStream`;
- C7 audio contracts;
- C9 semantics;
- logical 540x960 social geometry.

Producer remains orchestration/delivery, not simulation authority.

## Acceptance order

Run the focused contract tests and launcher verification first. Then run one representative test for each distinct game/mechanic. Then run the Art Direction parallel smoke with `-Workers 7`, followed by the full logical/physical acceptance corpus.

A final C11-C freeze receipt is allowed only after workstation acceptance is completely green.
