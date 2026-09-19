# C11-A.1 — CHALLENGE SEED QUALIFICATION

## Estado

OPEN — implementation package prepared. No core code is modified by this package.

## Objective

Stress the existing `CHALLENGE_001` … `CHALLENGE_009` corpus with a controlled seed matrix while preserving each challenge's authoritative route, mechanic version and native video profile.

This phase is qualification/evidence gathering. It is not a mathematical redesign, mechanic migration or visual polish phase.

## Matrix

9 challenges × 6 seed cases = 54 executions.

| Label | Seed |
|---|---:|
| 12345_A | 12345 |
| 54321 | 54321 |
| 314159 | 314159 |
| 7770001 | 7770001 |
| 998877 | 998877 |
| 12345_B | 12345 |

The duplicated `12345_A` / `12345_B` pair is the deterministic gate.

## Authoritative routing

The harness reads each challenge definition and delegates execution to the existing `build_factory.py` / `GeneradorMaestro.gd` path.

It must not replace a mechanic based on name similarity or version assumptions.

In particular:

- `CHALLENGE_002` remains `mechanic=parking`, `rng_version=1.0`.
- `CHALLENGE_004` remains `mechanic=parking_v2`, `rng_version=2.0`.
- Other challenges retain the mechanic/version declared by their own files.

The harness only overrides `generation.seed` in a QA copy of the definition. Source challenge files are never edited.

## Native timing

The harness derives expected frame counts from each definition's `video.fps` and `hook_duration`, `game_duration`, `reveal_duration`, `cta_duration` using the same seconds-to-frames rounding contract used by `build_factory.py`.

No global 540×960 / 30fps / 60-frame constraint is imposed.

## Per-run evidence

Each run records:

- original fixture seed;
- QA test seed and label;
- challenge/mechanic/version/RNG identity;
- `initial_seed`;
- `final_seed`;
- `seed_used`;
- `attempts` and derived `retries_used`;
- `winning_frame_game`;
- `winning_frame`;
- `winning_frame_in_valid_window`;
- `minimum_distance`;
- `score`;
- `close_calls`;
- physical AVI/MP4;
- decoded `framemd5`;
- review keyframes;
- contact sheet.

## Technical gate

Every one of the 54 executions must have:

- successful factory exit;
- PASS unit manifest;
- telemetry;
- physical AVI and MP4;
- frame count matching the declarative native timeline;
- native FPS preserved;
- native master resolution;
- `framemd5`;
- review keyframes/contact sheet;
- valid winning frame inside the video;
- `winning_frame_in_valid_window=true`.

## Determinism A/B gate

For each challenge, `12345_A` and `12345_B` must have:

1. identical challenge/mechanic/version/RNG identity;
2. identical simulation metadata;
3. identical `initial_seed`, `final_seed`, `seed_used`, `attempts`;
4. identical winning-frame values;
5. identical `framemd5` output.

The MP4 SHA-256 is recorded separately. Its equality is **not** the visual determinism criterion because container/encoding metadata may vary without changing decoded frames.

## Non-goals

C11-A.1 does not:

- modify mathematical formulas;
- modify RNG streams/primitives;
- migrate legacy mechanics;
- change video timelines;
- redesign renderers;
- add the Persistent Social Frame;
- add social-platform metadata/APIs.

## Acceptance

The technical phase is accepted only when the user executes the runner and independently supplies the console evidence.

Required finalizer marker:

```text
[C11A1] Manifest finalized: technical=54/54, determinism_ab_pass=True
```

That marker is necessary but does not replace the subsequent human visual review of the 54 contact sheets/keyframes.
