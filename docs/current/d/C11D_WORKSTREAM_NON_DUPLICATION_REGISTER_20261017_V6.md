# C11-D Workstream Non-Duplication Register — V6 (2026-10-17)

| Surface | Accepted / current artifact | Boundary | Next work must not do |
|---|---|---|---|
| Canonical Challenge planning | `d_renderer_challenge_seed_domain_preflight_v2.py` | 9 selectors, 27 seed cases, 54 planner calls; planning-only | Duplicate planner or misreport as visual payload sensitivity |
| Challenge visual capability | `d_renderer_challenge_visual_payload_capability_matrix_v1.py` | Static inventory, 43 pins, 27 asset refs, 9 mechanics | Convert capability inventory into renderer authorization |
| Challenge semantic binding proposal | `d_renderer_challenge_visual_payload_semantic_binding_proposal_v1.py` | Static proposals only; 0 approved bindings | Consume proposals as approved transforms or serialize all `custom_data` |
| Challenge 004 visual preview V1 | Existing accepted V1 binder/harness | Fixed to `parking_v2 / CHALLENGE_004`; regression fixture | Broaden selector guard or modify the binder in place |
| Visual Loop exact-selector V2 | Existing separate runtime audit | 5 grammar payload instances; no renderer input | Extrapolate its acceptance to Challenge mechanics |
| Visual Loop seed-domain V2 | Existing runtime audit | Five grammars; seed-domain scoped; policy metadata only | Claim global candidate seed domains complete |
| Visual Drill V2 | Existing runtime matrix/seed work | Selector/runtime receipts scoped to Drill | Treat as Challenge payload acceptance |
| D4 and D9.10 adapters | Existing c11c-suite surfaces | Use actual signatures, request boundary and preparation/provenance only | Introduce `c11d-control` or clone adapters |
| Delivery/timebase | Shared timebase policy authority | 008/009 have 11s declared vs 12s phase sum | Resolve duration in Challenge definition without authority |
| Promotion/release | Canonical governance gates | Blocked | Treat static/runtime subgate PASS as renderer or release approval |

## Current ordering

1. Review live source semantics for each proposed binding.
2. Design a separate Challenge runtime-harness V1 and report schema.
3. Static tests and negative cases before any Godot invocation.
4. Runtime source-frame receipts with independent process repeats, safe visual projection and honest per-selector scope.
5. Separate request-boundary music orthogonality and remaining candidate-I/O/seed-domain work.
6. Resolve timebase policy for 008/009 before phase-bound payload acceptance.
7. Re-run D4, existing Challenge 004 V1, Loop V2, Drill V2 and governance regressions before any future gate review.

## Hard governance

C11-C remains immutable and authoritative. `renderer=OFF`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `media_created=false`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `release_authority=NONE`.
