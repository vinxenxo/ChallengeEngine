# C11-D Final Closeout Start Prompt — V14 (2026-10-21)

Continue from the active Windows checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. The live checkout is the only source of truth; never extract context packages over it. Frozen C11-C manifest SHA-256 is `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` and must remain immutable.

## Latest accepted gate

The operator-confirmed V2-B candidate semantic decision record was checked on Windows with 146/146 static tests, receipt SHA-256 `3cf2284c454a06571ea97a2e771a259d2b73a8f4616432063a581b5c3e57ecf9`; stdout SHA `e0c05466cb7d14cfb7efb049a1d9f2ac8f5fb5b73a4d81b769b073edbf4c96f7`; stderr empty. Four candidates were accepted only for future binding-specification work; `CHALLENGE_008.active_selection` and `CHALLENGE_009.displayed_count` remain blocked.

## Current gate: field-to-region/visibility proposal

Overlay: `C11D_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_PROPOSAL_OVERLAY_20261021_V1.zip`.

1. Apply the add-only overlay using the embedded ZIP, manifest, base-pin and destination-absence checks. Stop at the first mismatch.
2. Run `python -B .\tools\c11d\d9\test_d_renderer_challenge_visual_payload_v2b_candidate_field_region_visibility_proposal_v1.py` from the repository root. Claim PASS only if the exact denominator, 81/81 source pins, 9/9 authority pins, 6/6 semantic-decision pins, and lock markers all pass.
3. Review the proposed full-source-frame visibility and target region for each of the four candidates. The proposal status must stay `PROPOSED_NOT_APPROVED` until a separate operator decision record is created.

`CHALLENGE_003.target_x` is only a scalar X track in `PILOT_0X100`; do not invent Y, normalize it, or project it to a canvas. `CHALLENGE_005.target_position` is one per-run constant Vector2 repeated per frame. `CHALLENGE_006/007.target_position` are per-frame target tracks distinct from the catcher/scanner `FrameSnapshot.position`. Candidate coordinates stay in source space. Destination-region bounds, asset scaling and logical `540x960`/delivery `720x1280` transforms remain unresolved; no rendering/consumer is authorized.

## Hard locks

`renderer=OFF`; no media; no payload materialization; candidate input inadmissible; approved bindings/custom-data bindings/projection bindings stay zero; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; baseline approval MISSING; freeze ineligible; release authority NONE. Never serialize the whole `FrameSnapshot.custom_data`. Do not change C11-C, challenge JSONs, or the CHALLENGE_004 V1 fixture. `winning_frame` remains the sole Challenge temporal anchor; `close_calls` remains episode-count metadata only. Do not rerun the 45/45 Godot runtime matrix for static proposal changes.
