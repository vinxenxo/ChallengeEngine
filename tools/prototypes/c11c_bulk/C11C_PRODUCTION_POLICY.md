# C11-C Production Policy v2.1.2

## Product boundary

A product is a C11-C Visual Loop video deliberately published after review. It is not staging material.

## Final-product path

```text
artifacts\production\audiovisual\<family>\<product-id>\
```

The directory is protected from C11-C cleanup/reset/review commands.

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

The raw Movie Maker `.avi` and `_silent.mp4` intermediate are never published to production.

## Replacement policy

Existing products are immutable by default. Use `-Force` only after an explicit decision to replace the same product ID. The production runner renders and validates the replacement candidate before deleting an existing product directory, preventing loss of a previously published product after a failed render.

## Reproducibility

Every product stores its seed, family, source revision and exact production reproduction command. `C11C_PRODUCTION_CATALOG.json` indexes all published products.
