# C11-D — Challenge Coordinate + Sample Composition Proposal Checkpoint V1

**State:** `PROPOSED_NOT_APPROVED_NOT_FROZEN`  
**Scope:** deterministic in-memory contract validation for the composed spatial projection and temporal sample-selection proposal.  
**Canonical C11-C manifest:** SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` (immutable).

## Proposal

For `CHALLENGE_004 / parking_v2`, the spatial projection continues to create a detached review representation of all 420 GAME snapshots in their original order using the existing uniform scale of `2/3` and zero offset. A separate composition step selects projected GAME-local indices `0, 2, ..., 418`, yielding 210 delivery-candidate records at 30 FPS from the 60 FPS source cadence. No interpolation is performed.

The actual winning anchor (`GAME-local=394`, absolute source frame `574`) is an exact selected sample and maps to delivery GAME-local frame `197`, absolute delivery frame `287`. `winning_frame` is checked after index selection but does not control sample selection; `close_calls` remains episode count only.

Because the declared spatial transformation is affine, uniform and zero-offset, project-then-select is equivalent to select-then-project for the chosen samples. The proposal states project-all-then-select as the canonical review composition order so existing 420-record spatial projection evidence remains independently inspectable.

## Required execution

From the repository root:

```powershell
python -m py_compile .\tools\c11d\d9\d_renderer_challenge_coordinate_sample_composition.py .\tools\c11d\d9\test_d_renderer_challenge_coordinate_sample_composition.py
python .\tools\c11d\d9\test_d_renderer_challenge_coordinate_sample_composition.py
```

## Boundaries

This is not policy approval or renderer authorization. It creates no payload files, no media, no persistent run report, no renderer-native input, and no dispatch. It does not modify `SimulationResult`, simulation metrics, the frozen C11-C manifest, the coordinate projection policy, or the sample-selection policy. Both underlying policies remain `PROPOSED_NOT_APPROVED`; D4.8 remains `BLOCKED`; renderer OFF; release authority NONE. Existing eight unresolved gates are unchanged.
