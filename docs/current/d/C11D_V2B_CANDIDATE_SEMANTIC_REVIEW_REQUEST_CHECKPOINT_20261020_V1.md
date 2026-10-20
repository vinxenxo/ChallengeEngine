# C11-D V2-B Candidate Semantic Review Request — V1 (2026-10-20)

## Decision

This checkpoint records a source-bound review request only. It is not a reviewer decision, not a binding approval, and not authorization to implement a payload-side visual consumer.

## Accepted evidence entering this gate

- Candidate evidence audit JSON SHA-256: `8c4503c128355fa21e670be0aaea25b093a73c325253a2afcec2a066a92e5f00`.
- Runtime report SHA-256: `f7a1522695cbd6d3f3681d3f266b625e3062d5141c32cddbb4532bcb466e0446`; result `PASS_SAFE_PROJECTION_SEED_SENSITIVITY`, 45/45 planner invocations, 45/45 independent Godot 4.7.1 Mono processes, 9/9 selectors.
- Implementation static receipt SHA-256: `e64cfd259914c471d03e8578b955140ad487b04694c5f682834517d823fcbfc4`; 198/198 tests.
- Candidate evidence audit tests passed 38/38, then governance-shape regression passed 39/39 and receipt-schema regression passed 40/40. The accepted audit JSON was subsequently reconciled without rerunning Godot.
- Source semantic review SHA-256: `374472b2d7ab0a70d94ed1f650302869b829252dcf06a7afe29c7c2e18e345dc`; prior review records nine selector proposals and six custom-data candidates, with zero bindings approved.
- V2-B design SHA `e4f02e37fd4b9b2c89cbaa7597162f87b180da43182dc576d664263c1b937cfc`; seed matrix SHA `d69c3fb2aca78a26c3afbfda0084f7f7aef458ee404b37f65261c6d22e43121a`; runtime contract SHA `f89235640f40c81be6100f01f1007ed4e787990a1bbf7927fcd8d676ef2cb9a3`; V2-C source-frame contract SHA `6d3c59214edbdd917cf63fe9ca4859edb6968d503368ec84e867bdd56a8df74c`.
- Frozen C11-C manifest SHA remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

## Candidate review scope

Six source-grounded candidates are presented for explicit semantic review: `CHALLENGE_003.target_x` (`float`, scalar X track in `PILOT_0X100`); `CHALLENGE_005.target_position` (`Vector2`, one seeded target point per run replicated in each frame); `CHALLENGE_006.target_position` (`Vector2`, per-frame target track separate from catcher); `CHALLENGE_007.target_position` (`Vector2`, per-frame target track separate from scanner); `CHALLENGE_008.active_selection` (`int`, option index); and `CHALLENGE_009.displayed_count` (`int`, displayed count with primary-position encoding).

The request binds each candidate to the accepted sanitized audit hash and the existing source-semantic review. It deliberately contains no raw candidate values and does not duplicate the per-role candidate hashes. Those hashes remain in the separately pinned audit JSON.

## What reviewers must decide

For each candidate, review its source meaning, type, coordinate space, sampling/lifecycle, missing/out-of-range behavior, proposed visible property, invariants, gameplay-seed relation and music/editorial orthogonality. Then record one semantic decision in a separate decision record:

- `ACCEPT_SEMANTIC_DEFINITION_FOR_FUTURE_BINDING_SPECIFICATION`
- `REJECT_CANDIDATE_SEMANTIC_DEFINITION`
- `BLOCKED_NEEDS_SOURCE_OR_POLICY_DECISION`

An acceptance means only that the semantic definition may proceed to a separate future binding specification. It does **not** approve the renderer binding.

## Independent blockers

- `CHALLENGE_008` and `CHALLENGE_009` remain source-frame-only because `total_duration=11s` while phase durations sum to 12s. Do not change source challenge JSON or infer precedence.
- `CHALLENGE_003.target_x` is an X scalar derived from configured start/velocity and frame index. Its field value is not itself an independent gameplay-seed sensitivity oracle.
- `CHALLENGE_005.target_position` is per-run constant, not a moving target track.
- `CHALLENGE_006.target_position` and `CHALLENGE_007.target_position` are per-frame target tracks distinct from the primary object/scanner, respectively.
- `CHALLENGE_009.displayed_count` is not `target_count`; its relationship to primary-position encoding must be considered before any future visible binding.
- Static target proposals for `CHALLENGE_001`, `CHALLENGE_002` and `CHALLENGE_004` remain outside this six-candidate runtime audit and remain unapproved.

## Governance locks

`approved_bindings=0`; `approved_custom_data_bindings=0`; `candidate_input_admissible=false`; `payload_materialized=false`; `media_created=false`; `renderer=OFF`; `release_authority=NONE`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14/D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; baseline approval missing; freeze ineligible.

## Next gate

Record explicit semantic decisions in a separate artifact validated against `D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_SEMANTIC_DECISION_RECORD_SCHEMA_V1.json`. Keep this review request immutable. Do not implement a consumer, materialize payload, render media, alter seed domains, or change release authority based on this request.
