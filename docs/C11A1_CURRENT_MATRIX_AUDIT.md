# C11-A.1 — CURRENT C10 MATRIX AUDIT

Audited against `ChallengeEngineV01.2_C10_LATEST_FREEZE.zip` before implementing the QA harness.

| Challenge | Mechanic | Mechanic version | RNG | Native timeline |
|---|---|---:|---:|---:|
| CHALLENGE_001 | key | 1.0 | 1.0 | 540 frames / 9.0 s |
| CHALLENGE_002 | parking | 1.0 | 1.0 | 600 frames / 10.0 s |
| CHALLENGE_003 | pilot | 2.0 | 2.0 | 720 frames / 12.0 s |
| CHALLENGE_004 | parking_v2 | 2.0 | 2.0 | 900 frames / 15.0 s |
| CHALLENGE_005 | hit_v1 | 1.0 | 2.0 | 420 frames / 7.0 s |
| CHALLENGE_006 | catch_v1 | — | 2.0 | 540 frames / 9.0 s |
| CHALLENGE_007 | find_v1 | — | 2.0 | 600 frames / 10.0 s |
| CHALLENGE_008 | choose_v1 | — | 2.0 | 720 frames / 12.0 s |
| CHALLENGE_009 | count_v1 | — | 2.0 | 720 frames / 12.0 s |

The timing is derived from each current definition's `video.*` durations. The harness does not impose a common duration.

## Important consequence

`CHALLENGE_002` is deliberately left on legacy `parking` / RNG 1.0 while `CHALLENGE_004` is `parking_v2` / RNG 2.0. No migration is performed by C11-A.1.

`CHALLENGE_004` has a 3.0 s reveal in the current source definition; therefore its physical native output is 15.0 s / 900 frames. This must not be flattened to the old 11 s profile for QA.

## Harness architecture

The QA layer creates a disposable copy of each challenge definition, changes only `generation.seed`, and invokes the existing `build_factory.py --config ...` path. No simulation class, mechanic registry, RNG implementation, renderer, or source fixture is modified.

The finalizer operates only on already-created evidence and never re-renders.
