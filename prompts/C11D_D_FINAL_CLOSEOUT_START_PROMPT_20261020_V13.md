# C11-D Final Closeout Start Prompt — V13 (2026-10-20)

Continue from the active Windows checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. The active checkout is truth. Do not extract context ZIPs wholesale over it.

## Latest accepted V2-B evidence

- Design gate 90/90; implementation tests 198/198.
- Runtime safe-projection gate accepted: 45/45 planner calls, 45/45 independent Godot 4.7.1 Mono processes, 9/9 selectors. Report SHA `f7a1522695cbd6d3f3681d3f266b625e3062d5141c32cddbb4532bcb466e0446`.
- Candidate evidence audit reconciled PASS; audit SHA `8c4503c128355fa21e670be0aaea25b093a73c325253a2afcec2a066a92e5f00`; six typed candidates, no raw values.
- Semantic review request tests 75/75; request SHA `b576612dd0913ce8f706a5272a5b9ca5ceb6c7a1f39d832323d9db98578b5d01`; request receipt SHA `8de93859cd82e391d541d190f21d95a98a5508a7d5ee5952fe65eff256d1d53d`.
- Operator-confirmed decision matrix is recorded separately; next verify its test suite and pins before advancing.

## Current gate

Run `tools/c11d/d9/test_d_renderer_challenge_visual_payload_v2b_candidate_semantic_decision_record_v1.py` with the actual candidate audit JSON and accepted receipt paths. Expect the exact four semantic acceptances and two blocked decisions. Do not rerun the 45/45 Godot matrix.

After the decision record tests pass, prepare a **separate proposed field-to-region/visibility contract** for the four accepted definitions only. It must cover field semantics, coordinate projection, frame visibility/lifecycle, absent/nonfinite/out-of-range behavior, visual owner/asset role, temporal policy and invariants. Every policy without explicit approval must be `PROPOSED_NOT_APPROVED`. Do not implement a payload consumer as part of that proposal.

## Candidate decisions

- Accepted only for future binding-specification work: `CHALLENGE_003.target_x` scalar X track in `PILOT_0X100`; `CHALLENGE_005.target_position` per-run constant `Vector2`; `CHALLENGE_006.target_position` per-frame track distinct from catcher; `CHALLENGE_007.target_position` per-frame track distinct from scanner and excluding distractor/scoring telemetry.
- Blocked: `CHALLENGE_008.active_selection` and `CHALLENGE_009.displayed_count` until the declared 11s duration versus 12s phase sum is explicitly resolved. `displayed_count` is not `target_count`.
- No semantic decision approves renderer binding or projection.

## Hard locks

Frozen C11-C manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` is immutable. `renderer=OFF`; payload/media absent; candidate input inadmissible; approved bindings/custom-data bindings remain 0; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; baseline approval MISSING; freeze ineligible; release authority NONE. Never serialize all `FrameSnapshot.custom_data`, alter the challenge JSONs for 008/009, or mutate the CHALLENGE_004 V1 harness/fixture.
