# C11-C Production Policy v2.1.4

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
- 18.00 s review baseline
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

## Reproducibility

Every product stores its seed, family, source revision and exact production reproduction command. `C11C_PRODUCTION_CATALOG.json` indexes published products.
