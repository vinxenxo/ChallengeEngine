# V2-B plan — semantic binding review and runtime acceptance gate design

Date: 2026-10-17
Status: PLANNING ONLY. No bindings approved, no runtime harness authorized by this plan, no payloads materialized.

## Gate A — inspect sources and schemas

Reopen the current checkout and verify the two contracts by hash:

- Capability matrix `definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_CAPABILITY_MATRIX_V1.json`: `3b4375957da12d16a6c7f652c1ba2536ce1a819b781b68b15e5dd3f0ee4bda75`.
- Semantic binding proposal `definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_SEMANTIC_BINDING_PROPOSAL_V1.json`: expected package/source reference SHA `d37cb74f360e19e664b94673bbf4b95462cad6e681a08215a95f4565c6e810aa`.
- Frozen C11-C manifest: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

If any hash differs, stop and reconcile against the active checkout. Do not copy a hash from a stale snapshot.

## Gate B — field-by-field semantic review

For each of the nine secondary proposals, record:

- challenge selector and owning mechanic;
- concrete source field and source file/hash;
- canonical type, units, coordinate frame and valid range;
- frame/time sampling semantics relative to `winning_frame`;
- no-value/out-of-range behavior;
- visible property that the field is allowed to control;
- fields it must not affect (simulation/result/input/pause/editorial identity);
- deterministic repeat check and gameplay-seed mutation expected;
- music-seed orthogonality expected;
- review decision, reviewer rationale and test coverage.

Review each of the six `custom_data` candidate fields separately. They are not allowed just because the field exists or its asset reference resolves. Keep every approval flag false until the evidence supports a specific decision. The expected current total is zero approved bindings.

## Gate C — temporal issues are independent

Maintain separate unresolved records for `CHALLENGE_008` and `CHALLENGE_009`, where declared total duration conflicts with phase-duration sum. Record the source field values and the responsible decision needed. Do not auto-correct, infer a preferred value, or treat visual binding approval as a timing decision.

## Gate D — runtime harness design (design first, implementation after review)

The eventual bounded harness must separate three identities:

1. canonical request/plan identity;
2. semantic binding instance identity;
3. materialized visual payload identity.

For each challenge selector, it should test same-input repeat stability; gameplay-seed mutation changes the intended visual payload; music-seed mutation does not change gameplay-driven visuals; editorial identity remains invariant when only seeds change; all selected source and asset references remain pinned; invalid/unsupported bindings fail closed; no writes/media/renderer-input emission occurs.

A PASS for request or plan hashes alone is not a pass for visual payload seed sensitivity. Report distinct field-level and final payload hashes separately. Define exact runtime invocation count and receipt schema before executing Godot.

## Gate E — bounded Godot validation

Only after Gates A–D are reviewed and tests pass, design the runtime audit using the configured Windows Godot 4.7.1 Mono executable, not a stale hard-coded executable path. Keep it non-rendering and non-media-producing. Capture executable/version, command, exit code, stdout/stderr, source lineage, each invocation receipt, aggregate report and SHA-256 fingerprints. No renderer inputs may be emitted.

## Gate F — regression and documentation

Run existing Challenge planner preflight, V2-A matrix tests, semantic binding proposal tests, seed/domain regression and the applicable cross-type audits. Do not overstate their scope; each report must indicate exactly which selectors were exercised. Update checkpoint and prompts only from observed evidence.

## Invariants and blockers

- `winning_frame` is the sole temporal anchor; `close_calls` only counts episodes.
- Logical frame 540×960: Header 0–144, Body 144–816, Footer 816–960.
- Delivery profile 720×1280 at 30 FPS does not authorize resampling the preview source.
- No simulation/input/pause/result changes from presentation.
- Renderer OFF; no media; candidate input inadmissible; seed-domain completeness false; release authority NONE; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION.
