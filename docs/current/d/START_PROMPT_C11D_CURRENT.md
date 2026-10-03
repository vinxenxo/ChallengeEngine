# C11-D START PROMPT

Continue ChallengeEngineV01_STATELESS from C11-D D3.1.

## Read first

docs\current\d\MASTER_HANDOVER_C11D_CURRENT.md
docs\current\d\START_PROMPT_C11D_CURRENT.md
artifacts\tests\c11d_d3\d3_0_validation_receipt.json
artifacts\tests\c11d_d3\d3_1_validation_receipt.json
definitions\c11d\music\C11D_MUSIC_ENGINE_V5_SPEC_V1.json
definitions\c11d\music\C11D_CHALLENGE_8BIT_STYLE_PROFILE_V1.json
docs\current\d\D3.1_SHARED_MUSIC_ENGINE_V5_CONTRACT.md

## Current state

D0 = CLOSED / PASS
D1 = functional checkpoints complete
D2 = CLOSED
D3.0 = PASS / DESIGN READY
D3.1 = PASS / SPECIFIED
D3 = ACTIVE

## D3.1 architecture

Use one shared procedural music engine.
Use declarative style profiles instead of family-specific music engines.
Challenge style profile = challenge_8bit_v1.

## Musical layers

timbre
harmony
rhythm
motif
texture
spatial treatment

## Determinism

Use a dedicated music seed.
Never consume structural RNG.
Never consume gameplay RNG.
Presentation synchronization must not modify simulation truth.

## Non-interference

Visual Loop runtime unchanged.
Visual Drill runtime unchanged.
Challenge mechanics unchanged.
Challenge simulation truth unchanged.
Frozen C11-C unchanged.

## Next

D3.2 - Deterministic Music Implementation / Render Comparison.