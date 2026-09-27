> SUPERSEDED: Producer 0.8.0 state. Current GUI: `docs/current/producer/C11C_PRODUCER_0.9.0_CURRENT_STATE.md`.

# C11-C Producer 0.8.0 — Current State

## Status

**FUNCTIONALLY COMPLETE / READY FOR RUNTIME GUI ACCEPTANCE.** The orchestration surface is functionally complete at the single-content level for Challenges, Visual Loops and Visual Drills, and retains selective C11-C review batches plus full logical regression.

## Authority

Backend truth remains the frozen `ChallengeEngine-C11-C2.16.9 FROZEN.zip`. C11-B, C7, C9 and certified Challenge mechanics are not implemented in Python and are not reopened by this Producer.

## UI contract

The approved two-column light interface from Producer 0.4.0 is preserved. The current form dynamically exposes:

- A LA CARTA → CHALLENGES / VISUAL LOOPS / VISUAL DRILLS.
- Current delivery profile.
- Seed mode and deterministic parameter controls where the backend exposes them.
- Optional sound/footer/GIF/AVI controls.
- Review batch operations and logical regression.

## Delivery contract

The central delivery source is `profiles/delivery/c11c_video_delivery_profiles.json`.

`MASTER_1080` is the standard default. `REVIEW_720`, `MIN_540`, `META_REELS_FINAL_V1` and `LONGFORM_1080` remain explicit profiles.

Delivery resolution is a production concern. It must never be used to alter simulation coordinates, mechanics, RNG truth, `SimulationResult`, `winning_frame` or other frozen runtime contracts.

## Challenge route

The GUI reads the nine canonical files under `challenges/` rather than trusting a duplicated challenge-duration table. The four declarative phase durations define total frames; a legacy `video.total_duration` field is ignored by the production launcher.

Each queued Challenge seed receives an isolated output root so multi-seed production cannot replace an earlier seed accidentally.

## Visual Loop route

The GUI calls `tools/prototypes/c11c_bulk/run_c11c_production.ps1`. The proven C11-C 720x1280 review render remains the source; non-review delivery profiles are post-capture FFmpeg transformations.

## Visual Drill route

The GUI calls `c11c-producer/run_visual_drill_production.ps1`. The proven C11-C 720x1280 review capture remains the source; higher/lower delivery profiles are post-capture transformations.

The canonical current presentation envelope is:

- Tracking: 3 s PRE_ROLL + 21 s GAME + 3 s END_CTA = 27 s / 810 frames.
- Saccade, Pursuit, Peripheral Scan: 3 s PRE_ROLL + 17 s GAME + 3 s END_CTA = 23 s / 690 frames.

## Safety gates

The GUI startup gate verifies the frozen backend hash, delivery profile file and all nine Challenge definitions. `self_test.py` cross-validates the project against these same contracts.

## Error handling

The GUI uses `QProcess` for launchers, keeps failed queue recipes visible as `ERROR`, clears in-memory job state after a failed process, and leaves the queue retryable. `RESUME` and `RESET` are mutually exclusive.

## Known limitation

PySide6 GUI runtime must still be exercised on the user's Windows environment because the build environment used for this overlay does not provide the PySide6 runtime package. Static compilation and Producer self-tests pass.
