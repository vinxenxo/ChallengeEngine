# E4B Loop Policy Readiness Review — V1

## Purpose

Separate accepted D9.9 plan-only matrix coverage from the approvals required for a D-only visual consumer. This review is not itself an operator approval or policy change.

## Current policy fingerprints

| Policy group | Current JSON | Current SHA-256 | Packet V1 fingerprint | Packet state |
|---|---|---|---|---|
| A.1 shared presentation semantic regions | `D_RENDERER_UNIFIED_PRESENTATION_REGION_POLICY_PROPOSAL_V1.json` | `101092bb32127bb8854a501a9215c0b6cf69581594383903716907d49719c01a` | same | MATCH; still unapproved |
| A.3 Loop/Drill editorial field windows | `D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json` | `609a4d183aac07c2cbe1abaf41444160fdd137217faffbead3aef618320d57dc` | `25fe4aaaaa94a80dbabcbf92533ff9c19a9d61cc0b3173cb0cd986a62701fd57` | STALE |
| B.1 unified delivery timebase | `D_RENDERER_UNIFIED_DELIVERY_TIMEBASE_POLICY_PROPOSAL_V1.json` | `41a62b0766db47cd99772f28642ef67766314f20f0f7891789d6b7497bbfee85` | `251b2384aabfe975b55938bc4a6696aba81b8dc817aa6902bf1f60f3894ad019` | STALE |
| D.1 unified audio/music delivery | `D_RENDERER_UNIFIED_AUDIO_MUSIC_DELIVERY_POLICY_PROPOSAL_V1.json` | `3dd4874e1b6506de6d9ddbe6ad1b567a284b94cc00ef1bac0d35d1731af05e23` | `f6fac5edf88269885c18d9b8272214f28d8bb3569cc4da249d2d67c727dac0a8` | STALE |
| E4B Loop composition | `C11E_E4B_LOOP_EDITORIAL_COMPOSITION_PROPOSAL_V1.json` | `9e206704665ea85226ecc10854be9f679c32fe9ed7efb690a829f6e8456d43da` | not included in packet V1 | separate C11-E proposal; unapproved |

The D renderer packet V1 remains `REVIEW_PACKET_ONLY_ALL_POLICIES_UNAPPROVED`. Its protocol requires the operator to decide against the exact proposal SHA and then record a versioned D-owned decision record plus focused tests. Do not use stale hashes or silently carry forward any prior decision.

## D9.8/D9.9 semantic boundary

The current D9.8 model JSON SHA-256 is `50655c82521a353f1db6920f4d099cad92452ae369251f9fbde45cbaee4e8c53`. It states Loop `model_state=ACTIVE_MODEL_ONLY` and `request_plan_compatibility=PENDING_D9_9_UNIVERSAL_REQUEST_ADAPTER`. The accepted matrix independently demonstrates D9.9 plan-only `PLANNED` over 27 selectors. These facts must be represented separately. No D4 executable-plan/renderer compatibility is proven; do not rewrite D9.8 metadata in the readiness step.

## Historical scope restrictions

- Exact-selector Godot payload runtime remains Geometric Waves-only: five in-memory selector payloads, no renderer input, zero approvals granted. The other 22 grammar selectors/four other families have not passed that path.
- Request-bound timing carrier is preparation-only and not approved.
- Loop/Drill field-window review is integrated for review only, with `visibility_windows=null` and zero evaluated windows.
- Shared-region geometry remains unresolved; current Loop composition proposal is not approved and has only static arithmetic/geometry checks.
- Font shaping/fallback, raster clipping/wrapping, visual legibility and actual compositor coexistence are unverified.

## Decision sequencing

Immediate visual decision docket: A.1 shared regions, A.3 Loop/Drill windows, E4B Loop composition. Do not implement the D-only consumer before these current-hash decisions and family-binding scope review are versioned and tested.

Later A/V docket: B.1 unified delivery timebase and D.1 audio/music policy must be reconciled before any Loop A/V materialization. The family music route must remain C11-C-owned; use `request.music_seed` separately from `request.seed`. This readiness audit does not select music or authorize generation.

Expected read-only audit status: `PASS_AUDIT_ONLY_POLICY_APPROVAL_REQUIRED`; stale packet V1 count 3; renderer input false; release authority NONE.
