# C11-D — Renderer Policy Approval Decision Packet V1

**Status:** `REVIEW_PACKET_ONLY_ALL_POLICIES_UNAPPROVED`  
**Scope:** consolidate decisions required before a payload-side visual consumer or prospective renderer input can be implemented. This document is not a policy, does not resolve source proposals, and records no operator approval.

## Decision protocol

For each group, the operator must explicitly select **APPROVE AS PROPOSED**, **REQUEST CHANGES**, or **DEFER** and identify the exact proposal SHA-256 being decided. A selection is not binding until written back as a versioned D-owned decision record, pinned by the relevant contracts, with its own focused positive/negative tests. Blank/pending values mean unapproved. No proposal file is modified by this packet. No values below should be treated as defaults that can flow into runtime.

## A. Semantic regions, frame geometry and editorial visibility

| Decision group | Authoritative proposal | SHA-256 | Required decision | Current status |
|---|---|---|---|---|
| Shared presentation semantic-region map | `definitions/c11d/production/D_RENDERER_UNIFIED_PRESENTATION_REGION_POLICY_PROPOSAL_V1.json` | `101092bb32127bb8854a501a9215c0b6cf69581594383903716907d49719c01a` | Region IDs/meaning and shared-frame inheritance | PENDING — NOT APPROVED |
| Challenge editorial field windows | `definitions/c11d/production/D_RENDERER_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json` | `23c33f99f0bef1c76edc6526bcdfa6bf98dc27d7d22b38f48a424008f8f59c5f` | Field → region/window; universal fields and phase-field namespace stay distinct | PENDING — NOT APPROVED |
| Visual Loop/Drill field windows | `definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json` | `25fe4aaaaa94a80dbabcbf92533ff9c19a9d61cc0b3173cb0cd986a62701fd57` | Shared presentation inheritance and the full-span/timing semantics | PENDING — NOT APPROVED |

Until these decisions are approved, editorial visual payload consumption remains **0/14**, no evaluated text visibility windows are inferred, `CHALLENGE_OVERLAY` remains a semantic role rather than fixed coordinates, and Challenge phase fields `hook/reveal/cta` must not alias `title/subtitle/call_to_action`.

## B. Timebase, temporal alignment and delivery

| Decision group | Authoritative proposal | SHA-256 | Required decision | Current status |
|---|---|---|---|---|
| Unified delivery timebase | `definitions/c11d/production/D_RENDERER_UNIFIED_DELIVERY_TIMEBASE_POLICY_PROPOSAL_V1.json` | `251b2384aabfe975b55938bc4a6696aba81b8dc817aa6902bf1f60f3894ad019` | Frame/sample clock conversion, rounding, interval and resampling semantics | PENDING — NOT APPROVED |
| Challenge temporal alignment | `definitions/c11d/production/D_RENDERER_CHALLENGE_TEMPORAL_ALIGNMENT_POLICY_PROPOSAL_V1.json` | `bf8084f4d6e1257ac3aa594cd5a5625a6814d9022643774f152392558a224dd4` | Source event/frame alignment and legal sample selection boundaries | PENDING — NOT APPROVED |

No new `winning_frame` or `close_calls` interpretation is permitted. These fields remain governed by their existing simulation meanings; the review packet does not reinterpret simulation truth.

## C. Challenge sampling and coordinates

| Decision group | Authoritative proposal | SHA-256 | Required decision | Current status |
|---|---|---|---|---|
| Simulation sample selection | `definitions/c11d/production/D_RENDERER_CHALLENGE_SIMULATION_SAMPLE_SELECTION_PROPOSAL_V1.json` | `3e278481afe9d66458f05f29c15275819af49f9b68120b6a0b39dda2e9715cf3` | Selection of source-bound simulation records for payload composition | PENDING — NOT APPROVED |
| Coordinate sample composition | `definitions/c11d/production/D_RENDERER_CHALLENGE_COORDINATE_SAMPLE_COMPOSITION_PROPOSAL_V1.json` | `72aa659dfc464ce8f2205cc483c18cdff96b82e55f3651102310f9f83ce897b4` | Permitted coordinate records and ordering for a review payload | PENDING — NOT APPROVED |
| Coordinate projection | `definitions/c11d/production/D_RENDERER_CHALLENGE_COORDINATE_PROJECTION_V1.json` | `c1caf8e640595bc89957f17ef8bbd7abe80a92cac18cf77974633a1ddde0e264` | Coordinate systems/transforms, normalization and bounds | PENDING — NOT APPROVED |

No exploratory normalized bounds or ad hoc coordinate transform become canonical by virtue of this list. Any accepted mapping must preserve source lineage, deterministic ordering and negative validation.

## D. Audio and music delivery

| Decision group | Authoritative proposal | SHA-256 | Required decision | Current status |
|---|---|---|---|---|
| Unified audio/music delivery | `definitions/c11d/production/D_RENDERER_UNIFIED_AUDIO_MUSIC_DELIVERY_POLICY_PROPOSAL_V1.json` | `f6fac5edf88269885c18d9b8272214f28d8bb3569cc4da249d2d67c727dac0a8` | Audio enablement, music-seed separation, source/schedule and output obligations | PENDING — NOT APPROVED |

Music seed remains separate from gameplay seed and cannot influence visual-state digest. This packet does not grant access to audio output or dispatch.

## E. Explicit operator decision record — intentionally blank

| Group | Decision (`APPROVE AS PROPOSED` / `REQUEST CHANGES` / `DEFER`) | Proposal SHA confirmed | Rationale / requested change | Operator + date |
|---|---|---|---|---|
| A.1 Shared presentation regions | PENDING | PENDING | PENDING | PENDING |
| A.2 Challenge field windows | PENDING | PENDING | PENDING | PENDING |
| A.3 Loop/Drill field windows | PENDING | PENDING | PENDING | PENDING |
| B.1 Unified timebase | PENDING | PENDING | PENDING | PENDING |
| B.2 Challenge temporal alignment | PENDING | PENDING | PENDING | PENDING |
| C.1 Simulation sample selection | PENDING | PENDING | PENDING | PENDING |
| C.2 Coordinate sample composition | PENDING | PENDING | PENDING | PENDING |
| C.3 Coordinate projection | PENDING | PENDING | PENDING | PENDING |
| D.1 Audio/music delivery | PENDING | PENDING | PENDING | PENDING |

## Governance

This packet grants no approval and does not change any source proposal or runtime contract. No renderer input, dispatch, shader execution, media output, freeze, release or promotion is permitted. `renderer=OFF`; `media_created=false`; `D4.8=BLOCKED`; `release_authority=NONE`; `baseline_approval=MISSING`; `freeze_eligible=false`. C11-C 2.19.12 and its frozen manifest remain immutable. D9.14 and D9.16 remain blocked, D9.17 remains NO-GO, and D10 remains blocked. Future C11-D cutover as baseline/Producer remains conditional on complete D acceptance and formal approval/freeze.
