# C11-D V2-B Candidate Field-Region Visibility Decision Record Overlay V2

## Intent

This ADD_ONLY overlay records the operator-confirmed decision to accept the four field-region/visibility proposals **only for a future coordinate-policy specification**. It does not approve coordinates, pixel placement, bindings, a payload consumer, renderer activation, render testing or media creation.

## Prior Windows evidence pinned

- Field-region/visibility proposal SHA-256: `f3afe4d7d08791c7634c9851500ca551438870babc195db1908440b93e740692`.
- Field-region/visibility proposal schema SHA-256: `503d0cbe4af4c5db04161d8a54e96f41b2dd8b503d5190169d5f208f8a44937a`.
- Static regression suite SHA-256: `e3c9b47e075d14145117b3c5f325681e37c01e3504a2fabc0f7e5133c13458de`.
- Test result: `551/551`, stdout SHA-256 `dc6ecb960fc59852c4b3251a1146ef6425675c44be4cf03304d3fc0026942d27`, stderr SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Prior receipt SHA-256: `87c8ab97db18a7531dc2df610b51fe819c8bf746b2b66475b544220c37c95cbb`.
- Prior semantic decision record SHA-256: `cc3550cd4d13f228ec9b3d51eeaa199505c5975b42882fb06ba3e83c4a000e90`; 146/146 receipt SHA-256 `3cf2284c454a06571ea97a2e771a259d2b73a8f4616432063a581b5c3e57ecf9`.
- Frozen C11-C manifest SHA-256: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

## Recorded decision

`CHALLENGE_003.target_x`, `CHALLENGE_005.target_position`, `CHALLENGE_006.target_position` and `CHALLENGE_007.target_position` are accepted for future coordinate-policy specification only. `CHALLENGE_008.active_selection` and `CHALLENGE_009.displayed_count` remain blocked.

## Files added (8)

- `definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_DECISION_RECORD_V1.json`
- `definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_DECISION_RECORD_SCHEMA_V1.json`
- `tools/c11d/d9/test_d_renderer_challenge_visual_payload_v2b_candidate_field_region_visibility_decision_record_v1.py`
- `docs/current/d/C11D_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_DECISION_RECORD_CHECKPOINT_20261021_V1.md`
- `docs/current/d/C11D_FULL_CONTEXT_CONTINUITY_CHECKPOINT_20261021_V15.md`
- `prompts/C11D_D_FINAL_CLOSEOUT_START_PROMPT_20261021_V15.md`
- `prompts/C11D_D_FINAL_CLOSEOUT_OVERHAND_MASTER_PROMPT_20261021_V15.md`
- `README_C11D_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_DECISION_RECORD_OVERLAY_20261021_V2.md`

## Safety boundary

This record is separate from and does not mutate the immutable proposal. `coordinate_policy_approval=NOT_GRANTED_BY_THIS_DECISION`; bindings and renderer projection remain unauthorized; consumer, render test, payload and media remain unauthorized. `renderer=OFF`, `candidate_input_admissible=false`, `D4.8=BLOCKED`, D10 remains blocked, release authority none. C11-C and CHALLENGE_004 V1 remain untouched.

The next step is an explicit, unapproved coordinate-policy proposal. Preserve the distinction between source-to-logical coordinate mapping and delivery-profile mapping. Do not infer a Y for CHALLENGE_003, do not silently infer mapping from canvas dimensions, and do not implement a consumer in the specification stage.

## Decision-record tests

The static suite is expected to report `C11D_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_DECISION_RECORD_TESTS=653/653`. It reconciles the four decisions with the immutable proposal, verifies all 81 source pins, 9 authority pins and 6 semantic-decision input pins, and asserts that no coordinate, binding, consumer or render authorization was granted. It does not invoke Godot.

## V2 correction

The unaccepted V1 overlay had an overlay-authoring typo in the empty-stderr SHA-256 constant: it omitted `bf`, yielding 62 characters. This V2 package fixes the digest consistently in the decision record, static regression test and manifest. The predecessor Windows receipt remains pinned; no runtime, rendering, binding or release authorization is added.
