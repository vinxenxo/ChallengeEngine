# C11-D Future Renderer Baseline Preparation Plan V1

**State:** `PREPARATION_ONLY_NOT_APPROVED_NOT_FROZEN`  
**Current candidate:** `C11-D-BASELINE-CANDIDATE-0.1`  
**Date:** 2026-10-09  
**Owner boundary:** C11-D only; C11-C 2.19.12 and its freeze manifest remain immutable.

## Current spatial-contract reconciliation — 2026-10-10

The first normalized semantic-region boxes passed their proposal-generator tests on Windows, but those PASS results did not approve the geometry. D1.5 already specifies the shared 540×960 logical `HEADER` / `BODY` / `FOOTER` frame, and the existing profile distinguishes this social frame from profile-driven safe/content geometry. Family-specific layout behavior remains with the existing profile/binder/renderers. See `D_RENDERER_REGION_HIERARCHY_RECONCILIATION_CHECKPOINT_V1.md`; do not drive the temporal proposal from the previous normalized box set.


## Current hierarchy status after proposal testing — 2026-10-10

The operator has confirmed the logical-composition, renderer-neutral frame-program and normalized region-proposal focused tests on Windows. Those passes establish deterministic preparation contracts and fail-closed behavior; they do not approve a renderer or layout. The normalized region proposal was intentionally not promoted. Source review has since reconciled the future D renderer with the existing D1.5 540×960 `HEADER` / `BODY` / `FOOTER` frame, the separate profile-driven safe/content geometry, and the existing family-specific binder/renderer paths. The active checkpoint is `D_RENDERER_REGION_HIERARCHY_RECONCILIATION_CHECKPOINT_V1.md`; follow it instead of treating the old proposed rectangles as canonical.

Windows confirmed the region-proposal test: content types 3/3, deterministic 3/3, editorial flow 3/3, negative 20/20 and structural schema 3/3. The optional `jsonschema` package was absent on Windows; preparation-workspace Draft 2020-12 validation succeeded for that proposal. This evidence validates the proposal builder and its locks only, not its coordinates.

The next design item after the hierarchy-reconciliation focused test is a separate temporal proposal that derives timing from explicit supported duration/timeline contracts. Unknown duration or phase timing remains unknown; no values should be synthesized from the normalized region proposal.

## 1. Why this is the next work item

The latest Windows run confirms canonical D9.15 `PASS_CLOSED`, D9.16 preflight integration, candidate preflight and aggregate Suite 22/22. D9.15 is no longer the gating issue. The remaining candidate blockers are:

1. `D9_14_REAL_MEDIA_CERTIFICATION_BLOCKED`;
2. `D9_16_FULL_ACCEPTANCE_NOT_CLOSED`;
3. `D9_17_CLOSURE_NO_GO`;
4. `D_RENDERER_BASELINE_APPROVAL_NOT_RECORDED`;
5. `D_BASELINE_APPROVAL_NOT_RECORDED`.

D9.14 explicitly requires a separately approved/frozen future D renderer baseline and explicit D4.8 governance authorization. This plan prepares the engineering work; it does not approve either gate.

## 2. Scope for the engineering candidate

The future renderer must be D-owned and versioned, separate from the frozen C11-C renderer/source baseline. It must not edit protected C11-C source or change `release/C11C_FREEZE_PACKAGE_MANIFEST.json`.

Supported scope is Challenge, Visual Loop and Visual Drill. Longform remains unsupported until canonical D request and renderer contracts explicitly support it. The renderer candidate must eventually demonstrate that editor-controlled values in the canonical D request/plan reach the rendered content, rather than appearing only in provenance metadata.

D9.10 remains an inspection-only bridge/adapter envelope with status `PREPARED_NOT_DISPATCHED_RENDERER_DISABLED`. It is not renderer-native input. Do not add dispatch to `d_render_adapter.py`; any future request-to-renderer translation and dispatcher must be separately versioned, governed and locked behind authorization checkpoints.

## 3. Required contract and implementation deliverables

### A. D-owned renderer identity

- Versioned renderer specification and implementation identity.
- Explicit scope for Challenge, Visual Loop and Visual Drill; explicit unsupported Longform rule.
- Versioned input/output schema; fail-closed behavior for unknown fields, missing required values, invalid profiles and unauthorized execution.
- Immutable references to the canonical D request, universal editorial model, producer plan, bridge record and prepared adapter envelope.
- Per-stage SHA-256 and lineage identifiers; source revision and renderer/build identity in output provenance.

### B. Determinism and seed isolation

- Same canonical request and same seeds reproduce the same logical frame stream and audio PCM/parameters according to a declared deterministic comparison contract.
- `request.seed` remains gameplay-domain only and `request.music_seed` remains music-domain only; no `master_seed`, cross-domain seed reuse, automatic seed generation or runtime seed derivation.
- Changing only `music_seed` must not change gameplay/simulation truth or visual sequence; its audio impact is independently identified.
- Editorial-only changes must change the intended rendered property and must not mutate `SimulationResult`, `winning_frame`, `close_calls`, mechanics or C11-C simulation truth.
- Worker count, render ordering and unrelated content must not change governed determinism outputs unless a versioned contract explicitly defines an allowed difference.

### C. Provenance and quality contracts

- Traceable chain: canonical request → editorial resolution → producer plan → D9.10 bridge → prepared envelope → separately authorized D renderer input → rendered outputs → visual/audio QA → Catalog identity/provenance → deterministic reproduction.
- Explicit frame size/rate and delivery encoding profile bound to the selected approved profile; current bounded qualification uses H.264/YUV420P at 720×1280/30 fps, but that bounded path is not automatically the universal D renderer baseline.
- Audio-enabled outputs must contain a decodable audio stream and pass declared loudness/peak/mobile QA; silent or near-silent output fails closed.
- Output manifest identifies hashes of video, audio, final mux, request, plan, renderer contract, renderer build, profiles and QA reports.
- Real-media comparison distinguishes file hash identity from decoded-frame/audio identity where container metadata may differ.

### D. Negative and boundary tests

- Invalid or ambiguous requests fail closed before renderer launch.
- Unknown content types and Longform fail closed until explicitly supported.
- Editorial identity mutation is visible in the intended rendered result.
- Gameplay/music seed isolation and same-configuration reproducibility pass.
- Protected C11-C roots and the historical manifest remain byte-identical.
- Invalid/tampered provenance, altered adapter envelopes, output-path escape, unauthorized release and any attempt to activate without D4.8 all fail closed.
- No test may change the activation policy, grant authority, produce media in the D9.10 Qt harness, or silently route the PREPARE_ONLY envelope to a renderer.

## 4. Work sequence — do not skip governance boundaries

1. **Contract design:** define the D renderer input/output schemas and mapping from the D9.10 prepared envelope. Keep the translation interface inert and non-dispatching.
2. **Isolated implementation:** add D-owned renderer candidate files only in approved D roots. Do not patch protected C11-C sources.
3. **Static/unit acceptance:** test schema, field binding, provenance, seed-domain isolation, deterministic logical output contracts, path safety, and all negative cases without production invocation.
4. **Candidate identity:** produce a read-only inventory, source fingerprint, manifest linkage, build/tool versions and review packet. Do not generate the baseline approval checkpoint yet.
5. **Independent approval:** the renderer baseline review must explicitly identify the implementation/contract hashes and record an accountable approver. D4.8 must be authorized by its separate governance decision; a local file, test pass or preflight cannot infer authorization.
6. **Authorized D9.14 execution:** only after valid renderer-baseline approval/freeze and D4.8 authorization exist, run the ten declared GUI E2E cases, produce real media, validate audio/video/provenance/replay and accept the Windows operator evidence.
7. **D9.16/D9.17:** rerun full acceptance against the complete evidence packet and adjudicate closure explicitly. Only then prepare the exact-source `D_BASELINE_APPROVAL_CHECKPOINT.json` and a separately approved/frozen C11-D baseline.

## 5. Approval checkpoints are deliberately absent

`docs/current/d/D_RENDERER_BASELINE_APPROVAL_CHECKPOINT.md` must not say `Decision: APPROVED` before the renderer candidate has been reviewed and the required explicit D4.8 decision exists. `docs/current/d/D_BASELINE_APPROVAL_CHECKPOINT.json` must not be generated as an approval until it binds to the exact reviewed candidate source fingerprint, immutable C11-C manifest SHA-256, valid renderer-baseline checkpoint SHA-256, reviewer and UTC timestamp.

This plan is not an approval, does not change the canonical activation policy and is not sufficient to run D9.14. Keep `D4.8=BLOCKED`, renderer OFF, production/media disabled, `release_authority=NONE`, D9 OPEN and D10 BLOCKED.

## 6. Pre-implementation checks

Run from the active Windows checkout before beginning the renderer candidate implementation:

```powershell
python .\tools\c11d\d9\test_editorial_render_bridge.py
python .\tools\c11d\d9\test_cross_suite_lifecycle.py
python .\tools\c11d\baseline_candidate\operator_evidence.py status
python .\tools\c11d\baseline_candidate\test_d_baseline_candidate.py
python -u .\c11c-suite\self_test.py
```

Expected baseline state: bridge/lifecycle pass; D9.15 remains `PASS_CLOSED`; candidate preflight passes as an audit with the five independent blockers, `freeze_eligible=false`; aggregate Suite 22/22. Recompute the candidate source fingerprint after every accepted change; the last previously observed value is historical and will change after this documentation overlay.

## 2026-10-10 temporal topology increment

`D_RENDERER_TEMPORAL_SCHEDULE_PROPOSAL_CHECKPOINT_V1.md` is the next isolated preparation contract. It distinguishes existing Challenge phase semantics from the single continuous spans used by Visual Loops and Visual Drills. Timing values remain upstream-bound and uninstantiated. Do not use the older normalized-permille proposal as canonical geometry. This increment does not create a renderer baseline, output schedule, media or production authority.

## 2026-10-10 — Source-bound temporal preview (preparation only)

The topology-only temporal proposal is now complemented by `D_RENDERER_TEMPORAL_BOUND_PREVIEW_CHECKPOINT_V1.md`. The new contract produces in-memory half-open frame intervals from pinned representative sources: CHALLENGE_004 (`HOOK>GAME>REVEAL>CTA`, 900 frames at 60 FPS), geometric Visual Loop (60 frames at 30 FPS) and tracking Visual Drill (630 frames at 30 FPS). It checks the exact frame-count arithmetic, source lineage and fail-closed execution boundary. It does not create a video, renderer input, or output artifact; `D4.8=BLOCKED`, `release_authority=NONE`, D9 OPEN, D10 BLOCKED. Windows acceptance is pending. The next step is to bind this report to actual canonical D9.9/D9.10 request/payload results, then assemble an editorial review manifest for the first visual proof. Any real-media attempt remains gated by separately approved/frozen D renderer baseline plus explicit D4.8 authorization.

## Increment — D Renderer Editorial Review Manifest V1 (2026-10-10)

Added `D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1` to join D9.9 canonical editorial identity through the D9.10 bridge/adapter, candidate binding, logical composition, neutral frame program and a source-bound temporal reference. The manifest asserts exact editorial value parity and self-hashes the in-memory result while keeping proposed region targets unapproved and per-field frame windows unresolved.

The contract deliberately reports a known FPS mismatch: `CHALLENGE_004` timeline source is 60 FPS while `REVIEW_720` delivery metadata is 30 FPS. It does not resample. Visual Loop is family-level timing reference only; Visual Drill is type/tier timing reference only. No item is declared video-render-ready. The new focused test stays separate from the immutable 22-step aggregate until local acceptance and an explicitly reviewed integration change.

## Next renderer preparation increment — delivery timebase projection (2026-10-10)

`D_RENDERER_DELIVERY_TIMEBASE_PROJECTION_V1` introduces a source-pinned, in-memory proposal for cumulative frame-boundary projection from canonical source FPS to an explicit delivery-profile FPS. The representative `CHALLENGE_004`/`REVIEW_720` result is 900@60 FPS to 450@30 FPS with phase spans 90/210/90/60. The policy remains `PROPOSED_NOT_APPROVED`. It does not determine simulation frame samples, event-anchor mapping, interpolation, audio resampling, generated loop/drill payload identity, or field visibility windows. No renderer input or media is emitted; D4.8 BLOCKED and release authority NONE.


<!-- C11D_REQUEST_SCOPED_PAYLOAD_BINDING_V1_PLAN -->

## Request-scoped payload source binding â€” 2026-10-10

`tools/c11d/d9/d_renderer_request_scoped_payload_binding.py` now resolves the exact selection in the canonical D9.9 request against a pinned canonical source and audits the complete D9.9â†’D9.10â†’renderer-neutral review chain. V1 covers only `parking_v2/CHALLENGE_004`, `c11c_geometric_waves_v1/harmonic_membrane`, and `tracking/tier-2`, because the current temporal/editorial reference contracts are pinned to those examples. Other pairs fail closed.

Critical distinction: source resolution is not instance materialization. Challenge runtime payload remains absent; the Visual Loop family profile is not a grammar-specific instance; a Visual Drill type/tier example is not a request-generated instance. Payload instance ID/hash/path remain null and `video_render_ready=false`. Next required engineering item is a separately governed request-specific payload materializer that consumes the real seed/profile/selection and emits a hash-bound in-memory or approved review artifact without mutation of C11-C.

<!-- C11D_VISUAL_PAYLOAD_MATERIALIZATION_PREVIEW_V1 -->
## D9 visual payload materialization preview V1

D9 V1 now contains a headless, in-memory materialization harness for the exact Visual Loop `harmonic_membrane` and Visual Drill `tracking/tier-2` review fixtures using existing C11-C authoring APIs. It prints only hashes and frame/timing summaries, does not persist payloads or media, and leaves Challenge runtime output unresolved. `variation_index` is metadata-only in this V1. See `D_RENDERER_VISUAL_PAYLOAD_MATERIALIZATION_PREVIEW_CHECKPOINT_V1.md`.


<!-- C11D_CHALLENGE_RUNTIME_OUTPUT_PREVIEW_V1 -->
## D9 CHALLENGE_004 in-memory runtime output preview

The challenge runtime preview invokes the frozen `ChallengeRuntimeBridge.run_effective_pipeline` twice for source `CHALLENGE_004.json` and summarizes only in-memory runtime results. The SimulationResult is real runtime evidence, but is **not** a rendered/visual challenge payload; no image/video or renderer input is produced. See `D_RENDERER_CHALLENGE_RUNTIME_OUTPUT_PREVIEW_CHECKPOINT_V1.md`.

## Increment â€” D Renderer Profile Identity Separation V1 (2026-10-10)

The profile identity review separates four roles for CHALLENGE_004: legacy `video_profile=test_master_11s` (its named profile is 30 FPS / 11 seconds), canonical inline source timing (60 FPS / 15 seconds / 900 frames), explicit source `presentation.profile=social_default_v1`, and independent delivery `REVIEW_720` (30 FPS / 720Ã—1280). The legacy migration maps the top-level `video_profile` identifier into canonical presentation binding, so the frozen runtime reports `test_master_11s` as presentation profile even though the source also declares `social_default_v1`. D must bind presentation and delivery identity explicitly without modifying C11-C. The new in-memory rebind harness changes only a deep copy's presentation-profile identifier and verifies simulation-frame signature, winning frame, frame count and metrics remain unchanged. No renderer input or media is emitted; delivery timebase projection remains proposed/unapproved and D4.8 remains BLOCKED.

## Increment â€” Challenge Delivery Timeline Review V1 (2026-10-10)

The D review harness now joins actual frozen `CHALLENGE_004` runtime timing with the D-owned `social_default_v1` presentation bind and the still-proposed `REVIEW_720@30FPS` delivery projection. It checks repeated runtime determinism and simulation invariance, then derives source ranges `[0,180,600,780,900]` and delivery ranges `[0,90,300,390,450]`. Phase ranges are not text-visibility windows; those remain unresolved. No source simulation truth is mapped to delivery frames, no renderer input is emitted, and no media is created. The timebase proposal remains unapproved and D4.8 remains BLOCKED.
