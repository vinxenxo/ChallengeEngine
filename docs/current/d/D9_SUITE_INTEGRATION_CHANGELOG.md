# D9 Suite Integration — Change Log


## Renderer region hierarchy reconciliation V1 — preparation increment (2026-10-10)

- Reconciled the future D renderer layout model with the existing D1.5 540×960 logical social frame and the distinct profile-driven composition geometry in `PresentationProfile`.
- Preserved the five Visual Loop family identities/routing. The family catalog is not treated as a declaration of normalized family rectangles.
- Explicitly retained the prior normalized region proposal as unapproved exploratory data; it cannot drive timing, pixel coordinates or renderer dispatch. No invented fixed `CHALLENGE_OVERLAY` box is adopted.
- Added a strict output schema, read-only report builder and 21 negative controls; test is not registered in the aggregate and awaits Windows acceptance.
- No C11-C file/manifest mutation, renderer-native input, dispatch, activation, timing schedule or media. D4.8 remains BLOCKED; authority NONE.

## D renderer candidate logical composition V1 — preparation increment (2026-10-10)

- Added a D-owned versioned contract/schema and a pure in-memory logical-composition builder over the previously validated binding preview. Exact canonical editorial values map to semantic text-element `text_value` fields; locale is attached to all text elements and per-value SHA-256 values are recorded.
- Added 16 fail-closed regressions including tampered element values, re-sealed hashes, mapping self-promotion, unauthorized renderer input/activation/media/release claims, lineage mismatch, unknown fields/slots, Longform rejection, and attempted contract self-approval. Schema validation passed for all three supported content types in the preparation workspace.
- No aggregate-suite registration was added; existing Suite remains 22/22. The new focused test is pending operator Windows confirmation.
- This is not a renderer implementation that encodes frames; it creates no files/media and is not renderer-native input. Target mapping is still `PROPOSED_NOT_APPROVED`. Adapter remains `PREPARE_ONLY`; renderer OFF; D4.8 BLOCKED; release authority NONE.

## D9.15 sealed-checkpoint consumer integration — 2026-10-09

- Latest Windows outputs confirmed canonical D9.15 `PASS_CLOSED` (13/13 pairings) but exposed stale consumers: D9.16 still printed operator evidence REQUIRED and candidate preflight preferred the historical candidate-only waiver.
- Updated the candidate evaluator to validate the actual D9.15 checkpoint with the shared recorder, bind status to current ledger/evidence hashes, prefer canonical closure over the waiver, and fail closed for a present invalid/stale checkpoint.
- Updated D9.16 preflight to report D9.15 `PASS_CLOSED` only when the same canonical checkpoint validates; it removes only the satisfied D9.15 blocker from the dynamic full-acceptance blocker list. D9.14 remains BLOCKED and D9.16 full acceptance remains BLOCKED_AS_REQUIRED.
- Updated the aggregate Suite assertion/summary so it recognizes either canonical D9.15 closure or the earlier candidate-only waiver according to current sealed state; no governance control is bypassed.
- Added a regression that builds a ledger/checkpoint in a temporary isolated tree and rejects tampered checkpoint fields and changed evidence bytes.
- Preparation verification: Python compilation PASS; focused D9.16 test PASS in both no-checkpoint/REQUIRED and sealed-checkpoint/PASS_CLOSED scenarios; candidate test PASS in both waiver and canonical-closure scenarios. Full aggregate packaging-tree run was unable to pass the unrelated Maintenance step because the isolated source snapshot lacks the live D9.11 quarantine ledger; Windows checkout must rerun the listed tests.
- Candidate must remain `freeze_eligible=false`; D9.14 remains `BLOCKED_AS_REQUIRED`; renderer OFF; no media; D4.8 BLOCKED; release authority NONE; D9 OPEN; D10 BLOCKED.


## D9.15 canonical operator evidence PASS/CLOSED — 2026-10-09

- Operator ran `operator_evidence.py status`: 13/13 recorded PASS pairings, 0 blocked, 0 pending, 13 events, no media, release authority NONE.
- Operator ran `operator_evidence.py finalize --operator-attestation I_CONFIRM_ALL_D915_PAIRINGS_REVIEWED_NO_MEDIA` and received `D9.15_OPERATOR_EVIDENCE_PASS_CLOSED`.
- Sealed checkpoint `docs/current/d/D9_15_OPERATOR_ACCEPTANCE_CHECKPOINT.json`; checkpoint SHA-256 `2e3b9d591288ba77259ee650685ba16deb12abcf770c123406612a5efbe309f5`; ledger SHA-256 `dda1c150ab18a7fbe0c4e531997b6f3d30fc121b58f22552762d53b79ed488fa`.
- This supersedes the earlier candidate-only capture-waiver limitation for canonical D9.15 operator GUI acceptance. The waiver remains historical/candidate-scope documentation and is not used to fabricate evidence.
- Next action: re-run D9.15 focused preflight, D9.16 full-acceptance preflight, candidate preflight and aggregate Suite after the checkpoint. Do not assume updated blocker counts before observing output.
- D9.14 remains `BLOCKED_AS_REQUIRED` (Windows gate 10/10 cases, 20/20 negatives); D9.16 remains full-acceptance blocked pending the approved/frozen future D renderer baseline and explicit D4.8 authorization. Renderer OFF, no media, `release_authority=NONE`, D9 OPEN, D10 BLOCKED.
- C11-C manifest SHA-256 remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; adapter remains `PREPARE_ONLY`.

---

## D9.10 Qt runtime accepted; next gate D9.14 (2026-10-09)

- Confirmed direct Windows PySide6 offscreen acceptance `D910_QT_GUI_RUNTIME_FIX_02`: PASS 3/3.
- Confirmed combined D9.10 acceptance `D910_QT_ACCEPTANCE_FIX_02`: PASS 7/7, with `C11-C_manifest_match=true`, `qt_gui_runtime=PASS`, renderer OFF, media false and release authority NONE.
- Confirmed D9.13 lifecycle PASS: 3/3 content types, 5/5 stages, GUI/CLI parity 3/3, catalog projection 3/3, maintenance audit 3/3, negative 14/14, persisted parity regression 4/4.
- Confirmed aggregate Suite PASS 22/22 and baseline candidate preflight PASS with protected entries 854/854, negative 22/22, five blockers retained, `freeze_eligible=false` and `baseline_approval=MISSING`.
- Root cause was the mismatch between seven GUI parity checks and a six-check exact validator schema; fixed by making `d_only_adapter_envelope_equal` required with hash binding. No fail-closed, parity or governance assertions were removed.
- `GUI_runtime_observed=false` is accurate for automated offscreen execution. It is not a human visual-review claim and is not a failed check.
- Next active work is no-media verification of the D9.14 certification gate and D9.16 preflight. Full D9.14 remains blocked until a separately approved/frozen D renderer baseline and explicit D4.8 checkpoint. D9.15 waiver remains candidate-only; D9.17 NO-GO; D9 OPEN; D10 BLOCKED.
- C11-C manifest SHA remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; adapter `PREPARE_ONLY`; renderer OFF; no media; `release_authority=NONE`.


## D9.10 post-runtime integration follow-up — 2026-10-09

- Windows Qt runtime `D910_QT_GUI_RUNTIME_FIX_01` PASS 3/3 after the seven-key persisted-parity schema repair.
- D9.13 lifecycle PASS with 14/14 negative cases and persisted parity regression 4/4.
- Combined acceptance `D910_QT_ACCEPTANCE_FIX_01` remains FAIL 5/7: candidate preflight rejects an altered `docs/current/07_ROADMAP.md` outside approved D roots; aggregate Suite step 13 has a stale assertion for `negative=12/12`.
- Follow-up overlay restores the roadmap to the exact immutable manifest hash and synchronizes the aggregate assertion to `negative=14/14`, requiring `persisted_parity_regression=4/4` plus the governance fields. It does not change the manifest or weaken the candidate audit.
- Offscreen runtime does not claim human GUI observation, so `operator_gui_runtime_observed=false` remains correct. Re-run runtime and combined acceptance under fresh IDs; D9 remains OPEN until full gates pass.

## D9.5.1 — Producer 0.10.0

- Added a C11-D Production Request + Personalization tab to the existing `c11c-producer` GUI.
- Kept all current C11-C Producer screens and launchers; no new app/suite.
- Added toolkit-independent D9 helper for D4 request mapping, the existing delivery profile alias resolver, D4.6 planning, and D4.5 exact parity comparison.
- Added evidence output per unique request under `artifacts/tests/c11d_d9/producer_gui/`.
- Added 90-case core matrix, 12-case personalization matrix and four negative checks.
- Updated Producer/Suite current tests, manifests and active docs; C11-C backend fingerprint and schema version unchanged.
- Runtime authority NONE; D4.8 BLOCKED; this increment creates plans only, not media.
- Operator confirms the GUI request/plan tab opens and creates plans in Windows. The tab remains plan-only; actual D text-to-render integration is deferred until the future C11-D production baseline is frozen.

## D9.6 — Catalog 0.2.0 overlay

- Preserved the existing artifact browser and added a C11-D Products/Provenance tab inside `c11c-catalog`.
- Added explicit D7.3/D7.4 canonical-intent projection, D9.4 manifest/hash-backed validation pilot rows and D9.5.1 Producer GUI plan rows.
- Added canonical D4.5 plan replay command copy for persisted plan-only requests; copying is not execution.
- Added pure-standard-library data projection tests and a static GUI contract test; wired both into `c11c-suite/self_test.py`.
- Version target delivered: Catalog 0.2.0. Renderer/production execution remain false; release authority remains NONE.
- Operator confirms Catalog works in Windows. The D9.4-listed pilot media remains validation-only and is not release-eligible.

## D9.7 — Config 0.2.0 overlay prepared

- Extended the existing `c11c-config`; no new suite/application.
- Added read-only D2–D9 contract inspection, SHA-256 and invariants validation.
- Added explicit operator presets with profile validation, required independent seeds, diff/hash, explicit save, backup and validated restore.
- Added seven configuration/seed/path negatives, an executable generic-editor protected-root contract, and isolated save/backup/validated-restore lifecycle tests; wired these into consolidated Suite self-test.
- The generic editor protects all profiles and project/suite roots; only the dedicated allowlisted Operator Profiles tab can write operator profiles. No renderer/production/release authority; Windows GUI acceptance pending.


## D9.8 — Universal Editorial Model V1

- Registered the canonical editorial model and strict resolver across the supported Challenge, Visual Loop and Visual Drill identities; Longform remains explicitly disabled.
- Added live inventory coverage and 25 negative controls. Editable editorial content remains separate from derived telemetry, provenance, seed governance and simulation truth.
- Model checkpoint only; no renderer or production activation.

## D9.9 — Producer universal coverage / Windows GUI smoke check

- Producer 0.11.0 adds universal editorial selection, scoped editing, canonical request/plan output and GUI/CLI parity to the existing Producer.
- The operator applied the UTF-8 CLI fix and Qt scope-handler fix, ran the focused and aggregate tests successfully, and confirmed Windows GUI plan generation for all currently implemented D content types.
- Longform remains disabled; Loop/Drill stay editorial-intent plans. No physical renderer or release authority.

## D9.10 — Editorial-to-render bridge planning

- Added canonical contract `definitions/c11d/production/C11D_EDITORIAL_RENDER_BRIDGE_D9_10_V1.json` and the pure plan-only mapping builder `tools/c11d/d9/editorial_render_bridge.py`.
- Producer 0.11.1 exposes a read-only bridge-planning output tab in the existing universal editorial view. The canonical CLI emits the same bridge record; GUI/CLI parity includes the record and record hash.
- Tested Challenge/Loop/Drill route planning, 3/3 CLI process parity cases and 15 negative controls. Tests are registered in Producer and consolidated Suite self-tests.
- Each planning record includes SHA-256 identities for the canonical bridge contract and the D9.8 editorial model in addition to request/editorial/plan identity. The bridge emits no renderer input, invokes no renderer, creates no media, and has no output artifact path. D4.8 remains BLOCKED and `release_authority=NONE`.
- The operator should confirm the newly added D9.10 output tab launches and shows the bridge record in Windows before this GUI addition is considered interactively accepted.
- Config 0.2.0 registers the bridge contract read-only and validates the non-execution/governance locks; its registry contained 22 canonical contracts at D9.10; D9.11 adds the maintenance policy and brings it to 23. See `docs/current/d/D9.10_EDITORIAL_TO_RENDER_BRIDGE_PLANNING_CHECKPOINT.md`.


## D9.11 — Maintenance 0.2.0 implementation

- Added `D9_11_MAINTENANCE_POLICY_V1.json` and registered it read-only in Config (23/23 contracts).
- The existing Maintenance GUI calls `tools/c11d/d9/maintenance.py` for dry-run plan, documentation audit, freeze preflight, allowlisted reversible cleanup, quarantine/restore and recovery operations.
- Only `c11c-suite/c11d-control` is eligible for legacy quarantine. The operation is not performed when applying the overlay; it requires explicit GUI/CLI confirmation and records the original tree and historical manifest file references in an append-only ledger.
- The historical C11-C manifest is never rewritten. Cleanup has exactly two allowed transient roots and archives rather than permanently deleting. Freeze preflight never creates a release archive.
- Static backend, Maintenance GUI-contract, prior cleanup/organization and aggregated Suite tests pass. Windows Maintenance GUI/operator acceptance remains pending; D9 stays OPEN and D10 BLOCKED.

## D9.10 addendum — D-only render-adapter envelope (2026-10-09)

- Added `definitions/c11d/production/C11D_RENDER_ADAPTER_BOUNDARY_D9_10_V1.json` and `tools/c11d/d9/d_render_adapter.py`.
- Canonical request + allowlisted editorial + production plan + bridge record now map to a versioned, hash-bound binding-preview envelope for Challenge, Visual Loop and Visual Drill.
- CLI includes the envelope; the existing Producer test GUI shows a `D-ONLY RENDER ADAPTER (PREPARED / OFF)` view and writes per-request `d_render_adapter_envelope.json`; GUI/CLI compares envelope identity.
- Adapter-specific negatives cover forged hash/fields, activation/dispatch/media claims, C11-C mutation and seed-domain violations. Adapter preparation is enabled, but no renderer input is emitted and there is no dispatch control.
- Config registers the adapter boundary read-only; canonical registry validation is 30/30.
- `tools/c11d/d9/capture_d910_acceptance.py` automates report/log generation for backend, CLI and static GUI-contract checks. It does not require screenshots and does not claim interactive Qt launch.
- Preserve the earlier plan-only checkpoint at `docs/history/c11d/d9/D9.10_EDITORIAL_TO_RENDER_BRIDGE_PLANNING_CHECKPOINT_SUPERSEDED_20261009.md`.

## D9.14 addendum — bounded production qualification passed (2026-10-09)

- Operator run `D914_COLON_FIX_20261009_E` generated and audited four final A/V MP4 outputs; eight qualification checks passed.
- Report SHA-256 `daa5e5676224d606e9d67ac7a7ed7e88c3c02a63c76ecdc579c3bc2dd320853f`; qualification-only baseline SHA-256 `15343119f0f8338b13b47b0ea98546e5470d4a1a8895b65dbe1f41ee183e66d3`.
- Challenge D3 Music Engine V5 mux, deterministic same-seed Loop replay and changed-music-seed isolation passed.
- This is qualification-only using proven generators; full D9.14 GUI/E2E remains blocked, D4.8 is BLOCKED, general D renderer dispatch remains OFF, D9.16/D9.17 remain blocked and release authority is NONE.


## D9.10 acceptance readme restoration fix (2026-10-09)

- Restored the two historical root README files exactly as specified by the immutable C11-C source manifest after a candidate preflight found them absent in the active checkout.
- This was a repository-inventory defect. No C11-C manifest rewrite, protected-code change, D adapter dispatch or renderer activation was performed.
- Prepared-workspace validation: candidate preflight PASS; 854/854 protected entries; 22/22 negative controls; five candidate blockers retained; freeze eligibility false. Automated D9.10 acceptance returns 5/5 with the default five focused checks.
- `operator_gui_runtime_observed=false` remains an accurate scope annotation, not an acceptance failure. Backend/CLI/static GUI checks need no screenshots. This does not claim the live GUI was launched by the acceptance runner.
- See `docs/history/c11d/d9/D9.10_ACCEPTANCE_README_MANIFEST_REPAIR_20261009.md`.

## D9.10.2 — automated offscreen GUI runtime harness (2026-10-09)

- Added `tools/c11d/d9/test_d910_gui_runtime_acceptance.py` to exercise the actual PySide6 Producer test/operator GUI offscreen for Challenge, Visual Loop and Visual Drill. The test clicks the existing D9.10 planning action and validates the generated canonical request, editorial resolution, plan, bridge record, adapter envelope, lifecycle receipt and separate-process GUI/CLI parity.
- Every type carries an explicit editorial title override; the test requires that value to arrive in the allowlisted adapter binding preview and verifies the envelope hash and all prepare-only/governance locks.
- Added a dependency-free static guard `test_d910_gui_runtime_contract.py` as aggregate Suite check 22/22. Extended `capture_d910_acceptance.py` with opt-in `--include-qt-gui-runtime`, which records the offscreen run in per-check logs and binds its result into the hash-bound acceptance report. No screenshots required.
- Windows runtime acceptance is pending; PySide6 is unavailable in the package-preparation environment. The static contract and aggregate suite can be validated here, but no runtime PASS is claimed.
- No renderer-native input, renderer dispatch, media production, release authority or definitive GUI work is introduced. C11-C remains immutable; D4.8 BLOCKED, D9 remains OPEN, and D10 remains BLOCKED.

## D9.10 Qt GUI runtime — persisted parity schema correction (2026-10-09)

- Inspected the operator's diagnostic bundle (`C11D_D910_QT_RUNTIME_DIAGNOSTICS_20261009_202637.zip`, SHA-256 `c1b6cb2c76b4a3f8b8dade00e0dfda8adea0df0f4355f39e1d67e86a73556a81`). The actual exception was `Persisted GUI/CLI parity receipt is not a complete PASS`, raised while the Producer GUI callback requested the D9.13 lifecycle receipt.
- Root cause: the live D9.10 Producer GUI records seven parity checks, while the D9.13 lifecycle validator hard-coded an exact six-check set. The GUI's valid `d_only_adapter_envelope_equal` check caused a deterministic fail-closed rejection.
- Corrected the required schema to include adapter-envelope parity, with SHA-256 binding across GUI, CLI and Producer receipt. The validator remains exact-schema and fail-closed.
- Updated the lifecycle fixture to use the canonical D-only adapter/CLI envelope and added positive and negative persisted-parity regression coverage.
- Preparation-copy checks pass for the static Qt harness contract, Producer GUI contract, bridge/adapter 3/3, bridge negatives 15/15, adapter negatives 9/9, focused parity receipt regression positive 1/1 + negative 4/4, and Config self-test 30/30 with negatives 7/7.
- Windows Qt runtime has **not yet been re-run**. The expected runtime 3/3, combined acceptance 7/7 and aggregate Suite 22/22 are targets, not asserted results. The full lifecycle test in the clean source-archive copy stopped later at the maintenance-plan guard because archive packaging excludes the working D9.11 ledger/quarantine evidence; the check was not weakened.
- Governance unchanged: C11-C 2.19.12/manifest immutable; D9.10 adapter `PREPARE_ONLY`; D4.8 BLOCKED; renderer OFF; media false; `release_authority=NONE`; D9 OPEN; D10 BLOCKED.
- Incident detail: `docs/history/c11d/d9/D9.10_QT_GUI_RUNTIME_PARITY_SCHEMA_FIX_20261009.md`.


## D9.14 / D9.16 no-media gate verification — Windows (2026-10-09)

- `test_gui_real_media_certification.py`: PASS, gate `BLOCKED_AS_REQUIRED`, cases 10/10 and negatives 20/20. Renderer OFF, media false, D4.8 BLOCKED, release authority NONE.
- `test_full_acceptance.py`: PASS, static checks 5/5, evidence routes 9/9, negatives 21/21; full acceptance remains `BLOCKED_AS_REQUIRED`, D9.14 BLOCKED and canonical D9.15 operator evidence REQUIRED.
- Candidate preflight: PASS, C11-C immutable reference match; protected entries 854/854; negative 22/22; legacy reconciliation 4/4; five blockers; `freeze_eligible=false`; `baseline_approval=MISSING`. Observed tree SHA-256 `877198711170beb4d57bbc8bd9bc610c5d76c60e36d6a9035b29c2cc500ee4d1`.
- Aggregate Suite: PASS 22/22. D9.10 Qt runtime remains PASS 3/3 and bound acceptance PASS 7/7.
- Next actionable no-media work: capture and seal canonical D9.15 operator evidence, all 13 pairings across the five existing GUIs. Candidate-only waiver does not substitute.
- These gate passes are not real-media acceptance or D9 closure. D9.14 full GUI/E2E remains blocked by the absent separately approved/frozen universal D renderer baseline and explicit D4.8 governance checkpoint. D9.16 and D9.17 remain blocked; D10 blocked; renderer OFF; release authority NONE.


## 2026-10-09 — Canonical D9.15 checkpoint consumed; D renderer baseline is next

Windows confirmation after the checkpoint-consumption overlay:

- D9.15 recorder status `PASS_CLOSED`, 13/13 pairings, checkpoint SHA-256 `2e3b9d591288ba77259ee650685ba16deb12abcf770c123406612a5efbe309f5`, ledger SHA-256 `dda1c150ab18a7fbe0c4e531997b6f3d30fc121b58f22552762d53b79ed488fa`.
- D9.15 static preflight 8/8 capabilities, 5/5 surfaces, negative 19/19; operator confirmation remains required in that static route by design.
- D9.14 gate PASS as `BLOCKED_AS_REQUIRED`, 10/10 cases and 20/20 negatives.
- D9.16 preflight PASS with 5/5 static checks, 9/9 evidence routes, 21/21 negatives, canonical D9.15 `PASS_CLOSED`, and full acceptance still `BLOCKED_AS_REQUIRED`.
- Candidate preflight PASS; protected entries 854/854, negative 22/22, legacy reconciliation 4/4, canonical D9.15 PASS_CLOSED, five blockers and `freeze_eligible=false`.
- Aggregate Suite PASS 22/22.

The prior D9.15 candidate-only waiver is superseded for live operational status by the canonical checkpoint. No renderer, production, media, freeze or release authority was granted. The next approved engineering activity is preparation and static verification of a separately versioned D-owned renderer baseline candidate, per `D_RENDERER_BASELINE_PREPARATION_PLAN_V1.md`; real-media D9.14 remains forbidden until independent renderer-baseline approval and explicit D4.8 governance authorization exist.


## 2026-10-10 — Renderer-neutral frame program candidate V1 (preparation)

- Added `D_RENDERER_NEUTRAL_FRAME_PROGRAM_V1` contract/schema and an in-memory builder that projects the accepted logical composition into ordered semantic text-binding declarations.
- The candidate preserves direct editorial values and hash lineage; region mappings remain `PROPOSED_NOT_APPROVED`; no frame schedule, pixel coordinates, transitions, output path or executable renderer command is emitted.
- Preparation workspace focused verification: content types 3/3, determinism 3/3, editorial flow 3/3, negative 19/19, schema 3/3, full JSON Schema 3/3; Python compile PASS. Windows verification of this increment is pending.
- The prior logical-composition increment is now operator-confirmed Windows PASS (content 3/3, determinism 3/3, editorial flow 3/3, negative 17/17, structural schema 3/3; optional `jsonschema` absent on Windows). Existing aggregate remains 22/22; frame program is not yet registered there.
- C11-C/manifest unchanged; adapter `PREPARE_ONLY`; renderer OFF; no media; D4.8 BLOCKED; release authority NONE; D9 OPEN; D10 BLOCKED.


## D Renderer Semantic Region Proposal V1 — 2026-10-10

- Operator-confirmed Windows acceptance of the preceding neutral frame program: content types 3/3, determinism 3/3, editorial flow 3/3, negatives 19/19, structural schema 3/3. Windows lacks the optional `jsonschema` library; no full library-backed validation claim is made for that run.
- Added the strict D-owned `D_RENDERER_SEMANTIC_REGION_PROPOSAL_V1` contract/schema and in-memory builder/validator. Proposed normalized-permille bounds cover HEADER, CONTENT_STAGE, CHALLENGE_OVERLAY and FOOTER; all remain `PROPOSED_NOT_APPROVED`. Source lineage to frame program retained.
- The proposal/test does not define timing, emit pixel coordinates/renderer-native input, dispatch, activate, or produce media. Focused Windows acceptance pending; keep separate from 22-step aggregate until reviewed.
- Video remains gated: independent renderer-baseline approval/freeze plus explicit D4.8 authorization are required before governed D9.14 real-media execution. C11-C immutable, adapter PREPARE_ONLY, renderer OFF, media false, release authority NONE.

## 2026-10-10 — Renderer temporal topology proposal V1

Added the D-only source-pinned temporal topology proposal and focused test. The proposal models existing Challenge phases and continuous Visual Loop/Visual Drill spans without emitting request-specific durations or frame indices. It consumes D1.5 region-hierarchy reconciliation and rejects canonicalization of the prior normalized-permille rectangles. The new focused test remains separate from the aggregate 22-step Suite pending Windows operator acceptance. No media, renderer activation, or authority change.

## D9 — Source-bound temporal preview (2026-10-10; separate focused test)

- Added `D_RENDERER_TEMPORAL_BOUND_PREVIEW_V1` to bind the existing topology proposal to three pinned canonical timing sources without engine/render execution.
- Focused test: `python .\tools\c11d\d9\test_d_renderer_temporal_bound_preview.py`.
- Not added to the 22-step aggregate yet; keep the increment isolated until Windows acceptance and explicit suite-integration review.
- Frame ranges are review-only data, not renderer-native input. No media, output path, C11-C mutation, D4.8 grant or release authority.

## D9 — Source-bound temporal preview (2026-10-10; separate focused test)

- Added `D_RENDERER_TEMPORAL_BOUND_PREVIEW_V1` to bind the existing topology proposal to three pinned canonical timing sources without engine/render execution.
- Focused test: `python .\tools\c11d\d9\test_d_renderer_temporal_bound_preview.py`.
- Not added to the 22-step aggregate yet; keep the increment isolated until Windows acceptance and explicit suite-integration review.
- Frame ranges are review-only data, not renderer-native input. No media, output path, C11-C mutation, D4.8 grant or release authority.

## D9 — Source-bound temporal preview (2026-10-10; separate focused test)

- Added `D_RENDERER_TEMPORAL_BOUND_PREVIEW_V1` to bind the existing topology proposal to three pinned canonical timing sources without engine/render execution.
- Focused test: `python .\tools\c11d\d9\test_d_renderer_temporal_bound_preview.py`.
- Not added to the 22-step aggregate yet; keep the increment isolated until Windows acceptance and explicit suite-integration review.
- Frame ranges are review-only data, not renderer-native input. No media, output path, C11-C mutation, D4.8 grant or release authority.
