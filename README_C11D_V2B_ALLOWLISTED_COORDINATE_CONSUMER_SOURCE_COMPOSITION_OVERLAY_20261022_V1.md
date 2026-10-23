# C11-D V2-B Allowlisted Coordinate Consumer Source Composition Overlay V1 (2026-10-22)

## Why this gate exists

The isolated runtime consumer V2 now has operator-verified PASS evidence: 115 static checks, 241 negative and 36 positive runtime cases (277 total), Godot 4.7.1 Mono exit code 0, empty stderr. The immutable acceptance record is `definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_ALLOWLISTED_COORDINATE_CONSUMER_RUNTIME_ACCEPTANCE_RECORD_V2_20261022.json` (SHA-256 `5ce4cddace9a8a04b4c1ba520cfdeeb79ee3a7e1952dc70f60baf45e02623d34`).

This ADD_ONLY overlay adds a review-only source-composition harness. Unlike the prior synthetic runtime test fixtures, it obtains each actual `SimulationResult` from the existing `ChallengeRuntimeBridge.run_effective_pipeline` for the exact four allowlisted challenge source files and passes the same object to `allowlisted_coordinate_consumer_review_only_v2.gd`.

## Expected test

- Static source-composition checks: see `runtime_static_test_expected` in the manifest.
- Godot cases: 4/4 candidates.
- Each pinned source: 60 FPS × 7 seconds = 420 game frames.
- Total input frames and output marker frames: 1,680 each.
- Challenge 005 retains an identical target marker across its run-constant target track.
- Output roots/frames/markers remain closed allowlists with zero object references.

## Boundary

This is a test harness, not production wiring. The harness itself does not read `FrameSnapshot.custom_data`; the consumer alone performs one direct allowlisted `Dictionary.get` per source frame. No dictionary enumeration, `has`-then-get, direct indexing, copying, serialization, raw value logs, asset resource loading, renderer dispatch, payload materialization or media creation.

The runtime composition test has not yet been executed on the operator's Windows checkout; do not claim PASS until its exit code is zero, its output markers are present, and stderr is empty. A PASS here does not grant production integration or rendering authorization.

## Governance

- C11-C remains immutable at manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- `renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`.
- Approved bindings remain zero; `release_authority=NONE`; baseline approval missing; freeze eligibility false.
- D4.8 blocked; D9.10 prepare-only; D9.14/D9.16 blocked; D9.17 blocked no-go; D10 blocked for promotion.
