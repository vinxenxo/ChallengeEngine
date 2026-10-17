# C11-D Workstream Non-Duplication Register V3 — 2026-10-17

This register prevents new V2 seed validation from forking the already accepted request/payload chain. The current step is an audit-only consumer of existing parents, not a new producer/binder/policy owner.

| Concern | Canonical owner | New audit behavior | Prohibited duplication or claim |
|---|---|---|---|
| Request selection/plan/seed normalization | `universal_producer.py` and D9.9 request contract | Rebuilds canonical request chain for every seed pair | Do not handcraft plan hashes or reuse a baseline chain for mutations. |
| Editorial bridge/adapter chain | `editorial_render_bridge.py`, `d_render_adapter.py` | Recomputes bridge/adapter hashes per explicit variant | Do not fork those services. |
| Source lineage | V1 source-binding core + accepted V2 direct pins | Rebuilds an in-memory family-source binding per variant and validates all 70 accepted source pins | Do not change parent V1 source binding or shrink the pin set. |
| Grammar parameters | `d_renderer_visual_loop_request_scoped_grammar_parameter_binding_v2.py` | Calls existing `_run_one`/receipt verifier for each row | Do not add a second parameter binder. |
| Exact selector payload | `d_renderer_visual_loop_exact_selector_payload_v2.py` | Calls existing exact payload probe and validates parent binding linkage | Do not fork the payload model or change the accepted V2 contract. |
| Timing/review policy references | `d_renderer_visual_loop_timing_review_request_bound_reference_carrier.py` | Reuses selector-scoped reference metadata; asserts nine references, `source_envelope_request_bound=false` and values not consumed | No policy consumption or false assertion that a changed seed is bound into this selector metadata carrier. |
| Explicit seed-domain semantics | New `d_renderer_visual_loop_seed_domain_audit_v2.py` | Compares request/binding/payload identity and gameplay-derived visual projections across 5 grammars × 3 variants × 2 repeats | Does not prove automatic seeds, master seed, arbitrary collisions, other Loop families/Drills/Challenges or candidate-wide completeness. |
| Runtime proof | Active Windows Godot 4.7.1 | Pending operator run after applying this overlay | Unit tests/planning preflight are not Godot runtime PASS. |
| Renderer/promotion authority | Existing D4.8/D9.14/D9.16/D9.17/D10 gates | Unchanged | Never enable renderer, emit renderer input, create media or promote baseline from this audit. |

## Existing completed work not to repeat

- Request-scoped grammar parameter binding V2 and exact-selector payload V2 implementation and contract tests.
- Active-Windows exact-selector payload runtime audit: 70/70 source pins; five payloads, five deterministic repeats, 45 policy reference pairs, zero renderer inputs/approvals.
- Visual Drill V2 dynamic request-to-payload matrix: 20/20 actual runtime receipts.
- Existing bounded V1 cross-type seed audit on one Challenge and one Loop grammar.

## Immediate next gate

Apply the add-only V2 seed audit overlay, run only `test_d_renderer_visual_loop_seed_domain_audit_v2.py`, then run the new audit on active Windows/Godot. Preserve every locked value. If it passes, start the Challenge seed subpopulation as a new scoped audit; do not rerun already accepted Loop payload matrix unless its source pins drift.
