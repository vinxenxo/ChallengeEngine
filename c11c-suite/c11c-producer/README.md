# C11-C Producer 0.9.1 — Suite Member

Compact two-column cyberpunk interface derived from the approved 0.4.0 layout; the header/banner and visible help text are intentionally removed to maximize workspace. The Producer is the single orchestration surface for single content, selective review batches and logical regression.

## Supported single production

- **Challenges:** `CHALLENGE_001` … `CHALLENGE_009`, using canonical `challenges/*.json` and `tools/prototypes/c11c_bulk/run_c11c_challenge_production.ps1`.
- **Visual Loops:** 5 families / 27 grammars, using the canonical C11-C producer launcher and seed planner.
- **Visual Drills:** Tracking, Saccade, Pursuit and Peripheral Scan, using the C11-C Producer drill wrapper.

## Delivery profiles

The GUI reads `profiles/delivery/c11c_video_delivery_profiles.json` and defaults to `MASTER_1080`. The available profiles are `MASTER_1080`, `REVIEW_720`, `MIN_540`, `META_REELS_FINAL_V1` and `LONGFORM_1080`. Delivery resolution is a production concern; it never changes frozen mechanic truth.

Challenges capture from the historical 540x960 source and scale after capture. Visual Loops and Visual Drills preserve their proven C11-C review capture and apply higher/lower delivery profiles after that capture.

## Queue behavior

A single recipe may contain multiple seeds. Challenge jobs are isolated by Challenge ID and seed output root, so a multi-seed queue never overwrites the previous seed. `RESUME` and `RESET` are mutually exclusive. Failed jobs remain visible as `ERROR` and the queue is left retryable without corrupted in-memory job state.

## Backend safety

The GUI verifies the frozen backend hash, requires all nine canonical Challenge definitions and requires the centralized delivery-profile file before enabling generation. Python does not implement mechanics, RNG, timing truth or renderers.

## Validation

Run:

```powershell
cd .\c11c-producer
python .\self_test.py
python .\preflight.py
```

Variation controls use visual sliders with an explicit ALEATORIO checkbox; fixed values are selected only when ALEATORIO is disabled. Completed queue entries remain visible and dimmed, while the active row receives a strong selection highlight. Delivery profiles are resolved centrally, including aliases.

The review runner is held to the current Visual Drill contract: Tracking 21s gameplay + 3s PRE_ROLL + 3s END_CTA = 27s / 810 frames; Saccade, Pursuit and Peripheral Scan remain 17s gameplay + 6s presentation = 23s / 690 frames.
