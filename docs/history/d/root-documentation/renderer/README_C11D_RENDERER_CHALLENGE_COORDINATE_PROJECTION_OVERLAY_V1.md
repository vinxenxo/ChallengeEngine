# C11-D Renderer Challenge Coordinate Projection Preview — Overlay V1

## Purpose

Adds a renderer-neutral, in-memory projection preview for the authentic `CHALLENGE_004` visual payload. It formalizes a two-stage spatial mapping using the existing C11-C `CoordinateMapper` and the canonical `REVIEW_720` delivery profile:

1. `CANVAS_1080X1920` → profile source canvas `540x960`, uniform scale `0.5`, zero offset.
2. `540x960` → delivery `REVIEW_720 720x1280`, uniform scale `4/3`, zero offset.
3. Combined source-to-delivery coordinate scale: `2/3` on both axes.

This is a **proposal and review-only projection**, not an approved render policy. It projects positions and asset intrinsic base dimensions in a detached in-memory representation. Simulation-local scale multipliers, rotation, opacity, texture index, and variant ID remain separate and unchanged. It does not perform frame sampling/interpolation, render, create scene nodes, write files, emit renderer input, or create media.

## Apply

Extract this ZIP into the repository root with `Expand-Archive -DestinationPath "." -Force`. Check the SHA-256 of the ZIP before extracting. The overlay contains only new/modified D-owned files and does not replace frozen C11-C files.

## Validation

```powershell
python -m py_compile `
  .\tools\c11d\d9\d_renderer_challenge_coordinate_projection.py `
  .\tools\c11d\d9\test_d_renderer_challenge_coordinate_projection.py
python .\tools\c11d\d9\test_d_renderer_challenge_coordinate_projection.py

godot --headless --path . --script res://tools/c11d/d9/review_challenge_coordinate_projection_in_memory.gd
```

Accept the Godot harness only if it prints `C11-D RENDERER CHALLENGE COORDINATE PROJECTION PREVIEW PASS` with no `ERROR:` or `SCRIPT ERROR:` lines. If that succeeds, update the documentation and rerun the regressions listed in the conversation instructions.

## Expected facts

- Source timeline remains `900@60FPS`; GAME contains 420 source snapshots.
- Delivery reference is `REVIEW_720`, `720x1280@30FPS`, `450` delivery frames / 15 seconds.
- Canonical target `[850,960]` maps to `[425,480]` on the profile source canvas and `[566.666…,640]` in delivery coordinates.
- Asset intrinsic base sizes project by `2/3`: background `720x1280`, car `106.666…x213.333…`, target `133.333…x266.666…`. Declared object/target scale values are carried separately and are not multiplied into simulation snapshots.
- `winning_frame` is not mapped to a delivery frame; `close_calls` and other telemetry are not emitted.

## Locked boundaries

`C11C_SOURCE_MUTATION=false`; `renderer=OFF`; `media_created=false`; `D4.8=BLOCKED`; `release_authority=NONE`; delivery sampling/interpolation remains unresolved; projection state remains `PROPOSED_NOT_APPROVED`.
