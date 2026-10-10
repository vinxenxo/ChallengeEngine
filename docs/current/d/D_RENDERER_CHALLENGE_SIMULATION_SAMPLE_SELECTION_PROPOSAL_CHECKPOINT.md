# C11-D — Challenge Simulation Sample Selection Proposal V1

**State: `PROPOSED_NOT_APPROVED`. This is a policy proposal and a deterministic mapping preview, not renderer input.**

## Problem

The existing delivery-timebase projection deliberately does not define how the 420 canonical gameplay snapshots at 60 FPS should be represented in the 210-frame GAME window at 30 FPS. The unified review therefore continues to report `CHALLENGE_SIMULATION_SAMPLE_SELECTION_AND_INTERPOLATION_UNRESOLVED` until this proposal is reviewed and explicitly approved.

## Proposed mapping for the pinned reference case

- Source timeline: 900 frames at 60 FPS; delivery timeline: 450 frames at 30 FPS.
- Source GAME window: `[180, 600)`, 420 snapshots / 7 seconds.
- Delivery GAME window: `[90, 300)`, 210 frames / 7 seconds.
- Select every second source GAME snapshot by zero-based local index: `source_game_snapshot_index = delivery_game_frame_index * 2`. The selected source local indices are `0, 2, 4, ..., 418`; absolute source frames are `180, 182, ..., 598`; delivery timeline frames are `90, 91, ..., 299`.
- Do **not** interpolate, average, synthesize, or reconstruct simulation states. Each mapped delivery GAME frame corresponds to one existing source snapshot.
- Preserve the winning event as a read-only temporal anchor. In the current reference evidence, `winning_frame=394` relative to GAME maps from source absolute frame `574` to GAME delivery frame `197`, absolute delivery frame `287`. It is already on the selected cadence, so the mapping error is zero.
- If a future source anchor falls exactly halfway between delivery ticks, the proposal uses integer-only half-up rounding toward the later tick. That rule maps the anchor time only; it does not inject an otherwise unsampled simulation snapshot into the cadence.
- `close_calls` remains a count of episodes. No timestamp, frame, duration, or visibility window may be inferred from it.

## Invariants and boundary

- The 60→30 proposal is deliberately limited to the pinned integer 2:1 case; unsupported rates fail closed and need a separate proposal.
- C11-C mechanics, RNG, `SimulationResult`, canonical snapshots, `winning_frame`, `close_calls`, and the frozen C11-C manifest remain unchanged.
- This preview returns index mappings only. It does not read or mutate `SimulationResult` objects, persist reports/payloads, invoke Godot or FFmpeg, dispatch/activate a renderer, create media, or grant release authority.
- This preview test passing establishes arithmetic/contract consistency only. It does not approve the policy.

## Acceptance command

```powershell
python -m py_compile .\tools\c11d\d9\d_renderer_challenge_simulation_sample_selection.py .\tools\c11d\d9\test_d_renderer_challenge_simulation_sample_selection.py
python .\tools\c11d\d9\test_d_renderer_challenge_simulation_sample_selection.py
```

Afterward, rerun the already-passing unified Godot review and existing regression commands. The unified review must still say `review=CONSISTENT_NOT_VIDEO_READY`, `renderer=OFF`, `media_created=false`, `D4.8=BLOCKED`, and `release_authority=NONE`; its unresolved gate count must not be reduced by this proposal alone.

## Required next decision

Operator/design approval or rejection of this sampling proposal remains explicit and external to these tests. Until approval and integration into a reviewed timebase contract, do not treat the frame selection policy as approved or video-ready.
