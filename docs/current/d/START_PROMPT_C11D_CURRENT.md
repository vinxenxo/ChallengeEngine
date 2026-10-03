# C11-D START PROMPT

Continue ChallengeEngineV01_STATELESS from C11-D D3.0.

## Read first

docs\current\d\MASTER_HANDOVER_C11D_CURRENT.md
docs\current\d\START_PROMPT_C11D_CURRENT.md
artifacts\tests\c11d_d3\d3_0_music_source_audit.json
docs\current\d\D3.0_PROCEDURAL_MUSIC_V5_DESIGN_CONTRACT.md
artifacts\tests\c11d_d3\d3_0_validation_receipt.json

## Current state

D0 = CLOSED / PASS
D1 = functional checkpoints complete
D2 = CLOSED
D3.0 = PASS / DESIGN READY
D3 = ACTIVE

## Core objective

Normalize procedural music for Challenge video generation using shared infrastructure.
Do not duplicate a music pipeline for Challenge when existing reusable functionality can be reused or cleanly extracted without behavior change.
Visual Loop and Visual Drill behavior must remain unchanged.

## Challenge music

Challenge uses an 8-bit/chiptune style profile. The profile is separate from the shared music engine.

## Musical layers

timbre
harmony
rhythm
motif
texture
spatial treatment

## Determinism

Music seed must be independent from structural/gameplay RNG.
Music generation must not mutate gameplay/simulation RNG.
Presentation synchronization must not modify simulation truth.

## Gate

D3.0 design contract = PASS / READY.
D3.0 source/provenance audit = PASS / READY.
Deterministic render comparison = pending.
Loudness/mobile QA = pending.

## Next checkpoint

D3.1 â€” Shared Music Engine V5 / Challenge 8-bit Style Profile.

## Frozen guardrails

Do not modify renderer, simulation, mechanics, RNG, SimulationResult, winning_frame, close_calls, WinningFrameDetector or RenderedFrameStream.
Do not modify Visual Loop or Visual Drill runtime behavior.
Do not reopen frozen C11-C production.