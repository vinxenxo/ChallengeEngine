# C11-D Challenge Visual Payload Capability Matrix V1 — Add-only overlay

**Purpose:** static source/capability inventory for V2-A. This is not a payload materializer and does not grant renderer authority.

## Included
- 43 pinned C11-D/C11-C source and asset references: nine Challenge definitions, the nine mechanic implementations and their canonical registry route, runtime/timeline/presentation/frame contracts, the 15 unique physical assets, and the existing Challenge_004-only V1 review harness/contract.
- Python audit and unit tests; strict contract and report schemas.
- V2-A checkpoint and start prompt.

## Boundaries
- No Godot invocation, simulation mutation, payload materialization, renderer input, media output, seed auto-generation, or release authority.
- All `FrameSnapshot.custom_data` keys are inventoried, not automatically bound. Per-mechanic visual semantic mappings remain unapproved.
- `CHALLENGE_008` and `CHALLENGE_009` each declare 11 seconds while their source phase components sum to 12 seconds. This conflict remains unresolved.
- The only pre-existing Challenge visual payload runtime preview is the scoped V1 `CHALLENGE_004` harness. Other selectors do not gain runtime support by this overlay.

## Run after applying
```powershell
python -B -m unittest tools.c11d.d9.test_d_renderer_challenge_visual_payload_capability_matrix_v1 -v
python -B tools/c11d/d9/d_renderer_challenge_visual_payload_capability_matrix_v1.py --root . --full-report
```
The executable must be run from the real Windows checkout for operator evidence.
