# C11-D V2-B Candidate Semantic Decision Record — V1 (2026-10-20)

## Operator-confirmed decision

The operator explicitly confirmed this decision matrix in the project conversation. The separate decision record is `definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_CANDIDATE_SEMANTIC_DECISION_RECORD_V1.json`.

- `CHALLENGE_003.target_x` — `ACCEPT_SEMANTIC_DEFINITION_FOR_FUTURE_BINDING_SPECIFICATION`: scalar X per frame in `PILOT_0X100`; this field is not an independent gameplay-seed sensitivity oracle. No Y coordinate or canvas transform is implied.
- `CHALLENGE_005.target_position` — same accept status: a single seeded `Vector2` target per attempt, replicated across frame receipts; not a trajectory.
- `CHALLENGE_006.target_position` — same accept status: per-frame target `Vector2` track, distinct from catcher `snapshot.position`.
- `CHALLENGE_007.target_position` — same accept status: per-frame target `Vector2` track, distinct from scanner; exclude distractor topology and scoring/close-call telemetry.
- `CHALLENGE_008.active_selection` — `BLOCKED_NEEDS_SOURCE_OR_POLICY_DECISION`: `total_duration=11s` conflicts with phase durations totalling 12s.
- `CHALLENGE_009.displayed_count` — same blocked status: same 11s/12s timebase conflict, plus unresolved visible presentation/primary-position encoding policy; `displayed_count` is not `target_count`.

## Meaning of accepted decisions

The four accepted definitions may proceed only to a **separate future binding specification**. They are not renderer approvals. The two blocked candidates remain unresolved. The request and source semantic review remain immutable.

## Evidence pins

- Decision record schema SHA-256: `ab09a617e9efc0aacb2111d9f6b02fc5764850f667cfdb33005451c5d4b073b9`.
- Review request SHA-256: `b576612dd0913ce8f706a5272a5b9ca5ceb6c7a1f39d832323d9db98578b5d01`.
- Sanitized candidate audit JSON SHA-256: `8c4503c128355fa21e670be0aaea25b093a73c325253a2afcec2a066a92e5f00`.
- Runtime report SHA-256: `f7a1522695cbd6d3f3681d3f266b625e3062d5141c32cddbb4532bcb466e0446`.
- Frozen C11-C manifest SHA-256: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

## Governance locks retained

`approved_bindings=0`; `approved_custom_data_bindings=0`; `binding_authorization=NOT_GRANTED_BY_SEMANTIC_REVIEW`; `renderer_projection_authorization=NOT_GRANTED_BY_SEMANTIC_REVIEW`; `candidate_input_admissible=false`; `payload_materialized=false`; `media_created=false`; `renderer=OFF`; `release_authority=NONE`. `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14/D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; baseline approval missing; freeze ineligible.

No payload consumer, coordinate projection, region/visibility/timebase policy, media output, renderer dispatch or production behavior is authorized by this record. C11-C and `CHALLENGE_004` V1 harness/fixture remain immutable.

## Next gate

Prepare a distinct candidate field-to-region/visibility proposal for the four accepted semantic definitions, with all unapproved projection/visibility/timing policy explicitly labelled `PROPOSED_NOT_APPROVED`. Do not implement a payload-side consumer until a separate explicit approval artifact authorizes the necessary policy and scope. Keep CHALLENGE_008/009 blocked pending timebase resolution.
