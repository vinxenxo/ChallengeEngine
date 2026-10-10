# C11-D Challenge Coordinate Projection Preview — Checkpoint V1

**Status:** `PROPOSED_NOT_APPROVED` · review-only · not renderer input.

## Established by this contract

The current `CHALLENGE_004` source coordinate space is `CANVAS_1080X1920`. The existing `CoordinateMapper` fits it into the immutable presentation source canvas `540x960` at uniform scale `0.5` with zero offset. The `REVIEW_720` delivery profile is `720x1280`, which fits `540x960` at uniform scale `4/3`. The composed coordinate scale is therefore uniform `2/3` with no offset or aspect distortion.

For a canonical target position `[850,960]`, the projected positions are `[425,480]` in the presentation source canvas and `[566.666…,640]` at delivery. The three bound SVGs remain the canonical resources; their intrinsic base dimensions project by `2/3`, separately from declared asset-scale metadata and per-snapshot local scale multipliers.

## Runtime harness

`tools/c11d/d9/review_challenge_coordinate_projection_in_memory.gd` calls the frozen runtime twice, obtains a D `social_default_v1` presentation binding on detached canonical copies, maps all 420 GAME frame positions through `CoordinateMapper.map_position`, and creates a separate projected descriptor list in memory. It hashes the original and projected records, loads the three resources only to confirm their pinned Texture2D dimensions, and checks invariance of the source frame signature, `winning_frame`, frame count, score, minimum distance and tolerance.

The projected frame descriptors retain original ordering and copy rotation, simulation-local scale, opacity, texture index and variant ID unchanged. No sample-selection, interpolation, clipping, frame drawing, scene-node creation, file output, renderer input, or media output is performed.

## Expected review output

- `source_points=420/420`; `projected_points=420/420`.
- Projection stages `0.5 → 1.333333…`; composed scale `0.666666…`.
- `assets=3/3`; deterministic repetition `2/2`; simulation invariance `PASS`.
- `delivery_resampling=UNRESOLVED_NOT_APPLIED`.

## Explicit unresolved gates

1. Projection policy approval and visual review remain outstanding.
2. Delivery resampling/sample selection and interpolation from 60 to 30 FPS remain unresolved.
3. Per-type editorial mappings for Loops and Drills remain undeclared.
4. Challenge presentation still has no approved renderer dispatch/production path.
5. D baseline approval/freeze and D4.8 authorization remain independent external gates.

No self-approval or baseline freeze is implied by this checkpoint.
