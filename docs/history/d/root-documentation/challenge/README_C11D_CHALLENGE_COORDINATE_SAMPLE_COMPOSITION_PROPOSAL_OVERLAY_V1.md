# C11-D Coordinate + Sample Composition Proposal Overlay V1

## Contents

- Adds a JSON contract and Draft 2020-12 schema for composing the existing spatial coordinate-projection preview with the 2:1 sample-selection proposal.
- Adds a small Python validator and unit tests for source lineage, affine coordinate mapping, sample cadence and anchor mapping.
- Adds a current D checkpoint.
- No existing files are overwritten; no C11-C or renderer paths are modified.

## Purpose

Make the relation between 420 projected source-timebase GAME snapshots and 210 proposed delivery snapshots explicit and testable. The spatial preview remains a 420-record detached representation. The composed delivery candidate is a separate 210-record mapping; it is not materialized as a file and is not renderer input.

## ZIP SHA-256

Computed at packaging time; use `Get-FileHash` after downloading to verify.

## Apply

Extract from the repository root with `Expand-Archive -DestinationPath . -Force`, then run:

```powershell
python -m py_compile .\tools\c11d\d9\d_renderer_challenge_coordinate_sample_composition.py .\tools\c11d\d9\test_d_renderer_challenge_coordinate_sample_composition.py
python .\tools\c11d\d9\test_d_renderer_challenge_coordinate_sample_composition.py
```

## Governance

`PROPOSED_NOT_APPROVED_NOT_FROZEN`; no renderer activation, no renderer input, no media, D4.8 blocked, release authority NONE. This proposal does not change the unified review's unresolved gates. Full project regression and Godot unified review remain separate required checks after application.
