# C11-C 2.6.0 — TRACKING SEEDED VARIATION + SACCADE JUMP COUNTER

## Tracking

- Added deterministic seed-to-authoring motion variation before runtime.
- Different seeds now select materially different Lissajous frequency pairs, phases, amplitudes, centre offsets, travel cycles and motion speed.
- Motion speed variation widened to 0.72x–1.38x so separate seed renders are visibly distinct without changing the common 20–30s delivery envelope.
- `tracking_variant` remains cosmetic-only.
- Removed the Tron 3D background from Tracking.
- Removed the former circular/elliptical operating-boundary visual.
- Restored and strengthened the history-only snake trail with age-based fading.
- Added a richer 12-palette visual bank with matching editorial text colours.
- Header/footer editorial colours and palette labels are now driven by the active Tracking/Saccade cosmetic variant.

## Saccade

- Added a numeric jump counter inside the target.
- Counter displays `jump_index + 1` directly from mechanic output.
- Saccade content seeds now deterministically author distinct polar spatial sequences while preserving the 180..300 px jump-distance contract.
- Expanded Saccade presentation palettes to the shared 12-palette bank.
- Counter typography was tightened so the index sits fully inside the target core.
- APPEAR/IDLE/VANISH timings remain unchanged.

## Validation

- Added `C11CVisualDrillSeedVariationContractTest.gd`.
- Updated Tracking/Saccade presentation contracts.
- Registered the new suite in `tests/run_all.py`.
