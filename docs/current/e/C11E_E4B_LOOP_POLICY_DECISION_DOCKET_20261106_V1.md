# E4B Loop Current-Hash Policy Decision Docket — V1

**State:** `OPERATOR_DECISION_REQUIRED_NOT_APPROVED`. This docket supersedes the stale fingerprint references in the historical D renderer approval packet V1 for the Loop-relevant decision groups only. It does not modify any D policy JSON, grant renderer input, alter D4.8 or authorize production.

## Decision protocol

For each group, the operator must select exactly one: `APPROVE AS PROPOSED`, `REQUEST CHANGES`, or `DEFER`. The decision must explicitly confirm the entire proposal SHA-256 below. Any approval becomes binding only after it is written into a versioned D-owned decision record, source-pinned, and covered by focused positive/negative tests. No response, blank value or prior approval against a different SHA counts as approval.

## Visual composition decisions required for E4B consumer work

| Group | Authoritative proposal | Current exact SHA-256 | Decision | SHA confirmed | Rationale / change | Operator + date |
|---|---|---|---|---|---|---|
| A.1 Shared presentation semantic regions | `definitions/c11d/production/D_RENDERER_UNIFIED_PRESENTATION_REGION_POLICY_PROPOSAL_V1.json` | `101092bb32127bb8854a501a9215c0b6cf69581594383903716907d49719c01a` | PENDING | PENDING | PENDING | PENDING |
| A.3 Loop/Drill editorial field windows | `definitions/c11d/production/D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json` | `609a4d183aac07c2cbe1abaf41444160fdd137217faffbead3aef618320d57dc` | PENDING | PENDING | PENDING | PENDING |
| E4B Loop outer editorial composition | `definitions/c11d/production/C11E_E4B_LOOP_EDITORIAL_COMPOSITION_PROPOSAL_V1.json` | `9e206704665ea85226ecc10854be9f679c32fe9ed7efb690a829f6e8456d43da` | PENDING | PENDING | PENDING | PENDING |

Until all three current-hash decisions are recorded, no D-only Loop editorial consumer implementation, renderer-native input or family visual payload expansion is authorized. The proposal geometry remains unapproved; actual Godot shaping/fallback/legibility must be tested after decision and implementation authorization.

## Later A/V decisions — not part of immediate visual consumer approval

| Group | Authoritative proposal | Current exact SHA-256 | Decision | SHA confirmed | Rationale / change | Operator + date |
|---|---|---|---|---|---|---|
| B.1 Unified delivery timebase | `definitions/c11d/production/D_RENDERER_UNIFIED_DELIVERY_TIMEBASE_POLICY_PROPOSAL_V1.json` | `41a62b0766db47cd99772f28642ef67766314f20f0f7891789d6b7497bbfee85` | PENDING — LATER A/V GATE | PENDING | PENDING | PENDING |
| D.1 Unified audio/music delivery | `definitions/c11d/production/D_RENDERER_UNIFIED_AUDIO_MUSIC_DELIVERY_POLICY_PROPOSAL_V1.json` | `3dd4874e1b6506de6d9ddbe6ad1b567a284b94cc00ef1bac0d35d1731af05e23` | PENDING — LATER A/V GATE | PENDING | PENDING | PENDING |

No music asset selection, synthesis, mixing, loudness operation, audio emission or mux may occur until B.1 and D.1 are separately decided and recorded. Loop must preserve the existing C11-C family music route and use `request.music_seed`, independently from visual `request.seed`. D3 V5 is not the Loop music path.

## Why packet V1 is not sufficient

`docs/current/d/D_RENDERER_POLICY_APPROVAL_DECISION_PACKET_V1.md` remains `REVIEW_PACKET_ONLY_ALL_POLICIES_UNAPPROVED`. A.1's hash still matches, but its A.3, B.1 and D.1 SHA values are stale. No operator decision is recorded in packet V1, and no approval may be transferred to the current hashes shown here. Packet V1 is retained unchanged as historical evidence.

## Separate technical reconciliation gates

1. D9.8 currently says Loop `ACTIVE_MODEL_ONLY` and `PENDING_D9_9_UNIVERSAL_REQUEST_ADAPTER`. The 81-case matrix proves D9.9 `UNIVERSAL_EDITORIAL_INTENT_PLAN_ONLY`, not D4 executable compatibility. A versioned semantic reconciliation must preserve that distinction.
2. Historic D exact-selector Godot payload coverage remains five Geometric Waves grammars only, in memory; renderer inputs `0/5`; approvals granted `0`. All-family matrix parity does not expand renderer admission to other families.
3. The other 22 grammar selectors/four non-geometric families require review of their own request-bound family binding and payload construction. Do not copy the geometric binder/payload or remove selector guards.

## Governance

All current policy approvals remain false. `renderer=OFF`; renderer input/dispatch/media false; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14/D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `release_authority=NONE`. C11-C 2.19.12 and its frozen manifest remain immutable.
