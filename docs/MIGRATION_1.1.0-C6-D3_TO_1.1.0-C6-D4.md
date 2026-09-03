# MIGRATION_1.1.0-C6-D3_TO_1.1.0-C6-D4.md

## Purpose
Move a C6-D3 repository to the C6-D4 phase-duration contract.

## Required changes
No schema migration is required. Existing `video` duration fields remain valid.

For any challenge, set one of these fields to `0` to omit its presentation phase:

```json
"hook_duration": 0.0,
"reveal_duration": 0.0,
"cta_duration": 0.0
```

`game_duration` must remain strictly greater than zero.

## Factory impact
`build_factory.py` does not need a structural change: it already derives the expected timeline from the four duration fields and validates the physical artifact against that timeline.

## Post-migration requirement
Regenerate every affected output manifest/video. Do not reuse manifests produced from a different duration composition.

## Verification sequence
1. Run `python tests/phase_duration_contract_test.py`.
2. Run the complete test corpus in a Godot 4.7.1 environment.
3. Render the nine fixtures through `build_factory.py`.
4. Confirm FFprobe duration/frame counts match telemetry.
5. Freeze and package the repository only after the nine-challenge batch passes.
