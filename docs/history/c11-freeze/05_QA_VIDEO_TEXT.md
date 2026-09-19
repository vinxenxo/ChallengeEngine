# QA Video Text

QA exports must be self-identifying when a large matrix is reviewed manually.

Challenge QA copies can use their existing `content.hook` and `content.cta` fields:

- Header: `QA · CHALLENGE_XXX · SEED N`
- Footer: `TEST · RNG X.Y · FPS · GAME Ns`

Visual Loop/Drill envelopes remain unchanged. Their QA text is supplied by `VisualContentPlayer` through the explicit `--qa-mode` presentation-only flag, producing:

- Header: `QA · visual_loop/fractal · SEED N`
- Footer: `TEST · RNG X.Y · FPS · FRAMES N`

The source definition is never modified by the QA text system.
