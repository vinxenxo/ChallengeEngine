# C11-D Renderer-Neutral Frame Program Overlay V1

## Scope

This incremental package adds a D-owned, in-memory semantic declaration plan derived from `D_RENDERER_CANDIDATE_LOGICAL_COMPOSITION_V1`. It does not create or invoke a renderer, emit renderer-native input, assign pixel coordinates, define a frame schedule, or create media.

## Files

- New: `definitions/c11d/production/D_RENDERER_NEUTRAL_FRAME_PROGRAM_V1.json`
- New: `definitions/c11d/production/D_RENDERER_NEUTRAL_FRAME_PROGRAM_SCHEMA_V1.json`
- New: `tools/c11d/d9/d_renderer_frame_program.py`
- New: `tools/c11d/d9/test_d_renderer_frame_program.py`
- New: `docs/current/d/D_RENDERER_NEUTRAL_FRAME_PROGRAM_CHECKPOINT_V1.md`
- New: `docs/history/c11d/d9/D_RENDERER_NEUTRAL_FRAME_PROGRAM_V1_20261010.md`
- Modified: renderer preparation plan, logical-composition checkpoint, current handover/start prompt and D9 suite changelog.

## Preparation verification

The focused test passes in the preparation workspace: 3/3 content types, 3/3 determinism, 3/3 editorial flow, 19/19 negative cases, structural schema 3/3 and Draft 2020-12 schema validation 3/3. Python compilation passes. These are not the operator's Windows results; Windows acceptance is still required.

## Windows commands

From the repository root, verify the ZIP SHA-256 supplied with the handover, extract it, and verify the immutable C11-C manifest SHA-256 still equals `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

Then run the exact sequence in `D_RENDERER_NEUTRAL_FRAME_PROGRAM_CHECKPOINT_V1.md`. Do not register this focused test in the 22-step aggregate until Windows acceptance and review.

## Governance

All semantic regions stay `PROPOSED_NOT_APPROVED`; schedule and coordinates stay undefined. Adapter `PREPARE_ONLY`; renderer OFF; no media; D4.8 BLOCKED; release authority NONE; D9 OPEN; D10 BLOCKED. This package does not approve or freeze the D renderer baseline.
