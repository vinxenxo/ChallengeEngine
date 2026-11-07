# C11-E D Baseline Isolation — Operator Decision Docket V1

**Date:** 2026-11-07  
**Decision status:** `OPERATOR_DECISION_REQUIRED`  
**Decision scope:** resolve the intentional E4A.6 D-only integration on protected root path `GeneradorMaestro.gd`, without changing C11-C 2.19.12 or its immutable manifest.

## 1. Problem statement

E4A.6 introduced an opt-in D-only Challenge editorial-envelope consumer in root `GeneradorMaestro.gd`. It is loaded only when `--c11e-editorial-envelope=<path>` is supplied; without the envelope, the D consumer is absent and the legacy C flow remains a no-op/unchanged path. The optional aspect is the envelope invocation, not the mandatory canonical editorial field schema.

The frozen C11-C manifest expects this file at 36,991 bytes with SHA-256 `4f10144c62c7bc149bd46aa37494b1df40c7185544b8477153150eec71c1aaf9`. The intentional E4A.6 postimage is 39,767 bytes with SHA-256 `d42782e8f5bb94ff0ede653a1c4624dc91541cc8203abf136b09a8fc288a7d82`. The baseline candidate policy protects `GeneradorMaestro.gd` as an exact-match C path and only permits D integration under declared D roots. The strict candidate audit therefore rejects this postimage even though the change is documented and D-only.

This is `KNOWN_E4A6_D_ONLY_POSTIMAGE_POLICY_CONFLICT`, not unknown drift and not evidence that simulation truth or mechanics were changed. E4A.7 proves an isolated D-composited Challenge A/V test with preserved source H.264 in its historical test route, but it does not establish that a new independent post-composition consumer for all Loop grammars exists.

## 2. Non-negotiable conditions

- Do not blindly restore or overwrite `GeneradorMaestro.gd`.
- Do not modify `release/C11C_FREEZE_PACKAGE_MANIFEST.json` or the frozen manifest hash.
- Do not add a silent protected-path exception or mark the candidate baseline clean.
- Do not clone C mechanics, RNG, binders, timeline or renderer.
- Do not add a sixth operational GUI surface or parallel binder.
- Keep original C source video/frames as immutable input; all D-composited outputs are separate artifacts.

## 3. Alternatives

### Option A — D/E-owned root or scene boundary referencing frozen C implementation

Create a D-owned entry scene/root that instantiates or references the frozen C implementation and supplies D-only integration at an approved scene boundary.

**Advantages:** Godot-native integration; can maintain per-frame presentation behaviour; root-level C file can return to exact frozen identity once the boundary works.

**Costs/risks:** Godot scene/script lifecycle and bind points must be proven without a second binder; possible duplication of root setup or fragile coupling to C node paths; may be more difficult to share across five Loop prototypes and their family-specific scenes. Must not introduce another operational surface.

### Option B — bounded source-level policy exception

Keep the E4A.6 postimage at `GeneradorMaestro.gd`, retain the exact frozen C preimage and produce a narrowly scoped policy exception record.

**Advantages:** lowest immediate code migration cost; preserves proven E4A.6 runtime integration.

**Costs/risks:** remains a protected-path exception in the D candidate; requires a policy/schema change and independent review; weakens the present exact protected-path equality rule for this candidate. This is not recommended while a clean external boundary is available.

### Option C — D-only post-composition over immutable C source output (recommended)

Run the existing C11-C launcher unchanged to create a silent C source video. R1V measures and hashes the actual source frames. A D-only post-composition consumer then reads the D9.9/D9.10 request/envelope plus the immutable source, applies D-owned layout/editorial layers according to approved timing/geometry, and writes a new D output artifact. D3/music/mux is a later independent stage. The C source file remains intact and is preserved separately with its hash.

**Advantages:** cleanest separation of concerns; preserves all protected C code and mechanics; makes R1V the stable boundary between C visual generation and D presentation; naturally scales across 5 families/27 grammar variants; no second C binder and no new GUI surface.

**Costs/risks:** a real D-only compositor still has to be implemented; the D video output will normally be encoded as a new stream (and therefore must not be represented as byte-identical C source media); the pipeline must pin encoder/filters and independently validate geometry, timestamps, frame count and pixel identity of the input source. This option is recommended because the project objective is D presentation/editable editorial on top of the existing C generator while leaving C mechanics unchanged.

## 4. Recommendation and proposed sequence

Recommend **Option C**. Its separation makes the source-to-presentation contract explicit:

`C11-C silent source video -> R1V measured frame inventory/pixel hashes -> D-only editorial/layout compositor -> D3 audio/mux -> final output`.

The compositor must consume the same canonical D9.9/D9.10 request/parent identity as R1P, and must fail closed on content identity, policy, timebase, geometry, field-window or source-hash mismatch. It must preserve an immutable copy of the C source and never overwrite it. The D output must have its own report, source-link, encoder pins and QA evidence.

The recommended next implementation increment after operator decision is a D-only post-composition consumer contract and static/negative harness (no renderer invocation), then the bounded D4.8 qualification policy/checkpoint. R1V physical qualification comes only after both pass.

## 5. Separate D4.8 clarification

D4.8/D4.9 historical artifacts say PASS/CLOSED because the governance validator correctly exercises 8/8 deny/validation cases and 102/102 GUI/CLI parity. The active production activation policy still has `renderer_activation_policy.state=DISABLED`; REVIEW mode cannot authorize execution and production requires a distinct renderer approval. Therefore the historical PASS/CLOSED record is not a permit for R1V.

The next governance work should define a limited `R1V_QUALIFICATION_ONLY` authorization or equivalent separate policy checkpoint. It must enumerate allowed C11-C launcher calls, selected family/grammar, `-NoSound`, unique output roots, allowed read-only frame/pixel inspection, pinned toolchain, no D3/audio/mux/compositor and no production/release/promotion. The policy author and approver must be explicit; do not silently set the existing v1 renderer policy to APPROVED.

## 6. Operator decision requested

Please select the architecture route:

- **A:** D/E-owned Godot root/scene boundary;
- **B:** bounded exception with exact C preimage retained;
- **C:** D-only post-composition of immutable C source video (recommended).

No code path is being changed by this docket. Until the operator decision is recorded, keep the current root postimage intact and preserve the baseline conflict classification. Even after the architecture decision, physical R1V remains blocked until the separate bounded D4.8 authorization checkpoint is approved.
