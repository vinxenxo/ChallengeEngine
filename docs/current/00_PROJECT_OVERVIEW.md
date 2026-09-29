# Project Overview — C11-C 2.19.5 Consolidated Repair Candidate

`ChallengeEngineV01_STATELESS` is currently at **C11-C 2.19.5 consolidated repair candidate** status. It is not yet frozen for D.

## Manufacturing surfaces

- deterministic Challenge engine/runtime;
- 9 historical Challenges;
- 27 Visual Loop grammars across 5 families;
- 4 Visual Drill families;
- 5 family Longforms at 180 s;
- profile-driven delivery;
- C11-A.1 54-run historical QA corpus;
- C11-C Suite 0.1.4;
- Producer 0.9.7.

## Social / physical contract

- logical frame: 540×960;
- review capture: 720×1280 @ 30 FPS;
- default master: 1080×1920;
- Tracking Drill: 27 s total / 810 frames;
- Saccade/Pursuit/Peripheral Scan: 23 s total / 690 frames.

## Current 2.19.x interpretation

The branch-level history is consolidated in `docs/history/c11c/releases/C11-C_2.19_CONSOLIDATED_HISTORY.md`.

2.19.2's former freeze claim is historical/superseded for final-freeze purposes. The current repair candidate is 2.19.5 and exists to finish acceptance without reopening backend truth.

## Operational ownership

`c11c-suite/` is the only active C11-C Suite surface. `c11c-studio/` is retired and is not to be updated or depended upon.

The Art Direction batch uses worker-local temporary Godot project roots so `Workers=7` remains genuinely concurrent while each capture owns its own temporary `override.cfg` and `.godot` state.

## Next gate

Run `docs/current/c11c/C11-C_2.19.5_ACCEPTANCE_GATE.md`. D starts only after a new formal C11-C freeze is accepted and recorded.
