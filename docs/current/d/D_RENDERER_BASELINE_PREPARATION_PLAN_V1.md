# C11-D Future Renderer Baseline Preparation Plan V1

**State:** `PREPARATION_ONLY_NOT_APPROVED_NOT_FROZEN`  
**Current candidate:** `C11-D-BASELINE-CANDIDATE-0.1`  
**Date:** 2026-10-09  
**Owner boundary:** C11-D only; C11-C 2.19.12 and its freeze manifest remain immutable.

## Latest incremental implementation — logical composition V1 (2026-10-10)

The operator-confirmed binding-preview increment has passed on Windows: logical inputs for Challenge/Loop/Drill are represented by a hash-bound preview; bridge and D9.13 tests pass; candidate preflight passes with five blockers; Suite remains 22/22. The next isolated preparation increment adds `D_RENDERER_CANDIDATE_LOGICAL_COMPOSITION_V1`: it places exact canonical editorial strings into logical `text_value` properties for semantic text elements.

The logical composition is in-memory review data only, not renderer-native input. The field-targets and regions remain `PROPOSED_NOT_APPROVED`; no renderer consumes this plan. Its preparation-copy focused test currently reports content types 3/3, determinism 3/3, editorial flow 3/3, negatives 17/17 and schema validation 3/3. **Windows verification of this new increment is pending.** See `D_RENDERER_CANDIDATE_LOGICAL_COMPOSITION_CHECKPOINT_V1.md`. Do not register it as an aggregate-suite step until Windows acceptance and separate review.

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
