# D Renderer Profile Identity Separation — Checkpoint V1

**State:** PREPARATION ONLY; Windows Godot verification pending.

## Finding

`CHALLENGE_004` contains three separate profile identities that must not be collapsed into one field:

- Legacy top-level `video_profile`: `test_master_11s`, whose named file describes 30 FPS and 11 seconds (330 frames).
- Inline `video` timeline: 60 FPS, 3+7+3+2 seconds, 15 seconds total (900 frames); this is the timing the frozen effective runtime currently executes. The matching named timeline profile is `parking_v2_social_15s`.
- Explicit nested `presentation.profile`: `social_default_v1`.
- D delivery profile: `REVIEW_720`, independently resolved at 30 FPS and 720×1280.

The current legacy migration path assigns the top-level `video_profile` ID to the canonical presentation binding. Consequently the observed runtime presentation binding is `test_master_11s`, despite the explicit source presentation field being `social_default_v1`. This checkpoint documents that collision; it does **not** label the frozen C11-C behavior as changed or mutate it.

## D-owned preview strategy

The Godot harness runs the effective frozen runtime, duplicates the canonical V2 dictionary, changes only the duplicate's `presentation.profile_id` to the explicit source presentation profile and invokes the existing `ChallengePresentationBinder` with the same timeline and same `SimulationResult`. It verifies the gameplay-frame signature, `winning_frame`, frame count and metrics before and after. The original context and C11-C files are not modified. Delivery FPS remains a separate `REVIEW_720` identity. The 60→30 cumulative boundary projection remains proposed and is not executed.

## Acceptance command

```powershell
python .\tools\c11d\d9\test_d_renderer_profile_identity_separation.py
godot --headless --path . --script res://tools/c11d/d9/rebind_challenge_presentation_profile_in_memory.gd
```

Expected harness evidence: `profile=test_master_11s->social_default_v1`, `delivery=REVIEW_720@30FPS`, `timeline=900@60FPS`, `simulation_invariance=PASS`. This is a runtime review report only; it is not renderer input and creates no artifact.

## Governance

C11-C 2.19.12 remains immutable. No renderer dispatch, production, media output or authority is granted. `D4.8=BLOCKED`, `release_authority=NONE`, D9 OPEN, D10 BLOCKED. Renderer baseline approval/freeze remain missing.
