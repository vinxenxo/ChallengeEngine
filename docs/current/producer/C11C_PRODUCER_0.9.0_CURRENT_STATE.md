# C11-C Producer 0.9.0 — Current State

## UI

- Two-column layout retained.
- Banner/header removed.
- Visible help/instruction copy removed.
- Dark cyberpunk palette with cyan/magenta accents.
- Strong selected-row styling.
- Completed products remain in the table and appear dimmed.
- Existing manual-seed products are marked `YA PRODUCIDO` and skipped unless `FORCE`.
- Variation parameters use slider + `ALEATORIO` checkbox.

## A LA CARTA routes

- Challenges → `run_c11c_challenge_production.ps1`.
- Visual Loops → `run_c11c_production.ps1`.
- Visual Drills → `c11c-producer/run_visual_drill_production.ps1`.

Every route receives the selected delivery profile from the central catalog.

## Queue state model

`EN COLA` → `GENERANDO n/m` → `COMPLETADA`

Failure leaves the recipe row visible as `ERROR` and leaves it retryable. Completion does not delete the row.

## Production boundary

The GUI remains orchestration only. It does not contain Challenge mechanics, RNG, simulation calculations or canonical renderer logic.


## Existing-product detection

For manual seeds, the GUI considers a product already produced only when its `production_manifest.json` matches the requested delivery profile and an MP4 is present. This avoids treating a 720×1280 product as satisfying a requested 1080×1920 master.
