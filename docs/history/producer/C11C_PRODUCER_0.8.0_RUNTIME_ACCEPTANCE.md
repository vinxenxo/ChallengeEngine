> SUPERSEDED: Producer 0.8.0 state. Current GUI: `docs/current/producer/C11C_PRODUCER_0.9.0_CURRENT_STATE.md`.

# C11-C Producer 0.8.0 — Runtime Acceptance Contract

## Estado

Producer 0.8.0 is the current GUI/orchestration implementation. Static self-test and preflight pass. The final GUI acceptance step must be performed on the user's Windows environment because the model/container does not have PySide6 installed.

## Backend acceptance already demonstrated

The canonical Challenge production launcher has been runtime-verified by the user after 2.17.8:

- CHALLENGE_001 / seed 12345 / REVIEW_720: source 540×960, 540 frames → delivery 720×1280.
- CHALLENGE_001 / seed 12345 / MASTER_1080: source 540×960, 540 frames → delivery 1080×1920.
- CHALLENGE_004 / seed 12345 / MASTER_1080: source 540×960, 900 frames → delivery 1080×1920.

These runs prove the delivery layer does not alter Challenge runtime geometry or phase timing.

## Visual Drill timing authority

The canonical C11-C contract is:

- Tracking: 21 s gameplay + 3 s PRE_ROLL + 3 s END_CTA = 27 s / 810 frames.
- Saccade: 17 s gameplay + 3 s PRE_ROLL + 3 s END_CTA = 23 s / 690 frames.
- Pursuit: 17 s gameplay + 3 s PRE_ROLL + 3 s END_CTA = 23 s / 690 frames.
- Peripheral Scan: 17 s gameplay + 3 s PRE_ROLL + 3 s END_CTA = 23 s / 690 frames.

A previous physical smoke printed Tracking as 24 s / 720 frames. That output is treated as stale runner behavior and is not the active C11-C contract.

## GUI routes

A LA CARTA supports:

- Challenges: CHALLENGE_001…CHALLENGE_009 loaded directly from the canonical JSON corpus.
- Visual Loops: 5 families / 27 grammars.
- Visual Drills: Tracking, Saccade, Pursuit, Peripheral Scan.

All three routes expose the central delivery profiles:

- MASTER_1080 (standard)
- REVIEW_720
- MIN_540
- META_REELS_FINAL_V1
- LONGFORM_1080

Batch Review operations intentionally remain historical C11-C review orchestration and do not silently inherit the A LA CARTA delivery profile.

## Safety boundary

Python GUI and PowerShell producers orchestrate canonical launchers. They do not implement mechanics, RNG, SimulationResult, winning_frame, close_calls, or renderer mathematics.
