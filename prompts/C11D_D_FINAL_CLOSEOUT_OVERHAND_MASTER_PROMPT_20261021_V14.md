# C11-D Final Closeout Overhand Master Prompt — V14 (2026-10-21)

## Authority and immutable baseline

The active Windows repository `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS` is authoritative. Apply only reviewed ADD_ONLY overlays from the repo root after checking ZIP SHA-256, internal manifest, exact preconditions/pins, destination absence, post-copy hashes and rollback behavior. Never bulk-extract a context package over the checkout. C11-C 2.19.12 remains frozen at manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

## Provenance state

V2-B design tests passed 90/90; runtime implementation static tests 198/198; runtime source-frame gate passed 45/45 planner calls, 45/45 independent Godot 4.7.1 Mono processes and nine selectors. Candidate audit is source-pinned, sanitized and has zero approved bindings. Semantic review request passed 75/75. Operator-confirmed semantic decision record passed 146/146 on Windows with receipt `3cf2284c454a06571ea97a2e771a259d2b73a8f4616432063a581b5c3e57ecf9`.

## Field-to-region/visibility proposal is not approval

New contract `D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_PROPOSAL_V1.json` covers only four accepted semantic definitions. It proposes a target asset/semantic region role, full source-frame visibility window, exact source frame count, finite-only values and fail-closed behavior for missing, nonfinite or mismatched tracks. The exact test denominator lives in the contract and its suite.

Candidate constraints:

- `CHALLENGE_003.target_x`: X-only scalar in `PILOT_0X100`; no Y, no invented Vector2 and no normalization or canvas transform.
- `CHALLENGE_005.target_position`: run-constant Vector2 repeated every source frame, not a trajectory.
- `CHALLENGE_006.target_position`: target Vector2 track distinct from catcher.
- `CHALLENGE_007.target_position`: target Vector2 track distinct from scanner; no distractor, scoring or close-call telemetry.

All mappings remain `PROPOSED_NOT_APPROVED`. Keep source coordinate spaces exact; do not invent destination region bounds, asset scaling, transform, pixel placement or visibility phase. `winning_frame` remains the only Challenge temporal anchor. `close_calls` remains episode-count metadata only. No interpolation, extrapolation, delivery resampling, target fallback or whole custom-data map serialization.

A test PASS validates contract/provenance and does not grant renderer authority. After the focused suite passes on the Windows checkout, obtain a separate operator decision record before any field binding or renderer projection work. Even a positive proposal decision must not by itself enable a consumer.

## Non-negotiable locks

`renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `automatic_seed_generation=false`; `master_seed=NOT_ADOPTED`; `approved_bindings=0`; `approved_custom_data_bindings=0`; `approved_renderer_projection_bindings=0`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`.

`CHALLENGE_008.active_selection` and `CHALLENGE_009.displayed_count` remain blocked by the 11s vs 12s phase conflict and further policy questions. Do not edit those challenge JSONs or infer timing precedence. Never mutate C11-C or the CHALLENGE_004 V1 harness/fixture. Do not repeat the prior 45/45 Godot matrix solely because this increment is a static proposal.
