# C11-C Producer — Visual Drills overlay v0.1.4

Overlay for the frozen **C11-C Producer 0.4.0**.

## Scope
- Activates Visual Drills in the existing Producer form.
- Preserves the 0.4.0 layout and light theme exactly; only the existing type selector behavior is extended.
- Adds Tracking, Saccade, Pursuit and Peripheral Scan.
- Uses the authoritative C11-C 2.10.1 authoring generator and seed-variation stage.
- Adds producer-side physical capture/publish wrapper; backend files are not changed.
- Keeps Visual Loop UI and canonical launcher path unchanged.
- Adds canonical technical_id → artistic_name → production_id documentation.

## Parameter truth
- Difficulty tier 1..5 is available for all four drills.
- Speed multiplier is available where the current backend actually consumes it.
- Tracking pacing (`constant`, `accelerating`, `pulsed`) is exposed because TrackingGenerator consumes it.
- Saccade pacing is not exposed because the current runtime does not consume it.
- Pursuit and Peripheral Scan authoring paths retain their backend-owned pacing modes; the producer does not pretend those are user-overrides.
- Peripheral Scan speed is not exposed because its current runtime does not use it to alter the schedule.

## Apply
Extract this archive at the repository root, merging the contained paths. It contains only modified/new Producer files and docs.

## v0.1.4 hotfix

- Removes all `$LASTEXITCODE` reads from the Drill production wrapper.
- Uses immediate PowerShell `$?` checks and a captured `$nativeOk` flag for Godot.
- No layout, theme, backend, or Visual Loop changes.
