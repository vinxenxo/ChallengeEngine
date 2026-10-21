# C11-D V2-B Candidate Field-to-Region / Visibility Proposal — Checkpoint V1 (2026-10-21)

## Gate outcome

The operator-confirmed semantic decision record was tested on Windows with **146/146** checks, stdout SHA-256 `e0c05466cb7d14cfb7efb049a1d9f2ac8f5fb5b73a4d81b769b073edbf4c96f7`, empty stderr SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`, and receipt SHA-256 `3cf2284c454a06571ea97a2e771a259d2b73a8f4616432063a581b5c3e57ecf9`.

This overlay is the next additive step: it proposes target-region ownership, source-frame cardinality and visibility semantics for exactly four accepted semantic definitions. It adds a contract and schema, a read-only Python regression suite, this checkpoint, V14 continuity/start/master prompts, and a README. It modifies no existing file.

## Candidate proposal

- **CHALLENGE_003.target_x** — scalar X-axis target track in `PILOT_0X100`; `assets/c6/waypoint.svg` is the proposed TARGET asset. Candidate window is the full source-frame span, but placement remains blocked: the field contains no Y value and no pilot-to-canvas/output transform is approved. Do not infer a 2D vector or a 0–100 normalization.
- **CHALLENGE_005.target_position** — run-constant `Vector2` target point repeated for every source frame; proposed `assets/c6/target.svg` marker. It is not a dynamic trajectory.
- **CHALLENGE_006.target_position** — one target `Vector2` per source frame; proposed `assets/c6/target.svg` marker. It remains separate from the catcher track in `FrameSnapshot.position`.
- **CHALLENGE_007.target_position** — one target `Vector2` per source frame; proposed `assets/c6/target.svg` marker. It remains separate from the scanner track; distractor topology and scoring/close-call telemetry are excluded.

Full-source-span visibility, marker-center anchoring and any destination-region mapping are **PROPOSED_NOT_APPROVED**. All candidates are source-frame only. Every candidate track requires exact source-frame cardinality and finite values; missing, non-finite or mismatched tracks fail closed as a whole. No per-frame auto-hide, fallback, interpolation, extrapolation or delivery resampling is proposed. Source coordinate spaces remain intact; destination region bounds, asset scale and the transformation to the logical `540x960` / delivery `720x1280` spaces are unresolved.

## Current static suite

The test is expected to report `C11D_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_PROPOSAL_TESTS=551/551`, with 4/4 candidates, 81/81 source pins, 9/9 authority-input pins and 6/6 semantic-decision-input pins. This overlay was assembled and tested in an isolated staging tree. The authoritative Windows checkout must run the provided tests after APPLY; no Windows result is claimed for this new test suite yet.

## Required locks

`renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; approved bindings and approved custom-data bindings stay zero; no payload consumer, renderer projection, native input or dispatch. `CHALLENGE_008.active_selection` and `CHALLENGE_009.displayed_count` remain blocked. Keep `winning_frame` as the only Challenge temporal anchor; `close_calls` remains episode-count metadata only. C11-C manifest stays `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

## Next gate

After the focused Python suite passes on Windows, review the four proposed field-to-region/visibility contracts. Record the operator decision in a separate artifact; do not edit this proposal to imply approval. A positive proposal decision would still not authorize bindings, coordinate projection or a payload consumer.
