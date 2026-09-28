> **Historical cross-context prompt.** Current repository authority is C11-C 2.19.2 under `docs/current/c11c/`.
>
# MASTER HANDOVER — ChallengeEngineV01_STATELESS — 2.17.9 Producer

## Authority

The frozen backend authority remains `ChallengeEngine-C11-C2.16.9 FROZEN.zip`. This handover is operational guidance for the additive post-freeze Producer/delivery layer.

## Current verified production

Challenge delivery has been runtime-verified by the user for:

- CHALLENGE_001 / seed 12345 / REVIEW_720.
- CHALLENGE_001 / seed 12345 / MASTER_1080.
- CHALLENGE_004 / seed 12345 / MASTER_1080.

All use native 540×960 source capture and post-capture delivery scaling.

## Producer GUI

Current target: `c11c-producer` 0.8.0.

It is an orchestration/UI surface for:

- single Challenges;
- single Visual Loops;
- single Visual Drills;
- historical batch review operations;
- full regression.

The GUI reads the canonical Challenge JSON corpus and the central delivery profile catalogue.

## Drill timing authority

- Tracking: 21 s gameplay + 3 s PRE_ROLL + 3 s END_CTA = 27 s / 810 frames.
- Saccade/Pursuit/Peripheral Scan: 17 s gameplay + 3 s PRE_ROLL + 3 s END_CTA = 23 s / 690 frames.

## Frozen boundaries

No Producer feature may reimplement or mutate mechanics, RNG ownership, SimulationResult, winning_frame, close_calls, WinningFrameDetector, RenderedFrameStream, C7 contracts or C9 authoring semantics.

## Final acceptance gate

Run the GUI under the user's normal Windows/PySide6 environment and execute one A LA CARTA Challenge and one A LA CARTA Visual Drill. Then return to the Video Challenger + Asset Recovery phase.
