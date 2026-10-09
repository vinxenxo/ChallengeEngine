# CURRENT AUTHORITATIVE UPDATE — region hierarchy reconciliation (2026-10-10)

Windows operator accepted `D_RENDERER_SEMANTIC_REGION_PROPOSAL_V1` as a proposal generator, not as approved geometry. The next source review clarified that D1.5 and the frozen presentation code already establish the 540×960 logical social `HEADER` / `BODY` / `FOOTER` frame and the distinct profile/family composition layers. The four normalized-permille boxes remain exploratory and must not drive a temporal schedule. The new increment `D_RENDERER_REGION_HIERARCHY_RECONCILIATION_V1` formalizes this source hierarchy and tests it read-only. **Windows verification of its focused test is pending.**

Apply `C11D_RENDERER_REGION_HIERARCHY_RECONCILIATION_OVERLAY_V1.zip` only after verifying the supplied SHA-256, then re-check the required C11-C manifest hash. Run the new focused hierarchy test, followed by the existing renderer region proposal test and the established parent checks. Keep the focused test outside the 22-step aggregate until Windows acceptance.

No timing schedule, pixels, renderer-native input or media are emitted by this increment. D9.10 stays `PREPARE_ONLY`; renderer OFF; media false; D4.8 BLOCKED; `release_authority=NONE`; D9 OPEN; D10 BLOCKED. Do not approve or freeze a renderer/C11-D baseline. The next design item after focused acceptance is a timing proposal derived from explicit supported duration contracts, with unknown durations left unknown.

---

# CURRENT AUTHORITATIVE UPDATE — Renderer-neutral frame program candidate (2026-10-10)

The operator confirmed the logical composition increment on Windows: `test_d_renderer_logical_composition.py` PASS (content types 3/3, determinism 3/3, editorial flow 3/3, negatives 17/17, structural schema 3/3; `jsonschema` not installed on Windows). The binding preview, D9.10 bridge, D9.13 lifecycle, candidate preflight and existing Suite also passed: bridge parity 3/3, adapter parity 3/3, bridge negatives 15/15, adapter negatives 9/9, lifecycle negative 14/14 and parity regression 4/4, candidate five blockers / `freeze_eligible=false`, Suite 22/22. D9.15 is canonically PASS/CLOSED (13/13).

The next isolated preparation increment adds `D_RENDERER_NEUTRAL_FRAME_PROGRAM_V1`: an in-memory, non-executable, renderer-neutral list of semantic text-binding declarations derived from the validated logical composition. It preserves exact editorial values and lineage but defines no frame schedule, duration, transitions or pixel coordinates. Semantic regions stay `PROPOSED_NOT_APPROVED`; this is not renderer input. Its focused test passes in the preparation workspace and now requires Windows verification.

Apply `C11D_RENDERER_NEUTRAL_FRAME_PROGRAM_OVERLAY_V1.zip` only after verifying its SHA-256 and the immutable C11-C manifest after extraction. Run the new focused frame-program test first, then logical composition, binding preview, bridge, D9.13 lifecycle, candidate preflight and aggregate Suite. Do not add the new test to the 22-step aggregate yet.

Governance remains unchanged: C11-C 2.19.12 and manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` immutable; D9.10 adapter `PREPARE_ONLY`; renderer OFF; no dispatch or media; D4.8 BLOCKED; `release_authority=NONE`; D9 OPEN; D10 BLOCKED. Renderer-baseline approval/freeze remain false, five candidate blockers remain, and the definitive GUI remains deferred.

---

# C11-D MASTER HANDOVER — D9.15 accepted; D9.14/D9.16 remain gated (2026-10-09)

## Latest operator-confirmed state — D9.15 checkpoint consumed; next work is renderer-baseline preparation (2026-10-09)

The Windows integration rerun after `C11D_D915_CHECKPOINT_CONSUMPTION_FIX_OVERLAY_V1.zip` is now confirmed. This block supersedes any older text below saying canonical D9.15 evidence is still required or the candidate-only waiver remains the current D9.15 status.

- `operator_evidence.py status`: `D9.15_OPERATOR_EVIDENCE_PASS_CLOSED`; 13/13 pass pairings, 0 blocked, 0 pending, 13 events; checkpoint `PASS_CLOSED`.
- D9.15 ledger SHA-256: `dda1c150ab18a7fbe0c4e531997b6f3d30fc121b58f22552762d53b79ed488fa`.
- D9.15 checkpoint SHA-256: `2e3b9d591288ba77259ee650685ba16deb12abcf770c123406612a5efbe309f5`.
- D9.15 static GUI preflight: PASS, capabilities 8/8, surfaces 5/5, negative 19/19; `operator_confirmation=REQUIRED` remains truthful for that static test because it must not infer human evidence.
- D9.14 gate: PASS as `BLOCKED_AS_REQUIRED`, cases 10/10, negative 20/20; renderer OFF, no media, D4.8 BLOCKED, release authority NONE.
- D9.16 preflight: PASS, static checks 5/5, evidence routes 9/9, negative 21/21; `D9.15_operator_evidence=PASS_CLOSED`; full acceptance remains `BLOCKED_AS_REQUIRED` due D9.14.
- Candidate preflight: PASS as a read-only audit; C11-C immutable reference match, protected entries 854/854, negative 22/22, legacy quarantine reconciled 4/4, canonical D9.15 `PASS_CLOSED`, five blockers retained, `freeze_eligible=false`.
- Last observed candidate tree fingerprint before this documentation-only update: 2,641 files; SHA-256 `b2970567cfe688653899a7e29cfecc36ae6224fdb8eb12386bf5a6a0e6caa331`.
- Aggregate `c11c-suite/self_test.py`: PASS 22/22.
- D9.10 Qt runtime / bound acceptance previously confirmed: PASS 3/3 and 7/7; D9.13 parity/lifecycle and bridge regressions pass.
- Historical C11-C manifest SHA-256 remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

Canonical D9.15 is no longer a candidate blocker. The old D9.15 waiver remains historical evidence only. The remaining five candidate blockers are D9.14 real-media certification, D9.16 full acceptance, D9.17 closure, D renderer-baseline approval, and exact-source D baseline approval.

## Next active engineering track — future D-owned renderer baseline (PREPARATION ONLY)

Do not run D9.14 real-media E2E or change activation policy yet. Start the D-owned renderer-baseline preparation track described in `D_RENDERER_BASELINE_PREPARATION_PLAN_V1.md`. The first deliverable is a separately versioned and hash-bound D renderer implementation/contract which can be reviewed and tested without dispatch. D9.10 stays PREPARE_ONLY; any future dispatcher must be a separately governed component and may not reinterpret the prepared envelope as renderer-native input.

The renderer baseline is not approved/frozen merely because its design or static tests pass. D9.14 requires both a separately approved/frozen future D renderer baseline and an explicit D4.8 governance checkpoint before authorized real-media tests. Neither approval is being created by this update. `D4.8=BLOCKED`, renderer OFF, production/media false, `release_authority=NONE`, D9 OPEN, D10 BLOCKED, C11-C immutable.


## Integration correction after D9.15 finalization — 2026-10-09

The operator has now rerun D9.15/D9.16/candidate preflights after the canonical checkpoint was sealed. The ledger is valid and D9.15 is `PASS_CLOSED`, but the old D9.16 and candidate code did not consume that checkpoint: D9.16 still reported `D9.15_operator_evidence=REQUIRED`, and candidate status still preferred the historical candidate-only waiver. This is a state-integration defect, not a failure of the 13 accepted observations.

A minimal integration overlay now makes D9.16 and candidate preflight validate `operator_evidence.py validate_acceptance_checkpoint()` against the live sealed ledger and each evidence file. A present but invalid/stale checkpoint fails closed and cannot fall back to the waiver. A valid canonical checkpoint supersedes the candidate-only waiver for status reporting and removes only the D9.15 evidence blocker from D9.16's dynamic blocker list. It does not change the D9.14 block, baseline approval requirements, freeze eligibility, renderer/media permissions or release authority.

The static D9.15 GUI preflight may still print `operator_confirmation=REQUIRED`: that command tests static surface/control readiness and is intentionally forbidden from inferring human evidence. The canonical operational closure is the separately sealed `D9_15_OPERATOR_ACCEPTANCE_CHECKPOINT.json` plus hash-bound ledger.

**Pending Windows confirmation for the integration overlay:** D9.16 should report `D9.15_operator_evidence=PASS_CLOSED` while `full_acceptance=BLOCKED_AS_REQUIRED`; the candidate should report `D9.15=D9.15_OPERATOR_EVIDENCE_PASS_CLOSED` with the five independent blockers retained and `freeze_eligible=false`; the aggregate Suite must accept either a valid canonical closure or the candidate-only waiver depending on the active tree. Do not close D9.14 or D9.16.


## Latest operator-confirmed state — authoritative

The operator has completed and finalized canonical D9.15 no-media GUI operational acceptance on the active Windows checkout. The `operator_evidence.py status` and `finalize` outputs are provided by the operator in this conversation.

- D9.15 recorder status before finalization: `recorded_pass_pairings=13/13`, `blocked_pairings=0`, `pending_pairings=0`, `events=13`, `complete=true`.
- Finalization: **`D9.15_OPERATOR_EVIDENCE_PASS_CLOSED`**.
- Sealed acceptance checkpoint: `docs/current/d/D9_15_OPERATOR_ACCEPTANCE_CHECKPOINT.json`.
- Checkpoint SHA-256: `2e3b9d591288ba77259ee650685ba16deb12abcf770c123406612a5efbe309f5`.
- Ledger SHA-256: `dda1c150ab18a7fbe0c4e531997b6f3d30fc121b58f22552762d53b79ed488fa`.
- D9.15 scope is only the no-media operational GUI matrix across Config, Producer, Test, Catalog and Maintenance. It grants no renderer, production, D4.8, D9.16, baseline-freeze or release authority.

## Latest verified D9.10/D9.13 acceptance

- D9.13 persisted parity contract: PASS, positive 1/1 and negative 4/4.
- D9.13 lifecycle: PASS; content types 3/3, stages 5/5, identity continuity PASS, GUI/CLI parity 3/3, catalog projection 3/3, maintenance audit 3/3, negative 14/14, persisted-parity regression 4/4.
- D9.10 bridge/adapter: PASS; content types 3/3, CLI bridge parity 3/3, adapter parity 3/3, bridge negatives 15/15, adapter negatives 9/9. Adapter remains `PREPARE_ONLY`.
- Direct Qt runtime `D910_QT_GUI_RUNTIME_FIX_02`: **PASS 3/3**; C11-C manifest match true.
- Combined capture `D910_QT_ACCEPTANCE_FIX_02`: **PASS 7/7**; `GUI_runtime_observed=false` is correct for offscreen automation, not an error.
- Aggregate suite: **PASS 22/22**.
- C11-C manifest SHA-256 remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

## Latest no-media gate results — 2026-10-09

- `test_gui_real_media_certification.py`: PASS, `gate=BLOCKED_AS_REQUIRED`, cases 10/10, negatives 20/20, renderer OFF, no media, D4.8 BLOCKED, release authority NONE.
- `test_full_acceptance.py`: PASS as preflight; static checks 5/5, evidence routes 9/9, negatives 21/21. Full D9.16 acceptance remains `BLOCKED_AS_REQUIRED` because D9.14 real-media acceptance is not authorized/available.
- Candidate preflight before D9.15 finalization: PASS, C11-C immutable reference match, protected entries 854/854, negatives 22/22, legacy reconciliation 4/4, five blockers, `freeze_eligible=false`; tree SHA-256 at that point was `877198711170beb4d57bbc8bd9bc610c5d76c60e36d6a9035b29c2cc500ee4d1`. Re-run after finalization; do not assume the blocker count remains unchanged.
- Aggregate suite before D9.15 finalization: PASS 22/22.

## Next active work — re-evaluate D9.16 and candidate after D9.15 closure

1. Verify the sealed D9.15 record with `python .\tools\c11d\baseline_candidate\operator_evidence.py status`.
2. Re-run `python .\tools\c11d\d9\test_gui_operational_acceptance.py` and `python .\tools\c11d\d9\test_full_acceptance.py`.
3. Re-run `python .\tools\c11d\baseline_candidate\test_d_baseline_candidate.py` and `python -u .\c11c-suite\self_test.py`.
4. Record their actual outputs and new candidate tree SHA-256. D9.15 is no longer pending, but do not assume that D9.16 or candidate blocker counts change until verified.

D9.14 full real-media GUI/E2E remains `BLOCKED_AS_REQUIRED` until a separately approved/frozen future D renderer baseline and an independent, explicit D4.8 governance checkpoint authorize the work. Do not run full production-media acceptance before those conditions exist.

## Governance boundary

- C11-C 2.19.12 and `release/C11C_FREEZE_PACKAGE_MANIFEST.json` remain immutable; manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- D9.10 adapter = `PREPARE_ONLY`; no renderer-native input or dispatch.
- D4.8 `BLOCKED`; renderer OFF; production/media OFF; `release_authority=NONE`.
- D9.15 canonical operational GUI matrix = PASS/CLOSED, checkpoint above.
- D9 remains OPEN; D9.14 full GUI/E2E, D9.16 full acceptance and D9.17 closure remain unresolved; D10 BLOCKED.
- Existing Producer window is test/operator GUI only. Definitive GUI work is deferred until all D acceptance gates are closed and the D baseline is frozen.

---

# C11-D MASTER HANDOVER — D9 Second-Stage Suite Integration

## Current status — updated 2026-10-09

**C11-C 2.19.12 remains immutable. D9 remains OPEN, D9.17 remains NO-GO, and D10 remains BLOCKED.**

D9.10 now connects the canonical D9.9 request/editorial/plan and bridge record to a versioned D-only adapter binding preview. The adapter is PREPARE_ONLY; it does not emit renderer input or dispatch production. Automated focused checks pass in the preparation workspace; Windows UI runtime for the new adapter tab is not claimed by the automation report.

D9.14 bounded qualification run `D914_COLON_FIX_20261009_E` passed on Windows and sealed four final A/V MP4s, eight checks, report SHA-256 `daa5e5676224d606e9d67ac7a7ed7e88c3c02a63c76ecdc579c3bc2dd320853f` and qualification-baseline SHA-256 `15343119f0f8338b13b47b0ea98546e5470d4a1a8895b65dbe1f41ee183e66d3`. This does not close full D9.14 GUI/E2E acceptance, activate general D rendering, authorize D4.8 or approve the final D baseline.

The existing Producer window is a **test/operator GUI only**. Work on the definitive GUI is deferred until all D acceptance gates are closed and the D baseline has been frozen. The 13 D9.15 screenshot/log requirement was waived for candidate-readiness only; do not infer canonical D9.15 PASS/CLOSED.

## Important correction of scope

D9 is not complete when the media pilot and backend tests pass. The roadmap requirement is to extend the existing `c11c-suite` surfaces so the D capabilities become fully operable and observable from GUI:

- `c11c-producer` — production, request, personalization, editorial configuration and later real D production;
- `c11c-catalog` — products, catalog identity, provenance and reproduction;
- `c11c-config` — contracts, profiles, snapshots and controlled editing;
- `c11c-maintenance` — cleanup, quarantine, organization and freeze;
- `c11c-test` — registration, QA, parity, GUI E2E and negative acceptance.

No new suite is allowed for this purpose.

The old `c11c-studio` experiment is retired and must not be revived.

## Completed D9 evidence

D9.1 real video: PASS.

D9.2 A/V: PASS.

D9.3 deterministic repeatability/negative: PASS.

D9.4 acceptance checkpoint: PASS/CLOSED.

D9.5.1 Producer 0.10.0 request/personalization GUI: implemented and Windows-validated.

D9.6 Catalog 0.2.0: implemented and Windows-validated.

D9.7 Config 0.2.0: overlay prepared; confirm Windows bring-up in the current working context before declaring it closed.

## Key product direction

The current Producer D tab is Challenge-centric because D4.3 originally defined Challenge editorial personalization. That is not the final D9 target.

The target is a **Universal Editorial Model** across:

- Challenge;
- Visual Loop families and grammar/subfamily variants;
- Visual Drill families/types/variants;
- Longform where the production contract supports it.

Editable editorial data must remain separate from derived telemetry, provenance and simulation truth.

## C11-C freeze boundary

Do not modify C11-C 2.19.12 simulation/mechanics/RNG/truth, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7/C9 contracts, logical 540×960 geometry or proven C11-C presentation/production behavior during this integration stage.

## D4/D6/D7/D8 governance locks

- `master_seed=NOT_ADOPTED`.
- gameplay seed = `request.seed`.
- music seed = `request.music_seed`.
- cross-domain sharing = `FORBIDDEN`.
- runtime derivation disabled.
- automatic seed generation disabled.
- D4.8 `BLOCKED`.
- `release_authority=NONE` unless an explicit future checkpoint changes it.

## D9.8–D9.10 completion record

- D9.8: PASS/CLOSED for the universal editorial model/resolver and its static contract tests.
- D9.9: PASS for the universal request/plan adapter and GUI/CLI parity; the operator confirms Windows GUI successfully generated plans for all currently implemented D content types.
- D9.9 Windows UTF-8 CLI defect: repaired; the operator reports the five focused/aggregate checks PASS.
- D9.9 GUI callback defect: repaired; the operator confirms Producer starts and generates plans without errors.
- D9.10 bridge planning: original 3-type bridge records, CLI parity 3/3, 15 negatives; subsequent addendum implemented D-only adapter envelope preparation, adapter parity 3/3 and adapter negatives 9/9. See the current `D9.10_EDITORIAL_TO_RENDER_BRIDGE_PLANNING_CHECKPOINT.md` and its superseded prior checkpoint in `docs/history/c11d/d9/`.
- D9.10 envelope remains inspection-only; no renderer-native input is emitted. C11-C 2.19.12 is immutable; D4.8 remains BLOCKED; release authority NONE.

## Next work

1. Run `python .\tools\c11d\d9\capture_d910_acceptance.py --run-id D910_WINDOWS_ACCEPTANCE_01` to create machine-verifiable JSON and per-command logs without screenshots.
2. Open the **test-only** Producer GUI, exercise one Challenge, one Visual Loop and one Visual Drill, and inspect the `D-ONLY RENDER ADAPTER (PREPARED / OFF)` tab. No screenshots are requested; report any runtime defect only.
3. Run the focused/aggregate tests listed in the D9.10 runbook and retain the automated report under `artifacts/tests/c11d_d9/d910_adapter_acceptance/`.
4. Complete the real editorial-to-render path only after the required D renderer baseline and separate dispatch authorization are eligible. The current adapter does not emit render input.
5. Advance D9.14 full GUI/E2E acceptance, D9.16, then D9.17 adjudication; only after all gates pass and explicit approvals may the final D baseline be frozen.
6. Keep definitive GUI implementation deferred until the D baseline is closed and frozen.

## New-context read order

1. `docs/current/d/C11-D_ROADMAP_V1.0_STATELESS.md`
2. `docs/current/d/C11-D_MILESTONES_APPROVED.md`
3. `docs/current/d/D9_UNIVERSAL_EDITORIAL_MODEL_V1.md`
4. `docs/current/d/D9_GUI_E2E_CERTIFICATION_PLAN_V1.md`
5. `docs/current/d/D9.4_ACCEPTANCE_CHECKPOINT.md`
6. `docs/current/suite/C11C_SUITE_CURRENT_RULES.md`
7. `docs/current/suite/C11C_SUITE_TOOLING_MATRIX.md`
8. `docs/current/d/START_PROMPT_C11D_CURRENT.md`

Do not use the D9.4 ZIP upload as the current working tree if later D9 overlays have already been applied locally.

## Parallel D baseline candidate track — 2026-10-09

The user has requested testing the integrated D branch as a future frozen-baseline candidate instead of treating C11-C as the active future-development baseline. This is a parallel **evaluation-only** track: C11-C 2.19.12 remains immutable and continues as the certified comparison reference. No C11-C source, renderer, mechanics, RNG, simulation truth or historical manifest is replaced.

Candidate: `C11-D-BASELINE-CANDIDATE-0.1`. Start with `docs/current/d/D_BASELINE_CANDIDATE_EVALUATION_V1.md`, `docs/current/d/D_BASELINE_CANDIDATE_TEST_MATRIX_V1.md`, and `python .\tools\c11d\baseline_candidate\test_d_baseline_candidate.py`. The test is registered in the existing Test 0.2.0 GUI as `D BASELINE CANDIDATE INTEGRITY PREFLIGHT (NO FREEZE)` and its policy is read-only in Config 0.2.0.

Expected current result: `PREFLIGHT_PASS_CANDIDATE_FREEZE_BLOCKED_AS_REQUIRED`. This confirms integrity/gate correctness and intentionally does not grant freeze eligibility. D9.14 real-media authorization/evidence, D9.15 five-surface operator evidence, D9.16 full acceptance, D9.17 closure, separate D renderer-baseline approval and the operator-controlled disposition of `c11d-control` remain blockers. `D4.8=BLOCKED`, renderer/media remain off and release authority remains `NONE`.

## Operator D9.15 capture waiver — candidate-only (2026-10-09)

Per explicit operator decision, do not require the 13 screenshot/log captures to continue **candidate-readiness evaluation**. The sealed checkpoint is `docs/current/d/D9.15_OPERATOR_EVIDENCE_WAIVER_CHECKPOINT.json`; the baseline candidate evaluator validates its seal and scope. Expected candidate output includes `D9.15=WAIVED_NOT_EVIDENCED_FOR_CANDIDATE_ONLY` and `blockers=5`, with `freeze_eligible=false`. Do not represent the waiver as captured evidence or D9.15 PASS/CLOSED. Canonical D9.15 remains operationally unclosed and D9.17 remains BLOCKED/NO-GO; D9.14 and D9.16 remain blocked, D4.8 remains BLOCKED, renderer/production remain OFF, media remains absent, and release authority remains NONE. C11-C 2.19.12 and its frozen manifest remain immutable.

## D9.10 + bounded D9.14 latest evidence (2026-10-09)

- New `C11D_RENDER_ADAPTER_BOUNDARY_D9_10_V1.json` is a read-only Config registry contract (Config now 30/30).
- D-only envelope is schema `C11-D-D9.10-D-ONLY-RENDER-ADAPTER-ENVELOPE-V1`; it preserves canonical request/plan/bridge/model hashes, editorial allowlist, explicit profiles/audio flag, and disjoint gameplay/music seed domains.
- Focused D9.10 result: content types 3/3, CLI bridge parity 3/3, adapter parity 3/3, bridge negatives 15/15, adapter negatives 9/9. Automated acceptance runner has five focused checks by default; the aggregate Suite is opt-in with `--include-aggregate` and records `operator_gui_runtime_observed=false`; the report is not an assertion of interactive GUI observation.
- Actual D9.14 bounded qualification: run `D914_COLON_FIX_20261009_E`, four final A/V MP4s, report SHA-256 `daa5e5676224d606e9d67ac7a7ed7e88c3c02a63c76ecdc579c3bc2dd320853f`, qualification baseline SHA-256 `15343119f0f8338b13b47b0ea98546e5470d4a1a8895b65dbe1f41ee183e66d3`.
- Current candidate preflight is expected to PASS as an audit but remain `freeze_eligible=false` with five blockers. D4.8 BLOCKED, renderer dispatch OFF, release authority NONE.


## D9.10 acceptance regression repair — 2026-10-09

The first Windows acceptance capture after the D9.10 adapter overlay showed 4/5 focused checks because the candidate preflight found two historical root README paths missing: `README_C11D_D9.5.1_OVERLAY.md` and `README_C11D_D9.6_CATALOG_INTEGRATION_OVERLAY.md`. The aggregate Suite then failed only when it reached that same candidate preflight. This is fixed by the additive restoration overlay `C11D_D9.10_ACCEPTANCE_README_RESTORE_FIX_OVERLAY_V1.zip`, which reinstates the two files byte-for-byte at their immutable manifest hashes. It does not change C11-C source or manifest.

Prepared-workspace revalidation: candidate preflight PASS (protected 854/854; negative 22/22; 34 allowlisted D changes; five blockers retained; `freeze_eligible=false`); default D9.10 acceptance PASS 5/5. `operator_gui_runtime_observed=false` is not a failed check; it records that the automated runner does not launch/observe an interactive Qt session. Do not require screenshots for those five backend/CLI/static-GUI checks. Windows needs to rerun the restored candidate, acceptance capture and aggregate suite. All governance locks remain unchanged.

## D9.10 next phase — offscreen Qt GUI runtime (2026-10-09)

The operator has restored both historical README files byte-for-byte, confirmed the candidate preflight PASS with five blockers retained, run D9.10 automated acceptance PASS 5/5 and aggregate Suite PASS 21/21. The next increment adds an opt-in offscreen Qt GUI runtime runner for the existing Producer test/operator GUI. It drives the D9.10 action for all three content types and audits editorial override propagation through canonical request, plan, bridge record and adapter envelope with exact CLI parity. No screenshots required.

**Next Windows command:**

```powershell
python .\tools\c11d\d9\test_d910_gui_runtime_acceptance.py --run-id D910_QT_GUI_RUNTIME_01
python .\tools\c11d\d9\capture_d910_acceptance.py --run-id D910_QT_ACCEPTANCE_01 --include-qt-gui-runtime --include-aggregate
python -u .\c11c-suite\self_test.py
```

The runtime test is a real Qt code path exercised offscreen, not a manual visual review; `operator_interactive_visual_observation=false` must remain truthful. PySide6 is not installed in the preparation environment, so no Qt runtime result has been claimed yet. The static harness contract is included in aggregate step 22/22. No media is created. Do not enable dispatch or attempt to consume the adapter envelope as renderer input; D4.8 remains BLOCKED, D9.14 full E2E/D9.16/D9.17 and final baseline approvals remain open, release authority NONE. The GUI remains test-only; the definitive GUI comes after final D baseline freeze.

---

# Latest authoritative update — D9.10 Qt runtime parity schema fix (2026-10-09)

This section supersedes older statements above that describe the Qt runtime as not yet diagnosed.

- The operator-provided diagnostic bundle SHA-256 is `c1b6cb2c76b4a3f8b8dade00e0dfda8adea0df0f4355f39e1d67e86a73556a81`.
- Confirmed exception: `RuntimeError: Qt GUI callback raised a modal warning for challenges: C11-D Editorial Universal: Persisted GUI/CLI parity receipt is not a complete PASS`.
- Root cause: current Producer GUI persists seven parity checks, including `d_only_adapter_envelope_equal`; D9.13 lifecycle validation expected exactly six. The valid current receipt was rejected fail-closed before a lifecycle receipt could be created. Qt font and `propagateSizeHints()` messages were incidental.
- Repair overlay updates `tools/c11d/d9/cross_suite_lifecycle.py` to require the current seven-check schema and bind the GUI/CLI/Producer adapter-envelope SHA-256 fields. `tools/c11d/d9/test_cross_suite_lifecycle.py` now generates a matching adapter parity fixture and covers one positive plus four focused negative receipt cases. No check was removed or loosened.
- Preparation-copy verification: Qt harness static contract PASS; Producer GUI static contract PASS; bridge/adapter content 3/3, CLI bridge parity 3/3, adapter parity 3/3, negatives 15/15 + 9/9; focused receipt regression positive 1/1 and negative 4/4; Config self-test 30/30 and negative 7/7.
- **Windows re-acceptance remains pending.** Do not claim runtime 3/3, combined acceptance 7/7 or aggregate 22/22 until the fresh runs report those results. Run the complete lifecycle test and the required commands in `docs/current/d/D9.10_QT_GUI_RUNTIME_ACCEPTANCE_CHECKPOINT.md` on the active Windows checkout. The clean archive copy lacks runtime-only D9.11 ledger/quarantine evidence, so its complete lifecycle test stops later at the existing maintenance guard; that guard was not weakened.
- Immutable boundaries remain: C11-C 2.19.12 and manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; adapter `PREPARE_ONLY`; D4.8 `BLOCKED`; renderer OFF; no Qt-test media; `release_authority=NONE`; D9 OPEN; D10 BLOCKED. The definitive GUI remains deferred until the full D baseline is accepted and frozen.
- Incident record: `docs/history/c11d/d9/D9.10_QT_GUI_RUNTIME_PARITY_SCHEMA_FIX_20261009.md`.

## 2026-10-10 — Renderer-neutral frame program accepted; semantic region proposal next

Operator-confirmed Windows results for `D_RENDERER_NEUTRAL_FRAME_PROGRAM_V1`: focused PASS, content types 3/3, determinism 3/3, editorial flow 3/3, negative 19/19, structural schema 3/3. Windows reports `jsonschema=NOT_INSTALLED`, so no claim of library-backed Draft 2020-12 validation is made for that run. Logical composition, binding preview, D9.10 bridge, D9.13 lifecycle, candidate preflight and C11-C Suite 22/22 all passed.

Next candidate increment: `D_RENDERER_SEMANTIC_REGION_PROPOSAL_V1`, a pure in-memory D-owned proposal for normalized-permille bounds of HEADER, CONTENT_STAGE, CHALLENGE_OVERLAY and FOOTER. All mappings/bounds remain `PROPOSED_NOT_APPROVED`; no pixel coordinates, frame schedule, renderer-native input, output path or media are emitted. Windows test is pending. Review checkpoint: `docs/current/d/D_RENDERER_SEMANTIC_REGION_PROPOSAL_CHECKPOINT_V1.md`.

Five candidate blockers remain; `freeze_eligible=false`. A real video/ D9.14 run is not yet authorized: a separately approved/frozen D renderer baseline and explicit D4.8 governance authorization are required. C11-C 2.19.12/manifest immutable; adapter PREPARE_ONLY; renderer OFF; media false; D4.8 BLOCKED; release authority NONE; D9 OPEN; D10 BLOCKED.

## Latest renderer preparation checkpoint — temporal topology (2026-10-10)

See `D_RENDERER_TEMPORAL_SCHEDULE_PROPOSAL_CHECKPOINT_V1.md`. This proposal is source-pinned to the frozen C11-C manifest and the existing timeline/runtime files. Challenges use the existing `HOOK → GAME → REVEAL → CTA` phase order. Visual Loops and Visual Drills use bound duration/FPS/frame-count payloads as continuous spans; Visual Drill subphases are not defined. No concrete schedule, durations, frame indices/ranges, renderer input or media are produced. D1.5 region hierarchy remains spatial authority; the normalized-permille proposal is not canonical. D9.10 stays `PREPARE_ONLY`, D4.8 remains BLOCKED, release authority NONE, D9 OPEN and D10 BLOCKED.


<!-- C11D_EDITORIAL_REVIEW_MANIFEST_V1_HANDOVER -->

## Latest D9 editorial-review increment (2026-10-10)

The editorial review manifest now audits the canonical D9.9â†’D9.10 chain against the temporal reference. Current focused test expected result: 3/3 content types, 3/3 determinism, 3/3 editorial chain, 3/3 temporal reference, 28/28 negative cases, 3/3 structural schema checks and 3/3 Draft 2020-12 schema checks when `jsonschema` is installed.

Known unresolved issues that must remain visible: CHALLENGE_004 source FPS 60 vs REVIEW_720 target FPS 30; Visual Loop family-level and Drill type/tier-level timing references do not yet bind the generated visual payload; editorial-field frame windows remain undefined. This manifest permits copy review only. It does not make a video render-ready.

Governance remains unchanged: C11-C frozen and immutable; renderer OFF; media_created=false; D4.8 BLOCKED; release authority NONE; D baseline approval/freeze and full acceptance still pending.
