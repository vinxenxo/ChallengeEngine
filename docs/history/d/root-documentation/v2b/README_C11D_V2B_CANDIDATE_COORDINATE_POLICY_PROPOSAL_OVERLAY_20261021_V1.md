# C11-D V2-B Candidate Coordinate Policy Proposal Overlay V1

## Purpose

An additive proposal for explicit spatial mapping of the four accepted field-region candidates. It does not approve the policy or activate rendering.

## Package integrity

ZIP SHA-256 is supplied in the assistant handoff. Internal manifest name: `C11D_V2B_CANDIDATE_COORDINATE_POLICY_PROPOSAL_OVERLAY_MANIFEST_20261021_V1.json`. The archive is ADD_ONLY with eight payload files.

## Proposed spatial stages

1. `CANVAS_1080X1920` to logical `540x960`: scale 0.5, zero offset, no intermediate rounding.
2. Logical `540x960` to reference profile `REVIEW_720` (`720x1280`): spatial scale 4/3, zero offset. This is not final delivery selection and does not resample frames.
3. Combined reference source-to-delivery spatial factor is 2/3.

`CHALLENGE_003.target_x` remains scalar-only. The proposal explicitly offers `Y=480` as a presentation-only centerline default; it is not source data and awaits a separate decision. Source scalar domain is `[0,100]` with fail-closed out-of-range handling and no clamping. The three `Vector2` targets use bounds-checked 0.5 scaling. Marker dimensions, center anchor and edge clipping are also proposals, not approved rendering parameters.

## Prior Windows evidence

Field-region decision suite: 653/653; stdout `a7e3b9dd98b317df5bb19e02c1751ae2b79ed4c297440eada8493c452bb44bba`; stderr `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; receipt `4df0b28d7d933ca2c28b34e50e126112007bc0cc6fe24322e020d9d5f222677a`. Field-region decision record `1ec59d7a9257cfc2477fc37efe8cb2f04d9807a7f9986d96afc2f2ddd9b4f7af`.

## Files added

- `definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_COORDINATE_POLICY_PROPOSAL_V1.json`
- `definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_COORDINATE_POLICY_PROPOSAL_SCHEMA_V1.json`
- `tools/c11d/d9/test_d_renderer_challenge_visual_payload_v2b_candidate_coordinate_policy_proposal_v1.py`
- `docs/current/d/C11D_V2B_CANDIDATE_COORDINATE_POLICY_PROPOSAL_CHECKPOINT_20261021_V1.md`
- `docs/current/d/C11D_FULL_CONTEXT_CONTINUITY_CHECKPOINT_20261021_V17.md`
- `prompts/C11D_D_FINAL_CLOSEOUT_START_PROMPT_20261021_V17.md`
- `prompts/C11D_D_FINAL_CLOSEOUT_OVERHAND_MASTER_PROMPT_20261021_V17.md`
- `README_C11D_V2B_CANDIDATE_COORDINATE_POLICY_PROPOSAL_OVERLAY_20261021_V1.md`

## Governance

`coordinate_policy_approval=NOT_GRANTED`; bindings and renderer projection remain unauthorized; consumer/render test/payload/media remain unauthorized; `renderer=OFF`; D4.8 is blocked; D10 remains blocked for promotion; baseline approval missing; release authority none. C11-C, all Challenge JSON, `CoordinateMapper.gd`, and the CHALLENGE_004 V1 harness remain unchanged. `winning_frame` stays the sole Challenge temporal anchor and `close_calls` stays episode-count metadata only.

Static suite expected in this overlay: `961/961`. The Python suite is read-only, uses standard-library checks plus optional jsonschema validation, and does not invoke Godot, render media, write payloads or mutate source.
