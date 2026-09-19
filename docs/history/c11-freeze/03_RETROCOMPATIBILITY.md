# C11 Freeze — Retrocompatibility Contract

## Scope

Retrocompatibility covers the production corpus represented by CHALLENGE_001 through CHALLENGE_009 plus the already frozen C6/C7/C10 presentation and production contracts.

## Layers

### R0 — mathematical telemetry

For each canonical seed run, compare:

- challenge id/version;
- mechanic/mechanic version;
- RNG version;
- seed used/final seed;
- attempts;
- `winning_frame_game`;
- `winning_frame`;
- valid window;
- minimum distance;
- score;
- close calls;
- challenge-specific frozen telemetry when present.

### R1 — frame-state determinism

Where a baseline frame digest exists, compare the digest. Otherwise compare a normalized frame signature derived from `position`, `rotation`, `scale`, `opacity` and relevant `custom_data`.

### R2 — presentation integrity

Verify:

- 540x960 social canvas;
- 30/60 FPS according to native challenge profile;
- expected total duration;
- Unified Social Frame geometry;
- BodyRegion visibility;
- declared framing policy;
- no simulation values changed by presentation.

### R3 — physical video

Validate with FFprobe:

- container decodes;
- dimensions correct;
- FPS correct;
- duration correct;
- frame count acceptable;
- manifest references exist.

A raw video hash is not a mathematical regression oracle because presentation text, framing and art direction may legitimately change.

## Canonical seeds

The existing C11-A.1 seed set remains the first compatibility corpus:

- `12345_A`
- `12345_B`
- `314159`
- `54321`
- `7770001`
- `998877`

New stress seeds must be generated deterministically and recorded, never chosen from an unseeded runtime RNG.
