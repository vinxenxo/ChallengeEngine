# C11-D workstream and non-duplication register — 2026-10-17

**Purpose:** identify the canonical implementation for each concern, record what is already proven, prevent duplicate binders/audits, and sequence the remaining work by dependency. This is a dated execution register subordinate to the canonical contracts and the frozen C11-C reference.

## 1. Evidence classes

Never collapse these into one “PASS” category:

1. **Contract regression PASS:** schema/pin/negative behavior, frequently with mocked subprocesses.
2. **Real Godot in-memory runtime PASS:** exact executable/version, live process, validated receipt, runtime digest and declared selector coverage.
3. **Candidate readiness PASS:** the readiness auditor ran correctly and can still report open groups/blockers.
4. **Policy approval:** separate operator decision bound to exact proposal hashes.
5. **Production/media acceptance:** authorized renderer created actual outputs, which were then inspected and repeated.
6. **Baseline approval/freeze/cutover:** formal and separate governance decisions.

A result at an earlier level does not imply a later level.

## 2. Canonical workstream matrix

| Workstream | Existing canonical owner(s) | Last established scope | Do not duplicate | Next work / exit condition |
|---|---|---|---|---|
| Frozen reference | `release/C11C_FREEZE_PACKAGE_MANIFEST.json`; C11-C freeze package | Manifest SHA `e405d08e...4b953` | Never “repair” C11-C to satisfy D | Verify before each overlay; C remains immutable until formal cutover |
| Seed rejection/collision | `d_renderer_seed_domain_collision_audit.py`, its V1 contract/schema/test | Explicit seed presence/range/type, missing/invalid/implicit requests and 4 equal-numeric cross-domain collision cases for fixed Challenge/Loop selector pair; 7/7 regression PASS | Do not clone collision rules into a second unrelated validator or enable `master_seed`/automatic derivation to ease coverage | Reuse the current rejection contract; expand only its source-pinned selector/request coverage in a separately versioned audit |
| Challenge + Loop seed sensitivity | `d_renderer_candidate_seed_domain_audit.py`; `D_RENDERER_CANDIDATE_SEED_DOMAIN_AUDIT_V1.json` | Challenge `CHALLENGE_004` and Loop `harmonic_membrane`, 3 variants, two independent runs each, 12 runtime receipts | Do not repeat the same 12-call matrix; do not call it catalog-wide | Add only after broader canonical selector/request support exists; retain V1 as historical bounded evidence |
| Visual Drill dynamic request/payload binding | `d_renderer_dynamic_request_payload_binding.py` with V2 input/output schemas and Drill harness; `D_RENDERER_DYNAMIC_REQUEST_PAYLOAD_BINDING_V2.json` | 4 drill types × 5 tiers = 20; 20/20 receipts, 67/67 lineage from operator-confirmed Godot run | Do not create a second Drill binder or treat `runtime_receipts=NOT_TESTED` from the source-chain-only regression as invalidating separate live runtime receipts | Reuse accepted V2 path in shared matrices; rerun only if its pinned source changes |
| Visual Drill seed sensitivity/orthogonality | `d_renderer_visual_drill_seed_domain_audit.py` and its V1 contract/schema | Prior operator-reported 20 selectors, 20/20 gameplay sensitivity, 20/20 music orthogonality, 120 invocations, 70 pins; log hash for this specific run not restated | Do not use the payload-binding matrix log as its seed audit log | Treat as prior bounded evidence; recapture only if the seed auditor/source pins change or a traceable-log gate requires it |
| Visual Loop geometric grammar→parameters | `d_renderer_visual_loop_geometric_grammar_matrix_v2.py`, GDScript probe, V2 contract/schema/test | 5 shader grammar IDs × 4 seed values = 20 projection cases; later input-shape repairs are present in snapshot | Do not add another grammar-to-style projection module; do not claim canonical request admission from parameter projections | Runtime status must be checked against the latest post-fix source; final exact-selector runner includes its parent request/reference chain |
| Visual Loop request→parameter instance | `d_renderer_visual_loop_request_scoped_grammar_parameter_binding_v2.py`, its V2 contract/schemas/test | Five request-specific 20-field parameter instances; no full visual payload under this stage alone | Do not promote `parameter_instances_bound=5/5` to `payload_instances=5/5` | Reuse as parent stage to exact-selector V2; no new parameter binder unless a real schema gap is identified |
| Visual Loop exact-selector visual payload | `d_renderer_visual_loop_exact_selector_payload_v2.py`, its contract/schema/harness/test; corrected projection/bound-instance/tolerance layers | Five Geometric Waves grammar IDs; in-memory payload only; no renderer input/shader/media. Final active-Windows post-fix run is not evidenced in this reconciliation | Do not reapply the original overlay or preceding fixes; do not create a parallel payload builder | Run the existing final full-chain audit once under actual Godot 4.7.1, with logs/hashes. Required receipt 5/5 and deterministic repeats 5/5 |
| Challenge dynamic request/payload support | `d_renderer_dynamic_request_payload_binding.py` V1 and Challenge-specific harnesses | Current seed/binder audit receipts for `parking_v2 / CHALLENGE_004` only | Do not add all nine IDs to an allowlist without compatible mechanic-specific payload evidence; do not rewrite fixed V1 pins in place | First source-pinned no-media D9.9/D9.10 planning/adapter inventory for `CHALLENGE_001`–`009`; classify accepted plan, bridge and payload harness separately. Then version a bounded extension for the next genuinely supported selector |
| Request-specific manifests and lineage | Existing Dynamic Request/Payload V1/V2 contracts and request-scoped binding/materialization audits | 10 bounded request cases in V1 chain; 20 Drill V2 manifests and lineage closures; three fixed fixtures for request-scoped binding; 40-entry fixed-fixture materialization join is historical bounded scope | Do not write another manifest generator or claim every request follows the same harness | Extend the existing canonical binder's request manifest/lineage path only after new selector cases are materializable; update source pins and schema/test together |
| Candidate I/O interface contract | `D_RENDERER_CANDIDATE_IO_CONTRACT_V1.json` and schema/test | 30/30 pins, 3/3 schemas, 2/2 fixtures, 13/13 fail-closed and 8/8 schema-instance negatives | Do not use this contract regression as proof of implementation/admission | Keep as fail-closed gate; update only when a new complete input group is implemented/evidenced |
| Candidate I/O gap audit | `d_renderer_candidate_io_gap_audit.py`; `D_RENDERER_CANDIDATE_IO_GAP_AUDIT_V1.json` | 54/54 pins; 0 complete, 6 partial, 4 blocked | Do not duplicate the ten-group gap table in another machine-readable contract; do not report audit PASS as readiness PASS | Re-run after upstream contract/code changes, then update each finding using its own exit criteria |
| Candidate identity inventory | `d_renderer_candidate_identity_inventory.py`; `D_RENDERER_CANDIDATE_IDENTITY_INVENTORY_V1.json` | 164 source inventory entries; runtime output fingerprint and report SHA recorded above | Do not call this a full repository tree freeze | Refresh alongside I/O gap audit when source-pinned candidate files change |
| Unified content review | `d_renderer_unified_content_review.py` and V1 contract/schema/harnesses | Three types; seven real Godot harnesses; 18 cross-artifact checks; ten unresolved gates; `CONSISTENT_NOT_VIDEO_READY` | Do not turn cross-check success into policy approval or create duplicate three-type review harnesses | Keep it as the integration consumer after upstream changes; unresolved policies remain proposal-only |
| Editorial sidecar and consumption | `d_renderer_request_scoped_editorial_value_carrier.py`, editorial field audit, field routing/visibility reconciliation, unified review | 14/14 field parity in review/sidecar; actual visual payload consumption 0/14 | Do not count sidecar fields or textual equality as visible video text | After exact policies are approved, implement a shared D-owned payload-side consumer and prove each approved field value is in the final in-memory payload and intended visible target |
| Shared presentation/geometry | Existing semantic-region, region-hierarchy, neutral-frame-program and coordinate projection/proposal contracts | Proposal/review only; no geometry approval | Do not create another semantic region map or infer coordinate policy from C11-C geometry | Use the existing 9-group decision packet; record approved hashes and then implement the accepted version |
| Timeline/timebase/sample policy | Existing unified delivery-timebase and Challenge temporal/sample/coordinate-composition proposals | Proposal/review only | Do not introduce a parallel frame clock or reinterpret `winning_frame`/`close_calls` | Explicit decisions; derive sample mapping and schedule under approved policy, with negative and deterministic tests |
| Audio/music delivery | Existing unified audio/music delivery proposal, canonical D seed isolation contract | Proposed only; gameplay/music seed separation is locked | Do not duplicate a new music-selection policy or share seed derivation domains | Explicit decision and later output/timeline QA; music seed must not influence visual state |
| GUI / five-surface lifecycle | Existing Producer/adapter/shared production context plus D9.11–D9.13 | D9.13 lifecycle 3 content types, 5 stages, GUI/CLI parity 3/3, Catalog 3/3, Maintenance 3/3, negatives 14/14, persisted parity 4/4; surfaces remain exactly five | No `c11d-control` and no separate GUI business rules | Preserve common context; run lifecycle and relevant GUI contracts after code/contract changes |
| D9.14 / D9.16 / D9.17 / D10 | Canonical qualification, acceptance and adjudication checkpoints | D9.15 `PASS_CLOSED` 13/13; D9.14/D9.16 blocked; D9.17 no-go; D10 blocked | Do not make gate scripts print a desired state or allow subtests to close later gates | Only use canonical procedure after actual required input, explicit D4.8 authorization and controlled real-media evidence |

## 3. Candidate I/O states and specific exit requirements

| Group | Current state | Minimum evidence before reconsidering state |
|---|---|---|
| `content_identity` | PARTIAL | Selector/variant/tier support comes from the admitted canonical matrix, request and payload identity agree, all supported selectors fail closed outside that matrix |
| `source_lineage` | PARTIAL | Complete source/policy chain for every admitted request; manifest/receipt digest joins plan, bridge, adapter and payload without stale or missing pins |
| `payload_instance` | PARTIAL | Request-specific, hash-closed payload instance exists for each admitted selector; current Drill V2 coverage can be reused; the renderer input schema consumes it only after separate approval |
| `seed_domains` | PARTIAL | Seed sensitivity/orthogonality, repeats, invalids/collisions and independent domains proven over the complete *admitted* selector matrix; automatic derivation remains disabled/rejected until separately approved |
| `editorial` | PARTIAL | Request-specific effective values, approved field/window rules and actual in-memory payload consumption; 0/14 consumption remains the current documented value |
| `delivery` | PARTIAL | Resolved delivery profile and approved timebase/output parameters are hash-bound to a complete input |
| `presentation` | BLOCKED | Approved semantic regions/coordinate projection and resolved presentation data bound to the input |
| `timeline` | BLOCKED | Approved timebase, source-time/sampling/temporal/coordinate composition rules and request-specific deterministic schedule |
| `audio` | BLOCKED | Approved audio/music delivery policy, timeline alignment and seed-domain orthogonality evidence |
| `authorization` | BLOCKED | Independent renderer-baseline review/approval, formal freeze as required, and explicit D4.8 decision with hash-bound evidence |

A group can stay open even if its verifier prints PASS. Every audit has two questions: “Did the audit correctly evaluate the rule?” and “Is the evaluated engineering requirement satisfied?” Current I/O result is yes to the first, no to complete input readiness.

## 4. Canonical next-action order

1. Run final exact-selector Visual Loop V2 full-chain runtime acceptance using the current source pins and real Godot 4.7.1. No overlay application first.
2. If it fails, fix only the diagnosed boundary in a new add-only ZIP and rerun the focused tests then real runtime; do not edit the frozen C11-C reference or weaken exact identity/source/hash checks.
3. If it passes, design a separately versioned seed-domain audit over the five geometric grammar selectors, using the accepted existing V2 request→payload stage. No parallel binder.
4. In parallel planning only, produce a source-pinned no-media Challenge planner/adapter matrix for IDs 001–009. This inventories support; it is not a claim that every Challenge can materialize a visual payload.
5. Expand the Challenge seed/payload matrix only for supported and evidenced selector entries; keep unsupported mechanics explicitly rejected.
6. After any meaningful upstream source change, rerun the candidate I/O gap audit and identity inventory, then unified review, D9.13 lifecycle and baseline preflight. Do not rerun unchanged focused gates just to accumulate green output.
7. Consolidate the existing policy packet and record explicit decisions bound to proposal hashes. The packet has nine high-level decisions; the exact-selector contract checks 19 policy approval assertions; these are different denominators.
8. Implement approved editorial consumption and input completeness; independently review the strict candidate-input schema before seeking authorization.
9. Obtain explicit D4.8 authorization through its canonical process before a controlled D-only render; then carry real output into D9.14, D9.16, D9.17, D10 and formal promotion/cutover.

## 5. Closed-loop anti-duplication rules

- Before adding a new file, search both code and contracts for an owner already serving the responsibility in this table.
- Keep accepted fixed V1 audits immutable as evidence; version a new scope rather than mutating a pinned contract or its report meaning in place.
- One canonical binder implementation; versioned schemas/contracts/harnesses are extensions, not competing request builders.
- Policy proposals are inputs to the existing decision packet, not approvals and not alternative policy engines.
- A new summary/report must preserve the exact scope and evidence class of its parent, including “no renderer input/media”.
- Historical README installation instructions are not active work instructions if their overlay paths are already in the designated snapshot.
