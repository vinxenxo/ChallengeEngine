**Current authoritative phase (2026-10-09): D9.10 runtime PASS 3/3; bound acceptance PASS 7/7; aggregate Suite PASS 22/22; D9.15 canonical operator GUI acceptance PASS/CLOSED (13/13 pairings).** D9.14 gate remains `BLOCKED_AS_REQUIRED`; D9.16 is a passing preflight only and full acceptance remains blocked; D9 remains OPEN. The D9.15 checkpoint is sealed at SHA-256 `2e3b9d591288ba77259ee650685ba16deb12abcf770c123406612a5efbe309f`, bound to ledger SHA-256 `dda1c150ab18a7fbe0c4e531997b6f3d30fc121b58f22552762d53b79ed488fa`. Next safe action: re-run D9.15/D9.16/candidate preflights against this checkpoint and record actual current outputs. Full D9.14 remains blocked until a separately approved/frozen universal D renderer baseline and explicit `D4.8` governance authorization exist. D9.17 remains `BLOCKED/NO-GO`; D10 remains BLOCKED.

## D9.15 checkpoint-consumption integration fix — 2026-10-09

The canonical D9.15 evidence ledger/checkpoint is now sealed PASS/CLOSED (13/13, no blocked or pending pairings). The latest operator preflights showed that the old consumers were stale: D9.16 still returned `D9.15_operator_evidence=REQUIRED` and candidate preflight still used the candidate-only waiver status. The next safe action is to apply the integration correction that validates the current D9.15 checkpoint and ledger in both consumers. A valid closure removes only the D9.15 evidence requirement from D9.16's dynamic blocker list and sets the candidate D9.15 gate to canonical PASS/CLOSED; a present invalid/stale checkpoint is a hard failure. The candidate still has five independent blockers and is not freeze-eligible. D9.14, D4.8, renderer and release authority remain blocked.


# Challenge Engine V1.0 STATELESS — C11-D Roadmap

**Governance boundary remains unchanged:** C11-C 2.19.12 and its manifest are immutable; adapter `PREPARE_ONLY`; renderer OFF; no media; `D4.8=BLOCKED`; `release_authority=NONE`. The definitive GUI remains deferred until the complete D baseline is accepted and frozen.

## Governing baseline

C11-C remains an immutable certified reference:

`ChallengeEngineV01_STATELESS_C11-C_2.19.12_FROZEN_20260930_175709.zip`

- ZIP SHA-256: `D85425CF18C5211C8497574F4FC66202D613EACC0EC14CD4E2FEF0B24F634A32`
- Tree SHA-256: `2D39B7B923B42CDC6647A4D25493B75023CDD19CEE18214BBDE1FDD295B8F256`

D7.5 remains the frozen D governance baseline used to open D8/D9:

`ChallengeEngineV01_STATELESS_C11-D_7.5_V8_FROZEN_20261008_111052.zip`

SHA-256: `396d9f4bfdbb44b4878acf06db8d6c1c385103c110de537a174632e93611cd1d`

The user's later local working tree contains the post-D7.5 D8/D9 implementation and must be treated as the current development state. **Do not roll back to the D9.4 upload or any older ZIP merely because it is easier to locate.**

## Non-negotiable governance

- `master_seed=NOT_ADOPTED`.
- Gameplay seed = `request.seed`.
- Music seed = `request.music_seed`.
- Cross-domain seed sharing = `FORBIDDEN`.
- Runtime derivation = disabled.
- Automatic seed generation = disabled.
- `D4.8 = BLOCKED` until a separately authorized future checkpoint changes it.
- `runtime_authority = NONE` unless explicitly elevated by a future contract.
- GUI and CLI are co-equal operator surfaces over the same canonical backend commands.
- No C11-C simulation/mechanics/RNG/truth refactor.
- No change to `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7/C9 contracts or logical 540×960 geometry during the current D9 integration stage.

## D9 purpose — corrected interpretation

D9 is **Suite integration/evolution**, not merely another test phase. The roadmap requirement is to extend the existing operator surfaces:

- `c11c-test` → validation, QA and acceptance (0.2.0: D2–D9 routes, negative controls, GUI/CLI parity and real-media certification preflight).
- `c11c-producer` → production, review and job orchestration;
- `c11c-maintenance` → cleanup, organization, quarantine and freeze operations;
- `c11c-catalog` → catalog, products, provenance and reproducibility;
- `c11c-config` → configuration, profiles, snapshots and controlled editing.

No sixth operational suite is to be created. Historical `c11c-studio` material is archived context only and is **not an implementation dependency or target architecture**.

## Completed D milestones

- D0–D7.5: PASS/CLOSED; D7 FROZEN.
- D8.0–D8.7: PASS/CLOSED; media state remains governed separately from release authority.
- D9.0: real-media preflight PASS.
- D9.1: first physical Challenge video pilot PASS.
- D9.2: audio-enabled A/V pilot PASS.
- D9.3: deterministic A/V repeat + negative control PASS.
- D9.4: acceptance checkpoint PASS/CLOSED.
- D9.5.1: existing `c11c-producer` extended with D4 Request/Personalization planning surface. Producer version at D9.5.1: **0.10.0**. Windows GUI bring-up passed for that checkpoint; D9.9 expanded the same application to Producer 0.11.0; the additive D9.10 bridge-planning view is Producer 0.11.1.
- D9.6: existing `c11c-catalog` extended with D branch product/provenance/reproduction view. Catalog target/version: **0.2.0**. Windows GUI bring-up passed in the current working tree.
- D9.7: existing `c11c-config` extended with D contracts and controlled operator profiles. Config target/version: **0.2.0**. Overlay is prepared; Windows bring-up is pending explicit confirmation if not yet executed in the current context.

## D9 second-stage roadmap

### D9.8 — Universal editorial model

**Implementation status: PASS — canonical declarative model, strict resolver, live inventory and 25 negative tests. D9.8 is a closed model checkpoint only; it does not close D9.**

Create one declarative editorial model spanning the content system rather than a Challenge-only personalization surface.

Coverage:

- Challenge;
- Visual Loop;
- Visual Drill;
- Longform;
- family;
- subfamily / grammar / drill type;
- individual production override.

The model must distinguish editable editorial fields from derived telemetry, provenance and simulation truth.

### D9.9 — Producer universal editorial coverage

Extend the **existing `c11c-producer`** (Producer 0.11.0 at D9.9; 0.11.1 with D9.10 additive bridge planning) with the universal editorial tab: content type → family → subfamily/grammar/variant, editable scoped editorial fields, canonical request/plan output and reproducibility evidence. Both GUI and CLI use `tools/c11d/d9/universal_producer.py`; Challenge delegates to the existing D4 request/plan adapter, while Loop/Drill produce only a deterministic editorial-intent plan until the future D renderer baseline.

Required tests:

- all supported content types;
- all current families;
- all current subfamilies/grammars where represented;
- validation and normalization;
- GUI/CLI canonical plan parity;
- unsupported-field negatives;
- unchanged gameplay/music seeds.

**Implementation status: PASS (plan-only scope).** The inventory matrix resolves all 9 Challenge IDs, 27 concrete Loop grammars plus five family-level `auto` selectors, and 20 Drill type/tier variants. Separate CLI-process parity is certified for Challenge, Loop and Drill; 21 negative controls pass. Renderer/production remain off, `release_authority=NONE`, and the operator has now confirmed Windows GUI plan generation for all currently implemented D types without errors. This does not constitute real-media GUI acceptance or close D9.

### D9.10 — Editorial-to-render bridge + D-only adapter envelope

**Implementation status: PREPARE-ONLY IMPLEMENTED.** The canonical contract `definitions/c11d/production/C11D_EDITORIAL_RENDER_BRIDGE_D9_10_V1.json` validates the bridge mapping; the new `definitions/c11d/production/C11D_RENDER_ADAPTER_BOUNDARY_D9_10_V1.json` defines the D-only adapter boundary. `tools/c11d/d9/d_render_adapter.py` consumes the canonical D9.9 request/editorial/plan and D9.10 bridge record and emits a hash-bound binding-preview envelope for Challenge, Visual Loop and Visual Drill.

Prepared-workspace acceptance: three supported types 3/3; bridge CLI parity 3/3; adapter-envelope parity 3/3; bridge/governance negatives 15/15; adapter-specific negatives 9/9. The existing Producer test GUI exposes `D-ONLY RENDER ADAPTER (PREPARED / OFF)` and persists `d_render_adapter_envelope.json`; its CLI parity is checked through a separate process. Config registers the boundary read-only and validates 30/30 canonical contracts.

The preview is **not renderer-native input**. The adapter may prepare the binding envelope but must not invoke a renderer, emit renderer input, create media, or authorize production. `renderer_dispatch_enabled=false`, `renderer_activation=false`, `D4.8=BLOCKED`, and `release_authority=NONE` are invariant. Definitive GUI work is deferred until the D branch has completed acceptance and the final D baseline is frozen; the current Producer remains a test/operator GUI.

Focused validation: `python .\tools\c11d\d9\test_editorial_render_bridge.py`. No screenshots are required for automated D9.10 contract acceptance. Run `python .\tools\c11d\d9\capture_d910_acceptance.py --run-id D910_ACCEPTANCE_RUN` to create the hash-bound JSON report and per-check logs; the report explicitly does not claim the Qt window was interactively observed.

### D9.11 — Maintenance integration

Implementation status: **PASS/CLOSED — Maintenance 0.2.0 backend and full Suite regression PASS; the operator confirmed the Windows Maintenance GUI opens, and `test_maintenance.py`, Maintenance self-test and Suite self-test all pass after restoring the original read-only C11-C manifest byte-for-byte.** The implementation stays inside the existing `c11c-maintenance` surface and delegates GUI/CLI operations to `tools/c11d/d9/maintenance.py`.

Expose and test:

- dry-run;
- repository organization;
- cleanup allowlists;
- quarantine;
- conflict handling;
- documentation consolidation;
- freeze preparation;
- protected-root enforcement.

The canonical policy `definitions/c11d/d9/D9_11_MAINTENANCE_POLICY_V1.json` is exposed read-only in Config. Cleanup has a two-root allowlist and archives reversibly instead of permanently deleting. The unregistered `c11c-suite/c11d-control` path can only be quarantined/restored by explicit operator confirmation; its legacy manifest references are recorded in an append-only ledger while `release/C11C_FREEZE_PACKAGE_MANIFEST.json` remains byte-for-byte unchanged. Freeze preflight is read-only, creates no archive and grants no authority.

Focused validation: `python .\tools\c11d\d9\test_maintenance.py`. Windows bring-up and operator review of the preview actions remain required.

### D9.12 — Test integration

Implementation status: **IMPLEMENTED — Test 0.2.0 route registry, negative/parity bundles and GUI E2E certification preflight are integrated; static contract acceptance is available, and Windows GUI bring-up remains an operator check.**

Upgrade existing `c11c-test` to target **0.2.0**.

Register D2–D9 contracts and GUI integration tests without duplicating the canonical backend. Test must provide explicit routes for:

- D request/personalization;
- seed governance;
- catalog/provenance;
- media QA;
- negative controls;
- GUI/CLI parity;
- real-media GUI certification.

### D9.13 — Cross-suite lifecycle

Implementation status: **BACKEND/STATIC PASS — canonical receipt builder/validator, five-surface lifecycle test and aggregated regression PASS; Windows GUI receipt/audit confirmation remains an operator check.**

The shared `tools/c11d/d9/cross_suite_lifecycle.py` adapter proves that the same production intent survives:

`Config → Producer → Test/QA → Catalog → Maintenance`

with one SHA-256 sealed `lifecycle_id`, `identity_sha256` and `binding_sha256`, and no suite-specific reinterpretation of seeds, profiles or editorial payload. The test replays the persisted request/plan/bridge through canonical backends, checks separate CLI-process parity for Challenge/Loop/Drill, validates Catalog's non-authoritative intent projection, and runs Maintenance's read-only audit. It covers 12 negative cases. Longform remains unsupported; no media or release artifact is created.

### D9.14 — Real GUI production certification

**Current implementation status: GATE/PREFLIGHT PASS; REAL-MEDIA CERTIFICATION BLOCKED.** The existing Producer now exposes the D9.14 certification gate and `c11c-test` registers the same canonical test. The preflight seals the state and lists the ten required cases, but never starts production. The future D renderer baseline is not present/authorized and D4.8 remains BLOCKED; therefore no real-media case is claimed or executed by this checkpoint.

Do not bypass this blocker using the frozen C11-C renderer or by invoking legacy media scripts from the new universal editorial GUI. A future approved D frozen baseline and an explicit governance checkpoint must first version/hash the renderer adapter, authorize D4.8, pass seed/editorial determinism and media provenance/QA gates, and approve real-media Windows E2E. No local file or GUI toggle can confer that authority.

Run the gate with `python .\tools\c11d\d9\test_gui_real_media_certification.py`. The expected gate status is `BLOCKED`, while the gate test itself is PASS only if it remains blocked and creates no media.

Required end-to-end cases after those gates are authorized:

Minimum end-to-end set:

1. Challenge personalised video.
2. Visual Loop personalised video.
3. Visual Drill personalised video.
4. Longform personalised video where supported by the D production contract.
5. Same configuration repeated → deterministic reproduction.
6. Changed music seed → changed audio/product identity.
7. Changed editorial text → changed editorial identity/output.
8. Invalid request → blocked.
9. Protected-root mutation → blocked.
10. Release mutation without authority → blocked.

### D9.15 — GUI operational acceptance

**Current implementation status: PREFLIGHT PASS; OPERATOR GUI ACCEPTANCE REQUIRED.** `tools/c11d/d9/gui_operational_acceptance.py` validates the eight operational capabilities across exactly the five canonical surfaces. `c11c-test` registers the same canonical preflight; Config registers its policy as read-only. A passing preflight is not operational acceptance: the operator must inspect and execute the specified no-media actions in Windows and capture evidence.

Eight operational capabilities: (1) Config contracts/profiles/validate/hash/backup/restore; (2) Producer universal Challenge/Loop/Drill planning, D9.10 bridge, D9.13 lifecycle and D9.14 blocked gate; (3) Test validation/preflight/logging; (4) Catalog identity; (5) provenance/hashes; (6) process logs; (7) Maintenance read-only/dry-run operations; (8) reproduction and lifecycle identity continuity. D9.14 real-media execution remains blocked; this checkpoint must not claim real-media acceptance.

Run `python .\tools\c11d\d9\test_gui_operational_acceptance.py`, the Config/Test contract tests, and the aggregate Suite test. Operator GUI evidence must cover all five surfaces, show the same request/plan/lifecycle hashes where applicable, preserve separate gameplay/music seed identity, and confirm no renderer/media/release side effects. No APPLY, freeze archive creation or physical production is part of D9.15.

### D9.16 — D9 final acceptance

**Current implementation status: PREFLIGHT PASS / FULL ACCEPTANCE BLOCKED AS REQUIRED.** The canonical full-acceptance preflight checks the D9.8–D9.16 evidence wiring, the five-surface topology, Config/Test registration, the immutable C11-C manifest hash, the D9.14 fail-closed gate and the D9.15 operator-evidence state. It provides a sealed record and 21 negative controls without executing the test suite recursively or creating files/media.

This is not D9.16 closure. Full acceptance still requires (1) authorized real-media GUI evidence for the required cases after a separately approved D frozen renderer baseline and an explicit D4.8 governance checkpoint, and (2) recorded operator GUI evidence across all five existing Suite surfaces. No local file, preflight, or button may unlock D4.8. `D9.14=BLOCKED`, `D9.15=OPERATOR_EVIDENCE_REQUIRED`, `renderer_activation=false`, `media_created=false`, and `release_authority=NONE` remain mandatory.

Run `python .\tools\c11d\d9\test_full_acceptance.py`, then the entire `python -u .\c11c-suite\self_test.py`. The preflight itself should report `PREFLIGHT_PASS_FULL_ACCEPTANCE_BLOCKED_AS_REQUIRED`; the aggregate suite PASS proves only that all gates correctly behave, not that physical real-media acceptance occurred.

### D9.17 — D9 closure adjudication (2026-10-09)

**Decision: BLOCKED — D9 remains OPEN. D9.17 has not achieved PASS/CLOSED.** The Windows-confirmed D9.16 preflight and 20/20 aggregate prove that the acceptance gates behave correctly; they do not satisfy the required acceptance payload. Two closure prerequisites remain unsatisfied:

1. **D9.14 real-media GUI certification:** the fail-closed gate is visible and executable in Producer and Test, but no authorized future D frozen renderer baseline exists, `D4.8=BLOCKED`, no D9.14 media evidence has been produced by the universal GUI, and `release_authority=NONE`. Do not route around this through the frozen C11-C renderer or legacy scripts. A separately approved D baseline and explicit governance checkpoint are required before real-media E2E can even be attempted.
2. **D9.15 operational evidence:** the preflight passes for 8 capabilities and 5 surfaces, but an evidence packet/log ledger showing operator actions and outcomes for Config, Producer, Test, Catalog and Maintenance has not been recorded as required. Individual GUI bring-ups and focused checks do not substitute for the complete capability-level evidence matrix.

D9.17 may be reconsidered only after both prerequisites are satisfied and D9.16 is rerun with complete evidence. Until then: `D9=OPEN`, `D9.17=BLOCKED`, `D10=BLOCKED`, `renderer_activation=false`, `media_created=false`, and `release_authority=NONE`. C11-C 2.19.12 and its historical freeze manifest remain immutable.

## Suite version/update plan

| Surface | Current/confirmed D9 version | Next target | Required acceptance |
|---|---:|---:|---|
| `c11c-suite` shell | 0.1.4 | keep 0.1.4 unless common launcher contract changes | full launcher/registry acceptance |
| `c11c-producer` | 0.11.1 | 0.11.x only for approved additive D coverage | universal request → editorial resolution → plan-only; real media remains a later authorized D gate |
| `c11c-catalog` | 0.2.0 | 0.2.x | product identity → provenance → reproduction |
| `c11c-config` | 0.2.0 | 0.2.x | profiles → validation → save/restore → protected roots |
| `c11c-maintenance` | 0.2.0 PASS/CLOSED; operator-confirmed Windows GUI and focused/regression tests passed | 0.2.0 | dry-run → reversible allowlist archive/quarantine → doc/freeze preflight |
| `c11c-test` | 0.2.0 implemented; D9.14/D9.15/D9.16 routes integrated; Windows D9.14 gate and D9.16 preflight confirmed | 0.2.0 | D2–D9 registration + full-acceptance preflight; real-media evidence remains blocked |

Versions labelled “next target” are planning targets, not claims of current release.

## D10 gate

D10 = **BLOCKED** until:

`D9.17 PASS/CLOSED`

and the GUI has successfully demonstrated the complete operator lifecycle for the unified content/editorial model.


## Parallel track — D baseline candidate evaluation (2026-10-09)

**Status: PREFLIGHT IMPLEMENTED / CANDIDATE NOT FREEZE-ELIGIBLE.** The user has elected to evaluate the integrated D tree as a future candidate baseline rather than treat C11-C 2.19.12 as the operating baseline for future D work. This does **not** supersede, mutate, or unfreeze C11-C: its historical manifest and protected core/assets/challenges/schemas/tests and critical engine entrypoints must continue matching their C11-C hashes.

Candidate identity: `C11-D-BASELINE-CANDIDATE-0.1`. Policy: `definitions/c11d/baseline/D_BASELINE_CANDIDATE_POLICY_V1.json`. Read-only evaluator: `tools/c11d/baseline_candidate/d_baseline_candidate.py`; test: `tools/c11d/baseline_candidate/test_d_baseline_candidate.py`; existing Test GUI route: `D BASELINE CANDIDATE INTEGRITY PREFLIGHT (NO FREEZE)`.

This candidate track is a source-integrity and readiness assessment only. It must not create a freeze/release archive, produce media, activate a renderer, grant D4.8, or grant release authority. The current run must report `PREFLIGHT_PASS_CANDIDATE_FREEZE_BLOCKED_AS_REQUIRED` while D9.14/D9.15/D9.16/D9.17 blockers remain. Candidate promotion requires a separate governance checkpoint and a new candidate identity/hash after the required real-media and five-surface operator evidence have been accepted. The legacy `c11d-control` path is not an active surface and remains an operator-controlled quarantine/disposition item; the preflight never moves it.


## D baseline candidate track (parallel, not a freeze)

The user has authorized evaluating the integrated D tree as a **candidate** future baseline in place of using C11-C as the active development baseline for D. C11-C 2.19.12 remains an immutable certified reference and is not altered or erased. Candidate identity: `C11-D-BASELINE-CANDIDATE-0.1`. The read-only integrity audit is registered in Config (policy access read-only) and Test (preflight route).

The candidate audit must return `PREFLIGHT_PASS_CANDIDATE_FREEZE_BLOCKED_AS_REQUIRED`: protected C source integrity may pass while freeze eligibility remains false. Current gates separately require: D9.14 real-media certification and D4.8 governance; consolidated D9.15 operator evidence; D9.16 full acceptance; D9.17 closure; an explicitly approved D renderer baseline checkpoint; a source-hash-bound D baseline approval checkpoint; and exact reconciliation of the four legacy `c11d-control` references through the append-only D9.11 ledger. A quarantine tree hash alone is insufficient if any archived file hash/size differs from the C manifest. No freeze package or release authority is created by the candidate-evaluation track.


### D baseline candidate remediation status (2026-10-09)

The candidate audit now prints per-file legacy quarantine mismatch names, verifies each manifest/ledger/archive hash, and requires a separate D baseline approval checkpoint in addition to renderer baseline approval. See `docs/current/d/D_BASELINE_CANDIDATE_REMEDIATION_PLAN_V1.md`. Its exit remains a pass of the audit with `freeze_eligible=false`; never interpret it as a freeze approval.

## Operator D9.15 capture waiver — candidate-only (2026-10-09)

The operator explicitly directs proceeding without collecting the 13 D9.15 screenshot/log pairings and states the five GUIs function. The sealed record `docs/current/d/D9.15_OPERATOR_EVIDENCE_WAIVER_CHECKPOINT.json` is honored **only by the D baseline-candidate readiness evaluator**. The candidate report must show `D9.15=WAIVED_NOT_EVIDENCED_FOR_CANDIDATE_ONLY`; this is not operational acceptance and does not change canonical D9.15 from `OPERATOR_EVIDENCE_REQUIRED`, nor the D9.17 `BLOCKED / NO-GO` adjudication. Five independent candidate blockers remain: D9.14 real-media authorization/evidence, D9.16 full acceptance, D9.17 closure, D renderer-baseline approval and D baseline approval. `D4.8=BLOCKED`, renderer/production OFF, no media, no freeze eligibility and release authority `NONE` remain mandatory.

## D9.10 D-only adapter implementation update (2026-10-09)

The earlier bridge-planning checkpoint has advanced to **adapter envelope preparation only**. `tools/c11d/d9/d_render_adapter.py` consumes the canonical D9.9 request/plan and D9.10 bridge record and emits a hash-bound binding preview. CLI and the existing test-only Producer GUI expose it; GUI/CLI envelope parity is covered for all three supported content types. The output is not renderer-native input. No dispatcher, render callback or production flag is added. Config now validates 30/30 canonical registry entries including the read-only adapter boundary.

`tools/c11d/d9/capture_d910_acceptance.py` automates focused backend/static GUI contract checks and writes hash-bound JSON plus command logs under `artifacts/tests/c11d_d9/d910_adapter_acceptance/`; no screenshots or media are required for those automated checks. Its report explicitly says the Qt GUI was not interactively observed. The test GUI remains test-only; definitive GUI work is deferred until after the final D baseline is closed and frozen.

## D9.14 bounded production qualification result (2026-10-09)

Windows run `D914_COLON_FIX_20261009_E` passed and sealed a qualification-only baseline with 4 final A/V MP4s and 8 checks. Report SHA-256: `daa5e5676224d606e9d67ac7a7ed7e88c3c02a63c76ecdc579c3bc2dd320853f`; qualification baseline SHA-256: `15343119f0f8338b13b47b0ea98546e5470d4a1a8895b65dbe1f41ee183e66d3`. Challenge Music Engine V5 mux, deterministic Loop replay and music-seed isolation passed. This is bounded smoke qualification using established launchers; it is not full D9.14 GUI certification, D4.8 authorization, general renderer activation, final baseline approval or release.

## D9.10 offscreen Qt GUI automation — 2026-10-09

The default D9.10 automated acceptance has passed 5/5 checks in Windows, the candidate preflight passes with five blockers retained, and the aggregate Suite passed 21/21 after restoring both manifest-pinned historical README files. To replace optional manual screenshots with machine evidence, `test_d910_gui_runtime_acceptance.py` exercises the existing Producer test GUI offscreen for all three supported content types and checks that an explicit editorial override arrives in the D-only prepared envelope with exact GUI/CLI parity. Use `capture_d910_acceptance.py --include-qt-gui-runtime --include-aggregate` for one bound report. The offscreen runtime test is prepared but not yet executed in the package preparation environment because PySide6 is unavailable there; Windows must record its result. No renderer input or media is emitted by this test.

The test/operator GUI remains temporary acceptance tooling. The definitive GUI remains deferred until the final D baseline has been accepted, D9 has been closed and that baseline is frozen. D4.8 remains BLOCKED, D9.14 full E2E/D9.16/D9.17 remain open gates, and release authority remains NONE.


## D9.10 Qt runtime acceptance closure — 2026-10-09

Operator-confirmed Windows result:

- Direct offscreen Qt runtime `D910_QT_GUI_RUNTIME_FIX_02`: PASS, `content_types=3/3`, C11-C manifest match true, renderer OFF, media false.
- Combined `D910_QT_ACCEPTANCE_FIX_02`: PASS, checks 7/7; the `GUI_runtime_observed=false` field remains intentionally truthful because the GUI was automated/offscreen.
- D9.13 lifecycle: PASS, content types 3/3, stages 5/5, parity 3/3, catalog projection 3/3, maintenance audit 3/3, negative 14/14, persisted parity regression 4/4.
- Aggregate Suite: PASS 22/22.
- Candidate preflight: PASS as a readiness audit, still `freeze_eligible=false` with five blockers; baseline approval missing; C11-C immutable reference match.

The D9.10 Qt-runtime sub-gate is accepted. This does not close D9.14, D9.15 canonical operator evidence, D9.16 or D9.17. No D4.8 authorization, renderer activation, production/media, freeze or release authority is granted. See `D9.10_QT_GUI_RUNTIME_ACCEPTANCE_CHECKPOINT.md` and incident history for the root cause and evidence.


## Latest Windows confirmation — D9.15 checkpoint consumption complete (2026-10-09)

The operator-confirmed latest run now establishes: D9.15 canonical operational acceptance PASS/CLOSED (13/13; checkpoint `2e3b9d591288ba77259ee650685ba16deb12abcf770c123406612a5efbe309f5`; ledger `dda1c150ab18a7fbe0c4e531997b6f3d30fc121b58f22552762d53b79ed488fa`); D9.15 static preflight 8/8 capabilities, 5/5 surfaces, negative 19/19; D9.14 gate PASS as `BLOCKED_AS_REQUIRED` (10/10 cases, 20/20 negatives); D9.16 preflight PASS (5/5 static checks, 9/9 evidence routes, 21/21 negatives, `D9.15_operator_evidence=PASS_CLOSED`, overall full acceptance blocked); candidate preflight PASS with five remaining blockers and `freeze_eligible=false`; aggregate Suite PASS 22/22. The historical candidate-only D9.15 waiver is superseded for current operational status by the validated canonical checkpoint.

**Next active work:** prepare and statically verify a separately versioned D-owned renderer baseline candidate under `D_RENDERER_BASELINE_PREPARATION_PLAN_V1.md`. This is engineering preparation only. Do not dispatch the D9.10 envelope, run D9.14 real-media GUI E2E, change the production activation policy, or create approval checkpoints before independent renderer review and explicit D4.8 governance authorization. C11-C and its manifest remain immutable.
