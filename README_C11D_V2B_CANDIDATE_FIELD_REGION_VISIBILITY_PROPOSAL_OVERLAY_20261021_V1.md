# C11-D V2-B Candidate Field-to-Region / Visibility Proposal Overlay V1

## Purpose

This add-only overlay introduces an unapproved target-region/visibility proposal for the four semantic candidates expressly accepted for future specification: CHALLENGE_003.target_x, CHALLENGE_005.target_position, CHALLENGE_006.target_position and CHALLENGE_007.target_position. It is source-frame-only and renderer-agnostic. No implementation, binding approval, coordinate transform, payload consumer, renderer dispatch, media creation or release authority is granted.

## Files added (8)

- `definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_PROPOSAL_V1.json`
- `definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_PROPOSAL_SCHEMA_V1.json`
- `tools/c11d/d9/test_d_renderer_challenge_visual_payload_v2b_candidate_field_region_visibility_proposal_v1.py`
- `docs/current/d/C11D_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_PROPOSAL_CHECKPOINT_20261021_V1.md`
- `docs/current/d/C11D_FULL_CONTEXT_CONTINUITY_CHECKPOINT_20261021_V14.md`
- `prompts/C11D_D_FINAL_CLOSEOUT_START_PROMPT_20261021_V14.md`
- `prompts/C11D_D_FINAL_CLOSEOUT_OVERHAND_MASTER_PROMPT_20261021_V14.md`
- `README_C11D_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_PROPOSAL_OVERLAY_20261021_V1.md`

## Proposed field-to-region semantics

- `CHALLENGE_003.target_x`: `assets/c6/waypoint.svg`, scalar X-only target in `PILOT_0X100`. Missing Y and unresolved coordinate mapping block actual pixel placement.
- `CHALLENGE_005.target_position`: `assets/c6/target.svg`; one per-run constant Vector2 repeated across the source frames.
- `CHALLENGE_006.target_position`: `assets/c6/target.svg`; per-source-frame Vector2 target track, separate from catcher `FrameSnapshot.position`.
- `CHALLENGE_007.target_position`: `assets/c6/target.svg`; per-source-frame Vector2 target track, separate from scanner `FrameSnapshot.position`; exclude distractors, scoring and close-call telemetry.

Full-source-span visibility and center-anchor semantics are proposals only. Exact sample cardinality must equal source-frame count; missing/non-finite/mismatched values fail closed for the whole candidate track. No interpolation, extrapolation, fallback or delivery resampling. Coordinates remain in source spaces; destination bounds, asset scale and the 540x960/720x1280 mappings are unresolved.

## Verification

Focused tests are expected at `551/551`. The script checks 81/81 source pins, 9/9 authority-input pins, six semantic-decision input pins, the exact four-candidate matrix, fail-closed/temporal rules and governance locks. Tests are static Python only; no Godot, renderer, GUI or media is invoked. Local isolated staging passed; the user's active Windows checkout must run the tests after APPLY before this gate may be claimed accepted.

## Prior operator evidence pinned

Semantic decision record regression suite: 146/146, receipt SHA `3cf2284c454a06571ea97a2e771a259d2b73a8f4616432063a581b5c3e57ecf9`, stdout SHA `e0c05466cb7d14cfb7efb049a1d9f2ac8f5fb5b73a4d81b769b073edbf4c96f7`, stderr SHA `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## Governance

`renderer=OFF`; payload/media false; candidate input inadmissible; approved bindings/projections zero; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; D9.14/D9.16 blocked; D9.17 no-go; D10 blocked for promotion; baseline approval missing; freeze ineligible; release authority none. CHALLENGE_008/009 remain blocked. C11-C manifest SHA remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

The next gate is a separate operator decision record about the proposal. Neither a static-test PASS nor a positive field/region proposal decision authorizes renderer bindings, coordinate projection or a consumer.
