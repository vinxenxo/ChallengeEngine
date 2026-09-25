# C11-C Production Policy v2.13.0

## Product boundary

A product is a C11-C Visual Loop deliberately published after review. It is not staging material.

## Final-product path

```text
artifacts\production\audiovisual\<family>\<product-id>\
```

This tree is permanent and is not targeted by C11-C prototype cleanup, reset, or review generation.

## Current delivery

- 720x1280 / 9:16
- 30 FPS
- Visual Loop review baseline: 20..23 s; Visual Drill timing remains separate
- Visual Loop chapters use complete authored cycles; default cycle mapping is 20/22/23 s for 1/2/3 cycles
- Visual Drill total presentations are 27..30 s including the 3 s countdown and 3 s terminal CTA
- exactly one final `.mp4`
- sound ON by default; `-NoSound` / `-Silent` produces the silent final MP4

## Product contents

Required:

- final `.mp4` (exactly one)
- `_social.txt`
- `_manifest.json`
- `_authoring.json`
- `_ffprobe.json`
- `_godot.log`
- `production_manifest.json`
- `PRODUCT.txt`

Optional when enabled/generated:

- `.gif`
- `_music.wav`

The raw Movie Maker `.avi` and temporary `_silent.mp4` are never published to production.

## Replacement policy

Existing products are immutable by default. Use `-Force` only after an explicit decision to replace the same product ID. The production runner renders and validates the replacement candidate before deleting the existing product directory.

## 5x5 batch production

Run:

```powershell
.\tools\prototypes\c11c_bulk\run_c11c_production_25.ps1
```

This generates five stratified, widely separated seeds and publishes all 25 family/seed combinations. The same five seeds are shared across all five families. Seed spacing is enforced, not merely uniqueness. Existing products cause an upfront abort unless `-Force` is explicitly supplied. The batch manifest is written under `artifacts\production\audiovisual`.

## Reproducibility

Every product stores its seed, family, source revision and exact production reproduction command. `C11C_PRODUCTION_CATALOG.json` indexes published products.

## Weekly / monthly production

The canonical weekly schedule contains 27 grammar slots. Run:

```powershell
.\tools\prototypes\c11c_bulk\run_c11c_weekly_production_batch.ps1
```

Monthly production repeats the 27-slot pattern and enforces seed spacing across the entire month:

```powershell
.\tools\prototypes\c11c_bulk\run_c11c_monthly_production_batch.ps1
```

## Long-form Visual Loop anthologies

A three-minute anthology is composed from existing canonical production segments; it does not create a new renderer. Each segment remains 20..23 s and loop-safe.

```powershell
.\tools\prototypes\c11c_bulk\run_c11c_visual_loop_longform_production_bulk.ps1 -Seed 314159
```

The five family anthologies are exactly 180 s. The overall anthology is a chapter sequence, not a single 180 s loop contract.
