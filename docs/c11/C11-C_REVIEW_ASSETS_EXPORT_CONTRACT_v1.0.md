# C11-C — REVIEW ASSETS EXPORT CONTRACT v1.0

Purpose: create lightweight review copies of generated MP4s for visual inspection/upload without
altering canonical production artifacts.

## Canonical outputs are untouched

Original MP4/WAV/GIF/AVI files remain in artifacts/prototypes.
Review derivatives live under:

artifacts/prototypes/c11c_review_assets/

## Review GIF

Default:
- 360x640
- 12 FPS
- 96 colors
- palettegen/paletteuse
- no audio

The review GIF is for visual QA/upload, not production delivery.

## Keyframes

Default 8 PNGs per video:
0.0s, 1.25s, 2.50s, 3.75s, 5.00s, 6.25s, 7.50s, 8.75s

PNG resolution:
540x960

The last frame is intentionally excluded so the review set samples the loop interior
rather than duplicating the seamless boundary.

## Naming

Family:
    FractalBloom_v1_seed_271828

GIF:
    FractalBloom_v1_seed_271828_review.gif

Keyframes:
    FractalBloom_v1_seed_271828_kf_01.png
    ...
    FractalBloom_v1_seed_271828_kf_08.png

## Production rule

These derivatives never replace canonical video assets and never enter the production manifest
as media deliverables unless explicitly requested.
