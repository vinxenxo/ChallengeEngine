# C11-D V2-B Allowlisted Coordinate Consumer Implementation Design — Checkpoint V1

Date: 2026-10-22
Status: `REVIEW_ONLY_DESIGN_PENDING_IMPLEMENTATION`

## Predecessor gate accepted in active Windows checkout

The operator confirmed the allowlisted consumer specification suite passed `1038/1038`, with stdout SHA-256 `c5daea5a270aec81d76aa1c5b1499f8826d1d09e9047b3ad7ae0a7941dfc3682`, empty-stderr SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`, and receipt SHA-256 `c52d3f5ca276beea0482eb1ab521d163e201023f818e9448f6f7279c306b2ef0`.

## This increment

Adds a machine-readable design contract and static design regression suite for the *next* isolated consumer implementation. It defines the entry contract, validation order, single-key extraction rule, atomic failure semantics, output allowlist, stable failure vocabulary, and a planned 261-case negative matrix. It does not add consumer runtime code and does not claim that those 261 negative runtime cases have been executed.

The exact candidate-field allowlist remains `CHALLENGE_003.target_x`, `CHALLENGE_005.target_position`, `CHALLENGE_006.target_position`, `CHALLENGE_007.target_position`. `CHALLENGE_008.active_selection` and `CHALLENGE_009.displayed_count` remain blocked.

## Important implementation rule

For each source frame, the future GDScript consumer must perform exactly one `Dictionary.get(allowlisted_key, unique_missing_sentinel)` against `FrameSnapshot.custom_data`. It must not enumerate or copy that dictionary, must not use `winning_frame` as a target-sample selector, and must not read `FrameSnapshot.position` as fallback. Validate all samples before returning a success track; any invalid frame rejects the full track.

## Gates still closed

This is design-only. No consumer module, renderer dispatch, renderer-native input, binding approval, payload materialization, media creation, or render test is included or authorized. Pixel rounding and raster crop/antialias/subpixel semantics stay blocked. `renderer=OFF`; candidate input remains inadmissible; bindings remain zero; C11-C remains immutable with manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

## Next gate

After the design suite is accepted in the active Windows checkout, implement the helper in an isolated review-only GDScript surface, then run the negative and positive runtime matrix without dispatching or invoking the renderer. Production wiring and renderer authorization remain separate formal gates.
