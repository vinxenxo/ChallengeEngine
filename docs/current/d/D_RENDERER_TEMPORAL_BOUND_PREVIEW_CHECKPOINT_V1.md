# C11-D Renderer Temporal Bound Preview — Checkpoint V1

**State:** `PREPARATION_ONLY_SOURCE_BOUND_TEMPORAL_PREVIEW_NOT_APPROVED_NOT_FROZEN`  
**Date:** 2026-10-10  
**Depends on:** accepted Windows temporal-topology test; D1.5/region-hierarchy contract; existing C11-C timing sources (read-only)  
**Purpose:** produce deterministic, numeric frame-span review data for actual, pinned source examples without producing renderer input or media.

## Why this increment exists

The topology proposal correctly left per-content timing unbound. The next engineering step is to exercise that topology against real existing timing inputs without inventing values. This checkpoint creates one in-memory review preview from each existing route:

| Content | Pinned source | Resulting timeline |
|---|---|---|
| Challenge | `challenges/CHALLENGE_004.json` | `HOOK → GAME → REVEAL → CTA`, from inline canonical phase durations |
| Visual Loop | `definitions/visual_loop_geometric_canonical.json` | One continuous span; source duration/FPS/frame_count must agree |
| Visual Drill | `definitions/visual_drill_tracking_canonical.json` | One continuous span; source duration/FPS/frame_count must agree |

These are source-grounded representative fixtures, not a claim that all variants or families have been reviewed. The output uses zero-based, half-open frame intervals `[start_frame, end_frame_exclusive)`. Frame counts use the existing Godot `TemporalCore.duration_to_frames` nonnegative rounding rule; the Python implementation explicitly avoids Python's ties-to-even `round()` behavior. Challenge phase durations are rounded independently, then summed, matching `ChallengeTimeline`'s total-frame construction.

## Expected reference outputs

- Challenge 004: 60 FPS; `HOOK [0,180)`, `GAME [180,600)`, `REVEAL [600,780)`, `CTA [780,900)`; 900 total frames.
- Geometric Visual Loop: 30 FPS, 2 seconds, 60 frames, one continuous span.
- Tracking Visual Drill: 30 FPS, 21 seconds, 630 frames, one continuous span.

The preview does not use simulation results, `winning_frame`, or `close_calls`. It reads no gameplay state and does not synthesize visual-drill subphases. It emits only an in-memory review report; it writes no JSON artifacts and is not renderer-native input.

## Files

- `definitions/c11d/production/D_RENDERER_TEMPORAL_BOUND_PREVIEW_V1.json` — source pins, sample bindings, policies and governance locks.
- `definitions/c11d/production/D_RENDERER_TEMPORAL_BOUND_PREVIEW_SCHEMA_V1.json` — strict Draft 2020-12 schema for preview reports.
- `tools/c11d/d9/d_renderer_temporal_bound_preview.py` — in-memory report builder/validator; fail-closed source, arithmetic and governance checks.
- `tools/c11d/d9/test_d_renderer_temporal_bound_preview.py` — 3 content types, determinism, lineage, frame interval continuity, schema checks and negative controls.

## Acceptance boundary

A temporal preview PASS means only that its source-bound intervals match current pinned data. It does not approve the temporal topology, region mappings, renderer baseline, production output or C11-D freeze. Do not treat the report as renderer-native input. The prior normalized-permille region proposal remains noncanonical; D1.5 and the region-hierarchy reconciliation remain spatial authority.

## Windows verification

```powershell
python -m py_compile `
  .\tools\c11d\d9\d_renderer_temporal_bound_preview.py `
  .\tools\c11d\d9\test_d_renderer_temporal_bound_preview.py

python .\tools\c11d\d9\test_d_renderer_temporal_bound_preview.py
```

Then rerun the temporal-topology, spatial-hierarchy, region, frame-program, logical-composition, candidate binding, D9.10 bridge, D9.13 lifecycle, baseline-candidate preflight and aggregate C11-C suite already prescribed in `D_RENDERER_TEMPORAL_SCHEDULE_PROPOSAL_CHECKPOINT_V1.md`.

## Governance locks

- C11-C 2.19.12 and `release/C11C_FREEZE_PACKAGE_MANIFEST.json` are immutable; required manifest SHA-256: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- D9.10 remains `PREPARE_ONLY`; no renderer-native input, dispatch, activation, production, media or output path.
- `D4.8=BLOCKED`, `release_authority=NONE`, D9 OPEN, D9.14/D9.16 full acceptance blocked, D9.17 NO-GO, D10 BLOCKED.
- Renderer baseline approval/freeze is absent. This checkpoint creates no governance approval.

## Next step

Bind the preview to a canonical D9.9/D9.10 request result and its real payload rather than just the representative source fixtures. Then build a renderer-neutral editorial review manifest that aligns exact editorial strings with timing/semantic-region metadata. Only after the isolated D renderer and its full regressions are approved may governance authorize a first real-media test.
